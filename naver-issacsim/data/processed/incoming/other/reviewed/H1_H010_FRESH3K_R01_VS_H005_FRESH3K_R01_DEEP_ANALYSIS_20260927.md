# H1 H-010 fresh3K R01 vs H-005 fresh3K R01 심층 분석

- 작성일: 2026-09-27
- 로봇: Unitree H1 / `Humanoid-v0`
- 주 비교 A: `20260927-043527-h1-h010-fresh3k-r01-20260927`
- 주 비교 B: `20260927-032343-h1-h005-fresh3k-r01-20260927`
- 맥락 참고 C: `20260925-102659-h1-h010-r02-airtime025-corrected-h1-corrected-20`
- 환경 분류: 세 Run 모두 `PERSONAL`
- 분석 범위: 제공된 학습 archive 3개, 6지형 영상 bundle 3개, 프로젝트 핵심팩의 계보·checkpoint 해석 규칙

> A/B 표기는 사용자가 역할을 명시하지 않은 상태에서 **reward diff와 가설 ID를 기준으로 분석 편의를 위해** 정했다. A를 우월 정책으로 가정하지 않는다. 실제 단일변수 질문은 `track_lin_vel_xy_exp 0.50 → 0.75`이며, B가 0.50, A가 0.75다.

---

## 1. 결론 요약

### 질문 1 — 이번 정책 A는 목표 행동을 실제로 얼마나 수행하는가?

A(H-010 fresh, `track_lin_vel_xy_exp=0.75`)는 **선형 속도 추종과 실제 지형 진행 쪽을 분명히 더 강하게 학습한 흔적**이 있다.

- 동일 정의의 TensorBoard late-500에서 XY 속도 오차는 B `0.37355` → A `0.33248`로 `-0.04108` 감소했다. B 대비 약 11.0% 낮다.
- 이 차이는 late-700 `-0.03949`, late-300 `-0.04317`로 window를 바꿔도 유지된다.
- 6지형 영상의 sampled frames에서 A의 `boxes`는 약 16초 시점에 장애물 patch 밖으로 나온 반면 B는 19초 프레임까지 patch 내부에 남아 있었다. `random_rough`도 A가 약 16초에 patch 밖, B는 약 19초에 밖으로 나오는 장면이 확인된다.
- stairs / inverted stairs / 두 slope에서도 sampled frames 기준 양쪽 모두 upright 상태로 지형을 지나가는 장면이 확인되며, A가 명백히 정체하는 장면은 없다.

그러나 **전체 locomotion 품질이 좋아졌다고 결론낼 수는 없다.** 같은 late-500에서 yaw 오차는 B `1.02692` → A `1.58899`로 `+0.56206` 증가했고, training base-contact termination도 `29.94% → 30.49%`, 평균 episode length도 `775.83 → 759.33 steps`로 악화됐다. 행동 비용도 A가 더 크다. 즉 A는 “더 잘 나아가는 대신 방향 추종·부드러움·자세 비용 일부를 잃은 정책”에 가깝다.

### 질문 2 — 무엇이 관찰된 차이이고, 무엇을 설정 변경의 효과로 해석할 수 있는가?

이번 fresh A/B는 현재 자료 중 **reward 효과를 보기 가장 좋은 비교**다.

- 두 archive의 `source/identity.json`을 대조하면 `train.py`, `play.py`, `env_cfg.py`, `agent_cfg.py`, `_finalize.py`, `pyproject.toml`은 SHA-256이 동일하다.
- `source/humanoid_rewards.py`의 실제 diff는 한 줄뿐이다.

```diff
- "track_lin_vel_xy_exp": 0.5,
+ "track_lin_vel_xy_exp": 0.75,
```

- native `env.yaml` diff도 log directory와 위 reward weight 외에는 없다.
- `agent.yaml`은 byte-level 내용상 동일하다.
- 양쪽 모두 seed 42, 4096 env, 3000 iterations, 24 rollout steps/env/iteration, 동일 PPO 설정, 동일 source를 사용한다.

따라서 **이 단일 실행 계보 안에서** XY 개선·yaw 악화·action/posture cost 증가는 `track_lin` 강화와 연결된 효과라는 해석에 상당한 근거가 있다. 다만 terrain generator seed가 `null`이고, 단일 seed이며, CUDA/환경 비결정성이 있으므로 이를 여러 seed·공식 평가에 일반화한 인과 효과로 확정하지 않는다.

영상 차이는 더 약한 근거다. 세 video manifest에는 source checkpoint SHA는 있으나 **command sequence, terrain seed, difficulty, initial state가 기록되어 있지 않다.** 따라서 boxes/rough에서 A가 더 빨리 patch를 벗어난 것은 관찰된 행동 차이이지만, 정확한 paired traversal time이나 reward의 인과 효과로 승격시키지 않는다.

### 질문 3 — 현재 자료에서 내려야 할 결정과 가장 먼저 풀 불확실성

**가설 판단: `PROMOTE — fixed paired evaluation 단계에만`, 최종 채택은 아님.**

이유는 긍정 신호가 작지 않기 때문이다. A의 XY 개선은 late window 전체에서 일관되고, 영상에서도 boxes/rough 진행이 더 적극적이다. 반면 yaw 악화가 훨씬 크고, action-rate/slide/hip 관련 weighted cost와 exploration std도 증가한다. 이 trade-off를 native training scalar와 unmatched video만으로 어느 쪽이 공식 평가에 유리한지 정할 수 없다.

**다음 한 번의 행동은 새 학습이 아니라 기존 final checkpoint의 고정 paired 평가다.**

- A: fresh `model_2999.pt`, SHA-256 `088eb7fe725197a304065c348db69f431623d50eb644b2344a8ce811391ceb38`
- B: fresh `model_2999.pt`, SHA-256 `ff51151a037d25396f03c5032c1484f828c741a6dd54a3ac8713904d7cee25a2`
- 동일 command sequence / terrain seed / difficulty / initial state / evaluator version으로 비교
- 축별 `vx`, `vy`, yaw error, 실제 전진·traversal, stall, base-contact/fall, hip/torso posture, action delta를 함께 기록

final-vs-final을 우선하는 이유는 **동일 학습량 3000회**를 맞춰 reward 효과를 보는 데 가장 깨끗하기 때문이다. 현재 영상은 A `model_2700`, B `model_2750`이라는 각 Run의 자동 reward-best checkpoint로 생성돼 selector 효과와 50 iteration 차이가 섞여 있다.

---

## 2. 실제 Run·checkpoint·영상 identity

### 2.1 Run identity

| 항목 | A — H-010 fresh3K | B — H-005 fresh3K | C — H-010 corrected Run 02 |
|---|---|---|---|
| archive | `20260927-043527-h1-h010-fresh3k-r01-20260927.tar.gz` | `20260927-032343-h1-h005-fresh3k-r01-20260927.tar.gz` | `20260925-102659-h1-h010-r02-airtime025-corrected-h1-corrected-20.tar.gz` |
| mode | PERSONAL | PERSONAL | PERSONAL |
| fresh/resume | fresh | fresh | resume |
| status | COMPLETE, exit 0 | COMPLETE, exit 0 | COMPLETE, exit 0 |
| evidence validation | PASS | PASS | PASS |
| seed / envs | 42 / 4096 | 42 / 4096 | 42 / 4096 |
| requested training | 3000 | 3000 | +2000 |
| TensorBoard iteration | 0–2999 | 0–2999 | global 2998–4997 |
| transitions | 294,912,000 | 294,912,000 | child 추가 196,608,000 |
| wall time | 2459.9 s | 2448.5 s | 1677.5 s |
| checkpoint mirror | 61, 50-iter 간격 + final | 61, 50-iter 간격 + final | 21, 100-iter 간격 + final |
| parent | 없음 | 없음 | 기록상 corrected H-008 `model_2998.pt` |
| parent SHA | 해당 없음 | 해당 없음 | metadata 기록 `49fdb297924c861493d377f22b9de135d83c73969ef3d8a2e4a56c9879414983` |
| parent 원본 바이트 재검증 | 해당 없음 | 해당 없음 | **이번 입력에는 parent archive가 없어 미검증** |

C의 parent 연결은 child `metadata.json` / `resume_lineage`에 기록된 provenance다. 이번 입력에는 H-008 parent checkpoint 원본이 없으므로 “기록상 연결됨”이며 parent 바이트를 다시 SHA-256 계산해 대조한 것은 아니다.

### 2.2 실제 reward 설정

| reward | B H-005 fresh | A H-010 fresh | C H-010 R02 |
|---|---:|---:|---:|
| `track_lin_vel_xy_exp` | **0.50** | **0.75** | **0.75** |
| `track_ang_vel_z_exp` | 0.50 | 0.50 | 0.50 |
| `feet_air_time` | 0.25 | 0.25 | 0.25 |
| `termination_penalty` | -50 | -50 | -50.0 |
| `flat_orientation_l2` | -1.5 | -1.5 | -1.5 |
| `ang_vel_xy_l2` | -0.05 | -0.05 | -0.05 |
| `joint_deviation_hip` | -0.2 | -0.2 | -0.2 |
| `joint_deviation_torso` | -0.1 | -0.1 | -0.1 |
| `action_rate_l2` | -0.0005 | -0.0005 | -0.0005 |

A/B의 reward source diff는 `track_lin_vel_xy_exp` 한 줄뿐이다. C와 A의 reward 값은 의미상 동일하고 source diff는 `-50` 대 `-50.0` 표기뿐이다. 그러나 C는 다른 3K parent에서 +2K resume한 정책이라 fresh A와 동등한 training history가 아니다.

### 2.3 source/PPO/environment parity

A와 B에서 동일 확인된 source SHA:

- `h1_task/__init__.py`: `3334dc0a…d4026`
- `h1_task/_finalize.py`: `734b712f…ea1a`
- `h1_task/agent_cfg.py`: `4e8c9919…2bb6`
- `h1_task/env_cfg.py`: `78927fc5…adab`
- `play.py`: `39be98d4…2617`
- `train.py`: `36fcd90a…a358`

다른 것은 `humanoid_rewards.py`뿐이다.

공통 agent 설정:

- rollout: 24 steps/env/iteration
- PPO epochs / mini-batches: 5 / 4
- learning rate: 0.001 adaptive
- gamma / lambda: 0.99 / 0.95
- entropy coefficient: 0.008
- desired KL: 0.01
- fresh save interval: 50

공통 training environment:

- physics `dt=0.005`, decimation 4 → policy/control step 0.020 s
- episode limit 20 s
- terrain curriculum enabled
- terrain generator seed: `null`, cache false
- terrain proportions: stairs 0.15, inverted stairs 0.15, boxes 0.30, random rough 0.10, slope up 0.10, slope down 0.10
- command resampling: 10 s
- `lin_vel_x = [-1.0, 1.5]`, `lin_vel_y = [-0.5, 0.5]`, `ang_vel_z = [-1.0, 1.0]`, heading command enabled

같은 RL seed 42여도 terrain generator seed가 null이므로 정확히 같은 terrain realization/episode sequence를 보장하지 않는다.

### 2.4 checkpoint ↔ video 연결

선택 checkpoint를 archive에서 직접 SHA-256 계산하고 video manifest의 source SHA와 대조했다.

| 정책 | video source | checkpoint SHA-256 | 연결 결과 | 성격 |
|---|---|---|---|---|
| B H-005 fresh | `model_2750.pt` | `6d7d0ecb13c70730087d43a82f88f6386f1af8b5721ab0b13e32e110a43c29eb` | exact match | 자동 `model_best` |
| A H-010 fresh | `model_2700.pt` | `5d19578749df66e1c7fda6fc1d6fe62bedd0d87b11aeb99ada087638cddf3356` | exact match | 자동 `model_best` |
| C H-010 R02 | `model_4997.pt` | `fd497dcb7a763ca496996dde89f23308e5a45cb23d11fe1861d4e5d63947e5df` | exact match | final numbered + 자동 `model_best` |

세 video bundle 모두 manifest에 기록된 MP4 SHA-256을 실제 MP4와 다시 계산해 **6/6 PASS**했다.

각 MP4는 H.264, 1920×1080, 50 fps, 999 frames, 19.98 s였다.

### 2.5 stale artifact 제외

A archive의 `collected/provenance.json`에는 이전 작업공간의 다음 파일이 `UNCHANGED`로 남아 있다.

- `policy.pt`
- `policy.onnx`
- `play_video.mp4`
- 이전 H-005 시각의 `model_best_20260927032354.pt`, `env_20260927032354.yaml`

특히 A의 `play_video.mp4`는 이번 A fresh Run에서 새로 생성된 행동 증거가 아니다. C archive에도 `policy.pt`, `policy.onnx`, `play_video.mp4` 및 여러 과거 timestamp artifact가 `UNCHANGED`다. 이 파일들은 **이번 행동 분석에서 전부 제외**했다.

행동 근거는 별도 전달된 `checkpoint-h1-model_*.tar.gz`의 manifest-linked six-terrain MP4만 사용했다.

---

## 3. 비교 설계와 해석 가능한 범위

| 질문 | 판정 | 이유 |
|---|---|---|
| `track_lin 0.50→0.75`가 fresh 3K training metric에 미친 방향 | **직접 비교에 적합** | source/PPO/env/seed/학습량 동일, 실제 reward source 한 줄 diff |
| A와 B의 완성 policy 행동 차이 | **조건부 비교** | video checkpoint provenance는 강함. 하지만 command/terrain seed/difficulty/initial state가 manifest에 없음 |
| A가 공식 evaluator에서 B보다 우수한가 | **판단 불가** | fixed evaluator / OFFICIAL 점수 없음 |
| C H-010 R02와 A H-010 fresh 중 어느 training recipe가 우수한가 | **맥락 참고** | reward는 같지만 fresh 3K vs 다른 parent의 +2K resume, 총 history/초기 state 다름 |
| `feet_air_time=0.25` 자체 효과 | **이 A/B로 판단 불가** | A와 B 모두 0.25라 통제변수가 아니라 공통 배경 |

A/B는 동일 seed를 썼지만 독립 seed 반복이 아니다. TensorBoard 500 points는 500 independent trials가 아니며 자기상관이 강한 한 개 학습 trajectory다. 따라서 p-value나 seed-level confidence interval은 계산하지 않았다.

---

## 4. TensorBoard raw event 재분석

### 4.1 파싱 방법

각 archive의 `native_run/events.out.tfevents.*`를 TFRecord/Event protobuf 수준에서 직접 파싱했다.

- A: 3000 scalar points/tag, step 0–2999
- B: 3000 scalar points/tag, step 0–2999
- C: 2000 scalar points/tag, global step 2998–4997
- A/B 모두 주요 tag에 중복 step이나 reset 없음
- C도 global iteration을 유지해 reset 없음
- 각 Run 31 tags, 핵심 training tag 29개 + `/time` 계열 2개
- NaN/Inf scalar 없음

후반 primary window는 fresh Run의 마지막 500 iterations(`2500–2999`)로 정했다. 이유는 양쪽 모두 이미 terrain level 5대에 진입해 초기 curriculum 상승 구간의 영향이 줄어든 상태이며, 동일 길이의 마지막 구간을 비교하기 쉽기 때문이다. 선택 민감도는 late-700(`2300–2999`)와 late-300(`2700–2999`)로 재확인했다.

### 4.2 핵심 late-500 비교

| 지표 | B H-005 0.50 | A H-010 0.75 | A−B | 해석 |
|---|---:|---:|---:|---|
| terrain level | 5.50379 | 5.49196 | -0.01183 | 사실상 비슷함; A의 terrain 우위 없음 |
| XY velocity error | 0.37355 | **0.33248** | **-0.04108** | A의 명확한 선형 추종 개선 |
| yaw velocity error | **1.02692** | 1.58899 | **+0.56206** | A의 큰 yaw 추종 악화 |
| base-contact termination | 29.935% | 30.491% | **+0.56%p** | A가 약간 불리 |
| timeout | 70.074% | 69.520% | -0.55%p | base-contact 변화와 같은 방향 |
| mean episode length | 775.83 steps | 759.33 steps | -16.50 | A가 약 0.33 s 짧음(0.02 s/step 환산) |
| policy mean std | 1.34552 | 1.49844 | +0.15291 | A가 더 높은 exploration/action dispersion |
| value loss | 0.005126 | 0.006583 | +0.001458 | A가 높지만 발산 수준은 아님 |

`base_contact`는 training termination 집계이며 고정 evaluator의 낙상률과 동일시하지 않는다. `Train/mean_episode_length`는 simulation control steps로 해석했고, config의 0.020 s control period를 사용하면 B 약 15.52 s, A 약 15.19 s다.

### 4.3 window 민감도

| window | XY A−B | yaw A−B | terrain A−B | base-contact A−B |
|---|---:|---:|---:|---:|
| late-700 | -0.03949 | +0.57721 | -0.02160 | +0.44%p |
| late-500 | -0.04108 | +0.56206 | -0.01183 | +0.56%p |
| late-300 | -0.04317 | +0.54262 | -0.01867 | +1.09%p |

핵심 결론은 경계 선택에 민감하지 않다. **A는 XY가 약 0.04 좋아지고 yaw가 약 0.54–0.58 나빠지는 방향**이 후반 여러 window에서 유지된다.

### 4.4 학습 phase

500-iteration 평균을 따라가면 다음 패턴이 보인다.

| 구간 | terrain B→A | XY B→A | yaw B→A | base-contact B→A |
|---|---|---|---|---|
| 0–499 | 0.902→0.783 | 0.383→0.323 | 1.139→1.465 | 68.80%→68.35% |
| 500–999 | 4.206→3.887 | 0.426→0.403 | 1.563→2.335 | 32.66%→29.40% |
| 1000–1499 | 5.078→5.005 | 0.390→0.364 | 1.306→2.035 | 30.94%→30.20% |
| 1500–1999 | 5.282→5.196 | 0.376→0.348 | 1.145→1.869 | 31.01%→30.56% |
| 2000–2499 | 5.432→5.391 | 0.372→0.337 | 1.050→1.706 | 30.10%→29.85% |
| 2500–2999 | 5.504→5.492 | 0.374→0.332 | 1.027→1.589 | 29.94%→30.49% |

A는 처음부터 XY를 더 낮게 유지하지만 초기 curriculum progression은 B보다 느리다. 500–999에는 contact termination이 A가 일시적으로 더 낮았으나, 후반에는 이 장점이 사라지고 약간 반전된다. yaw 악화는 전체 학습에서 지속되며 후반에 줄어들기는 하지만 사라지지 않는다.

이 패턴은 단순한 “A가 더 빨리 수렴했기 때문”만으로 설명하기 어렵다. `track_lin` 강화가 translation 성능을 우선하도록 행동 분포를 바꾸고, yaw/자세/제어 비용과 경쟁하는 reward trade-off가 형성됐을 가능성이 높다.

### 4.5 행동 비용 term

아래는 late-500의 **logged weighted Episode_Reward contribution**이다. A/B에서 해당 항목의 weight와 계산 정의가 같으므로 방향 비교는 가능하지만, weight를 역산해 raw physical deviation을 만들지는 않았다.

| weighted term | B | A | A−B | 방향 |
|---|---:|---:|---:|---|
| `feet_air_time` | +0.013603 | +0.010843 | -0.002760 | A가 해당 positive contribution을 덜 얻음 |
| `flat_orientation_l2` | -0.012696 | -0.013065 | -0.000369 | A가 약간 더 큰 orientation cost |
| `ang_vel_xy_l2` | -0.022201 | -0.026577 | -0.004375 | A가 roll/pitch angular-velocity cost 증가 |
| `joint_deviation_hip` | -0.033701 | -0.038211 | -0.004510 | A가 hip deviation cost 증가 |
| `joint_deviation_torso` | -0.006327 | -0.006430 | -0.000102 | 거의 같음 |
| `action_rate_l2` | -0.063372 | -0.072626 | -0.009254 | A가 더 급격한 action 변화 비용 |
| `feet_slide` | -0.041988 | -0.051340 | -0.009352 | A가 더 큰 slide cost |

이 표는 A의 XY 개선이 “같은 gait를 조금 더 정확히 추종한 것”만은 아닐 수 있음을 보여준다. A는 더 높은 policy std와 함께 action-rate, slide, hip, ang-vel cost를 더 지불한다. **더 공격적으로 진행하지만 gait/control quality 일부를 희생하는 기전**과 일치한다.

### 4.6 최적화 안정성

- A/B raw scalar에서 NaN/Inf 없음.
- console은 두 Run 모두 `Learning iteration 2999/3000`, exit code 0.
- Traceback / CUDA OOM / 치명 오류는 발견되지 않았다.
- 초기 iteration 1의 value loss는 A `0.1789`, B `0.1808`이지만, iteration 100 이후 최대는 A `0.02088`, B `0.01096`이며 후반 평균은 각각 `0.00658`, `0.00513` 수준이다.
- A의 mean std가 높지만 수치 폭발이나 collapse는 아니다.

따라서 차이는 optimizer failure보다는 학습된 행동 trade-off로 보는 편이 현재 증거에 더 잘 맞는다.

---

## 5. checkpoint 해석

### 5.1 fresh A/B automatic best

B:

- raw `Train/mean_reward` 최대: `3.71809 @ iter 2747`
- nearest saved checkpoint: `model_2750.pt`
- current `model_best.pt` SHA가 `model_2750.pt`와 exact match

A:

- raw `Train/mean_reward` 최대: `4.85623 @ iter 2699`
- nearest saved checkpoint: `model_2700.pt`
- current `model_best.pt` SHA가 `model_2700.pt`와 exact match

A와 B는 `track_lin` weight가 다르므로 total mean reward 절댓값 `4.86 vs 3.72`를 정책 성능 우열로 비교하지 않는다. 이 값은 각 Run 내부의 자동 checkpoint selection을 설명하는 용도만 있다.

### 5.2 final checkpoint와 late 상태

B final `model_2999` endpoint:

- terrain 5.5872
- XY 0.3784
- yaw 1.0397
- base-contact 29.94%
- episode length 822.41

A final `model_2999` endpoint:

- terrain 5.5043
- XY 0.3249
- yaw 1.4778
- base-contact 31.48%
- episode length 695.74

A의 마지막 한 점은 contact/episode length가 불리하지만, 마지막 100회 평균은 terrain 5.5125, XY 0.3332, yaw 1.5597, base-contact 31.10%, episode length 749.24다. terrain과 tracking이 함께 붕괴한 상태는 아니다. 따라서 final checkpoint를 “실패”로 처리할 근거는 없다. 반대로 final 행동 영상도 없으므로 `model_2999`가 `model_2700`보다 실제 행동상 좋다고 주장할 근거도 없다.

**현재 행동이 직접 확인된 A checkpoint는 `model_2700`, B는 `model_2750`이다. final `model_2999` 행동은 미확인이다.**

### 5.3 C H-010 Run 02 selector 재현

C는 global 2998→4997 resume다.

- raw 전체 reward 최대: `6.33398 @ 3079`
- resume selector warm-up threshold: 약 `3197`
- eligible reward 최대: `5.98835 @ 4960`
- 저장 checkpoint 중 가장 가까운 것은 `model_4997.pt`
- current `model_best.pt` SHA = final `model_4997.pt` SHA

이는 프로젝트 핵심팩 `18_H1_FINALIZE_REPORT_LIMITATIONS.md`의 corrected H-010 selector 기록과 일치한다.

---

## 6. 여섯 지형 행동 분석

### 6.1 영상 조사 방법과 한계

이번 분석은 MP4를 byte/hash 확인한 뒤 프레임을 실제 디코딩해 조사했다.

- 모든 18개 영상: 약 4초 간격 overview sampling
- stairs / inverted stairs / boxes / random rough: 8–20 s 구간을 약 1초 간격으로 추가 sampling
- 모든 terrain: robot 주변 crop에서 frame 500 / 650 / 800 / 950, 즉 약 10 / 13 / 16 / 19 s를 추가 확인(영상 끝 경계에서 일부 마지막 crop이 비어 있는 경우 overview frame으로 보완)

따라서 **전체 50 fps 영상을 연속 재생해 gait cycle/jitter frequency를 계측한 분석은 아니다.** 짧은 순간의 hop, slip, contact recovery가 sample 사이에 있었을 수 있으므로 그런 현상은 없었다고 단정하지 않는다.

또한 video manifest에는 command, seed, difficulty, initial state가 없다. 같은 terrain label이고 화면상 layout이 유사해 보여도 matched episode로 취급하지 않는다.

### 6.2 terrain별 관찰

| terrain | A H-010 fresh `m2700` | B H-005 fresh `m2750` | C H-010 R02 `m4997` 참고 | 판단 한계 |
|---|---|---|---|---|
| stairs | 10 s 접근, 13 s경 stair 위/접촉, 16 s경 반대쪽으로 이탈, 19 s upright. sampled frames에서 진행 정체 없음 | 유사하게 stair를 통과하고 16–19 s에 반대쪽 평지. A와 큰 차이 확인 어려움 | 유사하게 통과, 16 s경 반대쪽 | command/난이도 미기록. step별 발 걸림·충격은 연속 영상 분석 아님 |
| inverted stairs | 10 s 구조 위, 13 s경 이미 하단/평지 쪽으로 빠져나오는 장면, 16–19 s 평지 | 10–13 s 구조 위/경계, 16 s경 구조 밖, 19 s 평지 | A와 비슷하거나 빠른 이탈 | A가 약간 빠른 진행처럼 보이나 matched episode 아님 |
| boxes | **가장 큰 차이.** 10–13 s patch 내부 진행, **16 s에는 patch 밖 평지**, 19 s 계속 전진 | 10–19 s sampled frames 내내 box patch 내부에 남음. 낙상은 sampled frame에서 없음 | 10 s patch, **13 s에는 거의/이미 평지**, 16–19 s 평지 | traversal time 차이는 강한 정성 신호지만 command/seed/difficulty 미기록 |
| random rough | 10–13 s rough patch 진행, **16 s경 patch 밖**, 19 s 평지 | 10–16 s patch 내부, **19 s경 patch 밖** | 10–16 s 경계 진행, 19 s 평지 | A가 더 적극적으로 전진한 듯하지만 정확한 command 불명 |
| slope up label | sampled frames에서 upright, 10–19 s 동안 지형을 따라 진행. 명확한 stall/fall 장면 없음 | sampled frames에서 upright, 유사한 진행 | sampled frames에서 upright | `10deg`는 bundle label이며 manifest 자체에 numeric slope/difficulty가 없어 각도 독립 검증 안 함 |
| slope down label | sampled overview/crops에서 upright, 명확한 정체 없음 | sampled frames에서 upright | sampled frames에서 upright | yaw command/실제 downhill heading을 알 수 없어 command-following 판정 보류 |

### 6.3 영상과 수치의 합치·충돌

**합치:**

- A가 boxes/rough patch를 더 빨리 벗어나는 장면은 late TensorBoard의 낮은 XY error와 일관된다.
- A의 높은 action std와 더 큰 action-rate/feet-slide/hip cost는 sampled frames에서 더 적극적인 stride를 보이는 인상과 방향상 맞는다. 다만 프레임 sampling만으로 step frequency나 실제 slide를 정량 판독하지 않았다.

**충돌 또는 미해결:**

- training late-500에서 A의 base-contact termination은 B보다 약간 나쁘지만, 제공된 짧은 영상 sample에서는 둘 다 명백한 낙상을 잡지 못했다. 이는 모순이 아니다. training termination은 수천 env/episode 집계이고 영상은 각 terrain 20초 single clip이다.
- A yaw error는 크게 나쁘지만 영상 manifest에 yaw command가 없어 화면만으로 그 yaw 병목을 검증할 수 없다.
- A/B의 terrain level은 거의 같은데 boxes에서 진행 차이는 크다. 이는 curriculum level 하나가 특정 fixed terrain traversal 성능을 대표하지 않는다는 점을 보여준다.

---

## 7. C: 과거 H-010 corrected Run 02가 주는 맥락

C는 A와 최종 reward 값은 같지만, corrected H-008 `model_2998`에서 `feet_air_time 0.20→0.25`로 +2K resume한 다른 training history다. 따라서 A의 direct control이 아니다.

raw late-500을 이번에 동일 parser로 다시 계산하면:

| metric | A H-010 fresh late-500 | C H-010 R02 late-500 |
|---|---:|---:|
| terrain | 5.49196 | **5.66105** |
| XY error | 0.33248 | **0.32958** |
| yaw error | 1.58899 | **1.36436** |
| base-contact | 30.491% | **28.821%** |
| mean episode length | 759.33 | **781.82** |
| mean std | 1.49844 | 1.45871 |

이 수치는 프로젝트 핵심팩 `14_H1_NEXT_RUN_PARAMETER_COMPARISON.md`에 보존된 corrected H-010 Run 02 late-500 수치와 사실상 일치한다.

해석은 다음과 같다.

1. `track_lin=.75 / feet=.25`라는 **같은 최종 reward 값 자체가 반드시 A fresh의 큰 yaw penalty를 고정적으로 만든다고 볼 수는 없다.** C에서는 yaw가 A보다 상당히 낮다.
2. 반대로 C가 더 좋다는 이유로 “resume가 항상 낫다”라고 말할 수도 없다. C는 처음 3K의 parent policy와 feet=.20 학습 history가 있고 추가 2K를 더 받았다.
3. 즉 A/B의 single-delta 효과와, C가 보여주는 lineage/training-stage 효과를 분리해야 한다.

C의 six-terrain sampled behavior도 boxes에서 약 13 s에 patch를 벗어나고, stairs/inverted/rough/slopes에서 upright 진행이 보인다. 이는 같은 최종 reward가 충분히 다른 behavior quality에 도달할 수 있다는 참고 증거다.

---

## 8. 핵심 발견별 경쟁 설명 검토

### 발견 A — H-010 fresh의 XY error가 확실히 낮다

**관찰**  
late-500 B `0.37355` vs A `0.33248`; late-300/700에서도 약 0.04 차이 유지. boxes/rough sampled frames에서도 A가 patch를 더 일찍 이탈.

**주 해석**  
`track_lin_vel_xy_exp` 0.50→0.75가 translation command 추종 압력을 높여 실제 진행을 더 공격적으로 만든 가능성이 높다.

**경쟁 설명**  
terrain generator seed null, episode command sequence 비동일, CUDA 비결정성으로 우연한 trajectory 차이가 일부 섞일 수 있다.

**반대 근거**  
terrain level은 A가 더 높지 않고, yaw·posture/action cost는 악화된다. 따라서 “전반적으로 locomotion이 좋아졌다”는 해석은 지지되지 않는다.

**판별 방법**  
동일 final checkpoint iteration, 동일 command/terrain/seed fixed evaluator에서 실제 displacement와 XY component error를 함께 측정.

### 발견 B — yaw error가 매우 크게 악화된다

**관찰**  
late-500 +0.562, late-300 +0.543, late-700 +0.577. 전체 학습 phase에서 A가 지속적으로 높다.

**주 해석**  
선형 추종 보상 강화가 정책 용량/행동 선택을 translation에 더 배분하면서 heading/yaw control과 trade-off를 만든 가능성이 높다.

**경쟁 설명**  
A가 다른 command realization에서 더 많은 회전 요구를 받았을 가능성, curriculum/episode reset 차이.

**반대 근거**  
C H-010 R02는 동일 최종 reward로 late yaw `1.364`, 즉 A보다 낮다. 따라서 reward 값 하나만으로 yaw 수준이 결정되는 것은 아니다.

**판별 방법**  
동일 yaw command transitions를 강제한 paired evaluator에서 yaw-rate error, heading drift, turn completion을 분리 측정.

### 발견 C — A의 gait/control 비용이 커진다

**관찰**  
action-rate, feet-slide, hip, ang-vel weighted cost가 모두 더 음수이고 std가 약 +0.153 높다.

**주 해석**  
더 적극적인 translation을 얻기 위해 빠른/큰 행동 변화와 접촉 품질을 희생했을 가능성.

**경쟁 설명**  
reward term이 episode 집계이므로 episode length/terrain mix 차이가 contribution에 영향을 줄 수 있다.

**반대 근거**  
짧은 sampled videos에서는 명백한 붕괴·낙상·한발 hop이 확인되지 않는다.

**판별 방법**  
fixed evaluation에서 raw foot contact/slide, action delta, torso/hip deviation을 직접 기록. weighted reward term을 weight로 나눠 raw deviation을 추정하지 않는다.

### 발견 D — 영상은 A의 traversal 이점을 시사하지만 quantitative proof는 아니다

**관찰**  
boxes A ~16 s exit vs B 19 s에도 patch 내부; rough A ~16 s exit vs B ~19 s exit.

**주 해석**  
A의 선형 추종 압력이 장애물 위에서도 진행을 높였을 가능성.

**경쟁 설명**  
video manifest에 command/seed/difficulty/initial state가 없으므로, 서로 다른 명령 또는 쉬운 realization 차이가 원인일 수 있다.

**반대 근거**  
stairs/slopes에서는 A/B의 명백한 차이가 작다.

**판별 방법**  
같은 terrain mesh/seed/difficulty와 같은 command로 traversal time, displacement, stall을 자동 기록.

---

## 9. 실행·evidence·가설·정책 판정

### 실행

- A H-010 fresh3K: **COMPLETE**
- B H-005 fresh3K: **COMPLETE**
- C H-010 corrected R02: **COMPLETE**

세 Run 모두 exit 0, full scalar event 존재, evidence validation PASS. 실행 성공과 정책 품질을 분리한다.

### evidence와 비교

- A/B 설정 single-delta: **강하게 확인**
- A/B raw TensorBoard 동일 정의 재계산: **확인**
- selected checkpoint ↔ video SHA: **확인**
- video MP4 6/6 SHA: **확인**
- A/B video command/terrain seed/difficulty matching: **미확인**
- 공식 evaluator: **없음**
- 복수 seed: **없음**

### 가설

**H-010 fresh의 `track_lin 0.50→0.75` 효과: `PROMOTE — fixed paired evaluation only`.**

판단 범위는 “이 fresh 3K 단일 seed에서 선형 추종/진행 신호가 충분히 커서 다음 고정 평가에 올릴 가치가 있음”이다. 최종 reward 채택, OFFICIAL 우월성, 제출 정책 승인을 의미하지 않는다.

### 정책

A의 장점:

- 일관된 XY error 개선
- boxes/rough의 더 적극적인 visual progression
- terrain level을 거의 유지

A의 약점:

- 매우 큰 yaw error 증가
- late base-contact/episode length 소폭 악화
- action-rate, slide, hip, angular-velocity cost 증가
- higher policy std

따라서 **현재 자료만으로 A를 B의 overall replacement라고 선택하지 않는다.**

---

## 10. 다음 한 번의 행동

### 1순위: 기존 final checkpoint A/B fixed paired evaluation

새 GPU 학습이 아니라 이미 보존된 checkpoint를 평가한다.

- A: `20260927-043527.../checkpoints/model_2999.pt`
  - SHA `088eb7fe725197a304065c348db69f431623d50eb644b2344a8ce811391ceb38`
- B: `20260927-032343.../checkpoints/model_2999.pt`
  - SHA `ff51151a037d25396f03c5032c1484f828c741a6dd54a3ac8713904d7cee25a2`

맞출 조건:

- evaluator implementation/version
- terrain type + exact terrain seed/mesh + difficulty
- initial state
- command sequence와 command switch 시점
- seed set
- episode horizon
- logging window

기록할 값:

- `vx`, `vy`, yaw-rate error를 축별로
- 실제 forward/lateral displacement
- terrain traversal 완료/진행률, stall time
- base-contact/fall, timeout, episode length
- hip/torso raw deviation, foot slide/contact, action delta
- scenario별 worst case

### 결과별 다음 결정

- A가 동일 조건에서 실제 진행·XY 이득을 유지하면서 yaw와 survival 손실이 작거나 회복되면: **PROMOTE를 유지하고 longer/official 후보 검토**.
- A의 yaw 손실이 fixed command에서도 크게 유지되고 overall 3-axis tracking 또는 survival을 깎으면: **이 background에서 track 0.75를 REJECT 또는 더 작은 micro-step 후보로 되돌림**.
- 차이가 fixed evaluator에서 사라지면: 현재 training/video 차이의 상당 부분을 stochastic trajectory/selector 영향으로 재분류하고 **HOLD**.

새 training을 바로 돌릴 정보 가치는 낮다. 현재 가장 큰 불확실성은 수렴 부족보다 **같은 episode에서 linear 이득과 yaw/안정 손실을 함께 재는 것**이다.

---

## 11. 한계

1. A/B는 단일 seed 한 번씩이다. 300/500개의 TensorBoard point를 independent samples로 보지 않았다.
2. terrain generator seed가 `null`이어서 같은 RL seed가 동일 terrain realization을 보장하지 않는다.
3. video manifest에는 command / terrain seed / difficulty / initial state가 없다.
4. 영상은 auto-best checkpoint A 2700, B 2750이고 final 2999 영상은 없다.
5. 프레임 조사 방식이므로 전체 gait cycle, 순간 slip, jitter frequency, 모든 낙상을 연속 계측하지 않았다.
6. training `base_contact`, `terrain_levels`, weighted reward terms는 fixed official evaluator score가 아니다.
7. 프로젝트 핵심팩에 기록된 공개 evaluator 구조는 제공된 운영진 답변 정리본에 기반하며, 이번 분석에서 evaluator 원코드를 독립 검증하지 않았다. 따라서 training XY/yaw 평균으로 공식 Tracking Score를 계산하지 않았다.
8. C의 parent SHA는 child metadata에서 확인했지만 parent archive 원본 바이트는 이번 입력에 없어 재해시하지 않았다.

---

## 12. 재확인 가능한 근거 위치

### B H-005 fresh

- 설정: `20260927-032343-h1-h005-fresh3k-r01-20260927/source/humanoid_rewards.py`
- env: `.../native_run/params/env.yaml`
- agent: `.../native_run/params/agent.yaml`
- raw scalar: `.../native_run/events.out.tfevents.1790479449.brev-b26rbxifs.22833.0`
- console: `.../console.log`
- checkpoint: `.../checkpoints/model_2750.pt`, `model_2999.pt`
- collected provenance: `.../collected/provenance.json`
- video manifest: `checkpoint-h1-model_2750-6d7d0ecb13c7/video_suite_manifest.json`
- videos: `.../videos/{stairs,inverted_stairs,boxes,random_rough,slope_up_10deg,slope_down_10deg}.mp4`

### A H-010 fresh

- 설정: `20260927-043527-h1-h010-fresh3k-r01-20260927/source/humanoid_rewards.py`
- env: `.../native_run/params/env.yaml`
- agent: `.../native_run/params/agent.yaml`
- raw scalar: `.../native_run/events.out.tfevents.1790483746.brev-b26rbxifs.35946.0`
- console: `.../console.log`
- checkpoint: `.../checkpoints/model_2700.pt`, `model_2999.pt`
- collected provenance: `.../collected/provenance.json`
- video manifest: `checkpoint-h1-model_2700-5d19578749df/video_suite_manifest.json`
- videos: 같은 6 terrain MP4

### C H-010 corrected R02

- 설정: `20260925-102659-h1-h010-r02-airtime025-corrected-h1-corrected-20/source/humanoid_rewards.py`
- metadata / resume lineage: `.../metadata.json`
- raw scalar: `.../native_run/events.out.tfevents.1790332037.brev-p049cuh9h.103027.0`
- checkpoint: `.../checkpoints/model_4997.pt`
- video manifest: `checkpoint-h1-model_4997-fd497dcb7a76/video_suite_manifest.json`

### 프로젝트 해석 규칙

- `14_H1_NEXT_RUN_PARAMETER_COMPARISON.md`: corrected lineage와 late-500 비교 경계
- `18_H1_FINALIZE_REPORT_LIMITATIONS.md`: resume finalizer warm-up과 final checkpoint 원칙, stale artifact 경계
- `16_EXPERIMENT_EXPORT_AND_TENSORBOARD.md`: raw event/영상/evidence 비교 원칙
- `10_SOLUTION_AND_VALIDATION_BLUEPRINTS.md`: 생존·실제 진행·추종·보행 품질을 분리하는 평가 원칙

---

## 최종 판단 한 문장

**`track_lin_vel_xy_exp 0.50→0.75`는 이번 fresh 3K에서 선형 추종과 장애물 진행을 실제로 강화했지만, yaw 추종과 gait/control 비용을 상당히 희생했다. 따라서 H-010은 채택이 아니라 “고정 paired evaluator에서 한 번 더 판별할 가치가 있는 후보”로 PROMOTE하고, 그 평가 전에는 H-005를 대체했다고 결론내리지 않는다.**
