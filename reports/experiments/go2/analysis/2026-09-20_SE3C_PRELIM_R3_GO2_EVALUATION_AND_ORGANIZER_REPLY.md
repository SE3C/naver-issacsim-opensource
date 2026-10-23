---
title: "SE3C 예선 3라운드 Go2 평가와 운영진 답변 요약"
environment: "OFFICIAL submission evaluation"
status: "verified_received_evaluation_record"
source: "data/processed/incoming/other/reviewed/SE3C_예선3라운드_Go2_평가_및_운영진답변_20260920.md"
source_sha256: "f4403f34e5b6fe71ca9ff5756ca8652082048dc204bb8829010685588938d68f"
---

> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/experiments/go2/analysis/2026-09-20_SE3C_PRELIM_R3_GO2_EVALUATION_AND_ORGANIZER_REPLY.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.


# [분석] SE3C 예선 3라운드 Go2 평가와 운영진 답변 요약

> 관리 안내 (2026-10-13): **분석** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](<../../../../research/EXPERIMENTS.md>)를 확인한다.

## 범위와 원문 경계

수신 원문은 2026-09-16 07:33에 제출한 Go2 `policy.pt`·`env.yaml`의 평가와 이후 운영진 문의·답변을 함께 기록한다. 원문은 변경하지 않고 reviewed incoming〔원본 참조: `../../../incoming/other/reviewed/SE3C_예선3라운드_Go2_평가_및_운영진답변_20260920.md` / 공개 사본 미포함〕에 SHA-256 `f4403f34…8d68f`로 보존한다. 이 문서는 그 평가 사실과 향후 보고서 작성 규칙만 분리해 요약한다.

기존 G-005 Run 07의 official original-4800 submission snapshot과 결합해 해석한다. 수신 평가 기록은 실제 Round-3 결과를 제공하지만, 개인 fixed evaluator·native 영상의 수치를 official scenario별 원인 증명으로 바꾸지는 않는다.

## 확인된 평가 결과

| 항목 | 결과 |
| --- | ---: |
| 종합 | **87.55 / 100** |
| 시뮬레이션 | **58.55 / 70** |
| 설계 의도 분석 | **19 / 20** |
| 리포트 품질 | **10 / 10** |

| 평가 시나리오 | 점수 / 배점 |
| --- | ---: |
| 전진 속도 추종 | 8.87 / 10.5 |
| 전방위 속도 추종 | 8.76 / 10.5 |
| 거친 지형 | 11.80 / 14 |
| 경사 ±20° | 8.88 / 10.5 |
| 계단 10–15 cm | 8.52 / 10.5 |
| 밀침 회복 | 5.83 / 7 |
| 도메인 랜덤화 | 5.89 / 7 |

이 점수는 original `model_4800.pt` actor와 matching `env.yaml`으로 만든 G-005 Run 07 제출 snapshot의 **공식 제출 평가 결과**다. 4800 대 recovery-4900의 개인 비교는 정책 선택 당시의 보조 근거였고, 이 단일 공식 결과를 multi-seed 일반화 또는 각 reward 항의 독립 효과로 확장하지 않는다.

## 기술 개선 리포트에서 유지할 원칙

- `ang_vel_xy_l2 -0.08 → -0.12`의 악화와 원복, 이후 두 reward를 함께 바꾼 G-005 조합, fresh run의 4837 부근 중단, original 4800과 recovery 4900의 비교·선택을 실제 설정과 결과에 맞게 그대로 구분한다.
- 두 reward를 동시에 바꾼 G-005는 조합 가설이지 두 항의 개별 인과 증명이 아니다.
- 남은 접촉률·생존율·traversal 한계를 숨기지 않는다. 원복한 실패와 residual problem을 정확히 쓰는 것이 설정·결과 불일치보다 안전하며, 이번 리포트 품질은 10/10이었다.
- 운영진은 설계 의도 분석 19/20의 정확한 단일 판정 요인은 AI 평가라 특정할 수 없다고 답했다. 해소되지 않은 문제가 남아 있으면 만점이 아닐 수 있다는 해석만 기록하며, 임의의 감점 원인을 확정하지 않는다.
- 운영진은 다음 라운드도 현재의 구체적 기록 방식을 유지하라고 안내했고, 만점이 아닐 때의 이유를 4라운드부터 평가문에 남기는 방향을 검토한다고 답했다.

## 의사결정

G-005 Run 07은 실제 official score를 받은 제출 결과로 갱신한다. 이 결과는 original-4800 제출 snapshot의 provenance·선택이 실제 평가로 이어졌음을 확인한다. 다만 다음 가설의 reward 결정에는 scenario별 부족분, fixed evaluator의 multi-seed/worst-terrain 검증, 그리고 변경 항목을 분리한 ablation을 계속 사용한다.

후속 R3/R5 운영진 DM 답변〔원본 참조: `../2026-10-08_GO2_R3_R5_OFFICIAL_SCORE_COMPONENTS_ORGANIZER_REPLY.md` / 공개 사본 미포함〕에서는 R3 original 4800 대비 R5 terminal 7450의 계단 survival **99.0%→99.8%**, Tracking Score **0.819→0.796**을 확인했다. 생존 이득보다 추종 손실이 커 공식 계단 점수는 **8.52→8.35**로 하락했다. 이 후속 구성 설명은 당시 제출·원문·reward 인과 판단을 소급 변경하지 않는다.
