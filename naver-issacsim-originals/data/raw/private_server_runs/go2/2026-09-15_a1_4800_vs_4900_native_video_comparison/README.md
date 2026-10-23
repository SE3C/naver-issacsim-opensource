# Go2 A1 original 4800 vs recovery 4900 native video comparison

This directory preserves the received bundle byte-for-byte. It is classified
as a **private L40S visual sanity check** of official-run checkpoints, not an
official-server evaluation and not an official competition score.

Actual frame-level behavior has not yet been adjudicated here. Preserve the
bundle first; merge the later analysis report into the analysis repository
without rewriting this raw source.

## Received files

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `A1_4800_vs_4900_FINAL_BUNDLE_20260915.tar.gz` | 158,959,751 | `424467b9c5b61666957ff22cc3395803f45d5c48bfc7797e3c85749a29902a7d` |
| `A1_4800_vs_4900_FINAL_BUNDLE_20260915.tar.gz.sha256` | 111 | `6569432511e5e85d47d888362d2fe4445cd1b428f602a9ef925c29f1a1e89d96` |

The sidecar matches the received archive.

Convenience mirror: [`private-go2-20260915-a1-4800-vs-4900-native-video`](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-go2-20260915-a1-4800-vs-4900-native-video). The Release is classified as PERSONAL auxiliary validation; this directory remains the canonical raw evidence.

## Content and verified lineage

- Models: original fresh 4800 SHA-256 `ea93f9b5…aba65`; recovery 4900
  SHA-256 `250e430c…14cd`.
- Terrains per model: `stairs`, `boxes`, `inverted_stairs`.
- Six separate `issacsimz play` evidence directories, six native logs, a
  six-row manifest, final-video checksums, the two checkpoint inputs, and the
  orchestration script are included.
- Every run records the expected source-checkpoint SHA, exit code `0`, evidence
  validation `PASS`, and unchanged task-source identity.
- Every terrain command sets only its selected terrain proportion to `1.0` and
  the other five supported terrain proportions to `0.0`.
- Final videos exactly match their corresponding evidence-run
  `collected/exported/play_video.mp4` files.

## Media verification

All six files are H.264, 1920×1080, 50 fps, 999 frames, and 19.98 seconds.
Their SHA-256 values are recorded in `final_videos/MANIFEST.tsv` and
`final_videos/SHA256SUMS`; both agree with the files.

All seven included `SHA256SUMS` files were checked successfully. The six
native logs contain `COMPLETED exit=0 validation=PASS` and no traceback,
runtime-error, OOM, or segmentation-fault marker.

## Interpretation boundary

The pair is fair for same-terrain visual comparison in the following limited
sense: the model pair uses the same native `play.py`, seed 4201, one
environment, camera/video settings, terrain-proportion isolation, and duration.

It is **not** a replay of the quantitative difficulty-1.0 benchmark. The native
curriculum manager and native command manager remain active; the command does
not force difficulty 1.0 or `vx=1.0, vy=0, yaw=0`. Therefore these videos are a
behavioral sanity check, not a new measurement of the 1,152-episode table.
Reward weights printed by native play are irrelevant to inference actions, but
must not be presented as a new A1 training or reward evaluation.

For frame review, prioritize body roll/pitch, foot snagging or dragging,
recovery after obstacle contact, actual forward progress, lateral/yaw drift,
and pre-fall oscillation. Boxes and stairs are the primary 4800-vs-4900
discriminators; inverted stairs is a shared stall/traversal diagnostic. Do not
equate staying upright with traversal success.

## TorchScript serialization note

The three 4800 `policy.pt` exports are byte-identical. The 4900 boxes export has
a different whole-file SHA from the stairs/inverted-stairs exports, while all
three 4900 ONNX files are byte-identical and the TorchScript tensor data records
are identical. The differing archive members are serialization ID and generated
code-mangling records. Treat checkpoint SHA plus evidence-run linkage as the
policy identity; do not infer a different trained 4900 policy from the container
SHA difference alone.
