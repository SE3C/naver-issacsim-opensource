> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/incoming/other/reviewed/H1_H009_HIPDEV030_FROM_H008_3K_DEEP_ANALYSIS_20260920.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# H1 H-009 HIPDEV030 FROM H-008 3K — Deep Analysis

> **Run:** `20260918-010042-h1-h009-hipdev030-from-h008-3k`\
> **Robot:** H1 / `Humanoid-v0`\
> **Environment:** **PERSONAL** NVIDIA L40S\
> **Experiment hypothesis:** H-008 3K final에서 `joint_deviation_hip`만 `-0.20 → -0.30`으로 강화했을 때, tracking을 크게 잃지 않고 골반/보행 안정성을 개선하는가?\
> **Decision:** **HOLD**\
> **분석 기준:** 첨부 archive의 raw TensorBoard, console, env/agent 설정, reward source, checkpoint 21개, provenance/hash, GPU telemetry를 우선. 기존 프로젝트 문서는 parent/baseline 맥락에만 사용.

---

# 1. Executive Summary

이번 H-009는 **H-008 3K final `model_2998.pt`를 parent로 하는 PERSONAL resume/fine-tuning run**이며, 2,000 iteration을 추가해 global iteration `2998 → 4997`까지 정상 완료됐다. 실행 metadata가 기록한 parent SHA-256은 `d9a30c8a117f69cac49c4e640500f0fa8d88de72d6c61855f1e147ea6c1912ae`이고, 이번 child에서 바뀐 참가자 reward는 계획대로 `joint_deviation_hip -0.20 → -0.30` 하나로 확인된다.

학습 자체는 매우 안정적이었다. exit code는 `0`, TensorBoard는 2,000개 iteration을 모두 보존하며, NaN/Inf/OOM/broken pipe가 없고, 21개 checkpoint의 actor·critic·optimizer tensor는 전부 finite다. Value loss는 resume 직후 `0.0253`이 최고이고 이후 대부분 `0.006`대에 머물러 장기 발산 신호가 없다.

정책은 resume 직후 curriculum reset/재적응 구간을 거쳤다. terrain은 `3.44`에서 일시적으로 `3.17`까지 내려간 뒤 빠르게 회복해 50-iteration rolling mean 기준 global `3275`에서 `5.5`를 넘어섰고, 후반 500회 평균은 `5.596`이었다. 따라서 초반 낮은 terrain은 parent 능력 상실이라기보다 **resume 후 curriculum 재적응**으로 해석하는 것이 타당하다.

후반 정책은 terrain을 유지하면서 XY tracking이 약간 좋아지는 방향을 보였다. 마지막 500회 평균은 **XY error `0.3278`**, yaw error `1.3085`, base-contact `29.99%`, timeout `70.03%`, episode length `770.4`, terrain `5.596`이다. 마지막 500회 선형 추세에서도 XY와 yaw error는 소폭 감소하고 terrain은 소폭 증가했다. 즉 final 구간에서 joint collapse는 없다.

하지만 **`joint_deviation_hip -0.30`의 인과적 이득은 아직 강하게 확인되지 않는다.** 같은 H-008 3K parent에서 reward를 바꾸지 않고 +2K 이어간 H-008 continuation의 프로젝트 요약값은 late terrain `5.604`, XY `0.3314`, base-contact `29.67%`다. H-009의 last-500은 terrain `5.596`, XY `0.3278`, base-contact `29.99%`로 거의 같은 범위다. H-009가 XY는 약 `0.0036` 낮지만 terrain은 약 `0.008` 낮고 base-contact는 약 `0.32%p` 높다. 원본 H-008 continuation raw event를 이번 입력에서 재분석하지 못했으므로 엄밀한 paired 통계는 아니지만, 현재 근거만 보면 **hip penalty 강화가 성능 축을 크게 이동시켰다고 보기 어렵다.**

또한 yaw가 계속 병목이다. last-500 yaw error `1.3085`는 XY error `0.3278`보다 훨씬 크며, 후반 tracking reward에서도 yaw term은 약 `0.1245`, linear term은 약 `0.4812`다. 이 run은 hip penalty 강화로 yaw 병목을 해결하지 못했다.

가장 중요한 checkpoint 발견은 자동 `model_best.pt` 선택이 다시 신뢰하기 어렵다는 점이다. finalizer는 `reward 5.736 @ 3627 → model_3600.pt`를 선택했지만, raw TensorBoard 전체에서 실제 mean reward 최고는 **`5.978 @ 3041`**이다. 더 중요한 것은 그 `3041` 시점의 terrain이 `3.43`, yaw error가 `1.51`로 late policy보다 좋다고 보기 어렵다는 사실이다. 따라서 이번 run에서도 reward peak, `model_best`, 실제 제출/대표 정책은 서로 같은 개념이 아니다. **대표 checkpoint는 `model_4997.pt`를 기본값으로 유지하는 것이 더 타당하다.**

영상은 이번 archive에 H-009에서 새로 생성된 것으로 확인되지 않는다. `policy.pt`, `policy.onnx`, `play_video.mp4`는 provenance상 run 이전부터 존재한 **UNCHANGED artifact**다. 그러므로 그 파일을 H-009 행동 근거로 사용하면 안 된다. 이 때문에 hopping, foot dragging, stop drift, terrain별 실제 회복 동작은 현재 수치만으로 확정할 수 없다.

최종 판정은 **HOLD**다. 정책은 건강하고 final checkpoint는 좋은 분석 후보지만, `-0.30`이 unchanged control보다 의미 있게 우수하다는 증거가 부족하고, 실제 행동 영상/evaluator도 없다. 다음 한 번의 실험에서 가장 많은 정보를 얻으려면 **새 reward를 또 추가하기보다 같은 parent에서 `joint_deviation_hip=-0.10` sibling(H-011)을 동일 2K 조건으로 실행해 `-0.10 / -0.20 control / -0.30`의 방향성을 완성**하는 것이 가장 정보 효율적이다.

---

# 2. Run Identity & Evidence Integrity

## 2.1 실험 정체성

| 항목 | 확인 결과 | 근거 강도 |
|---|---|---|
| Robot | H1 / `Humanoid-v0` | 확인됨 |
| Experiment ID | H-009 · HIPDEV030 | 프로젝트 lineage + run name |
| Run ID | `20260918-010042-h1-h009-hipdev030-from-h008-3k` | 확인됨 |
| Environment | **PERSONAL** | metadata `mode=personal` |
| 실행 형태 | **resume / fine-tuning** | `--resume` |
| Parent | H-008 3K final | 확인됨 |
| Parent checkpoint | `model_2998.pt` | 확인됨 |
| Parent SHA-256 | `d9a30c8a117f69cac49c4e640500f0fa8d88de72d6c61855f1e147ea6c1912ae` | metadata에 기록 |
| Requested iterations | +2,000 | agent/command |
| 실제 TensorBoard 범위 | global `2998..4997` | raw event 직접 읽음 |
| 마지막 console iteration | `4997/4998` | console |
| 마지막 저장 checkpoint | `model_4997.pt` | archive |
| Seed | 42 | env/agent/console |
| num_envs | 4096 | env/console |
| rollout steps/env | 24 | agent.yaml |
| transitions/iteration | 98,304 | `4096 × 24` |
| 추가 transitions | 196,608,000 | 2,000 iterations |
| Headless | yes | command |
| Camera | 학습 중 camera 사용 근거 없음 | headless; recorder 0 |
| Run start | `2026-09-18T01:00:42.913700+00:00` | metadata |
| Run end | `2026-09-18T01:33:36.187969+00:00` | metadata |
| KST 환산 | 2026-09-18 10:00:42 ~ 10:33:36 KST | UTC+9 계산 |
| Native training time | 1,944.64 s | console |
| 전체 wrapper 시간 | 약 32분 53초 | metadata |
| Evidence validation | PASS | validation.json |

**중요:** metadata의 `resume_lineage.official_resume=true`라는 필드명은 이 run이 대회 **OFFICIAL 환경**이라는 뜻이 아니다. 상위 metadata의 `mode=personal`, 개인 L40S 경로, backup 설정 부재를 함께 보면 이번 실행은 명확히 PERSONAL이다. 이 필드를 환경 분류로 오해하면 안 된다.

## 2.2 아카이브 무결성

첨부 archive 자체 SHA-256:

```text
16f98464106cad8cfde7af39cbf22b70d89420df709af6ee26a2c246d241abe7
```

추출 후 `SHA256SUMS`에는 43개 파일이 기록되어 있고 **43/43 검증 통과**했다. 최상위 `SHA256SUMS` 자신을 포함해 실제 파일은 44개다.

아카이브에는 다음 핵심 원본이 존재한다.

- full `console.log` 약 3.6 MB
- TensorBoard event 1개 약 4.0 MB
- checkpoint 21개: `model_3000`부터 100회 간격 + `model_4997`
- `native_run/params/env.yaml`
- `native_run/params/agent.yaml`
- 실행 당시 `humanoid_rewards.py`
- source identity before/after hash
- IsaacLab git commit/diff
- GPU telemetry 972 samples
- finalizer output `report.html`, `env.yaml`, `model_best.pt`
- metadata / validation / provenance

따라서 **학습 프로세스 성공**, **evidence 보존 성공**, **정책 성능**, **제출 적합성**을 분리해서 판단할 수 있다.

## 2.3 실행 성공 / evidence / 정책 / 제출 적합성 분리

| 질문 | 판정 | 이유 |
|---|---|---|
| 학습 프로세스가 정상 종료됐는가? | **YES** | exit 0, global 4997까지 완료 |
| evidence가 정상 보존됐는가? | **YES** | validation PASS, raw event/console/checkpoints 포함 |
| 정책 자체가 좋은가? | **중간 이상, 단 확정 불가** | terrain 5.6대와 tracking 유지, 하지만 yaw 병목·약 30% base-contact |
| 공식 제출 후보인가? | **NO, 현재 자료로는 아님** | PERSONAL run이며 공식 점수/evaluator 없음 |

---

# 3. Configuration Verification

## 3.1 실제 reward 설정

raw `env.yaml`과 console은 동일한 14개 active reward term을 보여준다.

### 참가자 수정 대상 9개

| Reward | H-008 parent 기준 | H-009 | Delta |
|---|---:|---:|---:|
| `track_lin_vel_xy_exp` | 0.75 | 0.75 | 0 |
| `track_ang_vel_z_exp` | 0.50 | 0.50 | 0 |
| `feet_air_time` | 0.20 | 0.20 | 0 |
| `termination_penalty` | -50.0 | -50.0 | 0 |
| `flat_orientation_l2` | -1.5 | -1.5 | 0 |
| `ang_vel_xy_l2` | -0.05 | -0.05 | 0 |
| **`joint_deviation_hip`** | **-0.20** | **-0.30** | **-0.10 only** |
| `joint_deviation_torso` | -0.10 | -0.10 | 0 |
| `action_rate_l2` | -0.0005 | -0.0005 | 0 |

프로젝트의 H-009 계획 문서와 이번 archive의 source/env/console은 **`joint_deviation_hip` 하나만 더 negative로 강화한 실험**이라는 점에서 일치한다.

단, parent checkpoint bytes 자체는 이번 child archive에 포함되어 있지 않다. parent SHA가 metadata에 기록되어 있고 기존 프로젝트 기록의 H-008 3K final SHA와 일치하므로 lineage는 강하지만, 이번 한 archive만으로 parent bytes를 다시 hash하는 완전한 self-contained proof는 아니다.

## 3.2 framework 기본 reward

추가 active term:

- `dof_acc_l2 = -1.25e-7`
- `dof_pos_limits = -1.0`
- `feet_slide = -0.25`
- `joint_deviation_arms = -0.2`
- `dof_torques_l2 = 0.0`

분석 시 참가자 9개만 보고 행동을 설명하면 안 된다. 특히 slide, arm deviation, dof acceleration이 실제 gait dynamics에 계속 기여한다.

## 3.3 PPO 및 environment

| 설정 | 값 |
|---|---:|
| Physics dt | 0.005 s |
| Decimation | 4 |
| Control dt | 0.020 s |
| Episode horizon | 20 s |
| Observation dim | 256 |
| Action dim | 19 |
| Actor/Critic | 512 → 256 → 128, ELU |
| PPO epochs | 5 |
| mini-batches | 4 |
| LR | 0.001 initial, adaptive |
| gamma / lambda | 0.99 / 0.95 |
| entropy coef | 0.008 |
| desired KL | 0.01 |
| clip | 0.2 |
| max grad norm | 1.0 |
| NaN check | enabled |
| save interval | 100 |

Command ranges:

- x: `-1.0 ~ +1.5 m/s`
- y: `-0.5 ~ +0.5 m/s`
- yaw: `-1.0 ~ +1.0 rad/s`
- heading command enabled
- standing env ratio: `0.02`

## 3.4 Terrain

Curriculum enabled, 10×20 grid, 8×8 m patch.

| Terrain | proportion |
|---|---:|
| stairs | 0.15 |
| inverted stairs | 0.15 |
| boxes | 0.30 |
| random rough | 0.10 |
| slope | 0.10 |
| inverted slope | 0.10 |

합이 0.90이므로 framework 내부 정규화를 고려해야 하며, `Curriculum/terrain_levels`는 4096개 env의 평균 curriculum level이지 “level 5.6 지형을 전부 정복했다”는 뜻이 아니다.

Terrain generator seed가 `null`이고 cache도 false다. 따라서 같은 RL seed라도 terrain realization 차이가 남을 수 있다. 이 점은 sibling run과 작은 차이를 과대해석하지 않아야 하는 이유다.

---

# 4. Training Dynamics

Terrain curve〔원본 참조: `h009_report_assets/terrain.png` / 공개 사본 미포함〕

raw TensorBoard는 정확히 2,000개의 scalar point를 갖고 있으며 global step `2998..4997`을 연속 기록한다.

## 4.1 Phase 0 — resume reset / 재적응 (`2998~3047`)

첫 50회 평균:

| Metric | 평균 |
|---|---:|
| reward | 3.006 |
| episode length | 517.2 |
| terrain | 3.301 |
| XY error | 0.224 |
| yaw error | 0.900 |
| base-contact | 11.23% |
| timeout | 50.37% |

첫 iteration에는 episode length 11.5, XY error 0.013, yaw error 0.022처럼 비현실적으로 “좋아 보이는” 값이 나온다. 이는 충분한 episode가 아직 종료되지 않은 warm-up/aggregation 효과다. 첫 수십 iteration endpoint를 parent보다 우수하다고 읽으면 안 된다.

Terrain은 `3.438 @2998 → min 3.167 @3012`로 일시 후퇴한다. resume 시 curriculum이 parent의 기존 trajectory를 그대로 연속하지 않는다는 기존 경고와 일치한다.

## 4.2 Phase 1 — 빠른 curriculum 재상승 (`3048~3297`)

50-iteration rolling terrain이 처음으로:

- 3.5: global 3070
- 4.0: 3104
- 4.5: 3141
- 5.0: 3188
- 5.25: 3219
- 5.5: 3275

를 넘는다.

즉 약 300 global iteration 안에 high-terrain regime으로 복귀한다.

이 구간의 평균 reward는 `4.913`, episode length `805`, terrain `4.905`, base-contact `25.57%`. terrain이 올라갈수록 base-contact가 같이 증가하는 강한 동시 변화가 보이지만, 이는 정책이 어려운 지형에 더 많이 노출되는 curriculum interaction이 섞이므로 “hip penalty가 낙상을 늘렸다”라고 직접 인과 해석할 수 없다.

## 4.3 Phase 2 — high-terrain 정착 (`3298~3597`)

- terrain 평균 `5.578`
- XY `0.3365`
- yaw `1.3207`
- base-contact `29.65%`
- episode `768.9`

이 구간부터 정책은 새로운 안정 regime에 들어간다. terrain 분산이 크게 줄고, termination mix도 약 70% timeout / 30% base-contact 근처에서 안정된다.

## 4.4 Phase 3 — plateau / 정책 재조정 (`3598~4597`)

중기 500회:

- terrain `5.526`
- XY `0.3350`
- yaw `1.3264`
- base-contact `30.27%`

다음 500회:

- terrain `5.556`
- XY `0.3348`
- yaw `1.3289`
- base-contact `29.32%`

큰 성능 변화 없이 plateau에 가깝다. 다만 뒤 구간에서 base-contact는 소폭 내려가고 terrain은 약간 오른다.

## 4.5 Phase 4 — 후반 tracking 미세 개선 (`4598~4997`)

마지막 400회:

- terrain `5.605`
- XY `0.3269`
- yaw `1.3037`
- base-contact `30.07%`
- reward `4.528`

마지막 500회의 선형 추세(100 iteration당):

- terrain: `+0.0122`
- XY error: `-0.00129`
- yaw error: `-0.00461`
- reward: `+0.0341`
- base-contact: `+0.094%p`
- action std: `-0.00206`

즉 final window에서 **tracking은 아주 천천히 개선**, terrain은 유지/소폭 개선, stability는 사실상 평평하다. 학습을 더 길게 돌리면 엄청난 추가 개선이 기대되는 형태는 아니지만, 적어도 regression은 아니다.

---

# 5. Tracking Analysis

Tracking curve〔원본 참조: `h009_report_assets/tracking.png` / 공개 사본 미포함〕

## 5.1 Linear / XY tracking

Last-500:

- mean `0.3278`
- median `0.3279`
- last `0.3099`

중기 `3598~4097` 평균 `0.3350`에서 last-500 `0.3278`로 약 2.2% 감소했다. H-009 내부 trajectory에서는 **후반 XY 개선이 실재**한다.

단, forward와 lateral을 분리한 raw error scalar는 제공되지 않는다. `error_vel_xy`는 XY 결합 지표이므로:

- forward가 좋아졌는지
- lateral이 좋아졌는지
- 둘 중 하나가 다른 하나의 악화를 가렸는지

는 판단 불가다.

## 5.2 Yaw tracking

Last-500 mean yaw error `1.3085`, last `1.2478`.

중기 `1.3264`보다 조금 개선됐지만 여전히 절대적으로 크다. 이번 hip penalty 강화가 yaw tracking 병목을 해결했다는 근거는 없다.

XY와 yaw error는 high-terrain regime에서 상관계수 약 `0.81`로 같이 움직이는 경향이 있었다. 둘을 완전히 독립 능력으로 보기는 어렵지만, yaw의 error scale이 훨씬 큰 상태라는 점은 변하지 않는다.

## 5.3 Stop behavior

standing environment ratio가 `0.02`인 것은 확인된다. 하지만 zero-command 전용 drift metric, stop yaw drift, 재출발 성공률은 없다.

**판단: 불가.**

`episode length`가 길고 timeout이 많다는 사실을 stop 성능으로 대체해서는 안 된다.

## 5.4 Tracking 결론

- **강한 근거:** XY tracking은 late run에서 미세 개선.
- **강한 근거:** yaw는 계속 더 큰 병목.
- **판단 불가:** forward vs lateral 분리.
- **판단 불가:** stop drift / restart.
- **가설:** hip penalty 강화가 XY를 직접 개선했다기보다, late policy refinement와 curriculum 적응의 결과일 수 있음.

---

# 6. Stability Analysis

Termination curve〔원본 참조: `h009_report_assets/termination.png` / 공개 사본 미포함〕

## 6.1 Base-contact / timeout

Last-500:

- base-contact `29.99%`
- timeout `70.03%`

Last-10 base-contact 평균은 약 `29.72%`로 report의 29.7%와 일치한다.

이 수치는 “70% episode가 horizon까지 생존한다”는 뜻에 가깝지만, 그 자체가 정상 보행을 증명하지 않는다. 다만 terrain이 5.6대이고 tracking error가 유한/안정적이어서 Go2 G5처럼 “누워서 timeout만 버는” 극단적 survival local optimum의 수치 패턴과는 다르다.

## 6.2 Episode length

Last-500 mean `770.4 / 1000` environment steps.

20 ms control step이므로 최대 episode는 20 s다. Timeout fraction과 평균 episode length를 이용한 단순 mixture 근사에서는 fall episode 평균 종료 시점이 약 **4.7 s**로 추산된다. 이 값은 raw individual episode distribution이 아니라 aggregate algebra로 계산한 **근사값**이며, 정확한 fall-time 통계가 아니다.

의미는 분명하다. 실패하는 약 30%의 episode는 대체로 horizon 직전의 아주 작은 stumble만 있는 것이 아니라, 상당수는 비교적 이른 시점에 끝날 가능성이 있다.

## 6.3 Terrain

- raw max `5.672 @4795`
- endpoint `5.593`
- last-500 mean `5.596`
- last-300 mean `5.621`
- rolling-50 max `5.656 @4817`

따라서 endpoint 한 점이 아니라 후반 전체가 high-terrain regime이다.

## 6.4 Posture / gait smoothness

직접 posture angle, foot clearance, gait symmetry, contact timing scalar는 없다.

대신 reward component를 간접적으로 보면 last-500:

- `flat_orientation_l2 = -0.01228`
- `ang_vel_xy_l2 = -0.02539`
- `feet_slide = -0.04841`
- `action_rate_l2 = -0.07361`
- `feet_air_time = +0.00737`

중기 대비 late에서 orientation penalty magnitude는 약 8.8% 증가했지만, action-rate와 feet-slide는 거의 변하지 않았다. 즉 **후반 tracking 개선을 위해 동작이 급격히 거칠어졌다는 강한 신호는 없다.** 다만 orientation cost가 조금 커진 것은 몸통 자세 trade-off 후보로 남긴다.

## 6.5 Push recovery

학습 config에는 reset 시 external force/torque 이벤트가 있으나, push-specific recovery metric이나 evaluator가 없다.

**판단 불가.**

---

# 7. Reward Component Analysis

## 7.1 주요 component 변화

| Component | Mid (`3598~4097`) | Last-500 | 변화 |
|---|---:|---:|---:|
| linear tracking | +0.47539 | +0.48117 | +1.2% |
| yaw tracking | +0.12191 | +0.12448 | +2.1% |
| hip deviation | -0.04808 | -0.04672 | penalty magnitude -2.8% |
| action rate | -0.07369 | -0.07361 | 거의 동일 |
| feet air time | +0.00671 | +0.00737 | +9.9% |
| flat orientation | -0.01129 | -0.01228 | penalty magnitude +8.8% |
| feet slide | -0.04878 | -0.04841 | 약간 개선 |
| dof acceleration | -0.05557 | -0.05394 | 약간 개선 |
| termination | -0.02041 | -0.02010 | 거의 동일 |

`joint_deviation_hip` reward가 더 negative weight를 가짐에도 late weighted penalty magnitude가 중기보다 약간 줄었다. 이는 **정책이 hip deviation cost를 어느 정도 실제로 줄이는 방향으로 적응했다는 정황**이다.

하지만 이 값은 weighted reward term이다. H-008 `-0.20` control의 같은 raw component/underlying hip deviation이 없으므로 “-0.30이 실제 hip deviation을 X% 줄였다”고 주장할 수 없다.

## 7.2 Trade-off

관찰되는 가장 유력한 trade-off는:

**hip/posture control 강화 → late XY tracking 유지/미세 개선, terrain 유지 ↔ yaw 병목은 그대로, orientation cost 약간 증가**

이다.

다만 action rate가 악화되지 않았기 때문에 “골반 penalty 강화 때문에 다리가 경직되어 control smoothness가 무너졌다”는 신호는 없다.

## 7.3 Reward magnitude 해석 주의

H-009는 parent보다 `joint_deviation_hip` weight가 달라졌으므로, hip reward component 절댓값을 H-008과 그대로 비교하면 안 된다. 같은 underlying deviation이라도 weight가 1.5배이므로 component 값 자체가 달라질 수 있다.

---

# 8. PPO / Numerical Stability

Value loss〔원본 참조: `h009_report_assets/value_loss.png` / 공개 사본 미포함〕

## 8.1 Value loss

전체 2,000회:

- median `0.00648`
- p90 `0.00699`
- p95 `0.00714`
- p99 `0.00737`
- p99.9 `0.00800`
- max `0.02532 @2998`
- `>=0.01`: 2회
- `>=0.05`: 0회
- `>=0.1`: 0회

resume 첫 iteration이 최대이며 바로 회복한다. 반복적 spike나 발산 패턴이 없다.

**Numerical stability: 매우 양호.**

## 8.2 Surrogate / entropy / LR

- surrogate: 대부분 `-0.014` 근처
- entropy: `26.58 → 26.08`
- adaptive LR: `1e-5`에서 시작해 주로 `2.56e-4` 근처, final `1.71e-4`

학습률이 adaptive하게 변했지만 value loss나 std와 함께 붕괴하는 구간은 없다.

TensorBoard에 KL scalar 자체는 없다. desired KL은 `0.01` 설정으로만 확인되며 실제 KL trajectory는 **판단 불가**다.

## 8.3 Action std

mean std:

- first `1.4758`
- min `1.4345`
- last `1.4577`
- last-500 mean `1.4602`

평균만 보면 높다. 하지만 final checkpoint의 19개 action dimension별 `std_param`은:

```text
0.219, 0.221, 0.177, 0.472, 0.487,
2.212, 2.224, 0.327, 0.333,
2.489, 2.501, 0.519, 0.497,
2.525, 2.509, 2.464, 2.513, 2.510, 2.498
```

로 매우 비균일하다.

따라서 report의 “std 1.0 근처 → 거의 학습 안 됨” 식 단일 평균 경고는 이번 정책에 적용하기 어렵다. 일부 joint dimension은 낮은 exploration, 일부는 높은 exploration을 유지한다. 무엇보다 terrain/tracking/episode가 안정된 후반 regime을 같이 봐야 한다.

## 8.4 Checkpoint tensor health

21개 retained checkpoint 모두:

- actor finite
- critic finite
- optimizer state finite
- std positive/finite

였다.

장기 numerical instability 징후 없음.

## 8.5 Performance / GPU

TensorBoard:

- median FPS 약 `103,686`
- mean FPS 약 `103,261`
- collection median `0.850 s`
- learning median `0.097 s`

GPU telemetry 972 samples:

- GPU utilization mean 약 `43%`, median `44%`
- VRAM median `5236 MiB`
- power median 약 `140 W`
- temperature median `37°C`, max `39°C`

초기화/종료 idle sample이 포함되어 있으므로 steady-state utilization 자체를 policy 품질과 연결하면 안 된다. OOM이나 thermal throttling 징후는 없다.

---

# 9. Checkpoint Analysis

## 9.1 자동 best mismatch

Finalizer 출력:

```text
Best by Train/mean_reward: step 3627, reward 5.736 → model_3600.pt
```

하지만 raw TensorBoard 전체 직접 파싱 결과:

```text
global step 3041: reward 5.977645
global step 3044: reward 5.969421
global step 3108: reward 5.881795
...
global step 3627: reward 5.735898
```

즉 report/finalizer는 이번 2,000-scalar run에서도 실제 global max를 선택하지 않았다.

`model_best.pt` SHA-256은 `model_3600.pt`와 정확히 같다:

```text
6f735f5a78496f6b4ea7591e29837b9274516a3741618ecce2cbc29185fc3c40
```

## 9.2 reward peak가 좋은 checkpoint인가?

Raw reward max `3041`:

- reward `5.978`
- terrain `3.431`
- XY `0.350`
- yaw `1.508`
- base-contact `19.37%`
- timeout `80.63%`

자동 best 근처 `3627`:

- reward `5.736`
- terrain `5.530`
- XY `0.343`
- yaw `1.389`
- base-contact `30.10%`

Final `4997`:

- reward `4.454`
- terrain `5.593`
- XY `0.310`
- yaw `1.248`
- base-contact `29.50%`

즉 **mean reward가 가장 높은 시점은 curriculum이 아직 낮고 episode length/termination composition이 달랐던 재적응 초반**이다. 실제 task 관점에서는 final이 tracking과 terrain에서 더 균형적이다.

이것은 resume run에서 `model_best` 자동 선택이 curriculum reset에 크게 오염될 수 있음을 직접 보여준다.

## 9.3 대표 checkpoint

현재 데이터에서:

- 학습 reward 최고: early `~3041`
- 자동 model_best: `model_3600`
- terrain peak 근처: `model_4800` 주변
- tracking best late candidate: `model_4997` / `4900` 근처
- 최종 대표: **`model_4997.pt`**

마지막 수백 iteration에서 terrain·tracking·fall이 함께 악화하지 않았으므로 기존 프로젝트의 “충분히 긴 resume는 final numbered checkpoint를 기본 대표로” 규칙과도 일치한다.

**주의:** 이번 archive의 기존 `policy.pt`는 H-009에서 새로 export된 것이 아니다.

---

# 10. Video / Behavioral Analysis

이번 run 자체의 H-009 video evidence는 **없다**고 판단해야 한다.

`collected/provenance.json`에서:

- `policy.pt`: UNCHANGED
- `policy.onnx`: UNCHANGED
- `play_video.mp4`: UNCHANGED

이다.

즉 exported 폴더에 파일이 존재한다는 사실과, 이번 H-009 checkpoint에서 새로 생성되었다는 사실은 다르다.

따라서 현재 판단 가능한 행동:

- terrain curriculum에서 장시간 학습 안정: 수치로 확인
- command tracking: aggregate scalar로 확인
- 실제 upright gait: H-009에 대해서는 직접 확인 불가
- hopping: 판단 불가
- one-leg stance: 판단 불가
- foot dragging: 판단 불가
- sliding visual severity: 판단 불가
- stop drift: 판단 불가
- turn-in-place: 판단 불가
- boxes/stairs/slopes 실제 통과: 판단 불가
- push recovery visual behavior: 판단 불가

H-008 parent의 기존 six-terrain 영상은 parent sanity evidence일 뿐, H-009 `-0.30`의 행동 증거가 아니다.

---

# 11. Baseline / Parent Comparison

## 11.1 가장 적절한 control

가장 중요한 비교는 **같은 H-008 3K parent `model_2998`에서 reward 변경 없이 +2K한 H-008 continuation**이다.

현재 프로젝트 요약에 남은 H-008 unchanged +2K late 수치:

- terrain `5.604`
- XY `0.3314`
- base-contact `29.67%`

H-009 raw last-500:

- terrain `5.596`
- XY `0.3278`
- base-contact `29.99%`

비교:

| Metric | H-008 unchanged continuation | H-009 hip -0.30 | 차이 | 해석 |
|---|---:|---:|---:|---|
| Terrain | 5.604 | 5.596 | -0.008 | 사실상 동일 |
| XY error | 0.3314 | 0.3278 | -0.0036 | H-009 미세 우세 |
| Base-contact | 29.67% | 29.99% | +0.32%p | H-009 미세 열세 |
| Yaw | raw control 값 미확보 | 1.3085 | 비교 불가 | — |

이 정도 차이는 terrain randomization, stochastic PPO, window 정의 차이로도 충분히 나올 수 있다. 따라서 **H-009가 control을 이겼다고 선언할 수 없다.**

오히려 현재 가장 강한 결론은:

> `joint_deviation_hip=-0.30`은 기존 H-008 성능을 크게 망가뜨리지 않았지만, 눈에 띄는 aggregate 성능 gain도 만들지 않았다.

이다.

## 11.2 공식 TERM50 anchor와의 비교

공식 TERM50 5K endpoint는 프로젝트 기록상:

- terrain `5.825`
- XY `0.378`
- yaw `0.935`
- base-contact `28.93%`

H-009와 직접 비교하면 H-009는 XY가 좋고 yaw는 나쁘며 terrain은 조금 낮다. 그러나:

- H-009는 PERSONAL L40S
- TERM50은 OFFICIAL RTX 5080
- parent/reward lineage 다름
- H-009는 resume
- TERM50은 별도 run
- terrain realization 다름

이므로 **causal baseline 비교가 아니다.** 정책 성격의 참고점일 뿐이다.

## 11.3 Single seed

H-009는 seed 42 한 번이다. terrain generator seed는 null이다. 따라서:

- 통계적 개선
- 최적 weight
- 일반화
- 대회 성능 향상

을 주장할 수 없다.

---

# 12. Tracking vs Stability Trade-off

현재 정책은 억지로 1~4 중 하나를 고르면 안 된다.

### Tracking

- XY: late 개선, 양호
- yaw: 병목 유지
- forward/lateral 분리: 불가
- stop: 불가

### Stability

- terrain: 높고 안정
- base-contact: 약 30%, 뚜렷한 개선 없음
- episode length: 약 770
- recovery: 직접 metric 없음
- gait smoothness: action-rate는 안정
- posture: orientation penalty는 late 약간 증가

따라서 성격은:

> **XY tracking은 소폭 ↑ / terrain은 유지 / fall은 거의 동일 / yaw는 여전히 약함**

에 가깝다.

즉 “Tracking ↑ / Stability ↑”라고 부르기에는 stability gain이 부족하고, “Tracking ↑ / Stability ↓”라고 부르기에도 stability 손실이 너무 작다. **거의 같은 stability 위에서 XY가 미세 개선된 HOLD 상태**가 가장 정확하다.

---

# 13. Local Optimum / Reward Hacking Check

## 13.1 움직이지 않고 생존

강한 증거 없음.

이유:

- terrain `5.6`
- XY error `0.33` 수준
- track_lin reward 지속
- curriculum이 high regime 유지

따라서 zero-motion survival optimum과는 맞지 않는다.

## 13.2 비정상 자세로 termination 회피

수치상 강한 신호는 없지만 영상이 없으므로 완전 배제는 불가.

## 13.3 Hopping / 과도한 airtime

`feet_air_time` weight는 그대로 0.2이고 weighted term도 작다. hopping reward hacking의 강한 수치 신호 없음. 하지만 H-009 video가 없으므로 행동 확인은 못 했다.

## 13.4 Sliding

feet_slide penalty는 후반 안정적이며 악화하지 않았다. reward hacking 신호는 약하다.

## 13.5 Command 무시

XY는 낮지만 yaw error가 높다. “전체 command 무시”는 아니지만 **yaw command specialization 부족**은 명확하다.

## 13.6 Hip reward 단일 과최적화

hip weighted penalty가 late에서 줄었지만 terrain/tracking이 무너지지 않았다. 한 reward만 과최적화해 task 전체가 망가진 패턴은 없다.

---

# 14. Key Findings

1. **H-009 실행 자체는 매우 건강하다.** exit 0, raw event 2,000점, checkpoint 21개 finite, value loss 안정, NaN/OOM 없음.

2. **resume 직후 낮은 terrain은 실패가 아니라 재적응 구간이다.** rolling-50 terrain은 global 3275에 5.5를 회복하며 이후 high-terrain plateau를 유지한다.

3. **`joint_deviation_hip=-0.30`은 H-008의 성능을 망가뜨리지 않았다.** last-500 terrain 5.596, XY 0.3278, base-contact 29.99%로 H-008 unchanged continuation과 거의 동일하다.

4. **하지만 aggregate 성능 gain도 작다.** 알려진 unchanged control 대비 XY 약 `-0.0036` 개선, terrain `-0.008`, base-contact `+0.32%p`로 사실상 trade-off 없는 미세 변동 수준이다.

5. **yaw가 현재 더 큰 병목이다.** late yaw error 1.31이며 hip penalty 강화로 해결되지 않았다.

6. **자동 `model_best`가 raw reward peak조차 정확히 고르지 못했다.** finalizer는 3627/3600을 선택했지만 raw max는 3041이다. 기존 finalize warning이 이번 run에서도 재현됐다.

7. **reward peak 자체도 좋은 policy selector가 아니다.** raw peak 3041은 terrain 3.43/yaw 1.51이고 final 4997은 terrain 5.59/XY 0.31/yaw 1.25다.

8. **H-009의 실제 행동 영상은 현재 없다.** 기존 policy/video artifact는 provenance상 UNCHANGED이므로 이번 정책 행동 근거로 사용 금지다.

9. **final `model_4997.pt`가 현재 대표 checkpoint로 가장 합리적이다.** late joint deterioration이 없고, terrain/tracking 균형이 automatic best보다 낫다.

10. **이번 실험은 “hip -0.30이 대박”이 아니라 “-0.30까지 강화해도 성능이 거의 유지된다”는 정보를 얻었다.** 이 차이가 중요하다.

---

# 15. Final Decision

## **HOLD**

### 근거

- **PROMOTE로 보기 부족한 점**
  - unchanged H-008 continuation 대비 aggregate gain이 매우 작음
  - multi-seed 없음
  - H-009 video 없음
  - evaluator 없음
  - OFFICIAL 결과 아님
  - yaw 병목 미해결

- **REJECT가 아닌 이유**
  - numerical stability 매우 좋음
  - terrain high regime 유지
  - XY tracking 유지/미세 개선
  - base-contact collapse 없음
  - local optimum 붕괴 증거 없음
  - final policy가 parent 방향성을 보존

즉 `-0.30`은 **안전한 후보 범위 안에 있으나 우월성이 아직 증명되지 않은 값**이다.

---

# 16. Next Experiment

## 1순위 — H-011 `joint_deviation_hip=-0.10` sibling을 동일 조건으로 실행

### 설계

| 항목 | 값 |
|---|---|
| Parent | 동일 H-008 3K `model_2998.pt` |
| Parent SHA | `d9a30c8a…1912ae` |
| Seed | 42 |
| num_envs | 4096 |
| Additional iterations | +2000 |
| Reward change | `joint_deviation_hip -0.20 → -0.10` only |
| 기타 reward | H-008와 동일 |
| Headless | 동일 |
| PPO | 동일 |
| Evidence | raw event + console + all checkpoints + fresh video |

### 왜 이게 가장 정보 효율적인가

지금 이미:

- `-0.20`: unchanged H-008 control
- `-0.30`: H-009

의 방향이 있다.

여기에 `-0.10` 한 점을 추가하면 hip penalty axis의 **양방향 반응**을 볼 수 있다.

가능한 결과:

1. `-0.10`이 XY/yaw는 좋아지고 fall/terrain은 나빠짐\
   → hip penalty가 진짜 stability ↔ tracking trade-off knob라는 증거 강화.

2. `-0.10`, `-0.20`, `-0.30`이 거의 동일\
   → 이 범위의 hip penalty 영향은 작고, 다음 병목은 yaw/다른 reward라는 결론.

3. `-0.30`만 terrain/fall에서 의미 있게 좋아짐\
   → H-009를 PROMOTE할 근거가 생김.

4. `-0.10`이 오히려 모든 축에서 좋아짐\
   → 현재 hip penalty가 과도할 수 있다는 강한 방향성.

### 성공/실패 판정

H-009 대비가 아니라 **동일-parent control과 세 점을 함께** 본다.

핵심 metric:

- last-500 terrain
- last-500 XY
- last-500 yaw
- last-500 base-contact
- episode length
- action-rate
- orientation penalty
- hip reward term
- fresh native play:
  - flat
  - boxes
  - stairs
  - inverted stairs
  - rough
  - slopes
  - stop / yaw command 가능하면 별도

### 실험 길이

- 첫 200회: numerical sanity만 확인
- 1K: terrain recovery 방향 체크
- **2K까지 완료**: H-009/H-008과 동일 window로 비교
- 2K 전에 NaN/Inf/value-loss 폭발이 없으면 중간 scalar 악화만으로 조기 종료하지 않음

## 2순위 — hip axis가 평평하면 yaw 축으로 이동

세 sibling이 비슷하면 hip을 더 만질 정보 가치가 낮아진다.

그 경우 다음은 `track_ang_vel_z_exp 0.5 → 0.6` 같은 **단일 yaw reward 미세 강화**가 더 합리적이다. 이유는 현재 late yaw error `1.31`이 가장 뚜렷한 병목이기 때문이다.

단, H-011 결과를 보기 전에 hip과 yaw를 동시에 바꾸면 H-009가 준 정보를 버리게 된다.

---

# 17. Confidence & Limitations

## 확실한 것

- H-009는 PERSONAL resume run이다.
- parent metadata SHA는 H-008 3K final 기록과 일치한다.
- seed 42, 4096 env, +2000 iteration.
- `joint_deviation_hip=-0.30`.
- raw TensorBoard 2000점.
- exit 0.
- value loss 안정.
- all retained checkpoint finite.
- last-500 terrain/XY/yaw/fall 수치.
- finalizer/raw TensorBoard best mismatch.
- current H-009 archive의 policy/video가 fresh artifact가 아니라는 provenance.

## 강한 정황

- resume 초기 terrain 하락은 curriculum 재적응.
- H-009는 H-008 unchanged continuation과 aggregate 성능이 거의 같다.
- hip -0.30이 catastrophic trade-off를 만들지 않았다.
- final checkpoint가 auto model_best보다 representative policy로 더 적합하다.

## 가설

- stronger hip penalty가 실제 hip asymmetry를 조금 억제했을 가능성.
- late XY 개선 일부가 hip stabilization에서 왔을 가능성.
- orientation cost 증가가 hip constraint의 보상 trade-off일 가능성.

이 셋은 matched raw control/영상 없이는 인과로 확정하지 않는다.

## 판단 불가

- forward vs lateral 개별 tracking
- stop drift
- recovery success rate
- 실제 hip symmetry
- foot dragging / hopping
- terrain별 traversal success
- official evaluation gain
- multi-seed generalization
- H-009 policy.pt 실제 행동
- 정확한 actual KL trajectory

## 전체 분석 신뢰도

**Run identity / integrity: 매우 높음**\
**H-009 내부 dynamics: 매우 높음**\
**H-008 대비 인과적 reward 효과: 중간**\
**실제 행동 품질: 낮음~중간 (fresh H-009 video 없음)**\
**공식 대회 성능 일반화: 낮음 (PERSONAL single-seed)**

---

# Provenance — 사용한 근거

## 이번 H-009 archive 원본

`20260918-010042-h1-h009-hipdev030-from-h008-3k.tar(1).gz`

- outer SHA-256: `16f98464106cad8cfde7af39cbf22b70d89420df709af6ee26a2c246d241abe7`
- `SHA256SUMS`: 43/43 verified
- `metadata.json`
- `validation.json`
- `console.log`
- raw TensorBoard event
- `native_run/params/env.yaml`
- `native_run/params/agent.yaml`
- `source/humanoid_rewards.py`
- `source/identity.json`
- `native_run/git/IsaacLab.diff`
- 21 retained checkpoints
- GPU telemetry
- collected provenance
- report/finalizer outputs

## 프로젝트 맥락 자료

- `14_H1_NEXT_RUN_PARAMETER_COMPARISON`
  - H-008/H-009/H-010/H-011 lineage
  - H-009 planned delta
  - H-008 unchanged continuation late summary
- `15_OPTUNA_REWARD_DECISION_ENGINE`
  - H-008 HOLD 해석, sibling 구조
- `16_EXPERIMENT_EXPORT_AND_TENSORBOARD`
  - resume/final checkpoint selection 규칙
  - H-008 continuation provenance
- `18_H1_FINALIZE_REPORT_LIMITATIONS`
  - 자동 model_best/report mismatch의 기존 확인 사례
- `13_H1_OFFICIAL_SERVER_BASELINE_EVIDENCE`
  - 공식 TERM50 5K와 공식 Round 2 anchor

프로젝트 문서가 이번 raw archive와 충돌하는 경우 이번 H-009 raw artifact를 우선했다.

---

# 최종 답변 — 8개 질문

1. **이 정책은 무엇을 배웠는가?**\
   Resume reset 뒤 high-terrain locomotion을 빠르게 재적응하고, hip penalty가 더 강한 조건에서도 기존 tracking/stability regime을 유지하는 정책을 학습했다.

2. **이전 정책보다 무엇이 실제로 좋아졌는가?**\
   H-009 내부 late trajectory에서 XY tracking은 미세 개선했다. 그러나 unchanged H-008 control 대비 gain은 매우 작아 인과적 개선으로 확정할 수 없다.

3. **무엇을 잃었는가?**\
   aggregate 수준에서 큰 손실은 없다. terrain과 fall은 control과 거의 동일하다. yaw는 여전히 약하다.

4. **학습 중 언제 중요한 변화가 일어났는가?**\
   `2998~3047` resume warm-up, `3048~3275` curriculum 급회복, `~3300` 이후 terrain 5.5대 정착, `~4600` 이후 XY/yaw 미세 개선이 핵심 phase다.

5. **높은 지표가 실제 행동 개선을 의미하는가?**\
   아니다. raw reward 최고는 오히려 낮은 terrain의 early checkpoint였다. H-009 fresh video도 없으므로 scalar만으로 행동 개선을 확정할 수 없다.

6. **현재 가장 큰 병목은 무엇인가?**\
   yaw tracking과 약 30% base-contact termination. hip penalty는 이 병목을 크게 움직이지 않았다.

7. **이 가설은 계속 실험할 가치가 있는가?**\
   **있지만 HOLD.** `-0.30` 하나를 더 길게 돌리는 것보다 반대쪽 `-0.10` sibling으로 hip axis를 완성하는 편이 정보 가치가 높다.

8. **다음 한 번의 학습으로 가장 많은 정보를 얻으려면?**\
   동일 H-008 3K parent에서 **H-011 `joint_deviation_hip=-0.10` +2K**를 동일 조건으로 실행해 `-0.10 / -0.20 / -0.30`을 비교한다.
