# H1 다음 실험 방향 — 새 angxy 결과와 1차 연구 근거

**2026-10-18 후속 방향:** 새 reward 가설 추가보다 기존 설정의 10K 장기 확인을 우선한다. [TOP10 외주 자문](../experiments/h1/analysis/2026-10-18_H1_10K_TOP10_SELECTION_INTAKE.md)의 상위3개는 JOINT(.65/.60/-.0003)5K 연장 → action=-.0003 3K 연장 → ORIENT-100 연장이다. 자문 수신/사용자 선택 대기이며 아래 과거 계획을 삭제하거나 새 학습을 승인하지 않는다. 평가2850과 keeper2950이 다른 후보의 출발점은 별도 확인하며 기존 HOLD·제출본을 보존한다.

**수신 후 상태 갱신:** 아래 action=-.0003 fresh3K 제안은 실제 Run `20261016-033023-h1-actrate-0003-fresh3k`로 OFFICIAL COMPLETED/exit0/PASS를 확인했다. [현재 Run 기록](../../../research/experiments/h1/exp-h1-action-rate-relaxation.md) · [PERSONAL 행동 평가·분석 완료/HOLD](../experiments/h1/analysis/2026-10-16_H1_ACTION0003_MODEL2950_POLICY_REVIEW.md). 아래 표의 해당 fresh 제안은 실행 전 설계 기록이며 다시 미실행 후보로 제안하지 않는다. 다른 후보는 실행됐다고 해석하지 않는다.

작성 2026-10-16 KST. **설계·권고 문서이며 GPU/학습 실행 승인이나 Run 완료 기록이 아니다.** [현재 registry](../../../research/EXPERIMENTS.md)와 [angxy 수납·5정책 CPU 결과](../experiments/h1/analysis/2026-10-16_H1_ANGXY008_MODEL4650_POLICY_REVIEW.md)를 먼저 읽는다. 새 H/HS 번호를 발급하지 않는다.

## 2026-10-17 제출 임박 시 고위험 조합 후보 — 학습·평가·보고서 완료 / HOLD

**후속 수납:** [joint tracking Experiment](../../../research/experiments/h1/exp-h1-joint-tracking-balance.md)의 실제 OFFICIAL Run `20261017-015509-h1-lintrack-065-angtrack-060-actrate-0003-fresh5`가 fresh5K·seed42/4096env, console4999, COMPLETED/exit0/PASS로 확인됐다. keeper4950과 auto-best4800은 별개다. **이후 PERSONAL 평가와 [보고서](../experiments/h1/analysis/2026-10-17_H1_JOINT_TRACKING_MODEL4950_POLICY_REVIEW.md)도 수신 완료/HOLD**로 갱신됐다. H5는 낙상·완전 정체보다 지속 저속이 남고, 기존 LINTRACK065 raw와의 CPU 비교는 미실행이다. 아래 미실행·실행 승인 없음 및 후속 보고서 미반영 문구는 각 설계 시점의 기록이며 새 실행이나 우선순위를 자동 확정하지 않는다.

사용자는 제출까지 하루 남은 상황에서 재현성 확인보다 새 성능 후보 탐색을 우선하도록 요청했다. 이에 따른 **예외적인 고위험 config 탐색**이며, 아래의 보수적 기본 우선순위와 구분한다. 가설 문서 반영 요청은 학습 실행 승인이 아니며 실제 Run ID·실행 환경·결과·새 submission preset은 아직 없다.

**Experiment 질문:** 선형·각속도 추종 보상을 함께 높이고 중간 action 평활화를 적용하면, 기존 선형 추종 강화의 yaw 손실을 줄이면서 명령 추종과 험지 진행의 더 나은 조합을 얻을 수 있는가?

- 기반: immutable `h1-submit-2`. 최종 override는 `action=-0.0003 + ang=0.60 + lin=0.65`이며 기존 H/HS 번호를 새로 발급하지 않는다.
- 계획: **fresh/no checkpoint, 5000회, 4096env, seed42, save_interval50**. 부모·resume 전환이 없는 고정 config 한 번의 실행이다. 환경은 실제 실행 시 확인·기록한다.
- 실행 전 목표 9개 값: `track_lin_vel_xy_exp=0.65`, `track_ang_vel_z_exp=0.60`, `feet_air_time=0.20`, `termination_penalty=-50`, `flat_orientation_l2=-1.5`, `ang_vel_xy_l2=-0.05`, `joint_deviation_hip=-0.2`, `joint_deviation_torso=-0.1`, `action_rate_l2=-0.0003`. 다른 활성 reward·환경·PPO는 기준 preset 유지. 이 목록은 전체 resolved config를 대신하지 않으며 실제 설정은 실행 evidence에 보존한다.
- 의도: lin=.65로 선형 추종 압력을 높이고, ang=.60으로 yaw 추종 보완을 시도하며, action=-.0003을 평활화 기준으로 사용한다. **보상 증가가 실제 추종 개선을 보장하거나 서로의 부작용을 상쇄한다는 증거는 없다.**
- 선택 배경: [action=-.0002 단독 보고서](../experiments/h1/analysis/2026-10-17_H1_ACTION0002_MODEL2950_POLICY_REVIEW.md)는 HOLD이고 -.0003 대비 뚜렷한 우위가 확인되지 않았다. 따라서 seed 반복·무변경 연장은 보존하되, 당장의 공격적 탐색보다 우선하지 않는다.
- 위험 근거: [ANGTRACK-.65 대조](../experiments/h1/analysis/2026-10-10_H1_ANGTRACK065_TERM50_DEEP_RAW_COMPARISON.md)에서 yaw 이득과 H3 접촉·추종 손실이 함께 관측됐고, [lin=.65 fresh5K 기록](../../../research/experiments/h1/exp-h1-planar-tracking-weight.md)도 HOLD다. ang=.60과 이번 3항 조합은 그 결과와 다른 미검증 설정이며, 기존 실패가 해결됐다고 간주하지 않는다.
- 비교: 기존 -.0003 fresh3K와 lin=.65 fresh5K, 현재 제출 정책을 참고군으로 사용한다. 설정·학습량·checkpoint 역할이 달라 단일 reward의 인과효과로 해석하지 않는다. 세 항을 동시에 바꾸는 목적은 원인 분리가 아니라 **완성 config 후보 발견**이다.
- 판정: H1 정지 비의도 이동, H2 선형·H3 횡속도·H4 yaw 추종, H5 rough 진행/추종/하위 꼬리, H6 경사·H7 회복 및 생존을 함께 확인한다. total reward나 생존만으로 채택하지 않으며 H3 world 잔류를 공식 원점복귀 실패로 바꾸지 않는다. 기존 제출 정책은 보존하고 새 후보를 자동 제출하지 않는다.
- 운영: 1K는 치명 붕괴 점검이고 정상이라면 계획된 5K까지 진행하는 고위험 후보다. 기존 issacsimz tmux/evidence/keeper 흐름을 사용하고, 학습 종료 후 실제 보존된 final checkpoint를 확인한다. 추가 resume·자동 batch·서버 종료는 이 기록에 포함하지 않는다. 최종 평가·export·제출 파일 확인 시간을 따로 확보한다.

## 2026-10-17 추가 공격적 H1 3안 — 아래는 당시 계획, 최신 수신 상태는 다음과 같음

2026-10-18 갱신: 후보1은 [OFFICIAL fresh3K 학습 완료](../../../research/experiments/h1/exp-h1-rotation-priority-tracking.md), 평가·보고서는 미수신이다. 후보3도 OFFICIAL fresh3K 학습과 PERSONAL model2850 평가가 완료됐고 [보고서 수신/HOLD](../experiments/h1/analysis/2026-10-18_H1_LIN075_ACTION0001_MODEL2850_POLICY_REVIEW.md)다. 아래의 후보1·3 PLANNED/미수신은 작성 당시 상태이며 현재 상태가 아니다. 새 실행·승격은 승인하지 않는다.

**목적·현재 상태:** 사용자 재확인에 따라 아래 세 설정과 fresh3K 공통 조건을 유지한다. **후보2는 실제 OFFICIAL fresh3K COMPLETED/exit0/PASS와 PERSONAL model2850 6영상·full 평가 수신을 확인했다.** [Run·최신 keeper2950과의 구분·원본 Release](../../../research/experiments/h1/exp-h1-joint-tracking-posture-relaxation.md). [정책 보고서도 수신 완료/HOLD](../experiments/h1/analysis/2026-10-17_H1_JOINT_TRACKING_POSTURE_MODEL2850_POLICY_REVIEW.md)다. 생존에도 H1/H3 후진 성분과 H5 지속 속도 손실이 남으며 기존 JOINT5K와의 차이는 학습량·다중 변경의 한계를 가진다. 후보1·3은 evidence 미수신/PLANNED이며 새 submission preset은 없다. 최초 작성 때 대기였던 JOINT fresh5K의 [보고서는 이후 수신 완료/HOLD](../experiments/h1/analysis/2026-10-17_H1_JOINT_TRACKING_MODEL4950_POLICY_REVIEW.md)다. 당시 **탐색 우선순위는 2번 → 3번 → 1번**이었으며 아래 번호는 사용자 후보 번호이지 새 legacy H-ID나 성능 순위가 아니다. 후속 실행 승인·분석·채택을 자동으로 뜻하지 않는다.

- 공통 기준: frozen `h1-submit-2`; **OFFICIAL 예정, fresh/no parent, 각 3,000 iterations, 4,096 env, seed42, save_interval50**. 각각 checkpoint를 불러오지 않고 처음부터 시작하는 독립 Run 설계다. 실행 간 resume/공유 checkpoint 없음. 표에 없는 모든 활성 reward 및 task/env/agent/PPO는 실제 preset 기준 유지. 새 공식 서버의 운영진 baseline이 자동으로 `h1-submit-2`인 것은 아니므로 termination=-50과 나머지 목표값까지 실제 reward와 대조해야 한다. 이 문서만으로 공식 서버 source·bootstrap·runner를 확인했다고 간주하지 않는다.
- 기준점 9개: `track_lin_vel_xy_exp=0.50`, `track_ang_vel_z_exp=0.50`, `feet_air_time=0.20`, `termination_penalty=-50`, `flat_orientation_l2=-1.5`, `ang_vel_xy_l2=-0.05`, `joint_deviation_hip=-0.2`, `joint_deviation_torso=-0.1`, `action_rate_l2=-0.0005`. 이는 목표 설계의 변경 가능 축 확인용이며 완전한 resolved native config가 아니다.

| 사용자 후보 번호 / 질문 | **최종 preset-relative override** (나머지 reward 유지) | 주된 기대 신호 | 주요 반증·위험 / 기존 evidence |
| --- | --- | --- | --- |
| **1. 회전 추종 강화형** — 선형·yaw 추종의 균형을 강한 yaw 보상과 중간 action-rate로 얻는가? | `track_lin_vel_xy_exp=0.55`, `track_ang_vel_z_exp=0.75`, `action_rate_l2=-0.0003` | H4 yaw 오차 감소, H1 정지 누수와 H5 rough 진행의 허용 가능한 trade-off | ANGTRACK-065 OFFICIAL fresh3K는 H4 yaw 이득에도 H3 15/384 첫 시도 접촉 종료·횡추종 손실로 HOLD. 과거 H-002의 `ang=.75` PERSONAL BASE 1K는 terrain0/contact100%로 REJECT였으나 **같은 preset/조합의 검증은 아님**. [관련 분석](../../../research/experiments/h1/exp-h1-angular-tracking-boost.md) · [H-002](../../../research/experiments/h1/H-002.md) |
| **2. 자세·고관절 제약 완화형** — joint 3중 조합의 제약을 줄이면 움직임·회복 여유가 커지는가? | `track_lin_vel_xy_exp=0.65`, `track_ang_vel_z_exp=0.60`, `action_rate_l2=-0.0003`, `flat_orientation_l2=-1.0`, `joint_deviation_hip=-0.1` | H5 지형 진행/꼬리 및 H7 회복 개선, 추종과 생존 유지 | ORIENT-100 단독 fresh3K는 H5 진행을 높였으나 자세 roll/pitch RMS와 H1 정지 누수가 악화되어 HOLD. 과거 H-003은 hip+torso 완화의 **다른** PERSONAL 1K 조합이며 미검증 교호작용. [ORIENT 분석](../../../research/experiments/h1/exp-h1-rough-terrain-orientation-relaxation.md) · [H-003](../../../research/experiments/h1/H-003.md) |
| **3. 전진 돌파형** — 강한 선형 추종과 약한 action-rate 규제로 rough 진행 상한을 높이는가? | `track_lin_vel_xy_exp=0.75`, `track_ang_vel_z_exp=0.50` (**preset 유지**), `action_rate_l2=-0.0001` | H2 선형 추종·H5 진행 평균/P05/최악 꼬리 개선 | H1/H3 비의도 전진 증가, H4 yaw 손실과 낙상 위험. 기존 `ACTRATE=-.0001` fresh3K는 rough 이득과 정지 누수가 함께 있었으며, `LINTRACK=.75`의 과거 PERSONAL 실험은 yaw/contact/terrain trade-off 및 계보 차이가 있다. [기존 ACTRATE 기록](../../../research/experiments/h1/exp-h1-action-rate-relaxation.md) · [H-008](../../../research/experiments/h1/H-008.md) |

### 최신 JOINT 분석을 반영한 검토 — 2 → 3 → 1

- **2번 우선은 합리적이다.** 실제 JOINT4950은 3072/3072 생존했지만 H5 진행 평균/P05/최소가8.853/8.403/7.930m로 명령적분10m에 못 미쳤다. 같은 lin/ang/action 조합에서 자세·hip 제약을 덜어 진행 여유를 찾는 질문은 이 병목에 맞는다. 다만 제약이 원인이라는 증거는 없고, orientation 완화의 과거 자세 RMS·정지 누수 악화와 hip 완화의 작은/미확정 이득을 감수하는 **조합 탐색**이다. 두 penalty를 함께 바꾸므로 각각의 효과는 분리되지 않는다.
- **3번은 다음 공격적 대안이다.** 선형 추종과 action 완화를 통해 H2/H5 진행을 노리지만 정지·횡이동 비의도 전진, yaw 손실, 거친 행동이 커질 수 있다. 명령보다 많이 움직이거나 전진량만 증가한 것을 추종 개선으로 세지 않는다.
- **1번은 후순위다.** 기존 ANGTRACK-.65가 yaw 이득과 H3 접촉 종료/추종 손실을 함께 보였으므로 ang=.75에 더 올리는 것은 세 안 중 yaw 특화 위험이 크다. 다만 다른 reward 조합의 과거 실패로 이번 설정의 실패를 확정하지는 않는다.
- **3K는 이번 후보 탐색의 판단 시점이지 최적 성능 보장이 아니다.** 2번과 기존 JOINT5K는 다른 학습량이므로 단순 차이로 orientation/hip 효과를 확정하지 않는다. 동일 학습 seed42나 동일 평가 cohort 키도 독립 학습 반복·동일 실제 지형을 보증하지 않는다. 좋은 후보가 나오더라도 자동 +2K·자동 제출하지 않는다.

**비교·판정:** 1번의 주 질문은 H4 yaw 개선이고 H3 추종/접촉 및 H5 진행을 보호 지표로 본다. 2/3번의 주 질문은 H5 속도오차·진행 평균/P05/최소/stall이며 H1 정지, H3 vy/비의도 vx/접촉, H4 yaw, H6 경사와 H7 회복·생존을 함께 확인한다. H3 world 종료 잔류는 보조 지표이지 원점복귀 명령의 실패가 아니다. 제출된 기존 정책과 당일 JOINT fresh5K keeper `model_4950.pt`(SHA `2df05840…62bc478`)를 참고군으로 두고, auto-best4800 및 이전 LINTRACK0654950(`b7528923…`)과 구분한다. 새 후보도 실제 보존된 final numbered checkpoint를 SHA로 고정한다. 학습량3K 대5K·복수 reward 변경·평가 protocol·source/seed 차이를 명시한다. 전체 reward·terrain·생존 하나만으로 우승/공식 점수를 예측하지 않으며, 주 지표 이득과 동시에 정지/추종/생존이 악화하면 trade-off/HOLD로 기록한다. 개별 reward 인과효과를 검증하는 설계는 아니다.

**시간·운영:** 1K는 import/load·NaN·치명 붕괴의 screening 지점일 뿐 정상 후보의 순위/제출 판정 지점이 아니다. 3K 이후 자동 +2K·무한 resume·후속 평가·제출은 승인에 포함하지 않는다. 실제 서버의 활성 reward `show/diff`, CLI/README, 실제 경로와 `--preflight-only`를 확인하고 같은 인자의 승인된 `issacsimz_tmux_train.sh` 흐름으로만 학습한다. 종료 exit code, 전체 resolved config, lineage, numbered checkpoint, evidence와 실패 자료를 보존하며 서버 종료를 수행하지 않는다. **새 가설을 문서화한 것만으로 세 Run을 모두 학습하라는 뜻은 아니다.**

## 1. 지금 바꿀 방향

### 2026-10-17 판단 목표와 다음 질문 구분

- **공식 제출 경쟁력과 광의의 보행 능력을 분리한다.** 현재 H1 공식 7개 시나리오는 제자리 균형·전진·좌우·회전 복합·약한 요철·±10° 경사·밀침 회복이다. 계단·박스 영상은 보조 행동 자료이며 중앙 완주 미입증을 기록하되, 그 공백만으로 H1 공식 후보를 자동 REJECT하지 않는다. 보조 영상 실패도 숨기지 않고 해당 목표의 한계로 남긴다.
- **개선 정체의 범위를 먼저 정한다.** 내부 행동 지표의 개선·손실, 공식 제출 점수 변화, reward 효과의 재현성은 다른 주장이다. 최근 모든 후보가 HOLD라는 사실만으로 학습 전체가 무의미하거나 더 학습하면 반드시 좋아진다고 결론내리지 않는다. 로컬 순위는 공식 점수 예측이 아니다.
- **다음 Run은 질문 하나를 고른다.** reward/config 탐색은 설정 간 trade-off, 독립 학습 seed 반복은 같은 설정의 재현성, 고정 설정의 추가 학습은 학습량·후반 안정성, reward 전환 resume는 학습 경로를 묻는다. 평가 seed 여러 개는 독립 학습 반복이 아니다. 기존 결과로 답할 수 있는 질문은 다시 GPU 작업으로 만들지 않는다.
- **무기한 resume·공격적 다중 변경·촘촘한 미세 sweep을 기본 해법으로 두지 않는다.** resume 전략은 유지하되 시작 checkpoint·추가 학습량·비교 대상·판단 시점을 먼저 정한다. 기존 PLANNED 후보는 보존하며 이번 원칙 정리로 새 실행이나 후보 승격을 승인하지 않는다.

근거: [H1 공식 시나리오 기록](../experiments/h1/analysis/2026-09-10_OFFICIAL_EVAL_H1_ROUND2_TERM50.md), [현재 제출·Run registry](../../../research/EXPERIMENTS.md), [로컬 평가의 역할·조건](../ai_library/21_WINDOWS_GO2_VIDEO_AND_EVALUATION.md), 아래 1차 연구 검토. 연구 결과는 특정 reward 값이나 우리 다음 정책의 개선을 보증하지 않는다.

**부모2700에서 벌점/추종 가중치를 하나씩 더 바꾸는 +2K 가지치기를 무조건 계속하지 않는다.** 부모2700은 rough가 좋은 *관측된 checkpoint*이지 공식 점수나 전 시나리오 우승의 증거가 아니다. 무변경 연장도 rough가 떨어졌고, lin=.55/.65는 회복과 yaw/lateral 비용이 공존하며, angxy=-.08은 rough 꼬리와 자세/횡속도 개선을 함께 달성하지 못했다. 더 오래 학습하거나 “중간값”을 고른다고 자동 해결되지 않는다.

따라서 **새 후보 탐색이 목적이라면** 전역 body-rate 벌점 강화 반복보다 action regularization의 fresh 균형 확인을 제안한다. 기존 이득이 재현되는지를 묻는 목적이라면 독립 학습 seed 반복이 먼저다. 둘은 다른 질문이며 아래 순서는 개선 확률의 통계적 순위가 아니다. 여러 새 보상을 동시에 바꾸지 않고, 정지/전진/좌우/회전/rough를 함께 본다. resume는 버리지 않되 동일 부모의 동일 길이 대조가 질문에 맞을 때 사용한다.

이번 CPU 확인으로 angxy의 부모/무변경 비교는 끝났다. 같은 비교를 또 분석 대기로 되돌리지 않는다. source/PPO·checkpoint 선택·단일 학습 seed 한계 때문에 보상 단독 인과는 여전히 미확정이다.

## 2. 연구·공식 구현에서 확인한 것과 적용 한계

조회일 2026-10-16. 아래는 1차 논문/저자 코드이며 블로그의 추천 weight를 최적값처럼 가져오지 않았다. Rudin 본문 §2.2·3.1·3.2(PDF3–5쪽)와 저자 코드, Eimer 본문 §4·4.2·부록A(PDF4–5·14쪽)를 확인했다. Agarwal·Nikishin은 출판사/arXiv 초록 범위에서만 사용하며 세부 실험을 재현했다고 하지 않는다.

| 근거 | 확인한 내용 | 이번 설계에 반영 | 이 근거가 **증명하지 않는 것** |
| --- | --- | --- | --- |
| Rudin et al., *Learning to Walk in Minutes* (CoRL2021, arXiv v3 2022), [논문](https://arxiv.org/abs/2109.11978), [저자 코드](https://github.com/leggedrobotics/legged_gym/blob/master/legged_gym/envs/base/legged_robot.py) | 병렬 locomotion·terrain curriculum의 중요성. 저자 `_reward_tracking_lin_vel`, `_reward_ang_vel_xy`, `_reward_action_rate` 함수 직접 확인 | 추종, XY body 각속도, action 차이는 서로 다른 목표다. 총 reward만으로 우승 판단하지 않음 | ANYmal 결과가 H1 최적 weight를 주지 않는다. OFFICIAL curriculum/PPO 변경 권한도 주지 않음 |
| Eimer et al., ICML2023, [*Hyperparameters in RL and How To Tune Them*](https://proceedings.mlr.press/v202/eimer23a.html) | tuning seed에 민감한 hyperparameter landscape와 tuning/test seed 분리 권고 | 탐색 seed42에서 좋아 보인 값은 보류 학습 seed에서 확인. 평가 seed 3개를 학습 반복으로 세지 않음 | -.0003이 최적이라는 근거가 아니며 논문의 broad HPO를 공식 서버 자동 탐색 허가로 확대하지 않음 |
| Agarwal et al., NeurIPS2021, [*Deep RL at the Edge of the Statistical Precipice*](https://arxiv.org/abs/2108.13264) | 소수 training-run의 점추정과 aggregate 순위가 불확실할 수 있음 | 축별·seed별 결과와 한계를 보존. 384 env의 승패 수를 독립 학습 유의성으로 바꾸지 않음 | H1에 필요한 최소 seed 수나 .02 공식 점수 차이의 원인을 정해주지 않음 |
| Nikishin et al., ICML2022, [*The Primacy Bias in Deep RL*](https://proceedings.mlr.press/v162/nikishin22a.html) | 과거 경험에 편중되는 RL 학습 경로 문제와 별도 실험의 reset 방법 | 같은 최종 reward라도 fresh/resume는 다른 질문임을 유지 | 현재 PPO resume 손실을 primacy/forgetting으로 확정할 수 없음. network reset/optimizer 수정은 이번 규정 범위 밖이며 권고하지 않음 |

저자 legged_gym 코드는 body XY 각속도 제곱과 action 간 차이 제곱을 구분한다. 하지만 **프로젝트의 실제 수식은 보존된 IsaacLab source/실행 resolved config가 우선**이다. reward 이름/weight만 같다고 upstream 최신 구현과 동일하다고 하지 않는다. `roll_pitch_rms`는 기울기 각도이고 body-rate penalty의 직접 측정량이 아니며, 최종 world 복귀도 body-frame 속도 명령의 직접 목표가 아니다.

Rudin의 지형별 curriculum은 학습 분포가 계속 달라질 수 있다는 해석 근거이지, 이번 서버에서 curriculum을 수정하자는 제안이 아니다. Eimer의 평균적 hyperparameter landscape가 비교적 매끄럽다는 결과 역시 **우리 reward 계수의 단조성·중간값 우위**를 증명하지 않는다. 논문의 튜닝/검증 seed 분리는 참고하되 권장 seed 수를 이번 대회의 의무 GPU 예산으로 그대로 옮기지 않는다.

## 3. 실행 전 설계 기록 — action=-.0003 fresh 3K (현재 완료/HOLD)

**질문:** 강한 action 평활화(-.001)와 약한 평활화(-.0001)의 기존 행동 비용 사이에서, 중간 강도의 고정 config를 fresh로 학습하면 rough 진행을 보존하면서 정지 누수·H3·yaw를 균형 있게 만들 수 있는가?

- 기반 preset: `h1-submit-2`; 최종 override **`action_rate_l2=-0.0003`만**. 이는 기존 보고서의 미선택 제안을 현재 결과로 재우선순위화한 것이며 새 성공 사실은 아니다.
- **fresh/no checkpoint, 3000회, seed42, 4096env** 제안. 부모2700에서 -.0003으로 resume한 Run과 혼동하지 않는다. fresh는 baseline reward로 복원한다는 뜻이 아니다.
- 목표 9개 변경 가능 값: lin=.5, yaw-track=.5, feet=.2, termination=-50, orientation=-1.5, body-angxy=-.05, hip=-.2, torso=-.1, action=-.0003. 나머지 활성 reward·agent/env/PPO는 기준 그대로다. 현재 서버 전체 reward·source를 확인하기 전 명령을 확정하지 않는다.
- 선택 이유: 기존 action=-.0001 fresh3K는 rough가 강하지만 정지 누수가 컸고, action=-.001 fresh3K도 누수·H3 문제가 남았으며, -.0005로 복원한 resume는 rough 최악 꼬리가 커졌다. **-.0003의 이득은 알려져 있지 않지만**, global body-rate 강화 반복보다 action 자유도/평활화의 균형이라는 명확한 질문을 직접 검증한다. 기존 계수별 정책은 학습 경로·checkpoint 선택이 달라 이 관측을 dose-response 곡선이나 중간값 최적성의 증거로 해석하지 않는다.
- **왜 resume -.0003이 1순위가 아닌가:** 같은 부모 unchanged/복원 대조를 재사용해 1K 절약할 수 있으나, 최근 모든 +2K의 학습 경로·선택 checkpoint 효과가 얽혀 있다. 다음 공식 fresh 설정을 고르는 목적에는 fresh 질문이 더 직접적이다. resume 전략 일반을 폐기하는 판단은 아니다.
- **3K→무조건5K 금지:** 1K는 치명 붕괴 screening만, 3K에서 기존 후보 대비 경쟁력·안정성이 확인된 경우에만 별도 승인으로 5K. 무조건 5K 예산이 있다면 단순 연장보다 대조/독립 seed 확인의 정보가치를 먼저 고려한다.

단일 fresh Run으로 보상 효과를 증명하지 않는다. 1차 reference는 기존 TERM-50/action=-.0005 fresh3K model2800 및 ACTRATE/action=-.0001 fresh3K model2700이고, source/PPO/환경·학습량/선택 역할 차이를 명시한다. 공식 서버 배포 source가 달라졌다면 이를 matched reward pair라 부르지 않는다.

## 4. 후속 후보의 조건부 우선순위

| 우선순위 | 질문 / 설계 | 지금보다 이득인 이유·대기 이유 |
| --- | --- | --- |
| **완료/HOLD** | `h1-submit-2 + action=-.0003`, fresh3K | 위 실제 Run·보고서 확인. 후속 비교와 채택은 별개이며 같은 실행을 다시 권고하지 않음 |
| **재현성이 목적이면 1순위** | 유망한 기존 fixed config를 fresh로 독립 학습 seed에서 반복 | 새로운 knob보다 관측 이득의 재현성 확인. 선택 후보와 대조 조건을 먼저 고정하며, 학습 seed는 평가 seed와 별도 |
| **3 비용 절약 대안** | 같은 부모2700에서 action -.0001→-.0003, +2K | 기존 unchanged/복원 sibling을 이용한 경로 질문. fresh 후보 선택과 섞지 않음; 새 child에서 다시 resume 금지 |
| **대기 유지** | 기존 `exp-h1-action-first-airtime-switch`: 부모2700에서 feet .20→.25, +2K | 미실행 계획은 보존하되 신호가 약함. 기존 fresh action+feet=.25도 rough 평균7.826m·누수 때문에 HOLD라 우선순위 자동 승격 안 함; fresh와 resume를 같은 실험 결과로 취급하지 않음 |
| **지금 추가 안 함** | angxy 더 강화/더 긴 continuation, lin .56/.57 등의 연속 미세 sweep, 여러 reward 동시 변경 | 현재 비교가 이미 trade-off를 보여 다음 1 Run의 식별력이 낮음. 연구가 특정 계수의 개선을 보장하지 않음 |

새 proposal는 기존 Experiment `exp-h1-action-rate-relaxation`의 action 강도 질문 안에서 관리한다. fresh/resume는 각각 별도 Run/lineage이며, 실행 전 실제 Run ID를 만들지 않는다. 승인된 과거 계획을 삭제하거나 다른 설정으로 몰래 대체하지 않는다.

## 5. 판정·중단·예산

1. **primary:** H5 `vx_error`, body progress 평균/P05/최소와 stall. 진행이 커도 명령 초과면 추종 개선으로 보지 않는다. P05는 seed별도 확인한다.
2. **guardrails:** H1 zero-command `vx/vy`·world/절댓값 body 누수, H3 `vy_error`/비의도 vx, H4 yaw, H6 진행·각도/action Δ, H7 push. world H3 종료 거리 하나만으로 순위 정하지 않는다.
3. **공식과 분리:** H1 R2/R4 56.37, R6 56.35라는 사용자 전달 점수는 이전 제출 actor의 결과다. Go2 운영진 답변의 Survival×Tracking 분해는 중요한 판단 구조지만 H1 미공개 component 값을 만들어 채우지 않는다. 내부 mixed-unit 총점을 공식 예상 점수로 만들지 않는다.
4. **사전 수치 gate를 날조하지 않음:** 손실을 숨기지 않는 축별 비교와 기존 후보 대비 경쟁성으로 판단한다. 반복 후에도 엇갈리면 Pareto 후보로 남기고 “안정성 때문에 무조건 채택”하지 않는다.
5. **선택 후에만 실행:** 활성 allowlist 숫자 weight만 변경. OFFICIAL terrain/command curriculum, PPO, network reset, 새로운 reward 활성화/비활성화·Optuna 설치/원격 제어는 하지 않는다. 개인 PC Optuna는 승인된 비교/objective 전 Tell 차단 유지.
6. 장기 작업은 기존 `issacsimz` tmux/evidence/keeper 경로를 사용. final native checkpoint 기본, auto-best 과신·checkpoint 토너먼트 없음. OFFICIAL 종료는 AI 권한 밖이다.

**지금 완료한 것:** 새 원문 보존, raw CPU 비교, 문헌·구현 확인과 계획 갱신. **하지 않은 것:** 새 GPU·재렌더·학습·실제 Optuna Ask/Tell·서버 조작·제출.

## 6. 선택 가능한 가설 후보장

아래 첫 번째 **action=-.0003 fresh는 완료/HOLD**, 나머지는 미실행 제안이다. 여섯 개를 한꺼번에 돌리는 batch가 아니며 미실행 후보의 실제 Run ID를 미리 발급하지 않는다. 결과와 질문에 따라 불필요한 후속은 건너뛴다. 표시명은 질문을 기억하기 위한 설명이고 새 H/HS 번호나 canonical config ID가 아니다.

| 가설 / 검증할 질문 | 설정·시작점·예산 | 비교 대상 | 지지 신호 / 중단·보류 근거 |
| --- | --- | --- | --- |
| **action 중간 강도 fresh** — 움직임 자유도와 평활화 사이에 더 나은 균형이 있는가? | `h1-submit-2 + action_rate_l2=-0.0003`, **fresh3K**, seed42/4096env. 다른 reward 유지 | 기존 action=-.0001 fresh3K와 -.0005 TERM-50 fresh3K | H1 정지 누수·H3 vy·H4 yaw 개선과 H5 진행/꼬리 보존을 함께 확인. 정지만 좋아지고 rough가 손해면 범용 승격 보류 |
| **약한 중간 강도 fresh** — -.0003이 진행을 과도하게 제약한다면 -.0002가 교환비를 줄이는가? | `h1-submit-2 + action_rate_l2=-0.0002`, **fresh3K**, seed42/4096env | -.0003 fresh와 기존 -.0001 fresh | **-.0003에서 누수 개선·rough 손실이 함께 나온 경우에만** 후속 후보. -.0003이 전반적으로 나쁘거나 동등하면 자동 미세 sweep하지 않음. -.0002 우위 근거는 아직 없음 |
| **action 중간 강도 전환** — 이미 익힌 진행성을 유지하면서 평활화만 보완할 수 있는가? | 검증된 ACTRATE 부모2700에서 action **-.0001→-.0003**, resume **+2K**, seed42/4096env | 같은 부모 unchanged4699 및 -.0005 복원4650; fresh -.0003은 학습 경로 참고 | unchanged보다 H1/H3/yaw가 개선되고 H5 P05·최소가 유지되는지 확인. fresh3K와 총 학습량·초기 정책이 달라 순수 schedule 인과로 해석하지 않음 |
| **기존 airtime 전환** — 후반 발 체공 보상만 올리면 보행 습득 후 장애물 대응이 달라지는가? | 기존 `exp-h1-action-first-airtime-switch`: 부모2700, **feet .20→.25**, action=-.0001 유지, resume **+2K** | 동일 부모 unchanged4699; 이미 완료된 fresh action+feet=.25는 별도 경로 참고 | H5 진행/추종과 H3·H4·정지 누수를 함께 확인. 계단 영상은 실제 중앙 다단 통과가 보여야 별도 지지 근거. fresh 조합 HOLD를 근거로 resume 성공·실패를 미리 확정하지 않음 |
| **action 후보 재현성** — 현재 장점이 seed42의 우연인가? | 먼저 고정한 후보 config를 **fresh3K, 학습 seed43**, 4096env. reward는 변경하지 않음 | 같은 config의 seed42 Run; 평가는 기존 동일 protocol·평가 seed 사용 | rough·누수·vy·yaw의 trade-off 방향이 반복되는지 확인. 이것은 새 reward 가설이 아니라 재현성 가설이며 seed 두 개만으로 안정적 우승을 확정하지 않음 |
| **유망 fresh의 무변경 장기화** — 3K의 균형이 추가 학습에서도 유지되는가? | **경쟁력 있는 새 fresh3K가 나온 경우에만**, 그 Run의 실제 final checkpoint에서 reward unchanged **+2K** | 동일 Run의 3K 정책과 새 5K 정책 | late terrain/tracking/contact와 행동 guardrail이 유지·개선되는지 확인. 새 child를 또 이어 7K로 만드는 계획은 아님. 단순 추가 학습 효과와 reward 효과를 구분 |

### 실행 순서 제안

**새 값을 찾을 때:** 완료된 action=-.0003 fresh3K의 HOLD·trade-off를 먼저 읽고, -.0002 탐색 또는 고정 후보의 독립 학습 seed 확인 중 어느 질문을 풀지 선택한다. -.0002 우위는 미확정이며 자동 다음 Run이 아니다. 충분히 경쟁력 있는 후보만 무변경 +2K를 검토한다. 후속을 자동으로 모두 실행하지 않는다.

**resume 질문을 먼저 풀고 싶을 때:** action=-.0003 전환 또는 기존 airtime 전환 중 하나를 고른다. 서로 다른 child가 아니라 같은 검증 부모2700에서 직접 분기한다. 비용 절약과 다음 OFFICIAL fresh 설정 선택은 다른 목적이다.

**이번 결과로 우선순위를 낮춘 것:** angxy 추가 강화, 무조건 더 긴 부모 연장, 여러 reward 동시 변경. 이는 영구 금지가 아니라 현재 근거에서 다음 한 Run의 질문이 덜 명확하다는 판단이다. 모든 후보의 실제 서버 설정·checkpoint 경로는 실행 시 확인하며 여기서 추측해 명령으로 채우지 않는다.
