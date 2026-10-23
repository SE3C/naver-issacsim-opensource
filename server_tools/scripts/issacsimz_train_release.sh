#!/usr/bin/env bash
# Personal NVIDIA/Brev use only: train through issacsimz, then mirror the
# resulting evidence archive to the private NVIDIA GitHub Releases page.
# Do not use on the official competition server.
set -Eeuo pipefail

die() { echo "[ERROR] $*" >&2; exit 1; }
info() { echo "[INFO] $*"; }

[[ $# -ge 1 ]] || die "Usage: $0 <h1|go2> --iters N --name NAME [issacsimz train options]"
ROBOT="$1"
shift
case "$ROBOT" in h1|go2) ;; *) die "robot must be h1 or go2";; esac

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYZ="${ISSACSIMZ_PYZ:-$HOME/issacsimz.pyz}"
LOG_ROOT="${ISSACSIMZ_LOG_ROOT:-$HOME/issacsimz-evidence}"
RELEASE_REPO="${ISSACSIMZ_RELEASE_REPO:-SE3C/naver-issacsim-nvidia}"
TASK_ROOT="${NVIDIA_TASK_ROOT:-$ROOT/training/$([[ "$ROBOT" == h1 ]] && echo humanoid || echo quadruped)}"
ISAACLAB_ROOT="${NVIDIA_ISAACLAB_ROOT:-${ISAACLAB_ROOT:-$HOME/IsaacLab}}"

[[ -f "$PYZ" ]] || die "issacsimz.pyz not found: $PYZ (set ISSACSIMZ_PYZ)"
[[ -f "$TASK_ROOT/train.py" ]] || die "task train.py not found: $TASK_ROOT"
[[ -x "$ISAACLAB_ROOT/isaaclab.sh" ]] || die "Isaac Lab launcher not found: $ISAACLAB_ROOT/isaaclab.sh"
command -v gh >/dev/null 2>&1 || die "gh is missing; run scripts/ncrc_l40s_prepare.sh first"
gh auth status --hostname github.com >/dev/null 2>&1 || die "GitHub CLI is not authenticated; run scripts/ncrc_l40s_prepare.sh before training"

mkdir -p "$LOG_ROOT"
runner_log="$(mktemp "$LOG_ROOT/${ROBOT}-release-wrapper.XXXXXX.log")"
cleanup() { rm -f "$runner_log"; }
trap cleanup EXIT

info "Personal NVIDIA archive mirror: $RELEASE_REPO"
info "issacsimz archive output: $LOG_ROOT/exports"
set +e
python3 "$PYZ" train "$ROBOT" --log-root "$LOG_ROOT" --task-root "$TASK_ROOT" --isaaclab-root "$ISAACLAB_ROOT" "$@" 2>&1 | tee "$runner_log"
train_code=${PIPESTATUS[0]}
set -e

archive="$(sed -n 's/^\[issacsimz\] archive=//p' "$runner_log" | tail -n 1)"
[[ -n "$archive" && -f "$archive" ]] || die "issacsimz did not produce an archive; no Release was created"
digest="${archive}.sha256"
pack_metadata="${archive}.metadata.json"
[[ -f "$digest" && -f "$pack_metadata" ]] || die "archive sidecars are missing; refusing Release upload"
python3 "$PYZ" verify "$archive" --require-sidecar

archive_name="$(basename "$archive")"
tag="private-${ROBOT}-${archive_name%.tar.gz}"
if gh release view "$tag" --repo "$RELEASE_REPO" >/dev/null 2>&1; then
  die "Release tag already exists: $tag (refusing to overwrite an existing backup)"
fi

notes="Personal NVIDIA/Brev evidence mirror. Canonical raw archive must also be preserved under naver-issacsim-originals/data/raw/private_server_runs/. issacsimz child exit: ${train_code}."
info "Uploading verified evidence archive to GitHub Release: $tag"
gh release create "$tag" "$archive" "$digest" "$pack_metadata" \
  --repo "$RELEASE_REPO" --title "$tag" --notes "$notes"
echo "[OK] Release: https://github.com/${RELEASE_REPO}/releases/tag/${tag}"
echo "[OK] Archive remains on the VM: $archive"

# Preserve the native/issacsimz training result: failed and interrupted runs
# are deliberately uploaded for analysis, but still return a non-zero status.
exit "$train_code"
