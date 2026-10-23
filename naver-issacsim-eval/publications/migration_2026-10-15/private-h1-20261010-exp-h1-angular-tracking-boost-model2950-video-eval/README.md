# Release copy migration — 2026-10-15

This is an exact-asset copy of the existing NVIDIA evaluation Release, not a new evaluation, training Run, submission or official score. All three original asset filenames/bytes are preserved. Embedded publication manifests retain their historical repository/tag fields; do not treat those fields as the new publication location. The new Eval annotated tag points to this migration-record commit, not the original task/training source. Original NVIDIA Release and tags remain unchanged; deletion is not part of this migration.

Original Release: https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261010-exp-h1-angular-tracking-boost-model2950-video-eval

New Release: https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261010-exp-h1-angular-tracking-boost-model2950-video-eval

## Original Release body (unchanged)

<!-- management-context:work-type-20261013 -->
> 현재 관리 분류: **분석**. 실행 출처: PERSONAL · Windows PC. 분류는 실행 장소가 아니라 수행한 작업을 따른다. 서버의 보조평가·영상도 분석이며 OFFICIAL 채점이나 추가 학습 Run을 뜻하지 않는다.
>
> 기존 태그·애셋·본문은 보존한다. 아래 본문의 과거 이름·관리 절차는 당시 기록으로 읽고, 현재 관리 규칙은 [Release 분류 문서](https://github.com/SE3C/naver-issacsim/blob/review/20261012-knowledge-structure-stage1/docs/RELEASE_TAXONOMY.md)를 따른다.

---

## Identity and status

### H1 ANGTRACK-065 model_2950 · PERSONAL Windows videos + full evaluation

## Artifacts

Assets: unchanged integrated ZIP + matching `.sha256` + `publication_manifest.json`.

Additional exact existing asset filenames (unchanged):

- `model_best_h1_6terrain_evaluation_20261010-041416_066bf8a3.zip.sha256`

## Run and checkpoint provenance

Six `maneuver_push` terrain videos (20 seconds each, H1 ±10° slopes), followed by a separate camera-off full H1 `scenario7` evaluation. This is a post-training PERSONAL evaluation, not an official score, a new training Run, or an A/B comparison.

- Source OFFICIAL training Run: `20261009-155344-h1-angtrack-065-fresh3k`; [training Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261010-exp-h1-angular-tracking-boost-fresh3k).
- Selected checkpoint: `model_2950.pt`, SHA-256 `6a6f456eb3f25a7d2764af576e30b1a8169674256ae5c2ba0a1b79ed368e118c`. This links the evaluation to ANGTRACK-065; the source bundle's `source_run_id=null`, `preset=null`, and `source_provenance_verified=false` remain unchanged.
- Evaluation: COMPLETE, non-smoke, 128 environments × 3 seeds (4201/4202/4203) × 8 cases × 20 seconds; 3,087 episodes; native exit 0. Protocol `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34`.
- ZIP: `model_best_h1_6terrain_evaluation_20261010-041416_066bf8a3.zip`, 32,626,954 bytes / 18 files, SHA-256 `ec1bc325feae5cd6da1643a9fbbe13b0640ad7514b77b79e5532d8b836def93b`.
- [Canonical raw backup](https://github.com/SE3C/naver-issacsim-originals/tree/main/data/raw/private_server_runs/h1/2026-10-10_windows_angtrack065_model2950_video_evaluation).
- Evaluation task / annotated-tag target: `ef10b7a4c9a83481346d446e8a75aed655f72214`.

**Decision remains HOLD.** Evaluation completion alone does not establish improvement or promotion; policy analysis is received/HOLD, and the later TERM-50 raw comparison matched 3,072 first-attempt cohort keys (15 ANGTRACK restart rows were handled separately). Physical terrain/reset parity, independent training replication and causal reward improvement remain unverified. Follow-up: https://github.com/SE3C/naver-issacsim/blob/main/data/processed/experiments/h1/2026-10-10_H1_ANGTRACK065_TERM50_DEEP_RAW_COMPARISON.md . No official score is claimed.

## Configuration and lineage

The display label is not a full resolved configuration. Configuration and lineage remain those of the original evidence; missing parameters or parent identities are not inferred.

## Canonical preservation and boundaries

Existing asset filenames and bytes remain unchanged. These are PERSONAL evidence/backup records, not an OFFICIAL competition score or a submission snapshot; original provenance and failed/interrupted evidence remain preserved.
