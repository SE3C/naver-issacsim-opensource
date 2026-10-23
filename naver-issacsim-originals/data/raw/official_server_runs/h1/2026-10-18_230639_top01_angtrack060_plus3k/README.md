# H1 TOP01 ANG070 +3K — OFFICIAL training archive

Run: `20261018-140635-h1-top01-angtrack060-plus3k`; native run directory `2026-10-18_23-06-39`. The run completed with exit code 0 and archive validation PASS. The original downloaded outer wrapper is preserved without modifying its bytes.

## Archive identity and validation

- Original filename: `20261018-140635-h1-top01-angtrack060-plus3k-download.tar.gz`
- Size: 419,806,526 bytes
- SHA-256: `8a0c8c8e36ab34ed25357e70a7963d5613a72d6a9f5802f98113c64e0b0c6b31`
- Inner archive: `20261018-140635-h1-top01-angtrack060-plus3k.tar.gz`, 413,264,621 bytes, SHA-256 `c06254737f62f6f60f0df13ac51936e5888be418e79c68fdee9a5f24ddc57924`; matches its included `.sha256` sidecar.
- Inner `SHA256SUMS`: 82/82 entries PASS.
- Run validation: `overall=PASS`; exit=0, official backup success, official finalize completed.

## Training lineage and checkpoints

The archived metadata records a resume from `/workspace/model_9950.pt`, SHA-256 `6e03f421b422c442ee85d449c708b3bf340d39e17c55de786276b9fd091847f3`, with 3,000 requested additional iterations. That SHA matches the keeper recorded for TOP01 parent Run `20261018-021823-h1-top01-same-reward-to10k`.

The raw run metadata remains as received: `parent_run_id=null`, `source_provenance_verified=false`, origin `user_imported_checkpoint`. The separate SHA match does not rewrite the archive's lineage fields.

The automatic-best policy is `model_11650.pt` (stored iteration 11,650; SHA-256 `3d978261fb1b2c3c2cfbd48f8957972e81a54d6541e96d252a7d6a3344b3a381`). Latest preserved checkpoint is `model_12900.pt` (iteration 12,900; SHA-256 `3f78944c81ff09cba97586deaaf2c6874b4e39bff1fde945628af6d314451b7a`). These are distinct; model_12900 is not the selected-best policy.

Resolved archived rewards: `track_lin_vel_xy_exp=0.65`, `track_ang_vel_z_exp=0.7`, `action_rate_l2=-0.0003`, `termination_penalty=-50.0`, `feet_air_time=0.2`, and `feet_slide=-0.25`. Run name retains `angtrack060`; the archived config resolves angular tracking to 0.70.

## Credential filename review and Downloads extraction

No credential-like filenames (`.env`, token, secret, credential, private-key patterns) were found. Validation metadata reports boolean presence of submit host/token/credentials in the source environment; the archive contains no credential payload identified by the filename review. The raw archive remains unchanged.

The Downloads extraction contained 90 files. 89 match the outer or inner archive at the same relative path and SHA-256; the only uncovered file is the additional `policy.pt` (1,206,166 bytes; SHA-256 `3a49ac4a183609032b8bb23cf75a146048704e435c62d8797573d8cf001dbd1e`). This file is outside this run archive and should be preserved separately if needed.

Validation details: [evidence_intake_validation.json](evidence_intake_validation.json). Archive checksum: [SHA256SUMS](SHA256SUMS). [Remote asset verification](remote_verification.json) records successful size and SHA-256 checks for all five published assets.

[Training Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261018-exp-h1-joint-tracking-balance-ang070-plus3k)
