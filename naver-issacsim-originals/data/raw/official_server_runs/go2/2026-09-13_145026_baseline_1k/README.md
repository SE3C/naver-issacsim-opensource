# Go2 official baseline 1K raw evidence

## Canonical received bundle

| Field | Value |
| --- | --- |
| received name | `go2-b0-1k-official-complete-bundle.tar.gz` |
| canonical repository name | `GO2_baseline_1k_complete_20260913.tar.gz` |
| bytes | 94,875,860 |
| SHA-256 | `db659cdad4bf4a61de6c40c6185f80bb2465054e67abda91da4cfa8d0408a5bf` |
| source | user-provided official-server baseline 1K bundle, received from Downloads |

Only the repository filename changed.  The canonical archive is otherwise a
byte-for-byte copy of the received bundle: it was not repacked, extracted,
flattened, or edited after verification.

## Bundle format and verification

This is a valid `issacsimz` complete bundle, not a workspace backup.  Its sole
top-level directory is `go2-b0-1k-download/`, containing the following direct
evidence artifacts:

| Internal artifact | Bytes | SHA-256 / supplied sidecar target |
| --- | ---: | --- |
| `20260913-145026-go2-b0-1k-official.tar.gz` | 83,269,165 | `7dff91b8ad8fe041493876e58f17f21ed1bc22eda53a21aaad076f223098dc68` |
| `20260913-145026-go2-b0-1k-official.tar.gz.sha256` | 108 | train archive hash above |
| `20260913-145026-go2-b0-1k-official.tar.gz.metadata.json` | 238 | train packing metadata |
| `20260913-155641-20260913-145026-go2-b0-1k-official-video.tar.gz` | 11,640,471 | `a1d79a67ca0ec36612410a49d9fc5ae9e04a76ba4ce4dd376c862ec5e0bbf7db` |
| `20260913-155641-20260913-145026-go2-b0-1k-official-video.tar.gz.sha256` | 130 | video archive hash above |
| `20260913-155641-20260913-145026-go2-b0-1k-official-video.tar.gz.metadata.json` | 259 | video packing metadata |

Receipt verification extracted the bundle only to a temporary inspection
location.  Both direct archives matched their supplied sidecars, and their
combined internal `SHA256SUMS` contained 53 entries with zero mismatches.
Train metadata records completed native/finalize status, expected official
backup success, 11 mirrored checkpoints, and `evidence_validation: PASS`.
The video manifest points to parent train run
`20260913-145026-go2-b0-1k-official` and source checkpoint SHA-256
`99ceeaa1a3a1ebee972841a771072b711744a1c8dec6e94b318b55f146dc4676`.

This archive is raw training/provenance evidence, not an official evaluator
score or a policy-adoption decision.  Any analysis belongs in
`naver-issacsim/data/processed/experiments/`.
