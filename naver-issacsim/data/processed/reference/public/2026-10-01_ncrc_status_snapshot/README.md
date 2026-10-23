# 2026-10-01 NCRC 진행 현황 페이지 저장본

이 폴더는 **2026-10-01**에 브라우저의 전체 페이지 저장으로 보존한 NCRC 진행 현황 페이지(`https://robotics.connect.or.kr/status`)를 날짜별 증거로 분리해 둔 스냅샷이다. 과거 2026-09-22/23 공개 페이지 저장본을 대체하거나 그 시점의 자료와 합치지 않는다.

## 보존물

| 파일 | 역할 |
| --- | --- |
| `status_page_2026-10-01.html` | ZIP 안의 저장 HTML을 바이트 그대로 별도 보존한 파일. |
| `NCRC_STATUS_SNAPSHOT_20261001.zip.b64` | 사용자가 제공한 전체 페이지 ZIP의 **base64 transport encoding**. 디코드하면 원본 ZIP 바이트가 복원된다. |
| `NCRC_STATUS_20261001_SHA256SUMS.txt` | ZIP 내부의 디렉터리를 제외한 34개 파일 SHA-256 목록. |

## 원본 ZIP provenance

- 사용자 제공 파일명: `팀 운영보드_NCRC.zip`
- 크기: **1,023,560 bytes**
- SHA-256: `3eac543a784248d083d2865d69e0ce1cbc3c7decd5a40fe2e8869ba02d533064`
- ZIP 엔트리: **36개** = 디렉터리 2개 + 파일 34개
- ZIP 내부 HTML: `팀 운영보드_NCRC/팀 운영보드 _ NCRC.html`
- ZIP 내부 HTML 크기: **109,872 bytes**
- ZIP 내부 HTML SHA-256: `d82275249dfbad536c702add4adfeac31b6baa5d2c3d5b9500709f2d5fcb41d2`
- ZIP 엔트리 메타데이터의 HTML 시각: **2026-10-01 00:35:00**. ZIP 기본 시각 필드에는 timezone 정보가 없으므로 서버 시각 증거로 해석하지 않는다.
- 별도로 업로드된 HTML과 ZIP 내부 HTML은 SHA-256 및 바이트가 정확히 일치했다.

HTML 첫 부분에는 브라우저가 기록한 원본 URL 주석 `saved from url=(0037)https://robotics.connect.or.kr/status`가 있다.

## 페이지 자체에서 보존된 상태

저장 HTML에는 당시 화면의 다음 정보가 포함되어 있다.

- 예선 **5라운드** 제출 마감: **2026-10-06 09:00**
- TOP 32 표의 화면 표시 기준 **최종 업데이트: 2026-09-30 11:54**
- 로그인된 팀에 따라 보이는 운영보드 링크와 팀별 표시가 포함된 **인증된 사용자 화면 스냅샷**

위 값은 이 HTML에 렌더링되어 저장된 화면 상태다. 이 저장본만으로 서버 backend의 전체 상태나 API 응답 시점을 소급 확정하지 않는다.

## ZIP 복원

GitHub 연결 경로에서 바이너리 ZIP을 직접 기록할 수 없어, 원본 ZIP은 손실 없는 base64 텍스트로 보존했다.

Linux/macOS 예:

```bash
base64 -d NCRC_STATUS_SNAPSHOT_20261001.zip.b64 > NCRC_STATUS_SNAPSHOT_20261001.zip
sha256sum NCRC_STATUS_SNAPSHOT_20261001.zip
```

복원 ZIP의 SHA-256은 반드시 다음과 같아야 한다.

```text
3eac543a784248d083d2865d69e0ce1cbc3c7decd5a40fe2e8869ba02d533064
```

## 범위와 한계

- 전체 페이지 저장에 포함된 HTML·JS·CSS·SVG·이미지는 ZIP 안에 보존되어 있으며 각 파일 해시는 manifest에 있다.
- 외부 URL로만 참조되고 브라우저가 로컬 `_files` 폴더에 저장하지 않은 자산은 이 ZIP에 존재한다고 가정하지 않는다.
- 별도 `/api/notice`, `/api/evaluation-report` 등 API JSON 원본을 이번 저장본이 자동으로 포함한다고 가정하지 않는다.
- 인증정보 문자열에 대해 `Authorization`, `Bearer`, `access_token`, `refresh_token`, `Set-Cookie`, `Cookie:`, `password`, `api_key`, `apikey`, `secret` 패턴을 간단히 검사했으며 저장 HTML에서 일치 항목은 발견되지 않았다. 이는 모든 형태의 비밀정보 부재를 보증하는 보안 감사가 아니다.
