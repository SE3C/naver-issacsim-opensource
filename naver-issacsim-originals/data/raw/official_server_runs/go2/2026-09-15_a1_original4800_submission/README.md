# Go2 A1 original-4800 official submission export

## Canonical received bundle

| Field | Value |
| --- | --- |
| source | user-provided `3.zip`, identified as created on the official server |
| received/canonical name | `3.zip` |
| bytes | 1,079,093 |
| SHA-256 | `a16f26b6e4b3ba15cf333c35e9111bfa64b7a9aedb411b1c09c849bcba7a10df` |
| internal root | `3차 제출/` |

The received ZIP is preserved byte-for-byte with its original filename. It was extracted
only into a temporary inspection directory and was not edited or repacked. The Release
asset uses a descriptive filename while retaining identical bytes.

## Contents and identity checks

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `3차 제출/policy.pt` | 1,159,510 | `387237907daa02998f720c0f861c4e504445b96ca0f176d81cbab7765b92b254` |
| `3차 제출/env.yaml` | 28,503 | `133ea8c46714c93dc7ee100f9518f038529aa38779ae4624d31f13af285278a9` |
| `3차 제출/기술 개선 리포트.txt` | 1,074 | `ad69df76a481717e18eb96791f67eb73452e41ca44a5edfe988b21f98459af57` |

- `env.yaml` is byte-identical to the native environment configuration preserved by the
  official fresh A1 run `20260914-084321-go2-a1-tracklin150-lvz-m2-5k-official`.
- Every one of the eight tensor payloads in `policy.pt` matches an actor tensor payload in
  that run's original `model_4800.pt` (checkpoint SHA-256
  `ea93f9b5b04d91a91d1cdb97c6d328978017991e0602745f9269c7190bfaba65`).
- The policy SHA differs from the discarded mixed package's recovery-4900 policy SHA
  `22957506fefe1cde249548705fef30147fe149e1086c926ff447ff001c2cc277`.

These checks identify the bundle as a fresh official export of the original-4800 A1
candidate, not the previously rejected 4800/4900 mixed package. They do not independently
prove that the bundle was submitted to the competition portal; submission status must be
recorded separately.
