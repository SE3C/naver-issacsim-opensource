# H1 H-005 Fresh 3K vs Corrected 3K→5K 심층 분석

- 작성일: 2026-09-27
- 로봇: Unitree H1 / `Humanoid-v0`
- 분석 대상 A: H-005 `feet_air_time=+0.25` **fresh 3K**
- 비교 대상 B1: corrected `feet=+0.20` 부모에서 H-005 `+0.25`로 분기한 **3K endpoint**
- 비교 대상 B2: B1 final에서 reward 변경 없이 이어간 **3K→5K continuation**
- 환경 분류: 세 학습 Run 모두 **PERSONAL**. OFFICIAL 점수나 제출 성능 증거가 아니다.
- 분석 범위: 사용자가 제공한 3개 통합 학습 archive + 각 정책의 6지형 영상 bundle 3개. 새 학습·렌더링·export·외부 게시·서버 작업은 수행하지 않았다.

## 1. 결론 요약

### 세 질문에 대한 답

**1) 이번 정책은 목표 행동을 실제로 얼마나 수행하는가?**  
제공 영상으로 직접 확인 가능한 정책은 fresh3K의 `model_2750`, corrected3K의 final `model_2998`, corrected5K의 `model_4800`이다. 세 정책 모두 6지형의 표본 프레임에서 upright locomotion을 보였고, stairs/inverted-stairs/random-rough에서는 0.5초 간격 전 구간 표본에서 명백한 낙상을 확인하지 못했다. 가장 구분력이 큰 장면은 **boxes**다. fresh `model_2750`은 약 **9.1–9.5 s**에 몸통이 거의 수평까지 무너지는 큰 자세 손실을 보인 뒤 약 **9.7 s**부터 다시 upright로 회복한다. corrected3K `model_2998`과 corrected5K `model_4800`은 같은 시각대의 각자 영상에서 이런 큰 자세 붕괴가 보이지 않았다. 특히 corrected5K `model_4800`은 약 **15.4 s 이후 box patch를 벗어나 평지로 진입하는 장면**이 명확하다. 다만 세 영상은 command/terrain seed/difficulty/initial state가 manifest에 기록되지 않은 native qualitative suite이므로, 이 차이를 동일 episode의 traversal 성능 차이로 수치화할 수 없다.

**2) 무엇이 관찰된 차이이고, 무엇을 설정 변경 효과로 해석할 수 있는가?**  
세 Run의 **현재 effective env/reward 설정은 동일**하며, 실제 `env.yaml` diff는 `log_dir`만 다르다. seed 42, 4096 env, 24 rollout steps/env, PPO 핵심 설정도 동일하다. 차이는 학습 계보다. fresh3K는 처음부터 `feet_air_time=+0.25`로 0→2999를 학습했고, corrected3K는 `feet=+0.20`로 학습된 parent `model_1499`에서 `+0.25`로 바꿔 1499→2998을 resume했으며, corrected5K는 그 final `model_2998` 바이트를 정확히 이어 2998→4997을 같은 reward로 추가 학습했다. 따라서 **corrected3K→5K의 변화는 동일 reward 아래 추가 학습·curriculum 진행과 함께 관찰된 변화**라고 말할 수 있다. 반면 이 세 파일만으로 `feet_air_time 0.20→0.25` 자체의 인과효과는 확정할 수 없다. 그 질문의 직접 대조군은 같은 corrected parent에서 reward를 유지한 unchanged continuation이다.

**3) 현재 자료에서 내려야 할 결정은 무엇인가?**  
- 실행 상태: 세 Run 모두 **COMPLETE**, `exit_code=0`, evidence validation **PASS**.
- H-005 reward 가설 자체: **HOLD**. 이유는 corrected 3K의 보존된 기존 unchanged-control 요약에서 XY error만 작게 좋아지고 terrain/base-contact는 거의 동률·trade-off였으며, 이번 5K에는 동일 길이의 `feet=+0.20` unchanged 5K raw control이 없기 때문이다.
- 정책 후보: corrected 5K는 **fixed paired evaluation 단계로 PROMOTE할 가치가 있다**. late-500에서 corrected3K 대비 terrain, XY, yaw, training base-contact, episode length가 모두 같은 방향으로 개선됐고 boxes 영상도 질적으로 강하다. 이는 최종 채택이나 OFFICIAL 우월성 주장이 아니다.
- checkpoint: 충분히 진행한 resume의 운영 원칙상 **final `model_4997.pt`가 기본 대표 후보**다. late-500/late-300에서 terrain·tracking·contact가 함께 악화되는 late collapse가 보이지 않는다. 그러나 제공된 6지형 영상은 `model_4800.pt`에서 만들어졌으므로 **final 4997의 실제 행동은 아직 미확인**이다.
- 다음 한 번의 행동: **새 학습보다 먼저 `model_4997`과 `model_4800`을 동일 command/terrain/seed의 fixed evaluator에서 비교**한다. 이 검증은 “final을 대표 정책으로 쓸지”를 바로 결정하며, 4800 영상에서 보인 boxes 통과가 final에도 유지되는지 확인할 수 있다. reward 인과효과까지 필요할 때에만 그 다음으로 corrected H-001 unchanged 3K control을 +2K 이어 `feet=+0.20` 5K control을 만드는 것이 맞다.

---

## 2. 실제 Run → checkpoint → 영상 identity

### 2.1 받은 원본과 outer SHA-256

| 역할 | 파일 | SHA-256 |
|---|---|---|
| A 학습 | `20260927-032343-h1-h005-fresh3k-r01-20260927.tar.gz` | `089b2dcfcecba53ad41dcf70810a753e3a04a89891281cd25aef787c04814b40` |
| A 6지형 | `checkpoint-h1-model_2750-6d7d0ecb13c7-download.tar.gz` | `807061318ab5a870b82202b2d5d81e15f95bbffc9add783dc875e92f6d1c4dc5` |
| B1 학습 | `20260925-071158-h1-h005-r02-gait025-corrected-h1-corrected-20260.tar.gz` | `3a25c5c728959c28a35148bb1d9f50066720fceec56bf1c68e1b906245b98e96` |
| B1 6지형 | `checkpoint-h1-model_2998-9454afa964bb-download.tar.gz` | `2c9640f8831ba938f714ebd76fbf26082958e392773af0844e5f9bf006d8a2e5` |
| B2 학습 | `20260927-054950-h1-h005-corrected3kto5k-r02-20260927.tar.gz` | `f436ef315792f72cb80395169e4233d303ebf71d5ae3ea724b552d76a3841d07` |
| B2 6지형 | `checkpoint-h1-model_4800-40c6a4a8273c-download.tar.gz` | `1b0d862cc778fc7b1d878169eb932ddba045f4fec2594829e1c8fe8a1f1b8382` |

### 2.2 Run 정체성

| 항목 | A: fresh3K | B1: corrected3K | B2: corrected5K continuation |
|---|---|---|---|
| mode | PERSONAL | PERSONAL | PERSONAL |
| 실행 | fresh | resume | resume |
| 실제 TensorBoard global iteration | `0..2999` (3000점) | `1499..2998` (1500점) | `2998..4997` (2000점) |
| 부모 | 없음 | 기록상 corrected H-001 `model_1499` | B1 final `model_2998` |
| 부모 SHA | — | `5e3a3150…1b8ad82` | `9454afa9…6a485cc` |
| 부모 바이트 대조 | 해당 없음 | 이 입력 세트에는 부모 archive 미포함; metadata 기록과 기존 보존 문서만 연결 | **직접 검증됨**: B1 `model_2998.pt` SHA와 B2 source SHA exact match |
| seed / env | 42 / 4096 | 42 / 4096 | 42 / 4096 |
| rollout | 24 steps/env/iter | 동일 | 동일 |
| 실제 agent save interval | 50 | 100 | 50 |
| 종료 | COMPLETE, exit 0 | COMPLETE, exit 0 | COMPLETE, exit 0 |
| evidence | PASS | PASS | PASS |

핵심 provenance 경로:

- 각 train archive: `<run>/metadata.json`, `<run>/validation.json`, `<run>/native_run/params/env.yaml`, `<run>/native_run/params/agent.yaml`, `<run>/native_run/events.out.tfevents*`, `<run>/collected/exported/`
- 각 video archive: `video_suite_manifest.json`, `videos/*.mp4`

`source_provenance_verified=false`는 B1/B2 metadata에 남아 있다. B1은 실제 부모 바이트가 이번 입력에 없으므로 그 상태를 유지한다. B2는 staging metadata 필드는 false지만, 이번 분석에서 **공급된 B1 final checkpoint의 실제 SHA를 계산해 B2 source SHA와 일치함을 별도로 검증**했다. 이 두 진술은 모순이 아니다.

### 2.3 effective reward와 환경

세 Run의 `native_run/params/env.yaml`을 직접 diff하면 `log_dir` 한 줄을 제외하고 동일하다. 핵심 참가자 reward는 모두 다음과 같다.

| reward | 세 Run의 effective weight |
|---|---:|
| `track_lin_vel_xy_exp` | +0.5 |
| `track_ang_vel_z_exp` | +0.5 |
| `feet_air_time` | **+0.25** |
| `termination_penalty` | -50.0 |
| `flat_orientation_l2` | -1.5 |
| `ang_vel_xy_l2` | -0.05 |
| `joint_deviation_hip` | -0.2 |
| `joint_deviation_torso` | -0.1 |
| `action_rate_l2` | -0.0005 |

B1의 부모 corrected H-001은 보존된 프로젝트 자료 기준 `feet_air_time=+0.20`, `termination=-50`인 parent다. 따라서 B1에서 묻는 변경은 `feet_air_time +0.20→+0.25`; B2는 reward를 더 바꾸지 않은 continuation이다. A는 +0.25를 처음부터 사용한 fresh 학습이므로 B1과 학습 경로가 다르다.

환경의 terrain generator는 `curriculum: true`, generator `seed: null`, difficulty range `0.0..1.0`이다. command manager는 10초마다 재샘플하며 허용 범위는 `lin_vel_x=-1.0..1.5`, `lin_vel_y=-0.5..0.5`, `ang_vel_z=-1.0..1.0`, heading `-π..π`다. 이는 **학습 설정**이다. video manifest에는 각 clip의 실제 command draw, terrain seed/difficulty, 초기 상태가 기록되지 않으므로 해당 값이 영상끼리 matched라고 가정하지 않았다.

PPO 핵심 설정은 세 Run에서 동일하다: 5 epochs, 4 mini-batches, adaptive LR 0.001, gamma 0.99, lambda 0.95, entropy coef 0.008, desired KL 0.01, clip 0.2, max grad norm 1.0.

### 2.4 checkpoint와 영상의 실제 연결

| 정책 | 자동 `model_best` | final numbered | 제공 6지형 source | 판정 |
|---|---|---|---|---|
| A fresh3K | `model_2750.pt`, SHA `6d7d0ecb…c29eb` | `model_2999.pt`, SHA `ff51151a…e25a2` | **2750** | 영상은 auto-best 행동. final 2999 행동은 미확인 |
| B1 corrected3K | `model_2900.pt`, SHA `af97fc0b…` | `model_2998.pt`, SHA `9454afa9…6a485cc` | **2998** | 영상이 final 행동과 exact-match |
| B2 corrected5K | `model_4800.pt`, SHA `40c6a4a8…64a8a` | `model_4997.pt`, SHA `62376709…6310a5` | **4800** | 영상은 auto-best 4800. final 4997 행동은 미확인 |

위 checkpoint SHA는 train archive에서 해당 numbered checkpoint를 선택적으로 추출해 직접 계산했다. video bundle의 `checkpoint_sha256`/`source_checkpoint_sha256`과도 대조했다. 18개 MP4 역시 manifest에 적힌 SHA와 실제 파일 SHA가 모두 일치했다.

세 suite의 모든 MP4는 H.264, 1920×1080, 50 fps, 999 frames, 19.98 s였다. 이 검증은 영상 무결성과 source checkpoint identity를 말해 줄 뿐, command가 같거나 terrain realization이 같다는 뜻은 아니다.

---

## 3. 무엇을 직접 비교할 수 있는가

| 질문 | 판정 | 이유 |
|---|---|---|
| B1→B2에서 추가 +2K가 학습 내부 지표에 어떤 변화를 동반했는가 | **직접 비교에 적합** | 같은 실제 parent chain, 같은 effective reward/env/PPO/seed/num_envs. B1 final 바이트와 B2 source SHA도 exact match |
| A fresh3K와 B1 staged corrected3K의 3K endpoint가 어떻게 다른가 | **조건부 비교** | endpoint 학습량과 current 설정은 비슷하지만 B1의 앞 1.5K는 feet=0.20 parent에서 이미 학습된 상태. 학습 경로 효과가 섞임 |
| `feet_air_time 0.20→0.25`의 인과효과 | **현재 입력만으로 판단 불가** | raw unchanged sibling control이 이번 파일 세트에 없음. B2의 개선에는 추가 학습량도 포함 |
| 세 영상 중 어느 정책이 boxes에서 더 안정적으로 보이는가 | **질적 비교 가능** | 실제 프레임 관찰은 가능. 다만 command/seed/difficulty가 unmatched라 정량 승패로 승격 불가 |
| final 4997이 4800보다 실제 행동이 좋은가 | **판단 불가** | 영상 source는 4800; final 4997 영상/evaluator 없음 |
| OFFICIAL 제출 성능 | **판단 불가** | 전부 PERSONAL evidence이며 공식 evaluator 결과 없음 |

기존 프로젝트의 corrected 3K sibling 요약에는 같은 corrected parent의 unchanged control late-500이 `terrain 5.5010 / XY 0.3695 / yaw 1.0455 / base-contact 29.616%`, H-005 B1이 `5.4776 / 0.3609 / 1.0410 / 29.761%`로 기록돼 있다. 이는 H-005의 **작은 XY 개선 신호와 거의 동률인 yaw, terrain·contact trade-off**를 시사한다. 그러나 unchanged control의 raw archive가 이번 입력에 없으므로 이 값은 `14_H1_NEXT_RUN_PARAMETER_COMPARISON.md`의 보존 요약 인용이며, 이번에 동일 parser로 재계산한 수치가 아니다.

---

## 4. TensorBoard 원본 재분석

### 4.1 처리 방법

각 Run에서 `native_run/events.out.tfevents*`를 직접 읽었다. 세 Run 모두 event 파일은 하나였고 scalar step reset/중복 파일 병합 문제는 없었다. scalar는 TFRecord framing에서 `Event.summary.value.simple_value`를 파싱했다.

- A: 3000점, step `0..2999`
- B1: 1500점, global step `1499..2998`
- B2: 2000점, global step `2998..4997`

resume 직후에는 episode/curriculum 통계가 재적응하는 큰 transient가 실제로 관찰된다. 따라서 head-to-head는 **각 Run의 late-500**을 사전에 동일 window로 사용했고, 경계 민감도는 **late-300**으로 확인했다. 자동 finalizer의 reward-best warm-up 필터와 전체 trajectory 해석은 분리했다.

### 4.2 late-500 동일 정의 비교

아래는 raw TensorBoard에서 직접 재계산한 평균이다. `base-contact`와 `time-out`은 **training termination 통계**이며 fixed evaluator의 낙상률/Survival이 아니다.

| 지표 (late-500 mean) | A fresh3K | B1 corrected3K | B2 corrected5K | B2 − B1 |
|---|---:|---:|---:|---:|
| `Curriculum/terrain_levels` | 5.5038 | 5.4776 | **5.6646** | **+0.1871** |
| `Metrics/base_velocity/error_vel_xy` | 0.37355 | 0.36093 | **0.35293** | **-0.00800** (-2.2%) |
| `Metrics/base_velocity/error_vel_yaw` | 1.02692 | 1.04095 | **0.94024** | **-0.10072** (-9.7%) |
| `Episode_Termination/base_contact` | 29.935% | 29.761% | **28.729%** | **-1.032 %p** |
| `Episode_Termination/time_out` | 70.074% | 70.246% | **71.286%** | +1.040 %p |
| `Train/mean_episode_length` | 775.83 | 773.76 | **785.30** | +11.55 (+1.5%) |
| `Policy/mean_std` | 1.3455 | 1.3419 | **1.3189** | -0.0230 |
| `Loss/value` | 0.00513 | 0.00498 | **0.00476** | -0.00021 |
| `Train/mean_reward` | 2.840 | 2.825 | **3.620** | +0.796 |

`Train/mean_reward`는 이번 세 Run의 current reward weights가 동일하므로 내부 trajectory 상태를 비교하는 보조값으로는 쓸 수 있다. 그래도 공식 성능 metric이나 traversal score로 해석하지 않았다.

**핵심 관찰:** B1→B2 continuation은 late-500에서 tracking 두 축, terrain, base-contact, episode length가 동시에 같은 방향으로 개선됐다. 단순히 “낙상 대신 정지해서 버티는” 패턴이라면 tracking/progress 계열이 함께 좋아지는 설명과 잘 맞지 않는다. 다만 terrain curriculum이 학습과 함께 변하므로 고정 난이도 통과율의 개선이라고 부르지는 않는다.

### 4.3 late-300 민감도 확인

| 지표 (late-300 mean) | A fresh3K | B1 corrected3K | B2 corrected5K |
|---|---:|---:|---:|
| terrain | 5.5177 | 5.4753 | **5.6869** |
| XY error | 0.37567 | 0.35846 | **0.35322** |
| yaw error | 1.02544 | 1.02526 | **0.94112** |
| base-contact | 29.435% | 29.938% | **28.673%** |
| timeout | 70.569% | 70.066% | **71.340%** |
| episode length | 781.74 | 771.89 | **786.11** |
| mean reward | 2.945 | 2.885 | **3.645** |
| policy std | 1.3437 | 1.3398 | **1.3166** |

따라서 B2의 개선 방향은 late-500 경계 하나를 골라 만든 결과가 아니다. A와 B1 사이의 작은 차이는 일부 지표에서 window에 따라 방향이 바뀐다. 예를 들어 base-contact는 late-500에서는 B1이 약 0.17 %p 낮지만 late-300에서는 A가 약 0.50 %p 낮다. **3K fresh vs staged의 작은 차이는 강한 우열 근거로 쓰지 않는 것이 맞다.**

### 4.4 최적화 안정성

전체 raw event에서 NaN/Inf scalar는 검출되지 않았다. console에서도 `Traceback`, CUDA OOM, fatal error 패턴을 확인하지 못했고 실제 iteration marker는 각각 요청된 구간 끝까지 이어졌다.

`Loss/value`의 전체 분포:

| Run | median | p95 | p99 | max @ step | `>=1` |
|---|---:|---:|---:|---:|---:|
| A | 0.00528 | 0.00679 | 0.00805 | 0.18083 @ 1 | 0 |
| B1 | 0.00500 | 0.00546 | 0.00568 | 0.03518 @ 1499 | 0 |
| B2 | 0.00482 | 0.00537 | 0.00560 | 0.01647 @ 2998 | 0 |

fresh 초기와 resume 첫 step의 transient를 제외하면 value loss가 폭발하거나 장기 상승하는 신호가 없다. `Policy/mean_std` late-500은 1.346→1.342→1.319로 내려가지만, std 단독으로 수렴 성공을 판정하지 않았다. 여기서는 tracking/terrain/contact와 같이 움직였다는 점만 사용한다.

### 4.5 자동 `model_best`와 raw reward peak

B2 raw `Train/mean_reward` 전체 최대는 **4.920 @ 3042**지만 resume finalizer의 warm-up eligibility는 `2998 + max(50, floor((4997-2998)*0.10)) ≈ 3197` 이후다. 따라서 이 early re-adaptation peak는 자동 selector 후보 밖이며, eligible reward peak가 late 구간에 있어 `model_best=model_4800`으로 연결된 것은 기존 finalizer 규칙과 일관된다. 이 auto-best는 어디까지나 training reward 후보이지, final 4997보다 official/behavioral 성능이 좋다는 증거가 아니다.

---

## 5. 6지형 행동 비교

### 5.1 영상 조사 방법과 한계

18개 MP4를 ffprobe/SHA로 확인한 뒤 프레임 시퀀스로 직접 조사했다.

- boxes/stairs/inverted-stairs/random-rough: **0.5 s 간격으로 전체 20 s**를 훑음
- boxes 핵심 disturbance와 exit: **0.2 s 간격**으로 `8.5–10.5 s`, `13.0–16.0 s` 추가 조사
- ±10° slope: 전체 clip을 약 **2.5 s 간격**으로 확인

따라서 boxes의 회복 과정은 비교적 촘촘히 확인했지만, slope의 보행 주기·진동 주파수처럼 연속 관찰이 필요한 주장은 하지 않는다. 한 clip에서 sampled fall이 없다고 낮은 낙상률을 추정하지도 않는다.

또한 manifest에는 command/terrain seed/difficulty/initial state/camera 파라미터가 없다. 학습 env의 command는 10초마다 재샘플되므로 같은 9–10초대라도 실제 각 clip의 command가 같다고 가정할 수 없다. 영상의 파란/초록 visualizer 방향을 정량 command로 역산하지 않았다.

### 5.2 지형별 관찰

| 지형 | A fresh3K @2750 | B1 corrected3K @2998 | B2 corrected5K @4800 | 판단 한계 |
|---|---|---|---|---|
| **stairs** | 14.5 s 전후 계단 접근, 이후 계단 영역을 지나며 sampled frames에서 upright | 유사하게 14.5–19.5 s 계단 영역 통과, sampled fall 없음 | 계단 접근·진행 확인, sampled fall 없음 | 접근 시각 차이는 command/scene unmatched라 속도 우열로 해석 불가 |
| **inverted_stairs** | 전 구간 0.5 s 표본에서 upright, 후반 계단 영역을 벗어남 | upright 진행, 뚜렷한 collapse 없음 | upright 진행; 일부 순간 lean은 있으나 회복/진행 | 한 trajectory만으로 fall rate·평균 traversal 불가 |
| **boxes** | **9.1–9.5 s 큰 전방/측방 자세 붕괴**, 거의 수평까지 내려감. **9.7 s 이후 upright 회복**. 13–16 s에도 patch 내부 | 8.5–10.5 s에는 같은 크기의 붕괴 없음. 13–16 s patch 내부에서 계속 진행 | 8.5–10.5 s upright. **약 15.4 s부터 평지로 명확히 이탈** | 가장 강한 질적 차이지만 scene/command/difficulty unmatched. 통과율 수치로 승격 금지 |
| **random_rough** | 0.5 s 표본에서 upright locomotion, 후반 평지 쪽 진행 | 유사; 명백한 sampled fall 없음 | 유사; 명백한 sampled fall 없음 | 미세 gait 품질 우열은 frame sampling만으로 불충분 |
| **slope_up_10deg** | 약 2.5 s 표본 전 구간 upright | sampled upright | sampled upright | 지형 경계가 저대비이고 camera tracking이 있어 거리/속도 정밀 비교 불가 |
| **slope_down_10deg** | sampled upright | sampled upright | sampled upright | 동일. pitch/roll RMS나 jitter 주파수는 미측정 |

### 5.3 수치와 영상의 교차검증

B2는 학습 late-500에서 B1보다 base-contact termination이 1.03 %p 낮고 XY/yaw error가 각각 약 2.2%/9.7% 낮다. boxes 영상에서 B2@4800이 큰 붕괴 없이 patch를 벗어나는 장면은 이 “tracking + contact가 같이 나아진 방향”과 **정성적으로 일치**한다.

반대로 fresh A는 late-500 terrain이 B1보다 약간 높고 yaw error도 미세하게 낮지만 boxes 영상에서는 큰 자세 손실이 있다. 이는 training aggregate 하나만으로 특정 hard terrain의 행동 품질을 대표할 수 없다는 반례다. 따라서 fresh의 약간 높은 terrain/mean reward를 행동상 우월성으로 읽지 않았다.

B1/B2의 weighted posture/reward term도 late-500에서 대체로 약간 덜 부정적으로 변한다(`joint_deviation_hip -0.03459→-0.03228`, torso `-0.00587→-0.00543`, flat orientation `-0.01106→-0.01064`, feet_slide `-0.04654→-0.04078`). 그러나 이 값은 **weighted training reward term**이다. 비가중 hip angle/RMS의 계산 정의를 여기서 확인하지 않았으므로 weight로 나눠 “실제 자세가 몇 % 좋아졌다”고 역산하지 않았다.

---

## 6. 핵심 발견과 경쟁 설명

### 발견 1 — 3K→5K continuation은 단순 reward 상승만이 아니라 여러 training 축에서 함께 개선됐다

- **관찰:** B1→B2 late-500 terrain +0.187, XY -0.0080, yaw -0.1007, base-contact -1.032 %p, episode length +11.55. late-300에서도 방향 유지.
- **해석:** 같은 reward를 유지한 채 추가 학습하면서 curriculum 적응과 command tracking, 접촉 안정성이 함께 개선된 것으로 보는 것이 가장 자연스럽다.
- **경쟁 설명:** resume 후 curriculum state/episode sampling의 변화, 단일 seed의 stochasticity, terrain generator `seed=null`이 섞인다. 같은 seed가 matched episode를 보장하지 않는다.
- **반대 근거:** 없다기보다는, 영상 source가 4800이고 final은 4997이라는 provenance gap 때문에 “최종 정책 행동도 개선됐다”까지는 아직 못 간다.
- **판별:** 4800 vs 4997 fixed paired evaluator가 가장 싸고 직접적이다.

### 발견 2 — fresh3K와 corrected3K는 training aggregate상 거의 같은 영역에 수렴하지만 행동은 완전히 동일하지 않다

- **관찰:** late-500 terrain 차이 0.026, yaw 0.014, base-contact 0.17 %p 수준으로 작고 일부는 late-300에서 방향이 바뀐다. 반면 fresh@2750 boxes에는 9.1–9.5 s 큰 자세 붕괴가 있다.
- **해석:** 3K 시점의 평균 training scalar만으로 hard-terrain recovery morphology를 충분히 설명하지 못한다. staged history가 특정 recovery behavior에 영향을 줬을 가능성도 있다.
- **경쟁 설명:** 가장 큰 경쟁 설명은 영상 조건 mismatch다. fresh clip이 우연히 더 어려운 box realization/command를 받았을 수 있다.
- **판별:** 동일 boxes seed/difficulty/command로 2750/2998/4800을 재평가해야 한다.

### 발견 3 — `feet_air_time=+0.25`는 현재 자료에서 “망가진 값”은 아니지만, 인과적 승리도 아니다

- **관찰:** fresh 3K가 정상적으로 high-terrain 영역까지 학습되고, corrected branch도 5K까지 수치 붕괴 없이 이어진다. 기존 corrected 3K unchanged-control 요약 대비 H-005는 XY만 소폭 개선, terrain/contact는 거의 동률 또는 약한 열세였다.
- **해석:** +0.25는 최소한 이 계보에서 장기 학습을 방해하는 강한 negative setting으로 보이지 않는다. 5K에서 정책 자체는 더 경쟁력 있는 상태로 진화했다.
- **경쟁 설명:** B2의 개선은 +0.25의 효과가 아니라 +2K 추가 학습의 효과일 수 있다. 바로 이 이유로 reward hypothesis는 HOLD다.
- **판별:** reward 인과를 정말 결정하려면 동일 corrected parent 계보의 `feet=+0.20` unchanged child도 global 4997까지 같은 +2K를 진행하고 동일 evaluator로 비교해야 한다.

---

## 7. checkpoint·가설·프로젝트 판단

### 7.1 실행 / evidence / 가설 / 정책

| 층 | 현재 판정 |
|---|---|
| 실행 | **COMPLETE** — 세 Run 모두 exit 0, 요청 구간 끝까지 iteration 존재 |
| evidence | **PASS** — 각 archive validation PASS; 필요한 checkpoint와 18 MP4 identity를 추가 대조 |
| H-005 reward 가설 | **HOLD** — +0.25 장기 안정성은 긍정적이나 same-length unchanged control이 없어 reward 인과효과 미확정 |
| corrected5K 정책 | **fixed paired evaluation로 PROMOTE** — training late-window와 boxes 행동이 유망. OFFICIAL/최종 채택 아님 |
| 대표 checkpoint | **기본 후보는 final `model_4997.pt`**, 단 행동 미확인. 제공 영상이 증명하는 것은 `model_4800.pt`의 행동 |

### 7.2 왜 final 4997을 기본 후보로 두는가

이 프로젝트 운영 원칙은 충분히 긴 resume에서 final numbered checkpoint를 기본 대표로 두고, 마지막 수백 iteration에서 terrain·tracking·fall/contact가 함께 뚜렷하게 무너질 때만 이전 checkpoint를 검토하는 것이다. B2는 late-500과 late-300 모두에서 joint collapse가 보이지 않는다. 따라서 자동 reward-best 4800이라는 이유만으로 final 4997을 버릴 근거가 없다.

동시에 **4800이 행동상 더 좋지 않다는 증명도 없다.** 현재 영상은 4800뿐이다. 따라서 final 선택의 마지막 미확인 고리는 동일 evaluator의 4800↔4997 행동 비교다.

### 7.3 다음 한 번의 행동 — GPU 재학습보다 먼저

**우선순위 1: B2의 `model_4800.pt`와 final `model_4997.pt`를 동일 fixed evaluator에서 짝 비교한다.**

맞출 조건:

- 동일 command sequence와 command transition 시점
- 동일 terrain type, difficulty, terrain realization/seed와 initial state
- 동일 episode budget/window
- 동일 evaluator 코드/normalization
- 축별 `vx`, `vy`, yaw-rate error + 실제 progress/stall + base contact/fall/timeout
- boxes/stairs 같은 hard terrain의 실제 통과 여부와 회복 annotation

답할 질문은 하나다: **late training scalar 개선이 final 4997의 실제 행동으로 이어졌는가, 아니면 4800 근처가 더 좋은 behavioral checkpoint였는가?**

결과별 결정:

- 4997이 tracking/contact/progress를 유지하거나 개선 → final 4997을 H-005 현재 대표 정책으로 사용.
- 4997이 hard terrain에서 4800보다 뚜렷하게 악화 → final 원칙의 예외 근거가 생기므로 4800을 후보로 유지하고 악화 구간을 좁힘.
- 둘이 사실상 동률 → final 4997을 기본 대표로 유지하되 H-005 reward 가설은 여전히 HOLD.

**그 이후에도 reward 변경 자체의 인과효과가 의사결정에 필요할 때만** 새 학습을 고려한다. 필요한 최소 대조군은 corrected H-001 unchanged 3K control final에서 reward를 `feet=+0.20` 그대로 유지한 +2K continuation이다. parent/source/PPO/seed/num_envs/추가 iteration/evaluator를 H-005 3K→5K와 맞춰야 한다. 이 실행은 현재 분석 요청에는 포함되지 않았고 수행하지 않았다.

---

## 8. 한계와 재확인 가능한 근거 목록

### 직접 확인·재계산한 것

1. 6개 outer archive SHA-256.
2. 세 train archive의 `metadata.json`, validation, command, resume lineage, env/agent 설정.
3. B1 final `model_2998` ↔ B2 source checkpoint의 SHA exact match.
4. A `model_2750`/final2999, B1 model2900/final2998, B2 model4800/final4997의 선택적 checkpoint SHA.
5. video manifest의 checkpoint SHA 및 18개 MP4 SHA 실제 파일 대조.
6. 18개 영상의 codec/resolution/fps/frame count/duration.
7. 세 raw TensorBoard event의 전체 scalar 파싱, late-500/late-300 재집계, optimizer 분포와 nonfinite 검사.
8. 6지형 모두 프레임 조사; boxes/stairs/inverted-stairs/random-rough는 더 촘촘한 sequence 확인.

### 이번 입력만으로 확인하지 못한 것

1. B1의 부모 corrected H-001 `model_1499` 원본 바이트 — metadata와 기존 보존 자료에는 SHA가 있지만 부모 archive 자체가 이번 6개 입력에 없다.
2. corrected H-001 unchanged 3K control의 raw TensorBoard/event — 기존 프로젝트 요약값만 인용했다.
3. 6지형 video의 실제 numeric command, terrain seed/difficulty, initial state — manifest에 없음.
4. fresh final `model_2999`과 corrected5K final `model_4997`의 실제 6지형 행동 — 제공 영상 source가 각각 2750, 4800.
5. fixed evaluator·복수 seed·OFFICIAL score.
6. 비가중 hip/torso posture RMS, world-frame progress distance, stall time — 현재 video/TensorBoard만으로 동일 정의 정량치가 없다.

### 핵심 evidence locator

- A train: `20260927-032343-h1-h005-fresh3k-r01-20260927.tar.gz`
  - `metadata.json`
  - `native_run/params/{env.yaml,agent.yaml}`
  - `native_run/events.out.tfevents*`
  - `native_run/model_*.pt`
  - `collected/exported/{model_best.pt,report.html}`
- B1 train: `20260925-071158-h1-h005-r02-gait025-corrected-h1-corrected-20260.tar.gz` — 같은 내부 구조
- B2 train: `20260927-054950-h1-h005-corrected3kto5k-r02-20260927.tar.gz` — 같은 내부 구조
- 각 video bundle:
  - `video_suite_manifest.json`
  - `videos/stairs.mp4`
  - `videos/inverted_stairs.mp4`
  - `videos/boxes.mp4`
  - `videos/random_rough.mp4`
  - `videos/slope_up_10deg.mp4`
  - `videos/slope_down_10deg.mp4`

### 최종 판단 한 줄

**H-005 `feet_air_time=+0.25`는 5K까지 안정적으로 학습되며 corrected3K→5K에서 tracking·terrain·contact가 함께 좋아지고 boxes 행동도 유망해졌지만, reward 인과효과는 아직 HOLD다. 현재 가장 가치 있는 다음 검증은 새 학습이 아니라 final `model_4997`을 `model_4800`과 동일 fixed evaluator에서 직접 맞붙여 representative checkpoint를 확정하는 것이다.**
