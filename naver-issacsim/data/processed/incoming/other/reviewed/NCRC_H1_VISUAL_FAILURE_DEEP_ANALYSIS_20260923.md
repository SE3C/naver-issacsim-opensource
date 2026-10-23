# NCRC H1 공개 실패 영상 심층 행동 분석

분석일: 2026-09-23

## 1. 목적과 범위

이 문서는 `NCRC_H1_VISUAL_FAILURE_ANALYSIS_20260923.zip`에 포함된 공개 H1 실패 영상 가운데 다음 5건을 우선 심층 분석한다.

- `reel-78394459`: `action_rate_l2 -0.0005 → -0.0025` 단독 기록
- `reel-60061435`: `track_ang_vel_z_exp 0.5 → 1.0` 단독 기록
- `reel-11999811`: `track_lin_vel_xy_exp 0.5 → 1.0` 단독 기록
- `reel-93039572`: 낮은 fall rate에도 진행 정체가 의심되는 장기 사례
- `reel-14106372`: 높은 best reward·terrain level에도 실패로 분류된 사례

원칙은 수치나 공개 failure label을 영상 관찰 결과로 복사하지 않고, 먼저 실제 화면에서 보이는 행동을 기록한 뒤 메타데이터와 대조하는 것이다. 각 영상은 20초 선택 장면이며 동일 parent, seed, evaluator, command, camera, policy SHA가 통제되지 않았으므로 reward의 인과 효과를 판정하지 않는다.

## 2. 핵심 발견 요약

### 발견 A — 낮은 fall rate는 task progress를 보장하지 않는다

`reel-93039572`는 메타데이터상 마지막 10회 평균 fall rate가 12.9%로 낮지만, 영상에서는 가파른 계단 앞에서 한쪽 다리를 과도하게 들어 올리는 동작과 큰 다리 스윙을 반복하며 20초 안에 명확한 계단 상승을 보여주지 못한다. 생존과 traversal을 분리해 측정해야 한다.

### 발견 B — 낮은 action std도 좋은 정책을 의미하지 않는다

`reel-78394459`의 exploration std는 0.419로 5건 중 가장 낮지만, 영상에서는 여러 environment의 H1이 좁은 범위에서 짧고 굽힌 보행을 반복하거나 일부가 무너져 있는 장면이 보인다. 메타데이터의 terrain 3.4→0.0, fall 100%와 합치면 “무작위성이 줄어든 나쁜 정책” 가능성을 반드시 고려해야 한다. action std 단독 success criterion은 부적절하다.

### 발견 C — 높은 reward·terrain level도 gait pathology를 가릴 수 있다

`reel-14106372`는 best reward 26.61, terrain 5.90으로 수치상 매우 높지만, 내리막 영상에서는 한쪽 무릎을 지속적으로 높게 들어 올리는 hop/skip형 비대칭 보행과 큰 자세 진동이 반복된다. 선택된 20초 안에서는 명확한 낙상이 보이지 않으므로 “높은 reward인데 실제로 즉시 넘어진다”가 아니라 “높은 reward·terrain과 비정상 gait quality가 공존할 수 있다”가 정확한 관찰이다.

### 발견 D — aggregate fall metric과 한 개의 20초 클립은 서로 다른 것을 본다

`reel-60061435`는 fall 83.1%지만 선택된 20초 영상에서는 로봇이 대체로 서 있는 상태를 유지한다. 대신 교차 보폭·측면 스텝·방향 변화가 두드러진다. 따라서 공개 fall rate를 20초 클립에서 재현하려 하거나, 영상 한 편에서 낙상이 안 보인다고 stats가 틀렸다고 판단하면 안 된다.

### 발견 E — linear tracking 실패는 단순 “과속 후 낙상”보다 progress/heading failure로 볼 가치가 있다

`reel-11999811`은 계단 상승 지형이지만, 영상에서 H1은 계단 앞 평지에서 자세가 흐트러지고 이후 계단 lane을 명확하게 타고 올라가지 못한다. 선택 구간에서 뚜렷한 정상 stair traversal은 확인되지 않는다. 따라서 내부 `track_lin_vel_xy_exp` 실험은 XY error만이 아니라 forward progress, lateral drift, obstacle engagement, stair ascent count를 함께 봐야 한다.

## 3. 사례별 심층 판독

### 3.1 `reel-78394459` — action-rate 단독 기록

**메타데이터**

- terrain: 기둥 숲
- checkpoint: iter 4300 / 총 5000
- reward dial: `action_rate_l2 -0.0005 → -0.0025`
- best reward: 0.42 @ 4288
- terrain: 3.4 → 0.00
- fall rate: 100.0% (마지막 10회 평균)
- std: 0.419

**영상 관찰**

- 약 6초 부근부터 화면에 이미 바닥에 무너져 있는 개체가 보인다.
- 약 7~13초 확대 구간에서는 여러 environment의 H1이 동시에 보이므로 한 개체를 연속 추적하기 어렵다.
- 확대 구간의 다수 개체는 무릎을 굽힌 채 짧은 스텝을 반복하거나 좁은 영역에서 자세를 유지하려는 모습이 두드러진다.
- 일부 개체는 옆으로 크게 기울거나 바닥에 무너져 있으며, 기둥 숲을 일관되게 통과하는 명확한 traversal은 확인되지 않는다.
- 카메라가 여러 env를 줌인/아웃하므로 실제 이동거리의 정량 판독은 불가하다.

**수치와의 대조**

- terrain collapse와 fall 100%라는 aggregate 진단은 영상의 다수 정체·무너짐 장면과 방향이 맞는다.
- 반면 std 0.419는 낮다. 영상상 행동 품질은 좋지 않으므로 “낮은 std = 잘 학습됨”이라는 해석은 반례를 맞는다.
- 이 영상만으로 `action_rate_l2=-0.0025`가 원인이라고 할 수 없다. 동일 parent control이 없고 여러 env를 한 화면에 담는다.

**내부 평가에 추가할 항목**

1. command speed 대비 실제 pelvis speed response
2. 1초 이상 저속 상태의 stall ratio
3. action-delta RMS와 실제 이동거리의 동시 기록
4. 발 clearance와 짧은 shuffle step 비율
5. obstacle 전방 progress / 통과거리
6. fall뿐 아니라 “upright but non-progressing”을 별도 failure로 기록

### 3.2 `reel-60061435` — yaw tracking 단독 기록

**메타데이터**

- terrain: 거친 요철
- checkpoint: iter 999 / 총 1000
- reward dial: `track_ang_vel_z_exp 0.5 → 1.0`
- best reward: 4.67 @ 968
- terrain: 0.01
- fall rate: 83.1%
- std: 0.763

**영상 관찰**

- 선택된 20초 동안 H1은 대부분 upright 상태를 유지한다.
- 다리 배치가 전후로 깔끔하게 반복되기보다 교차하거나 옆으로 벌어지는 프레임이 반복된다.
- 몸통과 진행 방향이 프레임마다 바뀌는 모습이 있으며, rough terrain 위에서 안정적인 직선 보행으로 보기 어렵다.
- follow camera 때문에 실제 world-frame 이동거리와 heading drift의 절대량은 판별하기 어렵다.
- 선택 구간에서는 명확한 full fall이 확인되지 않는다.

**수치와의 대조**

- fall 83.1%는 이 20초 한 클립에서 직접 재현되지 않는다. 이는 통계가 틀렸다는 증거가 아니라 aggregate window와 selected clip의 차이다.
- terrain 0.01과 영상의 불안정한 foot placement는 “정상 rough-terrain traversal이 정착되지 않았다”는 방향에서는 일치한다.
- 내부 YAW075 1K에서 terrain 0 / base-contact 100%가 나온 사실과 방향은 비슷하지만, 서로 다른 run이므로 동일 failure mode라고 단정하지 않는다.

**내부 평가에 추가할 항목**

1. fixed yaw command에서 yaw-rate tracking error
2. world-frame lateral drift
3. cross-step 빈도 / stance-width 변동
4. 회전 명령 종료 후 residual spin
5. stop-command에서 heading oscillation
6. fall 여부와 별도로 5~10초간 heading stability

### 3.3 `reel-11999811` — linear tracking 단독 기록

**메타데이터**

- terrain: 계단 올라가기
- checkpoint: iter 900 / 총 1000
- reward dial: `track_lin_vel_xy_exp 0.5 → 1.0`
- best reward: 4.51 @ 902
- terrain: 0.90
- fall rate: 76.5%
- std: 1.259

**영상 관찰**

- 초기 구간에서 H1은 계단 근처 평지에 서 있으며 이동을 시작한다.
- 약 3~5초 부근에 몸통이 기울고 진행축이 계단 정면과 어긋나는 장면이 보인다.
- 이후 crane camera가 멀어지면서 로봇은 계단 구조 주변 평지에 남아 있는 모습이 이어진다.
- 20초 안에 계단을 연속적으로 올라가는 명확한 성공 장면은 확인되지 않는다.
- 카메라 이동이 커서 정확한 속도 overshoot나 총 이동거리 측정은 불가능하다.

**수치와의 대조**

- 낮은 terrain 0.90과 높은 fall 76.5%는 “계단 task progress가 불충분”하다는 영상 관찰과 방향이 맞는다.
- 하지만 영상에서 명확한 고속 질주→낙상 패턴은 확인되지 않는다. 공개 dial 설명의 “과속 시 넘어짐”을 이 영상의 관찰 사실로 승격하면 안 된다.
- 우리 H-007은 같은 `0.5→1.0`을 썼지만 실제 계보상 `feet_air_time -0.2→+0.2`도 동시에 바뀌었다. 따라서 외부 단독 기록은 corrected-parent 내부 rerun 질문의 우선도를 높이는 참고 prior로만 사용한다.

**내부 평가에 추가할 항목**

1. commanded forward velocity 대비 actual velocity overshoot
2. forward displacement / 20s
3. lateral displacement / forward displacement
4. 계단 첫 접촉까지 시간
5. 실제 오른 stair riser 수 / 20s
6. obstacle 앞 stall time
7. base pitch/roll RMS와 fall 직전 spike

### 3.4 `reel-93039572` — 낮은 fall, 진행 정체

**메타데이터**

- terrain: 가파른 계단 15~30cm
- checkpoint: iter 8300 / 총 10000
- dials: `track_lin_vel_xy_exp 0.5→1.0`, `termination_penalty -5→-200`
- best reward: 4.58 @ 8311
- terrain: 3.4 → 3.74
- fall rate: 12.9%
- std: 2.593

**영상 관찰**

- H1은 영상 대부분에서 서 있는 상태를 유지한다.
- 계단으로 접근하지만 한쪽 무릎을 매우 높이 들어 올리고 반대 다리로 버티는 자세가 반복된다.
- 약 10초 이후 계단 바로 앞/옆에서 큰 다리 스윙, 옆으로 뻗는 동작, 긴 single-support 자세가 반복된다.
- 영상 끝까지 명확한 stair ascent가 보이지 않는다.
- 즉 “안 넘어지는 시간”은 길지만 locomotion objective인 계단 진행은 매우 제한적으로 보인다.

**수치와의 대조**

- fall 12.9%는 영상의 생존성과 잘 맞는다.
- 그러나 낮은 fall을 성능으로만 읽으면 영상상 stall/hopping을 놓친다.
- std 2.593이라는 매우 높은 값은 큰 사지 동작과 방향상 일치하지만, 이 값이 동작의 원인이라고 할 수는 없다.
- 공개 label의 `JITTERY JOINTS`는 영상의 큰 프레임간 다리 자세 변화와 질적으로 부합한다. 다만 실제 고주파 jitter의 Hz나 action oscillation은 원본 joint/action 로그 없이 정량화할 수 없다.

**내부 평가에 추가할 항목**

1. survival과 task progress를 별도 축으로 분리
2. stair ascent count / vertical progress
3. obstacle-contact 후 2초 내 progress 여부
4. one-foot support 지속시간 분포
5. foot-contact 좌우 duty-cycle imbalance
6. joint velocity high-frequency energy 또는 action-delta spectrum
7. upright-but-stalled time

### 3.5 `reel-14106372` — 높은 reward·terrain, 비정상 gait

**메타데이터**

- terrain: 내리막 경사
- checkpoint: iter 9700 / 총 10000
- best reward: 26.61 @ 9658
- terrain: 5.90
- fall rate: 21.5%
- std: 1.155
- 동시에 변경된 reward 8개: linear tracking, yaw tracking, feet air time, termination, flat orientation, hip/torso deviation, action rate

**영상 관찰**

- H1은 선택된 20초 동안 대체로 upright 상태이며 경사면 위에서 이동한다.
- 그러나 한쪽 무릎을 반복적으로 매우 높이 들어 올리는 hop/skip형 보행이 지속된다.
- 좌우 다리의 자세와 지지 시간이 대칭적인 정상 alternating gait로 보이지 않는다.
- 몸통 pitch/roll과 다리 스윙 진폭도 비교적 크다.
- 선택 구간에서 명확한 full fall은 확인되지 않는다. 따라서 공개 `LOSS OF BALANCE` 문구를 “영상에서 실제 낙상 확인”으로 읽으면 안 된다.

**수치와의 대조**

- high reward 26.61과 terrain 5.90은 정책이 curriculum 내부에서 상당한 진행을 했음을 시사하지만, 영상은 gait quality가 여전히 비정상일 수 있음을 보여준다.
- 이 사례는 mean reward/terrain level을 최종 policy-quality proxy로 단독 사용하지 말아야 하는 강한 시각적 근거다.
- 8개 reward가 동시에 바뀌었기 때문에 어떤 reward가 hopping이나 자세 자유를 만들었다는 인과 분해는 금지한다.

**내부 평가에 추가할 항목**

1. foot-contact 좌우 대칭성
2. 연속 single-leg dwell time
3. pelvis vertical velocity / body-height oscillation
4. base roll/pitch RMS와 peak
5. step-frequency regularity
6. lateral drift
7. progress를 유지하면서 gait pathology가 생기는지 영상 확인

## 4. 다섯 영상에서 도출되는 행동 failure taxonomy

| 유형 | 대표 key | 화면에서 보이는 핵심 | 기존 metric이 놓치는 부분 |
|---|---|---|---|
| Converged bad / stall-collapse | `reel-78394459` | 낮은 std인데 짧은 보폭·정체·무너짐 | std 감소를 학습 성공으로 오해 가능 |
| Heading/foot-placement instability | `reel-60061435` | upright지만 교차·측면 스텝과 방향 불안정 | 20초 clip에는 fall이 없어 aggregate fall과 괴리 |
| Progress/heading failure | `reel-11999811` | 계단 task인데 명확한 stair ascent 없음 | XY tracking reward만 보면 obstacle engagement를 놓침 |
| Safe-but-nonfunctional | `reel-93039572` | 거의 안 넘어지지만 high-knee/hopping 상태로 계단 앞 정체 | survival/fall만 보면 좋은 정책처럼 보임 |
| High-score pathological gait | `reel-14106372` | 높은 reward/terrain에도 비대칭 hop/skip gait | reward·terrain이 gait quality를 완전히 대표하지 못함 |

## 5. 성공 분류 영상과의 질적 참고

동봉된 성공 분류 영상은 동일 parent/seed/evaluator가 아니므로 성능 비교용이 아니다. 다만 행동 형태를 정의하는 참고로는 쓸 수 있다.

- `reel-9586400`(계단 올라가기 성공 분류): 선택 프레임에서 H1이 계단 접근/이동 구간을 비교적 연속적인 보행으로 수행하는 장면이 보인다. `reel-11999811`처럼 계단 lane 주변에서 진행이 끊기는 모습과 질적으로 다르다.
- `reel-97612025`(가파른 계단 성공 분류): 여러 env가 보이는 wide shot이라 개별 policy 추적은 어렵지만, 여러 개체가 계단 영역을 실제로 점유하며 진행하는 장면이 있다. `reel-93039572`의 한 개체가 계단 앞에서 고관절/무릎 동작만 크게 반복하는 장면과 대비된다.
- `reel-77792863`(기둥 숲 성공 분류): 다수 env가 보이는 영상이므로 직접 비교는 어렵지만, obstacle field 내부에 분산된 upright 개체들이 확인된다. `reel-78394459`의 줌 구간에서는 다수 개체가 좁은 영역에 뭉쳐 있거나 무너진 모습이 더 두드러진다.
- `reel-78202966`(완만한 경사 성공 분류): 여러 개체가 경사면을 따라 이동하며, `reel-14106372`에서 보이는 지속적인 한쪽 high-knee hop 형태가 모든 개체의 공통 동작으로 나타나지는 않는다.

이 비교는 오직 “어떤 시각적 체크 항목을 만들 것인가”에만 사용한다.

## 6. 우리 내부 H1 실험과 연결

### 6.1 `track_lin_vel_xy_exp`

우리 H-007의 기록값은 `0.5→1.0`으로 외부 `reel-11999811`과 동일하지만, H-007은 실제로 `feet_air_time -0.2→+0.2`도 같이 바뀌어 clean single-delta가 아니다. 따라서 corrected +0.2 parent에서 `track_lin_vel_xy_exp`만 바꾸는 rerun이 여전히 필요하다.

영상 분석으로 추가된 핵심은 판정 지표다. 단순 XY error가 아니라 **forward displacement, lateral drift, obstacle engagement, stair ascent count, stall time**을 반드시 같이 본다.

### 6.2 `track_ang_vel_z_exp`

우리 YAW075 1K는 terrain 0 / base-contact 100%였고, 외부 `reel-60061435`의 YAW100도 terrain 0.01 / fall 83.1%다. 두 자료는 서로 독립이므로 인과 증거는 아니지만 “초기 H1에서 yaw tracking을 크게 단독 강화했을 때 collapse/instability가 나타나는가?”라는 질문의 내부 검증 가치는 높인다.

영상 분석 때문에 다음 yaw 실험에서는 fall 외에 **cross-step, lateral drift, residual spin, heading oscillation**을 측정해야 한다.

### 6.3 `action_rate_l2`

우리 내부에는 외부 `-0.0005→-0.0025`에 대응하는 clean single-delta가 없다. 따라서 외부 5건 가운데 신규 정보량이 가장 큰 축 중 하나다.

단, `reel-78394459`은 “강한 action-rate penalty가 실패의 원인”을 증명하지 않는다. 내부 실험을 한다면 핵심 질문은 다음과 같아야 한다.

> 같은 parent에서 `action_rate_l2`만 `-0.0005→-0.0025`로 강화했을 때 action 변화량은 줄지만, command response와 terrain progress까지 같이 줄어 stall/shuffle이 늘어나는가?

판정에는 action smoothness와 progress를 동시에 넣는다.

### 6.4 `termination_penalty`

우리 TERM50은 survival/terrain anchor로 이미 많은 evidence가 있다. `reel-93039572`는 termination -200과 linear tracking 1.0이 함께 들어가 fall 12.9%인데도 stair progress가 나쁘다. 이 사례는 termination 값을 더 세게 하는 질문보다 **survival을 progress와 분리해서 평가해야 한다**는 교훈이 더 크다.

### 6.5 `feet_air_time` / hip deviation

`reel-14106372`에는 feet_air_time 0.35 등 8개 reward 변경이 섞여 있고 hop/skip gait가 보이지만, 특정 reward의 원인 효과로 분리할 수 없다. 우리 H-010 AIRTIME025는 unchanged control과 사실상 tie였고 현재 lineage correction 때문에 HOLD다. 따라서 이 영상만으로 feet_air_time 우선도를 올릴 근거는 부족하다.

## 7. 다음 내부 고정 평가 프로토콜에 바로 추가할 항목

### 필수 정량 metric

1. **Progress**
   - forward displacement
   - terrain-specific vertical progress / stair count
   - obstacle first-contact → successful progress latency
   - upright-but-stalled time

2. **Tracking**
   - XY velocity error
   - yaw-rate error
   - lateral drift
   - command 종료 후 residual drift/spin

3. **Stability**
   - fall/base-contact
   - base roll/pitch RMS 및 peak
   - recovery time after large tilt/contact
   - episode length / survival

4. **Gait quality**
   - left/right foot contact duty cycle
   - longest single-leg support duration
   - foot clearance distribution
   - pelvis vertical oscillation
   - cross-step count

5. **Control smoothness / exploration**
   - action-delta RMS
   - joint velocity/acceleration high-frequency energy
   - action std
   - 위 값들을 progress와 함께 해석

### 필수 영상 annotation

각 20초 또는 고정 evaluator episode마다 다음을 사람이 한 번 확인한다.

- 정상 전진/통과
- obstacle 앞 stall
- 발 끌림/걸림
- 한 발 들기 지속
- hopping/skip
- cross-step
- 상체 pitch/roll 흔들림
- 반복되는 큰 관절 reversal
- 접촉 후 회복 여부
- 방향 이탈
- 낙상/리셋

## 8. 실험 우선순위에 미치는 영향

### A. 바로 검증 가치가 높은 것

1. **corrected-parent linear tracking single-delta**
   - 이유: 외부 `reel-11999811`이 정확히 0.5→1.0 단독 기록이며 영상에서도 stair progress 실패가 보인다.
   - 내부: H-007/H-008은 lineage confounder 때문에 재실험 필요.
   - 추가 판정: XY error + stair progress + lateral drift + stall.

2. **yaw micro-step single-delta**
   - 이유: 외부 YAW100과 내부 YAW075 모두 early collapse 방향이지만 영상은 단순 fall보다 foot-placement/heading instability를 시사한다.
   - 다음 값은 기존 계획대로 큰 점프보다 작은 micro-step을 우선 검토한다.
   - 추가 판정: yaw error + cross-step + lateral drift + residual spin.

3. **action-rate negative-control/screen**
   - 이유: 내부에 clean evidence가 없고 외부 단독 사례가 강한 collapse signal이다.
   - 목적: 값을 채택하려는 실험이 아니라 stall-sensitive evaluator를 검증하는 정보 실험.
   - 추가 판정: action smoothness와 progress 동시 측정.

### B. 우선순위를 낮춰도 되는 것

- termination을 더 강하게만 만드는 실험: 이미 내부 TERM50 evidence가 있고, `reel-93039572`는 낮은 fall이 progress를 보장하지 않는다는 쪽이 더 중요한 정보다.
- feet_air_time 단독 추가 sweep: `reel-14106372`의 hopping은 8개 reward confounded이고, 내부 H-010도 control 대비 결정적 이득이 없었다.
- mean reward 최대화: `reel-14106372`가 시각적으로 강한 반례다.

## 9. 가장 중요한 실험 설계 변경

앞으로 H1 single-delta run은 **“reward가 올랐는가?”가 아니라 다음 네 질문을 동시에 통과해야 한다.**

1. 안 넘어지는가? — survival
2. 실제로 목표 방향/지형을 진행하는가? — progress
3. 명령을 맞게 따르는가? — tracking
4. 이상한 gait hack 없이 걷는가? — gait quality

이 네 축 가운데 하나라도 빠지면 `reel-93039572` 같은 safe-but-stalled policy나 `reel-14106372` 같은 high-score pathological gait를 좋은 정책으로 오판할 수 있다.

## 10. 한계

- 각 영상은 20초 선택 장면이며 전체 evaluator episode가 아니다.
- 카메라가 crane/follow/orbit/zoom으로 달라 world-frame 이동거리를 영상만으로 정량화할 수 없는 경우가 많다.
- 일부 영상은 여러 environment의 로봇을 동시에 보여 개별 policy trajectory를 연속 추적하기 어렵다.
- 공개 stats의 fall rate window와 영상 구간은 동일하다고 보장되지 않는다.
- command vector가 화면에 표시되어도 정확한 수치 command history는 제공되지 않는다.
- 성공 분류 영상은 동일 parent·seed·reward·evaluator가 아니므로 qualitative reference일 뿐이다.
- joint/action raw log가 없으므로 “jitter”는 시각적 limb reversal로만 관찰할 수 있고 주파수·진폭의 정량 판정은 내부 evaluator에서 새로 측정해야 한다.

## 결론

이번 영상 분석의 가장 큰 수확은 새로운 reward 값을 찾은 것이 아니라 **우리 evaluator가 반드시 잡아야 할 failure mode가 구체화된 것**이다.

- `reel-78394459`: 낮은 std인데도 converged bad/stall-collapse가 가능
- `reel-60061435`: aggregate fall과 한 클립의 upright behavior가 공존 가능
- `reel-11999811`: tracking 강화 실패를 speed error만으로 보면 stair progress failure를 놓침
- `reel-93039572`: low-fall safe-but-nonfunctional 정책의 명확한 시각적 사례
- `reel-14106372`: high-reward/high-terrain pathological gait의 명확한 시각적 사례

따라서 다음 내부 H1 실험은 **progress + tracking + stability + gait quality**의 4축 evaluator로 판정해야 하며, 이 기준에서 가장 정보가 큰 single-delta 질문은 corrected-parent linear tracking, yaw micro-step, action-rate negative-control 순이다.
