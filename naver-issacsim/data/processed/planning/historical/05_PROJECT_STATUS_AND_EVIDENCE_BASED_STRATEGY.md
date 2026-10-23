---
id: planning-project-status-evidence-strategy
source_type: verified_status_synthesis
category: project_status_and_execution_strategy
trust_level: evidence_bounded
reviewed_at: "2026-08-24"
source: "git history: data/processed/incoming/other/inbox/NCRC_2026_현재까지_진행상황_전략_기술환경_통합정리.md at 996e7ca"
---

# NCRC 2026 프로젝트 현황과 증거 기반 실행 전략

> **현재 상태: historical / superseded (2026-08-24 snapshot).** 이 문서는 당시 상태와 실행 전략을 보존한 기록이며 현재 운영 기준으로 사용하지 않는다. 이후 `h1-submit-2 / TERM-50`, `g2-submit-3 / LINTRACK-150-LINZ-2`, `h1-submit-4 / AIRTIME-025`의 실제 제출·공식 평가와 다수의 후속 Run이 완료됐다. 현재 상태와 다음 행동은 `PROJECT_CONTEXT.md`, `research/EXPERIMENTS.md`, AI library `00_START_HERE_CONTEXT_AND_MAP.md`를 우선하며, 이후 `ORIENT-100` OFFICIAL fresh 3K 학습은 완료되고 2026-10-07 `model_2850` PERSONAL 행동 평가는 HOLD로 판정됐다. 현재 다음 판단은 registry·AI library `00`/`14`에서 동일 조건 TERM-50 대조 자료 확인이 우선이며, `ACTRATE-001`은 별도 PLANNED 상태다.

## 기술 요약

현재까지 **규정·OT·서버 백업 코드 분석, 저장소 분리, 개인 NVIDIA 서버 작업공간 설계, evaluator와 Optuna 탐색 설계**가 문서화됐고, 2026-08-24 H1 baseline 300회 실행의 `model_best.pt`, `env.yaml`, policy, ONNX, report, MP4도 원본 저장소에 보존됐다. 다만 전체 콘솔·TensorBoard·GPU 시계열은 없고 개인 evaluator와 Optuna trial도 아직 없다. 따라서 현재 단계는 **첫 파이프라인 기준선을 얻었지만 비교 가능한 최적화 실험 전**이다.

다음 실행의 우선순위는 reward를 바꾸기 전에 동일 H1 baseline의 전체 로그를 보강하고, 더 긴 동일-reward 학습에서 terrain·fall·episode-length가 언제 개선되는지 확인하는 것이다. 그와 병행해 보존된 `policy.pt`를 개인 NVIDIA evaluator에서 로드한다. Optuna는 비교 가능한 evaluator 결과가 쌓인 뒤에만 시작한다.

이 문서는 다운로드 폴더의 통합정리 원문을 그대로 보존한 요약본이 아니다. 저장소의 규정·코드·현재 파일 상태로 근거가 확인되는 내용만 남긴 **실행 기준 문서**다.

## 현재 확인된 사실

### 규정과 제출 조건은 명확하다

| 확인 항목 | 확인된 내용 | 근거 |
| --- | --- | --- |
| 제출 정책 학습 장소 | 운영진 제공 서버에서만 수행 | `../ai_library/12_2026_UNIFIED_REGULATIONS.md` |
| 공식 서버 시간 | 팀 합산 총 100시간, 서버가 켜진 작업 시간이 포함됨 | 같은 문서 |
| 참가자 수정 대상 | H1 `humanoid_rewards.py`, Go2 `quadruped_rewards.py` | 같은 문서 및 백업 README |
| 로봇별 배점 | 시뮬레이션 성능 70, reward 의도와 `env.yaml` 일치 20, 기술 리포트 10 | 같은 문서 |
| 개인 환경의 역할 | 코드·문서 분석과 공식 서버 정책의 검증에 사용하며, 개인 학습 정책은 제출하지 않음 | 같은 문서 |
| 제출 관련 핵심 파일 | `policy.pt`, `env.yaml`, 기술 개선 설명 | 같은 문서 |

규정·마감·제재·허용 범위는 분석본보다 최신 공식 공지와 단계별 규정을 우선한다.

### H1 학습 코드에서 확인되는 실행 계약

| 항목 | 코드·README에서 확인된 값 또는 동작 | 해석 |
| --- | --- | --- |
| task | `Humanoid-v0` | 공식 서버에서 help와 등록 여부를 다시 확인한다. |
| README 실행 예 | `--num_envs 4096 --max_iterations 10000 --headless` | 기준선 진단은 같은 형태에서 iteration만 짧게 제한한다. |
| PPO rollout | `num_steps_per_env = 24` | 실제 실행 결과의 `env.yaml`·로그로 재확인한다. |
| 설정 기본값 | `max_iterations = 5000` | 진단을 위해 설정 파일을 수정하지 않고 CLI override를 사용한다. |
| 학습 후 선별 | `_finalize.py`가 로그의 `Train/mean_reward` 계열 값을 사용해 best checkpoint를 고름 | 이것은 대회 시나리오 성능 최고 정책이라는 뜻이 아니다. |
| 학습 산출물 | `model_best.pt`, `env.yaml`, 조건부 `report.html` | `report.html` 생성은 실패할 수 있으므로 존재를 확인한다. |
| 매치 정책 export | `play.py` 실행 후 `policy.pt`가 생성됨 | 학습 진단만 수행하면 `policy.pt`가 없어도 이상이 아니다. |
| 자동 백업 제어 | `NO_AUTO_SUBMIT=1`이면 `_finalize.py`의 외부 자동 백업을 건너뜀 | 제출 자체가 아니라 코드에 포함된 편의 백업 기능의 제어다. |

근거 파일은 다음과 같다.

- `../server_backup/code/training/humanoid/train.py.md`
- `../server_backup/code/training/humanoid/README.md.md`
- `../server_backup/code/training/humanoid/h1_task/agent_cfg.py.md`
- `../server_backup/code/training/humanoid/h1_task/_finalize.py.md`

### 저장소와 설계 자산은 준비됐지만 실행 시스템은 아직 아니다

현재 세 저장소의 역할은 다음처럼 분리돼 있다.

| 저장소 | 확인된 역할 | 현재 확인 가능한 수준 |
| --- | --- | --- |
| `SE3C/naver-issacsim-originals` | 원본·영상·대용량 자료 아카이브 | 원본 보존과 LFS 분리 |
| `SE3C/naver-issacsim` | 분석·기획·코드 참조·AI 핵심팩 | 규정과 백업 코드 분석, 실행 설계 문서 존재 |
| `SE3C/naver-issacsim-nvidia` | NVIDIA 서버 작업공간 bootstrap | 저장소 clone·갱신·선택적 LFS 수신 스크립트 존재 |

`naver-issacsim-nvidia`에는 아직 Policy Loader, Scenario Runner, Metrics Collector, Batch Evaluator 구현이 없다. 그러므로 개인 서버 evaluator는 **설계 완료, 구현 미완료** 상태다. 관련 설계는 아래 문서에 있다.

- [정책·본선 전략 구현 청사진](./01_SOLUTION_BLUEPRINT.md)
- [개인 NVIDIA 서버 검증환경 설계안](./02_PRIVATE_SERVER_VALIDATION_DESIGN.md)
- [개인 NVIDIA 서버 운영안](./03_NVIDIA_SERVER_OPERATIONS.md)
- [Optuna reward 탐색 설계](../04_OPTUNA_REWARD_SEARCH_DESIGN.md)

## 현재 상태 판정

| 작업 | 상태 | 판정 근거 |
| --- | --- | --- |
| 공식 규정 통합 | 완료 | AI 핵심팩의 통합 규정집 존재 |
| OT 전사·통합 분석 정리 | 완료 | `data/processed/incoming/ot/` 자료 존재 |
| 공식 서버 백업 코드 정적 분석 | 완료 | `data/processed/server_backup/` 코드·보고서 존재 |
| 분석/원본/NVIDIA 저장소 분리 | 완료 | 세 저장소와 bootstrap 스크립트 존재 |
| H1 공식 서버 기준선 진단 설계 | 완료 | `06_H1_OFFICIAL_SERVER_BASELINE_DIAGNOSTIC.md` |
| H1 기준선 실제 실행 | 부분 완료 | 300회 산출물은 원본 저장소에 있으나 전체 콘솔·TensorBoard·GPU 로그가 없음 |
| Go2 기준선 실제 실행 | 미확인·미완료 | 학습 로그와 산출물이 저장소에 없음 |
| 개인 evaluator 구현 | 미완료 | 구현 명세만 있고 실행 모듈이 없음 |
| evaluator 지표 검증 | 미완료 | policy별 multi-seed 결과가 없음 |
| reward 단변수 실험 | 미완료 | 비교 가능한 experiment record가 없음 |
| Optuna study 실행 | 미완료 | study DB·trial snapshot·결과가 없음 |

“미완료”는 실패를 뜻하지 않는다. 현재 저장소에서 완료를 증명할 산출물이 없다는 의미다.

## 확인되지 않아 제거한 주장

원문에는 과거 대화나 다른 PC 경로에서 유래한 것으로 보이는 구체적 환경 정보가 포함돼 있었다. 다음 내용은 현재 작업공간에서 재검증할 수 없으므로 실행 기준에서 제외했다.

- RTX 3060 12GB가 현재 실제 사용 GPU라는 주장
- `C:\isaacsim`의 Isaac Sim 6.0.1 RC 설치 상태
- 별도 백업 경로의 Isaac Lab 2.3.2 설치·실행 상태
- Isaac Lab 3 설치 완료 여부와 특정 beta 버전 선택
- 로컬 학습 명령이 실제로 어디까지 성공했는지에 대한 과거 진술
- H1 또는 Go2가 먼저여야 한다는 확정적 우선순위
- 첫 실행의 4분을 근거로 한 장기 학습시간 선형 예측
- 예시 leaderboard의 reward·fall rate·proxy 수치를 실제 실험 결과처럼 읽을 수 있는 표

이 항목들은 새 로그·명령 출력·버전 파일로 재확인되면 별도 환경 현황 문서에 추가한다. 현재는 삭제가 가장 안전하다.

## 다음 실행은 baseline 증거를 완성하는 데서 시작한다

### 1단계: H1 공식 서버 기준선 보강

[H1 공식 서버 기준선 진단 가이드](../06_H1_OFFICIAL_SERVER_BASELINE_DIAGNOSTIC.md)에 따라 변경되지 않은 H1 reward로 실행하고, 첫 300회 묶음에서 빠진 진단 자료를 보강한다. 첫 결과의 상세 검토는 [H1 300-iteration 기준선 분석](../../experiments/h1/2026-08-24_OFFICIAL_SERVER_300ITER_BASELINE.md)에 있다.

반드시 확보할 것은 다음과 같다.

- 관련 코드의 Git diff와 SHA-256
- `train.py --help` 결과
- GPU·드라이버·VRAM 정보와 학습 중 GPU 시계열
- 전체 실행시간과 안정 구간 iteration 시간
- `num_envs`, `num_steps_per_env`, seed, PPO 설정
- 학습 로그, `model_best.pt`, `env.yaml`, 가능한 경우 `report.html`

이 단계의 목적은 300회 정책의 품질을 높게 평가하는 것이 아니라 **공식 서버의 실제 환경·처리량과 동일 reward의 학습 진행을 분리 측정하는 것**이다.

### 2단계: 측정값으로 시간 예산을 다시 계산

300 iterations의 전체시간을 그대로 장기 학습에 선형 외삽하지 않는다. Isaac Sim 초기화·finalize 시간과 안정 구간 iteration 시간을 분리한다.

```text
예상 장기 실행시간
≈ 초기화 시간 + 목표 iterations × 안정 구간 sec/iteration + finalize 시간
```

이 계산이 끝나야 100시간 중 baseline, 단변수 screening, 상위 후보 장기 학습에 각각 몇 회를 배정할지 정할 수 있다.

### 3단계: 개인 evaluator의 최소 기능 구현

보존된 첫 `policy.pt`를 사용해 다음 최소 기능만 우선 구현한다.

1. H1/Go2 정책 로딩과 observation 형상 검증
2. 전진·측면·yaw·정지 명령 시나리오
3. 생존 시간, 낙상 여부, 속도 추종 오차 수집
4. seed 반복과 결과 CSV/JSON 저장
5. 정책 A/B 비교

험지·경사·push recovery는 기본 추론과 평지 지표가 안정된 뒤 추가한다. 공식 평가 환경과 정확히 같다는 주장은 하지 않고, 같은 evaluator 안에서 정책의 상대 순위를 비교하는 용도로 쓴다.

### 4단계: 단변수 reward screening

처음에는 한 번에 한 reward 계수만 바꾼다. 각 실험은 baseline과 같은 학습량·평가 버전으로 비교한다.

H1의 첫 paired 비교는 [H1 2차 공식 서버 reward 비교 실험 계획](./07_H1_SECOND_RUN_PARAMETER_COMPARISON_PLAN.md)을 따른다. baseline 300회를 전체 로그와 함께 다시 수집하고, 다른 조건을 고정한 채 `termination_penalty -5 → -50` 한 항목만 변경한다. 새 실행을 하나만 확보한 경우에는 기존 report endpoint와의 잠정 관찰로 제한한다.

```text
baseline
  → reward 한 개 변경
  → 공식 서버 학습
  → 산출물·로그 보존
  → 같은 evaluator와 seed set으로 평가
  → 채택·기각과 이유 기록
```

학습 mean reward만으로 정책을 고르지 않는다. `_finalize.py`의 best checkpoint 선택 기준과 최종 정책 비교 기준은 분리한다.

### 5단계: Optuna는 비교 가능한 데이터가 생긴 뒤 사용

Optuna는 공식 서버에 설치하거나 서버를 직접 제어하지 않는다. 개인 작업공간에서 다음 reward 후보를 제안하고, 공식 서버 학습과 개인 evaluator 결과를 다시 기록하는 Ask-and-Tell 방식으로만 쓴다.

Optuna 시작 조건은 `04_OPTUNA_REWARD_SEARCH_DESIGN.md`의 readiness gate를 따른다. 최소 조건은 다음과 같다.

- evaluator 결과가 반복 실행에서 재현됨
- objective와 scenario 버전이 고정됨
- 동일 robot·학습량·평가 버전의 비교 가능한 trial이 축적됨
- 실패 policy도 누락하지 않고 낮은 점수로 기록할 규칙이 있음
- 공식 서버 남은 시간으로 탐색과 최종 재학습이 모두 가능함

조건이 충족되지 않으면 Optuna보다 수동 단변수 실험이 낫다.

## 결과 기록의 최소 단위

각 실험은 다음 항목을 빠뜨리지 않는다.

```text
experiment_id
robot
parent_experiment
code_commit
reward_file_sha256
changed_reward
old_value
new_value
hypothesis
training_iterations
training_wallclock
seed
headless_camera_viewport_video_mode
log_run_path
policy_sha256
env_yaml_sha256
evaluator_version
scenario_version
metric_summary
observed_behavior
decision
decision_reason
```

예시 숫자는 실제 결과 테이블에 넣지 않는다. 값이 없는 항목은 빈칸이나 `미측정`으로 표시한다.

## 한계와 검증 규칙

- 분석 저장소의 규정집은 통합 분석본이다. 최종 제출 판단에는 최신 공식 원문을 다시 확인한다.
- 백업 코드는 서버에서 받은 시점의 스냅샷이다. 실제 공식 서버 배포본의 commit·help·파일 hash가 다를 수 있다.
- 개인 evaluator의 proxy score는 공식 점수의 추정치가 아니다. 정책 간 상대 비교 도구다.
- `Train/mean_reward`는 reward 정의가 달라지면 정책 간 절대 비교가 왜곡될 수 있다.
- 소요시간과 GPU 처리량은 실제 공식 서버 진단 전에는 숫자로 단정하지 않는다.
- 로컬 Isaac Sim/Lab 호환성은 실제 설치 로그와 공식 호환표를 확보한 별도 작업에서 판단한다.

## 권장 다음 행동

1. 첫 300회 결과 분석에서 확인된 누락 자료 목록을 실험 체크리스트로 사용한다.
2. 공식 서버가 baseline 상태인지 코드 hash와 diff로 확인한다.
3. 동일 reward의 다음 실행에서 전체 콘솔·TensorBoard·GPU 시계열을 수집한다.
4. `07_H1_SECOND_RUN_PARAMETER_COMPARISON_PLAN.md`에 따라 baseline 재수집과 단일 변경을 paired 비교한다.
5. 산출물은 원본 저장소의 실행 ID별 폴더에 보관한다.
6. 안정 구간 처리량을 확인한 뒤에만 장기 학습시간을 계산한다.
7. 현재 보존된 policy로 NVIDIA 저장소의 evaluator 최소 구현을 시작한다.

## 아직 답이 필요한 질문

- 실제 공식 서버의 GPU 상세, 드라이버와 Isaac Sim/Lab 버전을 재검토 가능한 로그로 보존할 수 있는가?
- 배포된 `train.py --help`와 백업 README의 CLI가 일치하는가?
- 공식 서버 baseline의 안정 구간 sec/iteration과 FPS는 얼마인가? 첫 실행은 end-to-end 4분만 확인됐다.
- H1과 Go2 baseline 중 어느 쪽이 상대적으로 더 취약한가?
- 개인 evaluator에서 반복 가능한 최소 시나리오와 seed 수는 얼마인가?
- 개인 proxy 순위가 실제 공식 평가 결과의 순위와 어느 정도 일치하는가?
