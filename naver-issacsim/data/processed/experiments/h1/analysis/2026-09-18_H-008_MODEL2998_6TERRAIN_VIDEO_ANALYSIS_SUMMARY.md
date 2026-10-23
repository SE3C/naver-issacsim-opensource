---
title: "H-008 model_2998 six-terrain video analysis summary"
environment: "PERSONAL / Brev L40S"
status: "hold_with_final_checkpoint_visual_evidence"
source_report: "data/processed/incoming/other/reviewed/2026-09-18_H008_H1_MODEL2998_6TERRAIN_VIDEO_ANALYSIS.md"
---

# [분석] H-008 — `model_2998` six-terrain video analysis summary

> 관리 안내 (2026-10-13): **분석** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](../../../../../research/EXPERIMENTS.md)를 확인한다.

> **2026-09-21 정정 · 상대 비교용 · 재실험 필요.** 개인 H-001 부모의 feet는 -0.2이며 공식 TERM50(+0.2)과 다르다. H-005/006은 feet -0.2→+.25/+.30, H-007/008은 feet -0.2→+.2와 track을 동시에 변경했다. H-009~011의 직접 부모 대비 단일변수 사실은 유효하지만 새 +0.2 부모 계보에서 재검증한다. 기존 COMPLETE와 수치는 보존하며 현재 판단은 HOLD다. [근거 및 재실험 계획](../2026-09-21_H1_PARENT_AIRTIME_LINEAGE_CORRECTION.md).

## Scope and provenance

The received report analyzes the separately received H-008 `model_2998` six-terrain video
collection. Its raw Markdown source is preserved byte-for-byte with SHA-256
`c3993ebc9da59a510eee57e676438f547da7a01825d4f4cb6d07ac73b8ca4328`.

All six SHA-256 values quoted in the report exactly match the H-008 video ZIP intake:
`boxes`, `stairs`, `inverted_stairs`, `random_rough`, `slope_up_10deg`, and
`slope_down_10deg`. They are each H.264, 1920×1080, 50 fps, 999 frames, and 19.98 seconds
(119.88 seconds total). The report's `(...1)` filename notation is an analysis-side name only;
the received ZIP contains the same bytes without that suffix.

The videos have no embedded checkpoint hash, command, or runtime metadata. Their association
with H-008 final `model_2998` is user-provided provenance, not independent cryptographic
checkpoint identification. This remains PERSONAL visual evidence, never OFFICIAL evidence.

## Reported visual and metric interpretation

The report describes continuous upright locomotion in all six single trajectories, terrain
entry/traversal behavior on stairs, inverted stairs, boxes, and random rough, and no observed
fall/reset over the recorded 119.88 seconds. It treats the boxes recovery observation as
qualitative evidence of recovery capability. Those are useful visual sanity checks, but one
trajectory per terrain cannot establish a fall rate, traversal success rate, terrain maximum,
or competition score.

It connects the videos to H-008's reported last-100 training values: terrain 5.423, XY error
0.3394, yaw error 1.3776, base-contact termination 30.68%, timeout 69.33%, episode length
763.0, and mean reward 4.212. This connection supports the final-checkpoint visual narrative;
it does not directly measure velocity tracking or yaw tracking in the videos.

## Decision and operational boundary

The report's checkpoint-level conclusion — use final `model_2998` as the representative H-008
policy — is consistent with the current final-numbered-checkpoint resume policy and with the
previous H-008 visual intake. It is **not** a promotion of the H-008 reward hypothesis:
H-008 remains **HOLD / rerun required** because feet and track changed together in
its historical branch. The plan uses a new +0.2 parent and unchanged resume control;
the old branch is not track-only causal evidence.

The report proposes further yaw, vx/vy, repeat-terrain, and push checks. Preserve these as
analysis limitations, not as a new PC tournament, multi-checkpoint comparison, or selector
workflow. The current official operational procedure remains final-checkpoint preservation,
one native play/export and download; shutdown requires a separate explicit user request.

## Sources

- [Raw received report](../../../incoming/other/reviewed/2026-09-18_H008_H1_MODEL2998_6TERRAIN_VIDEO_ANALYSIS.md)
- [H-008 video ZIP intake](../2026-09-18_H-008_MODEL2998_6TERRAIN_VIDEO_INTAKE.md)
- [Existing H-008 decision summary](../2026-09-17_H-008_PERSONAL_RESUME_FROM_H-001_1P5K_DEEP_ANALYSIS.md)
- [H-008 experiment record](../../../../../research/experiments/h1/H-008.md)
