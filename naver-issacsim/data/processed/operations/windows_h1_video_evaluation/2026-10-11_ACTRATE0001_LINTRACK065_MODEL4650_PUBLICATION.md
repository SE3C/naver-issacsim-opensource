# ACTRATE-0001 → lin=0.65: training and model_4650 publication

- Experiment: [exp-h1-action-first-planar-tracking-switch](../../../../research/experiments/h1/exp-h1-action-first-planar-tracking-switch.md).
- OFFICIAL train Run `20261010-154926-h1-actrate0001-lintrack065-from2700-plus2k`: resume from imported model_2700, +2000 iterations, console end4699/4700, exit0, validation PASS. Latest keeper4650 differs from automatic best2900. No fresh5K claim.
- Raw parent provenance=false/unknown/null remains unchanged. Parent SHA matches the existing OFFICIAL ACTRATE-0001 model2700; separate publication linkage is not a retroactive provenance rewrite.
- PERSONAL Windows evaluation ZIP: six H1 videos and separate full scenario7, COMPLETE/non-smoke, checkpoint SHA matches train index model4650. 18 files, ZIP CRC PASS. No GPU job was launched in this publication task.
- Original raw bytes preserved in Originals commit `19cbb9e`. Official training Git commit unknown. NVIDIA annotated evaluation tag targets actual task checkout `ef10b7a4c9a83481346d446e8a75aed655f72214`.
- [Training Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261011-exp-h1-action-first-planar-tracking-switch-resume2700-plus2k).
- [Video/evaluation Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261011-exp-h1-action-first-planar-tracking-switch-model4650-video-eval).

## Remote verification — 2026-10-11 KST

Both Releases contain exactly three assets: original archive, SHA sidecar, publication_manifest.json. All six remote sizes/digests matched their local files via GitHub API after upload.

| Repository | Original asset | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| Originals | `20261010-154926-h1-actrate0001-lintrack065-from2700-plus2k-download.tar.gz` | 286230956 | `4e604b7d29a0a4b220b44b2b60081b7742109e9b67b266d90434df234f925e3d` |
| NVIDIA | `model_4650_h1_6terrain_evaluation_20261011-030854_89b4c4a0.zip` | 35747757 | `5fa60c81a3808481b9a547ab097fa527a708e792992ea4443d66be3c5900ae3d` |

Canonical Originals paths:

- `data/raw/official_server_runs/h1/2026-10-11_004932_actrate0001_lintrack065_resume2700_plus2k/`
- `data/raw/private_server_runs/h1/2026-10-11_windows_actrate0001_lintrack065_model4650_video_evaluation/`

Publication is complete. At publication time analysis/AI-library delivery was pending/not requested; the later user request supplied the [model4650 report](../../incoming/other/reviewed/H1_MODEL4650_POLICY_ANALYSIS_20261011.md), now integrated with [policy review](../../experiments/h1/2026-10-11_ACTRATE0001_LINTRACK065_MODEL4650_POLICY_REVIEW.md) and the AI library. Policy decision remains HOLD; matched unchanged +2K control/adoption pending. No OFFICIAL score or submission is inferred. Downloads originals were neither modified nor deleted.
