# 공개 준비·게시 기록

## 2026-10-23 — 자체 도구 1차 snapshot

- 새 공개 저장소: `SE3C/naver-issacsim-opensource`
- main commit: `698a6e677ebf12cb91e7750dcdee1bd229dd8e0b`
- 원격 push 성공. 기존 5개 저장소의 공개 설정, 과거 이력, Release는 변경하지 않았다.
- 게시 파일 79개: 원본에서 선별한 source 68개와 새 안내·방법론·검증·출처 문서/설정 11개.
- 기존 source 68개 중 sidecar README, tests README, archival-test 제거 파일 3개만 공개 사본에서 편집했다. 런타임 핵심·점수화 코드의 계산은 바꾸지 않았다.
- 원문 keeper 1개 및 그 원문을 문자열로 내장한 테스트 제외. 공식 training, 강의, 실습, DM, 원본 checkpoint, 결과 archive, 기존 Git 이력 제외.
- 정적 보안 검사: 검사 대상 source에서 사용 가능한 자격증명·개인 프로필/메일·사설 IP 발견 없음. 바이너리/전체 원본의 안전성 인증은 아니다.
- evaluation CPU tests 72개 PASS, PowerShell 구문 4개 PASS. sidecar Ubuntu-22.04 WSL CPU tests 138개 PASS, sidecar shell 구문 PASS.
- source-copy SHA 68개 및 Git index 바이트 일치 검사 PASS. root `.gitattributes`로 바이트/줄바꿈을 보존하며 shell 실행 모드를 기록했다. `git diff --cached --check` PASS.
- 실제 GPU·서버 설치·학습·렌더·게시 wrapper는 실행하지 않았다.

라이선스는 사용자 결정에 따라 **미정**으로 유지했다. 공개 열람 가능 상태이며, 라이선스가 확정된 오픈소스 배포가 완료됐다는 의미는 아니다. README·PUBLICATION_STATUS·PROVENANCE에 이 경계를 명시했다.

## 남은 확대 작업

자체 분석 문서·registry·그래프·평가 ZIP을 원문/개인정보/공개 제한과 분리해 추가할 수 있는지 검토한다. 자료를 많이 공개하는 것이 목표지만, 단순한 자동 치환으로 권한 문제를 해결했다고 취급하지 않는다. 원본은 삭제하지 않는다.

기존 장기 보관 10개 압축본은 이번 신규 저장소와 준비 문서를 만들기 전 snapshot이다. 이 게시 기록은 그 백업에 포함되지 않는다.

## 2026-10-23 — 분석·연구·평가 결과 확대 게시

- 사용자 추가 승인: 자체 분석 보고서·Release 결과를 포함해 가능한 많이 공개한다. 서브에이전트 8개가 H1·Go2 보고서, 연구 registry, 수신 분석, 운영 지식, 그래프/구조화 결과, 평가 ZIP과 독립 공개성 검토를 분담했다. 메인이 범위를 통합하고 공개 사본을 작성했다.
- 공개 main commit: **`1c3fa3e0f6121993bf2d1a980483bea0e46ccd7f`**, push 성공. 공개 저장소 총 추적 파일 330개.
- 공개 사본 **247개**: H1·Go2 분석/학습 기록, 수신 AI 분석, experiment/lineage/planning, 선별 운영 지식, 자체 PNG/CSV/JSON. `REPORT_MANIFEST.json`에 출처 commit·원본 SHA·공개 SHA·변환 내역을 기록했다.
- 숫자·Run ID·checkpoint SHA·역사적 PLANNED/HOLD/실패 상태는 유지했다. 개인 프로필 경로 일반화, 미포함 로컬 원문 링크 텍스트화, 공개 안내, 명시적 Markdown hard break·공백 정리, 평가 코멘트 한 곳 요약만 수행했다. 일반 native play CLI 호출은 실제 공식 소스 복제와 달라 보존했다.
- 전체 preset YAML은 공개하지 않았다. `research/submission_presets/README.md`에 h1-submit-7을 포함한 완전한 설정/정책 payload 미포함 경계를 명시했다. 공개 해시가 누락된 원본을 대체하거나 완전한 재현을 보장하지 않는다.
- 평가 결과 **33 ZIP, 761,710,841 bytes**: 원본 source/archive는 변경하지 않고 공개 파생본을 생성했다. 개인 프로필 경로 일반화·`.log` 제외·checksum 재생성. 각 ZIP의 `PUBLICATION.json`이 원본 ZIP 및 구성원 해시와 변환 내역을 기록한다.
- 독립 검증: 원본 구성원 392개 대조, 영상 **132개**·episode JSONL **33개** 바이트 동일, JSON **115개**는 개인 경로 외 값 동일. `null`/unverified provenance와 launcher 실패도 그대로 보존했다. 원본 ZIP 33개는 백업 inventory SHA와 일치했다.
- 공개 사본 247개 원본/출력 SHA 및 JSON 의미 대조 PASS, 변환 상대 링크 **773개** 존재 확인 PASS, 공개 코드 source68개 이전 snapshot과 동일. `git diff --cached --check` PASS. GPU/서버 작업과 평가 재실행은 하지 않았다.

### 게시한 Release

1. `public-evaluation-snapshot-20261023`: 공개 평가 ZIP 33개와 `EVALUATION_SHA256SUMS.txt`, 총 asset34개.
2. `public-research-snapshot-20261023`: 현재 공개 파일 snapshot ZIP 1개, 2,767,809 bytes, SHA-256 `462042ef8aea4594d3d355045ba6f19d0c3e96df7b9260871af1511f78f35b16`. 기존 private Git 이력이 아닌 공개 commit의 파일 snapshot이다.

두 Release는 초안 업로드 후 **원격 asset35개 전체의 크기·GitHub SHA-256 digest를 로컬과 대조**하고 공개 게시했다. 원본 비공개 Release를 옮기거나 수정·삭제하지 않았다. 원래 5개 저장소의 공개 설정·공식 source·evidence·과거 보고서 원문도 보존했다.

### 남은 경계

라이선스는 여전히 미정이다. 공식 training·강의·실습, 운영진 DM/메일 원문, checkpoint·제출 정책·전체 training archive와 개인 작업물 묶음은 이번 공개에 넣지 않았다. 미검사 원본 archive 전체의 공개 적합성을 이번 결과로 보증하지 않는다. 기존 백업 10개는 이번 확장 게시 이전 snapshot이며 삭제하지 않는다.

## 2026-10-23 — 원본 구조·본문 보존 방식으로 전환

사용자 결정: 최대한 공개하되 개인정보만 블라인드하고, 내용을 다시 요약하거나 링크·수치를 고치지 않는다. 공개하기 곤란한 파일은 통째로 제외한다. 공개 저장소 하나 아래 원래 5개 저장소 이름과 내부 폴더 경로를 유지한다.

- 공개 구조 전환 commit: `70c9171cea1be3315cc99d75ba220787b1562cac`, main push 성공. 이전 기능별 배치와 파생 문서는 Git 이력에 보존되며 원본 저장소는 그대로다.
- 선별 **426개**: 원본 바이트 동일 **422개**, 개인 프로필 경로 블라인드 **4개**. 각 출처 commit·원본/공개 SHA·Git mode는 `_publication/FILES.json`에 기록한다. 전체 추적 파일은 관리 문서를 포함해 436개다.
- 이전 공개 안내문·상대 링크 치환·인용문 요약·공백 정리를 원본 파일에서 걷어냈다. 파일명·제목·본문·수치·Run ID·계보·링크·줄바꿈·원래 실행 mode를 보존한다. 미포함 자료·역사적 참조 358건은 원문 대신 별도 목록에 기록했다.
- 후보 5개는 파일 단위로 제외: 제공 keeper 코드를 내장한 테스트 1개, 제3자 피드백 전사 문서 3개, 로컬 전용 AGENTS 1개. 공식 training·강의·실습·원문 대화·모델·전체 training archive는 선별 범위 밖이다.
- 원래 평가 **33 Release·99 asset**을 공개 저장소에 게시했다. tag는 `eval--<원래 tag>`, 제목·설명·파일명은 원본을 보존한다. 공개 안내 뒤 원래 본문을 그대로 붙였다. 기존 두 snapshot Release는 삭제하지 않았다.
- ZIP **18개 원본 동일 / 15개 개인 경로만 블라인드**. 멤버 437개 이름·순서와 로그·기존 checksum을 유지했다. 영상132개·episode33개는 원본 바이트 동일하다. 부속 JSON/체크섬66개는 **64개 동일 / 2개 개인 경로만 블라인드**. 원래 checksum은 원본 기준이며 공개 hash는 `_publication/RELEASES.json`을 따른다.
- 로컬·독립 대조: 원본/공개 파일426개, ZIP33개, 부속물66개, 원본 body33개 검증 통과. 게시 시 asset99개 전부 원격 크기·GitHub SHA-256 digest 일치를 확인했다.
- CPU 테스트: eval72개, sidecar106개 통과. PowerShell4개 및 shell syntax 통과. 원본 Git mode13개 실행 파일 보존, index 바이트426개 대조와 diff check 통과. GPU·원격 서버·학습 실행 없음.

라이선스는 미정이다. 이 공개 선별은 제외된 원본 자료의 권리 허가나 전체 재현성을 보증하지 않는다. 기존 비공개 저장소의 코드·evidence·Release·백업은 변경·삭제하지 않았다. AI 라이브러리의 Downloads 자동 복사는 하지 않았다.
