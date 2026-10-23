#!/usr/bin/env bash
# Render one single-robot H1 video for every supplied checkpoint, sequentially.
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TASK_DIR="$ROOT_DIR/training/humanoid"
ISAACLAB_ROOT="${ISAACLAB_ROOT:-$HOME/IsaacLab}"
VIDEO_LENGTH="${H1_VIDEO_LENGTH:-6000}"
OUTPUT_DIR="${H1_VIDEO_OUTPUT_DIR:-$ROOT_DIR/results/videos/h1_baseline_5k}"

usage() {
  cat <<'EOF'
Usage: record_h1_checkpoints.sh [--video_length FRAMES] CHECKPOINT [CHECKPOINT ...]

Defaults to 6000 frames (120 seconds at 50 Hz). Videos use one robot and are
rendered sequentially to avoid competing Isaac Sim processes and GPU OOM.
EOF
}

checkpoints=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --video_length) VIDEO_LENGTH="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    --*) echo "Unknown argument: $1" >&2; usage >&2; exit 2 ;;
    *) checkpoints+=("$1"); shift ;;
  esac
done

[[ ${#checkpoints[@]} -gt 0 ]] || { usage >&2; exit 2; }
[[ "$VIDEO_LENGTH" =~ ^[1-9][0-9]*$ ]] || { echo "Invalid video length: $VIDEO_LENGTH" >&2; exit 2; }
[[ -x "$ISAACLAB_ROOT/isaaclab.sh" ]] || { echo "Isaac Lab launcher not found: $ISAACLAB_ROOT/isaaclab.sh" >&2; exit 1; }

mkdir -p "$OUTPUT_DIR" "$TASK_DIR/exported"
stage="$TASK_DIR/exported/model_best.pt"
backup_dir="$(mktemp -d)"
for artifact in model_best.pt policy.pt play_video.mp4; do
  [[ -f "$TASK_DIR/exported/$artifact" ]] && cp -p "$TASK_DIR/exported/$artifact" "$backup_dir/$artifact"
done

restore_stage() {
  for artifact in model_best.pt policy.pt play_video.mp4; do
    if [[ -f "$backup_dir/$artifact" ]]; then
      cp -p "$backup_dir/$artifact" "$TASK_DIR/exported/$artifact"
    else
      rm -f "$TASK_DIR/exported/$artifact"
    fi
  done
  [[ -n "$backup_dir" && -d "$backup_dir" ]] && rm -rf -- "$backup_dir"
}
trap restore_stage EXIT

manifest="$OUTPUT_DIR/video_manifest.tsv"
printf 'checkpoint_file\tcheckpoint_sha256\trequested_frames\texpected_seconds_at_50hz\tvideo_file\tvideo_sha256\tpolicy_file\tpolicy_sha256\n' > "$manifest"

for checkpoint in "${checkpoints[@]}"; do
  checkpoint="$(realpath "$checkpoint")"
  [[ -s "$checkpoint" ]] || { echo "Missing or empty checkpoint: $checkpoint" >&2; exit 1; }

  base="$(basename "$checkpoint" .pt)"
  expected_seconds="$(awk -v frames="$VIDEO_LENGTH" 'BEGIN { printf "%.2f", frames / 50 }')"
  target="$OUTPUT_DIR/${base}_${VIDEO_LENGTH}frames.mp4"
  policy_target="$OUTPUT_DIR/${base}_policy.pt"

  cp -f "$checkpoint" "$stage"
  [[ "$(sha256sum "$checkpoint" | awk '{print $1}')" == "$(sha256sum "$stage" | awk '{print $1}')" ]] || {
    echo "ERROR: staged checkpoint hash mismatch for $checkpoint" >&2
    exit 1
  }
  rm -f "$TASK_DIR/exported/play_video.mp4" "$TASK_DIR/exported/policy.pt"
  echo "[h1-video] rendering $base from $checkpoint (frames=$VIDEO_LENGTH, num_envs=1)"

  (
    cd "$TASK_DIR"
    export ISAACLAB_PATH="${ISAACLAB_PATH:-$ISAACLAB_ROOT}"
    "$ISAACLAB_ROOT/isaaclab.sh" -p play.py \
      --task Humanoid-v0 --num_envs 1 --headless --video \
      --video_length "$VIDEO_LENGTH" --enable_cameras
  )

  [[ -s "$TASK_DIR/exported/play_video.mp4" ]] || {
    echo "ERROR: play completed without a non-empty video for $base" >&2
    exit 1
  }
  [[ -s "$TASK_DIR/exported/policy.pt" ]] || {
    echo "ERROR: play completed without a non-empty policy export for $base" >&2
    exit 1
  }
  cp -f "$TASK_DIR/exported/play_video.mp4" "$target"
  cp -f "$TASK_DIR/exported/policy.pt" "$policy_target"
  checkpoint_sha="$(sha256sum "$checkpoint" | awk '{print $1}')"
  video_sha="$(sha256sum "$target" | awk '{print $1}')"
  policy_sha="$(sha256sum "$policy_target" | awk '{print $1}')"
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$(basename "$checkpoint")" "$checkpoint_sha" "$VIDEO_LENGTH" "$expected_seconds" \
    "$(basename "$target")" "$video_sha" "$(basename "$policy_target")" "$policy_sha" >> "$manifest"
  echo "[h1-video] complete: $target"
done

echo "[h1-video] all recordings complete: $OUTPUT_DIR"
