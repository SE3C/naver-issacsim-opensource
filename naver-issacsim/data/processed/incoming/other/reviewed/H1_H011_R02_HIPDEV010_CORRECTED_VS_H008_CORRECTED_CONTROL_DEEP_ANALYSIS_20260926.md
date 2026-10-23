# H1 H-011 R02 HIPDEV010 corrected vs H-008 corrected control — Deep Analysis

- 분석일: 2026-09-26
- Robot: H1 / `Humanoid-v0`
- A(이번 분석 대상): **H-011 R02 HIPDEV010 corrected**, `joint_deviation_hip=-0.1`
- B(대조군): **H-008 corrected control**, `joint_deviation_hip=-0.2`
- 환경 분류: **PERSONAL / NVIDIA Brev L40S** — 공식 점수나 OFFICIAL 성능 증거가 아님
- 분석 범위: 첨부된 학습 원본 2개 + final `model_4997.pt` 6지형 영상 묶음 2개. 새 학습·렌더링·export·서버 조작은 수행하지 않음.

> A/B 역할은 실제 run 이름과 단일변수 구조를 기준으로 H-011을 intervention, H-008을 unchanged control로 두었다. 결론은 두 Run을 같은 기준으로 재집계하여 작성했다.

---

## 1. 결론 요약

### 세 질문에 대한 답

**1) 이번 정책(H-011)은 목표 행동을 실제로 얼마나 수행하는가?**  
H-011 final `model_4997.pt`는 제공된 6개 영상에서 모두 upright 상태로 지형을 진행한다. 1초 간격 전 구간 프레임 조사에서 stairs, inverted stairs, boxes, random rough, 10° up/down slope 모두에서 명백한 낙상·reset은 관찰되지 않았다. 특히 boxes에서는 약 17초 이후 장애물 patch를 벗어난 장면이 보인다. 다만 영상 manifest에는 수치 command, terrain seed/difficulty, 초기 상태가 없으므로 이 6개 클립을 command-tracking 정량평가나 성공률로 해석할 수 없다. 학습 로그의 late-500에서는 XY velocity-error tag `0.3289`, yaw velocity-error tag `1.4061`, training base-contact termination fraction `29.17%`, terrain level `5.642`였다. 이 수치는 **학습 내부 집계**이며 공식 evaluator 점수가 아니다.

**2) H-008 control과의 차이 중 무엇이 관찰됐고, 무엇을 hip penalty 변경 효과로 해석할 수 있는가?**  
이번 비교는 과거 H-005~011 계보 문제와 달리, 두 child가 **동일하게 기록된 parent checkpoint SHA `49fdb297…414983`**, 동일 seed 42, 4096 env, 동일 PPO, 동일 추가 2000 iteration, 동일 source를 사용하고 실제 `env.yaml` 차이가 `joint_deviation_hip -0.2 → -0.1` 하나뿐인 sibling이다. 따라서 이 계보 안에서 hip penalty 완화의 방향을 묻는 **직접 비교에 적합**하다. 다만 parent checkpoint 바이트가 이번 입력에 없어서 동일 parent는 metadata SHA 기록 수준으로 연결되며, terrain generator seed가 `null`이고 single seed이므로 일반화된 인과 효과를 확정할 수는 없다.

관찰된 차이는 작고 mixed다. late-500에서 H-011은 control보다 XY error가 `0.00052` 낮고 yaw error가 `0.02177` 낮으며 base-contact fraction이 `0.246 %p` 낮았다. 그러나 terrain은 `0.030` 낮았다. 더 좁은 late-300에서는 XY/yaw 개선 방향은 유지되지만 base-contact가 오히려 `0.122 %p` 높아지고 episode length 우위도 사라진다. 반대로 동일 weight인 posture 관련 reward component는 H-011에서 더 나빠지는 방향이 반복된다: late-500 `flat_orientation_l2 -0.01208 vs -0.01166`, `joint_deviation_torso -0.00731 vs -0.00606`. 이는 hip 제약 완화가 일부 이동/추종 자유도를 주는 대신 자세 정렬 비용을 키웠을 가능성과 맞지만, **기전 가설**이지 직접 hip angle을 측정한 결과는 아니다. `Episode_Reward/joint_deviation_hip` 자체는 weight가 절반으로 바뀌었으므로 절댓값 비교를 자세 개선 증거로 사용하지 않았다.

**3) 현재 자료에서 내려야 할 결정과 가장 먼저 풀 불확실성은?**  
실행은 양쪽 모두 **COMPLETE**, evidence는 **PASS**, H-011 가설은 **HOLD**가 적절하다. REJECT할 붕괴는 없고 6지형 행동도 유지되지만, PROMOTE하기에는 tracking 이득이 작고 stability 차이가 window에 따라 뒤집히며 posture 비용 증가가 보인다. 대표 checkpoint는 양쪽 모두 **final numbered `model_4997.pt`**가 맞다. 마지막 수백 iteration에서 terrain·tracking·base-contact가 함께 무너지는 joint collapse가 없고, 제공 영상도 실제 final SHA에 연결되어 있다.

다음 한 번의 행동은 **새 학습이 아니라 두 final checkpoint를 동일 fixed evaluator에 넣는 paired 평가**다. 같은 terrain realization/difficulty, 같은 command sequence, 같은 initial state/seed set에서 per-terrain progress/traversal, XY/yaw tracking, base-contact, stall, 그리고 가능하면 **unweighted hip yaw/roll deviation 및 torso/roll-pitch 자세량**을 함께 기록해야 한다. 이것이 boxes 영상의 진행 차이가 실제 policy 차이인지, 그리고 hip 완화의 의도된 기전이 있는지를 가장 직접적으로 판별한다.

### 현재 판정

| 항목 | 판정 |
|---|---|
| H-011 실행 | **COMPLETE** — exit 0, global 2998→4997, evidence validation PASS |
| H-008 control 실행 | **COMPLETE** — exit 0, global 2998→4997, evidence validation PASS |
| 비교 적합성 | **직접 비교에 적합(단일 sibling run 범위)** — 실제 child 설정 차이는 hip weight 하나. single-seed/PERSONAL/terrain RNG 한계는 유지 |
| H-011 가설 | **HOLD** — 작은 late tracking 이득 신호, posture trade-off, stability 우위 비강건 |
| 대표 checkpoint | 양쪽 **`model_4997.pt`** |
| OFFICIAL/제출 판단 | **판단 불가** — PERSONAL evidence이며 공식 evaluator 결과 없음 |

---

## 2. 실제 Run · checkpoint · 영상 identity

### 2.1 입력 원본과 무결성

| 역할 | 입력 archive | archive SHA-256 | 내부 검증 |
|---|---|---|---|
| A 영상 | `checkpoint-h1-model_4997-9881687e534a-download.tar.gz` | `a36be9a6…e8316d38` | `SHA256SUMS` 전체 OK |
| B 학습 | `20260925-091257-h1-h008-corrected-control-to5k-h1-corrected-2026.tar(1).gz` | `17aa0817…1bd76faf` | `SHA256SUMS` 전체 OK, `validation.json=PASS` |
| B 영상 | `checkpoint-h1-model_4997-4349fe565013-download.tar(1).gz` | `faf3563d…89d814f4` | `SHA256SUMS` 전체 OK |
| A 학습 | `20260925-110346-h1-h011-r02-hipdev010-corrected-h1-corrected-202.tar.gz` | `de04585e…06dc50ae` | `SHA256SUMS` 전체 OK, `validation.json=PASS` |

### 2.2 checkpoint ↔ video 연결

**A / H-011**

- train final: `checkpoints/model_4997.pt`
- SHA-256: `9881687e534addf6bfa6d0b86f2827df6ef8dc104c51ed35c4ecaf424f34fcf6`
- video suite manifest: `checkpoint-h1-model_4997-9881687e534a/video_suite_manifest.json`
- manifest의 `checkpoint_sha256`가 위 final checkpoint SHA와 **정확히 일치**
- 6개 terrain entry 모두 `source_checkpoint_sha256`가 같은 SHA를 기록

**B / H-008 control**

- train final: `checkpoints/model_4997.pt`
- SHA-256: `4349fe5650135c6a77546afc1b165ff60c235bdd83831bd562d618b04c3b5b6d`
- video suite manifest: `checkpoint-h1-model_4997-4349fe565013/video_suite_manifest.json`
- manifest의 `checkpoint_sha256`가 위 final checkpoint SHA와 **정확히 일치**
- 6개 terrain entry 모두 같은 source SHA를 기록

따라서 이번 영상은 stale `exported/` artifact가 아니라 **각 Run의 final numbered checkpoint 행동**으로 사용할 수 있다.

### 2.3 학습 계보

두 Run metadata가 기록한 resume source는 동일하다.

- parent run ID: `NCRC_BATCH_h1-corrected-20260925-03_h008_corrected_2998`
- requested checkpoint: `model_2998.pt`
- source checkpoint SHA-256: `49fdb297924c861493d377f22b9de135d83c73969ef3d8a2e4a56c9879414983`
- start global iteration: `2998`
- requested additional iterations: `2000`
- final global iteration: `4997`

**한계:** parent `model_2998.pt` 파일 자체는 이번 네 archive에 포함되지 않았다. 따라서 “양쪽 metadata가 동일 SHA를 기록한다”는 것은 직접 확인했지만, parent 원본 바이트를 이번 intake에서 다시 hash 대조한 것은 아니다.

### 2.4 자동 best와 final의 분리

| Run | raw 전체 reward 최고 | native warm-up eligible 최고 | 자동 `model_best` | 실제 영상/대표 후보 |
|---|---:|---:|---|---|
| H-011 | `6.7142 @ 3053` | `6.0818 @ 4794` | `model_4800.pt` | **`model_4997.pt`** |
| H-008 ctrl | `6.1925 @ 3125` | `5.7572 @ 4874` | `model_4900.pt` | **`model_4997.pt`** |

관측 구간 `2998..4997`에 native selector 공식 `warmup = lo + max(50, floor((hi-lo)×0.10))`을 적용하면 `3197`부터 eligible이다. 양쪽 raw global reward max는 모두 이 경계 전이라 자동 selector가 제외한 것이 정상이다.

또한 H-011은 hip penalty weight 자체를 바꿨으므로 `Train/mean_reward` 척도가 B와 동일하지 않다. H-011의 더 높은 total reward나 자동 best reward를 정책 우위 근거로 사용하지 않았다.

---

## 3. 실제 설정 차이와 비교 설계

### 3.1 실제 적용 reward

두 `source/humanoid_rewards.py`와 두 `native_run/params/env.yaml`을 직접 diff했다. 동적 `log_dir`을 제외하면 **실행 설정의 유일한 reward 차이는 아래 한 줄**이다.

| 항목 | H-011 A | H-008 control B | 차이 |
|---|---:|---:|---:|
| `track_lin_vel_xy_exp` | +0.75 | +0.75 | 동일 |
| `track_ang_vel_z_exp` | +0.5 | +0.5 | 동일 |
| `feet_air_time` | +0.2 | +0.2 | 동일 |
| `termination_penalty` | -50.0 | -50.0 | 동일 |
| `flat_orientation_l2` | -1.5 | -1.5 | 동일 |
| `ang_vel_xy_l2` | -0.05 | -0.05 | 동일 |
| **`joint_deviation_hip`** | **-0.1** | **-0.2** | **+0.1 (penalty 완화)** |
| `joint_deviation_torso` | -0.1 | -0.1 | 동일 |
| `action_rate_l2` | -0.0005 | -0.0005 | 동일 |

`source/identity.json`도 두 Run 사이에서 `humanoid_rewards.py` SHA만 다르고 `train.py`, `play.py`, `_finalize.py`, `env_cfg.py`, `agent_cfg.py` 등 나머지 hash는 동일하다. `native_run/params/agent.yaml`은 byte-level diff가 없다.

중요한 해석: finalize report가 H-011에서 `track_lin 0.5→0.75`, `termination -5→-50`, `hip -0.2→-0.1`을 함께 “기본값 대비 변화”로 출력하지만, **이번 sibling 간 실제 차이는 hip 하나뿐**이다. report의 baseline diff를 child-to-child delta로 잘못 읽지 않았다.

### 3.2 공통 학습 조건

| 조건 | A / H-011 | B / H-008 control |
|---|---|---|
| Environment | PERSONAL | PERSONAL |
| robot/task | H1 / `Humanoid-v0` | 동일 |
| resume parent record | `49fdb297…414983` | 동일 |
| seed | 42 | 42 |
| num_envs | 4096 | 4096 |
| rollout | 24 steps/env/iteration | 동일 |
| 추가 iteration | 2000 | 2000 |
| global range | 2998..4997 | 2998..4997 |
| 추가 transitions | 196,608,000 | 196,608,000 |
| PPO | 5 epochs, 4 minibatches, LR 1e-3 adaptive, γ .99, λ .95, entropy .008, KL .01, clip .2 | 동일 |
| checkpoint interval | 100 | 100 |
| headless | yes | yes |
| terrain generator | curriculum, 10×20, seed `null` | 동일 |
| command training range | x `[-1,1.5]`, y `[-0.5,0.5]`, yaw `[-1,1]`, resample 10 s | 동일 |
| exit / validation | 0 / PASS | 0 / PASS |

### 3.3 무엇을 인과로 말할 수 있는가

**판정: 직접 비교에 적합 — 단, single-run 방향성까지.**

- 동일한 기록상 parent checkpoint에서 분기했다.
- child에서 실제로 바뀐 reward는 hip penalty 하나다.
- source/PPO/seed/학습량/num_envs가 같다.
- 따라서 이 두 trajectory의 차이를 “hip penalty 완화가 만든 결과 후보”로 해석할 수 있다.

그러나 다음 때문에 **일반화된 causal effect**나 최적값 판정은 아니다.

1. 단일 seed다.
2. terrain generator seed가 `null`이다. training seed가 같아도 branch 이후 policy와 RNG 상호작용 때문에 동일 terrain/episode 대응을 보장하지 않는다.
3. 후반 TensorBoard 500점은 독립 500개 seed가 아니라 자기상관된 한 시계열이다.
4. 영상 suite는 terrain 종류를 고정한 정성 sanity check지만 manifest에 numeric command, terrain seed/difficulty, 초기 상태가 없다.

---

## 4. TensorBoard raw 시계열 재분석

### 4.1 파싱 방법

각 학습 archive의 `native_run/events.out.tfevents.*`를 TFRecord/Event protobuf로 직접 읽었다.

- 각 Run: main global scalar tag마다 **2000 points**
- global steps: **2998..4997**, 중복 없음
- event 파일: Run당 1개
- step reset 없음
- `Train/mean_reward/time`, `Train/mean_episode_length/time`은 wall-time 기반 pseudo-step에 중복 step이 있어 global-iteration 분석에서 제외
- `3197` 이전은 native finalizer의 resume warm-up 구간으로 별도 취급

주 비교 window는 **late-500 = 4498..4997**로 잡았다. 이유는 3197 이후 충분히 긴 재적응 구간을 지난 뒤 final 직전의 정책 상태를 보는 대칭 window이기 때문이다. 결론의 경계 민감성은 **late-300 = 4698..4997**으로 확인했다. 마지막 추세는 `4398..4697` vs `4698..4997`도 비교했다.

### 4.2 핵심 late-500 비교

> `base_contact`/`time_out`은 training logger의 episode termination fraction이다. 고정 evaluator의 낙상률·성공률로 부르지 않는다. `Curriculum/terrain_levels`는 평균 curriculum level이지 고정 난이도 통과율이 아니다.

| 지표 / tag | H-011 A late-500 | H-008 B late-500 | A-B | 해석 |
|---|---:|---:|---:|---|
| `Curriculum/terrain_levels` | 5.6420 | 5.6718 | -0.0299 | control이 아주 조금 높음; 사실상 근접 |
| `Metrics/base_velocity/error_vel_xy` | 0.32886 | 0.32938 | **-0.00052** | H-011 미세하게 낮음 |
| `Metrics/base_velocity/error_vel_yaw` | 1.40613 | 1.42790 | **-0.02177** | H-011 소폭 낮음 |
| `Episode_Termination/base_contact` | 29.174% | 29.420% | **-0.246 %p** | H-011 소폭 낮음 |
| `Episode_Termination/time_out` | 70.841% | 70.595% | +0.246 %p | 위와 상보적 |
| `Train/mean_episode_length` | 779.35 steps | 774.94 steps | +4.41 | H-011 소폭 길음 |
| `Policy/mean_std` | 1.47467 | 1.47776 | -0.00309 | 사실상 동일 |
| `Episode_Reward/track_lin_vel_xy_exp` | 0.48605 | 0.48237 | +0.00368 | 같은 weight 아래 H-011 소폭 높음 |
| `Episode_Reward/track_ang_vel_z_exp` | 0.11881 | 0.11617 | +0.00264 | 같은 weight 아래 H-011 소폭 높음 |
| `Episode_Reward/action_rate_l2` | -0.07354 | -0.07443 | +0.00089 | H-011 late-window penalty magnitude가 조금 작음 |
| `Episode_Reward/ang_vel_xy_l2` | -0.02554 | -0.02599 | +0.00044 | H-011 late-window penalty magnitude가 조금 작음 |
| `Episode_Reward/feet_slide` | -0.04834 | -0.04928 | +0.00093 | H-011 late-window penalty magnitude가 조금 작음 |
| `Episode_Reward/flat_orientation_l2` | **-0.01208** | -0.01166 | -0.00042 | H-011 자세 penalty가 더 큼 |
| `Episode_Reward/joint_deviation_torso` | **-0.00731** | -0.00606 | -0.00125 | H-011 torso deviation penalty가 더 큼 |
| `Episode_Reward/feet_air_time` | 0.00995 | 0.00938 | +0.00057 | H-011 조금 높음 |

`Episode_Reward/joint_deviation_hip`는 H-011 `-0.02416`, control `-0.03686`이지만 **직접 비교하지 않는다**. reward weight가 `-0.1` vs `-0.2`로 다르기 때문에 term 값 차이 자체가 행동의 hip deviation 감소를 뜻하지 않는다. 원 reward의 normalization/집계 전 raw deviation metric도 event에 없다.

### 4.3 late-300 sensitivity check

| 지표 | H-011 A | H-008 B | A-B | late-500 대비 |
|---|---:|---:|---:|---|
| terrain | 5.6442 | 5.6516 | -0.0074 | 거의 동률 |
| XY error | 0.32549 | 0.32806 | **-0.00256** | H-011 개선 방향 유지 |
| yaw error | 1.37999 | 1.40977 | **-0.02979** | H-011 개선 방향 유지 |
| base-contact | 29.217% | 29.095% | **+0.122 %p** | **방향 반전** |
| timeout | 70.794% | 70.912% | -0.118 %p | 방향 반전 |
| episode length | 777.69 | 778.69 | -1.00 | 우위 소멸 |
| flat orientation component | -0.01235 | -0.01151 | -0.00083 | H-011 불리 방향 유지 |
| torso deviation component | -0.00737 | -0.00598 | -0.00139 | H-011 불리 방향 유지 |

따라서 **tracking의 작은 H-011 우위 신호는 late-window에서 비교적 일관적**이지만, survival/base-contact/episode-length 우위는 강건하지 않다. posture 관련 비용 증가는 오히려 더 일관적이다.

### 4.4 후반 악화 여부와 final checkpoint

`4398..4697 → 4698..4997` 변화:

- H-011 terrain: `5.6459 → 5.6442` (거의 평탄)
- H-011 XY error: `0.3340 → 0.3255` (개선)
- H-011 yaw error: `1.4511 → 1.3800` (개선)
- H-011 base-contact: `28.754% → 29.217%` (0.463 %p 악화)
- H-011 episode length: `783.0 → 777.7` (소폭 감소)

즉 안정성 지표 한 축은 약간 나빠지지만 tracking과 terrain이 동시에 무너지지 않는다. 프로젝트의 “충분히 긴 resume는 final numbered checkpoint를 기본 대표로 두고, 마지막 수백 iteration에서 terrain·tracking·낙상이 함께 뚜렷하게 악화될 때만 예외 검토” 원칙에 따르면 H-011 final `model_4997.pt`를 버릴 근거가 없다.

control도 마찬가지다. late terrain은 다소 낮아졌지만 XY/yaw와 base-contact가 함께 무너지지 않는다. 따라서 양쪽 모두 final을 대표로 사용한다.

### 4.5 최적화 안정성

두 Run 모두 NaN/Inf 또는 optimizer 폭발 근거는 없다.

- `Loss/value` post-warmup mean: H-011 `0.00643`, control `0.00652`
- `Loss/surrogate` post-warmup mean: H-011 `-0.01377`, control `-0.01389`
- `Policy/mean_std` post-warmup mean: H-011 `1.4815`, control `1.4785`
- adaptive LR은 두 Run 모두 정상 범위 내에서 움직이며 max 약 `3.84e-4`
- final std도 `1.475` vs `1.472`로 근접

따라서 이번 차이를 “한쪽 학습이 수치적으로 실패했다”로 설명할 근거는 없다.

---

## 5. 여섯 지형 영상 행동 비교

### 5.1 영상 조사 방법과 한계

모든 MP4는 `ffprobe`로 확인했으며 동일 형식이다.

- H.264
- 1920×1080
- 50 fps
- 999 frames
- 19.98 s

현재 분석 환경에는 연속 재생 UI가 없으므로, 각 50fps 원본에서 **0~19초를 1초 간격으로 전 구간 샘플링(영상당 20장)**하고 장애물 접촉 구간을 별도 확대 프레임으로 재확인했다. 따라서 아래 관찰은 실제 영상 프레임 근거지만, 20~100 ms 규모의 foot slip, gait frequency, 순간 recovery를 연속 재생한 것처럼 주장하지 않는다.

영상 suite는 H1에서 stairs / inverted stairs / boxes / random rough / fixed 10° up slope / fixed 10° down slope를 한 checkpoint로 렌더한 PERSONAL sanity suite다. 프로젝트 운영 문서상 slope 값은 `0.176326981`이고 대상 terrain proportion만 1.0으로 고정한다. **하지만 받은 `video_suite_manifest.json`에는 command 값·terrain seed·difficulty·initial state가 없다.** 이름이 같은 terrain이라고 A/B가 동일 episode라고 가정하지 않는다.

### 5.2 지형별 관찰

| Terrain | H-011 A 관찰 | H-008 control B 관찰 | 공통/차이 | 판단 한계 |
|---|---|---|---|---|
| `stairs` | 약 12~13 s 접근·첫 계단 진입, 14~15 s 계단 위 진행, 16~17 s 이후 반대편 평지. 샘플상 upright. | 거의 같은 시간대에 진입·통과. 샘플상 upright. | **둘 다 명확한 계단 통과**. 큰 차이 없음. | 1초 샘플로 발 걸림·순간 slip 빈도는 판정 불가. command 수치 없음. |
| `inverted_stairs` | 약 9~12 s 계단 영역을 지나 13 s 이후 평지 쪽으로 이탈. 낙상/reset 없음. | 유사하게 9~12 s 계단 영역, 이후 평지. | **둘 다 통과**, 큰 차이 없음. | 동일 terrain realization/command 여부 미확인. |
| `boxes` | 10~15 s 장애물군 내부 진행, 약 17 s부터 patch 바깥 평지에 있고 18~19 s에는 장애물이 뒤쪽에 남음. | 10~19 s 동안 계속 outer boxes 안/근처에 보이며 19 s에도 patch가 가까움. 낙상은 없음. | **가장 큰 시각 차이:** A가 이 클립에서는 더 멀리 진행한 장면. | command/seed/difficulty 미기록이라 “A가 더 빠르다/추종이 좋다”는 정량 결론은 보류. |
| `random_rough` | 10~15 s 거친 patch 진행, 16~17 s 경계/평지로 이동. upright. | 매우 유사하게 10~16 s 진행 후 경계를 벗어남. upright. | 둘 다 traversability 확인. 뚜렷한 차이 없음. | sub-second 발 미끄러짐·충격은 미측정. |
| `slope_up_10deg` | 9~16 s slope patch를 지나며 upright 유지, 후반 평지 쪽으로 이동. | 유사한 진행. | 둘 다 10° up-slope sanity 통과. | 영상의 저대비 지형 때문에 정확한 접촉 시각/경사 위 체류시간 정밀 측정은 하지 않음. |
| `slope_down_10deg` | 9~16 s down-slope 영역을 지나며 upright, 명백한 pitch collapse 없음. | 유사함. | 둘 다 10° down-slope sanity 통과. | pitch/roll angle telemetry 없음. |

### 5.3 영상에서 말할 수 있는 것 / 없는 것

**말할 수 있는 것**

- 두 final checkpoint 모두 6개 제공 클립에서 terrain traversal을 실제로 수행한다.
- 1초 샘플 전 구간에서 명백한 낙상/reset은 보이지 않는다.
- H-011 boxes 클립은 control보다 patch를 더 빨리 벗어난 것처럼 보이는 진행 차이가 있다.
- H-011이 hip penalty를 완화했다고 해서 즉시 심한 collapse나 명백한 비정상 정체가 생긴 흔적은 없다.

**말할 수 없는 것**

- 6/6 성공률 또는 낙상 확률: 각 지형 1개 19.98 s trajectory뿐이다.
- 정확한 command tracking: command numeric log가 없다.
- “boxes에서 H-011이 정책적으로 더 빠르다”: A/B command·terrain seed·difficulty가 manifest에 없다.
- hip deviation이 실제로 줄거나 늘었다: 영상에서 정밀 관절각을 측정하지 않았고 TB의 hip reward term은 weight가 다르다.
- hopping/sliding frequency: 1초 sampling만으로 sub-second gait cycle을 정량화하지 않았다.

---

## 6. 수치와 영상의 교차검증

### 6.1 서로 맞는 부분

1. **둘 다 학습 붕괴가 아니다.**  
   terrain late 평균이 약 5.64~5.67이고, base-contact training fraction이 약 29%, episode length가 약 775~779 steps로 유지된다. 영상에서도 6지형 모두 upright locomotion이 보인다.

2. **H-011의 small tracking/progress 신호는 영상과 모순되지 않는다.**  
   late-500/300에서 XY·yaw error가 아주 조금 낮고, boxes 클립에서 더 멀리 진행한 장면이 보인다. 다만 영상 조건이 paired evaluator가 아니므로 이 둘을 같은 효과의 재현이라고 단정하지 않는다.

3. **hip 완화가 심각한 생존 손실을 만들었다는 증거는 없다.**  
   base-contact/episode length는 late-500에서 오히려 H-011이 조금 낫고 late-300에서는 사실상 tie/약간 열세다. 영상에서도 낙상은 관찰되지 않는다.

### 6.2 서로 긴장되는 부분

1. **posture cost는 H-011에서 더 크다.**  
   `flat_orientation_l2`와 `joint_deviation_torso`의 동일-weight component가 H-011에서 더 negative다. 즉 더 자유로운 hip이 tracking을 조금 돕는 대신 torso/flat posture를 희생했을 가능성이 있다.

2. **stability 우위는 window에 민감하다.**  
   late-500의 base-contact `-0.246 %p`, episode length `+4.4`는 late-300에서 `+0.122 %p`, `-1.0`으로 뒤집힌다. 따라서 “hip 완화가 낙상을 줄였다”는 결론은 현재 자료로 지지되지 않는다.

3. **terrain은 개선되지 않았다.**  
   late-500 terrain은 control이 `+0.030`, late-300도 `+0.007` 높다. 차이는 작지만, H-011 tracking 신호를 지형 난이도 progression 개선으로 확대해석할 수 없다.

---

## 7. 핵심 발견 · 경쟁 설명 · 반대 근거

### 발견 A — hip penalty 완화는 late tracking에 작은 양의 신호를 보인다

- **관찰:** late-500 XY `-0.00052`, yaw `-0.02177`; late-300 XY `-0.00256`, yaw `-0.02979` (H-011이 낮음).
- **해석:** hip yaw/roll deviation penalty를 줄이면 하체가 command에 맞춰 자세를 더 자유롭게 조정할 수 있어 tracking에 도움이 될 수 있다.
- **경쟁 설명:** branch 이후 stochastic terrain/episode 차이, single seed, curriculum state 변동으로도 설명 가능하다.
- **반대 근거:** post-warmup 전체 3197..4997에서는 yaw error가 H-011 `1.4527` vs control `1.4358`로 오히려 약간 나쁘다. 즉 이득은 **후반부에 나타난 작은 신호**이지 전체 run 일관 우위가 아니다.
- **판별:** 동일 command/terrain fixed evaluator에서 axis별 tracking을 재측정한다.

### 발견 B — posture trade-off 신호는 tracking 신호보다 더 일관적이다

- **관찰:** late-500 flat-orientation component `-0.01208 vs -0.01166`, torso deviation `-0.00731 vs -0.00606`; late-300에서도 같은 방향.
- **해석:** hip 제약 완화가 pelvic/torso 자유도를 키워 자세 정렬 비용을 늘렸을 가능성이 있다.
- **경쟁 설명:** reward component는 episode/curriculum distribution 영향도 받으며 직접 angle이 아니다.
- **반대 근거:** `ang_vel_xy_l2`는 late-500/300에서 H-011이 오히려 덜 negative여서, “더 흔들린다”를 단순히 주장할 수 없다. 자세 offset은 늘었지만 회전 속도는 낮아진 형태일 수도 있다.
- **판별:** fixed evaluator에서 base roll/pitch, torso joint deviation, hip yaw/roll raw deviation을 weight 적용 전 물리량으로 기록한다.

### 발견 C — 생존/낙상 개선은 현재 자료에서 확정할 수 없다

- **관찰:** base-contact 차이가 late-500 `-0.246 %p`에서 late-300 `+0.122 %p`로 뒤집힌다.
- **해석:** 실질 효과가 매우 작거나 후반 변동 범위와 비슷할 가능성이 크다.
- **경쟁 설명:** curriculum/episode mix 변화.
- **반대 근거:** 영상 6개에서는 양쪽 모두 샘플상 낙상이 없다. 영상은 반복 trial이 아니므로 training fraction 차이를 검증하지 않는다.
- **판별:** 동일 evaluator의 여러 matched episode에서 base-contact/timeout을 직접 비교한다.

### 발견 D — boxes 영상은 H-011에 유리한 질적 단서지만 결정 근거는 아니다

- **관찰:** H-011은 약 17 s부터 patch 밖, control은 19 s까지 외곽 boxes와 가깝다.
- **해석:** obstacle negotiation 또는 진행성이 좋아졌을 수 있다.
- **경쟁 설명:** command vector, terrain realization, difficulty 또는 시작 상태가 달랐을 수 있다.
- **반대 근거:** 다른 5지형에서는 큰 시각 차이가 없다.
- **판별:** 동일 boxes realization/command의 paired evaluator에서 displacement, stall time, obstacle progress를 기록한다.

---

## 8. Checkpoint 판단 · 가설 결정 · 다음 한 번의 행동

### 8.1 checkpoint

**H-011:** final `model_4997.pt` 유지.  
자동 best `model_4800.pt`는 eligible `Train/mean_reward` peak에 가까운 checkpoint일 뿐이고, reward scale 자체가 control과 다르다. late terrain/tracking/base-contact의 joint collapse가 없으므로 final을 대표로 두는 현재 프로젝트 운영 원칙과 맞는다. 제공된 6지형 영상도 이 final SHA에 직접 연결돼 있어 행동 provenance가 가장 깨끗하다.

**H-008 control:** final `model_4997.pt` 유지.  
자동 best `model_4900.pt`보다 final을 버릴 joint late collapse 근거가 없다. A/B 모두 같은 selection rule을 적용했다.

### 8.2 가설 결정

**H-011 R02 HIPDEV010 corrected: HOLD**

- PROMOTE하지 않는 이유: late tracking 개선은 작고, survival 차이는 window-sensitive이며, posture component가 나빠진다. 영상의 유일하게 큰 차이인 boxes 진행도 paired condition이 아니다.
- REJECT하지 않는 이유: 수치적 붕괴가 없고, terrain 수준과 안정성은 control과 대체로 유지되며, 6지형 final 영상도 모두 traversal을 보인다. late tracking에는 양의 신호가 있다.
- INVALID가 아닌 이유: 실행·설정·checkpoint/video identity가 깨지지 않았고 child 실제 single-delta가 확인됐다.

### 8.3 다음 한 번의 행동 — 정보가치 1순위

**새 학습 없이, H-011 `model_4997` vs H-008 control `model_4997`의 matched fixed-evaluator batch를 실행한다.**

맞춰야 할 조건:

- 동일 evaluator version
- 동일 terrain realization 및 difficulty
- 동일 command sequence와 command transition timing
- 동일 initial state/episode horizon
- 동일 seed set
- 동일 camera 여부와 무관하게 물리 평가 조건 동일

반드시 기록할 지표:

- per-terrain 실제 progress/displacement/traversal
- stall time
- XY/yaw tracking
- base-contact / timeout
- base roll/pitch 또는 flat-orientation raw state
- torso joint deviation
- **hip yaw/roll raw deviation (weight 적용 전)**
- 가능하면 feet slide / action delta

결과별 결정:

- **tracking/progress가 재현되고 posture·fall이 유지** → H-011을 다음 OFFICIAL 재검증 후보로 PROMOTE 검토.
- **tracking 차이가 사라지고 posture 악화만 재현** → HIPDEV010을 REJECT 방향으로 전환.
- **terrain별 trade-off가 갈림** → HOLD 유지하고 어떤 공식 시나리오에 영향을 주는지 먼저 분리. 바로 새 reward를 겹쳐 바꾸지 않음.

이 평가가 현재 결정에 가장 직접적이다. 추가 1K/3K 학습을 먼저 하면 “hip weight 효과”와 “추가 학습 효과”가 다시 섞이므로 우선순위가 낮다.

---

## 9. 한계와 재확인 가능한 근거 목록

### 핵심 한계

1. 두 Run은 PERSONAL이다. 공식 서버 점수/제출 성능으로 승격하지 않는다.
2. parent checkpoint SHA는 두 metadata에서 동일하지만 parent 원본 바이트는 이번 입력에 없다.
3. single seed이며 training terrain generator seed는 `null`이다.
4. TB late-500/300은 독립 반복이 아니라 한 trajectory의 자기상관 시계열이다.
5. 영상은 각 terrain 1개 trajectory뿐이다.
6. 영상 manifest에 numeric command, seed, difficulty, initial state가 없다.
7. 영상 분석은 50fps 원본에서 전 구간 1초 sampling + 핵심 구간 확대 프레임 조사이며 continuous gait-cycle 측정이 아니다.
8. hip term은 reward weight가 다르므로 weighted component에서 raw hip deviation을 역산하지 않았다.

### 재확인 위치

**H-011 train archive**

- `metadata.json` — status, parent SHA, global iteration, mode
- `validation.json` — evidence PASS
- `source/humanoid_rewards.py` — hip `-0.1`
- `source/identity.json` — source hashes
- `native_run/params/env.yaml` — 실제 적용 env/reward/terrain/command 설정
- `native_run/params/agent.yaml` — PPO/seed/rollout
- `native_run/events.out.tfevents.*` — raw scalar 2998..4997
- `checkpoints/model_4997.pt` — SHA `9881687e…34fcf6`
- `console.log` — exit 0, native selector `6.0818 @4794 → model_4800`

**H-008 corrected control train archive**

- 동일 상대 경로
- `source/humanoid_rewards.py` — hip `-0.2`
- `checkpoints/model_4997.pt` — SHA `4349fe56…3b5b6d`
- `console.log` — selector `5.7572 @4874 → model_4900`

**영상 묶음**

- H-011: `checkpoint-h1-model_4997-9881687e534a/video_suite_manifest.json`
- H-008: `checkpoint-h1-model_4997-4349fe565013/video_suite_manifest.json`
- 각 묶음 `videos/{stairs,inverted_stairs,boxes,random_rough,slope_up_10deg,slope_down_10deg}.mp4`

**프로젝트 해석 기준 참고**

- `11_SERVER_OPERATIONS(20260924-141416).md` — resume final checkpoint 원칙, PERSONAL 6-terrain suite의 역할/경계
- `16_EXPERIMENT_EXPORT_AND_TENSORBOARD(20260924-141415).md` — raw TensorBoard, same-parent unchanged control 우선, video/evaluator 구분
- `18_H1_FINALIZE_REPORT_LIMITATIONS(20260922-160915).md` — native warm-up selector와 automatic best 한계

---

## 최종 결론

H-011 `joint_deviation_hip -0.1` corrected sibling은 **H-008 control의 6지형 traversability를 잃지 않았고, 후반 XY/yaw tracking에 작은 개선 신호가 있으며 boxes 영상에서 더 큰 진행을 보이는 질적 단서가 있다.** 동시에 **flat orientation과 torso-deviation 비용은 더 나빠지고, base-contact/episode-length 우위는 window를 좁히면 사라지거나 뒤집힌다.** 따라서 현재 자료는 “hip penalty 완화가 명백히 더 좋은 정책을 만들었다”까지는 지지하지 않는다.

실행과 provenance는 정상이고 가설 자체는 유효하므로 **HOLD**가 맞다. 양쪽 대표 checkpoint는 **final `model_4997.pt`**다. 다음 판단을 바꿀 가장 큰 정보는 새 학습이 아니라 **동일 command·terrain·initial state의 paired fixed evaluator + raw hip/torso posture telemetry**다.
