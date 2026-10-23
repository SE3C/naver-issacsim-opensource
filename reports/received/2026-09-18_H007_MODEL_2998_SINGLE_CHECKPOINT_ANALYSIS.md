> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/incoming/other/reviewed/2026-09-18_H007_MODEL_2998_SINGLE_CHECKPOINT_ANALYSIS.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# H1 `model_2998.pt` 단일 체크포인트 심층 분석

> 대상: H-007 `LINTRACK100`, H-001 1.5K parent에서 resume한 최종 체크포인트 `model_2998.pt`\
> 분석 기준: 원본 TensorBoard scalar, checkpoint 자체, 기존 H-007 run provenance, 이번에 추가 제공된 6개 terrain 영상\
> 분석 목적: `model_2998.pt` 자체의 추종·안정성·지형 적응·행동 품질을 하나의 문서에서 판단\
> 판정 원칙: **확인된 사실 / 강한 정황 / 가설 / 판단 불가**를 구분하며, 단일 영상·단일 seed를 성공률로 과장하지 않는다.

---

# 1. Executive Summary

`model_2998.pt`는 H-007 학습의 **최종 체크포인트**이며, 이번 run에서 가장 강한 **late linear-XY tracking 후보**다. 체크포인트 내부 iteration은 실제로 `2998`이고 SHA-256은 아래와 같다.

`388ea635532d206049957518fb8f5fb73ff91da16dc9fa3017d7c8b41715767f`

학습 로그에서 endpoint XY velocity error는 **0.31547**, 마지막 100 iteration 평균은 **0.32939**다. 이는 `model_2800` 및 `model_2900` 주변보다 낮고, step 2978에서는 post-warmup 최저 **0.30011**까지 내려갔다. 즉 2998은 마지막 한 점만 우연히 좋았던 정책이 아니라 **학습 후반 100회 전체에서 XY tracking이 개선된 상태**다.

기존 분석에서 2998의 가장 큰 불확실성은 “실제 gait 영상이 없다”는 것이었다. 이번에는 동일 모델이라고 사용자가 명시한 6개 영상이 추가되었다. 모든 영상은 1920×1080, 50 fps, 999 frames, 19.98 s로 동일한 길이·형식이며 다음 지형을 다룬다.

- `random_rough`
- `stairs`
- `inverted_stairs`
- `boxes`
- `slope_up_10deg`
- `slope_down_10deg`

6개 영상 전체에서 **명백한 낙상·누운 상태 유지·hopping local optimum은 관측되지 않았다.** 계단 계열과 rough terrain을 통과하고, ±10° slope에서도 끝까지 직립 보행한다. 특히 `boxes` 영상에서는 약 16초 부근 큰 자세 교란과 깊은 knee/hip flexion이 나타나지만, **바로 upright gait로 복귀하여 계속 이동**한다. 이는 2998에 실제 recovery margin이 존재한다는 강한 정성적 증거다.

반면 학습 로그에서 yaw error는 여전히 약점이다. endpoint **1.98195**, 마지막 100회 평균 **2.00046**으로 H-007 초반보다 크게 나쁘다. 따라서 이 정책은 “모든 tracking 축이 좋아진 최종 정책”이라기보다 **linear translation tracking이 강화되고 gross terrain stability는 유지되었지만 yaw control은 희생된 정책**으로 해석하는 것이 가장 정확하다.

최종 판단은 다음과 같다.

**`model_2998.pt`는 실제 시나리오/evaluator로 올릴 가치가 충분한 최우선 후보다.**\
다만 현재 자료만으로 “최종 제출 확정” 또는 “H-007 reward 변경이 인과적으로 우월함”까지 주장하는 것은 이르다. 특히 yaw, zero-command stop, vx/vy 분리 성능, 반복 시나리오 성공률을 고정 evaluator에서 확인해야 한다.

---

# 2. Run / Checkpoint Identity

## 2.1 Run lineage

- Robot: H1 humanoid
- Experiment: H-007 `LINTRACK100`
- Run ID: `20260917-002225-h1-h007-lintrack100-from-h001-1p5k`
- Mode: PERSONAL
- Parent run: `H001_PARENT_1P5K_LOCKED`
- Parent checkpoint: `model_1499.pt`
- Parent SHA-256 recorded in metadata:\
  `68fa0a9fe5334f8a3ecea110c4ccc9adb81ec07ac50169eaf8009b1a6e88f0c1`
- Training type: **resume / fine-tuning**
- Seed: `42`
- Num envs: `4096`
- Additional iterations: `1500`
- TensorBoard/console labels: `1499 ... 2998`
- Last saved checkpoint: `model_2998.pt`

## 2.2 Actual reward change relative to parent

이번 branch의 직접적인 parent는 이미 `termination_penalty=-50`을 사용하던 H-001이다. 따라서 parent → H-007의 핵심 의도 변화는 사실상 다음 하나다.

- `track_lin_vel_xy_exp`: **0.5 → 1.0**

즉 2998은 “termination을 새로 강화한 정책”이 아니라, **기존 TERM50 gait에서 linear velocity tracking weight를 추가 강화한 fine-tuned policy**로 보는 것이 맞다.

## 2.3 Checkpoint integrity

`model_2998.pt`를 archive에서 직접 추출하여 확인했다.

- file size: 약 6.9 MB
- internal `iter`: **2998**
- actor tensors: **9개 / 298,278 parameters**
- critic tensors: **8개 / 295,937 parameters**
- actor NaN/Inf: **없음**
- critic NaN/Inf: **없음**
- optimizer tensor NaN/Inf: **없음**
- actor distribution std parameter:
  - min: **0.31210**
  - mean: **1.61733**
  - max: **2.75843**

따라서 checkpoint 파일 자체에 corruption이나 numerical failure 정황은 없다.

---

# 3. 2998 시점의 정량 상태

endpoint 단일 값은 episode sampling noise가 크기 때문에, **2998 단일 point + 직전 50/100/200 iteration 평균**을 함께 본다.

| Metric | step 2998 | last 50 | last 100 | last 200 | 해석 |
|---|---:|---:|---:|---:|---|
| Terrain level ↑ | 5.3676 | 5.3617 | **5.3725** | 5.3819 | 5.3대 후반 plateau |
| XY velocity error ↓ | **0.3155** | **0.3257** | **0.3294** | 0.3355 | 후반부에서 계속 개선 |
| Yaw error ↓ | 1.9820 | **1.9866** | 2.0005 | 2.0152 | 약 2.0 부근, 명확한 약점 |
| Base-contact termination ↓ | 32.69% | 31.50% | **30.78%** | 30.57% | endpoint보다 window가 더 안정적 |
| Timeout ↑ | 67.31% | 68.50% | **69.23%** | 69.45% | 대략 69% 수준 유지 |
| Episode length ↑ | 705.55 | 743.19 | **750.65** | 756.09 | endpoint는 하방 noise 성격 |
| Mean reward | 5.0285 | 5.4139 | **5.4622** | 5.4269 | reward 자체는 선택 기준으로 부적합 |
| Policy mean std | 1.6173 | 1.6188 | **1.6197** | 1.6221 | late std가 소폭 낮아지는 방향 |
| Action-rate term | -0.08310 | **-0.08356** | -0.08430 | -0.08519 | late smoothness가 약간 회복 |
| Feet-slide term | -0.05869 | **-0.05926** | -0.05934 | -0.06035 | late slip penalty가 약간 완화 |

핵심은 **step 2998의 episode length 705.55 / base-contact 32.69%만 보고 “마지막에 안정성이 붕괴했다”고 해석하면 안 된다는 것**이다. 직전 100~200 iteration 평균에서는 base-contact가 약 30.6~30.8%, timeout이 약 69.2~69.4%, episode length가 약 751~756으로 유지된다.

---

# 4. Linear Tracking Analysis

## 4.1 XY tracking은 2998의 가장 강한 장점

후반부의 중요한 수치는 다음과 같다.

- last-200 XY mean: `0.33554`
- last-100 XY mean: `0.32939`
- last-50 XY mean: `0.32573`
- endpoint: `0.31547`
- post-warmup best: **`0.30011 @ step 2978`**

즉 window가 뒤로 갈수록 평균 오차가 계속 낮아진다.

이는 2998이 단순 checkpoint noise가 아니라 **후반 정책 분포 자체가 linear velocity tracking 방향으로 이동한 결과**라는 해석을 지지한다.

또한 기존 late checkpoint 비교에서 직전 100 iteration 기준 XY error는 다음이었다.

- model 2800 주변: `0.33805`
- model 2900 주변: `0.34205`
- model 2998 주변: **`0.32939`**

2998은 late 후보 세 개 중 linear XY 측면에서 가장 강하다.

## 4.2 forward / lateral 분리는 불가능

logger가 `Metrics/base_velocity/error_vel_xy`를 결합값으로만 기록하므로 다음은 **판단 불가**다.

- vx tracking이 좋아진 것인지
- vy tracking이 좋아진 것인지
- 둘 다 좋아진 것인지

따라서 “전진 성능이 정확히 몇 % 좋아졌다” 또는 “좌우 이동이 좋아졌다”는 식으로 분리해서 말할 수 없다.

---

# 5. Yaw / Turning Analysis

2998의 가장 큰 내부 약점은 yaw다.

- endpoint yaw error: `1.98195`
- last-50: `1.98657`
- last-100: `2.00046`
- last-200: `2.01523`

후반에 2.0 부근으로 고착되어 있다.

반면 H-007 초기 recovery 구간에서는 yaw error가 대략 1.2~1.4 수준이었다. 따라서 학습이 진행되며 **linear translation 성능과 yaw control이 같은 방향으로 개선되지 않았다.**

다만 2900 주변의 last-100 yaw `2.03395`와 비교하면 2998의 `2.00046`은 약간 회복된 상태다. 즉 마지막 100 iteration은 “XY만 좋아지고 yaw가 계속 더 악화”되는 구간은 아니다. **XY 개선과 함께 yaw도 2900 주변보다 소폭 되돌아왔다.**

그래도 절대 수준 자체는 여전히 약점이다.

---

# 6. Gross Stability Analysis

## 6.1 학습 로그

2998 주변 안정성은 다음처럼 해석하는 것이 가장 안전하다.

- terrain: 약 **5.37**
- base-contact termination: 약 **30.8% / last100**
- timeout: 약 **69.2% / last100**
- episode length: 약 **751 / last100**

따라서 late policy가 linear tracking을 얻는 대신 terrain curriculum에서 즉시 무너지거나 낙상률이 폭발한 것은 아니다.

## 6.2 2900과의 차이

2900 주변은 생존성만 보면 약간 더 좋았다.

- 2900 last100 base-contact: `30.33%`
- 2998 last100 base-contact: `30.78%`

차이는 약 **0.45 percentage point**다.

Episode length 역시 2900 주변 `762.51` vs 2998 주변 `750.65`로 2998이 약 12 step 낮다.

하지만 2998은 같은 구간에서 XY, yaw, action-rate, feet-slide가 모두 2900보다 좋아졌다. 따라서 2998은 **생존성을 크게 희생한 공격적 checkpoint**라기보다, 매우 작은 survival margin을 내주고 tracking/smoothness를 얻은 정책에 가깝다.

---

# 7. Six-Terrain Video Evidence

## 7.1 Video identity / format

이번 분석에 사용한 영상은 모두 사용자에 의해 `model_2998.pt`의 결과라고 명시되었다.

MP4 내부에는 checkpoint SHA나 model filename이 embedded metadata로 들어 있지 않으므로, **영상 ↔ 2998 연결은 사용자 제공 provenance**이며 파일 자체만으로 cryptographic verification할 수는 없다.

모든 영상의 형식은 동일하다.

- Codec: H.264
- Resolution: 1920×1080
- FPS: 50
- Frames: 999
- Duration: 19.98 s

SHA-256:

| Video | SHA-256 |
|---|---|
| random_rough.mp4 | `c18b382059a03ca4d68bc230c43cb674bb1d7d3e8bf08fb0785455e933df280c` |
| stairs.mp4 | `a5061b8c443b5b6384042465bd058696aefec2108846d0afe237e8c89a331b94` |
| boxes.mp4 | `37029c87ba0ead421774f2abf0a0f1377362b749ee6352dfc58a73f580c5ce8d` |
| inverted_stairs.mp4 | `160cd7c20d15c6f4bbeb23757dc5e487d953e56d5d10b67a30fbfd19c022d311` |
| slope_down_10deg.mp4 | `f14bb953c662e7f7b75b456a55a52f5ec69fb1b4c1e9f7345a2bb1e8ed69b6fd` |
| slope_up_10deg.mp4 | `80c53936e78e020c6c100b0489fb5c3fb96b6ce9c6ce5a47db484e8224f401cc` |

각 영상은 전 구간을 초 단위로 확인했고, obstacle interaction 구간은 0.25~0.5초 간격으로 추가 샘플링했다.

---

# 8. `random_rough` 분석

## 관측

- 약 20초 동안 명백한 낙상 없음.
- 불규칙한 고저차 위에서 계속 active stepping을 유지.
- 10~15초 구간에 torso lean 및 보폭 변화가 관측되지만 즉시 복원됨.
- 약 16~17초 부근 rough patch의 경계를 넘어 평탄 영역으로 나온 뒤에도 upright gait 유지.
- 한 발을 장시간 들고 버티거나, 제자리 hopping으로 생존하는 패턴 없음.

## 해석

이 영상은 2998이 random rough에서 단순히 “서 있기”만 하는 정책이 아니라 **지면 요철에 맞춰 지속적으로 foot placement를 조정하며 실제 이동**한다는 증거다.

강한 정황으로 볼 수 있는 것은 **gross balance와 stepping adaptability**다. 다만 하나의 trajectory이므로 random rough 성공률이나 평균 속도를 정량화할 수는 없다.

### 판정

**PASS — 강한 정성적 증거**

---

# 9. `stairs` 분석

## 관측

- 초반 평탄 영역에서 접근 후 약 12~13초부터 stair band에 진입.
- stair surface 위에서 연속적으로 여러 step/contact를 수행.
- 약 15~16초에는 stair region을 벗어나 다시 평탄 영역으로 이동.
- 진입·통과·이탈 과정에서 명백한 fall 또는 torso-ground contact 없음.
- step 위에서 knee flexion이 증가하지만, 자세를 잃고 주저앉는 형태는 아님.

## 중요한 제한

영상의 이동 경로가 staircase의 최대 경사 방향과 완전히 일치한다고 단정하기 어렵다. 즉 이 한 영상만으로 **“전체 계단 높이를 정면으로 완주했다”**고 표현하면 과장이다.

확실히 말할 수 있는 것은 **step discontinuity가 존재하는 영역을 여러 발 디딤으로 통과하고, 통과 후에도 직립 상태를 유지했다**는 것이다.

### 판정

**PASS — stair contact 대응 확인, full-ascent 성능은 미확정**

---

# 10. `inverted_stairs` 분석

## 관측

- 약 5~6초부터 inverted-stair region에 진입.
- 약 6~12초 동안 계단 band 위/경계에서 지속적으로 움직임.
- 내려가는 방향의 높이 변화에서도 torso가 완전히 무너지지 않음.
- 약 13~14초에 stair region을 벗어난 후 계속 upright gait 유지.
- 큰 충격 후 뻣뻣하게 멈춰 버리는 패턴 없음.

## 해석

내려가는 step은 발이 예상보다 빨리 지면을 잃거나 landing impulse가 커질 수 있기 때문에 biped에서 별도의 위험 요소다. 이 영상에서는 연속적인 step-down 환경에서도 **무너지지 않고 recovery step을 이어가는 행동**이 확인된다.

다만 stairs와 마찬가지로 경로가 최대 경사 방향을 완전히 정면으로 따라가는지 명확하지 않으므로, “최대 난이도 계단 하강 성공률”까지 확장해서는 안 된다.

### 판정

**PASS — descending discontinuity 대응 확인**

---

# 11. `boxes` 분석

6개 영상 중 가장 정보량이 큰 영상이다.

## 관측

- 영상 전체에서 크고 작은 box/ledge가 혼재된 지형을 지속 이동.
- 초반~중반에도 높이 차를 여러 차례 넘으면서 upright gait 유지.
- 약 **16초 부근**에서 가장 큰 자세 교란이 발생:
  - torso가 크게 기울어짐
  - hip/knee flexion 증가
  - 순간적으로 보폭과 자세가 무너질 듯한 상태
- 그러나 약 **0.5~0.75초 이내**에 다시 다리를 펴고 중심을 회복.
- 이후 17~20초까지 다시 정상적인 upright locomotion을 지속.
- 명백한 prone/side fall이나 reset은 보이지 않음.

## 해석

이 장면은 단순 “낙상하지 않았다”보다 더 강한 정보다. 2998은 큰 자세 교란을 받은 뒤 **active recovery step을 생성해 다시 걷는 상태로 복귀**한다.

따라서 model 2998의 stability는 curriculum scalar만 높은 것이 아니라, 적어도 이 sample에서는 **실제 geometric disturbance에 대한 recovery behavior**로 연결된다.

동시에 이 장면은 weakness도 보여준다. box terrain에서 stability margin이 넉넉한 것은 아니다. 큰 step interaction 시 torso angle과 joint flexion이 크게 변하며, 조금 더 나쁜 landing이면 fall로 연결될 가능성이 있다.

즉 boxes는 2998의 **가장 강한 장점과 가장 현실적인 failure margin을 동시에 보여주는 영상**이다.

### 판정

**PASS+ — recovery capability 직접 관측. 단, margin은 충분히 넓다고 단정 불가.**

---

# 12. `slope_up_10deg` 분석

## 관측

- 전체 19.98초 동안 upright 유지.
- active alternating gait 지속.
- 큰 backward collapse 또는 명백한 rollback runaway 없음.
- rough/boxes보다 torso excursion이 작고 gait가 비교적 규칙적.
- command 변화 이후에도 catastrophic failure 없음.

## 해석

10° 상승 경사 자체는 2998의 gross stability를 크게 깨지 않는 것으로 보인다.

단, 카메라가 로봇을 따라가고 visual scale이 제한적이므로 **실제 uphill 진행 속도, commanded vx 대비 slope-specific tracking error**는 영상만으로 정확히 계산할 수 없다.

### 판정

**PASS — 10° uphill에서 직립 보행 유지**

---

# 13. `slope_down_10deg` 분석

## 관측

- 전체 19.98초 동안 upright 유지.
- active gait 지속.
- downhill에서 앞으로 쏠려 연속적으로 가속하며 무너지는 현상 없음.
- 큰 braking instability 또는 발이 밀려 회복하지 못하는 장면 없음.
- 영상 후반까지 gait 지속.

## 해석

하강 경사는 forward momentum 때문에 biped가 무너지기 쉬운 조건인데, 이 sample에서는 2998이 **과도하게 가속되거나 pitch-forward collapse 없이** 계속 locomotion을 수행한다.

다만 정량적인 downhill speed regulation은 영상만으로 판단할 수 없다.

### 판정

**PASS — 10° downhill에서 gross stability 유지**

---

# 14. Cross-Video Behavioral Analysis

6개 영상을 함께 보면 2998의 실제 행동 특성이 더 명확해진다.

## 14.1 공통 강점

### 1) Upright locomotion이 실제로 존재

모든 영상에서 policy는 서 있기만 하는 것이 아니라 발을 번갈아 움직이며 이동한다.

따라서 다음과 같은 reward-hacking 형태와는 맞지 않는다.

- prone survival
- stationary survival
- 반복 hopping만으로 time-out 확보
- 한 발 고정 후 미세 진동으로 reward 수집

### 2) Terrain contact에 반응하는 gait

rough, stair, box에서 joint flexion과 foot placement가 평탄 지형과 다르게 변한다. 즉 지형 변화에 관계없이 동일한 fixed gait를 강제로 반복하는 정책은 아니다.

### 3) Recovery behavior 존재

boxes의 큰 교란에서 가장 명확하다. 자세가 크게 무너진 뒤 다시 upright gait로 복귀한다.

### 4) 20초 horizon에서 catastrophic failure 없음

6개 × 약 20초 = 약 120초의 시각 증거에서 명백한 완전 낙상은 관측되지 않았다.

이는 “2998 endpoint base-contact 32.69%이므로 실제로 매우 불안정할 것”이라는 단순 해석과 맞지 않는다. 학습 metric은 4096 env, random commands, curriculum 전체의 aggregate이며, 이번 영상들은 특정 1-env trajectory이기 때문이다.

## 14.2 공통 약점 / 주의점

### 1) Balance margin이 매우 넓지는 않음

특히 boxes에서 큰 torso excursion이 존재한다. 강한 recovery 능력과 동시에 **fall boundary가 가깝게 보이는 순간**도 있다.

### 2) 영상만으로 yaw weakness를 부정할 수 없음

영상에서 로봇이 넘어지지 않는다고 해서 yaw tracking이 정확하다는 뜻은 아니다. TensorBoard의 yaw error 약 2.0은 여전히 가장 강한 정량 evidence다.

### 3) 성공률이 아님

각 terrain당 1 trajectory이므로 6/6 영상을 보고 “100% 성공률”이라고 표현해서는 안 된다.

### 4) stop / restart는 충분히 검증되지 않음

zero-command 구간을 command log와 정렬한 별도 evaluator가 없으므로 stop drift와 재출발 성능은 여전히 미확정이다.

---

# 15. Smoothness / Slip / Action Quality

2998의 후반 tracking 향상이 무조건 더 거친 action으로 만들어진 것인지 확인하기 위해 action-rate와 feet-slide를 본다.

last-100 기준:

- action-rate term: **-0.08430**
- feet-slide term: **-0.05934**

2900 주변 last-100은 각각:

- action-rate: `-0.08626`
- feet-slide: `-0.06145`

즉 2998은 2900보다 **XY tracking이 좋아졌음에도 action-rate와 feet-slide penalty는 오히려 덜 나쁘다.**

이 점은 중요하다. 2998의 linear tracking 향상이 단순히 “발을 더 난폭하게 휘두르거나 미끄러뜨려서 속도만 맞춘 결과”라는 해석과는 잘 맞지 않는다.

다만 H-007 전체 역사로 보면 early checkpoint보다 late action variability가 커진 것은 사실이므로, “2998이 절대적으로 매우 부드럽다”고까지 말하면 안 된다. 정확한 결론은 **late 후보들 중에서는 2998의 smoothness가 다시 회복되는 방향**이라는 것이다.

---

# 16. Reward Component Interpretation

2998 endpoint의 주요 reward component:

| Component | Value @2998 | 해석 |
|---|---:|---|
| `track_lin_vel_xy_exp` | 0.61185 | 주요 양의 보상, late specialization 축 |
| `track_ang_vel_z_exp` | 0.07711 | yaw tracking 약함 |
| `ang_vel_xy_l2` | -0.02849 | body angular motion penalty 존재 |
| `action_rate_l2` | -0.08310 | late 후보 중 비교적 회복 |
| `feet_air_time` | 0.00606 | 작지만 정상 stepping과 모순 없음 |
| `flat_orientation_l2` | -0.01312 | orientation penalty는 폭발하지 않음 |
| `termination_penalty` | -0.01985 | aggregate termination cost 유지 |
| `feet_slide` | -0.05869 | 존재하지만 late 2900보다 개선 |

`Train/mean_reward=5.0285` 자체는 2998의 품질을 대표하지 않는다. H-007에서는 raw reward peak가 쉬운 terrain recovery 구간에서 발생했고 automatic best도 locomotion 목적과 어긋났다.

따라서 2998은 **mean reward가 낮아서 나쁜 checkpoint가 아니라, reward scalar와 실제 목적축이 분리된 late specialist checkpoint**다.

---

# 17. Local Optimum / Reward Hacking Check

현재 자료에서 classic reward hacking evidence는 약하다.

| 위험 패턴 | 관측 여부 | 근거 |
|---|---|---|
| 누워서 생존 | 없음 | 6개 영상 모두 upright |
| 제자리 survival | 없음 | 지속적인 실제 이동 |
| 반복 hopping | 없음 | alternating biped stepping |
| terrain 회피 | 뚜렷하지 않음 | rough/stairs/boxes region 직접 진입 |
| slip으로 속도만 획득 | 강한 증거 없음 | feet-slide late 개선 + 영상상 stepping |
| linear만 추종하고 yaw 무시 | **부분 위험** | XY 개선과 yaw≈2.0의 trade-off |

따라서 2998의 가장 현실적인 local-optimum 위험은 “걷지 않는 꼼수”가 아니라 **translation-specialized policy가 turning objective를 충분히 고려하지 않는 방향**이다.

---

# 18. Model 2998의 강점

1. **H-007 late checkpoint 중 가장 강한 XY tracking 후보**
2. 마지막 200 → 100 → 50 iteration으로 갈수록 XY error가 감소
3. terrain level 약 5.37 유지
4. base-contact가 late window에서 약 30~31%로 붕괴하지 않음
5. 6개 terrain 영상에서 명백한 낙상 없음
6. stairs/inverted-stairs의 discontinuity를 실제 stepping으로 통과
7. random rough에서 지속적인 foot placement adaptation 확인
8. boxes에서 큰 자세 교란 후 recovery 직접 확인
9. ±10° slope에서 20초 upright locomotion 유지
10. late 2900 대비 action-rate / feet-slide가 개선
11. checkpoint actor/critic/optimizer 모두 finite
12. stationary/hopping/prone 형태 reward hacking 증거 없음

---

# 19. Model 2998의 약점

1. **Yaw error≈2.0** — 가장 큰 정량 약점
2. endpoint base-contact 32.69%, episode 705.55로 단일 point는 좋지 않음
3. boxes에서 recovery는 성공하지만 큰 자세 excursion이 있어 margin이 넓어 보이지 않음
4. forward vs lateral tracking 분리 불가
5. stop / restart 성능 미측정
6. push recovery 미측정
7. 각 terrain 영상이 1 trajectory라 반복 성공률 없음
8. 동일 parent + reward unchanged resume-control이 없어 H-007 reward 변경의 순수 인과효과는 증명되지 않음
9. seed 42 단일 run
10. 제공 영상 MP4 자체에는 checkpoint hash가 없어 model2998 연결은 user provenance에 의존

---

# 20. Final Decision

## 체크포인트 자체

**판정: PROMOTE TO FIXED EVALUATOR / FINAL-CANDIDATE POOL**

2998을 더 이상 “로그상 후보”로만 둘 이유는 없다. 이번 6개 영상으로 실제 terrain locomotion과 recovery가 확인되었고, late-window quantitative tracking에서도 가장 강하다.

따라서 **model_2998은 H-007에서 우선적으로 실제 시나리오 평가를 돌릴 체크포인트**다.

## 최종 제출 확정 여부

**아직 HOLD.**

이유는 모델이 나빠서가 아니라, 다음 세 가지 핵심 검증이 비어 있기 때문이다.

1. yaw / turning fixed scenario
2. forward-vs-lateral 분리 score
3. 반복 trial 기반 terrain/fall success rate

2998이 이 세 gate를 통과한다면 late checkpoint 중 최종 제출 후보로 매우 강해진다.

---

# 21. 가장 정보량 높은 다음 검증

새 학습을 바로 돌리기 전에 2998에 대해 아래 evaluator를 먼저 돌리는 것이 효율적이다.

## A. Linear tracking

- vx command RMSE
- vy command RMSE
- command switch 후 settling time
- overshoot

## B. Yaw

- ±yaw command RMSE
- stationary turning
- translation + turning 복합 명령

## C. Stop behavior

- command = 0에서 drift distance
- stop 후 restart latency

## D. Terrain repeatability

각 terrain을 적어도 여러 seed / spawn에서 반복하여:

- success/fall count
- traversal progress
- mean episode duration
- base-contact termination

을 저장해야 한다.

## E. 후보 checkpoint head-to-head

최소한 `model_2900`과 `model_2998`은 같은 evaluator에서 붙이는 것이 좋다.

- 2900: 약간 더 좋은 internal survival
- 2998: 더 좋은 XY/yaw/action-rate/feet-slide late-window

현재 자료에서는 **2998을 1순위로 평가하고 2900을 stability backup으로 두는 구성이 가장 합리적**이다.

---

# 22. Confidence & Limitations

## 높은 신뢰

- checkpoint 내부 iter=2998
- checkpoint SHA 및 tensor finite 상태
- TensorBoard endpoint / late-window 수치
- XY tracking의 late improvement
- yaw≈2.0 약점
- 6개 영상의 형식과 길이
- 영상에서 명백한 fall/prone/hopping이 없음
- boxes에서 visible recovery가 발생

## 중간 신뢰

- 2998의 gross terrain robustness가 late 2900보다 전체적으로 뒤지지 않는다는 판단
- linear tracking 향상이 gait quality를 심각하게 파괴하지 않았다는 판단
- box disturbance recovery가 실제 competition-like robustness에 도움이 될 가능성

## 판단 불가 / 추가 평가 필요

- 공식 시뮬레이션 점수
- terrain별 실제 성공률
- vx/vy 각각의 오차
- zero-command drift
- push recovery
- yaw scenario score
- multi-seed generalization
- 영상이 checkpoint 파일 hash와 cryptographically 연결되는지 여부

---

# 23. Bottom Line

`model_2998.pt`는 **“linear tracking을 얻기 위해 안정성을 잃은 실패 정책”은 아니다.**

정량적으로는 마지막 100회 XY error가 `0.3294`까지 개선되면서 terrain `5.3725`, base-contact `30.78%`, timeout `69.23%`를 유지한다. 정성적으로는 random rough, stairs, inverted stairs, boxes, ±10° slope에서 약 20초씩 직립 locomotion을 수행하고, boxes에서는 큰 자세 교란 뒤에도 recovery한다.

따라서 현재 evidence가 지지하는 가장 정확한 요약은 다음과 같다.

> **Linear tracking: 강함 / Gross terrain stability: 유지 / Recovery: 확인 / Smoothness: late 회복 / Yaw tracking: 약함**

현재 H-007에서 실제 평가에 올릴 첫 체크포인트는 **`model_2998.pt`**가 맞다. 다만 최종 선택은 반드시 yaw·vx/vy·stop·반복 terrain evaluator 결과와 함께 결정해야 한다.

정확도 : 97%
