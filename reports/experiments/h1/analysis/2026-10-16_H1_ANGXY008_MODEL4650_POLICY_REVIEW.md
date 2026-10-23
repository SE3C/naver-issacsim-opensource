> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/experiments/h1/analysis/2026-10-16_H1_ANGXY008_MODEL4650_POLICY_REVIEW.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# H1 angxy=-0.08 model4650 보고서 수납·저장 raw 5정책 비교

## 수신·보존·계보

- [제공 보고서 원문](<../../../received/H1_ACTRATE0001_ANGXY008_MODEL4650_POLICY_ANALYSIS_20261016.md>): 22,751 bytes, SHA-256 `25a3b5777ee75f60b23bfb976430a692659461d549da73ac2a9974d66a44a622`. 내용 bytes 그대로 보존했다. 원문의 영상 판독을 이번 작업자가 다시 수행했다고 쓰지 않는다.
- 실제 OFFICIAL 학습 Run `20261015-143107-h1-actrate0001-angxy008-from2700-plus2k`: completed/exit0/validation PASS, seed42/4096env, 부모2700에서 +2000 요청·console4699/4700. [상세·원본 학습 Release](<../../../../research/experiments/h1/planned/exp-h1-action-first-body-rate-switch.md>).
- 평가 정책은 keeper `model_4650.pt`, SHA `c272b13b5d3702c8a84c1470b597526efe2214d0ee38f34f65918c5f912a335f`. endpoint4699·automatic-best3400·다른 실험의 동명4650과 구분한다. 부모2700 SHA `e54d3389e20ea913968ef8d3edbea5004368ff225fa6b94f73fcd91cf93ca7ae`의 외부 연결은 raw imported-parent null/unverified를 수정하지 않는다.
- 기존 PERSONAL [평가 Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261016-exp-h1-action-first-body-rate-switch-angxy008-model4650-video-eval)와 Originals 보존본은 이미 있다. 입력 ZIP SHA `522c8b6a6bc2e1a9ae99e1fdf86308b7a335c7bb6c2964c03ad6b3875be51d22` 일치. 동일 산출물을 다시 게시하지 않았다.

## 원문 판정과 이번 추가 확인

원문은 **HOLD**다. 모든 3072 episode가 20초 timeout이고, rough H5 진행 평균/P05/최소는 **7.972/7.230/6.374m**, stall 평균 .01145다. 주된 문제는 잦은 완전 정체보다 **목표 속도보다 느린 진행**이다. H3 종료 world XY 평균 .258m는 보조 진단이며 명령이 world 원점 복귀를 요구한 것은 아니다. 계단 중앙 다단 완주는 원문도 미입증으로 남겼다.

원문이 제안한 다음 CPU 비교는 **이번에 완료**했다. 재현 코드〔원본 참조: `2026-10-16_ANGXY_SAVED_COMPARISON/reproduce.py` / 공개 사본 미포함〕, [case/seed 요약](<2026-10-16_ANGXY_SAVED_COMPARISON/case_seed_summary.csv>), [angxy−대조군 차이](<2026-10-16_ANGXY_SAVED_COMPARISON/angxy_minus_reference.csv>), [입력 SHA·검증](<2026-10-16_ANGXY_SAVED_COMPARISON/verification.json>)을 보존한다. 외주 첨부 코드는 실행하지 않았고, 별도 작성한 CPU 집계만 수행했다.

5정책 × 3072행 = **15,360행**, 정책별 고유 case/seed/env 키·20초 timeout/1000steps·policy SHA를 검증했다. **evaluation protocol 전체와 resolved evaluation configs가 동일**했다. 이는 training source/PPO 동등성이나 실제 난수 지형·궤적 일치까지 증명하지 않는다. P05는 선형 보간 주변분포 5백분위이며 차이분포의 5백분위가 아니다.

| 정책 | H5 평균/P05/최소 진행 m ↑ | H3 vy 오차 m/s ↓ | H4 yaw 오차 rad/s ↓ | H6 상/하 roll-pitch RMS ↓ |
| --- | --- | ---: | ---: | --- |
| A 부모2700 | 9.948 / 9.592 / 8.815 | .06727 | .11832 | .03816 / .03550 |
| B 무변경4699 | 7.919 / 7.427 / 6.239 | .06825 | .09189 | .05637 / .05287 |
| C lin=.55 keeper4650 | 9.242 / 8.859 / 8.256 | .07139 | .11256 | .06895 / .06492 |
| D lin=.65 selected4650 | 9.546 / 9.228 / 8.974 | .05708 | .17906 | .07099 / .06497 |
| **E angxy=-.08 keeper4650** | **7.972 / 7.230 / 6.374** | **.08246** | **.11686** | **.07930 / .07557** |

- E vs B: H5 평균은 **+.05255m**에 그치고 P05는 **−.19671m**, H3 vy **+.01421m/s**, H4 yaw **+.02497rad/s**다. 경사 자세 RMS·action Δ도 B보다 높다. **몸통 벌점 강화가 실측 자세/횡속도 추종을 개선했다는 기대는 이 선택 정책들에서 지지되지 않는다.** 단, roll/pitch *각도* RMS는 벌점의 body XY *각속도*와 다른 지표라 reward가 적용되지 않았다는 뜻은 아니다.
- E vs A: H1 body 비의도 전진은 1.987→.010m(행별 절댓값 평균 .01447m)로 감소하고 H3 종료 world 순변위도 .669→.258m다. 그러나 H3 vy와 H5 진행 꼬리는 악화한다. 정지 누수 개선 하나로 범용 개선이라 부르지 않는다.
- E vs C/D: H5 평균·P05·최소 진행이 모두 낮다. 일부 yaw/world 종료 진단 이득은 전체 우월성을 뜻하지 않는다. D는 yaw 비용이 큰 별도 trade-off다.

**현재 판단: E HOLD 유지, 범용 PROMOTE 없음.** A/C/D HOLD, B의 기존 범용·전진/험지 대표 제외 판단은 유지한다. 새 학습·평가·렌더·export·checkpoint 토너먼트·공식 서버 변경은 없었다. 세 평가 seed는 독립 학습 반복 세 번이 아니고, A best2700/B endpoint4699/C-D-E keeper4650의 선택 차이도 남아 있다.

## 원문과 현재 기록의 차이

원문의 R6 “공식 점수 미수신”은 현재 사용자 제공 정보보다 오래됐다. 사용자는 **2026-10-11 23:19 H1 R6 제출의 공식 simulation 56.35/70, 종합86.35/100** 및 7개 점수 **8.60,11.30,5.73,5.68,8.02,8.52,8.50**을 전달했다(합계56.35). R2 56.37보다 .02 낮으며 E angxy 정책의 점수가 아니다. 이는 **사용자 전달 공식 결과**이고 이번에 포털/수령증을 직접 조회한 사실은 아니다. 원문·preset 설정·제출 policy bytes는 소급 수정하지 않는다.

또 원문 말미의 “CPU 비교 미완료”는 원문 작성 시점의 정확한 한계였으나 위 재집계로 해소됐다. 반대로 영상·중앙 계단 완주·training seed 반복의 공백은 해소되지 않았다.

## 이후 방향

[2026-10-16 연구 근거 기반 후속 계획](<../../../../research/planning/2026-10-16_H1_EVIDENCE_AND_RESEARCH_NEXT_EXPERIMENTS.md>)을 따른다. angxy 강화 반복·lin 임의 미세 sweep·부모2700 추가 연장을 자동 기본값으로 쓰지 않는다. 새 Run은 사용자 선택 후이며 어떤 학습도 이번에 시작하지 않았다.
