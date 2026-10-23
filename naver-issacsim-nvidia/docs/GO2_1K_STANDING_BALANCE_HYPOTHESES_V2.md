# Go2 1K 저-Iteration 제자리 균형 문제 재분석 및 Reward 가설 v2

작성일: 2026-09-12  
대상: NAVER CONNECT Robotics Cup 2026 / Unitree Go2 / Isaac Lab PPO  
목적: **1K screening에서 제자리 균형이 심하게 무너지는 원인을 좁히고, 단일 변수 reward 가설을 재설계**

> **역사적 가설 제안:** 아래 우선순위는 2026-09-12 당시 계획이지 네 실행 기록이 아니다. 이 문서의 S1/S2는 orientation `-0.5/-1.0` 후보이고, 같은 delta의 실행 관찰은 G-006에 기록됐다. 이 문서의 S3는 angular-velocity `-0.12` 제안으로 이후 G-004와 delta가 같지만 S3라는 이름으로 실행됐다는 뜻은 아니다. S4 action-rate `-0.015`의 실행 근거는 확인되지 않았다. 9/13 실제 screening 보고서는 **같은 S1–S4 라벨을 orientation 네 값 `-1.0/-0.5/-0.25/-0.125`에 다시 썼다.** 두 문서의 S 번호를 일대일로 합치거나 `GS` schedule ID로 바꾸지 않는다. 이후 orientation 축은 생존 편향·terrain 저하로 현재 `REJECT`다. 새 Go2 실험 판단은 분석 저장소 `research/EXPERIMENTS.md`를 따른다.

---

# 0. 결론

기존에는 `track_lin_vel_xy_exp` 강화를 가장 먼저 실험하려 했지만,  
당시 소스와 과거 장기학습 상태를 대조해 **`flat_orientation_l2` 활성화를 1순위 가설로 제안했다.** 후속 G-006 screening의 현재 판정은 위 역사적 주석을 따른다.

현재 환경의 핵심 특징:

- standing command 비율: **2%**
- `flat_orientation_l2`: **0.0 / 사실상 비활성**
- `lin_vel_z_l2`: **-3.0**
- `ang_vel_xy_l2`: **-0.08**
- `action_rate_l2`: **-0.01**
- `track_lin_vel_xy_exp`: **1.0**
- `feet_air_time`: **0.01**
- `track_ang_vel_z_exp`: **0.75**

즉 현재 정책은 저-iteration에서:

> **"가만히 똑바로 서 있는 자세"를 직접 많이 연습하지도 않고, 몸통의 정적 기울기 자체도 직접 벌점받지 않는다.**

반면:

- `ang_vel_xy_l2`는 roll/pitch 각속도, 즉 **얼마나 빨리 흔들리는가**를 벌점
- `lin_vel_z_l2`는 수직 속도, 즉 **얼마나 위아래로 튀는가**를 벌점

하기 때문에,

> **기울어진 채로 거의 움직이지 않는 자세**는 위 두 항만으로 강하게 교정되지 않을 수 있다.

장기 학습에서는 다른 tracking/동역학 reward와 반복 경험으로 결국 안정 자세를 학습하지만,  
1K에서는 그 credit assignment가 충분히 진행되지 않아 제자리 균형이 늦게 형성된다는 가설이 가장 그럴듯하다.

따라서 이번 1K screening의 핵심 질문은:

> **"직접적인 body orientation penalty를 켜면, 장기학습까지 기다리지 않아도 standing skill이 조기에 형성되는가?"**

이다.

---

# 1. Release / 영상 자료 확인 결과

확인한 GitHub Release:

```text
Go2 recovery bundle 20260830_125132_KST
tag: brev-go2-recovery-20260830_125132_KST
```

Release 설명상 포함 자료:

```text
- source
- full run logs/events
- model_9500
- exported best
- env/report
- 5k snapshot
- environment metadata
- console traceback
- SHA256 manifest
```

해당 장기 실행은 약 **9,512 iteration에서 numerical stop**이 발생한 run이다.

또한 repo에는 Go2 checkpoint 영상을 각각 별도로 생성하기 위한:

```text
docs/GO2_BASELINE_RECORDING.md
scripts/record_go2_checkpoints.sh
```

가 존재하며, 5K와 장기 checkpoint를 독립적으로 재생하도록 설계되어 있다.

## 중요 제한

현재 GitHub Release에서 Go2 자료는 직접 `.mp4` asset으로 노출된 것이 아니라  
`go2-recovery-20260830_125132_KST.tar.gz` 내부에 묶여 있다.

현재 연결된 GitHub 인터페이스에서는 private release의 binary archive 내부 MP4를 직접 디코딩해 프레임 단위로 재생할 수 없었다.

따라서 아래 진단은:

```text
Release 메타데이터
+ 정확한 당시 source
+ 정확한 Isaac Lab 고정 commit
+ 5K / 9.5K checkpoint 존재
+ 사용자가 관찰한 "저iter에서는 못 서고 장기학습에서는 해결" 현상
```

을 결합한 **source-grounded diagnosis**이다.

실제 `play_video.mp4` 또는 1K checkpoint 영상을 별도로 확보하면  
아래 가설 중 `action_rate` 방향 등은 영상 증상에 따라 더 정확하게 좁힐 수 있다.

---

# 2. 현재 Baseline

현재 `training/quadruped/quadruped_rewards.py`:

```python
REWARD_WEIGHTS = {
    "track_lin_vel_xy_exp": 1.0,
    "feet_air_time":        0.01,
    "lin_vel_z_l2":        -3.0,
    "ang_vel_xy_l2":       -0.08,
    "action_rate_l2":      -0.01,

    # "track_ang_vel_z_exp": 0.75,
    # "flat_orientation_l2": -1.0,
}
```

---

# 3. Stock Isaac Lab Go2와 현재 Baseline 차이

고정 환경:

```text
Isaac Sim: 5.1.0-rc.19
Isaac Lab commit:
3e73d6dd79080fd7632488c061052a6edd52e230
```

해당 commit의 stock Go2는 대략:

```python
track_lin_vel_xy_exp = 1.5
track_ang_vel_z_exp  = 0.75
feet_air_time        = 0.01

lin_vel_z_l2         = -2.0
ang_vel_xy_l2        = -0.05
action_rate_l2       = -0.01

flat_orientation_l2  = 0.0
```

현재 baseline은 stock 대비:

| Reward | Stock Go2 | 현재 | 변화 |
|---|---:|---:|---|
| track_lin_vel_xy_exp | 1.5 | 1.0 | 약화 |
| track_ang_vel_z_exp | 0.75 | 0.75 | 동일 |
| feet_air_time | 0.01 | 0.01 | 동일 |
| lin_vel_z_l2 | -2.0 | -3.0 | 안정성 강화 |
| ang_vel_xy_l2 | -0.05 | -0.08 | 흔들림 억제 강화 |
| action_rate_l2 | -0.01 | -0.01 | 동일 |
| flat_orientation_l2 | 0.0 | 0.0 | 비활성 |

여기서 중요한 점:

**이미 현재 baseline은 stock보다 vertical motion과 roll/pitch angular motion을 더 강하게 억제한다.**

따라서 저iter standing 실패 원인을 단순히:

```text
"안정성 penalty가 약하다"
```

라고 보는 것은 설명력이 떨어진다.

---

# 4. 가장 중요한 구조적 문제 — Standing sample이 2%

정확한 Isaac Lab commit의 velocity command 설정:

```python
rel_standing_envs = 0.02
```

즉 4096 env 기준 기대값으로 약:

```text
4096 × 0.02 ≈ 82 env
```

정도만 standing command를 받는다.

나머지 약 98%는 움직이는 velocity command를 학습한다.

이는 평가 구조와 상당한 mismatch가 있다.

평가에서는:

```text
제자리 균형 = 10.5점
```

으로 독립된 고배점 항목인데,

학습 distribution에서는 explicit standing command가:

```text
2%
```

에 불과하다.

## 가설

장기학습에서는 수천 iteration 동안 충분한 standing sample이 누적되면서 결국 해결된다.

하지만 1K에서는:

```text
standing 경험 부족
+
직접 orientation reward 없음
+
초기 exploration noise
```

가 겹치면서 제자리 안정 자세의 학습 속도가 늦다.

따라서 **1K standing 문제는 final capability 부족보다 sample-efficiency 문제일 가능성이 높다.**

---

# 5. 왜 `flat_orientation_l2`가 핵심 후보인가

현재 안정성 항목:

```python
"lin_vel_z_l2":  -3.0
"ang_vel_xy_l2": -0.08
```

하지만 둘은 서로 다른 물리량을 본다.

## lin_vel_z_l2

억제:

```text
body vertical velocity
```

즉:

```text
위아래 bouncing
```

을 억제한다.

정적인 roll/pitch 기울기를 직접 고치지는 않는다.

## ang_vel_xy_l2

억제:

```text
roll angular velocity
pitch angular velocity
```

즉:

```text
휘청이는 속도
```

를 줄인다.

하지만 몸이 이미 기울어진 뒤 angular velocity가 거의 0이면  
"기울어진 상태" 자체를 직접 크게 벌점 주는 항은 아니다.

## flat_orientation_l2

직접 억제:

```text
gravity vector 대비 body orientation error
```

즉:

```text
몸통이 수평에서 벗어난 정도
```

자체를 벌점준다.

따라서:

```text
standing
→ posture
→ static tilt
```

문제에는 가장 직접적인 reward다.

---

# 6. 수정된 1K 가설 우선순위

## B0 — Baseline

```python
REWARD_WEIGHTS = {
    "track_lin_vel_xy_exp": 1.0,
    "feet_air_time":        0.01,
    "lin_vel_z_l2":        -3.0,
    "ang_vel_xy_l2":       -0.08,
    "action_rate_l2":      -0.01,
}
```

목적:

```text
1K 기준점 재확보
```

필수.

---

## S1 — Flat Orientation 약하게 활성화 ★★★★★

### 변경

```python
"flat_orientation_l2": -0.5
```

나머지 baseline 그대로.

### 가설

저iter에서 standing skill 형성이 늦는 핵심 원인은  
정적인 body tilt를 직접 교정하는 reward가 없기 때문이다.

`-0.5` 정도의 orientation penalty를 넣으면:

```text
roll/pitch 정적 오차
→ 즉시 비용 발생
→ upright posture가 더 빨리 학습
```

할 가능성이 있다.

### 기대

```text
제자리 균형        ↑↑↑
밀침 후 자세복구   ↑
평지 gait 안정성   ↑
전진 추종          유지 가능
```

### 위험

경사 ±10°에서는 몸통이 terrain에 맞게 기울 필요가 있으므로  
orientation penalty가 너무 강하면 경사/요철 적응성이 떨어질 수 있다.

따라서 첫 값은:

```text
-0.5
```

로 보수적으로 시작.

### 우선도

**1위**

---

## S2 — Flat Orientation 기본 강도 ★★★★★

### 변경

```python
"flat_orientation_l2": -1.0
```

### 목적

S1과 sensitivity 비교.

```text
S1 = -0.5
S2 = -1.0
```

을 같은 1K에서 비교해 orientation penalty 효과가 실제로 monotonic한지 확인한다.

### 기대

S1보다:

```text
제자리 안정 ↑
body tilt ↓
```

가능.

### 위험

```text
경사 대응 ↓
요철 대응 ↓
gait 경직 ↑
```

가능.

### 판정

S1과 standing 차이가 거의 없는데 terrain만 나빠지면:

```text
-1.0 폐기
-0.5 채택
```

---

## S3 — Roll/Pitch Angular Velocity 강화 ★★★★☆

### 변경

```python
"ang_vel_xy_l2": -0.12
```

기존:

```python
-0.08
```

### 가설

저iter standing 실패가 static tilt보다:

```text
좌우/앞뒤 oscillation
```

때문이라면 angular velocity penalty를 강화하는 것이 효과적일 수 있다.

### 기대

```text
제자리 흔들림 ↓
밀침 후 overshoot ↓
평지 gait 안정 ↑
```

### 진단 가치

S1/S2와 비교하면 원인을 분리할 수 있다.

```text
S1 개선 > S3 개선
→ 주원인 = static posture / orientation
```

```text
S3 개선 > S1 개선
→ 주원인 = body angular oscillation
```

---

## S4 — Action Smoothness 강화 ★★★☆☆

### 변경

```python
"action_rate_l2": -0.015
```

기존:

```python
-0.01
```

### 조건부 가설

1K 영상에서 다음이 보인다면:

```text
발이 빠르게 떨림
joint command가 계속 바뀜
제자리에서도 다리를 쉴 새 없이 수정함
body가 작은 진동을 반복함
```

action chatter가 원인일 수 있다.

### 기대

```text
제자리 leg jitter ↓
body micro-oscillation ↓
standing 안정 ↑
```

### 위험

```text
외란 대응 속도 ↓
속도 명령 반응 ↓
밀침 recovery ↓
```

따라서 S1/S2/S3보다 후순위.

---

## S4B — Action Penalty 완화 ★★☆☆☆

반대로 영상이:

```text
쓰러질 때 다리를 빨리 못 뻗음
correction이 지나치게 느림
명령 변화에 반응이 둔함
```

이라면 반대 방향을 테스트.

```python
"action_rate_l2": -0.0075
```

이는 영상 증상이 없으면 우선 실행하지 않는다.

---

## T1 — Linear Tracking 복원 ★★★★☆

### 변경

```python
"track_lin_vel_xy_exp": 1.25
```

현재:

```python
1.0
```

stock Go2:

```python
1.5
```

### 가설

현재 track linear reward가 stock Go2보다 낮아  
moving skill 자체의 학습 속도가 느려졌을 가능성이 있다.

1.25는 중간값.

### 기대

```text
전진 추종 ↑
좌우 추종 ↑
1K에서 보행 형성 속도 ↑
```

### standing과의 관계

직접 standing reward는 아니므로  
**standing 문제 해결용 1순위로 보지 않는다.**

오히려 너무 일찍 강하게 하면:

```text
"일단 움직여서 보상 받기"
```

가 강화되어 standing 안정 형성이 늦어질 수도 있다.

---

## T2 — Stock Linear Tracking 복원 ★★★☆☆

### 변경

```python
"track_lin_vel_xy_exp": 1.5
```

### 목적

정확한 stock Go2 값 복원.

### 가설

현재 1.0이 너무 약해서 locomotion skill formation 자체가 늦다.

### 위험

저iter standing과 terrain 안정성을 희생할 수 있다.

T1이 유효할 때 sensitivity test로 사용.

---

## R1 — Feet Air Time 소폭 강화 ★★★★☆

### 변경

```python
"feet_air_time": 0.03
```

현재:

```python
0.01
```

### 근거

현재 평가에서 가장 낮은 상대 점수:

```text
약한 요철 = 8.17 / 10.5 = 77.8%
```

### 중요한 사실

Isaac Lab `feet_air_time` reward는 linear command가 충분히 작으면 0이 된다.

즉 standing command에서 직접 발을 들도록 유도하지 않는다.

따라서 0.01 → 0.03은:

```text
standing을 직접 악화시키기보다
moving gait / foot clearance에 영향을 주는 실험
```

으로 보는 것이 맞다.

### 기대

```text
약한 요철 ↑
발 끌림 ↓
경사 적응 ↑ 가능
```

### 위험

너무 높이면:

```text
bounding
과도한 swing
vertical oscillation
```

이 증가할 수 있다.

---

## R2 — Vertical Penalty 완화 ★★★★☆

### 변경

```python
"lin_vel_z_l2": -2.5
```

현재:

```python
-3.0
```

stock Go2:

```python
-2.0
```

### 가설

현재 vertical penalty가 stock보다 강해서 저iter에서 정책이:

```text
적극적인 corrective stepping
body height 변화
terrain 적응
```

을 지나치게 억제할 가능성이 있다.

### 기대

```text
요철 ↑
경사 ↑
빠른 자세복구 ↑
전진 tracking ↑ 가능
```

### 위험

```text
제자리 bounce ↑
standing ↓
```

가능.

따라서 standing 문제 해결용이 아니라  
**terrain/회복성과 현재 -3.0의 과도함을 검증하는 반대 방향 실험**이다.

---

# 7. 이번 1K에서 실제로 돌릴 핵심 세트

전체를 다 돌리기보다 다음 7개가 가장 정보량이 크다.

| ID | 변경 | 질문 | 우선도 |
|---|---|---|---:|
| B0 | baseline | 1K 기준점 | 필수 |
| S1 | flat orientation `-0.5` | static tilt가 원인인가 | ★★★★★ |
| S2 | flat orientation `-1.0` | orientation sensitivity | ★★★★★ |
| S3 | ang vel xy `-0.12` | oscillation이 원인인가 | ★★★★☆ |
| T1 | linear track `1.25` | locomotion 학습속도 문제인가 | ★★★★☆ |
| R1 | feet air `0.03` | 요철 foot clearance 문제인가 | ★★★★☆ |
| R2 | lin vel z `-2.5` | vertical penalty가 과한가 | ★★★★☆ |

---

# 8. 가장 중요한 판별 로직

## Case A

```text
S1/S2에서 제자리 균형이 크게 개선
S3은 변화 작음
```

판단:

```text
주원인 = static body orientation 학습 지연
```

다음 단계:

```text
flat_orientation_l2 = -0.5 ~ -1.0 범위 최적화
```

---

## Case B

```text
S3가 가장 크게 개선
S1/S2는 제한적
```

판단:

```text
주원인 = roll/pitch oscillation
```

다음 단계:

```text
ang_vel_xy_l2 = -0.10 ~ -0.14 세밀 탐색
```

---

## Case C

```text
T1에서 standing 포함 전반이 같이 개선
```

판단:

```text
정책 전체 locomotion skill formation이 느린 것이 핵심
```

현재 `track_lin=1.0`이 너무 낮아  
저iter에서 유용한 locomotion representation이 늦게 형성됐을 가능성.

---

## Case D

```text
R2에서 terrain/속도는 개선
standing은 하락
```

판단:

```text
현재 -3.0 vertical penalty는 terrain에는 과하지만 standing에는 유리
```

최종적으로:

```text
-2.5 ~ -3.0 사이
```

에서 compromise 탐색.

---

## Case E

```text
1K에서는 전부 standing이 불안정
3K 이상에서 대부분 해결
```

판단:

```text
reward coefficient보다 training horizon / standing sample efficiency 문제가 더 큼
```

이 경우 1K를 최종성능 평가로 사용하면 안 된다.

1K는:

```text
방향성 screening
```

으로만 사용.

---

# 9. 우선순위 최종 정리

## 제자리 균형 원인 탐색

```text
1. flat_orientation_l2 -0.5
2. flat_orientation_l2 -1.0
3. ang_vel_xy_l2 -0.12
4. action_rate_l2 -0.015   ← jitter가 실제로 보일 때만
```

## 속도 추종

```text
5. track_lin_vel_xy_exp 1.25
6. track_lin_vel_xy_exp 1.5
```

## 요철 / terrain

```text
7. feet_air_time 0.03
8. lin_vel_z_l2 -2.5
```

---

# 10. 추천 1K 실행 순서

```text
B0  baseline
S1  flat_orientation -0.5
S2  flat_orientation -1.0
S3  ang_vel_xy -0.12
T1  track_lin 1.25
R1  feet_air 0.03
R2  lin_vel_z -2.5
```

시간이 더 부족하면:

```text
B0
S1
S3
T1
R1
```

이 5개만 우선.

---

# 11. 절대 하지 말 것

1K screening 단계에서는:

```text
flat_orientation + ang_vel_xy
track_lin + feet_air
track_lin + lin_vel_z
```

처럼 두 개 이상 동시에 바꾸지 않는다.

이번 목적은:

```text
"어떤 reward 축이 실제 병목인가"
```

를 찾는 것이다.

조합 최적화는 그 다음 단계.

---

# 12. 이번 분석의 핵심 판단

현재 현상:

```text
낮은 iter → 제자리 균형 매우 약함
높은 iter → 제자리 균형 해결
```

은 오히려 좋은 단서다.

이건:

```text
정책이 standing을 본질적으로 못 배우는 구조
```

보다는

```text
standing skill이 늦게 형성되는 구조
```

에 가깝다.

현재 소스를 기준으로 가장 설명력이 높은 이유는:

```text
standing command 비율 2%
+
flat_orientation reward 비활성
+
초기 exploration
```

이다.

따라서 **이번 1K screening의 최우선 가설은 `flat_orientation_l2` 활성화**로 수정한다.

---

# 13. 최종 핵심 가설 5개

```text
S1  flat_orientation_l2 : 0.0 → -0.5
    목적: static tilt 직접 억제

S2  flat_orientation_l2 : 0.0 → -1.0
    목적: orientation 효과 sensitivity 확인

S3  ang_vel_xy_l2       : -0.08 → -0.12
    목적: roll/pitch oscillation 억제

T1  track_lin_vel_xy_exp: 1.0 → 1.25
    목적: moving skill 학습속도 개선

R1  feet_air_time       : 0.01 → 0.03
    목적: 요철 foot clearance 개선
```

가장 먼저 돌릴 것:

```text
B0 → S1 → S3 → T1 → R1
```

특히 **S1과 S3 비교가 이번 실험에서 가장 중요한 진단 포인트**다.
