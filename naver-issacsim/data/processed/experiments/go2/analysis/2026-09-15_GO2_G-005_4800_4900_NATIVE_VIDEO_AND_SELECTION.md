# [분석] Go2 G-005 4800/4900: fixed evaluation, native video, and current selection

> 관리 안내 (2026-10-13): **분석** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](../../../../../research/EXPERIMENTS.md)를 확인한다.

> Historical selection record from 2026-09-15. “Current decision” below refers to that date's private comparison, not the present submission status. A separate original-4800 matching snapshot was later submitted and scored 87.55/100; see the [experiment registry](../../../../../research/EXPERIMENTS.md), G-005 Run 07. The private evaluation itself is not an official score.

## Scope and decision

This record integrates the preserved report `A1_4800_vs_4900_DEEP_ANALYSIS_AND_LEARNING_RECORD_20260915.md`, the fixed-condition private evaluation, and the six native play videos. It does not replace canonical evidence and it is not an official score.

**Current decision:** original fresh `model_4800.pt` (SHA-256 `ea93f9b5b04d91a91d1cdb97c6d328978017991e0602745f9269c7190bfaba65`) is the primary submission candidate. Recovery `model_4900.pt` (SHA-256 `250e430cbb74f837af15384c145e865f7c8d8155fc65a7fe8b21dda1c27514cd`) remains the higher-progress, higher-risk alternative; fresh `model_4300.pt` remains the reference control.

This is a candidate-selection decision, not a declaration that 4800 is submit-ready or an official performance claim. Before an actual submission, retain a fresh 4800 export with its matching policy/configuration and provenance, and repeat the controlled comparison across additional seeds where time permits.

## Controlled quantitative evidence

The private L40S evaluator ran deterministic inference for three checkpoints across six terrains and 64 environments per cell: 18 CSVs and 1,152 episodes in total. It fixed seed `4201`, difficulty `1.0`, command `(vx, vy, yaw_rate) = (1.0, 0.0, 0.0)`, horizon 20 seconds, and disabled curriculum/randomization effects. This is stronger selection evidence than training-console point values or visual impressions, but it remains one seed on a private evaluator.

| Checkpoint | Falls / 384 | Fall rate | Timeout survival | Mean XY RMSE | Mean yaw RMSE | Mean +X | Interpretation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 4300 | 13 | 3.39% | 96.61% | 0.456 | 0.135 | 11.58 m | reference control |
| **4800** | **7** | **1.82%** | **98.18%** | 0.443 | **0.102** | 12.11 m | stability-first primary candidate |
| 4900 | 23 | 5.99% | 94.01% | **0.410** | 0.110 | **12.56 m** | progress-first, higher-risk alternative |

On matched 4800/4900 environment keys, 4800 alone fell in 7 cases, 4900 alone fell in 23, neither fell in 354, and neither had a joint fall. Those parallel environments are useful paired observations, not independent multi-seed repeats.

Boxes and stairs are the principal risk discriminators: 4800 had 3/64 and 4/64 falls, versus 4900's 11/64 and 9/64. Inverted stairs demonstrates why timeout is not traversal: 4800 timed out without base contact in all 64 episodes but advanced only 1.16 m on average; 4900 advanced 2.28 m and still did not demonstrate satisfactory traversal.

## Native video evidence

The comparison bundle contains six successful native-play evidence runs: 4800 and 4900 on stairs, boxes, and inverted stairs. Each validation file is `PASS`, each evidence SHA list matches its recorded MP4, and the consolidated video SHA list has six matching files. The videos are H.264, 1920x1080, 50 fps, 999 frames, and about 19.98 seconds each.

Their purpose is qualitative sanity checking, not a remeasurement of the controlled benchmark. They used the same staged checkpoint identities, seed `4201`, native `play.py` path, selected terrain proportions, camera, and recording duration, but did not force the benchmark's difficulty, curriculum state, command, or traversal alignment. The logs show native curriculum and command managers active. Therefore:

- stairs and boxes support the observed distinction of more conservative 4800 behavior versus more aggressive 4900 behavior, but do not establish full-terrain completion;
- inverted-stairs videos are diagnostic only: survival or motion near an edge is not directed descent/traversal;
- video cannot overturn the fixed-condition stability result, and should not be cited as an official evaluation.

The exported `policy.pt` files may differ in PyTorch serialization metadata between video runs. Policy identity is anchored to each evidence run's source checkpoint SHA and validation lineage, not the outer serialization bytes alone.

## Integrity and provenance checks

- Received report SHA-256: `81b79688f820b4f4957db79f19fcd368d2d63648a2684fe1b31d578aaa85c1a8`; preserved byte-for-byte under `data/processed/incoming/other/reviewed/`.
- Fixed-evaluation archive SHA-256: `72c00b43345e9438647e30a6e01905391c3aea085b90042c75fdbbb5ad2695bd`; `EXPORT_SHA256SUMS.txt` verification found zero mismatches.
- Raw evaluation: 18 data CSVs, 1,152 finite rows, complete required schema, and 1,152 unique `(model_iter, terrain, difficulty, seed, env_id)` keys.
- Native-video bundle SHA-256: `424467b9c5b61666957ff22cc3395803f45d5c48bfc7797e3c85749a29902a7d`; six validation files and six final-video checksums had zero mismatches.

The immutable private evaluation and video bundles remain under `naver-issacsim-originals/data/raw/private_server_runs/go2/`; this analysis repository stores interpretation and the byte-preserved incoming report only.

## Next evaluation rule

For a future traversal video, explicitly fix command, curriculum off, difficulty, start heading/alignment, and terrain completion criteria. Report world-frame forward progress, heading error, lateral drift, completion rate, and recovery after contact separately from body-frame tracking and timeout survival.

## Links

- [Preserved integrated report](../../../incoming/other/reviewed/A1_4800_vs_4900_DEEP_ANALYSIS_AND_LEARNING_RECORD_20260915.md)
- [Fixed evaluation detail](../2026-09-15_GO2_G-005_FIXED_EVAL_SEED4201_D1.md)
- [Prior checkpoint decision record](../2026-09-15_GO2_G-005_CHECKPOINT_4300_4800_4900_DECISION.md)
