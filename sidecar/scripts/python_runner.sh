#!/usr/bin/env bash

issacsimz_find_python_runner() {
  local isaaclab_root="${1:-}" configured="${ISSACSIMZ_PYTHON_RUNNER:-}" candidate resolved

  if [[ -n "$configured" ]]; then
    if [[ "$configured" == */* && -x "$configured" ]]; then
      printf '%s\n' "$configured"
      return 0
    fi
    if [[ "$configured" != */* ]] && resolved="$(command -v -- "$configured" 2>/dev/null)"; then
      printf '%s\n' "$resolved"
      return 0
    fi
    printf '[issacsimz] ERROR: configured Python runner is unavailable: %s\n' "$configured" >&2
    return 1
  fi

  if resolved="$(command -v python3 2>/dev/null)"; then
    printf '%s\n' "$resolved"
    return 0
  fi

  for candidate in \
    "${isaaclab_root:+$isaaclab_root/_isaac_sim/python.sh}" \
    "${isaaclab_root:+$isaaclab_root/../isaac-sim/python.sh}" \
    /workspace/IsaacLab/_isaac_sim/python.sh \
    /workspace/isaac-sim/python.sh \
    /isaac-sim/python.sh \
    "${HOME:+$HOME/IsaacLab/_isaac_sim/python.sh}" \
    /ephemeral/IsaacLab/_isaac_sim/python.sh; do
    if [[ -n "$candidate" && -x "$candidate" ]]; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done

  printf '[issacsimz] ERROR: Python runner not found; install python3 or provide IsaacLab/Isaac Sim python.sh\n' >&2
  return 1
}
