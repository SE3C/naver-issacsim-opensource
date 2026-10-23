"""Interactive PERSONAL A/B evaluation using the existing collector and scorer."""
import argparse
import json
import os
import subprocess
import sys
import uuid
from datetime import datetime
from pathlib import Path

from eval_core import (calibrate, compare_policies, load_jsonl, load_suite,
                       report_html, validate_calibration, validate_dataset, write_json)
from isaac_runner import TASKS, _parse_seeds


def _input_path(value, prompt):
    text = (value or input(prompt)).strip().strip("\"'")
    if not text:
        raise ValueError("both input paths are required")
    path = Path(text).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"input does not exist: {path}")
    return path


def _read_evaluation(path):
    manifest = json.loads((path / "evaluation_manifest.json").read_text(encoding="utf-8-sig"))
    return load_jsonl(path / "episodes.jsonl"), manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description="PERSONAL A/B comparison; A=candidate, B=reference")
    parser.add_argument("--a", help="candidate .pt or completed evaluation directory")
    parser.add_argument("--b", help="reference .pt or completed evaluation directory")
    parser.add_argument("--robot", choices=tuple(TASKS), default="go2")
    parser.add_argument("--isaaclab-root")
    parser.add_argument("--task-root")
    parser.add_argument("--suite", choices=("scenario7", "terrain6"), default="scenario7")
    parser.add_argument("--num-envs", type=int, default=128)
    parser.add_argument("--seeds", default="4201,4202,4203")
    parser.add_argument("--policy-a", action="store_true", help="A is exported TorchScript, not a native checkpoint")
    parser.add_argument("--policy-b", action="store_true", help="B is exported TorchScript, not a native checkpoint")
    parser.add_argument("--calibration", help="optional existing calibration JSON; otherwise use B provisionally")
    parser.add_argument("--output", help="new result directory (must not already exist)")
    parser.add_argument("--preview", action="store_true", help="show commands; do not evaluate or create output")
    args = parser.parse_args(argv)
    output = None
    try:
        mode = os.environ.get("ISSACSIMZ_MODE", "personal").strip().lower()
        if mode != "personal":
            raise ValueError("this comparison CLI is PERSONAL only")
        a = _input_path(args.a, "Candidate A (.pt or completed evaluation directory): ")
        b = _input_path(args.b, "Reference B (.pt or completed evaluation directory): ")
        if a == b:
            raise ValueError("A and B must be different input paths")
        if args.num_envs < 1:
            raise ValueError("--num-envs must be positive")
        _parse_seeds(args.seeds, False)
        saved_evaluations = a.is_dir() and b.is_dir()
        if a.is_dir() != b.is_dir():
            raise ValueError("provide two .pt files or two completed evaluation directories")
        calibration = None
        if args.calibration:
            calibration = json.loads(Path(args.calibration).read_text(encoding="utf-8-sig"))
            if not saved_evaluations:
                validate_calibration(calibration, load_suite(args.robot, args.suite))
        output = Path(args.output).expanduser().resolve() if args.output else (
            a.parent / f"comparison-{args.robot}-{datetime.now():%Y%m%d-%H%M%S}-{uuid.uuid4().hex[:8]}")
        if output.exists():
            raise FileExistsError(f"output already exists; nothing overwritten: {output}")
        commands = []
        if saved_evaluations:
            data_a, data_b = _read_evaluation(a), _read_evaluation(b)
            if any(data[1]["robot"] != args.robot for data in (data_a, data_b)):
                raise ValueError("evaluation robot differs from --robot")
            if data_a[1]["policy"].get("kind") != data_b[1]["policy"].get("kind"):
                raise ValueError("comparison requires the same policy format for A and B")
        else:
            if args.policy_a != args.policy_b:
                raise ValueError("use two native checkpoints or two TorchScript policies; do not mix formats")
            for path in (a, b):
                if path.suffix.lower() != ".pt" or not path.is_file() or path.stat().st_size <= 0:
                    raise ValueError(f"input must be a nonempty .pt file: {path}")
            if not args.isaaclab_root or not args.task_root:
                raise ValueError("checkpoint evaluation requires --isaaclab-root and --task-root")
            lab = Path(args.isaaclab_root).expanduser().resolve()
            task = Path(args.task_root).expanduser().resolve()
            profile = TASKS[args.robot]
            required = [lab / ("isaaclab.bat" if os.name == "nt" else "isaaclab.sh"),
                        task / profile["package"] / "__init__.py",
                        task / profile["package"] / "env_cfg.py",
                        task / profile["package"] / "agent_cfg.py", task / profile["reward_file"]]
            for path in required:
                if not path.is_file():
                    raise FileNotFoundError(f"required source/launcher is missing: {path}")
            common = ["--mode", "personal", "--robot", args.robot, "--suite", args.suite,
                      "--isaaclab-root", str(lab), "--task-root", str(task),
                      "--num-envs", str(args.num_envs), "--seeds", args.seeds]
            for label, path, policy in (("a", a, args.policy_a), ("b", b, args.policy_b)):
                commands.append([sys.executable, "-u", str(Path(__file__).with_name("isaac_runner.py")),
                                 *common, "--policy" if policy else "--checkpoint", str(path),
                                 "--output", str(output / label)])
        print(f"A (candidate): {a}\nB (reference): {b}\nOutput: {output}", flush=True)
        if calibration is None:
            print("Calibration: B-reference PROVISIONAL; internal score only, not official ranking.", flush=True)
        if args.preview:
            print(json.dumps({"commands": commands, "saved_evaluations": saved_evaluations,
                              "output": str(output)}, indent=2))
            return 0
        output.mkdir(parents=True, exist_ok=False)
        if not saved_evaluations:
            print("Full camera-off evaluation: A then B. No training, video, publish, or shutdown.", flush=True)
            evaluations = []
            for label, command in zip(("a", "b"), commands):
                print(f"Evaluating {label.upper()}...", flush=True)
                subprocess.run(command, check=True)
                data = _read_evaluation(output / label)
                validate_dataset(*data)
                if calibration and calibration.get("reference_protocol_id") not in (None, data[1]["protocol_id"]):
                    raise ValueError("reference calibration belongs to another execution protocol")
                evaluations.append(data)
            data_a, data_b = evaluations
        if calibration is None:
            calibration = calibrate(*data_b, "reference-b-provisional")
        result = compare_policies(*data_a, *data_b, calibration)
        if not args.calibration:
            result["warnings"].append("B is the provisional reference: changing B or reversing A/B changes the score scale; do not rank across different pairs.")
        write_json(output / "calibration.json", calibration)
        write_json(output / "comparison.json", result)
        (output / "comparison.html").write_text(report_html(result), encoding="utf-8")
        print(f"REPORT: {output / 'comparison.html'}\nDelta A-B: {result['delta_A_minus_B']:+.3f}", flush=True)
        return 0
    except (ValueError, KeyError, TypeError, OSError, EOFError, subprocess.CalledProcessError, KeyboardInterrupt) as exc:
        print(f"COMPARISON FAILED: {exc}", file=sys.stderr)
        if output and output.exists():
            print(f"Raw output preserved: {output}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
