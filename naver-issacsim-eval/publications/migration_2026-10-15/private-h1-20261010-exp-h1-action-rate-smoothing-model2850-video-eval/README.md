# Release copy migration — 2026-10-15

This is an exact-asset copy of the existing NVIDIA evaluation Release, not a new evaluation, training Run, submission or official score. All three original asset filenames/bytes are preserved. Embedded publication manifests retain their historical repository/tag fields; do not treat those fields as the new publication location. The new Eval annotated tag points to this migration-record commit, not the original task/training source. Original NVIDIA Release and tags remain unchanged; deletion is not part of this migration.

Original Release: https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261010-exp-h1-action-rate-smoothing-model2850-video-eval

New Release: https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261010-exp-h1-action-rate-smoothing-model2850-video-eval

## Original Release body (unchanged)

<!-- management-context:work-type-20261013 -->
> 현재 관리 분류: **분석**. 실행 출처: PERSONAL · Windows PC. 분류는 실행 장소가 아니라 수행한 작업을 따른다. 서버의 보조평가·영상도 분석이며 OFFICIAL 채점이나 추가 학습 Run을 뜻하지 않는다.
>
> 기존 태그·애셋·본문은 보존한다. 아래 본문의 과거 이름·관리 절차는 당시 기록으로 읽고, 현재 관리 규칙은 [Release 분류 문서](https://github.com/SE3C/naver-issacsim/blob/review/20261012-knowledge-structure-stage1/docs/RELEASE_TAXONOMY.md)를 따른다.

---

## Identity and status

### H1 ACTRATE-001 model_2850 PERSONAL Windows video and evaluation

## Artifacts

Existing GitHub assets (filenames and bytes unchanged):

- `model_2850_h1_6terrain_evaluation_20261010-233937_1cc2ab9d.zip`
- `model_2850_h1_6terrain_evaluation_20261010-233937_1cc2ab9d.zip.sha256`
- `publication_manifest.json`

## Run and checkpoint provenance

This directory preserves the received combined ZIP unchanged. It records PERSONAL Windows post-training video and evaluation of the automatic-best checkpoint from an OFFICIAL H1 ACTRATE-001 fresh 3K Run. The checkpoint number `model_2850.pt` also appears in the separate ORIENT-100 Run; the SHA-256 below identifies this artifact as ACTRATE-001. This is not an official score, a new training Run, or an official-server evaluation.

- Source training Run: `20261010-125324-h1-actrate-001-fresh3k`; [OFFICIAL training Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261010-exp-h1-action-rate-smoothing-fresh3k).
- Source checkpoint: `model_2850.pt`, SHA-256 `1e6d0950f5bd981ca1f88044e65ae7ee57505c47b92b5caad8c39263f4d93bb1` (automatic best at iteration 2850, matching the official training checkpoint index). The latest preserved training checkpoint `model_2950.pt` is a different file and is not evaluated here.
- Original bundle: `model_2850_h1_6terrain_evaluation_20261010-233937_1cc2ab9d.zip`; 35,121,564 bytes; SHA-256 `1906880030393b904d7323bdbf71352f408a067328a09ac8bf87604438c07351`.
- Bundle contents: 18 files, including six 20-second H1 videos and full camera-off `scenario7` evaluation evidence. The videos use the separate qualitative `maneuver_push` suite with ±10° slopes. CRC validation passed.
- Evaluation: PERSONAL Windows, scenario7, complete and not smoke; 7 scenarios / 8 cases, 128 environments, seeds 4201/4202/4203, 3,072 episodes total, 20 seconds / 1,000 steps each, camera disabled. Diagnostics record zero base-contact failures in these fixed 20-second windows; this does not establish terrain completion or an official score.
- Protocol ID: `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34`.
- The original `evaluation/evaluation_manifest.json` and `evaluation/video_evaluation_link.json` keep `policy.source_run_id` null. The external Run link is based on the source checkpoint SHA matching the preserved OFFICIAL ACTRATE-001 training evidence; the ZIP metadata itself is unchanged.
- [PERSONAL Windows Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261010-exp-h1-action-rate-smoothing-model2850-video-eval).

The OFFICIAL training archive remains in the parent Run directory. No checkpoint, source code, or training artifact was modified or merged into this PERSONAL evaluation bundle.

## Configuration and lineage

The display label is not a full resolved configuration. Configuration and lineage remain those of the original evidence; missing parameters or parent identities are not inferred.

## Canonical preservation and boundaries

Existing asset filenames and bytes remain unchanged. These are PERSONAL evidence/backup records, not an OFFICIAL competition score or a submission snapshot; original provenance and failed/interrupted evidence remain preserved.
