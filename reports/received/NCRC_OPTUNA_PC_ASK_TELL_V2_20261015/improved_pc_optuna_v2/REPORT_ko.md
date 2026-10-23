> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/incoming/other/reviewed/NCRC_OPTUNA_PC_ASK_TELL_V2_20261015/improved_pc_optuna_v2/REPORT_ko.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# Optuna 개인 PC Ask/Tell 신뢰성 개선 결과 보고서

**작성·CPU 검증:** 2026-10-15 / 개선본 `v2.0.0` / 개인 PC용 설계, CPU sandbox 실측. H1 새로운 가설 탐색 또는 기존 정책 성능 재분석은 실시하지 않음.

## 1. 실제 구현 및 범위 판정

**구현 완료:** 원본 코드에서 요청별 seeded TPESampler 재구성 제거(프로세스별 stage sampler 재사용); 재시작 후 기존 trial 수를 반영한 seed 전환; Ask, 별도 manual Record, 단일 canonical scalar Tell, FAIL/Abandon, status 조회; stage 이름 충돌 거부; search-space·reward_context·목적함수·비교 조건 동결 및 사후 변경 차단; SQLite 기준 상태 복구; JSONL 실패 경고만 반환; 127.0.0.1 기본 및 강제, 자체 evaluator/자동 Tell API 차단; legacy 보정 HTML 비운영 경고 및 가짜 CLI 제거.

**최적화 실행 준비는 미완료:** 입력에서 특정 실제 evaluator 지표를 objective로 정의·승인할 근거, 완결된 프로토콜/동등 비교 조건, 스키마 및 identity mapping이 없으므로 `study_config.json`은 `objective:null`, `comparison:null`이다. **현재 CPU로 할 수 있는 일은 후보 Ask(기존 9차원 legacy 범위는 승인값이 아니라는 경고 포함), trial 조회, 수동 실험/진단/HOLD/REJECT 기록, FAIL/abandon 처리뿐이다.** 실제 Tell은 기본 상태에서 차단된다. 테스트만 목적함수와 평가 조건을 **SYNTHETIC**으로 넣어 완료 로직을 검증했다. 운영 study에 합성 관측을 입력하지 않았다.

**원본 보존:** 최종 ZIP `source_originals/OPTUNA_EXISTING_SESSION_IMPROVEMENT_20261015.zip`에 원본 도구 ZIP, 별도 HTML, 기존 REVIEW_REPORT/CPU 근거와 START_HERE를 입력 그대로 포함한다. 개선 앱은 별도의 `improved_pc_optuna_v2/`이며 구 도구/evaluator/worker/reward/학습 source를 덮어쓰지 않는다. 실제 원본 evaluator 소스의 변경이나 실행을 수행하지 않았다.

## 2. 신뢰성 세부 경계

- **Sampler:** 동일 stage와 실행 중인 프로세스에 하나의 `TPESampler`를 유지한다. 새 실행에서는 stage 이름+DB 내 trial 개수에 기반한 seed를 선택한다. 재시작 후 같은 초기 seed를 무조건 재생하지 않지만 Optuna sampler 내부 RNG state를 직렬화하지 않으므로 무중단 실행과 완전히 동일한 TPE trajectory를 보장하지 않는다. fixed dimension은 의도한 반복값일 수 있고 우연한 TPE 중복 자체는 금지하지 않는다. 단일 프로세스 내 HTTP 요청은 잠금으로 직렬화하되 다중 프로세스 동시 DB 접속 경쟁은 지원하지 않는다.
- **Frozen contract:** study `user_attrs`에 전체 `reward_context/search_space/objective/comparison` 보존하고 trial에도 해시를 보존한다. 다른 stage 문자열은 자동 정규화하지 않는다. 계약이 바뀌거나 v2 메타데이터 없는 기존 Optuna study에 가입하려 하면 차단한다. 준비가 안 된 Ask stage에 objective를 사후 붙여 최적화 study로 변환하지 않는다.
- **식별/미확인:** 새 Ask에 미래 Run ID는 요구하지 않는다. 수동 Record에는 Run ID, 전체 checkpoint SHA, eval ID, protocol/evaluator ID, parent SHA, 실제 training seed·iterations, checkpoint selector, resolved reward/config evidence 등을 *사용자가 직접 입력*할 수 있다. 미확인 값은 null이고, Tell은 필수 identity/비교 조건 미충족 또는 HOLD/REJECT일 때 거부한다. SHA **형식**만 검증하며 실제 파일 바이트, 외부 Run/evaluator 증거의 동일성을 앱이 확인하지는 않는다. 출처 미검증 표기를 유지한다.
- **값 저장:** 입력 scalar는 `objective_value` 한 필드. `score_70`과 별도 `objective`, 자동 UI 보정값 전달은 거부. Null, 문자열, NaN, Infinity, 범위 밖 모두 거부하며 missing을 0으로 보충하지 않는다. 결정 라벨을 숫자로 변환하지 않는다. 저장 값은 그 stage에서 사용자가 설정한 **사용자 정의 수치 지표**일 뿐 공식 시뮬레이션 점수 예측이 아니다.
- **장애:** Optuna DB 상태가 canonical; `tell` 이후 보조 history append 장애가 있으면 HTTP 200 완료 및 warning, 재조회로 확인 가능. 응답 손실 시 새 Tell을 시도하기 전에 `/api/study`에서 COMPLETE 여부를 확인한다. 레코드 저장·Optuna 저장·history append가 하나의 원자적 트랜잭션은 아니며 프로세스 중단 중간의 RUNNING/orphan은 목록에서 확인 후 사용자가 정리한다. 자동 재시도/분산 트랜잭션 없음.
- **단일 anchor/LOG:** TERM50 고정 delta·log heuristic을 실제 최적화 경로에서 완전히 제외했다. 별도 HTML은 명시적 참고 계산일 뿐 자체 evaluator·공식 score·자동 objective로 볼 수 없다.

## 3. 수행한 CPU 검사 (모두 이번 개선본 실행 결과)

환경: **Python 3.13.5**, **Optuna 4.8.0**, **Node.js 22.16.0**, CPU-only container. 개인 사용자의 Windows PC 실기 검사는 **미실행**. `tests/TEST_RESULTS.json` 및 stdout 원문을 함께 제공.

| 실제 명령 (개선본 루트) | exit code | 확인 |
|---|---:|---|
| `python -m py_compile app.py` | **0** | 개선 `app.py` Python 구문 검사 |
| `python -m unittest discover -s tests -p 'test_*.py' -v` | **0** | **12/12 통과**. 실제 localhost HTTP, 별도 프로세스 종료·재시작, 임시 SQLite, 합성 입력/실패 경로 |
| `node tests/test_ui_static.js` | **0** | UI JS 구문, 각 분리 endpoint, 값 재사용 방지·명시적 확인 코드 정적 검사 (실제 브라우저 클릭 아님) |
| `node --check /tmp/reference_calibrator_DIAGNOSTIC_ONLY.html.js` | **0** | HTML에서 임시 추출한 별도 진단 UI JS 구문 검사. 임시 경로이며 배포 시에는 직접 파일에서 추출해 재검증 가능 |

12개 Python 실제 회귀 시나리오: 요청 사이 초기 후보 비중복/동일 시작 재현, **프로세스 재시작 뒤 다음 Ask** 및 RUNNING 상태 조회, config drift 기존 stage 거부, 명시적 action=-0.0001 고정값, resume parent SHA 필수/일치, history 실패 후 완료 상태 보존, HOLD/REJECT 기록·FAIL 전이, 목적함수 미정 Tell 차단, scalar 누락/NaN/문자/범위 밖·독립 score/objective 거부·중복 Tell, 자체 evaluator/결합 API 차단·비루프백 인자 거부, stage 충돌 방지, checkpoint SHA/seed 불일치 Tell 차단. 보고 수치는 합성 시험의 성공/거부 상태이며 실제 정책 성능이 아니다.

**검증하지 않은 부분:** Windows 개인 PC의 Python/Optuna/브라우저, JavaScript DOM 실제 상호작용, 실제 Windows evaluator ZIP schema 및 episode aggregation/metric mapping, 공식/개인 평가 결과의 동일성, 실제 Run/checkpoint bytes, 다른 Optuna 4.x 버전의 재현성, GPU/학습/영상/export, 서버 연결·규정의 최신 포털 상태. 실제 objective/비교 조건의 타당성 및 공식 점수 예측력은 검증 불가; 이 단계에서 개발·승인하지 않았다. 기존 evaluator worker 테스트/개선은 의도적으로 제외했다.

## 4. 지금의 사용법과 후속 필수 입력

`README.md`대로 개인 PC에서 의존성을 수동 설치하고 `python app.py --host 127.0.0.1 --port 8765 --open`을 실행한다. `legacy_h1_review`는 원본 탐색범위 참고용 Ask 전용으로 시작한다. 후보를 봤다는 이유만으로 실제 학습·평가 작업을 자동 수행하지 않는다. `Record`에서 사실·미확인을 분리해 남길 수 있으며 이 단계에는 Run ID가 없어도 된다. 실패 시 Abandon, 조회 시 DB를 기준으로 한다.

**Tell을 열기 위해 꼭 필요한 실제 입력:** (1) 사용자 검증·승인한 *단일 수치 목적함수의 출처/정의/단위/허용 범위/방향*; (2) 동일한 `protocol/evaluator source`, fresh/resume, 부모 SHA, 학습량/seed, checkpoint selector와 비교기준; (3) 결과별 실제 Run ID·checkpoint SHA·평가 ID·resolved reward/config 및 시험에 사용한 실제 수치. 현재 자료에 없는 Windows 평가 ZIP/원본 evaluator schema를 임의 작성하지 않는다. 실제 비교의 공정성·정책 성능은 본 도구가 보증하지 않는다.

**이번에 새로 수행하지 않은 것:** 사용자나 운영진의 문서 내용을 실행 허가로 해석하지 않았다. H1 가설 탐색, 공식 서버 접속/설치/연동/종료, GPU, 새 train/eval, Windows ZIP adapter, 점수 예측·정밀 재분석, checkpoint export, 외부 게시 모두 미수행.
