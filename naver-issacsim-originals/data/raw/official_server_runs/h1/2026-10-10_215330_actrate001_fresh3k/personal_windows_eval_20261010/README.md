# H1 ACTRATE-001 model_2850 PERSONAL Windows video and evaluation

This directory preserves the received combined ZIP unchanged. It records PERSONAL Windows post-training video and evaluation of the automatic-best checkpoint from an OFFICIAL H1 ACTRATE-001 fresh 3K Run. The checkpoint number `model_2850.pt` also appears in the separate ORIENT-100 Run; the SHA-256 below identifies this artifact as ACTRATE-001. This is not an official score, a new training Run, or an official-server evaluation.

- Source training Run: `20261010-125324-h1-actrate-001-fresh3k`; [OFFICIAL training Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261010-exp-h1-action-rate-smoothing-fresh3k).
- Source checkpoint: `model_2850.pt`, SHA-256 `1e6d0950f5bd981ca1f88044e65ae7ee57505c47b92b5caad8c39263f4d93bb1` (automatic best at iteration 2850, matching the official training checkpoint index). The latest preserved training checkpoint `model_2950.pt` is a different file and is not evaluated here.
- Original bundle: `model_2850_h1_6terrain_evaluation_20261010-233937_1cc2ab9d.zip`; 35,121,564 bytes; SHA-256 `1906880030393b904d7323bdbf71352f408a067328a09ac8bf87604438c07351`.
- Bundle contents: 18 files, including six 20-second H1 videos and full camera-off `scenario7` evaluation evidence. The videos use the separate qualitative `maneuver_push` suite with ±10° slopes. CRC validation passed.
- Evaluation: PERSONAL Windows, scenario7, complete and not smoke; 7 scenarios / 8 cases, 128 environments, seeds 4201/4202/4203, 3,072 episodes total, 20 seconds / 1,000 steps each, camera disabled. Diagnostics record zero base-contact failures in these fixed 20-second windows; this does not establish terrain completion or an official score.
- Protocol ID: `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34`.
- The original `evaluation/evaluation_manifest.json` and `evaluation/video_evaluation_link.json` keep `policy.source_run_id` null. The external Run link is based on the source checkpoint SHA matching the preserved OFFICIAL ACTRATE-001 training evidence; the ZIP metadata itself is unchanged.
- [PERSONAL Windows Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261010-exp-h1-action-rate-smoothing-model2850-video-eval).

The OFFICIAL training archive remains in the parent Run directory. No checkpoint, source code, or training artifact was modified or merged into this PERSONAL evaluation bundle.
