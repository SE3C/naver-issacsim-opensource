---
title: "H1 공개 실패 38건 × 내부 계보: GPU 시간을 아끼는 실험 prior"
purpose: "AI upload bundle — 공개 researchlog의 재사용 가능한 실패 지도, 인과 경계, 다음 통제 실험"
sources:
  - "data/processed/incoming/other/reviewed/NCRC_H1_EXTERNAL_INTERNAL_SINGLE_DELTA_ANALYSIS_20260923.md"
  - "data/processed/incoming/other/reviewed/NCRC_H1_VISUAL_FAILURE_DEEP_ANALYSIS_20260923.md"
  - "data/processed/incoming/other/reviewed/NCRC_EXTERNAL_FAILURE_EVIDENCE_FOR_DATABASE_20260922.md"
  - "data/processed/incoming/other/reviewed/NCRC_VIDEOS_JSON_DEEP_ANALYSIS_20260922.md"
  - "data/processed/reference/public/2026-09-22_ncrc_public_data_audit/README.md"
  - "data/processed/reference/public/2026-09-22_ncrc_public_data_audit/NCRC_PUBLIC_DATA_AUDIT_20260922.zip"
  - "data/processed/experiments/h1/analysis/2026-09-21_H1_PARENT_AIRTIME_LINEAGE_CORRECTION.md"
  - "research/EXPERIMENTS.md"
  - "data/processed/incoming/other/reviewed/H1_H010_FRESH3K_R01_VS_H005_FRESH3K_R01_DEEP_ANALYSIS_20260927.md"
  - "data/processed/experiments/h1/analysis/2026-09-30_OFFICIAL_EVAL_H1_ROUND4_AIRTIME025.md"
type: "external_observation_and_experiment_design"
---

# H1 공개 실패 사례를 값싸게 활용하는 방법

**2026-10-18 내부 후보3 관측:** [LIN075 + ACT0001/2850 보고서](../experiments/h1/analysis/2026-10-18_H1_LIN075_ACTION0001_MODEL2850_POLICY_REVIEW.md)는 H5 진행9.867m·P05 9.640m·stall>.05 0/384와 동시에 H4/H5 yaw .2725/.2730rad/s를 보여 **HOLD**다. 진행 증가를 추종 전반 개선으로 바꾸지 않으며, 공개 타팀 실패나 reward 단독 인과의 증거로 합치지 않는다. 원문 비교는 미대응 참고이고 matched CPU 비교는 미실행이다.

**2026-10-17 내부 후보2 관측:** [자세·hip 완화형2850 보고서](../experiments/h1/analysis/2026-10-17_H1_JOINT_TRACKING_POSTURE_MODEL2850_POLICY_REVIEW.md)는 **HOLD**다. 생존3072/3072에도 H5 진행8.024/10m, P05/최소7.460/6.721m·stall>.05 1/384로, 완전 정체가 드물어도 속도 손실이 남는다. H1/H3 body 후진−.719/−.679m도 별도 비용이다. 우리 PERSONAL 평가 결과이지 공개 타팀 실패나 공식 점수가 아니며, 여러 reward·학습량 차이 때문에 자세/hip 완화의 인과효과를 말하지 않는다.

**2026-10-17 joint tracking 내부 관측:** [lin=.65/ang=.60/action=-.0003 fresh5K keeper4950 보고서](../experiments/h1/analysis/2026-10-17_H1_JOINT_TRACKING_MODEL4950_POLICY_REVIEW.md)는 수신 완료/**HOLD**다. H5 생존384/384·stall>.05 0건이어도 진행평균8.853m가 명령적분10m보다 작다. 즉 낙상·완전 정체와 지속 저속은 별도 문제다. 공개 타팀 실패와의 원인 동일성·세 reward의 개별 효과·공식 점수 향상은 미입증이며 기존 LINTRACK065 raw와의 CPU 비교도 별도 미실행이다.

**2026-10-17 내부 관측:** [action=-.0002 keeper2950 단독 보고서](../experiments/h1/analysis/2026-10-17_H1_ACTION0002_MODEL2950_POLICY_REVIEW.md)는 **HOLD**다. 생존3072/3072와 H5 진행8.941m만으로 정지·좌우 명령 대응까지 개선됐다고 판단하지 않는다. 이는 우리 PERSONAL 평가 관측이며 타팀 공개 실패의 원인이나 -.0003 대비 보상 효과를 입증하지 않는다.

**2026-10-16 action=-.0003 내부 관측:** [fresh3K keeper2950·보고서](../experiments/h1/analysis/2026-10-16_H1_ACTION0003_MODEL2950_POLICY_REVIEW.md)는 완료/HOLD다. PERSONAL 3072/3072 생존에도 H5 진행mean/P05/min9.018/8.664/6.771m와 두 stall outlier가 남는다. 정지 누수 감소 가능성과 rough 진행 손해 가능성을 동시에 보며, 공개 타팀 자료의 인과나 공식 점수 향상으로 확대하지 않는다. 기존 model2700과의 상대 raw 대조는 이번 보고서에서 미실행이다.

**2026-10-16 내부 후속:** [angxy=-.08 보고서·5정책 CPU 비교](../experiments/h1/analysis/2026-10-16_H1_ANGXY008_MODEL4650_POLICY_REVIEW.md)는 HOLD다. H5 저속은 높은 낙상·완전 stall과 다르며, body-rate 벌점 강화가 자세/추종 개선을 보장하지 않았다. 이것은 공개 타팀 실패의 인과가 아닌 우리 INTERNAL PERSONAL 평가 관측이다. [다음 제안·연구](../planning/2026-10-16_H1_EVIDENCE_AND_RESEARCH_NEXT_EXPERIMENTS.md): 당시 action=-.0003 fresh3K 제안은 위 실제 Run·보고서 HOLD로 갱신됐다. resume는 별도 미실행이다. 아래 날짜별 미실행/평가대기 표현은 당시 기록이다.
> 날짜별 업데이트는 해당 시점의 기록이다. 최신 Run·제출 상태는 [현재 Experiment registry](../../../research/EXPERIMENTS.md)를 우선한다.

## 2026-10-11 model_9999 내부 관찰 — 외부 prior·인과 비교와 분리

[model_9999 정책 검토](../experiments/h1/analysis/2026-10-11_ACTRATE0001_MODEL9999_POLICY_REVIEW.md): ACTRATE-0001 fresh10K model_9999는 20초 3,072episode 전부 생존했지만 rough 전진 평균/P05/최소 8.915/8.251/6.492m, 최악 seed4202/env57 stall 0.104를 기록했다. 낮은 낙상만으로 진행 성공을 선언하지 않는 기존 공개 실패 prior와 함께 참고한다. 여섯 영상에서는 boxes/rough 초기 패치 이동이 관찰됐으나 연속 계단 완주는 미입증이다. **HOLD**이며 model2700과 같은 조건의 직접 비교나 reward 효과로 해석하지 않는다.



## 2026-10-11 ACTRATE-001 / model_2850 — 내부 PERSONAL 행동 결과와 공개 prior 분리

[2026-10-10 원문 분석](../incoming/other/reviewed/H1_MODEL2850_SHA1E6D_POLICY_ANALYSIS_20261010.md) · [2026-10-11 정책 검토](../experiments/h1/analysis/2026-10-11_ACTRATE001_MODEL2850_POLICY_REVIEW.md) · [Experiment](../../../research/experiments/h1/exp-h1-action-rate-smoothing.md). OFFICIAL `ACTRATE-001` fresh3K best `model_2850` SHA `1e6d…bb1`로 기존 개인 Windows `scenario7`을 평가한 보고서: **3,072/3,072 timeout 생존**, H2/H7 body 이동 **15.470/10.656m**, H6 상/하 경사 전진 **20.297/20.058m**. 하지만 H1 정지 world 이동 평균 **1.151m**, H3 왕복 world 이동 평균 **2.177m**, rough H5 P05 body 진행 **8.921m**와 계단 중앙 통과 미검증 때문에 범용 정책 **HOLD**다. 다른 팀의 공개 실패 사례가 아닌 우리 자체 INTERNAL/PERSONAL 행동 기록이며, 이전 `ORIENT-100/model_2850` SHA `6aed…f7b0`·`ACTRATE-0001/model_2700`와 분리한다.

외부 reward 성공/실패 prior와 단일 후보 생존 결과는 `action_rate_l2=-0.001`의 독립 인과 증거가 아니다. 기존 `TERM-50/model_2800`의 동일 프로토콜 raw 대조부터 시도하고 평가 source·seed·cohort parity가 맞지 않으면 HOLD 유지한다. 신규 GPU 또는 Optuna trial 없음.


## 2026-10-10 ACTRATE-0001 combinations — 2026-10-14 three completed, two planned

> unchanged control [Run `20261014-111135-h1-actrate-0001-unchanged-cont2k`](../../../research/experiments/h1/exp-h1-action-rate-relaxation.md)는 동일 부모2700 SHA·reward 유지 +2K OFFICIAL 학습 COMPLETED/PASS다. 후속 PERSONAL 평가·부모/4650 raw 비교도 완료했으며, 범용·전진/험지 대표는 REJECT다. 아래 초기 가설 개수에 control을 처리 가설로 합치지 않는다. 인과 한계는 유지한다.

[Selected H1 ACTRATE-0001 five-question plan](../planning/2026-10-10_H1_ACTRATE0001_FIVE_COMBINATION_HYPOTHESES.md). Existing `ACTRATE-0001/model_2700` PERSONAL evaluation showed H5 rough mean/P05 `9.948/9.592m` plus unfavorable H1 unintended body forward `1.987m`, H3 unwanted forward `1.677m` and overall action Δ RMS `0.45687`. Two fresh combinations (action+AIRTIME; action+feet_slide) and three one-step sibling resumes (AIRTIME, XY tracking, XY angular rate) are hypotheses to test those weaknesses, **not** observed reward successes.

Frozen `h1-submit-2` has active `feet_slide=-0.25`; measured H3 foot slipping is absent, so strengthening it is not a verified H3 fix. Historical corrected PERSONAL LINTRACK-075/H-010 tradeoffs are not OFFICIAL ACTRATE-child causal evidence. **2026-10-16 현재 lin=.65·angxy=-.08 resume와 fresh action+airtime/action+feet_slide는 학습·평가·보고서 수신 완료, 채택 HOLD**다. 최초 다섯 계획 중 **resume AIRTIME만 PLANNED**다. 별도 ACTRATE-001도 위 완료 기록을 따른다. 완료 자체를 reward 성공이나 Optuna outcome으로 해석하지 않는다.

model4650은 3,072회 무낙상이어도 H3 world XY 잔류2.398m와 H4 yaw .179rad/s가 남아 **생존≠명령/위치 복귀 성공**의 내부 관찰이다. [2026-10-14 4정책 CPU 비교 보고서·CSV](../experiments/h1/analysis/2026-10-14_H1_4POLICY_LINTRACK065_COMPARISON_INTAKE.md)에서 부모2700 대비 x/y 오차 개선과 H5 진행 평균/P05 9.948/9.592→9.546/9.228m 악화가 공존한다. 이번 수납에서 원본 평가 ZIP 전체 재검증은 하지 않았다. 동일 부모 unchanged +2K 대조군 학습은 이후 완료됐지만 행동 평가·비교가 없어 연장 학습과 reward 전환 효과를 분리하지 못하며 범용 승격 HOLD를 유지한다. 9999는 별도 fresh10K, 당일 lin=.65 fresh5K는 action=-.0005인 다른 설정/계보다. 공개 실패 사례의 인과나 공식 점수로 해석하지 않는다.


## 2026-10-10 ANGTRACK-065/TERM-50 기존 raw 대조 — 만성 횡이동 정체 확인

[기존 평가 두 ZIP 직접 대조 보고서](../experiments/h1/analysis/2026-10-10_H1_ANGTRACK065_TERM50_DEEP_RAW_COMPARISON.md). **ANG H3 종료 15건을 제외해도** 정상 20초 timeout 369개에서 횡속도 오차 `0.18087`, stall `0.33889`로 같은 cohort TERM `vy_error≈0.06847`, stall≈`0.00913`보다 크다. 처음 384개 기준 H3 vy error와 stall은 **384/384** ANG가 TERM보다 나쁘다. H4 yaw error는 384/384 ANG 우세(`0.07704` vs TERM `0.11934`)이나 H5 평균 진행은 거의 같고, 전체 `xy_rmse`는 ANG가 더 크다. 이 기록은 우리 보존 INTERNAL PERSONAL 결과의 동일 평가 인덱스 비교이지 외부 공개 실패 확률이나 단독 reward 계수 인과를 입증한 것이 아니다. **ANG all-terrain HOLD**. 기존 단일정책의 matched-control 미분석 표기는 역사적 상태.

## 2026-10-10 ANGTRACK-065 — 측면 명령 base-contact와 재시작 행 분모 문제

[원본 단일 정책 분석](../incoming/other/reviewed/H1_ANGTRACK-065_POLICY_ANALYSIS_20261010.md) · [Experiment·행동 판정](../experiments/h1/analysis/2026-10-10_ANGTRACK065_MODEL2950_POLICY_REVIEW.md). OFFICIAL fresh3K `ANGTRACK-065` Run `20261009-155344-h1-angtrack-065-fresh3k`의 best/keeper `model_2950.pt`를 Windows PERSONAL 평가한 결과, **횡이동 H3에서 최초 384 cohort 중 15회 base-contact 종료(3.91%)**. 각 종료 cohort의 `-n1` 짧은 `evaluation_end`가 추가되므로 3,072 최초 cohort에 3,087 raw episode행, H3만 399행이다. H3 399행 생존률 **96.24%**는 단축 재시작을 포함하므로 **최초 20초 timeout 생존 369/384=96.09%**와 구분해야 한다. H3 stall `0.3532`, vy error `0.1871m/s`이어서 낮은 yaw error/적은 action 변화만으로 lateral 제어 성공을 인정할 수 없다. H1 정지 명령에도 body 전진 `+0.875m`; 반면 H2 전진 `14.703m`, H5 rough `8.895m`, H6 경사, H7 외란 이동 등 전진형 증거는 있다.

**후보 HOLD:** H3 협소공간·횡이동 안정성 미달. 영상 6개는 순수 H3 명령을 담지 않으며 stairs/boxes에 대한 정량 `scenario7` case 없음. `06_slope_down_10deg.mp4` 짝수 500 검정 프레임은 해당 ANGTRACK 영상 캡처 결함이며 다른 정책의 검정 프레임 사례와 섞지 않는다. 이전 `ANGTRACK-075` BASE 1K collapse나 공개 yaw 실패는 외부·별개 계보 prior이지 해당 0.65 reward 효과의 인과 증거가 아니다. 기존 9,216-row `TERM-50/ORIENT/ACTRATE` raw 비교에는 ANGTRACK 자료가 없고, `TERM-50 model_2800` raw 대조는 아직 별도 미수행이다.

## 2026-10-10 H1 내부 실패 신호 — 기존 세 ZIP 직접 읽기로 확정된 관찰

[TERM-50/ORIENT-100/ACTRATE-0001 원본 9,216 episode 직접 분석](../experiments/h1/analysis/2026-10-10_H1_SCENARIO7_RAW_3POLICY_MATCHED_ANALYSIS.md) · [case 집계 JSON](../experiments/h1/2026-10-10_H1_SCENARIO7_RAW_SUMMARY.json) · [코호트 대응 차이 JSON](../experiments/h1/2026-10-10_H1_SCENARIO7_PAIRED_DELTAS.json). 이번에는 기존 GitHub에 있던 ZIP 3개를 **사용자가 업로드해 직접 추출**했고 SHA/CRC, 동일 원본 resolved 평가 설정·24 case/seed fingerprint와 3,072×3 episode/cohort ID를 확인했다. 기존 문서의 “TERM-50 raw 미추출”은 이전 상태다.

- **새로 확인한 대조군 실패:** `TERM-50/model_2800`도 rough H5 `seed4201/env16`에서 전진 **2.639m**, stall **0.611**, tracking **0.4543**인데도 20초 생존. H5 평균/P05는 **8.896/8.533m**이고 384 rough episode 중 전진 `<9.5m`는 **374개**. zero-command 비의도 전진은 **1.352m**로 세 후보 중 가장 작지만 정상적 제자리 유지 완료는 아니다.
- **ORIENT 행동 비용:** tracking 전체 **0.14041**(TERM **0.15712**보다 낮음), rough 평균 진행 **9.451m**, H1 전진 누수 **1.633m**. **roll/pitch RMS 0.08015**는 TERM **0.03381**, ACTRATE **0.03019**보다 높아 단순 “가장 안정적” 표현을 경계한다. **ACTRATE 행동 비용:** rough 평균/P05/min **9.948/9.592/8.815m**로 가장 높고 모든 rough 대응 인덱스에서 TERM보다 전진 증가, H1 전진 누수 **1.987m**, action Δ RMS **0.45687**로 가장 높다.
- **계보·판정:** 둘 다 독립 OFFICIAL fresh3K 정책의 후속 PERSONAL 평가, `LINTRACK-075`는 PERSONAL corrected5K로 별도. 학습 프로세스 완료·평가 생존·case tracking 개선·공식 점수는 다른 판정. 동일 cohort 인덱스가 실제 물리 terrain/episode의 동일성이나 reward 원인을 증명하지 않는다. 모두 HOLD; 새 GPU 자동실행·원본 수정·Optuna trial 없음.

## 2026-10-10 H1 다정책 내부 실패 신호 비교 — 원본 GitHub 위치와 raw 미검증 경계

[비교 기록](../experiments/h1/analysis/2026-10-10_H1_SCENARIO7_CROSS_POLICY_REPORT_LEVEL_COMPARISON.md). OFFICIAL fresh3K TERM-50 `model_2800`, ORIENT-100 `model_2850`, ACTRATE-0001 `model_2700`의 동일 protocol PERSONAL `scenario7` full ZIP은 **모두 GitHub Originals/Release에 존재**한다. 그러나 연결된 API는 실제 private ZIP bytes를 열지 못해 이 단계에선 **원문에 보고된 각 정책별 통계만 대조**했다. ORIENT는 행동 추종·action-change RMS가 전반적으로 낮고 ACTRATE는 rough P05 진행·전진/경사 추종이 유리하지만, H1 정지 body leakage ORIENT 1.633m·ACTRATE 1.987m, H3 횡이동 ORIENT 1.180m·ACTRATE 1.677m라는 실패 축이 뚜렷하다. rough H5 최소 진행은 ACTRATE 8.815m, ORIENT 7.831m, PERSONAL corrected LINTRACK 2.871m지만 **각각 다른 worst cohort이므로 1:1 동일 terrain 개선이라고 단정하지 않는다**. LINTRACK의 최악 stall 0.664는 전체 rough 384건 중 심한 한 사례이지 전부 실패가 아니다. TERM-50 baseline 실제 수치·같은 seed/env 초기 상태 확인 전에는 대조 개선·reward 원인·OFFICIAL 점수 모두 HOLD다. 기존 영상의 검정 교대 프레임은 캡처 결함이다.

## 2026-10-10 ACTRATE-0001 model_2700 — 내부 행동 성공과 실패 신호

공개 타 팀 사례가 아닌 **우리 OFFICIAL 학습 정책을 Windows PERSONAL로 평가한 사용자 제공 분석**이다. [원문](../incoming/other/reviewed/H1_MODEL2700_POLICY_ANALYSIS_20261010.md) · [판정 요약](../experiments/h1/analysis/2026-10-10_ACTRATE0001_MODEL2700_POLICY_REVIEW.md). OFFICIAL fresh3K `ACTRATE-0001` Run `20261009-142350-h1-actrate-0001-fresh3k`의 auto-best `model_2700.pt` SHA가 후속 Windows 평가 policy SHA와 일치한다. 하지만 정책 최종 keeper `model_2950.pt`가 아니라는 점과 ZIP의 null source_run_id는 유지한다.

- **성공:** 3,072/3,072개 20초 생존, base-contact 종료 0. H2 전진 15.326m(명령 적분 15m), H7 외란 전진 10.542m(명령 10m), H6 경사 상/하 20.052/19.834m(body-frame). 박스·초기 rough 실제 이동은 영상에서 정성적으로 지지된다.
- **실패 유형:** 정지 H1 body 비의도 전진 **1.987m** 및 월드 XY 순변위 크기 중앙값 2.012m; 횡이동 H3 비의도 전진 **1.677m**. H5 rough `seed 4202/env 108`은 전진 8.815m, tracking 0.2908, roll/pitch RMS 0.0999의 조건별 악화가 있으나 전체 rough의 붕괴로 과장하지 않는다. 중앙 다단 계단 통과/별도 stairs 평가 결과는 없다. `01_stairs.mp4` 교대 검정 프레임은 낙상이 아닌 캡처 결함.
- **의사결정:** 전진 보행 내부 후보 **HOLD**. 높은 생존률은 zero-command 성공·계단 완주를 보장하지 않는다. `action_rate_l2=-0.0001` 인과적 보상 효과나 공식 NCRC 점수를 증명하지 않는다. 원본 `TERM-50 model_2800` 동일 evaluator raw 대조를 우선하고 `ORIENT-100/model_2850`은 2순위 행동 참고 비교로 둔다. 새 GPU를 실행하지 않는다.

## 2026-10-10 내부 LINTRACK-075 corrected5K 행동 실패/성공 분리

이번 근거는 **공개 다른 팀 자료가 아니라 우리 개인 Windows 평가 보고서**다. [원문](../incoming/other/reviewed/H1_LINTRACK-075_CORRECTED5K_POLICY_ANALYSIS_20261010.md) · [H-008 행동 판정](../experiments/h1/analysis/2026-10-10_LINTRACK075_CORRECTED5K_MODEL4997_POLICY_REVIEW.md).

- `model_4997.pt` SHA `4349fe56…b6d`(PERSONAL corrected H-008 R04)의 `scenario7` 3,072/3,072 20초 생존, H2 body 15.015m / H7 push 10.038m / H6 경사 19.943/19.776m는 **생존을 넘는 이동 능력**을 보여준다.
- 그러나 rough H5 단일 cohort `seed 4202/env 41`은 20초 생존에도 전진 2.8708m·stall 66.4%. 전체 rough 384건에서 stall>0.05는 한 건이며, 이를 전체 붕괴로 과장하거나 평균 100% survival로 덮지 않는다. H1 zero-command 월드 순변위 0.516m, H3 왕복 1.280m, slope yaw 절대오차 0.2613rad/s 및 action Δ RMS 0.5098(하행)도 별도 위험 축이다.
- Boxes 영상에는 실제 블록 접지·전진이 있지만 stairs/inverted-stairs **다단 중앙 통과 성공은 미검증**이고 camera-off stairs/boxes case는 없다. 영상과 정량 평가의 trajectory를 합치지 않는다. `06_slope_down_10deg.mp4` 교대 검정 프레임은 캡처 artifact로, 낙상으로 집계하지 않는다.
- **HOLD**: 행동 후보로 보존하되 `lin=0.75` reward 변경의 인과적 성능 개선이나 OFFICIAL 정책 채택은 증명되지 않는다. 1순위 비교는 기존 보존 `h1-submit-2 / TERM-50` 동일 `scenario7` source/agent/command/terrain/seed/horizon parity 확인 뒤 H5 worst-tail 및 H1/H3·H6·H7 raw cohort 비교. 신규 GPU 작업은 승인하지 않는다.

## ORIENT-100 내부 관찰로 확인한 실패 prior 해석 (2026-10-07)

외부 공개 researchlog의 위험 신호와 **우리** H1 `ORIENT-100 / model_2850` PERSONAL 고정 평가 결과는 출처가 서로 다르다. 내부 `scenario7`은 **3,072/3,072 episode가 20초 생존**, 하지만 정지 H1 body 전진 **+1.633m**, lateral H3 비의도 전진 **+1.180m**, rough H5 **tracking 0.1709 / 진행 최소 7.831m**를 기록했다. 따라서 공개 실패 prior에서 강조했던 **높은 생존률만으로 지형 실제 진행과 명령 추종을 보장할 수 없다**는 위험 유형은 내부에서도 관찰 가능한 형태로 나타났다. 이것은 공개 실패 표본의 인과 효과·발생률을 검증한 통제 실험이 아니다.

`02_inverted_stairs.mp4`의 검정 짝수 프레임은 기록 품질 문제다. boxes/rough 초기 보행과 다단 계단 통과 여부는 분리하고, `flat_orientation_l2 -1.5→-1.0` reward 인과는 이제 확보된 동일 evaluator `h1-submit-2` 대조 자료의 숫자 차이가 있어도 train 반복·물리 reset/지형 동일성 및 PPO/source parity가 미확인이라 **HOLD**로 둔다. [원문 내부 분석](../incoming/other/reviewed/H1_ORIENT-100_POLICY_ANALYSIS_20261007.md).



## 2026-10-10 당시 H1 single-delta 현황(후속 ACTRATE-001 완료는 위 최신 단락 우선)

아래 9/22~9/23 공개 실패 분석은 그대로 보존한다. 다만 **현재 다음 H1 실행 순서**는 Round-4 공식 결과와 이후 확인한 외부 성공 사례를 반영해 갱신한다.

1. **OFFICIAL COMPLETE/PASS · PERSONAL 행동 HOLD(2026-10-07):** `exp-h1-rough-terrain-orientation-relaxation / ORIENT-100` — frozen `h1-submit-2` 대비 `flat_orientation_l2 -1.5→-1.0`, feet 0.20인 OFFICIAL fresh 3K Run `20261006-133517-h1-orient-100-fresh3k-official`. [접수·원본·Release](../experiments/h1/training/2026-10-06_ORIENT100_OFFICIAL3K_EVIDENCE_INTAKE.md). 실행 완료를 prior 검증 성공으로 해석하지 않는다.
2. **2026-10-10 OFFICIAL fresh3K COMPLETE/PASS · PERSONAL 행동 HOLD:** `exp-h1-action-rate-smoothing / ACTRATE-001` — frozen `h1-submit-2`에서 `action_rate_l2 -0.0005→-0.001`만 변경, Run `20261010-125324-h1-actrate-001-fresh3k`, best `model_2850` SHA `1e6d…bb1`, 단일정책 3,072 episode 생존이나 정지/횡왕복 이동 잔류로 HOLD. ORIENT checkpoint/config를 상속하지 않는다.
3. **2026-10-10 OFFICIAL fresh 3K COMPLETED/PASS · 분석 HOLD:** [`ACTRATE-0001 / exp-h1-action-rate-relaxation`](../../../research/experiments/h1/exp-h1-action-rate-relaxation.md) — `action_rate_l2 -0.0005→-0.0001` 단독 완화, Run `20261009-142350-h1-actrate-0001-fresh3k`; no parent, seed42, 4096 env. Auto-best `model_2700.pt`로 별도 PERSONAL 영상·scenario7 3,072 episode 평가 COMPLETE, 단일 정책 행동 분석 수신·정책 판정 HOLD, 2026-10-10 TERM-50 raw 대응-index 기술비교 완료(독립 Run 반복·reward 인과는 미검증). [train](../experiments/h1/training/2026-10-09_ACTRATE0001_OFFICIAL3K_EVIDENCE_INTAKE.md) · [Windows 평가](../operations/windows_h1_video_evaluation/2026-10-10_ACTRATE0001_MODEL2700_PUBLICATION.md).
4. **2026-10-10 OFFICIAL fresh 3K COMPLETED/PASS · 분석 HOLD:** [`ANGTRACK-065 / exp-h1-angular-tracking-boost`](../../../research/experiments/h1/exp-h1-angular-tracking-boost.md) — `track_ang_vel_z_exp 0.5→0.65` 단독 강화, Run `20261009-155344-h1-angtrack-065-fresh3k`; no parent, seed42, 4096 env, auto-best/keeper `model_2950.pt` 동일. 현재 PERSONAL 평가와 단일 정책 심층 분석 수신(H3 최초 cohort base-contact 15/384, all-terrain HOLD); 동일 TERM-50 raw 대조는 미완료. 과거 PERSONAL BASE `ANGTRACK-075` fresh1K 초기 붕괴는 별도 위험 prior이지 동일 실험의 성능 결론이 아니다. [train](../experiments/h1/training/2026-10-10_ANGTRACK065_OFFICIAL3K_EVIDENCE_INTAKE.md).
5. AIRTIME 추가 증가는 현재 후순위. Round-4 AIRTIME-025의 세 구성 점수 합계는 86.37/100으로 Round-2 종합 점수와 수치상 같았고, 약한 요철은 8.17→8.00으로 하락했다. Round-4 수신 원문에는 별도 종합 점수 필드가 없었다.

이 우선순위는 공개 실패 row에서 ORIENT가 강할수록/약할수록 좋다는 단조 결론을 얻어서 정한 것이 아니다. 공개 실패 데이터는 성공 reward detail이 비어 있고 대부분 다중 변경이라 방향성을 확정할 수 없다. 대신 다음 **성공 사례 prior**를 추가로 참고한다.

- IIT Delhi CoE-BIRD 2026 Unitree H1 uneven-terrain/staircase project: orientation penalty `-1.0`, linear/angular tracking `+1.0/+0.5`, action-rate `-0.01` 등으로 rough/stairs curriculum과 평가를 공개.
  - https://github.com/iitd-bird-robotics/2026-major-Bipedal_Locomotion_Using_RL
- public Isaac Lab H1 rough-terrain run: `flat_orientation_l2=-1.0`, `action_rate_l2=-0.005`; 공개 결과는 4K terrain 5.76/8, velocity error 0.24 m/s, fall rate 0.74%.
  - https://github.com/egeozgul/humanoid-locomotion-isaaclab
- Humanoid-Gym/RobotEra: zero-shot real-robot locomotion에서 tracking + gait/contact + clearance/slip + action smoothness를 함께 사용.
  - https://github.com/roboterax/humanoid-gym

외부 환경·reward 함수·scale은 NCRC와 다르므로 `-1.0`이나 더 강한 ACTRATE를 최적값으로 가져오지 않는다. 외부 성공 사례와 우리 Round-4 요철 하락이 함께 **`ORIENT-100` 단일변수를 먼저 시험할 정보가치**를 높였다고만 해석한다.

또한 2026-10-06 현재 H1 PERSONAL evaluator core를 재사용하는 Windows 통합 launcher가 `C:\NCRC\h1_6terrain_video.bat`로 설치됐고 CPU 회귀 테스트 60개와 PowerShell/설치 파일 검증을 통과했다. H1은 경사 ±10° 6영상 뒤 별도 camera-off `scenario7` 8 case 전체 평가를 사용하며 smoke 옵션은 제거됐다. 2026-10-07 `model_2850` 단일 정책 PERSONAL Windows GPU full 및 6영상 자료는 확보됐다. **2026-10-10 보존된 ZIP 3개를 이용한 9,216 episode 대응-key raw 비교를 추가 완료**했다. 다만 별도 Windows 비교 CLI·실제 동일 초기 지형 검증·인과 실험은 하지 않았다. 아래 과거 절의 "fixed eval"은 미래 검증 설계이며, 2026-10-10 이후 H1에는 이 원본 camera-off `scenario7` episode 기반 대조 수치도 있다; 더 오래된 TensorBoard·console·native 영상 분석과 구분한다. 세부 실행 계획은 [14](14_H1_NEXT_RUN_PARAMETER_COMPARISON.md), [ORIENT plan](../../../research/experiments/h1/exp-h1-rough-terrain-orientation-relaxation.md), [ACTRATE plan](../../../research/experiments/h1/exp-h1-action-rate-smoothing.md)을 따른다.


## 증거 등급과 재현 가능한 범위

이 자료는 2026-09-22 공개 researchlog의 읽기 전용 스냅샷이다. **대회 관련 공개 자료**라는 점에서 실험 질문을 고르는 데 가치가 높지만, 운영진이 채점한 우리 정책의 **OFFICIAL 성능 데이터**는 아니다. 다른 참가자의 정책 파일·parent·seed·실행 코드·동일 evaluator가 확인되지 않으며, 제출 점수나 성공 정책의 reward 최적값도 제공하지 않는다. 이 구분은 데이터의 유용성을 깎는 것이 아니라, 잘못된 결론으로 공식 서버 시간을 낭비하지 않기 위한 경계다.

원본 audit ZIP의 `04_failure_runs.csv`를 다시 확인하면 실패 key 47개 중 H1은 38개, Go2는 7개, 로봇 미상은 2개다. H1의 `actual_dial_count=1`은 **5개**다. 아래 빈도는 **선택되어 게시된 실패 표본 내부**의 기술통계이지 참가자 전체의 실패확률이 아니다. `trial`은 화면 번호이고 연결 키는 `key`다. 동형 지표를 가진 key 두 개가 독립 정책인지도 알 수 없다.

| H1 실패 표본에서 확인한 사실 | 해석에 남길 경계 |
| --- | --- |
| 38개 중 27개는 마지막 terrain level ≥5, 32개는 fall rate >20%, 34개는 exploration std ≥1 | 높은 curriculum 단계·reward·생존 중 하나만으로 unseen terrain 통과를 주장하지 않는다. 각 지표의 단위와 집계 window를 유지한다. |
| 구덩이/틈 11개 중 10개는 `학습에 없던 지형`으로 기록 | 늦게까지 학습했어도 해당 장면에서 실패할 수 있다는 **평가 누락 경고**다. 내부 공식 점수의 실패율로 환산하지 않는다. |
| rail/stepping-stone 6개가 모두 `학습에 없던 지형` 라벨 | 좁은 접촉면 traversability를 별도 질적 점검 질문으로 남긴다. 공개 failure label 자체가 정답 판정은 아니다. |
| H1 38개 중 single-dial 5개; 다수는 reward가 동시에 바뀜 | single-dial도 대조군이 없는 관찰이고, 다중 변경에서 개별 계수의 인과 효과를 추출하지 않는다. |
| 성공 34개는 `detail`이 비어 있음 | 실패/성공 parameter 분포를 대조하거나 안전한 reward 범위를 역산할 수 없다. |

특히 `fall_rate_pct`는 18개 H1 row에서 마지막 10회 평균, 나머지 20개에서 마지막 값이다. `terrain_direction`도 20/38은 시작점이 미기록이다. `checkpoint iteration`과 `total iterations`가 다른 사례를 같은 학습량으로 묶지 않는다. `why`·`severity`·`bias`는 지표/설정에서 파생된 진단일 수 있어 독립 label로 학습시키지 않는다. 세부 값과 38개 key 전수표는 보존한 원문 보고서를 따른다.

## 공개 사례가 주는 실전 경보

| 경보 질문 | 공개 관찰 key | 우리에게 도움이 되는 사용법 / 금지할 결론 |
| --- | --- | --- |
| reward peak가 높으면 안전한가? | `reel-14106372`: reward 26.61·terrain 5.90·fall 21.5%; `reel-74319272`: reward 21.65·terrain 5.82·fall 27.3% | reward coefficient가 다른 run의 절댓값을 순위로 쓰지 않는다. late terrain·fall·tracking·실제 통과를 함께 본다. |
| 낙상이 적으면 충분히 이동하는가? | `reel-93039572`: fall 12.9%·terrain 3.74; `reel-92770425`: fall 16.1%·terrain 3.67 | stall/느린 전진을 생존 성공으로 오인하지 않는다. 고정 명령에서 진행 거리·XY·영상의 실제 traversal을 확인한다. |
| 오래 돌리면 특수 지형 문제가 사라지는가? | `reel-8945010`: total 11.699K에도 gap failure; `reel-88114018`: total 10K에도 rail failure | 학습량 부족과 일반화 실패를 분리한다. 1K는 screening이고 장기 미해결을 무작정 추가 iteration으로 대체하지 않는다. |
| std가 높거나 낮으면 좋은가? | `reel-97541917`: std 2.720·jitter; `reel-78394459`: std 0.419·terrain 0·fall 100% | 높은 std는 흔들림 경고일 수 있고 낮은 std는 나쁜 정책 고착일 수 있다. std 단독으로 수렴/실패를 판정하지 않는다. |

구덩이·틈·레일·떠 있는 고리·극한 박스는 공개 로그에서 진단 가치가 있지만, 현재 우리 공식 채점 시나리오와 동일하다고 가정하지 않는다. 공개 장면은 **stress-test 질문**으로만 사용하고, 공식 점수와 직접 연결되는 7개 시나리오의 비중을 별도로 유지한다. 개인 영상/고정 평가에서 관찰한 행동은 제출 정책의 공식 성능 주장으로 승격하지 않는다.

### 2026-09-23 영상 5건의 행동 관찰

별도 심층 보고서는 공개 실패 영상 5건과 성공 분류 영상 일부를 **선택된 약 20초 클립**으로 직접 판독했다. 아래는 그 보고서의 화면 관찰 요약이며, 이 문서 작성 과정에서 MP4 프레임을 다시 독립 판독한 결과는 아니다. 수치 메타데이터는 9월 22일 보존본 기준으로 취급한다. 9월 23일 웹/JSON 스냅샷의 전체 통계 변화나 `school` 필드 제거를 같은 실험의 새 결과로 합치지 않는다. 22일본에서는 이 필드가 84개 모두에 존재했고 33개는 비어 있지 않았지만, 제거된 식별값을 다시 배포하지 않는다.

원본 공개 연구기록 영상 중 선별한 H1 MP4 31개(실패 분류 22, 성공 분류 9)는 당시 `reference-h1-researchlog-20260922-selected31` 참조 Release에 **개별 영상만** 게시했고 31개 자산의 크기·SHA-256을 업로드 원본과 대조한 기록이 있다. **2026-10-01 consistency audit에서 해당 GitHub Release tag endpoint가 404이고 현재 Release 목록에도 없음을 확인했으므로, 이를 현재 접근 가능한 보존 위치로 취급하지 않는다.** 공개 snapshot의 메타데이터·선별 목록은 [보존 README](../reference/public/2026-09-22_ncrc_public_data_audit/README.md)에 남아 있다. 이 자료는 우리 팀의 공식 서버 학습 evidence나 공식 채점 영상이 아니며, 이 절의 사례별 판독은 당시 선별본 중 5개 실패 클립에 한정된다.

| 공개 key | 보고서의 화면 관찰 | 내부 평가에서 분리할 것 |
| --- | --- | --- |
| `reel-78394459` | 낮은 std 0.419에도 짧고 굽힌 스텝·정체와 이미 무너진 개체가 보인다. 여러 env를 한 화면에 담아 개체별 이동거리는 알 수 없다. | action smoothness와 명령 응답·실제 전진·정체 시간을 동시 기록. 낮은 std를 수렴 성공으로 읽지 않기. |
| `reel-60061435` | 공개 fall 83.1%와 달리 선택 클립에서는 대체로 upright; 교차·측면 스텝과 방향 불안정이 두드러진다. | 집계 fall window와 한 영상의 낙상 유무를 혼동하지 않고 yaw error·heading drift·cross-step을 따로 보기. |
| `reel-11999811` | 계단 앞에서 축이 어긋나고, 20초 안에 명확한 연속 계단 상승이 보이지 않는다. 과속 후 낙상은 화면상 확인되지 않는다. | XY error 외 전진 거리·측면 이탈·첫 계단 접촉·상승 단수·stall을 측정. |
| `reel-93039572` | fall 12.9%로 낮지만 한쪽 다리를 크게 들고 계단 앞에서 스윙·한 발 지지를 반복한다. 명확한 상승이 없다. | 생존과 계단 통과를 별도 축으로 두고 `upright-but-stalled`를 실패로 표기. |
| `reel-14106372` | reward 26.61·terrain 5.90에도 내리막에서 비대칭 high-knee hop/skip과 큰 자세 진동이 보인다. 선택 구간의 명확한 낙상은 없다. | reward·terrain과 보행 품질을 분리. 좌우 접촉·단일 다리 지지·몸통 진동을 확인. |

이 클립들로는 world-frame 이동거리, jitter 주파수, 전체 낙상률, 계수의 인과 효과를 측정할 수 없다. 카메라·parent·seed·command·evaluator가 통제되지 않은 성공 분류 영상도 **좋은 동작 형태를 정의하는 질적 참고**일 뿐 matched control은 아니다. 특히 `reel-14106372`는 8개 reward가 함께 바뀌었으므로 hop을 `feet_air_time` 탓으로 돌리지 않는다. `reel-11999811`의 공개 단일 dial도 우리 H-007의 혼합 delta를 정당화하지 않는다.

현재 설치·CPU 검증된 H1 evaluator를 Windows GPU full로 실제 검증하고 matched paired evaluation에 사용할 때의 최소 설계 축은 **생존·실제 지형 진행·명령 추종·보행 품질 네 축**이다. 현재 launcher/source와 CPU 검증에 더해 2026-10-07 `model_2850` 단일 정책 full 자료는 확보했지만, `h1-submit-2` 기존 동일 protocol `scenario7` ZIP과 평가 raw는 확보돼 대응-index 비교 완료다. 단, 실제 동일 물리 terrain/initial state와 독립 training seed가 통제된 paired dataset임은 증명되지 않았다. 같은 checkpoint/명령/지형/seed/window에서 fall·base-contact와 함께 forward displacement, stair ascent 또는 obstacle progress, lateral drift, XY/yaw error, stall time을 기록한다. 가능하면 발 접촉 좌우 duty cycle·긴 one-foot support·base pitch/roll·action-delta도 남긴다. 영상에는 stall, 발 걸림, hop/skip, cross-step, 회복, 낙상을 사람 손으로 표기한다. 로그가 없으면 해당 정량 항목은 **미측정**으로 남기고 클립 관찰을 숫자로 대체하지 않는다. 이 체크리스트는 새 공식 점수식이나 자동 selector가 아니다.

## 단일 dial 다섯 건: 값 추천이 아니라 반증할 질문

| `key` | H1에서 공개된 단독 변경 | 관찰 | 다음 판단 |
| --- | --- | --- | --- |
| `reel-11309747` | `termination_penalty -5→-50` | 999회, terrain 4.82, fall 32.4%; floating ring 실패 | 우리 OFFICIAL `TERM-50` 5K와 길이·지형이 달라 성능 우열은 못 매긴다. -50도 unseen terrain을 자동 해결하지 않는다는 질문만 남긴다. |
| `reel-11806238` | `termination_penalty -5→-200` | checkpoint 1300 / total 2155, terrain 5.12, fall 21.7%, std 2.066 | -200을 즉시 시도할 근거가 아니다. 내부에서는 동일 부모의 -50 vs -100을 먼저 짝짓는다. |
| `reel-11999811` | `track_lin_vel_xy_exp 0.5→1.0` | 1K, terrain 0.90, fall 76.5% | 1.0 금지값이라는 뜻이 아니다. 안정된 +0.2 `TERM-50` parent에서 0.75의 작은 step과 unchanged control을 비교한다. |
| `reel-60061435` | `track_ang_vel_z_exp 0.5→1.0` | 1K, terrain 0.01, fall 83.1% | 우리 PERSONAL `ANGTRACK-075` 1K(legacy `YAW075`)도 early collapse였다. 조건이 달라 인과 복제는 아니며, 다음은 0.6 micro-step을 안정된 parent에서만 시험한다. |
| `reel-78394459` | `action_rate_l2 -0.0005→-0.0025` | total 5K, terrain 3.4→0, fall 100%, std 0.419 | 강한 음성 신호이나 다른 보상과 함께 더 강한 penalty를 쓴 high-terrain 반례가 있다. 무조건 금지하지 말고 짧은 matched screen으로 재현 여부를 확인한다. |

Go2의 single-dial `reel-87463271` (`feet_air_time 0.01→0.08`)은 별도 1건이며 H1 인과 근거가 아니다. `reel-11659221`/`reel-87278881`처럼 설정과 주요 수치가 동일한 key는 중복 가능성을 표시하고 독립 반복으로 세지 않는다. 다중 변경 co-occurrence(`termination+track_lin` 25건, `action_rate+termination` 24건)는 참가자들이 자주 함께 바꾼 조합이지 효과의 증거가 아니다.

## 2026-09-23 당시 내부 실험 prior — 현재 실행 지시 아님

`h1-submit-2 / TERM-50` 공식 fresh 5K(legacy H-001 R02)는 `feet=+0.2`이고, **역사적 PERSONAL R01 계보**의 legacy H-005~008 부모는 `feet=-0.2`였다. 그 계보의 H-007/008은 feet와 track을 함께 바꿨으므로 track 단독효과로 읽지 않는다. 이후 `+0.2` corrected PERSONAL Run들과 OFFICIAL `h1-submit-4 / AIRTIME-025` fresh 10K(legacy H-005 R05)는 별도 계보다. [현재 Run·상태](14_H1_NEXT_RUN_PARAMETER_COMPARISON.md)와 [가설 registry](../../../research/EXPERIMENTS.md)를 우선한다.

당시 공개 실패 사례에서 나온 질문은 같은 corrected 부모의 unchanged continuation을 control로 두고 `track_lin 0.5→0.75`, `termination -50→-100`, `track_ang 0.5→0.6`, `action_rate -0.0005→-0.0025`(붕괴 재현용 negative-control), 이후 `ang_vel_xy -0.05→-0.10`을 **각각 별도로** 시험할지였다. 이는 후보 질문이지 성능 결론이나 미실행 목록이 아니다. 9/25 corrected 비교와 9/27 `AIRTIME-025` fresh·continuation, `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch fresh는 이미 완료됐다. `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch(legacy H-010)의 `feet=0.25`는 향후 paired-evaluation 우선 후보(PROMOTE); H1 통합 launcher 설치·CPU 60개 검증 완료·Windows GPU full/해당 paired evaluation 미실행, legacy H-006/009/011은 HOLD다. 공개 row가 이 판정을 대신하지 않는다.

다음 비교를 실제로 진행한다면 부모 checkpoint identity·reward·source·seed·iteration과 evaluator의 command/terrain/초기 상태를 맞춘다. 1K는 방향성 screen이며 같은 길이 control과 late-window의 XY/yaw, 실제 진행·stall, 낙상·자세를 함께 본다. reward 계수가 다른 Run의 총 reward 절댓값만으로 승자를 고르지 않는다. 영상은 **실제 source checkpoint**로 표기한다(9/27 `AIRTIME-025` continuation 영상, legacy H-005 R04는 final 4997이 아닌 4800). 공개 사례는 개인 PC 후보 prior로만 쓰고 Optuna `study.tell()`·내부 objective·OFFICIAL evidence로 합치지 않는다.
