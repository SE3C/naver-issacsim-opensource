> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/research/experiments/h1/exp-h1-joint-tracking-posture-relaxation.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# exp-h1-joint-tracking-posture-relaxation

## Question

Can relaxing orientation and hip penalties in the joint-tracking/action configuration improve movement and recovery without losing tracking or survival? This is user candidate **2** from the [three-candidate plan](<../../planning/2026-10-16_H1_EVIDENCE_AND_RESEARCH_NEXT_EXPERIMENTS.md>), a complete-config search. Both penalties change together; the existing joint-tracking reference trained for 5K rather than this Run's 3K, so differences cannot isolate either reward's effect.

## Actual OFFICIAL training Run — 2026-10-17

- Run ID `20261017-072659-h1-lintrack-065-angtrack-060-actrate-0003-orient`; **COMPLETED / exit0 / evidence validation PASS**. Fresh/no parent/checkpoint/resume lineage, requested3000, console endpoint2999/3000, seed42,4096env, save_interval50.
- Final preset-relative override, full-field-name order: `h1-submit-2 + action=-0.0003 + orientation=-1.0 + hip=-0.1 + ang=0.60 + lin=0.65`. Other rewards match h1-submit-2. Full resolved source: original archive's `native_run/params/env.yaml`, `native_run/params/agent.yaml`, and `source/humanoid_rewards.py`; extracted copies are preserved with the train archive. Display names do not replace these full settings.
- Native Run `/workspace/training/humanoid/logs/rsl_rl/humanoid/2026-10-17_16-27-05`. UTC07:26:59.814138–08:03:36.921214. Official finalize/backup succeeded; organizer keeper copied60 checkpoints; source identity unchanged before/after. Captured commit `3e73d6dd79080fd7632488c061052a6edd52e230` identifies IsaacLab, not a separately established training-task revision.
- **Evaluated model_2850.pt** SHA256 `4a343750b47920d3b49e5e3ec7a3bf49fd9403d5b51a3727604971e6b7b0025d` has indexed native and organizer-keeper origins. Source keeper path `/workspace/training/humanoid/backup_log/2026-10-17_16-27-05/model_2850.pt`. The best reward event2840 is distinct from checkpoint filename2850.
- **Latest keeper model_2950.pt** SHA256 `c342e995ec77a2fb5f2845778d4e85146a244a4b4e311c29fe6f4275c539c216`, same keeper directory. It is preserved but is not the policy evaluated in the received ZIP. Neither checkpoint is an earlier ORIENT-100 or ACTRATE-001 policy with the same numbered filename.
- Canonical Originals path `data/raw/official_server_runs/h1/2026-10-17_072659_joint_tracking_posture_fresh3k/`. Unchanged received archive418915262bytes, SHA256 `be11dd838a3991f059b805477f015a9134831fc242d93b46960976214612e83c`. Its inner archive matches its received checksum. [Training Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261017-exp-h1-joint-tracking-posture-relaxation-fresh3k).

## PERSONAL Windows evaluation

- Evaluated model2850 SHA matches the verified official train checkpoint index and archive bytes. Source_run_id remains null in the received evaluation; the separate [publication manifest](https://github.com/SE3C/naver-issacsim-eval/blob/main/publications/2026-10-17_h1_joint_tracking_posture_model2850/publication_manifest.json) records the SHA-based connection without rewriting raw provenance.
- Six maneuver_push videos (20s each, H1 slopes±10°), plus separate camera-off H1 scenario7 **COMPLETE/non-smoke**, 128env × seeds4201/4202/4203 ×8cases =3072 episode rows. Original ZIP:18files, CRC and six MP4 checksums PASS.
- ZIP36524950bytes, SHA256 `af58e8f10165dbce7bd1c0363c09f523db925d9775870549819f94854fe4f6b9`; canonical Originals `data/raw/private_server_runs/h1/2026-10-17_windows_joint_tracking_posture_model2850_video_evaluation/`. [Evaluation Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261017-exp-h1-joint-tracking-posture-relaxation-model2850-video-eval).

## Decision

**Training, PERSONAL evaluation and policy report received; policy HOLD.** [Original report package and intake](<../../../reports/experiments/h1/analysis/2026-10-17_H1_JOINT_TRACKING_POSTURE_MODEL2850_POLICY_REVIEW.md>): reported3072/3072 timeout survival, but H1/H3 unintended body-forward progress−0.719/−0.679m, H3 world residual1.160m and H5 mean/P05/min progress8.024/7.460/6.721m remain. H5 stall>.05 occurs1/384, so persistent speed loss rather than widespread complete stall is the main rough concern. No promotion, matched A/B, official score or new submission is established. The report's missing train-link lookup is supplemented by the preserved train index/publication SHA connection; raw null metadata stays unchanged. Intake checked report/CSV/JSON, not raw episodes or MP4 playback, and launched no GPU work. Candidate1 and candidate3 remain planned until their own actual evidence arrives.
