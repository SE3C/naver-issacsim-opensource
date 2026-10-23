# Stage 2 파일별 이동 감사 및 실제 완료 기록 — 2026-10-12 (A+B 혼합)

**적용 결과:** Analysis Draft PR 검토 브랜치에서 아래 9건을 실제 재배치하고 원래 경로에 짧은 안내 문서를 유지했다. 사용자가 지시하지 않은 GPU 실행·자료 삭제·4개 저장소 `main` 병합은 진행하지 않았다.

## 이동 규칙

Analysis Draft PR에서만 일반/역사 문서를 이동한다. 이동 전 Git blob SHA를 검증하고 원본 문서 본문 및 근거를 그대로 두며 **상대 Markdown 링크만** 새 위치 깊이에 맞춰 보정한다. 이전 주소에 짧은 탐색 안내를 남긴다. GitHub 자동 301은 아니다. 실제 Run·evidence·submission YAML·원본 분석보고서/사용자 수신 원문은 이동하지 않는다.

## 이동 대상 (9개)

| 기존 경로 | 새 경로 | 이동 전 blob SHA | 내용 근거 |
| --- | --- | --- | --- |
| `data/processed/planning/04_OPTUNA_REWARD_SEARCH_DESIGN.md` | `data/processed/planning/historical/04_OPTUNA_REWARD_SEARCH_DESIGN.md` | `2dda4f9ed1b0f38e279ec810042852066cd89115` | 2026-08 pre-implementation design; AI 15 supersedes current Optuna readiness |
| `data/processed/planning/06_H1_OFFICIAL_SERVER_BASELINE_DIAGNOSTIC.md` | `data/processed/planning/historical/06_H1_OFFICIAL_SERVER_BASELINE_DIAGNOSTIC.md` | `cc3c52f2d8a8d328b75b709d02139f34d7cf4198` | status=historical_procedure; 2026-08 baseline guide, not current OFFICIAL procedure |
| `docs/ai_prompts/AI_공통_사용자_지침_20260923.txt` | `docs/ai_prompts/historical/AI_공통_사용자_지침_20260923.txt` | `2c340f7691c20ff3bd0ae9b4838dcf1b2bc04959` | dated earlier common-instructions snapshot, distinct from current 지침.txt |
| `research/experiments/h1/HS-001.md` | `research/experiments/h1/planned/HS-001.md` | `7c928c62c36410a0089d2ecc3b89e542885dc16e` | verified PLANNED, no HS Run; do not classify as executed |
| `research/experiments/h1/HS-002.md` | `research/experiments/h1/planned/HS-002.md` | `d5988e5019f60f9a59c4bea44a0fa829232fd1da` | verified PLANNED, no HS Run; do not classify as executed |
| `research/experiments/h1/exp-h1-action-airtime-fresh-interaction.md` | `research/experiments/h1/planned/exp-h1-action-airtime-fresh-interaction.md` | `9371d0fa8cba8772139178856ee960170432c336` | four remaining 2026-10-10 planned questions without issued Run |
| `research/experiments/h1/exp-h1-action-first-airtime-switch.md` | `research/experiments/h1/planned/exp-h1-action-first-airtime-switch.md` | `cd40770f8dd8a11de38af5ffabf15c22ad0e1db7` | four remaining 2026-10-10 planned questions without issued Run |
| `research/experiments/h1/exp-h1-action-first-body-rate-switch.md` | `research/experiments/h1/planned/exp-h1-action-first-body-rate-switch.md` | `4fe09389786d4ccabc407b4733258d76a58c9366` | four remaining 2026-10-10 planned questions without issued Run |
| `research/experiments/h1/exp-h1-action-foot-contact-stability.md` | `research/experiments/h1/planned/exp-h1-action-foot-contact-stability.md` | `52a4a4eb3083e32223332967e51fd1de9cfb3841` | four remaining 2026-10-10 planned questions without issued Run |

## 링크 영향

- `04` Optuna: 기존 `planning/INDEX`, AI 운영/설계/Optuna 문서가 참고한다. 링크는 새 canonical 위치로 고치고 옛 경로 안내를 남긴다.
- `06` H1 baseline: 기존 `planning/INDEX`, AI export 문서, 수신 과거 보고서에서 참고한다. 해당 당시 보고서 원문을 다시 쓰지 않고 옛 경로 안내로 연결한다.
- 2026-09-23 prompt: GitHub main code search에서 파일 basename 참조 0건. 현행 공통 지침 `docs/ai_prompts/지침.txt`와 구분한다.
- HS 두 개: `research/EXPERIMENTS.md`, H-005/H-010 문서와 연구 색인에서 참조한다.
- action 계열 네 개: `research/EXPERIMENTS.md`, H1 ACTRATE-0001 Experiment, 다섯 가설 원문 계획 등에서 참조한다. **다섯 가설 중 `exp-h1-action-first-planar-tracking-switch`는 실제 OFFICIAL resume Run 완료/PERSONAL 평가 완료(행동 HOLD)**이므로 planned 폴더로 옮기지 않는다.
- `planned/`는 파일 위치일 뿐 새 Experiment 이름·Run ID·실행 승인·현재 GPU 일정이 아니다. 실제 status가 변하면 registry와 이 폴더를 함께 정리해야 한다.

## 수행한 정합성 처리

- 현행 Experiment registry의 미실행 질문 6개 링크를 `planned/`로 교체하고, 원래 ACTRATE-0001 Experiment와 다섯 가설 계획의 링크를 갱신했다. 실제 resume 완료된 planar-tracking switch와 그 Run은 이동하지 않았다.
- AI 핵심팩의 planning `04`/`06` 원본 참조와 `planning/INDEX.md`를 새 canonical `historical/` 위치로 갱신했다. 과거 수신 보고서의 본문은 재작성하지 않고 호환용 이전 경로를 통해 찾을 수 있게 했다.
- 새 구조별 안내 `research/experiments/h1/planned/README.md`, `docs/ai_prompts/historical/README.md`를 만들었고, 현재 디렉터리 루트의 개요 안내도 연계한다.

## 보존 및 확인 기준

1. 이동 후 문서 본문의 문구·숫자·관측 판정은 그대로 두고 relative Markdown link target만 보정한다. 원본 blob SHA는 위에 남기며 Git 객체는 보존한다.
2. 기존 경로 stub은 이동 대상 전체 본문을 복제하지 않는다. 새 canonical 문서와 registry/현행 지침으로만 안내한다.
3. 참조 목록은 GitHub main code search와 실제 branch의 관련 파일 내용에 기초하며, 외부 Release의 임의 링크까지 전수 보장하지 않는다. 옛 경로를 남겨 호환한다.
4. staged tree의 경로/내용 비교, 링크 감사, generator가 수동 `planning` 파일을 덮어쓰지 않음, core Markdown 21개, 4개 `main` 미수정 검증 후 결과를 기록한다.
