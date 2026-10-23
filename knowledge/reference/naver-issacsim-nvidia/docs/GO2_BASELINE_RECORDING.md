> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim-nvidia/docs/GO2_BASELINE_RECORDING.md` (`91b32f6fc0bc`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# Go2 baseline video recording

This procedure produces two independently traceable baseline videos from two
explicitly selected RSL-RL checkpoints. It deliberately uses separate runs so
that Isaac Lab cannot silently replay the latest model for both videos.

## Preconditions

- Ubuntu with Isaac Sim `5.1.0-rc.19` and a compatible Isaac Lab installation.
- The repository is available on that machine, with the Go2 training package.
- Two preselected Go2 checkpoints. Their names and actual iterations must be
  recorded exactly; a "5k" or "12k" label is not proof that a corresponding
  `model_5000.pt` or `model_12000.pt` exists.

The local Windows checkout does not contain Isaac Lab or either checkpoint, so
rendering has to be run on the GPU Linux machine that owns the checkpoints.

## Run

```bash
cd /path/to/naver-issacsim-nvidia
ISAACLAB_PATH=/workspace/IsaacLab bash scripts/record_go2_checkpoints.sh \
  /absolute/path/to/first_selected_model.pt \
  /absolute/path/to/second_selected_model.pt
```

The default `NCRC_GO2_VIDEO_LENGTH=1600` records 1,600 frames at the Go2
environment's 50 Hz rate: 32 seconds. The output files use helper labels:

```text
results/videos/go2_baseline/go2_baseline_5k_32s.mp4
results/videos/go2_baseline/go2_baseline_12k_32s.mp4
```

## Verify duration and identity

```bash
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 \
  results/videos/go2_baseline/go2_baseline_5k_32s.mp4 \
  results/videos/go2_baseline/go2_baseline_12k_32s.mp4
```

Both values must be at least 30 seconds. Keep the helper console log with the
source checkpoint paths. Its labels and staging directory are convenience
names, not evidence of exact iteration identity.
