---
title: 'issacsimz 외부 evidence CLI 사용법'
purpose: '기존 Isaac Sim 학습 명령을 수정하지 않고 mode별 console·GPU·native run·checkpoint·archive 증거를 보존하는 범용 sidecar 사용법'
sources:
  - 'data/processed/incoming/other/reviewed/GO2_A1_1K_3K_VIDEO_FULL_EVIDENCE_ANALYSIS_20260914.md'
  - 'data/processed/incoming/other/reviewed/GO2_A1_THREE_EXPORTS_DEEP_ANALYSIS_20260914.md'
  - 'data/processed/incoming/other/reviewed/GO2_A1_MODEL_4300_DEEP_ANALYSIS_20260915.md'
  - 'data/processed/incoming/other/reviewed/GO2_A1_MODEL_4800_DEEP_ANALYSIS_20260915.md'
  - 'data/processed/incoming/other/reviewed/GO2_A1_MODEL_4900_DEEP_ANALYSIS_20260915.md'
  - 'data/processed/incoming/other/reviewed/A1_4800_vs_4900_DEEP_ANALYSIS_AND_LEARNING_RECORD_20260915.md'
  - 'data/processed/experiments/go2/2026-09-15_GO2_G-005_4800_4900_NATIVE_VIDEO_AND_SELECTION.md'
  - 'data/processed/incoming/other/reviewed/GO2_OFFICIAL_BASELINE_1K_AND_ISSACSIMZ_LOGGING_ANALYSIS_20260914.md'
  - 'naver-issacsim-originals official-go2-20260914-angxy-012-1k (G5/G-004 official 1K train archive SHA-256 1e162fdf640a715f19c564e21bff1011cd7ed91287db2f8d3586c3e0382d4359; internal SHA256SUMS 33/33 and validation PASS)'
  - 'Codeberg passerby1/issacsimz commit b24103b (organizer-provided H1 keep_ckpt.sh body scope clarified, stored verbatim and regression-checked; official persistent GPU sampler and generic checkpoint watcher/mirror remain disabled; official watch rejected; personal monitoring unchanged; 80 WSL fixtures)'
  - 'Codeberg passerby1/issacsimz commits 279fdec and 7a38413 (immutable finalized evidence after archive creation; FAIL handoff isolation; official user --collect rejection; checkpoint symlink/containment checks; full task Python source fingerprint; git-less ZIP fallback and portable build verification)'
  - 'Codeberg passerby1/issacsimz commit b7a231c (PERSONAL video suite explicit publish after verification; 10 assets; annotated tag from NVIDIA checkout; Windows 117 tests with 44 Linux/WSL fixtures skipped and shell syntax verified)'
  - 'Codeberg passerby1/issacsimz commit 018330b (both train modes pass save_interval=50; OFFICIAL run-specific organizer-derived keep-all copies checkpoints into automatic evidence/archive; 119 local WSL tests and portable build PASS)'
  - 'Codeberg passerby1/issacsimz commit d55f0be (PERSONAL general train/video publisher prepares an annotated tag from the checkout commit before Release creation; 121 local WSL tests and portable build PASS)'
  - 'Codeberg passerby1/issacsimz commit c6bed9f (PERSONAL six-terrain suite auto-publishes once after verification; --no-publish opts out; personal bootstrap configures repository-local Git tag identity; 121 local WSL tests and portable build PASS)'
  - 'Codeberg passerby1/issacsimz commit 16e07f8 (direct launcher inherits bootstrap evidence root unless explicitly overridden; related local WSL tests 52/52 PASS)'
  - 'Codeberg passerby1/issacsimz commit b5f0b15 (OFFICIAL indexed numbered checkpoint resume uses a native basename selector, verifies and restores keeper bytes only to the recorded native run, and preflights before tmux; Windows 124 tests with 48 Bash-dependent skips)'
  - 'Codeberg passerby1/issacsimz commit 0070ff6 (shell and portable tmux paths preflight before session creation; personal publisher accepts only completed PASS evidence and verifies remote asset size/digest)'
  - 'Codeberg passerby1/issacsimz commit 9f78009 (PERSONAL train and six-video Release accept optional Experiment/config display names; Go2 preset uses g2-submit-N; WSL 129/129 and portable build PASS)'
  - 'Codeberg passerby1/issacsimz commit bea81fa (README documents the optional preset-aware Release labels; no runtime change after 9f78009)'
  - 'https://isaac-sim.github.io/IsaacLab/develop/source/api/lab/isaaclab.terrains.html (pyramid_sloped_terrain defines slope as height change / horizontal width, while HfPyramidSlopedTerrainCfg field text calls slope_range radians; horizontal_scale is x/y discretization)'
  - 'naver-issacsim-originals main 4ebdaef (canonical official /workspace/training snapshot 2026-09-13 19:59:15; archive SHA-256 2c1326e0b58e9c860e32db81f110d2c0de16fac113de4424144b73e39fe01d15)'
  - 'naver-issacsim-nvidia training provenance commit 428a61d (training synchronized byte-for-byte with that official snapshot; later documentation-only commits do not change training/; personal orchestration remains outside training/)'
  - 'data/processed/incoming/other/reviewed/NCRC_20260913_MASTER_TRACKING_REPORT.md (G5 result and historical video-forensics correction)'
  - 'data/processed/incoming/other/reviewed/2026-09-26_H1_ORGANIZER_CHECKPOINT_QA_SIRIUS_YEOLMU.md (participant question and organizer reply; provided transcript, not a tested script)'
type: 'implementation_usage_with_official_go2_normal_path_evidence'
---

> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/ai_library/19_ISSACSIMZ_EXTERNAL_EVIDENCE_CLI.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.


# issacsimz 외부 evidence CLI

## 역할과 경계

`issacsimz`는 기존 Isaac Sim 학습 명령을 **그대로 실행**하고, 그 바깥에서 evidence를 기록하는 Python 표준 라이브러리 기반 도구다. 학습 task, reward, Isaac Lab 설치, 공식 `train.py`·`play.py`·`_finalize.py`를 수정하지 않으며 원본 checkpoint를 이동하거나 삭제하지 않는다.

Windows 로컬 영상·개별 평가는 [21](<21_WINDOWS_GO2_VIDEO_AND_EVALUATION.md>)과 `naver-issacsim-eval/WINDOWS_H1_WORKFLOW.md`의 robot별 통합 launcher를 쓴다. Go2 진입점은 `C:\NCRC\go2_6terrain_video.bat`, H1 진입점은 `C:\NCRC\h1_6terrain_video.bat`다. 두 경로 모두 원본 checkpoint SHA를 기록하고 ASCII work directory에 동일 bytes를 staging한 뒤 고정 6영상과 별도 camera-off full evaluator 자료를 순차 수집하며 `issacsimz` 서버 CLI나 자동 Release를 호출하지 않는다. H1은 ±10° 6영상과 `scenario7` 8 case(기본 128 env × seeds 4201/4202/4203)를 사용한다. standalone/integrated smoke 옵션은 제거됐고, 완료된 evaluation 폴더의 A/B 비교는 사용자가 명시적으로 맡긴 경우에만 `compare_policies`를 쓴다. H1/Go2 CPU 회귀 테스트 60개와 PowerShell/설치 검증은 완료됐다. 이 문서의 최초 작성 시점에는 H1 GPU full 근거가 없었지만 **2026-10-07 `ORIENT-100 / model_2850` Windows PERSONAL 6영상/단일 정책 full(3,072 episode) 완료 자료**가 확보됐다. [기록](<../../../../../../reports/received/H1_ORIENT-100_POLICY_ANALYSIS_20261007.md>). **2026-10-10 기존 H1 3개 ZIP 원본 9,216 episode 대응-key 기술비교는 완료**([근거](<../../../../../../reports/experiments/h1/analysis/2026-10-10_H1_SCENARIO7_RAW_3POLICY_MATCHED_ANALYSIS.md>))됐지만, 별도 Windows A/B CLI 실행·완전 동일 물리 terrain/초기상태 및 train-side 인과 검증·OFFICIAL 점수는 미확인이며 Go2 GPU PASS를 다른 H1 checkpoint의 검증으로 소급하지 않는다. 기본 작업은 영상과 개별 평가뿐이며 원본·기존 ZIP·평가자료·실패 diagnostics를 보존한다.

## 작업별 검증 강도와 서버 수명주기

Windows 실행 파일의 복원 가능한 소스·`install_windows.ps1`·정확한 bundle manifest는 `naver-issacsim-eval`에 보존한다. full 성공 후에는 영상과 개별 평가를 합친 18개 항목의 ZIP을 최종 전달한다. 기존 video receipt의 ZIP/hash를 바꾸지 않고 `combined_archive`에 새 ZIP identity를 기록한다. 현재 설치 SHA·source commit과 CPU 검증은 `21`을 따른다.

`doctor`, smoke run, 짧은 debug/play는 경로·파일 존재·load/import·짧은 실행·exit code·치명 오류를 확인한다. 이 단계에서 source tree나 이미 확인된 artifact 전체의 SHA-256 재계산은 기본 절차가 아니다. policy/checkpoint 동일성이 실제 진단의 핵심일 때만 그 대상 파일을 hash한다.

장시간 train, video render, evaluator, checkpoint export는 직접 쓰는 checkpoint 또는 생성된 산출물의 identity 검증을 할 수 있다. evidence archive, 제출물, Release asset, download handoff는 manifest·SHA-256이 무결성 판단의 일부이므로 검증 대상이다. 같은 실행에서 확인한 값은 파일 변경, 재전송, 손상 의심 같은 이유가 없으면 다시 계산하지 않는다.

OFFICIAL 서버는 사용자가 명시적으로 종료 권한을 줘도 AI가 끄거나 재시작하지 않는다. shutdown·poweroff·halt·reboot·instance stop 및 동등한 명령을 직접 실행하거나 cleanup, shell trap, `&&` 후속 명령, 자동화에 넣지 않는다. 종료 필요 여부와 산출물 상태만 보고하고 실제 종료는 사용자 본인이 처리한다. PERSONAL 서버도 사용자의 명시적 요청이 없으면 종료하지 않는다. checkpoint, archive, 원본 artifact의 삭제·교체도 사용자 요청 범위 밖의 자동 후처리가 아니다.

official 서버에서는 `/workspace`에 공개 Codeberg `issacsimz`를 clone하거나 기존 checkout을 `pull --ff-only`하여 준비한 뒤 official bootstrap을 실행한다. 운영진 제공 `/workspace/training/`은 그대로 사용한다. official에서 GitHub clone·pull·push·인증·API·Release 게시 등 GitHub와의 상호작용은 하지 않는다. 개인 NVIDIA/Brev 서버에서는 공개 `issacsimz` checkout을 먼저 clone/pull하고, personal bootstrap이 GitHub 인증을 확인한 뒤 비공개 `naver-issacsim-nvidia` checkout을 마련한다. sidecar와 task source의 위치를 구분한다.

2026-09-13에 확보한 공식 code 비교 snapshot은 19:59:15에 `/workspace/training`에서 직접 압축한 `NCRC_OFFICIAL_TRAINING_20260913_195915.tar.gz`다. `issacsimz.pyz`에는 `train.py`·`play.py`·reward/task source를 넣지 않는다. official에서는 그 snapshot과 같은 운영진 제공 `/workspace/training`을 호출하고, personal에서는 snapshot과 byte-for-byte 동기화된 NVIDIA `training/`을 호출한다. personal setup/bootstrap은 `training/` 바깥에만 둔다.

**이전 2026-10월 초 검사 기록:** sidecar `bea81fa`(동작 변경 `9f78009`, 후속 README만 수정)의 로컬 WSL 전체 단위 테스트는 **129/129 PASS**이고 `build_portable.sh`의 내장 테스트·archive checksum도 PASS다. Windows 로컬에서는 129개 중 78개 실행 PASS·51개 skip였으며 한글 경로의 Python runner 문제로 build를 완료하지 못했지만, 뒤이어 WSL에서 build를 확인했다. OFFICIAL 서버의 실제 resume 학습이나 GitHub Release 게시를 실행한 검증은 아니다. 과거 `16e07f8`의 evidence-root 관련 WSL 52/52 PASS 및 `c6bed9f`의 전체 121/121·portable build PASS를 현재 서버 검증으로 소급하지 않는다. profile train은 두 mode 모두 native `agent.save_interval=50`을 전달하고, OFFICIAL은 run별 organizer keep-all로 checkpoint를 evidence/archive에 보존한다. PERSONAL publisher는 checkout commit의 annotated tag를 먼저 push한다.

## 공식 Go2 정상 완료 실전 검증 범위

공식 Go2 baseline 1K와 legacy G-004 R02 1K는 정상 완료·backup·archive의 실측 사례다. `g2-submit-3 / LINTRACK-150-LINZ-2` 계보의 legacy G-005 R03 fresh 시도는 약 iter 4837에서 중단됐어도 실패 evidence를 보존했고, 원본 4800에서 이어간 recovery는 console 4999까지 완료됐다. original 4800과 recovery 4900의 영상 evidence 6건은 source/MP4 hash 연결을 확인했지만 fixed evaluator 결과는 아니다. 개별 검증 수치·원본 위치·정책 판정은 [16번 보존 근거](<16_EXPERIMENT_EXPORT_AND_TENSORBOARD.md>)와 07번 Go2 분석〔원본 참조: `07_QUADRUPED_TRAINING_CODE.md` / 공개 사본 미포함〕에 둔다. 과거 수신 run의 sidecar build hash는 확인되지 않아 현재 build 전체의 서버 검증으로 소급하지 않는다.

이 사례에서 recovery의 `final_iteration=4900`은 마지막 저장 checkpoint이고 마지막 학습 로그는 4999였다. requested/logged/saved/selected/best step을 분리하며, 같은 이름의 `model_4800.pt`도 원본과 recovery의 SHA가 다르므로 checkpoint 이름만으로 계보를 판단하지 않는다. loose 영상 묶음은 개별 video evidence의 source linkage를 대신하지 않는다.

당시 보고서의 runtime/build identity, 시간대, video 규격, scalar·value-loss 요약, 선택 checkpoint 기록 제안은 **backlog이지 구현 완료 기능이 아니다**. 현재 사용법은 아래 절차를 따른다.

## Experiment registry와의 연결

`issacsimz` evidence ID와 [새 Experiment 이름](<../../../../../../research/EXPERIMENT_NAMING.md>)은 역할이 다르다. evidence ID는 실제 train/video 작업을 식별하고, Experiment는 검증 질문을 식별한다. Video evidence는 새 학습 Run이 아니다. Sidecar는 registry를 만들거나 고치지 않으며, 작업자는 train 시작 전 질문·기준 preset·예상 override·부모를 정하고 완료 뒤 실제 학습 evidence ID와 archive를 Run에 연결한다. 기존 H/G/HS/GS·Rxx는 legacy 검색 주소로 남긴다.

같은 질문의 1K·3K·5K·resume·seed repeat은 새 H/G/HS/GS ID가 아니라 각각의 실제 학습 Run으로 기록한다. 다른 검증 질문에는 새 Experiment 주소를 쓰고, final config와 transition lineage를 분리한다. official mode가 만든 validated archive는 해당 Run을
`OFFICIAL`로 식별하는 근거가 될 수 있지만, personal evidence는 동일한 sidecar 형식이라도
`PERSONAL`로 남긴다. 이 연결은 canonical evidence를 복제·이동하지 않으며 외부 publish 정책과도 독립적이다.

## 시작

shell 진입점·bootstrap·train/video wrapper·portable build는 `ISSACSIMZ_PYTHON_RUNNER`가 있으면 그것을 엄격히 사용하고, 없으면 `python3`, 그마저 없으면 명시된 IsaacLab root의 `_isaac_sim/python.sh`와 표준 Isaac Sim 후보를 찾는다. bootstrap은 선택한 실행기와 함께 현재 mode에서 선택된 `ISSACSIMZ_H1_ROOT`·`ISSACSIMZ_GO2_ROOT`·`ISSACSIMZ_ISAACLAB_ROOT`·`ISSACSIMZ_EVIDENCE_ROOT`를 state에 기록한다. 직접 `./issacsimz` 실행 시 launcher는 별도 `ISSACSIMZ_LOG_ROOT` override가 없으면 state의 evidence root를 기본 log root로 전달한다. 따라서 wrapper 학습 run과 직접 CLI play가 서로 다른 기본 root를 보지 않는다. 명시한 runner가 잘못됐으면 조용히 다른 실행기로 넘어가지 않고 실패한다. 실제 profile train/play child는 별도로 확인한 `isaaclab.sh -p <train.py|play.py>`를 사용한다.

AI 명령 생성 규칙은 고정한다. `python3 train.py`, `python3 play.py`, `python3 issacsimz.pyz`를 습관적으로 직접 쓰지 않는다. checkout에서는 `./issacsimz` 또는 mode-aware shell wrapper를 사용한다. pyz만 단독으로 다뤄야 한다면 bootstrap이 검증·저장한 `ISSACSIMZ_PYTHON_RUNNER`로 실행한다. 화면에 sidecar용 `python3` process가 보일 수 있지만 native 학습 Python을 직접 지정한 것은 아니다.

profile `train`·`play`·`video`는 `ISSACSIMZ_MODE`가 없거나 `personal`/`official` 이외 값이면 즉시 실패한다. 이 검사는 CLI의 tmux 분기 전과 core의 profile evidence 생성 전에 적용되므로 portable을 직접 호출해도 mode 추론으로 personal watcher가 켜지지 않는다. bootstrap READY는 personal에는 게시 없는 직접 CLI smoke를, official에는 mode-aware tmux wrapper를 안내한다. 장기 실행은 `./scripts/issacsimz_tmux_train.sh ...`를 사용한다. 범용 `run`과 `watch`는 명시적 `personal` mode에서만 사용할 수 있고 official에서는 실행 전에 거부한다.

`--task-root`나 `--isaaclab-root`를 직접 준 경우도 strict하다. 각각 `train.py` 또는 `isaaclab.sh`가 없으면 환경변수나 `/workspace` 기본값으로 fallback하지 않고 즉시 실패한다. 옵션을 생략했을 때만 기존 환경변수·기본 경로 자동 탐색을 사용한다. tmux launcher 단위 테스트는 테스트 시작 시 `TMUX`를 제거하므로 실제 서버 shell이 tmux 안인지와 관계없이 detached-session 경로를 같은 방식으로 검사한다.

```bash
./issacsimz doctor --robot h1
```

### AI가 제시하는 서버용 복사·실행 카드

AI가 매번 긴 셸 스크립트를 즉석에서 재작성하지 않는다. **Brev 기본 home/base는 `/home/shadeform`이고, 현재 NVIDIA README의 새-VM checkout 기본 예시는 `/ephemeral`이다. 실제 checkout/task root는 실행 전에 확인하며 두 경로 개념을 혼동하지 않는다.** 사용자가 “Brev 셋업 스크립트 완료/서버 켬”이라고만 하면 **기본 환경 준비 단계**로 해석한다. 그것만으로 `issacsimz`나 비공개 NVIDIA checkout이 존재하거나 `pull`·personal bootstrap·doctor·`READY`가 끝났다고 가정하지 않는다. 먼저 **PERSONAL 첫 접속 / PERSONAL 재접속 / OFFICIAL 첫 접속 / OFFICIAL 재접속** 중 하나를 확인하고, 아래 해당 준비 명령만 별도 블록으로 제시한다. PERSONAL 첫 접속이면 `issacsimz` clone → 그 checkout에서 personal bootstrap → 비공개 NVIDIA checkout 준비·두 doctor·`READY` 순서다. 재접속이면 기존 checkout의 실제 존재를 확인한 뒤 `pull --ff-only`한다. OFFICIAL은 공개 Codeberg sidecar만 clone/pull하고 GitHub에는 접속하지 않는다. checkout이 없는 시점에 그 경로의 `git status`, `doctor`, `reward`, `runs list`, checkpoint 탐색을 첫 단계로 요구하지 않는다. 경로가 예시와 다르면 실제 checkout 위치를 확인해 바꾸며, 존재하지 않는 경로로 `cd`하거나 실패를 무시하고 학습 명령으로 이어가지 않는다. 학습 명령의 로봇·Experiment 질문·부모 checkpoint·iteration·env·name은 실험 기록과 대조해 채우고, 실제 evidence Run ID는 실행 후 기록한다. 자격 증명이나 token을 명령·로그에 노출하지 않는다.

```bash
# PERSONAL 첫 접속: 현재 NVIDIA README의 새-VM 기본 checkout 예시.
# /ephemeral 자체가 Brev home/base라는 뜻은 아니다.
cd /ephemeral && \
test ! -e /ephemeral/issacsimz && \
git clone https://codeberg.org/passerby1/issacsimz.git issacsimz && \
cd /ephemeral/issacsimz && \
bash scripts/bootstrap_server.sh --mode personal
```

```bash
# PERSONAL 재접속: 먼저 실제 checkout 위치를 확인한다.
# 아래는 현재 README 기본 위치가 실제로 존재할 때의 예시다.
test -d /ephemeral/issacsimz/.git && \
git -C /ephemeral/issacsimz pull --ff-only && \
cd /ephemeral/issacsimz && \
bash scripts/bootstrap_server.sh --mode personal
```

PERSONAL bootstrap은 GitHub 인증 상태를 확인하고 필요한 경우 로그인 절차를 안내하며, private `naver-issacsim-nvidia` checkout을 clone/fast-forward pull하고 두 profile doctor를 확인한다. Release용 annotated tag의 Git 작성자 정보를 해당 checkout의 로컬 설정에만 기록하며 이메일은 `ncrcissacsimz@users.noreply.github.com`이다. global Git 설정이나 OFFICIAL 서버에는 적용하지 않는다. `READY`가 없거나 인증·pull·doctor가 실패하면 중단한다. 별도 `gh auth login`·private clone·무조건 `git reset`을 AI가 덧붙이지 않는다. 이 시작 카드는 bootstrap의 대체 구현이 아니다.

```bash
# OFFICIAL 첫 접속: 공개 Codeberg sidecar만 가져온다. GitHub는 사용하지 않는다.
cd /workspace && \
git clone https://codeberg.org/passerby1/issacsimz.git issacsimz && \
cd /workspace/issacsimz && \
bash scripts/bootstrap_server.sh --mode official
```

```bash
# OFFICIAL 재접속: checkout과 clean 상태를 확인하고 fast-forward만 허용한다.
test -d /workspace/issacsimz/.git && \
test -z "$(git -C /workspace/issacsimz status --porcelain)" && \
git -C /workspace/issacsimz pull --ff-only && \
cd /workspace/issacsimz && \
bash scripts/bootstrap_server.sh --mode official
```

OFFICIAL에서 checkout이 없으면 첫 접속 절차를 쓰고, 재접속 시 로컬 변경으로 pull이 막히면 reset하지 말고 원인을 확인한다. Codeberg는 공개 sidecar clone/pull에만 사용하며 GitHub clone·pull·push·인증·API·Release 게시 등 GitHub와의 상호작용은 금지한다. `/workspace/training/` 원본은 bootstrap을 대신한다는 이유로 수정하지 않는다. 두 mode 모두 bootstrap의 두 doctor와 `READY`를 확인한 후에만 기존 mode-aware train/tmux wrapper 명령을 제시하며 `python3 train.py`를 새로 만들지 않는다.

학습 후에는 native exit·finalize·validation과 checkpoint 계보를 먼저 확인한다. 후보 영상의 PERSONAL/OFFICIAL별 실행 명령은 [17번 영상 운영 문서](<17_ISSACSIMZ_VIDEO_OPERATIONS.md>)를 따른다.

끝 카드에는 `shutdown`·`poweroff`·인스턴스 stop, 원본 삭제·archive 교체를 넣지 않는다. OFFICIAL 서버 종료는 명시적 요청이 있어도 AI의 단계에 포함하지 않고 사용자 본인이 처리한다. PERSONAL 서버 종료는 사용자가 별도로 명시한 경우에만 별도 단계로 다룬다. 아래 official 실전 runbook과 PERSONAL 시작 블록이 상세 명령의 기준이며, 이 카드는 그 순서를 빠뜨리지 않게 하는 선택 규칙이다.

## 장시간 학습: tmux는 실행 보호층이며 로깅은 그대로 유지

`--tmux`는 학습·finalize·archive를 바꾸지 않고, 기존 `train` 명령 전체를 detached tmux session 안에서 실행한다. 터미널/SSH 연결이 끊겨도 학습이 계속되게 하는 실행 보호층일 뿐이므로 기존 evidence 기록은 모두 그대로 지속된다.

```text
공통:
console.log                   stdout/stderr 전체
system/nvidia_smi_before.txt  실행 전 단발 snapshot
system/nvidia_smi_after.txt   실행 후 단발 snapshot
native_run/                   TensorBoard event와 native 산출물

personal only:
system/nvidia_smi_during.csv  주기적 GPU 기록
checkpoints/                  stable model_*.pt mirror
watcher.log                   checkpoint 보존 기록
```

official은 학습 중 GPU sampler와 **범용** checkpoint watcher를 시작하지 않는다. 대신 profile train에는 운영진 공개 keep-all 방식의 run별 파생 셸 스크립트 `organizer_keep_all_ckpt.sh`를 자동 시작한다. 학습 중 안정된 native `model_*.pt`를 `backup_log/<native-run>/`로 복사하고 종료 후 `organizer_checkpoints/`에 수집한다. console·source hash·finalize/backup 판정·archive/handoff는 그대로 유지한다. 기존 `organizer_keep_ckpt_h1_verbatim.sh`는 운영진 제공 고정 회차 `keep_ckpt.sh` **본문**의 수정하지 않은 보관본이며 현재 자동 절차가 아니다.

PERSONAL·OFFICIAL profile train은 모두 native `agent.save_interval=50`을 자동 전달한다. 운영진 답변 전사본〔원본 참조: `../incoming/other/reviewed/2026-09-26_H1_ORGANIZER_CHECKPOINT_QA_SIRIUS_YEOLMU.md` / 공개 사본 미포함〕의 셸 블록은 줄바꿈이 합쳐져 실행 파일로 쓰지 않는다. `issacsimz`의 별도 keep-all 파생본은 현재 run·PID를 명시해 실행하며 기존 verbatim 파일·generic `CheckpointWatcher`·GPU sampler에는 합치지 않았다. `checkpoint_index.json`은 종료 시 native run과 run별 backup을 일회성으로 hash하고, 공식 evidence `.tar.gz`에는 보존된 checkpoint bytes까지 포함한다. 마지막에 `organizer_checkpoint_count`와 실제 회차를 확인하되, 과거 run도 이미 보존됐다고 소급 주장하지 않는다.

로컬 테스트의 보존·압축 예시는 `model_100.pt`·`model_200.pt`였다. 이후 OFFICIAL Go2 `LINTRACK-125` fresh 3K/7.5K evidence에서 `agent.save_interval=50`이 실제 명령에 들어가고, 3K는 `model_0.pt`~`model_2950.pt` 60개, 7.5K는 `model_0.pt`~`model_7450.pt` 150개의 50-step checkpoint가 보존된 것을 확인했다. 따라서 공식 서버 native 50회 저장 자체는 실측 완료다. 다만 이 사실을 최신 sidecar build 전체의 실전 OFFICIAL 검증으로 확대하지 않는다.

official `issacsimz train --extra`는 계속 거부되지만 `agent.save_interval=50`은 CLI가 native command에 고정으로 추가한다. 운영진은 보존된 다른 checkpoint를 택해 native `exported/model_best.pt`로 복사하고 `play.py`에서 `policy.pt`를 생성하는 것과, 제출 코멘트에 선택 회차·근거를 쓰는 것을 허용했다. 이것도 현재 `issacsimz` official `play --from-run`의 격리 staging/원본 exported 불변 경로와 **동일한 명령 절차가 아니다**. 우리 기본값은 충분히 긴 resume의 final numbered checkpoint 한 번 export이며, 예외를 고를 때는 자동 best·선택 checkpoint·export policy의 identity를 분리 기록한다.

공식 서버의 장시간 실행 권장은 다음이다. tmux wrapper가 mode-aware train wrapper 전체를 새 detached session에서 실행하고 즉시 shell로 돌아온다. 이미 tmux 안에서 호출한 경우에는 nested tmux를 만들지 않고 현재 session에서 foreground로 실행한다.

```bash
./scripts/issacsimz_tmux_train.sh go2 \
  --iters 5000 --envs 4096 --name go2-final
```

세션 기본 이름은 `issacsimz-go2-go2-final`이고 `--tmux-session <name>`으로 덮어쓸 수 있다. 공백·특수문자는 안전한 이름으로 정리되며, 같은 이름의 live session이 있으면 새 학습을 거부한다.

```bash
tmux attach -t issacsimz-go2-go2-final
# detach: Ctrl-B, then D
```

정상 중단은 attach 뒤 `Ctrl-C`를 **한 번** 누르는 것이다. 그러면 기존 `SIGINT → native finalize/official backup → evidence archive` 흐름이 이어진다. `tmux kill-session`은 finalize·archive를 건너뛸 수 있으므로 정상 중단법으로 사용하지 않는다. tmux가 없으면 `--tmux`는 exit 2로 거부하며 bootstrap은 설치하지 않고 경고만 출력한다.

개인 NVIDIA/Brev도 같은 wrapper를 사용한다. train 뒤 evidence·archive·personal GitHub Release까지 같은 session 안에서 끝나며 official에서는 외부 publish가 발생하지 않는다.

짧은 smoke 또는 디버깅은 official에서 `./scripts/issacsimz_train.sh ...`를 foreground로 사용해도 된다. personal에서는 이 wrapper가 archive 생성 후 Release 게시를 시도하므로, 게시 없는 smoke는 `./issacsimz train ...` 직접 CLI로 실행한다. official mode의 GitHub 차단 규칙은 tmux 사용 여부와 무관하게 그대로 적용된다.

## v1.1 안전성·증거 판정

- 첫 `Ctrl+C`는 학습 process group에 SIGINT를 한 번만 전달한 뒤 stdout을 계속 소비하면서 `train.py`가 자체 finalize·공식 backup을 끝낼 때까지 기다린다. 자동 30초 kill은 없다. official에서는 추가 `Ctrl+C`도 강제 종료로 전환하지 않는다. personal에서만 두 번째 `Ctrl+C`에 SIGTERM→10초 대기→SIGKILL fallback이 있으며 `forced_stop`과 finalize 불완전을 metadata에 남긴다.
- `NO_AUTO_SUBMIT` 또는 `SUBMIT_DEBUG`가 환경에 **존재**하는 profile `train`은 기본 거부한다. 공식 finalizer와 똑같이 값이 `0`이어도 활성 상태다. 개인 서버에서 의도한 경우만 각각 `--allow-no-auto-submit`, `--allow-submit-debug`를 명시한다.
- metadata는 `training_status`, `official_finalize_status`, `official_backup_status`, `evidence_validation`을 분리한다. finalize는 `not_started`, `started`, `completed`, `incomplete`; backup은 `success`, `skipped_disabled`, `skipped_no_config`, `skipped_missing_artifacts`, `failed`, `unknown`이다. `/workspace/submit_config.txt` 또는 `SUBMIT_HOST`+`SUBMIT_TOKEN`이 존재하면 backup expected다. 환경변수의 값은 저장하지 않는다. expected인데 `success`가 아니면 validation은 FAIL이다.
- profile train은 필수 train/play/reward/finalize/config와 task root 아래 전체 Python source의 시작·종료 SHA-256을 `source/identity.json`에 기록한다. 동적 output/cache 경로는 제외하고 실제 `hashed_paths`를 함께 남긴다. 파일 수정·삭제·추가가 있으면 validation FAIL이다. native run·TensorBoard·checkpoint·수집 파일은 PASS/WARN/FAIL을 별도 `validation.json`에 남긴다.
- 완료된 profile train의 PASS에는 native TensorBoard event, 이번 run의 `NEW`/`MODIFIED` `model_best.pt`와 `env.yaml`, finalize 완료가 필요하다. personal은 mirror checkpoint 1개 이상, official은 범용 mirror 대신 organizer keeper 정상 종료와 보존 checkpoint 1개 이상을 확인한다. child exit 0이어도 evidence validation은 FAIL일 수 있으므로 둘을 모두 확인한다.
- personal watcher는 시작 전 run-root directory snapshot에 없던 새 run만 잡고 `[POST] 학습 종료`를 읽는 즉시 동기 final scan을 수행한다. 원본 checkpoint는 이동·삭제하지 않으며 이미 보존한 size/mtime이 같으면 SHA-256 재계산도 하지 않는다. official은 범용 watcher 대신 run별 organizer keep-all 셸을 시작하고, 종료 후 native run·backup checkpoint를 일회성으로 evidence에 수집한다.
- robot profile당 PID lock 하나만 허용한다. live PID는 절대 덮어쓰지 않고 stale PID만 명시적 `--force-unlock`으로 정리한다.
- `submit_config.txt`, `.env`, credential/secret/token 파일과 private key는 broad collect/native copy에서 제외한다. source snapshot은 정적 source만 수집하고, Python source fingerprint는 동적 output/cache를 제외한 task root의 `.py` 목록을 manifest에 기록한다.
- evidence 확인이 필요하면 `issacsimz verify <archive>.tar.gz --require-sidecar`로 archive 자체 hash와 내부 `SHA256SUMS`를 추출 없이 확인한다. `issacsimz runs list/show`는 evidence metadata·validation을 조회한다. resume의 실제 optimizer/state 로드는 기존 native `train.py`가 수행한다. resume evidence에는 parent run, source checkpoint와 SHA-256, 시작·최종 iteration, 실제 command, reward/config source identity가 남는다. play는 personal에서 `play h1|go2 --checkpoint <path>`, official에서 `play h1|go2 --from-run <OFFICIAL_TRAIN_RUN> --checkpoint <path>`로 별도 evidence run에 기록한다. OFFICIAL 서버 종료는 AI가 수행하지 않는다.

OFFICIAL indexed numbered checkpoint resume에서는 서로 다른 세 식별자를 섞지 않는다: `--from-run`은 source **evidence Run ID**, `--load-run`은 그 evidence의 `metadata.native_run` **디렉터리 이름**, `--checkpoint`는 `checkpoint_index.json`에서 확인한 `model_N.pt`의 실제 **source_path**다. 우선 실제 evidence root의 `metadata.json`, manifest가 보호하는 `checkpoint_index.json`에서 `source_path`·`origin`·SHA-256·size를 읽고 파일 존재와 동일성을 확인한다. `organizer_checkpoints/` 보존 사본이나 `metadata.native_run`만 보고 checkpoint 위치를 추정하지 않는다. `--checkpoint`에 검증된 keeper 절대경로를 입력해도 sidecar가 출처를 검사한 뒤 native `train.py`에는 basename 패턴 `model_N.pt`만 전달한다. native run에 해당 파일이 없을 때는 sidecar가 **그 source evidence의 원래 native run 디렉터리**에만 검증된 동일 바이트를 복원하며, 다른 파일을 덮어쓰거나 원본 keeper를 지우지 않는다. 이 indexed 경로에는 index에 기록된 numbered checkpoint만 쓰고 `model_best.pt`는 play/export 용도로 구분한다. 부모 evidence가 없는 단일 파일 import는 아래 별도 분기를 따른다.

실행 전에는 같은 인자에 `--preflight-only`를 붙여 **학습·복원 없이** 검증할 수 있다. 셸 tmux wrapper와 portable CLI의 `train --tmux` 모두 세션 생성 전에 이 검사를 자동 수행한다. tmux wrapper 자체에는 `--preflight-only`를 전달하지 않는다. 세션이 곧바로 종료되거나 새 native Run이 없으면 경로·CWD를 추측하거나 tmux를 반복하지 말고 preflight/foreground 오류부터 확인한다. 예: `./scripts/issacsimz_train.sh go2 --iters 5000 --envs 4096 --name <name> --from-run <evidence-id> --load-run <native-run-name> --checkpoint <index-source_path> --preflight-only`. PASS 뒤에는 같은 인자에서 `--preflight-only`만 빼고 tmux wrapper로 실행한다. 개인/공식 source checkpoint를 섞지 않는다.

### OFFICIAL 학습 시작·재개 표준 절차

**2026-10-12 문서에 기록된 후속 기능 검증 기준은 `issacsimz` commit `b779fb9`**다. 로컬 WSL CPU 회귀 테스트 136개와 portable build를 통과했다. 위 `bea81fa`의 129개 결과는 과거 버전의 별도 테스트이고, 둘을 같은 commit의 검증으로 합치지 않는다. Codeberg 원격 HEAD·실제 배포된 서버 checkout의 현재 commit은 이 문서만으로 확인되지 않는다. 실제 OFFICIAL GPU resume를 새로 실행한 검증도 아니다.

H1·Go2 모두 같은 순서를 사용한다: **실제 Codeberg checkout 확인 → official bootstrap·doctor·READY → 승인된 reward 확인 → 입력 유형 선택 → preflight → 같은 인자의 tmux wrapper**. 서버 setup/부팅만으로 checkout·bootstrap 완료를 가정하지 않는다. 위 numbered/index 설명은 기존 부모 evidence가 있는 **indexed resume** 경로다.

- Fresh: resume 입력 없이 `issacsimz_tmux_train.sh h1|go2 ...`를 쓴다.
- Indexed resume: 실제 evidence root와 부모 Run·index를 확인하고 `--from-run` 및 검증된 `--checkpoint <source_path>`를 쓴다. `--load-run`은 원래 native 디렉터리 이름이며 생략하면 sidecar가 도출한다.
- 단일 native `.pt`만 있는 새 서버: **`--import-checkpoint <실제 파일 경로>`**를 쓴다. `--from-run`, `--load-run`, `--checkpoint`와 혼용하지 않는다. sidecar가 파일 SHA 기반 `issacsimz-import-<SHA prefix>` native 입력 폴더와 동일 바이트 사본을 준비하고 공식 loader로 재개한다. 원본은 보존하며 충돌 파일을 덮어쓰지 않는다. `policy.pt` 같은 export 정책은 resume checkpoint가 아니다.

다음은 값만 채우는 표준 카드다. 실행 요청과 실제 경로 확인 없이 이 예시를 그대로 실행하지 않는다. Go2는 `ROBOT=go2`로 바꾼다. reward를 baseline으로 임의 복원하거나 native `tmux ... train.py`로 우회하지 않는다.

```bash
cd /workspace/issacsimz || exit 1
ROBOT=h1
ITERS=2000
ENVS=4096
SEED=42
NAME=your-run-name
MODEL=/workspace/REPLACE_WITH_VERIFIED_NATIVE_MODEL_N.pt
# 반드시 위 값을 실제 native .pt 경로로 교체한다. 예시 파일이 그대로면 중단.
case "$MODEL" in *REPLACE_WITH_VERIFIED_NATIVE_MODEL_N.pt) echo 'Set MODEL to a verified native checkpoint' >&2; exit 2;; esac
test -f "$MODEL" || { echo "Missing input: $MODEL" >&2; exit 2; }
./issacsimz reward show "$ROBOT"
./issacsimz reward diff "$ROBOT"
ARGS=("$ROBOT" --iters "$ITERS" --envs "$ENVS" --seed "$SEED" --name "$NAME"
      --import-checkpoint "$MODEL")
./scripts/issacsimz_train.sh "${ARGS[@]}" --preflight-only &&
./scripts/issacsimz_tmux_train.sh "${ARGS[@]}"
```

Preflight는 파일·목적지 충돌을 확인할 뿐 checkpoint를 deserialize하거나 로봇 state 호환성을 보증하지 않는다. 그 부분은 기존 native loader가 검사한다. `--iters`는 native `--max_iterations`로 그대로 전달되므로 실제 설치 runner의 resume 의미를 확인하고 마지막 checkpoint 번호를 미리 단정하지 않는다. 알려진 로컬 RSL runner는 resume 지점에서 N회 추가하지만 원격 설치 버전을 확인한 것으로 표현하지 않는다.

단일 파일의 path·SHA는 기록하되 부모 Run ID를 만들어내지 않고 `source_run_mode=unknown`, `source_checkpoint_origin=user_imported_checkpoint`, `source_provenance_verified=false`로 남긴다. **현재 학습이 OFFICIAL 서버에서 실행됐다는 것과 부모가 공식 출처라는 증명은 별개**다. 미검증 import 계보의 OFFICIAL sidecar play/export 및 indexed resume는 차단된다. 제출 계보가 필요하면 원래 부모 evidence/index로 verified 경로를 사용하며 metadata를 임의 편집해 승격하지 않는다. 기존 keeper·50회 저장·자동 evidence/archive 흐름은 유지한다.

명령 생성 시 이 카드와 현재 `issacsimz` README/CLI를 기준으로 하고, 없는 부모 evidence를 요구하다 native 학습으로 우회하거나 가짜 `load_run` 이름·수동 복사를 지시하지 않는다. 오류가 나면 foreground preflight 출력부터 확인한다. OFFICIAL은 공개 Codeberg 준비만 허용하고 GitHub와 상호작용하지 않으며 AI가 서버를 종료하지 않는다.

`doctor --robot h1|go2`는 Python, `nvidia-smi`, evidence 경로, task root, `train.py`, Isaac Lab launcher와 위험 환경변수를 확인한다. 화면이 FAIL이면 exit code도 반드시 non-zero다. GPU가 없더라도 generic 기록은 가능하지만 실제 profile smoke 전에는 별도 문제로 다룬다.

## Reward 수정은 학습과 분리

### 초기 baseline과 제출 preset을 혼동하지 않기

**새로 제공된 OFFICIAL 서버의 초기 reward는 운영진 baseline이다.** `h1-submit-2` 등 frozen preset은 비교·목표 설정이지 초기 서버 상태가 아니다. clone/pull·bootstrap·doctor·checkpoint import가 preset을 적용했다고 가정하지 않는다. 재접속·재부팅한 기존 서버에는 이전 변경이 남을 수 있다. H1·Go2 모두 먼저 `reward show`로 실제 활성 weight 전체를 읽고, 목표 resolved config와 다른 항목을 모두 적용한 뒤 다시 확인한다. `reward diff`는 sidecar가 보존한 수정 전 원본과의 차이이며 submission preset과의 비교 결과라고 간주하지 않는다.

예: **H1 목표가 `h1-submit-2 + action_rate_l2=-0.0001 + feet_air_time=0.25`**라면 제공 baseline의 `termination_penalty=-5`도 목표값 `-50`으로 바꿔야 한다. action·feet 두 줄만 적용하면 목표 설정이 아니다. 현재값이 제공 baseline임을 확인한 경우의 변경은 다음과 같다(이 조합 자체를 기본 추천하지는 않는다).

```bash
./issacsimz reward show h1
./issacsimz reward diff h1
# 현재 전체 reward와 목표를 대조한 뒤 필요한 차이를 모두 적용
./issacsimz reward set h1 termination_penalty -50
./issacsimz reward set h1 action_rate_l2 -0.0001
./issacsimz reward set h1 feet_air_time 0.25
./issacsimz reward show h1
./issacsimz reward diff h1
```

목표의 나머지 활성 weight도 실제값과 일치해야 학습을 시작한다. `fresh`/`resume`은 checkpoint 로딩 방식이지 reward 초기화 방식이 아니다. 이미 수정된 서버를 baseline으로 임의 restore하지 말고 현재값에서 승인된 목표값으로 맞춘다.

`reward`는 참가자 reward 파일을 import하거나 실행하지 않는 텍스트 기반 명령이다. Go2의 `quadruped_rewards.py`, H1의 `humanoid_rewards.py` 중 resolve된 task root 아래의 파일 하나만 대상으로 하며, allowlist의 reward key만 정확히 한 번 발견될 때 수정한다. 학습 명령·`issacsimz` shell wrapper·공식 `train.py`·`_finalize.py`는 수정하지 않는다.

```bash
./issacsimz reward show go2
./issacsimz reward set go2 track_lin_vel_xy_exp 1.25
./issacsimz reward diff go2
./scripts/issacsimz_train.sh go2 --iters 1000 --envs 4096 --name go2-lintrack125-screening
```

위 `--name`은 `LINTRACK-125`의 설명용 예시다. legacy G-001/G2 표기는 원문·registry 검색에 필요할 때만 확인하고, 실제 실행 전 새 Run 번호와 비교 조건을 기록한다. 첫 `set` 전 원본은 task 폴더 밖 `~/.issacsimz/reward-state/`에 byte-for-byte 보존된다. `diff`로 baseline 대비 변경을 확인한다. 숫자를 주면 주석 reward도 활성화할 수 있고, `off`는 활성 entry를 주석 처리한다. 허용되지 않은 key, 0개·2개 이상 매치, `nan`/`inf`, 그리고 마지막 관리 수정 뒤 수동으로 바뀐 파일은 수정·restore 모두 거부한다.

다음 실험 전 baseline으로 돌아갈 때만 아래를 쓴다. 이 명령은 마지막 issacsimz 관리 hash와 현재 파일이 같을 때만 원본을 복원하므로, 수동 수정 내용을 덮어쓰지 않는다.

```bash
./issacsimz reward restore go2
```

## 판정 뒤 영상 실행

학습·evidence 판정 후 영상이 필요한 경우 [17번 영상 운영 문서](<17_ISSACSIMZ_VIDEO_OPERATIONS.md>)를 따른다. **OFFICIAL 6영상 요청을 PERSONAL 서버로 돌리라고 하지 않는다.** 공식 서버에서 `issacsimz_video_suite.sh`와 GitHub 게시만 차단되며, 공식 `play.py`를 지형별로 직접 실행해 6영상을 만들 수 있다. OFFICIAL numbered checkpoint의 sidecar `play` 명령을 줄 때는 실제 evidence root를 `--log-root`에 넣고, `checkpoint_index.json`의 `source_path`·origin·SHA와 실제 파일을 확인한다. `organizer_checkpoints/`나 `metadata.native_run`에서 checkpoint 경로를 추측하지 않는다.

## H1·Go2 경로를 자동으로 잡는 smoke/baseline

`train`은 task root와 native run root를 로봇별로 자동 결정한다. personal은 이 run root를 checkpoint watcher에도 사용하고 official은 run별 organizer keeper의 대상 결정과 종료 후 evidence 수집에 사용한다. 실제 경로는 반드시 task working directory 아래다.

```text
H1:  /workspace/training/humanoid/logs/rsl_rl/humanoid/
Go2: /workspace/training/quadruped/logs/rsl_rl/quadruped/
```

official의 1-iteration 명령은 아래 실전 runbook에 한 번만 적는다. personal의 게시 없는 smoke는 `./issacsimz train <robot> --iters 1 --num-envs 64 --name <name>`을 사용한다. personal wrapper는 완료·validation PASS archive에만 publisher를 시도한다. 실패·중단 archive는 로컬 evidence/handoff에 보존한다.

personal의 비표준 배치라면 `--task-root`, `--isaaclab-root`을 명시한다. 명시 경로가 잘못되면 default로 fallback하지 않고 즉시 실패한다. official에서는 운영진 제공 기본 root 밖 override를 거부한다. native run을 찾지 못하면 CLI가 warning과 metadata를 남긴다. personal에서 checkpoint mirror가 없으면 validation 결함이지만, official archive에 범용 mirror가 없는 것은 의도된 정상 상태다. official은 native TensorBoard와 fresh export/finalize 조건으로 판정한다.

실제 baseline도 동일하게 쓴다.

```bash
./scripts/issacsimz_train.sh h1 --iters 5000 --envs 4096 --name h1-baseline-5k
./scripts/issacsimz_train.sh go2 --iters 5000 --envs 4096 --name go2-baseline-5k
```

## 다른 기존 학습 명령을 감싸기

```bash
./issacsimz run \
  --name h1-smoke \
  --workdir <개인-task-폴더> \
  --run-root <새 native run이 생기는 부모 폴더> \
  --collect <학습 뒤 수집할 exported-폴더> \
  -- <개인 서버의 기존 native 학습 명령>
```

이 범용 `run` 예시는 **personal-only**다. official에서는 명령 실행 전에 거부한다. `--` 뒤에는 기존 `isaaclab.sh -p train.py ...` 명령을 바꾸지 않고 넣는다. `--run-root`에는 동시에 하나의 학습만 새 run을 만드는 디렉터리를 지정한다. personal에서 동시 실행이 있거나 이미 정확한 native run 경로를 안다면 독립 watcher를 쓸 수 있다. official mode의 독립 `watch`도 안전상 거부된다.

```bash
./issacsimz watch \
  --run-dir <정확한-native-run-폴더> \
  --destination <별도-evidence-checkpoints-폴더> \
  --all
```

personal의 `model_*.pt`는 크기가 안정된 뒤 `.part` 임시 파일을 거쳐 SHA-256 검증 후 복사된다. source checkpoint는 절대 변경하지 않는다. 이 범용 watcher는 official에서 사용하지 않는다.

## 남는 evidence와 archive

### 2026-09-21 P2 무결성 기준

evidence directory는 archive를 만들기 전에 `metadata.json`, `validation.json`, `SHA256SUMS`까지 완전히 finalize한다. tar 생성 뒤에는 evidence 본체를 다시 수정하지 않는다. 따라서 archive 내부 `metadata.json`과 loose evidence의 동일 파일 SHA-256이 같고, archive 내부 `SHA256SUMS`와 loose evidence의 내용도 같아야 한다. `archive_bytes`, `pack_duration_sec` 같은 압축 작업 자체의 정보는 evidence metadata가 아니라 형제 `<archive>.metadata.json`에만 기록한다.

train validation 정책은 `PASS/WARN → evidence + archive + 가능한 loose artifact`, `FAIL → evidence + archive only`다. FAIL evidence와 archive는 진단 근거이므로 삭제하지 않지만, `model_best.pt`, `env.yaml`, `report.html`처럼 제출 성공물로 오해할 수 있는 loose handoff는 만들지 않는다. download handoff에는 archive와 `.sha256`뿐 아니라 `.metadata.json`도 함께 둔다.

official train/play/video에서 CLI 사용자가 직접 지정한 `--collect`는 실행 전에 거부한다. task profile이 내부적으로 수집하는 `exported/`, native run, TensorBoard는 이 제한의 대상이 아니며 계속 수집한다. personal의 명시적 `--collect`는 기존대로 허용한다.

official checkpoint index는 `exists`, regular file, non-symlink, `size > 0`, SHA-256 계산 가능, 승인 root containment를 모두 만족해야 한다. resolved path가 해당 native run 또는 승인된 `backup_log` 밖이면 official provenance로 index하지 않는다.

source identity schema 2는 고정된 핵심 파일 목록에 더해 task root 아래 실행에 영향을 줄 수 있는 모든 `.py`를 fingerprint한다. `logs/`, `exported/`, `__pycache__/`, `.git/`, evidence/download, `backup_log` 등 동적 디렉터리는 제외하며 `hashed_paths`와 `after_hashed_paths`로 검사 범위를 manifest에 명시한다. 실행 중 기존 파일 수정·삭제 또는 새 Python 파일 추가도 before/after 비교에서 변경으로 잡는다.

공개 tree 검사와 portable build는 Git checkout과 `.git` 없는 ZIP source 모두에서 동작해야 한다. checkout에서는 `git ls-files`, ZIP에서는 generated/cache 경로를 제외한 filesystem walk를 사용하며, 금지된 파일명이나 텍스트는 어느 배포 형태에서도 동일하게 실패한다.

각 `run`은 다음을 만든다.

```text
metadata.json
command.txt
console.log
system/runtime.txt
system/nvidia_smi_before.txt
system/nvidia_smi_during.csv  # personal only
system/nvidia_smi_after.txt
native_run/
checkpoints/                  # personal only
collected/
source/identity.json
validation.json
watcher.log                   # personal only
SHA256SUMS
```

성공은 `<run-id>.tar.gz`, 실패는 `<run-id>_FAILED.tar.gz`, 중단은 `<run-id>_INTERRUPTED.tar.gz`로 기본 archive된다. archive 자체의 `.sha256`과 pack 시간·evidence bytes·archive bytes가 든 `.metadata.json` sidecar도 함께 생성된다. 압축 전 evidence 크기와 안전 여유분보다 free space가 적으면 archive를 만들지 않는다. 수동 재압축은 다음과 같다.

```bash
./issacsimz pack <run-id>
```

같은 archive가 있으면 덮어쓰지 않는다. 확인 후 정말 교체할 때만 `pack <run-id> --force`를 쓴다. run ID에는 단일 evidence 디렉터리 이름만 허용되어 absolute path와 `../` traversal을 거부한다.

archive를 다운로드하고 hash를 확인한 뒤에도 OFFICIAL 서버 종료는 AI가 수행하지 않는다. archive 생성 뒤 evidence 원본이나 native run을 삭제하지 않는다.

`--collect` 폴더는 실행 전과 후의 size·mtime·SHA-256을 비교한다. `NEW`·`MODIFIED`만 archive에 복사하고, 이전 run의 `policy.pt`, MP4, `model_best.pt`처럼 `UNCHANGED`인 파일은 `collected/provenance.json`에만 기록한다. 따라서 stale output을 이번 실행 산출물로 해석하지 않는다.

## 탐색기용 download handoff

archive 생성 뒤 `train`은 canonical evidence와 `exported/`를 바꾸지 않은 채 작은 다운로드 복사본을 만든다. 기본 위치는 mode별로 다음과 같고, `ISSACSIMZ_DOWNLOAD_ROOT`가 있으면 그 경로를 우선한다.

```text
personal: /home/shadeform/ISSACSIMZ_DOWNLOAD/<RUN_ID>/
official: /workspace/ISSACSIMZ_DOWNLOAD/<RUN_ID>/

같은 root:
<RUN_ID>-download.tar.gz
<RUN_ID>-download.tar.gz.sha256
```

train handoff에는 가능한 경우 evidence `.tar.gz`, 같은 파일명의 `.tar.gz.sha256`·`.tar.gz.metadata.json`을 `copy2`로 넣는다. validation이 `PASS` 또는 `WARN`일 때만 `model_best.pt`, `env.yaml`, `report.html` 같은 loose artifact도 추가한다. validation `FAIL`이면 실패·중단 evidence와 archive sidecar까지만 복사하고 제출 성공물처럼 보이는 loose artifact는 배포하지 않는다. console·TensorBoard·checkpoint 전체는 archive 안의 canonical evidence에만 남겨 중복을 만들지 않는다. archive 이름은 바꾸지 않으므로 sidecar도 그대로 유효하다. missing optional file이나 handoff 복사 오류는 native finalize/evidence 결과를 실패로 바꾸지 않는다.

train handoff를 만든 직후 현재 `<RUN_ID>/` 전체를 형제 `<RUN_ID>-download.tar.gz`로 감싸고 다운로드 bundle 자체의 `.sha256`을 새로 생성한다. 압축 안에는 `<RUN_ID>/` 하나만 최상위로 두며, handoff 폴더에 이미 있는 `videos/` 같은 중첩 사용자 산출물도 그대로 포함한다. 원래 `<RUN_ID>/`는 삭제하지 않는다. 성공한 video가 parent train handoff를 갱신하면 같은 bundle과 sidecar를 임시 파일에서 다시 만들어 교체한다. bundle 생성 오류는 경고로 남고 native finalize/evidence 결과를 바꾸지 않는다.

성공(`validation=PASS`)한 label 없는 `video`는 parent train run의 같은 handoff 폴더에 fresh `play_video.mp4`를 추가한다. `--label`이 있으면 `videos/<label>.mp4`로 복사해 기존 `play_video.mp4`와 앞선 label 영상을 덮어쓰지 않는다. 각 성공 뒤 download bundle이 다시 만들어지므로 마지막 suite video 뒤에는 현재 여섯 영상이 모두 포함된다. handoff root의 `LATEST.txt`에는 가장 최근에 갱신한 train run ID 한 줄만 쓴다. official mode는 이 로컬 copy만 만들며 `gh`, GitHub API, push, Release를 호출하지 않는다. personal mode의 기존 Release publisher는 그대로 별도 동작한다. server 종료 전 검증과 장기 보존은 handoff가 아니라 canonical archive/evidence를 기준으로 한다.

## baseline 전 smoke

아래 official 1-iteration 명령은 학습 시작·종료, exit status, 치명 오류, console/native run/TensorBoard 및 archive·handoff 존재를 확인한다. official에서 주기 sampler·범용 watcher 파일이 없는 것은 정상이다. archive 생성 과정의 검증 결과를 보고, 별도 전체 SHA 재검증은 손상·동일성 의문이 있을 때만 한다. smoke로 reward·성능을 판단하지 않는다.

## 공식 서버 실전 runbook

위 **OFFICIAL 첫 접속/재접속 카드**로 Codeberg checkout과 bootstrap을 준비하고, 두 profile doctor·`READY`를 확인한다. GitHub에는 접속하지 않고 공식 task source를 덮어쓰지 않는다. checkout 동일성이나 손상이 실제 의문일 때만 필요한 파일을 검증하며 `NO_AUTO_SUBMIT`·`SUBMIT_DEBUG` guard를 우회하지 않는다.

기본 공식 배치가 다음과 같을 때는 task path를 별도로 쓸 필요가 없다.

```text
H1 task:  /workspace/training/humanoid
H1 runs:  /workspace/training/humanoid/logs/rsl_rl/humanoid/
Go2 task: /workspace/training/quadruped
Go2 runs: /workspace/training/quadruped/logs/rsl_rl/quadruped/
```

먼저 H1·Go2를 각각 1 iteration으로 실행한다.

```bash
./scripts/issacsimz_train.sh h1 \
  --iters 1 --envs 64 --name smoke-h1

./scripts/issacsimz_train.sh go2 \
  --iters 1 --envs 64 --name smoke-go2
```

official의 task root는 운영진 제공 `/workspace/training/humanoid` 또는 `/workspace/training/quadruped`로 고정된다. 실제 경로가 다르면 `--task-root`로 우회하지 말고 실행을 중단해 배치와 최신 지침을 확인한다. official에서는 `watcher.log`가 생성되지 않는다. CLI 출력에 아래 warning이 있으면 종료 후 새 native run을 식별하지 못한 것이므로 baseline을 시작하지 않고 배치·run 탐색 상태를 먼저 확인한다.

```text
WARNING native run was not detected under ...
```

경고가 없으면 run evidence에서 `native_run/`, TensorBoard event, `collected/provenance.json`, 실행 전·후 GPU snapshot, `SHA256SUMS`와 `exports/*.tar.gz`를 확인한다. official에서는 `checkpoints/`, `watcher.log`, `system/nvidia_smi_during.csv`가 없는 것이 정상이다. 그 뒤에만 baseline을 실행한다.

```bash
./scripts/issacsimz_tmux_train.sh go2 \
  --iters 5000 --envs 4096 --name go2-b0

cd ~/issacsimz-evidence/exports
sha256sum *.tar.gz
cat *.tar.gz.sha256
```

## Personal NVIDIA/Brev automatic Release mirror

This is a **personal NVIDIA/Brev-only** convenience backup. `issacsimz` Python core remains a public, shared evidence sidecar and never calls GitHub itself. The current personal orchestration is Codeberg's explicit mode-aware shell layer; the older NVIDIA-only wrapper is compatibility history. Never use personal publishing wrappers on the official competition server.

개인 Brev VM은 위 **PERSONAL 첫 접속/재접속 카드**를 따른다. bootstrap이 GitHub 인증, private NVIDIA checkout clone/pull, repository-local tag identity(`ncrcissacsimz@users.noreply.github.com`), runner·두 doctor·`READY`를 처리한다. pull이 fast-forward되지 않으면 reset하지 말고 확인한다. Release 없는 짧은 smoke는 `./issacsimz train h1 --iters 1 --num-envs 64 --name h1-smoke`처럼 직접 CLI로 실행한다. 본학습 wrapper는 완료·validation PASS인 결과에만 publisher를 시도하므로 smoke 기본 명령이 아니다.

Thereafter, use the short mode-aware command:

```bash
./scripts/issacsimz_train.sh go2 \
  --iters 5000 --num-envs 4096 --name go2-baseline-5k
```

Personal mode invokes the separate publisher only for completed training with evidence validation PASS. The publisher independently requires `issacsimz verify --require-sidecar --publishable`, uploads `.tar.gz`, `.tar.gz.sha256`, and `.tar.gz.metadata.json` to `SE3C/naver-issacsim-nvidia` Releases, and checks remote asset size and SHA-256 after upload. Failed or interrupted archives remain local and retain their original non-zero exit code; direct publishing of those archives is rejected. The publisher first pushes an annotated tag targeting the personal checkout commit and refuses an existing Release or conflicting tag. If private environment variables `NO_AUTO_SUBMIT` or `SUBMIT_DEBUG` intentionally exist, explicitly append their matching allow flag.

PERSONAL 본학습 wrapper와 자동 6영상 suite에는 선택적으로 `--release-experiment exp-h1-...|exp-go2-...`와 `--release-config 'h1-submit-N + key=value'|'g2-submit-N + key=value'`를 **둘 다** 전달할 수 있다. 예를 들어 Go2는 `--release-experiment exp-go2-gait-stability --release-config 'g2-submit-3 + feet=0.03'`이다. CLI 로봇명과 tag에는 `go2`를 쓰지만 Go2 제출 preset의 canonical 약자는 `g2`다. 이 값은 Release tag/title/notes의 표시 정보일 뿐 evidence run ID, reward, checkpoint 선택이나 원본 archive 이름을 바꾸지 않는다. 자동 영상 suite에서만 이 이름 지정 옵션을 사용하며 `--no-publish`·수동 `--publish`와 섞지 않는다. 옵션을 생략하면 기존 자동 Release 이름을 유지한다. OFFICIAL에는 이 PERSONAL 게시 옵션을 사용하지 않는다.

OFFICIAL은 위 bootstrap·train 카드의 같은 wrapper를 쓰되 GitHub와 상호작용하지 않으며 `SUBMIT_HOST`/`SUBMIT_TOKEN`은 native 공식 흐름에만 맡긴다.

개인 Release의 tag 정렬·보존 규칙은 sidecar evidence와 별도다. 미래 Release는 UI/`gh release create`가 새 lightweight tag를 만들게 두지 않는다. 개인 NVIDIA checkout의 현재 commit에 로컬 annotated tag를 먼저 만들고 push한 뒤 그 기존 tag를 Release에 연결한다. 6-terrain suite와 일반 train/video publisher가 이 순서를 사용하며, Release 생성이 실패했다면 checkout HEAD가 동일할 때만 기존 annotated tag를 재사용한다. 기존 Release/tag/asset은 순서만을 이유로 재생성하지 않는다.

성공한 bootstrap은 `~/issacsimz-server-manifest/`에 환경·코드 commit·doctor 결과를 남기되 token·private key·제출 credential은 기록하지 않는다. `.git`이 없는 배포본은 `git metadata unavailable`로 표시하고 계속한다.

NVIDIA Releases mirror PERSONAL server training and native video. From 2026-10-12, new Windows PC combined video/evaluation Releases belong in private `naver-issacsim-eval`; retain historical NVIDIA links. Do not change the shared train/video publisher repo setting to redirect PC artifacts. Retain canonical private raw under `naver-issacsim-originals/data/raw/private_server_runs/`. Never include credentials, tokens, `submit_config.txt`, or `.env` in an archive or Release.

성공·실패와 관계없이 archive를 로컬로 다운로드하고 SHA-256을 확인한다. 작업 완료와 무관하게 OFFICIAL 서버 종료는 AI가 수행하지 않으며, PERSONAL 서버 종료만 사용자의 별도 명시 요청을 따른다.

## H1 재실험 실행 전 계보 확인 — 2026-09-21

과거 H-005~H-011의 부모 계보와 새 corrected-lineage Run을 분리한다. `issacsimz` evidence의 실제 parent checkpoint와 설정을 확인하며 이름만으로 provenance를 추정하지 않는다. 계보 상세〔원본 참조: `14_H1_NEXT_RUN_PARAMETER_COMPARISON.md` / 공개 사본 미포함〕.

## 운영진 영상 진단 팁과 CLI 경계

운영진 `play.py` 영상 팁의 재사용할 요점은 [17번 영상 운영 문서](<17_ISSACSIMZ_VIDEO_OPERATIONS.md>), 원문과 전달본 분석은 외부 분석 자료〔원본 참조: `../external_analysis/2026-09-23_ORGANIZER_DAILY_HONEY_TIPS_SOURCE_AND_NOTES.md` / 공개 사본 미포함〕에 둔다. 공식 팁은 `issacsimz` official CLI의 native `--extra` 제한을 바꾸는 근거가 아니다.
