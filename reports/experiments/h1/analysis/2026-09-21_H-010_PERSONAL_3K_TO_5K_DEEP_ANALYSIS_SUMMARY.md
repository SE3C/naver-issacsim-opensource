---
title: "H-010 PERSONAL 3K→5K deep-analysis summary"
environment: "PERSONAL / NVIDIA L40S"
status: "completed_run_hold_decision"
source: "data/processed/incoming/other/reviewed/H1_H010_AIRTIME025_3K_TO_5K_DEEP_ANALYSIS_REVISED.md"
source_sha256: "13a45b8c7cdb776e425e7b3f82a11abba101a236240eccbb815468a6d802a98a"
---

> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/experiments/h1/analysis/2026-09-21_H-010_PERSONAL_3K_TO_5K_DEEP_ANALYSIS_SUMMARY.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.


# [분석] H-010 — PERSONAL 3K→5K 분석 요약

> 관리 안내 (2026-10-13): **분석** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](<../../../../research/EXPERIMENTS.md>)를 확인한다.

> **2026-09-21 정정 · 상대 비교용 · 재실험 필요.** 개인 H-001 부모의 feet는 -0.2이며 공식 TERM50(+0.2)과 다르다. H-005/006은 feet -0.2→+.25/+.30, H-007/008은 feet -0.2→+.2와 track을 동시에 변경했다. H-009~011의 직접 부모 대비 단일변수 사실은 유효하지만 새 +0.2 부모 계보에서 재검증한다. 기존 COMPLETE와 수치는 보존하며 현재 판단은 HOLD다. 근거 및 재실험 계획〔원본 참조: `../2026-09-21_H1_PARENT_AIRTIME_LINEAGE_CORRECTION.md` / 공개 사본 미포함〕.

## 원문과 검증 경계

수신 원문은 train archive와 별도 6-terrain video suite를 직접 분석한 보고서다. 원문은 [reviewed incoming](<../../../received/H1_H010_AIRTIME025_3K_TO_5K_DEEP_ANALYSIS_REVISED.md>)에 byte-for-byte 보존했고 SHA-256은 `13a45b8c…a98a`다.

이번 intake에서는 보고서 파일의 보존 hash와 프로젝트 계보를 확인했다. 아래 TensorBoard 수치, archive 내부 checksum, checkpoint tensor 및 영상 판독은 archive를 다시 추출해 독립 재계산한 값이 아니라 **수신 원문의 direct-analysis 결과**다.

## 확인된 Run 정체성

| 항목 | 결과 |
| --- | --- |
| Run ID | `20260920-134309-h1-h010-airtime025-rerun` |
| Environment | PERSONAL / Brev NVIDIA L40S |
| Parent | H-008 3K final `model_2998.pt`, SHA `d9a30c8a…1912ae` |
| Delta | `feet_air_time 0.20 → 0.25` only |
| Seed / envs | 42 / 4096 |
| Length | +2,000, global 2998→4997 |
| Execution / evidence | exit 0 / validation PASS |
| Retained checkpoints | 21, `model_3000`…`model_4900` plus `model_4997` |
| Final representative | `model_4997.pt` |
| Classification | PERSONAL; OFFICIAL evaluator/score evidence 아님 |

## 결과와 해석

- Resume 직후 재적응 뒤 terrain이 다시 상승했으며, last-500은 terrain `5.663`, XY error `0.3318`, yaw error `1.4187`, base-contact `29.63%`, episode length `773.65`다. 후기 terrain·tracking·fall의 공동 붕괴는 보고되지 않았다.
- 같은 H-008 `model_2998`에서 reward 변경 없이 +2K 진행한 control 요약(terrain `5.604`, XY `0.3314`, base-contact `29.67%`)과 사실상 같은 범위다. `feet_air_time=0.25`의 유의미한 우월성으로 읽지 않는다.
- Raw reward 최고 `6.585 @ 3044`는 resume 첫 10% warm-up 제외 구간이다. Eligible 최고 `5.7828 @ 3299`와 report의 `5.783 @ 3299 → model_3300`은 일치한다.
- 자동 `model_best`는 training-reward selector일 뿐 대표 정책을 뜻하지 않는다. 충분히 긴 resume이고 후반 공동 붕괴가 없어 final `model_4997`을 대표 checkpoint로 유지한다.
- 6-terrain 영상은 upright locomotion의 정성 sanity 근거다. 단일 19.98초 trajectory이며 bundle 안에 checkpoint bytes/hash가 없어 성공률·공식 성능 또는 암호학적으로 self-contained한 checkpoint provenance로 사용하지 않는다.

## 결정

**HOLD.** 학습은 안정적이고 명백한 hopping/reward hacking은 보고되지 않았지만, matched control을 이겼다는 근거가 없다. H-010을 더 연장하거나 airtime 축을 추가 sweep하기보다 H-009/H-011과 control을 같은-parent 조건으로 비교한다.
