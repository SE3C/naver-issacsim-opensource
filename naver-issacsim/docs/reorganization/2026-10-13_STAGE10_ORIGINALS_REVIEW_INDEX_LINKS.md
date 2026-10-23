# 10차 정리 — Originals 보존 기준과 Draft 탐색 색인 분리

**2026-10-13.** [8차 네 저장소 탐색 감사](2026-10-13_STAGE8_CROSS_REPOSITORY_NAVIGATION.md)와 [9차 Draft 경로 정합성](2026-10-13_STAGE9_DRAFT_LINK_CONSISTENCY.md) 이후 남아 있는 `ORIGINALS_REFERENCE.md`의 탐색 링크 두 곳을 현재 GitHub 원본과 비교하여 수정했다. 본 작업은 main 병합, Release 변경, 원본 자료 재배치가 아니다.

## 실제 확인한 버전 차이

| Originals 탐색 대상 | main Git blob | review Git blob | 검토 브랜치에만 있는 안내 |
| --- | --- | --- | --- |
| `data/raw/official_server_runs/README.md` | `0cf979f16c549e91e9b997f6e8dc6eb6722e6581` | `32cb35bb4c78497f7bc47ca8a9db4c4468c49a42` | 공식 학습/export/제출 18폴더 및 역사적 위치의 PERSONAL 사후평가 예외 |
| `data/raw/private_server_runs/README.md` | `c6791496a9634516dbbf6e0590a6da006eb7f3b0` | `67e2802219ce99df74bf98b752c47e4ffa5a1dc1` | 개인 학습/분석 16폴더와 공식 폴더의 Windows 평가 예외 |

기존 [Analysis Originals 원본 안내](../../ORIGINALS_REFERENCE.md)에서 위 두 색인을 목적별로 찾으라고 설명하면서 링크는 `blob/main/`을 가리켰다. 이 경로는 열리지만 main 내용은 8차에서 구성한 분류를 포함하지 않아 **찾는 내용과 링크 버전이 불일치**했다.

## 적용

- 두 링크를 실제 Originals `review/20261013-work-purpose-navigation` 브랜치의 해당 README 주소로 변경했다.
- 원본 기준 브랜치 `main` 및 원본 파일·checkpoint·evidence·native YAML·제출 preset·Release 태그/애셋은 바꾸지 않았다. 탐색용 검토 링크와 원본의 실제 provenance는 별개다.
- 9차에서 의도적으로 유지한 안정적인 `main` registry 및 수신 원문 링크는 일괄 변환하지 않았다. **새 분류가 review 브랜치에만 있는 것으로 확인된 두 안내만 변경**했다.

## 검증 범위와 미해결

- Originals `main`과 Draft의 공식/개인 README 네 파일을 GitHub connector `fetch_file`로 읽어 각 SHA와 실제 본문 차이를 확인했다. 새 두 URL은 이미 존재하는 검토 브랜치 대상 파일이다.
- 변경한 문서의 링크 경로는 Draft Git tree와 재검증한다. 문서 내부 모든 external URL·GitHub Release 실물·LFS 객체·Run 원본의 전수 재검증을 뜻하지 않는다.
- 네 저장소가 모두 승인·병합되어 대상 색인이 실제 main에 들어온 뒤에만 Draft URL의 main 전환을 별도 검토한다. 이 단계에서 그런 병합 또는 미래 변경을 실행·예약하지 않았다.
