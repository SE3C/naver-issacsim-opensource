# Release copy migration — 2026-10-15

This is an exact-asset copy of the existing NVIDIA evaluation Release, not a new evaluation, training Run, submission or official score. All three original asset filenames/bytes are preserved. Embedded publication manifests retain their historical repository/tag fields; do not treat those fields as the new publication location. The new Eval annotated tag points to this migration-record commit, not the original task/training source. Original NVIDIA Release and tags remain unchanged; deletion is not part of this migration.

Original Release: https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261010-exp-h1-action-rate-relaxation-model2700-video-eval

New Release: https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261010-exp-h1-action-rate-relaxation-model2700-video-eval

## Original Release body (unchanged)

<!-- management-context:work-type-20261013 -->
> 현재 관리 분류: **분석**. 실행 출처: PERSONAL · Windows PC. 분류는 실행 장소가 아니라 수행한 작업을 따른다. 서버의 보조평가·영상도 분석이며 OFFICIAL 채점이나 추가 학습 Run을 뜻하지 않는다.
>
> 기존 태그·애셋·본문은 보존한다. 아래 본문의 과거 이름·관리 절차는 당시 기록으로 읽고, 현재 관리 규칙은 [Release 분류 문서](https://github.com/SE3C/naver-issacsim/blob/review/20261012-knowledge-structure-stage1/docs/RELEASE_TAXONOMY.md)를 따른다.

---

## Identity and status

### H1 ACTRATE-0001 model_2700 · PERSONAL Windows videos + full evaluation

## Artifacts

Assets: unchanged ZIP + .sha256 + publication_manifest.json.

Additional exact existing asset filenames (unchanged):

- `model_2700_h1_6terrain_evaluation_20261010-012639_61aa406d.zip.sha256`

## Run and checkpoint provenance

Six maneuver_push videos (20 seconds each, H1 ±10° slopes), then **separate camera-off full H1 scenario7**. This is post-training PERSONAL evaluation, not OFFICIAL scoring, a new training Run or A/B comparison.

- Source OFFICIAL training Run: `20261009-142350-h1-actrate-0001-fresh3k`; [training Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261009-exp-h1-action-rate-relaxation-fresh3k).
- Config display: `h1-submit-2 + action=-0.0001`. Selected native checkpoint `model_2700.pt` SHA-256 `e54d3389e20ea913968ef8d3edbea5004368ff225fa6b94f73fcd91cf93ca7ae` matches the official index/automatic best. It is not latest keeper model_2950 or ANGTRACK-065.
- Evaluation COMPLETE, smoke=false, 128 env × 3 seeds (4201/4202/4203) × 8 cases × 20 seconds; 3,072 episodes / 24 cohorts.
- Local receipt records video_success=true, overall success=true, evaluation.native_exit_code=0, and matching combined ZIP SHA. BAT exit code is not recorded; do not infer one.
- Task checkout/tag target `ef10b7a4c9a83481346d446e8a75aed655f72214`, tracked clean; evaluator handoff `28895d75edf3095607e392a07207a62e768478c7`; protocol `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34`.
- ZIP `model_2700_h1_6terrain_evaluation_20261010-012639_61aa406d.zip`, 32,539,016 bytes, 18 nonempty files; SHA-256 `6270d299def2a3bcb8cc10253027898621dd65a00ad30baafde0cbcde03076e3`.
- [Canonical Originals backup](https://github.com/SE3C/naver-issacsim-originals/tree/main/data/raw/private_server_runs/h1/2026-10-10_windows_actrate0001_model2700_video_evaluation).

Source Run/preset null inside the ZIP remain unchanged; the external publication manifest links training by checkpoint SHA. Raw files are not renamed or edited. Training source_provenance_verified=false is not rewritten. **Analysis received; all-terrain HOLD.** A later TERM-50/ORIENT-100/ACTRATE-0001 raw comparison matched 3,072 cohort keys per policy; identical physical terrain/reset and replicated reward causality remain unverified. Completion does not imply a quality upgrade. Follow-up: https://github.com/SE3C/naver-issacsim/blob/main/data/processed/experiments/h1/2026-10-10_H1_SCENARIO7_RAW_3POLICY_MATCHED_ANALYSIS.md .

## Configuration and lineage

The display label is not a full resolved configuration. Configuration and lineage remain those of the original evidence; missing parameters or parent identities are not inferred.

## Canonical preservation and boundaries

Existing asset filenames and bytes remain unchanged. These are PERSONAL evidence/backup records, not an OFFICIAL competition score or a submission snapshot; original provenance and failed/interrupted evidence remain preserved.
