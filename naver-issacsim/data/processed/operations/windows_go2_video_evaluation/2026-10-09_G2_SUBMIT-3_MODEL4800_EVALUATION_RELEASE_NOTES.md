# Go2 g2-submit-3 · model_4800 · PERSONAL six-video + evaluation

Unmodified Windows PERSONAL post-training evaluation of the original Round-3 submission checkpoint, not a new training Run or an official score.

- Checkpoint SHA-256: `ea93f9b5b04d91a91d1cdb97c6d328978017991e0602745f9269c7190bfaba65`.
- OFFICIAL source training: [original fresh run](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-go2-20260914-lintrack-150-linz-2-5k-interrupted), which remains **INTERRUPTED / validation FAIL**; successful PERSONAL evaluation does not change that state.
- [Original4800 official submission export](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-go2-20260915-lintrack-150-linz-2-original4800-submission); not recovery model_4900 or automatic-best model_7050.
- Six maneuver/push terrain videos and full camera-off scenario7: 128 environments, seeds 4201/4202/4203, nine cases × 20 seconds; 3,471 episodes, complete=true, smoke=false, native exit 0.
- Evaluation task checkout: `ef10b7a4c9a83481346d446e8a75aed655f72214`; this annotated tag records evaluation source, not the September training source.
- ZIP: g2-submit-3_model_4800_go2_6terrain_evaluation_20261009-021618_04460d33.zip; 36,843,939 bytes; SHA-256 `f2bb7917fd325544858ce5aecf801f54e24572c164ed5c6d38ed17c316a1d221`; 18 files.
- Assets: original ZIP, its SHA sidecar and publication_manifest.json. No separate MP4 duplication, official score, calibrated score or A/B report.

Canonical raw copy: `SE3C/naver-issacsim-originals/data/raw/private_server_runs/go2/2026-10-09_windows_model4800_video_evaluation/`. Original ZIP manifests were not rewritten; training linkage is recorded in the external publication manifest.
