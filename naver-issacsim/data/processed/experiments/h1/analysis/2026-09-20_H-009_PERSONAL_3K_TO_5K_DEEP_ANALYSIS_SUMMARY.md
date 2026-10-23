---
title: "H-009 PERSONAL 3K→5K deep-analysis summary"
environment: "PERSONAL / NVIDIA L40S"
status: "completed_run_hold_decision"
source: "data/processed/incoming/other/reviewed/H1_H009_HIPDEV030_FROM_H008_3K_DEEP_ANALYSIS_20260920.md"
source_sha256: "e6d836fd550930de411d9ac86b7b06de18ded8fb235ec7c2fe0b4d8e3a131c39"
---

# [분석] H-009 — PERSONAL 3K→5K 분석 요약

> 관리 안내 (2026-10-13): **분석** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](../../../../../research/EXPERIMENTS.md)를 확인한다.

> **2026-09-21 정정 · 상대 비교용 · 재실험 필요.** 개인 H-001 부모의 feet는 -0.2이며 공식 TERM50(+0.2)과 다르다. H-005/006은 feet -0.2→+.25/+.30, H-007/008은 feet -0.2→+.2와 track을 동시에 변경했다. H-009~011의 직접 부모 대비 단일변수 사실은 유효하지만 새 +0.2 부모 계보에서 재검증한다. 기존 COMPLETE와 수치는 보존하며 현재 판단은 HOLD다. [근거 및 재실험 계획](../2026-09-21_H1_PARENT_AIRTIME_LINEAGE_CORRECTION.md).

## 원문과 검증 경계

수신 원문은 H-009 archive의 raw TensorBoard·console·config·source·checkpoint·telemetry를 직접 분석했다고 기록한다. 원문은 [reviewed incoming](../../../incoming/other/reviewed/H1_H009_HIPDEV030_FROM_H008_3K_DEEP_ANALYSIS_20260920.md)에 byte-for-byte 보존했고 SHA-256은 `e6d836fd…1c39`다.

원문이 참조하는 `h009_report_assets/`의 그래프 PNG 4개는 함께 수신되지 않았다. 원문 링크는 보존하지만 이 저장소에서 이미지를 직접 확인한 것으로 취급하지 않는다.

보고서가 인용한 PERSONAL Release archive `20260918-010042-h1-h009-hipdev030-from-h008-3k.tar.gz`의 GitHub asset digest와 크기는 원격에서 `16f98464…abe7`, 153,929,548 bytes로 대조했다. `SHA256SUMS` 43/43, TensorBoard 수치·checkpoint tensor 검사·provenance 판독은 이 intake에서 archive를 다시 추출해 재계산한 것이 아니라 **수신 원문의 direct-analysis 결과**다.

## 확인된 Run 정체성

| 항목 | 결과 |
| --- | --- |
| Environment | PERSONAL / NVIDIA L40S |
| Parent | H-008 3K `model_2998.pt`, SHA `d9a30c8a…1912ae` |
| Delta | `joint_deviation_hip -0.20 → -0.30` only |
| Seed / envs | 42 / 4096 |
| Length | +2,000, global 2998→4997 |
| Execution / evidence | exit 0 / validation PASS |
| Retained checkpoints | 21, `model_3000`…`model_4997` |
| Final representative | `model_4997.pt` |
| Classification | PERSONAL; OFFICIAL score or submission evidence 아님 |

## 결과와 해석

- Numerical health는 양호하다. report 기준 TensorBoard 2,000 point, NaN/Inf/OOM/broken pipe 없음, 21 checkpoint actor·critic·optimizer finite, value loss median `0.00648`, max `0.02532`(resume 첫 step)이다.
- resume 직후 terrain은 약 3.44→3.17로 낮아졌지만 rolling-50이 global 3275에 5.5를 넘고 후반 high-terrain regime을 유지했다. 이를 parent 능력 상실로 읽지 않는다.
- last-500은 terrain `5.596`, XY error `0.3278`, yaw error `1.3085`, base-contact `29.99%`, timeout `70.03%`, episode length `770.4`다. 후반 terrain·tracking·fall이 함께 붕괴하지 않아 final `model_4997`이 대표 checkpoint다.
- unchanged H-008 +2K control의 기록값(terrain `5.604`, XY `0.3314`, base-contact `29.67%`)과 비교하면 H-009 차이는 XY `-0.0036`, terrain `-0.008`, base-contact `+0.32%p`다. control raw event를 동일 방식으로 재분석하지 않았고 terrain realization 차이도 가능하므로, hip `-0.30`의 우월성으로 선언하지 않는다.
- yaw error가 계속 큰 병목이며 hip penalty 강화가 이를 해결했다는 근거는 없다.

## 자동 best와 영상 경계

`model_best.pt`는 `model_3600.pt`와 hash가 같다. Full raw event 최고 reward는 global 3041이지만, finalizer는 관측 범위 2998→4997에서 `lo + max(50, floor(range×10%))`, 즉 약 3197 이전을 resume warm-up으로 제외하므로 3041은 자동 best 후보가 아니다. Report의 eligible peak `5.736 @3627`과 `model_3600` 선택은 이 규칙과 모순되지 않는다. 다만 자동 reward best와 대표 정책은 별개이므로 final numbered checkpoint를 기본으로 한다.

이 archive의 `policy.pt`, `policy.onnx`, `play_video.mp4`는 provenance상 이번 H-009에서 새로 만들어진 파일이 아니라 **UNCHANGED** artifact다. 따라서 H-009 행동·gait·terrain traversal·recovery의 영상 근거로 사용하지 않는다.

## 결정

**HOLD / 재실험 필요.** `-0.30`은 catastrophic regression 없이 parent regime을 유지했지만 의미 있는 aggregate gain·yaw 개선·fresh video·multi-seed·official 근거가 없다. 당시 제안한 H-011은 이후 완료되었다. 현재 계획은 새 +0.2 부모 계보의 H-008 3K에서 H-009~H-011과 unchanged control을 다시 검증하는 것이다.
