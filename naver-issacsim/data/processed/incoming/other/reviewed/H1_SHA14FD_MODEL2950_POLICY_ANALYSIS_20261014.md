# H1 `model_2950` (SHA `14fd…ffd6`) 6지형 영상·camera-off 평가 심층 분석

- **분석일:** 2026-10-14 (KST)
- **입력 원본:** `model_2950_h1_6terrain_evaluation_20261014-023343_bcda8c25.zip` 1개
- **정책 표시명:** **H1-14FD**. 원 checkpoint 경로의 `h1-actrate0001-airtime025-fresh3k`는 **경로에 기록된 설명명**이며 학습 reward 값·실제 Run·OFFICIAL provenance를 ZIP만으로 확증한 명칭이 아니다. 기존 `ANGTRACK-065/model_2950` 등 *동명이 checkpoint*와 구분한다.
- **판정 범위:** ZIP의 H1 Windows **PERSONAL** 평가·영상에 대한 행동 분석. 학습 성과, 변경 reward의 인과효과, 공식 제출/채점의 판정은 아님.

## 1. 결론 — 전진·외란 후 보행은 유효하지만 범용 후보는 **HOLD**

**목표 행동 달성은 부분적으로 확인된다.** 3,072개 평가 episode가 모두 20초 `timeout`까지 유지되고, 평지 전진 **14.093m / 명령 적분 15m**, 전진하면서 밀침을 받는 조건 **9.024m / 10m**, 경사 상행·하행 **19.030/18.649m / 각 20m**의 body-frame 전진 적분이 측정됐다. 여섯 영상에서도 로봇은 움직임을 지속하며, 특히 boxes·random rough 초기 구간에서 실제 요철을 밟고 빠져나온다. **살아만 있고 멈춰 있는 정책은 아니다.**

그렇지만 **전체 목표 수행 성공 또는 경쟁 후보보다 좋은 방향이라고 보기 어렵다.** (1) 정지 H1에서 **-0.689m**, 횡왕복 H3에서 **-0.697m**의 비의도 **후진 body 적분**이 384/384 episode에서 각각 발생하고, H3에는 평균 **1.690m의 시작-끝 world XY 순변위**가 남는다. (2) rough H5는 목표 10m에 비해 **평균 7.826m, 하위 5% 경계(P05) 7.153m, 최악 6.641m**이다. 384/384개가 9m에도 미달하지만 20초 생존한다. (3) 계단의 **중앙 다단 통과**는 두 영상에서 확인되지 않고, 정량 `scenario7`에는 계단/boxes case 자체가 없다. 낮은 stall·100% survival을 보행 목적 달성으로 대체할 수 없는 사례다.

**후보 결정: `HOLD` — 현재 범용 대표·제출 우선 후보로 채택하지 않는다.** 평지/경사 전진의 기술적 유용성은 보존하되, 횡왕복 위치 복귀와 험지 진행 부족을 해결하거나 기존 후보 대비 수용 가능한 교환인지 **기존 평가 원자료로 우선 확인**한다. `PROMOTE` 근거는 부족하며, 보행 자체가 무효이므로 즉시 `REJECT`할 수준은 아니다. 가장 큰 trade-off는 **전진 및 무낙상 ↔ 정지/횡방향 위치 제어·험지 속도추종**이다.

## 2. 정책 identity와 비교 가능한 조건

| 검증 항목 | ZIP에서 직접 확인한 값 |
|---|---|
| Robot / checkpoint | `h1` / 원본 경로 끝 `model_2950.pt`; `policy.kind=rsl_rl_checkpoint` |
| 정책 SHA-256 | `14fd9ad432dfc2ba7696b0d48d9a31753f42c74727083429cc9f2c7299aaffd6` |
| Provenance | `policy.preset=null`, `policy.source_run_id=null`; source 경로 문자열에 `20261013-144616-h1-actrate0001-airtime025-fresh3k` 포함. **공식 학습 Run ID로 확정하지 않음** |
| 평가 실행 | `PERSONAL`, `COMPLETE`, `complete=true`, `smoke=false`, `evaluation.log` child exit **0**, 2026-10-14 **02:06:05–02:33:42 KST** |
| 평가기 / protocol | `scenario7` internal-suite-v1; `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34`; deterministic inference / camera off |
| 범위 | 7 scenarios, **8개 case**(H6 상·하 분리), seed **4201/4202/4203**, case·seed당 128 env, 20초 고정 창, **3,072개 최초 cohort 및 3,072 episode** |
| 평가 설정 | command 10초 주기(조건별 고정), noise/corruption off, terrain difficulty **0.5**, rough generator 10행×20열, 경사 `slope=0.17632698`(약 10°), H7 설정상 push |
| source / 환경 fingerprint | task repo head `ef10b7a4…`; `humanoid_rewards.py` fingerprint `050b8ee7…`; agent config fingerprint `976cb139…`; 8 case×3 seed에 대한 applied-env fingerprint 기록. Isaac Lab commit `3e73d6dd…` |
| 영상 연결 | 6개 1920×1080/50fps/1,000프레임 MP4. `source_checkpoint.txt`, `BUNDLE_README.txt`, `evaluation_manifest.json`, `video_evaluation_link.json`에 **동일 정책 SHA**. 영상 SHA256SUMS 6/6 대조, ZIP CRC PASS |

**연결의 범위:** MP4와 camera-off 평가가 **같은 정책 SHA 기록**으로 연결된 것은 확인했다. 다만 native `.pt` 원본은 ZIP에 없어 그 모델의 바이트를 다시 해시한 검증은 아니다. 영상은 **num_envs=1, seed=42, terrain_seed=42, 초기 pose 고정**, 경사 ±10°/단일 tile(terrain `num_rows=1, num_cols=1`, `horizontal_scale=0.05`); 정량 평가는 여러 env의 별도 reset·다른 terrain generator(`horizontal_scale=0.1`)다. 영상과 평가의 20초가 동일 궤적 또는 동일 지형·명령 재측정은 아니다.

평가 명령은 H1 `0,0,0`, H2 `vx=0.5→1.0`, H3 `vy=+0.3→-0.3`, H4 `vx=0.5, yaw=+0.5→-0.5`, H5 `vx=0.5`, H6 `vx=1.0`, H7 `vx=0.5`이다(단위 m/s, yaw rad/s). 평가의 동일 `protocol_id`만으로 다른 정책의 PPO/source/terrain randomization까지 동일하다고 단정할 수 없다. `resolved_configs.json`의 `max_iterations` 같은 **평가기 로드 설정을 학습 iteration으로 역추정하지 않는다**.

## 3. `episodes.jsonl` 직접 재집계 — 생존 이상의 품질

**검증:** 정확히 8 case×3 seed×128 env = **3,072 고유 `(scenario, case, seed, env_id)`**, episode ID 중복 **0**, 모든 `-n0` 최초 episode, 추가 reset 행 **0**, `duration_s=20.0` 전부, `end_reason=timeout` **3,072**, `survived=true` **3,072**, `base_contact_failure=false` **3,072**. 관련 지표 누락 없음. raw episode별 `mean_tracking_error` 단순 평균이 `diagnostics.json`의 각 scenario 값과 계산상 일치한다. 즉 여기서는 **episode 실패율 0/3,072**, **20초 cohort 내 한 번 이상 terminated된 비율 0/3,072**가 우연히 같지만 정의는 다르다. 실제 넘어짐이 없었다는 것은 *이 내부 고정 평가 조건*에 한정된다.

아래 값은 모두 **원자료 직접 계산**, 각 행 **384 episode 동일가중 평균**이다. `tracking`은 세 오차의 혼합 크기 평균이라 단일 물리 단위가 없다. `vx/vy/yaw`는 각각 절대 오차 평균(m/s, m/s, rad/s), 진행은 `forward_progress_m`인 **body-frame 전진 속도 적분**이다. 목표는 고정 command를 20초 적분한 참고값이지 공식 합격선이 아니다.

| 평가 case | Tracking ↓ | vx / vy / yaw 오차 ↓ | Body 전진 적분 / 명령 적분 (m) | World XY 순변위 크기 평균 (m) | Stall fraction ↓ |
|---|---:|---:|---:|---:|---:|
| H1 정지 | 0.14538 | .036 / .078 / .099 | **-0.689 / 0** | **0.674** | **0.0000** |
| H2 전진 | 0.15321 | .049 / .078 / .101 | **14.093 / 15** | 13.947 | 0.0050 |
| H3 순수 횡왕복 | 0.14574 | .036 / .083 / .094 | **-0.697 / 0** | **1.690** | 0.0090 |
| H4 전진+회전 | 0.18111 | .049 / .081 / **.139** | **9.037 / 10** | 4.539 | 0.0050 |
| H5 rough 전진 | **0.20204** | **.117** / .074 / .112 | **7.826 / 10** | 7.535 | 0.0100 |
| H6 경사 상행 | 0.18937 | .069 / .075 / .135 | **19.030 / 20** | 18.327 | 0.0050 |
| H6 경사 하행 | 0.19733 | .081 / .078 / .133 | **18.649 / 20** | 18.014 | 0.0050 |
| H7 push+전진 | 0.14903 | .059 / .083 / .084 | **9.024 / 10** | 8.984 | 0.0059 |

- **전체 episode 동일가중 tracking 평균 0.17040**. H6이 두 case라 768 episode로 반영된다. 이번 자료에서는 각 8개 case가 384행으로 같아 *case 동일가중 평균*도 0.17040이다. scenario 평균 7개의 단순 합산이나 공식 가중 점수를 만들지 않았다. `xy_rmse` 전체 평균 **0.13366m/s**, `yaw_rmse` **0.13837rad/s**는 각각 축 절대오차 평균과 별개다.
- **정지 H1의 핵심 실패는 조용한 후진 드리프트**다. `forward_progress_m` **-0.640~-0.750m**(전 episode 음수), world XY 순변위 평균 **0.674m**. 평균 `world_dx=-0.022m`만 보면 제자리처럼 보이나, env별 초기 yaw가 달라 월드 X/Y 부호가 상쇄된 것이다. 정지에서는 `stall_fraction=0`이 **유효 명령 step이 없어서 기록된 0**일 뿐 성공 판정이 아니다.
- **H3에서는 횡속도 추종 오차만 보면 실패가 가려진다.** `vy_error=0.08265m/s`, `stall≈0.009`이지만 목표는 10초마다 반대 방향으로 움직여 위치를 되돌리는 것이고, 평균 시작-끝 XY 순변위는 **1.690m**다. 이는 `|Δvy|` 적분인 `lateral_drift_m=1.653m`와 **서로 다른 값**이며, 영상의 혼합 command로는 순수 H3 복귀 동작을 재현하지 못한다.
- **H2/H6/H7은 유효한 전진이나 명령을 조금씩 놓친다.** body 적분 목표 대비 H2 약 0.907m, H6 상행 0.970m·하행 1.351m, H7 0.976m 부족하다. H4에서 world 순변위 4.539m가 body 전진 9.037m보다 작은 것은 회전 경로 때문이므로 stall로 세지 않았다. H4의 `yaw_error=0.13881rad/s`는 이 후보의 회전 추종 약점이다.
- **보행 비용 trade-off:** 평균 `roll_pitch_rms`는 H6 상행 **0.09693**, 하행 **0.09132**, H2 **0.09020**이고 H5는 **0.06667**이다. `action_delta_rms`는 H6 **상행 0.48916 / 하행 0.50678**로 높고 H4는 0.36801이다. 경사의 빠른 전진은 자세/액션 변화가 상대적으로 큰 상태에서 나타난다. 보존된 지표만으로 발 미끄럼 거리·air time·관절 deviation을 수치화하지 않았다.

### 실패 꼬리, seed 일관성, 정체의 해석

H5는 낙상이나 장시간 정체가 아닌 **지속적인 저속 진행**이 핵심이다. 384개 모두 9m 미만, **252/384개가 8m 미만**, **12/384개가 7m 미만**인데 `stall_fraction>0.05`는 **2/384개뿐**(최댓값 0.064). `stall`은 명령 속도 ≥0.2m/s일 때 실제 body XY 속도 <0.1m/s인 시간 비율이어서, 명령 0.5m/s를 0.35~0.45m/s로 계속 못 따라가는 문제를 잘 잡지 못한다. H5 `vx_error` 평균 **0.11709m/s**는 H2 **0.04897m/s**보다 크다.

H5 원자료 분포: **진행 P05/중앙값/P95 = 7.153/7.844/8.423m**, 최소 **6.641m**, 최대 **8.833m**. Tracking **P95=0.23361**, 최악 **0.26104**. 같은 384행에서 진행과 tracking의 상관은 **-0.940**, 진행과 `vx_error`의 상관은 **-0.981**이다. 이는 느린 cohort에서 오차도 커진다는 **기술통계**이지 새 reward의 원인이나 별도 학습 seed 반복의 증거가 아니다. 극단 사례 `H5-rough-s4202-e103-n0`는 **6.641m / tracking 0.25876 / stall 0.042**: 거의 정체 없이도 목표 진행을 크게 놓친다.

H5 seed별 **평균 진행 / P05 진행 (m)**은 `4201: 7.819/7.094`, `4202: 7.855/7.189`, `4203: 7.805/7.158`이다. seed 평균값의 차이보다 각 seed 안 env별 진행 분포가 훨씬 크다. 이 결함은 특정 seed 한 개에만 집중되지 않는다. 반대로 H2 seed별 평균 진행은 **14.0929/14.0937/14.0928m**로 매우 근접하다. 128개의 env와 3개 평가 seed는 독립적인 *training* seed 384개가 아니다. 관찰 결과에 근거 없는 유의확률을 부여하지 않았다.

## 4. 6개 MP4 실제 프레임 관찰과 정량 연결

6개 모두 프레임을 디코딩해 **초반·장애물 접촉 구간·중반 command 전환·후반**을 살폈다(기본 0.5~19.5초 시점 16개 + 확대 관찰 0.8~16.3초 12개/영상, 일부 초기 인접 프레임 추가 확인). 아래 시간은 **영상의 global clock**, `#`는 50fps의 실제 프레임 번호다. 정밀 관절/슬립 추적이나 모든 프레임 연속 분석은 수행하지 않았으므로 미세 sliding, 접촉력, 회복 지연시간을 단정하지 않는다.

| MP4 | 접근 → 접촉·진행 → 후반에서 실제 관찰한 것 | 판단 / 정량과의 연결 |
|---|---|---|
| `01_stairs.mp4` | **0.8~2.5초 `#40~125`** 계단 모서리가 로봇의 측면·전방 가까이에 보이고, **3.5~6초 `#175~300`** 계단 선을 옆에 둔 채 보폭을 지속한다. **8초 `#400` 이후** 주로 평지. 가시 샘플에서 바닥 낙상 없음. | 계단 **가장자리 인근 이동**은 보이지만 중앙 여러 단을 발로 딛고 통과했다고 확인할 수 없다. stairs 정량 case 없음. |
| `02_inverted_stairs.mp4` | **0.8~3.5초 `#40~175`** 역계단 선과 매우 가까이 이동하고, **4.3~6초 `#215~300`** 선이 뒤/측면으로 사라진다. 이후 평지 보행·명령 전환 관찰. | 역계단 중앙 다단 하행을 입증하지 못한다. 비낙상 장면은 정량 성공률이 아니다. |
| `03_boxes.mp4` | **0.8~4.3초 `#40~215`** 높낮이 있는 박스 블록 사이/윗면에서 무릎을 들어 교대 보행하며 진행하고, **5.2~6초 `#260~300`** 박스 지역에서 나와 평지로 이동한다. 낙상 없이 자세 유지. | **장애물 접촉을 동반한 실질적 초기 구간 진행**의 강한 시각적 근거. 다만 단일 tile·한 궤적이며 평가에는 boxes case 없음. |
| `04_random_rough.mp4` | **0.8~4.3초 `#40~215`** 불규칙 요철 표면에서 발을 교대하며 이동, **5.2초 `#260`** 가장자리, **6초 `#300`** 이후 평지. 발이 높은 장애물에 걸려 완전히 멈추거나 넘어지는 장면은 샘플에서 보이지 않는다. | 초반 rough 접근/진행은 확인. 그러나 별도 H5 camera-off에서 평균 **7.826/10m**이고 하위 꼬리도 나쁘다. 영상 후반 평지 걷기를 험지 20초 완주로 세면 안 된다. |
| `05_slope_up_10deg.mp4` | **0.8~5.2초 `#40~260`** 완만한 높이무늬의 구간에서 반복 보행, **8.2/12.2/16.3초 `#409/#610/#815`** 이후에도 보행·방향 변환 유지. 가시 샘플상 낙상 없음. | H6 상행의 높은 body 전진 적분 **19.030m**과 양립. 화면만으로 20초 내내 정확한 10° 경사를 전부 통과했는지 계산할 수 없음. |
| `06_slope_down_10deg.mp4` | **0.8~5.2초 `#40~260`** 하행 구성의 높이무늬 구간에서 교대 보행; **8.2/12.2/16.3초** 전후 가시 자세 유지. 아래쪽으로 급격히 무너지거나 바닥에 접촉하는 장면은 표본에서 없음. | H6 하행 body 전진 **18.649m**, 상행보다 tracking이 약간 높고 action 변화도 큼. 경사 전체 통과율·정확한 pitch는 영상으로 계측하지 않음. |

**영상의 혼합 command/push를 따로 해석:** `environment.txt`의 video schedule은 **0–6초 `vx=1.0`**, **6–10초 `vx=0.5, vy=+0.3`**, **10–14초 `vx=0.5, vy=-0.3`**, **14–17초 `vx=0.5, yaw=+0.5`**, **17–20초 `vx=0.5, yaw=-0.5`**이며, **4/8/12/16초에 world-Y ±0.5m/s 속도 충격**을 준다. 접촉 및 command 전환 후 **4.3초 `#215`, 8.2초 `#409`, 12.2초 `#610`, 16.3초 `#815`**에서 여러 지형 영상의 보행이 유지되는 것은 **정성적인 외란 견딤/재개 신호**다. 그러나 이들 화면은 H7 evaluator의 push 조건과 동일한 시험이 아니고, 충격 직후의 속도 회복시간·오차 면적을 측정하지 못했다. 영상에는 `vx=0` 순수 lateral H3가 없으므로 H3 횡제어 성공을 영상으로 주장하지 않는다. 14초 이후 로봇 방향 변화도 계획된 회전 명령이므로 전진 실패로 보지 않는다.

**캡처 결함:** 여섯 MP4 모두 `#0`은 검정 프레임이고 `01_stairs.mp4`의 초기 `#2`도 검정이다. `#1/#3`, `#49/#50/#51`, `#99/#100/#101` 등 인접 프레임을 확인했고 이후 여러 시간대에서도 유효 프레임이 있었다. 이전 *다른* 정책에서 보고된 전 구간 parity 교대 검정 현상을 이 영상에 소급하지 않는다. 검정 시작 프레임은 **캡처 artifact**이지 정책 낙상이 아니다. 원본 영상은 재렌더·교체하지 않았다.

## 5. 기존 정책 기록에 비춘 방향성 — 직접 A/B가 아닌 참고 비교

업로드된 별도 프로젝트 참고자료 `00_START_HERE_CONTEXT_AND_MAP.md`, `06_HUMANOID_TRAINING_CODE.md`, `21_WINDOWS_GO2_VIDEO_AND_EVALUATION.md`의 **2026-10-10 과거 원자료 분석 기록**에 따르면, 이전 `ACTRATE-0001/model_2700` 정책은 같은 이름 계열의 **다른 checkpoint**로서 rough H5 평균/P05 **9.948/9.592m**, H1 정지 비의도 body 전진 **+1.987m**, H3 비의도 전진 **+1.677m**, 전체 혼합 tracking **0.14534**, 전체 `action_delta_rms` **0.45687**, 전체 `roll_pitch_rms` **0.03019**로 기술돼 있다.

이번 **H1-14FD**는 자체 raw 기준 rough **7.826/7.153m**, H1/H3 body 전진 **-0.689/-0.697m**, tracking **0.17040**, action Δ RMS **0.42350**, roll/pitch RMS **0.08157**다. **기록 수준에서** 정지·lateral의 *전진 누수 크기*는 작아 보이지만 **방향이 후진으로 바뀌었고**, rough 평균 진행은 약 **2.122m**, P05는 약 **2.439m** 낮으며 혼합 tracking도 높다. action 변화 하나만 낮다고 종합 개선으로 채택할 수 없다. 특히 rough 후퇴가 크다는 **경고 신호**다.

**비교 경계:** 이 보고서에 입력된 평가 ZIP은 **현재 1개뿐**이다. 과거 모델의 `episodes.jsonl`, 실제 `resolved_configs.json`, source/agent/terrain fingerprint, 원본 MP4를 **이번 작업에서 재열람·재대응하지 않았다**. 과거 요약 수치는 *외부 참고 기록의 인용*이지 지금 계산한 matched A/B가 아니다. source 경로의 `ACTRATE0001-AIRTIME025` 텍스트만으로 `feet_air_time`의 독립 효과 또는 같은 시작 checkpoint/학습 조건을 증명하지 않는다. 그러므로 과거 수치와의 차이는 **우선 확인할 trade-off**, 인과적 우열·공식 점수·통제된 개선율이 아니다. 반면 이번 ZIP **하나만으로도** H5 지속 저속, 정지/횡이동 잔류 변위, 전진·경사 이동 능력에 대한 자체 행동 판정은 유효하다.

## 6. 다음 행동 한 가지와 재현 가능한 근거

**다음 행동(추가 GPU 불필요):** 이미 보존된 **`ACTRATE-0001/model_2700`의 Windows PERSONAL 평가 원본 ZIP**을 찾아, 먼저 이번 정책과 robot·protocol·`resolved_configs.json`(명령, noise, 지형/난이도, 시간창), evaluator source/agent/applied-env fingerprint, seed·case·cohort key가 대응하는지 검증한 다음 **H1 정지 world 순변위와 body 누수, H3 횡왕복 복귀/접촉, H5 rough 진행 P05·최악 및 tracking·자세/액션**만 최초 cohort 기준으로 대조한다. 동일 ID를 동일 물리 궤적으로 해석하지 않는다. 이번 rough 열세와 위치제어 개선이 공통 조건에서도 유지된다면 **H1-14FD의 대표 후보 채택을 계속 보류하고 기존 전진/험지 후보 우선**; 반대로 비교 조건 불일치로 발생한 겉보기 차이라면 matched 재집계 근거 범위에서 HOLD를 재검토한다. 새 학습·평가·영상 생성·export는 이 결정에 포함하지 않는다.

**이번 판단의 재확인 경로(모두 입력 ZIP 내부):**

- **정책·실행:** `source_checkpoint.txt`, `environment.txt`, `evaluation/evaluation_manifest.json`, `evaluation/video_evaluation_link.json`, `evaluation/evaluation.log`
- **설정·계산:** `evaluation/resolved_configs.json`, `evaluation/episodes.jsonl`(위 직접 재집계의 근거), `evaluation/diagnostics.json`(재집계 cross-check), `evaluation/README.txt`
- **프레임·캡처:** 루트 `01_stairs.mp4`~`06_slope_down_10deg.mp4`, `SHA256SUMS.txt`, `README.txt`, `BUNDLE_README.txt`

**계산 규약:** 원자료 JSONL 전체를 case/seed/`env_id`로 분류하고 episode별 지표를 동등 가중 산술평균; P05·P95는 관측 episode 분포의 분위수; world 순변위는 각 episode에서 `hypot(world_dx_m,world_dy_m)`를 먼저 계산 후 평균; 첫 cohort 종료 여부는 `(scenario,case,seed,env_id)`별 원 시간창의 `terminated` 여부로 집계. `forward_progress_m`와 `integrated_body_forward_m`은 **3,072행 전부 정확히 같아** 하나의 근거로만 사용했다. `lateral_drift_m`는 `|vy 추종오차|`의 적분으로 취급했다. 결측값을 0으로 채우지 않았고, 실패 episode를 제외하지 않았으며 공식 합산점수를 만들지 않았다.

**최종 판단:** 유용한 실제 보행·경사 전진·초기 장애물 접촉은 확인되지만, 정지/횡왕복 위치 제어와 rough 진행의 보편적 손실이 커서 **현 정책 후보 `HOLD`, 범용 대표로는 비채택**. **추가로 먼저 할 일은 새로운 GPU 평가가 아니라 기존 비교 정책의 원본 평가와의 조건·cohort 재대조다.**
