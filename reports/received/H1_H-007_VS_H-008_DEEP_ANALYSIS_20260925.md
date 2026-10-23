> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/incoming/other/reviewed/H1_H-007_VS_H-008_DEEP_ANALYSIS_20260925.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# H1 H-007 vs H-008 심층 분석 — corrected H-001 control 포함

- 분석일: 2026-09-25
- 대상 로봇: H1 / `Humanoid-v0`
- 환경: **PERSONAL NVIDIA/Brev L40S** — 공식 제출 점수 근거가 아니라 가설 검증·정책 행동 비교용
- 비교 역할: 사용자가 A/B를 별도 지정하지 않았으므로 **H-007과 H-008을 대칭적으로 비교**하고, 함께 제공된 **corrected H-001을 matched unchanged control**로 사용했다.
- 최종 분석 대상 checkpoint: 세 Run 모두 `model_2998.pt`
- 학습 구간: 공통 parent `model_1499.pt`에서 global 1499→2998, 추가 학습 1500 iterations

## 1. 결론 요약

이번 corrected 자료는 과거 H-007/H-008의 계보 문제를 실제로 바로잡은 **동일 부모 sibling 단일변수 비교**다. 세 Run의 기록상 parent checkpoint SHA-256은 모두 `5e3a31502d229884f91faf38962ffd32d63db69a64ca46ed7c1c404671b8ad82`이고, `train.py`, `env_cfg.py`, PPO/agent 설정, seed=42, 4096 env, 학습량이 동일하다. 원본 `humanoid_rewards.py`와 실행 `env.yaml`을 diff하면 실질적 차이는 `track_lin_vel_xy_exp`뿐이다.

| Run | `track_lin_vel_xy_exp` | 역할 | 실행 / evidence | final checkpoint SHA-256 |
|---|---:|---|---|---|
| corrected H-001 | 0.50 | unchanged control | COMPLETE / PASS | `fc3c60cdff61c43b...` |
| H-008 | 0.75 | 작은 강화 | COMPLETE / PASS | `49fdb297924c8614...` |
| H-007 | 1.00 | 큰 강화 | COMPLETE / PASS | `3fed4affcce4a3b6...` |

### 세 질문에 대한 답

**1) 목표 행동을 실제로 얼마나 수행하는가?**  세 final 정책은 제공된 여섯 19.98초 영상에서 모두 upright locomotion을 보였고, stairs·inverted stairs·random rough·±10° slope에서 짧은 클립 내 명백한 낙상은 관찰되지 않았다. boxes에서는 control과 H-008이 약 12–16초 사이 중앙 obstacle 영역을 벗어나 진행하는 반면, H-007은 약 10–17초 동안 같은 중앙 평탄부 주변에 머물다가 18–19초에야 다시 obstacle 쪽으로 진행하는 장면이 보인다. 다만 manifest에는 command stream/seed/difficulty telemetry가 없으므로 이를 명령 미추종이나 정량 traversal 실패로 확정하지 않는다.

**2) 무엇이 관찰 차이이고 무엇을 설정 효과로 해석할 수 있는가?**  학습 raw scalar에서는 `track_lin_vel_xy_exp`를 높일수록 late-500 XY error가 **0.3695 → 0.3483 → 0.3366**으로 단조 감소한다. 반대로 yaw error는 **1.0455 → 1.5292 → 2.0117**로 크게 악화되고, action-rate·feet-slide·hip deviation 비용과 policy std도 단조 악화된다. 세 sibling이 같은 parent·source·PPO·학습량이고 실제 reward 차이가 linear-track weight 한 개뿐이므로, **이 계보·이 단일 seed 안에서는 linear tracking 강화가 XY 추종을 개선하면서 yaw·동작 비용을 희생하는 trade-off를 만든다는 해석이 강하다.** 단, terrain generator seed가 `null`이고 복수 seed가 없으므로 일반화된 최적값이나 공식 점수 효과로 확장할 수 없다.

**3) 현재 결정은 무엇인가?**  **H-007(track=1.0)은 현재 overall 정책 후보로 REJECT**, **H-008(track=0.75)은 HOLD**, corrected H-001은 control로 유지하는 것이 근거에 가장 잘 맞는다. H-007은 control 대비 XY가 약 8.9% 낮지만 yaw error가 약 92% 높고, action-rate/feet-slide/hip 비용과 std도 더 나쁘며 terrain·episode length 이득이 없다. H-008은 XY 약 5.7% 개선으로 trade-off가 H-007보다 작지만 yaw가 약 46% 악화되고 안정·동작비용 지표도 control보다 좋아지지 않아 PROMOTE 근거가 부족하다.

**다음 한 번의 행동:** 새 학습보다 먼저, 세 `model_2998`을 **동일 command stream·동일 terrain realization·동일 evaluator**에 놓고 x/y/yaw tracking과 actual progress를 분리 측정하는 paired fixed evaluation이 가장 정보가 크다. 현재 6지형 영상은 source checkpoint는 정확히 연결되지만 command/difficulty가 manifest에 없어 이 질문을 완전히 해결하지 못한다.

---

## 2. 실제 Run·checkpoint·영상 identity

### 2.1 받은 학습 원본

1. `20260925-064143-h1-h001-corrected-control-to3k-h1-corrected-2026.tar(1).gz`
   - archive SHA-256: `3b5a716e80325566e953c262640e69390d5d876350feaec94d87eb85eaa7b048`
   - run: `h1-h001-corrected-control-to3k-h1-corrected-20260925-03`
   - status: `completed`, evidence validation: `PASS`
   - source checkpoint: recorded SHA `5e3a3150...ad82`, start iteration 1499
   - final numbered checkpoint: `model_2998.pt`, SHA `fc3c60cd...8556a`

2. `20260925-081241-h1-h007-r02-lintrack100-corrected-h1-corrected-2.tar.gz`
   - archive SHA-256: `85307507cafe09f1b7f118fb907d95185664d89ee43d693fdd3e4e60313a8d3e`
   - run: `h1-h007-r02-lintrack100-corrected-h1-corrected-20260925-03`
   - status: `completed`, evidence validation: `PASS`
   - same recorded source checkpoint SHA `5e3a3150...ad82`
   - final `model_2998.pt`, SHA `3fed4aff...c2be5`

3. `20260925-084248-h1-h008-r03-lintrack075-corrected-h1-corrected-2.tar.gz`
   - archive SHA-256: `e6bfc5a3c242a8414afbf77d68d754093218aadeed93ef56c608d56842582c69`
   - run: `h1-h008-r03-lintrack075-corrected-h1-corrected-20260925-03`
   - status: `completed`, evidence validation: `PASS`
   - same recorded source checkpoint SHA `5e3a3150...ad82`
   - final `model_2998.pt`, SHA `49fdb297...14983`

각 archive 내부 `SHA256SUMS`는 직접 `sha256sum -c`로 검사했고 모두 PASS했다. 세 final checkpoint의 actor/critic tensor도 직접 로드해 finite임을 확인했다.

### 2.2 부모 identity의 확인 수준

세 metadata는 모두 다음을 기록한다.

- parent run: `NCRC_BATCH_h1-corrected-20260925-03_h001_corrected_1499`
- requested checkpoint: `model_1499.pt`
- source checkpoint SHA-256: `5e3a31502d229884f91faf38962ffd32d63db69a64ca46ed7c1c404671b8ad82`
- start iteration: 1499
- requested additional iterations: 1500
- final iteration: 2998

공급된 6개 파일 안에는 **부모 `model_1499.pt` 원본 바이트 자체는 없다.** 따라서 parent SHA는 “세 실행 metadata가 동일 parent를 기록함”까지는 직접 확인했지만, 별도 parent archive와 바이트 대조한 것은 아니다. 다만 세 TensorBoard의 step 1499에서 terrain `3.437958`, XY `0.013287`, yaw `0.019864`, base-contact `0`, episode length `11.52`가 일치하며, step 1500~1501도 거의 동일하게 출발한다. 이는 동일 parent에서 분기했다는 metadata와 강하게 일치한다.

### 2.3 실제 source/PPO 차이

`source/identity.json`의 hash를 비교한 결과:

- `train.py`: 동일 (`36fcd90a...`)
- `h1_task/env_cfg.py`: 동일 (`78927fc5...`)
- `_finalize.py`, `agent_cfg.py`, `play.py`, `pyproject.toml`: 동일
- `humanoid_rewards.py`: 세 Run만 서로 다름

`native_run/params/agent.yaml`은 세 파일이 byte-identical하다. PPO는 공통으로 24 steps/env/iteration, 5 epochs, 4 mini-batches, adaptive LR 0.001, gamma 0.99, lambda 0.95, entropy coef 0.008, desired KL 0.01, clip 0.2, max-grad-norm 1.0, save interval 100이다.

`env.yaml` 전체 diff에서 log directory를 제외한 실제 설정 차이는 다음 하나뿐이다.

```text
corrected H-001: track_lin_vel_xy_exp = 0.50
H-008:           track_lin_vel_xy_exp = 0.75
H-007:           track_lin_vel_xy_exp = 1.00
```

다른 주요 reward는 공통이다: `track_ang_vel_z_exp=0.5`, `feet_air_time=0.2`, `termination_penalty=-50`, `flat_orientation_l2=-1.5`, `ang_vel_xy_l2=-0.05`, `joint_deviation_hip=-0.2`, `joint_deviation_torso=-0.1`, `action_rate_l2=-0.0005`.

즉 **과거의 feet -0.2→+0.2 혼합 변경은 이번 corrected sibling에는 존재하지 않는다.** 이번 세 자료만 놓고 보면 linear-track weight 단일변수 비교가 성립한다.

### 2.4 영상 source 연결

세 영상 bundle의 manifest는 각각 `model_2998.pt` SHA를 명시하며, 그 SHA가 해당 학습 archive의 final checkpoint 실제 SHA와 정확히 일치한다.

| 정책 | 영상 bundle | manifest checkpoint SHA | 학습 final과 일치 |
|---|---|---|---|
| H-001 control | `checkpoint-h1-model_2998-fc3c60cdff61...` | `fc3c60cd...8556a` | 예 |
| H-007 | `checkpoint-h1-model_2998-3fed4affcce4...` | `3fed4aff...c2be5` | 예 |
| H-008 | `checkpoint-h1-model_2998-49fdb297924c...` | `49fdb297...14983` | 예 |

각 bundle의 `SHA256SUMS`도 6 MP4 + manifest 모두 PASS했다. 모든 영상은 H.264 계열 1920×1080, 50 fps, 999 frames, 19.98초다. 이번 영상은 stale `model_best`가 아니라 **각 Run final `model_2998` 행동 증거**다.

---

## 3. 비교 설계와 해석 가능한 범위

### 3.1 비교 적합성

| 조건 | H-001 control | H-008 | H-007 | 판단 |
|---|---|---|---|---|
| parent identity | 동일 기록 SHA | 동일 | 동일 | 직접 비교에 적합; parent 바이트 별도 미제공 |
| reward 차이 | lin 0.50 | lin 0.75 | lin 1.00 | **단일변수** |
| robot/source/PPO | 동일 | 동일 | 동일 | 직접 비교에 적합 |
| 추가 학습량 | 1500 | 1500 | 1500 | 동일 |
| global range | 1499–2998 | 1499–2998 | 1499–2998 | 동일 |
| seed / num_envs | 42 / 4096 | 42 / 4096 | 42 / 4096 | 동일 |
| terrain generator seed | `null` | `null` | `null` | 같은 학습 seed만으로 terrain realization 동일 보장 불가 |
| curriculum | enabled, 10×20 | 동일 | 동일 | 동일 설정 |
| command range | x -1~1.5, y -0.5~0.5, yaw -1~1 | 동일 | 동일 | 학습 설정 동일 |
| 영상 terrain | 같은 6 label | 같음 | 같음 | 정성 비교 가능 |
| 영상 command/difficulty/seed | manifest에 없음 | 없음 | 없음 | strict paired behavior 비교는 불가 |
| 공식 여부 | PERSONAL | PERSONAL | PERSONAL | 공식 성능 주장 불가 |

**Reward 변경 효과 질문:** 이 계보의 단일 seed·1.5K 추가학습 범위에서는 **직접 비교에 적합**하다. 특히 XY/yaw/action-cost의 지속적 방향 차이는 reward change와 연결할 수 있다. 다만 terrain stochasticity와 단일 seed 때문에 일반화·최적값 확정은 불가하다.

**완성 정책 행동 질문:** 세 final checkpoint의 6지형 영상은 source SHA가 정확히 연결되어 있으므로 qualitative behavior 비교에 유효하다. 그러나 공통 evaluator/command stream가 없으므로 성능 점수 비교나 success rate로 바꾸지 않는다.

**OFFICIAL 제출 질문:** PERSONAL 자료이므로 맥락 참고만 가능하다.

---

## 4. TensorBoard raw 시계열 재분석

### 4.1 파싱 방법

각 archive의 `native_run/events.out.tfevents*`를 protobuf TFRecord로 직접 파싱했다.

- 각 Run: scalar tag 31종
- 핵심 tag마다 n=1500
- global step: 1499..2998
- duplicate step: 0
- step reset: 없음
- event file: Run당 1개

주 비교 window는 **late-500 = 2499–2998**이다. 이유는 모든 Run이 1500-step resume이고, 초반 curriculum 재적응을 충분히 지난 뒤 전체의 마지막 1/3을 비교해 endpoint spike의 영향을 줄이기 위해서다. 민감도 확인은 **late-300 = 2699–2998**로 했으며 핵심 방향은 동일했다.

### 4.2 curriculum 재적응

세 Run은 시작 terrain `3.43796`에서 약간 하락한 뒤 빠르게 회복한다.

| Run | 최소 terrain / step | 시작 수준 재돌파 | 최대 terrain / step | endpoint |
|---|---|---|---|---:|
| H-001 | 3.1612 @1513 | 1547 | 5.5666 @2756 | 5.4950 |
| H-008 | 3.1558 @1515 | 1545 | 5.5117 @2613 | 5.4557 |
| H-007 | 3.1555 @1515 | 1547 | 5.5034 @2751 | 5.4522 |

세 Run의 early dynamics가 매우 비슷한 것은 shared parent 기록과 일치한다. late에는 control이 terrain 평균에서 작지만 일관된 우위를 보인다.

### 4.3 late-500 핵심 비교

직접 재계산값, window 2499–2998, TensorBoard scalar 500점 평균:

| 지표 | H-001 0.50 | H-008 0.75 | H-007 1.00 | 해석 |
|---|---:|---:|---:|---|
| `Metrics/.../error_vel_xy` | **0.3695** | 0.3483 | **0.3366** | lin weight↑에 따라 XY error↓ |
| `Metrics/.../error_vel_yaw` | **1.0455** | 1.5292 | **2.0117** | lin weight↑에 따라 yaw error 크게↑ |
| `Curriculum/terrain_levels` | **5.5010** | 5.4526 | 5.4302 | control이 약간 높음 |
| `Episode_Termination/base_contact` | **29.62%** | 30.56% | 30.47% | track 강화가 낙상 proxy를 개선하지 않음 |
| `Train/mean_episode_length` | **777.66** | 766.04 | 764.39 | control이 길음 |
| `Policy/mean_std` | **1.3432** | 1.5042 | **1.6272** | track 강화에 따라 exploration/action spread↑ |
| `Episode_Reward/action_rate_l2` | **-0.06310** | -0.07506 | **-0.08528** | 동일 weight에서 action-rate cost 악화 |
| `Episode_Reward/feet_slide` | **-0.04586** | -0.05435 | **-0.06301** | sliding cost 악화 |
| `Episode_Reward/joint_deviation_hip` | **-0.03508** | -0.03821 | **-0.04351** | hip deviation cost 악화 |
| `Episode_Reward/flat_orientation_l2` | **-0.01078** | -0.01167 | **-0.01355** | orientation cost 악화, 특히 H-007 |
| `Loss/value` | **0.00495** | 0.00666 | **0.00856** | 더 높지만 finite·폭발 없음 |

`Episode_Reward/*`는 reward contribution이며 물리 단위 자체가 아니다. 다만 해당 항목들의 **weight와 구현은 세 Run에서 동일**하므로 같은 tag의 상대 방향은 행동 비용 변화의 보조 근거로 사용할 수 있다.

### 4.4 control 대비 효과 크기

late-500 기준:

- **H-008 (0.75 vs 0.50)**
  - XY error: **-5.75%**
  - yaw error: **+46.3% 악화**
  - terrain: -0.0484 (-0.88%)
  - base-contact: **+0.94%p**
  - episode length: -1.49%
  - policy std: +12.0%
  - action-rate contribution 절댓값: 약 +19.0%
  - feet-slide contribution 절댓값: 약 +18.5%

- **H-007 (1.00 vs 0.50)**
  - XY error: **-8.90%**
  - yaw error: **+92.4% 악화**
  - terrain: -0.0708 (-1.29%)
  - base-contact: **+0.86%p**
  - episode length: -1.71%
  - policy std: +21.1%
  - action-rate contribution 절댓값: 약 +35.1%
  - feet-slide contribution 절댓값: 약 +37.4%

- **H-007 (1.00) vs H-008 (0.75)**
  - XY error 추가 개선: **-3.35%**
  - yaw error 추가 악화: **+31.5%**
  - policy std: +8.18%
  - action-rate cost 절댓값: +13.6%
  - feet-slide cost 절댓값: +15.9%
  - hip-deviation cost 절댓값: +13.9%

즉 0.75→1.0에서 얻는 추가 XY 이득은 작아지는 반면 yaw와 동작 비용은 계속 크게 악화된다. **diminishing return + trade-off 확대**가 핵심 패턴이다.

### 4.5 window 민감도

late-300(2699–2998)에서도 같은 방향이다.

| 지표 | H-001 | H-008 | H-007 |
|---|---:|---:|---:|
| terrain | 5.5219 | 5.4498 | 5.4543 |
| XY error | 0.3689 | 0.3473 | **0.3326** |
| yaw error | **1.0407** | 1.5231 | **2.0104** |
| base-contact | **29.79%** | 30.65% | 30.53% |
| episode length | **777.91** | 766.47 | 764.54 |
| std | **1.3398** | 1.5021 | 1.6289 |

따라서 late-500 경계를 조금 바꾼 결과가 아니다.

### 4.6 학습 안정성과 late deterioration

NaN/Inf는 핵심 loss·reward·terrain·std 전체에서 발견되지 않았다. value loss 최대는 H-001 0.0327@1499, H-008 0.0152@1519, H-007 0.0248@1499로 resume 시작부가 가장 크고 이후 안정적이다.

late-500 slope에서 세 Run 모두 terrain이 붕괴하지 않는다. H-001/H-007 terrain은 오히려 완만한 상승이고, H-008은 거의 평탄하다. XY error도 세 Run 모두 late-500에서 완만히 감소한다. 따라서 **final `model_2998`을 배제할 만한 공동 late collapse는 없다.**

---

## 5. automatic best와 final checkpoint

native finalizer/report의 선택은 다음과 같다.

| Run | raw global reward max | selector eligible best | `model_best.pt` 실제 일치 | final |
|---|---|---|---|---|
| H-001 | 3.662 @2878 | 동일 | `model_2900.pt` SHA와 동일 | `model_2998.pt` |
| H-008 | 6.849 @1545 | 5.724 @1677 | `model_1700.pt` SHA와 동일 | `model_2998.pt` |
| H-007 | 10.171 @1565 | 8.686 @1680 | `model_1700.pt` SHA와 동일 | `model_2998.pt` |

resume selector는 약 step 1648 이전을 warm-up으로 제외하기 때문에 H-007/H-008의 raw global peak가 자동 best가 아닌 것은 예상되는 동작이다. 또한 Run 사이에는 linear-track reward weight가 다르므로 `Train/mean_reward` 절댓값을 정책 우열로 사용할 수 없다.

이번 영상 source는 세 정책 모두 `model_best`가 아니라 **final `model_2998`**이다. 충분히 진행된 resume에서 late terrain·tracking·fall의 공동 붕괴가 없으면 final numbered checkpoint를 대표 후보로 보는 현재 프로젝트 원칙과 일치한다.

---

## 6. 여섯 지형 행동 비교

### 영상 판독 범위

각 19.98초 MP4 전체를 디코딩 가능한지 확인했고, 비교를 위해 2초 간격 전체 contact sheet와 중요 구간은 0.5~1초 간격 프레임으로 추가 확인했다. 따라서 아래는 **연속 영상의 프레임 시계열을 이용한 정성 관찰**이지, telemetry 기반 보행 주기·거리·각도 측정은 아니다.

manifest에 terrain label과 source checkpoint SHA는 있지만 command stream, evaluation seed, difficulty, world-frame pose telemetry가 없다. 같은 이름의 지형이라도 세 영상이 같은 mesh realization·같은 command를 받았다고 가정하지 않는다.

| 지형 | corrected H-001 (0.50) | H-008 (0.75) | H-007 (1.00) | 공통 약점 / 한계 |
|---|---|---|---|---|
| stairs | 약 7–17초 샘플에서 upright를 유지하며 계단 위에서 지속 보행. 명백한 낙상 없음. | 유사하게 upright, 여러 계단 접촉을 지나며 보행 지속. | 유사하게 upright; 몸통/팔 자세 변화가 더 커 보이는 프레임이 있으나 정량화 불가. | command·동일 stair realization 불명. 화면 중앙 여부로 진행량 판단 금지. |
| inverted_stairs | 하강 계단 구간에서 upright, 연속 스텝 유지. | upright 유지, 하강 뒤 평탄부 쪽으로 이동. | upright 유지, 명백한 낙상 없음. | 하강 속도·yaw 추종은 telemetry 없어 판단 불가. |
| boxes | **10–12초 obstacle 경계**, 13–15초 주변 box를 지나고, 약 16초 이후 평탄부에 도달한 장면이 보임. | **10–12초 obstacle**, 13–16초 바깥쪽으로 진행, 17–19초 평탄부. control과 비슷하게 명확한 scene-relative progress. | **10–17초 중앙 평탄 platform 주변에 오래 머물며 주변 box 구조가 거의 유지**, 18–19초에야 obstacle 방향 이동이 커짐. 이 클립에서 세 정책 중 가장 뚜렷한 stall/저진행 신호. | command가 없으므로 H-007의 정체가 명령 위반인지 확정 못함. 단일 trajectory다. |
| random_rough | rough patch를 지나 late clip에서 가장자리/평탄부까지 진행, upright. | 유사하게 late clip에서 patch 밖/경계까지 진행, upright. | 약간 늦어 보이지만 late clip에서 patch 경계·평탄부까지 진행, upright. | 실제 이동거리·rough difficulty 미측정. |
| slope_up_10deg | 5,10,15,19초 샘플 모두 upright. | 동일하게 upright. | 동일하게 upright. | 세 영상의 heading이 다르게 보이며 command가 없어 “더 잘 추종” 판단 불가. |
| slope_down_10deg | 전체 샘플에서 upright, 경사 위 보행. | upright 유지. | upright 유지. | pitch/roll·속도 수치 없음. |

### 수치와 영상의 교차검증

- **XY tracking:** 학습 scalar에서는 H-007이 가장 낮은 XY error지만, boxes 영상에서는 오히려 가장 긴 scene-relative 정체가 관찰된다. 이는 “낮은 평균 XY error = 모든 험지에서 더 빠른 traversal”이 아님을 보여준다. command와 terrain realization이 통제되지 않아 정면 모순이라고 할 수는 없지만, **고정 evaluator에서 actual progress를 별도로 측정해야 한다는 강한 이유**다.
- **yaw:** H-007/H-008의 yaw error 악화는 영상의 다양한 heading 변화만으로 확인/반증할 수 없다. camera와 command가 없기 때문이다. 따라서 yaw 결론은 TensorBoard raw metric이 주 근거다.
- **낙상/안정:** 6×3개의 짧은 영상에서 명백한 낙상이 관찰되지 않았다는 사실은 late training base-contact 약 30%와 모순되지 않는다. 영상 한 trajectory의 무낙상은 training population의 termination fraction을 대신하지 않는다.
- **action cost:** H-007의 높은 std/action-rate/feet-slide cost와 영상상 더 큰 자세 변화가 일부 장면에서 함께 보이지만, 영상만으로 frequency/slide를 정량 측정하지 않았으므로 “영상이 수치를 증명”한다고 표현하지 않는다.

---

## 7. 핵심 발견과 경쟁 설명

### 발견 A — linear-track 강화는 의도한 XY 축에는 실제 효과가 있다

**관찰:** late-500 XY error가 0.3695(control) → 0.3483(H-008) → 0.3366(H-007)로 단조 개선한다. early-300에서도 0.3526 → 0.3436 → 0.3335로 같은 방향이다.

**해석:** `track_lin_vel_xy_exp` weight 상승이 PPO 업데이트에서 linear command 추종을 더 강하게 선택하도록 만든 결과와 일치한다. 이번 세 sibling은 실제 단일변수 차이여서 과거 mixed-delta 자료보다 인과 해석이 훨씬 강하다.

**경쟁 설명:** terrain generator seed가 null이고 단일 seed이므로 각 Run의 stochastic terrain 경험 차이가 일부 효과 크기에 섞일 수 있다.

**반대 근거:** actual terrain progression, episode length, base-contact가 함께 좋아지지는 않았고 boxes clip의 H-007 진행도 더 좋지 않다. 따라서 “XY 개선 = 전체 locomotion 개선”은 성립하지 않는다.

**판별:** 동일 command/terrain fixed evaluator에서 x/y error와 world displacement를 동시에 측정한다.

### 발견 B — 얻은 XY 성능보다 yaw·동작비용 손실이 빠르게 커진다

**관찰:** late-500 yaw error는 control 대비 H-008 +46%, H-007 +92%. 0.75→1.0의 추가 XY 개선은 3.35%인데 yaw는 추가 31.5% 악화한다. action-rate, slide, hip, orientation 비용과 std도 0.5→0.75→1.0 순으로 악화한다.

**해석:** policy capacity/behavior가 linear translation을 더 강하게 최적화하면서 회전 제어와 smooth/stable gait의 비용을 지불하는 trade-off로 볼 수 있다. `track_ang_vel_z_exp` 자체는 0.5로 고정돼 있어 상대적으로 linear objective의 비중이 커진 것도 이 방향과 맞는다.

**경쟁 설명:** 동일 seed라도 terrain realization 차이, curriculum 분포 차이가 yaw 평균에 영향을 줄 수 있다.

**반대 근거:** terrain 차이는 작고 H-007의 late XY는 일관되게 좋다. 즉 정책이 전체적으로 붕괴한 것은 아니다. 특정 축의 specialization에 가깝다.

**판별:** 고정 forward/lateral/yaw/stop command를 분리해 같은 final checkpoint들을 평가한다. 특히 yaw-only와 combined command에서 trade-off 크기를 확인한다.

### 발견 C — H-007의 boxes clip은 “tracking scalar만으로 선택하면 놓치는” 행동 경보다

**관찰:** boxes 10–17초 동안 H-007은 중앙 platform 주변 geometry가 거의 유지되고, control/H-008은 12–16초 사이 obstacle 영역을 빠져나오는 scene-relative 이동이 명확하다.

**해석:** 높은 lin-track weight가 평균 velocity error를 낮추면서도 특정 obstacle transition에서 신중한/제자리성 동작을 만들었을 가능성이 있다.

**경쟁 설명:** 가장 중요하다. **영상 command stream과 terrain seed가 기록되지 않았다.** H-007이 실제로 정지/회전 command를 받았다면 이 장면은 실패가 아닐 수 있다.

**반대 근거:** stairs, inverted stairs, random rough, slopes에서는 H-007도 upright locomotion을 수행한다. 따라서 “H-007은 traversal을 못 한다”는 결론은 과장이다.

**판별:** boxes fixed command에서 forward displacement, stall time, XY/yaw error를 동시 기록한다. 새 학습 없이 현재 세 checkpoint로 해결 가능하다.

---

## 8. Checkpoint·가설·정책 판단

### 실행

- corrected H-001: **COMPLETE**, evidence **PASS**
- H-007 corrected: **COMPLETE**, evidence **PASS**
- H-008 corrected: **COMPLETE**, evidence **PASS**

실행 실패와 비교 제한을 혼동할 이유가 없다. 세 실행 모두 정상 완료했고 비교 evidence도 충분히 보존됐다.

### 가설 판정

#### H-007 / `track_lin_vel_xy_exp = 1.0`

**판정: REJECT — “전체 정책 개선 후보” 범위에서.**

- 지지: XY tracking 자체는 가장 좋다.
- 기각 근거: yaw error가 control의 약 1.92배, std +21%, action-rate/slide/hip/orientation cost 악화, terrain·episode length 이득 없음.
- 영상 경보: boxes에서 긴 저진행 구간.
- 의미: “linear weight를 높이면 XY는 좋아진다”는 하위 기전 가설은 지지되지만, **1.0을 현재 overall policy로 채택할 근거는 없다.**

#### H-008 / `track_lin_vel_xy_exp = 0.75`

**판정: HOLD.**

- 지지: control 대비 XY error 약 5.7% 개선, H-007보다 yaw·동작비용 악화가 작음, 영상 6지형에서 upright locomotion과 boxes progress가 보임.
- 보류 근거: yaw +46%, base-contact +0.94%p, terrain/episode length 비개선, std/action/sliding 비용 상승.
- 의미: H-007보다는 trade-off가 완만하지만 **control보다 overall 우수하다고 말할 공통 evaluator가 아직 없다.**

#### corrected H-001 / `track_lin_vel_xy_exp = 0.5`

가설 후보가 아니라 **matched control**이다. late terrain, yaw, episode length, std, 여러 motion-cost 지표에서 가장 안정적인 기준점을 제공한다. XY는 세 정책 중 가장 나쁘다.

### 정책 대표 checkpoint

세 Run 모두 **final `model_2998.pt`를 대표 checkpoint로 유지**한다.

- final 구간 joint deterioration 없음
- 6지형 영상이 정확히 final SHA에 연결됨
- H-007/H-008 automatic `model_best=model_1700`은 resume 초기 eligible reward peak이며, 현재 행동 대표로 우선할 근거가 없다.
- control automatic best `model_2900` 역시 `model_2998`보다 공식 행동상 우수하다는 증거가 없다.

---

## 9. 다음 한 번의 행동

### 1순위 — 새 학습 없이 세 final checkpoint의 paired fixed evaluation

이번 결정을 가장 잘 바꿀 수 있는 정보는 **학습을 더 돌리는 것보다 현재 세 `model_2998`을 같은 evaluator에 놓는 것**이다.

- 대상: H-001 `fc3c60cd...`, H-008 `49fdb297...`, H-007 `3fed4aff...`
- 공통 조건: 동일 terrain realization / 동일 initial state / 동일 command sequence / 동일 horizon / 동일 evaluator version
- 최소 분리 시나리오:
  - forward linear command
  - lateral command
  - yaw-only command
  - boxes 또는 obstacle progress
  - stop/transition이 가능하면 추가
- 기록:
  - x/y/yaw tracking error
  - world-frame displacement 또는 obstacle progress
  - base-contact/fall
  - episode length/timeout
  - stall time
  - 가능하면 action-delta 또는 action-rate, body pitch/roll
- 질문:
  1. H-008의 XY 이득이 실제 progress를 늘리는가?
  2. H-008/H-007의 yaw 악화가 command-controlled evaluator에서도 재현되는가?
  3. H-007 boxes 정체가 command 차이였는가, 실제 traversal trade-off였는가?

### 결과별 다음 결정

- **H-008이 동일 evaluator에서 progress/XY를 개선하고 yaw·survival 손실이 작거나 시나리오상 상쇄된다면:** H-008을 PROMOTE 후보로 올리고 corrected lineage의 3K/5K 확장을 검토한다.
- **H-008의 yaw·stability 손실이 그대로 재현되고 overall behavior가 control을 넘지 못하면:** H-008도 REJECT하고 0.5 control을 유지한다. 더 긴 동일 0.75 학습은 우선순위가 낮다.
- **H-007 boxes stall과 yaw 악화가 fixed evaluation에서도 재현되면:** 1.0은 종료한다. 이미 현재 자료에서도 overall 후보로 REJECT이므로 추가 장기 학습의 정보가치는 낮다.

새 GPU 학습이 꼭 필요해진다면 다음 실험은 현재 matched parent에서 **0.5 vs 0.75의 동일 길이 확장**이 우선이며, 1.0을 다시 길게 돌리는 것은 현재 근거상 후순위다. 이 제안은 실행 승인이 아니다.

---

## 10. 한계와 재확인 가능한 근거

### 중요한 한계

1. 세 Run은 모두 PERSONAL이다. OFFICIAL 점수나 제출 성능이 아니다.
2. parent checkpoint 원본 바이트는 이번 입력에 없다. parent 동일성은 세 metadata의 같은 SHA와 초기 scalar 일치로 강하게 지지되지만 외부 parent archive와 직접 hash 대조하지 않았다.
3. training seed는 같지만 terrain generator seed는 `null`; 같은 terrain realization을 보장하지 않는다.
4. 단일 seed라서 시계열 500점을 독립 반복으로 취급하지 않았다. p-value/좁은 CI를 계산하지 않았다.
5. 영상 manifest에는 source SHA와 terrain label은 있으나 command stream, difficulty, eval seed, pose telemetry가 없다.
6. 19.98초 영상의 무낙상은 fall rate 추정이 아니다.
7. total mean reward는 linear-track weight가 달라 직접 성능 척도로 비교하지 않았다.

### 재확인 가능한 원본 위치

**학습 archive 내부**

- `metadata.json`: mode, parent/run/checkpoint, iteration, exit/evidence 상태
- `validation.json`: evidence validation
- `source/identity.json`: source 파일 hash와 실행 중 변경 여부
- `source/humanoid_rewards.py`: 실제 reward source
- `native_run/params/env.yaml`: effective env/reward/terrain/command 설정
- `native_run/params/agent.yaml`: PPO/runner 설정
- `native_run/events.out.tfevents*`: 이 보고서의 raw scalar 계산 원본
- `console.log`: iteration 출력과 native finalizer best 선택
- `checkpoints/model_2998.pt`: final 정책
- `collected/exported/model_best.pt`: automatic selector 산출물

**영상 bundle 내부**

- `video_suite_manifest.json`: source checkpoint SHA, terrain label, MP4 SHA
- `videos/stairs.mp4`
- `videos/inverted_stairs.mp4`
- `videos/boxes.mp4`
- `videos/random_rough.mp4`
- `videos/slope_up_10deg.mp4`
- `videos/slope_down_10deg.mp4`

### 프로젝트 해석 원칙과의 연결

제공된 프로젝트 핵심팩의 `18_H1_FINALIZE_REPORT_LIMITATIONS` 및 `16_EXPERIMENT_EXPORT_AND_TENSORBOARD`는 충분히 긴 resume에서 automatic best를 정책 품질의 자동 승자로 보지 말고, late terrain/tracking/fall이 함께 붕괴하지 않으면 final numbered checkpoint를 기본 대표로 보며, 6지형 영상은 정성 sanity evidence로만 사용하도록 정리한다. 이번 원본 결과는 그 원칙을 그대로 적용할 수 있는 사례다.

---

## 최종 판단표

| 항목 | corrected H-001 | H-008 0.75 | H-007 1.0 |
|---|---|---|---|
| 실행 | COMPLETE | COMPLETE | COMPLETE |
| evidence | PASS | PASS | PASS |
| corrected matched comparison | control | 직접 비교 적합 | 직접 비교 적합 |
| XY tracking | 기준 | 개선 | 가장 개선 |
| yaw tracking | **가장 좋음** | 뚜렷한 악화 | **매우 큰 악화** |
| terrain / episode stability | **가장 좋음** | 소폭 열세 | 소폭 열세 |
| action/sliding/posture cost | **가장 낮음** | 악화 | **가장 악화** |
| 6지형 영상 | 모두 upright; boxes 진행 | 모두 upright; boxes 진행 | 모두 upright; boxes 장시간 저진행 신호 |
| 가설 결정 | control | **HOLD** | **REJECT (overall candidate)** |
| 대표 checkpoint | `model_2998` | `model_2998` | `model_2998` |

**현재 자료가 말하는 핵심은 “linear tracking reward를 높이면 XY tracking은 실제로 좋아지지만, 0.75부터 yaw·동작비용을 눈에 띄게 잃고 1.0에서는 그 손실이 매우 커진다”는 것이다.** 따라서 1.0을 더 밀기보다, 0.75가 실제 fixed evaluator에서 control을 넘는지를 먼저 확인하는 것이 다음 의사결정의 정보가치가 가장 높다.
