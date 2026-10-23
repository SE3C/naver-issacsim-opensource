# [Training] H1 ACTRATE-0001 + FEETSLIDE-035 — OFFICIAL continuation toward 10K

Experiment: `exp-h1-action-foot-contact-stability`. Actual Run: `20261018-062435-h1-top04-same-reward-to10k`; metadata identifies OFFICIAL mode, completed status, exit 0, official finalize complete, organizer backup success, and evidence validation PASS.

This Run continues from stored iteration 2,950 for 7,050 additional iterations toward the 10,000 boundary, with seed 42, 4,096 environments, and save interval 50. Native Run: `/workspace/training/humanoid/logs/rsl_rl/humanoid/2026-10-18_15-24-41`. The checkpoint index contains 142 entries; latest preserved keeper is `model_9950.pt`, SHA-256 `2008e2f4c93a820c1ab396839ede1ba493e7b8dca7fffc3bbacb8de5ea257569`.

The selected parent is OFFICIAL fresh3K Run `20261013-153313-h1-actrate0001-feet_slide-fresh3k`, `model_2950.pt`, SHA-256 `c4b283509cc659e7bd47f5bf49eddbc387a43963d751ef353c632f48c7da1374`. The prepared Rank-4 plan and this Run's source-checkpoint SHA agree. The raw Run metadata nevertheless retains `source_evidence_run_id=null`, `source_run_mode=unknown`, and `source_provenance_verified=false`; the independent SHA link does not rewrite those fields.

Resolved reward configuration is `h1-submit-2 + action_rate_l2=-0.0001 + feet_slide=-0.35`; no reward changed from the parent. Full resolved settings and source identity remain in the unchanged evidence archive. The source snapshot did not change during training. No post-training evaluation, policy-quality decision, official score, submission, or preset promotion is recorded for `model_9950.pt`.

Outer download wrapper: `20261018-062435-h1-top04-same-reward-to10k-download.tar.gz`, 959,132,408 bytes, SHA-256 `49594ffed705a77c1137e55a88dc4e08b5a3519ccbe1e179782173a3a85908cf`. Its nested evidence archive is 952,724,498 bytes, SHA-256 `f6466b32b02245660abaa5e38d66bc3b19d0ea048d45890196310d38f55b0eb8`; the embedded SHA sidecar matches. The archive contains 173 members; no names matching `.env`, token, credential, submit config, secret, or auth were found.

[Training Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261018-exp-h1-action-foot-contact-stability-action0001-feetslide035-resume10k). This is training evidence only; a separate evaluation is still needed for policy assessment.
