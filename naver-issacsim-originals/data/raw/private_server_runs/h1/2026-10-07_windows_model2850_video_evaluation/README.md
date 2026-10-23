# H1 ORIENT-100 model_2850 PERSONAL Windows video and evaluation evidence

This directory preserves the received combined ZIP byte-for-byte. It records a PERSONAL Windows post-training video and evaluation of the automatic-best checkpoint from the official H1 ORIENT-100 fresh 3K Run. It is not an official evaluation score, a new training Run, or an additional official result.

- Source Run: `20261006-133517-h1-orient-100-fresh3k-official`.
- Source checkpoint: `model_2850.pt`, SHA-256 `6aedeced60562c1d496d5319d29b76cf9e26ff43df06827cb370f24f5313f7b0` (automatic best at iteration 2850; the latest preserved checkpoint is model_2950.pt and is a distinct checkpoint).
- Original bundle: `model_2850_ORIENT-100_h1_6terrain_evaluation_20261007-010444_f6b3b8b3.zip`.
- Size: 33,323,164 bytes. SHA-256: `aecc82b13671d54c96813af6c02c1b2a7769ee001b30aa4a5c2761457110eb7a`.
- Contents: six H1 terrain videos, their source/evaluation metadata, and completed full camera-off `scenario7` evaluation files (18 files total).
- Evaluation protocol: 128 environments, seeds 4201/4202/4203, 20 seconds per case, camera disabled; complete and not smoke. The six videos use the separate qualitative `maneuver_push` suite.
- Protocol ID: `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34`.
- The original evaluation manifest's `policy.source_run_id` remains null. The external source Run linkage is based on the checkpoint SHA matching the preserved official intake evidence.
- Publication: [PERSONAL Windows Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261007-exp-h1-rough-terrain-orientation-relaxation-model2850-video-eval).

The official training archive and checkpoint remain preserved separately. No source training artifact was modified or merged into this personal evaluation bundle.
