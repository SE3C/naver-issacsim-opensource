> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/experiments/h1/analysis/2026-10-10_H1_SCENARIO7_RAW_3POLICY_MATCHED_ANALYSIS.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# [분석] H1 `TERM-50` vs `ORIENT-100` vs `ACTRATE-0001` — 원본 9,216 episode 직접 대조 (2026-10-10)

> 관리 안내 (2026-10-13): **분석** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](<../../../../research/EXPERIMENTS.md>)를 확인한다.

**재현용 수치 산출물 (이번 정합성 점검에서 추가 수납):** [raw case summary JSON](<../2026-10-10_H1_SCENARIO7_RAW_SUMMARY.json>) (12,090 bytes; SHA-256 `be02c5cf2c47e3844dddd46cc4d9276d6ce6786c718d549d44359ceb14849aee`) · [paired cohort delta JSON](<../2026-10-10_H1_SCENARIO7_PAIRED_DELTAS.json>) (42,907 bytes; SHA-256 `c3fb1977d0accab92d42675842bd659868a4b464d85896a026e3946af8d2c76a`). 두 JSON은 당시 계산한 원본 byte 그대로 수납했고, JSON parse 및 Git blob 동일성 검증을 통과했다. `n_b_lower/n_b_higher`는 통제된 독립 학습 반복이 아니라 일치하는 evaluator cohort **인덱스 수**다.

**판정:** 원본 ZIP 3개·3,072 rows/정책과 case/seed/env 대응 키를 직접 확인한 **Windows PERSONAL 동일 프로토콜 관측 비교 완료**. 전지형 대표 정책 **모두 HOLD**, 신규 학습·GPU 평가·OFFICIAL 채점/제출은 수행하지 않았다. 본 보고서는 이전 [보고서 기반 잠정 비교](https://github.com/SE3C/naver-issacsim/blob/main/data/processed/experiments/h1/2026-10-10_H1_SCENARIO7_CROSS_POLICY_REPORT_LEVEL_COMPARISON.md)의 *원자료 접근 불가* 상태를 **후속 ZIP 업로드로 해소한 별도 분석**이다.

## 1. 원본과 무결성·계보

| 정책(평가 checkpoint) | 학습 계보 | ZIP SHA-256 | 보존된 원본 GitHub Release |
|---|---|---|---|
| **TERM-50** (`model_2800.pt`) | `20261008-062732-h1-term-50-fresh3k-control` (OFFICIAL fresh3K) | `d4a47b0e182763e21077b688f44f7d9cdc00759c0f0f78f4217930e1c49975da` | [평가 ZIP](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261008-exp-h1-rough-terrain-orientation-relaxation-model2800-control-video-eval) |
| **ORIENT-100** (`model_2850.pt`) | `20261006-133517-h1-orient-100-fresh3k-official` (OFFICIAL fresh3K) | `aecc82b13671d54c96813af6c02c1b2a7769ee001b30aa4a5c2761457110eb7a` | [평가 ZIP](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261007-exp-h1-rough-terrain-orientation-relaxation-model2850-video-eval) |
| **ACTRATE-0001** (`model_2700.pt`) | `20261009-142350-h1-actrate-0001-fresh3k` (OFFICIAL fresh3K) | `6270d299def2a3bcb8cc10253027898621dd65a00ad30baafde0cbcde03076e3` | [평가 ZIP](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261010-exp-h1-action-rate-relaxation-model2700-video-eval) |

- 직접 읽은 3개 ZIP은 각 **18 entries**, `testzip()` **PASS**, GitHub에 기존 등록된 ZIP SHA-256 **전부 일치**. 정책 각각 `evaluation/episodes.jsonl` **3,072 rows**, 8개 case × **384 rows**, 평가 seed `4201·4202·4203` × env_id `0…127`; 중복 `(scenario,case,seed,env_id)` **0**, 각 정책 cohort key 집합과 `episode_id` **정확히 일치**. 모든 episode는 1,000 step / 20.0 s, timeout/survived, base-contact failure **0/3,072** (이 20초 창의 생존만 의미).
- **평가 설정 파리티 직접 확인:** `evaluation/resolved_configs.json` **3개 바이너리 내용 동일**, `evaluation/evaluation_manifest.json`의 `protocol` 구조 **완전 동일**, agent config fingerprint·source fingerprints·24개 `(case,seed)`의 적용 env config fingerprints **동일**. Deterministic actor, camera-off, 같은 command·disturbance schedule, fixed `scenario7` protocol SHA `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34`. 체크포인트 SHA는 ZIP manifest와 별도 OFFICIAL 기록의 identity와 부합. ZIP의 `policy.source_run_id/preset=null`은 그대로 유지하며 OFFICIAL Run 연결은 **별도 기록·해시**를 근거로 함.
- **중요한 범위:** 평가 protocol/설정/코호트 키가 일치한다는 것은 일관된 인덱스 비교의 근거이나, runtime 난수 소비·reset 직후 상태·실제 각 tile 배치/물리 trajectory가 정책별로 *바이트 동일*함을 증명하지는 않는다. 훈련 당시 전체 task/PPO provenance도 평가 ZIP만으로는 증명하지 못한다. 전체 3,072개 환경을 독립 training seed 3,072개로 해석하거나 짝별 delta에서 무조건적인 인과 검정/p-value를 계산하지 않았다.

## 2. 전체 및 case별 추종 (낮을수록 유리)

평가 내부 `mean_tracking_error`는 매 step의 속도 x/y/yaw-rate 오차를 결합한 **혼합 단위** 지표다. 공식 점수 또는 물리적으로 동일한 m/s 척도가 아니다. 전체 평균은 **8 case/episode 동일가중** (H6 상·하 각각 384개)이다.

| case | TERM-50 `2800` | ORIENT-100 `2850` | ACTRATE-0001 `2700` |
|---|---:|---:|---:|
| H1 정지 | 0.10133 | 0.11706 | 0.15369 |
| H2 전진 | 0.16179 | 0.12703 | 0.11878 |
| H3 좌우 | 0.12748 | 0.11997 | 0.15255 |
| H4 회전 | 0.14805 | 0.14293 | 0.15355 |
| H5 rough | 0.18152 | 0.17089 | 0.17811 |
| H6 경사 상행 | 0.19103 | 0.15777 | 0.13611 |
| H6 경사 하행 | 0.18996 | 0.15857 | 0.13667 |
| H7 외란 | 0.15579 | 0.12906 | 0.13326 |
| **전체 3,072 episode 평균** | **0.15712** | **0.14041** | **0.14534** |

- **대조군 대비:** ORIENT 전체 오차 `0.15712→0.14041` (**10.63% 감소**), ACTRATE `0.15712→0.14534` (**7.50% 감소**). ORIENT는 H1을 제외한 7 case에서 TERM보다 tracking 평균이 낮고, ACTRATE는 H2·H5·H6상·H6하·H7 **5 case**에서 낮다. ACTRATE는 H1·H3·H4에서 TERM보다 tracking이 나쁘다.
- **오차 성분주의:** 세 정책의 전체 평균 x속도 절대오차는 TERM `0.05284`, ORIENT `0.06015`, ACTRATE `0.05998`로 TERM이 오히려 작다. yaw-rate 절대오차는 TERM `0.11438`, ORIENT `0.08744`, ACTRATE `0.09469`로 변화한다. 따라서 결합 tracking 평균의 개선을 무조건 **직진 속도 추종 개선**으로 읽으면 안 된다.

## 3. 명령별 핵심 행동 비용 (원자료 직접 집계)

| 지표 | TERM-50 | ORIENT-100 | ACTRATE-0001 |
|---|---:|---:|---:|
| H1 정지시 비의도 body 전진 ↓ | 1.3523m | 1.6334m | 1.9870m |
| H1 월드 순변위 크기 평균 ↓ | 1.3565m | 1.6268m | 2.0113m |
| H3 횡이동 중 비의도 body 전진 ↓ | 1.2050m | 1.1803m | 1.6771m |
| H3 횡이동 후 월드 순변위 크기 평균 ↓ | 0.9725m | 0.8200m | 0.6693m |
| H2 전진 body 진행 (명령 적분 15m) | 15.1681m | 15.4075m | 15.3262m |
| H5 rough 평균 body 진행 (명령 10m) ↑ | 8.8961m | 9.4513m | 9.9482m |
| H5 rough 진행 P05 ↑ | 8.5325m | 8.8631m | 9.5924m |
| H5 rough 최소 진행 ↑ | 2.6391m | 7.8313m | 8.8150m |
| H5 rough tracking P95 ↓ | 0.2058 | 0.1948 | 0.1916 |
| H5 rough 최대 stall_fraction ↓ | 0.6110 | 0.0730 | 0.0230 |
| H6 상행 tracking ↓ | 0.1910 | 0.1578 | 0.1361 |
| H6 하행 tracking ↓ | 0.1900 | 0.1586 | 0.1367 |
| H6 하행 action Δ RMS ↓ | 0.4798 | 0.4639 | 0.5401 |
| H6 하행 roll/pitch RMS ↓ | 0.0392 | 0.0903 | 0.0355 |
| H7 push body 진행 (명령 10m) | 10.0503m | 10.5305m | 10.5424m |

- **H1 정지:** TERM은 body 전진 `1.352m`; ORIENT `1.633m` (**+0.281m**), ACTRATE `1.987m` (**+0.635m**). 이 평가에서는 TERM이 세 정책 중 가장 잘 정지하지만 **TERM도 20초에 약 1.35m의 비의도 전진**이 있어 완벽한 균형 정책은 아니다. `stall_fraction=0`은 H1에서 command가 0이라 denominator가 없어서 만들어진 값이며 제자리 유지 성공이 아니다.
- **H3 횡이동:** ACTRATE는 body 비의도 전진 `1.677m`로 가장 높지만, *world XY 순변위 크기*는 `0.669m`로 가장 낮다(ORIENT `0.820m`, TERM `0.973m`). 두 값은 **서로 다른 현상**이며 body-frame forward leakage와 횡이동 후 위치 복귀 정확도를 동일 지표로 취급해서는 안 된다.
- **H5 rough 실증:** TERM 최악 `seed=4201, env=16`: 전진 `2.6391m`, stall `0.611`, tracking `0.4543`, 20초 timeout. ORIENT 최악 진행 `seed=4201, env=6`: `7.8313m`, stall `0.072`; ACTRATE 최악 `seed=4202, env=108`: `8.8150m`, stall `0.019`. TERM도 rough 심각한 정체 사례가 있음을 **이번 원자료에서 새로 확인**했다. `forward_progress_m<9.5m`인 384 episode 수는 TERM **374**, ORIENT **212**, ACTRATE **6**. H5 tracking P95는 ACTRATE가 조금 낮지만 **H5 평균 yaw 오차는 ORIENT `0.1190`, TERM `0.1322`, ACTRATE `0.1343`**로 ACTRATE가 전 지표에서 우월한 것은 아니다.
- **몸통 자세·동작 비용:** ORIENT의 전체 roll/pitch RMS 평균 `0.08015`는 TERM `0.03381`, ACTRATE `0.03019`보다 **상당히 크고**, 이 평가의 **8 case 모두에서 평균이 가장 높다**. ORIENT action Δ RMS 평균 `0.35759`는 TERM `0.36529`보다 약간 낮지만 TERM이 H1·H3·H4에서는 더 낮다. ACTRATE 전체 action Δ RMS `0.45687`은 TERM/ORIENT보다 높다. **action 변화가 작다고 상체 흔들림도 작은 것은 아니다.**

## 4. 같은 `(scenario,case,seed,env_id)`에서 직접 계산한 차이

아래는 각 case 384개 **키 대응 결과의 평균 차이**이며 `변경 정책 − TERM-50`이다. tracking/action/posture/정지 비의도 전진은 음수가 유리하고, rough body 진행은 양수가 유리하다. 같은 키=같은 초기 랜덤 지형이 **반드시 재현됨**을 증명한 것은 아니므로 **대응 인덱스 기술통계**로 쓴다.

| case / 지표 | ORIENT−TERM | ACTRATE−TERM | 대응 episode 관찰 |
|---|---:|---:|---|
| H1 정지 비의도 전진 | +0.28109m | +0.63474m | 각 case 384개 인덱스 대응 평균 |
| H2 추종 오차 | -0.03475 | -0.04301 | 오차 낮은 코호트 ORIENT **384/384**, ACTRATE **384/384** |
| H3 추종 오차 | -0.00751 | +0.02507 | 오차 낮은 코호트 ORIENT **384/384**, ACTRATE **0/384** |
| H5 진행 | +0.55516m | +1.05204m | 진행 우세 코호트 ORIENT **364/384**, ACTRATE **384/384** |
| H5 추종 오차 | -0.01063 | -0.00341 | 오차 낮은 코호트 ORIENT **290/384**, ACTRATE **184/384** |
| H6 상행 추종 | -0.03327 | -0.05492 | 오차 낮은 코호트 ORIENT **384/384**, ACTRATE **384/384** |
| H6 하행 추종 | -0.03139 | -0.05329 | 오차 낮은 코호트 ORIENT **384/384**, ACTRATE **384/384** |
| H6 하행 action 변화 | -0.01581 | +0.06033 | 각 case 384개 인덱스 대응 평균 |

원본 자료에서 각 policy의 3,072 episode ID가 대응되고 case/seed/env-key가 전부 일치하지만, **독립 학습 seed 수는 각 Run 1개**로 실험 반복 없는 관찰이다. 대량 env를 독립 RL Run이나 정책 효과의 통계적 인과 표본으로 둔갑시키지 않았다. 영상 6개는 camera-off 평가와 다른 경로·command의 **정성 자료**이며 계단 중앙 다단 완주나 boxes 정량 성공률을 이 8 case 평가로 증명하지 않는다.

## 5. Experiment / 정책 선택 판단

1. **TERM-50 `model_2800`:** 같은 `scenario7`에서 H1 정지 전진·정지 tracking과 작은 자세 흔들림/작은 action 변화의 기준. H5 mean `8.896m`, 최소 `2.639m`/stall `61.1%`가 취약하다. 이전에 raw baseline 미수납으로 보류했던 *baseline의 실제 H5 지표는 이제 확보 완료*.
2. **ORIENT-100 `model_2850`:** 8-case tracking **1위(낮음)** 및 ACTRATE보다 작은 action 변화 비용. TERM 대비 tracking 약 **10.63% 낮음**, rough 진행 P05 개선. 그러나 TERM 대비 H1 비의도 전진 증가와 **모든 case에서 크게 높은 roll/pitch RMS**가 있어 “안정성 최상”이라고 표현하지 않는다. **범용 후보 HOLD**.
3. **ACTRATE-0001 `model_2700`:** rough 진행 P05/최소/평균 강점과 H2/H6 tracking 강점. TERM 대비 평균 tracking **7.50% 낮음**, H5 평균 진행 **+1.052m**, rough 384/384 대응 인덱스에서 진행 우세. 그러나 zero/lateral 의도하지 않은 전진, action 변화 증가, H5 yaw 비용. **지형 진행 후보 HOLD**.
4. **Reward 단일변수 효과:** ORIENT 및 ACTRATE는 frozen TERM-50 대비 서로 독립 fresh3K/seed42/same env 수치로 비교했지만, 각각 **Run 1개**, 정책 자동-best 저장 시점이 기준 `2800` vs ORIENT `2850` vs ACTRATE `2700`으로 다르다. 평가/선택 시점 효과, source/PPO training-side 완전 parity, 정책 stochastic variation까지 격리한 인과 결론은 아니다. 새 reward coefficient와 확정적 성능 우위를 연결해 보고하지 않는다.
5. **그 외 정책:** PERSONAL corrected5K `LINTRACK-075/model_4997`는 별도 원문에서 H1/H3 전진 억제와 H5 severe tail(전진 2.871m/stall 0.664)을 보인다. 3개 **OFFICIAL fresh3K** 보상 인과 실험과 섞지 않는다. `ANGTRACK-065` OFFICIAL fresh3K 완료/PASS나 camera-off 정책 평가는 미접수. `ACTRATE-001` 아직 PLANNED.

**현재 최종 상태:** matched-index raw metric comparison **PASS**; 3개 ZIP+evaluation config 무결성 **PASS**; 3개 정책의 20초 camera-off 평가 survival **PASS**; 실제 terrain/episode 동일성·training-side complete parity·multi-run 통제 인과 검증 **NOT ESTABLISHED**; 범용 정책 선별과 공식 점수 **HOLD**.

## 보존·재현성

- 업로드받은 세 ZIP은 읽기만 수행했고 **기존 Originals/GitHub Releases를 수정하거나 원본 ZIP을 재게시하지 않았다**. 이 보고서와 별도 생성한 `h1_raw_summary.json`(case 평균/quantiles/ZIP·checkpoint SHA), `h1_paired_deltas.json`(case별 대응 인덱스 평균·중앙 delta와 개선 건수)이 재집계 결과다.
- 정책 학습을 재개하거나 GPU 정책 evaluator, 영상 decode, export, submission 또는 server shutdown은 실행하지 않았다. Python/Pandas로 기존 JSONL/manifest 읽기와 기술통계만 수행했다.
