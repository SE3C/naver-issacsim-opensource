# exp-h1-action-foot-contact-stability

> **2026-10-14 현재 상태:** 이 문서의 PLANNED는 2026-10-10 계획 당시 상태다. 이후 OFFICIAL fresh3K와 PERSONAL 평가가 완료됐다. 현재 Run·출처·판정은 [완료 기록](../exp-h1-action-foot-contact-stability.md)을 따른다. 아래 계획 원문은 보존한다.

- Robot: H1
- Status: **PLANNED / no new training Run executed** (2026-10-10 KST)
- Experiment question: ACTRATE-0001 × feet_slide foot-contact stability
- Proposed mode: **OFFICIAL fresh 0→3K**
- Actual Run ID: **not issued**
- Submission preset reference: `h1-submit-2`
- Proposed final preset-relative override: `h1-submit-2 + action=-0.0001 + feet_slide=-0.35`
- Display reward descriptor: **not issued** (only currently defined short keys / full native field names)

## Question

동작 변화 페널티를 완화하면서 접촉 중 발 미끄럼 페널티를 강화하면 H5 rough 진행을 잃지 않고 H3 lateral 안정성, 접촉 유지 및 worst-case stall을 개선하는가?

## Proposed actual changes

- `action_rate_l2`: -0.0005 → -0.0001
- `feet_slide`: -0.25 → -0.35

Two baseline-relative reward changes are applied **from the first iteration**. No checkpoint parent or resume is used. Proposed budget: 3,000 iterations, seed42, 4096 envs.

## Prior evidence and uncertainty

Frozen `h1-submit-2` full `env.yaml`에는 활성 `feet_slide=-0.25`가 존재한다. ACTRATE-0001 H5 진행은 좋은 편이나 H3 비의도 전진·action Δ가 높다. 현재 evaluator ZIP에는 발 미끄럼 직접 계측 필드가 없으므로 lateral 불안정의 원인이 slip이라는 주장은 미검증이다.

## Preferred control and analysis

1순위 OFFICIAL ACTRATE-0001 fresh3K (공통 action; slide 단일 차이). 2순위 unchanged TERM-50 fresh3K. H3 vy/vx error, base-contact, stall 및 H5 mean/P05/min 실제 진행을 동일 evaluator로 확인한다.

**Risk / falsification:** 발 전환이 소극화되어 정체, 보폭 감소, 지형 통과 악화가 일어날 수 있다. 공식 서버의 활성 reward term 및 weight 적용 확인 필수.

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
- [학습 기준 native resolved H1 env.yaml](../../../submission_presets/h1-submit-2/env.yaml)
- [Experiment Registry](../../../EXPERIMENTS.md)

**This is a plan, not training, result, evaluation, export, or official score.**
