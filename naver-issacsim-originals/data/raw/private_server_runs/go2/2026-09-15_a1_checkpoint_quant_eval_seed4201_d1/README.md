# Go2 A1 checkpoint quantitative evaluation — seed 4201, difficulty 1.0

This directory preserves the received comparison bundle byte-for-byte. It is
classified as a **private L40S auxiliary evaluation**, not an official-server
training run and not an official competition score.

## Received files

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `A1_QUANT_EVAL_SEED4201_D1.tar.gz` | 19,196,227 | `72c00b43345e9438647e30a6e01905391c3aea085b90042c75fdbbb5ad2695bd` |
| `A1_QUANT_EVAL_SEED4201_D1.tar.gz.sha256` | 115 | `10652b85396e9a625b43e6267001fe6e4949c3c7c93aba8e2c7b0940c06ecbae` |

The archive sidecar matches the received archive. Its recorded source path is
`/home/shadeform/A1_QUANT_EVAL_SEED4201_D1.tar.gz`.

Convenience mirror: [`private-go2-20260915-a1-checkpoint-quant-eval-seed4201-d1`](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-go2-20260915-a1-checkpoint-quant-eval-seed4201-d1). The Release is classified as PERSONAL auxiliary evaluation; this directory remains the canonical raw evidence.

## Provenance and scope

- Checkpoints: fresh 4300, original fresh 4800, recovery 4900. All three
  checkpoint hashes match the canonical official-run artifacts.
- Evaluation host: NVIDIA L40S, Isaac Sim `5.1.0-rc.19`, Isaac Lab commit
  `3e73d6dd79080fd7632488c061052a6edd52e230`, task repository commit
  `92835ec73b980900581e29e241c46691882f779a`.
- Matrix: three checkpoints × six fixed terrains, seed `4201`, difficulty
  `1.0`, 64 environments, fixed command `(1.0, 0.0, 0.0)`, 20-second first
  episodes.
- The evaluator is inference-only custom analysis code included in the bundle.
  It does not update the policies.

## Integrity verification

- outer archive SHA-256 sidecar: PASS;
- `EXPORT_SHA256SUMS.txt`: 45/45 referenced files match;
- raw output: 18 CSV and 18 JSON summaries, 64 rows per CSV;
- 1,152 composite evaluation keys are unique; required values, schema,
  categorical domains, and termination flags pass validation;
- all numeric fields inspected are finite;
- raw CSV to JSON aggregation: 18/18 exact within `1e-9`;
- batch completion marker exists and no traceback, runtime error, OOM, or
  segmentation-fault marker was found.

`success_timeout_pct` means that an environment reached the time limit without
the configured `base_contact` termination. It is a survival proxy, not proof
that the robot traversed the terrain or followed the command. In particular,
the inverted-stairs displacement and tracking values must be inspected instead
of treating timeout as task success.

Interpretation is maintained in
`naver-issacsim/data/processed/experiments/go2/2026-09-15_GO2_A1_FIXED_EVAL_SEED4201_D1.md`.
