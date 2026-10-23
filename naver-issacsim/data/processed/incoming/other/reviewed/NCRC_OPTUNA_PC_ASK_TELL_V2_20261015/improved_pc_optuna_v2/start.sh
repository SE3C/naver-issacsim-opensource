#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
PYTHON_BIN="${PYTHON_BIN:-python}"
"$PYTHON_BIN" -c 'import optuna' || { echo 'Install dependencies with: python -m pip install -r requirements.txt'; exit 1; }
exec "$PYTHON_BIN" app.py --host 127.0.0.1 --port 8765
