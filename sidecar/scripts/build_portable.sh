#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$ROOT/scripts/python_runner.sh"
PYTHON_RUNNER="$(issacsimz_find_python_runner "${ISSACSIMZ_ISAACLAB_ROOT:-${ISSACSIMZ_PERSONAL_ISAACLAB_ROOT:-${ISSACSIMZ_OFFICIAL_ISAACLAB_ROOT:-}}}")" || exit 2
OUT="${ROOT}/dist"
STAGE="$(mktemp -d)"
trap 'rm -rf "${STAGE}"' EXIT

mkdir -p "${STAGE}/issacsimz_cli" "${OUT}"
cd "${ROOT}"
"$PYTHON_RUNNER" -m unittest discover -v
"$PYTHON_RUNNER" -m py_compile issacsimz_cli/*.py
cp "${ROOT}"/issacsimz_cli/*.py "${STAGE}/issacsimz_cli/"
printf '%s\n' 'from issacsimz_cli.cli import main' 'raise SystemExit(main())' > "${STAGE}/__main__.py"
"$PYTHON_RUNNER" -m zipapp "${STAGE}" -o "${OUT}/issacsimz.pyz"
chmod 0755 "${OUT}/issacsimz.pyz"
sha256sum "${OUT}/issacsimz.pyz" > "${OUT}/SHA256SUMS"
"$PYTHON_RUNNER" "${OUT}/issacsimz.pyz" doctor
(cd "${OUT}" && sha256sum --check SHA256SUMS)
echo "Built ${OUT}/issacsimz.pyz"
