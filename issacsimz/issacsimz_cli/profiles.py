from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TrainingProfile:
    robot: str
    task: str
    root_env: str
    default_root: Path
    native_run_root: Path
    reward_file: str
    task_package: str


PROFILES = {
    "h1": TrainingProfile(
        robot="h1",
        task="Humanoid-v0",
        root_env="ISSACSIMZ_H1_ROOT",
        default_root=Path("/workspace/training/humanoid"),
        native_run_root=Path("logs/rsl_rl/humanoid"),
        reward_file="humanoid_rewards.py",
        task_package="h1_task",
    ),
    "go2": TrainingProfile(
        robot="go2",
        task="Quadruped-v0",
        root_env="ISSACSIMZ_GO2_ROOT",
        default_root=Path("/workspace/training/quadruped"),
        native_run_root=Path("logs/rsl_rl/quadruped"),
        reward_file="quadruped_rewards.py",
        task_package="go2_task",
    ),
}

OFFICIAL_ISAACLAB_ROOT = Path("/workspace/IsaacLab")


def _official_mode() -> bool:
    return os.environ.get("ISSACSIMZ_MODE", "").strip().lower() == "official"


def resolve_task_root(robot: str, explicit: str | None = None) -> Path:
    profile = PROFILES[robot]
    if _official_mode():
        expected = profile.default_root.resolve()
        configured = os.environ.get(profile.root_env)
        if configured and Path(configured).expanduser().resolve() != expected:
            raise ValueError(f"official {profile.root_env} override is disabled; expected {expected}")
        if explicit is not None and Path(explicit).expanduser().resolve() != expected:
            raise ValueError(f"official --task-root override is disabled; expected {expected}")
        if (expected / "train.py").is_file():
            return expected
        raise FileNotFoundError(f"official task root is invalid; expected {expected / 'train.py'}")
    if explicit is not None:
        root = Path(explicit).expanduser().resolve()
        if (root / "train.py").is_file():
            return root
        raise FileNotFoundError(f"explicit --task-root is invalid; expected {root / 'train.py'}")

    candidates = [os.environ.get(profile.root_env), str(profile.default_root)]
    for value in candidates:
        if not value:
            continue
        root = Path(value).expanduser().resolve()
        if (root / "train.py").is_file():
            return root
    raise FileNotFoundError(
        f"{robot} task root not found; set --task-root or {profile.root_env}. "
        f"Expected {profile.default_root}/train.py"
    )


def resolve_isaaclab_launcher(explicit: str | None = None) -> Path:
    launcher_name = "isaaclab.bat" if os.name == "nt" else "isaaclab.sh"
    if _official_mode():
        expected_root = OFFICIAL_ISAACLAB_ROOT.resolve()
        configured = os.environ.get("ISSACSIMZ_ISAACLAB_ROOT")
        if configured and Path(configured).expanduser().resolve() != expected_root:
            raise ValueError(f"official ISSACSIMZ_ISAACLAB_ROOT override is disabled; expected {expected_root}")
        if explicit is not None and Path(explicit).expanduser().resolve() != expected_root:
            raise ValueError(f"official --isaaclab-root override is disabled; expected {expected_root}")
        launcher = expected_root / launcher_name
        if launcher.is_file():
            return launcher
        raise FileNotFoundError(f"official Isaac Lab launcher is invalid; expected {launcher}")
    if explicit is not None:
        root = Path(explicit).expanduser().resolve()
        launcher = root / launcher_name
        if launcher.is_file():
            return launcher
        raise FileNotFoundError(f"explicit --isaaclab-root is invalid; expected {launcher}")

    candidates = [
        os.environ.get("ISSACSIMZ_ISAACLAB_ROOT"),
        os.environ.get("ISAACLAB_PATH"),
        "/workspace/IsaacLab",
        str(Path.home() / "IsaacLab"),
    ]
    for value in candidates:
        if not value:
            continue
        root = Path(value).expanduser().resolve()
        launcher = root / launcher_name
        if launcher.is_file():
            return launcher
    raise FileNotFoundError("Isaac Lab launcher not found; set --isaaclab-root or ISSACSIMZ_ISAACLAB_ROOT")
