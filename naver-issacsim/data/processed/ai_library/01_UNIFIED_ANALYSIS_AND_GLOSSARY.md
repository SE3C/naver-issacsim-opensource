---
title: "프로젝트 통합 분석과 용어집"
purpose: "AI upload bundle — 저장소의 역할·근거·용어를 빠르게 연결"
sources:
  - "../naver-issacsim-originals/data/raw/server_backup/extracted/training/"
  - "data/processed/server_backup/reports/"
  - "data/processed/server_backup/code/"
  - "data/processed/reference/"
---

# 프로젝트 통합 분석과 용어집

## 핵심 결론

이 저장소는 대회 제출 환경을 재구성하거나 결과를 검증하기 위한 분석 기반이다. **공식 서버에서만 제출 정책을 학습**하며, 개인 NVIDIA 서버와 여기의 연습 엔진은 코드 이해·검증·실험 기록에만 사용한다.

## 자료를 읽는 순서

1. `12_2026_UNIFIED_REGULATIONS.md`: 허용 범위·제출·일정 판단.
2. `05`·`11`: 예선 실험 루프와 서버 운영 습관 (OT 판단은 여기로 흡수).
3. `05`~`07`: 예선 reward 학습·파일·검증.
4. `08`~`09`: 본선 연습 엔진과 에이전트의 구현 구조.
5. `10`~`11`: 개인 서버 검증 환경과 개발 우선순위.

## 저장소 역할

| 위치 | 역할 |
| --- | --- |
| `naver-issacsim-originals` | 원본 HTML·영상·에셋·원시 코드 보존. 현재 H1/Go2 source는 `server_backup/extracted/training/`의 2026-09-13 공식 snapshot이다. |
| `data/processed/reference` | 공식 문서의 분석·추출본. |
| `data/processed/server_backup` | 과거 서버 백업에서 읽을 수 있게 정리한 코드·상세 보고서. 최신 실행 source가 필요할 때는 Originals canonical snapshot을 우선한다. |
| `data/processed/ai_library` | 상담 AI용 압축 판단 문서. 원문 전문을 두지 않는다. |
| `data/processed/incoming` | 새 자료의 전사·교차검증·상세 분석을 보관하고 핵심팩 반영 전 검토하는 곳. |

## 구현 사실과 제안의 구분

- 서버 백업 코드에서 직접 읽힌 클래스·함수·파일은 **구현 사실**이다.
- `10`, `11`의 실험 순서·검증 환경·설계안은 **권장안**이다.
- OT 설명은 **운영 맥락**이고, 규정·공지와 충돌하면 규정·최신 공지가 우선한다.
- 예전 경로명이나 백업 코드의 키·URL·업로드 구현은 현재 운영 지시가 아니다.

## 최소 용어

| 용어 | 의미 |
| --- | --- |
| policy | 관측을 받아 로봇 명령을 내는 학습 정책. 제출본은 `policy.pt`를 기준으로 확인한다. |
| reward | 정책이 어떤 행동을 선호하게 할지 정의하는 보상 항목·가중치. |
| env.yaml | 학습 환경과 reward 설정의 기록. 제출 정책의 의도와 대조하는 근거다. |
| play | 체크포인트를 실행해 실제 동작·영상으로 확인하는 단계. |
| checkpoint | 학습 중 저장된 후보 모델. 항상 최종 제출 정책은 아니다. |
| observation | 정책·에이전트가 현재 상태를 이해하기 위해 받는 수치·센서 정보. |
| waypoint | 경로계획 결과의 중간 목표점. 저수준 정책이 직접 따라갈 수 있는 속도 명령으로 변환된다. |

## AI 응답 규칙

- 실험·제출 정책을 부를 때는 현재 이름/제출 preset/reward descriptor를 먼저 쓴다. 현재 Go2 실제 제출은 `g2-submit-5 / LINTRACK-125`이며, 직전 Round-3 기준 제출은 `g2-submit-3 / LINTRACK-150-LINZ-2`다. `g2-submit-5`는 OFFICIAL fresh 7.5K의 terminal `model_7450.pt`에서 export됐고 사용자가 2026-10-06 실제 제출 완료를 보고했다. Release의 policy actor는 native 7450과 exact-match이고 env는 OFFICIAL training record와 일치하지만 2026-10-08 사용자 전달 공식 평가에서 제출 시각 2026-10-06 01:10(시간대 미기재), 종합 88.32/100(시뮬레이션 58.32/70·설계 의도 20/20·리포트 품질 10/10)을 수신했다. 별도 포털 receipt 파일은 미보유다. track-only `LINTRACK-125`의 fresh 3K와 7.5K는 첫 3K trajectory exact match 덕분에 3K→7.5K를 같은 single-seed/config의 학습량 비교로 읽되 BASE 대비 reward 인과효과로 바꾸지 않는다. `G-001`, `G-005`, `A1`, `G5` 같은 legacy alias는 원문 검색·계보 해소에 필요할 때만 괄호로 짧게 병기하고 본문 주어·제목으로 반복하지 않는다.
- 불확실한 규정·일정은 단정하지 말고 공식 공지 확인을 안내한다.
- 코드 수정 요청이면 먼저 최신 Originals canonical training 또는 현재 NVIDIA `training/`에서 실제 파일·함수 위치를 확인한다. processed server backup은 과거 구현·분석 확인용이다.
- 개인 서버에서 학습한 정책을 제출하는 경로는 제안하지 않는다.
