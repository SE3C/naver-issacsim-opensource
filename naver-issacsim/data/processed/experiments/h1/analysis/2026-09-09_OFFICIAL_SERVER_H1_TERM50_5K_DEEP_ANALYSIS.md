---
id: h1-official-server-term50-20260908-5k
source_type: received_artifact_analysis
category: official_server_experiment
robot: H1
run_started_at: '2026-09-08 23:23:33 KST'
received_at: '2026-09-09'
source_sha256: aec55d15df51f3cb8deebefd2f1ebbd7a3d6faaf7608a6379f9f8405d966c846
trust_level: artifact_linkage_verified_with_documented_comparison_limits
authority: '공식 서버 실행 산출물의 분석이며 공식 evaluator 점수나 최종 제출 성능 판정은 아니다.'
---

# [분석] H1 TERM50 5K 심층 분석 보고서

> 관리 안내 (2026-10-13): **분석** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](../../../../../research/EXPERIMENTS.md)를 확인한다.

- 대상 아카이브: `H1_TERM50_5k_complete_20260909_003012.tar.gz`
- 실험 ID: `H1_TERM50_5k`
- Task: `Humanoid-v0`
- 핵심 변경: `termination_penalty: -5.0 → -50.0`
- 학습: 4,096 envs / seed 42 / 5,000 iterations / 24 rollout steps per env
- source run: `2026-09-08_23-23-33`
- 분석 범위: TensorBoard 5,000개 scalar 전량, `env.yaml`, `agent.yaml`, reward 파일, checkpoint/policy hash, `report.html`, 현재 TERM50 play 영상, 아카이브에 함께 남은 직전 `-5` play 영상

---

## 1. 결론 요약

**TERM50 5K는 “낙상 억제 + 지형 진행” 가설을 성공적으로 확인했지만, 최종 제출용 균형 정책으로 보기에는 yaw 추종 성능이 아직 부족하다.**

가장 중요한 결과는 다음과 같다.

1. **안정성은 명확히 좋아졌다.**
   - 마지막 base-contact 종료율: **28.93%**
   - 마지막 timeout 비율: **71.07%**
   - 현재 40초 play 영상에서는 샘플링한 전 구간에서 **명확한 낙상이 보이지 않았다.**
   - 반대로 아카이브에 남아 있는 이전 `termination_penalty=-5` 영상은 약 20초 안에 여러 차례 명확한 낙상/바닥 접촉이 보인다.

2. **지형 curriculum은 강하게 진행됐다.**
   - 마지막 terrain level: **5.825**
   - 1K 시점 이미 **4.821**
   - 4K 부근에서 **5.8**을 넘었고, 이후 거의 포화 구간에 들어갔다.

3. **회전/yaw 추종은 이번 정책의 가장 큰 병목이다.**
   - yaw error: 1K **1.468** → 3K **0.934** → 5K **0.935**
   - 즉 1K→3K에서는 크게 좋아졌지만, **3K 이후에는 거의 정체**됐다.
   - 과거 5K baseline(`termination=-5`) endpoint의 yaw error **0.652**보다 현재 TERM50 5K가 약 **43% 더 크다.**

4. **`model_best.pt`는 공식 평가 기준의 “최고 정책”이라고 볼 수 없다.**
   - 학습 reward peak: **iteration 4851, mean reward 4.6484**
   - 실제 저장 checkpoint는 100회 간격이므로 `model_best.pt = model_4900.pt`
   - 4900 시점은 4999 시점보다 생존성/episode length는 좋지만, **XY/yaw tracking은 오히려 나쁘다.**
   - 즉 현재 reward 함수가 “안정성”을 강하게 선호한 결과, training reward 기반 best 선택도 그 방향으로 편향되어 있다.

### 최종 판정

| 항목 | 판정 |
|---|---|
| 낙상 안정성 | **개선 확인** |
| Terrain progression | **매우 좋음** |
| 전진/XY 추종 | **보통~양호, baseline보다 소폭 열세** |
| Yaw/회전 추종 | **명확한 병목** |
| 학습 수치 안정성 | **정상** |
| 영상 안정성 | **TERM50 쪽이 훨씬 안정적** |
| 그대로 장시간 추가 학습 | **효율 낮음 가능성 큼** |
| 최종 제출 후보 | **아직 보류** |
| 다음 단계 용도 | **stability anchor / staged training 출발점으로 적합** |

---

## 2. 산출물 무결성 및 provenance

이번 묶음은 과거 TERM50 1K 분석 때 문제가 되었던 “영상과 checkpoint 오연결” 문제를 상당 부분 해결했다.

### 현재 TERM50 산출물 연결

| 파일 | 확인 내용 |
|---|---|
| `logs/.../model_4900.pt` | SHA-256 = `e7343a...` |
| `exported/model_best.pt` | 위 `model_4900.pt`와 **동일 hash** |
| `exported/model_best_20260908232333.pt` | 위와 **동일 hash** |
| `exported/policy.pt` | `policy_20260909_003012.pt`와 **동일 hash** |
| `exported/play_video.mp4` | `play_video_20260909_003012.mp4`와 **동일 hash** |
| `env.yaml` | `termination_penalty=-50.0` 확인 |
| `humanoid_rewards.py` | 학생 변경값 `-50.0` 확인 |
| IsaacLab | commit `3e73d6dd79080fd7632488c061052a6edd52e230`, working tree clean |
| 호스트 | Ubuntu 24.04.2 LTS, RTX 5080 16,303 MB, driver 580.126.09 (originals TERM50 README) |

`model_best.pt` 내부의 `iter` 필드도 **4900**으로 확인됐다.

Torch checkpoint와 TorchScript policy의 parameter를 직접 검사한 결과 **NaN/Inf 없이 모두 finite**였다.

### 주의: `exported/` 안에 이전 실행 파일도 같이 존재

현재 아카이브에는 아래와 같은 이전 실행 산출물도 남아 있다.

- `env_20260908230725.yaml` → `termination_penalty=-5.0`
- `model_best_20260908230725.pt`
- `policy_20260908_232209.pt`
- `play_video_20260908_232209.mp4`

따라서 제출·후속 분석 때 파일명만 보고 고르면 안 된다. **현재 TERM50 산출물은 `20260909_003012` 계열과 현재 `model_best.pt` hash를 기준으로 구분해야 한다.**

---

## 3. 실제 적용된 reward 구조

play console과 `env.yaml`에서 14개 reward term이 활성 manager에 등록되어 있고, 그중 `dof_torques_l2=0`을 제외하면 **13개가 실질적으로 non-zero**다.

### 학생 수정 대상 9개

| Reward | Weight |
|---|---:|
| `track_lin_vel_xy_exp` | +0.5 |
| `track_ang_vel_z_exp` | +0.5 |
| `feet_air_time` | +0.2 |
| `termination_penalty` | **-50.0** |
| `flat_orientation_l2` | -1.5 |
| `ang_vel_xy_l2` | -0.05 |
| `joint_deviation_hip` | -0.2 |
| `joint_deviation_torso` | -0.1 |
| `action_rate_l2` | -0.0005 |

### 프레임워크 쪽 추가 활성 term

| Reward | Weight |
|---|---:|
| `dof_acc_l2` | -1.25e-7 |
| `dof_pos_limits` | -1.0 |
| `feet_slide` | -0.25 |
| `joint_deviation_arms` | -0.2 |
| `dof_torques_l2` | 0.0 |

이번 실험에서 학생 reward 중 실제로 바뀐 값은 **`termination_penalty` 하나뿐**이다.

---

## 4. 5K 학습 곡선 분석

TensorBoard event에는 주요 scalar가 **iteration 0~4999 전부 5,000 point**로 남아 있다.

### 4.1 주요 milestone

| iter | Mean reward | Episode length | Terrain | Fall(base contact) | Timeout | XY error | Yaw error | Mean std |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 99 | -1.180 | 90.8 | 0.000 | 100.0% | 0.0% | 0.131 | 0.259 | 0.817 |
| 299 | -0.564 | 706.3 | 0.846 | 48.31% | 51.69% | 0.588 | 1.657 | 0.986 |
| 499 | 0.595 | 781.2 | 2.441 | 39.91% | 60.09% | 0.498 | 1.645 | 1.129 |
| **999** | **1.344** | **819.8** | **4.821** | **32.37%** | **67.63%** | **0.431** | **1.468** | **1.319** |
| 1499 | 1.101 | 686.0 | 5.119 | 32.41% | 67.59% | 0.371 | 1.119 | 1.347 |
| 1999 | 2.277 | 778.3 | 5.337 | 28.66% | 71.34% | 0.359 | 1.082 | 1.336 |
| 2499 | 2.653 | 759.5 | 5.452 | 29.27% | 70.73% | 0.371 | 1.018 | 1.323 |
| 2999 | 3.063 | 775.1 | 5.636 | 29.79% | 70.24% | 0.360 | **0.934** | 1.311 |
| 3999 | 2.827 | 725.9 | 5.792 | 28.30% | 71.70% | 0.345 | 0.872 | 1.308 |
| 4499 | 3.216 | 778.8 | 5.722 | 29.05% | 70.95% | 0.378 | 0.947 | 1.302 |
| **4851 reward peak** | **4.648** | **890.4** | 5.703 | **27.10%** | **72.90%** | 0.387 | 0.985 | 1.291 |
| **4900 selected ckpt** | 4.131 | 852.8 | 5.743 | **27.97%** | **72.06%** | 0.384 | **0.995** | 1.293 |
| **4999 final** | **3.346** | **774.1** | **5.825** | **28.93%** | **71.07%** | **0.378** | **0.935** | **1.296** |

### 4.2 구간 평균

| 구간 | Mean reward | Episode len | Terrain | Fall | XY err | Yaw err |
|---|---:|---:|---:|---:|---:|---:|
| 0~499 | -0.729 | 469.1 | 0.805 | 69.36% | 0.405 | 1.130 |
| 500~999 | 0.916 | 771.1 | 4.043 | 34.28% | 0.450 | 1.505 |
| 1000~1999 | 1.732 | 771.1 | 5.091 | 30.67% | 0.396 | 1.255 |
| 2000~2999 | 2.890 | 774.4 | 5.449 | 29.71% | 0.366 | 1.021 |
| 3000~3999 | 3.320 | 783.5 | 5.656 | 28.93% | 0.366 | **0.957** |
| 4000~4499 | 3.349 | 791.6 | 5.734 | 28.55% | 0.381 | **0.953** |
| 4500~4999 | 3.701 | 796.0 | 5.731 | 28.15% | 0.369 | **0.921** |
| 마지막 100 | 3.745 | 795.6 | 5.787 | 28.04% | 0.360 | **0.908** |

### 해석

학습은 크게 네 단계로 나뉜다.

#### Phase A — 0~300: 초기 붕괴 후 생존 학습

- 100 iter 부근에서는 base-contact 종료가 거의 100%다.
- 300 iter까지 episode length가 700 이상으로 급상승하며 낙상 회피를 빠르게 학습한다.
- 이 시점에는 tracking이 아직 매우 나쁘다. 특히 yaw error가 1.6 이상까지 커진다.

즉 `-50`의 강한 종료 penalty가 처음에는 **“명령을 잘 따르기보다 일단 죽지 않는 법”**을 먼저 배우게 한 것으로 해석하는 것이 가장 자연스럽다.

#### Phase B — 300~1000: terrain 급상승

- terrain 0.85 → 4.82
- fall 48% → 32%
- episode length 약 820

**1K만으로 이미 stability/terrain 쪽 핵심 효과 대부분이 나타난다.**

#### Phase C — 1K~3K: tracking 회복

- yaw error 1.47 → 0.93
- XY error 0.43 → 0.36
- terrain 4.82 → 5.64

이 구간은 “안정성 확보 후 추종을 다시 회복하는 시기”로 보인다.

#### Phase D — 3K~5K: 안정성/terrain 포화, yaw 개선 둔화

- fall 평균 약 29% 주변
- terrain 약 5.65~5.8
- yaw error 평균 0.95 → 0.92 정도

즉 **3K 이후에는 추가 2K의 효율이 크게 떨어진다.**

---

## 5. Terrain progression

처음 특정 terrain level을 넘은 iteration은 다음과 같다.

| Terrain threshold | 최초 도달 iter |
|---:|---:|
| 4.0 | 692 |
| 4.5 | 819 |
| 5.0 | 1359 |
| 5.5 | 2633 |
| 5.7 | 3807 |
| 5.8 | 4008 |

1K 시점에 이미 4.82까지 올라가고, 약 4K에서 5.8을 넘었다.

**지형 적응만 놓고 보면 5K는 충분히 고난도 영역까지 도달한 상태다.** 이후 더 오래 돌려 얻을 terrain 이득은 제한적일 가능성이 높다.

---

## 6. Reward term별 분석

아래 값은 TensorBoard `Episode_Reward/*`의 **마지막 500 iteration 평균**이다. 서로 다른 reward weight가 이미 적용된 logger 값이므로, 단순히 항목끼리 더해서 `Train/mean_reward`와 같다고 보면 안 된다. 각 항목의 상대적인 압력과 추세를 보는 용도다.

### 마지막 500 iter 평균

| Reward term | logged mean |
|---|---:|
| `track_lin_vel_xy_exp` | **+0.32066** |
| `track_ang_vel_z_exp` | **+0.17856** |
| `feet_air_time` | +0.01049 |
| `termination_penalty` | -0.01884 |
| `joint_deviation_arms` | **-0.08461** |
| `action_rate_l2` | **-0.06062** |
| `dof_acc_l2` | -0.04394 |
| `feet_slide` | -0.04011 |
| `joint_deviation_hip` | -0.03394 |
| `ang_vel_xy_l2` | -0.02143 |
| `flat_orientation_l2` | -0.01125 |
| `joint_deviation_torso` | -0.00659 |
| `dof_pos_limits` | -0.00393 |

### `termination_penalty` 자체의 변화

| 구간 | logged mean |
|---|---:|
| 0~499 | -0.03644 |
| 500~999 | -0.02076 |
| 1000~1999 | -0.02023 |
| 4500~4999 | **-0.01884** |

강한 `-50` penalty를 주었지만 후반에는 실제 종료 빈도가 줄어들면서 이 term의 평균 손실도 감소한다.

이것은 TERM50이 단순히 매 step 정책을 억누르는 방식이라기보다, **초기 학습 방향을 “낙상 회피” 쪽으로 강하게 재배치한 뒤 실제 낙상이 줄면서 penalty 발생 자체가 줄어든 패턴**으로 볼 수 있다.

### Tracking reward의 성장

| Reward | 0~499 | 500~999 | 1000~1999 | 4500~4999 |
|---|---:|---:|---:|---:|
| `track_lin_vel_xy_exp` | 0.136 | 0.283 | 0.300 | **0.321** |
| `track_ang_vel_z_exp` | 0.0556 | 0.110 | 0.130 | **0.179** |

angular tracking reward도 계속 증가하므로 회전 능력이 전혀 학습되지 않은 것은 아니다. 다만 실제 yaw error는 baseline보다 여전히 커서 **“회전 추종을 배우고는 있지만 안정성 우선 정책의 trade-off를 완전히 회복하지 못했다”**고 보는 것이 맞다.

---

## 7. 학습 안정성 / PPO 상태

### Loss

후반 1,000 iter 평균:

- value loss: 약 **0.0048~0.0049**
- surrogate loss: 약 **-0.012**
- entropy: 약 **22.7~23.0**
- learning rate: 약 **1.8~2.0e-4**

초기 value loss spike 이후 장기적인 폭주나 NaN 패턴은 보이지 않는다.

### Policy mean std

- 시작: 1.001
- 최소: 0.813 @ iter 75
- 최대: 1.352 @ iter 1297
- 마지막: **1.296**

`report.html`은 이 값을 보고 “std가 높다”고 경고하지만, **std 하나만으로 미학습이라고 판단하면 안 된다.** 실제로 동시에 terrain 5.8, timeout 약 71%, episode length 약 800까지 올라와 있기 때문이다.

이번 run에서는 std가 높은 것이 “학습 실패”의 직접 증거라기보다, **여전히 상당한 stochastic exploration을 유지하는 정책 특성**으로 보는 편이 더 합리적이다.

---

## 8. 처리량 / 학습 시간

TensorBoard wall-time 기준 첫 scalar~마지막 scalar 간격은 약 **3,851초 = 64.2분**이다.

`collection_time + learning_time`의 전체 합은 약 **3,576.6초 = 59.6분**이다.

후반 성능:

- total FPS: 약 **138k env-steps/s**
- collection time: 약 **0.629 s/iter**
- learning time: 약 **0.079 s/iter**

큰 처리량 저하나 장기적인 성능 degradation은 보이지 않는다.

단, **training console 원문이 이 아카이브에 없기 때문에** 실제 train stdout/stderr warning, 정확한 process exit code, GPU utilization/power 시계열은 확인할 수 없다.

---

## 9. 현재 TERM50 play 영상 분석

### 영상 메타데이터

- 파일: `play_video_20260909_003012.mp4`
- 1920×1080
- 50 FPS
- 2,000 frames
- **40.00초**
- play environment: 1 env
- episode limit: **20초**
- command resampling: **10초**

따라서 40초 영상은 **최대 20초 episode 두 개 정도의 행동을 포함할 수 있으며, 40초 연속 생존 증거는 아니다.**

### 화살표 의미

`env.yaml`의 visualizer 색상 설정으로 직접 확인했다.

- **초록색 arrow = goal velocity**
- **파란색 arrow = current velocity**

즉 두 arrow의 방향/크기 차이는 명령과 실제 이동 속도의 차이를 시각적으로 보여준다.

### 0~10초

- 로봇은 계속 upright 상태를 유지한다.
- 발 교대가 나타나며 큰 낙상 없이 이동한다.
- goal/current arrow가 완전히 겹치지는 않고 방향·크기 차이가 반복된다.
- 안정성은 좋지만 tracking이 아주 날카로운 느낌은 아니다.

### 10~20초

- 큰 방향 전환/이동 명령에도 로봇은 쓰러지지 않는다.
- 다만 일부 구간에서 초록 goal과 파란 current가 눈에 띄게 어긋난다.
- 다리를 교차하거나 보폭이 다소 보수적으로 보이는 프레임이 있다.

### 20~30초

- 초록 goal arrow가 거의 보이지 않는 구간이 길게 나타난다. 즉 목표 XY 속도가 매우 작거나 0에 가까운 command로 해석할 수 있다.
- 그런데 파란 current arrow는 계속 관찰된다.
- 로봇도 완전히 정지 자세로 고정되기보다 작은 잔류 움직임/드리프트가 남아 있는 모습이다.

이 구간은 **Stop/standing command tracking이 완벽하지 않을 가능성**을 시사한다.

### 30~40초

- 다시 큰 goal velocity가 들어오고 로봇이 방향을 바꿔 이동한다.
- 낙상은 보이지 않는다.
- goal/current arrow가 대체로 같은 방향을 향하는 순간도 있지만, 일치도가 일정하지 않다.

### 영상 종합

**가장 큰 장점은 “안 넘어지는 것”이고, 가장 큰 단점은 “명령과 실제 속도가 정확히 겹치지 않는 것”이다.**

이 영상 관찰은 TensorBoard 결과와 매우 잘 일치한다.

- fall ↓ / timeout ↑ → 영상에서도 안정
- terrain ↑ → 적극적인 이동 중에도 자세 유지
- XY error 약 0.36~0.38 → goal/current arrow mismatch 존재
- yaw error 약 0.9 → 방향/회전 추종이 날카롭지 않음

---

## 10. 아카이브에 남은 이전 `termination=-5` 영상과 비교

아카이브 안의 `play_video_20260908_232209.mp4`는 대응 `env_20260908230725.yaml`에서 `termination_penalty=-5.0`임을 확인했다.

- 길이: 19.98초
- 50 FPS
- 999 frames

### 시각적 차이

이 이전 영상에서는 약 20초 안에 로봇이 **여러 차례 명확히 바닥으로 넘어지거나 주저앉는 장면**이 보인다. 대략 5~6초, 8~9초, 10~15초 사이에 반복적으로 실패 자세가 나타난다.

반면 현재 TERM50 40초 영상에서는 0.5초 간격 프레임 샘플 전체에서 **명백한 낙상 자세가 관찰되지 않았다.**

따라서 play 영상만 놓고 봐도 `-50`이 **낙상 회피 행동을 크게 강화했다는 정성적 증거**는 강하다.

### 단, 직접적인 A/B 점수 비교로 쓰면 안 되는 이유

- 두 영상 길이가 다르다.
- command sequence가 동일하다는 증거가 없다.
- terrain/reset random state가 동일하다는 증거가 없다.
- 이전 영상의 정확한 source checkpoint와 현재 checkpoint가 같은 selection rule인지 완전히 확정할 training manifest가 없다.

따라서 영상 비교는 **강한 정성적 증거**지만 엄밀한 paired evaluator 결과는 아니다.

---

## 11. 기존 5K baseline 수치와 비교

프로젝트에 보존된 이전 5K baseline endpoint:

- episode length: **742.97**
- terrain: **5.054**
- timeout: **66.79%**
- base-contact: **33.21%**
- XY error: **0.342**
- yaw error: **0.652**

현재 TERM50 5K endpoint와 비교하면:

| Metric | Baseline 5K | TERM50 5K | 변화 |
|---|---:|---:|---:|
| Episode length | 742.97 | **774.13** | +4.2% |
| Terrain | 5.054 | **5.825** | **+15.3%** |
| Timeout | 66.79% | **71.07%** | **+4.28%p** |
| Base-contact fall | 33.21% | **28.93%** | **-4.28%p** |
| XY error | **0.342** | 0.378 | **+10.6% 악화** |
| Yaw error | **0.652** | 0.935 | **+43.3% 악화** |

### 핵심 trade-off

**TERM50는 stability/terrain을 얻고 tracking, 특히 yaw를 희생했다.**

이 결과는 TERM50을 “최종 해답”보다는 **초기 안정성 curriculum 또는 안정성 anchor**로 쓰는 것이 더 타당하다는 쪽에 강한 근거를 준다.

---

## 12. 1K 시점이 왜 중요한가

현재 동일 5K run의 **999 iteration** 값:

- terrain: **4.821**
- timeout: **67.63%**
- fall: **32.37%**
- episode length: **819.77**
- XY error: **0.431**
- yaw error: **1.468**

주목할 점은 **TERM50 1K의 timeout 67.63%가 과거 baseline 5K의 66.79%와 이미 비슷하거나 조금 높다**는 것이다.

즉 1K에서:

- 안정성은 이미 baseline 5K 수준에 도달
- terrain도 4.82까지 올라감
- 남은 큰 문제는 yaw tracking

따라서 제한된 서버 시간 안에서라면

> **“-50으로 1K 정도 안정성을 먼저 만든 뒤, 그 checkpoint에서 reward 성격을 tracking 쪽으로 전환하여 이어 학습한다”**

는 전략은 이번 5K 데이터로 상당히 설득력을 얻었다.

특히 3K 이후 yaw 개선이 크게 둔화되므로 `-50`을 그대로 유지한 채 5K 이상 계속 돌리는 것보다, **1K~2K 부근에서 다음 단계로 전환하는 실험**이 정보 효율 측면에서 더 낫다.

---

## 13. 과거 TERM50 25K 결과와의 참고 비교

별도 과거 개인 서버 TERM50 25K run의 마지막 지표는 다음과 같이 보존되어 있다.

- episode length 867.16
- terrain 5.876
- timeout 78.57%
- base-contact 21.43%
- XY error 0.372
- yaw error 0.803

현재 5K에서 25K까지 더 학습했을 때의 역사적 차이는 대략:

| Metric | TERM50 5K | 과거 TERM50 25K | 차이 |
|---|---:|---:|---:|
| Terrain | 5.825 | 5.876 | +0.051 |
| Fall | 28.93% | 21.43% | -7.50%p |
| XY error | 0.378 | 0.372 | -0.006 |
| Yaw error | 0.935 | 0.803 | -0.132 |

즉 더 오래 돌리면 생존성과 yaw가 추가로 좋아지기는 하지만:

- terrain은 사실상 거의 포화
- yaw는 20K를 더 돌려도 과거 baseline 5K의 0.652보다 여전히 나쁨

따라서 **“시간만 더 주면 yaw 병목이 완전히 사라진다”는 근거는 없다.**

단, 이 25K는 별도 날짜/실행의 역사적 결과이므로 현재 5K와 완전한 paired comparison은 아니다.

---

## 14. `model_best` 선택의 함정

이번 run의 reward peak는:

- iter **4851**
- mean reward **4.6484**
- episode length **890.42**
- fall **27.10%**
- yaw error **0.985**

checkpoint 저장 주기는 100회이므로 finalize는 가장 가까운 `model_4900.pt`를 선택했고, 이 파일이 현재 `model_best.pt`다.

그런데 4999 endpoint와 비교하면:

| Metric | model_best 근처 4900 | final 4999 |
|---|---:|---:|
| Episode length | **852.79** | 774.13 |
| Fall | **27.97%** | 28.93% |
| Terrain | 5.743 | **5.825** |
| XY error | 0.384 | **0.378** |
| Yaw error | 0.995 | **0.935** |

즉 `model_best`는 **생존/episode length 쪽으로 더 좋은 대신 tracking은 final 쪽보다 나쁘다.**

공식 평가는 여러 시나리오에서 생존과 추종을 같이 보기 때문에, `Train/mean_reward` peak만으로 policy를 고르는 것은 위험하다.

이번 archive에는 `model_4999.pt`가 남아 있지 않아 4900과 4999를 직접 play/evaluator 비교할 수 없다. 다음 실행에서는 finalize 전에 중간 checkpoint를 보존하는 것이 중요하다.

---

## 15. 다음 실험에 대한 권장 방향

### 가장 강한 결론

**`termination_penalty=-50`을 처음부터 끝까지 5K 이상 고정하는 전략보다, 초반 stability curriculum으로 쓰고 중간에 성격을 바꾸는 것이 더 합리적이다.**

이번 데이터가 지지하는 전환점은 대략 **1K~2K**다.

### 추천 실험 형태

한 번에 한 값만 바꾼다는 원칙을 유지한다.

#### Stage A

- TERM50
- 1K 또는 1.5K
- 목적: upright / terrain / survival 확보

#### Stage B 후보 1 — penalty 완화

- 이전 checkpoint에서 resume
- `termination_penalty: -50 → -20` 정도의 중간값
- 나머지 reward 고정
- 목적: 안정성을 크게 잃지 않고 명령 추종 자유도 회복 여부 확인

이 값은 **검증 전 가설**이며 최적값이라는 뜻이 아니다.

#### Stage B 후보 2 — angular tracking 미세 강화

- stable TERM50 checkpoint에서만 실험
- `track_ang_vel_z_exp: 0.5 → 0.6`처럼 작은 변화부터
- `0.75`를 처음부터 주는 실험은 과거 1K screening에서 100% base-contact 실패가 있었으므로, 동일 방식을 반복하는 것은 비효율적이다.

### 우선 판정 metric

1. yaw error
2. base-contact / timeout
3. terrain
4. XY error
5. Stop command에서 residual drift
6. 실제 play 영상

**mean reward는 보조지표로만 사용한다.**

---

## 16. 이 아카이브에서 아직 확정할 수 없는 것

- 공식 7개 시나리오 실제 점수
- push recovery 성능
- slope ±10°만 분리한 성능
- 좌우 velocity 명령만 격리한 tracking
- yaw-only command의 정확한 response curve
- 동일 seed/동일 command sequence의 baseline-vs-TERM50 paired video
- 4900과 4999 checkpoint의 직접 policy 비교
- 복수 seed 재현성
- training stdout/stderr 전체 warning 및 GPU telemetry

따라서 이 보고서의 결론은 **“TERM50의 학습 내부 지표 + 현재 play 행동 + 과거 baseline 맥락”에 대한 판단**이며, 공식 평가 점수 예측은 아니다.

---

# 최종 한 줄 결론

**TERM50 5K는 H1을 확실히 덜 넘어지고 더 어려운 지형까지 보내는 데 성공했지만, yaw 추종을 희생했으며 3K 이후 그 회복이 둔화된다. 따라서 `-50`은 최종 고정 reward라기보다 약 1K 전후의 안정성 pre-training 단계로 쓰고, 이후 tracking 쪽으로 한 변수씩 전환하는 staged training 전략이 현재 데이터에 가장 잘 맞는다.**
