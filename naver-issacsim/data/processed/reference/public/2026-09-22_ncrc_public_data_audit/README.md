# 2026-09-22 NCRC 공개 연구 기록 intake

## 범위와 보존

이 폴더는 2026-09-22에 공개 페이지에서 GET으로 받은 읽기 전용 자료의 보존본이다.
수집 스크립트는 인증·팀·학습파일·제출·서버 endpoint를 호출하지 않도록 작성되었다.
따라서 이 자료는 공개 표면의 당시 스냅샷일 뿐, 대회 backend 전체나 타 팀의 비공개
상태를 나타내지 않는다.

| 파일 | 역할 |
| --- | --- |
| `NCRC_PUBLIC_DATA_AUDIT_20260922.zip` | 원본 public export와 정규화 CSV·schema·manifest를 묶은 canonical audit bundle. SHA-256 `8bfe3527…219afb7b` |
| `videos.json` | 연구 기록 페이지의 원본 영상 메타데이터 84개 |
| `NCRC_H1_failures_38_full.json` | `videos.json` 실패 목록 중 humanoid 38개와 key가 정확히 일치하는 편의 subset |
| `success_mp4_probe.json` | 성공 기록 34개의 URL probe 결과. 모두 fetch 오류였으므로 duration/해상도 메타데이터를 파일 실측으로 부르지 않는다. |
| `researchlog_page_2026-09-22.html` | 당시 연구 기록 페이지의 HTML snapshot |
| `ncrc_public_exporter.md` | public/read-only GET export의 재현용 문서·스크립트 |
| `ncrc_public_exporter_console_ready.md` | DevTools Console에 바로 붙여 넣는 동일 범위의 실행본 |
| `NCRC_HTML_SNAPSHOTS_20260922.zip` | 이 날짜의 연구 기록 HTML과 대응 `_files` 폴더, `videos.json`을 상대 경로 그대로 묶은 보존본. SHA-256 `55aff3bcec0e5c5fc7dcfd0533bcb5eef9e98aaa233b16630d4993a8c9ffa2a0`; 실제 추출 후 4/4 파일 해시 일치 확인. 기존 public audit ZIP을 대체하지 않는다. |

Downloads의 loose `ncrc_public_export_2026-09-22T15-12-25-697Z.json`은 audit ZIP 내부의 같은
파일과 SHA-256 `39ff3f05…70d4fcb49`가 일치했다. 별도 복사하지 않아 중복을 피했다.

## 확인된 데이터 품질 경계

- `videos.json`은 key 중복 없이 84개다: 실패 `flip` 47, 성공 `ring` 34, 대회 `wall` 3.
- 실패 47개 중 45개만 비어 있지 않은 `detail`을 가진다. reward dial은 214개,
  stat row는 180개로 정규화되었다.
- 성공·대회 기록의 `detail`은 모두 비어 있다. 이 스냅샷만으로 성공 정책의 reward,
  학습 지표나 공식 채점식을 복원할 수 없다.
- embedded `videos.json` stats와 별도 live `stats.json`은 수치가 다르다. 서로 다른
  시점의 snapshot이므로 합치거나 하나로 재계산하지 않는다.
- public endpoint 9개 중 `finalRank` 요청은 404였고 tournament result는 비어 있었다.
  이는 해당 시점 응답일 뿐 순위·평가의 부재를 뜻하지 않는다.

## 허용되는 내부 활용

외부 실패 사례는 reward 변경 폭·terrain·실패 패턴을 살피는 **비인과 prior**다. 새 단일변수
가설, 탐색 범위, run-health 경보 규칙의 후보를 만드는 데만 쓴다. 실제 채택은 동일 parent,
seed, evaluator, 환경과 lineage가 확인된 우리 Run으로 다시 검증한다.

다음은 금지한다.

- 외부 row를 Optuna `study.tell()` trial이나 공식 성능 비교에 직접 입력
- 다중 reward 변경 사례에서 특정 reward 하나의 효과를 인과로 단정
- `why`·`severity`를 독립적인 정답 label로 사용
- 이 공개 snapshot을 제출 policy·env·공식 evaluation provenance로 인용

AI 핵심팩에는 위 경계와 사용 규칙만 요약한다. 원문 분석 보고서는
`data/processed/incoming/other/reviewed/`에 byte-for-byte 보존한다.
반복 분석의 입력 순서와 질문은 [ANALYSIS_TASKS.md](./ANALYSIS_TASKS.md)를 따른다.

2026-09-23에 새로 저장한 연구 기록 HTML과 `videos.json`·`current.json`·`notice.json`은
[`../2026-09-23_ncrc_site_snapshot/`](../2026-09-23_ncrc_site_snapshot/)에 **별도 원본**으로
보존한다. 22일과 23일의 HTML 바이트와 `videos.json.stats`는 다르므로 혼합하거나
최신 파일로 과거 관찰을 덮어쓰지 않는다. 두 스냅샷의 필드별 비교는 새 폴더 README를 따른다.

2026-09-23 H1 외부 38건 × 내부 가설 계보 교차 보고서
`NCRC_H1_EXTERNAL_INTERNAL_SINGLE_DELTA_ANALYSIS_20260923.md`도 reviewed incoming에
다운로드 원문 그대로 보존했다(SHA-256
`d55933c23d83ef75753da19ee173a0568c5f7c5de7b4cdc0f636ecfba7cdeab4`).
AI 라이브러리의 `20_H1_PUBLIC_FAILURES_AND_EXPERIMENT_PRIORS.md`는 그 원문의 실험
우선순위와 한계를 재구성한 판단 문서다. 공개 실패 기록을 공식 채점 결과로 승격하지 않는다.

## 2026-09-23 공개 H1 참조 영상 31개

사용자가 선별 보존을 요청한 공개 researchlog MP4 31개(실패 분류 22개, 성공 분류 9개)는 당시 `reference-h1-researchlog-20260922-selected31` Release의 **개별 원본 MP4 asset**으로 게시했고, 원격 asset 31개 전부의 이름·크기·SHA-256이 로컬 추출본과 일치함을 확인한 기록이 있다. **2026-10-01 consistency audit에서는 해당 GitHub Release tag endpoint가 404이고 현재 Release 목록에도 없으므로, 그 Release를 현재 접근 가능한 보존 위치로 보지 않는다.** 358MB 작업용 분석 ZIP, 가공 보고서, 타 팀의 비공개 자료는 당시 Release에 넣지 않았다. 원본 `mp4` URL과 당시 분류 메타데이터는 이 폴더의 `videos.json`에서 각 `reel-<key>`로 찾을 수 있다.

실패 분류 22개: `11309747`, `11659221`, `11806238`, `11999811`, `12918663`, `14106372`, `19129897`, `22863265`, `60061435`, `60491775`, `74319272`, `77658123`, `78339600`, `78394459`, `87278881`, `88114018`, `8945010`, `9050001`, `92770425`, `93015733`, `93039572`, `97541917`.

성공 분류 9개: `39297234`, `74265314`, `77702969`, `77792863`, `78202966`, `8836451`, `92815087`, `9586400`, `97612025`.

이는 운영진의 **공개 연구기록 영상**이지 우리 팀의 공식 서버 학습 evidence·공식 채점 영상·동일 조건 성공 대조군이 아니다. `school`처럼 9월 23일 공개본에서 제거된 식별 메타데이터를 영상 Release에 다시 첨부하지 않는다.
