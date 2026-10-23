# [학습] H1 ACTRATE-0001 + airtime025 · OFFICIAL fresh 3K

- Experiment: `exp-h1-action-airtime-fresh-interaction`; preset reference `h1-submit-2`, displayed overrides `{"action_rate_l2":-0.0001,"feet_air_time":0.25}`. This display is not a complete resolved configuration.
- Actual training Run: `20261013-144616-h1-actrate0001-airtime025-fresh3k`; OFFICIAL / H1 / train / fresh, no parent checkpoint or resume. Seed 42, 4096 environments, requested 3000 iterations, COMPLETED / exit 0 / validation PASS.
- Native Run: `/workspace/training/humanoid/logs/rsl_rl/humanoid/2026-10-13_23-46-24`. Full native env/agent YAML, reward source and source identity are preserved inside the original nested evidence archive.
- Verified native command: `/workspace/IsaacLab/isaaclab.sh -p /workspace/training/humanoid/train.py --task Humanoid-v0 --max_iterations 3000 --num_envs 4096 --seed 42 --headless agent.save_interval=50`.
- Selected for PERSONAL post-training evaluation: indexed `model_2950.pt`, 7151477 bytes, SHA-256 `14fd9ad432dfc2ba7696b0d48d9a31753f42c74727083429cc9f2c7299aaffd6`. This is not an assertion that auto-best or the final console iteration is 2950.
- Received wrapper: `20261013-144616-h1-actrate0001-airtime025-fresh3k-download.tar.gz`, 418977650 bytes, SHA-256 `be197500532832d3d43c4436e9f64b967ded6f1cd92e14e5b1ee6cd31a8fa90e`. Nested archive hash matches the embedded sidecar. Preserve original wrapper/checkpoints/logs unchanged.
- Release: https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261013-exp-h1-action-airtime-fresh-interaction-fresh3k
- Separate PERSONAL evaluation: https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261014-exp-h1-action-airtime-fresh-interaction-model2950-video-eval

Assets: unchanged download wrapper, its external checksum, this preservation note. Training completion and PERSONAL evaluation completion do not establish policy adoption, reward causality, a new submission preset or an OFFICIAL score. Analysis/adoption decision remains pending/HOLD. Downloads originals are retained.
