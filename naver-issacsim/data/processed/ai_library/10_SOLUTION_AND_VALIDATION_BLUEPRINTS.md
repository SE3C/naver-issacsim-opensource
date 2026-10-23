---
title: "솔루션·검증 청사진"
purpose: "AI upload bundle — 정책 선택과 본선 전략을 위한 권장 개발 순서"
sources:
  - "data/processed/server_backup/reports/"
  - "data/processed/planning/historical/04_OPTUNA_REWARD_SEARCH_DESIGN.md"
  - "data/processed/planning/historical/07_H1_SECOND_RUN_PARAMETER_COMPARISON_PLAN.md"
  - "data/processed/experiments/h1/training/2026-08-24_OFFICIAL_SERVER_300ITER_BASELINE.md"
  - "data/processed/external_analysis/video_reports/03_100_hour_workflow_hGbBn5xliyg.md"
  - "data/processed/external_analysis/video_reports/05_preliminary_participation_r4Zq8wQdk1Y.md"
  - "data/processed/incoming/other/reviewed/NCRC_H1_EXTERNAL_INTERNAL_SINGLE_DELTA_ANALYSIS_20260923.md"
  - "data/processed/incoming/other/reviewed/NCRC_H1_VISUAL_FAILURE_DEEP_ANALYSIS_20260923.md"
  - "data/processed/incoming/other/reviewed/자동평가_Tracking_Survival_구조_분석보고서_20260924.md"
type: "recommendation"
---

# 솔루션·검증 청사진

## 2026-10-11 ACTRATE-001 / model_2850에서 재확인한 정책 선택 기준

[2026-10-10 원문 분석](../incoming/other/reviewed/H1_MODEL2850_SHA1E6D_POLICY_ANALYSIS_20261010.md) · [2026-10-11 정책 검토](../experiments/h1/analysis/2026-10-11_ACTRATE001_MODEL2850_POLICY_REVIEW.md) · [Experiment](../../../research/experiments/h1/exp-h1-action-rate-smoothing.md). OFFICIAL fresh3K `ACTRATE-001` best checkpoint SHA `1e6d…bb1`의 Windows PERSONAL 3,072 episode는 모두 20초 생존했다. 하지만 H1 제자리 world XY 순변위 평균 **1.151m**, H3 횡왕복 잔류 **2.177m**, rough H5 P05 body 진행 **8.921m**와 계단 중앙 통과 미입증이 남았다. 이동 능력은 H2/H7 body 전진 **15.470/10.656m**, H6 경사 **20.297/20.058m**로 관찰됐다. 따라서 **HOLD**: survival, 정지 위치 제어, lateral 복귀, terrain worst-tail, yaw/action 비용, 계단 영상 검증 범위를 서로 분리하여 채택한다.

`ORIENT-100/model_2850`은 SHA `6aed…f7b0`의 다른 정책이다. 먼저 기존 `TERM-50/model_2800` 동일 evaluator 원자료의 protocol/source/PPO/seed/terrain/command parity를 확인하고 대응 cohort를 비교한다. 이번 기록은 제공 원문 분석 반영이지 새 GPU 실행·matched A/B 완료·인과 입증·공식 채점이 아니다.


## ORIENT-100 사례로 보강한 실제 채택 기준 (2026-10-07)

`ORIENT-100 / model_2850`의 Windows PERSONAL H1 `scenario7` full에서는 3,072/3,072개 episode가 모두 timeout 생존했지만, 정지 명령에서도 body 전진 적분 **+1.633m/20초**, 순수 lateral에서도 **+1.180m**가 발생했다. rough H5 평균 tracking error는 **0.1709**, 진행 **최소 7.831m / P05 8.863m**다. 즉 **생존률 100%는 정지 유지·경계 지형의 진행·worst-case tracking을 대체하지 못한다.** tracker의 정지 H1 `stall=0`도 분모에 speed-command step이 없어 위치 유지 성공을 뜻하지 않는다.

실무 평가 표에서는 생존, 목표별 몸체 전진/횡이동 및 world 이동의 정의, 명령별 tracking, rough **P05 진행·P95 오차·stall**, yaw/action smoothness, 발/단차가 동시에 보이는 영상의 계단 접촉을 분리한다. 다만 `forward_progress_m`와 `integrated_body_forward_m`는 동일 필드의 중복 기록이고 `lateral_drift_m`는 `|Δvy|` 적분이지 실제 세계좌표 횡변위가 아니다. 6영상의 대부분 후반은 지형 패치 밖 평지이며 `02_inverted_stairs.mp4` 검정 교대 프레임은 캡처 결함이다.

이 후보의 **HOLD**는 단일 정책 보행 능력 부정이 아닌 **동일 `h1-submit-2 / TERM-50` protocol 대조 부재**에 따른 정책 승격 보류다. 새 GPU 실행 전에 보존된 baseline 평가 원자료를 먼저 찾는다. [원문 분석](../incoming/other/reviewed/H1_ORIENT-100_POLICY_ANALYSIS_20261007.md) · [Experiment](../../../research/experiments/h1/exp-h1-rough-terrain-orientation-relaxation.md).



## 2026-09-30 evaluator 구현 상태

2026-10-06 현재 H1용 PERSONAL evaluator의 공용 core를 재사용하는 Windows 통합 launcher가 `C:\NCRC\h1_6terrain_video.bat`로 설치됐고 CPU 회귀 테스트 60개와 PowerShell/설치 파일 검증을 통과했다. H1은 경사 ±10°의 고정 6영상 뒤 별도 camera-off `scenario7` 8 case 전체 평가를 사용하며 standalone/integrated smoke 옵션은 제거됐다. 다만 **2026-10-06 설치 검증 당시 H1 GPU full은 없었으나, 2026-10-07 `ORIENT-100 / model_2850`의 PERSONAL full 자료가 확보됐다. paired comparison은 여전히 미실행이다.** 아래의 평가 harness 설계는 현재 구현의 목적과 해석 경계를 설명하는 청사진이며, 실제 H1 후보 비교는 동일 조건 baseline 자료가 생기기 전까지 보존 TensorBoard·console·checkpoint provenance와 native play 영상에 대한 AI 분석으로 수행한다. 영상은 command·terrain instance·초기 상태가 matched되지 않으면 정성 근거로만 쓴다.

따라서 다른 문서의 `PROMOTE to fixed paired evaluation`은 "설치·CPU 검증된 평가기로 향후 GPU full/paired 검증할 후보"라는 상태이지, 이미 H1 내부 evaluator 점수를 얻었다는 뜻이 아니다. 공식 NCRC 점수는 실제 제출 후 운영진 평가로만 확정한다.

## 전제

이 문서는 공식 규정이 아니라 개발 권장안이다. 개인 서버에서는 정책을 새로 학습해 제출하지 않고, 공식 서버에서 만든 산출물을 **재현·관찰·비교**하는 데 쓴다.

## 우선순위

1. 제공 환경과 코드·파일 구조를 이해한다.
2. H1·Go2의 baseline을 각각 학습하고 play 영상으로 기준 행동을 남긴다.
3. 명령 추종·회전·정지·지형 전환·외란 회복을 분리한 평가 harness를 만든다.
4. reward 가설을 하나씩 실험하고 결과를 표준 로그로 저장한다.
5. 내부 점수보다 영상·안정성·재현성을 함께 봐 제출 후보를 고른다.
6. 본선은 고정 전략 → 규칙 기반 전략 → 필요 시 제한된 LLM 순으로 확장한다.

## 팀 연구 운영 루프

공식 운영 영상은 팀 작업을 `정책 학습`, `로그 진단`, `전략문`, `기록·운영`으로 나누고, 첫 한 바퀴는 팀원이 전체 흐름을 함께 경험한 뒤 주담당을 나누는 방식을 제시한다. 이는 의무 역할명이 아니라 중복 작업과 서버 방치를 줄이기 위한 운영 모델이다.

모든 실험은 서버를 켜기 전에 질문·단일 변경·명령·종료 조건·필요 산출물을 적고, 실행 후 로그·행동·결론·다음 질문을 기록한다. 영상이 설명한 연구 루프는 다음과 같다.

```text
질문 → 실험 → 확인 → 기록 → 다음 질문
```

## 최소 평가 세트

| 범주 | 확인할 질문 |
| --- | --- |
| 속도 추종 | 전후·측면·회전 명령을 과도한 진동 없이 따르는가? |
| Stop & Go | 멈춤과 재출발에서 넘어짐·과도한 관성이 없는가? |
| 지형 | 평지 성능을 잃지 않고 요철·경사·계단을 통과하는가? |
| 회복 | 외란 뒤 안전하게 다시 서고 목표를 재개하는가? |
| 재현성 | 같은 후보가 반복 실행에서 비슷한 행동을 내는가? |
| 보행 품질 | 생존·전진 중에도 한 발 지지, hop/skip, 교차 보폭, 큰 몸통 진동이 지속되지 않는가? |

예선 안내 영상의 `생존율 × 추종 점수`는 공식 평가 방향을 이해하기 위한 참가자용 설명이다. 개인 evaluator는 이를 참고할 수 있지만, `Robust Proxy Score`나 내부 지표를 공식 채점식으로 부르지 않는다.

### 제공된 운영진 공개 답변의 Tracking·Survival 구조 — 2026-09-26 갱신

[1차·추가 답변 정리본](../incoming/other/reviewed/01_운영진_자동평가_Tracking_Survival_공개답변_20260926.md)에 따르면 매 step의 몸통 기준 `vx`, `vy`, yaw-rate 오차를 **별도 단위·범위 정규화 없이** 하나의 Euclidean 크기 `sqrt(Δvx²+Δvy²+Δyaw²)`로 합친다. 수치상 선속도 `1 m/s` 오차와 yaw 각속도 `1 rad/s` 오차가 같은 크기로 들어가며, 목표가 0인 축의 흔들림도 포함한다. 이 오차를 episode 내부에서 단순 평균하고, **길이와 무관하게 각 episode의 평균 오차를 같은 비중으로 다시 평균한 다음** 비공개 함수로 Tracking Score를 정한다. episode마다 점수를 먼저 산출해 평균하는 방식은 아니다. 출발·10초 명령 재생성 직후·낙상 전 구간 모두 평가하며 순간 최대 오차에 별도 추가 가중치를 주지 않는다.

Survival은 **episode 수가 분모**다. 몸통 바닥 접촉 종료는 실패, 제한시간 도달과 평가 종료 시점의 비낙상 진행은 생존이다. 같은 로봇의 반복 낙상은 매번 새로운 실패 episode가 된다. 모든 제출은 같은 seed로 평가하지만 정책마다 낙상·reset 시점이 달라 이후 명령 sequence까지 완전히 같다는 뜻은 아니다. 따라서 짧은 실패 episode가 Tracking과 Survival 모두에 영향을 줄 수 있고, 고정 조건 내부 평가는 통합 3축 오차뿐 아니라 축별 오차·명령 전환·반복 낙상·실제 진행을 따로 기록해야 한다.

**미공개:** 전체 평균오차를 실제 Tracking Score로 바꾸는 함수, 시나리오별 구체적인 command 값. 제공된 문서는 공개 대화의 전사·정리본이며 원본 게시 화면이나 evaluator 코드를 이 저장소에서 독립 검증한 것은 아니다. 이를 공식 점수의 완전한 복제식으로 부르지 않는다. 이전 [2026-09-24 2차 분석](../incoming/other/reviewed/자동평가_Tracking_Survival_구조_분석보고서_20260924.md)에서 미확인으로 적었던 단위 정규화와 Survival 분모는 이번 [구조 분석](../incoming/other/reviewed/02_자동평가_Tracking_Survival_구조_분석보고서_20260926.md)의 제공 답변 내용에 따라 갱신한다.

### Go2 R3/R5 운영진 후속 답변 — 생존과 추종의 상쇄

[사용자 제공 운영진 DM](../experiments/go2/analysis/2026-10-08_GO2_R3_R5_OFFICIAL_SCORE_COMPONENTS_ORGANIZER_REPLY.md)은 공식 계단 survival **99.0%→99.8%**, Tracking Score **0.819→0.796**과 약 **+0.07/−0.24점**의 구성 기여를 설명했다. 계단 점수 **8.52→8.35**의 손실은 생존 악화가 아니라 추종 손실이 생존 이득보다 컸기 때문이다. 학습은 변하는 curriculum·행동 탐색 무작위에서 contact를 측정하고, 고정 공식 평가는 그 행동 무작위 없이 잰다. `1−학습 contact`를 공식 survival로 쓰지 않으며, 평가의 모든 무작위화가 꺼진다고 확대하지 않는다. 생존·추종·진행을 따로 보고 **개선된 생존을 유지하며 명령 추종 손실을 회복**하는 질문을 우선한다. 표시 정밀도·미공개 변환식 때문에 이 한 쌍으로 로컬 scorer를 공식식에 맞추지 않는다.

### 공개 실패 사례로 보강할 H1 진단

2026-09-22 공개 researchlog에서는 높은 terrain/reward에도 구덩이·틈·레일에서 실패한 기록과, 낙상률이 낮아도 지형 진행이 정체된 기록이 함께 나온다. 따라서 평가 결과표는 **공식 7시나리오와 특수 지형 stress check를 분리**하고, 각 지형에서 생존뿐 아니라 고정 명령에 따른 실제 전진 거리·traversal·XY/yaw 추종·낙상·정체 여부를 함께 기록한다. 공개 지형 이름이 공식 평가 지형과 동일하다고 가정하지 않으며, 외부 실패 빈도를 우리 정책의 실패 확률로 옮기지 않는다. 공개 자료의 구체적인 key와 내부 실험 우선순위는 `20_H1_PUBLIC_FAILURES_AND_EXPERIMENT_PRIORS.md`를 따른다.

9월 23일 별도 보고서의 20초 공개 클립 5건은 이 평가표에 **생존·진행·추종·보행 품질**을 따로 두어야 하는 구체적 장면을 제공한다. `reel-93039572`는 낮은 fall에도 계단 앞에서 정체하고, `reel-14106372`는 높은 reward·terrain에도 비대칭 hop/skip을 보인다. 내부 고정 평가에서는 `upright-but-stalled`와 abnormal gait를 실패 annotation으로 남기되, 카메라가 움직이는 클립에서 이동거리·낙상률·jitter 주파수를 역산하지 않는다. 이 영상은 외부 관찰이지 동일 조건 대조나 공식 채점 근거가 아니다.

## H1 초기 300회에서 얻은 역사적 교훈

첫 300회 H1 policy는 report상 terrain level 0.00과 fall rate 100.0%였다. 이 policy는 evaluator의 “명백한 실패를 낮게 평가하는가”를 점검하는 negative-control 후보로는 쓸 수 있지만, reward 최적화 baseline이나 Optuna trial로 쓰지 않는다.

300회 이후의 “더 긴 baseline 우선”은 당시 권고이며 현재 실행 명령이 아니다. **2026-10-06 ORIENT-100 OFFICIAL fresh 3K는 COMPLETE/PASS이며, 2026-10-07 PERSONAL 행동 진단은 HOLD**다. [접수 기록](../experiments/h1/training/2026-10-06_ORIENT100_OFFICIAL3K_EVIDENCE_INTAKE.md). ACTRATE-001은 frozen `h1-submit-2`에서 action=-0.001만 바꾼 별도 OFFICIAL fresh3K를 완료/PASS했고 model2850 PERSONAL 분석도 수납/HOLD다. ORIENT checkpoint/config를 상속하지 않았다. Go2 staged screening은 `07`의 1K→3K→5K를 따르고, 실제 evidence 절차는 `19`다. 학습량 효과와 reward 효과는 공통 시계열 조건을 확인한 뒤 구분한다.

단, 300회 초기 효과를 먼저 비교하려면 baseline 300회 재수집과 단일 reward 변경 300회를 같은 조건으로 짝지어 실행한다. 첫 변경 후보는 `termination_penalty -5 → -50`이며 나머지 reward·seed·iterations·실행 모드는 고정한다. 두 실행의 reward 함수가 달라지므로 총 mean reward 절댓값보다 낙상·episode length·terrain·tracking·영상의 paired 차이를 우선한다.

## 실험 기록 최소 단위

- 정책·체크포인트 식별자
- 변경한 파일과 단일 가설
- 실행 환경·명령·seed·학습 시간
- GUI/headless, camera/offscreen rendering, viewport update, video recording 조건
- 주요 지표와 play 영상 위치
- 성공·실패 관찰, 다음에 바꿀 한 가지

학습·batch 평가는 가능한 한 camera 없는 headless로 실행하고, 영상 생성과 시각 검증은 별도 실행으로 분리한다. GUI 또는 offscreen rendering 조건이 다른 결과는 처리량·VRAM 기준선으로 직접 비교하지 않는다.

## Optuna reward 탐색 원칙

- Optuna는 공식 서버에서 학습을 자동 실행하는 도구가 아니라, 개인 환경에서 **다음 reward 후보를 추천하는 Ask-and-Tell 의사결정 엔진**으로만 쓴다.
- evaluator·scenario·seed·objective가 고정되기 전에는 Optuna trial을 시작하지 않는다.
- 로봇, reward 단계, 공식 학습 iterations, evaluator/objective 버전마다 study를 분리한다.
- 첫 sampler는 2~4차원 TPE를 쓰고, 비교 가능한 완료 trial이 8개 미만이면 수동 1차원 sweep을 우선한다.
- objective는 `Train/mean_reward`가 아니라 tracking·survival·worst scenario·recovery·seed 분산을 합친 상대 비교용 Robust Proxy Score다.
- 초기에는 `NopPruner`를 사용한다. 정상 평가된 붕괴 정책은 FAIL로 버리지 않고 낮은 완료 점수로 남겨 나쁜 영역을 학습하게 한다.
- 첫 300회 H1 실행은 정책 미수렴이고 evaluator score가 없으므로 study에 backfill하지 않는다.

상세 search space·예산 gate·기록 형식은 `data/processed/planning/historical/04_OPTUNA_REWARD_SEARCH_DESIGN.md`를 따른다.

## 본선 전략 원칙

- 정책의 보행 안정성을 전제로 두고, 전략은 목표 선택·경로·위험 관리에 한정한다.
- LLM은 자유 서술을 바로 실행하지 않게 하고, 유효한 목표와 우선순위만 출력하도록 제한한다.
- 위험도와 남은 시간에 따라 보수적·공격적 선택을 바꾸되, 실제 경기 환경에서 검증되지 않은 가정은 피한다.

## 2026-10-09 Go2 평가 coverage 후속

[검증 요약](../experiments/go2/analysis/2026-10-09_GO2_R3_4800_R5_7450_LOCAL_OFFICIAL_COMPARISON.md): 같은 PERSONAL protocol에서 계단 통합 오차 **0.32029→0.14852**, 실패 **15/783→4/772**, G2 오차 **0.09085→0.07699**로 개선됐지만 공식 계단·전방위 Tracking Score는 하락했다. 로컬 고정 12.5cm/직진 조건과 공식10–15cm·미공개 명령/초기조건의 coverage를 우선 확인한다. 같은 scorer/collector/config와 raw 재집계가 일치하므로 점수 보정·scorer 교체·새 reward 학습을 서두르지 않는다. 과거 PERSONAL all-around REJECT를 공식 추종 대조군 제외로 확대하지 않으며, 4800의 공식 추종 상대 우위와7450의 공식 생존 이득을 모두 보존한다. reward-effect HOLD는 유지한다. episode/step/n0 분모를 구분하고 body-forward 진행 적분을 계단 완주로 부르지 않는다. G2 자세 비용과 잔여 stall 꼬리는 조건부 취약성 후보이지 공식 감점의 확정 원인이 아니다.
