# H1 selected ACTRATE-0001 combination hypotheses — 2026-10-10

**2026-10-16 현재 상태:** 아래는 최초 계획의 역사다. fresh 조합 두 개, lin=.65 resume, angxy=-.08 resume는 학습·PERSONAL 평가·보고서 수신 완료/HOLD이며 미실행은 feet=.25 resume 한 갈래다. 동일 부모 unchanged +2K control과 후속 raw 비교도 완료했다. [현재 방향·연구 근거](2026-10-16_H1_EVIDENCE_AND_RESEARCH_NEXT_EXPERIMENTS.md), [registry](../../../research/EXPERIMENTS.md)를 우선한다. 아래 no-Run/PLANNED/control 미완료를 현재 상태로 복사하지 않는다.

**Status: PLANNED.** Five research questions selected by the user and registered for future review; no new training Run ID, training, evaluation, checkpoint, export, or official score exists for these five. Today's separately scheduled `ACTRATE-001 / exp-h1-action-rate-smoothing` remains outside this group (actual execution not independently verified here).

**2026-10-12 탐색 갱신:** 이 문서는 2026-10-10 제안 당시의 계획 원문이다. 다섯 개 중 `exp-h1-action-first-planar-tracking-switch`는 2026-10-11 기준 **OFFICIAL resume 학습 완료/PASS, PERSONAL full 평가 완료·행동 HOLD**로 후속 근거가 확인됐다. 나머지 네 질문은 별도 Run 미실행이다. 실험 상태는 [registry](../../../research/EXPERIMENTS.md), 해당 [완료 Experiment](../../../research/experiments/h1/exp-h1-action-first-planar-tracking-switch.md)를 우선한다. 아래의 `PLANNED` 표현은 원래 작성 시점의 상태다.

## Five hypotheses and distinct training modes

| Research question | Proposed run | Final preset-relative override | Delta in new run |
| --- | --- | --- | --- |
| [`exp-h1-action-airtime-fresh-interaction`](../../../research/experiments/h1/planned/exp-h1-action-airtime-fresh-interaction.md) | **fresh 0→3K** | `h1-submit-2 + feet=0.25 + action=-0.0001` | 2 reward changes vs frozen baseline |
| [`exp-h1-action-foot-contact-stability`](../../../research/experiments/h1/planned/exp-h1-action-foot-contact-stability.md) | **fresh 0→3K** | `h1-submit-2 + action=-0.0001 + feet_slide=-0.35` | 2 reward changes vs frozen baseline |
| [`exp-h1-action-first-airtime-switch`](../../../research/experiments/h1/planned/exp-h1-action-first-airtime-switch.md) | **one-step resume from ACTRATE-0001 OFFICIAL 3K, +2K** | `h1-submit-2 + feet=0.25 + action=-0.0001` | 1 additional reward change vs same parent |
| [`exp-h1-action-first-planar-tracking-switch`](../../../research/experiments/h1/exp-h1-action-first-planar-tracking-switch.md) | **one-step resume from ACTRATE-0001 OFFICIAL 3K, +2K** | `h1-submit-2 + lin=0.65 + action=-0.0001` | 1 additional reward change vs same parent |
| [`exp-h1-action-first-body-rate-switch`](../../../research/experiments/h1/planned/exp-h1-action-first-body-rate-switch.md) | **one-step resume from ACTRATE-0001 OFFICIAL 3K, +2K** | `h1-submit-2 + angxy=-0.08 + action=-0.0001` | 1 additional reward change vs same parent |

**Important:** Fresh AIRTIME+ACTRATE and Resume ACTRATE-first AIRTIME use **the same final reward values** `feet=0.25 + action=-0.0001`, but have different learning histories and total budgets (3K vs roughly 5K). Difference between their final policies is a policy comparison, **not a controlled causal test of reward schedule**.

## Parent checkpoint, independent branches, and user resume constraint

## Resume parent lineage and preflight

- **Existing OFFICIAL parent train Run:** `20261009-142350-h1-actrate-0001-fresh3k`, fresh 3,000 requested/completed (console 2999/3000), seed42 / 4096 envs, exit0 and validation PASS.
- Evaluated automatic-best: `model_2700.pt`, SHA-256 `e54d3389e20ea913968ef8d3edbea5004368ff225fa6b94f73fcd91cf93ca7ae`; this is the checkpoint with completed PERSONAL 3,072-cohort evaluation.
- Later numbered keeper: `model_2950.pt`, SHA-256 `d4fa722131d0559e02bbdf499cac87e6bba91372a1c9f9334b8cd4a7b7269b70`; this checkpoint is **not yet separately behavior-evaluated**. Prefer late numbered checkpoint unless late-window terrain/tracking/fall jointly collapse, but do not equate its behavior with model_2700.
- Before execution, inspect the **actual OFFICIAL checkout**, resolved agent/task/PPO and training reward, indexed checkpoint/`source_path`, selected parent bytes/SHA. All three proposed Resume children must branch from the **same verified ACTRATE-0001 numbered checkpoint**, not from each other. No made-up Run ID or checkpoint path.
- **One resume per branch**, +2,000 requested iterations. Multiple independent sibling Resume Runs are allowed. Do not add a further 5K→7K continuation; actual global iteration end is determined from execution evidence, not a guessed number.


User's intended constraint is **one resume step per branch**, not “only one Resume Run in the whole research project.” Three independent sibling children can use a common 3K parent, each changing exactly one additional reward weight and running an independently tracked +2K. They must not resume any 5K child further to 7K under this plan. No new Run ID is issued until actual evidence.

## Comparison strategy

- **Fresh 2 questions:** First compare to completed OFFICIAL ACTRATE-0001 fresh3K `20261009-142350-h1-actrate-0001-fresh3k` since action remains -0.0001. Second compare to completed unchanged OFFICIAL TERM-50 fresh3K `20261008-062732-h1-term-50-fresh3k-control` where appropriate. Fresh baseline-relative differences involve two reward weights; avoid independent attribution without further ablation and source/PPO parity.
- **Resume 3 questions:** Preferred reward-effect control is an unchanged **+2K continuation from precisely the same verified parent checkpoint**; this control is not yet registered as completed or authorized for execution. Second, compare pre-resume parent behavior with training-budget and selected checkpoint caveats.
- **Validation:** H1 unintended body/world motion; H3 vy tracking, lateral-only forward leakage, contact termination, stall; H4 yaw; H5 rough mean/P05/min forward and tail stall; H6 slope body RMS/action-change/progress; H7 push. Use same evaluator & sufficient gait/stairs/boxes evidence before candidate promotion. A 20s timeout, good mean tracking or evidence PASS does not establish obstacle completion or reward causality.
- **Local provenance:** The previously observed ACTRATE-0001/model_2700 PERSONAL H5 mean/P05 forward 9.948/9.592m, H1 unintended forward 1.987m, H3 unwanted forward 1.677m, and action delta RMS 0.45687 motivate the tests but do **not** predict success.
- **OFFICIAL legal/source preflight:** permitted file `training/humanoid/humanoid_rewards.py`; compare live resolved config and full source/PPO. Frozen `h1-submit-2` has active `feet_slide=-0.25` and `ang_vel_xy_l2=-0.05`; do not assume reward activation from name alone. Preserve original evidence.

## Naming and status boundaries

- Follow [Experiment naming](../../../research/EXPERIMENT_NAMING.md). These are **research-question slugs**, not Run IDs, reward descriptors, legacy H/HS IDs, or invented numbered labels. Existing official short keys: `feet`, `action`, `lin`, `angxy`. The unregistered `feet_slide` short descriptor is not invented; use actual field `feet_slide=-0.35`.
- All five remain **PLANNED**; existing ACTRATE-0001 is OFFICIAL training COMPLETE/PASS and its model_2700 evaluation is PERSONAL. These are separate evidence classes. No automatic Optuna trial/tell, GPU job, video, export, submission, server power operation or external upload.

Sources: [ACTRATE-0001 Experiment](../../../research/experiments/h1/exp-h1-action-rate-relaxation.md) · [H1 raw 3-policy comparison](../experiments/h1/2026-10-10_H1_SCENARIO7_RAW_3POLICY_MATCHED_ANALYSIS.md) · [H-008 LINTRACK historical](../../../research/experiments/h1/H-008.md) · [H-010 combination historical](../../../research/experiments/h1/H-010.md) · [H1 frozen native env.yaml](../../../research/submission_presets/h1-submit-2/env.yaml).
