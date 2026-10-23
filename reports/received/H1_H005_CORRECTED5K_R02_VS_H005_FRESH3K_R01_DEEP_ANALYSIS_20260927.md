> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/incoming/other/reviewed/H1_H005_CORRECTED5K_R02_VS_H005_FRESH3K_R01_DEEP_ANALYSIS_20260927.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# H1 H-005 심층 분석 — corrected 5K vs fresh 3K, corrected 3K 계보 앵커

- 작성일: 2026-09-27
- 로봇: Unitree H1 / Humanoid
- 환경 분류: **PERSONAL** (Brev/NVIDIA L40S), OFFICIAL 점수 아님
- 주 비교 A: `H-005 corrected 3K→5K Run 02` — 최신 장기 continuation
- 주 비교 B: `H-005 fresh 3K Run 01`
- 계보 앵커 C: `H-005 corrected 3K Run 02`
- 분석 원칙: 파일명/가설 별칭보다 archive 내부 metadata, `env.yaml`, raw TensorBoard event, checkpoint SHA, video-suite manifest를 우선한다.

---

## 1. 결론 요약

### 질문 1 — 이번 정책은 목표 행동을 실제로 얼마나 수행하는가?

A의 **학습 후반 지표는 C보다 일관되게 좋아졌다.** 직접 재계산한 late-500에서 terrain `5.4776 → 5.6646`(+3.42%), XY tracking error `0.3609 → 0.3529`(-2.22%), yaw tracking error `1.0410 → 0.9402`(-9.68%), training base-contact `29.761% → 28.729%`(-1.032%p), mean episode length `773.76 → 785.30`(+1.49%)였다. late-300에서도 terrain +3.86%, XY -1.46%, yaw -8.21%, base-contact -1.265%p로 같은 방향이 유지됐다. 따라서 **corrected H-005를 3K에서 5K까지 더 학습한 것은 training distribution 안에서 tracking·terrain·접촉 안정성을 동시에 조금씩 개선한 것으로 관찰된다.**

다만 행동 영상의 source는 A의 final `model_4997.pt`가 아니라 자동 best인 **`model_4800.pt`**다. 여섯 지형 모두 19.98초 클립의 샘플 프레임에서는 upright locomotion을 유지했고 stairs/inverted-stairs/random-rough/slope 양방향에서 명확한 붕괴를 보지 못했다. 가장 눈에 띈 질적 차이는 `boxes.mp4`: A의 `model_4800`은 약 14–15초 무렵 박스 패치를 빠져나와 평탄면으로 진행하는 장면이 보인 반면 B `model_2750`과 C `model_2998`은 18–19.5초 샘플까지 박스 패치 안에 남아 있었다. 그러나 이 native-play suite는 command, terrain seed, difficulty, 초기 상태가 matched라는 증거가 없으므로 **A가 boxes를 더 잘 통과한다고 정량 판정할 수는 없다.**

즉 현재 자료가 직접 지지하는 표현은 다음이다.

> **A는 training scalar 기준으로 C보다 성숙했고, 제공된 A/model_4800 영상은 6지형에서 정상적인 upright traversal 형태를 보여 준다. 그러나 final model_4997의 행동은 아직 영상으로 확인하지 못했고, 20초 단일 native-play 영상에서 낙상률·공식 추종 점수·고정 난이도 통과율을 추정할 수 없다.**

### 질문 2 — 비교 정책과의 차이 중 무엇이 관찰이고, 무엇을 설정 변경 효과로 해석할 수 있는가?

- **A vs C:** reward 설정은 동일하고 C final `model_2998.pt`를 A가 실제로 resume했다. 따라서 후반 차이는 **같은 H-005 정책에 +2K 학습을 추가한 결과**로 해석할 수 있다. 이것은 `feet_air_time=0.25`의 인과효과가 아니라 추가 학습/재적응을 포함한 continuation 효과다.
- **C vs 동일 부모 unchanged control:** `feet_air_time 0.20→0.25`의 가장 직접적인 reward 비교다. 다만 이번 입력에는 unchanged-control raw archive가 없다. 프로젝트에 보존된 재분석 요약은 control late-500 `terrain 5.5010 / XY 0.3695 / yaw 1.0455 / base-contact 29.616%`, C를 이번에 직접 재계산한 값은 `5.4776 / 0.3609 / 1.0410 / 29.761%`다. 즉 C는 XY 약 2.3% 개선 신호가 있지만 terrain -0.43%, base-contact +0.145%p의 trade-off가 있고 yaw 차이는 작다. **현재 입력만으로 reward 단일변수의 강한 우월성을 확정할 수 없다.**
- **A vs B:** 두 정책의 완성 상태를 비교하는 참고에는 쓸 수 있지만 학습 길이와 초기화/계보가 다르므로 reward 인과 비교가 아니다. A late-500은 B보다 terrain +2.92%, XY -5.52%, yaw -8.44%, base-contact -1.206%p였지만 대부분은 `3K vs 5K` 학습량 차이로도 설명된다.

### 질문 3 — 지금 내려야 할 결정과 먼저 해결해야 할 불확실성

- **실행:** A/B/C 모두 `COMPLETE`; child exit code 0, evidence validation PASS.
- **가설 H-005 (`feet_air_time 0.20→0.25`):** **PROMOTE — 단, 범위는 fixed paired evaluation 단계까지만. 최종 채택/인과 확정은 HOLD.** 3K matched-control 신호가 작고 trade-off가 있으며, 5K에는 unchanged-control continuation이 아직 직접 대조되지 않았다.
- **정책 대표 checkpoint:** 프로젝트 운영 원칙과 이번 late-window를 적용하면 A는 **final numbered `model_4997.pt`**를 기본 대표로 보는 것이 타당하다. 마지막 수백 iteration에서 terrain·tracking·접촉이 함께 붕괴하지 않았다. 그러나 제공된 A 영상은 `model_4800.pt`이므로 **model_4997의 행동 품질은 미확인**이다.
- **다음 한 번의 행동:** 새 학습보다 먼저 보존 checkpoint를 동일 fixed evaluator에 놓는다. 최소 비교는 `H-001 unchanged 3K final` vs `H-005 corrected 3K final model_2998` vs `H-005 corrected 5K final model_4997`; B final `model_2999`도 path-dependence 확인용으로 함께 넣을 가치가 있다. 동일 command/terrain/difficulty/seed-set/window에서 x/y/yaw error, 실제 진행·stall, base-contact/fall, hip/torso raw posture를 측정한다. **이 한 번의 평가가 H-005 reward 효과, 추가 2K의 행동 효과, fresh/resume 경로 차이를 동시에 가장 많이 구분한다.**

---

## 2. 실제 Run → 설정 → checkpoint → 영상 identity

### 2.1 입력 자료와 역할

| 역할 | 학습 archive | 제공 영상/checkpoint bundle | 실제 영상 source |
|---|---|---|---|
| B — fresh 3K | `20260927-032343-h1-h005-fresh3k-r01-20260927.tar.gz` | `checkpoint-h1-model_2750-6d7d0ecb13c7-download.tar.gz` | `model_2750.pt` SHA `6d7d0ecb13c7…c29eb` |
| C — corrected 3K | `20260925-071158-h1-h005-r02-gait025-corrected-h1-corrected-20260.tar.gz` | `checkpoint-h1-model_2998-9454afa964bb-download.tar.gz` | final `model_2998.pt` SHA `9454afa964bb…85cc` |
| A — corrected 5K continuation | `20260927-054950-h1-h005-corrected3kto5k-r02-20260927.tar.gz` | `checkpoint-h1-model_4800-40c6a4a8273c-download.tar.gz` | `model_4800.pt` SHA `40c6a4a8273c…4a8a` |

세 video bundle의 `video_suite_manifest.json`과 실제 MP4 18개의 SHA-256을 대조했고 모두 일치했다. 각 manifest의 source checkpoint SHA도 대응 학습 archive의 실제 checkpoint 바이트와 일치했다. 따라서 영상 source identity는 파일명 추정이 아니라 **manifest ↔ checkpoint 실제 SHA**로 연결됐다.

### 2.2 B — fresh 3K

- status: `COMPLETED`, exit code 0, evidence validation `PASS`
- mode: `personal`
- 학습 방식: fresh
- seed: 42
- num_envs: 4096
- requested/global scalar range: 3000 iterations, step `0…2999`
- PPO: 24 steps/env, actor/critic `[512,256,128]`, ELU, 5 epochs, 4 mini-batches, adaptive LR 0.001, gamma 0.99, lambda 0.95, entropy 0.008, desired KL 0.01, clip 0.2, max grad norm 1.0
- 실제 H-005 reward: `track_lin=0.5`, `track_ang=0.5`, `feet_air_time=0.25`, `termination=-50`, `flat_orientation=-1.5`, `ang_vel_xy=-0.05`, `hip=-0.2`, `torso=-0.1`, `action_rate=-0.0005`
- raw reward peak: 약 `3.72 @ 2747`; 자동 `model_best.pt`는 `model_2750.pt`와 byte-identical
- final numbered: `model_2999.pt`, SHA `ff51151a037d…25a2`
- 영상 source: `model_2750.pt`; **final 2999 영상은 없음**

원본 위치:
- TensorBoard: `20260927-032343-h1-h005-fresh3k-r01-20260927/native_run/events.out.tfevents.1790479449.brev-b26rbxifs.22833.0`
- env: `.../native_run/params/env.yaml`
- agent: `.../native_run/params/agent.yaml`
- console: `.../console.log`
- integrity: `.../SHA256SUMS`

### 2.3 C — corrected 3K

- status: `COMPLETED`, exit code 0, evidence validation `PASS`
- mode: `personal`
- 학습 방식: resume
- 기록상 부모: corrected H-001 Run 05 final `model_1499.pt`
- parent SHA: `5e3a31502d22…8ad82`
- parent iteration: 1499
- child 추가 학습량: 1500 iterations
- global scalar range: `1499…2998` (1500 points)
- seed/env/PPO: B와 동일
- parent 설정은 프로젝트 보존 기록상 `termination=-50`, `feet_air_time=+0.20`; C에서 **`feet_air_time 0.20→0.25`만 변경**
- raw reward peak: 약 `3.68 @ 2932`; 자동 `model_best.pt`는 `model_2900.pt`
- final numbered: `model_2998.pt`, SHA `9454afa964bb…85cc`
- 영상 source: **final `model_2998.pt`**

중요 provenance 경계: child metadata의 `source_provenance_verified=false`는 이번 child archive 자체에 부모 원본 바이트가 없다는 뜻이다. 프로젝트에 보존된 corrected parent 기록은 같은 SHA를 가리키지만, 이번 입력 세트에는 그 parent archive가 별도로 포함되지 않았다. 따라서 **“기록상/프로젝트 보존자료상 연결”과 “이번 업로드 안에서 부모 바이트까지 직접 대조”를 구분한다.**

원본 위치:
- TensorBoard: `20260925-071158-h1-h005-r02-gait025-corrected-h1-corrected-20260/native_run/events.out.tfevents.1790320336.brev-p049cuh9h.57036.0`
- env: `.../native_run/params/env.yaml`
- agent: `.../native_run/params/agent.yaml`
- console: `.../console.log`

### 2.4 A — corrected 3K→5K

- status: `COMPLETED`, exit code 0, evidence validation `PASS`
- mode: `personal`
- 학습 방식: resume
- parent checkpoint: C final `model_2998.pt`
- metadata parent SHA: `9454afa964bb…85cc`
- **이번 입력의 C 실제 `model_2998.pt` 바이트를 다시 hash해 A metadata의 parent SHA와 exact-match 확인**
- 추가 학습량: 2000 iterations
- global scalar range: `2998…4997` (2000 points)
- seed/env/PPO/reward: C와 동일
- raw/report reward peak: 약 `4.55 @ 4814`; 자동 `model_best.pt`는 `model_4800.pt`와 byte-identical
- final numbered: `model_4997.pt`, SHA `623767090b58…10a5`
- 영상 source: `model_4800.pt`; **final 4997 영상은 없음**

원본 위치:
- TensorBoard: `20260927-054950-h1-h005-corrected3kto5k-r02-20260927/native_run/events.out.tfevents.1790488209.brev-b26rbxifs.49250.0`
- env: `.../native_run/params/env.yaml`
- agent: `.../native_run/params/agent.yaml`
- console: `.../console.log`

### 2.5 stale export 배제

C와 A archive의 `collected/exported/`에 남아 있는 일부 `policy.pt`, `policy.onnx`, `play_video.mp4`는 provenance에서 `UNCHANGED`로 식별되는 이전 산출물이다. 이 파일들은 C/A의 새 행동 증거로 사용하지 않았다. 행동 분석은 checkpoint SHA가 명시된 **별도 6-terrain video suite**만 사용했다.

---

## 3. 비교 설계: 어떤 질문에 답할 수 있는가

| 비교 | 부모/설정 관계 | 학습량 | 해석 가능 범위 | 판정 |
|---|---|---:|---|---|
| A corrected5K vs C corrected3K | A가 C final을 exact-SHA parent로 resume, reward 동일 | +2K | 동일 lineage에서 추가 학습 뒤 training 지표/행동 변화 | **직접 비교에 적합** — 단 reward 효과가 아니라 continuation 효과 |
| C H-005 3K vs H-001 unchanged 3K | 같은 corrected parent에서 `feet 0.20→0.25` 단일 delta | 동일 +1.5K | H-005 reward 인과 질문 | **조건부 비교** — 이번 입력에 control raw archive가 없어 프로젝트 요약값만 인용 |
| A corrected5K vs B fresh3K | 최종 reward/source/PPO는 사실상 동일, 초기화·계보·학습량 다름 | 5K 계보 vs fresh 3K | 완성 정책의 학습상태 비교, path-dependence 단서 | **맥락 참고**; reward 인과 판단 불가 |
| A/B/C 6-terrain 영상 | checkpoint identity는 검증됨 | 각 checkpoint 상이 | 자세·접촉·stall·회복의 질적 sanity check | **조건부 정성 비교**; command/seed/difficulty matched 아님 |

공통점은 강하다. 세 child의 `env.yaml`은 run log directory를 제외하면 동일하고, PPO/source도 동일하다. reward source에서 C만 `-50.0` 표기, 다른 두 run은 `-50` 표기 차이가 있으나 수치 의미와 실제 env 설정은 동일하다. 따라서 A-C에서는 source/PPO/reward 변경보다 **학습 continuation**이 중심 차이다.

그러나 training terrain generator seed가 고정된 paired evaluator seed와 같다는 증거는 없고, native video suite도 동일 command/terrain realization을 강제하지 않는다. 같은 seed 42라는 사실만으로 A/B/C가 같은 episode를 경험했다고 가정하지 않았다.

---

## 4. raw TensorBoard 재분석

### 4.1 파싱과 처리

각 archive의 실제 `events.out.tfevents*`를 raw TFRecord/Event protobuf로 파싱했다. 세 run 모두 핵심 tag당 기대한 scalar point 수(B 3000, C 1500, A 2000)가 있었고, **각 event 파일 내부에 중복 step은 없었다.** 총 31개 scalar tag를 확인했다.

중요한 예외는 **resume 경계의 global step 중복**이다. C의 마지막 step과 A의 첫 step이 모두 `2998`이다. 값은 동일 상태의 연속 측정이 아니다. A가 resume되며 episode/curriculum accumulator가 새로 시작하기 때문이다. 예:

| tag | C @2998 | A @2998 |
|---|---:|---:|
| terrain level | 5.4657 | 3.4380 |
| XY error | 0.3650 | 0.0127 |
| yaw error | 1.0108 | 0.0154 |
| base-contact | 29.22% | 0% |
| timeout | 70.78% | 1.37% |
| mean episode length | 약 758 | 11.52 |
| mean reward | 약 2.814 | 0.0149 |

이 급변을 정책의 즉시 개선/악화로 읽지 않았다. A의 rolling-50 terrain이 C late-500 평균 수준을 다시 회복하는 시점은 대략 global 3258 부근, 즉 child 시작 후 약 260 iteration이었다. 따라서 A의 초반은 **resume 재적응 구간**으로 분리했다.

### 4.2 사전 정의 window

결과를 보고 유리한 경계를 고르지 않기 위해 각 run 길이에 맞춰 다음 구간을 사용했다.

- B fresh3K: early `0–299`, middle `1500–1999`, late-500 `2500–2999`, late-300 `2700–2999`, last-100 `2900–2999`
- C corrected3K: early `1499–1798`, middle `1999–2498`, late-500 `2499–2998`, late-300 `2699–2998`, last-100 `2899–2998`
- A corrected5K: early/re-adapt `2998–3297`, middle `3748–4247`, late-500 `4498–4997`, late-300 `4698–4997`, last-100 `4898–4997`

late-500을 주 비교로 쓰고 late-300을 민감도 확인으로 사용했다. TensorBoard point 500개는 독립 seed 500개가 아니므로 p-value나 좁은 신뢰구간은 계산하지 않았다.

### 4.3 late-500 동일 기준 비교 — 직접 재계산

| metric | B fresh3K | C corrected3K | A corrected5K |
|---|---:|---:|---:|
| Curriculum/terrain_levels | **5.50379** | 5.47757 | **5.66463** |
| Metrics/.../error_vel_xy | 0.37355 | 0.36093 | **0.35293** |
| Metrics/.../error_vel_yaw | 1.02692 | 1.04095 | **0.94023** |
| Episode_Termination/base_contact | 29.935% | 29.761% | **28.729%** |
| Episode_Termination/time_out | 70.074% | 70.245% | **71.285%** |
| Train/mean_episode_length | 775.825 | 773.755 | **785.303** |
| Policy/mean_std | 1.34552 | 1.34186 | **1.31887** |
| Train/mean_reward | 2.84020 | 2.82486 | **3.62042** |
| feet-air weighted term | 0.01360 | 0.01231 | 0.01465 |
| hip weighted term | -0.03370 | -0.03459 | -0.03228 |
| torso weighted term | -0.00633 | -0.00587 | -0.00543 |
| feet-slide weighted term | -0.04199 | -0.04654 | -0.04078 |
| action-rate weighted term | -0.06337 | -0.06244 | -0.06193 |
| value loss | 0.00513 | 0.00498 | 0.00476 |

주의: 세 run의 child reward weights는 같으므로 weighted term 자체의 방향 비교는 가능하다. 그러나 term 계산/정규화 정의를 여기서 다시 증명하지 않았으므로 **weight로 나눠 raw hip deviation, raw air-time 등을 역산하지 않았다.**

### 4.4 A vs C — 추가 2K의 관찰 효과

late-500:

- terrain: `+0.18706` = **+3.42%**
- XY error: `-0.00800` = **-2.22%**
- yaw error: `-0.10072` = **-9.68%**
- base-contact: **-1.032%p**
- timeout: +1.040%p
- episode length: +11.55 = **+1.49%**
- mean std: -0.02299 = **-1.71%**
- same-weight mean reward: +0.7956 = +28.2%

late-300 민감도:

| metric | C late-300 | A late-300 | 방향 |
|---|---:|---:|---|
| terrain | 5.47530 | 5.68688 | A +3.86% |
| XY error | 0.35846 | 0.35322 | A -1.46% |
| yaw error | 1.02526 | 0.94112 | A -8.21% |
| base-contact | 29.938% | 28.673% | A -1.265%p |
| episode length | 771.894 | 786.109 | A +1.84% |
| mean std | 1.33975 | 1.31664 | A -1.72% |

주요 방향이 window 변경에도 유지된다. 이 때문에 “A가 C보다 후반 training distribution에서 성숙했다”는 결론은 late-500 경계 하나에만 의존하지 않는다.

### 4.5 C vs B — 3K 시점의 path difference

late-500에서 C는 B보다:

- terrain -0.48%
- XY error -3.38% (C가 낮음)
- yaw error +1.37% (C가 높음)
- base-contact -0.174%p
- episode length -0.27%

late-300에서는 C의 XY 이득이 약 -4.58%로 보이지만 yaw는 거의 같고 base-contact는 오히려 +0.503%p, terrain은 -0.77%다. **3K 시점에서는 두 경로가 근접하며 어느 하나가 전 축에서 지배하지 않는다.** fresh vs resume 초기화/학습 history의 path-dependence 가능성은 있지만, 현재 단일 seed로 일반화할 수 없다.

### 4.6 optimization 안정성

- 세 event의 scalar에서 NaN/Inf를 찾지 못했다.
- console에서 traceback, RuntimeError, CUDA OOM, floating-point fatal error를 확인하지 못했고 exit code는 모두 0이다.
- value loss 최대치는 B fresh 시작부 약 0.1808, C resume 첫 step 약 0.0352, A resume 첫 step 약 0.0165였고 이후 낮은 범위로 안정됐다. late-500 평균은 약 0.005 수준이다.
- mean std는 A 후반 약 1.32로 B/C보다 소폭 낮지만, std 하나만으로 정책 수렴/품질을 판정하지 않았다.

### 4.7 A 후반 악화 여부와 final checkpoint

A의 `3998–4497` vs `4498–4997`:

- terrain `5.6768 → 5.6646` 소폭 하락
- XY `0.35330 → 0.35293` 소폭 개선
- yaw `0.94798 → 0.94023` 개선
- base-contact `29.194% → 28.729%` 개선
- episode length `781.05 → 785.30` 개선
- std `1.32515 → 1.31887` 감소

terrain 단독의 작은 하락은 있지만 tracking·접촉·episode가 함께 악화되지 않는다. 따라서 **joint late collapse는 없다.**

A video source `model_4800` 근방(window 4751–4850)과 final last-100(4898–4997)을 비교하면 final은 terrain·XY·yaw가 더 좋고 std도 약간 낮지만 base-contact는 약 +0.36%p, episode length는 약 -5.9로 소폭 불리하다. 이는 작은 stability trade-off이지 final을 배제할 정도의 공동 악화가 아니다. 그러므로 충분히 진행한 resume의 운영 원칙에 따라 **final `model_4997.pt`를 대표 후보로 유지**한다. 자동 reward-best `model_4800.pt`가 행동 최적임을 증명하는 자료는 없다.

---

## 5. 6지형 영상 분석

### 5.1 영상 identity와 관찰 범위

각 bundle은 다음 6개 MP4를 포함한다.

`stairs`, `inverted_stairs`, `boxes`, `random_rough`, `slope_up_10deg`, `slope_down_10deg`.

모든 18개 영상은 H.264, 1920×1080, 50 fps, 999 frames, 19.98 s였고 manifest SHA와 실제 MP4 SHA가 일치했다. 프로젝트의 `issacsimz` suite 정의상 H1 고정 경사는 `slope_range=[0.176326981, 0.176326981]`, `horizontal_scale=0.05`, 선택 terrain proportion 1.0을 사용한다. 이 suite는 **PERSONAL-only visual check**이며 checkpoint selector나 fixed evaluator가 아니다.

영상 분석은 모든 프레임을 실시간으로 연속 재생해 수동 주석한 것이 아니라 다음 범위로 프레임을 직접 조사했다.

- 전 영상: 약 `0.5, 3, 5.5, 8, 10.5, 13, 15.5, 18, 19.5 s` contact sheet
- 전 영상: `10–18 s` 1초 간격 확대 샘플
- stairs: `11.5–14.5 s` 약 0.3초 간격 dense sequence
- boxes: `10.5–14.0 s` 약 0.35초 간격 dense sequence
- slope-up: `4–7 s` 약 0.3초 간격 dense sequence

따라서 “샘플 구간에서 관찰됨/관찰되지 않음”으로 기술하며, 진동 주파수·정밀 속도·전체 낙상률·보행 주기 통계처럼 연속 측정이 필요한 수치는 만들지 않았다.

### 5.2 지형별 비교

| 지형 | B fresh3K / `model_2750` | C corrected3K / `model_2998` | A corrected5K / `model_4800` | 판단 한계 |
|---|---|---|---|---|
| stairs | 약 11.5–12 s 접근, 12–14.5 s 계단 stripe 위 진행, 15–16 s 이후 패치가 뒤로 이동. 샘플에서 upright. | 유사하게 12–14.5 s 계단 접촉·진행, 샘플에서 upright. | 유사하게 계단 접촉 후 진행, 샘플에서 upright. | command/계단 realization이 matched 아님; 상승 단수·속도 정량화 불가. |
| inverted_stairs | 약 10–15 s 내리막/반전 계단 패치와 상호작용, 16–18 s에는 패치에서 벗어나는 장면. | 유사, sampled frame에서 큰 자세 붕괴 없음. | 유사, sampled frame에서 upright. | 영상만으로 낙상률/회복 성공률 추정 불가. |
| boxes | 10.5 s 이후 박스 패치 진입. 18–19.5 s 샘플까지 patch 내부에 남아 있음. sampled frame에서 upright. | B와 비슷하게 late sample까지 patch 내부. | **약 14–15 s부터 평탄면으로 빠져나온 장면**이 보이고 이후 upright 진행. | 이번 영상의 가장 큰 질적 차이지만 box layout, command, seed, difficulty/initial state matched 증거가 없어 우월성·인과 주장 금지. |
| random_rough | rough patch에서 진행 후 약 17–18 s 평탄면에 가까운 장면; upright. | 유사한 rough traversal; sampled frame에서 upright. | 유사한 rough traversal; sampled frame에서 upright. | 실제 이동거리/heading drift를 영상 tracking camera만으로 정밀 비교 불가. |
| slope_up_10deg | dense 4–7 s에서 좌우 다리 자세가 번갈아 바뀌며 경사 위 이동. sampled frame에서 upright. | 유사한 alternating leg configuration, sampled frame에서 upright. | 유사, sampled frame에서 upright. | 화면 중앙 유지 자체는 stall 증거가 아님; command를 몰라 tracking 판정 보류. |
| slope_down_10deg | 전 구간 샘플에서 upright; 큰 pitch 붕괴는 샘플에 없음. | sampled frame에서 upright. | sampled frame에서 upright. | 짧은 한 클립으로 down-slope fall probability 추정 불가. |

### 5.3 수치와 영상의 일치·충돌

**일치:** A의 training late-window는 terrain·tracking·base-contact가 C보다 좋아졌고, A/model4800의 6지형 샘플도 비정상 자세 local optimum이나 명백한 즉시 붕괴를 보여 주지 않는다. 특히 boxes에서 빠르게 patch 밖으로 나온 장면은 “진행성이 완전히 희생된 생존형 정책”이라는 설명과는 맞지 않는다.

**충돌처럼 보이지만 실제로는 평가 조건 차이:** training late-500의 base-contact는 A도 약 28.7%다. 반면 각 19.98초 영상 샘플에서는 명확한 낙상을 관찰하지 못했다. 이것을 “영상이 training 낙상률을 반증한다”고 해석하면 안 된다. training scalar는 많은 env/episode와 curriculum distribution의 집계이고, native-play 영상은 단일 짧은 trajectory다. 영상에 낙상이 안 보인다는 사실은 low fall-rate 추정치가 아니다.

**미측정:** 영상 manifest에서 command·terrain seed·difficulty·초기 상태가 정책 간 paired라는 근거는 확인되지 않았다. 따라서 박스 탈출 시각이나 화면상 위치를 command tracking score로 변환하지 않았다.

---

## 6. 핵심 발견과 경쟁 설명

### 발견 1 — A의 +2K는 training distribution에서 유효한 성숙 신호다

- **관찰:** A vs C late-500에서 terrain +3.42%, XY -2.22%, yaw -9.68%, base-contact -1.032%p; late-300도 같은 방향.
- **해석:** 동일 reward/source/PPO에서 같은 checkpoint를 이어 학습하면서 H-005가 재적응 후 추종과 접촉 안정성을 함께 다듬었을 가능성이 높다.
- **경쟁 설명:** 단일 seed, curriculum trajectory, stochastic optimization 때문에 일부 차이는 우연한 경로 차이일 수 있다. 특히 A 초기 약 260 iteration은 resume reset 재적응이다.
- **반대 근거:** A의 terrain은 직전 500에서 마지막 500으로 소폭 낮아지고, final last-100은 model4800 근방보다 base-contact/episode length가 약간 불리하다. 완전한 단조 개선은 아니다.
- **판별:** 동일 fixed evaluator에서 C final2998 vs A final4997을 paired 평가한다.

### 발견 2 — H-005 reward 자체의 효과는 아직 작고 trade-off가 있다

- **관찰:** 보존된 same-parent unchanged 3K control 요약 대비 C는 XY 약 2.3% 낮지만 terrain 약 0.4% 낮고 base-contact 약 +0.145%p, yaw 차이는 매우 작다.
- **해석:** `feet_air_time 0.20→0.25`가 보행 cadence/진행성을 조금 바꿔 XY 추종에 도움을 줬을 가능성은 있다.
- **경쟁 설명:** control raw archive를 이번에 같은 파서로 재계산하지 못했다. 단일 seed와 curriculum variation도 있다.
- **반대 근거:** terrain/contact의 명백한 동시 개선이 없고 영상도 matched evaluator가 아니다.
- **판별:** control final과 C final의 fixed paired evaluator. 이 결과가 나쁘면 5K matched-control 추가 학습은 정보가 적으므로 하지 않는다.

### 발견 3 — A video의 boxes 진행은 유망하지만 causal evidence는 아니다

- **관찰:** A/model4800 `boxes.mp4`는 약 14–15 s에 patch 밖 평탄면으로 나온 장면이 보인다. B/C는 late sample까지 boxes 안에 있다.
- **해석:** A가 obstacle interaction에서 더 높은 진행성을 갖는 신호일 수 있다.
- **경쟁 설명:** box placement, initial pose, command, terrain seed/difficulty가 matched되지 않았을 수 있다. 같은 tracking camera라 화면상의 패치 이동도 정확한 world displacement가 아니다.
- **반대 근거:** 다른 5지형에서는 세 정책의 차이가 훨씬 작다.
- **판별:** 같은 boxes instance/command로 world-frame progress와 stall time을 측정한다.

### 발견 4 — final checkpoint를 버릴 근거는 없다

- **관찰:** A 마지막 500에서 tracking/contact/episode가 공동 붕괴하지 않는다. final last-100도 model4800 근방보다 terrain/XY/yaw는 더 좋다.
- **해석:** 충분히 긴 resume에서는 자동 reward-best보다 final numbered를 기본 대표로 쓰는 프로젝트 원칙과 이번 데이터가 일치한다.
- **경쟁 설명:** 자동 best model4800의 짧은 stability 지표가 final보다 약간 나은 부분이 있고, 실제 final 영상이 없다.
- **판별:** checkpoint tournament를 만들지 말고, 우선 final4997 하나를 fixed evaluator/native play로 검증한다. final 행동이 예상 밖으로 나쁠 때만 model4800을 비교 후보로 되돌린다.

---

## 7. checkpoint·가설·프로젝트 결정

### 7.1 실행 / evidence / 가설 / 정책 상태

| 항목 | 판정 | 근거 |
|---|---|---|
| B 실행 | **COMPLETE** | exit 0, 3000 scalar points, final2999 보존, validation PASS |
| C 실행 | **COMPLETE** | exit 0, 1500 resume points, final2998 보존, validation PASS |
| A 실행 | **COMPLETE** | exit 0, 2000 resume points, final4997 보존, validation PASS |
| checkpoint/video identity | **확인됨** | 18 MP4 manifest SHA 일치; source checkpoint SHA를 학습 archive 실제 bytes와 연결 |
| C→A parent lineage | **원본 바이트까지 확인됨** | C final2998 SHA = A metadata source SHA = `9454…85cc` |
| corrected H-001→C parent lineage | **기록상 연결됨, 이번 입력에서 parent bytes 미포함** | child metadata + 프로젝트 보존 parent SHA `5e3a…8ad82` |
| H-005 reward 가설 | **PROMOTE — fixed paired evaluation까지만** | same-parent 3K에서 작은 XY 신호, 5K continuation 자체는 개선; direct matched 5K control/evaluator 부재 |
| A 대표 checkpoint | **final `model_4997.pt` 우선** | late joint collapse 없음; 자동 best4800은 reward alias, 영상 source는 4800이라 final 행동은 미확인 |
| OFFICIAL 제출 근거 | **아님** | 세 run 모두 PERSONAL; fixed official evaluator/공식 점수 없음 |

### 7.2 model_best와 final을 혼동하지 않기

- B: auto best/video = `model_2750`; representative candidate = final `model_2999`; final video 없음.
- C: auto best = `model_2900`; video/representative = final `model_2998`.
- A: auto best/video = `model_4800`; representative candidate = final `model_4997`; final video 없음.

모든 선택 checkpoint와 final checkpoint의 tensor를 로드해 finite 여부와 checkpoint `iter` field를 확인했고 파일명 iteration과 맞았다. 이것은 **파일 무결성/로드 가능성** 확인일 뿐 정책 품질 증거는 아니다.

---

## 8. 다음 한 번의 행동

### 우선순위 1 — 새 학습 없이 fixed paired evaluator

가능하면 이미 보존된 다음 checkpoint를 한 배치에서 평가한다.

1. **H-001 corrected unchanged 3K final** — H-005 reward delta의 직접 control
2. **H-005 corrected 3K final `model_2998` (`9454…85cc`)** — reward delta candidate
3. **H-005 corrected 5K final `model_4997` (`6237…10a5`)** — 추가 2K가 행동 성능으로 이어졌는지 확인
4. **H-005 fresh3K final `model_2999` (`ff51…25a2`)** — fresh/resume path-dependence를 분리할 필요가 있을 때 포함

맞출 조건:

- 동일 evaluator code/version
- 동일 command sequence 또는 고정 command set
- 동일 terrain family·difficulty·instance/seed set
- 동일 episode horizon과 초기 상태 정책
- x/y/yaw tracking을 분리 기록
- 실제 world-frame forward/obstacle progress와 stall time
- fall/base-contact와 episode survival
- hip/torso raw posture, 가능하면 foot contact/duty-cycle·action delta
- 복수 evaluator seed가 가능하면 같은 seed set을 모든 정책에 사용

결과별 결정:

- C가 unchanged control보다 tracking/progress를 개선하고 안정성도 유지하며, A가 C보다 추가로 좋아지면 → **H-005를 장기 후보로 유지**하고 그때 same-parent unchanged 3K→5K continuation을 만들어 reward 효과의 장기 causal confirmation을 고려.
- C가 control보다 명확히 나쁘면 → A의 5K 개선은 “좋은 reward”보다 “더 오래 학습한 H-005”일 수 있으므로 **H-005 최종 채택은 중단/HOLD**. 굳이 matched control을 5K까지 새로 학습할 정보가치가 낮다.
- C와 control이 사실상 동률인데 A만 크게 좋아지면 → reward보다 학습량/경로가 핵심일 수 있다. 다음 실험은 reward 확대가 아니라 **동일 길이 baseline/unchanged continuation**이 우선이다.
- final4997이 fixed evaluator에서 model4800보다 예상 외로 나쁘다는 독립 신호가 생길 때만 두 checkpoint를 추가 비교한다. 지금 단계에서 PC checkpoint tournament나 새 selector를 만들 이유는 없다.

---

## 9. 한계와 재확인 가능한 근거

### 이번에 직접 확인/재계산한 것

- 세 학습 archive metadata/status/config
- 세 raw TensorBoard event 전 구간 scalar 파싱
- resume global-step 경계와 accumulator reset
- late-500/late-300/last-100 재집계
- source/PPO/reward 설정 비교
- C final2998 ↔ A parent의 실제 SHA exact match
- B model2750, C model2998, A model4800의 video manifest ↔ 실제 checkpoint SHA 연결
- MP4 18개 SHA/codec/resolution/fps/frame count/duration
- 지정 시각의 프레임 샘플과 stairs/boxes/slope-up dense sequence
- 선택/final checkpoint tensor finite 및 iteration field

### 기존 프로젝트 자료에서 인용한 것

- corrected H-001 Run05 parent가 `termination=-50`, `feet_air_time=+0.20`이고 C/H-005가 같은 parent에서 `0.25`로 단일 변경됐다는 lineage 기록
- same-parent H-001 unchanged 3K late-500 summary `5.5010 / 0.3695 / 1.0455 / 29.616%`
- 충분히 진행한 resume에서 joint late collapse가 없으면 final numbered checkpoint를 기본 대표로 쓰는 운영 원칙
- H1 six-terrain suite의 fixed slope 구성과 “정성 visual check이지 fixed evaluator가 아님”이라는 도구 경계

관련 핵심팩: `14_H1_NEXT_RUN_PARAMETER_COMPARISON.md`, `16_EXPERIMENT_EXPORT_AND_TENSORBOARD.md`, `18_H1_FINALIZE_REPORT_LIMITATIONS.md`, `19_ISSACSIMZ_EXTERNAL_EVIDENCE_CLI.md`.

### 아직 확인하지 못한 것

- corrected H-001 unchanged 3K control의 raw archive를 이번 파서로 재집계한 값
- A final `model_4997` 및 B final `model_2999`의 행동 영상/fixed evaluation
- 영상 간 동일 command·terrain seed·difficulty·initial-state 보장
- 복수 seed에서 H-005 효과의 재현성
- 공식 evaluator 점수 또는 OFFICIAL 서버 성능
- training `base_contact`를 fixed-evaluator fall rate로 변환하는 관계

---

## 최종 판단

이번 자료가 가장 강하게 말해 주는 사실은 **H-005 corrected lineage가 3K에서 멈추지 않고 5K까지 이어졌을 때 후반 tracking·terrain·training contact가 동시에 개선됐다는 것**이다. 따라서 A는 C보다 더 성숙한 H-005 정책이다. 그러나 이것은 `feet_air_time=0.25` 자체가 `0.20`보다 우월하다는 증명이 아니다. 그 질문에는 same-parent unchanged control이 필요하며, 현재 보존 요약상 3K 차이는 작고 trade-off가 남는다.

따라서 현재 결정은 **H-005를 fixed paired evaluation 단계까지 PROMOTE하되 최종 채택은 보류**하는 것이다. 대표 checkpoint는 A final `model_4997.pt`로 두되, 그 행동은 아직 미확인이므로 다음 작업은 새 GPU 학습이 아니라 보존 checkpoint의 동일 evaluator 비교가 가장 정보가 크다.
