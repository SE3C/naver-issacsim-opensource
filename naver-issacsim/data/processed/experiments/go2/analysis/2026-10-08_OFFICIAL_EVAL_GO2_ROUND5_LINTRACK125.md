---
title: "g2-submit-5 / LINTRACK-125 — Go2 예선 5라운드 공식 평가"
environment: "OFFICIAL submission evaluation"
status: "received_user_transcribed_official_evaluation"
source: "data/processed/incoming/other/reviewed/SE3C_예선5라운드_Go2_공식평가_사용자전달원문_20261008.md"
source_sha256: "0ed34b8779f6c2dd4a2b0993459245148a18b1d58408ec8b54ddb1725ae80c02"
received_date: "2026-10-08"
submission_time_as_displayed: "2026-10-06 01:10"
submission_timezone: "not specified in source"
submission_preset: "g2-submit-5"
source_run_id: "20260929-154342-go2-lintrack-125-fresh7500-official"
source_checkpoint: "model_7450.pt"
source_checkpoint_sha256: "b8766030e306dd72160d37292539575d5a1d92c2757f34637dafab3c1582343a"
---

# [분석] g2-submit-5 / LINTRACK-125 — Go2 예선 5라운드 공식 평가

> 관리 안내 (2026-10-13): **분석** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](../../../../../research/EXPERIMENTS.md)를 확인한다.

## 출처와 제출 연결

사용자가 2026-10-08 채팅으로 전달한 공식 평가 이미지·진행 현황 HTML의 전사를 [수신 원문](../../../incoming/other/reviewed/SE3C_%EC%98%88%EC%84%A05%EB%9D%BC%EC%9A%B4%EB%93%9C_Go2_%EA%B3%B5%EC%8B%9D%ED%8F%89%EA%B0%80_%EC%82%AC%EC%9A%A9%EC%9E%90%EC%A0%84%EB%8B%AC%EC%9B%90%EB%AC%B8_20261008.md)에 보존했다. 이번 수신은 원본 HTML·이미지 파일의 독립 검증이 아니라 사용자 전달 공식 결과 기록이다. 화면의 제출 시각은 **2026-10-06 01:10**이며 시간대는 추가로 추정하지 않는다.

이미 보존된 [Round-5 제출 snapshot](https://github.com/SE3C/naver-issacsim/releases/tag/submission-go2-prelim-r5-20261006)과 [intake manifest](../2026-10-06_PRELIM_R5_SUBMISSION/submission_manifest.json)에 연결한다. 제출 actor 8개가 OFFICIAL fresh 7.5K Run의 terminal `model_7450.pt`와 일치하고 env도 해당 학습 기록과 일치한다는 기존 검증을 유지한다. 자동 best `model_7050.pt`와 혼동하지 않는다. 당시 manifest·checksum·제출 파일은 사후 수정하지 않는다. 이번 결과는 새로운 학습 Run이나 새로운 preset 생성이 아니다.

## 공식 점수

| 항목 | 5라운드 | 3라운드 | 차이 |
| --- | ---: | ---: | ---: |
| 시뮬레이션 / 70 | **58.32** | 58.55 | −0.23 |
| 설계 의도 분석 / 20 | **20** | 19 | +1 |
| 리포트 품질 / 10 | **10** | 10 | 0 |
| 종합 / 100 | **88.32** | 87.55 | **+0.77** |

[3라운드 공식 기록](../2026-09-20_SE3C_PRELIM_R3_GO2_EVALUATION_AND_ORGANIZER_REPLY.md)과 비교한 산술 차이다. 종합 점수 상승을 시뮬레이션 성능 상승으로 표현하지 않는다.

| 지형·시나리오 | 5라운드 / 배점 | 3라운드 | 차이 |
| --- | ---: | ---: | ---: |
| 평지 · 전진 속도 추종 | 8.86 / 10.5 | 8.87 | −0.01 |
| 평지 · 전방위 속도 추종 | 8.70 / 10.5 | 8.76 | −0.06 |
| 험지 · 거친 지형 | 11.82 / 14 | 11.80 | +0.02 |
| 경사 · ±20° | 8.89 / 10.5 | 8.88 | +0.01 |
| 계단 · 10–15 cm | 8.35 / 10.5 | 8.52 | −0.17 |
| 평지 + 밀침 · 회복 | 5.83 / 7 | 5.83 | 0 |
| 험지 + 무작위화 · 도메인 랜덤화 | 5.87 / 7 | 5.89 | −0.02 |
| 합계 | **58.32 / 70** | **58.55** | **−0.23** |

공식 시나리오 점수는 로컬 evaluator의 raw metric·proxy score와 별도 측정이다.

## 리더보드 시점 기록

**2026-10-08 15:21** 화면 업데이트 기준 SE3C는 **29위(10계단 하락)**, H1 **86.37/100**, Go2 **88.32/100**, 합계 **174.69/200**이다. 사용자 제공 snapshot이지 live 순위가 아니며, 순위 변동만으로 정책 악화를 추정하지 않는다.

## 리포트와 판단

이 결과와 “로컬 평가 점수는 올랐는데 공식 시뮬레이션은 떨어졌다”는 사용자 고민에 대한 후속 방향은 [평가 불일치·분석 판정 논의](../2026-10-08_GO2_LOCAL_OFFICIAL_EVALUATION_GAP_AND_ANALYSIS_POLICY.md)에 별도로 기록한다. 후속 [운영진 답변과 점수 구성 분석](../2026-10-08_GO2_R3_R5_OFFICIAL_SCORE_COMPONENTS_ORGANIZER_REPLY.md)은 공식 감점이 생존 악화가 아니라 추종 손실에서 주로 발생했음을 밝혔다. evaluator 수정이나 reward 인과효과를 규명한 결과는 아니다.

## 운영진 후속 답변 — Survival Rate와 Tracking Score

사용자 제공 DM에서 운영진은 R3/R5 공식 기록을 시나리오별로 확인했다고 답했다. DM의 절대 날짜는 미기재이며 [문의·답변 원문](../../../incoming/other/reviewed/GO2_R3_R5_SURVIVAL_TRACKING_ORGANIZER_DM_RECEIVED_20261008.md)을 보존했다.

- **계단:** survival **99.0%→99.8%**, Tracking Score **0.819→0.796**. 생존 이득 약 **+0.07점**보다 추종 손실 약 **−0.24점**이 커 **8.52→8.35**가 됐다.
- **전방위 추종:** survival 두 정책 **100%**, Tracking Score **0.834→0.829**, 점수 약 **−0.06**.
- **나머지 다섯:** survival **100%**로 같고 R5 도메인 랜덤화만 **99.9%**. tracking 차이는 **0.003 이하**, 각 점수 차이는 **±0.02 이내**이며 개별 tracking 값은 미제공이다.

학습은 변하는 난이도와 행동 탐색 무작위를 포함하지만, 자동평가는 고정 시나리오에서 그 행동 무작위 없이 측정한다. 학습 contact 종료율을 `1−contact`로 공식 survival에 환산하지 않는다. 이번에는 공식 계단 survival도 개선됐다는 별도 확인이 있다. 공개된 반올림 survival/tracking이나 약 기여값으로 공식 표시 점수·미공개 변환식을 다시 만들지 않는다.

제출한 기술 개선 리포트·공식 AI 코멘트는 [수신 원문](../../../incoming/other/reviewed/SE3C_%EC%98%88%EC%84%A05%EB%9D%BC%EC%9A%B4%EB%93%9C_Go2_%EA%B3%B5%EC%8B%9D%ED%8F%89%EA%B0%80_%EC%82%AC%EC%9A%A9%EC%9E%90%EC%A0%84%EB%8B%AC%EC%9B%90%EB%AC%B8_20261008.md)에 전문을 보존했다. 공식 코멘트는 모든 시나리오를 보통 등급으로 설명하며 변경 목적과 구체적 학습 결과 기록을 평가했다. 설계 의도·리포트 품질은 각각 만점이다.

리포트의 계단 상행 `0.282→0.156`·하행 `0.359→0.141`은 별도 조건의 PERSONAL paired evaluator tracking error이며 공식 계단 점수의 개선을 의미하지 않는다. 이번 공식 계단 점수는 `8.52→8.35`다. PERSONAL 개선 신호, 공식 제출 총점, 공식 시뮬레이션 결과를 구분한다. 이 결과만으로 개별 reward 인과효과나 다음 학습 설정을 확정하지 않으며 기존 reward-effect HOLD를 변경하지 않는다.

원본 evidence·checkpoint·제출 snapshot·과거 분석 본문은 보존한다. 포털 제출 policy/env를 재다운로드·재 hash한 기록이나 독립 receipt 파일은 이번 작업에 추가하지 않았다.
