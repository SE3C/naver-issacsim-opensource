#!/usr/bin/env bash
# Run the complete personal/official ISSACSIMZ train wrapper inside detached tmux.
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
die() { echo "[issacsimz] ERROR: $*" >&2; exit 2; }

command -v tmux >/dev/null 2>&1 || die "tmux not found"
[[ $# -ge 1 ]] || die "usage: $0 h1|go2 --iters N --envs N --name NAME"
ROBOT="$1"
shift
[[ "$ROBOT" == h1 || "$ROBOT" == go2 ]] || die "robot must be h1 or go2"

ARGS=("$@")
for arg in "${ARGS[@]}"; do
  [[ "$arg" != --preflight-only ]] || die "--preflight-only must be run with scripts/issacsimz_train.sh, without tmux"
done
NAME=""
CUSTOM_SESSION=""
for ((index = 0; index < ${#ARGS[@]}; index++)); do
  case "${ARGS[$index]}" in
    --name) NAME="${ARGS[$((index + 1))]:-}" ;;
    --name=*) NAME="${ARGS[$index]#--name=}" ;;
    --tmux-session) CUSTOM_SESSION="${ARGS[$((index + 1))]:-}" ;;
    --tmux-session=*) CUSTOM_SESSION="${ARGS[$index]#--tmux-session=}" ;;
  esac
done
[[ -n "$NAME" ]] || die "--name is required"
if [[ -n "$CUSTOM_SESSION" ]]; then NAME="$CUSTOM_SESSION"; fi

SAFE_NAME="$(printf '%s' "$NAME" | sed -E 's/[^A-Za-z0-9_-]+/-/g; s/^-+//; s/-+$//')"
[[ -n "$SAFE_NAME" ]] || die "invalid tmux session name"
SAFE_NAME="${SAFE_NAME:0:80}"
if [[ -n "$CUSTOM_SESSION" ]]; then SESSION="$SAFE_NAME"
else SESSION="issacsimz-${ROBOT}-${SAFE_NAME}"; fi

if tmux has-session -t "$SESSION" 2>/dev/null; then
  die "tmux session already exists: $SESSION"
fi

bash "$ROOT/scripts/issacsimz_train.sh" "$ROBOT" --preflight-only "${ARGS[@]}" || die "train preflight failed; tmux session was not started"

printf -v COMMAND '%q ' bash "$ROOT/scripts/issacsimz_train.sh" "$ROBOT" "${ARGS[@]}"
tmux new-session -d -s "$SESSION" "exec $COMMAND"

echo "[issacsimz] tmux session=$SESSION"
echo "[issacsimz] attach: tmux attach -t $SESSION"
echo "[issacsimz] detach: Ctrl-B then D"
echo "[issacsimz] graceful stop: attach and press Ctrl-C once"
