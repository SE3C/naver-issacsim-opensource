# A1 Go2 4800 vs 4900 통합 심층 분석 보고서
## 정량 벤치마크 · 체크포인트 계보 · 영상 검증 · 최종 선택 · 학습기록서 활용안

- 작성 기준일: 2026-09-15
- 대상: Go2 A1 계열 `model_4800.pt`, `model_4900.pt`
- 비교 참조: `model_4300.pt`
- 결론 요약: **최종 제출 우선 후보는 `model_4800.pt`**
- 핵심 이유: `model_4900.pt`는 추종·진행성에서 이점이 있으나, 통제된 1,152-episode 내부 벤치마크에서 `model_4800.pt`가 훨씬 낮은 낙상률과 더 안정적인 행동 변화량을 보였고, 6개 native play 영상에서도 4800의 안정성이 심각한 locomotion 저하로 이어졌다는 증거가 관찰되지 않았다.
- 중요한 제한: 6개 영상은 **정량 벤치마크의 완전한 영상 재현이 아니라 qualitative sanity check**이다. 특히 stairs/inverted-stairs 영상은 특정 지형을 반드시 횡단하도록 command와 spawn 방향을 고정하지 않았으므로 traversal 성능의 직접 증거로 과장하면 안 된다.

---

# 1. 연구 질문

이번 비교의 핵심 질문은 단순히 “4800과 4900 중 reward가 더 높은 모델은 무엇인가?”가 아니다.

실제로 답해야 하는 질문은 다음과 같다.

1. 더 오래 학습된 4900이 4800보다 실제 locomotion 품질이 좋아졌는가?
2. 4900에서 좋아진 속도 추종·진행성이 낙상 위험 증가를 감수할 만큼 가치가 있는가?
3. 공식 평가처럼 다양한 지형에서 한 번의 실패가 큰 손실이 될 수 있는 상황에서 어느 checkpoint가 더 안전한가?
4. 학습 로그의 reward, terrain level, critic loss, action std 중 어떤 지표를 최종 모델 선택에 신뢰해야 하는가?
5. 정량평가와 실제 영상 관찰이 서로 같은 결론을 지지하는가?
6. evidence/provenance를 어떻게 남겨야 나중에 “어떤 checkpoint에서 어떤 영상과 수치가 나왔는지” 다시 검증할 수 있는가?

이 질문을 해결하기 위해 **학습 로그 → checkpoint forensic → 통제 정량평가 → native 영상 검증** 순서로 근거를 쌓았다.

---

# 2. 실험 전체의 맥락

## 2.1 A1 reward 가설

A1에서는 기본 Go2 reward에서 다음 두 핵심 항목을 조정했다.

| Reward | 기존 | A1 | 의도 |
|---|---:|---:|---|
| `track_lin_vel_xy_exp` | 1.0 | **1.5** | 명령된 평면 속도를 더 적극적으로 추종 |
| `lin_vel_z_l2` | -3.0 | **-2.0** | 수직 속도 억제를 약화해 지나친 보수성을 줄임 |
| `ang_vel_xy_l2` | -0.08 | -0.08 | 유지 |
| `action_rate_l2` | -0.01 | -0.01 | 유지 |
| `feet_air_time` | 0.01 | 0.01 | 유지 |

가설은 다음과 같았다.

> 전진 속도 추종을 강화하면서 수직 움직임 패널티를 약간 완화하면, 기본 정책보다 더 적극적으로 험지를 통과하면서도 기존 Go2의 안정성을 크게 잃지 않을 수 있다.

이 가설은 “속도만 크게 올리는 실험”이 아니라 **진행성 대 안정성의 균형점**을 찾는 실험으로 이해해야 한다.

## 2.2 G5 실패가 제공한 대비군

A1 이전의 G5 계열에서는 `ang_vel_xy_l2`를 더 강하게 억제하는 방향의 실험이 있었고, 결과적으로 로봇이 비정상 자세/눕기 같은 **survival local optimum**으로 빠지는 강한 음성 결과가 관찰되었다.

이 경험은 다음 연구 원칙을 강화했다.

> RL에서 “안 넘어지는 것처럼 보이는 지표”는 실제 task 성공과 동일하지 않다. 로봇은 reward의 허점을 이용해 움직이지 않거나 비정상 자세를 유지하는 방식으로도 생존시간을 늘릴 수 있다.

이 원칙은 이후 inverted stairs의 “timeout survival 100%인데 실제 전진은 거의 없음”을 해석하는 데도 그대로 적용된다.

---

# 3. A1 학습 및 checkpoint 계보

## 3.1 원래 5K 학습

- 목표: 5000 iterations
- 실제 원본 학습: 약 iteration 4837에서 사용자 Ctrl+C로 중단
- 마지막 보존 checkpoint: `model_4800.pt`
- `model_4800.pt` SHA-256:

```text
ea93f9b5b04d91a91d1cdb97c6d328978017991e0602745f9269c7190bfaba65
```

iteration 4800 부근의 주요 로그:

| 지표 | 값 |
|---|---:|
| Mean reward | 20.14 |
| Terrain level | 5.7367 |
| `track_lin_vel_xy_exp` | 0.5017 |
| `track_ang_vel_z_exp` | 0.4278 |
| Mean episode length | 968.01 |
| Mean action std | 0.66 |
| Timeout | 91.89% |
| Base contact | 8.11% |
| Value loss | 0.0259 |

원본 run에서는 critic/value loss가 일부 구간에서 크게 튀었으나 다시 회복했다. 이것을 “actor가 망가졌다”와 동일시하면 안 된다. value loss는 critic 진단값이며 제출되는 actor의 직접 성능 지표가 아니다.

## 3.2 4800 → 5000 recovery

`model_4800.pt`에서 resume하여 5000까지 이어갔다.

중요한 제한은 **resume 과정에서 curriculum state가 완전히 동일하게 이어지지 않아 terrain level이 reset되었다는 점**이다. 따라서 원본 4800의 terrain level과 recovery 4900/4999의 terrain level을 직접 비교해 “4900이 지형을 더 잘한다/못한다”고 결론내리면 안 된다.

recovery에서 실제 자동 best/export에 대응한 checkpoint는 `model_4900.pt`였다.

`model_4900.pt` SHA-256:

```text
250e430cbb74f837af15384c145e865f7c8d8155fc65a7fe8b21dda1c27514cd
```

4900 부근:

| 지표 | 값 |
|---|---:|
| Mean reward | 24.40 |
| Terrain level | 4.6251 (reset 이후 값) |
| `track_lin_vel_xy_exp` | 0.5489 |
| `track_ang_vel_z_exp` | 0.3741 |
| Mean episode length | 982.37 |
| Mean action std | 0.57 |
| Timeout | 96.18% |
| Base contact | 3.82% |
| Value loss | 0.0201 |

iteration 4999에서는 reward가 다시 21.08 정도였고, 즉 **4900은 단순히 “마지막 checkpoint”가 아니라 recovery 구간의 자동 best에 가까운 checkpoint**다.

## 3.3 4300의 위치

원본 run의 `model_best.pt`를 forensic으로 확인했을 때 exact checkpoint는 `model_4300.pt`였다.

- 원본 최고 instantaneous reward: 약 iteration 4284
- checkpoint 저장 간격: 100
- `model_4300.pt`가 그 best window를 대표
- `model_4300.pt` SHA-256:

```text
82efb1a59bfad74c5b03b7584fe7cf27865dcd0603550f11340c4134c6a802c8
```

4300은 “최종 제출 후보”라기보다 **원본 학습의 공식적인 중간 기준점**으로 의미가 있다.

---

# 4. checkpoint 내부 변화 분석

actor parameter 기준 상대 변화:

| 비교 | Relative L2 | Cosine similarity | 해석 |
|---|---:|---:|---|
| 4300 → 4800 | 18.75% | 0.98339 | 원본 후반부에서 의미 있는 정책 변화 |
| 4800 → 4900 | 9.83% | 0.99524 | recovery 100 iter 동안 미세하지만 실제적인 fine-tuning |
| 4300 → 4900 | 20.97% | 0.97951 | 4300과 4900 사이에는 누적된 변화가 분명함 |

action-distribution std 평균:

| Model | Mean std |
|---|---:|
| 4300 | 0.6378 |
| 4800 | 0.6636 |
| 4900 | 0.5653 |

해석:

- 4800은 4300보다 탐색 분산이 약간 더 크다.
- 4900은 recovery 후 std가 뚜렷하게 낮아진다.
- std가 낮아졌다는 사실만으로 “더 안정적”이라고 판단하면 안 된다.
- 실제 controlled benchmark에서는 오히려 4900의 낙상률이 더 높았다.
- 따라서 **action std는 탐색/분포 폭의 단서이지 robustness의 대체 지표가 아니다.**

---

# 5. 통제 정량 벤치마크 설계

최종 모델 선택을 학습 reward 하나로 하지 않기 위해 별도의 inference-only controlled benchmark를 수행했다.

## 5.1 환경

- GPU: NVIDIA L40S
- Isaac Sim: 5.1.0-rc.19+
- IsaacLab commit: `3e73d6dd79080fd7632488c061052a6edd52e230`
- task repository commit: `92835ec73b980900581e29e241c46691882f779a`
- PPO update 없음
- deterministic inference
- observation corruption OFF
- curriculum OFF
- command 고정:
  - `vx = 1.0`
  - `vy = 0.0`
  - `yaw_rate = 0.0`
- seed: 4201
- difficulty: 1.0
- terrain당 64 environments
- 모델: 4300 / 4800 / 4900
- terrain 6종:
  - stairs
  - inverted stairs
  - boxes
  - random rough
  - +20° slope
  - -20° slope

총 조건:

```text
3 models × 6 terrains × 64 envs = 1,152 episodes
```

## 5.2 측정한 핵심 지표

- timeout survival rate
- base-contact fall rate
- survival time
- episodic return
- body-frame XY velocity RMSE
- yaw-rate RMSE
- +X displacement
- XY displacement
- action-rate²
- torque² proxy
- base height / tilt

중요한 해석 규칙:

- timeout survival ≠ traversal success
- yaw-rate RMSE ≠ heading error
- torque² ≠ 실제 에너지 소비량
- world-Z base height는 terrain-relative clearance가 아님
- 단일 seed의 64 parallel env는 64개의 완전 독립적인 seed 실험과 동일하지 않음

---

# 6. 전체 정량 결과

6개 terrain을 동일 가중 평균했을 때:

| 지표 | 4300 | **4800** | 4900 | 좋은 방향 |
|---|---:|---:|---:|---|
| Timeout survival | 96.61% | **98.18%** | 94.01% | ↑ |
| Base-contact fall | 3.39% | **1.82%** | 5.99% | ↓ |
| Fall count / 384 | 13 | **7** | 23 | ↓ |
| Survival time (s) | 19.56 | **19.80** | 19.46 | ↑ |
| Return | 28.03 | 28.48 | **28.95** | ↑ |
| XY RMSE | 0.456 | 0.443 | **0.410** | ↓ |
| Yaw-rate RMSE | 0.135 | **0.102** | 0.110 | ↓ |
| +X progress | 11.58 | 12.11 | **12.56** | ↑ |
| Action-rate² | 0.158 | **0.142** | 0.179 | ↓ |

가장 중요한 패턴은 명확하다.

> **4800은 robustness가 가장 좋고, 4900은 tracking/progress가 가장 좋다.**

즉 4900은 단순한 “더 좋은 4800”이 아니다. 성능축이 달라진 checkpoint다.

---

# 7. 4800 vs 4900 낙상 비교

동일 환경 조건을 matching하여 4800과 4900을 비교했을 때:

- 4800에서만 fall: 7
- 4900에서만 fall: 23
- 둘 다 fall: 0
- 둘 다 survive: 354

방향성 자체는 4800에 매우 유리하다.

참고 수준의 matched comparison에서 p-value가 약 0.005 수준으로 나왔지만, 이 값은 **single seed + parallel env 간 상관 가능성** 때문에 엄격한 독립표본 통계 검정처럼 과장하면 안 된다.

보고서에서는 다음처럼 쓰는 것이 안전하다.

> 동일한 환경 인덱스를 기준으로 비교했을 때 4900에서만 실패한 사례가 4800에서만 실패한 사례보다 크게 많아, robustness 측면에서 4800 우위의 방향성이 뚜렷했다.

---

# 8. terrain별 정량 심층 분석

## 8.1 Boxes

| 모델 | Fall | Survival | XY RMSE | +X |
|---|---:|---:|---:|---:|
| 4300 | 5/64 | 92.19% | 0.658 | 8.52 |
| **4800** | **3/64** | **95.31%** | 0.596 | 9.78 |
| 4900 | 11/64 | 82.81% | **0.502** | **11.06** |

해석:

- 4900은 명령 추종과 전진거리 자체는 가장 좋다.
- 그러나 fall이 4800의 약 3.7배이다.
- 이 terrain은 “공격적으로 전진하는 policy”가 “실패하지 않는 policy”와 다를 수 있음을 가장 잘 보여준다.
- 최종 제출에서 한 번의 낙상이 큰 손실이라면 4800이 실용적으로 더 매력적이다.

## 8.2 Stairs

낙상:

- 4300: 8/64
- **4800: 4/64**
- 4900: 9/64

전진:

- 4300: 7.30 m
- 4800: 7.37 m
- **4900: 7.97 m**

도달거리 분포에서는 4900이 5m 이상 진행하는 사례가 많아 **초기 돌파력/공격성**이 강하게 나타났다. 그러나 10m 이상 장거리 traversal 비율에서는 압도적 우위로 이어지지 않았다.

해석:

> 4900은 계단에서 더 적극적으로 진입할 가능성이 있지만, 그 적극성이 완주율 또는 생존성 향상으로 연결됐다고 보기 어렵다.

## 8.3 Inverted stairs

timeout survival:

- 4300: 100%
- 4800: 100%
- 4900: 95.3%

그러나 +X progress:

- 4300: 1.17 m
- 4800: 1.16 m
- 4900: 2.28 m

이 결과는 매우 중요하다.

> “20초를 버텼다”는 사실은 “계단을 내려갔다”는 뜻이 아니다.

4300/4800은 거의 이동하지 않은 채 살아남는 경우가 많아 **timeout survival을 success로 부르면 안 된다.**

4900은 상대적으로 진행성은 증가했지만 여전히 inverted-stairs traversal을 잘 해결했다고 부르기 어렵다.

## 8.4 Random rough

- fall: 세 모델 모두 0
- XY RMSE: 0.170 / 0.162 / **0.152**
- return: 35.82 / 36.16 / **37.69**
- +X: 18.46 / 16.83 / **18.82**
- torque²: 31.15 / 33.34 / **27.04**

이 terrain은 4900의 장점이 가장 잘 보인다.

다만 4800은 body-frame 추종 지표에 비해 world +X가 낮았고 XY displacement와의 차이를 보면 lateral drift/heading drift 가능성이 있었다.

여기서 얻은 중요한 측정 교훈:

> body-frame velocity tracking이 좋아도 world-frame 목표 방향으로 똑바로 간다는 보장은 없다.

따라서 향후 evaluator에는 **heading error, lateral displacement, forward-progress ratio**를 추가하는 것이 좋다.

## 8.5 +20° slope

세 모델 모두 survival은 좋았다.

+X:

- 4300: 14.91
- **4800: 18.22**
- 4900: 16.38

yaw-rate RMSE:

- 4300: 0.0946
- **4800: 0.0696**
- 4900: 0.0838

4800은 실용적인 uphill progress에서 강한 결과를 보였다.

## 8.6 -20° slope

세 모델 모두 생존했다.

특히 4900은 downhill에서 lateral deviation이 매우 작아 **직진성/방향 유지** 측면에서 강한 특성이 나타났다.

즉 4900은 “항상 불안정한 모델”이 아니라, terrain에 따라 우수한 locomotion 특성이 분명히 존재한다.

---

# 9. 6개 native 영상 검증

## 9.1 영상 생성 방법

영상은 새 renderer를 작성하는 대신 다음 기존 경로를 사용했다.

```text
external checkpoint
→ issacsimz play --checkpoint
→ 기존 training/quadruped/play.py
→ IsaacLab native play
→ 기존 robot-follow tracking camera
→ issacsimz evidence + validation
```

즉 실제 simulation/policy/video 핵심 로직은 기존 검증된 경로를 재사용했고, 별도 batch script는 반복 실행과 파일 보존만 담당했다.

## 9.2 provenance

4800 영상 source checkpoint:

```text
ea93f9b5b04d91a91d1cdb97c6d328978017991e0602745f9269c7190bfaba65
```

4900 영상 source checkpoint:

```text
250e430cbb74f837af15384c145e865f7c8d8155fc65a7fe8b21dda1c27514cd
```

모든 영상 run에서:

```text
validation.overall = PASS
source_identity = PASS
before/after hashes match
collection = PASS
```

즉 영상 생성 중 task source가 변조되지 않았음을 evidence에서 검증할 수 있다.

## 9.3 영상 파일 사양

모든 6개 영상:

- H.264
- 1920×1080
- 50 fps
- 999 frames
- 19.98 s

영상 SHA는 `final_videos/MANIFEST.tsv`, `SHA256SUMS`에 보존되어 있다.

## 9.4 영상 조건

고정된 항목:

- model
- seed = 4201
- num_envs = 1
- terrain type
- terrain grid 1×1
- horizontal_scale = 0.05
- 동일 native play
- 동일 camera system
- 동일 video length

고정되지 않은/controlled benchmark와 다른 항목:

- command `(vx, vy, yaw)`를 `(1, 0, 0)`으로 고정하지 않음
- curriculum을 OFF로 강제하지 않음
- difficulty를 1.0으로 강제하지 않음
- reward source snapshot은 native play 당시 기본 파일 값 1.0 / -3.0을 표시

따라서 영상의 올바른 용도는:

> **behavioral sanity check / qualitative validation**

이며,

> **controlled traversal benchmark**

라고 부르면 안 된다.

---

# 10. 영상 관찰 결과

## 10.1 Stairs

4800과 4900 모두 정상 gait를 유지하며 움직였다. 눈에 띄는 catastrophic failure는 없었다.

그러나 둘 다 계단을 정면으로 끝까지 횡단하는 강제 조건이 아니어서, 주로 계단 가장자리 주변을 지나고 이후 평지로 빠져나왔다.

따라서 영상만으로:

- 4800이 stairs를 “더 잘 오른다”
- 4900이 stairs를 “더 잘 오른다”

라고 결론내릴 수 없다.

정량 결과의 4800 낙상 우위를 뒤집는 시각적 증거도 없었다.

## 10.2 Boxes

세 terrain 중 실제 비교 가치가 가장 높았다.

초기 수 초 동안 실제 uneven box field 위에서 locomotion을 수행했고, 이후 평지로 빠졌다.

관찰상:

- 4900은 terrain interaction에서 다소 적극적인 반응을 보임
- 4800은 상대적으로 보수적인 trajectory
- 해당 단일 영상에서는 둘 다 낙상하지 않음

이 결과는 controlled benchmark의:

> 4900 = tracking/progress 우위  
> 4800 = fall robustness 우위

라는 해석과 충돌하지 않는다.

## 10.3 Inverted stairs

두 모델 모두 inverted stairs를 정면으로 내려가는 trajectory가 아니었다.

초기에는 stair 구조 근처에 있지만 곧 terrain 밖으로 빠져나오기 때문에, 이 영상으로 “inverted stairs traversal 능력”을 검증할 수 없다.

이 terrain은 오히려 **실험 설계 자체의 한계**를 보여주는 자료로 가치가 있다.

---

# 11. 영상 evidence에 reward가 1.0 / -3.0으로 보이는 이유

영상 evidence의 `quadruped_rewards.py`에는:

```text
track_lin_vel_xy_exp = 1.0
lin_vel_z_l2         = -3.0
ang_vel_xy_l2        = -0.08
```

가 기록되어 있다.

A1 학습값 1.5 / -2.0과 다르므로 처음 보면 checkpoint가 잘못된 것처럼 보일 수 있다.

그러나 inference-only play에서는 PPO update를 수행하지 않으므로 **현재 reward weight가 actor checkpoint의 action을 다시 학습시키지 않는다.**

즉:

```text
행동을 만드는 핵심 = checkpoint actor weights
play 환경 reward = inference 중 학습에 사용되지 않음
```

따라서 영상에서 4800/4900 checkpoint 자체의 행동 비교는 유효하다.

단:

> 이 영상 run에서 계산되는 reward를 A1 학습 reward와 직접 비교하면 안 된다.

보고서에서 이 점을 반드시 구분해야 한다.

---

# 12. 정량 + 영상 통합 판정

## 12.1 model_4800

강점:

- 전체 fall rate 최저: **1.82%, 7/384**
- 전체 survival 최고: **98.18%**
- stairs/boxes에서 4900보다 명확히 낮은 fall count
- action-rate² 최저 → 상대적으로 smoother action
- +20° uphill에서 매우 강한 practical progress
- 영상에서 locomotion이 지나치게 굼뜨거나 붕괴된 증거 없음

약점:

- 4900보다 평균 XY tracking과 +X progress가 약간 낮음
- random rough에서 world-direction drift 가능성
- inverted stairs 문제를 해결한 모델은 아님

## 12.2 model_4900

강점:

- 전체 return 최고
- XY RMSE 최고
- +X progress 최고
- random rough에서 강한 성능
- 일부 terrain에서 방향성/직진성 장점
- 영상에서 정상적인 locomotion을 보임

약점:

- 전체 fall: **23/384, 5.99%**
- boxes: 11/64 fall
- stairs: 9/64 fall
- action-rate² 증가
- 진행성 증가가 robustness 비용과 함께 나타남
- 영상이 이 robustness 문제를 뒤집을 정도의 traversal 우위를 보여주지 못함

---

# 13. 최종 모델 선택

## 권고: `model_4800.pt`

최종 제출용 정책은 4800을 우선하는 것이 합리적이다.

결정 논리는 다음과 같다.

```text
4900의 이점
= tracking / progress / return

4800의 이점
= fall robustness / survival / smoother control

대회 제출 위험
= 한 번의 catastrophic fall이 평균 tracking 약간의 개선보다 더 큰 손실이 될 가능성

따라서
→ 4800
```

이 선택은 “4800의 reward가 높아서”도 아니고 “영상이 더 예뻐서”도 아니다.

> **가장 중요한 근거는 통제된 1,152-episode benchmark에서 확인된 failure-risk 차이이며, 영상은 그 선택에 반하는 심각한 행동 이상이 없음을 확인하는 보조 근거다.**

---

# 14. Evidence hierarchy — 보고서에서 근거의 무게를 다르게 둬야 하는 이유

근거는 같은 수준이 아니다.

## Level A — 가장 강한 모델 선택 근거

- controlled inference benchmark
- 동일 seed/command/difficulty
- curriculum OFF
- deterministic policy
- 동일 6 terrain
- 64 env × 3 model
- fall/progress/tracking 직접 비교

## Level B — checkpoint forensic

- exact SHA
- actor parameter similarity
- policy.pt ↔ checkpoint actor match
- original model_best ↔ model4300 exact match
- resume lineage 확인

## Level C — qualitative video

- 실제 gait 확인
- 비정상 자세/정지/local optimum 확인
- terrain interaction 관찰
- 단, command/difficulty 완전 통제 아님

## Level D — training reward/log

- candidate screening에 유용
- 하지만 curriculum 변화, critic spike, stochastic training 때문에 최종 모델 선택 근거로 단독 사용하면 위험

---

# 15. 보고서에서 피해야 하는 잘못된 주장

다음 표현은 쓰지 않는 것이 좋다.

### 잘못된 표현
“4900이 reward가 높으므로 가장 좋은 모델이다.”

### 개선
“4900은 평균 return과 tracking/progress에서 우수했으나, controlled benchmark에서 낙상률이 증가해 최종 모델은 robustness가 높은 4800을 선택했다.”

---

### 잘못된 표현
“4800은 inverted stairs 성공률 100%다.”

### 개선
“4800은 inverted stairs에서 timeout까지 생존한 비율은 높았지만 전진거리가 약 1.16m에 그쳐, 생존을 traversal success로 해석할 수 없었다.”

---

### 잘못된 표현
“영상에서 계단을 잘 통과했다.”

### 개선
“영상은 계단 terrain에서 정상 gait를 확인하는 qualitative validation으로 사용했으며, command 방향이 고정되지 않아 full traversal 시험으로는 사용하지 않았다.”

---

### 잘못된 표현
“4900은 불안정하고 나쁜 모델이다.”

### 개선
“4900은 tracking/progress가 강한 대신 boxes/stairs의 fall risk가 증가한 공격적 정책이었다.”

---

### 잘못된 표현
“value loss spike 때문에 policy가 망가졌다.”

### 개선
“critic value loss spike가 관찰됐지만 이후 회복되었고, deployed actor 품질은 별도의 inference benchmark로 검증했다.”

---

# 16. 이번 프로젝트에서 배운 RL 핵심 개념

## 16.1 Reward는 목표가 아니라 proxy다

로봇은 사람이 의도한 “잘 걷기”를 직접 이해하지 않는다.

정책은 reward function을 최적화한다.

따라서:

- survival reward → 안 움직이는 전략
- velocity reward → 불안정한 과속
- strong stability penalty → 지나치게 보수적인 gait
- high feet-air reward → 비정상 bounding

같은 reward hacking / proxy mismatch가 발생할 수 있다.

## 16.2 평균 reward 하나로 모델을 선택하면 위험하다

reward는 여러 항목의 합이며, 환경 curriculum과 episode composition에 따라 분포가 바뀐다.

같은 reward라도:

- 더 어려운 지형에서 받은 reward인지
- 쉬운 지형에서 안정적으로 받은 reward인지
- 실패를 감수하면서 tracking을 높인 reward인지

가 다를 수 있다.

## 16.3 “살아 있음”과 “task 성공”을 분리해야 한다

inverted stairs가 대표 사례다.

timeout survival이 100%에 가까워도 forward progress가 거의 0이면 navigation/traversal 관점에서는 실패다.

따라서 여러 metric을 동시에 사용해야 한다.

## 16.4 Body-frame metric과 world-frame 목표는 다르다

body-frame velocity tracking이 좋더라도 robot heading이 틀어지면 world +X progress가 낮을 수 있다.

향후:

- heading error
- lateral drift
- forward progress ratio

가 필요하다.

## 16.5 더 오래 학습한다고 항상 좋아지지 않는다

4800 → 4900에서:

- tracking/progress 향상
- std 감소
- return 증가

가 나타났지만,

- fall risk 증가

도 같이 나타났다.

즉 late training은 Pareto trade-off를 다른 방향으로 이동시킬 수 있다.

## 16.6 Checkpoint 선택은 multi-objective decision이다

“best”는 하나의 scalar가 아니다.

실제 제출에서는:

- robustness
- progress
- tracking
- smoothness
- terrain coverage
- catastrophic failure

사이의 우선순위를 정해야 한다.

---

# 17. 실험 방법론 측면에서 잘한 점

이 프로젝트에서 기록서에 강조하기 좋은 부분은 단순히 RL 코드를 실행한 것이 아니다.

## 17.1 가설 기반 reward 수정

임의로 많은 reward를 한꺼번에 바꾸지 않고 “전진 추종 강화 + vertical penalty 완화”라는 명시적인 성격 변화 가설을 세웠다.

## 17.2 실패 실험도 폐기하지 않음

G5 같은 negative result를 “망한 실행”으로 버리지 않고 survival local optimum 사례로 해석했다.

## 17.3 checkpoint를 중간중간 비교

최종 iteration만 보지 않고 4300/4800/4900을 각각 별도 후보로 취급했다.

## 17.4 학습과 평가를 분리

PPO update를 끈 deterministic inference benchmark를 만들어 training dynamics의 영향을 제거했다.

## 17.5 하나의 metric을 맹신하지 않음

reward, terrain level, episode length, std, fall, tracking RMSE, displacement, action rate, 영상 관찰을 종합했다.

## 17.6 재현성과 provenance 관리

checkpoint와 video SHA-256을 기록하고, task source before/after hash까지 검증했다.

## 17.7 실험의 한계를 스스로 찾아냄

영상이 정상 생성됐다는 사실에 만족하지 않고 “실제로 계단을 횡단하는 영상인가?”를 별도로 판단하여 qualitative evidence의 한계를 명시했다.

이것은 연구/공학 활동에서 매우 중요한 태도다.

---

# 18. 학습 기록서/활동 기록서에 쓰기 좋은 핵심 스토리

가장 좋은 서사는 “강화학습을 돌렸다”가 아니라 다음 흐름이다.

> 사족보행 로봇의 속도와 안정성 사이의 trade-off를 reward shaping 문제로 정의하고, reward 계수를 조정한 정책을 장시간 학습하였다. 학습 reward만으로 성능을 판단할 경우 잘못된 결론이 날 수 있다고 보고, 여러 checkpoint를 동일 조건에서 deterministic inference로 재평가하였다. 1,152개의 episode에서 낙상률·속도 추종 오차·전진거리·action smoothness를 함께 비교한 결과, 더 늦은 checkpoint가 tracking은 우수하지만 낙상률도 증가한다는 사실을 확인하였다. 또한 영상과 수치 결과를 교차 검증하면서 timeout survival이 실제 지형 통과 성공과 다르다는 점, body-frame velocity가 world-frame 방향성까지 보장하지 않는다는 점을 발견하였다. 최종적으로 높은 평균 reward 대신 robustness가 높은 checkpoint를 선택했으며, SHA-256과 source identity를 활용해 실험 결과의 재현성과 provenance도 관리하였다.

이 스토리는 다음 역량을 동시에 보여준다.

- 강화학습 이해
- 실험 설계
- 데이터 분석
- 실패 분석
- 통계적 사고
- simulation engineering
- reproducibility
- evidence management
- 비판적 해석
- 의사결정

---

# 19. 학습 기록서용 문장 예시

## 19.1 짧은 버전

> Isaac Sim 기반 Go2 사족보행 강화학습에서 reward shaping을 통해 속도와 안정성의 trade-off를 탐구하였다. 학습 reward만으로 모델을 선택하지 않고, 서로 다른 checkpoint를 동일한 명령·난이도에서 1,152회 inference 평가하여 낙상률과 추종 오차를 비교하였다. 더 늦게 학습한 모델이 tracking 성능은 향상됐지만 낙상 위험도 증가한다는 사실을 확인하고, 최종적으로 robustness가 높은 checkpoint를 선택하였다.

## 19.2 탐구 과정 강조 버전

> 초기에는 평균 reward와 terrain level을 중심으로 학습 상태를 판단했으나, reward가 높은 checkpoint가 실제로 더 안전한지 의문을 제기하였다. 이에 PPO 학습을 중단한 deterministic evaluation 환경을 별도로 구성해 3개 checkpoint를 6종 terrain에서 비교하였다. 평가 과정에서 timeout survival이 실제 지형 통과 성공과 다를 수 있다는 문제를 발견하여 displacement와 fall을 함께 해석했고, 정량 결과를 영상으로 다시 검증하였다. 이를 통해 강화학습의 scalar reward를 그대로 성능으로 해석하는 한계를 경험적으로 이해하였다.

## 19.3 공학/재현성 강조 버전

> 장시간 강화학습 실험에서 checkpoint와 실행 환경의 혼동을 방지하기 위해 SHA-256 기반 provenance 체계를 적용하였다. 학습 중단 후 resume 과정에서는 curriculum state reset으로 인해 terrain level을 직접 비교할 수 없음을 확인하고, 대신 checkpoint 자체를 동일한 inference 조건에서 재평가하였다. 영상 생성에서도 source identity의 before/after hash를 검증해 코드 변경 없이 동일 환경에서 실행됐음을 확인하였다.

## 19.4 문제 해결 강조 버전

> 영상 검증 중 headless 환경에서 camera tracking 오류와 고정 카메라의 시야 이탈 문제를 경험하였다. 새로운 렌더러를 계속 수정하기보다 기존에 검증된 native play wrapper를 재사용하는 방식으로 방향을 전환하였다. 외부 checkpoint를 정확히 staging하고 영상과 source checkpoint의 SHA를 연결하여 6개의 비교 영상을 정상 생성하였다. 이 과정에서 새 기능을 추가하는 것보다 검증된 시스템의 재사용이 오류 가능성을 줄이는 공학적 선택임을 배웠다.

---

# 20. 자기평가/성찰에 쓰기 좋은 내용

이번 활동에서 가장 의미 있는 변화는 **“좋아 보이는 결과를 찾는 것”에서 “틀린 해석을 피하는 것”으로 분석 관점이 바뀐 것**이다.

초기에는:

- reward 상승
- terrain level 상승
- std 감소

같은 하나의 지표가 좋아지면 모델이 개선됐다고 생각하기 쉽다.

그러나 실제 비교를 통해:

- reward ↑ + fall ↑
- survival ↑ + progress 거의 0
- body-frame tracking ↑ + world drift
- longer training + robustness ↓

가 동시에 발생할 수 있음을 확인했다.

따라서 최종적으로는 “어떤 숫자가 가장 큰가?”가 아니라:

> **평가 목적에 맞는 metric을 설계하고 여러 근거가 서로 같은 결론을 지지하는지 확인하는 것**

이 중요하다는 점을 배웠다고 정리할 수 있다.

---

# 21. 기술적으로 강조할 만한 키워드

기록서/발표에서 자연스럽게 사용할 수 있는 용어:

- reinforcement learning
- reward shaping
- locomotion policy
- PPO
- deterministic inference
- curriculum learning
- checkpoint selection
- policy robustness
- velocity tracking
- catastrophic failure
- reward hacking
- local optimum
- multi-objective optimization
- Pareto trade-off
- domain-specific evaluation metric
- world-frame / body-frame
- lateral drift
- heading error
- provenance
- SHA-256
- reproducibility
- source identity
- ablation-style comparison
- qualitative / quantitative cross-validation

단, 용어를 나열하기보다 실제로 한 행동과 연결해서 쓰는 것이 좋다.

---

# 22. 발표/면접에서 받을 수 있는 질문과 답변 포인트

## Q. 왜 reward가 더 높은 4900이 아니라 4800을 선택했나?

> reward는 여러 목적의 합성 지표이며 실제 낙상 위험을 완전히 표현하지 못했다. 통제 평가에서 4800의 fall이 7/384, 4900은 23/384로 차이가 컸다. 4900의 tracking 향상보다 catastrophic failure risk를 더 중요하게 보아 4800을 선택했다.

## Q. 4900이 더 오래 학습했는데 왜 더 나빠질 수 있나?

> PPO는 하나의 multi-objective reward를 계속 최적화한다. 후반 학습에서 tracking/progress 방향으로 policy가 이동하면서 robustness를 일부 잃을 수 있다. 더 많은 iteration이 모든 metric의 단조 개선을 보장하지 않는다.

## Q. 영상에서도 4800이 확실히 더 좋은가?

> 영상은 qualitative sanity check로 사용했다. 두 모델 모두 정상 gait였고 4900의 공격적인 움직임도 확인됐지만, command와 difficulty를 완전히 고정한 traversal 시험은 아니었다. 따라서 최종 선택 근거는 영상보다 controlled benchmark에 더 큰 가중치를 두었다.

## Q. inverted stairs survival 100%면 성공 아닌가?

> 아니다. 4800의 평균 전진이 약 1.16m뿐이어서 대부분 실제로 통과하지 못했다. 그래서 timeout survival을 traversal success와 분리해 해석했다.

## Q. 왜 64 env를 썼나?

> 동일 terrain 조건에서 다양한 procedural instance를 병렬 평가해 단일 영상이나 단일 rollout의 우연성을 줄이기 위해서다. 다만 single seed parallel env이므로 완전 독립 반복실험으로 과장하지 않았다.

## Q. critic value loss spike가 있었는데 괜찮나?

> critic은 학습 중 return estimation을 담당하지만 제출 시 actor가 행동을 생성한다. spike 자체는 진단 신호이지만 actor failure의 직접 증거는 아니다. 실제 actor는 별도 inference benchmark로 평가했다.

## Q. SHA-256을 왜 사용했나?

> 이름이 같은 파일이나 staging 과정에서 checkpoint가 바뀌는 문제를 방지하고, 영상/분석 결과가 정확히 어떤 모델에서 생성됐는지 검증하기 위해서다.

---

# 23. 다음 실험에서 개선할 점

## 23.1 진짜 traversal video

다음 영상 평가에서는 반드시:

- `vx = 1.0`
- `vy = 0`
- `yaw = 0`
- curriculum OFF
- difficulty = 1.0
- robot heading 고정
- terrain travel axis와 robot heading 정렬

을 사용해야 한다.

이렇게 해야 “stairs video”가 실제 stairs traversal 증거가 된다.

## 23.2 evaluator metric 추가

다음 evaluator에서 추천:

### Heading error
로봇의 body heading과 목표 world direction 차이.

### Lateral displacement
목표 진행축과 직교하는 방향의 drift.

### Forward progress ratio

```text
forward displacement / total XY displacement
```

1에 가까우면 목표 방향으로 곧게 진행한 것.

### Terrain traversal completion
특정 obstacle zone의 끝선을 통과했는지 여부.

### Recovery metric
충격/접촉 후 일정 시간 내 body orientation과 velocity가 정상범위로 회복됐는지.

## 23.3 여러 seed 반복

현재 4201 seed 결과를 기반으로 하되:

- 4202
- 4203
- 4204

등을 추가하면 robustness 결론의 통계적 신뢰도가 더 높아진다.

---

# 24. 공식 보고서와 내부 학습 기록을 반드시 구분할 것

이 프로젝트에서는 evidence 출처를 구분하는 것이 매우 중요하다.

## 공식 서버에서 실제 얻은 것

- 공식 학습 run
- checkpoint
- native training log
- official-server provenance

## 개인/Brev 내부 검증

- 1,152-episode controlled benchmark
- 4800/4900 visual comparison
- 추가 forensic
- evaluator-derived metric

따라서 대회 공식 보고서에서 내부 결과를 쓸 경우에는 반드시:

> “개인 검증 환경에서 수행한 내부 비교”

라고 표시해야 한다.

공식 서버에서 측정한 결과처럼 표현하면 안 된다.

반대로 **학교 학습 기록서/동아리 연구 기록**에서는 개인 검증 실험 자체가 중요한 학습 활동이므로 충분히 상세히 써도 된다.

---

# 25. 최종 결론

이번 A1 실험은 “reward를 바꿨더니 더 잘 걸었다” 수준의 단순한 실험이 아니다.

핵심 결과는 다음과 같다.

1. A1 reward shaping은 baseline보다 적극적인 locomotion 성격을 만들기 위한 시도였다.
2. 학습 후반 checkpoint 4900은 tracking·progress·return 측면에서 강해졌다.
3. 그러나 동일 조건 controlled benchmark에서는 4800이 훨씬 낮은 fall risk를 보였다.
4. 더 오래 학습한 모델이 모든 성능축에서 좋아지는 것은 아니었다.
5. survival, reward, terrain level, std 중 어느 하나도 task success의 완전한 대리변수가 아니었다.
6. 영상 검증은 policy가 실제로 정상 gait를 보이는지 확인하는 데 유용했지만, 실험 설계상 traversal 성능의 직접 증거는 아니었다.
7. 최종 모델 선택은 scalar reward가 아니라 **robustness와 catastrophic failure risk를 중심으로 한 multi-objective decision**으로 수행했다.
8. 결과의 신뢰성을 높이기 위해 checkpoint/video SHA, source identity, evidence run을 연결하여 provenance를 관리했다.

최종 권고:

```text
PRIMARY SUBMISSION CANDIDATE: model_4800.pt
SECONDARY / AGGRESSIVE CANDIDATE: model_4900.pt
REFERENCE: model_4300.pt
```

4800을 선택하는 가장 압축된 한 문장은 다음과 같다.

> **4900은 더 잘 추종하고 더 멀리 가는 경향이 있었지만, 4800은 훨씬 적게 넘어졌으며 영상에서도 심각한 locomotion 열화가 관찰되지 않았기 때문에, 실제 제출 위험을 고려하면 4800이 더 균형 잡힌 최종 정책이다.**

---

# Appendix A. 핵심 SHA-256

```text
model_4300.pt
82efb1a59bfad74c5b03b7584fe7cf27865dcd0603550f11340c4134c6a802c8

model_4800.pt
ea93f9b5b04d91a91d1cdb97c6d328978017991e0602745f9269c7190bfaba65

model_4900.pt
250e430cbb74f837af15384c145e865f7c8d8155fc65a7fe8b21dda1c27514cd
```

# Appendix B. 최종 영상 manifest 핵심

| Model | Terrain | Duration | Frames | Video SHA-256 |
|---|---|---:|---:|---|
| 4800 | stairs | 19.98 s | 999 | `b34b4c1d50e7a8b9f365d4458c11799a7d294307bf70375e483b08bd417461cd` |
| 4800 | boxes | 19.98 s | 999 | `351e205962806ec5e24b0a5facb1f54d3752a3b74404c13c8cabafb107a515fd` |
| 4800 | inverted_stairs | 19.98 s | 999 | `2aa538718d11d7326c2b13f063d3cb657e1b76500bab81c73f268b426f526d34` |
| 4900 | stairs | 19.98 s | 999 | `28029002e245b9aab360ed5c7c418d4396e0d2c70ce2c1ad0d99f00df4de7a01` |
| 4900 | boxes | 19.98 s | 999 | `273502d1f0259f93c785abf08e88c03083927dfc03ff3ed08490f4ed1c0c6cc4` |
| 4900 | inverted_stairs | 19.98 s | 999 | `7b24d69850629d62a52636b9995364173763ff8a29ad54cb1e9acf96e2bb3f0c` |

# Appendix C. 학습 기록서용 초압축 요약

> Go2 사족보행 강화학습에서 속도와 안정성의 trade-off를 reward shaping으로 탐구하였다. 5000 iteration 학습 과정의 여러 checkpoint를 비교하면서 학습 reward가 높은 모델이 항상 실제 task 성능도 우수한지 의문을 제기했고, 별도의 deterministic inference benchmark를 구성하여 3개 checkpoint를 6종 terrain에서 총 1,152 episode 평가하였다. 그 결과 후기 checkpoint는 velocity tracking과 진행성이 향상됐지만 낙상률도 증가했으며, timeout 생존률이 실제 장애물 통과 성공을 의미하지 않는 사례도 확인하였다. 정량 결과와 native simulation 영상을 교차 검증하여 최종적으로 robustness가 높은 4800 checkpoint를 선택했고, SHA-256 기반 provenance 관리로 실험 결과의 재현성을 확보하였다.
