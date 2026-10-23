from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
import threading
from datetime import datetime, timezone
from pathlib import Path


def capture(command: list[str]) -> str:
    try:
        return subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=20, check=False).stdout
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"unavailable: {exc}\n"


def runtime_report(path: Path) -> None:
    lines = [
        f"utc={datetime.now(timezone.utc).isoformat()}",
        f"platform={platform.platform()}",
        f"python={sys.version.replace(os.linesep, ' ')}",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def nvidia_snapshot(path: Path) -> None:
    path.write_text(capture(["nvidia-smi"]), encoding="utf-8")


class GpuMonitor:
    def __init__(self, output: Path, interval: float = 2.0) -> None:
        self.output = output
        self.interval = interval
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        self.output.parent.mkdir(parents=True, exist_ok=True)
        self.output.write_text("timestamp, utilization.gpu [%], memory.used [MiB], power.draw [W], temperature.gpu\n", encoding="utf-8")
        if shutil.which("nvidia-smi"):
            self._thread = threading.Thread(target=self._run, name="issacsimz-gpu-monitor", daemon=True)
            self._thread.start()

    def _run(self) -> None:
        query = "timestamp,utilization.gpu,memory.used,power.draw,temperature.gpu"
        while not self._stop.is_set():
            with self.output.open("a", encoding="utf-8") as stream:
                stream.write(capture(["nvidia-smi", f"--query-gpu={query}", "--format=csv,noheader"]))
            self._stop.wait(self.interval)

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=max(5.0, self.interval * 2))
