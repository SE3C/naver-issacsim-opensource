# H1 ACTRATE-0001 unchanged continuation · OFFICIAL resume +2K

Experiment: `exp-h1-action-rate-relaxation`. This is an unchanged-reward continuation control from the ACTRATE-0001 `model_2700` checkpoint; it is not a reward-change Run.

- Run ID: `20261014-111135-h1-actrate-0001-unchanged-cont2k`; OFFICIAL / H1 / train / resume.
- Requested 2,000 additional iterations; resumed at iteration 2700 and reached 4699/4700. Seed 42, 4096 environments, exit 0, training/evidence status COMPLETED/PASS; official finalize and backup succeeded.
- Native run: `/workspace/training/humanoid/logs/rsl_rl/humanoid/2026-10-14_20-11-42`.
- Effective reward values: `track_lin_vel_xy_exp=0.5`, `track_ang_vel_z_exp=0.5`, `feet_air_time=0.2`, `termination_penalty=-50`, `flat_orientation_l2=-1.5`, `ang_vel_xy_l2=-0.05`, `joint_deviation_hip=-0.2`, `joint_deviation_torso=-0.1`, `action_rate_l2=-0.0001`. These match the preserved ACTRATE-0001 fresh3K parent reward values.
- Resume checkpoint SHA-256 `e54d3389e20ea913968ef8d3edbea5004368ff225fa6b94f73fcd91cf93ca7ae` matches the preserved OFFICIAL ACTRATE-0001 fresh3K `model_2700.pt`. The new Run's own metadata nevertheless records `source_checkpoint_origin=user_imported_checkpoint`, `source_evidence_run_id=null`, `parent_run_id=null`, `source_run_mode=unknown`, and `source_provenance_verified=false`; this external hash match does not rewrite those fields.
- The evidence reports 41 organizer checkpoints copied and 42 checkpoint-index entries. No policy evaluation, submission, or official score is included; behavioral assessment remains pending.
- Received wrapper: `20261014-111135-h1-actrate-0001-unchanged-cont2k-download.tar.gz`, 292,815,996 bytes, SHA-256 `b492f6659d622f11c17e7f3d5f4efd5a761a59947ee24c96bbf325fd79f6fa61`.

The received wrapper is preserved unchanged. Training completion and validation do not establish policy quality or adoption.
