# 2026-10-13 — 가공 문서 배치·이름 정리

기존 Draft PR의 후속 정리다. 생성된 학습·평가 evidence나 사용자 수신 원문은 이동하지 않고, 수동 가공 문서 네 건만 선별했다. 기존 `main`에는 적용하지 않는다.

## 실제 이동·이름 변경

| 이전 경로 | 새 경로 | 이동 전 Git blob | 근거 |
| --- | --- | --- | --- |
| `data/processed/planning/08_H1_OFFICIAL_TRAINING_OPS_CHECKLIST.md` | `data/processed/planning/historical/2026-09-10_H1_OFFICIAL_TRAINING_CHECKLIST.md` | `a3ecf98b6fc8ca7575bb9353ac95dfda38712d25` | 9/10 작성 운영안에 과거 후보·PLANNED 표기가 남아 있음. 현행 실행 절차와 분리 |
| `data/processed/operations/windows_go2_video_evaluation/model4800_release_notes.md` | `data/processed/operations/windows_go2_video_evaluation/2026-10-09_G2_SUBMIT-3_MODEL4800_EVALUATION_RELEASE_NOTES.md` | `2e768d68934446cc59a6ce367e4c367c88043942` | ZIP 날짜·제출 preset·PERSONAL 평가 용도가 본문에 확인됨 |
| `data/processed/operations/windows_go2_video_evaluation/model7050_release_notes.md` | `data/processed/operations/windows_go2_video_evaluation/2026-10-04_LINTRACK-125_MODEL7050_EVALUATION_RELEASE_NOTES.md` | `b8861a0dcb644825babff59d8cfd4d5a75b89f0f` | ZIP 날짜·descriptor·PERSONAL 평가 용도가 본문에 확인됨 |
| `data/processed/reference/official/2026_briefing_qna_analysis.md` | `data/processed/reference/official/2026-08-14_OFFICIAL_BRIEFING_QA_ANALYSIS.md` | `2d4f2217c162944fd167be159cf928f29e3e0354` | metadata의 source_date 기준. 공식 Q&A 해석이며 원본 HTML이 아님 |

옛 Markdown 주소 네 곳에는 짧은 탐색 안내를 유지한다. HTTP redirect나 원문 중복 사본이 아니다. 세 이름 변경 문서는 본문을 그대로 보존하고, checklist만 역사적 문맥 안내와 깊이가 바뀐 상대 링크 한 곳을 보정한다. 과거 본문에 적힌 결과·후보·명령은 다시 작성하지 않는다.

## 참조·확장 처리

- checklist: planning INDEX/history 안내를 새 위치로 연결한다. 과거 Round-2 분석의 본문 참조는 기존 경로 안내로 호환하며 원문은 고치지 않는다.
- model7050: registry의 게시 노트 링크만 새 주소로 바꾼다. model4800은 기존 G-005 기록에 게시 노트를 연결한다. Run ID·상태·수치는 변경하지 않는다.
- Q&A: AI 12의 `sources` 경로와 reference 안내만 갱신한다. 핵심팩 이름·파일 수·내용 판단은 그대로다.
- 새 `data/processed/README.md`와 `operations/`·로봇별 README는 위치 안내와 파일 목록만 제공한다. 상태 DB나 새 evidence가 아니다. 도구 설치 JSON도 당시 snapshot임을 구분하며 물리적으로 옮기지 않는다.
- [DATA_LAYOUT](../DATA_LAYOUT.md)에 새 수동 문서 배치·날짜/대상/종류 파일명·이전 주소 호환 원칙을 짧게 모았다. 루트 README의 오래된 원문 분류 집계는 장부 참조로 바꿨다.
- 읽기 전용 구조 검사에 새 안내·이동 파일·운영 폴더 목록을 추가해 누락·깨진 상대 경로가 검사되게 했다. 생성기는 실행하거나 변경하지 않는다.

## 이동 제외

완료된 H1/Go2 실험 분석, 현재 네 조합 질문이 남아 있는 10/10 계획, 수신 원문, 제출 snapshot, Release/검증 JSON, source checkout, archive/checkpoint/영상은 그대로 둔다. 오래됐다는 이유만으로 결과·미실행 질문을 historical로 일괄 이동하지 않는다. 공식 팁처럼 전달 원문이 포함된 문서도 이번에는 이름을 바꾸지 않는다.

검증은 로컬 본문 보존 대조·링크/목록·구조 검사에 한정한다. GPU·서버 실행, 외부 Release 내용 변경, 원격 자료 재검증, Downloads 배포, PR 병합은 하지 않는다.

## 검증 결과

- 게시 노트 두 건과 Q&A의 새 파일 Git blob이 이동 전 값과 각각 일치한다. 운영안은 역사 안내 한 문단과 상대 링크 한 곳을 제외하면 본문이 같다.
- 검사기 구문 검사와 구조 검사 통과: 핵심팩 21개, 문서 99개, 로컬 상대 링크 1,062개, 오류 0건. 이동 파일까지 포함한 기본 `git diff --check`는 기존 운영안의 Markdown 줄바꿈용 끝 공백 10곳을 경고한다. 본문 보존을 위해 그대로 두고, `core.whitespace=-blank-at-eol`로 그 끝 공백만 제외한 변경 검사도 통과했다.
- 메모리상의 실패 fixture 세 건도 확인했다. 필수 문서 누락, 운영 색인에서 JSON 링크 누락, 옛 경로 안내의 깨진 링크를 각각 FAIL로 판정했다. 실제 원본 파일을 훼손해 테스트하지 않았다.
- 수신 원문·evidence·JSON·제출 preset·학습 코드는 변경하지 않았다. 서브에이전트가 이동 범위와 운영 색인을 독립 검토했고, 누락됐던 G-005 문서의 링크 검사도 추가했다.
