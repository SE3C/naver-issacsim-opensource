---
title: "H1 공식 서버 실행 — baseline·TERM-50 5K·h1-submit-4 / AIRTIME-025 fresh 10K"
purpose: "AI upload bundle — 공식 H1 실행 증거, TERM-50 평가, h1-submit-4 제출·평가 상태"
sources:
  - 'data/processed/experiments/h1/2026-09-09_OFFICIAL_SERVER_H1_TERM50_5K_DEEP_ANALYSIS.md'
  - 'naver-issacsim-originals/data/raw/official_server_runs/h1/2026-09-08_232333_term50_5k/'
  - 'data/processed/experiments/h1/2026-09-08_OFFICIAL_SERVER_H1_BASELINE_1K.md'
  - 'naver-issacsim-originals/data/raw/official_server_runs/h1/2026-09-08_230725_baseline_1k/'
  - "data/processed/experiments/h1/training/2026-08-24_OFFICIAL_SERVER_300ITER_BASELINE.md"
  - "naver-issacsim-originals/data/raw/official_server_runs/h1/2026-08-24_124413_baseline_300iter/"
  - "data/processed/experiments/h1/analysis/2026-09-10_OFFICIAL_EVAL_H1_ROUND2_TERM50.md"
  - "data/processed/reference/official/2026-09-20_PRELIM_R1_OFFICIAL_VIDEO_OCR_TEAM_BENCHMARK.md"
  - "naver-issacsim-originals/data/raw/official_server_runs/h1/2026-09-27_213434_h005_fresh10k/"
  - "data/processed/experiments/h1/2026-09-28_H005_OFFICIAL_10K_technical_report.txt"
  - "data/processed/incoming/other/reviewed/H1_H005_OFFICIAL10K_VS_TERM50_OFFICIAL5K_DEEP_ANALYSIS_20260928.md"
  - "data/processed/experiments/h1/analysis/2026-09-30_OFFICIAL_EVAL_H1_ROUND4_AIRTIME025.md"
type: "verified_experiment_summary"
---

공식 TERM-50 5K의 `feet_air_time=+0.2`와 과거 PERSONAL H-001 Run 04 부모의 `-0.2`를 혼동하지 않는다. 2026-09-25의 corrected PERSONAL H-001 Run 05(+0.2)와 자식 Run도 공식 서버 실행이나 공식 제출 정책이 아니다. 두 개인 계보와 공식 run의 구분은 [H1 비교 문서](14_H1_NEXT_RUN_PARAMETER_COMPARISON.md)를 따른다.


# H1 공식 서버 실행 — 검증된 실측 증거

## 2026-10-07 ORIENT-100 공식 학습과 개인 행동 진단의 연결

- `exp-h1-rough-terrain-orientation-relaxation / ORIENT-100`: **OFFICIAL fresh 3K**, seed 42, 4,096 env, Run `20261006-133517-h1-orient-100-fresh3k-official`; evidence COMPLETE/PASS. 변경은 frozen `h1-submit-2` 대비 `flat_orientation_l2 -1.5→-1.0` 단일축이고 auto best `model_2850.pt` SHA `6aedeced60562c1d496d5319d29b76cf9e26ff43df06827cb370f24f5313f7b0`와 latest keeper `model_2950.pt`를 구분한다. [공식 intake](../experiments/h1/training/2026-10-06_ORIENT100_OFFICIAL3K_EVIDENCE_INTAKE.md).
- 후속 **Windows PERSONAL** `model_2850` 평가: `scenario7` 8 case × seed 3 × env 128 = **3,072/3,072 episode 20초 생존**, base-contact failure 0. H1 balance 비의도 전진 **+1.633m**, H3 lateral **+1.180m**, H5 rough 평균 tracking **0.1709**, 최소 진행 **7.831m**가 남는다. 여섯 영상은 실제 초기 지형 보행 근거이나 중앙 다단 계단 완주 입증은 아니다. [원문 분석](../incoming/other/reviewed/H1_ORIENT-100_POLICY_ANALYSIS_20261007.md).
- **행동 후보 HOLD**이고 OFFICIAL 제출/채점 결과가 아니다. **2026-10-07 단일 정책 검토 당시에는** 동일 평가의 `h1-submit-2 / TERM-50` 대조 ZIP을 분석하지 못했다. **2026-10-10 후속 ZIP 3개 raw 대응-index 비교에서 TERM-50 대조군 수치를 확보**했고 ORIENT composite tracking `0.14041` vs TERM `0.15712`(10.63% 낮음)를 확인했다. 그러나 ORIENT 전체 roll/pitch RMS `0.08015` vs TERM `0.03381` 등 상쇄·학습 Run 반복/물리 초기조건/훈련 설정 통제 부족으로 **인과적 reward 효과와 범용 정책 우위는 여전히 미확정**. [후속 비교](../experiments/h1/analysis/2026-10-10_H1_SCENARIO7_RAW_3POLICY_MATCHED_ANALYSIS.md). 학습 archive에 보존된 OFFICIAL 계보와 개인 평가 ZIP의 source_run_id=null을 체크포인트 SHA로 연결하되 provenance 레벨은 구분한다.



## 이 문서의 권한

이 문서는 보관된 `env.yaml`, `report.html`, policy·checkpoint와 백업 코드로 다시 확인되는 사실만 요약한다. 300회·baseline 1K는 파이프라인 기준선이지 공식 평가 점수가 아니다. 예선 2라운드 TERM-50 제출의 공식 점수와 시나리오 실점은 마지막 절에 있다.

## 핵심 판정

- 학습, checkpoint 선별, 환경 export, policy·ONNX export와 play 영상 생성은 완료됐다.
- 300 iterations 정책은 report상 terrain level `0.00`, fall rate `100.0%`이므로 안정 정책으로 판단하지 않는다.
- 2026-09-08 공식 baseline 1K도 terrain `0.00`, 마지막 10회 평균 fall rate `100.0%`여서 안정 정책이 아니다.
- 1K에는 TensorBoard event·코드 hash·Isaac 환경 정보가 추가됐지만 전체 콘솔·GPU 시계열·공식 evaluator 점수는 없다.
- 전체 실행시간 4분은 초기화·학습·finalize·export가 섞인 end-to-end 값이다.
- 전체 콘솔·TensorBoard event·GPU 시계열이 없어 steady-state 처리량과 전체 학습 곡선은 확정할 수 없다.
- 이 정책은 evaluator가 명백한 실패를 낮게 평가하는지 확인하는 negative control로만 사용할 수 있다.
- 예선 2라운드 TERM-50 제출은 종합 86.37/100, 시뮬 56.37/70이다. 7시나리오 실점은 77.8%~82.1%로 고르게 보통이다.

## h1-submit-4 / AIRTIME-025 — OFFICIAL fresh 10K와 제출·평가

2026-09-27 `h1-submit-4 / AIRTIME-025` evidence Run `20260927-123428-h005-fresh10k-official`(legacy H-005 R05)은 공식 서버에서 `termination_penalty=-50`, `track_lin_vel_xy_exp=0.5`, `feet_air_time=0.25`로 checkpoint 없이 처음부터 10,000회 학습했다(seed 42, 4096 environments). 이 Run은 exit 0·validation PASS·finalize/backup 완료를 기록하며 [Originals raw-run Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20260927-airtime-025-fresh10k)에 연결된다. `model_best.pt`는 `model_9800.pt`와 동일하고 마지막 보존 numbered checkpoint는 별도 `model_9950.pt`다. 보존된 native `report.html`은 최고 보상 5.42(iter 9784), terrain 5.83, 마지막 10회 낙상률 25.7%를 표시한다.

사용자는 2026-09-28 이 `h1-submit-4 / AIRTIME-025` 정책의 **예선 4라운드 제출**을 알리고 [직접 작성한 기술 개선 리포트 원문](../experiments/h1/2026-09-28_H005_OFFICIAL_10K_technical_report.txt)을 제공했다. 수신한 세 제출 파일은 [별도 submission Release](https://github.com/SE3C/naver-issacsim/releases/tag/submission-h1-prelim-r4-20260928)에 게시하고 원격 크기·digest 5/5를 대조했다. 원본 포털 ZIP·수령증·정확한 제출 시각은 여전히 없지만, 2026-09-30 수신한 공식 평가 결과는 시뮬레이션 56.37/70, 설계 의도 20/20, 리포트 품질 10/10이다. 세 항목의 구성 점수 합계는 86.37/100이지만, 수신 원문에는 별도의 종합 점수 필드가 없었다. 뒤이어 받은 [심층 비교 보고서 원문](../incoming/other/reviewed/H1_H005_OFFICIAL10K_VS_TERM50_OFFICIAL5K_DEEP_ANALYSIS_20260928.md)은 작성 당시 “미제출”로 적었지만, 현재 제출·평가 상태는 그 이후의 수신 자료를 따른다. 이 Run을 이전 `h1-submit-2 / TERM-50` 5K나 PERSONAL legacy H-005 계보와 섞지 않는다.

심층 보고서의 raw TensorBoard late-500 비교에서 **같은 5K 단계** `AIRTIME-025`/`TERM-50`의 terrain은 `5.6570/5.7306`, XY error는 `0.3655/0.3690`, yaw error는 `0.9642/0.9213`, training base-contact는 `28.549%/28.150%`다. XY 차이는 작고 창에 따라 방향이 바뀌며 terrain·yaw·접촉에서는 `AIRTIME-025` 쪽이 불리하다. 따라서 `feet_air_time 0.25`가 `0.20`보다 5K 단계에서 전체적으로 우수하다는 결론은 없다. 반면 `AIRTIME-025` Run 자신의 5K→10K late-500은 terrain `5.6570→5.8065`, yaw error `0.9642→0.8843`, base-contact `28.549%→25.881%`, episode length `790.29→820.19`로 개선됐고 XY error는 거의 유지됐다. 이는 추가 학습 구간의 관찰이지 reward 변경의 순수 효과가 아니다.

보고서는 6영상에서 boxes·random rough·inverted stairs의 실제 진행을 관찰했으나, stairs 중앙 완주와 경사 실제 통과 거리는 입증하지 못했다. 영상 묶음에는 checkpoint SHA/manifest가 없어 `model_9800.pt` 또는 `model_9950.pt`의 행동으로 귀속할 수 없고, loose `policy.pt`의 정확한 source checkpoint도 확인되지 않는다. 현재 H1 PERSONAL evaluator의 공용 core를 재사용하는 Windows 통합 launcher가 `C:\NCRC\h1_6terrain_video.bat`로 설치됐고 CPU 회귀 테스트 60개와 PowerShell/설치 파일 검증을 통과했다. H1은 ±10° 6영상 뒤 camera-off `scenario7` 8 case full 평가를 사용하지만 당시(2026-10-06) H1 Windows GPU full·paired comparison은 미실행이었다. 이후 **2026-10-07 `ORIENT-100 / model_2850`의 PERSONAL 단일 정책 full**은 확보했지만, 이 문단의 Round-4/AIRTIME·TERM-50 checkpoint들에 대한 matched 평가나 paired comparison은 여전히 수행되지 않았다. 따라서 `model_9800.pt`·`model_9950.pt`와 공식 TERM-50 `model_4900.pt`의 동일 조건 수치 비교는 **미실행 미래 검증 항목**이다. 현재 내부 비교는 TensorBoard·console·native 영상의 AI 분석이다. 공식 Round-4의 세 구성 점수 합계는 Round-2 종합 점수와 수치상 같은 86.37이지만, 두 제출은 reward뿐 아니라 학습량도 5K→10K로 달라 이 점수 비교만으로 `feet_air_time 0.20→0.25`의 단독 효과를 격리할 수 없다.

## 2026-09-30 예선 4라운드 공식 평가

수신한 공식 결과는 다음과 같다.

| 시나리오 | Round 2 `h1-submit-2` | Round 4 `h1-submit-4` | 변화 |
| --- | ---: | ---: | ---: |
| 제자리 균형 | 8.62 / 10.5 | 8.58 / 10.5 | -0.04 |
| 전진 속도 추종 | 11.24 / 14 | 11.34 / 14 | +0.10 |
| 좌우 속도 추종 | 5.73 / 7 | 5.72 / 7 | -0.01 |
| 회전 복합 추종 | 5.66 / 7 | 5.68 / 7 | +0.02 |
| 약한 요철 | 8.17 / 10.5 | 8.00 / 10.5 | **-0.17** |
| 완만한 경사 ±10° | 8.47 / 10.5 | 8.53 / 10.5 | +0.06 |
| 밀침 회복 | 8.48 / 10.5 | 8.52 / 10.5 | +0.04 |
| **시뮬레이션 합계** | **56.37 / 70** | **56.37 / 70** | **0.00** |

Round 4의 설계 의도 분석은 20/20, 리포트 품질은 10/10이며 구성 점수 합계는 86.37/100이다. 즉 **Round-4의 10K AIRTIME-025 제출 전략**은 Round-2 제출보다 공식 7시나리오 점수 순증가를 만들지 못했고, 목표와 직접 연결해 기대했던 약한 요철은 0.17점 하락했다. 다만 Round-2는 5K, Round-4는 10K이므로 이를 AIRTIME 변경의 단독 인과효과로 읽지 않는다.

이 결과는 feet_air_time=0.25가 일반적으로 나쁘다는 증거가 아니다. AIRTIME 0.20→0.25와 학습량 5K→10K가 함께 달라, 공식 점수는 Round-4 제출 패키지 결과로만 사용한다. **2026-10-06 ORIENT-100 fresh 3K는 OFFICIAL COMPLETE/PASS이며, 2026-10-07 PERSONAL 행동 선택은 HOLD**다. [접수·원본·Release](../experiments/h1/training/2026-10-06_ORIENT100_OFFICIAL3K_EVIDENCE_INTAKE.md). ACTRATE-001은 이후 독립 OFFICIAL fresh3K 완료/PASS·PERSONAL model2850 분석 수납/HOLD로 갱신됐다. frozen `h1-submit-2`에서 action=-0.001만 바꿨고 ORIENT의 config/checkpoint를 상속하지 않았다.

## 증거 등급

| 등급 | 의미 | 예시 |
| --- | --- | --- |
| A | 보관된 실행 산출물에서 직접 확인 | iterations, 시간, seed, env 수, 마지막 report 지표 |
| B | 백업 코드와 산출물 설정을 교차검증 | PPO 설정, rollout 길이, checkpoint 선택 방식 |
| C | 과거 분석에만 있고 원본 로그가 없음 | 상세 GPU/OS, 코어 iteration 0.69~0.71초 |
| D | 재현 스크립트 없는 탐색 분석 | 단일 observation probe, Jacobian |

AI는 A·B만 핵심 결론으로 사용하고 C는 재측정 대상으로, D는 성능 근거에서 제외한다.

## 직접 확인된 실행값

| 항목 | 값 |
| --- | ---: |
| robot/task | Unitree H1 / Humanoid, 19 actions |
| 시작 시각 | 2026-08-24 12:44:13 KST |
| seed | 42 |
| 병렬 환경 | 4096 |
| iterations | 300, step 299까지 |
| end-to-end 시간 | 4분 0초 |
| end-to-end 평균 | 0.80초/iteration |
| 표시된 최고 mean reward | 0.16, step 287 |
| 선택 checkpoint | iteration 299 |
| 마지막 terrain level | 0.00 |
| 마지막 fall rate | 100.0% |
| 마지막 action std 평균 | 0.633 |
| NaN | report상 없음 |

## 2026-09-08 공식 baseline 1K 보강 증거

| 항목 | 값 |
| --- | ---: |
| seed / 병렬 환경 | 42 / 4096 |
| iterations | 1000, step 999까지 |
| 표시 학습시간 | 12분 14초 |
| 표시 최고 mean reward | 0.38, step 971 |
| 선택 checkpoint | `model_999.pt` |
| 마지막 terrain / fall rate | 0.00 / 100.0% |
| 마지막 exploration std | 0.653 |

1K는 300회보다 mean reward 표시값이 높지만 terrain과 낙상률은 개선되지 않았다. 단일 seed이고 terrain generator seed가 `null`이므로 통계적 paired 비교가 아니다.

1K 원본에는 TensorBoard event, 최종 checkpoint, env·agent, policy·ONNX·영상, 코드 hash와 Isaac 환경 정보가 있다. 해시 목록은 전체 작업공간 manifest가 아니며 TAR root의 `humanoid_rewards.py`는 목록의 baseline 1K snapshot과 일치한다.

`0.80초/iteration`은 240초를 300으로 나눈 계산값이다. 고정 startup/finalize overhead가 포함되므로 5,000·10,000·25,000 iterations 시간을 이 값으로 선형 예측하지 않는다.

## 환경과 데이터량

| 항목 | 값 |
| --- | ---: |
| physics dt | 0.005초, 200 Hz |
| decimation | 4 |
| control dt | 0.020초, 50 Hz |
| episode limit | 20초 |
| command resampling | 10초 |
| steps per env/iteration | 24, 0.48초 |
| observation/action | 256 / 19 |
| actor·critic hidden dims | `[512, 256, 128]`, ELU |

4096 envs와 24 steps를 기준으로 iteration당 98,304 transitions다. 300회에는 29,491,200 transitions가 있고, env 하나는 144초의 simulated experience를 누적한다. 전체 env를 합하면 163.84 robot-hours다. 이 계산은 데이터량이지 실제 wall-clock 학습시간 예측이 아니다.

## 확인된 PPO 설정

| 항목 | 값 |
| --- | ---: |
| algorithm | PPO |
| epochs / mini-batches | 5 / 4 |
| initial learning rate | 1.0e-3, adaptive |
| gamma / lambda | 0.99 / 0.95 |
| desired KL | 0.01 |
| entropy coefficient | 0.008 |
| clip | 0.2 |
| max grad norm | 1.0 |
| save interval | 100 |

이 값은 환경 이해용이다. 참가자 실험은 허용된 reward 파일을 중심으로 하며 PPO 설정을 탐색 대상으로 삼지 않는다.

## 실제 활성 reward

참가자 수정 대상 9개:

| reward | baseline |
| --- | ---: |
| `track_lin_vel_xy_exp` | +0.5 |
| `track_ang_vel_z_exp` | +0.5 |
| `feet_air_time` | +0.2 |
| `termination_penalty` | -5.0 |
| `flat_orientation_l2` | -1.5 |
| `ang_vel_xy_l2` | -0.05 |
| `joint_deviation_hip` | -0.2 |
| `joint_deviation_torso` | -0.1 |
| `action_rate_l2` | -0.0005 |

`env.yaml`에는 프레임워크 기본 nonzero reward 4개도 있다: `dof_acc_l2=-1.25e-7`, `dof_pos_limits=-1.0`, `feet_slide=-0.25`, `joint_deviation_arms=-0.2`. 따라서 실질 활성 reward는 총 13개다. 참가자는 허용된 9개만 수정하되 결과 해석에는 기본 4개의 영향도 포함한다.

`termination_penalty=-5`는 백업 reward 파일의 추천 구간 `-50~-400` 밖이다. 중요한 실험 후보지만 300회 실패의 단독 원인으로 확정하지 않는다.

## 지형과 재현성 주의

6개 terrain raw weight 합은 0.90이며 Isaac Lab에서 정규화된다. 정규화 비중은 stairs 16.67%씩, boxes 33.33%, rough와 두 slope 11.11%씩이다. raw weight에 200을 직접 곱해 정확한 patch 수를 단정하지 않는다.

보관 설정에서 terrain generator seed는 `null`, cache는 `False`다. 같은 학습 seed여도 지형 생성 차이가 섞일 수 있으므로 단일 실행 차이를 reward 효과로 과대해석하지 않는다.

## checkpoint 해석

백업 finalize 로직은 `Train/mean_reward` 최고 step과 가장 가까운 저장 checkpoint를 `model_best.pt`로 고른다. peak가 287이고 저장 checkpoint가 299라면 iteration 299가 선택될 수 있다. `model_best.pt`는 공식 시나리오 성능 최고 정책이라는 뜻이 아니다.

## 2026-08-24 300회 자료만으로 당시 답할 수 없었던 것

- iteration 0→299 전체 reward·episode·terrain 곡선
- reward term별 시계열, KL·learning-rate 변화
- 안정 구간 seconds/iteration과 FPS
- 상세 GPU·VRAM·전력 병목
- 장기 수렴 시점과 공식 평가 점수
- `termination_penalty=-5`가 실패의 단독 원인인지

이 목록은 2026-08-24의 300회 자료만 놓고 본 당시 한계다. 이후 TERM-50 5K와 다른 보존 evidence가 일부 항목을 해소했으므로, 현재 미확인 항목과 다음 행동은 이 문서의 후속 절·`14`·registry를 우선한다. 새 실행에서는 계속 전체 `logs/<run>/`, tfevents, 콘솔·GPU 시계열을 확보한다.

## 2026-09-08 h1-submit-2 / TERM-50 fresh 5K 공식 실행 (legacy H-001 R02)

같은 공식 서버 H1 task에서 seed 42, 4096 environments, 5000 iterations로 실행했고 학생 reward 중 `termination_penalty`만 `-5.0`에서 `-50.0`으로 바꿨다. 전체 TensorBoard scalar, config, checkpoint·policy hash와 현재 play 영상이 보존됐다.

| 항목 | 4999 endpoint |
| --- | ---: |
| mean reward | 3.346 |
| episode length | 774.1 |
| terrain level | 5.825 |
| base-contact | 28.93% |
| timeout | 71.07% |
| XY error | 0.378 |
| yaw error | 0.935 |
| exploration std | 1.296 |

결론은 안정성과 terrain progression이 확인됐지만 yaw 추종이 병목이라는 것이다. 개인 L40S baseline 5K의 base-contact 33.21%, terrain 5.054보다 방향상 좋지만 XY error는 0.342에서 0.378, yaw error는 0.652에서 0.935로 나빠졌다. 서버 출처와 실행 시점이 다른 단일 seed 비교이므로 엄밀한 paired causal effect로 부르지 않는다.

현재 `model_best.pt`는 `model_4900.pt`와 hash가 같고, 현재 policy와 40초 영상도 timestamp 별칭과 연결된다. 함께 들어 있는 `20260908230725`·`20260908_232209` 계열은 이전 baseline 파일이므로 TERM-50 증거로 사용하지 않는다. 현재 영상에는 명백한 낙상이 보이지 않지만 최대 episode가 20초라 40초 연속 생존 증거는 아니다.

복수 seed, 동일 command sequence paired 영상과 train stdout/stderr 전체는 없다. 예선 2라운드 공식 점수는 아래와 같다. TERM-50은 final optimum이 아니라 stability anchor로 취급하고, 후속 reward 변경은 같은 checkpoint에서 한 변수씩 분기해 이 점수와 비교한다.

## 2026-09-10 예선 2라운드 공식 평가

2026-09-09 00:42에 제출한 H1 TERM-50 정책의 공식 점수다. 대시보드 텍스트로 수신했다. 순위는 없다. 상세 판정은 `data/processed/experiments/h1/2026-09-10_OFFICIAL_EVAL_H1_ROUND2_TERM50.md`를 따른다.

| 항목 | 점수 |
| --- | ---: |
| 시뮬레이션 | 56.37 / 70 |
| 설계 의도 분석 | 20 / 20 |
| 리포트 품질 | 10 / 10 |
| 종합 | 86.37 / 100 |

| 시나리오 | 실점 / 배점 | 비율 |
| --- | ---: | ---: |
| 제자리 균형 | 8.62 / 10.5 | 82.1% |
| 전진 속도 추종 | 11.24 / 14 | 80.3% |
| 좌우 속도 추종 | 5.73 / 7 | 81.9% |
| 회전 복합 추종 | 5.66 / 7 | 80.9% |
| 약한 요철 | 8.17 / 10.5 | 77.8% |
| 완만한 경사 ±10° | 8.47 / 10.5 | 80.7% |
| 밀침 회복 | 8.48 / 10.5 | 80.8% |

7항목이 77.8%~82.1%라 공식 코멘트의 “고르게 보통”과 맞다. 비율 최저는 요철, 절대 실점 공백 최대는 전진(2.76점)이다. 회전 남은 점수는 1.34점이라 내부 yaw error를 공식 점수의 주 누수로 부르지 않는다. 다음 공식 비교 기준선은 시뮬 56.37과 위 7항목이다.

## 예선 1차 공식 영상의 타 팀 OCR 참고

수신 OCR에는 `Rough Slope ±10°` 화면의 H1 12팀과 Go2 2팀이 기록돼 있다. H1 checkpoint
중앙값은 `4,999`, 화면상 fall rate 범위는 `18.5%~28.3%`이고 중앙값은 `25.1%`다. Go2는
두 팀의 `9.2%`, `2.8%`만 있어 분포로 일반화하지 않는다. 원본 MP4 재검증, fall-rate 산식,
episode 수, seed, fresh/resume 구분이 없으므로 TERM-50의 report `base-contact 28.93%`나 공식
시뮬레이션 점수와 직접 비교하지 않는다. 이 자료는 타 팀 규모 확인용이며 가설 채택·순위 추정
근거가 아니다. 상세 표와 주의사항은
`data/processed/reference/official/2026-09-20_PRELIM_R1_OFFICIAL_VIDEO_OCR_TEAM_BENCHMARK.md`를 따른다.

## 공식 서버 기계 환경

TERM-50 5K 원본 README에 있는 호스트 기록이다. 분석 핵심팩의 개인 L40S 22.04와 섞지 않는다.

- Ubuntu 24.04.2 LTS, kernel 6.8.0-136-generic
- RTX 5080 16,303 MB, driver 580.126.09
- Isaac Sim `5.1.0-rc.19+release.26219.9c81211b.gl`
- Isaac Lab `3e73d6dd79080fd7632488c061052a6edd52e230`

1K 묶음 `h1_code_sha256.txt`의 live `train.py`·`play.py`·`h1_task/_finalize.py` 해시는 개인 nvidia 저장소 `training/humanoid`와 다르다. `env_cfg.py`·`agent_cfg.py`·`__init__.py`·`pyproject.toml`은 같다. 결과 tar에는 그 세 파일 원문이 없다.

위 문단은 2026-09-08 1K 실행 당시의 provenance다. 현재 source 기준은 2026-09-13 공식 서버 `/workspace/training` snapshot(`NCRC_OFFICIAL_TRAINING_20260913_195915.tar.gz`, SHA-256 `2c1326e0b58e9c860e32db81f110d2c0de16fac113de4424144b73e39fe01d15`)이다. 해당 snapshot은 Originals canonical extracted training과 NVIDIA `training/`에 동기화되어 있으며, 과거 1K 결과의 코드 hash 불일치가 현재 동기화 상태를 뜻하지는 않는다.
