# [학습] Go2 장기 학습 발산 — 운영진 답변 기반 판단

> 관리 안내 (2026-10-13): **학습** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](../../../../../research/EXPERIMENTS.md)를 확인한다.

- 답변 일시: 2026-08-30
- 출처: 사용자가 보존·제공한 운영진 Discord 답변 전문
- 적용 범위: Go2 개인 검증과 예선 제출용 학습의 구분
- 근거 등급: 운영진의 직접 답변은 **공식 운영 방침의 1차 근거**다. 9,500 iteration의 수치·checkpoint 상태는 사용자의 개인 실행 원본 분석 근거이며, 공식 서버 측의 재현 결과는 아니다.

## 확인된 운영진 답변

1. 장기 Go2 학습의 수치 발산은 알려진 현상이다. 특정 iteration(예: 9,500)을 넘으면 반드시 발생하는 결정적 오류가 아니며, 오래 돌릴수록 위험이 커지는 수치 불안정으로 보고 있다. 발산 없이 끝난 실행도 있었다.
2. 현재 배포 PPO 설정은 의도적으로 유지된 값이다. 과거 학습률을 낮춘 설정에서는 약 300회에 탐색이 수축해 제자리 회전 국소최적에 갇힌 사례가 있어, 발산 위험을 인지한 상태에서 정상 학습이 확인된 설정으로 되돌렸다고 설명했다.
3. 개인 검증 환경에서는 장기 학습 진단을 위해 learning rate를 낮추거나 `desired_kl=0.008`을 시험할 수 있다고 안내했다.
4. 그러나 **예선 제출 정책은 배포된 학습 설정 그대로 학습해야 한다.** 제출용으로 조절할 대상은 reward 설계와 iteration 수이며, PPO 학습 설정 변경은 개인 진단 실험과 분리한다.
5. `lin_vel_z_l2`, `ang_vel_xy_l2`를 포함한 reward 항목은 참가자 실험 대상으로 열려 있다. 단, 추천 범위를 참고해야 하며 두 안정화 항을 동시에 범위 밖으로 약화하면 수직 진동·몸통 회전이 잡히지 않아 value loss 발산 위험이 커질 수 있다.
6. 정답 iteration 수는 제시되지 않았다. 10,000회 이내에도 충분히 좋은 결과가 나올 수 있고, 오래 학습한다고 자동 점수가 계속 오르지는 않는다. 운영진 설명상 자동 점수의 관찰 기준은 생존과 명령 추종의 결합이다.
7. 사용자의 run은 9,500 시점에 terrain 난이도 5.85, 낙상 1.9%로 상당히 안정적이었다고 운영진이 평가했다. checkpoint가 100회마다 저장되므로 실제 발산 뒤에도 `model_9500.pt` 같은 발산 전 모델은 보존될 수 있다.
8. 운영진은 발산 시 report가 부정확한 조언을 주는 문제를 확인했고 수정 예정이라고 밝혔다. 이는 현재 로컬 mirror에 수정이 있다는 뜻이나, 공식 운영 서버에 언제 배포되는지까지 보장하지 않는다.

## 이 답변으로 확정하지 않는 것

- value loss가 왜 최초로 발산했는지의 정확한 수치 원인
- 5k·9.5k·10k 중 어느 iteration이 모든 reward 설계에 최적이라는 결론
- 개인 L40S 실행과 공식 서버가 런타임까지 동일하다는 주장
- 현재 혹은 미래 공식 서버에 report 수정이 이미 배포됐다는 주장
- `model_9500.pt`의 실제 예선 점수 또는 제출 적합성

## 실험 운영에 반영할 규칙

| 상황 | 허용된 판단 |
| --- | --- |
| 개인 검증에서 발산 원인을 좁히는 진단 | PPO learning rate·`desired_kl` 변경을 별도 실험 ID로 기록할 수 있다. 해당 정책은 제출 후보와 섞지 않는다. |
| 예선 제출 후보 학습 | 배포된 PPO/agent 설정을 그대로 두고 reward와 학습 iteration만 바꾼다. |
| 안정화 reward 변경 | `lin_vel_z_l2`와 `ang_vel_xy_l2`를 동시에 크게 약화하지 않고, 추천 범위·report 경고·영상·value loss를 함께 본다. |
| 긴 run의 checkpoint 선택 | 마지막 checkpoint만 보지 않는다. 100회 간격 checkpoint, terrain·fall·tracking 시계열, 재생 영상을 같은 평가 조건에서 비교한다. |
| 발산 뒤 판단 | `std` 오류만 최초 원인으로 단정하지 않는다. 이전 value loss, reward term, action std, actor/critic/optimizer finite 상태를 먼저 보존·검토한다. |

## Go2 baseline 해석 변경

개인 12k 요청 run은 약 9.5k 뒤 발산했지만, 이 사실만으로 baseline 전체가 무효가 되지는 않는다. 발산 전 `model_9500.pt`는 개인 비교 B0로 보존할 수 있다. 다만 장기 실행 성공 여부가 확률적일 수 있으므로, reward 효과를 비교할 때에는 요청 iteration, 실제 저장 checkpoint, 중단·발산 상태, 동일 horizon evaluator 결과를 각각 기록한다.

5k는 빠른 screening, 약 9.5k는 같은 horizon의 비교, 그보다 긴 실행은 추가 안정성 확인이라는 기존 구분을 유지한다. 각 단계는 자동 점수의 대리 지표가 아니라 후보 간 상대 비교다.

## 관련 자료

- 개인 run 원본 분석: [2026-08-30_GO2_BASELINE_CONVERSATION_SUMMARY.md](../2026-08-30_GO2_BASELINE_CONVERSATION_SUMMARY.md)
- AI 핵심 판단: `data/processed/ai_library/05_TRAINING_RULES_AND_SUBMISSION.md`, `07_QUADRUPED_TRAINING_CODE.md`, `15_OPTUNA_REWARD_DECISION_ENGINE.md`, `16_EXPERIMENT_EXPORT_AND_TENSORBOARD.md`
