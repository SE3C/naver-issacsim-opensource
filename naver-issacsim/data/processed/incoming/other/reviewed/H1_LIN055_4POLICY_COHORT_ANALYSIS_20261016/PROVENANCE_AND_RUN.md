# Provenance and reproduction

- Input: `H1_LIN055_4POLICY_COHORT_INPUT_20261015.zip`
- Input ZIP SHA-256: `eff60bee8fd66a5703110f3240626945a499476a9493f0256561d9deef6a9f21`
- ZIP archive member CRC tested with Python ZipFile.testzip() == None.
- `SHA256SUMS.txt`: 48 of 48 listed member checksums validated; `SHA256SUMS.txt` itself is not listed.
- Original inputs were opened read-only via ZipFile; no extraction, modification or posting.
- Evaluation raw checkpoint identifiers are assertions across `INPUT_MANIFEST.json`, evaluation manifest, evaluation link, and external publication metadata. **No `.pt` bytes included**, so checkpoint SHA is not a newly computed checksum.
- Raw evaluation `source_run_id=null`, `preset=null`, and publication imported-parent provenance remain unmodified and distinct from publication metadata mapping.
- Evaluator protocol parity is checked using full dict equality, full resolved config equality, source and applied environment fingerprints, not merely the protocol ID.
- Case keys required: scenario/case/seed/env_id; strict one `-n0` episode per case/seed/env and no restarts, all 20 seconds timeout. Missing, duplicate, reset or early-ended data fails the script rather than being silently omitted.
- Policy comparison order fixed before computing outputs: C−B, C−D, B−A, C−A, D−A. Every scenario/case included; no outcome-driven filtering.
- The sign of world XY net displacement is descriptive-only outside H1; H3 does NOT require world-origin return. Signed forward progress is descriptive-only for H1/H3 (zero forward command); absolute forward leakage is the meaningful comparison there. For descriptive-only metrics, improved/worsened/ties columns are deliberately blank, although delta values are preserved.
- P05 uses linear interpolation on sorted raw values at 0.05×(n−1); outliers are never trimmed. Sign counts use zero tolerance 1e-12 only.
- CSV files use UTF-8 BOM for Excel compatibility; decimal numbers remain full numeric precision.
- Runtime creating this package: Python `3.13.5`, system `Linux`. The analysis itself is Python standard-library only.

## Re-run (CPU only)

Place `analyze_cohorts.py` next to the input archive or point `--input` to the original ZIP. From a directory in which write access is available:

```bash
python analyze_cohorts.py \
  --input /path/to/H1_LIN055_4POLICY_COHORT_INPUT_20261015.zip \
  --out /path/to/recreated_results
```

No Isaac Sim, Torch, GPU, evaluator or video is invoked; reading source data and generating CSV/MD is the only action. Output directory is newly created or overwritten for same-name generated artifacts; source ZIP is never written. `INPUT_MANIFEST` was read first. Do not change provenance fields inside source JSON.

## Known limitations

This archive contains episode summaries and manifests, not evaluator implementation code, per-step trajectories, video, training resolved reward/PPO archives, actual terrain realization snapshots, or `.pt` checkpoint bytes. The publication linkage and training values come from supplied manifest metadata. Same evaluator fingerprint and cohort index do not certify matched physical trajectory. Three evaluator seeds are not independent training runs; no inferential confidence interval or significance test should be inferred from per-env paired fractions. No new official score is computed.
