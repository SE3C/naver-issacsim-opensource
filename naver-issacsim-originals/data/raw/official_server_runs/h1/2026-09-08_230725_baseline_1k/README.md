# H1 공식 서버 baseline 1K 실행 결과 원본

## 출처와 보존 범위

- 출처: 사용자가 NAVER CONNECT Robotics Cup 공식 서버에서 실행한 H1 결과
- 실행 시작 시각: `2026-09-08 23:07:25 KST`
- 수집 위치: 사용자 PC `Downloads`
- 분류: 작업공간 전체 백업이 아니라 공식 서버 실행의 결과·환경·출처 증거 묶음
- 보존 원칙: 전달받은 5개 파일의 이름과 바이트를 변경하지 않음
- Release: `official-h1-20260908-baseline-1k`의 동명 asset이며 아래 SHA-256과 일치

해석·성능 판정은 analysis 저장소의 `data/processed/experiments/h1/2026-09-08_OFFICIAL_SERVER_H1_BASELINE_1K.md`를 따른다.

## 수신 원본 manifest

| 파일 | bytes | SHA-256 |
| --- | ---: | --- |
| `H1_baseline_1k_complete_20260908_final.tar` | 41,994,240 | `000b07bdc91bd458770ad14d568bddb7261fa4fa3b89e6511080398ebea1dd79` |
| `h1_code_sha256.txt` | 2,079 | `66f61841c7d9e729ff78ec99bbee56c0dd153c9bd81d3634c6e6990899cbd0c2` |
| `history_backup.txt` | 1,769 | `88967c8d7772a81afc2a6d0da45a826da9f6b3872c83ff5b81efc08d642381eb` |
| `isaac_pip_freeze.txt` | 5,974 | `36cdbbfe4265eadb26afb58eae6e09e7f49a6268812eaf20bf9749e4a2c66b53` |
| `isaac_version.txt` | 37 | `3608df6c48e6857e9cdcf9cedb5ddf23d3ce76c46bc87b0f6ab3a5241ef5e5e7` |

`.tar` 원본은 이 저장소의 Git LFS 대상으로 관리한다.

## TAR에서 확인되는 실행 구성

TAR에는 상대경로만 사용한 파일 17개가 있다.

- 원본 run: TensorBoard event, `model_999.pt`, `env.yaml`, `agent.yaml`, `IsaacLab.diff`
- export: `model_best.pt`, TorchScript policy, ONNX policy, report, MP4와 timestamp 별칭
- reward 증거: root의 `humanoid_rewards.py`

직접 확인되는 실행 조건은 seed `42`, `4096` environments, `1000` iterations, `cuda:0`이다. reward는 기본 baseline 값이며 `termination_penalty=-5.0`, `track_ang_vel_z_exp=0.5`, `joint_deviation_hip=-0.2`, `joint_deviation_torso=-0.1`이다.

`IsaacLab.diff`는 Isaac Lab commit `3e73d6dd79080fd7632488c061052a6edd52e230`과 clean working tree를 기록한다. `isaac_version.txt`는 Isaac Sim `5.1.0-rc.19+release.26219.9c81211b.gl`을 기록하고, `isaac_pip_freeze.txt`도 같은 Isaac Lab commit 및 `torch==2.7.0+cu128`을 가리킨다.

이 1K 묶음 자체에는 `/etc/os-release` 사본이 없다. 같은 공식 서버의 바로 다음 TERM50 5K 원본 README에는 Ubuntu 24.04.2 LTS, RTX 5080, driver 580.126.09가 기록되어 있다. 1K tar 내용을 고친 것이 아니라 인접 실행의 호스트 기록이다.

## 핵심 내부 무결성 관계

| 관계 | SHA-256 |
| --- | --- |
| `model_999.pt` = 두 `model_best*.pt` | `b38e8a4c84165bf4ad7e2e5d6c7418c2b5d08696670aad971cd6f0da9eb8a674` |
| 두 TorchScript `policy*.pt` | `2a5ada7945a3c3a2852ad7e88d63324e5d156977fe807637f847c78ad1315687` |
| 두 ONNX `policy*.onnx` | `6a9f032c3c768ea65e3bc761527685190f6772fe8834babec5ccca06b69fe34d` |
| 두 `play_video*.mp4` | `d4a3c6fb4e055982a50812041270571d29756d224ac713d393998ace1c1c5161` |
| run·export의 세 `env*.yaml` | `177c28288f0641bb7edb0abbb085db754cae15ded8b034196ab1d5de936d1cc1` |
| TensorBoard event | `968929679dc2bec0460f78158aef3587593a61e5b3513c0790015015dbae3fd6` |
| `report.html` | `61ba62c594706b210c124c7f9507894dfe7bd6ae852d55c0a3aa2f21209daa35` |

영상은 H.264, 1920×1080, 50 fps, 999 frames, 19.98초이며 두 이름은 동일 파일이다.

## 코드 해시 파일의 의미

`h1_code_sha256.txt`는 결과 생성 시점에 관련 코드·설정 경로의 해시를 기록한 증거 목록이지, 그 경로 전체가 TAR에 들어 있다는 완전성 manifest가 아니다.

특히 해시 목록의 live `./humanoid_rewards.py`는 `2dc6f4...`이지만 TAR root의 `humanoid_rewards.py`는 `c09c85...`이다. 후자는 해시 목록의 `./humanoid_rewards_baseline_1k.py`와 정확히 일치한다. 따라서 TAR root 파일은 baseline 1K용 reward 스냅샷을 결과 묶음에 넣은 것으로 해석하며, live 작업공간 전체 백업으로 해석하지 않는다.

## report가 직접 표시하는 결과

| 항목 | 값 |
| --- | ---: |
| 완료 iteration | `999 / 1000` |
| 학습 시각 | 23:07~23:19 KST |
| 표시 소요시간 | 12분 14초 |
| 최고 mean reward | `0.38`, iteration `971` |
| 마지막 terrain level | `0.00` |
| 마지막 10회 평균 낙상률 | `100.0%` |
| 마지막 exploration std | `0.653` |
| 제출 파일 NaN | 없음 |

이 값은 학습 report의 반올림 표시값이며 공식 평가 점수가 아니다. `model_best.pt`가 `model_999.pt`와 같은 것은 peak iteration 971에 가장 가까운 저장 checkpoint가 마지막 checkpoint였던 결과와 일관된다.

## 증거 한계

- `history_backup.txt`는 실행 명령 전체가 아니라 결과 수집 시점의 최근 shell history다.
- 전체 학습 콘솔 로그, `nvidia-smi` 시계열, 실제 대시보드 사용시간, 공식 evaluator 점수는 포함되지 않았다.
- TensorBoard event는 보존됐지만 report의 종단 요약과 별개의 공식 점수를 의미하지 않는다.
- 해시 목록에 있으나 TAR에 없는 경로는 이 결과 묶음의 목적상 누락으로 판정하지 않는다.
- 텍스트 증거에서 credential 형태의 문자열은 발견되지 않았다.
