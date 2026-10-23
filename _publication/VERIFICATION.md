# 원본 구조 공개본 검증 — 2026-10-23

## 1차 구조 전환의 파일과 이력

- 원래 저장소 이름 5개를 최상위 폴더로 사용하고 원래 내부 경로를 유지했습니다.
- 선별 파일 426개 중 422개는 원본 Git blob 또는 검증된 LFS payload와 바이트 동일합니다. 나머지 4개는 개인 Windows 프로필 경로만 블라인드했습니다. 제목·본문·수치·링크·Markdown 공백을 재작성하지 않았습니다.
- 파일별 원본 commit, Git mode, 원본/공개 SHA는 `FILES.json`에 있습니다. 로컬 전용 지침 및 제공 소스·제3자 피드백 전사를 포함한 후보 5개는 파일 단위로 제외했습니다.
- 선별 범위 밖 파일을 참조하는 링크와 역사적 참조 358건은 원문을 고치지 않고 `MISSING_REFERENCES.json`에 기록했습니다. 이 수치는 원본 전체 저장소에서 모두 깨졌다는 의미가 아닙니다.
- 기존 원본 저장소·evidence·백업은 변경하지 않았습니다. 이전 기능별 공개 배치는 Git 이력에 보존했습니다.

## 1차 평가 Release

- 평가 결과 33건을 원래 실험 단위로 분리합니다. 원래 제목·본문·asset 파일명을 보존하며 tag에만 `eval--` 저장소 구분 접두어를 붙입니다.
- ZIP 33개 중 18개는 원본 archive와 바이트 동일하고 15개는 텍스트의 개인 프로필 경로만 블라인드했습니다. 원래 437개 ZIP 구성원 이름·순서, 로그·기존 checksum을 유지했습니다. 영상 132개와 episode 파일 33개는 원본과 바이트 동일합니다.
- 원래 부속 JSON·체크섬 66개도 같은 Release에 보존했습니다. 64개는 바이트 동일하고 2개는 개인 프로필 경로만 블라인드했습니다. 블라인드 후에는 원래 checksum과 공개 파일 hash가 다를 수 있습니다. 공개 asset 검증 기준은 `RELEASES.json`의 `public_sha256`입니다.
- Release 33건·asset 99개를 게시했습니다. 초안 asset 전체의 크기·GitHub SHA-256 digest와 제목·본문을 대조한 뒤 게시했습니다. 33개 공개 안내 뒤 원래 본문의 보존도 로컬에서 별도 검증했습니다.

## 로컬 실행 검사

- 평가기: Python unittest **72개 통과**, PowerShell 실행기 **4개 구문 검사 통과**.
- sidecar: Ubuntu-22.04 WSL에서 `ISSACSIMZ_PYTHON_RUNNER=/usr/bin/python3 /usr/bin/python3 -m unittest discover -s tests` **106개 통과**, exit 0. 제공 keeper source를 내장한 `test_orchestration.py`는 공개 선별에서 통째로 빠졌으므로 이 테스트 수에 포함하지 않습니다.
- sidecar shell과 평가기 `run_evaluation.sh`: `bash -n` 통과.
- Git index의 선별 426개 파일 바이트·원본 실행 mode 일치, 로컬 전용 지침 미포함, `git diff --cached --check` 통과. 전체 추적 파일은 공개 관리 문서 등을 포함해 436개입니다.
- GPU·학습·렌더·원격 서버 설치·종료는 실행하지 않았습니다.

라이선스는 아직 미정이며 이 검증은 제3자 권리의 포괄적 허가를 뜻하지 않습니다. 제외된 task·모델·전체 설정이 필요한 기능은 이 선별본만으로 완전히 재현되지 않습니다.

## 2차 추가 공개 — 2026-10-23

- 자체 분석·프롬프트·운영 문서, CPU 재현·Optuna 도구, publication·Run README/metadata/checksum **577개 추가**. 전체 선별 파일 **1,003개**이며 원본 바이트 동일 **986개**, 개인 프로필 경로만 블라인드 **17개**입니다. 1차 공개 426개는 내용·출처·mode 모두 그대로 유지했습니다.
- 추가 출처: analysis 322개, eval 80개, NVIDIA 10개, originals 165개. `FILES.json`의 정확한 출처 commit을 따릅니다. 문서에 적힌 당시 상태를 이번 공개 시점의 최신 운영 상태로 다시 쓰지 않았습니다.
- 전체 선택 파일 SHA·경로·JSON 181개 검증, 새 Python 17개 AST 및 JavaScript 5개 syntax 검사 통과. 강의 source preflight의 synthetic fixture 30개 테스트도 exit 0이며 실제 강의 입력 접근·출력 쓰기·전체 build는 하지 않았습니다. 받은 분석 스크립트 전체를 실행하거나 GPU 결과를 다시 계산했다는 뜻은 아닙니다.
- 독립 검토에서 추가 파일의 실제 credential·개인 메일·미처리 프로필 경로를 찾지 못했습니다. 제공 코드·DM·원문 평가 코멘트가 있는 후보는 파일 단위로 보류했습니다. 보류 목록은 `EXCLUDED.json`, 원문 그대로 남긴 미포함·역사 참조 346건은 `MISSING_REFERENCES.json`을 확인합니다.
- 기존 평가 33건 외 **자체 기술 보고서 4건**을 원래 Release 제목·본문·파일명으로 추가 게시했습니다. 공개 `analysis--` Release에는 보고서만 포함하며 원문이 설명하는 policy·env·전체 제출 snapshot은 포함하지 않습니다. 모델·공식 training source·대화 원문·전체 archive의 공개 범위를 늘린 것은 아닙니다.
- 개별 Release 37건의 asset 103개 전부 원격 크기·GitHub SHA-256 digest와 제목·본문 대조를 통과했습니다. 기존 snapshot Release 2건은 별도로 보존합니다. Git index의 원본 파일 1,003개 바이트·mode 대조와 `git diff --cached --check`도 exit 0이며 관리 파일 포함 전체 추적 파일은 1,013개입니다.
