---
id: planning-solution-blueprint
source_type: planning_analysis
category: implementation_blueprint
trust_level: mixed_code_confirmed_facts_and_recommendations
source: "data/raw/planning/NCRC2026_solution_blueprint.md"
---

> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/planning/historical/01_SOLUTION_BLUEPRINT.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.


> [!IMPORTANT]
> 이 문서는 사용자가 제공한 대회 준비 설계·권장안이다. 백업 코드에서 확인한 값과 구현 제안이 섞여 있다.
> 코드 사실은 현재 서버 백업으로 교차검증하고, 대회 시간·허용 범위·제출 규정·Isaac 버전은 최신 공식 공지를 우선한다.
# NCRC 2026 정책·본선 전략 구현 청사진

> **현재 취급: planning blueprint / historical design context.** 구현 아이디어와 백업 코드 분석을 보존한 문서이며 현재 Run 상태·다음 reward 후보·서버 운영 권한의 source of truth가 아니다. 현재 상태는 `PROJECT_CONTEXT.md`, `research/EXPERIMENTS.md`, AI library `00`; evaluator 구현 상태는 AI library `10/15`; 서버 운영은 `11/19`를 우선한다.

> 기준: 제공된 `workspace-backup.tar.gz`의 `training/`, `practice_sim/`, `examples/` 분석 결과\
> 목표: 시스템 허점이나 credential을 이용하지 않고, **locomotion policy + 평가기 + 경기 전략**으로 안정적인 점수를 내는 구조를 만든다.
>
> **[백업 확인]** = 실제 백업 코드에서 확인한 내용\
> **[권장]** = 확인된 구조를 바탕으로 한 구현 제안

---

## 1. 핵심 결론

이 대회는 단순히 **가장 빠르게 걷는 policy**를 만드는 문제가 아니다.

전체 구조를 보면 실제 본선에서 중요한 순서는 대략 다음과 같다.

```text
안정적인 locomotion
        ↓
정확한 velocity command tracking
        ↓
계단 / 박스 / 램프 통과
        ↓
회전 / 정지 / 저속 이동
        ↓
충격 후 recovery
        ↓
실제 경기 점수 기반 모델 선택
        ↓
큐브 우선순위 전략
        ↓
마지막에 LLM
```

특히 LLM은 관절을 직접 움직이지 않는다.

`practice_sim` 구조상 실질적인 제어는:

```text
Strategy
   ↓
GameAgent
   ↓
Path Planner
   ↓
Waypoint Controller
   ↓
[vx, vy, wz]
   ↓
RL Policy
   ↓
Joint Target
```

형태다.

따라서 가장 투자할 가치가 큰 부분은 **LLM prompt보다 locomotion policy의 안정성**이다.

---

# 2. 전체 시스템 구조

백업을 기준으로 추천하는 구조는 다음과 같다.

```text
┌─────────────────────────────────────┐
│          Strategy Layer             │
│                                     │
│ Fixed → Heuristic → Optional LLM    │
│ Cube priority / risk management     │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│        Existing Path Router         │
│                                     │
│ A* / Ramp / Stairs / Box routing    │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│       Waypoint Controller           │
│                                     │
│          vx / vy / wz               │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│       RL Locomotion Policy          │
│                                     │
│ Tracking / Terrain / Recovery       │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│             Simulator               │
│                                     │
│ Physics / Cube / Fall / Collision   │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│       Evaluation Framework          │
│                                     │
│ Score / Fall / RMSE / Success Rate  │
└─────────────────────────────────────┘
```

---

# 3. Policy 인터페이스

## H1

**[백업 확인]**

```text
Flat observation  = 69
Rough observation = 256
Action            = 19
Action scale      = 0.5
```

Rough policy에는:

```text
17 × 11 = 187
```

개의 height scan이 추가된다.

따라서:

```text
69 + 187 = 256
```

이다.

height scanner 해상도는 약:

```text
0.1 m
```

다.

---

## Go2

**[백업 확인]**

```text
Flat observation  = 48
Rough observation = 235
Action            = 12
Action scale      = 0.25
```

마찬가지로:

```text
48 + 187 = 235
```

이다.

---

# 4. 실제 경기에서 policy에 들어가는 명령

## H1

**[백업 확인]**

`waypoint_controller.py` 실제 상수 기준 최대 전진 명령은 약:

```text
1.0 m/s
```

학습 환경 command 범위는 대략:

```text
vx = -1.0 ~ 1.5
vy = -0.5 ~ 0.5
wz = -1.0 ~ 1.0
```

---

## Go2

실제 waypoint controller에서는 약:

```text
1.6 m/s
```

까지 사용한다.

학습 환경은:

```text
vx = -1.0 ~ 2.0
vy = -0.6 ~ 0.6
wz = -1.0 ~ 1.0
```

정도다.

일부 코드 설명에는 Go2 `2.0 m/s`라고 적힌 오래된 주석도 있지만 실제 실행 상수와 assertion은 `1.6 m/s`이므로 **주석보다 실제 코드 값을 우선한다.**

---

# 5. 가장 먼저 만들 것: Evaluation Harness

가장 먼저 reward를 수정하는 것이 아니다.

먼저 **현재 policy가 실제로 얼마나 좋은지 측정하는 코드**를 만든다.

추천 디렉터리:

```text
evaluation/
├── flat_tracking.py
├── turning.py
├── stop_and_go.py
├── terrain.py
├── recovery.py
├── full_match.py
└── metrics.py
```

그리고 최소 다음 metric을 기록한다.

```text
velocity_tracking_rmse
yaw_tracking_rmse

fall_rate
mean_survival_time

stairs_success_rate
ramp_success_rate
box_success_rate

recovery_success_rate
recovery_time

cube_collection_rate
match_score
```

최종적으로 가장 중요한 것은:

```text
1. Match Score
2. Fall Rate
3. Terrain Success Rate
4. Recovery Success Rate
5. Command Tracking RMSE
```

다.

---

# 6. `model_best.pt`를 그대로 믿으면 안 되는 이유

**[백업 확인]**

현재 `_finalize.py`는 checkpoint를 선택할 때 실제 경기 점수보다:

```text
Train/mean_reward
```

를 주요 기준으로 사용한다.

따라서:

```text
Train reward가 가장 높음
```

과:

```text
실제 경기에서 가장 좋음
```

은 서로 다를 수 있다.

예:

| Model | Train Reward | Match Score | Fall |
|---|---:|---:|---:|
| A | 82 | 430 | 18% |
| B | 76 | 525 | 5% |

실제로는 B가 훨씬 좋은 제출 모델일 수 있다.

따라서 모든 checkpoint를 별도 평가해야 한다.

```text
model_1000.pt
model_1500.pt
model_2000.pt
model_2500.pt
...
```

각 모델을 여러 seed에서 경기시킨다.

---

# 7. H1 학습 방향

## 현재 baseline

**[백업 확인]**

```text
track_lin_vel_xy_exp = 0.5
track_ang_vel_z_exp  = 0.5

feet_air_time        = 0.2

termination_penalty  = -5.0
flat_orientation_l2  = -1.5
ang_vel_xy_l2        = -0.05

joint_deviation_hip   = -0.2
joint_deviation_torso = -0.1

action_rate_l2       = -0.0005
```

---

## 가장 먼저 실험할 것

### 1. termination penalty

현재:

```text
-5
```

다.

백업의 reward 설명 자체에서도 이 값보다 훨씬 강한 termination penalty 범위를 고려하도록 되어 있다.

따라서 처음에는 좁게:

```text
baseline = -5

test A = -10
test B = -25
test C = -50
test D = -100
```

정도로 비교한다.

단순 training reward 대신:

```text
fall_rate
stairs_success
box_success
match_score
```

를 본다.

너무 강하게 넣으면:

```text
낙상을 지나치게 두려움
        ↓
보수적인 gait
        ↓
속도 저하
        ↓
장애물 진입 회피
```

가 발생할 수도 있다.

---

### 2. feet_air_time

현재:

```text
0.2
```

**[백업 확인]** reward 파일에도 값을 과하게 키울 경우 hopping 계열 reward hacking을 조심하라는 취지의 설명이 있다.

추천 sweep:

```text
0.10
0.15
0.20
0.25
```

영상에서 다음을 본다.

```text
한 발 hopping
과도한 high-step
불필요하게 뛰는 gait
발을 지나치게 높게 올림
계단에서 자세 불안정
```

---

# 8. H1 terrain 학습

**[백업 확인]**

H1의 별도 환경 설정에는 대략:

```text
box height = 0.15 ~ 0.50 m
box width  = 0.6 ~ 1.5 m

stairs step width = 0.30 m
```

형태의 override가 있다.

또 코드 주석에 본선 대비 `0.45 m`와 관련된 개발 메모가 존재한다.

다만 이것을 **실제 본선 맵 치수로 확정해서 사용하면 안 된다.**

---

## 추천 curriculum

처음부터 최대 obstacle만 학습시키기보다는 단계적으로 간다.

### Stage 1

```text
Flat
+
0.10 ~ 0.20 m
```

목표:

```text
command tracking
```

---

### Stage 2

```text
0.15 ~ 0.30 m
+
쉬운 stairs
```

목표:

```text
gait 유지
```

---

### Stage 3

```text
0.30 ~ 0.45 m

stairs
ramp
box
```

목표:

```text
실전 terrain 통과
```

---

### Stage 4

```text
0.45 ~ 0.50 m

좁은 접근
회전 후 즉시 장애물
terrain 연속 전환
```

목표:

```text
한계 상황 robustness
```

---

# 9. Go2 방향

**[백업 확인]** baseline:

```text
track_lin_vel_xy_exp = 1.0
feet_air_time        = 0.01

lin_vel_z_l2         = -3.0
ang_vel_xy_l2        = -0.08
action_rate_l2       = -0.01
```

주석으로 후보가 남아 있는 항목:

```text
track_ang_vel_z_exp
flat_orientation_l2
undesired_contacts
termination_penalty
```

등이 있다.

Go2는 큰 폭으로 수정하기 전에 baseline 자체의 성능을 먼저 측정하는 게 좋다.

```text
Baseline
   ↓
Yaw tracking
   ↓
Terrain
   ↓
Recovery
   ↓
Reward 수정
```

백업에는 과거 설정에서 exploration이 지나치게 줄어:

```text
stand & spin
```

형태의 local optimum이 발생했다는 개발 메모도 있다.

따라서:

```text
entropy ↓
learning rate ↓
penalty ↑
```

를 동시에 강하게 적용하는 것은 피하는 편이 좋다.

---

# 10. PPO는 마지막 쪽에서 만진다

**[백업 확인]** 기본 PPO는 대략:

```text
num_steps_per_env = 24

Actor:
512
256
128

Critic:
512
256
128

activation = ELU

learning_rate = 1e-3
entropy_coef  = 0.008

gamma  = 0.99
lambda = 0.95

desired_kl = 0.01
```

처음에는 이걸 그대로 두는 것을 권장한다.

수정 순서:

```text
환경
 ↓
Reward
 ↓
Curriculum
 ↓
PPO
```

정책이 이상한데 learning rate부터 건드리기 시작하면 원인 찾기가 매우 어려워진다.

---

# 11. 꼭 필요한 Policy Test

## Test 1 — Flat Velocity Tracking

```text
vx = 0.2
vx = 0.5
vx = 0.8
vx = 1.0
```

측정:

```text
velocity RMSE
body tilt
fall
```

---

## Test 2 — Yaw

```text
wz = ±0.3
wz = ±0.7
wz = ±1.0
```

측정:

```text
yaw tracking error
overshoot
fall
```

---

## Test 3 — Stop & Go

본선에서는 최고속도로 계속 달리지 않는다.

**[백업 확인]**

waypoint controller는 목표 약:

```text
1 m
```

부터 감속하고 약:

```text
0.3 m
```

부근에서 정지한다.

따라서:

```text
0.0
↓
0.3
↓
0.8
↓
0.3
↓
0.0
```

같은 command transition을 잘 따라가는지 본다.

---

# 12. 회전 성능

**[백업 확인]**

waypoint controller는 목표 방향과 yaw가 크게 다르면 전진 속도를 줄이고 먼저 회전하려는 구조다.

따라서 다음 초기 각도에서 테스트한다.

```text
0°
30°
60°
90°
135°
180°
```

측정:

```text
회전 시간
overshoot
turning radius
fall
```

특히 **제자리 또는 저속 회전 안정성**이 중요하다.

---

# 13. Terrain Transition

단순히:

```text
계단 하나 잘 올라감
```

만 측정해서는 부족하다.

실제 테스트는:

```text
flat → stairs → flat

flat → ramp → platform

flat → box → flat

turn → stairs

stairs → turn

box → turn → stop
```

처럼 해야 한다.

본선에서는 장애물을 독립적으로 통과하는 게 아니라 연속된 경로를 따라 움직이기 때문이다.

---

# 14. Recovery

**[백업 확인]**

경기 시스템에는 차량 충돌과 knockback이 구현되어 있다.

따라서 로봇이 안 넘어지는 것뿐 아니라:

```text
옆으로 밀림
yaw 틀어짐
pitch 변화
속도 급변
```

후 정상 gait로 돌아가는지도 중요하다.

추천 테스트:

```text
로봇에 lateral impulse
        ↓
자세 흔들림
        ↓
command 계속 입력
        ↓
정상 gait 복구 시간 측정
```

중요 metric:

```text
Recovery Time
Recovery Success Rate
```

---

# 15. Strategy는 LLM 없이 먼저 만든다

개발 순서는:

```text
Fixed Priority
      ↓
Heuristic
      ↓
Optional LLM
```

을 추천한다.

---

## Phase 1 — Fixed

예:

```text
cube_1
→ cube_4
→ cube_3
→ cube_7
```

고정 순서만 가지고 경기가 정상 작동하게 만든다.

이 단계에서 문제가 생긴다면 LLM 문제가 아니다.

---

## Phase 2 — Heuristic

각 cube에 대해:

```text
distance
terrain
expected_time
fall_risk
vehicle_risk
```

를 계산한다.

예:

```text
utility =
cube_score
- α × expected_time
- β × fall_probability
- γ × terrain_failure_probability
- δ × vehicle_risk
```

핵심은:

> 가장 어려운 큐브를 먹는 것이 아니라 **제한 시간 안에 실제 획득할 기대값이 높은 큐브를 선택**하는 것이다.

---

# 16. 실제 위험도는 실험 데이터로 만든다

예를 들어 simulator 결과가:

```text
GROUND
success = 99%

RAMP
success = 96%

STAIRS
success = 91%

HIGH BOX
success = 63%
```

라면 그대로 전략기의 risk table로 넣는다.

예:

```json
{
  "ground": {
    "success": 0.99,
    "avg_time": 2.1
  },

  "ramp": {
    "success": 0.96,
    "avg_time": 4.3
  },

  "stairs": {
    "success": 0.91,
    "avg_time": 5.8
  },

  "box_high": {
    "success": 0.63,
    "avg_time": 8.7
  }
}
```

이렇게 하면 strategy와 locomotion이 연결된다.

---

# 17. LLM의 역할

**[백업 확인]**

GameAgent가 LLM을 사용하지만:

- 실제 A*
- stairs route
- ramp route
- box route
- waypoint
- velocity command

등은 middleware에서 많이 처리한다.

따라서 LLM에게:

```text
계단에 접근할 때 속도를 줄이고
오른발을 먼저 들고
...
```

같은 저수준 지시를 시키는 것은 의미가 작다.

LLM은 다음 정도만 맡기는 편이 좋다.

```text
목표 cube priority
위험 지역 회피
경기 후반 전략 변경
예외 상황 재계획
```

---

# 18. LLM 출력도 단순하게

자유 문장보다 가능하면 구조화된 형태가 좋다.

```json
{
  "priority": [
    "cube_4",
    "cube_7",
    "cube_2"
  ],
  "avoid": [
    "vehicle_zone"
  ]
}
```

장점:

```text
파싱 안정성
hallucination 감소
fallback 구현 용이
재현성 증가
```

---

# 19. Replan

**[백업 확인]**

현재 GameAgent에는 약:

```text
20 s
```

주기의 replan 구조가 존재한다.

등반 중에는 목표 변경을 막는 로직도 있다.

추천 replan 조건:

```text
cube collected
target unreachable
robot stuck
major collision
remaining-time threshold
```

단순히 자주 LLM을 호출한다고 전략이 좋아지는 것은 아니다.

---

# 20. 경기 시간

**[백업 확인]**

본선 엔진 쪽은 약:

```text
180 s wall clock
```

을 기준으로 종료하는 구조다.

연습 simulator에는 실행 성능에 따른 simulation-time 차이를 보정하려는 구현 흔적도 있다.

따라서 최적화 목표는:

```text
가장 짧은 simulation path
```

보다:

```text
180초 동안 실제로 획득 가능한 기대 점수
```

가 되어야 한다.

---

# 21. 시간에 따라 Risk를 변경

추천:

```text
remaining > 120 s
→ Conservative

60 < remaining <= 120 s
→ Normal

remaining <= 60 s
→ Aggressive
```

예를 들어 초반에는:

```text
GROUND
RAMP
쉬운 STAIRS
```

위주로 확실한 점수를 얻고,

후반에 시간이 남으면:

```text
HIGH BOX
위험한 route
```

를 허용한다.

시간 경계는 실제 경기 반복 결과로 수정한다.

---

# 22. Checkpoint 자동 평가

각 checkpoint마다 최소 여러 seed를 돌린다.

```text
model_1000.pt
model_1500.pt
model_2000.pt
model_2500.pt
...
```

예:

```text
seed 1
seed 2
seed 3
seed 4
seed 5
```

결과:

| Model | Train Reward | Match | Fall | Terrain |
|---|---:|---:|---:|---:|
| 1000 | 61 | 420 | 12% | 84% |
| 1500 | 72 | 510 | 7% | 91% |
| 2000 | 80 | 470 | 16% | 88% |
| 2500 | 77 | 535 | 5% | 94% |

이런 경우:

```text
model_2500
```

을 선택한다.

---

# 23. 내부 Model Score

예를 들어 자동화용으로:

```text
model_score =
    match_score
  - 100 × fall_rate
  + 50 × terrain_success_rate
  - 10 × tracking_rmse
```

같이 만들 수 있다.

숫자는 예시일 뿐이다.

중요한 건:

```text
Train Reward
```

만으로 모델을 고르지 않는 것이다.

---

# 24. 추천 프로젝트 구조

```text
project/
│
├── competition/
│   ├── training/
│   └── practice_sim/
│
├── policies/
│   ├── h1/
│   └── go2/
│
├── evaluation/
│   ├── flat_tracking.py
│   ├── turning.py
│   ├── stop_and_go.py
│   ├── terrain.py
│   ├── recovery.py
│   ├── full_match.py
│   └── metrics.py
│
├── experiments/
│   ├── h1_baseline/
│   ├── h1_termination_25/
│   ├── h1_termination_50/
│   └── go2_baseline/
│
├── strategy/
│   ├── fixed.py
│   ├── heuristic.py
│   ├── llm_strategy.py
│   └── risk_table.json
│
└── results/
    ├── leaderboard.csv
    ├── experiment_log.csv
    └── videos/
```

대회 원본 코드와 본인이 작성한 실험 코드를 분리해 두는 것이 좋다.

---

# 25. 실험 하나당 저장할 정보

예:

```yaml
experiment: h1_termination_50

reward:
  track_lin: 0.5
  track_ang: 0.5
  feet_air_time: 0.2
  termination: -50

training:
  seed: 42
  iterations: 5000

evaluation:
  flat_rmse: 0.08
  fall_rate: 0.06
  stairs_success: 0.94
  box_success: 0.88
  recovery_success: 0.92
  match_score_mean: 512
```

이렇게 해야 나중에:

```text
왜 이 모델이 좋았지?
```

를 다시 찾을 수 있다.

---

# 26. 한 번에 한 변수씩

초기에는:

```text
termination
feet_air_time
orientation
learning_rate
entropy
terrain
```

를 동시에 바꾸면 안 된다.

예:

### Experiment A

```text
termination만 변경
```

### Experiment B

```text
feet_air_time만 변경
```

### Experiment C

```text
orientation penalty만 변경
```

좋은 방향을 찾은 후 조합한다.

---

# 27. 영상도 반드시 본다

강화학습은 scalar reward만 보면 쉽게 속는다.

다음 이상 현상을 체크한다.

```text
hopping
foot dragging
body leaning
stand & spin
목표 주변 진동
계단 edge 충돌
box에 몸통을 박음
stop 상태에서 계속 미끄러짐
회전 후 자세가 무너짐
```

---

# 28. 최소 실전 테스트 10개

최종 policy라면 적어도 다음은 통과시킨다.

1. Flat 고속 tracking
2. Flat 0.2~0.4 m/s 저속 tracking
3. 90° turn
4. 180° turn
5. Stop → accelerate
6. Stairs ascent
7. Stairs descent
8. Box/platform transition
9. Lateral push recovery
10. Full 180 s match

---

# 29. H1 / Go2 선택

현재 백업만으로:

```text
H1이 무조건 낫다
```

또는:

```text
Go2가 무조건 낫다
```

라고 단정할 근거는 없다.

실제로 표를 만든다.

| Metric | H1 | Go2 |
|---|---:|---:|
| Flat speed | | |
| Turn time | | |
| Stairs | | |
| Box | | |
| Recovery | | |
| Fall rate | | |
| Match mean | | |
| Match P10 | | |
| Match worst | | |

평균만 보면 안 된다.

```text
mean
P10
worst
```

를 같이 본다.

대회에서는 한 번의 치명적인 실패가 평균 성능보다 중요할 수 있다.

---

# 30. 추천 개발 순서

## Phase 1 — Baseline

```text
공식 baseline 그대로 학습
        ↓
baseline.pt 확보
        ↓
practice simulator에서 경기 완주
```

---

## Phase 2 — Evaluation

먼저:

```text
flat
turn
stop
terrain
recovery
full match
```

자동 평가기를 만든다.

---

## Phase 3 — Reward Sweep

H1 기준 우선순위 예:

```text
termination
↓
feet_air_time
↓
orientation
↓
action_rate
```

---

## Phase 4 — Terrain Robustness

```text
쉬운 terrain
↓
중간 terrain
↓
실전 범위
↓
terrain transition
```

순으로 강화한다.

---

## Phase 5 — 경기 기준 Model Selection

```text
Train Reward
```

가 아니라:

```text
Match Score
Fall Rate
Terrain Success
Recovery
```

기준으로 모델을 고른다.

---

## Phase 6 — Fixed Strategy

LLM 없이 전체 경기가 정상 동작하도록 만든다.

---

## Phase 7 — Heuristic Strategy

```text
distance
+
expected time
+
terrain risk
+
vehicle risk
```

로 priority 계산.

---

## Phase 8 — LLM

맨 마지막에:

```text
high-level target ordering
exception handling
```

용도로만 추가한다.

---

# 31. 우선순위가 높은 작업

```text
★★★★★ 자동 평가기
★★★★★ 낙상 감소
★★★★★ 저속 tracking
★★★★★ turning
★★★★★ terrain transition
★★★★★ recovery

★★★★ 경기 반복 평가
★★★★ checkpoint 비교
★★★★ risk-aware strategy

★★ LLM prompt 고도화
★★ PPO architecture 변경
★ 최대속도만 올리기
```

---

# 32. 권장 Leaderboard

`results/leaderboard.csv`:

```text
experiment
robot
train_reward

flat_rmse
yaw_rmse

turn_success
stairs_success
box_success
recovery_success

fall_rate

match_mean
match_p10
match_worst
match_best
```

최종 제출 모델은 여기서 고른다.

---

# 33. Strategy용 로그

각 경기에서:

```text
timestamp
target_cube
target_category
path_length

time_to_target
collection_success

fall
collision
stuck

replan
replan_reason
```

을 기록한다.

그러면:

```text
box가 안 좋음
```

수준이 아니라:

```text
box 접근 성공 = 97%
climb 성공 = 64%
top traverse = 94%
descent 성공 = 82%
```

처럼 병목을 정확히 찾을 수 있다.

---

# 34. 규정·보안 측면

대회 원본과 개인 개발물을 분리한다.

```text
competition-original/
private-experiments/
public-code/
```

특히 다음은 공개 저장소에 올리지 않는다.

```text
practice_key.bin
token
credential
대회에서 받은 원본 전체 백업
```

또 경기 엔진에서 우연히 발견한 판정 허점을 이용해 점수를 얻는 방식보다:

```text
Policy 성능
Path reliability
Strategy
```

로 점수를 높이는 방향으로 개발하는 것이 안전하다.

---

# 35. 실제로 내가 시작한다면

딱 다음 순서로 한다.

```text
1. Baseline 학습

2. Baseline으로 practice_sim 완주

3. evaluation/ 작성

4. Flat / Turn / Stop / Terrain / Recovery 측정

5. H1이면 termination penalty 소규모 sweep

6. 여러 checkpoint를 실제 match score로 비교

7. 가장 안정적인 policy 확보

8. Fixed cube priority로 본선 파이프라인 완성

9. Simulator 데이터를 이용해 terrain risk table 생성

10. Risk-aware heuristic 구현

11. 마지막에만 LLM 연결

12. 여러 seed로 최종 회귀 테스트
```

---

# 36. 구현 체크리스트

- [ ] H1 baseline 재현
- [ ] Go2 baseline 재현
- [ ] Flat tracking 평가기
- [ ] Yaw/turn 평가기
- [ ] Stop & Go 평가기
- [ ] Stairs 평가기
- [ ] Ramp 평가기
- [ ] Box 평가기
- [ ] Terrain transition 평가기
- [ ] Push recovery 평가기
- [ ] Full-match 자동 평가
- [ ] CSV leaderboard
- [ ] Reward 한 변수씩 sweep
- [ ] 여러 seed 평가
- [ ] 경기 점수 기준 checkpoint 선택
- [ ] Fixed-priority 전략
- [ ] Terrain risk table
- [ ] Risk-aware heuristic
- [ ] LLM fallback
- [ ] 최종 180초 regression test
- [ ] credential / 대회 원본 공개 저장소 제외

---

# 최종 요약

이 백업을 기준으로 보면 가장 좋은 개발 철학은:

```text
Reward를 무작정 높인다
```

가 아니다.

대신:

```text
Baseline
   ↓
Evaluation Harness
   ↓
Locomotion Stability
   ↓
Terrain + Recovery
   ↓
Match-based Model Selection
   ↓
Fixed Strategy
   ↓
Risk-aware Heuristic
   ↓
Optional LLM
```

순서로 가는 것이 좋다.

특히 본선 middleware가 이미 A*, waypoint, 계단·램프·박스 경로를 상당 부분 처리하고 있기 때문에 *​*똑똑한 상위 전략보다 middleware의 명령을 안정적으로 수행하는 policy가 먼저**다.

최종적으로 만들어야 하는 것은 하나의 `policy.pt`가 아니라:

```text
Robust Policy
+
Automatic Evaluation
+
Risk-aware Strategy
```

세 가지 묶음이다.
