# 외부 실패 사례 반복 분석 안내

이 자료는 2026-09-22 공개 researchlog 스냅샷이다. 분석 단위는 영상 기록의 `key`다.
실패 47개 중 H1 38개, Go2 7개, 로봇 미상 2개이며, 지표가 있는 기록은 45개다.
reward dial이 있는 기록은 44개이고 그중 6개에만 dial이 하나 있다. 단일 dial도
공통 부모·seed·평가 조건이 확인된 대조 실험은 아니다.

## 파일 사용 순서

1. `04_failure_runs.csv`: 로봇·지형·실패 사유와 지표를 `key`별로 확인.
2. `05_failure_reward_dials.csv`: 같은 `key`의 reward baseline·current·delta 확인.
3. `06_failure_stats_long.csv`와 `07_failure_reward_matrix.csv`: 지표 및 reward 조합 비교.
4. `videos.json`: 원본 `detail`·설명·영상 링크 확인. CSV와 충돌하면 원본을 확인.
5. `NCRC_H1_failures_38_full.json`: H1 실패 기록만 빠르게 검토할 때 사용.
6. reviewed incoming의 외부 실패·영상·2026-09-23 H1 교차 분석 보고서, 원본 public Export JSON과 `19_manifest.json`: 기존 해석과 원본 대조.

CSV의 `trial`은 공개 페이지의 표시 번호이지 우리 `research/EXPERIMENTS.md`의 Run ID가
아니다. 안정적인 연결 키는 `key`다. 성공 기록 34개의 `detail`은 비어 있고,
`success_mp4_probe.json`의 34개 HEAD 요청도 모두 fetch 오류로 끝났다. 그 파일의
duration·해상도 값은 MP4를 직접 측정한 결과로 쓰지 않는다.

## 여러 번 나눠 볼 질문

### 1. 실패 지형 지도

H1 38개와 Go2 7개를 따로 집계한다. 지형별 사례 수, 실패 사유, 낙상률·지형 수준·
탐색 std의 분포를 보여주고 `key`를 근거로 붙인다. 빈 상세 2개와 표본이 적은
지형은 따로 표시한다. 실패 목록의 빈도를 전체 참가자의 실패 확률로 해석하지 않는다.

### 2. reward 조합과 위험 신호

같은 `key`에서 동시에 바뀐 dial 수를 먼저 확인한다. 여러 값이 함께 바뀐 사례는
조합으로만 서술한다. 하나만 바뀐 6개도 비교군이 없으므로 인과 효과로 부르지 않는다.
높은 reward와 지형 정체, 낮은 낙상률과 지형 정체처럼 내부 실험에서도 점검할
경보 후보를 뽑되, 공개 자료에 실제로 있는 지표만 사용한다.

### 3. 우리 가설의 다음 질문

H-004~H-012와 Go2 G-005 등의 내부 가설 계보를 별도 자료로 제공한 경우에만
외부 사례와 나란히 놓는다. 외부에서 관찰된 reward 변경 방향·폭이 우리에게 아직
시험되지 않은 질문을 제시하는지 살핀다. 후보마다 관찰 `key`, 함께 바뀐 값,
부족한 비교 조건, 동일 부모에서 필요한 단일변수 검증을 적는다.

## AI에 요청할 결과 형식

| 후보 질문 | 관찰 key·사례 수 | 함께 바뀐 값/편향 | 필요한 내부 대조 실험 | 판단 |
| --- | --- | --- | --- | --- |
| 구체적인 reward·지형 질문 | 원본 key | confounder와 표본 한계 | 같은 부모·seed·evaluator 조건 | 탐색만/보류 |

외부 row는 공식 학습 evidence, 제출 점수, Optuna `study.tell()` observation으로
등록하지 않는다. `why`·`severity`는 `stats`에서 파생됐을 수 있어 독립 정답 label로
학습시키지 않는다. 공식 채점식이나 성공 reward 최적값은 이 자료로 추정하지 않는다.
