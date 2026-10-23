# 검증 기록 — 2026-10-02

## 2026-10-07 후속 H1 PERSONAL 실전 평가 근거

아래 2026-10-02~04 CPU/설치 기록의 `H1 GPU 미실행`은 **당시 스냅샷으로 보존**한다. 이후 별도 받은 [`ORIENT-100 / model_2850` H1 정책 분석](https://github.com/SE3C/naver-issacsim/blob/main/data/processed/incoming/other/reviewed/H1_ORIENT-100_POLICY_ANALYSIS_20261007.md)은 Windows PERSONAL 6영상·camera-off `scenario7` full(8 case × 3 seed × 128 env = **3,072 episode**, 20초 timeout, base-contact failure 0, child exit 0, `complete=true`)의 수집·재집계 근거다. H1 evaluator **단일 정책 GPU full evidence 확보**로 상태를 갱신하되, matched A/B, official score, full 새 렌더+평가 단일 invocation의 별도 재현 검증까지 완료됐다고 주장하지 않는다. 본 문서 변경은 실행 기록을 생성하지 않는다.



## 후속 Windows 통합 검증

이 문서의 아래 절들은 최초 CPU 구현과 standalone smoke 실패 당시의 역사 기록이다. 이후 검증된 CUDA 초기화 수정·pre-close traceback/FAILED 보존·통합 6영상 실행기를 이 저장소에 동기화했다. 현재 설치와 2950·7050 개별 full 기록은 [Windows 실행 지침](WINDOWS_WORKFLOW.md)을 따른다. 기존 6영상 receipt를 재사용해 두 full이 native/BAT exit0으로 완료됐다. 새로운 GPU 재실행·H1 전체 평가·실제 A/B calibration/score/비교 보고서는 이번 동기화에서 하지 않는다.

동기화 후보의 CPU unit tests는 **52/52 PASS**: 기존 45개, 실패 기록 3개, 통합 ZIP 4개다. ZIP 테스트는 synthetic 영상·평가 fixture로 정확한 18개 항목, checksum, 기존 파일 보존, smoke/incomplete 거부, 평가·영상 변조와 checkpoint link mismatch 차단을 확인한다. 추가로 이미 완료된 실제 2950·7050 영상 ZIP과 개별 평가 ZIP을 receipt SHA와 대조해 두 통합 ZIP을 생성·CRC·전 항목 SHA 검증했다. GPU·실제 A/B 비교는 재실행하지 않았다.

## H1 Windows 통합 source 추가 — 2026-10-04

공용 `eval_core.py`와 `isaac_runner.py`는 기존부터 H1을 지원하므로 계산·collector source는 변경하지 않았다. Go2 통합 launcher를 최소 변형해 `h1_6terrain_video.bat/.ps1`, `h1_eval_smoke.bat/.ps1`을 추가하고, installer가 같은 evaluator bundle을 `h1-video-evaluator/`에도 배포하도록 확장했다. H1 고정 영상 slope는 프로젝트의 기존 H1 6지형 규칙과 `load_suite("h1")`에 맞춰 10°(`0.176326981`)를 사용한다.

추가한 H1 bundle contract test는 `Humanoid-v0`, `training/humanoid`, `h1_task`, 10° slope, H1 scenario7 연결과 18-entry combined ZIP의 보존/변조 거부 계약을 검사하도록 작성했다. 구현 후 통합 smoke validator에 Go2의 첫 scenario ID `G1`이 한 줄 남아 H1 smoke를 잘못 거부할 수 있는 결함을 확인했고, 이를 H1 첫 scenario ID `H1`로 수정하고 회귀 assertion을 추가했다. **이 connector 작업 환경에서는 Windows PowerShell·Isaac Sim/GPU를 실행하지 않았으므로 실제 H1 GPU PASS는 아직 없다.** Go2 GPU 기록을 H1로 소급하지 않는다.

## 실행한 검증

- Windows 로컬 Python CPU 단위 테스트: **33/33 PASS**.
- Python source 및 두 테스트 파일의 compile 검사: PASS.
- Git Bash의 `bash -n run_evaluation.sh`: PASS.
- launcher의 OFFICIAL 환경 거부(exit 2): 확인.
- H1 / Go2 각각 scenario7 / terrain6의 합성 JSONL 생성 → calibration → score → A/B bootstrap → JSON/HTML 생성: **4개 조합 PASS**.
- 종료 우선순위, reset 후 partial episode, cohort 누락, protocol/policy 불일치, calibration 오용, bootstrap 재현성과 signed 변위 검사 포함.
- IsaacLab/RSL 버전별 observation·native load·contact term API는 CPU fixture로 검사. 실제 simulator 통합 테스트와 동일한 검증은 아님.
- 세 서브에이전트의 source/API 조사, 근거 검토, scorer test 작성 후 메인에서 통합·정합성 검토.

## 최초 구현 시 실행하지 않은 검증

- 실제 Isaac Sim/Lab 시작, GPU physics, native checkpoint inference 및 TorchScript 추론.
- WSL camera-off 구동과 128/256/512 env 실측 비교.
- 실제 정책/negative control에 기반한 e50 calibration 및 공식 평가 점수와의 상관 검증.

위 항목은 최초 CPU-only 구현 당시의 기록이다. 이후 Windows 실제 smoke 실행은 아래 최신 절에 기록한다. 현재 결과는 **CPU 로컬 검증된 v1 구현**이지 GPU 평가 성공까지 확인된 production scorer가 아니다. 짧은 smoke 성공도 전체 7시나리오 완료나 정책 품질 PASS를 뜻하지 않는다.

전체 평가에서는 같은 native stack·source·config·env 수·seed·suite로 reference와 후보들을 평가한다. calibration을 고정하기 전 점수/CI는 잠정값이며 최종 제출 선택을 자동 수행하지 않는다. 현 v1은 feed-forward 정책을 대상으로 하고 native recurrent 정책은 거부한다.

## 최초 구현 당시 보존·안전 경계

네 저장소의 tracked 파일과 원본 ZIP/HANDOFF, 기존 evidence/checkpoint/video는 변경하지 않았다. 학습·공식 서버 실행·GitHub 게시·설치·서버 종료를 실행하지 않았으며 evaluator에도 해당 자동 후처리 기능은 없다. 결과는 새 폴더로만 생성하고 실패/중단 raw data는 보존한다.

## Windows smoke CLI — 2026-10-03

`go2_eval_smoke.ps1`/`.bat`을 추가했다. PowerShell 5.1 구문 검사, checkpoint 미리보기, TorchScript/256 env 미리보기, 없는 입력 거부를 확인했다. Preview에서 Isaac/GPU 프로세스와 결과 폴더가 생성되지 않았다. 이 절은 CLI 작성 당시 기록이며 이후 실제 smoke 실패는 아래 절에 기록한다. CLI는 기존 6영상 스크립트·task source·학습 stack을 수정하지 않는다.

## 두 경로 비교 CLI — 2026-10-03

`compare_cli.py`와 Windows `compare_policies.ps1`/`.bat`을 추가했다. 기존 collector를 A/B 순차 실행하고 scorer/calibration/HTML 함수를 재사용한다. 완료된 평가 폴더의 합성 데이터로 리포트 생성, 기존 calibration 보존, 입력 프롬프트, 기존 output 보존, 실패 시 다음 실행 차단, preview 무실행, incomplete/protocol mismatch 및 official/혼합 형식 거부를 확인했다. native task config는 설치된 IsaacLab의 공개 `handle_deprecated_rsl_rl_cfg`가 있을 때만 사용하며 구버전의 기존 경로도 fixture로 확인했다.

CPU 테스트 **45개 PASS**. Windows 비교 CLI도 PowerShell 5.1 구문·공백 포함 경로 미리보기·없는 입력 거부를 확인했다. 불일치 calibration은 첫 평가 후 두 번째 GPU 실행 전에 거부한다. 저장된 평가 폴더 비교는 일반 Python을 사용하며, SDK가 없는 경로를 지정한 합성 데이터 HTML/JSON 생성도 PASS했다. 실제 checkpoint의 GPU 평가·점수 정확도는 아직 검증하지 않았다. 기존 점수 산정식과 공식 학습/영상 코드는 변경하지 않았다.

## Windows 실제 smoke — 2026-10-03 (실패)

사용자의 실행 요청에 따라 `C:\NCRC\go2_eval_smoke.ps1`을 Downloads의 `model_2950.pt`로 실행했다. 기본 128 env·seed4201·camera-off·2초 조건이다. Isaac startup은 완료됐지만 episode 출력 없이 종료했고, CLI가 exit 1로 실패를 판정했다. 결과는 `model_2950_go2_eval_smoke_128env_20261003-131151_a308843b` 디렉터리에 보존했다.

`evaluation_manifest.json`, `resolved_configs.json`은 존재하지만 `episodes.jsonl`은 없다. 종료 후 manifest는 RUNNING/complete=false로 남았고 error가 없어 실제 원인은 미확정이다. 따라서 GPU 평가/inference·전체 suite 성공은 주장하지 않는다. 이 실행 이후 수정이나 GPU 재시도는 하지 않았다. 원본 checkpoint, 6영상 스크립트 및 실패 자료는 보존했다.

로그 위치·실행 기반·후속 구현 방향은 [Windows 영상/evaluator 인계](WINDOWS_VIDEO_EVAL_HANDOFF.md)에 정리했다.
