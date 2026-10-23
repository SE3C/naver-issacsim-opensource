# H1 LINTRACK-075 + ACTRATE-0001 model2850 — 보고서 수신 / HOLD

## 원문 보존과 확인 범위

[받은 보고서](../../../incoming/other/reviewed/H1_LINTRACK075_ACTRATE0001_TERM50_FRESH3K_MODEL2850_POLICY_ANALYSIS_20261018/H1_LINTRACK075_ACTRATE0001_TERM50_FRESH3K_MODEL2850_POLICY_ANALYSIS_20261018.md)와 [원본 ZIP](../../../incoming/other/reviewed/H1_LINTRACK075_ACTRATE0001_TERM50_FRESH3K_MODEL2850_POLICY_ANALYSIS_20261018/H1_LINTRACK075_ACTRATE0001_TERM50_FRESH3K_MODEL2850_POLICY_ANALYSIS_20261018.zip), 내부25파일을 bytes 그대로 보존했다. ZIP **2115107bytes**, SHA256 `4ae1a878c2279b5b5166671db7abfb11ab8c31b5ef757361e50effbba2e4172a`, CRC PASS.

보고서 표와 첨부 [case CSV](../../../incoming/other/reviewed/H1_LINTRACK075_ACTRATE0001_TERM50_FRESH3K_MODEL2850_POLICY_ANALYSIS_20261018/derived/case_metrics.csv), [seed CSV](../../../incoming/other/reviewed/H1_LINTRACK075_ACTRATE0001_TERM50_FRESH3K_MODEL2850_POLICY_ANALYSIS_20261018/derived/seed_case_metrics.csv), [summary JSON](../../../incoming/other/reviewed/H1_LINTRACK075_ACTRATE0001_TERM50_FRESH3K_MODEL2850_POLICY_ANALYSIS_20261018/derived/summary.json)을 대조했다. 원 episode 재집계, 첨부 Python 실행, MP4 재판독, GPU 작업은 하지 않았다. 원 episode·checkpoint·MP4는 이 보고서 ZIP에 없으며 아래 결과는 외부 보고서의 분석값이다.

## 학습 Run과 평가 연결 — 원문의 미확인 상태 보완

[Experiment와 원본·Release](../../../../../research/experiments/h1/exp-h1-action-planar-tracking-fresh-interaction.md): OFFICIAL Run `20261017-140610-h1-lintrack-075-actrate-0001-term-50-fresh3k`, fresh/no parent, seed42/4096env/3000요청, **COMPLETED/exit0/PASS**. 실제 최종 override는 `h1-submit-2 + lin=0.75 + action=-0.0001`이며 ang=.50, feet=.20, termination=-50 유지. 전체 설정은 보존된 native env/agent/reward source를 따른다.

- 분석 대상 **model_2850.pt**, SHA256 `8238421049335a19c288986ed58aa84f01468da315fbf6c355ee45088934f959`는 공식 train checkpoint index와 PERSONAL 평가 publication에 일치한다. 최신 keeper **model_2950.pt**, SHA `952330c4d95c61e5104e446fdf947a94c38ad7feac6e4806b8164d709826fba3`는 다른 미평가 정책이다.
- [Eval publication](https://github.com/SE3C/naver-issacsim-eval/blob/main/publications/2026-10-18_h1_lin075_action0001_model2850/publication_manifest.json)의 원본 평가 ZIP SHA `bafeffabcc0e3d7c5b8e0548f2f6dc491c98607b2d9b49ec53c2ff1a1e353f2f`; PERSONAL Windows camera-off H1 scenario7 COMPLETE/non-smoke,128env×seeds4201/4202/4203×8case=3072행,20초. Protocol `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34`.
- 원문의 “조회에서 SHA/학습 출처 미확인”과 원시 평가 `source_run_id/preset=null`은 그대로 보존한다. 현재 보존된 train index와 위 publication의 SHA 연결로 별도 보완한 것이며, 원문·raw null을 고친 것이 아니다. 평가 환경의 baseline reward snapshot은 실제 학습 reward가 아니다.

## 보고서 핵심 결과

각 case384행,8case 전부 합3072행이20초 timeout이고 contact/terminated0. 생존은 추종 정확도·장애물 완주와 별개다.

| 축 | 보고된 결과 |
| --- | --- |
| H1 정지 | body 비의도 전진0.298m, world XY 종료 순변위 평균0.857m. |
| H2 전진 | body 진행15.107m / 명령 적분15m. |
| H3 좌우 | body 비의도 전진0.277m, world 종료 순변위2.605m. 원점 복귀는 공식 독립 채점 항목이 아닌 보조 진단이다. |
| H4 회전 | yaw 절대오차 **0.2725rad/s**. |
| H5 rough | body 진행 평균/P05/최소 **9.867/9.640/9.514m**, yaw 오차 **0.2730rad/s**, stall>.05 **0/384**. 주약점은 장기 정체보다 방향 추종이다. |
| H6·H7 | 경사 상/하 진행20.113/19.967m, 밀침10.126m. |

전체 episode 혼합 tracking **0.251289**, yaw오차0.22279rad/s, action Δ RMS0.57558. 혼합 지표는 공식 Tracking Score나 점수가 아니다. body-frame 적분은 world 전진거리·총 경로 길이와 다르며 action Δ로 slip/torque를 직접 측정했다고 쓰지 않는다. 3개 평가 seed는 독립 학습 seed3회가 아니다.

## 영상 결함과 판정

보고서와 [video probe](../../../incoming/other/reviewed/H1_LINTRACK075_ACTRATE0001_TERM50_FRESH3K_MODEL2850_POLICY_ANALYSIS_20261018/derived/video_probe.json)는 **03_boxes.mp4 짝수500/1000프레임 black·홀수 정상**을 기록한다. 전체 black 또는 낙상이 아닌 교대 capture artifact이며 이번 수납자의 독립 렌더 재현은 아니다. rough는 f0/f2 black, 여섯 영상 f999 몸체 소실도 보고됐다. 선택 인접 프레임 관찰과 전1000프레임 기초 검정 검사는 전프레임 행동의 수동 판독과 다르다. 원인 확정·실행기 수정은 이번 수납 범위가 아니다.

**HOLD — 현재 제출 대표 대체·승격 없음.** 진행·rough 하위 꼬리는 보존 가치가 있으나 H3 위치 잔류와 H4/H5 yaw 및 action 비용이 크다. 계단 중앙 완주 미입증 자체는 H1 공식 후보 탈락 이유가 아니다. 과거 TERM50/2800·ACTRATE0001/2700과의 표는 저장 집계의 미대응 참고이지 새 paired A/B가 아니다. 기존 평가 조건을 확인한 CPU 비교가 제안됐으나 실행하지 않았다. reward 인과·공식 점수·새 제출·추가 학습 승인은 없다. 이 단일3K 정책의 HOLD를 해당 설정의 10K 실패 확정으로 확대하지 않는다.
