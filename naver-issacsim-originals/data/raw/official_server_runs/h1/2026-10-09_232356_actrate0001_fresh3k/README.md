# H1 ACTRATE-0001 — OFFICIAL fresh 3K

Experiment: `exp-h1-action-rate-relaxation`. Does relaxing action-rate penalty improve command responsiveness and combined x/y/yaw tracking without unacceptable terrain/failure costs?

- Run: `20261009-142350-h1-actrate-0001-fresh3k`; native run `/workspace/training/humanoid/logs/rsl_rl/humanoid/2026-10-09_23-23-56`.
- OFFICIAL / train / fresh; no parent or resume checkpoint.
- Requested/completed: 3,000 iterations, console reaches 2999/3000; seed 42, 4096 environments, save_interval=50.
- Start/end UTC: 2026-10-09T14:23:50.440281+00:00 / 2026-10-09T15:01:07.363758+00:00.
- COMPLETED, exit 0, evidence validation PASS; official finalize completed and native backup succeeded. Backup is not a portal submission.
- Preset-relative display: `h1-submit-2 + action=-0.0001`. Checked effective weights: lin=0.5, ang=0.5, feet=+0.20, termination=-50, orientation=-1.5, angxy=-0.05, hip=-0.2, torso=-0.1, action=-0.0001.
- Full resolved source: nested `native_run/params/env.yaml` + `agent.yaml`; reward source `source/humanoid_rewards.py`, source fingerprint `source/identity.json`. Nine matching weights do not establish full source/PPO parity with the frozen submission or control. Official source Git commit is not independently identified; archived file fingerprints remain the source identity.
- Preserved: TensorBoard, console, full native config, source hashes and 60 organizer checkpoints at 50-step spacing (0–2950), inside the nested archive.
- Automatic best: `model_best.pt = model_2700.pt`, SHA-256 `e54d3389e20ea913968ef8d3edbea5004368ff225fa6b94f73fcd91cf93ca7ae` (checkpoint index; native peak at step 2715). Latest preserved `model_2950.pt`: SHA-256 `d4fa722131d0559e02bbdf499cac87e6bba91372a1c9f9334b8cd4a7b7269b70`, origin organizer_keeper_backup. These are distinct checkpoint roles.
- Unchanged received wrapper: `20261009-142350-h1-actrate-0001-fresh3k-download.tar.gz`, 419,108,331 bytes, SHA-256 `38a6225ae59465fcb36496eef472b396b9095754587489d4b3091350f5a35b04`.
- Nested evidence archive: `20261009-142350-h1-actrate-0001-fresh3k.tar.gz`, 412,571,809 bytes, SHA-256 `d387a5c608c81ee49bfca7f2ebb12ff7f7a3f08682a42b9c131e3fde74aa5db2`, matched received checksum. Wrapper and nested archive represent one Run, not two.
- Metadata source_provenance_verified=false remains unchanged; this fresh Run has no parent checkpoint to relabel.

Canonical raw: `data/raw/official_server_runs/h1/2026-10-09_232356_actrate0001_fresh3k/evidence_archives/`.
Release: https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261009-exp-h1-action-rate-relaxation-fresh3k

Assets: unchanged download archive + its external checksum + this preservation note. Native files and loose exports remain inside the wrapper; no duplicate checkpoint upload. No video, policy export, evaluator result, analysis report or submission snapshot is claimed. Outcome **HOLD / analysis and matched evaluation pending**; completing training does not establish superiority. User Downloads original is preserved.
