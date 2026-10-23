# H1 ACTRATE-0001 — OFFICIAL fresh 10K

- Experiment: `exp-h1-action-rate-relaxation`; display `h1-submit-2 + action=-0.0001`.
- Run: `20261011-041745-h1-actrate-0001-fresh10k-official`; H1 / train / OFFICIAL / fresh, no checkpoint parent and no resume. This is a separate Run from the completed 2026-10-09 fresh3K experiment.
- Requested iterations: 10,000; metadata completed, exit 0, evidence validation PASS, native finalize and official backup completed. Seed 42, 4096 environments.
- Native Run `/workspace/training/humanoid/logs/rsl_rl/humanoid/2026-10-11_13-17-54`; metadata start/end UTC `2026-10-11T04:17:45.241178+00:00` / `2026-10-11T06:19:34.270277+00:00`. Exact final console iteration and latest keeper filename were not independently checked; automatic best is not a final-endpoint claim.
- Checked report weights: lin=0.5, ang=0.5, feet=+0.20, termination=-50, orientation=-1.5, angxy=-0.05, hip=-0.2, torso=-0.1, action=-0.0001. The complete native `params/env.yaml` and `agent.yaml`, archived reward source and source identity remain the resolved-config/provenance sources; the nine-value display is not a complete config or a full source/PPO parity claim.
- Preserved 201 organizer keeper checkpoints; checkpoint index has 202 entries including the native checkpoint. Console, TensorBoard, native params, source identity and exported artifacts remain inside the original wrapper.
- Automatic best `model_best.pt` matches indexed native `model_9900.pt`, SHA-256 `6dd795e32383bc21ac487ea039bb2a03a565ec2ee6da893a3dc4ffaa844c769d`. Native report's peak reward step 9880 is not the numbered checkpoint step; record the roles separately.
- Received wrapper: `20261011-041745-h1-actrate-0001-fresh10k-official-download.tar.gz`, **1,358,051,174 bytes**, SHA-256 `6977db0f4cea94d7685023a4b58702290f762e2c075525bc977173a2d54ebdb7`.
- Nested evidence archive: `20261011-041745-h1-actrate-0001-fresh10k-official.tar.gz`; streamed SHA-256 `46fec3c49eac8e357f9916b422d8885bf94786639fae84520fd4501d706f8eb6` matches its received checksum. Native validation records PASS; the nested archive is not a second training Run.
- Credential/key/.env candidate paths were not found in the inspected archive lists; metadata contains credential-presence booleans, not credential values.

Canonical preservation: this directory's `evidence_archives/` contains the unchanged received wrapper and its external SHA-256. Do not flatten, rename checkpoint files, repackage, or overwrite the source. Downloads original is retained.

Release: https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261011-exp-h1-action-rate-relaxation-fresh10k

Assets: original wrapper + external checksum + preservation note. **Training COMPLETED/PASS; policy quality analysis pending/HOLD.** This intake does not establish a new 10K video/evaluator result, a submitted policy, an official score or a new submission preset. Historical model_2700 evaluation belongs to the fresh3K Run, not this 10K Run.
