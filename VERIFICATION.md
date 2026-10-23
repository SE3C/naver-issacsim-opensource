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

## 분석·결과 공개 확대 검증 — 2026-10-23

- `REPORT_MANIFEST.json` 247개: 원본 SHA·공개 SHA 및 출처 경로 확인 PASS. JSON의 값은 개인 프로필 경로 일반화 이외에 동일함을 확인했다. Markdown 공백은 명시적 hard break로 바꾸고 불필요한 말미 공백만 정리했다.
- 공개 사본의 변환된 상대 링크 773개: 포함 대상 존재 확인 PASS. 미포함 원문은 링크가 아닌 원본 경로 표기로 남긴다. 과거 비공개 GitHub URL은 출처 기록이며 공개 접근 가능성은 보장하지 않는다.
- 8개 서브에이전트가 보고서·연구·수신 분석·지식·산출물·평가 ZIP·개인정보를 분담 검토했다. 메인이 native CLI 호출과 실제 공식 소스 복제를 구분하고, 전체 preset YAML 미포함 공지를 추가했다.
- 공개 평가 ZIP 33개: CRC·내부 및 외부 SHA 목록·PUBLICATION manifest PASS. 독립 대조로 원본 구성원 392개를 확인했으며 영상 132개·episode JSONL 33개는 바이트 동일, JSON 115개는 개인 경로 일반화 이외 모든 값이 동일하다. 원본 ZIP은 백업 inventory SHA와 일치했다.
- 코드 후보 68개는 앞선 CPU 검증 snapshot과 바이트 동일하다. 문서·결과 공개 작업에서 평가 알고리즘이나 서버 코드를 변경하지 않았고 새 GPU 작업도 실행하지 않았다.

정적 검사에서 선택한 공개 사본의 실제 자격증명·개인 프로필 실명·개인 이메일·운영진 대화 전문은 발견하지 못했다. 짧은 공식 AI 피드백 한 곳은 자체 요약으로 대체했다. 검토 범위 밖 원본 archive 전체나 법적 권리 전반을 보증하는 검사는 아니다.
