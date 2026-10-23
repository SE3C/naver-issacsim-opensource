# H1 ACTRATE-001 model_2850 · PERSONAL Windows videos + full evaluation

Six `maneuver_push` terrain videos (20 seconds each, H1 ±10° slopes), followed by a separate camera-off H1 `scenario7` evaluation. This is a post-training PERSONAL evaluation of the existing ACTRATE-001 Run, not a new training Run, official score, or A/B comparison.

- Source OFFICIAL training Run: `20261010-125324-h1-actrate-001-fresh3k`; [training Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261010-exp-h1-action-rate-smoothing-fresh3k).
- Selected checkpoint: `model_2850.pt`, SHA-256 `1e6d0950f5bd981ca1f88044e65ae7ee57505c47b92b5caad8c39263f4d93bb1`. This SHA externally links the evaluation to ACTRATE-001. The ZIP's embedded `source_run_id=null` remains unchanged. Another H1 policy also has a `model_2850.pt`; use the SHA to distinguish it.
- Evaluation: COMPLETE, `complete=true`, `smoke=false`; seven scenario groups, with 8 cases × 128 environments × 3 seeds (4201/4202/4203) = 3,072 episode rows. No metric interpretation is included.
- ZIP: `model_2850_h1_6terrain_evaluation_20261010-233937_1cc2ab9d.zip`, 35,121,564 bytes / 18 files, CRC valid, SHA-256 `1906880030393b904d7323bdbf71352f408a067328a09ac8bf87604438c07351`.
- [Canonical Originals backup](https://github.com/SE3C/naver-issacsim-originals/tree/main/data/raw/official_server_runs/h1/2026-10-10_215330_actrate001_fresh3k/personal_windows_eval_20261010).
- [PERSONAL evaluation Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261010-exp-h1-action-rate-smoothing-model2850-video-eval); its ZIP asset remote size and SHA match the local archive. Annotated tag target: evaluator task commit `ef10b7a4c9a83481346d446e8a75aed655f72214`, not the OFFICIAL training source commit.
- Canonical Originals commit: `5dcbfe36b3fc6fd014a3eb738b9e56518afd1300`.

Behavior analysis has not run. The policy decision remains unassessed; evaluation completion alone establishes no reward benefit or promotion.
