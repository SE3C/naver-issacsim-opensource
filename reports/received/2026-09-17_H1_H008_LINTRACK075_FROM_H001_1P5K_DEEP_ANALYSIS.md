> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/incoming/other/reviewed/2026-09-17_H1_H008_LINTRACK075_FROM_H001_1P5K_DEEP_ANALYSIS.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# H1 H-008 LINTRACK075 from H-001 1.5K — Deep Analysis

**분석 대상:** `20260917-004530-h1-h008-lintrack075-from-h001-1p5k` 학습 evidence + 연결된 video evidence\
**분석일:** 2026-09-17\
**최종 판정:** **HOLD**\
**환경 분류:** **PERSONAL**\
**핵심 질문:** H-001 TERM50 1.5K 정책에서 `track_lin_vel_xy_exp`만 `0.5 → 0.75`로 높여 추가 1.5K fine-tuning 했을 때, 선형 속도 추종을 얻으면서 안정성·지형 능력을 유지할 수 있는가?

---

# 1. Executive Summary

이번 실행은 H1의 fresh training이 아니라, **H-001 1.5K TERM50 checkpoint `model_1499.pt`에서 이어서 학습한 PERSONAL resume/fine-tuning branch**다. parent checkpoint SHA-256은 `68fa0a9fe5334f8a3ecea110c4ccc9adb81ec07ac50169eaf8009b1a6e88f0c1`이며, 추가 학습은 1,500 iteration, 4,096 env, seed 42, headless로 정상 완료됐다. parent 대비 실제 reward 변경은 **`track_lin_vel_xy_exp: 0.5 → 0.75` 한 항목뿐**이며 `termination_penalty=-50`은 parent에서 이미 유지되던 값이다.

resume 직후 curriculum 평균 terrain은 `3.438 → 3.136`까지 내려갔지만 이는 알려진 resume curriculum reset/재적응 패턴과 일치한다. terrain은 global iter 1739부터 parent의 알려진 1.5K terrain `5.119`를 다시 넘었고, 마지막 500회 평균 `5.423`, endpoint `5.417`까지 회복했다. base-contact termination도 마지막 500회 평균 `30.74%`, endpoint `30.39%`로, parent H-001 1.5K의 알려진 `32.41%`보다 방향상 나쁘지 않다. 즉 **linear-tracking 강화가 stability를 즉시 붕괴시켰다는 증거는 없다.**

Tracking은 더 복잡하다. 이번 run의 XY velocity error는 마지막 500회 평균 `0.3499`, 마지막 100회 평균 `0.3394`, endpoint `0.3394`로 후반에 개선되는 방향을 보였다. 그러나 parent H-001의 동일 metric 전체 곡선/last-window가 이번 bundle에 없으므로, 이것을 `0.75` 변경의 인과 효과라고 확정할 수 없다. 반대로 yaw error는 post-reset 구간 평균 약 `1.31`에서 중·후반 `1.41~1.43` 수준으로 증가했고 endpoint도 `1.367`이다. **정책이 선형 이동 쪽으로 적응하면서 yaw 추종이 병목으로 남거나 더 악화되었을 가능성**이 강하다.

수치 안정성은 양호하다. value loss median `0.00681`, p95 `0.00773`, p99 `0.00814`, max `0.01681`이며 `0.1` 이상 spike가 한 번도 없다. NaN/Inf, CUDA OOM, optimizer crash, std 오류도 확인되지 않았고 보존된 16개 checkpoint의 actor/critic/optimizer tensor는 모두 finite였다. action std는 약 `1.34 → 1.49`로 올라간 뒤 후반 `1.48` 부근에서 머물지만, 높은 std 하나만으로 실패라고 볼 수는 없으며 실제 video에서는 20초 동안 upright locomotion이 유지된다.

중요한 checkpoint 문제도 있다. full raw TensorBoard의 `Train/mean_reward` 최고는 iter `1545`, `6.824`인데 report/finalize는 iter `1711`, `5.683`을 최고로 기록하고 `model_best.pt = model_1700.pt`를 선택했다. 원인 자체는 제공 evidence만으로 확정할 수 없다. 더 중요한 점은 **video도 이 model_1700을 재생한 것**이라, 후반 `model_2800/2900/2998`의 더 높은 terrain 및 더 낮은 XY error는 영상으로 검증되지 않았다.

따라서 이번 가설은 **REJECT할 정도로 나쁘지 않지만 PROMOTE하기에는 인과 evidence가 부족하다. 최종 판정은 HOLD**다. 가장 정보 효율이 높은 다음 실제 학습은 값을 또 올리는 것이 아니라, **같은 H-001 `model_1499.pt`에서 `track_lin_vel_xy_exp=0.5`를 그대로 둔 1.5K resume control branch**를 만드는 것이다. 이 control이 있어야 extra-training 효과와 `0.75` reward 효과를 분리할 수 있다.

---

# 2. Run Identity & Evidence Integrity

## 2.1 실험 정체성

| 항목 | 확인 결과 | 근거 강도 |
|---|---|---|
| Robot | **H1 / Humanoid-v0** | 확인됨 |
| Experiment ID | **H-008**로 취급 | metadata `name=h1-h008-...`; registry 원문은 bundle에 없어 registry-level 재검증은 못 함 |
| Run ID | `20260917-004530-h1-h008-lintrack075-from-h001-1p5k` | 확인됨 |
| Environment | **PERSONAL** | `metadata.json mode=personal` |
| 학습 형태 | **resume / fine-tuning** | 확인됨 |
| Parent run | `H001_PARENT_1P5K_LOCKED` | 확인됨 |
| Parent checkpoint | `model_1499.pt` | 확인됨 |
| Parent checkpoint SHA-256 | `68fa0a9f...e88f0c1` | 확인됨 |
| Requested additional iterations | **1500** | command/agent config |
| Global start iteration | **1499** | resume lineage |
| 마지막 console iteration | **2998/2999** | console/metadata |
| 마지막 저장 checkpoint | **model_2998.pt** | sidecar mirror |
| 저장 checkpoint 수 | **16개** | 1500~2900 every 100 + 2998 |
| seed | **42** | env/agent |
| num_envs | **4096** | command/env |
| rollout steps/env | **24** | agent.yaml |
| additional transitions | **147,456,000** | 4096×24×1500 |
| training | **headless, camera flag 없음** | command |
| video | headless + camera, 1 env, 1000 frames | video metadata |
| training start | 2026-09-17 00:45:30 UTC = **09:45:30 KST** | metadata |
| training end | 2026-09-17 01:06:06 UTC = **10:06:06 KST** | metadata |
| child-reported training time | **1214.84 s** | console |
| TensorBoard | **존재, 1 event, 31 scalar tags** | 확인됨 |
| console 전체 | **존재** | 확인됨 |
| play/video | **존재, lineage 연결됨** | 확인됨 |
| evaluator | **없음** | 판단 불가 |
| 공식 평가 결과 | **이번 run에는 없음** | PERSONAL |
| policy | video 실행에서 새로 export됨 | 확인됨 |
| ONNX | video 실행에서 새로 export됨 | 확인됨 |

### Fresh vs resume 판단

이 실행을 fresh trajectory의 단순한 “1.5K→3K 연속”으로 취급하면 안 된다. 명령 자체가 `--resume --load_run H001_PARENT_1P5K_LOCKED --checkpoint model_1499.pt`이며, H1 resume에서는 curriculum state가 원 정책 능력과 별개로 다시 쉬운 수준에서 재형성될 수 있다.

실제로 current event 첫 terrain은 `3.438`, 최저 `3.136 @ 1516`이다. 반면 parent H-001 1.5K의 알려진 endpoint terrain은 `5.119`다. 이는 resume 이후 curriculum 값이 parent의 직전 curriculum을 그대로 이어가는 형태가 아니라는 강한 관찰 증거다.

따라서 현재 run에서 **1499→2998 terrain 상승**은 “정책이 3.4에서 5.4까지 새로 실력을 얻었다”는 의미가 아니라, **reset된 curriculum을 parent 정책이 다시 올라간 뒤 fine-tuning을 계속한 궤적**으로 해석해야 한다.

---

## 2.2 Evidence 무결성

### 원본 archive

- Train archive:\
  `20260917-004530-h1-h008-lintrack075-from-h001-1p5k.tar.gz`\
  SHA-256: `06f7d1dad5b492e701587009f46811e8aa8e7a4504fba4d92f763db6b7c388b5`

- Video archive:\
  `20260917-010854-20260917-004530-h1-h008-lintrack075-from-h001-1p.tar.gz`\
  SHA-256: `d78257b8bc2cb5352b1674c31fc04d961fc854f17a41fff512f5b4bb2e57dde6`

두 extracted archive의 내부 `SHA256SUMS`는 로컬 재검증에서 모두 **100% PASS**했다.

### validation

Train evidence validation:

- native run copied: PASS
- TensorBoard: PASS (`events=1`)
- checkpoint mirror: PASS (`16`)
- source identity before/after: PASS
- collection freshness: PASS
- new/modified `model_best.pt`: PASS
- new/modified `env.yaml`: PASS
- finalize: PASS
- overall evidence validation: **PASS**

Video evidence validation:

- source identity: PASS
- fresh output collection: PASS
- fresh non-empty `play_video.mp4`: PASS
- overall: **PASS**

### 네 가지 상태를 분리한 판정

1. **학습 프로세스 정상 종료:** PASS\
2. **evidence 정상 보존:** PASS\
3. **정책 품질:** 부분적으로 유망하지만 미확정\
4. **제출 후보 적합성:** 이번 run은 PERSONAL이므로 공식 제출 성능 근거가 아니며, current evidence만으로 submit-ready 판정 불가

Evidence PASS는 “분석 가능한 run이 온전히 남았다”는 뜻이지 정책이 좋다는 뜻이 아니다.

---

## 2.3 실행 오류 검사

콘솔과 TensorBoard에서 다음 치명적 오류는 확인되지 않았다.

- NaN / Inf: **없음**
- CUDA OOM: **없음**
- optimizer/std exception: **없음**
- Python traceback: **없음**
- broken pipe: **없음**
- checkpoint 저장 실패: **없음**
- finalize failure: **없음**
- sidecar collection failure: **없음**

경고는 주로 Gym/RSL-RL deprecation, headless display 확인 불가, visualizer point-instancer 경고 등으로, 이번 정책의 numerical failure와 직접 연결되는 증거는 없다.

---

# 3. Configuration Verification

## 3.1 실제 적용 reward

`native_run/params/env.yaml`과 `source/humanoid_rewards.py`를 대조한 결과 주요 학생 reward는 다음과 같다.

| Reward | 실제 weight |
|---|---:|
| `track_lin_vel_xy_exp` | **+0.75** |
| `track_ang_vel_z_exp` | +0.50 |
| `feet_air_time` | +0.20 |
| `termination_penalty` | **-50.0** |
| `flat_orientation_l2` | -1.50 |
| `ang_vel_xy_l2` | -0.05 |
| `joint_deviation_hip` | -0.20 |
| `joint_deviation_torso` | -0.10 |
| `action_rate_l2` | -0.0005 |

프레임워크 기본 non-zero 항목도 유지된다.

- `dof_acc_l2=-1.25e-7`
- `dof_pos_limits=-1.0`
- `feet_slide=-0.25`
- `joint_deviation_arms=-0.2`

`dof_torques_l2`는 logger에 존재하지만 weight가 `0.0`이다.

## 3.2 parent 대비 실제 변경점

**가장 중요한 설정 해석:**

`report.html`은 배포 baseline(`termination_penalty=-5`, `track_lin=0.5`)과 현재 제출값을 비교하기 때문에 “두 reward가 바뀐 것처럼” 표시한다.

하지만 이번 실험의 parent는 이미 **H-001 TERM50**이다.

따라서 parent 대비 실제 experiment delta는:

```text
track_lin_vel_xy_exp: 0.50 → 0.75
```

**한 항목뿐이다.**

`termination_penalty=-50`은 이번 branch에서 새로 바꾼 값이 아니라 parent에서 유지한 stability anchor다.

이 차이는 인과 해석에 매우 중요하다. “이번 run에서 termination -50과 lin tracking 0.75를 동시에 바꿨다”고 쓰면 틀린 설명이다.

## 3.3 PPO / task / command

- PPO
- 5 epochs
- 4 mini-batches
- initial LR 1e-3 adaptive
- gamma 0.99
- lambda 0.95
- entropy coef 0.008
- desired KL 0.01
- max grad norm 1.0
- clip 0.2
- save interval 100
- actor/critic: 512→256→128 ELU
- observation/action: 기존 H1 task 구성
- episode horizon: 20 s
- command resampling: 10 s
- command range:
  - x: `-1.0 ~ +1.5 m/s`
  - y: `-0.5 ~ +0.5 m/s`
  - yaw: `-1.0 ~ +1.0 rad/s`
- `rel_standing_envs=0.02`
- heading command enabled

PPO/task 설정을 이번 reward 실험에서 임의 변경했다는 증거는 없다.

## 3.4 Terrain

- curriculum enabled
- 10×20 terrain grid
- max initial terrain level 5
- 8 m × 8 m patch
- stairs 15%
- inverted stairs 15%
- random boxes 30%
- random rough 10%
- slope 10%
- inverted slope 10%
- terrain generator seed: null
- cache: false

`Curriculum/terrain_levels`는 여러 env의 평균 난이도이며 “level 5.4 지형을 완전히 정복했다”는 의미로 쓰면 안 된다.

## 3.5 코드 identity

run 동안 다음 source hash는 before/after 동일했다.

- `train.py`: `36fcd90a...1a358`
- `play.py`: `39be98d4...62617`
- `humanoid_rewards.py`: `35768b8f...21771`
- `_finalize.py`: `734b712f...ea1a`
- `env_cfg.py`: `78927fc5...9adab`
- `agent_cfg.py`: `4e8c9919...72bb6`

따라서 **run 도중 source mutation은 확인되지 않는다.**

프로젝트 기록상 개인 NVIDIA `training/`은 2026-09-13 공식 snapshot과 동기화되어 있으나, 이번 evidence bundle 자체가 공식 snapshot 전체와 byte-for-byte parity manifest를 다시 포함하는 것은 아니다. 따라서 “현재 canonical source와 완전 동일”은 프로젝트 provenance에 의존하는 보조 사실로 두고, 이번 bundle에서 직접 확인된 사실은 위 source hash의 run 전후 불변성이다.

---

# 4. Training Dynamics

## 4.1 Raw TensorBoard coverage

주요 scalar는 각각 **1500 point**, global step `1499..2998`을 연속으로 가진다.

주요 tag:

- `Train/mean_reward`
- `Train/mean_episode_length`
- `Curriculum/terrain_levels`
- `Metrics/base_velocity/error_vel_xy`
- `Metrics/base_velocity/error_vel_yaw`
- termination 2종
- reward component 전부
- value/surrogate/entropy/lr
- policy mean std
- FPS / collection time / learning time

**KL scalar tag는 현재 event에 없다.** 없는 KL을 추정해서 채우지 않는다.

## 4.2 주요 지표 전체 요약

| Metric | 시작 | 최저/최고 | Endpoint | Last-500 mean | Last-100 mean |
|---|---:|---:|---:|---:|---:|
| Terrain | 3.438 | min 3.136 @1516 / max 5.502 @2815 | **5.417** | **5.423** | 5.423 |
| XY error | 0.013* | max 0.410 @1826 | **0.339** | **0.350** | **0.339** |
| Yaw error | 0.017* | max 1.605 @2411 | **1.367** | **1.426** | 1.378 |
| Base-contact | 0.000* | max 32.86% @2060 | **30.39%** | **30.74%** | 30.68% |
| Timeout | 1.37%* | max 73.31% @1540 | **69.63%** | **69.27%** | 69.33% |
| Episode length | 11.5* | max 889.1 @1711 | **741.1** | **764.9** | 763.0 |
| Mean reward | 0.032* | max 6.824 @1545 | **3.906** | **4.001** | 4.212 |
| Action std | 1.344 | max 1.501 @2518 | **1.476** | **1.490** | 1.482 |

`*` 표시가 붙은 resume 직후 episode-derived metric은 통계가 충분히 쌓이기 전의 transient이므로 정책 품질 시작값으로 쓰면 안 된다.

## 4.3 Phase 분석

### Phase A — Resume reset / 통계 재형성: 1499~1598

- terrain 평균 3.485
- terrain 최저 `3.136 @1516`
- XY error/termination/episode statistic이 0 근처에서 빠르게 정상 범위로 올라온다.
- mean reward는 일시적으로 매우 높아져 raw peak `6.824 @1545`가 발생한다.

이 구간은 policy가 갑자기 “완전히 좋아졌다/나빠졌다”기보다 **resume 직후 curriculum 및 episode statistics가 재형성되는 구간**이다.

특히 raw reward peak가 쉬운/reset terrain 구간에 생겼기 때문에, 이 peak만 보고 checkpoint를 고르는 것은 위험하다.

### Phase B — Curriculum rapid recovery: 약 1550~1739

terrain이 다음 순서로 회복한다.

| 기준 | 최초 도달 |
|---|---:|
| resume 시작 terrain 3.438 재돌파 | 1550 |
| terrain 4.0 | 1597 |
| terrain 4.5 | 1639 |
| terrain 5.0 | 1711 |
| parent H-001 1.5K terrain 5.119 재돌파 | **1739** |
| terrain 5.2 | 1764 |

즉 parent 수준의 terrain을 되찾는 데 약 **240 global iterations**가 필요했다.

### Phase C — High-terrain adaptation / yaw degradation: 약 1740~2300

terrain은 5.1~5.25에 머물며 안정화되지만:

- XY error: 대략 0.37→0.36 범위
- yaw error: 약 1.3→1.43 쪽으로 상승
- base-contact: 약 30~32%
- action std: 1.41→1.49 증가

정책이 높은 terrain에 다시 적응하면서 exploration과 gait activity를 유지하는 대신 yaw tracking이 뚜렷한 병목으로 커진다.

### Phase D — Terrain specialization / slow progress: 약 2300~2815

- terrain은 5.3을 2316에서 돌파
- 5.4 최초 돌파는 2521
- 50회 연속 5.4 이상은 2688 이후
- peak terrain `5.502 @2815`

동시에 XY error는 장기적으로 낮아지는 방향이지만 yaw error는 1.4대에 머문다.

이 구간은 **“더 높은 curriculum + linear tracking 미세 개선 + yaw 정체”**의 성격이다.

### Phase E — Late plateau: 2800~2998

- last-500 terrain mean: 5.423
- last-100 terrain mean: 5.423
- last-500 XY error mean: 0.350
- last-100 XY error mean: 0.339
- last-500 yaw error mean: 1.426
- last-100 yaw error mean: 1.378
- base-contact 약 30.7%
- std 1.48~1.49

terrain은 사실상 plateau에 들어갔고, XY는 후반 개선 신호가 있으나 yaw는 여전히 크다.

**중요:** endpoint 하나만 보면 terrain이 peak 5.50→5.42로 “퇴보”한 것처럼 보이지만 last-window가 5.42로 안정적이므로 큰 regression으로 해석할 근거는 없다.

---

# 5. Tracking Analysis

## 5.1 Linear XY tracking

현재 event가 제공하는 tracking metric은 `error_vel_xy` 하나다.

- last-500 mean: **0.3499**
- last-100 mean: **0.3394**
- endpoint: **0.3394**
- post-reset 1700~1899 mean: 약 **0.3729**
- late 2700~2998 mean: 약 **0.3473**

후반으로 갈수록 XY tracking error가 약 `0.373 → 0.347` 방향으로 내려간다. 내부 trajectory만 보면 linear tracking은 개선되는 쪽이다.

그러나 이 지표는 XY 합산이며 다음을 분리하지 못한다.

- forward x tracking
- lateral y tracking

따라서 “전진은 좋아졌지만 좌우는 나빠졌다” 같은 세부 결론은 현재 자료로 낼 수 없다.

## 5.2 Parent 대비 linear 개선 여부

parent H-001에 대해 현재 bundle에서 직접 비교 가능한 확정 수치는:

- terrain 5.119
- base-contact 32.41%

이지만 **H-001 1.5K의 동일 XY-error last-window/raw curve가 이번 bundle에 없다.**

따라서 다음 문장은 가능하다.

> H-008 후반 XY error가 0.34~0.35 수준까지 낮아졌다.

하지만 다음 문장은 아직 불가능하다.

> `track_lin_vel_xy_exp=0.75` 때문에 H-001보다 XY tracking이 X% 개선되었다.

추가 1.5K 학습 자체의 효과와 reward weight 변경의 효과가 분리되지 않았기 때문이다.

## 5.3 Yaw / turning

Yaw는 이번 run의 가장 뚜렷한 약점이다.

- 1700~1899 mean: `1.308`
- 2100~2399 mean: `1.433`
- 2700~2998 mean: `1.411`
- last-500 mean: **1.426**
- endpoint: **1.367**
- max: `1.605 @2411`

후반 terrain 및 XY가 개선되는 동안 yaw error는 초기 post-reset보다 높아졌다.

이것은 **linear tracking reward 강화가 정책 capacity/행동을 선형 이동 쪽으로 재배분하면서 turning이 상대적으로 희생됐을 가능성**과 일치한다.

다만 단일 branch 시계열의 상관은 인과가 아니다. 같은 parent에서 `track_lin=0.5` control resume가 필요하다.

참고로 과거 공식 TERM50 5K endpoint yaw error는 `0.935`였고 current H-008은 `1.367`이다. 하지만 공식 RTX 5080 run과 현재 PERSONAL L40S resume branch는 조건·학습 길이·curriculum history가 다르므로 **직접 인과 비교는 금지**한다. 그럼에도 current yaw `1.3~1.4`대는 절대적으로 다음 evaluator에서 반드시 확인해야 할 병목 신호다.

## 5.4 Stop behavior

설정상 `rel_standing_envs=0.02`로 standing command 노출은 존재한다.

하지만 다음 자료가 없다.

- zero-command drift
- stop 이후 위치/속도 시계열
- stop→go 고정 command evaluator
- 영상에 command sequence annotation

따라서 **stop behavior는 판단 불가**다.

---

# 6. Stability Analysis

## 6.1 Fall / termination

- endpoint base-contact: **30.39%**
- last-500: **30.74%**
- timeout last-500: **69.27%**
- parent H-001 1.5K known base-contact: **32.41%**

현재 branch는 parent 대비 fall-related termination을 눈에 띄게 악화시키지 않았다. 방향상 약 1.7~2.0 percentage point 낮다.

그러나 parent와 current는 **같은 순간의 curriculum 난이도**가 아니다. 특히 current는 resume reset 뒤 다시 5.4까지 올라갔다. 그러므로 32.41→30.74를 순수 stability improvement %로 계산하면 과대해석이다.

안전한 결론은:

> `track_lin=0.75` branch가 추가 1.5K 동안 stability를 붕괴시키지는 않았고, 높은 terrain으로 복귀한 뒤에도 약 30% base-contact termination 수준을 유지했다.

## 6.2 Episode length

- last-500 mean: 764.9 steps
- last-500 median: 766.8
- max: 889.1 @1711
- endpoint: 741.1

20초 episode horizon과 control dt 0.02 s를 고려하면 최대 1000 step이 timeout에 해당한다.

episode length는 후반 760대에 머문다. 긴 생존과 base-contact 약 30%가 서로 일관되며, “거의 전부 timeout”인 survival-only local optimum은 아니다.

## 6.3 Terrain

parent 알려진 1.5K terrain: **5.119**\
current last-500: **5.423**\
current peak: **5.502**\
current endpoint: **5.417**

추가 학습 이후 curriculum capability는 방향상 parent보다 높다.

하지만 이 개선은 다음 두 효과가 섞인다.

1. `track_lin 0.5 → 0.75`
2. 추가 1.5K training

따라서 reward의 단독 효과로 쓰지 않는다.

## 6.4 Gait / posture / smoothness

후반 reward component:

- `action_rate_l2` last-500 ≈ `-0.0745`
- `ang_vel_xy_l2` ≈ `-0.0252`
- `flat_orientation_l2` ≈ `-0.0126`
- `feet_slide` ≈ `-0.0509`
- `feet_air_time` ≈ `+0.00636`

post-reset 1700~1899와 late 2700~2998을 비교하면:

- feet-air reward는 `0.00473 → 0.00652`로 증가
- action-rate penalty magnitude는 `0.0693 → 0.0748`로 증가
- dof-acc penalty magnitude도 약간 증가
- flat-orientation penalty는 비슷
- feet-slide는 후반 약간 완화

즉 높은 terrain에서 정책이 **조금 더 적극적인 leg cycling/air phase를 사용**하는 정황이 있다. 동시에 자세 penalty가 폭발하지 않고 base-contact도 유지되므로 단순한 난폭화나 hopping으로 볼 근거는 없다.

## 6.5 Recovery / push

push recovery 전용 evaluator나 perturbation 결과는 없다. 현재 video도 push test가 아니다.

**판단 불가.**

---

# 7. Reward Component Analysis

## 7.1 `track_lin_vel_xy_exp`

weight 자체가 0.5→0.75로 바뀌었으므로 component 값 절댓값을 parent와 성능비처럼 비교하면 안 된다.

current last-500 component mean은 약 `+0.4668`이다.

실제 tracking quality 판단에는 reward component보다 **`error_vel_xy`를 우선**한다.

## 7.2 `track_ang_vel_z_exp`

weight는 0.5로 고정되어 있다.

- post-reset 1700~1899 mean: +0.1237
- mid 2100~2399: +0.1126
- late 2700~2998: +0.1144

yaw error 증가와 함께 yaw reward가 낮아지는 방향이어서 서로 정합적이다.

## 7.3 Stability 관련 reward

termination penalty weight는 -50로 고정되어 있으며 component는 후반 약 `-0.0206` 수준이다.

단순히 termination reward component가 작은 것만 보고 fall이 거의 없다고 해석하면 안 된다. 실제 termination frequency는 base-contact 약 30.7%다.

## 7.4 Trade-off 구조

이번 run에서 가장 중요한 내부 trade-off는:

```text
terrain progression ↑
XY error ↓
feet-air/activity ↑
    ↕
yaw error ↑
action variation 약간 ↑
```

반면:

```text
base-contact termination ≈ 유지
orientation penalty ≈ 유지
```

이므로 현재 evidence는 **“속도 추종을 얻자마자 안정성이 무너졌다”**보다\
**“선형 이동과 terrain 적응은 유지/개선됐으나 yaw가 비용을 치렀다”** 쪽에 더 가깝다.

---

# 8. PPO / Numerical Stability

## 8.1 Value loss

전체 1500 point:

- median: **0.006810**
- p90: 0.007530
- p95: **0.007731**
- p99: **0.008140**
- p99.5: 0.008457
- max: **0.016809 @1519**

threshold count:

- `>=0.01`: 3회
- `>=0.012`: 2회
- `>=0.015`: 2회
- `>=0.1`: **0회**
- `>=1`: **0회**
- `>=10`: **0회**

큰 spike가 반복되거나 이어지는 패턴이 없다.

특히 과거 Go2 장기 run처럼 value loss가 수십~수백으로 폭증하는 수치 불안정과는 전혀 다른 상태다.

## 8.2 Surrogate / entropy / LR

- surrogate는 후반 약 `-0.013~ -0.014`
- entropy는 후반 약 `26.6~26.9`
- adaptive LR은 `1.2e-5 ~ 2.96e-4` 범위에서 조정
- event에 KL tag 없음

optimizer instability를 의심할 징후는 현재 scalar에서 보이지 않는다.

## 8.3 Action std

TensorBoard mean std:

- start: 1.344
- max: 1.501 @2518
- last-500: 1.490
- endpoint: 1.476

checkpoint 내부 19 action dimension을 직접 보면 std가 균일하게 1.48인 것이 아니다.

예를 들어 final `model_2998`:

- min ≈ 0.193
- max ≈ 2.548
- 일부 joint dimensions는 0.2~0.5
- 일부는 2.3~2.5

즉 mean std 하나는 heterogeneous action distribution을 압축한 값이다.

보고서의 “std가 1.0 근처 → 거의 학습 안 됨” 같은 일반 경고를 그대로 정책 실패 판정으로 사용하면 안 된다. 실제 video locomotion과 terrain progression이 존재하고, 모든 checkpoint tensor도 finite다.

## 8.4 Checkpoint tensor health

보존된 16개 checkpoint:

```text
model_1500
model_1600
...
model_2900
model_2998
```

모두 actor/critic/optimizer 포함 recursive finite check를 통과했다.

**NaN/Inf checkpoint 없음.**

## 8.5 Throughput / GPU

TensorBoard:

- FPS mean: ~123,319
- FPS median: ~124,707
- last-100 mean: ~127,859
- collection time mean: 0.714 s
- learning time mean: 0.085 s

iteration processing에서 collection이 약 **89%**, learning이 약 11%다.

PERSONAL L40S GPU telemetry의 active-training 구간:

- utilization mean ≈ 53%
- VRAM ≈ 5,236 MiB
- power mean ≈ 162 W
- temperature median ≈ 50°C
- max temp 52°C

VRAM이나 온도 한계에 막힌 증거는 없다. GPU utilization 53%만으로 CPU bottleneck을 확정할 수는 없지만, 적어도 GPU memory saturation은 아니다.

---

# 9. Checkpoint Analysis

## 9.1 자동 `model_best`의 정체

`collected/exported/model_best.pt` SHA-256:

`5bf677674327e417e869a37c1e9ff86d62a5f38b47135ed99cbb06341a4e8824`

이 hash는 정확히:

`checkpoints/model_1700.pt`

와 일치한다.

즉 **model_best = model_1700**이다.

## 9.2 Raw TensorBoard vs report 불일치

Full raw event:

- raw mean reward max = **6.824 @1545**

`report.html` / finalize:

- reported best = **5.683 @1711**
- selected checkpoint = `model_1700.pt`

이 차이는 실제로 존재한다.

제공 evidence만으로는 왜 1545가 finalize selection에서 제외됐는지 확정할 수 없다. 가능한 원인 후보는 finalize의 event read/selection logic, resume handling, sampling/filtering이지만 **검증 없이 특정 원인을 단정하지 않는다.**

더 중요한 사실은 raw 1545 peak 자체도 resume-reset 쉬운 terrain 구간(`terrain≈3.37`)에서 생겼다는 것이다. 따라서 raw 1545를 무조건 “진짜 best”로 바꾸는 것도 올바른 해결은 아니다.

## 9.3 후보 checkpoint 역할

| 후보 | 역할 | 근처 scalar |
|---|---|---|
| `model_1500/1600` | resume transient raw reward peak 주변 | terrain 아직 낮음 |
| **`model_1700`** | report 자동 best / 현재 video source | terrain~4.95, XY~0.382, yaw~1.264 |
| `model_2800` | terrain peak 2815 인접 | terrain 5.50 부근 |
| `model_2900` | late mature candidate | terrain 5.422, XY 0.347, yaw 1.428 |
| **`model_2998`** | final | terrain 5.417, XY 0.339, yaw 1.367 |

현재 `model_1700`을 “최적 정책”으로 자동 확정할 근거는 부족하다.

특히 final/late 정책은:

- terrain이 더 높고
- XY tracking error가 더 낮다.

반면 yaw는 여전히 나쁘므로 실제 evaluator가 필요하다.

## 9.4 현재 가장 중요한 checkpoint gap

**Video는 `model_1700`만 검증했다.**

`model_2800`, `model_2900`, `model_2998`에 대한:

- 같은 command sequence
- 같은 terrain
- 같은 seed
- 동일 camera
- quantitative evaluator

가 없다.

따라서 이번 run에서 “학습 reward 최고”, “terrain 최고”, “linear tracking 최고”, “실제 제출 후보”는 서로 같은 checkpoint라고 볼 수 없다.

---

# 10. Video / Behavioral Analysis

## 10.1 Video provenance

Video source checkpoint:

- source: train run `model_best.pt`
- SHA-256: `5bf67767...a4e8824`
- = `model_1700.pt`

Video:

- SHA-256: `ed6566a0ec7c8d267d4a1e0ef6813d301c3aa282c0fce493f288d77befd15074`
- H.264
- 1920×1080
- 50 fps
- 999 frames
- 19.98 s
- 1 env
- evidence validation PASS

새 policy도 video 실행에서 export되었다.

- `policy.pt`: `c5609c191a4d3e946a0b765b516c3470dac1c296421beab72cc558a327041db9`
- `policy.onnx`: `83fdf88a...a85a65`

## 10.2 직접 행동 관찰

20초 contact-sheet 및 keyframe을 직접 확인한 결과:

### 확인됨

- 전 구간에서 upright posture 유지
- 명백한 낙상 없음
- 이동 자체를 거부하는 stationary survival 정책 아님
- 양발을 교대로 사용하는 보행이 보임
- 지속적인 one-leg hopping은 보이지 않음
- 옆으로 누워 termination만 회피하는 형태 아님
- 과도한 점프/공중 체류 없음
- 크게 무너지는 torso oscillation은 보이지 않음

### 관찰되는 성격

- 몸통과 팔이 보행 중 다소 적극적으로 움직임
- 일부 구간에서 lateral/turning 성분이 섞인 보행이 보임
- 자세가 완전히 경직된 survival-only gait는 아님

### 확인 불가

- 정확한 command 대비 forward tracking error
- lateral tracking을 forward와 분리한 성능
- yaw tracking 수치
- zero-command stop drift
- push recovery
- stairs/boxes 통과 성공률
- slope up/down 성공률

영상에는 주변에 terrain patch가 보이지만, 이 20초 sample만으로 특정 장애물의 진입→통과→회복을 정량적으로 검증할 수 없다. **terrain level 5.4의 시각적 검증 영상으로 사용하면 안 된다.**

## 10.3 숫자와 영상의 일치/충돌

일치:

- base-contact 약 30%라고 해서 즉시 쓰러지는 정책은 아님
- gait는 실제로 존재함
- hopping reward hacking은 보이지 않음
- high std에도 locomotion은 가능함

충돌/주의:

- late scalars는 더 높은 terrain/낮은 XY error를 보이지만 영상 source는 early `model_1700`
- 따라서 영상으로 late-policy 개선을 검증할 수 없음

---

# 11. Baseline / Parent Comparison

## 11.1 가장 직접적인 parent 비교

Parent H-001 1.5K의 프로젝트에 보존된 비교 가능 수치:

| Metric | H-001 parent 1.5K | H-008 current |
|---|---:|---:|
| terrain | 5.119 | endpoint 5.417 / last500 5.423 |
| base-contact | 32.41% | endpoint 30.39% / last500 30.74% |
| `track_lin` weight | 0.50 | **0.75** |
| termination weight | -50 | -50 |

이 두 stability/curriculum 지표만 보면 current가 parent보다 나쁘지 않다.

그러나 current는 parent에서 **추가 1.5K를 더 학습**했으므로:

```text
H-001 1.5K endpoint
vs
H-008 cumulative ~3K lineage
```

는 reward-only paired comparison이 아니다.

## 11.2 공식 TERM50 5K contextual comparison

과거 OFFICIAL TERM50 5K endpoint:

- terrain 5.825
- base-contact 28.93%
- timeout 71.07%
- XY error 0.378
- yaw error 0.935
- std 1.296

Current H-008 endpoint:

- terrain 5.417
- base-contact 30.39%
- timeout 69.63%
- XY error 0.339
- yaw error 1.367
- std 1.476

형태만 보면 current는:

- XY error는 낮음
- yaw는 크게 나쁨
- terrain/stability는 OFFICIAL 5K보다 약간 낮음
- std는 높음

하지만 이것은 **PERSONAL L40S resume 3K lineage vs OFFICIAL RTX5080 fresh/long 5K**이므로 직접 성능 우열이나 reward 인과로 쓰지 않는다.

## 11.3 Personal long-run TERM50 contextual comparison

과거 PERSONAL TERM50 25K endpoint:

- terrain 5.876
- base-contact 21.43%
- XY 0.372
- yaw 0.803

장기 학습에서는 stability와 yaw가 더 좋아질 여지가 있었음을 보여주지만, 25K와 이번 3K lineage를 동일 학습량 비교로 쓸 수 없다.

## 11.4 비교의 결론

확실한 것:

- H-008은 parent에서 stability를 즉시 파괴하지 않았다.
- resume reset 후 parent terrain 수준을 회복하고 더 올라갔다.
- current 후반 XY error는 0.34~0.35 수준이다.
- yaw는 현재 병목이다.

판단 불가:

- `0.75`가 `0.5` control보다 XY를 얼마나 개선했는지
- 같은 추가 학습량에서 stability를 얼마나 희생/개선했는지

---

# 12. Tracking vs Stability Trade-off

요청한 네 범주 중 하나로 억지로 단순화하기 어렵다.

## Tracking

- Linear XY: **후반 개선 방향**
- Forward vs lateral: **분리 불가**
- Yaw: **악화/병목**
- Stop: **판단 불가**

## Stability

- Base-contact: **유지 또는 소폭 개선 방향**
- Terrain: **resume reset 후 parent 이상으로 회복**
- Episode length: **후반 약 765**
- Recovery: **판단 불가**
- Gait: **video에서 정상적인 locomotion 확인**
- Smoothness: 큰 붕괴는 없지만 action-rate 활동량은 다소 증가

따라서 가장 정확한 표현은:

> **Linear Tracking ↑ 가능성 / Yaw Tracking ↓ / Stability ≈ 유지~소폭 ↑**

즉 “Tracking ↑ / Stability ↓”라는 단순 trade-off는 현재 자료와 맞지 않는다. tracking 자체가 linear와 yaw에서 서로 갈라졌다.

---

# 13. Local Optimum / Reward Hacking Check

## 움직이지 않고 생존

**증거 없음.** video에서 지속 이동하며 curriculum도 상승한다.

## 비정상 자세로 termination 회피

**증거 없음.** upright gait를 유지한다.

## hopping / 한 발 오래 들기

**명백한 증거 없음.** 2 fps contact-sheet에서도 교대 보행 패턴이다.

## sliding

reward term `feet_slide` penalty는 존재하지만, video 해상도/시점만으로 정확한 foot slip을 정량 판정하기 어렵다.

## command 무시

완전한 command 무시는 아님을 시사하지만, command telemetry가 video와 동기화되어 있지 않아 정량 검증 불가.

## terrain 회피

표준 play 영상에서 실제 obstacle traversal을 강제하지 않았으므로 **배제할 수 없음.**

## 지나친 소극성

video상 stationary/소극 survival은 아니다.

### 종합

명백한 reward hacking/local optimum 신호는 **낮음**.\
다만 fixed-command/fixed-terrain evaluator가 없어 task 목적 수행을 완전히 검증했다고 할 수 없다.

---

# 14. Key Findings

중요도 순으로 다음이 이번 의사결정에 가장 큰 영향을 준다.

1. **이번 실험의 실제 parent delta는 `track_lin_vel_xy_exp 0.5→0.75` 하나뿐이다.** report가 `termination -5→-50`도 변경으로 표시하는 것은 배포 baseline 대비 설명이지 H-001 parent 대비 experiment delta가 아니다.

2. **resume curriculum reset은 매우 크지만 빠르게 회복됐다.** terrain은 3.136까지 내려간 뒤 iter 1739에 parent terrain 5.119를 재돌파하고 last-500 5.423에 도달했다. 따라서 early terrain 하락만으로 실패 판정했으면 잘못된 결론이었을 것이다.

3. **stability sacrifice는 현재 evidence에서 크지 않다.** last-500 base-contact 30.74%로 parent known 32.41%보다 방향상 나쁘지 않고, video도 upright locomotion을 보인다.

4. **linear XY는 후반 좋아지지만 yaw가 명확한 병목이다.** post-reset 평균 XY 약 0.373→late 0.347로 내려가는 동안 yaw는 약 1.31→1.41대로 커졌다.

5. **자동 `model_best`는 현재 task 관점 best라고 보기 어렵다.** model_best/video는 model_1700인데, late `model_2800/2900/2998`은 terrain이 더 높고 XY error가 낮다.

6. **raw TensorBoard best와 report best가 불일치한다.** raw `6.824 @1545`, report `5.683 @1711`. 원인은 미확정이며 selection logic을 맹신하면 안 된다.

7. **수치 불안정은 이번 run의 병목이 아니다.** value loss p99 0.00814, max 0.0168, NaN/Inf 없음, 모든 16 checkpoint finite.

8. **현재 가장 큰 scientific limitation은 control 부재다.** H-008 개선이 reward 변경 때문인지 단순히 parent를 1.5K 더 학습해서인지 분리할 수 없다.

---

## 새로운 발견

### A. “Best checkpoint”가 오히려 early post-reset 정책일 가능성

model_1700은 curriculum이 parent 수준으로 막 복귀하는 시점의 checkpoint다. terrain peak는 2815이고, final XY는 1700보다 낮다.

따라서 현재 자동 selection은 **resume 이후 mature policy보다 일시적인 reward peak를 선호했을 가능성**이 있다.

이것은 원인 가설이지 finalize bug 확정은 아니다.

### B. Linear tracking 강화의 비용이 fall보다 yaw에서 먼저 나타났을 가능성

일반적으로 속도 보상을 올리면 “더 넘어질 것”을 먼저 걱정할 수 있지만, current data에서는 base-contact가 크게 악화되지 않았다.

대신 yaw error가 커졌다.

즉 현재 H1에서는 다음 trade-off가 더 실질적일 수 있다.

```text
linear progress
vs
turning authority / heading tracking
```

다음 실험에서는 fall만 보지 말고 yaw를 동등한 primary endpoint로 둬야 한다.

### C. Action std 경고는 이 정책에서 misleading 가능성이 큼

std는 1.48로 높지만:

- terrain 5.4 유지
- base-contact 약 30%
- video locomotion 정상
- value loss 안정
- checkpoint finite

이므로 std 하나를 기준으로 “거의 학습 안 됨”이라고 버리는 것은 현재 evidence와 맞지 않는다.

---

# 15. Final Decision

## **HOLD**

### HOLD 이유

**PROMOTE까지 못 가는 이유**

1. PERSONAL run이므로 공식 성능 증거가 아님.
2. same-parent control resume가 없어 reward change의 인과 효과를 분리할 수 없음.
3. forward/lateral tracking이 XY aggregate로만 기록됨.
4. yaw error가 1.4 전후로 커서 중요한 trade-off가 남아 있음.
5. video는 final이 아니라 model_1700만 검증함.
6. evaluator / multi-seed / fixed command / terrain-specific 결과가 없음.

**REJECT하지 않는 이유**

1. 학습과 evidence가 정상 완료됨.
2. terrain은 parent 수준을 회복하고 더 올라감.
3. base-contact stability가 붕괴하지 않음.
4. late XY tracking은 개선 방향.
5. video에 명백한 hopping, stationary survival, 비정상 자세, 낙상이 없음.
6. numerical instability 없음.

따라서 가설은 **가능성이 있으나 causal evidence가 한 단계 부족한 상태**다.

---

# 16. Next Experiment

## 16.1 학습을 더 하기 전에 가장 먼저 할 무료/저비용 검증

새 training 전에 현재 보존 checkpoint를 동일 evaluator에서 비교하는 것이 우선이다.

최소 후보:

```text
model_1700  # auto-best / 현재 video
model_2800  # terrain peak 근처
model_2900  # late mature
model_2998  # final
```

같은 seed·command sequence·terrain으로:

- forward
- lateral
- yaw
- stop
- rough
- boxes
- stairs
- slopes
- push/recovery

를 비교한다.

특히 current video는 1700만 있으므로 **2998 video/evaluator를 먼저 만들어야 late-policy에 대한 행동 결론을 낼 수 있다.**

이 단계는 새 학습이 아니므로 가장 비용 효율적인 immediate action이다.

---

## 16.2 다음 “한 번의 학습”으로 가장 많은 정보를 얻는 실험

### 제안: **H-001 same-parent resume CONTROL**

Parent:

```text
H001_PARENT_1P5K_LOCKED/model_1499.pt
SHA-256:
68fa0a9fe5334f8a3ecea110c4ccc9adb81ec07ac50169eaf8009b1a6e88f0c1
```

Control reward:

```text
track_lin_vel_xy_exp = 0.50  # parent 그대로
termination_penalty = -50
나머지 reward = parent 그대로
```

고정:

- PERSONAL 동일 environment
- seed 42
- 4096 envs
- additional 1500 iterations
- 같은 PPO
- 같은 terrain
- 같은 command ranges
- 같은 headless 조건
- 같은 evidence wrapper
- 같은 checkpoint save interval

### 왜 `0.75→1.0`이 아니라 control인가?

지금 H-008만으로는 다음 두 가설을 분리할 수 없다.

```text
A. track_lin 0.75 때문에 좋아졌다.
B. H-001을 그냥 1.5K 더 학습해서 좋아졌다.
```

`1.0`을 또 돌리면 세 번째 혼합 결과가 추가될 뿐, A/B가 계속 분리되지 않는다.

동일 parent `0.5` control 한 번이면 H-008과 거의 paired branch가 되어 reward effect를 훨씬 직접적으로 볼 수 있다.

### 비교 창

resume transient를 primary comparison에서 분리한다.

H-008에서 parent terrain 5.119 재돌파가 global 1739였으므로:

- reset/adaptation: first ~200~250 additional iterations
- primary trajectory: 그 이후
- primary endpoint: **last 500**
- secondary: last 100 / endpoint
- change-point 및 recovery speed 별도 기록

### 사전 성공 기준 제안

아래 threshold는 공식 기준이 아니라 **실험 전 decision rule**로 제안한다.

H-008 `0.75`가 control `0.5` 대비:

1. **XY error last-500이 최소 0.02 m/s 이상 낮고**
2. terrain last-500이 control보다 `0.15 level` 이상 나빠지지 않고
3. base-contact가 `+2 percentage point` 이상 악화되지 않고
4. yaw error가 `+0.10 rad/s` 이상 악화되지 않으며
5. fixed evaluator에서 forward/lateral 개선이 실제 displacement/tracking으로 확인되면

`0.75` 가설을 **PROMOTE 후보**로 올린다.

반대로:

- XY 개선 거의 없음 + yaw 악화
- terrain/fall 악화
- 영상에서 gait aggressive/oscillatory
- stop drift 증가

가 나오면 `0.75`는 **REJECT 또는 더 낮은 0.6~0.65 intermediate anchor**가 적절하다.

### 2순위 후속

control에서 `0.75`의 효과가 확인된 뒤에만:

```text
track_lin_vel_xy_exp = 1.0
```

같은 parent 또는 검증된 common checkpoint에서 추가 dose-response를 본다.

---

# 17. Confidence & Limitations

## 강한 근거

- PERSONAL / resume identity
- parent checkpoint path + SHA
- actual command
- seed / env / rollout / PPO
- actual reward weights
- parent 대비 변경 reward가 사실상 1개라는 점
- TensorBoard 1499~2998 full scalar
- terrain reset/recovery timing
- current XY/yaw/base-contact/episode curves
- value-loss distribution
- no NaN/Inf
- 16 checkpoint finite
- model_best=model_1700 hash identity
- video source=model_1700 hash identity
- 19.98s video codec/frame count
- video에서 명백한 낙상/hopping/stationary-local-optimum이 보이지 않는 점

## 중간 근거

- linear tracking이 late phase에서 실제로 개선되는 방향
- stability가 parent 대비 유지되거나 약간 좋아졌다는 방향성
- yaw가 linear tracking 강화와 trade-off일 가능성
- action activity 증가가 terrain adaptation과 함께 나타난다는 해석

## 약한 정황 / 가설

- `track_lin 0.75`가 yaw 악화의 직접 원인
- auto-best selection이 resume transient에 구조적으로 편향되었다는 원인 설명
- 높은 std가 특정 joint exploration을 의도적으로 유지한 결과라는 해석

## 판단 불가

- forward와 lateral 각각의 성능
- stop drift
- push recovery
- terrain별 성공률
- current policy의 공식 시나리오 점수
- multi-seed 일반화
- `0.75`의 causal effect size
- model_2998의 실제 영상 행동
- official submit-ready 여부

---

# 18. 최종 질문 8개에 대한 답

## 1. 이 정책은 무엇을 배웠는가?

parent TERM50의 안정 보행을 잃지 않은 채 resume reset 후 높은 terrain으로 다시 올라가며 **선형 XY 이동을 유지/미세 개선하는 locomotion**을 학습했다. 그러나 turning/yaw tracking은 충분히 따라오지 못했다.

## 2. 이전 정책보다 무엇이 실제로 좋아졌는가?

확실하게 말할 수 있는 것은 terrain/base-contact 방향성이다. parent known terrain 5.119에서 current last-500 5.423까지 올라갔고, base-contact도 32.41%에서 current 약 30.74% 수준이다.

다만 이것이 reward `0.75` 때문인지 추가 training 때문인지는 아직 분리되지 않았다.

## 3. 무엇을 잃었는가?

가장 강한 손실 후보는 **yaw/turning tracking**이다. current late yaw error는 약 1.4다.

## 4. 학습 중 언제 중요한 변화가 일어났는가?

- 1499~1516: curriculum reset/최저점
- ~1550: 시작 terrain 회복
- 1711: terrain 5.0 + report reward peak
- 1739: parent terrain 5.119 재돌파
- ~2300: terrain 5.3 구간 진입
- 2688 이후: 5.4 수준을 지속
- 2815: terrain peak 5.502
- 후반: terrain plateau + XY 미세 개선 + yaw 병목 지속

## 5. 높은 지표가 실제 행동 개선을 의미하는가?

항상 그렇지 않다. 현재 가장 높은 raw reward는 reset 초기 1545에서 나왔고, 자동 best도 1700이다. 후반 checkpoint가 terrain/XY에서는 더 좋다. 따라서 training reward peak와 실제 task-best는 분리해야 한다.

## 6. 현재 가장 큰 병목은 무엇인가?

**Yaw/turning + checkpoint selection uncertainty.**

## 7. 이 가설은 계속 실험할 가치가 있는가?

**있다. HOLD.** Stability collapse가 없고 linear metric은 유망하지만 control이 없어 아직 승격할 수 없다.

## 8. 다음 한 번의 학습으로 가장 많은 정보를 얻으려면?

**같은 H-001 model_1499에서 track_lin=0.5를 유지한 1.5K resume control을 실행한다.**

이 한 번이 H-008의 효과와 “그냥 1.5K 더 학습한 효과”를 분리한다.

---

# 19. Evidence / Provenance Index

## Train bundle

`20260917-004530-h1-h008-lintrack075-from-h001-1p5k.tar.gz`

SHA-256:

`06f7d1dad5b492e701587009f46811e8aa8e7a4504fba4d92f763db6b7c388b5`

주요 원본:

- `metadata.json`
- `validation.json`
- `command.txt`
- `console.log`
- `SHA256SUMS`
- `source/humanoid_rewards.py`
- `source/identity.json`
- `native_run/events.out.tfevents...`
- `native_run/params/env.yaml`
- `native_run/params/agent.yaml`
- `checkpoints/model_1500.pt ... model_2998.pt`
- `collected/exported/model_best.pt`
- `collected/exported/env.yaml`
- `collected/exported/report.html`
- `system/nvidia_smi_during.csv`

Event SHA-256:

`6a658d1ad742c02bf0f4fc83e068e50bf4960ecff493451dfd0a012b11026e8c`

Final checkpoint:

`model_2998.pt`\
SHA-256: `d9a30c8a117f69cac49c4e640500f0fa8d88de72d6c61855f1e147ea6c1912ae`

Auto-selected model_best:

`model_1700.pt`\
SHA-256: `5bf677674327e417e869a37c1e9ff86d62a5f38b47135ed99cbb06341a4e8824`

## Video bundle

`20260917-010854-20260917-004530-h1-h008-lintrack075-from-h001-1p.tar.gz`

SHA-256:

`d78257b8bc2cb5352b1674c31fc04d961fc854f17a41fff512f5b4bb2e57dde6`

Source checkpoint:

`model_best.pt = model_1700.pt`\
SHA-256: `5bf67767...a4e8824`

Play video:

SHA-256: `ed6566a0ec7c8d267d4a1e0ef6813d301c3aa282c0fce493f288d77befd15074`

Policy:

SHA-256: `c5609c191a4d3e946a0b765b516c3470dac1c296421beab72cc558a327041db9`

## Project comparison sources used

- `00_START_HERE_CONTEXT_AND_MAP(20260916-234815).md`
- `06_HUMANOID_TRAINING_CODE(20260916-152653).md`
- `13_H1_OFFICIAL_SERVER_BASELINE_EVIDENCE(20260915-042342).md`
- `14_H1_NEXT_RUN_PARAMETER_COMPARISON(20260916-234814).md`
- `15_OPTUNA_REWARD_DECISION_ENGINE(20260916-234815).md`
- `16_EXPERIMENT_EXPORT_AND_TENSORBOARD(20260916-092146).md`
- `17_H1_PERSONAL_SERVER_LONG_RUN_EVIDENCE(8).md`
- `18_H1_FINALIZE_REPORT_LIMITATIONS(9).md`
- `19_ISSACSIMZ_EXTERNAL_EVIDENCE_CLI(20260916-092146).md`

이 과거 문서의 숫자는 current run 원본과 섞지 않고 **parent/context comparison**에만 사용했다.

---

# 최종 한 줄

**H-008은 “linear tracking을 더 세게 주면 stability가 무너진다”는 실패가 아니라, stability는 대체로 유지하면서 XY는 유망해졌지만 yaw와 checkpoint selection 문제가 새 병목으로 드러난 run이다. 그러나 reward 효과를 확정하려면 동일 H-001 parent에서 `track_lin=0.5` control resume가 반드시 필요하다.**
