> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/planning/historical/README.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# 과거 계획·운영안 보존 자료

여기 있는 파일은 당시 받은 권장안과 내부 설계의 정리본입니다. **현재 명령·제출·정책 상태를 지시하는 문서가 아닙니다.** 현재 운영은 AI 핵심팩〔원본 참조: `../../ai_library/00_START_HERE_CONTEXT_AND_MAP.md` / 공개 사본 미포함〕, [Experiment registry](<../../EXPERIMENTS.md>), [현행 planning INDEX](<../INDEX.md>)를 우선합니다.

- [01_SOLUTION_BLUEPRINT.md](<01_SOLUTION_BLUEPRINT.md>): 초기 구현 로드맵
- [02_PRIVATE_SERVER_VALIDATION_DESIGN.md](<02_PRIVATE_SERVER_VALIDATION_DESIGN.md>): 초기 PERSONAL 평가환경 설계
- [03_NVIDIA_SERVER_OPERATIONS.md](<03_NVIDIA_SERVER_OPERATIONS.md>): 이전 개인 서버 운영안
- [04_OPTUNA_REWARD_SEARCH_DESIGN.md](<04_OPTUNA_REWARD_SEARCH_DESIGN.md>): 초기 Optuna reward 탐색 설계 — 현재 구현·readiness는 AI library `15`를 우선한다.
- [05_PROJECT_STATUS_AND_EVIDENCE_BASED_STRATEGY.md](<05_PROJECT_STATUS_AND_EVIDENCE_BASED_STRATEGY.md>): 2026-08-24 상태·전략 snapshot — 명시적으로 superseded
- [06_H1_OFFICIAL_SERVER_BASELINE_DIAGNOSTIC.md](<06_H1_OFFICIAL_SERVER_BASELINE_DIAGNOSTIC.md>): 2026-08 H1 baseline 300회 당시 진단 절차 — 현재 OFFICIAL 실행 지시가 아님.
- [07_H1_SECOND_RUN_PARAMETER_COMPARISON_PLAN.md](<07_H1_SECOND_RUN_PARAMETER_COMPARISON_PLAN.md>): 2026-08-24 2차 reward 비교 계획 — 명시적으로 superseded
- [2026-09-10_H1_OFFICIAL_TRAINING_CHECKLIST.md](<2026-09-10_H1_OFFICIAL_TRAINING_CHECKLIST.md>): 과거 H1 공식 운영 체크리스트. 당시 후보·PLANNED 문구를 현행 상태로 사용하지 않는다.
- [09_NCRC_V1_IMPLEMENTATION_AND_LIMITS.md](<09_NCRC_V1_IMPLEMENTATION_AND_LIMITS.md>): 폐기된 v1 내부 orchestration 기록 — 명시적으로 superseded

- [2026-09-27_H1_PERSONAL_FRESH_AND_CONTINUATION_PLAN.md](<2026-09-27_H1_PERSONAL_FRESH_AND_CONTINUATION_PLAN.md>): 당시 H-005/H-010 세 PERSONAL Run의 실행 전 비교 계획; 이후 완료된 실제 Run과 근거는 [registry](<../../EXPERIMENTS.md>)를 따른다.

원래 Git blob SHA와 링크 영향은 이동 계획표〔원본 참조: `../../../../docs/reorganization/2026-10-12_FILE_MOVE_PLAN.md` / 공개 사본 미포함〕에 남겼습니다. `01`–`03`은 동일 바이트 보존본이며 생성기의 다시 만든 버전은 `../_generated/` (빌드 이후 생성; 빌드 전에는 폴더가 없을 수 있음)로 별도 관리합니다. `05`는 이 폴더 위치에서 작동하도록 **내부 상대 링크만** 조정했습니다.
