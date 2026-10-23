# exp-h1-rotation-priority-tracking

- Robot: H1
- Experiment question: Does a rotation-prioritized fresh configuration (`ang=0.75`, `lin=0.55`) with intermediate action regularization produce a useful yaw/locomotion balance across forward, lateral, rough, and stability conditions?
- Preset reference: frozen `h1-submit-2`.
- Final overrides, verified from archived native reward source and resolved `env.yaml`: `track_lin_vel_xy_exp=0.55`, `track_ang_vel_z_exp=0.75`, `action_rate_l2=-0.0003`. Feet air time `0.2`, termination `-50`, orientation `-1.5`, roll/pitch angular velocity `-0.05`, hip `-0.2`, torso `-0.1` remain at the source values.
- Training status: **OFFICIAL fresh3K COMPLETED / exit 0 / validation PASS**.
- Policy status: no separate PERSONAL behavior evaluation or analysis was recorded in this intake. No promotion decision or official score.

## Actual Run

Run `20261017-145042-h1-lintrack-055-angtrack-075-actrate-0003-fresh3` used no parent, resume checkpoint, or imported source checkpoint. Command evidence records `Humanoid-v0`, 3,000 requested iterations, 4,096 environments, seed 42, headless execution, and `save_interval=50`. Metadata records OFFICIAL mode, normal completion, exit 0, completed finalize, successful official backup, 60 keeper checkpoints, and no collection errors. All nine checks in `validation.json` are PASS.

Native run path: `/workspace/training/humanoid/logs/rsl_rl/humanoid/2026-10-17_23-50-48`. Run time was 2026-10-17 14:50:42–15:27:49 UTC. The archived policy summary `report.html` displays iter 2700 / total 3000; it is not the latest keeper or a statement of the final console iteration. The report's `model_best.pt` SHA `6849363a2061a3c48bb45577195da128a290d6a8abc0480368a274cc0e3cae5d` matches indexed `model_2700.pt`. The latest numbered keeper is `model_2950.pt`, SHA-256 `ca40a6b1bc10d1d23af9f7e0acae74229fbd91c45998055a59cb22205163519c`.

## Evidence and lineage

- Canonical Originals directory: `SE3C/naver-issacsim-originals:data/raw/official_server_runs/h1/2026-10-17_145042_lin055_ang075_action0003_fresh3k/`.
- Original wrapper: `20261017-145042-h1-lintrack-055-angtrack-075-actrate-0003-fresh3-download.tar.gz`, SHA-256 `e84310aeb92e482dee90e7c67b1483855451ed8eb402fb732bacb728ca73ad8a`.
- Resolved sources: `native_run/params/env.yaml` SHA `5731ee6426e76fda3235388704c78adafb4a4a74ac2040e29f5f332819df51ec`; `native_run/params/agent.yaml` SHA `27308e8a2288335081dc26a5755fcd5a052360be8b33cb3203fddba0bc877aff`; `source/humanoid_rewards.py` SHA `6345bb13454befb7e61797bc0eccb0552189dc7bee3e4150632bc6b66eb075e5`. Exact files and hashes are listed in the preserved run `SHA256SUMS`.
- [Published training Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261017-exp-h1-rotation-priority-tracking-fresh3k): original archive and checksum remote sizes/digests verified; canonical preservation commit `0eb5dea`.

This is a completed 3K training Run, not an evaluation result. It does not establish a reward-specific causal effect, 10K competitiveness, an official score, or a submission decision.
