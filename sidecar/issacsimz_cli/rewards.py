from __future__ import annotations

import difflib
import hashlib
import json
import math
import os
import re
import stat
import tempfile
from pathlib import Path

from .profiles import PROFILES, resolve_task_root


ALLOWED_REWARDS = {
    "go2": ("track_lin_vel_xy_exp", "track_ang_vel_z_exp", "lin_vel_z_l2", "ang_vel_xy_l2", "action_rate_l2", "feet_air_time", "flat_orientation_l2", "undesired_contacts", "termination_penalty"),
    "h1": ("track_lin_vel_xy_exp", "track_ang_vel_z_exp", "feet_air_time", "termination_penalty", "flat_orientation_l2", "ang_vel_xy_l2", "joint_deviation_hip", "joint_deviation_torso", "action_rate_l2"),
}
NUMBER = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?"


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _state_root() -> Path:
    return Path(os.environ.get("ISSACSIMZ_REWARD_STATE_ROOT", Path.home() / ".issacsimz" / "reward-state")).expanduser().resolve()


def _paths(robot: str, explicit: str | None) -> tuple[Path, Path, Path]:
    root = resolve_task_root(robot, explicit)
    target = (root / PROFILES[robot].reward_file).resolve()
    if target.parent != root or not target.is_file():
        raise FileNotFoundError(f"reward target not found: {target}")
    key = hashlib.sha256(str(target).encode("utf-8")).hexdigest()[:16]
    state = _state_root() / f"{robot}-{key}"
    return target, state / "original.py", state / "metadata.json"


def _entries(text: str, key: str) -> list[re.Match[str]]:
    pattern = re.compile(rf'^(?P<indent>[ \t]*)(?P<comment>#[ \t]*)?(?P<prefix>"{re.escape(key)}"[ \t]*:[ \t]*)(?P<value>{NUMBER})(?P<suffix>[ \t]*,?.*)$', re.MULTILINE)
    return list(pattern.finditer(text))


def _read(path: Path) -> tuple[bytes, str]:
    raw = path.read_bytes()
    try:
        return raw, raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"reward file is not UTF-8: {path}") from exc


def _atomic_write(path: Path, raw: bytes, mode: int | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw); stream.flush(); os.fsync(stream.fileno())
        if mode is not None:
            os.chmod(temporary, stat.S_IMODE(mode))
        os.replace(temporary, path)
    except BaseException:
        try: os.unlink(temporary)
        except FileNotFoundError: pass
        raise


def _load_metadata(path: Path) -> dict | None:
    if not path.is_file(): return None
    try: data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc: raise ValueError(f"invalid reward state metadata: {path}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"invalid reward state metadata: expected JSON object: {path}")
    return data


def _write_metadata(path: Path, data: dict) -> None:
    _atomic_write(path, (json.dumps(data, indent=2, sort_keys=True) + "\n").encode("utf-8"))


def _verified_baseline(original: Path, metadata: dict, action: str) -> bytes:
    baseline = original.read_bytes()
    if metadata.get("original_sha256") != _sha(baseline):
        raise ValueError(f"stored reward baseline failed SHA-256 verification; refusing {action}")
    return baseline


def _ensure_managed(target: Path, original: Path, metadata_path: Path, robot: str, raw: bytes) -> dict:
    metadata = _load_metadata(metadata_path)
    if metadata is None:
        original.parent.mkdir(parents=True, exist_ok=True)
        _atomic_write(original, raw)
        metadata = {"robot": robot, "target": str(target), "original_sha256": _sha(raw), "managed_sha256": _sha(raw)}
        _write_metadata(metadata_path, metadata)
    elif metadata.get("target") != str(target) or not original.is_file():
        raise ValueError("reward state does not match its target; no files modified")
    elif metadata.get("robot") != robot:
        raise ValueError("reward state robot mismatch; no files modified")
    else:
        _verified_baseline(original, metadata, "modification")
        if metadata.get("managed_sha256") != _sha(raw):
            raise ValueError("reward file changed outside issacsimz after the last managed edit; refusing modification")
    return metadata


def _validate_value(value: str) -> str:
    if value == "off": raise ValueError("reward set cannot disable rewards; use a finite numeric weight")
    try: number = float(value)
    except ValueError as exc: raise ValueError("reward value must be a finite number") from exc
    if not math.isfinite(number): raise ValueError("reward value must be finite (nan/inf are rejected)")
    return value


def _target(args) -> tuple[Path, Path, Path, str, bytes, str]:
    target, original, metadata = _paths(args.robot, args.task_root)
    raw, text = _read(target)
    return target, original, metadata, args.robot, raw, text


def _set(args) -> int:
    if args.key not in ALLOWED_REWARDS[args.robot]:
        raise ValueError(f"'{args.key}' is not an allowed {args.robot.upper()} reward")
    value = _validate_value(args.value)
    target, original, metadata_path, robot, raw, text = _target(args)
    matches = _entries(text, args.key)
    if len(matches) != 1: raise ValueError(f"reward key '{args.key}' appears {len(matches)} times; no files modified")
    match = matches[0]; active = match.group("comment") is None
    if not active:
        raise ValueError(f"reward key '{args.key}' is disabled; reward set cannot activate it; no files modified")
    old = match.group("value")
    replacement = f'{match.group("indent")}{match.group("prefix")}{value}{match.group("suffix")}'
    new_status = "active"
    new_text = text[:match.start()] + replacement + text[match.end():]
    compile(new_text, str(target), "exec")  # syntax only; never imports or executes the reward module.
    verify = _entries(new_text, args.key)
    if len(verify) != 1 or (verify[0].group("comment") is None) != (new_status == "active"):
        raise ValueError("reward edit verification failed; no files modified")
    state = _ensure_managed(target, original, metadata_path, robot, raw)
    new_raw = new_text.encode("utf-8")
    _atomic_write(target, new_raw, target.stat().st_mode)
    state["managed_sha256"] = _sha(new_raw); _write_metadata(metadata_path, state)
    print(f"[issacsimz] reward target: {target}\n[issacsimz] change: {args.key}: {old} -> {value}\n[issacsimz] status: {new_status}\n[issacsimz] PASS")
    return 0


def _show(args) -> int:
    target, _, _, robot, _, text = _target(args)
    print(f"{robot.upper()} reward overrides\n{'-' * 56}")
    for key in ALLOWED_REWARDS[robot]:
        matches = _entries(text, key)
        if len(matches) == 1:
            entry = matches[0]; status = "active" if entry.group("comment") is None else "disabled"
            print(f"{key:<28} {entry.group('value'):<10} {status}")
        elif not matches:
            print(f"{key:<28} {'-':<10} not present")
        else: print(f"{key:<28} {'-':<10} ambiguous ({len(matches)})")
    print(f"[issacsimz] reward target: {target}")
    return 0


def _diff(args) -> int:
    target, original, metadata, _, raw, text = _target(args)
    state = _load_metadata(metadata)
    if not original.is_file() or state is None:
        raise ValueError("no managed reward baseline exists; run reward set first")
    original_text = _verified_baseline(original, state, "diff").decode("utf-8")
    lines = list(difflib.unified_diff(original_text.splitlines(True), text.splitlines(True), fromfile="original", tofile="current"))
    print("".join(lines) if lines else "[issacsimz] no managed reward changes")
    print(f"[issacsimz] reward target: {target}")
    return 0


def _restore(args) -> int:
    target, original, metadata_path, _, raw, _ = _target(args)
    metadata = _load_metadata(metadata_path)
    if metadata is None or not original.is_file(): raise ValueError("no managed reward baseline exists; nothing restored")
    if metadata.get("managed_sha256") != _sha(raw):
        raise ValueError("reward file changed outside issacsimz after the last managed edit; refusing automatic restore")
    baseline = _verified_baseline(original, metadata, "automatic restore")
    _atomic_write(target, baseline, target.stat().st_mode)
    metadata["managed_sha256"] = _sha(baseline); _write_metadata(metadata_path, metadata)
    print(f"[issacsimz] restoring {args.robot.upper()} reward file\n[issacsimz] current sha256 : {_sha(raw)}\n[issacsimz] original sha256: {_sha(baseline)}\n[issacsimz] restore PASS")
    return 0


def reward_command(args) -> int:
    return {"show": _show, "set": _set, "diff": _diff, "restore": _restore}[args.reward_action](args)
