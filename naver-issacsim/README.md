# naver-issacsim — 분석·문서·AI 라이브러리

로보틱스 강의, 단어 사전, 연습 시뮬레이션 코드베이스와 서버 워크스페이스 백업을 원본과 AI용 가공 데이터로 분리한 프로젝트입니다.

## 저장소 역할

| 저장소 | 역할 |
| --- | --- |
| [`naver-issacsim`](https://github.com/SE3C/naver-issacsim) | 분석·문서·AI 라이브러리·실험 registry와 실제 제출 snapshot |
| [`naver-issacsim-originals`](https://github.com/SE3C/naver-issacsim-originals) | 원본 자료·대용량 에셋·공식/개인 실행의 canonical evidence 보존 |
| [`naver-issacsim-nvidia`](https://github.com/SE3C/naver-issacsim-nvidia) | H1/Go2 학습 source·개인 NVIDIA 서버 학습 및 native 영상 Release |
| [`naver-issacsim-eval`](https://github.com/SE3C/naver-issacsim-eval) | PERSONAL 사후 평가·Windows H1/Go2 실행기·새 PC 평가 Release·명시적 정책 비교 |
| [`issacsimz`](https://codeberg.org/passerby1/issacsimz) | 별도 공개 실행/evidence sidecar; 공식 학습 source를 수정하지 않음 |

## 현재 상태의 첫 진입점

- H1 **2026-10-11 실제 Round-6 `h1-submit-6 / ACTRATE-0001` 제출**: [Experiment/Run registry](research/EXPERIMENTS.md) · [동결 native preset](research/submission_presets/README.md) · [원본 제출 manifest](data/processed/experiments/h1/2026-10-11_PRELIM_R6_SUBMISSION/submission_manifest.json). OFFICIAL fresh10K의 indexed keeper `model_9999`와 제출 actor 대응을 기록했으며, 별도 PERSONAL 정책 분석은 HOLD다. 공식 점수·포털 수령증은 아직 확인되지 않았다.
- 질문의 출발점은 [간결한 AI 시작 문서](data/processed/ai_library/00_START_HERE_CONTEXT_AND_MAP.md); 2026-10-11까지 상세 역사는 [보존본](data/processed/ai_library/_history/00_START_HERE_20261012_PRE_CLEANUP.md)에 두었다. 현재 상태의 독립 기준은 항상 registry다.

## 빠른 안내

- 공개 전 범위·권한·이력·Release 정리 구상: [오픈소스화 준비](docs/open_source/README.md). 아직 공개 승인이나 일괄 공개 계획은 아니다.
- **구조 정리 완료·감사 기록:** [병합 결과와 단계별 감사](docs/reorganization/README.md). 작업 목적별 배치와 미실행 계획 유지 기준을 반영한 Analysis PR #1 및 companion PR 세 건은 `main`에 병합됐다. 원문 evidence·checkpoint·Release 자산은 이 정리로 삭제·이동하지 않았다.
- 정책별 학습→분석→원문→게시 기록: [최근 정책 연결표](data/processed/experiments/RECENT_POLICY_LINKS.md). 현재 판단은 registry, 이 표는 탐색용이다.
- Go2 `g2-submit-5 / LINTRACK-125`: [5라운드 공식 평가](data/processed/experiments/go2/analysis/2026-10-08_OFFICIAL_EVAL_GO2_ROUND5_LINTRACK125.md) **88.32/100**(시뮬레이션 58.32/70·설계 의도 20/20·리포트 품질 10/10). 2026-10-08 15:21 사용자 전달 snapshot은 SE3C 29위·종합 174.69/200이다.
- [R3/R5 운영진 답변](data/processed/experiments/go2/analysis/2026-10-08_GO2_R3_R5_OFFICIAL_SCORE_COMPONENTS_ORGANIZER_REPLY.md): 공식 계단 생존율 **99.0%→99.8%**는 개선됐지만 Tracking Score **0.819→0.796**의 손실이 더 커 계단 점수는 **8.52→8.35**로 하락했다. 학습 contact, 공식 survival, tracking을 구분하는 현재 판단 근거다.

- H1 `ACTRATE-001 / model_2850` (SHA `1e6d…bb1`, 2026-10-11): [원문 `.md` 그대로 보존](data/processed/incoming/other/reviewed/H1_MODEL2850_SHA1E6D_POLICY_ANALYSIS_20261010.md) · [AI 라이브러리 정책 검토 HOLD](data/processed/experiments/h1/analysis/2026-10-11_ACTRATE001_MODEL2850_POLICY_REVIEW.md) · [기존 OFFICIAL 학습 Experiment](research/experiments/h1/exp-h1-action-rate-smoothing.md). 3,072개 PERSONAL 평가 전부 20초 생존했지만 정지/횡복귀 드리프트와 계단 통과 미입증으로 전지형 PROMOTE 보류; `ORIENT-100/model_2850`은 SHA가 다른 정책.
- AI context: [시작 문서](data/processed/ai_library/00_START_HERE_CONTEXT_AND_MAP.md)
- H1 `ORIENT-100 / model_2850`: [정책 분석 원문](data/processed/incoming/other/reviewed/H1_ORIENT-100_POLICY_ANALYSIS_20261007.md) · [Experiment 및 HOLD 판정](research/experiments/h1/exp-h1-rough-terrain-orientation-relaxation.md). 2026-10-10 [3정책 raw 비교](data/processed/experiments/h1/analysis/2026-10-10_H1_SCENARIO7_RAW_3POLICY_MATCHED_ANALYSIS.md)가 추가됐다. OFFICIAL 학습과 PERSONAL 평가는 별개이며, 이 비교는 reward 인과효과·공식 점수·승격 근거가 아니다.
- 실험 추적: [registry](research/EXPERIMENTS.md) · [이름 규칙](research/EXPERIMENT_NAMING.md) · [질문별/legacy 파일 구조](research/experiments/README.md)
- 과거 계획 분리: [planning 현재 안내](data/processed/planning/INDEX.md) · [historical 자료](data/processed/planning/historical/README.md) · [1차 이동 감사](docs/reorganization/2026-10-12_FILE_MOVE_PLAN.md) · [2차 이동 감사](docs/reorganization/2026-10-12_STAGE2_MOVE_PLAN.md)
- 원본/제출 배포: [Release 분류](docs/RELEASE_TAXONOMY.md)

## 자료 구조

- [가공 자료 전체 입구](data/processed/README.md): 용도별 폴더를 먼저 선택하고 로봇·주제·날짜별 기록을 찾는다.
- [운영 기록](data/processed/operations/README.md): 게시 설명·검증 receipt와 설치 snapshot을 구분해서 찾는다.
- `data/processed/ai_library/`: 상담 AI에 넣는 핵심팩 21개 (`00`~`08`, `10`~`21`). Windows Go2의 실제 검증 기록은 `21`, H1 companion 실행 계약은 `naver-issacsim-eval/WINDOWS_H1_WORKFLOW.md`를 따른다.
- `data/processed/incoming/`: 새 OT 전사·통합 분석·기타 분석을 검토 후 반영하는 수신함
- `PROJECT_CONTEXT.md`: AI에게 먼저 제공할 프로젝트 설명과 해석 규칙
- `data/processed/lessons/`: 강의별 가공 Markdown (**기존 22건 중 15건은 원본 불일치 또는 로딩 본문**; [2026-10-14 출처 장부](docs/reorganization/2026-10-14_LECTURE_SOURCE_PROVENANCE.md) 참조)
- `data/processed/planning/`: 대회 준비·검증·서버 운영 분석. 수동 `INDEX.md`는 생성기로 덮어쓰지 않는다.
- `data/processed/experiments/`: 로봇별 `training/` 학습 근거와 `analysis/` 사후 평가·해석; 환경은 각 기록의 provenance로 구분
- `data/processed/external_analysis/`: 외부 자료와 영상 분석 전문
- `data/processed/server_backup/reports/UNIFIED_ANALYSIS.md`: 로컬 분석과 외부 심층 분석을 합친 최종 분석본
- `data/processed/server_backup/reports/GAME_ENGINE_FULL_ANALYSIS.md`: 경기 엔진·LLM·경로·판정 코드의 상세 분석본
- `data/processed/server_backup/reports/OVERVIEW.md`: 로컬 분석의 핵심 구조·실행 흐름·보안 제외 사항
- `data/processed/server_backup/catalog/inventory.json`: 2천여 개 백업 파일의 전체 메타데이터 인벤토리
- `data/processed/server_backup/catalog/external_archive_manifest.jsonl`: 외부 분석의 tar 엔트리 2,780개를 구조화한 목록
- `data/processed/planning/INDEX.md`: 정책 개발·개인 검증환경·서버 운영 자료의 분류와 신뢰 규칙
- `data/processed/external_analysis/video_analysis_requests.jsonl`: 외부 영상 분석 요청 목록
- `data/processed/external_analysis/image_analysis_requests.jsonl`: 외부 이미지 분석 요청 목록
- `docs/EXTERNAL_ANALYSIS.md`: 전문 AI에게 그대로 전달할 분석 요청문과 결과 규격
- `docs/ai_prompts/`: 강화학습 비교 분석 프롬프트와 AI 공통 사용자 지침의 원본 TXT. 현행 사용자 지침은 `지침.txt`; 날짜가 붙은 이전 지침은 역사적 보존본이다.
- `docs/AI_LIBRARY_GUIDE.md`: 대회 대비 AI 라이브러리에 넣을 Markdown 묶음과 중복 제외 규칙
- [`docs/RELEASE_TAXONOMY.md`](./docs/RELEASE_TAXONOMY.md): 개인 실험·공식 raw run·실제 제출 snapshot의 Release 위치와 provenance 규칙
- [`research/EXPERIMENT_NAMING.md`](research/EXPERIMENT_NAMING.md): 새 submission preset·Experiment·Run·override·lineage 이름 규칙과 기존 H/G/HS/GS 검색 별칭
- [`research/submission_presets/README.md`](research/submission_presets/README.md): 실제 제출 preset의 동결된 전체 native env/agent 설정과 출처·미확인 계보

## 변환본·수동 안내의 경계

`tools/build_knowledge_base.js`가 갱신하는 강의·codebase·server_backup 변환본과 사람이 보강한 `planning/INDEX.md`, `planning/historical/*.md`, `external_analysis/README.md`는 다르다. 과거 수집 planning `01`~`03`의 자동 재생성본은 `planning/_generated/`에만 출력하므로 역사 문서 및 예전 경로의 이동 안내를 덮어쓰지 않는다. 후자의 두 파일은 생성기 소유가 아니며 기본 생성본은 각각 `_generated/`에 별도로 기록한다. 빌드 종료 receipt는 `data/processed/build_manifest.json`에 남긴다. **실패 시 원자적 rollback이나 stale 생성물 prune은 제공하지 않는다**. 사전 검사 옵션 `--preflight-only`는 필수 원본 세 위치(`lectures`, glossary `page.htm`, `codebase`)만 확인하며 전체 가공 성공이나 선택 입력의 가용성을 보증하지 않는다. 자동 삭제 없이 실제 변경 diff와 원본을 확인한다.

과거 수집 `data/raw/codebase`의 [파일명·실제 코드 내용 불일치](data/processed/codebase/README.md)와 JSON/CSV의 [checkpoint 식별 매핑](data/processed/experiments/DERIVED_IDENTITY_MAP.md)을 참고한다. 외부 웹 보존본과 원본 evidence는 조회 목적만으로 이동·삭제하지 않는다.

## 연구·AI 지침의 실제 분류

- [H1 완료·미실행 질문 분류](research/experiments/h1/README.md): 실제 Run이 있는 질문은 원래 `h1/` 위치, 미실행 6개는 [planned](research/experiments/h1/planned/README.md)에 보존하고 옛 주소에는 탐색 안내를 남긴다.
- [AI 지침의 버전 분리](docs/ai_prompts/README.md): 현행 공통 지침은 루트, 2026-09-23 이전 버전은 `historical/`에 보존한다.

## 원본 수신 63건의 참조 조사

- [원문별 Git blob SHA·참조 장부](data/processed/incoming/REPORT_PROVENANCE_TRIAGE.md): 현재 참조 분류·집계는 장부 한 곳을 따른다. 명시적 출처와 문맥 연결을 구분하며 orphan·integrated 여부는 단정하지 않는다.
- [5차 조사 범위와 한계](docs/reorganization/2026-10-12_STAGE5_SOURCE_COVERAGE.md).

## 수신 보고서 ↔ 후속 해석 대조

- [확인된 12개 source-to-interpretation 관계](data/processed/incoming/REPORT_CROSSWALK.md): 추가 평가 ZIP으로 확장된 분석과 원문 수납, 운영진 답변 전사를 구분한 noncanonical 탐색표. 원본 reports/evidence는 이동·수정하지 않고 기존 63개 reviewed 원문을 별도로 보존한다.

## 수신 원문·실험 자료 파일별 탐색

- [수신 원문 63개 색인](data/processed/incoming/other/reviewed/README.md) · [inbox 5개](data/processed/incoming/other/inbox/README.md): H1·Go2·공개/운영 자료를 파일명 기준으로 구분하며 원본은 그대로 보존한다.
- [H1 학습·분석·제출 탐색](data/processed/experiments/h1/README.md) · [Go2 학습·분석·제출 탐색](data/processed/experiments/go2/README.md): 가공 Markdown은 작업 목적별로 분리하고 옛 경로는 호환 안내로 남겼다. 수신 원문·데이터·제출 snapshot은 이동하거나 수정하지 않았다.
- [참고 게임 에이전트 자료](data/processed/reference/game_engine/README.md) · [3차 실제 이동 근거](docs/reorganization/2026-10-12_STAGE3_CLASSIFICATION_AND_MOVES.md).

## 읽기 전용 구조 검사

```bash
node tools/check_knowledge_structure.js
```

최상위 AI 핵심팩의 21개 파일, Markdown 첫 제목, 주요 문서의 상대 링크와 필요한 파일 존재만 검사한다. **원본 ZIP/SHA, 외부 URL·앵커, 전체 저장소 링크, GPU/실행 결과까지 검증하는 도구는 아니다.** 파일을 변경하지 않는다.

## 재생성

```powershell
node tools/build_knowledge_base.js --preflight-only  # 원본 경로 사전 검사, 쓰기 없음
# 실제 재생성은 입력 및 영향을 받는 출력 경로를 검토한 다음 별도 실행
node tools/build_knowledge_base.js
```

이 도구는 인접한 `../naver-issacsim-originals/data/raw`를 읽어 현재 저장소의 가공 자료를 갱신한다. 이 저장소에는 현재 작업에 사용할 가공·분석 자료만 두며, 통합 검색 인덱스(`corpus`)는 생성하지 않는다.

Git 저장소에서는 복원 가능한 연습용 키, `.env*`, 서버 tar, ETLI 추적과 중첩된 IsaacLab checkout을 제외합니다. IsaacLab은 `inventory.json`에 기록된 커밋으로 재현할 수 있으며, 제외한 파일의 존재·경로·크기는 인벤토리에 남아 있습니다.
## 운영 규칙

원본 파일·대용량 에셋은 `naver-issacsim-originals/data/raw/`에서 관리한다. 가공·분석 결과는 이 저장소의 `data/processed/`에 둔다. 사용자 제공 2026 NCRC 영상 분석 보고서 7개는 `data/processed/external_analysis/video_reports/`에 있으며, 대응 원본 영상은 원본 저장소의 `data/raw/external_analysis/single_videos/`에 있다.

규정·제출·허용 범위처럼 변할 수 있는 내용은 분석 문서보다 최신 공식 공지를 우선한다. NVIDIA 서버에서는 LFS 대용량 파일을 필요한 범위만 내려받는다.

Release는 개인 서버 학습·영상(NVIDIA), 새 PC 평가(eval), 공식 raw(Originals), 실제 제출 snapshot(analysis)으로 분리한다. 기존 PC 평가 링크는 유지한다. [RELEASE_TAXONOMY.md](./docs/RELEASE_TAXONOMY.md)를 따른다.

## 관리 점검 현황

필요한 수정만 적용한다. 미완료 항목도 실제 문제가 확인되기 전에는 자동 정리·새 인덱스 구축을 시작하지 않는다.

1. **현재 학습 source 기준 — 완료:** 실행 checkout·공식 서버·과거 분석 복사본의 구분과 비교 결과는 NVIDIA [`CURRENT_SOURCE.md`](https://github.com/SE3C/naver-issacsim-nvidia/blob/main/CURRENT_SOURCE.md)를 따른다.
2. **자동 생성 자료 — 부분 안전화:** 수동 planning/history 문서 보호 및 생성 디렉터리 분리를 구현했고 원본 필수 경로 preflight를 추가했다. 실제 전체 빌드는 아직 실행하지 않았다. 지금 삭제할 유령 파일은 특정되지 않았으므로 수동 작성 자료까지 지울 수 있는 일괄 재생성·prune은 하지 않는다. 원본 삭제로 실제 stale 출력이 생길 때 생성 범위만 좁혀 처리한다.
3. **실험 상태·이름 기준:** 별도 상태 YAML을 만들지 않고 [`research/EXPERIMENTS.md`](research/EXPERIMENTS.md)의 현재 판단 표를 기준으로 한다. 새 명명은 [Experiment naming](research/EXPERIMENT_NAMING.md)을 따른다. `H/G/HS/GS`와 `Rxx`는 기존 기록의 legacy 주소이며 더 발급하지 않는다. 실행 중 상태는 잠정적이고 evidence 확인 후 registry와 상세 파일에 반영한다.
4. **문서 링크 — 정적 확인:** 경로 호환 안내를 유지하며 변경된 문서의 Markdown 상대 경로를 Git 트리와 대조하고, [구조 검사 도구](tools/check_knowledge_structure.js)를 추가했다. H-009 수신 원문의 그래프 PNG 4개는 미수신이므로 원문을 수정하거나 가짜 이미지를 만들지 않고 [분석 요약](data/processed/experiments/h1/2026-09-20_H-009_PERSONAL_3K_TO_5K_DEEP_ANALYSIS_SUMMARY.md)에 한계를 표시했다. 다만 앵커·외부 URL·실제 전체 빌드는 확인 대상에 포함되지 않는다.
5. **incoming 처리 — 원문 보존·탐색 개선:** [`incoming/README.md`](data/processed/incoming/README.md)에 연결된 reviewed/inbox 파일별 색인은 원본 그대로 둔 채 H1·Go2·공개 자료를 제목 기준으로 찾아간다. `reviewed`와 AI 핵심팩 반영을 구분한다. 원문 byte 보존을 깨는 일괄 `integrated` 필드는 넣지 않는다.
6. **H1/Go2 회귀 검사 — 보류:** 현재 source가 보존 snapshot과 일치하며 이번에는 학습 코드를 변경하지 않는다. 실제 training/finalize 변경이 생길 때 필요한 공통 규칙만 테스트한다.
7. **evidence 전사 — 기존 Run 단위 점검 유지:** 새 원본을 수신할 때 run ID·parent checkpoint SHA·source commit·evidence 경로/SHA를 확인해 해당 실험 Run에 기록한다. [파생 결과물 참조](data/processed/experiments/DERIVED_IDENTITY_MAP.md)는 비공식 보조 색인으로만 사용하며 자동 checkpoint selector는 만들지 않는다.
