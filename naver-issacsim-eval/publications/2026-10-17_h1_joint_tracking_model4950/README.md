# [분석] H1 lin=0.65 · ang=0.60 · action=-0.0003 · PERSONAL model4950 · 6영상 + scenario7

Experiment `exp-h1-joint-tracking-balance`; source OFFICIAL fresh5K Run `20261017-015509-h1-lintrack-065-angtrack-060-actrate-0003-fresh5`. Configuration reference: `h1-submit-2 + action=-0.0003 + ang=0.60 + lin=0.65`. [Training Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261017-exp-h1-joint-tracking-balance-fresh5k).

Evaluated keeper **model_4950.pt**, SHA-256 `2df0584057deb4dc15ab3c4470d52da29e5468bbb819fe3e4c66a928462bc478`, matches the preserved OFFICIAL checkpoint index. Raw evaluation `source_run_id` and `preset` remain null; the publication records linkage by SHA without modifying the source manifest.

Windows PERSONAL camera-off H1 `scenario7` is COMPLETE/non-smoke: 128 environments × seeds 4201/4202/4203 × eight cases = 3,072 episode rows. Six 20-second `maneuver_push` videos use ±10° slopes. The unchanged 18-file ZIP passes CRC and all six listed video checksums. This publication did not launch GPU work or analyze policy quality.

Assets: original ZIP, checksum, `publication_manifest.json`. ZIP `20261017-015509-h1-lintrack-065-angtrack-060-actrate-0003-fresh5_model_4950_h1_6terrain_evaluation_20261017-133309_7911f3d0.zip`: 34,866,869 bytes; SHA-256 `f431ea153ffe6245fe29f781a3201239029922bc432f07bf1683a014e9cd46b3`. Canonical raw folder: Originals `data/raw/private_server_runs/h1/2026-10-17_windows_joint_tracking_model4950_video_evaluation/`.

This is PERSONAL post-training evaluation, not another training Run, official score, submission, or A/B report. Evaluation is complete; policy interpretation/report and adoption remain pending/HOLD. The annotated Eval tag identifies this publication record, not training source. [Evaluation Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261017-exp-h1-joint-tracking-balance-model4950-video-eval).
