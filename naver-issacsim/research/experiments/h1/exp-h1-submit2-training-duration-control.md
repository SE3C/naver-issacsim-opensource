# exp-h1-submit2-training-duration-control

- Robot: H1
- Baseline preset: `h1-submit-2`
- Question: What does an unchanged-reward continuation toward a longer training horizon produce from the same TERM-50 baseline checkpoint?
- Effective override: none; archived `source/humanoid_rewards.py` matches the `h1-submit-2` reward weights.
- Status: **OFFICIAL training and PERSONAL A4000 evaluation COMPLETE; policy analysis/adoption HOLD**.

## Actual Run — 2026-10-18

- Run ID: `20261018-075224-h1-top05-same-reward-to10k`.
- Environment/mode: OFFICIAL H1; seed 42; 4096 environments.
- Resume: start iteration 2950; request 7050 additional iterations; final saved keeper is `model_9950.pt` (SHA-256 `2df0f838f571ad4f40d43d6127ef6dbefe1c79d7a1feb14e14faf644226a4991`). Metadata records the run as completed, exit 0, finalize complete, evidence validation PASS.
- Parent SHA: `a568e8df7df74c0ed2f8c1929d106d3fbd9a6307700dfff35de9126a34266c3c`, matching the indexed OFFICIAL TERM-50 fresh3K control `20261008-062732-h1-term-50-fresh3k-control` `model_2950.pt`. The new Run's raw `parent_run_id` is still null, source mode unknown, and imported-parent verification false; record the SHA match without rewriting those raw fields.
- The preparation plan labeled TOP05 as fresh. The actual archive command and metadata show resume from 2950; this executed Run supersedes that planned mode. Do not describe it as fresh.
- Full resolved training config is preserved in the original archive. Archived reward source SHA-256: `d689fac1ad376b8c1b936520b9cf5d40ffaae0b654a541c4bb6d90c1633fa71c`. Source Git commit is null; source file hashes are in `source/identity.json`.
- Canonical raw: [Originals receipt](https://github.com/SE3C/naver-issacsim-originals/tree/main/data/raw/official_server_runs/h1/2026-10-18_term50_resume10k/README.md). Download wrapper 958,580,684 bytes, SHA-256 `2c96ec7932a97e7e8e916ef759cc17900a9a81bb44e3b8ca3d51e494658000f2`.
- [OFFICIAL training Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261018-exp-h1-submit2-training-duration-control-resume10k).

## Evaluation and decision

The PERSONAL Linux A4000 camera-off `scenario7` evaluation is COMPLETE/non-smoke with 128 environments × seeds 4201/4202/4203 × eight cases × 20 seconds and 3,073 episode rows. Evaluated policy `model_9950.pt` SHA matches the OFFICIAL keeper index. Raw evaluation `source_run_id` remains null.

- Canonical evaluation ZIP: `naver-issacsim-originals/data/raw/private_server_runs/h1/2026-10-18_a4000_submit2_model9950_evaluation/`; 545,448 bytes, SHA-256 `4f8977ee6d31845f61f6638a1dc935e84af5c7b448e2e333019643d47de774ff`.
- [PERSONAL evaluation Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261018-exp-h1-submit2-training-duration-control-model9950-a4000-eval).

This establishes evaluation completion and checkpoint identity, not policy quality. Keep decision **HOLD**; no promotion, submission, or official score is established.

`TOP05` is a historical candidate-ranking alias, not this Experiment's canonical identity.
