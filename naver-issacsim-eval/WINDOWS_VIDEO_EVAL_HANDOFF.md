# Windows 영상 담당 에이전트용 evaluator 인계 — 2026-10-03

> 이 문서는 최초 실패 당시의 인계를 보존한 역사 기록이다. 이후 CUDA 초기화·실패 기록 수정과 통합 실행기를 반영했으며 현재 설치 및 실제 Go2 개별 full 검증 범위는 [Windows 실행 지침](WINDOWS_WORKFLOW.md)을 따른다. 아래 미확정 원인·미구현 상태를 현재 상태로 읽지 않는다. 실제 A/B 비교는 후속 실행에서도 수행하지 않았다.

## 최초 인계 당시 상태

- 구현 기준 commit: `9c774a322f2f7d4944444de57f01308987bcb3da`.
- CPU 테스트 45개, Windows 구문/preview, 합성 데이터의 offline 비교 HTML/JSON 생성은 통과했다.
- **실제 Windows evaluator smoke는 실패했다. 전체 7시나리오 평가·실제 A/B 비교·영상 뒤 자동 평가 연결은 검증되지 않았다.** CPU 테스트 통과를 GPU 실행 성공으로 해석하지 않는다.
- 사용자는 기존 영상 에이전트가 만든 6지형 영상 실행의 성공을 확인했다. 그 에이전트의 검증된 실행 기반을 참고하되, 여기서는 원본 영상 스크립트를 변경하지 않았다. 해당 로컬 스크립트는 계속 갱신될 수 있으므로 담당 에이전트가 자신의 성공 버전을 기준으로 삼는다.

## 로컬 경로와 환경

| 역할 | 위치 |
| --- | --- |
| 기존 영상 CLI | `C:\NCRC\go2_6terrain_video.ps1` / `.bat` |
| evaluator checkout | `C:\NCRC\naver-issacsim-eval` |
| smoke CLI | `C:\NCRC\go2_eval_smoke.ps1` / `.bat` |
| 비교 CLI | `C:\NCRC\compare_policies.ps1` / `.bat` |
| IsaacLab | `C:\NCRC\IsaacLab` |
| SDK Python | `C:\NCRC\IsaacLab\_isaac_sim\python.bat` (`C:\isaacsim` 연결) |
| Go2 task | `C:\NCRC\naver-issacsim-nvidia\training\quadruped` |
| H1 task | `C:\NCRC\naver-issacsim-nvidia\training\humanoid` |

관측한 Windows stack은 Isaac Sim 5.1, IsaacLab 0.54.3, RSL-RL 5.0.1, Torch 2.7.0+cu128이며 GPU는 RTX 3060 Laptop 약 6GB다. manifest의 `isaacsim_version`은 `unavailable`로 기록되지만 Kit 로그에는 5.1이 나온다. 설치·버전 교체로 해결하려 하지 말고 성공한 영상 환경과 비교한다.

## 실제 smoke 실패 기록

실행한 명령:

```powershell
& C:\NCRC\go2_eval_smoke.ps1 -Path "$env:USERPROFILE\Downloads\model_2950.pt"
```

- 입력 SHA-256: `6b72c530e571f7e9fc826c3917bd6199a22c9b1a2a1028ca7bf981231485992a`. 같은 실행에서 이미 기록한 값이며 인계 때문에 다시 hash하지 않았다.
- 조건: Go2, native checkpoint, camera-off/headless, 128 env, seed 4201, 첫 case 2초 smoke.
- 결과 경로: `%USERPROFILE%\Downloads\model_2950_go2_eval_smoke_128env_20261003-131151_a308843b`.
- 해당 경로에는 `resolved_configs.json`, `evaluation_manifest.json`만 있고 **`episodes.jsonl`은 없다**.
- manifest는 `execution_status=RUNNING`, `complete=false`, `smoke=true`이며 error 정보가 없다. 이것은 실행 중이라는 현재 상태가 아니라, 종료 후 남은 미완성 기록이다.
- SDK 호출에서는 nonzero exit가 노출되지 않았지만, 바깥 CLI가 결과 파일 누락을 잡아 exit 1로 실패했다. 성공으로 게시하거나 점수를 만들지 않는다.
- Kit 로그: `C:\NCRC\IsaacLab\_isaac_sim\kit\logs\Kit\Isaac-Sim\5.1\kit_20261003_131152.log`. app startup complete 후 close/shutdown이 기록됐다. 확인 시 남은 Kit 프로세스는 없었다.
- **실패 원인은 아직 확정하지 않았다.** VRAM 부족, checkpoint 손상, RSL load 실패, viewport 경고 중 어느 하나를 원인으로 단정할 근거는 없다. 최초의 "출력 없음" 메시지와 달리 manifest/config는 실제로 생성돼 있었다.

조사할 좁은 구간: `isaac_runner.py`의 `_run()`에서 RUNNING manifest를 쓴 뒤 episode 파일을 열기 전까지. CUDA peak-memory reset과 그 뒤 초기화가 이 구간에 있다. 현재 FAILED/error를 기록하는 try는 cohort 실행 안쪽이며, `main()`은 finally에서 `simulation_app.close()`를 호출한다. **이 구간의 실제 예외를 close 전에 확인·보존하는 것부터** 진행한다. 위 호출 구조는 조사 단서이지 확정 원인이 아니다.

## 사용자가 원하는 최종 흐름

```text
선택 checkpoint A → 기존 6영상 완료 → 별도 camera-off 7시나리오 평가 → A 평가자료
선택 checkpoint B → 기존 6영상 완료 → 별도 camera-off 7시나리오 평가 → B 평가자료
                                                                  ↓
                                               저장된 A/B 자료의 CPU 비교 리포트
```

- 재사용 대상은 성공한 Python/Isaac 시작, task·checkpoint 로딩 및 native 환경 처리 방식이다. **6영상 loop를 7시나리오 평가라고 재사용하거나 MP4에서 정확한 수치를 추정하지 않는다.** 영상과 수치 평가의 case/command 설정은 분리한다.
- 영상 프로세스가 정상 종료한 뒤 평가를 순차 실행한다. 동시 GPU 프로세스, 새 daemon, 원본 영상 루프의 대규모 재작성은 필요 없다.
- 영상과 평가가 동일한 사용자가 선택한 checkpoint를 쓰도록 연결한다. 자동 best 선택·policy 교체·재학습은 하지 않는다.
- 기존 6영상은 환경 1개/영상 1,000프레임이다. Go2 `scenario7`은 7시나리오지만 slope/stairs 양방향으로 **9개 case**이며, 기본 128 env × 3 seed = 정책당 3,456개 환경·조건 조합을 각 20초 평가한다. 실제 episode 수는 낙상/reset에 따라 더 많을 수 있다.
- 렌더링은 영상 쪽, 병렬 physics/inference는 평가 쪽 부담이다. 영상 성공만으로 128 env 평가나 wall time을 보장하지 않는다. 우선 smoke를 해결하고 측정한다.
- H1은 별도 task·가중치·±10° 경사, Go2는 ±20°다. 현재 Go2 영상 성공을 H1 통합 성공으로 주장하지 않는다.

## 그대로 재사용할 evaluator 계약

- [isaac_runner.py](isaac_runner.py): 수집·종료/reset 처리·환경/정책 provenance. task source나 optimizer loading을 새로 구현하지 않는다.
- [eval_core.py](eval_core.py): `validate_dataset`, `calibrate`, `score_policy`, `compare_policies`, `report_html`.
- [SCORING_SPEC.md](SCORING_SPEC.md): 점수 산정식·진단 지표·bootstrap·해석 한계. 총 reward나 영상 인상점을 공식 점수처럼 끼워 넣지 않는다.
- [compare_cli.py](compare_cli.py): 두 완료된 평가 폴더를 받으면 GPU 재실행 없이 비교한다.
- [tests/test_eval.py](tests/test_eval.py), [tests/test_runner.py](tests/test_runner.py), [tests/test_compare_cli.py](tests/test_compare_cli.py): 기존 회귀 계약.

native checkpoint는 `--checkpoint`, exported TorchScript는 `--policy`다. `.pt` 확장자만으로 둘을 추측하지 않는다. 비교 CLI는 혼합 형식을 거부한다. 최신 RSL-RL은 actor/critic config를 요구하므로 `_prepare_agent_cfg()`가 IsaacLab native play와 같은 공개 `handle_deprecated_rsl_rl_cfg`를 재사용한다. 원본 task config를 고치거나 임의 state-dict 변환을 추가하지 않는다. 실제 checkpoint inference 성공은 아직 확인되지 않았다.

`isaaclab.bat -p`의 기존 Windows 실행 분기는 끝에서 `exit /b 0`을 반환할 수 있어 오류 exit를 믿을 수 없다. 새 CLI는 SDK `python.bat`을 직접 사용하고 결과 파일/manifest도 확인한다. 이번 smoke처럼 exit만으로 성공 판단하지 않는다.

평가 자료는 최소 `episodes.jsonl` + `evaluation_manifest.json` + `resolved_configs.json`이다. full 평가에서는 `execution_status=COMPLETE`, `complete=true`, 모든 cohort/horizon 검증이 필요하다. smoke는 성공해도 `complete=false`이며 점수를 만들지 않는다.

## 개별 평가지와 A/B 점수 기준

A/B는 같은 suite·seed·env 수·device·source/runtime/config 프로토콜로 평가한다. 결과를 재사용할 때는 두 디렉터리의 `protocol_id`가 같아야 한다.

개별 점수를 각각 자체 calibration으로 계산한 뒤 서로 비교하지 않는다. 이미 정한 공통 calibration이 있으면 양쪽에 똑같이 적용한다. 아직 없다면 먼저 raw 평가자료/진단을 남기고, 비교 시 B를 기준으로 provisional calibration을 생성해 A/B 양쪽에 적용한다. 이 경우 B를 바꾸거나 A/B를 뒤집으면 척도도 바뀌므로 여러 쌍의 전체 순위를 만들지 않는다. 개별 HTML 점수도 이 공통 기준을 정한 뒤 생성한다.

저장된 평가자료 비교 예시(일반 Python, GPU 없음):

```powershell
py -3 C:\NCRC\naver-issacsim-eval\compare_cli.py --robot go2 `
  --a "C:\results\policy-A-evaluation" --b "C:\results\policy-B-evaluation"
```

새 출력 디렉터리에 `calibration.json`, `comparison.json`, `comparison.html`을 남긴다. 내부 점수·CI는 공식 채점 결과가 아니며 자동 제출/채택을 하지 않는다.

## 다음 담당자의 완료 기준과 경계

1. 실제 smoke 예외를 확정하고 최소 범위 수정한다. 실패 자료·원본 checkpoint·성공한 영상 코드는 보존한다.
2. 명시적으로 허용된 짧은 실제 smoke에서 episode 출력 및 COMPLETE/smoke 상태를 확인한다.
3. 6영상 성공 뒤 7시나리오 평가를 연결하되, 영상 성공과 평가 성공을 따로 표시하고 실패하면 후속 평가/리포트를 중단한다.
4. full 평가의 cohort 검증과 저장된 A/B 자료 비교를 확인한다. mock/합성 데이터 통과를 실제 GPU 통과로 보고하지 않는다.

PERSONAL용 작업이다. 공식 서버·공식 train/play/finalize·reward 값은 수정하지 않는다. 학습·게시·삭제·서버 종료를 자동 후처리로 추가하지 않으며, 실제 GPU 재실행은 담당 작업의 사용자 승인 범위에서만 한다. 실패한 output을 삭제하거나 재사용해 덮어쓰지 않는다.
