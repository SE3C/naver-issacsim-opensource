# Go2 최종 제출용 기술 개선 리포트 — 권장 흐름 및 초안

> 문서 성격: **최종 제출본을 만들기 위한 near-final draft**  
> 대상 로봇: **Unitree Go2**  
> 기준일: **2026-09-15**  
> 현재 상태: reward 설계와 공식 학습 결과는 확정되어 있으나, **최종 제출 checkpoint는 4300 / 4800 / 4900 중 최종 선택 전**이다.  
> 작성 원칙: 공식 서버 학습 결과와 개인 서버의 보조 검증을 명확히 분리하고, 자동 `model_best`나 단일 reward 수치만으로 성능을 단정하지 않는다.

<!-- 제출 직전에는 이 주석과 '작성 메모' 성격의 문장을 제거해도 된다. -->

---

## 1. 개선 목표

기본 Go2 정책을 관찰했을 때 가장 먼저 해결하고자 한 문제는 **오래 버티는 것과 실제로 명령을 잘 따라 험지를 진행하는 것이 서로 다를 수 있다는 점**이었다.

공식 baseline 1K는 학습·export 파이프라인 자체는 정상적으로 완료되었지만, 마지막 구간에서 terrain level이 0으로 표시되고 XY velocity error가 약 `1.8421`, timeout이 약 `93.45%`였다. 즉 episode를 오래 유지하는 것만으로는 충분하지 않았고, 실제 이동 명령 추종과 지형 진행 능력을 더 직접적으로 강화할 필요가 있었다.

따라서 본 개선의 목표를 다음과 같이 정했다.

1. 전진 속도 명령 추종 성능을 강화한다.
2. 험지에서 필요한 수직 움직임까지 과도하게 억제하지 않는다.
3. 단순 생존이 아니라 **명령 추종 + 생존 + 지형 진행**이 동시에 유지되는 정책을 만든다.
4. 학습 reward 하나만 보지 않고 terrain, tracking error, termination, episode length, value loss, 실제 play를 함께 확인한다.

---

## 2. 실패 가설에서 얻은 교훈

A1 이전에 몸통의 roll/pitch 방향 각속도 억제를 더 강하게 하면 보행이 안정될 것이라는 가설을 시험했다.

### G5 실험

변경은 한 항목뿐이었다.

```text
ang_vel_xy_l2: -0.08 → -0.12
```

공식 서버에서 1K까지 학습한 결과 수치적으로는 timeout이 높고 base-contact 종료가 낮았지만, terrain level은 0에 머물렀고 XY velocity error는 약 `1.7363`이었다. play 영상에서는 정상적인 사족 보행 대신 비정상 자세로 episode를 유지하는 장면이 확인되었다.

이 실험을 통해 다음을 확인했다.

> **낮은 낙상 종료율과 긴 episode가 곧 좋은 locomotion을 의미하지 않는다.**

따라서 이후에는 안정성 penalty를 단순히 더 강하게 만드는 방식보다, **목표 속도를 제대로 추종하도록 보상을 강화하면서 험지에서 필요한 움직임 자유도를 지나치게 제한하지 않는 방향**으로 설계를 전환했다.

---

## 3. 최종 개선안 A1

A1에서는 baseline 대비 두 reward weight를 변경했다.

| Reward term | Baseline | A1 | 의도 |
|---|---:|---:|---|
| `track_lin_vel_xy_exp` | 1.0 | **1.5** | 목표 선속도 추종을 더 강하게 유도 |
| `lin_vel_z_l2` | -3.0 | **-2.0** | 험지 통과에 필요한 수직 운동을 과도하게 억제하지 않도록 완화 |
| `ang_vel_xy_l2` | -0.08 | -0.08 | G5에서 과도한 강화가 실패했으므로 baseline 유지 |
| `action_rate_l2` | -0.01 | -0.01 | 급격한 action 변화 억제 유지 |
| `feet_air_time` | 0.01 | 0.01 | 기존 보행 항 유지 |

핵심 가설은 다음과 같다.

> **선속도 추종 보상을 강화하고 수직 속도 penalty를 완화하면, 평지 생존에만 머무르지 않고 험지에서 실제로 전진하는 locomotion을 유도할 수 있다.**

A1은 두 reward를 동시에 변경한 조합 실험이므로, 두 항목 각각의 독립적인 인과 효과를 분리해 주장하지 않는다. 본 리포트의 결론은 **A1 조합 전체의 결과**에 대한 것이다.

---

## 4. 공식 서버 학습 방법

최종 제출 후보를 만드는 학습은 대회 운영진이 제공한 공식 서버에서 수행했다.

주요 조건은 다음과 같다.

```text
Robot           : Go2
Environments    : 4096
Seed            : 42
Reward setting  : A1
Training source : official competition environment
```

원본 A1 run은 fresh 상태에서 시작해 iteration 4837 부근에서 사용자 중단으로 종료되었다. 그러나 `model_0.pt`부터 `model_4800.pt`까지 49개의 checkpoint, TensorBoard event, console, source/config evidence가 보존되었다. 저장된 checkpoint의 actor/critic tensor에서는 NaN/Inf가 확인되지 않았다.

이후 원본 `model_4800.pt`를 정확한 SHA-256으로 확인한 뒤, 공식 서버에서 200 iteration을 이어 학습하여 nominal 5K 구간까지 복구했다.

중요한 점은 resume 과정에서 network와 optimizer는 이어졌지만 **environment-side curriculum은 다시 낮은 단계에서 시작했다는 것**이다. 따라서 원본 4800과 recovery 4900의 raw terrain level 또는 raw mean reward를 단순히 같은 난이도에서 나온 값처럼 비교하지 않았다.

---

## 5. 공식 학습 결과

### 5.1 원본 fresh run

원본 trajectory는 terrain level이 학습 후반까지 계속 상승했고, iteration 4800에서 다음 상태를 보였다.

| 지표 | Original iter 4800 |
|---|---:|
| Mean reward | 20.14 |
| Terrain level | 5.7367 |
| XY velocity error | 0.5017 |
| Yaw error | 0.4278 |
| Mean episode length | 968.01 |
| Timeout | 91.89% |
| Base contact termination | 8.11% |
| Mean action std | 0.66 |
| Value loss | 0.0259 |

원본 run에서 기록된 최고 mean reward는 `21.85 @ iter 4284`였다. 100-iteration checkpoint 간격 때문에 당시 자동으로 선택된 best 계열 checkpoint는 `model_4300.pt`였으며, hash 대조로도 이전 `model_best`와 정확히 일치했다.

### 5.2 장기 학습 중 critic 불안정성

원본 trajectory에서는 value loss가 대부분 낮은 수준을 유지했지만 간헐적으로 매우 큰 spike가 반복되었다. 최대값은 `283.8869 @ iter 3747`이었고, 일부 spike 구간에서는 mean reward도 급락했다.

그러나 이후 reward, terrain, episode length가 다시 회복되었고 보존된 checkpoint tensor에서 NaN/Inf는 발견되지 않았다. 따라서 이를 지속적인 학습 붕괴로 보지는 않았지만, **critic이 완전히 안정적인 trajectory였다고도 판단하지 않았다.**

이 때문에 자동 reward best 하나만으로 제출 후보를 정하지 않고, 후반 checkpoint들을 별도로 비교했다.

### 5.3 Recovery 4800→5000

원본 `model_4800.pt`에서 resume한 recovery run은 정상 완료되었고 evidence validation과 official backup도 완료되었다.

recovery에서 자동 선택된 checkpoint는 `model_4900.pt`였다.

| 지표 | Recovery iter 4900 |
|---|---:|
| Mean reward | 24.40 |
| Terrain level | 4.6251* |
| XY velocity error | 0.5489 |
| Yaw error | 0.3741 |
| Mean episode length | 982.37 |
| Timeout | 96.18% |
| Base contact termination | 3.82% |
| Mean action std | 0.57 |
| Value loss | 0.0201 |

\* resume 뒤 curriculum reset이 있었으므로 original 4800의 terrain `5.7367`과 직접 비교하지 않는다.

recovery 마지막 iteration 4999에서는 terrain level이 `5.7940`까지 다시 상승했다. 따라서 resume 뒤 curriculum을 다시 따라 올라가는 능력은 확인되었다.

recovery 구간의 최대 value loss는 `5.3492`로, 원본 장기 run의 최대 spike보다 훨씬 작았다. 한두 번의 일시적인 reward/value-loss 이상은 있었지만 지속 발산은 확인되지 않았다.

---

## 6. 제출 후보 3개를 따로 비교한 이유

학습 로그만 보면 자동 선택된 checkpoint가 항상 실제 locomotion 최적 정책이라고 보장할 수 없다. 따라서 다음 세 지점을 후보로 보존했다.

| 후보 | 의미 | 주요 특징 |
|---|---|---|
| `model_4300.pt` | 원본 fresh run의 자동 reward-best 계열 | 최고 reward 구간 4284 근처, fresh lineage |
| `model_4800.pt` | 원본 fresh run의 후반 checkpoint | terrain 5.7367, 높은 curriculum 구간을 경험한 정책 |
| `model_4900.pt` | recovery run의 자동 best | 낮은 base-contact, 높은 timeout, 낮은 std, policy export 완료 |

checkpoint SHA-256은 다음과 같다.

```text
model_4300.pt
82efb1a59bfad74c5b03b7584fe7cf27865dcd0603550f11340c4134c6a802c8

model_4800.pt
 ea93f9b5b04d91a91d1cdb97c6d328978017991e0602745f9269c7190bfaba65

model_4900.pt
250e430cbb74f837af15384c145e865f7c8d8155fc65a7fe8b21dda1c27514cd
```

<!-- 제출 직전 공백 오타가 신경 쓰이면 4800 SHA 앞의 선행 공백을 제거할 것. -->

recovery handoff의 `policy.pt`는 `model_4900.pt`의 deterministic actor MLP tensor 8개와 exact-match하여, 현재 4900 후보의 checkpoint→policy 연결은 검증되어 있다.

---

## 7. 보조 고정조건 검증

> **이 절의 결과는 개인 NVIDIA 서버에서 수행한 inference-only 후보 비교이며 공식 대회 평가 점수가 아니다.**  
> 정책을 새로 학습하지 않았고, 공식 서버에서 생성된 세 checkpoint를 동일 조건에서 실행하여 상대적인 특성을 확인하는 용도로만 사용했다.

학습 로그의 curriculum 차이를 제거하기 위해 세 후보를 동일한 고정 조건에서 비교했다.

```text
Models       : 4300 / 4800 / 4900
Terrains     : stairs, inverted_stairs, boxes, random_rough,
               +20° slope, -20° slope
Episodes     : 64 per model × terrain
Total        : 1,152 first episodes
Seed         : 4201
Command      : vx=1.0, vy=0.0, yaw_rate=0.0
Curriculum   : disabled
Inference    : deterministic
Difficulty   : 1.0
```

6개 terrain 단순 평균은 다음과 같았다.

| 지표 | 4300 | 4800 | 4900 |
|---|---:|---:|---:|
| 20 s timeout 도달률 ↑ | 96.61% | **98.18%** | 94.01% |
| Base-contact 종료율 ↓ | 3.39% | **1.82%** | 5.99% |
| 평균 생존시간 ↑ | 19.56 s | **19.80 s** | 19.46 s |
| Episode return ↑ | 28.03 | 28.48 | **28.95** |
| XY velocity RMSE ↓ | 0.456 | 0.443 | **0.410** |
| Yaw-rate RMSE ↓ | 0.135 | **0.102** | 0.110 |
| +X 평균 이동거리 ↑ | 11.58 m | 12.11 m | **12.56 m** |

이 결과는 세 후보의 성격이 서로 다름을 보여준다.

- **4800:** 세 후보 중 가장 낮은 base-contact 종료율과 가장 높은 20초 생존율
- **4900:** 평균 tracking error와 전진거리, episode return에서 강점
- **4300:** 원본 reward-best이지만 고정조건 비교에서 4800보다 뚜렷한 우위를 보이지 않음

특히 boxes와 stairs에서 4800의 안정성이 두드러졌다.

| Terrain | 4300 timeout | 4800 timeout | 4900 timeout |
|---|---:|---:|---:|
| Boxes | 92.19% | **95.31%** | 82.81% |
| Stairs | 87.50% | **93.75%** | 85.94% |

반면 random rough와 ±20° slope에서는 세 후보 모두 해당 seed에서 64/64가 20초 timeout까지 도달했다.

### Inverted stairs에서 발견한 평가 함정

`inverted_stairs`에서는 timeout 도달률만 보면 매우 좋아 보였지만 평균 +X 이동거리가 작았다.

```text
4300 : 1.17 m
4800 : 1.16 m
4900 : 2.28 m
```

즉 **넘어지지 않고 살아남는 것과 실제로 앞으로 진행하는 것은 다르다.**

이 결과 때문에 최종 후보를 고를 때 timeout/base-contact만 단독으로 사용하지 않고, tracking error와 실제 진행량을 함께 보게 되었다.

또한 이 evaluator의 `success_timeout_pct`는 엄밀히 말해 **20초 생존율**이며, 지형 완주 성공률로 표현하지 않는다.

---

## 8. 최종 정책 선택 논리

<!-- 이 절은 최종 제출 checkpoint가 정해진 뒤 한 번만 수정하면 된다. -->

현재 증거를 종합하면 세 후보는 다음과 같이 해석된다.

### 4300

원본 fresh trajectory의 자동 reward-best라는 장점이 있다. 그러나 후반 4800에 비해 curriculum 경험량이 적고, 동일 고정조건 evaluator에서도 명확한 우위를 확인하지 못했다.

### 4800

원본 fresh 0→4800 lineage를 유지하며 terrain level `5.7367`까지 학습했다. 개인 고정조건 비교에서는 6개 terrain 평균 base-contact 종료율이 가장 낮고, boxes와 stairs에서 가장 높은 생존률을 보였다. 반면 현재 보존본에는 4800 전용 `policy.pt`가 없으므로 **4800을 최종 제출할 경우 공식 checkpoint에서 fresh export한 policy와 matching env를 다시 검증해야 한다.**

### 4900

recovery 구간의 자동 best이며 현재 `policy.pt`와 actor tensor exact-match가 확인된 가장 완성된 제출 artifact다. 학습 로그에서 낮은 base-contact, 높은 timeout, 낮은 action std를 보였고, 고정조건 evaluator에서는 평균 tracking과 전진거리에서 가장 좋은 값을 보였다. 반면 boxes와 stairs에서는 4800보다 base-contact 종료가 많았다.

### 최종 선택 문장

> **최종 제출 정책: `[MODEL_XXXX]`**  
> 선택 이유: `[공식 play 결과 + 고정조건 evaluator + official training evidence를 종합한 최종 이유를 2~4문장으로 기입]`

최종 선택에서는 단일 `Train/mean_reward` 최고값보다 다음 우선순위를 사용한다.

```text
1. 비정상 자세/낙상 없이 실제 locomotion이 가능한가
2. 경사·계단·험지에서 생존하는가
3. 목표 속도와 회전 명령을 추종하는가
4. 특정 지형에서만 강하고 다른 지형에서 급격히 무너지지 않는가
5. checkpoint → policy.pt → env.yaml provenance가 명확한가
```

---

## 9. 개선안의 의미

이번 실험에서 가장 중요한 변화는 단순히 mean reward가 증가했다는 점이 아니다.

A1은 baseline보다 선속도 추종을 더 직접적으로 보상하고, 험지에서 발생하는 수직 움직임에 대한 penalty를 완화했다. 공식 fresh trajectory에서 terrain level이 5.x까지 상승했고, XY tracking error와 episode 유지 지표도 함께 개선되는 구간이 관찰되었다.

또한 G5 실패 사례와 후속 checkpoint 비교를 통해 다음과 같은 설계 원칙을 얻었다.

> **Go2 보행에서는 ‘넘어지지 않는 것’만 최적화하면 정상 locomotion과 다른 local optimum에 빠질 수 있으므로, 생존성과 명령 추종·지형 진행을 동시에 확인해야 한다.**

이 원칙에 따라 최종 제출 정책도 reward peak 하나가 아니라 여러 지표와 실제 동작을 함께 확인해 결정한다.

---

## 10. 한계와 과장하지 않는 범위

본 결과에는 다음 한계가 있다.

1. A1은 `track_lin_vel_xy_exp`와 `lin_vel_z_l2` 두 값을 동시에 변경했기 때문에 각각의 독립적인 인과 효과는 분리되지 않았다.
2. recovery에서는 curriculum이 reset되었으므로 original 4800과 recovery 4900의 raw reward·terrain 수치를 같은 난이도의 직접 비교로 사용할 수 없다.
3. 원본 장기 run에서는 반복적인 critic value-loss spike가 있었으므로 수치적으로 완전히 안정적인 학습 trajectory라고 표현하지 않는다.
4. 개인 서버의 1,152-episode benchmark는 **공식 점수나 공식 평가 구현이 아니라 후보 비교용 보조 자료**다.
5. 고정조건 benchmark는 seed 4201 단일 seed이므로 통계적 일반화를 과도하게 하지 않는다.
6. `inverted_stairs` 사례에서 확인했듯 timeout 도달은 실제 지형 진행 성공과 동일하지 않다.
7. 최종 제출 성능은 운영진의 공식 격리 시나리오 평가 결과로 결정되며, 내부 evaluator 값으로 공식 점수를 예측하지 않는다.

---

## 11. 제출 파일 정합성 확인

최종 제출 직전에는 다음 세 요소가 동일한 정책 lineage를 가리키는지 확인한다.

```text
policy.pt
+ env.yaml
+ 기술 개선 리포트
```

`model_best.pt`와 `report.html`은 진단 자료로 사용하되, 파일명이나 자동 선택 결과만으로 제출 정책을 단정하지 않는다.

### 4900을 선택할 경우 현재 확인된 연결

```text
model_4900.pt
SHA-256:
250e430cbb74f837af15384c145e865f7c8d8155fc65a7fe8b21dda1c27514cd

policy.pt
SHA-256:
22957506fefe1cde249548705fef30147fe149e1086c926ff447ff001c2cc277

policy deterministic actor ↔ model_4900 actor
8 / 8 MLP tensors exact-match
```

### 4800을 선택할 경우 필요한 조치

현재 보존된 4800 checkpoint는 다음이다.

```text
model_4800.pt
SHA-256:
ea93f9b5b04d91a91d1cdb97c6d328978017991e0602745f9269c7190bfaba65
```

4800을 최종 제출하려면 이 **원본 fresh 4800 checkpoint**를 source로 사용해 공식 export를 다시 수행하고, 새 `policy.pt`와 `env.yaml`의 provenance를 확인한 뒤 제출한다.

---

## 12. 최종 요약

본 개선은 Go2 baseline의 단순 생존 편향을 줄이고 실제 속도 추종과 험지 locomotion을 강화하기 위해 수행했다.

핵심 reward 변경은 다음 두 가지다.

```text
track_lin_vel_xy_exp : 1.0  → 1.5
lin_vel_z_l2         : -3.0 → -2.0
```

반대로 `ang_vel_xy_l2`를 더 강하게 만든 G5는 높은 생존 지표에도 불구하고 정상 locomotion을 만들지 못해 기각했다.

A1 공식 학습에서는 terrain 5.x 구간까지 진행했고, 후반 checkpoint들을 따로 보존하여 4300, 4800, 4900을 비교했다. recovery의 4900은 tracking 측면에서 강점을 보였고, 원본 4800은 동일 고정조건 비교에서 낙상 안정성이 가장 좋았다.

따라서 최종 제출 정책은 자동 reward-best가 아니라 **공식 학습 provenance, 실제 locomotion, 지형별 안정성, 명령 추종을 함께 고려해 선택한다.**

> **최종 제출 checkpoint: `[MODEL_XXXX]`**  
> **최종 선택 근거: `[최종 official play 확인 뒤 기입]`**

---

# 부록 A. 현재 후보 핵심 수치

## Original 4300

```text
reward          20.65
terrain          5.5469
XY error         0.5636
yaw error        0.3999
episode length 951.37
base contact      7.86%
timeout          92.14%
action std        0.64
value loss        0.1777
```

## Original 4800

```text
reward          20.14
terrain          5.7367
XY error         0.5017
yaw error        0.4278
episode length 968.01
base contact      8.11%
timeout          91.89%
action std        0.66
value loss        0.0259
```

## Recovery 4900

```text
reward          24.40
terrain          4.6251   # curriculum reset 이후이므로 직접 비교 금지
XY error         0.5489
yaw error        0.3741
episode length 982.37
base contact      3.82%
timeout          96.18%
action std        0.57
value loss        0.0201
```

---

# 부록 B. 증거 등급

| 자료 | 사용 방식 |
|---|---|
| 공식 서버 train console / TensorBoard / checkpoint | **주요 학습 근거** |
| 공식 `env.yaml`, source identity, SHA-256 | **reward 설정·provenance 근거** |
| 공식 play 영상 | **정성 locomotion 검증** |
| 개인 서버 고정조건 evaluator | **후보 간 보조 비교만 사용** |
| 자동 `report.html` / `model_best` | 진단·후보 생성용. 최종 성능 판정 단독 사용 금지 |
| 내부 evaluator의 timeout | 생존 지표. 공식 지형 성공률로 표현 금지 |

---

# 부록 C. 작성에 사용한 주요 근거

- NAVER CONNECT Robotics Cup 2026 통합 규정 정리
- 학습·제출 실행 안내
- Go2 학습 코드 및 A1 1K→3K 분석 정리
- 실험 전체 export / TensorBoard 복원 규칙
- Go2 G5 Official 1K Lightweight Failure Analysis
- Go2 A1 공식 서버 3개 Export 심층 분석
- `A1_QUANT_EVAL_SEED4201_D1` fixed benchmark archive

개인 서버 자료는 제출 정책 학습 근거로 사용하지 않고, **공식 서버에서 학습된 checkpoint의 inference-only 비교 자료**로만 구분했다.
