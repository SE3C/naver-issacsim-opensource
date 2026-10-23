# h1-submit-2 / TERM-50 — OFFICIAL fresh 3K control, 2026-10-08

Received from the user's Downloads. The original download archive and its three loose exports are preserved byte-for-byte. This is a fresh control Run, not a new submission preset, portal submission, evaluation or quality decision.

- Experiment linkage: baseline control for `exp-h1-rough-terrain-orientation-relaxation`.
- Evidence Run: `20261008-062732-h1-term-50-fresh3k-control`.
- Native run: `/workspace/training/humanoid/logs/rsl_rl/humanoid/2026-10-08_15-27-38`.
- OFFICIAL / train / fresh, no parent; seed 42 (resolved `agent.yaml`), 4096 environments, requested/completed 3000 iterations (console reaches 2999/3000).
- Start/end UTC: `2026-10-08T06:27:32.704453+00:00` / `2026-10-08T07:04:30.219668+00:00`.
- Completed, exit 0, validation PASS; native finalize completed and native backup succeeded. Backup is not a portal submission.
- Preset-relative reward display: `h1-submit-2`, no reward overrides. Confirmed weights: lin/ang 0.5/0.5, feet +0.20, termination -50, orientation -1.5, angxy -0.05, hip -0.2, torso -0.1, action -0.0005.
- Full resolved config: nested `native_run/params/env.yaml` and `agent.yaml`; reward source `source/humanoid_rewards.py`; source fingerprint `source/identity.json`. Matching the nine reward weights does not by itself establish full source/PPO parity with the historical Round-2 submission.
- Save interval 50; 60 organizer-preserved checkpoints remain inside the nested evidence archive. Automatic best `model_2800.pt` / loose `model_best.pt`: SHA-256 `dffaa77848741fed1f4d22d0b78d4d8911af49057541107845e4d1df02c09ad6`. Latest preserved `model_2950.pt`: SHA-256 `a568e8df7df74c0ed2f8c1929d106d3fbd9a6307700dfff35de9126a34266c3c`, origin `organizer_keeper_backup`; not the same policy as automatic best.
- Unchanged wrapper: `evidence_archives/20261008-062732-h1-term-50-fresh3k-control-download.tar.gz`, 418943382 bytes, SHA-256 `594f5fdf83b702b2d6e5e664b35a3d1e1d2b7f9a42c8891dd1faddc1bfea8c1c`.
- Nested archive: `20261008-062732-h1-term-50-fresh3k-control.tar.gz`, 412410073 bytes, SHA-256 `1f8485003755e0cbce80df4b99d389ff993624af76c7b3c862b0c5137859efda`, verified against its received sidecar. Wrapper and nested archive are one Run, not two.

Release: https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261008-h1-submit-2-fresh3k-control

Release assets are the unchanged download archive, its external checksum and this preservation note. Nested evidence, TensorBoard, checkpoints and config remain inside the archive; loose exports are also backed up under `exports/`. No videos, `policy.pt`, evaluator result or analysis report was received. Downloads originals were not moved or deleted. Matched evaluation and analysis remain pending.
