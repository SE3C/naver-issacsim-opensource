> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/research/experiments/h1/exp-h1-action-planar-tracking-fresh-interaction.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# exp-h1-action-planar-tracking-fresh-interaction

- Robot: H1
- Experiment question: In a fresh run, does pairing stronger planar tracking with reduced action-rate regularization improve forward and rough-terrain progress while retaining acceptable zero/lateral/yaw tracking and stability?
- Preset reference: frozen `h1-submit-2`.
- Final overrides, verified from archived native reward source and resolved `env.yaml`: `track_lin_vel_xy_exp=0.75`, `action_rate_l2=-0.0001`. `track_ang_vel_z_exp=0.5`, feet air time `0.2`, termination `-50`, orientation `-1.5`, roll/pitch angular velocity `-0.05`, hip `-0.2`, torso `-0.1` remain at the source values.
- Training status: **OFFICIAL fresh3K and TOP09 same-reward continuation COMPLETED / exit 0 / validation PASS**.
- Policy status: 3K behavior report and TOP09 final9950 PERSONAL A4000 raw evaluation received; **HOLD**, no promotion or official score. The 3K keeper2950 has no separate evaluation recorded here.

## Actual Run

Run `20261017-140610-h1-lintrack-075-actrate-0001-term-50-fresh3k` used no parent, resume checkpoint, or imported source checkpoint. Command evidence records `Humanoid-v0`, 3,000 requested iterations, 4,096 environments, seed 42, headless execution, and `save_interval=50`. Metadata records OFFICIAL mode, normal completion, exit 0, completed finalize, successful official backup, 60 keeper checkpoints, and no collection errors. All nine checks in `validation.json` are PASS.

Native run path: `/workspace/training/humanoid/logs/rsl_rl/humanoid/2026-10-17_23-06-13`. Run time was 2026-10-17 14:06:10–14:42:55 UTC. The archived policy summary `report.html` displays iter 2850 / total 3000; it is not the latest keeper or a statement of the final console iteration. The latest numbered keeper is `model_2950.pt`, SHA-256 `952330c4d95c61e5104e446fdf947a94c38ad7feac6e4806b8164d709826fba3`. `model_best.pt` and indexed native `model_2850.pt` share SHA-256 `8238421049335a19c288986ed58aa84f01468da315fbf6c355ee45088934f959`.

## Evidence and lineage

- Canonical Originals directory: `SE3C/naver-issacsim-originals:data/raw/official_server_runs/h1/2026-10-17_140610_lin075_action0001_fresh3k/`.
- Original wrapper: `20261017-140610-h1-lintrack-075-actrate-0001-term-50-fresh3k-download.tar.gz`, SHA-256 `6b8eaa8d7007c120a63840acd36cf762980a82048a466250963bb5691e0bfb97`.
- Resolved sources: `native_run/params/env.yaml` SHA `c082c5d4663cacf643641c2d72a6b4b859d4e3b6c7906135f027fb214583af81`; `native_run/params/agent.yaml` SHA `27308e8a2288335081dc26a5755fcd5a052360be8b33cb3203fddba0bc877aff`; `source/humanoid_rewards.py` SHA `15267130f596a2a922e60ff0f6d8b4566ee240f3dc49de4897ec7141548262cc`. Exact files and hashes are listed in the preserved run `SHA256SUMS`.
- Separate PERSONAL evaluation artifact received for `model_2850`: `20261017-140610-h1-lintrack-075-actrate-0001-term-50-fresh3k_model_2850_h1_6terrain_evaluation_20261018-010134_e75c39b0.zip`, SHA-256 `bafeffabcc0e3d7c5b8e0548f2f6dc491c98607b2d9b49ec53c2ff1a1e353f2f`. Its `source_checkpoint` SHA matches the indexed native `model_2850.pt`; the evaluation `source_run_id` is null. This identity link is not a policy-quality conclusion.
- [Published training Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261017-exp-h1-action-planar-tracking-fresh-interaction-fresh3k): original archive and checksum remote sizes/digests verified; canonical preservation commit `0eb5dea`.
- [Published PERSONAL evaluation](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261018-exp-h1-action-planar-tracking-fresh-interaction-model2850-video-eval): original 18-file ZIP plus checksum/publication manifest; remote sizes/digests verified. COMPLETE/non-smoke, 128env × three seeds × eight cases =3072 episode rows. Publication commit `c427b0b`; no new GPU run or A/B comparison.

## Behavior report received — 2026-10-18

[Preserved report and review](<../../../reports/experiments/h1/analysis/2026-10-18_H1_LIN075_ACTION0001_MODEL2850_POLICY_REVIEW.md>): all3072 episodes survive20s; H5 progress mean/P05/min9.867/9.640/9.514m, stall>.05 0/384, but H4/H5 yaw errors .2725/.2730rad/s and H3 world residual2.605m. **HOLD** for current representative policy. Legacy report lookup could not attribute training; current train index/publication SHA linkage supplies that context without rewriting raw nulls. The report's historical comparisons are unmatched references, not a new paired comparison. Alternating500black boxes frames are a reported capture defect, not a fall or an independently reproduced renderer diagnosis.

## TOP09 unchanged continuation received — 2026-10-18

- Actual Run: `20261018-105744-h1-top09-same-reward-to10k`, **OFFICIAL COMPLETED**, exit 0, finalize completed, backup success, evidence validation PASS. This is not the accidental PERSONAL Run `20261018-103844-h1-top09-same-reward-to10k`.
- Same resolved reward configuration: `h1-submit-2 + lin=0.75 + action=-0.0001`; authoritative archived `native_run/params/env.yaml` and reward source, not the display alias. Seed 42, 4,096 environments, start iteration 2950, requested +7050; final saved keeper `model_9950.pt`. The requested target does not imply an existing `model_10000.pt`.
- Imported parent SHA `952330c4d95c61e5104e446fdf947a94c38ad7feac6e4806b8164d709826fba3` matches the earlier OFFICIAL fresh3K Run's indexed `model_2950.pt`. This external identity join does not rewrite raw `parent_run_id=null` or `source_provenance_verified=false`. Source identity is unchanged during this Run; task-source Git commit is null.
- Final keeper SHA: `086cac9dbac3261dc44d8d079dcbdce658cbb28e34da7bbb7c309589c48d4d0e`; archive bytes and checkpoint index agree.
- Canonical training evidence: `SE3C/naver-issacsim-originals:data/raw/official_server_runs/h1/2026-10-18_105744_lin075_action0001_resume10k/`. Original download archive SHA `ba9334e5e4509a318562fb4ca31ae712392979b2e3ac9b6e99c79efd7a3fe995`, 959,601,708 bytes. [Training Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261018-exp-h1-action-planar-tracking-fresh-interaction-top09-resume10k).
- Separate **PERSONAL Linux A4000** camera-off `scenario7` / `internal-suite-v1` evaluation: COMPLETE/non-smoke, 128 environments × seeds 4201/4202/4203 × eight cases × 20 seconds, 3,072 unique episode rows. Policy SHA matches final9950. ZIP SHA `5473f31abbef9bb09736073572b3cec83fcdf9f37d0f4698988f28e1a69f3f26`, 548,968 bytes; three raw data files only, no videos, comparison report or official score. [Evaluation Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261018-exp-h1-action-planar-tracking-fresh-interaction-model9950-a4000-eval).
- Decision: **HOLD / quality analysis pending**. Intake confirms completion and identity, not policy superiority, a reward-specific causal effect, or a submission decision.
