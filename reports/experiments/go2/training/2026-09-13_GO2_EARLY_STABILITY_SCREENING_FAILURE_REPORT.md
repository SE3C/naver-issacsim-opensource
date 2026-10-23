> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/experiments/go2/training/2026-09-13_GO2_EARLY_STABILITY_SCREENING_FAILURE_REPORT.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# [학습] Go2 초기 안정화 Reward Screening 실패 분석 보고서

> 관리 안내 (2026-10-13): **학습** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](<../../../../research/EXPERIMENTS.md>)를 확인한다.

- 작성일: 2026-09-13
- 대상: Unitree Go2 / `Quadruped-v0`
- 환경: 개인 NVIDIA Brev L40S 검증 서버
- 목적: Go2의 초기 자세 안정성을 개선할 수 있는 단일 reward 변경을 짧은 screening으로 선별
- 주의: 본 문서는 **개인 서버의 screening 결과**이며 공식 제출 정책 성능이나 공식 평가 점수를 의미하지 않는다.

---

## 1. 실험 배경

기존 Go2 개인 baseline은 장기 학습에서 성능이 크게 개선되는 특성이 확인되어 있다.

- 약 4.5k 부근: XY error 약 `1.17`, terrain level 약 `0.92`
- 약 9.5k 부근: XY error 약 `0.72`, terrain level 약 `5.83`, base-contact 약 `1.91%`

따라서 Go2는 낮은 iteration에서 terrain level이 낮다고 해서 곧바로 장기 실패라고 단정할 수 없다. 이번 실험의 목적은 장기 최적값을 확정하는 것이 아니라, **초기 100~200 iteration에서 안정성 개선 신호가 있는 reward 후보를 빠르게 screening**하는 것이다.

이번 screening에서는 한 번에 하나의 reward만 변경했고, PPO·terrain·task·병렬 환경 수 등은 그대로 유지했다.

---

## 2. 공통 실행 조건

| 항목 | 값 |
|---|---|
| Task | `Quadruped-v0` |
| 병렬 환경 | `4096` |
| Seed | `42` |
| 실행 모드 | headless |
| 요청 iterations | `1000` |
| 기본 `track_lin_vel_xy_exp` | `1.0` |
| 기본 `track_ang_vel_z_exp` | `0.75` |
| 기본 `lin_vel_z_l2` | `-3.0` |
| 기본 `ang_vel_xy_l2` | `-0.08` |
| 기본 `action_rate_l2` | `-0.01` |
| 기본 `feet_air_time` | `0.01` |
| 기본 `flat_orientation_l2` | 비활성 (`0.0`) |
| 변경 원칙 | 한 번에 reward 1개만 변경 |

주요 판정 지표는 다음과 같이 고정했다.

- `Curriculum/terrain_levels`
- `Episode_Termination/base_contact`
- `Episode_Termination/time_out`
- `Mean episode length`
- `Metrics/base_velocity/error_vel_xy`
- `Metrics/base_velocity/error_vel_yaw`
- reward term별 기여값
- value loss / action std의 수치 안정성

---

# 3. 실패 실험 A — `flat_orientation_l2` 활성화

## 3.1 가설

> Go2가 1K 초반에 자세를 충분히 잡지 못하는 이유는 몸통 수평 자세를 직접 억제하는 reward가 비활성화되어 있기 때문일 수 있다.\
> `flat_orientation_l2`를 활성화하면 roll/pitch 안정성과 생존성이 좋아지고, 이후 보행 및 terrain progression으로 이어질 것이다.

원본 reward 파일에는 다음 후보가 주석 처리되어 있었다.

```python
# "flat_orientation_l2": -1.0,
```

따라서 외부 값을 임의로 가져오기보다 해당 값을 기준으로 강도를 단계적으로 줄여가며 screening했다.

---

## 3.2 G-006 — `flat_orientation_l2 = -1.0`

### 주요 관찰

| Iteration | Terrain | Timeout | Base contact | XY error | Yaw error |
|---:|---:|---:|---:|---:|---:|
| 103 | 1.313 | 97.17% | 2.83% | 1.741 | 0.767 |
| 145 | 0.740 | 99.32% | 0.68% | 1.856 | 0.524 |
| 205 | 0.210 | 99.35% | 0.65% | 1.677 | 0.392 |
| 약 217 | 0.119 | - | - | - | - |
| 이후 | 약 0.09 | - | - | - | - |

### 해석

`-1.0`은 초기 생존성과 자세 안정성을 매우 빠르게 강화했다.

- episode가 거의 항상 timeout까지 유지됨
- base-contact termination이 1% 이하까지 감소
- yaw error도 빠르게 개선

그러나 terrain level은 반대로 계속 하락했다.

```text
1.33 → 0.74 → 0.21 → 0.12 → 0.09
```

즉 정책이 **“안 넘어지는 안전한 행동”을 매우 빠르게 학습했지만, 실제 이동·terrain progression을 희생하는 방향으로 수렴**한 것으로 판단했다.

### 판정

**기각**

- 안정성 효과: 강함
- terrain progression: 명확히 악화
- 보행/이동 촉진 효과: 확인되지 않음
- 실패 형태: 지나치게 보수적인 자세 유지 정책

---

## 3.3 G-006 — `flat_orientation_l2 = -0.5`

### 주요 관찰

| Iteration | Terrain | Timeout | Base contact | XY error | Yaw error |
|---:|---:|---:|---:|---:|---:|
| 67 | 1.901 | 83.92% | 16.10% | 1.899 | 0.989 |
| 103 | 1.284 | 95.14% | 4.89% | 1.902 | 0.755 |
| 127 | 0.999 | 97.90% | 2.10% | 1.817 | 0.607 |
| 130 | 0.956 | 97.92% | 2.08% | 1.887 | 0.657 |
| 131 | 0.940 | 97.90% | 2.10% | 1.853 | 0.588 |
| 132 | 0.923 | 97.91% | 2.09% | 1.996 | 0.633 |
| 133 | 0.906 | 97.93% | 2.07% | 1.799 | 0.638 |

중단 후 finalize report에는 최고 reward step 141, terrain 약 `0.76`, 낙상률 약 `1.7%`가 기록되었다.

### 해석

`-1.0`보다 자세 안정화가 약해졌지만, 기대했던 terrain 개선은 나타나지 않았다.

오히려 다음 패턴이 다시 나타났다.

```text
생존성 상승
base-contact 감소
terrain 지속 하락
```

즉 강도만 절반으로 낮춰도 기본적인 실패 방향은 유지됐다.

### 판정

**기각**

- `-1.0`보다 덜 보수적이지만 근본 패턴 동일
- 안정성 희생에 비해 terrain 이득 없음
- XY tracking도 명확한 개선 없음

---

## 3.4 G-006 — `flat_orientation_l2 = -0.25`

### 주요 관찰

103 iteration 기준:

| 지표 | 값 |
|---|---:|
| Terrain | 1.259 |
| Timeout | 92.91% |
| Base contact | 7.12% |
| XY error | 1.875 |
| Yaw error | 0.763 |
| Episode length | 990.47 |

이후 terrain level은 약 `1.02` 부근까지 지속 하락하여 조기 중단했다.

### 해석

강도를 더 줄이자 생존성은 예상대로 떨어졌지만, **그 대가로 terrain progression이 살아나는 현상은 나타나지 않았다.**

동일 103 iteration 비교:

| Weight | Terrain | Timeout | Base contact |
|---:|---:|---:|---:|
| -1.0 | 1.313 | 97.2% | 2.8% |
| -0.5 | 1.284 | 95.1% | 4.9% |
| -0.25 | 1.259 | 92.9% | 7.1% |

강도를 줄일수록 생존성만 악화됐고 terrain은 오히려 소폭 낮아졌다.

### 판정

**기각**

---

## 3.5 G-006 — `flat_orientation_l2 = -0.125`

### 주요 관찰

103 iteration 기준:

| 지표 | 값 |
|---|---:|
| Terrain | 1.196 |
| Timeout | 88.16% |
| Base contact | 11.86% |
| XY error | 1.741 |
| Yaw error | 0.805 |
| Episode length | 988.74 |

### 해석

`-0.125`까지 약하게 만들었지만 결과는 더 명확했다.

- 생존성 추가 악화
- base-contact 증가
- terrain 개선 없음
- XY tracking은 일부 좋아졌지만 전체 trade-off를 뒤집을 수준은 아님

103 iteration 비교:

| Weight | Terrain | Timeout | Base contact | XY error |
|---:|---:|---:|---:|---:|
| -1.0 | 1.313 | 97.2% | 2.8% | 1.741 |
| -0.5 | 1.284 | 95.1% | 4.9% | 1.902 |
| -0.25 | 1.259 | 92.9% | 7.1% | 1.875 |
| -0.125 | 1.196 | 88.2% | 11.9% | 1.741 |

### 판정

**기각**

`-0.125` 아래로 더 세분화하는 것은 정보 대비 서버 시간 효율이 낮다고 판단하고 `flat_orientation_l2` 축을 종료했다.

---


## 3.6 실시간 관찰과 중단 판단

`flat_orientation_l2` screening은 단순히 endpoint 수치만 보고 기각한 것이 아니다. 학습 도중 실시간 로그를 보면서 **정책이 “잘 걷는 방향”보다 “안 넘어지고 버티는 방향”으로 학습되는 징후**를 확인했고, 이를 근거로 조기 중단과 weight 축소를 반복했다.

특히 `flat_orientation_l2=-1.0` 실행에서 약 145 iteration 부근에는 mean reward가 약 `8.7` 수준까지 올라갔지만 terrain level은 약 `0.5` 수준으로 내려가고 있었다. 당시 로그를 본 관찰은 다음과 같았다.

```text
reward는 계속 올라가는데
terrain level은 떨어지고
정책은 앞으로 적극적으로 이동하기보다
서서 버티는 쪽으로 학습되는 것으로 보였다.
```

이후 terrain level은 `1.x`대에서 빠르게 내려가 최종적으로 약 `0.07~0.09` 수준까지 접근했다. 이 시점에서는 높은 mean reward가 실제 locomotion 성능 개선을 의미하지 않는다고 판단했다.

즉 이 실험은 다음과 같은 **reward hacking / 생존 편향에 가까운 패턴**을 보였다.

```text
flat_orientation penalty 활성화
→ 몸통을 수평으로 유지하는 행동 강화
→ 넘어지지 않고 오래 버티는 정책 형성
→ timeout 비율 상승
→ mean reward 상승
→ 실제 이동 및 terrain curriculum 진행은 오히려 붕괴
```

따라서 mean reward만 보면 성공처럼 보일 수 있었지만, terrain progression과 실제 행동 성격을 함께 보면 실패였다.

### 영상 확인을 생략한 이유

`-1.0` 실행은 terrain이 거의 0으로 수렴하는 수준까지 악화했고, 로그상에서도 정책이 이동보다 생존에 치우친 것으로 판단되었다. 따라서 이 단계에서는 별도 play 영상을 생성해 추가 분석할 정보 가치가 낮다고 판단해 영상 검증을 생략했다.

이는 “영상이 필요하지 않다”는 일반 원칙이 아니다. 정상 후보나 경계선 후보라면 반드시 play 영상으로 확인해야 한다. 이번 경우는 **screening 단계에서 명확한 실패 신호가 너무 강해서 서버 시간을 아끼기 위한 조기 탈락 결정**이었다.

### weight를 단계적으로 낮춘 이유

`-1.0`의 실패가 단순히 방향 자체의 문제인지, penalty가 너무 강했던 문제인지 구분하기 위해 다음과 같이 절반씩 약화했다.

```text
-1.0
→ -0.5
→ -0.25
→ -0.125
```

각 단계에서 기대한 것은 다음과 같았다.

```text
penalty 약화
→ 지나친 정지/생존 편향 감소
→ 이동성 회복
→ terrain progression 회복
```

그러나 실제로는 penalty를 약화할수록 timeout은 감소하고 base-contact가 증가했으며, terrain progression은 의미 있게 회복되지 않았다.

103 iteration 부근 비교:

| flat_orientation_l2 | Terrain | Timeout | Base contact | XY error | 해석 |
|---:|---:|---:|---:|---:|---|
| -1.0 | 1.313 | 97.2% | 2.8% | 1.741 | 매우 안정적이지만 이후 terrain 급락 |
| -0.5 | 1.284 | 95.1% | 4.9% | 1.902 | 생존성 감소, terrain 회복 없음 |
| -0.25 | 1.259 | 92.9% | 7.1% | 1.875 | 안정성 추가 감소 |
| -0.125 | 1.196 | 88.2% | 11.9% | 1.741 | 네 후보 중 가장 약하지만 여전히 개선 없음 |

따라서 `-0.125`가 상대적으로 “덜 나쁜” 값일 수는 있어도, baseline 대비 유망한 개선 후보라고 보기는 어려웠다. 이 때문에 `-0.0625` 이하로 더 세분화하지 않고 `flat_orientation_l2` 가설 자체를 종료했다.

### 조기중단 판단의 불확실성

이번 결정에는 한 가지 중요한 반례가 있었다. 이전 개인 Go2 baseline은 장시간 동안 성능이 좋지 않아 보이다가 뒤늦게 크게 개선된 경험이 있었다.

기존 장기 baseline에서:

- 약 4.5k: terrain 약 `0.92`
- 약 9.5k: terrain 약 `5.83`

까지 상승했다.

실시간 판단 당시에도 “지금은 실패처럼 보여도 오래 학습하면 뒤늦게 회복할 수 있다”는 가능성을 고려했다. 실제 이전 baseline은 약 8k 전후까지 부진하다가 이후 terrain이 크게 상승한 경험이 있었다.

하지만 이번 `flat_orientation=-1.0`은 단순히 “terrain 상승이 늦는 것”과 다른 패턴을 보였다.

```text
terrain이 정체된 것이 아니라
1.x → 0.5 → 0.1 이하 방향으로 지속적으로 붕괴
+
timeout은 거의 100%
+
base-contact는 매우 낮음
+
mean reward는 오히려 상승
```

즉 **학습이 안 되고 있는 상태라기보다, 잘못된 행동 전략을 매우 성공적으로 학습하고 있는 상태**에 가까웠다.

이 차이 때문에 장기 회복 가능성을 완전히 부정하지는 않되, 현재 screening 목적에서는 추가 GPU 시간을 투입할 가치가 낮다고 판단했다.

### `flat_orientation_l2` 최종 실패 정의

이번 가설의 실패를 단순히 “terrain level이 낮았다”로 정의하지 않는다.

실패의 핵심은 다음 세 가지가 동시에 나타난 것이다.

1. `flat_orientation_l2`를 강하게 주면 survival은 크게 향상됨
2. 그러나 locomotion 및 terrain progression은 지속적으로 악화됨
3. penalty를 1/8 수준까지 약화해도 이 trade-off가 해소되지 않음

따라서 현재 Go2에서 `flat_orientation_l2`는 **초기 자세 안정성만 따로 높이는 효과는 있으나, 전체 보행 성능을 개선하는 stability anchor로는 부적합**하다고 판단했다.


# 4. 실패 실험 B — `lin_vel_z_l2: -3.0 → -4.0`

## 4.1 가설

> Go2 초반 불안정의 핵심이 몸통 기울기 자체가 아니라 수직 바운싱이라면, `lin_vel_z_l2`를 `-3.0`에서 `-4.0`으로 강화하면 수직 움직임과 착지 불안정을 억제하여 base-contact를 감소시키고, terrain progression은 유지할 수 있을 것이다.

변경은 다음 한 줄뿐이었다.

```diff
- "lin_vel_z_l2": -3.0,
+ "lin_vel_z_l2": -4.0,
```

`flat_orientation_l2`는 다시 비활성 상태로 유지했다.

실험 ID:

```text
go2-g3-linvelz-m4-1k-20260913
```

---

## 4.2 주요 결과

### Iteration 97

| 지표 | 값 |
|---|---:|
| Mean reward | 3.64 |
| Episode length | 959.93 |
| Terrain | 1.3742 |
| Timeout | 86.12% |
| Base contact | 13.88% |
| XY error | 1.9591 |
| Yaw error | 0.9074 |
| Action std | 0.51 |
| Value loss | 0.0071 |

이 시점에서 terrain은 비교적 유지됐지만, 기대했던 초기 안정성 향상은 크지 않았다.

---

### Iteration 145

| 지표 | 값 |
|---|---:|
| Mean reward | 7.56 |
| Episode length | 981.09 |
| Terrain | 0.6992 |
| Timeout | 93.05% |
| Base contact | 6.95% |
| XY error | 1.7140 |
| Yaw error | 0.6801 |
| Action std | 0.48 |
| Value loss | 0.0079 |

97→145 사이에는 안정성과 tracking이 일부 개선됐다.

하지만 terrain은:

```text
1.374 → 0.699
```

로 절반 가까이 감소했다.

---

### Iteration 205

| 지표 | 값 |
|---|---:|
| Mean reward | 8.96 |
| Episode length | 920.29 |
| Terrain | **0.1741** |
| Timeout | **88.06%** |
| Base contact | **11.97%** |
| XY error | **1.5303** |
| Yaw error | **0.4586** |
| Action std | 0.46 |
| Value loss | 0.0080 |
| `lin_vel_z_l2` contribution | -0.0328 |

145→205에서는 tracking error는 계속 개선됐지만 안정성은 다시 나빠졌다.

```text
terrain      0.699 → 0.174
timeout      93.1% → 88.1%
base contact 7.0%  → 12.0%
episode len  981   → 920
```

즉 수평 명령 추종은 좋아졌지만, **terrain 적응과 생존성이 동시에 붕괴**했다.

---

## 4.3 실패 판정

**G3 `lin_vel_z_l2=-4.0` 기각**

가설에서 기대한 결과:

```text
수직 흔들림 감소
→ base-contact 감소
→ episode survival 증가
→ terrain 유지
```

실제 결과:

```text
tracking 일부 개선
→ terrain 지속 붕괴
→ 중간에 좋아졌던 survival도 다시 악화
```

따라서 `-4.0`은 Go2 초기 안정화 anchor로 채택하기 어렵다.

가능한 해석은 **수직 움직임을 지나치게 억제하여 지형에 대응하기 위한 필요한 상하 운동까지 제한했을 가능성**이다. 다만 현재 screening만으로 정확한 인과 메커니즘을 확정하지 않는다.

---

# 5. 실패 실험들의 공통 패턴

이번 screening에서 두 종류의 안정화 접근이 모두 같은 문제를 보였다.

## 5.1 `flat_orientation_l2`

몸통의 **기울어진 상태 자체**를 억제했다.

결과:

```text
자세 안정 ↑
생존성 ↑
terrain progression ↓
```

강도를 낮추면 생존성만 다시 떨어졌고 terrain은 살아나지 않았다.

---

## 5.2 `lin_vel_z_l2=-4.0`

몸통의 **수직 움직임**을 더 강하게 억제했다.

결과:

```text
tracking 일부 개선
초기/중간 생존성 일부 개선
terrain progression 크게 ↓
후반 survival 재악화
```

---

## 5.3 현재 판단

지금까지 결과는 Go2의 초반 문제를 단순히

> “움직임을 더 억제하면 안정적으로 잘 걷게 된다”

라고 볼 수 없음을 보여준다.

오히려 안정성 penalty를 강화하면 정책이 terrain에 필요한 자유도까지 잃거나, 안전한 행동 쪽으로 과도하게 최적화될 가능성이 있다.

따라서 다음 단계에서는 **안정성 penalty 강화보다 이동 목표를 더 명확하게 주는 reward 방향**을 우선 검증하는 것이 정보 효율이 높다.

---

# 6. 다음 실험 우선순위

## G-001 — `track_lin_vel_xy_exp: 1.0 → 1.25`

### 가설

> Go2가 초반에 terrain을 충분히 올라가지 못하는 이유가 안정성 부족만이 아니라, 명령 속도를 적극적으로 추종할 유인이 상대적으로 약하기 때문일 수 있다.

### 기대 결과

- XY error 조기 감소
- locomotion 적극성 증가
- terrain progression 유지 또는 개선
- survival이 심하게 악화되지 않음

### 기각 조건

- XY error는 줄지만 base-contact가 급격히 증가
- terrain이 이전 실패 실험처럼 빠르게 0 방향으로 붕괴
- 큰 진동 또는 과도한 속도 추종으로 생존성 상실

---

## G-003 — `feet_air_time: 0.01 → 0.03`

G2 이후 후속 후보.

목적은 발을 조금 더 적극적으로 들도록 유도하여 험지·계단 clearance를 개선하는 것이다.

다만 hopping 또는 과도한 발 들기 가능성이 있으므로 반드시 play 영상과 함께 검증한다.

---

# 7. Screening 방법론의 한계

이번 결과는 **짧은 단일-seed screening**이다.

특히 기존 Go2 baseline은 약 4.5k에서 terrain level 약 `0.92`였지만 9.5k에서는 약 `5.83`까지 회복된 사례가 있다. 따라서 100~200 iteration에서 terrain이 낮다는 이유만으로 그 reward가 장기적으로 반드시 실패한다고 증명할 수는 없다.

이번 기각은 다음 의미로 해석해야 한다.

> 제한된 서버 시간을 사용하는 현재 탐색 단계에서, 해당 reward를 장시간 confirmation까지 올릴 만큼 긍정적인 초기 신호를 확보하지 못했다.

즉 **“장기적으로 절대 작동하지 않는다”가 아니라 “현재 screening에서 후속 장기 실험 우선순위에서 제외한다”**는 판정이다.

---

# 8. 최종 요약

| 실험 | 변경 | 핵심 결과 | 판정 |
|---|---|---|---|
| S1 | `flat_orientation_l2=-1.0` | 생존성 극대화, terrain `~0.09`까지 붕괴 | 기각 |
| S2 | `flat_orientation_l2=-0.5` | 같은 패턴 반복, terrain 약 `0.76` 수준까지 하락 | 기각 |
| S3 | `flat_orientation_l2=-0.25` | 안정성 감소, terrain 이득 없음 | 기각 |
| S4 | `flat_orientation_l2=-0.125` | 안정성 추가 감소, terrain 이득 없음 | 기각 |
| G3 | `lin_vel_z_l2 -3.0 → -4.0` | tracking은 개선됐지만 terrain `0.174`, survival 재악화 | 기각 |

현재까지의 결론:

> **Go2 초기 안정성을 단순히 orientation 또는 vertical-motion penalty 강화로 해결하려는 접근은 유망하지 않았다.**

다음 실험은 baseline으로 복구한 뒤:

```text
track_lin_vel_xy_exp: 1.0 → 1.25
```

단일 변경을 우선 검증한다.

---

## 9. 현재 실험 상태

다음 실험 전에 reward는 반드시 baseline으로 복구한다.

```python
"track_lin_vel_xy_exp": 1.0
"lin_vel_z_l2": -3.0
# "flat_orientation_l2": -1.0,   # 비활성
"feet_air_time": 0.01
```

그리고 다음 run에서 `track_lin_vel_xy_exp`만 `1.25`로 변경한다.
