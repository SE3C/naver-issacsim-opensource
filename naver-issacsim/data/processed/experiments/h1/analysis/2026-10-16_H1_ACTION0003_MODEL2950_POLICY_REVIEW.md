# H1 action=-0.0003 model2950 정책 보고서 수납

## 원문·실행 연결

- [제공 보고서 원문](../../../incoming/other/reviewed/H1_ACTRATE-0003_POLICY_ANALYSIS_20261016.md): 23,666bytes, SHA256 `7565132f80068c36509609540e14f330b246e6fa38f14d46dbeba88831fbba87`, bytes 그대로 보존.
- Experiment [`exp-h1-action-rate-relaxation`](../../../../../research/experiments/h1/exp-h1-action-rate-relaxation.md), OFFICIAL fresh3K Run `20261016-033023-h1-actrate-0003-fresh3k`, `h1-submit-2 + action_rate_l2=-0.0003`, seed42/4096env, requested3000/console2999, COMPLETED/exit0/validation PASS. 전체 설정·source는 기존 학습 archive에 있다.
- 평가 keeper `model_2950.pt`, SHA `1cc2c03197097c21c642e8373c760b25664b9c859ed75b5dc07582a770473c4b`; auto-best2900/endpoint2999와 다르다. [PERSONAL 평가 Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261016-exp-h1-action-rate-relaxation-action0003-model2950-video-eval). 원문·평가 ZIP·학습 원본을 재게시하거나 수정하지 않았다.

## 보고서 결론과 확인 범위

**HOLD 유지, 범용 제출 대체 후보로 PROMOTE하지 않음.** 보고서는 3072행을 재집계하고 실제 영상의 선택·인접 프레임을 확인했다. 수납 과정의 독립 확인은 checkpoint SHA, complete/non-smoke, 고유 cohort3072개·8case·seed4201–4203, 전부20초 timeout/낙상0, diagnostics의 scenario별 추종 평균 일치다. 영상 판독은 이번 수납자가 재수행하지 않았다.

- 원문상 body-frame 진행: H2 **14.930m/명령15m**, H7 **9.796/10m**, 경사 상·하 **20.049/19.856m**. 생존과 실제 진행이 공존한다.
- H5 rough mean/P05/min **9.018/8.664/6.771m**; 두 cohort의 stall .225/.085. 생존100%가 저속·정체 꼬리를 없애지 않는다.
- H1 비의도 전진 **.382m**, 종료 world XY 잔류 **.455m**; H3 vy오차 **.07035m/s**, 종료 world XY 잔류 **.407m**. world 종료 잔류는 공식 추종 점수나 원점복귀 명령의 성공률이 아니다.
- 원문 영상 관찰: 첫 프레임 black, 마지막999프레임 몸체 소실 경계 이상; 조사한 중간 표본에 교대 black은 없으나 전프레임 자동검사는 아님. 계단 중앙 다단 연속 통과 미입증. 캡처 결함을 낙상으로 세지 않는다.
- 과거 model2700 기록과 누수 개선/험지 진행 손해 가능성이 있으나 이번 보고서는 상대 ZIP 전체를 대조하지 않았다. checkpoint 선택·학습경로·평가계약을 확인하기 전 통제된 reward 효과나 공식 점수 향상으로 해석하지 않는다.

## 다음 단계의 상태

후속 AI 라이브러리 요청에 따라 기존 00/06/14/15/20/21 및 구성 가이드의 실제 완료 상태·HOLD·미실행 resume 구분에 반영했다. 원문 보고서는 변경하지 않았다.

원문은 기존 model2700 우선, TERM50 model2800 보조로 **저장 ZIP CPU 비교**를 제안했다. 이 보고서 수납에서는 그 비교를 실행하지 않았다. 새 GPU 학습·렌더·평가·제출은 없고, 해당 후보의 공식 점수도 없다. 기존 계획은 본 보고서 수신 전 제안으로 보존하며 후속 우선순위를 자동 확정하지 않는다.
