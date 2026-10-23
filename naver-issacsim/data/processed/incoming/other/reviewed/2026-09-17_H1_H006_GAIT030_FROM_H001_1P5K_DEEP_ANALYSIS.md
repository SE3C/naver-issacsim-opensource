# H1 H-006 GAIT030 from H-001 1.5K — Deep Analysis

> **분석 대상**: `20260916-235914-h1-h006-gait030-from-h001-1p5k` 학습 evidence + 연결된 video evidence  
> **실험 분류**: **PERSONAL / resume fine-tuning / H1**  
> **가설 delta**: H-001 1.5K 부모에서 `feet_air_time: 0.20 → 0.30` **1개만 변경**  
> **최종 판정**: **HOLD**  
> **핵심 이유**: H-006은 수치적으로 정상 학습됐고 지형 curriculum 및 추종이 후반에 개선되며 영상상 명백한 hopping 붕괴도 보이지 않는다. 그러나 같은 부모에서 `feet_air_time=0.20`을 그대로 이어 학습한 matched control이 없어, 현재 개선이 **0.30의 효과인지 단순한 추가 1.5K 학습 효과인지 분리할 수 없다**. 또한 현재 영상은 자동 `model_best=model_2700` 한 개만 검증하며, 후반 `model_2900`/`model_2998`은 여러 행동 지표에서 더 경쟁력 있어 checkpoint 선택 자체도 아직 미완료다.

---

# 1. Executive Summary

이번 실행은 H1의 H-001 TERM50 계열 `model_1499.pt`에서 이어 학습한 **PERSONAL resume/fine-tuning run**이며, fresh 3K가 아니다. 부모 checkpoint는 SHA-256 `68fa0a9f…f0c1`로 명시되어 있고, 추가 1,500 iterations를 수행해 global console iteration `2998`까지 정상 완료했다. 실제 H-006 단일 변경은 `feet_air_time 0.20→0.30`이며 `termination_penalty=-50`은 부모에게서 이미 상속된 값이다.

실행과 evidence 보존은 매우 양호하다. exit code 0, NaN/Inf·CUDA OOM·broken pipe·traceback 없음, TensorBoard raw event 1개와 1,500-step 전체 scalar, 16개 checkpoint, env/agent 설정, source hash, GPU telemetry, report, linked video가 모두 보존되었고 내부 `SHA256SUMS`도 검증된다. Value loss는 steady 구간에서 median `0.00505`, p99 `0.00575`, max `0.00616`으로 사실상 spike가 없으며 PPO 학습은 수치적으로 안정적이었다.

정책 trajectory의 가장 큰 특징은 **resume curriculum reset → 빠른 재회복 → 느린 후반 개선**이다. 첫 raw terrain은 `3.438`, 최저 `3.135 @1516`까지 내려갔지만, 부모 1.5K의 알려진 terrain `5.119`를 `1757`에 다시 회복했고 이후 peak `5.523 @2877`, endpoint `5.491`까지 상승했다. 따라서 1.5K→3K 구간을 fresh trajectory의 단순 연속으로 보면 안 된다.

Tracking은 run 내부에서 점진적으로 좋아졌다. steady early window에서 XY error `0.3891`, yaw error `1.1121`이던 것이 last-300에서 각각 `0.3713`, `1.0249`로 낮아졌다. 반면 stability의 핵심인 base-contact termination은 `30.06% → 29.93%`로 거의 그대로여서, 이번 run의 본질은 **낙상률을 크게 낮춘 정책**이 아니라 **기존 TERM50 생존성을 대체로 유지하면서 terrain progression과 추종을 조금 더 끌어올린 정책**에 가깝다.

`feet_air_time` weighted reward는 early `0.00731`에서 last-300 `0.01174`로 약 60% 증가했다. 동시에 foot-slide·orientation·torso penalty는 나빠지지 않았고 action-rate penalty도 장기 평균은 거의 동일했다. 하지만 시간 추세를 제거한 residual 분석에서는 air-time이 평소보다 높게 튀는 순간 XY/yaw error와 action-rate 비용이 함께 악화되는 상관이 강하게 나타났다. 즉 **장기적으로는 gait가 성숙하지만, 순간적인 과도한 체공은 tracking/smoothness trade-off를 만들 가능성**이 있다.

자동 reward peak는 `3.959 @2670`이지만 저장 간격 때문에 `model_best.pt`는 `model_2700.pt`다. 이 peak 주변은 오히려 XY/yaw error와 action-rate가 후반보다 나쁘며, `model_2900` 및 `model_2998`의 trailing-window가 terrain/tracking/fall 조합에서 더 경쟁력 있다. 따라서 `model_best`를 최종 정책으로 자동 채택하면 안 된다.

19.98초 linked play 영상의 source는 정확히 `model_2700` hash와 연결된다. 영상에서는 로봇이 upright locomotion을 유지하고 뚜렷한 낙상, 장시간 한 발 고정, 양발 hopping, 옆으로 누워 생존하는 local optimum은 보이지 않는다. 다만 1 env·약 20초·자동 terrain/command 1회이며, stairs/boxes/slope/push/stop을 격리한 시험이 아니므로 H-006의 terrain 능력이나 공식 점수 개선을 주장할 수 없다.

결론적으로 H-006은 **REJECT할 만한 붕괴는 없지만 PROMOTE하기에는 인과 증거가 부족한 HOLD**다. 다음 한 번의 학습으로 가장 많은 정보를 얻는 방법은 동일 부모 SHA에서 `feet_air_time=0.20`을 그대로 둔 **matched resume control +1.5K**를 실행하는 것이다. 이것이 있어야 H-006의 후반 개선을 gait030 효과와 추가 학습 효과로 분리할 수 있다.

---

# 2. Run Identity & Evidence Integrity

## 2.1 실험 정체성

| 항목 | 확인 결과 | 근거 강도 |
|---|---|---|
| Robot / task | H1 / `Humanoid-v0` | 확인됨 |
| Experiment ID | H-006 · GAIT030 | 파일명·현재 delta·프로젝트 가설 문맥 일치 |
| Train Run ID | `20260916-235914-h1-h006-gait030-from-h001-1p5k` | 확인됨 |
| Video Run ID | `20260917-002012-20260916-235914-h1-h006-gait030-from-h001-1p5k-v` | 확인됨 |
| Environment | **PERSONAL** | `metadata.json mode=personal` |
| Training type | **resume / fine-tuning** | `--resume --load_run ... --checkpoint model_1499.pt` |
| Parent run label | `H001_PARENT_1P5K_LOCKED` | 확인됨 |
| Parent checkpoint | `model_1499.pt` | 확인됨 |
| Parent SHA-256 | `68fa0a9fe5334f8a3ecea110c4ccc9adb81ec07ac50169eaf8009b1a6e88f0c1` | 강한 lineage evidence |
| Requested additional iterations | 1500 | 확인됨 |
| Global start iteration | 1499 | metadata + TensorBoard |
| Last console iteration | 2998 (`2998/2999`) | 확인됨 |
| Last saved checkpoint | `model_2998.pt` | 확인됨 |
| Seed | 42 | env/agent 모두 일치 |
| num_envs | 4096 | 확인됨 |
| rollout steps/env/iter | 24 | 확인됨 |
| transitions/iteration | 98,304 | 계산값 |
| 이 run 신규 transitions | 147,456,000 | 98,304 × 1,500 |
| Train mode | `--headless`, camera 없음 | command 확인 |
| Video mode | 1 env, headless + `--enable_cameras`, 1000 frames | command 확인 |
| Train 시작/종료 KST | 2026-09-17 08:59:14 → 09:19:23 | UTC metadata +09:00 변환 |
| Video 시작/종료 KST | 09:20:12 → 09:21:32 | 확인됨 |
| TensorBoard | 존재, raw event 1개 | 확인됨 |
| Console | 전체 존재 | 확인됨 |
| Checkpoint | 16개 mirror 보존 | 확인됨 |
| Play video | 존재, source checkpoint SHA 연결 | 확인됨 |
| Evaluator | 없음 | 판단 불가 |
| 현재 run 공식 평가 점수 | 없음 | **없음** |

### 중요한 identity 해석

이 run은 이름에 `1p5k`가 들어 있지만 **1.5K fresh training이 아니다**. H-001의 1.5K checkpoint에서 **추가 1.5K**를 수행한 run이다. 전체 lineage의 global iteration은 약 3K 지점까지 가지만, resume 시 curriculum state가 부모의 raw trajectory를 그대로 유지하지 않아 fresh 3K와 같다고 볼 수 없다.

또한 metadata 내부에 `resume_lineage.official_resume=true`라는 중첩 필드가 있으나, run의 최상위 분류는 명시적으로 `mode=personal`이다. 이 필드는 **OFFICIAL 서버 실행 provenance를 증명하지 않으며**, 현재 run은 PERSONAL로 취급해야 한다.

## 2.2 archive / evidence 무결성

| 검사 | 결과 |
|---|---|
| Train archive SHA-256 | `eda221a1a6fe5c16e79ea6401d085c973eaa210e422e3444fdaf92e2da6d197d` |
| Video archive SHA-256 | `17e776120fa35d2220b51b65b1ca75b0e921c3ab514610a521a395f56d522ea1` |
| Train 내부 SHA256SUMS | 전체 일치 |
| Video 내부 SHA256SUMS | 전체 일치 |
| Evidence validation | Train PASS / Video PASS |
| source hash before/after | 동일, run 중 source 변경 없음 |
| exit code | 0 |
| finalize | completed |
| backup | `skipped_no_config`, PERSONAL에서 expected=false이므로 실패 아님 |
| TensorBoard | PASS, 1 event |
| checkpoint mirror | PASS, 16개 |
| env/model_best | NEW/MODIFIED로 fresh artifact 확인 |
| video | fresh non-empty `play_video.mp4` PASS |

### 네 가지를 분리한 판정

| 질문 | 판정 |
|---|---|
| 1. 학습 프로세스가 정상 종료됐는가? | **YES** |
| 2. Evidence가 정상 보존됐는가? | **YES, 매우 양호** |
| 3. 정책 자체가 좋은가? | **부분적으로 유망하나 미확정** |
| 4. 공식 제출 후보로 적합한가? | **현재 자료만으로 판단 불가 / PERSONAL** |

Evidence PASS는 정책 품질 PASS가 아니다. 이번 run은 오히려 이 구분이 잘 되는 사례다.

## 2.3 오류·발산 검사

전체 console과 raw scalar에서 다음 심각 오류는 발견되지 않았다.

- NaN/Inf 학습 붕괴: 없음
- CUDA OOM: 없음
- simulator fatal error: 없음
- broken pipe: 없음
- traceback: 없음
- optimizer/std invalid error: 없음
- checkpoint 저장 실패: 없음
- finalize 실패: 없음
- export 실패: 없음
- source mutation: 없음

Headless 환경 관련 warning과 일부 deprecation/config warning은 있으나 학습 종료나 scalar 품질을 훼손한 증거는 없다.

---

# 3. Configuration Verification

## 3.1 H-006의 실제 delta

가장 중요한 설정 해석은 **비교 기준을 무엇으로 두느냐**다.

| Reward | 배포 baseline | H-001 parent | H-006 | H-006의 parent 대비 delta |
|---|---:|---:|---:|---:|
| `track_lin_vel_xy_exp` | +0.50 | +0.50 | +0.50 | 0 |
| `track_ang_vel_z_exp` | +0.50 | +0.50 | +0.50 | 0 |
| `feet_air_time` | +0.20 | +0.20 | **+0.30** | **+0.10** |
| `termination_penalty` | -5 | **-50** | **-50** | 0 |
| `flat_orientation_l2` | -1.50 | -1.50 | -1.50 | 0 |
| `ang_vel_xy_l2` | -0.05 | -0.05 | -0.05 | 0 |
| `joint_deviation_hip` | -0.20 | -0.20 | -0.20 | 0 |
| `joint_deviation_torso` | -0.10 | -0.10 | -0.10 | 0 |
| `action_rate_l2` | -0.0005 | -0.0005 | -0.0005 | 0 |

따라서 **이번 실험의 인과적 질문은 `feet_air_time 0.20→0.30` 하나**다. `report.html`에는 배포 baseline 대비 `termination -5→-50`도 변경으로 표시되지만, 이는 H-006 run에서 새로 바뀐 값이 아니라 부모로부터 물려받은 설정이다. H-006을 “두 reward 동시 변경”으로 분류하면 실험 identity를 잘못 해석하게 된다.

## 3.2 실제 활성 reward

`env.yaml`에는 총 14개 항목이 scalar로 나타나며, `dof_torques_l2`는 weight 0이라 실질 nonzero reward는 13개다.

| 항목 | weight |
|---|---:|
| `track_lin_vel_xy_exp` | +0.5 |
| `track_ang_vel_z_exp` | +0.5 |
| `feet_air_time` | **+0.3** |
| `termination_penalty` | -50.0 |
| `flat_orientation_l2` | -1.5 |
| `ang_vel_xy_l2` | -0.05 |
| `joint_deviation_hip` | -0.2 |
| `joint_deviation_torso` | -0.1 |
| `action_rate_l2` | -0.0005 |
| `dof_acc_l2` | -1.25e-7 |
| `dof_pos_limits` | -1.0 |
| `feet_slide` | -0.25 |
| `joint_deviation_arms` | -0.2 |
| `dof_torques_l2` | 0.0 |

## 3.3 Environment / PPO 고정 조건

| 항목 | 값 |
|---|---|
| physics dt | 0.005 s (200 Hz) |
| decimation | 4 |
| policy/control interval | 0.020 s (50 Hz) |
| episode horizon | 20 s |
| command resampling | 10 s |
| command x | -1.0 ~ +1.5 m/s |
| command y | -0.5 ~ +0.5 m/s |
| command yaw | -1.0 ~ +1.0 rad/s |
| standing env ratio | 2% |
| obs/action | 256 / 19 |
| actor/critic hidden | 512→256→128, ELU |
| PPO epochs / minibatches | 5 / 4 |
| initial LR / schedule | 1e-3 / adaptive |
| gamma / lambda | 0.99 / 0.95 |
| entropy coefficient | 0.008 |
| desired KL | 0.01 |
| clip | 0.2 |
| max grad norm | 1.0 |
| save interval | 100 |
| NaN check | enabled |

PPO·task·terrain·command 관련 의도치 않은 변경 증거는 현재 bundle에서 발견되지 않았다. source hash도 run 전후 동일하다.

## 3.4 Terrain 설정

Curriculum은 활성화되어 있고 10×20 grid, patch 8m×8m, `max_init_terrain_level=5`, generator seed `null`, cache false다. raw proportion은 stairs 0.15, inverted stairs 0.15, boxes 0.30, random rough 0.10, slope 0.10, inverted slope 0.10이다.

`Curriculum/terrain_levels`는 다수 environment의 평균 난이도 지표다. 이를 “level 5.5 지형을 완전히 정복했다”로 해석하면 안 된다. 특히 terrain generator seed가 null이므로 다른 run과 완전한 deterministic paired terrain 비교도 보장되지 않는다.

---

# 4. Training Dynamics

## 4.1 Raw TensorBoard 범위

Raw event에는 `/time` 파생 태그를 제외하고 **29개 주요 scalar tag가 global step 1499~2998에 걸쳐 1,500개씩** 기록되어 있다. 이번 run은 25K 사례처럼 EventAccumulator 10,000-sample 제한에 걸릴 길이가 아니며, raw event와 `report.html`의 peak reward가 서로 일치한다.

주요 extrema:

| Metric | 값 | step |
|---|---:|---:|
| Train mean reward max | **3.958956** | **2670** |
| mean episode length max | **892.69** | **2670** |
| terrain minimum after resume | **3.1346** | **1516** |
| terrain maximum | **5.5227** | **2877** |
| base-contact maximum | **32.53%** | 1899 |
| XY error maximum | 0.4418 | 1979 |
| yaw error maximum | 1.2473 | 1550 |
| value loss maximum | **0.00616** | steady analysis상 비정상 spike 아님 |
| action std min/max | 1.3341 / 1.3531 | 매우 좁은 범위 |

## 4.2 resume warm-up을 성능으로 오해하면 안 되는 이유

step 1499~초기 수십 회의 episode 통계는 새 runner가 episode statistics를 다시 채우는 구간이다. 예를 들어 step 1499는 episode length 11.5, fall 0%, XY error 0.013처럼 비현실적으로 작다. 이는 부모 정책이 갑자기 극도로 좋아졌다는 뜻이 아니라 **통계 window가 아직 채워지지 않은 초기 상태**다.

따라서 성능 window는 step 1549 이후를 주 분석 대상으로 잡았다.

## 4.3 학습 phase

| Phase | 대략 step | 관찰 | 해석 |
|---|---:|---|---|
| P0. resume reset/warm-up | 1499~1548 | terrain 3.44→최저 3.13, episode 통계 급격히 채워짐 | curriculum/stat window reset. 정책 붕괴로 해석 금지 |
| P1. curriculum reacquisition | 1549~1757 | terrain 평균 4.56, 빠르게 5.119 회복 | 부모 능력에 맞는 난이도를 다시 찾아가는 단계 |
| P2. post-recovery adaptation | 1758~2298 | terrain 약 5.15→5.33, fall 약 30%, tracking 완만 개선 | 생존성은 정체, terrain과 yaw 적응 |
| P3. gait/tracking maturation | 2299~2698 | feet-air reward 상승, XY/yaw 감소, terrain 5.35대 | gait030 성향이 더 뚜렷해짐 |
| P4. late specialization | 2699~2998 | terrain 5.52 peak, XY/yaw 개선 유지, fall 약 30% | 수치 안정적. reward peak와 행동 peak 분리 |

### 핵심 change point: step 1757

부모 H-001 1.5K에서 알려진 terrain `5.119`를 H-006은 resume 직후 잃었다가 **step 1757에서 처음 다시 도달**한다. 즉 추가 학습의 앞 약 258 iterations는 상당 부분 “새 gait 가설 검증” 이전에 curriculum을 부모 난이도로 되돌리는 데 사용된 것으로 보는 편이 안전하다.

## 4.4 Window 통계

| Window | Terrain | Base-contact | XY err | Yaw err | Episode len | Mean reward | Std |
|---|---:|---:|---:|---:|---:|---:|---:|
| early 1549~1798 | 4.559 | 30.06% | 0.3891 | 1.1121 | 780.2 | 2.421 | 1.3408 |
| middle 1799~2298 | 5.222 | 30.17% | 0.3894 | 1.0941 | 774.8 | 2.378 | 1.3489 |
| late 2299~2698 | 5.357 | 30.39% | 0.3724 | 1.0430 | 765.6 | 2.604 | 1.3434 |
| **last-300 2699~2998** | **5.469** | **29.93%** | **0.3713** | **1.0249** | **774.2** | **2.870** | **1.3384** |
| last-100 2899~2998 | 5.487 | 30.17% | 0.3677 | 1.0134 | 773.0 | 2.929 | 1.3388 |

### 전체 trajectory 해석

- Terrain은 reset 회복 후에도 후반까지 완만하게 상승한다.
- XY와 yaw error는 middle 이후 실제로 감소한다.
- Base-contact는 30% 부근에서 거의 plateau다.
- Episode length도 약 770대에서 장기 개선이 뚜렷하지 않다.
- 즉 후반 정책은 **더 어려운 curriculum에서 비슷한 생존률을 유지하면서 tracking을 조금 개선**하는 쪽으로 발전했다.
- 아직 명확한 완전 plateau라고 단정하기 어렵지만, stability 자체는 이미 plateau 신호가 강하다.

---

# 5. Tracking Analysis

## 5.1 Linear tracking

Raw training scalar는 `error_vel_xy` 하나이므로 **forward x와 lateral y를 분리할 수 없다**. 현재 자료에서 x/y 각각의 RMSE를 만들어내면 추정값이 된다.

확인 가능한 것은 aggregate XY tracking이다.

- early mean: `0.3891`
- late mean: `0.3724`
- last-300 mean: `0.3713`
- last-100 mean: `0.3677`
- endpoint: `0.3670`

Early→last-300 변화는 약 `-0.0178`으로, run 내부에서는 tracking이 점진적으로 좋아졌다. 그러나 이것을 **feet_air_time=0.30의 인과 효과**라고 부를 수는 없다. 1.5K 추가 학습 자체가 함께 들어 있기 때문이다.

## 5.2 Yaw / turning

Yaw도 유사하다.

- early mean: `1.1121`
- middle: `1.0941`
- late: `1.0430`
- last-300: `1.0249`
- last-100: `1.0134`
- endpoint: `1.0287`

Run 내부 방향성은 개선이다. 다만 H-001 공식 TERM50 5K endpoint yaw `0.935`보다 현재 H-006의 3K-lineage 후반 값은 아직 높다. 이는 학습 길이·환경이 달라 H-006의 열세를 증명하는 비교가 아니라, **yaw 병목이 완전히 해결되지는 않았다**는 참고 수준이다.

## 5.3 Forward / lateral 개별 평가

**판단 불가.** Current TensorBoard에는 x와 y error가 분리되어 있지 않고, play video에도 command numeric log가 붙어 있지 않다. 공식 평가처럼 전진/좌우를 분리하려면 evaluator가 필요하다.

## 5.4 Stop behavior

**판단 불가.** Training config에 2% standing env는 있지만, 1-env 20초 영상에서 zero-command가 실제 샘플링됐다는 근거가 없다. 따라서 drift, stop 후 흔들림, 재출발 안정성을 평가할 수 없다.

## 5.5 Tracking 결론

**확인됨**: aggregate XY 및 yaw tracking은 H-006 추가 학습 중 후반으로 갈수록 개선.  
**판단 불가**: x/y 분리, stop, fixed command tracking, 공식 전진/좌우/회전 점수의 개선.

---

# 6. Stability Analysis

## 6.1 Fall / base-contact

Base-contact termination은 steady run 전반에서 약 30%로 매우 안정적으로 유지된다.

- early: 30.06%
- middle: 30.17%
- late: 30.39%
- last-300: 29.93%
- endpoint: 29.21%

endpoint 한 점만 보면 좋아 보이지만 last-window를 보면 큰 개선은 아니다. **이번 run이 낙상률을 크게 줄였다는 주장은 지지되지 않는다.**

## 6.2 Timeout / episode length

Last-300 timeout은 약 70.09%, episode length 774.2다. Early episode length 780.2와 사실상 비슷하다. 높은 timeout을 무조건 stability 개선으로 해석할 수는 없지만, 아래 terrain·tracking·영상과 함께 보면 “움직이지 않고 버티기” local optimum의 증거는 약하다.

## 6.3 Terrain progression

Terrain은 가장 뚜렷한 개선 축이다.

- resume 첫 값: 3.438
- minimum: 3.135 @1516
- parent terrain 5.119 재돌파: 1757
- last-300 mean: 5.469
- peak: 5.523 @2877
- endpoint: 5.491

그러나 이 값은 curriculum 평균이고, terrain type별 성공률이 아니다. 특히 play 영상은 특정 stairs/boxes/slope를 명시적으로 통과하는 fixed test가 아니므로 terrain level과 시각 성공을 직접 연결할 수 없다.

## 6.4 Posture / angular stability / slide / smoothness

Reward component 변화는 안정성 희생 신호가 크지 않음을 보조한다.

| Component (weighted) | Early | Last-300 | 방향 |
|---|---:|---:|---|
| `flat_orientation_l2` | -0.01266 | -0.01094 | 덜 나쁨 |
| `ang_vel_xy_l2` | -0.02174 | -0.02159 | 거의 동일 |
| `feet_slide` | -0.04708 | -0.04381 | 덜 나쁨 |
| `action_rate_l2` | -0.06333 | -0.06322 | 장기 평균 거의 동일 |
| `dof_acc_l2` | -0.04633 | -0.04493 | 소폭 덜 나쁨 |
| `joint_deviation_torso` | -0.00745 | -0.00622 | 덜 나쁨 |

따라서 gait reward를 0.30으로 올린 뒤 **장기 평균 posture/smoothness가 뚜렷하게 무너졌다는 증거는 없다**. 다만 뒤의 detrended 분석에서는 순간적으로 air-time이 높아질 때 action-rate/track 비용이 커지는 trade-off가 보인다.

## 6.5 Recovery / push

Push/recovery evaluator나 영상이 없으므로 **판단 불가**다. Parent TERM50 공식 정책의 과거 push 점수는 H-006의 결과로 이전해 쓸 수 없다.

---

# 7. Reward Component Analysis

## 7.1 주요 reward의 장기 변화

| Reward component | Early | Last-300 | 변화 |
|---|---:|---:|---:|
| `track_lin_vel_xy_exp` | 0.30734 | 0.30904 | +0.00170 |
| `track_ang_vel_z_exp` | 0.14672 | 0.15570 | +0.00898 |
| **`feet_air_time`** | **0.00731** | **0.01174** | **+0.00443 (~+60%)** |
| `flat_orientation_l2` | -0.01266 | -0.01094 | +0.00172 |
| `feet_slide` | -0.04708 | -0.04381 | +0.00327 |
| `action_rate_l2` | -0.06333 | -0.06322 | +0.00012 |
| `termination_penalty` | -0.01980 | -0.02004 | 거의 동일 |

### 해석

H-006이 실제로 학습한 가장 분명한 특성은 **더 많은 유효 발 체공 패턴**이다. `feet_air_time` component가 지속적으로 증가한다. 동시에 aggregate yaw tracking reward도 올라가고, orientation/slide는 악화되지 않는다. 이것만 보면 “gait030이 발을 더 들게 하면서 전체 locomotion을 망가뜨리지 않았다”는 방향성은 지지된다.

하지만 reward component 크기 자체는 서로 단위가 다르므로 “air reward가 작아서 중요하지 않다” 또는 “tracking reward가 더 커서 더 중요하다”처럼 절댓값 크기로 중요도를 판단하면 안 된다.

## 7.2 중요한 새 발견 — 시간 추세가 trade-off를 가리고 있었다

Step 1600 이후 단순 Pearson 상관을 보면 `feet_air_time`과 terrain이 `r≈+0.72`, yaw error가 `r≈-0.35`라서 air-time 증가가 tracking/terrain을 개선한 것처럼 보인다. 그러나 둘 다 “학습 시간이 지날수록 함께 좋아지는” 공통 trend가 있다.

선형 step trend를 각각 제거한 residual끼리 다시 보면:

| air-time residual vs | Pearson r | Spearman ρ | 해석 |
|---|---:|---:|---|
| terrain residual | +0.03 | -0.05 | 독립적 연관 거의 없음 |
| base-contact residual | -0.25 | -0.24 | 높은 air-time 순간에 fall이 약간 낮은 정황 |
| **XY error residual** | **+0.59** | **+0.59** | 평소보다 air-time이 높게 튀면 tracking이 나빠지는 경향 |
| **Yaw error residual** | **+0.72** | **+0.71** | 같은 trade-off가 더 강함 |
| **action-rate penalty residual** | **-0.75** | **-0.74** | air-time burst가 더 큰 action variation과 동반 |
| mean reward residual | +0.54 | +0.52 | 그럼에도 총 reward는 높아짐 |

이 결과는 인과 증명이 아니지만 매우 중요하다. **장기적으로 gait가 좋아지는 것과, 순간적으로 air-time을 과도하게 취하는 행동은 다른 현상**일 수 있다. 특히 총 reward가 높은 순간에 tracking/smoothness가 오히려 나빠질 수 있다는 점은 checkpoint 선택에도 직접 연결된다.

## 7.3 reward peak의 성격

`Train/mean_reward` peak step 2670:

- reward 3.959
- episode length 892.69 (run 최고)
- terrain 5.366
- fall 30.35%
- XY error 0.3914
- yaw error 1.1726
- air reward 0.01310
- action-rate penalty -0.07254

즉 peak는 **긴 episode + 높은 air-time + 높은 총 reward**를 만들었지만, 후반보다 tracking과 action smoothness가 좋지 않았다. 이것은 reward hacking이라고 단정할 정도는 아니지만, **mean reward peak가 실제 task optimum과 어긋나는 구체적인 사례**다.

---

# 8. PPO / Numerical Stability

## 8.1 Value loss

steady step 1549 이후 value loss:

- median: `0.00505`
- p95: `0.00554`
- p99: `0.00575`
- max: `0.00616`
- `>=0.01`: 0회
- `>=0.05`: 0회
- `>=1`: 0회

**이번 run에는 value-loss spike라고 부를 만한 사건이 없다.** Go2 장기 run에서 보였던 수십~수백 단위 spike와는 전혀 다른 상태다.

## 8.2 Surrogate / entropy / learning rate

- surrogate loss는 대략 -0.011~-0.012대에서 안정.
- entropy scalar는 early 평균 24.02, last-300 23.78로 완만히 낮아짐.
- adaptive LR는 여러 discrete level을 오가며 steady median 약 `1.98e-4`, 관측 min `1.73e-5`, max `2.96e-4`.
- desired KL은 config에 `0.01`이지만 **KL 자체 TensorBoard tag가 기록되지 않아 직접 분석 불가**.
- gradient norm도 tag가 없어 직접 확인 불가.

## 8.3 Action std

- early mean 1.3408
- middle 1.3489
- late 1.3434
- last-300 1.3384
- endpoint 1.3402

Std는 사실상 1.34 부근에서 plateau다. `report.html`은 이를 “무작위성이 안 줄어 거의 학습이 안 됨” 경고와 연결하지만, 현재 raw data에서는 terrain/tracking이 실제로 개선되고 loss도 안정적이며 play에서 locomotion도 확인된다. 따라서 **std 하나로 실패 판정하면 안 된다**.

오히려 이 branch에서는 parent로부터 이미 높은 std를 이어받았고, 추가 1.5K 동안 exploration variance를 크게 낮추지 않은 채 policy mean 자체를 다듬은 것으로 보는 것이 더 데이터에 부합한다. 다만 높은 std가 최종 robustness에 유리한지 불리한지는 evaluator 없이는 판단할 수 없다.

## 8.4 Checkpoint tensor finite 검사

`model_1500`, `model_2700`, `model_2998`을 직접 로드해 actor/critic/optimizer tensor를 확인했으며 non-finite tensor는 발견되지 않았다. `distribution.std_param`도 모두 finite 및 양수 범위로 유지됐다.

## 8.5 처리량 / GPU

Steady 구간:

- collection time median ≈ 0.691 s
- learning time median ≈ 0.082 s
- total FPS median ≈ 126,955
- total FPS p95 ≈ 129,322
- L40S GPU utilization median 53%, p95 61%, max 70%
- memory median/steady max ≈ 5,236 MiB
- power median ≈ 163 W, max 176 W
- GPU temp median 49°C, max 51°C

OOM이나 throttling/thermal pressure 정황은 없다. 학습 성능 변화가 하드웨어 자원 고갈로 생겼다는 근거도 없다.

---

# 9. Checkpoint Analysis

## 9.1 `model_best` identity

Finalize는 raw `Train/mean_reward` 최고 step `2670`을 찾고, 저장 간격 100에 가장 가까운 checkpoint인 `model_2700.pt`를 선택했다.

- `model_best.pt` SHA-256: `7099e0801d51983c3d5271c352cb70758c6c3ea046e4e3daefe02747025f7c18`
- `model_2700.pt` SHA-256: 동일
- final `model_2998.pt`: `d5af8527…` (별도 정책 state)

따라서 `model_best`는 **step 2670의 정확한 tensor state조차 아니다**. 30 updates 뒤의 model2700을 reward peak의 대표로 고른 것이다.

## 9.2 Late checkpoint 비교 — trailing 50 iterations

| Checkpoint | Terrain ↑ | Fall ↓ | XY err ↓ | Yaw err ↓ | Reward | Episode |
|---|---:|---:|---:|---:|---:|---:|
| 2300 | 5.316 | 30.15% | 0.3772 | 1.0702 | 2.410 | 766.5 |
| 2400 | 5.340 | 30.48% | 0.3757 | 1.0568 | 2.557 | 770.8 |
| 2500 | 5.353 | **29.20%** | 0.3690 | 1.0419 | 2.706 | 769.5 |
| 2600 | 5.371 | 31.45% | **0.3613** | 1.0120 | 2.572 | 749.0 |
| **2700 / model_best** | 5.365 | 30.50% | 0.3784 | 1.0550 | 2.737 | 775.2 |
| 2800 | 5.447 | 29.58% | 0.3713 | 1.0321 | 2.824 | 771.4 |
| 2900 | **5.514** | 30.26% | 0.3695 | **1.0136** | 2.823 | 766.1 |
| 2998 | 5.480 | 29.77% | 0.3680 | 1.0143 | **2.968** | **777.8** |

### 해석

자동 선택된 2700은 late candidates 가운데 특별히 우월하지 않다. 오히려:

- 2900은 terrain 및 yaw 측면에서 강함.
- 2998은 fall·XY·yaw가 2700보다 낫고 trailing reward/episode도 높음.
- 2800도 fall/terrain 균형이 좋음.
- 2500은 fall이 낮은 편이지만 terrain은 후반보다 낮음.

이런 다목적 지표에서는 여러 checkpoint가 Pareto-like trade-off를 만든다. **현재 evidence만으로 하나를 “최종 승자”로 고르는 것은 부적절**하다.

## 9.3 반드시 비교할 checkpoint

다음 평가 단계에서는 최소 `2700 (자동 best)`, `2900 (terrain/yaw 후보)`, `2998 (final 균형 후보)`를 동일 evaluator에서 비교해야 한다. 가능하면 `2800`도 포함한다.

이 비교는 새 학습이 아니라 기존 checkpoint evaluation이므로 서버 학습 시간을 추가로 쓰지 않고도 큰 정보를 얻을 수 있다.

---

# 10. Video / Behavioral Analysis

## 10.1 Video provenance

Video evidence는 source checkpoint SHA `7099e080…f7c18`을 명시하며 이는 `model_best=model_2700`과 동일하다. MP4 SHA는 `6243d091…ed31b`다.

ffprobe 확인:

- H.264
- 1920×1080
- 50 fps
- 999 frames
- 19.98 s
- 1 env

즉 영상 관찰은 **model_2700에만 적용**된다. `model_2900` 또는 final 2998의 행동을 이 영상으로 대신 판단할 수 없다.

## 10.2 직접 관찰

20초 영상의 여러 시점을 샘플링해 확인한 결과:

- 로봇은 전 구간 upright 상태를 유지한다.
- 명백한 낙상이나 옆으로 눕는 생존형 local optimum은 없다.
- 보행 시 무릎을 들어 swing leg를 만드는 gait가 확인된다.
- 한 발이 영구적으로 들린 상태로 고정되지는 않는다.
- 연속적으로 양발이 함께 튀는 명백한 bounding/hopping은 샘플에서 보이지 않는다.
- 몸통은 다소 역동적으로 기울지만, 영상상 즉시 불안정 붕괴 수준은 아니다.
- 명백한 제자리 정지 local optimum도 아니다. 실제 이동이 발생한다.

### `feet_air_time=0.30` reward-hacking 관점

현재 reward source 자체가 `0.3 이상에서 한 발 깡총/바운딩이 나타날 수 있음`을 경고한다. 이번 영상에서는 그 **명백한 형태는 확인되지 않았다**. 따라서 “0.30이 즉시 gait hacking을 일으켰다”는 가설은 현재 영상과 맞지 않는다.

그러나 다음 제한 때문에 reward hacking을 완전히 배제할 수 없다.

- 20초 1 env 한 번뿐이다.
- video source는 2700 한 checkpoint뿐이다.
- camera가 멀고 접촉 판독은 프레임만으로 제한적이다.
- fixed forward/lateral/yaw/stop command sequence가 아니다.
- 명시적 boxes/stairs/slope/push traversal가 아니다.

## 10.3 Terrain 행동

화면에는 여러 terrain patch가 보이지만, 이 영상은 특정 지형 통과 benchmark로 설계되지 않았다. 로봇이 주로 평탄한 구간을 이동하고 있어 **terrain 5.5라는 training scalar를 실제 stairs/boxes 정복으로 시각 검증하지 못했다**.

## 10.4 Video와 수치의 일치 여부

수치가 말하는 “약 30% base-contact”와 20초 단일 영상의 “낙상 없음”은 모순이 아니다. Training scalar는 4096 env에서 다양한 terrain/command를 평균한 값이고, 영상은 단 1 env의 한 episode다. 오히려 이 차이는 single play 영상만으로 stability를 과대평가하면 안 된다는 근거다.

---

# 11. Baseline / Parent Comparison

## 11.1 가장 중요한 비교 가능성 문제

현재 H-006은 부모 checkpoint 자체와 직접 paired continuation을 하지 않았다. 즉 다음 세 변화가 동시에 섞여 있다.

1. `feet_air_time 0.20→0.30`
2. **추가 1,500 PPO updates**
3. resume에 따른 **curriculum/stat reset 후 재적응**

따라서 “부모보다 H-006이 좋아졌으므로 air-time 0.30이 효과적”이라고 말하면 인과 과대해석이다.

## 11.2 H-001 1.5K parent와 방향성 비교

프로젝트의 이전 검증 요약에 있는 H-001 1.5K 지표:

- terrain ≈ 5.119
- base-contact ≈ 32.41%

H-006:

- last-300 terrain 5.469, final 5.491
- last-300 base-contact 29.93%, final 29.21%

표면적으로는 terrain이 약 +0.35, fall이 약 -2.5 percentage points 방향으로 좋아 보인다. 그러나 **parent endpoint 1점 vs child late-window + 추가 학습량** 비교라서 reward 효과로 귀속하지 않는다. 현재 자료에서 말할 수 있는 것은 “H-006이 부모 수준을 회복한 뒤 추가 progression을 보였고 생존성이 붕괴하지 않았다”까지다.

## 11.3 H-001 TERM50 5K long-run reference

과거 OFFICIAL TERM50 5K endpoint는 terrain 5.825, base-contact 28.93%, XY 0.378, yaw 0.935였다. 현재 H-006 last-100은 terrain 5.487, base-contact 30.17%, XY 0.368, yaw 1.013이다.

이 비교에서는 H-006이 XY는 비슷하거나 약간 낮고, terrain/fall/yaw는 아직 TERM50 5K reference보다 못하다. 하지만 H-006은 global 약 3K lineage이고 PERSONAL L40S이며, TERM50 reference는 OFFICIAL 5K이므로 **직접 우열 판정에 사용하면 안 된다**. 다만 “gait030이 3K에서 이미 TERM50 5K를 압도했다”는 주장은 자료와 맞지 않는다.

## 11.4 공식 Round2 score와의 관계

Parent TERM50 계열의 과거 공식 시뮬레이션 점수는 56.37/70이고 7개 scenario가 대략 77.8~82.1%였다. 현재 H-006은 공식 evaluator 결과가 없다. 따라서:

- 내부 terrain/XY/yaw 개선 ≠ 공식 점수 개선
- H-006이 official 56.37를 넘었다고 말할 수 없음
- 특히 전진/좌우/회전/rough/slope/push를 각각 분리 평가해야 함

현재 run은 **hypothesis screening evidence**로만 사용해야 한다.

---

# 12. Tracking vs Stability Trade-off

이번 정책을 강제로 네 quadrant 중 하나에 넣기보다, 축별로 분리하면 다음이 가장 정확하다.

| 축 | run 내부 변화 | 근거 |
|---|---|---|
| XY tracking | **개선** | 0.389→0.371 |
| yaw tracking | **개선** | 1.112→1.025 |
| terrain progression | **개선** | reset 후 5.12 재돌파, late 5.47 |
| fall/base-contact | **거의 동일** | 약 30% plateau |
| episode length | **거의 동일** | 약 770대 |
| smoothness 장기 평균 | **유지** | action-rate 거의 동일 |
| 순간적 aggressive gait | **trade-off 정황** | detrended air-time↑ 시 tracking/action-rate 악화 |

따라서 현재 H-006의 성격은 대략:

> **Tracking ↑ / Terrain capability proxy ↑ / Stability(fall) ≈ 유지**

즉 1번 “Tracking↑/Stability↑”라고 단정하기보다는 **Tracking↑, stability neutral, curriculum progression↑**가 더 정확하다.

---

# 13. Local Optimum / Reward Hacking Check

| 의심 패턴 | 현재 판정 | 근거 |
|---|---|---|
| 움직이지 않고 생존 | **증거 없음** | terrain/track + 영상 실제 이동 |
| 비정상 자세로 termination 회피 | **증거 없음** | 영상 upright |
| 한 발 영구 유지 | **명백한 증거 없음** | 여러 sampled frame에서 support leg 변화 |
| hopping/bounding | **명백한 증거 없음, 완전 배제 불가** | 20초 영상 한계 |
| sliding | **악화 증거 없음** | feet_slide penalty late에서 덜 나쁨 |
| command 무시 | **부분 판단 가능** | train aggregate tracking 개선, fixed command 영상 없음 |
| terrain 회피 | **판단 불가** | fixed terrain traversal 없음 |
| 지나친 소극성 | **증거 약함** | 실제 locomotion + terrain progression |
| reward component 하나만 과최적화 | **약한 경고** | air-time 증가, 순간적 tracking/smoothness trade-off |
| episode length만 긴 정책 | **아님** | terrain/track도 함께 개선 |

### 가장 중요한 reward-hacking 경고

`feet_air_time=0.30`은 현재 source comment상 이미 hopping 위험 경계에 들어간 값이다. 실제 영상에서는 붕괴가 없지만 residual 분석에서는 air-time burst가 tracking/action-rate 악화와 강하게 연결된다. 따라서 **0.30을 더 높이는 실험은 지금 단계에서 정보 효율이 낮고 위험하다**.

---

# 14. Key Findings

## 중요도 순 핵심 발견

1. **H-006은 valid한 resume fine-tuning run이다.** 부모 `model_1499.pt` SHA가 확보되어 이전 문서에서 “정확한 1.5K parent가 없어 HOLD”였던 provenance 문제는 이번 H-006 자체에 대해서는 해소됐다.
2. **Curriculum reset이 매우 선명하다.** terrain 5.119 수준의 부모에서 resume했지만 첫 값 3.44→3.13으로 내려간 뒤 step 1757에서 다시 부모 terrain 수준을 회복했다. 따라서 first ~258 updates를 단순 성능 regression으로 해석하면 안 된다.
3. **H-006은 stability를 크게 개선한 run이 아니다.** base-contact는 전체 steady 구간에서 약 30% plateau다. 핵심 변화는 terrain progression과 tracking의 후반 개선이다.
4. **feet-air 행동 자체는 실제로 강화됐다.** weighted air-time component가 early→last300 약 60% 증가했다. 영상에서도 swing leg가 분명하다.
5. **장기 평균으로는 gait 강화가 posture/smoothness를 무너뜨리지 않았다.** feet_slide/orientation/torso/action-rate가 악화되지 않았다.
6. **하지만 short-timescale trade-off가 존재한다.** 시간 추세를 제거하면 air-time이 평소보다 높게 튀는 순간 XY/yaw error 및 action-rate 비용이 함께 악화된다. 이 때문에 0.30 이상 증가는 특히 조심해야 한다.
7. **reward peak 2670은 behavior peak가 아니다.** 그 시점은 episode length와 air reward가 높지만 tracking과 action-rate가 후반보다 나쁘다.
8. **자동 model_best=2700은 최종 선택 근거가 약하다.** 2900/2998가 여러 행동 근접 지표에서 더 경쟁력 있어 evaluator 비교가 필요하다.
9. **PPO는 매우 안정적이었다.** value loss spike, NaN, std invalid, GPU resource pressure가 없어 현재 병목은 optimizer failure가 아니라 policy objective/selection 쪽이다.
10. **가장 큰 인과 공백은 matched control 부재다.** 현재 좋아진 부분을 `.30` reward의 효과와 +1.5K additional training 효과로 분리할 수 없다.

## 새로운 가설

### 가설 A — gait030의 이득은 “더 높은 air-time 자체”보다 후기 curriculum exposure와 결합될 때 나타난다

근거: raw air-time과 terrain은 장기적으로 함께 상승하지만 time-detrended residual 상관은 거의 0이다. 즉 air-time의 순간 상승이 terrain level을 직접 밀어올리는 신호는 약하고, 둘의 raw 상관 상당 부분은 공통 학습 시간 trend일 가능성이 있다.

### 가설 B — 0.30은 이미 tracking/smoothness trade-off 경계에 가깝다

근거: detrended air-time residual과 XY/yaw error, action-rate penalty의 강한 동시 악화. source comment의 hopping 경고와도 방향이 일치한다. 따라서 다음 탐색은 0.35/0.40 상향보다 0.20 control 또는 0.25 sibling이 더 유익하다.

### 가설 C — final checkpoint가 자동 model_best보다 실제 task에는 더 나을 수 있다

근거: model2700 trailing metrics보다 model2900/2998의 terrain/tracking/fall 조합이 전반적으로 경쟁력 있다. Reward peak가 long episode/air-time burst에 끌렸을 가능성이 있다.

---

# 15. Final Decision

## **HOLD**

### HOLD인 이유

**PROMOTE하기에는 부족한 점**

- matched `feet_air_time=0.20` resume control 없음
- single seed
- PERSONAL run
- fixed evaluator 없음
- forward/lateral/stop/push/terrain별 분리 측정 없음
- 영상이 model2700 한 checkpoint에만 연결됨
- model_best와 후반 checkpoint 사이 선택 문제 미해결

**REJECT하지 않는 이유**

- 학습/evidence 완전성 높음
- numerical failure 없음
- terrain progression 확실함
- XY/yaw tracking이 후반에 개선됨
- fall이 악화되지 않음
- linked video에서 명백한 hopping/immobility/abnormal survival 없음

따라서 H-006은 **“가능성은 있으나 causal proof와 evaluator가 부족한 gait 후보”**로 유지하는 것이 타당하다.

---

# 16. Next Experiment

## 16.1 1순위 — 가장 정보 효율이 높은 한 번의 학습

### `H-001-CONTROL-RESUME-1P5K`

**목적**: H-006의 개선이 `feet_air_time=0.30` 때문인지, 단순히 H-001을 1.5K 더 학습했기 때문인지 분리한다.

| 항목 | 제안 |
|---|---|
| Parent | **동일 SHA** `68fa0a9f…f0c1` (`model_1499.pt`) |
| Reward change | **없음** — `feet_air_time=0.20` 유지 |
| termination | -50 유지 |
| Additional iterations | 1500 |
| Seed | 42 |
| num_envs | 4096 |
| PPO / terrain / commands | H-006과 완전 동일 |
| Mode | PERSONAL screening이면 current H-006과 직접 비교 가능. OFFICIAL 성능 주장은 별도 official run에서만 |
| Headless / camera | train: headless camera off; video/evaluator 별도 |
| Evidence | raw event, full console, all checkpoints, exact parent SHA, env/hash, evaluator, linked videos |

### 왜 이것이 H-005(0.25)보다 우선인가

H-005 `.25`는 dose-response를 보여주지만, `.20 control`이 없으면 `.25`와 `.30` 둘 다 “추가 학습 효과”를 공유한다. 현재 가장 큰 불확실성은 **gait reward 효과와 추가 training 효과의 분리**이므로 control이 정보 가치가 더 높다.

H-001 control continuation이 이미 동일 조건으로 존재한다면 그때 다음 1순위는 **H-005 `.25` sibling**이다.

## 16.2 사전 성공/실패 기준

아래는 공식 채점 threshold가 아니라 **이번 실험을 비교하기 위한 사전 등록 기준**이다.

H-006 `.30`이 matched `.20` control 대비 다음을 만족하면 PROMOTE 근거가 강해진다.

1. last-300 terrain median이 control보다 명확히 높고, 최소 차이가 current within-window 변동보다 충분히 큼.
2. base-contact가 control보다 악화되지 않음. 실무상 `+1 percentage point` 이상 악화 시 경고.
3. XY error가 control보다 `+0.02 m/s` 이상 나빠지지 않음.
4. yaw error가 control보다 `+0.05 rad/s` 이상 나빠지지 않음.
5. 같은 fixed evaluator에서 boxes/stairs/rough/slope 중 최소 하나의 capability가 개선되고 worst terrain이 악화되지 않음.
6. stop command drift 및 push recovery가 악화되지 않음.
7. linked video에서 persistent one-leg hopping/bounding이 없음.

위 수치는 **의사결정용 제안 threshold**이며 공식 평가 기준이 아니다. 가능하면 단일 endpoint가 아니라 last-window 및 multi-seed evaluator로 판단한다.

## 16.3 학습 전에 먼저 할 “무료” 평가

새 학습을 돌리기 전 기존 checkpoint로 다음을 수행하는 것이 더 효율적이다.

- `model_2700`, `model_2900`, `model_2998` 동일 fixed evaluator
- forward / lateral / yaw / zero-command 분리
- flat / rough / boxes / stairs / inverted stairs / ±slope / push 분리
- 같은 seed set 사용
- video source SHA와 evaluator source checkpoint SHA 연결

이 비교에서 2900/2998이 2700을 반복적으로 앞서면 자동 `model_best` 선택을 버리고 checkpoint selection 절차를 별도 단계로 두어야 한다.

## 16.4 지금 하지 않는 것이 좋은 실험

- `feet_air_time`을 0.35/0.40 이상으로 바로 올리기
- gait reward와 tracking reward를 동시에 변경하기
- H-006에서 바로 `track_lin_vel`까지 올려 원인을 섞기
- Train/mean_reward만 보고 2700을 제출 후보로 고정하기

현재는 **원인 분리**가 추가 성능 욕심보다 정보 가치가 높다.

---

# 17. Confidence & Limitations

## 17.1 근거 수준

| 결론 | 수준 |
|---|---|
| run은 PERSONAL resume이며 parent SHA가 특정됨 | **강한 근거** |
| 학습 정상 완료 / evidence PASS / no NaN | **강한 근거** |
| 실제 delta는 parent 대비 feet_air_time +0.10 하나 | **강한 근거** |
| curriculum reset 후 step1757에 parent terrain 회복 | **강한 근거** |
| 후반 XY/yaw tracking 개선 | **강한 근거** |
| fall은 약 30%로 plateau | **강한 근거** |
| numerical optimization은 안정적 | **강한 근거** |
| model_best 2700이 행동 최적이 아닐 가능성 | **중간~강한 근거** |
| 0.30이 terrain 개선의 원인 | **약한 근거 / causal 판단 불가** |
| 0.30이 공식 점수를 개선 | **판단 불가** |
| forward/lateral/stop/push 개선 | **판단 불가** |
| terrain type별 capability 개선 | **판단 불가** |
| reward hacking 완전 부재 | **판단 불가; 명백한 형태만 미관찰** |

## 17.2 핵심 한계

- Single seed.
- Current run은 PERSONAL.
- H-006용 공식 evaluator 없음.
- Parent checkpoint의 original evidence bundle 자체가 이번 두 archive에 함께 포함되지는 않았고, current metadata에 parent SHA/경로가 기록된 형태다.
- Parent endpoint의 일부 비교 수치는 이전 프로젝트 검증 요약을 사용한다.
- Terrain generator seed가 null이라 run간 terrain realization 차이가 개입할 수 있다.
- Resume curriculum reset 때문에 fresh trajectory와 단순 연결 불가.
- Video는 model2700 1 env 19.98초뿐.
- Video command numeric sequence 및 terrain-specific success label 없음.
- TensorBoard에 KL/gradient norm/x-y 분리 error가 없음.
- Official score는 parent TERM50 과거 reference만 있고 H-006 자체에는 없음.

### 최종 신뢰도

- **Run identity / evidence integrity**: 99%
- **현재 run 내부 학습 dynamics**: 98%
- **behavioral qualitative 판단**: 88%
- **feet_air_time=0.30의 인과 효과**: 65% 이하 → 확정 결론을 내리지 않음
- **공식 대회 성능에 대한 결론**: 판단 불가

---

# Appendix A. Evidence & Provenance Inventory

## A.1 Current train bundle에서 직접 사용한 원본

- `metadata.json`
- `validation.json`
- `command.txt`
- `console.log`
- `SHA256SUMS`
- `source/identity.json`
- `source/humanoid_rewards.py`
- `native_run/events.out.tfevents...`
- `native_run/params/env.yaml`
- `native_run/params/agent.yaml`
- `native_run/git/IsaacLab.diff`
- `system/runtime.txt`
- `system/nvidia_smi_before.txt`
- `system/nvidia_smi_during.csv`
- `system/nvidia_smi_after.txt`
- `checkpoints/model_1500.pt` ~ `model_2998.pt`
- `collected/exported/model_best.pt`
- `collected/exported/env.yaml`
- `collected/exported/report.html`
- `collected/provenance.json`

## A.2 Current video bundle에서 직접 사용한 원본

- `metadata.json`
- `validation.json`
- `video_manifest.json`
- `command.txt`
- `collected/provenance.json`
- `collected/exported/play_video.mp4`
- `collected/exported/policy.pt`
- `collected/exported/policy.onnx`
- `SHA256SUMS`

## A.3 Project reference로만 사용한 과거 검증 자료

Current raw bundle에 없는 parent/official context를 위해 다음 project reference를 보조적으로 사용했다.

- `13_H1_OFFICIAL_SERVER_BASELINE_EVIDENCE...md`: H1 TERM50 5K endpoint 및 Round2 공식 점수
- `14_H1_NEXT_RUN_PARAMETER_COMPARISON...md`: H-005/H-006 sibling 설계, resume curriculum reset 주의
- `15_OPTUNA_REWARD_DECISION_ENGINE...md`: gait search range와 기존 HOLD 조건
- `16_EXPERIMENT_EXPORT_AND_TENSORBOARD...md`: raw event 우선, checkpoint/report 해석 원칙
- `18_H1_FINALIZE_REPORT_LIMITATIONS...md`: model_best/report 자동 판단 한계
- `06_HUMANOID_TRAINING_CODE...md`: H1 reward/environment historical context
- `00_START_HERE_CONTEXT_AND_MAP...md`: H-001/H-004 상태와 개인/공식 경계 요약

Current raw evidence와 과거 요약이 충돌할 경우 **이번 current archive의 직접 evidence를 우선**했다.

---

# Appendix B. Checkpoint Identity

| Checkpoint | SHA-256 (prefix) | 역할 |
|---|---|---|
| parent `model_1499.pt` | `68fa0a9fe533…f0c1` | H-001 1.5K source |
| model_1500 | `22f59a85…` | resume 직후 최초 mirror |
| model_1600 | `7b7d10d5…` | early |
| model_1700 | `4eea1ef4…` | curriculum reacquisition |
| model_1800 | `a3192764…` | parent terrain 회복 직후 |
| model_1900 | `1a1befa8…` | middle |
| model_2000 | `687fdcb8…` | middle |
| model_2100 | `1757db31…` | middle |
| model_2200 | `2ff8c92c…` | middle |
| model_2300 | `9e0f3c29…` | late |
| model_2400 | `686d7786…` | late |
| model_2500 | `b86c0420…` | low-fall candidate |
| model_2600 | `34fed74c…` | low-XY candidate |
| **model_2700 / model_best** | **`7099e080…f7c18`** | auto-selected / video source |
| model_2800 | `1177ff68…` | late balance candidate |
| **model_2900** | **`0a2f2c20…`** | terrain/yaw candidate |
| **model_2998** | **`d5af8527…`** | final candidate |

---

# Appendix C. 분석 방법

1. 두 tar.gz를 별도 디렉터리에 추출하고 archive SHA 및 내부 `SHA256SUMS`를 검증했다.
2. metadata/validation/provenance/source identity로 run lineage와 artifact freshness를 확정했다.
3. TensorBoard package의 요약값 대신 raw event TFRecord를 protobuf로 직접 읽어 scalar를 복원했다.
4. `/time` 파생 tag를 제외한 주요 29 tags를 global step 기준으로 pivot했다.
5. resume warm-up 1499~1548을 steady 성능 비교에서 제외했다.
6. early/middle/late/last-window를 run 길이와 curriculum 회복 시점을 기준으로 나눴다.
7. raw extrema, rolling/trailing windows, checkpoint 근처 50-step 평균을 비교했다.
8. Reward component는 동일 H-006 run 내부에서만 절댓값 변화를 해석했다.
9. Air-time trade-off 검사는 step 1600 이후 각 scalar의 선형 time trend를 제거한 residual 상관(Pearson/Spearman)을 추가로 계산했다. 이는 인과 검정이 아니라 confounding을 줄인 탐색 분석이다.
10. Checkpoint tensor는 대표 1500/2700/2998을 직접 로드해 actor/critic/optimizer finite 여부를 확인했다.
11. MP4는 provenance hash를 source checkpoint와 연결한 뒤 ffprobe와 시간대별 frame sampling으로 정성 검사했다.
12. Parent/official 비교는 current raw bundle에 없는 값이므로 프로젝트 내 기존 검증 문서의 확정값만 보조적으로 사용하고, current run의 official 성능처럼 표현하지 않았다.

---

## 최종 한 문장

**H-006은 `feet_air_time=0.30`에서 망가지지 않고 terrain·tracking이 후반 개선되는 유망한 gait fine-tuning 결과지만, 현재 가장 중요한 실험적 공백은 “동일 H-001 parent를 0.20 그대로 +1.5K 학습한 control”이 없다는 점이며, 다음 한 번의 학습은 그 control이 가장 많은 정보를 준다.**
