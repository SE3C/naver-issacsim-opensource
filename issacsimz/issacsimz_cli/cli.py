from __future__ import annotations

import argparse
import copy
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

from .checkpoints import CheckpointWatcher, parse_keep
from .core import archive_run, default_log_root, list_evidence_runs, run_command, verify_archive
from .artifacts import PROFILE_SLOPE_LABELS, VIDEO_LABELS, sha256_file
from .profiles import PROFILES, resolve_isaaclab_launcher, resolve_task_root
from .rewards import reward_command
from .safety import ProfileLock


def _positive(value: str) -> float:
    number = float(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return number


def _positive_int(value: str) -> int:
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return number


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="issacsimz", description="External evidence recorder for Isaac Sim commands")
    sub = parser.add_subparsers(dest="action", required=True)
    doctor = sub.add_parser("doctor", help="check local runtime and evidence directory")
    doctor.add_argument("--log-root")
    doctor.add_argument("--robot", choices=PROFILES, help="also check an H1 or Go2 task profile")
    doctor.add_argument("--task-root")
    doctor.add_argument("--isaaclab-root")
    doctor.add_argument("--allow-no-auto-submit", action="store_true")
    doctor.add_argument("--allow-submit-debug", action="store_true")
    doctor.add_argument("--json", action="store_true")
    run = sub.add_parser("run", help="run a command and preserve evidence")
    run.add_argument("--name", required=True)
    run.add_argument("--workdir")
    run.add_argument("--log-root")
    run.add_argument("--run-root", help="parent directory where a native run appears")
    run.add_argument("--collect", action="append", default=[], help="directory to copy after the command; repeatable")
    run.add_argument("--output-dir")
    run.add_argument("--poll-seconds", type=_positive, default=1.0)
    run.add_argument("--gpu-interval", type=_positive, default=2.0)
    run.add_argument("--no-pack", action="store_true")
    run.add_argument("command", nargs=argparse.REMAINDER)
    train = sub.add_parser("train", help="run the standard H1 or Go2 Isaac Lab train.py with evidence")
    train.add_argument("robot", choices=PROFILES)
    train.add_argument("--name", required=True)
    train.add_argument("--iters", type=int, required=True)
    train.add_argument("--task-root", help="explicit training/humanoid or training/quadruped directory")
    train.add_argument("--isaaclab-root", help="directory containing isaaclab.sh")
    train.add_argument("--num-envs", type=int)
    train.add_argument("--seed", type=int)
    train.add_argument("--resume", action="store_true")
    train.add_argument("--load-run", help="native run name passed to train.py with --resume")
    train.add_argument("--checkpoint", help="resume checkpoint; official uses indexed source path and forwards its basename")
    train.add_argument("--import-checkpoint", help="official single-file native checkpoint resume; parent provenance remains unverified")
    train.add_argument("--from-run",
                       help="source train evidence run; required for indexed official resume")
    train.add_argument("--preflight-only", action="store_true", help="validate train inputs without starting training")
    train.add_argument("--allow-no-auto-submit", action="store_true", help="allow an intentional NO_AUTO_SUBMIT environment")
    train.add_argument("--allow-submit-debug", action="store_true", help="allow intentional SUBMIT_DEBUG on a private run")
    train.add_argument("--lock-root", help="override profile lock directory")
    train.add_argument("--force-unlock", action="store_true", help="remove a stale profile lock; never overrides a live PID")
    train.add_argument("--headless", action=argparse.BooleanOptionalAction, default=True)
    train.add_argument("--collect", action="append", default=[], help="additional directory to collect after training; repeatable")
    train.add_argument("--log-root")
    train.add_argument("--output-dir")
    train.add_argument("--poll-seconds", type=_positive, default=1.0)
    train.add_argument("--gpu-interval", type=_positive, default=2.0)
    train.add_argument("--no-pack", action="store_true")
    train.add_argument("--tmux", action="store_true", help="launch this training run in a detached tmux session")
    train.add_argument("--tmux-session", help="override tmux session name")
    train.add_argument("--extra", nargs=argparse.REMAINDER, default=[])
    watch = sub.add_parser("watch", help="mirror checkpoints from an existing native run")
    watch.add_argument("--run-dir", required=True)
    watch.add_argument("--destination", required=True)
    select = watch.add_mutually_exclusive_group(required=True)
    select.add_argument("--all", action="store_true")
    select.add_argument("--keep", help="comma-separated model iterations")
    watch.add_argument("--poll-seconds", type=_positive, default=1.0)
    pack = sub.add_parser("pack", help="archive an existing evidence run")
    pack.add_argument("run_id")
    pack.add_argument("--log-root")
    pack.add_argument("--output-dir")
    pack.add_argument("--force", action="store_true", help="replace an existing archive and sidecars")
    verify = sub.add_parser("verify", help="verify archive SHA-256 and internal SHA256SUMS without extracting")
    verify.add_argument("archive")
    verify.add_argument("--require-sidecar", action="store_true")
    verify.add_argument("--publishable", action="store_true", help="require completed, PASS-validated evidence")
    runs = sub.add_parser("runs", help="list or show evidence runs")
    runs_sub = runs.add_subparsers(dest="runs_action", required=True)
    runs_list = runs_sub.add_parser("list", help="list evidence runs")
    runs_list.add_argument("--log-root")
    runs_show = runs_sub.add_parser("show", help="show metadata and validation for one evidence run")
    runs_show.add_argument("run_id")
    runs_show.add_argument("--log-root")
    play = sub.add_parser("play", help="run an existing profile play.py externally with evidence")
    play.add_argument("robot", choices=PROFILES)
    play.add_argument("--name", required=True)
    play.add_argument("--checkpoint")
    play.add_argument("--from-run",
                      help="source train evidence run; required for official play")
    play.add_argument("--video-label", choices=VIDEO_LABELS,
                      help="treat this play as a labeled video run for download handoff")
    play.add_argument("--handoff-run-id",
                      help="download-handoff parent ID; required with --video-label")
    play.add_argument("--task-root")
    play.add_argument("--isaaclab-root")
    play.add_argument("--num-envs", type=int)
    play.add_argument("--headless", action=argparse.BooleanOptionalAction, default=True)
    play.add_argument("--collect", action="append", default=[])
    play.add_argument("--log-root")
    play.add_argument("--output-dir")
    play.add_argument("--poll-seconds", type=_positive, default=1.0)
    play.add_argument("--gpu-interval", type=_positive, default=2.0)
    play.add_argument("--no-pack", action="store_true")
    play.add_argument("--extra", nargs=argparse.REMAINDER, default=[])
    video = sub.add_parser("video", help="render video from model_best.pt preserved by an issacsimz train run")
    video.add_argument("robot", choices=PROFILES)
    video.add_argument("--from-run", required=True)
    video.add_argument("--name")
    video.add_argument("--label", choices=VIDEO_LABELS,
                       help="optional terrain label used only for evidence metadata and handoff naming")
    video.add_argument("--task-root")
    video.add_argument("--isaaclab-root")
    video.add_argument("--num-envs", type=int, default=1)
    video.add_argument("--video-length", type=_positive_int, default=1000,
                       help="recording length in 50 Hz frames (default: 1000 = 20 seconds)")
    video.add_argument("--headless", action=argparse.BooleanOptionalAction, default=True)
    video.add_argument("--collect", action="append", default=[])
    video.add_argument("--log-root")
    video.add_argument("--output-dir")
    video.add_argument("--poll-seconds", type=_positive, default=1.0)
    video.add_argument("--gpu-interval", type=_positive, default=2.0)
    video.add_argument("--no-pack", action="store_true")
    video.add_argument("--extra", nargs=argparse.REMAINDER, default=[])
    reward = sub.add_parser("reward", help="inspect or edit participant reward overrides without importing them")
    reward_sub = reward.add_subparsers(dest="reward_action", required=True)
    for action in ("show", "diff", "restore"):
        command = reward_sub.add_parser(action)
        command.add_argument("robot", choices=PROFILES)
        command.add_argument("--task-root")
    set_reward = reward_sub.add_parser("set")
    set_reward.add_argument("robot", choices=PROFILES); set_reward.add_argument("key"); set_reward.add_argument("value"); set_reward.add_argument("--task-root")
    return parser


def _environment_present(name: str) -> bool:
    """Match the native finalizer: even NAME=0 is enabled when the key exists."""
    return name in os.environ


def doctor(log_root: Path, as_json: bool, robot: str | None = None, task_root: str | None = None,
           isaaclab_root: str | None = None, allow_no_auto_submit: bool = False,
           allow_submit_debug: bool = False) -> int:
    try:
        log_root.mkdir(parents=True, exist_ok=True)
        writable = os.access(log_root, os.W_OK)
        free = shutil.disk_usage(log_root).free
    except OSError:
        writable, free = False, 0
    report = {
        "ok": writable,
        "python": sys.version.split()[0],
        "gpu_tool": shutil.which("nvidia-smi"),
        "log_root": str(log_root),
        "log_root_writable": writable,
        "free_bytes": free,
        "submit_config_present": Path("/workspace/submit_config.txt").is_file(),
        "no_auto_submit_present": _environment_present("NO_AUTO_SUBMIT"),
        "submit_debug_present": _environment_present("SUBMIT_DEBUG"),
        "submit_host_present": _environment_present("SUBMIT_HOST"),
        "submit_token_present": _environment_present("SUBMIT_TOKEN"),
    }
    if robot:
        try:
            resolved_task = resolve_task_root(robot, task_root)
            launcher = resolve_isaaclab_launcher(isaaclab_root)
            report.update({
                "profile": robot,
                "task_root": str(resolved_task),
                "task_train_py": (resolved_task / "train.py").is_file(),
                "native_run_root": str(resolved_task / PROFILES[robot].native_run_root),
                "isaaclab_launcher": str(launcher),
            })
        except FileNotFoundError as exc:
            report.update({"profile": robot, "profile_error": str(exc)})
            report["ok"] = False
        if report["no_auto_submit_present"] and not allow_no_auto_submit:
            report["profile_environment_error"] = "NO_AUTO_SUBMIT is present"
            report["ok"] = False
        if report["submit_debug_present"] and not allow_submit_debug:
            report["profile_environment_error"] = "SUBMIT_DEBUG is present"
            report["ok"] = False
    if as_json:
        print(json.dumps(report, indent=2))
    else:
        print("issacsimz doctor:", "PASS" if report["ok"] else "FAIL")
        for key, value in report.items():
            if key != "ok":
                print(f"  {key}={value}")
    return 0 if report["ok"] else 1


def watch(args) -> int:
    _require_mode("watch", {"personal"})
    run_dir = Path(args.run_dir).expanduser().resolve()
    if not run_dir.is_dir():
        raise FileNotFoundError(run_dir)
    destination = Path(args.destination).expanduser().resolve()
    keep = None if args.all else parse_keep(args.keep)
    watcher = CheckpointWatcher(run_dir.parent, destination, start_time=time.time(), interval=args.poll_seconds, keep_iterations=keep, log_path=destination / "watcher.log", native_run=run_dir)
    watcher.start()
    print(f"[issacsimz] watching {run_dir}; Ctrl+C stops copying")
    try:
        while True:
            if watcher.complete:
                print("[issacsimz] requested checkpoints preserved; watch completed")
                return 0
            time.sleep(min(1.0, args.poll_seconds))
    except KeyboardInterrupt:
        return 0
    finally:
        watcher.stop()


def _require_mode(action: str, allowed: set[str]) -> str:
    mode = os.environ.get("ISSACSIMZ_MODE", "").strip().lower()
    if not mode:
        raise ValueError(f"ISSACSIMZ_MODE is not set; use bootstrap before {action}")
    if mode not in {"personal", "official"}:
        raise ValueError(f"unsupported ISSACSIMZ_MODE for {action}: {mode}")
    if mode not in allowed:
        allowed_text = " or ".join(sorted(allowed))
        raise ValueError(f"{action} requires ISSACSIMZ_MODE={allowed_text}; current mode={mode}")
    return mode


def _require_train_mode() -> str:
    return _require_mode("train", {"personal", "official"})


def _official_mode() -> bool:
    return os.environ.get("ISSACSIMZ_MODE", "").strip().lower() == "official"


def _load_train_evidence(log_root: Path, run_id: str, robot: str,
                         *, require_official: bool) -> tuple[Path, dict, str | None]:
    runs_root = (log_root / "runs").resolve()
    train_run = (runs_root / run_id).resolve()
    if train_run.parent != runs_root or not train_run.is_dir():
        raise FileNotFoundError(f"train evidence run not found: {run_id}")
    try:
        metadata = json.loads((train_run / "metadata.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid train evidence metadata: {run_id}") from exc
    if not isinstance(metadata, dict):
        raise ValueError(f"invalid train evidence metadata: {run_id}")
    if metadata.get("operation") != "train":
        raise ValueError("--from-run must refer to a train run")
    if metadata.get("profile") != robot:
        raise ValueError(f"robot mismatch: run={metadata.get('profile')} requested={robot}")
    validation = metadata.get("evidence_validation")
    if validation is None:
        try:
            report = json.loads((train_run / "validation.json").read_text(encoding="utf-8"))
            validation = report.get("overall") if isinstance(report, dict) else None
        except (OSError, json.JSONDecodeError):
            validation = None
    if require_official:
        if not _manifest_matches(train_run, "metadata.json", train_run / "metadata.json"):
            raise ValueError("official source train metadata does not match its evidence SHA256SUMS")
        if metadata.get("mode") != "official":
            raise ValueError("official play/video requires a source train run with mode=official")
        if (metadata.get("source_checkpoint_origin") == "user_imported_checkpoint"
                and not metadata.get("source_provenance_verified")):
            raise ValueError("official source lineage is unverified after single-file import; official play/export and indexed resume require verified parent evidence")
        if validation == "FAIL":
            raise ValueError("official play/video refuses source train evidence with validation=FAIL")
    return train_run, metadata, validation


def _manifest_matches(evidence: Path, relative: str, source: Path) -> bool:
    manifest = evidence / "SHA256SUMS"
    if not manifest.is_file():
        return False
    expected = None
    for line in manifest.read_text(encoding="utf-8").splitlines():
        digest, separator, name = line.partition("  ")
        if separator and name == relative:
            expected = digest
            break
    return bool(expected and re.fullmatch(r"[0-9a-f]{64}", expected) and expected == sha256_file(source))


def _official_checkpoint_origin(checkpoint: Path, task_root: Path, train_run: Path,
                                metadata: dict) -> str:
    source = checkpoint.resolve()
    evidence_checkpoint = (train_run / "collected" / "exported" / "model_best.pt").resolve()
    if source == evidence_checkpoint:
        if not _manifest_matches(train_run, "collected/exported/model_best.pt", source):
            raise ValueError("official source checkpoint does not match its evidence SHA256SUMS")
        return "train_evidence_export"
    canonical = (task_root / "exported" / "model_best.pt").resolve()
    if source == canonical and evidence_checkpoint.is_file() and sha256_file(source) == sha256_file(evidence_checkpoint):
        if not _manifest_matches(train_run, "collected/exported/model_best.pt", evidence_checkpoint):
            raise ValueError("official source checkpoint does not match its evidence SHA256SUMS")
        return "canonical_export_alias"
    if re.fullmatch(r"model_\d+\.pt", source.name):
        index_path = train_run / "checkpoint_index.json"
        if not _manifest_matches(train_run, "checkpoint_index.json", index_path):
            raise ValueError("official numbered checkpoint requires a manifest-verified checkpoint_index.json")
        try:
            index = json.loads(index_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError("invalid official checkpoint_index.json") from exc
        entries = index.get("checkpoints") if isinstance(index, dict) else None
        if not isinstance(entries, list):
            raise ValueError("invalid official checkpoint_index.json")
        source_sha = sha256_file(source)
        source_size = source.stat().st_size
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            try:
                recorded_path = Path(entry.get("source_path", "")).expanduser().resolve()
            except (OSError, RuntimeError):
                continue
            if (recorded_path == source
                    and entry.get("sha256") == source_sha
                    and entry.get("size") == source_size
                    and entry.get("origin") in {"official_native_run", "organizer_keeper_backup"}):
                return str(entry["origin"])
        raise ValueError("official numbered checkpoint does not match the train evidence checkpoint index")
    raise ValueError(
        "official checkpoint must be the selected train evidence model_best.pt, its identical "
        "canonical export, a numbered checkpoint in that native run, or backup_log/model_<iter>.pt"
    )


def _validate_official_video_extra(extra: list[str]) -> None:
    """Allow only native recording switches; reject Hydra/viewer overrides."""
    values = list(extra)
    if values[:1] == ["--"]:
        values = values[1:]
    index = 0
    while index < len(values):
        item = values[index]
        if item in {"--video", "--enable_cameras"}:
            index += 1
            continue
        if item == "--video_length":
            if index + 1 >= len(values):
                raise ValueError("official --video_length requires a value")
            try:
                length = int(values[index + 1])
            except ValueError as exc:
                raise ValueError("official --video_length must be a positive integer") from exc
            if length < 1:
                raise ValueError("official --video_length must be a positive integer")
            index += 2
            continue
        if item.startswith("--video_length="):
            try:
                length = int(item.split("=", 1)[1])
            except ValueError as exc:
                raise ValueError("official --video_length must be a positive integer") from exc
            if length < 1:
                raise ValueError("official --video_length must be a positive integer")
            index += 1
            continue
        raise ValueError(
            f"official play/video arbitrary --extra is disabled: {item}; "
            "only --video, --video_length, and --enable_cameras are allowed"
        )


def train(args) -> int:
    mode = _require_train_mode()
    if args.iters < 1:
        raise ValueError("--iters must be greater than zero")
    if mode == "official" and args.extra:
        raise ValueError("official train --extra is disabled")
    if mode == "official" and (args.allow_no_auto_submit or args.allow_submit_debug):
        raise ValueError("private submit bypass flags are disabled in official mode")
    profile = PROFILES[args.robot]
    no_auto_submit = _environment_present("NO_AUTO_SUBMIT")
    if no_auto_submit and not args.allow_no_auto_submit:
        raise ValueError("NO_AUTO_SUBMIT is enabled; refuse to hide official backup. Use --allow-no-auto-submit only for an intentional private run.")
    submit_debug = _environment_present("SUBMIT_DEBUG")
    if submit_debug and not args.allow_submit_debug:
        raise ValueError("SUBMIT_DEBUG is present; refuse to capture verbose official backup output. Use --allow-submit-debug only for an intentional private run.")
    task_root = resolve_task_root(args.robot, args.task_root)
    launcher = resolve_isaaclab_launcher(args.isaaclab_root)
    imported_checkpoint = getattr(args, "import_checkpoint", None)
    if imported_checkpoint:
        if mode not in {"official", "personal"}:
            raise ValueError("--import-checkpoint requires official or personal mode")
        if args.from_run or args.load_run or args.checkpoint:
            raise ValueError("--import-checkpoint cannot be combined with --from-run, --load-run, or --checkpoint")
        imported_source = Path(imported_checkpoint).expanduser()
        if imported_source.is_symlink() or not imported_source.is_file() or imported_source.stat().st_size == 0:
            raise ValueError("--import-checkpoint requires a nonempty regular native checkpoint file")
        if imported_source.suffix != ".pt" or imported_source.name == "policy.pt":
            raise ValueError("--import-checkpoint requires a native .pt checkpoint, not exported policy.pt")
        imported_source = imported_source.resolve()
        imported_sha = sha256_file(imported_source)
        args.checkpoint = str(imported_source)
        args.load_run = f"issacsimz-import-{imported_sha[:16]}"
    resume_requested = bool(args.resume or args.load_run or args.checkpoint)
    source_train_run = None
    source_train_metadata = None
    source_validation = None
    checkpoint_origin = None
    native_resume_run = None
    if imported_checkpoint:
        native_resume_run = task_root / profile.native_run_root / args.load_run
        if native_resume_run.is_symlink() or (native_resume_run.exists() and not native_resume_run.is_dir()):
            raise ValueError(f"official import destination is not a regular directory: {native_resume_run}")
    elif mode == "official" and resume_requested:
        if not args.from_run:
            raise ValueError("official resume requires --from-run OFFICIAL_TRAIN_RUN")
        if not args.checkpoint:
            raise ValueError("official resume requires an explicit --checkpoint")
        source_train_run, source_train_metadata, source_validation = _load_train_evidence(
            default_log_root(args.log_root), args.from_run, args.robot, require_official=True
        )
        native_run_value = source_train_metadata.get("native_run")
        if not native_run_value:
            raise ValueError("official resume source evidence has no native run")
        native_resume_run = Path(native_run_value).resolve()
        if args.load_run and args.load_run != native_resume_run.name:
            raise ValueError(
                f"official --load-run does not match source evidence native run: "
                f"{args.load_run} != {native_resume_run.name}"
            )
        args.load_run = native_resume_run.name
        expected_run = (task_root / profile.native_run_root / args.load_run).resolve()
        if native_resume_run != expected_run or not native_resume_run.is_dir():
            raise ValueError(f"official resume native run is unavailable: {native_resume_run}")
    command = [str(launcher), "-p", str(task_root / "train.py"), "--task", profile.task, "--max_iterations", str(args.iters)]
    if args.num_envs is not None:
        if args.num_envs < 1:
            raise ValueError("--num-envs must be greater than zero")
        command += ["--num_envs", str(args.num_envs)]
    if args.seed is not None:
        command += ["--seed", str(args.seed)]
    if resume_requested:
        command.append("--resume")
    if args.load_run:
        command += ["--load_run", args.load_run]
    if args.checkpoint:
        command += ["--checkpoint", args.checkpoint]
    if args.headless:
        command.append("--headless")
    extra = list(args.extra)
    if extra[:1] == ["--"]:
        extra = extra[1:]
    if any(item.startswith("agent.save_interval=") for item in extra):
        raise ValueError("train checkpoint save interval is fixed at 50")
    command += extra
    command.append("agent.save_interval=50")
    args.command = command
    args.workdir = str(task_root)
    args.run_root = str(task_root / profile.native_run_root)
    args.collect = [str(task_root / "exported"), *args.collect]
    args.source_profile = profile
    args.profile_operation = "train"
    if resume_requested:
        requested_checkpoint = args.checkpoint
        candidates: list[Path] = []
        if requested_checkpoint:
            candidate = Path(requested_checkpoint).expanduser()
            if candidate.is_absolute():
                candidates.append(candidate)
            else:
                if args.load_run:
                    candidates.append(task_root / profile.native_run_root / args.load_run / candidate)
                candidates += [task_root / "exported" / candidate, task_root / candidate]
        source = next((path.resolve() for path in candidates if path.is_file()), None)
        if mode == "official" and source is None:
            raise FileNotFoundError(f"official resume checkpoint not found: {requested_checkpoint}")
        if imported_checkpoint:
            checkpoint_origin = "user_imported_checkpoint"
            command[command.index("--checkpoint") + 1] = re.escape(source.name)
        elif mode == "official":
            assert source_train_run is not None and source_train_metadata is not None
            checkpoint_origin = _official_checkpoint_origin(
                source, task_root, source_train_run, source_train_metadata
            )
            if checkpoint_origin not in {"official_native_run", "organizer_keeper_backup"}:
                raise ValueError("official resume requires a numbered checkpoint in the source evidence checkpoint index")
            command[command.index("--checkpoint") + 1] = source.name
        start_iteration = None
        if requested_checkpoint:
            match = re.fullmatch(r"model_(\d+)\.pt", Path(requested_checkpoint).name)
            if match:
                start_iteration = int(match.group(1))
        source_sha = imported_sha if imported_checkpoint else sha256_file(source) if source else None
        provenance_verified = bool(mode == "official" and checkpoint_origin and not imported_checkpoint)
        args.parent_run_id = None if imported_checkpoint else args.from_run or args.load_run
        args.source_checkpoint = str(source) if source else requested_checkpoint
        args.source_checkpoint_sha256 = source_sha
        args.source_evidence_run_id = args.from_run
        args.source_run_mode = "unknown" if imported_checkpoint else source_train_metadata.get("mode") if source_train_metadata else None
        args.source_evidence_validation = source_validation
        args.source_checkpoint_origin = checkpoint_origin
        args.source_provenance_verified = provenance_verified
        args.resume_lineage = {
            "official_resume": mode == "official",
            "parent_run_id": args.parent_run_id,
            "requested_checkpoint": requested_checkpoint,
            "source_checkpoint": str(source) if source else requested_checkpoint,
            "source_checkpoint_sha256": source_sha,
            "source_checkpoint_origin": checkpoint_origin,
            "source_provenance_verified": provenance_verified,
            "start_iteration": start_iteration,
            "requested_max_iterations": args.iters,
            "final_iteration": None,
            "source_identity": "source/identity.json",
        }
    args.environment_guards = {
        "no_auto_submit_enabled": no_auto_submit,
        "allow_no_auto_submit": args.allow_no_auto_submit,
        "submit_debug_present": submit_debug,
        "allow_submit_debug": args.allow_submit_debug,
    }
    native_checkpoint = None
    if imported_checkpoint or (mode == "official" and resume_requested):
        assert source is not None and native_resume_run is not None
        native_checkpoint = native_resume_run / source.name
        if native_checkpoint.is_symlink() or (native_checkpoint.exists() and not native_checkpoint.is_file()):
            raise ValueError(f"resume native checkpoint is not a regular file: {native_checkpoint}")
        if native_checkpoint.is_file() and sha256_file(native_checkpoint) != args.source_checkpoint_sha256:
            reason = "imported source" if imported_checkpoint else "indexed source"
            raise ValueError(f"resume native checkpoint differs from {reason}: {native_checkpoint}")
        args.resume_lineage["native_checkpoint_path"] = str(native_checkpoint)
        args.resume_lineage["native_checkpoint_staged"] = not native_checkpoint.is_file()
    if imported_checkpoint:
        print("[issacsimz] imported parent provenance=UNVERIFIED; this does not establish official submission lineage")
    if args.preflight_only:
        print("[issacsimz] train preflight=PASS (no training started)")
        return 0
    lock_root = Path(args.lock_root) if args.lock_root else None
    with ProfileLock(args.robot, lock_root=lock_root, force_unlock=args.force_unlock):
        if native_checkpoint is not None and not native_checkpoint.is_file():
            if imported_checkpoint:
                native_resume_run.mkdir(parents=True, exist_ok=True)
            temporary = native_checkpoint.with_name(f".{native_checkpoint.name}.issacsimz-{os.getpid()}.tmp")
            try:
                shutil.copy2(source, temporary)
                if sha256_file(temporary) != args.source_checkpoint_sha256:
                    raise ValueError("resume staged checkpoint SHA-256 mismatch")
                temporary.replace(native_checkpoint)
                strategy = "imported" if imported_checkpoint else "restored indexed"
                print(f"[issacsimz] {strategy} checkpoint for native resume: {native_checkpoint}")
            finally:
                temporary.unlink(missing_ok=True)
        return run_command(args)


def _tmux_session_name(robot: str, name: str, override: str | None) -> str:
    raw = override or f"issacsimz-{robot}-{name}"
    safe = re.sub(r"[^A-Za-z0-9_-]+", "-", raw).strip("-")
    if not safe:
        raise ValueError("invalid tmux session name")
    return safe[:100]


def _without_tmux_options(argv: list[str]) -> list[str]:
    """Remove only launcher flags so the detached child cannot recurse."""
    cleaned: list[str] = []
    index = 0
    while index < len(argv):
        item = argv[index]
        if item == "--tmux":
            index += 1
            continue
        if item == "--tmux-session":
            index += 2
            continue
        if item.startswith("--tmux-session="):
            index += 1
            continue
        cleaned.append(item)
        index += 1
    return cleaned


def launch_train_tmux(args) -> int:
    tmux = shutil.which("tmux")
    if not tmux:
        raise FileNotFoundError("tmux not found; install/enable tmux before requesting --tmux")
    if os.environ.get("TMUX"):
        print("[issacsimz] already inside tmux; running training in this session")
        args.tmux = False
        return train(args)

    session = _tmux_session_name(args.robot, args.name, args.tmux_session)
    exists = subprocess.run([tmux, "has-session", "-t", session], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if exists.returncode == 0:
        raise ValueError(f"tmux session already exists: {session}")

    pyz = Path(sys.argv[0]).expanduser().resolve()
    if not pyz.is_file():
        raise FileNotFoundError(f"cannot resolve current issacsimz.pyz: {pyz}")
    preflight_args = copy.copy(args)
    preflight_args.preflight_only = True
    if train(preflight_args) != 0:
        raise ValueError("train preflight failed; tmux session was not started")
    child_argv = _without_tmux_options(list(args._source_argv))
    command = [sys.executable, str(pyz), *child_argv]
    try:
        subprocess.run([tmux, "new-session", "-d", "-s", session, shlex.join(command)], check=True)
    except subprocess.CalledProcessError as exc:
        raise OSError(f"failed to create tmux session: {session}") from exc

    print(f"[issacsimz] tmux session={session}")
    print(f"[issacsimz] attach: tmux attach -t {session}")
    print("[issacsimz] detach: Ctrl-B then D")
    print("[issacsimz] graceful stop: attach, then press Ctrl-C once")
    return 0


def _atomic_copy(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(f".{target.name}.issacsimz-{os.getpid()}.tmp")
    temporary.unlink(missing_ok=True)
    try:
        shutil.copy2(source, temporary)
        temporary.replace(target)
    finally:
        temporary.unlink(missing_ok=True)


def _copy_isolated_play_outputs(checkpoint: Path, task_root: Path, started: float,
                                *, promote_policy: bool) -> list[str]:
    """Promote only fresh native play outputs from an isolated checkpoint copy."""
    output_root = checkpoint.parent
    exported = task_root / "exported"
    promoted: list[str] = []
    for name in (("policy.pt", "policy.onnx") if promote_policy else ()):
        candidates = [
            path for path in output_root.rglob(name)
            if path.is_file() and path.stat().st_mtime >= started - 5
        ]
        if candidates:
            _atomic_copy(max(candidates, key=lambda path: path.stat().st_mtime), exported / name)
            promoted.append(name)
    videos = [
        path for path in output_root.rglob("*.mp4")
        if path.is_file() and path.stat().st_mtime >= started - 5
    ]
    if videos:
        _atomic_copy(max(videos, key=lambda path: path.stat().st_mtime), exported / "play_video.mp4")
        promoted.append("play_video.mp4")
    return promoted


def _run_with_isolated_checkpoint(args, task_root: Path, checkpoint: Path) -> int:
    """Run play from an isolated copy without replacing canonical model_best.pt.

    The official task wrapper still requires its canonical model_best.pt to
    exist during startup. An arbitrary source is copied under the evidence
    staging root and passed through the wrapper's native --checkpoint option.
    """
    source = Path(args.stage_checkpoint_source).expanduser().resolve()
    target = checkpoint.resolve()
    if source == target:
        args.prepared_checkpoint = {
            "source": str(source), "execution": str(target), "canonical": str(target),
            "staged": False, "strategy": "canonical_direct",
        }
        return run_command(args)
    if not source.is_file():
        raise FileNotFoundError(f"play source checkpoint not found: {source}")
    if not target.is_file():
        raise FileNotFoundError(
            "official play.py requires the canonical exported/model_best.pt to exist; "
            f"refusing to create or replace it: {target}"
        )
    canonical_sha256 = sha256_file(target)
    staging_root = default_log_root(args.log_root) / "staging"
    staging_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="play-checkpoint-", dir=staging_root) as raw:
        prepared = Path(raw) / source.name
        shutil.copy2(source, prepared)
        checkpoint_index = args.command.index("--checkpoint") + 1
        args.command[checkpoint_index] = str(prepared)
        started = time.time()
        args.prepared_checkpoint = {
            "source": str(source), "execution": str(prepared), "canonical": str(target),
            "canonical_sha256": canonical_sha256, "staged": True,
            "strategy": "isolated_copy",
        }
        args.native_output_roots = {
            **getattr(args, "native_output_roots", {}),
            "isolated_checkpoint": str(prepared.parent),
        }
        def promote_outputs() -> None:
            args.prepared_checkpoint["promoted_outputs"] = _copy_isolated_play_outputs(
                prepared, task_root, started,
                promote_policy=getattr(args, "source_provenance_verified", False) or not _official_mode(),
            )
        args._post_run = promote_outputs
        result = run_command(args)
        if sha256_file(target) != canonical_sha256:
            raise OSError(f"canonical checkpoint changed during play: {target}")
        return result


def play(args) -> int:
    profile = PROFILES[args.robot]
    video_label = getattr(args, "video_label", None)
    if video_label is not None:
        slope_labels = {label for labels in PROFILE_SLOPE_LABELS.values() for label in labels}
        if video_label in slope_labels and video_label not in PROFILE_SLOPE_LABELS[args.robot]:
            raise ValueError(f"video label {video_label!r} does not match profile {args.robot!r}")
        if not getattr(args, "handoff_run_id", None) and not getattr(args, "parent_run_id", None):
            raise ValueError("--handoff-run-id is required with --video-label")
    task_root = resolve_task_root(args.robot, args.task_root)
    launcher = resolve_isaaclab_launcher(args.isaaclab_root)
    log_root = default_log_root(args.log_root)
    source_run_id = getattr(args, "from_run", None)
    train_run = None
    train_metadata = None
    source_validation = None
    if source_run_id:
        train_run, train_metadata, source_validation = _load_train_evidence(
            log_root, source_run_id, args.robot, require_official=_official_mode()
        )
    elif _official_mode():
        raise ValueError("official play requires --from-run OFFICIAL_TRAIN_RUN")
    requested_value = getattr(args, "stage_checkpoint_source", None) or getattr(args, "checkpoint", None)
    if requested_value is None and train_run is not None:
        requested_value = str(train_run / "collected" / "exported" / "model_best.pt")
    if requested_value is None:
        raise ValueError("play requires --checkpoint PATH or --from-run TRAIN_RUN")
    requested_checkpoint = Path(requested_value).expanduser().resolve()
    if not requested_checkpoint.is_file():
        raise FileNotFoundError(f"checkpoint not found: {requested_checkpoint}")
    checkpoint_origin = "explicit_path"
    provenance_verified = False
    if train_run is not None and train_metadata is not None:
        if _official_mode():
            if (re.fullmatch(r"model_\d+\.pt", requested_checkpoint.name)
                    and train_metadata.get("status") != "completed"):
                raise ValueError("official numbered checkpoint play/export requires a completed source train run")
            checkpoint_origin = _official_checkpoint_origin(
                requested_checkpoint, task_root, train_run, train_metadata
            )
            provenance_verified = True
        else:
            expected = (train_run / "collected" / "exported" / "model_best.pt").resolve()
            checkpoint_origin = "train_evidence_export" if requested_checkpoint == expected else "explicit_path_with_run"
    args.source_evidence_run_id = source_run_id
    args.source_run_mode = train_metadata.get("mode") if train_metadata else None
    args.source_evidence_validation = source_validation
    args.source_checkpoint_origin = checkpoint_origin
    args.source_provenance_verified = provenance_verified
    if source_run_id and not getattr(args, "parent_run_id", None):
        args.parent_run_id = source_run_id
    checkpoint = (task_root / "exported" / "model_best.pt").resolve()
    command = [str(launcher), "-p", str(task_root / "play.py"), "--task", profile.task, "--checkpoint", str(checkpoint)]
    if args.num_envs is not None:
        if args.num_envs < 1:
            raise ValueError("--num-envs must be greater than zero")
        command += ["--num_envs", str(args.num_envs)]
    if args.headless:
        command.append("--headless")
    extra = list(args.extra)
    if extra[:1] == ["--"]:
        extra = extra[1:]
    if _official_mode():
        _validate_official_video_extra(extra)
    args.command, args.workdir, args.run_root = command + extra, str(task_root), None
    args.collect = [str(task_root / "exported"), *args.collect]
    args.source_profile = profile
    args.profile_operation = "video" if video_label is not None else getattr(args, "profile_operation", None) or "play"
    if video_label is not None and getattr(args, "handoff_run_id", None):
        args.parent_run_id = args.handoff_run_id
        args.fail_on_validation = True
    args.source_checkpoint = getattr(args, "source_checkpoint", None) or str(requested_checkpoint)
    args.source_checkpoint_sha256 = getattr(args, "source_checkpoint_sha256", None) or sha256_file(requested_checkpoint)
    args.stage_checkpoint_source = str(requested_checkpoint)
    args.native_output_roots = {
        "exported": str(task_root / "exported"),
        "videos": str(task_root / "videos"),
    }
    args.environment_guards = {
        "source_provenance_required": _official_mode(),
        "source_provenance_verified": provenance_verified,
    }
    return _run_with_isolated_checkpoint(args, task_root, checkpoint)


def video(args) -> int:
    slope_labels = {label for labels in PROFILE_SLOPE_LABELS.values() for label in labels}
    if args.label in slope_labels and args.label not in PROFILE_SLOPE_LABELS[args.robot]:
        raise ValueError(f"video label {args.label!r} does not match profile {args.robot!r}")
    log_root = default_log_root(args.log_root)
    train_run, _, _ = _load_train_evidence(
        log_root, args.from_run, args.robot, require_official=_official_mode()
    )
    checkpoint = train_run / "collected" / "exported" / "model_best.pt"
    if not checkpoint.is_file():
        raise FileNotFoundError(f"model_best.pt not preserved by train run: {args.from_run}")
    args.name = args.name or f"{args.from_run}-video" + (f"-{args.label}" if args.label else "")
    extra = list(args.extra)
    if extra[:1] == ["--"]:
        extra = extra[1:]
    if "--video" not in extra:
        extra.append("--video")
    if not any(item == "--video_length" or item.startswith("--video_length=") for item in extra):
        extra += ["--video_length", str(args.video_length)]
    if "--enable_cameras" not in extra:
        extra.append("--enable_cameras")
    args.extra = extra
    task_root = resolve_task_root(args.robot, args.task_root)
    args.stage_checkpoint_source = str(checkpoint)
    args.checkpoint = str(task_root / "exported" / "model_best.pt")
    args.parent_run_id = args.from_run
    args.video_label = args.label
    args.source_checkpoint = str(checkpoint)
    args.source_checkpoint_sha256 = sha256_file(checkpoint)
    args.profile_operation = "video"
    args.fail_on_validation = True
    return play(args)


def main(argv: list[str] | None = None) -> int:
    source_argv = list(argv if argv is not None else sys.argv[1:])
    args = build_parser().parse_args(source_argv)
    args._source_argv = source_argv
    try:
        if _official_mode() and args.action in {"train", "play", "video"} and getattr(args, "collect", []):
            raise ValueError("user-supplied --collect is disabled in official mode")
        if args.action == "doctor":
            if _official_mode() and (args.allow_no_auto_submit or args.allow_submit_debug):
                raise ValueError("private submit bypass flags are disabled in official mode")
            return doctor(default_log_root(args.log_root), args.json, args.robot, args.task_root, args.isaaclab_root,
                          args.allow_no_auto_submit, args.allow_submit_debug)
        if args.action == "watch":
            return watch(args)
        if args.action == "pack":
            archive, digest = archive_run(default_log_root(args.log_root), args.run_id, args.output_dir, force=args.force)
            print(archive)
            print(digest)
            return 0
        if args.action == "verify":
            report = verify_archive(Path(args.archive), require_sidecar=args.require_sidecar)
            if args.publishable:
                metadata = report.get("metadata") or {}
                if metadata.get("status") != "completed" or metadata.get("evidence_validation") != "PASS":
                    report["errors"].append("publishing requires completed evidence with validation PASS")
                    report["ok"] = False
            print(json.dumps(report, indent=2))
            return 0 if report["ok"] else 1
        if args.action == "runs":
            log_root = default_log_root(args.log_root)
            if args.runs_action == "list":
                print(json.dumps(list_evidence_runs(log_root), indent=2))
                return 0
            source = (log_root / "runs" / args.run_id).resolve()
            if source.parent != (log_root / "runs").resolve() or not source.is_dir():
                raise FileNotFoundError(f"evidence run not found: {args.run_id}")
            print((source / "metadata.json").read_text(encoding="utf-8"))
            validation = source / "validation.json"
            if validation.is_file():
                print(validation.read_text(encoding="utf-8"))
            return 0
        if args.action == "train":
            _require_train_mode()
            if args.preflight_only:
                return train(args)
            if args.tmux:
                return launch_train_tmux(args)
            return train(args)
        if args.action == "reward":
            return reward_command(args)
        if args.action == "play":
            _require_mode("play", {"personal", "official"})
            return play(args)
        if args.action == "video":
            _require_mode("video", {"personal", "official"})
            return video(args)
        if args.action == "run":
            _require_mode("run", {"personal"})
        return run_command(args)
    except (FileNotFoundError, ValueError, OSError) as exc:
        print(f"[issacsimz] error: {exc}", file=sys.stderr)
        return 2
