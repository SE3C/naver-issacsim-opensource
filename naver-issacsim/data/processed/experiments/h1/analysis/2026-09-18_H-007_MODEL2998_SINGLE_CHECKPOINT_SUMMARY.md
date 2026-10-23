---
title: "H-007 model_2998 single-checkpoint analysis summary"
environment: "PERSONAL / Brev L40S"
status: "hold_with_final_checkpoint_visual_evidence"
source_report: "data/processed/incoming/other/reviewed/2026-09-18_H007_MODEL_2998_SINGLE_CHECKPOINT_ANALYSIS.md"
---

# [분석] H-007 — `model_2998` final-checkpoint summary

> 관리 안내 (2026-10-13): **분석** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](../../../../../research/EXPERIMENTS.md)를 확인한다.

> **2026-09-21 정정 · 상대 비교용 · 재실험 필요.** 개인 H-001 부모의 feet는 -0.2이며 공식 TERM50(+0.2)과 다르다. H-005/006은 feet -0.2→+.25/+.30, H-007/008은 feet -0.2→+.2와 track을 동시에 변경했다. H-009~011의 직접 부모 대비 단일변수 사실은 유효하지만 새 +0.2 부모 계보에서 재검증한다. 기존 COMPLETE와 수치는 보존하며 현재 판단은 HOLD다. [근거 및 재실험 계획](../2026-09-21_H1_PARENT_AIRTIME_LINEAGE_CORRECTION.md).

## Scope and provenance

The received report analyzes the final numbered checkpoint of the existing H-007 PERSONAL
resume run (H-001 `model_1499.pt` → global step 2998; seed 42; 4096 environments). Its raw
Markdown source is preserved byte-for-byte with SHA-256
`cd86e0d65b620f39561d473d58d3f2976a1c4139b3023ba55887796c3a76a76a`.

The report states that extracted `model_2998.pt` has SHA-256
`388ea635532d206049957518fb8f5fb73ff91da16dc9fa3017d7c8b41715767f`, iteration 2998,
and finite actor, critic, and optimizer tensors. This intake contains the report, not the
checkpoint or its source archive, so that checkpoint identity remains **report-derived** rather
than independently re-hashed here.

Its six listed MP4 SHA-256 values exactly match the separately received H-007 `model_2998`
six-terrain video collection. The MP4 files establish a visual sanity check; absent embedded
checkpoint identity or command/runtime metadata, their association with `model_2998` is the
provided provenance and not a cryptographic proof.

## Reported late-window evidence

The report's TensorBoard-derived final-window values are consistent with the existing H-007
interpretation: strong late linear-XY tracking with a material yaw trade-off.

| Metric | Step 2998 | Last 100 |
| --- | ---: | ---: |
| Terrain level | 5.3676 | 5.3725 |
| XY velocity error | 0.3155 | 0.3294 |
| Yaw error | 1.9820 | 2.0005 |
| Base-contact termination | 32.69% | 30.78% |
| Timeout | 67.31% | 69.23% |
| Episode length | 705.55 | 750.65 |

The report observes sustained upright movement in the six 19.98-second videos and a visible
recovery after a boxes-terrain disturbance. Those observations support gross locomotion and
recovery as qualitative evidence only; each terrain has one trajectory, so they do not define
a terrain success rate or competition score.

## Decision and operational boundary

`model_2998.pt` remains the representative H-007 checkpoint under the documented resume
policy: it is the final numbered checkpoint and the reported late window does not show a joint
terrain/tracking/fall collapse. H-007 remains **HOLD / rerun required**: its historical
branch changed both feet and track. The plan now uses a new +0.2 parent and unchanged
control; this collection cannot establish a track-only effect or an OFFICIAL claim.

The received report recommends a fixed evaluator and head-to-head comparison with
`model_2900`. That recommendation is historical report analysis, not the current operating
procedure: do not run a PC checkpoint tournament or build a selector. On an official server,
preserve the final checkpoint through the organizer-approved procedure, perform one native
play/export from that final checkpoint and download it. Server shutdown requires a separate explicit user request.

## Sources

- [Raw received report](../../../incoming/other/reviewed/2026-09-18_H007_MODEL_2998_SINGLE_CHECKPOINT_ANALYSIS.md)
- [Existing H-007 decision summary](../2026-09-17_H-007_PERSONAL_RESUME_FROM_H-001_1P5K_DEEP_ANALYSIS.md)
- [H-007 experiment record](../../../../../research/experiments/h1/H-007.md)
