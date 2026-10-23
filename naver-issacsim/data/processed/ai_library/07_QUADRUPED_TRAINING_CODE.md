---
title: "Go2 사족보행 학습 코드 판단"
purpose: "AI upload bundle — Go2 reward 실험·검증의 코드 지도"
sources:
  - "data/processed/incoming/other/reviewed/GO2_A1_1K_3K_VIDEO_FULL_EVIDENCE_ANALYSIS_20260914.md"
  - 'data/processed/incoming/other/reviewed/GO2_OFFICIAL_BASELINE_1K_AND_ISSACSIMZ_LOGGING_ANALYSIS_20260914.md'
  - "../naver-issacsim-originals/data/raw/server_backup/extracted/training/quadruped/"
  - "data/processed/server_backup/code/training/quadruped/"
  - "data/processed/incoming/other/reviewed/NCRC_20260913_MASTER_TRACKING_REPORT.md"
  - "data/processed/incoming/other/reviewed/GO2_A1_1K_DEEP_EVIDENCE_ANALYSIS_20260913.md"
  - "data/processed/incoming/other/reviewed/GO2_G5_OFFICIAL_1K_LIGHTWEIGHT_FAILURE_ANALYSIS_20260914.md"
  - "data/processed/incoming/other/reviewed/GO2_A1_THREE_EXPORTS_DEEP_ANALYSIS_20260914.md"
  - "data/processed/incoming/other/reviewed/GO2_A1_MODEL_4300_DEEP_ANALYSIS_20260915.md"
  - "data/processed/incoming/other/reviewed/GO2_A1_MODEL_4800_DEEP_ANALYSIS_20260915.md"
  - "data/processed/incoming/other/reviewed/GO2_A1_MODEL_4900_DEEP_ANALYSIS_20260915.md"
  - "data/processed/experiments/go2/analysis/2026-09-15_GO2_G-005_FIXED_EVAL_SEED4201_D1.md"
  - "data/processed/experiments/go2/analysis/2026-09-15_GO2_G-005_4800_4900_NATIVE_VIDEO_AND_SELECTION.md"
  - "data/processed/incoming/other/reviewed/A1_4800_vs_4900_DEEP_ANALYSIS_AND_LEARNING_RECORD_20260915.md"
  - "data/processed/incoming/other/reviewed/GO2_FINAL_TECHNICAL_REPORT_FLOW_DRAFT_20260915.md"
  - "data/processed/incoming/other/reviewed/SE3C_예선3라운드_Go2_평가_및_운영진답변_20260920.md"
  - "data/processed/incoming/other/reviewed/NCRC_R3_WEIGHT_SIMILARITY_DISCOVERY_2026-09-23.md"
  - "data/processed/incoming/other/reviewed/GO2_20260929-154342-go2-lintrack-125-fresh7500-official_VS_20260928-230114-go2-lintrack125-fresh3k-r5-official_DEEP_ANALYSIS_20260930.md"
  - "data/processed/incoming/other/reviewed/GO2_20260929-154342-go2-lintrack-125-fresh7500-official_VS_20260928-230114-go2-lintrack125-fresh3k-r5-official_DEEP_ANALYSIS_20261004.md"
---

# Go2 사족보행 학습 코드 판단

## Windows 로컬 영상·개별 평가 운영

고정 6영상과 camera-off 수치 평가는 [21](21_WINDOWS_GO2_VIDEO_AND_EVALUATION.md)의 검증된 `C:\NCRC\go2_6terrain_video.bat`로 순차 실행한다. 2950·7050 checkpoint는 출처의 전체 SHA256과 일치한다. 각 `scenario7` full 자료를 생성한 뒤 사용자가 제공한 2026-10-04 심층 보고서가 raw 진단·영상 비교를 수행했다. 새 학습 Run·OFFICIAL 점수·자동 comparison-CLI 산출물이 아니다. `model_7050` 행동 후보는 이 PERSONAL 조건에서 PROMOTE이며 reward 자체 효과는 HOLD다. task source·reward·PPO·기존 `exported/model_best.pt`는 수정하지 않았다. 단, Windows evaluator task source를 OFFICIAL 학습 source와 byte-identical한 재현으로 취급하지 않는다.

## 수정·확인 위치

- 참가자 실험의 중심 파일은 `training/quadruped/quadruped_rewards.py`다.
- play·task·환경·결과 정리의 현재 코드 기준은 Originals `server_backup/extracted/training/quadruped/`와 동기화된 NVIDIA `training/quadruped/`다. processed server backup은 과거 분석용 추출본이다.
- Go2의 접촉 계산과 지형 조건은 H1과 달라서, 두 로봇의 실행 시간을 단순 비교하지 않는다.
- 공식 서버 실행은 `python3 training/quadruped/train.py`처럼 Python을 직접 지정하지 않는다. `issacsimz`의 mode-aware wrapper가 확인된 IsaacLab launcher를 통해 `isaaclab.sh -p training/quadruped/train.py ...`를 구성하게 한다. AI가 수동 명령을 작성할 때도 이 경계를 우회하지 않는다.

## Go2 reward 표기 규칙

AI 답변과 새 실험 이름은 실제 reward 변수에서 바로 읽히는 아래 약어를 기본으로 쓴다. **약어와 숫자 값 사이는 항상 하이픈(`-`)으로 분리한다.** 숫자 인코딩은 프로젝트 convention이며 정확한 값은 항상 config/evidence가 기준이다.

| 실제 변수 | 기본 약어 |
| --- | --- |
| `track_lin_vel_xy_exp` | `LINTRACK` |
| `track_ang_vel_z_exp` | `ANGTRACK` |
| `lin_vel_z_l2` | `LINZ` |
| `ang_vel_xy_l2` | `ANGXY` |
| `dof_torques_l2` | `TORQUES` |
| `dof_acc_l2` | `DOFACC` |
| `action_rate_l2` | `ACTRATE` |
| `feet_air_time` | `AIRTIME` |
| `flat_orientation_l2` | `ORIENT` |
| `dof_pos_limits` | `DOFPOSLIM` |

예: `LINTRACK-125` = `track_lin_vel_xy_exp=1.25`, `ANGTRACK-100` = `track_ang_vel_z_exp=1.0`, `LINZ-2` = `lin_vel_z_l2=-2.0`, `AIRTIME-003` = `feet_air_time=0.03`, `ANGXY-012` = `ang_vel_xy_l2=-0.12`. 실제 3라운드 제출은 `g2-submit-3 / LINTRACK-150-LINZ-2`를 기본 이름으로 쓰며, legacy `G-005`·초기 alias `A1`은 필요할 때만 괄호에 병기한다.

## Go2에서 먼저 볼 것

현재 후속 방향은 [R3/R5 로컬·공식 불일치 논의](../experiments/go2/analysis/2026-10-08_GO2_LOCAL_OFFICIAL_EVALUATION_GAP_AND_ANALYSIS_POLICY.md)와 [운영진 점수 구성 답변](../experiments/go2/analysis/2026-10-08_GO2_R3_R5_OFFICIAL_SCORE_COMPONENTS_ORGANIZER_REPLY.md)을 따른다. 공식 계단 survival **99.0%→99.8%**는 개선됐지만 tracking **0.819→0.796** 손실이 더 커 계단 점수는 **8.52→8.35**로 낮아졌다. 학습 contact와 공식 survival은 다른 지표이며, 로컬 tracking error 개선을 공식 Tracking Score 개선으로 확대하지 않는다. 다음 질문은 개선된 생존을 유지하면서 실제 명령 추종 손실을 회복할 수 있는가다. 평가기는 유지하고 합산 점수 단독 채택을 제한한다. 공식 구성 기여가 알려졌어도 로컬·공식 역전 메커니즘·reward 인과·새 학습 계획은 미확정이다.

1. 전후·측면·회전 명령을 안정적으로 따르는지 확인한다.
2. 거친 지형, 경사, 계단, 외란 뒤 회복을 따로 검증한다.
3. 빠른 보행과 낮은 수직 흔들림·착지 안정의 균형을 만든다.

## 실험 등록과 historical alias

현재 가설·Run의 운영 기준은 [`research/EXPERIMENTS.md`](../../../research/EXPERIMENTS.md)다.
현재 새 이름은 [Experiment naming](../../../research/EXPERIMENT_NAMING.md)에 따라 제출 preset·검증 질문·실제 학습 Run·최종 override·lineage를 구분한다. AI 답변에서는 제출 preset 또는 위 reward descriptor를 기본 이름으로 쓰고, 아래 `G-xxx`·`Rxx`·초기 alias는 기존 기록을 찾기 위한 legacy 주소로만 다룬다.

모든 새 Go2 Run은 Experiment 질문, 기준 제출 preset, 최종 override, resolved config 출처, `Environment`, `requested iterations`, `last console iteration`, `last saved checkpoint iteration`, `parent/resume checkpoint SHA`, `completion status`, canonical evidence·Release 링크를 같은 형식으로 남긴다. 실제 3라운드 제출 기준 전체 설정은 [g2-submit-3](../../../research/submission_presets/README.md)에 보존한다. 특히 resume은 원본 fresh run과 분리된 새 가설이 아니라 같은 가설의 계보 Run이며, curriculum reset 가능성 때문에 raw reward·terrain을 fresh trajectory의 직접 개선율로 읽지 않는다.
따라서 iteration이 늘었다고 새 Experiment를 만들지 않으며, 다른 검증 질문이 생길 때만 새 질문 주소를 만든다. 기존 `G/GS` 번호는 더 발급하지 않는다. 과거 표기 `G2/G3/G4/G5`는 각각 registry의 `G-001/G-002/G-003/G-004`를 가리키는 historical alias이고, 아주 오래된 `A1`은 legacy `G-005`를 가리킨다. 이 매핑은 원문 검색용이며 새 답변의 기본 이름으로 재사용하지 않는다.

개인 결과는 가설의 screening·우선순위 판단에만 사용한다. 성능 보고서와 제출 근거에는
registry의 `Environment: OFFICIAL` Run만 사용하고, 공식 baseline 1K와 개인 `LINTRACK-150-LINZ-2` 계보 자료를
동일 서버·동일 delta의 paired 비교처럼 쓰지 않는다.

## 2026-09-13 Go2 early-screen 재분류와 비교 규칙

원문은 `data/processed/experiments/go2/2026-09-13_GO2_EARLY_STABILITY_SCREENING_FAILURE_REPORT.md`, `2026-09-13_GO2_G-002_G-003_FAILURE_AND_VALIDATION_STRATEGY_V2.md`, 통합 정정본 `data/processed/incoming/other/reviewed/NCRC_20260913_MASTER_TRACKING_REPORT.md`, A1 1K와 fresh 3K forensic 원문 `data/processed/incoming/other/reviewed/GO2_A1_1K_DEEP_EVIDENCE_ANALYSIS_20260913.md`, `GO2_A1_1K_3K_VIDEO_FULL_EVIDENCE_ANALYSIS_20260914.md`, 공식 A1 fresh/recovery 원문 `GO2_A1_THREE_EXPORTS_DEEP_ANALYSIS_20260914.md`에 보존한다. 앞의 1K/3K는 개인 NVIDIA Brev L40S single-seed 자료이고, 마지막 문서는 공식 서버 run을 분석한다. 어느 것도 공식 evaluator 점수 자체는 아니다.

초기 100~200 iteration에서 terrain이 내려간다는 사실만으로 reward 가설을 최종 기각하지 않는다. curriculum은 정책 능력에 맞춰 난이도를 낮출 수 있고, 같은 개인 Go2 baseline도 약 4.5k terrain `0.92`에서 약 9.5k `5.83`으로 늦게 회복한 이력이 있다. 따라서 이 세 early-screen은 **early-screen negative**(초기 구간에서 기대한 즉시 개선이 없었음)로 기록하며 장기 실패 확정으로 읽지 않는다.

| 현재 표기 | 단일 변경 | 초기 관찰 | 현재 우선순위 |
| --- | --- | --- | --- |
| `LINTRACK-125` | `track_lin_vel_xy_exp: 1.0 → 1.25` | OFFICIAL fresh 3K·7.5K COMPLETE/PASS; 첫 3K trajectory exact match; PERSONAL 3정책 same-protocol 행동 비교 완료 | **terminal model_7450은 PERSONAL 행동 주후보 PROMOTE 뒤 `g2-submit-5 / LINTRACK-125`로 2026-10-06 actual Round-5 제출(사용자 확인). model_7050은 안전성 fallback HOLD; reward 효과 HOLD. g2-submit-3 4800의 all-around REJECT는 PERSONAL 후보 판단이며 공식 추종 비교 대조군에서 제외한다는 뜻이 아니다. R5 공식 점수 88.32/100(시뮬 58.32/70·설계 20/20·리포트 10/10), 2026-10-08 수신; PERSONAL 비교 자체는 공식 점수가 아님** |
| `LINZ-4` | `lin_vel_z_l2: -3.0 → -4.0` | 205 iter terrain `0.174`, base-contact 재증가; tracking 일부 개선 | 낮음 |
| `AIRTIME-003` | `feet_air_time: 0.01 → 0.03` | 115 iter terrain 약 `1.01`, timeout/base-contact 일부 개선 | 중간 |

`flat_orientation_l2`의 `-1.0`~`-0.125` 축은 강한 생존 편향과 terrain 하락 신호가 반복되어 현재 우선순위에서 제외한다. 다만 이 역시 짧은 screening의 관찰이며, 다른 축보다 재검증 우선순위가 낮다는 뜻이다.

legacy `G-004 ANG-STAB`(아주 오래된 alias `G5`)와 같은 delta의 공식 fresh 1K run `20260914-012909-go2-g5-angvelxy-m012-1k-official`은 Originals에 정식 보존됐다. train archive SHA-256은 `1e162fdf640a715f19c564e21bff1011cd7ed91287db2f8d3586c3e0382d4359`이며 내부 `SHA256SUMS` 33/33, evidence validation, official finalize와 backup PASS를 직접 확인했다. 그러나 report의 best reward `14.41 @ 972`에도 terrain은 `0.00`이었고, iter 613의 XY error `1.7363`, timeout `97.71%`, base-contact `2.29%`, episode length `973.45`는 정상 보행이 아닌 termination 회피를 가리킨다. 받은 play video에 대한 행동 판독도 옆으로 눕거나 거의 뒤집힌 비정상 자세의 반복이다. 낮은 base-contact과 높은 timeout을 안정성으로 읽지 말아야 하는 **공식 서버에서 관찰된 생존형 local optimum**이므로 이 legacy ANG-STAB 실험은 strong negative로 기록하고 3K로 연장하지 않는다. loose MP4는 H.264 1920×1080, 50 fps, 19.98초로 검증했지만 별도 video evidence archive가 공급된 것은 아니다.

각 run 전 reward는 baseline에서 단 하나만 바꾼다.

```python
"track_lin_vel_xy_exp": 1.0,
"lin_vel_z_l2": -3.0,
# "flat_orientation_l2": -1.0,
"feet_air_time": 0.01,
```

`LINTRACK-125`(`track_lin_vel_xy_exp: 1.0 → 1.25`, legacy G-001 / LIN-TRACK)은 이제 OFFICIAL fresh 3K와 별도 fresh 7.5K까지 완료·분석됐다. 두 Run은 reward/source/PPO/env/seed 42/4096 env가 같고 구조적 차이는 `max_iterations`와 run별 `log_dir`뿐이다. 더 강하게 7.5K의 iteration 0–2999 substantive TensorBoard scalar 22개가 3K와 전 점 exact match하고, 0–2950의 50-step checkpoint 60개 SHA도 60/60 동일하다. 따라서 **3K→7.5K 차이는 이 exact single-seed trajectory의 추가 4.5K 학습 효과**로 읽을 수 있다. 반대로 둘 다 이미 1.25이므로 BASE `1.0` 대비 reward 자체의 효과는 판단할 수 없고 same-length unchanged BASE fresh control이 필요하다. 아래 `g2-submit-3 / LINTRACK-150-LINZ-2`도 두 변수 조합이라 이 인과 질문을 대체하지 않는다. `0~200`은 NaN/Inf, value-loss 폭발, action-std 이상, 실행 오류, reward 적용 오류 같은 **수치적 붕괴 sanity check** 전용이다. terrain/mean reward/base-contact의 단기 악화만으로 중단하지 않는다.

`1K`는 긍정 후보의 최종 채택 근거가 아닌 가벼운 1차 screening이다. 같은 조건의 baseline 대비 다음을 함께 본다: terrain이 완전히 눌리지 않았는지, base-contact 감소 방향, timeout/episode length 개선, XY 또는 yaw tracking 중 하나의 의미 있는 개선, `500→1000` 회복·개선 추세, 수치 안정성. 특히 terrain 절대값보다 `500→1000` 방향성을 우선한다. 예를 들어 500에서 낮더라도 1K에 회복 중이면 연장 후보이며, 500부터 1K까지 0 근처에 머물고 다른 지표도 전반적으로 나쁘며 회복 추세가 없을 때 중단 후보가 된다. 다만 사전 중단 조건이나 legacy `G-004 ANG-STAB`처럼 수치·영상이 함께 드러내는 명백한 붕괴·생존형 local optimum은 1K에서도 `REJECT`할 수 있다.

1K에서 위 지표 중 2~3개에 개선 가능성이 보이면 동일 조건 baseline과 함께 `3K`로 연장한다. 3K에서 terrain 추세, XY/yaw tracking, base-contact, timeout, episode length, reward/action-std 안정성과 evidence-linked video를 종합해 baseline보다 경쟁력이 있으면 `5K`로 간다. 긍정 후보의 최종 채택은 5K 영상과 수치를 합쳐 검증하며, 위의 명백한 실패 예외는 1K에서 기각할 수 있다.

## `LINTRACK-125` OFFICIAL fresh 3K→7.5K 분석 — 2026-09-30

[심층 원문](../incoming/other/reviewed/GO2_20260929-154342-go2-lintrack-125-fresh7500-official_VS_20260928-230114-go2-lintrack125-fresh3k-r5-official_DEEP_ANALYSIS_20260930.md)은 B=`20260928-230114-go2-lintrack125-fresh3k-r5-official`과 A=`20260929-154342-go2-lintrack-125-fresh7500-official`을 비교한다. 둘 다 fresh·OFFICIAL·seed 42·4096 env·동일 source/PPO/env/reward이고, A는 B의 resume가 아니다. 실행/evidence는 두 Run 모두 COMPLETE/PASS다.

late-500 동일 정의에서 3K→7.5K는 terrain `5.282→5.913`, XY error `0.736→0.567`, training base-contact `9.93%→6.23%`, timeout `90.07%→93.77%`, episode length `948.6→968.7`로 개선했고 yaw `0.396→0.399`는 사실상 동일하다. late-1000에서도 terrain·XY·contact·episode length 방향이 유지된다. total reward는 late-500에서 `16.123→15.684`로 오히려 낮아지므로 mean reward 하나를 locomotion 품질 순위로 쓰지 않는다.

장기 구간의 critic instability는 경고다. 0–2999에서 value loss >100은 0점, 3000–7499에서는 11점이고 max `273.12 @ 4711`이다. late-500 value-loss median/p99/max도 `0.023/8.24/37.10 → 0.200/40.58/109.04`로 커졌다. 그러나 NaN/Inf·terrain collapse 없이 후기 proxy가 회복했으므로 현재 판정은 **발산이 아니라 장기 critic instability 증가**다. 실제 행동 확인 전 10K 이상 자동 연장은 우선순위가 낮다.

checkpoint는 질문별로 구분한다. 3K automatic best는 `model_2000.pt`, terminal 인접 비교 대상은 `model_2950.pt`다. 7.5K automatic best `model_7050.pt`와 terminal `model_7450.pt`는 같은 OFFICIAL fresh 7.5K Run의 서로 다른 checkpoint이며 별도 reward trial이나 새 Run이 아니다. 2026-10-05 PERSONAL 동일 프로토콜 비교에서는 **7450이 7050보다 9개 case 중 8개 tracking·8개 진행에서 우위**라 현재 행동 주후보로 PROMOTE됐지만, stair-up 종료가 2→4회이고 `action_delta_rms`·`roll_pitch_rms`가 커져 7050은 안전성 fallback으로 HOLD한다. 이 차이를 reward 변경 인과효과로 해석하지 않는다. 이후 사용자는 terminal `model_7450.pt`에서 export된 policy를 `g2-submit-5 / LINTRACK-125`로 2026-10-06 실제 Round-5 제출했다고 확인했다. submission Release의 actor/env identity는 OFFICIAL 7.5K source와 연결됐지만 2026-10-08 사용자 전달 공식 평가에서 제출 시각 2026-10-06 01:10(시간대 미기재), 종합 88.32/100(시뮬레이션 58.32/70·설계 의도 20/20·리포트 품질 10/10)을 수신했다. 별도 포털 receipt 파일은 미보유다.

**2026-09-30 분석 당시에는** 행동 자료가 없었다. [2026-10-04 후속 원문](../incoming/other/reviewed/GO2_20260929-154342-go2-lintrack-125-fresh7500-official_VS_20260928-230114-go2-lintrack125-fresh3k-r5-official_DEEP_ANALYSIS_20261004.md)은 동일 프로토콜 PERSONAL `scenario7`에서 7050의 7개 scenario tracking error가 모두 낮고, G5 계단 error `0.60996→0.17085`, survival `96.0%→99.740%`임을 보고한다. 계단 상승 progress `9.23→18.67 m`, stall `34.51%→1.18%`; 하강 progress `7.20→18.89 m`, stall `53.44%→2.52%`다. 단 G2 roll/pitch와 일부 action delta는 증가하므로 전 지표 개선이나 더 부드러운 동작으로 일반화하지 않는다. episode reset으로 분모가 달라 episode-level paired 통계가 아니며, 공식 점수·제출 우위·reward 인과효과도 아니다.

영상에서 2950 `03_boxes.mp4`는 보고서의 20개 샘플 frame 모두 검은 화면이다. decode·파일 무결성 통과와 유효한 행동 증거는 별개다. 이는 캡처 결함이지 정책 실패가 아니며 scenario7에도 boxes case가 없어 해당 지형 비교는 미확인이다. 영상의 maneuver/push 시간표와 정량평가의 command 조건도 구분한다. 새 학습보다 미측정 `model_7450`을 기존 7050 자료와 같은 조건으로 평가하는 것이 우선이며, 실제 실행은 별도 승인·지원 경로 확인 후 진행한다. reward 자체 효과 질문에만 same-length BASE control이 필요하다.

## 2026-10-09 R3/R5 해석 갱신

[심층 비교·검증 요약](../experiments/go2/analysis/2026-10-09_GO2_R3_4800_R5_7450_LOCAL_OFFICIAL_COMPARISON.md): 같은 PERSONAL protocol에서 계단 통합 오차 **0.32029→0.14852**, 실패 **15/783→4/772**, G2 오차 **0.09085→0.07699**로 개선됐지만 공식 계단·전방위 Tracking Score는 하락했다. 로컬 고정 12.5cm/직진 조건과 공식10–15cm·미공개 명령/초기조건의 coverage를 우선 확인한다. 같은 scorer/collector/config와 raw 재집계가 일치하므로 점수 보정·scorer 교체·새 reward 학습을 서두르지 않는다. 과거 PERSONAL all-around REJECT를 공식 추종 대조군 제외로 확대하지 않으며, 4800의 공식 추종 상대 우위와7450의 공식 생존 이득을 모두 보존한다. reward-effect HOLD는 유지한다. G2 xy_rmse **0.09327→0.09493**, roll_pitch_rms **0.04330→0.15349**는 악화돼 전 지표 우위가 아니다. 이를 공식 Tracking 입력이나 감점 원인으로 단정하지 않는다.

## `g2-submit-3 / LINTRACK-150-LINZ-2` 계보: 1K→fresh 3K→official recovery

`g2-submit-3`으로 이어진 `LINTRACK-150-LINZ-2` 조합(legacy G-005, 초기 alias A1)은 `track_lin_vel_xy_exp: 1.0 → 1.5`와 `lin_vel_z_l2: -3.0 → -2.0`를 **동시에** 바꾼 개인 L40S run에서 시작했다. 1K train archive SHA-256은 `b1e89933d38c4ca8f1e04d19df13cc3e7e6426db74aeccd0e95819b0cef97fb8`, fresh 3K train은 `68a880bc12d624504bdda6ecc3456db1e4add4183cbaf1c73868251511715c31`, 3K video evidence는 `c5e19b7a00596094f14f049da6db39a85e44791c033566d007770ff89fcedb5b`로 보고됐다. 새 보고서 원문 SHA-256은 `6ccdba37a05f3a65ef33c87cb6c5e4fdbbb2511ac4140c03a85325fda265c08e`다. 현재 workspace에는 세 archive가 없으므로 3K archive 내부 검증과 tensor·TensorBoard 수치는 보존 보고서의 직접 분석 결과로 인용한다.

보고서의 effective configuration은 seed `42`, 4096 env, env당 24 rollout steps, iteration당 98,304 transitions, save interval 100이다. 3K는 1K checkpoint resume가 아니라 같은 seed/config로 처음부터 돌린 fresh run이며 총 294,912,000 transitions다. actor·critic MLP는 각각 `512→256→128` ELU이고, PPO는 5 epochs·4 mini-batches·adaptive learning rate `0.001`·gamma `0.99`·lambda `0.95`·entropy coefficient `0.008`·desired KL `0.01`·max grad norm `1.0`·clip `0.2`·NaN check enabled로 기록됐다.

terrain은 curriculum-enabled generator, `10×20` grid, `max_init_terrain_level=5`, patch `8 m×8 m`, horizontal/vertical scale `0.1/0.005`다. stairs·inverted stairs·random boxes·random rough가 각각 20%, slope·inverted slope가 각각 10%이고, command 범위는 x `-1~2 m/s`, y `-0.6~0.6 m/s`, yaw `-1~1 rad/s`, episode horizon은 20초다. `Curriculum/terrain_levels`는 4096개 env의 **평균**이므로 로봇이 확정적으로 정복한 단일 최대 level로 해석하지 않는다.

보고서에 따르면 1K와 fresh 3K는 timing/Perf를 제외한 step 0~999 TensorBoard scalar 25개 계열이 동일하고 `model_0`~`model_900` 공통 checkpoint 10개도 byte-identical이다. seed·source·PPO·reward가 같고 `max_iterations`만 달라 첫 1K 궤적의 재현성이 강하다. 이는 같은 deterministic 조건의 재현 근거이며 다른 seed·호스트로의 일반화 증거는 아니다.

3K는 초기 terrain `3.5284`에서 iter 193 `0.1666`까지 후퇴한 뒤 iter 1072에 초기 평균을 재돌파하고 final `5.3393`까지 올랐다. last-500은 terrain `5.1599`, XY error `0.7144`, base-contact `9.20%`, episode length `952.77`로 final 단일점만의 상승이 아니다. final은 XY `0.6522`, yaw `0.4172`, base-contact `8.98%`, episode length `959.37`, action std `0.61`이다. 31개 checkpoint는 finite·std 양수로 보고됐지만 value loss는 median `0.0265`, p99 `7.8971`, max `104.1677 @ 2912`의 일시 spike가 반복됐다. 곧 회복했으므로 3K 실패로 보지 않되 5K에서는 연속 폭증·NaN/Inf·std·terrain 하락을 감시한다.

final reward component는 `track_lin_vel_xy_exp +1.0749`, `lin_vel_z_l2 -0.0490`, `ang_vel_xy_l2 -0.1876`, `dof_torques_l2 -0.0971`, `dof_acc_l2 -0.2140`, `action_rate_l2 -0.1251`로 보고됐다. 높은 terrain에서 몸통·관절 운동과 action variation이 늘어난 정황이지만 episode·base-contact가 함께 유지돼 단순 난폭화로만 보지는 않는다. 다만 `LINTRACK-150-LINZ-2`는 tracking reward weight 자체가 `1.5`로 바뀌었으므로 reward component 절댓값을 baseline 성능비처럼 비교하지 않고 실제 추종 품질은 `error_vel_xy`를 우선한다.

reward peak는 iter 2905의 `21.45`이고 `model_best.pt`는 SHA-256상 `model_2900.pt`와 같다(`1f2cc93aee18e9b772a1260bf56912cc297be1e4632a047445c32bf739a4e8c3`). final `model_2999.pt`는 별도 정책이다. 3K video는 best checkpoint를 MP4 SHA-256 `deb0b7d548e572555de07ed4132bf54740b641a99efec87f47d704a9d53d43af`에 연결하며 PASS로 보고됐다. 이 결과가 reward를 유지한 공식 5K 시도의 승격 근거였다. 두 reward의 개별 효과를 알려면 `LINTRACK-125` 같은 track-only 대조 또는 별도 ablation이 여전히 필요하다.

공식 fresh 5K 시도 `20260914-084321-...`는 같은 `LINTRACK-150-LINZ-2` 설정으로 약 iter 4837까지 진행된 뒤 broken pipe로 중단됐다. 원본 wrapper SHA-256 `d2919617…30ef`, direct evidence 내부 SHA 66/66을 확인했고 49개 checkpoint·전체 console·TensorBoard가 남았다. iter 4800은 terrain `5.7367`, XY `0.5017`, episode `968.01`, base-contact `8.11%`였지만 finalize·backup이 실행되지 않아 validation FAIL이다. 장기 trajectory에는 value-loss spike `283.8869 @ 3747`, `265.3461 @ 4415`가 반복됐으나 이후 지표가 회복했고 보존 tensor에는 NaN/Inf가 없다고 분석됐다. 이 run을 완료된 fresh 5K로 승격하지 않는다.

공식 recovery `20260914-132725-...`는 원본 `model_4800.pt` SHA-256 `ea93f9b5…aba65`에서 200회를 이어 console `4999/5000`까지 완료했다. direct evidence 내부 SHA 24/24, validation·finalize·backup PASS다. 저장 간격 때문에 checkpoint는 4800·4900뿐이고 자동 선택 `model_best.pt`와 최종 `policy.pt`는 recovery `model_4900` 계열이다. 4900은 reward `24.40`, terrain `4.6251`, XY `0.5489`, yaw `0.3741`, episode `982.37`, base-contact `3.82%`, action std `0.57`; 4999는 terrain `5.7940`, XY `0.5697`이다. resume 시 curriculum이 `5.7367 → 3.5275`로 reset됐으므로 4800과 4900 raw reward·terrain을 같은 난이도의 개선율로 계산하지 않는다.

`g2-submit-3` 계보의 당시 checkpoint 선택 과정에서 개인 L40S fixed batch는 fresh `model_4300`, original `fallback_model_4800`, recovery `model_4900`을 seed 4201·difficulty 1.0·6지형·64 env·20초로 비교했다. Original 4800이 평균 timeout 생존 `98.18%`, worst terrain `93.75%`, base-contact `1.82%`, yaw RMSE와 action-rate에서 가장 균형적이어서 안정성 우선 제출 후보가 됐다. Recovery 4900은 평균 XY RMSE `0.4099`와 변위가 가장 좋지만 boxes `17.19%`, stairs `14.06%` base-contact인 진행성 대안이다. 4300은 control이다. 이 단일 seed 개인 평가는 공식 점수나 submit-ready 판정이 아니며, 이후 original 4800 matching 제출 snapshot이 별도로 공식 평가를 받았다.

세 checkpoint의 역할을 분리한다. Fresh `model_4300` SHA `82efb1a5…02c8`는 iter 4284 reward peak 주변의 **control**이다. Original `model_4800` SHA `ea93f9b5…aba65`는 첫 fixed batch에서 안전성 우선 **당시 제출 후보**였고, 이후 matching policy/env snapshot으로 실제 3라운드 평가를 받았다. Recovery `model_4900` SHA `250e430c…14cd`는 recovery run의 export policy actor와 exact-match하고 추종 지표가 좋은 **progress-first challenger**다. 이후 4800·4900 각각의 native play evidence run 6개가 validation과 MP4 SHA를 통과해 source-checkpoint 영상 연결은 확보됐다. 다만 이 영상은 difficulty·curriculum·고정 command·진행 방향을 fixed evaluator와 동일하게 강제하지 않았으므로 traversal benchmark나 공식 점수 근거가 아니다.

2026-09-23에 받은 웹 `study-file` ZIP `submission_1789393113.zip`은 기존 recovery Run 04의 `model_best.pt`(recovery 4900)·`env.yaml`·`report.html` 백업으로 판별해 Originals에 별도 원문 보존했다. 실제 R3 제출 `policy.pt`는 SHA-256과 기존 제출 Release가 일치하는 **original 4800 계열**이며 ZIP에는 들어 있지 않다. 후속 보고서가 두 actor의 similarity `0.9952368736`과 평가 `remark`의 `0.9952` 일치를 제시하지만, 계산 재현이나 백엔드 구현 확인 없이 cosine 판정식·합격선을 확정하지 않는다. 이 백업은 새 학습 Run이나 original 4800 제출물의 설정 파일이 아니다. 제출 provenance 운영상 의미는 `05`를 따른다.

새 numbered final checkpoint의 동일한 정성 확인에는 personal 서버에서만
`issacsimz_video_suite.sh go2 --checkpoint <PATH>`를 쓴다. 이 경로는 checkpoint를 evidence staging
root의 격리 사본으로 six terrain에 렌더하고 source SHA가 붙은 labeled video evidence·handoff를
만든다. canonical task `exported/model_best.pt`는 교체하지 않는다. `--from-run`의 자동
`model_best.pt`를 몰래 대체하지 않으며, 영상 여섯 개를 evaluator나 checkpoint tournament로
해석하지 않는다. official에서 거부되는 것은 이 PERSONAL 자동 suite 스크립트다. 공식 서버의 6지형 영상 제작 자체가 금지된 것은 아니며, 필요하면 운영진 제공 `play.py`를 지형별로 직접 실행한다([17](17_ISSACSIMZ_VIDEO_OPERATIONS.md)).

4300→4800 actor relative L2 drift는 `18.75%`, 4800→4900은 `9.83%`로 보고됐다. 즉 4300과 4800은 의미 있게 다른 fresh 정책이고, 4900은 4800을 완전히 대체한 새 정책보다 refinement에 가깝다. 이 수치 역시 행동 성공률이 아니므로 six-terrain 평균·worst terrain·tracking·fall·seed variance를 동일 조건에서 측정한다.

fixed evaluator의 `success_timeout_pct`는 task 성공률이 아니라 `base_contact` 없이 20초 timeout에 도달한 비율이다. inverted stairs에서 세 모델은 95~100% timeout이지만 XY RMSE `0.917~0.970`, 전진 변위 `1.16~2.28 m`에 그쳤다. 따라서 생존과 terrain traversal을 분리하고, 후속 evaluator에는 명시적 진행 거리·통과 기준과 multi-seed worst case를 둔다.

native 영상의 판독 우선순위는 fixed quantitative benchmark보다 아래다. 동일 terrain 안에서 몸통 roll/pitch, 발 걸림, 충돌 후 회복, 옆 drift, 진동 증가를 비교하되 화면 안의 순간 전진이나 20초 생존을 완주로 바꾸지 않는다. 후속 traversal 영상은 `vx/vy/yaw`, curriculum OFF, difficulty 1.0, 시작 heading과 진행 방향을 고정하고 world-frame 전진률·heading error·lateral drift·terrain completion·recovery를 별도 지표로 남긴다.

최종 기술 개선 리포트에는 이 결과를 “`g2-submit-3 / LINTRACK-150-LINZ-2` 두 항의 독립 효과”로 쓰지 않는다. 이 설정은 두 항을 동시에 바꾼 조합이며, fixed batch는 공식 checkpoint의 개인 inference 비교다. 보존된 원문은 submission 전 near-final draft이므로 historical source로 둔다. 이후 original 4800 matching export·공식 Round-3 제출 평가는 완료됐지만, 새 제출 문서는 현재 artifact와 평가 사실로 다시 작성한다.

## 예선 3라운드 Go2 제출 평가와 다음 보고서

후속 **g2-submit-5 / LINTRACK-125**의 [2026-10-08 공식 평가](../experiments/go2/analysis/2026-10-08_OFFICIAL_EVAL_GO2_ROUND5_LINTRACK125.md)는 **88.32/100(시뮬 58.32/70·설계 의도 20/20·리포트 10/10)**이다. Round-3 대비 종합 **+0.77**, 시뮬레이션 **−0.23**, 계단 **8.52→8.35**로, PERSONAL paired evaluator의 계단 tracking 개선과 공식 점수는 다른 결론이다. 운영진 답변상 계단은 생존 이득 약 **+0.07점**보다 추종 손실 약 **−0.24점**이 컸고, 전방위는 survival **100%**로 같지만 tracking **0.834→0.829**로 약 **−0.06점**이다. 나머지 다섯은 survival **100%**(R5 도메인만 **99.9%**), tracking 차이 **0.003 이하**, 각 점수 차이 **±0.02 이내**다. 제출 terminal은 7450이고 7050이 아니다. 이 구성 설명만으로 reward-effect HOLD를 승급하거나 새 GPU 실행을 시작하지 않는다.

original `model_4800` actor와 matching `env.yaml`으로 만든 `g2-submit-3` 제출 snapshot(`submission-go2-prelim-r3-20260915`; registry legacy G-005 Run 07)은
2026-09-16 Round-3 평가에서 **87.55/100**을 받았다(시뮬레이션 58.55/70, 설계 의도 19/20,
리포트 품질 10/10). 시나리오 점수는 거친 지형 11.80/14가 가장 높고, 계단 10–15 cm 8.52/10.5가
가장 낮았다. 이 공식 결과는 original-4800 submission snapshot에만 귀속하며 4900 recovery나
개인 evaluator의 직접 점수로 일반화하지 않는다.

운영진은 설계 의도 19와 20을 가르는 정확한 단일 요인은 AI 평가라 특정할 수 없다고 답했다.
미해결 문제가 남으면 만점이 아닐 수 있다는 해석만 유지한다. 따라서 실패한 `ang_vel_xy_l2`
강화와 원복, 두 항을 함께 바꾼 `LINTRACK-150-LINZ-2`의 인과 한계, fresh 5K 중단, checkpoint별 안정성 trade-off를
숨기거나 성공 서사로 평탄화하지 않는다. 실제 설정·전후 결과·원복·선택 근거를 정확히 연결하는
현재 기록 방식은 리포트 품질 10/10을 받았으며 다음 라운드에도 유지한다.

## 공식 Go2 baseline 1K: 생존과 추종의 차이

2026-09-13 공식 run `20260913-145026-go2-b0-1k-official`은 4096 env, 1000 iteration(0~999), headless로 완료됐다. 수신 분석 보고서의 핵심 endpoint·console·checkpoint hash는 canonical bundle과 재대조했다. 전체 console 1000개 구간 중 iter 322~999의 678개 구간에서 terrain이 `0.0000`으로 표시된다. 이는 콘솔 소수점 네 자리 기준이며 더 작은 양수까지 정확히 0으로 확정하지 않는다.

최종 terrain 표시 `0`, XY error `1.8421`, yaw error `0.3082`, episode length `975.33`, timeout `93.45%`, base-contact `6.55%`, action std `0.44`, value loss `0.0058`이다. 쉬운 지형에서 생존은 길지만 선형 속도 추종이 약한 상태로 해석한다. 보고서는 11개 checkpoint의 tensor finite 검사를 통과했다고 기록한다. 이 finite 검사와 낮은 자세의 영상 행동 관찰은 보고서 분석 결과이며 이번 문서 통합에서 재실행한 검사는 아니다.

reward peak는 iter 794의 `14.17`이고, 보존된 `model_best.pt`는 SHA-256 대조상 `model_800.pt`와 동일하다(`99ceeaa1a3a1ebee972841a771072b711744a1c8dec6e94b318b55f146dc4676`). 자동 reward best와 최종 999 checkpoint, locomotion 성능 best를 구분한다. terrain collapse만으로 baseline의 장기 가능성을 기각하지 않는다.

개인 `LINTRACK-150-LINZ-2` 계보의 terrain `2.8915`·XY `0.7050`은 이 공식 기준선보다 좋고 yaw `0.4860`은 더 높다. 서버/GPU와 두 reward 변경이 함께 달라 paired 인과 비교가 아니다. 이 조합의 회복 가능성과 `LINTRACK-125` 단일변수 검증을 구분하고 기존 1K→3K→경쟁력 있는 5K 절차를 유지한다.

## 자주 생기는 실패

| 증상 | 우선 점검 |
| --- | --- |
| 통통 튀거나 미끄러짐 | 수직 속도·접촉·자세 안정 항목의 균형. |
| 발을 과도하게 들어 절뚝거림 | `feet_air_time` 같은 보상 항목 과대 여부. |
| 험지에서만 무너짐 | 지형 난이도 노출과 속도 추종 가중치의 trade-off. |
| 오래 학습해도 영상 품질이 나쁨 | reward를 여러 개 동시에 바꿨는지, play 조건이 같은지 확인. |

## 제출 판단

평지 지표가 좋아도 험지·경사·계단 검증이 빠지면 후보로 확정하지 않는다. 설정과 결과를 실험 기록에 남겨 H1과 Go2의 시간 배분을 근거 있게 결정한다.

## 개인 Go2 9.5k·5k 실행 (2026-08-30)

출처: `data/processed/experiments/go2/2026-08-30_GO2_BASELINE_CONVERSATION_SUMMARY.md`. 개인 L40S 검증이며 공식 평가 점수가 아니다.

요청 명령: `Quadruped-v0`, 4096 envs, `--max_iterations 12000`, `--headless`, seed 42, 기본 reward. Isaac Sim `5.1.0-rc.19+release.26219.9c81211b.gl`, Lab `3e73d6dd`, RSL-RL 5.0.1, PyTorch `2.7.0+cu128`.

12k는 완주하지 못했다. 최종 예외는 `RuntimeError: normal expects all elements of std >= 0.0`이지만, 최초 관찰 이상은 action std가 아니라 **value loss 발산**이다.

| iteration | value loss | 상태 |
| ---: | ---: | --- |
| 9500 | 0.0143 | 정상. 이 시점 checkpoint가 `model_9500.pt` |
| 9512 | 2.34 | 첫 뚜렷한 이상 |
| 9515 | 1.04e6 | reward -2008, action-rate 극단 |
| 9516~9520 | 정상대 | 일시 회복 |
| 9524~ | 재발산 | 9532 inf, 9535 nan 뒤 std 오류로 종료 |

`model_9500.pt`는 깨진 모델이 아니다. actor/critic/optimizer는 finite, action std min/mean/max = 0.300 / 0.477 / 0.593. 발산 전 개인 B0로 보존한다. 수렴·공식 점수·재개 안정성은 보장하지 않는다.

편의상 “5k 모델”은 **정확한 5000 checkpoint가 아니다.** `Train/mean_reward` peak 4509에 가까운 `model_4500.pt`다. 이 checkpoint std는 0.292 / 0.482 / 0.660으로 9500과 비슷하다. 장기 std 수축으로 음수가 됐다는 가설은 폐기한다.

| 학습 내부 지표 | 4509 (`model_4500`) | 9500 (`model_9500`) |
| --- | ---: | ---: |
| XY error (m/s) | 1.1683 | 0.7192 |
| terrain level | 0.9181 | 5.8252 |
| base-contact termination | 1.60% | 1.91% |

초기 후보는 낙상이 적어도 추종이 약하다. 9.5k는 추종·지형이 나아졌지만 모든 지표가 좋아진 것은 아니다. 동일 evaluator 점수가 아니다.

play 영상 `go2_best_5k_120s.mp4`, `go2_best_9500_120s.mp4`가 있다. 학습은 4096 env, 영상은 로봇 1대·1×1 terrain·6000 step(120초). 120초는 여러 episode이며 연속 생존 증명이 아니다. 영상 OOM(10000 step)은 학습 발산과 별개다.

운영진: 장기 Go2 발산은 알려진 확률적 수치 불안정이며 9.5k 결정적 임계값이 아니다. 제출용은 배포 PPO를 유지하고 reward·iteration만 조절한다. 개인에서 lr/`desired_kl` 진단은 별도 실험 ID. 발산 시 report 조언은 부정확할 수 있고 수정 예정이라 했다.

비교 때 5k 선별(`model_4500`)과 9.5k(`model_9500`)와 12k 미완주를 섞지 않는다. 원본은 originals `data/raw/private_server_runs/go2/2026-08-30_brev_l40s_baseline_5k_9500iter/`, 릴리스 `brev-go2-recovery-20260830_125132_KST`. 영상 운영은 `11`, 보존은 `16`, 운영진 전문은 `data/processed/experiments/go2/2026-08-30_ORGANIZER_REPLY_GO2_DIVERGENCE.md`.

## L40S 벽시계 (`go2-12k.log` 실측)

추정 아님. 같은 12k 시도 로그에서 iteration 0~9535의 `Time elapsed`를 파싱했다. 4096 envs, iteration당 98,304 sim steps. 상세 표는 `data/processed/experiments/go2/2026-09-11_GO2_12K_WALLCLOCK_FROM_LOG.md`.

| 지점 | 누적시간 | 비고 |
| ---: | ---: | --- |
| 1,000 | 01:16:44 | 예전의 “1k≈70분”보다 김 |
| 5,000 | 05:56:33 | 예산 기준점 |
| 9,000 | 10:34:00 | 2.5k~9k는 500iter당 약 34~35분 |
| 9,500 | 11:21:55 | **일반화 금지.** 9k→9.5k가 47:55 |

iter 9451에서 SPS 176, collection 491s + learning 67s ≈ 558s. 평소 iteration은 약 4.1~4.3초. 그래서 9500 누적시간을 정상 9.5k 학습시간으로 쓰지 않는다.

개인 Go2 실험 예산: **5k ≈ GPU 6시간**, 3k screening ≈ 3시간 40분. 가설 다섯 개를 모두 5k면 약 30 GPU-hours. H1 공식 1K 12분·TERM-50 5K 1시간과 섞지 않는다.

## Optuna 초기 탐색 범위

첫 study는 현재 활성화된 key 세 개만 좁게 탐색한다.

- `track_lin_vel_xy_exp`: 0.75~1.50
- `feet_air_time`: 0.01~0.15, log sampling
- `lin_vel_z_l2`: 절댓값 1.5~5.0을 log sampling한 뒤 음수 적용

흔들림·동작 급변이 병목으로 확인된 뒤에만 `ang_vel_xy_l2`와 `action_rate_l2`를 별도 단계로 연다. 주석 처리된 optional reward는 실제 환경 적용이 로그나 `env.yaml`로 확인되기 전에는 탐색 변수로 넣지 않는다.
