---
title: "H-004 personal 1.5K decision"
environment: "PERSONAL / Brev L40S"
status: "hold_comparison_requires_revalidation"
source_report: "data/processed/incoming/other/reviewed/2026-09-17_H1_H004_TERM20_1P5K_DEEP_ANALYSIS.md"
---

> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/experiments/h1/analysis/2026-09-17_H-004_PERSONAL_FRESH_1P5K_DEEP_ANALYSIS.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.


# [분석] H-004 — personal fresh 1.5K decision

> 관리 안내 (2026-10-13): **분석** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](<../../../../research/EXPERIMENTS.md>)를 확인한다.

> **2026-09-21 정정 · 상대 비교용 · TERM50 비교 재검증 필요.** H-004는 fresh feet=+0.2, 비교한 개인 H-001은 feet=-0.2다. termination 단독 우열 해석을 철회한다. 과거 parent 선택 결정과 관측 수치는 보존하되 현재 판단은 HOLD다. 정정 근거〔원본 참조: `../2026-09-21_H1_PARENT_AIRTIME_LINEAGE_CORRECTION.md` / 공개 사본 미포함〕.

## Scope

This is a PERSONAL/Brev L40S screening result, not OFFICIAL performance evidence or a
submission claim. The intended termination comparison was -50→-20, but actual PERSONAL H-001 also had feet=-0.2 versus H-004's +0.2. This was a fresh start.

## Evidence-backed result

The 1,500-iteration run completed with exit code 0 and reported evidence validation PASS.
There was no reported OOM, PPO divergence, NaN, or Inf. The learning curve recovered after
an early curriculum collapse, but its endpoint remained materially behind H-001 TERM50 on
the same 1.5K window:

| Metric at iter 1499 | H-004 TERM20 | H-001 TERM50 |
| --- | ---: | ---: |
| Episode length | 632.87 | 686.00 |
| Terrain level | 0.8595 | 5.119 |
| Base-contact termination | 68.87% | 32.41% |
| Timeout | 31.13% | 67.59% |

Mean reward is deliberately excluded from this decision because the termination coefficient
changed. The report also identifies the selected `model_best.pt` as the reward-peak
checkpoint near iteration 1400, while the endpoint continued changing. It includes neither
a `policy.pt` nor a video, so it cannot support a visual locomotion conclusion.

## Decision

Historical decision: H-004 was not chosen as the fresh parent. Current decision: HOLD; the comparative reward conclusion requires revalidation. It is not a numerical or optimizer
failure; the recorded values compare differently configured runs, not an isolated termination change. A future
TERM50-pretrained, TERM20 fine-tune would need a separately registered hypothesis because
it asks a different question.

H-005~H-011 require planned reruns from a newly trained +0.2 H-001 parent. Their historical -0.2 parent is identified; it must not be relabeled as +0.2.

## Sources

- [Raw received analysis](<../../../received/2026-09-17_H1_H004_TERM20_1P5K_DEEP_ANALYSIS.md>)
- [Experiment registry entry](<../../../../research/experiments/h1/H-004.md>)
