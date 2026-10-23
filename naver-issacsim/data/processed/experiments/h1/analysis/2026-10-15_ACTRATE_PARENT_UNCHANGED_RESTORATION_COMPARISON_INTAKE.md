# H1 부모2700 · 무변경4699 · action 복원4650 — CPU 비교 보고서 수납

## 출처·검토 범위

- [수신 보고서 원문](../../../incoming/other/reviewed/H1_ACTRATE_PARENT_UNCHANGED_RESTORATION_COMPARISON_20261015/H1_ACTRATE_PARENT_UNCHANGED_RESTORATION_REPORT_20261015.md)과 CSV·그림·contact sheet·CPU 스크립트 32개를 상대경로 및 bytes 그대로 보존했다. 원문 수정·첨부 코드 실행·새 GPU 작업은 하지 않았다.
- [원본 ZIP 보존](https://github.com/SE3C/naver-issacsim-originals/blob/main/data/raw/external_analysis/h1/2026-10-15_actrate_parent_unchanged_restoration_comparison/H1_ACTRATE_PARENT_UNCHANGED_RESTORATION_COMPARISON_20261015.zip): 2,550,019 bytes, SHA-256 `879e4b357eaed81c1f7f3d2eaf48ac6c08c9d325c6ba43583430cda703a37ad5`.
- 이번 수납은 제공 보고서와 집계 CSV의 대조다. 보고서 작성자는 입력 평가 ZIP 원자료 9,216행·18MP4를 CPU로 검사했다고 기록했다. 이 Git 수납에서 해당 입력을 재집계·재디코딩한 것과 구분한다.

## 정책↔학습 Run 연결

| 표기 | OFFICIAL source training Run | 평가 checkpoint / SHA | 선택 기준 |
|---|---|---|---|
| A 부모 | `20261009-142350-h1-actrate-0001-fresh3k` | model2700 / `e54d3389…93ca7ae` | fresh3K 자동 best; 마지막 keeper2950과 다름 |
| B 무변경 | `20261014-111135-h1-actrate-0001-unchanged-cont2k` | model4699 / `722b35a1…48f646` | 같은 부모에서 reward 유지 +2K endpoint |
| C 복원 | `20261014-142200-h1-actrate-return2700-2k` | model4650 / `a8249db4…25b84ea` | 같은 부모에서 action -0.0001→-0.0005; endpoint4699 이전 선택본 |

[ACTRATE Experiment](../../../../../research/experiments/h1/exp-h1-action-rate-relaxation.md) · [복원 Experiment](../../../../../research/experiments/h1/exp-h1-action-rate-restoration.md). 학습 Run·reward·부모는 외부 registry/publication에 의한 연결이며 평가 원문 source_run_id/preset=null과 resume imported-parent provenance=false/null을 변경하지 않는다. C는 옛 lin=.65 resume model4650/SHA `ce7ad586…`과 다르다. LINTRACK065 fresh4950과 TERM-50 control2800은 이번 비교에 포함되지 않는다.

## 비교 결과와 현재 판단

| H5 rough / 384 episode | A 부모2700 | B 무변경4699 | C 복원4650 |
|---|---:|---:|---:|
| body 진행 mean/P05/min (m) | 9.948/9.592/8.815 | 7.919/7.427/6.239 | 8.769/7.970/4.845 |
| mixed tracking 평균 (단일 물리단위 없음) | .17811 | .18596 | .19816 |
| 최대 stall fraction | .023 | .074 | .386 |
| 이번 대표 후보 판단 | HOLD | **범용·전진/험지 대표에서 REJECT** | HOLD |

- B는 A보다 대응 H5 **384/384건 진행 감소**(평균 -2.029m). 기존 단독 HOLD에서 이번 세 후보의 범용·전진/험지 대표 선정에 한해 REJECT로 갱신한다. 학습 COMPLETED/PASS를 FAILED로 바꾸거나 원본을 폐기한다는 뜻은 아니다.
- C는 B보다 **373/384건 진행 증가**, 평균 +0.850m·P05 회복. 그러나 **283/384건 mixed tracking 악화**, 최소 진행 6.239→4.845m, 최대 stall .074→.386으로 꼬리가 나빠졌다. 같은 키 seed4201/env60은 A/B/C 진행 9.710/7.997/4.845m다.
- C도 A보다 H5 **381/384건 진행 감소**. A는 rough 기준, C는 정지·횡복귀·action 변화량 참고 후보로 유지하며 **PROMOTE 없음**.
- H1 정지 world XY 잔차 A/B/C는 2.011/.692/.304m, H3 횡왕복은 .669/.581/.167m. C의 작은 복귀 잔차가 더 좋은 vy 추종을 뜻하지 않는다(H3 vy 절대오차 A/B/C .0673/.0682/.0771m/s).
- 전체 episode 가중 mixed tracking은 A/B/C .145339/.137377/.140944로 B가 가장 낮지만 rough 진행 손실을 가린다. 모든 정책 3,072/3,072 timeout 생존은 명령 이행·지형 완주 증거가 아니다.

수치는 [rough 대응 방향 CSV](../../../incoming/other/reviewed/H1_ACTRATE_PARENT_UNCHANGED_RESTORATION_COMPARISON_20261015/csv/rough_paired_direction.csv)와 [보고서](../../../incoming/other/reviewed/H1_ACTRATE_PARENT_UNCHANGED_RESTORATION_COMPARISON_20261015/H1_ACTRATE_PARENT_UNCHANGED_RESTORATION_REPORT_20261015.md)의 근거다. 기존 세 단독 보고서의 주요 숫자와 충돌은 보고되지 않았고, 새 직접 비교가 B의 판단 범위를 좁혔다.

## 검증 경계·남은 비교

제공 parity JSON은 A/B/C의 protocol, source fingerprints, task config, resolved config 및 cohort keyset 일치를 기록한다. 각 3,072 최초 cohort·8 case·3 evaluator seed는 독립 학습 반복이 아니며 같은 물리 지형/궤적을 보장하지 않는다. 자동 best 부모2700·endpoint4699·선택4650 차이 및 train-side 전체 source/PPO 미독립검증 때문에 **reward 인과효과는 미확정**, 공식 점수 예측도 하지 않는다.

보고된 capture artifact는 A stairs 502/1000, B rough 501/1000 black이며 다른 16영상은 시작 한 프레임 black이다. 유효 프레임에 기반한 contact sheet 관찰은 camera-off 평가와 별개이고 중앙 다단 계단 완주·물리 토크를 증명하지 않는다.

이번에 **A/B/C CPU 원자료 비교 대기는 해소**됐다. 옛 lin=.65 resume4650(`ce7ad586…`) 대 B도 이후 [다음 가설 보고서](./2026-10-15_H1_NEXT_HYPOTHESIS_DECISION_INTAKE.md)에서 기존 파생 CSV 수준으로 비교됐다(직접 원 episode 재집계 아님). LINTRACK065 fresh4950과 TERM-50 비교는 별개다. 자동 추가 학습·평가·제출 승인이 아니며 과거 보고서 원문은 역사적 판단으로 그대로 보존한다.
