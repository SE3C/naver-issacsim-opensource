# [학습] H1 ACTRATE-0001 + feet_slide · OFFICIAL fresh 3K

- Experiment: `exp-h1-action-foot-contact-stability`; preset reference `h1-submit-2`, displayed overrides `{"action_rate_l2":-0.0001,"feet_slide":-0.35}`. This display is not a complete resolved configuration.
- Actual training Run: `20261013-153313-h1-actrate0001-feet_slide-fresh3k`; OFFICIAL / H1 / train / fresh, no parent checkpoint or resume. Seed 42, 4096 environments, requested 3000 iterations, COMPLETED / exit 0 / validation PASS.
- Native Run: `/workspace/training/humanoid/logs/rsl_rl/humanoid/2026-10-14_00-33-21`. Full native env/agent YAML, reward source and source identity are preserved inside the original nested evidence archive.
- Verified native command: `/workspace/IsaacLab/isaaclab.sh -p /workspace/training/humanoid/train.py --task Humanoid-v0 --max_iterations 3000 --num_envs 4096 --seed 42 --headless agent.save_interval=50`.
- Selected for PERSONAL post-training evaluation: indexed `model_2950.pt`, 7151477 bytes, SHA-256 `c4b283509cc659e7bd47f5bf49eddbc387a43963d751ef353c632f48c7da1374`. This is not an assertion that auto-best or the final console iteration is 2950.
- Received wrapper: `20261013-153313-h1-actrate0001-feet_slide-fresh3k-download.tar.gz`, 419078411 bytes, SHA-256 `9c7ffdac7cc4cbed0652b4bda028de950f0d1d3ed3510efdfcbcee04381bb409`. Nested archive hash matches the embedded sidecar. Preserve original wrapper/checkpoints/logs unchanged.
- Release: https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261013-exp-h1-action-foot-contact-stability-fresh3k
- Separate PERSONAL evaluation: https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261014-exp-h1-action-foot-contact-stability-model2950-video-eval

Assets: unchanged download wrapper, its external checksum, this preservation note. Training completion and PERSONAL evaluation completion do not establish policy adoption, reward causality, a new submission preset or an OFFICIAL score. Analysis/adoption decision remains pending/HOLD. Downloads originals are retained.
