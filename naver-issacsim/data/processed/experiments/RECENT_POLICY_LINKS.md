# 최근 정책 — 학습·분석·원문·게시 연결

## 2026-10-15 lin=.55 / model4650 보고서 수납 완료

[원문·계보·HOLD](h1/analysis/2026-10-15_H1_LINTRACK055_MODEL4650_POLICY_REVIEW.md): OFFICIAL Run `20261015-105910-h1-actrate0001-lintrack-055-from2700-plus2k`, PERSONAL 평가 checkpoint SHA `e8a358a5…`. 학습·평가·분석 수납 완료와 범용 채택 보류를 구분한다. H1 world drift .702m,H3 world 잔류2.363m,H5 진행9.242m는 제공 보고서 값이며 원점 복귀를 공식 tracking 실패율로 취급하지 않는다.

## 2026-10-15 ACTRATE 같은 부모 CPU 비교 완료

[원문·CSV·계보·판정](h1/analysis/2026-10-15_ACTRATE_PARENT_UNCHANGED_RESTORATION_COMPARISON_INTAKE.md): 부모2700 HOLD, 무변경4699는 이번 세 후보의 범용·전진/험지 대표에서 REJECT, 복원4650(`a8249db4…`) HOLD. 학습 COMPLETED/PASS·원본·null provenance를 유지하며 옛 lin=.65 resume4650(`ce7ad586…`)은 이번 비교가 아니다.


## 2026-10-15 H1 신규 원문 판정 링크 (현재)

[두 정책 통합 검토](h1/analysis/2026-10-15_H1_MODEL4650_LINTRACK065_POLICY_REVIEW.md), [MODEL4650 분석 원문](../incoming/other/reviewed/H1_MODEL4650_POLICY_ANALYSIS_20261015.md), [LINTRACK-065 분석 원문](../incoming/other/reviewed/H1_LINTRACK-065_POLICY_ANALYSIS_20261015.md). 두 원문은 각 PERSONAL 3,072-episode 평가·6영상의 사후 분석으로, **행동 후보 둘 다 HOLD**다. ZIP `source_run_id=null`은 유지하며 별도의 OFFICIAL index/SHA 연결로 각각 `20261014-142200-h1-actrate-return2700-2k / model_4650`(SHA `a8249d…`)과 `20261014-081901-h1-lintrack-065-fresh5k / model_4950`(SHA `b75289…`)을 식별한다. 기존 `20261010-154926-h1-actrate0001-lintrack065-from2700-plus2k / model_4650`(SHA `ce7ad5…`)와 서로 다른 정책. 다음에는 새로운 GPU보다 보존된 CPU 평가 raw의 동일 조건 비교가 우선이며, 분석 완료 ≠ 공식 점수/실제 채점이다.


2026-10-14 선별 탐색표. 새로운 canonical 상태 DB가 아니다. [현재 registry](../../../research/EXPERIMENTS.md)와 각 문서의 실제 SHA/Run을 우선한다. 파일명만 같다고 같은 정책으로 묶지 않는다.

학습과 후속 평가를 다른 열에 둔다. NVIDIA 보조평가도 분석이다. 이 표의 Windows 후속 평가는 PERSONAL이며 OFFICIAL 학습/채점과 별개다. LINTRACK-075 corrected 4997의 학습도 PERSONAL이다. 원문은 읽기 전용 reviewed 자료로 유지한다.

## 보고서의 비어 있는 Run ID를 보완하는 확인된 학습 연결

원문 또는 평가 JSON의 `source_run_id=null`은 그대로 보존한다. 아래는 별도 학습 기록의 checkpoint SHA와 연결한 **Source training Run ID**이며 Windows 평가 ID가 아니다. 원문 자체가 이 계보를 검증했다고 소급하지 않는다. 보고서의 비교 대상도 해당 정책 행으로 찾는다.

| 보고서의 정책 | Source training Run ID | 검증 근거 |
| --- | --- | --- |
| H1 ACTRATE0001→lin=.55 / model4650 (e8a358a5…) | `20261015-105910-h1-actrate0001-lintrack-055-from2700-plus2k` | [보고서·기존 학습 index/SHA 연결](h1/analysis/2026-10-15_H1_LINTRACK055_MODEL4650_POLICY_REVIEW.md); 원 evaluation source_run_id=null 유지 |
| H1 ACTION-rate 복원 +2K / `model_4650` (a8249d…) | `20261014-142200-h1-actrate-return2700-2k` | [2026-10-15 정책 판정/학습 SHA 연결](h1/analysis/2026-10-15_H1_MODEL4650_LINTRACK065_POLICY_REVIEW.md); 기존 lin=.65 resume의 같은 번호와 **별개** |
| H1 LINTRACK-065 h1-submit-2 fresh5K / `model_4950` (b75289…) | `20261014-081901-h1-lintrack-065-fresh5k` | [2026-10-15 정책 판정/학습 SHA 연결](h1/analysis/2026-10-15_H1_MODEL4650_LINTRACK065_POLICY_REVIEW.md); ACTRATE-parent lin=.65 resume와 별개 |
| H1 ACTRATE-0001 unchanged +2K / `model_4699` (722b35…) | `20261014-111135-h1-actrate-0001-unchanged-cont2k` | [같은 부모 reward 무변경 control 학습·후속 평가](../../../research/experiments/h1/exp-h1-action-rate-relaxation.md); **부모2700·복원4650 CPU 비교 완료; 이번 범용 대표 선정에서 REJECT** |
| H1 ACTRATE-0001 / model_9999 | `20261011-041745-h1-actrate-0001-fresh10k-official` | [정책·학습 SHA 연결](h1/analysis/2026-10-11_ACTRATE0001_MODEL9999_POLICY_REVIEW.md) |
| H1 ACTRATE-0001→lin=.65 / model_4650 | `20261010-154926-h1-actrate0001-lintrack065-from2700-plus2k` | [정책·학습 SHA 연결](h1/analysis/2026-10-11_ACTRATE0001_LINTRACK065_MODEL4650_POLICY_REVIEW.md) |
| H1 ACTRATE-0001 / model_2700 | `20261009-142350-h1-actrate-0001-fresh3k` | [학습·평가 SHA 연결](../../../research/experiments/h1/exp-h1-action-rate-relaxation.md) |
| H1 ACTRATE-001 / model_2850 (1e6d…) | `20261010-125324-h1-actrate-001-fresh3k` | [정책·학습 SHA 연결](h1/analysis/2026-10-11_ACTRATE001_MODEL2850_POLICY_REVIEW.md) |
| H1 ORIENT-100 / model_2850 (6aed…) | `20261006-133517-h1-orient-100-fresh3k-official` | [학습 index](h1/training/2026-10-06_ORIENT100_OFFICIAL3K_EVIDENCE_INTAKE.md) |
| H1 ANGTRACK-065 / model_2950 | `20261009-155344-h1-angtrack-065-fresh3k` | [학습 index](h1/training/2026-10-10_ANGTRACK065_OFFICIAL3K_EVIDENCE_INTAKE.md) |
| H1 LINTRACK-075 corrected / model_4997 | `20260925-091257-h1-h008-corrected-control-to5k-h1-corrected-2026` | [PERSONAL 계보·SHA 연결](h1/analysis/2026-10-10_LINTRACK075_CORRECTED5K_MODEL4997_POLICY_REVIEW.md) |
| H1 action+airtime / model_2950 (14fd…) | `20261013-144616-h1-actrate0001-airtime025-fresh3k` | [학습 index와 보고서 연결](h1/analysis/2026-10-14_ACTRATE0001_FRESH_COMBINATION_REPORT_INTAKE.md) |
| H1 action+feet_slide / model_2950 (c4b2…) | `20261013-153313-h1-actrate0001-feet_slide-fresh3k` | [학습 index와 보고서 연결](h1/analysis/2026-10-14_ACTRATE0001_FRESH_COMBINATION_REPORT_INTAKE.md) |
| Go2 original model_4800 / g2-submit-3 | `20260914-084321-go2-a1-tracklin150-lvz-m2-5k-official` | [Original 4800 계보](../../../research/experiments/go2/G-005.md); interrupted 학습, recovery 4900과 구분 |
| Go2 LINTRACK-125 / model_2950 | `20260928-230114-go2-lintrack125-fresh3k-r5-official` | [학습 index·평가 SHA 연결](../../../research/experiments/go2/G-001.md) |
| Go2 LINTRACK-125 / model_7050 및 model_7450 | `20260929-154342-go2-lintrack-125-fresh7500-official` | [학습·제출 SHA 연결](../../../research/experiments/go2/G-001.md); best 7050과 terminal 7450은 별도 checkpoint |

이전 보고서에 이미 명시된 학습 Run ID는 원문을 따른다. 공개 실패·규정·운영진 답변에는 단일 학습 Run ID가 해당하지 않을 수 있다. 근거가 부족한 옛 보고서는 미확인으로 남기며 alias·파일명·날짜로 새 ID를 만들어 채우지 않는다.

### 과거 보고서의 누락 보완

- [H1_H005_VS_H006_DEEP_ANALYSIS_20260925.md](../incoming/other/reviewed/H1_H005_VS_H006_DEEP_ANALYSIS_20260925.md): corrected unchanged 3K control = `20260925-064143-h1-h001-corrected-control-to3k-h1-corrected-2026`; AIRTIME-025 = `20260925-071158-h1-h005-r02-gait025-corrected-h1-corrected-20260`; AIRTIME-030 = `20260925-074219-h1-h006-r02-gait030-corrected-h1-corrected-20260`。근거는 [H-001](../../../research/experiments/h1/H-001.md), [H-005](../../../research/experiments/h1/H-005.md), [H-006](../../../research/experiments/h1/H-006.md)의 corrected Run 기록이다. 문자열 끝을 추정해서 늘리지 않는다.
- [A1_4800_vs_4900_DEEP_ANALYSIS_AND_LEARNING_RECORD_20260915.md](../incoming/other/reviewed/A1_4800_vs_4900_DEEP_ANALYSIS_AND_LEARNING_RECORD_20260915.md), [기술리포트 초안](../incoming/other/reviewed/GO2_FINAL_TECHNICAL_REPORT_FLOW_DRAFT_20260915.md), [R3 weight similarity 보고서](../incoming/other/reviewed/NCRC_R3_WEIGHT_SIMILARITY_DISCOVERY_2026-09-23.md): original 4300/4800 = 위 original Run `20260914-084321-go2-a1-tracklin150-lvz-m2-5k-official`; recovery 4900 = `20260914-132725-go2-a1-tracklin150-lvz-m2-resume4800-to5k-offici`. [G-005 원본·recovery 기록](../../../research/experiments/go2/G-005.md)을 구분한다.
- [2026-09-18_H008_H1_MODEL2998_6TERRAIN_VIDEO_ANALYSIS.md](../incoming/other/reviewed/2026-09-18_H008_H1_MODEL2998_6TERRAIN_VIDEO_ANALYSIS.md): **역사적 H-008 Run 01의 exact training Run ID 미확인**. [기존 detail](../../../research/experiments/h1/H-008.md)의 후대 corrected Run 03/model2998 ID로 대체하지 않는다.

| 정책 checkpoint | 학습 Run 근거 | 후속 해석/공식 채점 | 수신 보고서 원문 | 평가 게시·receipt |
| --- | --- | --- | --- | --- |
| H1 ACTRATE0001→lin=.55 · model4650 (e8a358a5…) | [학습 기록](../../../research/experiments/h1/exp-h1-action-first-planar-tracking-switch.md) | [HOLD](h1/analysis/2026-10-15_H1_LINTRACK055_MODEL4650_POLICY_REVIEW.md) | [원문](../incoming/other/reviewed/H1_ACTRATE0001-LINTRACK055_POLICY_ANALYSIS_20261015.md) | [Eval Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261015-exp-h1-action-first-planar-tracking-switch-lin055-model4650-video-eval) |
| H1 ACTION 복원 +2K · model4650 (a8249d…) | [학습 기록](../../../research/experiments/h1/exp-h1-action-rate-restoration.md) | [2026-10-15 HOLD](h1/analysis/2026-10-15_H1_MODEL4650_LINTRACK065_POLICY_REVIEW.md) | [원문](../incoming/other/reviewed/H1_MODEL4650_POLICY_ANALYSIS_20261015.md) | [Eval Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261015-exp-h1-action-rate-restoration-model4650-video-eval) |
| H1 LINTRACK-065 fresh5K · model4950 (b75289…) | [학습 기록](../../../research/experiments/h1/exp-h1-planar-tracking-weight.md) | [2026-10-15 HOLD](h1/analysis/2026-10-15_H1_MODEL4650_LINTRACK065_POLICY_REVIEW.md) | [원문](../incoming/other/reviewed/H1_LINTRACK-065_POLICY_ANALYSIS_20261015.md) | [Eval Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261015-exp-h1-planar-tracking-weight-model4950-video-eval) |
| H1 action+airtime · 2950 (14fd…) | [학습 기록](../../../research/experiments/h1/exp-h1-action-airtime-fresh-interaction.md) | [수신·Run 연결](h1/analysis/2026-10-14_ACTRATE0001_FRESH_COMBINATION_REPORT_INTAKE.md) | [원문](../incoming/other/reviewed/H1_SHA14FD_MODEL2950_POLICY_ANALYSIS_20261014.md) | 해당 Experiment의 학습·Eval Release |
| H1 action+feet_slide · 2950 (c4b2…) | [학습 기록](../../../research/experiments/h1/exp-h1-action-foot-contact-stability.md) | [수신·Run 연결](h1/analysis/2026-10-14_ACTRATE0001_FRESH_COMBINATION_REPORT_INTAKE.md) | [원문](../incoming/other/reviewed/H1_C4B2_POLICY_ANALYSIS_20261014.md) | 해당 Experiment의 학습·Eval Release |
| H1 ACTRATE-0001 · 9999 | [학습 기록](h1/training/2026-10-11_ACTRATE0001_OFFICIAL10K_EVIDENCE_INTAKE.md) | [분석 기록](h1/analysis/2026-10-11_ACTRATE0001_MODEL9999_POLICY_REVIEW.md) | [원문](../incoming/other/reviewed/H1_MODEL9999_POLICY_ANALYSIS_20261011.md) | [게시/검증 기록](../operations/windows_h1_video_evaluation/2026-10-11_ACTRATE0001_FRESH10K_MODEL9999_PUBLICATION.md) |
| H1 ACTRATE-0001→lin=.65 · 4650 | [학습 기록](../../../research/experiments/h1/exp-h1-action-first-planar-tracking-switch.md) | [분석 기록](h1/analysis/2026-10-11_ACTRATE0001_LINTRACK065_MODEL4650_POLICY_REVIEW.md) | [원문](../incoming/other/reviewed/H1_MODEL4650_POLICY_ANALYSIS_20261011.md) | [게시/검증 기록](../operations/windows_h1_video_evaluation/2026-10-11_ACTRATE0001_LINTRACK065_MODEL4650_PUBLICATION.md) |
| H1 ACTRATE-0001 · 2700 | [학습 기록](h1/training/2026-10-09_ACTRATE0001_OFFICIAL3K_EVIDENCE_INTAKE.md) | [분석 기록](h1/analysis/2026-10-10_ACTRATE0001_MODEL2700_POLICY_REVIEW.md) | [원문](../incoming/other/reviewed/H1_MODEL2700_POLICY_ANALYSIS_20261010.md) | [게시/검증 기록](../operations/windows_h1_video_evaluation/2026-10-10_ACTRATE0001_MODEL2700_PUBLICATION.md) |
| H1 ACTRATE-001 · 2850 (SHA 1e6d…bb1) | [학습 기록](../../../research/experiments/h1/exp-h1-action-rate-smoothing.md) | [분석 기록](h1/analysis/2026-10-11_ACTRATE001_MODEL2850_POLICY_REVIEW.md) | [원문](../incoming/other/reviewed/H1_MODEL2850_SHA1E6D_POLICY_ANALYSIS_20261010.md) | [게시/검증 기록](../operations/windows_h1_video_evaluation/2026-10-10_ACTRATE001_MODEL2850_PUBLICATION.md) |
| H1 ORIENT-100 · 2850 (SHA 6aed…f7b0) | [학습 기록](h1/training/2026-10-06_ORIENT100_OFFICIAL3K_EVIDENCE_INTAKE.md) | [분석 기록](../../../research/experiments/h1/exp-h1-rough-terrain-orientation-relaxation.md) | [원문](../incoming/other/reviewed/H1_ORIENT-100_POLICY_ANALYSIS_20261007.md) | 아래 안내 참고 |
| H1 ANGTRACK-065 · 2950 | [학습 기록](h1/training/2026-10-10_ANGTRACK065_OFFICIAL3K_EVIDENCE_INTAKE.md) | [분석 기록](h1/analysis/2026-10-10_ANGTRACK065_MODEL2950_POLICY_REVIEW.md) | [원문](../incoming/other/reviewed/H1_ANGTRACK-065_POLICY_ANALYSIS_20261010.md) | [게시/검증 기록](../operations/windows_h1_video_evaluation/2026-10-10_ANGTRACK065_MODEL2950_PUBLICATION.md) |
| H1 LINTRACK-075 corrected · 4997 | [학습 기록](../../../research/experiments/h1/H-008.md) | [분석 기록](h1/analysis/2026-10-10_LINTRACK075_CORRECTED5K_MODEL4997_POLICY_REVIEW.md) | [원문](../incoming/other/reviewed/H1_LINTRACK-075_CORRECTED5K_POLICY_ANALYSIS_20261010.md) | [게시/검증 기록](../operations/windows_h1_video_evaluation/2026-10-09_LINTRACK075_MODEL4997_PUBLICATION.md) |
| Go2 g2-submit-3 · original 4800 | [학습 기록](../../../research/experiments/go2/G-005.md) | [분석 기록](go2/analysis/2026-10-09_GO2_R3_4800_R5_7450_LOCAL_OFFICIAL_COMPARISON.md) | [원문](../incoming/other/reviewed/GO2_R3_4800_VS_R5_7450_DEEP_ANALYSIS_20261009.md) | [게시/검증 기록](../operations/windows_go2_video_evaluation/2026-10-09_G2_SUBMIT-3_MODEL4800_EVALUATION_RELEASE_NOTES.md) |
| Go2 LINTRACK-125 · 7050 | [학습 기록](../../../research/experiments/go2/G-001.md) | [분석 기록](go2/analysis/2026-10-09_GO2_R3_4800_R5_7450_LOCAL_OFFICIAL_COMPARISON.md) | [원문](../incoming/other/reviewed/GO2_C4800_C7050_C7450_POLICY_COMPARISON_20261005.md) | [게시/검증 기록](../operations/windows_go2_video_evaluation/2026-10-04_LINTRACK-125_MODEL7050_EVALUATION_RELEASE_NOTES.md) |
| Go2 g2-submit-5 · 7450 | [학습 기록](../../../research/experiments/go2/G-001.md) | [분석 기록](go2/analysis/2026-10-08_OFFICIAL_EVAL_GO2_ROUND5_LINTRACK125.md) | [원문](../incoming/other/reviewed/GO2_R3_4800_VS_R5_7450_DEEP_ANALYSIS_20261009.md) | 아래 안내 참고 |
| Go2 LINTRACK-125 · 2950 | [학습 기록](../../../research/experiments/go2/G-001.md) | [평가 안내](../ai_library/21_WINDOWS_GO2_VIDEO_AND_EVALUATION.md) | 별도 원문 연결 없음 | [게시/검증 기록](../operations/windows_go2_video_evaluation/evaluation_2950_verified.json) |

ORIENT-100의 평가 Release 주소는 [Release 관리 문서](../../../docs/RELEASE_TAXONOMY.md)에 보존돼 있다. Go2 7450은 실제 g2-submit-5 제출과 공식 채점 기록이 있으며, 이 선별 조사에서 별도 Windows 평가 Release 연결을 확정하지 못했다. 미연결을 미실행으로 해석하지 않는다. Go2 2950 receipt는 개별 전체 평가 검증이며 자동 A/B 비교 결과가 아니다.

각 분석 문서의 원문·SHA 연결을 따라가면 학습 source와 평가 checkpoint를 구분할 수 있다. h1-submit-6 제출 사실과 PERSONAL model9999 행동 HOLD도 다른 판정으로 유지한다.
