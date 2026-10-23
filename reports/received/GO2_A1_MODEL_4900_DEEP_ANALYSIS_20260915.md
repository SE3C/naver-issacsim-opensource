> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/incoming/other/reviewed/GO2_A1_MODEL_4900_DEEP_ANALYSIS_20260915.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# Go2 A1 Recovery `model_4900.pt` 매우 심층 분석

작성 기준: 2026-09-15\
대상: original `model_4800.pt`에서 official resume한 recovery run의 `model_4900.pt`\
분석 목적: 4900의 높은 reward·낮은 낙상률·낮은 action std가 실제 policy 개선인지, curriculum reset 착시인지, 제출 후보로 얼마나 강한지 분리해 평가한다.

---

## 0. 한 줄 결론

`model_4900.pt`는 현재 세 후보 중 **artifact 완성도와 training-side 안정성, 생존성, yaw tracking, action smoothness가 가장 강한 후보**다. 최종 `policy.pt`가 4900 actor와 exact-match해 제출 계보도 깔끔하다. 그러나 best가 선택된 당시 curriculum 난이도가 4300/4800보다 낮았기 때문에, **고정 6-terrain benchmark에서 hard-terrain capability만 확인되면 사실상 최종 1순위로 확정할 수 있는 모델**이다.

---

# 1. Recovery provenance

Recovery run:

```text
run_id:
20260914-132725-go2-a1-tracklin150-lvz-m2-resume4800-to5k-offici
```

실행 구조:

```text
--max_iterations 200
--num_envs 4096
--resume
--load_run a1-recovery-4800-source
--checkpoint model_4800.pt
--headless
```

Source:

```text
original source checkpoint:
model_4800.pt

SHA-256:
ea93f9b5b04d91a91d1cdb97c6d328978017991e0602745f9269c7190bfaba65
```

Recovery metadata:

```text
status                    = completed
training_status           = completed
official_finalize_status  = completed
official_backup_status    = success
evidence_validation       = PASS
source_changed_during_run = false
```

즉 original interrupted run과 달리 recovery run은 정상 종료·finalize·backup까지 모두 완료됐다.

---

# 2. 4900 checkpoint 식별

```text
model_4900.pt

SHA-256:
250e430cbb74f837af15384c145e865f7c8d8155fc65a7fe8b21dda1c27514cd
```

Recovery export provenance에서:

```text
model_best.pt
SHA =
250e430cbb74f837af15384c145e865f7c8d8155fc65a7fe8b21dda1c27514cd
```

또 timestamp alias:

```text
model_best_20260914222728.pt
```

도 같은 SHA다.

따라서 recovery 자동 best는 실제 `model_4900.pt`다.

---

# 3. 최종 제출 `policy.pt`와 4900 연결

최종 handoff의 `policy.pt`:

```text
SHA-256:
22957506fefe1cde249548705fef30147fe149e1086c926ff447ff001c2cc277
```

TorchScript policy의 deterministic actor MLP parameter 8개를 checkpoint actor와 직접 비교한 결과:

```text
model_4300 : mismatch
model_4800 : mismatch
model_4900 : 8/8 exact-match
model_best : 8/8 exact-match
```

즉 현재 recovery 제출용 `policy.pt`는 **4900 actor에서 export된 정책**으로 확인된다.

이 점은 파일명 추정이 아니라 tensor-level forensic verification이다.

---

# 4. iteration 4900 순간 상태

| 지표 | 값 |
|---|---:|
| Mean reward | **24.40** |
| Terrain level | **4.6251** |
| XY velocity error | **0.5489** |
| Yaw-rate error | **0.3741** |
| Mean episode length | **982.37** |
| Timeout termination | **96.18%** |
| Base-contact termination | **3.82%** |
| Action std | **0.57** |
| Mean value loss | **0.0201** |
| Mean surrogate loss | **-0.0098** |
| Entropy loss | **9.6408** |

Reward component:

| 항목 | 값 |
|---|---:|
| `track_lin_vel_xy_exp` | +1.1910 |
| `track_ang_vel_z_exp` | +0.6170 |
| `lin_vel_z_l2` | -0.0389 |
| `ang_vel_xy_l2` | -0.1573 |
| `dof_torques_l2` | -0.1093 |
| `dof_acc_l2` | -0.1954 |
| `action_rate_l2` | -0.1187 |
| `feet_air_time` | -0.0013 |

4900의 순간값은 거의 모든 면에서 매우 좋다.

단 하나의 큰 문제는 terrain이 4.6251이라는 것이다.

---

# 5. 직전 20 iteration: 매우 안정적인 local optimum

```text
reward mean       24.5265
reward std         0.6701

terrain mean       4.4702
terrain slope     +0.01689 / iter

XY error mean      0.4343
base contact       3.70%

value-loss median  0.0201
value-loss max     0.0242
```

이 구간은 critic까지 거의 완벽하게 조용하다.

4300/4800과 비교해 4900의 가장 강한 evidence다.

---

# 6. 직전 50 iteration

```text
reward mean       24.5700
reward std         0.7884
reward min        22.95
reward max        26.39

terrain mean       4.2195
terrain slope     +0.01677 / iter

XY error mean      0.4352
yaw error mean     0.365
episode length   ~978.9

base contact       3.62%
timeout           96.38%
action std         0.573

value-loss median  0.01985
value-loss max     0.1777
```

중요한 점:

**reward 최저가 22.95다.**

즉 50 iteration 동안 한 번도 원본 4300/4800의 평균 수준 아래로 크게 무너지지 않는다.

Training stability만 보면 세 후보 가운데 4900 주변이 압도적으로 깨끗하다.

---

# 7. 직전 100 iteration은 왜 평균이 낮은가

4900 직전 100회:

```text
reward mean 19.34
reward std   7.69
```

만 보면 오히려 나빠 보인다.

하지만 이 window는 recovery 시작 직후를 포함한다.

Recovery 첫 iteration 4800은:

```text
reward        0.07
terrain       3.5275
episode      11.87
timeout       1.15%
```

수준에서 재초기화된 environment/curriculum statistics를 다시 채우는 구간이다.

따라서 recovery 100-window 평균은 stationary performance window가 아니다.

4900을 평가할 때는 recovery startup transient와 후반 안정 구간을 분리해야 한다.

---

# 8. 가장 큰 confound: curriculum reset

원본 4800:

```text
terrain = 5.7367
```

Recovery 4900:

```text
terrain = 4.6251
```

4900 직전 50회 평균:

```text
4.2195
```

4300 직전 50회:

```text
5.5323
```

4800 직전 50회:

```text
5.6928
```

차이가 크다.

따라서 4900의 높은 reward, 낮은 base-contact, 낮은 tracking error 일부는 **더 쉬운 최근 terrain distribution**의 영향을 받을 수 있다.

이 때문에 4900의 training reward를 그대로 4300/4800과 비교하는 것은 공정하지 않다.

---

# 9. 그렇다고 4900 개선이 전부 착시는 아니다

Recovery를 계속 진행하면 terrain이 빠르게 다시 올라간다.

Recovery 4900~4999:

```text
terrain mean       5.2875
reward mean       22.8315
XY error mean      0.4920
yaw error mean     0.3873
episode length   973.48
base contact       5.15%
timeout           94.85%
action std         0.5889
value-loss median  0.0381
```

그리고 마지막 30회(4970~4999):

```text
terrain mean       5.6778
reward mean       21.5807
XY error mean      0.5323
yaw error mean     0.4107
episode length   968.05
base contact       6.42%
timeout           93.58%
action std         0.6123
value-loss median  0.0291
```

즉 terrain이 원본 4800과 비슷한 5.6~5.8 수준으로 복귀해도 recovery trajectory는 완전히 붕괴하지 않는다.

이것은 recovery 개선이 **오직 쉬운 curriculum 때문만은 아니다**라는 강한 간접 증거다.

단, 4970~4999의 정책은 4900과 같은 checkpoint가 아니므로 4900의 고난도 성능을 직접 증명하는 것은 아니다.

---

# 10. 4800 → 4900 순간 변화

| 지표 | 4800 | 4900 | 변화 |
|---|---:|---:|---:|
| Reward | 20.14 | **24.40** | +21.15% |
| Terrain | **5.7367** | 4.6251 | -19.38% |
| XY error ↓ | **0.5017** | 0.5489 | +9.41% |
| Yaw error ↓ | 0.4278 | **0.3741** | -12.55% |
| Episode length | 968.01 | **982.37** | +1.48% |
| Action std ↓ | 0.66 | **0.57** | -13.64% |
| Timeout | 91.89% | **96.18%** | +4.29%p |
| Base contact ↓ | 8.11% | **3.82%** | -4.29%p |
| Value loss ↓ | 0.0259 | **0.0201** | -22.39% |

여기서 terrain 차이 때문에 reward/낙상률을 직접 causal improvement라고 단정하면 안 된다.

하지만 yaw, action std, motion penalties 개선은 policy refinement의 방향과 일치한다.

---

# 11. Motion-cost component의 개선

4800 → 4900:

```text
lin_vel_z
-0.0482 → -0.0389

ang_vel_xy
-0.2016 → -0.1573

torque
-0.1216 → -0.1093

dof_acc
-0.2223 → -0.1954

action_rate
-0.1454 → -0.1187
```

동시에 tracking reward:

```text
track_lin
1.1642 → 1.1910

track_yaw
0.5762 → 0.6170
```

로 상승한다.

이 패턴이 중요한 이유는 단순 reward hacking과 반대이기 때문이다.

더 높은 tracking reward를 얻으면서 motion penalty도 덜 먹고 있다.

따라서 4900은 적어도 최근 rollout distribution에서는 **더 효율적이고 정돈된 gait**를 학습했을 가능성이 높다.

---

# 12. Recovery critic 안정성

Original fresh run:

```text
max value loss = 283.8869
value loss > 10 = 70회
```

Recovery 200 iteration:

```text
max value loss = 5.3492
value loss > 10 = 0회
```

단순 max 비교에는 run length 차이가 있지만, 4900 바로 주변은 특히 깨끗하다.

```text
4900 직전 50회
median = 0.01985
max    = 0.1777
```

이는 4900이 만들어진 학습 구간에서 critic이 매우 안정적이었다는 근거다.

Value loss는 실제 제출 actor의 직접 성능 지표는 아니지만, **정책 생성 과정의 안정성**이라는 면에서는 4900이 가장 강하다.

---

# 13. Checkpoint tensor 상태

4900:

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
mean -0.000253
std   0.09524
min  -1.4415
max   1.7667
L2   50.9902
```

Critic:

```text
mean  0.003044
std   0.10202
min  -2.1632
max   1.3909
L2   54.5040
```

수치 손상 징후가 없다.

---

# 14. Action std의 구조적 감소

Checkpoint 내부 action std parameter 평균:

```text
4300 = 0.6378
4800 = 0.6636
4900 = 0.5653
```

4800→4900에서 약 14.8% 정도 감소한다.

각 action dimension에서도 전반적으로 내려간다.

4900은 단순 특정 관절 하나만 std가 줄어든 것이 아니라, **대부분의 action dimension에서 distribution이 좁아졌다.**

이것은:

- 행동 reproducibility
- command tracking 안정성
- 불필요한 joint excursion

에 긍정적일 가능성이 있다.

반대로:

- 계단
- 강한 push
- 급격한 terrain transition

에서 큰 corrective action을 덜 낼 위험도 있다.

따라서 low std는 “무조건 좋은 지표”가 아니라 fixed evaluator에서 확인할 가설이다.

---

# 15. 4800 → 4900 parameter drift

Deterministic actor:

```text
parameters          286,604
L2 delta            4.97097
relative L2 drift   9.83%
cosine similarity   0.99524
mean abs delta      0.00696
max abs delta       0.07193
```

4300→4800 drift:

```text
18.75%
```

의 절반 정도다.

따라서 4900은 4800에서 정책의 기본 구조를 크게 깨뜨린 모델이 아니다.

이것은 4800의 hard-terrain experience가 완전히 사라졌을 가능성을 낮춰주는 정황이다.

---

# 16. 4300 → 4900 비교

순간값:

```text
Reward         +18.2%
XY error        -2.6%
Yaw error       -6.5%
Episode length  +3.3%
Action std     -10.9%
Base contact    약 절반
```

하지만 terrain은 16.6% 낮다.

따라서 4900이 4300보다 전반적으로 더 좋은 것처럼 보여도 **같은 시험지를 푼 결과가 아니다.**

이 비교 역시 fixed benchmark 없이는 최종 결론이 아니다.

---

# 17. Recovery 후반이 보여주는 중요한 신호

4900 이후 정책은 terrain이 계속 올라가면서:

- reward가 조금 내려감
- base-contact가 3~4%에서 6%대로 상승
- action std가 0.57에서 0.61~0.62로 다시 증가

한다.

이것은 오히려 curriculum이 성능 수치에 얼마나 영향을 주는지 보여준다.

즉 4900의 매우 좋은 local metrics 일부는 쉬운 terrain 효과를 분명 포함한다.

그러나 5.6~5.8 terrain에서도 recovery가 reasonable performance를 유지한다는 점 때문에 4900 lineage 자체가 약한 것은 아니다.

---

# 18. 6 terrain에서 4900의 검증 가설

아래는 측정치가 아닌 검증 가설이다.

| Terrain | 4900 가설 |
|---|---|
| stairs | smoother action이 장점일 수 있으나 correction amplitude 부족 위험 |
| inverted stairs | 낮은 std와 낮은 ang_vel penalty가 안정성에 유리할 가능성 |
| boxes | 4800 hard-terrain memory 유지 여부가 핵심 |
| random rough | 4800과 비슷하면 4900 승리 근거가 강해짐 |
| +20° slope | 반드시 4800과 직접 비교 필요 |
| -20° slope | smoother gait가 오히려 가장 큰 장점일 가능성 |

4900의 가장 중요한 질문은:

> “낮은 std와 smoothness 개선이 hard-terrain robustness를 희생하지 않았는가?”

다.

---

# 19. 현재 가장 강한 제출 후보인 이유

4900은 현재 세 후보 중 다음이 동시에 갖춰져 있다.

1. recovery 정상 완료
2. evidence validation PASS
3. official backup success
4. source 4800 SHA lineage 명확
5. `model_best.pt == model_4900.pt`
6. final `policy.pt` actor와 exact-match
7. low base-contact
8. high timeout
9. low action std
10. low critic loss
11. improved yaw
12. improved motion costs

즉 **artifact-level 완성도**는 가장 높다.

---

# 20. 4900을 바로 확정하면 안 되는 이유

오직 한 가지지만 매우 큰 이유:

> best selection 당시 terrain distribution이 더 쉬웠다.

이 confound 하나 때문에 4900의 training-side 우세를 실제 competition-side 우세라고 그대로 승격하면 안 된다.

따라서 추가 학습보다 **동일 evaluator 비교가 먼저**다.

---

# 21. 정량 evaluator에서 4900에 요구되는 최소 조건

4900이 최종 제출 1순위를 유지하려면:

- 6 terrain 평균 success가 4800보다 크게 떨어지지 않음
- worst terrain success가 4800과 동급 이상
- stairs에서 큰 실패 증가 없음
- +20° / -20° slope에서 4800과 동급 이상
- random rough/boxes에서 capability 유지
- base-contact / survival은 4800보다 우수
- tracking RMSE도 최소 동급
- seed 간 분산이 4800보다 낮거나 동급

이면 된다.

특히 **hard terrain에서 4800과 동률만 나와도**, smoothness/survival/provenance를 합치면 4900이 매우 강한 winner가 된다.

---

# 22. 4900이 패배하는 시나리오

4900이 최종 탈락할 수 있는 가장 현실적인 경우는:

```text
평지/쉬운 terrain:
4900 우세

stairs/slope/rough:
4800 명확 우세
```

인 경우다.

그 결과가 나오면 recovery가 4800을 “더 부드럽지만 덜 robust한 정책”으로 만든 것으로 해석할 수 있다.

이 경우 대회 terrain 비중을 고려해 4800이 더 안전한 제출 후보가 될 수 있다.

---

# 23. 현재 판정

### 강점

- evidence/finalize/backup 모두 정상
- source 4800 lineage 명확
- policy.pt와 4900 actor exact-match
- 직전 50회 reward 안정성이 매우 높음
- base-contact 크게 감소
- timeout 증가
- yaw tracking 개선
- action std 크게 감소
- motion cost 전반 개선
- critic local stability 압도적
- checkpoint tensor finite

### 약점

- curriculum reset이라는 큰 confound
- best 당시 terrain이 4300/4800보다 낮음
- 낮은 std가 hard-terrain correction을 제한할 가능성
- 4900 자체의 동일 난이도 fixed evaluation 미완료

### 최종 등급

```text
Artifact integrity       : A+
Provenance               : A+
Local training stability : A+
Survival evidence        : A
Yaw tracking             : A
Smoothness prior         : A
Hard-terrain evidence    : B (fixed evaluator 필요)
Curriculum comparability : C
Submission readiness     : A-
```

---

# 24. 최종 요약

`model_4900.pt`는 현재 자료에서 가장 유력한 제출 후보다.

단순히 reward 24.4라서가 아니다.

실제로:

> 낮은 base-contact\
> 긴 episode\
> 높은 timeout\
> 낮은 action std\
> 낮은 critic loss\
> 개선된 yaw tracking\
> 감소한 motion penalties\
> 정확한 source/policy lineage

가 동시에 나타난다.

이 정도로 여러 독립 지표가 같은 방향으로 움직이는 것은 의미가 있다.

하지만 best 당시 curriculum이 쉬웠다는 문제는 제거되지 않는다.

따라서 4900의 정확한 현재 위치는:

> **“가장 완성도 높은 provisional winner”**

다.

4300/4800/4900을 같은 six-terrain fixed benchmark에 올렸을 때 4900이 hard-terrain 성능만 유지한다면, 현재 남은 가장 큰 반론이 사라지고 최종 제출 1순위로 고를 근거가 매우 강해진다.
