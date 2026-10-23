# Optuna PC Ask/Record/Tell v2 수납 — 개선본 수신, 운영 최적화는 미준비

## 출처와 검증

- [Originals 원본 ZIP](https://github.com/SE3C/naver-issacsim-originals/blob/main/data/raw/external_analysis/h1/2026-10-15_optuna_pc_ask_tell_v2/NCRC_OPTUNA_PC_ASK_TELL_V2_20261015.zip): 148,755 bytes, SHA-256 `10f341f4beff8cde96b47ecf9d5b74c77fa1d813d6edd6554ef5f64f13f38c0d`.
- 수신 [20개 파일](../incoming/other/reviewed/NCRC_OPTUNA_PC_ASK_TELL_V2_20261015/)을 bytes 그대로 보존했다. ZIP CRC PASS, 내부 [manifest](../incoming/other/reviewed/NCRC_OPTUNA_PC_ASK_TELL_V2_20261015/MANIFEST_SHA256.json)의 19개 크기·SHA 일치. 이전 전달본도 수신 ZIP 안 `source_originals/`에 있다.
- [외주 보고서](../incoming/other/reviewed/NCRC_OPTUNA_PC_ASK_TELL_V2_20261015/improved_pc_optuna_v2/REPORT_ko.md), [사용법](../incoming/other/reviewed/NCRC_OPTUNA_PC_ASK_TELL_V2_20261015/improved_pc_optuna_v2/README.md), 실제 app.py/config의 핵심 분기를 정적으로 대조했다. 프로그램·수신 테스트를 실행하거나 설치하지 않았다.

## 코드에서 확인한 변화

| 이전 검토 문제 | v2 정적 확인 | 남는 경계 |
|---|---|---|
| 요청마다 동일 seeded sampler 재생성 | 프로세스 내 stage별 sampler 재사용; 재시작 시 stage·기존 trial 수에서 seed 유도 | RNG state 복원·무중단과 동일한 경로·후보 고유성 보증 아님 |
| evaluator→Tell→다음 Ask 결합 | 명시 Ask/Record/Tell/Abandon 및 DB 상태 조회 분리; loopback 기본·강제 | 실제 evaluator 자동 실행·서버 연동은 없음 |
| score/objective·trial 연결 부족 | 단일 유한 objective_value, frozen contract, 수동 evidence·부모/조건·중복 검사 | SHA 형식과 입력 일치 검사이며 실제 checkpoint bytes·입력 진실성 인증 아님 |
| anchor/LOG 보정값을 objective로 사용 | 진단 전용 HTML로 격리, 운영 Tell 경로에서 제외 | 보정 점수의 공식 예측력·정책 성능이 검증됐다는 뜻 아님 |

기본 [study_config.json](../incoming/other/reviewed/NCRC_OPTUNA_PC_ASK_TELL_V2_20261015/improved_pc_optuna_v2/study_config.json)은 **objective=null, comparison=null**이다. 후보 Ask·수동 진단 Record·조회·Abandon은 구현돼 있으나 **Tell 차단 / 실제 최적화 준비 미완료**다. Ask 전용 초기 후보를 TPE 최적화의 성공적 추천으로 부르지 않는다. 기존 9차원 탐색 범위는 미승인 legacy 범위이고 action=-.0001이 범위 밖이라는 제한도 유지한다. 실제 사용 범위·목적함수·비교 조건을 확인하기 전에 운영 study/trial을 만들지 않는다.

## 제공 테스트와 미검증

[TEST_RESULTS.json](../incoming/other/reviewed/NCRC_OPTUNA_PC_ASK_TELL_V2_20261015/improved_pc_optuna_v2/tests/TEST_RESULTS.json)과 stdout은 외주 CPU sandbox에서 Python 3.13.5/Optuna 4.8.0/Node 22.16.0, Python 구문 검사·**12개 unittest**·UI 정적 검사·참고 HTML JS 구문 검사 모두 exit0를 기록한다. 이 버전과 통과는 외주 실행 기록이며 이번 로컬 수납의 독립 재실행 결과가 아니다. 합성 DB/관측을 실제 H1 완료 trial로 이전하지 않는다.

Windows 실기·브라우저 동작·실제 평가 ZIP adapter와 지표 매핑·objective 타당성·입력 policy/evaluator bytes·다른 Optuna 버전은 미검증이다. SQLite가 기준이며 JSONL은 보조 기록, 단일 프로세스만 지원한다. 요청 중단 시 RUNNING/orphan을 조회해 수동 처리해야 하며 자동 복구/재시도·분산 사용을 보증하지 않는다.

## 채택 상태와 다음 조건

**개선본 수신·원본 보존·정적 검토 완료**, **설치·운영 검증·실제 Tell·성능 검증 미완료**로 구분한다. 실행 도구나 기존 Windows 평가기를 자동 교체하지 않는다. 다음 사용을 선택하면 개인 PC에서 (1) 범위·기준 reward, (2) 출처·단위·집계·방향이 명확한 단일 목적함수, (3) 동일 protocol/source·fresh/resume·부모·학습량·seed·checkpoint selector, (4) 실제 관측과 config identity를 먼저 확인한다. 목적함수 변경은 기존 stage를 바꾸지 않고 새 stage로 분리하는 구현이다.

[운영진 허용](../incoming/other/reviewed/2026-09-21_OPTUNA_PERSONAL_ASK_TELL_ORGANIZER_APPROVAL.md)은 PC Ask/Tell과 참가자의 직접 공식 reward 수정·학습이라는 경계다. 이번 수납은 공식 서버 설치·연동·GPU 실행이나 실제 study 생성을 승인하지 않는다. [이전 검토](./2026-10-15_OPTUNA_EXTERNAL_CPU_REVIEW_INTAKE.md) · [별도 H1 가설 권고](../experiments/h1/analysis/2026-10-15_H1_NEXT_HYPOTHESIS_DECISION_INTAKE.md).
