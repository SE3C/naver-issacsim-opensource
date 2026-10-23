# Release copy migration — 2026-10-15

This is an exact-asset copy of the existing NVIDIA evaluation Release, not a new evaluation, training Run, submission or official score. All three original asset filenames/bytes are preserved. Embedded publication manifests retain their historical repository/tag fields; do not treat those fields as the new publication location. The new Eval annotated tag points to this migration-record commit, not the original task/training source. Original NVIDIA Release and tags remain unchanged; deletion is not part of this migration.

Original Release: https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261011-exp-h1-action-first-planar-tracking-switch-model4650-video-eval

New Release: https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261011-exp-h1-action-first-planar-tracking-switch-model4650-video-eval

## Original Release body (unchanged)

<!-- management-context:work-type-20261013 -->
> 현재 관리 분류: **분석**. 실행 출처: PERSONAL · Windows PC. 분류는 실행 장소가 아니라 수행한 작업을 따른다. 서버의 보조평가·영상도 분석이며 OFFICIAL 채점이나 추가 학습 Run을 뜻하지 않는다.
>
> 기존 태그·애셋·본문은 보존한다. 아래 본문의 과거 이름·관리 절차는 당시 기록으로 읽고, 현재 관리 규칙은 [Release 분류 문서](https://github.com/SE3C/naver-issacsim/blob/review/20261012-knowledge-structure-stage1/docs/RELEASE_TAXONOMY.md)를 따른다.

---

## Identity and status

### H1 ACTRATE-0001 → lin=0.65 — PERSONAL model_4650 videos + evaluation

## Artifacts

Publication includes the ZIP, its SHA-256 sidecar and publication manifest. Windows evaluation is PERSONAL post-training evidence, not an OFFICIAL score, new training Run, submission or A/B comparison. Policy analysis received; decision HOLD; adoption remains pending.

Additional exact existing asset filenames (unchanged):

- `model_4650_h1_6terrain_evaluation_20261011-030854_89b4c4a0.zip`
- `model_4650_h1_6terrain_evaluation_20261011-030854_89b4c4a0.zip.sha256`
- `publication_manifest.json`

## Run and checkpoint provenance

Six H1 terrain videos (±10° slopes, maneuver_push, 20 seconds each), followed by separate full camera-off scenario7 evaluation: 128 environments, three seeds, eight cases. Recorded completion is COMPLETE, not smoke.

The 18-file ZIP is preserved unchanged; CRC validation passed. Its checkpoint SHA matches the completed OFFICIAL resume Run `20261010-154926-h1-actrate0001-lintrack065-from2700-plus2k` index for `model_4650.pt`, SHA-256 `ce7ad58657f3dd744e7cf2b7531f3d7d455773dfc6fb135f39d8a55aa49dea70`. This latest preserved/evaluated checkpoint is distinct from automatic-best `model_2900.pt`; embedded source metadata is preserved unchanged.
Evaluation task checkout/tag target: `ef10b7a4c9a83481346d446e8a75aed655f72214`; this is not an inferred OFFICIAL training source commit.

## Configuration and lineage

The display label is not a full resolved configuration. Configuration and lineage remain those of the original evidence; missing parameters or parent identities are not inferred.

## Canonical preservation and boundaries

Existing asset filenames and bytes remain unchanged. These are PERSONAL evidence/backup records, not an OFFICIAL competition score or a submission snapshot; original provenance and failed/interrupted evidence remain preserved.
