Go2 preliminary Round 5 submission snapshot — LINTRACK-125, selected model_7450.pt.

Preserves the three files received in the user's `Downloads/5` folder byte-for-byte: `policy.pt`, `env.yaml`, and the user-written technical report (asset name `technical_report.txt`). As with the Round-4 snapshot, no original portal ZIP was supplied; the five assets are those three files plus `submission_manifest.json` and `SHA256SUMS`.

Source Experiment: `exp-go2-planar-tracking-terrain-progression`. OFFICIAL training Run: `20260929-154342-go2-lintrack-125-fresh7500-official`, fresh 7,500 iterations, COMPLETE/PASS. Canonical training evidence: https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-go2-20260929-lintrack-125-fresh7500 .

Selected checkpoint: `model_7450.pt`, SHA-256 `b8766030e306dd72160d37292539575d5a1d92c2757f34637dafab3c1582343a`. All eight exported policy actor tensors match that native checkpoint exactly in a CPU check. The received `env.yaml` matches the official training-record extract. Automatic training best `model_7050.pt` is a distinct checkpoint; the report's highest training reward is a Run statistic rather than a claim that 7450 was automatic best.

Relative to `g2-submit-3`, the effective reward changes are `track_lin_vel_xy_exp 1.5 → 1.25` and `lin_vel_z_l2 -2.0 → -3.0`. The received `env.yaml` is the resolved configuration. The report's separate matched evaluation is PERSONAL evidence, not an official competition score. No Round-5 score, portal receipt or exact submission time was supplied.

Canonical received snapshot: https://github.com/SE3C/naver-issacsim-originals/tree/main/data/raw/official_server_runs/go2/2026-10-06_round5_model7450_submission . See the manifest and checksums for exact file identities.
