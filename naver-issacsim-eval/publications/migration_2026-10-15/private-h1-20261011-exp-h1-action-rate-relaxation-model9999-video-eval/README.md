# Release copy migration — 2026-10-15

This is an exact-asset copy of the existing NVIDIA evaluation Release, not a new evaluation, training Run, submission or official score. All three original asset filenames/bytes are preserved. Embedded publication manifests retain their historical repository/tag fields; do not treat those fields as the new publication location. The new Eval annotated tag points to this migration-record commit, not the original task/training source. Original NVIDIA Release and tags remain unchanged; deletion is not part of this migration.

Original Release: https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261011-exp-h1-action-rate-relaxation-model9999-video-eval

New Release: https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261011-exp-h1-action-rate-relaxation-model9999-video-eval

## Original Release body (unchanged)

<!-- management-context:work-type-20261013 -->
> 현재 관리 분류: **분석**. 실행 출처: PERSONAL · Windows PC. 분류는 실행 장소가 아니라 수행한 작업을 따른다. 서버의 보조평가·영상도 분석이며 OFFICIAL 채점이나 추가 학습 Run을 뜻하지 않는다.
>
> 기존 태그·애셋·본문은 보존한다. 아래 본문의 과거 이름·관리 절차는 당시 기록으로 읽고, 현재 관리 규칙은 [Release 분류 문서](https://github.com/SE3C/naver-issacsim/blob/review/20261012-knowledge-structure-stage1/docs/RELEASE_TAXONOMY.md)를 따른다.

---

## Identity and status

### H1 ACTRATE-0001 fresh10K model_9999 — PERSONAL videos + evaluation

## Artifacts

Unchanged received ZIP: `model_9999_h1_6terrain_evaluation_20261011-162017_8438c90e.zip`, 34,850,043 bytes, SHA-256 `ecb6df0e03bf11ec1e2259f5e0fd8b7d4b57e6e63ca09c482f31a8adcf63bfbe`. All 18 entries passed CRC: six MP4, four video metadata files, seven evaluation files and BUNDLE_README.txt.

Assets: unchanged ZIP, SHA-256 sidecar, publication_manifest.json. NVIDIA annotated tag targets recorded evaluation task source `ef10b7a4c9a83481346d446e8a75aed655f72214`, not the preservation commit. Downloads original remains untouched.

Additional exact existing asset filenames (unchanged):

- `model_9999_h1_6terrain_evaluation_20261011-162017_8438c90e.zip.sha256`

## Run and checkpoint provenance

Source checkpoint SHA `a5020c273bc2b69bea1b20782fe80ba6605b3036b4054a7e5a8ab66151d2cb74` matches OFFICIAL fresh10K Run `20261011-041745-h1-actrate-0001-fresh10k-official`, indexed keeper `model_9999.pt`. This is not the same policy as automatic-best model_9900 or historical fresh3K model_2700. The publication manifest supplies the external lineage link; ZIP source_run_id/preset=null and protocol.smoke=null remain unchanged.

PERSONAL Windows H1 scenario7: COMPLETE, top-level smoke=false, camera off, 128 environments × three seeds × eight cases, 3,072 episode rows. No GPU job or A/B analysis was run during publication. Behavioral analysis received; decision HOLD. This PERSONAL evaluation is not an OFFICIAL score or policy-quality upgrade. The user's later actual Round-6 submission is recorded separately as h1-submit-6; it does not turn the independent analysis decision into PROMOTE.

## Configuration and lineage

The display label is not a full resolved configuration. Configuration and lineage remain those of the original evidence; missing parameters or parent identities are not inferred.

## Canonical preservation and boundaries

Training Release: https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261011-exp-h1-action-rate-relaxation-fresh10k

Evaluation Release: https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261011-exp-h1-action-rate-relaxation-model9999-video-eval
