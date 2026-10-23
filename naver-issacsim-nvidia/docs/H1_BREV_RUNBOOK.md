# H1 Brev 다음 실행 runbook

개인 NVIDIA/Brev에서 H1을 실행할 때의 짧은 체크리스트다. 서버 시작·GitHub 인증·두 checkout 갱신은 먼저 [저장소 README](../README.md#개인-서버-시작-순서)를 따른다. 가설의 부모·reward·상태는 분석 저장소 `research/EXPERIMENTS.md`가 기준이다.

## 먼저 볼 파일

| 필요 | 기준 문서 |
| --- | --- |
| 새 인스턴스 환경 구성 | [RC19 재현 환경](./BREV_RC19_REPRODUCIBILITY.md) |
| 과거 5K baseline 환경 | [H1 5K preflight — historical](./H1_5K_TODAY_PREFLIGHT.md) |
| 옛 direct wrapper와 산출물 의미 | [historical H1 5K workflow](./BREV_H1_5K_BASELINE.md) |
| 실제로 성공한 package/driver | [known-good environment](./KNOWN_GOOD_ENV_20260907.txt) |
| 현재 가설·다음 reward | 분석 저장소 `research/EXPERIMENTS.md`, `data/processed/experiments/h1/2026-09-21_H1_PARENT_AIRTIME_LINEAGE_CORRECTION.md` |

개인 run의 canonical raw archive는 `naver-issacsim-originals/data/raw/private_server_runs/`에 두고, NVIDIA Release는 검증된 편의 mirror로만 쓴다. 결론과 실험 판정은 **analysis**, 설치와 서버 실행 방법은 **nvidia**에 둔다. 큰 binary를 nvidia 저장소에 넣지 않는다.

## 실행 전과 smoke

```bash
cd /ephemeral/issacsimz
./issacsimz train h1 --iters 1 --num-envs 64 --name h1-smoke
```

bootstrap의 `READY`와 H1 doctor가 PASS한 뒤에만 별도 이름으로 1-iteration smoke를 실행한다. 직접 CLI는 local evidence만 남기며 자동 Release publisher를 호출하지 않는다. smoke evidence의 child exit·finalize·validation을 보고 본학습의 부모 checkpoint, reward, seed, iteration을 registry와 대조한다. `NO_AUTO_SUBMIT`을 개인 서버에서 의도적으로 설정했다면 `--allow-no-auto-submit`을 명시한다. 영상 오류가 나면 `libglu1-mesa` 설치 상태를 확인한다.

본학습은 같은 checkout에서 `./scripts/issacsimz_tmux_train.sh h1 --iters ITERATIONS --envs ENVS --name RUN_NAME` 형식으로 시작한다. 대문자 자리표시는 registry에서 확정한 값으로 바꾼다. wrapper는 공식 `train.py`를 호출하고 personal checkpoint mirror·evidence를 남긴다. archive가 생성되면 실패·중단 증거도 personal publisher가 게시할 수 있으므로 Release 이름과 canonical raw 보존 경로를 실행 전에 확인한다. 학습과 영상은 별도 실행한다.

## Historical direct wrapper 재현만 할 때

`scripts/run_h1_brev_5k_baseline.sh`와 `H1_AUTO_RELEASE=1`은 2026-09-07의 direct wrapper workflow를 재현하는 용도다. 새 baseline·새 reward 실험에는 쓰지 않는다.

```bash
# Historical reproduction only; not the current new-run command.
H1_AUTO_RELEASE=1 ./scripts/run_h1_brev_5k_baseline.sh
```

## 완료 판단

다음 항목이 모두 있어야 “완료”다.

- 원본 run directory 전체, TensorBoard event, console log, 설정과 GPU metadata
- `metadata.json`의 child exit, native finalize, official backup, evidence validation 상태
- `native_run/` TensorBoard event, `checkpoints/model_*.pt` mirror, `source/identity.json`
- 이번 run에 생성·변경된 `collected/exported/model_best.pt`, `env.yaml`과 provenance
- `SHA256SUMS`, `.tar.gz`, `.tar.gz.sha256` 및 `./issacsimz verify <archive> --require-sidecar`
- checkpoint에서 별도 policy/video를 만들면 checkpoint→policy→MP4 SHA-256 manifest

5,000회 zero-based 실행은 정상적으로 `model_4999.pt`에서 끝날 수 있다. 옛 wrapper의 `h1_milestone_5000.pt` 별칭은 historical output일 뿐 새 sidecar run의 필수 파일명이 아니다.

## 이번 자료에서 배운 금지선

- H-001 (과거 별칭 TERM50)의 로그 지표는 유망하지만, 전달된 TERM50 MP4는 baseline 1K MP4와 동일하다. TERM50 동작을 말하려면 checkpoint에서 새로 렌더해야 한다.
- `exported/model_best.pt`가 최종 5K임을 가정하지 않는다. 수신 baseline에서는 1K 모델이었다.
- reward weight가 다르면 `Train/mean_reward` 절댓값을 run 간 우열로 쓰지 않는다. survival, episode length, terrain, tracking, 올바르게 연결된 영상을 같이 본다.
- checkpoint와 영상은 파일명으로 연결하지 않는다. manifest hash가 없는 영상은 참고용일 뿐 정책 증거가 아니다.

## 현재 H1 계보 주의

공식 H-001 (과거 별칭 TERM50) 5K는 `feet_air_time=+0.2`지만, 과거 개인 H-001 1.5K 부모는 `-0.2`였다. 그 옛 부모에서 나온 H-005~H-011 결과는 역사적 상대 비교용이다. 이후 `feet=+0.2`인 새 H-001 부모와 unchanged control, corrected H-005~H-011 일부 Run은 별도로 완료됐다. 두 계보를 합치지 말고 각 부모 archive·checkpoint SHA·실제 설정을 registry에서 확인한다.
