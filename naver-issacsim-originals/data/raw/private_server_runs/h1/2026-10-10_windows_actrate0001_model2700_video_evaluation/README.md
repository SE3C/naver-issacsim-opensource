# H1 ACTRATE-0001 model_2700 · PERSONAL Windows videos + full evaluation

Six maneuver_push videos (20 seconds each, H1 ±10° slopes), then **separate camera-off full H1 scenario7**. This is post-training PERSONAL evaluation, not OFFICIAL scoring, a new training Run or A/B comparison.

- Source OFFICIAL training Run: `20261009-142350-h1-actrate-0001-fresh3k`; [training Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261009-exp-h1-action-rate-relaxation-fresh3k).
- Config display: `h1-submit-2 + action=-0.0001`. Selected native checkpoint `model_2700.pt` SHA-256 `e54d3389e20ea913968ef8d3edbea5004368ff225fa6b94f73fcd91cf93ca7ae` matches the official index/automatic best. It is not latest keeper model_2950 or ANGTRACK-065.
- Evaluation COMPLETE, smoke=false, 128 env × 3 seeds (4201/4202/4203) × 8 cases × 20 seconds; 3,072 episodes / 24 cohorts.
- Local receipt records video_success=true, overall success=true, evaluation.native_exit_code=0, and matching combined ZIP SHA. BAT exit code is not recorded; do not infer one.
- Task checkout/tag target `ef10b7a4c9a83481346d446e8a75aed655f72214`, tracked clean; evaluator handoff `28895d75edf3095607e392a07207a62e768478c7`; protocol `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34`.
- ZIP `model_2700_h1_6terrain_evaluation_20261010-012639_61aa406d.zip`, 32,539,016 bytes, 18 nonempty files; SHA-256 `6270d299def2a3bcb8cc10253027898621dd65a00ad30baafde0cbcde03076e3`.
- [Canonical Originals backup](https://github.com/SE3C/naver-issacsim-originals/tree/main/data/raw/private_server_runs/h1/2026-10-10_windows_actrate0001_model2700_video_evaluation).

Source Run/preset null inside the ZIP remain unchanged; the external publication manifest links training by checkpoint SHA. Raw files are not renamed or edited. Training source_provenance_verified=false is not rewritten. **HOLD / analysis and matched comparison pending**, with no quality upgrade implied by completion.

Assets: unchanged ZIP + .sha256 + publication_manifest.json.
