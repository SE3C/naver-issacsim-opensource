# H-008 LINTRACK075 PERSONAL 5K continuation — download handoff

This directory is the source for a small derived download bundle. It contains only the final
numbered checkpoint, matching environment configuration, native report, and a manifest. It is
not canonical evidence and does not replace `../received/`.

| File | Meaning |
| --- | --- |
| `model_4997.pt` | representative final numbered checkpoint |
| `env.yaml` | configuration collected from the native export |
| `report.html` | native finalize report; diagnostic only |
| `HANDOFF_MANIFEST.json` | source archive, hashes, lineage, and limitation |

`model_best.pt` is intentionally absent: the automatic finalizer selected `model_4900.pt`, while
this resume workflow uses final `model_4997.pt` unless a joint late-window regression is shown.
