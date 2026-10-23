# NVIDIA 서버 작업공간 규칙

## 읽는 순서

코딩 에이전트나 작업자는 먼저 아래 파일을 읽는다.

1. `workspace/naver-issacsim/README.md`
2. `workspace/naver-issacsim/PROJECT_CONTEXT.md`
3. `workspace/naver-issacsim/docs/DATA_LAYOUT.md`
4. 현재 작업에 맞는 `data/processed/` 하위 문서

이는 강제 에이전트 지침 파일이 아니라 작업공간 안내다.

## 저장소 역할

| 위치 | 역할 | 대용량 파일 |
| --- | --- | --- |
| `workspace/naver-issacsim` | 분석, 기획, 코드 참조, AI 핵심팩, 새 분석 수신함 | 없음 |
| `workspace/naver-issacsim-originals` | 원본 HTML, 코드, 영상, 이미지, USD 등 아카이브 | Git LFS로 필요할 때만 받음 |
| `workspace/naver-issacsim-nvidia` | 개인 NVIDIA 서버의 H1·Go2 학습 source와 준비 문서 | raw archive는 별도 보존 |
| `workspace/issacsimz` | 개인·공식 mode-aware 실행과 evidence sidecar | 학습 source·원본 archive 없음 |

## 새 자료 처리

- OT 전사 → `naver-issacsim/data/processed/incoming/ot/transcripts/`
- OT 개별 분석 → `.../incoming/ot/analyses/`
- OT 통합 분석 → `.../incoming/ot/synthesis/`
- 기타 새 분석 → `.../incoming/other/inbox/`
- 검토 완료·핵심팩 반영 전 자료 → `.../incoming/other/reviewed/`

상담 AI용 핵심팩은 `naver-issacsim/data/processed/ai_library/`의 Markdown 20개(`00`~`08`, `10`~`20`)다. 게임 에이전트 참고문서 `09`는 `naver-issacsim/data/processed/reference/`에 보존한다. 새 자료는 검토 후 관련 핵심 문서에 통합한다.

## LFS 원칙

원본 저장소의 LFS asset은 이 학습 소스 저장소에서 받지 않는다. 필요한 경우
`naver-issacsim-originals`의 raw-data 절차를 따라 개별적으로 가져오며, 전체 LFS
다운로드는 서버 디스크 사용량을 크게 늘리므로 명시적으로 결정한 경우에만 수행한다.
