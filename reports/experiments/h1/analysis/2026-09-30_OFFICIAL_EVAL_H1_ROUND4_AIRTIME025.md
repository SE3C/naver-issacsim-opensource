---
id: h1-official-eval-round4-airtime025-20260930
source_type: reviewed_official_evaluation
category: official_evaluator_result
robot: H1
reviewed_at: '2026-09-30'
round: '예선 4라운드'
submission_preset: 'h1-submit-4'
display_descriptor: 'AIRTIME-025'
trust_level: user_provided_official_result_text_with_per_scenario_scores
authority: '사용자가 전달한 공식 평가 결과다. 순위는 이 문서에 없다.'
source: 'data/processed/incoming/other/reviewed/SE3C_예선4라운드_H1_평가_20260930.md'
---

> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/experiments/h1/analysis/2026-09-30_OFFICIAL_EVAL_H1_ROUND4_AIRTIME025.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.


# [분석] H1 예선 4라운드 공식 평가 — h1-submit-4 / AIRTIME-025

> 관리 안내 (2026-10-13): **분석** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](<../../../../research/EXPERIMENTS.md>)를 확인한다.

## 범위와 원문 경계

이 문서는 사용자가 전달한 예선 4라운드 H1 공식 평가 결과를 2·3라운드 기록과 같은 구조로 정리한다. 수신 원문은 reviewed incoming〔원본 참조: `../../../incoming/other/reviewed/SE3C_예선4라운드_H1_평가_20260930.md` / 공개 사본 미포함〕에 보존한다.

평가 대상은 기존 submission snapshot `h1-submit-4 / AIRTIME-025`에 연결한다. 기존 provenance상 이 제출은 OFFICIAL `AIRTIME-025` fresh 10K evidence Run `20260927-123428-h005-fresh10k-official`(legacy H-005 R05; `termination_penalty=-50`, `track_lin_vel_xy_exp=0.5`, `feet_air_time=0.25`)과 연결되지만, 제출 `policy.pt`의 정확한 numbered source checkpoint는 별도 근거 없이 새로 확정하지 않는다.

## 확인된 평가 결과

| 항목 | 결과 |
| --- | ---: |
| 시뮬레이션 | **56.37 / 70** |
| 설계 의도 분석 | **20 / 20** |
| 리포트 품질 | **10 / 10** |
| 구성 점수 합계 | **86.37 / 100** |

사용자가 전달한 원문에는 별도의 "종합 점수" 필드가 없었다. 따라서 `86.37 / 100`은 위 세 구성 점수의 산술 합계이며, 원문에서 독립적으로 표시된 종합 필드라고 표현하지 않는다.

## 시뮬레이션 세부 점수

| 지형 | 평가 시나리오 | 점수 / 배점 |
| --- | --- | ---: |
| 평지 | 제자리 균형 | 8.58 / 10.5 |
| 평지 | 전진 속도 추종 | 11.34 / 14 |
| 평지 | 좌우 속도 추종 | 5.72 / 7 |
| 평지 | 회전 복합 추종 | 5.68 / 7 |
| 요철 | 약한 요철 | 8.00 / 10.5 |
| 경사 | 완만한 경사 ±10° | 8.53 / 10.5 |
| 평지 + 밀침 | 밀침 회복 | 8.52 / 10.5 |
| | **합계** | **56.37 / 70** |

세부 시나리오 7개의 합은 전달된 시뮬레이션 점수 `56.37 / 70`과 일치한다.

## 제출 리포트에서 확인되는 실험 설명

제출 리포트는 다음 흐름을 기록한다.

- 기본 1K에서 terrain 0·낙상률 100%를 관찰했다.
- `termination_penalty -5 → -50`로 강화한 공식 5K에서 terrain 약 5.8, episode length 약 800까지 개선했다고 기록했다.
- 이후 `feet_air_time 0.20 → 0.25`를 추가 변경하고 나머지 7개 값은 유지했다고 설명했다.
- OFFICIAL fresh 10K를 이어학습 없이 처음부터 수행했다고 기록했다.
- 최고 보상 약 5.4 @ 9784, terrain 약 5.8, 최종 낙상률 25.7%, 후반 500회 평균 XY error 0.36, yaw error 0.88, 몸통 접촉 종료율 25.9%를 기술했다.
- 6개 지형 영상에서 지속적인 낙상 없이 이동했고 박스·역계단·불규칙 요철 구간에서 계속 전진했다고 제출 리포트에 적었다.

위 문장은 **제출 리포트에 적힌 주장**을 보존한 것이다. 기존 프로젝트 원칙대로 loose 영상이나 제출문만으로 정확한 checkpoint identity 또는 fixed evaluator 성능을 새로 확정하지 않는다.

## 공식 AI 코멘트

> 모든 시나리오에서 등급이 보통으로 고르게 나왔습니다. 낙상 벌점과 발 체공 보상을 조정한 이유와 단계별 실험 과정, 그리고 최종 학습 지표와 영상 관찰 결과를 구체적인 수치와 함께 충실하게 기록했습니다.

## 현재 기록 판정

- Round-4 제출은 **공식 평가 결과 수신 완료**로 갱신한다.
- 시뮬레이션: `56.37 / 70`
- 설계 의도 분석: `20 / 20`
- 리포트 품질: `10 / 10`
- 구성 점수 합계: `86.37 / 100`
- 7개 시나리오 모두 공식 점수 기록이 있다.
- 이 결과는 `h1-submit-4 / AIRTIME-025` submission snapshot에 귀속한다.
- 이 한 번의 공식 평가를 `feet_air_time 0.25`의 단독 인과효과나 다른 checkpoint의 점수로 확장하지 않는다.

## 연결 자료

- 수신 공식 평가 원문〔원본 참조: `../../../incoming/other/reviewed/SE3C_예선4라운드_H1_평가_20260930.md` / 공개 사본 미포함〕
- [`h1-submit-4 / AIRTIME-025` 계보 상세 (legacy H-005)](<../../../../research/experiments/h1/H-005.md>)
- [Round-4 submission snapshot](https://github.com/SE3C/naver-issacsim/releases/tag/submission-h1-prelim-r4-20260928)
- [OFFICIAL fresh 10K raw evidence](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20260927-airtime-025-fresh10k)
