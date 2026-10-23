# NCRC 외부 H1 실패 38건 × 내부 H1 실험 DB 교차 분석

작성 기준일: 2026-09-23  
분석 단위: 외부 `key` (공개 페이지 `trial` 번호는 표시용이며 내부 H-xxx/G-xxx와 무관)  
외부 원자료 우선순위: `04_failure_runs.csv` → `05_failure_reward_dials.csv` → `06_failure_stats_long.csv` → `07_failure_reward_matrix.csv` → `NCRC_H1_failures_38_full.json` / `videos.json` → 파생 보고서  
내부 근거: 첨부된 `00`, `06`, `13`, `14`, `15`, `17`, `18` H1 문서의 검증된 계보/실험 요약

> **해석 경계**: 외부 공개 실패 로그는 선택된 관찰 자료이며 동일 parent, seed, evaluator, environment, code version, training length가 통제되지 않았다. 따라서 이 보고서는 외부 row를 공식 성능 비교나 Optuna `study.tell()` trial로 취급하지 않는다. 다중 reward 변경 run은 조합 신호로만 사용한다. `why`, `severity`, `bias`는 stats/dials에서 자동 생성되었을 가능성이 있으므로 독립적인 정답 label로 사용하지 않는다.

## 1. 핵심 발견 요약

1. **H1 실패 38건은 “terrain이 안 오른 실패”보다 “terrain은 5.x까지 올랐는데 특정 지형/명령에서 계속 넘어지는 실패”가 더 많다.** 전체 실패 표본의 terrain median은 **5.695**, fall-rate median은 **24.2%**, exploration std median은 **1.382**다. 38건 중 **27건은 terrain ≥5**, **32건은 fall rate >20%**, **34건은 std ≥1.0**이다. 이 빈도는 전체 참가자의 실패확률이 아니라 공개된 실패 사례 안의 분포다.
2. **구덩이/틈이 가장 반복적인 late-stage failure cluster다.** 11건 중 10건이 `학습에 없던 지형`으로 기록됐고, median terrain **5.73**인데 median fall **25.4%**다. 대표: `reel-22863265`, `reel-74420401`, `reel-78059501`, `reel-8945010`, `reel-60491775`.
3. **높은 training reward는 실패를 배제하지 못한다.** best reward ≥10이면서 fall ≥20%인 H1 기록이 9건 있다. `reel-14106372`는 best reward **26.61**, terrain **5.90**인데 fall **21.5%**이고, `reel-74319272`는 reward **21.65**, terrain **5.82**, fall **27.3%**, std **2.286**이다.
4. **낮은 fall도 terrain progression 성공을 보장하지 않는다.** `reel-93039572`는 fall **12.9%**지만 terrain **3.74**, std **2.593**이고, `reel-92770425`는 fall **16.1%**지만 terrain **3.67**, std **2.325**다. 생존만 최적화된 정책을 경계해야 한다.
5. **single-dial 기록은 실제로 6건이며, H1은 5건이다.** 가장 강한 경고는 `action_rate_l2 -0.0005→-0.0025` only인 `reel-78394459`: checkpoint 4300 / total 5000, terrain **0.00**, fall **100%**. 그러나 더 강한 action-rate penalty가 다른 reward와 묶인 run들은 terrain 5.x에 도달해 **원인 확정은 불가**하다. 이 모순 때문에 내부 clean screen의 정보가치가 높다.
6. **외부와 내부가 가장 일관되게 경고하는 축은 큰 yaw-tracking 단독 강화다.** 외부 `reel-60061435`는 `track_ang_vel_z_exp 0.5→1.0` only에서 1K terrain **0.01**, fall **83.1%**; 내부 PERSONAL YAW075(`0.5→0.75`) 1K도 terrain **0**, base-contact **100%**였다. 따라서 다음 yaw 실험은 0.75/1.0 재시도가 아니라 안정된 TERM50 parent에서 작은 0.6 step이 더 정보가치가 높다.
7. **우리 내부에서 가장 큰 미해결 인과 질문은 linear tracking이다.** H-007/H-008은 parent의 `feet_air_time=-0.2` 문제로 실제로 track과 feet가 동시에 바뀌었으므로 `track 0.5→0.75/1.0` 단독효과를 증명하지 못했다. 외부 single-dial 1.0도 early collapse라, corrected `+0.2` TERM50 parent에서 **0.75 clean sibling + unchanged control**이 다음 GPU run의 최우선 질문이다.
8. **termination은 “더 세게 = 더 좋음”이 아니다.** 외부 -200~-300 영역 12건은 median terrain **5.68**, fall **19.4%**로 생존 자체는 나쁘지 않지만 std median이 **2.117**이다. 내부 OFFICIAL TERM50 5K는 안정성 anchor지만 yaw error **0.935**가 남았고 H-012 -100도 high-yaw trade-off가 보고됐다. 그래서 -200/-300으로 점프하기보다 **-50 vs -100 matched sibling**이 우선이다.
9. **feet_air_time과 hip deviation은 당장 GPU 1회의 정보가치가 상대적으로 낮다.** H-010 `feet 0.20→0.25`는 unchanged control과 사실상 tie였고 H-009(-0.30)/H-011(-0.10) hip siblings도 decisive gain이 없었다. lineage 재검증은 필요하지만, 새 질문을 하나만 고른다면 tracking/action-rate/termination보다 뒤다.

## 2. H1 38건 지형별 실패 지도

### 2.1 의미 기반 지형군 요약

| 지형군 | n | 원본 terrain | 실패 이유 | fall 중앙값(범위) | terrain 중앙값(범위) | std 중앙값(범위) | best reward 중앙값(범위) | 자주 바뀐 reward | key |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 구덩이/틈 | 11 | 구덩이(6), 틈 뛰어넘기(5) | 학습에 없던 지형 10, 학습 부족 1 | 25.4% (18.5–82.9) | 5.73 (0.43–5.95) | 1.405 (1.072–2.798) | 6.26 (3.74–18.03) | `track_lin_vel_xy_exp` 10, `termination_penalty` 10, `action_rate_l2` 8, `feet_air_time` 8 | `reel-36602380`, `reel-78059501`, `reel-77755064`, `reel-74420401`, `reel-8945010`, `reel-92451333`, `reel-60491775`, `reel-22863265`, `reel-19129897`, `reel-14325580`, `reel-87505560` |
| 기타 특수 지형 | 7 | 떠 있는 고리(4), 복합 — 모든 지형 (학습 그대로)(2), 기둥 숲(1) | 학습에 없던 지형 4, 학습 부족 2, 관절 떨림 1 | 28.2% (15.6–100.0) | 5.20 (0.00–5.92) | 1.096 (0.419–2.168) | 3.16 (0.00–11.23) | `action_rate_l2` 5, `track_ang_vel_z_exp` 5, `track_lin_vel_xy_exp` 5, `termination_penalty` 5 | `reel-78394459`, `reel-78339600`, `reel-78293289`, `reel-74375233`, `reel-93015733`, `reel-11309747`, `reel-82918128` |
| 징검다리/레일 | 6 | 징검다리(4), 레일(2) | 학습에 없던 지형 6 | 22.8% (14.9–28.8) | 5.67 (4.74–5.97) | 1.427 (1.036–2.066) | 2.00 (-5.87–23.46) | `termination_penalty` 6, `action_rate_l2` 4, `track_lin_vel_xy_exp` 4, `feet_air_time` 3 | `reel-8908141`, `reel-97191601`, `reel-88114018`, `reel-12918663`, `reel-11806238`, `reel-87239593` |
| 계단/경사 | 4 | 계단 — 가파르게 (15~30cm)(1), 완만한 경사 ±10°(1), 경사 — 내리막(1), 계단 — 올라가기(1) | 관절 떨림 2, 균형 상실 1, 학습 부족 1 | 18.8% (12.9–76.5) | 3.71 (0.90–5.90) | 1.792 (1.155–2.593) | 4.54 (-3.70–26.61) | `track_lin_vel_xy_exp` 3, `termination_penalty` 3, `feet_air_time` 2, `action_rate_l2` 1 | `reel-93039572`, `reel-92770425`, `reel-14106372`, `reel-11999811` |
| 요철/거친 지형 | 4 | 거친 요철(2), 약한 요철(1), 물결(1) | 학습 부족 2, 균형 상실 1, 관절 떨림 1 | 49.1% (14.6–83.1) | 3.57 (0.01–5.84) | 1.776 (0.763–2.720) | 6.78 (4.67–21.65) | `flat_orientation_l2` 3, `track_ang_vel_z_exp` 3, `track_lin_vel_xy_exp` 3, `action_rate_l2` 2 | `reel-74319272`, `reel-97541917`, `reel-60061435`, `reel-59781704` |
| 속도 추종 | 3 | 좌우 속도 추종(3) | 학습 부족 2, 균형 상실 1 | 23.3% (22.5–100.0) | 5.49 (0.82–5.81) | 1.112 (0.991–1.559) | 0.88 (-0.19–8.46) | `action_rate_l2` 2, `termination_penalty` 2, `ang_vel_xy_l2` 1, `feet_air_time` 1 | `reel-77873715`, `reel-77658123`, `reel-14243203` |
| 회전 추종 | 2 | 회전 복합 추종(2) | 학습 부족 2 | 22.8% (22.8–22.8) | 5.92 (5.92–5.92) | 1.572 (1.572–1.572) | 6.07 (6.07–6.07) | `action_rate_l2` 2, `ang_vel_xy_l2` 2, `feet_air_time` 2, `flat_orientation_l2` 2 | `reel-11659221`, `reel-87278881` |
| 박스 단차 | 1 | 박스 단차 — 극한 (10~35cm)(1) | 균형 상실 1 | 22.0% (22.0–22.0) | 5.98 (5.98–5.98) | 2.441 (2.441–2.441) | 12.98 (12.98–12.98) | `action_rate_l2` 1, `ang_vel_xy_l2` 1, `flat_orientation_l2` 1, `joint_deviation_hip` 1 | `reel-9050001` |

### 2.2 지형군별 해석

**구덩이/틈 — 11건.** 가장 큰 군이며 `학습에 없던 지형`이 10/11이다. median terrain 5.73인데 median fall 25.4%라, “curriculum progression이 충분했으니 gap/pit도 잘한다”는 해석은 성립하지 않는다. 8.4K~11.7K total training에서도 실패가 남은 `reel-22863265`, `reel-60491775`, `reel-8945010`이 있다. 반대로 1K `reel-19129897`은 terrain 0.43/fall 82.9%로 명백한 undertraining cluster다. 즉 이 군은 **초기 미수렴 실패**와 **late-stage generalization failure**가 함께 존재한다.

**징검다리/레일 — 6건.** 전부 `학습에 없던 지형` 라벨이다. median terrain 5.67, fall 22.8%로 late-stage generalization failure에 가깝다. `reel-88114018`은 total 10K, terrain 5.57, fall 14.9%인데도 rail 실패이며, `reel-12918663`은 reward 23.46/terrain 5.83/fall 23.9%다. 낮은 fall 또는 높은 reward 하나만으로 좁은 접촉면 traversal을 보장하지 않는다.

**계단/경사 — 4건.** 표본이 작고 이질적이다. `reel-11999811`은 1K linear-tracking single-dial로 terrain 0.90/fall 76.5%의 early collapse, `reel-14106372`는 total 10K에서 terrain 5.90/reward 26.61/fall 21.5%의 late balance failure다. `reel-93039572`와 `reel-92770425`는 fall은 12.9/16.1%로 낮지만 terrain 3.74/3.67, std 2.593/2.325라 **낮은 fall + progression 정체**의 대표 반례다. 표본 4건이므로 “계단에서는 X가 일반적”이라고 부르지 않는다.

**요철/거친 지형 — 4건.** 가장 뚜렷한 bimodal group이다. 1K `reel-60061435`(yaw-only)는 terrain 0.01/fall 83.1%, 999-step `reel-59781704`는 terrain 1.31/fall 71.0%인 반면, 장기 `reel-74319272`·`reel-97541917`은 terrain 5.82/5.84까지 갔지만 관절 떨림/균형 상실과 std 2.286/2.720이 남았다. 학습량과 reward 조합을 분리하지 않으면 같은 “rough failure” 안에서도 전혀 다른 문제를 섞게 된다.

**기타 특수 지형 — 7건.** 떠 있는 고리 4, 복합 2, 기둥 숲 1. `reel-78394459`은 특별히 중요하다. total 5K인데 action-rate only 변경 후 terrain 0/fall 100%라 “학습량 부족”만으로 설명하기 어렵다. 반면 떠 있는 고리 3건(`reel-93015733`,`reel-74375233`,`reel-78293289`)은 terrain 5.73~5.92, fall 20.3~28.2%로 late generalization failure다.

**속도 추종 — 3건.** `reel-14243203`은 total 10회라 사실상 초기 weight를 평가한 특이점이다. 이를 제외한 `reel-77658123`과 `reel-77873715`은 total 약 5K~5.7K, terrain 5.49/5.81, fall 22.5/23.3%다. 따라서 3건 median을 그대로 “속도 추종 특성”으로 읽으면 10-iteration outlier에 왜곡된다.

**회전 추종 — key는 2건이지만 독립 표본으로 보지 않는 편이 안전하다.** `reel-11659221`과 `reel-87278881`은 terrain, iteration, best reward, terrain level, fall, std와 reward dial vector가 전부 동일하다. 따라서 공개 key는 2개지만 실질적인 독립 정책 증거는 1개일 가능성을 배제할 수 없다.

**박스 단차 — 1건.** `reel-9050001` 하나뿐이라 사례 수준이다. terrain 5.98/reward 12.98인데 fall 22.0%, std 2.441이며 8개 reward가 동시에 바뀌었다. 박스에 대한 특정 reward 효과를 이 1건에서 분리하면 안 된다.

### 2.3 원본 terrain 이름별 요약

| 원본 terrain | n | 실패 이유 | fall | terrain level | std | best reward | key |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 구덩이 | 6 | 학습에 없던 지형 5, 학습 부족 1 | 25.8% (18.5–82.9) | 5.54 (0.43–5.83) | 1.522 (1.072–2.798) | 6.18 (3.74–10.10) | `reel-36602380`, `reel-78059501`, `reel-74420401`, `reel-22863265`, `reel-19129897`, `reel-87505560` |
| 틈 뛰어넘기 | 5 | 학습에 없던 지형 5 | 22.3% (20.8–27.5) | 5.85 (5.73–5.95) | 1.405 (1.225–1.642) | 10.38 (4.58–18.03) | `reel-77755064`, `reel-8945010`, `reel-92451333`, `reel-60491775`, `reel-14325580` |
| 떠 있는 고리 | 4 | 학습에 없던 지형 3, 학습 부족 1 | 26.9% (20.3–32.4) | 5.76 (4.82–5.92) | 1.208 (1.001–1.359) | 4.45 (0.00–11.23) | `reel-78293289`, `reel-74375233`, `reel-93015733`, `reel-11309747` |
| 징검다리 | 4 | 학습에 없던 지형 4 | 24.2% (21.7–28.8) | 5.45 (4.74–5.83) | 1.571 (1.036–2.066) | 2.00 (-5.87–23.46) | `reel-8908141`, `reel-97191601`, `reel-12918663`, `reel-11806238` |
| 좌우 속도 추종 | 3 | 학습 부족 2, 균형 상실 1 | 23.3% (22.5–100.0) | 5.49 (0.82–5.81) | 1.112 (0.991–1.559) | 0.88 (-0.19–8.46) | `reel-77873715`, `reel-77658123`, `reel-14243203` |
| 거친 요철 | 2 | 균형 상실 1, 학습 부족 1 | 55.2% (27.3–83.1) | 2.92 (0.01–5.82) | 1.524 (0.763–2.286) | 13.16 (4.67–21.65) | `reel-74319272`, `reel-60061435` |
| 레일 | 2 | 학습에 없던 지형 2 | 17.9% (14.9–21.0) | 5.77 (5.57–5.97) | 1.333 (1.243–1.424) | 7.55 (-4.84–19.95) | `reel-88114018`, `reel-87239593` |
| 복합 — 모든 지형 (학습 그대로) | 2 | 관절 떨림 1, 학습 부족 1 | 47.8% (15.6–80.0) | 2.60 (0.00–5.20) | 1.529 (0.890–2.168) | 3.93 (3.16–4.70) | `reel-78339600`, `reel-82918128` |
| 회전 복합 추종 | 2 | 학습 부족 2 | 22.8% (22.8–22.8) | 5.92 (5.92–5.92) | 1.572 (1.572–1.572) | 6.07 (6.07–6.07) | `reel-11659221`, `reel-87278881` |
| 경사 — 내리막 | 1 | 균형 상실 1 | 21.5% (21.5–21.5) | 5.90 (5.90–5.90) | 1.155 (1.155–1.155) | 26.61 (26.61–26.61) | `reel-14106372` |
| 계단 — 가파르게 (15~30cm) | 1 | 관절 떨림 1 | 12.9% (12.9–12.9) | 3.74 (3.74–3.74) | 2.593 (2.593–2.593) | 4.58 (4.58–4.58) | `reel-93039572` |
| 계단 — 올라가기 | 1 | 학습 부족 1 | 76.5% (76.5–76.5) | 0.90 (0.90–0.90) | 1.259 (1.259–1.259) | 4.51 (4.51–4.51) | `reel-11999811` |
| 기둥 숲 | 1 | 학습에 없던 지형 1 | 100.0% (100.0–100.0) | 0.00 (0.00–0.00) | 0.419 (0.419–0.419) | 0.42 (0.42–0.42) | `reel-78394459` |
| 물결 | 1 | 학습 부족 1 | 71.0% (71.0–71.0) | 1.31 (1.31–1.31) | 1.266 (1.266–1.266) | 4.84 (4.84–4.84) | `reel-59781704` |
| 박스 단차 — 극한 (10~35cm) | 1 | 균형 상실 1 | 22.0% (22.0–22.0) | 5.98 (5.98–5.98) | 2.441 (2.441–2.441) | 12.98 (12.98–12.98) | `reel-9050001` |
| 약한 요철 | 1 | 관절 떨림 1 | 14.6% (14.6–14.6) | 5.84 (5.84–5.84) | 2.720 (2.720–2.720) | 8.71 (8.71–8.71) | `reel-97541917` |
| 완만한 경사 ±10° | 1 | 관절 떨림 1 | 16.1% (16.1–16.1) | 3.67 (3.67–3.67) | 2.325 (2.325–2.325) | -3.70 (-3.70–-3.70) | `reel-92770425` |

## 3. H1 주요 metric 패턴

### 3.1 전체 실패 표본 분포

| metric | n | mean | median | Q1–Q3 | min–max |
| --- | ---: | ---: | ---: | ---: | ---: |
| fall rate | 38 | 34.21% | 24.20% | 21.55–28.65% | 12.9–100% |
| terrain level | 38 | 4.609 | 5.695 | 4.760–5.838 | 0–5.98 |
| exploration std | 38 | 1.527 | 1.382 | 1.161–1.767 | 0.419–2.798 |
| best reward | 38 | 6.843 | 5.395 | 3.305–9.753 | -5.87–26.61 |
| checkpoint iteration | 38 | 4997 | 4650 | 1775–7725 | 0–11000 |
| actual reward dial count | 38 | 4.97 | 6 | 2–8 | 0–9 |

`terrain_direction`은 원본이 명시한 경우에만 사용했다. H1 38건 중 17건이 명시적 상승, 1건(`reel-78394459`)이 3.4→0 하락, 20건은 구 스키마가 마지막 값만 제공해 **미기록**이다. 마지막 값이 5.x라고 해서 미기록 row의 direction을 임의로 “상승”으로 보충하지 않았다. fall-rate window도 18건은 `마지막 10회 평균`, 20건은 `마지막`으로 원자료 정의가 달라 직접 정밀 비교에는 한계가 있다.

### 3.2 높은 reward + 나쁜 terrain/fall

training reward는 서로 다른 reward coefficient를 가진 run 사이에서 척도 자체가 달라지므로 우열 지표가 아니다. 외부에서도 이 문제가 직접 보인다.

- `reel-14106372`: reward 26.61, terrain 5.90, fall 21.5%.
- `reel-12918663`: reward 23.46, terrain 5.83, fall 23.9%.
- `reel-74319272`: reward 21.65, terrain 5.82, fall 27.3%, std 2.286.
- `reel-87239593`: reward 19.95, terrain 5.97, fall 21.0%.
- `reel-60491775`: reward 18.03, terrain 5.86, fall 22.3%.

따라서 내부에서도 `Train/mean_reward` 최고 checkpoint를 최종 policy selector로 쓰지 않고 terrain/fall/tracking/영상으로 재검증하는 기존 원칙이 맞다.

### 3.3 fall은 낮지만 progression이 정체된 사례

- `reel-93039572`: total 10K, fall 12.9%, terrain 3.74, std 2.593. `track_lin 0.5→1.0` + `termination -5→-200` 두 항 동시 변경.
- `reel-92770425`: total 6K, fall 16.1%, terrain 3.67, std 2.325. `feet 0.2→0.12` + `termination -5→-200`.

이 둘은 **survival 또는 낮은 fall만 최적화해도 curriculum progression이 충분하지 않을 수 있다**는 관찰 prior다. 원인은 특정 reward 하나로 귀속할 수 없다.

### 3.4 std가 비정상적으로 높은 사례

std ≥2.0인 H1 failure는 9건이다: `reel-36602380`(2.798), `reel-97541917`(2.720), `reel-93039572`(2.593), `reel-9050001`(2.441), `reel-92770425`(2.325), `reel-74319272`(2.286), `reel-78339600`(2.168), `reel-74420401`(2.097), `reel-11806238`(2.066). 이 중 다수는 terrain 5.x까지 올라갔다. 따라서 std>2는 “학습 자체가 안 됐다”기보다 **late policy가 여전히 높은 stochasticity를 유지하는 위험 신호**로 보는 것이 안전하다.

### 3.5 학습량이 많은데도 실패한 사례

5K 이상 total training인데 실패인 H1 기록이 다수 존재한다. 특히 `reel-78394459`은 total 5K에서 terrain 0/fall100%, `reel-93039572`은 total10K에서 terrain3.74/std2.593, `reel-8945010`은 total11.699K에서 terrain5.83/fall24.7%, `reel-97541917`은 total10K terrain5.84이지만 joint jitter/std2.720이다. “더 오래 돌리면 해결”과 “reward 설계/일반화 문제”를 분리해야 한다.

## 4. reward 조합 패턴

### 4.1 H1에서 실제로 변경된 reward 범위

| reward | H1 등장 수 | baseline | current 관측 범위 | absolute delta 범위 | |delta|/|baseline| 범위 |
| --- | --- | --- | --- | --- | --- |
| action_rate_l2 | 25 | -0.0005 | -0.008–-0.0002 | -0.0075–0.0003 | 0.20–15.00× baseline magnitude change |
| ang_vel_xy_l2 | 16 | -0.05 | -0.25–-0.02 | -0.2–0.03 | 0.20–4.00× baseline magnitude change |
| feet_air_time | 19 | 0.2 | 0.12–0.5 | -0.08–0.3 | 0.10–1.50× baseline magnitude change |
| flat_orientation_l2 | 20 | -1.5 | -2.5–-0.3 | -1–1.2 | 0.07–0.80× baseline magnitude change |
| joint_deviation_hip | 13 | -0.2 | -0.4–-0.1 | -0.2–0.1 | 0.25–1.00× baseline magnitude change |
| joint_deviation_torso | 13 | -0.1 | -0.25–-0.03 | -0.15–0.07 | 0.50–1.50× baseline magnitude change |
| termination_penalty | 31 | -5 | -300–-40 | -295–-35 | 7.00–59.00× baseline magnitude change |
| track_ang_vel_z_exp | 23 | 0.5 | 0.55–2 | 0.05–1.5 | 0.10–3.00× baseline magnitude change |
| track_lin_vel_xy_exp | 29 | 0.5 | 0.7–2 | 0.2–1.5 | 0.40–3.00× baseline magnitude change |

상대 크기 관점에서 특히 큰 조작은 `termination_penalty`다. baseline -5에 대해 외부 current는 -40~-300, 즉 penalty magnitude가 **8~60배**까지 커졌다. `action_rate_l2`도 baseline -0.0005에서 -0.008까지 최대 **16배** 강해진 사례가 있다. 이런 큰 배율 변화는 단순한 미세 튜닝이 아니라 정책 목표의 균형 자체를 바꿀 수 있는 수준이므로, 내부에서는 좁은 single-delta로 확인해야 한다.

### 4.2 반복 co-occurrence

| 동시 변경 pair | H1 사례 수 | 대표 key |
| --- | --- | --- |
| `termination_penalty` + `track_lin_vel_xy_exp` | 25 | `reel-11659221`, `reel-12918663`, `reel-14106372`, `reel-14325580`, `reel-36602380`, `reel-60491775`, `reel-74319272`, `reel-74375233` … |
| `action_rate_l2` + `termination_penalty` | 24 | `reel-11659221`, `reel-12918663`, `reel-14106372`, `reel-14325580`, `reel-22863265`, `reel-36602380`, `reel-60491775`, `reel-74319272` … |
| `action_rate_l2` + `track_lin_vel_xy_exp` | 21 | `reel-11659221`, `reel-12918663`, `reel-14106372`, `reel-14325580`, `reel-36602380`, `reel-60491775`, `reel-74319272`, `reel-74375233` … |
| `termination_penalty` + `track_ang_vel_z_exp` | 21 | `reel-11659221`, `reel-12918663`, `reel-14106372`, `reel-14325580`, `reel-22863265`, `reel-36602380`, `reel-60491775`, `reel-74319272` … |
| `track_ang_vel_z_exp` + `track_lin_vel_xy_exp` | 21 | `reel-11659221`, `reel-12918663`, `reel-14106372`, `reel-14325580`, `reel-36602380`, `reel-60491775`, `reel-74319272`, `reel-74375233` … |
| `action_rate_l2` + `track_ang_vel_z_exp` | 20 | `reel-11659221`, `reel-12918663`, `reel-14106372`, `reel-14325580`, `reel-22863265`, `reel-36602380`, `reel-60491775`, `reel-74319272` … |
| `flat_orientation_l2` + `termination_penalty` | 19 | `reel-11659221`, `reel-12918663`, `reel-14106372`, `reel-14325580`, `reel-22863265`, `reel-60491775`, `reel-74319272`, `reel-74375233` … |
| `flat_orientation_l2` + `track_lin_vel_xy_exp` | 19 | `reel-11659221`, `reel-12918663`, `reel-14106372`, `reel-14325580`, `reel-59781704`, `reel-60491775`, `reel-74319272`, `reel-74375233` … |
| `action_rate_l2` + `flat_orientation_l2` | 18 | `reel-11659221`, `reel-12918663`, `reel-14106372`, `reel-14325580`, `reel-22863265`, `reel-60491775`, `reel-74319272`, `reel-74375233` … |
| `feet_air_time` + `termination_penalty` | 18 | `reel-11659221`, `reel-12918663`, `reel-14106372`, `reel-14325580`, `reel-22863265`, `reel-74319272`, `reel-74375233`, `reel-74420401` … |
| `feet_air_time` + `track_lin_vel_xy_exp` | 17 | `reel-11659221`, `reel-12918663`, `reel-14106372`, `reel-14325580`, `reel-19129897`, `reel-74319272`, `reel-74375233`, `reel-74420401` … |
| `flat_orientation_l2` + `track_ang_vel_z_exp` | 17 | `reel-11659221`, `reel-12918663`, `reel-14106372`, `reel-14325580`, `reel-22863265`, `reel-60491775`, `reel-74319272`, `reel-74375233` … |

가장 흔한 구조는 **tracking + termination + action-rate**다. `termination_penalty + track_lin_vel_xy_exp`가 25건, `action_rate_l2 + termination_penalty`가 24건, `termination + yaw tracking`이 21건이다. 따라서 외부에서 “termination이 들어간 run의 fall이 낮았다” 같은 단일항 해석은 거의 항상 다른 tracking/control penalty와 섞인다.

### 4.3 공격적/안정화 조합의 대표 사례와 trade-off

- **공격적 gait/tracking 조합 — `reel-74319272`**: `track_lin=2.0`, `yaw=1.0`, `feet=0.5`, `termination=-40`, `flat=-1.0`, `ang_vel_xy=-0.2`, `torso=-0.25`, `action_rate=-0.0006`. terrain 5.82, reward 21.65까지 가지만 fall 27.3%, std 2.286, failure=`균형 상실`. 높은 tracking/gait reward가 progression과 reward를 올려도 안정성을 자동 보장하지 않는다.
- **강한 yaw + feet + relaxed posture + 강한 action-rate penalty — `reel-14106372`, `reel-12918663`**: 두 key는 동일 dial vector(`track_lin=1.0`, `yaw=2.0`, `feet=0.35`, `termination=-150`, `flat=-0.3`, `hip=-0.15`, `torso=-0.03`, `action_rate=-0.0075`)를 사용한다. 각각 terrain 5.90/5.83, reward 26.61/23.46, fall 21.5/23.9%. 지형은 다르며 checkpoint도 달라 같은 run이라고 단정하지 않는다. 하지만 높은 reward와 high terrain에도 20%대 fall이 남는 조합 관찰이다.
- **강한 안정화 조합 — `reel-22863265`**: `termination=-300`, `flat=-2.5`, `ang_vel_xy=-0.25`, `hip=-0.4`, `torso=-0.15`, `action_rate=-0.004`, `yaw=1.5`, `feet=0.25`. terrain 5.83, fall 18.5%, std1.177로 수치상 비교적 안정적이지만 pit failure다. 강한 posture/termination이 특정 unseen terrain traversal을 보장하지 않는다.
- **relaxed posture + strong termination — `reel-9050001`, `reel-97541917`, `reel-78339600`**: `flat=-0.75`, hip/torso 완화, termination -200~-300, tracking 강화가 함께 들어간다. terrain 5.20~5.98이지만 std 2.168~2.720이고 박스/요철/복합에서 balance/jitter failure가 남는다. “posture를 풀면 민첩해져 좋아진다”는 결론도, “풀어서 실패했다”는 결론도 이 조합만으로는 불가능하다.

### 4.4 조합 간 모순이 보여주는 것

가장 중요한 반례는 action-rate다. single-dial `reel-78394459`의 -0.0025는 total5K에도 완전 collapse지만, `reel-88114018`(-0.002 + termination -250)은 rail terrain5.57/fall14.9%, `reel-14106372`(-0.0075 포함 8-dial)은 slope terrain5.90/fall21.5%다. 즉 “-0.0025보다 강하면 실패”라는 threshold는 외부 데이터가 **반박**한다. 대신 “action-rate penalty가 다른 보상 없이 단독으로 강해질 때 H1을 과도하게 소극적으로 만들 수 있는가?”가 내부 검증 질문이다.

## 5. 단일 dial 사례 전수 분석

원자료의 `actual_dial_count`/원본 `dials`로 재검산한 결과 **정확히 6건**이다. H1 5건, Go2 1건이다. `ndial`은 UI/패널 의미가 섞일 수 있어 single-variable 판정에 사용하지 않았다.

| key | robot | terrain | reward | baseline → current | checkpoint/total iter | best reward | terrain level | fall rate | std | 결과/진단 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| reel-87463271 | quadruped | 물결 | `feet_air_time` | 0.01 → 0.08 | 1400 / 1499 | 15.36 @ 1358 | 0.60 | 7.8% | 0.432 | Go2: feet_air_time +0.07 단독. 수치상 큰 이상은 없지만 H1 인과 근거로 전이하면 안 됨. |
| reel-11309747 | humanoid | 떠 있는 고리 | `termination_penalty` | -5 → -50 | 999 / 999 | 1.61 @ 956 | 4.82 | 32.4% | 1.319 | H1: termination -50 단독. terrain 4.82, fall 32.4%; -50도 특수 지형 실패를 자동 해결하지 않음. |
| reel-11806238 | humanoid | 징검다리 | `termination_penalty` | -5 → -200 | 1300 / 2155 | -5.87 @ 1274 | 5.12 | 21.7% | 2.066 | H1: termination -200 단독. terrain은 5.12까지 갔지만 std 2.066·fall 21.7%; 붕괴보다는 안정성/탐색 trade-off 질문. |
| reel-11999811 | humanoid | 계단 — 올라가기 | `track_lin_vel_xy_exp` | 0.5 → 1 | 900 / 1000 | 4.51 @ 902 | 0.90 | 76.5% | 1.259 | H1: linear tracking만 +0.5. 1K에서 terrain 0.90·fall 76.5%; early aggressive-tracking 경고. |
| reel-60061435 | humanoid | 거친 요철 | `track_ang_vel_z_exp` | 0.5 → 1 | 999 / 1000 | 4.67 @ 968 | 0.01 | 83.1% | 0.763 | H1: yaw tracking만 +0.5. 1K에서 terrain 0.01·fall 83.1%; 큰 yaw 강화의 early-collapse 신호. |
| reel-78394459 | humanoid | 기둥 숲 | `action_rate_l2` | -0.0005 → -0.0025 | 4300 / 5000 | 0.42 @ 4288 | 0.00 | 100.0% | 0.419 | H1: 장기 학습인데 terrain 0·fall 100%. action-rate 강화가 과도한 소극성/정체를 만들었는지 내부 복제 가치가 큼. |

### 5.1 사례별 “관찰 / 가능한 해석 / 아직 미증명”

**`reel-78394459` — H1, `action_rate_l2 -0.0005→-0.0025` only**  
관찰: checkpoint 4300 / total5000, terrain 3.4→0 하락, fall100%, std0.419.  
가능한 해석: action-rate penalty를 5배 강하게 하면 행동 변화 비용이 커져 H1이 필요한 회복/보행 동작을 회피하고 stagnant policy로 갈 수 있다. 낮은 std는 “잘 수렴”이 아니라 **나쁜 행동에 일찍 고정**됐을 가능성도 있다.  
미증명: parent/seed/evaluator가 없으므로 -0.0025가 원인이라고 확정할 수 없다. 다중 reward run의 반례도 존재한다.

**`reel-60061435` — H1, `track_ang_vel_z_exp 0.5→1.0` only**  
관찰: 999/1000, terrain0.01, fall83.1%, std0.763.  
가능한 해석: fresh/early training에서 yaw objective를 2배로 키우면 기본 upright locomotion을 배우기 전에 회전 행동이 과도하게 경쟁할 수 있다.  
미증명: 학습량 1K 자체가 부족할 수 있다. 다만 내부 YAW075 1K도 terrain0/base-contact100%라 독립적인 경고 신호가 겹친다.

**`reel-11999811` — H1, `track_lin_vel_xy_exp 0.5→1.0` only**  
관찰: 900/1000, terrain0.90, fall76.5%, std1.259.  
가능한 해석: early stage에 linear tracking을 2배로 키우면 안정 자세를 배우기 전에 전진/가속을 추구해 낙상이 늘 수 있다.  
미증명: 외부 다중변경에서 track=1.0~2.0인데 terrain5.x인 사례가 많아, 1.0 자체가 금지값은 아니다. **stable parent에서 clean 0.75**가 더 좋은 내부 질문이다.

**`reel-11806238` — H1, `termination_penalty -5→-200` only**  
관찰: checkpoint1300 / total2155, terrain5.12, fall21.7%, std2.066, best reward -5.87.  
가능한 해석: 매우 큰 낙상 penalty는 terrain progression을 완전히 막지는 않지만 policy stochasticity나 tracking/gait trade-off를 악화시킬 수 있다. reward 계수가 바뀌어 best reward 절댓값은 비교 불가다.  
미증명: -200이 std 상승의 원인인지, checkpoint/total mismatch와 undertraining 영향인지 분리되지 않는다.

**`reel-11309747` — H1, `termination_penalty -5→-50` only**  
관찰: 999/999, terrain4.82, fall32.4%, std1.319.  
가능한 해석: -50은 early curriculum progression을 가능하게 해도 floating-ring 같은 unseen terrain stability를 해결하지 못할 수 있다.  
미증명: 우리 OFFICIAL TERM50 5K와 조건/지형/길이가 다르므로 직접 성능 비교가 아니다.

**`reel-87463271` — Go2, `feet_air_time 0.01→0.08` only**  
관찰: checkpoint1400 / total1499, terrain0.60, fall7.8%, std0.432; `why`는 수치상 큰 이상 없음.  
가능한 해석: failure label이 특정 wave terrain generalization을 반영했을 수 있다.  
미증명: 로봇/기본 reward 구조가 H1과 다르므로 H1 feet-air-time 인과 근거로 사용하지 않는다.

## 6. 외부 실패 parameter region 후보

| 등급 | 관측 영역 | 외부 관찰 | 해석/내부 조치 |
| --- | --- | --- | --- |
| **강한 경고 신호** | H1 `action_rate_l2=-0.0025` **단독** | `reel-78394459`: total5K, terrain0, fall100% | 금지값은 아님. same-parent short negative-control로 재현 여부 확인. full 5K를 바로 쓰지 않음. |
| **강한 경고 신호** | fresh H1 `track_ang_vel_z_exp` 큰 단독 증가 | `reel-60061435` 1.0 only: terrain0.01/fall83.1%; 내부 0.75 screen도 collapse | 0.75/1.0 direct jump 후순위. stable parent에서 0.6 micro-step. |
| **주의해서 검증** | fresh H1 `track_lin_vel_xy_exp=1.0` 단독 | `reel-11999811`: 1K terrain0.90/fall76.5%; 그러나 다중변경 1.0~2.0 고terrain 반례 다수 | corrected stable parent에서 0.75 clean test 먼저. 1.0은 그 후. |
| **주의해서 검증** | `termination_penalty=-200~-300` | 12 H1 cases: terrain median5.68, fall median19.4%, std median2.117 | collapse region이 아니라 **stability/entropy trade-off** 후보. 내부는 -50→-100 matched를 먼저, -200/300 점프 보류. |
| **주의해서 검증** | `feet_air_time>=0.35` | 3 multi-change: terrain5.82~5.90, fall21.5~27.3 | 높은 gait reward가 high terrain과 공존해도 fall이 남음. 내부 H-010 tie 때문에 immediate priority 낮음. |
| **정보 부족** | `flat_orientation_l2` -2.5~-0.3 | 강/약 양쪽 모두 high-terrain failure 존재 | 단조 경향 없음. clean rough/box screen으로만 판단. |
| **정보 부족** | `ang_vel_xy_l2` -0.25~-0.02 | strong/weak 양쪽 모두 mixed outcome | -0.10 moderate single-delta가 내부 공백을 가장 싸게 메움. |
| **내부 단일변수 검증 가치 높음** | action-rate, track-linear, termination -100 matched, yaw micro-step | 외부 모순/경고 + 내부 계보 공백이 겹침 | 다음 GPU 예산을 이 네 축에 우선 배분. |

중요하게도 **외부에서 실제 관측되지 않은 숫자를 “외부 실패 범위”로 추가하지 않았다.** 내부 candidate의 `yaw=0.6`은 외부 실패 region 추정이 아니라, 내부 기존 프로토콜에 있던 micro-step을 외부의 large-step negative와 연결해 우선순위를 높인 것이다.

## 7. 우리 내부 DB와의 교차 비교

| 내부 evidence | 환경 | delta/계보 | 학습량 | 핵심 관찰 | 현재 해석 |
| --- | --- | --- | --- | --- | --- |
| OFFICIAL baseline 300 | OFFICIAL | fresh baseline, seed42, 4096 env | 300 | terrain 0.00; fall 100%; std 0.633 | 파이프라인/negative control. reward 우열 근거 아님 |
| OFFICIAL baseline 1K | OFFICIAL | baseline `termination=-5`, `feet=+0.2` | 1K | terrain 0.00; 마지막10회 fall 100%; std 0.653 | 1K 학습량에서 미수렴 |
| PERSONAL baseline 5K | PERSONAL | baseline | 5K | terrain 5.054; base-contact 33.21%; timeout 66.79%; XY 0.342; yaw 0.652 | 개인 기준선. 공식 TERM50과 paired 아님 |
| PERSONAL TERM50 screen | PERSONAL | `termination -5→-50` only | 1K | terrain 4.823; timeout 68.34%; episode 799.97; yaw 1.577 | stability 방향은 유망, yaw trade-off |
| PERSONAL YAW075 screen | PERSONAL | `track_ang_vel_z_exp 0.5→0.75` only | 1K | terrain 0; base-contact 100% | 큰 yaw 단독 강화의 강한 early negative |
| OFFICIAL TERM50 5K | OFFICIAL | `termination -5→-50` only; feet +0.2 | 5K | terrain 5.825; base-contact 28.93%; timeout 71.07%; XY 0.378; yaw 0.935; std 1.296; 공식 sim 56.37/70 | 현재 가장 강한 공식 stability anchor; paired baseline은 아님 |
| H-005 GAIT025 | PERSONAL | 실제 parent feet=-0.2에서 `feet -0.2→+0.25` | +1.5K | late terrain 5.422 | HOLD. corrected +0.2 parent 재실험 필요 |
| H-006 GAIT030 | PERSONAL | 실제 parent feet=-0.2에서 `feet -0.2→+0.30` | +1.5K | last-300 terrain 5.469; XY 0.3713; base-contact≈30% | HOLD. corrected parent 필요 |
| H-007 LIN100 | PERSONAL | `track 0.5→1.0` + `feet -0.2→+0.2` | +1.5K | last-500 XY 0.3386; yaw 2.008 | track 단독 효과 철회 |
| H-008 LIN075 | PERSONAL | `track 0.5→0.75` + `feet -0.2→+0.2` | +1.5K + unchanged +2K | unchanged continuation late terrain 5.604; XY 0.3314; base-contact 29.67% | track 단독 효과 미검증; corrected parent+control 필요 |
| H-009 HIP030 | PERSONAL | H-008 3K parent에서 `hip -0.20→-0.30` only | +2K | last-500 terrain 5.596; XY 0.3278; base-contact 29.99% | unchanged control 대비 사실상 tie; HOLD |
| H-010 AIR025 | PERSONAL | H-008 3K parent에서 `feet 0.20→0.25` only | +2K | last-500 terrain 5.663; XY 0.3318; base-contact 29.63% | unchanged control과 사실상 tie; HOLD |
| H-011 HIP010 | PERSONAL | H-008 3K parent에서 `hip -0.20→-0.10` only | +2K | last-300 terrain 5.661; XY 0.3304; base-contact 29.02%; yaw 1.411 | decisive gain 없음; HOLD |
| H-012 TERM100 | PERSONAL | BASE에서 `termination -5→-100` only | fresh 5K | terrain/survival 회복, high yaw; model_4700 automatic best, final model_4999 | matched PERSONAL control 부재; HOLD |

### 7.1 외부와 내부가 같은 방향을 가리키는 부분

- **large yaw-tracking boost 경고**: 외부 `reel-60061435`(1.0 only)와 내부 YAW075 1K가 모두 terrain collapse를 보인다. 이것은 서로 다른 조건의 반복 관찰이지 인과 복제는 아니지만, 0.75/1.0을 다음 대규모 run으로 택할 정보가치는 낮춘다.
- **termination은 stability와 tracking 사이 trade-off**: 외부 -50 single은 terrain4.82/fall32.4, -200 single은 terrain5.12/fall21.7/std2.066이다. 내부 OFFICIAL -50은 terrain5.825/base-contact28.93/yaw0.935, H-012 -100은 terrain/survival 회복+high yaw다. “낙상 penalty를 세게 하면 무조건 좋아진다”가 아니라 **stability gain을 tracking cost와 함께 재야 한다**는 방향이 반복된다.
- **reward/terrain 하나만으로 선택하면 안 됨**: 외부 high-reward/high-terrain failure와 내부 `model_best`/late-window 경계가 같은 진단 원칙을 지지한다. 내부에서는 final numbered checkpoint + late terrain/tracking/fall + video를 보는 기존 방식이 유지되어야 한다.

### 7.2 외부가 내부의 “미해결 질문”을 선명하게 하는 부분

- **linear tracking**: 외부 single 1.0 early failure와 다중변경 high-terrain 반례가 서로 충돌한다. 내부 H-007/008도 feet confound 때문에 답을 못 냈다. 따라서 clean 0.75 sibling은 단순 반복이 아니라 **모순을 해소하는 실험**이다.
- **action-rate**: 외부 single long-run collapse vs multi-change high-terrain 반례가 강하게 충돌하고, 내부 H1 evidence가 거의 없다. 짧은 negative-control screen의 정보가치가 매우 높다.
- **ang_vel_xy / flat_orientation**: 외부 사용 빈도는 높지만 내부 H1 clean evidence가 없다. 다만 single-dial 외부 사례가 없어 A급이 아니라 B급이다.

### 7.3 내부 evidence가 이미 많아 다음 정보가치가 낮은 부분

- `feet_air_time`: H-005/006 historical data + H-010 clean historical sibling(.25)까지 존재. lineage correction 때문에 최종 인과 채택은 못 하지만 .25가 control과 tie였다는 정보가 있다.
- `joint_deviation_hip`: H-009(-.30), H-011(-.10), unchanged control의 same-parent three-point가 이미 decisive gain 없음. corrected lineage 재실험은 보존 목적이지 첫 번째 새 질문은 아니다.

## 8. 다음 single-delta 실험 질문

| 후보 질문 | 외부 근거 key·사례 수 | 외부에서 바뀐 값 | 함께 바뀐 값 / confounder | 우리 내부 관련 evidence | 필요한 대조 실험 | 주요 판정 지표 | 우선도 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A1. corrected parent에서 `track_lin_vel_xy_exp 0.5→0.75`만 올리면 전진/좌우 XY 추종을 개선하면서 terrain·fall·yaw를 유지할 수 있는가? | H1 track_lin 변경 29건; single-dial `reel-11999811` 1건. 1.0 단독은 1K terrain 0.90/fall 76.5%; 2.0 조합 3건은 terrain 5.82–5.97이나 fall 21.0–27.3%. | 외부 0.7–2.0; 특히 1.0 single-dial, 1.25/1.35/1.4/2.0 조합 | 대부분 termination/action-rate/yaw/feet 등 동시 변경; 학습량도 1K~10K | H-007/008은 feet 계보 오류로 track 단독 효과 미검증. H-008 0.75 branch는 corrected rerun 예정. 공식 TERM50의 가장 큰 절대 점수 공백은 전진. | 새 `+0.2 TERM50` 동일 parent checkpoint에서 unchanged control과 `track 0.5→0.75` branch를 같은 seed·추가 iteration으로 실행. fixed evaluator/동일 terrain suite; late-window 비교. | terrain progression, fall/base-contact, XY tracking, yaw tracking, episode length, action std, late-window 안정성, 영상 | A — 최우선 |
| A2. 동일 TERM50 parent에서 `termination_penalty -50→-100`만 강화하면 fall/base-contact를 더 낮추되 XY/yaw와 terrain progression을 유지할 수 있는가? | H1 termination 변경 31건; single-dial `reel-11309747`(-50)·`reel-11806238`(-200) 2건. -200~-300 사례 12건은 terrain 중앙 5.68/fall 중앙 19.4%지만 std 중앙 2.117. | 외부 -40~-300; single -50, -200 | 대부분 tracking/posture/action-rate와 동시 변경; -200 single도 checkpoint 1300/total2155 | OFFICIAL TERM50 5K는 terrain 5.825/base-contact 28.93/yaw 0.935. H-012 -100 fresh 5K는 terrain/survival 회복이나 high yaw, matched control 없음. | 동일 `-50,+0.2` parent에서 unchanged -50 control과 -100 sibling. same seed/iterations/evaluator. -200/-300으로 바로 점프하지 않음. | fall/base-contact, timeout/survival, terrain, XY, yaw, episode length, action std, late-window, 영상 | A — 높음 |
| A3. 안정된 TERM50 parent에서 `track_ang_vel_z_exp 0.5→0.6`의 작은 증가가 yaw만 개선하고 early terrain collapse를 피할 수 있는가? | H1 yaw 변경 23건; single-dial `reel-60061435` 1건은 0.5→1.0, 1K terrain 0.01/fall 83.1%. 외부 0.55도 실제 관측(`reel-87505560`). | 외부 0.55–2.0; single 1.0 | 0.8~2.0은 거의 모두 다중 변경. single 1.0은 짧은 1K. | 내부 PERSONAL YAW075(0.75) 1K도 terrain 0/base-contact 100%. 반면 OFFICIAL TERM50 yaw error 0.935는 개선 여지가 있음. 기존 계획에도 0.6 micro-step이 있음. | same stable TERM50 parent, unchanged control, `0.5→0.6` only. 동일 추가 iteration 및 evaluator; 0.75/1.0은 당장 재시도하지 않음. | yaw tracking, terrain, fall, XY, stop-command drift, episode length, action std, 영상 | A — 높음 |
| B1. `action_rate_l2 -0.0005→-0.0025` 단독 강화가 H1 terrain progression을 실제로 붕괴시키는가, 아니면 외부 특정 run의 confounder인가? | single-dial `reel-78394459` 1건: checkpoint 4300/total5000, terrain 0, fall 100%, std 0.419. 하지만 action_rate≤-0.0025 다중변경 9건은 다수 terrain 5.8대. | 외부 -0.008~-0.0002; single -0.0025 | 강한 반례들은 termination/tracking/posture 동시 변경. 단일 사례는 evaluator/seed/parent 미상. | 내부 H1 action_rate clean screen 없음. 따라서 정보 공백이 큼. | corrected TERM50 parent에서 unchanged control과 -0.0025 branch를 우선 1K/짧은 screen. 수치 붕괴가 아니면 같은 길이까지 연장; terrain 0 고착·행동 정체 시 중단. | terrain 500→1000 방향, fall, XY/yaw, episode length, action std, action-rate reward term, 영상의 굼뜸/stall | B — 작은 screen 가치 매우 높음 |
| B2. `ang_vel_xy_l2 -0.05→-0.10`만 강화하면 요철/박스에서 lateral 흔들림·fall을 줄이면서 XY/terrain을 유지하는가? | H1 ang_vel_xy 변경 16건. -0.10은 구덩이/징검/고리 등 여러 key(`reel-78059501`,`reel-74420401`,`reel-87505560`,`reel-97191601`,`reel-36602380`,`reel-93015733`)에서 관측; 모두 다중 변경. | 외부 -0.25~-0.02; -0.10 반복 | termination/tracking/feet/posture가 함께 바뀜; 방향 효과 분리 불가. | 내부 H1 clean 단일 실험 없음. 공식 TERM50은 요철 점수 비율이 7시나리오 중 최저. | same TERM50 parent + unchanged control, -0.05→-0.10 only, same iteration/evaluator. rough/box/push를 별도 fixed scenario로 비교. | fall, terrain, roll/pitch 안정성 대리, XY/yaw, episode length, action std, rough/box/push 영상 | B — 중상 |
| B3. `flat_orientation_l2`를 -1.5에서 한 단계 강화(-2.0)했을 때 rough/box stability가 좋아지는가, 아니면 기동성을 잃는가? | H1 20건. 강한 -2.0/-2.5는 `reel-77755064`,`reel-22863265`; 완화 -0.5~-0.3도 5건에서 terrain 5.8대. 양 방향 모두 실패 관찰이 있어 monotonic 신호 없음. | 외부 -2.5~-0.3 | 모두 다중 변경; 지형과 학습량 상이. | 내부 clean flat_orientation test 없음. | same TERM50 parent + unchanged control, -1.5→-2.0 only; short screen 후 rough/box/push fixed eval. | terrain, fall, XY, yaw, episode length, action std, 자세/발 끌림/회복 영상 | B — screen 후 판단 |
| C1. `feet_air_time 0.20→0.25/0.30`을 다음 최우선으로 다시 돌릴 것인가? | H1 19건, 0.25가 반복되지만 전부 다중 변경. 0.35~0.5 세 사례도 terrain은 높지만 fall 21.5–27.3%. | 외부 0.12–0.5 | tracking/termination/posture 동시 변경. | H-010 0.20→0.25 same-parent sibling이 unchanged control과 사실상 tie. H-005/006은 lineage 수정 때문에 formal rerun 필요하나 기존 정보는 이미 많음. | 재실험은 lineage 정리 목적일 때만. GPU 1회 정보가치 기준으로는 track/action-rate/termination보다 뒤. | 동일 지표 | C — 당장 후순위 |
| C2. `joint_deviation_hip -0.20→-0.30` 또는 -0.10을 다시 최우선으로 시험할 것인가? | 외부 H1 13건이나 모두 다중 변경. | 외부 -0.4~-0.1 | 다중 변경 | H-009(-0.30), H-011(-0.10), unchanged control이 같은 historical parent에서 거의 tie; winner 없음. | corrected lineage 재확인이 필요할 수 있으나 다음 GPU의 최대 정보가치 축은 아님. | terrain/fall/XY/yaw/영상 | C — 낮음 |
| C3. H1에서 `lin_vel_z_l2`를 탐색할 것인가? | 외부 failure dial 목록에는 6건이 있으나 H1 38건에서는 0건; Go2 쪽 항목. | H1 관측 없음 | 로봇/task 차이 자체가 confounder | 내부 H1 참가자 baseline reward 목록에도 이 항목은 주 실험 축으로 잡혀 있지 않음. | 현재 H1 single-delta 후보에서 제외. | — | C — 건드리지 않음 |

### A. 바로 검증 가치가 높은 질문

**A1 `track_lin 0.5→0.75` clean rerun**, **A2 `termination -50→-100` matched sibling**, **A3 `yaw 0.5→0.6` micro-step**이다. 세 질문 모두 외부의 반복/상충 관찰과 내부의 구체적인 evidence gap이 연결되고, 같은 corrected parent에서 unchanged control을 공유하면 추가 GPU 비용 대비 정보량이 크다.

### B. 흥미롭지만 먼저 작은 screen이 필요한 질문

**B1 action-rate -0.0025**가 가장 강하다. 외부 single-dial은 놀랄 만큼 나쁘지만 다중변경 반례가 있어 오히려 짧은 복제가 가치 있다. **B2 ang_vel_xy -0.10**, **B3 flat_orientation -2.0**은 외부에 충분히 많이 등장하지만 clean causal row가 없으므로 full 5K보다 1K~1.5K screen이 맞다.

### C. 현재 자료만으로는 당장 건드리지 않는 편이 나은 질문

`feet_air_time 0.25/0.30`, `joint_deviation_hip ±방향`, H1 `lin_vel_z_l2`다. feet/hip은 내부 정보가 이미 많아 다음 한 번의 GPU run이 추가할 정보가 작고, `lin_vel_z_l2`는 외부 H1 38건에서 아예 등장하지 않아 Go2 신호를 H1로 전이할 근거가 없다. 또한 `track_ang_vel_z_exp=0.75/1.0` large jump는 외부+내부 negative가 겹쳐 당장 재실험 우선도가 낮다.

## 9. 바로 실행할 가치가 높은 3~5개 실험 설계

| 실험 | 설계 | 판정/중단 기준 |
| --- | --- | --- |
| 0. 공통 prerequisite/control | 새 `+0.2 feet_air_time`, `termination=-50`의 corrected 1.5K parent를 확정하고, 그 parent에서 reward unchanged continuation을 동일 길이로 1회 확보 | 모든 sibling의 진짜 control을 하나로 공유. parent SHA/config/seed/evaluator 고정. 이 control 없이는 H-005~008 계보 문제를 반복함. |
| 1. LIN075 clean | 같은 parent에서 `track_lin_vel_xy_exp 0.5→0.75`만 변경, control과 같은 +1.5K | late-500 XY가 개선되면서 terrain·fall·yaw가 control 대비 악화하지 않으면 5K confirmation 후보. |
| 2. TERM100 matched | 같은 parent에서 `termination_penalty -50→-100`만 변경, control과 같은 +1.5K | base-contact/fall 개선이 yaw·XY·terrain 손실보다 큰지 판단. H-012의 unmatched gap을 닫음. |
| 3. YAW060 micro | 같은 parent에서 `track_ang_vel_z_exp 0.5→0.6`만 변경, control과 같은 +1.5K | yaw 개선과 terrain/fall 유지가 동시에 나오는지 확인. 0.75/1.0 large-step negative를 피함. |
| 4. ACTIONRATE short negative-control | 같은 parent에서 `action_rate_l2 -0.0005→-0.0025`만 변경. 우선 1K 구간을 screen하고 catastrophic stall이 없을 때만 동일 길이 완료 | 외부 single-dial 장기 collapse가 재현되는지 확인. terrain 0 고착/행동 정체/추종 악화 시 즉시 full-length 승격 금지. |
| 5. ANGVELXY010 (예산 남을 때) | 같은 parent에서 `ang_vel_xy_l2 -0.05→-0.10` only | 요철/박스/밀침 안정성 gain이 있는지 확인. flat_orientation보다 먼저 보는 이유는 외부에서 -0.10 반복 관측되고 내부 H1 clean evidence가 0이기 때문. |

### 공통 판정 규칙

- **same parent checkpoint**: parent 파일/SHA를 모든 sibling에 동일하게 사용.
- **unchanged control**: 같은 parent에서 reward를 바꾸지 않은 continuation을 반드시 확보하고 여러 sibling이 공유.
- **same seed / same additional iterations / same env source**: 단, 내부 자료상 terrain generator seed가 `null`일 수 있으므로 training seed 동일만으로 완전한 paired terrain을 보장한다고 쓰지 않는다.
- **same evaluator / terrain test**: 학습 후 동일 fixed evaluator 또는 동일한 격리 terrain/command suite로 비교. 가능하면 evaluator seed·scenario version을 고정.
- **late-window 우선**: endpoint 1점보다 마지막 300/500 iteration의 terrain, fall/base-contact, XY/yaw, episode length, action std를 함께 본다.
- **reward peak 비우선**: reward coefficient가 달라지는 branch끼리 `Train/mean_reward` 절댓값으로 승자를 고르지 않는다.
- **영상 provenance**: final numbered checkpoint에서 fresh video를 만들고 source checkpoint를 명시. 기존 stale MP4/자동 `model_best` 이름만으로 동작을 연결하지 않는다.

### 실행 순서 제안

GPU 예산이 아주 제한적이면 **control → LIN075 → TERM100** 순서가 가장 효율적이다. 여유가 있으면 **YAW060 → ACTIONRATE short screen**을 이어 붙인다. 이유는 LIN075가 공식 점수의 전진 공백과 내부 계보 공백을 동시에 해결하고, TERM100은 H-012의 가장 큰 비교 결손을 닫으며, YAW060은 large-step negative를 피하면서 남은 yaw 병목만 겨냥하기 때문이다. ACTIONRATE는 upside 최적화보다 **위험영역 확인용 negative-control** 성격이 강하므로 짧게 보는 편이 낫다.

## 10. 분석의 한계와 아직 필요한 데이터

1. **38 H1 keys ≠ 38 독립 정책**이다. `reel-11659221`과 `reel-87278881`은 reward dial과 모든 주요 stats가 동일하다. 또 `reel-14106372`와 `reel-12918663`은 exact dial vector를 공유하지만 terrain/checkpoint가 다르다. 공개 데이터가 같은 policy를 여러 terrain에서 재사용했는지 식별할 parent/policy hash가 없다.
2. **성공 34건에는 detail/reward가 비어 있어 실패-vs-성공 parameter contrast를 만들 수 없다.** 따라서 이 보고서의 parameter region은 “실패 관찰에서 본 경고/질문 후보”이지 성공 범위의 complement가 아니다.
3. **fall-rate window가 통일되지 않았다.** 18 H1 rows는 마지막10회 평균, 20 rows는 마지막 값이다. 같은 percentage라도 noise 특성이 다를 수 있다.
4. **terrain start/direction이 20/38에서 미기록**이다. 명시되지 않은 start를 3.4로 가정하지 않았다.
5. **checkpoint iteration과 total train iteration이 다르다.** 대표적으로 `reel-14243203`은 checkpoint0/total10, `reel-36602380`은 1000/3000, `reel-11806238`은 1300/2155다. 이 차이를 무시하면 “학습량” 해석이 틀어진다.
6. **외부 reward 다중 변경이 지배적**이다. H1 38건 중 single-dial은 5건뿐이고, 22건은 reward 변경이 5개 이상이다. co-occurrence를 인과로 해석하지 않았다.
7. **`why`, `severity`, `bias`는 독립 label이 아니다.** stats/dials에서 파생된 자동 진단일 수 있어 metric과 중복된 정보를 담는다.
8. **내부 H-005~H-011은 lineage correction 이후 HOLD**다. H-009~011은 historical H-008 configuration 안에서는 single sibling이 맞지만 corrected +0.2 parent 계보에서 재확인이 필요하다. H-012도 fresh -100 single change이지만 matched PERSONAL control이 없다.
9. **OFFICIAL vs PERSONAL을 섞어 causal effect로 계산하지 않았다.** OFFICIAL TERM50과 PERSONAL baseline/H-012 간 차이는 방향 참고일 뿐 paired causal estimate가 아니다.
10. **추가로 가장 필요한 데이터**는 corrected +0.2 TERM50 parent의 unchanged continuation, 각 sibling의 fixed evaluator 결과, evaluator seed/scenario version, late-window action std/XY/yaw/fall 시계열, 그리고 final checkpoint에 직접 연결된 fresh video다.

---

# 부록 A. H1 38건 정규화 전수표

아래 표는 요청한 필드를 가능한 범위에서 모두 정규화한 것이다. `terrain start→end`의 시작값/방향은 원자료가 명시할 때만 기록했다. `reward 변경 수`는 `actual_dial_count`/원본 `dials` 기준이다.

| key | 날짜 | 지형군 | 원본 terrain | failure reason | checkpoint/total iter | best reward @ iter | terrain start→end | fall rate(window) | std | severity | reward 변경 수 | 변경 reward | bias | why |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| reel-82918128 | 2026-08-18 | 기타 특수 지형 | 복합 — 모든 지형 (학습 그대로) | 학습 부족 | 999 / 999 | 4.70 @ 959 | —→0.00 (미기록) | 80.0% (마지막) | 0.890 | bad | 2 | `track_lin_vel_xy_exp` 0.5→0.7<br>`track_ang_vel_z_exp` 0.5→0.9 | 공격/적극 지향 — 속도↑ | 🔴 절반 이상 넘어짐 — 거의 못 걷는 정책. \| 🔴 지형 난이도가 0 수준 — 평지조차 제대로 못 걸어 난이도가 안 올라감(주저앉기·STUCK 의심). |
| reel-87239593 | 2026-08-19 | 징검다리/레일 | 레일 | 학습에 없던 지형 | 9500 / 9999 | 19.95 @ 9529 | —→5.97 (미기록) | 21.0% (마지막) | 1.243 | warn | 8 | `track_lin_vel_xy_exp` 0.5→2<br>`track_ang_vel_z_exp` 0.5→1<br>`feet_air_time` 0.2→0.28<br>`flat_orientation_l2` -1.5→-0.3<br>`joint_deviation_hip` -0.2→-0.15<br>`joint_deviation_torso` -0.1→-0.03<br>`action_rate_l2` -0.0005→-0.0075<br>`termination_penalty` -5→-150 | 공격/적극 지향 — 속도↑·발들기↑(등반)·자세자유↑(과감)·안전↑ | ⚠️ 자주 넘어짐 — 불안정. 안정 쪽 보상 검토. \| ⚠️ 탐색 std 가 초기값(1.0) 수준 — 거의 학습이 안 됨(iter 부족 의심). |
| reel-87278881 | 2026-08-20 | 회전 추종 | 회전 복합 추종 | 학습 부족 | 4600 / 4999 | 6.07 @ 4602 | —→5.92 (미기록) | 22.8% (마지막) | 1.572 | warn | 7 | `track_lin_vel_xy_exp` 0.5→1.25<br>`track_ang_vel_z_exp` 0.5→1<br>`feet_air_time` 0.2→0.22<br>`flat_orientation_l2` -1.5→-0.9<br>`ang_vel_xy_l2` -0.05→-0.08<br>`action_rate_l2` -0.0005→-0.002<br>`termination_penalty` -5→-180 | 공격/적극 지향 — 속도↑·발들기↑(등반)·자세자유↑(과감)·안전↑ | ⚠️ 자주 넘어짐 — 불안정. 안정 쪽 보상 검토. \| ⚠️ 탐색 std 가 초기값(1.0) 수준 — 거의 학습이 안 됨(iter 부족 의심). |
| reel-87505560 | 2026-08-20 | 구덩이/틈 | 구덩이 | 학습에 없던 지형 | 2900 / 2999 | 6.26 @ 2933 | —→5.43 (미기록) | 31.3% (마지막) | 1.072 | warn | 9 | `track_lin_vel_xy_exp` 0.5→0.8<br>`track_ang_vel_z_exp` 0.5→0.55<br>`feet_air_time` 0.2→0.25<br>`flat_orientation_l2` -1.5→-1.8<br>`joint_deviation_hip` -0.2→-0.25<br>`joint_deviation_torso` -0.1→-0.15<br>`ang_vel_xy_l2` -0.05→-0.1<br>`action_rate_l2` -0.0005→-0.002<br>`termination_penalty` -5→-50 | 균형(혼합) — 속도↑·발들기↑(등반)·자세안정↑(꼿꼿)·안전↑ | ⚠️ 자주 넘어짐 — 불안정. 안정 쪽 보상 검토. \| ⚠️ 탐색 std 가 초기값(1.0) 수준 — 거의 학습이 안 됨(iter 부족 의심). |
| reel-11309747 | 2026-08-20 | 기타 특수 지형 | 떠 있는 고리 | 학습 부족 | 999 / 999 | 1.61 @ 956 | —→4.82 (미기록) | 32.4% (마지막) | 1.319 | warn | 1 | `termination_penalty` -5→-50 | 안정 지향 — 안전↑ | ⚠️ 자주 넘어짐 — 불안정. 안정 쪽 보상 검토. \| ⚠️ 탐색 std 가 1.0 근처인데 지형·낙상 지표는 정상 — 학습은 됐지만 무작위성이 안 줄었습니다(엔트로피 과다). |
| reel-11659221 | 2026-08-20 | 회전 추종 | 회전 복합 추종 | 학습 부족 | 4600 / 4999 | 6.07 @ 4602 | —→5.92 (미기록) | 22.8% (마지막) | 1.572 | warn | 7 | `track_lin_vel_xy_exp` 0.5→1.25<br>`track_ang_vel_z_exp` 0.5→1<br>`feet_air_time` 0.2→0.22<br>`flat_orientation_l2` -1.5→-0.9<br>`ang_vel_xy_l2` -0.05→-0.08<br>`action_rate_l2` -0.0005→-0.002<br>`termination_penalty` -5→-180 | 공격/적극 지향 — 속도↑·발들기↑(등반)·자세자유↑(과감)·안전↑ | ⚠️ 자주 넘어짐 — 불안정. 안정 쪽 보상 검토. \| ⚠️ 탐색 std 가 초기값(1.0) 수준 — 거의 학습이 안 됨(iter 부족 의심). |
| reel-11806238 | 2026-08-19 | 징검다리/레일 | 징검다리 | 학습에 없던 지형 | 1300 / 2155 | -5.87 @ 1274 | —→5.12 (미기록) | 21.7% (마지막) | 2.066 | warn | 1 | `termination_penalty` -5→-200 | 안정 지향 — 안전↑ | ⚠️ 자주 넘어짐 — 불안정. 안정 쪽 보상 검토. \| ⚠️ 탐색 std 가 초기값(1.0) 수준 — 거의 학습이 안 됨(iter 부족 의심). |
| reel-11999811 | 2026-08-21 | 계단/경사 | 계단 — 올라가기 | 학습 부족 | 900 / 1000 | 4.51 @ 902 | —→0.90 (미기록) | 76.5% (마지막) | 1.259 | bad | 1 | `track_lin_vel_xy_exp` 0.5→1 | 공격/적극 지향 — 속도↑ | 🔴 절반 이상 넘어짐 — 거의 못 걷는 정책. \| ⚠️ 탐색 std 가 초기값(1.0) 수준 — 거의 학습이 안 됨(iter 부족 의심). |
| reel-12918663 | 2026-08-21 | 징검다리/레일 | 징검다리 | 학습에 없던 지형 | 4900 / 5000 | 23.46 @ 4949 | —→5.83 (미기록) | 23.9% (마지막) | 1.036 | warn | 8 | `track_lin_vel_xy_exp` 0.5→1<br>`track_ang_vel_z_exp` 0.5→2<br>`feet_air_time` 0.2→0.35<br>`termination_penalty` -5→-150<br>`flat_orientation_l2` -1.5→-0.3<br>`joint_deviation_hip` -0.2→-0.15<br>`joint_deviation_torso` -0.1→-0.03<br>`action_rate_l2` -0.0005→-0.0075 | 공격/적극 지향 — 속도↑·발들기↑(등반·⚠️깽깽이)·자세자유↑(과감)·안전↑ | ⚠️ 자주 넘어짐 — 불안정. 안정 쪽 보상 검토. \| ⚠️ 탐색 std 가 1.0 근처인데 지형·낙상 지표는 정상 — 학습은 됐지만 무작위성이 안 줄었습니다(엔트로피 과다). |
| reel-14106372 | 2026-08-21 | 계단/경사 | 경사 — 내리막 | 균형 상실 | 9700 / 10000 | 26.61 @ 9658 | —→5.90 (미기록) | 21.5% (마지막) | 1.155 | warn | 8 | `track_lin_vel_xy_exp` 0.5→1<br>`track_ang_vel_z_exp` 0.5→2<br>`feet_air_time` 0.2→0.35<br>`termination_penalty` -5→-150<br>`flat_orientation_l2` -1.5→-0.3<br>`joint_deviation_hip` -0.2→-0.15<br>`joint_deviation_torso` -0.1→-0.03<br>`action_rate_l2` -0.0005→-0.0075 | 공격/적극 지향 — 속도↑·발들기↑(등반·⚠️깽깽이)·자세자유↑(과감)·안전↑ | ⚠️ 자주 넘어짐 — 불안정. 안정 쪽 보상 검토. \| ⚠️ 탐색 std 가 1.0 근처인데 지형·낙상 지표는 정상 — 학습은 됐지만 무작위성이 안 줄었습니다(엔트로피 과다). |
| reel-14243203 | 2026-08-21 | 속도 추종 | 좌우 속도 추종 | 학습 부족 | 0 / 10 | -0.19 @ 0 | —→0.82 (미기록) | 100.0% (마지막) | 0.991 | bad | 0 | 없음(원본 dials 비어 있음) | 균형(혼합) — 기본값 그대로 | 🔴 학습을 10 회만 돌렸습니다 — 체크포인트는 100 회마다 저장되므로 제출 파일이 사실상 '학습이 반영되지 않은 초기 가중치' 입니다. \| → 아래 지표(지형 난이도·낙상률·탐색 std)는 이 횟수에서는 판단 근거가 못 됩니다. 동작 확인용 짧은 실행이었다면 정상입니다. |
| reel-14325580 | 2026-08-21 | 구덩이/틈 | 틈 뛰어넘기 | 학습에 없던 지형 | 9500 / 10000 | 5.95 @ 9470 | —→5.85 (미기록) | 20.8% (마지막) | 1.642 | warn | 8 | `track_lin_vel_xy_exp` 0.5→1<br>`track_ang_vel_z_exp` 0.5→0.8<br>`feet_air_time` 0.2→0.3<br>`termination_penalty` -5→-150<br>`flat_orientation_l2` -1.5→-0.5<br>`joint_deviation_hip` -0.2→-0.3<br>`joint_deviation_torso` -0.1→-0.2<br>`action_rate_l2` -0.0005→-0.001 | 공격/적극 지향 — 속도↑·발들기↑(등반)·자세자유↑(과감)·안전↑ | ⚠️ 자주 넘어짐 — 불안정. 안정 쪽 보상 검토. \| ⚠️ 탐색 std 가 1.0 근처인데 지형·낙상 지표는 정상 — 학습은 됐지만 무작위성이 안 줄었습니다(엔트로피 과다). |
| reel-19129897 | 2026-08-21 | 구덩이/틈 | 구덩이 | 학습 부족 | 999 / 1000 | 3.74 @ 986 | —→0.43 (미기록) | 82.9% (마지막) | 1.258 | bad | 2 | `track_lin_vel_xy_exp` 0.5→1<br>`feet_air_time` 0.2→0.25 | 공격/적극 지향 — 속도↑·발들기↑(등반) | 🔴 절반 이상 넘어짐 — 거의 못 걷는 정책. \| 🔴 지형 난이도가 0 수준 — 평지조차 제대로 못 걸어 난이도가 안 올라감(주저앉기·STUCK 의심). \| ⚠️ 탐색 std 가 초기값(1.0) 수준 — 거의 학습이 안 됨(iter 부족 의심). |
| reel-22863265 | 2026-08-21 | 구덩이/틈 | 구덩이 | 학습에 없던 지형 | 7500 / 8400 | 10.10 @ 7509 | —→5.83 (미기록) | 18.5% (마지막) | 1.177 | warn | 8 | `track_ang_vel_z_exp` 0.5→1.5<br>`feet_air_time` 0.2→0.25<br>`termination_penalty` -5→-300<br>`flat_orientation_l2` -1.5→-2.5<br>`ang_vel_xy_l2` -0.05→-0.25<br>`joint_deviation_hip` -0.2→-0.4<br>`joint_deviation_torso` -0.1→-0.15<br>`action_rate_l2` -0.0005→-0.004 | 안정 지향 — 발들기↑(등반)·자세안정↑(꼿꼿)·안전↑ | ⚠️ 탐색 std 가 1.0 근처인데 지형·낙상 지표는 정상 — 학습은 됐지만 무작위성이 안 줄었습니다(엔트로피 과다). |
| reel-59781704 | 2026-08-20 | 요철/거친 지형 | 물결 | 학습 부족 | 999 / 999 | 4.84 @ 993 | —→1.31 (미기록) | 71.0% (마지막) | 1.266 | bad | 2 | `track_lin_vel_xy_exp` 0.5→1<br>`flat_orientation_l2` -1.5→-1.6 | 균형(혼합) — 속도↑·자세안정↑(꼿꼿) | 🔴 절반 이상 넘어짐 — 거의 못 걷는 정책. \| ⚠️ 탐색 std 가 1.0 근처인데 지형·낙상 지표는 정상 — 학습은 됐지만 무작위성이 안 줄었습니다(엔트로피 과다). |
| reel-60061435 | 2026-08-21 | 요철/거친 지형 | 거친 요철 | 학습 부족 | 999 / 1000 | 4.67 @ 968 | —→0.01 (미기록) | 83.1% (마지막) | 0.763 | bad | 1 | `track_ang_vel_z_exp` 0.5→1 | 균형(혼합) — 기본값 그대로 | 🔴 절반 이상 넘어짐 — 거의 못 걷는 정책. \| 🔴 지형 난이도가 0 수준 — 평지조차 제대로 못 걸어 난이도가 안 올라감(주저앉기·STUCK 의심). |
| reel-60491775 | 2026-08-21 | 구덩이/틈 | 틈 뛰어넘기 | 학습에 없던 지형 | 9300 / 9999 | 18.03 @ 9346 | —→5.86 (미기록) | 22.3% (마지막) | 1.236 | warn | 5 | `track_lin_vel_xy_exp` 0.5→2<br>`track_ang_vel_z_exp` 0.5→1<br>`termination_penalty` -5→-150<br>`flat_orientation_l2` -1.5→-0.3<br>`action_rate_l2` -0.0005→-0.005 | 공격/적극 지향 — 속도↑·자세자유↑(과감)·안전↑ | ⚠️ 자주 넘어짐 — 불안정. 안정 쪽 보상 검토. \| ⚠️ 탐색 std 가 1.0 근처인데 지형·낙상 지표는 정상 — 학습은 됐지만 무작위성이 안 줄었습니다(엔트로피 과다). |
| reel-88114018 | 2026-09-05 | 징검다리/레일 | 레일 | 학습에 없던 지형 | 9999 / 10000 | -4.84 @ 9992 | 3.4→5.57 (상승) | 14.9% (마지막 10회 평균) | 1.424 | warn | 2 | `termination_penalty` -5→-250<br>`action_rate_l2` -0.0005→-0.002 | 안정 지향 — 안전↑ | ⚠️ 탐색 std 가 1.0 근처인데 낙상률은 정상 — 학습은 됐지만 무작위성이 안 줄었습니다(엔트로피 과다). |
| reel-92451333 | 2026-09-04 | 구덩이/틈 | 틈 뛰어넘기 | 학습에 없던 지형 | 5700 / 6000 | 4.58 @ 5742 | 3.4→5.95 (상승) | 21.7% (마지막 10회 평균) | 1.225 | warn | 7 | `track_lin_vel_xy_exp` 0.5→1<br>`track_ang_vel_z_exp` 0.5→1<br>`feet_air_time` 0.2→0.25<br>`termination_penalty` -5→-200<br>`flat_orientation_l2` -1.5→-1<br>`ang_vel_xy_l2` -0.05→-0.02<br>`action_rate_l2` -0.0005→-0.004 | 공격/적극 지향 — 속도↑·발들기↑(등반)·자세자유↑(과감)·안전↑ | ⚠️ 자주 넘어짐 — 불안정. 안정 쪽 보상 검토. \| ⚠️ 탐색 std 가 1.0 근처 — 무작위성이 안 줄었습니다. 위의 높은 낙상률과 함께 보면 아직 안정된 보행을 못 찾은 상태입니다. |
| reel-92770425 | 2026-09-06 | 계단/경사 | 완만한 경사 ±10° | 관절 떨림 | 5500 / 6000 | -3.70 @ 5520 | 3.4→3.67 (상승) | 16.1% (마지막 10회 평균) | 2.325 | warn | 2 | `feet_air_time` 0.2→0.12<br>`termination_penalty` -5→-200 | 안정 지향 — 발들기↓(평지안정)·안전↑ | ⚠️ 탐색 std 가 1.0 근처인데 낙상률은 정상 — 학습은 됐지만 무작위성이 안 줄었습니다(엔트로피 과다). |
| reel-93015733 | 2026-09-04 | 기타 특수 지형 | 떠 있는 고리 | 학습에 없던 지형 | 4100 / 4300 | 11.23 @ 4061 | 3.4→5.73 (상승) | 28.2% (마지막 10회 평균) | 1.359 | warn | 6 | `track_lin_vel_xy_exp` 0.5→1.2<br>`track_ang_vel_z_exp` 0.5→1<br>`feet_air_time` 0.2→0.3<br>`termination_penalty` -5→-100<br>`ang_vel_xy_l2` -0.05→-0.1<br>`action_rate_l2` -0.0005→-0.002 | 공격/적극 지향 — 속도↑·발들기↑(등반)·안전↑ | ⚠️ 자주 넘어짐 — 불안정. 안정 쪽 보상 검토. \| ⚠️ 탐색 std 가 1.0 근처 — 무작위성이 안 줄었습니다. 위의 높은 낙상률과 함께 보면 아직 안정된 보행을 못 찾은 상태입니다. |
| reel-93039572 | 2026-09-04 | 계단/경사 | 계단 — 가파르게 (15~30cm) | 관절 떨림 | 8300 / 10000 | 4.58 @ 8311 | 3.4→3.74 (상승) | 12.9% (마지막 10회 평균) | 2.593 | warn | 2 | `track_lin_vel_xy_exp` 0.5→1<br>`termination_penalty` -5→-200 | 균형(혼합) — 속도↑·안전↑ | ⚠️ 탐색 std 가 1.0 근처인데 낙상률은 정상 — 학습은 됐지만 무작위성이 안 줄었습니다(엔트로피 과다). |
| reel-97191601 | 2026-08-21 | 징검다리/레일 | 징검다리 | 학습에 없던 지형 | 1400 / 1500 | 4.42 @ 1399 | —→4.74 (미기록) | 28.8% (마지막) | 1.713 | warn | 5 | `track_lin_vel_xy_exp` 0.5→1<br>`feet_air_time` 0.2→0.25<br>`termination_penalty` -5→-75<br>`ang_vel_xy_l2` -0.05→-0.1<br>`joint_deviation_hip` -0.2→-0.25 | 공격/적극 지향 — 속도↑·발들기↑(등반)·안전↑ | ⚠️ 자주 넘어짐 — 불안정. 안정 쪽 보상 검토. \| ⚠️ 탐색 std 가 1.0 근처인데 지형·낙상 지표는 정상 — 학습은 됐지만 무작위성이 안 줄었습니다(엔트로피 과다). |
| reel-97541917 | 2026-09-04 | 요철/거친 지형 | 약한 요철 | 관절 떨림 | 9600 / 10000 | 8.71 @ 9570 | 3.4→5.84 (상승) | 14.6% (마지막 10회 평균) | 2.720 | warn | 8 | `track_lin_vel_xy_exp` 0.5→1.25<br>`track_ang_vel_z_exp` 0.5→1<br>`termination_penalty` -5→-300<br>`flat_orientation_l2` -1.5→-0.75<br>`ang_vel_xy_l2` -0.05→-0.04<br>`joint_deviation_hip` -0.2→-0.1<br>`joint_deviation_torso` -0.1→-0.05<br>`action_rate_l2` -0.0005→-0.001 | 공격/적극 지향 — 속도↑·자세자유↑(과감)·안전↑ | ⚠️ 탐색 std 가 1.0 근처인데 낙상률은 정상 — 학습은 됐지만 무작위성이 안 줄었습니다(엔트로피 과다). |
| reel-8908141 | 2026-09-02 | 징검다리/레일 | 징검다리 | 학습에 없던 지형 | 5900 / 5999 | -0.42 @ 5936 | 3.4→5.77 (상승) | 24.5% (마지막 10회 평균) | 1.430 | warn | 3 | `track_lin_vel_xy_exp` 0.5→0.7<br>`termination_penalty` -5→-150<br>`action_rate_l2` -0.0005→-0.0015 | 균형(혼합) — 속도↑·안전↑ | ⚠️ 자주 넘어짐 — 불안정. 안정 쪽 보상 검토. \| ⚠️ 탐색 std 가 1.0 근처 — 무작위성이 안 줄었습니다. 위의 높은 낙상률과 함께 보면 아직 안정된 보행을 못 찾은 상태입니다. |
| reel-8945010 | 2026-09-02 | 구덩이/틈 | 틈 뛰어넘기 | 학습에 없던 지형 | 11000 / 11699 | 10.38 @ 10989 | 3.4→5.83 (상승) | 24.7% (마지막 10회 평균) | 1.405 | warn | 4 | `track_lin_vel_xy_exp` 0.5→0.7<br>`track_ang_vel_z_exp` 0.5→0.8<br>`termination_penalty` -5→-50<br>`joint_deviation_hip` -0.2→-0.4 | 균형(혼합) — 속도↑·안전↑ | ⚠️ 자주 넘어짐 — 불안정. 안정 쪽 보상 검토. \| ⚠️ 탐색 std 가 1.0 근처 — 무작위성이 안 줄었습니다. 위의 높은 낙상률과 함께 보면 아직 안정된 보행을 못 찾은 상태입니다. |
| reel-9050001 | 2026-09-02 | 박스 단차 | 박스 단차 — 극한 (10~35cm) | 균형 상실 | 4900 / 5000 | 12.98 @ 4948 | 3.4→5.98 (상승) | 22.0% (마지막 10회 평균) | 2.441 | warn | 8 | `track_lin_vel_xy_exp` 0.5→1.25<br>`track_ang_vel_z_exp` 0.5→1<br>`termination_penalty` -5→-200<br>`flat_orientation_l2` -1.5→-0.75<br>`ang_vel_xy_l2` -0.05→-0.03<br>`joint_deviation_hip` -0.2→-0.1<br>`joint_deviation_torso` -0.1→-0.05<br>`action_rate_l2` -0.0005→-0.001 | 공격/적극 지향 — 속도↑·자세자유↑(과감)·안전↑ | ⚠️ 자주 넘어짐 — 불안정. 안정 쪽 보상 검토. \| ⚠️ 탐색 std 가 1.0 근처 — 무작위성이 안 줄었습니다. 위의 높은 낙상률과 함께 보면 아직 안정된 보행을 못 찾은 상태입니다. |
| reel-74319272 | 2026-09-01 | 요철/거친 지형 | 거친 요철 | 균형 상실 | 7800 / 9000 | 21.65 @ 7831 | 3.4→5.82 (상승) | 27.3% (마지막 10회 평균) | 2.286 | warn | 8 | `track_lin_vel_xy_exp` 0.5→2<br>`track_ang_vel_z_exp` 0.5→1<br>`feet_air_time` 0.2→0.5<br>`termination_penalty` -5→-40<br>`flat_orientation_l2` -1.5→-1<br>`ang_vel_xy_l2` -0.05→-0.2<br>`joint_deviation_torso` -0.1→-0.25<br>`action_rate_l2` -0.0005→-0.0006 | 공격/적극 지향 — 속도↑·발들기↑(등반·⚠️깽깽이)·자세자유↑(과감)·안전↑ | ⚠️ 자주 넘어짐 — 불안정. 안정 쪽 보상 검토. \| ⚠️ 탐색 std 가 1.0 근처 — 무작위성이 안 줄었습니다. 위의 높은 낙상률과 함께 보면 아직 안정된 보행을 못 찾은 상태입니다. |
| reel-74375233 | 2026-09-01 | 기타 특수 지형 | 떠 있는 고리 | 학습에 없던 지형 | 9500 / 10000 | 7.29 @ 9471 | 3.4→5.92 (상승) | 20.3% (마지막 10회 평균) | 1.096 | warn | 6 | `track_lin_vel_xy_exp` 0.5→1<br>`track_ang_vel_z_exp` 0.5→1<br>`feet_air_time` 0.2→0.25<br>`termination_penalty` -5→-200<br>`flat_orientation_l2` -1.5→-1<br>`action_rate_l2` -0.0005→-0.005 | 공격/적극 지향 — 속도↑·발들기↑(등반)·자세자유↑(과감)·안전↑ | ⚠️ 자주 넘어짐 — 불안정. 안정 쪽 보상 검토. \| ⚠️ 탐색 std 가 1.0 근처 — 무작위성이 안 줄었습니다. 위의 높은 낙상률과 함께 보면 아직 안정된 보행을 못 찾은 상태입니다. |
| reel-74420401 | 2026-09-01 | 구덩이/틈 | 구덩이 | 학습에 없던 지형 | 4700 / 5000 | 6.10 @ 4716 | 3.4→5.66 (상승) | 26.0% (마지막 10회 평균) | 2.097 | warn | 6 | `track_lin_vel_xy_exp` 0.5→1.35<br>`feet_air_time` 0.2→0.22<br>`termination_penalty` -5→-140<br>`flat_orientation_l2` -1.5→-1.2<br>`ang_vel_xy_l2` -0.05→-0.1<br>`joint_deviation_torso` -0.1→-0.15 | 공격/적극 지향 — 속도↑·발들기↑(등반)·자세자유↑(과감)·안전↑ | ⚠️ 자주 넘어짐 — 불안정. 안정 쪽 보상 검토. \| ⚠️ 탐색 std 가 1.0 근처 — 무작위성이 안 줄었습니다. 위의 높은 낙상률과 함께 보면 아직 안정된 보행을 못 찾은 상태입니다. |
| reel-77658123 | 2026-08-19 | 속도 추종 | 좌우 속도 추종 | 학습 부족 | 4999 / 4999 | 8.46 @ 4996 | —→5.49 (미기록) | 22.5% (마지막) | 1.559 | warn | 7 | `track_lin_vel_xy_exp` 0.5→1.35<br>`track_ang_vel_z_exp` 0.5→1<br>`feet_air_time` 0.2→0.24<br>`flat_orientation_l2` -1.5→-0.9<br>`ang_vel_xy_l2` -0.05→-0.08<br>`action_rate_l2` -0.0005→-0.002<br>`termination_penalty` -5→-180 | 공격/적극 지향 — 속도↑·발들기↑(등반)·자세자유↑(과감)·안전↑ | ⚠️ 자주 넘어짐 — 불안정. 안정 쪽 보상 검토. \| ⚠️ 탐색 std 가 초기값(1.0) 수준 — 거의 학습이 안 됨(iter 부족 의심). |
| reel-77755064 | 2026-08-19 | 구덩이/틈 | 틈 뛰어넘기 | 학습에 없던 지형 | 4300 / 4999 | 12.31 @ 4337 | —→5.73 (미기록) | 27.5% (마지막) | 1.563 | warn | 9 | `track_lin_vel_xy_exp` 0.5→1.2<br>`track_ang_vel_z_exp` 0.5→1<br>`feet_air_time` 0.2→0.25<br>`flat_orientation_l2` -1.5→-2<br>`joint_deviation_hip` -0.2→-0.3<br>`joint_deviation_torso` -0.1→-0.2<br>`ang_vel_xy_l2` -0.05→-0.15<br>`action_rate_l2` -0.0005→-0.001<br>`termination_penalty` -5→-80 | 균형(혼합) — 속도↑·발들기↑(등반)·자세안정↑(꼿꼿)·안전↑ | ⚠️ 자주 넘어짐 — 불안정. 안정 쪽 보상 검토. \| ⚠️ 탐색 std 가 초기값(1.0) 수준 — 거의 학습이 안 됨(iter 부족 의심). |
| reel-77873715 | 2026-09-02 | 속도 추종 | 좌우 속도 추종 | 균형 상실 | 3900 / 5700 | 0.88 @ 3903 | 3.4→5.81 (상승) | 23.3% (마지막 10회 평균) | 1.112 | warn | 2 | `termination_penalty` -5→-150<br>`action_rate_l2` -0.0005→-0.003 | 안정 지향 — 안전↑ | ⚠️ 자주 넘어짐 — 불안정. 안정 쪽 보상 검토. \| ⚠️ 탐색 std 가 1.0 근처 — 무작위성이 안 줄었습니다. 위의 높은 낙상률과 함께 보면 아직 안정된 보행을 못 찾은 상태입니다. |
| reel-78059501 | 2026-09-02 | 구덩이/틈 | 구덩이 | 학습에 없던 지형 | 4600 / 5000 | 6.58 @ 4566 | 3.4→5.65 (상승) | 25.6% (마지막 10회 평균) | 1.785 | warn | 6 | `track_lin_vel_xy_exp` 0.5→1.35<br>`feet_air_time` 0.2→0.22<br>`termination_penalty` -5→-140<br>`flat_orientation_l2` -1.5→-1.2<br>`ang_vel_xy_l2` -0.05→-0.1<br>`action_rate_l2` -0.0005→-0.001 | 공격/적극 지향 — 속도↑·발들기↑(등반)·자세자유↑(과감)·안전↑ | ⚠️ 자주 넘어짐 — 불안정. 안정 쪽 보상 검토. \| ⚠️ 탐색 std 가 1.0 근처 — 무작위성이 안 줄었습니다. 위의 높은 낙상률과 함께 보면 아직 안정된 보행을 못 찾은 상태입니다. |
| reel-78293289 | 2026-09-02 | 기타 특수 지형 | 떠 있는 고리 | 학습에 없던 지형 | 3800 / 4000 | 0.00 @ 3826 | 3.4→5.79 (상승) | 25.7% (마지막 10회 평균) | 1.001 | warn | 4 | `track_lin_vel_xy_exp` 0.5→0.8<br>`track_ang_vel_z_exp` 0.5→0.8<br>`termination_penalty` -5→-200<br>`action_rate_l2` -0.0005→-0.008 | 균형(혼합) — 속도↑·안전↑ | ⚠️ 자주 넘어짐 — 불안정. 안정 쪽 보상 검토. \| ⚠️ 탐색 std 가 1.0 근처 — 무작위성이 안 줄었습니다. 위의 높은 낙상률과 함께 보면 아직 안정된 보행을 못 찾은 상태입니다. |
| reel-78339600 | 2026-09-03 | 기타 특수 지형 | 복합 — 모든 지형 (학습 그대로) | 관절 떨림 | 4900 / 5000 | 3.16 @ 4856 | 3.4→5.20 (상승) | 15.6% (마지막 10회 평균) | 2.168 | warn | 8 | `track_lin_vel_xy_exp` 0.5→1.25<br>`track_ang_vel_z_exp` 0.5→1<br>`termination_penalty` -5→-300<br>`flat_orientation_l2` -1.5→-0.75<br>`ang_vel_xy_l2` -0.05→-0.03<br>`joint_deviation_hip` -0.2→-0.1<br>`joint_deviation_torso` -0.1→-0.05<br>`action_rate_l2` -0.0005→-0.0015 | 공격/적극 지향 — 속도↑·자세자유↑(과감)·안전↑ | ⚠️ 탐색 std 가 1.0 근처인데 낙상률은 정상 — 학습은 됐지만 무작위성이 안 줄었습니다(엔트로피 과다). |
| reel-78394459 | 2026-09-02 | 기타 특수 지형 | 기둥 숲 | 학습에 없던 지형 | 4300 / 5000 | 0.42 @ 4288 | 3.4→0.00 (하락) | 100.0% (마지막 10회 평균) | 0.419 | bad | 1 | `action_rate_l2` -0.0005→-0.0025 | 균형(혼합) — 기본값 그대로 | 🔴 절반 이상 넘어짐 — 거의 못 걷는 정책. \| 🔴 지형 난이도가 0 수준 — 평지조차 제대로 못 걸어 난이도가 안 올라감(주저앉기·STUCK 의심). |
| reel-36602380 | 2026-09-22 | 구덩이/틈 | 구덩이 | 학습에 없던 지형 | 1000 / 3000 | 4.77 @ 951 | 3.4→5.32 (상승) | 25.4% (마지막 10회 평균) | 2.798 | warn | 7 | `track_lin_vel_xy_exp` 0.5→1.4<br>`track_ang_vel_z_exp` 0.5→1<br>`termination_penalty` -5→-200<br>`ang_vel_xy_l2` -0.05→-0.1<br>`joint_deviation_hip` -0.2→-0.3<br>`joint_deviation_torso` -0.1→-0.15<br>`action_rate_l2` -0.0005→-0.0002 | 균형(혼합) — 속도↑·안전↑ | ⚠️ 자주 넘어짐 — 불안정. 안정 쪽 보상 검토. \| ⚠️ 탐색 std 가 1.0 근처 — 무작위성이 안 줄었습니다. 위의 높은 낙상률과 함께 보면 아직 안정된 보행을 못 찾은 상태입니다. |

# 부록 B. 분석 재현에 사용한 원본 파일

- `04_failure_runs.csv`
- `05_failure_reward_dials.csv`
- `06_failure_stats_long.csv`
- `07_failure_reward_matrix.csv`
- `NCRC_H1_failures_38_full.json`
- `videos.json`
- `ANALYSIS_TASKS.md`
- 내부: `00_START_HERE_CONTEXT_AND_MAP`, `06_HUMANOID_TRAINING_CODE`, `13_H1_OFFICIAL_SERVER_BASELINE_EVIDENCE`, `14_H1_NEXT_RUN_PARAMETER_COMPARISON`, `15_OPTUNA_REWARD_DECISION_ENGINE`, `17_H1_PERSONAL_SERVER_LONG_RUN_EVIDENCE`, `18_H1_FINALIZE_REPORT_LIMITATIONS`

# 최종 결론

외부 45개 상세 실패 관찰(그중 H1 38개)의 가장 큰 가치는 “남들이 어떤 값을 썼다”가 아니라 **우리 내부에서 아직 깨끗하게 답하지 못한 질문을 골라내는 것**이다. 다음 H1 실험의 정보가치만 보면 우선순위는 **(1) corrected-parent `track_lin 0.75` clean test → (2) matched `termination -100` → (3) yaw 0.6 micro-step → (4) action-rate -0.0025 short negative-control → (5) ang_vel_xy -0.10 screen** 순이다. feet-air-time/hip은 기존 내부 evidence가 상대적으로 많아 뒤로 미루는 편이 합리적이다.
