> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/incoming/other/reviewed/H1_H011_HIPDEV010_MODEL4997_DEEP_ANALYSIS.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# H1 H-011 HIPDEV010 (model_4997) Deep Analysis

- 분석 대상: `20260920-150652-h1-h011-hipdev010.tar.gz`
- 영상 묶음: `h1-h011-hipdev010-model4997-6terrain-video-suite-20260920.tar.gz`
- 분석 시점: 2026-09-21
- 핵심 가설: H-008 3K final `model_2998.pt`에서 `joint_deviation_hip`만 `-0.20 → -0.10`으로 완화하면, H-008의 linear tracking/stability를 유지하면서 골반/하지 움직임 제약을 줄여 지형·보행 성능을 개선할 수 있는가?
- 환경 분류: **PERSONAL / Brev L40S**. 공식 제출 성능 근거가 아님.
- 최종 판정: **HOLD**

> 판정 용어: **확인됨** = 원본 artifact에서 직접 검증, **강한 정황** = 여러 독립 지표가 같은 방향, **가설** = 가능한 설명이나 인과 미확정, **판단 불가** = 현재 자료로 검증 불가.

---

# 1. Executive Summary

이번 H-011은 새 fresh training이 아니라, 이미 검증된 H-008 3K final `model_2998.pt`에서 **2,000 iteration을 추가한 resume fine-tuning**이다. parent checkpoint SHA-256은 `d9a30c8a117f69cac49c4e640500f0fa8d88de72d6c61855f1e147ea6c1912ae`로 기존 H-008 lineage 기록과 일치하며, 이번 branch에서 의도한 reward 변경은 `joint_deviation_hip -0.20 → -0.10` 하나다. 학습은 exit code 0으로 정상 종료했고 TensorBoard 2,000 scalar step, console 전체, 21개 checkpoint mirror, source hash, GPU telemetry가 보존되었다. evidence validation은 PASS다.

정책은 resume 직후 curriculum/episode 통계가 재형성되는 강한 transient를 거친 뒤, 대략 global iteration 3.2K~3.5K 이후 **terrain 5.5~5.7, XY error 약 0.33, base-contact 약 29~30%, episode length 약 770~790**의 장기 plateau에 들어갔다. 후반 300회 평균은 terrain `5.661`, XY error `0.3304`, base-contact `29.02%`, timeout `70.99%`, episode length `780.24`로, 같은 H-008 parent에서 reward 변경 없이 5K까지 연장한 기존 control 요약(`terrain 5.604`, `XY 0.3314`, `base-contact 29.67%`)과 비교하면 차이는 **매우 작다**. 즉 less-negative hip penalty가 명확한 tracking/stability 이득을 만들었다는 증거는 아직 없다.

가장 중요한 부작용 후보는 yaw다. H-011 후반 300회 yaw error 평균은 `1.411`, endpoint `1.445`이며, 최대 `1.639 @ 4546`까지 올라간다. H-008 계열에서 이미 yaw trade-off가 알려져 있었으므로, H-011은 이를 해소하지 못했다. 반면 PPO 수치 안정성은 매우 좋다. value loss는 median `0.00639`, p95 `0.00706`, p99 `0.00742`, max `0.01358`이며 NaN/Inf/OOM/optimizer failure가 없다. action std도 후반 약 `1.47`로 안정적이고 반복 발산 신호가 없다.

full raw TensorBoard의 전 구간 최고는 **`6.886 @ 3084`**이지만, 이것은 finalizer가 best 후보에서 제외하는 **resume 구간 첫 10% warm-up 영역**에 있다. 이번 추가 학습은 2998→4997의 2,000 iteration이므로 첫 약 200회(대략 global 2998~3197)는 best 후보에서 제외되며, `3084`는 시작점 대비 +86회(약 4.3%)라 선택 대상이 아니다. report/finalizer의 **`6.184 @ 3203` → `model_3200.pt` 선택은 이 10% 제외 규칙과 일치**한다. 따라서 이번 run에서는 raw 전구간 최고와 report best의 차이를 finalizer mismatch/bug로 해석하면 안 된다. 다만 `model_best`는 어디까지나 허용된 후보 구간 안의 training-reward 기준 자동 선택이므로, 실제 행동/지형/추종 관점의 최적 정책을 뜻하지는 않는다. 충분히 긴 resume에서 final numbered checkpoint를 대표값으로 쓰는 기존 원칙은 별개의 이유로 유지된다.

6-terrain 영상은 모두 19.98초, H.264 1920×1080 50 fps로 checksum이 맞는다. 샘플링 프레임에서는 boxes, random rough, stairs, inverted stairs, ±10° slope에서 로봇이 upright locomotion을 유지하는 모습이 확인되며 명백한 누운 자세나 정지형 reward hacking은 보이지 않는다. 다만 영상 bundle은 checkpoint bytes나 source hash를 포함하지 않고 `model_4997` 연결은 manifest의 assertion이므로, **정성 sanity evidence**이지 checkpoint provenance·성공률·tracking 측정·공식 평가가 아니다.

결론적으로 H-011은 **실패 정책은 아니지만, `joint_deviation_hip=-0.10`의 우월성을 보여 주지도 못했다.** 가장 정보 효율적인 다음 조치는 새 학습을 즉시 추가하는 것이 아니라, 이미 존재하는 sibling H-009 (`-0.30`) evidence를 동일 방식으로 분석하여 `-0.30 / -0.20(control) / -0.10`의 같은-parent 3점 비교를 완성하는 것이다. 세 branch의 추가 학습량과 evaluator 조건이 맞는 경우에만 hip penalty 방향성을 판단해야 한다.

---

# 2. Run Identity & Evidence Integrity

## 2.1 확정된 실험 정체성

| 항목 | 확인 결과 | 근거/해석 |
|---|---|---|
| Robot / task | **H1 / `Humanoid-v0`** | command, env, source |
| Experiment ID | **H-011 / HIPDEV010** | run name + video manifest + 프로젝트 registry 맥락 |
| Run ID | `20260920-150652-h1-h011-hipdev010` | `metadata.json` |
| Environment | **PERSONAL** | `metadata.json: mode=personal`, Brev L40S |
| Training type | **resume / fine-tuning** | `--resume --load_run H008_PARENT_2998_STAGE --checkpoint model_2998.pt` |
| Parent | H-008 3K final `model_2998.pt` | metadata lineage |
| Parent SHA-256 | `d9a30c8a117f69cac49c4e640500f0fa8d88de72d6c61855f1e147ea6c1912ae` | metadata, 기존 H-008 기록과 일치 |
| Requested additional iterations | **2000** | command / agent.yaml |
| Global start iteration | **2998** | resume lineage + first scalar |
| Last console iteration | **4997/4998** | full console |
| Last saved checkpoint | **`model_4997.pt`** | checkpoint mirror |
| Seed | **42** | agent/env yaml |
| num_envs | **4096** | command/env |
| rollout | **24 steps/env/iteration** | agent.yaml |
| transitions/iteration | **98,304** | 4096×24 |
| additional transitions | **196,608,000** | console final total steps for this resumed segment |
| headless | **yes** | command |
| camera during training | 확인되는 활성 video/camera flag 없음 | 학습 command 기준 |
| start/end UTC | 2026-09-20 15:06:52.749 → 15:34:04.477 | metadata |
| wall time | 약 **27m 11.7s** | metadata |
| training time | **1608.23 s (26m 48.2s)** | console |
| TensorBoard | **존재, 1 event, 31 scalar tags, 각 핵심 tag 2000점** | raw event 직접 파싱 |
| console | **전체 2000 iteration 존재** | 2998~4997 파싱 |
| checkpoint preservation | **21개: 3000~4900/100 + 4997** | archive |
| play/video | **별도 6-terrain suite 존재** | video archive |
| evaluator | **없음** | artifact에 evaluator 결과 없음 |
| 공식 평가 | **없음** | PERSONAL run |

### 중요한 identity 해석

- 이 실행은 H-008의 **별도 5K continuation을 다시 이어간 run이 아니다.** 같은 H-008 3K final `model_2998`에서 직접 갈라진 sibling branch다.
- 따라서 H-011의 global iteration 4997은 “H-008 5K + H-011 추가”가 아니라, **H-008 3K parent + H-011 2K**다.
- `model_best.pt`라는 파일명은 identity 근거가 아니다. 이번 archive에서 `model_best.pt`는 hash상 `model_3200.pt`와 동일하다.

## 2.2 실행 성공, evidence, 정책 품질, 제출 적합성 분리

| 질문 | 판정 | 이유 |
|---|---|---|
| 학습 프로세스 정상 종료? | **YES** | exit code 0, console 4997까지 완료 |
| evidence 정상 보존? | **YES (PASS)** | SHA256SUMS 검증, event/console/checkpoints/source/GPU 보존 |
| 정책 자체가 좋은가? | **부분적으로만 확인** | 후반 안정 plateau + 영상 sanity는 양호, yaw 병목 및 comparator 이득 미미 |
| 제출 후보로 적합한가? | **아직 아님** | PERSONAL이고 official evaluator 없음. H-011 final에서 생성된 `policy.pt` provenance도 train archive에 없음 |

## 2.3 무결성/오류 검사

확인된 결과:

- NaN/Inf: **발견되지 않음**
- CUDA OOM: **없음**
- broken pipe / traceback / fatal simulator error: **없음**
- value loss 폭발: **없음**
- checkpoint mirror 실패: **없음**
- finalize: **completed**
- official backup: **`skipped_no_config`**, PERSONAL 환경이므로 예상된 상태
- source mutation: **없음** (`source/identity.json` before/after hash 동일)
- archive internal SHA256SUMS: **검증 통과**

console의 warning은 deprecated configuration, headless display, Isaac PhysX 관련 일반 warning이며 이번 run을 실패시킨 증거는 없다.

---

# 3. Configuration Verification

## 3.1 실제 적용 reward

`source/humanoid_rewards.py`와 `native_run/params/env.yaml`을 교차검증했다.

| Reward | 실제 weight |
|---|---:|
| `track_lin_vel_xy_exp` | +0.75 |
| `track_ang_vel_z_exp` | +0.50 |
| `feet_air_time` | +0.20 |
| `termination_penalty` | -50.0 |
| `flat_orientation_l2` | -1.5 |
| `ang_vel_xy_l2` | -0.05 |
| `joint_deviation_hip` | **-0.10** |
| `joint_deviation_torso` | -0.10 |
| `action_rate_l2` | -0.0005 |
| framework `dof_acc_l2` | -1.25e-7 |
| framework `dof_pos_limits` | -1.0 |
| framework `feet_slide` | -0.25 |
| framework `joint_deviation_arms` | -0.2 |

### Parent 대비 실제 delta

H-011의 실험 가설 관점에서 바뀐 것은 **`joint_deviation_hip -0.20 → -0.10` 단 하나**다.

자동 report는 baseline 배포값과 비교하여 `track_lin 0.5→0.75`, `termination -5→-50`, `hip -0.2→-0.1` 세 개가 바뀌었다고 표시한다. 이것은 “원본 baseline 대비 누적 설정 차이”로는 맞지만, **H-011 parent 대비 변경 개수**를 의미하지 않는다. H-011의 인과 질문에서는 hip penalty 하나만 delta다.

## 3.2 PPO / runner 설정

- seed 42
- 4096 env
- 24 rollout steps/env
- PPO epochs 5, mini-batches 4
- adaptive learning rate, initial config 1e-3
- gamma 0.99, lambda 0.95
- desired KL 0.01
- entropy coefficient 0.008
- clip 0.2
- max grad norm 1.0
- actor/critic MLP `[512, 256, 128]`, ELU
- save interval 100
- NaN check enabled

이 run에서 PPO/task/env source hash는 학습 중 바뀌지 않았다.

## 3.3 terrain / command / episode

- episode horizon: 20 s
- terrain curriculum enabled
- terrain generator seed: `null`
- command resampling range가 env 설정에 존재

따라서 **같은 RL seed 42라도 terrain 생성 자체가 완전히 고정된 paired trajectory라고 단정할 수 없다.** H-008 unchanged continuation과 H-011의 수치 차이가 매우 작을 때 특히 이 점이 중요하다.

---

# 4. Training Dynamics

## 4.1 raw TensorBoard 우선 분석

TensorBoard event를 TFRecord/Event protobuf 수준에서 직접 읽어 31 scalar tag를 복원했다. 주요 scalar는 모두 2000점이며 global step 2998~4997을 연속으로 가진다. console의 매-iteration 값과 일치한다.

### 구간별 핵심 지표

| 구간 | Reward 평균 | Episode len 평균 | Terrain 평균 | XY error 평균 | Yaw error 평균 | Base-contact | Action std |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2998~3197 | 5.173 | 747.87 | 4.240 | 0.3140 | 1.2605 | 20.41% | 1.450 |
| 3198~3497 | 4.812 | 781.58 | 5.586 | 0.3438 | 1.3713 | 29.13% | 1.472 |
| 3498~3997 | 4.663 | 772.79 | 5.533 | 0.3332 | 1.4153 | 29.91% | 1.486 |
| 3998~4697 | 4.698 | 774.34 | 5.593 | 0.3351 | 1.4493 | 29.80% | 1.477 |
| **last 300: 4698~4997** | **4.948** | **780.24** | **5.661** | **0.3304** | **1.4113** | **29.02%** | **1.469** |
| last 500: 4498~4997 | 4.883 | 778.85 | 5.656 | 0.3310 | 1.4220 | 29.24% | 1.470 |

### 주요 extremum

- raw mean reward max: **6.886 @ 3084**
- terrain max: **5.7177 @ 3349**
- terrain min: **3.1701 @ 3013**
- episode length max: **911.01 @ 3045**
- XY error max: **0.3786 @ 3047**
- yaw error max: **1.6392 @ 4546**
- value loss max: **0.01358 @ 3018**

## 4.2 Phase 분석

### Phase 1 — Resume reset / metric re-population (2998~약 3050)

첫 iteration의 `episode length=11.52`, XY error `0.0128`, yaw error `0.0216`, base-contact `0`은 H-008 policy가 갑자기 완벽해졌다는 뜻이 아니다. resume 시작 직후 새 environment의 episode/termination/reward accumulator가 충분히 채워지기 전 transient다. terrain도 3.44에서 3.17까지 떨어진다.

이 구간에서 policy 성능을 endpoint처럼 비교하면 잘못된 결론을 낼 가능성이 매우 높다.

### Phase 2 — Curriculum re-expansion (약 3050~3350)

terrain이 빠르게 회복하여 3349에서 5.718을 찍는다. 동시에 episode length는 700~800대, base-contact는 약 25~30%의 평형으로 들어간다. 즉 resume 후 환경/curriculum이 정책 능력에 맞게 다시 확장되는 구간으로 보인다.

### Phase 3 — Long plateau (약 3350~4500)

terrain 5.5대, XY error 0.33대, base-contact 약 30%, episode length 770대가 장기간 유지된다. reward는 큰 장기 상승보다 약 4.6~4.8을 중심으로 진동한다. 이 구간은 “계속 빠르게 학습 중”보다는 **이미 형성된 gait/tracking 정책이 재최적화되는 plateau**에 가깝다.

### Phase 4 — Late modest recovery (약 4500~4997)

last 300에서 reward/terrain/base-contact/XY가 중기보다 소폭 좋아진다. terrain 평균 5.661, base-contact 29.02%, XY 0.3304로 late joint collapse는 없다. 반면 yaw는 약 1.41로 여전히 높다. 즉 후반 개선은 **새 능력의 급격한 획득**보다 기존 안정 보행의 미세 회복/정착으로 보는 편이 안전하다.

## 4.3 Plateau 여부

강한 plateau가 존재한다. 3.5K 이후 terrain, XY, base-contact, episode length가 좁은 범위에서 움직인다. hip penalty 완화가 큰 behavioral phase transition을 일으켰다는 징후는 없다.

---

# 5. Tracking Analysis

## 5.1 Linear / XY tracking

- last-500 XY error: **0.3310**
- last-300 XY error: **0.3304**
- endpoint: **0.3398**
- late track-linear reward: last-300 평균 **0.4875**, endpoint **0.5109**

H-008 unchanged 5K control의 프로젝트 요약 XY `0.3314`와 비교하면 H-011 last-300 `0.3304`는 사실상 같은 수준이다. 절대 차이는 `-0.0010`이며 약 0.3% 수준이다. terrain seed가 null이고 반복 seed가 없으므로 이것을 hip penalty 완화의 실질적 개선으로 부르기 어렵다.

**판정: linear tracking은 유지되었지만, 명확히 개선되었다는 근거는 약함.**

## 5.2 Forward vs lateral

현재 TensorBoard의 `error_vel_xy`는 XY 결합 오차다. forward x와 lateral y가 별도 scalar로 기록되지 않았으므로 두 축을 분리한 정량 판정은 불가능하다.

- forward: **판단 불가 (분리 scalar 없음)**
- lateral: **판단 불가 (분리 scalar 없음)**

6-terrain 영상도 command telemetry가 없어 실제 command tracking 측정으로 사용할 수 없다.

## 5.3 Yaw / turning

- last-500 yaw error: **1.4220**
- last-300: **1.4113**
- endpoint: **1.4448**
- max: **1.6392 @ 4546**
- `track_ang_vel_z_exp` last-300 평균: **0.1187**

이것은 이번 정책의 가장 뚜렷한 내부 병목이다. 기존 H-008 자체가 linear 개선과 yaw trade-off를 가진 branch였고, H-011 hip penalty 완화는 이 문제를 해소하지 못했다.

단, yaw error를 공식 회전 시나리오 점수로 직접 변환하면 안 된다. H-011은 공식 evaluator를 거치지 않았다.

## 5.4 Stop behavior

zero-command 전용 drift, 정지 후 흔들림, 재출발 안정성 scalar/evaluator가 없다. 영상 manifest에도 command stream이 없다.

**판단 불가.**

---

# 6. Stability Analysis

## 6.1 Fall / termination / survival

- last-300 base-contact: **29.02%**
- last-300 timeout: **70.99%**
- endpoint base-contact: **28.35%**
- endpoint timeout: **71.67%**
- last-300 episode length: **780.24 / 1000-step horizon scale**

H-008 unchanged 5K control 요약의 base-contact `29.67%`와 비교하면 H-011은 약 `0.65 percentage point` 낮다. 방향은 좋지만 효과가 작고 single trajectory/terrain randomness를 넘는 증거는 아니다.

또한 timeout 71%만으로 안정 보행을 주장하지 않았다. 영상에서 upright locomotion이 보이고 terrain 5.6대를 유지하므로 “누워서 버티는 생존형 local optimum”과는 양상이 다르다.

## 6.2 Terrain progression

- resume 직후 terrain: 3.438
- minimum: 3.170 @ 3013
- 5.0 이상으로 재상승: 초반 재적응 이후
- peak: 5.718 @ 3349
- last-500 mean: **5.656**
- last-300 mean: **5.661**
- endpoint: **5.651**

핵심은 초기 terrain 하락이 실패가 아니라 resume curriculum reset/repopulation의 일부였다는 점이다. 3.3K 이후에는 5.5~5.7 수준을 장기 유지한다.

H-008 unchanged control 요약 terrain `5.604` 대비 H-011 last-300 `5.661`은 +0.057 정도다. 역시 작다.

`Curriculum/terrain_levels`는 전체 4096 env의 평균 난이도이며 특정 level을 완전 정복했다는 뜻이 아니다.

## 6.3 Posture / body angular motion

`ang_vel_xy_l2` last-300은 약 -0.026 수준, `flat_orientation_l2`는 약 -0.015 수준이며 후반에 폭발하지 않는다. hip penalty 완화가 곧바로 자세 붕괴를 일으켰다는 신호는 없다.

## 6.4 Gait smoothness / action-rate

- action-rate reward last-300 평균: 약 **-0.0738**
- endpoint: **-0.0770**
- action std last-300: **1.469**

큰 late deterioration은 없지만, H-011이 gait smoothness를 개선했다는 비교 근거도 없다. hip 제약을 완화했음에도 action-rate가 특별히 낮아지는 변화는 보이지 않는다.

## 6.5 Recovery / push recovery

학습 scalar에서 push-specific success가 없고, 6-terrain 영상에도 외란 시나리오가 없다.

**판단 불가.**

---

# 7. Reward Component Analysis

이번 실험에서 가장 중요한 reward component는 `joint_deviation_hip`이다.

## 7.1 Hip component

- weight: `-0.10`
- early 평균 component: 약 `-0.0193`
- 3198~3497: `-0.0235`
- 3498~3997: `-0.0242`
- 3998~4697: `-0.0244`
- last-300: **`-0.0263`**
- endpoint: **`-0.0285`**

후반으로 갈수록 hip deviation penalty component의 절대 손실이 커진다. weight 자체가 절반으로 완화되었는데도 component가 더 음수 방향으로 가는 것은 정책이 허용된 hip deviation을 점차 더 사용하는 정황과 양립한다.

하지만 이것이 “더 좋은 골반 움직임”을 의미하지는 않는다. 실제 joint angle distribution, step symmetry, gait kinematics가 없기 때문에 **가설** 수준이다.

## 7.2 Tracking vs hip motion

settled 구간(≥3300)에서 단순 Pearson correlation을 보면 hip component와 XY error 사이에 약한~중간 수준의 관계가 나타나지만, 동일 학습 trajectory 내부 상관은 인과 증거가 아니다. 특히 reward component는 episode length/terrain/command 분포에도 영향을 받는다.

따라서 “hip을 더 자유롭게 쓰니 XY가 좋아졌다”는 주장은 현재 evidence로 확정할 수 없다.

## 7.3 다른 reward와 trade-off

- linear tracking component는 후반 유지됨.
- yaw tracking component는 상대적으로 낮게 유지됨.
- action-rate, feet-slide, dof-acc penalty는 후반 큰 폭발이 없음.
- termination penalty component도 후반 안정적.

즉 hip 완화로 인해 명백한 hopping/난폭화/termination 회피가 생겼다는 scalar evidence는 없다. 그러나 yaw 병목은 그대로 남는다.

## 7.4 Mean reward 해석

H-011과 H-008 control은 reward weight가 hip 하나 다르므로 `Train/mean_reward` 절대값을 직접 정책 품질 점수로 비교하는 것은 부적절하다. hip penalty의 scale 자체가 바뀌었기 때문이다.

---

# 8. PPO / Numerical Stability

## 8.1 Value loss

raw 2000점 기준:

| 통계 | Value loss |
|---|---:|
| median | **0.00639** |
| p95 | **0.00706** |
| p99 | **0.00742** |
| p99.9 | **0.00911** |
| max | **0.01358 @ 3018** |
| ≥0.01 횟수 | **1 / 2000** |
| ≥0.02 횟수 | **0** |

초기 resume 적응 시점에 작은 spike가 한 번 있지만 즉시 회복하며 이후 매우 안정적이다. Go2 장기 run에서 관찰됐던 수십~100 수준의 value-loss 발산과는 전혀 다른 양상이다.

## 8.2 Surrogate / entropy / LR

- surrogate loss는 후반 정상적인 작은 음수 범위
- entropy는 약 26~27 범위
- learning rate는 adaptive schedule로 변화하며 endpoint 약 `1.71e-4`
- std는 `1.44~1.49` 정도 범위에서 유지

수치적으로 policy distribution 붕괴나 optimizer instability 증거는 없다.

## 8.3 Performance / GPU

GPU telemetry 806 samples:

- median utilization 약 **52%**
- p95 약 **59.8%**, max 67%
- steady memory 약 **5236 MiB**
- median power 약 **154 W**
- 최고 temperature **46°C**
- 후반 iteration time 약 **0.78 s**
- endpoint throughput 약 **125k steps/s**

첫 iteration의 낮은 throughput은 initialization/resume overhead이며 steady-state 성능과 분리해야 한다.

---

# 9. Checkpoint Analysis

## 9.1 `model_best`의 10% 제외 규칙과 이번 선택

full raw TensorBoard 전 구간:

- **raw 전체 reward peak = 6.886 @ step 3084**

이번 run은 global 2998에서 resume하여 4997까지 2,000 iteration을 추가했다. finalizer는 **resume에서도 현재 추가 학습 구간의 첫 10%를 best 후보에서 제외**한다. 따라서 약 200 iteration의 warm-up, 즉 대략 global `2998~3197` 구간은 자동 best 탐색 대상이 아니다.

- `3084`는 resume 시작점 대비 **+86 iteration ≈ 4.3%** → **제외 구간**
- report best `3203`은 시작점 대비 **+205 iteration ≈ 10.25%** → **유효 후보 구간**
- report/finalizer best = **6.184 @ step 3203**
- selected checkpoint = `model_3200.pt`
- `collected/exported/model_best.pt` SHA-256 = `0caa8ced...71b060`
- `checkpoints/model_3200.pt` SHA-256 = 같은 값

따라서 이번 H-011에서 `3084`와 `3203`의 차이는 **finalizer mismatch가 아니라 의도된 10% warm-up exclusion으로 설명된다.** raw 전체 최고를 곧바로 “finalizer가 놓친 peak”라고 부르면 안 된다.

## 9.2 왜 그래도 `model_3200`을 최종 정책으로 자동 승격하면 안 되는가

`3203`은 10% 제외 경계를 막 지난 시점이고, 여전히 resume 후 curriculum/episode/termination 통계가 재형성되는 초반부에 가깝다. 이후 정책은 1,700+ iteration 동안 다른 steady state에서 학습된다. 또한 finalizer의 선택 기준은 허용 구간 내 `Train/mean_reward`이므로 terrain·tracking·fall·영상·공식 evaluator를 직접 최적화한 선택이 아니다.

따라서 `model_3200`은 **finalizer 규칙상 정상적인 자동 best**이지만, 장기 terrain/tracking/stability를 대표하는 제출 후보라고 자동 해석할 수는 없다.

## 9.3 Final `model_4997`

- SHA-256: `990534ae58fca33ab5841d94af981b56a3ebfe169d7bb3eaeee98712a11997fa`
- last-window에서 terrain/XY/base-contact가 동시에 붕괴하지 않음
- PPO 수치 안정성 유지

기존 resume 선택 규칙에 따라 **대표 checkpoint는 `model_4997.pt`가 더 타당**하다. 이것은 “4997이 모든 기준에서 최고”라는 뜻이 아니라, 자동 early-reward peak보다 run의 최종 학습 상태를 대표한다는 뜻이다.

## 9.4 `policy.pt` 상태

train 종료 시 `exported/policy.pt`는 provenance상 **UNCHANGED**이며 H-011 final에서 새로 생성된 정책이라는 증거가 없다. 따라서 이 archive만으로는 H-011 final checkpoint와 제출용 TorchScript policy의 exact linkage를 확정할 수 없다.

---

# 10. Video / Behavioral Analysis

## 10.1 영상 무결성

6개 모두 checksum PASS:

- boxes
- inverted stairs
- random rough
- slope down 10°
- slope up 10°
- stairs

공통 codec/format:

- H.264
- 1920×1080
- 50 fps
- 999 frames
- 19.98 s

## 10.2 직접 관찰

영상의 2초 간격 frame contact sheet를 별도로 추출해 확인했다.

**확인된 정성적 사실:**

- boxes: 여러 시점에서 upright 상태로 obstacle 영역 위/주변을 이동한다.
- random rough: 거친 지형 안에서 upright 상태를 유지하며 위치가 변한다.
- stairs/inverted stairs: 계단 영역 접근/통과 과정에서 upright posture가 유지되는 샘플이 확인된다.
- ±10° slope: 경사 접근/통과 장면에서 누운 자세나 명백한 정지형 local optimum이 보이지 않는다.

**보이지 않은 명백한 이상 행동(샘플링 기준):**

- 옆으로 누워 timeout만 얻는 행동
- 지속적인 한 발 고정 체공
- 명백한 반복 점프/hopping
- 지속 제자리 회전
- 완전한 stall

## 10.3 영상의 한계

- 20초 단일 trajectory/terrain이다.
- 모든 frame을 정량 pose tracking한 evaluator가 아니다.
- command stream이 없다.
- reset/fall event telemetry가 없다.
- 영상 내부에 checkpoint SHA가 embedded 되어 있지 않다.
- manifest의 `asserted_checkpoint=model_4997.pt`는 사용자/수집 단계 assertion이다.

따라서 영상은 “final candidate가 적어도 눈에 띄는 비정상 local optimum은 아니다”라는 sanity check로는 유효하지만, terrain 성공률·낙상률·tracking accuracy를 증명하지 않는다.

---

# 11. Baseline / Parent Comparison

## 11.1 가장 적절한 control

가장 중요한 비교 대상은 official TERM50이나 오래된 baseline이 아니라, **동일 parent `H-008 model_2998`에서 reward 변경 없이 2998→4997로 연장한 H-008 continuation**이다.

이 control은 다음 점에서 좋다.

- 같은 robot
- 같은 parent checkpoint
- 같은 global start/end 범위
- 같은 seed 42
- 같은 4096 env
- 같은 H-008 reward 설정에서 hip만 `-0.20`으로 유지

다만 control run은 generic orchestration으로 execution-time provenance 일부가 WARN이고 terrain generator seed가 null이므로 완벽한 deterministic paired experiment는 아니다.

## 11.2 후반 핵심 비교

프로젝트에 보존된 H-008 unchanged continuation late summary와 H-011 last-300을 비교한다.

| Metric | H-008 unchanged control | H-011 HIPDEV010 | 변화 | 해석 |
|---|---:|---:|---:|---|
| Terrain | 5.604 | **5.661** | +0.057 | 방향은 좋지만 작음 |
| XY error | 0.3314 | **0.3304** | -0.0010 | 실질적으로 동일 |
| Base-contact | 29.67% | **29.02%** | -0.65 pp | 소폭 개선 방향 |
| Yaw error | control exact late값 미확보 | **1.411** | 판단 불가 | H-011 자체로는 병목 |
| Episode length | control exact late값 미확보 | **780.24** | 판단 불가 | 단독으로는 안정 plateau |

### 비교 결론

세 공통 지표가 모두 H-011 방향으로 아주 조금 좋아졌다는 점은 흥미롭지만, 효과 크기가 작다. single seed + terrain seed null + control provenance WARN을 고려하면 **hip -0.10의 실질적 이득을 확정할 정도는 아니다.**

## 11.3 Official TERM50와의 관계

공식 TERM50 5K는 별도 서버/시점/설정 lineage이므로 직접 causal control은 아니다. 공식 TERM50의 내부 endpoint yaw `0.935`, terrain `5.825`, base-contact `28.93%`와 H-011 수치를 나란히 볼 수는 있지만, H-011의 개선/악화율로 해석하면 안 된다.

---

# 12. Tracking vs Stability Trade-off

이번 H-011의 성격은 다음과 같다.

### Tracking

- XY: H-008 unchanged control과 사실상 동일
- yaw: 절대적으로 높은 error가 유지되어 병목
- forward/lateral 분리: 판단 불가
- stop: 판단 불가

### Stability

- terrain: 5.6대 안정 plateau
- base-contact: 약 29%, control 대비 소폭 개선 방향
- episode length: 약 780
- video: 6 terrain에서 upright locomotion sanity 확인
- numerical stability: 매우 양호

따라서 4분류를 억지로 고르면 `Tracking ≈ / Stability ≈~소폭↑`에 가깝지만, 사용자 요청의 네 가지 ↑/↓ 틀로 확정하기보다는 **“stability를 해치지 않고 hip 자유도를 늘렸으나, tracking 또는 stability의 유의미한 추가 개선은 아직 입증되지 않음”**이 더 정확하다.

---

# 13. Local Optimum / Reward Hacking Check

| 위험 유형 | 판정 | 근거 |
|---|---|---|
| 움직이지 않고 생존 | **낮음** | terrain 5.6 + 영상 이동 |
| 비정상 자세로 timeout | **낮음** | sampled video upright |
| hopping | **명백한 증거 없음** | 영상 샘플 + feet-air component 작음 |
| 한 발 오래 들기 | **명백한 증거 없음** | sampled video |
| sliding | **완전 배제 불가** | feet-slide penalty 존재하나 전용 kinematic metric 없음 |
| command 무시 | **부분 판단** | XY error 양호, yaw는 나쁨; command-separated evaluator 없음 |
| terrain 회피 | **명백한 증거 없음** | terrain video/level |
| survival-only | **낮음** | XY tracking과 terrain 동시 유지 |
| 한 reward만 과최적화 | **명백한 증거 없음** | 여러 component 안정 |

이번 run의 문제는 reward hacking보다 **효과 크기가 작고 yaw 병목이 남는 것**에 가깝다.

---

# 14. Key Findings

1. **H-011 identity가 강하게 확정됐다.** H-008 3K final `model_2998` SHA와 일치하는 parent에서 2998→4997을 수행한 PERSONAL resume이며, 실험 delta는 hip penalty `-0.20→-0.10` 하나다.
2. **실행/evidence는 건강하다.** exit 0, 2000-step raw TB, full console, 21 checkpoint, source immutability, GPU telemetry, checksum PASS가 있다.
3. **resume 초반 50~200 iteration은 성능 비교에 부적합한 transient다.** terrain/episode/termination accumulator가 재형성되며 reward peak도 이 시기에 나타난다.
4. **정책은 3.3K 이후 명확한 plateau에 들어갔다.** terrain 약 5.5~5.7, XY 약 0.33, base-contact 약 29~30%가 장기 유지된다.
5. **H-011은 H-008 unchanged control을 압도하지 않는다.** terrain +0.057, XY -0.001, base-contact -0.65pp 정도로 방향은 약간 좋지만 너무 작아 single-run noise와 분리하기 어렵다.
6. **yaw는 가장 큰 내부 병목으로 남는다.** last-300 yaw error 1.411, endpoint 1.445이며 hip 완화가 이를 해결하지 못했다.
7. **PPO numerical stability는 매우 좋다.** value loss p99 0.0074, max 0.0136, NaN/Inf 없음. 학습 실패가 아니라 “정책 성능 차이가 작음”이 핵심이다.
8. **이번 run의 raw 전체 peak와 report best 차이는 버그가 아니다.** `6.886@3084`는 resume 추가 구간의 첫 10%(+86회, 약 4.3%)에 있어 자동 best 후보에서 제외되고, `6.184@3203`은 +205회(약 10.25%)로 유효 구간에 들어간다. `model_3200` 선택은 finalizer 규칙과 일치한다.
9. **final `model_4997`이 대표 checkpoint로 더 타당하다.** 후반 terrain/tracking/fall joint collapse가 없고 long-run state를 대표한다.
10. **영상은 local-optimum sanity check에는 긍정적이지만 provenance/evaluator가 아니다.** 6 terrain에서 upright locomotion을 보였지만 checkpoint SHA와 command telemetry는 없다.

---

# 15. Final Decision

## **HOLD**

### 이유

H-011은 실행 실패도 아니고 명백한 정책 실패도 아니다. `joint_deviation_hip=-0.10`에서도 H-008 계열의 terrain/XY/stability를 유지하고, 6-terrain 영상에서 비정상 생존형 local optimum이 보이지 않는다는 점은 긍정적이다.

하지만 가설의 핵심인 **“hip penalty 완화가 정책을 실제로 더 좋게 만든다”**는 아직 입증되지 않았다. 같은-parent unchanged continuation 대비 공통 late metric 차이는 작고, yaw 병목은 남아 있다. multi-seed/fixed evaluator가 없으며 terrain generator seed도 null이다.

따라서:

- **PROMOTE**: 아직 이르다.
- **REJECT**: 성능 붕괴가 없으므로 과도하다.
- **INVALID**: provenance는 충분히 유효하다.
- **HOLD**가 가장 적절하다.

---

# 16. Next Experiment

## 16.1 가장 정보 효율이 높은 다음 행동 — 새 학습 전에 H-009 분석 완료

현재 가장 가치 있는 것은 새 reward를 또 바꾸는 것이 아니라, 이미 존재하는 sibling H-009 `HIPDEV030` (`joint_deviation_hip=-0.30`) evidence를 H-011과 동일한 파이프라인으로 분석하는 것이다.

이유:

- H-009/H-011은 같은 H-008 `model_2998` parent의 반대 방향 branch다.
- H-008 unchanged continuation의 `-0.20`이 중간 control이 된다.
- 따라서 조건이 맞으면 `-0.30 / -0.20 / -0.10`의 **3-point response curve**를 추가 GPU 시간 없이 얻을 수 있다.

먼저 H-009에서 다음을 확정해야 한다.

- 실제 additional iterations가 H-011과 같은 2000인지
- parent SHA가 정확히 같은지
- seed/env/PPO 동일성
- last-300/500 terrain, XY, yaw, base-contact, episode length
- raw full-TB peak와 resume 첫 10% 제외 후 eligible best/report selection의 일치 여부
- final checkpoint 영상

### 3-point 판정 규칙

- `-0.10`이 control 대비 **terrain↑ + base-contact↓ + XY 유지/개선**을 반복하고 `-0.30`이 반대로 악화 → hip 완화 방향을 PROMOTE 후보로.
- `-0.30`이 더 좋고 `-0.10`이 control과 같음 → stronger hip constraint 후보.
- 세 값 차이가 모두 작음 → hip deviation은 현재 병목이 아니므로 reward 축을 닫고 다른 병목으로 이동.

## 16.2 다음 *실제 학습*이 반드시 하나 필요하다면

H-009 분석 후 세 값이 사실상 동률이면, hip을 더 세분화하지 말고 **yaw 병목을 격리**하는 것이 정보 효율이 높다.

권장 설계 예시:

- Parent: H-008/H-011 계열에서 선택한 동일 안정 checkpoint
- Control: `track_ang_vel_z_exp=0.50`
- Test: `track_ang_vel_z_exp=0.60`
- 나머지 reward 완전 고정
- 같은 seed / 4096 env / 같은 +2K resume 조건
- 반드시 unchanged same-parent control과 paired

성공 기준:

1. late yaw error가 control보다 명확히 낮음
2. XY error 악화가 작거나 없음
3. terrain 및 base-contact가 control 범위를 유지
4. action-rate/flat-orientation의 명확한 악화 없음
5. fixed yaw/stop evaluator에서 실제 회전 및 정지 행동 개선

단, H-009 결과가 hip 방향성을 명확히 보여 준다면 yaw branch 전에 hip optimum을 공식/반복 평가로 확인하는 것이 더 낫다.

---

# 17. Confidence & Limitations

## 17.1 강하게 확인된 것

- H-011 run identity, PERSONAL 여부
- parent checkpoint path/SHA
- resume 2998→4997
- seed 42, 4096 env, 24 rollout
- 실제 reward weights
- hip-only parent delta
- exit 0 / finalize complete / evidence PASS
- raw TensorBoard 31 scalar tags, 2000 points
- console 2000 iteration
- value-loss/terrain/tracking/termination 시계열
- `model_best == model_3200` hash
- final `model_4997` hash
- full raw reward peak(`3084`)가 resume 첫 10% 제외 구간이라는 점과 report best(`3203`)의 selection-rule 일치
- 6 MP4 checksum/codec/duration

## 17.2 강한 정황

- 3.3K 이후 long plateau
- hip 완화가 stability를 크게 해치지 않음
- final 4997이 early auto-best보다 대표 checkpoint로 적합
- 영상상 survival-only/hopping형 local optimum 가능성이 낮음

## 17.3 가설

- hip penalty 완화가 실제 hip excursion을 증가시켰을 가능성
- 소폭 terrain/base-contact 개선이 hip 자유도 때문일 가능성
- yaw 병목과 hip 자유도 사이의 상호작용

이들은 joint kinematics, fixed evaluator, matched multi-run 없이 인과로 확정하지 않는다.

## 17.4 판단 불가 / 누락

- forward와 lateral tracking 분리
- zero-command stop drift
- push recovery
- terrain별 반복 성공률
- exact fall count per terrain
- H-011 final `policy.pt`와 checkpoint의 actor exact-match
- 공식 evaluator score
- OFFICIAL 성능 개선
- multi-seed statistical significance
- video의 cryptographic checkpoint linkage

## 17.5 Single-seed 주의

이 run은 single seed다. 현재 결과는 방향성 실험 evidence로는 충분하지만, 최적값·통계적 우월성·일반화·확정 인과를 주장할 수 없다.

---

# 18. Evidence / Provenance Inventory

## 사용자 제공 원본

### Train evidence archive

`20260920-150652-h1-h011-hipdev010.tar.gz`

주요 내부 파일:

- `metadata.json`
- `validation.json`
- `command.txt`
- `console.log`
- `native_run/events.out.tfevents...`
- `native_run/params/env.yaml`
- `native_run/params/agent.yaml`
- `source/humanoid_rewards.py`
- `source/identity.json`
- `checkpoints/model_3000.pt` ... `model_4900.pt`, `model_4997.pt`
- `collected/exported/model_best.pt`
- `collected/exported/env.yaml`
- `collected/exported/report.html`
- `system/nvidia_smi_before.txt`
- `system/nvidia_smi_during.csv`
- `system/nvidia_smi_after.txt`
- `SHA256SUMS`

내부 checksum은 검증 통과했다.

### Video suite

`h1-h011-hipdev010-model4997-6terrain-video-suite-20260920.tar.gz`

- `boxes.mp4`
- `inverted_stairs.mp4`
- `random_rough.mp4`
- `slope_down_10deg.mp4`
- `slope_up_10deg.mp4`
- `stairs.mp4`
- `video_suite_manifest.json`
- `SHA256SUMS`

모든 MP4 checksum PASS.

## 프로젝트 비교 자료

- `14_H1_NEXT_RUN_PARAMETER_COMPARISON(20260920-134532).md`
  - H-008/H-009/H-010/H-011 sibling lineage
  - H-008 unchanged 2998→4997 control late summary
- `15_OPTUNA_REWARD_DECISION_ENGINE(20260920-134531).md`
  - hip fine-search 범위와 H-008/H-011 계획
- `18_H1_FINALIZE_REPORT_LIMITATIONS(20260918-020450).md`
  - 과거 model_best/report mismatch 사례와 자동 best의 해석 한계. 단, 이번 H-011의 `3084`→`3203` 차이는 첫 10% 제외 규칙으로 설명되므로 과거 mismatch 사례와 구분
- `13_H1_OFFICIAL_SERVER_BASELINE_EVIDENCE(20260918-020633).md`
  - 공식 TERM50 기준선 및 공식 평가와 PERSONAL 분리
- `16_EXPERIMENT_EXPORT_AND_TENSORBOARD(20260918-020542).md`
  - evidence 보존/분석 경계

---

# 최종 답변: 8개 질문

1. **이 정책은 무엇을 배웠는가?**\
   H-008 parent의 linear-tracking 중심 gait를 유지하면서, resume 후 terrain curriculum에 다시 적응해 terrain 5.6대와 약 71% timeout 수준의 장기 보행을 유지했다. hip penalty 완화로 새로운 뚜렷한 phase transition은 없었다.

2. **이전 정책보다 무엇이 실제로 좋아졌는가?**\
   unchanged H-008 continuation 대비 terrain/base-contact/XY가 모두 아주 조금 좋은 방향이지만 차이가 작아 “실제 개선”으로 확정할 수 없다.

3. **무엇을 잃었는가?**\
   명확한 새 손실은 보이지 않지만 yaw tracking은 여전히 나쁘다. hip 완화가 yaw를 개선하지 못했다.

4. **학습 중 언제 중요한 변화가 일어났는가?**\
   2998~약 3050 resume transient, 3050~3350 curriculum 재확장, 이후 long plateau, 4500 이후 소폭 late recovery가 핵심 phase다.

5. **높은 지표가 실제 행동 개선을 의미하는가?**\
   자동 reward peak는 아니다. early reward peak와 long-run behavior가 분리되어 있고 finalizer도 raw peak를 잘못 선택했다. 영상에서는 upright locomotion이 확인되어 late terrain/stability scalar와 정성적으로는 일치한다.

6. **현재 가장 큰 병목은 무엇인가?**\
   내부 지표상 **yaw tracking**과, hip reward 효과가 control noise보다 충분히 큰지 확인할 **비교 신뢰성**이다.

7. **이 가설은 계속 실험할 가치가 있는가?**\
   **HOLD.** 붕괴하지 않았고 약한 개선 방향은 있으나, 현 단계에서 -0.10을 승격할 근거는 부족하다.

8. **다음 한 번으로 가장 많은 정보를 얻으려면?**\
   우선 새 GPU run 없이 H-009 `-0.30` 기존 evidence를 동일 방식으로 분석하여 `-0.30/-0.20/-0.10` 3-point sweep을 완성한다. 그 결과 hip 축이 평평하면 다음 실제 학습은 yaw reward를 단일 변수로 격리한다.

---

**보고서 자체 신뢰도:** 높음. 원본 train archive의 raw event/console/config/hash/checkpoint와 video checksum을 직접 교차검증했으며, 비교 control 일부는 프로젝트 요약값에 의존한다. 공식 evaluator와 multi-seed가 없으므로 정책 우월성에 대한 확신은 제한된다.
