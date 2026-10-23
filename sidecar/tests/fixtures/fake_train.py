from __future__ import annotations

import os
import signal
import sys
import time
from pathlib import Path


scenario = os.environ.get("ISSACSIMZ_FIXTURE_SCENARIO", "success")
task = "Humanoid-v0"
if "--task" in sys.argv:
    task = sys.argv[sys.argv.index("--task") + 1]
robot = "humanoid" if "Humanoid" in task else "quadruped"
run = Path.cwd() / "logs" / "rsl_rl" / robot / f"fixture-{time.time_ns()}"
exported = Path.cwd() / "exported"
run.mkdir(parents=True)
exported.mkdir(parents=True, exist_ok=True)


def checkpoint(name: str, data: bytes) -> None:
    (run / name).write_bytes(data)


checkpoint("model_100.pt", b"checkpoint-100")
(run / "events.out.tfevents.fixture").write_text("tensorboard", encoding="utf-8")
print("[fixture] training", flush=True)


if scenario == "exit1":
    raise SystemExit(1)


def interrupted(_signum, _frame) -> None:
    print("[POST] 학습 종료 (exit=130)", flush=True)
    time.sleep(30 if scenario == "wait_for_force" else 0.2)
    (exported / "model_best.pt").write_bytes(b"best-interrupted")
    (exported / "env.yaml").write_text("fixture: interrupted", encoding="utf-8")
    print("[backup] 백업 서버 설정 없음 — 자동 백업 skip", flush=True)
    print("[DONE] 예선 제출 결과물 → exported/", flush=True)
    raise SystemExit(130)


signal.signal(signal.SIGINT, interrupted)
if scenario in {"wait_for_interrupt", "wait_for_force"}:
    while True:
        time.sleep(0.1)

checkpoint("model_200.pt", b"checkpoint-200")
print("[POST] 학습 종료 (exit=0)", flush=True)

if scenario == "cleanup_race":
    # The normal poller is deliberately slower than this delay in the test;
    # only the synchronous [POST] final scan can preserve these files.
    time.sleep(0.2)
    for path in run.glob("model_*.pt"):
        path.unlink()

if scenario == "finalize_incomplete":
    raise SystemExit(1)

if scenario not in {"missing_artifacts", "stale_exports"}:
    (exported / "model_best.pt").write_bytes(b"best-current")
    (exported / "env.yaml").write_text("fixture: current", encoding="utf-8")

if scenario == "source_change":
    reward = Path.cwd() / ("humanoid_rewards.py" if robot == "humanoid" else "quadruped_rewards.py")
    reward.write_text(reward.read_text(encoding="utf-8") + "\n# changed\n", encoding="utf-8")

if scenario == "backup_failed":
    print("[backup] ❌ 백업 실패 (HTTP 500)", flush=True)
elif scenario == "missing_artifacts":
    print("[backup] model_best.pt/env.yaml 없음 — 자동 백업 skip", flush=True)
elif scenario == "disabled":
    print("[backup] NO_AUTO_SUBMIT 설정됨 — 자동 백업 건너뜀", flush=True)
elif scenario == "no_config":
    print("[backup] 백업 서버 설정 없음 — 자동 백업 skip", flush=True)
else:
    print("[backup] ✅ 백업 완료", flush=True)

print("[DONE] 예선 제출 결과물 → exported/", flush=True)
