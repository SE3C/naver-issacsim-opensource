# Lifecycle fixture coverage

The fixture suite exercises file, process, native-finalize and official-backup
lifecycle behavior without Isaac Sim or a GPU.

Run it from the repository root in Linux or WSL:

```bash
source scripts/python_runner.sh
PYTHON_RUNNER="$(issacsimz_find_python_runner "${ISSACLAB_ROOT:-/workspace/IsaacLab}")"
"$PYTHON_RUNNER" -m unittest discover -s tests -v
```

`test_core.py` covers parsers, profile path resolution, doctor exit status,
environment-variable presence semantics, run discovery, checkpoint hash reuse,
archive traversal and disk-space guards.

`test_lifecycle.py` launches `fixtures/fake_train.py` and covers:

- success and each supported official-backup outcome;
- official mode without periodic GPU telemetry, checkpoint mirror, or watcher log;
- personal mode retaining periodic GPU telemetry and checkpoint mirroring;
- official rejection of the independent `watch` command;
- run-specific keep-all checkpoint preservation; the separately supplied
  historical keeper and its archival byte-identity test are not distributed;
- train/play/video fail-closed behavior when `ISSACSIMZ_MODE` is absent or invalid;
- personal-only enforcement for generic `run` and `watch`;
- official resume and numbered/keeper checkpoint SHA inventory provenance;
- official-mode rejection of generic `run`, train Hydra extras, private submit
  bypass flags, and non-canonical task/IsaacLab roots;
- official play/video allowlisting of native recording switches and rejection
  of arbitrary Hydra extras;
- official video-suite rejection while the personal six-terrain suite remains
  covered;
- stale exports, missing artifacts and source mutation;
- the final checkpoint scan immediately after `[POST]` and before cleanup;
- first Ctrl+C waiting for native finalize, personal second Ctrl+C force-stop,
  and official repeated-Ctrl+C suppression
  recording;
- live/stale per-profile locks;
- credential exclusion and archive verification;
- overwrite refusal unless `--force` is explicit.

The suite does not claim Isaac Lab or official-server compatibility. Those are
deliberately deferred integration smoke tests performed with the exact built
`dist/issacsimz.pyz` artifact.
