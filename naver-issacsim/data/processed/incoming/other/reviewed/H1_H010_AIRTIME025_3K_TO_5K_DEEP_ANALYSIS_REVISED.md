# H1 H-010 AIRTIME025 3K→5K Deep Analysis

**Experiment:** H-010 · AIRTIME025  
**Robot:** Unitree H1 / `Humanoid-v0`  
**Environment:** PERSONAL / Brev L40S  
**Run:** `20260920-134309-h1-h010-airtime025-rerun`  
**Parent:** H-008 3K final `model_2998.pt`  
**Parent SHA-256:** `d9a30c8a117f69cac49c4e640500f0fa8d88de72d6c61855f1e147ea6c1912ae`  
**Single intended delta:** `feet_air_time: 0.20 → 0.25`  
**Requested additional training:** 2,000 iterations  
**Observed global iteration range:** 2998→4997  
**Primary representative checkpoint in this analysis:** `model_4997.pt`  
**Analysis status:** complete for supplied train archive + supplied six-terrain video suite; no official evaluator result supplied.

---

# 1. Executive Summary

이번 H-010은 H-008 3K final `model_2998.pt`에서 시작해 `feet_air_time`만 `0.20 → 0.25`로 올리고 2,000회 resume한 PERSONAL 실험이다. 실행 자체는 정상 완료됐고, exit code 0, TensorBoard 2,000 scalar points/tag, 21개 numbered checkpoint, source hash, GPU telemetry가 보존되었으며 evidence validation은 PASS다. 정책/optimizer tensor도 보존된 21개 checkpoint 모두 finite였다.

학습 동역학은 명확한 **resume 재적응 → 빠른 생존 회복 → terrain 재상승 → 후기 plateau**의 네 단계로 보인다. resume 직후 terrain은 3.438에서 3.170까지 내려갔다가 iter 3041에 시작값을 회복했고, iter 3164에 terrain 5.0, iter 3254에 5.5를 넘어섰다. 후반 last-500 terrain 평균은 **5.663**, XY error **0.3318**, base-contact **29.63%**, episode length **773.65**, yaw error **1.4187**이었다. 즉 정책은 높은 terrain에서 약 70% timeout / 30% base-contact 수준으로 오래 걷는 정책을 유지했고, 후기에는 terrain이나 XY tracking의 공동 붕괴가 없다.

그러나 이번 변경의 인과적 이득은 약하다. 가장 중요한 matched control은 같은 H-008 `model_2998`에서 reward를 바꾸지 않고 +2K 진행한 H-008 continuation이다. 그 control의 late console 요약은 terrain **5.604**, XY **0.3314**, base-contact **29.67%**이다. H-010의 대응 late/last-window 값과 사실상 같은 범위다. 따라서 `feet_air_time=0.25`가 terrain/tracking/stability를 의미 있게 개선했다고 주장할 근거는 없다. 반대로 명확한 붕괴나 hopping reward hacking도 관찰되지 않아 “해로운 변경”으로 확정하기도 어렵다.

raw TensorBoard 전체의 `Train/mean_reward` 최대는 **6.585 @ iter 3044**지만, resume 시 finalizer는 **추가 학습 구간의 첫 10%를 best 후보에서 제외**한다. 이번 +2,000 iteration resume에서는 약 첫 200회(global 약 2998~3197)가 제외되므로 iter 3044는 애초에 best 후보가 아니다. 이 규칙을 적용한 eligible 구간의 raw 최대는 **5.7828 @ iter 3299**이며, `report.html`의 **5.783 @ iter 3299 → model_3300**과 정확히 일치한다. 따라서 여기에는 report/finalizer와 raw TensorBoard의 불일치가 없다. 다만 이 자동 best는 training-reward selector의 결과일 뿐 실제 terrain/tracking/stability 최적 정책을 뜻하지 않으므로, late metrics가 공동 붕괴하지 않은 **final `model_4997`**을 이번 resume의 대표 checkpoint로 본다.

여섯 terrain 영상은 boxes, stairs, inverted stairs, random rough, ±10° slope에서 샘플 프레임 기준 로봇이 upright locomotion을 유지하고 지형 내부를 이동하는 모습을 보여준다. 특히 boxes에서 큰 단차 구간을 지나면서도 지속적인 한발 깡충이나 누운 자세 생존은 보이지 않았다. 다만 영상 manifest는 checkpoint를 `model_4997.pt`라고 “assert”할 뿐 checkpoint bytes/hash를 영상 bundle 안에 포함하지 않으므로, 영상→checkpoint 연결은 암호학적으로 self-contained하지 않다. 또한 단일 19.98초 trajectory/terrain이므로 성공률·fall rate·명령 추종 점수를 뜻하지 않는다.

**최종 판정: HOLD.** `0.25`는 안정적으로 학습되고 reward hacking도 뚜렷하지 않지만, 같은 parent + 같은 +2K의 `.20` control을 이긴다는 실질적 증거가 없다. 따라서 이 값을 더 길게 연장하거나 AIRTIME 축을 계속 sweep하기보다, 다음 정보 효율이 높은 학습은 같은 H-008 `model_2998` parent에서 `joint_deviation_hip -0.20 → -0.10`만 바꾸는 H-011 방향이다. 이미 반대 방향 `-0.30`인 H-009가 있으므로, H-009 분석을 먼저 끝낸 뒤 H-011을 실행하면 hip constraint의 local sensitivity를 양쪽에서 확인할 수 있다.

---

# 2. Run Identity & Evidence Integrity

## 2.1 확정된 실행 정체성

| 항목 | 확인 결과 | 근거 강도 |
|---|---|---|
| Robot / task | H1 / `Humanoid-v0` | 확인됨 |
| Experiment ID | H-010 / AIRTIME025 | project registry + video manifest |
| Run ID | `20260920-134309-h1-h010-airtime025-rerun` | 확인됨 |
| Environment | **PERSONAL** | metadata `mode=personal`, Brev/L40S |
| Fresh / resume | **resume / fine-tuning** | 확인됨 |
| Parent checkpoint | H-008 `model_2998.pt` | metadata |
| Parent SHA-256 | `d9a30c8a...1912ae` | metadata |
| Parent global iteration | 2998 | metadata |
| Requested additional iterations | 2000 | command / agent.yaml |
| Global final console iteration | 4997/4998 | console |
| Final saved checkpoint | `model_4997.pt` | checkpoint archive |
| Seed | 42 | agent.yaml |
| num_envs | 4096 | command |
| rollout steps/env | 24 | agent.yaml |
| headless | yes | command |
| camera during train | no camera flag | command |
| train start UTC | 2026-09-20 13:43:09 | metadata |
| train end UTC | 2026-09-20 14:10:52 | metadata |
| training time | 1635.79 s core; ~27m43s metadata wall | console / metadata |
| TensorBoard | 1 event file, 31 scalar tags, 주요 tag 2000 points | 직접 파싱 |
| console | global 2998→4997 전체 iteration block 존재 | 확인됨 |
| checkpoints | `model_3000`~`4900` 100-step 간격 + `4997`, 총 21 | 확인됨 |
| policy.pt / ONNX | **없음** | supplied train archive |
| report.html | 있음 | 확인됨 |
| evaluator | 없음 | supplied evidence |
| official score | 없음 | PERSONAL run |
| play/video | 별도 6-terrain suite 있음 | 확인됨 |

### 중요한 metadata 모순

`metadata.json`의 최상위 mode는 `personal`인데 `resume_lineage.official_resume`가 `true`다. 실제 실행 경로가 `/ephemeral/naver-issacsim-nvidia/...`, GPU가 L40S, official backup은 `skipped_no_config`이며 전체 metadata도 PERSONAL을 명시한다. 따라서 `official_resume=true`는 **field-level metadata inconsistency**로 취급하고 OFFICIAL 판정 근거로 사용하지 않는다.

이는 성능 분석을 invalid하게 만들 정도의 오류는 아니다. parent checkpoint path/hash, command, console, raw event, source identity가 서로 일치하기 때문이다.

## 2.2 archive 무결성

- Train archive outer SHA-256: `edc92686267b8df4c10880101ea7783a50ebf2f19affb5502216c96b249f2335`
- Video suite outer SHA-256: `e9025e750eda9822370a23a0e6a9a4ebd0dd3f1626d7c9679415fd05cf4c33e1`
- Train archive 내부 `SHA256SUMS`: 검증 통과
- Video suite 내부 `SHA256SUMS`: 6 MP4 모두 검증 통과
- `validation.json`: overall `PASS`
- source identity: train/play/reward/env cfg/agent cfg/finalize hash before/after 동일
- source mutation during run: false
- collection errors: 없음

## 2.3 네 가지 상태를 분리한 판정

1. **학습 프로세스 정상 종료:** PASS  
2. **evidence 보존:** PASS, 단 video→checkpoint linkage는 self-contained하지 않음  
3. **정책 성능:** 정상 locomotion 후보이나 matched control 대비 우월성 미확인  
4. **제출 후보 적합성:** 이 run은 PERSONAL이고 `policy.pt`가 없으므로 제출 후보 자체가 아님

---

# 3. Configuration Verification

## 3.1 실제 적용 reward

`source/humanoid_rewards.py`와 native run `params/env.yaml`은 다음 핵심 participant reward를 일치하게 기록한다.

| Reward | H-008 parent 설정 | H-010 실제 설정 | Delta |
|---|---:|---:|---:|
| `track_lin_vel_xy_exp` | 0.75 | 0.75 | 0 |
| `track_ang_vel_z_exp` | 0.50 | 0.50 | 0 |
| `feet_air_time` | **0.20** | **0.25** | **+0.05** |
| `termination_penalty` | -50 | -50 | 0 |
| `flat_orientation_l2` | -1.5 | -1.5 | 0 |
| `ang_vel_xy_l2` | -0.05 | -0.05 | 0 |
| `joint_deviation_hip` | -0.20 | -0.20 | 0 |
| `joint_deviation_torso` | -0.10 | -0.10 | 0 |
| `action_rate_l2` | -0.0005 | -0.0005 | 0 |

framework 기본 nonzero reward도 env.yaml에 유지된다.

- `dof_acc_l2=-1.25e-7`
- `dof_pos_limits=-1.0`
- `feet_slide=-0.25`
- `joint_deviation_arms=-0.2`

즉 **H-010 자체의 source/config에서는 의도한 single change가 맞다.**

## 3.2 PPO / runner 설정

- PPO
- 5 epochs
- 4 mini-batches
- initial LR `1e-3`, adaptive
- gamma `0.99`
- lambda `0.95`
- entropy coefficient `0.008`
- desired KL `0.01`
- clip `0.2`
- max grad norm `1.0`
- save interval `100`
- actor/critic MLP `512→256→128`, ELU
- action distribution: scalar Gaussian std parameter
- `check_for_nan=true`

PPO는 변경하지 않았다.

## 3.3 resume 해석 주의

이 실행은 fresh trajectory의 2999번째 iteration이 아니라 **checkpoint load 후 새 simulator/curriculum state에서 시작한 resume branch**다. 실제 첫 scalar가 이를 보여준다.

- iter 2998 terrain: 3.438
- episode length: 11.52
- XY error: 0.0128
- timeout 1.37%
- base-contact 0%

이 값들은 “부모 policy가 갑자기 완벽해졌다”는 뜻이 아니라 새 run 초기의 아직 episode 통계가 충분히 쌓이지 않은 상태다. 따라서 첫 수십 iteration과 이후 steady region을 직접 이어진 stationary time series처럼 해석하면 안 된다.

---

# 4. Training Dynamics

## 4.1 raw TensorBoard 전체 요약

TensorBoard raw event를 직접 TFRecord로 읽었으며 주요 학습 tag는 global step 2998→4997에 정확히 2,000개씩 존재한다.

### 주요 extrema

| Metric | Start | Peak / Min | Final |
|---|---:|---:|---:|
| mean reward | 0.017 | **6.585 @ 3044** | 4.027 |
| episode length | 11.52 | **896.58 @ 3044** | 734.56 |
| terrain | 3.438 | **5.716 @ 4742** | 5.643 |
| XY error | 0.0128* | max 0.378 @ 4004 | 0.3265 |
| yaw error | 0.0216* | max 1.613 @ 4004 | 1.3150 |
| base-contact | 0* | max 31.64% @ 3877 | 29.06% |
| timeout | 1.37%* | max 80.57% @ 3040 | 70.94% |
| mean action std | 1.476 | min 1.441 @ 3087 | 1.474 |

`*` resume 첫 iteration의 immature episode accumulator 값이므로 정책 성능 endpoint로 해석하지 않는다.

## 4.2 의미 있는 phase

### Phase A — Resume rewarm / curriculum re-entry: 2998~3040 전후

terrain이 3.438 → 최저 3.170 @3012로 잠깐 떨어진다. 동시에 episode length와 timeout이 빠르게 상승한다. start terrain을 다시 회복한 시점은 iter **3041**이다.

이 구간의 reward/episode peak는 정책 최종 성능보다 “쉬워진 curriculum + 새 episode accumulator의 빠른 포화” 효과가 강하게 섞여 있다. 또한 finalizer는 resume 추가 학습의 **첫 10%를 best 후보에서 제외**하므로, 이번 run에서는 대략 global 2998~3197이 자동 best 탐색 대상에서 제외된다.

### Phase B — terrain 재상승: 약 3041~3300

- terrain 4.0 최초 돌파: iter 3080
- terrain 5.0 최초 돌파: iter 3164
- terrain 5.5 최초 돌파: iter 3254
- terrain 5.6 최초 돌파: iter 3300

이 구간에서 정책은 resume reset 이후 높은 난이도로 빠르게 돌아간다.

### Phase C — high-terrain adaptation: 약 3300~4300

terrain 평균은 5.5 부근으로 안정되지만 base-contact은 약 28~31%에 머문다. 즉 “더 높은 terrain을 접하면서 낙상 비율이 0에 수렴”하는 형태가 아니라, 높은 난이도에서 약 70/30의 timeout/fall 균형을 유지하는 정책이다.

### Phase D — late plateau / slight XY recovery: 약 4300~4997

terrain은 5.65 부근에서 plateau하고 XY error는 약 0.33으로 약간 좋아진다. yaw error는 약 1.4로 남아 있다. terrain·XY·fall이 함께 무너지는 late regression은 없다.

## 4.3 구간 평균

| Window | Reward | Episode | Terrain | XY error | Yaw error | Base-contact | Std |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2998~3097 rewarm | 4.426 | 672.8 | 3.607 | 0.2808 | 1.1487 | 17.01% | 1.450 |
| 3098~3497 | 4.827 | 790.6 | 5.339 | 0.3420 | 1.3559 | 27.57% | 1.455 |
| 3498~4297 | 4.412 | 772.2 | 5.562 | 0.3394 | 1.4264 | 29.90% | 1.467 |
| 4298~4797 | 4.359 | 772.5 | 5.653 | 0.3338 | 1.4431 | 29.81% | 1.481 |
| **last-500 4498~4997** | **4.475** | **773.7** | **5.663** | **0.3318** | **1.4187** | **29.63%** | **1.480** |
| last-200 | 4.588 | 773.2 | 5.659 | 0.3294 | 1.3861 | 29.66% | 1.478 |

후기 500회와 200회가 유사하므로 final 한 점의 우연한 spike가 아니라 plateau 상태라고 보는 근거가 강하다.

---

# 5. Tracking Analysis

## 5.1 Linear / XY tracking

late XY error는 약 **0.33**이다.

- last-500 mean: **0.33175**
- last-200 mean: **0.32938**
- final: **0.32645**

후반으로 갈수록 terrain은 높은 상태를 유지하면서 XY error가 소폭 개선된다. 3500 이후 terrain과 XY error의 단순 correlation은 약 **-0.35**로, 이번 run에서는 terrain이 높아졌다고 linear tracking이 악화되는 정황은 없다. 단, 같은 trajectory 내부 correlation은 인과 효과가 아니다.

### matched `.20` control과 비교

기존 H-008 unchanged +2K continuation의 late console summary:
- terrain 5.604
- XY 0.3314
- base-contact 29.67%

H-010:
- last-500 terrain 5.663
- XY 0.3318
- base-contact 29.63%

이 차이는 **실질적으로 동일 범위**다. 특히 XY는 거의 변화가 없다.

따라서 `feet_air_time +0.05`가 linear tracking을 개선했다고 볼 수 없다.

## 5.2 Forward vs lateral

TensorBoard에는 XY aggregate error만 있고 forward(x)와 lateral(y)이 별도 scalar로 기록되지 않았다. 영상에도 command telemetry가 없으므로 forward/lateral을 수치적으로 분리할 수 없다.

**판정: 판단 불가.**

## 5.3 Yaw / turning

- last-500 yaw error: **1.4187**
- last-200: **1.3861**
- final: **1.3150**
- high-terrain middle/late는 대체로 1.35~1.45

이는 이 run의 명확한 내부 tracking 병목이다. `track_ang_vel_z_exp` reward component도 last-500 평균 약 `+0.1168`에 머문다.

다만 이것은 PERSONAL training metric이다. 과거 공식 TERM50 score에서는 회전 복합이 특별히 최악의 official scenario는 아니었으므로, 이 값을 공식 점수의 직접 병목으로 치환하지 않는다.

## 5.4 Stop behavior

zero-command drift, 정지 후 흔들림, 재출발 안정성의 isolated evaluator/telemetry가 없다. 여섯 terrain 영상은 command vector가 화면에 보이지만 정확한 time-aligned numeric command와 base velocity가 저장되지 않았다.

**판정: 판단 불가.**

---

# 6. Stability Analysis

## 6.1 fall / survival

last-500:
- base-contact: **29.63%**
- timeout: **70.37%**
- episode length: **773.65 / max 1000 step scale**

이는 “거의 안 넘어지는 정책”은 아니다. 약 30%의 episode가 base-contact termination으로 끝난다. 그러나 Go2 G5에서 관찰된 “누운 채 timeout하는 생존형 local optimum”과 달리 영상에서 upright locomotion이 확인되고 terrain도 5.66까지 유지되므로 단순 생존 hacking 정황은 약하다.

## 6.2 terrain progression

- resume start: 3.438
- min: 3.170 @3012
- start 값 회복: 3041
- terrain 5.0: 3164
- 5.5: 3254
- peak: **5.716 @4742**
- last-500 mean: **5.663**
- final: 5.643

중요한 점은 peak가 4742이고 후반 평균도 5.66이라서, terrain peak 후 급락하지 않았다는 것이다.

Curriculum level은 4096 env의 평균 난이도이며 “level 5.7을 완전히 정복”했다는 뜻은 아니다.

## 6.3 posture / angular stability

last-500 reward contribution:
- `flat_orientation_l2`: -0.0138
- `ang_vel_xy_l2`: -0.0267
- `feet_slide`: -0.0490
- `joint_deviation_hip`: -0.0372
- `joint_deviation_torso`: -0.00619

중후반에 이 값들이 폭발하는 패턴은 없다. video frame sampling에서도 torso가 지속적으로 누워 있거나 비정상 자세로 정지하는 모습은 보이지 않는다.

## 6.4 recovery / push recovery

push evaluator가 없다. 영상은 terrain traversal만 있고 외부 push recovery trial이 아니다.

**판정: 판단 불가.**

---

# 7. Reward Component Analysis

## 7.1 핵심 late reward component

last-500 mean:

| Component | Mean |
|---|---:|
| `track_lin_vel_xy_exp` | +0.4817 |
| `track_ang_vel_z_exp` | +0.1168 |
| `feet_air_time` | +0.01077 |
| `action_rate_l2` | -0.07456 |
| `ang_vel_xy_l2` | -0.02665 |
| `flat_orientation_l2` | -0.01380 |
| `feet_slide` | -0.04905 |
| `joint_deviation_hip` | -0.03719 |
| `joint_deviation_torso` | -0.00619 |
| `termination_penalty` | -0.01987 |
| `dof_acc_l2` | -0.05545 |
| `joint_deviation_arms` | -0.09793 |

## 7.2 AIRTIME025가 실제로 무엇을 바꿨나

`feet_air_time` reward contribution은 resume 초기 거의 0에서 high-terrain 구간에 약 0.009~0.011로 올라간다. 이는 로봇이 swing phase를 활용하고 있다는 정황이다.

하지만 **weight가 0.20→0.25로 25% 증가했으므로 component 절댓값 자체는 동일 behavior에서도 커질 수 있다.** 따라서 reward component 값 증가를 행동 개선으로 직접 해석하면 안 된다.

행동에 가까운 terrain/XY/fall의 matched control 비교가 사실상 동일하므로, 현재 evidence에서 `0.25`가 “발을 더 잘 들어 obstacle capability를 개선했다”는 인과 주장은 지지되지 않는다.

## 7.3 trade-off

관찰 가능한 trade-off는 다음과 같다.

- 높은 terrain 유지 ↔ base-contact 약 30% 지속
- XY tracking은 후기 소폭 회복 ↔ yaw는 1.4 수준 병목 유지
- `feet_air_time` 증가 ↔ hopping 증거는 없음
- action-rate penalty contribution은 약 -0.075로 크지만 후반 폭증하지 않음

즉 이번 변경은 새로운 “공격적 gait”를 만든 것보다, 기존 H-008 policy의 성격을 거의 유지한 채 AIRTIME reward의 weighting만 약간 바꾼 것으로 보인다.

---

# 8. PPO / Numerical Stability

## 8.1 value loss

raw TensorBoard `Loss/value`:

- median: **0.006462**
- p95: **0.007117**
- p99: **0.007458**
- p99.9: **0.007852**
- max: **0.019326 @ 2998**
- `>=0.01`: 2 points
- `>=0.02`: 0
- `>=0.1`: 0
- `>=1`: 0
- `>=10`: 0

max가 resume 첫 step에 있고 즉시 낮아진다. 반복 spike나 발산 전조는 없다.

## 8.2 surrogate / entropy / LR / std

- surrogate loss는 정상 범위에서 움직이며 NaN/Inf 없음
- adaptive LR은 resume 직후 `1e-5`에서 이후 약 `1.7e-4~2.6e-4` 구간을 주로 사용
- mean action std: 약 1.44→1.48, final 1.474
- std가 낮아지는 전형적인 “exploration collapse”는 없음

중요: std가 1.47이라고 해서 학습 실패로 판정할 수 없다. episode/terrain/tracking/video가 모두 기능적 locomotion을 보여주기 때문이다. `report.html`의 “1.0 근처면 거의 학습 안 됨” 경고는 이 run에 기계적으로 적용하기 어렵다.

## 8.3 checkpoint tensor finite 검사

21개 보존 checkpoint에 대해 actor, critic, optimizer state를 재귀적으로 검사했다.

- finite: **21/21**
- actor std parameter: 모든 checkpoint에서 finite
- final `model_4997`: std param min 약 0.188, max 약 2.550, mean 약 1.474

수치적 failure evidence 없음.

## 8.4 throughput / GPU

training scalar 기준 steady iteration은 대략 0.8초 수준이며, console 마지막은 약 123.8k steps/s다.

GPU telemetry 822 samples:
- utilization mean 51.6%, median 52%, p95 61%, max 67%
- VRAM median/max 5240 MiB
- power mean 152.8 W, max 166.4 W
- temperature median 45°C, max 46°C

OOM, thermal throttling, memory saturation 정황 없음.

---

# 9. Checkpoint Analysis

## 9.1 automatic best 규칙 검증

직접 확인한 hash:

- `collected/exported/model_best.pt`
  - SHA-256 `0479e755...b47e80`
  - **`model_3300.pt`와 exact hash match**

report/finalizer:
- best reward **5.783 @ iter 3299**
- → `model_3300.pt`

raw TensorBoard 전체:
- **global raw max reward 6.585 @ iter 3044**

하지만 resume finalizer는 추가 학습 구간의 **첫 10%를 best 후보에서 제외**한다. 이번 run은 +2,000 iteration이므로 약 첫 200회(global 약 2998~3197)가 제외된다.

이 exclusion을 적용해 raw event를 다시 계산하면:
- **eligible raw max reward 5.7827835 @ iter 3299**
- report 표시 **5.783 @ iter 3299**
- 선택 checkpoint **model_3300.pt**

즉 **report/finalizer 선택은 raw TensorBoard와 일치한다.**

### 왜 중요한가

iter 3044의 6.585는 전체 raw 곡선의 최고점이지만 자동 best selector의 후보가 아니며, 실제로도 resume 재적응 초기다:
- terrain 약 3.49
- episode length 896.6
- timeout 약 79.5%
- curriculum 재상승 초기

따라서 10% exclusion은 resume 직후의 비정상적으로 유리한/미성숙한 통계가 `model_best`를 차지하는 것을 막는 역할을 한다. 다만 `model_best=model_3300` 역시 **training reward 기준 eligible best**라는 뜻이지 terrain/tracking/stability를 종합한 실제 정책 최적점이라는 뜻은 아니다.

## 9.2 대표 checkpoint

후기:
- terrain plateau 유지
- XY error 악화 없음
- base-contact 급증 없음
- value loss 안정
- final checkpoint finite
- 6-terrain 영상이 “model_4997”로 관리됨

따라서 **학습 대표 checkpoint는 `model_4997.pt`**로 두는 것이 가장 일관적이다.

SHA-256:
`65bb008d1c5617691eb57877e113455bd8d8359f8c922403dd02c03ffa581b2d`

단, 영상 bundle에는 checkpoint bytes/hash linkage가 없으므로 영상이 실제로 이 exact checkpoint에서 렌더됐다는 것은 manifest assertion 수준이다.

---

# 10. Video / Behavioral Analysis

## 10.1 video integrity

6개 모두:
- H.264
- 1920×1080
- 50 fps
- 999 frames
- 19.98 s

MP4 hash는 `SHA256SUMS` 및 `video_suite_manifest.json`과 일치한다.

## 10.2 terrain별 관찰

### boxes

샘플 프레임에서 로봇이 큰 box 단차가 있는 영역 내부를 통과하면서 upright를 유지한다. 무릎 굴곡과 스텝 높이 변화가 보이며, 한 발만 지속적으로 든 채 깡충대는 형태는 보이지 않는다. 장면 후반에도 쓰러진 상태로 유지되지 않는다.

**해석:** AIRTIME 0.25에서 명백한 hopping reward hacking은 관찰되지 않음. 큰 단차에서 locomotion sanity는 통과.

### stairs

계단 영역으로 접근하고 계단과 겹치는 구간을 지나며 upright를 유지한다. 영상 샘플에서는 넘어져 reset되는 명백한 장면이 없다.

### inverted stairs

불연속 단차를 지나가는 동안 upright locomotion이 유지된다. 지속적인 한쪽 다리 고정이나 누운 자세 생존은 보이지 않는다.

### random rough

불규칙 rough patch에서 body가 기울고 다리 동작이 커지지만 upright를 유지한다. 정적 survival이 아니라 실제로 위치가 변한다.

### slope +10° / -10°

경사 위에서 upright locomotion을 유지한다. 과도한 점프나 즉시 fall은 sampled trajectory에서 관찰되지 않는다.

## 10.3 영상으로 확인할 수 없는 것

- 정확한 forward/lateral/yaw tracking error
- zero-command drift
- trial success rate
- fall probability
- push recovery
- 같은 terrain 반복 재현성
- H-008 `.20` control 대비 causal improvement
- 영상이 exact `model_4997.pt`에서 생성됐다는 cryptographic proof

따라서 영상은 **local optimum / obvious gait failure를 거르는 qualitative sanity check**로만 사용한다.

---

# 11. Baseline / Parent Comparison

## 11.1 가장 중요한 비교: H-008 unchanged +2K control

H-010의 설계상 가장 좋은 control은 H-008 3K final `model_2998`에서 reward를 바꾸지 않고 2K 더 학습한 기존 H-008 continuation이다. parent checkpoint가 같고 training length도 같다.

| Metric | H-008 unchanged +2K control | H-010 AIRTIME025 | 해석 |
|---|---:|---:|---|
| parent | same `model_2998` | same `model_2998` | 강한 비교 구조 |
| `feet_air_time` | 0.20 | 0.25 | 유일한 의도 delta |
| late terrain | 5.604 (project late console summary) | 5.663 last-500 | 매우 작은 차이 |
| late XY error | 0.3314 | 0.3318 last-500 | 사실상 동일 |
| late base-contact | 29.67% | 29.63% last-500 | 사실상 동일 |
| final checkpoint | 4997 | 4997 | 동일 global endpoint |
| OFFICIAL | no | no | 둘 다 PERSONAL |

엄밀히 같은 aggregation window가 완전히 확보된 것은 아니므로 소수점 차이를 effect size로 해석하지 않는다. 현재 수준에서는 **no clear material improvement**가 가장 안전한 결론이다.

## 11.2 H-005 GAIT025와의 관계

H-005도 `feet_air_time 0.20→0.25`를 실험했지만 parent가 H-001 `model_1499`이고 +1.5K branch였다. H-010은 H-008 3K `model_2998` parent에서 +2K이므로 **같은 reward delta라도 policy state가 다르다.**

따라서 H-005와 H-010을 합쳐 “0.25가 반복적으로 좋다”고 주장할 수 없다. H-005 역시 unchanged `.20` control 부족 때문에 HOLD였고, 이번 H-010은 오히려 같은-parent `.20` continuation과 비교했을 때 차이가 매우 작다.

## 11.3 공식 TERM50 5K와의 관계

공식 TERM50 5K는 다른 server/environment와 더 이른 lineage다. 공식 endpoint:
- terrain 5.825
- base-contact 28.93%
- XY 0.378
- yaw 0.935
- 공식 sim 56.37/70

이 숫자는 historical anchor일 뿐 H-010과 paired causal comparison이 아니다. 특히 H-010은 PERSONAL이고 이미 `track_lin_vel_xy_exp=0.75` lineage 위에 있다.

---

# 12. Tracking vs Stability Trade-off

현재 H-010은 다음 성격에 가깝다.

- **Linear tracking:** 유지 / 약한 후기 회복
- **Yaw tracking:** 여전히 약함
- **Stability:** high-terrain에서 약 70% timeout, 30% base-contact로 유지
- **Terrain:** 높은 plateau
- **Gait:** 영상상 upright, active locomotion, obvious hopping 없음
- **Smoothness:** action-rate가 악화 폭발하지는 않으나 penalty contribution은 여전히 큼

H-008 unchanged control과 비교하면 명확한 `Tracking ↑ / Stability ↑`는 아니다. 가장 정확한 표현은:

> **Tracking ≈ / Stability ≈, gait reward만 높였지만 behavior-facing metrics는 거의 그대로.**

---

# 13. Local Optimum / Reward Hacking Check

| 가능성 | 판정 | 근거 |
|---|---|---|
| 움직이지 않고 생존 | 낮음 | terrain 영상에서 실제 이동 |
| 누운 자세로 timeout | 낮음 | 영상에서 upright |
| hopping | 뚜렷한 증거 없음 | boxes/rough 포함 sampled frames에서 지속 한발 hopping 없음 |
| 한 발 오래 들기 | 뚜렷한 증거 없음 | sampled frames |
| sliding | 정량 판단 불가 | feet_slide penalty는 존재하나 영상 telemetry 없음 |
| command 무시 | 판단 불가 | numeric command/base velocity 없음 |
| terrain 회피 | 낮음~중간 | 지형 내부 진입은 보이나 traversal 목표/heading 고정 아님 |
| 지나친 소극성 | 낮음 | 적극적 이동 관찰 |
| episode length만 긴 local optimum | 낮음 | terrain progression + actual locomotion |
| AIRTIME reward 하나만 과도 최적화 | 근거 없음 | component small, behavior metrics 거의 control과 동일 |

가장 큰 위험은 reward hacking이 아니라 **“변경했지만 실제 behavior가 거의 변하지 않은 neutral delta”**다.

---

# 14. Key Findings

1. **H-010은 실행/증거 무결성 측면에서 좋은 run이다.** exit 0, validation PASS, raw event/console/21 checkpoint/source hash/GPU telemetry가 모두 보존됐다.
2. **resume 초반 약 60 iteration은 정상적인 재적응 구간이다.** terrain 3.17까지 떨어졌다가 3041에 시작값을 회복하고 3164에 5.0, 3254에 5.5를 넘어섰다.
3. **후기 policy는 high-terrain plateau에 도달했다.** last-500 terrain 5.663, XY 0.3318, base-contact 29.63%, episode 773.7.
4. **`feet_air_time=0.25`의 인과적 개선 증거는 거의 없다.** 같은 parent + same +2K `.20` control과 terrain/XY/fall이 사실상 같다.
5. **반대로 AIRTIME025가 hopping을 유발했다는 증거도 없다.** six-terrain video에서 upright locomotion이 보이며 persistent hopping/lying survival은 관찰되지 않았다.
6. **yaw tracking은 여전히 내부 병목이다.** last-500 yaw error 1.419.
7. **PPO는 매우 안정적이다.** value loss p99 0.00746, max 0.0193(첫 resume step), NaN/Inf/optimizer failure 없음.
8. **automatic model_best 선택은 규칙상 정상이다.** resume 첫 10%를 제외하면 raw eligible maximum이 5.783@3299로 report와 일치한다. 다만 이는 training reward 기준 selector이므로 실제 대표 policy 선택은 late terrain/tracking/fall까지 함께 봐야 한다.
9. **final `model_4997`이 대표 checkpoint다.** late terrain/tracking/fall의 joint collapse가 없고 final tensor finite다.
10. **현재 병목은 AIRTIME 부족보다 yaw 및 약 30% base-contact이다.** AIRTIME 0.25는 그 두 문제를 의미 있게 바꾸지 않았다.

---

# 15. Final Decision

## **HOLD**

### 근거

- PROMOTE하기에는 same-parent `.20` control 대비 효과가 너무 작다.
- REJECT하기에는 수치적/행동적 부작용이 명확하지 않고 terrain locomotion도 정상이다.
- INVALID가 아닌 이유는 train archive 자체의 lineage/config/evidence가 충분히 검증되었기 때문이다.
- 다만 VIDEO provenance는 checkpoint exact-hash 연결이 없으므로 영상 evidence만 독립적으로 강한 provenance라고 보지는 않는다.

### 실무적 의미

`feet_air_time=0.25`를 다음 parent 기본값으로 승격시키지 않는다. 더 긴 AIRTIME025 continuation도 우선순위가 낮다. 현재 evidence는 `.20`과 `.25`가 이 lineage에서 behavior-facing metrics에 거의 같은 결과를 낸다는 쪽에 가깝다.

---

# 16. Next Experiment

## 1순위 — H-011: `joint_deviation_hip -0.20 → -0.10`, same-parent +2K resume

### 왜 이게 가장 정보 효율적인가

H-010으로 AIRTIME 축의 작은 증가가 거의 neutral임을 확인했다. 한편 H-009는 같은 H-008 `model_2998` parent에서 **반대 방향**인 `joint_deviation_hip -0.20→-0.30`을 이미 완료했고 분석이 pending이다.

따라서 먼저 H-009 archive 분석을 끝낸 뒤, H-011을 실행하면:

- `-0.30`
- control `-0.20`
- `-0.10`

의 대칭적인 local sensitivity를 같은 parent에서 볼 수 있다. 이는 새로운 축 하나를 무작정 여는 것보다 훨씬 많은 정보를 준다.

### 설계

| 항목 | 제안 |
|---|---|
| Parent | H-008 `model_2998.pt` SHA `d9a30c8a...1912ae` |
| Reward 변경 | `joint_deviation_hip -0.20 → -0.10` only |
| Other rewards | H-008 parent와 동일 |
| Additional iterations | 2,000 |
| Global target | 2998→4997 |
| seed | 42 |
| envs | 4096 |
| rollout | 24 |
| PPO | unchanged |
| mode | PERSONAL screening |
| train | headless/no camera |
| video | final checkpoint 별도 6-terrain |

### 기대 효과

hip deviation penalty를 약하게 하면 다리/골반 자유도가 늘어:
- lateral/turning adaptation
- obstacle step placement
- gait amplitude

가 좋아질 가능성이 있다.

### 예상 부작용

- 좌우 흔들림 증가
- 비대칭 gait
- base-contact 증가
- action-rate 증가
- yaw/terrain 불안정

### 사전 성공 기준 — 내부 screening heuristic

공식 기준이 아니라 다음 branch 비교를 위한 사전 기준으로 사용한다.

H-008 `.20` control 대비 last-500에서:
- terrain이 **5.55 이상 유지**
- base-contact이 **31%를 지속적으로 넘지 않음**
- XY error가 **0.32 이하** 또는 yaw error가 **1.30 이하**로 의미 있게 개선
- improvement가 endpoint 한 점이 아니라 last-500/last-200 모두에서 유지
- value loss 반복 spike/NaN/Inf 없음
- video에서 hip looseness가 hopping/sliding/oscillation으로 바뀌지 않음

한 metric만 좋아지고 stability가 나빠지면 HOLD/REJECT한다.

### 가장 먼저 해야 할 것

**새 학습 전에 H-009 archive를 먼저 완전 분석한다.** H-009가 이미 `-0.30` 방향을 측정했으므로 이를 보지 않고 H-011을 돌리면 정보 설계의 절반을 버리는 셈이다.

## 2순위 — yaw micro-adjustment

H-009/H-011 hip sweep 결과가 neutral이라면 `track_ang_vel_z_exp 0.50→0.60`의 작은 one-change branch를 검토할 수 있다. 과거 `0.75` standalone 실패가 있으므로 큰 jump는 피한다. 단, official score에서 yaw가 가장 큰 점수 공백은 아니었으므로 H-011보다 우선하지 않는다.

---

# 17. Confidence & Limitations

## 17.1 강한 근거

- run identity / command / parent hash
- PERSONAL classification
- single intended reward delta
- 2,000 raw scalar points
- 21 checkpoint hash/finite status
- TensorBoard metrics와 last-window 통계
- resume 첫 10% exclusion을 적용한 report/finalizer 선택과 raw event의 일치
- train archive SHA integrity
- video files hash/codec/duration
- supplied six-terrain footage에서 upright locomotion이 존재

## 17.2 중간 근거

- H-010 `.25`가 H-008 `.20` control보다 실질적으로 낫지 않다는 결론  
  - 이유: 같은 parent/길이의 매우 좋은 control이지만, project에 남은 H-008 숫자는 동일한 raw last-500 table 전체가 아니라 late summary이므로 소수점 effect size까지 엄밀히 paired statistical comparison은 아니다.
- video에서 hopping이 없다는 판정  
  - 6 terrain × 단일 19.98s trajectory의 qualitative observation이다.

## 17.3 약한 정황 / 가설

- AIRTIME가 이 lineage에서 이미 포화되어 0.20→0.25가 behavior를 거의 바꾸지 못했다는 해석.
- yaw bottleneck의 원인이 hip/gait freedom이나 turn reward 부족이라는 해석.

## 17.4 판단 불가

- forward vs lateral 별도 tracking
- stop command drift
- push recovery
- repeated terrain success rate
- official scenario score
- multi-seed generalization
- video exact checkpoint cryptographic linkage
- final `policy.pt` submission identity
- automatic reward-best가 실제 evaluator/공식 시나리오 최적 checkpoint와 일치하는지 여부

## 17.5 single-seed 경계

seed 42 단일 run이다. 이 결과는 같은 lineage에서 강한 방향성 screening으로는 의미가 있지만, 통계적 개선·최적값·일반화를 주장할 수 없다.

---

# 18. Provenance / 사용한 근거

## 직접 분석한 사용자 제공 archive

1. `20260920-134309-h1-h010-airtime025-rerun.tar.gz`
   - outer SHA-256 `edc92686267b8df4c10880101ea7783a50ebf2f19affb5502216c96b249f2335`
   - `metadata.json`
   - `validation.json`
   - `command.txt`
   - full `console.log`
   - native TensorBoard event
   - `params/env.yaml`
   - `params/agent.yaml`
   - `source/humanoid_rewards.py`
   - source identity hashes
   - 21 numbered checkpoints
   - GPU telemetry
   - exported env/model_best/report

2. `h1-h010-airtime025-model4997-6terrain-video-suite-20260920.tar.gz`
   - outer SHA-256 `e9025e750eda9822370a23a0e6a9a4ebd0dd3f1626d7c9679415fd05cf4c33e1`
   - boxes
   - stairs
   - inverted stairs
   - random rough
   - slope +10°
   - slope -10°
   - manifest + SHA256SUMS

## Project comparison sources

- `14_H1_NEXT_RUN_PARAMETER_COMPARISON`
  - H-008/H-009/H-010/H-011 lineage
  - H-008 unchanged +2K late summary
- `15_OPTUNA_REWARD_DECISION_ENGINE`
  - H-005~H-011 experiment framing
- `16_EXPERIMENT_EXPORT_AND_TENSORBOARD`
  - evidence/checkpoint selection rules
- `18_H1_FINALIZE_REPORT_LIMITATIONS`
  - H1 finalize/report 자동 선택의 한계와 checkpoint 해석 주의
- `13_H1_OFFICIAL_SERVER_BASELINE_EVIDENCE`
  - official TERM50 anchor and Round-2 score

Project 문서는 이전 archive 분석을 요약한 secondary evidence이며, H-010 자체의 값은 이번에 받은 raw archive를 직접 재계산한 값을 우선했다.

---

# 19. 최종 질문에 대한 직접 답

1. **이 정책은 무엇을 배웠는가?**  
   H-008의 linear-tracking 강화 policy를 유지하면서 resume reset 뒤 high-terrain locomotion으로 빠르게 재적응했다. terrain 5.6대에서 약 70% timeout, 30% base-contact의 보행을 유지한다.

2. **이전 정책보다 무엇이 실제로 좋아졌는가?**  
   같은 parent `.20` +2K control 대비 확실히 좋아졌다고 말할 지표가 없다. terrain이 약간 높아 보이지만 XY/fall은 사실상 같다.

3. **무엇을 잃었는가?**  
   명확히 잃은 것도 확인되지 않는다. hopping이나 stability collapse는 없다. yaw 병목은 계속 남아 있다.

4. **학습 중 언제 중요한 변화가 일어났는가?**  
   3012 terrain 최저 → 3041 resume 시작값 회복 → 3164 terrain 5.0 → 3254 5.5 → 4300 이후 5.65 plateau.

5. **높은 지표가 실제 행동 개선을 의미하는가?**  
   반드시 그렇지 않다. raw 전체 peak 3044는 resume 첫 10% 제외 규칙 때문에 자동 best 후보도 아니며 curriculum 재적응 구간이다. 10% exclusion 뒤 선택된 3299/model_3300도 training reward 기준 best일 뿐이므로 영상과 late window가 더 중요하다.

6. **현재 가장 큰 병목은 무엇인가?**  
   내부적으로 yaw error ~1.4와 base-contact ~30%. AIRTIME 부족은 현재 자료에서 주 병목으로 보이지 않는다.

7. **이 가설은 계속 실험할 가치가 있는가?**  
   AIRTIME025 자체는 HOLD. 더 길게 연장할 우선순위는 낮다.

8. **다음 한 번의 학습으로 가장 많은 정보를 얻으려면?**  
   H-009 `hip -0.30` 분석을 먼저 끝내고, 같은 H-008 parent에서 H-011 `hip -0.10` +2K를 실행해 `-0.30 / -0.20 / -0.10` local sensitivity를 완성한다.

---

**종합 신뢰도:** 높음. H-010 자체 수치/무결성/수치안정성 분석은 raw archive 직접 재계산 기반이다. H-008 control 비교와 video checkpoint provenance에는 명시한 한계가 있다.
