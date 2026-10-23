# H1 ANGTRACK-065 model_2950 · PERSONAL Windows videos + full evaluation

Six `maneuver_push` terrain videos (20 seconds each, H1 ±10° slopes), followed by a separate camera-off full H1 `scenario7` evaluation. This is a post-training PERSONAL evaluation, not an official score, a new training Run, or an A/B comparison.

- Source OFFICIAL training Run: `20261009-155344-h1-angtrack-065-fresh3k`; [training Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261010-exp-h1-angular-tracking-boost-fresh3k).
- Selected checkpoint: `model_2950.pt`, SHA-256 `6a6f456eb3f25a7d2764af576e30b1a8169674256ae5c2ba0a1b79ed368e118c`. This links the evaluation to ANGTRACK-065; the source bundle's `source_run_id=null`, `preset=null`, and `source_provenance_verified=false` remain unchanged.
- Evaluation: COMPLETE, non-smoke, 128 environments × 3 seeds (4201/4202/4203) × 8 cases × 20 seconds; 3,087 episodes; native exit 0. Protocol `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34`.
- ZIP: `model_best_h1_6terrain_evaluation_20261010-041416_066bf8a3.zip`, 32,626,954 bytes / 18 files, SHA-256 `ec1bc325feae5cd6da1643a9fbbe13b0640ad7514b77b79e5532d8b836def93b`.
- [Canonical raw backup](https://github.com/SE3C/naver-issacsim-originals/tree/main/data/raw/private_server_runs/h1/2026-10-10_windows_angtrack065_model2950_video_evaluation).
- Evaluation task / annotated-tag target: `ef10b7a4c9a83481346d446e8a75aed655f72214`.

**Decision remains HOLD.** At original publication the single-policy behavioral analysis was pending. A later 2026-10-10 analysis is now received: [verbatim user report](../../incoming/other/reviewed/H1_ANGTRACK-065_POLICY_ANALYSIS_20261010.md) / [behavioral intake](../../experiments/h1/2026-10-10_ANGTRACK065_MODEL2950_POLICY_REVIEW.md). The analysis reports 3,072 initial cohorts but 3,087 episode rows after 15 H3 lateral initial-cohort base-contact terminations and 15 short restarts; H3 first-attempt 20-second timeout survival is 369/384. Evaluation completion alone does not establish improvement or promotion; a matched unchanged-control ANGTRACK raw comparison and official score are not established.

Assets: unchanged integrated ZIP + matching `.sha256` + `publication_manifest.json`.

- Release: https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261010-exp-h1-angular-tracking-boost-model2950-video-eval
- Canonical Originals commit: `2329fbfaf72334ee25c7023de4f7e8baaaaa6b92`.
- Remote size/digest verification: all three assets match; the annotated tag targets evaluator task commit `ef10b7a4c9a83481346d446e8a75aed655f72214`. [Verification record](2026-10-10_angtrack065_model2950_release_verified.json).
