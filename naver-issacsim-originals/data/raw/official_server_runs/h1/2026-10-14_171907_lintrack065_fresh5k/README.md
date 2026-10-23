# [학습] H1 LINTRACK-065 · OFFICIAL fresh 5K

- Experiment: `exp-h1-planar-tracking-weight`; baseline `h1-submit-2`; final override `h1-submit-2 + lin=0.65`.
- Actual training Run: `20261014-081901-h1-lintrack-065-fresh5k`; OFFICIAL / H1 / train / fresh, no parent checkpoint or resume. Seed 42, 4096 environments, requested 5000 iterations, COMPLETED / exit 0 / evidence validation PASS.
- Native Run: `/workspace/training/humanoid/logs/rsl_rl/humanoid/2026-10-14_17-19-07`. Full resolved `env.yaml`, `agent.yaml`, reward source and source identity are preserved inside the original nested evidence archive.
- Verified command: `/workspace/IsaacLab/isaaclab.sh -p /workspace/training/humanoid/train.py --task Humanoid-v0 --max_iterations 5000 --num_envs 4096 --seed 42 --headless agent.save_interval=50`.
- Effective reward values in the archived source: `track_lin_vel_xy_exp=0.65`, `track_ang_vel_z_exp=0.5`, `feet_air_time=0.2`, `termination_penalty=-50`, `flat_orientation_l2=-1.5`, `ang_vel_xy_l2=-0.05`, `joint_deviation_hip=-0.2`, `joint_deviation_torso=-0.1`, `action_rate_l2=-0.0005`. The full native configuration remains authoritative.
- Parent/resume lineage: none (fresh). The source identity snapshot reports unchanged before/after; official training source commit is not established by this archive.
- Evidence reports 100 organizer checkpoints copied and indexed, official finalize and backup completed. No policy evaluation, adoption decision, submission, or official score is recorded here.
- Received wrapper: `20261014-081901-h1-lintrack-065-fresh5k-download.tar.gz`, 685,424,409 bytes, SHA-256 `61142daf19b260438360e7b517fb35a9a826f5d57196060d3eb4fce72a1c0bac`. Its embedded nested evidence archive SHA-256 `e64da2230365bef6e07842bf81d206a0d2e3427d6dd378e1d8dc08000b9346f1` matches the embedded sidecar. Preserve the received wrapper and nested evidence unchanged.
- Release: https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261014-exp-h1-planar-tracking-weight-fresh5k

The training Run is complete. Behavior assessment and any adoption decision remain pending; this record does not claim an official score or submission.
