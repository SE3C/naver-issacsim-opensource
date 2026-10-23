# Release copy migration — 2026-10-15

This is an exact-asset copy of the existing NVIDIA evaluation Release, not a new evaluation, training Run, submission or official score. All three original asset filenames/bytes are preserved. Embedded publication manifests retain their historical repository/tag fields; do not treat those fields as the new publication location. The new Eval annotated tag points to this migration-record commit, not the original task/training source. Original NVIDIA Release and tags remain unchanged; deletion is not part of this migration.

Original Release: https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-go2-20261009-g2-submit-3-model4800-video-eval

New Release: https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-go2-20261009-g2-submit-3-model4800-video-eval

## Original Release body (unchanged)

<!-- management-context:work-type-20261013 -->
> 현재 관리 분류: **분석**. 실행 출처: PERSONAL · Windows PC. 분류는 실행 장소가 아니라 수행한 작업을 따른다. 서버의 보조평가·영상도 분석이며 OFFICIAL 채점이나 추가 학습 Run을 뜻하지 않는다.
>
> 기존 태그·애셋·본문은 보존한다. 아래 본문의 과거 이름·관리 절차는 당시 기록으로 읽고, 현재 관리 규칙은 [Release 분류 문서](https://github.com/SE3C/naver-issacsim/blob/review/20261012-knowledge-structure-stage1/docs/RELEASE_TAXONOMY.md)를 따른다.

---

## Identity and status

### Go2 g2-submit-3 · model_4800 · PERSONAL six-video + evaluation

## Artifacts

Existing GitHub assets (filenames and bytes unchanged):

- `g2-submit-3_model_4800_go2_6terrain_evaluation_20261009-021618_04460d33.zip`
- `g2-submit-3_model_4800_go2_6terrain_evaluation_20261009-021618_04460d33.zip.sha256`
- `publication_manifest.json`

## Run and checkpoint provenance

Unmodified Windows PERSONAL post-training evaluation of the original Round-3 submission checkpoint, not a new training Run or an official score.

- Checkpoint SHA-256: `ea93f9b5b04d91a91d1cdb97c6d328978017991e0602745f9269c7190bfaba65`.
- OFFICIAL source training: [original fresh run](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-go2-20260914-lintrack-150-linz-2-5k-interrupted), which remains **INTERRUPTED / validation FAIL**; successful PERSONAL evaluation does not change that state.
- [Original4800 official submission export](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-go2-20260915-lintrack-150-linz-2-original4800-submission); not recovery model_4900 or automatic-best model_7050.
- Six maneuver/push terrain videos and full camera-off scenario7: 128 environments, seeds 4201/4202/4203, nine cases × 20 seconds; 3,471 episodes, complete=true, smoke=false, native exit 0.
- Evaluation task checkout: `ef10b7a4c9a83481346d446e8a75aed655f72214`; this annotated tag records evaluation source, not the September training source.
- ZIP: g2-submit-3_model_4800_go2_6terrain_evaluation_20261009-021618_04460d33.zip; 36,843,939 bytes; SHA-256 `f2bb7917fd325544858ce5aecf801f54e24572c164ed5c6d38ed17c316a1d221`; 18 files.
- Assets: original ZIP, its SHA sidecar and publication_manifest.json. No separate MP4 duplication, official score, calibrated score or A/B report.

## Configuration and lineage

The display label is not a full resolved configuration. Configuration and lineage remain those of the original evidence; missing parameters or parent identities are not inferred.

## Canonical preservation and boundaries

Canonical raw copy: `SE3C/naver-issacsim-originals/data/raw/private_server_runs/go2/2026-10-09_windows_model4800_video_evaluation/`. Original ZIP manifests were not rewritten; training linkage is recorded in the external publication manifest.
