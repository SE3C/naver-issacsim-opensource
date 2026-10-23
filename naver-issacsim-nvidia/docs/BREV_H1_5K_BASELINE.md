# Historical Brev L40S H1 5k direct-wrapper workflow

This document preserves the 2026-09-07 direct-wrapper workflow that trained the unchanged H1 baseline once for 5,000 iterations. It
keeps both the latest numbered checkpoint at each 1,000/2,500/5,000 boundary
and the separate `Train/mean_reward` best-through checkpoint. After training
has finished, it records a single-robot video from each boundary checkpoint.

For a **new** experiment, use the mode-aware `issacsimz` shell wrappers as described in
[`H1_BREV_RUNBOOK.md`](./H1_BREV_RUNBOOK.md). Do not use
`run_h1_brev_5k_baseline.sh` or `H1_AUTO_RELEASE=1` as the current default.

## Safety properties

- Training and rendering never run at the same time.
- Videos are rendered sequentially with `--num_envs 1`.
- Numbered checkpoints are mirrored externally by `issacsimz`; native finalize cleanup remains unchanged.
- `h1_milestone_*.pt` means the latest numbered checkpoint at or before that boundary; a zero-based 5k run normally ends at `model_4999.pt`.
- `h1_best_through_*.pt` separately uses the maximum finite `Train/mean_reward` at or before its cutoff, mapped to the latest available checkpoint at or before that scalar peak.
- Actual source iterations and checkpoint hashes are recorded in `milestone_best_selection.json`.
- Each MP4 is tied to its source checkpoint and exported policy by `video_manifest.tsv`.
- The operation-server auto-submit is disabled.
- The Brev instance is not stopped or deleted by these scripts.

## Historical reproduction only: fresh Brev instance

```bash
git clone https://github.com/SE3C/naver-issacsim-nvidia.git
cd naver-issacsim-nvidia
git pull --ff-only
./scripts/prepare_brev_rc19.sh
```

The preparation script pins Isaac Sim 5.1.0-rc.19 and the repository's tested
Isaac Lab revision.

Before starting the paid run, perform a short smoke test:

```bash
export ISAACLAB_ROOT="$HOME/IsaacLab"
export ISAACLAB_PATH="$ISAACLAB_ROOT"
test -x "${ISAACLAB_ROOT}/isaaclab.sh"
nvidia-smi
./scripts/run_h1_rc19.sh --num_envs 64 --max_iterations 1 --run_name h1-smoke
```

Remove the smoke-test output or leave it outside the baseline result; do not
resume the 5k baseline from the smoke run.

## Historical reproduction only: run

Use tmux so the run survives an SSH disconnect:

```bash
tmux new -s h1-5k
cd ~/naver-issacsim-nvidia
H1_AUTO_RELEASE=1 ./scripts/run_h1_brev_5k_baseline.sh
```

Detach with `Ctrl-b d`, and reconnect with:

```bash
tmux attach -t h1-5k
```

The default run uses 4,096 environments, 5,000 iterations, and 6,000 video
frames (120 seconds at 50 Hz). Optional environment overrides:

```bash
H1_NUM_ENVS=4096 H1_VIDEO_LENGTH=6000 H1_RUN_NAME=my-h1-5k \
  ./scripts/run_h1_brev_5k_baseline.sh
```

## Outputs

The result directory contains:

```text
results/h1_baseline_5k/<run-name>/
├── checkpoints/
│   ├── h1_milestone_1000.pt
│   ├── h1_milestone_2500.pt
│   ├── h1_milestone_5000.pt
│   ├── h1_best_through_1000.pt
│   ├── h1_best_through_2500.pt
│   ├── h1_best_through_5000.pt
│   └── milestone_best_selection.json
├── videos/
│   ├── h1_milestone_1000_6000frames.mp4
│   ├── h1_milestone_2500_6000frames.mp4
│   ├── h1_milestone_5000_6000frames.mp4
│   ├── h1_milestone_*_policy.pt
│   └── video_manifest.tsv
├── metadata/
├── training_console.log
└── SHA256SUMS
```

The script also creates:

```text
results/<run-name>.tar.gz
results/<run-name>.tar.gz.sha256
```

The archive includes the complete original run directory, TensorBoard event
files, all numbered checkpoints, configurations, console log, milestone
checkpoints, videos, exported policies, hardware metadata, and checksums.

With `H1_AUTO_RELEASE=1`, the script creates a GitHub Release after all six
boundary/best-through checkpoints, three boundary-checkpoint MP4 files and
their manifests have been created. It uploads those assets, the full archive,
checksums, and run manifest. It performs an authenticated `gh` preflight
**before** training begins. The Brev instance is never stopped or deleted by
this workflow.

The 2026-09-07 received archive contains 999-frame videos even though an earlier
document described 6,000 frames. Treat the generated `video_manifest.tsv` and
actual MP4 metadata as authoritative; a configured length is not proof that the
video reached that length.
