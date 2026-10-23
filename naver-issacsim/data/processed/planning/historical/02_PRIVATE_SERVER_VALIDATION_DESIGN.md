---
id: planning-private-validation-environment
source_type: planning_analysis
category: validation_environment_design
trust_level: mixed_code_confirmed_facts_and_recommendations
source: "data/raw/planning/예선_대비_개인서버_검증환경_설계.md"
---

> [!IMPORTANT]
> 이 문서는 사용자가 제공한 대회 준비 설계·권장안이다. 백업 코드에서 확인한 값과 구현 제안이 섞여 있다.
> 코드 사실은 현재 서버 백업으로 교차검증하고, 대회 시간·허용 범위·제출 규정·Isaac 버전은 최신 공식 공지를 우선한다.
# NAVER CONNECT Robotics Cup 2026 예선 대비 개인 NVIDIA 서버 검증환경 설계안

> **현재 상태: historical validation design.** 이 문서의 “개인 서버에서는 학습하지 않는다”는 초기 예선 검증환경 설계 원칙이며 현재 프로젝트 운영 사실을 설명하지 않는다. 이후 PERSONAL NVIDIA/Brev 학습 Run들이 별도 evidence 계보로 수행·보존됐다. PERSONAL 결과는 OFFICIAL 성능/제출 근거가 아니지만, PERSONAL 학습 자체가 금지된 것으로 해석하지 않는다. 현재 PERSONAL/OFFICIAL 경계와 실행 규칙은 AI library `11`, `16`, `19`를 우선한다.

> 목적: **예선 통과 가능성을 높이기 위한 로컬 검증/분석 환경**을 만든다.\
> 핵심 원칙: 개인 서버에서는 **학습하지 않고**, 운영진 서버에서 생성된 `policy.pt`를 가져와 실행·관찰·비교·분석만 한다.

---

## 1. 왜 이렇게 만드는가

예선의 핵심 평가는 본선 경기처럼 큐브를 모으는 것이 아니라, 여러 조건에서의 **생존율 × 명령 추종 성능**이다.

따라서 `practice_sim`의 경기 엔진 전체를 그대로 복제하는 것보다 다음 부분만 떼어내는 편이 효율적이다.

- 정책 로딩
- H1 / Go2 observation 생성
- policy inference
- joint target 적용
- Isaac Sim / Isaac Lab physics
- rough terrain / height scan
- 속도 명령 생성
- 낙상 감지
- 외력(push) 적용
- trajectory / velocity / orientation 로그 수집

반대로 예선 준비 단계에서는 다음 기능의 우선순위가 낮다.

- Gemini 전략
- 큐브 우선순위 결정
- 차량 경로
- 큐브 획득 점수
- 상대 팀 로봇
- 본선 1:1 경기 UI

즉 구조를 다음처럼 단순화한다.

```text
공식 대회 서버
    │
    │  policy.pt + env.yaml
    ▼
개인 NVIDIA 서버
    │
    ├─ Policy Loader
    ├─ Observation Builder
    ├─ Command Generator
    ├─ Scenario Runner
    ├─ Physics / Robot
    ├─ Metrics Collector
    └─ HTML/CSV Report
```

개인 서버가 하는 일은 **policy를 평가하는 것**이며 policy 자체를 업데이트하지 않는다.

---

# 2. 가장 추천하는 전체 구조

```text
prelim-validator/
│
├── policies/
│   ├── h1/
│   │   ├── run_001/
│   │   │   ├── policy.pt
│   │   │   └── env.yaml
│   │   └── run_002/
│   │       ├── policy.pt
│   │       └── env.yaml
│   └── go2/
│
├── engine/
│   ├── policy_loader.py
│   ├── observation.py
│   ├── robot_adapter.py
│   ├── height_scanner.py
│   ├── fall_detector.py
│   └── push_controller.py
│
├── scenarios/
│   ├── h1/
│   │   ├── balance.py
│   │   ├── forward_tracking.py
│   │   ├── lateral_tracking.py
│   │   ├── yaw_tracking.py
│   │   ├── rough.py
│   │   ├── slope.py
│   │   └── push_recovery.py
│   │
│   └── go2/
│       ├── forward_tracking.py
│       ├── omnidirectional.py
│       ├── rough.py
│       ├── slope.py
│       ├── stairs.py
│       ├── push_recovery.py
│       └── domain_randomization.py
│
├── metrics/
│   ├── tracking.py
│   ├── survival.py
│   ├── stability.py
│   └── score.py
│
├── runner/
│   ├── run_single.py
│   ├── run_suite.py
│   └── compare.py
│
├── reports/
│   └── ...
│
└── config/
    ├── h1.yaml
    └── go2.yaml
```

---

# 3. `practice_sim`에서 가져올 부분

기존 백업의 경기 엔진을 처음부터 다시 작성할 필요는 없다.

재사용 가치가 큰 코드는 다음과 같다.

## `engine.py`

가져올 것:

- TorchScript policy 로딩
- H1 / Go2 자동 판별
- observation 구성
- action → joint target 변환
- actuator / PD 설정
- physics step 처리

버릴 것:

- Match
- backend communication
- 상대 팀 처리
- 경기 시간 판정
- 큐브 게임 점수

---

## `observation.py`

가능하면 거의 그대로 재사용한다.

현재 엔진 기준 policy 입력 차원은 다음과 같다.

### H1

```text
Flat  : 69
Rough : 256
Action: 19
```

### Go2

```text
Flat  : 48
Rough : 235
Action: 12
```

Rough policy에는 약 `187`개의 terrain height observation이 추가된다.

이 부분이 실제 policy와 조금이라도 달라지면 policy 성능 자체가 완전히 달라질 수 있으므로, **가장 먼저 동일성을 확보해야 하는 코드**다.

---

## `height_scanner.py`

Rough policy 검증에 사용한다.

기존 엔진의 scanner를 그대로 쓰거나 최소한 다음을 동일하게 유지한다.

```text
17 × 11 = 187 points
resolution ≈ 0.1 m
```

---

## `waypoint_controller.py`

전체를 그대로 쓸 필요는 없지만 **속도 명령 범위 검증용**으로 유용하다.

현재 엔진의 실질적인 최대 전진 명령은 대략 다음과 같다.

```text
H1  : 1.0 m/s
Go2 : 1.6 m/s
```

따라서 예선 validator에서도 최소한 이 범위까지 command tracking을 시험해보는 것이 좋다.

---

# 4. 예선 평가 시나리오를 직접 복제한다

## H1

공식 평가 항목을 그대로 테스트 케이스로 만든다.

| ID | 테스트 | 비중 |
|---|---|---:|
| H1 | 제자리 균형 | 0.15 |
| H2 | 전진 속도 추종 | 0.20 |
| H3 | 좌우 속도 추종 | 0.10 |
| H4 | 회전 복합 추종 | 0.10 |
| H5 | 약한 요철 | 0.15 |
| H6 | 완만한 경사 ±10° | 0.15 |
| H7 | 밀침 회복 | 0.15 |

### 중요한 점

H1 학습 환경에는 더 어려운 계단/박스가 있지만, **예선 자동평가 70점의 H1 7개 시나리오에는 높은 박스 등반이 직접 들어 있지 않다.**

따라서 예선 통과가 우선이라면

```text
평지 추종
→ 균형
→ 요철
→ 경사
→ push recovery
→ 본선용 고단차
```

순으로 우선순위를 잡는다.

---

# 5. Go2 평가 시나리오

| ID | 테스트 | 비중 |
|---|---|---:|
| G1 | 전진 속도 추종 | 0.15 |
| G2 | 전방위 속도 추종 | 0.15 |
| G3 | 거친 지형 | 0.20 |
| G4 | 경사 ±20° | 0.15 |
| G5 | 10~15 cm 계단 | 0.15 |
| G6 | 밀침 회복 | 0.10 |
| G7 | Domain Randomization | 0.10 |

Go2는 `G3 rough terrain`의 비중이 가장 크므로, 평지에서 잘 뛰는 것만으로는 부족하다.

---

# 6. Command Generator

각 시나리오에서 일정한 명령 하나만 주면 policy의 취약점을 찾기 어렵다.

따라서 command를 여러 단계로 변화시키는 테스트를 만든다.

예:

```text
0~5 s    : 정지
5~10 s   : vx = 0.3
10~15 s  : vx = 0.6
15~20 s  : vx = 1.0
20~25 s  : vx = 0
25~30 s  : vy = +0.3
30~35 s  : vy = -0.3
35~40 s  : wz = +0.5
40~45 s  : wz = -0.5
```

이걸 한 번 돌려보면

- 가속할 때 넘어지는지
- 감속할 때 넘어지는지
- 좌우 이동에서 발이 꼬이는지
- 회전 시작 시 흔들리는지
- 회전 후 직진 복귀가 되는지

등을 쉽게 확인할 수 있다.

---

# 7. Metrics Collector

영상만 보고 판단하지 말고 반드시 수치를 저장한다.

최소한 다음을 기록한다.

```text
simulation_time
command_vx
command_vy
command_wz
actual_vx
actual_vy
actual_wz
base_height
roll
pitch
gravity_projection
joint_position
joint_velocity
action
fall_flag
terrain_level
```

CSV 예시:

```csv
time,cmd_vx,vel_vx,error_vx,roll,pitch,height,fallen
0.00,0.50,0.47,0.03,0.01,-0.02,0.98,0
0.02,0.50,0.48,0.02,0.02,-0.02,0.98,0
...
```

---

# 8. 예선용 로컬 추정 점수

공식 규정은 대략 다음 구조다.

```text
scenario_score = survival_rate × tracking_score
```

따라서 개인 validator에서도 똑같은 형태의 proxy metric을 만든다.

예:

```python
tracking_error = mean(abs(command_velocity - actual_velocity))

tracking_score = exp(-k * tracking_error)

scenario_score = survival_rate * tracking_score
```

주의할 점:

**운영진의 실제 tracking score 세부 공식은 제공 자료에 공개되어 있지 않다.**

따라서 로컬 점수는 실제 예선 점수를 복제하는 것이 아니라 **policy A/B 비교용 상대 지표**로만 사용한다.

즉

```text
Local score = 0.82
```

라고 나왔다고 해서 예선에서 정확히 57.4/70점이 나온다고 생각하면 안 된다.

대신

```text
Policy A = 0.71
Policy B = 0.84
```

처럼 같은 validator에서 비교하는 용도로 쓴다.

---

# 9. Survival 판정

낙상은 단순 높이 하나로만 판단하지 말고 여러 조건을 기록한다.

예:

```text
base height
roll / pitch
projected gravity
body contact
velocity collapse
```

그리고

```text
FALL
NEAR_FALL
RECOVERED
STABLE
```

정도로 상태를 나누면 reward 튜닝 방향을 찾기 쉽다.

예:

```text
Policy A
- 완전 낙상: 2회
- near fall: 8회
- recovery 성공: 6회

Policy B
- 완전 낙상: 0회
- near fall: 4회
- recovery 성공: 4회
```

이면 B가 훨씬 안전하다.

---

# 10. Push Recovery 테스트

push 테스트는 반드시 여러 방향으로 수행한다.

```text
+X
-X
+Y
-Y
```

그리고 힘도 단계화한다.

```text
weak
medium
strong
```

예:

```text
T = 5s   weak +Y
T = 10s  weak -Y
T = 15s  medium +X
T = 20s  medium -X
```

평가할 것:

```text
넘어졌는가?
회복까지 몇 초 걸렸는가?
회복 이후 command tracking이 정상으로 돌아왔는가?
```

단순히 "안 넘어짐"보다 **회복 이후 다시 제대로 걷는지**가 중요하다.

---

# 11. Terrain Test Suite

하나의 큰 맵보다 작은 테스트맵 여러 개를 만든다.

```text
flat.usd
rough_weak.usd
rough_medium.usd
slope_10.usd
slope_20.usd
stairs_10cm.usd
stairs_15cm.usd
```

이 방식의 장점은 실패 원인을 정확히 알 수 있다는 것이다.

예를 들어 하나의 복잡한 경기맵에서 넘어지면

```text
경사 때문인가?
회전 때문인가?
속도 때문인가?
단차 때문인가?
```

판단하기 어렵다.

격리된 test scene을 만들면 바로 확인할 수 있다.

---

# 12. 반복 실행

강화학습/PhysX는 실행마다 조금씩 달라질 수 있으므로 1회 성공으로 판단하면 안 된다.

권장 예시:

```text
각 scenario × 10 seeds
```

또는 빠른 검증에서는

```text
각 scenario × 3 seeds
```

최종 후보 policy는

```text
각 scenario × 20 seeds
```

정도로 비교한다.

---

# 13. Policy 비교 시스템

예를 들어 공식 서버에서 세 개의 policy를 학습했다고 하자.

```text
policy_A.pt
policy_B.pt
policy_C.pt
```

개인 서버에서 다음처럼 비교한다.

```bash
python runner/run_suite.py \
    --robot h1 \
    --policy policies/h1/A/policy.pt \
    --seeds 10
```

결과:

```text
H1 Policy A

Balance        0.96
Forward        0.91
Lateral        0.72
Yaw            0.84
Rough          0.79
Slope          0.75
Push           0.68
-------------------
Weighted       0.825
```

Policy B:

```text
Balance        0.97
Forward        0.88
Lateral        0.83
Yaw            0.88
Rough          0.85
Slope          0.81
Push           0.80
-------------------
Weighted       0.862
```

그러면 training reward가 A가 더 높더라도 **예선 제출 후보는 B를 우선 검토**할 수 있다.

이게 개인 서버 validator의 가장 큰 가치다.

---

# 14. `model_best.pt`를 무조건 믿지 않는다

현재 제공된 finalize 로직은 training reward가 가장 높았던 checkpoint와 가까운 모델을 `model_best.pt`로 선택한다.

하지만

```text
높은 training reward
        ≠
높은 예선 평가 점수
```

일 수 있다.

예를 들어

```text
Policy A
training reward = 높음
tracking = 매우 좋음
push recovery = 나쁨

Policy B
training reward = 약간 낮음
tracking = 좋음
push recovery = 매우 좋음
```

이라면 공식 평가에서는 B가 더 유리할 수 있다.

따라서 가능하다면 공식 서버에서 생성된 후보 정책들을 보관해두고 로컬 validator에서 비교한다.

---

# 15. 결과 Dashboard

최종적으로 HTML 하나에서 보는 것을 추천한다.

예:

```text
┌──────────────────────────────┐
│ H1 Policy #12                │
├──────────────────────────────┤
│ Survival Rate     96.2%      │
│ Tracking Score    0.89       │
│ Estimated Score   0.856      │
│ Falls             4 / 100    │
└──────────────────────────────┘

Scenario
Balance        ██████████ 0.98
Forward        █████████░ 0.91
Lateral        ████████░░ 0.82
Yaw            █████████░ 0.88
Rough          ████████░░ 0.81
Slope          ███████░░░ 0.76
Push           ████████░░ 0.83
```

그리고 policy끼리 바로 비교한다.

```text
                A       B       C
Balance       0.96    0.97    0.91
Forward       0.91    0.88    0.94
Rough         0.79    0.85    0.73
Push          0.68    0.80    0.61
---------------------------------
Weighted      0.825   0.862   0.803
```

---

# 16. 추천 개발 순서

## Phase 1 — 최소 실행 환경

목표:

```text
policy.pt 하나를 로드해서 H1/Go2가 정상적으로 걷게 만들기
```

필요:

- Isaac Sim
- Isaac Lab
- robot asset
- policy loader
- observation
- action → joint target

여기까지 먼저 성공한다.

---

## Phase 2 — Flat command tester

```text
정지
전진
후진
좌
우
좌회전
우회전
```

command를 자동으로 바꾸면서 velocity error를 저장한다.

이 단계만으로도 reward tuning에 상당한 도움을 받을 수 있다.

---

## Phase 3 — Fall / Push tester

추가:

```text
fall detector
push force
recovery timer
```

이 단계부터 안정성을 객관적으로 비교할 수 있다.

---

## Phase 4 — Terrain suite

추가:

```text
rough
slope
stairs
```

이 시점에서 사실상 **예선용 policy benchmark**가 완성된다.

---

## Phase 5 — Batch evaluation

```text
policy × scenario × seed
```

자동 반복.

예:

```text
3 policies
× 7 scenarios
× 10 seeds
= 210 simulations
```

사람이 하나씩 `play.py`를 보는 것보다 훨씬 효율적이다.

---

## Phase 6 — Report

자동으로

```text
CSV
JSON
plot
HTML report
```

생성.

최종적으로 reward 변경과 결과를 연결한다.

예:

```text
termination_penalty
-5 → -50

Result
Fall rate
14% → 5%

Tracking
0.91 → 0.88
```

그러면 다음 training에서

```text
안정성을 더 올릴지
tracking을 회복할지
```

근거를 가지고 결정할 수 있다.

---

# 17. 공식 서버와 개인 서버 역할 분리

가장 중요하다.

## 공식 대회 서버

여기서만:

```text
reward 수정
train.py
policy 생성
제출용 policy.pt 생성
```

## 개인 NVIDIA 서버

여기서는:

```text
policy.pt 실행
영상 확인
scenario benchmark
로그 수집
그래프 생성
policy 비교
reward 변경 방향 분석
```

**optimizer step / gradient update / RL training은 하지 않는다.**

개인 서버에서 학습해 만든 policy를 제출하는 것은 규정상 금지되어 있다.

---

# 18. 서버에 넣지 말아야 할 것

가능하면 다음은 개인 서버용 repo에서 제거한다.

```text
practice_key.bin
실제 Gemini credential
대회 계정 credential
submit token
backend credential
```

예선 validator에는 애초에 Gemini가 필요하지 않다.

따라서 `GameAgent` 자체를 제거하는 것이 가장 깔끔하다.

---

# 19. 경기 엔진은 별도 폴더에 보존

원본 `practice_sim`을 수정하지 말고

```text
original/
    practice_sim/

prelim-validator/
    ...
```

처럼 분리한다.

그러면 나중에 본선 진출 시 원본 경기 엔진을 다시 사용할 수 있다.

예선을 위해 경기 엔진을 마구 뜯어고쳤다가 본선 준비 때 원본 구조를 잃어버리는 상황을 방지한다.

---

# 20. 예선 통과 목표 기준 추천 우선순위

```text
1. Go2 baseline 확보
2. Go2 rough / slope / stairs 안정화
3. Go2 push recovery
4. H1 balance + forward tracking
5. H1 rough / slope
6. H1 push recovery
7. 두 로봇 모두 제출 가능한 상태 확보
8. 이후 H1 고단차 / 본선 대비
```

예선은 **H1 최고점 + Go2 최고점 합산**이므로 한 로봇만 극단적으로 파는 것보다 둘 다 실전 가능한 점수를 확보하는 전략이 유리하다.

---

# 21. 권장 실제 운용 루프

```text
[1]
공식 서버
reward 수정

      ↓

[2]
공식 서버
train.py

      ↓

[3]
공식 서버
play.py 빠른 육안 확인

      ↓

[4]
policy.pt 다운로드

      ↓

[5]
개인 서버
자동 7-scenario benchmark

      ↓

[6]
개인 서버
이전 policy와 비교

      ↓

[7]
실패 원인 분석

예:
- lateral tracking 부족
- push recovery 부족
- slope에서 pitch instability

      ↓

[8]
다음 reward 변경안 결정

      ↓

[1]로 반복
```

이 방식이면 개인 GPU를 **대회 서버 학습시간을 절약하는 분석 장비**로 활용할 수 있다.

---

# 22. 내가 가장 추천하는 MVP

처음부터 거창하게 만들 필요는 없다.

최소 버전은 이것만 있으면 된다.

```text
policy.pt loader
        ↓
Isaac Sim robot
        ↓
command sequence
        ↓
velocity / orientation recorder
        ↓
fall detector
        ↓
CSV
```

그리고 7개 scenario runner를 붙인다.

최종 구조:

```text
              ┌─ H1 Balance
              ├─ H1 Forward
              ├─ H1 Lateral
              ├─ H1 Yaw
policy.pt ────┼─ H1 Rough
              ├─ H1 Slope
              └─ H1 Push

                     ↓

                metrics.csv

                     ↓

               compare.py

                     ↓

             다음 reward 결정
```

본선 경기 엔진 전체를 복제하는 것보다 **이 구조가 예선 통과라는 현재 목표에 훨씬 직접적이다.**

---

# 23. 요약

개인 NVIDIA 서버의 역할은 다음 한 문장으로 정의하면 된다.

> **운영진 서버에서 학습된 여러 policy를 예선과 유사한 조건에서 대량 실행해, 어떤 policy와 reward 방향이 더 안정적인지 판단하는 오프라인 검증 서버.**

만들어야 할 핵심은

```text
Policy Runtime
+ Scenario Runner
+ Metrics Collector
+ Batch Evaluator
+ Policy Comparator
```

네 가지다.

반대로 지금은

```text
Gemini
Cube Game
Opponent
Car
Backend
Tournament
```

등은 없어도 된다.

예선을 통과한 뒤 원본 `practice_sim`을 기반으로 본선용 시스템을 다시 확장하면 된다.

---

# 규정상 주의

이 설계의 전제는 **개인 서버에서 정책을 학습하지 않는 것**이다.

예선 규정상 정책 생성은 운영진이 제공한 학습 환경에서 수행되어야 하며, 개인/학교 장비에서 결과물을 실행·관찰·검토하는 것은 허용되지만 외부 장비에서 학습해 생성한 정책으로 제출물을 대체하는 것은 금지된다.

또한 운영진이 배포한 자격증명은 외부로 유출하거나 대회 외 용도로 사용해서는 안 된다.

따라서 개인 서버는 철저히

```text
Inference / Evaluation / Analysis Only
```

로 운용하는 것을 권장한다.
