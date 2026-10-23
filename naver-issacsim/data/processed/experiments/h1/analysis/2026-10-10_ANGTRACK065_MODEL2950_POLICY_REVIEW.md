# [분석] H1 ANGTRACK-065 / model_2950 — 2026-10-10 PERSONAL policy analysis intake and HOLD decision

> 관리 안내 (2026-10-13): **분석** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](../../../../../research/EXPERIMENTS.md)를 확인한다.

## Provenance and decision

- **Decision: HOLD**, especially **not** an all-direction or lateral-control representative. Useful forward, turning, slopes, push and short obstacle-patch continuation do not overcome **15 H3 lateral-command base-contact failures** and high stall.
- **Unmodified original user report:** [H1_ANGTRACK-065_POLICY_ANALYSIS_20261010.md](../../../incoming/other/reviewed/H1_ANGTRACK-065_POLICY_ANALYSIS_20261010.md). The report states that its author directly examined the complete evaluation ZIP, `episodes.jsonl` and all 6 videos. **This GitHub document intake read only the supplied Markdown report and pre-existing GitHub records; it did not independently download/redecode the ZIP, rerun evaluation or verify training checkpoint bytes.**
- **OFFICIAL training (independent evidence):** `exp-h1-angular-tracking-boost / ANGTRACK-065`, fresh3K Run `20261009-155344-h1-angtrack-065-fresh3k`, seed 42, 4096 env, no parent, native exit 0 and evidence PASS; only `track_ang_vel_z_exp 0.5 → 0.65` against frozen `h1-submit-2`. Official auto-best and latest keeper both `model_2950.pt` checkpoint SHA-256 **`6a6f456eb3f25a7d2764af576e30b1a8169674256ae5c2ba0a1b79ed368e118c`**. [OFFICIAL training intake](../2026-10-10_ANGTRACK065_OFFICIAL3K_EVIDENCE_INTAKE.md).
- **PERSONAL Windows post-training evaluation:** same checkpoint SHA is reported across source/video/evaluation metadata, although embedded `policy.source_run_id`/`preset` are null; linkage is based on separately preserved OFFICIAL intake and Windows publication, not invented embedded lineage. Full `scenario7`, 7 scenarios/8 cases, 3 evaluation seeds (4201–4203), 128 environments, 20s, protocol `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34`; six distinct `maneuver_push` videos. [Windows publication](../../../operations/windows_h1_video_evaluation/2026-10-10_ANGTRACK065_MODEL2950_PUBLICATION.md), [preserved PERSONAL Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261010-exp-h1-angular-tracking-boost-model2950-video-eval).
- ZIP name `model_best_h1_6terrain_evaluation_20261010-041416_066bf8a3.zip`, 32,626,954 bytes, 18 entries, archived ZIP SHA-256 `ec1bc325feae5cd6da1643a9fbbe13b0640ad7514b77b79e5532d8b836def93b` (from existing GitHub publication, not independently rehashed here).

## Episode denominator: 3,072 initial cohorts, but 3,087 rows

**This is critical**: H3 lateral command generated **15 first-episode base-contact terminations** among **384 initial H3 cohorts** (3.91%; seed 4201=6, 4202=4, 4203=5). Each terminated cohort restarted once, generating 15 short `evaluation_end` rows. Thus **8 cases ×384 initial cohorts = 3,072 initial cohorts but 3,087 distinct raw episode rows**. The H3 original 20-second timeout count is **369/384 = 96.09%**. If counting all H3 episode rows, there are **384/399 = 96.24% survived**, but this includes 15 restarted short segments: **not** 384 successful 20-second initial trials. Reported 15 termination times: 6.92–11.50s; 15/15 had `base_contact_failure=true`.

By contrast the previously analyzed `TERM-50 model_2800`, `ORIENT-100 model_2850`, `ACTRATE-0001 model_2700` each recorded 3,072 raw rows and 3,072/3,072 complete 20-second timeout survivors. **ANGTRACK's H3 episode-row mean/row denominator and restart policy prevent blindly joining all 3,087 rows with those 3,072-row datasets**. Proper matched comparison requires initial-cohort (n0) status, explicit failure handling and censoring/window alignment.

## Reported scenario behavior (single policy; not A/B)

| Case | Reported tracking | Body-frame forward integral | Failure or behavioral limit |
| --- | ---: | ---: | --- |
| H1 zero | 0.0552 | **+0.875m unintended** | World net magnitude median 0.899m; computed stall=0 has no valid commanded-speed denominator |
| H2 forward | 0.1068 | 14.703m / 15m command | 384/384 timed out normally |
| **H3 lateral** | **0.2203** (399 episode-row mean) | +0.416m; not lateral distance | **15/384 initial cohorts terminated**, 35.32% row-mean stall, mean vy error 0.1871m/s, completed-20s world net magnitude median 0.917m |
| H4 turn+forward | 0.1095 | 9.889m / 10m command | yaw absolute error 0.0770rad/s; world net 2.661m is not automatic stall |
| H5 rough | 0.1644 | mean 8.895m / 10m | P05 8.399m; min 7.725m; P95 tracking 0.1816, max 0.2582, no H5 contact terminations |
| H6 slope up 10° | 0.1409 | 19.571m / 20m | action Δ RMS 0.5202; no termination |
| H6 slope down 10° | 0.1426 | 19.235m / 20m | action Δ RMS 0.5134; no termination |
| H7 push | 0.1067 | 9.996m / 10m | 384/384 timeout, but instantaneous recovery time unmeasured |

Full episode-row tracking mean **0.1312** over 3,087 rows; 8-case equal-weight mean **0.1308**; these are *not interchangeable* nor official scores. H3 terminated rows are shorter than 20 seconds and 15 follow-up rows represent restarts; unqualified single-number comparisons to no-restart policies are unreliable. H3 tracked only poorly in lateral XY despite sometimes good yaw metrics. **Do not infer increased yaw reward improved yaw** without the matched unchanged `TERM-50` baseline.

## Video limitations and follow-up

The source report describes decoding all six 1,000-frame 50fps MP4s and checking their SHA against their ZIP manifest. Video commands contain combined forward+lateral turns, **not pure H3 `vx=0,vy=±0.3`**. Video boxes and rough patch progression are positive *qualitative* evidence, not a dedicated full-duration obstacle-traversal result; multi-step central stairs/inverted-stairs completion is not proven, and `scenario7` has no stairs/boxes case. **`06_slope_down_10deg.mp4` has black EVEN 500/1000 frames, VISIBLE odd 500/1000 frames** per this report. Capture artifact is not a policy fall; do not conflate with the different MP4 defects seen for other H1 policies.

**Next comparator without GPU:** existing unchanged OFFICIAL fresh3K `h1-submit-2/TERM-50 model_2800` full PERSONAL `scenario7` ZIP is already archived and previously read; contrast with ANGTRACK original `model_2950` ZIP *only after checking* raw evaluation commands/terrain/environment fingerprints, first-cohort keys, and H3 terminated/restarted rows. Questions: H3 initial-cohort fall/actual timeout/stall/vy/yaw/posture, H1 zero displacement, H4 yaw, H2/H5/H6/H7 progress and worst tails. Existing three-policy [raw benchmark](../2026-10-10_H1_SCENARIO7_RAW_3POLICY_MATCHED_ANALYSIS.md) is context and did **not** include ANGTRACK. This report **does not perform** the ANGTRACK-vs-control matched raw comparison, a new training/evaluation/video/export, official score calculation or Optuna trial.

**Status:** OFFICIAL training COMPLETE/PASS; PERSONAL full evaluation COMPLETE; **single-policy behavioral analysis RECEIVED and HOLD**; controlled baseline comparison and all-terrain promotion **pending**.
