# 2026-10-12 Stage 3: incoming/experiments 분류와 보존형 이동 완료 기록

**적용 결과:** Analysis 검토 브랜치에 표의 2개 본문을 실제 이동하고 예전 경로에 각각 Markdown 탐색 안내를 남겼다. 주요 관련 AI/Research 문서 링크를 새 canonical 경로로 교체했다. `main` 미병합.

## 원칙

- 기존 `incoming/other/reviewed/`의 장문 사용자 수신 분석, `incoming/ot/` 원본 전사, `data/processed/experiments/`의 실측 분석·evidence 수신 문서, `reference/public/`의 dated snapshot, `research/experiments/`의 Run 계보는 이 단계에서 **이동하거나 재작성하지 않는다**.
- 대체된 **실행 전 계획**과 **일반 참고자료**만 아래 2건 선별 이동한다. 이전 경로는 안내 문서로 남기고 새 본문은 동일 Git blob 또는 위치 의존 링크만 수정한 버전으로 보존한다.
- `reviewed`라는 폴더 명칭은 상담 핵심팩 통합 완료가 아니며, 동일 정책의 후속 보고서라는 이유만으로 원문을 superseded로 판정하지 않는다.
- 문서 분류와 추가 탐색 색인은 상태 등록·새 Experiment/Run ID 발급·공식 성능 판정이 아니다.

## 이동 대상 파일별 계획

| 기존 경로 | 목표 경로 | 이동 전 Git blob SHA | 선별 이유 / 참조 영향 |
| --- | --- | --- | --- |
| `data/processed/reference/09_GAME_AGENT_NAVIGATION_SENSORS.md` | `data/processed/reference/game_engine/09_GAME_AGENT_NAVIGATION_SENSORS.md` | `80acfcd845897917f03db1bfd3692f3e70c7a822` | H1/Go2 현행 실행 근거가 아닌 게임 에이전트·경로계획 참고 요약. `reference/README`, AI `00`·`05`, `docs/AI_LIBRARY_GUIDE`에서 기존 경로 참조. 원문 내부 Markdown 상대 링크 없음. |
| `data/processed/experiments/h1/2026-09-27_H1_PERSONAL_FRESH_AND_CONTINUATION_PLAN.md` | `data/processed/planning/historical/2026-09-27_H1_PERSONAL_FRESH_AND_CONTINUATION_PLAN.md` | `b17fbc6bc60f819ae17c3db3de1376ca520c07af` | 이후 PERSONAL Run 3건이 완료된 **사전 계획**. 실행·evidence intake 기록은 원래 experiments에 유지. `research/EXPERIMENTS`, H-005/H-010, AI 14/15, evidence-intake에서 링크로 참조. 이동 문서 안의 상대 링크 4개는 새 위치 기준으로 보정. |

## 이동 제외·색인 작업

- `incoming/other/reviewed/`의 현재 사용자 보고서 **원문 전체**: 이동하지 않고 `README.md`에서 H1 / Go2 / 공식답변·공개자료 / 공통 / 확인 필요로 인덱싱한다. 이는 **파일명/출처에 기초한 탐색 분류**이며 integration status·원본의 진실성 판정이 아니다. 파일 링크를 전부 남기고 본문을 변경하지 않는다.
- `incoming/other/inbox/`: 원문 4개와 그 하위 폴더의 기존 README 1개를 포함한 5개 수신 대기·미검토 항목을 별도 README로 목록화한다. 자동 완료·이관 처리는 하지 않는다.
- `experiments/h1`, `experiments/go2`: 학습 근거·평가·제출 snapshot은 이동하지 않고 주제별 README로 찾아가도록 만든다. `go2` 그래프/CSV, `h1` 제출 manifest와 수치 JSON은 그 폴더에 둔다.
- `reference/public/`: 공개 사이트 관찰 스냅샷의 시점별 상태를 구분하며 archive/HTML/JSON byte를 유지한다.

## 전체 목록 색인 구현 결과

- `incoming/other/reviewed/README.md`: 수신 원문 63개를 파일명 기준 H1 33 / Go2 17 / 운영·공개자료 제목 10 / 공통·기타 3으로 분류해 **63/63 링크**를 검증했다. 원문 63개 byte는 바꾸지 않았다.
- `incoming/other/inbox/README.md`: 기존 수신 원문 4개와 하위 폴더 README 1개를 포함해 **5/5**를 보존·연결했다.
- `experiments/h1/README.md`: 기존 48개 파일을 원위치에 보존하고 제출 snapshot, 데이터, 평가, 학습 수신 기록 등으로 **48/48** 연결했다.
- `experiments/go2/README.md`: 기존 28개 파일(그래프 8개 및 그래프 폴더 README·CSV 포함)을 원위치 보존하고 **28/28** 연결했다.
- `incoming/other/README.md`, `reference/game_engine/README.md` 및 루트 README/데이터 레이아웃을 연결해 접근성을 개선했다.
- 위 카테고리는 단순 **파일명·확장자 분류**이며 canonical 상태 YAML이나 완료·제출 판단이 아니다. 누락을 발견하도록 읽기 전용 구조 검사 스크립트에 4개 폴더의 inventory 완전성 조건을 추가했다.

## 이동 후 본문 및 링크 검증

- `09_GAME_AGENT_NAVIGATION_SENSORS.md`: 이전/새 경로 Git blob SHA **동일** (`80acfcd845897917f03db1bfd3692f3e70c7a822`). 내부 Markdown 상대 링크 0개.
- `2026-09-27_H1_PERSONAL_FRESH_AND_CONTINUATION_PLAN.md`: 원본 Git blob `b17fbc6bc60f819ae17c3db3de1376ca520c07af`, 새 위치 `f8977bb804f25fc5f58f7fd042fba156efeca168`. 이동 후 텍스트를 이동 전 원문과 재비교해 **내부 Markdown 링크 4개를 위치에 맞게 조정한 것 외 완전히 동일**함을 확인했다.
- 전체 검토 브랜치의 **변경 Markdown 81개·상대 링크 960개**를 staged Git tree 대상으로 검사해 없는 파일 경로 0건. 마크다운 앵커 정합성, 외부 URL, 원본 ZIP 내용, 실제 생성기 full run은 검증 범위 밖.

## 호환 및 검증

1. 이전 경로 두 건에는 새 canonical 문서로 연결하는 짧은 Markdown 안내를 남긴다. **HTTP 자동 redirect가 아닌 탐색 링크**다.
2. Git blob SHA 및 본문의 링크 외 변경 여부 확인. 수신 원문·evidence·checkpoint·제출 파일의 변경 건수 0이어야 한다.
3. 관계 문서/AI source 메타데이터 및 README의 canonical 경로를 새 위치로 고친다. 과거 보고서 본문은 고치지 않아 이전 경로 안내가 호환되도록 한다.
4. 새 README의 분류 전체를 원격 tree의 실제 파일 집합과 대조하고 Markdown 상대 파일 링크를 확인한다.
5. 전체 재생성·Windows 평가·GPU 학습·Release·원격 서버 조작·병합은 승인 범위에 없다.
