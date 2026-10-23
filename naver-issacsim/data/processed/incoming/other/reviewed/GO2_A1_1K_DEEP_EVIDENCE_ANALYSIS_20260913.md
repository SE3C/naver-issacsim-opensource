# Go2 A1 1K 심층 분석 보고서
## `track_lin_vel_xy_exp=1.5` + `lin_vel_z_l2=-2.0`
### Evidence forensic analysis / curriculum dynamics / numerical stability / checkpoint selection / 3K continuation

- 분석 기준 파일: `A1_GO2_1K_train_evidence.tar.gz`
- Run ID: `20260913-132700-go2-a1-aggressive-tracklin150-lvz-m2-1k`
- 로봇: Unitree Go2
- Task: `Quadruped-v0`
- 작성 기준: 2026-09-13
- 결론 등급: **A1 1K screening 성공 / A1 3K 연장 정당화**
- 주의: 이 문서는 **1K train evidence 자체를 주 자료**로 사용하고, 현재 대화에서 확인된 A1 3K iter 289 로그를 재현성 비교용으로만 추가했다.

---

# 1. 핵심 결론

A1은 다음 두 reward를 동시에 바꾼 공격적 locomotion 실험이다.

```text
track_lin_vel_xy_exp : 1.0  →  1.5
lin_vel_z_l2         : -3.0 → -2.0
```

나머지 주요 reward는 공식 baseline을 유지했다.

```text
track_ang_vel_z_exp = 0.75
ang_vel_xy_l2       = -0.08
dof_torques_l2      = -0.0002
dof_acc_l2          = -2.5e-07
action_rate_l2      = -0.01
feet_air_time       = 0.01
flat_orientation_l2 = 0.0
```

1K 결과는 단순히 “안 넘어졌다”가 아니다.

학습 궤적은 크게:

```text
초기 붕괴
→ 쉬운 terrain으로 curriculum 후퇴
→ survival gait 확보
→ terrain 재상승
→ 800 iter 이후 locomotion 성능 급개선
```

형태를 보였다.

가장 중요한 최종 수치:

```text
iter 999
terrain level      2.8915
XY velocity error  0.7050
yaw error          0.4860
episode length     982.52
timeout            92.34%
base contact       7.66%
mean reward        20.01
action std         0.53
```

특히 terrain은 학습 중 최저:

```text
iter 193
terrain = 0.1666
```

까지 붕괴했지만 이후:

```text
iter 751  → 1.0026
iter 852  → 1.5022
iter 910  → 2.0019
iter 959  → 2.5070
iter 999  → 2.8915
```

로 회복했다.

따라서 이 evidence는 **Go2에서 100~200 iteration의 terrain collapse만 보고 실험을 기각하면 좋은 가설을 놓칠 수 있음**을 매우 강하게 보여준다.

또한 현재 별도로 fresh start한 A1 3K run의 **iteration 289 출력이 이 1K evidence의 iteration 289 출력과 표시된 모든 주요 지표에서 정확히 일치**했다.

이는 같은:

- reward
- seed
- 환경
- 코드
- 하드웨어 계열

조건에서 A1 초반 학습 trajectory가 매우 높은 수준으로 재현되고 있다는 강한 증거다.

---

# 2. Evidence 무결성

업로드된 archive 자체 SHA256:

```text
b1e89933d38c4ca8f1e04d19df13cc3e7e6426db74aeccd0e95819b0cef97fb8
```

archive 내부의 `SHA256SUMS`:

```text
총 검증 항목: 33
실패: 0
```

즉 내부 evidence 파일은 전부 해시 검증을 통과했다.

`validation.json`:

```text
overall = PASS

native_run          PASS
tensorboard         PASS
checkpoints         PASS
source_identity     PASS
official_backup     PASS
collection          PASS
exported_model_best PASS
exported_env        PASS
official_finalize   PASS
```

`metadata.json`:

```text
exit_code                 0
status                    completed
training_status           completed
official_finalize_status  completed
forced_stop               false
evidence_validation       PASS
checkpoint_count          11
collection_errors         []
warnings                  []
```

따라서 이번 분석 대상은 **중간에 끊긴 run이 아니라 정상적으로 1000 iteration을 모두 완료하고 official finalize까지 끝난 run**이다.

---

# 3. 실제 학습 명령과 환경

실제 command:

```bash
/home/shadeform/IsaacLab/isaaclab.sh \
  -p /ephemeral/naver-issacsim-nvidia/training/quadruped/train.py \
  --task Quadruped-v0 \
  --max_iterations 1000 \
  --num_envs 4096 \
  --headless
```

핵심 환경:

```text
seed             = 42
num_envs         = 4096
num_steps_per_env= 24
max_iterations   = 1000
save_interval    = 100
device           = cuda:0
```

한 PPO iteration 당 transition 수:

```text
4096 × 24
= 98,304 transitions
```

1K 총 transition:

```text
98,304,000
```

---

# 4. PPO 설정

`agent.yaml`에서 확인한 주요 설정:

```text
Algorithm: PPO

actor hidden dims:
512 → 256 → 128

critic hidden dims:
512 → 256 → 128

activation              ELU
initial action std      1.0

num_learning_epochs     5
num_mini_batches        4
learning_rate           0.001
schedule                adaptive
gamma                   0.99
lambda                  0.95
entropy_coef            0.008
desired_kl              0.01
max_grad_norm           1.0
value_loss_coef         1.0
clip_param              0.2
clipped value loss      true
NaN check               true
```

공식 report 기준 policy는:

```text
12 actions
약 0.29M parameters
```

이다.

---

# 5. 실제 effective reward 확인

`quadruped_rewards.py`뿐 아니라 **학습 후 저장된 `native_run/params/env.yaml`에서 effective weight를 다시 확인**했다.

실제 적용된 값:

```text
track_lin_vel_xy_exp = +1.5
track_ang_vel_z_exp  = +0.75
lin_vel_z_l2         = -2.0
ang_vel_xy_l2        = -0.08
dof_torques_l2       = -0.0002
dof_acc_l2           = -2.5e-07
action_rate_l2       = -0.01
feet_air_time        = +0.01
```

여기서 한 가지 혼동하기 쉬운 점:

`issacsimz reward show`에서:

```text
track_ang_vel_z_exp 0.75 disabled
```

라고 보였던 것은 **override가 비활성이라는 의미**다.

실제 environment에서는 official baseline 값:

```text
track_ang_vel_z_exp = 0.75
```

가 정상적으로 활성 적용됐다.

즉 A1이 실제로 변경한 것은 정확히 두 개다.

```text
track_lin_vel_xy_exp +0.5
lin_vel_z_l2         +1.0
```

---

# 6. Terrain 구성

이 run은 plane 전용 학습이 아니다.

`env.yaml` 기준:

```text
terrain_type = generator
curriculum   = true
num_rows     = 10
num_cols     = 20
max_init_terrain_level = 5
```

terrain 구성:

```text
pyramid stairs         20%
inverted stairs        20%
random boxes/grid      20%
random rough           20%
pyramid slope          10%
inverted slope         10%
```

즉 final terrain level은 단순 평지 locomotion 수치가 아니라 **stairs / boxes / rough / slope가 섞인 curriculum에서 얻은 결과**다.

---

# 7. 전체 학습 Timeline

## 7.1 핵심 milestone

| Iter | Reward | Terrain | XY error | Episode len | Timeout | Base contact | Std |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | -0.63 | 3.528 | 0.022 | 13 | 1.1% | 0.0% | 1.00 |
| 50 | -1.64 | 1.971 | 1.274 | 706 | 44.9% | 55.1% | 0.64 |
| 100 | 5.26 | 0.949 | 1.327 | 792 | 55.9% | 44.2% | 0.57 |
| 150 | 8.83 | 0.371 | 1.358 | 878 | 75.5% | 24.5% | 0.57 |
| 193 | 9.46 | **0.167** | 1.727 | 933 | 81.3% | 18.7% | 0.56 |
| 200 | 11.00 | 0.170 | 1.457 | 929 | 82.0% | 18.0% | 0.55 |
| 289 | 13.57 | 0.334 | 1.666 | 974 | 94.7% | 5.3% | 0.53 |
| 391 | 14.86 | 0.544 | 1.489 | 979 | 96.1% | 3.9% | 0.52 |
| 451 | 16.42 | 0.654 | 1.146 | 967 | 96.7% | 3.3% | 0.52 |
| 500 | 16.09 | 0.719 | 1.589 | 992 | 95.9% | 4.1% | 0.52 |
| 600 | 16.38 | 0.843 | 1.454 | 994 | 95.2% | 4.8% | 0.52 |
| 700 | 15.76 | 0.934 | 1.468 | 969 | 92.3% | 7.7% | 0.53 |
| 751 | 16.87 | **1.003** | 1.184 | 950 | 93.7% | 6.3% | 0.52 |
| 800 | 16.85 | 1.186 | 1.228 | 971 | 94.6% | 5.4% | 0.52 |
| 841 | 18.41 | 1.431 | **0.950** | 951 | 94.4% | 5.7% | 0.51 |
| 852 | 17.58 | **1.502** | 1.072 | 954 | 94.6% | 5.4% | 0.51 |
| 859 | 17.28 | 1.556 | 1.246 | 969 | 94.6% | 5.4% | 0.51 |
| 900 | 16.32 | 1.915 | 0.937 | 952 | 93.3% | 6.8% | 0.51 |
| 906 | 19.46 | 1.960 | **0.790** | 967 | 93.0% | 7.0% | 0.51 |
| 910 | 18.66 | **2.002** | 0.999 | 994 | 93.1% | 6.9% | 0.52 |
| 932 | **20.95** | 2.241 | **0.642** | 968 | 93.5% | 6.5% | 0.51 |
| 950 | 17.90 | 2.416 | 0.824 | 940 | 93.6% | 6.4% | 0.53 |
| 955 | 18.65 | 2.469 | 0.798 | 962 | 93.3% | 6.7% | 0.54 |
| 959 | 19.97 | **2.507** | 0.752 | 977 | 93.3% | 6.7% | 0.54 |
| 999 | 20.01 | **2.892** | **0.705** | **983** | 92.3% | 7.7% | 0.53 |

---

# 8. 학습을 네 단계로 나눠서 해석

## Phase A — 0~199: 초기 붕괴 / curriculum 강제 후퇴

평균:

```text
terrain mean       1.279
XY error mean      1.294
episode length     744
timeout            57.4%
base contact       33.9%
std                0.627
```

terrain slope:

```text
약 -1.69 level / 100 iter
```

초기 terrain:

```text
3.528
```

에서:

```text
iter 193
0.1666
```

까지 급락했다.

이 구간만 보면 실패처럼 보인다.

특히 iter 50:

```text
base contact 55.1%
```

로 절반 이상이 contact termination이다.

하지만 이것은 “A1이 이미 나쁜 정책으로 수렴했다”기보다:

> 초기 난이도 배치를 받은 거의 미학습 정책이 어려운 terrain에서 연속 실패하면서 curriculum이 빠르게 쉬운 지형으로 내려가는 과정

으로 보는 것이 더 정확하다.

`max_init_terrain_level=5`이기 때문에 iter 0 terrain 3.53은 **정책이 level 3.5를 정복했다는 의미가 아니다.**

이는 official report의:

```text
시작 3.5 → 마지막 2.9이므로 내려감
```

경고를 해석할 때 중요한 점이다.

---

## Phase B — 200~399: survival gait 형성

평균:

```text
terrain mean       0.356
XY error mean      1.550
reward mean       13.60
episode length     971
timeout            92.6%
base contact        7.4%
std                 0.529
```

terrain slope:

```text
+0.189 / 100 iter
```

여기서 중요한 변화는 locomotion보다 **생존성 회복**이다.

```text
iter 193 base contact 18.7%
→ iter 289 5.3%
→ iter 391 3.9%
```

episode length는:

```text
933 → 974 → 979
```

까지 올라간다.

그러나 XY error는 여전히:

```text
약 1.5~1.7
```

수준이다.

즉 이 단계의 정책은 먼저:

> “안 넘어지고 에피소드를 끝까지 버티는 법”

을 확보한다.

G5와 비슷해 보일 수 있지만 이후 trajectory가 결정적으로 다르다.

---

## Phase C — 400~749: 안정화 + 완만한 terrain 회복

평균:

```text
terrain mean       0.800
XY error mean      1.437
reward mean       15.94
episode length     976
timeout            95.2%
base contact        4.85%
std                 0.522
```

terrain slope:

```text
+0.117 / 100 iter
```

이 시기는 생존 정책이 굳어지고 terrain을 천천히 다시 올리는 구간이다.

특징:

```text
episode length 거의 1000
base contact 대부분 3~8%
std 약 0.52
```

즉 탐색은 초기보다 줄었지만 0으로 collapse하지 않았다.

다만 XY는 아직 큰 변동을 보인다.

예:

```text
iter 451 XY = 1.146
iter 500 XY = 1.589
```

따라서 특정 한 iteration의 XY만 보고 정책을 평가하면 안 된다.

---

## Phase D — 750~999: locomotion breakthrough

이 구간이 A1의 핵심이다.

평균:

```text
terrain mean       1.781
XY error mean      1.027
reward mean       17.86
episode length     964
timeout            93.7%
base contact        6.30%
std                 0.520
```

terrain slope:

```text
+0.799 level / 100 iter
```

즉 Phase C보다 curriculum 상승 속도가 크게 빨라졌다.

대표 milestone:

```text
terrain 1.0  → iter 751
terrain 1.5  → iter 852
terrain 2.0  → iter 910
terrain 2.5  → iter 959
terrain 2.89 → iter 999
```

동시에 XY error가:

```text
iter 700  1.468
iter 800  1.228
iter 841  0.950
iter 906  0.790
iter 932  0.642
iter 999  0.705
```

로 크게 줄었다.

이것이 A1을 유망하다고 판단하는 가장 강한 근거다.

---

# 9. Terrain 상승과 실제 velocity tracking의 관계

iter 200 이후:

```text
terrain level ↔ XY error correlation
r ≈ -0.91
```

즉 이 구간에서는 terrain이 올라갈수록 XY error가 **강하게 감소**했다.

이는 단순히:

> 쉬운 terrain에서 오래 살아남으면서 reward만 높이는 정책

으로 보기 어렵게 만든다.

오히려:

```text
생존성 확보
→ locomotion skill 형성
→ 더 어려운 terrain으로 curriculum 상승
→ 실제 velocity tracking error 감소
```

가 함께 나타났다.

특히 750 이후에도:

```text
terrain ↔ XY error
r ≈ -0.84
```

수준의 강한 음의 관계가 유지된다.

상관관계가 인과를 증명하는 것은 아니지만, 최소한 A1의 curriculum progression이 **실제 추종 성능 악화와 함께 일어난 것은 아니다.**

---

# 10. G5와 다른 점

이전 G5:

```text
ang_vel_xy_l2
-0.08 → -0.12
```

는 생존성을 지나치게 우선하면서:

```text
terrain → 0 근처 고착
timeout → 약 98~99%
base contact → 매우 낮음
XY tracking → 충분히 회복하지 않음
```

형태의 survival local optimum을 보였다.

A1은 반대다.

A1 후반:

```text
terrain       2.89
XY error      0.705
timeout       92.3%
base contact   7.7%
episode len   982.5
```

즉 A1은 G5보다 조금 더 넘어질 위험을 감수하지만:

```text
curriculum progression
+
실제 이동 추종
```

을 얻고 있다.

A1의 trade-off는:

```text
극단적 안정
→ 일부 포기

locomotion activity / terrain progression
→ 확보
```

에 가깝다.

현재까지는 이 trade-off가 유리해 보인다.

---

# 11. 정말 더 “공격적으로” 움직였는가?

후반으로 갈수록 여러 움직임 관련 penalty의 절댓값이 커졌다.

예:

### lin_vel_z penalty

```text
iter 517  -0.0222
iter 800  -0.0340
iter 859  -0.0448
iter 999  -0.0549
```

### ang_vel_xy penalty

```text
iter 517  -0.1077
iter 800  -0.1366
iter 999  -0.1720
```

### torque penalty

```text
iter 517  -0.0623
iter 800  -0.0756
iter 999  -0.0961
```

### DOF acceleration penalty

```text
iter 517  -0.1096
iter 800  -0.1384
iter 999  -0.1929
```

### action-rate penalty

```text
iter 517  -0.0754
iter 800  -0.0841
iter 999  -0.1055
```

이는 후반 정책이 더 큰 관절 변화와 몸통 운동을 사용한다는 정황이다.

즉 A1이 단순히 reward 숫자만 바뀐 것이 아니라:

> 실제 행동 distribution도 더 적극적인 locomotion 쪽으로 이동

한 것으로 해석할 수 있다.

다만 이 지표만으로 영상에서 gait가 “빠르다 / 역동적이다”를 확정할 수는 없다.

그 부분은 play video가 필요하다.

---

# 12. 생존성과 공격성의 trade-off

후반 terrain이 올라가면서 base contact도 조금 증가한다.

```text
iter 451   3.34%
iter 600   4.77%
iter 700   7.72%
iter 800   5.42%
iter 900   6.75%
iter 999   7.66%
```

200 이후 terrain과 base contact 관계는 전체적으로 약하지만,
400 이후에는 terrain 상승과 base contact 증가가 함께 나타난다.

즉:

> 더 어려운 terrain으로 올라갈수록 낙상 위험이 조금 늘어난다.

이것은 자연스러운 trade-off일 수 있다.

중요한 것은 최종적으로도:

```text
episode length = 982.52 / 약 1000
```

로 매우 높다는 점이다.

last 10 iterations 평균 base contact:

```text
7.806%
```

공식 report의:

```text
낙상률 7.8%
```

과 일치한다.

따라서 최종 A1은:

> G5만큼 극단적으로 안전하지는 않지만 여전히 높은 생존성을 유지하며 더 어려운 terrain으로 진행

하는 정책이다.

---

# 13. Reward 해석에서 주의할 점

A1의:

```text
track_lin_vel_xy_exp weight
1.0 → 1.5
```

때문에 `Episode_Reward/track_lin_vel_xy_exp` 절대값은 baseline과 직접 비교하면 안 된다.

예:

```text
iter 999
track_lin reward = 1.0767
```

이라고 해서 baseline보다 추종 능력이 50% 좋아졌다고 해석하면 안 된다.

weight 자체가 커졌기 때문이다.

따라서 실제 locomotion 품질 비교에는:

```text
Metrics/base_velocity/error_vel_xy
```

를 더 중요하게 봐야 한다.

A1 final:

```text
XY error = 0.7050
```

이라는 점이 핵심이다.

---

# 14. 탐색 Std 분석

11개 checkpoint의 실제 `distribution.std_param`을 직접 읽었다.

| checkpoint | mean std | min std | max std | NaN | Inf |
|---|---:|---:|---:|---:|---:|
| model_0 | 0.999 | 0.993 | 1.004 | 0 | 0 |
| model_100 | 0.575 | 0.382 | 0.756 | 0 | 0 |
| model_200 | 0.552 | 0.333 | 0.718 | 0 | 0 |
| model_300 | 0.530 | 0.334 | 0.685 | 0 | 0 |
| model_400 | 0.523 | 0.341 | 0.665 | 0 | 0 |
| model_500 | 0.519 | 0.344 | 0.656 | 0 | 0 |
| model_600 | 0.524 | 0.362 | 0.666 | 0 | 0 |
| model_700 | 0.527 | 0.355 | 0.690 | 0 | 0 |
| model_800 | 0.519 | 0.352 | 0.681 | 0 | 0 |
| model_900 | 0.513 | 0.358 | 0.685 | 0 | 0 |
| model_999 | **0.531** | **0.369** | **0.734** | **0** | **0** |

해석:

초기:

```text
std ≈ 1.0
```

에서 100~300 사이 빠르게:

```text
0.57 → 0.53
```

로 감소한다.

그 후:

```text
약 0.51~0.53
```

근처에서 유지된다.

이는:

- 탐색이 죽지 않았고
- std가 0 근처로 collapse하지 않았고
- 음수 std 문제도 없고
- checkpoint가 finite

하다는 뜻이다.

A1 final의 std `0.531`은 현재 단계에서 건강한 탐색 범위로 보인다.

---

# 15. Checkpoint numerical integrity

모든 checkpoint에서:

```text
actor NaN = 0
actor Inf = 0
critic NaN = 0
critic Inf = 0
std > 0
```

를 확인했다.

즉 저장된 11개 checkpoint는 수치적으로 정상이다.

checkpoint 목록:

```text
model_0
model_100
model_200
model_300
model_400
model_500
model_600
model_700
model_800
model_900
model_999
```

따라서 1K run 자체에는 baseline 9.5K에서 경험했던 최종 NaN/Inf 발산과 같은 failure는 없었다.

---

# 16. Value loss 이상 spike

A1 1K에서 가장 주의할 부분이다.

대부분의 value loss는:

```text
약 0.01 ~ 0.03
```

범위였다.

하지만 900 이후 일시적으로 큰 spike가 발생했다.

```text
iter 917  value loss = 3.0768
iter 942             = 4.0019
iter 948             = 1.6339
iter 950             = 10.9995
iter 951             = 8.40 수준
iter 952             = 2.07 수준
iter 953             = 1.26 수준
iter 954             = 0.0296
iter 955             = 0.0245
iter 999             = 0.0235
```

가장 큰 값:

```text
iter 950
10.9995
```

이다.

중요한 점은 **지속 발산이 아니라 즉시 회복했다는 것**이다.

실제로 spike 이후에도:

```text
terrain 계속 상승
XY error 계속 양호
checkpoint finite
std 정상
NaN/Inf 없음
```

이다.

따라서 이것만으로 run 실패로 판단할 이유는 없다.

그러나 기존 장기 baseline에서 value loss가:

```text
수 단위
→ 수십/수백
→ 수만
→ inf
→ nan
```

으로 진행된 경험이 있기 때문에 A1 3K에서 반드시 감시할 필요가 있다.

### 3K 위험 신호

일회성:

```text
3 → 10 → 0.02
```

처럼 회복하면 관찰 지속.

반면:

```text
10
→ 100
→ 1000
→ 지속 상승
```

또는:

```text
Inf / NaN
```

이 나타나면 numerical divergence 가능성이 높다.

---

# 17. 공식 model_best 선택 분석

공식 finalize 결과:

```text
Best by Train/mean_reward

iter   = 932
reward = 20.948
```

save interval이 100이므로 선택된 제출 checkpoint:

```text
model_900.pt
```

이다.

해시 확인:

```text
model_900.pt
SHA256 =
29d0316715d42b52e2c40fd0c548c622422ca64be0f86956a2849ef776479385
```

`exported/model_best.pt` SHA256도:

```text
29d0316715d42b52e2c40fd0c548c622422ca64be0f86956a2849ef776479385
```

로 완전히 동일하다.

즉 official finalize가 의도대로 `model_900.pt`를 model_best로 export했다.

---

# 18. `model_best`와 final checkpoint의 차이

여기에는 중요한 운영 포인트가 있다.

### model_best 근처

iter 900:

```text
terrain       1.9149
XY error      0.9372
episode len   952.06
base contact  6.75%
```

best reward 발생 iter 932:

```text
reward        20.95
terrain       2.2405
XY error      0.6415
episode len   968.46
base contact  6.51%
```

### final

iter 999:

```text
reward        20.01
terrain       2.8915
XY error      0.7050
episode len   982.52
base contact  7.66%
```

즉 final은 최고 scalar reward는 아니지만:

```text
terrain progression
episode survival
```

관점에서는 더 높은 값을 보인다.

따라서 제출 후보를 평가할 때:

> `model_best.pt` 하나만 무조건 가장 좋은 locomotion 정책이라고 가정하면 안 된다.

현재 evidence 기준으로는 최소:

```text
model_900
model_999
```

를 같은 조건의 play/evaluation으로 비교할 가치가 있다.

특히 official model selection은:

```text
Train/mean_reward
```

하나를 기준으로 한다.

우리가 실제로 관심 있는:

```text
terrain
XY tracking
낙상
영상 gait
```

와 순위가 완전히 같다는 보장은 없다.

---

# 19. Official report의 “terrain 시작보다 낮음” 경고 재해석

공식 report는:

```text
시작 terrain 3.5
최종 terrain 2.9

→ 시작보다 내려갔으므로 경고
```

를 표시한다.

이 경고 자체는 report 규칙상 맞다.

하지만 학습 trajectory를 보면 해석을 조금 더 정교하게 해야 한다.

iter 0:

```text
terrain 3.528
episode length 12.97
std 1.0
```

이다.

즉 untrained policy가 13 step 정도밖에 살지 못한다.

`max_init_terrain_level=5`로 초기 환경이 여러 난이도에 배정되어 있기 때문에:

> iter 0의 terrain 3.53을 “로봇이 level 3.53을 이미 정복했다”고 볼 수 없다.

실제 의미 있는 학습 과정은:

```text
3.53 초기 배치
→ 실패
→ 0.17까지 내려감
→ 실제 skill 형성
→ 2.89까지 재등반
```

이다.

따라서 A1을 평가할 때 더 중요한 지표는:

```text
final 2.89 < initial 3.53
```

단일 비교보다:

```text
minimum 0.17
→ final 2.89
```

의 recovery trajectory다.

---

# 20. 100~200 iteration 조기중단 전략에 대한 증거

A1은 이 프로젝트의 실험 방법론에 중요한 교훈을 준다.

iter 193에서:

```text
terrain       0.1666
XY error      1.7266
base contact 18.66%
```

이다.

당시 수치만 보면:

> “terrain collapse, tracking 나쁨, 실패”

라고 판단하기 쉽다.

그러나 806 iteration 후:

```text
iter 999

terrain       2.8915
XY error      0.7050
base contact  7.66%
episode len   982.52
```

가 되었다.

따라서:

> Go2 rough terrain curriculum 실험에서 100~200 iteration의 terrain 값은 최종 reward 가설의 채택/기각 근거로 부족하다.

현재 더 타당한 screening 규칙:

```text
0~200
→ NaN/Inf/실행 오류/명백한 numerical collapse 확인

500
→ survival 및 curriculum 방향 관찰

1K
→ light screening

3K
→ 첫 substantive evaluation

5K
→ 채택/기각 및 제출 후보 판단
```

이다.

---

# 21. 현재 A1 3K와의 재현성

현재 별도 fresh 3K run에서 확인된 iteration 289:

```text
Total steps       28,508,160
Steps/sec         30,278
Collection time   3.159 s
Learning time     0.088 s
Value loss        0.0180
Surrogate loss   -0.0049
Entropy loss      8.9664
Mean reward       13.57
Episode length    973.63
Action std         0.53
track_lin reward   0.4746
track_ang reward   0.5651
lin_vel_z          -0.0260
ang_vel_xy         -0.1078
torque             -0.0630
dof_acc            -0.1138
action_rate        -0.0783
feet_air_time      -0.0013
terrain             0.3336
XY error            1.6656
yaw error           0.4736
timeout            94.72%
base contact        5.28%
```

이 값은 **A1 1K evidence의 iteration 289와 전부 일치**한다.

단순히 terrain/XY만 비슷한 것이 아니라:

- loss
- reward
- std
- 모든 표시 reward component
- termination ratio
- timing 수치 일부까지

일치한다.

따라서 현 시점에서는:

> A1 3K는 1K와 거의 같은 초기 trajectory를 fresh start로 다시 재현하고 있다.

고 볼 근거가 매우 강하다.

이는 A1 1K가 “한 번 우연히 잘 나온 run”일 가능성을 줄인다.

다만 GPU 계산은 일반적으로 완전 결정성을 항상 보장하는 것은 아니므로,
이를 수학적 bitwise determinism의 증명으로 표현하지는 않는다.

---

# 22. A1 3K에서 예상되는 1K 이전 milestone

현재 3K가 1K trajectory를 계속 재현한다면 대략:

```text
iter ~374   terrain 0.5
iter ~751   terrain 1.0
iter ~852   terrain 1.5
iter ~910   terrain 2.0
iter ~959   terrain 2.5
iter 999    terrain 2.89
```

근처의 흐름을 기대할 수 있다.

따라서 현재 3K에서 iter 289 시점 terrain:

```text
0.3336
```

만 보고 걱정할 필요는 없다.

A1 1K에서 정확히 같은 지점 뒤에 강한 recovery가 발생했다.

---

# 23. A1 3K에서 진짜 새로 확인할 구간

1K까지는 이미 evidence가 있다.

따라서 3K의 핵심 연구 질문은:

> **A1이 1K 이후에도 locomotion improvement를 계속 유지하는가?**

이다.

특히 확인할 것:

### 1. terrain

```text
1K 약 2.9
→ 3K에서 3, 4, 5 수준으로 계속 진행 가능한가?
```

### 2. XY error

```text
약 0.7~1.0 수준을 유지하는가?
```

terrain이 올라가도 XY가 다시 1.5~2 이상으로 무너지지 않는지가 중요하다.

### 3. base contact

현재 final:

```text
약 7.7%
```

이다.

3K에서:

```text
10~15% 이상으로 지속 상승
```

하면 공격성의 안정성 비용이 커진 것으로 볼 수 있다.

### 4. episode length

```text
900~1000
```

범위를 장기 유지하는지 확인한다.

### 5. action std

현재:

```text
0.53
```

이다.

장기적으로:

```text
0.4~0.7
```

근처라면 큰 문제는 없어 보인다.

### 6. value loss

가장 중요.

```text
일회성 spike 후 회복
```

인지,

```text
연속 증가 → Inf/NaN
```

인지 반드시 확인한다.

---

# 24. A1 3K 성공 판단 기준 제안

3K 종료 시 다음 그림이면 매우 유망하다.

```text
terrain       ≥ 3~4, 가능하면 그 이상
XY error      ≲ 1.0 전후
episode len   ≥ 900
base contact  ≲ 10~12%
std           finite, 대략 0.3~0.7
NaN / Inf     없음
value loss    장기 발산 없음
```

특히:

```text
terrain ↑
+
XY error 유지/감소
+
base contact 제한적 증가
```

가 동시에 나오면 A1은 **5K 이상의 실제 제출 후보군**에 넣을 가치가 크다.

---

# 25. A1 3K 실패 판단 기준

반대로 다음이면 A1의 공격적 방향에 한계가 있는 것으로 볼 수 있다.

```text
terrain 1K 이후 장기간 정체/하락
XY error 1.5~2 이상으로 지속 악화
base contact 15~20%+ 지속
episode length 크게 하락
std 비정상적으로 0 또는 폭증
value loss 연속 폭발
NaN / Inf
```

특히 terrain이 올라가면서 base contact만 계속 폭증한다면:

> `lin_vel_z_l2=-2.0`이 높은 terrain에서 안정성 여유를 너무 많이 풀어준 것

일 수 있다.

그 경우 다음 ablation 후보는:

```text
track_lin = 1.5 유지
lin_vel_z = -2.5
```

처럼 안정성을 절반 정도 되돌리는 방향이 논리적이다.

다만 3K 결과 전에 추가 변경할 이유는 없다.

---

# 26. `track_lin=1.5`와 `lin_vel_z=-2` 각각의 기여는 아직 분리되지 않음

A1은 두 변수를 동시에 바꿨다.

따라서 현재 evidence만으로:

```text
track_lin 1.5가 주효했는지
lin_vel_z -2가 주효했는지
둘의 interaction이 중요했는지
```

는 분리할 수 없다.

A1이 3K/5K에서도 강하게 나온다면 후속 ablation으로:

```text
A: baseline
B: track_lin 1.5 only
C: lin_vel_z -2 only
D: A1 combination
```

을 같은 길이로 비교하면 causal 해석이 가능하다.

그러나 현재 대회 시간/비용을 고려하면:

> 먼저 A1이 실제 제출 후보인지 확인한 뒤 ablation

하는 것이 효율적이다.

---

# 27. Runtime / 성능

training 내부 출력:

```text
Training time = 3310.24 sec
≈ 55분 10초
```

전체 issacsimz run:

```text
13:27:00.934
→ 14:22:47.492

= 3346.56 sec
≈ 55분 47초
```

따라서 evidence collection/finalize overhead는 매우 작다.

최종 iteration:

```text
Steps/sec ≈ 30,295
```

---

# 28. GPU telemetry

GPU:

```text
NVIDIA L40S
VRAM total ≈ 49 GB
```

전체 telemetry 평균:

```text
GPU utilization  ≈ 76.8%
VRAM             ≈ 7.46 GB
Power            ≈ 215.7 W
Temperature      ≈ 42.8 °C
```

startup 60초 제외:

```text
GPU utilization  ≈ 77.6%
VRAM             ≈ 7.52 GB
Power            ≈ 217.3 W
Temperature      ≈ 43.0 °C
```

최대:

```text
GPU util   89%
VRAM       7.54 GB
Power      248.78 W
Temp       44°C
```

즉:

- VRAM 압박 없음
- thermal 문제 없음
- GPU 활용 정상
- hardware throttling 징후 없음

으로 판단된다.

---

# 29. Source mutation 검사

`source/identity.json` 기준 아래 파일은 학습 전후 SHA256이 모두 동일했다.

```text
train.py
play.py
quadruped_rewards.py
pyproject.toml
go2_task/_finalize.py
go2_task/env_cfg.py
go2_task/agent_cfg.py
go2_task/__init__.py
```

결과:

```text
changed_during_run = false
changed_paths      = []
```

즉 학습 도중 source가 바뀌어 결과가 오염된 흔적이 없다.

---

# 30. Output provenance

공식 finalize가 새로 생성/수정한 결과:

```text
model_best.pt
model_best_20260913132713.pt
env.yaml
env_20260913132713.yaml
report.html
```

`model_best.pt`:

```text
size    6,882,219 bytes
SHA256  29d0316715d42b52e2c40fd0c548c622422ca64be0f86956a2849ef776479385
```

`env.yaml`:

```text
SHA256
20bee913eb1e4c85ade4beea181c3cdb678670a41fb8a54c6c9fb1f654fd0205
```

따라서 제출 결과와 학습 환경 provenance가 명확하다.

---

# 31. 현재 평가

## 성능 관점

```text
A1 1K: 성공적인 screening
```

이유:

1. 초기 collapse 이후 curriculum이 명확하게 회복됨.
2. terrain 2.89까지 상승.
3. XY error 0.705까지 감소.
4. episode length 약 983 유지.
5. fall/base-contact 약 7.7% 수준.
6. std 0.53으로 탐색 유지.
7. checkpoint 전부 finite.
8. NaN/Inf 없음.
9. 3K fresh run에서 iter 289 trajectory가 재현됨.

---

## 안정성 관점

```text
주의 필요하지만 현재 정상
```

이유:

- value loss spike 존재
- 후반 base contact 증가
- terrain이 높아질수록 공격성 비용이 증가하는 징후

그러나:

- spike는 회복
- std 정상
- final checkpoint finite
- final performance 유지

이므로 현재는 중단 사유가 아니다.

---

## 제출 후보 관점

```text
1K만으로 제출 확정 X
3K 연장 O
3K가 좋으면 5K 후보 O
```

A1 1K는 “유망한 가설” 단계까지는 충분히 올라왔다.

---

# 32. 최종 결론

A1의 핵심 의미는 단순히:

> “reward를 공격적으로 바꾸니 reward가 높아졌다”

가 아니다.

실제 evidence가 보여주는 것은:

```text
초기 어려운 terrain에서 반복 실패
→ curriculum 0.17까지 후퇴
→ survival gait 확보
→ 약 400~700 동안 천천히 회복
→ 750 이후 locomotion breakthrough
→ terrain 2.89
→ XY error 0.705
```

라는 구조다.

즉 A1은 현재까지:

> **서 있기/생존만 최적화하는 정책에서 벗어나면서도 생존성을 대부분 유지하고, 적극적인 locomotion과 curriculum progression을 동시에 얻은 가설**

로 평가할 수 있다.

특히 G5와 비교하면:

```text
G5
survival ↑
terrain collapse
locomotion 약함

A1
survival 유지
terrain recovery ↑
locomotion ↑
```

라는 차이가 뚜렷하다.

그리고 현재 fresh 3K run이 iter 289까지 1K run과 동일한 수치를 재현했다는 점은:

> A1의 초기 trajectory가 우연한 한 번의 run이 아닐 가능성

을 크게 높인다.

따라서 현재 판단은:

```text
A1 1K
= 성공적인 screening

A1 3K
= 반드시 계속 진행할 가치 있음

A1 3K가 1K 이후에도
terrain↑ + XY 유지 + 낙상 제한
을 보이면

A1 5K
= 실제 제출 후보 검증 가치 높음
```

이다.

---

# 33. 3K 결과를 받을 때 바로 확인할 체크리스트

3K evidence가 나오면 우선 아래 순서로 비교한다.

1. `terrain` 1000 → 3000 trajectory
2. `XY error` 1000 → 3000 trajectory
3. `base_contact`
4. `episode_length`
5. `timeout`
6. `action std`
7. `value loss` spike/발산 여부
8. best checkpoint iteration
9. final checkpoint와 official model_best 비교
10. video에서:
   - 실제 전진
   - turning
   - foot clearance
   - bouncing
   - body roll/pitch
   - stairs/rough 대응
11. 필요하면 `model_best` vs final checkpoint 영상 비교

3K 결과가 확보되면 이 문서를 기반으로 **A1 1K→3K 연속 분석 보고서**로 확장하면 된다.
