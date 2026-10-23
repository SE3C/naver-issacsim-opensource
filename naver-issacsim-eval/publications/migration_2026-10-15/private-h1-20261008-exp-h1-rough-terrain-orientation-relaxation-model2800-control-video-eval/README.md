# Release copy migration — 2026-10-15

This is an exact-asset copy of the existing NVIDIA evaluation Release, not a new evaluation, training Run, submission or official score. All three original asset filenames/bytes are preserved. Embedded publication manifests retain their historical repository/tag fields; do not treat those fields as the new publication location. The new Eval annotated tag points to this migration-record commit, not the original task/training source. Original NVIDIA Release and tags remain unchanged; deletion is not part of this migration.

Original Release: https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261008-exp-h1-rough-terrain-orientation-relaxation-model2800-control-video-eval

New Release: https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261008-exp-h1-rough-terrain-orientation-relaxation-model2800-control-video-eval

## Original Release body (unchanged)

<!-- management-context:work-type-20261013 -->
> 현재 관리 분류: **분석**. 실행 출처: PERSONAL · Windows PC. 분류는 실행 장소가 아니라 수행한 작업을 따른다. 서버의 보조평가·영상도 분석이며 OFFICIAL 채점이나 추가 학습 Run을 뜻하지 않는다.
>
> 기존 태그·애셋·본문은 보존한다. 아래 본문의 과거 이름·관리 절차는 당시 기록으로 읽고, 현재 관리 규칙은 [Release 분류 문서](https://github.com/SE3C/naver-issacsim/blob/review/20261012-knowledge-structure-stage1/docs/RELEASE_TAXONOMY.md)를 따른다.

---

## Identity and status

### H1 h1-submit-2 / TERM-50 · model_2800 · PERSONAL Windows 6영상 + 평가

## Artifacts

### 자산

ZIP은 6 MP4·영상 metadata 4개·evaluation 파일 7개·README로 총 18개입니다. CRC와 receipt 일치를 확인했습니다. 개별 영상을 중복 게시하지 않습니다.

Additional exact existing asset filenames (unchanged):

- `model_2800_h1_6terrain_evaluation_20261008-171331_a8ab9d61.zip.sha256`

## Run and checkpoint provenance

공식 fresh 3K control Run `20261008-062732-h1-term-50-fresh3k-control`의 automatic-best `model_2800.pt`를 Windows PERSONAL 환경에서 사후 촬영·평가한 자료입니다. 공식 서버 학습 결과와 개인 평가를 구분합니다. 공식 채점·새 학습 Run·제출 snapshot이 아닙니다.

- 원본 통합 ZIP `model_2800_h1_6terrain_evaluation_20261008-171331_a8ab9d61.zip`: 34,012,853 bytes, SHA-256 `d4a47b0e182763e21077b688f44f7d9cdc00759c0f0f78f4217930e1c49975da`.
- 동일 파일명의 `.sha256`.
- `publication_manifest.json`: 공식 학습 계보와 PERSONAL 평가 출처.

### 출처

- Experiment: `exp-h1-rough-terrain-orientation-relaxation`의 baseline control; reward descriptor `TERM-50`, preset `h1-submit-2`, reward override 없음.
- [공식 학습 원본](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261008-h1-submit-2-fresh3k-control): OFFICIAL fresh 3000, COMPLETE/PASS, seed 42, 4096 env, parent 없음.
- `model_2800.pt` SHA-256 `dffaa77848741fed1f4d22d0b78d4d8911af49057541107845e4d1df02c09ad6`는 공식 checkpoint index와 일치합니다. latest keeper `model_2950.pt`와 다릅니다.
- PERSONAL Windows 평가: H1 camera-off scenario7, 128 env × seeds 4201/4202/4203 ×8 cases ×20초; 3072 aggregate episodes; complete=true, smoke=false, native exit 0.
- protocol `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34`.
- 별도 6영상은 maneuver_push / 각20초 / H1 ±10° slope 조건입니다.
- 평가 task checkout 및 annotated tag target: `ef10b7a4c9a83481346d446e8a75aed655f72214`; evaluator handoff `28895d75edf3095607e392a07207a62e768478c7`, upstream `9c774a322f2f7d4944444de57f01308987bcb3da`.
- 원본 내부 preset/source_run_id=null은 그대로 보존합니다. 외부 공식 학습 연결은 checkpoint SHA로 기록합니다. A/B 비교·공식 점수·reward 우위 판정은 포함하지 않습니다.

## Configuration and lineage

The display label is not a full resolved configuration. Configuration and lineage remain those of the original evidence; missing parameters or parent identities are not inferred.

## Canonical preservation and boundaries

Canonical: `SE3C/naver-issacsim-originals/data/raw/private_server_runs/h1/2026-10-08_windows_model2800_video_evaluation/`. 공식 학습 원본 및 Downloads 파일은 변경·삭제하지 않았습니다.
