# H1 action-rate restoration · OFFICIAL resume +2K

Experiment: `exp-h1-action-rate-restoration`. Question: after an ACTRATE-0001 policy was trained with the relaxed action-rate penalty, what is the result of restoring the `h1-submit-2` action-rate weight for one +2K resume step?

- Run ID: `20261014-142200-h1-actrate-return2700-2k`; OFFICIAL / H1 / train / resume.
- Requested 2,000 additional iterations from iteration 2700; console reaches 4699/4700. Seed 42, 4096 environments, exit 0, training/evidence status COMPLETED/PASS; official finalize and backup succeeded.
- Native run: `/workspace/training/humanoid/logs/rsl_rl/humanoid/2026-10-14_23-22-08`.
- Archived effective rewards: `track_lin_vel_xy_exp=0.5`, `track_ang_vel_z_exp=0.5`, `feet_air_time=0.2`, `termination_penalty=-50`, `flat_orientation_l2=-1.5`, `ang_vel_xy_l2=-0.05`, `joint_deviation_hip=-0.2`, `joint_deviation_torso=-0.1`, `action_rate_l2=-0.0005`. Compared with the ACTRATE-0001 `model_2700` parent, the action-rate weight returns from `-0.0001` to `-0.0005`; the other eight archived rewards match.
- Parent checkpoint SHA-256 `e54d3389e20ea913968ef8d3edbea5004368ff225fa6b94f73fcd91cf93ca7ae` matches the preserved OFFICIAL ACTRATE-0001 fresh3K `model_2700.pt`. The Run's raw metadata still records `source_checkpoint_origin=user_imported_checkpoint`, `source_evidence_run_id=null`, `parent_run_id=null`, `source_run_mode=unknown`, and `source_provenance_verified=false`; the external SHA match does not rewrite those fields.
- This is the reward-change branch paired with unchanged-reward control Run `20261014-111135-h1-actrate-0001-unchanged-cont2k` from the same checkpoint SHA. No video or policy evaluation is included; behavior assessment/adoption remains pending, and no score or submission is claimed.
- Received wrapper: `20261014-142200-h1-actrate-return2700-2k-download.tar.gz`, 286,147,158 bytes, SHA-256 `18ae2c05fb991fbcc9871f88001712165246c47e6a457df0d15e311cb01c488a`.

The received wrapper is preserved unchanged. Training completion and validation do not establish policy quality or adoption.
