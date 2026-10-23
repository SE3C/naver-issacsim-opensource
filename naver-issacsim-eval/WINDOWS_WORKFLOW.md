# Windows Go2 PERSONAL 영상·개별 평가

> H1의 같은 형태 Windows 통합 경로는 [WINDOWS_H1_WORKFLOW.md](WINDOWS_H1_WORKFLOW.md)에 분리했다. Go2 2950/7050 기존 검증 기록과 이후 2026-10-07 수신된 H1 `ORIENT-100 / model_2850` **별개 단일 정책 full(3,072 episode)** 증거를 섞지 않는다. H1 paired A/B와 타 checkpoint 검증은 미완료다.

이 저장소는 `C:\NCRC`에서 검증한 Go2·H1 통합 BAT/PS1과 비교 실행기과 evaluator bundle을 보존한다. 학습 코드·checkpoint·driver·패키지는 설치하거나 변경하지 않는다. “6영상 뽑고 평가 돌려줘”는 선택된 native RSL-RL checkpoint의 고정 6영상 ZIP과 별도 camera-off full 평가 요청이다. 비교 보고서는 별도 요청 때만 실행한다.

## 설치와 실행

저장소 루트에서 아래 명령을 실행한다. Preview는 파일·bundle SHA·PS1 구문과 복사 계획만 확인하고 아무것도 설치하거나 GPU를 실행하지 않는다.

```powershell
& .\install_windows.ps1 -Preview
& .\install_windows.ps1 -Destination C:\NCRC
```

설치 대상의 내용이 다르면 `go2-video-suite-backups\install-<guid>`에 먼저 보존한다. 동일한 파일은 그대로 둔다. `windows_bundle_manifest.json`의 세 Python hash를 검사하고 `go2-video-evaluator\bundle_manifest.json`으로 설치한다. `.gitattributes`는 배포 파일의 BOM·개행까지 보존한다. manifest의 upstream/handoff commit은 최초 구현 provenance이며 이 저장소의 현재 HEAD와 같은 값이어야 한다는 뜻은 아니다.

이후 `C:\NCRC\go2_6terrain_video.bat`를 더블클릭하고 native `.pt` 경로를 입력한다. 따옴표·drag/drop을 지원하고 원본과 같은 SHA의 ASCII copy를 Isaac에 넘긴다. 원본 checkpoint와 `exported/model_best.pt`를 교체하지 않는다. 사용자 콘솔에서 Kit 로그를 실시간으로 확인하고 `.pt` 옆에서 최종 영상+평가 통합 ZIP을 받는다. 설치 자체는 영상·평가를 실행하지 않는다.

| 파일 | 역할 |
|---|---|
| `go2_6terrain_video.bat` / `.ps1` | 기본 통합 경로. 6영상 → ZIP 검증 → 별도 full 평가. |
| `compare_policies.bat` / `.ps1` | 명시 요청된 비교. 두 완료 폴더는 CPU; `.pt` 입력은 새 GPU 평가를 시작할 수 있다. |

별도 eval_smoke 실행기와 통합 `-EvaluationSmoke` 옵션은 제거했다. 같은 checkpoint의 receipt를 `-VideoResult`로 주면 영상 재렌더 없이 full 평가한다. 과거 smoke/incomplete evidence는 보존하되 full ZIP으로 포장하지 않는다. `-CompareWith`는 비교를 명시적으로 요청한 경우에만 사용한다.

직접 실행 요청은 지정 checkpoint와 해당 작업의 진단·재시도만 승인한다. 보류되었거나 별도 시작 승인을 요구한 작업은 재개·승인 전에 실행하지 않는다. 문서 편집·설치·Preview는 GPU 실행 승인이 아니다.

## 고정 조건과 보존

영상은 `Quadruped-v0`, 1 env, seed42, headless/cameras, 지형별 1,000 control step·20초다. stairs/inverted stairs/boxes/random rough/slope up20°/slope down20°를 각각 촬영한다. generator rows/cols1·horizontal scale0.05, 선택 proportion1·나머지0, slope range `[0.363970234,0.363970234]`다. `maneuver_push`는 전진 → 양의 횡이동 → 음의 횡이동 → 양/음 yaw 순서이며 전역4/8/12/16초의 worldY 속도 delta로 밀침을 준다. 이 영상 시간표는 episode reset 때 다시 시작하는 평가 명령과 다르다.

평가는 camera-off Go2 `scenario7`, 기본128 env·seeds4201/4202/4203·9 cases·20초다. full 자료는 `episodes.jsonl`, `evaluation_manifest.json`, `resolved_configs.json`, `video_evaluation_link.json`, `diagnostics.json`, `evaluation.log`, `README.txt`로 보존한다. full은 native exit0와 complete/cohort/horizon 검증이 모두 필요하다. 실패 child가 Kit shutdown으로 exit0을 보여도 누락 파일을 성공으로 취급하지 않는다.

내부 영상 ZIP은 `C:\NCRC\go2-video-suite-logs\suite-<id>\video_source.zip`에 보존하며 checkpoint 옆에는 만들지 않는다. 영상 ZIP은 정확히 MP4 6개와 `SHA256SUMS.txt`, `source_checkpoint.txt`, `environment.txt`, `README.txt`를 담는다. native exit0·fresh/nonempty MP4·1,000 frame·ZIP 항목/CRC/SHA와 원본 checkpoint SHA를 검증한다. 치명 오류는 다음 terrain으로 넘기지 않고 로그부터 진단한다. 원본과 기존 evidence는 남기고 실패 작업은 보존한다.

full 완료 후 checkpoint 옆에는 최종 `<checkpoint>_go2_6terrain_evaluation_<timestamp>_<id>.zip` 하나만 새로 만든다. root의 기존 영상 10개 항목에 `evaluation/`의 위 원자료 7개와 `BUNDLE_README.txt`를 더한 정확히 18개 파일이다. MP4·평가 파일 각각의 SHA와 ZIP CRC를 다시 확인하고 최종 ZIP SHA를 콘솔에 출력한다. 평가 summary에 checkpoint/protocol 불일치나 누락·변경 파일이 있으면 통합 ZIP을 만들지 않는다. receipt의 `combined_archive`가 최종 파일을 가리키며 기존 `zip_path`와 link는 변경하지 않아 video receipt 재사용이 유지된다. 이전 영상 ZIP·평가 폴더를 덮어쓰거나 삭제하지 않는다. smoke는 full 분석본이 아니므로 통합 ZIP을 만들지 않는다.

검증 환경: Python3.11.13, torch2.7.0+cu128, tensordict0.9.0, rsl-rl-lib5.0.1, RTX3060 Laptop, IsaacLab `3e73d6dd79080fd7632488c061052a6edd52e230`, task `ef10b7a4c9a83481346d446e8a75aed655f72214`. `WARP_CACHE_PATH=C:\ov\warp-cache`, `OMNI_CONFIG_PATH=C:\ov-config`, `ISAACLAB_PATH=C:\NCRC\IsaacLab`를 유지한다. WSL·driver 교체·패키지 upgrade·학습 실행은 하지 않는다.

## 실제 검증 범위

### 교대 검정 프레임 진단 기록 (2026-10-15)

H1/Go2 실행기는 캡처 직후와 인코딩 직전에 각 프레임의 번호·shape·dtype·최댓값을 기록한다. 추가 렌더, 이미지 복사/보정, 재인코딩 없이 기존 CPU 이미지 배열만 읽으며, 완전 검정은 모든 픽셀 값이 정확히 0인 경우다. 첫 프레임 외 검정·probe 변화·프레임 미추가에는 경고만 출력하고 기존 성공/실패 판정은 바꾸지 않는다.

성공 시 `C:\NCRC\<robot>-video-suite-logs\suite-<id>\<terrain>.capture_diagnostics.json`에 보존한다. 실패 시에는 기존 work 폴더를 확인한다. 진단 파일은 기존 18파일 통합 ZIP 밖에 둔다. `capture_black_indices`와 `pre_encode_black_indices`가 같으면 캡처 직후부터 검정이었고, `changed_probe_indices`는 두 시점의 shape/dtype/max 변화다. 같은 probe가 같은 bytes를 증명하지는 않는다. MP4에만 검정이 있으면 인코딩 경로를 별도로 조사해야 하며, 이 기록만으로 빈 annotator·GPU 동기화·메모리 문제 중 하나를 확정하지 않는다. 자동 재시도나 재발 해결 기능이 아니며 이번 변경의 GPU 검증은 미실시다.

첫 실패 원인은 CUDA 초기화 전 peak-memory reset의 `Invalid device argument`였다. 설치 copy의 `torch.cuda.init()` 선행과 pre-close traceback/FAILED manifest 보존을 이 저장소에도 반영했다. scorer·cohort·checkpoint loading 계약은 바꾸지 않았다. 이전 evaluator checkout은 당시 수정하지 않았으며 이번 Git 동기화에서 검증된 수정만 반영한다.

| 자료 | 2950 | 7050 |
|---|---|---|
| native checkpoint SHA256 | `6b72c530e571f7e9fc826c3917bd6199a22c9b1a2a1028ca7bf981231485992a` | `d40f2666da6063c16c88353163115dcac1a2bd8b98011bf745543737a2188015` |
| full native/BAT exit | 0 / 0 | 0 / 0 |
| cohorts / episodes | 3,456 / 3,488 | 3,456 / 3,458 |
| wall time | 1,721.047초 | 1,749.031초 |

두 full 실행은 기존 검증된 6영상 receipt를 재사용했다. 두 protocol ID는 `806d7e8280d8fac8bbbb6015013b1752335fe0446c8e39bf8f9dd4fbf7c145ad`다. 출력 이름의 `20261004`는 Asia/Seoul(+09:00), 완료 검증 JSON은 2026-10-03 UTC다. 증거 snapshot과 모든 산출물 경로는 분석 저장소의 [Go2 게시·검증 색인](https://github.com/SE3C/naver-issacsim/blob/main/data/processed/operations/windows_go2_video_evaluation/README.md) 및 AI 문서 `21_WINDOWS_GO2_VIDEO_AND_EVALUATION.md`에 있다. Go2 4800의 후속 게시도 이 색인에서 찾으며 이번 초기 2950/7050 검증과 다른 기록이다. H1 기록은 [별도 운영 색인](https://github.com/SE3C/naver-issacsim/blob/main/data/processed/operations/windows_h1_video_evaluation/README.md)에 있다. 색인은 Analysis main에 반영됐으며 원자료·receipt를 변경하지 않는다. MP4/checkpoint/full raw dataset을 이 저장소에 업로드하지 않는다.

기존 12영상과 두 개별 full 자료가 통과한 기록이다. 새 6영상 재렌더+full을 하나의 호출로 다시 실행한 검증, 실제 A/B score/calibration/보고서, **이 문서의 원래 2026-10-04 소스 동기화 당시** H1 GPU 전체 평가는 하지 않았고 CPU 테스트·설치 fixture만 검증했다. **이후 2026-10-07 별도 H1 `model_2850` PERSONAL 단일 정책 full 결과가 확보**됐으나, 이번 소스 동기화 자체에서 새 GPU 테스트를 수행한 것은 아니며 H1 paired comparison도 없다. 정성 영상과 내부 수치 진단은 공식 score·제출 채택 판정이 아니다.
