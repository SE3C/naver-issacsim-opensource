# PERSONAL 로컬 전용 resume 설정 — A6000 준비 및 L40S 재사용

2026-10-18 설정 보존 기록이다. 실행 환경은 PERSONAL이며 OFFICIAL로 바꾸지 않는다.
사용자는 A6000에서 6순위 학습을 시작했으나 iteration 시간이 길어 L40S로 전환할 예정이라고 알렸다.
완료·중단 여부와 실제 Run ID는 아직 수신하지 않았다. 이 기록을 위해 서버나 학습을 중지하지 않았다.
L40S는 아직 접속·준비·실행하지 않았다.

## 고정한 source와 경로

| 항목 | 확인한 값 |
| --- | --- |
| 기존 Brev 인스턴스 | `a6000-ncrc` / RTX A6000 48 GB |
| sidecar | `/ephemeral/issacsimz` |
| sidecar source | Codeberg `passerby1/issacsimz`, commit `b01a3971b3e709a2aa6e20dd9bf32ffe6afe7f1e` |
| native task source | `naver-issacsim-nvidia` commit `7ed0ea9b5ca917074994466c8e60fb09c8bbfc88` 의 tracked `training/` |
| 전송된 task root | `/home/shadeform/naver-training/training/humanoid`, `.../quadruped` |
| IsaacLab | `/home/shadeform/IsaacLab` |
| evidence | `/home/shadeform/issacsimz-evidence` |
| bootstrap state | `/ephemeral/issacsimz/.issacsimz-mode.env` (`0600`) |

학습 코드는 개인 PC에서 SSH로 전송했다. 서버에서 GitHub 인증·clone·pull·API·게시를 하지 않았다.
전송에는 `.git`, credential, `submit_config.txt`, 기존 학습 산출물을 포함하지 않았다.
전송 archive SHA-256: `7f41f46a97acac098efcfe22676925f38706055d1023073967cc6252bb2f8ec3`.

## 재사용하는 bootstrap

L40S의 기본 Isaac Sim/Lab 설치와 위 tracked task source 배치를 먼저 확인한다.
아래는 A6000에서 확인한 경로다. 새 서버에서도 확인 없이 존재한다고 가정하지 않는다.
sidecar 최초 clone은 공개 Codeberg에서 하고, 기존 checkout은 변경 사항을 보존하며 fast-forward 갱신한다.

```bash
cd /ephemeral/issacsimz
ISSACSIMZ_PERSONAL_ROOT=/home/shadeform/naver-training \
ISSACSIMZ_PERSONAL_ISAACLAB_ROOT=/home/shadeform/IsaacLab \
  bash scripts/bootstrap_server.sh --mode personal --local-only
```

`--local-only`는 기존 PERSONAL 기능의 선택 경로다. GitHub 인증·task checkout 갱신·train wrapper 자동 Release 게시를 생략한다.
native 자동 업로드도 막기 위해 wrapper가 `SUBMIT_HOST`/`SUBMIT_TOKEN`을 제거하고 native loader가 읽는 checkout-root `submit_config.txt`를 거부한다.
이 설정을 위해 공식 `train.py`나 `_finalize.py`를 수정하지 않았다.
이 보장은 학습 wrapper 경로에 해당한다. 별도의 video publisher를 자동으로 실행하라는 지침은 아니다.

state가 저장되므로 매 Run마다 bootstrap을 다시 만들거나 native tmux 명령으로 우회하지 않는다.
7·8·9순위도 동일 설치를 사용하고 해당 checkpoint·reward·추가 반복 수·Run 이름만 맞춘다.

## 6순위 확인값

- 부모 Run: `20261014-081901-h1-lintrack-065-fresh5k` (기존 OFFICIAL 기록).
- 업로드 checkpoint: `/home/shadeform/model_4950.pt`.
- SHA-256: `b7528923eef5b1368ba2299f4e0538804ba00dd358049bfdff5027f448e31ece`.
- PERSONAL에서 단일 파일을 가져오므로 새 evidence의 부모 provenance는 `UNVERIFIED`로 유지한다. 기존 부모 ID를 검증된 서버 evidence인 것처럼 등록하지 않는다.
- 추가 `5050` iterations, `4096` environments, seed `42`, save interval `50`, headless.
- `--iters`는 이 native resume에서 **추가 반복 수**다. 실제 마지막 checkpoint 번호는 종료 후 확인한다.

A6000에서 기본 baseline을 확인한 뒤 아래 두 값만 바꿨다. 나머지 reward는 변경하지 않았다.

```bash
cd /ephemeral/issacsimz
./issacsimz reward set h1 track_lin_vel_xy_exp 0.65
./issacsimz reward set h1 termination_penalty -50
./issacsimz reward show h1
./issacsimz reward diff h1
```

이 명령은 baseline에서 해당 목표로 가는 delta다. 새로운 서버에 preset이 자동 적용됐다고 가정하거나, 이전 실험 변경이 남았다고 추측하지 않는다.
같은 서버에서 다른 순위를 실행할 때는 실제 현재값과 그 순위의 목표값 차이만 조정한다.

## 확인 후 사용자가 실행하는 표준 명령

```bash
cd /ephemeral/issacsimz
./scripts/issacsimz_tmux_train.sh h1 \
  --iters 5050 --envs 4096 --seed 42 \
  --name h1-top06-same-reward-to10k \
  --import-checkpoint /home/shadeform/model_4950.pt --headless
```

```bash
tmux attach -t issacsimz-h1-h1-top06-same-reward-to10k
```

tmux wrapper가 동일 인자의 preflight를 먼저 실행한다.
단일 pt import는 기존 native resume loader를 그대로 사용하고 입력 파일을 보존한다.
`--from-run`, `--load-run`, `--checkpoint`를 import와 혼합하지 않는다.

완료 시 checkpoint mirror·로그·설정·evidence의 `.tar.gz`가 생성되며 `[issacsimz] archive=...`로 위치를 확인한다.
PERSONAL checkpoint watcher는 native finalize의 중간 checkpoint 정리 전에 numbered checkpoint를 evidence에 보존한다.
GitHub 자동 게시·영상·평가·서버 종료는 이 작업에 포함되지 않는다.

## 완료한 검증과 남은 확인

- 로컬 WSL: 관련 회귀 테스트 29개, Bash 문법, `git diff --check` PASS.
- A6000: portable build 139개 테스트, H1·Go2 doctor, 6순위 preflight PASS.
- 전송 source archive와 업로드 checkpoint identity 확인 완료.
- 에이전트는 학습이나 GPU smoke를 시작하지 않았다. 이후 학습 시작은 사용자 보고이며, 결과 evidence는 아직 검증하지 않았다.
- L40S의 드라이버·Isaac Sim/Lab 버전·경로와 bootstrap/preflight는 새 서버 접속 후 별도로 확인한다. A6000 준비 성공을 L40S 검증 성공으로 간주하지 않는다.
- A6000 작업의 중단·종료·파일 삭제 또는 서버 stop은 별도 사용자 지시 없이 수행하지 않는다.
