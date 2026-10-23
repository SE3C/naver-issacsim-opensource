# H1 LINTRACK-075 + ACTRATE-0001 same-reward continuation to 10K — OFFICIAL

- Actual training Run: `20261018-105744-h1-top09-same-reward-to10k` (selection alias TOP09).
- Mode/status: OFFICIAL; COMPLETED, exit 0, official finalize complete, official backup success, evidence validation PASS.
- Command: `Humanoid-v0`, resume from iteration 2950 with requested `--max_iterations 7050`, seed 42, 4096 environments, save interval 50. Final saved checkpoint is iteration 9950.
- Effective reward config from archived `source/humanoid_rewards.py` (SHA-256 `15267130f596a2a922e60ff0f6d8b4566ee240f3dc49de4897ec7141548262cc`) and `source/resolved_env.yaml`: `h1-submit-2 + track_lin_vel_xy_exp=0.75 + action_rate_l2=-0.0001`; remaining weights are track_ang_vel_z_exp=0.5, feet_air_time=0.2, termination_penalty=-50, flat_orientation_l2=-1.5, ang_vel_xy_l2=-0.05, joint_deviation_hip=-0.2, joint_deviation_torso=-0.1.
- Resume checkpoint SHA-256: `952330c4d95c61e5104e446fdf947a94c38ad7feac6e4806b8164d709826fba3`. It matches the separately preserved OFFICIAL `model_2950.pt` from `2026-10-17_140610_lin075_action0001_fresh3k`. The raw Run metadata remains unchanged: `parent_run_id=null`, `source_run_mode=unknown`, and `source_provenance_verified=false`; this SHA join is recorded separately and does not change those raw claims.
- Final keeper `model_9950.pt` SHA-256 `086cac9dbac3261dc44d8d079dcbdce658cbb28e34da7bbb7c309589c48d4d0e`, recorded in `checkpoint_index.json` and matched against the archived keeper bytes.
- Source Git commit is null. Archived `source/identity.json` records per-file identities and no source changes during the run.
- Original download wrapper is preserved unchanged at `evidence_archives/20261018-105744-h1-top09-same-reward-to10k-download.tar.gz`, 959,601,708 bytes, SHA-256 `ba9334e5e4509a318562fb4ca31ae712392979b2e3ac9b6e99c79efd7a3fe995`. Its embedded evidence archive is retained inside the wrapper; extracted run metadata, checkpoint index, validation, checksum manifest, reward source, source identity, and resolved environment are byte-preserved here for inspection.
- Release title: `[학습] H1 LINTRACK-075 + ACTRATE-0001 · OFFICIAL continuation to 10K`.
- [Training Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261018-exp-h1-action-planar-tracking-fresh-interaction-top09-resume10k); its annotated tag targets this preservation record, not an unavailable task-source commit.

Training completion is not a policy decision. Evaluation and analysis remain separate; no score, submission, or adoption result is asserted here.
