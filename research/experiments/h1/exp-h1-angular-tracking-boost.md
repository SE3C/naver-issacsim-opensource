> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/research/experiments/h1/exp-h1-angular-tracking-boost.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# exp-h1-angular-tracking-boost

- Robot: H1
- Display descriptor: `ANGTRACK-065` = `track_ang_vel_z_exp=0.65`
- Status: **OFFICIAL fresh 3K COMPLETED/PASS; PERSONAL six-video/full evaluation COMPLETE; behavior analysis RECEIVED; policy HOLD, control comparison PENDING** (received 2026-10-10)
- Baseline: frozen `h1-submit-2 / TERM-50`
- Final override: `h1-submit-2 + ang=0.65`
- Single delta: `track_ang_vel_z_exp 0.5 → 0.65`
- Actual: OFFICIAL **fresh 3K**, seed 42, 4096 envs, no parent checkpoint; Run `20261009-155344-h1-angtrack-065-fresh3k`, console 2999/3000, exit 0/PASS.

## Question

Does a stronger angular-rate tracking reward improve yaw and overall x/y/yaw command following, including zero/turn/lateral commands, without unacceptable XY, terrain traversal and base-contact losses? Modest survival sacrifice may be acceptable only where the tracking benefit outweighs it.

## Previous work: do not call it new evidence

Legacy [`H-002 / ANGTRACK-075`](<H-002.md>) ran a **PERSONAL BASE fresh 1K** with yaw reward `0.5→0.75`: terrain `0`, base-contact `100%`, timeout `0%`. Its low reported yaw error arose in a non-locomoting policy, so the original candidate was REJECT. This is a high-risk warning but **not** a matched test of `0.65` under `TERM-50`.

Corrected PERSONAL [`LINTRACK-075`](<H-008.md>) (`lin 0.5→0.75`) improved late training XY error but worsened yaw/contact/terrain. Its checkpoint is **not** a parent; the new question changes only angular tracking. The Go2 official tracking/survival trade-off is context, not proof of the H1 direction.

## Preset and single-delta protocol

Start from the verified full frozen `h1-submit-2` native reward/task/PPO config. Change only:

```text
track_ang_vel_z_exp: 0.5 -> 0.65
```

Keep `track_lin_vel_xy_exp=0.5`, `action_rate_l2=-0.0005`, `flat_orientation_l2=-1.5`, `feet_air_time=0.20`, `termination_penalty=-50`, `ang_vel_xy_l2=-0.05`, `joint_deviation_hip=-0.2` and `joint_deviation_torso=-0.1`. Verify the **complete** native preset, not just these weights. Do not stack ORIENT, LINTRACK, AIRTIME or either ACTRATE delta.

## Completed Run

Full resolved config is archived at `native_run/params/env.yaml` and `agent.yaml`; nine intended weights match `h1-submit-2 + ang=0.65`, but full source/PPO parity remains unverified. Native run: `/workspace/training/humanoid/logs/rsl_rl/humanoid/2026-10-10_00-53-50`. No parent/resume; save_interval=50, 60 keeper checkpoints. Automatic best and latest keeper both match `model_2950.pt`, SHA `6a6f456eb3f25a7d2764af576e30b1a8169674256ae5c2ba0a1b79ed368e118c`.

[OFFICIAL training Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261010-exp-h1-angular-tracking-boost-fresh3k) / training intake〔원본 참조: `../../../data/processed/experiments/h1/2026-10-10_ANGTRACK065_OFFICIAL3K_EVIDENCE_INTAKE.md` / 공개 사본 미포함〕. `model_2950.pt` has a completed PERSONAL Windows six-video/full scenario7 evaluation (3,087 episodes; publication record〔원본 참조: `../../../data/processed/operations/windows_h1_video_evaluation/2026-10-10_ANGTRACK065_MODEL2950_PUBLICATION.md` / 공개 사본 미포함〕, [PERSONAL evaluation Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261010-exp-h1-angular-tracking-boost-model2950-video-eval)). A later PERSONAL single-policy behavior report is now received (HOLD); matched control comparison remains pending. No official score is claimed. The accompanying model_2700 ZIP belongs to ACTRATE-0001, not this Run.

## 2026-10-10 later matched-index RAW comparison with unchanged TERM-50 — HOLD

New direct RAW comparison〔원본 참조: `../../../data/processed/experiments/h1/2026-10-10_H1_ANGTRACK065_TERM50_DEEP_RAW_COMPARISON.md` / 공개 사본 미포함〕. Archived `TERM-50 model_2800` and `ANGTRACK-065 model_2950` evaluator ZIPs were directly read; integrity, byte-identical evaluator configs and **3,072 matching first-attempt cohort keys** verified. ANG recorded 3,087 raw rows: 3,072 initial episodes plus 15 short restart rows after H3 base-contact terminations. Only `-n0` initial cohort rows were compared with TERM's 3,072 rows.

**H3** first-attempt contact termination **TERM 0/384 vs ANG 15/384**, `vy_error` **0.06848 vs 0.18601**, stall **0.00912 vs 0.34339**. Both lateral metrics are worse in **384/384** matching cohort indices; ANG still performs poorly among its 369 completed 20-second H3 trials. **H4** yaw error **0.11934 vs 0.07704** (384/384 matching indices favor ANG). Composite tracking **0.157118 vs 0.130669** is lower for ANG, but **XY RMSE 0.112589 vs 0.125612** deteriorates, so the lower composite primarily reflects better yaw, not all-direction tracking. H5 rough mean forward **8.8961m vs 8.8949m** is approximately equal, with ANG ahead in only 179/384 paired indices. H1 unintended body-forward is smaller with ANG **0.8751m vs TERM 1.3523m**.

**Current decision: ALL-TERRAIN HOLD**, despite a yaw/zero-command benefit; no new training, evaluation or official score. Same evaluation keys do not prove identical physical terrain/reset realizations, independent training-seed replication, or causal reward improvement. The historical single-policy text below correctly described an earlier stage before raw baseline pairing.

## 2026-10-10 PERSONAL model_2950 behavior analysis received — HOLD

[Original report](<../../../reports/received/H1_ANGTRACK-065_POLICY_ANALYSIS_20261010.md>) / structured interpretation〔원본 참조: `../../../data/processed/experiments/h1/2026-10-10_ANGTRACK065_MODEL2950_POLICY_REVIEW.md` / 공개 사본 미포함〕. This is the previously trained OFFICIAL Run `20261009-155344-h1-angtrack-065-fresh3k` checkpoint SHA `6a6f456eb3f25a7d2764af576e30b1a8169674256ae5c2ba0a1b79ed368e118c`, not a new training Run or official evaluation.

The PERSONAL `scenario7` contains **3,072 initial cohorts but 3,087 episode rows**, because **15/384 first H3 lateral cohorts terminated** in base contact, each followed by one short reset episode. **H3 first-attempt 20-second timeout: 369/384 (96.09%)**; its 399-row survival percentage (96.24%) counts truncated restart rows and cannot replace the initial-cohort result. H3 `stall_fraction=0.3532`, `vy_error=0.1871m/s` and tracking `0.2203`. H1 zero command still yields +0.875m unintended forward displacement.

The report finds useful H2 14.703m forward, H4 yaw absolute error 0.0770rad/s, H5 rough 8.895m mean, H6 up/down 19.571/19.235m, H7 push 9.996m, and qualitative initial box/rough traversal. Videos do **not** show pure lateral-only commands or proven central multistep stairs. Reported `06_slope_down_10deg.mp4` alternating black even frames are a capture defect, not a fall.

**Decision HOLD**, especially for all-direction/lateral representative use. The existing `TERM-50/model_2800` raw evaluation is the next comparison candidate, but no ANGTRACK-to-control raw pairing, reward causal analysis or new GPU work was performed in this intake.

## Controls and outcome

1. Primary unchanged control: OFFICIAL `h1-submit-2` fresh3K Run `20261008-062732-h1-term-50-fresh3k-control`, COMPLETE/PASS, seed 42, 4096 envs. Its `model_2800` has separate PERSONAL full evaluation, not a completed A/B. Verify source/PPO/schema and evaluation parity.
2. Compare like-for-like late-window yaw and XY training errors, terrain progression, base-contact, timeout/episode length and action cost. After **separate GPU approval**, paired PERSONAL fixed evaluation should match commands, terrain/seed/horizon and measure yaw, combined x/y/yaw, balance/lateral drift, progress/stall and fall.
3. Treat old PERSONAL `ANGTRACK-075` BASE 1K collapse and public yaw 1.0 failures only as risk priors. Low yaw error when a robot is repeatedly failing or stationary cannot justify promotion.

PROMOTE only to controlled evaluation if real command tracking improves with acceptable terrain and failure costs. HOLD without matched evidence; REJECT collapsed policies. Preserve actual evidence provenance if a training Run later occurs. This plan creates no actual Run, official score or approval to change official source.
