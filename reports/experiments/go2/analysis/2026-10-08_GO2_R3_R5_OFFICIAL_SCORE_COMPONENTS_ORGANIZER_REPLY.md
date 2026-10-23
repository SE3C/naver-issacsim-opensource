---
title: "Go2 R3/R5 운영진 답변 — 계단 생존 개선과 추종 점수 손실"
status: "organizer_reported_official_score_components; behavioral_mechanism_unresolved"
recorded_date: "2026-10-08"
source: "data/processed/incoming/other/reviewed/GO2_R3_R5_SURVIVAL_TRACKING_ORGANIZER_DM_RECEIVED_20261008.md"
source_sha256: "8a7a6341b0b348f1b5c5b37dd81ef64bd15d31058ae9afee732819b5eb57308c"
source_calendar_date: "unspecified; pasted timestamps say yesterday 17:54 and 21:52"
source_access: "user-provided DM transcription; no independent Discord or evaluator-log read"
scope: "official result interpretation and analysis guidance; no code or GPU work"
---

> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/experiments/go2/analysis/2026-10-08_GO2_R3_R5_OFFICIAL_SCORE_COMPONENTS_ORGANIZER_REPLY.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.


# [분석] Go2 R3/R5 운영진 답변 — 계단 생존 개선과 추종 점수 손실

> 관리 안내 (2026-10-13): **분석** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](<../../../../research/EXPERIMENTS.md>)를 확인한다.

## 핵심 결론

**공식 시뮬레이션 점수 하락은 계단 생존율 악화가 아니라 추종 점수 손실이 주된 항목이었다.** 운영진은 두 제출의 평가 기록을 확인해 계단 생존율이 `99.0%→99.8%`로 개선됐지만 Tracking Score가 `0.819→0.796`으로 낮아졌다고 답했다. 안정성 개선은 공식 평가에서도 관찰됐으나 최종 계단 점수는 `8.52→8.35`로 하락했다.

사용자가 제공한 문의·운영진 답변 전문〔원본 참조: `../../../incoming/other/reviewed/GO2_R3_R5_SURVIVAL_TRACKING_ORGANIZER_DM_RECEIVED_20261008.md` / 공개 사본 미포함〕을 수신 형태대로 보존했다. 파일의 날짜는 이번 기록 날짜이며 DM의 실제 달력 날짜가 아니다. 원문의 “어제”를 임의의 절대 날짜로 바꾸지 않는다. 아래 수치는 운영진 답변 전사에 근거하며 공식 평가 원시 로그를 직접 조회한 결과는 아니다.

## 비교 대상과 공식 지표

- R3: `g2-submit-3 / LINTRACK-150-LINZ-2`, original `model_4800.pt` 계보.
- R5: `g2-submit-5 / LINTRACK-125`, terminal `model_7450.pt` 계보. 자동 best `model_7050.pt`와 구분한다.
- 기존 공식 점수표〔원본 참조: `../2026-10-08_OFFICIAL_EVAL_GO2_ROUND5_LINTRACK125.md` / 공개 사본 미포함〕: 시뮬레이션 `58.55→58.32 / 70`(−0.23), 종합 `87.55→88.32 / 100`(+0.77). 종합 상승과 시뮬레이션 하락을 섞지 않는다.

| 공식 시나리오 | Survival Rate R3→R5 | Tracking Score R3→R5 | 시나리오 점수 R3→R5 | 운영진의 설명 |
| --- | --- | --- | --- | --- |
| 계단 10–15 cm | **99.0%→99.8% (+0.8%p)** | **0.819→0.796 (−0.023)** | **8.52→8.35 (−0.17)** | 생존 개선 약 +0.07점보다 추종 손실 약 −0.24점이 컸음 |
| 전방위 속도 추종 | 100%→100% | 0.834→0.829 (−0.005) | 8.76→8.70 (−0.06) | 생존이 같은 상태에서 추종 점수 감소 |
| 나머지 5개 | 두 제출 100%; R5 도메인 랜덤화만 99.9% | 각 차이 0.003 이하; 개별 값 미제공 | 각 차이 ±0.02점 이내 | 큰 변화 없음; 개별 Tracking Score를 역산하지 않음 |

나머지 다섯 시나리오는 전진 속도 추종·거친 지형·경사·밀침 회복·도메인 랜덤화다. 정확한 각 점수는 기존 공식 점수표를 따른다. 계단 −0.17과 전방위 −0.06이 합해 순감소 −0.23이며 나머지 다섯의 표시 점수 차이 합은 0이다. 이는 **공식 점수의 구성 기여**이지 reward 변경의 인과효과나 실패 원인 비율이 아니다.

공개된 Survival/Tracking 값과 약 ±0.07/0.24 기여에는 표시 정밀도 한계가 있다. 이 값들을 다시 곱해 기존 공식 점수 `8.52/8.35`를 고치거나 더 정밀한 내부 값·완전한 공식 채점 함수를 추정하지 않는다. 평균 tracking error를 Tracking Score로 바꾸는 함수, 시나리오별 명령·세부 조건, 반복 평가 변동 폭은 이 답변에서도 제공되지 않았다.

## 학습 contact와 공식 survival을 구분

문의에 적힌 학습 몸통 접촉 종료율은 R3 `8.11%`(iteration 4800), R5 `6.23%`(후반 500회 평균)로 **집계 구간도 서로 다르다**. 운영진 설명상 학습은 curriculum으로 난이도가 변하며 행동 탐색 무작위를 포함하고, 자동평가는 고정 시나리오에서 그 행동 탐색 무작위 없이 측정한다. 이것을 평가 환경의 모든 무작위화가 꺼진다는 뜻으로 확대하지 않는다.

따라서 `1 − 학습 contact 종료율 = 공식 Survival Rate`로 계산하거나 둘의 동반 개선을 항상 보장하지 않는다. 이번 쌍에서는 계단 공식 survival도 실제로 개선됐다는 **별도의 운영진 확인**이 있다. 학습 contact 개선 자체가 공식 점수 하락의 원인이라는 해석도 맞지 않는다.

## 현재 분석 판단과 다음 확인 순서

1. **목표별 성패:** “계단 생존 안정성 개선”은 공식 지표에서 관찰됐다. “공식 계단 점수 개선”은 달성하지 못했다. “계단 추종 점수”는 감소했다. 둘을 합쳐 전면 실패나 전면 성공으로 부르지 않는다.
2. **다음 질문:** 개선된 계단 생존을 유지하면서 명령 속도 추종 손실을 회복할 수 있는가? 우선 R3 4800과 R5 7450의 실제 명령 대비 x/y/yaw-rate 오차와 진행·stall을 계단 상행/하행별로 확인한다. 운영진은 공식 `play.py`로 두 정책의 계단 명령 추종을 나란히 보라고 권했다. 영상의 단순 이동속도·활동성만으로 tracking을 판정하지 않는다.
3. **로컬 평가 역할:** PERSONAL tracking error 개선과 공식 Tracking Score 하락이 동시에 존재한다. 같은 지표·조건이라고 가정하지 말고 command·terrain·오차 정의·집계를 대조한다. 합산 proxy score나 낙상률 하나로 채택하지 않는다. 기존 자료를 먼저 사용하고 재실행은 별도 요청 범위에서만 한다.
4. **확인된 것과 남은 것:** 공식 점수의 survival/tracking 분해는 제공된 답변 기준으로 확인됐다. 왜 공식 tracking이 낮아졌는지, 어떤 reward 변경이 이를 일으켰는지, 로컬·공식의 어떤 조건 차이가 역전을 만들었는지는 아직 미확인이다. R3/R5는 reward와 학습량 등도 달라 단일변수 인과 비교가 아니다.
5. **유지할 경계:** 과거 PERSONAL 후보 판단은 그 프로토콜 한정이고 공식 정책 우열로 확대하지 않는다. `LINTRACK-125` reward-effect HOLD, 원본 보고서·frozen preset·제출 snapshot·evidence는 유지한다. 이 답변 한 쌍에 맞춰 evaluator 가중치·calibration·Optuna objective를 재설계하거나 다음 reward를 자동 결정하지 않는다.

이 문서는 기존 로컬·공식 차이 논의〔원본 참조: `../2026-10-08_GO2_LOCAL_OFFICIAL_EVALUATION_GAP_AND_ANALYSIS_POLICY.md` / 공개 사본 미포함〕의 “공식 감점 구성 미확인”을 후속 답변으로 갱신한다. 새 학습 Run·submission preset·GPU 작업·Release 변경·평가기 코드 변경을 뜻하지 않는다.
