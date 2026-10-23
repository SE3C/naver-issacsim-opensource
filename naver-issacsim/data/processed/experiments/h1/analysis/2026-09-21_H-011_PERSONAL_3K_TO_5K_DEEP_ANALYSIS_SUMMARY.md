---
title: "H-011 PERSONAL 3K→5K deep-analysis summary"
environment: "PERSONAL / NVIDIA L40S"
status: "completed_run_hold_decision"
source: "data/processed/incoming/other/reviewed/H1_H011_HIPDEV010_MODEL4997_DEEP_ANALYSIS.md"
source_sha256: "4e1d3e31a8b3a5e3b4bd57c85ef61fc5d28a61ac3ad44b33dac432c4a32b7f01"
---

# [분석] H-011 — PERSONAL 3K→5K 분석 요약

> 관리 안내 (2026-10-13): **분석** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](../../../../../research/EXPERIMENTS.md)를 확인한다.

> **2026-09-21 정정 · 상대 비교용 · 재실험 필요.** 개인 H-001 부모의 feet는 -0.2이며 공식 TERM50(+0.2)과 다르다. H-005/006은 feet -0.2→+.25/+.30, H-007/008은 feet -0.2→+.2와 track을 동시에 변경했다. H-009~011의 직접 부모 대비 단일변수 사실은 유효하지만 새 +0.2 부모 계보에서 재검증한다. 기존 COMPLETE와 수치는 보존하며 현재 판단은 HOLD다. [근거 및 재실험 계획](../2026-09-21_H1_PARENT_AIRTIME_LINEAGE_CORRECTION.md).

## 원문과 검증 경계

수신 원문은 train archive와 별도 6-terrain video suite를 직접 분석한 보고서다. 원문은 [reviewed incoming](../../../incoming/other/reviewed/H1_H011_HIPDEV010_MODEL4997_DEEP_ANALYSIS.md)에 byte-for-byte 보존했고 SHA-256은 `4e1d3e31…7f01`이다.

이번 intake에서는 보고서 파일의 보존 hash와 프로젝트 계보를 확인했다. 아래 TensorBoard 수치, archive 내부 checksum, checkpoint tensor 및 영상 판독은 archive를 다시 추출해 독립 재계산한 값이 아니라 **수신 원문의 direct-analysis 결과**다.

## 확인된 Run 정체성

| 항목 | 결과 |
| --- | --- |
| Run ID | `20260920-150652-h1-h011-hipdev010` |
| Environment | PERSONAL / Brev NVIDIA L40S |
| Parent | H-008 3K final `model_2998.pt`, SHA `d9a30c8a…1912ae` |
| Delta | `joint_deviation_hip -0.20 → -0.10` only |
| Seed / envs | 42 / 4096 |
| Length | +2,000, global 2998→4997 |
| Execution / evidence | exit 0 / validation PASS |
| Retained checkpoints | 21, `model_3000`…`model_4900` plus `model_4997` |
| Final representative | `model_4997.pt` |
| Classification | PERSONAL; OFFICIAL evaluator/score evidence 아님 |

## 결과와 해석

- Resume transient 뒤 global 약 3.2K~3.5K부터 고지형 plateau에 진입했다. 후반 300회는 terrain `5.661`, XY error `0.3304`, yaw error `1.411`, base-contact `29.02%`, timeout `70.99%`, episode length `780.24`다.
- Unchanged H-008 +2K control 요약(terrain `5.604`, XY `0.3314`, base-contact `29.67%`)과 차이가 매우 작다. `joint_deviation_hip=-0.10`의 명확한 tracking/stability 이득으로 선언하지 않는다.
- Yaw error는 endpoint `1.445`, max `1.639 @ 4546`으로 기존 병목을 해소하지 못했다. 반면 NaN/Inf/OOM/optimizer failure 없이 PPO 수치 안정성은 양호하다.
- Raw reward 최고 `6.886 @ 3084`는 resume 첫 10% warm-up 제외 구간이다. Report의 `6.184 @ 3203 → model_3200`은 제외 규칙과 일치한다.
- 자동 `model_best`보다 final `model_4997`이 run의 장기 학습 상태를 대표한다. 6-terrain 영상은 정성 sanity evidence일 뿐 성공률·tracking 측정·공식 평가 또는 self-contained checkpoint provenance가 아니다.

## 결정

**HOLD.** 실패 정책은 아니지만 `-0.10`의 우월성도 입증하지 못했다. H-009 `-0.30`, unchanged control `-0.20`, H-011 `-0.10`을 같은-parent 3점 비교로 해석하되 현재 자료만으로 hip penalty 방향을 확정하지 않는다.
