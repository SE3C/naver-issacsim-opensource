from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path


SENSITIVE_NAMES = {
    "submit_config.txt",
    ".env",
    "credentials",
    "credentials.json",
    "secrets.json",
}
SENSITIVE_SUFFIXES = {".pem", ".key", ".p12", ".pfx"}


def is_sensitive_path(path: Path) -> bool:
    """Conservative denylist for broad native/collect copies; source is allowlisted elsewhere."""
    for part in path.parts:
        lower = part.lower()
        if lower in SENSITIVE_NAMES or Path(lower).suffix in SENSITIVE_SUFFIXES:
            return True
        if any(token in lower for token in ("credential", "secret", "submit_token")):
            return True
    return False


def _pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False
    return True


class ProfileLock:
    """One training process per profile, with explicit stale-lock recovery."""

    def __init__(self, profile: str, *, lock_root: Path | None = None, force_unlock: bool = False) -> None:
        root = lock_root or (Path.home() / ".cache" / "issacsimz")
        self.path = root.expanduser().resolve() / f"{profile}.lock"
        self.profile = profile
        self.force_unlock = force_unlock
        self.acquired = False

    def _owner_pid(self) -> int | None:
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            return int(data.get("pid"))
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            return None

    def acquire(self) -> "ProfileLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.exists():
            pid = self._owner_pid()
            if pid is not None and _pid_alive(pid):
                raise ValueError(f"{self.profile} training lock is active (pid={pid}): {self.path}")
            if not self.force_unlock:
                raise ValueError(f"stale {self.profile} training lock found: {self.path}; retry with --force-unlock")
            self.path.unlink()
        payload = json.dumps({
            "schema_version": 1,
            "profile": self.profile,
            "pid": os.getpid(),
            "created_utc": datetime.now(timezone.utc).isoformat(),
        }, indent=2) + "\n"
        try:
            descriptor = os.open(self.path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError as exc:
            raise ValueError(f"{self.profile} training lock raced with another process: {self.path}") from exc
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(payload)
        self.acquired = True
        return self

    def release(self) -> None:
        if not self.acquired:
            return
        if self._owner_pid() == os.getpid():
            self.path.unlink(missing_ok=True)
        self.acquired = False

    def __enter__(self) -> "ProfileLock":
        return self.acquire()

    def __exit__(self, exc_type, exc, traceback) -> None:
        self.release()
