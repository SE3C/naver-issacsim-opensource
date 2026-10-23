---
title: "개인 NVIDIA 서버 운영 판단"
purpose: "AI upload bundle — 개인 검증 환경을 규정에 맞게 사용하는 방법"
sources:
  - "data/processed/incoming/other/reviewed/GO2_A1_1K_3K_VIDEO_FULL_EVIDENCE_ANALYSIS_20260914.md"
  - 'data/processed/incoming/other/reviewed/GO2_OFFICIAL_BASELINE_1K_AND_ISSACSIMZ_LOGGING_ANALYSIS_20260914.md'
  - "data/processed/server_backup/reports/"
  - "data/processed/planning/historical/04_OPTUNA_REWARD_SEARCH_DESIGN.md"
  - "data/processed/planning/historical/07_H1_SECOND_RUN_PARAMETER_COMPARISON_PLAN.md"
  - "data/processed/experiments/h1/training/2026-08-24_OFFICIAL_SERVER_300ITER_BASELINE.md"
  - "data/processed/experiments/h1/analysis/2026-09-07_BREV_L40S_H1_BASELINE_5K_AND_SCREENING.md"
  - "data/processed/incoming/other/reviewed/GO2_G5_OFFICIAL_1K_LIGHTWEIGHT_FAILURE_ANALYSIS_20260914.md"
  - "data/processed/incoming/other/reviewed/GO2_A1_THREE_EXPORTS_DEEP_ANALYSIS_20260914.md"
  - "data/processed/incoming/other/reviewed/GO2_A1_MODEL_4300_DEEP_ANALYSIS_20260915.md"
  - "data/processed/incoming/other/reviewed/GO2_A1_MODEL_4800_DEEP_ANALYSIS_20260915.md"
  - "data/processed/incoming/other/reviewed/GO2_A1_MODEL_4900_DEEP_ANALYSIS_20260915.md"
  - "data/processed/experiments/go2/analysis/2026-09-15_GO2_G-005_FIXED_EVAL_SEED4201_D1.md"
  - "data/processed/experiments/go2/analysis/2026-09-15_GO2_G-005_4800_4900_NATIVE_VIDEO_AND_SELECTION.md"
  - "data/processed/incoming/other/reviewed/A1_4800_vs_4900_DEEP_ANALYSIS_AND_LEARNING_RECORD_20260915.md"
  - "data/processed/incoming/other/reviewed/NCRC_20260913_MASTER_TRACKING_REPORT.md"
  - "data/processed/external_analysis/video_reports/03_100_hour_workflow_hGbBn5xliyg.md"
  - "data/processed/external_analysis/video_reports/04_isaac_sim_server_usage_sJi7hHWOTLU.md"
  - "data/processed/external_analysis/video_reports/07_compliance_and_prohibited_actions_VQE9DPn4KAg.md"
  - "https://isaac-sim.github.io/IsaacLab/main/source/tutorials/00_sim/launch_app.html"
  - "https://docs.isaacsim.omniverse.nvidia.com/latest/reference_material/sim_performance_optimization_handbook.html"
type: "recommendation"
---

# 개인 NVIDIA 서버 운영 판단

## Windows 로컬 Go2/H1 실행은 별도 경로

이 PC의 PERSONAL “6영상 뽑고 평가 돌려줘”는 [21](21_WINDOWS_GO2_VIDEO_AND_EVALUATION.md)의 robot별 진입점을 뜻한다: Go2는 `C:\NCRC\go2_6terrain_video.bat`, H1은 `C:\NCRC\h1_6terrain_video.bat`다. checkpoint 입력 한 번으로 고정 지형별 20초 영상 6개를 만들고, 렌더 프로세스 종료 뒤 camera-off 개별 `scenario7` 평가와 최종 통합 ZIP을 생성한다. 실제 RTX 3060 Laptop GPU에서 Go2 2950·7050 full 평가를 각각 약 28분 41초·29분 9초에 완료했고, 이는 학습 시간이나 다른 GPU의 보장 시간이 아니다. 기존 영상 ZIP을 재사용한 당시 Go2 full 검증에서는 영상을 다시 렌더링하지 않았다.

GPU 실행은 명시적으로 승인된 범위에서만 한다. 문서 작업은 GPU 실행을 승인하지 않으며, 사용자가 게임 중이거나 실행을 보류했다면 재승인 전에는 시작하지 않는다. 원본 checkpoint를 보존하고 ASCII staging·`WARP_CACHE_PATH=C:\ov\warp-cache`·고정 패키지 버전을 유지한다. stdout/stderr는 콘솔에 실시간 표시하고 실패 자료를 남긴다. H1은 `h1_6terrain_video.bat`에서 ±10° 6영상과 8 case full 평가를 수행한다. 중간 영상 ZIP은 내부 로그 폴더에, 최종 통합 ZIP은 checkpoint 옆에 보존한다. 독립 `go2_eval_smoke`와 `-EvaluationSmoke`는 2026-10-06 제거된 역사 경로다. `compare_policies`의 별도 runner·경로와 receipt 조건은 `21`을 따른다. 기본 범위는 각 checkpoint의 영상·개별 평가이며 A/B 비교는 사용자 담당이다.

## 역할과 금지선

### 새 공식 서버의 출발점과 목표 설정

새로 제공된 OFFICIAL 서버는 **운영진 baseline reward**에서 시작한다. `h1-submit-2` 같은 frozen submission preset은 비교·재현 기준이며 서버에 이미 적용된 초기값이 아니다. Codeberg clone/pull·bootstrap·doctor·checkpoint import도 preset reward를 자동 적용하는 단계가 아니다. 기존 서버 재접속·재부팅은 reward 초기화를 뜻하지 않는다.

실행 안내는 **현재 reward 전체 확인 → 목표 resolved config와 차이 계산 → 필요한 모든 활성 weight 변경 → 실제값 재확인 → preflight → tmux** 순서를 따른다. `fresh`는 checkpoint 없이 학습한다는 뜻일 뿐 reward가 baseline 또는 preset이라는 뜻이 아니다. resume도 현재 reward 파일을 확인하며 부모 checkpoint에서 reward가 자동 복원된다고 가정하지 않는다. 구체적인 예시는 `19`를 따른다.

개인 NVIDIA 서버는 보상 가설의 사전 학습·비교, 공식 서버 정책의 관찰·재생, 평가 harness와 로그·영상 분석에 사용한다. **개인 서버에서 새로 학습한 정책은 공식 제출물로 쓰지 않는다.** 제공 GPU 서버에는 외부 에이전트·MCP·임의 패키지를 설치하지 않는다.

## 권장 구성

```text
공식 서버: reward 수정 · 학습 · 제출 산출물 생성
        ↓ 산출물 다운로드
개인 서버: play/검증 · 반복 평가 · 영상/로그 · 후보 비교
        ↓ 판단만 반영
공식 서버: 다음 reward 실험 또는 제출
```

## 실행 전후 experiment registry 갱신

실험의 판단·계보는 [`research/EXPERIMENTS.md`](../../../research/EXPERIMENTS.md)와
`research/experiments/<robot>/`의 가설 파일에 남긴다. 원본 evidence, policy, checkpoint,
TensorBoard, video는 이 registry로 복사하거나 이동하지 않고 Originals에 둔다.

실행 전에는 기존 가설의 다음 Run인지, 부모 대비 새 reward 질문인 새 가설인지 먼저 정한다.
Run에는 environment (`PERSONAL` 또는 `OFFICIAL`), iteration, seed, 상태, artifact 위치와
decision을 기록한다. 공식 서버에서 실제 학습했고 식별 가능한 evidence가 있을 때만 Run을
`OFFICIAL`로 표시한다. 개인 서버의 수치·영상은 다음 실험 선택과 도구 검증에 쓰되, 공식
대회 성능 또는 제출 근거로 승격하지 않는다.

공식 실행이 끝나면 archive와 export가 보존된 것을 확인한 뒤 해당 Run을 갱신한다. 실패·중단도
evidence archive가 남으면 동일하게 기록하며, 결과 파일을 지우거나 registry를 위해 재배치하지 않는다.

공식 legacy `G-004 ANG-STAB` fresh 1K(아주 오래된 alias G5)는 이 구분의 사례다. 정식 보존한 train archive의 내부 checksum 33/33과
validation·finalize·official backup PASS를 직접 확인했지만, terrain `0.00`, XY error `1.7363`과
비정상 자세 영상 때문에 정책은 strong negative다. 파이프라인 성공과 정책 성공을 분리해 기록하고,
높은 timeout·긴 episode만으로 서버 실행을 연장하지 않는다. 받은 loose MP4는 정상 재생 가능한
최종 산출물이지만 별도 video evidence archive가 아니므로 train provenance와 같은 수준으로
과장하지 않는다.

## 공식 서버의 확인된 작업 순서

서버 사용 안내 영상에서 확인되는 기본 흐름은 다음과 같다. 버튼명과 UI는 바뀔 수 있으므로 현재 대시보드를 우선한다.

```text
팀 대시보드에서 서버 시작
→ 사용 가능 상태까지 대기
→ 브라우저 code-server 열기
→ reward·명령·로그 위치 확인
→ 학습 또는 필수 검증 실행
→ 결과 파일과 로그 확인·다운로드
→ OFFICIAL 서버 종료는 사용자가 직접 처리(AI는 명시적 요청을 받아도 실행하지 않음); PERSONAL 서버는 명시적 요청이 있을 때만 AI가 종료 가능
```

서버가 꺼진 상태에서 편집기 버튼이 비활성인 것은 영상상 정상 흐름이다. 데모에 나온 서버 주소·사용시간·학습시간은 현재 팀의 값으로 사용하지 않는다.

OT 운영 습관: 예선 100시간은 팀 합산이며 한 시점에 한 명만 접속한다. 유휴 자동 종료가 있을 수 있으나, 학습 실행 중인지의 세부 판정은 영상만으로 확정하지 않는다. 재시작·초기화에 대비해 산출물과 실험 기록을 개인 작업공간에 받는다. OFFICIAL 서버 종료는 사용자 본인이 처리하고 AI는 명시적 요청을 받아도 실행하지 않는다. 서버에서 문서 작업·대규모 분석을 오래 하지 않는다.

## 2026-08-24 H1 실측과 남은 증거

H1 baseline 300회 실행은 report 기준 end-to-end 4분이었다. 따라서 확인된 전체 평균은 0.80초/iteration이지만 여기에는 초기화·checkpoint·finalize·export가 포함된다. 콘솔 전체 로그가 없어 원래 분석에 적힌 코어 0.69~0.71초는 재검증할 수 없으며, 5k·10k·25k 시간을 이 값으로 확정하지 않는다.

이 2026-08-24 실행에서는 policy·checkpoint·env·report·ONNX·MP4는 보존됐지만 전체 콘솔, TensorBoard event, `nvidia-smi`, GPU 시계열, 코드 hash가 빠졌다. **당시 후속 재실행 권고는 새 reward보다 진단 증거를 먼저 완성하는 것이었다.** 이후 evidence 절차는 `19`로 정비됐다. 2026-10-06 ORIENT-100은 OFFICIAL fresh 3K COMPLETE/PASS이고, 후속 2026-10-07 `model_2850` Windows PERSONAL 단일 정책 6영상/full 분석은 **HOLD**다([원문](../incoming/other/reviewed/H1_ORIENT-100_POLICY_ANALYSIS_20261007.md), `14`). H1 8 case × 3 seed × 128 env = 3,072 episode full이 완료됐으나 동일 `h1-submit-2` 대조·reward 인과·OFFICIAL 점수는 미확인이다. ACTRATE-001도 독립 OFFICIAL fresh3K 완료/PASS·PERSONAL model2850 분석 수납/HOLD다. 두 설정은 frozen `h1-submit-2` 대비 독립 single delta이며 서로의 checkpoint를 상속하지 않는다. 이 역사적 실행의 권고를 현재 우선순위로 사용하지 않는다.

## 공식 서버 호스트 (`h1-submit-2 / TERM-50` 5K 로그; legacy H-001 R02)

originals `2026-09-08_232333_term50_5k/README.md`에 기록된 공식 학습 호스트다.

- OS: Ubuntu 24.04.2 LTS, kernel 6.8.0-136-generic
- GPU: NVIDIA GeForce RTX 5080 16,303 MB
- driver: 580.126.09
- CPU: Intel Core Ultra 5 250KF Plus 18 cores, RAM 64,006 MB
- Isaac Sim: `5.1.0-rc.19+release.26219.9c81211b.gl` (`/isaac-sim`)
- Isaac Lab: commit `3e73d6dd79080fd7632488c061052a6edd52e230`, `/workspace/IsaacLab`
- H1 코드: `/workspace/training/humanoid`

이 조합을 개인 L40S와 같다고 부르지 않는다.

## 검증된 Brev L40S RC19 환경

2026-09-07 H1 5K를 정상 완료한 **개인** 서버 조합은 Ubuntu 22.04, L40S 46GB, driver 580.126.09, Isaac Sim `5.1.0-rc.19`, Isaac Lab `2.3.2` commit `3e73d6dd...`, Python 3.11.13, PyTorch 2.7.0+cu128이다. 영상 실행에 `libglu1-mesa`가 필요했다. 드라이버 버전은 공식 `TERM-50` 호스트와 같다. OS 메이저 버전과 GPU는 다르다.

개인 NVIDIA 환경의 실행 checkout은 `naver-issacsim-nvidia`의 `training/`이며, `scripts/prepare_brev_rc19.sh`는 personal setup 진입점이다. 새 학습의 실행·evidence 보존은 별도 공개 `issacsimz`가 담당한다. 설치·학습·GitHub 업로드를 하나의 setup script에 묶지 않으며, `train.py`·`_finalize.py`는 sidecar가 수정하지 않는다. 코드 자체의 최상위 기준은 바로 다음 문단의 최신 공식 snapshot이다.

### 개인 서버 checkout 사전 조건

개인 NVIDIA/Brev 서버의 표준 작업에는 두 checkout이 필요하다. **Brev의 기본 home/base는 `/home/shadeform`이지만, 현재 NVIDIA README의 새 VM 예시는 checkout을 `/ephemeral` 아래에 둔다.** 이 둘을 같은 개념으로 보지 않는다. `/home/shadeform`은 사용자 home·IsaacLab·download/evidence 기준 경로에 쓰일 수 있고, `/ephemeral`은 현재 README가 제시하는 checkout 기본 예시다. 실제 명령 전에는 서버에서 두 checkout과 task root의 존재·현재 위치·bootstrap state를 직접 확인한다.

**Brev Setup Script 실행 완료나 서버 부팅은 기본 Isaac Sim/Lab 환경 준비이지, 두 checkout 준비 또는 `issacsimz` personal bootstrap 완료가 아니다.** 새 서버에서 현재 README 기본을 따를 때 공개 `issacsimz`를 `/ephemeral` 아래에 clone하고, 재접속이면 추측한 경로가 아니라 실제 checkout 존재를 확인한 뒤 그 checkout을 `pull --ff-only`한다. 그 checkout에서 personal bootstrap을 실행하면 GitHub 인증 상태를 확인한 뒤 비공개 `naver-issacsim-nvidia`를 clone하거나 `pull --ff-only`한다. bootstrap은 Release의 annotated tag 생성에 필요한 Git 작성자 정보를 이 개인 NVIDIA checkout에만 설정하며, 이메일은 `ncrcissacsimz@users.noreply.github.com`이다. global Git 설정이나 official 환경은 변경하지 않는다. pull이 미커밋 변경 때문에 실패하면 원본 변경을 버리지 말고 보고한다.

```text
/home/shadeform/                    # Brev 기본 home/base
/ephemeral/naver-issacsim-nvidia/   # 현재 NVIDIA README의 새-VM checkout 기본 예시
/ephemeral/issacsimz/               # 현재 README의 sidecar checkout 기본 예시
```

`naver-issacsim-nvidia` checkout의 `training/`이 H1·Go2 task root이고, `issacsimz` checkout에서 `bash scripts/bootstrap_server.sh --mode personal`과 mode-aware wrapper를 실행한다. bootstrap의 GitHub 로그인은 필요한 경우에만 시작하며 `READY` 이전에는 학습하지 않는다. 이 절차의 명령과 첫 접속·재접속 구분은 NVIDIA 저장소 README가 기준이다. sidecar는 공식 `train.py`·`play.py`·`_finalize.py`를 수정하지 않는다. official은 운영진의 `/workspace/training/`을 그대로 사용한다.

AI가 사용자에게 복사·실행 명령을 줄 때는 `19`의 **서버용 복사·실행 카드**를 먼저 적용한다. 개인 첫 접속과 재접속의 sidecar clone/pull, bootstrap의 인증·private checkout·doctor·`READY`를 빠뜨리지 않는다. official 첫 접속에는 `/workspace`에서 공개 Codeberg `issacsimz`를 clone하고, 재접속에는 기존 checkout을 확인한 뒤 Codeberg에서 `pull --ff-only`한다. 그다음 official bootstrap을 실행하며 운영진 제공 `/workspace/training/`을 사용한다. official에서는 GitHub clone·pull·push·인증·API·Release 등 GitHub와의 상호작용을 하지 않는다. 학습 후에는 evidence와 결과를 먼저 판정하고, 유망한 정책의 영상 필요성과 선택 checkpoint를 설명한 뒤 [17의 영상 실행 절차](17_ISSACSIMZ_VIDEO_OPERATIONS.md)에서 해당 mode의 명령을 제시한다. OFFICIAL에서 6영상 요청을 PERSONAL 서버로 돌리라고 거절하지 않는다. PERSONAL 자동 suite 스크립트 대신 공식 `play.py`의 지형별 직접 실행을 안내하며, 임의 server stop은 넣지 않는다.

2026-09-13 19:59:15에 공식 서버 `/workspace/training`에서 직접 만든 `NCRC_OFFICIAL_TRAINING_20260913_195915.tar.gz`가 현재 source of truth다. SHA-256은 `2c1326e0b58e9c860e32db81f110d2c0de16fac113de4424144b73e39fe01d15`이며, canonical archive와 extracted training은 `naver-issacsim-originals` commit `4ebdaef`, 개인 NVIDIA의 `training/` 동기본은 commit `428a61d`에 있다. 따라서 새 개인 실행은 NVIDIA의 최신 `training/`을 사용하고, 공식 실행은 운영진이 제공한 `/workspace/training/`을 그대로 사용한다. 이전 1K/TERM-50 hash 비교는 당시 실행 provenance로만 해석하며 현재 코드와의 parity 판정에는 쓰지 않는다.

학습 시작·재개의 고정 절차는 [19번](19_ISSACSIMZ_EXTERNAL_EVIDENCE_CLI.md)의 **「OFFICIAL 학습 시작·재개 표준 절차」**다. H1·Go2 모두 preflight 뒤 같은 인자의 tmux wrapper를 쓰며, 부모 evidence가 있으면 indexed resume, 단일 native `.pt`만 있으면 `--import-checkpoint`를 선택한다. import 부모 출처는 unknown이며 제출 계보 증명으로 취급하지 않는다. raw native tmux 명령으로 우회하지 않는다.

### Python/IsaacLab 호출 규칙

AI는 공식 서버에서 `python3 train.py` 또는 `python3 play.py`를 직접 실행하지 않는다. `bash scripts/bootstrap_server.sh --mode official`로 경로와 runner를 먼저 검증한 뒤, 학습은 `./scripts/issacsimz_tmux_train.sh` 또는 `./scripts/issacsimz_train.sh`, 일반 영상은 `./scripts/issacsimz_video.sh`를 사용한다. 다만 **OFFICIAL 6지형 수동 영상**은 [17의 공식 native `play.py` 6회 절차](17_ISSACSIMZ_VIDEO_OPERATIONS.md)에 따라 `/workspace/IsaacLab/isaaclab.sh -p play.py`를 지형별로 실행한다. bootstrap state는 선택 mode의 `ISSACSIMZ_H1_ROOT`·`ISSACSIMZ_GO2_ROOT`·`ISSACSIMZ_ISAACLAB_ROOT`를 공통으로 기록·export하므로 bootstrap 후 `./issacsimz doctor --robot h1|go2`에 task root를 반복 지정하지 않는다. sidecar shell entrypoint는 `ISSACSIMZ_PYTHON_RUNNER`가 있으면 그것을 엄격히 사용하고, 없으면 `python3`, 그마저 없으면 IsaacLab/Isaac Sim `python.sh`를 찾는다. 이 선택은 sidecar interpreter용이다. 실제 native child는 `isaaclab.sh -p /workspace/training/<task>/train.py|play.py`로 실행되므로 AI가 임의의 Python 경로로 바꾸지 않는다.

기존 H1 `organizer_keep_ckpt_h1_verbatim.sh`는 운영진 제공 `keep_ckpt.sh` **본문**을 보존한 역사적 수동 절차다. `WANT="2000 5000 8000"` 원문은 수정하지 않았고 현재 자동 keep-all 경로와 함께 실행하지 않는다. official에서 범용 `checkpoints/` mirror·`watcher.log`·`nvidia_smi_during.csv`가 없는 것은 정상이다.

2026-09-26 받은 [시리우스_열무 질의·운영진 답변 전사본](../incoming/other/reviewed/2026-09-26_H1_ORGANIZER_CHECKPOINT_QA_SIRIUS_YEOLMU.md)의 공개 keep-all 방식에 따라 `issacsimz`는 official H1/Go2 profile train에서 별도 `organizer_keep_all_ckpt.sh`를 자동 시작한다. 현재 native run의 `model_*.pt`를 학습 중 `backup_log/<native-run>/`에 복사하고 종료 후 evidence의 `organizer_checkpoints/`로 수집해 자동 `.tar.gz`에 넣는다. 이 스크립트는 run·PID 선택을 sidecar에 맞춘 **파생본**이지 전사본/운영진 원문 그대로가 아니다. 전사본의 줄바꿈이 합쳐진 셸 블록을 실행하지 않는다. 실제 보존 수량·누락 회차는 run마다 확인하며, 범용 watcher·GPU sampler는 여전히 꺼져 있다.

같은 답변이 허용한 native `agent.save_interval=50`은 `issacsimz`가 PERSONAL·OFFICIAL profile train 명령에 자동 전달한다. 사용자가 official `--extra`로 직접 넣을 필요는 없고 임의 `--extra` 차단은 유지한다. 저장 주기 변경과 checkpoint 보존은 별개이므로 위 keep-all 절차도 함께 사용한다. 공식 `train.py`·`_finalize.py` 수정 금지는 그대로다.

로컬 fixture는 명령에 `agent.save_interval=50`이 붙는 것과 `model_100.pt`·`model_200.pt`의 보존·압축을 검증했다. 이후 OFFICIAL Go2 `LINTRACK-125` fresh 3K/7.5K evidence에서 50-step 저장이 실제로 확인됐다: 3K는 `model_0.pt`~`model_2950.pt` 60개, 7.5K는 `model_0.pt`~`model_7450.pt` 150개다. 따라서 공식 서버 native 50회 저장 자체는 실측 완료다. 새 Run에서는 여전히 native checkpoint 회차와 `organizer_checkpoint_count`, evidence archive 내용을 실행별로 확인한다.

충분히 긴 **resume** official run에서는 보존된 final numbered checkpoint를 기본 제출 후보로 둔다. 현재 native finalizer의 자동 best는 관측 step 범위에서 `warmup = lo + max(50, floor((hi-lo)×0.10))`을 계산하고 **`step >= warmup`**만 후보로 삼는다. 따라서 2998→4997이면 3197은 포함되고 3197 미만만 제외된다. 이 규칙은 초반 curriculum 재적응 spike를 피하는 자동 reward selector일 뿐 제출 정책 selector는 아니다. 마지막 수백 iteration에서 terrain·tracking·낙상이 함께 명확히 악화된 경우만 직전 checkpoint를 검토한다. 운영진의 새 답변은 **보존된 다른 checkpoint를 비교 근거로 선택해 native `exported/model_best.pt` 자리에 넣고 `play.py`로 `policy.pt`를 만드는 것 자체는 허용**하며, 학습 기록과 대조할 수 있도록 선택 회차·이유를 제출 코멘트에 적으라고 한다. 이는 우리 final 기본값을 폐기하거나 PC checkpoint tournament를 자동화하라는 지시가 아니다. 기존 exported 자동 선정본과 선택본의 identity를 분리 보존하고, `issacsimz` official provenance/evidence 경로와 native 수동 교체 절차를 혼동하지 않는다. 현재 sidecar 정상 경로에서는 verified official train evidence를 `--from-run`으로 지정해 final checkpoint에서 native play/export를 **한 번만** 실행해 handoff를 다운로드한다. OFFICIAL 서버 종료는 사용자 본인이 처리하며 AI는 실행하지 않는다. 별도 6지형 정성 영상은 공식 `play.py` 수동 6회 절차로 만들 수 있다(`17`); PERSONAL 자동 suite 스크립트만 OFFICIAL에서 사용할 수 없다.

현재 sidecar 안전 기준은 evidence를 archive하기 전에 완전히 finalize하고, tar 생성 뒤 evidence directory의 `metadata.json`·`SHA256SUMS`를 다시 쓰지 않는 것이다. pack 시간·크기는 `<archive>.metadata.json`에만 기록하며 download handoff에도 archive·`.sha256`·`.metadata.json`을 함께 복사한다. validation `PASS`와 `WARN`은 기존 loose handoff 정책을 유지하지만, `FAIL`은 실패 evidence directory와 archive만 보존하고 `model_best.pt`·`env.yaml`·`report.html` 같은 제출형 loose artifact는 배포하지 않는다.

official에서는 사용자가 지정한 `--collect`를 train/play/video 시작 전에 거부한다. 내부 표준 수집인 native run·TensorBoard·`exported/`는 그대로 유지한다. 종료 후 checkpoint index는 symlink, 빈 파일, regular file이 아닌 대상, 승인된 native run 또는 `backup_log` 밖으로 resolve되는 경로를 official provenance로 인정하지 않는다. source identity는 필수 profile 파일뿐 아니라 task root 아래 전체 `.py`를 fingerprint하며 `logs/`, `exported/`, `__pycache__/`, `.git/`, evidence/download·backup 같은 동적 경로는 제외하고 실제 hash 대상 목록을 manifest에 남긴다.

portable source 검사는 `.git`이 있으면 `git ls-files`를 쓰고, ZIP처럼 `.git`이 없으면 동일한 공개-tree 금지어 검사를 filesystem walk로 수행한다. `.git` 없는 archive 복사본에서도 전체 테스트, `py_compile`, `zipapp` build가 통과해야 배포 가능한 source로 본다.

`scripts/prepare_brev_rc19.sh`는 예전 clone 후 설치 경로로 남아 있다. 같은 VM의 완료 marker 또는 실제 persistent volume만 재사용하며, 삭제되는 인스턴스의 로컬 cache를 영구 보존으로 착각하지 않는다.

과거 5K wrapper의 checkpoint·영상 흐름은 historical reproduction 기록이다. 새 personal 실행은 `issacsimz`의 checkpoint mirror/evidence/archive를 사용하고, personal mode에서만 선택적으로 GitHub Release를 올린다. 5K의 zero-based 최종 파일은 `model_4999.pt`일 수 있다. 인스턴스 stop/delete는 자동화하지 않는다.

## Export·다운로드·영상 결과 확인

사용자가 export를 요청하면 policy만이 아니라 원본 native `logs/<run>/`, TensorBoard event, 콘솔·exit code, 설정·reward, 중간/final checkpoint, `exported/`, report와 영상의 보존 여부를 확인한다. 원본 run 구조는 유지하고, 제출·다운로드용 복사본과 구분한다. event에 없는 값은 추정하지 않는다. OFFICIAL 서버는 AI가 종료하지 않으며, PERSONAL 서버는 사용자가 별도로 명시한 경우에만 종료한다. 세부 수집·판정은 [16](16_EXPERIMENT_EXPORT_AND_TENSORBOARD.md), train·evidence 실행은 [19](19_ISSACSIMZ_EXTERNAL_EVIDENCE_CLI.md), 영상 실행은 [17](17_ISSACSIMZ_VIDEO_OPERATIONS.md)을 따른다.

`issacsimz`의 native 실행 성공 여부(`execution`)와 evidence 무결성(`evidence_validation`)은 별개다. video는 실제 source checkpoint·SHA와 새 MP4 SHA를 연결하고, 새롭거나 수정된 non-empty `exported/play_video.mp4`를 확인한다. `policy.pt`는 video 성공 조건이 아니다. official policy 승격은 검증된 official train 계보에만 허용된다. canonical task tree의 기존 export를 덮어쓰지 않는 격리 staging·승격 절차와 `--from-run`/checkpoint 제한은 [19](19_ISSACSIMZ_EXTERNAL_EVIDENCE_CLI.md)의 현재 규칙을 적용한다. OFFICIAL numbered checkpoint 재생 명령을 만들기 전에는 [17의 preflight](17_ISSACSIMZ_VIDEO_OPERATIONS.md)대로 실제 evidence root와 index의 `source_path`·SHA를 확인한다. `organizer_checkpoints/` 보존 사본이나 `metadata.native_run`에서 실행 경로를 추측하지 않는다.

download handoff는 canonical evidence를 옮기는 것이 아니라 로컬 다운로드용 복사본이다. 기본 경로는 PERSONAL `/home/shadeform/ISSACSIMZ_DOWNLOAD/`, OFFICIAL `/workspace/ISSACSIMZ_DOWNLOAD/`이며 override는 `ISSACSIMZ_DOWNLOAD_ROOT`다. PERSONAL 자동 6지형 suite는 성공한 각 영상을 `videos/<label>.mp4`로 보존하고, 전부 검증된 후 GitHub Release에 게시한다(`--no-publish`면 로컬만). 이 자동 suite 스크립트와 게시만 OFFICIAL에서 차단된다. OFFICIAL에서 H1 6지형 영상을 요청하면 기존 `play.py`를 지형별 6회 직접 실행하고 매 영상 직후 별도 이름으로 복사하는 [17의 native 예시](17_ISSACSIMZ_VIDEO_OPERATIONS.md)를 따른다. 이 수동 영상 폴더는 sidecar suite manifest·archive를 자동 생성하지 않는다.

## GUI와 headless 운영 원칙

- 화면이 필요 없는 학습·batch 평가·처리량 진단은 공식 스크립트가 지원하는 `--headless`를 기본으로 한다. GUI·viewport 렌더링을 줄이면 CPU/GPU 렌더 부담과 관련 RAM·VRAM 사용을 줄일 여지가 있다.
- 절감량은 환경마다 다르다. headless에서도 물리 시뮬레이션, 환경 tensor, terrain, policy, CUDA 메모리는 그대로 필요하므로 “메모리를 거의 쓰지 않는다”고 해석하지 않는다.
- 카메라·이미지 센서가 필요 없는 학습에는 `--enable_cameras`를 켜지 않는다. 이 옵션은 GUI 없이도 오프스크린 렌더러를 활성화하므로 GPU 연산과 VRAM을 사용한다.
- play 영상·시각 디버깅·이미지 기반 평가만 별도 렌더 실행으로 분리한다. 학습 처리량을 측정할 때는 영상 녹화를 끈다.
- 자체 `SimulationApp` 도구는 headless에서도 기본 viewport overhead가 남을 수 있다. 카메라와 streaming이 전혀 없는 경우에만 `disable_viewport_updates=True`를 검토하며, streaming에는 사용하지 않는다.
- 공식 서버에서는 최적화를 이유로 제공 설정을 임의 수정하지 않는다. `train.py --help`로 지원 여부를 확인하고 공개된 CLI만 쓴다.
- 실험 기록에는 GUI/headless, camera/offscreen rendering, viewport update, video recording 여부를 남긴다. 이 조건이 다른 실행의 seconds/iteration과 VRAM 사용량을 직접 비교하지 않는다.

## Go2 L40S 학습 벽시계 (로그 실측)

2026-08-30 개인 Go2 12k 시도의 `go2-12k.log`를 파싱한 값이다. 추정 아님. 공식 서버 시간이 아니다.

- 1,000: 1시간 16분 44초
- 5,000: 5시간 56분 33초 → 예산은 **5k ≈ 6 GPU-hours**
- 9,000: 10시간 34분
- 9,500 누적 11시간 21분 55초는 iter 9451 stall(약 9분, SPS 176)을 포함하므로 정상 9.5k 시간으로 쓰지 않는다

표와 1k 구간 속도는 `07`과 `data/processed/experiments/go2/2026-09-11_GO2_12K_WALLCLOCK_FROM_LOG.md`를 따른다. 3k screening은 이 run 기준 약 3시간 40분이다.

## Go2 영상 운영에서 확인한 것

2026-08-30 개인 L40S/Isaac Sim 5.1.0-rc.19 실행 기록 기준이다. 학습은 4096 envs였고 영상은 로봇 1대였다. 영상 속 로봇 수로 학습 병렬 수를 추정하지 않는다.

- 10,000 step 영상은 CPU RAM 약 70GB 부근에서 OOM이 발생했다. 학습의 value-loss/std 오류와 별도 사건이며 영상이 학습 발산을 유발했다는 인과관계는 입증되지 않았다.
- 6,000 step은 한 대·headless·카메라·영상용 1×1 terrain 조건에서 두 후보 모두 완성됐다. 시스템 RAM은 약 53GiB까지 증가 후 유지됐다. 메모리 누적은 관찰됐지만 구체적 누수 원인은 확정하지 않는다.
- 50Hz에서 6,000 step은 약 120초 영상이다. 실제 생성 시간은 렌더·인코딩·종료를 포함해 더 길다. 경과 시간이나 프로세스 존재만으로 진행률·정상 상태·완료 임박을 단정하지 않는다.
- 한 번에 재생 하나만 실행하고 재시도 전 자식 프로세스·자동 재실행 작업·종료 코드·파일을 확인한다. 120초는 보편적인 메모리 안전 상한이 아니다.
- 지형 축소는 영상 관찰 조건을 바꾼다. 학습 조건이나 여러 지형 성능 평가와 동일하게 취급하지 않는다.

이 Go2 설정의 episode limit은 20초, 명령 resampling은 10초다. 120초 영상은 여러 episode의 행동 자료이며 연속 120초 생존 증명이 아니다. 단일 행동은 18~20초, 반복 관찰은 60~120초처럼 목적에 맞춰 선택한다.

당시 massedcompute L40S는 stop/start 불가 옵션이었다. 프로세스 종료·유휴 상태를 과금 중단으로 안내하지 않는다. 삭제 전 백업 내용과 hash를 검증하고 인스턴스 삭제 여부를 별도로 확인한다.

## 공식 Go2 1K 실행 시간과 영상 증거

공식 baseline 1K의 metadata UTC 구간은 2026-09-13 14:50:27~15:55:29(약 65분 02초), native training time은 `3887.04 s`(64분 47초)다. 이 공식 Go2 실측과 기존 개인 L40S 시간을 구분한다. 보고서의 median iteration은 3.91초, median 처리량은 25,137 steps/s이며 다른 학습량·서버의 보장값으로 확대하지 않는다.

보고서 GPU 집계는 1,928 samples, utilization 평균 87.81%, VRAM 최대 7008 MiB, power 평균 180.76 W다. 초기화·종료 idle을 포함한다. metadata UTC와 native/CSV의 KST는 +09:00 차이로 연결한다.

video manifest는 train의 `model_800.pt`와 동일한 best checkpoint를 MP4 SHA-256 `9cd9546dfed7cd7eee7e7ec08732a23a0ef006e0d0b68e0937f91ccaa61493c6`에 연결한다. 보고서의 ffprobe 결과는 H.264, 1920×1080, 50fps, 999 frames, 19.98초다. 이는 요청 video_length 1000과 실제 media frame 수를 따로 기록해야 하는 사례다. 낮은 자세로 버틴다는 행동 해석은 보고서 관찰이며 공식 평가나 장기 생존 증명이 아니다.

개인 L40S `LINTRACK-150-LINZ-2` fresh 3K 보고서(원문 legacy A1)는 약 2.76시간, 평균 약 29,887 steps/s, GPU utilization 평균 76.2%, VRAM 평균 약 7.52 GiB로 기록한다. 공식 RTX 5080 baseline과 하드웨어·run이 다르므로 속도를 직접 비교하지 않는다. 3K video는 best `model_2900`과 연결된 H.264 1920×1080, 50fps, 999 frames, 19.98초로 보고됐고 MP4 SHA-256은 `deb0b7d548e572555de07ed4132bf54740b641a99efec87f47d704a9d53d43af`다. 20초 단일 env 영상은 정성 증거다.

공식 `LINTRACK-150-LINZ-2` fresh 5K 시도(legacy G-005 계보)는 약 iter 4837에서 broken pipe로 끊겼지만 sidecar가 console·TensorBoard·49개 checkpoint를 interrupted archive로 보존했다. finalize 미실행과 backup unknown 때문에 validation FAIL인 것이 정상이며, 이를 completed로 바꾸지 않는다. 원본 `model_4800`에서 시작한 recovery는 200회를 더 실행해 console 4999까지 도달하고 finalize·backup·validation PASS를 남겼다. 이 사례에서 `metadata.final_iteration=4900`은 마지막으로 mirror된 100-간격 checkpoint이지 마지막 학습 iteration이 아니다. 운영 기록에는 requested 5000, last logged 4999, last saved 4900을 별도 필드로 쓴다.

영상 전 32MB handoff와 6-video 완료 뒤 79MB handoff는 같은 recovery run의 의도적인 두 단계다. 전자는 후자의 byte-identical subset이므로 별도 run으로 세지 않는다. loose export/video 복사본도 final wrapper와 hash가 같으면 canonical을 다시 늘리지 않는다. 반면 이름이 `4800 submission`이어도 내부 policy가 recovery 4900과 연결된 혼합 bundle은 제출 후보로 쓰지 않는다.

4300·original 4800·recovery 4900의 첫 고정 비교는 개인 L40S에서 완료됐고, 이어 4800/4900의 native 비교 영상 6개도 보존됐다. original 4800에서 새로 export한 matching policy/env 제출 snapshot은 공식 3라운드 평가 87.55/100을 받았다. 과거 recovery `policy.pt`를 4800 정책으로 이름만 바꾼 혼합 bundle은 제출 근거로 사용하지 않는다. 추가 개인 평가가 필요하면 같은 evaluator·command·horizon을 유지한 seed 반복과 worst terrain 확인을 우선한다.

첫 개인 L40S fixed batch는 seed 4201·difficulty 1.0에서 18개 조합을 완료했고 checksum·raw 집계도 검증됐다. 이 결과로 original 4800이 multi-seed 우선 후보가 됐지만 한 seed를 공식 점수나 최종 승자로 승격하지 않는다. **당시 4800/4900 비교를 확장한다면** 같은 evaluator·commit·command·64 env·20초에서 seed를 추가해 worst-seed를 확인하는 것이 우선이었다. inverted stairs는 생존 외에 전진·traversal을 기록한다. 현재 `07`·`21`의 후속 PERSONAL same-protocol 비교는 `g2-submit-3` original 4800, `model_7050`, terminal `model_7450`까지 완료됐다. **7450은 내부 행동 주후보 PROMOTE, 7050은 안전성 fallback HOLD, 4800은 현재 all-around 후보 기준 REJECT**다. 남은 핵심 불확실성은 stair-up seed 4201에서 7050의 종료 2회 대비 7450이 4회인 차이의 재현성이다. terminal 7450은 이후 `g2-submit-5 / LINTRACK-125`로 실제 Round-5 제출됐다고 사용자가 2026-10-06 확인했다. 따라서 stair-up 추가 seed/반복은 더 이상 R5 제출 전 gate가 아니라 향후 라운드/분석에서 그 차이가 의사결정을 바꿀 때만 고려한다. 이 문서 갱신은 GPU 실행 승인이 아니다.

뒤이어 수행한 4800/4900 native 영상 6개는 evidence validation 6/6과 최종 MP4 checksum 6/6을 통과했다. 두 모델 모두 같은 native play·seed·카메라·길이·terrain proportion을 사용했지만 native curriculum/command manager가 활성 상태였고 fixed evaluator의 difficulty·명령·진행 방향을 재현하지 않았다. 서버 운영상 이를 “영상 비교 완료”로 기록할 수는 있어도 “정량 평가 반복”이나 “terrain 완주 검증”으로 기록하지 않는다. 고정 traversal 영상을 다시 만들 때만 curriculum OFF, difficulty, command, spawn heading과 completion 기준을 명령/metadata에 명시한다.

## 최소 기능부터

1. 제공 환경과 최대한 비슷한 재생·관찰 환경을 만든다.
2. 정책별 메타데이터와 play 영상을 저장한다.
3. 평지 추종, 회전, 지형, 외란 회복 평가를 분리한다.
4. 여러 실행 결과를 모아 후보 leaderboard를 만든다.
5. 연습 게임은 정책·전략의 통합 관찰에만 사용한다.

## 운영 규칙

- smoke run과 사전 점검은 파일·경로·import/load·짧은 실행·exit code·치명 오류 확인으로 끝낸다. 이미 검증한 source·artifact 전체를 이유 없이 다시 SHA-256으로 훑지 않는다.
- 일반 디버깅과 짧은 play에는 checksum을 기본값으로 넣지 않는다. 특정 checkpoint나 policy가 같은 바이트인지가 실제 원인 판별에 필요할 때만 해당 파일을 확인한다.
- 장시간 학습, video render, evaluator, checkpoint export처럼 서버 시간·GPU를 쓰는 작업은 직접 사용하는 checkpoint와 생성 산출물의 hash를 확인할 수 있다. 그러나 그 작업과 무관한 source tree 전체 반복 hash는 추가하지 않는다.
- evidence·archive·제출·다운로드 handoff처럼 동일성·손상 여부가 결과의 일부인 단계에서는 SHA-256과 manifest 검증을 쓴다. 같은 실행에서 이미 확인한 파일은 변경이나 재전송 근거가 없으면 반복하지 않는다.
- OFFICIAL 서버에서는 사용자에게서 명시적 종료 권한을 받아도 AI가 shutdown, poweroff, halt, reboot, instance stop 또는 동등한 종료·재시작 명령을 실행하지 않는다. 명령 체인·trap·정리 스크립트·자동화에도 넣지 않는다. 종료가 필요하면 사용자 본인이 처리하도록 상태만 보고한다. PERSONAL 서버는 사용자가 명시적으로 요청한 경우에만 종료할 수 있다.
- checkpoint·archive·원본 산출물 삭제나 교체는 자동 정리가 아니다. 요청된 정확한 대상만 처리하고, 가능한 경우 복구 가능한 방식으로 이동한다.
- 공식 점수·공식 순위를 내부 점수로 대체하지 않는다.
- 서버를 켜기 전에 실험 ID, 담당자, 단일 가설, 실행 명령, 종료 조건, 필요한 산출물을 확정한다. 종료 전에는 결과 파일·로그 다운로드와 실험 기록을 확인한다.
- 사용자가 export·다운로드·서버 종료를 언급하면 `logs/<run>/` 전체, TensorBoard event, 콘솔 로그, 실행 전·후 GPU snapshot, 코드·설정 hash를 먼저 확인하도록 안내한다. personal의 주기 GPU telemetry는 추가 증거이며, official에서는 sidecar 상주 sampler를 기대하지 않는다.
- 팀 서버는 한 시점에 한 명만 접속하는 운영 기준을 따르고, 읽기·토론·대규모 분석은 서버 밖에서 수행한다.
- 참가자가 직접 작성한 반복 실행 스크립트와 서버에 새 에이전트·도구를 설치하는 행위를 구분한다. 전자는 공식 안내 영상의 허용 예시이고, 후자는 제공 환경 변경 금지에 걸린다.
- 백업에 있던 credential, key, tracker, 원본 에셋을 외부 공개·재배포하지 않는다.
- 개인 서버 작업도 실험 단위로 기록해 팀이 같은 실험을 반복하지 않게 한다.
- 고장 원인을 먼저 환경 차이, 정책 파일 형식, 명령 범위, 지형 차이 순으로 좁힌다.
- Optuna·trial DB·objective 계산은 개인 PC 또는 개인 NVIDIA 서버에서만 실행한다. 공식 서버에는 추천된 reward 값만 수동 반영한다.
- Optuna DB에는 파라미터와 objective만 두고, policy·env·영상·전체 metric은 trial ID와 SHA-256으로 연결한 별도 artifact로 보관한다.
- 서로 다른 학습 iterations나 evaluator 버전의 결과를 한 study에 섞지 않는다.

## AI 응답 규칙

개인 서버의 제안은 항상 “검증용”으로 표현하며, 제출 정책을 외부에서 재학습·변조하도록 안내하지 않는다.

## H1 재실험 실행 전 계보 확인 — 2026-09-21

과거 PERSONAL H-001 부모(`feet=-0.2`)와 공식 `TERM-50`(`+0.2`)을 혼동하지 않는다. 새 Run은 실제 부모 설정과 checkpoint identity를 확인하고 Delta를 기록한다. 실행 상태는 evidence와 [가설 registry](../../../research/EXPERIMENTS.md)를 따른다. [계보 상세](14_H1_NEXT_RUN_PARAMETER_COMPARISON.md).
