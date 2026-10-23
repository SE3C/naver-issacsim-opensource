# Go2 G5 / G-004 official 1K raw evidence

## Receipt and provenance

| Field | Value |
| --- | --- |
| run ID | `20260914-012909-go2-g5-angvelxy-m012-1k-official` |
| source | user-provided official-server result directory from Downloads |
| received container name | `20260914-012909-go2-g5-angvelxy-m012-1k-official.tar` (directory despite the suffix) |
| canonical action | copied all five received files byte-for-byte; no rename, repack, move, or deletion |
| train archive bytes | 83,248,303 |
| train archive SHA-256 | `1e162fdf640a715f19c564e21bff1011cd7ed91287db2f8d3586c3e0382d4359` |

## Received files

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `20260914-012909-go2-g5-angvelxy-m012-1k-official.tar.gz` | 83,248,303 | `1e162fdf640a715f19c564e21bff1011cd7ed91287db2f8d3586c3e0382d4359` |
| `env.yaml` | 28,503 | `f7d17203e3d2755cf078dc86dd90860fb60afac426ec743203c38727bd44bec2` |
| `model_best.pt` | 6,882,219 | `85cc1aad6bd20af17d7277d97ee5d05f74b7deca2ac463b7feb7602bb06c72bd` |
| `play_video.mp4` | 3,581,817 | `35d7b9ebe128d23447d2b3e0b1737cf5d37a555a4995f4a36618b8c4e9eafe4b` |
| `report.html` | 12,843 | `17b24c51593cf042f81bed4b847e2685aee3509364105aef79ab802f35c2fab8` |

The loose `env.yaml`, `model_best.pt`, and `report.html` are byte-identical to
the corresponding `collected/exported/` files inside the train archive. They
are retained because they were part of the received download result, not
generated again by this repository.

## Verification

- The gzip/tar archive opened successfully and has the sole top-level directory
  `20260914-012909-go2-g5-angvelxy-m012-1k-official/`.
- All 33 entries in the archive's internal `SHA256SUMS` matched.
- `validation.json` reports `overall: PASS` for native run, TensorBoard,
  checkpoints, source identity, official backup, collection, exported files,
  and official finalize.
- `metadata.json` reports a completed 1K official Go2 train run, 11 mirrored
  checkpoints, official backup success, no source mutation, and
  `evidence_validation: PASS`.
- No token, credential, secret, `.env`, or submission configuration file is
  present in the archive member list. Metadata records only boolean presence
  flags for the official backup environment, not secret values.
- The received MP4 probes as H.264, 1920×1080, 50 fps, 19.98 seconds, and is
  nonempty. It is a loose received artifact; no separate video evidence archive
  was supplied.

This is official-server raw evidence, not an official evaluator score. The 1K
result is a light screening result and its interpretation belongs in
`naver-issacsim` under experiment `G-004`.
