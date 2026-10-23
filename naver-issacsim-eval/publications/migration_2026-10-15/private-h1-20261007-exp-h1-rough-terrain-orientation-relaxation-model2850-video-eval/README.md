# Release copy migration — 2026-10-15

This is an exact-asset copy of the existing NVIDIA evaluation Release, not a new evaluation, training Run, submission or official score. All three original asset filenames/bytes are preserved. Embedded publication manifests retain their historical repository/tag fields; do not treat those fields as the new publication location. The new Eval annotated tag points to this migration-record commit, not the original task/training source. Original NVIDIA Release and tags remain unchanged; deletion is not part of this migration.

Original Release: https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261007-exp-h1-rough-terrain-orientation-relaxation-model2850-video-eval

New Release: https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261007-exp-h1-rough-terrain-orientation-relaxation-model2850-video-eval

## Original Release body (unchanged)

<!-- management-context:work-type-20261013 -->
> 현재 관리 분류: **분석**. 실행 출처: PERSONAL · Windows PC. 분류는 실행 장소가 아니라 수행한 작업을 따른다. 서버의 보조평가·영상도 분석이며 OFFICIAL 채점이나 추가 학습 Run을 뜻하지 않는다.
>
> 기존 태그·애셋·본문은 보존한다. 아래 본문의 과거 이름·관리 절차는 당시 기록으로 읽고, 현재 관리 규칙은 [Release 분류 문서](https://github.com/SE3C/naver-issacsim/blob/review/20261012-knowledge-structure-stage1/docs/RELEASE_TAXONOMY.md)를 따른다.

---

## Identity and status

H1 ORIENT-100 · model_2850 · PERSONAL Windows 6영상 + 평가

## Artifacts

Existing GitHub assets (filenames and bytes unchanged):

- `model_2850_ORIENT-100_h1_6terrain_evaluation_20261007-010444_f6b3b8b3.zip`
- `model_2850_ORIENT-100_h1_6terrain_evaluation_20261007-010444_f6b3b8b3.zip.sha256`
- `publication_manifest.json`

## Run and checkpoint provenance

PERSONAL Windows post-training evidence for official H1 ORIENT-100 fresh 3K Run checkpoint model_2850.pt. Six qualitative terrain videos and a completed full camera-off scenario7 evaluation. Not an official score or a new training Run. The original archive evaluation source_run_id remains null; linkage to the official Run is by verified checkpoint SHA.

---

### 2026-10-07 당시 정책 행동 분석 — PERSONAL / HOLD

### 분석 원문 및 provenance

- **분석 원문:** [H1 ORIENT-100 model_2850 정책 분석](https://github.com/SE3C/naver-issacsim/blob/main/data/processed/incoming/other/reviewed/H1_ORIENT-100_POLICY_ANALYSIS_20261007.md)
- **Experiment:** [exp-h1-rough-terrain-orientation-relaxation](https://github.com/SE3C/naver-issacsim/blob/main/research/experiments/h1/exp-h1-rough-terrain-orientation-relaxation.md)
- **원본 OFFICIAL 학습 Release:** [ORIENT-100 fresh 3K](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261006-exp-h1-rough-terrain-orientation-relaxation-fresh3k)
- **학습 Run:** `20261006-133517-h1-orient-100-fresh3k-official`
- **평가 정책:** automatic-best `model_2850.pt` (마지막 보존 checkpoint `model_2950.pt`와 구분)
- **평가 metadata의 checkpoint SHA-256:** `6aedeced60562c1d496d5319d29b76cf9e26ff43df06827cb370f24f5313f7b0`
- 평가 ZIP 내부의 `source_run_id=null`은 수정하지 않는다. OFFICIAL Run 연결은 별도 학습 evidence와 checkpoint SHA를 근거로 한다.

### PERSONAL 평가 결과

- H1 camera-off `scenario7`: **8 case × 3 seed × 128 env = 3,072 episodes**
- **3,072/3,072 episodes가 20초 timeout까지 생존**
- `base_contact_failure`: **0건**
- 평지 전진 H2: body-forward 적분 **15.408m**
- 외란 H7: body-forward 적분 **10.530m**
- 정지 H1: 원치 않는 body-forward 적분 **+1.633m**
- 횡이동 H3: 원치 않는 body-forward 적분 **+1.180m**
- 거친 지형 H5: 평균 tracking error **0.1709**, 평균 진행 **9.451m**, 최소 진행 **7.831m**

### 영상 관찰 및 한계

- Boxes와 rough 지형의 초반 진행, 10° 경사 보행을 관찰했다.
- **중앙 다단 계단 완주는 입증되지 않았다.**
- `02_inverted_stairs.mp4`의 짝수 500개 검정 프레임은 **영상 캡처 결함**이며 정책 낙상으로 판정하지 않는다.
- 고정 6영상과 camera-off 평가는 서로 다른 명령·지형·episode 조건이므로 동일 평가로 합치지 않는다.

### 현재 판정

**PERSONAL 행동 후보: HOLD**

기본 전진과 외란 조건에서 의미 있는 보행을 보였으므로 REJECT하지 않고 비교 후보로 보존한다. 그러나 정지·횡이동 drift, rough 지형의 하위 성능 저하, 계단 완주 미입증 때문에 현재 대표 정책으로 PROMOTE하지 않는다.

**`h1-submit-2 / TERM-50`의 동일 조건 evaluator 대조군이 없으므로 `ORIENT-100` reward 변경의 인과적 개선 효과는 미검증이다.** 이 평가는 OFFICIAL 채점 결과, 제출 기록 또는 Optuna trial이 아니다.

위 대조군 부재와 다음 우선순위는 2026-10-07 보고서 당시의 한계다. 2026-10-10 후속 분석에서는 TERM-50 model_2800, ORIENT-100 model_2850, ACTRATE-0001 model_2700의 총 9,216개 원자료 행과 3,072개 대응 cohort key를 직접 비교했다. 세 정책 모두 HOLD이며, 대응 key만으로 실제 지형/reset/trajectory 동일성이나 reward 인과효과를 입증하지 않는다. 후속 기록: https://github.com/SE3C/naver-issacsim/blob/main/data/processed/experiments/h1/2026-10-10_H1_SCENARIO7_RAW_3POLICY_MATCHED_ANALYSIS.md

## Configuration and lineage

The display label is not a full resolved configuration. Configuration and lineage remain those of the original evidence; missing parameters or parent identities are not inferred.

## Canonical preservation and boundaries

Existing asset filenames and bytes remain unchanged. These are PERSONAL evidence/backup records, not an OFFICIAL competition score or a submission snapshot; original provenance and failed/interrupted evidence remain preserved.
