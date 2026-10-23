#!/usr/bin/env bash
# Reproduce the Go2 5k / 9.5k policy videos on the Brev massedcompute L40S setup.
set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TRAINING_DIR="$ROOT_DIR/training/quadruped"
ISAACLAB_PATH="${ISAACLAB_PATH:-/home/shadeform/IsaacLab}"
VIDEO_LENGTH="${NCRC_GO2_VIDEO_LENGTH:-6000}" # 50 Hz x 6000 = 120 seconds.
OUTPUT_DIR="$ROOT_DIR/results/videos/go2_brev_l40s"

usage() {
  cat <<'EOF'
Usage:
  ISAACLAB_PATH=/home/shadeform/IsaacLab bash scripts/record_go2_brev_l40s.sh \
    /absolute/path/to/model_5000.pt /absolute/path/to/model_9500.pt

The script renders one robot at a time and writes:
  results/videos/go2_brev_l40s/go2_5k_120s.mp4
  results/videos/go2_brev_l40s/go2_9500_120s.mp4

Set NCRC_GO2_VIDEO_LENGTH to change the number of 50 Hz simulation steps.
EOF
}

[[ $# -eq 2 ]] || { usage >&2; exit 2; }
[[ -x "$ISAACLAB_PATH/isaaclab.sh" ]] || {
  echo "ERROR: Isaac Lab launcher not found: $ISAACLAB_PATH/isaaclab.sh" >&2
  exit 1
}

mkdir -p "$OUTPUT_DIR" "$TRAINING_DIR/exported"
SECONDS_LABEL="$((VIDEO_LENGTH / 50))"

render() {
  local label="$1"
  local checkpoint="$2"
  local target="$OUTPUT_DIR/go2_${label}_${SECONDS_LABEL}s.mp4"

  [[ -f "$checkpoint" ]] || { echo "ERROR: checkpoint not found: $checkpoint" >&2; exit 1; }
  cp -f "$checkpoint" "$TRAINING_DIR/exported/model_best.pt"
  rm -f "$TRAINING_DIR/exported/play_video.mp4"

  (
    cd "$TRAINING_DIR"
    export ISAACLAB_PATH
    unset NCRC_PLAY_PUSH
    "$ISAACLAB_PATH/isaaclab.sh" -p play.py --task Quadruped-v0 --num_envs 1 \
      --headless --video --video_length "$VIDEO_LENGTH" --enable_cameras \
      env.scene.terrain.terrain_generator.num_rows=1 \
      env.scene.terrain.terrain_generator.num_cols=1
  )

  [[ -s "$TRAINING_DIR/exported/play_video.mp4" ]] || {
    echo "ERROR: play completed without producing a video" >&2
    exit 1
  }
  cp -f "$TRAINING_DIR/exported/play_video.mp4" "$target"
  echo "[go2-brev-video] complete: $target"
}

render 5k "$1"
render 9500 "$2"
