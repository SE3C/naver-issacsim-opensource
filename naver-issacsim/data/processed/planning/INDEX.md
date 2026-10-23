# 대회 준비 전략·검증·서버 운영 자료

## 현재 탐색 구조

- [과거 계획·운영안](./historical/README.md): 역사적·대체된 초기 설계와 과거 운영 절차를 분리 보관한다. 이전 주소의 간단 안내는 기존 참조를 찾는 용도이며 최신 실행 기준은 아니다.
- 이 폴더 루트의 `01`~`09`는 과거 주소 안내이고, 실제 과거 문서는 `historical/`에 보관한다. 날짜별 가설 문서는 registry를 기준으로 판단한다. 폴더 위치만으로 실행 여부를 확정하지 않는다.

## 분류

- [NCRC 2026 정책·본선 전략 구현 청사진](./historical/01_SOLUTION_BLUEPRINT.md): historical/planning blueprint. 정책 평가기·보상 튜닝·체크포인트 선택·전략 계층의 초기 개발 로드맵이며 현재 상태/운영 기준은 아님
- [예선 대비 개인 NVIDIA 서버 검증환경 설계안](./historical/02_PRIVATE_SERVER_VALIDATION_DESIGN.md): historical validation design. 초기 평가전용 개인서버 설계이며 현재 PERSONAL 학습/증거 운영 경계는 AI library `11/16/19`를 따름
- [예선 대비 개인 NVIDIA 서버 운영안](./historical/03_NVIDIA_SERVER_OPERATIONS.md): historical operations design. 현재 PERSONAL/OFFICIAL 역할·실행·게시 경계는 AI library `11/19`를 따름
- [Optuna 기반 reward 탐색 설계](./historical/04_OPTUNA_REWARD_SEARCH_DESIGN.md): pre-implementation design. 현재 readiness/objective/실행 여부는 AI library `15`를 따름
- [프로젝트 현황과 증거 기반 실행 전략](./historical/05_PROJECT_STATUS_AND_EVIDENCE_BASED_STRATEGY.md): **historical/superseded 2026-08-24 snapshot**. 당시 완료·미완료 상태와 실행 순서 기록이며 현재 상태는 registry/PROJECT_CONTEXT를 따름
- [H1 공식 서버 기준선 진단 가이드](./historical/06_H1_OFFICIAL_SERVER_BASELINE_DIAGNOSTIC.md): baseline 무변경 검증, 300-iteration 측정, 로그·GPU·산출물 수집 절차
- [H1 2차 공식 서버 reward 비교 실험 계획](./historical/07_H1_SECOND_RUN_PARAMETER_COMPARISON_PLAN.md): **historical/superseded** 2026-08-24 계획. 누락 로그 재수집과 `termination_penalty` 단일 변경의 paired 비교 설계 기록
- [2026-09-10 H1 공식 학습 운영안](./historical/2026-09-10_H1_OFFICIAL_TRAINING_CHECKLIST.md): 과거 checklist snapshot. 현재 실행·후보 선택은 registry와 AI 운영 문서를 따름
- [H1 예선 2라운드 공식 평가](../experiments/h1/2026-09-10_OFFICIAL_EVAL_H1_ROUND2_TERM50.md): TERM50 제출 86.37/100. 시나리오 실점 있음. 요철 최저 비율, 전진 최대 공백, 회전은 고른 보통
- [Historical NCRC v1 record (superseded)](./historical/09_NCRC_V1_IMPLEMENTATION_AND_LIMITS.md): 이전 NVIDIA 내부 orchestration 기록. 현재 실행·evidence 도구는 AI library `19`의 공개 `issacsimz`를 따른다.
- [H1 300-iteration 실제 결과 분석](../experiments/h1/2026-08-24_OFFICIAL_SERVER_300ITER_BASELINE.md): 첫 실행에서 확인된 환경·reward·지형·산출물과 누락된 진단 증거
- [H1 개인 서버 `termination_penalty=-50` 25k 검증 기록](../experiments/h1/2026-08-25_PERSONAL_SERVER_TERMINATION_M50_25K.md): 개인 NVIDIA/Brev 장기 실행의 검증된 지표와 공식 결과로 해석하지 않는 한계
- [H1 finalize/report 버그 검토](../experiments/h1/2026-08-26_H1_FINALIZE_REPORT_BUG_REVIEW.md): full scalar와 자동 선택 불일치, checkpoint 삭제 위험, 다음 export 규칙

## 읽는 순서

1. **지금 실제로 진행할 작업**은 [Experiment registry](../../../research/EXPERIMENTS.md)와 [AI 핵심팩 00](../ai_library/00_START_HERE_CONTEXT_AND_MAP.md), 해당 운영 문서로 확인한다.
2. 초기 구현·개인 평가기·서버 운영을 이해할 필요가 있을 때만 [과거 설계 모음](./historical/README.md)의 `01`–`03`을 읽는다. 과거 권장안을 현재 실행 근거로 사용하지 않는다.
3. evaluator와 objective의 현재 구현 상태가 확인된 후에만 `04` Optuna 설계를 과거 제안으로 참고한다.
4. `05`는 historical status snapshot으로만 읽고, 현재 상태·다음 행동은 `research/EXPERIMENTS.md`와 `PROJECT_CONTEXT.md`에서 확인한다.
5. 2차 reward 비교 계획은 historical 설계 예시로만 읽고 현재 실행 후보를 거기서 고르지 않는다.
6. 과거 체크리스트를 현재 복붙 명령으로 쓰지 않는다. 필요한 보존·판정 원칙은 현행 운영 문서와 대조하고 현재 reward 후보는 `research/EXPERIMENTS.md`를 따른다.
7. 개인/공식 학습 보존은 `issacsimz` 사용 문서(AI library `19`)로 범위를 확인한다. 공식 server smoke는 운영자 검증 전까지 미완료로 유지한다.

## 신뢰 규칙

- `백업 확인` 또는 코드 상수는 현재 `training`·`practice_sim` 원본과 교차검증한다.
- `권장`, 예시 score, curriculum, 시간 배분은 실행 제안이며 공식 규정이 아니다.
- 학습 가능 장소, 제출 조건, 총 GPU 시간, Isaac Sim 버전은 최신 대회 공식 공지를 우선한다.
- credential, practice key, backend 정보는 외부 AI나 공개 저장소에 제공하지 않는다.
