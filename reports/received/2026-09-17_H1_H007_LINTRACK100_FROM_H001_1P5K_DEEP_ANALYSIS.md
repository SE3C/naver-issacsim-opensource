> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/incoming/other/reviewed/2026-09-17_H1_H007_LINTRACK100_FROM_H001_1P5K_DEEP_ANALYSIS.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# H1 H-007 LINTRACK100 from H-001 1.5K — Deep Analysis

- 분석 대상: `20260917-002225-h1-h007-lintrack100-from-h001-1p5k`
- Robot: H1 humanoid
- 환경 분류: **PERSONAL**
- 실험 형태: **H-001 1.5K checkpoint에서 resume/fine-tuning**
- 핵심 변경: parent H-001 대비 `track_lin_vel_xy_exp: 0.5 → 1.0` 단일 변경
- 분석 작성일: 2026-09-17
- 최종 판정: **HOLD**

> **해석 표기**
> - **확인됨**: 원본 archive/hash/metadata/TensorBoard/console/checkpoint/video에서 직접 검증.
> - **강한 정황**: 복수 독립 지표가 같은 방향을 가리키지만 실험적 인과 분리는 안 됨.
> - **가설**: 다음 실험으로 검증해야 하는 해석.
> - **판단 불가**: 현재 자료에 직접 관측값이 없음.

---

# 1. Executive Summary

이번 H-007은 fresh training이 아니라, H-001 TERM50 계열의 `model_1499.pt`에서 시작해 **1,500 iteration을 추가 fine-tuning한 PERSONAL resume run**이다. 부모 checkpoint SHA-256은 metadata에 `68fa0a9f...8f0c1`로 고정되어 있고, H-007에서 parent 대비 의도적으로 바꾼 reward는 `track_lin_vel_xy_exp 0.5 → 1.0` 하나다. 학습 프로세스는 exit code 0으로 정상 종료했고, TensorBoard·전체 console·16개 checkpoint·env/config·source hash·GPU telemetry가 보존되었으며 내부 `SHA256SUMS`도 전부 일치했다. 따라서 **실행 및 evidence 무결성은 높다**.

정책은 resume 직후 curriculum이 쉬운 쪽으로 내려간 뒤 약 250여 update에 걸쳐 H-001 1.5K 시점의 terrain 수준을 다시 회복했다. 이후 terrain은 약 5.3~5.4에서 안정되었고 base-contact termination도 약 30% 수준을 유지했으므로, `track_lin` 강화 때문에 생존·terrain capability가 즉시 붕괴한 run은 아니다. 동시에 XY velocity error는 후반으로 갈수록 개선되어 last-500 평균 `0.3386`, 마지막 값 `0.3155`, post-warmup 최저 `0.3001`까지 내려갔다.

그러나 이 개선에는 분명한 대가가 있었다. yaw error는 early-adapt 평균 `1.337`에서 후반 약 `2.0`으로 상승했고, `track_ang_vel_z` reward도 후반에 약화됐다. `action_rate`, `dof_acc`, `feet_slide`, arm-deviation penalty도 후반으로 갈수록 더 나빠져 **정책이 선형 이동에는 더 적극적이지만 회전·동작 매끄러움은 희생하는 방향으로 specialization**한 정황이 강하다. 영상에서도 선택된 `model_1700`은 약 20초 동안 명백한 낙상 없이 직립 보행하지만, 명령/현재 속도 화살표가 항상 일치하지는 않는다. classic reward hacking(제자리 버티기, 누운 채 생존, 한 발 hopping)은 확인되지 않았다.

PPO 수치 안정성은 매우 좋다. value loss는 전체 median `0.00926`, p99 `0.01148`, 최대 `0.0573`이며 최대치는 resume 첫 step이다. step 1550 이후 최대는 `0.01244`에 불과하고 NaN/Inf/OOM/std 오류는 없다. 16개 checkpoint의 actor/critic/optimizer tensor도 모두 finite였다. 따라서 이번 결과의 병목은 optimizer 발산이 아니라 **행동 objective 사이의 trade-off**다.

중요한 provenance 문제도 하나 있다. raw TensorBoard/console의 최고 mean reward는 **iter 1564의 `9.8259`**인데, `report.html`/finalizer는 **iter 1733의 `8.2135`**를 best로 기록하고 `model_1700.pt`를 선택했다. 이 run은 tag당 scalar가 1,500개뿐이라 과거 장기-run의 10,000-event truncation 문제를 그대로 원인으로 단정할 수 없다. 다만 자동 best selection이 raw scalar와 불일치한다는 사실 자체는 확정적이며, `model_best`를 실제 locomotion 최적 정책으로 사용할 근거는 없다.

최종적으로 H-007은 **REJECT할 만큼 실패하지 않았지만 PROMOTE할 만큼 인과가 분리되지도 않았다.** 같은 parent checkpoint에서 reward를 바꾸지 않고 동일하게 +1.5K resume한 control이 없기 때문에, 후반 XY 개선이 `track_lin 1.0` 때문인지 단순 추가 학습 때문인지 분리할 수 없다. 따라서 판정은 **HOLD**가 가장 적절하다. 다음 학습 한 번으로 가장 많은 정보를 얻으려면, exact same H-001 parent에서 `track_lin=0.5`를 유지한 **resume-control +1.5K**를 같은 조건으로 돌려 H-007과 직접 비교해야 한다.

---

# 2. Run Identity & Evidence Integrity

## 2.1 실험 정체성

| 항목 | 확인 결과 | 근거 수준 |
|---|---|---|
| Robot | H1 humanoid | 확인됨 |
| Experiment/Hypothesis | H-007 · LINTRACK100 | 확인됨(이름·프로젝트 계보) |
| Train Run ID | `20260917-002225-h1-h007-lintrack100-from-h001-1p5k` | 확인됨 |
| Environment | **PERSONAL** | 확인됨: `metadata.json mode=personal` |
| Fresh / Resume | **Resume / fine-tuning** | 확인됨 |
| Parent run | `H001_PARENT_1P5K_LOCKED` | 확인됨 |
| Parent checkpoint | `model_1499.pt` | 확인됨 |
| Parent checkpoint SHA-256 | `68fa0a9fe5334f8a3ecea110c4ccc9adb81ec07ac50169eaf8009b1a6e88f0c1` | metadata에서 확인됨 |
| Requested iterations | `1500` additional | 확인됨 |
| Console/TB iteration labels | `1499 ... 2998` (1,500 scalar rows) | 확인됨 |
| Actual last console iteration | `2998` | 확인됨 |
| Actual last saved checkpoint | `model_2998.pt` | 확인됨 |
| Seed | `42` | 확인됨 |
| num_envs | `4096` | 확인됨 |
| rollout steps/env | `24` | 확인됨 |
| transitions/iteration | `98,304` | 계산: 4096×24 |
| additional transitions | `147,456,000` | 계산: 98,304×1,500 |
| Train mode | headless, camera 없음 | command에서 확인 |
| Play mode | headless + cameras + video, 1 env | 확인됨 |
| 학습 시작 | 2026-09-17 09:22:25 KST | metadata UTC→KST |
| 학습 종료 | 2026-09-17 09:42:42 KST | metadata UTC→KST |
| Wrapper elapsed | 약 20분 17.5초 | metadata |
| Native training time | 1,195.98초 ≈ 19분 56초 | console |
| TensorBoard | 존재, raw scalar 추출 가능 | 확인됨 |
| 전체 console | 존재 | 확인됨 |
| mirrored checkpoint | 16개 | 확인됨 |
| play/video | 존재, lineage manifest 포함 | 확인됨 |
| evaluator | 없음 | 판단 불가/미제공 |
| H-007 공식 평가 | 없음 | **없음 — PERSONAL run** |

### PERSONAL/OFFICIAL 구분

`metadata.json` 안에 `official_finalize_status=completed` 및 `resume_lineage.official_resume=true` 같은 필드가 존재하지만, 이 필드는 native finalize/resume 흐름의 상태 표현이다. **실험 환경 분류 자체는 `mode=personal`이 우선**이며, 이번 H-007을 OFFICIAL run으로 승격해서 해석하면 안 된다. 공식 대회 성능 개선이나 공식 점수 향상이라고 표현할 수 없다.

## 2.2 원본 archive 무결성

### Train evidence archive

- 파일: `20260917-002225-h1-h007-lintrack100-from-h001-1p5k.tar.gz`
- 외부 SHA-256: `ebcf43a6e6eccdc93508c75c7e78d4595370c92c8965f47f8215a80b67ae00bb`
- 내부 `SHA256SUMS`: **38/38 일치**
- evidence validation: **PASS**
- source before/after hash: **동일**
- mirrored checkpoints: **16개**

### Play evidence archive

- 파일: `20260917-004341-20260917-002225-h1-h007-lintrack100-from-h001-1p.tar(1).gz`
- 외부 SHA-256: `695e47d77edb85f72f1a326a05d7086bdc198129d65437961596464c0d0b0cb7`
- 내부 `SHA256SUMS`: **20/20 일치**
- evidence validation: **PASS**
- source checkpoint SHA-256: `fcca77192048...dfa94668`
- video SHA-256: `58cdde2cacb13c26f93a8ccfe84203489a18a570f73480aa4a0beac87dd27d91`

## 2.3 네 가지 상태를 분리한 판정

| 질문 | 판정 |
|---|---|
| 1. 학습 프로세스가 정상 종료됐는가? | **YES** — exit 0, completed, 2998까지 완료 |
| 2. Evidence가 정상 보존됐는가? | **YES** — archive checksum, TB, console, checkpoints, config, video lineage PASS |
| 3. 정책 자체가 좋은가? | **부분적** — XY/terrain은 강하지만 yaw/smoothness trade-off 큼 |
| 4. 제출 후보로 적합한가? | **아직 판단 불가 / HOLD** — PERSONAL, fixed evaluator/official score 없음, checkpoint selection 미완 |

Evidence PASS는 “잘 보존된 실행”이라는 뜻이지 “좋은 정책”이라는 뜻이 아니다.

## 2.4 실행 오류/오염 검사

직접 검사한 train/play console에서 다음은 발견되지 않았다.

- NaN / Inf
- CUDA OOM
- broken pipe
- traceback / segmentation fault
- optimizer/std 관련 fatal error
- checkpoint 저장 실패
- finalize 실패
- stale play video 사용

관측된 warning은 headless/display·deprecated API·observation group compatibility·Fabric marker 등 비치명 경고다. 학습 후 `[notify] skip: No module named 'notify'` 메시지가 있지만 optional notification 모듈 부재이며 학습/산출물에는 영향이 없다.

---

# 3. Configuration Verification

## 3.1 실제 학습 명령

```bash
/home/shadeform/IsaacLab/isaaclab.sh \
  -p /ephemeral/naver-issacsim-nvidia/training/humanoid/train.py \
  --task Humanoid-v0 \
  --max_iterations 1500 \
  --num_envs 4096 \
  --resume \
  --load_run H001_PARENT_1P5K_LOCKED \
  --checkpoint model_1499.pt \
  --headless
```

따라서 이 run을 “fresh 1.5K”로 읽으면 안 된다. **H-001 1.5K 시점에서 추가 1.5K fine-tuning한 branch**다.

## 3.2 적용 reward

실제 `source/humanoid_rewards.py`와 `env.yaml`에서 확인되는 핵심 weight는 다음과 같다.

| Reward | H-007 적용값 |
|---|---:|
| `track_lin_vel_xy_exp` | **+1.00** |
| `track_ang_vel_z_exp` | +0.50 |
| `feet_air_time` | +0.20 |
| `termination_penalty` | **-50.0** |
| `flat_orientation_l2` | -1.50 |
| `ang_vel_xy_l2` | -0.05 |
| `joint_deviation_hip` | -0.20 |
| `joint_deviation_torso` | -0.10 |
| `action_rate_l2` | -0.0005 |

환경에 기본적으로 활성화된 항목까지 포함하면 `dof_acc_l2`, `dof_pos_limits`, `feet_slide`, `joint_deviation_arms` 등도 실제 reward 합산에 참여한다. 총 manager reward term은 14개이며, `dof_torques_l2=0`을 제외하면 13개가 nonzero다.

## 3.3 “baseline 대비 변경 2개”와 “parent 대비 변경 1개”를 구분해야 함

`report.html`은 원래 배포 default와 비교하여 다음 두 변화를 표시한다.

- `track_lin_vel_xy_exp: 0.5 → 1.0`
- `termination_penalty: -5 → -50`

하지만 H-007의 실제 parent는 이미 TERM50인 H-001이다. 따라서 **이번 branch에서 새로 바뀐 causal delta는 `track_lin_vel_xy_exp` 하나**다. `termination_penalty=-50`은 H-007에서 새로 바꾼 변수가 아니라 parent로부터 상속된 stability anchor다.

즉:

```text
배포 default → H-007 : 2개 차이 (LIN 0.5→1.0, TERM -5→-50)
H-001 parent → H-007 : 1개 차이 (LIN 0.5→1.0)
```

이 구분을 하지 않으면 H-007의 효과를 termination penalty와 혼동하게 된다.

## 3.4 PPO / environment 설정

- seed: 42
- envs: 4096
- rollout: 24 steps/env
- actor/critic: `[512, 256, 128]`, ELU
- PPO epochs: 5
- mini-batches: 4
- learning rate: 0.001, adaptive
- gamma: 0.99
- lambda: 0.95
- entropy coefficient: 0.008
- desired KL: 0.01
- max grad norm: 1.0
- clip: 0.2
- NaN check: enabled
- action dimension: 19
- observation dimension: 256
- physics dt: 0.005 s (200 Hz)
- decimation: 4 → control 50 Hz
- episode horizon: 20 s
- command resampling: 10 s

Command range:

- vx: `[-1.0, 1.5] m/s`
- vy: `[-0.5, 0.5] m/s`
- yaw: `[-1.0, 1.0] rad/s`

Terrain curriculum은 활성화되어 있고 10×20 grid, max initial terrain level 5다. stairs/inverted stairs/boxes/random rough/slopes가 혼합되어 있다. `Curriculum/terrain_levels`는 4096개 env의 **평균 난이도 상태**이지 해당 숫자의 지형을 “완전 정복했다”는 의미가 아니다.

## 3.5 Source mutation 검사

학습 전후 source hash가 모두 일치했다.

- `train.py`: `36fcd90a...`
- `play.py`: `39be98d4...`
- `humanoid_rewards.py`: `d35105f1...`
- `_finalize.py`: `734b712f...`
- `env_cfg.py`: `78927fc5...`
- `agent_cfg.py`: `4e8c9919...`

`changed_during_run=false`다. 의도하지 않은 code mutation evidence는 없다.

---

# 4. Training Dynamics

## 4.1 Resume run이므로 초반을 fresh learning으로 읽으면 안 됨

H-001 1.5K parent에 대해 프로젝트 기록상 terrain≈`5.119`, base-contact≈`32.41%`가 알려져 있다. 그런데 H-007의 첫 TensorBoard point(step 1499)는 terrain `3.438`, 이후 step 1514에서 `3.134`까지 내려간다.

이는 parent policy가 갑자기 능력을 잃었다는 뜻이라기보다, **resume 직후 curriculum state/reset 및 logger warm-up이 fresh trajectory와 다르다는 강한 증거**다. 따라서 `1499~1549`는 성능 비교 구간이 아니라 resume warm-up으로 별도 취급한다.

H-007은 이후:

- terrain 4.0 최초 도달: step **1596**
- terrain 5.0 최초 도달: step **1717**
- H-001 1.5K reference 5.119 최초 재돌파: step **1764**
- terrain peak: **5.423 @ 2845**
- endpoint: **5.368 @ 2998**
- last-500 mean: **5.372**

즉 resume reset을 회복한 뒤 terrain capability를 다시 확보하고 후반에는 5.3대에서 plateau한다.

## 4.2 Phase별 평균

| Phase | Step | Mean reward | Episode length | Terrain | XY error ↓ | Yaw error ↓ | Base-contact ↓ | Timeout ↑ | Mean std |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Resume warm-up | 1499–1549 | 4.962 | 486.84 | 3.242 | 0.245 | 0.735 | 17.58% | 46.44% | 1.351 |
| Early adaptation | 1550–1749 | 7.415 | 773.02 | 4.455 | 0.368 | 1.337 | 30.01% | 70.00% | 1.436 |
| Terrain consolidation | 1750–2149 | 5.652 | 756.12 | 5.156 | 0.362 | 1.690 | 32.07% | 67.95% | 1.575 |
| Late specialization | 2150–2649 | 5.443 | 769.13 | 5.296 | 0.350 | 1.955 | 30.23% | 69.78% | 1.625 |
| Final plateau | 2650–2998 | 5.392 | 757.14 | 5.376 | **0.337** | **2.014** | 30.66% | 69.35% | 1.626 |

이 표의 핵심은 **terrain과 XY는 후반까지 좋아지지만 yaw는 같은 기간 꾸준히 나빠진다**는 점이다.

## 4.3 Last-window

| Window | Episode | Terrain | XY error ↓ | Yaw error ↓ | Base-contact ↓ | Timeout ↑ | Std |
|---|---:|---:|---:|---:|---:|---:|---:|
| Last 500 | 759.77 | 5.3718 | **0.3386** | **2.0080** | 30.62% | 69.39% | 1.6262 |
| Last 200 | 756.09 | 5.3819 | 0.3355 | 2.0152 | 30.57% | 69.45% | 1.6221 |
| Last 100 | 750.65 | 5.3725 | 0.3294 | 2.0005 | 30.78% | 69.23% | 1.6197 |
| Last 50 | 743.19 | 5.3617 | 0.3257 | 1.9866 | 31.50% | 68.50% | 1.6188 |
| Last 10 | 741.42 | 5.3698 | 0.3282 | 2.0016 | 32.27% | 67.73% | 1.6186 |

Endpoint 하나만 보면 episode length가 `705.55`, base-contact `32.69%`로 다소 나빠 보이지만 last-window 전체를 보면 후반 정책은 대략 terrain 5.37 / BC 30~31% / XY 0.33~0.34 / yaw 2.0 영역에 머문다. 따라서 endpoint 노이즈를 성능 전체로 해석하면 안 된다.

## 4.4 Change point 후보

### Phase A — curriculum reset/recovery (`1499~1764`)

- terrain이 3.1대까지 낮아졌다가 5.1대로 빠르게 회복
- episode가 정상 범위로 올라감
- std 증가
- yaw error 동반 증가

이 구간은 “새 gait를 처음부터 배우는 단계”보다 **parent 정책을 새로운 reward 아래에서 재적응시키고 curriculum을 다시 올라가는 단계**로 보는 것이 타당하다.

### Phase B — terrain consolidation (`~1750~2150`)

- terrain 5.1대 정착
- base-contact 32% 안팎
- XY는 큰 변화 없음
- yaw가 계속 나빠짐
- std가 1.5→1.6대로 상승

### Phase C — translation specialization (`~2150~2998`)

- terrain은 5.3대 plateau
- XY error는 점진적으로 개선
- yaw error는 약 2.0에서 높은 plateau
- action-rate/dof-acc/slide 관련 비용 증가

이를 종합하면 **“생존/terrain 회복 → 선형 추종 미세 개선 → yaw/smoothness 희생을 동반한 specialization”**이 가장 설명력이 높은 phase model이다.

---

# 5. Tracking Analysis

## 5.1 Linear XY tracking

현재 logger는 x와 y error를 분리하지 않고 `error_vel_xy`를 기록한다. 따라서 **forward와 lateral을 독립적으로 평가할 수 없다.** 아래 결론은 결합 XY tracking에 한정한다.

주요 관측:

- early-adapt mean: `0.3683`
- terrain-consolidation: `0.3624`
- late-specialization: `0.3500`
- final-plateau: `0.3367`
- last-500: `0.3386`
- final: `0.3155`
- post-warmup minimum: `0.3001 @ 2978`

50-step rolling mean도 상당히 늦게 개선된다.

- rolling XY ≤ 0.35: 약 step 2278
- rolling XY ≤ 0.34: 약 step 2587
- rolling XY ≤ 0.33: 약 step 2971

즉 linear tracking 개선은 resume 직후 즉시 나타난 것이 아니라 **terrain이 이미 회복된 뒤 후반 수백 iteration에서 천천히 축적**됐다.

### 해석

**강한 정황:** `track_lin_vel_xy_exp`를 1.0으로 높인 branch는 후반에 XY error를 낮추는 방향으로 specialization한다.

**하지만 인과 미확정:** 같은 parent에서 `track_lin=0.5`로 +1.5K 이어간 control이 없기 때문에, 이 감소량 전체를 reward 변경 효과라고 주장할 수 없다. 추가 학습만으로도 같은 개선이 일어났을 수 있다.

## 5.2 Forward vs lateral

**판단 불가.** 결합 XY error만 존재한다. 공식 시나리오의 전진/좌우를 따로 최적화하려면 evaluator에서 `vx RMSE`, `vy RMSE` 또는 command-bucket별 score를 따로 저장해야 한다.

## 5.3 Yaw / Turning

Yaw는 이번 run에서 가장 명확한 부작용이다.

- early-adapt mean: `1.337`
- terrain-consolidation: `1.690`
- late-specialization: `1.955`
- final-plateau: `2.014`
- last-500: `2.008`
- max: `2.236 @ 2626`
- final: `1.982`

50-step rolling yaw error는 대략:

- `≥1.5`: step ~1787
- `≥2.0`: step ~2466

즉 terrain이 안정권으로 올라간 뒤 회전 추종은 계속 악화된다. 이것은 단순 endpoint noise가 아니라 장기간 지속되는 방향이다.

### 결론

**확인됨:** XY와 yaw는 이번 학습에서 같은 방향으로 개선되지 않았다.

**강한 정황:** reward budget/정책 표현이 선형 이동 쪽으로 재배분되면서 turning fidelity가 희생되는 specialization이 발생했다.

## 5.4 Stop behavior

- zero-command drift: 판단 불가
- 정지 후 흔들림: 판단 불가
- 재출발: 판단 불가

영상 command가 10초마다 resample되지만, “정지 명령을 의도적으로 부여한 고정 evaluator”가 아니다. stop 성능은 현재 video로 인증할 수 없다.

## 5.5 영상의 command tracking sanity check

play 환경 visualizer에서 goal velocity arrow와 current velocity arrow가 여러 프레임에서 완전히 겹치지 않는다. 특히 약 10초 command-resample 전후에는 목표 화살표 변화 뒤 현재 속도 방향이 따라가는 transient가 보인다.

이것은 **tracking이 완벽하지 않다는 정성 evidence**로는 유효하지만, 카메라 투영만으로 m/s error를 읽을 수 없으므로 물리량으로 환산하지 않는다. 수치 판단은 TensorBoard error를 우선한다.

---

# 6. Stability Analysis

## 6.1 Fall / base-contact / timeout

후반(last-500):

- base-contact: `30.62%`
- timeout: `69.39%`
- episode length: `759.77`

H-001 1.5K reference의 base-contact≈`32.41%`와 비교하면 H-007 후반은 약 `-1.79 percentage point`다. terrain도 5.119→5.372 수준으로 높다. 다만 H-007은 parent 이후 1.5K를 더 학습했으므로 이것을 reward 효과라고 말할 수 없다.

중요하게도 높은 timeout만 보고 “안정적”이라고 결론내리지 않았다. 실제 video에서 걷고 있고 terrain이 진행되며, 누워서 termination만 피하는 패턴은 관찰되지 않았다.

## 6.2 Terrain progression

- resume 직후: `3.44`
- min: `3.13 @1514`
- parent reference 5.119 재돌파: `1764`
- last-500: `5.372`
- peak: `5.423 @2845`
- endpoint: `5.368`

terrain이 `0`으로 눌리거나 장기 collapse하지 않았다. 선형 tracking 강화가 H1의 gross terrain progression을 파괴했다는 evidence는 없다.

다만 curriculum 평균은 obstacle별 capability를 의미하지 않는다. boxes/stairs/slope 각각의 성공률은 별도 evaluator가 필요하다.

## 6.3 Posture / vertical motion / body angular stability

직접 error metric이 부족하다. `flat_orientation_l2` reward term은 early와 late가 거의 비슷하여 gross posture cost가 크게 악화됐다는 수치 evidence는 약하다. 반면 `ang_vel_xy_l2` 및 기타 motion cost는 약간 더 부정적으로 움직이는 시점들이 있어 활동량 증가 가능성이 있다.

## 6.4 Recovery / push recovery

**판단 불가.** train에는 randomization이 있을 수 있지만 explicit push evaluator 결과가 없다. play 영상도 의도적 push sequence가 아니다.

## 6.5 Foot sliding / gait smoothness

`feet_slide`와 `action_rate` penalty가 후반에 더 부정적으로 변한다. 영상의 `model_1700`에서는 명백한 skating/hopping이 보이지 않지만 카메라만으로 미세 foot slip을 정확히 측정할 수 없다.

따라서 결론은:

- gross gait stability: 유지
- fine smoothness/contact quality: 악화 정황
- 정확한 foot slip: 추가 fixed evaluator 필요

---

# 7. Reward Component Analysis

`1550~1749`의 early stable 구간과 last-500을 비교하면 다음과 같다.

| Reward component | Early | Last-500 | 변화 해석 |
|---|---:|---:|---|
| `track_lin_vel_xy_exp` | +0.6221 | +0.6225 | 거의 동일 |
| `track_ang_vel_z_exp` | +0.1232 | +0.0806 | **약 -34.6%**; yaw 추종 악화와 일치 |
| `dof_acc_l2` | -0.0538 | -0.0659 | penalty magnitude **+22.5%** |
| `action_rate_l2` | -0.0707 | -0.0859 | penalty magnitude **+21.4%** |
| `feet_air_time` | +0.0044 | +0.0062 | 약 +39%, 더 적극적 swing 가능성 |
| `flat_orientation_l2` | -0.0145 | -0.0146 | 거의 동일 |
| `feet_slide` | -0.0536 | -0.0607 | penalty magnitude **+13.2%** |
| `joint_deviation_arms` | -0.0913 | -0.1069 | penalty magnitude **+17.2%** |
| `termination_penalty` | -0.0200 | -0.0208 | 거의 비슷, 약간 악화 |

## 7.1 왜 `track_lin` component 자체는 거의 안 올랐는데 XY error는 개선됐나?

Reward component 값은 weight, kernel/saturation, episode distribution, terrain 난이도, command distribution의 영향을 동시에 받는다. 특히 이번 run은 curriculum이 움직인다. 따라서 `track_lin` component 절댓값을 “실제 속도 오차”의 대용치로 직접 비교하면 안 된다.

이 분석에서는 실제 `Metrics/base_velocity/error_vel_xy`를 더 우선한다. 그 지표는 후반에 명확히 감소한다.

## 7.2 핵심 trade-off

가장 중요한 패턴은 다음과 같다.

```text
XY error ↓
terrain 유지/소폭 ↑
        동시에
Yaw error ↑↑
action-rate penalty ↑
dof acceleration penalty ↑
feet-slide penalty ↑
```

즉 H-007은 “빠르게만 가는 대신 바로 넘어지는” 단순 실패가 아니다. 더 미묘하게, **선형 tracking을 정교화하면서 turning/smoothness 비용을 지불하는 정책**이다.

## 7.3 시계열 동행관계 — 인과 아님

step 1600 이후 Spearman descriptive correlation은 대략:

- terrain ↔ yaw error: `+0.81`
- yaw error ↔ mean std: `+0.81`
- mean std ↔ action-rate reward: `-0.64`
- terrain ↔ XY error: `-0.60`

이 값은 시간과 curriculum이 공통 confounder이므로 causal coefficient가 아니다. 단지 “후반/높은 terrain으로 갈수록 XY는 좋아지고 yaw·action variation은 나빠진다”는 phase 해석과 일치하는 보조 정황이다.

---

# 8. PPO / Numerical Stability

## 8.1 Value loss

전체 1,500 points:

- median: **0.009259**
- p95: **0.010867**
- p99: **0.011481**
- max: **0.057324 @1499**
- `>=0.02`: 2회
- `>=0.05`: 1회
- `>=0.1`: 0회

resume warm-up을 제외한 step 1550 이후:

- max: **0.012444 @1642**

즉 이전 Go2 사례처럼 수십~수백 단위 value-loss spike가 반복되는 상태와 전혀 다르다. **H-007은 PPO numerical instability가 주요 문제라는 evidence가 없다.**

## 8.2 Surrogate / entropy / learning rate

fatal anomaly는 없다. entropy는 정책 std 상승과 함께 증가하는 방향이며 adaptive LR은 여러 level로 조정됐다.

주요 LR value 빈도:

- 약 `2.56e-4`: 가장 오래 사용
- 약 `1.71e-4`: 그 다음
- 약 `3.84e-4`: 일부 구간
- 약 `1.14e-4`: 일부 구간

Adaptive schedule이 작동한 흔적으로 해석할 수 있다.

## 8.3 KL

`desired_kl=0.01`은 config에 있지만 TensorBoard raw scalar에 실제 KL tag가 없다. 따라서 **KL 시계열은 판단 불가**다. 없는 값을 추정하지 않는다.

## 8.4 Action std

mean std:

- first: `1.3448`
- max: `1.6341 @2621`
- last-500 mean: `1.6262`
- final: `1.6173`

평균 std가 높지만 이것만으로 “학습 실패”라고 판정할 수 없다. 실제 checkpoint의 action-dimension별 std는 매우 이질적이며, low-std dimension과 high-std dimension이 공존한다.

검사 예:

- `model_1700`: mean≈1.471, min≈0.193, max≈2.542
- `model_2998`: mean≈1.617, min≈0.312, max≈2.758

16개 checkpoint의 actor/critic/optimizer tensors를 로드해 finite 여부를 검사했으며 **모두 finite**다.

더 중요한 점은 play용 exported TorchScript policy가 deterministic actor mean을 사용하며 `distribution.std_param`을 포함하지 않는다는 것이다. 따라서 play 영상에서 보이는 gait를 “std가 높아서 랜덤으로 흔들렸다”고 설명하면 안 된다.

## 8.5 Throughput / GPU

steady-state train telemetry:

- GPU: NVIDIA L40S 46 GB
- GPU util mean: 약 **54.2%**
- GPU util p95: 약 **61.9%**
- VRAM: 약 **5,236 MiB** steady
- power mean: 약 **164 W**
- temperature mean: 약 **49.8°C**, max 52°C
- FPS median: 약 **126,361**
- collection time median: 약 **0.695 s**
- learning time median: 약 **0.082 s**

OOM/memory pressure evidence는 없다. 첫 iteration의 낮은 FPS는 startup overhead라 steady-state 성능으로 사용하지 않는다.

---

# 9. Checkpoint Analysis

## 9.1 자동 best와 raw best가 다름

가장 중요한 tooling 발견이다.

### Raw TensorBoard + console

- global raw max `Train/mean_reward`: **9.825895 @ step 1564**
- console에도 `Learning iteration 1564`, `Mean reward: 9.83` 명시

### report/finalizer

- `report.html`: **8.21 @ iter 1733**
- console finalize: `Best by Train/mean_reward: step 1733, reward 8.214 → model_1700.pt`
- exported `model_best.pt` SHA == `model_1700.pt` SHA

따라서 raw scalar와 automatic selection은 실제로 불일치한다.

### 원인에 대한 제한

과거 H1 25K에서는 EventAccumulator default scalar limit 10,000으로 인한 report truncation이 확인된 적이 있다. 그러나 이번 H-007은 tag당 scalar가 1,500개뿐이므로 **그 과거 버그를 이번 불일치의 원인이라고 단정할 수 없다.** `_finalize.py` 실제 내부 selection 로직/입력 범위를 추가 실행 없이 역추적하지 않았으므로 원인은 “미확정”으로 둔다.

또 raw reward 최고인 1564는 terrain이 아직 `3.605`인 resume-recovery 구간이다. 따라서 raw reward peak도 locomotion capability best라는 뜻은 아니다.

## 9.2 주요 checkpoint 후보

| Checkpoint | Reward | Episode | Terrain | XY ↓ | Yaw ↓ | BC ↓ | Std | 해석 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| ~1600 | 8.129 | 810.21 | 4.055 | 0.380 | **1.290** | 29.24% | 1.403 | raw reward peak 인접, 쉬운 terrain |
| **1700** | 6.402 | 739.74 | 4.902 | 0.348 | **1.310** | 31.40% | 1.471 | 자동 selected + video |
| 1800 | 6.225 | 777.16 | 5.231 | 0.383 | 1.618 | 32.93% | 1.531 | terrain 회복 완료 |
| 2300 | 5.101 | 748.21 | 5.237 | **0.339** | 1.862 | 30.22% | 1.625 | mid-late XY 개선 |
| **2800** | 5.640 | 767.78 | **5.401** | **0.333** | 1.994 | 31.31% | 1.627 | terrain-peak 근처 |
| **2900** | 6.058 | **801.40** | 5.364 | 0.338 | 2.084 | **29.70%** | 1.622 | late survival 강함, yaw 약함 |
| **2998** | 5.029 | 705.55 | 5.368 | **0.315** | 1.982 | 32.69% | 1.617 | late linear 강함, endpoint survival 약함 |

한 checkpoint가 모든 축에서 우월하지 않다.

### 역할별 후보

- training reward 후보: 1600/1700 주변
- yaw 보존 후보: 1600/1700
- terrain + XY 균형 후보: 2800 부근
- episode/base-contact late 후보: 2900
- linear tracking late 후보: 2998 / 2978 인근

즉 **“학습 reward 최고”, “tracking 최고”, “terrain 최고”, “stability 최고”, “실제 제출 후보”가 서로 같은 checkpoint가 아니다.**

## 9.3 Checkpoint hash

선택된 주요 hash:

- `model_1700.pt`: `fcca7719204808401ac24fdffaec62ed3099f433f202377f9d9dbd72dfa94668`
- `model_2800.pt`: `44c2693b65a3fa83ee47dbea36b47068bc4bd804d7871b41b3e718f3fb03e07b`
- `model_2900.pt`: `71ec877e59c977440557ba541e0c98ab2a5764258701d914b1b08429cac6fa18`
- `model_2998.pt`: `388ea635532d206049957518fb8f5fb73ff91da16dc9fa3017d7c8b41715767f`

`model_best.pt`는 `model_1700.pt`와 byte/hash identity가 같다.

## 9.4 Policy lineage

play export의 `policy.pt` SHA-256:

`ee58fffde4f3e00e28cc09c95759df36d35f04489065a44d0337a6eab6a53386`

TorchScript의 8개 MLP actor weight/bias를 checkpoint `model_1700.pt` actor tensor와 직접 비교했으며 **모두 `torch.equal`**이었다. 따라서 video의 actor lineage는 파일명 수준이 아니라 tensor 수준으로 강하게 연결된다.

---

# 10. Video / Behavioral Analysis

## 10.1 Video provenance

- source checkpoint: `model_best/model_1700` SHA `fcca...94668`
- H.264, 1920×1080
- 50 fps
- 약 19.98 s
- 999 frames
- MP4 SHA: `58cdde2c...27d91`
- 1 env
- headless + offscreen cameras

Fresh/modified MP4만 수집된 provenance라 stale video 가능성은 낮다.

## 10.2 기본 행동

영상 프레임을 구간별로 확인한 결과:

- 초기 로딩 직후부터 로봇은 직립 상태를 유지
- 영상의 가시 구간에서 명백한 낙상/옆으로 눕기/뒤집힘 없음
- 좌우 발을 교대로 사용하는 정상적인 biped gait 존재
- 장시간 한 발만 들고 버티는 현상 없음
- 반복적인 깡충 hopping 없음
- 명령 변화 뒤에도 즉시 catastrophic fall하지 않음

따라서 “높은 timeout이 사실은 누운 채 버티는 local optimum”이라는 형태는 이 selected checkpoint 영상과 일치하지 않는다.

## 10.3 관측되는 약점

후반 프레임 일부에서 좁은 보폭/cross-over에 가까운 발 배치와 knee flexion이 보인다. 이는 catastrophic failure는 아니지만 aggressive translation 시 gait margin이 넓지 않을 가능성을 시사한다.

또 goal/current velocity visualizer 화살표가 여러 시점에서 겹치지 않는다. 특히 약 10초 command-resample 경계에서 transient mismatch가 보인다. 이는 raw tracking metric의 “완벽하지 않은 추종”과 정성적으로 일치한다.

## 10.4 영상으로 판정할 수 없는 것

- stop command drift
- push recovery
- terrain 종류별 성공률
- boxes/stairs/slope 완주율
- 정확한 foot slip 속도
- final `model_2998` 행동

영상은 **model_1700 하나**만 보여준다. 따라서 late checkpoint의 향상/악화는 영상으로 직접 검증되지 않았다.

---

# 11. Baseline / Parent Comparison

## 11.1 가장 중요한 비교 한계

H-007의 causal parent 비교에는 **동일 parent에서 reward를 바꾸지 않고 +1.5K resume한 control이 없다.** 따라서 다음 두 효과가 섞여 있다.

1. 추가 1,500 iteration 학습 효과
2. `track_lin_vel_xy_exp 0.5→1.0` 효과

또 terrain generator seed가 고정된 paired benchmark 형태가 아니므로 curriculum sample sequence도 완전히 같다고 가정할 수 없다.

## 11.2 H-001 1.5K parent와 제한적 비교

프로젝트에 기록된 H-001 1.5K reference:

- terrain ≈ `5.119`
- base-contact ≈ `32.41%`

H-007 last-500:

- terrain `5.3718` → reference 대비 약 `+0.253` (+4.9%)
- base-contact `30.62%` → 약 `-1.79 pp`

이 결과는 “H-007이 parent에서 완전히 망가지지 않았다”는 근거로는 좋다. 그러나 **추가 학습량이 다르므로 reward change의 causal improvement로 부르면 안 된다.**

## 11.3 H-001 공식 TERM50 5K와 contextual comparison

H-001 공식 5K endpoint 기록:

| Metric | H-001 OFFICIAL TERM50 5K | H-007 PERSONAL last-500 | 단순 차이 | 해석 제한 |
|---|---:|---:|---:|---|
| Terrain | 5.825 | 5.372 | -0.453 (-7.8%) | 환경/길이/lineage 다름 |
| Base-contact | 28.93% | 30.62% | +1.69 pp | H-007 약간 열세 |
| Timeout | 71.07% | 69.39% | -1.68 pp | H-007 약간 열세 |
| Episode length | 774.1 | 759.8 | -14.3 (-1.9%) | contextual only |
| XY error | 0.378 | **0.339** | **-10.4%** | H-007 방향상 우세 |
| Yaw error | **0.935** | **2.008** | **+114.8%** | H-007 명확한 열세 |
| Mean std | 1.296 | 1.626 | +25.5% | 단독 성패 기준 아님 |

가장 눈에 띄는 패턴은 **XY는 좋아졌지만 yaw는 크게 나빠졌다**는 것이다. 다만 이 표는 OFFICIAL 5K vs PERSONAL resumed branch를 비교하므로 paired causal table이 아니다.

## 11.4 공식 점수와 연결

H-001 TERM50 정책의 예선 2라운드 공식 결과는 종합 `86.37/100`, simulation `56.37/70`이었다. H-007에는 공식 평가 결과가 없다.

따라서:

- H-001 공식 실점 병목: 전진 절대 gap과 rough terrain 비율 등
- H-007 내부 병목: yaw error와 smoothness 비용

을 섞어 말하면 안 된다. H-007의 XY 개선이 공식 전진 점수를 올릴지는 **아직 검증되지 않았다.**

---

# 12. Tracking vs Stability Trade-off

이번 run은 네 가지 단순 quadrant 중 하나로 깔끔하게 분류하기 어렵다.

## Tracking

- Linear/XY: **↑ 개선**
- Forward: 판단 불가(별도 x metric 없음)
- Lateral: 판단 불가(별도 y metric 없음)
- Yaw: **↓ 악화**
- Stop: 판단 불가

## Stability

- gross terrain progression: **유지/회복 성공**
- base-contact/timeout: **대체로 유지**
- episode: 대체로 유지하되 후반 약한 하락
- posture: 큰 붕괴 evidence 없음
- smoothness/contact quality: **악화 정황**
- push recovery: 판단 불가

따라서 가장 정확한 성격 표현은:

> **“Linear tracking ↑ / Yaw tracking ↓ / Gross stability ≈ / Fine smoothness ↓”**

즉 “Tracking ↑ / Stability ↑” 같은 한 줄 quadrant로 압축하면 중요한 trade-off를 숨긴다.

---

# 13. Local Optimum / Reward Hacking Check

| 위험 패턴 | 판정 | 근거 |
|---|---|---|
| 움직이지 않고 생존 | **증거 없음** | terrain 진행, video 실제 보행 |
| 누운 자세로 termination 회피 | **증거 없음** | selected video 직립 |
| 한 발 장시간 들기 | **증거 없음** | dense frame 확인 |
| hopping | **증거 없음** | 반복 hopping 관찰 안 됨 |
| sliding | **판단 제한** | reward penalty 악화 정황, 카메라로 정량 불가 |
| command 무시 | **부분 위험** | XY는 개선, yaw는 악화; command arrow mismatch 존재 |
| terrain 회피 | **판단 불가** | curriculum 평균만 있음 |
| episode length만 긴 정책 | **아님** | 실제 이동/terrain/XY 지표 동반 |
| reward component 하나만 hacking | **classic hacking 증거 없음** | 다만 translation over-specialization 가능 |

이번 run의 위험은 classic reward hacking보다 **objective over-specialization**이다. 선형 translation objective를 강화한 결과 turning fidelity와 control smoothness가 밀려나는 구조가 더 잘 맞는다.

---

# 14. Key Findings

중요도 순으로 정리한다.

1. **H-007은 정상 종료·evidence PASS인 유효한 PERSONAL resume experiment다.** 수치적 발산이나 artifact corruption으로 결과를 폐기할 이유가 없다.
2. **실험의 실제 단일 delta는 H-001 parent 대비 `track_lin 0.5→1.0`이다.** report가 `termination -5→-50`도 표시하는 것은 default 대비 설명이지 이번 branch의 새 변경이 아니다.
3. **Resume 직후 curriculum reset이 명확하다.** parent terrain≈5.119에서 H-007 시작 3.44/최저3.13으로 내려갔다가 step1764에 다시 parent 수준을 넘는다. 따라서 fresh trajectory의 단순 연속으로 읽으면 안 된다.
4. **Linear XY tracking 개선은 실제로 존재하지만 매우 늦게 나타난다.** rolling50 XY≤0.35는 ~2278, ≤0.33은 ~2971이다.
5. **Yaw는 반대 방향으로 악화된다.** early mean1.337 → last500≈2.008. H-007의 가장 큰 내부 병목이다.
6. **Gross stability/terrain은 무너지지 않았다.** last500 terrain5.372, base-contact30.62%, timeout69.39%; selected video도 약20초 동안 직립 보행한다.
7. **Fine control quality는 희생되는 정황이 있다.** action-rate, dof acceleration, feet-slide, arm deviation penalty가 후반에 더 커진다.
8. **PPO 자체는 매우 안정적이다.** step1550 이후 value-loss max0.01244, NaN/Inf 없음, 16 checkpoint tensor finite. 병목은 optimizer가 아니라 reward trade-off다.
9. **자동 `model_best` selection이 raw TensorBoard와 불일치한다.** raw max9.826@1564 vs report8.214@1733→model1700. 따라서 자동 별칭을 실제 최적 policy로 보지 않는다.
10. **현재 가장 큰 실험 설계 공백은 same-parent resume-control 부재다.** 이 때문에 XY 개선을 reward change의 순수 효과로 분리할 수 없다.

---

# 새로운 발견

## A. Reward 강화의 효과가 즉시가 아니라 “후반 specialization”으로 나타남

H-007은 초반부터 XY가 급격히 좋아지는 정책이 아니다. 먼저 curriculum을 회복하고 terrain 5대에서 버틴 뒤, 2.2K 이후부터 XY가 서서히 내려간다. 이는 단순 “weight를 키우면 바로 tracking reward가 증가”하는 형태보다, **기존 H-001 gait를 유지한 채 후반에 행동 분포를 재조정하는 fine-tuning**에 가깝다.

## B. Yaw degradation과 std/action variation의 동시 상승

Yaw error와 std가 매우 유사한 시기에 상승하고 action-rate penalty도 악화된다. 이는 translation-focused policy가 더 적극적인 관절 action을 사용하며 yaw control margin을 소모하는 가능성을 제기한다. 다만 time/curriculum confounding이 있으므로 인과는 다음 ablation에서 검증해야 한다.

## C. 자동 best checkpoint가 “실험 질문”과 맞지 않음

H-007의 실험 질문은 linear tracking 개선이다. 그런데 자동 best는 early terrain-recovery 구간의 model1700을 선택했다. 후반 model2800/2900/2998이 더 높은 terrain/낮은 XY를 보이므로, **training reward based selection rule 자체가 H-007의 목적 함수와 어긋날 수 있다.**

---

# 15. Final Decision

## **HOLD**

### PROMOTE가 아닌 이유

- H-007에는 same-parent no-change resume control이 없다.
- linear XY는 좋아졌지만 yaw가 크게 악화됐다.
- smoothness/contact 관련 비용도 악화 정황이 있다.
- current video는 early `model_1700`만 검증하며 late checkpoint 행동은 미확인이다.
- single seed다.
- PERSONAL run이며 official evaluator/score가 없다.

### REJECT가 아닌 이유

- terrain progression이 회복되고 강한 수준을 유지한다.
- base-contact/timeout이 붕괴하지 않는다.
- XY error는 후반에 실제로 개선된다.
- numerical instability가 없다.
- video에서 classic reward hacking/낙상 정책이 아니다.

따라서 H-007은 **“가능성은 있지만 causal benefit과 trade-off가 아직 분리되지 않은 후보”**다.

---

# 16. Next Experiment

## 16.1 다음 학습 1순위 — Same-parent Resume Control

가장 정보 효율이 높은 다음 학습은 새 reward를 또 바꾸는 것이 아니다.

### 설계

**Parent:** H-001 exact `model_1499.pt`

- required SHA-256: `68fa0a9fe5334f8a3ecea110c4ccc9adb81ec07ac50169eaf8009b1a6e88f0c1`

**Control reward:**

- `track_lin_vel_xy_exp = 0.5` 유지
- `termination_penalty = -50` 유지
- 나머지 reward 모두 parent와 동일

**학습량:** +1,500 iterations

**고정 조건:**

- seed 42
- 4096 envs
- 24 rollout steps/env
- 동일 PPO
- 동일 H1 source hash
- 동일 terrain/environment config
- 동일 headless/camera 조건
- 동일 checkpoint save policy

### 왜 이 실험이 최우선인가

현재 H-007은 다음 두 변수를 동시에 갖는다.

```text
추가 학습 +1500 iterations
track_lin 0.5 → 1.0
```

control branch를 만들면 최초로:

```text
H-001 parent
 ├─ Control: track_lin 0.5, +1500
 └─ H-007:   track_lin 1.0, +1500
```

의 paired question을 만들 수 있다. 그러면 **“추가 학습 효과”와 “reward 변화 효과”를 분리**할 수 있다.

## 16.2 성공/실패 판정 기준

Train mean reward는 비교 objective로 사용하지 않는다. reward weight가 다르므로 척도가 달라진다.

H-007을 PROMOTE하려면 같은 evaluator/last-window에서 최소한 다음을 확인해야 한다.

### Primary success

- H-007 XY error가 control보다 일관되게 낮음
- 복수 checkpoint 또는 last-window에서 같은 방향

### Guardrail

- yaw error가 control 대비 크게 악화되지 않음
- terrain이 control과 동급 이상
- base-contact/timeout이 의미 있게 악화되지 않음
- action-rate/feet-slide가 과도하게 악화되지 않음
- 영상에서 hopping/overstride/fall 증가 없음

### 해석 분기

**A. Control도 H-007만큼 XY가 좋아진다**

→ H-007의 causal benefit 미확인. 현재 개선은 대부분 추가 학습일 가능성. `track_lin=1.0` 승격 중단.

**B. H-007이 XY는 확실히 좋지만 yaw/smoothness가 나쁘다**

→ 다음 단일 변수 후보는 같은 parent에서 `track_lin=0.75`. 1.0과 0.5 사이 Pareto point를 찾는다.

**C. H-007이 XY가 좋고 yaw/stability도 control과 동급이다**

→ H-007을 stronger evaluator / OFFICIAL confirmation 후보로 PROMOTE.

## 16.3 새 학습 전에 먼저 할 수 있는 zero-training checkpoint test

추가 GPU 학습보다 먼저, 이미 보존된 checkpoint를 동일 fixed evaluator로 비교하는 것이 매우 값싸고 정보량이 크다.

추천 후보:

1. `model_1700` — 현재 자동 best, yaw 상대적으로 양호
2. `model_2300` — mid-late XY 개선
3. `model_2800` — terrain peak 근처 + 낮은 XY
4. `model_2900` — episode/base-contact late 강점
5. `model_2998` — late linear 최강 후보

고정 evaluator에서 최소 다음을 분리한다.

- vx tracking RMSE
- vy tracking RMSE
- yaw RMSE
- zero-command drift
- base-contact/fall
- terrain별 traversal progress
- action-rate / foot sliding
- command-switch transient

현재 `model_best=1700` 하나만 video를 본 상태라 late checkpoint를 평가하지 않고 추가 학습하는 것은 비효율적이다.

## 16.4 2순위 학습 후보

Same-parent control로 `track_lin=1.0`의 실제 benefit이 확인되었지만 yaw trade-off가 너무 크다면:

- `track_lin_vel_xy_exp: 0.5 → 0.75`
- same H-001 parent
- +1.5K 동일 조건

을 실행한다.

목표는 “1.0에서 얻은 XY 개선 대부분을 유지하면서 yaw/action-rate 손실을 줄이는 Pareto point”다.

**현재 단계에서 `track_ang_vel_z`까지 동시에 올리는 조합 실험은 권장하지 않는다.** 그렇게 하면 LIN change의 인과를 다시 잃는다.

---

# 17. Confidence & Limitations

## 17.1 강하게 확정 가능한 것

- H-007은 H1 PERSONAL resume run이다.
- parent checkpoint name/path/SHA가 metadata에 기록되어 있다.
- command, seed, env count, PPO, reward, env config가 보존됐다.
- train archive 38/38, play archive 20/20 checksum이 맞는다.
- run은 exit 0으로 완료됐다.
- 1500 raw TensorBoard rows와 full console이 일치한다.
- terrain/XY/yaw/base-contact/std/loss 전체 trajectory를 복원했다.
- numerical failure가 없다.
- 16 checkpoint tensors는 finite다.
- `model_best == model_1700` hash identity가 확정됐다.
- exported policy actor == model1700 actor tensor exact-match다.
- video가 해당 selected checkpoint에서 생성됐다는 lineage가 강하다.
- selected video에서는 명백한 fall/prone/hopping이 보이지 않는다.

## 17.2 중간 신뢰의 해석

- policy가 translation specialization 방향으로 이동했다.
- yaw/smoothness 희생이 LIN 강화와 관련 있을 가능성이 높다.
- 후반 std/action variation 증가가 turning trade-off와 연결되어 있을 가능성이 있다.

이들은 시계열과 reward term이 일관되지만 same-parent control이 없어 causal proof는 아니다.

## 17.3 약한 정황 / 판단 불가

- forward와 lateral 중 어느 축이 더 좋아졌는가: **판단 불가**
- zero-command stop: **판단 불가**
- push recovery: **판단 불가**
- stairs/boxes/slopes 각각의 성공률: **판단 불가**
- H-007의 공식 대회 점수: **없음**
- multi-seed 일반화: **판단 불가**
- final `model_2998`의 실제 gait 영상: **없음**
- report/raw reward-best mismatch의 정확한 내부 원인: **미확정**

## 17.4 Single-seed 경고

이번 run은 seed 42 단일 실행이다. 현재 방향성은 실험 evidence로 충분히 의미 있지만, “통계적 개선”, “최적값”, “일반화 성능 향상”으로 표현해서는 안 된다.

---

# Appendix A. 핵심 Raw Scalar Landmarks

| Step | Reward | Episode | Terrain | XY | Yaw | BC | Timeout | Std | 비고 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1499 | 0.056 | 11.52 | 3.438 | 0.013 | 0.017 | 0% | 1.37% | 1.345 | resume 첫 logger point; 성능용 아님 |
| 1514 | — | — | **3.134** | — | — | — | — | — | terrain minimum |
| 1564 | **9.826** | 875.24 | 3.605 | 0.387 | 1.306 | 26.82% | 73.21% | 1.378 | raw reward max |
| 1596 | — | — | 4.010 | — | — | — | — | — | terrain 4 최초 |
| 1717 | — | — | 5.004 | 0.378 | 1.520 | — | — | — | terrain 5 최초 |
| 1733 | **8.214** | 859.7 | 5.059 | 0.372 | 1.573 | 31.72% | — | 1.491 | report-selected reward step |
| 1764 | — | — | **5.123** | 0.348 | 1.403 | 31.93% | — | — | parent terrain 5.119 재돌파 |
| 1843 | — | **875.34** | 5.215 | 0.394 | 1.786 | 33.68% | — | — | episode max |
| 2400 | — | — | 5.325 | 0.355 | 1.971 | 29.77% | — | 1.631 | late specialization |
| 2626 | — | — | 5.308 | 0.358 | **2.236** | — | — | 1.633 | yaw max |
| 2845 | — | — | **5.423** | 0.351 | 2.036 | — | — | terrain peak |
| 2978 | — | — | 5.349 | **0.300** | 1.831 | — | — | — | post-warmup XY min |
| 2998 | 5.029 | 705.55 | 5.368 | **0.315** | 1.982 | 32.69% | 67.31% | 1.617 | endpoint |

---

# Appendix B. Evidence / Provenance Inventory

본 분석에서 실제 사용한 자료:

### Current H-007 raw evidence

- train archive + internal manifests
- train `metadata.json`
- `validation.json`
- full `console.log`
- raw TensorBoard `events.out.tfevents*`
- derived full scalar table (1,500×30)
- `native_run/params/env.yaml`
- `native_run/params/agent.yaml`
- actual `source/humanoid_rewards.py`
- source identity before/after hash
- 16 mirrored checkpoints
- exported `model_best.pt`
- `report.html`
- GPU before/during/after telemetry
- play archive + metadata/validation
- `video_manifest.json`
- exported `policy.pt` / ONNX
- `play_video.mp4`
- dense frame/contact/command-switch visual inspection

### Project historical comparison/provenance documents

- `00_START_HERE_CONTEXT_AND_MAP(20260916-234815).md`
- `06_HUMANOID_TRAINING_CODE(20260916-152653).md`
- `13_H1_OFFICIAL_SERVER_BASELINE_EVIDENCE(20260915-042342).md`
- `14_H1_NEXT_RUN_PARAMETER_COMPARISON(20260916-234814).md`
- `15_OPTUNA_REWARD_DECISION_ENGINE(20260916-234815).md`
- `16_EXPERIMENT_EXPORT_AND_TENSORBOARD(20260916-092146).md`
- `18_H1_FINALIZE_REPORT_LIMITATIONS(9).md`
- `19_ISSACSIMZ_EXTERNAL_EVIDENCE_CLI(20260916-092146).md`

### Evidence caveat

Parent H-001 `model_1499.pt`의 **SHA는 H-007 metadata에 강하게 기록되어 있으나 parent checkpoint 원본 바이트 자체는 이번 두 archive 안에 포함되지 않았다.** 따라서 parent lineage는 강하지만 완전 self-contained re-hash는 불가능하다. 다음 control experiment에서는 parent checkpoint 자체를 evidence bundle에도 보존하면 더 좋다.

---

# 최종 답변 — 사용자가 요청한 8개 질문

1. **이 정책은 무엇을 배웠는가?**\
   H-001의 안정 gait를 유지하면서, curriculum을 재회복한 뒤 후반에 XY velocity tracking을 더 정교하게 하는 방향으로 fine-tuning됐다. 동시에 yaw 제어와 smoothness는 희생됐다.

2. **이전 정책보다 무엇이 실제로 좋아졌는가?**\
   현재 자료에서 가장 강한 개선 evidence는 후반 XY error 감소다. terrain과 gross survival도 parent reference 수준을 재회복한다. 단, same-parent control 부재 때문에 reward 변경의 순수 효과로 확정할 수 없다.

3. **무엇을 잃었는가?**\
   yaw tracking이 크게 악화됐고, action-rate/dof-acc/feet-slide 등 fine control cost도 나빠졌다.

4. **학습 중 언제 중요한 변화가 일어났는가?**\
   1499~1764에 resume/curriculum recovery, 1750~2150 terrain consolidation, 2150 이후 linear-tracking specialization이 나타난다. XY의 강한 개선은 특히 2.3K 이후 늦게 나타난다.

5. **높은 지표가 실제 행동 개선을 의미하는가?**\
   일부만 그렇다. terrain/XY는 실제 보행 video와 모순되지 않지만, 높은 training reward의 peak는 쉬운 terrain recovery 구간에 있고 자동 `model_best`도 raw peak와 불일치한다. reward 하나만으로 policy quality를 고르면 안 된다.

6. **현재 가장 큰 병목은 무엇인가?**\
   내부 성능 기준으로는 **yaw tracking + smoothness trade-off**, 실험 설계 기준으로는 **same-parent resume-control 부재**다.

7. **이 가설은 계속 실험할 가치가 있는가?**\
   **있다. HOLD.** XY 개선 가능성은 충분하지만 아직 causal benefit과 yaw 비용이 분리되지 않았다.

8. **다음 한 번의 학습으로 가장 많은 정보를 얻으려면?**\
   exact same H-001 `model_1499.pt`에서 `track_lin=0.5` 그대로 +1.5K 이어가는 resume-control을 실행한다. 이것이 H-007의 reward 효과와 단순 추가학습 효과를 처음으로 분리해 준다.

---

원본 archive/hash, raw TensorBoard, full console, checkpoint tensors, policy actor identity, video provenance를 직접 교차검증했다. 남은 불확실성은 single seed, parent raw artifact 미포함, fixed evaluator/official H-007 score 부재, forward/lateral 분리 metric 부재에서 발생한다.

정확도 : 97%
