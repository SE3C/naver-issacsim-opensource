# 검토 산출물 안내

**본 산출물은 원본 프로그램의 수정본이 아닙니다.** ZIP 원본 및 별도 UI HTML을 재포장하지 않았습니다. source 의존성을 재현하려면 사용자가 `ncrc_h1_end_to_end.zip`을 별도 경로에 풀어 `NCRC_SOURCE_DIR`로 지정해야 합니다.

- `REVIEW_REPORT_ko.md`: 2026-10-15 한국어 심층 검토 보고서, 코드 파일:줄 근거와 판단.
- `test_optuna_cpu.py`, `optuna_cpu_results.json`, `optuna_cpu_stdout.txt`: 원본 app.py를 **import** 후 Optuna 4.8.0/임시 SQLite·임시 localhost HTTP로만 검증한 CPU 테스트. GPU/실제 evaluator 안 함.
- `test_ui_calibration.js`, `ui_calibration_results.json`, `ui_cpu_stdout.txt`: 원본 ZIP `index.html`의 상수·pure function 발췌 계산. Node.js 필요.
- `test_worker_pure_cpu.py`, `worker_pure_results.json`, `worker_cpu_stdout.txt`: worker AST 순수 함수만 추출, IsaacLab/AppLauncher import 안 함.
- `audit_saved_eval_zip_cpu.py`: 개인 PC 기존 통합 평가 ZIP을 위한 **schema-only** 감사 도구. 실제 Windows evaluator schema는 이번 입력에 없으므로 자동 점수 계산/비교를 하지 않음.
- `fixture_synthetic_eval.zip`, `fixture_audit_results.json`, `fixture_audit_stdout.txt`: audit 도구 자체를 검사한 **가상 manifest/episodes/diagnostics 3파일**. 학습·평가·공식 증거 아님.
- `calibration_profiles.csv`, `term50_anchor_inferred.csv`, `search_space.csv`: 원본 상수의 CPU 재계산표. 원본 official H1~H7 문서를 대체하지 않음.
- `TEST_STATUS.json`: 실제 실행한 테스트 명령, 결과, 제한.

**실제 평가기/Isaac Sim/학습/영상/export/서버/업로드는 실행하지 않았습니다.** CPU-only 시험 이외의 runtime 적합성은 주장하지 않습니다. 보고서와 테스트의 임시 조작은 원본 입력을 바꾸지 않습니다.
