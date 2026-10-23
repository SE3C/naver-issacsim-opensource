> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/incoming/other/reviewed/GO2_A1_MODEL_4300_DEEP_ANALYSIS_20260915.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# Go2 A1 `model_4300.pt` 매우 심층 분석

작성 기준: 2026-09-15\
대상: 공식 서버 A1 fresh run의 `model_4300.pt`\
분석 목적: 4300을 단순 “옛 checkpoint”가 아니라 **fresh-run의 reward optimum 후보**로 독립 평가하고, 4800·4900과 비교할 때 무엇을 강점/위험으로 봐야 하는지 정리한다.

---

## 0. 한 줄 결론

`model_4300.pt`는 **원본 fresh A1 학습에서 가장 높은 reward가 발생한 구간을 대표하는 실제 보존 checkpoint이며, 4800보다 낮은 curriculum 난이도에서 만들어졌지만 주변 50~100 iteration의 reward 안정성은 더 좋았다.** 따라서 “자동 best니까 무조건 최고”도 아니고 “4300이라 오래됐으니 4800보다 열등”도 아니다. 현재 세 후보 중 **가장 깨끗한 fresh-run stability control**이다.

최종 제출 후보로 채택하려면 4300/4800/4900을 동일한 fixed terrain·seed·command에서 비교해야 한다.

---

# 1. Provenance와 무결성

## 1.1 체크포인트 식별

```text
checkpoint:
model_4300.pt

SHA-256:
82efb1a59bfad74c5b03b7584fe7cf27865dcd0603550f11340c4134c6a802c8
```

원본 A1 run:

```text
run_id:
20260914-084321-go2-a1-tracklin150-lvz-m2-5k-official

requested iterations:
5000

actual logged range:
0 ~ 4837

environments:
4096

seed:
42

status:
interrupted
```

이 run은 4837 부근에서 사용자 입력으로 중단되어 `official_finalize`가 완료되지 않았지만, checkpoint mirror 자체는 정상 보존되었다.

원본 evidence validation에서 확인되는 항목:

```text
native_run      PASS
tensorboard     PASS
checkpoints     PASS (49개)
source_identity PASS
```

전체 validation이 FAIL인 이유는 checkpoint 손상 때문이 아니라 **중단 때문에 official backup/finalize가 끝나지 않았기 때문**이다.

---

## 1.2 4300이 실제 old `model_best`였다는 forensic 근거

후속 recovery run 시작 전 `/workspace/training/quadruped/exported/` provenance에는 다음 파일이 남아 있었다.

```text
model_best_20260914174326.pt
SHA-256:
82efb1a59bfad74c5b03b7584fe7cf27865dcd0603550f11340c4134c6a802c8
```

이 SHA-256은 원본 evidence의 `model_4300.pt`와 정확히 일치한다.

따라서 4300은 나중에 임의로 “좋아 보이는 checkpoint”라고 붙인 것이 아니라, **원본 fresh trajectory에서 당시 자동 best로 선택되었던 실제 checkpoint**다.

---

# 2. 왜 4300이 best였는가

원본 console 전체를 파싱했을 때 fresh run 최고 Mean Reward는:

```text
21.85 @ iteration 4284
```

였다.

checkpoint는 100 iteration 간격으로 저장되므로 4284 자체의 weight는 보존되지 않았고, 그 peak에 가장 가까운 저장 checkpoint 계열이 4300이다.

중요한 해석:

- `reward 21.85`는 `model_4300.pt`의 고정 평가 점수가 아니다.
- 이것은 iteration 4284 training rollout의 mean reward다.
- 따라서 `4300 reward = 21.85`라고 쓰면 안 된다.
- 실제 iteration 4300의 mean reward는 `20.65`다.

즉 4300의 의미는:

> “4284에서 최고 training reward가 나온 구간을 대표하는 저장 checkpoint”

이지:

> “공식 시나리오에서 21.85점을 받은 모델”

이 아니다.

---

# 3. iteration 4300 순간 상태

| 지표 | 값 |
|---|---:|
| Mean reward | **20.65** |
| Terrain level | **5.5469** |
| XY velocity error | **0.5636** |
| Yaw-rate error | **0.3999** |
| Mean episode length | **951.37** |
| Timeout termination | **92.14%** |
| Base-contact termination | **7.86%** |
| Action std | **0.64** |
| Mean value loss | **0.1777** |
| Mean surrogate loss | **0.0002** |
| Entropy loss | **11.1948** |

Reward component:

| 항목 | 값 |
|---|---:|
| `track_lin_vel_xy_exp` | +1.1654 |
| `track_ang_vel_z_exp` | +0.5937 |
| `lin_vel_z_l2` | -0.0404 |
| `ang_vel_xy_l2` | -0.1862 |
| `dof_torques_l2` | -0.1073 |
| `dof_acc_l2` | -0.2099 |
| `action_rate_l2` | -0.1346 |
| `feet_air_time` | -0.0015 |

한 iteration만 보면 4300은 매우 정상적인 고성능 상태다. Episode length가 약 951이고 base-contact가 8% 아래이며, terrain도 이미 5.5 수준이다.

---

# 4. 단일점이 아니라 주변 window로 본 4300

## 4.1 직전 20 iteration

```text
reward mean      20.196
reward std        0.680
terrain mean      5.5405
XY error mean     0.6171
base contact      8.10%
value-loss median 0.0838
value-loss max    2.2483
```

4300 바로 직전은 상당히 평온하다.

Reward 표준편차가 0.68에 불과하고, value loss도 큰 폭발 없이 유지된다.

---

## 4.2 직전 50 iteration

```text
reward mean      19.8482
reward std        1.7788
reward min        9.07
reward max       21.85

terrain mean      5.5323
XY error mean     0.6115
yaw error mean    0.417
episode length  ~960.0

base contact      8.31%
timeout          91.69%
action std        0.628

value-loss median 0.0304
value-loss max   15.8577
```

핵심은 reward 최대값만이 아니다.

4300 근처 50회 평균도 19.85로 높고, 표준편차도 1.78이다.

4800 직전 50회의 reward 표준편차가 약 4.37이라는 점을 고려하면, 4300 구간은 **후기 4800보다 학습 상태가 훨씬 정돈되어 있었다.**

---

## 4.3 직전 100 iteration

```text
reward mean      19.6278
reward std        1.4284
terrain mean      5.5380
XY error mean     0.6259
base contact      8.66%
value-loss median 0.0276
value-loss max   15.8577
```

100 iteration까지 넓혀도 4300 주변 reward variance는 비교적 낮다.

따라서 4284 하나만 우연히 튀었다기보다는, **4300 전후가 원본 run의 안정적인 고보상 구간이었던 것**으로 보는 편이 합리적이다.

---

# 5. 4300 이후에도 학습은 계속 좋아졌는가

이 질문이 4300 평가의 핵심이다.

4300 이후 100 iteration(4300~4399)을 보면:

```text
reward mean       18.8880
terrain mean       5.5764
XY error mean      0.6277
yaw error mean     0.4253
episode length   962.39
base contact       7.61%
action std         0.6535
value-loss median  0.0889
value-loss max    23.76
```

즉 4300 이후:

- terrain은 계속 올라감
- base-contact는 조금 좋아짐
- episode length도 증가
- 하지만 reward는 내려감
- action std는 증가
- critic 변동성이 커짐

이 패턴은 4300 이후 정책이 단순 퇴보했다기보다 **더 어려운 curriculum으로 넘어가며 적응 비용을 치르기 시작했다**고 해석하는 것이 자연스럽다.

---

# 6. 4300 → 4800에서 무엇이 변했는가

순간값 기준:

| 지표 | 4300 | 4800 | 변화 |
|---|---:|---:|---:|
| Reward | 20.65 | 20.14 | -2.47% |
| Terrain | 5.5469 | 5.7367 | **+3.42%** |
| XY error | 0.5636 | 0.5017 | **-10.98%** |
| Yaw error | 0.3999 | 0.4278 | +6.98% |
| Episode length | 951.37 | 968.01 | +1.75% |
| Action std | 0.64 | 0.66 | +3.13% |
| Base contact | 7.86% | 8.11% | +0.25%p |

따라서 4300이 “모든 면에서 4800보다 좋았다”는 결론은 지원되지 않는다.

오히려 4800은:

- 더 어려운 terrain
- 더 좋은 XY tracking
- 더 긴 episode

을 얻었다.

4300이 앞서는 것은:

- reward 안정성
- yaw 순간값
- 낮은 action std
- 더 평온한 학습 window

다.

---

# 7. Actor/critic tensor 상태

`model_4300.pt`의 actor와 critic tensor를 직접 검사한 결과:

```text
Actor parameters : 286,616
Actor NaN        : 0
Actor Inf        : 0

Critic parameters: 285,185
Critic NaN       : 0
Critic Inf       : 0
```

Actor weight 통계:

```text
mean  -0.000286
std    0.09180
min   -1.3954
max    1.6949
L2    49.1442
```

Critic weight 통계:

```text
mean   0.002324
std    0.09865
min   -2.0412
max    1.3747
L2    52.6966
```

따라서 checkpoint 자체가 수치적으로 손상됐다는 신호는 없다.

---

# 8. Action distribution 분석

4300 checkpoint의 12 action 차원 `std_param` 평균:

```text
mean = 0.63775
min  = 0.40221
max  = 0.81645
```

로그의 `Mean action std = 0.64`와 정확히 같은 방향이다.

4300은 4800보다 낮고, 4900보다는 높은 exploration scale을 가진다.

```text
4300 : 0.6378
4800 : 0.6636
4900 : 0.5653
```

해석하면 4300은 세 후보 중 **중간 정도의 행동 분산**을 가진다.

너무 좁게 수렴하지 않았고, 4800처럼 후기 curriculum에서 action variance가 더 커진 상태도 아니다.

---

# 9. Parameter-space에서 4300은 얼마나 다른 정책인가

Deterministic actor parameter 기준:

```text
4300 → 4800
relative L2 drift = 18.75%
cosine similarity = 0.98339

4300 → 4900
relative L2 drift = 20.97%
cosine similarity = 0.97951
```

4300 이후 정책이 단순 미세조정만 된 것은 아니다.

특히 4300→4800 사이에는 상당한 policy drift가 있었다.

즉 4300과 4800은 같은 A1 reward로 학습됐지만 **행동 정책 수준에서는 충분히 다른 후보**라고 볼 수 있다.

---

# 10. Critic instability 관점의 4300

원본 전체 fresh run에는 매우 큰 value-loss spike가 반복됐다.

하지만 4300 바로 직전 20 iteration은 비교적 깨끗하다.

```text
20-window max value loss = 2.2483
```

50-window에서는 한 번 큰 spike가 포함돼:

```text
max = 15.8577
```

이지만 중앙값은:

```text
0.0304
```

에 불과하다.

즉 4300이 저장된 정확한 구간은 **원본 run 전체의 극단적 critic instability 구간 한가운데라기보다는 비교적 안정적인 구간**이다.

이 점은 4300을 후보로 유지할 근거다.

---

# 11. Curriculum 관점의 한계

4300의 가장 큰 약점이다.

원본 curriculum은 4300 이후에도 상승했다.

4300 순간:

```text
terrain = 5.5469
```

4800 순간:

```text
terrain = 5.7367
```

따라서 4300은 4800보다 낮은 평균 난이도 분포에서 만들어진 정책이다.

`Curriculum/terrain_levels`는 단일 지형의 “최대 정복 레벨”이 아니라 병렬 4096 env 평균이므로 절대적인 능력 점수로 보면 안 된다. 그래도 4300과 4800이 같은 fresh trajectory에 있기 때문에 **상대적으로 후기 정책이 더 어려운 지형에 노출됐다는 방향성**은 의미가 있다.

---

# 12. 6개 고정 terrain에서 예상되는 4300의 검증 가설

아래는 **현재 training evidence에서 유도한 검증 가설**이며 측정 결과가 아니다.

| Terrain | 4300 가설 |
|---|---|
| stairs | 안정적일 가능성 높으나 4800보다 hard step 대응이 약할 수 있음 |
| inverted stairs | 균형은 좋으나 후기 terrain 적응 부족 여부 확인 필요 |
| boxes | 비교적 안정적인 gait가 장점일 수 있음 |
| random rough | 4800보다 성공률이 약간 낮을 가능성 |
| +20° slope | tracking/자세 균형은 좋을 수 있으나 4800보다 correction 여유가 적을 가능성 |
| -20° slope | 지나치게 aggressive하지 않은 것이 오히려 장점일 수 있음 |

4300에서 가장 기대되는 것은 **평균적인 균형과 재현성**이다.

가장 걱정되는 것은 **최고 난이도 terrain에서 4800보다 낮은 capability ceiling**이다.

---

# 13. 대회 관점에서 4300의 가장 큰 장점

공식 Go2 평가 방향은 단순 mean reward가 아니라 전진, 전방위 추종, 험지, 경사, 계단, 밀침 회복 같은 복수 시나리오다.

이 관점에서 4300의 장점은:

1. fresh uninterrupted lineage
2. reward peak 주변에서 안정적
3. 높은 terrain까지 이미 도달
4. action std가 과도하게 크지 않음
5. yaw tracking이 4800보다 좋음
6. checkpoint 자체 수치 무결성 정상

이다.

특히 fixed evaluator에서 hard-terrain 성공률까지 4800/4900과 비슷하게 나온다면 **4300은 생각보다 강력한 제출 후보**가 된다.

---

# 14. 가장 큰 위험

4300의 위험은 training reward가 너무 좋아서가 아니라, 그 reward best가 **curriculum capability best와 동일하지 않을 수 있다는 것**이다.

4300을 선택하면 다음 질문에 답해야 한다.

> “4800까지 추가 학습하면서 얻은 hard-terrain 적응을 버려도 되는가?”

현재 training log만으로는 답할 수 없다.

---

# 15. 정량 evaluator에서 4300에 요구할 통과 조건

4300을 최종 제출 후보로 올리려면 최소한:

- 6 terrain 평균 success가 4800/4900과 통계적으로 큰 차이가 없어야 함
- worst terrain success가 4800보다 크게 떨어지지 않아야 함
- +20° / -20° slope에서 낙상률이 높아지지 않아야 함
- XY RMSE가 4800의 장점을 심하게 잃지 않아야 함
- push/recovery에서 4900 대비 지나치게 불안정하지 않아야 함

이 조건을 통과한다면 fresh provenance와 안정적인 training region 때문에 4300의 가치가 크게 올라간다.

---

# 16. 현재 판정

### 강점

- 원본 fresh-run의 실제 reward-best checkpoint
- 4284 peak와 forensic provenance가 일치
- 주변 20~100 iteration이 비교적 안정적
- checkpoint tensor 완전 finite
- 4800보다 낮은 action std
- 4800보다 좋은 yaw 순간값
- resume/curriculum-reset confound 없음

### 약점

- 4800보다 낮은 terrain exposure
- 4800보다 XY tracking이 약함
- 4300 이후 정책이 상당히 변했으므로 후기 capability를 놓쳤을 가능성
- 4300 고정 6-terrain 정량평가가 아직 없음

### 최종 등급

```text
Fresh-run stability      : A
Provenance               : A
Reward-optimum evidence  : A
Hard-terrain evidence    : B
Tracking evidence        : B+
Numerical integrity      : A
Submission readiness     : B (fresh export/paired evaluator 확인 필요)
```

---

# 17. 최종 요약

`model_4300.pt`는 “4800보다 덜 학습된 낡은 모델”이라고 단순화하면 안 된다.

원본 A1 trajectory에서 **실제 최고 reward가 발생한 안정 구간을 대표하는 checkpoint**이며, 후기 4800보다 reward variance와 action variance가 낮았다.

반대로 4300이 “진짜 최고 정책”이라고 단정하는 것도 잘못이다. 4300 이후 curriculum은 계속 상승했고 4800에서는 더 어려운 terrain과 더 좋은 XY tracking을 얻었다.

따라서 4300의 정확한 역할은:

> **fresh A1의 가장 안정적인 reward-optimum 후보이자, 4800/4900의 hard-terrain·recovery 개선이 실제인지 판정하기 위한 핵심 control**

이다.

고정 조건 benchmark에서 4300이 4800/4900과 비슷한 성공률을 보이면, 자동 `model_best`라는 사실 이상의 매우 강한 제출 근거가 생긴다.
