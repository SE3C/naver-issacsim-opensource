# naver-issacsim-nvidia — H1/Go2 학습 source·개인 서버 재현

H1 humanoid and Go2 quadruped training source plus the minimal environment and
reproduction notes needed to run them with Isaac Sim / Isaac Lab.

## 저장소 역할

| 저장소 | 역할 |
| --- | --- |
| [`naver-issacsim`](https://github.com/SE3C/naver-issacsim) | 분석·문서·AI 라이브러리·실험 registry와 실제 제출 snapshot |
| [`naver-issacsim-originals`](https://github.com/SE3C/naver-issacsim-originals) | 원본 자료·대용량 에셋·공식/개인 실행의 canonical evidence 보존 |
| [`naver-issacsim-nvidia`](https://github.com/SE3C/naver-issacsim-nvidia) | H1/Go2 학습 source·개인 NVIDIA 서버 학습 및 native 영상 Release |
| [`naver-issacsim-eval`](https://github.com/SE3C/naver-issacsim-eval) | PERSONAL 사후 평가·Windows H1/Go2 실행기·새 PC 평가 Release·명시적 정책 비교 |
| [`issacsimz`](https://codeberg.org/passerby1/issacsimz) | 별도 공개 실행/evidence sidecar; 공식 학습 source를 수정하지 않음 |

## 빠른 안내

- 현재 실행 source: [CURRENT_SOURCE.md](CURRENT_SOURCE.md)
- 개인 H1 실행: [H1 runbook](docs/H1_BREV_RUNBOOK.md)
- 문서 용도별 입구: [현행 실행·역사 기록·Release 색인](docs/README.md)
- 원본/제출 배포: [Release 분류](https://github.com/SE3C/naver-issacsim/blob/main/docs/RELEASE_TAXONOMY.md)

> **현재 안내 (2026-10-14):** 아래 작업 목적별 Release 분류·배치 링크는 [Analysis PR #1](https://github.com/SE3C/naver-issacsim/pull/1)이 병합된 `main` 문서를 가리킨다. 기존 Release·학습 source 자체가 변경됐다는 뜻은 아니다.

## 자료 구조

- `training/` — H1 and Go2 task code, reward functions, train/play entry points,
  and task finalizers.
- `config/` — local workspace repository layout configuration.
- `docs/` — current personal runbook, preserved historical environment/baseline/recording notes and Release navigation; use [the index](docs/README.md) to distinguish them.
- `scripts/` — direct environment, training and recording helpers retained for
  reproducing the documented H1/Go2 runs.

This repository intentionally does not contain raw run archives, processed
analysis datasets, or a general-purpose evidence/archiving CLI. Those belong to
their respective data and tooling repositories.

`issacsimz` is the separate public, dependency-free sidecar used on both this
personal NVIDIA environment and the official environment. It launches this
repository's existing `train.py` unchanged, preserves checkpoints through the
mode-specific procedure (PERSONAL mirror; OFFICIAL organizer keeper), records
evidence, and archives it. It must not replace or edit `train.py` or a task
`_finalize.py`; the finalizer remains responsible for its native cleanup and,
where configured, official backup.

## 운영 규칙

This repository preserves its tracked task source without modification by
`issacsimz`. Do not treat personal
server observations as official competition results. Keep raw archives and
derived analysis outside this repository, and use the task-specific documents
before recreating a historical run.

## Source provenance — 실행 source의 출처

The current execution-source rule and preserved-backup comparison are recorded in [CURRENT_SOURCE.md](CURRENT_SOURCE.md).

## Release 분류와 보존

새 Release는 개인 NVIDIA 서버의 `[학습]` run archive와 `[분석]` native 영상·보조평가를 구분한다. 실행 장소가 NVIDIA여도 보조평가는 분석이다. 기존 Windows PC 평가 Release는 주소·애셋을 유지하며 [유형별 인덱스](docs/RELEASE_INDEX.md)에서 구분한다. 새 PC 통합 영상·평가는 `naver-issacsim-eval`에 게시한다. PERSONAL 결과는 공식 점수나 제출이 아니다. 공식 raw는 Originals, 제출 snapshot은 analysis에 둔다. [공통 규칙](https://github.com/SE3C/naver-issacsim/blob/main/docs/RELEASE_TAXONOMY.md)을 따른다.

## 자료 조회와 실행 판단을 분리

이 저장소의 `training/`이 **PERSONAL 현재 실행 코드**이며, 과거 보존된 `Originals/data/raw/codebase/`의 일부 수집 파일명은 실제 구현과 대응이 틀릴 수 있다. [과거 코드명 대조](https://github.com/SE3C/naver-issacsim/blob/main/data/processed/codebase/README.md)는 기록 검색용이지 training source 교체 근거가 아니다. OFFICIAL Run에서 사용된 실행 코드는 organizer-provided `/workspace/training`을 해당 evidence로 확인해야 한다. 재현 전에는 실제 checkout·source commit·task root, Run의 source/provenance 및 resolved configuration을 함께 대조한다. [실행 source 기준](CURRENT_SOURCE.md).

Experiment/Run·제출 상태의 single entry는 [Analysis registry](https://github.com/SE3C/naver-issacsim/blob/main/research/EXPERIMENTS.md)와 [preset](https://github.com/SE3C/naver-issacsim/blob/main/research/submission_presets/README.md)이다. 새 Windows PC 사후 평가 Release는 [Eval](https://github.com/SE3C/naver-issacsim-eval/blob/main/EVALUATION_RELEASES.md)로, 개인 서버 학습/native 영상 Release는 기존 NVIDIA 위치로 구분한다. 이 링크 갱신만으로 재학습·export·Release 재게시를 시작하지 않는다.

## 개인 서버 시작 순서

새 Brev VM은 먼저 `NCRC_H1_Brev_L40S_setup_script.txt`를 Brev Setup Script에 적용해 Isaac Sim/Lab 환경을 준비한다. 기존 VM이면 설치를 반복하지 않는다. 서버 shell에서 `nvidia-smi`, `gh --version`, IsaacLab의 `isaaclab.sh` 존재를 확인한다. 아래 예시는 기본 checkout 위치 `/ephemeral`을 쓴다.

```bash
# 첫 접속에서만 실행한다.
cd /ephemeral
git clone https://codeberg.org/passerby1/issacsimz.git issacsimz
```

```bash
# 재접속에서만 실행한다.
git -C /ephemeral/issacsimz pull --ff-only
```

```bash
# 두 경우 모두 이어서 실행한다.
cd /ephemeral/issacsimz
bash scripts/bootstrap_server.sh --mode personal
```

기존 checkout에 미커밋 변경이 있으면 먼저 확인하고 임의로 버리지 않는다. bootstrap은 GitHub CLI 인증 상태를 확인하고 필요하면 브라우저 로그인을 시작한다. 이어 비공개 `SE3C/naver-issacsim-nvidia`를 `/ephemeral/naver-issacsim-nvidia`에 clone하거나 기존 checkout에서 `pull --ff-only`한 뒤, Python runner·IsaacLab 경로·H1/Go2 doctor를 확인한다. `READY`가 나올 때까지 학습을 시작하지 않는다. 인증만 별도로 점검할 때는 `gh auth status --hostname github.com`을 쓴다.

bootstrap은 두 robot의 doctor를 이미 실행하며 학습은 시작하지 않는다. Release 없는 짧은 smoke는 `./issacsimz train h1 --iters 1 --num-envs 64 --name h1-smoke`처럼 직접 CLI로 실행한다. 본학습은 실험 ID·reward·iteration을 확인한 뒤 `./scripts/issacsimz_tmux_train.sh`에 로봇(`h1` 또는 `go2`), `--iters`, `--envs`, `--name`을 지정한다. PERSONAL train wrapper는 성공·실패·중단 여부와 별개로 archive가 생성되면 무결성 검증 후 NVIDIA Release 편의 복사본을 게시할 수 있으므로 실행 전에 게시 대상과 인증을 확인한다. 다운로드 handoff는 기본 `/home/shadeform/ISSACSIMZ_DOWNLOAD/<RUN_ID>/`이고 canonical raw는 `naver-issacsim-originals/data/raw/private_server_runs/`에 따로 보존한다. 공식 서버에서는 이 개인 서버 절차를 사용하지 않는다.

과거 direct helper와 설치 재현 설명은 `docs/`에 역사 기록으로 남긴다. 새 H1 실행은 [H1 runbook](docs/H1_BREV_RUNBOOK.md), Release 분류는 [공통 규칙](https://github.com/SE3C/naver-issacsim/blob/main/docs/RELEASE_TAXONOMY.md)을 따른다.

See `docs/` for exact version, recording and baseline constraints.
