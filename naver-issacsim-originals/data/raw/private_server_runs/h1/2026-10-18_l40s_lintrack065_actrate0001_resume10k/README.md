# H1 LINTRACK-065 + ACTRATE-0001 resume toward 10K — PERSONAL run evidence receipt

Actual Run ID: `20261018-090630-h1-top08-same-reward-to10k`.

The received run archive records `mode=personal`, `status=completed`, `training_status=completed`, `exit_code=0`, `official_finalize_status=completed` (local finalizer status only), `official_backup_status=skipped_no_config`, and `evidence_validation=PASS`. It resumed from imported `model_4650.pt` (stored iteration 4650), requested 5,350 iterations, and reached final native `model_9999.pt`. Seed 42, 4,096 environments. Effective reward: `h1-submit-2 + track_lin_vel_xy_exp=0.65 + action_rate_l2=-0.0001`; `termination_penalty=-50`.

Parent checkpoint SHA-256: `ce7ad58657f3dd744e7cf2b7531f3d7d455773dfc6fb135f39d8a55aa49dea70`. Raw metadata classifies it as `user_imported_checkpoint`, with null source Run ID and `source_provenance_verified=false`; this parent lineage is not verified.

Received outer download archive: `20261018-090630-h1-top08-same-reward-to10k-download.tar.gz`, 739,533,489 bytes, SHA-256 `416b10bd9c921d3b0f58df9332a3f809c104409b25c5dd6b079f801d284406a8`. A byte-preserving copy is in `evidence_archives/`; the Downloads original remains untouched. No `checkpoint_index.json` is present in the embedded archive. `SHA256SUMS` identifies final `checkpoints/model_9999.pt` as 7,151,477 bytes, SHA-256 `852c95fa0fcfabec456572541c24dad68385084ce480aa09b8422597b704929b`, matching the separate PERSONAL A4000 evaluation manifest.

Verified training Release: [private-h1-20261018-exp-h1-action-first-planar-tracking-switch-resume10k](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261018-exp-h1-action-first-planar-tracking-switch-resume10k). Remote asset size and digest match the recorded outer archive.
