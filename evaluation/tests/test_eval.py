"""Contract tests for the offline policy evaluator core."""

from __future__ import annotations

import copy
import math
import sys
import unittest
from pathlib import Path
from typing import Any


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from eval_core import (  # noqa: E402
    calibrate,
    compare_policies,
    load_suite,
    protocol_hash,
    score_policy,
    validate_dataset,
)


def _scenario_cases(suite: Any, robot: str, suite_name: str) -> list[tuple[str, str]]:
    return [(scenario["id"], case["id"]) for scenario in suite["scenarios"]
            for case in scenario["cases"]]


def _fixture(
    suite_name: str = "scenario7",
    robot: str = "go2",
    policy_sha: str = "a" * 64,
    num_envs: int = 2,
) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    suite = load_suite(robot, suite_name)
    protocol = {
        "suite": suite,
        "num_envs": num_envs,
        "seeds": [42],
        "collector_version": "1",
    }
    manifest = {
        "schema": "se3c-evaluation-v1",
        "robot": robot,
        "suite": suite,
        "protocol": protocol,
        "protocol_id": protocol_hash(protocol),
        "policy": {"sha256": policy_sha, "path": "model.pt"},
        "complete": True,
    }

    pairs = _scenario_cases(suite, robot, suite_name)
    if not pairs:
        raise AssertionError(f"load_suite({robot!r}, {suite_name!r}) exposes no scenarios")

    rows = []
    episode = 0
    for scenario, case in pairs:
        for env_id in range(num_envs):
            episode += 1
            rows.append(
                {
                    "scenario": scenario,
                    "case": case,
                    "seed": 42,
                    "env_id": env_id,
                    "episode_id": f"ep-{episode:04d}",
                    "steps": 1000,
                    "duration_s": 20.0,
                    "end_reason": "evaluation_end",
                    "survived": True,
                    "mean_tracking_error": 1.0,
                    "policy_sha256": policy_sha,
                    "protocol_id": manifest["protocol_id"],
                }
            )
    return suite, manifest, rows


def _calibration(manifest: dict[str, Any], calibration_id: str = "cal-001") -> dict[str, Any]:
    suite = manifest["suite"]
    rows = []
    episode = 0
    for scenario in suite["scenarios"]:
        for case in scenario["cases"]:
            for seed in manifest["protocol"]["seeds"]:
                for env_id in range(manifest["protocol"]["num_envs"]):
                    episode += 1
                    rows.append(
                        {
                            "scenario": scenario["id"],
                            "case": case["id"],
                            "seed": seed,
                            "env_id": env_id,
                            "episode_id": f"cal-ep-{episode:04d}",
                            "steps": 1000,
                            "duration_s": suite["duration_s"],
                            "end_reason": "evaluation_end",
                            "survived": True,
                            "mean_tracking_error": 1.0,
                            "policy_sha256": manifest["policy"]["sha256"],
                            "protocol_id": manifest["protocol_id"],
                        }
                    )
    return calibrate(rows, manifest, calibration_id)


class EvaluatorContractTests(unittest.TestCase):
    def test_signed_world_displacement_is_valid(self):
        _, manifest, rows = _fixture()
        for row in rows:
            row.update(world_dx_m=-2., world_dy_m=-3., integrated_body_forward_m=-1.)
        result = score_policy(rows, manifest, _calibration(manifest))
        self.assertEqual(result["scenarios"]["G1"]["diagnostics"]["world_dx_m"], -2.)

    def test_score_and_scenario_values_stay_within_numeric_limits(self) -> None:
        _, manifest, rows = _fixture()
        result = score_policy(rows, manifest, _calibration(manifest))

        self.assertTrue(math.isfinite(result["internal_policy_score"]))
        self.assertGreaterEqual(result["internal_policy_score"], 0.0)
        self.assertLessEqual(result["internal_policy_score"], 100.0)
        for scenario in result["scenarios"].values():
            self.assertGreaterEqual(scenario["survival_rate"], 0.0)
            self.assertLessEqual(scenario["survival_rate"], 1.0)
            self.assertGreaterEqual(scenario["internal_tracking_score"], 0.0)
            self.assertLessEqual(scenario["internal_tracking_score"], 1.0)

    def test_tracking_transform_is_applied_after_equal_episode_mean(self) -> None:
        _, manifest, rows = _fixture()
        first_scenario = rows[0]["scenario"]
        scenario_rows = [row for row in rows if row["scenario"] == first_scenario]
        scenario_rows[0]["mean_tracking_error"] = 0.0
        scenario_rows[1]["mean_tracking_error"] = 2.0

        result = score_policy(rows, manifest, _calibration(manifest))
        scenario_score = result["scenarios"][first_scenario]

        self.assertEqual(scenario_score["mean_tracking_error"], 1.0)
        self.assertAlmostEqual(scenario_score["internal_tracking_score"], 0.5, places=12)
        self.assertNotAlmostEqual(scenario_score["internal_tracking_score"], (1.0 + 0.25) / 2.0)

    def test_missing_case_cohort_is_rejected(self) -> None:
        _, manifest, rows = _fixture()
        incomplete = copy.deepcopy(rows)
        incomplete.pop()

        with self.assertRaises(ValueError):
            validate_dataset(incomplete, manifest)

    def test_scenario7_accepts_terminal_reset_and_horizon_partial_in_one_cohort(self) -> None:
        suite, manifest, rows = _fixture("scenario7")
        self.assertEqual(suite["episode_mode"], "time_window")
        revised = copy.deepcopy(rows)
        original = revised.pop(0)
        terminal = copy.deepcopy(original)
        terminal.update(
            episode_id="ep-terminal",
            duration_s=7.0,
            steps=350,
            end_reason="terminated",
            survived=False,
        )
        partial = copy.deepcopy(original)
        partial.update(
            episode_id="ep-horizon-partial",
            duration_s=13.0,
            steps=650,
        )
        revised.extend([terminal, partial])

        validate_dataset(revised, manifest)

    def test_terrain6_allows_first_episode_to_end_early(self) -> None:
        suite, manifest, rows = _fixture("terrain6")
        self.assertEqual(suite["episode_mode"], "first_episode")
        revised = copy.deepcopy(rows)
        revised[0].update(
            duration_s=3.2,
            steps=160,
            end_reason="terminated",
            survived=False,
        )

        validate_dataset(revised, manifest)

    def test_failure_termination_takes_priority_over_survived_flag(self) -> None:
        _, manifest, rows = _fixture("terrain6")
        contradictory = copy.deepcopy(rows)
        contradictory[0].update(end_reason="terminated", survived=True)

        with self.assertRaises(ValueError):
            validate_dataset(contradictory, manifest)

    def test_invalid_required_values_are_rejected(self) -> None:
        _, manifest, rows = _fixture()
        bad_cases = [
            ("survived", 1),
            ("mean_tracking_error", True),
            ("mean_tracking_error", float("nan")),
            ("mean_tracking_error", float("inf")),
            ("mean_tracking_error", -0.01),
            ("steps", 0),
            ("duration_s", float("nan")),
        ]
        for key, value in bad_cases:
            with self.subTest(key=key, value=value):
                malformed = copy.deepcopy(rows)
                malformed[0][key] = value
                with self.assertRaises(ValueError):
                    validate_dataset(malformed, manifest)

    def test_row_policy_and_protocol_must_match_manifest(self) -> None:
        _, manifest, rows = _fixture()
        for key, value in (
            ("policy_sha256", "b" * 64),
            ("protocol_id", "not-the-manifest-protocol"),
        ):
            with self.subTest(key=key):
                mismatched = copy.deepcopy(rows)
                mismatched[0][key] = value
                with self.assertRaises(ValueError):
                    validate_dataset(mismatched, manifest)

    def test_comparison_rejects_different_protocols(self) -> None:
        _, manifest_a, rows_a = _fixture(policy_sha="a" * 64)
        _, manifest_b, rows_b = _fixture(policy_sha="b" * 64, num_envs=3)

        with self.assertRaises(ValueError):
            compare_policies(rows_a, manifest_a, rows_b, manifest_b, _calibration(manifest_a))

    def test_comparison_allows_reset_count_difference_with_same_cohorts(self) -> None:
        _, manifest_a, rows_a = _fixture(policy_sha="a" * 64)
        _, manifest_b, rows_b = _fixture(policy_sha="b" * 64)
        # A time-window evaluator may record different episode counts after
        # different numbers of terminal resets. Cohorts remain paired by
        # scenario/case/seed/environment, not by episode_id.
        original = rows_b.pop(0)
        first = copy.deepcopy(original)
        first.update(
            episode_id="policy-b-reset",
            duration_s=7.0,
            steps=350,
            end_reason="terminated",
            survived=False,
        )
        second = copy.deepcopy(original)
        second.update(
            episode_id="policy-b-partial",
            duration_s=13.0,
            steps=650,
        )
        rows_b.extend([first, second])

        comparison = compare_policies(
            rows_a,
            manifest_a,
            rows_b,
            manifest_b,
            _calibration(manifest_a),
            bootstrap=200,
            seed=7,
        )
        self.assertIn("delta_A_minus_B", comparison)
        self.assertIn("ci95_delta", comparison)
        self.assertIn("warnings", comparison)

    def test_comparison_bootstrap_is_deterministic(self) -> None:
        _, manifest_a, rows_a = _fixture(policy_sha="a" * 64)
        _, manifest_b, rows_b = _fixture(policy_sha="b" * 64)
        calibration = _calibration(manifest_a)

        first = compare_policies(rows_a, manifest_a, rows_b, manifest_b, calibration, bootstrap=200, seed=7)
        second = compare_policies(rows_a, manifest_a, rows_b, manifest_b, calibration, bootstrap=200, seed=7)
        self.assertEqual(first, second)

    def test_same_policy_and_same_outcomes_are_a_tie(self) -> None:
        _, manifest, rows = _fixture(policy_sha="a" * 64)
        result = compare_policies(rows, manifest, copy.deepcopy(rows), copy.deepcopy(manifest), _calibration(manifest))

        self.assertEqual(result["delta_A_minus_B"], 0.0)
        self.assertEqual(result["conclusion"], "TIE")

    def test_calibration_is_bound_to_robot_suite_and_positive_finite_e50(self) -> None:
        _, manifest, rows = _fixture()
        calibration = calibrate(rows, manifest, "cal-valid")

        self.assertEqual(calibration["schema"], "se3c-calibration-v1")
        self.assertEqual(calibration["id"], "cal-valid")
        self.assertEqual(calibration["robot"], manifest["robot"])
        self.assertEqual(calibration["suite_hash"], protocol_hash(manifest["suite"]))
        self.assertTrue(calibration["e50_by_scenario"])
        for value in calibration["e50_by_scenario"].values():
            self.assertTrue(math.isfinite(value))
            self.assertGreater(value, 0.0)

        invalid = copy.deepcopy(calibration)
        first_scenario = next(iter(invalid["e50_by_scenario"]))
        invalid["e50_by_scenario"][first_scenario] = 0.0
        with self.assertRaises(ValueError):
            score_policy(rows, manifest, invalid)


if __name__ == "__main__":
    unittest.main()
