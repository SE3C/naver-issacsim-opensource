# H1 H-012 TERM100 5K Deep Analysis

> 분석 대상: `20260921-033633-h1-h012-term100-5k.tar.gz`  
> 원본 archive SHA-256: `b84fa6dd72c41293786ee6dff71b1001d37663813a0e4bdee74998b61436171d`  
> 분석 기준: archive 내부 원본 evidence를 우선하고, 프로젝트 핵심팩의 과거 H1 기준선은 비교 가능성 제한을 명시한 보조 근거로만 사용함.  
> 환경 분류: **PERSONAL** — 공식 대회 성능/제출 결과로 해석하지 않음.

---

# 1. Executive Summary

이번 실행은 **H1 fresh 5K PERSONAL 학습**으로 확인된다. `resume=false`, parent checkpoint 없음, seed 42, 4096 environments, 24 rollout steps/env, headless이며, 참가자 reward 9개 중 **`termination_penalty`만 baseline `-5 → -100`으로 변경**되었다. 학습 프로세스는 `exit_code=0`으로 정상 종료했고, TensorBoard 5,000점 전체, console 전체, 51개 checkpoint, source hash, GPU telemetry가 보존되었으며 archive 내부 `SHA256SUMS`는 **73/73 전부 일치**했다. 따라서 “실행/증거 무결성”은 강하다.

정책의 학습 trajectory는 단순 상승형이 아니다. 초기 평균 terrain은 `3.438`이었지만 **iter 25에 0까지 급락**했고, 이후 쉬운 지형에서 다시 학습하여 `terrain ≥ 0.5 @215`, `1 @292`, `2 @444`, `3 @604`, 초기 수준 재돌파 `@671`, `5 @1762`, `5.5 @2535`를 거쳐 후반 last-500 평균 `5.763`까지 회복했다. 즉 이번 정책은 높은 초기 curriculum을 그대로 유지한 것이 아니라, **초기 실패 → curriculum retreat → 생존/기본 보행 재학습 → 고난도 재진입**의 뚜렷한 phase를 거쳤다.

안정성 지표는 의미 있게 개선됐다. last-500 base-contact termination은 `26.68%`, timeout은 `73.34%`, mean episode length는 `811.68`이었다. terrain도 후반 `5.7`대에서 유지되므로 “움직이지 않고 쉬운 지형에서 시간만 버티는” 전형적 생존형 local optimum과는 다르다. 반면 tracking은 균형이 나쁘다. XY error는 last-500 `0.4126`까지 내려왔지만, yaw error는 last-500 `1.9107`로 매우 높다. 학습 내내 yaw는 늦게 개선되기는 했지만 마지막까지 큰 병목으로 남았다.

수치 안정성은 매우 좋다. value loss median `0.00724`, p95 `0.00920`, p99 `0.01028`, max `0.495 @ iter 1`이며, `value loss > 1`은 한 번도 없었다. 51개 checkpoint의 actor/critic/optimizer tensor를 직접 검사했을 때 **모두 finite**였다. 따라서 이번 run의 주요 문제는 optimizer 발산이나 NaN이 아니라 **정책이 어떤 행동 목표를 우선 학습했는가**에 있다.

자동 `model_best.pt`는 SHA-256상 **`model_4700.pt`와 동일**하며 raw TensorBoard reward peak `0.37454 @ iter 4671`에 의해 선택됐다. 이번 run은 5,000 scalar이므로 과거 25K run에서 확인된 EventAccumulator 10,000-limit 문제는 적용되지 않고, raw event와 report selector가 일치한다. 그러나 `model_best`가 실제 행동·공식 시나리오에서 최적이라는 뜻은 아니다. 4700 이후 final 4999까지 terrain/tracking/fall이 동시에 붕괴하지 않았고, 오히려 survival은 약간 좋아졌다. 따라서 **4700과 4999 중 실제 정책 선택은 현재 자료만으로 결정할 수 없으며 고정 evaluator/play가 필요**하다.

과거 공식 TERM50 5K endpoint와 제한적으로 비교하면 TERM100은 base-contact가 `28.93% → 26.69%`, episode length가 `774.1 → 816.45`로 안정성 방향의 이득은 보이지만, terrain은 `5.825 → 5.740`으로 높아지지 않았고 XY error는 `0.378 → 0.402`, yaw error는 `0.935 → 1.897`로 악화됐다. 특히 yaw 손실이 안정성 이득보다 훨씬 크다. 다만 두 실행은 **PERSONAL vs OFFICIAL, 실행 시점/host/source provenance가 동일하지 않기 때문에 causal paired comparison은 아니다**.

따라서 이번 H-012 가설은 **HOLD**가 적절하다. TERM100은 “더 강한 낙상 회피가 실제로 학습을 망가뜨리지 않고 high-terrain survival을 유지한다”는 점은 보여줬지만, “TERM50보다 전체 성능이 더 좋다”는 증거는 부족하고, 오히려 yaw tracking 손실 정황이 강하다. 다음 한 번의 학습으로 가장 많은 정보를 얻으려면 새로운 reward를 추가로 조정하기보다 **현재와 동일한 PERSONAL L40S / 동일 source / 동일 5K 조건에서 `termination_penalty=-50` fresh control을 재수집**해야 한다. 그 뒤에야 `-50 vs -100`의 survival-tracking trade-off를 같은 조건에서 판단할 수 있다.

---

# 2. Run Identity & Evidence Integrity

## 2.1 실험 정체성

| 항목 | 확인 결과 | 근거 수준 |
|---|---|---|
| Robot | H1 / `Humanoid-v0`, 19 actions | **확인됨** — console/env |
| Experiment ID | `H-012`로 추정 | **강한 정황** — run name에 `h012`; 제공 핵심팩 registry에는 아직 H-012 항목이 없어 독립 확인은 못함 |
| Run ID | `20260921-033633-h1-h012-term100-5k` | **확인됨** — `metadata.json` |
| Environment | **PERSONAL** | **확인됨** — `metadata.json mode=personal` |
| fresh / resume | **fresh training** | **확인됨** — `agent.yaml resume=false`, parent/source checkpoint null |
| Parent checkpoint | 없음 | **확인됨** |
| Parent iteration / SHA | 해당 없음 | **확인됨** |
| Requested iterations | 5000 | **확인됨** — command/agent |
| 마지막 console iteration | 4999/5000 | **확인됨** |
| 마지막 저장 checkpoint | `model_4999.pt` | **확인됨** |
| Checkpoint 수 | 51 (`0,100,...,4900,4999`) | **확인됨** |
| Seed | 42 | **확인됨** |
| Num envs | 4096 | **확인됨** |
| Rollout steps/env | 24 | **확인됨** |
| Observation / action | 256 / 19 | **확인됨** — console |
| Headless | yes | **확인됨** |
| Camera | 학습 command에 `--enable_cameras` 없음 | **확인됨**; 별도 video 없음 |
| 시작 시각 | `2026-09-21T03:36:33.461485+00:00` | **확인됨** |
| 종료 시각 | `2026-09-21T04:44:53.544397+00:00` | **확인됨** |
| KST 환산 | 2026-09-21 12:36:33 → 13:44:53 KST | timestamp offset 환산 |
| Core training time | `4064.41 s` ≈ 67m 44s | **확인됨** — console |
| Wrapper end-to-end | 약 `4100 s` ≈ 68m 20s | metadata 시각 차이 |
| TensorBoard | 있음, 1 event file, 5,000 step 전 구간 | **확인됨** |
| Console | 전체 있음 | **확인됨** |
| policy.pt | **없음** | **확인됨** |
| play/video | **없음** | **확인됨** |
| evaluator | **없음** | **확인됨** |
| 공식 평가 | **없음** | PERSONAL run이므로 공식 결과 아님 |

`H-012`라는 experiment ID는 filename만 본 것이 아니라 `metadata.run_id/name`에도 들어 있지만, 프로젝트 핵심팩의 registry snapshot은 H-011까지만 설명하고 있어 registry-level 독립 확인은 되지 않았다. 따라서 본 보고서는 run을 편의상 H-012로 부르되, registry source of truth가 갱신되기 전까지는 **run metadata 기반 식별자**로 취급한다.

## 2.2 실행 성공 / evidence 보존 / 정책 품질 / 제출 적합성 분리

| 판단층 | 결과 | 해석 |
|---|---|---|
| 1. 학습 프로세스 종료 | **PASS** | exit 0, iter 4999까지 완료, finalize 완료 |
| 2. Evidence 보존 | **PASS** | validation PASS, 73/73 SHA 일치, TensorBoard/console/51 checkpoints 보존 |
| 3. 정책 품질 | **부분 성공 / trade-off 존재** | high terrain·survival 확보, yaw tracking 큰 병목 |
| 4. 제출 후보 적합성 | **아님** | PERSONAL run이며 policy/video/evaluator/official score 없음 |

이 네 층을 섞으면 안 된다. 특히 `evidence_validation=PASS`는 “정책이 좋다”는 뜻이 아니라 **분석 가능한 실행이 정상 보존되었다**는 뜻이다.

## 2.3 Archive / source 무결성

- archive 내부 `SHA256SUMS`: **73/73 OK**.
- `source/identity.json`: 선택된 H1 task Python source가 실행 전후 **변경되지 않음**.
- `IsaacLab.diff`: commit `3e73d6dd79080fd7632488c061052a6edd52e230`, detached HEAD, working tree clean.
- `collected/provenance.json`: `exported/`는 run 전 file count 0, run 후 `env.yaml`, timestamp env, `model_best.pt`, timestamp best, `report.html`이 모두 **NEW**. 따라서 이번 collected export에 stale artifact가 섞였다는 증거는 없다.
- `model_best.pt`와 timestamp alias의 SHA가 동일하고, `env.yaml`과 timestamp alias도 동일하다.
- native finalizer는 원래 run 폴더의 intermediate checkpoint 50개를 삭제했지만, personal sidecar watcher가 **51개 전부를 별도 `checkpoints/`에 미리 복사**했다. 따라서 checkpoint 보존은 성공했다.

### 남은 provenance 한계

`source/identity.json`은 task 파일 hash를 남기지만 `naver-issacsim-nvidia` checkout 자체의 Git commit을 직접 기록하지 않는다. 프로젝트 운영 문서는 해당 NVIDIA `training/`이 2026-09-13 official snapshot과 동기화되었다고 설명하지만, **이번 archive 단독으로 그 repository commit을 재검증할 수 있는 Git metadata는 없다**. 또한 `runtime.txt`의 Python 3.10.12는 sidecar wrapper runtime이고, 실제 Isaac child는 `/home/shadeform/IsaacLab/_isaac_sim/python.sh` 경로를 사용한다. native child의 정확한 Python/PyTorch/RSL-RL 버전은 이 archive의 runtime summary에 일괄 기록되지 않았다.

---

# 3. Configuration Verification

## 3.1 실제 reward 변경

`source/humanoid_rewards.py`, native `params/env.yaml`, console Reward Manager, `report.html` 네 소스를 대조했다.

| Student reward | Baseline | H-012 실제값 | 변경 |
|---|---:|---:|---:|
| `track_lin_vel_xy_exp` | +0.5 | +0.5 | 0 |
| `track_ang_vel_z_exp` | +0.5 | +0.5 | 0 |
| `feet_air_time` | +0.2 | +0.2 | 0 |
| `termination_penalty` | -5.0 | **-100.0** | **-95** |
| `flat_orientation_l2` | -1.5 | -1.5 | 0 |
| `ang_vel_xy_l2` | -0.05 | -0.05 | 0 |
| `joint_deviation_hip` | -0.2 | -0.2 | 0 |
| `joint_deviation_torso` | -0.1 | -0.1 | 0 |
| `action_rate_l2` | -0.0005 | -0.0005 | 0 |

**결론: 참가자 수정 reward 기준으로는 1개만 변경된 단변수 실험이다.**

프레임워크 기본 활성 항목도 그대로 존재한다.

| 기본 reward | weight |
|---|---:|
| `dof_acc_l2` | `-1.25e-7` |
| `dof_pos_limits` | `-1.0` |
| `feet_slide` | `-0.25` |
| `joint_deviation_arms` | `-0.2` |
| `dof_torques_l2` | `0.0` |

Reward Manager에는 14개 항목이 등록되지만 `dof_torques_l2=0`이므로 **실질 nonzero reward는 13개**다.

## 3.2 PPO / environment

| 항목 | 실제 설정 |
|---|---|
| PPO epochs / minibatches | 5 / 4 |
| initial LR | 0.001, adaptive |
| gamma / lambda | 0.99 / 0.95 |
| entropy coef | 0.008 |
| desired KL | 0.01 |
| clip | 0.2 |
| max grad norm | 1.0 |
| save interval | 100 |
| physics dt | 0.005 s |
| env/control dt | 0.020 s |
| episode horizon | 20 s |
| command resampling | 10 s |
| observation shape | 256 |
| action shape | 19 |

Command range는 현재 archive 기준으로 `x=-1.0~1.5`, `y=-0.5~0.5`, `yaw=-1.0~1.0`, heading command enabled이며 standing env 비율은 `0.02`다.

## 3.3 Terrain 구성

현재 run의 curriculum terrain은 `10×20` grid, patch `8m×8m`, difficulty `0~1`, `max_init_terrain_level=5`, terrain seed `null`이다.

| terrain | proportion |
|---|---:|
| stairs | 0.15 |
| inverted stairs | 0.15 |
| boxes | **0.30** |
| random rough | 0.10 |
| slope | 0.10 |
| inverted slope | 0.10 |

따라서 `Curriculum/terrain_levels`는 4096 env와 여러 terrain 유형이 섞인 **평균 curriculum 상태**다. “terrain 5.7 = 모든 terrain level 5.7 정복”으로 읽으면 안 된다. 특히 boxes가 30%로 가장 큰 비중이다.

## 3.4 Push / recovery 학습 여부

`env.yaml`에서 `push_robot: null`이고 `base_external_force_torque`의 force/torque range도 0이다. 따라서 이번 학습 데이터 자체는 **명시적인 push disturbance recovery를 학습시킨 run이 아니다**. 공식 밀침 회복 능력은 이 training scalar로 판단할 수 없다.

---

# 4. Training Dynamics

## 4.1 TensorBoard 원본 복원

Event file을 raw protobuf 레코드로 끝까지 읽었다.

- 총 event records: **155,001**
- parse error: **0**
- scalar tags: **31**
- `/time` mirror 2개를 제외한 주요 scalar: **29**
- 각 주요 scalar: step `0~4999`, **5,000 points**

이번 run은 tag당 5,000 scalar이므로 과거 25K 사례의 EventAccumulator default 10,000-point truncation 문제는 발생하지 않는다. `report.html`의 best reward와 raw TensorBoard best reward도 정확히 일치했다.

## 4.2 Terrain trajectory — 가장 중요한 구조

| 사건 | iteration | terrain |
|---|---:|---:|
| 초기값 | 0 | 3.438 |
| 최저점 | **25** | **0.000** |
| min 이후 0.5 회복 | 215 | ≥0.5 |
| 1.0 | 292 | ≥1 |
| 2.0 | 444 | ≥2 |
| 3.0 | 604 | ≥3 |
| 초기 3.438 재돌파 | **671** | ≥3.438 |
| 4.0 | 875 | ≥4 |
| 5.0 | **1762** | ≥5 |
| 5.5 | **2535** | ≥5.5 |
| 5.8 첫 도달 | 4746 | ≥5.8 |
| raw peak | **4763** | **5.854** |
| endpoint | 4999 | 5.740 |
| last-500 평균 | 4500~4999 | **5.763** |

100-step moving average 기준으로도 `terrain ≥3 @652`, `≥4 @920`, `≥5 @1818`, `≥5.5 @2591`이다. 즉 단일 spike가 아니라 지속적인 재상승이다.

### 중요 해석

`report.html`은 “시작 3.4 → 마지막 5.74, 올라감”만 보여주지만 raw trajectory는 **중간에 0까지 완전히 후퇴했다**. 정책은 처음부터 높은 난이도를 견딘 것이 아니라, curriculum이 난도를 낮춘 후 다시 올라온 것이다. 이 차이는 H-012의 학습 메커니즘을 이해하는 데 매우 중요하다.

## 4.3 Phase 분석

| Phase | 범위 | terrain 평균 | base-contact | episode length | XY error | yaw error | 해석 |
|---|---:|---:|---:|---:|---:|---:|---|
| P0 Curriculum collapse | 0~214 | 0.215 | 78.5% | 386.7 | 0.518 | 1.549 | 초기 정책 실패, 난이도 급강하 |
| P1 Rebuild | 215~670 | 1.978 | 35.5% | 777.5 | 0.599 | 2.623 | 쉬운 지형에서 생존/보행 재구축 |
| P2 Terrain scale-up | 671~1761 | 4.383 | 29.2% | 795.3 | 0.484 | 2.502 | 초기 난도 회복 후 5까지 상승 |
| P3 High-terrain entry | 1762~2534 | 5.331 | 28.3% | 792.6 | 0.442 | 2.309 | terrain 5+ 유지, tracking 서서히 개선 |
| P4 Consolidation | 2535~4670 | 5.648 | 27.5% | 801.6 | 0.420 | 2.092 | stability plateau, yaw/XY 점진 개선 |
| P5 Late plateau | 4671~4999 | 5.769 | 26.4% | 813.4 | 0.413 | 1.910 | high terrain 유지, survival 소폭 개선, yaw 여전히 병목 |

P0/P1의 tracking 값은 episode 길이와 curriculum이 급변하는 구간이므로 후반과 단순 성능비로 비교하지 않는다. 특히 아주 짧은 episode에서는 command tracking metric의 표본 구성이 후반과 다르다.

## 4.4 Late plateau 여부

후반에는 terrain 상승 속도가 크게 둔화된다.

- 2000~2999 terrain mean: `5.482`
- 3000~3999: `5.632`
- 4000~4499: `5.718`
- 4500~4999: `5.763`

반면 yaw error는 같은 구간에서 `2.271 → 2.102 → 1.987 → 1.911`로 계속 감소한다. 즉 **terrain/stability는 먼저 plateau에 도달하고, yaw tracking은 느리게 뒤늦게 개선되는 구조**다. 5K 종료 시점에도 yaw가 아직 완전히 수렴했다고 보기 어렵지만, 절대 수준은 여전히 높다.

---

# 5. Tracking Analysis

## 5.1 Linear XY tracking

| 구간 | XY error 평균 |
|---|---:|
| 500~999 | 0.5156 |
| 1000~1999 | 0.4675 |
| 2000~2999 | 0.4375 |
| 3000~3999 | 0.4206 |
| 4000~4499 | 0.4096 |
| 4500~4999 | 0.4126 |
| endpoint | **0.4017** |

XY tracking은 명확하게 개선되었고 4K 이후 대체로 plateau다. 마지막 500에서 약간의 악화가 있지만 폭은 작고 terrain/survival과 함께 붕괴하지 않는다.

### Forward / lateral 분리 한계

TensorBoard에는 `Metrics/base_velocity/error_vel_xy` 하나만 있고 x/y component error가 따로 없다. command range에는 x/y가 모두 존재하지만 **forward와 lateral을 분리해 어느 쪽이 병목인지 확인할 수 없다**. 따라서 “전진 추종이 좋아졌다” 또는 “좌우 추종이 나쁘다” 같은 세부 결론은 이 archive만으로는 불가하다.

## 5.2 Yaw / turning

| 구간 | yaw error 평균 |
|---|---:|
| 500~999 | 2.5456 |
| 1000~1999 | 2.4581 |
| 2000~2999 | 2.2708 |
| 3000~3999 | 2.1017 |
| 4000~4499 | 1.9872 |
| 4500~4999 | **1.9107** |
| endpoint | **1.8967** |

Yaw는 꾸준히 개선되지만 **절대적으로 가장 큰 병목**이다. raw max는 `3.059 @ iter 290`이고 후반에도 약 `1.9` 수준이다. `track_ang_vel_z_exp` reward component는 500~999 `0.0681`에서 4000~4999 `0.0937`로 증가하므로 정책이 회전을 전혀 무시하는 것은 아니지만, 실제 error metric은 여전히 크다.

과거 공식 TERM50 5K endpoint yaw `0.935`와 비교하면 H-012 endpoint `1.897`은 거의 두 배다. 다만 실행 환경/시점 차이로 인과 효과를 확정할 수는 없다. 그래도 **TERM100을 바로 승격하기 어렵게 만드는 가장 강한 negative evidence**다.

## 5.3 Stop behavior

`rel_standing_envs=0.02`이므로 일부 standing command는 학습에 포함되지만 zero-command drift, stop 후 흔들림, restart 안정성 scalar가 없다. 영상/evaluator도 없다. 따라서 stop behavior는 **판단 불가**다.

---

# 6. Stability Analysis

## 6.1 Fall / survival

| 구간 | base-contact | timeout | episode length |
|---|---:|---:|---:|
| 500~999 | 32.33% | 67.69% | 785.18 |
| 1000~1999 | 27.93% | 72.09% | 798.84 |
| 2000~2999 | 28.12% | 71.89% | 793.75 |
| 3000~3999 | 27.49% | 72.52% | 801.24 |
| 4000~4499 | 27.30% | 72.71% | 804.97 |
| 4500~4999 | **26.68%** | **73.34%** | **811.68** |
| endpoint | 26.69% | 73.34% | 816.45 |

초기 recovery 이후 base-contact는 1K 전후부터 약 28%대로 들어가고, 이후 개선 폭은 작다. 즉 TERM100의 핵심 survival 성격은 비교적 일찍 형성되고, 후반 3K 동안은 terrain와 tracking refinement가 주로 진행된다.

`report.html`의 “낙상률 26.5%”는 마지막 10회 평균 `26.47%`와 일치한다. 이 값은 낮다고 할 수는 없지만, timeout이 약 73%이고 high-terrain curriculum을 유지하므로 **정책이 전혀 안정되지 않은 상태**라고도 볼 수 없다.

## 6.2 Orientation / gait proxy

reward component 평균 변화는 다음과 같다.

- `flat_orientation_l2`: 500~999 `-0.0187` → 4000~4999 `-0.0130` — 후반 자세 penalty 감소 방향.
- `feet_slide`: `-0.0655 → -0.0512` — 후반 sliding penalty 감소 방향.
- `feet_air_time`: `0.00442 → 0.00898` — swing phase 보상 증가.
- `action_rate_l2`: `-0.0703 → -0.0827` — 초기보다 동작 변화량 penalty는 더 커졌지만 1K 이후에는 거의 plateau.
- `dof_acc_l2`: 후반에도 약 `-0.064` 수준 — 동적 움직임 비용이 남음.

이 조합은 “완전히 경직되어 움직이지 않는 안정 정책”보다는 **실제 gait를 수행하면서 점차 slip/orientation을 정리한 정책**과 더 잘 맞는다. 다만 영상이 없으므로 hopping, dragging, oscillation 같은 구체적 gait morphology는 확인할 수 없다.

## 6.3 Terrain capability

후반 last-500 terrain `5.763`은 강한 내부 curriculum 성과다. 그러나 per-terrain scalar가 없으므로 아래는 판단 불가다.

- boxes만 강한지
- stairs / inverted stairs 통과율
- rough에서 foot slip 증가 여부
- slope up/down 비대칭
- terrain 진입/이탈 recovery

특히 boxes proportion이 30%로 가장 높기 때문에 aggregate terrain progression을 모든 지형의 동일한 숙련도로 해석하면 안 된다.

## 6.4 Push recovery

학습 설정에 push perturbation이 활성화되어 있지 않고 evaluator/video도 없다. **밀침 회복 능력은 판단 불가**다.

---

# 7. Reward Component Analysis

아래는 구간별 평균이다. reward weight가 바뀐 `termination_penalty` 때문에 `Train/mean_reward` 절댓값을 다른 penalty run과 직접 비교하지 않는다.

| Component | 0~499 | 500~999 | 1000~1999 | 2000~2999 | 3000~3999 | 4000~4999 |
|---|---:|---:|---:|---:|---:|---:|
| track lin | 0.1550 | 0.2706 | 0.2930 | 0.2986 | 0.3079 | **0.3144** |
| track yaw | 0.0478 | 0.0681 | 0.0731 | 0.0778 | 0.0856 | **0.0937** |
| termination | -0.0602 | -0.0398 | -0.0364 | -0.0374 | -0.0363 | **-0.0353** |
| feet air | 0.00255 | 0.00442 | 0.00565 | 0.00695 | 0.00814 | **0.00898** |
| flat orientation | -0.0159 | -0.0187 | -0.0168 | -0.0146 | -0.0134 | **-0.0130** |
| action rate | -0.0295 | -0.0703 | -0.0847 | -0.0842 | -0.0838 | **-0.0827** |
| feet slide | -0.0603 | -0.0655 | -0.0586 | -0.0546 | -0.0526 | **-0.0512** |
| hip deviation | -0.0378 | -0.0472 | -0.0459 | -0.0445 | -0.0430 | **-0.0422** |
| arms deviation | -0.0803 | -0.1074 | -0.1106 | -0.1074 | -0.1049 | **-0.1049** |

## 7.1 무엇을 배웠는가

가장 일관된 변화는 다음 구조다.

1. **생존 회복**: termination component와 base-contact가 초기 극단 상태에서 빠르게 개선.
2. **terrain 재확장**: survival이 어느 정도 확보된 뒤 curriculum이 0→5.5 이상으로 재상승.
3. **linear tracking 점진 개선**: track-lin reward 증가와 XY error 감소가 일치.
4. **yaw는 늦은 개선**: track-yaw reward는 계속 증가하지만 yaw error가 끝까지 높음.
5. **gait dynamism 증가 후 정리**: action-rate/acc 비용은 초기보다 커졌지만 1K 이후 안정화되고, 동시에 slip/orientation penalty는 완화됨.

즉 정책은 TERM100 아래에서 “최대한 움직이지 않고 생존”만 배운 것이 아니라, **terrain을 재등반할 수 있는 보행을 학습**했다. 그러나 행동 우선순위가 survival 쪽으로 강하게 치우치면서 **회전 명령 추종이 충분히 따라오지 못한 specialization** 가능성이 있다.

## 7.2 Trade-off 정황

과거 TERM50 endpoint 대비 TERM100은 historical comparison에서 survival은 소폭 좋아지고 yaw는 크게 악화된다. 내부 trajectory에서도 survival은 대략 1~2K 사이에 plateau에 가까워진 반면 yaw는 5K까지 계속 느리게 개선된다. 이는 `termination_penalty=-100`이 초기/중기 optimization에서 survival을 강하게 우선하게 만들어 tracking 특히 yaw 학습을 지연시켰을 가능성과 부합한다.

단, 이것은 **가설**이다. 동일 host/source fresh TERM50 control이 없으므로 인과관계로 확정하지 않는다.

---

# 8. PPO / Numerical Stability

## 8.1 Value loss

| 통계 | 값 |
|---|---:|
| median | **0.00724** |
| p95 | **0.00920** |
| p99 | **0.01028** |
| max | **0.49523 @ iter 1** |
| `>0.1` | 6회, 모두 iter 1~6 |
| `>0.5` | 0회 |
| `>1` | **0회** |
| `>5` | 0회 |
| `>10` | 0회 |

초기 1~6 iteration을 제외하면 value loss는 매우 낮고 안정적이다. 과거 Go2 long-run에서 관찰된 반복적 value-loss spike/발산 패턴과는 전혀 다르다.

## 8.2 Surrogate / entropy / learning rate

- surrogate loss: 후반 약 `-0.014` 수준에서 안정.
- entropy: 초기 `26.98`, max `30.07 @1171`, last-500 mean `28.59`.
- learning rate: adaptive schedule로 early max `0.003375 @6`, min `1e-5 @1999`, last-500 mean 약 `2.15e-4`.
- NaN/Inf: TensorBoard/console/checkpoint 직접 검사에서 없음.
- 실제 KL scalar는 **로그에 없음**. `desired_kl=0.01` 설정만 확인되므로 KL trajectory는 판단 불가.
- gradient norm scalar도 없음.

## 8.3 Action std — report 경고 재해석

mean std는 `1.001`에서 시작해 min `0.891 @59`, max `1.631 @1961`, endpoint `1.551`이다. report는 이를 “무작위성이 안 줄어 거의 학습이 안 됨”으로 경고하지만, 이 해석은 이번 데이터와 맞지 않는다.

최종 checkpoint의 19차원 std parameter는:

- min `0.257`
- median `2.473`
- max `2.662`
- `<0.5`인 action dimension: **5/19**
- `>2.0`인 dimension: **10/19**

즉 scalar mean `1.55`는 모든 관절이 비슷하게 높은 것이 아니라 **action dimension별로 매우 이질적인 exploration scale**의 평균이다. 동시에 terrain `5.7+`, timeout `73%`, episode length `800+`, tracking improvement가 존재하므로 std 하나로 “학습 실패”라고 판정할 수 없다.

반대로 std가 높은 사실 자체를 무시해서도 안 된다. deterministic play/export에서 행동이 안정적인지 확인할 video/evaluator가 없기 때문에 **정책의 실제 실행 변동성은 미확인**이다.

## 8.4 Checkpoint tensor 건전성

51개 checkpoint를 직접 load해 actor, critic, optimizer 내부 floating tensor를 검사했다.

- **51/51 finite**
- std parameter 모두 양수
- final까지 NaN/Inf 없음

따라서 H-012는 numerical failure가 아니라 **behavioral objective trade-off** 문제로 보는 것이 맞다.

## 8.5 Throughput / GPU

Late training 평균은 대략:

- collection time `~0.71 s`
- learning time `~0.086 s`
- total FPS last-500 `~123.5k`

2초 간격 GPU telemetry에서 training active 구간은:

- GPU util mean `52.4%`
- VRAM `5274 MiB` 고정
- power mean `160.2 W`
- temperature mean `49.1°C`, max `51°C`

실행 성능은 안정적이다. GPU utilization이 100%에 가깝지 않지만 CPU/physics/host 병목 telemetry가 충분하지 않아 원인을 특정하지 않는다. 정책 품질 판단과도 직접 관련이 없다.

---

# 9. Checkpoint Analysis

## 9.1 자동 best 연결

- raw `Train/mean_reward` global peak: **`0.374539 @ iter 4671`**
- finalizer 선택: nearest saved checkpoint **`model_4700.pt`**
- exported `model_best.pt` SHA-256: `f8732e4f1bee1da324472c465675c353c1a40b273b55d872932db2b346411f52`
- `model_4700.pt` SHA-256: 동일
- final `model_4999.pt` SHA-256: `6fe0559d2ac0dfb24867bd482dc66a8181f3995ca127516fdb5736aec54bb104`

이번 run은 fresh 5K이며 scalar count 5K이므로 selector의 raw/report mismatch는 없다.

## 9.2 `model_best` ≠ 실제 최적 정책

단일 reward spike `4671` 주변 100-step 평균과 late window를 비교하면:

| Window | reward mean | terrain | base-contact | episode | XY | yaw |
|---|---:|---:|---:|---:|---:|---:|
| 4621~4720 (reward peak 주변) | -0.305 | 5.752 | 26.78% | 809.0 | 0.4085 | 1.9056 |
| 4700~4799 | -0.303 | **5.799** | 26.98% | 810.2 | **0.4094** | 1.9057 |
| 4900~4999 | -0.224 | 5.737 | **26.22%** | **815.1** | 0.4142 | **1.9053** |

후반 final window는 terrain/XY가 약간 나쁘지만 survival/episode가 약간 좋고 yaw는 사실상 동일하다. **여러 핵심 지표가 함께 붕괴한 late regression은 없다.**

또한 actor parameter는 4700→4999 사이 계속 변했다. actor float parameter의 relative L2 차이는 약 `13.3%`로, 두 checkpoint가 byte alias가 아니라 실제로 다른 정책 상태임을 확인한다. 이 값 자체는 성능 지표가 아니다.

### 현재 checkpoint 판정

- `model_4700`: **자동 reward-best 후보**
- `model_4999`: **final training representative 후보**
- 어느 쪽이 실제 tracking/stability/terrain 행동에서 우월한지는 **판단 불가**
- fixed evaluator + 동일 command/terrain play가 없으므로 “4700이 제출 후보” 또는 “4999가 더 좋다”를 확정하지 않는다.

---

# 10. Video / Behavioral Analysis

이번 archive에는 `policy.pt`, `policy.onnx`, MP4, fresh play evidence가 없다. 따라서 아래 항목은 직접 시각 검증하지 못했다.

| 행동 항목 | 상태 |
|---|---|
| upright posture | scalar 정황은 긍정적, **영상 확인 불가** |
| command 방향 이동 | aggregate tracking은 존재, **영상 확인 불가** |
| stop / restart | **판단 불가** |
| turning morphology | yaw error가 높아 우려, **영상 확인 불가** |
| hopping | **판단 불가** |
| one-leg hold | **판단 불가** |
| foot dragging / sliding | feet-slide scalar 개선 정황, **영상 확인 불가** |
| body oscillation | orientation/ang-vel scalar 일부 있음, **영상 확인 불가** |
| abnormal survival posture | high terrain + base-contact로 가능성 낮아 보이나 **배제 불가** |
| per-terrain traversal | **판단 불가** |
| recovery after obstacle/push | **판단 불가** |

수치와 행동이 충돌하는지를 검사할 video가 없다는 점은 이번 보고서의 가장 큰 한계 중 하나다.

---

# 11. Baseline / Parent Comparison

## 11.1 Parent comparison

이 run은 **fresh**이므로 parent checkpoint가 없다. 따라서 resume lineage나 curriculum reset 영향은 없다.

## 11.2 Historical TERM50 5K 비교

프로젝트 핵심팩의 공식 H1 TERM50 5K는 seed42/4096 env/5K였고 endpoint가 다음과 같다. 현재 H-012는 PERSONAL L40S이고 과거 TERM50은 OFFICIAL RTX5080이며 실행 시점/source provenance도 완전히 동일하다고 증명되지 않으므로 **directional historical comparison**으로만 본다.

| Metric | 공식 TERM50 5K endpoint | H-012 TERM100 endpoint | 변화 | 해석 |
|---|---:|---:|---:|---|
| terrain | 5.825 | 5.740 | -0.085 | 더 강한 penalty가 terrain을 추가로 올렸다는 증거 없음 |
| base-contact | 28.93% | **26.69%** | **-2.24 pp** | survival 방향 개선 |
| timeout | 71.07% | **73.34%** | +2.27 pp | survival 방향 개선 |
| episode length | 774.1 | **816.45** | +42.35 | survival 방향 개선 |
| XY error | 0.378 | 0.402 | +0.024 | 소폭 악화 |
| yaw error | **0.935** | **1.897** | **+0.962** | 큰 악화, 핵심 문제 |
| action std | 1.296 | 1.551 | +0.255 | scalar만으로 품질 판정 금지 |

가장 중요한 점은 **안정성 이득은 modest하지만 yaw 손실은 매우 크다**는 것이다. 이 비교가 같은 조건 paired run이었다면 TERM100은 상당히 부정적으로 평가할 만하다. 그러나 현재는 environment/provenance confound 때문에 이를 causal proof로 승격하지 않는다.

## 11.3 Historical PERSONAL baseline(-5) 5K 비교

과거 개인 L40S baseline 5K endpoint는 terrain `5.054`, base-contact `33.21%`, timeout `66.79%`, episode `742.97`, XY `0.342`, yaw `0.652`였다.

H-012는 그보다 terrain/survival이 강하지만 XY와 yaw tracking은 더 나쁘다. 이는 `termination_penalty` 강화 계열에서 반복되는 **stability ↔ tracking trade-off 정황**과 일치한다. 역시 실행 시점/source가 동일하지 않아 직접 인과 비교는 아니다.

## 11.4 공식 점수와의 연결

H-012 자체에는 공식 evaluator가 없다. 과거 공식 TERM50 제출은 시뮬레이션 `56.37/70`이었고 7개 시나리오가 77.8~82.1%로 고르게 분포했다. H-012의 내부 yaw error가 높다는 이유만으로 공식 회전 점수가 자동으로 크게 떨어진다고 환산할 수 없다. **내부 metric 병목과 공식 scoring 병목은 분리**한다.

---

# 12. Tracking vs Stability Trade-off

현재 evidence에서 정책 성격은 **“Stability 강함 / Tracking 특히 yaw 약함”**에 가깝다.

Historical TERM50을 참고하면 4분면 중 **Tracking ↓ / Stability ↑** 정황이 가장 강하다. 다만 strict paired control이 없으므로 확정 분류가 아니라 **현재 최선의 해석**이다.

### Stability 쪽 근거

- high terrain last-500 `5.763`
- base-contact last-500 `26.68%`
- timeout `73.34%`
- episode length `811.68`
- terrain retreat 뒤 재진입 성공
- no numerical collapse

### Tracking 쪽 근거

- XY는 후반 `0.41`대로 개선했지만 historical TERM50보다 약간 나쁨
- yaw는 후반 `1.91`로 명확한 병목
- stop/forward/lateral 세분화 evidence 없음

따라서 “TERM100이 더 안정적이니 전체적으로 더 좋은 정책”이라고 요약하면 안 된다.

---

# 13. Local Optimum / Reward Hacking Check

| 가능성 | 판정 | 근거 |
|---|---|---|
| 움직이지 않고 생존 | **강한 반증** | terrain 5.7+, track-lin reward 증가, XY error 개선 |
| 비정상 자세로 termination 회피 | **낮은 정황 / 영상 필요** | base-contact 26.7%, orientation penalty 후반 개선, high terrain. 영상 없으므로 완전 배제 불가 |
| hopping | **판단 불가** | feet-air reward는 낮은 정상 범위지만 영상 없음 |
| 한 발 오래 들기 | **판단 불가** | 영상 없음 |
| sliding | **심각한 악화 증거 없음** | feet-slide penalty가 후반 덜 negative |
| command 무시 | **부분 문제** | XY는 추종하지만 yaw error 큼 |
| terrain 회피 | **강한 반증** | curriculum 0→5.7 재상승 |
| 지나친 소극성 | **일부 가능성** | TERM100 의도와 yaw 손실 정황. 하지만 실제 이동은 학습됨 |
| 한 reward만 과최적화 | **가능성 있음** | stability 이득 대비 yaw trade-off가 강함 |
| episode length만 긴 정책 | **반증 있음** | terrain 및 tracking component도 함께 개선 |

가장 현실적인 reward-hacking 우려는 “완전히 멈춰 버티기”가 아니라 **낙상 회피를 우선해 회전/공격적 tracking을 충분히 학습하지 않는 보수적 specialization**이다.

---

# 14. 새로운 발견 / 가설

## 14.1 Curriculum retreat가 실제 학습의 핵심 단계다 — 강한 근거

보고서 endpoint만 보면 terrain이 3.4→5.74로 단순 증가한 것처럼 보이지만 실제로는 25 iter 만에 0으로 떨어졌다. 이 run의 성패는 **초기 high-level 유지가 아니라 curriculum이 난도를 낮춰 준 뒤 재학습할 수 있었는가**에 달려 있었다.

향후 1K 이하 screening에서 terrain이 초기에 떨어지는 것만으로 가설을 기각하면 delayed learning을 놓칠 수 있다.

## 14.2 TERM100은 “terrain ceiling”을 높이기보다 survival bias를 강화했을 가능성 — 중간 근거

과거 TERM50보다 survival은 소폭 좋아졌지만 terrain은 더 높지 않고 yaw는 크게 악화됐다. 따라서 -100의 추가 penalty는 난도 확장보다 **낙상 회피 우선순위**에 더 많은 영향을 줬을 가능성이 있다.

## 14.3 Numerical instability가 병목은 아니다 — 강한 근거

value loss, checkpoint finite, console, optimizer state 모두 안정적이다. 다음 실험에서 PPO/learning rate를 건드리는 것은 현재 문제를 겨냥한 실험이 아니다. 병목은 reward trade-off와 behavior validation이다.

## 14.4 `mean_std` report 경고는 이번 정책의 품질을 요약하지 못한다 — 강한 근거

std=1.55가 높지만 action dimensions가 bimodal하게 나뉘고 terrain/survival/tracking이 실제로 학습됐다. `std≈1 → 거의 학습 안 됨`이라는 report 문구를 그대로 적용하면 H-012 trajectory와 모순된다. 다만 deterministic behavior quality는 video가 필요하다.

## 14.5 4700 자동 best는 robust checkpoint selection 근거가 약하다 — 중간 근거

reward peak는 단일 step이고 주변 100-step 평균 reward는 음수이며 final window와 큰 성능 차이가 없다. late joint collapse도 없다. 따라서 checkpoint selection을 reward peak alias 하나로 끝내면 안 된다.

---

# 15. Key Findings

1. **H-012는 실행/증거 측면에서는 매우 깨끗한 fresh 5K PERSONAL run이다.** 51 checkpoints, full TensorBoard, full console, GPU telemetry가 있고 73/73 manifest가 맞는다.
2. **정책은 초기 curriculum을 유지하지 못하고 terrain 3.44→0으로 붕괴한 뒤 다시 5.7대로 올라왔다.** delayed learning/recovery가 핵심이다.
3. **TERM100은 생존형 local optimum으로 멈추지 않았다.** high terrain, tracking reward, slip/orientation 개선이 함께 나타난다.
4. **가장 큰 병목은 yaw tracking이다.** last-500 yaw error `1.91`, endpoint `1.897`로 high terrain/stability에 비해 크게 뒤처진다.
5. **Stability는 먼저 plateau, yaw는 늦게 개선된다.** 2K 이후 survival은 27~28% base-contact 부근에서 큰 변화가 없지만 yaw는 5K까지 계속 감소한다.
6. **PPO 수치 안정성은 매우 좋다.** value loss p99 `0.0103`, >1 없음, 51 checkpoint 전부 finite. 이번 문제는 발산이 아니다.
7. **자동 `model_best=model_4700`은 selector 로직상 정상이나 실제 정책 최적성은 미확인이다.** final 4999까지 joint collapse가 없고 evaluator/video가 없다.
8. **Historical TERM50 대비 TERM100은 survival 이득보다 yaw 손실이 훨씬 커 보인다.** 하지만 현재 비교는 host/source가 맞지 않아 causal proof가 아니다.
9. **이번 run만으로 forward/lateral/stop/push/per-terrain capability는 분리할 수 없다.** 관련 metric/video/evaluator가 없다.
10. **다음 정보 효율 최우선은 TERM50 matched control이다.** 새로운 reward를 또 바꾸면 TERM100 효과를 영원히 분리하기 어렵다.

---

# 16. Final Decision

## **HOLD**

### 이유

H-012는 실패 run이 아니다. high-terrain locomotion과 survival을 학습했고, numerical health도 좋다. 따라서 `REJECT`로 버릴 정도의 붕괴 evidence는 없다.

그러나 `PROMOTE`하기에도 근거가 부족하다.

- yaw tracking이 매우 약함
- historical TERM50 대비 survival gain은 작고 yaw loss는 큼
- 같은 host/source의 TERM50 5K matched control 없음
- policy/play video 없음
- fixed evaluator 없음
- 공식 score 없음
- single seed

따라서 현재 의미는 **“TERM100이 학습 가능한 안정성 강한 영역임을 확인한 screening/anchor”**까지다. “TERM50보다 더 좋은 정책” 또는 “다음 공식 제출 후보”로 승격하지 않는다.

---

# 17. Next Experiment

## 17.1 1순위 — Matched TERM50 fresh 5K control

다음 학습은 새 값을 탐색하는 실험이 아니라 **인과 비교를 완성하는 control**이어야 한다.

| 항목 | 제안 |
|---|---|
| Robot | H1 |
| Environment | PERSONAL L40S, H-012과 동일 host/runtime 가능한 범위 |
| Training mode | **fresh**, resume 금지 |
| Reward 변경 | `termination_penalty: -100 → -50`만 변경 |
| 나머지 reward | H-012와 동일 |
| Seed | 42 |
| Num envs | 4096 |
| Iterations | 5000 |
| Headless / camera | H-012과 동일: headless, training camera off |
| PPO/env/task source | 동일 hash 확인 |
| Evidence | full console, raw tfevents, 51 checkpoints, source hash, GPU telemetry |
| 평가 | 마지막 500 평균 + 4700/4999 성격 비교 + 동일 fixed evaluator/play |

### 왜 이 실험이 가장 정보 효율적인가

현재 가장 중요한 미확정 질문은 “`-100`의 survival gain과 yaw loss가 penalty 자체 때문인가?”이다. TERM75나 yaw reward를 새로 건드리면 세 번째 조건이 생길 뿐 이 질문은 풀리지 않는다. 동일 환경 TERM50 control 하나가 생기면 H-012의 인과 해석 가치가 크게 올라간다.

### 비교할 핵심 metric

1. last-500 base-contact / timeout / episode length
2. last-500 terrain 및 terrain 5/5.5 도달 시점
3. last-500 XY / yaw error
4. reward component: track-lin / track-yaw / termination / action-rate / feet-slide
5. value loss p95/p99/max와 std 분포
6. `model_4700` 계열과 final checkpoint의 fixed evaluator 결과
7. 동일 command sequence play에서 turning, stop, terrain entry/recovery

### 사전 decision band — 통계검정이 아니라 운영용 effect-size 기준

TERM100을 TERM50보다 유망하다고 볼 최소 조건을 다음처럼 미리 정하는 것을 권장한다.

- base-contact가 TERM50보다 **≥2 percentage points 낮음**
- episode length가 **≥20** 높음
- terrain last-500이 **0.1 이상 낮아지지 않음**
- XY error 악화가 **≤0.02**
- yaw error 악화가 **≤0.20**
- video/evaluator에서 stop/turning의 명백한 행동 악화가 없음

이 threshold는 통계적 유의성 기준이 아니라, 현재 H-012와 historical TERM50 사이의 차이를 기준으로 만든 **실험 운영용 practical band**다. multi-seed가 없으므로 작은 차이는 동률로 취급해야 한다.

현재 historical comparison처럼 `base-contact 약 -2.2pp`를 얻는 대신 `yaw +0.96`이 재현된다면 **TERM100은 REJECT 방향**이다.

## 17.2 2순위 — TERM75 fresh 5K

Matched TERM50에서 `-50`이 tracking은 좋지만 survival이 확실히 약하고, `-100`이 survival은 좋지만 yaw가 명확히 나쁘다는 trade-off가 동일 환경에서 재현될 때만 `-75`를 중간점으로 시험한다.

`-75` 실험 전에는 다른 reward를 동시에 바꾸지 않는다. `track_ang_vel_z_exp` 강화와 TERM75를 같이 하면 어느 변화가 yaw를 회복시켰는지 알 수 없게 된다.

---

# 18. Confidence & Limitations

## 18.1 강한 근거

- run identity의 PERSONAL/fresh/5K/seed42/4096/headless
- 실제 reward `termination=-100` 및 나머지 student reward unchanged
- exit0 / finalizer completed / validation PASS
- archive 73/73 checksum
- 51 checkpoint 보존과 모두 finite
- TensorBoard 0~4999 전체 trajectory
- terrain collapse/recovery milestone
- last-window terrain/survival/XY/yaw
- value loss numerical stability
- `model_best == model_4700` hash identity
- final `model_4999` 별도 정책

## 18.2 중간 근거

- TERM100이 survival을 더 우선하고 yaw를 희생했다는 해석
- 4700보다 final 4999도 충분히 경쟁력 있다는 해석
- 보수적 specialization 가능성

이들은 내부 metric과 historical comparison에 의해 지지되지만 같은 조건 paired control / evaluator가 없어 인과 증명은 아니다.

## 18.3 약한 정황

- 실제 gait가 부드럽고 upright일 것이라는 추론
- specific terrain에서 잘 통과할 것이라는 추론
- high action std가 특정 관절군의 exploration을 의미한다는 행동 해석

영상/관절명 mapping/evaluator가 없어 제한적이다.

## 18.4 판단 불가

- forward vs lateral 개별 tracking
- zero-command drift / stop-go
- push recovery
- terrain별 성공률
- hopping / foot dragging / oscillation
- deterministic policy play quality
- official H1 score
- multi-seed 일반화
- TERM100의 TERM50 대비 causal effect
- 4700 vs 4999 실제 evaluator 우열

---

# 19. Evidence Provenance

## H-012 archive에서 직접 사용한 원본

- `metadata.json`
- `validation.json`
- `SHA256SUMS`
- `command.txt`
- `console.log`
- `native_run/events.out.tfevents.*`
- `native_run/params/env.yaml`
- `native_run/params/agent.yaml`
- `native_run/git/IsaacLab.diff`
- `source/humanoid_rewards.py`
- `source/identity.json`
- `collected/provenance.json`
- `collected/exported/env.yaml`
- `collected/exported/model_best.pt`
- `collected/exported/report.html`
- `checkpoints/model_0.pt` ... `model_4999.pt`
- `watcher.log`
- `system/nvidia_smi_before.txt`
- `system/nvidia_smi_during.csv`
- `system/nvidia_smi_after.txt`
- `system/runtime.txt`

## Historical comparison에 사용한 프로젝트 핵심팩

- `00_START_HERE_CONTEXT_AND_MAP(20260921-031145).md`
- `06_HUMANOID_TRAINING_CODE(20260921-031145).md`
- `12_2026_UNIFIED_REGULATIONS(20260921-031144).md`
- `13_H1_OFFICIAL_SERVER_BASELINE_EVIDENCE(20260921-031146).md`
- `14_H1_NEXT_RUN_PARAMETER_COMPARISON(20260921-031146).md`
- `16_EXPERIMENT_EXPORT_AND_TENSORBOARD(20260921-031145).md`
- `18_H1_FINALIZE_REPORT_LIMITATIONS(20260921-031144).md`
- `19_ISSACSIMZ_EXTERNAL_EVIDENCE_CLI(20260921-031144).md`

Historical 자료는 현재 H-012의 raw evidence보다 낮은 우선순위로 사용했고, host/source/official-personal 차이가 있는 비교에는 모두 limitation을 붙였다.

---

# 최종 답변 — 8개 질문

| 질문 | 답변 |
|---|---|
| 1. 이 정책은 무엇을 배웠는가? | 초기 curriculum 붕괴 후 쉬운 지형에서 survival/보행을 재학습하고 terrain 5.7대까지 다시 올라가는 안정 지향 locomotion을 배웠다. Linear tracking도 개선했지만 yaw는 불완전하다. |
| 2. 이전 정책보다 무엇이 실제로 좋아졌는가? | Historical TERM50/B0 대비 survival 방향(base-contact↓, timeout/episode↑)의 이득 정황이 있다. 다만 same-condition causal proof는 아니다. |
| 3. 무엇을 잃었는가? | 가장 강한 정황은 yaw tracking 손실이다. TERM50 historical endpoint `0.935` 대비 H-012 `1.897`. XY도 소폭 나쁘다. |
| 4. 언제 중요한 변화가 일어났는가? | terrain 0 @25, recovery 시작 ~215, 초기 terrain 재돌파 671, terrain 5 @1762, 5.5 @2535, high-terrain plateau ~3K 이후, reward peak 4671. |
| 5. 높은 지표가 실제 행동 개선인가? | terrain/survival은 강한 내부 개선이지만 video가 없어 실제 gait morphology와 scenario 성공률은 미확인이다. |
| 6. 현재 가장 큰 병목은? | **Yaw/turning tracking**, 그 다음은 행동/evaluator evidence 부족. Numerical stability는 병목이 아니다. |
| 7. 이 가설은 계속 가치가 있는가? | **HOLD**. TERM100은 viable하지만 TERM50보다 전체적으로 낫다는 증거가 없다. |
| 8. 다음 한 번으로 가장 많은 정보는? | **동일 환경 TERM50 fresh 5K matched control**. 이것이 TERM100의 실제 causal trade-off를 분리한다. |

