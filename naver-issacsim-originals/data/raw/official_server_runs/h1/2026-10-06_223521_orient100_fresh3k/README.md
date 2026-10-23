# H1 ORIENT-100 — OFFICIAL fresh 3K, 2026-10-06

Received from the user's Downloads/of folder. Original archive and loose exports are preserved byte-for-byte. Analysis is in progress; no quality decision, evaluation score, or submission is asserted.

- Experiment: `exp-h1-rough-terrain-orientation-relaxation`
- Run: `20261006-133517-h1-orient-100-fresh3k-official`
- Native run: `/workspace/training/humanoid/logs/rsl_rl/humanoid/2026-10-06_22-35-21`
- OFFICIAL / train / fresh, no parent; seed 42, 4096 environments, requested/completed 3000 iterations (console ends at 2999/3000).
- Completed, exit 0, validation PASS; native finalize completed, backup success. This is backup, not a portal submission.
- Preset-relative reward display: `h1-submit-2 + orientation=-1.0`. Confirmed reward weights: lin/ang 0.5/0.5, feet 0.20, term -50, orientation -1.0, angxy -0.05, hip -0.2, torso -0.1, action -0.0005.
- Full resolved config: nested train evidence `native_run/params/env.yaml` and `agent.yaml`; source fingerprint: `source/identity.json`. Full source/PPO parity with Round 2 is not asserted from the reward display alone.
- Save interval 50; 60 organizer-preserved checkpoints. Automatic best `model_2850.pt`: SHA `6aedeced60562c1d496d5319d29b76cf9e26ff43df06827cb370f24f5313f7b0`. Latest preserved checkpoint `model_2950.pt`: SHA `a0748cd294c52710806ef9dbd4c9ade3d20b40461b7e5f238f67c7eb36a76e5f`; origin `organizer_keeper_backup`.
- Wrapper: `evidence_archives/20261006-133517-h1-orient-100-fresh3k-official-download.tar.gz`, 418957086 bytes, SHA `85ea5dd5e6ccd4f9edee587fb7a4dacd2f311caa4dd256e3c1b57744bd4fed83`.
- Nested evidence archive: `20261006-133517-h1-orient-100-fresh3k-official.tar.gz`, 412424848 bytes, SHA `c589ff4d5c4d3b5559d96ab0195610eebb492082bb70d5331654cb77c0ec2fbf`; matches its received checksum. Do not count wrapper and nested archive as two Runs.

Loose exports: `exports/model_best.pt` (7151477 bytes; same SHA as 2850), `exports/env.yaml` (33530 bytes; SHA `a142cb19a855a7b8b61d96d9715e1bd270e7475df5145e3fe3541fae9edc2357`), `exports/report.html` (14381 bytes; SHA `9d5ac21550baccf5d112bb67aa4de830c6fd7782f59ed13836cf98f74b3b78eb`). They also occur inside the wrapper.

Release: https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261006-exp-h1-rough-terrain-orientation-relaxation-fresh3k

Only the unchanged wrapper, its external checksum and this preservation note are Release assets; nested evidence/checkpoints remain inside the wrapper. No videos, policy.pt, evaluator result, or analysis report was received in this intake. Downloads originals have not been moved or deleted.
