# H1 H-005 fresh 10K — official server, 2026-09-27

This directory preserves the received official-server run without changing the downloaded files. The canonical download wrapper contains the direct train evidence archive, its SHA-256 and archive metadata, plus the finalized `model_best.pt`, `env.yaml`, and `report.html`. Do not treat the wrapper and its nested train archive as two independent runs.

- Evidence run ID: `20260927-123428-h005-fresh10k-official`
- Native run: `/workspace/training/humanoid/logs/rsl_rl/humanoid/2026-09-27_21-34-34`
- Mode/operation: `official` / `train`; fresh start, no parent checkpoint
- Command: official `train.py`, 10,000 iterations, 4,096 environments, seed 42, headless, `agent.save_interval=50`
- Evidence: execution completed, exit 0, validation PASS, official finalize completed, official backup succeeded
- Reward configuration: H-005 `termination_penalty=-50`, `track_lin_vel_xy_exp=0.5`, `feet_air_time=0.25`
- Automatic best: reward step 9784, saved as `model_9800.pt`; `model_best.pt` has the same SHA-256 as `model_9800.pt`
- Latest preserved numbered checkpoint: `model_9950.pt`, distinct from automatic best; both are inside the evidence archive. This run has not been assigned an official evaluator score.

## Received files

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `evidence_archives/20260927-123428-h005-fresh10k-official-download.tar.gz` | 1,351,378,181 | `3ff1dc0a820df63870c445260c2acf7d66781ab282325f3889d4d1ba669c0566` |
| `evidence_archives/20260927-123428-h005-fresh10k-official-download.tar.gz.sha256` | 121 | `c934d26192273b7e9705538f273f22bb892f62a8efabab292bed7fbf3c814021` |
| `checkpoints/model_best.pt` | 7,151,477 | `20d04452c908056c1bacdbf569080e5eb458c26239e9b438aca637453f5f6a2f` |
| `submission/policy.pt` | 1,206,166 | `833b525921fc40ade0574d99fad656f0f386e30f61101b8caec83e77f2637db6` |
| `submission/env.yaml` | 33,531 | `d65d550f4bd062f62018e5e981052169e80a67581d4331f9059487471c126782` |
| `other_exports/policy.onnx` | 1,194,183 | `0738b7becf771000e49938db6454af66a1cc93e8825e501f2c7e77bb573af6d9` |
| `other_exports/report.html` | 14,447 | `2dc42f064fe2ea414bdae8145dfad553457a08ef2160aa90845b92f4cc993f8a` |
| `videos/stairs.mp4` | 5,583,361 | `c5c6eb6ac048891ff4ddb402d708bc46659c7e8ba998270b1b38f939fa3b3b5e` |
| `videos/inverted_stairs.mp4` | 6,199,251 | `bbcb75508bf6c1d10faad5d04c3420e4455c73d077ea1c7d21aa7620a471b06e` |
| `videos/boxes.mp4` | 6,538,702 | `0de5292229fa45b4ed79f0e50d9d03529e96cfc23d0bcf4dc57336d27fa10a3f` |
| `videos/random_rough.mp4` | 10,108,136 | `b207b626677d2fe762fdd0965dee4c764d8e0b014417f7fc36c874c1a9c8a5e5` |
| `videos/slope_up_10deg.mp4` | 5,994,855 | `56851c68675fdf298b95bd317938b4d83b0a5f96390d1a2bceb84c65df6581dd` |
| `videos/slope_down_10deg.mp4` | 5,610,142 | `b3e5138e156205151d3e17547df52da216568342c52af12ab17f791a69866674` |

The nested direct archive is `20260927-123428-h005-fresh10k-official.tar.gz` (1,345,055,518 bytes; SHA-256 `3864440a819aade9c178d426bdc6545a52dc44ba419e68fbb0213185c71d223c`). Its metadata, `SHA256SUMS`, console, TensorBoard event, checkpoint index, and organizer-preserved numbered checkpoints are retained inside the wrapper. Both the direct archive and wrapper passed local SHA-256 and tar listing checks before intake.

The six loose MP4 files and `policy.pt` were received after the train archive was created. Their exact source-checkpoint linkage is **not independently proven by this train evidence**; in particular, do not label `policy.pt` as exported from `model_9950.pt`. At initial intake, these loose files had not been identified as a submission snapshot. The user later identified the same `submission/policy.pt` and `submission/env.yaml`, together with the received technical report, as the preliminary Round-4 submission files; the separate [submission snapshot Release](https://github.com/SE3C/naver-issacsim/releases/tag/submission-h1-prelim-r4-20260928) preserves them. No portal receipt, exact submission time, evaluator score, or original portal ZIP was supplied. The policy's numbered-checkpoint lineage remains unproven.

The 1.35GB wrapper was uploaded once as this canonical Git LFS object. The raw-run Release links to that object rather than uploading a second copy as a Release asset; smaller received exports and videos may be attached for convenient access.
