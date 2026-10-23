# exp-h1-action-foot-contact-stability

- Robot: H1
- Experiment question: Does ACTRATE-0001 + feet_slide=-0.35 improve foot-contact stability when trained fresh?
- Current training status: **OFFICIAL COMPLETED / exit 0 / validation PASS**.
- Current post-training evaluation: **PERSONAL Windows model2950 and Linux A4000 model9950 COMPLETE**, not official scores.
- Decision: **HOLD / model2950 analysis report received; model9950 analysis pending**; no adoption, reward causality or submission claim.
- Preset reference: `h1-submit-2`; final displayed overrides `{"action_rate_l2":-0.0001,"feet_slide":-0.35}`.
- Resolved configuration: archived native `params/env.yaml`, `params/agent.yaml`, reward source and source identity. Abbreviated overrides are not the full resolved config.

## Actual training Run

`20261013-153313-h1-actrate0001-feet_slide-fresh3k`: fresh, no resume/parent, seed42, 4096 environments, 3000 requested iterations; training COMPLETED and validation PASS. Native Run `/workspace/training/humanoid/logs/rsl_rl/humanoid/2026-10-14_00-33-21`. Indexed checkpoint used for evaluation: `model_2950.pt`, SHA `c4b283509cc659e7bd47f5bf49eddbc387a43963d751ef353c632f48c7da1374`; checkpoint filename is not unique across Runs.

[Canonical OFFICIAL archive](https://github.com/SE3C/naver-issacsim-originals/tree/main/data/raw/official_server_runs/h1/2026-10-14_003321_actrate0001_feet_slide_fresh3k) · [Training Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261013-exp-h1-action-foot-contact-stability-fresh3k). Original wrapper `20261013-153313-h1-actrate0001-feet_slide-fresh3k-download.tar.gz`, 419078411 bytes, SHA `9c7ffdac7cc4cbed0652b4bda028de950f0d1d3ed3510efdfcbcee04381bb409`. This is a new actual Run of the previously planned question, not another legacy H/HS ID.

## OFFICIAL same-reward continuation toward 10K — 2026-10-18

Run `20261018-062435-h1-top04-same-reward-to10k` continues the same `h1-submit-2 + action_rate_l2=-0.0001 + feet_slide=-0.35` configuration from stored iteration 2,950 for +7,050 iterations, seed 42 / 4,096 environments / save interval 50. It completed with exit 0 and evidence validation PASS. Latest indexed keeper: `model_9950.pt`, SHA-256 `2008e2f4c93a820c1ab396839ede1ba493e7b8dca7fffc3bbacb8de5ea257569`.

Parent checkpoint: OFFICIAL fresh3K Run `20261013-153313-h1-actrate0001-feet_slide-fresh3k`, `model_2950.pt`, SHA-256 `c4b283509cc659e7bd47f5bf49eddbc387a43963d751ef353c632f48c7da1374`. The prepared Rank-4 plan and child metadata source SHA match. The child's raw imported-parent fields remain `source_evidence_run_id=null`, `source_run_mode=unknown`, and `source_provenance_verified=false`; do not rewrite them. [Canonical OFFICIAL archive](https://github.com/SE3C/naver-issacsim-originals/tree/main/data/raw/official_server_runs/h1/2026-10-18_actrate0001_feetslide035_resume10k) · [Training Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261018-exp-h1-action-foot-contact-stability-action0001-feetslide035-resume10k). The model_9950 PERSONAL evaluation is recorded below; its policy analysis/adoption remain pending/HOLD.

### PERSONAL A4000 model9950 evaluation — 2026-10-18

[Canonical raw ZIP](https://github.com/SE3C/naver-issacsim-originals/tree/main/data/raw/private_server_runs/h1/2026-10-18_a4000_actrate0001_feetslide035_model9950_evaluation) · [Eval Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261018-exp-h1-action-foot-contact-stability-action0001-feetslide035-model9950-a4000-eval). Checkpoint SHA `2008e2f4c93a820c1ab396839ede1ba493e7b8dca7fffc3bbacb8de5ea257569` matches the OFFICIAL continuation index. Raw evaluation `source_run_id`/`preset=null` are preserved; linkage is external.

PERSONAL Linux RTX A4000 camera-off H1 scenario7 COMPLETE/non-smoke: 128 env × three seeds (4201/4202/4203) × eight cases ×20 seconds, 3,072 complete time-window cohorts and 3,074 episode rows including restarts. Existing dataset validator and ZIP CRC pass. Runtime 966.51s. Original three-file ZIP is 546,945 bytes, SHA-256 `62345448eabc9e550816103ded5117495c303103d1a0521add2ea6a877b1f582`. No six videos, A/B comparison, official score, submission or policy-quality decision is included. Publication launched no GPU work.

## Separate post-training evaluation

[Canonical PERSONAL ZIP](https://github.com/SE3C/naver-issacsim-originals/tree/main/data/raw/private_server_runs/h1/2026-10-14_windows_actrate0001_feet_slide_model2950_video_evaluation) · [Eval Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261014-exp-h1-action-foot-contact-stability-model2950-video-eval). ZIP CRC PASS / 18 files; six videos + separate full camera-off H1 scenario7, 128 env × three seeds × eight cases × 20 seconds, 3073 episode rows. Protocol `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34`. Actual task commit `ef10b7a4c9a83481346d446e8a75aed655f72214`; Eval publication tag is not a training-source commit. No new GPU run or behavior analysis was performed during intake.

## Comparison and historical plan

2026-10-14 [사용자 분석 원문 수신·보존](../../../data/processed/experiments/h1/analysis/2026-10-14_ACTRATE0001_FRESH_COMBINATION_REPORT_INTAKE.md) 완료. 이번 수납에서 결론 재검증이나 채택 판단 변경은 하지 않았다.

Primary reference: existing ACTRATE-0001 fresh3K, with matched source/PPO/seed/budget/evaluation conditions checked before causal interpretation. Historical plan and its guardrails remain [preserved](planned/exp-h1-action-foot-contact-stability.md); historical PLANNED does not override the verified completion above.

[Current registry](../../EXPERIMENTS.md)
