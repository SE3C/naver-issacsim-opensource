# exp-h1-action-rate-smoothing

## 2026-10-18 same-reward resume toward 10K and PERSONAL A4000 evaluation

OFFICIAL Run `20261018-092452-h1-top07-same-reward-to10k` completed with exit 0 and evidence validation PASS. It resumed from stored iteration 2,950, requested 7,050 additional iterations, and produced final saved keeper `model_9950.pt` (not model9999). Effective reward remained `h1-submit-2 + action_rate_l2=-0.001`; seed 42, 4,096 envs. Archive SHA-256 is `72449e4ba3b0cf5bc3b9d1278b243e7e273f982513198fe202e544a8598c141b` (958,182,392 bytes). The keeper SHA-256 `642255c41cf09dac6a9401985f70cce0177c41cd87b85aa085a5f35bbbdf09c6` matches the archive checkpoint index and SHA256SUMS.

The parent checkpoint SHA `8914b6b48e74a6463808f629648f87900efdb853e5253e142e99c738adb2d085` is recorded as `user_imported_checkpoint`; source Run ID is null and `source_provenance_verified=false`. Do not present the parent lineage as verified. A separate PERSONAL Linux A4000 camera-off scenario7 evaluation is COMPLETE/non-smoke, with 128 envs, seeds 4201/4202/4203, eight cases, 20 seconds/case, and 3,072 episode rows. Its manifest policy SHA matches the keeper. The three-file evaluation ZIP is 547,067 bytes, SHA-256 `00967e49176bcd03742db776f2d8ae4ce8ea633a6a9d9435cdac0cc26fcb953a`; no videos, comparison report, or official score are included.

Training Release [published and verified](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261018-exp-h1-action-rate-smoothing-resume10k); evaluation Release [published and verified](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261018-exp-h1-action-rate-smoothing-model9950-a4000-eval). Analysis and adoption decision remain pending/HOLD; the earlier HOLD remains until the new Run is reviewed.

- Robot: H1
- Display descriptor: `ACTRATE-001`
- Status: OFFICIAL training COMPLETE/PASS; PERSONAL evaluation/behavior analysis complete; policy **HOLD**
- Environment target: OFFICIAL
- Training mode: fresh
- Requested length: 3,000 iterations
- Run ID: `20261010-125324-h1-actrate-001-fresh3k`
- Baseline preset: `h1-submit-2`
- Final override: `h1-submit-2 + action=-0.001`
- Single reward delta: `action_rate_l2 -0.0005 → -0.001`
- Run outcome: OFFICIAL fresh training completed; this is independent of `ORIENT-100` and `ACTRATE-0001`

## 2026-10-11 PERSONAL policy behavior analysis received — HOLD

[원문 심층 분석](../../../data/processed/incoming/other/reviewed/H1_MODEL2850_SHA1E6D_POLICY_ANALYSIS_20261010.md) · [AI 라이브러리 판단 기록](../../../data/processed/experiments/h1/2026-10-11_ACTRATE001_MODEL2850_POLICY_REVIEW.md). The analysis of the existing 2026-10-10 Windows `scenario7` ZIP reports **3,072/3,072** 20-second timeout survivals, H2/H7 body-forward **15.470/10.656 m**, H6 up/down **20.297/20.058 m**; but H1 zero-command unintended body-forward **1.164 m** (mean world XY drift **1.151 m**), H3 lateral unintended forward **1.109 m** (mean world XY displacement **2.177 m**), rough H5 mean/P05 body progress **9.359/8.921 m** and stairs/boxes quantitative gaps. **Policy decision HOLD**, not all-terrain PROMOTE. The source report directly analyzed its ZIP; this GitHub intake did not newly rerun the evaluator or the MP4s.

The report's standalone ZIP has `source_run_id=null` and cannot prove the training origin itself. Existing verified OFFICIAL `ACTRATE-001` Run `20261010-125324-h1-actrate-001-fresh3k` independently records identical full checkpoint SHA `1e6d0950f5bd981ca1f88044e65ae7ee57505c47b92b5caad8c39263f4d93bb1`, establishing a *cross-record* identity link without rewriting the ZIP. This is **not** `ORIENT-100/model_2850` (SHA `6aed…f7b0`). First seek the existing unchanged `h1-submit-2 / TERM-50` `model_2800` matched `scenario7` raw, checking protocol/agent/source/PPO/terrain/seed/command parity before any performance-causality claim. No new GPU job or Optuna trial.

## Question

Does strengthening the H1 action-rate penalty from `-0.0005` to `-0.001`, while keeping the rest of the frozen `h1-submit-2` configuration unchanged, improve action smoothness and locomotion stability without sacrificing tracking, terrain progression, or survival?

This is a separate Experiment question. It is not a new `H-xxx` legacy ID. The Run ID above identifies its first actual training execution.

## Planning rationale

The current H1 baseline uses `action_rate_l2=-0.0005`. External humanoid systems provide a directional prior that stronger action smoothing can be useful, but their reward definitions, scales, curricula and evaluators differ from NCRC. Public examples using substantially stronger values such as `-0.005` or `-0.01` are therefore not directly transferable, and a previously observed public `-0.0025` long-run failure signal argues for a conservative first step.

The planned first test was therefore `ACTRATE-001` at `-0.001`, not a jump to the larger external magnitudes. The actual Run and its evidence are recorded below.

## Effective configuration

Start from the full frozen `h1-submit-2` resolved configuration and change only:

```text
action_rate_l2: -0.0005 -> -0.001
```

Keep the other known `h1-submit-2` reward values unchanged, including:

- `termination_penalty=-50`
- `feet_air_time=0.20`
- `track_lin_vel_xy_exp=0.5`
- `track_ang_vel_z_exp=0.5`
- `flat_orientation_l2=-1.5`
- `ang_vel_xy_l2=-0.05`

Do **not** inherit `ORIENT-100` into this `ACTRATE-001` Run. The two single-delta experiments are separate questions.

The Run evidence, not this plan, determines the effective configuration. Source before/after snapshots matched; the source commit is unknown. The full resolved configuration is sourced from inner archive members `<RUN>/native_run/params/env.yaml` and `<RUN>/native_run/params/agent.yaml`, with source identity in `<RUN>/source/identity.json`. Full preset/PPO parity has not been established.

## Original execution plan

- OFFICIAL server
- fresh 0→3K
- seed 42
- 4,096 environments
- same native PPO/task/source as the verified official H1 environment unless the current server source has changed
- no checkpoint parent
- the 2026-10-07 `ORIENT-100 / model_2850` PERSONAL behavior analysis is already received and classified HOLD; this order does not make `ORIENT-100` an ACTRATE training parent or authorize a Run
- preserve console, TensorBoard, checkpoints, resolved `env.yaml`/`agent.yaml`, source fingerprint, report/export and evidence archive according to the current `issacsimz` official procedure

This historical plan did not itself authorize a server start or training. The actual completed Run is documented below.

## Comparison and current H1 evaluator evidence (2026-10-07)

At the 2026-10-04 planning snapshot, the PERSONAL evaluator core and H1 Windows launcher had no GPU validation. On 2026-10-07, a full **single-policy** H1 Windows PERSONAL evaluation of `ORIENT-100 / model_2850` was received: 3,072/3,072 episodes reached 20-second timeout without base-contact failures, but balance/lateral body-forward drift and rough-terrain tracking/progress tails led to **HOLD**. [Original analysis](../../../data/processed/incoming/other/reviewed/H1_ORIENT-100_POLICY_ANALYSIS_20261007.md) and [Experiment detail](exp-h1-rough-terrain-orientation-relaxation.md). This establishes one H1 full GPU case, **not** a matched `h1-submit-2` control, ORIENT reward-effect proof, validated ACTRATE result or official score.

For this completed ACTRATE Run, review training evidence first; any matched PERSONAL diagnostic requires separately authorized execution and checked evaluator/command/terrain/seed/source parity:

1. Preferred control: verify source/PPO/seed/schema parity against OFFICIAL unchanged fresh 3K `h1-submit-2` Run `20261008-062732-h1-term-50-fresh3k-control` (COMPLETE/PASS); the first 3K of the old official fresh 5K Run is a secondary historical training comparison.
2. Compare terrain progression, XY/yaw tracking, base-contact/fall proxy, timeout/episode length, action std and available action-rate/posture reward terms.
3. Use native terrain videos only as qualitative evidence unless command and terrain conditions are matched.
4. Do not claim official NCRC score improvement without an actual competition evaluation.

## 2026-10-10 related Experiment status (verified evidence)

- [ACTRATE-0001 action-rate relaxation](exp-h1-action-rate-relaxation.md) weakens the same penalty to `-0.0001` on the frozen baseline. OFFICIAL fresh3K training `20261009-142350-h1-actrate-0001-fresh3k` COMPLETED/PASS. Its model_2700 has a distinct PERSONAL six-video/full scenario7 evaluation, and a received single-policy behavior analysis (policy HOLD); the 9,216-row TERM-50 matched-cohort-index comparison is complete, while independent-training-seed and identical-physical-terrain causal A/B remain unverified. A future comparison of ACTRATE-001 with comparable evidence should compare both directions (`-0.001`, `-0.0001`) against unchanged `-0.0005`.
- [ANGTRACK-065 angular-tracking boost](exp-h1-angular-tracking-boost.md) tests `track_ang_vel_z_exp=0.65` separately, without inheriting any ACTRATE change. OFFICIAL fresh3K Run `20261009-155344-h1-angtrack-065-fresh3k` COMPLETED/PASS; analysis/evaluation pending (HOLD).

Both related training Runs have verified completion evidence; they remain separate experiments and do not change this Run's independent single-delta protocol. ACTRATE-001 now has a completed PERSONAL video/evaluation and a received single-policy behavior analysis (HOLD). This does not establish causal reward benefit or an official score.

## 2026-10-10 OFFICIAL training Run

- Environment: OFFICIAL H1 server; fresh; seed 42; 4096 environments; no parent Run/checkpoint.
- Requested/actual iterations: 3000 requested; completed 0–2999 (3000 iterations); process exit 0; validation PASS.
- Final override: `h1-submit-2 + action=-0.001`; distinct from `ACTRATE-0001` at `action=-0.0001`.
- All 12 active reward weights: `track_lin_vel_xy_exp=0.5`, `track_ang_vel_z_exp=0.5`, `ang_vel_xy_l2=-0.05`, `action_rate_l2=-0.001`, `feet_air_time=0.2`, `flat_orientation_l2=-1.5`, `termination_penalty=-50`, `joint_deviation_hip=-0.2`, `joint_deviation_torso=-0.1`, `dof_pos_limits=-1`, `feet_slide=-0.25`, and `joint_deviation_arms=-0.2`. These weights are a subset of the full resolved configuration in `native_run/params/env.yaml`; they are not the complete configuration.
- Resolved configuration members: `<RUN>/native_run/params/env.yaml`, `<RUN>/native_run/params/agent.yaml`; source identity: `<RUN>/source/identity.json`. Source before/after snapshots match; source commit unknown. Full preset/PPO parity has not been established.
- Source: before/after snapshots match; source commit unknown.
- Checkpoints: best `model_2850.pt` (SHA-256 `1e6d0950f5bd981ca1f88044e65ae7ee57505c47b92b5caad8c39263f4d93bb1`); last preserved `model_2950.pt` (SHA-256 `8914b6b48e74a6463808f629648f87900efdb853e5253e142e99c738adb2d085`). No `model_2999.pt` artifact is asserted.
- Separate Windows PERSONAL behavior analysis of best `model_2850.pt`: **received**, single-policy quality **HOLD**. Training-curve causal/matched-policy assessment is still not established; last numbered `model_2950.pt` has not been promoted on this basis.
- Canonical evidence directory: `naver-issacsim-originals/data/raw/official_server_runs/h1/2026-10-10_215330_actrate001_fresh3k/evidence_archives/`.
- Outer archive: SHA-256 `ab507e1a2b060469413d4f8ada9a4663a5e3eff81cbe0ca85612dd16e5e68966`; size `418745259` bytes. Inner training archive SHA-256 `7265418b6d6843a05a67330ab5300110388b63e7ccc196fb972b93b259770b59`. [Verified OFFICIAL training Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261010-exp-h1-action-rate-smoothing-fresh3k) (asset 418,745,259 bytes; SHA-256 `ab507e1a2b060469413d4f8ada9a4663a5e3eff81cbe0ca85612dd16e5e68966`).

## 2026-10-10 Windows PERSONAL post-training evaluation

- This is a post-training evaluation of the existing ACTRATE-001 Run, not a new training Run, official score, or A/B comparison.
- Source OFFICIAL training Run: `20261010-125324-h1-actrate-001-fresh3k`; selected checkpoint `model_2850.pt`, SHA-256 `1e6d0950f5bd981ca1f88044e65ae7ee57505c47b92b5caad8c39263f4d93bb1`. The external SHA lineage match identifies this as ACTRATE-001; the ZIP's embedded `source_run_id=null` remains unchanged. Another H1 policy also uses the filename `model_2850.pt`; use the SHA and Run ID to disambiguate.
- Six `maneuver_push` terrain videos (20 seconds each, H1 ±10° slopes) followed by a separate camera-off H1 `scenario7` evaluation. Evaluation COMPLETE, `complete=true`, `smoke=false`; seven scenario groups, with 8 cases × 128 environments × 3 seeds (4201/4202/4203) = 3,072 episode rows. No metric interpretation is recorded here.
- Integrated ZIP: `model_2850_h1_6terrain_evaluation_20261010-233937_1cc2ab9d.zip`, 35,121,564 bytes, 18 files, CRC valid; SHA-256 `1906880030393b904d7323bdbf71352f408a067328a09ac8bf87604438c07351`.
- [Canonical Originals backup](https://github.com/SE3C/naver-issacsim-originals/tree/main/data/raw/official_server_runs/h1/2026-10-10_215330_actrate001_fresh3k/personal_windows_eval_20261010) · [PERSONAL video/evaluation Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261010-exp-h1-action-rate-smoothing-model2850-video-eval).
- Canonical Originals commit: `5dcbfe36b3fc6fd014a3eb738b9e56518afd1300`. Release ZIP remote size/SHA match: 35,121,564 bytes / `1906880030393b904d7323bdbf71352f408a067328a09ac8bf87604438c07351`. Annotated tag target is evaluator task commit `ef10b7a4c9a83481346d446e8a75aed655f72214`, not the OFFICIAL training source commit.
- [Publication/provenance record](../../../data/processed/operations/windows_h1_video_evaluation/2026-10-10_ACTRATE001_MODEL2850_PUBLICATION.md).
- A subsequent [single-policy behavior report](../../../data/processed/incoming/other/reviewed/H1_MODEL2850_SHA1E6D_POLICY_ANALYSIS_20261010.md) and [HOLD review](../../../data/processed/experiments/h1/2026-10-11_ACTRATE001_MODEL2850_POLICY_REVIEW.md) are received. Evaluation completion and 3,072 timeout survivals do not establish reward improvement or official promotion.

## Decision after evidence

The evidence archive and Release are verified. The PERSONAL single-policy behavior decision is **HOLD**; matched baseline evidence, complete source/PPO parity, and reward-causal judgment remain outstanding. This is not a submission or official score.
