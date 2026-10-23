# 출처와 공개 사본의 변경

이 저장소는 기존 비공개 보관 저장소의 이력을 가져오지 않고 별도 snapshot으로 준비했다. 저장된 자격증명·모델·학습 task·강의 원문·운영진 대화·실험 원본 압축본은 포함하지 않는다.

| 배포 위치 | 코드 출처 snapshot | 역할 |
| --- | --- | --- |
| `evaluation/` | `naver-issacsim-eval` · `ddd12bc` | 자체 수집·점수화·비교·영상 실행기 |
| `sidecar/` | `issacsimz` · `b01a397` | 외부 native 학습 호출·evidence 관리 |
| `server_tools/` | `naver-issacsim-nvidia` · `91b32f6` | 자체 setup·체크포인트·과거 운영 wrapper |

`SOURCE_MANIFEST.json`은 복사한 파일별 원본 상대 경로·원본 SHA-256·공개 사본 SHA-256을 기록한다. 원래 커밋 작성자 정보나 Git object 이력은 포함하지 않는다. 새로 작성한 안내 문서는 별도 파일이며 이 source-copy manifest의 대상이 아니다.

공개 사본에서는 다음만 달라졌다.

- 별도 제공 원문 keeper 파일과 그것을 문자열로 내장한 보존 테스트를 제외했다. 테스트 제외는 런타임 검증 실패를 숨기기 위한 것이 아니라 배포하지 않는 원문 fixture의 제거다.
- 이에 맞춰 sidecar README와 테스트 안내의 보존 설명을 고쳤다.
- 루트·평가기·서버 도구 사용법, 외부 의존성, 실험 방법론을 새로 작성했다. 비공개 Release와 운영진 원문 링크를 복사하지 않았다.

과거 private 저장소 주소와 `/workspace`, `/ephemeral`, `C:\NCRC` 같은 기본값이 일부 코드에 남아 있다. 이는 인증정보가 아니며 사용자 환경에 맞춰 외부 task 경로와 게시 대상을 명시적으로 설정해야 한다. 어떤 업로드 wrapper도 공개 코드 검증 중 실행하지 않았다.

출처 추적이 있다는 사실은 모든 제3자 권리나 라이선스가 확정됐다는 뜻이 아니다. 라이선스는 아직 선택하지 않았으며, 외부 Isaac 구성요소의 이용 조건도 이 코드의 공개와 구별한다.

## 분석·결과 확대 snapshot — 2026-10-23

`REPORT_MANIFEST.json`은 선별한 분석·연구·운영 지식·그래프·JSON/CSV의 별도 manifest다. 본래 결론·수치·식별자와 당시 상태를 유지하며 공개 사본 안내, 개인 프로필 일반화, 누락 원본 링크의 텍스트화, 제한된 평가 코멘트의 요약만 기록한다. 일반 native CLI 호출은 공식 소스 파일의 복제와 구분해 보존했다.

`results/PUBLIC_RESULTS_MANIFEST.json`과 각 공개 ZIP의 `PUBLICATION.json`은 원본 asset·멤버와 공개 결과의 해시를 연결한다. 원본 ZIP과 기존 Release는 수정하거나 삭제하지 않는다. 공개 ZIP에 로그/체크섬 변환이 있어 원본 archive와 바이트가 다르며, 영상과 episode 원자료는 동일하게 보존한다.
