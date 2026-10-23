---
title: "NCRC 2026 Optuna 기반 reward 탐색 설계"
status: "설계 확정안 — evaluator 준비 전 trial 시작 금지"
audience: "technical"
reviewed_at: "2026-08-21"
optuna_reference_version: "4.9.0 stable documentation"
authority: "공식 규정·공지 우선. 이 문서는 실험 의사결정 설계이며 공식 점수 예측기가 아니다."
---

# Optuna는 학습기가 아니라 다음 reward 실험을 고르는 엔진으로 쓴다

> **현재 취급: pre-implementation design.** 실제 study/trial 상태와 현재 후보 우선순위는 이 문서에서 추정하지 않는다. 현재 Optuna readiness·objective·evidence 경계는 AI library `15_OPTUNA_REWARD_DECISION_ENGINE.md`를 우선하고, H1 `ORIENT-100`은 2026-10-06 OFFICIAL 3K 완료·2026-10-07 PERSONAL 행동 HOLD이며, 현재 다음 판단은 registry와 AI library `14`의 **동일 조건 대조 자료 우선 확인**이다. 별도 `ACTRATE-001`은 PLANNED 질문으로만 유지한다.

## 기술 요약

**채택 결론은 조건부 찬성이다.** Optuna Ask-and-Tell과 TPE는 공식 서버 밖에서 다음 reward 조합을 추천하고, 공식 서버에서 생성한 정책을 개인 NVIDIA 서버에서 평가한 뒤 결과를 돌려주는 구조에 잘 맞는다. 공식 GPU 서버에는 Optuna를 설치하거나 외부 에이전트를 연결하지 않는다.

도입 순서는 반드시 `공식 baseline → 개인 evaluator 검증 → objective 고정 → Optuna`다. 현재 `_finalize.py`의 `model_best.pt`는 대회 proxy score가 아니라 `Train/mean_reward`가 가장 높은 checkpoint를 고르므로, 이 값을 Optuna objective로 쓰면 reward hacking을 자동화할 위험이 있다.

첫 버전은 **로봇·탐색 단계·학습 iteration 예산·evaluator 버전별로 별도 single-objective study**를 사용한다. 한 study에는 2~4개의 활성 reward만 넣고, `Robust Proxy Score`와 안전성 hard penalty로 순위를 만든다. 비교 가능한 완료 trial이 8개 미만이면 TPE보다 baseline과 수동 1차원 sweep이 낫다.

이 설계는 실제 trial 결과가 없는 사전 설계다. 따라서 탐색 범위와 objective 가중치는 공식 점수가 아니라 코드의 현재 baseline·권장 범위와 개인 evaluator의 상대 비교 목적에 맞춘 초기값이다.

## 첫 H1 실측은 Optuna trial이 아니다

2026-08-24 H1 baseline 300회 실행은 report 기준 end-to-end 4분, 마지막 terrain level 0.00, fall rate 100.0%였다. 실행 파이프라인과 실제 환경 설정은 확인됐지만 정책이 미수렴 상태이고 개인 evaluator 결과도 없으므로 이 실행을 Optuna objective 표본으로 넣지 않는다.

이 실행에서 실질 활성 reward가 참가자 수정 대상 9개와 프레임워크 기본 nonzero 4개를 합친 13개라는 점이 확인됐다. Optuna는 허용된 9개 중 단계별 2~4개만 바꾸되, 결과 해석에는 나머지 기본 reward의 영향도 포함한다. `termination_penalty=-5`가 report 추천 구간 밖인 사실만으로 실패 원인을 단정하지 않고, 동일 reward의 더 긴 baseline으로 학습량 효과를 먼저 분리한다.

저장된 자료는 전체 콘솔·TensorBoard·GPU 시계열이 없어 안정 구간 `sec/iteration`을 확정하지 못한다. 4분/300의 `0.80 s/iteration`은 초기화·finalize까지 포함한 end-to-end 평균일 뿐 screening 시간 모델의 steady-state 값으로 사용하지 않는다.

## 근거상 Optuna의 적용 위치는 명확하다

| 확인된 사실 | 설계상 의미 |
| --- | --- |
| 예선에서 참가자가 수정하는 핵심은 H1·Go2 reward 파일이다. | PPO 자체 하이퍼파라미터가 아니라 reward coefficient만 탐색한다. |
| 공식 제출 정책은 제공 서버에서 학습해야 한다. | Optuna와 evaluator는 개인 환경에 두고, 공식 서버에는 reward 값만 수동 반영한다. |
| H1·Go2 reward는 서로 영향을 주는 연속 계수가 여러 개다. | Grid Search보다 이전 결과를 활용하는 sampler가 적합하다. |
| `_finalize.py`는 `Train/mean_reward` 최고 checkpoint를 선택한다. | 대회 성능과 별도의 multi-seed proxy evaluator가 필요하다. |
| 공식 tracking score의 세부식은 공개되지 않았다. | objective는 공식 점수 예측이 아니라 같은 evaluator 안의 상대 비교값이다. |
| Optuna `Study.ask()`와 `Study.tell()`은 외부에서 trial 수명주기를 제어한다. | 공식 학습과 개인 평가를 Optuna 프로세스에서 분리할 수 있다. |

근거 문서: [통합 규정집](../../ai_library/12_2026_UNIFIED_REGULATIONS.md), [H1 reward 코드](../../server_backup/code/training/humanoid/humanoid_rewards.py.md), [Go2 reward 코드](../../server_backup/code/training/quadruped/quadruped_rewards.py.md), [H1 finalize 코드](../../server_backup/code/training/humanoid/h1_task/_finalize.py.md), [개인 서버 검증환경 설계](02_PRIVATE_SERVER_VALIDATION_DESIGN.md).

## 확정 아키텍처

```text
개인 PC 또는 개인 NVIDIA 서버
  Optuna ask() → trial 번호 + reward 후보 JSON
             ↓ 값만 수동 전달
공식 대회 GPU 서버
  허용 reward 파일 수정 → 공식 train.py → play.py → policy.pt/env.yaml
             ↓ 산출물 다운로드
개인 NVIDIA 서버
  고정 evaluator × 고정 scenarios × 고정 seeds
  → component metrics + Robust Proxy Score
             ↓
개인 PC 또는 개인 NVIDIA 서버
  Optuna tell() → 다음 후보
```

금지선은 명확하다.

- 공식 서버에 Optuna·MCP·외부 agent·추가 optimizer를 설치하지 않는다.
- 개인 서버에서는 공식 정책을 실행·관찰·평가만 하고 gradient update나 RL 학습을 하지 않는다.
- Optuna가 PPO의 `learning_rate`, `gamma`, `lambda`, network 구조를 바꾸게 하지 않는다.
- 백업 코드에 있는 credential·practice key·외부 endpoint를 trial 자료에 넣지 않는다.

세 GitHub 저장소는 2026-08-21 확인 시 모두 private이었다. 대회 중에는 계속 private을 유지한다.

## evaluator 준비 전에는 Optuna를 시작하지 않는다

다음 readiness gate를 모두 통과해야 첫 `ask()`를 실행한다.

1. 공식 `policy.pt`가 개인 서버에서 observation/action shape 오류 없이 로드된다.
2. H1·Go2 baseline을 동일 scenario와 seed로 재실행할 수 있다.
3. Flat tracking, yaw, stop-and-go, fall, push recovery, rough, slope, stairs 중 해당 로봇의 필수 시나리오가 자동 종료된다.
4. 모든 metric이 CSV 또는 JSON으로 저장되고 policy·env·evaluator commit과 연결된다.
5. 같은 baseline을 반복했을 때 score 분산과 실패율을 확인했다.
6. `objective_version`, scenario weight, seed set, normalization 상수를 고정했다.
7. 최소 두 정책의 영상과 metric을 대조해 evaluator가 명백한 실패를 더 낮게 평가하는지 확인했다.

하나라도 실패하면 reward 탐색이 아니라 evaluator 수정 단계다.

## 한 trial의 정의를 고정한다

한 trial은 단순 reward 딕셔너리가 아니라 아래 묶음 전체다.

```yaml
trial_id: h1_stability_v1_0007
robot: h1
study: h1_stability_v1_iter3000

reward:
  termination_penalty: -40.0
  flat_orientation_l2: -1.2
  ang_vel_xy_l2: -0.08

official_training:
  iterations: 3000
  seed: 42
  source_commit: "..."
  reward_file_sha256: "..."
  env_yaml_sha256: "..."
  policy_sha256: "..."

evaluation:
  evaluator_commit: "..."
  objective_version: robust_proxy_v1
  scenario_set: h1_prelim_v1
  seeds: [101, 202, 303]
  metrics_json: "results/h1_stability_v1_0007/metrics.json"
```

다음 중 하나라도 다르면 같은 study에 섞지 않는다.

- 로봇 종류
- 탐색 대상 reward 집합
- 공식 학습 iterations
- evaluator 또는 observation 구현
- scenario 집합·weight·seed 집합
- objective 공식·normalization

특히 1,000회 학습과 5,000회 학습 결과를 같은 objective 표본으로 넣으면 sampler가 reward 효과와 학습량 효과를 구분하지 못한다.

## sampler는 저예산 TPE부터 시작한다

Optuna 4.9.0의 `TPESampler` 기본값은 `n_startup_trials=10`, `multivariate=False`다. `n_startup_trials` 동안은 TPE가 아니라 random sampling을 사용한다. `multivariate=True`는 파라미터 상관관계를 함께 모델링하지만 실험적 API이고, 데이터가 너무 적으면 이점이 제한적이다.

초기 권장 설정은 다음과 같다.

```python
sampler = optuna.samplers.TPESampler(
    seed=20260821,
    n_startup_trials=6,
    multivariate=True,
)

study = optuna.create_study(
    study_name="h1_stability_v1_iter3000",
    direction="maximize",
    sampler=sampler,
    pruner=optuna.pruners.NopPruner(),
    storage="sqlite:///runtime/optuna.db",
    load_if_exists=True,
)
```

운영 원칙:

- baseline은 `enqueue_trial()`로 첫 후보에 반드시 포함한다.
- 이미 완료한 수동 실험은 같은 학습량·evaluator·objective로 재평가할 수 있을 때만 backfill한다.
- startup 6개는 순수 무작위보다 baseline과 안전한 저·중·고 anchor 조합을 우선한다.
- 완료 trial이 8개 미만이면 TPE 추천을 신뢰하지 않고 수동 sweep으로 취급한다.
- CMA-ES는 동일한 3~4개 연속 파라미터의 좁은 범위에서 충분한 완료 trial이 쌓인 후에만 검토한다. Optuna의 CMA-ES는 별도 `cmaes` 패키지가 필요하고 categorical distribution을 지원하지 않는다.

공식 근거: [Study Ask-and-Tell](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html), [TPESampler](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html), [CmaEsSampler](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.CmaEsSampler.html).

## 첫 objective는 단일 Robust Proxy Score로 고정한다

공식 평가 내부식이 없으므로 실제 공식 점수를 복제하려 하지 않는다. 각 scenario와 seed에서 동일하게 계산되는 상대 비교 지표를 사용한다.

### 1. scenario 단위

```text
normalized_tracking_error
= velocity RMSE / scenario command range

tracking_score
= exp(-k × normalized_tracking_error)

scenario_score
= survival_rate × tracking_score
```

`k`와 command range는 baseline 분포를 보고 정하되 study 시작 전에 고정한다.

### 2. policy 단위

초기안:

```text
weighted_mean
= 공식 공개 시나리오 비중을 반영한 scenario 평균

worst_scenario
= scenario 평균 중 최솟값

seed_instability
= scenario별 seed score 표준편차의 가중 평균

Robust Proxy Score
= 0.65 × weighted_mean
 + 0.20 × worst_scenario
 + 0.15 × recovery_success_rate
 - 0.10 × fall_rate
 - 0.05 × seed_instability
```

계수는 초기 설계값이며 공식 배점이 아니다. 모든 component는 0~1 범위로 정규화한다. baseline으로 saturation과 방향성을 확인한 뒤 `robust_proxy_v1`로 동결한다.

### 3. hard penalty

다음 조건은 높은 평균 점수로 상쇄하지 못하게 한다.

```text
policy load 실패 또는 observation mismatch → trial FAIL
평가 산출물 누락                          → trial FAIL
정상 평가됐지만 모든 seed에서 즉시 붕괴    → COMPLETE, objective를 음수로 기록
fall_rate가 사전 한도 초과                 → COMPLETE, 큰 음수 penalty
필수 scenario 하나라도 미실행              → COMPLETE 금지
```

나쁜 정책을 정상 평가했다면 `FAIL`로 버리지 않는다. Optuna의 built-in sampler는 실패 trial을 다음 sampling에서 무시하므로, 평가 가능한 실패 정책은 낮은 완료 점수로 남겨 나쁜 영역을 학습하게 한다.

초기 버전은 metric component를 별도 `trial_ledger.jsonl`에 기록하고 Optuna에는 단일 objective만 넣는다. evaluator와 Optuna가 한 프로세스로 통합된 후에는 `constraints_func`를 검토할 수 있다. 공식 문서상 constraint는 성공적으로 끝난 trial 뒤에 평가되며, 양수 값이 제약 위반을 뜻한다.

## H1은 안정성부터 3차원으로 시작한다

현재 active baseline과 코드 주석 범위를 바탕으로 한 초기 search space다. 음수 penalty는 절댓값을 양수 log scale로 추천받은 뒤 다시 음수로 적용한다.

### H1 Stability v1

| Optuna 파라미터 | 실제 reward | 범위 | scale | baseline |
| --- | --- | ---: | --- | ---: |
| `termination_abs` | `-termination_abs` | 5~100 | log | 5 |
| `flat_orientation_abs` | `-flat_orientation_abs` | 0.3~3.0 | log | 1.5 |
| `ang_vel_xy_abs` | `-ang_vel_xy_abs` | 0.02~0.30 | log | 0.05 |

이 단계에서는 `action_rate_l2`, tracking, joint deviation을 baseline에 고정한다. 목적은 낙상 감소가 tracking·지형 진입을 얼마나 희생하는지 확인하는 것이다.

### H1 Tracking/Gait v1

Stability v1의 상위 안전 영역을 고정한 후 별도 study로 연다.

| 파라미터 | 범위 | baseline |
| --- | ---: | ---: |
| `track_lin_vel_xy_exp` | 0.5~1.5 | 0.5 |
| `track_ang_vel_z_exp` | 0.5~1.5 | 0.5 |
| `feet_air_time` | 0.10~0.30 | 0.20 |

코드 주석의 허용 범위는 더 넓지만 초기 탐색은 보수적으로 둔다. `feet_air_time=0.75`에서 hopping을 유도하는 설명이 있으므로 고위험 영역을 startup random에 노출하지 않는다.

### H1 Fine v1

앞 두 단계 결과에서 명확한 실패 원인이 있을 때만 연다.

- `joint_deviation_hip`: 절댓값 0.1~0.5
- `joint_deviation_torso`: 절댓값 0.05~0.3
- `action_rate_l2`: 절댓값 0.0001~0.005, log scale

## Go2는 active key만 좁게 탐색한다

Go2의 첫 study는 현재 활성화된 key만 사용한다.

### Go2 Locomotion v1

| Optuna 파라미터 | 실제 reward | 범위 | scale | baseline |
| --- | --- | ---: | --- | ---: |
| `track_lin_vel_xy_exp` | 그대로 | 0.75~1.50 | linear | 1.0 |
| `feet_air_time` | 그대로 | 0.01~0.15 | log | 0.01 |
| `lin_vel_z_abs` | `-lin_vel_z_abs` | 1.5~5.0 | log | 3.0 |

두 번째 단계는 첫 결과에서 흔들림·동작 급변이 병목일 때만 연다.

- `ang_vel_xy_l2`: 절댓값 0.02~0.15
- `action_rate_l2`: 절댓값 0.005~0.02

Go2 파일에 주석 처리된 `track_ang_vel_z_exp`, `flat_orientation_l2`, `termination_penalty`는 실제 환경에서 적용된다는 로그·`env.yaml` 근거가 확인되기 전에는 Optuna 파라미터로 넣지 않는다. 존재하지 않는 이름은 경고 후 skip될 수 있어, sampler가 효과 없는 변수를 학습하는 문제가 생길 수 있다.

## 100시간 안에서는 trial 수를 먼저 계산한다

300-iteration 첫 실행은 end-to-end 4분만 확인됐고 안정 구간 로그가 빠졌다. 다음 기준선에서 `sec_per_iteration`, 초기화 시간, finalize 시간을 분리 측정한 뒤 예산을 계산한다.

```text
screening_trial_hours
= (startup_seconds
   + screening_iterations × steady_sec_per_iteration
   + finalize_seconds) / 3600

search_budget_hours
= min(남은 공식 서버 시간 × 0.30, 30시간)

available_trials
= floor(search_budget_hours / screening_trial_hours)
```

의사결정 규칙:

| 가능한 비교 trial | 선택 |
| ---: | --- |
| 0~4 | baseline + 수동 1차원 sweep만 수행 |
| 5~7 | designed anchors를 비교하고 TPE는 시작하지 않음 |
| 8~12 | `n_startup_trials=6` TPE 한 단계만 수행 |
| 13 이상 | 한 로봇의 2단계 study 또는 상위 영역 재검증 검토 |

탐색 budget은 고정 상한이 아니라 안전장치다. H1과 Go2 baseline 점수를 먼저 비교하고, 공식 점수 격차가 큰 로봇에 우선 배정한다. 두 로봇에 동일한 trial 수를 기계적으로 배분하지 않는다.

screening과 final training은 같은 study에 섞지 않는다. screening 상위 2~3개만 공식 장시간 학습하고, 장시간 결과는 별도 confirmation study 또는 최종 후보 표에서 비교한다.

## pruning은 초기 버전에서 끈다

`MedianPruner`는 training mean reward의 초반 값이 최종 terrain·recovery 성능을 대표한다는 보장이 없어서 사용하지 않는다. Optuna의 pruning은 `trial.report()`와 `should_prune()`에 들어오는 intermediate objective를 기준으로 하는데, 현재 공식 서버의 intermediate 값은 우리가 원하는 개인 evaluator score가 아니다.

초기 정책:

- `NopPruner` 사용
- NaN, 학습 프로세스 crash, policy export 실패만 실패 처리
- evaluator가 정상 실행된 붕괴 정책은 낮은 완료 점수로 기록
- 향후 동일 checkpoint를 중간마다 개인 evaluator로 평가할 수 있을 때만 보수적 threshold pruning 검토

공식 근거: [Optuna pruners](https://optuna.readthedocs.io/en/stable/reference/pruners.html).

## 기록과 storage는 단순하게 유지한다

단일 운영자가 순차적으로 ask/tell하는 초기 버전은 로컬 SQLite로 충분하다. DB는 binary runtime 상태이므로 Git에 커밋하지 않는다.

```text
runtime/optuna.db            # gitignored
studies/trial_ledger.jsonl   # trial·policy·metric 연결
studies/trials.csv           # 사람이 읽는 snapshot
artifacts/<trial_id>/        # policy/env/metrics/video 또는 그 경로
```

Optuna DB에는 작은 파라미터와 objective만 두고, `policy.pt`, 영상, 전체 metric은 파일 artifact로 보관한다. Optuna 공식 문서도 큰 trial 산출물은 artifact store를 사용하도록 안내한다. 병렬 실행이 필요해지면 SQLite를 공유하지 않고 `JournalStorage`나 client/server RDB를 검토한다.

공식 근거: [Optuna artifact tutorial](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/012_artifact_tutorial.html), [SQLite 병렬 사용 주의](https://optuna.readthedocs.io/en/stable/faq.html#how-can-i-solve-the-error-that-occurs-when-performing-parallel-optimization-with-sqlite3).

## 견고성 검증과 중단 조건

Optuna가 유용하다는 결론은 아래 검증을 통과할 때만 유지한다.

1. **순위 안정성:** seed 3개와 seed 10개 평가에서 상위 후보 순서가 크게 뒤집히지 않는다.
2. **공식 피드백 일치:** 최소 5개 정책이 쌓이면 로컬 proxy 순위와 공식 라운드 결과의 순위 상관을 확인한다.
3. **objective 민감도:** 가중치를 합리적 범위로 바꿔도 상위 후보가 완전히 바뀌지 않는다.
4. **재현성:** 같은 policy hash와 evaluator commit에서 같은 seed 결과가 허용 오차 내에 들어온다.
5. **reward hacking 검사:** 상위 trial 영상에서 hopping, foot dragging, stand-and-spin, terrain 회피가 없는지 사람이 확인한다.

다음 상황이면 Optuna를 중단하고 수동 실험으로 돌아간다.

- evaluator 버그나 observation mismatch가 반복됨
- 같은 정책의 분산이 reward 후보 간 차이보다 큼
- 로컬 proxy 순위와 공식 결과 순위가 지속적으로 반대임
- 남은 공식 서버 시간으로 8개 이상의 비교 가능한 trial을 만들 수 없음

## 권장 실행 순서

1. 첫 H1 300-iteration 산출물에 누락된 콘솔·TensorBoard·GPU 로그를 보강해 공식 서버 처리량을 확정한다.
2. 개인 NVIDIA 서버에 policy loader와 Flat tracking MVP를 만든다.
3. fall/push/terrain suite와 multi-seed batch evaluator를 완성한다.
4. baseline 정책으로 metric·영상·반복성 gate를 통과한다.
5. `robust_proxy_v1`의 normalization과 weights를 고정한다.
6. H1·Go2 중 baseline 격차가 큰 로봇 하나를 선택한다.
7. 가능한 trial 수를 계산한다. 8개 미만이면 수동 sweep을 한다.
8. baseline과 designed anchors를 넣고 한 단계 TPE를 실행한다.
9. 상위 2~3개를 더 많은 seed와 영상으로 재검증한다.
10. 최종 후보만 공식 서버에서 장시간 학습한다.

## 아직 답이 필요한 질문

- 공식 서버에서 robot별 실제 screening iteration 시간은 얼마인가?
- 공식 서버의 학습 seed를 CLI로 고정할 수 있는가?
- 개인 서버에서 공식 policy observation·action 순서를 완전히 재현했는가?
- 공개된 scenario weight가 최신 규정과 동일한가?
- 로컬 proxy와 첫 공식 라운드 점수의 순위 상관은 어느 정도인가?
- H1과 Go2 중 현재 baseline의 공식 점수 손실이 더 큰 쪽은 어디인가?

이 질문에 답하기 전에는 search space를 더 넓히거나 CMA-ES로 전환하지 않는다.
