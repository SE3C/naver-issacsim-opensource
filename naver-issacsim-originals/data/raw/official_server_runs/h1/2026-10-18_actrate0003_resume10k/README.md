# [학습] H1 ACTRATE-0003 · OFFICIAL same-reward continuation toward 10K

Experiment: `exp-h1-action-rate-relaxation`. Actual Run: `20261018-032205-h1-top02-same-reward-to10k`; metadata identifies OFFICIAL mode, completed status, exit 0, official finalize complete, organizer backup success, and evidence validation PASS.

This resumes from `/workspace/model_2950.pt`, SHA-256 `1cc2c03197097c21c642e8373c760b25664b9c859ed75b5dc07582a770473c4b`. That SHA matches the preserved OFFICIAL keeper index of Run `20261016-033023-h1-actrate-0003-fresh3k`. The new archive itself retains `parent_run_id=null`, `source_run_mode=unknown`, and `source_provenance_verified=false`; the separate hash/index match does not rewrite these raw provenance fields.

Requested 7,050 additional iterations from stored iteration 2,950 toward the 10,000 boundary; seed 42, 4,096 environments. Native console endpoint is **9999/10000**. Latest preserved keeper is **model_9950.pt**, SHA-256 `6da0deb29a2d539c2c1447a1235cfdc46d16baa989397b8216ea824586f3ec10`; there is no indexed `model_10000.pt`. The finalizer's `model_best.pt` is a different selected checkpoint at reported iteration 9560.

Resolved reward weights are `h1-submit-2 + action_rate_l2=-0.0003`; other recorded active weights match that preset. Full config and source identity remain in the unchanged archive. Recorded source identity is IsaacLab commit `3e73d6dd79080fd7632488c061052a6edd52e230`; this is not a separately verified training-task Git commit.

Original wrapper archive: 958,823,518 bytes, SHA-256 `99d6993b408d36881f929c8a62b42b550ff35076b12c51b33f3ea8bd4a35d1df`.

[Training Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261018-exp-h1-action-rate-relaxation-action0003-resume10k). This records completed training evidence only; no new evaluation, policy-quality decision, official score, submission, or preset promotion is implied.
