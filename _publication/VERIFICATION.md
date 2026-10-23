# 원본 구조 공개본 검증 — 2026-10-23

## 파일과 이력

- 원래 저장소 이름 5개를 최상위 폴더로 사용하고 원래 내부 경로를 유지했습니다.
- 선별 파일 426개 중 422개는 원본 Git blob 또는 검증된 LFS payload와 바이트 동일합니다. 나머지 4개는 개인 Windows 프로필 경로만 블라인드했습니다. 제목·본문·수치·링크·Markdown 공백을 재작성하지 않았습니다.
- 파일별 원본 commit, Git mode, 원본/공개 SHA는 `FILES.json`에 있습니다. 로컬 전용 지침 및 제공 소스·제3자 피드백 전사를 포함한 후보 5개는 파일 단위로 제외했습니다.
- 선별 범위 밖 파일을 참조하는 링크와 역사적 참조 358건은 원문을 고치지 않고 `MISSING_REFERENCES.json`에 기록했습니다. 이 수치는 원본 전체 저장소에서 모두 깨졌다는 의미가 아닙니다.
- 기존 원본 저장소·evidence·백업은 변경하지 않았습니다. 이전 기능별 공개 배치는 Git 이력에 보존했습니다.

## Release

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
