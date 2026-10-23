"""Camera-off PERSONAL Isaac Lab collector for numeric policy evaluation."""
from __future__ import annotations

import argparse
import importlib
import importlib.metadata
import inspect
import json
import math
import os
import random
import shutil
import subprocess
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace


COLLECTOR_VERSION = "se3c-isaac-collector-v1"
TASKS = {
    "h1": {
        "task_id": "Humanoid-v0",
        "package": "h1_task",
        "env_class": "HumanoidRoughEnvCfg",
        "agent_class": "HumanoidPPORunnerCfg",
        "reward_file": "humanoid_rewards.py",
    },
    "go2": {
        "task_id": "Quadruped-v0",
        "package": "go2_task",
        "env_class": "QuadrupedRoughEnvCfg",
        "agent_class": "QuadrupedPPORunnerCfg",
        "reward_file": "quadruped_rewards.py",
    },
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="PERSONAL camera-off numeric policy evaluation"
    )
    parser.add_argument("--mode", choices=("personal", "official"), required=True)
    parser.add_argument("--robot", choices=tuple(TASKS), required=True)
    parser.add_argument("--suite", choices=("scenario7", "terrain6"), default="scenario7")
    parser.add_argument("--task-root", required=True)
    parser.add_argument("--isaaclab-root")
    policy_group = parser.add_mutually_exclusive_group(required=True)
    policy_group.add_argument("--checkpoint", help="Native RSL-RL model_*.pt checkpoint")
    policy_group.add_argument("--policy", help="TorchScript policy.pt exported by play.py")
    parser.add_argument("--source-run-id")
    parser.add_argument("--preset")
    parser.add_argument("--output", required=True)
    parser.add_argument("--num-envs", type=int, default=128)
    parser.add_argument("--seeds", default="4201,4202,4203")
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--duration", type=float)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args(argv)
    args.headless = True
    args.enable_cameras = False
    return args


def _parse_seeds(value: str, smoke: bool) -> list[int]:
    try:
        seeds = [int(token.strip()) for token in value.split(",") if token.strip()]
    except ValueError as exc:
        raise ValueError("--seeds must be a comma-separated list of non-negative integers") from exc
    if not seeds or any(seed < 0 for seed in seeds) or len(set(seeds)) != len(seeds):
        raise ValueError("--seeds must contain unique non-negative integers")
    return seeds[:1] if smoke else seeds


def _require_personal_mode(args: argparse.Namespace) -> None:
    if args.mode != "personal":
        raise ValueError("this evaluator accepts --mode personal only")
    if os.environ.get("ISSACSIMZ_MODE", "").strip().lower() == "official":
        raise ValueError("ISSACSIMZ_MODE=official blocks the PERSONAL evaluator")


def _resolve_inputs(args: argparse.Namespace) -> tuple[Path, Path, str, str]:
    task_root = Path(args.task_root).expanduser().resolve()
    profile = TASKS[args.robot]
    package_dir = task_root / profile["package"]
    reward_path = task_root / profile["reward_file"]
    for required in (
        package_dir / "__init__.py",
        package_dir / "env_cfg.py",
        package_dir / "agent_cfg.py",
        reward_path,
    ):
        if not required.is_file():
            raise FileNotFoundError(f"task source not found: {required}")
    policy_arg = args.checkpoint or args.policy
    policy_path = Path(policy_arg).expanduser().resolve()
    if not policy_path.is_file() or policy_path.stat().st_size <= 0:
        raise FileNotFoundError(f"policy file missing or empty: {policy_path}")
    kind = "rsl_rl_checkpoint" if args.checkpoint else "torchscript"
    return task_root, policy_path, kind, profile["task_id"]


def _load_task_configs(task_root: Path, robot: str):
    if str(task_root) not in sys.path:
        sys.path.insert(0, str(task_root))
    profile = TASKS[robot]
    importlib.import_module(profile["package"])
    env_module = importlib.import_module(f"{profile['package']}.env_cfg")
    agent_module = importlib.import_module(f"{profile['package']}.agent_cfg")
    return (
        getattr(env_module, profile["env_class"]),
        getattr(agent_module, profile["agent_class"]),
    )


def _prepare_agent_cfg(agent_cfg_class, device: str):
    agent_cfg = agent_cfg_class()
    if hasattr(agent_cfg, "device"):
        agent_cfg.device = device
    rsl_api = importlib.import_module("isaaclab_rl.rsl_rl")
    adapter = getattr(rsl_api, "handle_deprecated_rsl_rl_cfg", None)
    if adapter is not None:
        agent_cfg = adapter(agent_cfg, importlib.metadata.version("rsl-rl-lib"))
    return agent_cfg


def _configure_case(env_cfg, case: dict, duration_s: float) -> None:
    command_cfg = env_cfg.commands.base_velocity
    command_cfg.heading_command = False
    command_cfg.rel_standing_envs = 0.0
    command_cfg.resampling_time_range = (duration_s + 1.0, duration_s + 1.0)
    if hasattr(command_cfg, "rel_heading_envs"):
        command_cfg.rel_heading_envs = 0.0
    if hasattr(env_cfg, "episode_length_s"):
        env_cfg.episode_length_s = duration_s
    observations = getattr(env_cfg, "observations", None)
    if observations is not None:
        for group in vars(observations).values():
            if hasattr(group, "enable_corruption"):
                group.enable_corruption = False
    curriculum = getattr(env_cfg, "curriculum", None)
    if curriculum is not None:
        for name, term in list(vars(curriculum).items()):
            if term is not None:
                setattr(curriculum, name, None)

    terrain_cfg = env_cfg.scene.terrain
    terrain_name = case["terrain"]
    if terrain_name == "flat":
        terrain_cfg.terrain_type = "plane"
        terrain_cfg.terrain_generator = None
    else:
        terrain_cfg.terrain_type = "generator"
        generator = terrain_cfg.terrain_generator
        if generator is None:
            raise ValueError("rough terrain case has no terrain generator")
        sub_terrains = generator.sub_terrains
        if terrain_name not in sub_terrains:
            raise ValueError(f"terrain {terrain_name!r} is unavailable in this task config")
        for name, sub_cfg in sub_terrains.items():
            if not hasattr(sub_cfg, "proportion"):
                raise ValueError(f"terrain {name!r} has no configurable proportion")
            sub_cfg.proportion = 1.0 if name == terrain_name else 0.0
        difficulty = float(case.get("difficulty", 0.5))
        if hasattr(generator, "difficulty_range"):
            generator.difficulty_range = (difficulty, difficulty)
        if hasattr(generator, "curriculum"):
            generator.curriculum = False

        if "slope" in case:
            sub_cfg = sub_terrains[terrain_name]
            if not hasattr(sub_cfg, "slope_range"):
                raise ValueError(f"terrain {terrain_name!r} cannot accept the requested slope")
            sub_cfg.slope_range = (float(case["slope"]), float(case["slope"]))
        if "step_height" in case:
            sub_cfg = sub_terrains[terrain_name]
            if not hasattr(sub_cfg, "step_height_range"):
                raise ValueError(f"terrain {terrain_name!r} cannot accept the requested step height")
            sub_cfg.step_height_range = (float(case["step_height"]), float(case["step_height"]))

    randomization = case.get("randomization", False)
    randomization_cfg = randomization if isinstance(randomization, dict) else {}
    randomization_enabled = bool(randomization)
    if randomization_enabled and not {
        "friction_range", "added_mass_range"
    }.issubset(randomization_cfg):
        raise ValueError("domain randomization requires explicit friction_range and added_mass_range")
    event_cfg = env_cfg.events
    material_event_found = False
    mass_event_found = False
    for name, event in list(vars(event_cfg).items()):
        if event is None or not hasattr(event, "func"):
            continue
        function_name = getattr(event.func, "__name__", str(event.func)).lower()
        mode = str(getattr(event, "mode", "")).lower()
        params = getattr(event, "params", {}) or {}
        if "push" in name.lower() or "push" in function_name or mode == "interval":
            setattr(event_cfg, name, None)
            continue
        if "randomize_rigid_body_material" in function_name:
            material_event_found = True
            if not randomization_enabled:
                setattr(event_cfg, name, None)
                continue
            friction_range = randomization_cfg.get("friction_range")
            if friction_range is not None:
                params["static_friction_range"] = tuple(friction_range)
                params["dynamic_friction_range"] = tuple(friction_range)
            continue
        if "randomize_rigid_body_mass" in function_name:
            mass_event_found = True
            if not randomization_enabled:
                setattr(event_cfg, name, None)
                continue
            mass_range = randomization_cfg.get("added_mass_range")
            if mass_range is not None:
                params["mass_distribution_params"] = tuple(mass_range)
                params["operation"] = "add"
            continue
        if mode == "reset" and function_name in {"reset_root_state_uniform", "reset_joints_by_scale"}:
            continue
        setattr(event_cfg, name, None)
    if randomization_enabled and not (material_event_found and mass_event_found):
        raise ValueError("requested domain randomization requires material and added-mass event terms")


def _make_env_cfg(env_cfg_class, *, case: dict, duration_s: float,
                  num_envs: int, device: str, seed: int):
    env_cfg = env_cfg_class()
    env_cfg.scene.num_envs = num_envs
    env_cfg.sim.device = device
    env_cfg.seed = seed
    _configure_case(env_cfg, case, duration_s)
    return env_cfg


def _normalize_config(value, *, depth: int = 0, seen: set[int] | None = None):
    if isinstance(value, float) and not math.isfinite(value):
        return {"nonfinite_float": str(value)}
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if depth >= 12:
        return {"type": type(value).__qualname__, "truncated": True}
    if callable(value):
        return f"{getattr(value, '__module__', '')}.{getattr(value, '__qualname__', type(value).__qualname__)}"
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (tuple, list)):
        return [_normalize_config(item, depth=depth + 1, seen=seen) for item in value]
    if isinstance(value, dict):
        return {str(key): _normalize_config(item, depth=depth + 1, seen=seen)
                for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))}
    seen = seen if seen is not None else set()
    marker = id(value)
    if marker in seen:
        return {"type": type(value).__qualname__, "shared_reference": True}
    if hasattr(value, "__dict__"):
        seen.add(marker)
        fields = {
            name: _normalize_config(item, depth=depth + 1, seen=seen)
            for name, item in sorted(vars(value).items())
            if not name.startswith("_")
        }
        seen.remove(marker)
        return {"type": type(value).__qualname__, "fields": fields}
    return {"type": type(value).__qualname__}


def _runtime_versions(AppLauncher, isaaclab_root_arg: str | None) -> dict:
    def package_version(name: str) -> str:
        try:
            return importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            return "unavailable"

    root_candidates = [isaaclab_root_arg, os.environ.get("ISAACLAB_PATH"),
                       os.environ.get("ISSACSIMZ_ISAACLAB_ROOT")]
    launcher_file = Path(inspect.getfile(AppLauncher)).resolve()
    root_candidates.extend(str(parent) for parent in launcher_file.parents if (parent / ".git").exists())
    isaaclab_root = next(
        (Path(value).expanduser().resolve() for value in root_candidates if value and (Path(value).expanduser() / ".git").exists()),
        None,
    )
    isaaclab_commit = "unavailable"
    if isaaclab_root is not None:
        try:
            result = subprocess.run(
                ["git", "-C", str(isaaclab_root), "rev-parse", "HEAD"],
                capture_output=True, text=True, check=True, timeout=10,
            )
            isaaclab_commit = result.stdout.strip()
        except (OSError, subprocess.SubprocessError):
            pass
    try:
        import torch
        torch_version = torch.__version__
    except Exception:
        torch_version = "unavailable"
    try:
        rsl_version = package_version("rsl-rl-lib")
        if rsl_version == "unavailable":
            rsl_version = package_version("rsl_rl")
    except Exception:
        rsl_version = "unavailable"
    try:
        isaaclab_version = package_version("isaaclab")
    except Exception:
        isaaclab_version = "unavailable"
    return {
        "isaaclab_version": isaaclab_version,
        "isaaclab_commit": isaaclab_commit,
        "isaacsim_version": package_version("isaacsim"),
        "rsl_rl_version": rsl_version,
        "torch_version": str(torch_version),
    }


def _source_fingerprints(task_root: Path, robot: str, file_sha256) -> dict[str, str]:
    profile = TASKS[robot]
    relative_paths = [
        Path(profile["package"]) / "__init__.py",
        Path(profile["package"]) / "env_cfg.py",
        Path(profile["package"]) / "agent_cfg.py",
        Path(profile["reward_file"]),
    ]
    return {path.as_posix(): file_sha256(task_root / path) for path in relative_paths}


def _agent_summary(agent_cfg) -> dict:
    policy_cfg = getattr(agent_cfg, "policy", None) or getattr(agent_cfg, "actor", None)
    critic_cfg = getattr(agent_cfg, "critic", None)
    return {
        "runner_config_class": type(agent_cfg).__name__,
        "runner_class_name": getattr(agent_cfg, "class_name", None),
        "policy_class_name": getattr(policy_cfg, "class_name", None),
        "actor_hidden_dims": list(getattr(policy_cfg, "actor_hidden_dims", getattr(policy_cfg, "hidden_dims", [])) or []),
        "critic_hidden_dims": list(getattr(policy_cfg, "critic_hidden_dims", getattr(critic_cfg, "hidden_dims", [])) or []),
        "activation": getattr(policy_cfg, "activation", None),
        "empirical_normalization": bool(getattr(agent_cfg, "empirical_normalization", False)),
        "policy_observation_normalization": getattr(policy_cfg, "obs_normalization", False),
        "recurrent": False,
    }


def _load_native_runner(runner, agent_cfg, checkpoint: Path, device: str):
    config = agent_cfg.to_dict()
    load_parameters = inspect.signature(runner.load).parameters
    if "load_cfg" in load_parameters:
        if not {"actor", "critic"}.issubset(config):
            raise RuntimeError(
                "installed RSL-RL uses the actor/critic config schema, but this task agent config "
                "uses a different schema; use a compatible training stack or exported TorchScript policy"
            )
        runner.load(
            str(checkpoint),
            load_cfg={"actor": True, "critic": False, "optimizer": False,
                      "iteration": False, "rnd": False},
            strict=True,
            map_location=device,
        )
        actor_critic = runner.alg
        if bool(getattr(actor_critic, "is_recurrent", False)):
            raise ValueError("recurrent native policies are not supported")
        if not hasattr(actor_critic, "get_policy"):
            raise RuntimeError("installed RSL-RL actor does not expose get_policy()")
        actor = actor_critic.get_policy()
        return actor, actor_critic, "OnPolicyRunner.load(load_cfg=actor-only, strict=True)"
    if "load_optimizer" in load_parameters:
        if "policy" not in config:
            raise RuntimeError(
                "installed RSL-RL uses the policy config schema, but this task agent config "
                "does not; use a compatible training stack or exported TorchScript policy"
            )
        runner.load(str(checkpoint), load_optimizer=False)
        actor_critic = getattr(runner.alg, "policy", getattr(runner.alg, "actor_critic", None))
        if actor_critic is None:
            raise RuntimeError("installed RSL-RL exposes neither policy nor actor_critic")
        if bool(getattr(actor_critic, "is_recurrent", False)):
            raise ValueError("recurrent native policies are not supported")
        actor = runner.get_inference_policy(device=device)
        return actor, actor_critic, "OnPolicyRunner.load(load_optimizer=False)"
    raise RuntimeError("unsupported RSL-RL OnPolicyRunner.load API; refusing checkpoint coercion")


def _get_observation(vec_env, policy_kind: str):
    observation = vec_env.get_observations()
    if isinstance(observation, tuple) and len(observation) == 2:
        observation = observation[0]
    if policy_kind == "torchscript" and hasattr(observation, "keys") and "policy" in observation:
        observation = observation["policy"]
    return observation


def _set_commands(env, command_values, torch):
    command = env.unwrapped.command_manager.get_command("base_velocity")
    target = torch.as_tensor(command_values, dtype=command.dtype, device=command.device)
    if target.ndim == 1:
        target = target.reshape(1, 3).expand(command.shape[0], 3)
    command[:, :3] = target.reshape(command.shape[0], 3)
    if command.shape[1] > 3:
        command[:, 3:] = 0.0
    return command[:, :3].clone()


def _apply_push(env, env_ids, delta: float, direction_idx: int, torch) -> None:
    robot = env.unwrapped.scene["robot"]
    root_vel = robot.data.root_vel_w.clone()
    vectors = ((delta, 0.0), (-delta, 0.0), (0.0, delta), (0.0, -delta))
    dx, dy = vectors[direction_idx % len(vectors)]
    root_vel[env_ids, 0] += dx
    root_vel[env_ids, 1] += dy
    robot.write_root_velocity_to_sim(root_vel[env_ids], env_ids=env_ids)


class _EpisodeStats:
    """Numerical accumulator kept independent of Isaac Lab and PyTorch."""

    def __init__(self) -> None:
        self.steps = 0
        self.tracking_error = 0.0
        self.vx_abs = 0.0
        self.vy_abs = 0.0
        self.yaw_abs = 0.0
        self.xy_sq = 0.0
        self.yaw_sq = 0.0
        self.progress = 0.0
        self.lateral_error_distance = 0.0
        self.stall = 0
        self.stall_candidates = 0
        self.roll_pitch_sq = 0.0
        self.action_delta_sq = 0.0
        self.action_delta_count = 0
        self.previous_action: list[float] | None = None
        self.base_contact_failure: bool | None = None
        self.initial_world_xy: tuple[float, float] | None = None
        self.final_world_xy: tuple[float, float] | None = None

    def add(self, *, vx_error: float, vy_error: float, yaw_error: float,
            actual_vx: float, actual_vy: float, command_vx: float, command_vy: float,
            roll: float, pitch: float, action: list[float], dt: float,
            stall_command_m_s: float, stall_speed_m_s: float,
            base_contact_failure: bool | None, world_xy: tuple[float, float] | None = None,
            episode_start_world_xy: tuple[float, float] | None = None) -> None:
        self.steps += 1
        self.tracking_error += (vx_error * vx_error + vy_error * vy_error + yaw_error * yaw_error) ** 0.5
        self.vx_abs += abs(vx_error)
        self.vy_abs += abs(vy_error)
        self.yaw_abs += abs(yaw_error)
        self.xy_sq += vx_error * vx_error + vy_error * vy_error
        self.yaw_sq += yaw_error * yaw_error
        self.progress += actual_vx * dt
        self.lateral_error_distance += abs(vy_error) * dt
        if (command_vx * command_vx + command_vy * command_vy) ** 0.5 >= stall_command_m_s:
            self.stall_candidates += 1
            if (actual_vx * actual_vx + actual_vy * actual_vy) ** 0.5 < stall_speed_m_s:
                self.stall += 1
        self.roll_pitch_sq += roll * roll + pitch * pitch
        if self.initial_world_xy is None and episode_start_world_xy is not None:
            self.initial_world_xy = episode_start_world_xy
        if world_xy is not None:
            self.final_world_xy = world_xy
        if self.previous_action is not None and action:
            delta_sq = sum((new - old) ** 2 for new, old in zip(action, self.previous_action))
            self.action_delta_sq += delta_sq / len(action)
            self.action_delta_count += 1
        self.previous_action = list(action)
        if base_contact_failure is not None:
            self.base_contact_failure = bool(self.base_contact_failure or base_contact_failure)

    def diagnostics(self) -> dict:
        count = self.steps
        return {
            "mean_tracking_error": self.tracking_error / count,
            "vx_error": self.vx_abs / count,
            "vy_error": self.vy_abs / count,
            "yaw_error": self.yaw_abs / count,
            "xy_rmse": (self.xy_sq / count) ** 0.5,
            "yaw_rmse": (self.yaw_sq / count) ** 0.5,
            "forward_progress_m": self.progress,
            "integrated_body_forward_m": self.progress,
            "world_dx_m": (self.final_world_xy[0] - self.initial_world_xy[0]) if self.final_world_xy and self.initial_world_xy else None,
            "world_dy_m": (self.final_world_xy[1] - self.initial_world_xy[1]) if self.final_world_xy and self.initial_world_xy else None,
            "lateral_drift_m": self.lateral_error_distance,
            "stall_fraction": self.stall / self.stall_candidates if self.stall_candidates else 0.0,
            "roll_pitch_rms": (self.roll_pitch_sq / count) ** 0.5,
            "action_delta_rms": (self.action_delta_sq / self.action_delta_count) ** 0.5 if self.action_delta_count else 0.0,
            "base_contact_failure": self.base_contact_failure,
        }


def _contact_terms(termination_manager):
    names = getattr(termination_manager, "active_terms", ())
    if hasattr(termination_manager, "get_term"):
        return [termination_manager.get_term(name) for name in names
                if "base" in str(name).lower() and "contact" in str(name).lower()]
    terms = getattr(termination_manager, "term_dones", {})
    return [value for name, value in terms.items()
            if "base" in str(name).lower() and "contact" in str(name).lower()]


class _EpisodeCollector:
    def __init__(self, *, args, suite, scenario, case, seed, num_envs, dt,
                 policy_sha256, protocol_id, torch, output_stream):
        self.args = args
        self.suite = suite
        self.scenario = scenario
        self.case = case
        self.seed = seed
        self.num_envs = num_envs
        self.dt = dt
        self.policy_sha256 = policy_sha256
        self.protocol_id = protocol_id
        self.torch = torch
        self.output_stream = output_stream
        self.counts = [0] * num_envs
        self.states = [self._new_state() for _ in range(num_envs)]
        self.first_episode_done = [False] * num_envs
        self.active = [True] * num_envs
        self.action = None
        self.command = None
        self.global_step = 0

    def _new_state(self):
        return _EpisodeStats()

    @property
    def time_window(self) -> bool:
        return self.suite["episode_mode"] == "time_window"

    def set_step(self, action, command, global_step: int, world_xy) -> None:
        self.action = action.detach().clone()
        self.command = command.detach().clone()
        self.global_step = global_step
        self.step_world_xy = world_xy[:, :2].detach().clone()

    def _finish(self, env_id: int, reason: str) -> None:
        state = self.states[env_id]
        count = state.steps
        if count <= 0:
            return
        survived = reason != "terminated"
        diagnostics = state.diagnostics()
        row = {
            "scenario": self.scenario["id"],
            "case": self.case["id"],
            "seed": self.seed,
            "env_id": env_id,
            "episode_id": f"{self.scenario['id']}-{self.case['id']}-s{self.seed}-e{env_id}-n{self.counts[env_id]}",
            "steps": count,
            "duration_s": count * self.dt,
            "end_reason": reason,
            "survived": survived,
            "policy_sha256": self.policy_sha256,
            "protocol_id": self.protocol_id,
        }
        row.update(diagnostics)
        if diagnostics["base_contact_failure"] is None:
            del row["base_contact_failure"]
        self.output_stream.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n")
        self.output_stream.flush()
        self.counts[env_id] += 1
        if not self.time_window:
            self.first_episode_done[env_id] = True
            self.active[env_id] = False
        self.states[env_id] = self._new_state()

    def record_before_reset(self, env, termination_manager, terminated, timeouts) -> None:
        robot = env.unwrapped.scene["robot"]
        data = robot.data
        actual = data.root_lin_vel_b
        angular = data.root_ang_vel_b
        command = self.command
        action = self.action
        root_pos = data.root_pos_w[:, :2]

        projected_gravity = getattr(data, "projected_gravity_b", None)
        if projected_gravity is not None:
            gx, gy, gz = projected_gravity[:, 0], projected_gravity[:, 1], projected_gravity[:, 2]
            roll = self.torch.atan2(gy, -gz)
            pitch = self.torch.atan2(-gx, self.torch.sqrt(gy.square() + gz.square()))
            roll_pitch_sq = roll.square() + pitch.square()
        else:
            roll_pitch_sq = self.torch.zeros(self.num_envs, device=actual.device)

        contact_terms = _contact_terms(termination_manager)
        contact_tensor = (self.torch.stack(contact_terms).any(dim=0) if contact_terms else
                          self.torch.zeros(self.num_envs, dtype=self.torch.bool, device=actual.device))
        combined = self.torch.cat((
            actual[:, :2], angular[:, 2:3], command[:, :3], roll_pitch_sq[:, None],
            action.reshape(self.num_envs, -1), terminated.reshape(self.num_envs, 1).to(actual.dtype),
            timeouts.reshape(self.num_envs, 1).to(actual.dtype), contact_tensor.reshape(self.num_envs, 1).to(actual.dtype),
            root_pos[:, :2], self.step_world_xy[:, :2],
        ), dim=1).detach().to("cpu").tolist()
        active_ids = [index for index, active in enumerate(self.active) if active]
        action_width = action.reshape(self.num_envs, -1).shape[1]
        for env_id in active_ids:
            values = combined[env_id]
            actual_vx, actual_vy, actual_yaw = values[0:3]
            command_vx, command_vy, command_yaw = values[3:6]
            roll_pitch_norm = values[6] ** 0.5
            action_values = values[7:7 + action_width]
            status_offset = 7 + action_width
            is_terminated = bool(values[status_offset])
            is_timeout = bool(values[status_offset + 1])
            contact = bool(values[status_offset + 2]) if contact_terms else None
            world_offset = status_offset + 3
            world_xy = (values[world_offset], values[world_offset + 1])
            episode_start_world_xy = (values[world_offset + 2], values[world_offset + 3])
            dx, dy, dyaw = actual_vx - command_vx, actual_vy - command_vy, actual_yaw - command_yaw
            self.states[env_id].add(
                vx_error=dx,
                vy_error=dy,
                yaw_error=dyaw,
                actual_vx=float(actual_vx),
                actual_vy=float(actual_vy),
                command_vx=float(command_vx),
                command_vy=float(command_vy),
                roll=float(roll_pitch_norm),
                pitch=0.0,
                action=[float(value) for value in action_values],
                dt=self.dt,
                stall_command_m_s=self.suite.get("stall_command_m_s", 0.2),
                stall_speed_m_s=self.suite.get("stall_speed_m_s", 0.1),
                base_contact_failure=contact,
                world_xy=world_xy,
                episode_start_world_xy=episode_start_world_xy,
            )

            if is_terminated:
                self._finish(env_id, "terminated")
            elif is_timeout:
                self._finish(env_id, "timeout")

    def finish_horizon(self) -> None:
        for env_id, active in enumerate(self.active):
            if active:
                self._finish(env_id, "evaluation_end")


def _one_shot_gpu_info() -> str | None:
    executable = shutil.which("nvidia-smi")
    if not executable:
        return None
    try:
        result = subprocess.run(
            [executable, "--query-gpu=name,memory.used,memory.total", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=10, check=True,
        )
        return result.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None


def _set_seed(seed: int, torch) -> None:
    random.seed(seed)
    try:
        import numpy as np
        np.random.seed(seed)
    except ImportError:
        pass
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def _prepare_output(path_value: str) -> Path:
    output = Path(path_value).expanduser().resolve()
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise FileExistsError(f"output must be a new or empty directory: {output}")
    output.mkdir(parents=True, exist_ok=True)
    return output


def _add_exception_note(exc: BaseException, note: str) -> None:
    add_note = getattr(exc, "add_note", None)
    if add_note is not None:
        add_note(note)
    else:
        print(note, file=sys.stderr)


def _record_runtime_failure(*, output: Path, manifest: dict, started: float,
                            exc: BaseException, write_json) -> None:
    manifest["execution_status"] = "INTERRUPTED" if isinstance(exc, KeyboardInterrupt) else "FAILED"
    manifest["complete"] = False
    manifest["error"] = f"{type(exc).__name__}: {exc}"
    manifest["error_traceback"] = "".join(
        traceback.format_exception(type(exc), exc, exc.__traceback__)
    )
    manifest["elapsed_wall_s"] = time.monotonic() - started
    manifest["finished_at"] = _utc_now()
    try:
        manifest["gpu_info_after"] = _one_shot_gpu_info()
    except BaseException as diagnostic_exc:
        _add_exception_note(exc, f"Could not collect post-failure GPU information: {diagnostic_exc!r}")
    try:
        write_json(output / "evaluation_manifest.json", manifest)
    except BaseException as write_exc:
        _add_exception_note(exc, f"Could not persist failure manifest: {write_exc!r}")


def _run_cohort(*, args, task_root, policy_path, policy_kind, task_id, suite,
                scenario, case, seed, output_stream, policy_sha256, protocol_id,
                AppLauncher, versions, torch, app):
    profile = TASKS[args.robot]
    env_cfg_class, agent_cfg_class = _load_task_configs(task_root, args.robot)
    _set_seed(seed, torch)
    env_cfg = _make_env_cfg(env_cfg_class, case=case, duration_s=suite["duration_s"],
                            num_envs=args.num_envs, device=args.device, seed=seed)

    import gymnasium as gym
    from isaacsim.core.utils.stage import create_new_stage
    from isaaclab_rl.rsl_rl import RslRlVecEnvWrapper
    agent_cfg = _prepare_agent_cfg(agent_cfg_class, args.device)
    create_new_stage()
    raw_env = gym.make(task_id, cfg=env_cfg, render_mode=None)
    term_manager = None
    try:
        vec_env = RslRlVecEnvWrapper(raw_env, clip_actions=getattr(agent_cfg, "clip_actions", None))
        if policy_kind == "rsl_rl_checkpoint":
            from rsl_rl.runners import OnPolicyRunner
            runner = OnPolicyRunner(vec_env, agent_cfg.to_dict(), log_dir=None, device=args.device)
            actor, actor_critic, _ = _load_native_runner(runner, agent_cfg, policy_path, args.device)
            if hasattr(actor, "eval"):
                actor.eval()

            def reset_actor(done_mask):
                if hasattr(actor, "reset"):
                    actor.reset(done_mask)
                elif hasattr(actor_critic, "reset"):
                    actor_critic.reset(done_mask)
        else:
            actor = torch.jit.load(str(policy_path), map_location=args.device)
            actor.eval()

            def reset_actor(done_mask):
                if hasattr(actor, "reset"):
                    actor.reset(done_mask)

        raw_env.reset()
        env = vec_env
        unwrapped = env.unwrapped
        dt = float(getattr(unwrapped, "step_dt", env_cfg.sim.dt * env_cfg.decimation))
        if dt <= 0:
            raise ValueError(f"invalid environment step duration: {dt}")
        horizon_steps = max(1, round(suite["duration_s"] / dt))
        period_steps = max(1, round(suite["command_period_s"] / dt))
        collector = _EpisodeCollector(
            args=args, suite=suite, scenario=scenario, case=case, seed=seed,
            num_envs=args.num_envs, dt=dt, policy_sha256=policy_sha256,
            protocol_id=protocol_id, torch=torch, output_stream=output_stream,
        )
        term_manager = unwrapped.termination_manager
        original_compute = term_manager.compute

        def compute_and_collect(*call_args, **call_kwargs):
            result = original_compute(*call_args, **call_kwargs)
            terminated = getattr(term_manager, "terminated", None)
            timeouts = getattr(term_manager, "time_outs", None)
            if terminated is None or timeouts is None:
                raise RuntimeError("termination manager does not expose terminated/time_outs")
            collector.record_before_reset(unwrapped, term_manager, terminated, timeouts)
            done_mask = terminated | timeouts
            reset_actor(done_mask)
            return result

        term_manager.compute = compute_and_collect
        push_delta = case.get("push_delta")
        push_steps = {round(t / dt): i for i, t in enumerate((4.0, 8.0, 12.0, 16.0))}
        for global_step in range(horizon_steps):
            if not app.is_running():
                raise RuntimeError("Isaac Sim application stopped before the evaluation horizon")
            if not collector.time_window and all(collector.first_episode_done):
                break
            if push_delta is not None and global_step in push_steps:
                active_ids = [i for i, active in enumerate(collector.active) if active]
                if active_ids:
                    _apply_push(unwrapped, torch.as_tensor(active_ids, device=args.device, dtype=torch.long),
                                float(push_delta), push_steps[global_step], torch)
            command_values = [
                case["commands"][min(collector.states[index].steps // period_steps,
                                      len(case["commands"]) - 1)]
                if active else [0.0, 0.0, 0.0]
                for index, active in enumerate(collector.active)
            ]
            commands = _set_commands(unwrapped, command_values, torch)
            observation = _get_observation(vec_env, policy_kind)
            with torch.inference_mode():
                actions = actor(observation)
            if not torch.isfinite(actions).all():
                raise FloatingPointError("policy produced non-finite actions")
            collector.set_step(actions, commands, global_step,
                               unwrapped.scene["robot"].data.root_pos_w[:, :2])
            vec_env.step(actions)
        collector.finish_horizon()
        return {"dt_s": dt, "horizon_steps": horizon_steps}
    finally:
        if term_manager is not None:
            term_manager.compute = original_compute
        raw_env.close()


def _run(args, simulation_app, AppLauncher) -> int:
    from eval_core import file_sha256, load_jsonl, load_suite, protocol_hash, validate_dataset, write_json
    import torch

    _require_personal_mode(args)
    if args.num_envs < 1:
        raise ValueError("--num-envs must be positive")
    if args.duration is not None and args.duration <= 0:
        raise ValueError("--duration must be positive")
    os.environ.pop("NCRC_PLAY_PUSH", None)
    task_root, policy_path, policy_kind, task_id = _resolve_inputs(args)
    seeds = _parse_seeds(args.seeds, args.smoke)
    suite = load_suite(args.robot, args.suite)
    if args.smoke:
        suite["duration_s"] = 2.0
    elif args.duration is not None:
        suite["duration_s"] = float(args.duration)
    scenarios = suite["scenarios"][:1] if args.smoke else suite["scenarios"]
    if args.smoke:
        scenarios = [{**scenarios[0], "cases": scenarios[0]["cases"][:1]}]
    output = _prepare_output(args.output)
    episodes_path = output / "episodes.jsonl"
    policy_sha256 = file_sha256(policy_path)
    versions = _runtime_versions(AppLauncher, args.isaaclab_root)
    source_fingerprints = _source_fingerprints(task_root, args.robot, file_sha256)
    profile = TASKS[args.robot]
    env_cfg_class, agent_cfg_class = _load_task_configs(task_root, args.robot)
    agent_cfg = _prepare_agent_cfg(agent_cfg_class, args.device)
    architecture = _agent_summary(agent_cfg)
    resolved_agent_config = _normalize_config(agent_cfg.to_dict())
    agent_cfg_fingerprint = protocol_hash(resolved_agent_config)
    applied_env_fingerprints = {}
    resolved_env_configs = {}
    for scenario in scenarios:
        for case in scenario["cases"]:
            for seed in seeds:
                config = _make_env_cfg(
                    env_cfg_class, case=case, duration_s=suite["duration_s"],
                    num_envs=args.num_envs, device=args.device, seed=seed,
                )
                key = f"{scenario['id']}/{case['id']}/{seed}"
                resolved_env_configs[key] = _normalize_config(config.to_dict())
                applied_env_fingerprints[key] = protocol_hash(resolved_env_configs[key])
    write_json(output / "resolved_configs.json", {
        "agent": resolved_agent_config, "environment_by_case_seed": resolved_env_configs})
    protocol = {
        "suite": suite,
        "robot": args.robot,
        "task_id": task_id,
        "num_envs": args.num_envs,
        "seeds": seeds,
        "device": args.device,
        "camera_enabled": False,
        "render_mode": None,
        "actor_mode": "deterministic_inference",
        "collector_version": COLLECTOR_VERSION,
        "versions": versions,
        "source_fingerprints": source_fingerprints,
        "agent_config_fingerprint": agent_cfg_fingerprint,
        "applied_environment_config_fingerprints": applied_env_fingerprints,
        "command_schedule": "per_episode_step_clock_without_rng_v1",
        "disturbance_schedule": "fixed_xy_velocity_deltas_at_4_8_12_16s_v1",
    }
    protocol_id = protocol_hash(protocol)
    policy_info = {
        "path": str(policy_path),
        "sha256": policy_sha256,
        "kind": policy_kind,
        "source_run_id": args.source_run_id,
        "preset": args.preset,
    }
    manifest = {
        "schema": "se3c-evaluation-v1",
        "robot": args.robot,
        "suite": suite,
        "protocol": protocol,
        "protocol_id": protocol_id,
        "policy": policy_info,
        "evaluation_environment": "PERSONAL",
        "task_root": str(task_root),
        "source_fingerprints": source_fingerprints,
        "task_config": {
            "task_id": task_id,
            "environment_config_class": env_cfg_class.__name__,
            "agent_config_class": agent_cfg_class.__name__,
            "observation_architecture": architecture,
        },
        "smoke": bool(args.smoke),
        "complete": False,
        "execution_status": "RUNNING",
        "started_at": _utc_now(),
        "gpu_info_before": _one_shot_gpu_info(),
    }
    started = time.monotonic()
    write_json(output / "evaluation_manifest.json", manifest)
    try:
        if torch.cuda.is_available() and str(args.device).startswith("cuda"):
            device_index = torch.device(args.device).index or 0
            torch.cuda.init()
            torch.cuda.reset_peak_memory_stats(device_index)
        if str(task_root) not in sys.path:
            sys.path.insert(0, str(task_root))
        importlib.import_module(profile["package"])
        with episodes_path.open("x", encoding="utf-8") as output_stream:
            for scenario in scenarios:
                for case in scenario["cases"]:
                    for seed in seeds:
                        _run_cohort(
                            args=args, task_root=task_root, policy_path=policy_path,
                            policy_kind=policy_kind, task_id=task_id, suite=suite,
                            scenario=scenario, case=case, seed=seed,
                            output_stream=output_stream, policy_sha256=policy_sha256,
                            protocol_id=protocol_id, AppLauncher=AppLauncher,
                            versions=versions, torch=torch, app=simulation_app,
                        )
        manifest["execution_status"] = "COMPLETE"
        manifest["complete"] = False
        manifest["elapsed_wall_s"] = time.monotonic() - started
        manifest["finished_at"] = _utc_now()
        manifest["gpu_info_after"] = _one_shot_gpu_info()
        if torch.cuda.is_available():
            try:
                device_index = torch.device(args.device).index or 0
                properties = torch.cuda.get_device_properties(device_index)
                manifest["cuda_memory"] = {
                    "device": properties.name,
                    "peak_allocated_bytes": int(torch.cuda.max_memory_allocated(device_index)),
                    "total_bytes": int(properties.total_memory),
                }
            except Exception as exc:
                manifest["cuda_memory"] = {"error": f"{type(exc).__name__}: {exc}"}
        if args.smoke:
            manifest["smoke"] = True
        else:
            candidate = {**manifest, "complete": True}
            validate_dataset(load_jsonl(episodes_path), candidate)
            manifest["complete"] = True
        write_json(output / "evaluation_manifest.json", manifest)
        print(json.dumps({"execution_status": manifest["execution_status"],
                          "complete": manifest["complete"], "output": str(output),
                          "protocol_id": protocol_id}, ensure_ascii=False))
        return 0
    except BaseException as exc:
        try:
            _record_runtime_failure(output=output, manifest=manifest, started=started,
                                    exc=exc, write_json=write_json)
        except BaseException as record_exc:
            _add_exception_note(exc, f"Could not record runtime failure: {record_exc!r}")
        raise


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    _require_personal_mode(args)
    from isaaclab.app import AppLauncher

    app_launcher = AppLauncher(args)
    simulation_app = app_launcher.app
    try:
        result = _run(args, simulation_app, AppLauncher)
    except BaseException as run_exc:
        traceback.print_exc()
        sys.stderr.flush()
        try:
            simulation_app.close()
        except BaseException as close_exc:
            _add_exception_note(run_exc, f"simulation_app.close() also failed: {close_exc!r}")
        raise
    else:
        simulation_app.close()
        return result


if __name__ == "__main__":
    raise SystemExit(main())
