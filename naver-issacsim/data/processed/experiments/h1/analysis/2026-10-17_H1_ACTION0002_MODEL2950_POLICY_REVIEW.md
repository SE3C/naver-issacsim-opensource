# H1 action=-0.0002 model2950 정책 분석 패키지 수납

## 원문과 provenance

- [수신 보고서](../../../incoming/other/reviewed/H1_ACTRATE0002_MODEL2950_POLICY_ANALYSIS_20261017/H1_ACTRATE0002_MODEL2950_POLICY_ANALYSIS_20261017.md) · [원본 ZIP](../../../incoming/other/reviewed/H1_ACTRATE0002_MODEL2950_POLICY_ANALYSIS_20261017/H1_ACTRATE0002_MODEL2950_POLICY_ANALYSIS_20261017.zip). ZIP 1,373,408bytes, SHA256 `2499b22ac29de1757b2dcf23fdf73a98900686f169447fb1888a56b7963b3db7`; 보고서 18,757bytes, SHA256 `3bea22dbfbd4d08d3a1e5c746d62df052f8d32e2d2141cc592e84c8d9b6c12c7`. ZIP과 내부 14파일을 그대로 보존했다. 보고서 1개, CSV 3개, validation JSON, 그림 8개, 재현 코드 1개다.
- Experiment [action-rate relaxation](../../../../../research/experiments/h1/exp-h1-action-rate-relaxation.md), OFFICIAL fresh3K Run `20261016-150803-h1-actrate0002-fresh3k`. 학습은 `h1-submit-2 + action_rate_l2=-0.0002`, seed42/4096env, COMPLETED/exit0/PASS다.
- 분석 대상은 indexed keeper2950 SHA `eaa7a50c51fbdf3b39c15fe4278d1c9def38f96e9af872eb37111b66ac4d34fb`. [PERSONAL 평가 Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261017-exp-h1-action-rate-relaxation-action0002-model2950-video-eval)의 ZIP SHA `f658b2217737e5271caaf4eaa3c0ac48f29d1929d680a1688da509a0d87b3c3c`와 보고서 입력이 일치한다. auto-best·console endpoint와 구분한다.

## 결론과 확인 범위

**보고서 수신 완료·정책 HOLD.** H1 공식 제출 경쟁력과 계단·박스 보조 영상 관찰을 구분한 단독 정책 분석이다. 상대 정책 ZIP이 없어 A/B 우위·reward 인과·공식 점수 개선은 판단하지 않는다.

| 보고서 지표 | 값 |
| --- | --- |
| 평가 | 3072행·3072고유 cohort·8case, 전부20초 timeout/생존 |
| H1 비의도 body 전진 / world 종료 잔류 | 1.842 / 1.835m |
| H3 비의도 body 전진 / world 종료 잔류 | 1.225 / 1.046m |
| H5 진행 평균 / P05 / 최소 | 8.941 / 8.573 / 6.983m |
| H5 stall > .05 | 3/384 cohort |
| H2 / H7 body 전진 | 14.599 / 10.115m |
| H6 상행 / 하행 body 전진 | 19.775 / 19.661m |

수납의 독립 확인은 policy/input SHA의 기존 게시 기록 연결, 패키지 CSV·validation JSON과 본문 주요 수치 일치다. **원 episode 재집계·MP4 판독·첨부 코드 실행은 하지 않았다.** 원문이 기록한 영상 확인은 앞 3개 전프레임 black 검사와 뒤 3개 표본 검사이며, 이를 이번 수납자의 독립 영상 검증으로 바꾸지 않는다. 프레임 contact sheet는 보고서 파생자료이고 원본 영상은 기존 평가 ZIP에 있다.

**해석 보정:** H1의 zero-command 비의도 이동은 직접적인 정지 제어 진단이다. 그러나 H3의 목표는 좌우 속도 명령 추종이며, world 종료 잔류가 크다는 이유만으로 공식 원점복귀 실패라 부를 수 없다. 원문의 “횡이동 복귀 실패”는 이 범위로 제한해 읽는다. H3 vy 오차와 비의도 vx를 함께 보며 원문 bytes는 수정하지 않는다. 계단 중앙 통과 미입증도 H1 공식 시나리오의 자동 탈락 조건은 아니다.

평가 resolved reward `action=-.0005`는 평가 snapshot이고 실제 학습 reward는 별도 OFFICIAL archive의 `-.0002`다. 평가의 null source_run_id/preset도 변경하지 않는다.

## 후속 상태

원문은 기존 기준 정책과 저장 평가 ZIP의 parity 확인·CPU cohort 비교를 제안한다. 이번 수납에서는 실행하지 않았다. 새 학습·GPU 평가·렌더·제출·공식 점수·Optuna Tell은 없고, 기존 미실행 가설의 우선순위를 자동 확정하지 않는다. 원본 패키지 보존과 registry·분석 색인 연결에 이어, 사용자 후속 요청으로 AI 핵심팩 00/14/20/21에 결과와 해석 범위를 반영했다. 원문·첨부 자료는 변경하지 않았다.
