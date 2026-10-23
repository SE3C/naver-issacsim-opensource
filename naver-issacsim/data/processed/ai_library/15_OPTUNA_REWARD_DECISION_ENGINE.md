---
title: "Optuna reward 탐색 의사결정 엔진"
purpose: "AI upload bundle — 공식 학습과 개인 평가를 분리한 저예산 Ask-and-Tell 운영 규칙"
sources:
  - "data/processed/incoming/other/reviewed/GO2_A1_1K_3K_VIDEO_FULL_EVIDENCE_ANALYSIS_20260914.md"
  - 'data/processed/incoming/other/reviewed/GO2_OFFICIAL_BASELINE_1K_AND_ISSACSIMZ_LOGGING_ANALYSIS_20260914.md'
  - "data/processed/planning/historical/04_OPTUNA_REWARD_SEARCH_DESIGN.md"
  - "data/processed/planning/historical/07_H1_SECOND_RUN_PARAMETER_COMPARISON_PLAN.md"
  - "data/processed/experiments/h1/analysis/2026-09-07_BREV_L40S_H1_BASELINE_5K_AND_SCREENING.md"
  - "data/processed/experiments/go2/training/2026-09-13_GO2_G-002_G-003_FAILURE_AND_VALIDATION_STRATEGY_V2.md"
  - "data/processed/incoming/other/reviewed/GO2_A1_1K_DEEP_EVIDENCE_ANALYSIS_20260913.md"
  - "data/processed/incoming/other/reviewed/GO2_G5_OFFICIAL_1K_LIGHTWEIGHT_FAILURE_ANALYSIS_20260914.md"
  - "data/processed/incoming/other/reviewed/GO2_A1_THREE_EXPORTS_DEEP_ANALYSIS_20260914.md"
  - "data/processed/incoming/other/reviewed/GO2_A1_MODEL_4300_DEEP_ANALYSIS_20260915.md"
  - "data/processed/incoming/other/reviewed/GO2_A1_MODEL_4800_DEEP_ANALYSIS_20260915.md"
  - "data/processed/incoming/other/reviewed/GO2_A1_MODEL_4900_DEEP_ANALYSIS_20260915.md"
  - "data/processed/experiments/go2/analysis/2026-09-15_GO2_G-005_FIXED_EVAL_SEED4201_D1.md"
  - "data/processed/experiments/go2/analysis/2026-09-15_GO2_G-005_4800_4900_NATIVE_VIDEO_AND_SELECTION.md"
  - "data/processed/incoming/other/reviewed/A1_4800_vs_4900_DEEP_ANALYSIS_AND_LEARNING_RECORD_20260915.md"
  - "data/processed/experiments/h1/analysis/2026-09-18_H-007_MODEL2998_SINGLE_CHECKPOINT_SUMMARY.md"
  - "data/processed/experiments/h1/analysis/2026-09-18_H-008_MODEL2998_6TERRAIN_VIDEO_ANALYSIS_SUMMARY.md"
  - "data/processed/incoming/other/reviewed/2026-09-18_H007_MODEL_2998_SINGLE_CHECKPOINT_ANALYSIS.md"
  - "data/processed/incoming/other/reviewed/2026-09-18_H008_H1_MODEL2998_6TERRAIN_VIDEO_ANALYSIS.md"
  - "data/processed/experiments/h1/analysis/2026-09-18_H-008_CONT2K_FROM_MODEL2998_ANALYSIS.md"
  - "data/processed/incoming/other/reviewed/H1_H009_HIPDEV030_FROM_H008_3K_DEEP_ANALYSIS_20260920.md"
  - "data/processed/incoming/other/reviewed/H1_H010_AIRTIME025_3K_TO_5K_DEEP_ANALYSIS_REVISED.md"
  - "data/processed/incoming/other/reviewed/H1_H011_HIPDEV010_MODEL4997_DEEP_ANALYSIS.md"
  - "data/processed/incoming/other/reviewed/2026-09-21_OPTUNA_PERSONAL_ASK_TELL_ORGANIZER_APPROVAL.md"
  - "data/processed/incoming/other/reviewed/NCRC_EXTERNAL_FAILURE_EVIDENCE_FOR_DATABASE_20260922.md"
  - "data/processed/incoming/other/reviewed/NCRC_VIDEOS_JSON_DEEP_ANALYSIS_20260922.md"
  - "data/processed/reference/public/2026-09-22_ncrc_public_data_audit/README.md"
  - "data/processed/incoming/other/reviewed/NCRC_H1_EXTERNAL_INTERNAL_SINGLE_DELTA_ANALYSIS_20260923.md"
  - "data/processed/incoming/other/reviewed/자동평가_Tracking_Survival_구조_분석보고서_20260924.md"
  - "data/processed/incoming/other/reviewed/2026-09-26_H1_ORGANIZER_CHECKPOINT_QA_SIRIUS_YEOLMU.md"
  - "data/processed/incoming/other/reviewed/H1_H010_FRESH3K_R01_VS_H005_FRESH3K_R01_DEEP_ANALYSIS_20260927.md"
  - "data/processed/incoming/other/reviewed/GO2_20260929-154342-go2-lintrack-125-fresh7500-official_VS_20260928-230114-go2-lintrack125-fresh3k-r5-official_DEEP_ANALYSIS_20260930.md"
type: "optimization_design"
---

# Optuna reward 탐색 의사결정 엔진

**2026-10-17 목적 정렬:** [판단 프레임](14_H1_NEXT_RUN_PARAMETER_COMPARISON.md)을 먼저 적용한다. H1 계단·박스 영상은 공식 7시나리오와 다른 보조 근거다. 완주 공백 하나를 자동 탈락 gate나 Optuna 벌점으로 만들지 않는다. 내부 순위는 공식 점수 예측이 아니며 config 탐색·독립 학습 seed 확인·고정 config 장기화·reward 전환은 별도 질문이다. 새 trial·Tell·무한 resume·미세 sweep을 이번 문서화만으로 시작하지 않는다.

**2026-10-16 action=-.0003 실제 관측:** [OFFICIAL fresh3K·PERSONAL 평가·보고서](../experiments/h1/analysis/2026-10-16_H1_ACTION0003_MODEL2950_POLICY_REVIEW.md)는 수신 완료/HOLD다. Run `20261016-033023-h1-actrate-0003-fresh3k`, keeper2950(`1cc2c031…0473c4b`), H5 진행9.018/P05 8.664/min6.771m; 3072행 생존과 험지 저속 꼬리가 공존한다. 중간 reward 값이 최적이라는 증거가 아니며 자동 Tell·새 trial·공식 점수로 변환하지 않는다. 기존 model2700/TERM50 저장자료 비교가 제안됐으나 이번 보고서에서는 미실행이다. -.0003 resume는 별도 미실행 계획이다.

**2026-10-16 후속:** [angxy 보고서·5정책 CPU 비교](../experiments/h1/analysis/2026-10-16_H1_ANGXY008_MODEL4650_POLICY_REVIEW.md)도 HOLD이며 새 Tell/점수 관측이 아니다. [연구 기반 계획](../planning/2026-10-16_H1_EVIDENCE_AND_RESEARCH_NEXT_EXPERIMENTS.md)은 당시 action=-.0003 **fresh3K**를 제안했다. 이후 위 실제 Run·보고서를 수신했으나 검증된 최적값·승인 Optuna trial·Tell은 아니다. 평가 seed와 독립 학습 seed를 분리하고 축별 trade-off를 한 합성점수로 숨기지 않는다. 최초 다섯 가설 중 body-rate는 이제 학습/평가/분석 완료, 미실행 resume는 airtime 한 갈래다. 원문 raw null/unverified 유지.

**2026-10-16 참고:** [lin=.55 4정책 CPU 비교](../experiments/h1/analysis/2026-10-16_H1_LIN055_FOUR_POLICY_COHORT_INTAKE.md)는 rough 진행과 H3 vy/H4 yaw의 trade-off를 확인해 HOLD를 유지했다. 이를 단일 objective·공식 점수·새 Optuna Tell로 자동 변환하지 않는다. 당시 action=-.0003 fresh 제안은 위 완료·보고서 HOLD로 갱신됐고 resume만 미실행이다.

## 2026-10-15 Optuna v2 수신 — 최소 개선 반영, Tell/운영 최적화는 미준비

[개선본·검증·한계](../operations/2026-10-15_OPTUNA_PC_ASK_TELL_V2_INTAKE.md): PC Ask/Record/Tell v2.0.0을 수신·보존하고 핵심 코드를 정적으로 대조했다. stage별 sampler 재사용, 재시작 시 trial-count 기반 seed, 명시 Ask/Record/Tell/Abandon, frozen config·수동 identity·단일 objective 검증, loopback 강제와 자동 evaluator 경로 분리가 반영됐다. RNG state 복원·무중단과 동일한 후보열·실제 checkpoint 바이트/입력 진실성 검증은 아니다. 기존 진단 HTML은 비운영 참고용이다.

외주 로그는 CPU sandbox Python **12개 회귀 테스트**·구문/UI 정적 검사 exit0를 기록하지만 이번 수납에서 앱·테스트를 재실행하거나 설치하지 않았다. 기본 config의 **objective=null / comparison=null → Tell 차단**. 후보 Ask·수동 진단 기록은 구현됐으나 실제 범위·목적함수·동일 비교 조건 미승인으로 **운영 최적화 준비 미완료**, Windows 실기·실제 평가 ZIP adapter·metric mapping·실제 trial 수납도 미완료다. legacy 9차원 범위는 새 학습 권고가 아니고 action=-.0001이 범위 밖이라는 제한을 유지한다. HOLD/REJECT·합성 fixture를 임의 숫자 관측으로 바꾸지 않는다. 기존 Windows 평가기·공식 서버는 변경하지 않았다. [이전 원본 검토와 개선 요청](../operations/2026-10-15_OPTUNA_EXTERNAL_CPU_REVIEW_INTAKE.md)은 후속 전 역사다.

> 날짜별 업데이트는 해당 시점의 기록이다. 최신 Run·제출 상태는 [현재 Experiment registry](../../../research/EXPERIMENTS.md)를 우선한다.

## 2026-10-11 ACTRATE-0001 fresh10K 분석 수납 — HOLD

[model_9999 정책 검토](../experiments/h1/analysis/2026-10-11_ACTRATE0001_MODEL9999_POLICY_REVIEW.md): 공식 fresh10K 학습은 완료/PASS, 최종 model_9999의 별도 PERSONAL 6영상/full 평가 보고서는 생존 100%에도 rough 하위 꼬리·계단 완주 검증 공백으로 HOLD다. 완료는 채택이나 공식 제출을 뜻하지 않는다. 기존 planned 다섯 가설의 상태·Optuna trial 수를 이 Run만으로 변경하지 않으며 다음 작업은 보존된 TERM-50/model2800 대응 raw 비교다.


과거 `feet_air_time=-0.2` 부모에서 나온 H-005~H-011 수치를 검증된 단일변수 효과나 최종 채택 근거로 Optuna에 입력하지 않는다. 새 corrected-lineage 결과는 evidence 확인 후 별개로 판단한다. [계보 상세](14_H1_NEXT_RUN_PARAMETER_COMPARISON.md).

새 Experiment 이름은 [명명 규칙](../../../research/EXPERIMENT_NAMING.md)을 따른다. `H/G/HS/GS`와 `Rxx`는 과거 자료 검색용이며 새 번호를 발급하지 않는다. 기존 고정 설정 resume을 reward schedule 성과로 입력하지 않는다. Legacy HS-001/002에 대응하는 두 질문과 같은 부모의 unchanged control은 **미실행 PERSONAL 계획 질문**이며 현재 실행 예약·우선순위가 아니다. 따라서 Optuna의 완료 trial이나 공식 서버 결과가 아니다. 실제 config와 parent lineage는 [registry](../../../research/EXPERIMENTS.md) 및 evidence에서 확인한다.



## 2026-10-11 ACTRATE-001 / model_2850 — 관찰은 추가됐으나 Optuna completed trial 아님

[2026-10-10 원문 분석](../incoming/other/reviewed/H1_MODEL2850_SHA1E6D_POLICY_ANALYSIS_20261010.md) · [2026-10-11 정책 검토](../experiments/h1/analysis/2026-10-11_ACTRATE001_MODEL2850_POLICY_REVIEW.md) · [Experiment](../../../research/experiments/h1/exp-h1-action-rate-smoothing.md). OFFICIAL fresh3K `ACTRATE-001` Run `20261010-125324-h1-actrate-001-fresh3k` best `model_2850` SHA `1e6d…bb1`의 후속 Windows PERSONAL 단일 정책 `scenario7` 분석을 수신했다. **3,072/3,072 timeout 생존**에도 H1 정지 world XY 평균 **1.151m**, H3 횡왕복 **2.177m**, H5 rough P05 body 진행 **8.921m**이므로 정책 행동은 **HOLD**다. H2/H7 전진과 H6 경사 진행이 가능하다는 점은 부정하지 않는다. 동일 `model_2850` 이름의 ORIENT-100 SHA는 다르며 `source_run_id=null`은 원형 유지한다.

`action_rate_l2=-0.001` 강화의 reward 인과 효과는 해당 Run과 unchanged `h1-submit-2 / TERM-50`의 source/PPO/seed/command/terrain/horizon parity 확인과 raw 비교 전에는 식별되지 않는다. **Optuna objective 점수·study.tell() 완료 trial·공식 점수로 추가하지 않는다.** 자동 GPU 재평가/학습 없이 기존 raw를 먼저 확인한다.


### 2026-10-10 five selected H1 ACTRATE-0001 hypotheses: 현재 한 완료/HOLD·네 계획, not Optuna trials

**2026-10-11 갱신:** lin=0.65 resume Run `20261010-154926-h1-actrate0001-lintrack065-from2700-plus2k`는 OFFICIAL completed/PASS이고 model4650 PERSONAL full 평가·보고서 수납 완료/**HOLD**. 나머지 네 계획은 미실행이다. 아래 “Planning created no training”은 최초 계획 작성 행위만 뜻한다. 실제 학습·평가 완료를 Optuna trial/`study.tell()` 또는 공식점수로 바꾸지 않는다. H3 잔류 world XY2.398m, H4 yaw .179rad/s, rough P05 진행9.228m 및 중앙 계단 미확인을 함께 본다. [판정·계보](../experiments/h1/analysis/2026-10-11_ACTRATE0001_LINTRACK065_MODEL4650_POLICY_REVIEW.md).

[Five planned questions](../planning/2026-10-10_H1_ACTRATE0001_FIVE_COMBINATION_HYPOTHESES.md): **Fresh 2** (action=-0.0001 plus feet=0.25 or feet_slide=-0.35 from the start), **independent one-step Resume 3** (from the same ACTRATE-0001 OFFICIAL 3K checkpoint, +2K with feet=0.25, lin=0.65 or angxy=-0.08). Planning created **no training, evaluator, Optuna trial, or tell observation**. Resume can be performed on several separate sibling Runs, with at most one parent→child resume step per branch and no 5K→7K extension. Fresh combination changes two baseline rewards; causal term attribution is not warranted. Each Resume requires same-parent unchanged +2K control plus source/evaluator parity for causal reward inference. Fresh 3K and Resume total ~5K with identical final rewards are not comparable as schedule-only effects. No invented descriptor for `feet_slide`.


## 2026-10-07 ORIENT-100을 Optuna observation으로 읽는 경계

`exp-h1-rough-terrain-orientation-relaxation / ORIENT-100`은 OFFICIAL fresh 3K 학습 evidence COMPLETE/PASS이고, 뒤이은 `model_2850.pt`의 **Windows PERSONAL 단일 정책 full 평가**(8 case × 3 seed × 128 env, 3,072 episode)를 확보했다. 3,072회 timeout 생존, 정지 H1 +1.633m·lateral H3 +1.180m의 비의도 body 전진, rough H5 평균 tracking **0.1709**와 최소 진행 **7.831m**를 관찰했다. [원문](../incoming/other/reviewed/H1_ORIENT-100_POLICY_ANALYSIS_20261007.md).

이 **2026-10-07 단일정책 보고서를 작성할 당시**에는 `h1-submit-2 / TERM-50` 동일 평가 대조군을 함께 분석하지 못했지만, **2026-10-10에는 기존 3개 ZIP을 직접 받아 raw 9,216 episode 대응-index 비교까지 완료했다**. 다만 독립 Run 반복·초기 지형 재현·train source/PPO parity 등 인과 조건이 아직 미충족이다. 별도로 `source_run_id=null`인 ZIP 내부 기록은 별도 checkpoint SHA·공식 intake로 연결한다. 따라서 **ORIENT-100 자체 효과에 대한 comparable objective, official score, completed Optuna trial을 생성하지 않는다.** 생존률만 objective로 쓰면 정지/rough 실패 양상을 놓친다. 원본 보존 자료만으로 가능한 matched comparison부터 시도하고, 새 평가·학습은 별도 승인이다. `ACTRATE-001`은 다른 Experiment의 독립 OFFICIAL fresh3K 완료/PASS·PERSONAL model2850 분석 수납/HOLD 기록이다.



## 2026-09-30 evaluator 구현 상태

**2026-09-30 당시** H1/Go2 공용 fixed evaluator/paired harness는 없었다. 이후 [21](21_WINDOWS_GO2_VIDEO_AND_EVALUATION.md)의 Windows PERSONAL Go2 수집기가 2950·7050 full 평가를 완료했고, 2026-10-04 받은 보고서는 raw 진단 비교를 수행했다. 2026-10-06에는 같은 공용 core를 재사용하는 H1 통합 launcher를 `C:\NCRC\h1_6terrain_video.bat`에 설치해 CPU 회귀 테스트 60개와 PowerShell/설치 검증을 통과했으며, H1은 ±10° 6영상 뒤 camera-off `scenario7` 8 case 전체 평가를 사용한다. standalone/integrated smoke 옵션은 제거됐고 **2026-10-07 H1 `model_2850` 단일 정책 PERSONAL Windows GPU full이 완료됐으나, 2026-10-10 H1 기존 3개 ZIP의 대응-key raw 분석은 수행됐으나, Windows 비교 CLI와 동일 물리 초기상태 통제 실험은 없다.** 자동 comparison-CLI·calibration·점수 계산은 실행하지 않았다. 공식 채점 함수나 미공개 조건의 재현도 아니며 H1 multi-policy paired 검증·자동 Optuna study readiness까지 입증하지 않는다. 아래 objective는 readiness 검토 뒤의 계획이다. AI의 정성 판단을 가짜 수치 objective로 넣지 않는다.

## 적용 위치

Optuna는 공식 GPU 서버에 설치해 학습을 자동 반복하는 도구가 아니다. 이번 운영진 확인의 허용 범위에서는 **개인 PC**에서 이전 실험을 기록하고 다음 reward 후보를 추천하는 Ask-and-Tell 계층으로만 사용한다. 개인 NVIDIA 서버에 대한 별도 운용 판단을 이 답변으로 넓게 추론하지 않는다.

### 2026-09-21 운영진 확인

운영진은 개인 PC에서 이전 공식 학습 결과를 바탕으로 다음 reward 후보를 계산하는 Optuna Ask-and-Tell 사용이 예선 규정상 허용된다고 답변했다. 단, 이 허용은 다음 세 경계를 모두 지킬 때만 적용된다.

1. Optuna를 제공 서버에 설치하거나 제공 서버와 연동하지 않는다.
2. reward 파일 수정과 학습 실행은 참가자가 직접 수행한다.
3. 제출 정책은 운영진 제공 서버에서 학습해 생성한다.

따라서 Optuna study는 개인 PC의 후보 추천·분석 기록일 뿐이며, 공식 서버의 자동화 agent, remote controller, reward 편집기, 학습 scheduler가 아니다. 원문 답변은 `data/processed/incoming/other/reviewed/2026-09-21_OPTUNA_PERSONAL_ASK_TELL_ORGANIZER_APPROVAL.md`에 보존한다.

```text
개인 환경 study.ask()
→ reward 후보를 공식 서버에 수동 반영
→ 공식 train.py로 policy 생성
→ 원본 run 전체 export
→ 개인 evaluator에서 multi-seed 평가
→ Robust Proxy Score 계산
→ study.tell()
```

위 흐름은 승인된 사용 경계 안에서의 개념 설계이며, 현재 v2의 운영 절차 확정이나 Tell 사용 준비 완료를 뜻하지 않는다. objective/comparison 계약 승인 전에는 Tell을 실행하지 않는다.

공식 제출 정책은 제공 서버에서 학습하고, 공식 서버에는 외부 에이전트·Optuna·임의 패키지를 설치하지 않는다.

2026-09-26 [제공된 운영진 공개 답변 정리본](../incoming/other/reviewed/01_운영진_자동평가_Tracking_Survival_공개답변_20260926.md)은 step별 몸통 기준 `vx`/`vy`/yaw-rate 오차의 **비정규화 Euclidean 크기 → episode 내부 평균 → episode별 동일 가중 평균** 순서와 **episode 단위 Survival 비율**을 설명한다. 출발·10초 명령 전환·낙상 전 구간도 포함되고, 반복 낙상은 실패 episode를 반복 생성한다. 따라서 개인 proxy objective는 지속 3축 오차·transition 응답·낙상·짧은 episode를 함께 보되, 여전히 공개되지 않은 **최종 평균오차→Tracking Score 변환식과 시나리오별 구체적 command 값**을 임의로 채워 공식 점수와 동등하다고 주장하지 않는다. 같은 seed도 정책별 reset 이후 명령의 완전한 일치를 보장하지 않는다. 이 전사본은 원본 게시 화면·비공개 evaluator 코드를 독립 검증한 결과가 아니다. [해석과 평가 설계](10_SOLUTION_AND_VALIDATION_BLUEPRINTS.md).

## Registry와 study의 역할 분리

Experiment 질문·현재 판단·legacy 계보의 source of truth는
[`research/EXPERIMENTS.md`](../../../research/EXPERIMENTS.md)이며 새 이름은 [명명 규칙](../../../research/EXPERIMENT_NAMING.md)을 따른다. Optuna study는 registry를
대체하지 않고 조건이 맞는 완료 Run의 의사결정 보조 도구일 뿐이다. reward 값은 Experiment 주소에 넣지 않고 기준 preset 대비 최종 override와 부모 checkpoint lineage를 별도로 기록한다.

`PERSONAL` Run은 screening·실패 탐색·다음 가설 선택에 사용할 수 있지만 official score 또는
sampler의 comparable official-performance observation으로 넣지 않는다. `OFFICIAL` evidence가
식별 가능하고 iteration·evaluator·scenario·seed 정책이 같은 Run만 보고서 성능 근거 및 비교
가능한 study 후보가 된다. 1K·3K·5K는 새 ID가 아니라 한 가설의 staged Run이며, 1K screen을
완료 trial처럼 섞지 않는 기존 규칙을 그대로 적용한다.

## 2026-09-22 공개 researchlog 관찰의 제한된 사용

공개 `videos.json` 스냅샷에는 영상 84개(실패 47·성공 34·대회 3)가 있고, 실패 45개에는
reward dial·지표가 있으나 성공·대회 객체의 `detail`은 비어 있다. 따라서 이 자료는 성공
reward 범위나 공식 채점식을 학습시키는 데이터가 아니다. 원문 분석과 raw bundle은
`data/processed/reference/public/2026-09-22_ncrc_public_data_audit/`에 보존한다.

외부 사례에서 반복되는 변경 항목·극단값·terrain collapse 패턴은 다음 **단일변수 가설의
prior**나 anomaly rule 후보가 될 수 있다. 하지만 parent, seed, evaluator, 환경, source,
training length가 통제되지 않았으므로 외부 row는 `study.tell()`·objective·pruner 학습값·공식
성능 비교에 넣지 않는다. 다중 변경 run에서 특정 reward의 효과를 단정하지 않고, 우리
동일 조건 Run으로 재검증한 뒤에만 registry와 study 후보를 갱신한다.

2026-09-23 교차 분석에서 H1 실패 38건 중 단일 reward 변경은 5건뿐이다. `track_lin 1.0`
단독 초기 붕괴, `yaw 1.0` 단독 초기 붕괴, `action_rate -0.0025` 단독 장기 붕괴는
**금지값 목록이나 sampler의 실패 trial이 아니라 반증할 질문**이다. 공개 실패 표본의
고terrain/고reward와 낙상 공존, 저낙상/저진행 공존은 내부 objective의 guardrail 후보를
제시한다: 생존만이 아니라 고정 시나리오의 실제 진행·XY/yaw 추종·낙상·안정성을 함께 본다.
성공 34건의 detail이 비어 있고 fall 집계 window도 섞여 있어 공개 기록만으로
parameter bound·prior probability·가중치·성공 확률을 수치 학습시키지 않는다. 개인 PC에서
수동 후보 선택의 근거 key로만 남긴다. 다음 controlled 비교의 우선순위와 legacy H-005~012
계보 경계는 `20_H1_PUBLIC_FAILURES_AND_EXPERIMENT_PRIORS.md`를 따른다.

## 아직 시작하면 안 되는 조건

다음을 모두 통과하기 전에는 Optuna 대신 baseline과 수동 sweep을 사용한다.

1. 공식 `policy.pt`가 개인 환경에서 observation/action shape 오류 없이 로드됨
2. 같은 policy·seed의 metric과 영상이 재현됨
3. 낙상·정지·명령 추종 방향이 자동 metric과 일치함
4. 명백한 실패 정책이 낮은 score를 받음
5. scenario·seed·normalization·objective version이 고정됨
6. 같은 학습 iterations로 비교 가능한 completed trial이 충분함

첫 H1 300회 policy는 미수렴이고 evaluator score가 없으므로 Optuna trial로 backfill하지 않는다.

2026-09-07 개인 H1 자료도 아직 Optuna 시작 조건을 충족하지 않는다. baseline은 5K지만 당시 legacy `TERM50`·`YAW075`·`RECOVERY`는 1K라 학습량이 다르고, 공통 evaluator·복수 seed가 없으며 legacy `TERM50` 영상도 baseline 1K 영상과 잘못 연결됐다. 당시 `TERM50`은 수동 장기 confirmation 후보로만 기록하고, YAW075와 RECOVERY를 sampler 학습용 completed trial로 넣지 않는다.

## study 분리 기준

다음 중 하나라도 다르면 같은 study에 섞지 않는다.

- robot
- 탐색 reward 집합과 단계
- 공식 학습 iterations
- evaluator·observation 구현
- scenario·weight·seed set
- objective·normalization version

1,000회와 5,000회 결과를 섞으면 sampler가 reward 효과와 학습량 효과를 구분하지 못한다.

Go2의 `0~200` iteration은 NaN/Inf, value loss/action std 붕괴, 실행 오류, reward 적용 오류만 찾는 sanity check다. `1K`는 positive 후보의 최종 채택 근거가 아닌 가벼운 1차 screening으로, 같은 조건 baseline 대비 terrain 억제 여부, base-contact, timeout/episode length, XY 또는 yaw tracking, 특히 `500→1000` 회복 추세를 함께 본다. 1K에서 2~3개 지표의 개선 가능성이 있으면 동일 baseline과 `3K`로 연장한다. 전반적 악화와 회복 추세 부재일 때 중단 후보로 두며, 사전에 정의한 중단 조건이나 수치·영상이 함께 드러내는 명백한 붕괴/local optimum은 1K에서도 `REJECT`할 수 있다. 3K에서 경쟁력 있는 후보만 동일 5K 길이와 evaluator version으로 다시 측정한 뒤 비교 가능한 trial로 승격한다. 초기 screening 결과는 동일 study의 objective 표본으로 섞지 않는다.

공식 legacy `G-004 ANG-STAB` 1K(아주 오래된 alias G5)는 strong-negative 예외다. 보존·검증된 공식 run의 report에서 terrain `0.00`, XY error `1.7363`,
timeout `97.71%`이고 영상은 옆으로 눕거나 뒤집힌 자세의 생존을 반복했다. evidence pipeline이
PASS하고 episode가 길어도 locomotion objective에는 실패했으므로 3K로 연장하거나 좋은 completed
trial로 넣지 않는다. 이 판단은 공식 서버에서 실행됐다는 provenance를 인정하되, official이라는
표시 자체를 성능 우수성으로 오해하지 않는 사례다.

Go2 `g2-submit-3 / LINTRACK-150-LINZ-2` 계보(legacy G-005, 초기 alias A1)는 이 staged 규칙의 긍정 사례다. `track_lin_vel_xy_exp=1.5`와 `lin_vel_z_l2=-2.0` 조합은 개인 1K·fresh 3K에서 회복했고 공식 fresh 시도도 iter 4800 terrain `5.7367`, XY `0.5017`까지 도달했다. fresh run은 4837 부근에서 중단돼 completed trial이 아니지만, 원본 4800에서 이어진 공식 recovery는 console 4999까지 완료하고 evidence PASS를 남겼다. 따라서 이 조합 계보는 공식 후보로 확인하되 **uninterrupted official 5K 표본**으로는 넣지 않는다. 두 변수가 동시에 바뀌었으므로 sampler의 개별 reward 효과 표본이나 공식 evaluator 점수로도 읽지 않는다. baseline / `LINTRACK-125` 같은 track-only / lin-vel-z-only / 조합 ablation은 별도 목적의 비교다.

### 2026-10-10 ANGTRACK-065/TERM-50 RAW 대응 비교 추가 완료 — trial 인과 판정 불가

[직접 재집계 결과](../experiments/h1/analysis/2026-10-10_H1_ANGTRACK065_TERM50_DEEP_RAW_COMPARISON.md). 보존된 ZIP 두 개의 동일 평가 protocol과 3,072 처음 시도 cohort 인덱스를 매칭했다(ANG 15 종료·15 재시작은 분리). H4 yaw error는 TERM `0.11934`에서 ANG `0.07704`로 좋아졌지만 H3 `vy_error`는 `0.06848→0.18601`, stall은 `0.00912→0.34339`로 악화되고 접촉 종료 `0/384→15/384`. H5 평균 진행은 실질적 차이가 없다. 복합 tracking 개선만으로 안전/횡이동 품질 성공이나 reward causal effect를 판정하지 않는다. 동일 인덱스는 물리 초기 상태 일치가 아니며, 독립 train seed·PPO/source 완전 parity·공식 score는 미검증. `study.tell()`, Optuna trial 등록, 신규 학습·평가 모두 미실행; 정책 HOLD.

### 2026-10-10 ANGTRACK-065 후속 PERSONAL 분석 수신 — Optuna/score 승격 금지

[원문](../incoming/other/reviewed/H1_ANGTRACK-065_POLICY_ANALYSIS_20261010.md) · [근거 요약](../experiments/h1/analysis/2026-10-10_ANGTRACK065_MODEL2950_POLICY_REVIEW.md). `track_ang_vel_z_exp=0.65` OFFICIAL fresh3K의 `model_2950` Windows PERSONAL 6영상+`scenario7` **단일 정책 분석 수신**. 3,072 최초 cohort와 달리 3,087 episode행이 존재하며 H3 순수 lateral에서 **15/384 initial-cohort base-contact 종료**, 그 뒤 15개 짧은 재시작이 포함된다. H3 `399`행 생존율 **96.24%**는 원본 20초 완주율이 아니며 원본 timeout은 **369/384=96.09%**다. H3 stall **0.3532**, vy error **0.1871m/s**, H1 비의도 전진 **0.875m**로 전방위 대표 HOLD. H4 yaw abs error **0.0770rad/s**와 H2/H5/H6/H7 이동 능력은 기록하되 이는 **동일 변경 없는 TERM-50 대비 인과적 yaw 개선**이 아니다.

기존 TERM/ORIENT/ACTRATE 9,216행 matched-index 데이터에는 ANGTRACK의 평가 row가 없으므로 Optuna 결과를 합치지 않는다. **ANGTRACK와 기준선의 실제 `episodes.jsonl` 대응 분석을 별도로 수행하기 전에는** completed trial, comparable objective, `study.tell()`, 보상 우열 또는 OFFICIAL score를 생성하지 않는다. GPU 재평가/학습 없이 기존 증거 보존·행동 HOLD 유지.

### 2026-10-10 H1 기존 ZIP raw 9,216 episode 수납·재계산 결과 — 자동 tell 금지

[3정책 원본 직접 비교](../experiments/h1/analysis/2026-10-10_H1_SCENARIO7_RAW_3POLICY_MATCHED_ANALYSIS.md) · [case summary JSON](../experiments/h1/2026-10-10_H1_SCENARIO7_RAW_SUMMARY.json) · [paired cohort deltas JSON](../experiments/h1/2026-10-10_H1_SCENARIO7_PAIRED_DELTAS.json): `TERM-50/model_2800`, `ORIENT-100/model_2850`, `ACTRATE-0001/model_2700`의 camera-off `scenario7` 원본 3개 ZIP/9,216 raw 행을 실제 열고 ZIP SHA/CRC 및 evaluator resolved config **바이트 동일**·코호트 ID 전부 대응을 확인했다. TERM-50 case별 수치 미확인은 **해결됨**: tracking `0.15712`, H1 비의도 body 전진 `1.352m`, rough H5 mean/min `8.896/2.639m`. ORIENT composite tracking `0.14041`이나 전체 roll/pitch RMS `0.08015`로 TERM `0.03381`보다 크고, ACTRATE tracking `0.14534`·H5 rough 평균 `9.948m`이나 정지 전진 `1.987m`·action 비용이 크다.

이는 **같은 평가 프로토콜에서 받은 정책별 관찰값**이지 동일 정책 선택 시점·다수 train seed·완전 동일 terrain 초기조건/훈련 PPO source의 통제 반복 실험이 아니다. Optuna trial/objective로 무턱대고 환산하지 않으며 `study.tell()` **미실행**, reward 인과 개선 판정 **HOLD**. 새 GPU 학습·평가 없음.

### 2026-10-10 GitHub 기준 H1 TERM-50 / ORIENT-100 / ACTRATE-0001 비교 가능 범위

[세 평가 ZIP 위치, 체크포인트, protocol·관찰표 및 미검증 항목](../experiments/h1/analysis/2026-10-10_H1_SCENARIO7_CROSS_POLICY_REPORT_LEVEL_COMPARISON.md). 보존된 TERM-50 `model_2800`의 `scenario7` full 평가가 GitHub에 **실제로 존재함**을 manifest와 Release에서 확인했다. ORIENT `model_2850`, ACTRATE `model_2700`과 evaluator task/handoff/protocol/seeds/env/horizon가 기록상 같다. 하지만 ZIP은 private Release 바이너리/LFS pointer이고 이번 접근에서는 세 raw `episodes.jsonl`을 **추출/조인하지 못했다**. 기존 ORIENT·ACTRATE 분석 보고서의 평균만으로 어떤 단일 reward를 최적화된 `study.tell()`이나 공정한 `Objective`로 추가해서는 안 된다.

요약 관찰: ORIENT는 8 case 중 5개 tracking과 8/8 action-change RMS가 유리하지만 ACTRATE는 H2/H6 tracking·H5 mean/P05 진행이 유리하다. 두 정책 모두 정지 H1에 비의도 전진(`1.633m / 1.987m`)이 있다. `LINTRACK-075 corrected5K`는 PERSONAL 계보라 reward 단변수 인과 분석에서 별도 컨텍스트다. TERM-50 raw baseline 값을 먼저 추출하고 source/agent/terrain/command parity를 확인해 cohort별 대응 비교를 마친 뒤에만 Optuna objective/비교판정 입력 후보를 검토한다. **현재 Optuna completed trial 증가 없음; 정책 HOLD**.

### 2026-10-10 ACTRATE-0001 model_2700 행동 분석 접수 — Optuna 목적함수로 자동 승격 금지

[원문](../incoming/other/reviewed/H1_MODEL2700_POLICY_ANALYSIS_20261010.md) · [판정](../experiments/h1/analysis/2026-10-10_ACTRATE0001_MODEL2700_POLICY_REVIEW.md). 동일 checkpoint의 Windows PERSONAL `scenario7` 3,072/3,072 episode 생존과 H2 15.326m/H7 10.542m의 실제 진행이 보고됐지만 **H1 정지 전진 1.987m, H3 횡이동 비의도 전진 1.677m**, rough H5 하위 꼬리(전진 8.815m/tracking 0.2908), 경사 action 변동·계단 통과 검증 공백으로 **전천후 후보 HOLD**다. 이것은 단일 checkpoint 행동 분석 완료이지 비교 개선율·reward의 인과 효과·OFFICIAL score 또는 완료된 Optuna trial이 아니다. zero command의 stall=0은 유효 denominator가 없으므로 objective에 정지 성공으로 넣지 않는다. 먼저 이미 보존된 `TERM-50 model_2800` 동일 evaluator raw와 조건 맞춘 cohort 비교를 하되, `study.tell()` 생성이나 새로운 GPU 평가를 승인하지 않는다.

### 2026-10-10 H1 신규 tracking Run 2건 COMPLETE/PASS — completed Optuna observation 아님

신규 [`ACTRATE-0001 / exp-h1-action-rate-relaxation`](../../../research/experiments/h1/exp-h1-action-rate-relaxation.md)(`action_rate_l2=-0.0001`)은 OFFICIAL fresh3K Run `20261009-142350-h1-actrate-0001-fresh3k` **COMPLETED/PASS**이고, auto-best `model_2700`의 후속 Windows PERSONAL 6영상+전체 `scenario7` 평가도 3,072 episode **COMPLETE**다. [`ANGTRACK-065 / exp-h1-angular-tracking-boost`](../../../research/experiments/h1/exp-h1-angular-tracking-boost.md)(`track_ang_vel_z_exp=0.65`)도 별도 OFFICIAL fresh3K Run `20261009-155344-h1-angtrack-065-fresh3k` **COMPLETED/PASS**이나 PERSONAL full 고정평가와 단일 정책 행동 분석이 수신됐으며(H3 최초 cohort 15/384 접촉 종료; 정책 HOLD), TERM-50 raw 대조·인과 검증은 아직 미완료다. **ACTRATE-001=-0.001 Run `20261010-125324-h1-actrate-001-fresh3k`도 OFFICIAL fresh3K COMPLETE/PASS·PERSONAL model2850 분석 수납/HOLD**이다. 두 완료 학습의 원본 evidence와 checkpoint SHA가 있다고 해서 비교·reward 효과 분석이나 official score가 생기는 것은 아니다. 연구 설계용 Optuna에도 **completed trial, comparable objective, `study.tell()`을 자동 생성하지 않는다**. OFFICIAL unchanged fresh3K `h1-submit-2` control `20261008-062732-h1-term-50-fresh3k-control`와 PERSONAL model_2800 full 자료를 사용해 실제 학습량·source/PPO/seed·command/terrain/evaluator parity 확인 후 x/y/yaw tracking·진행/stall·fall을 matched 비교해야 한다. Go2 R3/R5 공식 생존/추종 상쇄는 H1의 연구 동기이지 H1 보상 인과·공식 scoring 변환식이 아니다.

## Go2 비교에서 추가할 구분

[2026-10-08 R3/R5 분석 방향 논의](../experiments/go2/analysis/2026-10-08_GO2_LOCAL_OFFICIAL_EVALUATION_GAP_AND_ANALYSIS_POLICY.md)에 따라 **로컬 합산 점수 상승만으로 공식 성능 개선·reward 채택을 판정하지 않는다.** 다음 reward 값을 먼저 정하지 말고 기존 자료의 목표별·seed별 tracking/진행/stall/종료/자세 trade-off를 확인한다. 한 쌍의 공식 결과에 맞춘 objective·scorer 가중치 보정이나 새 Optuna trial 생성은 하지 않는다. 기존 reward-effect HOLD와 과거 PERSONAL 후보 판정의 제한된 범위를 유지한다.

[운영진 DM 후속 확인](../experiments/go2/analysis/2026-10-08_GO2_R3_R5_OFFICIAL_SCORE_COMPONENTS_ORGANIZER_REPLY.md): R3→R5 공식 계단 survival **99.0%→99.8%**가 좋아졌지만 tracking **0.819→0.796**의 손실이 커 점수는 하락했다. 학습 contact 감소만 최적화 목표로 쓰지 않고, 생존 이득을 유지하는 조건에서 명령 추종 손실을 조사한다. 이는 공식 점수 구성 관찰이며 어떤 reward 변경이 원인인지 밝힌 matched trial은 아니다. 답변 하나로 proxy의 보정 계수·Optuna objective·다음 reward를 정하지 않는다.

### LINTRACK-125 3K↔7.5K: reward trial과 training-budget 비교를 분리

[2026-09-30 OFFICIAL 비교](../incoming/other/reviewed/GO2_20260929-154342-go2-lintrack-125-fresh7500-official_VS_20260928-230114-go2-lintrack125-fresh3k-r5-official_DEEP_ANALYSIS_20260930.md)에서 `LINTRACK-125` fresh 3K와 별도 fresh 7.5K는 동일 reward/source/PPO/env/seed 42/4096 env이고, 7.5K의 처음 3K substantive scalar 22개와 공통 checkpoint 60개가 exact match한다. 따라서 이 쌍은 **동일한 reward 후보를 더 오래 학습했을 때의 budget/trajectory 효과**를 읽는 데는 강하지만, `track_lin_vel_xy_exp 1.0→1.25`의 reward 효과를 추정하는 독립 trial 두 개가 아니다.

Optuna/수동 sampler에 넣을 때 3K와 7.5K를 서로 다른 reward completed trial로 두어 표본 수를 늘리지 않는다. 같은 parameter point의 서로 다른 budget 관찰로 분리하고, objective 비교는 동일 budget·동일 evaluator version끼리만 한다. 7.5K late-500의 terrain/XY/base-contact proxy 개선은 **학습량 증가 신호**이며 BASE `1.0` 대비 causal reward gain이 아니다. reward 효과 질문에는 same-length BASE fresh control이 필요하다.

이후 [2026-10-05 3정책 행동 비교](../incoming/other/reviewed/GO2_C4800_C7050_C7450_POLICY_COMPARISON_20261005.md)는 동일 PERSONAL `scenario7` protocol에서 `g2-submit-3` original 4800, 7.5K automatic-best `model_7050`, terminal `model_7450`을 비교했다. **7450은 현재 내부 행동 주후보 PROMOTE, 7050은 안전성 fallback HOLD, 4800은 현재 all-around 후보 기준 REJECT**다. 7450은 7050보다 tracking/진행이 대부분 case에서 좋아졌지만 stair-up 종료 2→4회와 더 큰 action/body RMS 비용이 있다. 이 결과를 Optuna의 새 completed trial로 넣지 않는다: 7050과 7450은 **같은 7.5K training Run·같은 reward point의 서로 다른 checkpoint**이고, 4800은 다른 preset/lineage라 이 3자 정책 순위를 reward 단일변수 인과 관찰로 바꿀 수 없다. `LINTRACK-125` reward `1.25` 효과는 same-length BASE control 부재로 계속 **HOLD**다. raw 비교와 comparison-CLI score/calibration은 구분하며 이번 보고서에도 후자를 생성하지 않았다. 이후 terminal 7450은 `g2-submit-5 / LINTRACK-125`로 2026-10-06 actual Round-5 제출됐다고 사용자가 확인했고 submission Release의 policy/env/report identity도 보존됐다. 이 제출 사실은 checkpoint 선택 상태를 갱신할 뿐 PERSONAL 비교를 새 Optuna trial, reward 인과 관찰, 공식 점수로 바꾸지 않는다. 2026-10-08 사용자 전달 공식 평가에서 제출 시각 2026-10-06 01:10(시간대 미기재), 종합 88.32/100(시뮬레이션 58.32/70·설계 의도 20/20·리포트 품질 10/10)을 수신했다. 별도 포털 receipt 파일은 미보유다.


2026-08-30 개인 Go2 12k 시도는 수치 오류로 중단됐다. 운영진은 장기 발산이 알려진 확률적 불안정이며, 제출용은 배포 PPO 설정을 유지해야 한다고 답변했다. 이를 공식 completed trial로 넣지 않는다. 발산 전 9500 후보의 별도 evaluator 결과와 실패한 학습 run 상태를 각각 기록한다.

“5k best”의 실제 저장 iteration은 4500이었다. 요청 iterations·실제 checkpoint iteration·reward peak step·선택 규칙을 분리해 기록한다. 동일 9500 시점 또는 동일 best-through-window 규칙끼리 비교하고, 5k 선별·9.5k 비교·12k 추가 확인을 섞지 않는다. baseline 근거는 `07`을 따른다.

각 비교 표의 Run 행에는 최소한 `fresh/resume`, parent checkpoint SHA, requested iterations, last console iteration, last saved checkpoint iteration, reward peak step, 선택한 policy/checkpoint SHA를 함께 쓴다. 이 중 어느 하나가 불명확하면 “5K”, “best”, “개선”이라는 짧은 표기를 근거로 사용하지 않는다. canonical evidence·Release 링크와 OFFICIAL 여부는 registry Run에서 확인한다.

## 첫 sampler

- 비교 가능한 trial 0~4개: baseline + 수동 단변수 sweep
- 5~7개: designed anchor 비교, TPE 시작 안 함
- 8~12개: `n_startup_trials=6`, `multivariate=True`, 고정 seed의 TPE 한 단계
- 13개 이상: 한 로봇의 2단계 study 또는 상위 영역 재검증 검토

CMA-ES는 동일한 3~4개 연속 파라미터의 좁은 영역에 충분한 완료 trial이 쌓인 후에만 검토한다. Grid Search는 차원 증가에 따른 조합 폭발 때문에 사용하지 않는다.

## H1 단계별 search space

### Stability v1

| Optuna 값 | 실제 reward | 범위 | scale | baseline |
| --- | --- | ---: | --- | ---: |
| `termination_abs` | 음수로 적용 | 5~100 | log | 5 |
| `flat_orientation_abs` | 음수로 적용 | 0.3~3.0 | log | 1.5 |
| `ang_vel_xy_abs` | 음수로 적용 | 0.02~0.30 | log | 0.05 |

이 단계에서는 tracking, gait, joint deviation, action-rate를 baseline에 고정한다.

### Tracking/Gait v1

Stability의 안전 영역을 고정한 뒤 별도 study로 연다.

| reward | 범위 | baseline |
| --- | ---: | ---: |
| `track_lin_vel_xy_exp` | 0.5~1.5 | 0.5 |
| `track_ang_vel_z_exp` | 0.5~1.5 | 0.5 |
| `feet_air_time` | 0.10~0.30 | 0.20 |

`feet_air_time=0.75`는 백업 코드가 hopping reward hacking 예시로 제시한 값이므로 성능 탐색 후보에서 제외한다.

H-004's observed metrics remain available, but its comparison with PERSONAL H-001 does not isolate termination. Historical H-005~H-008 completed from the identified -0.2 PERSONAL parent; H-005/006 changed feet -0.2→+.25/+.30, and H-007/008 changed both feet and track. Do not import those historical results as clean +0.2-parent single-delta Optuna trials. H-009~H-011 remain valid descriptions of single changes within the historical H-008 configuration, but require corrected-lineage interpretation separately. Existing late-window and video observations remain descriptive; they do not prove reward causality. The fresh +0.2 `TERM-50` parent and unchanged control described here were the plan as of 2026-09-21; their 2026-09-25 outcomes are recorded below. Preserve final-numbered policy selection and do not create a checkpoint tournament.

The corrected 2026-09-25 PERSONAL comparison is evidence for **manual candidate ranking**, not completed Optuna trials or official scores: `AIRTIME-025` is a modest XY-improvement follow-up candidate; `AIRTIME-030` remains HOLD; `LINTRACK-100` is REJECT as an overall candidate despite lower XY error because yaw and terrain deteriorated; `LINTRACK-075` remains HOLD; a future matched paired evaluation would be informative. The H1 integrated Windows launcher is installed and has passed 60 CPU regression tests plus PowerShell/install verification, but H1 Windows GPU full validation and these candidates' paired evaluations are not yet run. All four share the corrected `TERM-50` parent final `model_1499` (legacy H-001 Run 05) (SHA `5e3a3150…1b8ad82`) and an unchanged 3K control; no candidate is adopted from one seed and qualitative videos. See [corrected comparison](14_H1_NEXT_RUN_PARAMETER_COMPARISON.md) and the three 2026-09-25 source reports linked there.

The subsequent corrected `LINTRACK-075` 3K final (legacy H-008; recorded SHA `49fdb297…14983`) supports a separate +2K unchanged control versus `HIPDEV-030`, `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch, and `HIPDEV-010` single-delta comparisons. `HIPDEV-030` has the clearest late yaw-error reduction but no decisive posture/progress gain and stays HOLD; `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch has smaller yaw/contact direction gains and is PROMOTE **only as a future paired-evaluation candidate**; `HIPDEV-010` has small tracking gains but posture costs and window-sensitive contact, so remains HOLD. Do not rank changed-weight branches by total reward or count 2,000 consecutive TensorBoard points as independent trials. The organizer-described Tracking aggregate combines unnormalized body-frame x/y/yaw error per step and equally weights episode means, so yaw and repeated short failures matter, but the final error-to-score transform remains undisclosed. Keep these PERSONAL observations out of official-score Optuna labels until a comparable evaluator has been run; see [corrected 5K comparison](14_H1_NEXT_RUN_PARAMETER_COMPARISON.md) and [evaluation boundary](10_SOLUTION_AND_VALIDATION_BLUEPRINTS.md).

The 2026-09-27 [PERSONAL three-Run plan](../planning/historical/2026-09-27_H1_PERSONAL_FRESH_AND_CONTINUATION_PLAN.md) has now produced `AIRTIME-025` fresh 3K, `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch fresh 3K, plus an unchanged continuation of corrected `AIRTIME-025` through global 4997. All three train evidence archives record exit 0 and validation PASS; see the [evidence intake and three six-file comparison bundles](../experiments/h1/training/2026-09-27_H1_FRESH_AND_CONTINUATION_EVIDENCE_INTAKE.md). Fresh means no checkpoint, not BASE reward: `AIRTIME-025` records TERM/track/feet `-50/0.5/0.25`, while `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch records `-50/0.75/0.25`. The `AIRTIME-025` analyses find a small same-parent 3K XY gain against the unchanged control with terrain/contact trade-offs, no all-axis fresh-versus-resume winner, and improved late-window terrain/XY/yaw/contact after the corrected `AIRTIME-025` +2K continuation. That continuation is a training-length effect, **not proof that feet `0.25` beats `0.20`**. Its video is from `model_4800.pt`, not representative final `model_4997.pt`; the fresh `AIRTIME-025` video is from `model_2750.pt`, not final `model_2999.pt`. The received `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch versus `AIRTIME-025` fresh analysis reports lower late-500 XY error (0.33248 vs 0.37355) but higher yaw error (1.58899 vs 1.02692) and training base-contact (30.491% vs 29.935%), with no terrain advantage. This supports **PROMOTE only as a future paired-evaluation candidate**, not adoption; The `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch video's source is automatic best `model_2700.pt`, not final `model_2999.pt`. These remain PERSONAL single-seed observations, not Optuna objective labels or OFFICIAL performance evidence. **The reusable H1 Windows launcher is installed and CPU-verified (60 regression tests), but H1 Windows GPU full validation and these candidates' paired evaluations are not yet run.** Until that validation and actual matched datasets exist, use matched provenance and native-video behavior only as qualitative evidence; do not imply that a paired numeric evaluation is queued or already available. Keep the failed first resume attempt as failure evidence and never transfer a PERSONAL checkpoint as an official policy. [H-005/H-010 synthesis](14_H1_NEXT_RUN_PARAMETER_COMPARISON.md).

### Historical feet=-0.2 H-008 parent and Run 01 siblings (2026-09-17–21)

The following `d9a30c8a…1912ae` checkpoint, automatic-best mapping and **H-010/H-011 both HOLD** decision belong only to the old PERSONAL lineage. They do not supersede corrected Run 02's H-010 PROMOTE-to-paired-evaluation judgment above.

The user-directed H-008 continuation from verified `model_2998` to global 4997 is now complete
without reward changes. Its canonical archive outer hash and 41/41 internal manifest verify, but
generic `issacsimz run` leaves execution-time profile/source/lineage null and validation WARN.
This does not erase Run 01's HOLD interpretation, supply the missing unchanged control, or create
OFFICIAL performance evidence. H-009, H-010, and H-011 do **not** branch from that H-008 5K
continuation. All use the already completed H-008 3K final `model_2998.pt`
(SHA-256 `d9a30c8a…1912ae`) as their common parent: H-009 changes only
`joint_deviation_hip -0.20 → -0.30`, H-010 changes only `feet_air_time 0.20 → 0.25`, and H-011
changes only `joint_deviation_hip -0.20 → -0.10`. H-009 PERSONAL Run 01 is COMPLETE and analyzed:
global 2998→4997, validation PASS, final `model_4997`, numerical health good, but the known
unchanged-control comparison has only negligible aggregate differences and H-009 has no fresh
video/evaluator. Its decision is HOLD. H-010 and H-011 have since completed as PERSONAL
3K→5K (+2K) siblings with validation PASS and final `model_4997` representatives. H-010
`airtime=0.25` remains effectively tied with the unchanged `.20` control; H-011 `hip=-0.10`
also has no decisive aggregate gain and leaves yaw high. **These historical Run 01 branches** were both HOLD at that time; corrected H-010 Run 02 is separately PROMOTE only to paired evaluation. Together with H-009
`hip=-0.30`, the same-parent three-point hip comparison does not establish a winner. The deltas
must not be combined, and these records remain registry-managed hypotheses rather than Optuna trials.

### Separate TERM-100 fresh screen (legacy H-012)

`TERM-100` (legacy H-012) is a registry-managed **HOLD** hypothesis, not an Optuna trial. Its PERSONAL
fresh 5K run completed with evidence PASS after changing only `termination_penalty -5 → -100`
from the BASE configuration. The 3K length was an earlier plan. `model_4700` is the automatic
best and six-terrain video source; the run ended at `model_4999`. The available analysis reports
recovered terrain/survival but high yaw error and no matched PERSONAL `-5` control. Keep this
branch separate from H-001 and H-008-derived deltas, and do not call `-100` a search winner.

### Historical Run 01 selector example

Do not call the early raw/report difference a selector bug without reproducing the native resume
filter. The current finalizer excludes steps before `lo + max(50, floor((hi-lo)×0.10))`: H-009
3041, H-010 3044, and H-011 3084 are all below the approximately 3197 threshold. H-010's
eligible peak is 3299 (`model_3300`) and H-011's is 3203 (`model_3200`). Automatic reward best
still does not replace the final-numbered representative rule.

### Fine v1

- `joint_deviation_hip`: 절댓값 0.1~0.5
- `joint_deviation_torso`: 절댓값 0.05~0.3
- `action_rate_l2`: 절댓값 0.0001~0.005, log scale

## Go2 초기 범위

실제 `env.yaml`에서 활성 key임을 확인한 값만 넣는다.

| reward | 범위 | baseline |
| --- | ---: | ---: |
| `track_lin_vel_xy_exp` | 0.75~1.50 | 1.0 |
| `feet_air_time` | 0.01~0.15 | 0.01 |
| `lin_vel_z_l2` 절댓값 | 1.5~5.0 | 3.0 |

주석 처리된 key가 실제 환경에서 적용되는지 확인되지 않으면 탐색 변수로 넣지 않는다.

## 공식 baseline 1K를 비교 기준으로 쓰는 법

공식 Go2 1K는 terrain이 iter 322~999 동안 콘솔에서 0.0000, 최종 XY error 1.8421인 반면 timeout은 93.45%였다. 긴 episode·낮은 낙상률만으로 후보를 승격하지 않고 terrain 500→1000 방향, XY/yaw 추종, 생존과 수치 안정성을 함께 본다. 이 1K 결과 자체는 baseline 장기 실패 판정이나 Optuna objective가 아니다.

official fresh `model_4800`과 recovery `model_4900`의 학습 지표는 resume curriculum reset 때문에 같은 study objective의 개선율로 계산하지 않는다. 이후 개인 L40S의 동일 조건 fixed evaluator가 4300/4800/4900을 비교했고, 4800/4900 native 비교 영상 6개와 original 4800 matching policy/env 제출 snapshot도 확보됐다. 4800 제출본은 공식 3라운드에서 87.55/100을 받았다. 이 결과를 reward 두 항의 단독 인과 효과로 쓰지 않으며, 추가 일반화 확인에는 multi-seed와 worst-terrain 평가가 필요하다.

checkpoint selection은 새 reward trial이 아니다. 4300·4800은 같은 fresh trajectory의 서로 다른 policy state이고 4900은 4800에서 resume한 recovery state다. 학습 중 한 시점의 reward를 동일 objective table에 넣지 않는다. 첫 fixed evaluator는 4800의 낙상·생존 균형과 4900의 tracking·진행성 우세를 보였지만 단일 seed이므로 worst-seed 우열은 미확인이다. 4300은 fresh stability control이다.

제공된 [운영진 checkpoint 답변 전사본](../incoming/other/reviewed/2026-09-26_H1_ORGANIZER_CHECKPOINT_QA_SIRIUS_YEOLMU.md)은 자동 `model_best.pt`가 reward 기준의 기본 후보이며 보존된 다른 checkpoint를 근거와 함께 제출용으로 고를 수 있다고 설명한다. 이는 checkpoint 선택의 허용 범위이지 Optuna reward trial 수를 늘리거나 학습 중 `mean_reward` 최고를 공식 평가 objective로 대체하라는 뜻이 아니다. 선택 회차와 근거·policy identity는 별도로 기록한다.

첫 fixed batch(seed 4201, difficulty 1.0)에서는 4800이 평균 timeout 생존 `98.18%`, worst terrain `93.75%`, base-contact `1.82%`로 4900보다 앞섰고, 4900은 평균 XY RMSE와 변위에서 앞섰다. 따라서 objective를 한 숫자로 합쳐 즉시 승자를 선언하지 않는다. 4800을 multi-seed priority, 4900을 tracking challenger, 4300을 control로 두고 seed 반복 뒤 worst-seed·worst-terrain을 우선한다. `success_timeout_pct`는 traversal 성공이 아니므로 inverted stairs처럼 버티지만 전진하지 못한 경우를 별도 실패 기준으로 처리한다.

당시 개인 evaluator 판단은 4800을 stability-first 제출 후보, 4900을 progress-first 대안으로 두는 것이었다. 같은 env index를 맞춘 4800/4900 관측에서 4800만 낙상 7, 4900만 낙상 23, 공동 낙상 0, 공동 생존 354였지만 64 parallel env를 64개의 독립 seed 반복으로 세지 않는다. 후속 native 영상 6개는 이 trade-off를 정성적으로 확인하는 보조 자료이며 objective 표본을 추가하지 않는다. 실제 제출·공식 점수는 아래의 별도 original-4800 snapshot에만 귀속한다. reward trial 선택, checkpoint 선택, submit-ready artifact 판정은 서로 다른 의사결정 단계로 유지한다.

이 original-4800 matching submission snapshot은 이후 Round-3 official evaluation에서 **87.55/100**
(시뮬레이션 58.55/70)를 받았다. 이는 실제 제출 결과로 보존하되, 단일 정책·단일 대회 평가의
score를 private fixed evaluator의 multi-seed objective나 두 reward 항의 인과 효과로 역산하지
않는다. 다음 보고서에는 실패·원복·잔여 traversal 문제를 숨기지 않고, 설정과 수치가 맞는
checkpoint 선택 이유를 기록한다. 운영진은 이 구체적 기록 방식의 report quality를 10/10으로
평가했으며, design-intent 19/20의 정확한 AI 판정 이유는 특정하지 못했다고 답했다.

## objective 원칙

`Train/mean_reward`를 objective로 쓰지 않는다. reward 계수를 바꾸면 총 reward 척도가 달라지고, 높은 training reward가 생존·추종·terrain 성능을 보장하지 않는다.

아래는 과거에 제안한 `Robust Proxy Score` 개념안이며, 현재 v2에 승인·설정된 objective가 아니다. 실제 metric mapping·집계·가중치·비교 조건을 승인하기 전 임의로 이 식을 구현하거나 Tell에 입력하지 않는다.

```text
scenario score
= survival × tracking quality

policy score
= 평균 scenario 성능
 + worst-case 성능
 + recovery
 - fall/failure penalty
 - seed instability
```

모든 component와 normalization·weight를 study 시작 전에 고정하고 `objective_version`으로 기록한다. 공식 점수나 예상 공식 점수라고 부르지 않는다.

## trial 상태와 pruning

- 정상 평가됐지만 즉시 붕괴: `COMPLETE`와 낮거나 음수 objective
- NaN, process crash, export 실패: `FAIL` (발산 시점·직전 checkpoint·value loss/action std/finite 점검 결과를 metadata에 남긴다.)
- 운영자가 임의로 중단한 미완료 실행: 이유와 상태를 명시

초기에는 `NopPruner`를 쓴다. 초반 training mean reward가 최종 terrain·recovery를 대표한다는 근거가 없기 때문이다. 중간 checkpoint를 동일 evaluator로 반복 평가할 수 있을 때만 보수적 pruning을 검토한다.

## 저장 구조

Optuna DB에는 parameter, objective, 작은 metadata만 둔다. policy·checkpoint·영상·전체 metric은 trial ID와 SHA-256으로 연결한 별도 artifact로 보관한다.

```text
trial_id
robot / study / iterations / seed
reward values
source commit / reward hash / env hash / policy hash
evaluator / scenario / objective version
component metrics
artifact paths
decision and reason
```

## 중단 조건

- evaluator bug나 observation mismatch가 반복됨
- 같은 policy의 seed 분산이 reward 후보 간 차이보다 큼
- 개인 proxy 순위와 공식 결과가 지속적으로 반대임
- 남은 서버 시간으로 비교 가능한 trial 8개를 만들 수 없음
- reward hacking 상위 후보가 반복됨

이 경우 Optuna를 멈추고 evaluator 수정 또는 수동 단변수 실험으로 돌아간다.

## 2026-10-09 Go2 R3/R5 — objective 조정 전 coverage 확인

[후속 분석](../experiments/go2/analysis/2026-10-09_GO2_R3_4800_R5_7450_LOCAL_OFFICIAL_COMPARISON.md): 같은 PERSONAL protocol에서 계단 통합 오차 **0.32029→0.14852**, 실패 **15/783→4/772**, G2 오차 **0.09085→0.07699**로 개선됐지만 공식 계단·전방위 Tracking Score는 하락했다. 로컬 고정 12.5cm/직진 조건과 공식10–15cm·미공개 명령/초기조건의 coverage를 우선 확인한다. 같은 scorer/collector/config와 raw 재집계가 일치하므로 점수 보정·scorer 교체·새 reward 학습을 서두르지 않는다. 과거 PERSONAL all-around REJECT를 공식 추종 대조군 제외로 확대하지 않으며, 4800의 공식 추종 상대 우위와7450의 공식 생존 이득을 모두 보존한다. reward-effect HOLD는 유지한다. 이번 비교는 새 학습 trial이 아니다. 공식 수치 분해는 이미 받았으므로 미공개 높이·명령·전환/초기조건만 최소 확인한다. 이후 telemetry/coverage 확장은 별도 작업이며 이번 반영이 실행 승인은 아니다.
