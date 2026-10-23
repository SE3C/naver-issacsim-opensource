> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/incoming/other/reviewed/GO2_20260929-154342-go2-lintrack-125-fresh7500-official_VS_20260928-230114-go2-lintrack125-fresh3k-r5-official_DEEP_ANALYSIS_20261004.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# Go2 LINTRACK-125 OFFICIAL fresh 7.5K vs fresh 3K — 학습 원본·6지형 영상·camera-off 평가 심층 분석

- 작성일: 2026-10-04
- 로봇: Go2
- 비교 Run A: `20260929-154342-go2-lintrack-125-fresh7500-official`
- 비교 Run B: `20260928-230114-go2-lintrack125-fresh3k-r5-official`
- 현재 canonical reward descriptor: `LINTRACK-125` (`track_lin_vel_xy_exp=1.25`)
- 환경 분류: 두 학습 Run 모두 **OFFICIAL**, Windows 영상·scenario7 평가는 **PERSONAL 행동/진단 evidence**
- 분석 범위: 원본 학습 archive 2개, 6지형 영상 ZIP 2개, camera-off evaluation ZIP 2개를 직접 재파싱했다. 새 학습·렌더링·export·서버 조작은 수행하지 않았다.

## 1. 결론 요약

### 세 질문에 대한 답

**1) 이번 정책은 목표 행동을 실제로 얼마나 수행하는가?** 7.5K Run의 `model_7050.pt`는 현재 제공된 PERSONAL `scenario7` 평가에서 일곱 시나리오 모두 3K의 `model_2950.pt`보다 낮은 평균 tracking error를 기록했고, 가장 큰 차이는 계단이었다. 계단 전체 survival은 `96.0% → 99.740%`(+3.740%p), 평균 tracking error는 `0.60996 → 0.17085`(-71.99%)로 개선됐다. stairs-up 평균 전진 진행은 `9.23 → 18.67 m`, stall fraction은 `34.51% → 1.18%`; stairs-down은 `7.20 → 18.89 m`, stall은 `53.44% → 2.52%`였다. rough/slope/push/randomized에서도 survival은 100%를 유지하면서 tracking error가 각각 약 20.4%, 23.3%, 11.3%, 20.5% 낮았다. 이 수치는 공식 점수가 아니라 동일 PERSONAL 평가 harness 안의 raw diagnostic이다.

6지형 영상은 20초·50 Hz·1000 frame·seed 42의 동일 `maneuver_push` 프로토콜로 만들어졌고 source checkpoint SHA가 학습 archive의 checkpoint index와 정확히 연결된다. `model_7050`은 stairs/random rough/20° up/down slope에서 초기 지형 구간을 지나간 뒤 외란·횡이동·yaw 명령 구간까지 upright를 유지하는 장면이 확인된다. boxes 영상도 실제 상자 지형을 지나 flat 구간으로 빠져나온다. 반면 3K `03_boxes.mp4`는 디코딩은 되지만 **검은 화면**이며, 1초 간격 20개 샘플 frame의 평균/표준편차가 모두 0이어서 boxes에 대한 3K 시각 증거로 사용할 수 없다.

**2) 비교 정책의 차이 중 무엇이 관찰이고, 무엇을 설정 효과로 해석할 수 있는가?** 두 OFFICIAL Run은 fresh, seed 42, 4096 env, 같은 task/reward source SHA, 같은 resolved env/PPO이고 차이는 `max_iterations=3000` 대 `7500`뿐이다. `env.yaml`의 유일한 diff는 run별 `log_dir`, `agent.yaml`의 유일한 실질 diff는 `max_iterations`다. TensorBoard에서 첫 3000 iteration의 substantive scalar 22개가 byte-level value/step 기준으로 exact match했다. 달라진 것은 wall-clock 성능 tag 3개와 `/time` x-axis step뿐이다. 따라서 **이 pair에서 3K→7.5K 차이는 single-seed/config 내 추가 학습량 효과로 매우 강하게 해석할 수 있다.** 반대로 `track_lin_vel_xy_exp 1.0→1.25`라는 reward 변경 자체의 인과효과는 동일 길이 BASE control이 없으므로 이 자료만으로 확정할 수 없다.

**3) 현재 자료에서 내려야 할 결정과 가장 먼저 풀 불확실성은?** `LINTRACK-125`의 **정책/학습량 판단은 PROMOTE**, reward dial 자체의 인과 판단은 **HOLD**가 타당하다. 현재 행동 evidence 기준으로 `model_7050.pt`가 `model_2950.pt`보다 명확히 우수하다. 특히 계단 실패/정체가 크게 줄어 이번 비교의 가장 강한 발견이다. 다만 7.5K의 terminal `model_7450.pt`는 행동평가가 없고, 현재 영상/평가 source는 automatic best인 `model_7050.pt`다. 가장 정보가 큰 다음 행동은 새 학습이 아니라 **이미 보존된 `model_7450.pt`를 동일 scenario7 조건으로 한 번 평가해 `7050`과 late-terminal 차이를 확인하는 것**이다. 이는 7.5K Run의 대표 checkpoint를 확정하는 질문이며, reward 인과효과를 검증하는 실험과는 별개다. reward 효과 자체를 묻는다면 그 다음에 `track_lin_vel_xy_exp=1.0`의 same-source/same-seed/same-length fresh control이 필요하다.

### 현재 판정

| 항목 | 판정 | 근거 |
|---|---|---|
| 3K 실행 | **COMPLETE** | exit 0, finalize completed, official backup success, evidence validation PASS |
| 7.5K 실행 | **COMPLETE** | exit 0, finalize completed, official backup success, evidence validation PASS |
| 3K↔7.5K 학습량 비교 | **직접 비교에 적합** | 동일 source/config/seed/env, 첫 3K substantive trajectory exact match |
| `LINTRACK-125` reward 자체 효과 | **HOLD** | BASE `LINTRACK-100` same-length unchanged control 없음 |
| 정책 행동 비교 `2950` vs `7050` | **직접 비교에 적합한 PERSONAL 진단** | 동일 protocol ID, seeds, num_envs, camera-off suite; 공식 score는 아님 |
| 대표 policy | **`model_7050.pt` PROMOTE** | 계단 포함 모든 scenario tracking 개선, survival 유지/개선; late training balance도 7450보다 7050 인접부가 안정적 |
| 7.5K terminal `model_7450.pt` | **미확인 행동 후보** | checkpoint는 보존됐으나 이번 영상/평가 source가 아님 |

---

## 2. Run·checkpoint·영상 identity와 설정 연결

### 2.1 학습 provenance

#### B — OFFICIAL fresh 3K

- Run ID: `20260928-230114-go2-lintrack125-fresh3k-r5-official`
- operation/profile/mode: `train / go2 / official`
- 명령: `/workspace/IsaacLab/isaaclab.sh -p /workspace/training/quadruped/train.py --task Quadruped-v0 --max_iterations 3000 --num_envs 4096 --headless agent.save_interval=50`
- seed: 42
- rollout: 24 steps/env
- requested iterations: 3000
- TensorBoard global iteration: 0–2999
- 보존 numbered checkpoint: 0–2950, 50 interval, 60개
- 마지막 저장 checkpoint: `model_2950.pt`
- automatic `model_best.pt`: `model_2000.pt`와 동일 SHA `5a97c3e2…34ab7`
- execution: exit 0 / completed
- evidence: `validation.json` overall PASS, TensorBoard 1개, organizer checkpoint 60/60, source before/after hash 일치, official finalize/backup PASS
- fresh run: `parent_run_id=null`, `resume_lineage=null`

Resolved config 원본:

- `.../native_run/params/env.yaml`
- `.../native_run/params/agent.yaml`
- exported copy: `.../collected/exported/env.yaml`
- 실행 인자: `command.txt`, `metadata.json`
- reward source: `source/quadruped_rewards.py`
- source identity: `source/identity.json`

#### A — OFFICIAL fresh 7.5K

- Run ID: `20260929-154342-go2-lintrack-125-fresh7500-official`
- operation/profile/mode: `train / go2 / official`
- 명령: `/workspace/IsaacLab/isaaclab.sh -p /workspace/training/quadruped/train.py --task Quadruped-v0 --max_iterations 7500 --num_envs 4096 --headless agent.save_interval=50`
- seed: 42
- rollout: 24 steps/env
- requested iterations: 7500
- TensorBoard global iteration: 0–7499
- 보존 numbered checkpoint: 0–7450, 50 interval, 150개
- 마지막 저장 checkpoint: `model_7450.pt`, SHA `b8766030…343a`
- automatic `model_best.pt`: `model_7050.pt`와 동일 SHA `d40f2666…8015`
- execution: exit 0 / completed
- evidence: `validation.json` overall PASS, TensorBoard 1개, organizer checkpoint 150/150, source before/after hash 일치, official finalize/backup PASS
- fresh run: `parent_run_id=null`, `resume_lineage=null`

Resolved config와 metadata 경로 구조는 3K와 동일하다.

### 2.2 실제 설정 차이

두 `source/identity.json`의 8개 task-root 파일 SHA가 모두 같다. `quadruped_rewards.py` SHA는 양쪽 모두 `c0b625b2…d564`이고 실행 중 변경도 없다. `native_run/params/env.yaml` diff는 `log_dir` 한 줄뿐이다. `agent.yaml`에서 확인된 실질 설정 차이는 `max_iterations: 3000 → 7500`뿐이다.

핵심 reward resolved 값도 완전히 같다.

| reward term | 3K | 7.5K |
|---|---:|---:|
| `track_lin_vel_xy_exp` | **+1.25** | **+1.25** |
| `track_ang_vel_z_exp` | +0.75 | +0.75 |
| `lin_vel_z_l2` | -3.0 | -3.0 |
| `ang_vel_xy_l2` | -0.08 | -0.08 |
| `dof_torques_l2` | -0.0002 | -0.0002 |
| `dof_acc_l2` | -2.5e-7 | -2.5e-7 |
| `action_rate_l2` | -0.01 | -0.01 |
| `feet_air_time` | +0.01 | +0.01 |
| `flat_orientation_l2` | 0.0 | 0.0 |
| `dof_pos_limits` | 0.0 | 0.0 |

따라서 이 두 Run 사이에는 reward delta가 없다. 현재 프로젝트 naming 기준에서 둘 다 같은 `LINTRACK-125` 질문의 서로 다른 길이 fresh Run으로 다루는 것이 맞다. `g2-submit-3 / LINTRACK-150-LINZ-2`와는 다른 설정이다. frozen preset 파일 자체(`research/submission_presets/`)는 이번 첨부 파일 집합에 포함되지 않아 byte-for-byte preset diff를 새로 재검증하지 못했다. 다만 archive의 resolved config는 위 값으로 직접 확정했다.

### 2.3 checkpoint ↔ 영상 ↔ evaluator 연결

| 정책 | 학습 archive checkpoint index | 6지형 source | scenario7 source | 연결 상태 |
|---|---|---|---|---|
| 3K comparator | `model_2950.pt`, SHA `6b72c530e571f7e9fc826c3917bd6199a22c9b1a2a1028ca7bf981231485992a` | 동일 SHA | 동일 SHA | **원본 index ↔ 영상 ↔ 평가 일치** |
| 7.5K candidate | `model_7050.pt`, SHA `d40f2666da6063c16c88353163115dcac1a2bd8b98011bf745543737a2188015` | 동일 SHA | 동일 SHA | **원본 index ↔ 영상 ↔ 평가 일치** |
| 7.5K terminal | `model_7450.pt`, SHA `b8766030…343a` | 없음 | 없음 | 행동 미평가 |

중요한 비대칭은 3K가 **terminal 근처 `2950`**을 행동 comparator로 쓰고, 7.5K는 **automatic best `7050`**을 쓴다는 점이다. 따라서 이번 행동 비교는 “각 Run의 선택 후보 `2950 vs 7050`”이지 “정확한 3K endpoint vs 7.5K endpoint”가 아니다.

---

## 3. 비교 설계와 해석 가능한 범위

### 3.1 핵심 조건

| 조건 | 3K | 7.5K | 판정 |
|---|---|---|---|
| robot/task | Go2 / `Quadruped-v0` | 동일 | 직접 비교 가능 |
| 환경 | OFFICIAL train | OFFICIAL train | 동일 |
| fresh/resume | fresh | fresh | 동일 |
| parent checkpoint | 없음 | 없음 | 동일 |
| seed | 42 | 42 | 동일 |
| num_envs | 4096 | 4096 | 동일 |
| PPO/agent | 동일, max_iterations 제외 | 동일 | 직접 비교 가능 |
| reward source/config | 동일 | 동일 | 직접 비교 가능 |
| 학습량 | 3000 | 7500 | **의도된 유일 실질 차이** |
| training terrain | curriculum enabled | 동일 | 같은 첫 3K trajectory까지 확인 |
| 행동 checkpoint | 2950 | 7050 | 선택 시점 다름 |
| video | PERSONAL, seed 42, 1 env, 20 s | 동일 | 정성 비교 가능 |
| evaluation | PERSONAL scenario7, 128 env × seeds 4201–4203 | 동일 protocol ID | 동일 harness 안 정량 비교 가능 |

### 3.2 첫 3K exact-match 재검증

raw TensorBoard event를 직접 TFRecord/protobuf로 파싱했다. 27 scalar tag 중 다음 22개 substantive scalar는 0–2999의 `(step,value)`가 전부 exact match했다.

- curriculum/terrain
- 10개 episode reward term
- base-contact/time-out termination
- XY/yaw tracking error
- mean episode length/reward
- policy mean std
- value/surrogate/entropy/LR loss·optimizer 계열

차이가 난 5개는 학습 내용이 아니라 runtime timing/표현 tag였다.

- `Perf/collection_time`
- `Perf/learning_time`
- `Perf/total_fps`
- `Train/mean_episode_length/time`의 x-axis wall-time step
- `Train/mean_reward/time`의 x-axis wall-time step

즉 두 Run은 독립 fresh 실행임에도 결정론적으로 같은 초기 학습 trajectory를 재현했고, 7.5K는 그 동일 궤적을 4500 iteration 더 진행한 Run이다. 이 사실은 seed 하나의 일반화를 뜻하지 않지만 **추가 학습량 효과를 분리하는 내부 비교로는 매우 강한 조건**이다.

### 3.3 해석 등급

- **학습량 효과(3K→7.5K): 직접 비교에 적합.**
- **선택 policy 행동(`2950→7050`): 동일 PERSONAL harness 안에서 직접 비교에 적합.**
- **`LINTRACK-125` reward 자체 효과: 판단 불가/HOLD.** BASE unchanged same-length control이 없다.
- **공식 대회 점수 향상: 판단 불가.** scenario7은 공식 evaluator가 아니며 evaluation manifest도 `official_score=false`, `raw_diagnostics_only=true`다.
- **단일 seed 일반화: 판단 불가.** training seed는 42 하나다. PERSONAL evaluator가 seeds 4201–4203을 사용해 행동 robustness를 보강하지만, training seed 반복이 아니다.

---

## 4. 학습 시계열 재분석

### 4.1 후반 window 선택

두 Run이 같은 0–2999 trajectory를 공유하므로 3K의 후기 상태는 `2500–2999`, 7.5K의 후기 상태는 `7000–7499`의 **late-500**을 주 비교 window로 사용했다. 이는 각 Run의 마지막 500 scalar point를 같은 정의로 보는 선택이다. 경계 민감성은 `2000–2999`와 `6500–7499`의 **late-1000**으로 확인했다. 결론의 방향은 terrain·XY·base-contact·episode length에서 유지됐다.

### 4.2 late-500 핵심 수치

| TensorBoard tag | 3K late-500 | 7.5K late-500 | 관찰 |
|---|---:|---:|---|
| `Curriculum/terrain_levels` | 5.2823 | **5.9132** | +0.6309, higher curriculum exposure |
| `Metrics/base_velocity/error_vel_xy` | 0.73595 | **0.56700** | -0.16894 (-23.0%) |
| `Metrics/base_velocity/error_vel_yaw` | **0.39590** | 0.39931 | +0.00341, 사실상 보합/미세 악화 |
| `Episode_Termination/base_contact` | 0.09933 | **0.06229** | -3.70%p |
| `Episode_Termination/time_out` | 0.90071 | **0.93772** | +3.70%p |
| `Train/mean_episode_length` | 948.60 | **968.66** | +20.06 steps |
| `Train/mean_reward` | **16.1235** | 15.6843 | 오히려 -0.439; high variance |
| `Policy/mean_std` | 0.55656 | 0.67188 | exploration std 증가 |

late-1000에서도 terrain `5.1035→5.9038`, XY `0.7623→0.5633`, base-contact `9.951%→6.269%`, episode length `946.96→969.08` 방향이 유지된다. yaw는 `0.3989→0.3940`으로 late-1000에서는 오히려 약간 좋아져, yaw 차이는 window에 민감하고 “개선/악화”보다 **실질적으로 정체**로 보는 것이 안전하다.

### 4.3 최적화 안정성

모든 scalar는 finite였고 NaN/Inf는 확인되지 않았다. 다만 value loss와 mean reward에 큰 일시 spike가 존재한다.

- 3K `Loss/value` max `88.84 @ iter 2304`, `Train/mean_reward` min `-37.57 @ 2309`
- 7.5K `Loss/value` max `273.12 @ iter 4711`, `Train/mean_reward` min `-97.01 @ 5680`
- 7.5K `Loss/surrogate` max `+0.0496 @ 4663`

그럼에도 이후 terrain/tracking/base-contact/episode length가 회복·개선했고 마지막 값도 finite다. 따라서 “중간 spike가 있었음”은 사실이지만 장기 발산으로 분류할 근거는 없다. 오히려 mean reward가 후반 window에서 3K보다 높지 않은데 행동 관련 지표는 좋아졌다는 점은 **총 reward peak를 정책 성능의 단일 selector로 쓰지 말아야 한다는 반례**다.

### 4.4 7050 선택과 7450 terminal의 관계

7.5K에서 `model_7050.pt` 주변 7000–7099와 terminal 주변 7400–7499를 비교하면:

| tag | 7000–7099 | 7400–7499 | 방향 |
|---|---:|---:|---|
| terrain | **5.9639** | 5.9110 | 7050 인접부 우세 |
| XY error | 0.5653 | **0.5587** | terminal 인접부 미세 우세 |
| yaw error | **0.3825** | 0.4091 | 7050 인접부 우세 |
| base-contact | **5.593%** | 6.799% | 7050 인접부 우세 |
| episode length | **972.93** | 964.94 | 7050 인접부 우세 |
| mean reward | **16.65** | 15.24 | 7050 인접부 우세 |

개별 step에서도 `7050`은 terrain 5.9486, yaw 0.3838, base-contact 5.665%, episode length 978.92이고 `7450`은 각각 5.9332, 0.4083, 6.192%, 972.0이다. XY만 7450 step이 0.4898로 더 낮다. 따라서 현재 프로젝트가 7050을 행동평가 1순위로 둔 것은 원본 시계열과 일치한다. 다만 이 표는 행동평가가 아니므로 7450을 영구 배제하는 근거는 아니다.

---

## 5. PERSONAL scenario7 camera-off 재평가

### 5.1 protocol parity

두 evaluation ZIP의 `protocol_id`는 동일한 `806d7e82…145ad`다. 둘 다:

- `evaluation_environment=PERSONAL`
- deterministic inference
- `num_envs=128`
- seeds `4201,4202,4203`
- camera off
- duration 20 s
- command period 10 s
- 동일 scenario/case/environment fingerprints
- 동일 collector/scorer identity

두 평가에서 사용한 Windows evaluator source fingerprint도 서로 동일하다. 다만 이 PERSONAL evaluator의 task source SHA는 OFFICIAL training archive의 task source SHA와 byte-for-byte 동일하지 않다. 따라서 아래 비교는 **동일 PERSONAL harness에서 두 policy의 행동 차이를 측정한 것**이지 OFFICIAL server/environment를 완전 복제한 점수라고 부르지 않는다.

### 5.2 scenario-level 결과

| scenario | 2950 survival | 7050 survival | 2950 tracking error | 7050 tracking error | error 변화 |
|---|---:|---:|---:|---:|---:|
| G1 forward | 100% | 100% | 0.11131 | **0.08611** | **-22.64%** |
| G2 omnidirectional | 100% | 100% | 0.10913 | **0.08052** | **-26.22%** |
| G3 rough | 100% | 100% | 0.12212 | **0.09719** | **-20.42%** |
| G4 slope | 100% | 100% | 0.14723 | **0.11288** | **-23.34%** |
| G5 stairs | 96.0% | **99.740%** | 0.60996 | **0.17085** | **-71.99%** |
| G6 push recovery | 100% | 100% | 0.11806 | **0.10474** | **-11.28%** |
| G7 domain randomization | 100% | 100% | 0.12149 | **0.09658** | **-20.50%** |

모든 scenario에서 7050의 tracking error가 낮다. 단일 window가 아니라 세 seed × 다수 env episode를 포함하는 별도 행동 평가에서 training late-500의 XY 개선 방향이 재현됐다. 특히 training scalar만으로는 알 수 없었던 stairs의 큰 차이가 드러났다.

### 5.3 계단에서 무엇이 바뀌었는가

#### stairs-up

- 2950: 414 episodes, failures 30, survival 92.754%
- 7050: 386 episodes, failures 2, survival 99.482%
- mean tracking error: `0.54138 → 0.16812`
- forward progress: `9.23 → 18.67 m`
- stall fraction: `34.51% → 1.18%`
- roll/pitch RMS: `0.3658 → 0.2361`

#### stairs-down

- 2950: 386 episodes, failures 2, survival 99.482%
- 7050: 384 episodes, failures 0, survival 100%
- mean tracking error: `0.68352 → 0.17359`
- forward progress: `7.20 → 18.89 m`
- stall fraction: `53.44% → 2.52%`
- roll/pitch RMS: `0.3937 → 0.2363`

episode 수가 다른 이유는 실패 후 새 episode가 생성되기 때문이다. 따라서 800 vs 770 episode를 독립 샘플 수 우위로 해석하지 않았다. 핵심은 failure/survival, 동일 protocol의 episode-level error, progress, stall이다.

### 5.4 trade-off와 반대 근거

7050이 모든 축에서 단순히 “더 부드럽다”고 말할 수는 없다.

- G2 mixed의 roll/pitch RMS는 `0.0957 → 0.1240`으로 증가했다.
- slope-down action-delta RMS는 `0.4000 → 0.4440`, stairs-up은 `0.3448 → 0.4390`, stairs-down은 `0.3028 → 0.4756`으로 커졌다.
- 즉 7050은 일부 어려운 지형에서 **더 큰/빈번한 action 변화**를 사용하면서 실제 진행과 tracking을 크게 얻은 것으로 보인다.

이 패턴은 “학습이 길어져 단순히 action이 더 매끈해졌다”는 설명과 맞지 않는다. 더 유력한 해석은 추가 학습으로 지형 대응 동작을 더 적극적으로 사용하면서, 결과적으로 stall과 자세 RMS를 줄이고 진행을 회복했다는 것이다. 다만 action term 자체의 causal mechanism은 policy 내부 분석 없이 확정하지 않는다.

---

## 6. 여섯 지형 영상 비교

### 6.1 영상 계약과 확인 방법

두 ZIP 모두:

- `Quadruped-v0`
- num_envs 1
- seed 42
- 20 s / 50 Hz / 1000 frame
- 동일 scenario hash `b719e60d…d7dea`
- command: 0–6 s `(1.0,0,0)`, 6–10 s `(0.5,+0.3,0)`, 10–14 s `(0.5,-0.3,0)`, 14–17 s `(0.5,0,+0.5)`, 17–20 s `(0.5,0,-0.5)`
- world-Y push at 4, 8, 12, 16 s, ±0.5 m/s
- slope fixed 20°

MP4는 ffmpeg로 모두 1920×1080, 50 fps, 20.0 s, 1000 frame임을 확인했다. 행동 판독은 전체 파일을 디코딩하고 1 Hz contact sheet와 핵심 frame을 조사했다. 따라서 짧은 정지화면 한 장만 본 것은 아니지만, 관절 각도나 이동거리를 영상에서 정밀 추정하지 않았다.

### 6.2 지형별 관찰

| 지형 | 3K `model_2950` | 7.5K `model_7050` | 공통/판단 한계 |
|---|---|---|---|
| stairs | 약 0–6 s에서 visible stair patch를 지나가며 이후 flat 구간에서 upright 유지. sampled frames에서 낙상 없음. | 유사하게 약 0–6 s stair patch를 지나고 이후 command/push 구간에서 upright 유지. | 둘 다 한 clip에서는 생존. 정량 차이는 scenario7 G5가 훨씬 강함. |
| inverted stairs | terrain patch와의 상대 위치가 바뀌면서 upright 이동. sampled 1 Hz sequence에서 뚜렷한 낙상 없음. | 동일하게 upright. | tracking camera/장면 geometry 때문에 “중앙 계단 완주 거리”를 영상만으로 정밀 증명하지 않음. |
| boxes | **영상 자체가 검은 화면.** frame 0,50,…950의 pixel mean/std가 모두 0.0. 행동 판정 불가. | 약 1–6 s visible boxes 위/사이를 진행한 뒤 flat 영역으로 나가고 이후 upright 유지. | 3K의 boxes visual A/B는 INVALID. 이 한 영상 결함을 3K policy failure로 해석하지 않음. |
| random rough | 약 0–6 s rough patch 위를 진행해 flat으로 빠져나가고 이후 upright. | 같은 패턴. posture가 sampled frame에서 안정적으로 유지됨. | 실제 command error는 camera-off G3/G7 수치를 우선. |
| slope up 20° | 약 0–6 s visible slope 구간을 지나고 이후 flat에서 upright. | 동일하게 slope 구간을 지나고 upright. | slope traversal 거리/속도는 영상에서 정밀 계측하지 않음. scenario7 G4를 정량 근거로 사용. |
| slope down 20° | 약 0–6 s visible descending-slope 구간을 지나고 이후 upright. | 동일. | sampled frames에서 둘 다 낙상 없음; evaluator에서는 7050 tracking이 더 낮음. |

### 6.3 영상과 수치의 일치·충돌

- **일치:** random rough와 slope 영상은 둘 다 생존하고 진행하는 모습이며, scenario7에서도 양쪽 survival 100%다. 이 지형의 차이는 “넘어짐 여부”보다 tracking error/자세/진행의 질적 차이로 나타난다.
- **강한 일치:** stairs 영상은 양쪽 모두 한 번의 seed-42 clip에서는 무너지지 않지만, scenario7 다중 env/seed에서 2950의 stairs-up failure와 stall이 반복적으로 드러난다. 짧은 영상에서 안 넘어졌다고 낮은 실패율을 추정하면 안 된다는 좋은 사례다.
- **충돌이 아니라 증거 결함:** 2950 boxes MP4는 검은 화면이라 3K boxes 행동을 관찰할 수 없다. scenario7에는 boxes case가 없으므로 “3K boxes 행동은 이번 자료에서 직접 A/B 판정 불가”가 정확한 결론이다.

---

## 7. 핵심 발견별 설명·경쟁 가설·반대 근거

### 발견 A — 추가 학습은 XY tracking과 curriculum/stability를 함께 개선했다

**관찰:** late-500 terrain `5.282→5.913`, XY error `0.736→0.567`, base-contact `9.93%→6.23%`, episode length `948.6→968.7`. scenario7에서도 7개 모든 시나리오 tracking error가 낮아졌다.

**해석:** 동일 config의 추가 4.5K iteration 동안 정책이 더 높은 curriculum 난이도에서 command 추종과 접촉 안정성을 같이 개선한 것으로 해석할 수 있다.

**경쟁 설명:** 독립 fresh run의 stochastic 차이로 설명할 수 있는가? 첫 3K substantive trajectory가 exact match하므로 이 pair에서는 그 설명이 매우 약하다. 다만 single training seed이므로 다른 seed에서도 같은 크기의 향상이 재현된다는 보장은 없다.

**반대 근거:** late-500 yaw는 거의 변하지 않았고 mean reward는 오히려 낮다. 따라서 “모든 학습 지표가 단조 개선”은 아니다.

**판별 방법:** 추가 training seed 반복이 일반화 질문의 최소 실험이다. 하지만 현재 policy 선택 결정을 위해서는 새 학습보다 7450 동일 evaluator가 먼저다.

### 발견 B — 가장 큰 실제 행동 개선은 계단의 stall/실패 제거다

**관찰:** stairs error -72%, survival +3.74%p, stairs-up progress 약 2.0배, stairs-down progress 약 2.6배, stall은 34–53%에서 1–3% 수준으로 감소했다.

**해석:** 3K policy는 계단에서 “살아 있으나 전진하지 못하는” episode가 상당했고, 7.5K policy는 그 local behavior를 벗어난 것으로 보인다. training base-contact 개선만으로는 이 정도 차이를 예측할 수 없었으며, external evaluator의 progress/stall metric이 결정적인 추가 근거다.

**경쟁 설명:** evaluator seed/terrain realization 차이인가? 두 평가의 seed set, case fingerprint, protocol ID가 같고 각 seed에서 stairs-up/down 개선 방향이 반복된다. 다만 failure 이후 reset sequence는 정책별로 달라 완전 paired episode라고 부르지 않는다.

**반대 근거:** 7050 stairs의 action-delta RMS는 더 크다. 즉 개선은 “더 부드러운 동작”이 아니라 더 적극적 제어를 동반했다.

**판별 방법:** 같은 harness의 7450 평가가 이 능력이 late terminal까지 유지되는지 가장 싸게 구분한다.

### 발견 C — 7050은 좋은 후보지만 7.5K final 자체의 행동은 아직 미확인이다

**관찰:** automatic best와 video/evaluator source가 `model_7050`, 마지막 보존 checkpoint는 `model_7450`. 7400–7499에서 yaw/base-contact/episode length/terrain이 7000–7099보다 약간 나빠진다.

**해석:** 7050은 late-run 내부에서 균형이 좋은 checkpoint다. fresh Run이므로 automatic best 사용 자체가 규칙 위반은 아니지만, 7.5K 전체 결과를 7050 행동과 동일시하면 안 된다.

**경쟁 설명:** 7450의 낮은 XY error step이 실제 official-style tracking에서는 더 좋을 수 있다. 현재 행동 evidence가 없어 배제할 수 없다.

**판별 방법:** 7450을 동일 scenario7 camera-off 프로토콜에 넣어 한 번 비교한다. 새 selector나 여러 checkpoint tournament는 필요 없다.

### 발견 D — 3K boxes 영상은 policy 증거가 아니라 캡처 결함이다

**관찰:** `03_boxes.mp4`는 20 s/1000 frame H.264 파일로 구조는 정상이나, 1초 간격 20 frame 모두 RGB pixel mean/std가 0.0이고 실제 추출 frame도 완전 검정이다.

**해석:** stale policy나 policy collapse가 아니라 **영상 capture artifact**로 분류해야 한다. 다른 3K 지형 MP4는 정상 화면이고 scenario7에서 2950 policy가 여러 지형에서 정상 행동하므로 “boxes에서 로봇이 사라졌다”는 행동 해석은 성립하지 않는다.

**판별 방법:** boxes visual comparison이 꼭 필요할 때만 2950 boxes 한 편을 재렌더하면 된다. 현재 7050 채택 판단은 scenario7 계단/rough/slope 근거만으로도 바뀌지 않으므로 우선순위는 7450 evaluator보다 낮다.

---

## 8. checkpoint·가설·프로젝트 결정

### 8.1 checkpoint 판단

- 3K automatic best: `model_2000.pt`
- 3K 행동 comparator: `model_2950.pt` terminal-near checkpoint
- 7.5K automatic best/현재 행동 candidate: `model_7050.pt`
- 7.5K terminal: `model_7450.pt`, 행동 미확인

3K에서는 자동 best 2000보다 2950을 comparator로 쓴 것은 후기 terrain/XY 발전을 반영하는 목적과 맞는다. 7.5K에서는 7050 인접부가 terminal 인접부보다 terrain/yaw/base-contact/episode length가 더 균형적이고, 실제 행동평가도 강하다. 따라서 **현재 대표 행동 policy는 7050으로 유지**한다. 다만 “7.5K final은 7050”이라고 쓰지 않는다. final numbered checkpoint는 7450이다.

### 8.2 가설 판정

질문을 두 층으로 분리한다.

1. **`LINTRACK-125`를 3K보다 더 학습하면 정책 행동이 개선되는가? → PROMOTE.** 이 single-seed/config pair에서는 강한 YES다.
2. **`track_lin_vel_xy_exp=1.25`가 baseline 1.0보다 좋은 reward인가? → HOLD.** unchanged same-length BASE control 부재로 인과 판단 불가.

INVALID는 아니다. 두 Run은 정상 완료됐고 evidence identity도 충분하다. 단지 reward dial 자체에 필요한 대조군이 없는 것이다.

### 8.3 현재 정책의 장단점

**장점**

- forward/omnidirectional/rough/slope/push/randomized에서 tracking error가 일관되게 감소.
- 계단에서 survival, 전진, stall, 자세 RMS가 크게 개선.
- training terrain/base-contact/episode length 개선과 external behavior evaluator가 같은 방향을 지지.

**남은 약점/주의**

- yaw training scalar는 3K→7.5K에서 뚜렷한 개선이 아니다.
- 어려운 지형에서 action-delta가 증가해 더 공격적인 제어를 사용한다.
- 7450 terminal 행동 미평가.
- 2950 boxes visual evidence 결함.
- PERSONAL evaluator는 official score가 아니며 evaluator source가 OFFICIAL train source와 byte-identical하지 않다.

---

## 9. 다음 한 번의 행동

### 1순위 — 새 학습 없이 `model_7450.pt` 동일 scenario7 평가

**질문:** 7.5K의 late terminal이 7050의 계단/추종 개선을 유지하는가, 아니면 7050이 실제로 더 좋은 representative checkpoint인가?

- 대상: `model_7450.pt` SHA `b8766030…343a`
- 유지: 현재 7050 evaluation과 동일 evaluator build, protocol ID, 128 env, seeds 4201/4202/4203, scenario7, camera off
- 비교: 기존 `model_7050.pt` 결과 재사용
- 새 학습량: 없음
- 기대: 7450이 7050과 동등/개선이면 terminal 대표를 재검토; stairs/yaw/base-contact가 악화되면 7050 대표 유지
- 부작용/비용: GPU 평가 1회. 새 학습·렌더링 불필요.

이 결과가 현재 checkpoint 결정을 직접 바꾸므로 정보가치가 가장 크다.

### 2순위 — reward 인과 질문이 필요할 때만 unchanged BASE control

`LINTRACK-125` 자체를 채택/기각하려는 질문이라면 `track_lin_vel_xy_exp=1.0`의 same source/PPO/seed 42/4096 env fresh control을 동일 학습량과 evaluator 조건으로 만들어야 한다. 기존 3K↔7.5K pair는 그 질문에 답하지 않는다. 이 새 학습은 **현재 7050이 2950보다 좋은가**라는 정책 선택에는 필요하지 않다.

---

## 10. 한계와 재확인 가능한 근거 목록

### 직접 재계산/검증한 원본

- `20260928-230114-go2-lintrack125-fresh3k-r5-official-download.tar.gz`
- `20260929-154342-go2-lintrack-125-fresh7500-official-download.tar.gz.part1 + .part2`를 순서대로 결합해 tar.gz로 읽음; 원 part는 보존
- 각 nested evidence archive의:
  - `metadata.json`
  - `validation.json`
  - `command.txt`
  - `checkpoint_index.json`
  - `source/identity.json`
  - `source/quadruped_rewards.py`
  - `native_run/params/env.yaml`
  - `native_run/params/agent.yaml`
  - `native_run/events.out.tfevents.*`
- `model_2950_go2_6terrain_20261003-154646.zip`
- `model_7050_go2_6terrain_20261003-160918.zip`
- `model_2950_go2_evaluation_20261004-001124_8f0b655c.zip`
- `model_7050_go2_evaluation_20261004-004816_9981f1f5.zip`

### 프로젝트 문서와의 교차검증

- `00_START_HERE_CONTEXT_AND_MAP.md`: 현재 naming/legacy 경계, 기존 3K↔7.5K exact-match 상태
- `07_QUADRUPED_TRAINING_CODE.md`: `LINTRACK-125` 비교 해석 및 7050/7450 후보 원칙
- `16_EXPERIMENT_EXPORT_AND_TENSORBOARD.md`: raw TensorBoard/비교 규칙
- `17_ISSACSIMZ_VIDEO_OPERATIONS.md`: 영상 source checkpoint 경계
- `21_WINDOWS_GO2_VIDEO_AND_EVALUATION.md`: Windows 고정 6영상·scenario7 protocol과 PERSONAL/official-score 구분

### 한계

1. frozen `research/submission_presets/` 원본 파일은 이번 첨부 집합에 없어 preset 전체 byte diff를 새로 확인하지 못했다. Run resolved config 자체는 archive에서 직접 확정했다.
2. training은 seed 42 한 개다. evaluator seeds 4201–4203은 행동 robustness를 보강하지만 독립 training seed 반복이 아니다.
3. scenario7은 공식 evaluator가 아니며 평균오차→공식 Tracking Score 변환식도 적용하지 않았다.
4. 7050과 7450의 직접 행동 비교는 아직 없다.
5. 2950 boxes video는 검정 capture artifact라 해당 지형의 시각 A/B는 불가능하다.
6. 영상의 1 Hz 샘플과 full decode를 이용해 진행/자세/낙상 여부를 확인했지만, 영상에서 거리·각도·속도를 정밀 측정값으로 역산하지 않았다.

## 최종 의사결정

**정책:** `model_7050.pt`를 현재 `LINTRACK-125` 계보의 대표 행동 후보로 **PROMOTE**한다. 이번 자료에서는 `model_2950.pt`보다 명확히 낫고, 가장 큰 실질 개선은 계단에서의 stall/실패 감소다.

**가설:** “추가 학습 3K→7.5K가 이 config에서 유익하다”는 **PROMOTE**. “LINTRACK-125가 baseline reward보다 우수하다”는 **HOLD**.

**다음 행동:** 새 학습보다 먼저 `model_7450.pt`를 기존 7050과 동일 PERSONAL scenario7 프로토콜로 한 번 평가한다. 이것이 현재 대표 checkpoint 결정을 바꿀 가능성이 가장 큰 미해결 정보다.
