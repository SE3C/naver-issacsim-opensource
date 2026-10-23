> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/experiments/h1/training/2026-10-17_LIN055_ANG075_ACTION0003_FRESH3K_EVIDENCE_INTAKE.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# H1 LIN-055 + ANG-075 + ACTION-0003 fresh3K — OFFICIAL training intake

- Experiment: [exp-h1-rotation-priority-tracking](<../../../../research/experiments/h1/exp-h1-rotation-priority-tracking.md>).
- Run ID: `20261017-145042-h1-lintrack-055-angtrack-075-actrate-0003-fresh3`.
- Mode/lineage: OFFICIAL, fresh, no parent/resume/imported checkpoint; `Humanoid-v0`.
- Actual command settings: `--max_iterations 3000 --num_envs 4096 --seed 42 --headless agent.save_interval=50`. Metadata status `completed`, exit code 0, official finalize completed, official backup success; evidence validation overall PASS (all nine checks).
- Native run: `/workspace/training/humanoid/logs/rsl_rl/humanoid/2026-10-17_23-50-48`; metadata time 2026-10-17 14:50:42–15:27:49 UTC. There are 60 numbered keeper checkpoints and 61 index entries. The policy summary selects iteration 2700 (`model_best.pt` SHA matches indexed `model_2700.pt`); latest numbered keeper is `model_2950.pt` SHA `ca40a6b1bc10d1d23af9f7e0acae74229fbd91c45998055a59cb22205163519c`.
- Actual final reward values from archived `humanoid_rewards.py` and resolved `env.yaml`: lin `.55`, ang `.75`, feet air `.20`, termination `-50`, flat orientation `-1.5`, ang XY `-.05`, hip `-.2`, torso `-.1`, action rate `-.0003`. Thus final preset-relative changes are lin `.50→.55`, ang `.50→.75`, and action `-.0005→-.0003`; the other listed values are unchanged from `h1-submit-2`.
- Resolved configuration source: canonical Originals directory `data/raw/official_server_runs/h1/2026-10-17_145042_lin055_ang075_action0003_fresh3k/`, containing archived `native_run/params/env.yaml`, `native_run/params/agent.yaml`, and `source/humanoid_rewards.py`. Their SHA-256 values are recorded in the linked Experiment detail.
- Canonical wrapper: `20261017-145042-h1-lintrack-055-angtrack-075-actrate-0003-fresh3-download.tar.gz`, 418,903,285 bytes; SHA-256 `e84310aeb92e482dee90e7c67b1483855451ed8eb402fb732bacb728ca73ad8a`.
- No separate PERSONAL evaluation artifact or behavior-analysis result is included in this intake. No policy-quality decision or official score is recorded.
- [Originals training Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261017-exp-h1-rotation-priority-tracking-fresh3k) published; original archive/checksum remote sizes and digests verified. Originals commit `0eb5dea`.

This intake records training evidence only. It assigns no policy-quality decision, official score, or 10K adoption status.
