#!/usr/bin/env bash
set -euo pipefail
PACKAGE_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
if [[ "${ISSACSIMZ_MODE:-personal}" != personal ]]; then
  echo 'ERROR: this evaluator runs in PERSONAL environments only' >&2
  exit 2
fi
if [[ "${1:-}" != --isaaclab-root || -z "${2:-}" ]]; then
  echo 'usage: bash run_evaluation.sh --isaaclab-root /path/IsaacLab --robot go2 --task-root /path/training/quadruped --checkpoint /path/model.pt --output /new/results [options]' >&2
  exit 2
fi
ISAACLAB_ROOT=$2
shift 2
if [[ ! -f "$ISAACLAB_ROOT/isaaclab.sh" ]]; then
  echo "ERROR: IsaacLab launcher not found: $ISAACLAB_ROOT/isaaclab.sh" >&2
  exit 2
fi
export ISAACLAB_PATH="$ISAACLAB_ROOT"
exec bash "$ISAACLAB_ROOT/isaaclab.sh" -p "$PACKAGE_DIR/isaac_runner.py" --mode personal "$@"
