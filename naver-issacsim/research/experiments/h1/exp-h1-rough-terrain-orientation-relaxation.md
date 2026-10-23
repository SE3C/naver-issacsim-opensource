# exp-h1-rough-terrain-orientation-relaxation

- Robot: H1
- Display descriptor: `ORIENT-100`
- Status: HOLD (single-policy PERSONAL analysis; OFFICIAL train completed/PASS)
- Environment target: OFFICIAL
- Training mode: fresh
- Requested length: 3,000 iterations
- Run ID: `20261006-133517-h1-orient-100-fresh3k-official`
- Baseline preset: `h1-submit-2`
- Final override: `h1-submit-2 + orientation=-1.0`
- Single reward delta: `flat_orientation_l2 -1.5 → -1.0`

## 2026-10-18 TOP03 ORIENT-100 continuation and A4000 evaluation

- Actual Run: `20261018-045508-h1-top03-same-reward-to10k`, OFFICIAL resume from iteration 2950, requested +7050, final iteration 9999; COMPLETED, exit 0, official finalize complete, evidence validation PASS. Effective reward values in archived `source/humanoid_rewards.py` are `h1-submit-2 + flat_orientation_l2=-1.0`.
- Parent: imported checkpoint SHA `a0748cd294c52710806ef9dbd4c9ade3d20b40461b7e5f238f67c7eb36a76e5f`. Raw `parent_run_id=null`, source mode unknown, and `source_provenance_verified=false`; do not infer which prior Run provided it. The previously evaluated ORIENT-100 `model_2850.pt` is distinct from this Run's parent `model_2950.pt`.
- Final `model_9999.pt` SHA `e4e1db54d134c38bb6bd1d15ce4c019f9c7ec39169bee633f256e40106ca19c4` is indexed in the evidence archive. Canonical raw: [Originals receipt](https://github.com/SE3C/naver-issacsim-originals/tree/main/data/raw/official_server_runs/h1/2026-10-18_orient100_resume10k/README.md); wrapper 965,378,147 bytes, SHA `caf808e7f58275667e5709fe507afa9f473c34449ca2ace7c1c19cd53f44f205`. No source Git commit is recorded; file-level source identities are preserved.
- Separate PERSONAL Linux A4000 `scenario7` evaluation of the final checkpoint: COMPLETE/non-smoke, 3,072 time-window cohorts / 3,073 episode rows, no video, no comparison report or official score. Evaluated checkpoint SHA matches the training checkpoint index. [Evaluation Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261018-exp-h1-rough-terrain-orientation-relaxation-model9999-a4000-eval); ZIP 547,807 bytes, SHA `acaebad31aa5086137ed42817813662926d322b3f01543e9ad6f3b29264c842e`.
- Both imported-parent provenance and training source commit remain unverified/unrecorded. Completion/evaluation do not promote the policy; retain **HOLD** pending analysis. `TOP03` is a selection-rank alias, not an Experiment identity.

## 2026-10-10 direct RAW follow-up — 9,216 episodes and TERM-50 baseline now verified

[New raw three-policy report](../../../data/processed/experiments/h1/2026-10-10_H1_SCENARIO7_RAW_3POLICY_MATCHED_ANALYSIS.md). Received all three previously archived ZIPs, checked SHA and ZIP CRC, read 3,072 `episodes.jsonl` rows per policy, validated byte-identical `resolved_configs.json` and identical protocol/agent/source/environment fingerprints and 3,072 matched cohort IDs. The earlier report-only and baseline-unavailable statements are historical; TERM-50 case metrics are now directly available.

ORIENT model_2850 composite tracking **0.14041** versus TERM model_2800 **0.15712** (10.63% lower) and H5 rough progress **9.451m** versus **8.896m**. However its H1 unintended forward **1.633m** is worse than TERM **1.352m**, and its eight-case mean **roll/pitch RMS 0.08015** is substantially greater than TERM **0.03381** and ACTRATE **0.03019**. The same training-seed and selected-checkpoint-stage causal questions remain; same episode *keys* do not establish identical physical terrain realizations. **Candidate HOLD**, not an official score or a proven reward effect.

## 2026-10-10 post-training comparison status — metadata matched, policy HOLD

[Scenario7 cross-report comparison / original ZIP locations](../../../data/processed/experiments/h1/2026-10-10_H1_SCENARIO7_CROSS_POLICY_REPORT_LEVEL_COMPARISON.md): the original `h1-submit-2 / TERM-50` `model_2800` **PERSONAL evaluation ZIP actually exists on GitHub**, alongside this `ORIENT-100/model_2850` and `ACTRATE-0001/model_2700`. Publication manifests match task checkout `ef10b7a`, handoff `28895d7`, protocol `d406a296…7062d34`, 8 cases, 3 evaluation seeds, 128 env and 20-second duration. Earlier statements saying the control evaluation was not available described the evidence **then reviewed**, not current archival absence. GitHub connector could read manifests but not private binary ZIPs or 3,072 episode rows; full matched A/B against control remains **NOT RUN**.

Existing separate analysis reports put ORIENT tracking below ACTRATE in **5/8 cases** and action-change RMS below both ACTRATE and corrected PERSONAL LINTRACK in **8/8 cases**, but ORIENT still leaks **1.633 m** body forward on zero-command and **1.180 m** on lateral-only command. ACTRATE shows stronger H2/H6 tracking and rough P05 progress, at higher H1/H3 forward leakage. These are descriptive cross-report values, **not** evidence that relaxing `flat_orientation_l2` beats unchanged `TERM-50`, nor a formal adoption result. OFFICIAL fresh3K training and PERSONAL single-policy evaluation are separately complete; policy HOLD remains, with full-source/PPO/effective per-cohort parity and causal effect unverified.

## Received Run — 2026-10-06

OFFICIAL fresh 3000 iterations completed, exit 0, validation PASS, seed 42, 4096 envs, no parent. Actual reward weights confirm `h1-submit-2 + orientation=-1.0`, including feet 0.20 and termination -50. Save interval 50 preserved 60 checkpoints; auto best is `model_2850.pt`, latest preserved is `model_2950.pt`. Full config, both checkpoint hashes, source identity, canonical path and Release are in the [intake record](../../../data/processed/experiments/h1/2026-10-06_ORIENT100_OFFICIAL3K_EVIDENCE_INTAKE.md). The later PERSONAL single-policy analysis places the candidate on **HOLD**, without changing training completion or claiming a score/submission. The design below remains the comparison protocol, not proof of reward improvement.

## Linked PERSONAL Windows evaluation — model_2850, 2026-10-07 KST

This is post-training video/evaluation evidence, not another training Run, submission or OFFICIAL score. The source remains OFFICIAL Run `20261006-133517-h1-orient-100-fresh3k-official`; the checkpoint SHA matches its automatic-best `model_2850.pt`, not the latest keeper `model_2950.pt`.

- Native checkpoint SHA-256: `6aedeced60562c1d496d5319d29b76cf9e26ff43df06827cb370f24f5313f7b0`.
- Evaluation: PERSONAL Windows, COMPLETE, `complete=true`, `smoke=false`; camera-off H1 scenario7, 128 envs × seeds 4201/4202/4203 × eight cases × 20 simulated seconds.
- Evaluation protocol ID: `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34`.
- Six fixed-terrain videos include ±10° slopes; evaluation and video episodes are separate.
- Combined ZIP: `model_2850_ORIENT-100_h1_6terrain_evaluation_20261007-010444_f6b3b8b3.zip`, 33,323,164 bytes, 18 files, SHA-256 `aecc82b13671d54c96813af6c02c1b2a7769ee001b30aa4a5c2761457110eb7a`.
- Full evaluation ran 2026-10-06 15:28:55–16:01:10 UTC (2026-10-07 00:28:55–01:01:10 KST). Original internal `policy.source_run_id=null` is retained; external training linkage uses the matching checkpoint SHA.
- Publication scope: original combined ZIP, its checksum and external publication manifest only; no duplicated loose MP4s or generated A/B report.
- Canonical backup: `naver-issacsim-originals/data/raw/private_server_runs/h1/2026-10-07_windows_model2850_video_evaluation/` (Originals commit `a6370b1`).
- [PERSONAL video/evaluation Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261007-exp-h1-rough-terrain-orientation-relaxation-model2850-video-eval): three assets, remote sizes/digests verified; annotated tag targets evaluation task checkout `ef10b7a4c9a83481346d446e8a75aed655f72214`, not the official training source. Evaluator handoff commit is `28895d75edf3095607e392a07207a62e768478c7`.

## OFFICIAL baseline control Run — 2026-10-08

The fresh `h1-submit-2 / TERM-50` baseline control completed as a separate OFFICIAL training Run. It has no checkpoint parent and matches the nine listed reward weights in the frozen preset. Its automatic-best model_2800 now has separate PERSONAL Windows video/full evaluation evidence below. Source/PPO parity and a paired causal result are not established.

- Run ID: `20261008-062732-h1-term-50-fresh3k-control`; OFFICIAL, fresh, COMPLETE/PASS, exit 0; requested 3,000 iterations, console endpoint `2999/3000`.
- Start/end: `2026-10-08T06:27:32.704453Z` / `2026-10-08T07:04:30.219668Z`.
- Native run: `/workspace/training/humanoid/logs/rsl_rl/humanoid/2026-10-08_15-27-38`; seed 42, 4,096 environments; no parent checkpoint.
- Baseline preset: `h1-submit-2`; final override: none. Confirmed weights: `track_lin_vel_xy_exp=0.5`, `track_ang_vel_z_exp=0.5`, `feet_air_time=0.2`, `termination_penalty=-50.0`, `flat_orientation_l2=-1.5`, `ang_vel_xy_l2=-0.05`, `joint_deviation_hip=-0.2`, `joint_deviation_torso=-0.1`, `action_rate_l2=-0.0005`.
- Checkpoint interval 50; 60 keeper checkpoints. Automatic best `model_2800.pt`, SHA-256 `dffaa77848741fed1f4d22d0b78d4d8911af49057541107845e4d1df02c09ad6`; latest keeper `model_2950.pt`, SHA-256 `a568e8df7df74c0ed2f8c1929d106d3fbd9a6307700dfff35de9126a34266c3c`.
- Canonical archive: `naver-issacsim-originals/data/raw/official_server_runs/h1/2026-10-08_152738_term50_fresh3k_control/`. Original archive: `20261008-062732-h1-term-50-fresh3k-control-download.tar.gz`, 418,943,382 bytes, SHA-256 `594f5fdf83b702b2d6e5e664b35a3d1e1d2b7f9a42c8891dd1faddc1bfea8c1c`. Source/config evidence includes `source/identity.json`, `source/humanoid_rewards.py`, and `native_run/params/env.yaml` / `agent.yaml`.
- Published raw-evidence Release: [official-h1-20261008-h1-submit-2-fresh3k-control](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261008-h1-submit-2-fresh3k-control); three assets (original archive, checksum, preservation note), remote sizes/digests verified. Originals commit `d828a02`; annotated tag points to the preservation commit, not an official training source commit.
- No video, evaluation, analysis or submission was received inside this training archive. The subsequent model_2800 PERSONAL evaluation is recorded below. The Experiment remains **HOLD** pending comparison; no source/PPO parity or reward-causality conclusion is asserted.

## Linked PERSONAL Windows control evaluation — model_2800, 2026-10-08 KST

- Source OFFICIAL training Run: `20261008-062732-h1-term-50-fresh3k-control`; preset-relative reward override: none (`h1-submit-2 / TERM-50`). This record is not another training Run or submission.
- Selected automatic-best checkpoint: `model_2800.pt`, SHA `dffaa77848741fed1f4d22d0b78d4d8911af49057541107845e4d1df02c09ad6`, matching the official checkpoint index; not latest keeper model_2950.
- PERSONAL Windows full camera-off H1 scenario7: COMPLETE, native exit 0, complete=true, smoke=false, 128 envs × seeds 4201/4202/4203 ×8 cases ×20 seconds; 3072 aggregate episodes. Six separate maneuver_push videos include ±10° slopes, 1000 frames /20 seconds each.
- Protocol ID `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34` matches the recorded ORIENT-100 evaluation protocol; no A/B report or reward superiority is inferred from that match.
- Original ZIP: `model_2800_h1_6terrain_evaluation_20261008-171331_a8ab9d61.zip`, 34,012,853 bytes, 18 members, CRC checked, SHA `d4a47b0e182763e21077b688f44f7d9cdc00759c0f0f78f4217930e1c49975da`.
- Canonical preserved ZIP/checksum/publication manifest: `naver-issacsim-originals/data/raw/private_server_runs/h1/2026-10-08_windows_model2800_video_evaluation/`, Originals commit `c25221f`.
- [PERSONAL video/evaluation Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261008-exp-h1-rough-terrain-orientation-relaxation-model2800-control-video-eval): three assets; task checkout / annotated target `ef10b7a4c9a83481346d446e8a75aed655f72214`; evaluator handoff `28895d75edf3095607e392a07207a62e768478c7`.
- Original internal preset/source_run_id null values are preserved; external lineage uses checkpoint SHA. This is PERSONAL post-training evidence, not an OFFICIAL score. No new analysis, adoption decision, paired evaluation or submission is claimed.

## Received policy analysis — 2026-10-07

[Original report](../../../data/processed/incoming/other/reviewed/H1_ORIENT-100_POLICY_ANALYSIS_20261007.md) is preserved byte-for-byte (SHA-256 `024b3300a50890424e976b9669127a933521aff8cef903e2a11628acd6669b3b`). **Decision: HOLD**, retain for matched comparison; not REJECT or PROMOTE.

- The report reaggregates 3,072 initial-cohort episodes: all reach 20-second timeout, with zero termination/base-contact failures. Forward and push conditions show actual progress; survival alone is not the adoption criterion.
- Balance commands still produce mean body-forward integration +1.633 m/20 s; lateral commands +1.180 m. Rough-terrain tracking mean is 0.1709, with P05 progress 8.863 m and P95 tracking 0.1948; these are PERSONAL diagnostics, not official scores or physical-unit-equivalent totals.
- Video observations support early boxes/rough progress but do not establish central multi-step stair completion. The report identifies alternating black/valid frames in `02_inverted_stairs.mp4`; preserve the original and treat this as capture quality, not policy failure. No new frame inspection is claimed by this intake.
- At the time of the original 2026-10-07 ORIENT-only report, no matched `h1-submit-2 / TERM-50` evaluation was supplied. **The 2026-10-10 follow-up has since directly compared all 9,216 archived rows**, but training-replication, identical physical initial terrain and reward causality remain unverified. Reward causality, baseline superiority and submission adoption remain unestablished. The report's ZIP-only missing-training-lineage caveat is resolved externally by the official intake and publication manifest, not by rewriting the report.
- Next information priority: use an already available matched baseline evaluation if one exists; otherwise decide separately whether to authorize GPU comparison. This report/intake starts no new training, rendering, evaluation or export.

## Experiment question

Does relaxing the H1 flat-orientation penalty from `-1.5` to `-1.0`, while keeping the rest of the Round-2 TERM-50 configuration unchanged, improve rough-terrain adaptation without sacrificing balance, tracking, or survival?

This is a new Experiment question, not a new `H-xxx` legacy ID. Do not issue a Run ID until an actual training execution exists.

## Why this is the next H1 test

The Round-4 `h1-submit-4` AIRTIME-025 evaluation recorded simulation 56.37/70, design-intent analysis 20/20 and report quality 10/10; those components sum to 86.37/100, numerically equal to the Round-2 total, but the received Round-4 text did not expose a separate total field. The scenario mix changed, and weak-rough-terrain score decreased from 8.17/10.5 to 8.00/10.5 while forward, slope and push scenarios improved slightly. Because Round-2 was fresh 5K and Round-4 was fresh 10K, this does not isolate the causal effect of AIRTIME-025. It does make another airtime escalation lower-information than testing a distinct single-dial question.

The orientation test asks a different question: whether the current `flat_orientation_l2=-1.5` over-constrains torso pitch/roll adaptation on irregular ground.

External successful H1 work is only a prior, not a directly transferable optimum:

- IIT Delhi CoE-BIRD's 2026 Unitree H1 uneven-terrain/staircase project reports an orientation penalty of `-1.0` together with linear tracking `+1.0`, angular tracking `+0.5`, action-rate `-0.01`, gait-phase rewards and curriculum.
  - https://github.com/iitd-bird-robotics/2026-major-Bipedal_Locomotion_Using_RL
- A separate public Isaac Lab H1 rough-terrain run reports `flat_orientation_l2=-1.0`, `action_rate_l2=-0.005`, 4,000 iterations, terrain level 5.76/8, velocity error 0.24 m/s and 0.74% fall rate.
  - https://github.com/egeozgul/humanoid-locomotion-isaaclab

These environments, reward functions and metrics are not the NCRC evaluator. The shared `-1.0` value is therefore a testable prior, not evidence that `-1.0` is optimal for this competition.

## Effective configuration

Start from the full frozen `h1-submit-2` resolved configuration and change only:

```text
flat_orientation_l2: -1.5 -> -1.0
```

In particular:

- `termination_penalty=-50`
- `feet_air_time=0.20`
- `track_lin_vel_xy_exp=0.5`
- `track_ang_vel_z_exp=0.5`
- `ang_vel_xy_l2=-0.05`
- `action_rate_l2=-0.0005`

Do **not** inherit AIRTIME-025 from `h1-submit-4`; otherwise the orientation effect is confounded.

Before execution, verify the current official `/workspace/training/humanoid` source and resolved reward file. The final evidence, not this plan, determines the actual effective configuration.

## Planned execution

- OFFICIAL server
- fresh 0→3K
- seed 42
- 4,096 environments
- same native PPO/task/source as the verified official H1 environment unless the current server source has changed
- no checkpoint parent
- preserve console, TensorBoard, checkpoints, resolved `env.yaml`/`agent.yaml`, source fingerprint, report/export and evidence archive according to the current `issacsimz` official procedure

This plan authorizes no server start or training by itself.

## Comparison before H1 GPU evaluator validation

At the 2026-10-04 planning stage the PERSONAL evaluator core and Windows H1 launcher were implemented but not H1 GPU-verified. The linked 2026-10-07 PERSONAL six-video/full evaluation above now provides actual single-policy H1 GPU evidence. No matched paired evaluation or official score is established; training logs and source/protocol parity remain necessary for historical comparisons.

For this 3K Run:

1. If source/PPO/seed/schema parity is confirmed, compare the `ORIENT-100` run's 0→3K training curve against the corresponding first 3K segment of the official `h1-submit-2` fresh 5K run.
2. Compare late windows for terrain level, XY tracking error, yaw error, base-contact termination, timeout/episode length, action std and available posture/action reward terms.
3. Produce native terrain videos only as qualitative evidence. Keep command/terrain-instance mismatch explicit; do not convert video impressions into a score.
4. Official NCRC score improvement can only be established by an actual competition evaluation after a later submission.

## Promotion / stop signals

Promising direction:
- rough-terrain progression improves or is maintained,
- XY/yaw tracking does not jointly degrade,
- base-contact/fall proxy and episode length do not jointly degrade,
- videos do not show new stall, foot-dragging, excessive torso oscillation or loss of balance.

Negative direction:
- easier upright posture is bought with clear tracking loss, repeated torso oscillation, contact/fall increase, or terrain regression,
- only mean reward rises while behavior-facing metrics worsen.

A 3K training result is a screening/comparison result, not proof of an official score gain.

## Planned follow-up: action smoothing

A separate follow-up Experiment is now **PLANNED** as [`exp-h1-action-rate-smoothing / ACTRATE-001`](exp-h1-action-rate-smoothing.md):

```text
action_rate_l2: -0.0005 -> -0.001
```

`ACTRATE-001` remains a separate single-delta question and must not be combined with `ORIENT-100` in the same first Run. Its planned ordering after review of the `ORIENT-100` evidence does not make `ORIENT-100` a checkpoint parent. No `ACTRATE-001` Run ID is issued until an actual training execution exists.

## Decision after evidence

Update the registry only after receiving the actual Run evidence. Record the evidence Run ID, exact resolved config, completion status, final numbered checkpoint, and whether the result supports extending, holding, or rejecting this Experiment.
