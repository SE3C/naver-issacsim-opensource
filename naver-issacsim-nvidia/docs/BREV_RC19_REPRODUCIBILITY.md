# Brev L40S / Isaac Sim RC19 재현 환경

> 2026-09-07 환경 재현 기록이다. 아래 직접 clone·`run_h1_rc19.sh` 명령은 현재 실험 시작 절차가 아니다. 새 개인 서버의 첫 접속·재접속, GitHub 인증과 학습 실행은 저장소 루트 `README.md` 및 `docs/H1_BREV_RUNBOOK.md`를 따른다. 이 문서의 당시 버전·실측값은 역사적 근거로 보존한다.

이 저장소는 학습 코드와 재현용 설치 명령을 보관한다. Isaac Sim 원본 압축본, 로그, 체크포인트, 개인 인증정보는 크기·라이선스·보안 때문에 Git에 넣지 않는다.

## 고정 버전

- Isaac Sim: `5.1.0-rc.19+release.26219.9c81211b.gl`
- Isaac Lab: `2.3.2`, commit `3e73d6dd79080fd7632488c061052a6edd52e230`
- Isaac Sim Python: `3.11.13`
- PyTorch: `2.7.0+cu128`
- Tested GPU: NVIDIA L40S

실제 원본 백업의 `.git/HEAD`가 위 Isaac Lab commit이다. `af1bab4…`는 남아 있던 `release/3.0.0-beta2` 브랜치 참조이며 Python 3.12 이상을 요구해 RC19와 사용하지 않는다.

## 역사적 재현: 새 Brev 인스턴스에서 재구성

Ubuntu/Linux 터미널에서 저장소를 받은 뒤:

```bash
git clone https://github.com/SE3C/naver-issacsim-nvidia.git
cd naver-issacsim-nvidia
bash scripts/prepare_brev_rc19.sh
```

## Isaac Sim archive 캐시와 다음 인스턴스

기본 설치 스크립트는 `aria2c`를 설치해 Isaac Sim ZIP을 최대 8개 연결로 재개 가능하게 받는다. 성공적으로 내려받은 archive에는 `.complete` marker를 남기고, 다음 실행은 marker가 있는 archive만 네트워크 다운로드를 건너뛰어 바로 압축 해제한다. marker가 없으면 부분 파일로 보고 `aria2c`/`curl`의 재개 다운로드를 수행한다.

기본 archive 위치는 `${HOME}/.cache/isaac-sim/isaac-sim-standalone-5.1.0-linux-x86_64.zip`이며, 이는 **같은 VM**에서는 재사용되지만 인스턴스를 삭제하면 사라질 수 있다. provider의 persistent volume을 연결한 경우에는 다음처럼 그 볼륨 경로를 명시한다.

```bash
export ISAAC_SIM_CACHE_DIR=/mnt/cache/isaac-sim
bash scripts/prepare_brev_rc19.sh
```

`/mnt/cache`가 실제 persistent storage라는 보장은 이 저장소가 하지 않는다. 사용 전에 Brev/provider 콘솔의 mount·삭제 정책을 확인한다. 가장 빠른 장기 방법은 Isaac Sim·Isaac Lab 설치를 끝낸 인스턴스를 provider snapshot/image로 재사용하는 것이며, 이 스크립트는 snapshot 생성·삭제를 자동화하지 않는다.

이 스크립트는 Git, Git LFS, tmux, unzip을 설치하고 공식 5.1.0 standalone zip을 받아 `/isaac-sim`에 설치한다. 이후 Isaac Lab을 위 commit으로 checkout하고 `_isaac_sim -> /isaac-sim` 링크를 만든 뒤 `./isaaclab.sh -i rsl_rl`을 실행한다.

## 역사적 H1 직접 실행

```bash
./scripts/run_h1_rc19.sh --num_envs 4096 --max_iterations 200 --run_name exp0_baseline
```

필수 설정인 `env.commands.base_velocity.debug_vis=False`가 스크립트에 내장돼 있다. 이 설정을 빼면 headless 초기화에서 USD debug marker material 생성이 매우 오래 걸린다.

보상 실험은 float override를 사용한다.

```bash
... env.rewards.termination_penalty.weight=-50.0
... env.rewards.flat_orientation_l2.weight=-2.5
... env.rewards.ang_vel_xy_l2.weight=-0.10
... env.rewards.track_lin_vel_xy_exp.weight=1.0
```

`-50`처럼 정수를 사용하면 config type 오류가 나므로 `-50.0`으로 입력한다.

## 결과와 백업

실행 결과는 `training/humanoid/logs/`와 `training/humanoid/exported/`에 생긴다. 이 경로들은 `.gitignore` 대상이며 장기 보관은 별도 백업 방식(GitHub Release/S3 등)을 사용한다.

## 현재 검증된 실행 상태

- 2026-09-07 기본 H1 baseline은 4,096 env, seed 42, 5,000 iterations 요청을 `4999/5000`, exit 0으로 완료했다.
- 학습 loop는 4,208.45초였고 마지막 terrain은 5.054, time-out은 66.79%, base-contact 종료는 33.21%였다. 이 값은 개인 검증환경의 학습 내부 지표다.
- 같은 환경의 1K 단변수 screening에서 H-001 (당시 이름 TERM50)은 장기 확인 후보였고 YAW075와 RECOVERY standalone은 중단 대상으로 판정됐다.
- 검증된 패키지·driver 전체 목록은 [KNOWN_GOOD_ENV_20260907.txt](./KNOWN_GOOD_ENV_20260907.txt)에 보존한다.
- 원본 실행 Release tag는 `h1-baseline-5k-20260907_102236_KST`와 `h1-screening-20260907_122939_KST`다.

수신 baseline archive의 `exported/model_best.pt`는 1K checkpoint와 동일하므로 최종 5K 파일로 사용하지 않는다. 올바른 최종 checkpoint는 run의 `model_4999.pt`다. screening의 H-001 (당시 이름 TERM50) MP4도 baseline 1K 영상과 동일하므로 다시 렌더하기 전에는 해당 run의 시각 증거로 사용하지 않는다.
