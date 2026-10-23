# Release copy migration — 2026-10-15

This is an exact-asset copy of the existing NVIDIA evaluation Release, not a new evaluation, training Run, submission or official score. All three original asset filenames/bytes are preserved. Embedded publication manifests retain their historical repository/tag fields; do not treat those fields as the new publication location. The new Eval annotated tag points to this migration-record commit, not the original task/training source. Original NVIDIA Release and tags remain unchanged; deletion is not part of this migration.

Original Release: https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261009-lintrack-075-corrected5k-model4997-video-eval

New Release: https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261009-lintrack-075-corrected5k-model4997-video-eval

## Original Release body (unchanged)

<!-- management-context:work-type-20261013 -->
> 현재 관리 분류: **분석**. 실행 출처: PERSONAL · Windows PC. 분류는 실행 장소가 아니라 수행한 작업을 따른다. 서버의 보조평가·영상도 분석이며 OFFICIAL 채점이나 추가 학습 Run을 뜻하지 않는다.
>
> 기존 태그·애셋·본문은 보존한다. 아래 본문의 과거 이름·관리 절차는 당시 기록으로 읽고, 현재 관리 규칙은 [Release 분류 문서](https://github.com/SE3C/naver-issacsim/blob/review/20261012-knowledge-structure-stage1/docs/RELEASE_TAXONOMY.md)를 따른다.

---

## Identity and status

### H1 LINTRACK-075 corrected 5K model_4997 · PERSONAL Windows videos + evaluation

## Artifacts

Assets: unchanged integrated ZIP + matching .sha256 + publication_manifest.json.

Additional exact existing asset filenames (unchanged):

- `h1_LINTRACK-075_corrected5k_model_4997_h1_6terrain_evaluation_20261009-235216_59e47db4.zip.sha256`

## Run and checkpoint provenance

2026-10-09 KST에 완료된 **6지형 영상 + 별도 camera-off full H1 scenario7** 통합 결과입니다. 신규 학습 Run, OFFICIAL 점수, A/B 비교 또는 calibration 결과가 아닙니다.

- Source training: PERSONAL corrected R04, Run `20260925-091257-h1-h008-corrected-control-to5k-h1-corrected-2026`.
- [Training Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260925-091257-h1-lintrack-075-corrected-control-to5k-h1-corrected-2026). Legacy aliases: H-008 / R04; descriptor LINTRACK-075.
- Final config: `h1-submit-2 + lin=0.75`; feet=+0.20, termination=-50 유지. 전체 설정의 근거는 원본 training archive의 native settings입니다.
- Parent: corrected R03 `model_2998.pt`, SHA-256 `49fdb297924c861493d377f22b9de135d83c73969ef3d8a2e4a56c9879414983`.
- Evaluated final checkpoint: `model_4997.pt`, SHA-256 `4349fe5650135c6a77546afc1b165ff60c235bdd83831bd562d618b04c3b5b6d`; automatic best model_4900이 아닙니다. 역사적 minus-feet 계보의 model_4997과도 다릅니다.
- Full evaluation: 128 env × 3 seeds (4201/4202/4203) × 8 cases × 20 seconds; 3,072 episodes, 24 cohorts. COMPLETE, smoke=false, native/BAT exit=0.
- Six videos: maneuver_push, 지형당 20초, H1 경사 ±10°. 영상과 점수 평가 루프는 별개입니다.
- Evaluation task commit / annotated tag target: `ef10b7a4c9a83481346d446e8a75aed655f72214`. Evaluator handoff: `28895d75edf3095607e392a07207a62e768478c7`.
- ZIP: `h1_LINTRACK-075_corrected5k_model_4997_h1_6terrain_evaluation_20261009-235216_59e47db4.zip`, 34,470,580 bytes, 18 files, SHA-256 `1c740a56fe30596202dbf98870f6f3d730d548d781131e86473f9d053e6a5488`.
- [Canonical Originals backup](https://github.com/SE3C/naver-issacsim-originals/tree/main/data/raw/private_server_runs/h1/2026-10-09_windows_lintrack075_model4997_video_evaluation).

원본 ZIP은 변경하지 않았습니다. ZIP 내부 source_run_id/preset=null은 그대로이며 training 연결은 외부 publication manifest에서 checkpoint SHA로 기록합니다. 원본 train metadata의 source_provenance_verified=false도 PASS 표시에 기대어 true로 바꾸지 않습니다. 단일 정책의 후속 평가 완료만 기록하며, 기존 가설 HOLD/paired evaluation 필요 판정은 유지합니다.

## Configuration and lineage

The display label is not a full resolved configuration. Configuration and lineage remain those of the original evidence; missing parameters or parent identities are not inferred.

## Canonical preservation and boundaries

Existing asset filenames and bytes remain unchanged. These are PERSONAL evidence/backup records, not an OFFICIAL competition score or a submission snapshot; original provenance and failed/interrupted evidence remain preserved.
