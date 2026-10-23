# [분석] H1 ACTRATE-0001 / model_2700 — 2026-10-10 PERSONAL policy behavior intake

> 2026-10-15 후속: [부모2700·무변경4699·ACTION 복원4650 CPU 비교](2026-10-15_ACTRATE_PARENT_UNCHANGED_RESTORATION_COMPARISON_INTAKE.md) 수납 완료. 부모는 rough 기준으로 유지하되 정지/횡명령 누수 때문에 HOLD이며 PROMOTE는 없다. 이번 비교는 TERM-50 control2800과의 비교를 대신하지 않는다.


> 관리 안내 (2026-10-13): **분석** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](../../../../../research/EXPERIMENTS.md)를 확인한다.

## Evidence and decision

- **Decision: HOLD** for a general all-terrain H1 candidate. This checkpoint is a **useful forward-walking / short-rough / push continuation candidate**, not a verified zero-command/lateral/continuous-stair policy.
- **Primary source (preserved unchanged):** [H1_MODEL2700_POLICY_ANALYSIS_20261010.md](../../../incoming/other/reviewed/H1_MODEL2700_POLICY_ANALYSIS_20261010.md). This note **interprets the supplied report**; the original ZIP, episode rows and videos were **not directly reprocessed in this GitHub update**.
- **OFFICIAL training identity (separate established record):** `exp-h1-action-rate-relaxation / ACTRATE-0001`, Run `20261009-142350-h1-actrate-0001-fresh3k`, fresh 3K, seed 42, 4096 env, no parent, exit 0 / evidence PASS; reward display `h1-submit-2 + action=-0.0001`. Auto-best `model_2700.pt` SHA-256 `e54d3389e20ea913968ef8d3edbea5004368ff225fa6b94f73fcd91cf93ca7ae`; final numbered keeper **`model_2950.pt` is a different policy**. [Training record](../2026-10-09_ACTRATE0001_OFFICIAL3K_EVIDENCE_INTAKE.md).
- **PERSONAL evaluation evidence (not a new training Run):** Windows `scenario7` 7 scenarios / 8 cases, evaluation seeds 4201, 4202, 4203 ×128 environments = 3,072 episodes of 20 seconds, deterministic camera-off. ZIP `model_2700_h1_6terrain_evaluation_20261010-012639_61aa406d.zip` has 6 videos plus evaluation records. Policy SHA matches recorded OFFICIAL `model_2700` SHA via metadata, although ZIP `source_run_id` and `preset` are null and checkpoint bytes are not in the ZIP. [Existing Windows publication/Originals links](../../../operations/windows_h1_video_evaluation/2026-10-10_ACTRATE0001_MODEL2700_PUBLICATION.md).
- **Completion vs quality:** all 3,072 episodes ended in 20-second timeout, none in base-contact failure (**PERSONAL fixed evaluation completed**). This is distinct from OFFICIAL training COMPLETED/PASS, matched policy evaluation, reward effect, actual NCRC submission or score.

## Evidence presented in the user's analysis

| `scenario7` case | Reported observation | Interpretation |
| --- | --- | --- |
| H1 zero command | **1.987m** unintended body-forward integral / 20s; world XY displacement **median 2.012m** | Principal behavioral concern: zero-command forward leakage |
| H2 forward | **15.326m** body forward vs commanded integral 15m; tracking error **0.1188** | Useful forward gait and command following |
| H3 lateral command +0.3 then -0.3 | **1.677m** unintended body forward; world XY displacement magnitude **mean 0.669m** | Lateral task with forward leakage; world net displacement and body forward integral are different quantities |
| H5 rough | **9.948m** mean body-forward vs 10m target; tracking error **0.1781**; worst `seed 4202/env 108`: **8.815m**, tracking **0.2908**, roll/pitch RMS **0.0999** | Overall traversal persists, but tracking/yaw/posture worst-case tail remains |
| H6 slope up/down 10° | **20.052/19.834m** body forward; action Δ RMS **0.534/0.540** | Good movement, greater action/posture cost vs flat H2 |
| H7 push | **10.542m** body forward vs command 10m, 384/384 survived | Continued gait after disturbance, not a measured instantaneous recovery time |

The episode-weighted mixed-unit tracking mean is **0.14534**, not an NCRC score and not necessarily m/s. Reported `stall_fraction=0` for H1 zero command is an **undefined-denominator implementation result**, not proof of standing still. `forward_progress_m` and `integrated_body_forward_m` duplicate one measurement, not independent evidence. The six videos use a global maneuver/push schedule and **do not correspond to the same command, terrain or episode clock** as camera-off evaluation. Boxes/rough short-patch contact/progression is qualitative; central multi-step stairs/inverted-stairs traversal lacks direct proof and dedicated scenario7 cases. `01_stairs.mp4` reportedly includes 502/1,000 black frames, a **capture artifact rather than a fall**; do not conflate this with separate H1 video artifacts.

## Interpretation, provenance limits and next comparisons

1. The ZIP `evaluation/resolved_configs.json` is an **evaluation-time configuration**, not evidence of the training reward/parent/PPO. The Run↔policy connection comes from the separate training record and the repeated checkpoint SHA, not inferred from the policy name or the null metadata fields.
2. **Behavior candidate HOLD**: preserve forward-movement strengths and failures; do not PROMOTE to general all-terrain policy, REJECT as collapsed, infer that weaker action-rate reward caused a gain, create an Optuna result or claim an official score.
3. **First, no new GPU:** locate the already preserved unchanged `h1-submit-2 / TERM-50` `model_2800` PERSONAL `scenario7` evaluation and `ORIENT-100 / model_2850` evaluation. Check protocol `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34`, policy/source fingerprints, case-specific commands, terrain, start-state/seeds, horizon, agent and noise settings; compare cohort `(scenario,case,seed,env_id)` for H1 forward leakage, H3 lateral leakage, H5 tracking/progress tails, H6 posture/action and H7 survival/progress. The unchanged control is the **priority for reward-effect comparisons**; ORIENT-100 is an **additional behavioral candidate comparator**, not a matched single-delta cause test. Without parity or raw data, compare only supported axes and keep HOLD.
4. No training, GPU evaluation, new video, export, official submission, source modification or original ZIP replacement was requested or performed during this document intake.
