#!/usr/bin/env bash
# Render one deterministic Go2 baseline video for each supplied RSL-RL checkpoint.
# Run inside the Ubuntu Isaac Lab environment; see docs/GO2_BASELINE_RECORDING.md.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TRAINING_DIR="$ROOT_DIR/training/quadruped"
OUTPUT_DIR="$ROOT_DIR/results/videos/go2_baseline"
ISAACLAB_PATH="${ISAACLAB_PATH:-/workspace/IsaacLab}"
VIDEO_LENGTH="${NCRC_GO2_VIDEO_LENGTH:-1600}" # 50 Hz x 1600 = 32 seconds

usage() {
  cat <<'EOF'
Usage:
  ISAACLAB_PATH=/workspace/IsaacLab bash scripts/record_go2_checkpoints.sh \
    /absolute/path/to/model_5000.pt /absolute/path/to/model_12000.pt

The rendered files are written as:
  results/videos/go2_baseline/go2_baseline_5k_32s.mp4
  results/videos/go2_baseline/go2_baseline_12k_32s.mp4
EOF
}

[[ $# -eq 2 ]] || { usage >&2; exit 2; }
[[ -x "$ISAACLAB_PATH/isaaclab.sh" ]] || {
  echo "ERROR: Isaac Lab launcher not found: $ISAACLAB_PATH/isaaclab.sh" >&2
  exit 1
}
[[ -f "$TRAINING_DIR/play.py" ]] || { echo "ERROR: missing $TRAINING_DIR/play.py" >&2; exit 1; }

mkdir -p "$OUTPUT_DIR"

render_checkpoint() {
  local checkpoint="$1"
  local label="$2"
  # Official play.py loads exported/model_best.pt explicitly; stage each input there.
  local staged_model="$TRAINING_DIR/exported/model_best.pt"
  local target="$OUTPUT_DIR/go2_baseline_${label/000/k}_32s.mp4"

  [[ -f "$checkpoint" ]] || { echo "ERROR: checkpoint not found: $checkpoint" >&2; exit 1; }
  mkdir -p "$TRAINING_DIR/exported"
  cp -f "$checkpoint" "$staged_model"

  rm -f "$TRAINING_DIR/exported/play_video.mp4"
  echo "[go2-video] rendering checkpoint=$checkpoint (label=$label, frames=$VIDEO_LENGTH)"
  (
    cd "$TRAINING_DIR"
    "$ISAACLAB_PATH/isaaclab.sh" -p play.py --task Quadruped-v0 --num_envs 1 \
      --headless --video --video_length "$VIDEO_LENGTH" --enable_cameras
  )

  [[ -s "$TRAINING_DIR/exported/play_video.mp4" ]] || {
    echo "ERROR: play completed but exported/play_video.mp4 was not produced" >&2
    exit 1
  }
  cp -f "$TRAINING_DIR/exported/play_video.mp4" "$target"
  echo "[go2-video] completed: $target"
}

render_checkpoint "$1" 5000
render_checkpoint "$2" 12000

echo "[go2-video] all recordings complete: $OUTPUT_DIR"
