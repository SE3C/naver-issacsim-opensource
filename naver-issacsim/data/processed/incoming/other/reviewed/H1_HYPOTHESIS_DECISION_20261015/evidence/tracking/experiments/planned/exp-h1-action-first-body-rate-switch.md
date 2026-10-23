# exp-h1-action-first-body-rate-switch

- Robot: H1
- Status: **PLANNED / no new training Run executed** (2026-10-10 KST)
- Experiment question: ACTRATE-0001 first, body angular-rate one-step switch
- Proposed mode: **OFFICIAL resume from ACTRATE-0001 3K; +2K only**
- Actual Run ID: **not issued**
- Submission preset reference: `h1-submit-2`
- Proposed final preset-relative override: `h1-submit-2 + angxy=-0.08 + action=-0.0001`
- Display reward descriptor: **not issued** (only currently defined short keys / full native field names)

## Question

ACTRATE-0001의 동작 자유도를 확보한 뒤 roll/pitch 각속도 페널티를 강화해 한 번 +2K 이어학습하면 H3 횡이동 안정성, H6 경사 자세·action 변동을 개선하면서 rough 진행을 유지하는가?

## Proposed actual changes

- 부모에서 `action_rate_l2=-0.0001` **유지**
- `ang_vel_xy_l2`: -0.05 → -0.08 (**부모 대비 한 항목 추가**)

This is **one additional reward change relative to the existing ACTRATE-0001 checkpoint**, not a fresh 0→3K run. Proposed additional budget: 2,000 iterations; it does not inherit any other proposed child.

## Prior evidence and uncertainty

기존 ORIENT-100은 `flat_orientation_l2=-1.0`으로 기울기 자체를 제약하는 다른 실험이다. ORIENT PERSONAL 전체 roll/pitch RMS 0.08015의 관측은 angxy reward 강화 성공의 증거가 아니다. 동결 baseline에서 angxy=-0.05인 것은 확인됐다.

## Resume parent lineage and preflight

- **Existing OFFICIAL parent train Run:** `20261009-142350-h1-actrate-0001-fresh3k`, fresh 3,000 requested/completed (console 2999/3000), seed42 / 4096 envs, exit0 and validation PASS.
- Evaluated automatic-best: `model_2700.pt`, SHA-256 `e54d3389e20ea913968ef8d3edbea5004368ff225fa6b94f73fcd91cf93ca7ae`; this is the checkpoint with completed PERSONAL 3,072-cohort evaluation.
- Later numbered keeper: `model_2950.pt`, SHA-256 `d4fa722131d0559e02bbdf499cac87e6bba91372a1c9f9334b8cd4a7b7269b70`; this checkpoint is **not yet separately behavior-evaluated**. Prefer late numbered checkpoint unless late-window terrain/tracking/fall jointly collapse, but do not equate its behavior with model_2700.
- Before execution, inspect the **actual OFFICIAL checkout**, resolved agent/task/PPO and training reward, indexed checkpoint/`source_path`, selected parent bytes/SHA. All three proposed Resume children must branch from the **same verified ACTRATE-0001 numbered checkpoint**, not from each other. No made-up Run ID or checkpoint path.
- **One resume per branch**, +2,000 requested iterations. Multiple independent sibling Resume Runs are allowed. Do not add a further 5K→7K continuation; actual global iteration end is determined from execution evidence, not a guessed number.

## Preferred control and analysis

1순위 동일 ACTRATE-0001 checkpoint/동일 +2K 길이의 reward unchanged resume sibling. 2순위 기존 ACTRATE-0001 행동과 TERM-50 참고. H3 fall/vy/stall, H6 roll/pitch RMS 및 action Δ, H4 yaw, H5 worst progress를 함께 확인한다.

**Risk / falsification:** 균형 회복에 필요한 몸통 회전까지 억제되어 움직임이 경직되고 경사·횡이동 대응이 악화될 수 있다.

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
- [기존 ORIENT-100 실험](../exp-h1-rough-terrain-orientation-relaxation.md)
- [Experiment Registry](../../../EXPERIMENTS.md)

**This is a plan, not training, result, evaluation, export, or official score.**
