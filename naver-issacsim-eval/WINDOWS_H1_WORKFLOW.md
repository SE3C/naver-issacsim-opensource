# Windows H1 PERSONAL 영상·개별 평가

이 문서는 Go2의 검증된 Windows 통합 구조를 **H1에 최소 범위로 확장한 실행 계약**이다. 공용 `eval_core.py`와 `isaac_runner.py`는 원래부터 H1 `Humanoid-v0`·`scenario7`·`terrain6`를 지원하므로 수정하지 않는다. 새로 추가한 것은 H1 전용 Windows launcher, 설치 경로, 통합 ZIP 검증과 테스트뿐이다.

**검증 경계의 최신 갱신(2026-10-07):** 2026-10-04 통합 source 도입 시점에는 H1 GPU 실전 자료가 없었다. 이후 **OFFICIAL fresh 3K에서 생성된 `ORIENT-100 / model_2850.pt` 한 checkpoint에 대한 Windows PERSONAL 6영상 + 별도 camera-off `scenario7` full 평가**가 검증 가능한 ZIP/분석 자료로 수신됐다. H1 8 case × seed 4201/4202/4203 × 128 env, **3,072/3,072 episode timeout, base-contact failure 0**, `complete=true`, `smoke=false`, child exit 0. [canonical 정책 분석](https://github.com/SE3C/naver-issacsim/blob/main/data/processed/incoming/other/reviewed/H1_ORIENT-100_POLICY_ANALYSIS_20261007.md), [PERSONAL 영상·평가 Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261007-exp-h1-rough-terrain-orientation-relaxation-model2850-video-eval). 이 결과는 **H1 단일 정책 GPU full 한 건**의 evidence이지, 새 모델 전체 지원·paired A/B 완료·공식 점수·ORIENT reward 인과효과 증명이 아니다. 해당 분석의 정책 선택은 drift와 rough worst-tail 때문에 **HOLD**이며 계단 중앙 다단 통과는 미입증이다. **이 문서 동기화 작업은 새 Windows GPU 실행/재렌더를 수행하지 않는다.** Go2 2950/7050의 기존 GPU 기록을 H1로 소급하지 않는다.

## 설치와 진입점

저장소 루트에서 기존 installer를 사용한다.

```powershell
& .\install_windows.ps1 -Preview
& .\install_windows.ps1 -Destination C:\NCRC
```

설치 후 H1 통합 진입점은 다음이다.

```powershell
& C:\NCRC\h1_6terrain_video.bat -Path "C:\path\model_N.pt"
```

영상 없이 평가만 요청한 경우에는 같은 실행기에 `-EvaluationOnly`를 붙인다. video receipt 없이 camera-off full scenario7(128 env × seeds 4201/4202/4203 × 8 case × 20초)만 실행한다.

```powershell
& C:\NCRC\h1_6terrain_video.bat -Path "C:\path\model_N.pt" -EvaluationOnly
```

결과는 checkpoint 옆의 새 `<checkpoint>_h1_evaluation_<timestamp>_<id>` 폴더에 기존 평가 원자료 7개로 저장한다. MP4·영상 ZIP·18파일 통합 ZIP은 생성하지 않으며 `video_evaluation_link.json`의 두 video ZIP 필드는 `null`이다. `-VideoResult`와 함께 사용하지 않는다. 이 옵션의 CPU 회귀 테스트·구문 검사는 통과했으나 새 GPU 실행은 아직 수행하지 않았다.

설치되는 H1 전용 파일은 `h1_6terrain_video.bat/.ps1`이며 공용 evaluator 세 파일과 manifest는 `C:\NCRC\h1-video-evaluator\`에도 동일 bytes로 설치한다. 기존 Go2 파일과 `C:\NCRC\go2-video-evaluator\`는 변경하지 않는다. installer는 differing 기존 파일을 먼저 기존 backup root에 보존하고, Preview에서는 아무 파일도 쓰지 않는다.

## 통합 실행 계약

`h1_6terrain_video.ps1`은 원본 checkpoint SHA-256을 기록하고 ASCII work directory에 동일 bytes를 staging한 뒤 아래 순서로 처리한다.

1. 고정 6지형 영상을 순차 생성·검증한다.
2. 내부 video-only ZIP 10개 항목과 source SHA를 검증한다. 이 중간 ZIP은 `C:\NCRC\h1-video-suite-logs\suite-<id>\video_source.zip`에 보존하고 checkpoint 옆에는 만들지 않는다.
3. 같은 staged checkpoint로 별도 camera-off H1 `scenario7` full evaluation을 실행한다.
4. evaluation 7개 원자료의 completion/protocol/checkpoint identity를 검증한다.
5. full 성공일 때만 영상 10개 + `evaluation/` 7개 + `BUNDLE_README.txt`의 **18개 항목 통합 ZIP 하나**를 checkpoint 옆에 만든다.

원본 checkpoint, 기존 video ZIP, evaluation 폴더와 실패/중단 work는 덮어쓰거나 삭제하지 않는다. smoke/incomplete 자료는 통합 full ZIP으로 포장하지 않는다. A/B comparison은 기본 실행에 포함하지 않는다.

## H1 고정 6영상

- task: `Humanoid-v0`
- num envs: 1
- seed: 42
- headless + cameras
- 1,000 control step / 20초
- `horizontal_scale=0.05`
- terrain: stairs / inverted stairs / boxes / random rough / slope up 10° / slope down 10°
- H1 slope 고정값: `slope_range=[0.176326981,0.176326981]`
- 선택 terrain proportion만 1.0, 나머지 다섯 개는 0.0

영상의 `maneuver_push` 시간표는 Go2 Windows 통합 launcher와 같은 형식을 사용한다: 전진 → +측면 → -측면 → +yaw → -yaw, 전역 4/8/12/16초 world-Y velocity delta ±0.5 m/s. 이는 H1 command range 안의 **PERSONAL 정성 프로토콜**이며 공식 H1 평가 조건이라고 주장하지 않는다. H1의 기존 프로젝트 6지형 영상 규칙과 마찬가지로 slope는 Go2 20°가 아니라 **10°**다.

## H1 scenario7 camera-off full

공용 `eval_core.py::load_suite("h1", "scenario7")`를 그대로 사용한다. 기본값은 128 env, seeds `4201,4202,4203`, 20초 time window다.

| scenario | case |
|---|---|
| H1 balance | flat stationary |
| H2 forward tracking | flat forward |
| H3 lateral tracking | flat lateral |
| H4 rotation tracking | flat forward+yaw |
| H5 rough terrain | random rough |
| H6 slope | 10° up / 10° down |
| H7 push recovery | flat push |

따라서 기본 cohort 수는 `128 × 3 × 8 = 3,072`다. 낙상 뒤 reset으로 episode 수는 cohort 수와 달라질 수 있다. 출력은 `episodes.jsonl`, `evaluation_manifest.json`, `resolved_configs.json`, `video_evaluation_link.json`, `diagnostics.json`, `evaluation.log`, `README.txt`의 7개다.

이 evaluator는 PERSONAL 내부 진단이다. H1 공식 NCRC score, 공개되지 않은 official command/seed/physics 설정, 제출 우위를 재현한다고 주장하지 않는다.

## Full 전용과 비교

별도 eval_smoke 실행기와 통합 `-EvaluationSmoke` 옵션은 제거했다. 같은 checkpoint의 video receipt는 `-VideoResult`로 재사용한 뒤 full 평가를 수행한다. 과거 smoke/incomplete 결과와 실패 로그는 보존하고 full ZIP으로 승격하지 않는다.

A/B 비교는 공용 `compare_policies.ps1`을 명시적으로 요청했을 때만 사용한다.

```powershell
& C:\NCRC\compare_policies.ps1 -Robot h1 -A "C:\eval-A" -B "C:\eval-B"
```

완료된 두 evaluation 폴더는 CPU 비교다. `.pt` 두 개를 넣으면 새 GPU 평가가 시작될 수 있으므로 별도 실행 승인 범위로 취급한다.

## 검증과 한계

H1에도 [교대 검정 프레임 진단 기록](WINDOWS_WORKFLOW.md#교대-검정-프레임-진단-기록-2026-10-15)이 기본 적용된다. 캡처 직후/인코딩 직전의 픽셀 최댓값을 비교하고 `<terrain>.capture_diagnostics.json`을 기존 로그 폴더에 보존한다. 추가 렌더·보정·자동 재시도 없이 경고만 남기며 18파일 통합 ZIP과 평가 조건은 유지한다. 원인 확정이나 GPU 재현 성공을 뜻하지 않는다.

이번 H1 확장은 scorer/collector 계산식이나 task source를 수정하지 않는다. 확인해야 할 회귀 포인트는 H1 launcher가 `Humanoid-v0`, `training/humanoid`, `h1_task`, 10° slope, `--robot h1`을 사용하고 Go2 task 경로를 남기지 않는지, installer가 H1 파일과 bundle을 보존적으로 배포하는지, H1 통합 ZIP이 동일 18-entry 계약을 지키는지다.

실제 H1 GPU full이 성공하기 전에는 다음을 주장하지 않는다.

- H1 Windows GPU compatibility PASS
- H1 3,072 cohort full completion
- H1 A/B score/calibration
- H1 공식 점수와의 상관
- 특정 H1 checkpoint 우위

GPU 검증이 생기면 checkpoint SHA, task/source identity, exit code, protocol ID, cohort/episode 수, wall time, failure diagnostics와 최종 archive SHA를 별도 evidence로 보존한다.
