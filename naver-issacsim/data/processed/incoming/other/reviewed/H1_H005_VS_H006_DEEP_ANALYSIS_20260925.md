# H1 H-005 vs H-006 심층 분석 — corrected H-001 control 포함

- 작성일: 2026-09-25
- 분석 대상 로봇: H1 / `Humanoid-v0`
- A: H-005 corrected rerun (`feet_air_time=0.25`)
- B: H-006 corrected rerun (`feet_air_time=0.30`)
- 직접 대조군: corrected H-001 unchanged continuation (`feet_air_time=0.20`)
- 환경 분류: 세 Run 모두 **PERSONAL**
- 분석 범위: 제공된 3개 통합 학습 archive + 각 final `model_2998.pt`의 6지형 영상 묶음
- 주의: 이 보고서는 PERSONAL 상대 비교이며 OFFICIAL 성능·공식 점수의 증거가 아니다.

---

## 1. 결론 요약

이번 자료는 과거 H-005/H-006의 잘못된 `feet_air_time=-0.2` 부모 계보 문제를 바로잡기 위해 계획되어 있던 **corrected +0.2 parent 기반의 unchanged control / +0.25 / +0.30 sibling 비교**에 해당한다. 세 child archive의 metadata가 동일한 parent checkpoint SHA-256 `5e3a3150…ad82`를 기록하고, 세 run의 `agent.yaml`은 byte-identical이며, `env.yaml` 차이는 run-specific `log_dir`를 제외하면 `feet_air_time` weight 하나뿐이다. 따라서 **이 corrected sibling 세트 안에서는 `feet_air_time` 변경과 관찰된 차이를 연결해 해석할 수 있는 직접 비교에 적합**하다. 다만 parent 원본 archive 자체는 이번 입력에 없고 metadata의 `source_provenance_verified=false`이므로, 부모 바이트까지 독립 대조했다고 쓰지는 않는다.

핵심 결과는 다음과 같다.

1. **H-005 (`0.25`)**는 후반 500 iteration에서 control 대비 XY tracking error가 `0.3695 → 0.3609`로 `-0.0086` 개선되었다. yaw error도 `1.0455 → 1.0410`으로 거의 동일하거나 미세 개선이었다. 반면 terrain은 `5.5010 → 5.4776`으로 거의 같거나 약간 낮고, base-contact termination share는 `29.616% → 29.761%`로 `+0.145%p` 높아졌다. 즉 **작은 tracking 이득은 보이지만 안정성/terrain 이득은 확인되지 않았다.** 인접 late-300/late-750 window에서도 XY 개선 방향은 유지되어 window 선택만의 산물일 가능성은 낮다.
2. **H-006 (`0.30`)**은 terrain이 `5.5010 → 5.5595`로 `+0.0585` 높았지만, XY error는 `0.3695 → 0.3774`로 `+0.0079` 악화되고 base-contact termination share도 `29.616% → 30.047%`로 `+0.431%p` 높았다. yaw는 거의 동률이다. 즉 **조금 더 높은 curriculum terrain과 조금 나쁜 linear tracking/termination의 trade-off**가 관찰된다. `Train/mean_reward`가 더 높다는 사실은 reward weight 자체가 달라 직접 성능 척도로 쓰지 않는다.
3. 여섯 19.98초 영상은 세 정책 모두 **final numbered `model_2998.pt` SHA와 manifest가 정확히 연결**되며 stale `model_best` 영상이 아니다. sampled-frame 관찰에서는 계단·박스·rough·±10° slope에서 세 정책 모두 upright progression이 보이고 명백한 낙상은 보이지 않았다. 특히 `0.30`에서 우려할 수 있는 지속적인 한발 hop이 sampled frames에서 뚜렷하게 확인되지는 않았다. 그러나 영상 manifest에는 command, seed, difficulty/curriculum level이 없으므로 **영상만으로 어느 정책이 더 빠르거나 명령을 더 정확히 따른다고 판정할 수 없다.**
4. optimization 자체는 세 run 모두 정상이다. exit code 0, evidence validation PASS, 각 TensorBoard 핵심 tag는 global step `1499..2998`에 1500개 고유 값이 있고 reset/duplicate/NaN이 확인되지 않았다. 후반 value/surrogate loss도 안정적이며 세 run 사이에 발산 차이는 없다.

### 현재 결정

- **실행**: H-001 control / H-005 / H-006 모두 **COMPLETE**.
- **evidence**: 세 archive와 세 video bundle의 내부 `SHA256SUMS` 검증 통과. final checkpoint↔video manifest SHA 연결도 통과.
- **H-005 가설**: **PROMOTE — 단, “채택”이 아니라 다음 장시간 matched confirmation으로 승격.** 이유는 작은 XY 개선이 late-750/500/300에서 같은 방향이고 stability 손실이 크지 않기 때문이다.
- **H-006 가설**: **HOLD.** terrain 소폭 상승은 있으나 XY·base-contact에서 반대 trade-off가 있고 영상에서 이를 상쇄할 명확한 obstacle advantage가 보이지 않았다.
- **대표 checkpoint**: 세 run 모두 `model_2998.pt`를 기본 대표로 유지. control/H-005의 native automatic best는 `model_2900.pt`, H-006은 final `model_2998.pt`지만, 세 run 모두 마지막 수백 iteration에서 terrain·tracking·termination이 함께 붕괴하지 않아 충분히 진행한 resume의 final-numbered 원칙에 어긋날 근거가 없다. 제공된 6지형 영상도 바로 이 final checkpoint를 사용한다.

**다음 한 번의 행동 1순위**는 새 reward를 추가하는 것이 아니라, **H-001 control `model_2998`과 H-005 `model_2998`에서 각각 reward를 그대로 유지한 채 같은 추가 학습량으로 total 5K 수준까지 matched continuation**을 만드는 것이다. 이렇게 해야 0.25의 작은 tracking 이득이 장시간에도 유지되는지, terrain/termination trade-off가 누적되는지를 가장 직접적으로 판별할 수 있다. H-006을 동시에 연장하는 것은 현재 결정 정보량이 낮다.

---

## 2. 실제 Run·checkpoint·영상 identity

### 2.1 학습 archive 연결

| 역할 | Run | child mode | 기록된 parent | parent SHA-256 | 추가 학습 | global range | final checkpoint | 상태 |
|---|---|---|---|---|---:|---|---|---|
| Control | `h1-h001-corrected-control-to3k` | PERSONAL | `NCRC_BATCH_h1-corrected-20260925-03_h001_corrected_1499/model_1499.pt` | `5e3a3150…ad82` | +1500 | 1499→2998 | `model_2998.pt` | completed / validation PASS |
| H-005 | `h1-h005-r02-gait025-corrected` | PERSONAL | 동일 기록 | `5e3a3150…ad82` | +1500 | 1499→2998 | `model_2998.pt` | completed / validation PASS |
| H-006 | `h1-h006-r02-gait030-corrected` | PERSONAL | 동일 기록 | `5e3a3150…ad82` | +1500 | 1499→2998 | `model_2998.pt` | completed / validation PASS |

근거 위치:

- 각 archive `metadata.json`: command, mode, exit/status, `resume_lineage`, source checkpoint SHA, start/final iteration.
- 각 archive `command.txt`: `--max_iterations 1500 --num_envs 4096 --seed 42 --resume ... --checkpoint model_1499.pt --headless`.
- 각 archive `validation.json`: native run / TensorBoard / mirrored checkpoints / source identity / finalize 모두 PASS.
- 각 archive `source/identity.json`: run 전후 source hashes 동일, `changed_during_run=false`.

**계보 한계:** 세 metadata의 source checkpoint SHA와 path는 일치하지만, 이번 입력에 parent checkpoint 원본 archive가 별도 제공되지는 않았다. 또한 `source_provenance_verified=false`다. 따라서 “세 child가 같은 parent를 기록했다”는 것은 직접 확인했지만, “parent 원본 바이트를 이번 분석에서 별도 archive와 대조했다”는 주장은 하지 않는다.

### 2.2 실제 reward 차이

`source/humanoid_rewards.py`와 `native_run/params/env.yaml`을 양쪽 모두 대조했다.

| reward | Control | H-005 | H-006 |
|---|---:|---:|---:|
| `track_lin_vel_xy_exp` | 0.5 | 0.5 | 0.5 |
| `track_ang_vel_z_exp` | 0.5 | 0.5 | 0.5 |
| **`feet_air_time`** | **0.20** | **0.25** | **0.30** |
| `termination_penalty` | -50.0 | -50.0 | -50.0 |
| `flat_orientation_l2` | -1.5 | -1.5 | -1.5 |
| `ang_vel_xy_l2` | -0.05 | -0.05 | -0.05 |
| `joint_deviation_hip` | -0.2 | -0.2 | -0.2 |
| `joint_deviation_torso` | -0.1 | -0.1 | -0.1 |
| `action_rate_l2` | -0.0005 | -0.0005 | -0.0005 |

`env.yaml`의 full diff는 `log_dir`과 `feet_air_time.weight`만 달랐다. `agent.yaml` SHA-256은 세 run 모두 `11cada77…635`로 동일했다. 즉 이번 corrected sibling 세트는 **실제 적용 설정 기준으로 one-variable comparison**이다.

참고로 native report는 baseline default 대비 H-005/H-006에서 `termination -5→-50`도 “변경”으로 표시하지만, 이는 세 sibling 모두에 공통으로 들어 있는 corrected parent/control 설정이다. **이번 세 run 사이의 실험 변수는 `feet_air_time` 하나다.**

### 2.3 automatic best와 final

| Run | raw/report reward peak | automatic `model_best` | final numbered | video source |
|---|---|---|---|---|
| Control | `3.662 @ 2878` | `model_2900.pt` | `model_2998.pt` | `model_2998.pt` |
| H-005 | `3.681 @ 2932` | `model_2900.pt` | `model_2998.pt` | `model_2998.pt` |
| H-006 | `3.835 @ 2966` | `model_2998.pt` | `model_2998.pt` | `model_2998.pt` |

control/H-005의 `model_best.pt` SHA는 각각 보존된 `model_2900.pt`와 일치했고, H-006의 `model_best.pt`는 `model_2998.pt`와 일치했다. 그러나 reward weight가 다르므로 자동 best의 mean reward 크기를 정책 품질 우열로 사용하지 않는다.

### 2.4 영상 provenance

각 video suite의 `video_suite_manifest.json`이 지목한 checkpoint SHA를 학습 archive의 final checkpoint와 직접 대조했다.

| 정책 | final `model_2998.pt` SHA-256 | video manifest checkpoint SHA | 연결 |
|---|---|---|---|
| Control | `fc3c60cdff61…556a` | 동일 | PASS |
| H-005 | `9454afa964bb…85cc` | 동일 | PASS |
| H-006 | `dc1f61e22e7f…b5ff` | 동일 | PASS |

각 묶음은 `stairs`, `inverted_stairs`, `boxes`, `random_rough`, `slope_up_10deg`, `slope_down_10deg` 6개 MP4를 가지며, 전부 1920×1080, 50 fps, 999 frames, 19.98 s다. 각 video bundle의 `SHA256SUMS`도 검증 통과했다.

**중요한 제한:** manifest에는 source checkpoint와 terrain label은 있지만 **command, evaluator seed, difficulty/curriculum level, initial state**가 없다. 따라서 이름이 같은 terrain끼리도 strict paired episode라고 간주하지 않는다.

---

## 3. 비교 설계와 해석 가능한 범위

| 조건 | Control | H-005 | H-006 | 판정 |
|---|---|---|---|---|
| child mode | PERSONAL | PERSONAL | PERSONAL | 동일 |
| parent record | same model_1499 SHA | same | same | 직접 sibling 비교 가능, parent bytes 별도 미수신 |
| reward delta | unchanged | air 0.20→0.25 | air 0.20→0.30 | 단일변수 |
| seed | 42 | 42 | 42 | 동일, 동일 terrain realization 보장은 아님 |
| num_envs | 4096 | 4096 | 4096 | 동일 |
| PPO/agent | same SHA | same SHA | same SHA | 동일 |
| 추가 학습량 | +1500 | +1500 | +1500 | 동일 |
| global range | 1499–2998 | 1499–2998 | 1499–2998 | 동일 |
| train terrain/curriculum config | same env except reward/log_dir | same | same | 동일 설정 |
| 영상 checkpoint | final 2998 | final 2998 | final 2998 | 동일 checkpoint 시점 |
| 영상 episode metadata | command/seed/difficulty 없음 | 없음 | 없음 | 정성 비교만 가능 |

### 질문별 적합성

- **`feet_air_time 0.20→0.25/0.30`의 이 corrected lineage 안 상대 효과:** **직접 비교에 적합.** 동일 기록 parent, 동일 child 학습량, 동일 PPO/source/seed/num_envs, env diff가 reward 한 값뿐이다.
- **다른 seed·다른 공식 서버에서도 일반화되는 최적 weight:** **판단 불가.** single seed PERSONAL 결과다.
- **완성 정책의 행동 차이:** **조건부 비교.** final checkpoint 영상 provenance는 강하지만 video command/seed/difficulty가 없어 strict paired performance test는 아니다.
- **OFFICIAL 제출 성능/점수:** **판단 불가.** PERSONAL 자료다.

---

## 4. TensorBoard raw 시계열 재분석

### 4.1 파싱·window 정의

각 `native_run/events.out.tfevents*`를 protobuf event record 단위로 직접 파싱했다. `Train/mean_reward/time` 같은 wall-time 축 태그는 main trajectory에서 제외했다.

핵심 결과:

- 세 run 모두 주요 scalar tag 31개 확인.
- iteration 축 핵심 tag는 각각 **1500 points**, global step **1499..2998**, step 중복 없음.
- resume 경계에서 step reset 없음.
- 핵심 scalar에서 NaN/Inf 미검출.

주 비교 window는 **late-500 = 2499..2998**로 정했다. 이유는 +1500 resume 중 초반 curriculum 재적응을 충분히 지난 뒤 전체 후반 1/3을 사용하는 것이며, 자동 best의 reward peak를 따라 window를 고르지 않았다. 경계 민감도 확인으로 late-300(2699..2998), late-750(2249..2998)을 추가했다.

### 4.2 핵심 late-500 비교

아래 termination 값은 training logger의 `Episode_Termination/base_contact` / `time_out` 평균이다. **고정 evaluator의 낙상 확률이나 공식 survival rate가 아니다.**

| 지표 (late-500 mean) | Control 0.20 | H-005 0.25 | H-006 0.30 | H-005−Ctrl | H-006−Ctrl |
|---|---:|---:|---:|---:|---:|
| `Curriculum/terrain_levels` | 5.5010 | 5.4776 | **5.5595** | -0.0234 | **+0.0585** |
| `Metrics/.../error_vel_xy` | 0.3695 | **0.3609** | 0.3774 | **-0.0086** | +0.0079 |
| `Metrics/.../error_vel_yaw` | 1.0455 | 1.0410 | **1.0393** | -0.0045 | -0.0061 |
| `Episode_Termination/base_contact` | **29.616%** | 29.761% | 30.047% | +0.145%p | +0.431%p |
| `Episode_Termination/time_out` | **70.398%** | 70.245% | 69.969% | -0.153%p | -0.430%p |
| `Train/mean_episode_length` | **777.66** | 773.75 | 771.51 | -3.90 | -6.15 |
| `Policy/mean_std` | 1.3432 | **1.3419** | 1.3420 | -0.0013 | -0.0012 |
| `Train/mean_reward` | 2.6963 | **2.8249** | 2.7943 | +0.1285 | +0.0980 |

`Train/mean_reward`는 reward weight 자체가 달라 직접 정책 성능 척도로 쓰지 않는다.

### 4.3 window 민감도

H-005의 XY 개선은 다음과 같이 유지된다.

- late-750: `0.3710 → 0.3626` (`-0.0084`)
- late-500: `0.3695 → 0.3609` (`-0.0086`)
- late-300: `0.3689 → 0.3585` (`-0.0104`)

H-005 terrain은 late-750에서는 사실상 동률(`5.4697 vs 5.4708`), late-500/300에서는 control보다 소폭 낮다. base-contact는 모든 window에서 control보다 `+0.08~+0.15%p` 정도 높다. 따라서 **H-005의 핵심 관찰은 “tracking 소폭 개선, stability/terrain은 동률권”**으로 정리하는 것이 가장 재현성 있다.

H-006은 세 window에서 terrain이 control보다 높고(`+0.045~+0.059`), XY error도 control보다 높다(`+0.003~+0.008`). base-contact 역시 control보다 `+0.24~+0.43%p` 높다. 따라서 **H-006의 terrain↔tracking/stability trade-off 방향 역시 window 선택에 크게 의존하지 않는다.**

### 4.4 후반 붕괴 여부와 checkpoint

late-500을 앞/뒤 250으로 나누면:

- Control: terrain `+0.041`, XY error `-0.0050`, yaw error `-0.0176`, base-contact `+0.74%p`.
- H-005: terrain `-0.004`, XY `-0.0070`, yaw `-0.0427`, base-contact `+0.39%p`.
- H-006: terrain `-0.002`, XY `-0.0133`, yaw `-0.0102`, base-contact `-0.21%p`.

어느 run도 terrain·tracking·termination이 함께 뚜렷하게 악화되는 **joint late collapse**는 아니다. 그러므로 final `model_2998.pt`를 대표 checkpoint로 두는 현재 프로젝트 원칙과 충돌하지 않는다.

### 4.5 reward term과 행동 비용

`Episode_Reward/feet_air_time` weighted scalar late-500은 control `0.00892`, H-005 `0.01231`, H-006 `0.01584`로 weight와 함께 증가한다. 그러나 이 값은 **가중된 reward term**이며 이번 archive에는 해당 IsaacLab 함수의 내부 normalization/aggregation 구현이 포함되어 있지 않다. 따라서 weight로 나눠 “실제 airtime”을 복원하지 않았다.

다른 weighted terms의 late-500 차이는 작다.

- `feet_slide`: control `-0.04586`, H-005 `-0.04654`, H-006 `-0.04623`
- `joint_deviation_hip`: `-0.03508`, `-0.03459`, `-0.03532`
- `flat_orientation_l2`: `-0.01078`, `-0.01106`, `-0.01058`
- `action_rate_l2`: `-0.06310`, `-0.06244`, `-0.06127`

이 차이들만으로 실제 posture/airtime이 개선되었다고 주장하지 않는다.

### 4.6 optimization sanity

late-500 mean value loss는 control `0.00495`, H-005 `0.00498`, H-006 `0.00504` 수준이며, run 시작 resume 경계의 일시적인 큰 값 이후 폭발적 발산은 없다. surrogate loss와 entropy도 세 run이 유사하다. `Policy/mean_std ≈1.34`가 높지만 프로젝트의 기존 finalize/report 검토가 경고하듯 std 하나만으로 학습 실패를 판정하지 않는다. 실제로 terrain은 5.5 수준이고 6지형 영상에서도 upright locomotion이 확인된다.

---

## 5. 6지형 행동 비교

### 5.1 분석 방법과 한계

MP4는 ffprobe로 전체 container/stream metadata를 확인하고, 모든 영상에서 2초 간격 프레임을 조사했다. stairs / inverted stairs / boxes의 핵심 접촉 구간은 0.5초 간격으로 추가 조사했다. 따라서 아래는 **sampled-frame trajectory 관찰**이며, 모든 50 fps 프레임을 사람 눈으로 연속 재생해 보행 주기·jitter 주파수까지 판독한 결과는 아니다.

manifest에 command/seed/difficulty가 없어 **카메라 중심 이동, 화면상 거리, 동일 시각의 위치 차이를 속도·추종 성능으로 정량화하지 않았다.**

### 5.2 지형별 관찰

| Terrain | Control 0.20 | H-005 0.25 | H-006 0.30 | 공통 약점 / 판단 한계 |
|---|---|---|---|---|
| `stairs.mp4` | 약 10–14 s에 계단 접근·진입, sampled frames에서 upright 유지 | 동일 구간에 계단 진입·상승, 명백한 낙상 없음 | 동일하게 계단 진입·상승, 명백한 낙상 없음 | 세 정책 모두 “계단을 전혀 못 오르는” 실패는 보이지 않음. command·step count 미기록이라 통과 속도/성공률 비교 불가 |
| `inverted_stairs.mp4` | 8–14 s stair region 이동 후 flat 쪽 진행, upright | stair region 통과, upright | stair region 통과, upright | camera/방향 때문에 정확한 상승·하강 단수는 영상만으로 정량화하지 않음 |
| `boxes.mp4` | 10–16 s box field 안에서 계속 진행하며 sampled frames에서 upright; outer edge 쪽으로 빠져나오는 장면이 비교적 일찍 보임 | 10–16 s box field 내부 진행, upright | 10–16 s box field 내부 진행, upright | control이 더 빨리 빠져나온 것처럼 보이나 initial realization/command가 동일하다는 manifest 근거가 없어 “더 빠름”으로 판정하지 않음 |
| `random_rough.mp4` | 0–18 s upright progression, 큰 자세 붕괴 없음 | upright progression | upright progression | 작은 발 미끄러짐/roll은 2 s sampling으로 정확히 판독 불가 |
| `slope_up_10deg.mp4` | 약 8–16 s ramp 접근·상승, upright | ramp 위 진행, upright | ramp 위 진행, upright | 모두 slope traversal sanity는 통과. exact command/grade realization 외 정보 없음 |
| `slope_down_10deg.mp4` | ramp 하강/통과 구간에서 upright | upright | upright | descent braking/foot slip의 미세 차이는 sampled frames로 확정하지 않음 |

### 5.3 예상 부작용 확인

`feet_air_time`을 높이면 한 발 장기 지지나 hop/skip이 나타날 수 있다는 프로젝트 prior가 있다. 이번 H-006 `0.30`의 sampled frames에서는 **20초 동안 지속적으로 한 다리만 들고 깡총거리는 명백한 reward-hacking 형태는 보이지 않았다.** H-005도 동일하다.

그러나 이것은 “hop이 없다”는 완전한 판정이 아니다. 0.5 s detailed sampling은 stairs/boxes 핵심 구간만 적용했고, 모든 terrain의 보행 주기를 연속 재생·접촉 센서로 계측하지 않았다. 따라서 gait duty cycle이나 airtime 증가 자체는 미측정이다.

### 5.4 수치와 영상의 교차검증

- H-006의 training terrain이 가장 높다는 수치는 영상에서 slope/stairs/boxes를 전혀 못 넘는 실패와 충돌하지 않는다. 즉 **terrain 상승이 완전히 허구인 신호는 아니다.**
- 하지만 H-006 영상이 control/H-005보다 명백히 obstacle clearance가 우수하다는 증거는 없다. 따라서 `+0.0585 terrain`을 실제 6지형 통과 성능의 명확한 향상으로 승격하지 않는다.
- H-005의 낮은 XY error는 영상에서 큰 불안정이나 정체로 상쇄되는 모습은 보이지 않는다. 따라서 **작은 tracking 이득을 장기 확인해볼 가치**는 있다.
- 세 영상 모두 짧은 1회 클립에서 낙상이 없다고 해서 training base-contact 약 30%와 모순이라고 보지 않는다. training termination은 수천 env/episode 집계이고, 각 영상은 약 20초의 선택된 trajectory 한 개다.

---

## 6. 핵심 발견과 경쟁 설명

### 발견 A — H-005의 XY tracking 이득

**관찰:** late-500 XY error `0.3609`로 control `0.3695`보다 `0.0086` 낮고, late-750/300에서도 같은 방향이다. yaw는 사실상 동률, terrain/base-contact는 동률권이다.

**해석:** `feet_air_time 0.20→0.25`가 보행 스윙을 조금 더 적극적으로 만들어 commanded planar velocity를 따라가는 데 유리했을 가능성이 있다.

**경쟁 설명:** single seed에서의 stochastic training 차이, curriculum exposure 차이, simulator nondeterminism으로도 이 정도 작은 차이가 생길 수 있다. 같은 seed는 paired terrain episode를 보장하지 않는다.

**반대 근거:** terrain은 높아지지 않았고 base-contact도 미세하게 증가했다. weighted `feet_air_time` 증가는 weight 변경 자체가 포함된 값이라 physical airtime 개선 증거가 아니다.

**판별 방법:** control 2998과 H-005 2998에서 각각 **reward unchanged + 동일 +2K continuation**을 수행해 total 5K에서 same window/evaluator로 다시 비교한다. 결과가 유지되면 작은 효과가 누적되는지 확인할 수 있다.

### 발견 B — H-006의 terrain 증가와 linear tracking/stability 비용

**관찰:** late-500 terrain `5.5595`로 최고지만 XY `0.3774`와 base-contact `30.047%`는 control/H-005보다 높다. late-300/750에서도 방향이 같다.

**해석:** 더 큰 airtime reward가 장애물 노출/스윙을 늘려 curriculum progression에는 조금 유리했지만, 평면 속도 tracking 또는 안정성 비용을 만들었을 가능성이 있다.

**경쟁 설명:** terrain curriculum은 정책 행동에 따라 노출 분포가 바뀌므로 terrain 차이가 직접 obstacle skill 차이와 동일하지 않다. single-seed stochastic 차이일 수도 있다.

**반대 근거:** 6지형 영상에서 H-006의 명백한 장애물 우위도, 반대로 명백한 hopping collapse도 보이지 않는다. yaw는 오히려 control보다 미세하게 낮다.

**판별 방법:** 현재 목적이 “다음 GPU 시간을 어디에 쓸지”라면 H-006 장기 연장보다 H-005/control 확인이 정보가 크다. H-006의 terrain trade-off를 특별히 살릴 필요가 생길 때만 fixed evaluator에서 실제 obstacle progress를 직접 측정한다.

### 발견 C — automatic best 차이는 정책 우열 증거가 아님

Control/H-005 automatic best가 `model_2900`, H-006이 final `2998`이라는 차이는 mean reward peak의 위치 차이다. 이번 reward weight가 서로 달라 total reward scale과 landscape도 달라진다. 또한 video는 세 policy 모두 final 2998이다. 따라서 automatic best alias를 “H-006이 더 안정적으로 끝까지 개선됐다” 같은 행동 우열로 해석하지 않는다.

---

## 7. 프로젝트 판단과 다음 행동

### 7.1 상태 요약

| 항목 | Control | H-005 | H-006 |
|---|---|---|---|
| 실행 | COMPLETE | COMPLETE | COMPLETE |
| evidence validation | PASS | PASS | PASS |
| 비교 적합성 | matched control | direct sibling | direct sibling |
| 가설 결정 | 기준선 | **PROMOTE to long matched confirmation** | **HOLD** |
| 정책 행동 | 6지형 sampled sanity 통과 | 6지형 sanity 통과, XY 소폭 개선 | 6지형 sanity 통과, terrain↑ vs XY/base-contact trade-off |
| 대표 checkpoint | final 2998 | final 2998 | final 2998 |

### 7.2 다음 한 번의 행동 — 1순위

**H-001 corrected control 2998과 H-005 2998을 각각 reward 그대로 유지해 동일 +2K continuation**을 수행한다.

- parent/checkpoint: 각자의 `model_2998.pt`
- 유지 설정: source/PPO/seed/num_envs/headless/curriculum config 그대로
- 변경 값: 없음. H-005는 `feet_air_time=0.25`, control은 `0.20` 유지
- 추가 학습량: 동일 +2K (global 약 2998→4997 범위)
- 비교 질문: H-005의 XY 이득이 5K 수준까지 지속되는가? terrain/base-contact 비용이 누적되는가?
- 공통 평가: 동일 TensorBoard window + 가능한 동일 fixed evaluator command/terrain/seed set + final checkpoint native 6-terrain evidence
- 기대 효과: 현재 작은 차이를 단기 single-run noise와 지속 효과로 분리
- 부작용: H-005가 장기에서 terrain/stability를 잃거나 gait hopping을 강화할 가능성
- 결과별 결정:
  - XY 개선이 유지되고 terrain/termination/행동 품질이 control과 동등 이상 → H-005를 다음 OFFICIAL 검증 후보로 유지
  - XY 이득이 사라지거나 stability/terrain이 명확히 악화 → H-005 HOLD/REJECT, corrected control 유지

이 제안은 **새 학습 실행 승인이 아니다.** 현재 분석 요청 범위에는 학습·렌더·export·서버 작업이 포함되지 않는다.

### 7.3 2순위가 필요한 경우

H-006의 terrain trade-off가 실제 obstacle progress 향상인지 확인하고 싶다면 새 학습보다 먼저 동일 fixed evaluator에서 control/H-005/H-006 final 2998을 평가하는 편이 낫다. 특히 stairs/boxes/slope에서 **실제 forward progress, stall, fall, XY/yaw tracking**을 같은 command/seed/scenario로 기록하면 training curriculum level의 의미를 분리할 수 있다.

---

## 8. 한계와 재확인 가능한 근거

### 8.1 한계

1. 세 run은 PERSONAL single-seed다. OFFICIAL 점수나 일반적 최적 weight로 확대하지 않는다.
2. parent checkpoint는 세 metadata가 동일 SHA를 기록하지만 parent archive 원본 자체는 이번 입력에 없다. `source_provenance_verified=false`다.
3. video manifest에는 command/seed/difficulty가 없다. 같은 terrain label을 strict paired episode로 취급하지 않는다.
4. 영상은 sampled-frame 분석이다. 모든 보행 cycle을 연속 재생해 gait frequency, duty cycle, jitter를 측정한 것이 아니다.
5. TensorBoard point 500개는 500 independent seed가 아니다. p-value/CI를 계산하지 않았다.
6. weighted reward term을 나누어 underlying physical metric을 역산하지 않았다.
7. `Episode_Termination/base_contact`는 training 집계이며 official evaluator fall rate가 아니다.

### 8.2 재확인 가능한 archive 내부 근거

#### Control
- `metadata.json`
- `command.txt`
- `source/humanoid_rewards.py`
- `source/identity.json`
- `native_run/params/env.yaml`
- `native_run/params/agent.yaml`
- `native_run/events.out.tfevents.1790318521...`
- `console.log`
- `checkpoints/model_2998.pt`
- `collected/exported/model_best.pt`
- video bundle `checkpoint-h1-model_2998-fc3c60cdff61/video_suite_manifest.json`

#### H-005
- 동일 구조, event `events.out.tfevents.1790320336...`
- final SHA `9454afa964bb…85cc`
- video bundle `checkpoint-h1-model_2998-9454afa964bb/`

#### H-006
- 동일 구조, event `events.out.tfevents.1790322157...`
- final SHA `dc1f61e22e7f…b5ff`
- video bundle `checkpoint-h1-model_2998-dc1f61e22e7f/`

### 8.3 프로젝트 문서와의 정합성

현재 핵심팩은 과거 H-005/H-006이 `feet=-0.2` parent에서 실행되어 최종 단일변수 효과로 쓰지 말고, corrected `+0.2 TERM50` parent와 unchanged control에서 재실험해야 한다고 명시했다 (`18_H1_FINALIZE_REPORT_LIMITATIONS`, `14_H1_NEXT_RUN_PARAMETER_COMPARISON`, `00_START_HERE_CONTEXT_AND_MAP`). 이번에 제공된 corrected control/H-005/H-006 세 archive는 **그 재실험 질문에 직접 대응하는 새 evidence**다. 따라서 과거 HOLD의 이유였던 “잘못된 parent feet 값”은 이번 세 sibling 비교에는 더 이상 적용되지 않는다. 다만 PERSONAL/single-seed라는 한계는 그대로 남는다.

---

## 최종 답변

1. **목표 행동 수행 정도:** 세 final 2998 정책 모두 제공된 6지형 sampled 영상에서 upright locomotion과 obstacle-region progression을 보이며 명백한 20초 내 낙상은 확인되지 않았다. training late-500에서는 terrain 약 5.48–5.56, base-contact termination 약 29.6–30.0%, XY error 약 0.361–0.377이다. 영상은 qualitative sanity evidence이며 공식 성공률은 아니다.
2. **관찰 차이와 설정 효과:** corrected sibling 내 실제 설정 차이는 `feet_air_time` 하나이므로 상대 차이를 이 변경과 연결해 해석할 수 있다. H-005는 작은 XY tracking 이득, H-006은 작은 terrain 이득과 XY/base-contact 비용이 관찰된다. 그러나 single seed라 일반적 인과 효과 크기나 최적 weight를 확정할 수 없다.
3. **현재 결정:** H-005를 장시간 matched confirmation으로 **PROMOTE**, H-006은 **HOLD**, 대표 checkpoint는 세 run 모두 final `model_2998`. 가장 먼저 해소할 불확실성은 H-005의 작은 XY 이득이 total 5K 수준에서도 control 대비 유지되는지 여부다.
