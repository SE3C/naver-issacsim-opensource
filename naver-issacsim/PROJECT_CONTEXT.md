# AI 프로젝트 컨텍스트

## 목적과 역할

NAVER CONNECT Robotics Cup의 Isaac Sim/Isaac Lab 교육·코드·원본·실험·평가 자료를 **근거를 보존하며 조회**하는 프로젝트다. 이 파일은 안정적인 해석 규칙과 자료 위치만 유지하며, 날짜별 학습·제출 현황이나 점수는 별도 canonical 문서로 안내한다.

- **Analysis (`naver-issacsim`)**: 문서·실험 registry·제출 snapshot·AI 핵심팩.
- **Originals (`naver-issacsim-originals`)**: 원본·공식/개인 raw evidence·해시·아카이브.
- **NVIDIA (`naver-issacsim-nvidia`)**: 개인 환경의 현재 training task source; 실제 실행 commit을 Run별로 확인한다.
- **Eval (`naver-issacsim-eval`)**: PERSONAL Windows 영상·사후 평가 도구와 새 PC 평가 Release.
- **`issacsimz`**: 별도 Codeberg 공개 sidecar. OFFICIAL에서는 제공된 `/workspace/training`을 사용하고 공식 서버에서 GitHub 접근·게시를 하지 않는다.

## 읽기 순서와 신뢰 기준

1. **현재 Experiment/Run 및 제출 상태**: [research/EXPERIMENTS.md](research/EXPERIMENTS.md), [명명 규칙](research/EXPERIMENT_NAMING.md), [동결 설정/미완료 항목](research/submission_presets/README.md). 가장 먼저 변경 시각과 PERSONAL/OFFICIAL/제출/채점을 구분한다.
2. **AI 질문의 시작점**: [AI 핵심팩 00](data/processed/ai_library/00_START_HERE_CONTEXT_AND_MAP.md). `00`을 포함한 핵심팩 **전체 21개**는 [업로드 안내](docs/AI_LIBRARY_GUIDE.md)를 따른다. 과거 `09`는 [별도 reference](data/processed/reference/game_engine/09_GAME_AGENT_NAVIGATION_SENSORS.md)다.
3. **실행된 코드 확인**: PERSONAL은 NVIDIA checkout의 실행 당시 commit, OFFICIAL은 해당 Run evidence에 기록된 주최 측 `/workspace/training`이다. 현재 source라는 이유로 과거 Run의 코드를 소급 확정하지 않는다. [NVIDIA 기준](https://github.com/SE3C/naver-issacsim-nvidia/blob/main/CURRENT_SOURCE.md).
4. **원본과 파생 자료**: Originals `data/raw`를 원본으로, `data/processed/`를 변환·분석본으로 구별한다. 외부 분석은 제공된 관찰과 분석자 추론을 분리한다. 오래된 server_backup과 planning은 기록 당시 snapshot/권장안이다. [자료 구조](docs/DATA_LAYOUT.md).
5. **실행·보존·평가 안내**: [11 서버](data/processed/ai_library/11_SERVER_OPERATIONS.md), [19 evidence CLI](data/processed/ai_library/19_ISSACSIMZ_EXTERNAL_EVIDENCE_CLI.md), [21 Windows 평가](data/processed/ai_library/21_WINDOWS_GO2_VIDEO_AND_EVALUATION.md), [Release 분류](docs/RELEASE_TAXONOMY.md).

## AI 해석 규칙

- **Experiment**는 검증 질문, **Run**은 개별 학습이다. checkpoint/부모·seed·source commit·resolved config·평가 조건을 확인하고, legacy `H/G/HS/GS/Rxx` 별칭은 원본 검색용으로 남긴다.
- PERSONAL 실험·사후 평가, OFFICIAL 학습·증거, 실제 제출 및 채점은 서로 다른 단계다. 평가 COMPLETE, 정책 품질 HOLD/PROMOTE, 제출 여부를 자동 연결하지 않는다.
- 파일명이나 `model_best` 이름만으로 정책·계보를 확정하지 않는다. 제출 snapshot의 actor SHA 일치, native checkpoint index, 부모 경로와 unknown provenance를 구분한다.
- 영상·이미지·웹 자료는 실제 관찰한 범위만 설명한다. 장면을 보지 않았다면 본 것으로 말하지 않고, 20초 생존을 장애물 완주로 바꾸지 않는다.
- 강의는 교육자료, `codebase`는 이전 수집본, `server_backup`은 snapshot이다. 코드 질문에는 실제 파일·함수명과 실행 버전을 표시한다. [기존 코드 수집본 이름 주의](data/processed/codebase/README.md).
- 대회 규정·제출 조건은 [12 통합 규정](data/processed/ai_library/12_2026_UNIFIED_REGULATIONS.md)과 최신 공식 공지를 우선한다. `practice_key.bin`, credential, `.env*`, Git 내부 데이터·바이너리를 추측하거나 외부 게시하지 않는다.
- 사용자가 명시하지 않은 GPU 학습·평가, export, Release 게시, 원본 삭제, 서버 종료를 하지 않는다. **OFFICIAL 서버는 AI가 종료하지 않는다**.

## 이력 보존

이전 파일에 적힌 날짜별 정책별 수치와 판단은 [2026-10-12 정리 전 전체 문서](docs/archive/PROJECT_CONTEXT_20261012_PRE_CLEANUP.md)에 남겼다. 그 안의 상태는 당시 기록이며 새 상태는 registry와 해당 Run/evaluation/submission 자료를 확인한다. 비슷한 자료를 새 파일로 옮겼다는 이유만으로 해당 Run이 검증 완료된 것은 아니다.
