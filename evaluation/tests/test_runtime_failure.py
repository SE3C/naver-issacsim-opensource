import json
import sys
import tempfile
import time
import unittest
from pathlib import Path
from types import ModuleType, SimpleNamespace as NS
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import isaac_runner as runner
from eval_core import write_json


class RuntimeFailureTests(unittest.TestCase):
    def test_pre_episode_exception_is_saved_with_traceback_and_failed_status(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            manifest = {"execution_status": "RUNNING", "complete": False}
            with patch.object(runner, "_one_shot_gpu_info", side_effect=OSError("nvidia-smi unavailable")):
                try:
                    raise RuntimeError("CUDA peak-memory reset failed")
                except RuntimeError as exc:
                    runner._record_runtime_failure(
                        output=output, manifest=manifest, started=time.monotonic() - 1,
                        exc=exc, write_json=write_json,
                    )
                    saved = json.loads((output / "evaluation_manifest.json").read_text(encoding="utf-8"))
                    failure_notes = getattr(exc, "__notes__", [])

            self.assertEqual(saved["execution_status"], "FAILED")
            self.assertFalse(saved["complete"])
            self.assertEqual(saved["error"], "RuntimeError: CUDA peak-memory reset failed")
            self.assertIn("RuntimeError: CUDA peak-memory reset failed", saved["error_traceback"])
            self.assertTrue(any("nvidia-smi unavailable" in note for note in failure_notes))

    def test_manifest_write_failure_does_not_replace_runtime_exception(self):
        original = RuntimeError("initialization failed")

        def fail_write(*_args):
            raise OSError("disk unavailable")

        with patch.object(runner, "_one_shot_gpu_info", return_value=None):
            try:
                raise original
            except RuntimeError as exc:
                runner._record_runtime_failure(
                    output=Path("unused"), manifest={"execution_status": "RUNNING"},
                    started=time.monotonic(), exc=exc, write_json=fail_write,
                )
                self.assertIs(exc, original)
                self.assertTrue(any("disk unavailable" in note for note in getattr(exc, "__notes__", [])))

    def test_close_failure_does_not_mask_evaluation_exception(self):
        class SimulationApp:
            def __init__(self):
                self.close_calls = 0

            def close(self):
                self.close_calls += 1
                raise RuntimeError("close failed")

        simulation_app = SimulationApp()
        original = ValueError("cohort initialization failed")
        isaaclab = ModuleType("isaaclab")
        isaaclab.__path__ = []
        app_module = ModuleType("isaaclab.app")
        app_module.AppLauncher = lambda _args: NS(app=simulation_app)

        with patch.dict(sys.modules, {"isaaclab": isaaclab, "isaaclab.app": app_module}), \
                patch.object(runner, "_parse_args", return_value=NS()), \
                patch.object(runner, "_require_personal_mode"), \
                patch.object(runner, "_run", side_effect=original):
            with self.assertRaises(ValueError) as raised:
                runner.main([])

        self.assertIs(raised.exception, original)
        self.assertEqual(simulation_app.close_calls, 1)
        self.assertTrue(any("close failed" in note for note in getattr(original, "__notes__", [])))


if __name__ == "__main__":
    unittest.main()
