# H1 5k private-server preflight (historical direct-run guide)

This guide describes the private NVIDIA H1 baseline environment. It is not an
official submission procedure and must not be used to infer official scores.
The commands below are historical. For a new personal run, start with
`README.md` and `docs/H1_BREV_RUNBOOK.md`; use the current sidecar shell entry
points rather than calling a Python interpreter directly.

## Current logging boundary

`train.py` and `h1_task/_finalize.py` remain unchanged. For a new run, use the
public `issacsimz.pyz` sidecar from outside this repository. It records
evidence and mirrors numbered checkpoints while the native finalizer keeps its
normal cleanup behavior. Do not set `NCRC_KEEP_CHECKPOINTS`; that historical
environment switch has been removed.

`NO_AUTO_SUBMIT=1` is intentional only on the private server. `issacsimz train`
refuses that environment by default, so invoke `--allow-no-auto-submit` only
when the disabled backup is deliberate. Never carry that variable into an
official-server session.

## Static preflight

```bash
cd ~/naver-issacsim-nvidia
git pull --ff-only
export ISAACLAB_ROOT="$HOME/IsaacLab"
export ISAACLAB_PATH="$ISAACLAB_ROOT"
test -x "${ISAACLAB_ROOT}/isaaclab.sh"
nvidia-smi
```

The optional one-iteration server smoke is deliberately performed by the
operator, not by repository automation. Preserve its evidence separately from
the 5k baseline and never resume the baseline from a smoke run.

## Historical helpers

The `scripts/run_h1_brev_5k_baseline.sh` and recording helpers remain for
reproducing documented historical runs. New experiments should use the sidecar
for evidence capture and should verify source identity, native-run provenance,
checkpoint mirror, archive hash and rendered-video provenance before a result
claim.
