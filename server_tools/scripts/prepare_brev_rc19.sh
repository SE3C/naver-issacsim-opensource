#!/usr/bin/env bash
# Recreate the tested Brev/Linux environment for this repository.
# This intentionally does not commit or download training results.
set -Eeuo pipefail

ISAAC_SIM_VERSION="5.1.0-rc.19"
ISAAC_SIM_ARCHIVE_URL="https://downloads.isaacsim.nvidia.com/isaac-sim-standalone-5.1.0-linux-x86_64.zip"
ISAAC_SIM_ROOT="${ISAAC_SIM_ROOT:-/isaac-sim}"
ISAAC_SIM_CACHE_DIR="${ISAAC_SIM_CACHE_DIR:-${HOME}/.cache/isaac-sim}"
ISAACLAB_ROOT="${ISAACLAB_ROOT:-$HOME/IsaacLab}"
ISAACLAB_COMMIT="3e73d6dd79080fd7632488c061052a6edd52e230"

die() { echo "[ERROR] $*" >&2; exit 1; }
info() { echo "[INFO] $*"; }

[[ "$(uname -s)" == "Linux" ]] || die "Run this script inside Ubuntu/WSL/Linux, not PowerShell."

if [[ "${EUID}" -eq 0 ]]; then SUDO=""; else SUDO="sudo"; fi

info "Installing host tools"
${SUDO} apt-get update
${SUDO} env DEBIAN_FRONTEND=noninteractive apt-get install -y \
  aria2 curl git git-lfs tmux unzip build-essential cmake libglu1-mesa

mkdir -p "${ISAAC_SIM_CACHE_DIR}"
archive="${ISAAC_SIM_CACHE_DIR}/isaac-sim-standalone-5.1.0-linux-x86_64.zip"
archive_complete="${archive}.complete"

download_archive() {
  if command -v aria2c >/dev/null 2>&1; then
    info "Downloading Isaac Sim with aria2c (8 connections, resumable)"
    aria2c \
      --continue=true \
      --max-connection-per-server=8 \
      --split=8 \
      --min-split-size=16M \
      --file-allocation=none \
      --dir="${ISAAC_SIM_CACHE_DIR}" \
      --out="$(basename "${archive}")" \
      "${ISAAC_SIM_ARCHIVE_URL}"
  else
    info "aria2c unavailable; downloading Isaac Sim with resumable curl"
    curl --fail --location --retry 3 --continue-at - "${ISAAC_SIM_ARCHIVE_URL}" -o "${archive}"
  fi
  touch "${archive_complete}"
}

if [[ ! -f "${ISAAC_SIM_ROOT}/VERSION" ]] || ! grep -q "^${ISAAC_SIM_VERSION}" "${ISAAC_SIM_ROOT}/VERSION"; then
  if [[ -s "${archive}" && -f "${archive_complete}" ]]; then
    info "Using cached Isaac Sim archive: ${archive}"
  else
    info "Downloading or resuming Isaac Sim ${ISAAC_SIM_VERSION}"
    download_archive
  fi
  ${SUDO} mkdir -p "${ISAAC_SIM_ROOT}"
  ${SUDO} chown "$(id -u):$(id -g)" "${ISAAC_SIM_ROOT}"
  unzip -q -o "${archive}" -d "${ISAAC_SIM_ROOT}"
fi

grep -q "^${ISAAC_SIM_VERSION}" "${ISAAC_SIM_ROOT}/VERSION" || die "Isaac Sim version mismatch"
[[ -x "${ISAAC_SIM_ROOT}/python.sh" ]] || die "Isaac Sim python.sh is missing"

info "Running Isaac Sim post-install"
(cd "${ISAAC_SIM_ROOT}" && ./post_install.sh)

if [[ ! -d "${ISAACLAB_ROOT}/.git" ]]; then
  info "Cloning Isaac Lab"
  git clone https://github.com/isaac-sim/IsaacLab.git "${ISAACLAB_ROOT}"
fi

info "Checking out Isaac Lab ${ISAACLAB_COMMIT}"
git -C "${ISAACLAB_ROOT}" fetch --tags origin
git -C "${ISAACLAB_ROOT}" checkout "${ISAACLAB_COMMIT}"
ln -sfn "${ISAAC_SIM_ROOT}" "${ISAACLAB_ROOT}/_isaac_sim"

info "Installing Isaac Lab core and RSL-RL dependencies"
(cd "${ISAACLAB_ROOT}" && ./isaaclab.sh -i rsl_rl)

info "Verifying tested Python/GPU combination"
"${ISAAC_SIM_ROOT}/python.sh" -c \
  'import torch, isaaclab, rsl_rl; print(torch.__version__); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0)); print(isaaclab.__file__); print(rsl_rl.__file__)'

cat <<EOF

[OK] Environment ready.
Isaac Sim : ${ISAAC_SIM_ROOT}
Isaac Lab : ${ISAACLAB_ROOT}
Isaac Lab commit : ${ISAACLAB_COMMIT}

Next, from this repository:
  export ISAACLAB_PATH="${ISAACLAB_ROOT}"
  ./scripts/run_h1_rc19.sh --num_envs 4096 --max_iterations 200
EOF
