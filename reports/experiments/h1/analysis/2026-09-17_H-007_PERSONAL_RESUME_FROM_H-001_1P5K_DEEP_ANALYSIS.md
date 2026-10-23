---
title: "H-007 personal resume decision"
environment: "PERSONAL / Brev L40S"
status: "hold_rerun_required"
source_report: "data/processed/incoming/other/reviewed/2026-09-17_H1_H007_LINTRACK100_FROM_H001_1P5K_DEEP_ANALYSIS.md"
---

> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/experiments/h1/analysis/2026-09-17_H-007_PERSONAL_RESUME_FROM_H-001_1P5K_DEEP_ANALYSIS.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.


# [분석] H-007 — PERSONAL resume +1.5K decision

> 관리 안내 (2026-10-13): **분석** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](<../../../../research/EXPERIMENTS.md>)를 확인한다.

> **2026-09-21 정정 · 상대 비교용 · 재실험 필요.** 개인 H-001 부모의 feet는 -0.2이며 공식 TERM50(+0.2)과 다르다. H-005/006은 feet -0.2→+.25/+.30, H-007/008은 feet -0.2→+.2와 track을 동시에 변경했다. H-009~011의 직접 부모 대비 단일변수 사실은 유효하지만 새 +0.2 부모 계보에서 재검증한다. 기존 COMPLETE와 수치는 보존하며 현재 판단은 HOLD다. 근거 및 재실험 계획〔원본 참조: `../2026-09-21_H1_PARENT_AIRTIME_LINEAGE_CORRECTION.md` / 공개 사본 미포함〕.

## Scope and provenance

This PERSONAL resume run changes feet_air_time -0.2→+0.2 AND `track_lin_vel_xy_exp` 0.5→1.0 from PERSONAL H-001
TERM50 `model_1499.pt` (SHA-256 `68fa0a9fe5334f8a3ecea110c4ccc9adb81ec07ac50169eaf8009b1a6e88f0c1`).
It ran from global step 1499 to 2998 with seed 42 and 4096 environments. Train and video
evidence validation passed; the report records 16 checkpoints, raw TensorBoard, no reported
NaN/Inf/OOM, and archive SHA-256 values `ebcf43a6…ae00bb` (train) and
`695e47d7…0b0cb7` (video). This is not OFFICIAL evidence.

## Result and decision

After curriculum reset, last-500 terrain was 5.372 and base-contact termination 30.62%; XY
error improved to 0.3386. The material trade-off is yaw: it rose to 2.008 in the last-500,
with worsening smoothness-related penalties. Full raw reward peaks at 1564, but the preserved
finalizer intentionally excludes the first `max(50, 10% of observed step range)` after resume.
For 1499→2998 the threshold is approximately 1648, so 1564 is ineligible and the reported
eligible peak at 1733 correctly maps to `model_best=model_1700`. This is not an unexplained
report mismatch. The one linked video still validates only model_1700, not later
2800/2900/2998 candidates.

Decision: **HOLD / 재실험 필요**. Historical values remain descriptive relative-comparison evidence. Rerun from the new +0.2 parent lineage with its unchanged control before adoption. H-007/008 additionally changed feet, so no track-only conclusion is supported. Final numbered checkpoints identify historical representative policies; they do not authorize final reward adoption.

## Current resume checkpoint policy

This analysis remains a `HOLD` for causal reward inference. The earlier multi-checkpoint
comparison recommendation is superseded operationally: use final `model_2998` unless the
final window jointly and clearly worsens in terrain, tracking, and falls, then make one native
play/export. Do not run a PC tournament or selector program.

## Sources

- [Raw received analysis](<../../../received/2026-09-17_H1_H007_LINTRACK100_FROM_H001_1P5K_DEEP_ANALYSIS.md>)
- [Train Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260917-002225-h1-lintrack-100-from-term-50-feet-minus-0.2-1p5k)
- [Video Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260917-004341-20260917-002225-h1-lintrack-100-from-term-50-feet-minus-0.2-1p)
- [Experiment registry](<../../../../research/experiments/h1/H-007.md>)
