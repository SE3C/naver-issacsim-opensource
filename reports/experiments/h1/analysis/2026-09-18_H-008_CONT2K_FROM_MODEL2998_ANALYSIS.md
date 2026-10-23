---
title: "H-008 3K→5K PERSONAL continuation analysis"
purpose: "canonical archive verification, continuation interpretation, and checkpoint-selection boundary"
sources:
  - "naver-issacsim-originals/data/raw/private_server_runs/h1/2026-09-18_h008_cont2k_from_model2998/"
  - "https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/20260917-234047-h1-lintrack-075-cont2k-from-2998"
  - "data/processed/experiments/h1/2026-09-17_H-008_PERSONAL_RESUME_FROM_H-001_1P5K_DEEP_ANALYSIS.md"
type: "personal_training_evidence_analysis"
---

> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/experiments/h1/analysis/2026-09-18_H-008_CONT2K_FROM_MODEL2998_ANALYSIS.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.


# [분석] H-008 — 3K→5K PERSONAL continuation

> 관리 안내 (2026-10-13): **분석** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](<../../../../research/EXPERIMENTS.md>)를 확인한다.

> **2026-09-21 정정 · 상대 비교용 · 재실험 필요.** 개인 H-001 부모의 feet는 -0.2이며 공식 TERM50(+0.2)과 다르다. H-005/006은 feet -0.2→+.25/+.30, H-007/008은 feet -0.2→+.2와 track을 동시에 변경했다. H-009~011의 직접 부모 대비 단일변수 사실은 유효하지만 새 +0.2 부모 계보에서 재검증한다. 기존 COMPLETE와 수치는 보존하며 현재 판단은 HOLD다. 근거 및 재실험 계획〔원본 참조: `../2026-09-21_H1_PARENT_AIRTIME_LINEAGE_CORRECTION.md` / 공개 사본 미포함〕.

## 판정

H-008 3K final `model_2998.pt`에서 reward를 바꾸지 않고 추가 2,000 iteration을 수행한
PERSONAL continuation은 console global 2998~4997까지 exit code 0으로 완료됐다. archive outer
SHA-256과 internal `SHA256SUMS` 41/41이 일치하고, TensorBoard·console·21개 numbered checkpoint가
보존됐다. 다만 실행은 profile-aware `train`이 아닌 generic `issacsimz run`이어서 canonical
metadata의 `profile`, `source_checkpoint`, `resume_lineage`가 null이며 `validation.json= WARN`이다.
post-run provenance archive는 parent/final hash를 보강하지만 execution-time provenance를 대체하지
않는다.

이는 PERSONAL continuation evidence이지 OFFICIAL performance, submission, 또는 reward effect의
인과 증거가 아니다. H-009/H-010의 부모는 이 run의 5K final이 아니라 기존 H-008 3K
`model_2998.pt`다.

## Identity and integrity

| Item | Verified value |
| --- | --- |
| Parent | H-008 3K `model_2998.pt` |
| Parent SHA-256 | `d9a30c8a117f69cac49c4e640500f0fa8d88de72d6c61855f1e147ea6c1912ae` |
| Requested / actual | +2,000 / global 2998~4997 |
| Environment | PERSONAL Brev L40S, seed 42, 4096 env |
| Canonical archive | 153,896,399 bytes; SHA-256 `b669bf1b90a67a4468e6851ab237538bbab6450144b3e4f5e9eecbfeb6777d9e` |
| Archive verification | outer sidecar and Release digest match; internal `SHA256SUMS` 41/41 pass |
| Checkpoints | 21: `model_3000.pt`~`model_4900.pt` plus final `model_4997.pt` |
| Final checkpoint | `model_4997.pt`, 7,151,477 bytes, SHA-256 `e6deed62c1dfff4d5bdaac4cf77ee7308f91f04f9ea6db32a8f80f3e5db922a2` |
| Validation | WARN: generic run lacks execution-time profile/source/lineage identity |

The effective H-008 config in collected `env.yaml` is unchanged: `track_lin_vel_xy_exp=0.75`,
`feet_air_time=0.20`, `termination_penalty=-50`, and `joint_deviation_hip=-0.20`.

## Late training evidence

The following values are console-derived rounded scalar averages; they are useful trend evidence,
not an OFFICIAL evaluator or a replay benchmark.

| Window | Terrain | XY error | Yaw error | Base-contact | Timeout | Episode length |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| First 200 (2998~3197) | 4.248 | 0.3169 | 1.2593 | 20.18% | 70.21% | 746.90 |
| Last 500 (4498~4997) | 5.604 | 0.3314 | 1.3769 | 29.67% | 70.35% | 776.28 |
| Last 200 (4798~4997) | 5.599 | 0.3344 | 1.3818 | 28.65% | 71.36% | 788.89 |
| Endpoint 4997 | 5.689 | 0.3200 | 1.3230 | 29.41% | 70.59% | 772.78 |

Against H-008 Run 01's last-500 terrain 5.423, XY 0.3499, yaw 1.426, and base-contact 30.74%,
the continuation's late console windows are directionally compatible with retained terrain and
tracking rather than a joint late collapse. Because both are PERSONAL training traces and no
matched unchanged control/evaluator is present, this does not establish a reward-effect or score
improvement.

## Checkpoint choice and limitation

Native finalize chose automatic `model_best.pt = model_4900.pt` using a reported reward peak at
step 4911. The rounded console rows show a higher displayed mean reward near iteration 3042,
but the native resume selector excludes steps before about 3197 for the 2998→4997 range. The
early console high is therefore outside the eligible window and does not contradict the report.
This remains another reason not to equate automatic `model_best` with locomotion quality.

Under the established resume policy, use final numbered `model_4997.pt` as the representative
checkpoint unless terrain, tracking, and falls jointly deteriorate in the late window. That
joint deterioration is not visible in the retained console endpoint/late windows. A fresh native
play/export tied to `model_4997` would provide the missing visual sanity evidence; it is not
present in this Release.

## Storage and Release layout

The immutable canonical archive and its received sidecars are preserved under
`naver-issacsim-originals/data/raw/private_server_runs/h1/2026-09-18_h008_cont2k_from_model2998/`.
The NVIDIA Release exposes them as audit evidence and separately provides
`H-008_LINTRACK075_PERSONAL_5K_DOWNLOAD.tar.gz`, a derived handoff with only final `model_4997`,
matching `env.yaml`, `report.html`, and a manifest. The handoff does not replace canonical
evidence or carry an OFFICIAL claim.
