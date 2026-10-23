# [분석] H1 LINTRACK-065 · model9999 · PERSONAL A4000 scenario7 평가

Experiment: `exp-h1-planar-tracking-weight`. Source training Run: `20261018-074037-h1-top06-same-reward-to10k` ([PERSONAL training Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261018-exp-h1-planar-tracking-weight-lin065-resume10k)).

PERSONAL Linux A4000 camera-off H1 `scenario7` completed: 128 environments × seeds 4201/4202/4203 × eight cases × 20 simulated seconds. The manifest records COMPLETE, complete=true and smoke=false. There are 3,072 time-window cohorts and 3,072 episode rows. This evaluation-only ZIP contains three files and no videos, policy comparison or official score.

The evaluated native `model_9999.pt` SHA-256 is `030253593bda0b0b3b5ce11532cc8446b19fabdf172d8a96dd7c1c9757e3a856`, matching the checkpoint member in the training archive. The supplied training archive has no `checkpoint_index.json`; none was synthesized. Original `policy.source_run_id=null` and `policy.preset=null` remain unchanged. Protocol ID: `5ebd59ae7b45d3bc87af7916d871086872a1d90368461d01c2a28172dcd5b121`.

Archive: `h1-top06-same-reward-to10k_model_9999_A4000_evaluation_20261018.zip`, 545,434 bytes, SHA-256 `0c958e62450e3ee697d0c747bb00e0386c7bcebb5237009b869bea546c5ea417`. ZIP CRC and policy/cohort linkage were checked without another GPU run. Canonical raw: `naver-issacsim-originals/data/raw/private_server_runs/h1/2026-10-18_a4000_lintrack065_model9999_evaluation/`.

Assets: original ZIP, its `.sha256`, and `publication_manifest.json`. The annotated Release tag points to this repository's publication-record commit, not the training task or evaluator source commit. Evaluation completion does not establish policy improvement; analysis/adoption remain HOLD.
