# H1 ACTRATE-001 resume toward 10K — OFFICIAL run evidence receipt

Actual Run ID: `20261018-092452-h1-top07-same-reward-to10k`.

The received run archive records `mode=official`, `status=completed`, `training_status=completed`, `exit_code=0`, `official_finalize_status=completed`, `official_backup_status=success`, and `evidence_validation=PASS`. It resumed from the imported `model_2950.pt` (stored iteration 2950), requested 7,050 iterations, and finished with saved keeper `model_9950.pt`. Seed 42, 4,096 environments. Effective reward: `h1-submit-2 + action_rate_l2=-0.001`; other recorded weights include `track_lin_vel_xy_exp=0.5` and `termination_penalty=-50`.

Parent checkpoint SHA-256: `8914b6b48e74a6463808f629648f87900efdb853e5253e142e99c738adb2d085`. Raw metadata classifies it as `user_imported_checkpoint`, with null source Run ID and `source_provenance_verified=false`; this parent lineage is not verified.

Received outer download archive: `20261018-092452-h1-top07-same-reward-to10k-download.tar.gz`, 958,182,392 bytes, SHA-256 `72449e4ba3b0cf5bc3b9d1278b243e7e273f982513198fe202e544a8598c141b`. A byte-preserving copy is in `evidence_archives/`; the Downloads original remains untouched. The embedded run archive's recorded SHA-256 sidecar is `25166b2d8f5a3f3e4b0b61197602b648e1f2a47c5226baf7c72c54d97dd2f483`; its size was not independently captured in this receipt.

The embedded checkpoint index identifies keeper `model_9950.pt` at `/workspace/training/humanoid/backup_log/2026-10-18_18-24-58/model_9950.pt`, origin `organizer_keeper_backup`, size 7,151,477 bytes, SHA-256 `642255c41cf09dac6a9401985f70cce0177c41cd87b85aa085a5f35bbbdf09c6`. This matches the separate PERSONAL A4000 evaluation manifest policy SHA and the archive `SHA256SUMS` entry.

Verified training Release: [official-h1-20261018-exp-h1-action-rate-smoothing-resume10k](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261018-exp-h1-action-rate-smoothing-resume10k). Remote asset size and digest match the recorded outer archive.
