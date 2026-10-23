# NCRC 외부 실패 데이터 — 내부 실험 DB 연계용 단일 정리본

작성일: 2026-09-22  
대상: NAVER CONNECT Robotics Cup 2026 연구 기록 페이지의 `videos.json` 기반 외부 관찰 데이터  
목적: 우리 내부 H1/Go2 실험 DB에 **직접 trial로 합치지 않고**, 외부 실패 prior·탐색공간 보조·가설 생성 자료로 활용하기 위한 정리

---

## 1. 결론

이 데이터는 **유익하다. 다만 정식 Optuna trial 또는 인과 검증 데이터로 넣으면 안 된다.**

현재 확보한 외부 데이터의 가장 큰 장점은 다음과 같다.

- 다른 참가자의 실제 reward 변경 항목과 변경 폭을 볼 수 있음
- 각 실패 run에 대해 terrain, robot, checkpoint iteration, 최고 reward, terrain level, fall rate, exploration std가 구조화돼 있음
- 45개의 실질 상세 실패 기록에서 reward 조정과 실패 진단을 연결할 수 있음
- 우리 내부 DB가 깊은 단일-run 분석에 강한 반면, 이 자료는 **여러 참가자·여러 지형에 걸친 폭넓은 실패 사례**를 제공함
- 따라서 **외부 실패 prior**, **탐색범위 보조**, **새 단일변수 가설 생성**에 유용함

반면 다음이 보장되지 않는다.

- 동일 parent checkpoint
- 동일 seed
- 동일 evaluator
- 동일 scenario
- 동일 training length
- 동일 environment config
- 동일 source hash / lineage
- 모든 reward term이 완전히 공개되었는지 여부

따라서 이 데이터를 `study.tell()`에 직접 넣거나 내부 공식 trial과 같은 무게로 비교하면 안 된다.

---

## 2. 현재 확보된 영상/상세 데이터 규모

전체 영상 수:

- 총 84개

playlist별:

| 구분 | 총 영상 | 실질 상세 데이터 |
|---|---:|---:|
| 실패 기록 | 47 | 45 |
| 성공 기록 | 34 | 0 |
| 대회 기록 | 3 | 0 |

중요:

- 모든 영상에 `detail` 객체 자체는 존재할 수 있음
- 그러나 성공 기록과 대회 기록의 `detail`은 실질적으로 비어 있음
- 실패 기록 47개 중 45개에 유효한 상세 데이터가 존재
- 45개 중 44개에는 `dials`가 존재
- 45개 모두 `stats`, `why`, `bias`, `timing`, `meta`가 대부분 존재
- `warns` 필드는 스키마에는 존재하나 현재 확인된 45개에서는 사용되지 않음

---

## 3. 외부 상세 데이터 스키마

### 3.1 영상 객체

확인된 주요 필드:

```text
camera
day
desc
detail
iterations
key
mp4
robot
school
team
terrain
thumb
title
youtubeUrl
```

분석용으로 추가한 필드:

```text
playlist
playlistName
```

### 3.2 detail 객체

실제 확인된 필드:

```text
bias
dials
meta
ndial
note
sev
stats
timing
warns
why
```

| 필드 | 의미 |
|---|---|
| `bias` | reward 변경의 방향성/튜닝 의도 요약 |
| `dials` | 실제 변경된 reward 항목 |
| `meta` | robot/joint/checkpoint/총 학습량/model params 등의 메타 |
| `ndial` | 전체 dial 수 |
| `note` | 추가 메모 |
| `sev` | `ok` / `warn` / `bad` |
| `stats` | 학습 결과 지표 |
| `timing` | 학습 시작·종료·소요시간 |
| `warns` | 경고 목록 |
| `why` | 실패/진단 이유 |

---

## 4. 실제 reward dial 종류

현재 외부 실패 기록에서 확인된 reward 항목은 총 11종이다.

```text
action_rate_l2
ang_vel_xy_l2
feet_air_time
flat_orientation_l2
joint_deviation_hip
joint_deviation_torso
lin_vel_z_l2
termination_penalty
track_ang_vel_z_exp
track_ang_vel_z_exp (고급)
track_lin_vel_xy_exp
```

등장 빈도:

| reward dial | count |
|---|---:|
| `track_lin_vel_xy_exp` | 35 |
| `termination_penalty` | 31 |
| `action_rate_l2` | 27 |
| `feet_air_time` | 25 |
| `track_ang_vel_z_exp` | 23 |
| `ang_vel_xy_l2` | 20 |
| `flat_orientation_l2` | 20 |
| `joint_deviation_hip` | 13 |
| `joint_deviation_torso` | 13 |
| `lin_vel_z_l2` | 6 |
| `track_ang_vel_z_exp (고급)` | 1 |

총 reward 변경 row는 약 214개다.

---

## 5. 실제 baseline/변경 예시

### 5.1 Go2 샘플

```text
track_lin_vel_xy_exp   1     → 1.1
feet_air_time          0.01  → 0.05
lin_vel_z_l2          -3     → -4.5
ang_vel_xy_l2         -0.08  → -0.15
action_rate_l2        -0.01  → -0.02
```

관련 결과:

```text
best reward: 14.52 @ iter 693
terrain level: 0.00
fall rate: 14.0%
exploration std: 0.409
severity: bad
```

이 값들은 인과 증거가 아니라 **실패 parameter region의 관찰 사례**로만 사용한다.

### 5.2 H1 샘플

```text
track_lin_vel_xy_exp     0.5   → 1.4
track_ang_vel_z_exp      0.5   → 1.0
termination_penalty      -5    → -200
ang_vel_xy_l2           -0.05  → -0.1
joint_deviation_hip     -0.2   → -0.3
```

관련 결과:

```text
best reward: 4.77 @ iter 951
terrain level: 5.32
fall rate: 25.4%
exploration std: 2.798
severity: warn
```

여러 reward가 동시에 바뀌었으므로 단일변수 인과 추론은 금지한다.

---

## 6. 학습 지표 구조

실제 `stats`는 주로 다음 네 계열을 제공한다.

```text
최고 보상 · iter N
지형 난이도 ...
낙상률 ...
탐색 std ...
```

정규화하면:

```text
best_reward
best_reward_iter

terrain_level_start
terrain_level_end
terrain_level_direction

fall_rate
fall_rate_window

exploration_std
```

현재 `"학습 지표 이름"`이 52개로 보이는 이유는 실제 metric 종류가 52개이기 때문이 아니라, `최고 보상 · iter 693`처럼 iteration 숫자가 key 문자열에 섞여 있기 때문이다.

---

## 7. checkpoint iteration과 실제 총 학습량은 다를 수 있음

특이 사례:

```text
top-level iterations = 0
```

하지만 `detail.meta`:

```text
19관절 · iter 0 / 총 10 · 0.30M params
```

진단:

```text
학습을 총 10회 실행
checkpoint는 100회마다 저장
제출 파일은 사실상 iter 0 초기 가중치
```

따라서 DB에서는:

```text
checkpoint_iter
total_train_iter
```

를 분리해야 한다.

이 사례에서 추가 확인:

```text
robot: Unitree H1
joints: 19
model params: 0.30M
total_train_iter: 10
checkpoint_iter: 0
checkpoint interval: 100
training duration: 32 sec
camera: panorama

best reward: -0.19 @ iter 0
terrain level: 0.82
fall rate: 100.0%
exploration std: 0.991
ndial: 9
```

---

## 8. 우리 내부 DB와의 비교

### 8.1 내부 DB가 더 강한 부분

우리 내부 evidence/experiment DB는 다음을 더 엄격하게 관리한다.

```text
parent checkpoint
checkpoint hash
reward delta
official/personal
source hash
lineage
seed
training length
artifact
TensorBoard full curve
final checkpoint
evaluation condition
video provenance
```

event tag가 존재하면 다음 시계열도 0→마지막까지 복원 가능하다.

```text
Train/mean_reward
episode length
terrain progression
reward term별 값
KL
learning rate
entropy loss
value loss
surrogate loss
action std
```

즉 **한 run의 깊이와 신뢰도는 우리 DB가 훨씬 높다.**

### 8.2 외부 데이터가 더 강한 부분

외부 데이터는 다음에서 보완적 가치가 있다.

- 여러 참가자
- 여러 terrain
- 여러 reward 조합
- 다양한 실패 패턴
- reward 변경 방향성
- 자동 실패 진단
- fall rate
- terrain level
- exploration std
- 다양한 iteration 규모

요약:

```text
우리 DB = 좁고 깊음
외부 DB = 넓고 얕음
```

---

## 9. 내부 DB에 넣을 때 권장 구조

```text
internal_experiments/
  H-001
  H-002
  ...
  H-012
  ...
  → 공식/개인 실험
  → 인과 비교 가능성 검증
  → Optuna 후보

external_observations/
  NCRC_2026_failure_runs/
    source
    source_key
    day
    robot
    terrain
    checkpoint_iter
    total_train_iter
    training_duration
    model_params
    reward_deltas
    best_reward
    best_reward_iter
    terrain_level_start
    terrain_level_end
    terrain_level_direction
    fall_rate
    fall_rate_window
    exploration_std
    severity
    diagnosis
    bias
    camera
    mp4
    thumb
  → prior
  → 실패영역 탐색
  → 신규 가설 생성
```

---

## 10. 절대 하지 말아야 할 것

### 10.1 외부 row를 Optuna trial로 직접 입력

금지.

보장되지 않는 것:

```text
same parent
same seed
same evaluator
same scenario
same environment
same code
same training length
```

### 10.2 다중 변경 run에서 단일 reward 효과 추론

여러 reward가 동시에 바뀐 run에서 낙상률이 높았다고 특정 reward 하나의 원인으로 결론내리면 안 된다.

가능한 표현:

```text
이 조합은 외부 실패 사례에서 관찰됨.
동일 조건 single-delta 검증 필요.
```

### 10.3 `sev` / `why`를 독립 정답 label처럼 사용

`why`와 `severity`는 `stats`를 기반으로 자동 생성됐을 가능성이 높다.

반복 문구:

```text
자주 넘어짐
절반 이상 넘어짐
지형 난이도 0 수준
탐색 std가 1.0 근처
수치상 큰 이상 신호 없음
```

ML feature/label 설계에서 정보 누수를 주의한다.

---

## 11. 실제로 유익한 활용법

### A. 탐색 범위 보조

외부에서 실제로 시도된 값과 실패 영역을 보고 다음을 참고할 수 있다.

- 지나치게 큰 변경
- 반복 실패 조합
- exploration std 폭증 영역
- terrain collapse 영역

단, 범위를 확정하는 근거가 아니라 **prior**다.

### B. 새로운 single-delta 가설 생성

외부에서 반복적으로 쓰였지만 우리 내부 실험이 적은 항목:

```text
ang_vel_xy_l2
flat_orientation_l2
joint_deviation_torso
lin_vel_z_l2
```

등을 새로운 단일변수 가설 후보로 등록할 수 있다.

### C. terrain별 reward 우선순위 생성

예:

```text
stairs
rough
pit
stepping stones
rail
gap
slope
```

별로 어떤 reward가 자주 변경됐는지 집계한다.

### D. 실패 anomaly detector 보조

외부 로그의 주요 축:

```text
fall_rate
terrain_level
exploration_std
best_reward
```

이 네 축을 우리 내부 run health detector와 대조한다.

예:

```text
high reward + terrain collapse
low fall + high std
high terrain + high fall
reward peak before final
```

---

## 12. 우리 기존 탐색 설계와 겹치는 지점

우리 내부 탐색안의 주요 reward:

```text
track_lin_vel_xy_exp
track_ang_vel_z_exp
feet_air_time
joint_deviation_hip
joint_deviation_torso
action_rate_l2
termination_penalty
```

외부 실패 데이터에서도 동일 항목들이 반복적으로 등장한다.

Go2 쪽에서 외부 관찰 baseline은 다음과 같은 항목에서 내부 설계와 잘 맞는다.

```text
track_lin_vel_xy_exp ≈ 1.0
feet_air_time ≈ 0.01
lin_vel_z_l2 ≈ -3.0
```

이는 reward naming과 일부 baseline 구조가 동일 계열 환경에서 왔다는 점을 교차 확인하는 데 유용하다. 다만 동일 task config라고 단정하지 않는다.

---

## 13. 현재 데이터의 가치 등급

### 높은 가치

```text
reward term 목록
reward baseline → changed 값
terrain
robot
fall rate
terrain level
exploration std
best reward
best reward iter
checkpoint/total iter 분리 단서
training duration
model params 일부
```

### 중간 가치

```text
bias
severity
why
camera
video
```

### 낮은 가치 또는 주의 필요

```text
성공 기록의 reward 설정
정확한 인과 효과
직접 Optuna objective
공식 score 비교
```

---

## 14. 권장 DB 라벨

```yaml
source_class: external_observational
competition: NCRC_2026
source_surface: researchlog
causal_grade: non_causal
optuna_eligible: false
official_comparison_eligible: false
use_for:
  - prior
  - search_space_support
  - failure_region_screening
  - hypothesis_generation
  - anomaly_rule_design
```

---

## 15. 최종 판단

이 데이터는 **우리 데이터베이스에 넣을 가치가 충분히 있다.**

역할은 명확히 제한한다.

```text
정답 데이터 X
공식 trial X
인과 증거 X
Optuna observation X

외부 실패 prior O
탐색공간 보조 O
새 가설 생성 O
실패 parameter region 참고 O
terrain별 reward 우선순위 분석 O
anomaly detector 보조 O
```

가장 적절한 위치:

```text
external_observations/NCRC_2026_failure_runs
```

내부 `research/EXPERIMENTS.md`의 공식/개인 실험 lineage와는 분리한다.

---

## 16. 출처 메모

본 문서는 다음 자료를 바탕으로 정리되었다.

1. NCRC 연구 기록 페이지에서 추출한 `videos.json` 기반 84개 영상 메타데이터
2. 실질 상세 실패 기록 45개
3. reward dial 214개 관찰
4. 업로드된 콘솔 추출 결과
5. 프로젝트 내부 문서:
   - `15_OPTUNA_REWARD_DECISION_ENGINE`
   - `16_EXPERIMENT_EXPORT_AND_TENSORBOARD`
   - 기존 H1/Go2 experiment registry 및 evidence 설계 원칙

이 문서의 외부 데이터는 **관찰 자료**이며, 동일조건 통제 실험으로 간주하지 않는다.
