# H1 model40300 — PERSONAL two-seed evaluation receipt

[Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261019-model40300-2seed-personal-eval) · [Remote asset verification](remote_verification.json)

This is a PERSONAL Windows post-training evaluation archive. It is not evidence that the training Run was OFFICIAL, and it is not an official score.

The supplied archive is preserved byte-for-byte as `model_40300_h1_LOCAL_evaluation_2seed_20261019.zip` (377,570 bytes; SHA-256 `046359f52f88035b79866b17469c49ad8bd62c3af2135b3ebe72ec1a5f535ceb`). Its source path and the original checkpoint SHA recorded by the evaluator are in `intake_manifest.json`.

The ZIP contains eight files: `diagnostics.json`, `episodes.jsonl`, `evaluation.log`, `evaluation_manifest.json`, `launcher_result.json`, `README.txt`, `resolved_configs.json`, and `video_evaluation_link.json`. The manifest identifies H1 `scenario7`, camera off, 128 environments, seeds 4201 and 4202, and 20 seconds per case. It records `complete=true`, `execution_status=COMPLETE`, and `smoke=false`; the episode file has 2,048 rows across the eight cases per seed.

The evaluated checkpoint SHA recorded in the manifest is `fadaf83e56a972de050e357909eca4d62cca6229f11717d35b2e2cd41cbaa20b`. The evaluation metadata records Windows PERSONAL execution on an NVIDIA GeForce RTX 3060 Laptop GPU, Isaac Sim `5.1.0-rc.19+release.26219.9c81211b.gl`, and evaluator implementation commit `9c774a322f2f7d4944444de57f01308987bcb3da`. Raw `source_run_id` is null.

The archive also records `launcher_result.success=false`: the final source-integrity check could not find the original `C:/Users/[USER]\Downloads\model_40300.pt` after evaluation. A relocated checkpoint copy currently at `C:/Users/[USER]\Downloads\NCRC_프로젝트_보관_20261019\체크포인트\model_40300.pt` was independently hashed; its SHA-256 matches the evaluator-recorded checkpoint SHA above. This confirms the identity of that current copy while preserving the original post-run launcher result unchanged. Raw `source_run_id` remains null, and this does not independently validate training provenance. Cohort validation found 16 seed×case groups with 128 distinct environment IDs (0–127) each, no duplicate or missing cohorts. Fatal and secret-pattern scans of `evaluation.log` found no matches. The ZIP contains no videos or policy comparison.
