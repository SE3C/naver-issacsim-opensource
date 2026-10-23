# Go2 A1 official fresh 5K attempt — interrupted near 4.8K

## Canonical received bundle

| Field | Value |
| --- | --- |
| run ID | `20260914-084321-go2-a1-tracklin150-lvz-m2-5k-official` |
| received/canonical name | `20260914-084321-go2-a1-tracklin150-lvz-m2-5k-official-download.tar.gz` |
| bytes | 315,276,597 |
| outer SHA-256 | `d2919617dbb2121652fb0c38fc12efe8d874280d55adf4416b39c7e5adfe30ef` |
| source | user-provided official-server download wrapper received from Downloads |

The wrapper is preserved byte-for-byte. It was extracted only in a temporary
inspection directory and was not flattened, repacked, or edited.

## Direct evidence and verification

The wrapper contains one interrupted train evidence archive and its sidecar:

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `20260914-084321-go2-a1-tracklin150-lvz-m2-5k-official_INTERRUPTED.tar.gz` | 315,429,662 | `143dc6162ac2666e8902203e80d88ebf219c1a20fb0f85e1f3090a562cc643d5` |

- The direct archive matches its supplied sidecar.
- All 66 internal `SHA256SUMS` entries matched.
- The archive preserves the complete console through approximately iteration
  4837, one TensorBoard event, source/config/system records, and 49 checkpoints
  from `model_0.pt` through `model_4800.pt`.
- Metadata records `status: interrupted`, exit code 1, a
  `BrokenPipeError: [Errno 32] Broken pipe`, finalize not started, backup status
  unknown, and `evidence_validation: FAIL`.
- This validation failure describes an interrupted finalize/backup chain. It
  does not by itself mean the preserved checkpoints are corrupt.
- No credential, token, secret, `.env`, or submission-configuration file is
  present in the archive member list. Metadata contains boolean presence flags
  only, not secret values.

This is the official fresh trajectory source for the later recovery run. It is
not a completed uninterrupted official 5K result and must retain its failed /
interrupted status in analysis.
