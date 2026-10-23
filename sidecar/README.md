# issacsimz

## Distribution setup note

Run this document's relative commands from the `sidecar/` directory.
The training, bootstrap and video examples below are operational commands,
not CPU verification steps. They require a separately provisioned simulator
and authorized external task checkout; do not execute them just to validate
this source distribution. CPU fixtures are described in `tests/README.md`.

Historical personal-mode defaults still refer to the original external
training checkout and publishing repository. Before using personal bootstrap
or a publisher, explicitly configure your own `ISSACSIMZ_PERSONAL_REPO`,
`ISSACSIMZ_PERSONAL_ROOT` and the publisher's target options. Do not expect
this combined repository to contain a `training/` tree. The examples are not
permission to access another repository, upload artifacts or change a server.
The code license is pending; see the distribution root for publication status.

`issacsimz` is a dependency-free sidecar CLI for preserving evidence from an
existing Isaac Sim run. It runs a command without modifying its source,
records console and mode-appropriate evidence, and creates a verified
`.tar.gz` archive on either success or failure. Personal mode also mirrors
stable checkpoints and records periodic GPU telemetry.

This is an unofficial community tool. It is not affiliated with NVIDIA.

## What it does not do

- It does not provide training tasks, reward functions, simulator settings, or
  Isaac Lab installation scripts.
- It does not edit the command it launches or delete/move native checkpoints.
- It has no third-party Python dependencies.

`Ctrl+C` is intentionally conservative: the first signal is forwarded once to
the launched process group and `issacsimz` then waits for the native
`train.py` finalizer and any official backup to finish. In official mode,
additional Ctrl+C signals are ignored so the sidecar cannot force-stop native
finalization. Personal mode retains the second-Ctrl+C force-stop escape hatch.

## Quick start

Bootstrap the server mode once, then use the task-aware wrapper. It resolves
the Python runner, training working directory, and native run parent:

```bash
bash scripts/bootstrap_server.sh --mode official
bash scripts/issacsimz_train.sh h1 --iters 1 --envs 64 --name smoke-h1
bash scripts/issacsimz_train.sh go2 --iters 1 --envs 64 --name smoke-go2
```

Bootstrap writes the selected mode's canonical paths into `.issacsimz-mode.env`
as `ISSACSIMZ_H1_ROOT`, `ISSACSIMZ_GO2_ROOT`, and
`ISSACSIMZ_ISAACLAB_ROOT`. After bootstrap, `./issacsimz doctor --robot h1`
therefore uses the selected H1 task root without a repeated `--task-root`.
Mode-specific variables remain bootstrap inputs and metadata; doctor, reward,
train, and video consume the generic selected-path variables.

For a long official-server run, use the detached tmux launcher. It starts the
same `train` command inside tmux and immediately returns the shell; it does
not alter training, evidence, finalization, or official backup behavior.

```bash
bash scripts/issacsimz_tmux_train.sh go2 \
  --iters 5000 --envs 4096 --name go2-final
```

Attach with `tmux attach -t issacsimz-go2-go2-final` and detach with
`Ctrl-B`, then `D`. To stop safely, attach and press `Ctrl-C` once so the
native finalizer and evidence archive can finish. Do not use `tmux
kill-session` as a normal stopping method. `--tmux-session NAME` supplies an
explicit safe session name. If the command is already inside tmux, it runs in
that existing session instead of nesting another one. Foreground `train` is
still appropriate for a short smoke run or debugging.

If `NO_AUTO_SUBMIT` exists in the environment, `train` refuses by default so
an official backup cannot be accidentally suppressed. On an intentional
private run only, acknowledge that choice with `--allow-no-auto-submit`.
`SUBMIT_DEBUG` is handled the same way because console evidence may otherwise
contain unnecessary server details; use `--allow-submit-debug` only on an
intentional private run. Both acknowledgement flags are rejected in official
mode. This is presence-based: even `NAME=0` is active,
matching the native finalizer's Python truth test.

Profile `train`, `play`, and `video` are fail-closed when `ISSACSIMZ_MODE` is
missing or invalid. Generic `run` and `watch` additionally require explicit
`personal` mode. Use bootstrap plus the provided wrappers; invoking the portable
command directly without mode state cannot silently enable personal monitoring
or checkpoint behavior on an official task tree. Generic `run` remains
available for explicitly assembled non-profile commands in personal mode and
is rejected in official mode.

The default paths are intentionally task-relative:

```text
H1 root:  /workspace/training/humanoid
H1 runs:  /workspace/training/humanoid/logs/rsl_rl/humanoid/
Go2 root: /workspace/training/quadruped
Go2 runs: /workspace/training/quadruped/logs/rsl_rl/quadruped/
```

In official mode these roots are fixed to the paths above and
`/workspace/IsaacLab`; environment, config, and CLI overrides are rejected.
In personal mode, override a nonstandard layout with `--task-root` and
`--isaaclab-root`. An
explicit path is strict: if its expected `train.py` or `isaaclab.sh` is
missing, the command fails immediately instead of falling back to an
environment variable or default. If the native run cannot be found, `train`
emits a warning; do not treat that archive as complete evidence.

For a different Isaac Sim project, run an existing training command and record
it externally:

```bash
./issacsimz run \
  --name baseline \
  --run-root /workspace/logs/rsl_rl/humanoid \
  --collect /workspace/training/humanoid/exported \
  -- /workspace/IsaacLab/isaaclab.sh -p train.py --task Humanoid-v0 --headless
```

The evidence directory contains `metadata.json`, `command.txt`, `console.log`,
`system/`, `native_run/`, `collected/`, and `SHA256SUMS`. Personal mode also
contains `checkpoints/`, `watcher.log`, and `system/nvidia_smi_during.csv`.
Official mode does not start the generic checkpoint watcher or GPU sampler.
It starts a separate organizer-derived keep-all shell procedure during profile
training. Its run-specific checkpoint copies are included in the evidence
archive. One-shot `nvidia-smi` snapshots before and after the command remain.
An archive is created by default, including for a failed or interrupted
command. Suffixes are `_FAILED.tar.gz` and `_INTERRUPTED.tar.gz`. Existing
archives are never overwritten without `pack --force`; packing also checks a
free-space margin and writes `.sha256` plus `.metadata.json` sidecars.

For profile training, `source/identity.json` records before/after SHA-256 for
the train/play/reward/finalize/config files and stores a reward snapshot.
`validation.json` separately reports native run, TensorBoard, source identity,
collection and official-backup checks as PASS/WARN/FAIL. Personal mode also
reports the checkpoint mirror. For a completed official profile training run,
fresh `model_best.pt`, fresh `env.yaml`, a native TensorBoard event and completed
finalize are required for a clean PASS. The organizer checkpoint keeper must
also exit successfully and preserve at least one checkpoint; a generic mirrored
checkpoint is not required.
Official finalize start and completion are tracked separately from the child
exit code and official backup status.

`collected/provenance.json` records every collected file as `NEW`, `MODIFIED`,
or `UNCHANGED`, using size, mtime and SHA-256 before and after the command.
Only `NEW` and `MODIFIED` files are copied into the evidence archive, so stale
policies, videos and exports are not presented as current-run outputs.
Credential-like files such as `submit_config.txt`, `.env`, private keys and
secret/token files are excluded from broad native/collection copies. Backup
environment metadata records presence booleans only, never credential values.

Only one `train` process per H1/Go2 profile is allowed by a PID lock. A live
lock is never overridden. `--force-unlock` is accepted only for a stale PID.

In personal mode, use a watcher independently when another process starts the
training. Official mode rejects `watch`. Both profile train modes pass
`agent.save_interval=50` to native `train.py` without editing its source.
During official profile training, `scripts/organizer_keep_all_ckpt.sh` copies
stable `model_*.pt` files from the current native run into
`backup_log/<native-run>/`. It adapts the organizer's public keep-all procedure
for run-specific orchestration; it is not a verbatim organizer file or the
generic `CheckpointWatcher`. This distribution omits the historical
organizer-provided verbatim keeper and its archival byte-identity test.
The run-specific keep-all workflow remains included.
Check the copied checkpoint count and iterations after training. Official
still creates the normal evidence `.tar.gz` and local
`<RUN_ID>-download.tar.gz` automatically, with no external publisher.

```bash
./issacsimz watch --run-dir /path/to/native/run --destination ./checkpoints --all
```

Build a portable standard-library-only executable archive:

```bash
bash scripts/build_portable.sh
```

The shell entry points select `python3` when available. Otherwise they use an
executable Isaac Lab/Isaac Sim `python.sh`, including
`<isaaclab-root>/_isaac_sim/python.sh`. Bootstrap stores the selected runner
for train, video, build, and personal publishing wrappers. Set
`ISSACSIMZ_PYTHON_RUNNER` only when an explicit runner is required; an invalid
explicit runner fails instead of being ignored. The build script runs `doctor`
with the selected runner after creating the zipapp.

## Personal vs official orchestration

The Python core never calls GitHub. Optional shell wrappers make the mode
explicit and keep personal GitHub mirroring outside the sidecar itself.

On a personal VM, create the public checkout on first use:

```bash
cd /ephemeral
git clone https://codeberg.org/passerby1/issacsimz.git issacsimz
```

On a later session, update that checkout instead of cloning it again:

```bash
git -C /ephemeral/issacsimz pull --ff-only
```

Then run bootstrap from `/ephemeral/issacsimz`. Standard PERSONAL bootstrap checks
GitHub CLI authentication, starts `gh auth login` only when needed, and clones or
fast-forward pulls the private NVIDIA task checkout. It configures Git tag identity
only in that checkout; it does not change global Git settings. Inspect local
changes if a pull cannot fast-forward; do not discard them automatically.

For a supplied local NVIDIA training checkout, use `--local-only`. Set
`ISSACSIMZ_PERSONAL_ROOT` to its root (the directory containing `training/`) and
`ISSACSIMZ_PERSONAL_ISAACLAB_ROOT` to the IsaacLab directory. This branch requires
both `training/humanoid/train.py` and `training/quadruped/train.py`, performs no
GitHub authentication or task checkout update, disables automatic Release
publishing through the training wrapper, and prevents the native submit upload
through that wrapper. It refuses a root
`submit_config.txt`; the train wrapper also removes `SUBMIT_HOST` and
`SUBMIT_TOKEN` from the training environment.

```bash
# Personal NVIDIA/Brev only: checks gh auth, updates the private task source,
# builds the portable, and enables Release mirroring.
bash scripts/bootstrap_server.sh --mode personal

# Supplied local NVIDIA checkout; no GitHub auth, checkout update, or auto-publish.
ISSACSIMZ_PERSONAL_ROOT=/path/to/naver-issacsim-nvidia \
ISSACSIMZ_PERSONAL_ISAACLAB_ROOT=/home/shadeform/IsaacLab \
  bash scripts/bootstrap_server.sh --mode personal --local-only

# Official server: does not invoke gh or GitHub operations and clears GH_TOKEN
# and GITHUB_TOKEN for its subprocesses.
bash scripts/bootstrap_server.sh --mode official

# Personal NVIDIA/Brev long run: the entire existing wrapper is inside tmux,
# so evidence, archive, and personal Release publishing still finish there.
./scripts/issacsimz_tmux_train.sh go2 --iters 1000 --envs 4096 --name go2-test-001

# Foreground personal smoke/debug run: local evidence only, no Release publisher.
./issacsimz train go2 --iters 1 --num-envs 64 --name smoke-go2

# After inspecting a preserved train run, render a separate video evidence run.
./scripts/issacsimz_video.sh go2 --from-run 20260913-xxxx-go2-test-001

# Personal mode only: render six profile-specific terrain views, verify them,
# then publish one suite Release automatically.
./scripts/issacsimz_video_suite.sh go2 --from-run 20260913-xxxx-go2-test-001
./scripts/issacsimz_video_suite.sh h1 --from-run 20260913-xxxx-h1-test-001

# Render the same six views from a numbered checkpoint selected after a resume.
./scripts/issacsimz_video_suite.sh h1 --checkpoint /workspace/training/humanoid/logs/rsl_rl/.../model_4997.pt

# Generate locally for review without publishing.
./scripts/issacsimz_video_suite.sh h1 --checkpoint /path/to/model_4700.pt --no-publish

# Publish an already reviewed suite separately with a custom tag/title/notes.
./scripts/publish_video_suite_release.sh \
  --suite-dir /home/shadeform/ISSACSIMZ_DOWNLOAD/<RUN_ID> \
  --tag <TAG> --title "<TITLE>" --notes-file ./release-notes.md

# To customize the automatic Release details, render and publish in one command.
./scripts/issacsimz_video_suite.sh h1 --checkpoint /path/to/model_4700.pt \
  --publish --tag <TAG> --title "<TITLE>" --notes-file ./release-notes.md
```

Personal train Releases upload the archive plus its `.sha256` and
`.metadata.json` sidecars. Personal video Releases additionally expose the
fresh `play_video.mp4` and `video_manifest.json`; they are separate from the
parent train Release. Official mode never invokes the publisher; official
backup remains owned by the native `train.py`/`_finalize.py` flow. Copy `config/issacsimz.conf.example` to
`config/issacsimz.conf` only for non-secret path overrides.

For PERSONAL train wrappers and automatic six-video suites, optional
`--release-experiment exp-go2-gait-stability --release-config 'g2-submit-3 + feet=0.03'`
sets the Release tag/title/notes without changing evidence or checkpoint selection.
Use `exp-h1-...` with `h1-submit-N`, or `exp-go2-...` with `g2-submit-N`;
the robot CLI name remains `go2`. Supply both options together. The suite
accepts them only with automatic publish, not `--no-publish` or manual `--publish`.
Omitting them preserves the existing Release name.

## Local download handoff

After a profile train run is finalized, the sidecar creates a small download
folder without changing or moving canonical evidence. It copies the available
train archive and its `.sha256` and `.metadata.json` sidecars, plus available
`model_best.pt`, `env.yaml`, and `report.html` when validation is not FAIL.
If validation is FAIL, the handoff contains the evidence archive and sidecars
but excludes those loose exported files. Missing optional files do not turn
finalization into a failure. A successful video run also copies
`play_video.mp4` into the parent train run's handoff folder.
When `--label` is present, the video is instead copied to
`videos/<label>.mp4` without replacing the legacy `play_video.mp4`. The suite
wrapper invokes the existing video wrapper for `--from-run`, or the existing
portable `play` command for `--checkpoint`, sequentially for `stairs`,
`inverted_stairs`, `boxes`, `random_rough`, and two profile-specific slopes,
using only play-time terrain overrides, and stops on the first failure.
It accepts exactly one source: `--from-run RUN_ID` keeps the existing preserved-train
video path, while `--checkpoint PATH` invokes the existing `play --checkpoint`
isolated-copy path for each terrain. Checkpoint mode derives one deterministic handoff ID from the
robot, checkpoint filename, and source SHA-256 prefix; each labeled play is recorded as
video evidence and updates that handoff folder. Neither source mode alters the checkpoint.
At suite start, the wrapper pins the checkpoint filename and SHA-256. Completion
requires all six PASS video evidence records to reference that same digest and each
handoff MP4 to match its evidence copy. It then writes
`video_suite_manifest.json` (robot, checkpoint identity, generation time, terrain,
MP4 digest, and video evidence ID) and an exact `SHA256SUMS` covering the six MP4
files plus the manifest. Finally it rebuilds `<RUN_ID>-download.tar.gz`, writes the
archive `.sha256`, and verifies both the loose files and archived copies.
The suite command automatically calls the PERSONAL-only suite publisher after all six
videos and the archive pass verification. The default tag and title are
`private-<RUN_ID>-videos`; an existing Release or tag is never overwritten. Use
`--no-publish` for a local-only run, or explicit `--publish`, `--tag`, `--title`,
and `--notes-file` to set custom Release details. The publisher uploads six
MP4 files, `video_suite_manifest.json`, `SHA256SUMS`, the suite archive, and its
`.sha256` sidecar, then verifies each remote asset's size and digest. It creates
and pushes an annotated tag from the personal NVIDIA checkout before publishing;
an existing tag is only reused when its local and remote annotated objects match.
A normal personal train or video Release follows the same tag rule and requires
the tag to point at the current personal checkout commit. If publishing fails
after the tag push, the matching tag remains available for a retry.
A failed publish returns a nonzero exit status while leaving the local suite available
for inspection and a separate publish retry.
Go2 writes `slope_up_20deg`/`slope_down_20deg` with magnitude `0.363970234`;
H1 writes `slope_up_10deg`/`slope_down_10deg` with magnitude `0.176326981`.
Both use `horizontal_scale=0.05`. The broader
`[0.2,0.4]` range remains a separate randomized slope smoke test and is not
part of this fixed-angle suite.

The six-terrain suite and its Release publisher are PERSONAL-only. The suite
wrapper suppresses the normal per-video publisher and publishes only once after
all six videos are verified, unless `--no-publish` is set. The separate publisher
re-verifies the manifest, common checkpoint SHA, `SHA256SUMS`, archive, and archive
sidecar before uploading exactly six MP4 files, the suite manifest, `SHA256SUMS`,
the suite archive, and its sidecar. It never deletes or overwrites a Release and
fails if a Release already exists for the requested tag. An existing matching
annotated tag may be reused. Official mode remains blocked. A normal
official `video` still uses the native recording switches without terrain overrides.

The defaults are `/home/shadeform/ISSACSIMZ_DOWNLOAD/<RUN_ID>/` in personal
mode and `/workspace/ISSACSIMZ_DOWNLOAD/<RUN_ID>/` in official mode. Set
`ISSACSIMZ_DOWNLOAD_ROOT` to override the root. `LATEST.txt` contains the most
recent handoff folder name. Console logs, the full checkpoint set, and other
files already preserved inside evidence are not duplicated. This local copy
is independent of publishing; official mode still performs no external
publish operation.

After each train handoff, and again whenever a successful video updates it,
the sidecar also wraps the complete existing `<RUN_ID>/` folder as the sibling
`<RUN_ID>-download.tar.gz` and writes
`<RUN_ID>-download.tar.gz.sha256`. The archive keeps `<RUN_ID>/` as its single
top-level directory, includes any existing nested user-facing files such as
`videos/`, and never removes the unpacked handoff folder.

## Commands

```text
issacsimz doctor [--robot h1|go2] [--log-root PATH]
issacsimz run --name NAME [--run-root PATH] [--collect PATH] -- COMMAND ...
issacsimz train (h1|go2) --iters N --name NAME [--task-root PATH] [--tmux]
issacsimz play (h1|go2) [--from-run TRAIN_RUN_ID] [--checkpoint PATH] --name NAME [--task-root PATH]
issacsimz video (h1|go2) --from-run TRAIN_RUN_ID [--name NAME] [--task-root PATH]
issacsimz watch --run-dir PATH --destination PATH (--all | --keep 100,500)
issacsimz pack RUN_ID [--log-root PATH] [--output-dir PATH] [--force]
issacsimz verify ARCHIVE.tar.gz [--require-sidecar]
issacsimz runs list [--log-root PATH]
issacsimz runs show RUN_ID [--log-root PATH]
```

`train --resume` still uses the existing native `train.py` to load optimizer and
checkpoint state. For an indexed official resume, use three distinct identifiers:
`--from-run` is the source **evidence** run ID, `--load-run` is that evidence's
native run directory name (derived if omitted), and `--checkpoint` is the actual
indexed `model_N.pt` source path. Read its `source_path`, `origin`, SHA-256, and
size from the evidence's manifest-verified `checkpoint_index.json`; do not
guess a path from `metadata.native_run` or copy a checkpoint manually. The
sidecar verifies the original path and bytes, then passes only `model_N.pt` as
the native checkpoint selector. If the native run no longer has that file, the
sidecar restores a verified copy only to that same native run directory,
without overwriting a different file. The original keeper and restored copy
remain in place, and lineage records both paths. `model_best.pt` is not accepted
as an indexed official training-resume source; it remains available for play/export.

For either PERSONAL or OFFICIAL training with one native checkpoint file, H1 and
Go2 support `--import-checkpoint PATH`. Do not combine it with `--from-run`,
`--load-run`, or `--checkpoint`. The sidecar retains the input, hashes it, and
stages an identical copy under the robot's native run root in
`issacsimz-import-<SHA prefix>/`. It selects that directory and the literal
checkpoint basename for the unchanged native resume loader. It never invents
parent evidence. An existing conflicting staged file is rejected, not overwritten.
OFFICIAL imports remain unverified lineage and do not satisfy official evidence
requirements.

After official bootstrap and checking the intended reward configuration:

```bash
ARGS=(h1 --iters 2000 --envs 4096 --seed 42 --name your-run-name
      --import-checkpoint /workspace/model_2700.pt)
./scripts/issacsimz_train.sh "${ARGS[@]}" --preflight-only &&
./scripts/issacsimz_tmux_train.sh "${ARGS[@]}"
```

Use `go2` instead of `h1` for Go2. Values and the checkpoint path are examples,
not an instruction to start a particular run. `--iters` is forwarded unchanged
as native `--max_iterations`. Preflight checks the path and staging conflicts
without copying or starting training. Native checkpoint contents and robot compatibility are
validated by the native loader, not by this file-level preflight. Exported
TorchScript `policy.pt` is not a native training checkpoint.

In the recorded Top01 resume, `model_4950.pt` with `--iters 5050` reached
iteration 9950. The sidecar forwards the requested iteration count unchanged;
confirm the actual final iteration from run evidence rather than deriving it
from the checkpoint filename alone.

Imported parent lineage is explicitly `unknown`/unverified, with its path and
SHA recorded and no fabricated parent Run ID. This enables training, not proof
of official parent origin. OFFICIAL sidecar play/export and indexed resume from
an unverified imported lineage remain refused. Use the original verified parent
evidence/index path when submission provenance is required; do not edit metadata
to turn an import into verified evidence. Existing indexed resume, personal
resume, keeper, evidence/archive and publisher behavior remain unchanged.

Before starting tmux, `scripts/issacsimz_tmux_train.sh` now performs a
`--preflight-only` check with the same arguments. This checks evidence, index,
source checkpoint, native run, and any conflicting native file without starting
training or restoring a file. The portable CLI's `train --tmux` path performs
the same preflight before opening a detached session. For manual diagnosis, run the same arguments via
`scripts/issacsimz_train.sh ... --preflight-only`; if it fails, fix the reported
input rather than retrying tmux, changing CWD, or guessing another path.
Do not pass `--preflight-only` to the tmux wrapper itself.
`official_resume` is true only in official mode.

After each official train, issacsimz performs a one-shot inventory of numbered
checkpoints created or changed in the detected native run and organizer
`backup_log`. `checkpoint_index.json` records source path, origin, byte size,
and SHA-256 and is covered by evidence `SHA256SUMS`. The separate organizer
shell procedure preserves checkpoint bytes before this inventory; the generic
watcher/mirror stays disabled. Later official play/resume accepts a numbered or keeper
checkpoint only when its current bytes match that recorded inventory.

For a sufficiently long resume, do not treat automatic exported `model_best.pt`
as the representative policy. Preserve the final numbered native checkpoint through the
approved server procedure and use it explicitly with
`play --from-run <official-train-run> --checkpoint <final-model.pt>` for one native
play/export. Consider its predecessor only when the final several hundred
iterations jointly and clearly deteriorate in terrain, tracking, and falls. This workflow does
not require a checkpoint tournament or selector program.

In personal mode, `play --checkpoint PATH` accepts an arbitrary checkpoint as
its immutable source. Official mode instead requires `--from-run` to identify a
non-failing `mode=official` train evidence run. Its checkpoint must be that
evidence run's manifest-verified `collected/exported/model_best.pt`, an identical
canonical task export, a numbered checkpoint still in the recorded native run,
or an organizer-keeper `TASK_ROOT/backup_log/<native-run>/model_<iteration>.pt`. A bare or
unrelated checkpoint path is rejected.
OFFICIAL numbered-checkpoint play/export additionally requires source train
`status=completed`; failed, interrupted, or missing status is refused even with
a valid checkpoint index and SHA. Training resume is unaffected by this guard.

For a non-canonical checkpoint, `play` and `video --from-run` copy the selected
source into an isolated evidence staging directory and pass the isolated path through the official
`play.py` native `--checkpoint` option. Fresh policy/video outputs are promoted
to the task export for evidence collection. An identical canonical task export
can be used directly without a staging copy. The canonical
`TASK_ROOT/exported/model_best.pt` is never replaced, moved, or deleted.
Because the unchanged official wrapper checks that canonical path during
startup, it must already exist; issacsimz fails instead of creating it when it
is absent. Evidence records the original source path and SHA-256 separately
from the isolated execution path. `policy_manifest.json` records the source
evidence run ID, source run mode, validation state, checkpoint origin,
checkpoint SHA-256, and fresh policy SHA-256. Official policy promotion is
disabled unless that lineage was verified. The source checkpoint and parent
evidence are never writable. `video` invokes the native command with
`--headless --video --video_length 1000 --enable_cameras` (20 seconds at
50 Hz). Personal mode can forward `--extra`; official mode accepts only the
native `--video`, `--video_length`, and `--enable_cameras` recording switches
and rejects Hydra/viewer/terrain overrides. Official `train --extra` is also
rejected; the named train options remain available. It does not change the
default camera. It locates fresh MP4 output under the isolated play directory
and promotes it to the canonical export location. Success
requires a fresh, non-empty official `exported/play_video.mp4`, independently
of whether `policy.pt` is produced. `video_manifest.json` records the parent
run, source run mode, checkpoint origin, source checkpoint SHA-256 and MP4
SHA-256. Use `--video-length FRAMES`
only when a different duration is intentional.

The final console line reports execution and evidence separately, for example
`execution=FAILED exit=1 evidence_validation=PASS`. This means the native task
failed while its failure evidence was preserved consistently; it never means
that the play itself succeeded.

## Reward overrides

Reward editing is an explicit, separate action: it never runs automatically
before or after training and it never imports the Isaac reward module. Only
the allowlisted H1/Go2 reward keys in the resolved `*_rewards.py` file can be
edited. The first edit saves a byte-for-byte baseline outside the task tree;
use `show` and `diff` before training.

```bash
./issacsimz reward show go2
./issacsimz reward set go2 lin_vel_z_l2 -4.0
./issacsimz reward set go2 flat_orientation_l2 -0.5
./issacsimz reward diff go2
bash scripts/issacsimz_train.sh go2 --iters 1000 --envs 4096 --name go2-g3
./issacsimz reward restore go2
```

`reward set` changes only the finite numeric weight of an already active
allowlisted entry; `off` and activation of commented entries are refused.
`nan`, `inf`, unknown keys, zero or
multiple matching entry lines, and restore after a manual external edit are
all refused without modifying the reward file.

`--run-root` is a directory whose newly created child directory becomes the
native run. Directories present before launch are snapshotted and excluded,
preventing a previous run from being selected merely by mtime. In personal
mode the watcher copies stable `model_*.pt` files only and never alters the
source directory. In official mode the sidecar compares the directory listing
once after completion to preserve native TensorBoard and other non-checkpoint
files without starting a watcher. For a known exact personal run directory,
use `watch --run-dir`; `--keep` exits automatically after all requested
checkpoints are preserved.

## Validation performed without a GPU

The standard-library fixture suite simulates successful completion, official
backup states, missing/stale artifacts, source mutation, cleanup races,
graceful and forced Ctrl+C, profile locks, insufficient disk and archive
overwrite protection:

```bash
bash scripts/build_portable.sh
```

The build script runs the suite before producing the zipapp. Real Isaac Lab,
L40S and official-server smoke tests remain separate integration checks.

## License

No license has been selected yet. Do not assume reuse permission until a
license is added.
