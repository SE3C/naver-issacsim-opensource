> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/incoming/other/reviewed/GO2_A1_MODEL_4800_DEEP_ANALYSIS_20260915.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# Go2 A1 `model_4800.pt` 매우 심층 분석

작성 기준: 2026-09-15\
대상: 공식 서버 A1 fresh run의 `model_4800.pt`\
분석 목적: 4800을 “중단 직전 fallback” 이상으로 해석하고, 4300과 비교해 실제 capability가 어떻게 변했는지, 4900 recovery의 source로서 어떤 의미가 있는지 평가한다.

---

## 0. 한 줄 결론

`model_4800.pt`는 원본 fresh run의 자동 reward-best는 아니지만, **4300 이후 계속 상승한 curriculum을 따라가면서 XY tracking을 개선한 후기 정책**이다. 동시에 reward variance·action std·motion penalty·critic instability가 커진 흔적이 있어, 세 후보 중 가장 “공격적이고 거친 late-policy”에 가깝다. 4900이 정말 개선된 정책인지 판별하려면 4800이 가장 중요한 직접 대조군이다.

---

# 1. Provenance와 체크포인트 무결성

```text
checkpoint:
model_4800.pt

SHA-256:
ea93f9b5b04d91a91d1cdb97c6d328978017991e0602745f9269c7190bfaba65
```

원본 run:

```text
20260914-084321-go2-a1-tracklin150-lvz-m2-5k-official
```

이 checkpoint는 공식 서버 fresh A1 run에서 직접 생성됐다.

원본 run은 iteration 4837 부근에서 중단되었지만 `model_4800.pt`는 중단 전에 정상 저장되고 issacsimz evidence mirror에도 보존되었다.

후속 recovery metadata가 source checkpoint를 다음 SHA로 명시한다.

```text
resume_source=model_4800.pt
resume_source_sha256=
ea93f9b5b04d91a91d1cdb97c6d328978017991e0602745f9269c7190bfaba65
```

즉 recovery 4900의 계보가 이 4800으로 cryptographic하게 연결된다.

---

# 2. 4800의 핵심 의미

4800은 자동 `model_best`가 아니다.

원본 reward peak는 4284였고 old best artifact는 4300과 일치한다.

그럼에도 4800이 중요한 이유는:

1. 4300 이후에도 curriculum이 계속 상승함
2. 4800에서 terrain이 더 높아짐
3. XY tracking이 4300보다 좋아짐
4. recovery가 이 checkpoint에서 출발함
5. 중단 직전까지의 fresh-run capability를 가장 잘 대표하는 보존 checkpoint 중 하나임

이다.

즉 4800은:

> **reward optimum이 아니라 capability progression 후보**

다.

---

# 3. iteration 4800 순간 상태

| 지표 | 값 |
|---|---:|
| Mean reward | **20.14** |
| Terrain level | **5.7367** |
| XY velocity error | **0.5017** |
| Yaw-rate error | **0.4278** |
| Mean episode length | **968.01** |
| Timeout termination | **91.89%** |
| Base-contact termination | **8.11%** |
| Action std | **0.66** |
| Mean value loss | **0.0259** |
| Mean surrogate loss | **-0.0108** |
| Entropy loss | **11.6877** |

Reward component:

| 항목 | 값 |
|---|---:|
| `track_lin_vel_xy_exp` | +1.1642 |
| `track_ang_vel_z_exp` | +0.5762 |
| `lin_vel_z_l2` | -0.0482 |
| `ang_vel_xy_l2` | -0.2016 |
| `dof_torques_l2` | -0.1216 |
| `dof_acc_l2` | -0.2223 |
| `action_rate_l2` | -0.1454 |
| `feet_air_time` | -0.0013 |

4800 순간값만 보면 매우 정상적이다. 특히 value loss가 낮고 XY error가 4300보다 좋다.

하지만 한 점만 보면 4800의 실제 특징을 놓친다.

---

# 4. 직전 20 iteration: 4800의 가장 위험한 구간

```text
reward mean       17.997
reward std         6.796

terrain mean       5.7152
terrain slope      +0.00279 / iter

XY error mean      0.5693
base contact       7.88%

value-loss median  0.1905
value-loss max    20.2685
```

4300 직전 20회의 reward std가 0.68이었던 데 비해, 4800 직전 20회는 **6.80**이다.

즉 checkpoint 순간값 `reward=20.14`, `value loss=0.0259`만 보면 매우 안정적으로 보이지만, 실제 바로 전후 학습 상태는 상당히 거칠었다.

이 점은 4800의 가장 중요한 위험 신호다.

---

# 5. 직전 50 iteration

```text
reward mean       19.1272
reward std         4.3695
reward min       -10.00
reward max        21.43

terrain mean       5.6928
XY error mean      0.5547
yaw error mean     약 0.42
base contact       7.64%
timeout           92.36%
action std         0.654

value-loss median  0.0300
value-loss max    20.2685
```

중앙값 기준 critic은 평소 정상이다.

문제는 꼬리 분포다.

즉 4800 주변은:

> 대부분 정상 → 간헐적으로 매우 큰 shock

이라는 형태다.

이런 분포에서는 단일 endpoint만 보고 안정성을 판단하면 안 된다.

---

# 6. 직전 100 iteration

```text
reward mean       19.2874
reward std         3.1388

terrain mean       5.6774
terrain trend      상승

XY error mean      0.5782
base contact       7.32%

value-loss median  0.0329
value-loss max    20.2685
```

100회로 넓혀도 terrain은 계속 상승하고, base-contact 평균은 4300 주변보다 나쁘지 않다.

즉 4800의 후기 구간이 전체적으로 붕괴하고 있었던 것은 아니다.

정확한 해석은:

> **능력은 계속 확장되고 있었지만 critic/reward variance가 커진 상태**

다.

---

# 7. 4300 대비 4800의 실제 변화

순간값:

| 지표 | 4300 | 4800 | 판정 |
|---|---:|---:|---|
| Reward | **20.65** | 20.14 | 4300 |
| Terrain | 5.5469 | **5.7367** | 4800 |
| XY error ↓ | 0.5636 | **0.5017** | 4800 |
| Yaw error ↓ | **0.3999** | 0.4278 | 4300 |
| Episode length | 951.37 | **968.01** | 4800 |
| Action std ↓ | **0.64** | 0.66 | 4300 |
| Base contact ↓ | **7.86%** | 8.11% | 근소 4300 |
| Value loss ↓ | 0.1777 | **0.0259** | 순간값은 4800 |

중요한 변화:

```text
terrain +3.42%
XY error -10.98%
episode length +1.75%
```

즉 4800은 확실히 더 높은 terrain을 다루면서 linear tracking을 개선했다.

이는 4300 이후 학습이 단순한 overtraining이었다는 가설과 맞지 않는다.

---

# 8. 운동 비용은 왜 악화됐는가

4300 → 4800 reward component 변화:

```text
lin_vel_z penalty
-0.0404 → -0.0482

ang_vel_xy penalty
-0.1862 → -0.2016

torque penalty
-0.1073 → -0.1216

dof_acc penalty
-0.2099 → -0.2223

action_rate penalty
-0.1346 → -0.1454
```

거의 모든 motion-cost가 더 커졌다.

동시에 terrain과 XY tracking은 좋아졌다.

가장 자연스러운 해석은:

> 더 어려운 terrain에서 tracking을 유지하기 위해 더 큰 몸통 움직임, 관절 가속, torque, action variation을 사용하는 방향으로 정책이 적응했다.

이다.

즉 4800은 4300보다 **aggressive locomotion** 성향일 가능성이 높다.

이것은 계단·rough에서 장점이 될 수도 있고, 진동·미끄러짐·착지 안정에서는 단점이 될 수도 있다.

---

# 9. 원본 fresh run 전체 critic instability 속에서 4800의 위치

원본 4838 iteration 전체:

```text
value loss > 1    : 352회
value loss > 5    : 110회
value loss > 10   : 70회
value loss > 50   : 14회
value loss > 100  : 9회

max:
283.8869 @ iter 3747
```

그 외 큰 spike:

```text
265.3461 @ 4415
171.8605 @ 1121
133.0419 @ 1369
111.3286 @ 3847
108.5940 @ 2031
103.6954 @ 2105
```

따라서 fresh A1 학습은 전체적으로 완전히 평온한 run은 아니다.

4800은 바로 이 장기 trajectory의 후기 정책이며, 4300 이후에도 4415 같은 대형 spike를 통과했다.

그럼에도:

- terrain이 계속 상승
- episode length 유지
- checkpoint tensor finite
- 4800 자체 value loss 정상

이라는 사실 때문에 **catastrophic divergence 직전 checkpoint라고 볼 근거는 없다.**

더 정확한 표현은:

> recurrent critic instability를 견디면서 capability가 계속 올라간 후기 정책

이다.

---

# 10. 4800 이후 중단 직전 38 iteration

4800~4837:

```text
reward mean       18.699
terrain mean       5.7230
XY error mean      0.6030
yaw error mean     0.4395
episode length   963.55
action std         0.6674
base contact       8.17%
timeout           91.84%

value-loss median  0.1886
value-loss max     3.5712
```

이 구간은 4800 checkpoint 직후 정책이 즉시 무너졌다는 증거는 아니다.

Terrain은 약 5.72 수준을 유지했다.

따라서 Ctrl+C가 없었다면 학습이 적어도 단기적으로 계속 진행될 여지는 있었다.

---

# 11. Actor/critic tensor 상태

4800 checkpoint:

```text
Actor parameters : 286,616
Actor NaN        : 0
Actor Inf        : 0

Critic parameters: 285,185
Critic NaN       : 0
Critic Inf       : 0
```

Actor:

```text
mean -0.000306
std   0.09458
min  -1.4591
max   1.7612
L2   50.6364
```

Critic:

```text
mean  0.002793
std   0.10166
min  -2.1417
max   1.3870
L2   54.3101
```

수치적으로 손상된 checkpoint가 아니다.

---

# 12. Action distribution

4800의 action std parameter 평균:

```text
0.66361
```

12차원 범위:

```text
min 0.42122
max 0.84629
```

세 후보:

```text
4300  0.6378
4800  0.6636
4900  0.5653
```

4800이 가장 높다.

이는 후기 curriculum에서 정책이 **더 넓은 action distribution**을 유지했다는 뜻이다.

좋게 보면 adaptation flexibility이고, 나쁘게 보면 행동 variability다.

고정 evaluator에서 seed 간 성능 분산까지 측정해야 하는 이유다.

---

# 13. 4300 → 4800 policy drift

Deterministic actor:

```text
parameters compared : 286,604
L2 delta            : 9.2055
relative L2 drift   : 18.75%
cosine similarity   : 0.98339
mean abs delta      : 0.01295
max abs delta       : 0.16542
```

500 iteration 동안 policy는 의미 있게 변했다.

따라서 4300과 4800을 “거의 같은 모델”로 생각하면 안 된다.

4800이 얻은 hard-terrain 적응은 실제 weight 변화와 함께 나타난다.

---

# 14. Recovery source로서의 4800

Recovery run은 metadata에서 명시적으로:

```text
--resume
--load_run a1-recovery-4800-source
--checkpoint model_4800.pt
```

를 사용했다.

source checkpoint hash도 original 4800과 정확히 일치한다.

따라서:

```text
original fresh A1
→ model_4800
→ official recovery
→ model_4900
```

계보가 명확하다.

이는 4900을 평가할 때 4800을 반드시 직접 비교해야 하는 이유다.

---

# 15. Recovery archive의 `model_4800.pt`와 original 4800을 혼동하면 안 됨

Recovery run 안에도 `model_4800.pt`가 존재하지만 이것은 source original 4800과 byte-identical하지 않다.

Resume 시작 후 iteration 4800 update/save가 다시 일어나기 때문이다.

따라서 “원본 4800”은 반드시:

```text
SHA:
ea93f9b5b04d91a91d1cdb97c6d328978017991e0602745f9269c7190bfaba65
```

를 기준으로 식별해야 한다.

최종 recovery bundle에 별도 fallback으로 이 원본 4800이 보존된 것은 중요한 장점이다.

---

# 16. 4800 → 4900에서 실제 policy는 얼마나 바뀌었나

Deterministic actor 기준:

```text
relative L2 drift = 9.83%
cosine similarity = 0.99524
```

4300→4800의 18.75% drift보다 훨씬 작다.

즉 4900은 4800의 hard-earned policy를 완전히 버린 새 모델이라기보다 **4800을 기반으로 한 refinement**에 가깝다.

이 점은 4900이 hard-terrain capability를 어느 정도 유지했을 가능성을 높이지만, 실제 성공률을 보장하지는 않는다.

---

# 17. 6 terrain에서 예상되는 4800의 검증 가설

아래는 측정치가 아니라 training evidence 기반 가설이다.

| Terrain | 4800 가설 |
|---|---|
| stairs | **세 후보 중 강한 후보**. 높은 curriculum exposure와 aggressive correction이 유리할 수 있음 |
| inverted stairs | 적극적인 자세 수정이 장점일 수 있으나 oscillation 위험 |
| boxes | hard-terrain exposure의 직접 장점이 나타날 가능성 |
| random rough | 4300보다 강할 가능성이 높음 |
| +20° slope | 4300보다 tracking/correction 능력이 좋을 가능성 |
| -20° slope | 큰 action variability가 오히려 불안정성을 만들 수 있음 |

4800의 핵심 검증 질문은:

> “높은 action variability와 motion cost가 실제 hard-terrain success로 보상되는가?”

이다.

---

# 18. 대회 시나리오 관점

4800은 특히 다음 시나리오에서 가치가 있을 가능성이 있다.

- rough terrain
- slope
- stairs
- push/recovery

반면 위험은:

- 전방위 command에서 jitter 증가
- downhill에서 지나친 correction
- 장애물 접촉 시 큰 동작
- seed에 따른 행동 편차

다.

즉 평균 성능뿐 아니라 **worst-case와 variance**가 중요하다.

---

# 19. 4800의 가장 강한 제출 논리

4800을 선택한다면 제출 논리는 다음처럼 구성할 수 있다.

> A1 reward 설계로 높은 curriculum까지 진행하면서 선속도 추종을 유지·개선했고, 후기 checkpoint는 원본 fresh lineage에서 가장 높은 terrain exposure를 가진 후보 중 하나였다.

이 논리는 reward peak 4300보다 “왜 4800인가?”를 설명할 수 있다.

하지만 반드시 fixed evaluator에서 hard-terrain 우위를 실제로 보여줘야 설득력이 완성된다.

---

# 20. 4800의 가장 큰 반대 논리

반대 논리는 명확하다.

> 후기 학습에서 reward variance와 critic instability가 커졌고 action std 및 motion penalties도 악화되었다. 더 높은 curriculum은 얻었지만 실제 대회 시나리오의 안정성까지 좋아졌다고 단정할 수 없다.

따라서 4800은 **training capability는 강하지만 제출 안정성은 아직 검증이 필요한 후보**다.

---

# 21. 정량 evaluator에서 4800에 요구할 것

4800이 4900을 이기려면 특히:

- stairs success
- rough success
- ±20° slope success
- worst-terrain success
- push recovery success

에서 4900보다 의미 있게 좋아야 한다.

4900이 survival/tracking/smoothness에서 이미 유리한 training evidence를 갖고 있기 때문이다.

반대로 hard-terrain success까지 4900이 같거나 좋다면 4800을 최종 제출할 이유는 크게 줄어든다.

---

# 22. 현재 판정

### 강점

- official fresh checkpoint
- 원본 4800 SHA 명확
- 4300보다 높은 curriculum
- 4300보다 좋은 XY tracking
- 긴 episode
- recovery 4900의 직접 source
- tensor finite
- hard-terrain candidate로 매우 중요

### 약점

- 자동 reward-best 아님
- 후기 reward variance 큼
- action std 세 후보 중 가장 높음
- motion penalties 악화
- critic spike가 반복된 장기 trajectory
- 고정 평가 없이는 높은 terrain이 실제 성공률 우위인지 알 수 없음

### 최종 등급

```text
Fresh-run provenance      : A
Hard-terrain exposure     : A
XY tracking evidence      : A-
Training stability        : B-
Numerical checkpoint      : A
Behavior smoothness prior : B
Submission readiness      : B+
```

---

# 23. 최종 요약

`model_4800.pt`는 “4300보다 reward가 낮으니 나쁜 checkpoint”가 아니다.

오히려 fresh trajectory에서:

> terrain을 더 높이고\
> XY tracking을 개선하면서\
> 더 적극적인 locomotion으로 이동한

후기 정책이다.

다만 그 대가로:

> reward variance\
> action std\
> torque/acc/action-rate 비용\
> critic instability

가 커졌다.

따라서 4800은 세 후보 중 **가장 높은 hard-terrain capability를 기대할 수 있는 동시에 가장 거친 정책일 가능성이 있는 후보**다.

그리고 4900이 바로 이 checkpoint에서 이어졌으므로, **4800 vs 4900 fixed benchmark가 이번 최종 선택의 가장 중요한 비교**다.
