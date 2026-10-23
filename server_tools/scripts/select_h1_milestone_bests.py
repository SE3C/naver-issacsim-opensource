#!/usr/bin/env python3
"""Select H1 boundary and reward-best checkpoints for fixed milestones.

The criterion deliberately matches the training finalizer: maximum
``Train/mean_reward``.  A TensorBoard scalar can be logged at every iteration
while checkpoints are stored less often, so each scalar peak is mapped to the
latest available ``model_<iteration>.pt`` at or before that peak.

The boundary checkpoint is kept separately: it is the latest numbered
checkpoint at or before the milestone. For a zero-based 5,000-iteration run,
that final boundary may correctly be ``model_4999.pt``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
from pathlib import Path

from tensorboard.backend.event_processing.event_accumulator import EventAccumulator


CHECKPOINT_RE = re.compile(r"model_(\d+)\.pt$")
REWARD_TAG = "Train/mean_reward"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--milestones", nargs="+", type=int, default=[1000, 2500, 5000])
    return parser.parse_args()


def checkpoint_map(run_dir: Path) -> dict[int, Path]:
    checkpoints: dict[int, Path] = {}
    for path in run_dir.glob("model_*.pt"):
        match = CHECKPOINT_RE.fullmatch(path.name)
        if match and path.is_file() and path.stat().st_size > 0:
            checkpoints[int(match.group(1))] = path
    if not checkpoints:
        raise RuntimeError(f"No non-empty model_<iteration>.pt checkpoints in {run_dir}")
    return checkpoints


def best_scalar_by_milestone(run_dir: Path, milestone: int):
    accumulator = EventAccumulator(str(run_dir), size_guidance={"scalars": 0})
    accumulator.Reload()
    tags = accumulator.Tags().get("scalars", [])
    if REWARD_TAG not in tags:
        raise RuntimeError(f"TensorBoard tag {REWARD_TAG!r} is missing; available scalar tags: {tags}")

    candidates = [
        item
        for item in accumulator.Scalars(REWARD_TAG)
        if item.step <= milestone and math.isfinite(item.value)
    ]
    if not candidates:
        raise RuntimeError(f"No finite {REWARD_TAG} scalar at or before milestone {milestone}")
    return max(candidates, key=lambda item: (item.value, item.step))


def main() -> None:
    args = parse_args()
    run_dir = args.run_dir.resolve()
    output_dir = args.output_dir.resolve()
    milestones = sorted(set(args.milestones))
    if any(milestone <= 0 for milestone in milestones):
        raise ValueError("Milestones must be positive integers")

    checkpoints = checkpoint_map(run_dir)
    checkpoint_iterations = sorted(checkpoints)
    output_dir.mkdir(parents=True, exist_ok=True)
    selections = []

    for milestone in milestones:
        peak = best_scalar_by_milestone(run_dir, milestone)
        best_eligible = [iteration for iteration in checkpoint_iterations if iteration <= peak.step]
        boundary_eligible = [
            iteration for iteration in checkpoint_iterations if iteration <= milestone
        ]
        if not best_eligible:
            raise RuntimeError(
                f"No checkpoint at or before reward peak step {peak.step} for milestone {milestone}"
            )
        if not boundary_eligible:
            raise RuntimeError(f"No checkpoint at or before milestone {milestone}")

        best_iteration = max(best_eligible)
        boundary_iteration = max(boundary_eligible)
        best_source = checkpoints[best_iteration]
        boundary_source = checkpoints[boundary_iteration]
        best_target = output_dir / f"h1_best_through_{milestone}.pt"
        boundary_target = output_dir / f"h1_milestone_{milestone}.pt"
        shutil.copy2(best_source, best_target)
        shutil.copy2(boundary_source, boundary_target)
        selection = {
            "milestone_iteration": milestone,
            "criterion": REWARD_TAG,
            "reward_peak_step": peak.step,
            "reward_peak_value": peak.value,
            "best_checkpoint_iteration": best_iteration,
            "best_source_checkpoint": str(best_source),
            "best_copied_checkpoint": str(best_target),
            "best_sha256": sha256_file(best_target),
            "selected_checkpoint_iteration": best_iteration,
            "source_checkpoint": str(best_source),
            "copied_checkpoint": str(best_target),
            "milestone_checkpoint_iteration": boundary_iteration,
            "milestone_source_checkpoint": str(boundary_source),
            "milestone_copied_checkpoint": str(boundary_target),
            "milestone_sha256": sha256_file(boundary_target),
        }
        selections.append(selection)
        print(json.dumps(selection, ensure_ascii=False))

    manifest = {
        "run_dir": str(run_dir),
        "criterion": REWARD_TAG,
        "best_selection_rule": "maximum finite scalar at or before milestone; latest saved checkpoint at or before the scalar peak",
        "milestone_selection_rule": "latest saved numbered checkpoint at or before milestone; zero-based final checkpoint is allowed",
        "selections": selections,
    }
    (output_dir / "milestone_best_selection.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
