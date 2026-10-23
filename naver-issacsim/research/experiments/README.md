# Experiment 문서 탐색

- [H1 joint tracking + 자세·고관절 완화](h1/exp-h1-joint-tracking-posture-relaxation.md): 2026-10-17 후보2 OFFICIAL fresh3K와 model2850 PERSONAL 평가 수신 완료. 원본·SHA·정책 보고서 수신/HOLD를 실제 Run에 연결한다.

Experiment는 연구 질문, Run은 실제 개별 학습 실행이다. 현재 Experiment 이름은 [명명 규칙](../EXPERIMENT_NAMING.md), Run 상태·증거·제출은 [전체 registry](../EXPERIMENTS.md)가 우선한다. 이 디렉터리는 **역사적 검색 주소를 보존**하며 기존 파일명을 일괄 rename하지 않는다.

## H1

- 실제로 실행되거나 평가 근거가 있는 질문별 `exp-h1-*.md`는 [`h1/`](h1/)에 유지한다. 확인된 미실행 질문 여섯 건은 [`h1/planned/`](h1/planned/README.md)에 물리적으로 분리했고, 이전 주소는 탐색 안내로 유지한다. `H-001`–`H-012`는 보존된 legacy alias 및 당시 실행·비교 설명으로 유지한다.
- 예정된 두 schedule 비교 질문 [`exp-h1-stable-first-track-switch` (HS-001)](h1/planned/HS-001.md), [`exp-h1-track-first-stability-switch` (HS-002)](h1/planned/HS-002.md)는 **PLANNED/미실행**이다. 별도 새 Run ID나 빈 Run 문서를 생성하지 않는다. 새 Run ID를 만들지 않는다. 원문 HS 파일이 상세 출처다. 2026-10-10 다섯 ACTRATE-0001 조합 질문 중 [planar-tracking switch](h1/exp-h1-action-first-planar-tracking-switch.md)는 이후 OFFICIAL Run 완료/PERSONAL 평가 HOLD로 확인돼 `planned/`에 넣지 않았다.

## Go2

- [exp-go2-planar-tracking-terrain-progression](go2/exp-go2-planar-tracking-terrain-progression.md): Go2 평면 추종/지형 진행 질문의 탐색 주소. 원래 상세 Run/evidence 문서는 [`G-001.md`](go2/G-001.md)에 그대로 있다.
- [`G-001`–`G-006`](go2/)은 당시 수집된 Run·가설 관련 legacy 주소다. `G-005`의 original4800과 recovery4900을 한 Run으로 병합하거나, 평가·영상·제출을 새 training Run으로 바꾸지 않는다.

## 신뢰 경계

Release title, checkpoint 번호, `model_best` 또는 변경된 reward descriptor만으로 Run의 부모·정확한 입력 SHA·완료 상태를 단정하지 않는다. PERSONAL, OFFICIAL, 실제 제출, 공식 채점은 원본 evidence별로 확인한다.
