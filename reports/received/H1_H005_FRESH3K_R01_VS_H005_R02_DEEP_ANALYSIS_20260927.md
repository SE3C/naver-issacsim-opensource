> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/incoming/other/reviewed/H1_H005_FRESH3K_R01_VS_H005_R02_DEEP_ANALYSIS_20260927.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# H1 H-005 Fresh3K R01 vs H-005 Corrected R02 심층 분석

- 작성일: 2026-09-27
- 로봇: Unitree H1 / `Humanoid-v0`
- 환경 분류: **모든 학습 Run은 PERSONAL**
- 분석 대상: H-005 `feet_air_time=0.25` fresh 3K, corrected H-005 R02 resume 3K, corrected H-001 unchanged control 3K
- 영상: 각 정책의 6지형 suite 총 18개 MP4
- 주의: 파일명 역할만으로 A/B를 정하지 않고 archive 내부 metadata와 checkpoint SHA로 관계를 재구성했다. 최신 fresh 3K를 현재 분석 대상 A로, 동일 reward의 corrected resume를 주 비교 B로 두되, **reward 인과 질문에는 H-001 unchanged control을 직접 대조군으로 사용**한다.

---

## 1. 결론 요약

### 질문 1 — 이번 정책은 목표 행동을 실제로 얼마나 수행하는가?

현재 최신 H-005 fresh 3K의 영상 source는 final `model_2999.pt`가 아니라 자동 `model_best`인 **`model_2750.pt`**다. manifest SHA와 학습 archive 내부 checkpoint SHA가 정확히 일치한다. 이 `model_2750` 정책은 제공된 6개 지형에서 샘플링한 전체 19.98초 구간에서 명백한 prone/fall 자세 없이 upright locomotion을 보였고, stairs·inverted stairs·random rough·boxes에 실제로 진입해 진행하는 장면이 확인된다. 다만 영상 manifest에는 numeric command, terrain seed, difficulty, 초기 상태가 없으므로 **명령 추종 점수·낙상률·통과율을 영상만으로 정량화할 수 없다.**

학습 내부 late-500(`2500..2999`)에서 fresh H-005는 terrain `5.5038`, XY error `0.3736`, yaw error `1.0269`, training base-contact termination `29.935%`, episode length `775.83`이다. 이는 학습이 초반 붕괴 상태에 머문 정책은 아니라는 강한 신호지만, training scalar는 fixed evaluator 성능이 아니다.

### 질문 2 — 비교 정책과의 차이 중 무엇이 관찰이고 무엇을 reward 효과로 해석할 수 있는가?

**가장 직접적인 인과 비교는 fresh vs resume가 아니라 corrected H-005 R02 vs corrected H-001 unchanged control이다.** 두 Run은 metadata상 같은 부모 checkpoint SHA `5e3a3150...1b8ad82`, seed 42, 4096 env, 동일 PPO/task source, 동일 +1500 iteration이며 실제 reward source diff는 `feet_air_time 0.20 → 0.25` 한 줄뿐이다. 현재 첨부에는 부모 archive 자체가 없어서 부모 checkpoint 바이트를 다시 해시하지는 못했지만, 두 child metadata가 같은 source SHA를 기록한다.

이 matched sibling 비교의 late-500 재계산 결과는 다음과 같다.

- XY error: `0.36951 → 0.36093` (**-0.00859, 약 -2.3%**, H-005 개선 방향)
- yaw error: `1.04546 → 1.04095` (**-0.00451, 약 -0.4%**, 거의 동률에 가까운 개선 방향)
- terrain: `5.50101 → 5.47757` (**-0.02345**, 소폭 악화)
- training base-contact: `29.616% → 29.761%` (**+0.145 %p**, 소폭 악화)
- episode length: `777.66 → 773.75` (**-3.90**, 소폭 악화)

late-300에서도 XY와 yaw 개선 방향은 유지되지만 terrain·base-contact·episode length의 작은 열세도 유지된다. 따라서 현재 자료가 지지하는 해석은 **`feet_air_time 0.25`가 tracking을 조금 개선할 가능성과 terrain/survival을 아주 조금 희생하는 trade-off**이지, 전반적인 우월성이나 안정성 향상이 아니다.

fresh H-005와 corrected H-005 resume는 reward가 같지만 fresh/resume, 초기 정책, curriculum 이력이 다르므로 둘의 차이는 **학습 방식·계보 차이와 reward 효과가 섞인 완성 정책 비교**다. fresh late-500은 resume보다 terrain과 yaw가 약간 좋고 XY와 base-contact가 약간 나쁘다. 이 차이를 `feet_air_time=0.25`의 효과라고 부를 수 없다.

### 질문 3 — 현재 자료에서 내려야 할 결정과 가장 먼저 해결할 불확실성은?

- **실행:** 세 학습 Run 모두 `COMPLETE`, exit code 0, evidence validation `PASS`.
- **H-005 reward 가설:** **PROMOTE — 단, fixed paired evaluation 단계까지**. 채택이나 OFFICIAL 우월성으로 승격하지 않는다.
- **현재 fresh 3K 정책:** **HOLD for adoption**. 학습·영상 sanity는 통과했지만 command-fixed 정량 비교가 없다.
- **현재 가장 큰 불확실성:** 작은 tracking 이득이 실제 동일 command/terrain/seed 평가에서 유지되는지, 그리고 그 대가가 fall/stall/terrain progress 악화인지 여부.

가장 정보가 큰 다음 행동은 새 학습이 아니라 **이미 있는 세 checkpoint를 같은 fixed evaluator에서 평가하는 것**이다. 우선 `control model_2998`, `H-005 R02 model_2998`, `fresh H-005 model_2750`을 동일 command/terrain/seed/window에서 x/y/yaw tracking, 실제 진행·stall, fall/base-contact, hip/torso raw posture로 비교한다. 이 결과가 reward 가설과 현재 정책 선택을 동시에 가장 크게 바꿀 수 있다.

---

## 2. 실제 Run → 설정 → checkpoint → 영상 identity

### 2.1 학습 Run identity

| 역할 | archive | mode | fresh/resume | seed / env | 학습 구간 | 종료 | validation |
|---|---|---|---|---|---|---|---|
| C: unchanged control | `20260925-064143-h1-h001-corrected-control-to3k-h1-corrected-2026.tar.gz` | PERSONAL | resume | 42 / 4096 | global 1499→2998, +1500 | COMPLETE / exit 0 | PASS |
| B: corrected H-005 R02 | `20260925-071158-h1-h005-r02-gait025-corrected-h1-corrected-20260.tar.gz` | PERSONAL | resume | 42 / 4096 | global 1499→2998, +1500 | COMPLETE / exit 0 | PASS |
| A: H-005 fresh3k R01 | `20260927-032343-h1-h005-fresh3k-r01-20260927.tar.gz` | PERSONAL | fresh | resolved config seed 42 / 4096 | global 0→2999, 3000 | COMPLETE / exit 0 | PASS |

Fresh command에는 `--seed`가 명시되지 않았지만, 실제 저장된 `native_run/params/agent.yaml`과 `env.yaml`은 seed `42`를 기록한다. 따라서 실행 사실은 resolved config를 기준으로 한다.

### 2.2 부모 계보

Control과 corrected H-005 R02는 둘 다 다음 source를 기록한다.

- parent run id: `NCRC_BATCH_h1-corrected-20260925-03_h001_corrected_1499`
- source checkpoint: `model_1499.pt`
- recorded source SHA-256: `5e3a31502d229884f91faf38962ffd32d63db69a64ca46ed7c1c404671b8ad82`
- start iteration: `1499`

두 child의 `source_provenance_verified=false`는 그대로 유지한다. 이번 첨부 세트에는 parent archive가 없으므로 **“metadata상 같은 부모 SHA”는 확인했지만 parent 바이트를 이번 분석에서 독립 재해시한 것은 아니다.** 프로젝트 핵심팩 `14_H1_NEXT_RUN_PARAMETER_COMPARISON.md`와 `16_EXPERIMENT_EXPORT_AND_TENSORBOARD...md`도 이 corrected parent를 같은 SHA로 기록한다.

Fresh H-005는 `resume=false`, parent/source checkpoint가 없다.

### 2.3 실제 reward 설정

학생 변경 대상 9개 중 control과 corrected H-005의 실제 source diff는 한 줄이다.

| reward | control | corrected H-005 R02 | fresh H-005 |
|---|---:|---:|---:|
| `track_lin_vel_xy_exp` | 0.5 | 0.5 | 0.5 |
| `track_ang_vel_z_exp` | 0.5 | 0.5 | 0.5 |
| `feet_air_time` | **0.20** | **0.25** | **0.25** |
| `termination_penalty` | -50.0 | -50.0 | -50 (동일 의미) |
| `flat_orientation_l2` | -1.5 | -1.5 | -1.5 |
| `ang_vel_xy_l2` | -0.05 | -0.05 | -0.05 |
| `joint_deviation_hip` | -0.2 | -0.2 | -0.2 |
| `joint_deviation_torso` | -0.1 | -0.1 | -0.1 |
| `action_rate_l2` | -0.0005 | -0.0005 | -0.0005 |

Control↔corrected H-005의 `humanoid_rewards.py` unified diff는 `feet_air_time 0.2 → 0.25`만 존재했다. H-005 resume↔fresh의 source hash 차이는 `termination_penalty -50.0`과 `-50`의 표기 차이이며 의미상 동일하다. 그 외 task Python source hash는 동일하다.

### 2.4 PPO / environment 차이

Control과 corrected H-005 R02는 `agent.yaml` diff가 없고, `env.yaml`은 log directory와 feet weight만 다르다.

공통 주요 설정:

- PPO / OnPolicyRunner
- actor·critic hidden dims `512→256→128`, ELU
- `num_steps_per_env=24`
- `check_for_nan=true`
- seed 42
- 4096 env
- episode 20 s
- decimation 4
- `max_init_terrain_level=5`
- curriculum enabled

Fresh H-005는 같은 PPO/source를 사용하지만 `resume=false`, `max_iterations=3000`, `save_interval=50`이다. resume pair는 `save_interval=100`이다. save interval은 학습 동역학 자체보다 checkpoint 저장 빈도 차이다.

### 2.5 checkpoint와 영상 연결

| 정책 | 학습 checkpoint | checkpoint SHA-256 | video bundle | 연결 상태 |
|---|---|---|---|---|
| control | final `model_2998.pt` | `fc3c60cdff61c43baf1350aa89f22ac907089aab3d1fb28e60b14aa19778556a` | `checkpoint-h1-model_2998-fc3c60cdff61-download.tar.gz` | **manifest ↔ archive byte SHA exact match** |
| H-005 R02 | final `model_2998.pt` | `9454afa964bb4dd7168dba1dfbef2d0acd1aaafa11d02026550cfdb5d6a485cc` | `checkpoint-h1-model_2998-9454afa964bb-download.tar.gz` | **exact match** |
| fresh H-005 | auto best `model_2750.pt` | `6d7d0ecb13c70730087d43a82f88f6386f1af8b5721ab0b13e32e110a43c29eb` | `checkpoint-h1-model_2750-6d7d0ecb13c7-download.tar.gz` | **exact match** |
| fresh H-005 | final `model_2999.pt` | `ff51151a037d25396f03c5032c1484f828c741a6dd54a3ac8713904d7cee25a2` | 없음 | 행동 미확인 |

각 video bundle의 6개 MP4도 manifest 기록 SHA와 실제 추출 파일 SHA를 모두 대조했고 18/18 일치했다.

중요한 provenance 함정도 확인했다. control과 corrected H-005 train archive의 `collected/provenance.json`에서 기존 `policy.pt`와 `play_video.mp4`는 `UNCHANGED`다. 따라서 이를 이번 child의 새 export/영상으로 사용하지 않았다. 이번 행동 근거는 별도 video suite manifest와 checkpoint SHA가 연결된 6지형 bundle만 사용한다.

---

## 3. 무엇을 비교할 수 있는가

| 질문 | 비교 | 판정 | 이유 |
|---|---|---|---|
| `feet_air_time 0.20→0.25`의 training 효과 | control vs corrected H-005 R02 | **직접 비교에 가장 적합** | 같은 recorded parent SHA, seed, env, source/PPO, +1500 iter, 단일 reward diff |
| `feet=0.25` 완성 정책의 fresh vs resume 차이 | fresh H-005 vs corrected H-005 R02 | **조건부 비교** | reward는 같지만 초기 정책·curriculum trajectory가 다름 |
| 세 정책의 실제 행동 형태 | 각 manifest-linked 6지형 영상 | **맥락 참고 / 정성 비교** | checkpoint identity는 강하지만 command/terrain seed/difficulty가 matched 아님 |
| 공식 성능 / 제출 우열 | 어느 조합도 불가 | **판단 불가** | 모두 PERSONAL, 공식 evaluator 결과 없음 |
| 영상만으로 tracking score / fall rate | 어느 조합도 불가 | **판단 불가** | numeric command와 반복 episode 집계 없음 |

같은 seed 42는 동일 terrain realization이나 동일 episode를 보장하는 근거로 사용하지 않는다. 특히 정책이 달라지면 reset 시점 자체가 달라질 수 있다.

---

## 4. TensorBoard 원시 시계열 재분석 방법

세 archive의 `native_run/events.out.tfevents*`를 raw TFRecord protobuf로 직접 파싱했다.

- control: 핵심 iteration scalar 각 1500점, step `1499..2998`
- corrected H-005 R02: 각 1500점, step `1499..2998`
- fresh H-005: 각 3000점, step `0..2999`
- `Curriculum/*`, `Metrics/*`, `Episode_*`, `Loss/*`, `Policy/*`, `Train/mean_reward`, `Train/mean_episode_length`에는 **global iteration 중복 step 없음**
- `/time` 파생 tag는 wall-time 축 특성상 duplicate step이 있어 분석에서 제외

후반 비교 window는 기존 프로젝트의 corrected-lineage 비교 정의와 맞춰 **late-500**을 주 기준으로 사용했다. 작은 차이에 대한 경계 민감성을 보기 위해 **late-300**을 인접 sensitivity window로 추가했다. 단일 seed의 연속 300/500점을 독립 샘플로 취급하지 않았고 p-value/CI를 만들지 않았다.

기존 `14_H1_NEXT_RUN_PARAMETER_COMPARISON.md`의 corrected H-005 last-500 값과 이번 raw 재계산은 소수점 반올림 수준에서 일치했다. 이번 보고서의 수치는 기존 요약 복사가 아니라 raw event에서 재계산했다.

---

## 5. 학습 경과 — 같은 기준 수치 비교

### 5.1 reward 인과 질문: corrected H-005 R02 vs unchanged control

#### late-500 (`2499..2998`)

| 지표 | control | H-005 R02 | H-005 - control | 해석 |
|---|---:|---:|---:|---|
| terrain level | 5.50101 | 5.47757 | **-0.02345** | 소폭 악화 |
| XY error | 0.36951 | 0.36093 | **-0.00859** | 개선 방향 |
| yaw error | 1.04546 | 1.04095 | **-0.00451** | 거의 동률, 개선 방향 |
| base-contact termination | 29.616% | 29.761% | **+0.145 %p** | 소폭 악화 |
| timeout | 70.399% | 70.246% | -0.153 %p | base-contact와 상보적 방향 |
| episode length | 777.66 | 773.75 | **-3.90** | 소폭 악화 |
| flat-orientation weighted term | -0.010780 | -0.011062 | -0.000282 | 약간 더 큰 자세 비용 |
| hip-deviation weighted term | -0.035084 | -0.034591 | +0.000493 | 약간 덜 큰 비용 |
| torso-deviation weighted term | -0.006935 | -0.005865 | +0.001069 | 약간 덜 큰 비용 |
| action-rate weighted term | -0.063100 | -0.062441 | +0.000659 | 약간 덜 큰 비용 |
| feet-slide weighted term | -0.045865 | -0.046535 | -0.000670 | 약간 더 큰 비용 |
| `feet_air_time` weighted term | 0.008923 | 0.012310 | +0.003387 | weight 자체가 달라 raw behavior 역산 금지 |
| policy mean std | 1.34320 | 1.34187 | -0.00134 | 사실상 비슷 |
| value loss | 0.004946 | 0.004975 | +0.000029 | 수치 안정성 차이 없음 |
| mean reward | 2.69635 | 2.82486 | +0.12851 | reward weight가 달라 성능 우열 지표로 사용 금지 |

`feet_air_time` term은 weight가 0.20과 0.25로 다르므로 weighted term 차이를 weight로 나눠 실제 비가중 air-time 행동량으로 복원하지 않았다. term의 normalization/aggregation 정의를 이번 원본 세트에서 충분히 검증하지 않았기 때문이다.

#### late-300 (`2699..2998`) sensitivity

| 지표 | control | H-005 R02 | 차이 |
|---|---:|---:|---:|
| terrain | 5.52186 | 5.47531 | -0.04656 |
| XY error | 0.36888 | 0.35846 | **-0.01042** |
| yaw error | 1.04070 | 1.02526 | **-0.01544** |
| base-contact | 29.794% | 29.938% | **+0.144 %p** |
| episode length | 777.91 | 771.89 | -6.02 |

경계를 500→300으로 바꿔도 **tracking 개선 방향과 terrain/contact의 작은 손실 방향은 뒤집히지 않는다.** 따라서 “작은 tracking-vs-stability trade-off”라는 핵심 결론은 window 선택에 비교적 견고하다. 단, 효과 크기는 크지 않다.

### 5.2 학습 phase

#### control

- early-300 `1499..1798`: terrain 4.520, XY 0.3526, yaw 1.1185, base-contact 26.14%, episode length 736.8
- mid-500 `1999..2498`: terrain 5.359, XY 0.3756, yaw 1.0971, base-contact 30.15%, episode length 773.9
- late-500: terrain 5.501, XY 0.3695, yaw 1.0455, base-contact 29.62%, episode length 777.7

#### corrected H-005 R02

- early-300: terrain 4.511, XY 0.3506, yaw 1.1188, base-contact 26.01%, episode length 735.8
- mid-500: terrain 5.393, XY 0.3717, yaw 1.0878, base-contact 29.86%, episode length 776.5
- late-500: terrain 5.478, XY 0.3609, yaw 1.0410, base-contact 29.76%, episode length 773.8

두 sibling은 resume 직후 매우 비슷하게 시작하고 중후반에 작은 차이가 누적된다. H-005가 early phase부터 극적으로 바뀐 것은 아니며, late tracking 이득도 큰 분리라기보다 미세한 방향성이다.

### 5.3 fresh H-005의 독립 학습 경과

| window | terrain | XY | yaw | base-contact | episode length |
|---|---:|---:|---:|---:|---:|
| 0..499 | 0.902 | 0.3830 | 1.1391 | 68.80% | 470.8 |
| 1000..1499 | 5.078 | 0.3904 | 1.3058 | 30.94% | 768.0 |
| 2000..2499 | 5.432 | 0.3718 | 1.0503 | 30.10% | 771.7 |
| 2500..2999 | 5.504 | 0.3736 | 1.0269 | 29.94% | 775.8 |

Fresh run은 처음 500회에서 높은 base-contact와 낮은 terrain을 보인 뒤 1K 이후 회복했고, 2K 이후 terrain과 yaw가 안정화된다. 이는 **fresh 3K까지 충분히 학습 진행이 필요했다**는 사실을 보여주며, resume child와 global iteration 숫자만 맞춰 초반 성능을 비교하면 안 된다.

### 5.4 fresh H-005 vs corrected H-005 resume — 완성 정책 관찰, 인과 아님

late-500 기준:

| 지표 | H-005 resume | H-005 fresh | fresh - resume |
|---|---:|---:|---:|
| terrain | 5.47757 | 5.50379 | +0.02623 |
| XY error | 0.36093 | 0.37355 | +0.01263 (fresh 열세) |
| yaw error | 1.04095 | 1.02692 | -0.01403 (fresh 우세) |
| base-contact | 29.761% | 29.935% | +0.174 %p (fresh 열세) |
| episode length | 773.75 | 775.83 | +2.07 |
| flat-orientation term | -0.01106 | -0.01270 | fresh 비용 증가 |
| feet-slide term | -0.04654 | -0.04199 | fresh 비용 감소 |

즉 fresh는 terrain/yaw/feet-slide 쪽과 XY/base-contact/posture 쪽이 엇갈린다. **동일 reward라고 해서 fresh가 resume보다 일관되게 우수하다는 신호는 없다.** 이 비교는 계보 효과를 포함하므로 reward 최적값 판단에 쓰지 않는다.

### 5.5 최적화 안정성

세 Run 모두 핵심 scalar에서 NaN/Inf가 보이지 않고 value loss는 late window에서 약 `0.005` 수준이다. policy mean std도 late에 `1.34` 전후로 비슷하다. 학습이 수치적으로 발산해 정책 차이를 설명해야 할 증거는 없다.

따라서 현재 주요 차이는 optimizer failure가 아니라 **정상 학습 범위 안에서 나타난 작은 behavioral trade-off**로 보는 편이 더 타당하다.

---

## 6. 6지형 영상 비교

### 6.1 영상 분석 범위와 제한

모든 MP4는 H.264, 1920×1080, 50 fps, 999 frames, 19.98 s로 확인했다.

이 환경에서는 영상을 인간처럼 연속 재생해 실시간 주기 분석하지 않고, 다음 정지 프레임 시퀀스를 추출해 조사했다.

- 전 구간: `0, 2, 4, ..., 18 s` — 2초 간격
- 장애물 접촉이 집중된 구간: `8..15 s` — 1초 간격 center crop
- boxes/stairs 일부는 추가 0.5초 간격 strip으로 재확인

따라서 아래 관찰은 **접근·접촉·진행·낙상 여부의 sampled-frame 근거**다. 보행 주기, 미세 진동 주파수, 순간 slip, 짧은 recovery를 연속 관찰했다고 주장하지 않는다.

또한 video suite manifest에는 numeric command, terrain seed, difficulty, 초기 상태가 없다. 장면 이름이 같아도 세 정책이 같은 episode를 재생한 paired video라고 가정하지 않는다.

### 6.2 지형별 관찰

| terrain | control `model_2998` | H-005 R02 `model_2998` | fresh H-005 `model_2750` | 공통/한계 |
|---|---|---|---|---|
| stairs | 약 12~15 s에 계단 접근·진입. sampled frame에서 upright 유지 | 비슷한 시점에 계단 진입, upright | 비슷한 시점에 계단 진입, upright | 세 정책 모두 계단 접촉 후 즉시 붕괴하는 모습 없음. 실제 상승 단수·command 일치 미측정 |
| inverted stairs | 8~12 s에 단차 구간에서 이동, 12~15 s 이후 벗어나는 장면 | 단차를 지나며 upright | 단차 구간을 지나며 upright | 명확한 prone/fall 없음. 연속 foot-slip은 판단 불가 |
| boxes | 8~13 s 사이 불규칙 block 사이 진행, 약 14~16 s에는 patch 밖으로 나온 장면 | 8~15 s에도 block 구간 안에서 계속 진행, upright | 8~15 s block 사이 진행, upright | control이 더 빨리 patch를 벗어난 듯 보이지만 command/seed가 matched 아님. 속도 우열로 사용 금지 |
| random rough | 8~15 s 거친 patch를 통과해 edge 방향으로 진행, 16~18 s에는 patch 밖 장면 | rough에서 계속 전진, 후반 edge/out 장면 | rough에서 계속 전진, 후반 edge/out 장면 | 세 정책 모두 sampled frame에서 stall/prone 없음. 미세 흔들림 비교 불가 |
| slope up 10deg | 0~18 s upright locomotion, 큰 자세 붕괴 없음 | 동일 | 동일 | 영상의 실제 진행 방향/command 수치 미상. 10° label은 manifest 이름 기준 |
| slope down 10deg | 0~18 s upright locomotion, 큰 자세 붕괴 없음 | 동일 | 동일 | short clip 무낙상은 낮은 fall rate 증거가 아님 |

### 6.3 영상과 수치의 일치/충돌

- TensorBoard late base-contact가 약 29~30%라고 해서 영상에서 20초 내내 30% 확률로 넘어져야 하는 것은 아니다. 이는 training episode termination 집계이며 영상은 단일 native-play trajectory다.
- 세 정책의 영상에서 sampled frame 기준 명백한 prone/fall이 보이지 않는 것은 **“학습 scalar가 완전히 무너진 정책이 아니다”라는 sanity check**와는 일치한다.
- 반면 control boxes가 더 빠르게 patch를 벗어난 듯 보이는 장면은 H-005의 낮은 XY error와 충돌하는 성능 지표로 쓰지 않는다. command·seed·difficulty가 다를 수 있기 때문이다.
- fresh H-005의 late training terrain이 가장 높지만, 영상만으로 세 정책 중 지형 통과율이 가장 높다고 말할 수 없다.

---

## 7. 핵심 발견별 해석, 경쟁 설명, 반대 근거

### 발견 A — `feet_air_time 0.25`는 XY tracking을 작게 개선하는 방향

**관찰**\
Matched sibling late-500 XY error가 `0.36951 → 0.36093`, late-300은 `0.36888 → 0.35846`이다.

**해석**\
조금 더 높은 air-time 보상은 보폭/foot clearance를 키워 commanded planar velocity를 따라가기 쉽게 만들었을 가능성이 있다.

**경쟁 설명**\
단일 seed이고 policy-dependent reset/curriculum이 있으므로, 같은 parent라도 이후 episode realization 차이가 일부 기여할 수 있다.

**반대 근거**\
terrain은 소폭 낮아지고 base-contact와 episode length는 소폭 나빠졌다. 따라서 “tracking 개선 = 전반적 locomotion 개선”은 아니다.

**판별 방법**\
동일 command/terrain/seed fixed evaluator에서 x/y tracking과 실제 displacement, stall, fall을 동시에 본다.

### 발견 B — yaw 이득은 약하지만 late-300에서 더 선명해진다

**관찰**\
late-500 yaw 차이는 -0.0045로 거의 동률이지만 late-300은 -0.0154이다.

**해석**\
후반에 gait가 안정되며 yaw trade-off가 완화됐을 가능성이 있다.

**경쟁 설명**\
window sensitivity 또는 curriculum composition 변화일 수 있다.

**반대 근거**\
효과 크기가 작고 fixed yaw command evaluation이 없다.

**판별 방법**\
전진/측면/회전 명령을 분리한 fixed scenario에서 body-frame x/y/yaw error를 각각 기록한다.

### 발견 C — stability는 개선되지 않았다

**관찰**\
H-005 late-500 base-contact가 control보다 +0.145 %p, episode length가 -3.9이며 terrain도 -0.023 낮다.

**해석**\
조금 더 적극적인 foot airtime이 tracking에는 유리하지만 일부 지형에서 접촉 안정 margin을 줄였을 가능성이 있다.

**경쟁 설명**\
차이가 작기 때문에 단일 seed의 curriculum composition 차이일 수도 있다.

**반대 근거**\
영상 sampled frames에서는 여섯 지형 모두 즉시 붕괴하는 행동이 없고, H-005 posture/action weighted terms 일부는 오히려 control보다 덜 불리하다.

**판별 방법**\
낙상률만 보지 말고 실제 terrain progress와 stall을 함께 평가한다.

### 발견 D — fresh 3K는 “같은 reward의 더 좋은 버전”으로 단정할 수 없다

**관찰**\
Fresh late-500은 resume보다 yaw/terrain은 약간 좋지만 XY/base-contact/flat-orientation은 약간 나쁘다.

**해석**\
초기화와 curriculum trajectory가 서로 다른 local optimum으로 수렴했을 가능성이 있다.

**경쟁 설명**\
같은 seed라도 fresh/resume은 시작 정책이 다르므로 episode sequence 자체가 다르다.

**반대 근거**\
양쪽 모두 late terrain ~5.5, std ~1.34, value loss ~0.005로 전체적인 학습 품질은 비슷하다.

**판별 방법**\
동일 evaluator에서 직접 완성 정책을 비교한다. 이 비교 결과를 reward 인과 효과로 다시 해석하지 않는다.

---

## 8. checkpoint 판단

### 8.1 corrected control / H-005 R02 resume

- control auto `model_best.pt` = `model_2900.pt`
  - raw reward max: step 2878, 3.6621
- H-005 R02 auto `model_best.pt` = `model_2900.pt`
  - raw reward max: step 2932, 3.6812
- final numbered = 둘 다 `model_2998.pt`
- 영상 source = 둘 다 final `model_2998.pt`

프로젝트 운영 원칙대로 충분히 진행한 resume branch는 final numbered를 기본 대표로 본다. 실제로 2900 이후에도 H-005는 terrain·tracking·contact가 함께 붕괴하지 않는다. `2900..2998` 평균은 terrain 5.494, XY 0.3586, yaw 1.0194, base-contact 29.79%로 joint collapse가 없다. 따라서 **control/H-005 R02는 final `model_2998`을 대표 checkpoint로 유지**하는 것이 타당하다.

### 8.2 fresh H-005

- auto `model_best.pt` = `model_2750.pt`
- raw mean reward peak = step 2747, 3.7181
- final = `model_2999.pt`
- 6지형 영상 source = `model_2750.pt`

`2600..2799` vs `2800..2999`을 보면 후반에 terrain `5.479→5.536`, base-contact `30.11%→29.39%`, episode length `775.3→782.4`로 개선되고 yaw는 거의 유지되지만 XY가 `0.3707→0.3778`로 악화된다. **joint late collapse는 없다.**

그러나 fresh run에는 “resume이면 final을 기본 대표로 쓴다”는 운영 규칙을 자동 적용하지 않는다. 현재 실제 행동 증거가 연결된 checkpoint는 `model_2750`뿐이다. 따라서:

- **행동상 현재 확인된 fresh 후보:** `model_2750`
- **final `model_2999`:** scalar상 배제할 이유는 없지만 행동 미확인

이번 분석에서 `model_2999`를 새 대표로 바꾸거나 checkpoint tournament를 만들지 않는다.

---

## 9. 현재 프로젝트 판단

### 실행

- control: **COMPLETE / PASS**
- corrected H-005 R02: **COMPLETE / PASS**
- fresh H-005 R01: **COMPLETE / PASS**

실행 완료와 정책 우수성은 별개다.

### evidence와 비교

- train→checkpoint identity: 확인
- final resume checkpoint→6지형 영상 identity: SHA로 확인
- fresh auto-best→6지형 영상 identity: SHA로 확인
- MP4 18개 manifest hash: 확인
- TensorBoard raw scalar: 직접 파싱 및 재집계
- same-parent parent bytes: **이번 첨부 세트에서는 미재검증**, child metadata와 기존 프로젝트 기록으로만 연결
- fixed evaluator: 없음
- OFFICIAL score: 없음

### 가설 H-005 (`feet_air_time 0.20→0.25`)

**PROMOTE — fixed paired evaluation 단계까지만.**

근거는 matched sibling에서 window에 견고한 작은 XY 개선과 약한 yaw 개선 방향이다. 그러나 terrain/base-contact/episode length가 함께 아주 조금 악화되어 채택 근거가 아니다. 기존 프로젝트 핵심팩의 “작은 XY 이득으로 추가 확인 후보” 판단을 raw event와 현재 final 영상 identity 재검증이 지지한다.

### 정책

**현재 fresh H-005 policy: HOLD for adoption.**

장점:

- fresh 3K가 초반 붕괴를 지나 terrain ~5.5 수준으로 회복
- 6지형 sampled frames에서 upright locomotion과 실제 obstacle engagement 확인
- 수치 발산/NaN 증거 없음

약점/미확인:

- fixed command tracking 성능 없음
- fall/stall/traversal 반복률 없음
- fresh model_2750 vs final model_2999 행동 비교 없음
- resume H-005보다 XY가 late training에서 약간 나쁨
- 모든 자료가 PERSONAL

---

## 10. 다음 한 번의 행동

### 1순위 — 새 학습 없이 fixed paired evaluator

다음 세 **이미 보존된 checkpoint**를 한 evaluator version에 넣는다.

1. corrected control final `model_2998` — SHA `fc3c60cd...78556a`
2. corrected H-005 R02 final `model_2998` — SHA `9454af...a485cc`
3. fresh H-005 current behavior candidate `model_2750` — SHA `6d7d0e...c29eb`

맞출 조건:

- 동일 terrain set / difficulty
- 동일 command sequence 또는 명시된 command set
- 동일 seed set과 reset 정책
- 동일 evaluation horizon
- curriculum off 또는 evaluator 규칙으로 고정
- 동일 observation/task source

최소 측정:

- body-frame x/y/yaw tracking error
- 실제 forward/lateral displacement 또는 terrain progress
- stall time
- fall/base-contact termination
- episode survival
- hip/torso raw posture deviation
- 가능하면 foot contact/slide 보조 지표

**왜 이것이 가장 정보가 큰가:** 현재 결정은 2~3% 수준의 tracking 이득과 0.1%p 수준의 contact 차이가 실제 행동 성능인지 구분하는 데 달려 있다. 새 학습을 더 돌려도 evaluator가 없으면 같은 불확실성이 남는다.

결과별 결정:

- H-005 R02가 control보다 tracking이 반복적으로 좋아지고 fall/stall/progress 손실이 없으면 → H-005 reward 가설을 다음 장기/공식 검토 단계로 유지.
- tracking 이득이 사라지거나 terrain/fall 손실이 확인되면 → H-005를 HOLD 또는 REJECT로 내리고 `0.20` control 유지.
- fresh가 resume와 크게 다르면 → 그 차이는 reward 효과가 아니라 training lineage/initialization 영향으로 분리하고, fresh 자체 정책 선택 질문으로 다룬다.

### 2순위는 현재 불필요

우선순위 1의 fixed evaluator가 없으면 새 3K/5K 학습을 추가해도 이번 핵심 의사결정의 불확실성을 직접 줄이지 못한다. 따라서 지금은 새 GPU 학습을 먼저 추천하지 않는다.

---

## 11. 한계

1. 모든 학습은 PERSONAL이며 OFFICIAL 제출 성능이 아니다.
2. 단일 seed 결과다. TensorBoard 500점은 독립 seed 500개가 아니다.
3. same-parent source SHA는 child metadata와 기존 프로젝트 기록으로 연결했지만 이번 입력에는 parent archive 바이트가 없어 재해시하지 않았다.
4. 6지형 영상은 checkpoint identity는 강하게 확인했지만 numeric command, terrain seed, difficulty, 초기 상태가 manifest에 없다.
5. 영상은 정지 프레임 시퀀스로 판독했으므로 gait cycle, 고주파 jitter, 짧은 slip/recovery를 연속 관찰한 것으로 해석하면 안 된다.
6. training `base_contact`를 fixed evaluator 낙상률로 부르지 않았다.
7. `Curriculum/terrain_levels`를 특정 난이도 통과율로 사용하지 않았다.
8. reward weight가 달라진 `feet_air_time` weighted term과 total mean reward를 직접 성능 척도로 쓰지 않았다.
9. fresh `model_2999`의 행동은 미확인이다.

---

## 12. 재확인 가능한 근거 목록

### Control train

`20260925-064143-h1-h001-corrected-control-to3k-h1-corrected-2026.tar.gz`

- `metadata.json`
- `validation.json`
- `source/humanoid_rewards.py`
- `source/identity.json`
- `native_run/params/agent.yaml`
- `native_run/params/env.yaml`
- `native_run/events.out.tfevents.1790318521.brev-p049cuh9h.49041.0`
- `checkpoints/model_2998.pt`
- `collected/provenance.json`

### Corrected H-005 R02 train

`20260925-071158-h1-h005-r02-gait025-corrected-h1-corrected-20260.tar.gz`

- 동일 구조
- final `model_2998.pt` SHA `9454afa9...a485cc`
- auto best `model_2900.pt`

### Fresh H-005 train

`20260927-032343-h1-h005-fresh3k-r01-20260927.tar.gz`

- final `model_2999.pt` SHA `ff51151a...e25a2`
- auto best / video source `model_2750.pt` SHA `6d7d0ecb...c29eb`
- raw event step `0..2999`

### Video suites

- `checkpoint-h1-model_2998-fc3c60cdff61-download.tar.gz` — control final
- `checkpoint-h1-model_2998-9454afa964bb-download.tar.gz` — corrected H-005 R02 final
- `checkpoint-h1-model_2750-6d7d0ecb13c7-download.tar.gz` — fresh H-005 auto best

각 bundle의 `video_suite_manifest.json`과 `SHA256SUMS`를 확인했으며, 6개 MP4의 hash가 모두 일치했다.

### 프로젝트 기준 문서와의 교차검증

- `14_H1_NEXT_RUN_PARAMETER_COMPARISON.md` — corrected H-001/H-005 late-500 및 비교 경계
- `16_EXPERIMENT_EXPORT_AND_TENSORBOARD(20260926-030938).md` — final numbered resume 대표 원칙, video qualitative 경계
- `18_H1_FINALIZE_REPORT_LIMITATIONS(20260926-030939).md` — automatic best와 final checkpoint 구분
- `00_START_HERE_CONTEXT_AND_MAP(20260926-030939).md` — corrected lineage의 현재 registry 요약

이번 raw 재계산은 이 문서의 corrected H-005 last-500 값과 일치하며, 새 fresh3K 자료는 2026-09-26 핵심팩 이후 생성된 것이므로 이번 보고서에서 별도로 직접 분석했다.

---

## 최종 한 줄 결정

**`feet_air_time 0.25`는 corrected matched sibling에서 작은 tracking 이득과 작은 terrain/contact 비용이 함께 보여 “fixed paired evaluator로 PROMOTE”할 근거는 있지만 채택 근거는 아니다. 최신 fresh 3K `model_2750`은 6지형에서 정상 locomotion sanity를 보였으나, 현재 가장 먼저 필요한 것은 새 학습이 아니라 동일 evaluator에서 control/H-005 resume/fresh를 같은 조건으로 재는 것이다.**
