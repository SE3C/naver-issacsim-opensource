# Go2 A1 official recovery from original model 4800 to iteration 4999

## Canonical received wrappers

Two snapshots of the same recovery handoff were intentionally received. The
first was downloaded before the video suite finished; the second is the final
handoff. Both wrappers are preserved byte-for-byte with explicit canonical
names so that the Windows duplicate suffix is not mistaken for a different run.

| Stage | Received name | Canonical name | Bytes | SHA-256 |
| --- | --- | --- | ---: | --- |
| pre-video | `20260914-132725-go2-a1-tracklin150-lvz-m2-resume4800-to5k-offici-download.tar.gz` | `20260914-132725-go2-a1-tracklin150-lvz-m2-resume4800-to5k-offici-download-pre-video.tar.gz` | 32,098,775 | `cb6a31a93afecd66492a172861a76af53ced41723d9c4628f48c2cfec2847f14` |
| final | `20260914-132725-go2-a1-tracklin150-lvz-m2-resume4800-to5k-offici-download (1).tar.gz` | `20260914-132725-go2-a1-tracklin150-lvz-m2-resume4800-to5k-offici-download-final.tar.gz` | 79,246,903 | `265c3c5533ac2be5037cab0ea668b07990ccc8025a816b22178b7df7bd7257c5` |

The final wrapper contains every file in the pre-video wrapper byte-for-byte,
plus recovery lineage, original-4800 fallback, exported policy and sidecars,
and six terrain videos. The pre-video wrapper is retained as an intentional
stage snapshot, not treated as a separate experiment.

## Direct recovery evidence

Both wrappers contain the same direct evidence archive:

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `20260914-132725-go2-a1-tracklin150-lvz-m2-resume4800-to5k-offici.tar.gz` | 25,720,360 | `868361827a31eae25d98f99a4e48948f7bf659e29c926bc78c83c4c814811d9c` |

- The direct archive matches its supplied sidecar and all 24 internal
  `SHA256SUMS` entries matched.
- Metadata records a completed official resume from
  `a1-recovery-4800-source/model_4800.pt`, source SHA-256
  `ea93f9b5b04d91a91d1cdb97c6d328978017991e0602745f9269c7190bfaba65`,
  200 requested additional iterations, finalize complete, backup success, and
  `evidence_validation: PASS`.
- The console reaches learning iteration `4999/5000`. Only 100-interval
  checkpoints `model_4800.pt` and `model_4900.pt` were mirrored, so metadata's
  checkpoint-derived `final_iteration: 4900` and the report's `iter 4900 / 총
  5000` must not be read as early training termination.
- Finalization selected `model_4900.pt` around best reward step 4872 and copied
  it as `model_best.pt`.
- Source identity was unchanged during recovery.

## Final handoff content and boundaries

The final wrapper additionally preserves:

- `fallback_model_4800.pt`, SHA-256
  `ea93f9b5b04d91a91d1cdb97c6d328978017991e0602745f9269c7190bfaba65`
- `model_best.pt`, SHA-256
  `250e430cbb74f837af15384c145e865f7c8d8155fc65a7fe8b21dda1c27514cd`
- `policy.pt`, SHA-256
  `22957506fefe1cde249548705fef30147fe149e1086c926ff447ff001c2cc277`
- `env.yaml`, `report.html`, `RECOVERY_LINEAGE.txt`, and six Go2 terrain MP4s

The six MP4s are present and nonempty, but the handoff does not contain their
individual video evidence archives or manifests. Do not claim cryptographic
train-to-video linkage from this wrapper alone.

The separately received `A1_MODEL_4800_SUBMISSION.tar.gz` was not retained. It
mixed the original 4800 checkpoint/config with a policy and smoke video from
the recovery 4900 export, so the user directed that archive and its sidecar be
sent to the Windows Recycle Bin. It must not be used as a 4800 submission.

This recovery completed the requested trajectory through iteration 4999, but
it is not an uninterrupted fresh 5K run: network/optimizer state resumed from
the original model 4800 and environment-side curriculum statistics restarted.

## Later study-file backup from the team's competition account

The received `submission_1789393113.zip` is preserved byte-for-byte as a
**separate study-file backup of this same recovery run**, not as a new run or
the Round-3 submitted policy. The accompanying analysis reports account record
`sub-5916` (`id=5916`) and a 2026-09-14 22:38 KST upload; that authenticated
API response itself is not included in this directory.

| Received ZIP | Bytes | SHA-256 |
| --- | ---: | --- |
| `submission_1789393113.zip` | 6,376,026 | `e10aa9073bf30488a9bebd767cf6780526c6b5831becd3e6507c2a60b3ab5a87` |

The ZIP has exactly `model_best.pt` (6,882,293 bytes, SHA-256
`250e430cbb74f837af15384c145e865f7c8d8155fc65a7fe8b21dda1c27514cd`),
`env.yaml` (28,503 bytes, SHA-256
`5c08b0f45388261d64bdb1206980c7d3511885c66853dfbac416074f94501622`),
and `report.html` (12,756 bytes, SHA-256
`2d3b29c14570b385ea055ba429aafe3f1f215d9116c5655b2215232d830d8bf3`).
The checkpoint SHA matches the recovery `model_4900`/`model_best` already
documented above. The ZIP contains **no `policy.pt`**.

The independently received Round-3 submitted `policy.pt` has SHA-256
`387237907daa02998f720c0f861c4e504445b96ca0f176d81cbab7765b92b254`;
that exact asset is already preserved in the analysis repository's
`submission-go2-prelim-r3-20260915` Release. It belongs to the **original
4800 export**, not this recovery backup. Do not pair this ZIP's recovery
`env.yaml` or `model_best.pt` with that submitted policy as a new submission
bundle. The later weight-similarity analysis is preserved separately in the
analysis repository and does not change these artifact identities.
