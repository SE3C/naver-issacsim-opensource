# Go2 개인 L40S baseline 12K 시도 심층 분석
## 2026-08-29~30 run: 0→9535 전체 TensorBoard·콘솔·checkpoint 재분석

> **분류:** 개인 NVIDIA/Brev L40S 검증 실행. 공식 서버 학습·공식 제출 점수가 아니다.  
> **분석 원본:** `go2-recovery-20260830_125132_KST.tar.gz`  
> **핵심 run:** `training/quadruped/logs/rsl_rl/quadruped/2026-08-29_15-54-03/`  
> **요청:** 12,000 iterations / **실제:** 0~9535 기록 후 수치 발산으로 중단  
> **분석 기준:** raw TensorBoard event와 full console을 우선하고, 자동 `report.html`의 문구는 교차검증한다.

---

## 1. 결론 요약

이 run은 단순히 “9.5K에서 갑자기 망한 학습”이 아니다. 전체 9,536 iteration을 다시 읽으면 세 가지가 동시에 보인다.

**첫째, 장기 학습의 성능 이득은 실제로 컸다.** 4.5K 부근과 9.5K 부근의 100-iteration 평균을 비교하면 terrain은 `0.921 → 5.800`, XY 속도 오차는 `1.490 → 0.701`로 약 **53% 감소**했다. base-contact 종료율은 약 `1.92% → 1.72%`로 낮은 수준을 유지했고 episode length도 거의 그대로였다. 따라서 이 Go2 baseline에서 “5K 이후 학습은 의미가 없었다”는 결론은 틀리다. 특히 **5.5K~7K 사이 terrain curriculum 상승이 가장 강했고, 8K~9K에도 XY tracking 개선이 계속됐다.**

**둘째, 안정적인 정책 성능과 optimizer/critic의 수치 안정성은 별개였다.** 정책 행동에 가까운 지표는 9K 이후에도 좋아졌지만, `Loss/value`의 간헐적 폭주는 약 7.7K부터 나타나기 시작했고 8K 이후 빈도와 크기가 증가했다. 최종 붕괴 전에도 `8068: 11.68`, `8175: 21.86`, `8779: 25.20`, `9249: 54.87`, `9413: 303.34` 같은 critic loss burst가 있었고 대부분 일시 회복했다. 따라서 **9512가 최초 이상은 아니다.** 최종 붕괴는 그동안 반복되던 critic 불안정이 더 이상 회복되지 않은 마지막 사건으로 보는 것이 raw log에 가장 잘 맞는다.

**셋째, 최종 예외의 `std >= 0` 오류를 최초 원인으로 볼 근거는 없다.** 보존된 `model_9500.pt`의 12개 action std는 모두 양수(`0.300~0.593`)이고 actor/critic/optimizer tensor가 모두 finite다. raw log에서는 value loss가 먼저 `2.34 → 103 → 52,437 → 1.04e6`으로 폭주하고, 이후 재발산해 `inf → nan`이 된 뒤 `normal expects all elements of std >= 0.0`가 발생한다. 다만 실패 직전 checkpoint가 없으므로 **9535 이후 실제 어느 std 차원이 음수가 되었는지는 확인할 수 없다.**

실전적으로는 **Go2에서 1K/3K는 장기 terrain 성능을 판단하기 너무 이르다.** 이 run은 100-iteration 평균 terrain이 1.0에 도달한 시점이 약 4744, 3.0은 6084, 5.0은 7012였다. 따라서 1K는 catastrophic failure·기본 gait·standing 같은 초기 screening에는 쓸 수 있지만, 험지/계단 계열 reward의 최종 효과 판정에는 부족하다.

또 하나의 중요한 provenance 문제가 확인됐다. archive의 현재 `exported/model_best.pt`는 실제 `model_9500.pt`와 동일하지만, **`exported/policy.pt`의 actor weight는 5K 선별본인 `model_4500.pt`와 bit-for-bit 동일하고 `model_9500.pt`와는 다르다.** 따라서 이 archive의 `policy.pt`를 9.5K 정책이라고 사용하면 안 된다. 9.5K 후보를 평가하려면 `model_9500.pt`에서 policy/video를 새로 export해야 한다.

---

## 2. 원본과 무결성

| 항목 | 파일 | SHA-256 |
|---|---|---|
| recovery archive | go2-recovery-20260830_125132_KST.tar.gz | c3bea262eb45d5f46357ce97049a0ede9f2f7eeb11008d4b20cef1fd1a33106b |
| TensorBoard event | events.out.tfevents.1788018859.brev-vv1fhdfgk.15311.0 | 12377469daaba5739989c3f434eb7c88ad76acb30fbaac0a64435b1bab12e6c1 |
| console | go2-12k.log | 006dcccde340bf17c05e020bf44d5ab0b7f20292d8e0af6c5128888f1fcd7588 |
| 5K selected checkpoint | best_through_5k/model_best.pt | 7ec9542381b3d320009c23f9681dfd281dc022fc45998c9f6c9b7c9d020ef974 |
| 9.5K checkpoint | model_9500.pt | a7b65db49f0c6207e488ec707c3d11b2218cd75beef479503b441f44199637df |
| final exported model_best | exported/model_best.pt | a7b65db49f0c6207e488ec707c3d11b2218cd75beef479503b441f44199637df |
| stale exported policy | exported/policy.pt | 67379f85bbddb52a18bb99db3c70cc32e4d4468c929bc39bf5c998b41554f761 |

외부 recovery archive의 `MANIFEST.sha256`을 실제로 검증하면 README, console logs, scripts, environment, `worktree.tar.gz`는 모두 정상이다. 단, `MANIFEST.sha256`이 **자기 자신을 빈 파일 SHA-256으로 기록**해 자기 항목 하나만 FAIL한다. 이는 당시 manifest 생성 순서의 결함으로 보이며, 나머지 파일 손상 증거는 없다.

TensorBoard event에는 **27개 scalar tag가 step 0~9535에 9,536점씩** 존재한다. 핵심 학습곡선은 누락 없이 연속적이다.

---

## 3. 실행 조건

- Task: `Quadruped-v0`
- seed: `42`
- environments: `4096`
- rollout: `24 steps/env/iteration`
- iteration당 transition: `98,304`
- 요청 iterations: `12,000`
- 실제 기록: `9,536` iterations (`0~9535`)
- 실제 누적 transition: `937,426,944`
- headless
- episode limit: `20 s`
- action dimension: `12`
- observation dimension: `235`
- command resampling: `10 s`
- standing command 비율: `2%`
- terrain curriculum: enabled
- terrain generator seed: `null`
- checkpoint interval: `100`
- PPO: 5 epochs, 4 mini-batches, adaptive LR, initial LR `1e-3`, desired KL `0.01`
- Isaac Sim: `5.1.0-rc.19+release.26219.9c81211b.gl`
- Isaac Lab commit: `3e73d6dd79080fd7632488c061052a6edd52e230`
- RSL-RL: `5.0.1`
- GPU: NVIDIA L40S 46 GB
- OS: Ubuntu 22.04.5

학생 reward 파일은 baseline 값 그대로였다.

| reward | 적용값 |
|---|---:|
| `track_lin_vel_xy_exp` | +1.0 |
| `feet_air_time` | +0.01 |
| `lin_vel_z_l2` | -3.0 |
| `ang_vel_xy_l2` | -0.08 |
| `action_rate_l2` | -0.01 |

실제 Reward Manager에서는 기본 항목까지 포함해 `track_ang_vel_z_exp=0.75`, `dof_torques_l2=-0.0002`, `dof_acc_l2=-2.5e-7` 등이 활성화됐고, `flat_orientation_l2`와 `dof_pos_limits`는 weight `0.0`이었다.

---

## 4. 전체 학습 곡선: 100-iteration trailing 평균

단일 iteration은 command sampling과 episode reset에 따라 흔들리므로, 아래 표는 각 지점 직전 **100 iterations 평균**을 기본 비교값으로 사용한다.

| 누적 iter | L40S 경과 | reward(100) | terrain(100) | XY err(100) | yaw err(100) | base-contact %(100) | episode len(100) | std(100) | value p95(100) | value max(100) |
|---|---|---|---|---|---|---|---|---|---|---|
| 1000 | 01:16:39 | 10.300 | 0.000 | 1.438 | 0.253 | 23.27 | 787.6 | 0.444 | 0.01406 | 0.01545 |
| 2000 | 02:31:40 | 11.762 | 0.000 | 1.708 | 0.313 | 11.46 | 937.8 | 0.447 | 0.009808 | 0.01087 |
| 3000 | 03:40:13 | 12.591 | 0.041 | 1.693 | 0.333 | 6.10 | 975.4 | 0.451 | 0.01009 | 0.01152 |
| 4000 | 04:48:46 | 14.058 | 0.693 | 1.541 | 0.299 | 3.72 | 986.7 | 0.481 | 0.0118 | 0.01274 |
| 4500 | 05:22:36 | 14.828 | 0.921 | 1.490 | 0.283 | 1.92 | 993.2 | 0.480 | 0.0129 | 0.01347 |
| 5000 | 05:56:28 | 15.045 | 1.160 | 1.453 | 0.275 | 1.81 | 992.9 | 0.490 | 0.01266 | 0.01395 |
| 6000 | 07:04:29 | 16.196 | 2.700 | 1.301 | 0.275 | 1.82 | 991.6 | 0.469 | 0.01439 | 0.01508 |
| 7000 | 08:13:49 | 16.529 | 4.991 | 1.052 | 0.302 | 4.08 | 982.5 | 0.475 | 0.01696 | 0.07779 |
| 8000 | 09:23:43 | 17.029 | 5.409 | 0.941 | 0.300 | 2.87 | 987.7 | 0.480 | 0.0323 | 0.5823 |
| 9000 | 10:33:56 | 17.758 | 5.692 | 0.754 | 0.306 | 2.36 | 987.9 | 0.484 | 0.05033 | 0.7152 |
| 9500 | 11:21:51 | 17.893 | 5.800 | 0.701 | 0.306 | 1.72 | 992.3 | 0.484 | 1.84 | 303.3 |

### 해석

### 0~1.5K: 초기 curriculum 붕괴와 생존 악화

환경은 초기 terrain level을 여러 단계에 배치하지만, 정책이 준비되지 않은 상태에서 curriculum이 빠르게 낮아졌다. terrain 평균은 약 500 iteration 무렵부터 0에 붙었고 1K~1.5K에도 0이었다. 100-iteration 평균 base-contact는 약 1.4K 부근에서 **29.5%**까지 올라가 이 run의 가장 불안정한 초기 구간을 만들었다.

따라서 1K 결과만 보면 이 정책은 “험지에서 어떻게 학습될 정책인지”를 거의 보여주지 못한다. 이 시점은 주로 기본 생존·명령추종 형성 과정이다.

### 1.5K~3K: 생존 회복, terrain은 아직 거의 0

2K 이후 base-contact가 빠르게 내려가고 episode length가 900 후반으로 회복됐다. 하지만 terrain은 여전히 0에 가깝다. 3K 시점 100-iteration 평균 terrain도 `0.041`이다.

즉 **3K screening은 기본 gait/생존 방향성에는 쓸 수 있지만 terrain reward의 장기 성능을 판정하기에는 이 run 기준 너무 이르다.**

### 3K~5K: curriculum 재상승 시작

terrain 평균은 약 3.1K 이후 다시 의미 있게 상승하기 시작했고 4.5K에서 약 `0.92`, 5K에서 `1.16`까지 올라갔다. 동시에 fall/base-contact는 약 2%까지 내려왔다.

5K 선별본은 꽤 안정적이지만, 아직 curriculum의 중·고난도 구간까지 올라간 상태는 아니다.

### 5K~7K: 가장 큰 terrain 성장 구간

이 run에서 가장 중요한 구간이다.

- 5K: terrain `1.16`
- 6K: terrain `2.70`
- 7K: terrain `4.99`

XY error도 `1.45 → 1.30 → 1.05`로 계속 좋아졌다. 5K 이후 2K를 더 학습한 효과가 매우 컸다. 따라서 **이 baseline에서 5K를 최종 수렴점으로 취급할 근거는 없다.**

### 7K~9K: 고난도 terrain 정착 + linear tracking 개선

terrain은 `4.99 → 5.41 → 5.69`, XY error는 `1.05 → 0.94 → 0.75`로 개선됐다. 이 시기의 marginal terrain gain은 5~7K보다 작지만, linear tracking은 여전히 눈에 띄게 좋아진다.

반면 critic value loss의 tail이 두꺼워지기 시작한다. 7K까지는 100-iteration value-loss max가 작았지만 8K 구간부터 간헐적 큰 spike가 등장한다.

### 9K~9.5K: 성능은 조금 더 좋아지지만 critic 위험이 크게 증가

9K→9.5K에서 terrain은 `5.692 → 5.800`, XY error는 `0.754 → 0.701`, base-contact는 `2.36% → 1.72%`로 추가 개선된다. 즉 성능 관점에서 완전히 plateau라고 하기는 어렵다.

하지만 같은 100-iteration 구간에서 value-loss p95는 `0.050` 수준에서 **1 이상**으로 커지고, 최대는 `303.34`까지 튄다. 이 구간은 성능 개선과 수치 위험 증가가 동시에 나타나는 명확한 trade-off다.

---

## 5. terrain progression의 실제 시점

초기 random terrain 배치를 제외하고 step 500 이후부터 100-iteration 평균 terrain이 다시 올라간 시점을 계산했다.

| 100-iter 평균 terrain 임계값 | 최초 도달 step |
|---|---|
| 0.1 | 3114 |
| 0.5 | 3727 |
| 1 | 4744 |
| 2 | 5824 |
| 3 | 6084 |
| 4 | 6393 |
| 5 | 7012 |
| 5.5 | 8434 |
| 5.8 | 9313 |

이 표가 의미하는 바는 단순하다.

- 1K: terrain 성능 평가용으로는 너무 이르다.
- 3K: terrain curriculum이 이제 막 다시 움직이기 시작한다.
- 약 4.7K: 평균 terrain 1 수준.
- 약 6.1K: 평균 terrain 3.
- 약 7.0K: 평균 terrain 5.
- 약 9.3K: 평균 terrain 5.8.

**Go2의 험지/계단/terrain-oriented reward 실험을 1K 하나만 보고 탈락시키는 것은 위험하다.** 다만 1K는 넘어짐, 제자리 붕괴, 과도한 bouncing 같은 catastrophic behavior를 걸러내는 screening으로는 여전히 유효하다.

---

## 6. 5K 후보와 9.5K 후보 비교

5K용으로 실제 저장된 후보는 `selection.txt` 기준 reward peak step `4509`에 가장 가까운 `model_4500.pt`다. 9.5K 후보는 `model_9500.pt`다.

| 후보 | step | reward | terrain | XY err | yaw err | base-contact % | episode len | mean std | value loss |
|---|---|---|---|---|---|---|---|---|---|
| 5K 보존 후보 | 4509 | 16.574 | 0.918 | 1.168 | 0.279 | 1.60 | 1000.0 | 0.482 | 0.01258 |
| 9.5K 보존 checkpoint | 9500 | 18.034 | 5.825 | 0.719 | 0.311 | 1.91 | 981.5 | 0.477 | 0.01428 |

단일 step은 노이즈가 있으므로 100-iteration 평균으로 보면 차이가 더 명확하다.

- reward: `14.828 → 17.893` (**+20.7%**)
- terrain: `0.921 → 5.800`
- XY error: `1.490 → 0.701` (**-53.0%**)
- yaw error: `0.283 → 0.306` (**약 +8.1%, 개선되지 않음**)
- base-contact: `1.92% → 1.72%`
- episode length: `993.2 → 992.3`, 사실상 유지
- mean std: `0.480 → 0.484`, 사실상 유지

따라서 장기 학습의 핵심 이득은 **linear tracking + terrain curriculum**이다. 반대로 yaw error는 장기 학습으로 좋아졌다고 말할 수 없다.

이는 “더 오래 돌리면 모든 축이 같이 좋아진다”는 그림이 아니다. Go2 baseline은 5K 이후에도 많이 성장했지만, 그 성장의 방향은 주로 **전방위 linear tracking과 고난도 terrain 적응**이었다.

---

## 7. reward term 변화: 성능 향상과 제어비용의 trade-off

4.4K~4.5K와 9.4K~9.5K의 100-step 평균 reward term을 비교했다.

| reward term | 4400~4499 평균 | 9400~9499 평균 | Δ |
|---|---|---|---|
| track_lin_vel_xy_exp | 0.41425 | 0.73570 | +0.32145 |
| track_ang_vel_z_exp | 0.66576 | 0.65384 | -0.01191 |
| lin_vel_z_l2 | -0.02054 | -0.04681 | -0.02627 |
| ang_vel_xy_l2 | -0.09414 | -0.12878 | -0.03464 |
| dof_torques_l2 | -0.08729 | -0.09088 | -0.00360 |
| dof_acc_l2 | -0.06671 | -0.14187 | -0.07516 |
| action_rate_l2 | -0.06969 | -0.08791 | -0.01822 |
| feet_air_time | -0.00182 | -0.00143 | +0.00039 |
| flat_orientation_l2 | 0.00000 | 0.00000 | +0.00000 |
| dof_pos_limits | 0.00000 | 0.00000 | +0.00000 |

가장 큰 변화는 `track_lin_vel_xy_exp`가 `0.414 → 0.736`으로 크게 증가한 점이다. 반면 angular tracking reward는 거의 변하지 않았다.

동시에 `lin_vel_z_l2`, `ang_vel_xy_l2`, `dof_acc_l2`, `action_rate_l2` 같은 penalty contribution은 더 음수가 됐다. 이는 후반 정책이 더 어려운 terrain에서 더 많은/급한 동작을 사용했거나, policy 자체가 더 공격적으로 움직였거나, 둘이 섞였을 가능성이 있다. **현재 event만으로 어느 쪽이 원인인지는 분리할 수 없다.**

따라서 후반의 높은 총 reward를 “모든 움직임이 더 부드럽고 안정적으로 변했다”고 해석하면 안 된다. 정확한 결론은:

> 더 어려운 terrain까지 올라가면서 linear tracking 보상은 크게 좋아졌고, 그 과정에서 일부 동작·가속·자세 penalty 비용도 커졌다.

---

## 8. value-loss 불안정은 9512보다 훨씬 일찍 시작됐다

`Loss/value > 1`인 burst를 인접 step 단위로 묶으면 다음과 같다.

| 구간 | `value loss > 1` 횟수 | 구간 최대 | 최대 step | 그때 reward | 그때 LR |
|---|---|---|---|---|---|
| 7717 | 1 | 1.289 | 7717 | 16.700 | 1e-05 |
| 8068 | 1 | 11.68 | 8068 | 17.615 | 1.5e-05 |
| 8173~8176 | 3 | 21.86 | 8175 | 17.175 | 1e-05 |
| 8318~8320 | 2 | 9.095 | 8318 | 16.477 | 1e-05 |
| 8554~8555 | 2 | 3.213 | 8554 | 19.143 | 1e-05 |
| 8777~8780 | 4 | 25.2 | 8779 | 17.576 | 1.5e-05 |
| 9073~9077 | 3 | 6.564 | 9077 | 17.626 | 2.25e-05 |
| 9100~9102 | 3 | 14.51 | 9101 | 17.079 | 1e-05 |
| 9149~9150 | 2 | 15.75 | 9150 | 6.732 | 5.06e-05 |
| 9244~9249 | 5 | 54.87 | 9249 | 16.394 | 1e-05 |
| 9258 | 1 | 2.292 | 9258 | 18.514 | 1e-05 |
| 9292 | 1 | 1.675 | 9292 | 17.783 | 1.5e-05 |
| 9377 | 1 | 1.072 | 9377 | 18.282 | 1e-05 |
| 9400~9403 | 3 | 18.07 | 9403 | 17.200 | 1e-05 |
| 9411~9414 | 4 | 303.3 | 9413 | 15.417 | 1e-05 |

핵심 변화는 다음 순서다.

1. **7717:** 첫 `value loss > 1`
2. **8068:** 첫 `> 10`
3. 8K~9K 사이: 간헐적 burst가 반복되지만 다시 정상대로 회복
4. **9249:** 54.87
5. **9413:** 303.34 — 최종 붕괴 약 100 iteration 전 이미 매우 큰 critic spike
6. 9505~9506: `0.0956 → 0.8082`의 작은 전조 후 다시 회복
7. 9512: `2.34`
8. 9513: `103.24`
9. 9514: `52,437`
10. 9515: `1.04e6`
11. 9516~9520: 다시 `~0.012~0.016`으로 일시 회복
12. 9524: `0.239`
13. 9525: `46.0`
14. 9526: `5.42e4`
15. 9527: `5.33e8`
16. 9528: `2.24e13`
17. 9529: `3.50e18`
18. 9530: `7.77e23`
19. 9531: `2.51e29`
20. 9532~9534: `inf`
21. 9535: `nan`
22. 그 직후 `RuntimeError: normal expects all elements of std >= 0.0`

즉 최종 실패에는 **두 번의 폭발**이 있다. 9512~9515 첫 폭발 후 잠시 회복했고, 9524부터 두 번째 폭발이 시작되어 이번에는 회복하지 못했다.

특히 9515에는 다른 reward term은 대체로 정상 범위인데 `Episode_Reward/action_rate_l2`만 약 `-105.675`로 극단적으로 깨지고 `Train/mean_reward=-2008.65`가 된다. 이 시점은 critic loss 폭주가 실제 action dynamics/reward에도 영향을 준 순간으로 볼 수 있다. 단, 어느 쪽이 최초 trigger인지는 raw scalar의 순서만으로 확정할 수 없다.

---

## 9. adaptive learning rate가 불안정을 완전히 막지는 못했다

PPO 설정은 `learning_rate=1e-3`, adaptive schedule, `desired_kl=0.01`이다. TensorBoard의 `Loss/learning_rate`는 후반 spike 구간에서 반복적으로 최저 수준인 약 `1e-5`까지 내려간다.

후반 500-iteration 구간에서 LR이 `~1e-5`에 붙은 비율은 대략:

- 7.0~7.5K: 2.6%
- 7.5~8.0K: 4.0%
- 8.0~8.5K: 9.2%
- 8.5~9.0K: 7.2%
- 9.0~9.5K: 17.2%

즉 adaptive schedule이 후반 불안정에 반응하고 있었던 흔적은 있다. 다만 event에는 **실제 KL scalar가 저장되어 있지 않아서**, 어떤 KL 값 때문에 LR이 내려갔는지는 검증할 수 없다.

이 자료만으로 PPO learning-rate 설정을 원인이라고 확정하거나 변경을 권할 수는 없다. 오히려 대회 제출용에서는 배포 PPO를 유지하고 reward와 학습량으로 조절한다는 기존 운영 원칙과 맞춰, **학습량/체크포인트 보존/조기 경고**를 먼저 개선하는 것이 안전하다.

---

## 10. 9451의 9분 stall은 확인되지만 발산 원인으로 연결할 수 없다

일반적인 iteration은 후반 약 4.2초다. 그런데:

- 9450: collection `6.242s`, learning `7.935s`, 총 `14.18s`
- **9451: collection `491.110s`, learning `67.258s`, 총 `558.37s`**
- 9452: collection `4.274s`, learning `0.096s`, 정상 복귀

9451 한 iteration에서 약 **9분 18초**가 걸렸다. 이 때문에 9K→9.5K 벽시계가 비정상적으로 길어진다.

중요한 점은 stall 직후 policy metrics와 value loss가 즉시 붕괴하지 않았다는 것이다. 9452~9504는 다시 정상 처리량과 대체로 정상 value loss로 돌아왔고, 최종 대형 발산은 약 60 iteration 뒤다.

따라서:

- **stall이 있었다** → 확정
- stall이 GPU/CPU/I/O/다른 concurrent play 때문이었다 → 이 archive만으로 확정 불가
- stall이 9512 발산을 직접 유발했다 → 근거 부족

이 run에는 학습 중 GPU telemetry가 없으므로 원인 분석은 여기서 멈춰야 한다.

---

## 11. checkpoint 상태: 9500은 깨진 모델이 아니다

| 항목 | `model_4500` | `model_9500` |
|---|---:|---:|
| checkpoint `iter` | 4500 | 9500 |
| action std min | 0.292 | 0.300 |
| action std mean | 0.482 | 0.477 |
| action std max | 0.660 | 0.593 |
| actor tensors finite | True | True |
| critic tensors finite | True | True |
| optimizer tensors finite | True | True |

`model_9500.pt`는 final crash 이전의 정상 checkpoint다. action std가 모두 양수이며 actor/critic/optimizer가 finite다.

따라서 “9500 checkpoint 자체가 이미 NaN/negative std로 깨져 있었다”는 가설은 기각된다.

다만 이 사실이 **9500에서 resume하면 다시 안전하게 진행된다**는 뜻은 아니다. optimizer state까지 9500 시점의 상태를 포함하고 있으며, 이 run 자체가 이미 7.7K 이후 반복적 critic burst를 보였다. resume 안정성은 별도 실험 없이는 알 수 없다.

---

## 12. `std >= 0` 오류의 정확한 해석

raw console의 최초 명백한 수치 이상은 action std가 아니라 value loss다. 반면 console의 `Mean action std`는 crash 직전까지 약 `0.48~0.49`로 정상처럼 보인다.

여기서 주의할 점이 있다. `Mean action std`는 12개 차원의 평균이므로, 실패 순간에 특정 차원이 음수가 되었더라도 평균만으로는 검출되지 않을 수 있다. 또한 마지막 보존 checkpoint는 9500이라 9535 이후 실제 std vector를 직접 열어볼 수 없다.

따라서 가장 안전한 결론은:

> **최종 예외는 distribution std의 유효성 실패였지만, 최초 관찰 이상은 훨씬 앞선 critic value-loss burst였다. `std` 오류는 terminal failure이며 root cause라고 확정할 수 없다.**

---

## 13. 자동 `report.html`과 raw log 불일치

자동 report는 전체 방향은 맞지만 세부 시점 표현이 정확하지 않다.

report에는 대략 “value loss가 9533회째 nan”으로 표시되지만 raw console/TensorBoard는:

- 9532: `inf`
- 9533: `inf`
- 9534: `inf`
- **9535: `nan`**

이다.

따라서 발산 시점처럼 정확한 iteration이 중요한 분석에서는 raw event와 full console을 우선해야 한다.

자동 best selection 자체는 raw event와 일치한다.

- 최고 `Train/mean_reward`: step **9512**, `19.652462`
- 가장 가까운 저장 checkpoint: `model_9500.pt`
- 현재 `exported/model_best.pt` SHA-256 = `model_9500.pt` SHA-256

즉 checkpoint selection은 이번 run에서는 provenance가 확인된다.

---

## 14. 중대한 provenance 발견: 현재 `policy.pt`는 9500 policy가 아니다

archive 안의 파일 시간을 보면:

- `exported/policy.pt`: 2026-08-30 03:14:36 UTC
- final `exported/model_best.pt`: 2026-08-30 03:20:51 UTC

그리고 TorchScript `policy.pt`의 8개 actor MLP tensor를 checkpoint와 직접 비교했다.

- `policy.pt` vs `model_4500.pt` actor weights: **모든 tensor bit-for-bit 동일**
- `policy.pt` vs `model_9500.pt` actor weights: **불일치**

즉:

> **현재 archive의 `exported/policy.pt`는 5K 선별본 `model_4500.pt`에서 export된 policy다. 최종 9.5K `model_best.pt`와 연결된 policy가 아니다.**

이는 파일명이 아니라 실제 weight를 비교해서 확인한 사실이다.

따라서 이 archive에서:

- `model_best.pt` → 9500
- `policy.pt` → 4500

으로 서로 다른 정책이 섞여 있다.

9.5K 후보를 이후 evaluator/play에 사용할 경우 반드시 `model_9500.pt`를 source로 staging한 뒤 `policy.pt`와 video를 **새로 생성하고 hash manifest로 연결**해야 한다.

---

## 15. 학습시간과 marginal gain

L40S 실측 벽시계:

| 지점 | 경과 |
|---:|---:|
| 1K | 01:16:44 |
| 3K | 약 03:40 |
| 4.5K | 05:22:40 |
| 5K | 05:56:33 |
| 6K | 07:04:29 |
| 7K | 08:13:49 |
| 8K | 09:23:43 |
| 9K | 10:34:00 부근 |
| 9.5K | 11:21:55 부근, **9451 stall 포함** |

5K→9.5K에는 약 5시간 25분 이상이 추가로 들지만, 이 구간에서 terrain과 XY tracking이 크게 개선됐다. 따라서 이 run만 놓고 보면 장기학습 비용은 단순 낭비가 아니었다.

다만 9K→9.5K는 약 500 iterations에서 성능 gain이 작아지고 value instability가 매우 커진 구간이다. 9451 stall을 빼면 실제 계산시간은 기록된 47분55초보다 약 9분 짧다.

---

## 16. 다음 Go2 실험에 바로 적용할 수 있는 판단

### 16.1 screening 길이

이 run의 curriculum dynamics를 기준으로 용도를 분리하는 것이 좋다.

| 길이 | 이 run에서 확인 가능한 것 | 주의 |
|---:|---|---|
| 1K | 즉시 붕괴, standing/gait 방향, 심한 bouncing | terrain 성능 판단 불가 |
| 3K | 생존 회복, 기본 추종 방향 | terrain은 거의 0 |
| 5K | 초기 terrain 적응, 안정성 | 고난도 terrain 판단에는 이르다 |
| 7K | terrain 5 부근 진입 | 수치 불안정 감시 필요 |
| 8~9K | mature terrain + linear tracking 비교 | critic burst 빈도 증가 |
| 9.5K+ | 이 run에서는 추가 gain 존재 | 위험 증가, 단일 run으로 안전 한계 일반화 금지 |

따라서 **Go2 reward 후보를 1K에서 모두 최종 판정하는 방식은 피하는 것이 좋다.** 1K는 탈락용 screening, 살아남은 후보만 중간 길이와 장기 confirmation으로 올리는 구조가 적합하다.

### 16.2 다음 baseline/confirmation의 종료 전략

이 단일 run만으로 “9K가 정답”이라고 할 수는 없다. 운영진 설명대로 장기 발산은 확률적일 수 있다.

하지만 비용 대비 정보량을 보면 다음 전략이 합리적이다.

1. 1~3K에서 catastrophic reward 후보 제거
2. 유망 후보는 5K까지 확인
3. terrain/tracking이 계속 개선되면 7~9K까지 confirmation
4. 8K 이후에는 모든 `model_N.pt`를 외부 sidecar로 보존
5. 10K/12K를 처음부터 무조건 목표로 잡지 않고 8~9K 지표와 critic stability를 보고 결정

### 16.3 critic instability 경고선

아래 값은 **이 run에서 사후적으로 유용했던 경고선**이지 보편적인 공식 threshold가 아니다.

- `value loss > 1`: warning — 7717부터 간헐적 instability 시작
- `> 10`: strong warning — 8068 이후 반복
- `> 100`: critical — 9413에서 이미 303 발생
- `> 1e3`, `inf`, `nan`: immediate failure state로 취급
- rolling p95가 수십 배 증가하면서 spike 빈도가 증가하면 장기 continuation의 위험 신호

한 번의 spike만으로 즉시 정책을 폐기하면 안 된다. 실제로 여러 번 회복했다. **빈도·최댓값·rolling p95의 동시 증가**를 보는 것이 더 낫다.

---

## 17. standing-balance 가설과 이 자료의 한계

현재 config에서:

- `rel_standing_envs = 0.02`
- `flat_orientation_l2 = 0.0`

이라는 사실은 확인된다.

그러나 TensorBoard에는 standing-command 전용 roll/pitch, standing subset failure, orientation metric이 없다. 따라서 이 baseline만으로 “flat orientation 비활성화가 standing 실패의 원인”이라고 확정할 수 없다.

다음 standing-balance screening에서 이 가설을 검증하려면 aggregate mean reward가 아니라 standing command 구간의 자세·낙상·영상 데이터를 따로 확보해야 한다.

---

## 18. 이번 archive에서 답할 수 없는 것

- 공식 예선 시나리오 점수
- 4500 vs 9500의 동일 조건 play 영상 품질 — 영상이 archive에 없음
- 9451 stall의 GPU/CPU/I/O 원인 — GPU 시계열 없음
- critic burst의 정확한 최초 수학적 원인
- 실패 직전 std vector — 9500 이후 checkpoint 없음
- KL 변화 — TensorBoard에 KL scalar 없음
- 동일 reward의 seed 간 발산 확률
- 8K/9K checkpoint의 실제 evaluator 성능 — finalize cleanup으로 파일이 남지 않음
- 9.5K가 보편적 위험 임계점인지 여부

이 항목들은 추정으로 채우지 않는다.

---

## 19. 데이터 보존 측면에서 얻은 교훈

이번 run은 분석 가치가 높지만 finalize가 intermediate checkpoint 95개, 약 624MB를 삭제했다. 그래서 8K/9K처럼 분석상 중요한 시점의 실제 모델을 지금 다시 평가할 수 없다.

다음 실행에서는 현재 개발 중인 sidecar 방식으로 최소한 다음을 보존해야 한다.

- full console
- full TensorBoard event
- `model_*.pt` 100-iteration checkpoint mirror
- actual reward/config/source hash
- GPU telemetry
- final `model_best.pt`
- checkpoint→policy→video SHA-256 provenance
- 성공/실패 모두 archive

특히 이번에 `model_best.pt=9500`, `policy.pt=4500`이 섞인 사실이 실제 weight comparison으로 확인됐으므로 **stale export 방지는 선택 사항이 아니라 필수**다.

---

## 20. 최종 판정

### 정책 학습 관점

이 baseline은 **약 5K에서 끝났어야 할 학습이 아니었다.** 5K 이후에 terrain과 linear tracking이 크게 개선됐고, 특히 6~9K가 가장 정보 가치가 높았다.

### 수치 안정성 관점

반대로 **12K를 끝까지 밀어붙이는 것도 좋은 전략이 아니었다.** 7.7K 이후 critic value-loss burst가 반복됐고 9K 이후 tail risk가 급격히 커졌다. 최종 실패는 완전히 무전조가 아니었다.

### 보존 checkpoint 관점

`model_9500.pt`는 finite하고 action std도 정상 범위이므로 **발산 이전의 유효한 개인 검증 후보**다. 다만 공식 성능, 수렴, resume 안정성을 보장하지 않는다.

### 다음 학습 전략

> **짧은 screening → 5K 확인 → 유망 후보만 7~9K confirmation → 모든 checkpoint 보존 → critic instability 감시**가 이 데이터에 가장 잘 맞는다.

그리고 9.5K 후보를 실제로 비교할 때는 archive의 기존 `policy.pt`를 쓰지 말고 **`model_9500.pt`에서 fresh export**해야 한다.

---

## 부록 A. 핵심 원본 식별자

- recovery archive SHA-256: `c3bea262eb45d5f46357ce97049a0ede9f2f7eeb11008d4b20cef1fd1a33106b`
- event SHA-256: `12377469daaba5739989c3f434eb7c88ad76acb30fbaac0a64435b1bab12e6c1`
- console SHA-256: `006dcccde340bf17c05e020bf44d5ab0b7f20292d8e0af6c5128888f1fcd7588`
- 5K selected checkpoint SHA-256: `7ec9542381b3d320009c23f9681dfd281dc022fc45998c9f6c9b7c9d020ef974`
- 9.5K checkpoint SHA-256: `a7b65db49f0c6207e488ec707c3d11b2218cd75beef479503b441f44199637df`
- final exported `model_best.pt`: `a7b65db49f0c6207e488ec707c3d11b2218cd75beef479503b441f44199637df`
- current exported `policy.pt`: `67379f85bbddb52a18bb99db3c70cc32e4d4468c929bc39bf5c998b41554f761`
- `policy.pt == model_4500 actor`: `True`
- `policy.pt == model_9500 actor`: `False`

## 부록 B. 분석 규칙

1. TensorBoard scalar는 모든 점을 직접 읽었다.
2. 정확한 crash sequence와 wall-clock은 full console을 우선했다.
3. `report.html`은 교차검증용으로만 사용했다.
4. checkpoint는 `torch.load(..., weights_only=True)`로 tensor finite/std를 검사했다.
5. TorchScript `policy.pt` provenance는 actor state tensor의 bitwise equality로 확인했다.
6. 단일 seed/private L40S run이므로 공식 점수·통계적 최적값·보편적 발산 임계값으로 일반화하지 않는다.
