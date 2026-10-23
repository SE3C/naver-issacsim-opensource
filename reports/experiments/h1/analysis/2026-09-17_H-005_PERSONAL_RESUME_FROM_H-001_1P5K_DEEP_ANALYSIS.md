---
title: "H-005 personal resume decision"
environment: "PERSONAL / Brev L40S"
status: "hold_rerun_required"
source_report: "data/processed/incoming/other/reviewed/2026-09-17_H1_H005_GAIT025_FROM_H001_1P5K_DEEP_ANALYSIS.md"
---

> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/experiments/h1/analysis/2026-09-17_H-005_PERSONAL_RESUME_FROM_H-001_1P5K_DEEP_ANALYSIS.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.


# [분석] H-005 — PERSONAL resume +1.5K decision

> 관리 안내 (2026-10-13): **분석** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](<../../../../research/EXPERIMENTS.md>)를 확인한다.

> **2026-09-21 정정 · 상대 비교용 · 재실험 필요.** 개인 H-001 부모의 feet는 -0.2이며 공식 TERM50(+0.2)과 다르다. H-005/006은 feet -0.2→+.25/+.30, H-007/008은 feet -0.2→+.2와 track을 동시에 변경했다. H-009~011의 직접 부모 대비 단일변수 사실은 유효하지만 새 +0.2 부모 계보에서 재검증한다. 기존 COMPLETE와 수치는 보존하며 현재 판단은 HOLD다. 근거 및 재실험 계획〔원본 참조: `../2026-09-21_H1_PARENT_AIRTIME_LINEAGE_CORRECTION.md` / 공개 사본 미포함〕.

## Scope and provenance

This PERSONAL resume run changes only `feet_air_time` from -0.20 to 0.25 from H-001 TERM50
`model_1499.pt` (SHA-256 `68fa0a9fe5334f8a3ecea110c4ccc9adb81ec07ac50169eaf8009b1a6e88f0c1`).
It ran from global step 1499 to 2998 with seed 42 and 4096 environments. Train and video
evidence validation passed; the report records 16 checkpoints, raw TensorBoard, no reported
NaN/Inf/OOM, and archive SHA-256 values `6137bea5…8ebf35` (train) and
`d0c823eb…a07754` (video). This is not OFFICIAL evidence.

## Result and decision

After curriculum reset, terrain passed the parent reference at step 1760 and reached late-300
terrain 5.422. Late base-contact termination was about 30.5%, XY error 0.373, and yaw error
1.029. `model_best` equals final `model_2998`, but reward-best is not necessarily
tracking-best. The linked single video is a locomotion sanity check only.

Decision: **HOLD / 재실험 필요**. Historical values remain descriptive relative-comparison evidence. Rerun from the new +0.2 parent lineage with its unchanged control before adoption. H-007/008 additionally changed feet, so no track-only conclusion is supported. Final numbered checkpoints identify historical representative policies; they do not authorize final reward adoption.

## Current resume checkpoint policy

This analysis remains a `HOLD` for causal reward inference. Separately, the operational policy
uses final `model_2998` as the representative resume policy because its final window has no
joint terrain/tracking/fall collapse. Do one native play/export from that checkpoint; do not
run a PC tournament or multi-checkpoint selector.

## Sources

- [Raw received analysis](<../../../received/2026-09-17_H1_H005_GAIT025_FROM_H001_1P5K_DEEP_ANALYSIS.md>)
- [Train Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260916-233344-h1-airtime-025-from-term-50-feet-minus-0.2-1p5k)
- [Video Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260916-235551-20260916-233344-h1-airtime-025-from-term-50-feet-minus-0.2-1p5k-v)
- [Experiment registry](<../../../../research/experiments/h1/H-005.md>)
