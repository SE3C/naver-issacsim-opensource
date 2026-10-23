---
id: planning-h1-official-server-baseline-diagnostic
source_type: verified_execution_guide
category: official_server_diagnostic
trust_level: code_and_readme_crosschecked_server_verification_required
reviewed_at: "2026-08-21"
source: "C:/Users/<USER>/Downloads/H1_공식서버_기준선_진단_실행가이드.md"
status: historical_procedure
current_operations: "../ai_library/11_SERVER_OPERATIONS.md and ../ai_library/19_ISSACSIMZ_EXTERNAL_EVIDENCE_CLI.md"
---

> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/planning/historical/06_H1_OFFICIAL_SERVER_BASELINE_DIAGNOSTIC.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.


# H1 공식 서버 기준선 진단 가이드

> **역사적 절차:** 2026-08의 초기 baseline 진단용 기록이다. 현재 official 운영 source·sidecar·종료 원칙을 대신하지 않는다. 특히 이 문서의 과거 서버 종료 표현은 실행 지시가 아니며, 서버 종료는 현재 규칙대로 사용자가 명시적으로 요청한 경우에만 한다. 현재 운영은 `../ai_library/11_SERVER_OPERATIONS.md`, `../ai_library/19_ISSACSIMZ_EXTERNAL_EVIDENCE_CLI.md`와 workspace `AGENTS.md`를 따른다.

## 이 실행이 답해야 하는 질문

이 진단은 좋은 정책을 만드는 실험이 아니다. 변경하지 않은 H1 baseline을 짧게 실행해 다음 값을 확보하는 작업이다.

- 공식 서버의 GPU·드라이버·VRAM
- 실제 학습 CLI와 환경 설정
- 안정 구간 iteration 시간과 FPS
- 초기화와 finalize를 포함한 전체 실행시간
- GPU 사용률·VRAM·전력 시계열
- 개인 NVIDIA 서버와 비교할 재현 조건

300 iterations는 고정된 대회 권장값이 아니라 **한 번의 짧은 기준선 측정을 위한 작업값**이다. 예상 소요시간은 사전에 단정하지 않으며, 서버 대시보드의 실제 사용시간도 함께 기록한다.

### 2026-08-24 첫 실행 결과

첫 H1 baseline 300회 실행은 완료돼 `model_best.pt`, `env.yaml`, report, policy, ONNX, play 영상이 보존됐다. report 기준 end-to-end 시간은 4분이며 마지막 terrain level은 0.00, fall rate는 100.0%였다. 다만 이 실행에는 이 가이드가 요구한 전체 콘솔 로그, TensorBoard event, GPU 시계열, 코드 hash가 남지 않았다.

따라서 첫 실행은 **파이프라인·환경 산출물 기준선은 확보했지만 처리량 진단은 미완료**로 판정한다. 상세 검토는 H1 공식 서버 300-iteration 기준선 분석〔원본 참조: `../../experiments/h1/2026-08-24_OFFICIAL_SERVER_300ITER_BASELINE.md` / 공개 사본 미포함〕을 따른다. 다음 실행에서는 reward를 바꾸기 전에 누락 자료를 우선 보강한다.

## 실행 전 조건

- 새로 초기화됐거나 H1 관련 코드가 수정되지 않은 공식 서버에서 수행한다.
- `humanoid_rewards.py`, `agent_cfg.py`, `env_cfg.py`, `train.py`를 수정하지 않는다.
- `agent_cfg.py`의 `max_iterations` 값을 바꾸지 않는다.
- `--max_iterations`가 실제 서버 help에 있을 때만 CLI로 300을 지정한다.
- 기존 `exported/` 결과가 있으면 먼저 다운로드하고, 이번 진단을 계속하지 않는다.
- 이번 실행에서는 `play.py`를 돌리지 않는다.
- 진단 파일을 다운로드한다. 서버 종료 여부는 사용자가 명시적으로 결정한다.

백업 코드에서 확인된 실행 예는 다음과 같다.

```text
task                  Humanoid-v0
num_envs              4096
num_steps_per_env     24
CLI iteration option  --max_iterations
launcher              /workspace/IsaacLab/isaaclab.sh
```

실제 공식 서버 배포본은 다를 수 있으므로 아래 절차에서 다시 확인한다.

## 1. 작업 위치와 진단 폴더 설정

아래 블록은 같은 터미널에서 순서대로 실행한다.

```bash
set -uo pipefail

TRAIN_DIR=/workspace/training/humanoid
RUN_ID="h1_diag_$(date +%Y%m%d_%H%M%S)"
DIAG_DIR="/workspace/h1_diagnostics/$RUN_ID"

mkdir -p "$DIAG_DIR"
cd "$TRAIN_DIR"

pwd | tee "$DIAG_DIR/pwd.txt"
date -Is | tee "$DIAG_DIR/session_start.txt"
```

경로가 없거나 `train.py`가 보이지 않으면 추정 경로로 진행하지 말고 실제 서버 구조를 먼저 확인한다.

## 2. baseline 무변경 상태 확인

SHA-256은 실행한 파일의 신원을 기록하지만, 그 자체로 공식 baseline과 같음을 증명하지는 않는다. Git 저장소라면 관련 파일의 tracked diff가 없어야 한다.

```bash
cd "$TRAIN_DIR"

sha256sum \
  train.py \
  humanoid_rewards.py \
  h1_task/agent_cfg.py \
  h1_task/env_cfg.py \
  | tee "$DIAG_DIR/code_sha256.txt"

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git rev-parse HEAD | tee "$DIAG_DIR/git_commit.txt"
  git status --short | tee "$DIAG_DIR/git_status_before.txt"
  git diff HEAD -- \
    train.py \
    humanoid_rewards.py \
    h1_task/agent_cfg.py \
    h1_task/env_cfg.py \
    | tee "$DIAG_DIR/relevant_code_diff.txt"

  if ! git diff --quiet HEAD -- \
    train.py \
    humanoid_rewards.py \
    h1_task/agent_cfg.py \
    h1_task/env_cfg.py; then
    echo "[STOP] H1 관련 tracked 파일에 변경이 있습니다. baseline 진단을 실행하지 않습니다."
    exit 20
  fi
else
  echo "[WARN] Git 저장소가 아니므로 baseline 동일성을 hash만으로 확정할 수 없습니다." \
    | tee "$DIAG_DIR/baseline_verification_warning.txt"
fi
```

서버가 Git 저장소가 아니면 운영진이 제공한 새 환경인지 별도로 확인한다. 임의로 파일을 복구하거나 덮어쓰지 않는다.

## 3. 기존 결과물 보호

```bash
cd "$TRAIN_DIR"

if [ -d exported ] && find exported -maxdepth 1 -type f -print -quit | grep -q .; then
  echo "[STOP] exported/에 기존 결과물이 있습니다. 먼저 다운로드하세요."
  find exported -maxdepth 1 -type f \
    -printf '%TY-%Tm-%Td %TH:%TM:%TS %s %p\n' \
    | sort | tee "$DIAG_DIR/existing_exported_files.txt"
  exit 21
fi
```

기존 결과를 삭제하지 않는다. 새 환경을 사용하거나 다운로드 후 운영 절차에 맞게 정리한다.

## 4. 하드웨어와 런타임 기록

```bash
cd "$TRAIN_DIR"

{
  echo "===== nvidia-smi ====="
  nvidia-smi
  echo
  echo "===== nvidia-smi -L ====="
  nvidia-smi -L
  echo
  echo "===== uname ====="
  uname -a
} | tee "$DIAG_DIR/h1_diag_system.txt"

/workspace/IsaacLab/isaaclab.sh -p -c \
  'import sys, torch; print("python=", sys.version); print("torch=", torch.__version__); print("torch_cuda=", torch.version.cuda); print("gpu=", torch.cuda.get_device_name(0)); print("gpu_count=", torch.cuda.device_count())' \
  2>&1 | tee "$DIAG_DIR/h1_diag_python_torch.txt"
```

`nvidia-smi`의 CUDA 표시는 드라이버가 지원하는 CUDA 수준이다. PyTorch가 실제 사용하는 CUDA runtime은 `torch.version.cuda`로 따로 기록한다.

## 5. 공식 배포본의 CLI 확인

백업 wrapper는 `--task`가 없으면 종료하도록 구현돼 있으므로 task를 넣어 help를 호출한다.

```bash
/workspace/IsaacLab/isaaclab.sh -p train.py \
  --task Humanoid-v0 \
  --help 2>&1 | tee "$DIAG_DIR/h1_diag_train_help.txt"

if grep -q -- '--max_iterations' "$DIAG_DIR/h1_diag_train_help.txt"; then
  MAX_ITER_ARG=--max_iterations
elif grep -q -- '--max-iterations' "$DIAG_DIR/h1_diag_train_help.txt"; then
  MAX_ITER_ARG=--max-iterations
else
  echo "[STOP] iteration 제한 옵션을 확인하지 못했습니다. 학습하지 말고 help 파일을 검토하세요."
  exit 22
fi

echo "max_iteration_arg=$MAX_ITER_ARG" | tee "$DIAG_DIR/h1_diag_cli_selection.txt"
```

help가 실패하거나 task 등록 오류가 나면 학습으로 넘어가지 않는다. `agent_cfg.py`를 고쳐 우회하지 않는다.

## 6. GPU 시계열과 300-iteration 실행

help에서 정확한 옵션명이 `--max_iterations`임을 확인했을 때 아래 명령을 사용한다. 다른 표기라면 help에 표시된 형식을 따른다.

```bash
cd "$TRAIN_DIR"

touch "$DIAG_DIR/training_start.marker"

nvidia-smi \
  --query-gpu=timestamp,name,driver_version,memory.total,memory.used,utilization.gpu,utilization.memory,power.draw,temperature.gpu,clocks.sm \
  --format=csv \
  -l 2 > "$DIAG_DIR/h1_diag_gpu_timeseries.csv" &
GPU_MON_PID=$!

stop_gpu_monitor() {
  kill "$GPU_MON_PID" 2>/dev/null || true
  wait "$GPU_MON_PID" 2>/dev/null || true
}
trap stop_gpu_monitor EXIT INT TERM

START_EPOCH=$(date +%s)
date -Is | tee "$DIAG_DIR/training_start.txt"

NO_AUTO_SUBMIT=1 \
/workspace/IsaacLab/isaaclab.sh -p train.py \
  --task Humanoid-v0 \
  --num_envs 4096 \
  "$MAX_ITER_ARG" 300 \
  --headless 2>&1 | tee "$DIAG_DIR/h1_diag_train.log"

TRAIN_RC=${PIPESTATUS[0]}
END_EPOCH=$(date +%s)
END_TO_END_SECONDS=$((END_EPOCH - START_EPOCH))

stop_gpu_monitor
trap - EXIT INT TERM

{
  echo "exit_code=$TRAIN_RC"
  echo "start_epoch=$START_EPOCH"
  echo "end_epoch=$END_EPOCH"
  echo "end_to_end_seconds=$END_TO_END_SECONDS"
  echo "requested_iterations=300"
  echo "requested_num_envs=4096"
  echo "steps_per_env_expected_from_backup=24"
} | tee "$DIAG_DIR/h1_diag_summary.txt"

date -Is | tee "$DIAG_DIR/training_end.txt"
```

`NO_AUTO_SUBMIT=1`은 백업 `_finalize.py`에서 확인된 외부 자동 백업 비활성화 환경변수다. 학습 후 local finalize는 계속 수행된다. 실제 서버 코드가 다르면 로그로 동작을 확인한다.

`exit_code`가 0이 아니면 같은 명령을 즉시 재실행하지 않는다. 로그와 GPU 기록부터 내려받아 원인을 확인한다.

## 7. 결과 파일 수집

```bash
cd "$TRAIN_DIR"

tail -n 200 "$DIAG_DIR/h1_diag_train.log" \
  > "$DIAG_DIR/h1_diag_train_tail.txt"

{
  echo "===== files created after training start ====="
  for path in logs exported; do
    if [ -e "$path" ]; then
      find "$path" -type f -newer "$DIAG_DIR/training_start.marker" \
        -printf '%TY-%Tm-%Td %TH:%TM:%TS %s %p\n'
    fi
  done | sort
} | tee "$DIAG_DIR/h1_diag_recent_files.txt"

# 이번 실행에서 생성·갱신된 logs/와 exported/ 파일을
# 상대경로 그대로 별도 묶음에 보존한다.
NEW_RESULTS_LIST="$DIAG_DIR/h1_diag_new_result_files.null"
: > "$NEW_RESULTS_LIST"

for path in logs exported; do
  if [ -e "$path" ]; then
    find "$path" -type f -newer "$DIAG_DIR/training_start.marker" -print0 \
      >> "$NEW_RESULTS_LIST"
  fi
done

if [ ! -s "$NEW_RESULTS_LIST" ]; then
  echo "[STOP] 이번 실행에서 생성된 logs/exported 파일을 찾지 못했습니다." \
    | tee "$DIAG_DIR/result_collection_error.txt"
  exit 23
fi

tar --null -T "$NEW_RESULTS_LIST" -czf "$DIAG_DIR/h1_diag_new_run_artifacts.tar.gz"

find logs -type f -name 'events.out.tfevents*' \
  -newer "$DIAG_DIR/training_start.marker" -print 2>/dev/null \
  | sort | tee "$DIAG_DIR/h1_diag_tensorboard_events.txt"

for result_file in exported/model_best.pt exported/env.yaml exported/report.html; do
  if [ -f "$result_file" ]; then
    cp -p "$result_file" "$DIAG_DIR/"
    sha256sum "$result_file"
  fi
done | tee "$DIAG_DIR/result_sha256.txt"

tar -czf "/workspace/${RUN_ID}.tar.gz" \
  -C /workspace/h1_diagnostics "$RUN_ID"

echo "진단 묶음: /workspace/${RUN_ID}.tar.gz"
echo "새 run 전체 묶음: $DIAG_DIR/h1_diag_new_run_artifacts.tar.gz"
echo "학습 결과 원본: $TRAIN_DIR/logs/ 및 $TRAIN_DIR/exported/"
```

`h1_diag_new_run_artifacts.tar.gz`는 marker 이후 생성·갱신된 `logs/`와 `exported/` 파일을 상대경로 그대로 담고, 최종 `/workspace/${RUN_ID}.tar.gz` 안에 포함된다. `h1_diag_tensorboard_events.txt`가 비어 있으면 사용자가 종료를 요청한 경우에도 먼저 실제 run 폴더와 logger 설정을 확인한다. 이전 run 파일을 임의로 삭제하거나 이번 묶음에 섞지 않는다.

백업 코드상 `model_best.pt`와 `env.yaml`은 finalize 결과이며 `report.html` 생성은 조건부다. `play.py`를 실행하지 않았으므로 `policy.pt`가 없어도 이번 진단에서는 정상이다.

## 8. 다운로드 및 사용자 결정 종료

최소한 다음을 다운로드한다.

1. `/workspace/h1_diag_날짜시간.tar.gz` — 새 `logs/`·`exported/` 전체 묶음 포함 여부 확인
2. `training/humanoid/logs/<이번_run>/` 원본 전체 — 이중 확인용
3. `training/humanoid/exported/model_best.pt`
4. `training/humanoid/exported/env.yaml`
5. 존재한다면 `training/humanoid/exported/report.html`
6. 대시보드의 실행 전·후 남은 시간 또는 실제 사용시간 기록

파일 크기와 필요한 hash를 확인한다. 공식 서버 종료는 사용자가 명시적으로 요청한 경우에만 별도 수행한다.

## 9. 측정값 계산 규칙

### 전체시간과 안정 구간을 구분한다

`end_to_end_seconds`에는 simulator 초기화, 학습, checkpoint 선별, `env.yaml`·리포트 생성, 종료 정리가 포함될 수 있다. 이것을 바로 300으로 나눈 값은 순수 iteration 시간이 아니다.

로그에 iteration별 시간 또는 FPS가 있으면 초기 불안정 구간을 제외한 동일 구간의 중앙값을 사용한다. 제외할 iteration 수는 로그를 본 뒤 기록하고 임의로 숨기지 않는다.

```text
steady_sec_per_iter = 선택한 안정 구간 iteration 시간의 중앙값

예상 장기 실행시간
≈ 초기화 시간 + 목표 iterations × steady_sec_per_iter + finalize 시간
```

### 처리량 계산은 실제 설정을 우선한다

백업 설정의 `num_steps_per_env`는 24다. 실제 공식 서버의 로그나 `env.yaml`에서 같은지 확인한 뒤 계산한다.

```text
environment_steps_per_iteration = actual_num_envs × actual_num_steps_per_env
```

요청값이 실제 적용됐는지 확인하기 전에는 `4096 × 24`를 확정값으로 쓰지 않는다.

### 개인 서버 비교 조건

가능한 한 다음 조건을 같게 맞춘다.

- 동일 코드 commit 또는 파일 hash
- 동일 task와 robot configuration
- 동일 `num_envs`와 `num_steps_per_env`
- 동일 headless·camera 설정
- 동일 seed
- 동일 terrain·observation·PPO configuration

조건이 다르면 GPU의 순수 성능비로 해석하지 않고 차이를 함께 기록한다.

## 10. 완료 판정

- [ ] 관련 코드의 Git diff가 없거나 새 공식 환경임을 확인했다.
- [ ] 코드 commit과 SHA-256을 기록했다.
- [ ] help에서 실제 iteration 제한 옵션을 확인했다.
- [ ] GPU·Python·PyTorch runtime 정보를 기록했다.
- [ ] H1 300-iteration 진단을 한 번만 실행했다.
- [ ] exit code와 전체 실행시간을 기록했다.
- [ ] GPU 시계열과 전체 학습 로그를 다운로드했다.
- [ ] 새 `logs/<run>/` 전체와 TensorBoard event를 다운로드했다.
- [ ] 중간 checkpoint와 설정 파일이 run 묶음에 포함됐는지 확인했다.
- [ ] `model_best.pt`와 `env.yaml`을 다운로드했다.
- [ ] 대시보드 사용시간을 기록했다.
- [ ] 사용자가 명시적으로 요청한 경우에만 서버를 종료했다.

## 근거와 한계

이 가이드의 명령과 파일 동작은 다음 백업 자료와 교차검증했다.

- `../server_backup/code/training/humanoid/README.md.md`
- `../server_backup/code/training/humanoid/train.py.md`
- `../server_backup/code/training/humanoid/h1_task/agent_cfg.py.md`
- `../server_backup/code/training/humanoid/h1_task/_finalize.py.md`

백업은 실제 공식 서버의 현재 배포본과 다를 수 있다. 그래서 이 문서는 help·Git 상태·실제 로그를 먼저 수집하고, 일치하지 않으면 중단하도록 설계했다. 공식 서버 운영 규칙과 최신 공지가 이 가이드보다 우선한다.
