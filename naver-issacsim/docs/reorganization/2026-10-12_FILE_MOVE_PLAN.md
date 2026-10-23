# 2026-10-12 파일별 이동 감사·실행 기록 — A+B 혼합 / historical 분리

**실행 상태:** 2026-10-12 Draft PR 검토 브랜치에서 아래 6개 문서를 실제 `planning/historical/`로 이동 완료. `main` 미병합. 옛 경로에는 자동 HTTP redirect가 아닌 탐색용 Markdown 안내 6개를 유지한다.

## 범위와 판정

사용자 선택 A(선별 이동)에 따라, B의 **오래된 자료를 물리적으로 분리**하는 목적을 반영한다. 다음 여섯 항목은 날짜가 오래됐다는 이유만이 아니라 `planning/INDEX.md` 및 각 파일이 명시적으로 역사/대체된 계획이라고 판정한 경우다. 이동 대상은 **Analysis의 가공·기획 Markdown만**이며 Originals 원본 `data/raw/planning/`, 수신 분석 원문, run evidence, 평가 수치, 제출 snapshot, NVIDIA training, Eval runner는 변하지 않는다.

## 파일별 이동 계획

| 기존 경로 (`data/processed/planning/` 아래) | 목표 (`historical/` 아래) | Git blob SHA (이동 전) | 판단 |
| --- | --- | --- | --- |
| `01_SOLUTION_BLUEPRINT.md` | `historical/01_SOLUTION_BLUEPRINT.md` | `19bf15e72035d32bd48c381dc9a25affda7ae2aa` | 과거 구현 로드맵, 현재 Run/운영 기준 아님 |
| `02_PRIVATE_SERVER_VALIDATION_DESIGN.md` | `historical/02_PRIVATE_SERVER_VALIDATION_DESIGN.md` | `03056dfa2b8905dcf51d8843946638d2645fdcd1` | 과거 개인 서버 평가전용 설계, 이후 PERSONAL 실제 용법과 구분 |
| `03_NVIDIA_SERVER_OPERATIONS.md` | `historical/03_NVIDIA_SERVER_OPERATIONS.md` | `8231803792029ac4ed003578405f633498caf20f` | 과거 운영안, 현행 OFFICIAL/PERSONAL 경계와 구분 |
| `05_PROJECT_STATUS_AND_EVIDENCE_BASED_STRATEGY.md` | `historical/05_PROJECT_STATUS_AND_EVIDENCE_BASED_STRATEGY.md` | `0f40ccfca9885ebb93303ae1a91ffde125b25de9` | superseded 2026-08-24 상태/전략 snapshot |
| `07_H1_SECOND_RUN_PARAMETER_COMPARISON_PLAN.md` | `historical/07_H1_SECOND_RUN_PARAMETER_COMPARISON_PLAN.md` | `d90970bbb4b0b964daa0526be4084bbada664d33` | 2026-08-24 H1 후속 계획; 실제 실행 이후의 현재 명령이 아님 |
| `09_NCRC_V1_IMPLEMENTATION_AND_LIMITS.md` | `historical/09_NCRC_V1_IMPLEMENTATION_AND_LIMITS.md` | `ff478895ba426f021a16285c43fd3d51127731fe` | 폐기된 NVIDIA 내부 v1 orchestration의 역사 기록 |

## 이동 전 링크 영향 확인 및 처리 (2026-10-12)

GitHub의 `main` code search를 여섯 basename으로 검색하고, 기존 검토 브랜치의 `INDEX`·`incoming/README`·관련 AI 문서를 대조했다. 검색은 **완전한 본문 전수 색인 보증이 아니므로**, 이전 경로를 바로 삭제하지 않고 모든 여섯 기존 위치에 소규모 안내/redirect Markdown을 남긴다.

- 공통: `planning/INDEX.md`에 여섯 개 링크가 있다 → **실제 새 경로로 변경**한다.
- `05`: `incoming/README.md`, 과거 수신 보고서 `incoming/other/reviewed/NCRC_2026_검증된_프로젝트_현황.md`에 참조가 있다. 현재 안내만 갱신하고 **수신 원문은 변경하지 않으며**, 옛 경로 호환 안내를 사용한다.
- `07`: AI `06`, `10`, `11`, `14`, `15`에서 참조한다. 상세 링크는 옛 경로에서 새 경로로 안내하며 원래 분석 단락과 당시 판단은 유지한다.
- `01`–`03`: 생성기 `tools/build_knowledge_base.js`가 기존 root planning 파일을 재생성하는 문제가 있다. **generated 출력은 `planning/_generated/`로 바꾸고, 수동 역사 문서와 옛 경로 안내를 덮어쓰지 않는다.**
- `09`: `planning/INDEX.md`에서 역사 링크로만 확인됐다.
- `05` 문서 내부 상대 Markdown 링크 7개는 새 디렉터리 깊이에 맞춰 **실제 이동 폴더 밖으로 향하는 상대 Markdown 링크 **3곳만** 보정**한다. 그 외 다섯 문서는 원래 Git blob을 그대로 새 위치에서 재사용한다.

## 호환성·보존 계약

1. 여섯 **기존 경로는 없애지 않았다**. 짧은 historical 안내 페이지를 두고 새 경로를 상대 링크로 가리킨다. 이는 과거 링크가 최소한의 찾아가기 기능을 갖도록 하는 것이며 GitHub HTTP 자동 301이 아니다.
2. `01`–`03`, `07`, `09`는 새 위치의 Git blob SHA **동일을 확인**했다. `05`는 기존 7개 상대 Markdown 링크 중 같은 historical 폴더 내 링크 4개를 그대로 보존하고, 외부를 향하는 3개만 새 위치에 맞춰 보정했다. 원래 blob `0f40ccfca9885ebb93303ae1a91ffde125b25de9`와 새 blob `71cee8f834975309044ca0de097af803f77a5b35`를 구분한다. 원래 blob SHA는 이 표와 Git history에 남긴다.
3. 이전 보고서의 출처 주장, Experiment/Run/status, 오래된 실행 예시를 현재 실행지시처럼 변환하지 않는다. `planning/04`, `06`, `08`, 날짜별 현재 가설은 이번 단계에서 **유지**한다.
4. move/redirect/index/generator를 같은 branch에 반영했다. 이동된 6개 문서의 상대 링크 7개는 Git tree상 모두 존재하며, 다른 다섯 문서의 SHA는 이동 전과 동일하다. 전체 문서 구조 검사·최종 링크 감사는 이 PR의 별도 검증 결과를 따른다.
5. 수신·실험·OFFICIAL/제출 원본 전체는 디렉터리별 일괄 이동하지 않았다. 다음 이동 그룹도 이 형식의 파일별 감사 후 결정한다.

## 점검 한계

원격 GitHub connector를 이용한 텍스트·Git tree·소스 검사이며 로컬 Windows, NVIDIA/Brev 서버 또는 OFFICIAL 실행환경에서의 실제 빌드·GPU 실행을 뜻하지 않는다. 원본 archive를 열거나 삭제·재포장하지 않는다.

## 후속 구조 개선의 승인 경계

- `research/experiments/h1/H-*`, `go2/G-*`, `HS-*`: 파일명은 legacy지만 실제 Run/evidence·계보 검토의 canonical 기록으로도 쓰이므로 **이번에는 이동 보류**했다. 탐색용 `research/experiments/README.md`를 통해 현행 Experiment 이름으로 찾는다. 다음에 이동하려면 모든 수신 보고서·registry·AI 핵심팩·외부 Release 설명의 경로 영향과 새 원문 위치를 별도로 감사한다.
- `incoming/other/reviewed/` 및 `experiments/`: 출처가 사용자 수신 원문·평가 근거·제출 스냅샷인 경우 원칙적으로 원 위치를 보존한다. 분류 개선은 작은 관련 색인부터 적용한다.
- Originals, NVIDIA, Eval에는 이번 physical move를 적용하지 않았다. 이번 여섯 문서는 모두 Analysis의 processed planning에 있던 것이기 때문이다.
