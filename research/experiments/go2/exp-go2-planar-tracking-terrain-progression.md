> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/research/experiments/go2/exp-go2-planar-tracking-terrain-progression.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# exp-go2-planar-tracking-terrain-progression

> **탐색용 Experiment 주소**. 이것은 새로운 가설·학습 Run·원본 문서의 복제가 아니다. 전체 연구 질문, 실제 reward 설정, 부모·checkpoint SHA, training/evaluation 근거와 과거 판정은 기존 [Go2 G-001 상세 기록](<G-001.md>)을 canonical로 사용한다.

## 연구 질문

평면 속도 추종 reward를 높이면 명령 추종과 지형 진행의 균형을 개선할 수 있는가? Historical display descriptor `LINTRACK-125`는 `track_lin_vel_xy_exp=1.25`이며, 전체 resolved config나 Experiment ID가 아니다.

## 실제 기록의 위치

- [G-001 legacy 상세 기록](<G-001.md>): 초기 PERSONAL screening, **별개 OFFICIAL fresh3K** Run `20260928-230114-go2-lintrack125-fresh3k-r5-official`, **별개 OFFICIAL fresh7.5K** Run `20260929-154342-go2-lintrack-125-fresh7500-official`, control/평가와 제출 계보. fresh7.5K는 3K를 resume한 것이 아니다.
- [현재 registry](<../../EXPERIMENTS.md>): completion, 실험 비교의 한계와 채택/보류의 현재 판정.
- [제출 snapshot](<../../submission_presets/README.md>): 실제 `g2-submit-5` 2026-10-06 제출, native `model_7450.pt` 연결 및 공식 평가 88.32/100. 제출 preset의 native `agent.yaml`은 별도 미동결 상태이므로 전체 preset이 완성됐다고 표시하지 않는다.
- Go2 Round-5 공식 평가〔원본 참조: `../../../data/processed/experiments/go2/2026-10-08_OFFICIAL_EVAL_GO2_ROUND5_LINTRACK125.md` / 공개 사본 미포함〕: 공식 구성 점수의 출처. 내부 PERSONAL 평가를 공식 결과로 바꾸지 않는다.

## 관리 주의

과거 `G-001`/`LIN-TRACK`/`G2`는 검색용 legacy 별칭으로 유지한다. 이름이 새 형식이라는 이유로 기존 Run ID를 변경하거나 새로운 training, matched control, 평가, evidence 또는 공식 제출을 만들지 않는다. 다른 날짜의 검증·분석 보고서는 원본 시점과 protocol을 보존한다.
