# H1 lin=.65 / ang=.60 / action=-.0003 model4950 정책 분석 수납

## 원문과 정책 연결

- [보고서](../../../incoming/other/reviewed/H1_JOINT-LIN065-ANG060-ACT0003_POLICY_ANALYSIS_20261017/H1_JOINT-LIN065-ANG060-ACT0003_POLICY_ANALYSIS_20261017.md) · [수신 ZIP](../../../incoming/other/reviewed/H1_JOINT-LIN065-ANG060-ACT0003_POLICY_ANALYSIS_20261017/H1_JOINT-LIN065-ANG060-ACT0003_POLICY_ANALYSIS_20261017.zip). ZIP 1,850,907bytes, SHA256 `3308cf65727cba71d237367b9d5db57d3a06ec990fcb37e8b06d680e30d6075f`. ZIP과 내부 15파일(보고서·집계 CSV3개·validation·프레임 감사표·그림/접촉시트8개·재계산 코드)을 원문 bytes 그대로 보존했다.
- Experiment [joint tracking balance](../../../../../research/experiments/h1/exp-h1-joint-tracking-balance.md), 실제 OFFICIAL fresh Run `20261017-015509-h1-lintrack-065-angtrack-060-actrate-0003-fresh5`. `h1-submit-2 + lin=.65 + ang=.60 + action=-.0003`, feet=.20/termination=-50 유지, seed42/4096env, 5000요청/console4999, COMPLETED/exit0/PASS.
- 분석 checkpoint는 keeper **model_4950.pt**, SHA `2df0584057deb4dc15ab3c4470d52da29e5468bbb819fe3e4c66a928462bc478`. 기존 공식 train index 및 [PERSONAL 평가 Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261017-exp-h1-joint-tracking-balance-model4950-video-eval)와 일치한다. 평가 ZIP SHA `f431ea153ffe6245fe29f781a3201239029922bc432f07bf1683a014e9cd46b3`. auto-best4800 및 다른 LINTRACK-065 fresh5K keeper4950(`b7528923…`)과 다르다.

## 판정과 주요 수치

**분석 수신 완료 / 공식 제출 대체 후보 HOLD.** 생존·전진·경사·밀침은 긍정 신호지만 rough 목표 속도 부족과 비의도 위치 잔류가 있다. 단독 정책 보고서이므로 세 reward의 독립 효과·기준 정책 대비 승리·공식 점수 개선으로 해석하지 않는다.

| 보고서 지표 | 값 |
| --- | --- |
| PERSONAL camera-off 평가 | 128env×3seed×8case, 3072/3072 timeout 생존·접촉 종료0 |
| H1 body x 적분 / world 종료 순변위 크기 | −.259 / .460m |
| H2 body 전진 / 명령 적분 | 14.820 / 15m |
| H3 vy 절대오차 / body x 누수 / world 종료 순변위 | .07476m/s / −.202m / .739m |
| H4 yaw 절대오차 | .07308rad/s |
| H5 진행 평균 / P05 / 최소 | 8.853 / 8.403 / 7.930m (명령 적분10m) |
| H5 stall>.05 | 0/384; 완전 정체가 아닌 지속적 저속 |
| H6 상행 / 하행 body 전진 | 19.992 / 19.814m |
| H7 body 전진 / 명령 적분 | 9.688 / 10m |

수납자는 패키지 CRC, policy/input SHA의 기존 기록 연결, CSV·validation과 보고서 주요 수치를 대조했다. **원 episode 재집계·첨부 코드 실행·MP4 재판독은 하지 않았다.** `validation.json`의 archive_entries=18은 입력 평가 ZIP이고 수신 분석 ZIP은 15파일이다. 서로 다른 묶음이다.

## 해석과 영상 확인의 범위

- H3의 위치 원점 복귀는 공식 속도 명령 자체가 아니다. world 잔류 .739m는 보조 경로 진단이며 공식 실패 횟수로 환산하지 않는다. H1 signed body x와 world 순변위 크기도 별도 지표다.
- 원 보고서는 첫4영상 검정 프레임 전수검사에서 f0만 black, 경사2영상에서는 선택 프레임만 확인했다고 명시한다. 6영상 f999 본체 소실은 보고서가 기록한 종료 경계 화면 이상이며 물리 낙상으로 세지 않는다. 연속 행동 전수 판독·정량 회복시간 측정·6영상 전체 무결함 증명은 아니다. 수납자가 이를 재검증했다고 주장하지 않는다.
- 계단·박스 중앙 완주 미입증은 보조 관찰의 공백이고 H1 공식 시나리오 단독 REJECT 기준은 아니다. 평가 snapshot의 baseline reward는 실제 학습의 세 변경값을 대체하지 않는다. 원 evaluation source_run_id/preset=null을 그대로 유지한다.
- 이전 LINTRACK0654950 수치와의 대조는 과거 보고서 숫자의 문헌 비교일 뿐이다. 기존 원자료의 protocol·source·cohort를 이번 보고서에서 직접 맞춘 것은 아니므로 paired 효과나 통계적 우위는 미확정이다.

## 후속 상태

원문은 기존 LINTRACK065 fresh5K 평가와 이번 JOINT4950의 **저장 raw CPU 비교**를 제안했다. protocol/resolved config/source fingerprint/명령/cohort를 먼저 확인하고 H3 이득과 H1/H5/H6 비용을 함께 보자는 계획이며 **미실행**이다. 평가 seed3개는 독립 학습 반복3개가 아니다. 이번 수납은 새 GPU 작업·제출·공식 점수·Optuna Tell을 실행하거나 다음 PLANNED 가설을 자동 승인하지 않는다. AI 핵심팩 00/14/20/21에 요약·해석 경계를 연결했다.
