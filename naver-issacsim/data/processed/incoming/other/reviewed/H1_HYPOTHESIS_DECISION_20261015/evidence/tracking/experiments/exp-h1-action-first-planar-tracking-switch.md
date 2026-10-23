# exp-h1-action-first-planar-tracking-switch

- Robot: H1
- Status: **OFFICIAL training COMPLETED/PASS; PERSONAL full evaluation COMPLETE; analysis received / HOLD** (2026-10-11 KST)
- Experiment question: ACTRATE-0001 first, planar tracking one-step switch
- Actual mode: **OFFICIAL standalone resume from ACTRATE-0001 model_2700; +2K**
- Actual Run ID: `20261010-154926-h1-actrate0001-lintrack065-from2700-plus2k`
- Submission preset reference: `h1-submit-2`
- Actual final preset-relative override: `h1-submit-2 + lin=0.65 + action=-0.0001`
- Display reward descriptor: **not issued** (only currently defined short keys / full native field names)

## 2026-10-15 후속 상태 — 같은 이름의 정책·대조군 분리

이 문서의 `model_4650` SHA는 **`ce7ad58657f3dd744e7cf2b7531f3d7d455773dfc6fb135f39d8a55aa49dea70`**이며 `ACTRATE-0001 model_2700→lin=0.65` 한 단계 resume이다. 새로 접수된 **action-rate restoration** +2K `model_4650` SHA `a8249db467a60015036bf229b0026b215a61e17859f1d302efe283af225b84ea`와 서로 다른 Run/정책이다. 후자는 H3 월드 종료 잔류 **0.167m**, rough 평균 **8.769m**이고, **이 문서의 4650**은 H3 **2.398m**, rough **9.546m**라는 **서로 다른 제공 평가 보고서 수치**다. [2026-10-15 별도 보고서 수납](../../../data/processed/experiments/h1/analysis/2026-10-15_H1_MODEL4650_LINTRACK065_POLICY_REVIEW.md).

본 Run의 적절한 통제군인 동일 부모 무변경 +2K `20261014-111135-h1-actrate-0001-unchanged-cont2k`는 **OFFICIAL 학습과 PERSONAL `model_4699` 평가 모두 수납 완료**다. [10/15 후속 보고서](../../../data/processed/experiments/h1/analysis/2026-10-15_H1_NEXT_HYPOTHESIS_DECISION_INTAKE.md)에서 **기존 파생 CSV 수준의 4650 대 4699 비교도 완료**됐다. H5 진행 평균 +1.626684m·384/384건 증가 대신 H4 yaw 오차 +.087164rad/s·H3 world 잔류 +1.816354m로 **HOLD 유지**다. 원 episode 직접 재집계·선택 checkpoint4650 대 endpoint4699의 통제·reward 인과는 미확정이다. 외부 후속 lin=.55 +2K 권고는 아직 사용자 미선택·Run 미발급이다. 아래 당시 preflight·proposed parent 및 'control 필요' 문단은 *과거 계획/분석 시점*의 설명이며 이를 현재의 미실행 학습으로 오해하지 않는다. 별도 LINTRACK-065 **fresh5K `model_4950`**도 평가 완료/HOLD이나 이 Run의 continuation이 아니다.

## Question

기존 ACTRATE-0001의 역동적인 지형 진행을 먼저 학습한 뒤 선형속도 추종 가중치를 0.65로 올려 한 번 +2K 이어학습하면 H3 vy 추종과 H1 이동 편향이 개선되며 yaw·rough 진행이 유지되는가?

## Actual reward changes

- 부모에서 `action_rate_l2=-0.0001` **유지**
- `track_lin_vel_xy_exp`: 0.50 → 0.65 (**부모 대비 한 항목 추가**)

This is **one additional reward change relative to the existing ACTRATE-0001 checkpoint**, not a fresh 0→3K run. Executed additional budget: 2,000 iterations; it does not inherit any other proposed child.

## Received Run and publication

- OFFICIAL native Run: `/workspace/training/humanoid/logs/rsl_rl/humanoid/2026-10-11_00-49-32`; seed 42, 4096 environments, save interval 50. Exit 0, validation PASS, official finalize/backup completed. Console ends at 4699/4700; this is +2000 from checkpoint iteration 2700, not fresh5K.
- Imported parent `/workspace/model_2700.pt`, SHA `e54d3389e20ea913968ef8d3edbea5004368ff225fa6b94f73fcd91cf93ca7ae`, matches the existing OFFICIAL ACTRATE-0001 parent. Original metadata keeps `user_imported_checkpoint`, `source_provenance_verified=false`, `source_run_mode=unknown`, parent_run_id=null. Separate SHA linkage does not rewrite raw provenance.
- Latest preserved/evaluated `model_4650.pt`, SHA `ce7ad58657f3dd744e7cf2b7531f3d7d455773dfc6fb135f39d8a55aa49dea70`; automatic best is the distinct `model_2900.pt`. Forty organizer keeper checkpoints remain in the evidence archive.
- Full resolved-config sources: evidence `source/humanoid_rewards.py`, `native_run/params/env.yaml`, `native_run/params/agent.yaml`; actual weights: lin .65, ang .5, feet .2, termination -50, orientation -1.5, angular XY -.05, hip -.2, torso -.1, action -.0001. Official source Git commit is unknown; source identity before/after matched.
- [OFFICIAL archive Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261011-exp-h1-action-first-planar-tracking-switch-resume2700-plus2k); canonical Originals path `data/raw/official_server_runs/h1/2026-10-11_004932_actrate0001_lintrack065_resume2700_plus2k/`. Unchanged download archive SHA `4e604b7d29a0a4b220b44b2b60081b7742109e9b67b266d90434df234f925e3d`.
- [PERSONAL video/evaluation Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261011-exp-h1-action-first-planar-tracking-switch-model4650-video-eval); canonical Originals path `data/raw/private_server_runs/h1/2026-10-11_windows_actrate0001_lintrack065_model4650_video_evaluation/`. Unchanged ZIP SHA `5fa60c81a3808481b9a547ab097fa527a708e792992ea4443d66be3c5900ae3d`; 18 files, CRC PASS. Six H1 ±10° videos plus separate full camera-off scenario7, 128 envs × seeds4201/4202/4203 × eight cases, COMPLETE/non-smoke.
- Evaluation task/tag commit `ef10b7a4c9a83481346d446e8a75aed655f72214` is not the OFFICIAL training source Git commit. No new GPU execution was performed during intake/publication. Training completion is not policy adoption or an official score; analysis is received/HOLD. The later derived-CSV control comparison is recorded above; matched causal validation and adoption remain unconfirmed.

## Prior evidence and uncertainty

**2026-10-11 analysis received:** [원문](../../../data/processed/incoming/other/reviewed/H1_MODEL4650_POLICY_ANALYSIS_20261011.md) · [Policy review](../../../data/processed/experiments/h1/2026-10-11_ACTRATE0001_LINTRACK065_MODEL4650_POLICY_REVIEW.md). 3,072/3,072 timeout survival; H2/H7 body progress 14.812/9.757m, H1 world XY 0.228m, H3 residual world XY 2.398m, H4 yaw error .179rad/s, H5 progress mean/min 9.546/8.974m. **HOLD**: useful moving candidate, not all-terrain representative. Historical model2700 summary comparison is not matched raw A/B or reward causality. The report's unknown training identity is ZIP-only; separate train evidence supplies the external SHA link above. Report intake and later derived-CSV comparison are complete; adoption and matched causal validation remain unconfirmed.

PERSONAL corrected LINTRACK-075에서는 XY error 0.3695→0.3483 개선과 yaw error 1.0455→1.5292 악화가 함께 나타났다. 0.65는 실증된 최적값이 아니라 새로운 중간 가설이다. XY reward 상승이 정지 유지 문제를 직접 해결한다고 단정하지 않는다.

## Resume parent lineage and preflight

- **Existing OFFICIAL parent train Run:** `20261009-142350-h1-actrate-0001-fresh3k`, fresh 3,000 requested/completed (console 2999/3000), seed42 / 4096 envs, exit0 and validation PASS.
- Evaluated automatic-best: `model_2700.pt`, SHA-256 `e54d3389e20ea913968ef8d3edbea5004368ff225fa6b94f73fcd91cf93ca7ae`; this is the checkpoint with completed PERSONAL 3,072-cohort evaluation.
- Later numbered keeper: `model_2950.pt`, SHA-256 `d4fa722131d0559e02bbdf499cac87e6bba91372a1c9f9334b8cd4a7b7269b70`; this checkpoint is **not yet separately behavior-evaluated**. Prefer late numbered checkpoint unless late-window terrain/tracking/fall jointly collapse, but do not equate its behavior with model_2700.
- Before execution, inspect the **actual OFFICIAL checkout**, resolved agent/task/PPO and training reward, indexed checkpoint/`source_path`, selected parent bytes/SHA. All three proposed Resume children must branch from the **same verified ACTRATE-0001 numbered checkpoint**, not from each other. No made-up Run ID or checkpoint path.
- **One resume per branch**, +2,000 requested iterations. Multiple independent sibling Resume Runs are allowed. Do not add a further 5K→7K continuation; actual global iteration end is determined from execution evidence, not a guessed number.

## Preferred control and analysis

1순위 동일 ACTRATE-0001 checkpoint/동일 +2K 길이의 reward unchanged resume sibling. 2순위 기존 ACTRATE-0001 및 TERM-50 fixed evaluator 자료(학습량·source 차이 명시). H3 vy/vx error·stall, H4 yaw, H5 rough P05/최저 진행이 필수.

**Risk / falsification:** XY 강화에 따른 yaw/contact 희생, 거친 지형 정체, 비의도 움직임 악화 가능.

## Conditions and guardrails

- Preset `h1-submit-2` full native agent/env/source is the reference. On the competition OFFICIAL environment the permitted student change is `training/humanoid/humanoid_rewards.py` only; do not alter PPO, task, curriculum, or other files. Before running, verify actual active reward term and full resolved config, not just abbreviated weights.
- Proposed seed 42, 4096 environments. All actual Run IDs, parent/resume source, source revision, requested/performed iterations, checkpoint names, completion status, logs, console and evidence locations must be filled from **execution evidence only**.
- Evaluator guardrails: H1 zero-command unwanted body/world motion; H3 lateral `vy_error`, unwanted `vx`, stall and base-contact; H4 yaw; H5 rough mean/P05/min forward progress and worst-case stall; H6 slopes roll/pitch/action delta/progress; H7 push. Policy survival/training completion ≠ terrain completion or submission score.
- Equal `scenario7` keys do not prove identical terrain/reset across distinct runs. Unmatched videos are qualitative only; need controls for reward causality. All new evaluation/training/export, GPU/official server work and submission are **not authorized by this plan**.
- [Naming rule](../../EXPERIMENT_NAMING.md): Experiment is the research question; no legacy H-/HS- IDs, arbitrary series IDs, or unapproved reward descriptor. Full field name `feet_slide` is used verbatim. Actual execution is recorded above; the remaining sibling/control proposals do not imply completed Runs.

## Related resources

- 후속 control 학습·평가 완료: [ACTRATE unchanged +2K](exp-h1-action-rate-relaxation.md), Run `20261014-111135-h1-actrate-0001-unchanged-cont2k`, 동일 부모2700 SHA/reward 유지, OFFICIAL COMPLETED/PASS. 이 변경군과의 기존 CSV 교차 비교도 10/15 수납 완료다. 아래 과거 control 미완료 표현을 현재 학습·평가 부재로 해석하지 않는다.
- [2026-10-14 4정책 CPU 비교 수신](../../../data/processed/experiments/h1/analysis/2026-10-14_H1_4POLICY_LINTRACK065_COMPARISON_INTAKE.md): 부모2700 대비 x/y 오차 개선과 H4 yaw·H3 잔류·H5 평균/P05 진행 악화가 공존한다. HOLD 유지; 당시 없던 unchanged control은 이후 학습·평가 및 CSV 비교가 완료됐다. 당일 lin=.65 fresh5K/action=-.0005는 별도 Run이다.
- [All five selected hypotheses](../../../data/processed/planning/2026-10-10_H1_ACTRATE0001_FIVE_COMBINATION_HYPOTHESES.md)
- [Existing ACTRATE-0001 OFFICIAL train and PERSONAL evaluation](exp-h1-action-rate-relaxation.md)
- [Unchanged OFFICIAL TERM-50 control context](exp-h1-rough-terrain-orientation-relaxation.md)
- [기존 LINTRACK-075 기록](H-008.md)
- [Experiment Registry](../../EXPERIMENTS.md)

**The dated proposal is historical. The received training/evaluation completed; quality assessment, matched causal comparison and submission remain unconfirmed.**
