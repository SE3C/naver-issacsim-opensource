# 원본 자료 참조

이 저장소는 분석과 프로젝트 작업을 위한 경량 작업 공간입니다.

- 원본 아카이브: `../naver-issacsim-originals`
- 원본 기준 브랜치: `main`
- 포함 범위: 원본의 가공된 Markdown 자료, 가이드, 기존 분석 문서
- 제외 범위: `data/raw/` 원문, Git LFS 이미지·영상·USD 에셋, 원본 코드와 도구

원본 자료를 인용하거나 분석 결과를 추가할 때에는 가능한 한 원본의 상대 경로와 기준 커밋을 함께 기록합니다.

대용량 원본 에셋이 필요한 경우에만 원본 아카이브에서 선택적으로 Git LFS를 내려받습니다.

## 원본을 찾는 입구

아래 두 Originals 색인은 [Originals PR #3](https://github.com/SE3C/naver-issacsim-originals/pull/3)을 통해 **`main`에 병합된 탐색 안내**다. 이후 끊어진 상대 링크 두 건은 [Originals PR #4](https://github.com/SE3C/naver-issacsim-originals/pull/4)에서 정정했다. 보존 원본의 출처는 당시 evidence와 Git SHA로 확인한다. 현재 `main`의 탐색 색인은 실제 Run의 source checkout이나 학습 계보를 대신하지 않는다.

- [공식 학습·export·제출 원본](https://github.com/SE3C/naver-issacsim-originals/blob/main/data/raw/official_server_runs/README.md)
- [개인 학습과 사후 분석 원본](https://github.com/SE3C/naver-issacsim-originals/blob/main/data/raw/private_server_runs/README.md)
- [학습→분석→원문 연결표](data/processed/experiments/RECENT_POLICY_LINKS.md)

원본의 환경별 보존 경로는 역사적 주소로 유지한다. 작업 목적은 위 색인에서 구분하며 공식 학습 checkpoint의 PERSONAL 평가를 공식 점수나 새 학습으로 바꾸지 않는다. 현재 `main`은 조회 기준일 뿐 과거 Run의 실제 source commit을 대체하지 않는다.
