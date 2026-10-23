# 공개 snapshot 검증 — 2026-10-23

공개용 사본에서 실행한 CPU 검증이다. 원래 저장소에서 과거 통과했다는 사실로 대신하지 않았다.

| 범위 | 실행 | 결과 |
| --- | --- | --- |
| evaluation | `py -3 -m unittest discover -s tests -q` | 72 tests, OK |
| evaluation PowerShell | `.ps1` 4개의 PowerShell Parser 구문 검사 | PASS |
| sidecar | Ubuntu-22.04 WSL, `ISSACSIMZ_PYTHON_RUNNER=/usr/bin/python3 python3 -m unittest discover -s tests -q` | 138 tests, OK |
| sidecar shell | `scripts/*.sh` 및 `issacsimz`에 `bash -n` | PASS |
| 공개 코드 후보 | 알려진 토큰/개인키·개인 프로필·개인 메일·사설 IP 정적 점검 | 실제 비밀정보 발견 없음, 전면 보안 보증 아님 |

Windows sandbox에서 첫 평가기 테스트는 임시 fixture 쓰기 권한 때문에 실패했고, 권한 승인 후 같은 테스트가 통과했다. WSL도 첫 접근 권한 실패 후 승인된 실행에서 통과했다. 이를 기능 테스트 실패와 구분한다.

실제 GPU 평가·영상 재렌더·서버 설치·학습·게시 wrapper 실행은 하지 않았다. 외부 task와 simulator 호환성, 모든 서버 설치 조합, 공식 점수와의 상관은 이 검증으로 확인되지 않는다. 과거 원문 keeper fixture의 보존 테스트는 배포 대상에서 제외해 테스트 수가 원래 코드와 다를 수 있다.

원본 source와 공개 사본의 해시는 `SOURCE_MANIFEST.json`에 있다. 루트 `.gitattributes`는 파일 바이트를 보존하며, shell executable 모드도 별도로 기록한다. 새 공개 문서와 검사 기록은 source-copy manifest 대상이 아니다.
