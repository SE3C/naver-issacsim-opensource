# 가공 자료 — 위치별 탐색

자료는 **용도 → 로봇/주제 → 날짜별 문서** 순서로 찾는다. 현재 상태는 [Experiment registry](../../research/EXPERIMENTS.md), 전체 배치 규칙은 [DATA_LAYOUT](../../docs/DATA_LAYOUT.md)을 따른다.

| 찾는 자료 | 입구 | 경계 |
| --- | --- | --- |
| 상담용 요약 | [AI 시작 문서](ai_library/00_START_HERE_CONTEXT_AND_MAP.md) | 전체 원문이나 현재 Run 상태 DB가 아님 |
| 수신 원문·미검토 자료 | [incoming](incoming/README.md) | 수신 파일명·bytes 보존; reviewed ≠ 반영 완료 |
| 학습·평가·제출 해석 | [experiments](experiments/README.md) | 실제 측정·계보·원문 링크를 보존 |
| 게시·설치·검증 기록 | [operations](operations/README.md) | 실행 성공·정책 채택·현재 설치 상태와 구분 |
| 계획과 과거 운영안 | [planning](planning/INDEX.md) | 옛 계획은 historical; 현재 상태는 registry |
| 공식·공개·게임 참고 | [reference](reference/README.md) | 공지 해석·날짜별 관찰이며 내부 Run이 아님 |
| 외부 미디어 요청·보고서 | [external_analysis](external_analysis/README.md) | 원문 요청 ID·영상 ID 유지 |

**강의 자료 주의 (2026-10-14):** `lessons/`의 기존 Markdown 22건은 원본 저장본과 대조한 결과 6건의 강의 번호·제목 오연결, 9건의 로딩 화면 전용 본문이 포함되어 있다. 이 15건은 정상 강의 내용으로 인용하지 않는다. [22건 파일별 출처·복구 장부](../../docs/reorganization/2026-10-14_LECTURE_SOURCE_PROVENANCE.md)를 먼저 확인한다.

`lessons/`, `glossary/`, `codebase/`, `server_backup/`는 [생성기 소유 범위](../../docs/DATA_LAYOUT.md#생성물과-관리-문서의-소유권)에 속한다. 원본 archive·checkpoint·영상의 보존 위치는 인접한 Originals이며, 분류를 위해 이 폴더로 옮기지 않는다.
