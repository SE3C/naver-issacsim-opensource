# Optuna 도구 외주 검토 수납 — 최소 Ask/Tell 개선만 후속 요청

> **후속:** [v2 개선본 수납·정적 검토](./2026-10-15_OPTUNA_PC_ASK_TELL_V2_INTAKE.md)가 완료됐다. 아래는 최초 원본 검토·개선 요청 당시 기록이다. 개선본 수신과 실제 운영 최적화 준비는 별개이며 후자는 여전히 미완료다.

## 보존과 검토 범위

- [검토 원문](../incoming/other/reviewed/NCRC_H1_review_report_and_cpu_evidence_20261015/REVIEW_REPORT_ko.md) 및 [19개 산출물](../incoming/other/reviewed/NCRC_H1_review_report_and_cpu_evidence_20261015/README_ARTIFACTS.md)을 bytes 그대로 수납했다. [원본 ZIP](https://github.com/SE3C/naver-issacsim-originals/blob/main/data/raw/external_analysis/h1/2026-10-15_optuna_tool_cpu_review/NCRC_H1_review_report_and_cpu_evidence_20261015.zip)은 38,461 bytes, SHA-256 `e28e5748d99606b6c081435be49f7a49ee4632131ead8493e38ddcae4721cfa7`, CRC PASS다.
- 입력은 [기존 Optuna 도구 ZIP·별도 HTML·검토 프롬프트](https://github.com/SE3C/naver-issacsim-originals/tree/main/data/raw/external_analysis/h1/2026-10-15_optuna_external_review/received)이며 원문에 적힌 두 도구 SHA는 보존본과 일치한다. 도구를 수정한 결과가 아니라 **코드 검토와 합성 CPU 재현 결과**다.
- 외주 보고서는 Optuna 4.8.0/Python 3.13.5/Node 22.16.0에서 CPU 명령 4개 exit0를 기록한다([TEST_STATUS](../incoming/other/reviewed/NCRC_H1_review_report_and_cpu_evidence_20261015/TEST_STATUS.json)). 이번 수납은 원본 코드와 주요 결함을 정적으로 대조했으며 첨부 테스트·앱을 재실행하지 않았다. 실제 Windows 평가 ZIP, Isaac 환경, GPU·학습·영상·export 호환 검증은 없다.

## 확인한 핵심 결함과 채택 경계

| 원본 위치 | 코드에서 확인한 문제 | 최소 후속 방향 |
|---|---|---|
| `app.py:get_study` | 요청마다 같은 seed의 `TPESampler`를 새로 생성 | 요청 간 sampler 수명·재시작 정책 명시, 같은 초기 후보 반복 회귀 테스트 |
| `app.py:do_POST`, `safe_stage` | trial과 결과 identity를 연결하지 않고 score/objective를 각각 범위 검사; 서로 다른 stage 문자열 충돌 가능 | 명시 trial·고정 조건과 입력 결과 연결, 단일 objective 기준, stage 충돌 거부 |
| `index.html:runEvaluator`, `tellCurrentAndAskNext` | 자체 evaluator 완료 후 현재 UI 값으로 Tell하고 다음 Ask까지 연결 | 평가와 Optuna를 분리, 명시 Tell/Ask, 실패·중복·재시작 상태 확인 |
| UI calibration/LOG 계산 | 단일 TERM50 예시 anchor·근거 없는 LOG 보정이 objective에 섞이며 빈 입력/순위 역전 반례가 있음 | 자동 objective에서 제외, 원본 진단과 참고 보정을 구분 |

원본에 **공식 서버 자동 학습 구현이 있다는 뜻은 아니다**. 직접 발견한 것은 자체 로컬 평가→Tell 결합과 검증 누락이다. 외주 CPU의 합성 trial·fixture는 실제 Run이나 검증된 추천 성능이 아니다. 공식 56.37점 자체의 부정도 아니다. 그 공식 정책과 이 별도 worker 입력/프로토콜을 연결한 검증 없이 anchor를 일반화할 수 없다는 문제다.

## 판단과 다음 범위

**기존 외주 분석 세션에서 최소 개선 1회는 유용하다.** 분석 맥락과 CPU 반례를 재사용하되 sampler/Ask/Tell 신뢰성·loopback 실행·불완전 입력 차단까지만 먼저 구현하도록 한다. [전달 프롬프트](../../../docs/ai_prompts/Optuna_개선_기존세션_프롬프트_20261015.txt).

새 evaluator worker 개선·실행, 모든 계보를 묶는 대형 adapter, 9차원 자동 탐색·새 scalar 목적함수·공식 점수 예측은 이번 단계에서 제외한다. 탐색 범위는 명시 설정으로 분리하고 기존 study를 조용히 바꾸지 않는다. 실제 `action=-.0001` 값이 표현되지 않는 기존 범위는 알려진 제한이지만, 새 실제 탐색 범위를 자동 승인하지 않는다. Ask에서 알 수 없는 미래 Run ID를 요구하거나 만들어내지 않고, 결과 수납 시 확인 가능한 checkpoint/평가 identity와 별도 매핑한다.

현재 프로젝트의 **Windows PERSONAL 평가기와 저장된 결과는 유지**한다. 기존 결과 adapter는 실제 스키마를 확인한 뒤 별도 단계로 다룬다. field가 없으면 추정하지 않고 raw null/unverified를 유지한다. 목적함수·비교 조건이 승인되지 않으면 후보 생성/진단 기록까지만 가능하며 **Tell/최적화 readiness는 미완료**다. HOLD/REJECT를 임의 숫자 관측으로 바꾸지 않는다.

운영진 허용은 **개인 PC Ask/Tell → 참가자가 공식 reward 수정·학습 → 결과를 PC로 반입**하는 경계다([기존 승인 원문](../incoming/other/reviewed/2026-09-21_OPTUNA_PERSONAL_ASK_TELL_ORGANIZER_APPROVAL.md)). 이 수납은 실제 Optuna study/trial 생성, 새 학습·GPU·공식 서버 작업을 실행하거나 승인한 것이 아니다. [새 H1 가설 권고](../experiments/h1/analysis/2026-10-15_H1_NEXT_HYPOTHESIS_DECISION_INTAKE.md)와도 별개다.
