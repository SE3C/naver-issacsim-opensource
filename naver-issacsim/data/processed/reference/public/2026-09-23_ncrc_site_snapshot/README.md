# 2026-09-23 NCRC 웹 저장본 — 09-22 자료와 별도 보존

2026-09-23에 Downloads로 받은 읽기 전용 웹/API 저장본이다. 2026-09-22의
`../2026-09-22_ncrc_public_data_audit/`를 대체하거나 그 안의 JSON을 덮어쓰지 않는다.
페이지 저장본은 시점별 관찰 자료이며 대회 backend 전체·공식 채점 결과·타 팀의 비공개
학습 evidence가 아니다.

| 파일 | 역할 |
| --- | --- |
| `NCRC_HTML_SNAPSHOTS_20260923.zip` | Downloads의 HTML 4개와 각각 대응하는 `_files` 폴더, API JSON 3개를 원래 상대 경로대로 묶은 보존본. SHA-256 `7643ac2d313d847bb4f59b0fe3a583fd92f6af2be76cdde6acc04e08fd323136`. Windows `Expand-Archive`로 실제 추출해 270/270개 파일의 해시 일치를 확인했다. |
| `researchlog_page_2026-09-23.html` | 23일 `연구 기록 _ NCRC.html`의 원본 바이트 복사. SHA-256 `7088227b7f23d7c16ca3f9b7c5642848f1c17dc929835188e4aeed6c99c549bc`. |
| `videos.json` | 23일 researchlog 영상 메타데이터·페이지 전체 통계 원본. SHA-256 `596018918de3747f8d0247b2cd788470eca45138b0eb14ba6e1aa2ff17223f62`. |
| `current.json` | 23일 `/api/competition/current` 응답 원본. |
| `notice.json` | 23일 `/api/notice` 응답 원본. |

HTML 보존 ZIP 안의 원래 파일명과 `<title>`이 일부 일치하지 않는다. 예를 들어
`NCRC.html`의 제목은 `팀 운영보드 | NCRC`, `팀 운영보드 _ NCRC.html`의 제목은
`대회 비전 | NCRC`다. 파일명만으로 페이지 역할을 단정하지 않는다. `_files`는 저장된
리소스일 뿐이며 외부 CDN·API 호출까지 완전한 오프라인 재현을 보장하지 않는다.

## 09-22와 09-23의 차이 — 합치지 말 것

| 항목 | 09-22 보존본 | 09-23 수신본 | 해석 |
| --- | --- | --- | --- |
| 연구 기록 HTML | `researchlog_page_2026-09-22.html`, SHA-256 `302b53d1…331c3c1`, 278,814 bytes | 이 폴더의 HTML, SHA-256 `7088227b…9c549bc`, 278,889 bytes | 실제로 다른 바이트의 스냅샷이다. 하나를 다른 날짜 원본으로 대체하지 않는다. |
| `videos.json` | SHA-256 `37c4bbcc…717622d` | SHA-256 `59601891…17223f62` | 영상 key 84개와 실패 47·대회 3·성공 34라는 분류 수는 같다. 22일본에서 84개 모두에 존재하고 33개는 비어 있지 않았던 `school` 필드가 23일본에서는 전부 제거됐다. 나머지 개별 영상의 실질 필드값은 같고 페이지 전체 `stats`는 달라졌다. 제거된 식별값을 새 공개 자료로 재배포하지 않는다. |
| `videos.json.stats` | `day=36`, `policies=7195`, `avg_fall=38.2` | `day=37`, `policies=7344`, `avg_fall=38.1` | 공개 페이지의 전체 집계 시점 차이다. 개별 영상의 새 평가 결과로 읽지 않는다. |
| competition current | audit export의 `result.now=2026-09-22T15:12:24.783253877Z` | `current.json`의 `result.now=2026-09-23T00:42:03.758065917Z` | 재귀 필드 비교에서는 `now`만 달랐다. |
| notice | audit export에 11개 | `notice.json`에 11개 | 항목 ID와 재귀 필드값은 같았다. 23일 파일도 원본으로 별도 보존한다. |

09-22 `videos.json`의 embedded `stats`와 당시 별도 live `stats.json`도 서로 다른
시점이었다. 23일 `stats`로 22일 실패 사례의 fall·terrain 값을 소급 갱신하지 않는다.
새 영상 key나 개별 실패 수치가 늘어난 것으로 해석하지 않는다. 영상 자체의 시각 분석에는
두 날짜 중 어떤 메타데이터를 사용했는지 표시한다.

원본 HTML·JSON·ZIP과 이 README를 구분한다. 위 비교는 분석이며 원본 파일은 수정하지 않았다.
웹 프런트와 본인 팀 평가 응답에 관한 후속 분석 원문은 `data/processed/incoming/other/reviewed/NCRC_WEBSITE_PUBLIC_ANALYSIS_2026-09-23.md`에 보존한다. 해당 보고서의 R3 `remark`는 현재 이 폴더의 공개 API JSON에 포함되지 않으므로 보고서 기록과 직접 재검증된 raw 응답을 구분한다.
