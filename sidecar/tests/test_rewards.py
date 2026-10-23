from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from issacsimz_cli.cli import main


SAMPLE = '''REWARD_OVERRIDES = {
    "track_lin_vel_xy_exp": 1.0,
    "lin_vel_z_l2": -3.0,
    # "flat_orientation_l2": -1.0,
    # "termination_penalty": -200.0,
}
raise RuntimeError("reward modules must never be imported by issacsimz")
'''


class RewardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.task = self.base / "training" / "quadruped"
        self.task.mkdir(parents=True)
        (self.task / "train.py").write_text("# fixture\n", encoding="utf-8")
        self.reward = self.task / "quadruped_rewards.py"
        self.reward.write_text(SAMPLE, encoding="utf-8")
        self.environment = {"ISSACSIMZ_REWARD_STATE_ROOT": str(self.base / "state")}

    def tearDown(self) -> None:
        self.temp.cleanup()

    def command(self, *items: str) -> int:
        with patch.dict(os.environ, self.environment, clear=False):
            return main(["reward", *items, "--task-root", str(self.task)])

    def test_active_reward_changes_without_importing_module(self) -> None:
        self.assertEqual(self.command("set", "go2", "lin_vel_z_l2", "-4.0"), 0)
        self.assertIn('"lin_vel_z_l2": -4.0,', self.reward.read_text(encoding="utf-8"))
        self.assertEqual(self.command("show", "go2"), 0)

    def test_commented_reward_cannot_be_activated(self) -> None:
        before = self.reward.read_bytes()
        self.assertEqual(self.command("set", "go2", "flat_orientation_l2", "-0.5"), 2)
        self.assertEqual(self.reward.read_bytes(), before)
        self.assertFalse((self.base / "state").exists())

    def test_off_cannot_disable_active_or_commented_rewards(self) -> None:
        before = self.reward.read_bytes()
        for key in ("lin_vel_z_l2", "flat_orientation_l2"):
            with self.subTest(key=key):
                self.assertEqual(self.command("set", "go2", key, "off"), 2)
                self.assertEqual(self.reward.read_bytes(), before)
        self.assertFalse((self.base / "state").exists())

    def test_unknown_key_is_rejected_without_modification(self) -> None:
        before = self.reward.read_bytes()
        self.assertEqual(self.command("set", "go2", "learning_rate", "0.1"), 2)
        self.assertEqual(self.reward.read_bytes(), before)

    def test_duplicate_key_is_rejected_without_modification(self) -> None:
        self.reward.write_text(SAMPLE.replace('    # "termination_penalty": -200.0,', '    "lin_vel_z_l2": -2.0,'), encoding="utf-8")
        before = self.reward.read_bytes()
        self.assertEqual(self.command("set", "go2", "lin_vel_z_l2", "-4.0"), 2)
        self.assertEqual(self.reward.read_bytes(), before)

    def test_non_finite_values_are_rejected(self) -> None:
        before = self.reward.read_bytes()
        for value in ("nan", "inf"):
            with self.subTest(value=value): self.assertEqual(self.command("set", "go2", "lin_vel_z_l2", value), 2)
        # argparse rejects -inf before command dispatch because it resembles an option.
        with self.assertRaises(SystemExit): self.command("set", "go2", "lin_vel_z_l2", "-inf")
        self.assertEqual(self.reward.read_bytes(), before)

    def test_restore_is_byte_identical_to_first_baseline(self) -> None:
        original = self.reward.read_bytes()
        self.assertEqual(self.command("set", "go2", "lin_vel_z_l2", "-4.0"), 0)
        self.assertEqual(self.command("restore", "go2"), 0)
        self.assertEqual(self.reward.read_bytes(), original)

    def test_multiple_sets_restore_first_baseline(self) -> None:
        original = self.reward.read_bytes()
        self.assertEqual(self.command("set", "go2", "lin_vel_z_l2", "-4.0"), 0)
        self.assertEqual(self.command("set", "go2", "track_lin_vel_xy_exp", "1.25"), 0)
        self.assertEqual(self.command("restore", "go2"), 0)
        self.assertEqual(self.reward.read_bytes(), original)

    def test_restore_refuses_manual_external_change(self) -> None:
        self.assertEqual(self.command("set", "go2", "lin_vel_z_l2", "-4.0"), 0)
        self.reward.write_text(self.reward.read_text(encoding="utf-8") + "# manual change\n", encoding="utf-8")
        changed = self.reward.read_bytes()
        self.assertEqual(self.command("restore", "go2"), 2)
        self.assertEqual(self.reward.read_bytes(), changed)

    def test_restore_refuses_corrupted_stored_baseline(self) -> None:
        self.assertEqual(self.command("set", "go2", "lin_vel_z_l2", "-4.0"), 0)
        state_dir = next(Path(self.environment["ISSACSIMZ_REWARD_STATE_ROOT"]).iterdir())
        (state_dir / "original.py").write_text("CORRUPTED\n", encoding="utf-8")
        current = self.reward.read_bytes()
        self.assertEqual(self.command("restore", "go2"), 2)
        self.assertEqual(self.reward.read_bytes(), current)

    def test_set_refuses_corrupted_stored_baseline(self) -> None:
        self.assertEqual(self.command("set", "go2", "lin_vel_z_l2", "-4.0"), 0)
        state_dir = next(Path(self.environment["ISSACSIMZ_REWARD_STATE_ROOT"]).iterdir())
        (state_dir / "original.py").write_text("CORRUPTED\n", encoding="utf-8")
        current = self.reward.read_bytes()
        self.assertEqual(self.command("set", "go2", "track_lin_vel_xy_exp", "1.25"), 2)
        self.assertEqual(self.reward.read_bytes(), current)

    def test_non_object_metadata_is_rejected_without_modification(self) -> None:
        self.assertEqual(self.command("set", "go2", "lin_vel_z_l2", "-4.0"), 0)
        state_dir = next(Path(self.environment["ISSACSIMZ_REWARD_STATE_ROOT"]).iterdir())
        (state_dir / "metadata.json").write_text("[]\n", encoding="utf-8")
        current = self.reward.read_bytes()
        self.assertEqual(self.command("set", "go2", "lin_vel_z_l2", "-4.5"), 2)
        self.assertEqual(self.reward.read_bytes(), current)

    def test_diff_shows_only_managed_change(self) -> None:
        self.assertEqual(self.command("set", "go2", "lin_vel_z_l2", "-4.0"), 0)
        self.assertEqual(self.command("diff", "go2"), 0)


if __name__ == "__main__":
    unittest.main()
