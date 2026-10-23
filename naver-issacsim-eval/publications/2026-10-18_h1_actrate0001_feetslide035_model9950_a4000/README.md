# [분석] H1 ACTRATE-0001 + FEETSLIDE-035 · model9950 · PERSONAL A4000 scenario7 평가

Experiment `exp-h1-action-foot-contact-stability`; source OFFICIAL Run `20261018-062435-h1-top04-same-reward-to10k`. [Training Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261018-exp-h1-action-foot-contact-stability-action0001-feetslide035-resume10k).

Evaluated native keeper **model_9950.pt**, SHA-256 `2008e2f4c93a820c1ab396839ede1ba493e7b8dca7fffc3bbacb8de5ea257569`, matches the source train checkpoint index. Raw evaluation `source_run_id` and `preset` remain null; this publication records the separate SHA-based link.

PERSONAL Linux RTX A4000 camera-off H1 scenario7 is **COMPLETE/non-smoke**: 128 environments × seeds 4201/4202/4203 × eight cases, 20 seconds per case. All **3,072 time-window cohorts** pass the evaluator's dataset validator; **3,074 episode rows** include restarted episodes. Recorded runtime: 966.51 seconds. **No six videos, comparison report or official score are included.**

Assets: unchanged result ZIP, checksum, publication manifest. ZIP: 546,945 bytes, SHA-256 `62345448eabc9e550816103ded5117495c303103d1a0521add2ea6a877b1f582`; three files (`result/episodes.jsonl`, `result/evaluation_manifest.json`, `result/resolved_configs.json`). CRC and checkpoint identity passed. Successful console logs are excluded under the user's error-only log policy.

Canonical raw: Originals `data/raw/private_server_runs/h1/2026-10-18_a4000_actrate0001_feetslide035_model9950_evaluation/`. The Eval annotated tag identifies this publication record, not actual training/evaluator source. [Evaluation Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261018-exp-h1-action-foot-contact-stability-action0001-feetslide035-model9950-a4000-eval). Policy analysis/adoption remain pending/HOLD. No GPU work was launched for publication.
