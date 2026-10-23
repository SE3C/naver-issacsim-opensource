> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/incoming/other/reviewed/H1_ACTRATE_PARENT_UNCHANGED_RESTORATION_COMPARISON_20261015/H1_ACTRATE_PARENT_UNCHANGED_RESTORATION_REPORT_20261015.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# H1 동일 부모 action-rate 유지·복원 비교 — CPU 원자료 재집계

**작성일:** 2026-10-15 · **자료 범위:** 제공한 통합 ZIP 3개 안의 `evaluation/episodes.jsonl`·`diagnostics.json`·manifest/config 및 기존 MP4 18개. **새 학습·GPU 평가·렌더링·export 없음.** 아래 수치는 명시적 인용을 제외하고 모두 이번 입력에서 계산했다.

## 1. 결론 — 핵심 질문에 대한 판정

**B(무변경 +2K, model_4699) 대 C(action_rate_l2 복원 +2K, model_4650): `혼합`.** C는 rough H5의 **평균 실제 진행 7.919→8.769m**(대응 384개 중 **373개 증가**)·P05 **7.427→7.970m**를 회복하고 H1 정지 위치 잔차, H3 횡왕복 최종 위치 잔차 및 action 변화량이 더 작다. 반면 H5 **평균 혼합 tracking 0.18596→0.19816(악화)**, tracking P95 **0.21732→0.23468**, 최악 진행 **6.239→4.845m(악화)**, 최악 stall **0.074→0.386**이다. H5 평균 회복은 전 지형·최악 사례 개선이 아니다. B는 평균 혼합 tracking과 일부 yaw·자세 지표에서 C보다 좋지만 목표 전진·요철 진행이 전반적으로 뒤처진다. **C를 B보다 종합적으로 개선된 정책으로 확정할 수 없고, action 벌점 복원의 인과 효과도 확정할 수 없다.**

**A(부모 auto-best model_2700) 대비 B: `혼합, 전진·험지 행동은 뚜렷이 악화`.** B는 H1/H3 위치 이탈 및 전체 mixed tracking·action 변화를 줄였으나 H5 진행 평균 **9.948→7.919m**, P05 **9.592→7.427m**, 최악 **8.815→6.239m**이고 대응 H5 **384/384개 모두 진행 감소**. H2/H4/H6/H7의 진행도 줄고 자세 RMS는 커졌다. *변경 없이 더 학습했다*는 사실은 이 선택 checkpoint에서 행동이 더 좋아졌다는 뜻이 아니다.

**A 대비 C: `혼합, rough는 악화`.** C는 제자리·횡왕복 최종 위치 잔차와 action 변화를 크게 낮추면서 H2·H6·H7 목표 부근 body 진행은 상당 부분 보전한다. 그러나 H5 평균 **9.948→8.769m**, P05 **9.592→7.970m**, 최악 **8.815→4.845m**(대응 **381/384개 감소**), H5 stall·혼합 tracking·roll/pitch가 악화됐다. 자식 둘 모두 **전지형 일괄 개선: 아니오**.

**이번 PERSONAL 고정평가 범위의 대표 후보 판정:** **A = HOLD**(rough 진행 우위이지만 H1/H3 불필요한 몸체 전진과 큰 action 변화), **B = REJECT**(*세 후보 중 범용 대표/전진·험지 주후보 선정에서만 제외*; 별도 정지·yaw 참고군까지 폐기한다는 뜻 아님), **C = HOLD**(정지·횡왕복·action 측면 비교 후보이지만 H5 최악 꼬리로 전지형 대표 승격 불가). **PROMOTE 없음.** 학습 seed 하나와 선택 checkpoint 차이 때문에 reward 효과의 독립 인과 판정은 **판단 불가**다.

## 2. Identity, 계보, 비교 조건

| 구분 | A 부모 | B 무변경 continuation | C action 복원 |
|---|---|---|---|
| 첨부 계보의 OFFICIAL train Run | `20261009-142350-h1-actrate-0001-fresh3k` | `20261014-111135-h1-actrate-0001-unchanged-cont2k` | `20261014-142200-h1-actrate-return2700-2k` |
| 평가 checkpoint | `model_2700.pt` | `model_4699.pt` | `model_4650.pt` |
| checkpoint SHA-256 | `e54d3389…93ca7ae` | `722b35a1…48f646` | `a8249db4…84ea` |
| 설명된 학습 경로 | fresh 3K의 자동 best | 같은 A 부모에서 reward 유지 +2K | 같은 A 부모에서 action 벌점 `−0.0001→−0.0005`, +2K |
| 외부 기록상의 `action_rate_l2` | `−0.0001` | `−0.0001` | `−0.0005` |
| 평가 ZIP의 `policy.source_run_id`, `preset` | 모두 `null` | 모두 `null` | 모두 `null` |

위 **학습 Run·reward·공통 부모 SHA**는 동봉 `01_비교대상과계보.md`의 외부 registry/publication 설명에서 가져온 것으로, 이번 ZIP에 원본 native checkpoint·train archive·TensorBoard가 없으므로 재해시 또는 완전 독립 검증한 값이 아니다. B/C metadata에는 `user_imported_checkpoint`, 부모·source evidence ID null, `source_provenance_verified=false`가 기록된 것으로 설명되며 이를 verified로 바꾸지 않는다. 반면 **평가 checkpoint SHA**는 각 ZIP의 `source_checkpoint.txt`, manifest, video link와 일치한다. 세 하위 ZIP SHA-256도 동봉 기대값과 일치하고, ZIP CRC·각 ZIP의 영상 checksum 6/6(총 18/18)이 통과했다. 전체 SHA 및 항목별 증거는 `csv/identity_audit.csv`.

**선택 차이(필수 주의):** A의 2700은 **자동 best**로 fresh 3K의 마지막 keeper 2950과 다르다. B 4699는 +2K의 **endpoint**, C 4650은 console endpoint 4699/4700보다 이른 **선택본**이다. 동일 부모·비슷한 추가 학습량이라도 B/C 평가 checkpoint 번호 및 selection source가 동일하지 않다. 따라서 `C−B`는 동일 step을 고정한 순수 action reward A/B 실험이 아니다.

**평가 동일성 직접 확인:** 각 통합 ZIP은 18개 구성 항목(6 MP4 + camera-off 평가). `scenario7`은 **7 scenario / 8 case**(H6 상·하 분리), case당 3 evaluator seed(4201/4202/4203)×128 env=**384 episode**, 정책당 **3,072**, 총 **9,216**. `steps=1000`, 20초, `n0` 첫 cohort만 존재하며 모든 건 `timeout`, `survived=true`, `base_contact_failure=false`; **추가 reset 행 0**, 중복 대응 키 0, 누락 키 0. `(scenario,case,seed,env_id)` 3,072개가 세 정책 간 일치하며 `diagnostics.json`의 episode 수·survival·scenario 평균 tracking을 재현했다(최대 부동소수 오차 약 `5.8e−16`). 20초 생존은 목표 수행·요철 완주 증명이 아니다.

manifest의 **protocol ID** `d406a296…7062d34`, deterministic actor, episode clock 10초 명령 전환, 20초 time window, seed·128 env, 24 case×seed 적용환경 fingerprint, agent fingerprint `976cb139…729b2`, `source_fingerprints`의 4파일, task config 및 `evaluation/resolved_configs.json` **전체 바이트 SHA `3f7d219d…`가 A/B/C 동일**. 평가 링크의 handoff `28895d75…`, upstream implementation `9c774a32…`와 영상 `environment.txt`의 task repo git `ef10b7a4…`도 각기 **동일**이다. 이 서로 다른 source 식별자는 **서로 다른 역할**의 기록이며 상호 교환 불가. 입력에서 확인한 *평가 task source*의 정책 간 fingerprint 변경은 **없다**. 다만 **실제 OFFICIAL train-side task source·PPO·부모 checkpoint 내부 상태가 완전히 동일했는지**는 해당 학습 archive 없이 확인 불가다. 동일 키와 동일 프로토콜도 동일 random terrain tile·초기 상태·실제 궤적을 보증하지 않는다.

고정평가 설정은 camera off, 10×20 tile/무작위 reset 및 source 기록상의 적용환경 fingerprint, fixed scenario command와 4·8·12·16초 disturbance를 사용한다. 6영상은 별개 1 env, seed42, 1×1 tile, 고정 초기 pose, observation noise off, 1,000 frames/50fps, 전역 명령 스케줄, ±10° 지형이다. 영상 `environment.txt`에서 A/B/C 간 실행시각 외 설정 차이는 없었다. **영상과 정량 에피소드는 서로 대응하지 않는다.** 평가의 resolved reward config를 OFFICIAL 학습에서 실제 사용한 reward로 해석하지 않는다.

## 3. 핵심 정량·분포 (모두 원자료 재계산)

명령 적분은 **H5 vx=0.5m/s × 20초 = 10m**, H2 `(0.5×10)+(1.0×10)=15m`, H6 `1.0×20=20m`, H7 `0.5×20=10m`이다. `forward_progress_m` = `integrated_body_forward_m`는 확인된 **동일 body-forward 적분의 두 이름**이고 중복 근거가 아니다. 부족 진행 `10m−실제 body 적분`은 물리량 차이이며 **임의 10% 합격선이 아니다**. 회전하는 H4의 body 전진 적분은 world X 최종 거리와 다르다. `mean_tracking_error`는 vx(m/s)·vy(m/s)·yaw-rate(rad/s)의 결합 평균으로 **단일 m/s 단위를 붙이지 않는다**. `lateral_drift_m`은 `vy_error×duration_s`와 각 행이 수치적으로 동일(최대 차 ~`2.3e−14`)하여 **횡방향 실제 변위가 아닌 절대 횡속도 오차 적분**이다. world XY 최종 잔차는 별도로 `hypot(world_dx_m,world_dy_m)`에서 산출했다.

### 3.1 최우선 H5 random rough — 384 episode/정책

| 항목 | A 부모 | B 유지 +2K | C 복원 +2K |
|---|---:|---:|---:|
| body 진행 mean / P05 / **최악** (m) | **9.948 / 9.592 / 8.815** | 7.919 / 7.427 / 6.239 | 8.769 / 7.970 / **4.845** |
| 명령 10m 대비 부족 진행 mean / P95 / 최대 (m) | 0.052 / 0.408 / 1.185 | 2.081 / 2.573 / 3.761 | 1.231 / 2.030 / **5.155** |
| 10m에 미달한 건수 | 232/384 | 384/384 | 384/384 |
| tracking mean / P95 / 최대 | **.17811 / .19155 / .29076** | .18596 / .21732 / .29230 | .19816 / .23468 / **.33263** |
| vx / vy / yaw 평균 **축별 절대 오차** | .0592 / .0601 / .1343 | .1084 / .0626 / **.1054** | .0969 / .0638 / .1303 |
| stall 평균 / 최대 | .00555 / .023 | .00953 / .074 | .01269 / **.386** |
| stall_fraction `> .05`인 episode 수 (참고 임계값) | 0 | 1 | 7 |
| roll/pitch RMS 평균 | **.03313** | .04514 | .05207 |
| action delta RMS 평균 | .47916 | .40748 | **.36424** |
| 20초 생존 | 384/384 | 384/384 | 384/384 |

- **B→C:** 384 대응 키 중 **373건** 진행 증가, **11건** 감소. 세 evaluator seed 모두 평균 이득 **+0.852 / +0.872 / +0.826m** (4201/4202/4203). 그러나 혼합 tracking은 **283/384건 증가(악화)**, 감소 101건이다. 따라서 평균 진행 개선과 추종 손실이 동일 자료에서 공존한다. worst cohort는 서로 다르므로 최악값 간 비교를 1:1 개선이라고 부르지 않는다.
- **같은 키로 본 하위 꼬리:** C 최악 `H5-rough-s4201-e60-n0`은 **4.8446m / tracking .33263 / vx_error .26817m/s / stall .386 / roll-pitch .10261**이며, *그 대응 키의 B*는 **7.9972m / tracking .17427 / stall .005**, A는 **9.7100m / tracking .17974 / stall .004**. C가 그 조건에서 특히 뒤처진 기록이다. C의 다른 하위 사례 `seed4203/env61` 진행 **5.885m**, stall **.123**. B 자체 최악은 `seed4203/env30`의 **6.239m / stall .074**; A 최악은 `seed4202/env108`의 **8.815m**. 모두 timeout 생존했다.
- **A→B:** H5 같은 키의 진행 **384/384 감소**, 3 evaluator seed 평균 감소 **−1.997 / −2.059 / −2.030m**. **A→C:** **381/384 감소**, 3개 seed 평균 감소 **−1.145 / −1.187 / −1.205m**. 세 평가 seed에서 분포 방향이 대체로 유지되지만, 이들은 **독립 training seed 세 개가 아니라 한 학습 정책을 3개 evaluator seed로 검사한 것**이다.

H5 분포: 누적분포〔원본 참조: `figures/rough_progress_ecdf.png` / 공개 사본 미포함〕

H5 평균·P05·최악〔원본 참조: `figures/rough_mean_p05_worst.png` / 공개 사본 미포함〕

### 3.2 다른 case에서 보이는 개선의 대가

| case / 지표 | A 부모 | B 유지 | C 복원 | 해석 |
|---|---:|---:|---:|---|
| **H1 정지** world XY 최종 순변위 평균 m | 2.011 | 0.692 | **0.304** | C가 위치 잔차 최소. 단 `stall=0`은 정지 검증 아님 |
| H1 비명령 body 전진 적분 m (부호 유지) | +1.987 | −0.724 | **+0.282** | B는 뒤로 이동; 부호 없는 속도/전진 이득으로 읽으면 안 됨 |
| **H2 전진** body 진행 / 목표 15m | 15.326 | **13.972** | 15.297 | B가 둔화, C는 진행 회복. 혼합 tracking A .1188/B .1248/C .1373 |
| **H3 횡왕복** world XY 최종 순변위 평균 m | 0.669 | 0.581 | **0.167** | C 복귀 잔차 최소. 실제 vy 추종 절대오차는 A .0673/B .0682/C **.0771**로 C가 불리 |
| H3 비명령 body 전진 적분 m | +1.677 | −0.741 | +0.276 | 횡명령인데 앞뒤 누수 존재, 방향·크기 함께 봐야 함 |
| **H4 회전+전진** body 진행 / 목표 10m | 10.556 | **9.084** | 10.439 | C body 진행 회복. world 순변위 A 4.843/B 3.634/C 2.819m를 전진 속도 점수로 사용하지 않음 |
| **H6 상행** body 진행 / 목표 20m | 20.052 | **19.007** | 20.187 | C 진행 이점, mixed tracking A .1361/B .1506/C **.1584** |
| **H6 하행** body 진행 / 목표 20m | 19.834 | **18.834** | 19.975 | C 진행 이점, mixed tracking A .1367/B .1539/C **.1578** |
| **H7 밀침** body 진행 / 목표 10m | 10.542 | **8.981** | 10.364 | C 회복, mixed tracking B **.1256**/A .1333/C **.1459** |

- 전체 **episode 동일가중** mixed tracking은 **A .145339 / B .137377 / C .140944**; 이번 8 case는 각각 384행이라 **case 동일가중과 같다**. **7 scenario 동일가중**은 A .146617 / B .135252 / C .138496으로 H6를 하나의 scenario로 처리해 값이 달라진다. 공식 점수 가중치나 변환식을 적용하지 않았다. 전체 평균만 보면 B가 가장 좋지만 **진행을 무시한 잘못된 대표 선정**이 된다.
- 전체 action delta RMS의 episode 평균은 **A .45687 / B .40435 / C .39707**, roll/pitch RMS는 **A .03019 / B .05292 / C .06008**. C는 action 명령 변화가 적지만 몸통 자세 RMS는 가장 크다. 낮은 action delta만으로 발 미끄러짐·토크·effort 저감을 수치 확정할 수 없다.
- H2에서 C는 B보다 vx 오차가 적지만(0.0398 vs 0.0520m/s), yaw 오차는 높다(0.0994 vs 0.0672rad/s). H3에서도 C의 mixed tracking 향상은 횡축 자체(`vy_error`) 개선이 아니다. 월드 잔차·body-frame 적분·축별 오차를 서로 대용하지 않는다.
- H1/H3/H4/H5/H6/H7 모두 **20초 생존**했어도 정지 유지, 목표속도 충족, 외란 직후 복귀 시간, 지형 완주를 확인한 것은 아니다. 원본의 `stall_fraction`은 명령 없는 H1에서 0이며, 이 값만으로 완벽한 정지를 주장하지 않는다.

case별 혼합 tracking〔원본 참조: `figures/scenario_tracking.png` / 공개 사본 미포함〕

H5 seed별 평균 진행〔원본 참조: `figures/rough_seed_consistency.png` / 공개 사본 미포함〕

## 4. 여섯 영상의 CPU 프레임 근거 — 정책별 동일 영상 구간 비교

제공된 **각 정책 6개, 총 18개** MP4에 대해 **각 1,000프레임을 CPU 디코드**하고, 동일 terrain별 시간축에서 초기 **0–8초(0.5–1초 간격)**와 후반 **10/12/15/18/19.5초**를 모아 A/B/C 연속된 구간을 육안 대조했다. 도표 `video_contact_sheets/`의 `*_early.jpg`와 `*_late.jpg`는 실제 프레임 및 선택 frame index를 보인다. 검사 범위는 디코딩 전 구간과 선택된 시각의 시각 판독이며 **모든 중간 프레임에서 관절·접촉을 눈으로 검사했다고 주장하지 않는다**.

| 원본 MP4 | 비교한 유효 시각/프레임 | 직접 확인 가능한 것과 한계 |
|---|---|---|
| `01_stairs.mp4` | 0.5–4s `#25–200`, 5–8s `#250–400`, 10–19.5s `#500–975` | 세 정책 모두 보행 중 직립으로 보이며 계단형 줄무늬가 멀어져 후반 평지 쪽으로 이동한다. **중앙 다단 계단 완주를 단정할 접촉·높이 정보 없음.** A는 홀수 프레임 black이므로 유효 짝수 인접 프레임 사용 |
| `02_inverted_stairs.mp4` | 0.5–4s `#25–200`, 5–8s `#250–400` | 패치 가장자리에서 걸어 나오는 연속 위치 변화, 뚜렷한 전도 장면은 선택 프레임에 없음. 중앙 역계단 연속 발 디딤 성공은 미검증 |
| `03_boxes.mp4` | **0.5–4s `#25–200`**, 5–8s `#250–400` | 세 정책에서 장애물 패치 내부/가장자리의 직립 보행과 위치 변화. C는 5–8초에도 장애물이 근처에 보이는 등 **단일 영상 경로 차이**가 있으나 이를 정량 384 episode 성공률로 옮길 수 없음 |
| **`04_random_rough.mp4`** | 0.5–3s `#25–150`, 4–8s `#200–400`, 10–19.5s `#500–975` | 모두 초기 요철 패치에서 걷고 후반 평지로 이동. B의 홀수 #1,#3,…,#999는 black이어서 #26,#50,#76,#100,#126,#150,#200 같은 **유효 짝수 프레임**으로 확인. B의 낮은 camera-off 10m 진행을 영상의 별도 1m/s 명령으로 부정할 수 없음 |
| `05_slope_up_10deg.mp4` | 0.5–5s `#25–250`, 6–8s `#300–400`, 10–19.5s | 세 정책 모두 선택된 구간에서 자세를 유지하며 보행. 원근·추적 카메라 때문에 실제 상승 높이·접지력을 역산하지 않음 |
| `06_slope_down_10deg.mp4` | 0.5–5s `#25–250`, 6–8s `#300–400`, 10–19.5s | 하행 패치/후반 평지 방향의 보행이 관찰됨. 명령 추종·회복률은 별도 camera-off 지표로만 판단 |

**검정 캡처 감사:** A `01_stairs.mp4`는 검정 **502/1,000**(홀수 500 + 짝수 2), B `04_random_rough.mp4`는 검정 **501/1,000**(홀수 500 + 첫 프레임 #0). 그 외 16개 MP4는 시작 #0만 black(각 1개). A stairs 유효 498, B rough 유효 499, 나머지 각 999프레임을 판독 기반으로 활용했다. 프레임 흑화는 **캡처 결함**이지 정책 낙상/실패 횟수가 아니다. 수집기에서 0,50,100,…만 고른 것이 아니라 parity가 다른 이웃 프레임을 검사했다(`csv/video_decode_audit.csv`).

영상의 공통 전역 명령은 **0–6s vx=1.0 → 6–10s vx=.5,vy=.3 → 10–14s vx=.5,vy=−.3 → 14–17s vx=.5,yaw=.5 → 17–20s vx=.5,yaw=−.5**, 4/8/12/16초 외란이 별도로 걸린다. 후반 대부분은 원래 지형 패치 밖 평지다. camera-off H5는 **vx=.5×20초**이고 원자료의 384 terrain/reset episode와 다르므로, 비디오의 보행 지속은 **정성 교차 확인**에 한한다. 영상만으로 발 미끄러짐 수치·관절 토크·명령별 딜레이를 발명하지 않았다.

## 5. 기존 세 독립 보고서와 마지막 대조

기존 `H1_MODEL2700_POLICY_ANALYSIS_20261010.md`, `H1_ACTRATE-0001-UNCHANGED-CONT2K_POLICY_ANALYSIS_20261015.md`, `H1_MODEL4650_POLICY_ANALYSIS_20261015.md`는 **이번 raw 재계산에 사용하지 않았고 위 산출 후 검토**했다. 세 단일 정책 보고서의 핵심 H5 mean/P05/min, H1/H3 body 적분, 3,072 timeout, B 384/384 `<9m`, C 최악 seed4201/env60, A 최악 seed4202/env108은 **이번 수치와 표시 반올림 안에서 일치**했다. 직접 계산 결과와 충돌하는 주요 숫자는 발견되지 않았다.

**단, 결론의 비교 맥락은 달라졌다.** 기존 B 단독 HOLD는 같은 부모의 A/C raw 전체 대응 비교 이전 판정이다. 여기서는 B의 H5가 A보다 **384/384건 저하**, C보다 **373/384건 느린 것**까지 직접 확인해 **현재 세 후보 중 전진·rough 중심 범용 대표 선정의 B만 REJECT**했다. C 기존 단독 보고서의 A 대비 정지/진행 tradeoff도 유지되지만, B 대비 **H5 평균·P05 개선과 최악 위험 악화가 동시에 있다는 새로운 직접 대조**를 추가했다. 기존 보고서의 일부 “비교를 위해 A 원본을 확보할 것”은 이번 제공 패킷으로 해소된 이전 시점의 공백이다. **이번 판단은 기존 HOLD를 전제로 한 추종 판정이 아니다.**

## 6. 권고할 다음 행동 — 하나만

**이번 재집계 CSV의 후보별 tradeoff와 C의 H5 하위 사례(`4201/env60`, `4203/env61`)를 내부 정책 선택 기록에 반영해, A는 rough 기준 보존, C는 정지·횡복귀 참고 후보 유지, B는 현재 범용 대표 후보군에서 제외한다.** 이는 지금 있는 자료만으로 가능한 기록·선정 작업이며 새 학습/평가 실행 제안이 아니다.

### 재현 및 한계

`analyze_h1_cpu.py --input <제공한_상위_ZIP> --output <결과_폴더>`로 원본 ZIP만에서 재집계·CRC/SHA 검증·그림을 CPU 재생성한다(`pandas`, `numpy`, `matplotlib`). 영상 감사 재현은 통합 ZIP 세 개의 원본 MP4를 A/B/C 폴더에 **복사·추출만** 한 뒤 `inspect_h1_video_cpu.py --extracted-root <A_B_C_폴더> --output <결과_폴더>` (`opencv-python`, `Pillow`)를 사용한다. 원본 MP4와 ZIP은 수정하지 않았다. 제공하지 않은 학습 TensorBoard·native `.pt`의 원본 bytes, 학습시 전체 task/PPO lineage 및 hidden official evaluator에 대한 결론은 없다. Windows PERSONAL 수치를 공식 채점식·유의확률·reward 인과로 환산하지 않는다.
