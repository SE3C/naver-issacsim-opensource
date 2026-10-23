# v2.0.0 변경 요약 — 2026-10-15

| 대상 | 원본 결함 | 개선 |
|---|---|---|
| `app.py` sampler | HTTP 요청마다 동일 seed로 새 TPE 생성, 초기 벡터 반복 | stage별 프로세스 수명 캐시; 재시작 시 stage+기존 trial 수 기반 seed. 정확한 RNG stream 재현은 보장하지 않음 |
| Ask/Record/Tell | 단일 `tell-and-ask`로 완료와 신규 Ask 결합 | `/api/ask`, `/api/record`, `/api/tell`, `/api/abandon` 분리; `/api/study` SQLite 조회 |
| 상태·identity | stage 이름 정규화 충돌, 증거 연결 없음 | ASCII stage strict reject, 동결 계약 해시/Optuna attrs, trial별 수동 evidence+diagnostic SQLite 저장, FAILED 상태 |
| scalar | score/normalized objective 모순 가능, 미입력/가짜 0 | 오직 하나의 필수 `objective_value`; finite JSON number/승인 범위; HOLD·REJECT는 숫자화하지 않음 |
| 운영 안전 | 로컬 worker 호출·평가→Tell 및 `0.0.0.0` shell 바인딩 | 평가 시작·결합 API 폐쇄, 메인 실행파일에서 evaluator 분리, 127.0.0.1만 허용, 자동 pip 설치 제거 |
| calibration/LOG | 검증 전 proxy가 Optuna 입력으로 전달 | 메인 UI 계산 제거; 별도 HTML은 단일 anchor/heuristic 비운영 진단이라고 명시, 존재하지 않는 CLI 안내 중단 |
| 탐색 범위 | 코드 안 고정 9차원, 실제 -0.0001 제외 | `study_config.json`에 **원본 범위 그대로** 이동. 사용자가 설정한 새 stage에서 고정값/별도 범위 가능; 기존 study는 자동 재구성 불가 |
| 품질 검증 | 선행 외주 보고서 CPU 반례만 존재 | 새로운 v2 실제 서비스 대상 HTTP/서브프로세스/재시작/SQLite 합성 12테스트 + UI 스크립트 구문/정적 검사 |

**변경하지 않음:** 원본 ZIP의 evaluator source/worker, 실제 reward/학습/Isaac 구성. 본 개선본에는 evaluator를 호출하는 실행 경로 자체가 없으며 원본 source는 배포의 `source_originals` ZIP 안에 bytes 그대로 보존했다. 구현하지 않음: Windows 평가 ZIP 실어오기·metric adapter·evaluator worker 개선·학습/GPU/영상/export·공식 서버 연동.
