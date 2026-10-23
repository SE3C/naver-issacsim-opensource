# Go2 LINTRACK-125 OFFICIAL fresh 7.5K vs fresh 3K 심층 분석

- 분석일: 2026-09-30
- Robot: Go2 / `Quadruped-v0`
- Experiment: `exp-go2-planar-tracking-terrain-progression`
- 현재 표기: `LINTRACK-125`
- legacy alias: `G-001 / LIN-TRACK / G2` — 원문 검색용으로만 사용
- A: `20260929-154342-go2-lintrack-125-fresh7500-official`
- B: `20260928-230114-go2-lintrack125-fresh3k-r5-official`
- 입력 원본:
  - A: `20260929-154342-go2-lintrack-125-fresh7500-official-download.tar.gz.part1` + `.part2`
  - B: `20260928-230114-go2-lintrack125-fresh3k-r5-official-download.tar(3).gz`
- 주의: 요청된 **6지형 영상 묶음은 이번 입력에 포함되어 있지 않다.** 따라서 학습 원본 비교는 완료했지만 6지형 실제 행동 비교는 관찰 불가로 남긴다.

---

## 1. 결론 요약

### 세 질문에 대한 답

**1) 이번 7.5K 정책은 목표 행동을 실제로 얼마나 수행하는가?**

실제 6지형 행동 성공 정도는 현재 자료만으로 확정할 수 없다. A 학습 archive에는 MP4가 0개이고, B archive에도 MP4가 0개다. canonical Release를 추가 확인했을 때 B에는 단일 loose `play_video.mp4`가 있지만 6지형 suite/manifest가 아니며, A에는 MP4가 없다. 따라서 지형 접근·통과·stall·sliding·recovery를 본 것처럼 서술하지 않는다.

다만 **학습 분포 내부의 정량 proxy**는 7.5K에서 분명히 좋아졌다. late-500을 같은 정의로 비교하면:

- curriculum terrain 평균: **5.282 → 5.913**
- XY velocity error: **0.736 → 0.567** (`-0.169`, 약 `-23.0%`)
- training base-contact termination: **9.93% → 6.23%** (`-3.70%p`)
- timeout fraction: **90.07% → 93.77%** (`+3.70%p`)
- mean episode length: **948.6 → 968.7 steps** (20초 horizon의 최대 1000 steps)
- yaw error: **0.396 → 0.399**로 사실상 개선 없음

즉 이 단일 seed/config trajectory에서는 3K 이후 추가 학습이 **더 어려운 curriculum에서 더 낮은 XY 추종 오차와 더 적은 base-contact 종료**로 이어졌다. 하지만 이는 fixed evaluator의 terrain completion이나 공식 Survival/Tracking 점수가 아니다.

**2) A/B 차이 중 무엇을 설정 변경 효과로 해석할 수 있는가?**

A/B 사이에는 reward 설정 변경이 없다. 두 Run은 모두 fresh, seed 42, 4096 env, 같은 source/PPO/env/reward를 사용한다. 구조적으로 확인된 차이는 `agent.max_iterations: 3000 → 7500`과 run별 `log_dir`뿐이다.

더 강하게, **A의 iteration 0–2999는 B와 학습 궤적 자체가 동일하다.**

- raw TensorBoard의 substantive scalar 22개(Perf와 wall-time용 tag 제외)가 0–2999에서 **전 점 exact match**
- 0–2950의 50-step checkpoint 60개 SHA가 **60/60 동일**
- 선택 검증으로 실제 archive bytes를 다시 SHA-256 계산한 `model_2000.pt`, `model_2950.pt`도 양쪽이 각각 완전히 동일

따라서 3K와 7.5K의 후기 차이는 이 실험의 한 seed/config 안에서는 **추가 4.5K 학습에 따라 같은 trajectory가 더 진행된 결과**로 해석하기에 매우 강한 근거가 있다.

반대로 `track_lin_vel_xy_exp: 1.0 → 1.25`라는 **LINTRACK-125 reward 변경 자체의 효과**는 이 A/B 비교로는 판단할 수 없다. 양쪽 모두 이미 1.25이기 때문이다. 동일 길이의 unchanged BASE fresh control이 필요하다. 기존 OFFICIAL BASE 1K는 길이가 달라 맥락 참고는 가능하지만 3K/7.5K의 직접 reward control은 아니다.

**3) 현재 내려야 할 결정과 우선 해소할 불확실성은?**

- 실행: **A COMPLETE/PASS, B COMPLETE/PASS**
- 학습 길이 효과: **확인됨** — 3K→7.5K에서 terrain/XY/base-contact proxy 개선
- `LINTRACK-125` reward 인과 가설: **HOLD** — 같은 길이 BASE control 부재
- 7.5K 정책 자체: **fixed paired behavior evaluation 단계로 PROMOTE**, 채택/제출 우위 판정은 HOLD
- 대표 checkpoint 1순위: **`model_7050.pt`** — automatic reward-best이면서 7050 주변이 terminal 7450 주변보다 terrain/yaw/base-contact/episode length까지 더 균형적이다.
- `model_7450.pt`: terminal-state comparator로 보존. 현재 수치상 붕괴는 아니지만 7050 이후 약한 late regression이 있다.
- 다음 한 번의 행동: **새 학습 없이** 기존 `model_7050.pt`와 B의 terminal `model_2950.pt`를 동일 command/terrain/difficulty/seed/evaluator에서 paired 평가하고, 같은 checkpoint identity가 붙은 6지형 영상을 함께 만든다. 이 한 번으로 “학습 proxy 개선이 실제 traversal/추종/접촉 안정으로 이어졌는가?”를 가장 싸게 판별할 수 있다.
- 그 후 reward 자체의 인과효과가 필요하면 BASE `track_lin_vel_xy_exp=1.0` fresh control을 동일 3K 조건으로 추가하는 것이 다음 단계다.

---

## 2. 원본 무결성, Run identity, lineage

### 2.1 업로드 파일과 canonical Release 대조

A의 두 분할 파일을 순서대로 결합했다.

- part1: `499,000,000 bytes`
- part2: `481,852,211 bytes`
- 합계: `980,852,211 bytes`
- 결합 archive SHA-256:  
  `89449fe89d12107e9dcea0a67cd5d78b1611850f86d1bbeaf8b0611bd55bf13c`

이는 canonical OFFICIAL raw Release `official-go2-20260929-lintrack-125-fresh7500`의 asset size/digest와 정확히 일치한다.

B archive:

- size: `403,029,912 bytes`
- SHA-256:  
  `a20df5f67bbc65c286ba06c082d20ce47c043505eb41dfbc521aeab19d56ca00`

이 역시 `official-go2-20260928-lintrack-125-fresh3k-r5` Release의 asset digest와 정확히 일치한다.

각 outer archive 안의 nested evidence archive도 sidecar와 대조했다.

| Run | nested archive SHA-256 | embedded sidecar |
|---|---|---|
| B 3K | `d530117480b6575ad6932c7467a92bad462e4cb38c6eb95a64905e5ea9e7f607` | 일치 |
| A 7.5K | `029cbfbb98389ded2fa0fa25375de472c07cbab5c888f8648468770b860967f9` | 일치 |

### 2.2 실행 identity

| 항목 | B: fresh 3K | A: fresh 7.5K |
|---|---|---|
| Evidence Run ID | `20260928-230114-go2-lintrack125-fresh3k-r5-official` | `20260929-154342-go2-lintrack-125-fresh7500-official` |
| Environment | OFFICIAL | OFFICIAL |
| Operation | train | train |
| Fresh/resume | fresh | fresh |
| Parent Run | 없음 | 없음 |
| Source checkpoint | 없음 | 없음 |
| seed | 42 | 42 |
| num_envs | 4096 | 4096 |
| requested iterations | 3000 | 7500 |
| 실제 console iteration | `0–2999` | `0–7499` |
| rollout/env/iter | 24 steps | 24 steps |
| transitions/iter | 98,304 | 98,304 |
| 총 transitions | 294,912,000 | 737,280,000 |
| wall time | 2:54:19 | 7:02:06 |
| exit | 0 | 0 |
| execution | COMPLETE | COMPLETE |
| evidence validation | PASS | PASS |
| 보존 organizer checkpoints | 60 | 150 |
| last saved numbered ckpt | `model_2950.pt` | `model_7450.pt` |
| automatic best | `model_2000.pt` | `model_7050.pt` |

A는 B의 resume가 아니다. 별도 fresh 실행이지만 아래에서 보듯 첫 3K 궤적이 정확히 재현됐다.

### 2.3 실행 명령과 resolved config 출처

B:

`<B_RUN>/command.txt`

```text
/workspace/IsaacLab/isaaclab.sh -p /workspace/training/quadruped/train.py
  --task Quadruped-v0
  --max_iterations 3000
  --num_envs 4096
  --headless
  agent.save_interval=50
```

A는 위와 동일하며 `--max_iterations 7500`만 다르다.

resolved config의 archive 내부 근거:

- `<RUN>/native_run/params/env.yaml`
- `<RUN>/native_run/params/agent.yaml`
- `<RUN>/source/quadruped_rewards.py`
- `<RUN>/source/identity.json`
- `<RUN>/metadata.json`
- `<RUN>/checkpoint_index.json`

두 `agent.yaml`의 구조적 diff는 **`max_iterations` 한 항목뿐**이다.  
두 `env.yaml`의 구조적 diff는 **run별 `log_dir` 한 항목뿐**이다.

따라서 exported `env.yaml`의 파일 SHA가 서로 다른 것을 reward/env 차이로 해석하면 안 된다. 실제 resolved 값 비교에서는 `log_dir` 이외의 차이가 없다.

### 2.4 source identity

두 Run의 `source/identity.json`에 기록된 task source 8개가 같은 SHA를 가진다. 실행 전/후 hash도 같고 `changed_during_run=false`다.

특히 reward source:

`quadruped_rewards.py`  
SHA-256: `c0b625b26289ef06dd20f02296f2a4eb9fdf0a210ab106e6675dbe1a3154d564`

active participant reward dial:

```text
track_lin_vel_xy_exp = +1.25
feet_air_time        = +0.01
lin_vel_z_l2         = -3.0
ang_vel_xy_l2        = -0.08
action_rate_l2       = -0.01
```

프로젝트의 BASE parent 대비 의도한 변경은:

```text
track_lin_vel_xy_exp: 1.0 -> 1.25
```

뿐이다.

A/B 사이에는 이 reward 차이조차 없다. 둘 다 이미 `LINTRACK-125`다.

### 2.5 PPO/환경

공통 agent:

- PPO
- actor/critic MLP `[512, 256, 128]`, ELU
- epochs 5, mini-batches 4
- initial LR `1e-3`, adaptive
- gamma `0.99`, lambda `0.95`
- entropy coefficient `0.008`
- desired KL `0.01`
- clip `0.2`
- max grad norm `1.0`
- initial scalar std `1.0`
- `check_for_nan=true`

공통 env:

- sim dt `0.005 s`
- decimation `4` → control dt `0.020 s` (50 Hz)
- episode horizon `20 s` → 최대 약 1000 control steps
- command resampling `10 s`
- x command `[-1, 2] m/s`
- y command `[-0.6, 0.6] m/s`
- yaw command `[-1, 1] rad/s`
- curriculum enabled
- terrain grid `10×20`, max initial level 5
- terrain patch `8×8 m`
- training terrain proportion:
  - stairs 20%
  - inverted stairs 20%
  - boxes 20%
  - random rough 20%
  - slope 10%
  - inverted slope 10%

기준 submission preset ID는 archive metadata에 기록돼 있지 않다. Registry상 이 Experiment의 parent는 **BASE**다. `g2-submit-3 / LINTRACK-150-LINZ-2`는 다른 두-variable 정책이므로 여기의 기준 preset/control로 추정하지 않는다.

---

## 3. 비교 설계: 무엇을 직접 말할 수 있는가

### 3.1 A/B 비교 등급

| 질문 | 판정 | 이유 |
|---|---|---|
| 3K 이후 추가 학습 효과 | **직접 비교에 적합** | 동일 source/config/seed, A의 첫 3K scalar와 checkpoint가 B와 exact match |
| `LINTRACK-125` reward 자체의 효과 | **판단 불가** | A/B 모두 track=1.25; unchanged BASE same-length control 없음 |
| 완성 정책의 training proxy 성능 | **조건부 비교 가능** | 동일 정의 raw TensorBoard 재집계 가능 |
| 실제 6지형 traversal/보행 품질 | **판단 불가** | 6지형 MP4/manifest 미제공 |
| 공식 evaluator 성능 | **판단 불가** | fixed evaluator 결과 없음 |
| 다른 seed로의 일반화 | **판단 불가** | single seed 42 |

### 3.2 첫 3K가 실제로 같은 trajectory인지 검증

raw TensorBoard event를 직접 protobuf로 파싱했다.

- B: 27 scalar tags × iteration 0–2999
- A: 27 scalar tags × iteration 0–7499
- duplicate iteration 없음
- step reset 없음
- NaN/Inf scalar 없음

wall-clock 기반 `Train/*/time` 2개와 `Perf/*` 3개는 실행 시간/GPU scheduling 영향이므로 trajectory equality 판정에서 제외했다.

나머지 **22개 substantive scalar tag가 iteration 0–2999에서 모두 exact match**다. 예:

- `Curriculum/terrain_levels`
- `Metrics/base_velocity/error_vel_xy`
- `Metrics/base_velocity/error_vel_yaw`
- `Episode_Termination/base_contact`
- `Episode_Termination/time_out`
- `Train/mean_episode_length`
- `Train/mean_reward`
- `Policy/mean_std`
- `Loss/value`
- `Loss/entropy`
- 모든 `Episode_Reward/*`

checkpoint index에서도 `model_0.pt`부터 `model_2950.pt`까지 50-step 간격 60개가 **60/60 동일 SHA**다.

manifest 주장만 믿지 않기 위해 실제 archive bytes를 선택적으로 다시 hash했다.

| checkpoint | B actual SHA | A actual SHA | 결과 |
|---|---|---|---|
| `model_2000.pt` | `5a97c3e2...34ab7` | `5a97c3e2...34ab7` | 동일 |
| `model_2950.pt` | `6b72c530...5992a` | `6b72c530...5992a` | 동일 |

따라서 A는 “비슷하게 다시 학습한 7.5K”가 아니라, **첫 3K까지 B와 완전히 같은 policy/optimizer trajectory를 재현한 뒤 그 상태에서 4.5K 더 진행한 fresh 실행**으로 취급할 수 있다.

이는 single-seed 내부에서 추가 학습의 방향을 읽기에는 매우 강한 비교다. 다만 다른 seed에서도 같은 방향이 재현된다는 뜻은 아니다.

---

## 4. raw TensorBoard 동일 기준 재분석

### 4.1 window 선택

주 비교는 각 Run의 **late-500**으로 했다.

- B 3K: iter `2500–2999`
- A 7.5K: iter `7000–7499`

선택 이유는 endpoint 한 점이나 report의 reward peak를 피하고 각 실행의 terminal training phase를 비교하기 위해서다. 결론의 경계 민감도는 **late-1000**으로 별도 확인했다.

- B: `2000–2999`
- A: `6500–7499`

첫 10%를 기계적으로 삭제하지 않았고, 전체 500-step phase도 함께 확인했다.

### 4.2 핵심 late-500

| metric | B 3K late-500 | A 7.5K late-500 | 변화 | 해석 |
|---|---:|---:|---:|---|
| `Curriculum/terrain_levels` | 5.282 | **5.913** | +0.631 | 더 높은 curriculum 분포 |
| `error_vel_xy` | 0.736 | **0.567** | -0.169 (-23.0%) | XY 추종 개선 |
| `error_vel_yaw` | **0.396** | 0.399 | +0.003 | 사실상 차이 없음 |
| `base_contact` | 9.93% | **6.23%** | -3.70%p | training termination 감소 |
| `time_out` | 90.07% | **93.77%** | +3.70%p | horizon 도달 증가 |
| mean episode length | 948.6 | **968.7** | +20.1 steps | 더 긴 episode |
| mean reward | **16.123** | 15.684 | -0.439 | 총 reward는 오히려 낮음 |
| policy mean std | 0.557 | **0.672** | +0.115 | exploration spread 증가 |

`base_contact`는 training의 termination scalar다. 이를 공식 evaluator의 fall rate/Survival로 바꾸어 부르지 않는다.

### 4.3 late-1000 sensitivity

| metric | B 3K late-1000 | A 7.5K late-1000 | 변화 |
|---|---:|---:|---:|
| terrain | 5.103 | **5.904** | +0.800 |
| XY error | 0.762 | **0.563** | -0.199 (-26.1%) |
| yaw error | 0.399 | **0.394** | -0.005 |
| base-contact | 9.95% | **6.27%** | -3.68%p |
| timeout | 90.06% | **93.73%** | +3.68%p |
| episode length | 947.0 | **969.1** | +22.1 |
| mean reward | 16.016 | 16.228 | +0.212 |
| policy std | 0.548 | 0.656 | +0.108 |

late-500과 late-1000 모두 terrain, XY, base-contact, episode length의 방향이 같다. 따라서 이 개선은 window 한 번의 선택에 의존하지 않는다. yaw는 양쪽 window에서 실질적 우위를 보이지 않는다.

### 4.4 학습 phase

A의 500-iteration block mean:

| iter | terrain | XY err | yaw err | base-contact | episode length | reward | std |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0–499 | 0.743 | 1.512 | 0.512 | 14.15% | 900.9 | 9.141 | 0.538 |
| 500–999 | 0.730 | 1.470 | 0.378 | 5.93% | 973.9 | 14.651 | 0.502 |
| 1000–1499 | 1.040 | 1.337 | 0.365 | 8.14% | 960.8 | 15.445 | 0.506 |
| 1500–1999 | 3.186 | 0.905 | 0.385 | 9.83% | 946.6 | 17.052 | 0.501 |
| 2000–2499 | 4.925 | 0.789 | 0.402 | 9.97% | 945.3 | 15.908 | 0.539 |
| 2500–2999 | 5.282 | 0.736 | 0.396 | 9.93% | 948.6 | 16.123 | 0.557 |
| 3000–3499 | 5.493 | 0.727 | 0.406 | 7.86% | 962.0 | 16.074 | 0.579 |
| 3500–3999 | 5.560 | 0.715 | 0.403 | 7.84% | 961.6 | 15.902 | 0.594 |
| 4000–4499 | 5.663 | 0.672 | 0.390 | 8.63% | 957.5 | 15.996 | 0.596 |
| 4500–4999 | 5.749 | 0.674 | 0.399 | 6.61% | 968.0 | 15.746 | 0.620 |
| 5000–5499 | 5.776 | 0.630 | 0.384 | **5.03%** | **976.8** | 17.294 | 0.603 |
| 5500–5999 | 5.746 | 0.639 | 0.416 | 6.54% | 967.5 | 13.788 | 0.683 |
| 6000–6499 | 5.742 | 0.599 | 0.402 | 9.11% | 952.4 | 14.683 | 0.683 |
| 6500–6999 | 5.894 | **0.559** | 0.389 | 6.31% | 969.5 | 16.772 | 0.640 |
| 7000–7499 | **5.913** | 0.567 | 0.399 | **6.23%** | 968.7 | 15.684 | 0.672 |

중요한 패턴은 두 가지다.

1. **3K 이후에도 학습이 끝나지 않았다.** terrain과 XY tracking은 3K 이후 계속 개선된다.
2. 개선은 단조롭지 않다. 5.5K–6.5K 사이 reward·base-contact·yaw가 흔들린 뒤 6.5K 이후 다시 회복한다. 따라서 한 checkpoint나 mean reward만으로 장기 방향을 읽으면 안 된다.

### 4.5 무엇을 배웠고 무엇을 대가로 냈는가

동일 reward weights이므로 weighted reward term 자체는 A/B 안에서 계산 정의가 같다. late-500에서:

| weighted training term | 3K | 7.5K | 방향 |
|---|---:|---:|---|
| `track_lin_vel_xy_exp` | +0.832 | **+0.949** | 추종 reward 증가 |
| `track_ang_vel_z_exp` | +0.576 | +0.591 | 소폭 증가 |
| `action_rate_l2` | -0.103 | **-0.147** | 행동 급변 비용 증가 |
| `ang_vel_xy_l2` | -0.162 | **-0.194** | 몸통 각속도 비용 증가 |
| `lin_vel_z_l2` | -0.064 | **-0.098** | 수직 운동 비용 증가 |
| `dof_acc_l2` | -0.172 | **-0.211** | 관절 가속 비용 증가 |
| `dof_torques_l2` | -0.101 | **-0.122** | torque 비용 증가 |

이것은 “7.5K가 실제 영상에서 더 거칠다”는 증거가 아니다. 다만 **XY tracking/terrain 적응을 더 얻는 동안 control/body-motion 관련 weighted costs가 커진 training trade-off**가 관찰된다는 뜻이다.

이 trade-off 때문에 late-500 total reward는 7.5K가 오히려 조금 낮다. 따라서 total reward를 locomotion 품질 순위로 쓰면 잘못된 결론이 나온다.

---

## 5. 최적화 안정성

### 5.1 정상 종료와 finite 여부

- 두 Run console 모두 `Traceback=0`
- raw TensorBoard 모든 scalar finite
- console에서 NaN/Inf 학습 오류 없음
- exit 0
- native finalize 완료
- evidence validation PASS

따라서 A는 실행 실패나 numerical collapse로 분류하지 않는다.

### 5.2 value-loss spike

다만 장기 학습에서 value-function instability는 분명히 커졌다.

| 구간 | value loss > 10 | > 50 | > 100 | max |
|---|---:|---:|---:|---:|
| 0–2999 | 10 points | 2 | 0 | 88.84 @ 2304 |
| 3000–7499 | 92 points | 27 | 11 | **273.12 @ 4711** |

late-500 기준 value-loss:

- 3K: median `0.023`, p99 `8.24`, max `37.10`
- 7.5K: median `0.200`, p99 `40.58`, max `109.04`

그럼에도 terrain/XY/contact가 late phase에서 회복·개선되고 NaN/Inf로 이어지지 않았다. 따라서 현재 판단은 **“발산”이 아니라 “장기 학습에서 critic instability가 커지는 경고”**다.

추가 장기 학습을 자동으로 권할 근거는 없다. 실제 행동 검증 전에 10K 이상으로 더 돌리는 것은 정보 대비 GPU 비용이 낮다.

### 5.3 exploration

policy mean std는 late-500 `0.557 → 0.672`로 증가했다. 이는 training exploration distribution이 더 넓어졌다는 사실만 말할 수 있다. 영상 jitter나 deterministic exported actor의 보행 떨림으로 직접 바꾸어 해석하지 않는다.

---

## 6. 6지형 행동 비교 — 현재 입력으로는 수행 불가

### 6.1 실제 확인한 영상 availability

두 nested train archive를 전수 listing했다.

- B 3K archive: MP4 **0개**
- A 7.5K archive: MP4 **0개**
- `video_suite_manifest.json`: 없음

canonical OFFICIAL raw Release도 확인했다.

- B 3K Release: loose `play_video.mp4` 1개는 있으나 **6지형 suite가 아님**
- A 7.5K Release: MP4 없음
- 현재 확인한 Release 목록에서 이 `LINTRACK-125` A/B에 대응하는 6-terrain video suite Release를 찾지 못함

따라서 다음 표의 관찰값을 만들어내지 않는다.

| terrain | B 3K 행동 | A 7.5K 행동 | 공통 약점/차이 | 판단 |
|---|---|---|---|---|
| boxes | 미관찰 | 미관찰 | — | 영상 미제공 |
| random rough | 미관찰 | 미관찰 | — | 영상 미제공 |
| stairs | 미관찰 | 미관찰 | — | 영상 미제공 |
| inverted stairs | 미관찰 | 미관찰 | — | 영상 미제공 |
| slope up 20° suite | 미관찰 | 미관찰 | — | 영상 미제공 |
| slope down 20° suite | 미관찰 | 미관찰 | — | 영상 미제공 |

training env가 위와 유사한 지형 클래스를 포함한다는 사실은 실제 suite 통과 증거가 아니다. 특히 프로젝트의 Go2 6지형 영상 suite는 fixed slope와 별도 play 조건을 사용할 수 있으므로 `Curriculum/terrain_levels≈5.9`를 “20° 경사 통과”로 바꾸어 말하지 않는다.

현재 자료에서는 다음을 전부 **미측정**으로 남긴다.

- terrain 실제 전진/완주
- obstacle stall
- foot snagging / dragging
- sliding / hopping
- 몸통 pitch/roll
- 충돌 후 recovery
- command transition 실제 응답
- 짧은 영상에서의 낙상 여부

---

## 7. Checkpoint 판단

### 7.1 automatic best와 terminal checkpoint

B:

- report reward peak: `19.443 @ iter 2018`
- automatic `model_best.pt` → `model_2000.pt`
- SHA: `5a97c3e2e3a32ad18d7fd89254e03a94272e33f85da360ea40364ec05db34ab7`
- last preserved numbered: `model_2950.pt`
- SHA: `6b72c530e571f7e9fc826c3917bd6199a22c9b1a2a1028ca7bf981231485992a`

A:

- report reward peak: `19.917 @ iter 7038`
- automatic `model_best.pt` → `model_7050.pt`
- SHA: `d40f2666da6063c16c88353163115dcac1a2bd8b98011bf745543737a2188015`
- last preserved numbered: `model_7450.pt`
- SHA: `b8766030e306dd72160d37292539575d5a1d92c2757f34637dafab3c1582343a`

outer `model_best.pt`를 직접 hash해 각각 위 selected checkpoint SHA와 일치함을 확인했다.

### 7.2 3K에서는 reward-best가 후기 능력을 대표하지 않았다

`model_2000` 주변(1900–2149)과 terminal 2750–2999를 비교하면 terminal phase는:

- terrain `4.689 → 5.348`
- XY `0.801 → 0.728` 개선
- yaw `0.392 → 0.395` 유사
- base-contact `8.74% → 9.61%` 악화
- reward `17.17 → 16.17` 하락

즉 automatic reward-best는 terrain/XY의 후기 발전을 놓쳤다. 이것이 `model_best` label만으로 정책 능력을 고르면 안 되는 실제 사례다.

### 7.3 7.5K에서는 7050이 terminal 7450보다 training proxy상 더 균형적

`model_7050` 부근 `6900–7149` vs terminal `7250–7499`:

| metric | around 7050 | terminal 7250–7499 |
|---|---:|---:|
| terrain | **5.959** | 5.907 |
| XY error | **0.552** | 0.561 |
| yaw error | **0.385** | 0.404 |
| base-contact | **5.24%** | 6.73% |
| episode length | **973.9** | 965.6 |
| mean reward | **17.05** | 15.25 |
| std | 0.633 | 0.688 |

이 late regression은 catastrophic collapse가 아니지만 여러 축에서 같은 방향이다.

이 Run은 **fresh**이므로 프로젝트의 “긴 resume는 final numbered를 기본 대표로 둔다” 원칙을 기계적으로 적용할 대상도 아니다. 현재 training evidence만 놓고 보면 `model_7050`을 실제 행동 평가의 1순위 후보로 두는 것이 합리적이다.

다만 이것은 **정책 품질 확정 선택이 아니라 평가 순서 결정**이다. 6지형 영상/fixed evaluator 없이 `model_7050`이 실제 terrain 행동에서도 최선이라고 확정하지 않는다.

---

## 8. 핵심 발견별 설명과 경쟁 가설

### 발견 A — 추가 4.5K로 XY/terrain/contact가 동시에 좋아짐

**관찰**

late-500에서 terrain `+0.631`, XY error `-0.169`, base-contact `-3.70%p`, episode length `+20.1 steps`.

**해석**

3K 이후 policy가 더 높은 curriculum 분포에 적응하면서 planar command tracking과 training survival proxy를 함께 개선했다.

**경쟁 설명**

단순 seed 차이나 source 차이는 이번 A/B에서는 설명력이 매우 낮다. 첫 3K scalar와 checkpoint가 exact match하고 source/config도 같기 때문이다. 다만 curriculum 자체가 함께 진행되므로 “같은 고정 난이도에서 능력이 23% 개선됐다”고 바꾸어 말할 수는 없다.

**반대 근거**

yaw는 좋아지지 않았고 control/body-motion weighted penalties는 더 커졌다. value loss도 더 불안정해졌다.

**판별 방법**

`model_2950` vs `model_7050`을 같은 fixed terrain/command/difficulty에서 평가해 실제 displacement/traversal, XY/yaw, base-contact와 영상을 함께 비교한다.

### 발견 B — mean reward는 개선을 제대로 요약하지 못함

**관찰**

late-500 total reward는 `16.123 → 15.684`로 낮아졌는데 terrain/XY/base-contact는 오히려 좋아졌다.

**해석**

더 어려운 curriculum과 커진 action/body-motion costs 때문에 total reward 하나가 locomotion 품질을 대표하지 않는다.

**경쟁 설명**

reward 계산 정의가 바뀌어서가 아니다. 두 Run의 reward source/config는 동일하다.

**반대 근거**

late-1000에서는 mean reward가 `16.016 → 16.228`로 방향이 뒤집힌다. 즉 reward 차이 자체가 window-sensitive하다.

**판별 방법**

reward ranking이 아니라 고정 evaluator의 raw tracking/progress/contact 축으로 정책을 비교한다.

### 발견 C — 7.5K 후반에는 약한 regression 신호가 있음

**관찰**

7050 주변보다 7250–7499에서 terrain, XY, yaw, base-contact, episode length, reward가 모두 약간 불리하고 std가 높다.

**해석**

7.5K 끝부분이 이미 완전히 수렴한 안정 plateau라기보다, high-curriculum에서 policy/critic가 계속 흔들리는 phase일 가능성이 있다.

**경쟁 설명**

단일 seed의 stochastic minibatch/curriculum fluctuation일 수 있다. 실제 행동 악화로 직결된다는 영상 근거는 없다.

**반대 근거**

terminal late-500 자체는 3K보다 여전히 훨씬 좋다. NaN/Inf나 terrain collapse도 없다.

**판별 방법**

7050과 7450을 동일 evaluator에서 짧게 paired 평가하면 된다. 새 학습은 필요 없다.

---

## 9. 현재 판정

| 층 | 판정 | 범위 |
|---|---|---|
| A 실행 | **COMPLETE** | exit 0, iter 0–7499 |
| A evidence | **PASS** | native run/TB/checkpoints/source/finalize/backup |
| B 실행 | **COMPLETE** | exit 0, iter 0–2999 |
| B evidence | **PASS** | 동일 |
| A vs B training-length 비교 | **직접 비교에 적합** | first 3K exact trajectory |
| LINTRACK-125 reward 효과 | **HOLD** | unchanged BASE same-length control 없음 |
| 7.5K policy 후보 | **PROMOTE to fixed paired evaluation only** | training proxies 개선 |
| 실제 6지형 행동 | **확인 불가** | 영상 묶음 없음 |
| 공식 evaluator 성능 | **확인 불가** | evaluator 결과 없음 |
| 채택/제출 우위 | **HOLD** | 행동·고정평가 미확인 |

`INVALID`는 아니다. Run과 identity는 정상이며, 부족한 것은 행동 대조와 reward control이다.

---

## 10. 다음 한 번의 행동

### 1순위 — 새 GPU 학습 없이 기존 checkpoint paired 평가

비교:

- A: `model_7050.pt`  
  SHA `d40f2666da6063c16c88353163115dcac1a2bd8b98011bf745543737a2188015`
- B: `model_2950.pt`  
  SHA `6b72c530e571f7e9fc826c3917bd6199a22c9b1a2a1028ca7bf981231485992a`

맞출 조건:

- 같은 evaluator implementation
- 같은 terrain set/difficulty
- 같은 command schedule
- 같은 seed-set
- curriculum off 또는 동일하게 고정
- 같은 episode horizon
- 동일하게 source checkpoint SHA가 기록된 영상 manifest

기록할 것:

- XY와 yaw를 분리한 error
- base-contact/timeout
- world-frame forward displacement 또는 terrain completion
- lateral drift
- stall time
- terrain별 worst case
- 영상 annotation: snag/slide/hop/stall/recovery/fall

**결과별 다음 결정**

- 7050이 실제 progress + tracking + contact에서 함께 개선: 7.5K policy를 다음 제출/후보 비교 단계로 승격
- training proxy만 좋아지고 실제 traversal은 같거나 악화: LINTRACK-125 장기학습 채택 HOLD, reward/control 재검토
- 7450이 필요하다고 의심될 경우: 같은 batch 안에서 terminal `model_7450.pt`를 보조 후보로 추가하되 새 selector를 만들지는 않음

### 2순위 — reward 인과효과가 필요한 경우에만 새 control

현재 A/B만으로는 `track_lin_vel_xy_exp=1.25`가 BASE `1.0`보다 좋다는 인과 결론을 낼 수 없다.

가장 작은 새 control은:

- fresh start, parent checkpoint 없음
- `track_lin_vel_xy_exp=1.0`
- 나머지 source/PPO/env 그대로
- seed 42
- 4096 env
- 우선 3K
- 기존 LINTRACK-125 3K와 동일 evaluator

이 control은 reward 효과 질문을 답하기 위한 것이고, 현재 7.5K 정책의 실제 행동 확인보다 우선하지 않는다.

---

## 11. 한계와 재확인 가능한 근거 목록

### 직접 재계산한 것

- outer archive size/SHA
- nested archive SHA
- metadata/validation/provenance
- source identity SHA
- reward source
- resolved `env.yaml`/`agent.yaml` structural diff
- raw TensorBoard event 27 tags 파싱
- duplicate/reset/NaN/Inf 확인
- late-500/late-1000/500-step phase 통계
- first 3K scalar exact equality
- checkpoint index 60개 common SHA equality
- `model_2000`, `model_2950`, `model_7050`, `model_7450` 선택 actual byte hash
- outer `model_best.pt` hash와 selected numbered checkpoint 연결
- console의 실제 0–2999 / 0–7499 iteration과 finalize 메시지

### archive 내부 핵심 경로

A root:

`20260929-154342-go2-lintrack-125-fresh7500-official/`

B root:

`20260928-230114-go2-lintrack125-fresh3k-r5-official/`

각 nested evidence archive에서:

- `metadata.json`
- `validation.json`
- `command.txt`
- `console.log`
- `checkpoint_index.json`
- `native_run/params/env.yaml`
- `native_run/params/agent.yaml`
- `native_run/events.out.tfevents.*`
- `source/identity.json`
- `source/quadruped_rewards.py`
- `collected/provenance.json`
- `collected/exported/report.html`
- `organizer_checkpoints/model_*.pt`

### 프로젝트 해석 경계에 사용한 문서

- `00_START_HERE_CONTEXT_AND_MAP.md`
- `05_TRAINING_RULES_AND_SUBMISSION.md`
- `07_QUADRUPED_TRAINING_CODE.md`
- `12_2026_UNIFIED_REGULATIONS.md`
- `16_EXPERIMENT_EXPORT_AND_TENSORBOARD.md`
- `17_ISSACSIMZ_VIDEO_OPERATIONS.md`
- `19_ISSACSIMZ_EXTERNAL_EVIDENCE_CLI.md`

### 확인하지 못한 것

- A/B의 6지형 MP4 실제 프레임
- 6지형 `video_suite_manifest.json`
- A의 exported `policy.pt`
- A/B matched fixed evaluator
- same-length BASE control
- multi-seed generalization
- 공식 대회 evaluator score

따라서 본 보고서의 강한 결론은 **“추가 4.5K 학습이 이 정확히 재현된 single-seed LINTRACK-125 trajectory에서 training terrain/XY/contact proxy를 개선했다”**까지다.  
**“LINTRACK-125가 BASE보다 우수하다”**, **“6지형을 잘 통과한다”**, **“공식 점수가 더 높다”**는 현재 증거로 확정하지 않는다.