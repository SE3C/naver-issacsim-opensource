# H1 4정책 원자료 대조 — LINTRACK-065 resume 효과와 다음 GPU 우선순위

**분석 기준: 2026-10-14 | 평가 유형: PERSONAL Windows camera-off, 기존 자료 CPU 재집계 | 신규 GPU/학습 없음**

## 0. 즉시 결론

- **H5 병목: 해소되지 않음.** model_4650 H5 body-frame 진행 평균/P05/최저는 9.546/9.228/8.974m. 부모 model_2700의 9.948/9.592/8.815m보다 평균과 P05가 악화됐으나 최소값은 다른 최악 cohort를 가진 분포에서 올라갔다. 별도 fresh10K model_9999(8.915/8.251/6.492m)보다 model_4650의 기술통계가 좋으므로 **10K에서 보였던 진행 악화의 상대적 일부 완화**는 관찰된다.
- **회전·횡왕복 부작용 큼.** model_4650 H4 yaw-rate 절대오차는 0.1791rad/s(부모 0.1183), H3 world XY 종료 순변위는 2.398m(부모 0.669m). H3 x속도 오차와 비의도 body x진행은 개선되지만, 이것이 횡왕복 원점 복귀 개선을 뜻하지 않는다.
- **reward 계수의 인과효과는 미확정.** model_4650은 동일 model_2700에서 `track_lin_vel_xy_exp=0.50→0.65` 하나만 바꾼 +2K resume의 선택 model_4650이고, 같은 부모에서 보상 무변경으로 +2K한 control 데이터가 없다. 따라서 학습량, resume, reward 효과를 현재 데이터만으로 분리할 수 없다.
- **정책 결론:** LINTRACK-065 범용 승격 HOLD. 다음 GPU 작업을 단 하나 허용한다면 새로운 fresh 5K보다 **동일 부모 unchanged +2K sibling control**을 우선 추천한다. 이는 개선된 새 정책 보장이 아니라 기존 처리군의 원인·trade-off를 분리할 의사결정 실험이다.

## 1. 원본·계보·검증 범위

| 평가 정책 | 학습 측 외부 계보 | 평가 ZIP의 checkpoint SHA-256 |
|---|---|---|
| TERM-50 model_2800 | OFFICIAL fresh3K 기준 정책. **R2 실제 제출 정책 아님** | `dffaa77848741fed1f4d22d0b78d4d8911af49057541107845e4d1df02c09ad6` |
| ACTRATE-0001 model_2700 | OFFICIAL fresh3K, `action_rate_l2=-0.0001`; **4650 부모** | `e54d3389e20ea913968ef8d3edbea5004368ff225fa6b94f73fcd91cf93ca7ae` |
| LINTRACK-065 model_4650 | OFFICIAL `20261010-154926-h1-actrate0001-lintrack065-from2700-plus2k`; `track_lin_vel_xy_exp=0.50→0.65`, `action_rate_l2=-0.0001`, **부모 2700**에서 +2K resume, console `4699/4700`, 선택 model_4650 | `ce7ad58657f3dd744e7cf2b7531f3d7d455773dfc6fb135f39d8a55aa49dea70` |
| ACTRATE-0001 model_9999 | 별개 OFFICIAL fresh10K, 실제 R6 제출 정책. **2700의 연장 궤적이라 전제하지 않음** | `a5020c273bc2b69bea1b20782fe80ba6605b3036b4054a7e5a8ab66151d2cb74` |

**직접 검증:** 4개 평가 ZIP 각각 18항목, ZIP CRC PASS; 내부 영상 6개씩 SHA256SUMS 24/24 PASS; `evaluation_manifest` 4/4 `complete=true`, `execution_status=COMPLETE`, `smoke=false`, 평가 로그 4/4 `[CHILD EXIT] 0`.

- 평가 명령의 유효 핵심 인자는 모두 `--mode personal --robot h1 --suite scenario7 --num-envs 128 --seeds 4201,4202,4203 --device cuda:0`이며 명령은 보존된 Windows `kit.exe -u .../isaac_runner.py`로 실행됐다. GPU는 당시 RTX 3060 Laptop. 현재 사용자가 복사해 재실행할 명령이 아니다.
- 8 case × 3 seeds(4201/4202/4203) × 128 env = **3,072 첫 episode/정책**, 총 12,288개. `(scenario,case,seed,env_id)` key 3,072개와 `-n0` episode ID 전체 대응. 모든 episode 1,000 steps/20s, `timeout`, 접촉 종료 0. 재시작 `-n1` 없음.
- `protocol_id=d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34`; 네 evaluator의 `protocol`, `source_fingerprints`(task/agent/env/reward), `suite`, `task_config` 완전 일치. `resolved_configs.json` **바이트 동일**, SHA-256 `3f7d219d03574c10c07911eb1df7aa2cea27c90e6dbd60dfd290b35001631bbc`.
- `actor_mode=deterministic_inference`, `camera_enabled=false`, `command_schedule=per_episode_step_clock_without_rng_v1`, 10s 명령 변경, 20s horizon. H7은 4/8/12/16s의 지정된 외란. 동일 cohort key·평가 config가 동일 물리 초기 terrain tile·reset 상태·실제 rollout을 **보증하지는 않는다**.
- 각 원본 evaluator ZIP은 `policy.source_run_id=null`, `preset=null`이고 변경하지 않았다. 위 OFFICIAL 학습 연결은 **별도 보존 기록** 및 4650 영상·평가 `source_checkpoint` linkage에 근거한다. 평가 측 `resolved_configs`의 reward 내용을 실제 훈련 때 사용한 reward라고 재해석하지 않는다.

**평가의 측정 정의:** `vx_error`, `vy_error`, `yaw_error`는 episode 집계 추종 오차(각각 m/s, m/s, rad/s; 작을수록 좋음). `forward_progress_m`는 body-frame 전진 속도 적분이며 `integrated_body_forward_m`와 동일값으로 중복 합산하지 않는다. `world XY`는 종료 순변위 `sqrt(world_dx²+world_dy²)`이다. `lateral_drift_m`는 |vy 추종오차| 적분이므로 실제 횡이동거리로 사용하지 않았다.

## 2. H2~H5: 주 병목·교차축 오차

### H2 — 전진 x=0.5→1.0m/s (목표 적분 15m)

| Metric | TERM-50 / 2800 | ACTRATE / 2700 (parent) | LINTRACK-065 / 4650 | ACTRATE / 9999 |
|---|---:|---:|---:|---:|
| x 절대오차 (m/s) ↓ | 0.0384 | 0.0427 | 0.0254 | 0.0228 |
| y 절대오차 (m/s) ↓ | 0.0613 | 0.0627 | 0.0539 | 0.0759 |
| yaw 절대오차 (rad/s) ↓ | 0.1321 | 0.0725 | 0.1364 | 0.0615 |
| body x진행 평균 (m) | 15.168 | 15.326 | 14.812 | 14.885 |

**4650 vs 2700:** x오차 −0.01735, y오차 −0.00877 개선. 그러나 yaw오차 +0.06385 악화. 진행은 15.326→14.812m로 초과(+0.326)에서 과소(−0.188)로 바뀌었으며, 단순 진행 감소를 실패로만 평가하면 안 된다. 9999는 14.885m, x오차 0.0228로 참고 수준에서 더 낫다.

### H3 — 순수 lateral vy=+0.3→−0.3m/s (명령상 x=0, 목표 world 복귀)

| Metric | TERM-50 / 2800 | ACTRATE / 2700 (parent) | LINTRACK-065 / 4650 | ACTRATE / 9999 |
|---|---:|---:|---:|---:|
| 불필요한 x속도 절대오차 (m/s) ↓ | 0.0604 | 0.0840 | 0.0136 | 0.0146 |
| 목표 y속도 절대오차 (m/s) ↓ | 0.0685 | 0.0673 | 0.0571 | 0.0717 |
| yaw 절대오차 (rad/s) ↓ | 0.0674 | 0.0880 | 0.1121 | 0.0463 |
| 비의도 body x진행 적분 (m; 0에 가까울수록 좋음) | 1.205 | 1.677 | -0.044 | 0.273 |
| 종료 world XY 순변위 (m) ↓ | 0.973 | 0.669 | 2.398 | 0.395 |
| 평균 stall fraction ↓ | 0.00912 | 0.00619 | 0.00938 | 0.01030 |

**4650 vs 2700:** x오차 0.0840→0.0136, y오차 0.0673→0.0571, body x진행 1.677→−0.044m로 좋아졌지만, yaw오차 0.0879→0.1121, world XY 복귀 오차 0.669→**2.398m**, stall 0.00619→0.00938로 악화. 종료 world XY 증가 이유를 yaw drift·횡속도 적분 또는 카메라상 왕복 파형의 특정 원인으로 **단정할 수 없다**. 9999는 세계좌표 잔류 0.395m로 4650보다 좋다.

### H4 — 회전 + 이동, vx=0.5m/s, yaw=+0.5→−0.5rad/s (목표 body 전진 10m)

| Metric | TERM-50 / 2800 | ACTRATE / 2700 (parent) | LINTRACK-065 / 4650 | ACTRATE / 9999 |
|---|---:|---:|---:|---:|
| x오차 (m/s) ↓ | 0.0276 | 0.0392 | 0.0192 | 0.0175 |
| y오차 (m/s) ↓ | 0.0611 | 0.0655 | 0.0563 | 0.0734 |
| yaw 오차 (rad/s) ↓ | 0.1193 | 0.1183 | 0.1791 | 0.0666 |
| XY RMSE (m/s) ↓ | 0.0881 | 0.0965 | 0.0772 | 0.0969 |
| body 진행 (m), 목표 10 | 10.099 | 10.556 | 9.842 | 10.009 |
| world XY 종료 순변위 (m; 경로 오차 아님) | 3.007 | 4.843 | 4.719 | 2.821 |

**4650 vs 2700:** x/y 오차 감소 및 전진 목표 적분의 오차 절댓값 감소(10.556→9.842m)와 동시에 yaw 오차 **0.1183→0.1791** 악화. 384개 대응 cohort 모두 yaw 오차가 증가했다. H4에는 실제 이동 명령이 있으므로 종료 world XY 순변위가 작을수록 좋다고 단정하지 않는다.

### H5 — rough, vx=0.5m/s 20초 (목표 body 전진 10m)

| Metric | TERM-50 / 2800 | ACTRATE / 2700 (parent) | LINTRACK-065 / 4650 | ACTRATE / 9999 |
|---|---:|---:|---:|---:|
| x오차 (m/s) ↓ | 0.0712 | 0.0592 | 0.0514 | 0.0772 |
| y오차 (m/s) ↓ | 0.0633 | 0.0601 | 0.0497 | 0.0648 |
| yaw 오차 (rad/s) ↓ | 0.1322 | 0.1343 | 0.1523 | 0.1272 |
| 혼합 tracking error ↓ | 0.1815 | 0.1781 | 0.1847 | 0.1856 |
| 진행 평균 (m) | 8.896 | 9.948 | 9.546 | 8.915 |
| 진행 분포 P05 (m) | 8.533 | 9.592 | 9.228 | 8.251 |
| 진행 최소 (m) | 2.639 | 8.815 | 8.974 | 6.492 |
| 평균 stall fraction ↓ | 0.01001 | 0.00555 | 0.00685 | 0.00873 |
| action 변화 RMS ↓ | 0.3593 | 0.4792 | 0.5181 | 0.5099 |
| roll/pitch RMS ↓ | 0.0317 | 0.0331 | 0.0629 | 0.0547 |

| H5 worst-tail 진단 (384건/정책) | TERM 2800 | ACT 2700 | LIN 4650 | ACT 9999 |
|---|---:|---:|---:|---:|
| 진행 <9.5m | 374 | 6 | **142** | 364 |
| 진행 <8m | 2 | 0 | **0** | 7 |
| stall >5% | 2 | 0 | **0** | 2 |
| 최대 stall fraction | 0.611 | 0.023 | **0.022** | 0.104 |
| 혼합 tracking P95 | 0.2058 | 0.1916 | **0.2087** | 0.2153 |
| base contact 종료 | 0 | 0 | **0** | 0 |

**중요: 서로 다른 두 P05 정의**

- **각 분포의 주변(marginal) P05 차이:** 4650 진행 P05 9.228m − 부모 9.592m = **−0.364m**. 이는 두 분포의 하위 5백분위 위치 비교다.
- **cohort별 진행 변화량 Δ=4650−2700의 P05:** **-0.837m**; P95 **+0.008m**. 384개 같은 key 중 개선 24, 악화 360. 이는 `P05(차이)`이지 `P05(4650)−P05(2700)`이 아니다.
- seed별 H5 진행 평균: 4201 부모9.946→4650 9.533, 4202 부모9.959→4650 9.557, 4203 부모9.939→4650 9.548m. 세 seed에서 모두 감소. 다만 각 평가의 동일 key가 같은 물리 초기 지형 실현을 의미한다고 단정하면 안 된다.
- 최악 진행 cohort는 2700에서 (4202,108) 8.815m, 4650에서 (4202,101) 8.974m, 9999에서 (4202,57) 6.492m이다. **분포 최소값 증가만으로 동일 물리 사례의 문제 해결을 주장하지 않는다.**
- 4650의 H5 x오차 개선(0.0592→0.0514), y오차 개선(0.0601→0.0497)에도 yaw오차 증가(0.1343→0.1523), roll/pitch RMS(0.0331→0.0629), action Δ RMS(0.4792→0.5181)가 나타나고 진행 평균이 감소했다. 근본 원인을 ‘발 미끄럼’ 또는 ‘yaw 지연’으로 확정할 자료는 없다.

## 3. H1/H6/H7: 타 시나리오 비용

### H1 — 정지 명령 (목표 world XY 종료 순변위 0)

| Metric | TERM-50 / 2800 | ACTRATE / 2700 (parent) | LINTRACK-065 / 4650 | ACTRATE / 9999 |
|---|---:|---:|---:|---:|
| x오차 (m/s) ↓ | 0.0677 | 0.0994 | 0.0160 | 0.0119 |
| y오차 (m/s) ↓ | 0.0479 | 0.0593 | 0.0506 | 0.0648 |
| yaw 오차 (rad/s) ↓ | 0.0412 | 0.0830 | 0.1092 | 0.0439 |
| 비의도 body x진행 (m) | 1.352 | 1.987 | 0.108 | 0.231 |
| world XY 종료 순변위 (m) ↓ | 1.356 | 2.011 | 0.228 | 0.287 |
| roll/pitch RMS ↓ | 0.0343 | 0.0230 | 0.0723 | 0.0705 |
| action Δ RMS ↓ | 0.2391 | 0.3568 | 0.4299 | 0.3875 |

**4650:** 종료 world XY 0.228m로 4정책 중 가장 작고 부모 대비 위치 유지가 크게 개선. 대신 roll/pitch RMS 0.0231→0.0723, action Δ RMS 0.3568→0.4299, yaw오차 0.0830→0.1092 악화. 모든 정책 생존 100%는 자세 안정의 동등함을 뜻하지 않는다.

### H6 — ±10° 경사 (각각 목표 body 전진 20m)

| Metric | TERM-50 / 2800 | ACTRATE / 2700 (parent) | LINTRACK-065 / 4650 | ACTRATE / 9999 |
|---|---:|---:|---:|---:|
| **상행** x오차 ↓ | 0.0613 | 0.0512 | 0.0453 | 0.0331 |
| y오차 ↓ | 0.0575 | 0.0582 | 0.0532 | 0.0733 |
| yaw 오차 ↓ | 0.1531 | 0.0908 | 0.1601 | 0.0898 |
| 진행 (m) | 20.199 | 20.052 | 19.872 | 19.788 |
| roll/pitch RMS ↓ | 0.0406 | 0.0382 | 0.0710 | 0.0682 |
| action Δ RMS ↓ | 0.4764 | 0.5340 | 0.5420 | 0.6637 |

| Metric | TERM-50 / 2800 | ACTRATE / 2700 (parent) | LINTRACK-065 / 4650 | ACTRATE / 9999 |
|---|---:|---:|---:|---:|
| **하행** x오차 ↓ | 0.0582 | 0.0497 | 0.0480 | 0.0329 |
| y오차 ↓ | 0.0596 | 0.0594 | 0.0541 | 0.0764 |
| yaw 오차 ↓ | 0.1524 | 0.0919 | 0.1613 | 0.0892 |
| 진행 (m) | 19.985 | 19.834 | 19.633 | 19.730 |
| roll/pitch RMS ↓ | 0.0392 | 0.0355 | 0.0650 | 0.0638 |
| action Δ RMS ↓ | 0.4798 | 0.5401 | 0.5585 | 0.6884 |

**4650 vs 부모:** 상행 20.052→19.872m, 하행 19.834→19.633m 진행 감소. y오차 소폭 개선, yaw오차 상행 0.0908→0.1601, 하행 0.0919→0.1613로 악화; 768개 대응 경사 cohort에서 yaw 오차가 모두 증가했다. roll/pitch RMS와 action 변화 비용도 증가. 영상만으로 물리 경사 전체 통과 거리·슬립을 수치 추정하지 않는다.

### H7 — 밀침 외란 + vx=0.5m/s (목표 body 전진 10m)

| Metric | TERM-50 / 2800 | ACTRATE / 2700 (parent) | LINTRACK-065 / 4650 | ACTRATE / 9999 |
|---|---:|---:|---:|---:|
| x오차 ↓ | 0.0379 | 0.0544 | 0.0319 | 0.0289 |
| y오차 ↓ | 0.0676 | 0.0699 | 0.0575 | 0.0771 |
| yaw 오차 ↓ | 0.1172 | 0.0786 | 0.1292 | 0.0541 |
| 진행 (m) | 10.050 | 10.542 | 9.757 | 9.974 |
| world XY 종료 순변위 (m) | 9.797 | 10.512 | 8.708 | 9.998 |
| stall fraction ↓ | 0.00622 | 0.00424 | 0.00626 | 0.00630 |
| roll/pitch RMS ↓ | 0.0260 | 0.0284 | 0.0670 | 0.0656 |

**4650 vs 부모:** x/y오차 감소와 목표 10m에 더 가까운 진행(부모10.542→4650 9.757m, overshoot에서 undershoot로 전환), yaw오차 0.0786→0.1292 악화, 자세 RMS/정체 증가. 모두 20초 생존했고 접촉 종료는 없었지만 순간별 밀침 복구 시간은 episode raw로 측정 불가.

## 4. 기존 3정책 보고서의 유지·수정

**유지:** (a) H5 요철 진행은 생존률 100%나 혼합 tracking 평균으로 가려지는 중요 병목, (b) ACT 2700의 H5 진행 mean/P05는 기존 3정책 중 최고, (c) 별도 ACT 9999는 H1 위치, H3 비의도 x진행, H4 yaw 등에서 강하지만 H5 진행이 나쁨, (d) 생존과 위치/자세/진행/속도 추종 분리, (e) 로컬 수치를 공식 점수로 환산하지 않음.

**수정:** (a) `ACTRATE 부모→lin=0.65→+2K`는 제안 단계가 아니라 이미 완료된 OFFICIAL resume. (b) 4650에서 H5 x/y 오차는 개선돼도 진행 평균/P05는 부모보다 나쁘므로 `lin=0.65가 요철 병목을 해결했다`는 결론 불가. (c) 4650의 H3는 비의도 x진행이 거의 제거되지만 원점 복귀(world XY)는 크게 악화하므로 ‘lateral 성능 개선’으로 뭉뚱그리지 않음. (d) H4/H6 yaw, H1 자세 비용이 크므로 요철 하나만 보고 후속 reward를 채택할 수 없음. (e) ACT 9999는 ACT 2700의 동일 궤적 3K→10K 연장 근거 없음. (f) 10K 학습 TensorBoard의 훈련 곡선만으로 고정 H5 평가의 최초 악화 checkpoint를 확정할 수 없음.

**유지하되 표현 축소:** H5에서 `10K에서 3K 대비 악화`는 평가 정책 간 사실적 비교로 유지하지만, 정확히 어느 iteration에서 악화가 시작했는지, 원인이 추가 iteration인지, 학습 중 특정 reward 변화인지, 공식 H5 점수 변화인지 단정 금지.

## 5. 6영상 점검 범위 및 원자료 한계

- 4650의 6 MP4 각각 1920×1080, 50fps, 20초(1000frames) 확인, MP4 체크섬 검증. 영상의 실제 `maneuver_push` 조건은 단일 env, seed42, 처음 vx=1.0, 이후 lateral·회전 명령 전환 및 push가 섞인 별도 rollout. camera-off는 128 env×3seed, 8 case × 시간창, 10초 분기. 두 자료는 명령/지형/trajectory가 다르다.
- 4650 영상에서 1/5/11/18초 주변의 대표 프레임을 추출해 육안 점검했다(`video_4650_contact_sheet.jpg`). rough/boxes 지형 초기 구간의 동작과 이후 지형 패치 밖 이동은 확인 가능하나, stairs/inverted-stairs 중앙 다단 통과 완료나 매 step 자세/발 미끄럼/명령 변환 지연은 검증하지 않았다.
- Episode 필드에는 순간별 좌우 왕복 후 흔들림 파형, push 복구 지연, 발 접촉 속도 또는 실제 sliding 물리량이 없다. 행동 원인을 지어내지 않는다. 6영상은 수치 평가의 통계 표본으로 합산하지 않는다.

## 6. 다음 GPU 결정 — sibling unchanged +2K 한 건을 1순위

**목적:** 현재 모델 4650의 `lin=0.65` 변경이 같은 부모에서 일반적으로 일어난 추가 2K 학습 변화와 어떤 차이가 있는지 검증. 정책 승격이나 성능 향상을 사전에 약속하는 실험이 아님.

| 제약 | 통제군 설계 |
|---|---|
| 질문/Experiment | 기존 LINTRACK-065 resume의 인과 대비 질문에 속하는 **sibling unchanged control**. 변경이 0개라도 검증 질문은 동일하므로 별도 reward 가설로 자동 명명하지 않음 |
| 기준 학습 | OFFICIAL `ACTRATE-0001` fresh3K, 부모 `model_2700.pt`, SHA `e54d3389e20ea913968ef8d3edbea5004368ff225fa6b94f73fcd91cf93ca7ae` |
| 기준 reward | `track_lin_vel_xy_exp=0.50`, `action_rate_l2=-0.0001` 포함 부모의 **모든** 보상·환경·PPO를 그대로 유지 |
| 실제 reward 변경 | **없음** (`track_lin_vel_xy_exp` 0.50 유지) |
| 실행 형태 | **OFFICIAL native resume**, fresh 아님. 이미 완료된 4650과 sibling 관계. 검증된 원본 evidence/checkpoint_index의 `source_path` 사용 |
| 추가 학습 | 부모 `model_2700`에서 **+2,000 iteration**. 처리군 console 종료 `4699/4700`과 동급 학습량을 확인하고, **동일 번호 `model_4650`이 실제 보존되면 이를 기준 비교**. 로그 종료·checkpoint 선택을 구분 |
| 고정 조건 | 훈련 seed42, 4096 env(기존 학습 기록과 동일한지 공식 evidence에서 다시 점검), task source·Isaac 버전·PPO·optimizer/resume state·terrain curriculum 상태·save interval parity 검증 |
| 평가 기준 | 기존 camera-off `scenario7`과 동일 seed4201/4202/4203×128 env×8case, deterministic, 1000step/20초. **새 평가 GPU는 별도 승인 이후**, control raw가 없으므로 학습만으로 결론 불가 |

**사전 판정 문턱(정책 승격용, 원문의 기존 H5 P05 +0.5m 기준 활용):**

1. 처리군 4650 vs 동일 부모 unchanged sibling의 H5 **주변 P05 진행 +0.5m 이상**, 평균 진행 저하 없음, x오차 감소, <9.5m·stall tail 감소를 동시에 충족.
2. 부작용 guardrail: H3 종료 world XY 순변위 증가 **+0.25m 이내**, H4/H6 yaw 절대오차 증가 **+0.02rad/s 이내**, H1 roll/pitch RMS 증가 **+0.02 이내**를 잠정 허용선으로 사전 고정; H2/H7 목표 적분 오차와 H6 경사 평균·P05 진행이 의미 있게 악화하지 않을 것.
3. 모든 8case 최초 cohort base-contact 종료는 control보다 증가하지 않고, seed별 부호·최악 사례·cohort별 Δ P05도 확인. 조건을 만족하지 못하면 범용 후보 HOLD. **숫자는 운영 의사결정 문턱이지 공식 채점식이나 통계적 유의성을 보장하지 않는다**.

**대안 우선순위:** 별개의 `h1-submit-2` 기본 `action_rate_l2=-0.0005`를 유지하는 **fresh LINTRACK-065 5K**는 다른 질문이며, 4650의 `action=-0.0001` resume 근거로 승인할 수 없다. 그 실험은 같은 fresh5K unchanged `h1-submit-2` control이 필요하고, 현재의 회전/횡복귀 악화 신호 때문에 우선순위가 낮다. 다른 단일변수 가설(예: yaw reward)은 H4/H6 증상만으로 값을 제안할 인과 데이터가 부족해 보류.

**실행 전:** `19_ISSACSIMZ_EXTERNAL_EVIDENCE_CLI.md`의 OFFICIAL 학습 시작·resume 표준 절차, 실제 `issacsimz` README/CLI, 승인 reward show/diff, 실제 부모 run/index/source_path/checkpoint SHA, preflight를 검증한다. 기존 파일 삭제·ZIP 메타데이터 수정·출처 조작·GPU 학습 실행은 이번 분석에서 하지 않았다.

## 7. 후속 증거와 재현

- `scenario_summary.csv`: 4정책×8case+ALL 평균/P05/P95/최소·최대.
- `cohort_deltas.csv`: 4650/9999/TERM 각각과 부모 2700의 3,072 key 대응 오차·진행·자세/동작 차이. 각 case의 P05/평균/P95 변화 포함.
- `rough_cohorts.csv`: H5 384×4 episode 핵심 raw 및 worst-case ID.
- `protocol_verification.json`: manifest 정책 SHA/평가 명령/protocol 비교 결과.
- `reproduce.py`: 기존 두 원본 ZIP을 읽어 CPU에서 CSV/JSON 재집계하는 코드. numpy/pandas 필요.

**재현 방법:** 제공된 원본 ZIP 두 개와 `reproduce.py`를 한 폴더에 두고 `python reproduce.py --bundle H1_3policy_5K_bottleneck_full_bundle_20261014.zip --child model_4650_h1_6terrain_evaluation_20261011-030854_89b4c4a0.zip --out-dir H1_4policy_analysis_data` 실행. 이 Python은 해당 OS의 분석용 runner 예시이며 Isaac Lab 학습 실행기가 아니다.

**제약 요약:** 평가/protocol 및 공통 cohort index 확인=PASS. 물리적 trajectory 정확 대응, native training-side source/PPO parity 전체 확인, unchanged+2K control, independent train seed repeats, 공식 점수·실제 H5 악화 시작 시점=미확인. 질문의 평가 범위 바깥 사항은 결론으로 대체하지 않았다.
