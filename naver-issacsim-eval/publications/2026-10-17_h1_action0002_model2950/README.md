# [분석] H1 action=-0.0002 · PERSONAL model_2950 · 6영상 + scenario7 평가

Experiment `exp-h1-action-rate-relaxation`; source OFFICIAL fresh3K Run `20261016-150803-h1-actrate0002-fresh3k`. Config reference: `h1-submit-2 + action_rate_l2=-0.0002`; see the [training Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261016-exp-h1-action-rate-relaxation-action0002-fresh3k).

Evaluated native keeper **model_2950.pt**, SHA-256 `eaa7a50c51fbdf3b39c15fe4278d1c9def38f96e9af872eb37111b66ac4d34fb`, matching the OFFICIAL training checkpoint index. Raw evaluation `source_run_id` and preset are null; linkage here is by checkpoint SHA only.

Windows PERSONAL camera-off H1 `scenario7` is COMPLETE/non-smoke: 128 environments × seeds 4201/4202/4203 × eight cases = 3,072 episode rows. Six 20-second `maneuver_push` videos use ±10° slopes. Original ZIP has 18 entries; CRC and all six listed video hashes pass. This intake did not render videos, run evaluation, or assess policy behavior.

Assets: unchanged original ZIP, checksum, and `publication_manifest.json`. Archive `20261016-150803-h1-actrate0002-fresh3k_model_2950_h1_6terrain_evaluation_20261017-020342_54af98b1.zip`, 35,969,460 bytes, SHA-256 `f658b2217737e5271caaf4eaa3c0ac48f29d1929d680a1688da509a0d87b3c3c`. Canonical raw copy is in Originals at `data/raw/private_server_runs/h1/2026-10-17_windows_action0002_model2950_video_evaluation/evidence_archives/`.

This is PERSONAL evaluation evidence, not a new training Run, official score, submission, or comparison report. The annotated Eval tag identifies this publication-record commit, not the training source revision. [Evaluation Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261017-exp-h1-action-rate-relaxation-action0002-model2950-video-eval).
