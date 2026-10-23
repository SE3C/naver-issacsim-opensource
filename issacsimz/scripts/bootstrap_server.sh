#!/usr/bin/env bash
# Configure a personal NVIDIA/Brev or official competition-server shell.
set -Eeuo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$ROOT/scripts/python_runner.sh"
MODE=""; LOCAL_ONLY=0; CONFIG="${ISSACSIMZ_CONFIG:-$ROOT/config/issacsimz.conf}"
die() { echo "[issacsimz] ERROR: $*" >&2; exit 2; }
while (( $# )); do case "$1" in --mode) MODE="${2:-}"; shift 2;; --local-only) LOCAL_ONLY=1; shift;; --config) CONFIG="${2:-}"; shift 2;; *) die "usage: $0 --mode personal|official [--local-only] [--config PATH]";; esac; done
[[ "$MODE" == personal || "$MODE" == official ]] || die "--mode personal or official is required"
[[ "$LOCAL_ONLY" == 0 || "$MODE" == personal ]] || die "--local-only is personal-only"
[[ -f "$CONFIG" ]] && source "$CONFIG"
STATE="${ISSACSIMZ_STATE_FILE:-$ROOT/.issacsimz-mode.env}"; PYZ="${ISSACSIMZ_PYZ:-$ROOT/dist/issacsimz.pyz}"
MANIFEST="${ISSACSIMZ_MANIFEST_ROOT:-$HOME/issacsimz-server-manifest}"
find_isaaclab() {
  local explicit="${1:-}" candidate
  [[ -n "$explicit" && -x "$explicit/isaaclab.sh" ]] && { printf '%s\n' "$explicit"; return; }
  for candidate in "${ISAACLAB_ROOT:-}" /workspace/IsaacLab "$HOME/IsaacLab" /ephemeral/IsaacLab; do
    [[ -n "$candidate" && -x "$candidate/isaaclab.sh" ]] && { printf '%s\n' "$candidate"; return; }
  done
  for candidate in /ephemeral "$HOME" /workspace; do
    [[ -d "$candidate" ]] || continue
    find "$candidate" -maxdepth 5 -type f -name isaaclab.sh -print -quit 2>/dev/null | while read -r path; do dirname "$path"; done
  done | head -n 1
}
if [[ "$MODE" == official ]]; then
  # GitHub is deliberately unavailable to all bootstrap/doctor subprocesses.
  unset GH_TOKEN GITHUB_TOKEN
  EVIDENCE="${ISSACSIMZ_EVIDENCE_ROOT:-$HOME/issacsimz-evidence}"
  [[ -z "${ISSACSIMZ_OFFICIAL_H1_ROOT:-}" || "${ISSACSIMZ_OFFICIAL_H1_ROOT%/}" == "/workspace/training/humanoid" ]] || die "official H1 root override is disabled"
  [[ -z "${ISSACSIMZ_OFFICIAL_GO2_ROOT:-}" || "${ISSACSIMZ_OFFICIAL_GO2_ROOT%/}" == "/workspace/training/quadruped" ]] || die "official Go2 root override is disabled"
  [[ -z "${ISSACSIMZ_OFFICIAL_ISAACLAB_ROOT:-}" || "${ISSACSIMZ_OFFICIAL_ISAACLAB_ROOT%/}" == "/workspace/IsaacLab" ]] || die "official IsaacLab root override is disabled"
  H1_ROOT="/workspace/training/humanoid"
  GO2_ROOT="/workspace/training/quadruped"
  ISAACLAB_ROOT="/workspace/IsaacLab"
  echo "[issacsimz] MODE=official; GitHub is disabled by profile"
else
  command -v nvidia-smi >/dev/null || die "personal mode requires nvidia-smi"
  PERSONAL_ROOT="${ISSACSIMZ_PERSONAL_ROOT:-/ephemeral/naver-issacsim-nvidia}"
  PERSONAL_REPO="${ISSACSIMZ_PERSONAL_REPO:-SE3C/naver-issacsim-nvidia}"
  if [[ "$LOCAL_ONLY" == 1 ]]; then
    [[ -d "$PERSONAL_ROOT" ]] || die "local personal root does not exist: $PERSONAL_ROOT"
    [[ -f "$PERSONAL_ROOT/training/humanoid/train.py" ]] || die "local H1 task root is missing: $PERSONAL_ROOT/training/humanoid/train.py"
    [[ -f "$PERSONAL_ROOT/training/quadruped/train.py" ]] || die "local Go2 task root is missing: $PERSONAL_ROOT/training/quadruped/train.py"
    [[ ! -f "$PERSONAL_ROOT/submit_config.txt" ]] || die "local-only mode refuses task submit_config.txt; remove it from the supplied task checkout"
    echo "[issacsimz] MODE=personal LOCAL_ONLY=1; GitHub auth, task checkout updates, publishing, and submit upload disabled"
  else
    command -v gh >/dev/null || die "personal mode requires GitHub CLI"
    if ! gh auth status --hostname github.com >/dev/null 2>&1; then
      echo "[issacsimz] GitHub authentication required; starting gh web login"
      gh auth login --hostname github.com --git-protocol ssh
    fi
    gh auth status --hostname github.com >/dev/null || die "GitHub authentication did not complete"
    if [[ -d "$PERSONAL_ROOT/.git" ]]; then git -C "$PERSONAL_ROOT" pull --ff-only
    elif [[ ! -e "$PERSONAL_ROOT" ]]; then gh repo clone "$PERSONAL_REPO" "$PERSONAL_ROOT"
    else die "personal root exists but is not a git checkout: $PERSONAL_ROOT"; fi
    if [[ -z "$(git -C "$PERSONAL_ROOT" config user.name || true)" ]]; then
      GIT_NAME="$(gh api user --jq '.login')" || die "could not read GitHub login for Git tag identity"
      [[ -n "$GIT_NAME" ]] || die "GitHub login is empty; configure Git user.name"
      git -C "$PERSONAL_ROOT" config user.name "$GIT_NAME"
    fi
    git -C "$PERSONAL_ROOT" config user.email "nc""rcissacsimz@users.noreply.github.com"
    echo "[issacsimz] MODE=personal; GitHub Release mirror enabled"
  fi
  H1_ROOT="$PERSONAL_ROOT/training/humanoid"; GO2_ROOT="$PERSONAL_ROOT/training/quadruped"
  ISAACLAB_ROOT="$(find_isaaclab "${ISSACSIMZ_PERSONAL_ISAACLAB_ROOT:-}")"
  [[ -n "$ISAACLAB_ROOT" && -x "$ISAACLAB_ROOT/isaaclab.sh" ]] || die "could not find IsaacLab isaaclab.sh; set ISSACSIMZ_PERSONAL_ISAACLAB_ROOT"
  EVIDENCE="${ISSACSIMZ_EVIDENCE_ROOT:-${ISSACSIMZ_PERSONAL_EVIDENCE:-$HOME/issacsimz-evidence}}"
fi
PYTHON_RUNNER="$(issacsimz_find_python_runner "$ISAACLAB_ROOT")" || die "Python runner is unavailable"
export ISSACSIMZ_PYTHON_RUNNER="$PYTHON_RUNNER"
mkdir -p "$EVIDENCE"
if command -v tmux >/dev/null 2>&1; then
  echo "[issacsimz] tmux=$(command -v tmux)"
else
  echo "[issacsimz] WARNING: tmux not found; long-running training is not protected"
fi
if [[ "${ISSACSIMZ_SKIP_BUILD:-0}" != 1 ]]; then bash "$ROOT/scripts/build_portable.sh"; fi
[[ -f "$PYZ" ]] || die "portable missing: $PYZ"
mkdir -p "$MANIFEST"
{
  printf 'mode=%s\nstarted_utc=%s\n' "$MODE" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} > "$MANIFEST/mode.txt"
{
  date -u; uname -a; [[ -f /etc/os-release ]] && cat /etc/os-release; df -h
  printf 'evidence=%s\nh1_root=%s\ngo2_root=%s\nisaaclab_root=%s\n' "$EVIDENCE" "$H1_ROOT" "$GO2_ROOT" "$ISAACLAB_ROOT"
} > "$MANIFEST/environment.txt"
nvidia-smi > "$MANIFEST/nvidia-smi.txt" 2>&1 || true
"$PYTHON_RUNNER" --version > "$MANIFEST/python.txt" 2>&1 || true
"$PYTHON_RUNNER" -m pip freeze > "$MANIFEST/pip-packages.txt" 2>&1 || true
printf '%s\n' "$ISAACLAB_ROOT" > "$MANIFEST/isaaclab-path.txt"
git -C "$ISAACLAB_ROOT" rev-parse HEAD > "$MANIFEST/isaaclab-commit.txt" 2>&1 || true
if [[ -d "${PERSONAL_ROOT:-}/.git" ]]; then
  git -C "$PERSONAL_ROOT" rev-parse HEAD > "$MANIFEST/naver-repo-commit.txt"
  git -C "$PERSONAL_ROOT" remote -v > "$MANIFEST/naver-repo-remote.txt"
else
  printf 'not a personal git checkout\n' > "$MANIFEST/naver-repo-commit.txt"
  printf 'not a personal git checkout\n' > "$MANIFEST/naver-repo-remote.txt"
fi
if git -C "$ROOT" rev-parse HEAD > "$MANIFEST/issacsimz-commit.txt" 2>/dev/null; then
  :
else
  printf 'git metadata unavailable\n' > "$MANIFEST/issacsimz-commit.txt"
fi
{
  "$PYTHON_RUNNER" "$PYZ" doctor --robot h1 --task-root "$H1_ROOT" --isaaclab-root "$ISAACLAB_ROOT" --log-root "$EVIDENCE"
  "$PYTHON_RUNNER" "$PYZ" doctor --robot go2 --task-root "$GO2_ROOT" --isaaclab-root "$ISAACLAB_ROOT" --log-root "$EVIDENCE"
} 2>&1 | tee "$MANIFEST/bootstrap-validation.txt"
cat > "$STATE" <<EOF
ISSACSIMZ_MODE="$MODE"
ISSACSIMZ_PYZ="$PYZ"
ISSACSIMZ_PYTHON_RUNNER="$PYTHON_RUNNER"
ISSACSIMZ_EVIDENCE_ROOT="$EVIDENCE"
ISSACSIMZ_H1_ROOT="$H1_ROOT"
ISSACSIMZ_GO2_ROOT="$GO2_ROOT"
ISSACSIMZ_ISAACLAB_ROOT="$ISAACLAB_ROOT"
EOF
if [[ "$MODE" == personal ]]; then
cat >> "$STATE" <<EOF
ISSACSIMZ_PERSONAL_ROOT="${PERSONAL_ROOT:-/ephemeral/naver-issacsim-nvidia}"
ISSACSIMZ_PERSONAL_REPO="${PERSONAL_REPO:-SE3C/naver-issacsim-nvidia}"
ISSACSIMZ_PERSONAL_ISAACLAB_ROOT="$ISAACLAB_ROOT"
ISSACSIMZ_LOCAL_ONLY="$LOCAL_ONLY"
EOF
else
cat >> "$STATE" <<EOF
ISSACSIMZ_OFFICIAL_H1_ROOT="$H1_ROOT"
ISSACSIMZ_OFFICIAL_GO2_ROOT="$GO2_ROOT"
ISSACSIMZ_OFFICIAL_ISAACLAB_ROOT="$ISAACLAB_ROOT"
EOF
fi
chmod 600 "$STATE"
echo "[issacsimz] manifest=$MANIFEST"
if [[ "$MODE" == personal ]]; then
  echo "[issacsimz] READY: ./issacsimz train go2 --iters 1 --num-envs 64 --name smoke-go2 (local smoke; no Release)"
  echo "[issacsimz] Long runs: ./scripts/issacsimz_tmux_train.sh go2 --iters 5000 --envs 4096 --name go2-run"
else
  echo "[issacsimz] READY: ./scripts/issacsimz_tmux_train.sh go2 --iters 1 --envs 64 --name smoke-go2"
fi
