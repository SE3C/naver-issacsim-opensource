> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/incoming/other/reviewed/H1_H005_OFFICIAL10K_VS_TERM50_OFFICIAL5K_DEEP_ANALYSIS_20260928.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# H1 H-005 OFFICIAL 10K vs TERM50 OFFICIAL 5K 심층 분석

- 작성일: 2026-09-28
- A: **H-005 Run 05 — OFFICIAL fresh 10K** (`feet_air_time=0.25`, `termination_penalty=-50`)
- B: **TERM50 — OFFICIAL fresh 5K** (`feet_air_time=0.20`, `termination_penalty=-50`)
- 보조 근거: H-005 PERSONAL fresh 3K, corrected H-005 3K, corrected H-001 unchanged control 3K
- 분석 범위: 제공된 학습 archive, raw TensorBoard event, console/config/source, 선택 checkpoint, H-005 6지형 MP4
- 수행하지 않은 작업: 새 학습, 새 렌더링, export, 서버 조작, 외부 게시, 원본 삭제/교체

## 1. 결론 요약

### 질문 1 — 이번 정책은 목표 행동을 실제로 얼마나 수행하는가?

**학습 내부 지표상 H-005 10K는 후반까지 무너지지 않고 안정성이 개선된 정책이다.** 마지막 500 iteration(`9500–9999`) 평균은 terrain `5.8065`, XY error `0.3656`, yaw error `0.8843`, training base-contact termination `25.881%`, mean episode length `820.19`였다. `9000–9499` 대비 terrain은 다소 내려왔지만 XY/yaw/base-contact가 함께 붕괴하는 형태는 아니며, `9700–9999`에서도 유사한 수준을 유지했다.

6개 영상에서는 **boxes와 random_rough에서 실제 지형 진행이 화면상 확인**되고, inverted_stairs에서도 여러 지형 띠를 지나 평지 쪽으로 이동한다. 6개 모두 촘촘한 프레임 샘플에서 몸통이 바닥에 닿는 명백한 전도는 확인하지 못했다. 다만 **stairs는 중앙 계단을 여러 단 명확히 상승했다고 보기 어렵다.** 약 14초 이후 계단 영역에 들어가지만 가장자리/비스듬한 경로를 따라 움직이는 장면이어서, 생존과 계단 traversability를 분리해야 한다. 경사 두 영상은 upright locomotion은 보이지만 추적 카메라와 미확인 command 때문에 정확한 경사 방향 진행량을 판정할 수 없다.

따라서 현재 증거가 지지하는 표현은 **“여러 지형에서 upright locomotion과 실제 진행을 보이는 10K 정책”**이지, “6지형을 모두 확실히 통과하며 command를 정확히 추종한다”는 주장은 아니다.

### 질문 2 — 비교 정책과의 차이 중 무엇이 관찰이고, 무엇을 reward 변경 효과로 해석할 수 있는가?

가장 중요한 발견은 **H-005 자체의 0–4999 구간을 TERM50 fresh 5K와 같은 학습 stage로 맞춰 비교할 수 있다는 점**이다. 두 공식 Run은 reward source에서 실질적으로 `feet_air_time 0.20→0.25`만 다르고, H1 env/PPO 핵심 설정·seed 42·4096 env·Isaac Lab commit이 맞는다. 그러나 terrain generator seed가 `null`이고 단일 seed이며, H-005 run은 처음부터 `max_iterations=10000`, 저장 간격 50으로 실행된 차이가 있어 완전한 통제 실험이라고 부르지는 않는다.

같은 5K stage의 late-500 비교에서는 H-005 0.25가 TERM50 0.20보다:

| 지표 | H-005 0.25, 4500–4999 | TERM50 0.20, 4500–4999 | A-B | 해석 |
| --- | ---: | ---: | ---: | --- |
| terrain level | 5.6570 | 5.7306 | -0.0736 | H-005가 낮음 |
| XY error | 0.3655 | 0.3690 | **-0.0035** | H-005가 아주 조금 낮음 |
| yaw error | 0.9642 | 0.9213 | **+0.0429** | H-005가 높음 |
| base-contact termination | 28.549% | 28.150% | **+0.399%p** | H-005가 높음 |
| episode length | 790.29 | 796.02 | -5.73 | H-005가 짧음 |

XY의 작은 이득은 window에 민감하다. 인접 late-300에서는 XY 방향이 약간 반대로 바뀌며, terrain/yaw/base-contact/episode length의 불리한 방향은 유지된다. 즉 **5K stage에서 feet 0.25가 명확한 전반 개선을 만들었다는 증거는 없다.**

반면 H-005를 5K stage에서 10K까지 계속 학습했을 때는 late-500 기준 terrain `+0.1495`, yaw error `-0.0799`, base-contact `-2.668%p`, episode length `+29.90`의 개선이 나타난다. XY는 사실상 동일하다. 이 변화는 **같은 reward로 추가 5K 학습한 효과와 학습 phase 변화**가 섞인 것이므로 `feet_air_time=0.25`의 효과로 귀속할 수 없다.

PERSONAL corrected 같은-parent 3K 비교도 같은 방향의 경계를 준다. H-005 0.25는 unchanged H-001 0.20보다 late-500 XY가 `0.3609 vs 0.3695`로 낮지만, terrain `5.4776 vs 5.5010`, base-contact `29.761% vs 29.616%`, episode length `773.75 vs 777.66`은 약간 불리하고 yaw 차이는 작다. **작은 XY 신호 + 나머지 축 중립/작은 trade-off**라는 결론이 공식 5K stage 비교와 대체로 양립한다.

### 질문 3 — 현재 내려야 할 결정과 먼저 해결할 불확실성은 무엇인가?

- **실행:** `COMPLETE`. H-005 Run 05는 exit 0, evidence validation PASS, native finalize complete, official backup success다.
- **가설:** **PROMOTE — 단, fixed paired evaluation 단계로만 승격. final adoption은 HOLD.** 5K matched-stage 학습 scalar에서 0.25의 확실한 우위는 없고, 10K 후반의 개선은 추가 학습 효과와 분리되지 않는다.
- **정책:** H-005 10K는 행동 후보로 충분히 유망하지만, 현재 6영상은 checkpoint source가 독립 연결되지 않았고 stairs traversability가 불명확하다.
- **checkpoint:** 자동 best `model_9800.pt`와 최신 numbered `model_9950.pt` 중 현재 자료만으로 행동상 우위를 확정하지 않는다. fresh Run이므로 “긴 resume는 final 기본” 원칙을 기계적으로 적용하지 않는다.
- **다음 한 번의 행동:** 새 학습이 아니라 **기존 `H005 model_9800`, `H005 model_9950`, `TERM50 model_4900`을 동일 fixed evaluator에 한 번에 넣는 3-policy paired evaluation**이 정보가 가장 크다. 같은 terrain/command/seed/evaluator/window에서 x/y/yaw error, survival/base-contact, 실제 진행거리·stall, 지형 통과, posture를 함께 기록하면 제출 후보와 checkpoint 선택을 동시에 좁힐 수 있다.

---

## 2. 실제로 받은 자료와 Run identity

### 2.1 입력 자료의 역할

`README_분석시작(1).md`의 지시에 따라 직접 근거는 H-005 OFFICIAL 10K archive, H-005 6영상 ZIP, H-005 report, Round 2 공식 평가 기록으로 두었다. TERM50 OFFICIAL 5K는 과거 공식 기준이며, PERSONAL 3K 세 Run은 reward 가설·학습 경로를 해석하는 보조 비교로만 사용했다.

H-005 OFFICIAL archive는 업로드 제한 때문에 **후반 numbered checkpoint만 남긴 분석용 사본**이지만 TensorBoard, console, 설정, source, report는 유지돼 있다. 따라서 0–9999 학습 시계열은 raw event로 재계산할 수 있으나, archive 안에서 모든 0–6999 checkpoint 바이트를 다시 검사할 수 있는 구조는 아니다.

### 2.2 A — H-005 OFFICIAL fresh 10K

| 항목 | 확인 결과 |
| --- | --- |
| Robot | H1 / Humanoid-v0 |
| Environment | OFFICIAL, `/workspace/training/humanoid` |
| Run type | **fresh**, checkpoint parent 없음 |
| Evidence run ID | `20260927-123428-h005-fresh10k-official` |
| Native run | `2026-09-27_21-34-34` |
| 실제 명령 | `.../isaaclab.sh -p .../train.py --task Humanoid-v0 --max_iterations 10000 --num_envs 4096 --seed 42 --headless agent.save_interval=50` |
| Seed / envs | 42 / 4096 |
| Iteration | 0–9999, 요청·실행 10,000 |
| 종료 | exit 0, validation PASS, finalize complete, official backup success |
| organizer checkpoint | 200개 보존 기록; 받은 분석 사본에는 후반부 numbered checkpoint 보존 |
| reward 핵심 | `termination_penalty=-50`, `track_lin_vel_xy_exp=0.5`, `feet_air_time=0.25` |
| auto best | reward peak step 9784 → `model_9800.pt` |
| latest numbered | `model_9950.pt` |

선택적으로 확인한 SHA-256:

- `collected/exported/model_best.pt` = `organizer_checkpoints/model_9800.pt` = `20d04452c908056c1bacdbf569080e5eb458c26239e9b438aca637453f5f6a2f`
- `organizer_checkpoints/model_9950.pt` = `7665d871c32f81ac392cf41708d9a67a35b8d24106a21ac305c4feb3775b8bb9`

즉 `model_best.pt`는 9800의 별칭이며, 9800을 “마지막 checkpoint”라고 부르면 안 된다.

원본 근거 위치:

- `.../metadata.json`
- `.../command.txt`
- `.../validation.json`
- `.../source/humanoid_rewards.py`
- `.../native_run/params/env.yaml`
- `.../native_run/params/agent.yaml`
- `.../native_run/events.out.tfevents.*`
- `.../console.log`
- `.../organizer_checkpoints/model_9800.pt`, `model_9950.pt`

### 2.3 B — TERM50 OFFICIAL fresh 5K

| 항목 | 확인 결과 |
| --- | --- |
| Robot | H1 / Humanoid-v0 |
| Environment | OFFICIAL |
| Run type | fresh 5K |
| Native run | `2026-09-08_23-23-33` |
| Seed / envs | 42 / 4096 |
| Iteration | 0–4999 |
| reward 핵심 | `termination_penalty=-50.0`, `track_lin_vel_xy_exp=0.5`, `feet_air_time=0.20` |
| 선택 checkpoint | `model_4900.pt` / exported `model_best.pt`와 byte-identical |
| checkpoint SHA-256 | `e7343a96cf861bb700aefda704eda3eaadc42e7caac5a3d35904a6c2d17dabc0` |
| 공식 평가 | Round 2 simulation `56.37/70`, total `86.37/100` |

Round 2의 7개 simulation 항목은 평지 균형 `8.62/10.5`, 전진 `11.24/14`, 좌우 `5.73/7`, 회전 `5.66/7`, 요철 `8.17/10.5`, ±10° 경사 `8.47/10.5`, 밀침 회복 `8.48/10.5`였다. 이는 **TERM50 제출 정책의 실제 공식 평가**이며 H-005 10K의 점수로 이전할 수 없다.

### 2.4 reward/source 및 설정 차이

두 reward source를 직접 diff하면 의미 있는 reward 변경은 다음 하나다.

```text
feet_air_time: 0.20 -> 0.25
termination_penalty: -50.0 -> -50   # 숫자 의미는 동일
```

resolved `env.yaml`의 실질 차이도 log path와 `feet_air_time.weight`가 핵심이며, scene/command/terrain/나머지 reward 구조는 동일 계열이다. PPO도 같은 기본 설정을 사용한다. 확인된 공통 핵심은 rollout 24 steps/env/iteration, PPO epochs 5, mini-batches 4, initial LR `1e-3` adaptive, gamma `0.99`, lambda `0.95`, entropy coefficient `0.008`, desired KL `0.01`, clip `0.2`, actor/critic `[512,256,128]`이다.

agent 설정 차이는 H-005 `max_iterations=10000, save_interval=50`, TERM50 `max_iterations=5000, save_interval=100`이다. 이 차이를 reward 효과라고 해석하지 않는다.

두 Run의 Isaac Lab 기록은 동일 commit `3e73d6dd79080fd7632488c061052a6edd52e230` 계열이며 clean diff를 기록한다.

### 2.5 영상 identity

`H005_OFFICIAL_6videos(1).zip`에는 다음 6개 MP4만 있고 `video_suite_manifest.json` 또는 checkpoint SHA sidecar가 없다.

- `boxes.mp4`
- `stairs.mp4`
- `inverted_stairs.mp4`
- `random_rough.mp4`
- `slope_up_10deg.mp4`
- `slope_down_10deg.mp4`

6개 모두 H.264, 1920×1080, 50 fps, 약 19.98초, 999 frames로 확인했다.

**중요한 provenance 한계:** 영상 파일 생성 시각이 학습 종료 뒤라는 정황만으로 9800/9950 중 어느 checkpoint인지 증명할 수 없다. loose `policy.pt`의 source checkpoint 역시 이번 train evidence가 독립 연결하지 않는다. 따라서 이 보고서의 영상 관찰은 **“받은 H-005 영상 정책”**에만 귀속하며, `model_9800` 또는 `model_9950`의 행동이라고 단정하지 않는다.

---

## 3. 비교 설계와 해석 가능한 범위

| 비교 | 부모/학습 경로 | reward 차이 | 학습량/환경 | 평가 자료 | 판정 |
| --- | --- | --- | --- | --- | --- |
| H-005 OFFICIAL 0–5K vs TERM50 OFFICIAL 5K | 둘 다 fresh | feet `0.20→0.25` | 둘 다 5K stage, seed42/4096; H-005 전체 max_iterations는 10K | raw training TB | **조건부 직접 비교** |
| H-005 OFFICIAL 10K vs TERM50 OFFICIAL 5K | fresh vs fresh | feet 차이 + 학습량 차이 | 10K vs5K | TB + B 공식 score | **완성 정책 맥락 비교**; feet 인과효과 판단 불가 |
| corrected H-005 PERSONAL 3K vs H-001 unchanged PERSONAL 3K | 동일 corrected parent 1499에서 +1.5K sibling | feet `0.20→0.25` | PERSONAL, seed42/4096 | raw training TB | **reward 질문에 가장 직접적인 보조 대조**; 공식 성능 아님 |
| H-005 OFFICIAL 3K vs H-005 PERSONAL fresh 3K | 둘 다 fresh, 동일 H-005 config | reward 동일 | OFFICIAL vs PERSONAL | raw TB | **재현성/변동 규모 참고** |
| H-005 6영상 vs TERM50 행동 | B에 동등한 six-terrain provenance 자료 없음 | — | unmatched | A만 6영상 | **행동 A/B 판단 불가** |

### 동일 seed의 한계

H1 terrain generator 설정에서 seed는 `null`, cache는 false다. 학습 seed 42가 같아도 실제 terrain realization이나 reset 이후 command/episode를 완전히 paired라고 볼 수 없다. 따라서 단일 seed의 작은 차이를 통계적 일반화로 부르지 않는다.

### “같은 5K stage” 비교의 가치와 한계

H-005는 fresh 10K Run이므로 raw TensorBoard의 `0–4999` prefix가 존재한다. 따라서 TERM50 5K와 **동일 iteration stage의 학습 상태**를 비교할 수 있다. 이는 10K endpoint와 5K endpoint를 바로 비교하는 것보다 feet 변경 질문에 훨씬 직접적이다.

다만 H-005는 시작부터 10K 실행 인자를 가지고 있었고 save interval도 다르며, curriculum terrain 생성은 완전 고정 paired가 아니다. 따라서 “단일 reward의 확정 인과효과”보다 **통제에 가까운 단일-seed 관찰**로 해석한다.

---

## 4. raw TensorBoard 재분석

### 4.1 처리 방법

각 archive의 `events.out.tfevents.*`를 직접 TFRecord/Event proto로 파싱했다. 분석한 5개 Run 모두 공통 31개 scalar tag를 가졌다.

주요 iteration-indexed tag는:

- `Curriculum/terrain_levels`
- `Metrics/base_velocity/error_vel_xy`
- `Metrics/base_velocity/error_vel_yaw`
- `Episode_Termination/base_contact`
- `Episode_Termination/time_out`
- `Train/mean_episode_length`
- `Policy/mean_std`
- `Train/mean_reward`
- 관련 `Episode_Reward/*`, `Loss/*`

H-005 OFFICIAL은 각 주요 tag가 10,000 points, step `0..9999`; TERM50은 5,000 points, `0..4999`; PERSONAL fresh는 3,000 points, `0..2999`; resume 두 Run은 1,500 points, global `1499..2998`이었다. 주요 iteration tag에는 중복 step이 없고 비유한 NaN/Inf도 발견하지 않았다.

`Train/mean_reward/time`, `Train/mean_episode_length/time`은 wall-time 성격의 step alias가 있어 iteration 시계열 비교에서는 제외했다. 이 처리가 raw training scalar를 임의로 smoothing하거나 자동 report window와 혼합하지 않는다.

### 4.2 H-005 OFFICIAL 10K 학습 경과

| window | terrain | XY err | yaw err | base-contact | timeout | ep length | std | mean reward |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0–499 | 0.8487 | 0.4078 | 1.2040 | 65.090% | 34.471% | 484.58 | 0.9641 | -0.6368 |
| 2500–2999 | 5.3968 | 0.3600 | 1.0115 | 29.882% | 70.133% | 770.94 | 1.3452 | 2.8975 |
| 4500–4999 | 5.6570 | 0.3655 | 0.9642 | 28.549% | 71.468% | 790.29 | 1.3130 | 3.5394 |
| 7000–7499 | 5.8134 | 0.3784 | 0.9123 | 26.728% | 73.282% | 811.57 | 1.2919 | 4.0152 |
| 8000–8499 | 5.7978 | 0.3766 | 0.9167 | 26.322% | 73.689% | 818.01 | 1.2819 | 4.1776 |
| 8500–8999 | 5.8291 | 0.3741 | 0.8994 | 25.207% | 74.804% | 827.47 | 1.2756 | 4.4494 |
| 9000–9499 | 5.8809 | 0.3775 | 0.8890 | 25.871% | 74.138% | 822.71 | 1.2740 | 4.4337 |
| **9500–9999** | **5.8065** | **0.3656** | **0.8843** | **25.881%** | **74.143%** | **820.19** | **1.2723** | **4.5116** |
| 9700–9999 | 5.7918 | 0.3638 | 0.8867 | 25.948% | 74.076% | 819.77 | 1.2744 | 4.4904 |

**관찰:** 후반 terrain은 9000–9499에서 높았다가 마지막 500에서 약간 낮아지지만, yaw는 계속 낮아지고 base-contact/episode length가 동시에 악화하지 않는다. 따라서 “마지막 수백 iteration 공동 붕괴”는 보이지 않는다.

**주의:** `Episode_Termination/base_contact`는 training episode 집계다. 정의 확인 없이 고정 evaluator의 실제 fall probability 또는 공식 survival로 바꾸지 않았다.

### 4.3 TERM50 OFFICIAL 5K

| window | terrain | XY err | yaw err | base-contact | timeout | ep length | std | mean reward |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0–499 | 0.8048 | 0.4048 | 1.1304 | 69.361% | 30.205% | 469.09 | 0.9567 | -0.7287 |
| 2500–2999 | 5.5197 | 0.3636 | 0.9845 | 29.574% | 70.435% | 776.91 | 1.3158 | 3.0798 |
| 4000–4499 | 5.7345 | 0.3807 | 0.9528 | 28.547% | 71.471% | 791.59 | 1.3049 | 3.3488 |
| **4500–4999** | **5.7306** | **0.3690** | **0.9213** | **28.150%** | **71.864%** | **796.02** | **1.2919** | **3.7008** |
| 4700–4999 | 5.7284 | 0.3634 | 0.9119 | 28.035% | 71.979% | 796.38 | 1.2909 | 3.7800 |

두 Run은 reward weight가 다르므로 `Train/mean_reward` 절댓값을 정책 성능 순위로 쓰지 않았다.

### 4.4 같은 5K stage의 feet 0.25 vs 0.20

late-500의 핵심은 앞선 요약 표와 같다. 인접 window 민감도도 확인했다.

- late-300: terrain H-005가 약 `-0.0468`, yaw error 약 `+0.0453`, base-contact 약 `+0.710%p`, episode length 약 `-8.56`; XY는 H-005가 오히려 아주 약간 높아지는 방향.
- late-200: terrain 약 `-0.0453`, yaw 약 `+0.0428`, base-contact 약 `+0.938%p`, episode length 약 `-9.97`; XY 차이는 거의 0.

즉 **XY 이득은 작고 window 선택에 민감하지만, terrain/yaw/base-contact/episode length의 방향은 더 일관되게 H-005 5K 쪽에 불리하다.**

이것만으로 feet 0.25를 REJECT할 정도의 일반화 근거는 아니다. 그러나 “0.25가 5K에서 명확히 더 좋은 gait/terrain을 만들었다”는 가설은 현재 공식 raw scalar가 지지하지 않는다.

### 4.5 H-005에서 5K → 10K로 더 학습한 변화

동일 H-005 설정의 late-500끼리 비교하면:

| 지표 | H-005 5K stage | H-005 10K stage | 변화 |
| --- | ---: | ---: | ---: |
| terrain | 5.6570 | 5.8065 | +0.1495 |
| XY error | 0.3655 | 0.3656 | +0.0001 |
| yaw error | 0.9642 | 0.8843 | **-0.0799** |
| base-contact | 28.549% | 25.881% | **-2.668%p** |
| episode length | 790.29 | 820.19 | **+29.90** |

**해석:** H-005는 후반 추가 학습에서 안정/회전 축이 실제로 더 좋아졌다. 그러나 이 결과는 `feet=0.25`가 `0.20`보다 우수하다는 증명이 아니라 **0.25 설정도 10K까지 계속 학습하면 더 나아질 수 있음**을 보여준다.

가장 직접적인 경쟁 설명은 TERM50도 10K까지 같은 조건으로 학습했으면 비슷하거나 더 큰 후반 개선이 있었을 가능성이다. 현재 TERM50 10K unchanged control이 없으므로 이를 분리할 수 없다.

### 4.6 PERSONAL same-parent 단일변수 대조

corrected H-001 `feet=0.20` parent에서 동일 +1.5K를 이어간 두 sibling의 late-500:

| 지표 | H-005 0.25 | H-001 unchanged 0.20 | A-B |
| --- | ---: | ---: | ---: |
| terrain | 5.4776 | 5.5010 | -0.0234 |
| XY error | 0.3609 | 0.3695 | **-0.0086** |
| yaw error | 1.0410 | 1.0455 | -0.0045 |
| base-contact | 29.761% | 29.616% | +0.145%p |
| episode length | 773.75 | 777.66 | -3.91 |

이 비교는 reward 단일변수 질문에는 더 직접적이지만 PERSONAL 단일 seed다. **작은 XY 개선과 나머지 축 거의 중립/작은 손해**라는 수준으로만 읽는다.

### 4.7 동일 H-005 설정의 OFFICIAL vs PERSONAL fresh 3K

late-500에서 OFFICIAL H-005와 PERSONAL fresh H-005는 reward/env 구조가 같아도 terrain이 약 `0.107`, XY가 약 `0.014` 차이났다. 이는 서버/terrain realization/비결정성 등으로 같은 선언 설정에서도 이 정도 차이가 생길 수 있음을 보여주는 내부 경보다. 따라서 0.003~0.009 수준의 단일-seed tracking 차이를 과도하게 일반화하지 않는다.

### 4.8 행동 비용과 최적화 안정성

5K matched-stage late-500에서 H-005는 TERM50 대비:

- `feet_slide`: 거의 동일, H-005가 아주 약간 덜 음수
- `flat_orientation_l2`: H-005가 약간 더 큰 비용
- `joint_deviation_hip`: 거의 동일
- `joint_deviation_torso`: H-005가 약간 덜 큰 비용
- `action_rate_l2`: H-005가 약간 더 큰 비용

`feet_air_time` weighted reward term은 weight 자체가 0.20/0.25로 다르므로 값만 나눠 실제 비가중 gait quantity를 복원하지 않았다. term의 normalization/episode aggregation 정의를 별도 검증하지 않았기 때문이다.

H-005 후반 loss는 finite하며 value loss가 약 `0.005` 전후, surrogate가 약 `-0.01`대에서 유지된다. event에 KL scalar는 없으므로 KL 안정성을 수치로 주장하지 않는다. `Policy/mean_std≈1.27`은 낮지 않지만 std 하나로 정책 실패를 판정하지 않았다. console에서도 Traceback/CUDA OOM/NaN/Inf와 같은 치명적 학습 오류를 발견하지 않았다.

---

## 5. 6지형 영상 행동 분석

### 5.1 판독 방법과 한계

각 MP4 전체를 디코드했고, 전 구간을 약 0.24–0.25초 간격으로 촘촘하게 샘플링해 총 약 80프레임/지형을 시각 판독했다. boxes와 stairs의 전환 구간은 더 조밀한 프레임으로 보강했다.

따라서 아래는 단순 시작/끝 정지 프레임 몇 장만 본 결과보다 강한 정성 근거지만, **모든 20ms frame을 사람이 연속 판독한 것은 아니다.** 0.2초보다 짧은 순간적 slip/contact 이벤트를 완전히 배제하지 않으며, gait frequency·정밀 속도·각도는 측정값처럼 쓰지 않는다.

화면의 녹색/파란 command visualization은 약 10초 전후에 크게 바뀌는 장면이 있고, 학습 env의 command resampling `10s`와 형태상 부합한다. 그러나 ZIP에 manifest가 없으므로 실제 command vector를 복원하거나 “명령 추종 성공”으로 판정하지 않는다.

### 5.2 지형별 관찰

| terrain / 파일 | H-005 영상 관찰 | 진행/회복 판단 | 주요 한계 |
| --- | --- | --- | --- |
| **boxes.mp4** | 시작부터 boxes 내부. 1–10초 여러 block 사이를 이동하고, 11–13초 전후 큰 다리 들기/방향 변화가 보이지만 sampled frame에서 몸통 전도 없음. 약 14–16초에 조밀한 box 구역을 벗어나 평지로 이동. | **실제 진행 확인.** 높은 스텝이 있으나 지속적 한발 hop으로 보이지 않음. | command·difficulty·source checkpoint 미확인. |
| **random_rough.mp4** | 거의 전 구간 rough patch 위를 이동. 중간에 몸통 기울기와 불균일 step이 있으나 다시 upright. 약 19초대에 rough 경계에서 평지 쪽으로 나옴. | **6개 중 가장 명확한 rough traversal 근거 중 하나.** sampled fall 없음. | world displacement/속도 정량 불가. |
| **inverted_stairs.mp4** | 여러 반복 지형 띠를 지나가며 약 15초대에는 평지 쪽으로 전환. 큰 지속 붕괴 없음. | **지형 영역 진행은 확인.** | 카메라가 위에서 추적하며 exact step count/command 방향 불명. |
| **stairs.mp4** | 0–13초대는 접근/평지. 약 14초부터 stairs가 경로에 들어오지만 로봇은 계단의 왼쪽 가장자리/비스듬한 축을 따라 움직이는 모습. 20초까지 upright. | **생존·이동은 확인, 명확한 중앙 다단 상승은 미확인.** | command가 계단 정면 상승이었는지 모름. “계단 통과 성공” 판정 보류. |
| **slope_up_10deg.mp4** | 20초 동안 upright locomotion 유지, 간헐적 lateral lean 후 자세 회복. sampled full fall 없음. | **경사 장면에서 안정적 이동 sanity check.** | 추적 카메라 때문에 실제 uphill displacement와 command 추종 정량 불가. |
| **slope_down_10deg.mp4** | 유사하게 upright locomotion 지속, 큰 sampled collapse 없음. | **경사 장면의 생존 sanity check.** | downhill 진행량/속도/command 방향 미확인. |

### 5.3 다시 확인 가능한 주요 시각 위치

- `boxes.mp4`: 약 `11.3–13.2s` 큰 leg lift/방향 변화, 약 `14–16s` boxes 밀집 구간에서 평지로 이탈.
- `random_rough.mp4`: 약 `5–10s`, `16–18s` 몸통 기울기·거친 stepping; 약 `19.2–19.9s` rough 경계 이탈.
- `inverted_stairs.mp4`: 약 `14–16s` 반복 띠 지형에서 평지 쪽으로 전환.
- `stairs.mp4`: 약 `14.1s` 이후 stairs 접근, `14.6–19.9s` 계단 가장자리와 나란히/비스듬하게 이동하는 장면.
- `slope_up_10deg.mp4`, `slope_down_10deg.mp4`: 전 구간 upright, 초중반 일부 lateral lean 후 회복.

### 5.4 영상과 수치의 일치·충돌

**일치:** H-005 10K late base-contact 감소와 episode length 증가가 영상의 “짧은 20초 동안 쉽게 무너지지 않음”과 방향상 모순되지 않는다. boxes/random_rough의 실제 패치 진행은 높은 terrain curriculum이 단순 제자리 생존만 의미하는 것은 아니라는 질적 보강 근거다.

**충돌/주의:** training terrain level `~5.8`은 고정 난이도 통과율이 아니며, stairs 영상은 높은 curriculum 수치가 “계단 정면 상승 성공”을 자동 보장하지 않음을 보여준다. 또한 6개 짧은 영상에서 안 넘어졌다는 사실로 training base-contact `~25.9%` 또는 공식 survival을 역산할 수 없다.

TERM50 쪽에 동일한 source-linked six-terrain 영상 묶음이 제공되지 않았으므로, 이 절에서 행동상 A/B 우열은 만들지 않았다.

---

## 6. 핵심 발견별 해석, 경쟁 설명, 반대 근거

### 발견 A — feet 0.25는 5K stage에서 명확한 전반 개선이 아니다

- **관찰:** 공식 5K late windows에서 terrain/yaw/base-contact/episode length는 TERM50 0.20 쪽이 일관되게 유리하고, H-005의 XY 이득은 작고 window에 민감하다.
- **해석:** feet reward를 0.25로 올린 것이 최소한 이 학습 stage에서 terrain/stability/tracking을 동시에 개선하지 않았을 가능성이 높다.
- **경쟁 설명:** terrain generator seed가 null이고 single run이라 실제 terrain sequence 차이가 섞일 수 있다. H-005는 전체 run horizon/save interval도 다르다.
- **반대 근거:** PERSONAL corrected same-parent 비교에서는 H-005의 XY 개선이 조금 더 뚜렷하고 yaw도 거의 중립이다. 즉 “0.25가 항상 나쁨”으로 단정할 수 없다.
- **판별 방법:** 기존 H-005 10K와 TERM50 checkpoint를 동일 fixed evaluator로 비교. reward 인과만 엄밀히 묻는다면 동일 10K fresh 0.20 control이 더 직접적이지만, 지금 제출 결정을 위해 새 학습보다 기존 정책 평가가 우선이다.

### 발견 B — H-005는 5K 이후에도 의미 있게 학습됐다

- **관찰:** H-005 late-500에서 5K→10K 동안 yaw error `-0.0799`, base-contact `-2.668%p`, episode length `+29.90`, terrain `+0.1495`; XY는 사실상 유지.
- **해석:** 이 설정은 5K에서 끝난 정책보다 후반에 더 안정적/지속적인 locomotion을 학습했다.
- **경쟁 설명:** 이는 feet 0.25의 특수 효과가 아니라 일반적인 추가 학습/커리큘럼 적응일 수 있다.
- **반대 근거:** 마지막 500 terrain은 직전 500보다 내려와 모든 축이 단조 개선한 것은 아니다.
- **판별 방법:** 동일 evaluator에서 TERM50 model4900과 H-005 9800/9950를 평가하면 “현재 완성 정책”의 실질 차이는 바로 확인 가능하다.

### 발견 C — 영상은 ‘생존’보다 강한 실제 진행 증거를 일부 제공하지만 stairs는 예외다

- **관찰:** boxes/random_rough는 지형 패치 경계가 화면상 지나가며 실제 진행이 보인다. stairs는 가장자리 이동으로 보이고 명확한 여러 단 중앙 상승이 없다.
- **해석:** H-005는 단순 upright-stall local optimum으로만 보이지는 않지만, 특정 접촉 구조 특히 stairs traversability는 아직 불명확하다.
- **경쟁 설명:** command가 계단을 정면 횡단하도록 주어진 것이 아니라면 edge-following이 정상 command 추종일 수도 있다.
- **반대 근거:** 20초 동안 upright이고 계속 움직이므로 stairs 행동을 실패라고 확정할 수도 없다.
- **판별 방법:** command/terrain seed가 기록되는 fixed stairs evaluator에서 실제 상승 단수·forward displacement·stall·fall을 기록한다.

### 발견 D — 9800 vs 9950은 현재 scalar만으로 확정하기 어렵다

auto best 주변 `9750–9849`는 terrain 약 `5.765`, XY `0.359`, yaw `0.876`, base-contact `25.70%`, episode length `816` 수준이다. 마지막 `9900–9999`는 terrain 약 `5.817`, XY `0.370`, yaw `0.898`, base-contact `25.96%`, episode length `825` 수준이다.

9800 근처는 tracking이 조금 낫고, 9950 근처는 terrain/episode length가 조금 낫다. 차이는 단일 checkpoint evaluator 결과가 아니라 주변 training aggregate다. 영상 source도 불명이다.

따라서 `model_best=model_9800`이라는 label만으로 제출 최적을 선언하지 않고, 반대로 9950이 더 최신이라는 이유만으로 final을 선택하지도 않는다.

---

## 7. checkpoint, 가설, 프로젝트 판단

### 7.1 checkpoint 역할 구분

| artifact | 의미 | 현재 판단 |
| --- | --- | --- |
| `model_9800.pt` | Train/mean_reward peak step 9784에 대응한 자동 best | provenance 명확한 후보 |
| `model_best.pt` | 9800과 byte-identical alias | 별도 정책이 아님 |
| `model_9950.pt` | 받은 archive의 최신 numbered checkpoint | 별도 후보; 더 최신이라는 이유만으로 우수 확정 금지 |
| H-005 6영상 | checkpoint source manifest 없음 | 행동 sanity evidence지만 9800/9950에 귀속 불가 |
| loose/exported `policy.pt` | source checkpoint 독립 연결 없음 | 현재 제출 snapshot identity로 확정 불가 |
| TERM50 `model_4900.pt` | TERM50 model_best와 byte-identical | 과거 공식 제출 계열 기준 후보 |

### 7.2 현재 판정

- **Execution:** `COMPLETE`
- **Evidence:** train identity/config/raw TB/checkpoint 9800·9950 identity는 확인. 6영상 파일은 확인했으나 checkpoint lineage 미확인.
- **비교:** official 5K stage training scalar는 조건부 직접 비교 가능. 10K vs5K endpoint는 완성 정책 맥락 비교. 행동 A/B는 현재 자료로 대칭 비교 불가.
- **Hypothesis H-005:** **PROMOTE to fixed paired evaluation only**. **Final adoption: HOLD.**
- **Policy quality:** 후반 training 안정성과 일부 실제 terrain progression은 긍정. stairs traversability, command-specific tracking, 공식 evaluator performance는 미확인.
- **Submission:** H-005는 아직 실제 제출·채점 결과가 없으므로 TERM50 공식 `56.37/70`보다 높거나 낮다고 주장할 수 없다.

### 7.3 “무엇을 배웠고 무엇을 잃었나”

**배운 것으로 관찰되는 것**

- 5K 이후에도 yaw tracking과 training termination 안정성을 더 개선하는 장기 학습 trajectory.
- boxes/random_rough/inverted-stairs 계열에서 upright 상태로 실제 지형을 진행하는 행동.
- 후반 terrain level을 약 5.8대에서 유지하면서 episode length 약 820 수준으로 긴 episode를 만드는 정책.

**대가 또는 아직 잃었을 가능성이 있는 것**

- 동일 5K stage의 TERM50 대비 yaw/base-contact/terrain/episode-length에서 작은 불리함이 관찰됐다.
- stairs 중앙 traversability는 영상에서 증명되지 않았다.
- 9800/9950 중 어떤 checkpoint가 실제 command tracking과 terrain worst-case에 더 좋은지 아직 모른다.

“feet 0.25 때문에 발을 더 잘 들게 됐다”는 식의 기전 서술은 현재 weighted term과 영상만으로 확정하지 않았다.

---

## 8. 다음 한 번의 행동

### 1순위 — 기존 3 checkpoint 동일 fixed evaluator

**새 GPU 학습을 먼저 할 필요가 없다.** 현재 의사결정을 가장 많이 바꿀 정보는 다음 세 정책을 동일 evaluator에 넣는 것이다.

1. H-005 OFFICIAL `model_9800.pt`
2. H-005 OFFICIAL `model_9950.pt`
3. TERM50 OFFICIAL `model_4900.pt`

공통으로 맞출 조건:

- evaluator 코드/version
- terrain scenario와 difficulty
- command sequence 또는 command seed
- episode 수와 최대 길이
- reset/terrain seed 정책
- camera는 성능 계산과 분리

기록할 값:

- axis별 `vx`, `vy`, yaw-rate error와 통합 tracking error
- episode survival / base-contact termination
- 실제 forward/lateral displacement와 stall time
- stairs ascent / rough·boxes traversal 여부
- worst-scenario 결과
- 가능하면 hip/torso posture raw metric

**결과별 다음 결정:**

- H-005 둘 중 하나가 TERM50보다 tracking·survival·실제 진행에서 일관된 개선을 보이면 그 checkpoint를 제출 후보로 좁힌다.
- 9800과 9950이 trade-off면 공식 평가 비중과 worst-case를 기준으로 선택하고, 영상도 해당 checkpoint에서 lineage manifest와 함께 한 번만 다시 만든다.
- TERM50이 여전히 비슷하거나 우수하면 feet 0.25의 final adoption은 보류하고, 10K 추가 학습 자체가 얻은 가치와 reward 변경 가치를 분리한다.

이 평가는 **reward 변경의 완전한 인과 실험**과는 다르다. 그러나 현재의 실제 프로젝트 질문인 “어느 완성 정책/checkpoint를 제출 후보로 삼을 것인가”에는 새 10K control 학습보다 정보 효율이 높다.

---

## 9. 한계

1. H-005 영상 ZIP에 manifest/checkpoint SHA가 없어 9800/9950 행동으로 귀속할 수 없다.
2. TERM50에 동등한 source-linked 6지형 묶음이 현재 입력에 없어 행동 비교는 비대칭이다.
3. 같은 seed라도 terrain generator seed가 `null`이라 완전 paired terrain realization을 보장하지 않는다.
4. training base-contact, terrain curriculum, weighted reward term은 공식 evaluator의 fall/traversal/posture 점수와 같은 정의가 아니다.
5. H-005 10K와 TERM50 5K endpoint 차이는 추가 학습량이 크게 섞인다.
6. 같은 5K prefix 비교도 single seed이고 H-005의 전체 max-iteration/save-interval 설정이 다르다.
7. 영상은 약 0.25초 dense frame sampling 기반 정성 분석이다. 아주 짧은 slip/impact를 완전히 배제하지 않는다.
8. command vector, terrain difficulty/seed, camera metadata가 영상 묶음에 없어 command-specific 성공 판정은 보류했다.
9. H-005는 아직 공식 제출 점수가 없다. TERM50 Round 2 점수는 과거 기준이지 H-005 점수의 추정치가 아니다.

---

## 10. 재확인 가능한 근거 목록

### H-005 OFFICIAL 10K archive 내부

- `20260927-123428-h005-fresh10k-official/metadata.json`
- `.../validation.json`
- `.../command.txt`
- `.../source/humanoid_rewards.py`
- `.../native_run/params/env.yaml`
- `.../native_run/params/agent.yaml`
- `.../native_run/events.out.tfevents.*`
- `.../console.log`
- `.../collected/exported/report.html`
- `.../collected/exported/model_best.pt`
- `.../organizer_checkpoints/model_9800.pt`
- `.../organizer_checkpoints/model_9950.pt`

### TERM50 OFFICIAL 5K archive 내부

- `H1_TERM50_5k_complete_20260909_003012/humanoid_rewards.py`
- `.../logs/rsl_rl/humanoid/2026-09-08_23-23-33/params/env.yaml`
- `.../params/agent.yaml`
- `.../events.out.tfevents.*`
- `.../model_4900.pt`
- `.../exported/model_best.pt`
- `.../exported/report.html`

### PERSONAL 보조 대조

- `H005_PERSONAL_corrected3K_late.tar.gz`: corrected H-005 Run 02, global `1499–2998`
- `H001_PERSONAL_control3K_late.tar.gz`: same corrected parent unchanged control, global `1499–2998`
- `H005_PERSONAL_fresh3K_late.tar.gz`: fresh same H-005 reward config, `0–2999`

### 영상

- `boxes.mp4`
- `stairs.mp4`
- `inverted_stairs.mp4`
- `random_rough.mp4`
- `slope_up_10deg.mp4`
- `slope_down_10deg.mp4`

### 문서 맥락

- `README_분석시작(1).md`
- `H005_registry(1).md`
- `H005_OFFICIAL_report(1).html`
- `ROUND2_score_and_report(1).md`
- 프로젝트 핵심팩의 `14_H1_NEXT_RUN_PARAMETER_COMPARISON.md`, `16_EXPERIMENT_EXPORT_AND_TENSORBOARD.md`, `18_H1_FINALIZE_REPORT_LIMITATIONS.md`, `19_ISSACSIMZ_EXTERNAL_EVIDENCE_CLI.md`

---

## 최종 판단 한 문장

**H-005 OFFICIAL 10K는 후반 안정성과 여러 지형의 실제 진행을 확보한 유망 정책이지만, 같은 5K stage에서는 feet 0.25가 TERM50 0.20보다 명확히 낫지 않았고 10K 개선에는 추가 학습 효과가 섞여 있으므로, H-005는 fixed paired evaluation 단계로만 PROMOTE하고 final adoption은 HOLD하며, 다음 작업은 새 학습이 아니라 `9800 / 9950 / TERM50 4900`의 동일 evaluator 비교가 가장 정보 가치가 높다.**
