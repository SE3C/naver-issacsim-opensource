---
title: "H1 finalize/report 자동 판정의 한계"
purpose: "AI upload bundle — checkpoint·report 해석 시의 확인된 함정 방지"
sources:
  - "data/processed/experiments/h1/analysis/2026-08-26_H1_FINALIZE_REPORT_BUG_REVIEW.md"
  - "data/processed/experiments/h1/training/2026-08-25_PERSONAL_SERVER_TERMINATION_M50_25K.md"
  - "data/processed/experiments/h1/analysis/2026-09-07_BREV_L40S_H1_BASELINE_5K_AND_SCREENING.md"
  - "data/processed/experiments/h1/analysis/2026-09-17_H-005_PERSONAL_RESUME_FROM_H-001_1P5K_DEEP_ANALYSIS.md"
  - "data/processed/experiments/h1/analysis/2026-09-17_H-006_PERSONAL_RESUME_FROM_H-001_1P5K_DEEP_ANALYSIS.md"
  - "data/processed/experiments/h1/analysis/2026-09-17_H-007_PERSONAL_RESUME_FROM_H-001_1P5K_DEEP_ANALYSIS.md"
  - "data/processed/experiments/h1/analysis/2026-09-17_H-008_PERSONAL_RESUME_FROM_H-001_1P5K_DEEP_ANALYSIS.md"
  - "data/processed/experiments/h1/analysis/2026-09-18_H-007_MODEL2998_SINGLE_CHECKPOINT_SUMMARY.md"
  - "data/processed/experiments/h1/analysis/2026-09-18_H-008_MODEL2998_6TERRAIN_VIDEO_ANALYSIS_SUMMARY.md"
  - "data/processed/incoming/other/reviewed/2026-09-18_H007_MODEL_2998_SINGLE_CHECKPOINT_ANALYSIS.md"
  - "data/processed/incoming/other/reviewed/2026-09-18_H008_H1_MODEL2998_6TERRAIN_VIDEO_ANALYSIS.md"
  - "data/processed/experiments/h1/analysis/2026-09-18_H-008_CONT2K_FROM_MODEL2998_ANALYSIS.md"
  - "data/processed/incoming/other/reviewed/H1_H009_HIPDEV030_FROM_H008_3K_DEEP_ANALYSIS_20260920.md"
  - "data/processed/incoming/other/reviewed/H1_H010_AIRTIME025_3K_TO_5K_DEEP_ANALYSIS_REVISED.md"
  - "data/processed/incoming/other/reviewed/H1_H011_HIPDEV010_MODEL4997_DEEP_ANALYSIS.md"
  - "data/processed/incoming/other/reviewed/H1_H009_R02_VS_H008_CORRECTED_CONTROL_DEEP_ANALYSIS_20260925.md"
  - "data/processed/incoming/other/reviewed/H1_H010_R02_AIRTIME025_CORRECTED_VS_H008_CORRECTED_CONTROL_TO5K_DEEP_ANALYSIS_20260926.md"
  - "data/processed/incoming/other/reviewed/H1_H011_R02_HIPDEV010_CORRECTED_VS_H008_CORRECTED_CONTROL_DEEP_ANALYSIS_20260926.md"
  - "data/processed/incoming/other/reviewed/2026-09-26_H1_ORGANIZER_CHECKPOINT_QA_SIRIUS_YEOLMU.md"
type: "verified_tooling_warning"
---

# H1 finalize/report 자동 판정의 한계

개인 H1 장기 실행에서 자동 `report.html`과 full TensorBoard 자료가 서로 달랐다. 사용자 제공 공식 서버 확인 기록은 기본 `EventAccumulator` scalar limit이 10,000이고, `_finalize.py`가 별도 size guidance 없이 이를 사용한다고 보고한다. AI는 report를 정답으로 취급하지 말고 아래 규칙을 따른다.

## 확인된 사실

- report/finalize는 reward `6.749`, step 23101의 `model_23100.pt`를 고른다.
- 같은 실행의 full scalar CSV에는 reward 최고 `6.904`, step 24012가 있다.
- 공식 서버 확인 기록상 기본 scalar limit은 10,000인데 이 run의 scalar는 25,000개다. 따라서 이 사례의 자동 선택은 raw 전체가 아닌 제한된 EventAccumulator 결과에 의존했다는 근거가 강하다.
- finalize 뒤 intermediate checkpoint 250개가 삭제된 기록이 있다. 따라서 현재 archive에는 higher-reward 시점의 checkpoint가 남아 있지 않다.
- report는 action std `1.206`을 근거로 “거의 학습이 안 됨” 경고를 냈지만, 동일 run의 후반 episode length·terrain·survival 지표는 개선된 상태다.

이 사례는 **PERSONAL** H1 `Humanoid-v0`, seed 42, 4,096 env, rollout 24, `termination_penalty=-50`, headless 25K 실행이다. console은 `24999/25000`과 `exit=0`을 기록했고, 마지막 500회 평균은 episode length 869.23, terrain 5.897, timeout 78.96%, base-contact 종료 21.05%, XY error 0.360, yaw error 0.811이었다. `model_23100.pt`와 exported `model_best.pt`의 SHA-256은 같지만, play 영상·`policy.pt`·공식 evaluator·복수 seed가 없어 **공식 정책 성능 근거가 아니다**. 실행 조건·원본 위치·baseline 200회와의 비교 한계는 [상세 실험 분석](../experiments/h1/training/2026-08-25_PERSONAL_SERVER_TERMINATION_M50_25K.md)에 남겨 둔다.

2026-09-07의 별도 5K baseline에서는 다른 finalize/staging 결함도 확인됐다. `exported/model_best.pt`는 1K checkpoint였지만 마지막 exported `policy.pt`와 MP4는 4,999 checkpoint 결과였다. 또한 TERM50 이름의 MP4는 baseline 1K 영상과 동일했다. 이는 checkpoint 별칭과 영상 파일명이 provenance 증거가 아니라는 뜻이다.

## 해석 규칙

1. `model_best.pt`는 자동 선택된 학습 reward 후보일 뿐, 공식 시나리오·실제 보행 기준 최적 정책이 아니다.
2. action std 하나로 학습 성공/실패를 판정하지 않는다. episode length, terrain, termination, tracking, loss, evaluator, play 영상을 함께 본다.
3. report의 설정·종료·hash 표시는 원본과 대조해 쓸 수 있지만, 자동 “경고/성공” 문구는 가설로 취급한다.
4. raw event 전체는 trajectory 해석에 사용한다. 다만 report와 다르다고 판정하기 전에 native selector의 `warmup = min_step + max(50, int((max_step - min_step) * 0.10))` 필터를 동일하게 적용한다. 구현은 `step >= warmup`을 후보에 포함하므로 2998→4997에서는 3197이 포함되고 그 미만만 제외된다. 필터 밖의 raw reward 최고는 자동 선택 후보가 아니다. 자동 reward 최고 역시 실제 정책/공식 시나리오 최고라는 뜻은 아니므로 evaluator와 play 영상으로 다시 판단한다.
5. checkpoint, policy와 영상의 SHA-256 연결 manifest가 없으면 파일명만으로 같은 정책 산출물이라고 단정하지 않는다.
6. 요청 iteration과 실제 마지막 numbered checkpoint를 구분한다. 5,000회 zero-based 실행의 `model_4999.pt`는 정상적인 최종 checkpoint다.

## 제공된 운영진 checkpoint 질의·답변의 추가 경계

[시리우스_열무 질문과 운영진 답변 전사본](../incoming/other/reviewed/2026-09-26_H1_ORGANIZER_CHECKPOINT_QA_SIRIUS_YEOLMU.md)은 자동 `model_best.pt`가 학습 reward 기준의 **기본 후보**이지 채점 최적 후보 보장은 아니라고 설명한다. 중간 checkpoint를 학습 중 보존한 뒤 TensorBoard의 smoothed 흐름, episode length, XY error와 실제 play 동작을 비교해 선택할 수 있고, 제출에 사용할 회차와 근거를 코멘트에 남겨야 한다. 이는 최종 numbered checkpoint를 기본으로 삼는 우리 resume 운영 원칙과 양립한다. 다른 checkpoint 선택은 명시적 근거가 있을 때의 예외이며, 여러 정책을 자동 탐색하는 새 selector를 뜻하지 않는다.

운영진이 제시한 `agent.save_interval=50`은 native CLI에서 저장 간격을 좁히지만 finalize가 중간 파일을 삭제하므로 학습 중 복사해야 한다. 예시의 reward peak 2681에 가장 가까운 50회 저장 checkpoint도 2700(거리 19)이지 2650(거리 31)이 아니다. 2681의 `19.68`과 2700의 `15.73`은 서로 다른 최근 종료 episode 100개 평균이어서 정책 가중치 차이로 단정하지 않고 시계열을 smoothing해 해석한다. 이 전사본은 제공된 대화 텍스트이며 원 게시 화면과 실제 명령 실행을 독립 확인한 기록은 아니다.

## Historical feet=-0.2 PERSONAL resume branches (2026-09-17–21)

The following parent SHA `68fa0a9f…f0c1` and descendant H-008 parent SHA `d9a30c8a…1912ae` identify the **old** lineage. Its selector calculations and then-current HOLD decisions remain useful history, not the corrected Run 02/03 policy decisions.

H-005~H-008 are 1,500-scalar PERSONAL resume runs. H-007 and H-008 do not show an unexplained
selector mismatch: the native finalizer ignores events before
`min_step + max(50, int((max_step - min_step) * 0.10))`. Their 1499→2998 ranges therefore
become eligible at about 1648; raw maxima at 1564/1545 are excluded, and eligible maxima at
1733/1711 map to automatic `model_best=model_1700`. H-005 instead maps `model_best` to final
`model_2998`, and H-006 maps it to `model_2700`; none of those aliases answers which checkpoint
is best for tracking, terrain, stability, or an official evaluator.

The preserved raw H-007/H-008 reports predate this code-level confirmation: they describe a
shorter 1499–1549 analysis warm-up or leave the raw/report peak difference unexplained. Keep
those incoming files immutable as historical analysis, but use the processed summaries and the
verified finalizer formula above for current decisions.

For every resume branch, retain all numbered checkpoints and identify the actual video source
by hash. After sufficiently long additional training, use the final numbered checkpoint by
default; only joint late terrain/tracking/fall deterioration justifies its predecessor. Make one
native play/export from that final checkpoint rather than building a PC tournament or selector.
Distinguish a selection-report mismatch from a failed train or failed evidence archive. Do not
repair official source files to force a preferred result.

The later H-008 2,000-iteration PERSONAL continuation makes the same separation operational:
the native report/finalizer selected automatic `model_best=model_4900.pt` at a reported reward
peak near step 4911, while rounded console rows display a larger mean reward near 3042. For the
2998→4997 range the eligible threshold is about 3197, so the early console high is outside the
selector window and does not contradict the report. The final numbered `model_4997.pt` is
retained as the default resume representative
because late terrain/tracking/fall values do not jointly collapse, not because the report's
automatic best label proves policy quality. Its archive validation is WARN for generic-run
provenance gaps, not a failed train or hash mismatch.

H-009 confirms the same selector rule with a 2,000-point resume and validation PASS archive.
Its finalizer selected `model_best=model_3600.pt` at reported reward `5.736 @3627`, while the
received raw-event analysis finds the global reward maximum `5.978 @3041`. The latter is below
the roughly 3197 eligible threshold and is therefore intentionally excluded. Neither is
the default representative: the reward peak is still in a terrain `3.43` re-adaptation regime,
whereas final `model_4997.pt` has late terrain `5.593` and improved XY/yaw endpoint values without
a joint late collapse. The same archive labels its inherited policy/ONNX/MP4 as UNCHANGED, so an
existing file under `exported/` never proves a fresh export or H-009 video. Preserve all numbered
checkpoints and use final-numbered selection plus explicit fresh-video provenance rather than a
report alias or stale artifact name.

Historical H-010 and H-011 Run 01 independently show the same behavior. Both resume the old H-008 3K `model_2998` through
global 4997 with validation PASS and 21 checkpoints. Their raw reward maxima at 3044/3084 occur
before the roughly 3197 threshold; eligible report maxima at 3299/3203 map to
`model_3300`/`model_3200`. This is expected native behavior, not a report inconsistency. Their
final `model_4997` checkpoints remain the resume representatives, while both **historical Run 01** reward hypotheses
remain PERSONAL HOLD because the available metrics and qualitative videos did not establish a
decisive improvement over the old unchanged H-008 continuation.

## Corrected +0.2 lineage: final checkpoint remains representative (2026-09-25)

Corrected legacy H-008 Run 03 final `model_2998.pt` (recorded SHA `49fdb297…14983`) is the common parent of the unchanged 5K control and the legacy H-009/H-010/H-011 corrected Run 02 branches. Their final numbered `model_4997.pt` checkpoints remain the representatives because none has a joint late terrain/tracking/contact collapse. The corrected automatic `model_best.pt` maps to control `model_4900`, H-009/H-011 `model_4800`, and H-010 final `model_4997`; do not reuse the old `model_3300`/`model_3200` mappings above. Six-terrain suite manifests identify each final checkpoint, but are qualitative videos without matched commands/terrain seed. Corrected legacy H-009 and H-011 remain HOLD; the corrected `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch (legacy H-010) is **PROMOTE only to future fixed paired evaluation**, not final adoption or an OFFICIAL result. [Corrected H-009 comparison](../incoming/other/reviewed/H1_H009_R02_VS_H008_CORRECTED_CONTROL_DEEP_ANALYSIS_20260925.md) · [H-010 comparison](../incoming/other/reviewed/H1_H010_R02_AIRTIME025_CORRECTED_VS_H008_CORRECTED_CONTROL_TO5K_DEEP_ANALYSIS_20260926.md) · [H-011 comparison](../incoming/other/reviewed/H1_H011_R02_HIPDEV010_CORRECTED_VS_H008_CORRECTED_CONTROL_DEEP_ANALYSIS_20260926.md).

## 2026-09-27 AIRTIME-025 fresh와 continuation의 checkpoint 경계

새 `AIRTIME-025` fresh Run `20260927-032343-h1-h005-fresh3k-r01-20260927`(legacy H-005 R03)은 final `model_2999.pt`를 보존했지만 자동 best와 6지형 영상 source는 `model_2750.pt`다. corrected `AIRTIME-025` continuation Run `20260927-054950-h1-h005-corrected3kto5k-r02-20260927`(legacy H-005 R04)의 실제 부모는 corrected final `model_2998.pt`이고, +2K 후 final은 `model_4997.pt`이나 자동 best와 6지형 영상 source는 `model_4800.pt`다. `AIRTIME-025` continuation의 마지막 수백 iteration에서 terrain·tracking·training contact가 함께 붕괴하지 않아 final 4997을 기본 대표 후보로 유지한다. 그러나 **final 2999와 final 4997의 행동은 이 영상들로 검증되지 않았다.** 4800 영상의 boxes 진행 장면을 4997 성능이나 공식 채점 근거로 옮기지 않는다. resume 경계 step `2998`의 curriculum/episode accumulator reset도 정책의 즉각적 향상·악화로 읽지 않는다. [fresh 경로 분석](../incoming/other/reviewed/H1_H005_FRESH3K_R01_VS_H005_R02_DEEP_ANALYSIS_20260927.md) / [5K 분석](../incoming/other/reviewed/H1_H005_CORRECTED5K_R02_VS_H005_FRESH3K_R01_DEEP_ANALYSIS_20260927.md).

후속 재분석은 이 continuation의 **전체 raw** `Train/mean_reward` 최고를 `4.920 @3042`로 기록한다. 이는 resume warm-up 필터의 시작점 `3197`보다 앞이므로 자동 best 후보가 아니다. `console.log`와 `report.html`의 `4.550 @4814 → model_4800.pt`는 **eligible/report 최고**이며 두 수치는 서로 모순되지 않는다. 앞선 분석 원문의 “raw/report peak 약 4.55”라는 합쳐 쓴 표기는 이 범위 차이를 놓치기 쉬우므로 원문은 보존하고 여기서 구분한다. 높은 초기 raw peak나 자동 best 명칭만으로 final 4997을 버리지 않는다. [후속 재분석](../incoming/other/reviewed/H1_H005_FRESH3K_R01_VS_H005_CORRECTED3KTO5K_R02_DEEP_ANALYSIS_20260927.md).

## 2026-09-18 final-checkpoint video reports add visual evidence, not a score

H-007 and H-008 each now have a six-terrain `model_2998` video analysis whose quoted MP4 hashes
match the received collections. The analyses observe upright locomotion and terrain traversal
in their recorded 19.98-second trajectories; H-007 additionally describes a boxes recovery.
This is useful qualitative confirmation that final-checkpoint selection is not based only on a
scalar curve. It is not checkpoint-hash provenance embedded in the MP4, a repeated-trial
success rate, a commanded-tracking measurement, a reward-delta causal proof, or OFFICIAL score
evidence. Preserve the source reports and use their limitations to avoid turning a video-only
sanity check into a new evaluator/tournament workflow.

## ORIENT-100 자동 best 2850과 마지막 keeper 2950의 연결 (2026-10-07)

OFFICIAL fresh 3K Run `20261006-133517-h1-orient-100-fresh3k-official`의 auto best `model_2850.pt`와 마지막 보존 `model_2950.pt`는 서로 다르다. [학습 intake](../experiments/h1/training/2026-10-06_ORIENT100_OFFICIAL3K_EVIDENCE_INTAKE.md)에서 SHA와 출처를 구분한다. 이번 [Windows PERSONAL 분석](../incoming/other/reviewed/H1_ORIENT-100_POLICY_ANALYSIS_20261007.md)은 정확히 `model_2850`으로 연결되는 3,072 episode/6영상의 행동 근거이며 **`model_2950` 행동의 증명으로 복제하면 안 된다.** `model_best` 자동 선택은 평가기에서의 전면 우위·공식 점수·최종 checkpoint 선택을 의미하지 않는다. 이번 `model_2850` 행동 선택은 안정 생존에도 balance/lateral drift, rough tail, matched control 부재로 **HOLD**다.

## 다음 실행의 필수 조치

- finalize 전 `logs/<run>/`와 모든 `model_*.pt`를 복사한다.
- `events.out.tfevents*`, console, exact command, dependency/runtime version, config/hash/diff, GPU telemetry, play 영상까지 함께 export한다.
- 공식 서버 제공 파일은 직접 수정하지 않는다. **보존된 최신 직접 답변(2026-08-26)**은 운영진이 개발팀에 전달했고 검토 결과를 추후 안내하겠다는 상태다. 현재 저장소에는 그 이후의 최종 검토 답변이 보존되어 있지 않으므로, 이를 해결 완료로 쓰거나 반대로 현재도 실시간으로 '대기 중'이라고 단정하지 않는다. 현재 reusable PERSONAL evaluator 공용 core를 재사용하는 Windows H1 통합 launcher가 `C:\NCRC\h1_6terrain_video.bat`로 설치됐고 CPU 회귀 테스트 60개와 PowerShell/설치 파일 검증을 통과했다. H1은 ±10° 6영상 뒤 camera-off `scenario7` 8 case full 평가를 사용하며 smoke 옵션은 제거됐다. 2026-10-06 당시에는 H1 GPU full 근거가 없었으나 2026-10-07 `ORIENT-100 / model_2850` Windows PERSONAL 단일 정책 full 및 6영상 근거가 확보됐다. 다른 checkpoint의 matched paired comparison은 여전히 미실행이며 구현만으로 이를 완료했다고 부르지 않는다.
