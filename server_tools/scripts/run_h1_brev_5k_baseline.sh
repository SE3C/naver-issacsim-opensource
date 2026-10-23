#!/usr/bin/env bash
# One-command Brev L40S H1 baseline: train once to 5k, preserve both the
# boundary and reward-best checkpoints for 1k/2.5k/5k, then render the three
# boundary checkpoints sequentially.
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TASK_DIR="$ROOT_DIR/training/humanoid"
LOG_ROOT="$TASK_DIR/logs/rsl_rl/humanoid"
ISAACLAB_ROOT="${ISAACLAB_ROOT:-$HOME/IsaacLab}"
NUM_ENVS="${H1_NUM_ENVS:-4096}"
MAX_ITERATIONS="5000"
VIDEO_LENGTH="${H1_VIDEO_LENGTH:-6000}"
RUN_NAME="${H1_RUN_NAME:-h1-baseline-5k-l40s-$(date +%Y%m%d_%H%M%S)}"
RESULT_ROOT="$ROOT_DIR/results/h1_baseline_5k/$RUN_NAME"
CONSOLE_LOG="$RESULT_ROOT/training_console.log"
AUTO_RELEASE="${H1_AUTO_RELEASE:-0}"
RELEASE_REPO="${H1_RELEASE_REPO:-SE3C/naver-issacsim-nvidia}"
MARKER="$(mktemp)"

cleanup_marker() { rm -f "$MARKER"; }
trap cleanup_marker EXIT

[[ -x "$ISAACLAB_ROOT/isaaclab.sh" ]] || { echo "Isaac Lab launcher not found: $ISAACLAB_ROOT/isaaclab.sh" >&2; exit 1; }
[[ "$AUTO_RELEASE" == "0" || "$AUTO_RELEASE" == "1" ]] || { echo "H1_AUTO_RELEASE must be 0 or 1" >&2; exit 1; }
if [[ "$AUTO_RELEASE" == "1" ]]; then
  command -v gh >/dev/null || { echo "GitHub CLI (gh) is required for H1_AUTO_RELEASE=1" >&2; exit 1; }
  gh auth status --hostname github.com >/dev/null || {
    echo "GitHub CLI is not authenticated; run 'gh auth login --web --git-protocol https' before the 5k run" >&2
    exit 1
  }
fi
[[ ! -e "$RESULT_ROOT" ]] || {
  echo "Result directory already exists; choose a new H1_RUN_NAME: $RESULT_ROOT" >&2
  exit 1
}
mkdir -p "$RESULT_ROOT/checkpoints" "$RESULT_ROOT/videos" "$RESULT_ROOT/metadata" "$LOG_ROOT"

export ISAACLAB_ROOT
export ISAACLAB_PATH="${ISAACLAB_PATH:-$ISAACLAB_ROOT}"
export NO_AUTO_SUBMIT=1

{
  echo "run_name=$RUN_NAME"
  echo "started_at=$(date --iso-8601=seconds)"
  echo "git_commit=$(git -C "$ROOT_DIR" rev-parse HEAD)"
  echo "isaaclab_root=$ISAACLAB_ROOT"
  echo "num_envs=$NUM_ENVS"
  echo "max_iterations=$MAX_ITERATIONS"
  echo "video_length_frames=$VIDEO_LENGTH"
  echo "auto_release=$AUTO_RELEASE"
  echo "release_repo=$RELEASE_REPO"
} > "$RESULT_ROOT/metadata/run_manifest.txt"
nvidia-smi -q > "$RESULT_ROOT/metadata/nvidia-smi-q.txt"
git -C "$ROOT_DIR" status --short --branch > "$RESULT_ROOT/metadata/git-status.txt"

echo "[h1-5k] training starts: run=$RUN_NAME envs=$NUM_ENVS iterations=$MAX_ITERATIONS"
set +e
"$ROOT_DIR/scripts/run_h1_rc19.sh" \
  --num_envs "$NUM_ENVS" --max_iterations "$MAX_ITERATIONS" --run_name "$RUN_NAME" \
  2>&1 | tee "$CONSOLE_LOG"
train_status=${PIPESTATUS[0]}
set -e
if [[ $train_status -ne 0 ]]; then
  echo "[h1-5k] ERROR: training exited with $train_status; logs/checkpoints were left untouched" >&2
  exit "$train_status"
fi

run_dir="$(find "$LOG_ROOT" -mindepth 1 -maxdepth 1 -type d -newer "$MARKER" \
  -name "*${RUN_NAME}*" -printf '%T@ %p\n' | sort -nr | head -n 1 | cut -d' ' -f2-)"
[[ -n "$run_dir" && -d "$run_dir" ]] || { echo "Could not identify the completed run directory under $LOG_ROOT" >&2; exit 1; }
printf 'run_dir=%s\n' "$run_dir" >> "$RESULT_ROOT/metadata/run_manifest.txt"

echo "[h1-5k] selecting boundary and Train/mean_reward best checkpoints for 1k/2.5k/5k"
"${ISAACLAB_ROOT}/_isaac_sim/python.sh" "$ROOT_DIR/scripts/select_h1_milestone_bests.py" \
  --run-dir "$run_dir" \
  --output-dir "$RESULT_ROOT/checkpoints" \
  --milestones 1000 2500 5000 \
  | tee "$RESULT_ROOT/metadata/milestone_best_selection.log"

for milestone in 1000 2500 5000; do
  [[ -s "$RESULT_ROOT/checkpoints/h1_milestone_${milestone}.pt" ]] || {
    echo "ERROR: missing milestone-${milestone} checkpoint" >&2
    exit 1
  }
  [[ -s "$RESULT_ROOT/checkpoints/h1_best_through_${milestone}.pt" ]] || {
    echo "ERROR: missing best-through-${milestone} checkpoint" >&2
    exit 1
  }
done

if [[ -d "$run_dir/params" ]]; then
  cp -a "$run_dir/params" "$RESULT_ROOT/metadata/"
fi
cp -f "$TASK_DIR/humanoid_rewards.py" "$RESULT_ROOT/metadata/"
cp -f "$TASK_DIR/h1_task/agent_cfg.py" "$RESULT_ROOT/metadata/"
cp -f "$TASK_DIR/h1_task/env_cfg.py" "$RESULT_ROOT/metadata/"

export H1_VIDEO_OUTPUT_DIR="$RESULT_ROOT/videos"
"$ROOT_DIR/scripts/record_h1_checkpoints.sh" --video_length "$VIDEO_LENGTH" \
  "$RESULT_ROOT/checkpoints/h1_milestone_1000.pt" \
  "$RESULT_ROOT/checkpoints/h1_milestone_2500.pt" \
  "$RESULT_ROOT/checkpoints/h1_milestone_5000.pt"

for video in "$RESULT_ROOT"/videos/*.mp4; do
  [[ -s "$video" ]] || { echo "ERROR: missing/empty expected video: $video" >&2; exit 1; }
done

echo "completed_at=$(date --iso-8601=seconds)" >> "$RESULT_ROOT/metadata/run_manifest.txt"
(cd "$ROOT_DIR" && sha256sum \
  "${RESULT_ROOT#$ROOT_DIR/}"/checkpoints/*.pt \
  "${RESULT_ROOT#$ROOT_DIR/}"/checkpoints/milestone_best_selection.json \
  "${RESULT_ROOT#$ROOT_DIR/}"/videos/*.mp4 \
  "${RESULT_ROOT#$ROOT_DIR/}"/videos/*_policy.pt \
  "${RESULT_ROOT#$ROOT_DIR/}"/videos/video_manifest.tsv \
  > "${RESULT_ROOT#$ROOT_DIR/}/SHA256SUMS")

archive="$ROOT_DIR/results/${RUN_NAME}.tar.gz"
tar -C "$ROOT_DIR" -czf "$archive" \
  "${RESULT_ROOT#$ROOT_DIR/}" \
  "${run_dir#$ROOT_DIR/}"
sha256sum "$archive" > "$archive.sha256"

if [[ "$AUTO_RELEASE" == "1" ]]; then
  release_tag="h1-5k-${RUN_NAME}"
  release_assets=(
    "$RESULT_ROOT/checkpoints/h1_milestone_1000.pt"
    "$RESULT_ROOT/checkpoints/h1_milestone_2500.pt"
    "$RESULT_ROOT/checkpoints/h1_milestone_5000.pt"
    "$RESULT_ROOT/checkpoints/h1_best_through_1000.pt"
    "$RESULT_ROOT/checkpoints/h1_best_through_2500.pt"
    "$RESULT_ROOT/checkpoints/h1_best_through_5000.pt"
    "$RESULT_ROOT/checkpoints/milestone_best_selection.json"
    "$RESULT_ROOT"/videos/*.mp4
    "$RESULT_ROOT"/videos/*_policy.pt
    "$RESULT_ROOT/videos/video_manifest.tsv"
    "$RESULT_ROOT/SHA256SUMS"
    "$RESULT_ROOT/metadata/run_manifest.txt"
    "$archive"
    "$archive.sha256"
  )
  echo "[h1-5k] uploading GitHub Release: $RELEASE_REPO / $release_tag"
  gh release create "$release_tag" "${release_assets[@]}" \
    --repo "$RELEASE_REPO" \
    --target "$(git -C "$ROOT_DIR" rev-parse HEAD)" \
    --title "H1 baseline 5k — $RUN_NAME" \
    --notes "Personal NVIDIA/Brev H1 baseline. Preserves boundary checkpoints for 1k, 2.5k, and the zero-based 5k final boundary, separate reward-best-through checkpoints, and videos rendered from the boundary checkpoints. See the JSON/TSV manifests for actual source iterations and hashes. The instance is not stopped or deleted by this workflow."
fi

echo "[h1-5k] COMPLETE"
echo "  result : $RESULT_ROOT"
echo "  archive: $archive"
[[ "$AUTO_RELEASE" == "1" ]] && echo "  release: https://github.com/$RELEASE_REPO/releases/tag/$release_tag"
echo "  note   : the Brev instance is NOT deleted automatically"
