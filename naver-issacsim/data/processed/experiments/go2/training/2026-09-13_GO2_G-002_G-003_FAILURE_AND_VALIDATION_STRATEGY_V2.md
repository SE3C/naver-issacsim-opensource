# [학습] Go2 G-002·G-003 초기 부정 결과 분석 및 가설 검증 전략 보강본

> 관리 안내 (2026-10-13): **학습** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](../../../../../research/EXPERIMENTS.md)를 확인한다.

## 1. 작성 목적

기존 G2(`track_lin_vel_xy_exp: 1.0 → 1.25`) 실험까지는 별도로 정리되어 있으므로, 본 문서에서는 그 이후 진행한 G3와 G4 실험 결과를 정리하고, 이후 외부 자료와 기존 장기 baseline을 다시 검토하면서 확인한 **초기 조기중단 방식의 한계**를 보강한다.

처음에는 각 가설을 1K 학습으로 설정한 뒤 약 70~200 iteration 구간의 terrain, base-contact, tracking 지표를 보고 조기중단하였다. 그러나 이후 검토 결과, 이 구간의 부정적인 수치만으로 reward 가설 자체를 최종 기각하는 것은 지나치게 이른 판단일 수 있다고 보았다.

따라서 본 문서에서는 G3와 G4를 더 이상 “최종 실패”로 표현하지 않고 **early-screen negative(초기 구간에서 부정적인 신호가 확인된 상태)**로 재분류한다. 또한 G2 역시 같은 기준으로 재평가하며, 앞으로는 동일 학습량의 baseline과 비교하면서 3K와 5K를 중심으로 가설을 검증한다.

이번 실험들은 모두 한 번에 하나의 reward 항목만 변경하는 방식으로 진행하였다. 공통 조건은 Go2 `Quadruped-v0`, 4096 envs, seed 42이며, 별도로 언급하지 않은 reward 및 PPO 설정은 baseline을 유지하였다.

---

## 2. G-002 — 수직 움직임 억제 강화

### 2.1 가설

Go2가 초반에 자세를 제대로 잡지 못하고 넘어지는 원인 중 하나가 몸통의 수직 바운싱일 수 있다고 보았다. 이에 따라 기본값인 `lin_vel_z_l2 = -3.0`을 더 강하게 적용하면 위아래 움직임이 줄어들고, 낙상률과 base-contact termination이 감소할 것으로 예상하였다.

변경값은 다음과 같다.

```python
"lin_vel_z_l2": -3.0  ->  -4.0
```

그 외 `track_lin_vel_xy_exp`, `feet_air_time`, `ang_vel_xy_l2`, `action_rate_l2` 등은 baseline 값을 유지하였고, `flat_orientation_l2`는 비활성 상태로 두었다.

### 2.2 주요 결과

97 iteration에서는 다음과 같은 값이 확인되었다.

| 지표 | 97 iter |
|---|---:|
| Mean reward | 3.64 |
| Mean episode length | 959.93 |
| Terrain level | 1.3742 |
| XY error | 1.9591 |
| Yaw error | 0.9074 |
| Timeout | 86.12% |
| Base contact | 13.88% |

145 iteration에서는 생존 관련 지표가 일시적으로 좋아졌다.

| 지표 | 145 iter |
|---|---:|
| Mean reward | 7.56 |
| Mean episode length | 981.09 |
| Terrain level | 0.6992 |
| XY error | 1.7140 |
| Yaw error | 0.6801 |
| Timeout | 93.05% |
| Base contact | 6.95% |

205 iteration에서는 terrain level이 더 크게 떨어졌고, 생존 관련 지표도 다시 악화되었다.

| 지표 | 205 iter |
|---|---:|
| Mean reward | 8.96 |
| Mean episode length | 920.29 |
| Terrain level | 0.1741 |
| XY error | 1.5303 |
| Yaw error | 0.4586 |
| Timeout | 88.06% |
| Base contact | 11.97% |

### 2.3 초기 해석

G3에서는 학습이 진행될수록 XY 및 yaw 추종 오차는 감소하였다. 특히 205 iteration에서는 XY error 1.53, yaw error 0.46까지 내려가 추종 자체는 개선되는 모습을 보였다.

반면 terrain level은 `1.3742 → 0.6992 → 0.1741`로 지속적으로 하락하였다. 또한 145 iteration에서 6.95%까지 감소했던 base-contact termination이 205 iteration에서 다시 11.97%로 증가하였고, episode length도 감소하였다.

초기 구간만 보면 `lin_vel_z_l2=-4.0`은 추종 일부를 개선했지만 terrain curriculum 진행에는 좋지 않은 방향으로 보였다.

그러나 이 실험은 205 iteration에서 중단되었다. 이후 외부 자료와 기존 장기 baseline을 다시 검토한 결과, 이 정도 학습량만으로 “장기적으로 나쁜 reward”라고 단정하기에는 근거가 부족하다.

따라서 G3의 현재 분류는 다음과 같다.

> **G3 상태: early-screen negative. 장기 실패 미확정. 재검증 우선순위는 낮음.**

---

## 3. G-003 — `feet_air_time` 강화

### 3.1 가설

기본 `feet_air_time=0.01`이 너무 낮아 초반에 발을 충분히 들지 못하고, 이 때문에 험지나 착지 상황에서 안정적인 보행이 늦게 형성될 수 있다고 보았다.

따라서 발 체공 보상을 소폭 높이면 발을 조금 더 적극적으로 들게 되고, terrain 진행과 보행 형성이 빨라질 수 있다는 가설을 세웠다.

변경값은 다음과 같다.

```python
"feet_air_time": 0.01  ->  0.03
```

이 실험을 시작하기 전 G2에서 변경했던 `track_lin_vel_xy_exp=1.25`는 baseline인 1.0으로 복구하였다. `lin_vel_z_l2`도 baseline인 -3.0을 유지하였고, 나머지 reward는 모두 기존값을 유지하였다.

### 3.2 주요 결과

37 iteration에서는 terrain level이 아직 2.5489로 비교적 높았지만 base-contact termination이 29.54%로 높게 나타났다.

| 지표 | 37 iter |
|---|---:|
| Mean reward | -8.55 |
| Mean episode length | 820.84 |
| Terrain level | 2.5489 |
| XY error | 1.5012 |
| Yaw error | 1.1996 |
| Timeout | 63.93% |
| Base contact | 29.54% |

95~97 iteration에서는 episode length가 950 이상으로 증가하고 base-contact termination도 조금씩 감소했지만 terrain level 역시 계속 하락하였다.

| 지표 | 95 iter | 96 iter | 97 iter |
|---|---:|---:|---:|
| Terrain level | 1.3220 | 1.3013 | 1.2798 |
| XY error | 1.7347 | 1.6935 | 1.6722 |
| Yaw error | 0.8813 | 0.8987 | 0.8526 |
| Timeout | 81.76% | 82.37% | 82.92% |
| Base contact | 18.24% | 17.63% | 17.08% |
| Episode length | 966.89 | 967.00 | 957.53 |

115 iteration에서는 안정성 관련 지표가 추가로 개선되었다.

| 지표 | 115 iter |
|---|---:|
| Mean reward | 6.63 |
| Mean episode length | 928.18 |
| Terrain level | 1.0061 |
| XY error | 1.6805 |
| Yaw error | 0.6985 |
| Timeout | 89.61% |
| Base contact | 10.39% |

### 3.3 초기 해석

G4에서는 시간이 지나면서 base-contact termination이 감소하고 timeout 비율이 증가하였다. 즉 초반 생존 자체는 어느 정도 개선되는 모습을 보였다.

반면 기대했던 terrain progression 개선은 확인되지 않았다. terrain level은 37 iteration에서 2.55였으나 이후 지속적으로 떨어져 115 iteration에서 약 1.01까지 내려갔다. XY tracking 또한 1.68 수준으로 남아 있어 `feet_air_time` 증가가 초기 추종 성능을 눈에 띄게 개선했다고 보기는 어려웠다.

하지만 이 실험 역시 115 iteration에서 중단되었다. 따라서 현재 데이터가 말해주는 것은 “초기 115 iteration에서 기대했던 효과가 바로 나타나지 않았다”는 정도이며, 1K·3K·5K에서도 같은 결과가 유지된다는 의미는 아니다.

따라서 G4의 현재 분류는 다음과 같다.

> **G4 상태: early-screen negative. 장기 실패 미확정. 재검증 우선순위는 중간.**

---

## 4. 이번에 새롭게 확인한 핵심 문제

### 4.1 terrain level 하락 자체를 실패로 본 기준이 너무 강했다

초기에는 terrain level이 약 3.5에서 시작한 뒤 1.x 또는 0.x까지 내려가면 해당 reward가 locomotion을 방해한다고 판단하였다.

그러나 curriculum learning에서는 정책이 현재 난이도를 해결하지 못하면 더 쉬운 terrain으로 내려가는 것이 정상적인 동작일 수 있다. 즉 terrain level 감소는 **정책이 아직 어려운 지형을 해결하지 못하고 있다는 신호**이지, 그 reward 설정이 최종적으로 회복할 수 없다는 증거는 아니다.

특히 기존 개인 Go2 baseline에서도 장기 학습 중 상당히 늦은 시점까지 terrain level이 낮았지만, 이후 크게 회복한 기록이 있다.

- 약 4.5K 부근: terrain 약 0.92, XY error 약 1.17
- 약 9.5K 부근: terrain 약 5.83, XY error 약 0.72

같은 run 안에서도 수천 iteration 이후 결과가 크게 달라졌기 때문에 100~200 iteration의 terrain 값만 보고 reward를 최종 기각하는 것은 위험하다.

### 4.2 1K는 데이터량이 적은 것은 아니지만, 최종 정책 성격을 확정하기에는 짧을 수 있다

4096 envs와 약 24 steps/env 구조라면 한 policy update에서 약 98,304 environment steps가 수집된다. 1K면 총 transition 수 자체는 매우 많다.

하지만 PPO에서 중요한 것은 transition 수뿐 아니라 **정책 업데이트 횟수와 curriculum이 충분히 전개될 시간**이다. 정책이 쉬운 지형에서 기본 locomotion을 형성하고 더 어려운 terrain으로 다시 올라가는 과정은 여러 번의 curriculum 이동과 policy update를 필요로 할 수 있다.

따라서 1K는 의미 없는 짧은 run은 아니지만, 모든 reward 가설을 최종 판정하기 위한 보편적인 기준으로 사용하기에는 부족할 수 있다.

---

## 5. 외부 자료에서 확인한 근거

### 5.1 Rudin et al. — `Learning to Walk in Minutes`

Rudin et al.의 quadruped locomotion 연구는 수천 대의 로봇을 병렬로 학습시키고 terrain curriculum을 사용하는 PPO 기반 구조라는 점에서 현재 실험을 해석하는 데 참고가 된다.

논문에서 curriculum은 다음과 같이 동작한다.

- 로봇이 terrain 경계를 넘어 충분히 진행하면 더 높은 난이도로 이동
- episode 종료 시 목표 속도로 요구되는 거리의 절반도 이동하지 못하면 terrain level을 낮춤
- 최고 level을 해결한 로봇은 다시 다양한 level로 분산시켜 catastrophic forgetting을 방지

따라서 terrain level이 내려가는 현상 자체는 curriculum의 실패가 아니라 정책 능력에 따라 난이도를 다시 조정하는 정상 메커니즘이다.

더 중요한 것은 학습 진행 시점이다.

- **500 policy updates:** 경사와 계단 내려가기는 가능하지만, 계단 오르기와 장애물 통과에는 더 많은 학습이 필요
- **1000 policy updates:** 모든 terrain type에서 가장 어려운 level까지 도달
- **1500 policy updates:** 최종 성능으로 수렴시키기 위해 추가 학습

또한 논문의 최종 정책은 **4096 robots, batch size 98,304, 1500 policy updates**를 사용하였다. 이 규모는 현재 Go2 실험의 4096 envs와 iteration당 약 98K transition 구조와 매우 유사하다.

다만 이 연구는 ANYmal 중심이며 terrain, reward, robot dynamics가 현재 대회 Go2와 동일하지 않다. 따라서 “우리도 정확히 1500 iteration이면 충분하다”는 의미로 사용해서는 안 된다.

이 자료가 주는 핵심 교훈은 다음과 같다.

> **500 iteration에서도 어려운 terrain을 아직 못 푸는 것은 충분히 정상일 수 있으며, 초기 curriculum 분포만으로 최종 reward 가설을 기각해서는 안 된다.**

출처:\
N. Rudin, D. Hoeller, P. Reist, M. Hutter, *Learning to Walk in Minutes Using Massively Parallel Deep Reinforcement Learning*, CoRL 2021.\
https://arxiv.org/abs/2109.11978

### 5.2 Isaac Lab 공식 Unitree Go2 rough 설정

Isaac Lab의 Unitree Go2 rough terrain 설정에서는 다음 값이 사용되는 버전이 확인된다.

```text
track_lin_vel_xy_exp = 1.5
track_ang_vel_z_exp  = 0.75
feet_air_time        = 0.01
dof_torques_l2       = -0.0002
dof_acc_l2           = -2.5e-7
```

또한 Go2의 크기가 작기 때문에 terrain 자체도 축소하여 사용한다.

```text
boxes height range       = 0.025 ~ 0.1 m
random rough noise range = 0.01 ~ 0.06 m
```

우리 대회 baseline의 `track_lin_vel_xy_exp=1.0`과 비교하면, G2에서 시험한 `1.25`는 외부 사례에 비추어도 비정상적으로 큰 값은 아니다.

따라서 G2를 73 iteration에서 중단한 것은 현재 관점에서는 지나치게 빠른 판단일 가능성이 있다.

다만 Isaac Lab 버전, terrain, reward stack과 대회 코드가 완전히 같지는 않으므로 `1.5`를 그대로 대회 최적값으로 해석해서는 안 된다.

출처:\
Isaac Lab — Unitree Go2 Rough Environment Configuration\
https://github.com/isaac-sim/IsaacLab/blob/release/3.0.0-beta2/source/isaaclab_tasks/isaaclab_tasks/manager_based/locomotion/velocity/config/go2/rough_env_cfg.py

### 5.3 다른 Go2 locomotion 설정과 reward scale 차이

Unitree Robotics의 `unitree_rl_lab` Go2 locomotion 설정에서는 다음과 같은 예가 확인된다.

```text
track_lin_vel_xy = 1.5
track_ang_vel_z  = 0.75
lin_vel_z_l2     = -2.0
ang_vel_xy_l2    = -0.05
action_rate      = -0.1
flat_orientation = -2.5
feet_air_time    = 0.1
```

이 값들은 우리 대회 baseline과 상당히 다르다. 특히 여러 reward 항목과 termination, curriculum이 동시에 다르기 때문에 단일 coefficient를 직접 비교하여 “더 세다/약하다 = 더 좋다”라고 판단해서는 안 된다.

오히려 이 자료는 다음 사실을 보여준다.

> **reward weight는 전체 reward stack과 환경 설정의 맥락 안에서 해석해야 하며, 한 항목의 절댓값만 보고 정답 범위를 결정하면 안 된다.**

따라서 G3의 `lin_vel_z_l2=-4.0`이나 이후 `ang_vel_xy_l2` 실험도 단순히 다른 프로젝트의 숫자를 복사하기보다, 현재 baseline 대비 단일 변경으로 검증하는 방식이 계속 필요하다.

출처:\
Unitree Robotics — `unitree_rl_lab` Go2 velocity environment configuration\
https://github.com/unitreerobotics/unitree_rl_lab/blob/main/source/unitree_rl_lab/unitree_rl_lab/tasks/locomotion/robots/go2/velocity_env_cfg.py

### 5.4 장기 수치 발산은 reward 가설 검증과 별도로 관리해야 한다

Isaac Lab 공개 이슈/Discussion에도 Unitree Go2 rough locomotion을 다음 조건으로 장기 학습하다가

```text
4096 envs
seed 42
max_iterations 20000
```

`RuntimeError: normal expects all elements of std >= 0.0`

오류가 발생한 사례가 보고되어 있다.

이것은 우리 환경에서 발생한 9.5K 이후 value loss 발산의 원인이 동일하다고 증명하는 자료는 아니다. 그러나 적어도 **Go2 + RSL-RL 장기 학습에서 std 관련 수치 불안정이 외부에서도 보고된 적이 있다**는 점은 확인된다.

따라서 다음 두 문제는 분리하여 관리한다.

1. reward 변경이 locomotion/terrain 성능을 개선하는가
2. 장기 PPO 학습에서 value/std 수치 불안정이 발생하는가

reward 가설이 좋더라도 장기 수치 발산은 별도로 발생할 수 있고, 반대로 장기 발산이 있었다고 reward 가설 자체가 잘못되었다고 볼 수 없다.

출처:\
Isaac Lab Discussion #2868 — Unitree Go2 Training Script Error on Rough Env\
https://github.com/isaac-sim/IsaacLab/discussions/2868

---

## 6. 기존 G-001·G-002·G-003의 재분류

초기 실험 당시에는 G2~G4를 사실상 실패로 처리했으나, 현재는 다음과 같이 재분류한다.

| 가설 | 변경 | 초기 결과 | 현재 분류 | 재검증 우선순위 |
|---|---|---|---|---|
| G2 | `track_lin_vel_xy_exp 1.0 → 1.25` | 73 iter에서 base-contact 증가, terrain 하락 | **early-screen negative** | **높음** |
| G3 | `lin_vel_z_l2 -3.0 → -4.0` | 205 iter에서 terrain 0.174, base-contact 재증가 | **early-screen negative** | 낮음 |
| G4 | `feet_air_time 0.01 → 0.03` | 115 iter에서 terrain 약 1.01, 안정성 일부 회복 | **early-screen negative** | 중간 |

### G2를 우선 재검증하는 이유

G2는 73 iteration에서 종료되었기 때문에 세 실험 중 가장 짧게 관찰되었다.

또한 외부 Isaac Lab Go2 rough 설정에서 `track_lin_vel_xy_exp=1.5`가 사용되는 사례가 확인되기 때문에 `1.25`라는 값 자체는 충분히 검증할 가치가 있다.

따라서 기존 “G2 실패”라는 표현은 다음과 같이 수정한다.

> `track_lin_vel_xy_exp=1.25`는 73 iteration까지의 초기 지표에서 안정성 악화 신호가 있었으나, 학습량이 너무 짧아 최종 성능을 판정할 수 없다. 3K 수준의 재검증을 우선 수행한다.

### G3를 뒤로 미루는 이유

G3는 205 iteration으로 세 실험 중 상대적으로 가장 오래 보았고, terrain level이 0.174까지 강하게 하락하는 초기 신호가 있었다.

또한 baseline 자체가 이미 `lin_vel_z_l2=-3.0`으로 강한 편이므로 `-4.0`으로 추가 강화하는 방향은 현재 우선순위를 낮춘다.

단, 이것 역시 장기 실패 확정은 아니다.

### G4의 위치

G4는 115 iteration에서 terrain은 하락했지만 base-contact와 timeout은 계속 개선되고 있었다. 따라서 단순 실패라고 보기보다는 장기적으로 gait가 형성되는지 확인할 여지가 있다.

G2 재검증 후 서버 시간이 허용되면 3K 재검증 후보로 유지한다.

---

## 7. 수정된 가설 검증 전략

### 7.1 먼저 동일 조건 baseline을 확보한다

앞으로 가설 비교의 기준은 동일한 학습량의 baseline이다.

최소한 다음 두 run을 같은 조건에서 확보한다.

```text
B0 baseline                3K
G2 track_lin_vel_xy=1.25   3K
```

서로 다른 iteration의 결과를 직접 비교하면 reward 효과와 단순 학습량 효과를 구분하기 어렵다.

### 7.2 0~200 iteration — sanity check 전용

이 구간에서는 성능을 평가하지 않는다.

조기중단은 아래와 같은 명백한 이상이 있을 때만 시행한다.

- NaN / Inf 발생
- value loss의 비정상적 폭발
- action std 비정상
- Isaac Sim / RSL-RL 실행 오류
- reward 변경이 의도와 다르게 적용됨
- 학습이 수치적으로 붕괴하여 정상 회복을 기대하기 어려움

terrain level 하락, mean reward 하락, base-contact 일시 증가만으로는 중단하지 않는다.

### 7.3 500 iteration — 초기 curriculum 전개 기록

500 iteration에서는 다음을 기록하되 최종 판정하지 않는다.

- terrain level
- XY / yaw error
- base-contact
- timeout
- episode length
- action std
- 변경 reward contribution

외부 연구에서도 500 update 시점에는 어려운 terrain을 아직 해결하지 못하는 정책이 확인되므로, 이 구간은 진행 상황을 보는 checkpoint로 취급한다.

### 7.4 1K — 중간 checkpoint

1K에서는 baseline과 가설의 차이가 어느 방향으로 벌어지는지 확인한다.

그러나 1K 결과만으로 최종 기각하지 않는다.

특히 terrain curriculum이 아직 회복 단계에 있을 수 있으므로 단일 시점의 terrain 값보다 500→1000 사이의 추세를 함께 본다.

### 7.5 1.5K — 외부 연구 참고 milestone

Rudin et al.에서는 1500 policy updates까지 학습시켜 최종 성능으로 수렴시켰다.

우리 환경에 그대로 적용할 수 있는 숫자는 아니지만, 1K 전후가 quadruped curriculum 학습에서 여전히 변화가 큰 구간일 수 있다는 참고점으로 사용한다.

### 7.6 3K — 1차 가설 판정

현재 프로젝트에서는 3K를 **실질적인 1차 screening 기준**으로 사용한다.

3K에서 baseline과 동일 iteration끼리 비교하여 다음 항목을 종합 평가한다.

- terrain progression 및 최근 추세
- XY tracking
- yaw tracking
- base-contact termination
- timeout
- episode length
- reward 안정성
- action std
- gait 영상

여러 지표에서 baseline보다 일관된 개선이 있으면 5K로 연장한다.

반대로 3K까지 충분히 학습했는데도 대부분의 핵심 지표가 baseline보다 명확히 나쁘다면 그때 기각 후보로 분류한다.

### 7.7 5K — 채택/기각 검증

5K에서는 실제 가설 채택 여부를 결정한다.

동일 5K baseline 또는 동일 조건 reference와 비교하고, TensorBoard 수치뿐 아니라 play 영상도 반드시 확인한다.

다음과 같은 reward hacking이나 이상 gait가 있으면 수치가 좋아도 채택하지 않는다.

- 제자리 버티기
- 지나친 crouch
- hopping / bounding
- 발 끌기
- 과도한 몸통 고정
- tracking 명령을 무시하면서 생존만 하는 행동

### 7.8 5K 이상 — 최종 후보 장기 검증

최종 후보만 8K 전후 또는 서버 시간이 허용하는 범위까지 연장한다.

이 구간에서는 locomotion 성능뿐 아니라 이전 baseline에서 확인된 value loss/std 발산 여부도 함께 본다.

단, 장기 수치 발산은 reward 성능과 별도의 안정성 문제로 기록한다.

---

## 8. 앞으로의 우선 실험 순서

현재 기준으로는 다음 순서가 가장 합리적이다.

1. **B0 baseline 3K**
2. **G2 `track_lin_vel_xy_exp=1.25` 3K 재검증**
3. B0와 G2의 500 / 1K / 1.5K / 2K / 3K 동일 지점 비교
4. G2가 유망하면 5K 연장
5. 시간이 허용되면 G4 `feet_air_time=0.03` 3K 재검증
6. G3 `lin_vel_z_l2=-4.0`은 우선순위를 낮추고 필요할 때 재검증
7. 이후 새 reward 축은 같은 방식으로 3K까지 검증

이렇게 하면 많은 가설을 100~200 iteration씩 빠르게 버리는 방식보다 서버 시간은 더 들지만, **실제로 좋은 가설을 초기 curriculum 하락 때문에 잘못 제거하는 false negative 위험을 줄일 수 있다.**

---

## 9. 현재 결론

G3와 G4는 초기 학습 구간에서 기대했던 효과를 명확히 보여주지 못했다.

- G3 `lin_vel_z_l2=-4.0`은 tracking error가 개선되는 동안 terrain level이 205 iteration에서 0.174까지 내려갔고 base-contact도 다시 증가하였다.
- G4 `feet_air_time=0.03`은 base-contact와 timeout이 점차 개선되었지만 terrain level이 115 iteration에서 약 1.01까지 내려갔고 XY tracking 개선은 뚜렷하지 않았다.

초기 관찰만 보면 두 가설 모두 부정적이다.

그러나 이번에 외부 quadruped curriculum 자료와 기존 Go2 long-run baseline을 다시 검토하면서, **100~200 iteration은 reward 가설을 최종 기각하기에는 지나치게 짧을 수 있다는 점을 확인하였다.**

특히 curriculum은 정책이 어려운 terrain을 해결하지 못하면 의도적으로 난이도를 낮추며, 외부 연구에서도 500 policy update 이후까지 복잡한 terrain 능력이 계속 형성되었다. 기존 개인 Go2 baseline 또한 수천 iteration 이후 terrain과 tracking이 크게 회복되었다.

따라서 앞으로는 기존 실험을 “실패 확정”이 아니라 **early-screen negative**로 관리한다.

가설 검증 기준도 다음과 같이 수정한다.

```text
0~200 iter : 수치적 이상 여부만 확인
500 iter   : 초기 curriculum 진행 기록
1K         : 중간 checkpoint
1.5K       : 외부 연구 참고 milestone
3K         : 1차 가설 판정
5K         : 실제 채택/기각 검증
5K+        : 최종 후보 장기 검증
```

현재 가장 먼저 재검증할 가설은 **G2 `track_lin_vel_xy_exp=1.25`**이다. 동일 조건의 baseline 3K와 비교하여 초기 실패 판정이 실제 false negative였는지 확인한다.

이번 방식 변경의 목적은 더 많은 실험을 하는 것이 아니라, **한정된 서버 시간을 쓰더라도 각 가설에 충분한 학습 기회를 주고 더 신뢰도 높은 근거로 채택·기각하기 위한 것**이다.
