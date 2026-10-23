from __future__ import annotations

import re
import shutil
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

from .artifacts import sha256_file


MODEL_PATTERN = re.compile(r"model_(\d+)\.pt$")


def parse_keep(value: str) -> set[int]:
    values: set[int] = set()
    for token in value.split(","):
        token = token.strip()
        if not token:
            continue
        number = int(token)
        if number < 0:
            raise ValueError("checkpoint iteration must be zero or greater")
        values.add(number)
    if not values:
        raise ValueError("--keep requires at least one iteration")
    return values


class CheckpointWatcher:
    """Copies stable model_*.pt files without touching the source run."""

    def __init__(self, run_root: Path, destination: Path, *, start_time: float,
                 interval: float = 1.0, keep_iterations: set[int] | None = None,
                 log_path: Path | None = None, native_run: Path | None = None) -> None:
        self.run_root = run_root
        self.destination = destination
        self.start_time = start_time
        self.interval = interval
        self.keep_iterations = keep_iterations
        self.log_path = log_path
        self.native_run = native_run
        self._observed: dict[Path, tuple[int, int, int]] = {}
        self._preserved: dict[Path, tuple[int, int]] = {}
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._lock = threading.Lock()
        self._scan_lock = threading.Lock()
        self._initial_runs = self._snapshot_run_directories()
        self._complete = threading.Event()

    def _snapshot_run_directories(self) -> set[Path]:
        if not self.run_root.is_dir():
            return set()
        try:
            return {path.resolve() for path in self.run_root.iterdir() if path.is_dir()}
        except OSError:
            return set()

    @property
    def complete(self) -> bool:
        return self._complete.is_set()

    def _log(self, message: str) -> None:
        if not self.log_path:
            return
        with self._lock:
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
            with self.log_path.open("a", encoding="utf-8") as stream:
                stream.write(f"{datetime.now(timezone.utc).isoformat()} {message}\n")

    def _detect_run(self) -> Path | None:
        if self.native_run and self.native_run.is_dir():
            return self.native_run
        if not self.run_root.is_dir():
            return None
        try:
            candidates = [path for path in self.run_root.iterdir() if path.is_dir() and path.resolve() not in self._initial_runs]
        except OSError as exc:
            self._log(f"run-root scan failed: {exc}")
            return None
        if candidates:
            self.native_run = max(candidates, key=lambda path: path.stat().st_mtime)
            self._log(f"native run detected: {self.native_run}")
        return self.native_run

    def _selected(self, source: Path) -> bool:
        match = MODEL_PATTERN.fullmatch(source.name)
        return bool(match) and (self.keep_iterations is None or int(match.group(1)) in self.keep_iterations)

    def scan(self, *, final: bool = False) -> None:
        with self._scan_lock:
            self._scan_locked(final=final)

    def _scan_locked(self, *, final: bool) -> None:
        self.destination.mkdir(parents=True, exist_ok=True)
        native = self._detect_run()
        if not native:
            return
        for source in sorted(native.rglob("model_*.pt")):
            if not self._selected(source):
                continue
            try:
                stat = source.stat()
                size, modified_ns = stat.st_size, stat.st_mtime_ns
            except OSError as exc:
                self._log(f"stat failed: {source}: {exc}")
                continue
            if size <= 0:
                continue
            previous_size, previous_mtime, scans = self._observed.get(source, (-1, -1, 0))
            scans = scans + 1 if (previous_size, previous_mtime) == (size, modified_ns) else 1
            self._observed[source] = (size, modified_ns, scans)
            if not final and scans < 2:
                continue
            target = self.destination / source.name
            if self._preserved.get(source) == (size, modified_ns) and target.is_file() and target.stat().st_size == size:
                continue
            temporary = target.with_suffix(target.suffix + ".part")
            try:
                source_hash = sha256_file(source)
                shutil.copy2(source, temporary)
                if temporary.stat().st_size != size or sha256_file(temporary) != source_hash:
                    raise OSError("copy verification failed")
                temporary.replace(target)
                self._preserved[source] = (size, modified_ns)
                self._log(f"preserved {source.name} bytes={size} sha256={source_hash}")
            except OSError as exc:
                temporary.unlink(missing_ok=True)
                self._log(f"copy failed: {source}: {exc}")
        if self.keep_iterations is not None:
            preserved = {int(match.group(1)) for path in self._preserved for match in [MODEL_PATTERN.fullmatch(path.name)] if match}
            if self.keep_iterations.issubset(preserved):
                self._complete.set()
                self._log("requested checkpoints preserved; watcher complete")

    def _run(self) -> None:
        while not self._stop.wait(self.interval):
            self.scan()

    def start(self) -> None:
        self.destination.mkdir(parents=True, exist_ok=True)
        self._log("watcher started; source checkpoints are copied only")
        self._thread = threading.Thread(target=self._run, name="issacsimz-checkpoint-watcher", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=max(5.0, self.interval * 2))
        self.scan(final=True)
        self._log("watcher stopped")
