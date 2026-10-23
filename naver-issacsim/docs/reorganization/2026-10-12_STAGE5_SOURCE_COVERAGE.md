# Stage 5 원본 수신 보고서 참조 조사 기록

2026-10-12 Analysis Draft 브랜치에서 수신 원문 63개의 후속 문서 발견 상태를 확인하고 읽기 전용 보조 장부를 추가했다. 이 과정에서 원문 보고서, 평가 ZIP, 근거 JSON, Submit YAML 또는 Experiment/Run status를 변경하지 않았다.

- [63건 전체 원문별 추적표](../../data/processed/incoming/REPORT_PROVENANCE_TRIAGE.md): 기존 12쌍 관계표 등재 12, 별도 source_report 명시 7, 정확한 파일명 언급 27, 후속 직접 연결 미확인 17.
- 별도 source_report와 파일명 참조의 근거 수준을 구분했으며, source 파일의 Git blob SHA로 원본 동일성 확인이 가능하도록 했다.
- 범위는 일부 H1/Go2 분석·Experiment·운영 문서. 저장소의 모든 Markdown·외부 Release·실제 ZIP/영상까지 대조했다고 주장하지 않는다.
- 미확인 원문은 삭제·중복·superseded로 처리하지 않으며, raw 보고서와 user-provided evidence를 그대로 보존한다.

## 반영 후 정적 검사

- 신규 장부에서 원문 링크 63개를 **63개 서로 다른 파일**에 연결했으며, 장부의 상대 Markdown 링크 총 **111개**는 검토 브랜치 Git tree에 모두 존재한다.
- `main`과 이 Draft 브랜치의 `incoming/other/reviewed/` 기존 63개 사용자 보고서 **Git blob SHA 동일(변경 0개)**. 파일명·서술 자체를 축약·교체·분류 폴더로 이동하지 않았다.
- 루트 AI 핵심팩 최상위 Markdown **21개** 유지, 파일 삭제 없음. 새 관계 장부와 실행 검사 수정은 noncanonical Markdown/읽기 전용 체크 범위다.
- 범위 제약: 외부 URL·Markdown 앵커, raw ZIP·영상, 실제 Run/GPU/evaluator, 전체 JS 구조 검사 런타임 실행 및 원격 서버 확인은 수행하지 않았다.

## 2026-10-13 보류 항목 후속 대조

위 집계는 10/12 최초 조사 기록으로 유지한다. 당시 보류 17건을 세 영역으로 나눠 읽기 전용 대조한 후, 메인 검토에서 `sources`/본문 원문 경로 15건과 날짜·checkpoint/산출물 문맥 연결 2건을 장부에 추가했다. OCR 가공 문서의 명시적인 수신 원문 경로도 확인했다. 연결 미발견은 0건이지만 전체 반영 완료 판정은 아니다.

현재 집계는 [추적 장부](../../data/processed/incoming/REPORT_PROVENANCE_TRIAGE.md) 한 곳을 기준으로 삼고, 수신 README와 관계 색인의 반복 숫자를 제거했다. 9/24·9/26 답변 범위, 9/13·9/14 Go2 Run, 날짜별 공개 snapshot, 보고서 관찰과 영상 독립 검증을 구분했다. 원본 63건·Git blob SHA와 Experiment/Run 상태는 변경하지 않는다.

후속 검증: 원문 링크 63개는 모두 고유하며 기록 SHA가 커밋된 원본 Git blob과 일치했다. 원문·registry 변경은 없고, `git diff --check`와 `node tools/check_knowledge_structure.js`가 통과했다(핵심 문서 21개, 대상 문서 85개, 상대 링크 989개). 로컬 파일의 줄바꿈과 Git blob 바이트는 구분하며 외부 URL·실제 ZIP/영상 검증은 수행하지 않았다.
