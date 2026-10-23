> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/incoming/other/reviewed/2026-09-17_H1_H005_GAIT025_FROM_H001_1P5K_DEEP_ANALYSIS.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# H1 H-005 GAIT025 from H-001 1.5K — Deep Analysis

> 분석 대상: `20260916-233344-h1-h005-gait025-from-h001-1p5k` train evidence + `20260916-235551-...-v` video evidence\
> 분석일: 2026-09-17\
> 환경 분류: **PERSONAL**\
> 최종 가설 판정: **HOLD**\
> 핵심 변경: H-001 계열 `termination_penalty=-50` 상태를 유지하면서 `feet_air_time 0.20 → 0.25`\
> 주의: 이 보고서는 개인 서버 run의 분석이며 공식 대회 성능 개선 또는 공식 점수 상승을 주장하지 않는다.

---

# 1. Executive Summary

이번 run은 H1 `Humanoid-v0`의 **fresh 1.5K가 아니라, 식별된 `model_1499.pt`에서 1,500회를 추가 학습한 resume/fine-tuning run**이다. 실행 metadata는 parent를 `H001_PARENT_1P5K_LOCKED`, parent checkpoint를 `model_1499.pt`, SHA-256을 `68fa0a9f...8f0c1`로 기록하며, 실제 학습 iteration은 **1499~2998**이다. 따라서 전체 lineage상 약 3K 지점에 도달했지만, curriculum이 재초기화되므로 fresh 3K trajectory와 동일하게 해석하면 안 된다.

실행 자체는 정상 완료됐다. Train evidence의 내부 SHA256SUMS **38/38**, video evidence **20/20**이 재검증됐고, exit code 0, TensorBoard event, 전체 console, 16개 checkpoint mirror, env.yaml, report.html, model_best, policy, video가 모두 보존됐다. 16개 checkpoint의 tensor를 직접 검사했을 때 NaN/Inf는 없고 action-std parameter도 모두 양수였다. PPO value loss는 median 약 **0.00504**, p99 약 **0.00578**, max **0.01056**으로 발산 신호가 없다.

학습 동역학에서 가장 중요한 현상은 **resume 직후의 curriculum reset/transient**이다. 첫 로그 terrain은 3.438이며 1515에서 3.132까지 내려간 뒤 빠르게 회복해 1727에 5.0, 1760에 과거 H-001 1.5K 참고값 5.119를 다시 넘었고, 후반 300회 평균 **5.422**, 마지막 100회 평균 **5.433**에서 plateau했다. 즉 이 run을 “3.44→5.44의 순수 능력 향상”으로 계산하면 안 되고, “resume reset 이후 높은 terrain 영역으로 재진입하고 그 상태를 유지했다”로 해석해야 한다.

`feet_air_time` reward component는 early-recovery 평균 0.00584에서 late 300 평균 **0.00859**로 약 47% 증가했다. 동시에 action-rate penalty는 거의 변하지 않았고, feet-slide penalty는 오히려 약간 완화됐으며, orientation penalty도 소폭 개선됐다. 따라서 수치상으로는 “발 체공을 늘리면서 무조건 난폭해진” 패턴은 아니다. 다만 이 변화는 reward weight 증가뿐 아니라 추가 1.5K 학습과 curriculum 재상승의 영향을 함께 받았기 때문에 `feet_air_time=0.25`의 단독 인과효과로 확정할 수 없다.

후반 정책은 base-contact termination 약 **30.5%**, timeout 약 **69.5%**, episode length 약 **772**, XY tracking error 약 **0.373**, yaw error 약 **1.029** 수준이다(last 300). Terrain이 올라가는 동안 XY/yaw tracking은 오히려 조금 회복했지만, base-contact가 확실히 개선됐다고 말할 근거는 약하다. 과거 project summary의 H-001 1.5K 참고값 terrain **5.119**, base-contact **32.41%**와 비교하면 현재 후반은 terrain이 더 높고 base-contact는 약간 낮은 방향이나, **동일 resume-control run이 아니므로 이 차이를 GAIT025 효과로 귀속하지 않는다.**

20초 play 영상은 source checkpoint SHA가 train의 `model_best.pt`와 직접 연결되어 있다. 영상에서 로봇은 전체 구간에서 대체로 upright 상태를 유지하고 alternating stepping과 한쪽 발 체공이 반복되지만, 장시간 한 발 들기·연속 hopping/bounding·명백한 prone survival 같은 reward hacking은 확인되지 않았다. 다만 영상은 단일 환경, 가변 command, 비고정 terrain 조건의 sanity check라 forward/lateral/yaw/stop 및 boxes/stairs/recovery를 정량 평가할 수 없다.

자동 `model_best.pt`는 reward peak step 2984에 가장 가까운 보존 checkpoint인 **`model_2998.pt`와 SHA-256이 완전히 동일**하다. 이번 run은 reward peak가 사실상 마지막 구간에 있어 “초반 peak 후 regression” 패턴은 아니다. 그러나 peak step 2984는 XY error 0.403, yaw error 1.099로 tracking 최적점도 아니다. 즉 reward-best와 tracking-best는 여전히 다른 개념이다.

최종 판정은 **HOLD**다. H-005는 실패 정책이 아니고 gait reward가 명백한 hacking을 만들었다는 증거도 없으며, terrain capability를 유지·확장할 가능성이 있다. 하지만 현재 가장 큰 실험 설계 병목은 **동일 parent에서 feet_air_time=0.20을 유지한 matched resume control이 없다는 것**이다. 다음 한 번의 학습으로 가장 많은 정보를 얻으려면 H-006(0.30)보다 먼저 동일 parent SHA에서 `feet_air_time=0.20` control을 똑같이 1.5K resume하여 H-005와 paired 비교해야 한다.

---

# 2. Run Identity & Evidence Integrity

## 2.1 실험 정체성

| 항목 | 확인 결과 | 근거 수준 |
|---|---|---|
| Robot | **H1 / Humanoid-v0** | 확인됨 |
| Experiment ID | **H-005 · GAIT025** | run name + 프로젝트 계획과 일치 |
| Train Run ID | `20260916-233344-h1-h005-gait025-from-h001-1p5k` | 확인됨 |
| Video Run ID | `20260916-235551-20260916-233344-h1-h005-gait025-from-h001-1p5k-v` | 확인됨 |
| Environment | **PERSONAL** | metadata `mode=personal` |
| Training type | **resume / fine-tuning** | `--resume --load_run ... --checkpoint model_1499.pt` |
| Parent run label | `H001_PARENT_1P5K_LOCKED` | 확인됨 |
| Parent checkpoint | `model_1499.pt` | 확인됨 |
| Parent checkpoint SHA-256 | `68fa0a9fe5334f8a3ecea110c4ccc9adb81ec07ac50169eaf8009b1a6e88f0c1` | runtime metadata 직접 기록 |
| Parent canonical H-001과 byte-level 동일성 | **판단 불가** | parent 원본 바이트/신뢰 manifest가 이번 archive에 없음 |
| Requested additional iterations | 1,500 | 명령/agent.yaml |
| 실제 console iteration | **1499~2998, 1,500개** | console/TensorBoard |
| lineage total iteration 의미 | 약 2,999 step까지 | 단, fresh 3K와 동등하지 않음 |
| last saved checkpoint | `model_2998.pt` | 확인됨 |
| selected model_best | `model_2998.pt`와 동일 SHA | 확인됨 |
| seed | 42 | env/agent/console |
| num_envs | 4096 | 명령/env/console |
| rollout | 24 steps/env/iteration | agent.yaml |
| transitions/iteration | 98,304 | 4096×24 계산 |
| headless | Yes | 명령 |
| camera during training | No 명시적 camera flag | 확인됨 |
| play camera | `--enable_cameras` | 확인됨 |
| training start/end metadata | 2026-09-16 23:33:44~23:53:46 UTC | metadata |
| KST 환산 | 2026-09-17 08:33:44~08:53:46 KST | 계산 |
| native training time | 1181.42 s (19m 41s) | console |
| evidence wrapper wall time | 약 20m 02s | metadata |
| report 표시 소요 | 20m 46s | report.html; metadata와 약간 불일치 |
| TensorBoard | 있음, 1 event | validation PASS |
| console 전체 | 있음, 1,500 learning iterations | 직접 확인 |
| checkpoint mirror | 16개: 1500~2900 + 2998 | 직접 확인 |
| policy.pt / ONNX | video evidence에서 생성 | 확인됨 |
| video | 1920×1080, H.264, 50 fps, 999 frames, 19.98 s | ffprobe |
| evaluator | 없음 | 판단 불가 |
| 공식 평가 | 없음 | PERSONAL run이므로 없음 |

### 중요한 provenance 해석

과거 프로젝트 계획에는 H-005/H-006이 “정확한 H-001 1.5K checkpoint가 없어 HOLD”로 기록되어 있었다. 이번 run은 실제 runtime에서 `H001_PARENT_1P5K_LOCKED/model_1499.pt`를 읽었고 그 SHA까지 남겼으므로 **실행 시 사용한 parent는 이제 고유하게 식별된다.** 다만 현재 받은 archive에는 그 parent checkpoint 원본 자체나 trusted H-001 archive와의 대응 manifest가 포함돼 있지 않다. 따라서 “이번 parent가 canonical H-001의 정확한 원본이다”는 stronger claim은 아직 **미확정**이다.

`metadata.resume_lineage.official_resume=true`라는 필드가 있지만 run의 `mode=personal`이 명확하므로, 이 필드를 근거로 run 자체를 OFFICIAL이라 부르지 않는다.

## 2.2 Evidence 무결성

- Train archive SHA-256: `6137bea5de6de45bd060e3cf3c01647ae533014030743dd4f82d302e4e8ebf35`
- Video archive SHA-256: `d0c823eb82d757e0b649ae5fd3228dc03b72ea2c09ceb8c008953d7958a07754`
- Train 내부 `SHA256SUMS`: **38/38 검증 성공**
- Video 내부 `SHA256SUMS`: **20/20 검증 성공**
- Train validation: **PASS**
- Video validation: **PASS**
- source identity: train.py, play.py, reward, env_cfg, agent_cfg, `_finalize.py` 등 before/after hash 동일
- source mutation during run: false
- train exit code: 0
- video exit code: 0

### 4개의 판단을 분리

1. **학습 프로세스 정상 종료:** PASS\
2. **evidence 정상 보존:** PASS\
3. **정책 품질:** 중간 이상 가능성은 있으나 검증 제한 → HOLD\
4. **공식 제출 후보 적합성:** PERSONAL 학습이므로 **공식 제출 정책 근거로 사용 불가**

Evidence PASS는 좋은 정책이라는 뜻이 아니다. 여기서는 “무엇을 했는지 신뢰할 수 있게 분석할 수 있다”는 의미다.

## 2.3 오류 / 경고 검사

### 학습

학습 console에서 다음 치명 오류는 발견되지 않았다.

- NaN / Inf 계산 오류: 없음
- CUDA OOM: 없음
- broken pipe: 없음
- optimizer/std runtime error: 없음
- checkpoint 저장 실패: 없음
- finalize 실패: 없음

경고는 deprecated config, headless display, PhysX/viewport 관련 일반 경고 위주다. 학습 완료 자체를 깨뜨린 근거는 없다.

### video

video console에는 `viewport_camera_controller.py`에서 `ManagerBasedRLEnv`의 `scene` attribute를 찾지 못하는 **callback Traceback**이 한 번 기록되어 있다. 그러나 process exit code는 0이고, fresh MP4가 생성됐으며 validation도 PASS다. 따라서 이 건은 **영상 생성 실패가 아니라 viewport-camera callback의 비치명 오류**로 분류한다. 다만 향후 영상 비교에서는 카메라 추적 동작이 동일한지 확인할 필요가 있다.

---

# 3. Configuration Verification

## 3.1 실제 적용 reward

`env.yaml`과 console의 active reward table이 일치한다.

| Reward | 실제 weight |
|---|---:|
| `track_lin_vel_xy_exp` | +0.5 |
| `track_ang_vel_z_exp` | +0.5 |
| `ang_vel_xy_l2` | -0.05 |
| `dof_torques_l2` | 0.0 |
| `dof_acc_l2` | -1.25e-7 |
| `action_rate_l2` | -0.0005 |
| **`feet_air_time`** | **+0.25** |
| `flat_orientation_l2` | -1.5 |
| `dof_pos_limits` | -1.0 |
| `termination_penalty` | -50.0 |
| `feet_slide` | -0.25 |
| `joint_deviation_hip` | -0.2 |
| `joint_deviation_arms` | -0.2 |
| `joint_deviation_torso` | -0.1 |

console은 14 active terms라고 표시하지만 `dof_torques_l2=0.0`이므로 **실질적인 non-zero reward는 13개**다.

## 3.2 H-005의 진짜 delta

자동 report는 배포 baseline과 비교하기 때문에 다음 두 항목을 변경으로 표시한다.

- `feet_air_time: 0.20 → 0.25`
- `termination_penalty: -5 → -50`

그러나 H-005의 intended parent는 이미 H-001 TERM50 계열이다. 따라서 **H-005 parent 대비 실질 delta는 `feet_air_time +0.05` 한 항목**으로 해석해야 한다. `termination_penalty=-50`은 H-005에서 새로 바뀐 값이 아니라 유지된 stability anchor다.

이 차이를 무시하면 “GAIT025+TERM50 두 reward 조합 실험”으로 잘못 기록하게 된다.

## 3.3 환경 / command / terrain

- physics dt: 0.005 s (200 Hz)
- decimation: 4
- control dt: 0.020 s (50 Hz)
- episode horizon: 20 s
- observation dimension: 256
- action dimension: 19
- terrain curriculum: enabled
- terrain grid: 10×20
- max initial terrain level: 5
- terrain generator seed: **null**
- patch size: 8×8 m
- horizontal/vertical scale: 0.1 / 0.005
- command resampling: 10 s
- command x: -1.0~+1.5 m/s
- command y: -0.5~+0.5 m/s
- yaw: -1.0~+1.0 rad/s
- standing env fraction: 0.02

Terrain proportions:

| Terrain | proportion |
|---|---:|
| pyramid stairs | 0.15 |
| inverted stairs | 0.15 |
| boxes | 0.30 |
| random rough | 0.10 |
| slope | 0.10 |
| inverted slope | 0.10 |

console은 배포 기본 terrain 비율에서 boxes 강화 등의 override가 적용되었음을 출력한다. 이것은 H-005 reward delta가 아니라 현재 H1 task environment의 설정이다.

## 3.4 PPO

- PPO, 5 epochs, 4 mini-batches
- initial LR 1e-3, adaptive schedule
- gamma 0.99, lambda 0.95
- entropy coef 0.008
- desired KL 0.01
- clip 0.2
- max grad norm 1.0
- actor/critic MLP: 512→256→128 ELU
- save interval 100
- `check_for_nan=true`

PPO 설정 변경 evidence는 없다.

---

# 4. Training Dynamics

## 4.1 raw TensorBoard 우선 원칙

분석은 report.html의 endpoint 카드보다 **raw TensorBoard 1,500 step 전체**를 우선했다. report의 best reward 3.48@2984, terrain 5.44, fall 약 29.2%는 raw event와 대체로 일치한다. 다만 report의 자동 해석 문구(예: std 1.x를 거의 미학습으로 보는 문장)는 정책 성공/실패 판정에 사용하지 않았다.

## 4.2 phase 분해

이번 run은 resume이므로 첫 100여 iteration은 정상 정책 성능을 직접 나타내지 않는다. 첫 로그에서 episode length 11.5, base-contact 0, tracking error 거의 0인 것은 정책이 갑자기 완벽해서가 아니라 **새 run 통계가 충분히 누적되기 전의 transient**다.

| Phase | iteration | 핵심 현상 |
|---|---:|---|
| Resume transient | 1499~1598 | episode/termination 통계 재형성, terrain 3.44 근처에서 시작 |
| Early curriculum recovery | 1599~1798 | terrain 4.04→5.18 급회복, H-001 1.5K 참고 terrain 5.119 재돌파 |
| Mid adaptation | 1799~2098 | terrain ~5.15 정체, tracking/episode 안정화 |
| Terrain recovery II | 2099~2398 | terrain 5.19→5.40로 재상승 |
| Late adaptation | 2399~2698 | terrain ~5.38, reward plateau/변동 |
| Late plateau | 2699~2998 | terrain ~5.42, reward 평균 상승, tracking 소폭 회복 |

## 4.3 terrain trajectory

- 첫 기록: 3.438
- 최소: **3.132 @ 1515**
- 4.0 최초: 1597
- 4.5 최초: 1647
- 5.0 최초: 1727
- **5.119 최초 재돌파: 1760**
- 5.2 최초: 2101
- 5.4 최초: 2503
- peak: **5.466 @ 2828**
- endpoint: 5.438
- last 100 mean: **5.433**
- last 300 mean: **5.422**

50-step moving average로 봐도 5.0 재진입은 1753, 5.4 도달은 2536이다. 따라서 후반 terrain 증가는 단일 spike가 아니라 지속적이다.

**해석:** resume reset 후 약 260 local iterations 만에 과거 H-001 1.5K 참고 수준 5.119를 다시 넘어갔고 이후 약 1,200 iterations 동안 5.1~5.46 영역을 유지했다. 이것은 정책 capability가 reset으로 완전히 붕괴하지 않았으며 높은 curriculum 구간에 재적응했다는 강한 증거다. 반면 terrain 5.4가 “level 5.4를 완전히 정복했다”는 뜻은 아니다. 이 값은 4096 env의 평균 curriculum state다.

## 4.4 mean reward

- min -0.138 @ 1506
- max **3.477 @ 2984**
- endpoint 2.412
- last 100 mean 2.784
- last 300 mean 2.694
- highest rolling-100 mean 2.795 (2886~2985)

peak가 최후반에 있고 rolling mean도 최후반에 가장 높다. 따라서 **후반 regression으로 학습 reward가 무너진 run은 아니다.** 다만 weight가 변경된 reward function이므로 H-001/다른 run의 mean_reward 절댓값과 직접 비교하지 않는다.

## 4.5 episode length / termination

last 300:

- mean episode length: **771.54 / 1000-step horizon scale**
- base-contact: **30.52%**
- timeout: **69.49%**

last 50:

- episode length: 786.15
- base-contact: 29.19%
- timeout: 70.81%

후반에 생존성이 급격히 악화되는 패턴은 없다. 다만 early-recovery base-contact 29.45% → late 30.52%로 아주 소폭 나빠져, `feet_air_time` 증가가 stability를 동시에 확실히 개선했다고 말할 수는 없다.

---

# 5. Tracking Analysis

## 5.1 Linear / XY

| 구간 | XY error mean |
|---|---:|
| early recovery 1599~1798 | 0.3916 |
| mid 1799~2098 | 0.3848 |
| 2099~2398 | 0.3822 |
| 2399~2698 | 0.3778 |
| late 2699~2998 | **0.3725** |
| last 100 | 0.3794 |
| endpoint | 0.3727 |

Terrain이 상승하는 동안 XY error는 장기적으로 소폭 감소했다. 즉 “더 어려운 terrain으로 올라가면서 linear tracking이 지속적으로 희생되는” 패턴은 보이지 않는다.

하지만 TensorBoard에는 x와 y error가 분리되어 있지 않으므로 **forward와 lateral tracking을 별도로 확정할 수 없다.**

## 5.2 Yaw

| 구간 | yaw error mean |
|---|---:|
| early recovery | 1.1083 |
| mid | 1.0747 |
| terrain recovery | 1.0615 |
| late adaptation | 1.0574 |
| late plateau | **1.0293** |
| endpoint | 0.9873 |

Yaw도 late phase에서 조금 회복했다. 다만 absolute error는 여전히 높은 편이고, 공식 TERM50 5K의 endpoint yaw error 0.935보다 수치상 크다. 하지만 OFFICIAL 5K와 PERSONAL resume 3K 계열은 서버/trajectory/조건이 달라 paired causal comparison이 아니다.

## 5.3 Stop behavior

이번 TensorBoard는 zero-command drift를 분리 기록하지 않았고, play 영상도 2% standing environment 여부와 command sequence가 고정/기록된 evaluator가 아니다. 따라서 다음 항목은 **판단 불가**다.

- zero command drift
- stop 후 흔들림
- stop→restart 안정성
- 회전 drift의 정량값

---

# 6. Stability Analysis

## 6.1 Fall / survival

후반 300회의 base-contact termination은 30.52%, timeout은 69.49%다. 한 endpoint만 보면 29.46% / 70.59%다.

과거 project summary의 H-001 1.5K 참고값은 terrain 5.119, base-contact 32.41%다. H-005 후반 평균은 terrain 5.422, base-contact 30.52%로 방향상 둘 다 더 좋아 보인다. 그러나 이 비교는 다음 이유로 인과 증거가 아니다.

1. H-005는 parent에서 **추가 1.5K 학습**했다.
2. resume으로 curriculum state가 reset됐다.
3. 동일 parent에서 reward를 바꾸지 않고 1.5K 더 학습한 control이 없다.
4. terrain generator seed가 null이다.

따라서 “feet_air_time 0.25가 낙상률을 1.9%p 줄였다”고 쓰면 과대해석이다.

## 6.2 Posture / body motion

후반 reward component 기준으로:

- `flat_orientation_l2`: early -0.01257 → late -0.01176 (penalty 약간 완화)
- `ang_vel_xy_l2`: -0.02168 → -0.02121 (거의 동일/소폭 개선)
- torso deviation: -0.00724 → -0.00647

체공 reward가 늘면서 orientation/body angular penalty가 함께 나빠지는 신호는 없다.

## 6.3 Sliding / smoothness

- feet_slide: early -0.04836 → late -0.04561
- action_rate: early -0.06243 → late -0.06236
- dof acceleration penalty도 소폭 완화

따라서 **더 큰 발 체공이 더 많은 sliding 또는 더 큰 action jerk로 직접 이어졌다는 수치 증거는 없다.**

## 6.4 Recovery / push

학습 환경 console에서 startup/reset external-force event는 존재하지만 이번 자료에는 push-specific evaluator metric가 없다. 따라서 push recovery 성능은 판단 불가다.

---

# 7. Terrain Analysis

Train curriculum은 6 terrain mixture에 대한 평균 level이며 terrain별 성공률은 기록하지 않는다. 따라서 다음은 분리해야 한다.

**확인됨:** 전체 curriculum 평균이 reset 후 5.43 수준까지 재상승하고 유지됨.\
**판단 불가:** boxes/stairs/slope 각각에서 실제 통과율이 개선됐는지.

영상에 stairs/box/rough 형태가 배경에 보이지만, camera trajectory와 command가 고정되지 않아 “boxes 성공”, “stairs 정복”이라고 판정하지 않는다. 특히 gait reward의 목적이 등반 capability라면 다음에는 terrain별 fixed evaluator가 필수다.

---

# 8. Reward Component Analysis

## 8.1 가장 큰 변화는 실제로 feet_air_time

resume transient를 제외한 early recovery(1599~1798)와 late plateau(2699~2998)를 비교한다.

| Component | Early mean | Late mean | 변화 |
|---|---:|---:|---:|
| track lin vel | +0.30588 | +0.30619 | 거의 동일 |
| track yaw | +0.14691 | +0.15289 | 소폭 증가 |
| **feet_air_time** | **+0.00584** | **+0.00859** | **+47.2%** |
| ang vel xy penalty | -0.02168 | -0.02121 | 소폭 완화 |
| dof acc penalty | -0.04606 | -0.04418 | 소폭 완화 |
| action rate penalty | -0.06243 | -0.06236 | 거의 동일 |
| flat orientation | -0.01257 | -0.01176 | 소폭 완화 |
| feet slide | -0.04836 | -0.04561 | 소폭 완화 |
| termination penalty component | -0.01967 | -0.02051 | 약간 악화 |

### 해석

정책은 H-005 fine-tuning 중 **발 체공과 관련된 행동을 분명히 더 많이 보상받는 상태로 이동**했다. 중요한 점은 그와 함께 action-rate, sliding, orientation이 뚜렷하게 악화되지 않았다는 것이다. 즉 reward component level에서는 “0.25가 즉시 hopping을 유발했다”는 신호가 없다.

반대로 termination component가 약간 더 negative하고 base-contact도 early 대비 late에 약간 올라간다. 따라서 gait 강화가 stability를 공짜로 개선했다고도 말할 수 없다.

## 8.2 correlation은 인과가 아니다

resume transient를 제외하면 terrain level과 XY/yaw error 사이에는 음의 상관이 관찰된다(terrain↑ 시 error↓ 방향). 그러나 iteration이 공통 시간 변수이므로 이 상관을 “terrain이 tracking을 개선했다” 또는 “feet_air_time이 tracking을 개선했다”는 인과로 쓰지 않는다.

---

# 9. PPO / Numerical Stability

## 9.1 Value loss

| 통계 | 값 |
|---|---:|
| median | 0.00504 |
| p90 | 0.00543 |
| p95 | 0.00553 |
| p99 | 0.00578 |
| max | **0.01056 @ 1519** |
| ≥0.05 횟수 | 0 |
| ≥0.1 횟수 | 0 |
| ≥1 횟수 | 0 |

Resume 초반의 max조차 0.011 이하이며 이후 즉시 정상대로 돌아간다. 반복적 value-loss explosion은 없다.

## 9.2 Surrogate / entropy / learning rate

- surrogate loss는 resume 첫 step의 +0.0079 이후 정상적인 음수대(-0.01~-0.014)로 안정
- entropy는 24.38 → 약 23.85로 매우 완만하게 감소
- adaptive learning rate는 초반 낮은 값에서 조정된 후 대체로 2e-4 수준, endpoint 2.96e-4

KL 자체는 TensorBoard tag로 제공되지 않아 직접 분석할 수 없다.

## 9.3 Action std

mean std는 1.33~1.36 범위, endpoint 1.342다. 자동 report는 이를 높은 값으로 경고하지만, 이 run에서 action std는 **발산 신호가 아니다.**

16개 checkpoint를 직접 검사한 결과:

- 모든 checkpoint actor/critic/optimizer tensor finite
- `distribution.std_param` min은 약 0.126~0.145 범위로 항상 양수
- final mean std 1.342, max dimension std 약 2.36

즉 “std가 1.34라서 거의 학습되지 않았다”는 단독 판정은 raw loss/terrain/episode/video와 모순되므로 채택하지 않는다.

## 9.4 Performance / GPU

console 1,500 iterations:

- total FPS median 약 128k, 평균 약 126.7k
- startup 포함 minimum 42.6k
- collection time median 약 0.684 s
- learning time median 약 0.082 s
- final iteration time 약 0.81 s
- native training time 1181.42 s

GPU sampler(약 2초 간격):

- GPU utilization 평균 53.8%, median 54%, p95 62%, max 70%
- VRAM median/max 5238 MiB
- power 평균 162.5 W, max 177.4 W
- GPU temp median 50°C, max 52°C

OOM/thermal throttling의 정황은 없다.

---

# 10. Checkpoint Analysis

## 10.1 보존 상태

mirrored checkpoint:

`1500, 1600, 1700, ..., 2900, 2998` — 총 16개.

모두 finite tensor이며 std parameter도 양수다.

## 10.2 model_best의 정체

raw reward peak:

- step **2984**
- reward **3.477294**

finalize 선택:

- `model_2998.pt`
- exported `model_best.pt` SHA-256 `fbc134fe...5549f`
- `model_2998.pt`와 hash exact match

이번 run에서는 best가 사실상 final checkpoint와 같다. 따라서 과거 장기 run에서 있었던 report scalar sampling mismatch 때문에 엉뚱한 오래된 checkpoint를 고른 문제는 이번 자료에서는 관찰되지 않았다.

## 10.3 reward-best ≠ tracking-best

step 2984의 주요 값:

- episode 853.1
- terrain 5.450
- base-contact 28.87%
- XY error 0.403
- yaw error 1.099
- feet_air reward 0.0100

endpoint 2998:

- episode 738.8
- terrain 5.438
- base-contact 29.46%
- XY error 0.373
- yaw error 0.987

즉 reward peak는 높은 생존/feet-air reward와 연결됐지만 tracking error는 final보다 나쁘다. **Train/mean_reward 최고가 tracking 최고를 의미하지 않는다.**

현재 자료만으로 제출 후보 checkpoint를 하나 고른다면 model_best=2998은 합리적인 후보이지만, 2800/2900/2998을 fixed evaluator에서 비교하지 않았으므로 “실제 locomotion 최고”라고 확정할 수 없다.

## 10.4 policy lineage

video evidence는 source checkpoint SHA를 `fbc134fe...5549f`로 기록한다. 생성된 `policy.pt`를 직접 로드해 확인한 결과:

- TorchScript input 256 → output 19 정상
- tensor finite
- policy의 8개 MLP weight/bias가 checkpoint actor MLP와 **exact tensor match**

따라서 이번 video가 다른/stale checkpoint에서 생성됐을 가능성은 매우 낮다.

---

# 11. Video / Behavioral Analysis

## 11.1 영상 provenance

- source checkpoint SHA: `fbc134fe...5549f`
- play video SHA: `97827307...51f7`
- H.264, 1920×1080, 50 fps
- 999 frames, 19.98 s
- num_envs=1
- headless + cameras

## 11.2 관찰된 행동

프레임을 시간 순으로 샘플링해 확인한 정성 관찰:

- 전체 구간에서 몸통이 대체로 upright 상태를 유지한다.
- 반복적인 좌/우 stepping과 single-support phase가 확인된다.
- 발을 이전보다 높은 위치로 들어 올리는 듯한 장면이 여러 번 보이나, 이 영상만으로 parent와의 체공 높이 차이를 정량화할 수 없다.
- **장시간 한 발을 들고 멈춰 있는 행동은 보이지 않는다.**
- **연속적인 두 발 동시 hopping/bounding을 주 보행 전략으로 사용하는 모습은 뚜렷하지 않다.**
- prone/side-lying 상태로 termination만 회피하는 local optimum은 보이지 않는다.
- 일부 순간 stance가 넓어지고 몸통 pitch/roll이 커지는 장면은 있으나 다시 보행으로 복귀한다.
- 지속적인 큰 foot sliding은 육안상 지배적인 패턴이 아니다.

## 11.3 영상으로 판단할 수 없는 것

command arrows는 변하지만 command sequence가 fixed benchmark가 아니므로 다음은 정량 판정하지 않는다.

- forward RMSE
- lateral RMSE
- yaw RMSE
- zero-command stop drift
- boxes/stairs traversal success
- push recovery
- terrain completion distance

따라서 영상은 **reward-hacking sanity check에는 유효하지만 evaluator 대체물은 아니다.**

---

# 12. Baseline / Parent Comparison

## 12.1 가장 직접적인 parent 비교

과거 project summary가 보존한 H-001 1.5K 참고값:

- terrain: **5.119**
- base-contact: **32.41%**

H-005 late 300:

- terrain: **5.422**
- base-contact: **30.52%**

표면적으로는 terrain +0.303, base-contact 약 -1.89%p 방향이다.

그러나 이것은 **paired reward effect가 아니다.** Parent는 iteration 1499 시점이고 H-005는 거기에서 1500회를 더 학습했다. `feet_air_time=0.20` 그대로 같은 parent에서 1500회를 더 학습한 control이 없으므로, 개선분 중 얼마가 단순 추가학습이고 얼마가 +0.05 reward 때문인지 분리할 수 없다.

## 12.2 공식 TERM50 5K와의 참고 비교

공식 TERM50 5K endpoint (별도 OFFICIAL run):

- terrain 5.825
- base-contact 28.93%
- timeout 71.07%
- episode 774.1
- XY 0.378
- yaw 0.935
- std 1.296

H-005 PERSONAL late300:

- terrain 5.422
- base-contact 30.52%
- timeout 69.49%
- episode 771.5
- XY 0.373
- yaw 1.029
- std 1.341

H-005는 XY/episode는 비슷한 범위지만 terrain/survival/yaw는 공식 5K anchor보다 아직 약하다. 이것은 “GAIT025가 나쁘다”는 증거가 아니라 **총 학습량·resume state·서버가 다른 run**의 descriptive comparison이다.

## 12.3 공식 평가와 연결 가능한 범위

H-001 TERM50 계열의 과거 공식 평가 기준선은 시뮬레이션 **56.37/70**이며 7시나리오가 대략 77.8~82.1% 범위였다. H-005는 PERSONAL run이고 동일 official evaluator가 없으므로 이 점수보다 올랐다고 주장할 수 없다.

---

# 13. Tracking vs Stability Trade-off

현재 evidence는 네 분류 중 하나로 억지로 고르면 안 된다.

- **Tracking:** run 내부 late phase에서 XY와 yaw가 완만히 개선됨.
- **Stability:** terrain은 확실히 상승/유지, episode는 유지되지만 base-contact는 early recovery 대비 뚜렷이 개선되지는 않음.
- **Parent 대비:** terrain/base-contact 방향은 긍정적이지만 matched control 부재.

따라서 정책 성격은 다음처럼 표현하는 것이 가장 정확하다.

> **Terrain/Gait capability ↑ 가능성, Tracking 유지~소폭 회복, Stability 대체로 유지.**\
> 다만 `feet_air_time=0.25`가 이 결과의 원인이라는 causal confidence는 낮다.

---

# 14. Local Optimum / Reward Hacking Check

| 위험 | 판정 | 근거 |
|---|---|---|
| 움직이지 않고 생존 | 낮음 | 영상에서 지속 locomotion, terrain curriculum 상승 |
| 비정상 자세로 termination 회피 | 낮음 | 영상 upright, base-contact 30% 수준 |
| hopping/bounding | **명백한 증거 없음** | 20초 영상에서 주 전략으로 보이지 않음 |
| 한 발 오래 들기 | 명백한 증거 없음 | alternating support 관찰 |
| sliding | 강한 증거 없음 | feet_slide penalty late 개선, 영상도 지배적 sliding 없음 |
| command 무시 | 판단 제한 | fixed command evaluator 없음 |
| terrain 회피 | 판단 제한 | curriculum 평균만 존재 |
| 지나친 소극성 | 낮음~판단 제한 | 움직임은 지속하지만 commanded speed 직접 비교 불가 |
| episode length만 긴 생존형 정책 | 낮음 | terrain 상승 + tracking error도 유지/회복 |

가장 우려했던 `feet_air_time` reward hacking은 **현재 0.25에서는 강하게 관찰되지 않았다.** 이것은 0.30도 안전하다는 뜻은 아니다.

---

# 15. Learning Phase / New Findings

## 발견 1 — resume transient가 매우 크다

iteration 1499 직후 episode length/tracking/termination 값은 run 누적통계가 비어 있어 정상 상태를 대표하지 않는다. 첫 100회를 parent 성능과 직접 비교하면 잘못된 결론을 낸다.

## 발견 2 — curriculum recovery는 두 단계다

- 1599~1798: 4.0→5.18의 빠른 recovery
- 2100 이후: 5.2→5.4의 느린 late adaptation

즉 단순히 reset 전 level을 복원한 뒤 끝난 것이 아니라, 복원 이후에도 terrain 평균이 추가 상승했다.

## 발견 3 — gait reward는 증가했지만 smoothness 비용은 거의 고정

feet-air component는 약 47% 증가했지만 action-rate penalty는 거의 변하지 않는다. 적어도 학습 metric 관점에서는 체공을 확보하기 위해 동작 변화량을 크게 희생한 정책은 아니다.

## 발견 4 — reward peak와 tracking quality가 어긋난다

2984 reward peak에서 XY/yaw가 final보다 나쁘다. 따라서 다음 checkpoint selection은 mean reward만이 아니라 evaluator 기반으로 해야 한다.

## 발견 5 — 과거 HOLD 사유가 일부 해소됐지만 provenance chain이 완전히 닫히지는 않았다

이번 evidence로 runtime parent checkpoint SHA는 확보됐다. 하지만 그 SHA가 canonical H-001 checkpoint와 동일하다는 trusted upstream manifest가 현재 첨부 bundle 안에는 없다. 이후 registry에서는 parent SHA를 기준으로 연결하고, 가능하면 원본 parent checkpoint 또는 canonical manifest를 함께 보존하는 것이 좋다.

---

# 16. Key Findings

중요도 순으로 정리하면 다음과 같다.

1. **H-005는 실제로 H-001-like 1.5K checkpoint에서 resume한 fine-tuning이며 fresh run이 아니다.** Curriculum reset 때문에 iteration 1499의 초기 지표를 parent 성능으로 읽으면 안 된다.
2. **실행/evidence 품질은 매우 좋다.** 38/38 + 20/20 hash 검증, full console/TensorBoard, 16 checkpoints, source immutability, checkpoint→policy→video lineage가 연결된다.
3. **후반 terrain capability는 안정적으로 5.42 수준까지 올라왔다.** reset 후 1760에서 5.119를 재돌파하고 마지막 300회 평균 5.422를 유지한다.
4. **feet_air_time component는 크게 증가했지만 action-rate/sliding/orientation은 악화되지 않았다.** 0.25에서 명백한 reward hacking은 수치/영상 양쪽에서 보이지 않는다.
5. **stability의 확실한 향상은 아직 아니다.** late base-contact가 약 30.5%이고 early recovery 대비 크게 내려가지 않는다.
6. **tracking은 terrain 상승과 함께 무너지지 않았다.** late XY 약 0.373, yaw 약 1.029으로 초중반보다 소폭 회복한다.
7. **model_best는 final 2998과 동일하지만 reward-best가 tracking-best는 아니다.** 2984 reward peak의 XY/yaw가 final보다 나쁘다.
8. **현재 가장 큰 병목은 reward 값이 아니라 실험 control 부재다.** 동일 parent에서 0.20을 그대로 1.5K 이어 학습하지 않았기 때문에 GAIT025의 순수 효과를 분리할 수 없다.

---

# 17. Final Decision

## **HOLD**

### PROMOTE하지 않는 이유

- PERSONAL run이라 공식 성능 승격 근거가 아니다.
- 동일 parent, 동일 resume reset, 동일 추가 iterations의 `feet_air_time=0.20` control이 없다.
- evaluator가 없어 gait/terrain별 실제 task capability를 분리할 수 없다.
- single seed다.

### REJECT하지 않는 이유

- terrain이 reset 후 강하게 회복되고 후반 plateau가 높다.
- base-contact/episode가 붕괴하지 않았다.
- PPO 수치 안정성이 매우 좋다.
- video에서 명백한 hopping, prone survival, 장시간 single-leg exploit가 보이지 않는다.
- tracking이 terrain progression과 함께 장기적으로 악화되지 않았다.

따라서 `feet_air_time=0.25`는 **계속 검증할 가치가 있는 후보지만 아직 causal winner가 아니다.**

---

# 18. Next Experiment

## 1순위 — 동일 parent의 `feet_air_time=0.20` resume control

가장 정보 효율이 높은 다음 실험은 **H-006(0.30)이 아니라 H-005의 matched control**이다.

### 목적

현재 관찰된 terrain 상승과 gait 변화가

- `feet_air_time 0.20→0.25` 때문인지,
- 아니면 H-001 checkpoint를 1.5K 더 학습했기 때문인지

분리한다.

### 설계

| 항목 | Control | H-005 |
|---|---|---|
| parent checkpoint SHA | **동일 `68fa0a9f...8f0c1`** | 현재와 동일 |
| reward | feet_air_time **0.20** | 0.25 |
| termination | -50 | -50 |
| seed | 42 | 42 |
| envs | 4096 | 4096 |
| additional iterations | 1500 | 1500 |
| resume mode | 동일 | 현재와 동일 |
| task/PPO/source | 동일 hash | 현재 hash |
| video/evaluator | 동일 조건 | 동일 조건 |

### 반드시 비교할 metric

1. terrain trajectory와 last-300
2. base-contact / timeout / episode length
3. XY/yaw error
4. feet_air_time component
5. feet_slide / action_rate / orientation
6. value loss p95/p99/max
7. `model_2800`, `2900`, final 같은 matched checkpoint evaluator
8. fixed-command play: forward / lateral / yaw / stop
9. fixed terrain: flat / rough / boxes / stairs / inverted stairs / slope ±10°

### 사전 성공 기준(공식 채점 기준이 아닌 engineering gate)

H-005를 0.20 control보다 유망하다고 보려면 최소한:

- terrain last-300이 control보다 지속적으로 높거나 terrain별 traversal이 개선될 것
- base-contact가 의미 있게 악화되지 않을 것
- XY/yaw tracking이 명확히 악화되지 않을 것
- hopping / prolonged single-leg / sliding이 나타나지 않을 것
- improvement가 endpoint 한 점이 아니라 last-window와 evaluator에서 재현될 것

수치 threshold를 임의로 사후 조정하지 말고 실행 전에 팀 기준을 고정하는 편이 좋다.

## 2순위 — H-006 `feet_air_time=0.30`

0.20 control 대비 H-005가 실제로 gait/terrain을 개선했다는 근거가 생긴 뒤 같은 parent에서 0.30을 실행한다. 0.30은 0.25 대비 marginal gain과 reward-hacking onset을 찾는 실험이다.

0.30에서 특히 볼 부작용:

- 한 발 장기 체공
- hopping/bounding
- feet_slide 증가
- action_rate 악화
- base-contact 증가
- yaw/stop 성능 악화

---

# 19. Confidence & Limitations

## 강한 근거

- run identity, command, resume source path/SHA
- PERSONAL 분류
- seed, envs, PPO, reward/environment 설정
- 1,500-step raw TensorBoard trajectory
- console 전체와 exit=0
- checkpoint 16개와 finite 검사
- model_best=2998 hash identity
- policy actor exact tensor match
- video source-checkpoint SHA linkage
- 영상에서 명백한 severe reward hacking 부재

## 중간 근거

- H-005 후반 terrain/stability가 H-001 1.5K 참고점보다 방향상 개선됐다는 해석
- `feet_air_time=0.25`가 gait를 강화하면서 smoothness를 크게 해치지 않았다는 해석

## 약한 정황 / 가설

- terrain 추가 상승의 원인이 feet_air_time +0.05라는 주장
- 특정 terrain(특히 boxes/stairs) capability가 개선됐다는 주장
- 공식 시나리오 점수 상승 예상

## 판단 불가

- forward와 lateral tracking의 개별 RMSE
- stop drift / restart
- push recovery
- terrain별 정량 성공률
- multi-seed 일반화
- official server 성능
- canonical H-001 원본과 parent SHA의 독립적 byte-level 연결

### Single seed 주의

이번 run은 seed 42 한 번이다. 방향성 evidence는 사용할 수 있지만 “최적값”, “통계적 개선”, “일반화”, “확정적 인과관계”라고 부르지 않는다.

---

# 20. 최종 질문 8개에 대한 답

1. **이 정책은 무엇을 배웠는가?**\
   Resume reset 후 기존 TERM50 기반 보행을 빠르게 회복하고, 높은 terrain 영역에서 발 체공 행동을 더 많이 사용하는 정책으로 적응했다.

2. **이전 정책보다 무엇이 실제로 좋아졌는가?**\
   확인 가능한 참고값 기준 terrain과 base-contact 방향은 좋아졌고, 후반 tracking도 유지됐다. 다만 reward 변경의 순수 효과로는 아직 분리되지 않았다.

3. **무엇을 잃었는가?**\
   뚜렷하게 잃은 capability는 현재 evidence에서 확인되지 않는다. 다만 yaw는 공식 장기 TERM50 anchor보다 수치상 약하고, stability가 추가 학습에 비해 크게 개선된 것도 아니다.

4. **학습 중 언제 중요한 변화가 일어났는가?**\
   1599~1798에서 curriculum이 가장 빠르게 회복했고, 2100 이후 두 번째 상승, 2500 이후 5.4 plateau에 들어간다.

5. **높은 지표가 실제 행동 개선을 의미하는가?**\
   Terrain/reward 상승은 영상의 정상 locomotion과 모순되지 않지만, fixed terrain evaluator가 없어 terrain 정복으로 확대 해석할 수 없다.

6. **현재 가장 큰 병목은 무엇인가?**\
   정책 자체보다 **matched control 부재**다. 0.25 효과와 추가학습 효과를 분리하지 못한다.

7. **이 가설은 계속 실험할 가치가 있는가?**\
   **있다 — HOLD.** 명백한 부작용이 없고 terrain/gait 방향이 긍정적이지만 control이 필요하다.

8. **다음 한 번의 학습으로 가장 많은 정보를 얻으려면?**\
   동일 parent SHA에서 `feet_air_time=0.20`을 유지한 1.5K resume control을 실행하고 H-005와 paired 비교한다.

---

# 21. Provenance / 사용한 근거

## 사용자 제공 원본 archive

1. `20260916-233344-h1-h005-gait025-from-h001-1p5k.tar(1).gz`\
   - SHA-256 `6137bea5de6de45bd060e3cf3c01647ae533014030743dd4f82d302e4e8ebf35`
   - train metadata, command, full console, TensorBoard, 16 checkpoints, env.yaml, report, source identity, GPU telemetry, validation

2. `20260916-235551-20260916-233344-h1-h005-gait025-from-h001-1p5k-v.tar(1).gz`\
   - SHA-256 `d0c823eb82d757e0b649ae5fd3228dc03b72ea2c09ceb8c008953d7958a07754`
   - video metadata, source checkpoint SHA, policy.pt/onnx, MP4, video manifest, console, validation

## 프로젝트 참고 자료

- `00_START_HERE_CONTEXT_AND_MAP`: H-001/H-004/H-005 계획 상태와 H-001 1.5K 참고 terrain/base-contact
- `13_H1_OFFICIAL_SERVER_BASELINE_EVIDENCE`: 공식 TERM50 5K 및 공식 2라운드 점수 기준선
- `14_H1_NEXT_RUN_PARAMETER_COMPARISON`: resume curriculum reset 해석과 H-005/H-006 parent 조건
- `15_OPTUNA_REWARD_DECISION_ENGINE`: gait reward 탐색 범위와 control 필요성
- `16_EXPERIMENT_EXPORT_AND_TENSORBOARD`: raw TensorBoard 우선, checkpoint/video provenance 원칙
- `18_H1_FINALIZE_REPORT_LIMITATIONS`: report/model_best 자동 해석의 한계
- `19_ISSACSIMZ_EXTERNAL_EVIDENCE_CLI`: evidence validation의 의미와 PERSONAL/OFFICIAL 분리

## 분석 중 생성한 중간 자료

TensorBoard scalar CSV와 프레임 contact sheet를 내부 계산/시각 판독에 사용했지만, 모든 핵심 수치·해석·결론은 이 Markdown 보고서 본문에 통합했다. 별도 CSV를 읽어야 결론을 이해할 필요는 없다.

---

## 최종 한 줄

**H-005 GAIT025는 수치적으로 안정적으로 학습되었고, resume reset 후 terrain 5.4대까지 회복·유지하며 `feet_air_time` 행동을 강화했지만 명백한 hopping은 보이지 않았다. 그러나 matched 0.20 resume-control이 없으므로 GAIT025의 순수 효과는 아직 증명되지 않았고, 현재 판정은 HOLD다.**
