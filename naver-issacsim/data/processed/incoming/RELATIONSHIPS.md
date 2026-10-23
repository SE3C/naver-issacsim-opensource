# 수신 보고서 관계 색인 — 확인된 표본

이 색인은 `reviewed`와 핵심팩 반영 완료를 동일시하지 않고, 재검토할 때 관계를 찾기 위한 **비권위(non-canonical) 탐색 표**다. 원본 수신 Markdown·실험 기록을 수정하지 않는다. **2026-10-12 기준 63건 및 그 후 추가된 수신 보고서의 전수 목록이나 통합률이 아니다.**

**2026-10-12 당시 63건의 참조 수준:** 원문별 분류와 현재 집계는 [전체 추적 장부](REPORT_PROVENANCE_TRIAGE.md)를 따른다. 단순 언급·문맥 대조를 verified source lineage나 반영 완료로 승격하지 않는다.

**확장된 관계별 탐색:** [수신 보고서↔가공 해석 14쌍](REPORT_CROSSWALK.md)은 아래 두 `extends` 사례와 추가 12건의 원문/수납/Experiment 연결을 별도로 정리한다. 두 색인은 비권위이며 전수 관계도나 원문 대체 판정이 아니다.

| 선행 보고서 | 후속 보고서 | 관계·범위 | 통합 및 현재 판단 |
| --- | --- | --- | --- |
| [Go2 2026-09-30 fresh7.5K vs fresh3K](other/reviewed/GO2_20260929-154342-go2-lintrack-125-fresh7500-official_VS_20260928-230114-go2-lintrack125-fresh3k-r5-official_DEEP_ANALYSIS_20260930.md) | [Go2 2026-10-04 확장 비교](other/reviewed/GO2_20260929-154342-go2-lintrack-125-fresh7500-official_VS_20260928-230114-go2-lintrack125-fresh3k-r5-official_DEEP_ANALYSIS_20261004.md) | `extends`: 후속 문서는 영상·평가 ZIP을 추가로 다룬다. 초기 학습 archive 검토를 전면 `supersedes`한다고 가정하지 않는다. | 현재 정책 선택·제출 상태는 [registry](../../../research/EXPERIMENTS.md) 참조. 핵심팩 개별 반영 상태는 **unknown**. |
| [H1 ANGTRACK 등 3정책 보고서 기반 비교](../experiments/h1/analysis/2026-10-10_H1_SCENARIO7_CROSS_POLICY_REPORT_LEVEL_COMPARISON.md) | [H1 ZIP 원자료 9,216 episode 대조](../experiments/h1/analysis/2026-10-10_H1_SCENARIO7_RAW_3POLICY_MATCHED_ANALYSIS.md) | `extends`: 당시 보고서 기준의 raw ZIP 미접근 제한을 후속 ZIP 수신으로 해소. 서로 다른 분석 단계. | [원자료 분석](../experiments/h1/2026-10-10_H1_SCENARIO7_RAW_3POLICY_MATCHED_ANALYSIS.md), 공식 점수와 구분. |

## 2026-10-15 신규 수신 관계 — 정책 식별 혼동 방지

- [ACTION 복원 4650 원문](other/reviewed/H1_MODEL4650_POLICY_ANALYSIS_20261015.md)과 [LINTRACK-065 fresh4950 원문](other/reviewed/H1_LINTRACK-065_POLICY_ANALYSIS_20261015.md)은 [한 쌍의 후속 수납·판정](../experiments/h1/analysis/2026-10-15_H1_MODEL4650_LINTRACK065_POLICY_REVIEW.md)으로 연결됐다. 단, 두 정책 간 matched raw A/B가 이루어졌다는 뜻은 아니다.
- 10/11 [ACTRATE-parent lin=.65 4650](../experiments/h1/analysis/2026-10-11_ACTRATE0001_LINTRACK065_MODEL4650_POLICY_REVIEW.md)(SHA `ce7ad586…`)과 새 ACTION 복원 4650(SHA `a8249db4…`)의 같은 번호는 정책 동일성을 뜻하지 않는다. 원문 자체는 소급 교체하지 않았다.
- 2026-10-12의 **63건**은 당시 조사 snapshot이다. 이 뒤 확인된 10/14 원문 3건과 10/15 원문 2건의 추가 수신을 기존 63건 전수 통계에 조용히 포함시키지 않는다.

## 관리 규칙

- 추가 행은 실물을 읽고 확인된 연결만 기록한다. 날짜가 최신이라는 이유로 `supersedes`로 분류하지 않는다.
- `reviewed`는 검토 완료이지 `integrated`가 아니다. 실제 AI 반영 대상 파일·절이 확인될 때만 해당 링크를 붙인다.
- unknown을 추측으로 채우거나 원본 source_run_id=null, 미확인 parent, 원문 checksum을 수정하지 않는다.
- canonical 실험 현황은 [Experiment Registry](../../../research/EXPERIMENTS.md), archive와 Run 식별은 Originals의 증거를 따른다.
