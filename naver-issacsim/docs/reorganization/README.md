# 저장 구조 정리 — 병합 결과와 단계별 감사

**2026-10-14 현재:** [Analysis PR #1](https://github.com/SE3C/naver-issacsim/pull/1)은 `main`에 병합됐으며, [Originals #3](https://github.com/SE3C/naver-issacsim-originals/pull/3), [NVIDIA #4](https://github.com/SE3C/naver-issacsim-nvidia/pull/4), [Eval #2](https://github.com/SE3C/naver-issacsim-eval/pull/2)도 각각 `main`에 병합됐다. 아래 Stage별 Draft/미병합 표현과 검토용 링크 확인 수치는 **작성 당시(2026-10-12~13)의 감사 기록**이며 현재 PR 상태가 아니다. Downloads 전달본·원본 evidence·Release asset은 이번 병합에 따라 교체하지 않았다. 파일 위치·탐색 안내와 실제 실험/제출 판단을 분리한다.

## 전체 이동 범위 — 71개 가공 문서

**초기 Stage 1–3의 17건 + Stage 6의 4건 + Stage 7의 50건 = 총 71건**의 문서를 이동·재배치했다. Stage 4·5 및 Stage 8–10은 주로 관계 장부·색인·교차 저장소 검토 링크를 보완한 단계이며, 71건에 더할 이동 건수가 아니다. 각 시점의 과거 감사에 적힌 '17건'은 Stage 5 종료 당시의 누계다.

- **Stage 1–3 (17건):** 과거 planning·미실행 질문·일반 참조 문서를 역사/계획 위치로 이동하고 기존 경로에 호환 탐색 안내를 유지했다.
- **Stage 4–5 (추가 이동 0건):** 수신 보고서의 후속 해석 연결 12건 및 63건의 원문 출처 탐색 장부를 만들었다. 분류·언급만으로 개별 Run의 검증이나 자료 통합을 확정하지 않는다.
- **Stage 6 (4건):** 운영 checklist, Go2 Release notes 2건, 공식 Q&A 해석을 목적/날짜가 드러나는 경로로 배치했다.
- **Stage 7 (50건):** H1 36건(학습 8·분석 28), Go2 14건(학습 5·분석 9)을 **training/analysis 작업 목적**별로 배치했다. OFFICIAL/PERSONAL 실행 출처·Run 계보·정책 판정은 그대로 구별한다.
- **Stage 8–10 (추가 이동 0건):** 4개 저장소 목적별 안내 및 관련 Draft PR, Draft 대 main의 버전 차이에 따른 링크 보정(9차 10곳, 10차 2곳)을 기록했다. 병합되지 않은 문서는 확인된 review URL을 유지한다.

**보존 경계:** 옛 문서 경로는 새 위치를 안내하는 Markdown locator로 남는다(HTTP redirect는 아님). 원본 evidence, checkpoint, ZIP, LFS, 받았던 보고서 원문과 제출 snapshot을 이 이동 때문에 삭제·수정하지 않았다. 이 재분류는 학습 결과를 새로 생성하거나 PERSONAL을 OFFICIAL로 승격하는 작업이 아니다.

**별도 생성기 변경:** `tools/build_knowledge_base.js`는 필수 raw input의 읽기·존재 여부를 쓰기 전에 검사하며 `--preflight-only`는 출력 파일을 생성하지 않는다. 자동 생성 출력은 `planning/_generated/`와 `external_analysis/_generated/` 등 별도 위치에 두어 수동 문서를 보존한다. 전체 build는 파일별 갱신 방식으로 **atomic rollback이 없다**. `build_manifest.json`은 빌드 마지막에만 기록되므로 중간 실패하면 **이전 실행의 manifest가 남아 새 실행의 성공처럼 오인될 위험**이 있다. manifest의 경로·수정 시점·입력 identity를 현재 시도와 구분해야 하며, full 재생성은 격리된 checkout/입력 사본에서만 검토한다. 단순 문서 이동 검증과 생성기 preflight 검증을 구분한다.

**검증 한계:** 과거 단계 감사에 적힌 링크/구문/fixture 확인은 각 기록의 대상과 시점만 입증한다. 이번 설명 보강만으로 전체 재생성, 모든 71개 파일의 원본 재대조, 모든 GitHub URL 및 fragment·LFS 무결성, CI·Windows·GPU·공식 서버 실행을 새로 PASS 처리하지 않는다.

## 2026-10-14 생성기 파서·입력 검증 보완

- `tools/build_knowledge_base.js`의 강의 추출은 `readContent` ID가 실제 `<article>` 시작 태그에 붙어 있는지 확인하고 article 중첩 범위를 맞춘다. 별도의 `<span id="readContent">`나 이전 article로 잘못 이동하지 않는다.
- Preflight는 동일한 강의 추출·텍스트/코드 처리와 glossary의 **이름 있는 용어 추출**을 사용한다. 강의는 텍스트·코드·영상·이미지 중 유효한 추출 대상이 있어야 하고, codebase는 개별 0바이트 역사 파일을 보존하되 전체가 공백이면 거부한다. 인자 없는 full build와 `--preflight-only` 계약은 유지한다.
- **실제 raw 수집 한계:** 2026-10-14에 읽은 Originals `main`의 강의 HTML 22개 중 **04, 07, 09, 12, 14, 15, 17, 18, 19강의**는 `readContent` 본문이 `불러오는 중이에요…` 플레이스홀더만 포함한다. 정상 본문이 들어 있는 나머지 13개 강의의 구·신 article 추출 바이트는 동일하다. 따라서 **현재 수집본 22개를 그대로 이용한 전체 preflight/build는 정상 PASS를 주장할 수 없고**, 완전한 원본 강의 재확보 또는 명시적인 별도 데이터 범위 결정이 필요하다. 원본은 임의 변경·보정하지 않는다.
- 이번 검증에서 CLI·빈 입력 사례는 격리한 메모리 파일시스템으로 실제 JS의 preflight 경로를 실행해 확인했으며, 전체 checkout의 `node --check`·정상 구조 검사·전체 재생성 PASS를 주장하지 않는다. 기존 `build_manifest.json` 잔존 및 비원자적 갱신 위험은 그대로 유지한다.

## 강의 수집 원본과 기존 가공본의 정합성 (2026-10-14)

Originals `main` 강의 HTML 22건과 Analysis `main`/review의 기존 가공 Markdown 22건을 **파일별로 대조**했다. 정상 제목 7건, 다른 강의 본문이 저장된 6건, 로딩 화면만 남은 9건으로 나뉘며, 6+9건의 기존 가공본은 현재 올바른 강의 자료로 사용하지 않는다. [원본 SHA·실제 H1·가공본 SHA·재확보 대상을 기록한 provenance 장부](./2026-10-14_LECTURE_SOURCE_PROVENANCE.md)에서 확인한다. 생성기에는 쓰기 전 filename/readContent identity 검증을 추가했다. 수집본을 다시 확보하기 전에는 지식베이스 전체 생성 PASS를 주장하지 않는다.

## 이번 네 Draft 링크 재확인 (2026-10-13)

Originals PR #3, NVIDIA PR #4, Eval PR #2, Analysis PR #1의 **변경 patch 및 관련 Markdown 현재 본문**에서 `blob/review/20261012-`·`blob/review/20261013-` 링크를 확인했다. **9개 문서에서 25회, 중복 제외 13개 대상 경로**를 확인했고, 13개 모두 지정된 저장소의 review 브랜치에서 파일 내용을 읽어 존재를 검증했다. 그 13개 중 **4개는 main에 파일이 없고, 9개는 main의 Git blob과 다르다.** 그러므로 현재는 해당 검토 링크를 main 링크로 일괄 치환하지 않는다.

이 수치는 **네 저장소 전체 tree/text 전수 검색 결과가 아니라 현재 PR의 변경 patch와 확인된 연결 문서의 범위**다. 모든 PR이 별도 승인으로 병합된 뒤에는 각 main에 대상 파일의 실제 내용이 반영됐는지 확인하고 별도 링크 변경을 검토한다. 이번에는 Draft 유지, URL 목적지 확인만 수행했고 파일·evidence·Release 원본은 변경하지 않았다.

## 사용자 답변을 반영한 기준

1. **목적별 물리 분리:** 과거 절차는 `historical`, 미실행 질문은 `planned`, H1/Go2 가공 문서는 `training/`·`analysis/`로 나눈다. NVIDIA 서버의 보조평가도 분석이며 실행 장소는 출처 정보다. 원문과 데이터는 보존하고 옛 링크는 호환 안내로 유지한다. [배치 규칙](../DATA_LAYOUT.md) · [가공 자료 입구](../../data/processed/README.md).
2. **네 미실행 조합 질문:** 사용자 선택대로 `PLANNED` 유지. 오래됐다는 이유로 완료·폐기하지 않는다. [현재 registry](../../research/EXPERIMENTS.md) · [미실행 질문 목록](../../research/experiments/h1/planned/README.md). HS legacy 계획 두 건도 실행 사실을 새로 만들지 않는다.
3. **부분 내용 감사:** 최근 주요 보고서부터 선별 확인한다. 이번 model_9999·model_4650·Go2 R3/R5 대조 결과는 [7차 기록](./2026-10-13_STAGE7_WORK_TYPE_SPLIT.md)에 남겼다. [63건 참조 장부](../../data/processed/incoming/REPORT_PROVENANCE_TRIAGE.md)는 탐색 연결표이지 전부 반영·검증 완료라는 뜻이 아니다.
4. **Release 표시:** 제목과 상단 관리 안내만 정리하고 기존 본문·태그·애셋은 유지한다. NVIDIA 65건 수정, archive 5건 유지 및 태그·349개 애셋·구 본문 보존을 재조회로 확인했다. PR 병합은 별도 사용자 지시를 기다린다.

## 사용자 검토와 다른 증거 보완 사항

- [`g2-submit-5` native agent.yaml 동결](../../research/submission_presets/README.md)은 기존 canonical archive에서의 정확한 추출이 남아 있다. 설정값을 추측해 채우지 않았으며, 이번 위치·색인 정리와 별도 작업이다.
- 같은 문서의 H1 Round-2/4 제출 policy↔numbered checkpoint 미확정 부분과 H1 Round-6 포털 수령증/공식 점수 미수신은 원본 근거가 있어야 해소된다. 이미 수신한 Go2 Round-5 점수와 혼동하지 않으며, 색인이나 파일명 변경으로 해결하지 않는다.
- [inbox 원문](../../data/processed/incoming/other/inbox/README.md)의 검토 단계와 [H-009 미수신 이미지](../../data/processed/experiments/h1/2026-09-20_H-009_PERSONAL_3K_TO_5K_DEEP_ANALYSIS_SUMMARY.md)는 그대로 남겼다. 자동 삭제·가짜 근거·반영 완료 표기를 하지 않았다.

## 이번 후속 정리에서 닫은 항목

- 구 canonical 경로를 가리키던 프로젝트 컨텍스트를 새 주소로 연결했다.
- OT 안내의 핵심팩 개수와 `incoming`의 단계 설명을 현행 안내에 맞추고, OT 파일 경로를 클릭 가능한 링크로 바꿨다.
- 공식 OCR·공개 snapshot·규정 보존본의 탐색 연결을 보완하고 planning 읽기 순서의 빠진 번호를 고쳤다.
- 아래 감사 기록의 입구를 한곳에 모았다. 기존 기록·수신 원문·규정 텍스트·JSON·실험 상태·제출 preset·학습 코드는 변경하지 않는다.

## 작업별 근거와 보존 확인

| 기록 | 범위 |
| --- | --- |
| [1차 이동 감사](./2026-10-12_FILE_MOVE_PLAN.md) | 초기 설계·역사 계획 선별 이동 |
| [2차 이동 감사](./2026-10-12_STAGE2_MOVE_PLAN.md) | 미실행 질문·과거 지침 분리 |
| [3차 분류 감사](./2026-10-12_STAGE3_CLASSIFICATION_AND_MOVES.md) | 수신 원문·실험 파일 색인, 선별 이동 두 건 |
| [4차 관계 감사](./2026-10-12_STAGE4_REPORT_LINKAGE.md) | 원문↔후속 해석 12쌍 탐색 |
| [5차 출처 조사](./2026-10-12_STAGE5_SOURCE_COVERAGE.md) | 63건 참조 장부와 후속 대조의 범위·한계 |
| [6차 배치 감사](./2026-10-13_STAGE6_FILE_PLACEMENT.md) | 가공 문서 네 건 위치·이름 정리, 운영 색인 |
| [7차 작업 목적별 감사](./2026-10-13_STAGE7_WORK_TYPE_SPLIT.md) | 가공 Markdown 50건 학습·분석 분리, 부분 내용 대조, Release 진행 상태 |
| [8차 네 저장소 탐색 감사](./2026-10-13_STAGE8_CROSS_REPOSITORY_NAVIGATION.md) | Analysis·NVIDIA·Originals·Eval의 용도별 입구와 기존 게시/원본 색인 보완 |
| [9차 Draft 경로 정합성](./2026-10-13_STAGE9_DRAFT_LINK_CONSISTENCY.md) | 미병합 작업 목적/Release 분류 문서의 main↔review 연결 10곳 정정·대상 확인 |
| [10차 Originals 색인 링크 정합성](./2026-10-13_STAGE10_ORIGINALS_REVIEW_INDEX_LINKS.md) | 원본 기준 main과 review 전용 공식 18·개인 16폴더 색인을 구별하고 이전 main 링크 2곳 수정 |

Release 복구용 [변경 전 snapshot](./_snapshots/2026-10-13_NVIDIA_RELEASES_BEFORE.json)과 [수정 후 검증 기록](./_snapshots/2026-10-13_NVIDIA_RELEASE_EDIT_VERIFICATION.json)을 별도로 보관한다. 학습·분석 탐색은 [최근 정책 연결표](../../data/processed/experiments/RECENT_POLICY_LINKS.md)를 참고한다.

**중단 기준:** 현재 조사한 수동 안내·위치·색인에서 안전하게 고칠 누락을 처리한 뒤에는 내용 판정·원본 보완·사용자 선호를 임의로 결정하지 않는다. 전체 생성기 재빌드, 원본 pruning, Release 변경, GPU 실행 또는 PR 병합을 자동 후처리로 진행하지 않는다.

2026-10-13 후속 검증: 문서 105개·로컬 상대 링크 1,106개·핵심팩 21개 구조 검사, 검사기 구문 검사 및 변경 diff 검사 통과. 규정 색인 누락·OT 파일 링크 누락·감사 기록 목록 누락을 메모리 fixture로 만들었을 때 각각 FAIL도 확인했다. 원본 파일을 훼손하거나 실행 산출물을 재생성하지 않았다. 서브에이전트의 별도 안내 문서 조사에서도 추가로 옮길 안전한 후보는 확인되지 않았다. 이는 조사한 탐색 범위의 결과이며 모든 보고서 내용의 전수 검증이 아니다.
