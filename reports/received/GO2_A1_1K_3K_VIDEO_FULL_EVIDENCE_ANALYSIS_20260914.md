> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/incoming/other/reviewed/GO2_A1_1K_3K_VIDEO_FULL_EVIDENCE_ANALYSIS_20260914.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# Go2 A1 전체 Evidence 심층 분석 보고서

## 1K → fresh 3K 학습 재현성 · curriculum progression · 수치 안정성 · checkpoint · video · issacsimz evidence 품질

- 분석 대상: 사용자가 제공한 **A1 관련 `.tar.gz` 3개 전부**
- 핵심 실험: `track_lin_vel_xy_exp=1.5`, `lin_vel_z_l2=-2.0`
- 결론: **A1은 1K screening을 넘어 3K에서도 장기 curriculum progression을 실제로 유지했다. 공식 fresh 5K 검증으로 넘길 근거가 충분하다.**
- 가장 중요한 단서: **final terrain 5.3393 / XY error 0.6522 / base contact 8.98% / episode length 959.37 / final std 0.61**

> 이 보고서의 수치 분석은 세 archive 내부의 `console.log`, TensorBoard event, checkpoint, `env.yaml`, `agent.yaml`, `report.html`, validation/provenance/source identity, GPU telemetry, video 및 SHA256을 직접 확인하여 작성했다. 외부 자료로 빈칸을 채우지 않았다.

---

# 1. 분석 대상 archive와 무결성

| 구분 | 파일 | 압축 크기 | archive SHA256 |
|---|---|---:|---|
| A1 1K train | `A1_GO2_1K_train_evidence.tar.gz` | 79.5 MiB | `b1e89933d38c4ca8f1e04d19df13cc3e7e6426db74aeccd0e95819b0cef97fb8` |
| A1 3K train | `20260913-144615-go2-a1-aggressive-tracklin150-lvz-m2-3k.tar.gz` | 202.3 MiB | `68a880bc12d624504bdda6ecc3456db1e4add4183cbaf1c73868251511715c31` |
| A1 3K video | `20260913-173221-20260913-144615-go2-a1-aggressive-tracklin150-lv.tar.gz` | 17.8 MiB | `c5e19b7a00596094f14f049da6db39a85e44791c033566d007770ff89fcedb5b` |

세 archive 모두 내부 `SHA256SUMS` 검증을 통과했다.

| Evidence | 내부 파일 수 | SHA256SUMS 항목 | 비압축 총량 | validation |
|---|---:|---:|---:|---|
| 1K train | 34 | 33 | 88.7 MiB | **PASS** |
| 3K train | 54 | 53 | 226.5 MiB | **PASS** |
| 3K video | 21 | 20 | 18.1 MiB | **PASS** |

따라서 이번 분석에서 사용한 원본은 손상된 archive가 아니다.

---

# 2. Executive summary

이번 A1 실험의 핵심은 다음과 같다.

1. **1K와 fresh 3K의 첫 1000 iteration이 사실상 동일하게 재현됐다.** 비성능(non-Perf) TensorBoard scalar 25개 계열의 step 0~999 값이 float 저장값 기준으로 전부 동일했고, `model_0`부터 `model_900`까지 checkpoint SHA256도 전부 동일했다.
2. Curriculum은 `3.5284 → 0.1666 → 5.3393`의 명확한 **V형 회복 후 장기 상승**을 보였다. 초기 level 3.5는 미학습 정책의 능력이 아니라 초기 배치 효과였고, 정책은 실제로 0.17까지 후퇴한 뒤 재등반했다.
3. 3K 후반은 한 번 운 좋게 5.34를 찍은 것이 아니다. 마지막 500 iter 평균 terrain은 **5.1599**, 마지막 100 iter 평균은 **5.2510**이었다.
4. 난이도가 올라간 뒤 오히려 생존성은 다시 좋아졌다. 1500~1999 평균 base-contact 11.43% → 2000~2499 10.17% → 2500~2999 **9.20%**로 감소했고, 평균 episode length는 같은 구간 **939.7 → 946.7 → 952.8**로 증가했다.
5. 최종 tracking도 강하다. iter 2999에서 XY error **0.6522**, last-100 평균 **0.7015**이다. mature phase에서 terrain은 계속 상승했지만 XY tracking은 대체로 0.7대에서 유지됐다.
6. 수치적으로 **fatal divergence는 없었다.** 31개 checkpoint의 actor/critic은 모두 NaN=0, Inf=0이며 std도 전부 양수였다. 그러나 critic `value_loss`는 반복적으로 큰 transient spike를 보였고 최대 **104.1677 @ iter 2912**까지 올라갔다. 이 부분은 공식 5K에서 반드시 모니터링해야 한다.
7. official finalize가 고른 `model_best.pt`는 SHA256상 정확히 `model_2900.pt`이다. 최고 reward는 iter 2905의 **21.45**였기 때문에 이전 저장점 2900을 선택했다.
8. final `model_2999.pt`는 model_best와 다른 정책이며, final terrain이 더 높고 tracking/낙상도 나쁘지 않다. **제출 전 `model_2900`과 `model_2999`를 동일 조건으로 직접 비교할 가치가 높다.**
9. video evidence는 parent 3K run과 checkpoint SHA로 정확히 연결되고, **1920×1080 / 50 FPS / 999 frames / 19.98 s / H.264** 영상이 정상 생성됐다. 이번 video console에는 이전에 보였던 tracking-camera `AttributeError` traceback도 없다.
10. `issacsimz` evidence 기록 품질은 전반적으로 매우 좋다. 특히 checkpoint 보존, source-before/after hash, delta provenance, GPU telemetry, train→video lineage가 강점이다. 다만 child runtime 버전과 transient numerical spike를 더 직접 요약하면 증거성이 더 좋아질 수 있다.

---

# 3. 실험 설정: 실제 effective configuration

## 3.1 학습 명령

### 1K
```bash
/home/shadeform/IsaacLab/isaaclab.sh -p /ephemeral/naver-issacsim-nvidia/training/quadruped/train.py --task Quadruped-v0 --max_iterations 1000 --num_envs 4096 --headless
```

### fresh 3K
```bash
/home/shadeform/IsaacLab/isaaclab.sh -p /ephemeral/naver-issacsim-nvidia/training/quadruped/train.py --task Quadruped-v0 --max_iterations 3000 --num_envs 4096 --headless
```

3K는 1K checkpoint resume가 아니라 **동일 seed/config의 fresh run**이다.

## 3.2 PPO

`agent.yaml`에서 확인되는 핵심값:

```text
seed                  42
num_envs              4096
num_steps_per_env     24
transitions / iter    98,304
3K total transitions  294,912,000
save_interval         100
actor MLP             512 → 256 → 128
critic MLP            512 → 256 → 128
activation            ELU
initial std           1.0
PPO epochs            5
mini-batches          4
learning rate         0.001, adaptive
gamma                 0.99
lambda                0.95
entropy coef          0.008
desired KL            0.01
max grad norm         1.0
clip param            0.2
NaN check             enabled
```

## 3.3 A1 reward

실제 저장된 `env.yaml` 기준 effective weights:

| Reward | Baseline | A1 | 변화 |
|---|---:|---:|---:|
| `track_lin_vel_xy_exp` | 1.0 | **1.5** | +0.5 |
| `lin_vel_z_l2` | -3.0 | **-2.0** | +1.0 |
| `track_ang_vel_z_exp` | 0.75 | 0.75 | 없음 |
| `ang_vel_xy_l2` | -0.08 | -0.08 | 없음 |
| `dof_torques_l2` | -0.0002 | -0.0002 | 없음 |
| `dof_acc_l2` | -2.5e-7 | -2.5e-7 | 없음 |
| `action_rate_l2` | -0.01 | -0.01 | 없음 |
| `feet_air_time` | 0.01 | 0.01 | 없음 |

A1은 정확히 **두 변수를 동시에 바꾼 combo 실험**이다. 따라서 현재 evidence만으로 두 변경 중 어느 하나의 단독 인과효과를 분리할 수는 없다.

## 3.4 terrain

실제 terrain generator:

```text
terrain_type            generator
curriculum              true
rows × cols             10 × 20
max_init_terrain_level  5
terrain patch           8 m × 8 m
horizontal scale        0.1
vertical scale          0.005
```

혼합 terrain:

- pyramid stairs 20%
- inverted pyramid stairs 20%
- random boxes/grid 20%
- random rough 20%
- pyramid slope 10%
- inverted slope 10%

명령 범위는 `lin_vel_x -1~2 m/s`, `lin_vel_y -0.6~0.6 m/s`, `ang_vel_z -1~1 rad/s`이며 episode horizon은 20초다. `base_contact`는 base의 illegal contact로 종료된다.

---

# 4. 1K ↔ fresh 3K 재현성: 이번 evidence에서 가장 강한 검증

두 run의 configuration을 직접 diff하면:

- `source/quadruped_rewards.py`: **byte-identical**
- source identity에 기록된 `train.py`, `play.py`, reward, task cfg/finalize 파일 hash: **동일**
- IsaacLab commit: **`3e73d6dd79080fd7632488c061052a6edd52e230`**, 양쪽 모두 working tree clean
- `agent.yaml` 차이: **`max_iterations: 1000 → 3000`뿐**
- `env.yaml` 차이: **run log directory뿐**

더 강한 것은 결과 자체다.

### TensorBoard scalar

1K와 3K의 step 0~999에 대해 timing/Perf 계열을 제외한 모든 기록 scalar를 직접 비교했다.

```text
Curriculum
Episode_Reward/*
Episode_Termination/*
Loss/value
Loss/surrogate
Loss/entropy
Loss/learning_rate
Metrics/base_velocity/*
Policy/mean_std
Train/mean_reward
Train/mean_episode_length
```

**모든 값이 TensorBoard float 저장값 기준으로 정확히 동일했다.**

### Checkpoint

`model_0`~`model_900` 중 공통 저장점 10개가 모두 byte-identical SHA256이었다:

```text
0, 100, 200, 300, 400, 500, 600, 700, 800, 900
```

즉 1K가 우연히 한 번 잘 풀린 run이고 3K가 전혀 다른 trajectory였다는 해석은 evidence와 맞지 않는다. **첫 1000 iteration의 학습 궤적은 실질적으로 재현되었다.**

성능 관련 timing scalar(`FPS`, collection/learning time)는 당연히 완전 동일하지 않았지만, 정책 학습 scalar와 checkpoint는 동일했다.

---

# 5. Curriculum trajectory 전체 해부

## 5.1 핵심 궤적

- 초기: **3.5284 @ iter 0**
- 최저: **0.1666 @ iter 193**
- 초기 평균 level 재돌파: **3.5287 @ iter 1072**
- 최종: **5.3393 @ iter 2999**

즉:

```text
3.5284 (초기 배치)
   ↓
0.1666 (iter 193, 실제 curriculum 후퇴 최저)
   ↑
3.5287 (iter 1072, 초기값 재돌파)
   ↑
5.0002 (iter 2253)
   ↑
5.3393 (iter 2999)
```

초기값 3.53은 `max_init_terrain_level=5`의 초기 분포에서 나온 값이므로 **미학습 정책의 실제 정복 수준으로 읽으면 안 된다.** 정책은 실제로 0.17까지 내려갔다가 다시 올라왔다.

## 5.2 실제 회복 milestone

| Terrain threshold | 최초 재돌파 iteration | 기록값 |
|---:|---:|---:|
| 0.50 | 374 | 0.5028 |
| 1.00 | 751 | 1.0026 |
| 1.50 | 852 | 1.5022 |
| 2.00 | 910 | 2.0019 |
| 2.50 | 959 | 2.5070 |
| 3.00 | 1011 | 3.0114 |
| 3.50 | 1069 | 3.5011 |
| 4.00 | 1140 | 4.0008 |
| 4.50 | 1402 | 4.5006 |
| 5.00 | 2253 | 5.0002 |
| 5.10 | 2403 | 5.1028 |
| 5.20 | 2779 | 5.2000 |
| 5.25 | 2960 | 5.2522 |
| 5.30 | 2985 | 5.3023 |

특히 1K 종료값 2.8915 이후:

```text
3.0  @ 1011
3.5  @ 1069
4.0  @ 1140
4.5  @ 1402
5.0  @ 2253
5.2  @ 2779
5.3  @ 2985
5.3393 @ 2999
```

## 5.3 phase별 평균

| 구간 | terrain 평균 | terrain slope /100 iter | XY error | base contact | episode len | reward | std |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0-199 | 1.279 | -1.691 | 1.294 | 33.87% | 743.8 | 3.54 | 0.627 |
| 200-399 | 0.356 | +0.189 | 1.550 | 7.39% | 970.7 | 13.60 | 0.529 |
| 400-749 | 0.800 | +0.117 | 1.437 | 4.85% | 975.6 | 15.94 | 0.522 |
| 750-999 | 1.781 | +0.799 | 1.027 | 6.30% | 964.0 | 17.86 | 0.520 |
| 1000-1499 | 4.144 | +0.287 | 0.741 | 11.27% | 933.1 | 17.39 | 0.544 |
| 1500-1999 | 4.785 | +0.081 | 0.711 | 11.43% | 939.7 | 17.51 | 0.569 |
| 2000-2499 | 5.007 | +0.047 | 0.729 | 10.17% | 946.7 | 17.74 | 0.584 |
| 2500-2999 | 5.160 | +0.042 | 0.714 | 9.20% | 952.8 | 18.05 | 0.601 |

### 해석

**0~199 — 초기 붕괴**: terrain slope가 약 `-1.69 / 100 iter`. 미학습 정책이 어려운 초기 terrain에서 실패하면서 curriculum이 빠르게 내려간다.

**200~749 — survival gait 형성**: terrain은 낮지만 episode length가 970~976 수준으로 회복되고 base-contact가 7.4% → 4.8% 수준으로 낮아진다.

**750~999 — 첫 locomotion breakthrough**: terrain slope가 `+0.799 / 100 iter`로 급격히 증가하고 XY 평균이 1.027까지 개선된다.

**1000~1499 — 고난도 진입**: 평균 terrain 4.14. base-contact가 약 11.3%로 증가하지만 XY 0.741을 유지한다.

**1500~1999 — 4.7~4.9 영역 적응**: terrain 상승 속도는 느려지지만 XY 평균 0.711, episode 약 940을 유지한다.

**2000~2499 — 평균 level 5 진입**: terrain 5.007, XY 0.729. base-contact는 오히려 10.17%로 감소한다.

**2500~2999 — mature high-terrain phase**: terrain 평균 5.160, XY 0.714, base-contact 9.20%, episode length 952.8. 높은 난이도에서 생존성이 다시 개선되는 구간이다.

후반 1000 iter에서 terrain 증가와 XY error의 단순 상관은 거의 0에 가까워진다. 이는 초기에는 'terrain 상승 = tracking 개선'이 강하게 연결되다가, mature phase에서는 **terrain이 더 올라가도 tracking이 약 0.7 부근에서 유지되는 plateau**로 들어갔다는 쪽에 가깝다.

또한 iter 1000 이후 running maximum 대비 가장 큰 terrain drawdown은 약 **0.114 level**에 불과했다. 즉 1K 이후 curriculum은 작은 진동은 있어도 구조적으로 무너지지 않았다.

---

# 6. 1K 종료와 3K 종료 비교

| 지표 | 1K iter 999 | 3K iter 2999 | 변화 |
|---|---:|---:|---:|
| Terrain | 2.8915 | **5.3393** | +2.4478 |
| XY error | 0.7050 | **0.6522** | -0.0528 |
| Yaw error | 0.4860 | **0.4172** | -0.0688 |
| Mean reward | 20.0100 | **18.7700** | -1.2400 |
| Episode length | 982.5200 | **959.3700** | -23.1500 |
| Base contact | 7.6600% | **8.9800%** | +1.3200% |
| Timeout | 92.3400% | **91.0200%** | -1.3200% |
| Action std | 0.5300 | **0.6100** | +0.0800 |

해석:

- terrain은 **+2.4478 level** 증가했다.
- XY error는 오히려 `0.7050 → 0.6522`로 소폭 개선했다.
- base-contact는 7.66% → 8.98%로 약간 늘었지만, terrain이 2.89 → 5.34로 오른 것을 고려하면 작은 비용이다.
- action std는 0.53 → 0.61로 증가했다. exploration이 죽은 것이 아니라 high-terrain 구간에서 다소 넓어졌다.

---

# 7. 최종값이 한 번의 우연한 spike인가?

아니다. 후반 평균이 이를 뒷받침한다.

| Window | Terrain | XY error | Reward | Episode length | Base contact | Std |
|---|---:|---:|---:|---:|---:|---:|
| Last 500 | 5.1599 | 0.7144 | 18.05 | 952.77 | 9.20% | 0.601 |
| Last 100 | 5.2510 | 0.7015 | 18.23 | 955.32 | 8.76% | 0.606 |
| Last 10 | 5.3219 | 0.6759 | 18.96 | 958.27 | 9.01% | 0.604 |
| Final | 5.3393 | 0.6522 | 18.77 | 959.37 | 8.98% | 0.610 |

last-100 기준으로도 terrain이 이미 **5.25**, 낙상(base contact)은 **8.76%**, XY는 **0.70**이다. 따라서 `5.3393`은 고립된 한 점이 아니라 **상승한 분포의 끝점**이다.

---

# 8. Tracking / survival 관점의 최고 지점

초기 iter 0의 XY error는 episode가 거의 시작도 못 하고 끝나기 때문에 의미가 없다. 학습이 충분히 진행된 구간에서 가장 낮은 XY error는:

```text
iter 2207
terrain       4.9417
XY error      0.4743
mean reward   21.40
episode len   978.17
base contact  10.50%
```

즉 terrain 약 4.94에서 XY **0.4743**까지 내려간 지점도 있다.

후반에는 terrain이 5.2 이상으로 올라가면서도:

- iter 2857: terrain 5.1944, XY 0.5729, base-contact 7.66%
- iter 2925: terrain 5.2304, XY 0.5615, reward 21.18, base-contact 8.41%
- iter 2977: terrain 5.2765, XY 0.5168

같은 강한 샘플이 반복된다.

---

# 9. Reward component가 보여주는 gait 변화

A1 후반으로 갈수록 움직임 관련 penalty의 절댓값이 커졌다. final 2999:

```text
track_lin_vel_xy_exp  +1.0749
track_ang_vel_z_exp   +0.5732
lin_vel_z_l2           -0.0490
ang_vel_xy_l2          -0.1876
dof_torques_l2         -0.0971
dof_acc_l2             -0.2140
action_rate_l2         -0.1251
```

이는 정책이 높은 terrain에서 더 많은 몸통/관절 운동과 action variation을 사용하고 있다는 정황과 맞는다. 동시에 episode length와 base-contact가 안정적이므로 단순한 '난폭한 움직임'으로만 끝난 것은 아니다.

다만 `track_lin_vel_xy_exp`의 weight 자체가 1.5로 바뀌었으므로 이 reward component의 절대값을 baseline과 직접 성능비로 비교하면 안 된다. 실제 추종 품질은 `error_vel_xy`가 더 직접적인 지표다.

---

# 10. Numerical stability: 성공했지만 반드시 주의할 부분

## 10.1 fatal divergence는 없음

3K의 **31개 checkpoint 전부**를 직접 열어 actor/critic tensor를 검사했다.

```text
actor NaN = 0
actor Inf = 0
critic NaN = 0
critic Inf = 0
std NaN = 0
std Inf = 0
std min > 0 for every checkpoint
```

즉 3K는 요청한 3000 iteration을 정상 완료했고 저장 checkpoint도 깨지지 않았다.

## 10.2 하지만 value loss는 heavy-tailed

전체 3K:

```text
value loss median   0.0265
value loss p95      0.5336
value loss p99      7.8971
value loss max      104.1677 @ iter 2912
```

iter 1000 이후 median은 약 0.0286으로 평상시는 매우 낮지만, 드물게 큰 spike가 반복된다.

| Iter | Value loss | Reward | Terrain | XY error |
|---:|---:|---:|---:|---:|
| 950 | **10.9995** | 17.90 | 2.416 | 0.824 |
| 1190 | **28.3564** | 19.02 | 4.229 | 0.639 |
| 1326 | **55.0765** | 18.33 | 4.428 | 0.825 |
| 1608 | **15.7912** | 17.82 | 4.645 | 0.668 |
| 1812 | **10.0323** | 14.91 | 4.906 | 0.724 |
| 2045 | **17.2521** | 17.73 | 4.956 | 0.681 |
| 2101 | **40.8803** | 17.81 | 4.966 | 0.823 |
| 2300 | **29.9222** | 19.73 | 5.030 | 0.667 |
| 2562 | **81.3573** | 17.46 | 5.078 | 0.806 |
| 2674 | **54.7537** | 18.37 | 5.141 | 0.730 |
| 2912 | **104.1677** | 18.52 | 5.211 | 0.725 |

최대 spike:

```text
iter 2912  value loss 104.1677
iter 2913  reward     -12.21
iter 2925  value loss 0.0299, reward 21.18
```

즉 iter 2912의 value-loss 104.17 직후 일시적인 reward 충격이 있었지만 곧 회복했고, terrain도 이후 계속 증가해 5.3393으로 종료했다.

**판정:** 현재 3K는 발산한 run이 아니다. 하지만 critic이 완전히 조용한 run도 아니다. 공식 5K에서는 `value_loss` 연속 증가와 NaN/Inf를 반드시 감시해야 한다.

공식 report의 `수치상 큰 이상 신호 없음`은 'fatal NaN/Inf/미완료가 없다'는 의미에서는 맞지만, **반복된 transient critic spike까지 표현해 주지는 않는다.**

---

# 11. Action std / checkpoint 내부 분석

| Checkpoint | mean std | min | max | actor NaN/Inf | critic NaN/Inf | LR |
|---|---:|---:|---:|---:|---:|---:|
| model_0 | 0.999 | 0.993 | 1.004 | 0/0 | 0/0 | 0.000296 |
| model_100 | 0.575 | 0.382 | 0.756 | 0/0 | 0/0 | 0.000444 |
| model_900 | 0.513 | 0.358 | 0.685 | 0/0 | 0/0 | 0.000132 |
| model_1000 | 0.531 | 0.368 | 0.733 | 0/0 | 0/0 | 0.000384 |
| model_1500 | 0.565 | 0.371 | 0.800 | 0/0 | 0/0 | 0.000256 |
| model_2000 | 0.562 | 0.377 | 0.756 | 0/0 | 0/0 | 0.000256 |
| model_2500 | 0.581 | 0.384 | 0.785 | 0/0 | 0/0 | 0.000256 |
| model_2900 | 0.586 | 0.382 | 0.752 | 0/0 | 0/0 | 0.000384 |
| model_2999 | 0.606 | 0.408 | 0.793 | 0/0 | 0/0 | 0.000114 |

흐름은:

```text
초기      std ≈ 1.00
100~900   ≈ 0.51~0.57
1K 이후   다시 서서히 증가
2999      mean 0.606 / min 0.408 / max 0.793
```

따라서 탐색이 0으로 collapse한 정책은 아니다. 반대로 1.0 부근으로 폭주한 것도 아니다. high-terrain 구간에서 탐색 폭이 다시 조금 넓어진 형태다.

---

# 12. model_best 선택: 정확하지만 final과 별도 비교 가치가 있음

3K official report:

```text
최고 reward 21.45 @ iter 2905
제출 선택 checkpoint: iter 2900
```

SHA256을 직접 대조하면:

```text
exported/model_best.pt
= checkpoints/model_2900.pt
= 1f2cc93aee18e9b772a1260bf56912cc297be1e4632a047445c32bf739a4e8c3
```

즉 finalize의 checkpoint 선택은 내부 규칙대로 정확히 동작했다.

### model_2900 인접 상태

```text
iter 2900  terrain 5.2029 / XY 0.6906 / base 9.35% / episode 946.60
iter 2905  terrain 5.2194 / XY 0.5545 / reward 21.45
```

### final

```text
iter 2999  terrain 5.3393
           XY      0.6522
           base    8.98%
           episode 959.37
           reward  18.77
```

`model_2999.pt`는 `model_best.pt`와 SHA가 다르며 별도 정책이다.

**중요:** training scalar는 stochastic batch summary이므로 이 숫자만으로 model_2999가 model_2900보다 실제 평가 점수가 높다고 단정할 수 없다. 하지만 final은 terrain/survival/tracking이 충분히 강하므로, 제출 전 동일 `play/eval` 조건으로 **model_2900 vs model_2999**를 비교할 가치가 높다.

---

# 13. 1K report 경고가 3K에서 어떻게 뒤집혔는가

1K official report는:

```text
start terrain 3.5
final terrain 2.89
→ 시작보다 낮으므로 경고
```

를 냈다. 이 규칙은 기계적으로는 맞지만, 이번 3K trajectory를 보면 1K 시점에 이를 '실패 확정'으로 쓰면 안 됐다는 것이 명확하다.

정책은:

```text
initial distribution 3.53
→ 0.17까지 실제 후퇴
→ 1K final 2.89
→ iter 1072에서 initial 3.53 재돌파
→ 3K final 5.34
```

즉 **초기 terrain collapse 자체보다 그 이후 회복 slope와 tracking 동반 개선이 더 중요한 진단 정보**다.

이 evidence는 G2/G3/G4 같은 실험을 100~200 iteration terrain 값만으로 너무 빨리 기각하면 위험하다는 강한 실증 사례다.

---

# 14. Video evidence 분석

## 14.1 lineage

video metadata:

```text
parent_run_id            20260913-144615-go2-a1-aggressive-tracklin150-lvz-m2-3k
source checkpoint SHA    1f2cc93aee18e9b772a1260bf56912cc297be1e4632a047445c32bf739a4e8c3
video SHA                deb0b7d548e572555de07ed4132bf54740b641a99efec87f47d704a9d53d43af
exit_code                0
status                   completed
validation               PASS
```

source checkpoint SHA는 3K train의 `model_best.pt = model_2900.pt`와 정확히 일치한다. 따라서 영상이 어느 모델에서 나온 것인지 cryptographic lineage가 분명하다.

## 14.2 MP4

직접 `ffprobe`로 확인:

```text
codec       H.264
resolution  1920 × 1080
fps         50
frames      999
duration    19.98 s
size        7,162,281 bytes
bitrate     ~2.87 Mb/s
```

## 14.3 video 실행 상태

- `exit_code=0`
- evidence validation PASS
- `play_video.mp4` fresh/non-empty PASS
- source-before/after hash 동일
- staged `model_best.pt`는 실행 후 원상 복구됨
- 이번 video console에는 `Traceback`/`AttributeError`가 없다.

GLFW/X-display, deprecated config, Hydra mesh primvar 등의 warning은 있으나 이번 video 생성 실패로 이어지지 않았다.

1s/4s/7s/10s/13s/16s/19s 프레임을 샘플링해 확인했을 때 로봇은 전 프레임에서 화면 안에 있고 upright 상태로 보이며 tracking camera도 정상적으로 따라간다. 다만 20초짜리 단일-env 영상은 정성 확인용이지 statistical evaluation은 아니다.

---

# 15. GPU / 실행 성능

| Run | wall time | transitions | 평균 FPS/steps/s | GPU util 평균 | VRAM 평균 | power 평균 | max temp |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1K train | 55.8 min | 98,304,000 | 29822 | 76.8% | 7.46 GiB | 215.7 W | 44°C |
| 3K train | 2.76 h | 294,912,000 | 29887 | 76.2% | 7.52 GiB | 212.7 W | 43°C |
| 3K video | 93.3 s | - | - | 15.0% | 6.98 GiB | 96.8 W | 32°C |

L40S 49,140 MiB 중 training VRAM은 약 7.5 GiB 수준이라 VRAM/thermal 병목 징후는 없다.

---

# 16. `issacsimz` logging/evidence 품질 평가

## 16.1 잘 된 부분

### A. Archive 무결성
각 evidence root에 `SHA256SUMS`가 있고 실제 검증이 전부 PASS했다.

### B. Checkpoint 보존
watcher가 source checkpoint를 **copy-only**로 보존하며 각 checkpoint의 bytes와 SHA256을 기록했다. 3K에서는 31개 checkpoint가 정확히 남아 있다.

### C. Source mutation 탐지
핵심 task source의 before/after hash가 모두 같고 `changed_during_run=false`다. 학습 도중 소스 변경 오염을 배제하는 데 매우 유용하다.

### D. Native provenance
TensorBoard event, agent/env params, IsaacLab git commit/status가 archive에 같이 들어 있어 재현성 검토가 가능하다.

### E. Delta collection
3K 시작 시 `exported/`에 예전 1K video/policy 파일이 이미 있었지만 provenance가 이를 `UNCHANGED`로 구분했고, 실제 3K collected 영역에는 새/수정된 final artifacts만 들어갔다. stale 파일을 새 결과로 오인하지 않게 해 준다.

### F. Train → video lineage
video evidence가 `parent_run_id`, source checkpoint 경로와 SHA, generated video SHA를 기록한다. 이번 경우 parent/model SHA 연결이 정확히 검증된다.

### G. GPU telemetry
학습 중 GPU util, VRAM, power, temperature를 별도 CSV로 기록해 환경 성능 문제와 학습 문제를 분리할 수 있다.

## 16.2 가볍게 개선할 수 있는 부분

### 1. wrapper runtime과 child runtime을 구분해 기록

`system/runtime.txt`는 1K에서 Python 3.12.14, 3K/video에서 3.10.12를 기록한다. 반면 실제 training/play console은 `/home/shadeform/IsaacLab/_isaac_sim/python.sh`를 사용하고 `python3.11/site-packages/rsl_rl`을 로드한다.

따라서 현재 `runtime.txt`의 `python=`만 보면 실제 RL child interpreter로 오해할 수 있다. 무겁게 만들 필요 없이:

```text
wrapper_python=
child_python_path=
child_python_version=
```

세 줄만 분리 기록하면 provenance가 훨씬 명확해진다.

### 2. TensorBoard scalar summary를 작은 CSV/JSON으로 자동 추출

현재 event 파일은 완전하지만 분석하려면 parser가 필요하다. `terrain`, `XY`, `base_contact`, `reward`, `std`, `value_loss` 정도만 수백 KB 이하 CSV로 같이 넣으면 분석 UX가 크게 좋아진다.

### 3. transient numerical instability summary

현재 validation은 fatal NaN/Inf에는 강하지만 `value_loss=104` 같은 일시 spike를 별도 경고하지 않는다. 다음 정도만 metadata에 추가해도 충분하다:

```text
max_value_loss
value_loss_ge_1_count
value_loss_ge_10_count
nan_or_inf_seen
```

### 4. selected checkpoint를 metadata에 명시

현재는 report/hash 비교로 model_best=2900을 알아낼 수 있다. metadata에 `selected_checkpoint=model_2900.pt`, `best_reward_iter=2905` 정도를 넣으면 사람이 훨씬 빨리 읽을 수 있다.

이 네 가지는 모두 **작은 sidecar 개선**이고 기존 canonical 구조를 무겁게 바꿀 필요가 없다.

---

# 17. Evidence 품질 판정

이번 세 archive만으로 다음 질문에 답할 수 있다.

| 질문 | 답변 가능 여부 | 근거 |
|---|---|---|
| 실제 어떤 command로 돌렸나 | 가능 | `command.txt`, metadata |
| 어떤 reward/config였나 | 가능 | env/agent YAML, reward source |
| 소스가 중간에 바뀌었나 | 가능 | source identity before/after hash |
| 1K와 3K가 같은 설정인가 | 매우 강하게 가능 | config diff + source hash |
| 첫 1K가 재현됐나 | 매우 강하게 가능 | scalar exact match + checkpoint SHA match |
| 학습이 정상 종료됐나 | 가능 | exit/status/validation |
| checkpoint가 깨졌나 | 가능 | 직접 tensor 검사 |
| terrain/XY/낙상 trajectory | 가능 | console + TensorBoard 3000 points |
| GPU가 문제였나 | 상당 부분 가능 | telemetry |
| model_best가 어느 checkpoint인가 | 가능 | SHA match |
| 영상이 어느 model에서 나왔나 | 매우 강하게 가능 | parent + source SHA + video manifest |
| 실제 대회 점수가 얼마인가 | 불가능 | 공식 evaluator 결과 없음 |
| 20초 영상이 모든 terrain generalization을 증명하나 | 불가능 | single-env qualitative video |

전체적으로 `issacsimz` evidence는 **대회 실험 추적용으로 상당히 높은 수준**이다. 특히 '결과만 남긴 것'이 아니라 실행/소스/config/checkpoint/환경/video lineage까지 이어진 점이 강하다.

---

# 18. 공식 5K 진행 판단

이 evidence만 놓고 보면 **공식 서버 fresh 5K를 진행하는 판단은 타당하다.**

이유:

- 3K가 중간 실패가 아니라 정상 완료
- final terrain 5.3393
- last-500 terrain 5.1599
- last-500 XY 0.714
- last-500 base-contact 9.20%
- last-500 episode length 952.8
- 1K→3K 재현성이 매우 강함
- 3K 후반에도 terrain slope가 아직 양수
- checkpoint NaN/Inf 없음

다만 5K에서 가장 중요한 위험은 **critic transient instability**다. A1을 바꿀 이유는 없지만:

```text
reward는 그대로
fresh 5K
100-iter checkpoint 유지
value loss 연속 폭증 감시
model_best와 final 모두 보존
```

가 좋다.

## 공식 5K에서 볼 기준

3K보다 terrain 숫자가 무조건 커야만 성공인 것은 아니다. high-terrain 구간에서 안정적으로 유지되는 것도 중요하다.

좋은 결과의 형태:

```text
terrain        5.x 유지 또는 5.5~6 방향 진행
XY error       대체로 < 1.0
episode length 900+
base contact   대체로 < 15%
std            finite
value loss     spike가 있더라도 회복
NaN/Inf        없음
```

반대로 중단/주의 신호:

```text
value loss가 수십→수백→계속 증가
NaN/Inf
terrain 지속 하락
base-contact 20%+ 장기 고착
episode length 대폭 하락
XY 1.5+ 장기 고착
```

---

# 19. 현재 제출 후보 관점

현재 가장 합리적인 후보 관리 방식은:

1. **공식 fresh 5K로 A1 자체를 재검증**한다.
2. 5K 종료 후 official `model_best.pt`와 final checkpoint를 모두 보존한다.
3. 3K에서도 `model_2900`과 `model_2999`가 서로 장점이 있으므로, 최종 제출 단계에서는 scalar best만 자동 신뢰하지 않고 동일 평가/영상으로 비교한다.
4. A1이 official 5K에서도 강하면 그때 `track_lin 1.5 only`, `lin_vel_z -2 only` ablation은 연구적 가치가 있지만, 대회 효율 관점에서는 제출 후보 확정 뒤로 미뤄도 된다.

---

# 20. 최종 판정

### A1 1K

**성공적인 screening.** 초반 curriculum collapse를 회복하고 2.89까지 올라갔으며, 이후 fresh 3K가 첫 1K를 동일하게 재현했다.

### A1 fresh 3K

**강한 성공.**

```text
final terrain       5.3393
final XY error      0.6522
final yaw error     0.4172
final episode len   959.37
final base contact  8.98%
final timeout       91.02%
final reward        18.77
best reward         21.45 @ 2905
final action std    0.61
total transitions   294,912,000
```

학습의 질을 가장 잘 설명하는 문장은 다음이다.

> **A1은 초반 terrain 0.17까지 실제로 내려간 뒤 생존 gait를 만들고, 1K 이후에도 tracking을 유지한 채 terrain 평균 5.34까지 재등반했다. 후반 500 iteration에서는 terrain이 5.16 평균인데도 낙상 약 9.2%, episode 약 953, XY 약 0.71을 유지했다.**

단 하나의 주요 경고는 critic value-loss spike다. fatal divergence는 아니었지만 5K 장기 run에서는 monitoring 대상이다.

### 3K video

**정상 PASS.** parent/model/video lineage가 해시로 연결되고, 1080p 50 FPS 20초 영상이 정상 생성됐다.

### 다음 단계

**공식 서버에서 A1 reward를 그대로 유지한 fresh 5K 검증을 권장한다.**

---

# Appendix A. 핵심 milestone

| Iter | Terrain | XY | Reward | Episode | Base contact | Std | Value loss |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 3.5284 | 0.0223 | -0.63 | 13.0 | 0.00% | 1.00 | 0.1182 |
| 50 | 1.9706 | 1.2738 | -1.64 | 706.1 | 55.09% | 0.64 | 0.0123 |
| 100 | 0.9487 | 1.3267 | 5.26 | 791.6 | 44.18% | 0.57 | 0.0196 |
| 193 | 0.1666 | 1.7266 | 9.46 | 933.2 | 18.66% | 0.56 | 0.0145 |
| 289 | 0.3336 | 1.6656 | 13.57 | 973.6 | 5.28% | 0.53 | 0.0180 |
| 391 | 0.5444 | 1.4886 | 14.86 | 979.2 | 3.89% | 0.52 | 0.0182 |
| 500 | 0.7188 | 1.5887 | 16.09 | 992.3 | 4.10% | 0.52 | 0.0178 |
| 751 | 1.0026 | 1.1843 | 16.87 | 950.4 | 6.31% | 0.52 | 0.0261 |
| 841 | 1.4313 | 0.9497 | 18.41 | 950.7 | 5.65% | 0.51 | 0.0202 |
| 932 | 2.2405 | 0.6415 | 20.95 | 968.5 | 6.51% | 0.51 | 0.0214 |
| 999 | 2.8915 | 0.7050 | 20.01 | 982.5 | 7.66% | 0.53 | 0.0235 |
| 1072 | 3.5287 | 0.7346 | 19.26 | 967.6 | 9.38% | 0.54 | 0.0258 |
| 1140 | 4.0008 | 0.6806 | 18.00 | 887.9 | 11.54% | 0.52 | 0.0216 |
| 1291 | 4.4175 | 0.7556 | 17.76 | 918.3 | 11.54% | 0.54 | 0.0253 |
| 1405 | 4.4987 | 0.7258 | 16.71 | 959.8 | 11.38% | 0.57 | 0.0285 |
| 1513 | 4.5731 | 0.6528 | 18.75 | 963.7 | 12.44% | 0.56 | 0.0260 |
| 1573 | 4.5788 | 0.7306 | 17.51 | 943.5 | 12.25% | 0.56 | 0.1319 |
| 1699 | 4.7804 | 0.6011 | 19.37 | 931.3 | 11.65% | 0.56 | 0.0300 |
| 1843 | 4.8611 | 0.5981 | 18.57 | 945.8 | 11.14% | 0.58 | 0.0273 |
| 2000 | 4.9047 | 0.7837 | 17.49 | 961.7 | 11.30% | 0.56 | 0.0250 |
| 2207 | 4.9417 | 0.4743 | 21.40 | 978.2 | 10.50% | 0.59 | 0.0297 |
| 2253 | 5.0002 | 0.6659 | 19.39 | 956.3 | 9.35% | 0.57 | 0.0541 |
| 2257 | 5.0226 | 0.5871 | 20.00 | 972.4 | 9.24% | 0.58 | 0.0301 |
| 2500 | 5.0983 | 0.8530 | 20.06 | 965.4 | 7.92% | 0.58 | 0.0320 |
| 2779 | 5.2000 | 0.7260 | 18.42 | 958.4 | 8.74% | 0.61 | 0.0273 |
| 2857 | 5.1944 | 0.5729 | 20.21 | 964.8 | 7.66% | 0.59 | 0.0245 |
| 2900 | 5.2029 | 0.6906 | 18.36 | 946.6 | 9.35% | 0.59 | 0.0236 |
| 2905 | 5.2194 | 0.5545 | 21.45 | 973.9 | 9.27% | 0.59 | 0.0962 |
| 2912 | 5.2108 | 0.7253 | 18.52 | 938.9 | 9.05% | 0.60 | 104.1677 |
| 2925 | 5.2304 | 0.5615 | 21.18 | 976.5 | 8.41% | 0.61 | 0.0299 |
| 2977 | 5.2765 | 0.5168 | 19.00 | 941.0 | 8.76% | 0.60 | 0.2393 |
| 2985 | 5.3023 | 0.7028 | 17.69 | 939.5 | 8.73% | 0.61 | 0.0253 |
| 2999 | 5.3393 | 0.6522 | 18.77 | 959.4 | 8.98% | 0.61 | 0.0868 |

---

# Appendix B. Artifact 구조 요약

## 1K train

```text
11 checkpoints
TensorBoard event
agent.yaml / env.yaml
IsaacLab git identity
source identity + reward snapshot
GPU before/during/after
model_best.pt / env.yaml / report.html
metadata / validation / provenance / SHA256SUMS
```

## 3K train

```text
31 checkpoints
TensorBoard event (3000 scalar steps)
agent.yaml / env.yaml
IsaacLab git identity
source identity + reward snapshot
GPU before/during/after
model_best.pt / env.yaml / report.html
metadata / validation / provenance / SHA256SUMS
```

## 3K video

```text
play_video.mp4
policy.pt / policy.onnx
parent_run_id
source checkpoint SHA256
video SHA256
source identity
GPU telemetry
metadata / validation / provenance / video_manifest / SHA256SUMS
```

---

# Appendix C. 분석상 한계

- `Curriculum/terrain_levels`는 4096개 env의 평균이며 '로봇이 확정적으로 정복한 단일 최대 level'과 동일하지 않다.
- training scalar는 stochastic rollout batch의 통계다. checkpoint 간 최종 순위는 동일 evaluator/play 조건으로 확인해야 한다.
- 20초 single-env video는 qualitative evidence이지 낙상률/terrain generalization의 통계적 검증이 아니다.
- A1은 두 reward를 동시에 변경했기 때문에 각 변경의 독립적 causal contribution은 이 데이터만으로 분리할 수 없다.
- 공식 대회 evaluator 결과는 archive에 없으므로 실제 제출 점수는 이 보고서에서 추정하지 않는다.
