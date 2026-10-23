# exp-h1-action-rate-relaxation

## 2026-10-15 같은 부모 CPU 비교 — unchanged4699 대표 후보 REJECT

[CPU 비교 원문·CSV·판정](../../../data/processed/experiments/h1/analysis/2026-10-15_ACTRATE_PARENT_UNCHANGED_RESTORATION_COMPARISON_INTAKE.md). Run `20261014-111135-h1-actrate-0001-unchanged-cont2k`, model4699 SHA `722b35a1…48f646`: 부모2700 대비 H5 진행384/384건 감소·평균9.948→7.919m로 **현재 세 후보의 범용·전진/험지 대표에서 REJECT**. 별도 정지/yaw 참고군·원본·학습 COMPLETED/PASS는 유지한다. 부모2700은 rough 기준이지만 불필요한 이동 때문에 HOLD, 복원4650(`a8249db4…`)도 worst-tail 때문에 HOLD, PROMOTE 없음. 외부 원자료 비교 보고서/CSV를 대조한 수납이며 reward 인과·공식 점수는 미확정이다. 이하 단독 HOLD·비교 대기는 이전 시점 기록으로 읽고 imported-parent provenance는 보존한다.

## 2026-10-15 PERSONAL 사후 평가 완료

OFFICIAL Run `20261014-111135-h1-actrate-0001-unchanged-cont2k`의 `model_4699.pt`(SHA `722b35a127f7ae4209d94a9111ac5ee02071ba7f3b985dc9cdc0760bbe48f646`)로 Windows 6영상 + full H1 scenario7 평가가 완료됐다. [평가 Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261015-exp-h1-action-rate-relaxation-model4699-video-eval). 원본 평가의 source_run_id는 null이며 외부 checkpoint SHA/index로 학습에 연결한다. 학습 imported-parent provenance는 변경하지 않는다. 신규 학습/공식 점수/A/B 비교가 아니며 HOLD / 분석 대기. 아래 평가 대기는 과거 수납 시점 상태다.

## 2026-10-14 OFFICIAL unchanged-reward continuation control +2K

- Actual Run `20261014-111135-h1-actrate-0001-unchanged-cont2k`: H1 / OFFICIAL / train / resume; seed 42, 4096 envs, requested +2,000 iterations from 2700, final 4699/4700; exit 0, COMPLETED/PASS, finalization and official backup succeeded.
- Archived effective rewards match the ACTRATE-0001 fresh3K parent config: lin=0.5, ang=0.5, feet=0.2, termination=-50, orientation=-1.5, angxy=-0.05, hip=-0.2, torso=-0.1, action=-0.0001. This is an unchanged-reward continuation control; it is distinct from the `lin=0.65` child.
- Parent checkpoint SHA `e54d3389e20ea913968ef8d3edbea5004368ff225fa6b94f73fcd91cf93ca7ae` matches the preserved OFFICIAL ACTRATE-0001 fresh3K `model_2700.pt`. The new Run's raw metadata still has `source_checkpoint_origin=user_imported_checkpoint`, `source_evidence_run_id=null`, `parent_run_id=null`, `source_run_mode=unknown`, and `source_provenance_verified=false`; this cross-evidence SHA match does not rewrite the original provenance fields.
- [Canonical raw archive and preservation record](https://github.com/SE3C/naver-issacsim-originals/blob/main/data/raw/official_server_runs/h1/2026-10-14_201142_actrate0001_unchanged_cont2k/README.md) · [OFFICIAL Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261014-exp-h1-action-rate-relaxation-unchanged-cont2k). No policy evaluation, submission, or score is recorded; behavior assessment/adoption remains pending/HOLD.

## 2026-10-11 actual H1 Round-6 submission — h1-submit-6 / ACTRATE-0001

The user confirmed actual submission completion. [Immutable submission manifest](../../../data/processed/experiments/h1/2026-10-11_PRELIM_R6_SUBMISSION/submission_manifest.json) · [submission Release](https://github.com/SE3C/naver-issacsim/releases/tag/submission-h1-prelim-r6-20261011) · [full frozen native env/agent preset](../../submission_presets/h1-submit-6/). Exact portal time/receipt and official score remain unknown.

Selected policy source is final keeper model_9999, SHA `a5020c273bc2b69bea1b20782fe80ba6605b3036b4054a7e5a8ab66151d2cb74`, from completed OFFICIAL fresh10K Run `20261011-041745-h1-actrate-0001-fresh10k-official` (seed42/4096env/no parent, requested10000/final iter9999, exit0/PASS). CPU verification confirms all eight exported actor tensors exactly match that checkpoint. Received policy SHA `d304f5d51726cd48e0fda377cb4db2b72a93c65cc38344a85d6feae68d63365a`; env SHA `91f07d0be9d705cba9bade6c1ff3f9117286c9d7c04af7d9a6ea05df964cedc7` equals the official native configuration. A separate play/export evidence Run ID was not provided; do not invent it. The native checkpoint already remains in the training archive rather than becoming a portal policy asset.

Relative to submitted h1-submit-4, feet changes0.25→0.20 and action changes-0.0005→-0.0001. The training reference remains h1-submit-2 + action=-0.0001; fresh and resume histories below are not renamed. User submission does not retroactively change the independent PERSONAL analysis HOLD into PROMOTE, and model_9900 auto-best is not the selected policy. Earlier no-submission statements describe their historical intake/evaluation state.

## PERSONAL Windows follow-up — fresh10K model_9999 (2026-10-11)

The completed OFFICIAL fresh10K Run below now has a separate six-video/full H1 scenario7 evaluation for keeper `model_9999.pt` SHA `a5020c273bc2b69bea1b20782fe80ba6605b3036b4054a7e5a8ab66151d2cb74`, verified against its official checkpoint index. 128 env × three seeds × eight cases, 3,072 episode rows, COMPLETE/non-smoke. [Publication and Release](../../../data/processed/operations/windows_h1_video_evaluation/2026-10-11_ACTRATE0001_FRESH10K_MODEL9999_PUBLICATION.md). Source-run/preset nulls in the ZIP are preserved; external manifest records lineage. **User analysis received; report decision HOLD**: [raw report and policy review](../../../data/processed/experiments/h1/2026-10-11_ACTRATE0001_MODEL9999_POLICY_REVIEW.md). H1/H3 world residual 0.287/0.395m, H2 forward14.885m and H7 push9.974m are useful; rough mean/P05/min8.915/8.251/6.492m and central multi-step stairs proof remain weaknesses. This is not an official score, actual submission or completed paired comparison, and does not assign historical fresh3K/model_2700 results to this checkpoint.

## Completed training Run — 2026-10-11 OFFICIAL fresh 10K

- Separate Run `20261011-041745-h1-actrate-0001-fresh10k-official`: OFFICIAL fresh, no parent/resume; 10,000 requested iterations, seed 42, 4096 envs; metadata completed, exit 0, validation PASS and native finalize/backup complete.
- Display `h1-submit-2 + action=-0.0001`; nine intended report weights confirmed, full resolved native config/reward/source retained in the archive. Same display does not by itself establish full source/PPO parity with the previous fresh3K.
- 201 keeper checkpoints retained, 202 checkpoint-index entries including native. Automatic best `model_best.pt` matches `model_9900.pt`, SHA `6dd795e32383bc21ac487ea039bb2a03a565ec2ee6da893a3dc4ffaa844c769d`; report reward peak at step 9880 is a different value.
- [Intake and canonical evidence](../../../data/processed/experiments/h1/2026-10-11_ACTRATE0001_OFFICIAL10K_EVIDENCE_INTAKE.md) · [OFFICIAL Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261011-exp-h1-action-rate-relaxation-fresh10k). Received wrapper 1,358,051,174 bytes, SHA `6977db0f4cea94d7685023a4b58702290f762e2c075525bc977173a2d54ebdb7`.
- **Training complete; later model_9999 evaluation and user analysis received/HOLD**, linked above. No actual submission or official score is implied. Historical model_2700 PERSONAL results below belong to the separate fresh3K Run.

## 2026-10-10 five planned ACTRATE-0001 offspring/combinations — no child run yet

[Selected five-hypothesis plan](../../../data/processed/planning/2026-10-10_H1_ACTRATE0001_FIVE_COMBINATION_HYPOTHESES.md) registers two independent fresh combined-reward hypotheses and three **independent one-step children** of existing completed OFFICIAL ACTRATE-0001 3K training. Fresh: [`feet=0.25 + action=-0.0001`](planned/exp-h1-action-airtime-fresh-interaction.md), [`action=-0.0001 + feet_slide=-0.35`](planned/exp-h1-action-foot-contact-stability.md). Resume each +2K from the **same verified parent checkpoint**, changing exactly one field: [`feet=0.25 + action=-0.0001`](planned/exp-h1-action-first-airtime-switch.md), [`lin=0.65 + action=-0.0001`](exp-h1-action-first-planar-tracking-switch.md), [`angxy=-0.08 + action=-0.0001`](planned/exp-h1-action-first-body-rate-switch.md).

**Do not rewrite the parent's completed status or award child Run IDs.** Evaluated best `model_2700` (SHA `e54d3389…ca7ae`) and latest keeper `model_2950` (SHA `d4fa7221…b70`) are separate. Check actual OFFICIAL index/source_path and full parent SHA, then allow multiple sibling Resume Runs but **no second 5K→7K resume step in a branch**. Preferred attribution control is same-parent unchanged +2K; Fresh 3K vs resumed approximately 5K is not a matched training-schedule causal contrast. `ACTRATE-001` remains separately planned until its own evidence. No user-authorized GPU work or official submission is inferred.


- Robot: H1
- Display descriptor: `ACTRATE-0001` = `action_rate_l2=-0.0001`
- Status: **OFFICIAL train COMPLETED/PASS; PERSONAL model_2700 full evaluation COMPLETE, single-policy behavioral analysis received; policy HOLD pending matched control comparison** (2026-10-10)
- Baseline: frozen `h1-submit-2 / TERM-50`
- Final override: `h1-submit-2 + action=-0.0001`
- Single delta: `action_rate_l2 -0.0005 → -0.0001`
- Actual Run: OFFICIAL **fresh 3K**, seed 42, 4096 envs, no parent checkpoint; requested/completed 3,000 iterations.

## 2026-10-10 direct RAW follow-up — 9,216 episodes and baseline comparison completed

[New raw three-policy analysis](../../../data/processed/experiments/h1/2026-10-10_H1_SCENARIO7_RAW_3POLICY_MATCHED_ANALYSIS.md). Three original ZIPs now directly read (SHA/CRC PASS; 3×3,072 episode rows; matched all 3,072 cohort keys; binary-identical resolved evaluator config and equal agent/source/applied environment fingerprints). Earlier report-only/binary-inaccessible status is superseded. This evaluation is post-training PERSONAL and not a new Run.

ACTRATE model_2700 composite tracking **0.14534** versus frozen TERM model_2800 **0.15712** (7.50% lower); H5 rough mean progress **9.948m vs 8.896m**, P05 **9.592m vs 8.533m**, 384/384 matched-index cohorts with greater rough forward progress. But H1 zero-command unintended forward **1.987m vs 1.352m**, H3 lateral-only forward **1.677m vs 1.205m**, all-case action-change RMS **0.45687 vs 0.36529**. Rough yaw error **0.1343** exceeds ORIENT **0.1190**, so it is not uniformly better tracking. Same eval protocol/indices do not imply identical physical rollouts or multiple independent training-seed replications; selected auto-best checkpoints are also different steps. **All-terrain policy HOLD**, no isolated reward-causality or official score claim.

## 2026-10-10 post-training 3-policy report comparison (policy HOLD)

[Direct GitHub archive locations, matching publication-level evaluator metadata, raw-access limitation and 8-case report table](../../../data/processed/experiments/h1/2026-10-10_H1_SCENARIO7_CROSS_POLICY_REPORT_LEVEL_COMPARISON.md): the independent `TERM-50/model_2800` control, `ORIENT-100/model_2850` and this `ACTRATE-0001/model_2700` each have complete PERSONAL `scenario7` ZIP evidence (8 cases ×3 evaluation seeds×128 env×20 s), with same recorded task/handoff/protocol. Existing source documents were reviewed, but **this comparison did not extract private binary ZIP contents or run a matched raw cohort analysis**.

ACTRATE has stronger H2/H6 tracking and rough H5 body progress/P05 (`9.948/9.592m`) than ORIENT (`9.451/8.863m`), but worse zero H1 forward leakage (`1.987m` vs `1.633m`), lateral H3 leakage (`1.677m` vs `1.180m`), H6 action-change RMS down (`0.540` vs `0.464`) and H5 maximum tracking error (`0.2908` vs `0.2412`). ORIENT has lower tracking in 5/8 cases and lower action-change RMS in all 8. Neither candidate has verified `TERM-50` per-case baseline deltas; same protocol/seeds do not prove same individual terrain/reset or full training source/PPO parity. Thus **policy HOLD; reward `action_rate_l2=-0.0001` improvement not demonstrated**. No new Run, Optuna trial, export, GPU work or official score.

## Question

Does relaxing the H1 action-rate penalty increase command-change responsiveness and **combined x/y/yaw velocity tracking**, even if movement becomes less smooth and a modest survival cost appears? Count tracking gains together with real terrain progress/stall and repeated failure episodes, not tracking alone.

The existing [`ACTRATE-001 / exp-h1-action-rate-smoothing`](exp-h1-action-rate-smoothing.md) tests the **opposite direction**, strengthening the same penalty to `-0.001`. These are two separate Experiments/target fresh Runs; neither inherits the other's checkpoint or reward edits.

## Evidence and uncertainty

Go2 OFFICIAL R3→R5 stairs improved survival 99.0%→99.8% while tracking decreased 0.819→0.796 and stair score fell 8.52→8.35. This only suggests a survival/tracking trade-off question; it is **not H1 evidence** or a transferable scoring rule. H1 ORIENT-100 PERSONAL Windows evaluation had 3072/3072 20-second survivors but unwanted movement during balance and lateral commands. That evaluation identifies behavior weaknesses, not ACTRATE causality.

## Preset and single-delta protocol

Start from the verified **full native** frozen `h1-submit-2` source/config. Change only:

```text
action_rate_l2: -0.0005 -> -0.0001
```

Keep other checked baseline weights, including `termination_penalty=-50`, `feet_air_time=0.20`, `flat_orientation_l2=-1.5`, `track_lin_vel_xy_exp=0.5`, `track_ang_vel_z_exp=0.5`, `ang_vel_xy_l2=-0.05`, `joint_deviation_hip=-0.2`, `joint_deviation_torso=-0.1`. Confirm **all** other rewards/PPO/task/env against frozen resolved source, not only this shortlist. Revert any ACTRATE-001/ORIENT/LINTRACK edits left by previous Runs; do not stack them.

## Completed training Run — 2026-10-09

- Run ID: `20261009-142350-h1-actrate-0001-fresh3k`; OFFICIAL train/fresh, no parent or resume lineage. Native run `/workspace/training/humanoid/logs/rsl_rl/humanoid/2026-10-09_23-23-56`.
- Completed 3,000 requested iterations (console 2999/3000), seed 42, 4096 envs, save_interval=50; exit 0, validation PASS, native finalize completed and backup succeeded.
- Resolved config and provenance: original nested `native_run/params/env.yaml`, `agent.yaml`, `source/humanoid_rewards.py` and `source/identity.json`; checked nine weights match the intended `h1-submit-2 + action=-0.0001` display. Full source/PPO parity with the control remains unverified.
- Automatic best `model_2700.pt` SHA `e54d3389e20ea913968ef8d3edbea5004368ff225fa6b94f73fcd91cf93ca7ae`; latest keeper `model_2950.pt` SHA `d4fa722131d0559e02bbdf499cac87e6bba91372a1c9f9334b8cd4a7b7269b70`. 60 organizer checkpoints, TensorBoard, console/config/source records remain in the immutable archive.
- [OFFICIAL training Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261009-exp-h1-action-rate-relaxation-fresh3k) · [intake and canonical preservation](../../../data/processed/experiments/h1/2026-10-09_ACTRATE0001_OFFICIAL3K_EVIDENCE_INTAKE.md).
- Received wrapper: `20261009-142350-h1-actrate-0001-fresh3k-download.tar.gz`, SHA `38a6225ae59465fcb36496eef472b396b9095754587489d4b3091350f5a35b04`, 419,108,331 bytes. Downloads original unchanged.
- Decision at training intake (historical): HOLD until further evidence. A later PERSONAL model_2700 video/full scenario7 evaluation **and a separate single-policy behavioral analysis** are now received below; the current decision remains HOLD pending matched control comparison. No new submission preset or official score is claimed. Original source_provenance_verified=false is preserved, not rewritten as true.

## PERSONAL Windows follow-up — model_2700 (2026-10-10)

The official automatic-best checkpoint SHA `e54d3389e20ea913968ef8d3edbea5004368ff225fa6b94f73fcd91cf93ca7ae` now has six H1 videos and a separate full scenario7 evaluation (128 envs, seeds 4201–4203, 8 cases, 3,072 episodes; COMPLETE, smoke=false, native evaluation exit 0). This is not the latest keeper model_2950, an ANGTRACK policy or an official score. ZIP: `model_2700_h1_6terrain_evaluation_20261010-012639_61aa406d.zip`, 32,539,016 bytes / 18 files, SHA `6270d299def2a3bcb8cc10253027898621dd65a00ad30baafde0cbcde03076e3`.

[PERSONAL Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261010-exp-h1-action-rate-relaxation-model2700-video-eval) / [publication and canonical raw](../../../data/processed/operations/windows_h1_video_evaluation/2026-10-10_ACTRATE0001_MODEL2700_PUBLICATION.md). **Evaluation completion at publication was not a policy-quality decision.** The subsequently received single-policy analysis and HOLD decision are recorded below.

## 2026-10-10 PERSONAL model_2700 behavior analysis received — HOLD

- **Preserved original report:** [H1_MODEL2700_POLICY_ANALYSIS_20261010.md](../../../data/processed/incoming/other/reviewed/H1_MODEL2700_POLICY_ANALYSIS_20261010.md); [structured analysis/decision and next comparison](../../../data/processed/experiments/h1/2026-10-10_ACTRATE0001_MODEL2700_POLICY_REVIEW.md). User-supplied report analyzed the existing Windows ZIP's 3,072 `episodes.jsonl` records and six MP4; this GitHub intake did **not** independently rerun the evaluator or re-decode that ZIP. Evaluation policy SHA `e54d3389e20ea913968ef8d3edbea5004368ff225fa6b94f73fcd91cf93ca7ae` matches official auto-best `model_2700.pt`. ZIP-only training `source_run_id/preset=null` unchanged; the separate training record establishes lineage.
- **Useful movement:** PERSONAL 20s fixed `scenario7` 3,072/3,072 timeout survivors (0 base-contact failures); H2 commanded 15.0m / actual body forward **15.326m**, H7 push commanded 10.0m / **10.542m**, H6 10° up/down **20.052/19.834m**. The body-forward integral is not global displacement, obstacle completion or official score.
- **Major quality weaknesses:** H1 zero command nevertheless body forward **1.987m/20s** and world XY displacement **median 2.012m**; H3 lateral +0.3→-0.3 has unintended body forward **1.677m** (world net XY displacement **mean 0.669m**). H5 rough worst `seed4202/env108` has forward **8.815m**, tracking **0.2908** and roll/pitch RMS **0.0999** despite survival; H5 mean tracking 0.1781 and yaw absolute error 0.1343rad/s. H6 action Δ RMS up/down **0.534/0.540**; multi-step central stairs crossing unverified.
- **Video/evaluator distinction:** Six videos are differently commanded, pushed and tiled than camera-off `scenario7`. `01_stairs.mp4` reportedly has a black-frame capture defect (502/1000), not a falling policy. H1 stall_fraction=0 is an invalid denominator for zero XY command, not evidence of standing still. Integrated tracking mean 0.14534 is a mixed-units internal diagnostic, not NCRC score.
- **Current candidate HOLD:** forward-walking, push and brief rough/boxes movement are positive, while zero/lateral-command leakage and stairs proof are insufficient for all-terrain PROMOTE. This is **one PERSONAL checkpoint's behavior**, not confirmed `action_rate_l2=-0.0001` reward improvement. First re-use archived unchanged `h1-submit-2 / TERM-50` fixed `model_2800` comparison (prioritize baseline for reward question), optionally `ORIENT-100/model_2850` for behavior-choice comparison, checking source/protocol/case/seed/terrain/horizon parity before matching `episodes.jsonl` cohorts. No new GPU work is implied.

## Controls and outcome

1. **Primary:** previously completed OFFICIAL unchanged `h1-submit-2` fresh3K control `20261008-062732-h1-term-50-fresh3k-control` (seed 42, 4096 envs, no parent, COMPLETE/PASS), after checking native source/PPO/schema parity. Its `model_2800.pt` has separate PERSONAL Windows full evaluation; no completed A/B comparison is claimed.
2. **Directional sibling when executed:** compare `ACTRATE-001=-0.001` (still PLANNED), unchanged `-0.0005` (OFFICIAL control COMPLETE/PASS), and this completed `ACTRATE-0001=-0.0001` Run at the same training budget. ACTRATE-001 has no verified completed Run.
3. Compare late-window training XY/yaw errors, terrain progress, base-contact/episode length, action std/delta. If **separately authorized**, perform matched PERSONAL fixed evaluation of body-frame x/y/yaw error, command transition response, zero/lateral command drift, traversal/stall and falls with identical seed/command/terrain/horizon. Videos are qualitative if not matched.

PROMOTE only to later paired evaluation if tracking gains survive terrain/contact guardrails; HOLD without matched data; REJECT severe oscillation/fall/stall. Training completion is not a valid official score or proof of reward improvement. If run, retain source, resolved configs, checkpoint SHA, console/TensorBoard, exit status and validation. This plan itself executes nothing.
