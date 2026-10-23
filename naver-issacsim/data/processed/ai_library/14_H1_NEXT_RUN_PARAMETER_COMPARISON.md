---
title: "H1 계보 비교와 다음 OFFICIAL single-dial 검증 프로토콜"
purpose: "AI upload bundle — corrected lineage, Round-4 결과, planned ORIENT→ACTRATE single-dial sequence의 비교·판정 규칙"
sources:
  - "data/processed/experiments/h1/analysis/2026-09-09_OFFICIAL_SERVER_H1_TERM50_5K_DEEP_ANALYSIS.md"
  - "data/processed/planning/historical/07_H1_SECOND_RUN_PARAMETER_COMPARISON_PLAN.md"
  - "data/processed/experiments/h1/training/2026-08-24_OFFICIAL_SERVER_300ITER_BASELINE.md"
  - "data/processed/experiments/h1/analysis/2026-09-07_BREV_L40S_H1_BASELINE_5K_AND_SCREENING.md"
  - "data/processed/experiments/h1/analysis/2026-09-17_H-004_PERSONAL_FRESH_1P5K_DEEP_ANALYSIS.md"
  - "data/processed/experiments/h1/analysis/2026-09-17_H-005_PERSONAL_RESUME_FROM_H-001_1P5K_DEEP_ANALYSIS.md"
  - "data/processed/experiments/h1/analysis/2026-09-17_H-006_PERSONAL_RESUME_FROM_H-001_1P5K_DEEP_ANALYSIS.md"
  - "data/processed/experiments/h1/analysis/2026-09-17_H-007_PERSONAL_RESUME_FROM_H-001_1P5K_DEEP_ANALYSIS.md"
  - "data/processed/experiments/h1/analysis/2026-09-17_H-008_PERSONAL_RESUME_FROM_H-001_1P5K_DEEP_ANALYSIS.md"
  - "data/processed/experiments/h1/analysis/2026-09-18_H-007_MODEL2998_SINGLE_CHECKPOINT_SUMMARY.md"
  - "data/processed/experiments/h1/analysis/2026-09-18_H-008_MODEL2998_6TERRAIN_VIDEO_ANALYSIS_SUMMARY.md"
  - "data/processed/incoming/other/reviewed/2026-09-18_H007_MODEL_2998_SINGLE_CHECKPOINT_ANALYSIS.md"
  - "data/processed/incoming/other/reviewed/2026-09-18_H008_H1_MODEL2998_6TERRAIN_VIDEO_ANALYSIS.md"
  - "data/processed/experiments/h1/analysis/2026-09-18_H-008_CONT2K_FROM_MODEL2998_ANALYSIS.md"
  - "data/processed/incoming/other/reviewed/H1_H009_HIPDEV030_FROM_H008_3K_DEEP_ANALYSIS_20260920.md"
  - "data/processed/incoming/other/reviewed/H1_H010_AIRTIME025_3K_TO_5K_DEEP_ANALYSIS_REVISED.md"
  - "data/processed/incoming/other/reviewed/H1_H011_HIPDEV010_MODEL4997_DEEP_ANALYSIS.md"
  - "data/processed/incoming/other/reviewed/H1_H012_TERM100_5K_DEEP_ANALYSIS(1).md"
  - "research/experiments/h1/H-012.md"
  - "data/processed/incoming/other/reviewed/NCRC_H1_EXTERNAL_INTERNAL_SINGLE_DELTA_ANALYSIS_20260923.md"
  - "data/processed/incoming/other/reviewed/NCRC_H1_VISUAL_FAILURE_DEEP_ANALYSIS_20260923.md"
  - "data/processed/incoming/other/reviewed/H1_H001_R05_CORRECTED_PARENT_1P5K_DEEP_ANALYSIS_20260925.md"
  - "data/processed/incoming/other/reviewed/H1_H005_VS_H006_DEEP_ANALYSIS_20260925.md"
  - "data/processed/incoming/other/reviewed/H1_H-007_VS_H-008_DEEP_ANALYSIS_20260925.md"
  - "data/processed/incoming/other/reviewed/H1_H009_R02_VS_H008_CORRECTED_CONTROL_DEEP_ANALYSIS_20260925.md"
  - "data/processed/incoming/other/reviewed/H1_H010_R02_AIRTIME025_CORRECTED_VS_H008_CORRECTED_CONTROL_TO5K_DEEP_ANALYSIS_20260926.md"
  - "data/processed/incoming/other/reviewed/H1_H011_R02_HIPDEV010_CORRECTED_VS_H008_CORRECTED_CONTROL_DEEP_ANALYSIS_20260926.md"
  - "data/processed/planning/historical/2026-09-27_H1_PERSONAL_FRESH_AND_CONTINUATION_PLAN.md"
  - "data/processed/experiments/h1/training/2026-09-27_H1_FRESH_AND_CONTINUATION_EVIDENCE_INTAKE.md"
  - "data/processed/incoming/other/reviewed/H1_H005_FRESH3K_R01_VS_H005_R02_DEEP_ANALYSIS_20260927.md"
  - "data/processed/incoming/other/reviewed/H1_H005_CORRECTED5K_R02_VS_H005_FRESH3K_R01_DEEP_ANALYSIS_20260927.md"
  - "data/processed/incoming/other/reviewed/H1_H005_FRESH3K_R01_VS_H005_CORRECTED3KTO5K_R02_DEEP_ANALYSIS_20260927.md"
  - "data/processed/incoming/other/reviewed/H1_H010_FRESH3K_R01_VS_H005_FRESH3K_R01_DEEP_ANALYSIS_20260927.md"
  - "data/processed/incoming/other/reviewed/H1_H005_OFFICIAL10K_VS_TERM50_OFFICIAL5K_DEEP_ANALYSIS_20260928.md"
  - "data/processed/experiments/h1/analysis/2026-09-30_OFFICIAL_EVAL_H1_ROUND4_AIRTIME025.md"
type: "experiment_protocol"
---

# H1 다음 공식 서버 파라미터 비교 프로토콜

## 2026-10-22 장기 학습 정책 별도 직접 평가 수신

[원본 PDF·계보·표시 정밀도·비교](../experiments/h1/analysis/2026-10-22_H1_MODEL40500_ORGANIZER_DIRECT_EVALUATION.md): model40500/ang=.60의 운영진 별도 직접 평가는 자동56.9/70·의도20·코멘트10·총86.9/100이다. 실제 7라운드 접수 model11650/ang=.70·자동57.05/70과 `h1-submit-7` identity는 그대로다.40500은 R6 model9999에서 이어학습한 별도 Run이다. 표시 시나리오 합56.8과 보고총계56.9를 함께 보존한다. 학습 지표 개선에도 이번 점수 상승은 확인되지 않았다. 서로 다른 부모·reward 경로를 단순 학습량 효과로 해석하지 않으며, 장기 학습 무효·평가기 오류·합격 여부를 확정하지 않는다.

## 2026-10-18 기존 설정 장기 확인 TOP10 — 외주 제안 / 선택 대기

[전체 순위·원문·상위 Run/SHA](../experiments/h1/analysis/2026-10-18_H1_10K_TOP10_SELECTION_INTAKE.md): 1위 JOINT(.65/.60/-.0003) fresh5K의 평가·keeper4950 동일 reward 연장, 2위 action=-.0003 fresh3K의 평가·keeper2950 연장, 3위 ORIENT-100 연장이다. ORIENT는 평가2850과 재개 제안2950이 달라 행동 근거를 동일시하지 않는다. 기존 후보10개를 추린 실행 우선순위 자문이며 새 config·Run·학습 승인·승격은 아니다. 연장은 fresh10K와 다른 계보 질문이고, 전부 실행할 필요도 없다. 기존 정책 HOLD와 제출본 보존을 유지한다.

## 2026-10-18 후보3 보고서 완료 — 진행 이점과 yaw 비용 / HOLD

[lin=.75 + action=-.0001 fresh3K2850 검토](../experiments/h1/analysis/2026-10-18_H1_LIN075_ACTION0001_MODEL2850_POLICY_REVIEW.md): H5 진행 평균/P05/최소9.867/9.640/9.514m와 무장기stall에도 H4/H5 yaw .2725/.2730rad/s, H3 world 잔류2.605m로 현재 대표 채택 **HOLD**다. 이전 TERM50/2700 비교는 미대응 참고이며 새 paired 효과가 아니다. 해당3K 정책의 보류를 설정 자체의 10K 실패로 바꾸지 않는다. 평가2850과 latest keeper2950을 구분한다. 후보1도 학습 완료/PASS지만 평가·정책 보고서는 미수신이다.

## 2026-10-17 후보2 자세·고관절 완화형 — 보고서 수신 / HOLD

[실제 Run·평가2850 SHA·원문 수납](../experiments/h1/analysis/2026-10-17_H1_JOINT_TRACKING_POSTURE_MODEL2850_POLICY_REVIEW.md): lin=.65/ang=.60/action=-.0003/orientation=-1.0/hip=-.1 OFFICIAL fresh3K COMPLETED/PASS와 PERSONAL 보고서가 연결됐다. 생존3072/3072에도 H1/H3 body 후진−.719/−.679m, H3 world 잔류1.160m, H5 진행 평균/P05/최소8.024/7.460/6.721m로 **HOLD**다. rough stall>.05는1/384여서 완전 정체보다 지속 저속이 주된 문제다. 이전 JOINT fresh5K4950보다 수치상 불리하나 3K/5K 학습량·여러 reward가 달라 자세·hip의 독립 효과나 matched 우열로 해석하지 않는다. keeper2950은 미평가다. 후보1·3의 과거 PLANNED 표시는 이후 학습 수납으로 대체됐으며 후보3 보고서는 위 후속 상태를 따른다. 새 학습이나 비교 실행 승인은 아니다.

## 2026-10-17 joint tracking fresh5K 후속 — HOLD

[보고서·식별·검토](../experiments/h1/analysis/2026-10-17_H1_JOINT_TRACKING_MODEL4950_POLICY_REVIEW.md). `exp-h1-joint-tracking-balance`, 실제 OFFICIAL Run `20261017-015509-h1-lintrack-065-angtrack-060-actrate-0003-fresh5`는 `h1-submit-2 + lin=.65 + ang=.60 + action=-.0003`, fresh/no parent·seed42/4096env·5000요청/console4999, COMPLETED/exit0/PASS다. keeper4950 SHA `2df05840…62bc478`의 PERSONAL 평가·보고서가 완료됐고 **공식 제출 대체 후보 HOLD**다. 생존3072/3072, H2 전진14.820/15m·H6 상/하19.992/19.814m·H7 9.688/10m는 긍정 신호이나 H5 평균/P05/최소8.853/8.403/7.930m와 정지 body x−.259m/world 잔류.460m가 남는다. H3 vy 오차.07476m/s·world 잔류.739m를 구분하고 원점복귀를 공식 명령이라고 하지 않는다.

원문이 제안한 다음 단계는 **기존 LINTRACK065 fresh5K4950(`b7528923…`)과 JOINT4950(`2df05840…`)의 저장 평가 CPU 비교**다. protocol·resolved config·source·명령·cohort를 확인하기 전 기존 보고서 수치의 차이를 paired 효과로 취급하지 않는다. 비교는 미실행이며 새 GPU 작업 승인이 아니다. 학습길이·여러 reward 동시 변경·단일 학습 seed의 한계를 보존하고 아래 과거 미실행/분석대기 표현과 구분한다.

**2026-10-17 action=-.0002 보고서 수신:** [Run·keeper SHA·원문과 검토](../experiments/h1/analysis/2026-10-17_H1_ACTION0002_MODEL2950_POLICY_REVIEW.md). OFFICIAL fresh3K keeper2950의 PERSONAL 단독 평가 분석은 **HOLD**다. H5 진행 평균/P05/최소8.941/8.573/6.983m, H1/H3 비의도 body전진1.842/1.225m. -.0003보다 낫거나 나쁘다는 matched 비교는 아직 없다. H3는 좌우 속도 추종을 보며 world 종료 잔류만으로 공식 원점복귀 실패를 선언하지 않는다. 새 학습 우선순위를 이 단독 보고서로 자동 확정하지 않는다.

## 현재 판단 프레임 — 2026-10-17

[전략·연구 근거와 후보장](../planning/2026-10-16_H1_EVIDENCE_AND_RESEARCH_NEXT_EXPERIMENTS.md). 먼저 공식 제출 경쟁력을 묻는지 광의의 보행 능력을 묻는지 밝힌다. H1 공식 7시나리오에 계단·박스는 없으며, 로컬 scenario7도 이 둘의 정량 case가 없다. 따라서 계단 영상 완주 미입증은 보조 증거 공백이지 자동 공식 탈락 기준이 아니다. 기존 HOLD 판정은 삭제하지 않되 적용 목표와 실제 추종·진행 손실을 함께 읽는다. 로컬 우열을 공식 점수 개선이나 reward 단독 인과로 바꾸지 않는다.

다음 Run 권고는 config 탐색 / 독립 학습 seed 재현 / 고정 config 추가 학습 / reward 전환 resume 중 답할 질문을 먼저 고른다. 관측 장점이 반복되는지와 더 좋은 값을 찾는 것은 다르다. 무기한 resume·공격적 다중 변경·촘촘한 미세 sweep을 기본값으로 제안하지 않으며 기존 완료 비교를 다시 대기로 돌리지 않는다. 이번 정리는 실행·새 제출 승인이 아니다.

## 2026-10-16 action=-.0003 fresh3K 완료·보고서 HOLD

[실제 Run·원문·독립 확인 범위](../experiments/h1/analysis/2026-10-16_H1_ACTION0003_MODEL2950_POLICY_REVIEW.md): `20261016-033023-h1-actrate-0003-fresh3k`, OFFICIAL fresh/no parent, seed42/4096env, requested3000/console2999, COMPLETED/PASS. `h1-submit-2 + action=-.0003`, keeper2950 SHA `1cc2c031…0473c4b`(best2900 아님)의 PERSONAL 평가·보고서는 완료/HOLD다. H5 mean/P05/min9.018/8.664/6.771m, H1 body 누수 .382m·world 잔류 .455m, H3 vy오차 .07035m/s·world 잔류 .407m. 생존100%만으로 PROMOTE하지 않는다. 다음 비교 제안은 model2700 우선/TERM50 model2800 보조의 저장 ZIP CPU 대조이며 아직 미실행이다. 실제 평가 config/source·checkpoint 선택 차이를 확인하고, 같은 cohort 키를 동일 물리 지형이나 독립 학습 반복으로 해석하지 않는다. 아래 fresh 미실행 제안은 이 실제 Run 이전 기록이며 -.0003 resume는 별도 미실행이다.

## 2026-10-16 현재 방향 — angxy HOLD, CPU 비교 완료

[angxy 원문·5정책 CPU 비교](../experiments/h1/analysis/2026-10-16_H1_ANGXY008_MODEL4650_POLICY_REVIEW.md): 15,360행의 동일 evaluation protocol/config·키 확인. angxy4650은 무변경4699 대비 H5 평균+.053m/P05−.197m, H3 vy·H4 yaw·경사 자세 RMS 악화로 **HOLD**. posture angle RMS는 body-rate reward 자체와 다르며 인과·공식점수로 바꾸지 않는다. [문헌 근거·후속 계획](../planning/2026-10-16_H1_EVIDENCE_AND_RESEARCH_NEXT_EXPERIMENTS.md)은 당시 **action=-.0003 fresh3K**를 제안했으며 이후 위 실제 Run·보고서 HOLD로 갱신됐다. -.0003 resume는 별도 비용절약 대안, 독립 학습 seed 확인은 재현성 질문, airtime resume는 PLANNED 대기다. 해당 제안 자체는 실행 승인이 아니었으며 현재 완료 사실도 최적값 확정을 뜻하지 않는다. angxy CPU 비교를 다시 요청하지 않는다.

## 2026-10-15 lin=.55 실행 결과 수납 — 예비 action 후보는 미선택

**2026-10-16 후속:** [4정책 raw 코호트 비교](../experiments/h1/analysis/2026-10-16_H1_LIN055_FOUR_POLICY_COHORT_INTAKE.md)에서 `.55`는 무변경 대비 H5 +1.322m이나 H3 vy/H4 yaw 악화, `.65` 대비 H4 yaw 개선이나 H3 vy·rough 평균/P05/min 손실로 **HOLD 유지**다. `.55`를 새 범용 승자로 읽지 않는다. action=-.0003 fresh는 위 실제 Run·보고서 HOLD로 갱신됐고 resume만 미실행이며 angxy=-.08은 학습·PERSONAL 평가·보고서와 위 후속 CPU 비교 완료/HOLD다.

[후속 행동 보고서](../experiments/h1/analysis/2026-10-15_H1_LINTRACK055_MODEL4650_POLICY_REVIEW.md)는 **HOLD**: H1 world 종료 잔류 .702m,H3 2.363m,H5 mean/P05/min 진행9.242/8.859/8.256m,H4 yaw .1126rad/s,3072/3072 생존이다. 이는 제공 보고서 값이며 이번 반영에서 재집계·영상 디코딩하지 않았다. 상대 개선·공식 점수·reward 인과를 확정하지 않고, H3 world 잔류는 body-frame 속도 명령의 공식 실패율이 아닌 경로 진단으로 구분한다.

[후속 완료 기록·원문·비교 한계](../experiments/h1/analysis/2026-10-15_H1_NEXT_HYPOTHESIS_DECISION_INTAKE.md).

**lin=.55 후속 완료:** Run `20261015-105910-h1-actrate0001-lintrack-055-from2700-plus2k`는 OFFICIAL resume +2000, seed42/4096env, console4699/4700, COMPLETED/exit0/validation PASS다. 부모2700 SHA `e54d3389…93ca7ae`에서 lin .50→.55만 변경(action=-.0001, feet=.20, termination=-50 유지), 최종 preset-relative override는 `h1-submit-2 + lin=.55 + action=-.0001`다. 최신 indexed keeper `model_4650.pt` SHA `e8a358a50832f6653b1e558788a5a676ab9a849d3ec6c64e3ed2430e9ff41814`의 PERSONAL Windows 6영상·scenario7 평가도 COMPLETE(128env×3seed×8case,3072행)로 수납했다. console 종점4699와 keeper4650은 다르다. 원본 parent/source IDs=null·imported provenance=false는 유지하며 별도 SHA로 연결한다. **정책 분석 수납 완료·범용 후보 HOLD, 공식 점수·제출 아님**. [분석 원문·계보·한계](../experiments/h1/analysis/2026-10-15_H1_LINTRACK055_MODEL4650_POLICY_REVIEW.md). [학습 Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261015-exp-h1-action-first-planar-tracking-switch-lin055-resume2700-plus2k) · [평가 Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261015-exp-h1-action-first-planar-tracking-switch-lin055-model4650-video-eval). action=-.0003 fresh는 위 완료·보고서 HOLD를 따르고 resume만 별도 미실행이다. Optuna v2의 objective/comparison 미승인·Tell 차단은 별개다.

새 예비는 기존 같은 부모 B/C 대조를 활용한다는 비용·식별력 제안이지 중간값 성능 보증이 아니다. 기존 L−B CSV의 H5 진행 +1.626684m(384/384 증가), H4 yaw +.087164rad/s·H3 world +1.816354m와 C의 최악 진행4.845m/stall .386을 함께 본다. 외주 14개 파생값 검산을 원 episode/MP4·native 훈련 재검증으로 쓰지 않는다. endpoint4699 대 선택4650, 단일 학습 seed·null/unverified provenance 한계와 HOLD를 유지한다. 임시 실패 문구를 공통 gate로 채택하지 않는다. [Optuna v2](15_OPTUNA_REWARD_DECISION_ENGINE.md)는 별도 개선본 수신·정적 검토 완료이며 실제 최적화 준비·운영 검증은 미완료다.

## 2026-10-15 부모2700·무변경4699·ACTION 복원4650 CPU 비교 완료

[새 비교 원문·CSV·판정](../experiments/h1/analysis/2026-10-15_ACTRATE_PARENT_UNCHANGED_RESTORATION_COMPARISON_INTAKE.md): 같은 evaluation source/config·cohort key를 대조한 외부 CPU 비교 수납 완료. 무변경4699는 부모2700보다 rough 진행384/384건 감소해 **이번 세 정책의 범용·전진/험지 대표 후보 REJECT**. 복원4650(`a8249db4…`)은 무변경보다 진행373/384건 증가하지만 tracking283/384건 악화·최악 진행4.845m로 **HOLD**. 부모2700도 HOLD, PROMOTE 없음. 자동 best2700/endpoint4699/선택4650 차이와 train-side 미독립검증 때문에 reward 단독 인과는 미확정이다. 학습 실패·원본 폐기를 뜻하지 않으며 같은 비교를 다시 대기로 제안하지 않는다.

## 2026-10-15 평가 결과: ACTION 복원 +2K / LINTRACK-065 fresh5K — 우선 대조 업데이트

[2026-10-15 두 정책 보고서 통합 검토](../experiments/h1/analysis/2026-10-15_H1_MODEL4650_LINTRACK065_POLICY_REVIEW.md) · [ACTION 원문](../incoming/other/reviewed/H1_MODEL4650_POLICY_ANALYSIS_20261015.md) · [LINTRACK 원문](../incoming/other/reviewed/H1_LINTRACK-065_POLICY_ANALYSIS_20261015.md). **두 PERSONAL 영상·scenario7 full 분석 모두 정책 HOLD**. `model_4650`은 기존 ACTRATE-parent lin=.65 `model_4650`(SHA `ce7ad586…`)이 아닌, 2026-10-14 reward 복원 +2K Run의 SHA `a8249db4…` 정책이다. LINTRACK-065 fresh5K `model_4950`은 SHA `b7528923…`로 별개의 OFFICIAL fresh/부모 없는 질문.

| 비교축 | ACTION 복원 4650 | LINTRACK fresh4950 |
| --- | ---: | ---: |
| 평가 20초 생존 | 3,072/3,072 | 3,072/3,072 |
| H1 body 비의도 전진 | 0.282m | 0.063m |
| H3 world 최종 잔류 (행별 hypotenuse의 평균) | 0.167m | 3.102m |
| H5 rough 평균 / P05 / 최소 전진 | 8.769 / 7.970 / 4.845m | 8.995 / 8.411 / 7.943m |
| 전체 mixed tracking | 0.140944 | 0.17994 |

이 표는 **각 업로드 보고서의 별도 집계**다. 같은 protocol `d406a296…7062d34`를 가졌지만 두 ZIP 및 기존 대조군의 resolved evaluation source·cohort·물리 terrain과 training-side PPO를 이번 수납에서 직접 통제 비교한 것은 아니다. Mixed tracking을 단일 m/s로 해석하지 않는다. world H3 최종 복귀는 body-frame 목표 추종의 공식 합격 기준도 아니며, rough timeout 생존만으로 10m 진행 달성도 아니다.

**행동 채택 질문과 reward 실험 질문 분리:**
- action-rate 복원 가설의 **부모2700/무변경4699/복원4650(`a8249db4…`) raw CPU 비교는 완료**됐고 결과는 위 수납을 따른다. 두 resume 원 evidence의 imported-parent provenance=false/null은 외부 parent SHA 대조와 별개로 유지한다. 옛 lin=.65 resume4650(`ce7ad586…`) 대 무변경4699도 이후 위 다음 가설 보고서에서 기존 CSV 수준으로 비교됐다.
- `h1-submit-2` 기반 LINTRACK fresh5K는 기존 TERM-50 `model_2800` 평가 raw와 조건을 검토하되 **3K/5K·checkpoint 선택 차이 등 학습량 통제 부족**을 밝혀 reward 단독 인과로 쓰지 않는다.
- H1 6영상은 1 env/seed42 `maneuver_push`, camera-off H1/H3/H5/H6/H7은 별도 seed/cohort. stairs/boxes 정량 case 없음. LINTRACK `03_boxes` 501개 검정 프레임은 캡처 artifact로 보존.

두 정책은 20초 전진·경사·push 유효 이동을 보였으나 범용 PROMOTE나 공식 채점·제출 성능 개선을 뜻하지 않는다. 여기서 수행한 것은 기존 사용자 MD의 지식·판정 반영이고, 새 train/evaluator/영상/Optuna는 실행하지 않았다.

> 날짜별 업데이트는 해당 시점의 기록이다. 최신 Run·제출 상태는 [현재 Experiment registry](../../../research/EXPERIMENTS.md)를 우선한다.

## 2026-10-11 ACTRATE-0001 fresh10K / model_9999 비교 대기 — HOLD

> 별도 후속 실행: [LINTRACK065 fresh5K](../../../research/experiments/h1/exp-h1-planar-tracking-weight.md) Run `20261014-081901-h1-lintrack-065-fresh5k`는 OFFICIAL fresh/no parent·seed42·4096env·5000회, COMPLETED/exit0/PASS 및 원본 게시 완료다. `h1-submit-2 + lin=0.65`(action=-0.0005)이며 행동 평가 대기/HOLD. model2700→4650 resume(action=-0.0001)의 unchanged sibling control이 아니며, 현재 4정책 평가 비교에도 포함되지 않는다. 학습 완료만으로 새 설정을 추천·채택하지 않는다.

> 후속: [2026-10-14 4정책 CPU 비교](../experiments/h1/analysis/2026-10-14_H1_4POLICY_LINTRACK065_COMPARISON_INTAKE.md)가 수신돼 기존 2800/2700/9999에 4650을 대조했다. 아래 비교 대기는 당시 접근 상태이며 현재 자료 부재를 뜻하지 않는다. 공식 점수·reward 인과효과는 여전히 미확정이다.

[model_9999 정책 검토](../experiments/h1/analysis/2026-10-11_ACTRATE0001_MODEL9999_POLICY_REVIEW.md): 3,072/3,072 timeout 생존, 전체 혼합 단위 tracking 0.122384(공식 점수 아님). 정지 H1·횡왕복 H3 world 순변위 평균 0.287/0.395m, rough H5 body 전진 평균/P05/최소 8.915/8.251/6.492m다. 여섯 영상 분석도 받았으나 중앙 연속 계단 완주와 rough 하위 꼬리 문제가 남는다.

다음은 이미 보존된 TERM-50/model_2800과 protocol/source/명령/지형/seed/horizon·cohort 대응을 확인한 CPU raw 비교다. model_2700은 학습 길이가 다른 참고군이며, 이 단일 ZIP 보고서는 직접 A/B나 reward 인과 개선을 입증하지 않는다. 새 학습·평가를 자동 실행하지 않는다.



## 2026-10-11 ACTRATE-0001 → lin=0.65 / model_4650 — 당시 HOLD와 비교 계획

> **10/15 후속 갱신:** [unchanged +2K Run](../../../research/experiments/h1/exp-h1-action-rate-relaxation.md) `20261014-111135-h1-actrate-0001-unchanged-cont2k`의 OFFICIAL 학습·PERSONAL 평가와 lin=.65 resume4650 대 기존 CSV 비교는 완료됐다. 아래 control 부재는 당시 상태다. 남은 한계는 원 episode 직접 재집계·checkpoint 선택 차이·reward 인과 미확정이지 control 학습/평가 자료의 부재가 아니다. 새 sibling 학습·checkpoint 토너먼트를 자동 제안하지 않는다.

> 2026-10-14 후속 보고서·CSV 대조 완료: 부모2700→4650 H2 vx .0427→.0254m/s·H3 vy .0673→.0571m/s 개선, H4 yaw .1183→.1791rad/s·H3 world XY 잔류 .669→2.398m 악화. H5 body 진행 평균/P05 9.948/9.592→9.546/9.228m, 최소 8.815→8.974m. HOLD 유지. 필요 시 같은 부모 SHA의 reward-unchanged +2K sibling을 동일 endpoint/선택 규칙으로 비교한다. 평가384 cohort는 독립 학습384회가 아니며, 임시 승급 임계값은 검증된 공식 gate가 아니다. 이 업데이트는 새 학습을 실행하지 않는다.

[model_4650 정책 검토](../experiments/h1/analysis/2026-10-11_ACTRATE0001_LINTRACK065_MODEL4650_POLICY_REVIEW.md): 후속 4정책 보고서, unchanged +2K의 학습·평가 및 10/15 파생 CSV 교차 비교까지 수신됐다. matched reward 인과·제출 성능은 여전히 미확인이며 학습량·resume 효과와 reward 효과를 분리해 단정하지 않는다. 새 GPU 실행은 자동으로 시작하지 않는다.

## 2026-10-11 ACTRATE-001 / model_2850 행동 분석 수신 — 별도 fresh 정책 HOLD

[2026-10-10 원문 분석](../incoming/other/reviewed/H1_MODEL2850_SHA1E6D_POLICY_ANALYSIS_20261010.md) · [2026-10-11 정책 검토](../experiments/h1/analysis/2026-10-11_ACTRATE001_MODEL2850_POLICY_REVIEW.md) · [Experiment](../../../research/experiments/h1/exp-h1-action-rate-smoothing.md). OFFICIAL fresh3K `20261010-125324-h1-actrate-001-fresh3k` (best `model_2850` SHA `1e6d…bb1`)에 연결되는 Windows PERSONAL `scenario7` 단일 정책 분석이 완료됐다. **3,072/3,072 episode 20초 생존**, H2/H7 body 전진 **15.470/10.656m**, H6 경사 전진 **20.297/20.058m**는 이동 능력을 시사한다. 반면 H1 정지 world 평균 순변위 **1.151m**, H3 횡왕복 world 평균 순변위 **2.177m**, rough H5 P05 전진 **8.921m**, 계단 중앙 다단 통과 미검증이 남는다. **HOLD**이며 기존 같은 이름의 `ORIENT-100/model_2850` SHA `6aed…f7b0`와 반드시 구분한다.

1순위는 기존 `h1-submit-2 / TERM-50 model_2800`의 보존된 평가 raw를 protocol·source/PPO·command/terrain·seed·시간창 기준으로 검토한 뒤 cohort별 비교하는 것이다. 과거 단일정책 요약치만으로 reward `action_rate_l2=-0.001`의 인과 효과를 판단하지 않는다. 보고서의 ZIP 내부 `source_run_id=null`은 OFFICIAL Run 증거와 외부 SHA로 연결하되 내부 필드는 바꾸지 않는다. 신규 GPU 평가·train·Optuna·공식 채점 실행 없음.

## 2026-10-10 ANGTRACK-065 ↔ TERM-50 1순위 원본 대조 분석 완료 — 추가 GPU 불필요

[3,072 cohort 동일 인덱스 직접 분석](../experiments/h1/analysis/2026-10-10_H1_ANGTRACK065_TERM50_DEEP_RAW_COMPARISON.md). 1순위로 지정한 `ANGTRACK-065 model_2950` vs `TERM-50 model_2800` 보존 평가 ZIP raw를 직접 집계했다. 첫 episode만 `(scenario,case,seed,env_id)` 3,072개로 대응(ANG H3 접촉 종료 15건과 이후 짧은 재시작 행 별도), evaluator config/source/protocol parity를 검증했다. H3 base-contact TERM 0/384 vs ANG **15/384**, `vy_error` 0.06848 vs 0.18601, stall 0.00912 vs 0.34339. H4 yaw는 ANG **0.07704** vs TERM 0.11934로 이점이 크지만 H5 rough 진행 평균 8.895 vs TERM 8.896m로 개선 없음. 혼합 tracking ANG 0.130669 vs TERM 0.157118이지만 XY RMSE는 악화. **전방위 후보 ANG HOLD**, `ACTRATE-001` 후속 fresh3K는 완료/PASS·PERSONAL 분석 수납/HOLD; 자동 학습 실행/Optuna 없음. 같은 평가 키도 물리 terrain/reset과 훈련 인과의 동일성은 보증하지 않는다. 아래의 'ANG matched 미실행'은 이번 완료 이전 기록이다.

## 2026-10-10 ANGTRACK-065 / model_2950 — 단일 PERSONAL 행동 평가 수신, HOLD

[사용자 제공 원문](../incoming/other/reviewed/H1_ANGTRACK-065_POLICY_ANALYSIS_20261010.md) · [checkpoint·분모·판정](../experiments/h1/analysis/2026-10-10_ANGTRACK065_MODEL2950_POLICY_REVIEW.md) · [OFFICIAL 학습 Experiment](../../../research/experiments/h1/exp-h1-angular-tracking-boost.md). OFFICIAL `20261009-155344-h1-angtrack-065-fresh3k` COMPLETED/PASS, 자동 best=keeper `model_2950.pt`(SHA `6a6f456e…68e118c`)의 **후속 Windows PERSONAL** 6영상+`scenario7` 분석이다. 평가 COMPLETE이지 OFFICIAL 점수/재학습 Run이 아니다. 3,072 최초 cohort에서 H3 lateral first episode **15/384 base-contact 종료**가 발생하고 각 1개 재시작해서 **3,087 raw episode행**; H3 20초 최초 timeout **369/384=96.09%**. H3 stall **0.3532**, vy error **0.1871m/s**, tracking **0.2203**(399행), H1 정지 비의도 body 전진 **0.875m**. H2 전진 **14.703m**, H4 yaw abs error **0.0770rad/s**, H5 rough 평균/P05 **8.895/8.399m**, H6 상/하 **19.571/19.235m**, H7 push **9.996m**. `06_slope_down_10deg.mp4` 짝수 500/1000 검정 frame은 영상 캡처 결함이다.

**후속 대조 1순위:** 이미 보존된 `TERM-50/model_2800`의 동일 protocol `scenario7` 평가 raw. 단, ANGTRACK 보고서는 **ANGTRACK ZIP 하나만 직접 열었으므로** 기존 TERM/ORIENT/ACTRATE 9,216-episode matched-index 비교에 ANGTRACK를 소급 포함하지 않는다. 추가 비교 시 최초 cohort·restart·기준선 contact/timeout을 따로 집계하고 H3 vy/stall/fall, H1 정지, H4 yaw, H5 worst tail과 action/posture를 맞춘다. 대응 seed/ID만으로 동일 물리 terrain·episode를 보장하지 않는다. **단일 정책 HOLD**; matched reward 인과·공식 채점·다단 계단 통과는 미확정이고 GPU 실행을 승인하지 않는다.

## 2026-10-10 TERM-50/ORIENT/ACTRATE 동일 scenario7 원자료 직접 재집계 — 완료

[최종 원본 검증·9,216 episode·대응-index 비교 보고서](../experiments/h1/analysis/2026-10-10_H1_SCENARIO7_RAW_3POLICY_MATCHED_ANALYSIS.md) · [case 집계 JSON](../experiments/h1/2026-10-10_H1_SCENARIO7_RAW_SUMMARY.json) · [대응 차이 JSON](../experiments/h1/2026-10-10_H1_SCENARIO7_PAIRED_DELTAS.json). 기존 평가 ZIP 3개 수신 후 SHA-256 3/3, ZIP CRC, 18파일×3, 각 3,072행(총 9,216), policy SHA, `resolved_configs.json` **바이트 동일**, `protocol`/agent/source/applied-env fingerprints 동일, 3,072 대응 `(scenario,case,seed,env_id)` 1:1 **전부 PASS**. 이전 “Release ZIP 바이너리를 읽지 못해 TERM-50 raw 미확인”은 접수 전 단계의 기록이며 **현재 raw 비교는 수행됐다**. 다만 대응 key의 일치는 동일 초기 tile/물리 trajectory의 확증이 아니고 training-side source/PPO 완전 일치나 반복 Run 통제 인과로 확대하지 않는다.

- **기준 TERM-50/model_2800:** 전체 tracking `0.15712`, H1 비의도 전진 `1.352m`, H5 rough mean/P05/min `8.896/8.533/2.639m`; 최악 stall `0.611`. **ORIENT-100/model_2850:** 전체 tracking `0.14041` (TERM 대비 10.63% 낮음), H5 mean `9.451m`; H1 비의도 전진 `1.633m`; **roll/pitch RMS 전체 `0.08015` vs TERM `0.03381` (8 case 모두 ORIENT가 높음)**. **ACTRATE-0001/model_2700:** 전체 tracking `0.14534` (TERM 대비 7.50% 낮음), H5 mean/P05/min `9.948/9.592/8.815m`, H5 대응 인덱스 진행 증가 384/384; H1 비의도 전진 `1.987m`, action Δ RMS 전체 `0.45687` (TERM `0.36529`, ORIENT `0.35759`).
- **후속 결정:** 정책 모두 HOLD; TERM 정지·자세 비용 / ORIENT 혼합 tracking / ACTRATE 험지 진행은 각기 장점이며 만능 1위 없음. `LINTRACK-075 corrected5K`는 PERSONAL 다른 계보의 비교 context이고, `ANGTRACK-065` PERSONAL full 평가 및 단일 정책 분석 수신(HOLD; H3 15/384 initial-cohort contact 종료), `ACTRATE-001` 학습·PERSONAL 분석 완료/HOLD. 기존 raw 평가가 없어서 새 GPU를 실행해야 한다는 주장은 철회하고, 정책 선택에는 독립 학습 seed/대표 checkpoint·실전 stairs/boxes 검증이 추가로 필요하다고만 기록한다.

## 2026-10-10 고정평가 원본 3개 GitHub 추적 완료 · 비교 한계

[case별 3정책 보고서 비교 및 실제 ZIP 체크포인트·Release SHA 정리](../experiments/h1/analysis/2026-10-10_H1_SCENARIO7_CROSS_POLICY_REPORT_LEVEL_COMPARISON.md). `TERM-50/model_2800`, `ORIENT-100/model_2850`, `ACTRATE-0001/model_2700`의 **기존 PERSONAL Windows camera-off `scenario7` ZIP**을 각각 GitHub Originals manifest와 NVIDIA Release에서 찾았다. 확인된 공통은 evaluator task/handoff commit, protocol SHA `d406a296…7062d34`, eval seed 4201/4202/4203, 128 env, 8 cases, 20초다. **기존 "TERM-50 평가 ZIP 없음" 상태는 구식**이다. 다만 GitHub 커넥터는 private ZIP/Release의 바이너리 추출을 지원하지 않고 Originals `.zip`도 LFS pointer로 표시된다. 따라서 `TERM-50` 자체의 H1/H3/H5/H6/H7 raw 수치, 대응 cohort별 Δ, effective terrain/initial-state 일치, training source/PPO 완전 정합성과 인과 결과는 **아직 검증하지 못했다**.

보고서 값만으로 ORIENT가 8-case 중 5개의 tracking에서 ACTRATE보다 낮고 action-change RMS는 8/8 case 최소이며, ACTRATE는 H2 및 H6 상·하 tracking과 H5 rough P05 진행(`9.592m` vs ORIENT `8.863m`)에서 유리하게 관측된다. 그러나 ORIENT의 H1 비의도 전진도 `1.633m`, ACTRATE는 `1.987m`로 둘 다 정지 명령 실패 축이 있고, ACTRATE H6 하행 action RMS `0.540` vs ORIENT `0.464`도 trade-off다. 다음 작업은 **새 GPU가 아니라 이미 보존된 세 ZIP의 raw `episodes.jsonl`을 인증된 바이너리 접근 환경에서 읽어 `(scenario,case,seed,env_id)`로 대응시키고 manifest/resolved config를 대조한 다음** baseline 대비 방향·H5 worst tail·H1/H3 leak·H6 yaw/action 비용을 확인하는 것. 명령·reset·지형이 실제 대응인지 확인하기 전에는 `same seed=paired terrain`이라 가정하지 않는다. OFFICIAL 학습 완료/단일 평가 완료를 reward 효과나 제출 성과로 바꾸지 않는다.

## 2026-10-10 ACTRATE-0001 model_2700 PERSONAL 정책 행동 분석 — HOLD

[원문](../incoming/other/reviewed/H1_MODEL2700_POLICY_ANALYSIS_20261010.md) · [판정·재사용 비교 계획](../experiments/h1/analysis/2026-10-10_ACTRATE0001_MODEL2700_POLICY_REVIEW.md) · [OFFICIAL 학습 계보](../../../research/experiments/h1/exp-h1-action-rate-relaxation.md).

`ACTRATE-0001`은 OFFICIAL fresh3K `20261009-142350-h1-actrate-0001-fresh3k` COMPLETED/PASS, 해당 auto-best **`model_2700.pt`**(SHA `e54d3389…93ca7ae`)가 Windows PERSONAL 6영상+`scenario7`에서 3,072/3,072개 20초 생존했다. **정책 행동 분석 보고서도 수신**됐으며 품질 판정은 **HOLD**다. 후속 평가를 새 학습 Run, best가 아닌 `model_2950`, OFFICIAL 점수나 통제 비교로 착각하지 않는다.

- **장점:** H2 명령 15m에 body-frame 전진 **15.326m**, H7 외란 명령 10m에 **10.542m**, H6 경사 상/하 **20.052/19.834m**; 짧은 boxes/rough 접지 보행 영상 긍정, 20초 평가 base-contact 0.
- **약점:** H1 zero 명령에도 비의도 전진 **1.987m** / 월드 순변위 크기 중앙값 **2.012m**, H3 lateral 명령 중 전진 **1.677m**, H5 rough worst `4202/env108` 전진 **8.815m**·tracking **0.2908**·posture RMS **0.0999**, H6 높은 action Δ RMS **0.534/0.540**. 계단 중앙 다단 통과는 미입증이다. H1 stall_fraction=0은 무명령 구간의 분모 0이라서 제자리 성공 지표가 아니다. `01_stairs.mp4` black frame은 캡처 결함이다.
- **1순위 기존자료 대조:** unchanged `h1-submit-2 / TERM-50 model_2800` PERSONAL `scenario7` 평가 raw에 대해 protocol SHA `d406a296…7062d34`, case/seed/terrain/command/source/PPO parity를 확인해 H1/H3 편향, H5 하위 꼬리, H6 action/yaw, H7 진행·종료 비교. **2순위** `ORIENT-100/model_2850`은 별도 행동 후보 비교, reward 인과 대조가 아니다. 결과가 없다면 HOLD 유지; 새 GPU 평가/학습은 자동 시작하지 않는다.

## 2026-10-10 `LINTRACK-075` corrected5K / `model_4997` PERSONAL 정책 분석

[보고서 원문](../incoming/other/reviewed/H1_LINTRACK-075_CORRECTED5K_POLICY_ANALYSIS_20261010.md) · [통합 판정](../experiments/h1/analysis/2026-10-10_LINTRACK075_CORRECTED5K_MODEL4997_POLICY_REVIEW.md) · [H-008 계보](../../../research/experiments/h1/H-008.md).

이 분석은 **기존 PERSONAL corrected H-008 R04**(Run `20260925-091257-h1-h008-corrected-control-to5k-h1-corrected-2026`) final `model_4997.pt`(SHA `4349fe56…b6d`)의 **후속 Windows 행동 평가**다. 보고서 내 ZIP은 학습 Run ID/preset을 null로 보존하지만 정책 SHA가 이미 기록된 학습 checkpoint와 일치한다. 새로운 fresh/resume 학습 Run, OFFICIAL 평가나 공식 점수는 아니다.

- **강점:** 동일 `scenario7` 8-case, seeds 4201–4203 ×128 = 3,072개 20초 timeout 생존, base-contact failure 0. H2 15.015m(명령 15m), H7 10.038m(명령 10m), H6 경사 상/하 19.943/19.776m의 **body-frame 전진**은 실제 이동 증거다.
- **위험:** H5 rough 극단 cohort `seed 4202/env 41` 전진 2.8708m, stall 0.664(20초 생존); H1 zero-command world 순변위 0.516m, H3 좌우 왕복 종료 world 순변위 1.280m; H6 yaw 절대오차 최대 사례 0.2613rad/s, action Δ RMS 하행 0.5098. Stair/inverted-stair 다단 중앙 통과는 관찰·정량 평가 모두 미확인, boxes camera-off case 없음.
- **판정:** 실제 보행 능력을 가진 **내부 후보 HOLD**. 3072/3072 생존은 장애물 완주와 다른 판정이며 evaluator 기본 reward `lin=0.5/term=-5`는 학습 reward가 아니다. 영상과 camera-off 테스트 명령/terrain이 달라 통제 A/B로 취급하지 않는다.
- **1순위 대조:** 이미 수납된 `h1-submit-2 / TERM-50` 동일 `scenario7` PERSONAL raw `episodes.jsonl`/manifest/config가 있다면 프로토콜 SHA `d406a296…7062d34`, source/PPO/case/seed/command/terrain/horizon 비교 후 H5 worst-case, H1/H3 잔류, H6 yaw/action, H7 progress를 재집계한다. 자료가 없으면 HOLD. **새 GPU/영상/학습은 별도 승인 없이는 시작하지 않는다.**

## 2026-10-02 Round-4 결과 이후 현재 H1 planned sequence

### 평가기 상태

2026-09-30에는 H1 fixed evaluator/paired harness가 없었다. 2026-10-06 H1 Windows 통합 launcher 설치와 CPU 회귀 테스트 60개가 완료됐고, **2026-10-07에는 H1 `ORIENT-100 / model_2850.pt`의 실제 PERSONAL Windows 6영상 및 camera-off `scenario7` full 평가가 완료**된 자료를 수신했다(8 case × 3 seed × 128 env = 3,072 episode; child exit 0). 따라서 **H1 전체 GPU 평가 미실행**이라는 과거 문구를 현재 상태로 재사용하지 않는다. 다만 단일 정책 full 완료와 **2026-10-10에 보존된 3개 ZIP의 원본 9,216 episode 대응-index 분석까지 완료**됐지만, H1 reward 인과 효과·동일 물리 초기 지형·공식 NCRC 점수는 미검증이다. 상세 원문은 [ORIENT 분석](../incoming/other/reviewed/H1_ORIENT-100_POLICY_ANALYSIS_20261007.md)과 [Experiment](../../../research/experiments/h1/exp-h1-rough-terrain-orientation-relaxation.md)를 따른다.

### Round-4 AIRTIME-025에서 확인된 것

`h1-submit-4`의 공식 평가에는 시뮬레이션 56.37/70, 설계 의도 20/20, 리포트 품질 10/10이 기록됐다. 세 구성 점수의 합은 86.37/100으로 `h1-submit-2`의 종합 점수와 수치상 같지만, Round-4 수신 원문에는 별도의 종합 점수 필드가 없었다. 세부 시나리오는 다음처럼 재분배됐다.

| 시나리오 | Round 2 `h1-submit-2` | Round 4 `h1-submit-4` | 변화 |
| --- | ---: | ---: | ---: |
| 제자리 균형 | 8.62 | 8.58 | -0.04 |
| 전진 추종 | 11.24 | 11.34 | +0.10 |
| 좌우 추종 | 5.73 | 5.72 | -0.01 |
| 회전 추종 | 5.66 | 5.68 | +0.02 |
| 약한 요철 | 8.17 | 8.00 | **-0.17** |
| 완만한 경사 | 8.47 | 8.53 | +0.06 |
| 밀침 회복 | 8.48 | 8.52 | +0.04 |

따라서 AIRTIME을 추가로 올리는 것은 현재 다음 우선순위가 아니다. 다만 Round-2는 fresh 5K, Round-4는 fresh 10K라서 공식 점수만으로 `feet_air_time 0.20→0.25`의 단독 효과를 격리할 수는 없다. 확인된 사실은 **Round-4 AIRTIME-025 제출의 세 구성 점수 합계가 Round-2 종합 점수를 수치상 넘지 못했다**는 것이다.

### ORIENT-100 fresh 3K — OFFICIAL 학습 완료 / PERSONAL 행동 HOLD

새 Experiment 질문은 `exp-h1-rough-terrain-orientation-relaxation`이다. 새 H-ID를 발급하지 않는다.

- 기준: frozen `h1-submit-2`
- 변경: `flat_orientation_l2 -1.5 → -1.0` **한 항목만**
- `feet_air_time=0.20`, `termination=-50`, linear/angular tracking `0.5/0.5`, `ang_vel_xy=-0.05`, `action_rate=-0.0005` 유지
- 실제: **OFFICIAL fresh 3K COMPLETE/PASS**, seed 42, 4096 env
- checkpoint parent 없음
- Run: `20261006-133517-h1-orient-100-fresh3k-official`; auto best `model_2850.pt`, 마지막 보존본 `model_2950.pt`. 50회 간격 60개 보존. 2026-10-07 PERSONAL `model_2850` 6영상/full 평가 분석에서 행동 후보 HOLD를 판정했다. `model_2950`은 이 평가의 source가 아니다. [원본·Release·SHA 접수 기록](../experiments/h1/training/2026-10-06_ORIENT100_OFFICIAL3K_EVIDENCE_INTAKE.md).
- 세부 계획: [research plan](../../../research/experiments/h1/exp-h1-rough-terrain-orientation-relaxation.md)

학습 시계열의 역사적 비교는 source/PPO/seed/schema parity가 확인될 때 official `h1-submit-2` 5K의 **첫 3K 구간**과 새 Run의 0→3K TensorBoard·console 창을 맞춰 본다. terrain, XY/yaw error, base-contact, timeout/episode length, action std와 available posture/action reward term을 함께 본다. native 6지형 영상은 AI의 정성 행동 분석용이며 공식 score proxy로 쓰지 않는다.

### 2026-10-07 ORIENT-100 행동 평가 반영

- [원본 분석](../incoming/other/reviewed/H1_ORIENT-100_POLICY_ANALYSIS_20261007.md) 대상은 **OFFICIAL fresh 3K 학습 Run의 automatic-best `model_2850.pt`**와 일치하는 SHA를 기록한 PERSONAL 평가 ZIP이다. 영상/평가 내부 `source_run_id=null`이며 연결 근거는 별도 공식 train evidence·checkpoint SHA이다.
- **7 scenario / 8 case / 3 seed / 128 env = 3,072/3,072 episode 생존**, 20초 timeout, base-contact failure 0. 전진 H2 15.408m, push H7 10.530m, 경사 H6 상/하 20.426/20.173m는 몸체 전진 적분으로, world 순이동·계단 완주나 공식 점수가 아니다.
- 정지 H1에서도 비의도 전진 적분 **+1.633m/20초**, 순수 횡이동 H3에서 **+1.180m**. rough H5 평균 tracking error **0.1709**, 전진 평균 9.451m / P05 8.863m / 최소 7.831m, tracking P95 0.1948. 100% 생존만으로 정지 품질·거친 지면 하위 꼬리를 놓치면 안 된다.
- 여섯 영상은 초기 boxes/rough 진행을 지지하지만 중앙 다단 계단 완주·회복시간은 입증하지 않는다. `02_inverted_stairs.mp4`의 짝수 프레임 검정 현상은 **캡처 결함**이다. 영상과 camera-off 평가의 명령/지형/episode를 동일한 것으로 합치지 않는다.
- **판정: HOLD**, REJECT 아님. baseline 대비 reward 개선은 같은 evaluator의 `h1-submit-2 / TERM-50` 데이터가 없어 미확인. **1순위** 저장된 동일 protocol 대조의 `episodes.jsonl`, `evaluation_manifest.json`, `resolved_configs.json` 검색 및 case/seed 조건 점검; 없을 때만 별도 GPU 평가 필요성 판단. 이 기록은 새 GPU 실행 승인이 아니다.

### 외부 성공 사례를 prior로 쓰는 범위

다음 자료는 **우리 evaluator와 동일하지 않은 외부 prior**다. 값 자체를 최적값으로 복사하지 않고, 어떤 단일축을 먼저 검증할지 정하는 근거로만 사용한다.

- IIT Delhi CoE-BIRD 2026 Unitree H1 uneven-terrain/staircase project: orientation penalty `-1.0`, linear/angular tracking `+1.0/+0.5`, action-rate `-0.01` 등을 사용하고 rough/stairs curriculum과 평가를 공개했다.
  - https://github.com/iitd-bird-robotics/2026-major-Bipedal_Locomotion_Using_RL
- public Isaac Lab Unitree H1 rough-terrain run: `flat_orientation_l2=-1.0`, `action_rate_l2=-0.005`를 포함하며 공개 결과는 4K에서 terrain 5.76/8, velocity error 0.24 m/s, fall rate 0.74%를 보고한다.
  - https://github.com/egeozgul/humanoid-locomotion-isaaclab
- Humanoid-Gym/RobotEra는 real-robot zero-shot locomotion에 tracking, gait/contact, clearance, slip, action smoothness를 묶어 사용한다. 함수와 scale이 달라 숫자 직접 비교는 하지 않는다.
  - https://github.com/roboterax/humanoid-gym

이 자료와 Round-4 요철 하락을 합치면 현재 질문은 "airtime을 더 늘릴까"가 아니라 **"upright posture 제약을 `-1.5→-1.0`으로 완화하면 불규칙 지면 적응 여유를 얻을 수 있는가"**다.

### ACTRATE-001 후속 초기 계획(역사적; 학습·행동 분석은 이후 완료)

`ACTRATE-001` (`action_rate_l2 -0.0005 → -0.001`)은 이후 OFFICIAL fresh3K COMPLETE/PASS · PERSONAL `model_2850` 행동 HOLD로 갱신된 별도 single-delta Experiment `exp-h1-action-rate-smoothing`이다. 실행 순서는 `ORIENT-100` evidence를 먼저 검토한 뒤로 두되, ACTRATE Run은 ORIENT checkpoint를 resume하거나 ORIENT=-1.0을 상속하지 않는다. frozen `h1-submit-2`에서 `action_rate_l2`만 바꾼 OFFICIAL fresh 3K, seed 42, 4096 env를 계획한다. 외부 성공 시스템들이 더 강한 action smoothing을 쓰는 방향성은 참고하되 reward 함수·scale이 달라 `-0.005`나 `-0.01`을 그대로 가져오지 않는다. 공개 실패 자료의 `-0.0025` long-run negative 신호도 있으므로 첫 계획값은 **-0.001**이다. 실제 실행 전에는 Run ID를 발급하지 않고, `ORIENT-100`과 같은 Run에 합치지 않는다. 세부 문서는 [ACTRATE plan](../../../research/experiments/h1/exp-h1-action-rate-smoothing.md)을 따른다.

### 2026-10-10 tracking 단일변수 가설 2개 — OFFICIAL fresh3K 완료/PASS

당초 2026-10-09에 제안한 신규 질문 두 가지는 **2026-10-10 현재 각각 OFFICIAL fresh3K 학습 COMPLETED/PASS**로 변경됐다. `ACTRATE-0001`은 Run `20261009-142350-h1-actrate-0001-fresh3k`(seed42, 4096 env, no parent; `model_2700.pt` auto-best와 keeper `model_2950.pt` 별개), `ANGTRACK-065`는 Run `20261009-155344-h1-angtrack-065-fresh3k`(동일 seed/env, no parent; best·keeper 모두 `model_2950.pt`)이다. 두 Run은 frozen `h1-submit-2 / TERM-50`의 서로 다른 단일 reward delta를 시험했고 상호 체크포인트를 상속하지 않는다. 전체 source/PPO parity는 미확인. `ACTRATE-0001/model_2700` PERSONAL 6영상+scenario7 전체 평가와 단일 정책 행동 분석을 수신했고 정책은 **HOLD**, matched 비교는 **미완료**이며 `ANGTRACK-065` 고정 평가·단일 정책 분석은 수신됐고(HOLD), TERM-50 matched raw 비교는 미완료다. 따라서 **당시 계획으로 남았던 `ACTRATE-001`도 2026-10-10 OFFICIAL fresh3K 학습을 완료하고 후속 PERSONAL 행동 분석 HOLD로 갱신됨**이다. [ACTRATE 근거](../experiments/h1/training/2026-10-09_ACTRATE0001_OFFICIAL3K_EVIDENCE_INTAKE.md) · [ANGTRACK 근거](../experiments/h1/training/2026-10-10_ANGTRACK065_OFFICIAL3K_EVIDENCE_INTAKE.md) · [ACTRATE Windows 평가](../operations/windows_h1_video_evaluation/2026-10-10_ACTRATE0001_MODEL2700_PUBLICATION.md).

| 새 Experiment | descriptor | 한 항목 reward delta | 주요 trade-off |
| --- | --- | --- | --- |
| [`exp-h1-action-rate-relaxation`](../../../research/experiments/h1/exp-h1-action-rate-relaxation.md) | `ACTRATE-0001` | `action_rate_l2 -0.0005→-0.0001` | x/y/yaw tracking·반응성 vs action jitter·낙상·stall |
| [`exp-h1-angular-tracking-boost`](../../../research/experiments/h1/exp-h1-angular-tracking-boost.md) | `ANGTRACK-065` | `track_ang_vel_z_exp 0.5→0.65` | yaw 및 전체 tracking vs XY·지형 진행·base-contact |

**1순위 대조군:** 완료된 OFFICIAL unchanged fresh3K `h1-submit-2` Run `20261008-062732-h1-term-50-fresh3k-control`(seed42, 4096 env, no parent). 연계된 `model_2800` PERSONAL Windows full 자료도 있으나 source/PPO parity와 완성된 paired A/B 분석은 아직 미확인이다. **추가 비교:** action-rate `-0.001`(ACTRATE-001 OFFICIAL fresh3K COMPLETE/PASS·PERSONAL model2850 분석 수납/HOLD), `-0.0005`(기존 control COMPLETE/PASS), `-0.0001`(신규 OFFICIAL Run COMPLETE/PASS)을 같은 학습량과 evaluator에서 비교한다. 이미 실험한 PERSONAL `ANGTRACK-075` BASE fresh1K는 terrain 0/base-contact 100%의 실패 prior이고, corrected PERSONAL `LINTRACK-075`는 XY error 감소·yaw error 증가 prior이다. 이들은 OFFICIAL 동일 조건 control이 아니다.

**판정:** x/y/yaw tracking, stop/lateral drift, 실제 진행/stall, base-contact/fall, action-delta를 따로 비교한다. 생존률 하락을 어느 정도 감수하더라도 추종 이득을 낙상·정체 손실이 상쇄하면 기각한다. 신규 문서 등록은 학습·평가·export 실행 승인이 아니다.

## 현재 H1 schedule 명명과 미실행 비교

새 이름은 [Experiment naming](../../../research/EXPERIMENT_NAMING.md)을 따른다. `H-xxx`와 `HS-xxx`는 기존 고정 설정·schedule 질문의 legacy 주소이고 더 발급하지 않는다. legacy H-005·H-010 주소 아래의 fresh, corrected resume, unchanged continuation은 각기 다른 실제 학습 Run이며, 동일 최종 설정이라도 부모·학습 경로를 합치지 않는다. Archive `r01`을 registry `R01`로 치환하지 않는다: `AIRTIME-025` fresh 3K Run `20260927-032343-h1-h005-fresh3k-r01-20260927`과 `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch fresh 3K Run `20260927-043527-h1-h010-fresh3k-r01-20260927`은 각각 legacy R03이다. OFFICIAL `h1-submit-4 / AIRTIME-025` fresh 10K evidence Run `20260927-123428-h005-fresh10k-official`은 legacy R05다. [registry](../../../research/EXPERIMENTS.md).

- **`exp-h1-stable-first-track-switch` (legacy HS-001, PLANNED question; not current execution priority):** `AIRTIME-025` fresh 3K final `model_2999.pt`에서 `lin=0.75`로 +2K. 같은 부모에서 `AIRTIME-025` 설정을 유지하는 unchanged continuation이 control이다.
- **`exp-h1-track-first-stability-switch` (legacy HS-002, PLANNED question; not current execution priority):** `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch fresh 3K final `model_2999.pt`에서 `lin=0.5`로 +2K. 같은 부모에서 `lin=0.75` 설정을 유지하는 unchanged continuation이 control이다.

두 phase-1 final의 보고서 SHA는 각각 `ff51151a…e25a2`, `088eb7fe…1ceb38`이며 실제로 HS 질문을 재개하기 직전에 train evidence와 전체 SHA를 재대조한다. 이 네 child Run은 아직 시작하지 않았고 **현재 실행 우선순위도 아니다**. HS를 나중에 수행한다면 같은 부모의 전환/무전환 쌍을 동일 조건으로 만들고 비교한다. H1 통합 launcher 설치·CPU 검증은 완료됐지만 이 네 child를 대상으로 한 GPU full/paired evaluation은 아직 없으므로 이를 이미 수행된 고정 평가처럼 쓰지 않는다. 기존 `AIRTIME-025`/`track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch PERSONAL 결과나 서로 다른 부모의 단순 비교를 schedule 효과로 부르지 않는다. 과거 절의 `S1` 같은 표시는 당시 스크리닝 이름일 뿐 이 새 `HS` 명명과 무관하다.

## 2026-09-28 OFFICIAL h1-submit-4 / AIRTIME-025 fresh 10K vs h1-submit-2 / TERM-50 fresh 5K

[수신한 심층 보고서](../incoming/other/reviewed/H1_H005_OFFICIAL10K_VS_TERM50_OFFICIAL5K_DEEP_ANALYSIS_20260928.md)는 OFFICIAL `h1-submit-4 / AIRTIME-025`의 `feet=0.25`와 `h1-submit-2 / TERM-50`의 `feet=0.20`을 비교한다. 두 Run은 모두 fresh·seed 42·4096 env·track `0.5`·termination `-50`이지만 전체 학습 길이는 10K 대 5K다. 보고서의 같은 **5K 단계** late-500에서는 `AIRTIME-025`의 XY error가 `0.3655`로 TERM-50 `0.3690`보다 근소하게 낮았으나 terrain `5.6570<5.7306`, yaw error `0.9642>0.9213`, training base-contact `28.549%>28.150%`였다. 창을 바꾸면 XY 방향도 유지되지 않아 `feet=0.25`의 명확한 전체 우위는 없다. `AIRTIME-025` 자신의 5K→10K에서 terrain·yaw·접촉·episode length는 개선됐으나 이는 추가 학습량과 분리할 수 없다.

6영상은 boxes·random rough·inverted stairs에서 진행을 보여 주는 정성 자료지만 checkpoint source manifest가 없고 TERM-50의 대응 6영상 조건도 맞지 않는다. 자동 best `model_9800.pt`와 최신 numbered `model_9950.pt`는 서로 다른 후보이며, loose `policy.pt`의 source도 확정되지 않았다. **`h1-submit-4 / AIRTIME-025`는 이미 제출·공식평가 완료 상태이고, 향후 재사용·원인분리 관점의 일반적 AIRTIME-025 채택 주장은 HOLD**한다. 이 HOLD는 과거 Round-4 제출 상태를 되돌리는 뜻이 아니다. H1 evaluator의 Windows GPU full compatibility가 실제 검증된 뒤에는 OFFICIAL `AIRTIME-025` `9800`·`9950`과 `h1-submit-2 / TERM-50` `4900`을 동일 terrain·command·seed-set·episode 조건에서 tracking, contact/survival, 실제 진행·stall로 대조한다. 현재는 해당 수치 비교가 미실행이며, native 영상은 정성 evidence로만 취급한다. 이 보고서의 “아직 제출 전”은 작성 시점 진술이며 이후 `h1-submit-4 / AIRTIME-025` 제출과 공식 평가가 완료됐다. 2026-09-30 공식 평가에서는 시뮬레이션 56.37/70, 설계 의도 20/20, 리포트 품질 10/10이 수신됐고 구성 점수 합계는 86.37/100이다. 원본 포털 ZIP·수령증·정확한 제출 시각과 제출 `policy.pt`의 정확한 numbered source checkpoint는 여전히 미확인이다.

## 2026-09-27 PERSONAL H1 3-Run 완료 — AIRTIME-025·lin=0.75 분석 반영

[날짜별 계획](../planning/historical/2026-09-27_H1_PERSONAL_FRESH_AND_CONTINUATION_PLAN.md)에 등록한 `AIRTIME-025` fresh 0→3K, `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch fresh 0→3K, corrected `AIRTIME-025` final `model_2998.pt`에서 reward를 바꾸지 않은 +2K continuation이 완료됐다. 세 train archive의 metadata는 PERSONAL·exit 0·validation PASS를, 실행 명령은 4096 env를, native `env.yaml`은 seed 42를 기록한다. 보존 reward source는 TERM/track/feet 순서로 `-50/0.5/0.25`, `-50/0.75/0.25`, `-50/0.5/0.25`다. 두 fresh reward source의 유일한 내용 차이는 track `0.5` 대 `0.75`; `AIRTIME-025` continuation과 fresh reward source는 동일하다. 이것만으로 전체 PPO·simulation 조건을 같다고 단정하지 않는다. `fresh`는 checkpoint 없음이지 BASE reward가 아니다. Run 04의 source checkpoint SHA는 corrected Run 02의 final과 일치하지만 metadata의 `source_provenance_verified=false`를 PASS로 재해석하지 않는다. 첫 resume 시도는 손상 checkpoint 로드 오류로 종료됐고 완료 Run에 넣지 않는다. [수신 기록과 Release](../experiments/h1/training/2026-09-27_H1_FRESH_AND_CONTINUATION_EVIDENCE_INTAKE.md).

다운로드·분석 입력은 (1) `AIRTIME-025` fresh 3K / corrected `AIRTIME-025` 3K / corrected unchanged 3K control, (2) `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch fresh 3K / `AIRTIME-025` fresh 3K / corrected `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch 5K, (3) `AIRTIME-025` continuation 3K→5K / corrected `AIRTIME-025` 3K / `AIRTIME-025` fresh 3K의 **각 train+video, 묶음당 6개**다. `AIRTIME-025` 관련 비교·후속 재분석과 (2)의 `lin=0.75` 대 `AIRTIME-025` fresh 비교 보고서가 도착했다. 후자 보고서의 주된 직접 대조는 두 fresh 3K Run이며 corrected `lin=0.75` branch는 계보가 다른 맥락 자료다. 같은 seed만으로 동일 terrain/command sequence가 보장되지 않고 H1 fixed evaluation 결과도 아직 없다.

### `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch fresh 3K vs `AIRTIME-025` fresh 3K

두 Run은 PERSONAL·fresh 3K·seed 42·4096 env이며 보존 reward source의 차이는 `track_lin_vel_xy_exp: 0.50 → 0.75`다. raw 보고서가 비교한 late-500 training 지표는 다음과 같다. 이는 단일 seed 학습 곡선이지 고정 evaluator 점수가 아니다.

| Run | terrain | XY error | yaw error | training base-contact | episode length |
| --- | ---: | ---: | ---: | ---: | ---: |
| `AIRTIME-025` fresh (legacy H-005 R03) | 5.50379 | 0.37355 | 1.02692 | 29.935% | 775.83 |
| `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch fresh (legacy H-010 R03) | 5.49196 | 0.33248 | 1.58899 | 30.491% | 759.33 |

`track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch fresh의 XY error는 낮지만 yaw error와 contact는 높고 terrain 우위도 없다. XY·yaw 방향은 late-700/500/300에서 유지되어 단일 마지막 구간의 우연으로만 치부할 수는 없지만, 전체 승자·reward 인과 효과·OFFICIAL 성능으로 확정할 수 없다. 두 6지형 영상은 각각 final `model_2999.pt`가 아닌 자동 best `AIRTIME-025` `model_2750.pt`, `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch `model_2700.pt`에서 생성됐고 command·terrain seed·difficulty·초기 상태가 matched되지 않았다. **`track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch fresh 후보는 final 두 `model_2999.pt`의 동일 조건 fixed paired 평가 단계까지만 PROMOTE**한다. XY/yaw와 실제 진행·stall, 낙상/contact, posture/action cost를 함께 보고 채택을 결정한다. [원문](../incoming/other/reviewed/H1_H010_FRESH3K_R01_VS_H005_FRESH3K_R01_DEEP_ANALYSIS_20260927.md).

### `AIRTIME-025` fresh 3K · corrected 3K · corrected 5K 비교

| 비교 | late-500 terrain / XY error / yaw error / training base-contact | 판단 |
| --- | --- | --- |
| corrected `TERM-50` unchanged 3K control (legacy H-001 R06) | 5.5010 / 0.3695 / 1.0455 / 29.616% | corrected `AIRTIME-025`와 같은 부모의 보존 요약값; 두 번째 분석 입력에는 raw control archive가 없었다. |
| `AIRTIME-025` corrected (legacy H-005 R02), final `model_2998` | 5.4776 / 0.3609 / 1.0410 / 29.761% | control 대비 XY 약 2.3% 낮지만 terrain 약 0.4% 낮고 접촉 +0.145%p; 작은 방향성 신호와 trade-off. |
| `AIRTIME-025` fresh (legacy H-005 R03), final `model_2999` | 5.5038 / 0.3736 / 1.0269 / 29.935% | corrected 3K와 한쪽이 모든 축에서 우월하지 않음; 초기화·학습 경로 비교이지 reward 효과 아님. |
| `AIRTIME-025` continuation (legacy H-005 R04), final `model_4997` | 5.6646 / 0.3529 / 0.9402 / 28.729% | 동일 설정·실제 Run 02 final parent에서 +2K; Run 02 대비 terrain +3.42%, XY error -2.22%, yaw error -9.68%, 접촉 -1.032%p. late-300도 같은 방향이나 reward 단독 효과는 아님. |

`AIRTIME-025` continuation의 parent `model_2998.pt` SHA는 corrected `AIRTIME-025`의 실제 checkpoint 바이트와 대조됐다. 반면 corrected `TERM-50` parent는 두 번째 분석 입력 안에 없으므로 기록상 연결과 직접 대조를 구분한다. `AIRTIME-025` continuation 첫 약 260 iteration은 resume 시 curriculum/episode accumulator 재시작에 따른 재적응 구간으로, 경계 step의 급변을 즉시 성능 변화로 읽지 않는다. 18개 MP4의 manifest/checkpoint SHA는 원문에서 대조됐지만 영상은 각각 fresh `model_2750`, corrected 3K final `model_2998`, corrected 5K 자동 best `model_4800` 기반이다. 특히 boxes에서 4800 영상이 약 14–15초에 패치를 벗어난 샘플은 유망한 관찰일 뿐 command·지형 instance·초기 상태가 고정된 우월성 증거가 아니다. fresh final 2999와 Run 04 final 4997의 행동은 아직 미확인이다.

**현재 `AIRTIME-025` PERSONAL lineage 판단은 향후 paired-evaluation 우선 후보(PROMOTE); H1 통합 launcher 설치·CPU 60개 검증 완료, 해당 `AIRTIME-025` 후보의 Windows GPU full/paired evaluation 미실행, 일반적 채택은 HOLD.** continuation 후반에 terrain·tracking·접촉의 공동 붕괴가 없어 final numbered `model_4997.pt`를 기본 대표 후보로 둔다. 먼저 unchanged control final 2998, corrected `AIRTIME-025` final 2998, continuation final 4997을 같은 command·terrain·seed-set·horizon에서 평가하고, 학습 경로까지 볼 때 fresh final 2999를 추가한다. 실제 진행/stall·x/y/yaw·낙상·자세를 분리하며 새 학습이나 OFFICIAL 제출 우위로 바로 연결하지 않는다. [fresh/3K 원문](../incoming/other/reviewed/H1_H005_FRESH3K_R01_VS_H005_R02_DEEP_ANALYSIS_20260927.md) / [5K continuation 원문](../incoming/other/reviewed/H1_H005_CORRECTED5K_R02_VS_H005_FRESH3K_R01_DEEP_ANALYSIS_20260927.md).

[후속 재분석 원문](../incoming/other/reviewed/H1_H005_FRESH3K_R01_VS_H005_CORRECTED3KTO5K_R02_DEEP_ANALYSIS_20260927.md)은 같은 학습 archive 3개와 영상 bundle 3개를 다시 사용했으며 late-window 수치와 checkpoint identity는 앞선 5K 분석과 실질적으로 같다. 새 영상 관찰은 fresh `model_2750`의 boxes 약 9.1–9.5초 큰 자세 손실 뒤 9.7초 무렵 회복이다. 이전 보고서는 그 구간을 촘촘히 샘플링하지 않아 이를 기록하지 않았으므로 직접 모순은 아니다. 다만 command·box instance·난이도·초기 상태가 맞춰지지 않아 정책 간 회복 성능의 우열로 승격하지 않는다. 후속 보고서는 `model_4800` 대 final `model_4997` 평가를 첫 순위로 제안하지만, 이는 두 checkpoint의 행동 대표성만 묻는다. `AIRTIME-025` reward 효과를 판단할 때는 위 unchanged control 포함 paired 평가가 필요하며, late joint collapse가 없는 현재 final 4997 기본 대표 원칙을 자동 best 4800으로 바꾸지 않는다. 후속 보고서의 “가설 HOLD”는 인과적 채택 보류, registry의 “평가 단계까지만 PROMOTE”는 다음 검증 진입을 뜻해 양립한다.

여기서 “corrected 5K”는 **global endpoint 4997**을 가리킨다. 앞의 약 1.5K는 부모의 feet `0.20` 학습이고, 이후 corrected `AIRTIME-025` + continuation에서 `0.25`로 추가 학습한 구간은 약 3.5K다. 처음부터 `0.25`로 5K를 학습한 fresh 실험으로 표기하지 않는다.

## 2026-09-26 corrected LINTRACK-075 3K → 5K sibling 비교

corrected `LINTRACK-075` final `model_2998.pt`(legacy H-008 R03; 기록 SHA `49fdb297…14983`)에서 unchanged 5K control과 `HIPDEV-030`, `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch, `HIPDEV-010`을 각각 +2K resume했다. 네 child는 동일 기록상 부모·seed 42·4096 env·추가 2K·PPO/source를 사용하며 각 branch의 유일한 reward 변경을 control과 직접 비교한다. 입력 네 파일마다 원본 부모 checkpoint 바이트를 독립 재해시한 것은 아니므로 metadata상 동일 부모 기록과 실제 최종 checkpoint↔영상 SHA 검증을 구분한다. 수치는 **training TensorBoard late-500** 평균이고 공식 evaluator 성능이 아니다.

| Run | control 대비 단일 Delta | terrain / XY error / yaw error / training base-contact | 현재 판단 |
| --- | --- | --- | --- |
| `LINTRACK-075` unchanged control (legacy H-008 R04) | 없음 | 5.6718 / 0.32938 / 1.42790 / 29.420% | 비교 기준 |
| `HIPDEV-030` (legacy H-009 R02) | hip `-0.20→-0.30` | 5.63891 / 0.32921 / 1.32786 / 29.065% | yaw 신호는 late-300에도 유지; terrain·접촉·진행의 결정적 우위 없음, HOLD |
| `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch (legacy H-010 R02) | feet `0.20→0.25` | 5.6611 / 0.32957 / 1.36436 / 28.821% | yaw·접촉 방향의 작은 이득과 자세 비용 trade-off; **향후 paired-evaluation 우선 후보(PROMOTE); H1 통합 launcher 설치·CPU 60개 검증 완료·이 `AIRTIME-025` 계보의 Windows GPU full/paired evaluation 미실행** |
| `HIPDEV-010` (legacy H-011 R02) | hip `-0.20→-0.10` | 5.6420 / 0.32886 / 1.40613 / 29.174% | 작은 tracking 신호, late-300 접촉 방향 반전·자세 비용 악화; HOLD |

`track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch·`HIPDEV-010`의 boxes 영상에서는 control보다 patch를 일찍 벗어난 듯한 장면이 보고되지만, video manifest의 command·terrain seed·difficulty·초기 상태가 matched라는 증거가 없다. 영상 차이를 승격의 정량 근거로 쓰지 않는다. `HIPDEV-030`의 hip weighted term에서도 실제 비가중 hip deviation을 역산하지 않는다. `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch는 별개의 corrected `AIRTIME-025` 3K와 둘 다 `feet=0.25`지만 **부모 corrected `TERM-50` vs corrected `LINTRACK-075`, track 설정 0.5 vs 0.75, 학습 stage가 다르므로 동일 Run이나 반복 seed가 아니다.** 제출 채택·OFFICIAL 우월성·일반 최적값은 어느 branch도 확인하지 못했다. 2026-09-26 당시에는 새 학습보다 두 final `model_4997.pt`의 동일 command/terrain/seed fixed evaluator에서 x/y/yaw, 실제 진행·stall, 낙상, hip/torso raw posture를 함께 측정하도록 권고했다. 2026-09-27에 계획한 fresh 2회와 `AIRTIME-025` continuation 1회는 모두 실행 완료되었다. `AIRTIME-025` train/video와 위 `lin=0.75` fresh 비교 보고서는 반영했지만 H1 통합 launcher 설치·CPU 검증은 완료됐지만 해당 Windows GPU full 고정 evaluation은 아직 수행하지 않았다. [H-009](../incoming/other/reviewed/H1_H009_R02_VS_H008_CORRECTED_CONTROL_DEEP_ANALYSIS_20260925.md) / [H-010 corrected Run 02](../incoming/other/reviewed/H1_H010_R02_AIRTIME025_CORRECTED_VS_H008_CORRECTED_CONTROL_TO5K_DEEP_ANALYSIS_20260926.md) / [H-011](../incoming/other/reviewed/H1_H011_R02_HIPDEV010_CORRECTED_VS_H008_CORRECTED_CONTROL_DEEP_ANALYSIS_20260926.md).

## 2026-09-25 corrected +0.2 계보: 완료된 PERSONAL 비교

새 corrected `TERM-50` PERSONAL parent(legacy H-001 R05)는 `termination=-50`, `feet_air_time=+0.2`의 fresh 1.5K를 COMPLETE/PASS로 마쳤다. final `model_1499.pt`(SHA-256 `5e3a31502d229884f91faf38962ffd32d63db69a64ca46ed7c1c404671b8ad82`)를 새 부모로 고정했고, 같은 부모에서 unchanged 3K control과 `AIRTIME-025`·`AIRTIME-030`·`LINTRACK-100`·`LINTRACK-075`를 각각 +1.5K resume했다. 여섯 지형 영상은 각각 final numbered checkpoint와 연결된 정성 확인 자료다. 동일 seed만으로 동일 terrain sequence·명령을 보장하지 않으며, 영상은 fixed evaluator가 아니다.

| corrected 3K Run | 부모 대비 단일 Delta | last-500 terrain / XY error / yaw error / base-contact | 판단 |
| --- | --- | --- | --- |
| corrected `TERM-50` unchanged control | 없음 | 5.5010 / 0.3695 / 1.0455 / 29.616% | 비교 기준 |
| `AIRTIME-025` (legacy H-005 R02) | feet `0.20→0.25` | 5.4776 / 0.3609 / 1.0410 / 29.761% | 작은 XY 이득; matched 장기 확인 대상으로 PROMOTE, 채택 아님 |
| `AIRTIME-030` (legacy H-006 R02) | feet `0.20→0.30` | 5.5595 / 0.3774 / 1.0393 / 30.047% | 지형 소폭 이득과 XY·접촉 trade-off; HOLD |
| `LINTRACK-075` (legacy H-008 R03) | track `0.50→0.75` | 5.4526 / 0.3483 / 1.5292 / 30.56% | XY 개선, yaw·지형·접촉 악화; HOLD |
| `LINTRACK-100` (legacy H-007 R02) | track `0.50→1.00` | 5.4302 / 0.3366 / 2.0117 / 30.47% | XY 개선보다 yaw·지형 trade-off가 큼; 현 overall 후보 REJECT |

corrected `TERM-50` 부모의 last-300 terrain 5.050, XY 0.3917, yaw 1.3599, base-contact 30.98%는 새 부모의 1.5K 상태이지 3K control 값이 아니다. `AIRTIME-025`/`AIRTIME-030` 원문 자체는 원본 부모 archive를 입력받지 않아 child metadata의 `source_provenance_verified=false`를 지적한다. 여기서는 별도 보존된 부모 보고서·archive와 기록된 checkpoint SHA를 연결하되, 그 원문 단독으로 부모 검증이 완료됐다고 쓰지 않는다. 모든 결과는 PERSONAL 단일 seed의 방향성 근거이고 OFFICIAL 점수·제출 정책이 아니다. [부모 원문](../incoming/other/reviewed/H1_H001_R05_CORRECTED_PARENT_1P5K_DEEP_ANALYSIS_20260925.md) / [airtime 비교 원문](../incoming/other/reviewed/H1_H005_VS_H006_DEEP_ANALYSIS_20260925.md) / [tracking 비교 원문](../incoming/other/reviewed/H1_H-007_VS_H-008_DEEP_ANALYSIS_20260925.md) / [registry](../../../research/EXPERIMENTS.md).

## 2026-09-21 H1 계보 정정 — 상대 비교용 / 재실험 필요

공식 TERM-50 5K는 feet_air_time=+0.2이고 제출 기록은 유효하다. H-005~008의 실제 부모인 PERSONAL H-001 model_1499(`68fa0a9f…f0c1`)는 feet=-0.2다. H-005/006의 실제 Delta는 -0.2→+.25/+.30, H-007/008은 feet -0.2→+.2와 track .5→1.0/.75를 함께 바꿨다. track 단독 효과 주장을 철회한다.

H-009~011은 실제 H-008 3K model_2998(`d9a30c8a…1912ae`) 안에서 단일변수 형제 비교가 맞다. 다만 사용자의 결정에 따라 **과거 H-005~H-011 전부 HOLD / 재실험 필요**이며 기존 완료 결과는 상대 비교 참고용이다. 새 +0.2 TERM-50 1.5K 부모에서 H-005~008과 unchanged control을 만들고, 새 H-008 3K final에서 H-009~011 및 unchanged 5K continuation을 재검증하는 것은 2026-09-21 당시 계획이다. 이후 실행 상태는 이 문단이 아니라 새 evidence와 가설 registry로 판단한다.

기존 수치·영상·원문은 보존한다. 이를 최종 채택 근거나 검증된 단일변수 효과로 Optuna에 입력하지 않는다. H-004와 개인 H-001의 termination 단독 비교도 feet 차이로 성립하지 않는다. H-012는 별도 fresh 계보이며 공식 TERM-50과의 교차 환경 비교는 인과 검증이 아니다. 실제 parent 설정·checkpoint 계보와 새 Delta를 확인한 뒤 Run별로 기록한다. [상세 정정](../experiments/h1/analysis/2026-09-21_H1_PARENT_AIRTIME_LINEAGE_CORRECTION.md) / [가설 registry](../../../research/EXPERIMENTS.md).



## 2026-10-10 chosen five ACTRATE-0001 comparisons — 2026-10-14 세 완료·두 계획

아래 fresh의 “두 값 변경”은 **frozen `h1-submit-2` 대비 실험 delta**다. 새로 제공된 OFFICIAL 서버의 실제 출발점은 운영진 baseline이므로 `termination_penalty=-5→-50`도 적용해야 한다. preset이 이미 설치돼 있다고 가정하지 말고 실제 reward 전체를 목표 설정과 대조한다(`19`). 기존 서버 재접속·재부팅은 초기화가 아니다.

[최초 다섯 질문](../planning/2026-10-10_H1_ACTRATE0001_FIVE_COMBINATION_HYPOTHESES.md): fresh 조합 두 개(action=-.0001에 feet=.25 또는 feet_slide=-.35)와 같은 ACTRATE 부모의 resume 세 개(feet=.25, lin=.65, angxy=-.08)다. **2026-10-16 현재 fresh 두 개·lin·angxy는 OFFICIAL 학습/PERSONAL 평가/분석 원문 수신 완료, 채택 HOLD**이며 **미실행은 feet=.25 resume 한 갈래**다. Fresh는 preset 대비 두 값, 각 resume는 부모 대비 한 값을 바꾼다. 실행·SHA·원본 링크는 각 Experiment와 최신 registry를 따른다.

lin=.65 model4650 최신 판정 **HOLD**: H1 world XY .228m, H3 잔류2.398m, H2/H7 body 진행14.812/9.757m, H4 yaw .179rad/s, H5 mean/P05/min9.546/9.228/8.974m. [부모·무변경 sibling 포함 raw 비교](../experiments/h1/analysis/2026-10-16_H1_ANGXY008_MODEL4650_POLICY_REVIEW.md)는 이제 완료됐다. 동일 평가 config·키가 reward 인과를 뜻하지는 않는다. [정량·계보](../experiments/h1/analysis/2026-10-11_ACTRATE0001_LINTRACK065_MODEL4650_POLICY_REVIEW.md). ZIP의 학습 계보 null과 별도 OFFICIAL train SHA 연결을 구분한다.

The constraint is one **step per resume branch**, not one Resume Run for all experiments. Do not extend a 5K child again to 7K; multiple +2K siblings from a verified common 3K checkpoint are permissible. Use the original ACTRATE-0001 OFFICIAL evidence `20261009-142350-h1-actrate-0001-fresh3k`; automatic best `model_2700` and final keeper `model_2950` are different and require official index/source_path/SHA/late-trend preflight. The reward-unchanged **model_2700 +2K** control `20261014-111135-h1-actrate-0001-unchanged-cont2k` now has completed training, PERSONAL evaluation and saved-data comparison; no longer pending. Identical final reward `feet=0.25 + action=-0.0001` in Fresh vs Resume cannot prove learning-order effect at 3K versus approximately 5K total. Compare H1 unwanted motion, H3 vy/vx/contact/stall, H4 yaw, H5 mean/P05/min/stall, H6 slope posture/action/progress, H7 push with full protocol parity. Existing H-010 is a distinct PERSONAL parent, not completion of this proposal.


## 2026-09-23 공개 실패 × 내부 계보 교차 분석 — 실험 우선순위 갱신

공개 researchlog의 H1 실패 38건은 공식 채점 결과나 다른 팀의 controlled trial이 아니다. 그럼에도 H1 single-dial 5건과 다중 변경 반례는 **어떤 미해결 질문에 다음 GPU 시간을 쓸지** 고르는 데 유용하다. `track_lin 1.0` 단독 1K early collapse(`reel-11999811`)와 다중 변경 high-terrain 반례, `action_rate -0.0025` 단독 장기 붕괴(`reel-78394459`)와 다중 변경 반례를 함께 보아야 한다. 공개 key 자체를 우리 가설 Run·Optuna trial·공식 성능 근거로 등록하지 않는다. 수치, 출처, 판정 경계는 `20_H1_PUBLIC_FAILURES_AND_EXPERIMENT_PRIORS.md`에 정리했다.

이 자료와 H-005~011 계보 정정을 합친 **2026-09-23 당시 정보가치 순서**는 corrected `feet=+0.2, termination=-50` parent 확정 → 같은 parent의 reward unchanged continuation 확보 → `track_lin 0.5→0.75` 단독 → `termination -50→-100` 단독 → `track_ang 0.5→0.6` 단독이다. 앞의 parent·control·track 비교는 2026-09-25에 실행되었으므로 현재 미실행 계획으로 읽지 않는다. 각 변경은 독립 sibling이며 하나의 run에 합치지 않는다. 이후 예산이 남으면 `action_rate -0.0005→-0.0025` 짧은 negative-control, `ang_vel_xy -0.05→-0.10` 단독 screen을 고려한다. 이는 **당시 제안**이지 학습 실행 승인이나 새 Experiment 등록이 아니다. 1K는 방향성 screen, 유망하면 3K, 경쟁력 있는 3K만 5K로 늘린다. 같은 parent·추가 iteration·evaluator를 맞추되 training seed만으로 동일 terrain sequence를 보장한다고 쓰지 않는다.

9월 23일 공개 영상 심층 판독은 이 우선순위를 새 reward 효과로 확정하지 않는다. 대신 모든 후보의 paired evaluator에서 생존·진행·추종·보행 품질 네 축을 분리한다. 특히 linear tracking은 XY error와 함께 계단 상승·측면 이탈·정체를, yaw는 교차 보폭·잔여 회전을, action-rate 음성 대조는 smoothness와 실제 전진을 같이 본다. 공개 20초 클립의 낙상 부재·비정상 동작을 해당 run의 전체 수치나 우리 후보의 인과 효과로 바꾸지 않는다. 세부 관찰과 출처 경계는 `20`을 따른다.

아래 2026-09-09의 `-20` 완화/`yaw 0.6` 첫 후보 서술과 300회 재수집 설계는 **당시 계획**으로 보존한다. 새 우선순위를 덮는 현재 실행 순서로 읽지 않는다. 특히 H-012 fresh -100과 OFFICIAL TERM-50은 matched pair가 아니므로 새 control 없이 -100의 효과를 확정하지 않는다.

## 2026-09-09 공식 H-001 R02 5K 이후의 우선순위

공식 서버 TERM-50 5K에서 terrain 5.825, base-contact 28.93%, timeout 71.07%로 안정성·지형 진행은 확인됐다. 반면 endpoint yaw error 0.935는 개인 baseline 5K의 0.652보다 크고 3K 이후 개선이 둔화됐다. TERM-50은 최종 고정값보다 stability anchor로 보는 것이 안전하다.

다음 비교는 보존된 TERM-50 checkpoint에서 한 변수만 바꾼 fine-tuning 분기를 같은 남은 학습량과 evaluator로 맞춘다. 첫 후보는 `termination_penalty -50 → -20` 완화 또는 `track_ang_vel_z_exp 0.5 → 0.6` 미세 강화이며 둘을 동시에 바꾸지 않는다. 생존성, terrain, linear/yaw tracking과 stop-command drift를 함께 통과해야 채택한다.

예선 2라운드 공식 실점(제자리 8.62/10.5, 전진 11.24/14, 좌우 5.73/7, 회전 5.66/7, 요철 8.17/10.5, 경사 8.47/10.5, 밀침 8.48/10.5)은 7항목이 고르다. 공식 점수 공백은 회전보다 전진·요철이 크다. 따라서 공식 점수만 보면 A가 정보가 더 많고, B는 내부 yaw 곡선용 격리 실험으로 남긴다. 채택 기준은 시뮬 총점 56.37 초과와 제자리·요철·경사·밀침 유지이다.

제출 후보는 공식 서버(Ubuntu 24.04.2, RTX 5080)에서만 학습한다. 개인 L40S는 같은 Isaac 핀으로 검증할 수 있지만 GPU·OS·`train.py` 해시가 달라 공식 점수 대체값이 아니다. `--max_iterations 200`은 학습 목표가 아니다.

분석은 1K~2K 전환을 정보 효율이 높은 가설로 제안하지만 최적 전환점은 검증되지 않았다. H1 resume 시 terrain curriculum이 쉬운 단계로 리셋되므로 staged run은 완전한 연속 학습이 아니라 checkpoint fine-tuning으로 취급한다. 같은 중간 checkpoint에서 고정 TERM-50 control과 변경 분기를 만들고 동일한 resume reset·남은 iteration·evaluator 조건으로 비교한다.

아래 300회 paired 설계는 첫 공식 서버 실행의 누락 증거를 복원하기 위한 별도 프로토콜로 유지한다.

## Historical feet=-0.2 PERSONAL branches (2026-09-17–21) and separate H-012 fresh run

This section preserves the **pre-correction Run 01 lineage and its then-current decisions**, not the 2026-09-25 corrected outcomes above. H-004's historical parent-selection decision is retained, but the termination-only comparison with PERSONAL H-001 is withdrawn. H-005~H-008 completed from PERSONAL H-001 model_1499 SHA 68fa0a9f…f0c1, with feet=-0.2. Parent archive checksum matches the child source SHA; this is not the official +0.2 TERM-50 run. At the time H-005~H-011 required corrected-lineage reruns; those separate Run 02/03 results are now recorded at the top of this document and in the registry.

| ID | 실제 부모 | 실제 변경 | 기존 실행 | 판정·다음 조치 |
| --- | --- | --- | ---: | --- |
| H-004 · TERM-20 | fresh; historical H-001 comparison | termination -50→-20 and feet -.2→+.2 relative to PERSONAL H-001 | PERSONAL 1.5K complete | HOLD; termination comparison requires revalidation |
| H-005 · AIRTIME-025 | recorded H-001 `model_1499` | `feet_air_time -0.20 → 0.25` | PERSONAL +1.5K complete | HOLD / 재실험 필요; late terrain 5.422; final 2998 is representative unless final-window joint deterioration; new +0.2 parent and matched control required |
| H-006 · AIRTIME-030 | same recorded parent | `feet_air_time -0.20 → 0.30` | PERSONAL +1.5K complete | HOLD / 재실험 필요; last-300 terrain 5.469 / XY 0.3713, base-contact about 30%; final 2998 default, new +0.2 parent and matched control required |
| H-007 · LINTRACK-100 | same recorded parent | `track_lin_vel_xy_exp 0.5 → 1.0` + `feet_air_time -0.20 → +0.20` | PERSONAL +1.5K complete | HOLD / 재실험 필요; XY last-500 0.3386 but yaw 2.008; final 2998 default. Six-terrain video is qualitative sanity evidence only; new +0.2 parent and matched control required |
| H-008 · LINTRACK-075 | same recorded parent | `track_lin_vel_xy_exp 0.5 → 0.75` + `feet_air_time -0.20 → +0.20` | PERSONAL +1.5K plus unchanged +2K continuation complete (2998→4997) | HOLD / 재실험 필요; 5K continuation exit 0, outer/internal hashes verified, final `model_4997` representative. Validation WARN because generic run omitted execution-time profile/source/lineage; no matched unchanged control or OFFICIAL evidence |
| H-009 · HIPDEV-030 | H-008 3K final `model_2998` (`d9a30c8a…1912ae`) | `joint_deviation_hip -0.20 → -0.30` only | PERSONAL +2K complete (2998→4997), validation PASS | HOLD / 재실험 필요. Last-500 terrain 5.596 / XY 0.3278 / base-contact 29.99%; final `model_4997`. No decisive control gain, fresh H-009 video, or OFFICIAL claim |
| H-010 · AIRTIME-025 | H-008 3K final `model_2998` (`d9a30c8a…1912ae`) | `feet_air_time 0.20 → 0.25` only | PERSONAL +2K complete (2998→4997), validation PASS | HOLD / 재실험 필요. Last-500 terrain 5.663 / XY 0.3318 / base-contact 29.63%; final `model_4997`. Stable but effectively tied with unchanged control; 6-terrain video is qualitative only |
| H-011 · HIPDEV-010 | H-008 3K final `model_2998` (`d9a30c8a…1912ae`) | `joint_deviation_hip -0.20 → -0.10` only | PERSONAL +2K complete (2998→4997), validation PASS | HOLD / 재실험 필요. Last-300 terrain 5.661 / XY 0.3304 / base-contact 29.02% / yaw 1.411; final `model_4997`. Stable but no decisive control-relative gain |
| H-012 · TERM-100 | BASE configuration | `termination_penalty -5 → -100` only | PERSONAL fresh 5K completed; evidence PASS; HOLD | Automatic best/export and six qualitative videos use `model_4700` (SHA `f8732e4f…411f52`); final endpoint is `model_4999`. Strong integrity, but yaw trade-off and unmatched TERM-50 comparison leave no adoption claim |

The historical parent is identified as PERSONAL H-001 with feet=-0.2. Its archive checksum matches the children, resolving the earlier parent-identification uncertainty. A +0.2 resume from that old parent would itself change a reward and is not an unchanged control. The 2026-09-25 corrected runs used a distinct fresh +0.2 parent; neither the official 5K run nor H-004 substituted for it.

H-008's separately selected continuation to global 5K is now complete: it ran 2998~4997 with
unchanged rewards, 21 retained checkpoints, and late console terrain 5.604 / XY 0.3314 /
base-contact 29.67%. It remains PERSONAL evidence with validation WARN because generic execution
left profile/source/lineage null. H-009, H-010, and H-011 do not descend from that continuation:
all three branch directly from the already completed H-008 3K final
`model_2998.pt`, SHA-256 `d9a30c8a117f69cac49c4e640500f0fa8d88de72d6c61855f1e147ea6c1912ae`.
H-009 changes only the more-negative hip penalty, H-010 changes only airtime, and H-011 changes
only the less-negative hip penalty. They are parallel siblings, not a sequential combined delta.
H-009 Run 01 is a PERSONAL +2K completion. Its report-analyzed archive has 2,000 TensorBoard
points, 21 finite checkpoints and validation PASS; final `model_4997` is the representative
because late terrain/tracking/fall do not jointly deteriorate. Automatic `model_best=model_3600`
and existing policy/video are not selectors or fresh H-009 video provenance. Its late aggregate
values are nearly identical to the recorded unchanged H-008 continuation, so the decision is
HOLD rather than PROMOTE. H-010 and H-011 also completed as PERSONAL +2K resumes from the same
3K parent. Both reached global 4997 with validation PASS and use final `model_4997` as the run
representative because the late terrain/tracking/fall metrics do not jointly collapse. H-010's
late aggregate is effectively tied with the unchanged `.20` control; H-011 likewise shows only
small aggregate differences and leaves yaw high. The three completed siblings therefore remain
HOLD and do not establish a winning hip or airtime direction.

H-012 is a separate fresh stability screen from the BASE configuration, not an H-001 or H-008
sibling. The earlier 3K plan was superseded by a PERSONAL fresh 5K run with only
`termination_penalty -5 → -100`. `model_4700` is automatic best and the six-video source, while
`model_4999` is the endpoint. The received deep analysis finds strong evidence integrity and no
numerical divergence, but high late yaw error and no matched PERSONAL TERM-50 control. The decision
is HOLD; this is not an OFFICIAL result.

The automatic-best records are internally consistent with the preserved resume filter. The
finalizer excludes steps before `lo + max(50, floor((hi-lo)×0.10))`; for 2998→4997 this is about
3197. H-009 raw peak 3041, H-010 raw peak 3044, and H-011 raw peak 3084 are ineligible. H-010's
eligible peak 3299 maps to `model_3300`; H-011's 3203 maps to `model_3200`. This explains the
raw-global/report difference but does not turn automatic reward best into a policy selector.

For sufficiently long resume runs, keep the resume strategy but discard automatic `model_best`
as a policy selector. The default representative is the final numbered checkpoint; consider the
previous checkpoint only when the final several hundred iterations jointly and clearly worsen in
terrain, tracking, and falls. Preserve that final through an organizer-approved official
procedure, run one native play/export, and download. Stop the server only when the user separately requests it. This is not a PC tournament, a
multi-checkpoint comparison loop, or a new selector program.

The 2026-09-18 H-007 and H-008 analyses each match six supplied `model_2998` terrain-video
hashes. They provide a visual check of upright terrain locomotion and report no observed
fall/reset in those recorded trajectories, but they do not contain embedded checkpoint identity,
commands, telemetry, repeated trials, or OFFICIAL scoring. Treat them as a final-checkpoint
sanity check, not a causal reward comparison or a reason to restore PC checkpoint selection.

## 최소 유효 설계

첫 실행에는 전체 곡선이 없으므로 다음 두 run을 같은 조건으로 짝지어 수집한다.

| 순서 | ID | 변경 | iterations | 목적 |
| --- | --- | --- | ---: | --- |
| 1 | `H1-B0-RECAPTURE` | baseline 그대로 | 300 | 전체 event·콘솔·GPU 시계열 재수집 |
| 2 | `H1-S1-TERM50` | `termination_penalty -5 → -50`만 | 300 | 초기 낙상 억제 효과 분리 |

새 run을 하나만 할 수 있으면 S1을 실행하고 기존 report endpoint와 제한적으로 비교할 수 있다. 그러나 기존 곡선이 없으므로 효과 크기와 원인 결론은 `잠정 관찰`로 표시한다.

## 고정 조건

- 공식 서버 image, Isaac Sim/Lab, H1 task
- 참가자 수정 허용 파일 외 코드 hash
- seed 42
- 4096 envs, 24 steps/env
- 300 iterations
- PPO·observation·action·terrain 설정
- camera 없는 headless 학습, 영상은 별도 실행
- 동일 CLI와 환경변수

실제 적용값은 명령 문자열이 아니라 `env.yaml`, 콘솔 로그와 hash로 다시 확인한다. 여러 reward를 동시에 바꾸지 않는다.

## S1에서 바꿀 값

| reward | B0 | S1 |
| --- | ---: | ---: |
| `termination_penalty` | -5.0 | -50.0 |
| 나머지 참가자 reward 8개 | baseline | 그대로 |

첫 report의 마지막 fall rate가 100%였고 `-5`는 백업 reward 파일 추천 구간 밖이다. `-50`은 방향성을 확인하는 첫 stability anchor이지 최적값이 아니다.

## 실행 전 필수 기록

- experiment ID와 단일 가설
- 실제 실행 명령과 `train.py --help`
- 코드 commit/diff·SHA-256
- reward 변경 전·후 파일과 한 줄 diff
- GPU·driver·runtime 정보
- headless·camera·viewport·video 조건
- 종료 조건과 확보할 산출물

B0의 reward diff는 없어야 하고 S1 diff는 `termination_penalty` 한 줄만 달라야 한다. `agent_cfg.py`, `env_cfg.py`, `train.py`를 iteration 변경 목적으로 수정하지 않는다.

## 실행 중 확보

- stdout·stderr 전체를 `tee`로 저장
- TensorBoard `events.out.tfevents*`
- `logs/<run>/` 전체와 모든 checkpoint
- GPU utilization·VRAM·power·temperature 시계열
- 시작·종료 시각, exit code, dashboard 사용시간
- NaN·OOM·simulator 오류·반복 경고 시점

## 곡선 비교 창

| 구간 | iterations | 목적 |
| --- | ---: | --- |
| early | 0~49 | 초기 탐색과 즉시 붕괴 |
| middle | 50~149 | 학습 방향 형성 |
| late | 150~299 | 짧은 run의 마지막 상태 |
| last-window | 마지막 50개 | endpoint 노이즈를 줄인 중앙값 |

매 iteration 기록이 아니면 실제 공통 step을 기준으로 같은 비율의 창을 사용하고 누락률을 남긴다.

## 우선 비교 지표

1. fall rate와 termination 빈도
2. episode length의 last-window 중앙값과 분포
3. terrain level 최초 상승 step·late 중앙값·최댓값
4. linear/yaw tracking 유지 여부
5. action std와 action-rate, 정지·진동 여부
6. KL·learning rate·entropy·loss 안정성
7. seconds/iteration·FPS·collection/learning time
8. GPU·VRAM·power — 환경 동일성 확인용

TensorBoard에 실제 존재하는 태그만 분석한다. 없는 태그를 추정으로 채우지 않는다.

## mean reward 함정

`termination_penalty` 계수가 바뀌면 reward 함수의 척도도 달라진다. B0와 S1의 `Train/mean_reward` 절댓값만 보고 높은 쪽을 우수 정책으로 고르지 않는다. 총 reward는 각 run 내부의 진행·발산을 보는 보조 곡선이며, run 간 판단은 낙상·episode·terrain·tracking·영상처럼 행동에 가까운 지표를 우선한다.

## 영상 실패 검사

- 덜 넘어지지만 움직이지 않는 정책
- 제자리 회전 또는 명령 반대 이동
- 한 발 들기, hopping, foot dragging
- 상체 경직이나 큰 진동
- 평지 유지 후 terrain 진입 즉시 붕괴

낙상률만 좋아지고 추종·진행이 무너지면 채택하지 않는다.

## 판정

| 관찰 | 다음 행동 |
| --- | --- |
| fall↓, episode↑, tracking·terrain 유지 | 같은 설정 장시간 confirmation 후보 |
| fall↓, tracking↓ 또는 정지 | `-20` 같은 중간 anchor 검토 |
| 차이 거의 없음 | 300회 학습량·terrain 변동·영향 미약을 분리 |
| fall·진동·KL 악화 | S1 확장 중지, 로그 원인 분석 |
| 설정·처리량 불일치 | reward 결론 보류, 비교환경부터 복구 |

단일 seed 300회 결과를 통계적 개선이나 최적값으로 부르지 않는다.

## 후속 단변수 anchor

| 단계 | reward | 후보 |
| --- | --- | --- |
| Stability 1 | `termination_penalty` | -5, -20, -50, -100 |
| Stability 2 | `flat_orientation_l2` | -0.75, **-1.0**, -1.5, -2.5 |
| Stability 3 | `ang_vel_xy_l2` | -0.03, -0.05, -0.10 |
| Tracking | `track_lin_vel_xy_exp` | 0.5, 0.75, 1.0, 1.5 |
| Turning | `track_ang_vel_z_exp` | 0.5, 1.0, 1.5 |
| Gait | `feet_air_time` | 0.10, 0.20, 0.25, 최대 0.30 |
| Smoothness | `action_rate_l2` | -0.00025, -0.0005, -0.001 |

이 값은 최적값이 아니라 초기 비교점이다. Stability 안전 영역을 정한 뒤 Tracking/Gait를 열고, 단변수 증거 없이 조합 탐색으로 넘어가지 않는다.
