#!/usr/bin/env bash
# Personal-only Release mirror. The core Python sidecar never calls GitHub.
set -Eeuo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; STATE="${ISSACSIMZ_STATE_FILE:-$ROOT/.issacsimz-mode.env}"
source "$ROOT/scripts/python_runner.sh"
source "$ROOT/scripts/github_release_common.sh"
[[ -f "$STATE" ]] && source "$STATE"
die() { issacsimz_publish_die "$@"; }
[[ $# -ge 1 ]] || die "usage: $0 ARCHIVE.tar.gz [EXTRA_ASSET...]"
ARCHIVE="$1"; shift; EXTRA_ASSETS=("$@")
SHA="${ARCHIVE}.sha256"; META="${ARCHIVE}.metadata.json"
[[ -f "$ARCHIVE" && -f "$SHA" && -f "$META" ]] || die "archive and both sidecars are required"
for asset in "${EXTRA_ASSETS[@]}"; do [[ -f "$asset" ]] || die "extra asset missing: $asset"; done
PYZ="${ISSACSIMZ_PYZ:-$ROOT/dist/issacsimz.pyz}"; [[ -f "$PYZ" ]] || die "portable missing: $PYZ"
issacsimz_require_personal_github
PYTHON_RUNNER="$(issacsimz_find_python_runner "${ISSACSIMZ_PERSONAL_ISAACLAB_ROOT:-}")" || die "Python runner is unavailable"
"$PYTHON_RUNNER" "$PYZ" verify "$ARCHIVE" --require-sidecar --publishable
REPO="${ISSACSIMZ_PERSONAL_REPO:-SE3C/naver-issacsim-nvidia}"; RUN_ID="$(basename "${ARCHIVE%.tar.gz}")"
TAG="private-${RUN_ID}"; TITLE="$TAG"
NOTES="Personal NVIDIA/Brev evidence mirror. Preserve canonical raw separately."
if [[ -n "${ISSACSIMZ_RELEASE_EXPERIMENT:-}${ISSACSIMZ_RELEASE_CONFIG:-}" ]]; then
  [[ -n "${ISSACSIMZ_RELEASE_EXPERIMENT:-}" && -n "${ISSACSIMZ_RELEASE_CONFIG:-}" ]] || die "both release experiment and config are required"
  issacsimz_named_release "${ISSACSIMZ_RELEASE_ROBOT:-}" "$RUN_ID" train "$ISSACSIMZ_RELEASE_EXPERIMENT" "$ISSACSIMZ_RELEASE_CONFIG"
  TAG="$ISSACSIMZ_NAMED_TAG"; TITLE="$ISSACSIMZ_NAMED_TITLE"
  NOTES="Personal NVIDIA/Brev training evidence. Experiment: $ISSACSIMZ_RELEASE_EXPERIMENT. Final config display: $ISSACSIMZ_RELEASE_CONFIG. Evidence run/archive: $RUN_ID. Preserve canonical raw separately."
fi
issacsimz_require_new_release_tag "$REPO" "$TAG"
issacsimz_prepare_annotated_tag "${ISSACSIMZ_PERSONAL_ROOT:-/ephemeral/naver-issacsim-nvidia}" "$REPO" "$TAG" "$TITLE"
gh release create "$TAG" "$ARCHIVE" "$SHA" "$META" "${EXTRA_ASSETS[@]}" --repo "$REPO" --title "$TITLE" --notes "$NOTES"
issacsimz_verify_remote_assets "$REPO" "$TAG" "$ARCHIVE" "$SHA" "$META" "${EXTRA_ASSETS[@]}"
echo "[issacsimz] release=https://github.com/$REPO/releases/tag/$TAG"
