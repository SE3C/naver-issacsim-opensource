# exp-h1-action-airtime-fresh-interaction

- Robot: H1
- Experiment question: Does ACTRATE-0001 + feet=0.25 improve stability/progress when trained fresh?
- Current training status: **OFFICIAL COMPLETED / exit 0 / validation PASS**.
- Current post-training evaluation: **PERSONAL Windows COMPLETE**, not an official score.
- Decision: **HOLD / analysis report received**; no adoption, reward causality or submission claim.
- Preset reference: `h1-submit-2`; final displayed overrides `{"action_rate_l2":-0.0001,"feet_air_time":0.25}`.
- Resolved configuration: archived native `params/env.yaml`, `params/agent.yaml`, reward source and source identity. Abbreviated overrides are not the full resolved config.

## Actual training Run

`20261013-144616-h1-actrate0001-airtime025-fresh3k`: fresh, no resume/parent, seed42, 4096 environments, 3000 requested iterations; training COMPLETED and validation PASS. Native Run `/workspace/training/humanoid/logs/rsl_rl/humanoid/2026-10-13_23-46-24`. Indexed checkpoint used for evaluation: `model_2950.pt`, SHA `14fd9ad432dfc2ba7696b0d48d9a31753f42c74727083429cc9f2c7299aaffd6`; checkpoint filename is not unique across Runs.

[Canonical OFFICIAL archive](https://github.com/SE3C/naver-issacsim-originals/tree/main/data/raw/official_server_runs/h1/2026-10-13_234624_actrate0001_airtime025_fresh3k) · [Training Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261013-exp-h1-action-airtime-fresh-interaction-fresh3k). Original wrapper `20261013-144616-h1-actrate0001-airtime025-fresh3k-download.tar.gz`, 418977650 bytes, SHA `be197500532832d3d43c4436e9f64b967ded6f1cd92e14e5b1ee6cd31a8fa90e`. This is a new actual Run of the previously planned question, not another legacy H/HS ID.

## Separate post-training evaluation

[Canonical PERSONAL ZIP](https://github.com/SE3C/naver-issacsim-originals/tree/main/data/raw/private_server_runs/h1/2026-10-14_windows_actrate0001_airtime025_model2950_video_evaluation) · [Eval Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261014-exp-h1-action-airtime-fresh-interaction-model2950-video-eval). ZIP CRC PASS / 18 files; six videos + separate full camera-off H1 scenario7, 128 env × three seeds × eight cases × 20 seconds, 3072 episode rows. Protocol `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34`. Actual task commit `ef10b7a4c9a83481346d446e8a75aed655f72214`; Eval publication tag is not a training-source commit. No new GPU run or behavior analysis was performed during intake.

## Comparison and historical plan

2026-10-14 [사용자 분석 원문 수신·보존](../../../data/processed/experiments/h1/analysis/2026-10-14_ACTRATE0001_FRESH_COMBINATION_REPORT_INTAKE.md) 완료. 이번 수납에서 결론 재검증이나 채택 판단 변경은 하지 않았다.

Primary reference: existing ACTRATE-0001 fresh3K, with matched source/PPO/seed/budget/evaluation conditions checked before causal interpretation. Historical plan and its guardrails remain [preserved](planned/exp-h1-action-airtime-fresh-interaction.md); historical PLANNED does not override the verified completion above.

[Current registry](../../EXPERIMENTS.md)
