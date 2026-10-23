# 8차 정리 — 네 저장소의 작업 목적별 탐색

이 작업은 기존 Analysis Draft PR #1과 세 저장소의 companion 검토 브랜치에만 반영한다. `main` 병합·Downloads 핵심팩 교체·학습/평가 실행은 하지 않는다. `issacsimz`는 이번 네 저장소 범위에 포함하지 않는다.

## 연결된 검토 PR

| 저장소 | Draft PR | 이번 문서 정리 commit |
| --- | --- | --- |
| Analysis | [기존 PR #1](https://github.com/SE3C/naver-issacsim/pull/1) | `52ec281` 및 이 연결표 후속 기록 |
| NVIDIA | [PR #4](https://github.com/SE3C/naver-issacsim-nvidia/pull/4) | `a569132` |
| Originals | [PR #3](https://github.com/SE3C/naver-issacsim-originals/pull/3) | `024d31f` |
| Eval | [PR #2](https://github.com/SE3C/naver-issacsim-eval/pull/2) | `fa1cdb5` |

각 저장소 문서의 companion PR은 Analysis PR의 목적별 구조안과 함께 검토한다. 원래 `main`과 보존 artifact는 그대로다.

## 실제 조사·수정 범위

| 저장소 | 수정한 안내 | 보존 경계 |
| --- | --- | --- |
| Analysis | 루트 README의 오래된 파일 수·이동 전 경로·ORIENT 비교 없음 문구, AI 구성 가이드의 10/07 역사적 범위, Originals 탐색 연결 | 현재 registry 상태·수신 보고서 본문·preset·평가 raw는 변경 안 함 |
| NVIDIA | 용도별 `docs/README`, 루트 안내, Release 색인의 `[학습]`/`[분석]` 표시 | 학습 source·설정·실행기·태그·애셋 변경 안 함 |
| Originals | 공식 18폴더·개인 16폴더 전체 탐색, 학습/export/제출/분석 구분, 실제 Release 주소, 외부 영상 7개 대응 보고서 연결 | 개별 수납 README·원본 bytes·원본 경로·LFS 객체 변경 안 함 |
| Eval | 평가/게시/보고서 입구, 현재 게시처와 기존 NVIDIA 보존 목록 구분, 서버 보조평가 분류 | 실행기·evaluator·bundle manifest·점수·receipt 변경 안 함 |

분류 기준은 작업 목적이다. NVIDIA에서 수행한 보조평가도 분석이다. 환경별 원본 보존 폴더를 통째로 옮기지 않고 탐색 색인에서 목적을 분리한다. ACTRATE-001의 PERSONAL Windows 평가가 기존 공식 학습 폴더 안에 보존된 예외도 양쪽 색인에서 연결했으며, 이 위치로 OFFICIAL 평가를 추정하지 않는다.

## 확인한 누락과 역사적 표현

- Originals 공식 목록은 기존 9개에서 18개 실제 폴더 탐색으로 보완했다. Go2 Round-5 제출 폴더에는 README가 없으므로 기존 manifest에 연결한다. 개인 목록은 기존 5개에서 16개 폴더와 별도 분석 예외를 안내한다. Go2 Brev baseline은 기존 폴더 자체로 연결한다.
- 외부 영상 7개 모두 대응 보고서가 있다. “분석 대기”를 “보고서 보존됨”으로 정정했으며 보고서의 최신 검증·AI 반영 완료를 주장하지 않는다.
- 2026-10-13 GitHub 조회에서 Originals의 현행 Release tag를 확인해 루트의 오래된 링크 5개를 정정했다. 이 작업이 tag를 rename한 것은 아니다. Eval 저장소 Release는 조회 당시 0개다. 기존 NVIDIA 평가 12개가 eval로 이관됐다고 표시하지 않는다.
- Analysis README의 ORIENT “비교 없음”은 2026-10-10 raw 3정책 비교 존재와 충돌해 수정했다. 기술적 비교 조건과 HOLD 판정은 기존 근거를 따르며 reward 인과효과·공식 점수로 승격하지 않는다. 10/07 AI 흡수 기록 본문은 당시 기록으로 보존하고 후속 근거를 앞에 연결한다.

## 검증과 한계

메인이 직접 핵심 변경 근거를 확인하고 세 서브에이전트가 저장소별 색인·분류·링크·변경 범위를 독립 검토했다. NVIDIA 검토에서 발견한 VIDEO 섹션 제목 누락을 `[분석]` 주분류로 고쳤다. 70개 Release 링크와 snapshot tag 대응, 수정된 65개 표시 제목 일치 및 상태 prefix 보존을 확인했다. Originals 공식 18개·개인 16개 폴더가 모두 색인에 있고 분석 예외도 양쪽 입구에 연결됐다.

검토에서 지적된 인접 clone 상대 링크는 다른 저장소의 GitHub URL로 수정해 웹 탐색도 가능하게 했다. 변경 안내 문서 15개에서 로컬 상대 링크 156개 존재 검사를 통과했다. 기존 Analysis 구조 검사도 핵심팩 21개·문서 161개·로컬 상대 링크 1,540개에서 오류 0건이다. `git diff --check`를 저장소별로 적용한다. 원본 전체 SHA 재검증·LFS 다운로드·외부 URL 전수 검사·전체 보고서 내용 전수 감사는 하지 않는다.

관리 규칙의 기준은 [DATA_LAYOUT](../DATA_LAYOUT.md)와 [RELEASE_TAXONOMY](../RELEASE_TAXONOMY.md), 실제 판정은 [registry](../../research/EXPERIMENTS.md)다. companion PR의 분석 탐색 링크는 검토 브랜치를 명시하며, 승인 후 병합 시 `main` 주소로 바꾼다. 검토 중 안내를 이미 main에 배포된 정책으로 설명하지 않는다.

현재 수정은 네 저장소 **탐색·배치 안내**의 범위다. 모든 원본과 과거 본문을 재검증하거나 모든 Release를 다시 분석한 것은 아니다. 원본 보완이 필요한 `g2-submit-5 agent.yaml`, 과거 제출 checkpoint 미확정, Round-6 점수·수령증 미수신과 미실행 PLANNED 가설은 그대로 남긴다.
