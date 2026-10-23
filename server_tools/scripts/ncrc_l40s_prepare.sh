#!/usr/bin/env bash
# Run after the Brev Setup Script from an interactive VM terminal.
# This companion does GitHub CLI web authentication only: no clone, source
# modification, training, upload, Release, stop, or VM deletion.
set -Eeuo pipefail
die() { echo "[ERROR] $*" >&2; exit 1; }
command -v gh >/dev/null 2>&1 || die "gh is missing; run the Brev Setup Script first"
if ! gh auth status --hostname github.com >/dev/null 2>&1; then
  echo "[INFO] Starting GitHub CLI web login"
  gh auth login --hostname github.com --git-protocol https --web
fi
gh auth status --hostname github.com
echo "[OK] GitHub CLI authentication is ready. No repository or training action was performed."
