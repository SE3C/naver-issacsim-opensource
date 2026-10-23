---
title: "H-008 personal resume decision"
environment: "PERSONAL / Brev L40S"
status: "hold_rerun_required"
source_report: "data/processed/incoming/other/reviewed/2026-09-17_H1_H008_LINTRACK075_FROM_H001_1P5K_DEEP_ANALYSIS.md"
---

> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/experiments/h1/analysis/2026-09-17_H-008_PERSONAL_RESUME_FROM_H-001_1P5K_DEEP_ANALYSIS.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.


# [분석] H-008 — PERSONAL resume +1.5K decision

> 관리 안내 (2026-10-13): **분석** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](<../../../../research/EXPERIMENTS.md>)를 확인한다.

> **2026-09-21 정정 · 상대 비교용 · 재실험 필요.** 개인 H-001 부모의 feet는 -0.2이며 공식 TERM50(+0.2)과 다르다. H-005/006은 feet -0.2→+.25/+.30, H-007/008은 feet -0.2→+.2와 track을 동시에 변경했다. H-009~011의 직접 부모 대비 단일변수 사실은 유효하지만 새 +0.2 부모 계보에서 재검증한다. 기존 COMPLETE와 수치는 보존하며 현재 판단은 HOLD다. 근거 및 재실험 계획〔원본 참조: `../2026-09-21_H1_PARENT_AIRTIME_LINEAGE_CORRECTION.md` / 공개 사본 미포함〕.

## Scope

This is PERSONAL resume/fine-tuning evidence, not OFFICIAL performance evidence or a
submission claim. It resumes PERSONAL H-001 model_1499.pt and changes feet_air_time -0.2→+0.2 AND track_lin_vel_xy_exp 0.5→0.75 for an additional 1,500 iterations.

## Provenance and integrity

- Parent checkpoint SHA-256: `68fa0a9fe5334f8a3ecea110c4ccc9adb81ec07ac50169eaf8009b1a6e88f0c1`
- Train archive SHA-256: `06f7d1dad5b492e701587009f46811e8aa8e7a4504fba4d92f763db6b7c388b5`
- Video archive SHA-256: `d78257b8bc2cb5352b1674c31fc04d961fc854f17a41fff512f5b4bb2e57dde6`
- Received-report SHA-256: `54769c474864c27269b5d8334ab2265df313d393e198cf93aeaa748d063707bb`

The run completed at global step 2998 with train and video evidence validation PASS. It
preserved 16 checkpoints, raw TensorBoard, source hashes, configuration, GPU telemetry, and
finite actor/critic/optimizer tensors. The report records no NaN, Inf, CUDA OOM, or optimizer
failure. This establishes a valid PERSONAL run, not an OFFICIAL score improvement.

## Evidence-backed behavior

The resume terrain reset from 3.438 to 3.136, then crossed the parent reference terrain
(5.119) at step 1739. Last-500 terrain was 5.423, base-contact termination 30.74%, XY error
0.3499, yaw error 1.426, and episode length 764.9. The defensible interpretation is that
linear XY tracking improved within the run without clear stability collapse, while yaw
tracking worsened relative to the post-reset early window.

`model_best.pt` is `model_1700.pt`. Full raw TensorBoard peaks at step 1545, but the preserved
finalizer excludes the first `max(50, 10% of observed step range)` after resume. For
1499→2998 the threshold is approximately 1648, so 1545 is ineligible and the eligible report
peak at 1711 correctly maps to `model_1700`. This is intentional warm-up filtering, not an
unexplained report mismatch. Because the video also uses `model_1700`, it cannot validate the
later 2800/2900/2998 checkpoints, which have stronger late terrain/XY metrics.

## Decision

Decision: **HOLD / 재실험 필요**. Historical values remain descriptive relative-comparison evidence. Rerun from the new +0.2 parent lineage with its unchanged control before adoption. H-007/008 additionally changed feet, so no track-only conclusion is supported. Final numbered checkpoints identify historical representative policies; they do not authorize final reward adoption.

## Current resume checkpoint policy

H-008 remains a `HOLD` for causal reward inference, but its representative policy is final
`model_2998`. The final window maintains terrain and XY tracking without a joint
terrain/tracking/fall collapse. Preserve it, make one native play/export, and download; server shutdown requires a separate explicit user request;
do not run a PC tournament or selector program.

## Sources

- [Raw received analysis](<../../../received/2026-09-17_H1_H008_LINTRACK075_FROM_H001_1P5K_DEEP_ANALYSIS.md>)
- [Train Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260917-004530-h1-lintrack-075-from-term-50-feet-minus-0.2-1p5k)
- [Video Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260917-010854-20260917-004530-h1-lintrack-075-from-term-50-feet-minus-0.2-1p)
- [Experiment registry](<../../../../research/experiments/h1/H-008.md>)
