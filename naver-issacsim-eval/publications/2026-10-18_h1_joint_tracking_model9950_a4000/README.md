# [분석] H1 joint tracking · model9950 · PERSONAL A4000 scenario7 평가

Experiment `exp-h1-joint-tracking-balance`; source OFFICIAL Run `20261018-021823-h1-top01-same-reward-to10k`. [Training Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261018-exp-h1-joint-tracking-balance-resume10k).

Evaluated native keeper **model_9950.pt**, SHA-256 `6e03f421b422c442ee85d449c708b3bf340d39e17c55de786276b9fd091847f3`, matches the source train checkpoint index. Raw evaluation `source_run_id` and `preset` remain null; this publication provides the separate SHA-based link.

PERSONAL Linux RTX A4000 camera-off H1 scenario7 is **COMPLETE/non-smoke**: 128 environments × seeds 4201/4202/4203 × eight cases = 3,072 validated episode rows, 20 seconds per case. Recorded runtime 1,019.15 seconds. **No six videos, A/B report or official score are included.** This is not another training Run. Windows protocol equality is not assumed.

Assets: unchanged result ZIP, checksum, publication manifest. ZIP: 546,213 bytes, SHA-256 `f0ecd1089e4d86f5009da565b73ed621a8e52e66c4d4f99d724fefb9e84dd731`; three files (`result/episodes.jsonl`, `result/evaluation_manifest.json`, `result/resolved_configs.json`). CRC, complete cohort validation and ZIP-to-loose equality passed. Success console logs are excluded under the user's error-only log policy.

Canonical raw: Originals `data/raw/private_server_runs/h1/2026-10-18_a4000_joint_tracking_model9950_evaluation/`. The Eval annotated tag identifies this publication record, not actual task/evaluator source. [Evaluation Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261018-exp-h1-joint-tracking-balance-model9950-a4000-eval). Policy quality/adoption remain pending; no GPU work was launched for publication.
