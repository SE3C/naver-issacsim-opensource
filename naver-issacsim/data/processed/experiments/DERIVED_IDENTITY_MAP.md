# 파생 수치 파일 입력 식별 매핑 — 2026-10-12

이 문서는 기존 JSON/CSV를 재작성하지 않고 **파일명과 checkpoint 번호만으로 Run을 오인하지 않도록** 하는 외부 sidecar다. 아래 사례는 확인된 기존 보고서에서 읽은 값이며 전체 수치 파일의 전수 검사 결과가 아니다.

## 2026-10-15 추가 정책 식별 — 모델 번호 재사용 주의

다음 세 체크포인트는 모두 후속 Windows PERSONAL 평가가 존재하며, 숫자가 같거나 reward 축이 유사하더라도 **기존 2026-10-10 원자료 JSON 3정책 집합에 포함되지 않는다**. 아래 연결은 별도 OFFICIAL 학습 index·체크포인트 SHA와 평가 공개 기록에 근거하며, 10/15 MD 원문 안의 `source_run_id=null`을 바꾸지 않는다.

| 평가 정책 | 실제 학습 Run | 체크포인트 SHA-256 | 분석 판정 |
| --- | --- | --- | --- |
| ACTRATE-0001 부모→lin=0.65 +2K **old model_4650** | `20261010-154926-h1-actrate0001-lintrack065-from2700-plus2k` | `ce7ad58657f3dd744e7cf2b7531f3d7d455773dfc6fb135f39d8a55aa49dea70` | [2026-10-11 HOLD](h1/analysis/2026-10-11_ACTRATE0001_LINTRACK065_MODEL4650_POLICY_REVIEW.md) · [10/14 네 정책 참고 비교](h1/analysis/2026-10-14_H1_4POLICY_LINTRACK065_COMPARISON_INTAKE.md) |
| ACTRATE-0001 부모→action baseline 복원 +2K **new model_4650** | `20261014-142200-h1-actrate-return2700-2k` | `a8249db467a60015036bf229b0026b215a61e17859f1d302efe283af225b84ea` | [2026-10-15 HOLD](h1/analysis/2026-10-15_H1_MODEL4650_LINTRACK065_POLICY_REVIEW.md) |
| h1-submit-2 기준 lin=0.65 fresh5K **model_4950** | `20261014-081901-h1-lintrack-065-fresh5k` | `b7528923eef5b1368ba2299f4e0538804ba00dd358049bfdff5027f448e31ece` | [2026-10-15 HOLD](h1/analysis/2026-10-15_H1_MODEL4650_LINTRACK065_POLICY_REVIEW.md) |

**값 혼용 금지:** `ce7ad586…` 4650의 H3 월드 종료 잔류 **2.398m** / H5 rough 평균 **9.546m**와 `a8249db4…` 4650의 **0.167m / 8.769m**는 각각 다른 ZIP 분석 기록이다. `b7528923…` fresh4950의 H3/H5는 **3.102m / 8.995m**다. 서로 직접 짝지어 원인 효과를 판정한 통제 실험이 아니다.

## H1 `scenario7` 기존 파생 JSON

- [Paired deltas](h1/2026-10-10_H1_SCENARIO7_PAIRED_DELTAS.json)의 `model_2850 minus model_2800` 등은 **해당 비교 세트에서만** 해석해야 한다. `model_2850`은 ORIENT-100이고 별도 ACTRATE-001/model_2850과 다른 checkpoint다.
- [RAW_SUMMARY](h1/2026-10-10_H1_SCENARIO7_RAW_SUMMARY.json)의 SHA 값과 [9,216 episode 원문 분석](./h1/analysis/2026-10-10_H1_SCENARIO7_RAW_3POLICY_MATCHED_ANALYSIS.md)의 출처·프로토콜을 함께 읽는다.

| JSON key | 학습 Run ID | 체크포인트 SHA-256 | 원본 평가 ZIP SHA-256 |
| --- | --- | --- | --- |
| `model_2800` (`TERM-50`) | `20261008-062732-h1-term-50-fresh3k-control` | `dffaa77848741fed1f4d22d0b78d4d8911af49057541107845e4d1df02c09ad6` | `d4a47b0e182763e21077b688f44f7d9cdc00759c0f0f78f4217930e1c49975da` |
| `model_2850` (`ORIENT-100`) | `20261006-133517-h1-orient-100-fresh3k-official` | `6aedeced60562c1d496d5319d29b76cf9e26ff43df06827cb370f24f5313f7b0` | `aecc82b13671d54c96813af6c02c1b2a7769ee001b30aa4a5c2761457110eb7a` |
| `model_2700` (`ACTRATE-0001`) | `20261009-142350-h1-actrate-0001-fresh3k` | `e54d3389e20ea913968ef8d3edbea5004368ff225fa6b94f73fcd91cf93ca7ae` | `6270d299def2a3bcb8cc10253027898621dd65a00ad30baafde0cbcde03076e3` |

원문은 평가 cohort/protocol 패리티를 확인했지만 각 terrain episode의 물리 초기 조건까지 동일하다는 뜻은 아니다. OFFICIAL training source provenance가 자동 검증된 것도 아니다.

## Go2 G-005 recovery 그래프 CSV

[`checkpoint_comparison.csv`](go2/2026-09-14_GO2_A1_MAJOR_GRAPHS/checkpoint_comparison.csv)는 candidate·iteration·metric만 가지므로 숫자별 출처를 [해당 그래프 README](go2/2026-09-14_GO2_A1_MAJOR_GRAPHS/README.md) 및 [Go2 G-005 실험 기록](../../../research/experiments/go2/G-005.md)과 함께 읽는다. `Original fallback,4800`은 interrupted original fresh의 checkpoint, `Recovery best checkpoint,4900`은 별도 resume/recovery 단계다. 이 CSV에는 SHA·evaluated artifact/프로토콜 ID가 없으므로 해당 필드를 **unknown**으로 유지하고, 원문 CSV는 변경하지 않는다.

어느 파일에서든 `model_2850` 같은 이름·iteration·`model_best.pt`만으로 정책을 자동 병합하지 않는다.
