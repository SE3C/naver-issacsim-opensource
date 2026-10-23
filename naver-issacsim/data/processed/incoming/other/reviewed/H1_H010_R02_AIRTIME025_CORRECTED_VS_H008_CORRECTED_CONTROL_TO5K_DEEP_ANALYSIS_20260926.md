# H1 H-010 R02 AIRTIME025 CORRECTED vs H-008 CORRECTED CONTROL — 심층 분석

- 분석일: 2026-09-26
- Robot: H1 / `Humanoid-v0`
- A (분석 대상): `H-010 R02 AIRTIME025 corrected`, `feet_air_time=0.25`
- B (대조군): `H-008 corrected unchanged continuation`, `feet_air_time=0.20`
- 환경: 두 Run 모두 PERSONAL / Brev L40S
- 핵심 질문: corrected H-008 3K parent에서 `feet_air_time 0.20 → 0.25`만 바꾼 +2K resume이 unchanged +2K continuation보다 실제 학습 지표와 6지형 행동에서 개선 신호를 보이는가?

> **한 줄 결론:** 이 corrected sibling 비교에서는 A가 B와 거의 같은 terrain/XY 성능을 유지하면서 후반 yaw 추종과 training base-contact 종료 비중을 소폭 개선했고, 6지형 영상에서도 명백한 지속 한발 hopping은 보이지 않았다. 다만 hip/torso deviation 패널티가 조금 악화됐고 영상은 command/seed가 matched가 아니므로, **가설은 PERSONAL screening 범위에서 `PROMOTE`하되 최종 채택은 보류**하고 두 final checkpoint를 동일 fixed evaluator에 한 번 붙이는 것이 다음 정보가치가 가장 크다.

---

## 1. 결론 요약

### 세 질문에 대한 답

**1) 이번 정책은 목표 행동을 실제로 얼마나 수행하는가?**

A `model_4997`은 제공된 여섯 영상에서 모두 upright locomotion을 보이며, sampled frames에서 명백한 낙상·주저앉기·지속적인 한 발 hopping은 확인되지 않았다. 계단/역계단/rough에서는 장애물 구간을 지나 평지로 빠져나오는 진행이 보인다. 특히 `boxes.mp4`에서는 A가 약 12–13초에 dense box field를 빠져나온 반면 B는 19초까지 장애물 구간에 남아 있는 장면 차이가 크다. 다만 영상 suite manifest에는 command, video seed, difficulty, curriculum level, camera parameter가 없으므로 이 차이를 동일 episode 성능 차이로 정량화할 수 없다.

훈련 raw TensorBoard의 late-500(`4498–4997`)에서는 A가 B 대비:

- terrain: `5.6611 vs 5.6718` — 사실상 동률, A가 `-0.0108` 낮음
- XY error: `0.32957 vs 0.32938` — 사실상 동률, A가 `+0.00019`
- yaw error: `1.36436 vs 1.42790` — A가 `-0.06354`, 약 **4.45% 낮음**
- base-contact termination: `28.821% vs 29.420%` — A가 **-0.599%p**
- timeout: `71.185% vs 70.595%` — A가 **+0.590%p**
- mean episode length: `781.82 vs 774.94` — A가 `+6.88` steps, 약 **+0.89%**
- mean policy std: `1.4587 vs 1.4778` — A가 약 `-1.29%`

즉 현재 자료가 지지하는 목표 행동은 **“terrain/linear tracking을 잃지 않으면서 late yaw·생존 쪽을 조금 개선한 보행”**이다. 큰 폭의 terrain 향상이나 linear tracking 향상은 확인되지 않았다.

**2) 비교 정책과의 차이 중 무엇이 관찰된 차이이고, 무엇을 설정 변경 효과로 해석할 수 있는가?**

이번 A/B 학습 비교는 과거 잘못된 lineage 비교와 달리 상당히 강한 sibling 설계다.

- 두 Run의 기록상 resume source checkpoint SHA-256이 동일:
  `49fdb297924c861493d377f22b9de135d83c73969ef3d8a2e4a56c9879414983`
- 둘 다 parent iteration `2998`에서 시작해 global `4997`까지 정확히 2,000 scalar point를 기록
- seed `42`, num_envs `4096`, PPO/agent 설정 동일
- `train.py`, `play.py`, `env_cfg.py`, `_finalize.py`, `agent_cfg.py` 등 source hash 동일
- `humanoid_rewards.py`의 실제 diff는 `feet_air_time: 0.20 → 0.25` 한 줄뿐
- native `env.yaml` diff도 `log_dir`과 `feet_air_time weight`만 다름
- 동일 L40S / 동일 driver / 동일 runtime 계열에서 연속 실행

따라서 **훈련 시계열에서 관찰된 차이를 이 sibling 안의 `feet_air_time` 변경과 연관된 효과로 해석하는 것은 적절하다.** 다만 단일 seed이고 terrain generator seed가 `null`이므로, stochastic realization 차이를 완전히 제거한 deterministic causal estimate는 아니다.

영상 차이는 더 약한 인과 증거다. 두 suite가 각각 정확한 final checkpoint에서 생성됐다는 provenance는 강하지만, manifest에 matched command/seed가 없으므로 `boxes`에서의 큰 진행 차이는 **관찰된 행동 차이**이지, 그 자체로 reward 효과의 정량 인과 추정치는 아니다.

**3) 현재 자료에서 내려야 할 결정과 먼저 해결할 불확실성은?**

- 실행: **COMPLETE / COMPLETE**
- evidence integrity: **PASS / PASS**, 두 train archive 내부 `SHA256SUMS` 43개 항목 전부 검증 통과
- 비교: **reward-effect 질문에는 직접 비교에 적합하되 single-seed 조건부**, video performance 질문은 **조건부 비교**
- 가설 H-010 R02 `feet_air_time=0.25`: **PROMOTE — PERSONAL corrected-lineage screening 범위**
- 정책 대표 checkpoint: **A/B 모두 final `model_4997.pt`**
- 제출/공식 성능 판단: **아직 불가**
- 다음 한 번의 행동: **새 학습이 아니라 기존 A/B final checkpoint를 동일 fixed evaluator에서 paired 평가**

현재 결정은 “0.25를 바로 최종 채택”이 아니라 **“corrected control보다 다음 검증 단계에 올릴 만한 신호가 생겼다”**이다.

---

## 2. 실제 Run · checkpoint · 영상 identity

### 2.1 받은 원본

| 역할 | 파일 | 외부 archive SHA-256 |
|---|---|---|
| A train | `20260925-102659-h1-h010-r02-airtime025-corrected-h1-corrected-20.tar.gz` | `10ac53ae57a142b1bd74db4b36b67bdcbdaf95a45aa6d8a798ca89c7ba495674` |
| A video | `checkpoint-h1-model_4997-fd497dcb7a76-download.tar.gz` | `6302f6fe6a844660bc91bf9fbc5f29694d43894e6658d0ff5f7429f8942b7128` |
| B train | `20260925-091257-h1-h008-corrected-control-to5k-h1-corrected-2026.tar.gz` | `17aa08173eea96a8eb93499fe7763e7bde7f9b00179eac8cc5d353a51bd76faf` |
| B video | `checkpoint-h1-model_4997-4349fe565013-download.tar.gz` | `faf3563d104edae5fb2ca2edf6e784a07567350ed2629edd0e0c277a89d814f4` |

원본 archive는 수정하지 않았다.

### 2.2 A/B 학습 identity

| 항목 | A — H-010 R02 AIRTIME025 | B — H-008 corrected control |
|---|---|---|
| mode | PERSONAL | PERSONAL |
| task | `Humanoid-v0` | `Humanoid-v0` |
| seed | 42 | 42 |
| num_envs | 4096 | 4096 |
| rollout | 24 steps/env/iteration | 동일 |
| parent run ID | `NCRC_BATCH_h1-corrected-20260925-03_h008_corrected_2998` | 동일 |
| requested parent | `model_2998.pt` | 동일 |
| recorded parent SHA | `49fdb297...9414983` | 동일 |
| requested additional iterations | 2000 | 2000 |
| raw event global range | 2998–4997 | 2998–4997 |
| scalar points/core tag | 2000 | 2000 |
| final numbered checkpoint | `model_4997.pt` | `model_4997.pt` |
| exit | 0 | 0 |
| evidence validation | PASS | PASS |
| mirrored checkpoints | 21 | 21 |
| GPU | NVIDIA L40S 46,068 MiB | 동일 |
| driver | 580.126.09 | 동일 |
| runtime platform | Linux 6.8 / Ubuntu 22.04 계열 | 동일 |
| Python | 3.10.12 | 3.10.12 |

두 child archive에는 parent `model_2998.pt` 바이트 자체가 포함되지 않았다. 따라서 parent SHA는 **metadata에서 동일하게 기록된 연결**이며 이번 intake에서 parent 파일 바이트를 다시 hash한 것은 아니다. 다만 같은 parent run ID/SHA, 동일 source/PPO, 거의 같은 resume 직후 초기 scalar가 서로 일치하는 것은 같은 출발점 기록과 일관된다.

### 2.3 실제 reward diff

`source/humanoid_rewards.py`를 직접 diff한 결과:

```diff
-    "feet_air_time":        0.2,
+    "feet_air_time":        0.25,
```

나머지 사용자 reward는 동일:

| reward | A | B |
|---|---:|---:|
| `track_lin_vel_xy_exp` | 0.75 | 0.75 |
| `track_ang_vel_z_exp` | 0.5 | 0.5 |
| `feet_air_time` | **0.25** | **0.20** |
| `termination_penalty` | -50.0 | -50.0 |
| `flat_orientation_l2` | -1.5 | -1.5 |
| `ang_vel_xy_l2` | -0.05 | -0.05 |
| `joint_deviation_hip` | -0.2 | -0.2 |
| `joint_deviation_torso` | -0.1 | -0.1 |
| `action_rate_l2` | -0.0005 | -0.0005 |

`agent.yaml`은 byte-level textual diff가 없고, native `env.yaml` diff는 run별 `log_dir`과 `feet_air_time weight`만 존재했다. task source identity에서 `humanoid_rewards.py`만 hash가 달랐고 나머지 task source는 같았다.

### 2.4 final checkpoint ↔ video suite 연결

- A final `model_4997.pt`:
  `fd497dcb7a763ca496996dde89f23308e5a45cb23d11fe1861d4e5d63947e5df`
- A video suite manifest의 `checkpoint_sha256`:
  **동일 `fd497dcb...47e5df`**

- B final `model_4997.pt`:
  `4349fe5650135c6a77546afc1b165ff60c235bdd83831bd562d618b04c3b5b6d`
- B video suite manifest의 `checkpoint_sha256`:
  **동일 `4349fe56...3b5b6d`**

각 suite의 6개 MP4 내부 SHA도 manifest/SHA256SUMS와 전부 일치했다. 따라서 이번 영상은 stale/UNCHANGED artifact가 아니라 **각 Run의 final checkpoint 행동**으로 연결된다.

영상 공통 형식:

- H.264
- 1920×1080
- 50 fps
- 999 frames
- 19.98 s
- terrain 6종: `stairs`, `inverted_stairs`, `boxes`, `random_rough`, `slope_up_10deg`, `slope_down_10deg`

주의: `slope_up_10deg`/`slope_down_10deg`는 suite label이다. manifest는 terrain generator 이름을 기록하지만 실제 slope parameter 숫자를 별도로 기록하지 않으므로, **“10°”를 geometry에서 독립 검증한 것은 아니다.**

---

## 3. 비교 설계와 해석 가능한 범위

### 3.1 비교 등급

| 질문 | 판정 | 이유 |
|---|---|---|
| `feet_air_time 0.20→0.25`의 **훈련 trajectory 효과** | **직접 비교에 적합, single-seed 조건부** | 동일 기록상 parent/SHA, 동일 PPO/source/seed/env 수/추가 학습량, 실제 single reward diff |
| 완성된 final policy의 **훈련 내부 지표 성능** | **직접 비교에 적합** | 동일 tag/집계/iteration 범위 |
| 6지형 영상의 **정성 행동 차이** | **조건부 비교** | source checkpoint provenance는 정확하지만 command/seed/difficulty가 manifest에 없음 |
| reward 변경의 **공식 평가 점수 효과** | **판단 불가** | 둘 다 PERSONAL, 공통 공식 evaluator 없음 |
| reward 변경의 **일반화된 최적값** | **판단 불가** | 단일 training seed, 복수 evaluator seed 없음 |

### 3.2 같은 seed의 한계

두 Run의 training seed는 42이지만 native `env.yaml`의 terrain generator seed는 `null`이다. 따라서 “seed가 같으니 동일 terrain patch sequence/동일 episode”라고 가정하지 않는다. 이 비교는 조건을 매우 잘 맞춘 sibling이지만, 독립적인 stochastic realization 차이가 일부 섞일 수 있다.

### 3.3 총 reward를 성능 척도로 쓰지 않은 이유

A는 `feet_air_time` weight 자체가 더 크다. 따라서 `Train/mean_reward`와 `Episode_Reward/feet_air_time`은 정의상 scale이 바뀐다. A의 late reward가 높다는 사실은 기록하지만, 이를 성능 개선의 핵심 근거로 사용하지 않았다.

또한 `Episode_Reward/feet_air_time`을 weight로 나누어 “실제 air time”으로 역산하지 않았다. 해당 TensorBoard tag의 normalization/episode aggregation 정의를 이번 archive만으로 충분히 확인할 수 없기 때문이다.

---

## 4. TensorBoard raw event 재분석

### 4.1 파싱 방법과 이벤트 구조

두 `events.out.tfevents*`를 TensorFlow 없이 TFRecord framing + `tensorboardX.proto.event_pb2`로 직접 파싱했다.

각 Run:

- scalar records: 62,000
- tags: 31
- 핵심 iteration tag 29개: 각각 정확히 2,000 points
- global step: `2998..4997`
- 핵심 tag에서 duplicate step 없음
- step reset 없음
- core trajectory 누락 없음

`Train/mean_reward/time` 및 `Train/mean_episode_length/time`은 wall-time을 integer-like step으로 기록하면서 중복 step이 발생한다. 이 둘은 iteration trajectory 분석에서 제외했다.

### 4.2 resume 재적응

terrain 시작값은 양쪽 모두 `3.43796`.

- B terrain minimum: `3.18066 @3012`, 시작값 재돌파 `@3040`
- A terrain minimum: `3.17507 @3012`, 시작값 재돌파 `@3042`

즉 corrected parent에서 resume 직후 curriculum 재적응은 존재하지만, 약 40여 global iteration 안에 초기 terrain level을 회복했다. 따라서 primary late window를 **마지막 500 iterations (`4498–4997`)**로 잡는 것이 재적응 구간에서 충분히 멀다.

경계 민감도 확인을 위해 **last-300 (`4698–4997`)**도 별도로 계산했다. 결론 방향은 대부분 유지된다.

### 4.3 Primary: late-500 동일 기준 비교

| 지표 | B control | A airtime025 | A−B | 해석 |
|---|---:|---:|---:|---|
| terrain level | 5.6718 | 5.6611 | -0.0108 | 사실상 동률 |
| XY error | 0.32938 | 0.32957 | +0.00019 | 사실상 동률 |
| yaw error | 1.42790 | **1.36436** | **-0.06354** | A 약 4.45% 낮음 |
| base-contact termination | 29.420% | **28.821%** | **-0.599%p** | A 방향상 개선 |
| timeout | 70.595% | **71.185%** | **+0.590%p** | A 방향상 개선 |
| mean episode length | 774.94 | **781.82** | **+6.88** | A 약 +0.89% |
| policy mean std | 1.4778 | 1.4587 | -0.0190 | A 소폭 낮음 |
| value loss | 0.006342 | 0.006441 | +0.000099 | 실질 비슷 |
| surrogate loss | -0.014076 | -0.013734 | +0.000342 | 실질 비슷 |
| mean reward | 4.5336 | 4.8760 | +0.3424 | **weight가 달라 성능 비교 근거로 사용하지 않음** |

`Episode_Termination/base_contact`는 training logger의 집계값이다. 이를 fixed evaluator의 “낙상률”이나 공식 Survival score로 바꾸어 부르지 않는다.

### 4.4 last-300 sensitivity check

| 지표 | B control | A airtime025 | A−B |
|---|---:|---:|---:|
| terrain | 5.6516 | 5.6597 | +0.0081 |
| XY error | 0.32806 | 0.32725 | -0.00081 |
| yaw error | 1.40977 | **1.34583** | **-0.06394** |
| base-contact | 29.095% | **28.866%** | **-0.229%p** |
| timeout | 70.912% | **71.142%** | **+0.230%p** |
| episode length | 778.69 | 781.07 | +2.38 |
| policy std | 1.4735 | 1.4574 | -0.0161 |

late-500과 last-300 모두에서 가장 일관된 신호는 **yaw error 감소**다. base-contact/episode-length의 효과 크기는 window에 따라 줄어들지만 방향은 유지된다. terrain과 XY는 양쪽에서 거의 겹친다.

### 4.5 학습 phase별 변화

| phase | terrain Δ(A−B) | XY error Δ | yaw error Δ | base-contact Δ | episode length Δ |
|---|---:|---:|---:|---:|---:|
| first 200, `2998–3197` | -0.0085 | -0.00168 | **+0.02835** | **+0.356%p** | -3.03 |
| post-adapt 500, `3198–3697` | +0.0037 | -0.00070 | +0.01024 | -0.340%p | +3.66 |
| middle 500, `3698–4197` | +0.0351 | +0.00371 | **-0.02181** | -0.039%p | +4.91 |
| late 500, `4498–4997` | -0.0108 | +0.00019 | **-0.06354** | **-0.599%p** | **+6.88** |

중요한 점은 A의 이점이 resume 직후 즉시 나타난 것이 아니라, **초기에는 yaw/base-contact가 오히려 약간 나빴다가 학습 후반으로 갈수록 yaw 및 survival 방향이 역전**된다는 것이다. 이는 단순한 첫 수십 iteration 우연값보다는 학습 adaptation 이후 나타난 차이에 가깝다.

단, 한 Run의 연속 500 point는 500 independent seeds가 아니다. p-value나 좁은 신뢰구간을 만들지 않았다.

### 4.6 동일 weight인 reward term의 trade-off

late-500에서 weight가 동일한 term끼리만 비교하면:

| logged term | B | A | A−B | 해석 |
|---|---:|---:|---:|---|
| `track_lin_vel_xy_exp` | 0.48237 | 0.48808 | +0.00571 | A 방향상 소폭 높음 |
| `track_ang_vel_z_exp` | 0.11617 | 0.12300 | +0.00683 | A 방향상 높음 |
| `feet_slide` | -0.04928 | -0.04910 | +0.00018 | 거의 동일 |
| `joint_deviation_hip` | -0.03686 | **-0.03840** | **-0.00154** | A가 더 큰 penalty |
| `joint_deviation_torso` | -0.00606 | **-0.00660** | **-0.00054** | A가 더 큰 penalty |
| `action_rate_l2` | -0.07443 | -0.07394 | +0.00049 | 거의 동일/약간 덜 penalty |
| `flat_orientation_l2` | -0.01166 | -0.01151 | +0.00014 | 거의 동일 |
| `ang_vel_xy_l2` | -0.02599 | -0.02572 | +0.00027 | 거의 동일 |

따라서 A는 yaw/survival 쪽을 얻는 대신 **hip·torso 정렬 비용이 소폭 증가**한 것으로 보인다. 이것은 “자세가 눈에 띄게 무너졌다”는 뜻이 아니라, 동일 계산식의 training aggregate penalty가 조금 더 음수였다는 뜻이다.

`feet_air_time` term은 weight 자체가 다르므로 underlying 행동량 비교에 사용하지 않았다.

### 4.7 최적화 안정성

두 Run 모두 raw scalar에서 NaN/Inf가 0개였다.

- B value loss: min `0.00208`, max `0.01988`, p99 약 `0.00745`
- A value loss: min `0.00216`, max `0.01787`, p99 약 `0.00743`
- learning rate range: 둘 다 약 `1e-5 .. 3.844e-4`
- final LR: 둘 다 `1.7086e-4`
- final policy std: B `1.4722`, A `1.4582`

급격한 value-loss 발산이나 NaN/Inf, checkpoint 생성 중단은 없다. `std` 절대값 하나로 정책 품질을 판정하지 않았으며, 두 Run의 상대 추세를 보조적으로만 사용했다.

---

## 5. 자동 best와 final checkpoint

### 5.1 raw reward peak와 selector warm-up

global range `2998–4997`에 대해 verified finalizer 규칙의 eligible threshold는:

`2998 + max(50, floor((4997-2998)*0.10)) = 3197`

raw reward peak:

- B global max: `6.19254 @3125` — warm-up 아래라 selector 대상 아님
- A global max: `6.33398 @3079` — warm-up 아래라 selector 대상 아님

eligible reward peak:

- B: `5.75723 @4874` → nearest saved `model_4900.pt`
- A: `5.98835 @4960` → nearest saved `model_4997.pt`

실제 hash 확인:

- B `exported/model_best.pt` == `checkpoints/model_4900.pt`
- A `exported/model_best.pt` == `checkpoints/model_4997.pt`

report에 표시된 `5.76 @4874`, `5.99 @4960`과 raw event 재계산이 일치한다.

### 5.2 대표 checkpoint 판단

이 프로젝트의 long resume 운영 원칙에 따라 final numbered checkpoint를 기본 대표로 본다. 이번 자료에서도 마지막 구간에 terrain·tracking·base-contact가 함께 붕괴하는 joint late collapse는 없다.

**A final `4997`**은 late 평균 대비 endpoint에서 terrain, XY, yaw, base-contact, episode length가 전반적으로 양호하다.

**B final `4997`**은 `model_best=4900`보다 reward selector상 peak에서 멀지만, endpoint가 tracking까지 함께 무너진 것은 아니다.

- final terrain `5.6124`
- final XY `0.3257`
- final yaw `1.3912`
- final base-contact `30.25%`
- final episode length `764.63`

late-500 평균 대비 terrain/base-contact/episode가 조금 나쁘지만 XY/yaw는 오히려 낮아, “joint collapse”로 보기는 어렵다.

또한 제공된 영상이 두 Run 모두 **final model_4997**에 정확히 연결돼 있으므로, 이번 완성 정책 행동 비교의 대표 checkpoint는 A/B 모두 final 4997로 유지한다.

---

## 6. 6지형 영상 직접 관찰

### 6.1 관찰 범위

12개 MP4를 디코딩해 metadata를 확인하고, 각 영상에서 0.5/3/5.5/8/10.5/13/15.5/18/19.5초 full-frame을 A/B 동일 시각으로 비교했다. 자세 확인을 위해 5/10/13/16/19초 robot-centered crop도 만들었다.

추가로:

- `slope_up_10deg`: 9.50–11.50초를 0.25초 간격으로 dense sampling
- `boxes`: 10.00–12.00초를 0.25초 간격으로 dense sampling

을 확인했다.

따라서 아래는 **전체 50 fps를 사람 눈으로 실시간 재생한 판독**이 아니라, 전 구간의 균등 sampling + 차이가 큰 구간의 dense frame inspection이다. 짧은 순간의 transient stumble을 완전히 배제하는 근거로 쓰지 않는다.

### 6.2 지형별 비교

| terrain | A — H-010 0.25 | B — control 0.20 | 공통/판단 한계 |
|---|---|---|---|
| **stairs** | 약 13초 계단 접근, 16초 부근 접촉/통과, 19초에는 계단이 뒤로 빠진 평지 장면. sampled frames에서 upright 유지. | 매우 유사한 진행. 13초 접근, 16초 전후 계단 구간, 19초 평지. | 둘 다 명확한 stall/낙상 없음. command·difficulty 미기록이라 미세 속도 우열은 보류. |
| **inverted_stairs** | 5–10초 계단 구조 안/근처, 13초부터 이탈, 16–19초 평지. | 동일하게 5–10초 계단, 13–16초 이탈, 19초 평지. | 둘 다 obstacle traversal 정성 증거. A/B 우열은 크지 않음. |
| **boxes** | 10초 dense field 안, 10–12초 dense sampling에서 장애물을 지나 경계로 이동, 약 12–13초에는 평지로 빠져나옴. 16초는 확실한 평지. | 10–12초 계속 dense field 내. 13/16/19초 sampled frame에서도 box structure가 robot 주변에 남아 있음. | **가장 큰 행동 차이.** A가 훨씬 빠르게 box field를 벗어나는 관찰. 그러나 video command/seed가 matched임을 manifest가 보장하지 않아 causal speed gain으로 확정하지 않음. |
| **random_rough** | 5–16초 rough patch 내 보행, 19초에는 평지. | 5–16초 rough patch 내 보행, 19초에는 평지. | 둘 다 통과하는 정성 증거. 큰 차이 없음. |
| **slope_up_10deg** | 5/10/13/16/19초 upright. 9.5–11.5초 0.25초 sequence에서 좌우 다리가 번갈아 swing/support. 지속 한발 hopping 패턴은 확인되지 않음. | 동일하게 alternating gait, upright. | terrain boundary가 화면상 뚜렷하지 않고 command 미기록. “10° 성공률” 같은 정량 주장은 불가. |
| **slope_down_10deg** | sampled frames에서 upright, 보행 지속. | sampled frames에서 upright, 보행 지속. | 명백한 낙상/stall 차이는 없음. exact slope parameter·command 미확인. |

### 6.3 `feet_air_time=0.25`의 예상 부작용 점검

가설상 가장 중요한 실패 패턴은 “발을 더 오래 들기 위해 한 발 hopping/skip을 고착”하는 것이다.

이번 영상에서:

- slope-up dense sequence 9.5–11.5초: A와 B 모두 support leg가 교대
- boxes dense sequence 10–12초: A는 장애물에서 평지로 진행하며 한 다리 고정 hopping이 지속되지 않음
- 6지형 uniform samples에서도 A가 한쪽 다리만 계속 들고 있는 지속 패턴은 확인되지 않음

따라서 **0.25가 즉시 reward-hacking hopping을 유발했다는 반대 증거는 없다.**

반면 training late-500에서 `joint_deviation_hip`과 `joint_deviation_torso` penalty가 A에서 더 음수이므로, 더 큰 leg excursion/정렬 비용을 치르는 trade-off 가능성은 남는다. 영상만으로 이를 각도 수치로 바꾸지는 않는다.

### 6.4 수치와 영상의 교차검증

수치상 A는 terrain을 크게 높이지 않았고 XY도 거의 동일하다. 영상에서도 stairs/inverted/rough/slope 계열은 대부분 비슷하게 보인다. 이 둘은 일치한다.

수치상 A의 late yaw/base-contact가 조금 낫다. sampled 영상에서도 A가 더 불안정해 보이거나 지속 hopping을 보이는 반대 현상은 없다. 하지만 yaw command 값이 영상에 기록되지 않아 영상으로 yaw 개선을 직접 재현했다고 말할 수는 없다.

`boxes`의 큰 진행 차이는 training scalar의 작은 평균 차이보다 훨씬 커 보인다. 이것은 흥미로운 positive signal이지만, 바로 그 크기 때문에 **video command/seed mismatch라는 경쟁 설명을 먼저 제거해야 한다.**

---

## 7. 핵심 발견과 자기검토

### 발견 1 — A의 가장 강한 정량 신호는 late yaw 개선

**관찰**

- late-500 yaw: `1.36436 vs 1.42790`, A `-0.06354` (~4.45%)
- last-300 yaw: `1.34583 vs 1.40977`, A `-0.06394`
- 초기 200에서는 A가 오히려 `+0.02835` 더 나빴음

**해석**

`feet_air_time=0.25`가 즉시 yaw를 좋게 만든 것이 아니라 adaptation 이후 보행 phase/foot placement가 바뀌면서 회전 추종을 조금 도왔을 가능성이 있다.

**경쟁 설명**

- terrain realization 차이
- 같은 single seed 안의 stochastic policy update 차이
- curriculum exposure 미세 차이

**반대 근거**

- linear XY는 개선되지 않았다.
- terrain도 late-500에서 A가 아주 조금 낮다.

**판별 방법**

기존 final A/B를 동일 yaw command sequence의 fixed evaluator에 넣고 x/y/yaw error를 분리 측정한다.

---

### 발견 2 — A의 survival 방향 신호는 작지만 일관적

**관찰**

late-500:

- base-contact `-0.599%p`
- timeout `+0.590%p`
- episode length `+6.88`

last-300에서도 방향은 유지하나 효과 크기는 줄어든다.

**해석**

0.25가 더 적극적인 foot clearance를 제공하면서 obstacle contact/termination을 약간 줄였을 가능성.

**경쟁 설명**

training termination tag는 evaluator fall rate가 아니고 curriculum/episode distribution 변화의 영향을 받는다.

**반대 근거**

terrain 평균은 증가하지 않았고 B도 이미 높은 terrain 수준이다.

**판별 방법**

matched evaluator에서 실제 fall/termination count와 obstacle progress를 같이 측정한다. 생존만 보고 stall을 성공으로 처리하지 않는다.

---

### 발견 3 — terrain/XY를 희생하지 않은 것이 중요하지만 “개선”은 아님

**관찰**

late-500 terrain/XY 차이는 거의 0.

- terrain `-0.0108`
- XY `+0.00019`

last-300에서는 둘 다 A가 아주 조금 낫다.

**해석**

A의 변화가 기존 corrected H-008의 주된 linear/terrain 능력을 무너뜨리지는 않았다.

**경쟁 설명**

평균 scalar가 비슷해도 특정 terrain의 worst-case가 달라질 수 있다.

**반대 근거**

boxes video에서는 큰 차이가 보인다. 평균 scalar가 이를 설명하지 못한다.

**판별 방법**

terrain별 fixed progress metric을 분리한다. 평균 curriculum level만으로 boxes/steps 차이를 흡수하지 않는다.

---

### 발견 4 — 자세 비용 trade-off가 존재

**관찰**

late-500 same-weight logged term:

- hip deviation penalty magnitude A가 약 4.2% 큼
- torso deviation penalty magnitude A가 약 8.9% 큼

**해석**

조금 더 긴/과감한 swing이 hip/torso 정렬 비용을 늘렸을 가능성.

**경쟁 설명**

reward term은 episode aggregate이며 직접 joint-angle RMS가 아니다.

**반대 근거**

orientation, ang-vel, slide, action-rate term은 거의 같거나 A가 약간 덜 penalty다. 영상에도 명백한 지속 자세 붕괴는 없다.

**판별 방법**

fixed evaluator에서 hip/torso deviation 원시 metric 또는 base pitch/roll을 같이 기록한다.

---

### 발견 5 — boxes 영상은 유망하지만 가장 먼저 통제해야 할 confound

**관찰**

A는 약 12–13초에 boxes를 빠져나가고 B는 19초에도 boxes 구조가 주변에 남는다.

**해석**

A가 obstacle clearance/progress를 실제로 얻었을 가능성.

**경쟁 설명**

video suite의 command, seed, difficulty, initial pose가 manifest에 없으므로 동일 과제라고 보장할 수 없다.

**반대 근거**

training terrain 평균은 거의 동률이고 XY도 거의 같다. 영상만큼 큰 평균 차이는 없다.

**판별 방법**

동일 boxes patch/seed + 동일 fixed forward command로 두 final checkpoint를 paired 실행한다. 이 한 번의 평가가 현재 결정에 가장 많은 정보를 준다.

---

## 8. 현재 프로젝트 판단

### 8.1 실행

| Run | 판정 |
|---|---|
| A H-010 R02 AIRTIME025 corrected +2K | **COMPLETE** — exit 0, global 2998→4997, 21 checkpoints, evidence PASS |
| B H-008 corrected unchanged +2K | **COMPLETE** — exit 0, global 2998→4997, 21 checkpoints, evidence PASS |

### 8.2 evidence와 비교

**확인된 것**

- 동일 기록상 parent checkpoint SHA
- 동일 additional 2K
- 실제 reward single-delta `0.20→0.25`
- 동일 source/PPO/seed/num_envs
- raw TensorBoard 전체 2K trajectory
- final checkpoint ↔ 6 video SHA provenance
- 두 train archive와 video archive checksum 정상

**답할 수 있는 질문**

- corrected sibling 안에서 0.25가 학습 후반 지표를 어느 방향으로 바꿨는가
- final policy가 6 terrain 영상에서 어떤 정성 행동을 보이는가

**아직 답할 수 없는 질문**

- 공식 시뮬레이션 점수가 더 높은가
- 동일 evaluator에서 terrain별 성공률이 더 높은가
- 복수 seed에서 일반화되는가
- boxes 영상 차이가 동일 command/seed에서도 재현되는가

### 8.3 가설

**H-010 R02 AIRTIME025: `PROMOTE` — 단, 범위는 PERSONAL corrected-lineage screening에서 “paired evaluator 단계로 승격”이다.**

근거:

1. corrected unchanged control과 실제 single-variable sibling이 성립
2. late yaw 개선이 last-500/last-300에서 반복
3. base-contact/timeout/episode-length가 같은 방향
4. terrain/XY를 거의 잃지 않음
5. optimizer 안정
6. final 6-terrain 영상에서 지속 hopping 부작용 미관찰
7. boxes에서 유망한 traversal 차이

제약:

- hip/torso deviation penalty 소폭 악화
- single seed
- fixed evaluator 없음
- video command/seed mismatch 가능

따라서 이 `PROMOTE`는 **제출 채택, OFFICIAL 우월성, 최적 reward 확정**을 뜻하지 않는다.

### 8.4 정책

**A final `model_4997.pt`**

- SHA: `fd497dcb...47e5df`
- 영상 source 정확히 연결됨
- auto `model_best`와도 동일
- late collapse 없음
- 강점: yaw/survival 방향 소폭 개선, boxes에서 강한 qualitative progress signal
- 약점: hip/torso deviation term 소폭 악화, official/fixed-eval 미확인

**B final `model_4997.pt`**

- SHA: `4349fe56...3b5b6d`
- 영상 source 정확히 연결됨
- auto best는 `model_4900`, final은 별도
- late joint collapse 없음
- corrected unchanged continuation으로서 유효한 control

---

## 9. 다음 한 번의 행동

### 우선순위 1 — **새 학습 없이 A/B final fixed paired evaluation**

비교할 checkpoint:

- A: `model_4997.pt` SHA `fd497dcb...47e5df`
- B: `model_4997.pt` SHA `4349fe56...3b5b6d`

맞출 조건:

- 동일 evaluator 구현/version
- 동일 terrain class + difficulty
- 동일 initial-state policy
- 동일 command sequence
- 동일 evaluator seed set
- 동일 horizon
- 동일 camera는 영상 비교용으로만 고정
- 각 policy를 같은 episode set에 대응 평가

기록할 최소 metric:

- terrain별 실제 progress / obstacle traversal
- x/y/yaw tracking error
- base-contact termination / timeout
- stall time
- base pitch/roll 또는 posture metric
- foot slide
- 가능하면 one-foot support duration / gait asymmetry
- paired native video

특히 **boxes**를 포함해야 한다. 현재 영상에서 가장 큰 차이가 여기 있기 때문이다.

### 결과별 다음 결정

- **A가 matched boxes/progress와 yaw에서 재현되고 survival이 유지**  
  → H-010을 OFFICIAL confirmation 후보로 유지. 새 공식 학습을 한다면 corrected same parent/control 조건을 보존한다.

- **yaw만 좋아지고 boxes/progress 차이는 사라짐**  
  → “0.25는 yaw-oriented trade-off”로 재분류. terrain traversal 개선 가설은 철회.

- **A가 posture/fall에서 악화하거나 progress 차이가 사라짐**  
  → `HOLD` 또는 `REJECT`; 0.20 control 유지.

- **두 정책이 evaluator에서도 사실상 동률**  
  → 추가 GPU 학습보다 0.20을 단순성/control 기준으로 유지하고 다음 reward 질문으로 이동.

이 평가는 **기존 checkpoint만 사용**하므로 reward 재학습보다 정보비용이 낮고, 현재 가장 큰 불확실성인 “영상의 unmatched command/seed”를 직접 제거한다.

---

## 10. 한계와 재확인 가능한 근거 목록

### 한계

1. parent `model_2998.pt` 원본 바이트는 이번 네 파일에 포함되지 않아 parent SHA는 child metadata 기록을 신뢰한 연결이다.
2. 두 train은 single seed 42다.
3. terrain generator seed가 `null`이라 training seed만으로 동일 terrain realization을 보장하지 않는다.
4. video manifest에는 command, video seed, difficulty/curriculum level, camera 파라미터가 없다.
5. 영상 분석은 전체 구간 uniform sampling + 핵심 구간 dense sampling이며 모든 50 fps 프레임을 실시간 육안 판독한 것은 아니다.
6. training `base_contact`는 공식 evaluator fall rate가 아니다.
7. curriculum level은 fixed difficulty pass rate가 아니다.
8. total reward와 changed `feet_air_time` term은 weight 차이 때문에 성능 비교에 사용하지 않았다.
9. PERSONAL 결과이므로 OFFICIAL score/제출 성능으로 승격하지 않는다.

### 원본 내부 재확인 위치

A train root:

`20260925-102659-h1-h010-r02-airtime025-corrected-h1-corrected-20/`

- `metadata.json` — 실행/parent/source checkpoint identity
- `validation.json` — evidence PASS
- `command.txt` — 실제 train command
- `source/humanoid_rewards.py` — 실제 reward weight
- `source/identity.json` — task source before/after hash
- `native_run/params/env.yaml` — effective env/reward
- `native_run/params/agent.yaml` — PPO/iteration config
- `native_run/events.out.tfevents...` — raw 2K scalar
- `console.log` — final iteration/endpoint/exit context
- `checkpoints/model_4997.pt` — final
- `collected/exported/model_best.pt` — A에서는 final과 동일

B train root:

`20260925-091257-h1-h008-corrected-control-to5k-h1-corrected-2026/`

동일 구조. B의 `model_best.pt`는 `model_4900.pt`와 hash 동일.

A video root:

`checkpoint-h1-model_4997-fd497dcb7a76/`

B video root:

`checkpoint-h1-model_4997-4349fe565013/`

각각:

- `video_suite_manifest.json`
- `videos/stairs.mp4`
- `videos/inverted_stairs.mp4`
- `videos/boxes.mp4`
- `videos/random_rough.mp4`
- `videos/slope_up_10deg.mp4`
- `videos/slope_down_10deg.mp4`

---

## 최종 판정

**실행:** A COMPLETE / B COMPLETE  
**Evidence:** train/video provenance와 checksum 모두 강함  
**비교 설계:** corrected sibling single-variable 비교 성립; single-seed 조건부  
**가설:** **PROMOTE — fixed paired evaluator 단계로**  
**정책 대표:** A/B 모두 final `model_4997.pt`  
**현재 A의 장점:** late yaw error 감소, base-contact/timeout 방향 개선, terrain/XY 유지, boxes qualitative progress  
**현재 A의 손실:** hip/torso deviation penalty 소폭 증가, 명확한 terrain 평균 향상 없음  
**가장 먼저 풀 불확실성:** boxes를 포함한 **동일 command/seed fixed evaluator**에서 final A/B 행동 차이가 재현되는가  
**새 학습 필요 여부:** 지금은 **불필요**. 기존 두 final checkpoint의 paired evaluation이 먼저다.
