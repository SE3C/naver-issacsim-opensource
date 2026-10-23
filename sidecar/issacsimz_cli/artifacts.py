from __future__ import annotations

import hashlib
import json
import os
import shutil
import tarfile
from pathlib import Path
from typing import Any

from .safety import is_sensitive_path

VIDEO_LABELS = (
    "stairs",
    "inverted_stairs",
    "boxes",
    "random_rough",
    "slope_up_20deg",
    "slope_down_20deg",
    "slope_up_10deg",
    "slope_down_10deg",
)

PROFILE_SLOPE_LABELS = {
    "go2": ("slope_up_20deg", "slope_down_20deg"),
    "h1": ("slope_up_10deg", "slope_down_10deg"),
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, value: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def make_evidence_dir(log_root: Path, run_id: str, *, checkpoint_mirror: bool = True) -> Path:
    evidence = log_root / "runs" / run_id
    evidence.mkdir(parents=True, exist_ok=False)
    directories = ["system", "native_run", "collected"]
    if checkpoint_mirror:
        directories.append("checkpoints")
    for name in directories:
        (evidence / name).mkdir()
    files = ["command.txt", "console.log"]
    if checkpoint_mirror:
        files.append("watcher.log")
    for name in files:
        (evidence / name).touch()
    return evidence


def copy_tree(source: Path, destination: Path, *, skip_checkpoint_files: bool = False) -> tuple[int, list[dict[str, str]], list[str]]:
    if not source.is_dir():
        return 0, [{"path": str(source), "error": "source directory does not exist"}], []
    copied = 0
    errors: list[dict[str, str]] = []
    skipped: list[str] = []
    for item in source.rglob("*"):
        if not item.is_file():
            continue
        if skip_checkpoint_files and item.match("model_*.pt"):
            continue
        relative = item.relative_to(source)
        if is_sensitive_path(relative):
            skipped.append(relative.as_posix())
            continue
        try:
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)
            copied += 1
        except OSError as exc:
            errors.append({"path": str(item), "error": f"{type(exc).__name__}: {exc}"})
    return copied, errors, skipped


def write_manifest(evidence: Path) -> None:
    manifest = evidence / "SHA256SUMS"
    lines: list[str] = []
    for path in sorted(p for p in evidence.rglob("*") if p.is_file() and p != manifest):
        lines.append(f"{sha256_file(path)}  {path.relative_to(evidence).as_posix()}")
    manifest.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def download_handoff_root(task_root: Path) -> Path:
    """Resolve the small local-only handoff root without changing evidence paths."""
    override = os.environ.get("ISSACSIMZ_DOWNLOAD_ROOT")
    if override:
        return Path(override).expanduser()
    mode = os.environ.get("ISSACSIMZ_MODE", "").strip().lower()
    if mode not in {"personal", "official"}:
        mode = "official" if str(task_root).startswith("/workspace/") else "personal"
    return Path("/workspace/ISSACSIMZ_DOWNLOAD" if mode == "official" else "/home/shadeform/ISSACSIMZ_DOWNLOAD")


def _pack_download_handoff(destination: Path) -> tuple[Path, Path]:
    """Wrap the existing handoff directory without removing or changing it."""
    bundle = destination.parent / f"{destination.name}-download.tar.gz"
    sidecar = bundle.with_suffix(bundle.suffix + ".sha256")
    temporary_bundle = destination.parent / f".{bundle.name}.tmp"
    temporary_sidecar = destination.parent / f".{sidecar.name}.tmp"
    temporary_bundle.unlink(missing_ok=True)
    temporary_sidecar.unlink(missing_ok=True)
    bundle_replaced = False
    try:
        with tarfile.open(temporary_bundle, "w:gz", format=tarfile.PAX_FORMAT) as archive:
            archive.add(destination, arcname=destination.name, recursive=True)
        temporary_sidecar.write_text(
            f"{sha256_file(temporary_bundle)}  {bundle.name}\n",
            encoding="utf-8",
        )
        temporary_bundle.replace(bundle)
        bundle_replaced = True
        temporary_sidecar.replace(sidecar)
    except (OSError, tarfile.TarError):
        if bundle_replaced:
            sidecar.unlink(missing_ok=True)
        raise
    finally:
        temporary_bundle.unlink(missing_ok=True)
        temporary_sidecar.unlink(missing_ok=True)
    return bundle, sidecar


def copy_download_handoff(
    evidence: Path,
    *,
    task_root: Path,
    operation: str,
    archive: Path | None = None,
    parent_run_id: str | None = None,
    validation: str | None = None,
    video_label: str | None = None,
) -> tuple[Path | None, list[str]]:
    """Copy only final download artifacts; evidence and official exports stay untouched."""
    if operation not in {"train", "video"}:
        return None, []
    if operation == "video" and (validation != "PASS" or not parent_run_id):
        return None, []
    if video_label is not None and video_label not in VIDEO_LABELS:
        return None, [f"unsupported video label: {video_label}"]
    run_name = parent_run_id if operation == "video" else evidence.name
    errors: list[str] = []
    try:
        destination = download_handoff_root(task_root) / run_name
        destination.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        return None, [f"download handoff unavailable: {type(exc).__name__}: {exc}"]

    sources: list[tuple[Path, Path]] = []
    if operation == "train":
        if archive and archive.is_file():
            sources.append((archive, destination / archive.name))
            for suffix in (".sha256", ".metadata.json"):
                sidecar = archive.with_suffix(archive.suffix + suffix)
                if sidecar.is_file():
                    sources.append((sidecar, destination / sidecar.name))
        if validation != "FAIL":
            exported = evidence / "collected" / "exported"
            for name in ("model_best.pt", "env.yaml", "report.html"):
                source = exported / name
                if source.is_file():
                    sources.append((source, destination / name))
    else:
        source = evidence / "collected" / "exported" / "play_video.mp4"
        if source.is_file():
            target = destination / "videos" / f"{video_label}.mp4" if video_label else destination / source.name
            sources.append((source, target))

    for source, target in sources:
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        except OSError as exc:
            errors.append(f"{source.name}: {type(exc).__name__}: {exc}")
    try:
        latest = destination.parent / "LATEST.txt"
        temporary = latest.with_suffix(".txt.tmp")
        temporary.write_text(f"{run_name}\n", encoding="utf-8")
        temporary.replace(latest)
    except OSError as exc:
        errors.append(f"LATEST.txt: {type(exc).__name__}: {exc}")
    try:
        _pack_download_handoff(destination)
    except (OSError, tarfile.TarError) as exc:
        errors.append(f"download bundle: {type(exc).__name__}: {exc}")
    return destination, errors
