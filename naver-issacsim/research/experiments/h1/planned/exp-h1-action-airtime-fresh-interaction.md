# exp-h1-action-airtime-fresh-interaction

> **2026-10-14 현재 상태:** 이 문서의 PLANNED는 2026-10-10 계획 당시 상태다. 이후 OFFICIAL fresh3K와 PERSONAL 평가가 완료됐다. 현재 Run·출처·판정은 [완료 기록](../exp-h1-action-airtime-fresh-interaction.md)을 따른다. 아래 계획 원문은 보존한다.

- Robot: H1
- Status: **PLANNED / no new training Run executed** (2026-10-10 KST)
- Experiment question: ACTRATE-0001 × AIRTIME-025 fresh joint-reward interaction
- Proposed mode: **OFFICIAL fresh 0→3K**
- Actual Run ID: **not issued**
- Submission preset reference: `h1-submit-2`
- Proposed final preset-relative override: `h1-submit-2 + feet=0.25 + action=-0.0001`
- Display reward descriptor: **not issued** (only currently defined short keys / full native field names)

## Question

처음부터 두 reward를 함께 사용한 fresh 3K가, 기존 ACTRATE-0001의 rough 진행을 유지하면서 H1/H3 비의도 움직임과 접촉 안정성을 보완하는가?

## Proposed actual changes

- `feet_air_time`: 0.20 → 0.25
- `action_rate_l2`: -0.0005 → -0.0001

Two baseline-relative reward changes are applied **from the first iteration**. No checkpoint parent or resume is used. Proposed budget: 3,000 iterations, seed42, 4096 envs.

## Prior evidence and uncertainty

OFFICIAL `ACTRATE-0001`은 3K 완료. PERSONAL `model_2700` 평가에서 H5 rough mean/P05는 9.948/9.592m, H1 정지 비의도 전진은 1.987m, H3 측면 명령 비의도 전진은 1.677m다. AIRTIME-025의 공식 10K/과거 PERSONAL 학습 기록은 개별 방향성 참고이고 이 두 reward 결합의 성공 근거는 아니다.

## Preferred control and analysis

1순위는 OFFICIAL ACTRATE-0001 fresh3K와 동일 evaluator 조건 비교(공통 action=-0.0001, feet만 다른 설정). 2순위는 unchanged TERM-50 fresh3K 및 과거 AIRTIME-025의 별도 evidence. 실제 source/PPO/학습 길이/평가 조건·checkpoint 시점을 맞춘 정도에 따라 인과 해석을 제한한다.

**Risk / falsification:** 강해진 발 체공 보상이 불필요한 stepping, 정지 편향, yaw 비용 또는 base-contact 종료를 악화할 수 있다.

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
- [동일 최종 reward의 action-first AIRTIME one-step resume](exp-h1-action-first-airtime-switch.md)
- [Experiment Registry](../../../EXPERIMENTS.md)

**This is a plan, not training, result, evaluation, export, or official score.**
