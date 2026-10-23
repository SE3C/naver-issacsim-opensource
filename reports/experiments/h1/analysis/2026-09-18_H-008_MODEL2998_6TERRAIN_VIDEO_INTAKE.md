---
title: "H-008 model_2998 six-terrain video intake"
environment: "PERSONAL / Brev L40S (associated H-008 run)"
status: "verified_video_only_local_intake"
source_zip: "Downloads/H-0008 model 2998.zip"
---

> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/experiments/h1/analysis/2026-09-18_H-008_MODEL2998_6TERRAIN_VIDEO_INTAKE.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.


# [분석] H-008 — `model_2998` six-terrain video intake

> 관리 안내 (2026-10-13): **분석** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](<../../../../research/EXPERIMENTS.md>)를 확인한다.

> **2026-09-21 정정 · 상대 비교용 · 재실험 필요.** 개인 H-001 부모의 feet는 -0.2이며 공식 TERM50(+0.2)과 다르다. H-005/006은 feet -0.2→+.25/+.30, H-007/008은 feet -0.2→+.2와 track을 동시에 변경했다. H-009~011의 직접 부모 대비 단일변수 사실은 유효하지만 새 +0.2 부모 계보에서 재검증한다. 기존 COMPLETE와 수치는 보존하며 현재 판단은 HOLD다. 근거 및 재실험 계획〔원본 참조: `../2026-09-21_H1_PARENT_AIRTIME_LINEAGE_CORRECTION.md` / 공개 사본 미포함〕.

## Scope and provenance

This is a user-supplied, post-train video-only collection identified as H-008
`model_2998.pt` output. It is associated with the existing PERSONAL H-008 resume evidence,
not with an OFFICIAL run or submission. The ZIP contains no checkpoint bytes, train archive,
console log, command, runtime metadata, or source-checkpoint hash; it therefore does not
independently prove checkpoint identity or alter H-008's `HOLD` causal decision.

- Received ZIP SHA-256: `ef43bc9edbc367712e77cc1a74b8d0a0ad2c9d9f347ac4009e0bd3378b222aef`
- Layout: one `H-0008 model 2998/` directory containing exactly six MP4 files
- Association: H-008 PERSONAL resume from H-001 `model_1499.pt`, global iterations 1499–2998

## Media validation

Every file is H.264, 1920×1080, 50 fps, 999 frames, and 19.98 seconds. These are native-play
visual sanity-check materials for the final representative checkpoint, not a replacement for
the train evidence or a quantitative evaluator.

| Terrain video | Bytes | SHA-256 |
| --- | ---: | --- |
| `boxes.mp4` | 6,299,569 | `ecf4fce93443e520cc80d4ec973cb0cb03612b3166391cba42314de1d30306c3` |
| `inverted_stairs.mp4` | 6,618,375 | `682a008e4379fd62b7ca5807db451838d41e00aa0a9daf1eb0e9bda3a9ad13ba` |
| `random_rough.mp4` | 10,537,566 | `024fe82d303e7605181e98b3a55b5e60803c3d3dbf866dba4d439823f8b0b572` |
| `slope_down_10deg.mp4` | 6,043,409 | `071d9b7c6ad6a0880ec6f4c231afe22e36f06c41ac8c0c2e37e48bf90c512d53` |
| `slope_up_10deg.mp4` | 5,532,745 | `f12470ca802d56e7235c4d039fbaeba3a82bcd3dede6522d3218276177ec1b82` |
| `stairs.mp4` | 6,059,523 | `0d3f23ca0cebba99cd5bcbacbe11680ed127b818ba0f219df173a493432822c3` |

## Interpretation boundary

H-008's previous native video Release validates only automatic `model_1700`. This collection
addresses the documented need for one visual check of the final `model_2998` representative
checkpoint. It does not establish a reward-effect comparison, a terrain-score improvement, or
an OFFICIAL claim. The historical branch changed feet and track together. The next
planned experiment uses the new +0.2 parent with an unchanged resume control; this
collection remains relative-comparison evidence pending that rerun.

## Source links

- [H-008 experiment record](<../../../../research/experiments/h1/H-008.md>)
- H-008 processed decision〔원본 참조: `../2026-09-17_H-008_PERSONAL_RESUME_FROM_H-001_1P5K_DEEP_ANALYSIS.md` / 공개 사본 미포함〕
- [H-008 PERSONAL train Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260917-004530-h1-lintrack-075-from-term-50-feet-minus-0.2-1p5k)
