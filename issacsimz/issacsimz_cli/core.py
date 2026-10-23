from __future__ import annotations

import json
import hashlib
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tarfile
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from pathlib import PurePosixPath
from typing import Any

from .artifacts import copy_download_handoff, copy_tree, make_evidence_dir, sha256_file, write_json, write_manifest
from .checkpoints import CheckpointWatcher
from .telemetry import GpuMonitor, nvidia_snapshot, runtime_report
from .safety import is_sensitive_path


def default_log_root(value: str | None) -> Path:
    default = Path.home() / ".local" / "share" / "issacsimz"
    return Path(value or os.environ.get("ISSACSIMZ_LOG_ROOT", str(default))).expanduser().resolve()


def run_id(log_root: Path, name: str) -> str:
    safe = "".join(char if char.isalnum() or char in "._-" else "-" for char in name).strip(".-") or "run"
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    base, candidate, index = f"{stamp}-{safe[:48]}", "", 1
    candidate = base
    while (log_root / "runs" / candidate).exists():
        candidate = f"{base}-{index:03d}"
        index += 1
    return candidate


def _evidence_run(log_root: Path, identifier: str) -> Path:
    if not identifier or Path(identifier).name != identifier or identifier in {".", ".."}:
        raise ValueError("run ID must be one evidence directory name (no path separators)")
    runs_root = (log_root / "runs").resolve()
    source = (runs_root / identifier).resolve()
    if source.parent != runs_root or not source.is_dir():
        raise FileNotFoundError(f"evidence run not found: {identifier}")
    return source


def _tree_size(source: Path) -> int:
    total = 0
    for path in source.rglob("*"):
        try:
            if path.is_file():
                total += path.stat().st_size
        except OSError:
            continue
    return total


def _snapshot_run_directories(run_root: Path | None) -> set[Path]:
    if run_root is None or not run_root.is_dir():
        return set()
    try:
        return {path.resolve() for path in run_root.iterdir() if path.is_dir()}
    except OSError:
        return set()


def _detect_new_native_run(run_root: Path | None, initial_runs: set[Path]) -> Path | None:
    """Find a run once after completion without starting a watcher thread."""
    if run_root is None or not run_root.is_dir():
        return None
    try:
        candidates = [path for path in run_root.iterdir() if path.is_dir() and path.resolve() not in initial_runs]
        return max(candidates, key=lambda path: path.stat().st_mtime) if candidates else None
    except OSError:
        return None


def _checkpoint_state(roots: list[Path | None]) -> dict[str, tuple[int, int]]:
    """Capture a cheap pre/post state; checkpoint bytes are hashed only after training."""
    state: dict[str, tuple[int, int]] = {}
    for root in roots:
        if root is None or not root.is_dir():
            continue
        try:
            candidates = root.rglob("model_*.pt")
            for path in candidates:
                if path.is_symlink() or not path.is_file() or not re.fullmatch(r"model_\d+\.pt", path.name):
                    continue
                resolved = path.resolve()
                try:
                    resolved.relative_to(root.resolve())
                except ValueError:
                    continue
                stat = resolved.stat()
                if stat.st_size <= 0:
                    continue
                state[str(resolved)] = (stat.st_size, stat.st_mtime_ns)
        except OSError:
            continue
    return state


def _checkpoint_index(before: dict[str, tuple[int, int]], native_run: Path | None,
                      keeper_root: Path) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    checkpoints: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []
    roots = (("official_native_run", native_run), ("organizer_keeper_backup", keeper_root))
    for origin, root in roots:
        if root is None or not root.is_dir():
            continue
        try:
            candidates = sorted(root.rglob("model_*.pt"))
        except OSError as exc:
            errors.append({"path": str(root), "error": f"{type(exc).__name__}: {exc}"})
            continue
        for path in candidates:
            if path.is_symlink() or not path.is_file() or not re.fullmatch(r"model_\d+\.pt", path.name):
                continue
            try:
                resolved = path.resolve()
                try:
                    resolved.relative_to(root.resolve())
                except ValueError:
                    errors.append({"path": str(path), "error": "checkpoint resolves outside approved root"})
                    continue
                stat = resolved.stat()
                if stat.st_size <= 0:
                    errors.append({"path": str(path), "error": "checkpoint is empty"})
                    continue
                current = (stat.st_size, stat.st_mtime_ns)
                if before.get(str(resolved)) == current:
                    continue
                checkpoints.append({
                    "filename": resolved.name,
                    "source_path": str(resolved),
                    "origin": origin,
                    "size": stat.st_size,
                    "sha256": sha256_file(resolved),
                })
            except OSError as exc:
                errors.append({"path": str(path), "error": f"{type(exc).__name__}: {exc}"})
    return checkpoints, errors


def archive_run(log_root: Path, identifier: str, output_dir: str | None = None, *, force: bool = False) -> tuple[Path, Path]:
    source = _evidence_run(log_root, identifier)
    target_dir = Path(output_dir).expanduser().resolve() if output_dir else (log_root / "exports").resolve()
    try:
        target_dir.relative_to(source)
    except ValueError:
        pass
    else:
        raise ValueError("archive output must be outside its evidence directory")
    target_dir.mkdir(parents=True, exist_ok=True)
    evidence_bytes = _tree_size(source)
    safety_margin = max(64 * 1024 * 1024, evidence_bytes // 10)
    required = evidence_bytes + safety_margin
    free = shutil.disk_usage(target_dir).free
    if free < required:
        raise OSError(f"insufficient free disk for archive: need at least {required} bytes, have {free}")
    try:
        status = json.loads((source / "metadata.json").read_text(encoding="utf-8")).get("status")
    except (OSError, json.JSONDecodeError):
        status = None
    suffix = "_INTERRUPTED" if status == "interrupted" else ("_FAILED" if status == "failed" else "")
    archive = target_dir / f"{identifier}{suffix}.tar.gz"
    digest = archive.with_suffix(archive.suffix + ".sha256")
    pack_metadata = archive.with_suffix(archive.suffix + ".metadata.json")
    existing = [path for path in (archive, digest, pack_metadata) if path.exists()]
    if existing and not force:
        raise FileExistsError(f"archive output already exists: {existing[0]}; use --force to replace")
    temporary = archive.with_suffix(".tar.gz.part")
    temporary.unlink(missing_ok=True)
    started = time.perf_counter()
    try:
        with tarfile.open(temporary, "w:gz", format=tarfile.PAX_FORMAT, compresslevel=1) as tar:
            tar.add(source, arcname=identifier, recursive=True)
        with tarfile.open(temporary, "r:gz") as tar:
            if not tar.getmembers():
                raise OSError("empty archive")
        temporary.replace(archive)
    finally:
        temporary.unlink(missing_ok=True)
    digest.write_text(f"{sha256_file(archive)}  {archive.name}\n", encoding="utf-8")
    pack_info = {
        "schema_version": 1,
        "run_id": identifier,
        "pack_duration_sec": round(time.perf_counter() - started, 3),
        "evidence_bytes": evidence_bytes,
        "archive_bytes": archive.stat().st_size,
        "free_bytes_before": free,
        "required_free_bytes": required,
    }
    write_json(pack_metadata, pack_info)
    return archive, digest


def _stream_sha256(stream) -> str:
    digest = hashlib.sha256()
    for block in iter(lambda: stream.read(1024 * 1024), b""):
        digest.update(block)
    return digest.hexdigest()


def verify_archive(archive: Path, *, require_sidecar: bool = False) -> dict[str, Any]:
    """Verify an archive without extracting it to the filesystem."""
    archive = archive.expanduser().resolve()
    report: dict[str, Any] = {"archive": str(archive), "ok": False, "errors": [], "checked_files": 0}
    if not archive.is_file():
        report["errors"].append("archive does not exist")
        return report
    sidecar = archive.with_suffix(archive.suffix + ".sha256")
    if sidecar.is_file():
        expected = sidecar.read_text(encoding="utf-8").split()[0]
        actual = sha256_file(archive)
        if expected != actual:
            report["errors"].append("archive sidecar SHA-256 does not match")
    elif require_sidecar:
        report["errors"].append("archive SHA-256 sidecar is missing")
    try:
        with tarfile.open(archive, "r:gz") as tar:
            members = {member.name: member for member in tar.getmembers() if member.isfile()}
            for name in members:
                path = PurePosixPath(name)
                if path.is_absolute() or ".." in path.parts:
                    report["errors"].append(f"unsafe archive member: {name}")
            manifest_name = next((name for name in members if name.endswith("/SHA256SUMS")), None)
            metadata_name = next((name for name in members if name.endswith("/metadata.json")), None)
            validation_name = next((name for name in members if name.endswith("/validation.json")), None)
            if not manifest_name:
                report["errors"].append("SHA256SUMS missing from archive")
                return report
            if not metadata_name:
                report["errors"].append("metadata.json missing from archive")
            else:
                metadata_stream = tar.extractfile(members[metadata_name])
                assert metadata_stream is not None
                try:
                    metadata = json.loads(metadata_stream.read().decode("utf-8"))
                    report["metadata"] = {
                        "run_id": metadata.get("run_id"),
                        "status": metadata.get("status"),
                        "operation": metadata.get("operation"),
                        "evidence_validation": metadata.get("evidence_validation"),
                    }
                except (UnicodeDecodeError, json.JSONDecodeError):
                    report["errors"].append("metadata.json is not valid UTF-8 JSON")
                    metadata = {}
                if metadata.get("operation") == "train" and metadata.get("status") == "completed":
                    required_suffixes = (
                        "/native_run/events.out.tfevents.fixture",
                        "/checkpoints/model_",
                        "/collected/exported/model_best.pt",
                        "/collected/exported/env.yaml",
                    )
                    names = tuple(members)
                    if not any("/native_run/" in name and "/events.out.tfevents" in name for name in names):
                        report["errors"].append("completed train archive lacks native TensorBoard event")
                    if metadata.get("mode") != "official" and not any("/checkpoints/model_" in name and name.endswith(".pt") for name in names):
                        report["errors"].append("completed train archive lacks mirrored checkpoint")
                    for relative in required_suffixes[2:]:
                        if not any(name.endswith(relative) for name in names):
                            report["errors"].append(f"completed train archive lacks {relative.rsplit('/', 1)[-1]}")
            if not validation_name:
                report["errors"].append("validation.json missing from archive")
            prefix = manifest_name.removesuffix("SHA256SUMS")
            manifest_stream = tar.extractfile(members[manifest_name])
            assert manifest_stream is not None
            manifest_lines = manifest_stream.read().decode("utf-8", errors="replace").splitlines()
            for line in manifest_lines:
                try:
                    expected, relative = line.split("  ", 1)
                except ValueError:
                    report["errors"].append(f"invalid manifest line: {line}")
                    continue
                member = members.get(prefix + relative)
                if not member:
                    report["errors"].append(f"manifest file missing: {relative}")
                    continue
                stream = tar.extractfile(member)
                assert stream is not None
                if _stream_sha256(stream) != expected:
                    report["errors"].append(f"manifest SHA-256 mismatch: {relative}")
                report["checked_files"] += 1
    except (OSError, tarfile.TarError) as exc:
        report["errors"].append(f"archive read failure: {type(exc).__name__}: {exc}")
    report["ok"] = not report["errors"]
    return report


def list_evidence_runs(log_root: Path) -> list[dict[str, Any]]:
    runs_root = (log_root / "runs").resolve()
    records: list[dict[str, Any]] = []
    if not runs_root.is_dir():
        return records
    for directory in sorted((path for path in runs_root.iterdir() if path.is_dir()), reverse=True):
        metadata_path = directory / "metadata.json"
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            metadata = {"status": "unreadable"}
        records.append({"run_id": directory.name, "metadata": metadata})
    return records


def _send_sigint(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    if os.name == "nt":
        process.send_signal(signal.CTRL_BREAK_EVENT)
    else:
        os.killpg(process.pid, signal.SIGINT)


def _force_stop(process: subprocess.Popen[str]) -> int:
    if process.poll() is not None:
        return process.returncode
    if os.name == "nt":
        process.terminate()
    else:
        os.killpg(process.pid, signal.SIGTERM)
    try:
        return process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        if os.name == "nt":
            process.kill()
        else:
            os.killpg(process.pid, signal.SIGKILL)
        return process.wait()


def _interrupt_then_wait(process: subprocess.Popen[str], *, allow_force_stop: bool = True) -> tuple[int, bool]:
    """First Ctrl+C preserves the official cleanup path; a second is force stop."""
    _send_sigint(process)
    if allow_force_stop:
        message = "SIGINT sent once; waiting for train.py finalize/official backup. Press Ctrl+C again only to force stop."
    else:
        message = "SIGINT sent once; waiting for train.py finalize/official backup. Additional Ctrl+C is disabled in official mode."
    print(f"[issacsimz] {message}", file=sys.stderr)
    while True:
        try:
            return process.wait(), False
        except KeyboardInterrupt:
            if not allow_force_stop:
                print("[issacsimz] additional Ctrl+C ignored in official mode; waiting for native finalize/backup.", file=sys.stderr)
                continue
            print("[issacsimz] second Ctrl+C: force stopping process group; official finalize/backup may be incomplete.", file=sys.stderr)
            return _force_stop(process), True


def _snapshot_tree(source: Path) -> dict[str, dict[str, int | str]]:
    snapshot: dict[str, dict[str, int | str]] = {}
    if not source.is_dir():
        return snapshot
    for path in source.rglob("*"):
        if not path.is_file():
            continue
        try:
            relative = path.relative_to(source)
            if is_sensitive_path(relative):
                continue
            stat = path.stat()
            snapshot[relative.as_posix()] = {"size": stat.st_size, "mtime_ns": stat.st_mtime_ns, "sha256": sha256_file(path)}
        except OSError:
            continue
    return snapshot


def _collect_changed_files(source: Path, destination: Path, before: dict[str, dict[str, int | str]]) -> list[dict[str, int | str]]:
    records: list[dict[str, int | str]] = []
    if not source.is_dir():
        return records
    for path in source.rglob("*"):
        if not path.is_file():
            continue
        try:
            relative_path = path.relative_to(source)
            if is_sensitive_path(relative_path):
                records.append({"path": relative_path.as_posix(), "status": "SKIPPED_SENSITIVE"})
                continue
            stat = path.stat()
            relative = relative_path.as_posix()
            current: dict[str, int | str] = {"path": relative, "size": stat.st_size, "mtime_ns": stat.st_mtime_ns, "sha256": sha256_file(path)}
        except OSError as exc:
            records.append({"path": str(path), "status": "ERROR", "error": f"{type(exc).__name__}: {exc}"})
            continue
        previous = before.get(relative)
        unchanged = previous and all(previous[key] == current[key] for key in ("size", "mtime_ns", "sha256"))
        current["status"] = "UNCHANGED" if unchanged else ("MODIFIED" if previous else "NEW")
        if not unchanged:
            target = destination / relative
            try:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, target)
            except OSError as exc:
                current["copy_error"] = f"{type(exc).__name__}: {exc}"
        records.append(current)
    return records


def _source_paths(task_root: Path, profile: Any) -> list[Path]:
    package = getattr(profile, "task_package", "")
    reward = getattr(profile, "reward_file", "")
    relative = {Path("train.py"), Path("play.py"), Path(reward), Path("pyproject.toml")}
    if package:
        relative.update(Path(package) / name for name in ("_finalize.py", "env_cfg.py", "agent_cfg.py", "__init__.py"))
    excluded = {
        ".git", "__pycache__", "logs", "exported", "evidence", "downloads",
        "issacsimz_download", "backup_log", ".pytest_cache", ".mypy_cache",
    }
    for directory, names, files in os.walk(task_root, followlinks=False):
        names[:] = [
            name for name in names
            if name.lower() not in excluded and not (Path(directory) / name).is_symlink()
        ]
        parent = Path(directory)
        for name in files:
            if name.endswith(".py"):
                relative.add((parent / name).relative_to(task_root))
    return sorted((path for path in relative if str(path) not in {"", "."}), key=lambda path: path.as_posix())


def _capture_source_identity(task_root: Path, profile: Any, source_dir: Path) -> dict[str, Any]:
    files: list[dict[str, Any]] = []
    source_dir.mkdir(parents=True, exist_ok=True)
    for relative in _source_paths(task_root, profile):
        path = task_root / relative
        item: dict[str, Any] = {"path": relative.as_posix(), "exists": path.is_file()}
        if path.is_file():
            try:
                item.update({"size": path.stat().st_size, "sha256": sha256_file(path)})
                if relative.name == getattr(profile, "reward_file", ""):
                    shutil.copy2(path, source_dir / relative.name)
            except OSError as exc:
                item["error"] = f"{type(exc).__name__}: {exc}"
        files.append(item)
    return {
        "schema_version": 2,
        "task_root": str(task_root),
        "profile": getattr(profile, "robot", None),
        "selection": "required profile files plus all task-root Python files; dynamic directories excluded",
        "hashed_paths": [item["path"] for item in files if item.get("sha256")],
        "files": files,
    }


def _compare_source_identity(before: dict[str, Any], task_root: Path, profile: Any) -> dict[str, Any]:
    initial = {item["path"]: item for item in before["files"]}
    changed: list[str] = []
    after: list[dict[str, Any]] = []
    relative_paths = {Path(path) for path in initial}
    relative_paths.update(_source_paths(task_root, profile))
    for relative in sorted(relative_paths, key=lambda path: path.as_posix()):
        path = task_root / relative
        item: dict[str, Any] = {"path": relative.as_posix(), "exists": path.is_file()}
        if path.is_file():
            try:
                item.update({"size": path.stat().st_size, "sha256": sha256_file(path)})
            except OSError as exc:
                item["error"] = f"{type(exc).__name__}: {exc}"
        prior = initial.get(item["path"], {})
        did_change = prior.get("exists") != item.get("exists") or prior.get("sha256") != item.get("sha256")
        prior["after_exists"] = item.get("exists", False)
        prior["after_size"] = item.get("size")
        prior["after_sha256"] = item.get("sha256")
        prior["changed_during_run"] = did_change
        if did_change:
            changed.append(item["path"])
        after.append(item)
    before["after_files"] = after
    before["after_hashed_paths"] = [item["path"] for item in after if item.get("sha256")]
    before["changed_during_run"] = bool(changed)
    before["changed_paths"] = changed
    return before


def _backup_line_status(line: str) -> str | None:
    lower = line.lower()
    if "[backup]" not in lower:
        return None
    if "no_auto_submit" in lower:
        return "skipped_disabled"
    if "model_best.pt/env.yaml" in lower or "missing artifacts" in lower:
        return "skipped_missing_artifacts"
    if "백업 서버 설정 없음" in line or ("no backup" in lower and "config" in lower):
        return "skipped_no_config"
    if "백업 완료" in line or "✅" in line or "backup complete" in lower:
        return "success"
    if any(token in line for token in ("백업 실패", "연결 실패", "❌")) or any(token in lower for token in ("failed", "failure", "error", "자동 백업 skip")):
        return "failed"
    return "unknown"


def _finalize_line_state(line: str) -> str | None:
    lower = line.lower()
    if "[post]" in lower and ("학습 종료" in line or "training" in lower):
        return "started"
    if "[done]" in lower and ("예선 제출 결과물" in line or "finalize" in lower):
        return "completed"
    return None


def _backup_environment(workdir: Path) -> dict[str, bool]:
    config_candidates = {Path("/workspace/submit_config.txt"), workdir.parent.parent / "submit_config.txt"}
    config_present = any(path.is_file() for path in config_candidates)
    host_present = "SUBMIT_HOST" in os.environ
    token_present = "SUBMIT_TOKEN" in os.environ
    return {
        "submit_config_present": config_present,
        "submit_host_present": host_present,
        "submit_token_present": token_present,
        "submit_credentials_present": host_present and token_present,
    }


def _validate_evidence(evidence: Path, metadata: dict[str, Any], source_identity: dict[str, Any] | None,
                       provenance: list[dict[str, Any]]) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    def add(name: str, status: str, detail: str) -> None:
        checks.append({"name": name, "status": status, "detail": detail})
    operation = metadata.get("operation")
    if operation not in {"play", "video"}:
        if metadata["native_run_detected"] is False:
            add("native_run", "WARN", "native run was not detected")
        elif metadata["native_run_detected"] is True:
            add("native_run", "PASS", "native run copied")
        else:
            add("native_run", "WARN", "run-root was not supplied")
        events = list((evidence / "native_run").rglob("events.out.tfevents*"))
        add("tensorboard", "PASS" if events else "WARN", f"events={len(events)}")
        if metadata.get("mode") != "official":
            count = int(metadata["checkpoint_count"])
            add("checkpoints", "PASS" if count else "WARN", f"mirrored={count}")
        elif operation == "train":
            keeper = metadata.get("organizer_keeper") or {}
            count = int(metadata.get("organizer_checkpoint_count", 0))
            kept = keeper.get("exit_code") == 0 and count > 0
            add("organizer_checkpoints", "PASS" if kept else ("FAIL" if metadata["training_status"] == "completed" else "WARN"),
                f"copied={count} exit={keeper.get('exit_code')} error={keeper.get('error')}")
    if source_identity is None:
        add("source_identity", "WARN", "generic run has no profile source identity")
    elif any(not item.get("exists") for item in source_identity.get("files", [])):
        add("source_identity", "FAIL", "one or more required source files were missing")
    elif source_identity.get("changed_during_run"):
        add("source_identity", "FAIL", "tracked source changed during run")
    else:
        add("source_identity", "PASS", "before/after hashes match")
    if operation not in {"play", "video"}:
        backup = metadata["official_backup_status"]
        if metadata["official_backup_expected"] and backup != "success":
            add("official_backup", "FAIL", f"expected=true status={backup}")
        elif backup == "failed":
            add("official_backup", "WARN", f"status={backup}")
        elif backup == "unknown":
            add("official_backup", "WARN", "no conclusive backup log")
        else:
            add("official_backup", "PASS", f"status={backup}")
    if metadata["collection_errors"]:
        add("collection", "WARN", f"copy errors={len(metadata['collection_errors'])}")
    else:
        add("collection", "PASS", f"new_or_modified={metadata['collected_file_count']}")
    if operation in {"play", "video"} and metadata.get("mode") == "official":
        lineage_ok = bool(
            metadata.get("source_provenance_verified")
            and metadata.get("source_evidence_run_id")
            and metadata.get("source_run_mode") == "official"
        )
        add(
            "official_checkpoint_provenance", "PASS" if lineage_ok else "FAIL",
            f"run={metadata.get('source_evidence_run_id')} "
            f"mode={metadata.get('source_run_mode')} "
            f"origin={metadata.get('source_checkpoint_origin')}",
        )
    if metadata.get("operation") == "train":
        successful = metadata["training_status"] == "completed"
        exported_records = [record for collection in provenance if Path(collection["source"]).name == "exported" for record in collection["files"]]
        for required_name in ("model_best.pt", "env.yaml"):
            matches = [record for record in exported_records if record.get("path") == required_name]
            fresh = any(record.get("status") in {"NEW", "MODIFIED"} and "copy_error" not in record for record in matches)
            add(f"exported_{required_name}", "PASS" if fresh else ("FAIL" if successful else "WARN"), "NEW/MODIFIED" if fresh else "not produced by this run")
        if successful and metadata["official_finalize_status"] != "completed":
            add("official_finalize", "FAIL", f"status={metadata['official_finalize_status']}")
        else:
            add("official_finalize", "PASS" if metadata["official_finalize_status"] == "completed" else "WARN", f"status={metadata['official_finalize_status']}")
    if metadata.get("operation") == "video":
        exported_records = [record for collection in provenance if Path(collection["source"]).name == "exported" for record in collection["files"]]
        matches = [record for record in exported_records if record.get("path") == "play_video.mp4"]
        prepared = metadata.get("prepared_checkpoint") or {}
        isolated = prepared.get("strategy") == "isolated_copy"
        promoted = set(prepared.get("promoted_outputs") or [])
        fresh = any(
            record.get("status") in {"NEW", "MODIFIED"}
            and "copy_error" not in record
            and int(record.get("size", 0)) > 0
            for record in matches
        )
        if isolated and "play_video.mp4" not in promoted:
            fresh = False
        add("exported_play_video.mp4", "PASS" if fresh else "FAIL",
            "fresh non-empty official exported/play_video.mp4" if fresh else
            "not produced and promoted from this play run")
    overall = "FAIL" if any(item["status"] == "FAIL" for item in checks) else ("WARN" if any(item["status"] == "WARN" for item in checks) else "PASS")
    return {"schema_version": 1, "overall": overall, "checks": checks}


def run_command(args) -> int:
    command = list(args.command)
    if command[:1] == ["--"]:
        command = command[1:]
    if not command:
        raise ValueError("run requires a command after --")
    log_root = default_log_root(args.log_root)
    identifier = run_id(log_root, args.name)
    mode = os.environ.get("ISSACSIMZ_MODE", "").strip().lower()
    operation = getattr(args, "profile_operation", "run")
    if operation in {"train", "play", "video"} and mode not in {"personal", "official"}:
        if not mode:
            raise ValueError(f"ISSACSIMZ_MODE is not set; use bootstrap before {operation}")
        raise ValueError(f"unsupported ISSACSIMZ_MODE for {operation}: {mode}")
    if operation == "run" and mode != "personal":
        if not mode:
            raise ValueError("ISSACSIMZ_MODE is not set; use bootstrap before run")
        if mode not in {"personal", "official"}:
            raise ValueError(f"unsupported ISSACSIMZ_MODE for run: {mode}")
        raise ValueError("run requires ISSACSIMZ_MODE=personal; current mode=official")
    official_mode = mode == "official"
    keeper_script = None
    if official_mode and operation == "train":
        script_root = Path(__file__).resolve().parents[1]
        if not (script_root / "scripts" / "organizer_keep_all_ckpt.sh").is_file():
            script_root = Path(sys.argv[0]).resolve().parent.parent
        keeper_script = script_root / "scripts" / "organizer_keep_all_ckpt.sh"
        if not keeper_script.is_file():
            raise FileNotFoundError(f"official checkpoint keeper script not found: {keeper_script}")
    evidence = make_evidence_dir(log_root, identifier, checkpoint_mirror=not official_mode)
    collection_sources = [Path(item).expanduser().resolve() for item in args.collect]
    collection_before = {str(source): _snapshot_tree(source) for source in collection_sources}
    workdir = Path(args.workdir or Path.cwd()).expanduser().resolve()
    profile = getattr(args, "source_profile", None)
    source_identity = _capture_source_identity(workdir, profile, evidence / "source") if profile else None
    if source_identity:
        write_json(evidence / "source" / "identity.json", source_identity)
    backup_environment = _backup_environment(workdir)
    backup_expected = backup_environment["submit_config_present"] or backup_environment["submit_credentials_present"]
    native_run_root = Path(args.run_root).expanduser().resolve() if args.run_root else None
    initial_native_runs = _snapshot_run_directories(native_run_root) if official_mode else set()
    keeper_root = (workdir / "backup_log").resolve()
    checkpoint_state_before = _checkpoint_state([native_run_root, keeper_root]) \
        if official_mode and operation == "train" else {}
    metadata: dict[str, Any] = {
        "schema_version": 3, "run_id": identifier, "name": args.name, "command": command,
        "profile": getattr(profile, "robot", None), "operation": operation,
        "working_directory": str(workdir), "start_utc": datetime.now(timezone.utc).isoformat(), "end_utc": None,
        "exit_code": None, "status": "running", "training_status": "running", "official_finalize_status": "not_started",
        "official_backup_status": "unknown", "official_backup_expected": backup_expected,
        "official_backup_environment": backup_environment, "native_run": None, "native_run_detected": None,
        "checkpoint_count": 0, "collected_file_count": 0, "collection_errors": [], "warnings": [],
        "environment_guards": getattr(args, "environment_guards", {}),
        "parent_run_id": getattr(args, "parent_run_id", None),
        "video_label": getattr(args, "video_label", None),
        "source_checkpoint": getattr(args, "source_checkpoint", None),
        "source_checkpoint_sha256": getattr(args, "source_checkpoint_sha256", None),
        "source_evidence_run_id": getattr(args, "source_evidence_run_id", None),
        "source_run_mode": getattr(args, "source_run_mode", None),
        "source_evidence_validation": getattr(args, "source_evidence_validation", None),
        "source_checkpoint_origin": getattr(args, "source_checkpoint_origin", None),
        "source_provenance_verified": getattr(args, "source_provenance_verified", False),
        "prepared_checkpoint": getattr(args, "prepared_checkpoint", None),
        "native_output_roots": getattr(args, "native_output_roots", None),
        "resume_lineage": getattr(args, "resume_lineage", None),
        "mode": mode or None,
        "gpu_monitor_enabled": not official_mode,
        "checkpoint_mirror_enabled": not official_mode,
        "source_mutation": "none; issacsimz only observes and copies files",
    }
    (evidence / "command.txt").write_text(shlex.join(command) + "\n", encoding="utf-8")
    write_json(evidence / "metadata.json", metadata)
    runtime_report(evidence / "system" / "runtime.txt")
    nvidia_snapshot(evidence / "system" / "nvidia_smi_before.txt")
    gpu = None if official_mode else GpuMonitor(evidence / "system" / "nvidia_smi_during.csv", args.gpu_interval)
    watcher = CheckpointWatcher(native_run_root, evidence / "checkpoints", start_time=time.time(), interval=args.poll_seconds, log_path=evidence / "watcher.log") if native_run_root and not official_mode else None
    signals = {"finalize": "not_started", "backup": "unknown"}
    signal_lock = threading.Lock()

    def consume(line: str, console) -> None:
        sys.stdout.write(line)
        sys.stdout.flush()
        console.write(line)
        console.flush()
        with signal_lock:
            finalize_state = _finalize_line_state(line)
            if finalize_state == "started":
                signals["finalize"] = "started"
                if watcher:
                    watcher.scan(final=True)
            elif finalize_state == "completed":
                signals["finalize"] = "completed"
            status = _backup_line_status(line)
            if status:
                signals["backup"] = status

    if gpu:
        gpu.start()
    if watcher:
        watcher.start()
    process: subprocess.Popen[str] | None = None
    reader: threading.Thread | None = None
    keeper_thread: threading.Thread | None = None
    keeper_result: dict[str, Any] = {"exit_code": None, "native_run": None, "error": None}
    interrupted, forced_stop, launch_error, code = False, False, None, 1
    options: dict[str, Any] = {"cwd": str(workdir), "stdout": subprocess.PIPE, "stderr": subprocess.STDOUT, "text": True, "bufsize": 1, "errors": "replace"}
    if os.name != "nt":
        options["start_new_session"] = True
    try:
        process = subprocess.Popen(command, **options)
        if keeper_script is not None:
            def run_keeper() -> None:
                while process.poll() is None:
                    found = _detect_new_native_run(native_run_root, initial_native_runs)
                    if found:
                        break
                    time.sleep(0.2)
                else:
                    found = _detect_new_native_run(native_run_root, initial_native_runs)
                if found is None:
                    keeper_result["error"] = "native run was not detected"
                    return
                keeper_result["native_run"] = str(found)
                try:
                    with (evidence / "system" / "organizer_keep_all.log").open("w", encoding="utf-8") as stream:
                        keeper = subprocess.Popen(
                            ["bash", str(keeper_script), str(workdir), str(found), str(process.pid)],
                            cwd=str(workdir), stdout=stream, stderr=subprocess.STDOUT,
                            start_new_session=os.name != "nt",
                        )
                        keeper_result["exit_code"] = keeper.wait()
                except OSError as exc:
                    keeper_result["error"] = f"{type(exc).__name__}: {exc}"
            keeper_thread = threading.Thread(target=run_keeper, name="issacsimz-organizer-keeper", daemon=True)
            keeper_thread.start()
        assert process.stdout is not None
        console = (evidence / "console.log").open("a", encoding="utf-8")
        def drain() -> None:
            try:
                for line in process.stdout:
                    consume(line, console)
            finally:
                process.stdout.close()
                console.close()
        reader = threading.Thread(target=drain, name="issacsimz-console-reader", daemon=True)
        reader.start()
        try:
            code = process.wait()
        except KeyboardInterrupt:
            interrupted = True
            code, forced_stop = _interrupt_then_wait(process, allow_force_stop=not official_mode)
        reader.join(timeout=60)
        if reader.is_alive():
            metadata["warnings"].append("console reader did not finish within 60 seconds")
        post_run = getattr(args, "_post_run", None)
        if post_run is not None:
            try:
                post_run()
            except OSError as exc:
                error = {"source": "post_run", "error": f"{type(exc).__name__}: {exc}"}
                metadata["collection_errors"].append(error)
                print(f"[issacsimz] WARNING play output collection failed: {exc}", file=sys.stderr)
    except (OSError, subprocess.SubprocessError) as exc:
        launch_error = f"{type(exc).__name__}: {exc}"
        with (evidence / "console.log").open("a", encoding="utf-8") as console:
            console.write(f"[issacsimz] launch failure: {launch_error}\n")
    finally:
        if keeper_thread:
            keeper_thread.join()
        if watcher:
            watcher.stop()
        if gpu:
            gpu.stop()
        nvidia_snapshot(evidence / "system" / "nvidia_smi_after.txt")
    native_run = watcher.native_run if watcher else _detect_new_native_run(native_run_root, initial_native_runs)
    if native_run:
        metadata["native_run"], metadata["native_run_detected"] = str(native_run), True
        (evidence / "native_run" / "SOURCE_PATH.txt").write_text(str(native_run) + "\n", encoding="utf-8")
        copied, errors, skipped_sensitive = copy_tree(native_run, evidence / "native_run", skip_checkpoint_files=True)
        metadata["native_run_file_count"] = copied
        metadata["native_run_sensitive_skipped"] = skipped_sensitive
        metadata["collection_errors"].extend({"source": "native_run", **error} for error in errors)
    else:
        metadata["native_run_detected"] = False if args.run_root else None
        (evidence / "native_run" / "SOURCE_PATH.txt").write_text("NOT_FOUND\n", encoding="utf-8")
        if native_run_root:
            warning = f"native run was not detected under {native_run_root}"
            if not official_mode:
                warning += "; no checkpoints were mirrored"
            metadata["warnings"].append(warning)
            if not official_mode:
                with (evidence / "watcher.log").open("a", encoding="utf-8") as stream:
                    stream.write(f"{datetime.now(timezone.utc).isoformat()} WARNING {warning}\n")
            print(f"[issacsimz] WARNING {warning}", file=sys.stderr)
    if official_mode and operation == "train":
        metadata["organizer_keeper"] = keeper_result
        if native_run:
            kept = keeper_root / native_run.name
            copied, errors, skipped_sensitive = copy_tree(kept, evidence / "organizer_checkpoints")
            metadata["organizer_checkpoint_count"] = len(list((evidence / "organizer_checkpoints").glob("model_*.pt")))
            metadata["organizer_checkpoint_copy_count"] = copied
            metadata["collection_errors"].extend({"source": "organizer_keeper", **error} for error in errors)
        checkpoint_records, checkpoint_errors = _checkpoint_index(
            checkpoint_state_before, native_run,
            keeper_root / native_run.name if native_run else keeper_root / "__missing_native_run__",
        )
        write_json(evidence / "checkpoint_index.json", {
            "schema_version": 1,
            "run_id": identifier,
            "mode": "official",
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "checkpoints": checkpoint_records,
            "errors": checkpoint_errors,
        })
        metadata["checkpoint_index_count"] = len(checkpoint_records)
        metadata["checkpoint_index_errors"] = checkpoint_errors
    provenance, copied_collected = [], 0
    for source in collection_sources:
        records = _collect_changed_files(source, evidence / "collected" / source.name, collection_before[str(source)])
        copied_collected += sum(record.get("status") in {"NEW", "MODIFIED"} and "copy_error" not in record for record in records)
        for record in records:
            if "copy_error" in record or record.get("status") == "ERROR":
                metadata["collection_errors"].append({"source": str(source), **record})
        provenance.append({"source": str(source), "before_file_count": len(collection_before[str(source)]), "files": records})
    write_json(evidence / "collected" / "provenance.json", {"schema_version": 1, "collections": provenance})
    if metadata["operation"] in {"play", "video"}:
        exported_records = [record for collection in provenance if Path(collection["source"]).name == "exported" for record in collection["files"]]
        prepared = metadata.get("prepared_checkpoint") or {}
        isolated = prepared.get("strategy") == "isolated_copy"
        promoted = set(prepared.get("promoted_outputs") or [])
        def fresh_hash(name: str) -> str | None:
            if isolated and name not in promoted:
                return None
            records = [record for record in exported_records if record.get("path") == name]
            if not any(record.get("status") in {"NEW", "MODIFIED"} and "copy_error" not in record for record in records):
                return None
            path = evidence / "collected" / "exported" / name
            return sha256_file(path) if path.is_file() else None
        write_json(evidence / "policy_manifest.json", {
            "schema_version": 1,
            "robot": metadata["profile"],
            "source_checkpoint": metadata["source_checkpoint"],
            "source_checkpoint_sha256": metadata["source_checkpoint_sha256"],
            "source_evidence_run_id": metadata["source_evidence_run_id"],
            "source_run_mode": metadata["source_run_mode"],
            "source_evidence_validation": metadata["source_evidence_validation"],
            "source_checkpoint_origin": metadata["source_checkpoint_origin"],
            "source_provenance_verified": metadata["source_provenance_verified"],
            "policy_pt_sha256": fresh_hash("policy.pt"),
        })
    if metadata["operation"] == "video":
        write_json(evidence / "video_manifest.json", {
            "schema_version": 1,
            "parent_run_id": metadata["parent_run_id"],
            "video_label": metadata["video_label"],
            "robot": metadata["profile"],
            "source_checkpoint": metadata["source_checkpoint"],
            "source_checkpoint_sha256": metadata["source_checkpoint_sha256"],
            "source_evidence_run_id": metadata["source_evidence_run_id"],
            "source_run_mode": metadata["source_run_mode"],
            "source_evidence_validation": metadata["source_evidence_validation"],
            "source_checkpoint_origin": metadata["source_checkpoint_origin"],
            "source_provenance_verified": metadata["source_provenance_verified"],
            "play_video_sha256": fresh_hash("play_video.mp4"),
        })
    if source_identity:
        source_identity = _compare_source_identity(source_identity, workdir, profile)
        write_json(evidence / "source" / "identity.json", source_identity)
    if metadata.get("resume_lineage"):
        iterations = []
        for checkpoint in list((evidence / "checkpoints").glob("model_*.pt")) + list((evidence / "organizer_checkpoints").glob("model_*.pt")):
            match = re.fullmatch(r"model_(\d+)\.pt", checkpoint.name)
            if match:
                iterations.append(int(match.group(1)))
        metadata["resume_lineage"]["final_iteration"] = max(iterations) if iterations else None
        metadata["resume_lineage"]["source_changed_during_run"] = bool(source_identity and source_identity.get("changed_during_run"))
    with signal_lock:
        finalize_status, backup_status = signals["finalize"], signals["backup"]
    if finalize_status == "started":
        finalize_status = "incomplete"
    training_status = "interrupted" if interrupted or code == 130 else ("completed" if code == 0 else "failed")
    metadata.update({
        "end_utc": datetime.now(timezone.utc).isoformat(), "exit_code": code, "launch_error": launch_error,
        "forced_stop": forced_stop,
        "status": training_status, "training_status": training_status,
        "official_finalize_status": finalize_status,
        "official_backup_status": backup_status,
        "checkpoint_count": len(list((evidence / "checkpoints").glob("model_*.pt"))) + len(list((evidence / "organizer_checkpoints").glob("model_*.pt"))), "collected_file_count": copied_collected,
    })
    validation = _validate_evidence(evidence, metadata, source_identity, provenance)
    metadata["evidence_validation"] = validation["overall"]
    write_json(evidence / "validation.json", validation)
    write_json(evidence / "metadata.json", metadata)
    write_manifest(evidence)
    archive: Path | None = None
    if not args.no_pack:
        try:
            archive, digest = archive_run(log_root, identifier, args.output_dir, force=getattr(args, "force_pack", False))
            print(f"[issacsimz] archive={archive}")
            print(f"[issacsimz] sha256={digest.read_text(encoding='utf-8').strip()}")
        except OSError as exc:
            metadata["warnings"].append(f"archive not created: {type(exc).__name__}: {exc}")
            write_json(evidence / "metadata.json", metadata)
            write_manifest(evidence)
            print(f"[issacsimz] WARNING archive not created: {exc}", file=sys.stderr)
    handoff, handoff_errors = copy_download_handoff(
        evidence,
        task_root=workdir,
        operation=metadata["operation"],
        archive=archive,
        parent_run_id=metadata.get("parent_run_id"),
        validation=metadata["evidence_validation"],
        video_label=metadata.get("video_label"),
    )
    if handoff:
        print(f"[issacsimz] download_handoff={handoff}")
        download_bundle = handoff.parent / f"{handoff.name}-download.tar.gz"
        if download_bundle.is_file():
            print(f"[issacsimz] download_bundle={download_bundle}")
    for error in handoff_errors:
        print(f"[issacsimz] WARNING {error}", file=sys.stderr)
    print(
        f"[issacsimz] execution={metadata['status'].upper()} exit={code} "
        f"evidence_validation={metadata['evidence_validation']}"
    )
    print(f"[issacsimz] evidence={evidence}")
    if code == 0 and getattr(args, "fail_on_validation", False) and validation["overall"] == "FAIL":
        return 3
    return code
