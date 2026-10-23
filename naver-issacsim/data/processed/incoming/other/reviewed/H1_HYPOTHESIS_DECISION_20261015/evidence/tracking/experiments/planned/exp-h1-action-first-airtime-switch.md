# exp-h1-action-first-airtime-switch

- Robot: H1
- Status: **PLANNED / no new training Run executed** (2026-10-10 KST)
- Experiment question: ACTRATE-0001 first, AIRTIME-025 one-step reward switch
- Proposed mode: **OFFICIAL resume from ACTRATE-0001 3K; +2K only**
- Actual Run ID: **not issued**
- Submission preset reference: `h1-submit-2`
- Proposed final preset-relative override: `h1-submit-2 + feet=0.25 + action=-0.0001`
- Display reward descriptor: **not issued** (only currently defined short keys / full native field names)

## Question

ACTRATE-0001로 먼저 보행을 학습한 OFFICIAL 3K checkpoint를 부모로 하여 AIRTIME을 강화한 뒤 한 번 +2K fine-tuning하면 H5 진행을 유지하면서 H1/H3·yaw·접촉이 개선되는가? 동일 최종 reward를 처음부터 사용한 fresh 정책과의 차이는 무엇인가?

## Proposed actual changes

- 부모에서 `action_rate_l2=-0.0001` **유지**
- `feet_air_time`: 0.20 → 0.25 (**부모 대비 한 항목 추가**)

This is **one additional reward change relative to the existing ACTRATE-0001 checkpoint**, not a fresh 0→3K run. Proposed additional budget: 2,000 iterations; it does not inherit any other proposed child.

## Prior evidence and uncertainty

과거 H-008→H-010 PERSONAL corrected 3K→5K 분기는 LINTRACK-075 부모에서 feet_air_time을 0.20→0.25로 바꾸어 yaw/contact 개선 신호를 보였지만 부모/설정이 다르고 통제된 인과 근거는 아니다.

## Resume parent lineage and preflight

- **Existing OFFICIAL parent train Run:** `20261009-142350-h1-actrate-0001-fresh3k`, fresh 3,000 requested/completed (console 2999/3000), seed42 / 4096 envs, exit0 and validation PASS.
- Evaluated automatic-best: `model_2700.pt`, SHA-256 `e54d3389e20ea913968ef8d3edbea5004368ff225fa6b94f73fcd91cf93ca7ae`; this is the checkpoint with completed PERSONAL 3,072-cohort evaluation.
- Later numbered keeper: `model_2950.pt`, SHA-256 `d4fa722131d0559e02bbdf499cac87e6bba91372a1c9f9334b8cd4a7b7269b70`; this checkpoint is **not yet separately behavior-evaluated**. Prefer late numbered checkpoint unless late-window terrain/tracking/fall jointly collapse, but do not equate its behavior with model_2700.
- Before execution, inspect the **actual OFFICIAL checkout**, resolved agent/task/PPO and training reward, indexed checkpoint/`source_path`, selected parent bytes/SHA. All three proposed Resume children must branch from the **same verified ACTRATE-0001 numbered checkpoint**, not from each other. No made-up Run ID or checkpoint path.
- **One resume per branch**, +2,000 requested iterations. Multiple independent sibling Resume Runs are allowed. Do not add a further 5K→7K continuation; actual global iteration end is determined from execution evidence, not a guessed number.

## Preferred control and analysis

**1순위** 동일 ACTRATE-0001 checkpoint에서 reward 변경 없이 같은 +2K의 sibling control (별도 승인으로 실제 확보된 경우에만). **2순위** [같은 최종 reward Fresh 3K](exp-h1-action-airtime-fresh-interaction.md) 및 기존 ACTRATE-0001 행동 자료. Fresh 3K vs Resume 총 약 5K는 학습량과 학습 순서가 섞여 있으므로 schedule 인과 결론 금지.

**Risk / falsification:** 전환 직후 curriculum/optimizer 재적응, gait 불안정, yaw/자세 악화. 5K child를 다시 7K로 연쇄 resume 하지 않음.

## Conditions and guardrails

- Preset `h1-submit-2` full native agent/env/source is the reference. On the competition OFFICIAL environment the permitted student change is `training/humanoid/humanoid_rewards.py` only; do not alter PPO, task, curriculum, or other files. Before running, verify actual active reward term and full resolved config, not just abbreviated weights.
- Proposed seed 42, 4096 environments. All actual Run IDs, parent/resume source, source revision, requested/performed iterations, checkpoint names, completion status, logs, console and evidence locations must be filled from **execution evidence only**.
- Evaluator guardrails: H1 zero-command unwanted body/world motion; H3 lateral `vy_error`, unwanted `vx`, stall and base-contact; H4 yaw; H5 rough mean/P05/min forward progress and worst-case stall; H6 slopes roll/pitch/action delta/progress; H7 push. Policy survival/training completion ≠ terrain completion or submission score.
- Equal `scenario7` keys do not prove identical terrain/reset across distinct runs. Unmatched videos are qualitative only; need controls for reward causality. All new evaluation/training/export, GPU/official server work and submission are **not authorized by this plan**.
- [Naming rule](../../../EXPERIMENT_NAMING.md): Experiment is the research question; no legacy H-/HS- IDs, arbitrary series IDs, or unapproved reward descriptor. Full field name `feet_slide` is used verbatim. The **actual Run ID does not exist yet**.

## Related resources

- [All five selected hypotheses](../../../../data/processed/planning/2026-10-10_H1_ACTRATE0001_FIVE_COMBINATION_HYPOTHESES.md)
- [Existing ACTRATE-0001 OFFICIAL train and PERSONAL evaluation](../exp-h1-action-rate-relaxation.md)
- [Unchanged OFFICIAL TERM-50 control context](../exp-h1-rough-terrain-orientation-relaxation.md)
- [동일 reward Fresh 조합](exp-h1-action-airtime-fresh-interaction.md)
- [Experiment Registry](../../../EXPERIMENTS.md)

**This is a plan, not training, result, evaluation, export, or official score.**
