# NCRC 개인 PC Optuna Ask/Record/Tell v2.0.0

**범위:** 오직 개인 PC의 CPU Optuna 후보 `Ask` → 수동 증거/진단 `Record` → 조건 만족 시 명시적 `Tell` 또는 `Abandon`. 기존 Windows PERSONAL 평가기·실제 reward/학습 코드는 건드리지 않는다. GPU·자체 evaluator·공식 서버 연동은 없다.

## 실행

Python 및 Optuna 4.x 필요 (`requirements.txt`는 `optuna>=4.0,<5` 유지). 인터넷이 연결되는 설치 환경에서 필요할 때만 다음을 실행한다. 앱 실행 시 패키지를 자동 설치하지 않는다.

```bash
python -m pip install -r requirements.txt
python app.py --host 127.0.0.1 --port 8765 --open
# 또는 Windows: start.bat / Linux, macOS: bash start.sh
```

브라우저 `http://127.0.0.1:8765/` 에서 **새 후보 Ask**, Trial 선택, 수동 identity/진단 Record, 실패 시 Abandon, 허용되는 경우에만 **직접 수치 Tell**. `Tell`은 다음 `Ask`를 실행하지 않는다. 시작할 때 현재 study를 읽고, 재시작 후 **SQLite DB가 상태의 기준**이 된다. `optuna_history.jsonl`은 보조 감사 기록이다. 원본·새 DB를 혼동하지 않도록 v2는 자체 `ncrc_optuna.db`를 새 위치에 만들며 원본 DB를 마이그레이션하지 않는다. 원본 study는 자동 수용/수정하지 않는다.

`study_config.json`에는 기존 원본 `app.py`의 **9개 범위를 보존**했지만 이는 실험용으로 승인한 범위가 아니다. 특히 기존 `action_rate_l2` 상한 `-0.0002`는 실제 사용한 `-0.0001`을 포함하지 않는다. 항목/범위 또는 동결 기준이 바뀌면 별도의 **새 stage**를 사용한다. 정확한 고정값은 `[ -0.0001, -0.0001 ]`, 포함 가능한 연속 범위는 `[lo, hi]`로 설정할 수 있지만 **사용할 탐색 범위 자체는 사용자가 증거에 근거해 결정**해야 한다. 예시 범위를 정책 권고로 받아들이지 않는다.

## 최적화 준비 조건

`study_config.json`의 `objective`와 `comparison` 기본값은 **둘 다 `null`**이며, 이 상태는 **Ask·진단 기록 가능 / Tell 차단**이다. 다음 객체는 필수 **키의 형태만** 보여주며 숫자·조건을 제공하거나 승인하지 않는다:

```text
"objective": {
  "name": "<검증된 평가 지표 정의>", "unit": "<단위>",
  "source": "<실제 평가기·필드·집계 정의 근거>",
  "direction": "maximize 또는 minimize",
  "min": <승인된 하한>, "max": <승인된 상한>
},
"comparison": {
  "protocol_id": "<실제 고정 protocol ID>",
  "evaluator_id": "<실제 평가기 source ID>",
  "training_mode": "fresh 또는 resume",
  "training_iterations": <실제 동일 학습량>,
  "training_seed": <실제 동일 seed>,
  "checkpoint_selector": "<고정 선택 방법>",
  "parent_checkpoint_sha256": "<resume 시 실제 64자리 SHA, fresh 시 생략>"
}
```

목적함수·비교 조건은 과거 결과에서 멋대로 추정할 수 없으며, 실제 승인 후 **Ask 이전에** 설정해야 한다. 첫 Ask가 실행되면 reward_context/search_space/objective/comparison 전체를 study `user_attrs`에 **동결**한다. 나중에 파일을 바꾸면 이전 stage는 Ask/Record/Tell을 거부한다. 탐색만 하던 `objective:null` stage에 목적함수를 사후 채워 기존 trial을 최적화 trial로 바꾸는 기능은 **의도적으로 없다**. 그 대신 새 stage를 만들고 실제 조건을 검토한다. Run ID는 Ask 시 미래이므로 요구하지 않는다.

수동 Record에서는 실제 `training_run_id`, 선택 `checkpoint_sha256`(전체 64 hex), `evaluation_id`, `protocol_id`, `evaluator_id`, `parent_checkpoint_sha256`(resume), `training_iterations`, `training_seed`, `checkpoint_selector`, `resolved_reward_id` 등을 기록한다. 알 수 없는 값은 공란=미확인으로 기록된다. `HOLD`·`REJECT`는 숫자로 치환하지 않는다. 결과가 불완전하거나 조건이 불일치하면 Tell은 거부된다. 완전한 수동 입력도 **사용자가 제공한 진술일 뿐 앱이 checkpoint/evaluator 바이트를 독립 검증한 것이 아니다**. 기록만으로 공식 점수 또는 reward의 인과 효과가 성립하지 않는다.

입력 수치는 `objective_value` **하나만** 허용하며, 실제 정의된 목적함수의 단위·min/max 범위에서 유한한 JSON 숫자여야 한다. `score_70`, `objective`를 동시에 전달하거나 빈값·문자열·NaN·무한대는 거부한다. 유효한 0은 원래 목적값 정의·수동 근거가 있고 실제 입력되었을 때만 가능하며 입력 누락 대신 자동으로 쓰지 않는다. 원본 TERM50 단일 anchor 및 LOG heuristic은 `reference/calibrator_DIAGNOSTIC_ONLY.html`에 **참고 계산용**으로만 격리했다. 그 HTML이 산출하는 값으로 Tell하지 않는다.

## Sampler·재시작·장애 정책

- stage별 `TPESampler`를 서비스 **프로세스가 살아 있는 동안 캐시**하여 요청 때마다 동일 seed 초기화하지 않는다. seed 베이스 `20260922`, `n_startup_trials=8`, `multivariate=True`를 유지한다. 새 stage의 seed는 stage 이름/현재 trial 개수로 유도된다.
- 앱이 재시작되면 **RNG 내부 상태를 정확하게 복원하지 않는다**. 대신 SQLite의 해당 stage에 이미 존재하는 trial 개수로 새 seed를 유도하여 첫 후보 반복을 피한다. **재시작을 끼운 연속 Ask 시퀀스는 무중단 시퀀스와 bitwise identical하지 않을 수 있다.** Optuna 버전 변경도 시퀀스 동일성 보장 없음. 연속 seed 충돌 회피가 고유 후보를 수학적으로 보증하지는 않으며 고정 범위나 TPE에 의도적 중복 후보가 존재할 수 있다.
- HTTP 동시 요청은 단일 프로세스 `RLock`으로 직렬화한다. **같은 DB에 앱 2개 이상을 동시에 실행하지 말 것**(분산 locking·동시 다중 프로세스 지원 제외). `--host`는 `127.0.0.1`만 허용한다. 서버는 로컬용이며 다른 PC 공개/연동용이 아니다.
- 중복 Tell은 Optuna `RUNNING` 상태가 아니라면 차단된다. `Abandon`은 사유와 함께 Optuna `FAIL`로 남긴다. 데이터베이스 commit과 JSONL append는 원자적이지 않다. history 장애/응답 유실 시 `/api/study`의 SQLite 상태를 먼저 확인하고, **완료된 trial을 재-Tell하지 않는다**. Optuna DB 파일 자체 손상/복수 프로세스 경쟁 자동 복구는 제공하지 않는다.

## 수동 CPU 검토

```bash
python -m py_compile app.py
python -m unittest discover -s tests -p 'test_*.py' -v
node tests/test_ui_static.js              # Node가 있다면 선택
```

테스트는 임시 DB·가상 ID/목적값을 사용하며 실제 H1 결과가 아니다. 본 개선 ZIP의 `tests/cpu_test_stdout.txt`, `tests/TEST_RESULTS.json`과 `REPORT_ko.md`에 확인 결과를 기록했다. 원본 작업물이 필요하면 최종 배포 ZIP의 `source_originals/` 안에 전달 당시 ZIP 그대로 있다.
