# 수신 원문과 후속 해석 관계 — 선별 대조표 (2026-10-16 갱신)

> **비권위 탐색 색인.** 아래 15개 연결은 파일 본문·명시된 source 링크 및 검토된 status를 근거로 한다. 2026-10-12 당시 reviewed 원문 63건 및 이후 신규 수신 자료의 전수 관계도나 AI 핵심팩 반영률이 아니다. 15번 후속은 저장 raw CPU 재집계를 포함하며, 영상·운영진 시스템의 재조회와는 다르다.

**관계 유형:** `extends`는 후속 자료/검토 범위를 추가한다는 뜻이며 `supersedes`(원문 대체)가 아니다. `intake_interpretation`은 사용자 수신 원문과 별도 가공 수납 문서를 연결하지만 독립 evaluator 실행을 뜻하지 않는다. `experiment_context`는 별도 Run/Experiment 기록으로 가는 안내다. `transcript_to_analysis`는 전달받은 답변·화면의 전사와 분석본을 구분한다.

| 주제 | 선행 원문·보고서 | 후속 분석·Experiment | 관계 | 근거와 해석 경계 |
| --- | --- | --- | --- | --- |
| 1. Go2 fresh3K↔7.5K | [수신·선행](other/reviewed/GO2_20260929-154342-go2-lintrack-125-fresh7500-official_VS_20260928-230114-go2-lintrack125-fresh3k-r5-official_DEEP_ANALYSIS_20260930.md) | [후속·연결](other/reviewed/GO2_20260929-154342-go2-lintrack-125-fresh7500-official_VS_20260928-230114-go2-lintrack125-fresh3k-r5-official_DEEP_ANALYSIS_20261004.md) | `extends` | 09/30 training archive 분석에 10/04 PERSONAL 영상·평가 ZIP 분석 추가. 두 문서는 동일 연구쌍의 서로 다른 입력 범위를 기록. |
| 2. H1 scenario7 report↔raw | [수신·선행](../experiments/h1/analysis/2026-10-10_H1_SCENARIO7_CROSS_POLICY_REPORT_LEVEL_COMPARISON.md) | [후속·연결](../experiments/h1/analysis/2026-10-10_H1_SCENARIO7_RAW_3POLICY_MATCHED_ANALYSIS.md) | `extends` | 후속 9,216 episode 원자료 직접 비교. 기존 report-level 분석과 자료 접근 범위를 구분. |
| 3. H1 ACTRATE-0001 / model2700 | [수신·선행](other/reviewed/H1_MODEL2700_POLICY_ANALYSIS_20261010.md) | [후속·연결](../experiments/h1/analysis/2026-10-10_ACTRATE0001_MODEL2700_POLICY_REVIEW.md) | `intake_interpretation` | 수신 단일 정책 PERSONAL 분석과 가공 수납. 해당 OFFICIAL fresh3K 학습 근거는 별도로 확인. |
| 4. H1 ACTRATE-0001→LINTRACK065 / model4650 | [수신·선행](other/reviewed/H1_MODEL4650_POLICY_ANALYSIS_20261011.md) | [후속·연결](../experiments/h1/analysis/2026-10-11_ACTRATE0001_LINTRACK065_MODEL4650_POLICY_REVIEW.md) | `intake_interpretation` | 실제 OFFICIAL 2700 부모 resume +2K 계보와 PERSONAL model4650 분석 HOLD를 분리하여 연결. |
| 5. H1 ACTRATE-0001 fresh10K / model9999 | [수신·선행](other/reviewed/H1_MODEL9999_POLICY_ANALYSIS_20261011.md) | [후속·연결](../experiments/h1/analysis/2026-10-11_ACTRATE0001_MODEL9999_POLICY_REVIEW.md) | `intake_interpretation` | PERSONAL 행동 HOLD; OFFICIAL 학습 PASS·h1-submit-6 실제 제출과 동의어가 아님. |
| 6. H1 ACTRATE-001 / model2850 SHA1e6d | [수신·선행](other/reviewed/H1_MODEL2850_SHA1E6D_POLICY_ANALYSIS_20261010.md) | [후속·연결](../experiments/h1/analysis/2026-10-11_ACTRATE001_MODEL2850_POLICY_REVIEW.md) | `intake_interpretation` | ACTRATE-001 policy SHA 1e6d…bb1. ORIENT-100의 다른 model2850/SHA 6aed…3b7b0와 혼동 금지. |
| 7. H1 ORIENT-100 / model2850 SHA6aed | [수신·선행](other/reviewed/H1_ORIENT-100_POLICY_ANALYSIS_20261007.md) | [후속·연결](../../../research/experiments/h1/exp-h1-rough-terrain-orientation-relaxation.md) | `experiment_context` | ORIENT-100 단일 PERSONAL 평가 및 Experiment context. ACTRATE-001 model2850과 다른 Run/checkpoint. |
| 8. H1 ANGTRACK-065 / model2950 | [수신·선행](other/reviewed/H1_ANGTRACK-065_POLICY_ANALYSIS_20261010.md) | [후속·연결](../experiments/h1/analysis/2026-10-10_ANGTRACK065_MODEL2950_POLICY_REVIEW.md) | `intake_interpretation` | Windows PERSONAL 개별 정책 HOLD; H3 base-contact 종료 15건. 보상 효과 인과 검증 아님. |
| 9. H1 LINTRACK-075 / model4997 | [수신·선행](other/reviewed/H1_LINTRACK-075_CORRECTED5K_POLICY_ANALYSIS_20261010.md) | [후속·연결](../experiments/h1/analysis/2026-10-10_LINTRACK075_CORRECTED5K_MODEL4997_POLICY_REVIEW.md) | `intake_interpretation` | H-008 corrected PERSONAL continuation의 정책 관찰; 평가 분석을 새 training Run으로 등록하지 않음. |
| 10. Go2 R3/R5 운영진 DM | [수신·선행](other/reviewed/GO2_R3_R5_SURVIVAL_TRACKING_ORGANIZER_DM_RECEIVED_20261008.md) | [후속·연결](../experiments/go2/analysis/2026-10-08_GO2_R3_R5_OFFICIAL_SCORE_COMPONENTS_ORGANIZER_REPLY.md) | `transcript_to_analysis` | 받은 DM 전사 기반. stairs survival 99.0→99.8%, tracking 0.819→0.796; 공식 원시 로그를 직접 읽은 것이 아님. |
| 11. Go2 R5 공식 평가 snapshot | [수신·선행](other/reviewed/SE3C_예선5라운드_Go2_공식평가_사용자전달원문_20261008.md) | [후속·연결](../experiments/go2/analysis/2026-10-08_OFFICIAL_EVAL_GO2_ROUND5_LINTRACK125.md) | `transcript_to_analysis` | 사용자가 전달한 공식 화면/이미지 전사 ↔ Round-5 결과 요약. HTML/이미지 독립 조회가 아님. |
| 12. Go2 original4800 vs terminal7450 | [수신·선행](other/reviewed/GO2_R3_4800_VS_R5_7450_DEEP_ANALYSIS_20261009.md) | [후속·연결](../experiments/go2/analysis/2026-10-09_GO2_R3_4800_R5_7450_LOCAL_OFFICIAL_COMPARISON.md) | `intake_interpretation` | R3 original 4800 INTERRUPTED 학습과 R5 terminal 7450 제출/평가 근거 분리. PERSONAL 평가 COMPLETE가 과거 학습 INTERRUPTED를 바꾸지 않음. |

| 13. H1 ACTION 복원 +2K / `model_4650` SHA a824… | [2026-10-15 원문](other/reviewed/H1_MODEL4650_POLICY_ANALYSIS_20261015.md) | [2026-10-15 통합 검토](../experiments/h1/analysis/2026-10-15_H1_MODEL4650_LINTRACK065_POLICY_REVIEW.md) · [Experiment](../../../research/experiments/h1/exp-h1-action-rate-restoration.md) | `intake_interpretation` / `experiment_context` | OFFICIAL Run `20261014-142200-h1-actrate-return2700-2k`의 별도 index/SHA 외부 연결. 오래된 ACTRATE→lin=.65 모델명 `4650` SHA ce7a…와 서로 다른 정책. PERSONAL 3,072 episodes/HOLD. |
| 14. H1 LINTRACK-065 fresh5K / `model_4950` SHA b752… | [2026-10-15 원문](other/reviewed/H1_LINTRACK-065_POLICY_ANALYSIS_20261015.md) | [2026-10-15 통합 검토](../experiments/h1/analysis/2026-10-15_H1_MODEL4650_LINTRACK065_POLICY_REVIEW.md) · [Experiment](../../../research/experiments/h1/exp-h1-planar-tracking-weight.md) | `intake_interpretation` / `experiment_context` | OFFICIAL fresh5K `20261014-081901-h1-lintrack-065-fresh5k`와 외부 SHA 연결. 기존 ACTRATE-parent lin=.65 resume와 계보가 다름. PERSONAL 3,072 episodes/HOLD. |

| 15. H1 angxy=-.08 / model4650 SHA c272… | [2026-10-16 원문](other/reviewed/H1_ACTRATE0001_ANGXY008_MODEL4650_POLICY_ANALYSIS_20261016.md) | [수납·5정책 CPU 비교](../experiments/h1/analysis/2026-10-16_H1_ANGXY008_MODEL4650_POLICY_REVIEW.md) | `intake_interpretation` / `extends` | 학습 Run `20261015-143107-h1-actrate0001-angxy008-from2700-plus2k`와 index/SHA 외부 연결. 15,360행 비교 후 HOLD. 원문의 R6 미수신은 사용자 전달 공식56.35/70과 구분하며 원문 bytes는 유지. |

## 교차해서 확인할 canonical 기록

- [H1 ACTRATE-0001 fresh10K OFFICIAL evidence intake](../experiments/h1/training/2026-10-11_ACTRATE0001_OFFICIAL10K_EVIDENCE_INTAKE.md) · [Round-6 제출 manifest](../experiments/h1/2026-10-11_PRELIM_R6_SUBMISSION/submission_manifest.json): 실제 training evidence와 제출은 PERSONAL 행동 분석의 HOLD와 별개다. 사용자 전달 R6 공식56.35/70·86.35/100은 수신했으며 포털 원본·수령증 직접 확인은 별도 제약이다.
- [H1 scenario7 파생값 체크포인트 식별](../experiments/DERIVED_IDENTITY_MAP.md): `model_2850` 이름만으로 ACTRATE-001과 ORIENT-100을 하나의 정책으로 합치지 않는다.
- [Go2 공식 R5 결과](../experiments/go2/analysis/2026-10-08_OFFICIAL_EVAL_GO2_ROUND5_LINTRACK125.md)는 7.5K terminal `model_7450` 제출 계보의 결과이고, [Go2 3K↔7.5K PERSONAL 심층 분석](other/reviewed/GO2_20260929-154342-go2-lintrack-125-fresh7500-official_VS_20260928-230114-go2-lintrack125-fresh3k-r5-official_DEEP_ANALYSIS_20261004.md)은 `model_2950` ↔ `model_7050` 평가 비교다. checkpoint·scorer 조건을 혼동하지 않는다.
- [Experiment/Run 현재 registry](../../../research/EXPERIMENTS.md)를 실행·제출 상태의 기준으로 한다. [2026-10-12 기준 원문 63건 및 10/14·10/15 추가 수신 탐색](other/reviewed/README.md)은 별도 유지한다.

## 작업 범위와 한계

이번 연결은 기존 수신 원문·evidence·평가 JSON·제출 snapshot을 이동·교체·삭제하지 않는다. 이름·날짜가 비슷하다는 이유로 나머지 원문에 `duplicate`나 `supersedes`를 부여하지 않는다. source Run 또는 부모 checkpoint가 미검증이면 이름만으로 채우지 않는다. `extends` 관계라도 초기 분석의 당시 한계·평가 조건을 보존한다.
