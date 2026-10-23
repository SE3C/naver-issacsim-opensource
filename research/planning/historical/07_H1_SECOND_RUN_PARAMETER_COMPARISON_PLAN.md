---
id: planning-h1-second-run-parameter-comparison
source_type: evidence_based_experiment_plan
category: official_server_experiment
robot: H1
created_at: "2026-08-24"
trust_level: recommendation_based_on_first_run_and_server_backup
authority: "다음 공식 서버 실험을 비교 가능하게 만드는 내부 계획이며 공식 성능 보장이나 규정 해석이 아니다."
---

> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/planning/historical/07_H1_SECOND_RUN_PARAMETER_COMPARISON_PLAN.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.


# H1 2차 공식 서버 reward 비교 실험 계획

> **현재 상태:** 2026-08-24 시점의 historical plan이다. 이후 `h1-submit-2 / TERM-50` fresh 5K 실행·Round-2 평가까지 완료됐으므로 이 문서를 현재 다음 Run 지시로 사용하지 않는다. `ORIENT-100` OFFICIAL fresh 3K는 2026-10-06 완료됐고, 2026-10-07 PERSONAL `model_2850` 분석은 HOLD다. 현재 상태와 비교 우선순위는 `research/EXPERIMENTS.md` 및 `data/processed/ai_library/14_H1_NEXT_RUN_PARAMETER_COMPARISON.md`를 따른다. `ACTRATE-001`은 별도 미실행 PLANNED다.

## 결론부터

첫 300-iteration 실행은 최종 report와 policy는 남았지만 TensorBoard event·전체 콘솔·GPU 시계열이 빠졌다. 따라서 **파라미터를 바꾼 실행 하나만 추가하면 첫 실행과 endpoint 일부는 비교할 수 있어도, iteration 0→299의 변화량을 정밀 비교할 수 없다.**

가장 신뢰도 높은 최소 실험은 다음 두 실행을 같은 서버 환경에서 연속 수행하는 것이다.

| 순서 | 실험 ID | reward 변경 | iterations | 목적 |
| --- | --- | --- | ---: | --- |
| 1 | `H1-B0-RECAPTURE` | 없음, baseline 그대로 | 300 | 첫 실행에서 빠진 전체 시계열을 재수집 |
| 2 | `H1-S1-TERM50` | `termination_penalty: -5 → -50`만 변경 | 300 | 같은 학습량에서 낙상 penalty의 초기 효과 분리 |

둘 다 seed 42, 4096 envs, 같은 코드·PPO·terrain·headless 조건으로 맞춘다. 실행마다 생성된 `logs/<run>/`과 exported 결과를 즉시 별도 폴더로 보존해 다음 실행이 덮어쓰지 않게 한다.

공식 서버 시간을 아끼기 위해 새 실행을 하나만 할 수 있다면 `H1-S1-TERM50`을 수행할 수는 있다. 다만 이때는 기존 report의 최종값과 새 실행의 최종값만 비교하고, 곡선 차이와 원인 효과는 **잠정 관찰**로 표시한다. “-50이 -5보다 몇 % 좋다”는 결론은 내리지 않는다.

## 왜 첫 변경은 termination 하나인가

현재 참가자 reward baseline은 다음 9개다.

| reward | baseline | 2차 변경 실험 |
| --- | ---: | ---: |
| `track_lin_vel_xy_exp` | +0.5 | 유지 |
| `track_ang_vel_z_exp` | +0.5 | 유지 |
| `feet_air_time` | +0.2 | 유지 |
| `termination_penalty` | -5.0 | **-50.0** |
| `flat_orientation_l2` | -1.5 | 유지 |
| `ang_vel_xy_l2` | -0.05 | 유지 |
| `joint_deviation_hip` | -0.2 | 유지 |
| `joint_deviation_torso` | -0.1 | 유지 |
| `action_rate_l2` | -0.0005 | 유지 |

첫 report의 마지막 fall rate가 100%였고, 백업 `humanoid_rewards.py`는 `termination_penalty` 추천 범위를 `-50~-400`으로 설명하지만 baseline은 `-5`다. 따라서 `-50`은 강한 낙상 억제의 방향성을 시험하는 보수적인 첫 anchor다. 그렇더라도 300회 실패가 `-5` 때문이라고 확정된 것은 아니며, 아래 결과는 학습 초기 반응만 보여준다.

여러 reward를 동시에 바꾸면 fall rate가 개선돼도 어느 값이 원인인지 알 수 없다. 이번에는 PPO 설정, terrain, seed, `num_envs`, iterations, 나머지 reward를 고정한다.

## 이 실험이 답할 질문

1. `termination_penalty`를 -5에서 -50으로 강화하면 같은 300 iterations 안에서 낙상 빈도와 episode length가 달라지는가?
2. 생존 개선이 있다면 명령 추종과 terrain progression을 유지하는가, 아니면 움직이지 않는 소극적 정책으로 바뀌는가?
3. 차이가 학습 초반에만 나타나는가, 마지막 구간까지 유지되는가?
4. KL·learning rate·exploration std·loss에서 학습 불안정 신호가 생기는가?
5. 같은 headless 조건의 seconds/iteration·FPS·GPU 사용량이 재현되는가?

## 고정해야 할 비교 조건

다음 중 하나라도 다르면 reward 효과와 다른 효과가 섞인다.

- 동일 공식 서버 image와 Isaac Sim/Lab 버전
- 동일 H1 task와 참가자 수정 허용 파일 외 코드 hash
- 동일 seed 42
- 동일 `num_envs=4096`, `num_steps_per_env=24`
- 동일 300 iterations
- 동일 PPO·observation·action·terrain 설정
- 동일 camera 없는 headless 실행, 영상 녹화는 학습 뒤 별도 수행
- 동일 시작 방식과 환경변수

실제 적용값은 요청 명령이 아니라 생성된 `env.yaml`, 콘솔 로그와 hash로 재확인한다. terrain seed가 `null`이고 cache가 꺼져 있다면 같은 학습 seed여도 지형 생성 차이가 섞일 수 있으므로 이를 한계로 기록한다.

## 실행 전 기록

각 실행 전에 다음 파일을 별도 experiment 폴더에 만든다.

```text
experiment_id.txt
hypothesis.md
command.txt
train_help.txt
code_sha256.txt
reward_before.py
reward_after.py
reward_diff.patch
git_commit.txt 또는 source_identity.txt
system/nvidia_smi_before.txt
```

`reward_diff.patch`에서 B0는 변경 없음이어야 하고, S1은 `termination_penalty` 한 줄만 달라야 한다. `agent_cfg.py`, `env_cfg.py`, `train.py`를 iteration 조절 목적으로 수정하지 않는다. 실제 help가 지원하는 CLI를 사용한다.

## 실행 중 수집

- 전체 stdout·stderr를 `tee`로 저장
- TensorBoard `events.out.tfevents*`를 포함한 `logs/<run>/` 전체 보존
- 2초 안팎 간격의 GPU utilization·VRAM·power·temperature 시계열
- 시작·종료 epoch와 ISO 시각, exit code
- NaN, simulator error, CUDA OOM, 반복 경고 발생 시점

학습은 camera 없는 headless로 수행하고, play 영상은 학습 처리량 측정이 끝난 뒤 같은 checkpoint로 별도 생성한다.

## 비교 지표와 계산법

### 1. 구간을 나눠 본다

300 iterations를 다음 창으로 요약한다.

| 구간 | iteration | 목적 |
| --- | ---: | --- |
| early | 0~49 | 초기 탐색·붕괴 여부 |
| middle | 50~149 | 학습 방향 형성 |
| late | 150~299 | 짧은 실행의 마지막 상태 |
| last-window | 마지막 50개 | endpoint 노이즈를 줄인 중앙값·평균 |

태그가 매 iteration 기록되지 않았다면 실제 기록 step을 기준으로 같은 비율의 구간을 사용하고 누락률을 표시한다. 마지막 한 점만으로 우열을 정하지 않는다.

### 2. 우선순위 지표

| 축 | 가능한 지표 | 비교 방식 |
| --- | --- | --- |
| 생존 | fall rate, termination count/rate | late·last-window 절대 차이, 낮을수록 우선 |
| 지속 | episode length | last-window 중앙값과 분포, 길수록 유리하되 정지 정책 검사 |
| 진행 | terrain level | 최초 `>0` step, late 중앙값·최댓값 |
| 추종 | linear/yaw tracking term 또는 tracking error | 생존 개선과 함께 유지되는지 확인 |
| 행동 | action std, action-rate term | 지나친 정지·진동·급격한 제어 확인 |
| 최적화 | KL, learning rate, entropy/loss | 급등·급락·collapse 여부 확인 |
| 처리량 | seconds/iteration, FPS, collection/learning time | 같은 실행 모드에서만 비교 |
| 자원 | GPU util, VRAM, power | 병목·환경 차이 확인용, 정책 품질 지표 아님 |

TensorBoard에 실제 존재하는 태그만 사용하며 없는 값을 추정하지 않는다. 태그 목록과 step 수를 먼저 export해 두 실행의 공통 태그 집합을 만든다.

### 3. reward 총합 비교의 함정

`termination_penalty`의 계수를 바꾸면 reward 함수 자체의 척도가 달라진다. 따라서 B0와 S1의 `Train/mean_reward` 절댓값을 그대로 비교해 “높은 쪽이 더 좋은 정책”이라고 판단하면 안 된다.

총 reward는 각 run 내부에서 발산·학습 진행을 보는 보조 곡선으로만 쓴다. run 간 판단은 fall rate, episode length, terrain, tracking, 영상, 개인 evaluator처럼 reward 계수 변경에 직접 종속되지 않는 행동 지표를 우선한다.

### 4. 변화량 표

각 공통 지표에 대해 다음 표를 채운다.

| metric/window | B0 | S1 | 절대 변화 `S1-B0` | 상대 변화 | 판정 |
| --- | ---: | ---: | ---: | ---: | --- |
| fall rate / last 50 |  |  |  |  |  |
| episode length / last 50 median |  |  |  |  |  |
| terrain level / last 50 median |  |  |  |  |  |
| tracking / last 50 median |  |  |  |  |  |
| action std / last 50 median |  |  |  |  |  |
| steady sec/iteration median |  |  |  |  |  |

baseline이 0이거나 부호가 있는 reward term에는 상대 변화율을 쓰지 않는다. 단일 seed 차이는 통계적 유의성으로 표현하지 않고 `seed 42 paired observation`으로 기록한다.

## 영상에서 반드시 볼 실패 형태

- 덜 넘어지지만 제자리에서 거의 움직이지 않음
- 명령과 반대 방향 또는 회전만 반복
- 한 발 들기·hopping·foot dragging
- 상체가 지나치게 굳거나 큰 진동 발생
- 평지에서는 버티지만 terrain 진입 직후 붕괴

낙상률만 좋아지고 추종·진행이 무너지면 성공으로 판정하지 않는다.

## 실행 종료 후 export

각 run을 아래처럼 분리한다.

```text
H1-B0-RECAPTURE/
├─ diagnostics/
├─ logs/<run>/
├─ exported/
└─ manifest_sha256.txt

H1-S1-TERM50/
├─ diagnostics/
├─ logs/<run>/
├─ exported/
└─ manifest_sha256.txt
```

`logs/<run>/`에는 event와 checkpoint가 포함돼야 한다. 실행 직후 원본 폴더 구조를 보존해 복사하고, 다음 학습 전 별도 위치와 로컬 다운로드를 확인한다. 모든 상대경로·bytes·SHA-256을 manifest에 기록한다. credential·token·개인정보는 외부 업로드 전에 검사한다.

## 판정과 다음 단계

| 결과 | 해석 | 다음 행동 |
| --- | --- | --- |
| fall↓, episode↑, tracking·terrain 유지/개선 | 안정성 방향이 유망 | 같은 설정을 더 길게 학습한 confirmation 후보 |
| fall↓, episode↑, tracking↓ 또는 정지 | penalty가 너무 강하거나 학습 초기 소극성 | `-20` 같은 중간 anchor를 별도 동일조건 시험 |
| 차이 거의 없음 | 300회 학습량 부족, terrain 변동 또는 영향 미약 | 같은 reward의 장기 baseline을 먼저 확보 |
| fall·진동·KL 모두 악화 | S1 비유망 | -50 고정 조합 확장 중지, 원인 로그 검토 |
| 두 run의 처리량·설정이 다름 | 비교 오염 | reward 결론 보류, 환경 차이부터 해결 |

2차 실험의 결과가 좋아도 곧바로 Optuna에 넣지 않는다. evaluator가 고정되지 않았고 단일 seed·300회인 동안은 designed anchor 관찰이다. 다음 단계는 같은 iterations에서 `termination_penalty` anchor를 좁게 비교하고, 상위 설정만 장시간 confirmation으로 올리는 것이다.

## 이후 파라미터 지도

다음 값들은 한 번에 하나씩 비교하기 위한 초기 anchor이며 최적값이 아니다.

| 단계 | reward | anchor 후보 | 주로 볼 trade-off |
| --- | --- | --- | --- |
| Stability 1 | `termination_penalty` | -5, -20, -50, -100 | 낙상 억제 vs 소극적 행동 |
| Stability 2 | `flat_orientation_l2` | -0.75, -1.5, -2.5 | 몸통 안정 vs 기울임·민첩성 |
| Stability 3 | `ang_vel_xy_l2` | -0.03, -0.05, -0.10 | 흔들림 억제 vs 험지 적응 |
| Tracking | `track_lin_vel_xy_exp` | 0.5, 1.0, 1.5 | 이동 추종 vs 과속·낙상 |
| Turning | `track_ang_vel_z_exp` | 0.5, 1.0, 1.5 | 선회 추종 vs 회전 과민 |
| Gait | `feet_air_time` | 0.10, 0.20, 0.25, 최대 0.30 | 장애물 발 들기 vs hopping |
| Smoothness | `action_rate_l2` | -0.00025, -0.0005, -0.001 | 진동 억제 vs 반응 둔화 |

`feet_air_time=0.75`는 백업 코드가 reward hacking 체험값으로 제시한 고위험 설정이므로 성능 탐색 후보에 넣지 않는다. Stability에서 생존과 추종의 안전 영역을 먼저 찾은 뒤 Tracking/Gait를 별도 단계로 연다. 조합 실험은 단변수 결과가 쌓인 후 2~3개 reward만 대상으로 한다.

## 이 계획의 한계

- 첫 실행의 전체 event가 없어서 과거 곡선은 새 분석으로 복원할 수 없다.
- 단일 seed 300회 결과는 장기 성능이나 재현성을 보장하지 않는다.
- terrain 생성 비결정성이 reward 차이와 섞일 수 있다.
- 공식 비공개 평가 점수는 내부 metric이나 training reward로 대체할 수 없다.
- 실제 서버 help·폴더·허용 규칙이 백업과 다르면 현재 공식 안내를 우선한다.

상세 export 항목은 `data/processed/ai_library/11_SERVER_OPERATIONS.md`, 전체 Optuna 단계는 `data/processed/planning/04_OPTUNA_REWARD_SEARCH_DESIGN.md`를 따른다.
