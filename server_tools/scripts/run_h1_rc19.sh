#!/usr/bin/env bash
# Run the repository's H1 task with the exact tested RC19 settings.
set -Eeuo pipefail

ISAACLAB_ROOT="${ISAACLAB_ROOT:-$HOME/IsaacLab}"
ISAACLAB_PATH="${ISAACLAB_PATH:-$ISAACLAB_ROOT}"
NUM_ENVS="4096"
MAX_ITERATIONS="200"
RUN_NAME=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --num_envs) NUM_ENVS="$2"; shift 2 ;;
    --max_iterations) MAX_ITERATIONS="$2"; shift 2 ;;
    --run_name) RUN_NAME="$2"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done

args=(--task Humanoid-v0 --num_envs "${NUM_ENVS}" --max_iterations "${MAX_ITERATIONS}" --headless)
[[ -n "${RUN_NAME}" ]] && args+=(--run_name "${RUN_NAME}")

cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/training/humanoid"
export ISAACLAB_PATH
"${ISAACLAB_ROOT}/isaaclab.sh" -p train.py "${args[@]}" \
  env.commands.base_velocity.debug_vis=False
