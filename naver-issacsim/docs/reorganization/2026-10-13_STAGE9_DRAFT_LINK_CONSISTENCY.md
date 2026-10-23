# 9차 정리 — 네 저장소 Draft 탐색 링크와 배포판(main) 구분

> **사후 링크 보존 (2026-10-14):** 아래 검토 대상 URL은 2026-10-13 당시 내용을 재현할 수 있도록 당시 확인한 Git commit SHA로 고정했다. 실제 4개 PR은 이후 모두 `main`에 병합됐으며, 이 문서의 ‘아직 미병합’·‘현재 Draft’ 표현은 당시 관찰 기록이다. 현재 사용 안내는 각 저장소의 `main`을 따른다.


2026-10-13. 사용자 요청으로 [8차 네 저장소 탐색 감사](2026-10-13_STAGE8_CROSS_REPOSITORY_NAVIGATION.md)를 실제 검토 브랜치에서 읽고 후속 링크 정합성을 검토했다. 이 기록은 **8차 시점 기록을 수정하지 않는 별도 후속 감사**이며 main 병합·Release 변경·Downloads 갱신·서버/GPU 작업이 아니다.

## 발견한 문제

Analysis [Draft PR #1](https://github.com/SE3C/naver-issacsim/pull/1)의 `docs/RELEASE_TAXONOMY.md`에 추가된 ‘작업 목적과 실행 환경은 별도 축’([학습]/[분석]) 문단은 **main에 아직 없다**. Eval [Draft PR #2](https://github.com/SE3C/naver-issacsim-eval/pull/2)의 2026-10-13 `EVALUATION_RELEASES.md` 목적별 분류도 main의 2026-10-12 안내와 다르다. 두 파일 모두 main에서 열리지만, **Draft에서 정리한 분류를 설명하며 main 문서를 링크하면 사용자가 이전 버전의 규칙을 읽게 된다**. NVIDIA `docs/README.md`의 데이터 배치 규칙도 같은 문제다.

이는 브랜치 혼동에 따른 **탐색 버전 불일치**이지 8차 Release 태그·애셋 검증이나 실제 Run/공식 점수에 관한 오류라고 단정하지 않는다.

## 실제 수정 (총 10 링크 / 5 문서 / 3 저장소)

| 검토 저장소 · 문서 | 링크 수정 수 | 수정 대상 (미병합 source) |
| --- | ---: | --- |
| NVIDIA [README](https://github.com/SE3C/naver-issacsim-nvidia/blob/ed43af5ebb2add53ec724117e31695b3d5b3edc4/README.md) | 3 | Analysis review `docs/RELEASE_TAXONOMY.md` |
| NVIDIA [docs/RELEASE_INDEX](https://github.com/SE3C/naver-issacsim-nvidia/blob/ed43af5ebb2add53ec724117e31695b3d5b3edc4/docs/RELEASE_INDEX.md) | 2 | Analysis review `docs/RELEASE_TAXONOMY.md` 1, Eval review `EVALUATION_RELEASES.md` 1 |
| NVIDIA [docs/README](https://github.com/SE3C/naver-issacsim-nvidia/blob/ed43af5ebb2add53ec724117e31695b3d5b3edc4/docs/README.md) | 1 | Analysis review `docs/DATA_LAYOUT.md` |
| Originals [README](https://github.com/SE3C/naver-issacsim-originals/blob/35a58d68ac1e5f0b9514cd544a6811f167699e36/README.md) | 3 | Analysis review `docs/RELEASE_TAXONOMY.md` 2, Eval review `EVALUATION_RELEASES.md` 1 |
| Analysis [docs/RELEASE_TAXONOMY](../RELEASE_TAXONOMY.md) | 1 | Eval review `EVALUATION_RELEASES.md` |

**변경 내용:** 기존 `blob/main/`을 두 companion Draft 브랜치의 실제 `blob/review/.../` 경로로만 교체했다. NVIDIA/Originals의 README에는 ‘검토 중, 아직 main에 반영되지 않음’을 명시했다. stable `main`에 원래 존재하는 registry·영상 보고서 URL과 외부 Release/tag URL은 바꾸지 않았다.

## 확인한 실제 대상

- Analysis review [분류 규칙](../RELEASE_TAXONOMY.md)에는 ‘작업 목적과 실행 환경은 별도 축’ 문단이 있고, main 판에는 없다.
- Analysis review [데이터 배치](../DATA_LAYOUT.md)는 가공 `training/`·`analysis/` 분리와 원본 보존 경계를 설명한다.
- Eval review [평가 Release 색인](https://github.com/SE3C/naver-issacsim-eval/blob/a9b90ecb85f2107b66423bd377bc595aeff69a72/EVALUATION_RELEASES.md)은 목적별 분석 표기를 포함하며, Eval main의 이전 날짜 표기와 구분된다.
- 수정한 5개 문서에서 검토 브랜치 상대가 지정된 URL 10건을 다시 읽어 **기존 main 목적별 안내 링크 0건**임을 확인했다. 위 세 목적지의 Git blob과 내용도 실제 `fetch_file` 결과로 존재를 확인했다.

## 병합 전후 원칙

- **현재:** 네 Draft PR을 합의된 묶음으로 검토한다. NVIDIA [PR #4](https://github.com/SE3C/naver-issacsim-nvidia/pull/4), Originals [PR #3](https://github.com/SE3C/naver-issacsim-originals/pull/3), Eval [PR #2](https://github.com/SE3C/naver-issacsim-eval/pull/2). 병합·게시 권한을 이 문서가 새로 부여하지 않는다.
- **모두 승인·병합한 이후:** 네 main에 각 문서가 실제 반영됐는지 Git SHA·파일 경로·내용을 확인한 뒤, 검토 브랜치 URL을 main URL로 바꾸는 별도 링크 정리 PR을 검토한다. 이번 작업에서 장래 변경을 예약·실행하지 않았다.
- 기존 NVIDIA Release 70건의 8차 metadata 검증, Originals 공식/개인 raw 원본 목록, Eval Release 0건 관찰은 8차 당시 출처·날짜를 그대로 따른다. 이 단계에서 Releases API나 asset 전체 SHA를 재조회한 것으로 쓰지 않는다.
- 원본 보고서·실험 JSON·native checkpoint·제출 snapshot·실제 평가기는 수정하지 않았다. 교차 저장소 탐색의 버전 정합성만 다뤘다.

## 별도 미해결

`g2-submit-5` native `agent.yaml` 동결, H1 Round-2/4 numbered checkpoint 연결, Round-6 수령증·공식 점수, 미실행 H1 `PLANNED` 연구 질문은 출처 확보 전까지 상태를 바꾸지 않는다. 위 URL 정리가 이를 해결하지 않는다.
