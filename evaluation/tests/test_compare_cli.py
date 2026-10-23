import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import compare_cli
from eval_core import demo, write_json


class ComparisonCliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=Path(__file__).parent)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.env = patch.dict(os.environ, {"ISSACSIMZ_MODE": "personal"})
        self.env.start()
        self.addCleanup(self.env.stop)

    def run_cli(self, args):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return compare_cli.main(args)

    def saved_args(self):
        demo(self.root / "fixture", "go2", "scenario7")
        return ["--a", str(self.root / "fixture/a"), "--b", str(self.root / "fixture/b"),
                "--output", str(self.root / "result")]

    def checkpoint_args(self):
        task = self.root / "task"
        package = task / "go2_task"
        package.mkdir(parents=True)
        for name in ("__init__.py", "env_cfg.py", "agent_cfg.py"):
            (package / name).write_text("fixture")
        (task / "quadruped_rewards.py").write_text("fixture")
        lab = self.root / "lab"
        lab.mkdir()
        (lab / ("isaaclab.bat" if os.name == "nt" else "isaaclab.sh")).write_text("fixture")
        for name in ("a with spaces.pt", "b.pt"):
            (self.root / name).write_bytes(b"fixture")
        return ["--a", str(self.root / "a with spaces.pt"), "--b", str(self.root / "b.pt"),
                "--isaaclab-root", str(lab), "--task-root", str(task),
                "--output", str(self.root / "result")]

    def test_completed_evaluations_produce_html_json_and_provisional_calibration(self):
        args = self.saved_args()
        with patch.object(compare_cli.subprocess, "run") as run:
            self.assertEqual(self.run_cli(args), 0)
        run.assert_not_called()
        result = json.loads((self.root / "result/comparison.json").read_text())
        self.assertEqual(result["calibration_hash"], compare_cli.compare_policies(
            *compare_cli._read_evaluation(self.root / "fixture/a"),
            *compare_cli._read_evaluation(self.root / "fixture/b"),
            json.loads((self.root / "result/calibration.json").read_text()))["calibration_hash"])
        calibration = json.loads((self.root / "result/calibration.json").read_text())
        self.assertEqual(calibration["status"], "provisional")
        self.assertFalse(result["ranking_ready"])
        html = (self.root / "result/comparison.html").read_text(encoding="utf-8")
        self.assertIn("A (후보)", html)
        self.assertTrue(any("changing B" in warning for warning in result["warnings"]))

    def test_supplied_calibration_is_preserved(self):
        args = self.saved_args()
        self.assertEqual(self.run_cli(args + ["--calibration", str(self.root / "fixture/calibration.json")]), 0)
        self.assertEqual(json.loads((self.root / "result/calibration.json").read_text()),
                         json.loads((self.root / "fixture/calibration.json").read_text()))

    def test_failed_first_evaluation_does_not_launch_second_or_emit_report(self):
        args = self.checkpoint_args()
        with patch.object(compare_cli.subprocess, "run", side_effect=subprocess.CalledProcessError(1, "fixture")) as run:
            self.assertEqual(self.run_cli(args), 2)
        self.assertEqual(run.call_count, 1)
        self.assertTrue(self.root.joinpath("result").is_dir())
        self.assertFalse(self.root.joinpath("result/comparison.html").exists())

    def test_collector_runs_sequentially_with_matched_options(self):
        args = self.checkpoint_args()
        demo(self.root / "fixture", "go2", "scenario7")
        calls = []

        def collect(command, check):
            calls.append(command)
            source = self.root / "fixture" / ("a" if len(calls) == 1 else "b")
            target = Path(command[command.index("--output") + 1])
            target.mkdir()
            for name in ("evaluation_manifest.json", "episodes.jsonl"):
                target.joinpath(name).write_bytes(source.joinpath(name).read_bytes())

        with patch.object(compare_cli.subprocess, "run", side_effect=collect):
            self.assertEqual(self.run_cli(args), 0)
        self.assertEqual(len(calls), 2)
        for flag in ("--robot", "--suite", "--num-envs", "--seeds", "--task-root"):
            self.assertEqual(calls[0][calls[0].index(flag) + 1], calls[1][calls[1].index(flag) + 1])
        self.assertEqual(calls[0][0], sys.executable)
        self.assertNotIn("--smoke", calls[0])
        self.assertIn(str(self.root / "a with spaces.pt"), calls[0])

    def test_preview_does_not_launch_or_create_output(self):
        args = self.checkpoint_args()
        with patch.object(compare_cli.subprocess, "run") as run:
            self.assertEqual(self.run_cli(args + ["--preview"]), 0)
        run.assert_not_called()
        self.assertFalse(self.root.joinpath("result").exists())

    def test_incompatible_calibration_stops_before_second_evaluation(self):
        args = self.checkpoint_args()
        demo(self.root / "fixture", "go2", "scenario7")
        calibration = json.loads((self.root / "fixture/calibration.json").read_text())
        calibration["reference_protocol_id"] = "0" * 64
        write_json(self.root / "calibration.json", calibration)

        def collect(command, check):
            target = Path(command[command.index("--output") + 1])
            target.mkdir()
            for name in ("evaluation_manifest.json", "episodes.jsonl"):
                target.joinpath(name).write_bytes(self.root.joinpath("fixture/a", name).read_bytes())

        with patch.object(compare_cli.subprocess, "run", side_effect=collect) as run:
            self.assertEqual(self.run_cli(args + ["--calibration", str(self.root / "calibration.json")]), 2)
        self.assertEqual(run.call_count, 1)
        self.assertFalse(self.root.joinpath("result/comparison.html").exists())

    def test_existing_output_is_not_overwritten(self):
        args = self.saved_args()
        output = self.root / "result"
        output.mkdir()
        sentinel = output / "keep.txt"
        sentinel.write_text("preserve")
        self.assertEqual(self.run_cli(args), 2)
        self.assertEqual(sentinel.read_text(), "preserve")

    def test_official_and_mixed_input_formats_are_rejected_before_launch(self):
        args = self.checkpoint_args()
        with patch.object(compare_cli.subprocess, "run") as run:
            with patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}):
                self.assertEqual(self.run_cli(args), 2)
            self.assertEqual(self.run_cli(args + ["--policy-a"]), 2)
        run.assert_not_called()
        self.assertFalse(self.root.joinpath("result").exists())

    def test_incomplete_results_and_protocol_mismatch_do_not_emit_report(self):
        args = self.saved_args()
        path = self.root / "fixture/b/evaluation_manifest.json"
        manifest = json.loads(path.read_text())
        original = dict(manifest)
        manifest["complete"] = False
        write_json(path, manifest)
        self.assertEqual(self.run_cli(args), 2)
        self.assertFalse(self.root.joinpath("result/comparison.html").exists())
        original["protocol_id"] = "0" * 64
        write_json(path, original)
        args[-1] = str(self.root / "another-result")
        self.assertEqual(self.run_cli(args), 2)
        self.assertFalse(self.root.joinpath("another-result/comparison.html").exists())

    def test_prompt_input_supports_quoted_paths(self):
        args = self.saved_args()
        with patch("builtins.input", side_effect=['"' + args[1] + '"', args[3]]):
            self.assertEqual(self.run_cli(args[4:]), 0)


if __name__ == "__main__":
    unittest.main()
