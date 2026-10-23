# H1 TERM50 5K 공식 서버 실행 원본

NAVER 공식 서버에서 실행한 H1 TERM50 5K 학습 결과를 다운로드 당시의 압축 파일 그대로 보관한다. 이 디렉터리는 원본 증거 보존용이며, 해석과 성능 비교는 분석 저장소에서 관리한다.

## 원본 식별

- 원본 파일: `H1_TERM50_5k_complete_20260909_003012.tar.gz`
- 수집 위치: `C:/Users/[USER]\Downloads`
- 다운로드 파일 수정 시각: 2026-09-09 00:30:48 KST
- 크기: 70,432,371 bytes
- SHA-256: `723208aafa89e811d8c464b1482949df3259e935bff5f1ea1da7f8da61b806fb`
- 압축 내부 파일: 25개
- 원본 정책: 압축 파일의 내용, 파일명, 내부 manifest를 수정하지 않는다.
- Release: `official-h1-20260909-term50-5k`의 동명 asset이며 위 SHA-256과 일치

## 실행 조건

압축 내부 `experiment_info.txt`, `params/env.yaml`, `params/agent.yaml`, `git/IsaacLab.diff` 및 실행 로그에서 직접 확인한 값이다.

- experiment: `H1_TERM50_5k`
- task: `Humanoid-v0`
- source run: `logs/rsl_rl/humanoid/2026-09-08_23-23-33`
- seed: 42
- parallel environments: 4,096
- max iterations: 5,000
- reward schedule 변경: `termination_penalty`만 `-5.0`에서 `-50.0`으로 변경
- yaw tracking scale: `0.5`
- hip penalty scale: `-0.2`
- torso penalty scale: `-0.1`
- IsaacLab commit: `3e73d6dd79080fd7632488c061052a6edd52e230` clean detached tree

실행 환경 로그에는 NVIDIA GeForce RTX 5080 16,303 MB, driver 580.126.09, Ubuntu 24.04.2 LTS, kernel 6.8.0-136-generic, Intel Core Ultra 5 250KF Plus 18 cores, RAM 64,006 MB가 기록되어 있다.

## 결과 메타데이터

다음 수치는 압축에 포함된 HTML 보고서와 `experiment_info.txt`의 기록값이다. 별도의 공식 evaluator 점수는 묶음에 포함되어 있지 않다.

- 시작: 2026-09-08 23:23 KST
- 종료: 2026-09-09 00:27 KST
- duration: 약 1시간 5분
- best iteration: 4,851
- best reward: 4.648400783538818
- terrain level: 5.82
- 최근 10회 평균 fall rate: 28.9%
- final exploration std: 1.296
- 보고서 표시 checkpoint: iteration 4,900 / 5,000
- 보고서 경고: 낙상이 잦고 exploration이 높아 보행 안정성이 확정되지 않았으므로 영상 확인이 필요하다.

## 현재 TERM50 5K 산출물 관계

아래 별칭은 동일한 현재 실행 산출물이다.

| 종류 | 현재 파일 | 동일 별칭 | SHA-256 |
| --- | --- | --- | --- |
| checkpoint | `logs/.../model_4900.pt` | `exported/model_best.pt`, `exported/model_best_20260908232333.pt` | `e7343a96cf861bb700aefda704eda3eaadc42e7caac5a3d35904a6c2d17dabc0` |
| TorchScript policy | `exported/policy.pt` | `exported/policy_20260909_003012.pt` | `f776d2e5571497360fc46f101c69352a57ae8f1f40c8c7c868a4a11f8f117ef9` |
| ONNX policy | `exported/policy.onnx` | `exported/policy_20260909_003012.onnx` | `82c694e0e9695e2e313e4693bd6b17c217c4ba56cd08031e1b4951b75ea4e48f` |
| play video | `exported/play_video.mp4` | `exported/play_video_20260909_003012.mp4` | `ce97333c47f5c6700cc3c5a0270ca6d7d1dfbb4cfa3cbf45e58ff6a0359717a8` |
| environment config | `exported/env.yaml` | `exported/env_20260908232333.yaml`, run `params/env.yaml` | `63402b9b92723c0af0eaa0185222cb96b6c0aebfbdcba66c8a040d84bfca85fa` |

현재 play video는 H.264 1920x1080, 50 fps, 2,000 frames, 40.0초이다.

## 함께 들어 있는 이전 baseline 별칭

압축에는 앞선 baseline 1K 실행의 별칭 파일도 함께 들어 있다. 다음 파일들은 기존 공식 baseline 1K 보관본과 해시가 같으므로 TERM50 5K 결과 증거로 사용하면 안 된다.

- `exported/env_20260908230725.yaml`
- `exported/model_best_20260908230725.pt`
- `exported/policy_20260908_232209.pt`
- `exported/policy_20260908_232209.onnx`
- `exported/play_video_20260908_232209.mp4`

이전 영상은 999 frames, 19.98초이다. TERM50 5K를 사용할 때는 위의 현재 generic 파일 또는 `20260909_003012`, `20260908232333` 별칭을 선택한다.

## 무결성 점검

- 외부 TAR SHA-256은 다운로드 원본과 저장소 복사본이 일치한다.
- 내부 `manifest_sha256.txt`의 25개 항목 중 일반 파일 24개는 실제 해시와 일치한다.
- manifest가 자기 자신에 기록한 예상 SHA-256은 `a8de51b45645181ccf1e502450e639bf06c0ff9edd464bb684b0eb351f477199`이나 실제 manifest SHA-256은 `89af4caade9dabd2a346e3b1ac55df4ca3c5d5decef6f00dd3250780ab59a24a`이다.
- 위 한 건은 자기 자신의 해시 줄을 추가하면 파일 내용이 다시 바뀌는 self-entry 문제로 분류한다. 원본 보존 원칙에 따라 manifest를 수정하지 않는다.
- 텍스트 파일에서 credential 형태의 민감 문자열은 발견되지 않았다.
