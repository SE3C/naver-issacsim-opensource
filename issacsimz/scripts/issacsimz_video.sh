#!/usr/bin/env bash
# Mode-aware video orchestration. Never invokes GitHub in official mode.
set -Eeuo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; STATE="${ISSACSIMZ_STATE_FILE:-$ROOT/.issacsimz-mode.env}"
source "$ROOT/scripts/python_runner.sh"
[[ -f "$STATE" ]] || { echo "[issacsimz] ERROR: bootstrap first" >&2; exit 2; }; source "$STATE"
export ISSACSIMZ_MODE
[[ -z "${ISSACSIMZ_DOWNLOAD_ROOT:-}" ]] || export ISSACSIMZ_DOWNLOAD_ROOT
[[ $# -ge 1 ]] || { echo "[issacsimz] ERROR: usage: $0 h1|go2 --from-run RUN_ID [video options]" >&2; exit 2; }
ROBOT="$1"; shift; [[ "$ROBOT" == h1 || "$ROBOT" == go2 ]] || { echo "[issacsimz] ERROR: robot must be h1 or go2" >&2; exit 2; }
ARGS=(); while (( $# )); do case "$1" in --envs) ARGS+=(--num-envs "${2:?--envs needs a value}"); shift 2;; *) ARGS+=("$1"); shift;; esac; done
if [[ "$ROBOT" == h1 ]]; then TASK_ROOT="${ISSACSIMZ_H1_ROOT:?H1 task root missing; re-run bootstrap}"
else TASK_ROOT="${ISSACSIMZ_GO2_ROOT:?Go2 task root missing; re-run bootstrap}"; fi
LAB_ROOT="${ISSACSIMZ_ISAACLAB_ROOT:?IsaacLab path missing; re-run bootstrap}"
if [[ "$ISSACSIMZ_MODE" == official ]]; then unset GH_TOKEN GITHUB_TOKEN; fi
PYTHON_RUNNER="$(issacsimz_find_python_runner "$LAB_ROOT")" || exit 2
LOG="$(mktemp "${ISSACSIMZ_EVIDENCE_ROOT}/${ROBOT}-video.XXXXXX.log")"; trap 'rm -f "$LOG"' EXIT
set +e; "$PYTHON_RUNNER" "$ISSACSIMZ_PYZ" video "$ROBOT" --log-root "$ISSACSIMZ_EVIDENCE_ROOT" --task-root "$TASK_ROOT" --isaaclab-root "$LAB_ROOT" "${ARGS[@]}" 2>&1 | tee "$LOG"; CODE=${PIPESTATUS[0]}; set -e
ARCHIVE="$(sed -n 's/^\[issacsimz\] archive=//p' "$LOG" | tail -n 1)"; EVIDENCE="$(sed -n 's/^\[issacsimz\] evidence=//p' "$LOG" | tail -n 1)"
if [[ "$ISSACSIMZ_MODE" == personal && "${ISSACSIMZ_DISABLE_PUBLISH:-0}" != 1 && "$CODE" -eq 0 && -n "$ARCHIVE" && -f "$ARCHIVE" ]]; then
  EXTRA=()
  [[ -f "$EVIDENCE/collected/exported/play_video.mp4" ]] && EXTRA+=("$EVIDENCE/collected/exported/play_video.mp4")
  [[ -f "$EVIDENCE/video_manifest.json" ]] && EXTRA+=("$EVIDENCE/video_manifest.json")
  bash "$ROOT/scripts/publish_github_release.sh" "$ARCHIVE" "${EXTRA[@]}"
fi
exit "$CODE"
