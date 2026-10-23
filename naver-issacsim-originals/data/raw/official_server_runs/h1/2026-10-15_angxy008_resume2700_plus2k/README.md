# [학습] H1 angxy=-0.08 + action=-0.0001 · OFFICIAL resume2700 +2K

Experiment: `exp-h1-action-first-body-rate-switch`; Run `20261015-143107-h1-actrate0001-angxy008-from2700-plus2k`. Preset-relative reward override: `h1-submit-2 + ang_vel_xy_l2=-0.08 + action_rate_l2=-0.0001`. Relative to the imported ACTRATE parent, only angxy changes -0.05→-0.08; lin=.5, ang=.5, feet=.2, termination=-50, orientation=-1.5, hip=-.2, torso=-.1 remain unchanged. Complete resolved configuration is preserved inside the archive under native_run/params/{env,agent}.yaml and source/.

OFFICIAL training COMPLETED, exit0, validation PASS; resume from iteration2700, requested +2000, seed42/4096env, console endpoint4699/4700. Native run: `/workspace/training/humanoid/logs/rsl_rl/humanoid/2026-10-15_23-31-13`. Finalize and automatic backup succeeded; 40 organizer checkpoints copied. No new training or evaluation was launched during this intake.

Parent checkpoint SHA `e54d3389e20ea913968ef8d3edbea5004368ff225fa6b94f73fcd91cf93ca7ae` matches the preserved OFFICIAL ACTRATE-0001 fresh3K model_2700 from Run `20261009-142350-h1-actrate-0001-fresh3k`. Raw metadata retains imported checkpoint origin, null parent/evidence IDs, unknown source Run mode and source_provenance_verified=false. This separate SHA linkage does not rewrite raw provenance.

Latest indexed organizer keeper: model_4650 SHA `c272b13b5d3702c8a84c1470b597526efe2214d0ee38f34f65918c5f912a335f`, source `/workspace/training/humanoid/backup_log/2026-10-15_23-31-13/model_4650.pt`; its preserved bytes match the index. It is not the exact console endpoint4699. Automatic best model_3400 SHA `7e5c36424c91f1f449cd19f14eb5b612458248987ad5aeaf5541d64542568db8` is distinct.

Received archive: `20261015-143107-h1-actrate0001-angxy008-from2700-plus2k-download.tar.gz`; 286196248 bytes; SHA256 `2146f7535d23a74bf14201185d127756ba1e4fa1c4bbe6cdd47a846eb8573e3e`. Original bytes are preserved in evidence_archives/; adjacent .sha256 is the received archive checksum. metadata.json, validation.json and checkpoint_index.json are unchanged extracted reference copies. Console/config/TensorBoard/checkpoints remain in the original nested archive.

Policy quality/evaluation: **PENDING / HOLD**, not a new submission or official score. Publish repository: SE3C/naver-issacsim-originals; annotated publication tag `official-h1-20261015-exp-h1-action-first-body-rate-switch-angxy008-resume2700-plus2k` identifies this preservation record, not the actual training source revision.
