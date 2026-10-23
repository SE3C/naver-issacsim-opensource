---
id: planning-nvidia-server-operations
source_type: planning_analysis
category: server_operations
trust_level: mixed_code_confirmed_facts_and_recommendations
source: "data/raw/planning/NCRC_예선_개인_NVIDIA_서버_운영안.md"
---

> [!IMPORTANT]
> 이 문서는 사용자가 제공한 대회 준비 설계·권장안이다. 백업 코드에서 확인한 값과 구현 제안이 섞여 있다.
> 코드 사실은 현재 서버 백업으로 교차검증하고, 대회 시간·허용 범위·제출 규정·Isaac 버전은 최신 공식 공지를 우선한다.
# NAVER CONNECT Robotics Cup 2026
# 예선 대비 개인 NVIDIA 서버 운영안

> **현재 상태: historical operations design.** 이 문서는 개인 서버를 “평가 전용”으로 설계했던 초기 운영안이다. 이후 프로젝트에는 PERSONAL NVIDIA/Brev 학습 Run과 별도 evidence/Release 계보가 존재한다. PERSONAL 학습 결과는 OFFICIAL 제출 성능 근거가 아니며, 현재 실행·보존·게시 경계는 AI library `11`, `16`, `19`와 현재 repository instructions를 따른다. 이 문서의 “개인 서버에서 학습하지 않는다” 문구를 현재 금지 규칙으로 사용하지 않는다.

> 목표: 개인 NVIDIA 서버를 **학습 서버가 아니라 검증·분석 서버**로 사용하여, 운영진이 제공하는 100시간의 공식 학습 시간을 최대한 효율적으로 쓰고 예선 통과 확률을 높인다.

---

## 1. 핵심 원칙

예선에서 제출 가능한 정책은 **운영진이 제공한 클라우드 학습 환경에서 생성된 정책**이어야 한다.

따라서 개인 NVIDIA 서버는 다음 용도로 사용한다.

- 공식 서버에서 만든 `policy.pt` 실행
- 정책별 반복 테스트
- 여러 seed에서 안정성 측정
- 명령 추종 오차 측정
- 지형별 성공률 분석
- 낙상 및 복구 능력 측정
- 정책 A/B 비교
- 결과 영상 저장
- `env.yaml`, `report.html`과 실제 행동 비교
- 본선 `practice_sim`을 이용한 추가 실전성 검증

개인 서버에서 새로운 정책을 학습해 그것을 제출하는 방식은 사용하지 않는다.

---

# 2. 전체 운영 구조

```text
┌────────────────────────────┐
│ 대회 공식 GPU 서버          │
│                            │
│ reward 값 수정             │
│        ↓                   │
│ 강화학습                   │
│        ↓                   │
│ policy.pt                  │
│ env.yaml                   │
│ report.html                │
└──────────────┬─────────────┘
               │
               │ 다운로드
               ▼
┌────────────────────────────┐
│ 개인 NVIDIA 서버           │
│                            │
│ 1. policy 자동 실행        │
│ 2. 예선 시나리오 재현      │
│ 3. multi-seed 반복 테스트  │
│ 4. 생존율 측정             │
│ 5. tracking error 측정     │
│ 6. 낙상/복구 분석          │
│ 7. 정책 A/B 비교           │
│ 8. 영상/로그 저장          │
│ 9. 본선 엔진 보조 테스트   │
└──────────────┬─────────────┘
               │
               ▼
        다음 reward 결정
               │
               ▼
       공식 서버에서 재학습
```

즉 핵심 루프는 다음과 같다.

```text
Reward 변경
    ↓
공식 서버 학습
    ↓
정책 다운로드
    ↓
개인 서버 자동 평가
    ↓
수치 + 영상 분석
    ↓
다음 Reward 변경 결정
```

---

# 3. 개인 서버의 가장 중요한 기능

## 3.1 예선 Proxy Evaluator

개인 서버의 최우선 개발 대상이다.

운영진의 실제 평가 코드를 완전히 복제하는 것이 목적이 아니라, **정책 간 상대 성능을 일관되게 비교하는 자체 평가기**를 만드는 것이 목적이다.

예를 들어 H1 정책 하나를 넣으면 다음과 같은 결과를 자동으로 출력하도록 만든다.

```text
Policy: H1_012

Balance survival       : 100.0%
Forward tracking       : 0.92
Lateral tracking       : 0.85
Rotation tracking      : 0.88
Rough terrain          : 0.84
Slope                   : 0.91
Push recovery          : 0.79

Overall proxy score    : 0.886
Falls / 100 episodes   : 4
Average recovery time  : 1.32 sec
```

이 점수 자체가 실제 예선 점수라고 가정하면 안 된다.

목적은 다음처럼 정책을 비교하는 것이다.

```text
H1_010 = 0.81
H1_011 = 0.85
H1_012 = 0.89
H1_013 = 0.84
```

이렇게 하면 다음 학습에서 어떤 reward 방향을 유지할지 판단하기 쉬워진다.

---

# 4. H1 평가 시나리오 구성

예선 규정에 맞춰 다음 7개 평가기를 만든다.

## H1-1. 제자리 균형

목표:

- 명령 속도 `(0, 0, 0)`
- 일정 시간 서 있기
- pelvis/body가 쓰러지지 않기

수집할 값:

```text
survival_rate
body_height_mean
body_height_min
roll_rms
pitch_rms
joint_velocity_rms
fall_count
```

가장 중요한 것은 **아무 명령이 없을 때 불필요하게 걷거나 흔들리지 않는지** 확인하는 것이다.

---

## H1-2. 전진 속도 추종

여러 목표 속도를 준다.

예:

```text
0.25 m/s
0.50 m/s
0.75 m/s
1.00 m/s
```

각 속도에서 다음을 측정한다.

```text
vx_target
vx_actual
vx_RMSE
survival
overshoot
steady_state_error
```

개인 서버 evaluator에서는 다음과 같은 지표를 만들 수 있다.

```text
tracking_score = exp(-k * RMSE)
```

정확한 운영진 공식은 알 수 없으므로 이 값은 **정책 비교용 내부 지표**로만 사용한다.

---

## H1-3. 좌우 속도 추종

예:

```text
vy = -0.3 m/s
vy = -0.15 m/s
vy = +0.15 m/s
vy = +0.3 m/s
```

관찰할 것:

- 옆걸음 중 발이 꼬이는지
- torso가 과도하게 기울어지는지
- yaw drift가 발생하는지
- lateral command에서 낙상하는지

---

## H1-4. 회전 복합 추종

다음처럼 복합 명령을 준다.

```text
vx = 0.5
vy = 0.0
yaw = +0.5
```

또는

```text
vx = 0.3
vy = 0.2
yaw = -0.5
```

단순 직진이 아니라 **이동하면서 방향을 바꿀 때 안정적인지** 보는 테스트다.

본선의 waypoint controller도 결국 `[vx, vy, wz]` 형태의 속도 명령을 정책에 주므로 본선 실전성과도 연결된다.

---

## H1-5. 약한 요철

높이가 작은 noise terrain을 여러 seed로 생성한다.

권장 내부 테스트 예:

```text
2 cm
4 cm
6 cm
8 cm
10 cm
```

정책 간 비교에서는 다음을 기록한다.

```text
success_rate
fall_rate
average_speed
tracking_error
foot_slip
```

---

## H1-6. 경사

예선 공개 범위를 기준으로 주 평가 구간은 ±10° 주변을 집중적으로 테스트한다.

예:

```text
-10°
-5°
0°
+5°
+10°
```

추가 robustness 테스트로 더 높은 경사도 별도 측정할 수 있다.

```text
12°
15°
18°
20°
```

다만 **예선 통과 최적화용 주 점수에는 공개 평가 범위를 우선 반영**한다.

---

## H1-7. 밀침 회복

로봇 body에 순간 impulse 또는 force를 적용한다.

방향:

```text
앞
뒤
왼쪽
오른쪽
대각선
```

세기 역시 여러 단계로 나눈다.

측정값:

```text
fall / no fall
recovery_time
max_tilt
position_displacement
tracking_recovery_time
```

단순히 안 넘어지는 것뿐 아니라 **밀린 뒤 다시 command tracking으로 돌아오는 속도**도 저장한다.

---

# 5. Go2 평가 시나리오

Go2도 같은 구조로 evaluator를 만든다.

```text
G1  Forward tracking
G2  Omnidirectional tracking
G3  Rough terrain
G4  ±20° slope
G5  10~15 cm stairs
G6  Push recovery
G7  Domain Randomization
```

Go2는 비교적 안정성이 높기 때문에 예선 초반에 **빠르게 안정적인 점수를 확보하는 로봇**으로 활용할 가치가 있다.

---

# 6. 정책 하나를 최소 여러 번 실행한다

정책을 영상 한 번 보고 평가하면 안 된다.

권장 구조:

```text
Policy A

Scenario H1
    Seed 001
    Seed 002
    ...
    Seed 030

Scenario H2
    Seed 001
    ...
```

처음에는 시나리오당 10회 정도로 빠르게 screening하고, 유망한 모델만 30~100회까지 늘리는 방식이 효율적이다.

예:

```text
1차 screening
7 scenarios × 10 episodes = 70 episodes

최종 후보 평가
7 scenarios × 50 episodes = 350 episodes
```

---

# 7. 정책마다 저장해야 할 데이터

각 policy 디렉터리에 최소 다음을 저장한다.

```text
policy.pt
env.yaml
report.html
metadata.json
metrics.json
summary.md
videos/
logs/
```

예:

```json
{
  "name": "H1_012",
  "parent": "H1_011",
  "changes": {
    "termination_penalty": [-5.0, -50.0],
    "track_lin_vel_xy_exp": [0.5, 0.7]
  },
  "intent": "낙상 억제를 강화하면서 전진 추종 성능 개선",
  "official_training_hours": 7.4
}
```

이 기록은 나중에 기술 개선 리포트를 쓸 때도 도움이 된다.

---

# 8. 디렉터리 구조 예시

```text
NCRC-Lab/
│
├── IsaacLab/
│
├── competition_code/
│   ├── training/
│   └── practice_sim/
│
├── policies/
│   ├── H1/
│   │   ├── H1_001/
│   │   ├── H1_002/
│   │   └── H1_003/
│   │
│   └── Go2/
│       ├── G2_001/
│       └── G2_002/
│
├── evaluator/
│   ├── h1/
│   │   ├── balance.py
│   │   ├── forward.py
│   │   ├── lateral.py
│   │   ├── rotation.py
│   │   ├── rough.py
│   │   ├── slope.py
│   │   └── push.py
│   │
│   ├── go2/
│   │   ├── forward.py
│   │   ├── omni.py
│   │   ├── rough.py
│   │   ├── slope.py
│   │   ├── stairs.py
│   │   ├── push.py
│   │   └── domain_randomization.py
│   │
│   ├── metrics.py
│   ├── runner.py
│   └── compare.py
│
├── results/
│   ├── H1_001.json
│   ├── H1_002.json
│   ├── Go2_001.json
│   └── leaderboard.csv
│
├── videos/
│
└── dashboard/
```

---

# 9. 자동 평가 실행 형태

최종적으로는 이런 명령 하나로 평가되도록 만든다.

```bash
python evaluate.py \
    --robot h1 \
    --policy policies/H1/H1_012/policy.pt \
    --episodes 30
```

결과:

```text
================================================
Policy: H1_012
================================================
Balance             0.96
Forward             0.91
Lateral             0.87
Rotation            0.88
Rough               0.83
Slope               0.90
Push                0.81
------------------------------------------------
Weighted Proxy      0.886
Falls               7 / 210
================================================
```

그리고 자동으로:

```text
results/H1_012.json
results/leaderboard.csv
```

에 추가한다.

---

# 10. 정책 Leaderboard

매번 사람 눈으로 비교하지 말고 자동 정렬한다.

예:

| Policy | Survival | Tracking | Rough | Slope | Push | Proxy |
|---|---:|---:|---:|---:|---:|---:|
| H1_012 | 96% | 91% | 90% | 91% | 88% | 0.91 |
| H1_009 | 94% | 92% | 84% | 88% | 82% | 0.88 |
| H1_013 | 98% | 85% | 91% | 89% | 90% | 0.87 |
| H1_006 | 89% | 96% | 72% | 75% | 65% | 0.80 |

이런 식으로 보면 **training reward가 높은 모델과 실제 안정적인 모델이 다른지** 바로 알 수 있다.

---

# 11. `model_best.pt`를 맹신하지 않는다

현재 백업의 finalize 로직은 주로 TensorBoard의 `Train/mean_reward` 기준으로 best checkpoint를 고른다.

따라서 다음 상황이 가능하다.

```text
              Train Reward      예선 Proxy
Model A           40.1             0.84
Model B           47.3             0.90
Model C           53.8             0.81
                                  ↑
                           실제로 더 불안정
```

가능한 범위에서 여러 후보 policy를 확보하고 개인 서버에서 비교하는 것이 좋다.

핵심은:

```text
Training Reward ≠ 예선 점수
```

이다.

---

# 12. Reward 실험 방법

한 번에 reward 여러 개를 크게 바꾸지 않는다.

나쁜 예:

```text
track_lin       변경
track_ang       변경
feet_air_time   변경
termination     변경
orientation     변경
```

이후 성능이 나빠지면 원인을 알기 어렵다.

가능하면 다음처럼 실험한다.

```text
Experiment H1-07

변경:
termination_penalty
-5 → -50

가설:
낙상에 대한 비용을 증가시키면 생존율이 올라갈 것이다.

결과:
Survival       +7.2%
Tracking       -1.1%
Push recovery  +5.4%
Proxy          +4.8%

판단:
유지
```

이 데이터 자체가 예선의 설계 의도 설명에도 활용 가능하다.

---

# 13. 실험 DB

간단한 CSV만 있어도 충분하다.

```text
experiment_id
robot
parent_policy
reward_name
old_value
new_value
hypothesis
train_hours
survival
tracking
rough
slope
push
proxy
notes
```

예:

```text
H1-007,H1,H1-006,termination_penalty,-5,-50,
"낙상 억제",7.2,0.96,0.91,0.90,0.91,0.88,0.91,"유지"
```

---

# 14. 영상 자동 저장

모든 episode를 저장하면 저장공간이 너무 커진다.

따라서 다음만 자동 저장하면 좋다.

```text
best episode
median episode
worst episode
모든 fall episode
특이한 recovery episode
```

예:

```text
videos/H1_012/
├── slope_best.mp4
├── slope_worst.mp4
├── push_fall_seed17.mp4
├── rough_fall_seed08.mp4
└── forward_median.mp4
```

수치만 보면 알 수 없는 gait 문제를 확인할 수 있다.

---

# 15. 본선 엔진 활용 방법

`practice_sim`은 예선 평가의 핵심 도구가 아니라 **2차 검증 도구**로 사용한다.

예선 proxy가 비슷한 두 정책이 있다고 가정한다.

```text
Policy A
예선 Proxy = 0.900

Policy B
예선 Proxy = 0.895
```

그런데 본선 practice simulation에서는:

```text
Policy A
계단 진입 중 자주 낙상
좁은 회전 불안정

Policy B
계단/경사 안정
waypoint 추종 우수
```

이라면 B가 더 장기적으로 가치 있을 수 있다.

다만 **예선 통과가 우선이므로 본선 테스트 때문에 예선 점수를 크게 희생하지 않는다.**

우선순위는 다음처럼 잡는다.

```text
1. 예선 자동평가 성능
2. 재현성 / 생존율
3. 설계 의도와 실제 행동 일치
4. 본선 practice_sim 호환성
```

---

# 16. H1에서 특히 집중할 부분

H1은 본선 대비 학습환경에 계단과 높은 단차가 포함되어 있지만, 예선 자동평가의 핵심은 다음이다.

```text
제자리 안정
전진 추종
좌우 추종
회전 추종
약한 요철
±10° 경사
밀침 회복
```

따라서 예선 통과가 목표라면:

```text
50 cm 박스를 멋있게 오르는 정책
```

보다

```text
±10° 경사에서 거의 안 넘어짐
vx/vy/yaw 명령 정확히 추종
밀림 이후 빠르게 회복
```

하는 정책을 우선한다.

---

# 17. Go2 활용 전략

Go2는 상대적으로 안정적인 locomotion policy를 만들기 쉬울 가능성이 높다.

초기 전략:

```text
Go2에서 빠르게 안정적인 점수 확보
        ↓
H1에 더 많은 학습시간 투자
        ↓
후반 Go2 재개선
```

예선은 H1과 Go2 최고점을 합산하므로 한 종류만 계속 제출하는 전략보다 **두 로봇 모두 일정 점수를 확보하는 것이 중요**하다.

---

# 18. 공식 100시간 사용 예시

아래는 단순 운영 예시다.

```text
Go2        25~30 h
H1         55~60 h
예비시간    10~15 h
```

정확한 비율은 초기 학습 결과를 보고 바꾼다.

핵심은 개인 서버에서 평가를 돌리는 동안 **공식 학습 시간을 소비하지 않는 것**이다.

---

# 19. 추천 개발 순서

## Phase 1 — 환경 복제

```text
Isaac Sim 버전 맞추기
IsaacLab 백업 그대로 배치
H1/Go2 policy 실행 확인
```

목표:

```text
공식 서버에서 생성한 policy.pt가
개인 서버에서 정상적으로 동일 observation/action 구조로 실행됨
```

---

## Phase 2 — 기본 Metric Logger

먼저 다음만 기록한다.

```text
robot position
robot orientation
linear velocity
angular velocity
command velocity
fall state
simulation time
```

이것만 있어도 상당히 많은 평가가 가능하다.

---

## Phase 3 — Tracking Evaluator

```text
vx RMSE
vy RMSE
yaw RMSE
survival
```

부터 만든다.

가장 구현하기 쉽고 예선 점수와 직접 관계가 있다.

---

## Phase 4 — Terrain Evaluator

```text
rough
slope
stairs
```

를 추가한다.

---

## Phase 5 — Push Evaluator

random impulse를 추가해 회복 능력을 자동 측정한다.

---

## Phase 6 — Batch Runner

```text
1 policy
× 7 scenarios
× N seeds
```

를 자동 실행한다.

---

## Phase 7 — Leaderboard

모든 정책을 하나의 CSV 또는 간단한 웹 대시보드에서 비교한다.

---

## Phase 8 — Practice Sim

상위 후보 정책만 본선 경기 엔진에 넣어본다.

```text
Top 3 H1
Top 3 Go2
```

정도만 테스트해도 충분하다.

---

# 20. 최소 구현 버전

처음부터 거대한 시스템을 만들 필요는 없다.

가장 작은 MVP는 다음 4개면 된다.

```text
evaluate_tracking.py
evaluate_terrain.py
evaluate_push.py
compare_results.py
```

그리고 결과를 CSV로 저장한다.

```text
policy,scenario,seed,survival,tracking_error,falls
```

이 정도만 있어도 reward 튜닝 효율이 크게 올라간다.

---

# 21. 최종적으로 만들고 싶은 형태

```text
$ python evaluate.py --policy H1_012.pt --robot h1 --episodes 30

Running H1 evaluation...

[1/7] Balance       ██████████ 100%
[2/7] Forward       ██████████ 100%
[3/7] Lateral       ██████████ 100%
[4/7] Rotation      ██████████ 100%
[5/7] Rough         ██████████ 100%
[6/7] Slope         ██████████ 100%
[7/7] Push          ██████████ 100%

====================================
H1_012
====================================
Survival       96.7%
Tracking       0.914
Rough          0.887
Slope          0.902
Push           0.861
Proxy Score    0.904
====================================

Result saved:
results/H1_012.json
```

그리고:

```bash
python compare.py
```

결과:

```text
Rank  Policy     Proxy
1     H1_012     0.904
2     H1_009     0.889
3     H1_011     0.873
4     H1_006     0.812
```

이 구조가 완성되면 공식 서버에서 새 정책이 나올 때마다 개인 서버에 넣고 평가한 뒤 다음 reward 변경을 결정하면 된다.

---

# 22. 추천 운영 루프

실제 대회 기간에는 아래 방식으로 반복한다.

```text
[1]
현재 최고 정책 분석

[2]
가장 약한 시나리오 확인

예:
Push recovery = 매우 낮음

[3]
해당 실패와 관련된 reward 한두 개만 수정

[4]
공식 서버에서 학습

[5]
policy 다운로드

[6]
개인 서버에서 batch evaluation

[7]
기존 최고 모델과 비교

[8]
좋아졌으면 새 baseline
나빠졌으면 rollback
```

즉 reward tuning을 감이 아니라 **실험 기반 optimization**으로 바꾼다.

---

# 23. 절대 하지 말아야 할 것

## 개인 서버에서 새 정책을 학습해 제출

예선 규정상 제출 정책은 운영진 제공 학습 환경의 이력과 대응해야 한다.

따라서 개인 서버에서 training을 돌려 생성한 policy를 제출하지 않는다.

---

## 운영진 평가 취약점 악용

현재 백업에 경기 엔진 내부 로직이 상당히 많이 포함되어 있지만, 시스템 취약점을 악용해 점수를 만드는 방향은 사용하지 않는다.

개인 서버에서는 **정상적인 정책 성능 검증**에만 활용한다.

---

## 제공 credential 외부 사용

백업 내 practice credential 등 운영진이 제공한 자격증명을 대회 밖 서비스나 공개 환경에서 사용하지 않는다.

---

# 24. 이 서버의 가장 큰 가치

개인 서버의 목적은 GPU를 하나 더 확보하는 것이 아니다.

가장 큰 가치는 다음이다.

```text
공식 서버
100시간 제한
       ↓
학습에만 사용

개인 서버
사실상 반복 평가 제한 없음
       ↓
실험 실패 비용 감소
```

즉 공식 GPU 100시간을:

```text
학습 50%
평가 50%
```

로 쓰는 대신,

```text
공식 서버
학습 ≈ 대부분

개인 서버
검증 ≈ 대부분
```

으로 분리하는 것이 목표다.

---

# 25. 최종 권장 구성

## 필수

```text
Isaac Sim 5.1 계열 환경
백업의 IsaacLab checkout
대회 H1/Go2 환경
policy runner
metric logger
batch evaluator
CSV/JSON 결과 저장
```

## 강력 추천

```text
multi-seed evaluator
fall detector
tracking RMSE
terrain success rate
push recovery time
policy leaderboard
자동 영상 저장
```

## 나중에 추가

```text
간단한 웹 dashboard
practice_sim 본선 평가
자동 정책 regression test
실험 history visualization
```

---

# 결론

개인 NVIDIA 서버는 **예선 학습을 대신하는 서버가 아니라, 공식 서버에서 만든 정책을 매우 많이 시험하고 비교하는 연구실**로 만드는 것이 가장 좋다.

핵심 시스템은 다음 세 개다.

```text
1. 예선 7시나리오 Proxy Evaluator
2. Multi-seed Batch Runner
3. Policy Leaderboard
```

이 세 개만 제대로 구축해도 reward를 바꿀 때마다:

```text
"느낌상 좋아졌다"
```

가 아니라

```text
"생존율 +5.8%, tracking -0.7%, 최종 proxy +3.9%"
```

처럼 판단할 수 있다.

예선 통과라는 목표만 놓고 보면, 개인 서버에서 가장 먼저 만들어야 할 것은 **본선 경기 복제본이 아니라 예선 자동 평가기**다.

본선 `practice_sim`은 그다음 단계에서 상위 정책들의 실전성을 확인하는 보조 테스트베드로 쓰는 것이 좋다.
