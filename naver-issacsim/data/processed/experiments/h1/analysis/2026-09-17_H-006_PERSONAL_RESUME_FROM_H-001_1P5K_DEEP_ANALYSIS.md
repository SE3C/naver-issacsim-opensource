---
title: "H-006 personal resume decision"
environment: "PERSONAL / Brev L40S"
status: "hold_rerun_required"
source_report: "data/processed/incoming/other/reviewed/2026-09-17_H1_H006_GAIT030_FROM_H001_1P5K_DEEP_ANALYSIS.md"
---

# [분석] H-006 — PERSONAL resume +1.5K decision

> 관리 안내 (2026-10-13): **분석** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](../../../../../research/EXPERIMENTS.md)를 확인한다.

> **2026-09-21 정정 · 상대 비교용 · 재실험 필요.** 개인 H-001 부모의 feet는 -0.2이며 공식 TERM50(+0.2)과 다르다. H-005/006은 feet -0.2→+.25/+.30, H-007/008은 feet -0.2→+.2와 track을 동시에 변경했다. H-009~011의 직접 부모 대비 단일변수 사실은 유효하지만 새 +0.2 부모 계보에서 재검증한다. 기존 COMPLETE와 수치는 보존하며 현재 판단은 HOLD다. [근거 및 재실험 계획](../2026-09-21_H1_PARENT_AIRTIME_LINEAGE_CORRECTION.md).

## Scope

This is PERSONAL resume/fine-tuning evidence, not OFFICIAL performance evidence and not a
submission claim. It resumes H-001 TERM50 `model_1499.pt` and changes only
`feet_air_time` from -0.20 to 0.30 for an additional 1,500 iterations.

## Provenance and integrity

- Parent checkpoint SHA-256: `68fa0a9fe5334f8a3ecea110c4ccc9adb81ec07ac50169eaf8009b1a6e88f0c1`
- Train archive SHA-256: `eda221a1a6fe5c16e79ea6401d085c973eaa210e422e3444fdaf92e2da6d197d`
- Video archive SHA-256: `17e776120fa35d2220b51b65b1ca75b0e921c3ab514610a521a395f56d522ea1`
- Received-report SHA-256: `76e57462589425ce5cb354c57465a6802fe6266e551f8893836da6866f1efe58`

The run completed at global step 2998 with exit code 0. The report records evidence
validation PASS for train and video, 16 checkpoints, raw TensorBoard, settings, source
hashes, GPU telemetry, no reported NaN/Inf/OOM/traceback, and stable PPO value loss. These
facts establish a valid PERSONAL run; they do not establish an OFFICIAL score improvement.

## Evidence-backed behavior

The resume reset terrain from 3.438 to a minimum of 3.135 at step 1516, then reacquired the
parent terrain reference (5.119) at step 1757. Last-300 metrics were terrain 5.469,
base-contact termination 29.93%, XY error 0.3713, yaw error 1.0249, and episode length
774.2. The most accurate characterization is tracking and curriculum progression improving
while stability remains approximately flat around 30% base-contact termination.

`model_best.pt` is `model_2700.pt`, selected near reward peak step 2670. Reported
trailing-window comparisons make `model_2900` (terrain/yaw) and `model_2998` (late balance)
credible alternatives, so automatic `model_best` is not a final policy-selection result. The
linked 19.98-second native play video validates only `model_2700`; it is not a fixed
terrain-by-terrain or official evaluator test.

## Decision

Decision: **HOLD / 재실험 필요**. Historical values remain descriptive relative-comparison evidence. Rerun from the new +0.2 parent lineage with its unchanged control before adoption. H-007/008 additionally changed feet, so no track-only conclusion is supported. Final numbered checkpoints identify historical representative policies; they do not authorize final reward adoption.

## Current resume checkpoint policy

This analysis remains a `HOLD` for causal reward inference. The earlier multi-checkpoint
comparison recommendation is superseded operationally: use final `model_2998` unless the
final window jointly and clearly worsens in terrain, tracking, and falls, then make one native
play/export. Do not run a PC tournament or selector program.

## Sources

- [Raw received analysis](../../../incoming/other/reviewed/2026-09-17_H1_H006_GAIT030_FROM_H001_1P5K_DEEP_ANALYSIS.md)
- [Train Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260916-235914-h1-airtime-030-from-term-50-feet-minus-0.2-1p5k)
- [Video Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260917-002012-20260916-235914-h1-airtime-030-from-term-50-feet-minus-0.2-1p5k-v)
- [Experiment registry](../../../../../research/experiments/h1/H-006.md)
