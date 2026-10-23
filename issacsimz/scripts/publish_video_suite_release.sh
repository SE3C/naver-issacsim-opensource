#!/usr/bin/env bash
# Explicit PERSONAL-only publisher for an inspected six-terrain video suite.
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE="${ISSACSIMZ_STATE_FILE:-$ROOT/.issacsimz-mode.env}"
[[ -f "$STATE" ]] && source "$STATE"
source "$ROOT/scripts/python_runner.sh"
source "$ROOT/scripts/github_release_common.sh"

SUITE_DIR=""
TAG=""
TITLE=""
NOTES=""
NOTES_FILE=""
REPO="${ISSACSIMZ_PERSONAL_REPO:-SE3C/naver-issacsim-nvidia}"
while (( $# )); do
  case "$1" in
    --suite-dir) [[ $# -ge 2 ]] || issacsimz_publish_die "--suite-dir requires a value"; SUITE_DIR="$2"; shift 2 ;;
    --tag) [[ $# -ge 2 ]] || issacsimz_publish_die "--tag requires a value"; TAG="$2"; shift 2 ;;
    --title) [[ $# -ge 2 ]] || issacsimz_publish_die "--title requires a value"; TITLE="$2"; shift 2 ;;
    --notes) [[ $# -ge 2 ]] || issacsimz_publish_die "--notes requires a value"; NOTES="$2"; shift 2 ;;
    --notes-file) [[ $# -ge 2 ]] || issacsimz_publish_die "--notes-file requires a value"; NOTES_FILE="$2"; shift 2 ;;
    --repo) [[ $# -ge 2 ]] || issacsimz_publish_die "--repo requires a value"; REPO="$2"; shift 2 ;;
    *) issacsimz_publish_die "unknown option: $1" ;;
  esac
done

[[ -n "$SUITE_DIR" && -n "$TAG" && -n "$TITLE" ]] ||
  issacsimz_publish_die "usage: $0 --suite-dir DIR --tag TAG --title TITLE (--notes TEXT | --notes-file FILE) [--repo OWNER/REPO]"
issacsimz_require_personal_github
[[ -d "$SUITE_DIR" ]] || issacsimz_publish_die "suite directory is missing: $SUITE_DIR"
[[ -n "$NOTES" || -n "$NOTES_FILE" ]] || issacsimz_publish_die "--notes or --notes-file is required"
[[ -z "$NOTES" || -z "$NOTES_FILE" ]] || issacsimz_publish_die "use only one of --notes and --notes-file"
[[ -z "$NOTES_FILE" || -f "$NOTES_FILE" ]] || issacsimz_publish_die "notes file is missing: $NOTES_FILE"

LAB_ROOT="${ISSACSIMZ_ISAACLAB_ROOT:-${ISSACSIMZ_PERSONAL_ISAACLAB_ROOT:-}}"
PYTHON_RUNNER="$(issacsimz_find_python_runner "$LAB_ROOT")" || issacsimz_publish_die "Python runner is unavailable"
SUITE_DIR="$(cd "$SUITE_DIR" && pwd)"
DOWNLOAD_ROOT="$(dirname "$SUITE_DIR")"
SUITE_NAME="$(basename "$SUITE_DIR")"
ARCHIVE="$DOWNLOAD_ROOT/$SUITE_NAME-download.tar.gz"
ARCHIVE_SHA="$ARCHIVE.sha256"

"$PYTHON_RUNNER" "$ROOT/scripts/video_suite_artifacts.py" verify \
  --suite-dir "$SUITE_DIR" --archive "$ARCHIVE" --archive-sidecar "$ARCHIVE_SHA" ||
  issacsimz_publish_die "video suite integrity verification failed"
mapfile -t VIDEO_RELATIVES < <("$PYTHON_RUNNER" "$ROOT/scripts/video_suite_artifacts.py" list-assets --suite-dir "$SUITE_DIR")
[[ "${#VIDEO_RELATIVES[@]}" -eq 6 ]] || issacsimz_publish_die "expected exactly six suite videos"
ASSETS=()
for relative in "${VIDEO_RELATIVES[@]}"; do ASSETS+=("$SUITE_DIR/$relative"); done
ASSETS+=("$SUITE_DIR/video_suite_manifest.json" "$SUITE_DIR/SHA256SUMS" "$ARCHIVE" "$ARCHIVE_SHA")
for asset in "${ASSETS[@]}"; do [[ -f "$asset" ]] || issacsimz_publish_die "asset missing: $asset"; done

issacsimz_require_new_release_tag "$REPO" "$TAG"
issacsimz_prepare_annotated_tag "${ISSACSIMZ_PERSONAL_ROOT:-/ephemeral/naver-issacsim-nvidia}" "$REPO" "$TAG" "$TITLE"
CREATE_ARGS=(release create "$TAG" "${ASSETS[@]}" --repo "$REPO" --title "$TITLE")
if [[ -n "$NOTES_FILE" ]]; then CREATE_ARGS+=(--notes-file "$NOTES_FILE"); else CREATE_ARGS+=(--notes "$NOTES"); fi
gh "${CREATE_ARGS[@]}"
issacsimz_verify_remote_assets "$REPO" "$TAG" "${ASSETS[@]}"
echo "[issacsimz] video_suite_release=https://github.com/$REPO/releases/tag/$TAG"
