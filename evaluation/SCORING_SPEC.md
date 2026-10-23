# 점수 산정 명세 v1

핵심 구현은 `eval_core.py`이며 Isaac Sim 없이 JSONL과 manifest만으로 실행된다. `isaac_runner.py`는 별도의 데이터 수집 어댑터다. 실행·반복·서버 운영을 다른 에이전트에 맡겨도 아래 계산 순서와 데이터 계약은 바꾸지 않는다.

## 1. 입력과 비교 단위

정책 한 개마다 독립 평가 결과를 만든다. 최소 입력은 body-frame 명령 대비 추종 오차, 종료 사유, episode 길이, scenario/case/seed/env 식별자다. 정책 SHA와 실행 프로토콜도 기록한다.

`scenario7`: 환경 하나를 고정 시간창 동안 평가하고, 낙상 때마다 실패 episode를 남긴다. reset 이후 새 episode도 계속 기록한다. 시간창 끝에 진행 중인 episode는 생존이며, 마지막 step에서 종료한 경우 존재하지 않는 새 episode를 추가하지 않는다.

`terrain6`: 환경마다 첫 episode 하나만 평가한다. 일찍 낙상하면 실패로 끝내고 다시 시작한 episode는 집계하지 않는다. 두 방식은 서로 다른 질문이므로 점수/프로토콜을 섞지 않는다.

## 2. 추종 오차 → Tracking

step t의 오차:

`e_t = sqrt((vx_actual-vx_command)^2 + (vy_actual-vy_command)^2 + (yaw_actual-yaw_command)^2)`

세 축에 임의 가중치나 단위별 정규화를 추가하지 않는다. 이는 공개 답변에 맞춘 오차 정의이며 내부 변환식의 공식성을 뜻하지 않는다.

episode j의 step 수가 n_j이면:

`E_j = sum(e_t) / n_j`

시나리오 s에 포함된 episode 수가 N_s이면:

`E_s = sum(E_j) / N_s`

episode는 길이와 관계없이 동일 가중치다. 모든 step을 합쳐 긴 episode에 더 큰 가중치를 주거나, episode마다 비선형 점수를 먼저 만들어 평균하지 않는다. 여러 case가 있는 시나리오도 모든 episode를 이 원칙으로 집계하므로 낙상이 잦은 case는 더 많은 episode를 남긴다. 이를 감추지 않도록 case별 수치도 별도로 출력한다.

내부 Tracking 함수:

`T_s = exp(-ln(2) * E_s / e50_s) = 2^(-E_s/e50_s)`

`e50_s > 0`이고 오차 0이면 Tracking 1, 오차 e50이면 0.5다. 공식 비공개 변환식을 추정했다고 주장하지 않는다.

## 3. Survival → 전체 점수

terminated는 실패다. timeout과 평가 종료 시 진행 episode는 생존이다. terminated와 timeout이 동시에 발생하면 실패가 우선한다.

`S_s = survived_episode_count / N_s`

`Q_s = S_s * T_s`

`PolicyScore = 100 * sum(w_s * Q_s)`

각 w_s는 음수가 아니고 합계는 1이다. H1과 Go2는 서로 다른 시나리오/가중치/경사 기준을 쓴다. 두 로봇의 점수를 직접 순위화하지 않는다. reward 총합, 리포트 점수, 영상 인상점은 이 점수에 넣지 않는다.

## 4. Calibration의 의미

reference 정책을 같은 프로토콜로 평가하고 시나리오별 episode-error 중앙값을 초기 e50으로 잡는다. 이는 calibration 초안이지 정답 학습이 아니다. 중앙값이 0이면 임의 epsilon을 넣지 않고 중단한다.

후보를 보기 전 reference/negative control·e50·방법·근거를 검토해 버전을 동결한다. 후보마다 e50을 다시 맞추거나 A/B마다 다른 calibration을 사용하면 비교가 성립하지 않는다. suite hash와 reference protocol이 다른 calibration도 거부한다.

공식 제출 점수 몇 개와 외부 실패 사례만으로 공식 함수를 fit하지 않는다. 관측되지 않은 공식 command·seed·난이도 차이가 섞여 있기 때문이다.

## 5. A/B와 신뢰구간

같은 `(scenario, case, seed, env_id)`를 paired cohort로 본다. 낙상/reset 횟수가 다르므로 episode 1↔1 같은 인위적 pairing은 하지 않는다.

bootstrap 반복마다 seed를 복원추출하고, 각 seed/scenario/case 안의 env cohort를 복원추출한다. A/B에는 같은 cohort 선택을 적용하고 그 cohort의 모든 episode를 유지한다. 그 표본에서 위 점수를 다시 계산하여 `Δ = Score_A - Score_B`를 구한다. 기본 1,000회 Δ의 2.5/97.5 percentile이 95% 구간이다.

- 구간 전체가 0 초과: `A_HIGHER`.
- 구간 전체가 0 미만: `B_HIGHER`.
- 동일 점수·동일 0 구간: `TIE`.
- 그 외: `INCONCLUSIVE`.

이는 **표본 cohort 안에서의 내부 점수 비교**다. 단일 seed의 CI가 좁다고 seed 간 재현성이 증명되지는 않는다. `ranking_ready`는 최소 3 seed와 frozen calibration이 있어야 true지만, true라도 자동 제출 승격을 의미하지 않는다. 같은 seed도 reset 이후 완전히 동일한 지형/상태 궤적을 보장하지 않는다. 현재 CI는 A/B 차이에 대한 것이며 단일 정책 절대점수의 CI를 따로 제공하지 않는다.

## 6. 생존과 실제 보행을 분리

각 시나리오/case에서 축별 오차, XY/yaw RMSE, base-contact 실패율, world X/Y 변위, 몸통 전진 속도 적분, stall, roll/pitch RMS, raw action 변화량과 coverage를 함께 출력한다.

stall은 평면 명령 속도 ≥0.2m/s인 step 중 실제 평면 속도 <0.1m/s인 비율이다. 제자리 균형 명령에는 적용하지 않는다. 이 정의는 저속 정체를 포착하며 미끄러짐·제자리 회전·뒤로 걷기 전체를 완벽하게 분류하는 알고리즘은 아니다. 축별 오차와 실제 변위를 같이 본다.

회전하면서 몸통 기준 앞으로 걸으면 속도 적분은 양수여도 세계 X 변위는 0 또는 음수일 수 있다. 두 값을 같은 거리로 부르지 않는다. world 변위가 크다고 계단 완주를 자동 인증하지도 않는다.

정체·동작 품질 진단을 몰래 전체 점수에 곱하지 않는다. 상당한 stall 또는 진단 누락은 경고와 별도 지표로 드러낸다. 100% 생존하는 역계단 stall을 지형 통과 성공으로 채택하면 안 된다. 공개 타 팀 실패 기록은 이런 진단 항목을 정하는 prior이지 calibration 정답이 아니다.

## 7. 점수 생성 거부 조건

incomplete manifest, 누락/중복 cohort·episode, 정책/프로토콜 불일치, 잘못된 종료/생존 조합, 비유한 또는 음수 추종 오차, 부족한 평가 시간, 잘못된 calibration이면 점수를 내지 않는다. 음수 세계 변위·몸통 속도 적분은 유효한 관측이다. optional 진단 누락은 coverage로 표시하며 측정된 0으로 바꾸지 않는다.

완료 판정, 내부 수치 우위, 정책 품질, 공식 제출 적격성은 각각 별개다. 이 평가기는 학습·best checkpoint 선택·policy export·게시·서버 종료를 수행하지 않는다.
