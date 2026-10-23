#!/usr/bin/env bash
# Record the currently selected H1 model as a real robot-motion MP4.
set -Eeuo pipefail

ISAACLAB_ROOT="${ISAACLAB_ROOT:-$HOME/IsaacLab}"
VIDEO_LENGTH="1000"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --video_length) VIDEO_LENGTH="$2"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TASK_DIR="$ROOT_DIR/training/humanoid"
VIDEO="$TASK_DIR/exported/play_video.mp4"

[[ -x "$ISAACLAB_ROOT/isaaclab.sh" ]] || {
  echo "Isaac Lab launcher not found: $ISAACLAB_ROOT/isaaclab.sh" >&2
  exit 1
}
[[ -f "$TASK_DIR/exported/model_best.pt" ]] || {
  echo "Missing selected checkpoint: $TASK_DIR/exported/model_best.pt" >&2
  exit 1
}

cd "$TASK_DIR"
export ISAACLAB_PATH="${ISAACLAB_PATH:-$ISAACLAB_ROOT}"
"$ISAACLAB_ROOT/isaaclab.sh" -p play.py \
  --task Humanoid-v0 --num_envs 1 --headless --video \
  --video_length "$VIDEO_LENGTH" --enable_cameras

[[ -s "$VIDEO" ]] || {
  echo "Video recording did not produce a non-empty file: $VIDEO" >&2
  exit 1
}

echo "H1 motion video ready: $VIDEO"
echo "Inspect the video before backing up the run. This script does not delete the instance."
