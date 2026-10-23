> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/incoming/other/reviewed/H1_H001_R05_CORRECTED_PARENT_1P5K_DEEP_ANALYSIS_20260925.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# H1 H-001 R05 corrected parent 1.5K 심층 분석 — 2026-09-25

## 0. 분석 범위와 입력

이번 분석은 사용자가 제공한 두 archive를 A의 **학습 원본 + 행동 원본**으로 묶어 직접 조사했다. 별도 B 비교 정책의 학습 archive/영상 묶음은 제공되지 않았으므로, 본 보고서는 A의 독립 분석을 완성하고 기존 프로젝트 자료는 **맥락 참고**로만 사용한다. 과거 H-001이나 OFFICIAL TERM50을 B처럼 동일 기준으로 재계산했다고 쓰지 않는다.

- 학습 archive: `20260925-061112-h1-h001-r05-corrected-parent-1p5k-h1-corrected-2.tar.gz`
  - outer SHA-256: `f4386541b5cede2eb84133407f756b577b629ce4ed45b33ce0691d703c572ed2`
  - 내부 `SHA256SUMS` 38/38 PASS
- 6지형 영상 archive: `checkpoint-h1-model_1499-5e3a31502d22-download.tar.gz`
  - outer SHA-256: `db8c7db32bf559ed3f8a01a75f12604056bb3308aafffa1b05572c2009320287`
  - 내부 `SHA256SUMS` 7/7 PASS
- 영상 6개: H.264, 1920×1080, 50 fps, 각 19.98초 / 999 frames

프로젝트의 2026-09-24 문서들은 새 `feet_air_time=+0.2`, `termination=-50`의 1.5K corrected parent를 아직 **PLANNED**라고 기록하고 있다. 이번 2026-09-25 원본은 그 계획에 해당하는 fresh PERSONAL run이 실제로 완료되었음을 새로 증명한다. 이 보고서는 그 실행 사실을 반영하지만 registry/기존 문서는 수정하지 않았다.

---

# 1. 결론 요약

## 질문 1 — 이번 정책은 목표 행동을 실제로 얼마나 수행하는가?

**학습 자체는 정상 완료했고, final `model_1499.pt`는 6개 terrain의 단일 19.98초 영상에서 모두 가시적 낙상·body-contact reset 없이 upright locomotion을 유지했다.** 특히 `random_rough`에서는 거친 패치에서 평지로 실제 이동하는 장면이 명확하고, 두 slope 영상도 경사 패치 위에서 이동해 평지 쪽으로 나오는 행동이 확인된다. `boxes`에서는 uneven grid 위에서 계속 보행하며 약 9–11초의 큰 기울임/긴 단일다리 지지 뒤에도 넘어지지 않고 복구한다.

다만 **계단 능력을 “완전 통과”로 부를 증거는 부족하다.** `stairs.mp4`는 약 12–14초에 계단 가장자리/하단 step 구간을 밟고 지나간 뒤 15–16초에 다시 평지로 나오는 것은 보이지만, 여러 단을 연속 상승해 상단 platform까지 오르는 장면은 없다. `inverted_stairs.mp4`는 계단 basin/하단부에서 이동해 평지로 빠져나오는 장면이 더 분명하지만, 이것도 반복 성공률은 아니다.

수치도 “안정 정책 완성”보다는 **쓸 수 있는 corrected parent**에 가깝다. raw TensorBoard의 마지막 300 iteration 평균은 terrain `5.050`, XY error `0.3917`, yaw error `1.3599`, base-contact termination `30.98%`, timeout `69.03%`, episode length `769.6`이다. 마지막 100에서는 terrain `5.104`, XY `0.3859`, yaw `1.3060`으로 조금 더 좋아졌지만 base-contact는 `31.70%`다. 즉 **curriculum 진행과 추종은 후반까지 개선되지만 training aggregate의 낙상성은 여전히 무시할 수준이 아니다.**

## 질문 2 — 무엇이 관찰된 차이이고, 무엇을 설정 변경 효과로 해석할 수 있는가?

이번 입력에는 B가 없으므로 **`termination_penalty -5 → -50`의 인과 효과 크기는 판단 불가**다. 현재 archive가 증명하는 것은 다음이다.

- fresh 1.5K, seed 42, 4096 env에서 실제 적용 reward는 `feet_air_time=+0.2`, `termination_penalty=-50`이며 나머지 참가자 조정 7개는 baseline 값이다.
- 학습 내부에서는 초기 붕괴 후 terrain·생존·tracking이 회복됐다.
- final checkpoint가 6지형 단일 영상에서 실제로 upright motion을 낸다.

이것을 곧바로 “-50이 -5보다 좋다” 또는 “+0.2가 과거 -0.2보다 좋다”로 바꾸면 안 된다. 같은 조건의 unchanged fresh B가 없고, 과거 H-001은 설정 자체가 달랐으며, OFFICIAL TERM50 5K는 서버·학습량·시점이 다른 참고 자료다.

## 질문 3 — 현재 내려야 할 결정과 먼저 풀 불확실성

**실행: COMPLETE / evidence: PASS / corrected-parent 용도: PROMOTE / 제출·OFFICIAL 성능 주장: 해당 없음.**

`model_1499.pt`를 **새 corrected lineage의 실험 parent**로 채택하는 것이 현재 자료에 가장 잘 맞는다. 이유는 (1) intended config가 실제로 적용됐고, (2) fresh 1.5K가 정상 종료됐고, (3) final checkpoint SHA가 6개 영상의 source SHA와 정확히 일치하며, (4) 후반 terrain/tracking/fall이 공동 붕괴하지 않았기 때문이다.

다음 정보가 가장 큰 한 번의 행동은 **이 `model_1499`에서 reward를 아무것도 바꾸지 않은 +1.5K continuation control**을 확보하는 것이다. 이것이 있어야 이후 `track_lin 0.5→0.75`, `feet 0.2→0.25/0.30` 등의 sibling과 **추가 학습 효과를 분리한 직접 비교**가 가능해진다.

---

# 2. 실제 Run · checkpoint · 영상 identity

## 2.1 Run identity

| 항목 | 원본에서 확인한 값 |
|---|---|
| run_id | `20260925-061112-h1-h001-r05-corrected-parent-1p5k-h1-corrected-2` |
| run name | `h1-h001-r05-corrected-parent-1p5k-h1-corrected-20260925-03` |
| robot/task | H1 / `Humanoid-v0` |
| environment | `PERSONAL` |
| fresh/resume | **fresh**, `resume: false`, `parent_run_id: null`, `resume_lineage: null` |
| seed / num_envs | `42` / `4096` |
| requested iterations | `1500` |
| actual global iterations | `0..1499`, 1500 points |
| rollout | 24 steps/env/iteration |
| total transitions | `147,456,000` |
| final checkpoint | `checkpoints/model_1499.pt` |
| final SHA-256 | `5e3a31502d229884f91faf38962ffd32d63db69a64ca46ed7c1c404671b8ad82` |
| automatic model_best | `model_1400.pt` |
| model_best SHA-256 | `c08c818a4507cf40073b4de4f8edc2ea9beb7ef157c811e5402d436e56ca247b` |
| status | `completed`, exit code `0`, validation `PASS` |
| training loop time | console `1264.48 s`, final elapsed `00:20:47` |
| sidecar operation wall time | metadata 약 `21m 28s` |
| policy.pt / ONNX | **이번 학습 archive에는 없음** |

근거: `metadata.json`, `validation.json`, `command.txt`, `console.log`, `native_run/params/agent.yaml`, `checkpoints/`.

`model_1400.pt`와 `model_1499.pt` 두 선택 checkpoint만 tensor를 확인했으며 둘 다 non-finite tensor `0`이었다. 모든 checkpoint를 반복 검사하지 않았다.

## 2.2 source / PPO / 환경

`source/identity.json`은 task root Python/설정 핵심 8개 파일의 before/after SHA가 동일해 **run 중 source mutation이 없었음**을 기록한다. IsaacLab은 commit `3e73d6dd79080fd7632488c061052a6edd52e230`, clean detached HEAD로 기록됐다.

PPO 핵심은 actor/critic `512→256→128` ELU, `num_steps_per_env=24`, 5 epochs, 4 mini-batches, adaptive LR `1e-3`, gamma `0.99`, lambda `0.95`, entropy coef `0.008`, desired KL `0.01`, clip `0.2`, max grad norm `1.0`이다.

환경은 20초 episode, physics `0.005 s`, control `0.02 s`, curriculum-enabled `10×20` terrain grid, `max_init_terrain_level=5`, terrain generator seed `null`이다. command는 10초마다 resample되고 범위는 x `-1.0..1.5 m/s`, y `-0.5..0.5 m/s`, yaw `-1..1 rad/s`다.

## 2.3 실제 reward 설정과 “변경”의 범위

`source/humanoid_rewards.py`, `native_run/params/env.yaml`, `console.log`, `report.html`이 서로 일치한다.

| 참가자 reward | 실제 weight | baseline 대비 |
|---|---:|---|
| `track_lin_vel_xy_exp` | +0.5 | unchanged |
| `track_ang_vel_z_exp` | +0.5 | unchanged |
| `feet_air_time` | **+0.2** | unchanged |
| `termination_penalty` | **-50.0** | **-5 → -50** |
| `flat_orientation_l2` | -1.5 | unchanged |
| `ang_vel_xy_l2` | -0.05 | unchanged |
| `joint_deviation_hip` | -0.2 | unchanged |
| `joint_deviation_torso` | -0.1 | unchanged |
| `action_rate_l2` | -0.0005 | unchanged |

프레임워크 기본 nonzero 항목 `dof_acc_l2=-1.25e-7`, `dof_pos_limits=-1.0`, `feet_slide=-0.25`, `joint_deviation_arms=-0.2`도 활성이다. `dof_torques_l2`는 manager에 존재하지만 weight 0이다.

따라서 이번 새 parent는 과거 잘못된 `feet=-0.2` H-001과 다르다. 프로젝트 문서에 기록된 **옛 H-001 `model_1499` SHA prefix `68fa0a9f…f0c1`**와 이번 final `5e3a3150…ad82`를 혼동하면 안 된다.

## 2.4 영상 provenance

`video_suite_manifest.json`은 6개 영상 모두 source를 `model_1499.pt`, SHA `5e3a3150…ad82`로 기록한다. 실제 학습 archive의 `checkpoints/model_1499.pt`를 직접 hash한 값과 **완전 일치**했다. MP4 6개의 SHA도 manifest 및 `SHA256SUMS`와 모두 일치했다.

즉 이번 영상은 stale `UNCHANGED` artifact가 아니라 **현재 fresh 1.5K final checkpoint의 행동 근거**로 사용할 수 있다.

반대로 `collected/exported/model_best.pt`는 `model_1400.pt`와 hash가 같다. 따라서 다음 세 대상을 구분해야 한다.

- 자동 best: `model_1400.pt`
- final + 영상 source: `model_1499.pt`
- 실제 `policy.pt`: 이번 입력에 없음

---

# 3. 비교 설계와 해석 가능한 범위

## 3.1 이번 입력의 비교 등급

| 질문 | 등급 | 이유 |
|---|---|---|
| A 내부 학습 경과 | **직접 비교에 적합** | raw TensorBoard 0..1499 전 구간 존재 |
| final의 실제 6지형 행동 | **직접 관찰 가능** | final checkpoint SHA와 영상 manifest가 exact-match |
| automatic best vs final 정책 성능 | **조건부 비교** | scalar 시점은 비교 가능하나 `model_1400` 행동 영상/evaluator 없음 |
| `termination -5 → -50` 인과 효과 | **판단 불가** | 같은 조건 fresh baseline B가 없음 |
| 과거 잘못된 H-001(-0.2) 대비 +0.2 효과 | **판단 불가** | reward 외 계보/재실행 조건을 같은 원본으로 재분석하지 못함 |
| OFFICIAL TERM50 5K와 성능 비교 | **맥락 참고** | mode·학습량·실행 시점이 다름; B raw archive 미제공 |

현재 프로젝트 문서가 권고한 “corrected +0.2 TERM50 parent → unchanged continuation → sibling” 설계와 이번 새 원본은 잘 맞는다. 다만 corrected parent가 생겼다는 사실과 **reward 효과가 검증됐다는 사실은 다르다**.

---

# 4. raw TensorBoard 재분석

## 4.1 파싱 상태

원본 `native_run/events.out.tfevents.1790316691.brev-p049cuh9h.40766.0`을 직접 파싱했다. 핵심 scalar 29개는 각각 **1500 points**, step `0..1499`를 정확히 한 번씩 가진다. step reset, duplicate, 누락, resume boundary는 없다. protobuf에서 step 0이 default field로 생략된 첫 event는 0으로 정상화했다. `Train/*/time` 보조 태그는 일반 iteration index가 아니므로 trajectory 비교에서 제외했다.

report와 raw event의 주요 값은 일치한다.

- raw `Train/mean_reward` 최고: `2.1841335 @ step 1401`
- console/finalizer: `Best by 'Train/mean_reward': step 1401, reward 2.184 → model_1400.pt`
- report: 최고 보상 `2.18`, iter `1401`, selected model header `iter 1400`

따라서 이번 run에는 과거 사례처럼 EventAccumulator limit 때문에 생긴 selection mismatch 징후가 없다.

## 4.2 학습 phase

초기 `terrain=3.438 @0`을 능력으로 읽으면 안 된다. `max_init_terrain_level=5`인 curriculum 초기 배치값이고, 실제로 terrain은 step 25에서 `0.0`까지 빠르게 내려간다.

### Phase A — 초기 붕괴/재배치: 0–199

- rolling-100 @199: terrain `0.0156`
- base-contact `99.42%`
- episode length `205.8`
- reward `-1.297`

초기 정책은 사실상 대부분 base-contact로 종료된다.

### Phase B — 회복 시작: 200–599

- rolling-100 terrain은 @599 `2.684`
- base-contact는 `32.28%`까지 급격히 감소
- episode length `783.4`
- XY error는 초기보다 커졌다가 이후 감소하기 시작
- yaw error는 이 구간에 크게 악화되어 최고 `2.084 @451`

즉 먼저 “살아남고 지형을 버티는” 능력이 생긴 뒤 tracking이 따라오는 모양이다.

### Phase C — curriculum 상승: 600–1199

- rolling-100 terrain: @899 `4.640` → @1199 `4.910`
- XY: `0.4320 @899 window` → `0.3909 @1199 window`
- yaw: `1.6377` → `1.4435`
- base-contact는 대략 `31%` 부근에서 plateau

### Phase D — late mature: 1200–1499

본 보고서의 **주 late window는 마지막 300회(1200–1499)**로 잡았다. 이 구간에서 terrain이 5 부근에 머물며 추종이 계속 개선되고, 인접한 last-500에서도 방향이 같아 window 선택에 민감하지 않다.

| 지표 | last-500 (1000–1499) | last-300 (1200–1499) | last-100 (1400–1499) | final 1499 |
|---|---:|---:|---:|---:|
| mean reward | 1.340 | 1.485 | 1.650 | 1.881 |
| episode length | 770.40 | 769.63 | 767.32 | 754.02 |
| terrain level | 4.981 | **5.050** | **5.104** | **5.123** |
| XY error | 0.3962 | **0.3917** | **0.3859** | **0.3537** |
| yaw error | 1.4169 | **1.3599** | **1.3060** | **1.2326** |
| base-contact termination | 31.09% | **30.98%** | 31.70% | 31.41% |
| timeout | 68.92% | **69.03%** | 68.32% | 68.61% |
| action std | 1.350 | 1.354 | 1.357 | 1.353 |

**핵심 해석:** 후반에는 terrain·XY·yaw가 계속 좋아졌지만 base-contact가 더 줄어드는 단계는 아니다. 즉 “생존성 plateau 위에서 tracking/curriculum이 개선”되는 형태다.

## 4.3 checkpoint 1400 vs final 1499

| scalar 시점 | model_1400 인접 step 1400 | final step 1499 |
|---|---:|---:|
| reward | 1.320 | 1.881 |
| terrain | 5.069 | **5.123** |
| XY error | 0.3985 | **0.3537** |
| yaw error | 1.3635 | **1.2326** |
| base-contact | 32.22% | **31.41%** |
| episode length | 763.54 | 754.02 |
| action std | 1.355 | 1.353 |

자동 best가 model_1400인 이유는 step 1401의 **mean reward peak**와 가장 가까운 저장 checkpoint라서다. 그러나 final 1499가 terrain/tracking/fall에서 공동 악화한 흔적은 없다. 1300–1399와 1400–1499의 평균을 비교해도 terrain `5.075→5.104`, XY `0.3878→0.3859`, yaw `1.3438→1.3060`, base-contact `30.998→31.698%`로 **base-contact만 약 +0.70%p 악화하고 나머지는 유지/개선**했다.

따라서 실험 lineage의 parent로는 **정확히 1.5K를 끝낸 final model_1499**가 더 적절하다. 이것은 “fresh run의 model_best가 쓸모없다”는 일반 명제가 아니라, 이번 corrected-parent 실험의 계보 목적과 final 행동 provenance에 관한 선택이다.

## 4.4 optimization 안정성

- `Loss/value`: 초기 step 1의 `0.1805` spike 이후 late-300 평균 `0.00500`, p99 약 `0.00996`
- `Loss/surrogate`: late에서 약 `-0.01` 수준
- learning rate: adaptive하게 변화하며 final `1.98e-4`
- NaN/Inf: 선택 checkpoint tensor에서 0, console에도 치명적 NaN/Inf/traceback 없음
- action std: step 94의 `0.806`까지 내려갔다가 late 약 `1.35`로 상승

`action std≈1.35`만 보고 “학습 안 됨”으로 판정할 수 없다. 같은 late 구간에서 terrain과 tracking은 개선되고 실제 final 영상도 upright locomotion을 보인다. 다만 높은 탐색 폭이 정책의 민첩/불안정성을 키울 가능성은 남아 있으므로 추후 fixed evaluator에서 action smoothness와 함께 확인하는 것이 맞다.

---

# 5. 6지형 영상 직접 관찰

영상에서 보이는 녹색 화살표는 `goal_vel_visualizer`, 파란색 화살표는 `current_vel_visualizer`임을 `native_run/params/env.yaml`에서 확인했다. training command는 10초마다 resample되므로, 모든 영상의 약 10초 부근에서 goal/current 화살표 관계가 크게 바뀌는 것은 설정과 일치한다. 다만 manifest에는 실제 command 값·seed·terrain difficulty가 기록되어 있지 않으므로 정확한 명령 오차를 영상에서 수치화하지 않았다.

| terrain / 파일 | 직접 관찰 | 판단 한계 |
|---|---|---|
| stairs / `stairs.mp4` | 1–11초는 평지 보행. 약 **12–14초** 계단 가장자리/하단 step 영역에 접근·접촉하며 보행하고, **15–16초** 다시 평지 쪽으로 빠져나온다. 전 구간 upright, reset 없음. | 여러 단을 연속 상승해 상단 platform을 정복하는 장면은 없음. **full stair ascent 성공으로 판정하지 않음.** |
| inverted_stairs / `inverted_stairs.mp4` | 초반부터 stair basin/하단부 근처에서 보행. **8–12초** step 경계 위를 이동하고 **13–15초** 평지로 빠져나온다. visible fall 없음. | exact command 방향이 없어 “명령대로 계단을 내려가/올라왔다”는 판정은 보류. |
| boxes / `boxes.mp4` | uneven boxes 위에서 20초 동안 보행 유지. **9–11초** 몸통이 크게 기울고 긴 단일다리 지지가 나타나지만 **12초 이후 자세를 회복**한다. body contact/reset 없음. | 이 장면은 회복 능력의 질적 근거이지 boxes 통과율/거리의 정량값이 아님. |
| random_rough / `random_rough.mp4` | 거친 patch 위에서 지속 보행하며 **15–17초 부근 patch 경계를 넘어 평지로 이동**한다. visible fall 없음. | patch의 정확 difficulty/명령값 미기록. 한 번의 traversal을 반복 성공률로 환산하지 않음. |
| slope_up_10deg / `slope_up_10deg.mp4` | sloped patch 위에서 보행하고 후반에는 평지 쪽으로 이동한다. 10–12초 command 전환 직후 한쪽 다리 지지와 방향 조정이 보이나 회복한다. | filename의 `10deg` 외 manifest에 세부 difficulty/command 없음. 화면만으로 실제 uphill command 추종을 확정하지 않음. |
| slope_down_10deg / `slope_down_10deg.mp4` | slope patch에서 이동하며 후반 평지 쪽으로 빠져나온다. 전 구간 torso가 크게 무너지지 않고 visible fall 없음. | 실제 downhill 명령 및 이동축을 manifest가 기록하지 않아 방향성 평가는 제한됨. |

## 영상 전체에서 공통으로 보이는 패턴

1. **6/6 모두 한 클립의 19.98초 동안 visible fall/reset이 없다.** 이는 final checkpoint가 단순 tensor 정상 파일이 아니라 실제 locomotion을 수행한다는 강한 sanity evidence다.
2. 발을 비교적 크게 들고 single-leg support가 자주 보이며, 특히 command 전환 직후 한쪽 다리 체공/몸통 lean이 증가한다. 그러나 이번 6개 클립에서는 그 상태가 즉시 낙상으로 이어지지 않는다.
3. 약 10초 command resample 직후 녹색(goal)과 파란색(current) 화살표가 크게 어긋나는 구간이 반복된다. 몇 초 뒤 방향이 가까워지는 장면도 있지만 즉시 일치하지 않는다. 이는 raw TensorBoard에서 yaw error가 late에도 `~1.3` 수준인 것과 방향상 일치한다.
4. 영상만 보면 매우 안정적으로 보이지만 training last-300 base-contact termination은 약 `31%`다. 두 증거는 모순이 아니다. 영상은 terrain당 **단 1개 episode**이고, training 값은 많은 env/episode의 집계다. 따라서 영상 6개를 낙상률 `0%`라고 해석하지 않는다.

---

# 6. 핵심 발견의 설명과 경쟁 가설

## 발견 A — corrected parent identity는 해결됐다

**관찰:** current source는 `feet_air_time=+0.2`, `termination=-50`, fresh 1.5K이며 final SHA는 `5e3a3150…ad82`; 6개 영상도 이 SHA에 exact-match다.

**해석:** 9/24 프로젝트 문서가 요구한 “old `feet=-0.2` H-001을 대체할 +0.2 TERM50 corrected parent”의 identity/provenance 조건은 충족됐다.

**경쟁 설명/반대 근거:** 이것은 `-50`의 성능 우월성이나 +0.2의 최적성을 증명하지 않는다. 단지 올바른 parent가 생겼다는 뜻이다.

**판별 방법:** 다음 unchanged continuation을 같은 parent에서 만들고 sibling과 같은 추가 학습량/평가 조건으로 비교한다.

## 발견 B — 학습은 ‘생존 회복 → tracking/curriculum 개선’ 순서다

**관찰:** rolling-100 base-contact는 199에서 `99.4%`였으나 599에서 `32.3%`까지 내려가고, terrain은 599 `2.68` → 1199 `4.91` → 1499 window `5.10`으로 상승한다. yaw는 451에 `2.084`까지 악화 후 late `~1.3`으로 회복한다.

**해석:** -50 설정에서 정책이 먼저 “넘어지지 않는 행동”을 학습한 뒤 이동/회전 추종과 어려운 지형 적응을 진행한 가능성이 높다.

**경쟁 설명:** curriculum 자체가 쉬운 지형으로 내려갔다가 다시 올라온 효과가 섞여 있다. 따라서 terrain 상승을 reward의 직접 인과로 읽을 수 없다.

**반대 근거:** base-contact가 late 약 31%에서 더 내려가지 않는다. 안정성 완성보다 plateau에 가깝다.

**판별 방법:** unchanged continuation과 변경 sibling을 동일 평가에서 fall/progress/tracking으로 비교한다.

## 발견 C — final은 lineage parent로 적절하지만 ‘best policy’ 증명은 아니다

**관찰:** automatic best는 reward peak step 1401에 매핑된 `model_1400`; final은 `model_1499`. late 100에서 terrain/XY/yaw가 개선되고 joint collapse는 없다. 6지형 영상은 final에서 생성됐다.

**해석:** 실험 계보의 정확한 1.5K endpoint로는 final 1499가 가장 재현 가능한 기준점이다.

**경쟁 설명:** model_1400이 특정 evaluator에서 더 좋을 가능성은 남아 있다. 우리는 model_1400의 6지형 영상이나 fixed evaluator를 갖고 있지 않다.

**판별 방법:** 현재 목적은 checkpoint tournament가 아니라 corrected parent 확정이므로 추가 비교를 만들기보다 final을 parent로 고정하는 편이 정보 효율이 높다. 제출 후보 선별이 목적이 되는 시점에는 공통 evaluator에서 다시 비교해야 한다.

## 발견 D — 영상은 생존을 강하게 확인하지만 tracking은 아직 약점이다

**관찰:** 6개 영상 모두 upright이고 rough/slope/boxes에서 실제 이동이 보이지만, 10초 전환 직후 goal/current arrow mismatch와 방향 조정이 반복된다. raw late yaw error도 XY보다 상대적으로 크다.

**해석:** 현재 parent의 강점은 “움직이며 버티는 것”이고, 약점은 특히 방향 전환/회전 추종의 정밀도일 가능성이 높다.

**경쟁 설명:** 영상 command 값과 seed가 없고 camera/지형 방향이 정량 통제된 evaluator가 아니므로 arrow mismatch만으로 yaw 성능을 수치화할 수 없다.

**판별 방법:** fixed command evaluator에서 x/y/yaw를 분리하고, 10초 command transition 직후 수렴시간과 lateral drift를 측정한다.

---

# 7. checkpoint · 가설 · 프로젝트 의사결정

## 7.1 실행 / evidence / 가설 / 정책 판정

| 구분 | 판정 | 범위 |
|---|---|---|
| 실행 | **COMPLETE** | 1500/1500, exit 0 |
| evidence | **PASS** | training 38/38, video 7/7 checksum; source unchanged; raw event 존재 |
| 비교 | **A 독립 분석 가능 / B 인과 비교 불가** | B raw archive·영상 미제공 |
| corrected-parent 가설 | **PROMOTE** | **새 corrected lineage의 parent로 승격**. reward 최적성/제출 성능 PROMOTE가 아님 |
| 정책 성능 상태 | **사용 가능한 parent, 미완성 최종 정책** | 6지형 upright sanity 확인, late base-contact ~31%, yaw 병목 존재 |
| OFFICIAL 증거 | **아님** | metadata mode=`personal` |

## 7.2 대표 checkpoint

**대표 parent: `model_1499.pt` / SHA `5e3a3150…ad82`**

선택 이유:

- 정확한 fresh 1.5K endpoint
- 6지형 video source와 exact-match
- late terrain/XY/yaw가 공동 악화하지 않음
- 향후 sibling/unchanged continuation의 공통 부모로 가장 명확함

`model_best=model_1400.pt`는 reward peak selector 결과로 보존한다. 이를 삭제하거나 무효화할 이유는 없지만, corrected-parent lineage의 시작점으로 바꾸면 “1.5K parent에서 분기”라는 실험 조건이 흔들린다.

## 7.3 다음 한 번의 행동 — 정보가 가장 큰 선택

### 1순위: `model_1499`에서 **reward unchanged +1.5K continuation control**

- parent: `model_1499.pt` SHA `5e3a3150…ad82`
- 유지: 현재 `feet_air_time=+0.2`, `termination=-50` 포함 **모든 reward**, source/PPO, 4096 env, seed 42, headless
- 변경할 reward: **없음**
- 추가 학습량: +1500 iterations
- expected global endpoint: 기존 계보 관례상 약 `model_2998` (실제 생성 파일을 원본에서 확인해야 함)
- 공통 평가: 동일 final-checkpoint 6지형 video + 가능하면 고정 command evaluator에서 progress / XY / yaw / fall / stall
- 목적: 앞으로 corrected H-005~H-008 sibling의 **추가 학습 효과를 제거한 직접 control** 확보
- 결과별 결정:
  - unchanged도 크게 좋아지면: sibling의 단순 개선을 reward 효과로 과대해석하지 않음
  - sibling만 tracking/progress를 개선하고 fall을 유지하면: 해당 reward 변경을 3K/5K 후보로 승격 검토
  - unchanged와 sibling이 모두 나쁘면: parent maturity/평가 조건을 먼저 재검토

프로젝트의 9/24 우선순위 문서도 corrected parent 확정 후 unchanged control을 먼저 요구한다. 이번 자료로 corrected parent 단계는 완료됐으므로, 다음 실험의 정보가치는 control 확보가 가장 높다.

2순위는 control 이후의 `track_lin_vel_xy_exp 0.5→0.75` 단일 sibling이지만, **control보다 먼저 실행할 이유는 없다.**

---

# 8. 남은 한계

1. **B가 없다.** 따라서 termination -50의 효과, old H-001(-0.2) 대비 corrected +0.2 효과, 다른 정책 대비 우열은 확정하지 않는다.
2. 영상 manifest에 **command 값·seed·difficulty·camera parameter**가 없다. terrain label과 source checkpoint는 강하게 연결됐지만 동일 episode paired 비교는 아니다.
3. 6지형은 terrain당 단일 약 20초 trajectory다. 6/6 visible no-fall을 실패율/성공률로 변환할 수 없다.
4. `policy.pt`/ONNX가 이번 학습 archive에 없으므로 실제 제출/export actor의 identity는 확인하지 않았다.
5. training `base_contact`는 학습 집계 termination metric이며 fixed evaluator 낙상률이 아니다.
6. curriculum terrain level은 고정 difficulty 통과율이 아니다.
7. single seed다. 같은 seed도 terrain generator seed가 `null`이므로 다른 실행과 identical terrain realization을 보장하지 않는다.
8. automatic best와 final의 **행동 대 행동** 비교는 하지 않았다. model_1400 영상/evaluator가 없기 때문이다.

---

# 9. 재확인 가능한 근거 위치

## 학습 archive 내부

- `metadata.json` — run mode/status/command/start-end/checkpoint count
- `validation.json` — evidence PASS checks
- `command.txt` — exact train command
- `source/humanoid_rewards.py` — 실제 참가자 reward source
- `source/identity.json` — task source before/after hashes
- `native_run/params/env.yaml` — terrain, command, reward, episode 설정
- `native_run/params/agent.yaml` — fresh/resume, PPO, seed, max_iterations
- `native_run/events.out.tfevents.1790316691.brev-p049cuh9h.40766.0` — 0..1499 raw scalar
- `console.log` — 전 iteration console 및 finalizer mapping
- `checkpoints/model_1400.pt` — automatic best source
- `checkpoints/model_1499.pt` — final / 영상 source
- `collected/exported/model_best.pt`, `report.html`, `env.yaml`

## 영상 archive 내부

- `video_suite_manifest.json` — checkpoint SHA / terrain / MP4 SHA / video evidence ID
- `videos/stairs.mp4`
- `videos/inverted_stairs.mp4`
- `videos/boxes.mp4`
- `videos/random_rough.mp4`
- `videos/slope_up_10deg.mp4`
- `videos/slope_down_10deg.mp4`

## 현재 프로젝트 맥락 참고

- `00_START_HERE_CONTEXT_AND_MAP(20260924-141428).md`: 9–13, 121–122
- `14_H1_NEXT_RUN_PARAMETER_COMPARISON(20260923-170742).md`: 44, 66–80
- `16_EXPERIMENT_EXPORT_AND_TENSORBOARD(20260924-141415).md`: 50–64
- `18_H1_FINALIZE_REPORT_LIMITATIONS(20260922-160915).md`: 48–53, 70–73
- `20_H1_PUBLIC_FAILURES_AND_EXPERIMENT_PRIORS.md`: 77–83

이 과거 문서들은 이번 9/25 실행보다 이전 시점이다. “corrected parent는 아직 PLANNED”라는 문장은 이번 새 원본에 의해 최신 상태가 바뀌었지만, 기존 문서의 계보 정정 원칙과 unchanged-control 요구는 그대로 유효하다.

---

## 최종 판정 한 줄

**`H1 H-001 R05 corrected parent 1.5K`는 실행·identity·영상 provenance가 모두 확인된 PERSONAL corrected parent로 PROMOTE하며, 대표 parent는 final `model_1499.pt (5e3a3150…ad82)`이다. 다음 결정용 1순위 증거는 이 checkpoint에서 reward unchanged +1.5K continuation control을 만드는 것이다.**

정확도 : 96%
