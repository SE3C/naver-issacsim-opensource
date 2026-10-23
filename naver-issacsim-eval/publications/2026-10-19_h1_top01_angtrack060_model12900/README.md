# H1 TOP01 ANG070 +3K model12900 — PERSONAL evaluation receipt

[Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261019-exp-h1-joint-tracking-balance-ang070-model12900-local-eval) · [Remote asset verification](remote_verification.json)

This is a PERSONAL Windows post-training evaluation archive. It is not evidence that the training Run was OFFICIAL, and it is not an official score.

The supplied archive is preserved byte-for-byte under its original name, `h1-top01-angtrack060-plus3k_model_12900_LOCAL_evaluation_20261019.zip` (187,666 bytes; SHA-256 `abf37b45d32c28c26de232214313641d7e3fcd289e422df16ba8cae72b030eb2`). The original experiment detail identifies the actual reward setting as `ang=0.70`; the preserved input filename and folder retain their original `angtrack060` label. The source path and evaluator-recorded checkpoint identity are in `intake_manifest.json`.

The ZIP contains six files: `diagnostics.json`, `episodes.jsonl`, `evaluation_manifest.json`, `README.txt`, `resolved_configs.json`, and `video_evaluation_link.json`. The manifest identifies H1 `scenario7`, camera off, 128 environments, seed 4201, and 20 seconds per case. It records `complete=true`, `execution_status=COMPLETE`, and `smoke=false`; the episode file has 1,024 rows across the eight cases for the recorded seed.

The evaluated checkpoint SHA recorded in the manifest is `3f78944c81ff09cba97586deaaf2c6874b4e39bff1fde945628af6d314451b7a`. The evaluation metadata records Windows PERSONAL execution on an NVIDIA GeForce RTX 3060 Laptop GPU and evaluator implementation commit `9c774a322f2f7d4944444de57f01308987bcb3da`. Raw `source_run_id` is null. Training lineage remains a separate verification; this receipt does not assert OFFICIAL training provenance. Cohort validation found eight seed×case groups with 128 distinct environment IDs (0–127) each, no duplicate or missing cohorts. Fatal and secret-pattern scans of `evaluation.log` found no matches.

An independent intake comparison matches that SHA to keeper `model_12900.pt` in the [OFFICIAL +3K training archive](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261018-exp-h1-joint-tracking-balance-ang070-plus3k). This external link does not rewrite raw `source_run_id=null`. The recorded filename retains `angtrack060`, while archived angular reward is 0.70. The historical best11650 and current submitted40500 are different policies.

The ZIP contains no videos, policy comparison, or official score. This receipt records metadata and dataset completeness only.
