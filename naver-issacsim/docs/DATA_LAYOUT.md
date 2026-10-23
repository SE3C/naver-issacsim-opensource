# 데이터 구조와 스키마

```text
naver-issacsim/
├─ data/
│  └─ processed/                   # 현재 작업에 사용하는 가공·분석 자료
│     ├─ ai_library/               # 상담 AI 업로드용 핵심팩 00~08, 10~21 (21개)
│     ├─ incoming/                 # 검토·통합 전의 새 분석 자료
│     │  ├─ ot/                    # OT 전사, 개별 분석, 통합 분석
│     │  └─ other/                 # inbox/ · reviewed/ 원문 유지 + 파일별 탐색 색인
│     ├─ reference/                # 공식 자료·시점별 공개 snapshot / game_engine 참고자료
│     ├─ lessons/                  # 강의별 Markdown
│     ├─ glossary/                 # 추출된 용어 Markdown·JSONL
│     ├─ codebase/                 # 코드 파일별 AI용 Markdown
│     ├─ server_backup/
│     │  ├─ reports/               # 통합·엔진·외부 심층 분석과 구조 요약
│     │  ├─ catalog/               # 전체 인벤토리와 tar 엔트리 목록
│     │  └─ code/                  # training, practice_sim, examples, workspace 코드
│     ├─ planning/                 # 날짜별 계획, 이전 주소 안내 + INDEX.md
│     │  ├─ historical/           # 과거 설계·체크리스트·완료된 Run의 사전 계획
│     │  └─ _generated/           # 원본 planning 01~03 자동 변환본(생성 후 존재)
│     ├─ experiments/              # h1/ · go2/ 아래 작업 목적별 training/ · analysis/
│     ├─ external_analysis/        # 영상 분석 요청과 보고서 7개
│     └─ operations/               # 로봇별 게시 설명·검증 receipt·설치 snapshot + README
├─ tools/build_knowledge_base.js   # 원본 재가공용 도구
├─ PROJECT_CONTEXT.md              # AI에게 먼저 주는 지침
└─ README.md
```

## 생성물과 관리 문서의 소유권

`tools/build_knowledge_base.js`는 lectures/glossary/codebase/server_backup의 변환 산출물과 보조 생성용 안내 파일을 관리한다. 사람이 검토·보강한 `planning/INDEX.md`, `planning/historical/*.md`, 기존 계획 위치의 이동 안내 문서 및 `external_analysis/README.md`는 **수동 관리 문서**로, 재빌드 시 덮어쓰지 않는다. 원본 planning `01`~`03` 자동 변환본도 이제 `planning/_generated/`에만 출력한다. 자동 생성된 대조 인덱스와 기본 안내는 각 폴더의 `_generated/`에 분리한다. 새 파일 생성·이동을 이 규칙이 자동 허가하는 것은 아니다.

날짜별 `reference/public/` 웹 스냅샷은 읽기 전용 외부 관찰 자료다. 일부 보존 ZIP이 Analysis의 Git blob에 남아 있지만 이를 OFFICIAL/PERSONAL evidence로 간주하거나 검증 없이 Originals로 이동하지 않는다.

## 새 문서 배치와 이름

- 먼저 [자료별 입구](../data/processed/README.md)에서 용도를 정한다. 수신 원문은 `incoming`, 실제 학습 Run 수납·진단은 `experiments/<robot>/training`, 정책·영상·평가·비교 해석은 `experiments/<robot>/analysis`, 게시 설명·receipt는 `operations/<workflow>`, 공지/Q&A 해석은 `reference`, 실행 전 설계는 `planning`에 둔다. 별도 상태 DB는 만들지 않는다.
- **새 수동 Markdown**은 확인된 날짜·대상·종류가 드러나는 `YYYY-MM-DD_<대상>_<종류>.md`를 기본으로 한다. 날짜는 원문/작업일인지 문서에 밝히고, 알 수 없는 날짜나 Run identity를 파일명에 추측해 넣지 않는다. AI 핵심팩 번호·Experiment slug·생성기 파일명은 각각 기존 계약을 유지한다.
- 같은 주제의 새 자료는 기존 용도/로봇 폴더에 추가한다. 날짜마다 작은 폴더를 늘리거나 원본·설치·평가·제출을 하나의 정책 폴더에 섞지 않는다. 관련 파일 묶음이 실제로 필요한 경우에만 하위 폴더를 만들고 상위 README에서 연결한다.
- 원문 보고서·archive·checkpoint·검증 JSON·제출 snapshot의 이름과 bytes는 유지한다. 옛 수동 문서의 이동은 참조를 조사하고, 링크 보정과 이전 주소 안내를 함께 반영한다. 과거 상태는 최신 결과로 고쳐 쓰지 않고 historical로 구분한다.
- 수동 탐색 문서는 대상 폴더의 README/INDEX에서 관리한다. [게시 기록](../data/processed/operations/README.md)은 학습·분석 결과와 별도의 배포 기록이다. 생성기 범위는 `_generated` 소유권을 따른다.

## 학습·분석 분류 기준

분류 축은 **수행한 작업**이지 서버 종류가 아니다. `training/`은 학습 실행·설정·checkpoint·TensorBoard 등 Run 근거 수납과 학습 진단, `analysis/`는 6영상·평가기·보조평가·정책 비교·공식 채점 해석이다. NVIDIA 서버의 사후 보조평가와 Windows 평가 모두 `analysis/`에 둔다. OFFICIAL/PERSONAL과 서버/Windows는 문서·manifest의 출처 정보로 보존한다. 분석에 학습 곡선이 인용돼도 분석 작업을 학습 Run으로 등록하지 않는다.

이번 선별 이동은 가공 Markdown 50건만 대상으로 한다. 원문 보고서·archive·checkpoint·JSON·그래프·제출 snapshot은 재배치하지 않으며 옛 Markdown 주소에는 호환 안내를 둔다. 자세한 old→new 대응은 [7차 작업 목적별 감사](reorganization/2026-10-13_STAGE7_WORK_TYPE_SPLIT.md)를 따른다. 신규 파일에는 새 주소를 쓰고 기존 원문 안의 링크는 호환 주소로 유지한다.

최근 선별 이동·이름 정리의 근거와 이전 주소는 [2026-10-13 파일 배치 감사](reorganization/2026-10-13_STAGE6_FILE_PLACEMENT.md)에 기록한다.

구조 변경의 단계별 근거와 병합 결과는 [정리 감사 기록](reorganization/README.md)에 모았다. 규정 출처는 [보존 규정 색인](../data/processed/reference/regulations/README.md), OT 자료는 [OT 안내](../data/processed/incoming/ot/README.md)에서 찾는다.

## 연구 Experiment 및 AI 지침 분리

`research/experiments/h1/`는 실제 실행·평가 근거가 있는 Experiment를 유지하고, [미실행 질문 6개](../research/experiments/h1/planned/README.md)를 `planned/`로 물리적으로 분리한다. 이전 파일 경로는 탐색 안내만 남겼다. `2026-10-10` 다섯 조합 가설 중 실행된 planar-tracking switch는 **현재 폴더에 유지**하고, 4개 미실행 질문만 옮겼다. `research/EXPERIMENTS.md`를 현재 상태의 기준으로 삼는다.

`docs/ai_prompts/`의 2026-09-23 지침 스냅샷은 `historical/`에 보존하고, 현행 `지침.txt`를 같은 폴더 루트에 유지한다. 삭제·내용 축약이 아니라 실제 위치 분류다.

## 수신 원문 63건의 탐색 수준 관리

[5차 원문 조사](reorganization/2026-10-12_STAGE5_SOURCE_COVERAGE.md)에서 기존 사용자 수신 파일 63개에 대한 [참조 수준별 장부](../data/processed/incoming/REPORT_PROVENANCE_TRIAGE.md)를 만들었다. 원문이 언급되었다는 사실을 평가 완료·핵심팩 반영·근거 검증으로 취급하지 않는다.

## 수신 원문↔후속 분석 연결의 소유권

[REPORT_CROSSWALK.md](../data/processed/incoming/REPORT_CROSSWALK.md)는 사용자 수신 보고서와 가공 정책 검토·Experiment 문서 12쌍의 **선별 탐색**만 제공한다. 원본 보고서, ZIP, 공식/personal evidence 및 기존 registry를 변경하지 않으며, `supersedes`·핵심팩 통합률을 자동 추정하지 않는다. 처리 기록은 [4차 관계 감사](reorganization/2026-10-12_STAGE4_REPORT_LINKAGE.md)를 따른다.

## 수신·평가 자료 분류 현황

[Stage-3 보존형 이동 감사](reorganization/2026-10-12_STAGE3_CLASSIFICATION_AND_MOVES.md)에 따라 범용 game-agent 문서는 `reference/game_engine/`, 실제 완료된 세 Run의 2026-09-27 사전 계획은 `planning/historical/`로 선별 이동했다. **원본 수신 분석 63개**는 [reviewed 파일별 색인](../data/processed/incoming/other/reviewed/README.md)으로, **미검토 5항목**은 [inbox 목록](../data/processed/incoming/other/inbox/README.md)으로 탐색한다. 이후 Stage-7에서 [가공 학습·분석 문서](../data/processed/experiments/README.md)를 목적별로 이동했고 원본 데이터는 유지했다.

## 역사 문서 이동 기준

[1차 파일별 이동 감사](reorganization/2026-10-12_FILE_MOVE_PLAN.md) 및 [2차 이동 감사](reorganization/2026-10-12_STAGE2_MOVE_PLAN.md)에 따라 초기/대체 계획·기준선 진단 8건은 실제 `planning/historical/`로 이동했다. 예전 주소는 삭제하지 않고 전체 문서로 이동하는 탐색 안내를 남겼다. 다섯 문서는 이전 Git blob과 완전히 같은 바이트이고 `05`만 상대 Markdown 링크 3곳을 고쳤다. 지금 유효한 운영 지침과 기존 보고서·evidence는 옮기지 않았다.

## 원본 참조

원본 HTML·코드·영상·에셋은 인접한 `../naver-issacsim-originals/data/raw`에 보존한다.

## 알려진 제한

- 단어 사전 저장본에는 전체 556개 중 현재 화면에 렌더링된 첫 15개만 존재한다.
- 영상과 이미지는 메타데이터·로컬 참조만 포함하며, 실제 장면 분석은 외부 전문 AI 결과가 필요하다.
- 3D 캔버스와 상호작용 상태는 텍스트로 완전히 보존되지 않는다.
- 서버 백업의 IsaacLab 벤더 소스, Git 내부 데이터, ETLI, USD/USDZ, 키·환경파일은 분석본에서 제외한다.
- 정적 서버 백업에는 학습 완료 정책·체크포인트·실행 영상이 없다. 별도 공식 실행 원본은 `naver-issacsim-originals/data/raw/official_server_runs/`에 보관한다.
