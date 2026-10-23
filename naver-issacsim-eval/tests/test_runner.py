import io
import json
import math
import os
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import isaac_runner as runner
from eval_core import load_suite


def add_sample(state, **updates):
    values = dict(vx_error=1., vy_error=0., yaw_error=0., actual_vx=0., actual_vy=0.,
                  command_vx=1., command_vy=0., roll=0., pitch=0., action=[0., 0.], dt=.02,
                  stall_command_m_s=.2, stall_speed_m_s=.1, base_contact_failure=False)
    values.update(updates)
    state.add(**values)


class RunnerTests(unittest.TestCase):
    def test_agent_config_uses_native_version_adapter(self):
        calls = []
        adapted = NS(actor=NS(hidden_dims=[64]), critic=NS(hidden_dims=[32]), policy=None)

        def adapter(cfg, version):
            calls.append((cfg.device, version))
            return adapted

        api = NS(handle_deprecated_rsl_rl_cfg=adapter)
        with patch.object(runner.importlib, "import_module", return_value=api), \
                patch.object(runner.importlib.metadata, "version", return_value="5.0.1"):
            cfg = runner._prepare_agent_cfg(lambda: NS(device="cuda:0"), "cpu")
        self.assertIs(cfg, adapted)
        self.assertEqual(calls, [("cpu", "5.0.1")])
        summary = runner._agent_summary(cfg)
        self.assertEqual(summary["actor_hidden_dims"], [64])
        self.assertEqual(summary["critic_hidden_dims"], [32])

    def test_older_lab_without_adapter_preserves_task_config(self):
        original = NS(device="cuda:0", policy=NS(actor_hidden_dims=[64]))
        with patch.object(runner.importlib, "import_module", return_value=NS()), \
                patch.object(runner.importlib.metadata, "version") as version:
            cfg = runner._prepare_agent_cfg(lambda: original, "cpu")
        self.assertIs(cfg, original)
        self.assertEqual(cfg.device, "cpu")
        version.assert_not_called()

    def test_body_frame_three_axis_norm_has_equal_weight(self):
        state = runner._EpisodeStats()
        add_sample(state, vx_error=3., vy_error=4., yaw_error=12.)
        self.assertEqual(state.diagnostics()["mean_tracking_error"], 13.)
        self.assertEqual(state.diagnostics()["xy_rmse"], 5.)
        self.assertEqual(state.diagnostics()["yaw_rmse"], 12.)

    def test_stationary_balance_is_not_commanded_motion_stall(self):
        state = runner._EpisodeStats()
        add_sample(state, command_vx=0.)
        self.assertEqual(state.diagnostics()["stall_fraction"], 0.)
        add_sample(state)
        self.assertEqual(state.diagnostics()["stall_fraction"], 1.)

    def test_episode_action_delta_and_motion_accumulation(self):
        state = runner._EpisodeStats()
        add_sample(state, actual_vx=1., action=[0., 0.])
        add_sample(state, actual_vx=1., action=[1., 1.])
        self.assertAlmostEqual(state.diagnostics()["forward_progress_m"], .04)
        self.assertEqual(state.diagnostics()["action_delta_rms"], 1.)

    def test_body_speed_integral_is_not_world_displacement(self):
        state = runner._EpisodeStats()
        add_sample(state, actual_vx=1., episode_start_world_xy=(10., 20.), world_xy=(10., 20.02))
        add_sample(state, actual_vx=1., world_xy=(10., 20.04))
        diagnostics = state.diagnostics()
        self.assertAlmostEqual(diagnostics["integrated_body_forward_m"], .04)
        self.assertEqual(diagnostics["world_dx_m"], 0.)
        self.assertAlmostEqual(diagnostics["world_dy_m"], .04)

    def test_first_episode_stops_collection_after_failure(self):
        suite = load_suite("go2", "terrain6")
        stream = io.StringIO()
        collector = runner._EpisodeCollector(args=NS(), suite=suite, scenario=suite["scenarios"][0],
            case=suite["scenarios"][0]["cases"][0], seed=42, num_envs=1, dt=.02,
            policy_sha256="a" * 64, protocol_id="b" * 64, torch=None, output_stream=stream)
        add_sample(collector.states[0], base_contact_failure=True)
        collector._finish(0, "terminated")
        collector.finish_horizon()
        rows = [json.loads(line) for line in stream.getvalue().splitlines()]
        self.assertEqual(len(rows), 1)
        self.assertFalse(rows[0]["survived"])
        self.assertTrue(rows[0]["base_contact_failure"])
        self.assertFalse(collector.active[0])

    def test_time_window_keeps_reset_episode_and_final_partial(self):
        suite = load_suite("h1", "scenario7")
        stream = io.StringIO()
        collector = runner._EpisodeCollector(args=NS(), suite=suite, scenario=suite["scenarios"][0],
            case=suite["scenarios"][0]["cases"][0], seed=42, num_envs=1, dt=.02,
            policy_sha256="a" * 64, protocol_id="b" * 64, torch=None, output_stream=stream)
        add_sample(collector.states[0], vx_error=4.)
        collector._finish(0, "terminated")
        add_sample(collector.states[0], vx_error=0.)
        collector.finish_horizon()
        rows = [json.loads(line) for line in stream.getvalue().splitlines()]
        self.assertEqual([r["end_reason"] for r in rows], ["terminated", "evaluation_end"])
        self.assertEqual([r["mean_tracking_error"] for r in rows], [4., 0.])
        self.assertNotEqual(rows[0]["episode_id"], rows[1]["episode_id"])

    def test_official_mode_rejected_in_python_boundary(self):
        with self.assertRaises(ValueError):
            runner._require_personal_mode(NS(mode="official"))
        with patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}):
            with self.assertRaises(ValueError):
                runner._require_personal_mode(NS(mode="personal"))

    def test_output_cannot_overwrite_existing_artifacts(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            original = Path(directory) / "policy.pt"
            original.write_bytes(b"original")
            with self.assertRaises(FileExistsError):
                runner._prepare_output(directory)
            self.assertEqual(original.read_bytes(), b"original")

    def test_robot_specific_slope_and_rough_domain_randomization(self):
        for robot, degrees in (("h1", 10), ("go2", 20)):
            suite = load_suite(robot, "terrain6")
            for spec in suite["scenarios"][-2:]:
                self.assertAlmostEqual(spec["cases"][0]["slope"], math.tan(math.radians(degrees)))
        g7 = load_suite("go2", "scenario7")["scenarios"][-1]["cases"][0]
        self.assertEqual(g7["terrain"], "random_rough")
        self.assertTrue(g7["randomization"])

    def test_old_wrapper_observation_tuple_is_unwrapped(self):
        obs = object()
        wrapper = NS(get_observations=lambda: (obs, {"extras": True}))
        self.assertIs(runner._get_observation(wrapper, "native_checkpoint"), obs)

    def test_native_tensordict_and_jit_policy_observation_are_distinct(self):
        policy_obs = object()
        obs = {"policy": policy_obs, "critic": object()}
        wrapper = NS(get_observations=lambda: obs)
        self.assertIs(runner._get_observation(wrapper, "native_checkpoint"), obs)
        self.assertIs(runner._get_observation(wrapper, "torchscript"), policy_obs)

    def test_native_load_does_not_restore_optimizer(self):
        calls = []
        actor = NS(is_recurrent=False)

        class FakeRunner:
            alg = NS(policy=actor)

            def load(self, path, load_optimizer=True):
                calls.append(load_optimizer)

            def get_inference_policy(self, device):
                return actor

        cfg = NS(to_dict=lambda: {"policy": {}})
        loaded, _, _ = runner._load_native_runner(FakeRunner(), cfg, Path("model.pt"), "cpu")
        self.assertIs(loaded, actor)
        self.assertEqual(calls, [False])

    def test_new_native_load_is_actor_only(self):
        calls = []
        actor = NS(is_recurrent=False)

        class FakeRunner:
            alg = NS(is_recurrent=False, get_policy=lambda: actor)

            def load(self, path, load_cfg=None, strict=True, map_location=None):
                calls.append(load_cfg)

        cfg = NS(to_dict=lambda: {"actor": {}, "critic": {}})
        loaded, _, _ = runner._load_native_runner(FakeRunner(), cfg, Path("model.pt"), "cpu")
        self.assertIs(loaded, actor)
        self.assertEqual(calls, [{"actor": True, "critic": False, "optimizer": False,
                                  "iteration": False, "rnd": False}])

    def test_native_loader_rejects_unknown_api_and_mismatched_config(self):
        class UnknownRunner:
            def load(self, path):
                self.fail_if_called = True

        class NewRunner:
            def load(self, path, load_cfg=None, strict=True, map_location=None):
                self.fail_if_called = True

        cfg = NS(to_dict=lambda: {"policy": {}})
        with self.assertRaises(RuntimeError):
            runner._load_native_runner(UnknownRunner(), cfg, Path("model.pt"), "cpu")
        with self.assertRaises(RuntimeError):
            runner._load_native_runner(NewRunner(), cfg, Path("model.pt"), "cpu")

    def test_legacy_actor_critic_attribute_is_supported(self):
        actor = NS(is_recurrent=False)

        class FakeRunner:
            alg = NS(actor_critic=actor)

            def load(self, path, load_optimizer=True):
                pass

            def get_inference_policy(self, device):
                return actor

        cfg = NS(to_dict=lambda: {"policy": {}})
        loaded, _, _ = runner._load_native_runner(FakeRunner(), cfg, Path("model.pt"), "cpu")
        self.assertIs(loaded, actor)

    def test_contact_diagnostic_uses_public_termination_api(self):
        contact = object()
        manager = NS(active_terms=["time_out", "base_contact", "orientation"],
                     get_term=lambda name: contact if name == "base_contact" else None)
        self.assertEqual(runner._contact_terms(manager), [contact])
        self.assertEqual(runner._contact_terms(NS(active_terms=[], get_term=lambda _: None)), [])

    def test_config_fingerprint_keeps_function_identity_and_infinity(self):
        value = NS(func=add_sample, maximum=float("inf"), slope=(.2, .4))
        normalized = runner._normalize_config(value)["fields"]
        self.assertIn("add_sample", normalized["func"])
        self.assertEqual(normalized["maximum"], {"nonfinite_float": "inf"})
        self.assertEqual(normalized["slope"], [.2, .4])

    def test_case_config_removes_noise_curriculum_and_native_push(self):
        cfg = NS(commands=NS(base_velocity=NS(heading_command=True, rel_standing_envs=.2,
                                             resampling_time_range=(1, 2))),
                 episode_length_s=15,
                 observations=NS(policy=NS(enable_corruption=True)),
                 curriculum=NS(terrain_levels=object()),
                 scene=NS(terrain=NS(terrain_type="generator", terrain_generator=object())),
                 events=NS(push_robot=NS(func=lambda: None, mode="interval", params={})))
        runner._configure_case(cfg, {"terrain": "flat"}, 20.)
        self.assertFalse(cfg.observations.policy.enable_corruption)
        self.assertIsNone(cfg.curriculum.terrain_levels)
        self.assertIsNone(cfg.events.push_robot)
        self.assertEqual(cfg.scene.terrain.terrain_type, "plane")
        self.assertFalse(cfg.commands.base_velocity.heading_command)

    def test_domain_randomization_cannot_silently_disappear(self):
        cfg = NS(commands=NS(base_velocity=NS()), episode_length_s=20,
                 observations=NS(), curriculum=NS(),
                 scene=NS(terrain=NS(terrain_type="plane", terrain_generator=None)), events=NS())
        with self.assertRaises(ValueError):
            runner._configure_case(cfg, {"terrain": "flat", "randomization": {
                "friction_range": [.6, 1.2], "added_mass_range": [-1., 1.]}}, 20.)


if __name__ == "__main__":
    unittest.main()
