# H1 `model_2700` — 6지형 영상·camera-off 평가 통합 정책 분석

- **분석 기준일:** 2026-10-10 (KST)
- **입력:** `model_2700_h1_6terrain_evaluation_20261010-012639_61aa406d.zip` **1개**. 분석 대상은 별도 정책과 비교되지 않은 **단일 checkpoint**이며, 아래 수치는 전부 이 ZIP의 Windows **PERSONAL** 데이터다.
- **판정: HOLD (현재 전천후 정책 후보로 즉시 채택 보류).** 유효한 전진 보행과 낮은 정체·낙상 신호가 있으므로 **후속 비교 후보로 보존할 가치가 있다.** 다만 정지·순수 횡이동 명령에서 유의미한 비의도 전진이 있고, 거친 지형의 추종 하위 꼬리가 약하며, 계단 중앙 다단 통과를 영상으로 입증하지 못했다. *평가 COMPLETE*는 정책 채택, 학습 완료, 제출·공식 점수와 다른 판정이다.

## 1. 결론: 생존은 확실하지만 목표 행동은 조건부 성공

**확인한 성공:** `evaluation/episodes.jsonl`의 3,072개 전부 20.0초 `timeout`, `survived=true`, `base_contact_failure=false`; 고정 평가 8개 case에서 종료 후 reset 없이 생존했다. 전진 H2는 속도 명령 적분 **15.0m** 대비 body-frame 전진 **15.326m**, H7 push는 **10.0m** 대비 **10.542m**, H6 10° 상·하행은 **20.0m** 대비 **20.052/19.834m**다. 각각 정지/낙상이 아니라 유용한 이동이 발생한 근거다. 그러나 body-frame 속도 적분은 **장애물 완주 판정이나 지도상의 순변위가 아니다**.

**가장 큰 행동 실패:** 정지 H1(명령 `[0,0,0]`)에서도 평균 **1.987m/20초**의 전방 속도 적분이 발생한다. 무작위 초기 yaw 때문에 `world_dx_m`의 부호 평균은 이를 숨긴다. 실제 월드 XY 순변위 *크기의 중앙값*은 **2.012m**다. 순수 횡이동 H3(처음 +0.3, 나중 −0.3m/s)에서도 **+1.677m**의 비의도 body 전진, 월드 XY 순변위 크기 평균 **0.669m**가 있다. 따라서 *서 있기*와 *앞으로 걷기*를 같은 성공으로 묶으면 안 된다. 이 정책은 **전진 유지에는 강하지만 전방 운동 억제에는 약하다**.

**강점과 비용:** H2 전진의 통합 tracking error **0.1188**이 가장 낮다. H6 경사는 진행량을 유지하지만 `roll_pitch_rms` **0.0355~0.0382**와 `action_delta_rms` **0.534~0.540**으로 H2 평지 전진 **0.0283 / 0.465**보다 더 움직임·자세 비용이 든다. H5 rough는 tracking **0.1781**, 특히 yaw 절대오차 **0.1343rad/s**로 가장 취약하고, 소수의 환경에서 진행 저하와 큰 흔들림이 함께 나타난다. 단일 공식 점수나 정규화 없는 합산점수로 바꾸지 않는다.

## 2. 정책 동일성과 평가 조건

| 구분 | ZIP에서 직접 확인한 값 | 해석 |
|---|---|---|
| 표시명 | `H1 model_2700` | 파일명은 checkpoint 표지이며 실제 학습 iteration/계보의 완전한 증명은 아님 |
| checkpoint | `model_2700.pt`; **SHA-256 `e54d3389e20ea913968ef8d3edbea5004368ff225fa6b94f73fcd91cf93ca7ae`** | `source_checkpoint.txt`, `evaluation_manifest.json`, `video_evaluation_link.json`의 SHA 일치. 원본 `.pt`는 ZIP에 없어 원본 파일을 독립 hash하지 못함 |
| 로봇 / 정책 | H1 / `Humanoid-v0`; RSL-RL checkpoint; deterministic inference | `preset=null`, `source_run_id=null` → 학습 Run·fresh/resume·부모 checkpoint **미확인** |
| 실행 상태 | `complete=true`, `smoke=false`, `execution_status=COMPLETE` | 7 scenario, H6 상·하 분리 **8 case**, 3 seeds × 128 env × 20초. 총 3,072 episode |
| 평가 ID | `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34` | `se3c-evaluation-v1` / `scenario7` `internal-suite-v1`; **PERSONAL / official_score=false** |
| 평가 seed / 환경 | 4201·4202·4203, 128 env/seed/case; camera off; difficulty 0.5 | 무작위 초기 위치 ±0.5m 및 yaw ±3.14rad, 평가 중 observation corruption 비활성, 기타 resolved case 설정 별도 기록 |
| 영상 조건 | 6 × 20초 × 1,000f @50fps, seed 42, env 1, 지형 seed 42 | `maneuver_push`; 최초 `[1,0,0]` 보행, 전역 시간 기준 명령 전환과 4회 측면 push; 상·하 경사 각각 10° |
| 환경 연결 | 영상 `environment.txt`: Isaac Sim 5.1.0-rc.19, Isaac Lab `3e73d6d…`, task git `ef10b7a…`; 평가 manifest: Isaac Lab 동일 git와 task source 4파일 fingerprint 기록 | **동일 policy SHA에 연결된 영상과 평가**이나 1:1 같은 에피소드/terrain instance가 아님. 영상 task git과 평가 source fingerprint는 서로 다른 표현이므로 코드 byte-parity까지 증명하지 않음 |

`evaluation/resolved_configs.json`은 실제 **평가** 당시의 agent/env/case 설정이고, `evaluation/evaluation.log`의 reward manager 표시도 평가 로딩 환경의 설정이다. 이를 곧바로 checkpoint를 학습한 reward나 `max_iterations`, 부모 계보로 단정하지 않는다. 별도 training archive·공식 제출 증거는 이번 ZIP에 포함되지 않았다.

영상 전역 명령은 **0–6초** body `vx=1.0`, **6–10초** `[0.5,+0.3,0]`, **10–14초** `[0.5,−0.3,0]`, **14–17초** `[0.5,0,+0.5]`, **17–20초** `[0.5,0,−0.5]`이다(속도 m/s, yaw rad/s). 각 **4·8·12·16초**에 월드 Y로 ±0.5m/s의 additive velocity push가 예정되어 있다. camera-off 평가는 **episode 기준 10초 command 기간**과 case별 설정을 사용하므로 영상의 속도 전환·push와 직접적인 paired 표본이 아니다. 영상의 `stairs`, `inverted_stairs`, `boxes`에는 대응하는 camera-off 정량 case가 **없다**.

## 3. 원자료 재집계 및 실패 집중도

계산은 `evaluation/episodes.jsonl` **3,072행**에서 `(scenario, case)`로 나눠 **episode 동일가중 평균**을 사용했다. 모든 case가 384행·모두 20초이므로 여기서는 8-case 동일가중 평균도 일치한다. `diagnostics.json`의 7개 scenario별 episode 수·tracking 평균·survival과 **전부 일치**했다. 3,072개의 `(scenario,case,seed,env_id)` cohort는 각각 episode **1개**, `episode_id` 중복 **0**, 누락 필드 **0**, terminated cohort **0/3,072**, terminated episode **0/3,072**이다. H6만 두 case이므로 H6 scenario 집계는 768행이다.

| 평가 case (N=384 각각) | 명령상 기대 전진 적분 / 실제 body 전진 (m) | tracking 평균 ↓ | `vx/vy/yaw` 절대오차 평균 ↓ | `stall` 평균 | 자세 RMS / `action_delta_rms` |
|---|---:|---:|---:|---:|---:|
| H1 정지 | 0 / **1.987** (비의도) | 0.1537 | .0994 / .0593 / .0830 | **0*** | .0231 / .357 |
| H2 전진 | 15 / **15.326** | **0.1188** | .0427 / .0627 / .0725 | .0040 | .0283 / .465 |
| H3 좌우 이동 | 0 / **1.677** (비의도) | 0.1526 | .0840 / .0673 / .0880 | .0062 | .0271 / .411 |
| H4 회전+전진 | 10 / 10.556 | 0.1535 | .0392 / .0655 / **.1183** | .0040 | .0279 / .432 |
| H5 rough | 10 / **9.948** | **0.1781** | .0592 / .0601 / **.1343** | .0056 | .0331 / .479 |
| H6 10° 상행 | 20 / 20.052 | 0.1361 | .0512 / .0582 / .0908 | .0040 | **.0382 / .534** |
| H6 10° 하행 | 20 / 19.834 | 0.1367 | .0497 / .0594 / .0919 | .0040 | .0355 / **.540** |
| H7 push+전진 | 10 / 10.542 | 0.1333 | .0544 / .0699 / .0786 | .0042 | .0284 / .437 |

*별표: H1의 `stall_fraction=0`은 정지 성공을 뜻하지 않는다. `|command_xy|≥0.2`인 step이 없어서 이 구현은 분모 0을 그대로 0으로 기록한다. H2–H7의 0.004~0.006은 **전체 유효 commanded-step 중** 저속 비율이며, 작은 값이 순간 외란 회복 시간 0을 의미하지 않는다.*

- **오차 지표의 정확한 의미:** `mean_tracking_error`는 step별 `sqrt((Δvx)²+(Δvy)²+(Δyaw-rate)²)`의 episode 평균이다. 속도와 각속도 단위가 섞여 **전체 값을 m/s로 표시하지 않는다**. `vx_error`, `vy_error`, `yaw_error`는 각각 절댓값 step 평균이다. `xy_rmse`/`yaw_rmse`는 별도 RMS이며, H5 `yaw_rmse=0.1815`, H4 `yaw_rmse=0.1419`; H6 상·하 `xy_rmse≈0.1298`은 H5 `0.1102`보다 높다. 즉 rough의 약점은 무조건 XY가 아니라 **yaw·불규칙한 하위 꼬리**이고, slope의 추종 비용에는 XY RMS와 높은 action 변동이 함께 있다.
- **단위·중복:** `forward_progress_m == integrated_body_forward_m`는 전 행에서 정확히 동일하다. 독립 진행 근거 두 개로 세지 않았다. `lateral_drift_m`는 실제 가로 변위가 아니라 **`|Δvy|` 속도오차 적분**이다(H3 평균 1.3455m). `world_dx_m/world_dy_m`는 시작 heading이 달라 부호 평균이 상쇄될 수 있고, world X만으로 회전/횡이동의 정체를 판정하지 않았다.
- **종합 평균:** episode 평균 tracking **0.14534**, survival **1.000**, mean stall **0.00400**. H6이 2 case이므로 7개의 scenario를 각각 동일가중하면 tracking **0.14662**로 달라진다. 공식 배점이나 성능점수가 아니라 집계 선택의 차이다.

### 하위 꼬리·seed·종료 근거

**H5 rough의 최악 조건:** 384개 episode 중 전진 P05 **9.592m**, 중앙값 **9.947m**, 최소 **8.815m**; tracking P95 **0.1916**, 최대 **0.2908**. 특히 `seed=4202, env_id=108`의 tracking **0.2908**, 전진 **8.815m**, `roll_pitch_rms=0.0999`, stall **0.019**가 동시에 나쁘다. 이는 **낙상은 아니지만 진행·방향 추종·자세가 함께 저하**된 concrete tail case다. 전체 rough에서 tracking >0.19인 episode **34/384**, 전진 <9.5m **6/384**이며, 일부분의 큰 저하를 평탄한 평균으로 지워서는 안 된다. 다만 한 outlier를 전체 rough의 필연적 실패로 일반화하지 않는다.

3개 **평가 seed**의 rough tracking 평균은 **4201: .1786 / 4202: .1776 / 4203: .1782**, 전진 평균 **9.946 / 9.959 / 9.939m**로 평균 경향은 유사하다. 하지만 각 seed 내부에 128 env가 있으며 이들은 **독립 training seed 384개가 아니다**. H2 전진의 tracking은 각 seed 약 **0.1187~0.1188**, H6 상행 평균 전진 약 **20.049~20.054m**다. 현 조건의 mean stability는 좋지만 거친 지형 tail이 남는다는 쪽이 정확하다.

**낙상/회복:** `end_reason=terminated`와 `base_contact_failure=true`는 모두 **0**. 종료 뒤 재시작한 cohort도 0이고 20초 생존은 확실하다. 다만 evaluator는 step-by-step 재기립 시간이나 push 직후 추종 오차의 시간구간을 이 JSONL에 남기지 않는다. H7 평균 tracking **0.1333**, 전진 **10.542m**, 모든 episode 생존은 **외란 하 작업 지속**을 뒷받침하지만 **밀침 직후 얼마나 빨리 원래 속도로 복구했는지**를 정량적으로 입증하지 않는다.

## 4. 여섯 MP4: 프레임별 지형·접촉·실제 이동

영상 6개를 압축 해제해 **각각 50fps × 1,000프레임 디코딩**, 전 시간대 contact sheet 및 **초반 0.4~6.0초 확대 프레임**, 후반·명령/외란 시점의 프레임을 조사했다. 아래 초는 영상 시간이며 `frame≈초×50`. 추적 카메라의 피사체 고정만으로 정체 여부를 판단하지 않고, **장애물 가장자리/패치의 상대적 이동과 발의 보행 자세**를 함께 봤다. 발 미끄러짐·공중 시간·관절 편차를 직접 수치화할 프레임별 추적값은 없다.

| MP4 / 해당 지형 | 관찰한 대표 구간 및 프레임 | 행동 판정과 정량자료의 관계 |
|---|---|---|
| `01_stairs.mp4` / pyramid stairs | **0.4~3.2초 (f20~160):** 계단 테두리/단 근처에서 교대 보행하며 옆의 단차 줄이 이동. **4.8~6.0초 (f240~300):** 계단 줄이 뒤로 멀어지고 평면 구간에서 계속 걸음. **8~19초 (f400~950):** 직립 보행/방향전환. | **계단 가장자리의 접근·국소 보행은 관찰**, 중앙의 여러 단을 순차적으로 실제 오르거나 완주한 근거는 **없음**. 이 지형의 camera-off 독립 계단 case도 없음. 아래 교대 검정 프레임을 낙상으로 보지 않음 |
| `02_inverted_stairs.mp4` / inverted stairs | **0.4~2.8초 (f20~140):** 좌측/뒤쪽에 역계단 줄이 보인 채 주로 평탄한 측면으로 걷는 자세. **3.2~5.2초 (f160~260):** 줄이 멀어짐. **8~19초:** 일반 보행 지속. | 실제 역계단 중앙 **다단 하강을 보았다고 할 수 없음**. 접근 경로가 계단을 비껴가는 장면에 가까우므로 통과 성공 자료로 승격하지 않음 |
| `03_boxes.mp4` / boxes | **0.4~3.6초 (f20~180):** 불규칙 블록 위/사이에서 발을 교대하여 옮기고 몸통 직립 유지. **4.0~5.2초 (f200~260):** 블록 패치 경계를 넘어 평지로 나감. **6~19초:** 평지 계속 보행. | **실제 블록 접촉·장애물 구간 진행**이 여섯 영상 중 명확함. 초기 블록 구간을 지나간 정성적 긍정 근거이나 전 시간 다난도 boxes 성공률이나 수치 누적 거리는 없음; camera-off boxes case 없음 |
| `04_random_rough.mp4` / rough | **0.4~3.6초 (f20~180):** 거친 패치 내 발 걸음·몸통 직립을 이어감. **4.0~5.2초 (f200~260):** 패치 경계 밖으로 나오며 넘어지지 않음. **8~19초:** 주로 평지 보행. | **초기 rough 진행은 실제로 확인**되며, 평가 H5의 전진 평균 9.948m·20초 생존과 방향은 일치. 하지만 영상 후반 대부분은 rough 패치 밖이고, H5 최악 tail의 원인을 단일 영상에서 재현한 것은 아님 |
| `05_slope_up_10deg.mp4` / 상승 10° | **0.4~3.6초 (f20~180):** 경사 텍스처 부근에서 보행 유지. **4~6초 (f200~300)** 이후 주변이 평탄하게 보이며 계속 움직임. **8~19초** 직립/방향 변경. | 설정은 명백히 **+10°**이고 정량 H6 상행의 전진 20.052m·생존은 긍정적. 그러나 추적 카메라만으로 **경사 위 체류·전체 경사 구간 완주거리**를 정밀 입증하지 못함 |
| `06_slope_down_10deg.mp4` / 하강 10° | **0.4~3.6초 (f20~180)** 경사 패턴을 지나 지속 보행. **4~6초 이후** 평면 구간, **8~19초** 직립 및 명령 변경에 따른 움직임. | **−10°** 조건의 단일 영상에서 즉시 낙상·뚜렷한 장기 정체는 보이지 않음. H6 하행 평균 진행 19.834m·action 변동 .540과 양립하지만 지속 경사에서 발 sliding이나 가속/감속을 재구성할 수는 없음 |

**명령·외란 교차 확인:** 영상에는 6초·10초에서 `vy`의 부호가 바뀌고 14초·17초에서 yaw 명령이 달라진다. 따라서 후반 화면상 전방 이동량이 달라진다고 곧바로 전진 실패로 볼 수 없다. 대표 **4·8·12·16초 부근(f200/400/600/800)** 전후에는 녹화된 단일 로봇이 쓰러진 채 남는 장면 없이 계속 걸으며, H7의 `0/384` 종료 결과와 **정성적으로 부합**한다. 영상의 전역 push 일정은 H7 평가의 episode 기준 push와 표본이 다르며, 자세 복구 시간이나 push 응답 오차는 직접 측정하지 않았다. 후반 다수 장면의 몸통·발 교대는 유지되지만, 수 장의 표본만으로 미세 hopping, foot-slide 부재를 확정하지 않는다.

**캡처 무결성과 예외:** 영상 자체는 여섯 파일 모두 1,000프레임으로 정상 디코딩된다. `01_stairs.mp4`는 **검정 502/1,000프레임**(f0·f2 및 모든 홀수 f1~f999)이며 유효 짝수 프레임 f4~f998에서 지형과 보행을 볼 수 있다. 다른 **5개 MP4는 f0 한 프레임만 검정**이고 f1~f998은 정상 영상이다. 이 문제는 정책 낙상이 아니라 **캡처 artifact**다. 다른 5개 영상의 **마지막 f999**에서도 직전 f998과 동떨어진 로봇의 축소/시점 이상이 공통으로 나타나 terminal 단일 프레임을 실제 쓰러짐으로 읽지 않았다. 기존 MP4는 재렌더·교체하지 않았다.

## 5. 의사결정 및 다음 한 가지 행동

**정책 목표에 대한 답:** 기본 H1 **전진·짧은 rough/boxes 패치·10° 경사에서 지속 보행**, 명령 있는 구간의 낮은 stall과 **20초 push 조건 생존**은 이미 유용하다. 하지만 **정지 유지와 순수 횡이동의 정확도**, H5의 yaw/자세 하위 꼬리, **계단 실제 연속 통과**는 전천후 임무 능력을 주장하기 부족하다. “회복”은 *외란 이후 행동 지속*까지는 지지되나 *안정적인 즉시 복구 시간*은 미확인이다.

**후보 의사결정: HOLD.** 이 파일을 **전진 중심의 PERSONAL 행동 검증 후보**로 보존하되 **전천후 H1 대표 정책이나 기존 정책 교체안으로 바로 PROMOTE하지 않는다**. REJECT할 만큼 보행이 무너진 증거도 없다. 상대적으로 좋아졌다는 결론이나 reward 변경의 인과효과는 이번 입력에 비교 checkpoint가 없어 내리지 않는다.

**다음 행동 한 가지 — 보존된 H1 대조 ZIP의 재사용 비교:** 이미 생성된 **`ORIENT-100 / model_2850` H1 Windows PERSONAL 통합 ZIP**(프로젝트 참고자료에 기록된 별도 checkpoint) 또는 그와 동등한 기존 H1 대조 ZIP을 확보해 **새 학습/평가 없이**, 두 `evaluation_manifest.json`의 **policy SHA·protocol ID·source fingerprint**, `resolved_configs.json`의 8 case·command·noise/terrain, 3 seeds/128 env가 맞는지 확인한 뒤 **`episodes.jsonl`에서 동일 cohort `(scenario,case,seed,env_id)`별 H1 정지 편향, H3 횡이동, H5 하위 꼬리, H6 자세/action, H7 종료**를 대조한다. 조건이 다르면 일치하는 축만 비교한다. 이는 **어느 checkpoint 행동이 더 적합한가**를 판단하는 기존자료 비교이며, reward 가설의 인과효과 실험이 아니다. 그 결과에서도 계단 중심 통과는 입증되지 않으므로, 채택 목적이 **실제 계단 완주**라면 이 별도 확인이 필요하다는 제약은 유지한다. **새 GPU 작업 승인 또는 자동 실행 요청이 아니다.**

### 검증·재현 위치와 검사 결과

- **checkpoint·완료·조건:** `source_checkpoint.txt`, `environment.txt`, `evaluation/evaluation_manifest.json`, `evaluation/resolved_configs.json`, `evaluation/video_evaluation_link.json`.
- **재집계:** `evaluation/episodes.jsonl` (`scenario`, `case`, `seed`, `env_id`, `episode_id`, `end_reason`, `survived`, 측정 필드); `evaluation/diagnostics.json`과 7개 scenario의 건수/평균/생존 일치. `evaluation/evaluation.log`는 보조 실행 로그, 모든 episode를 대체하지 않음.
- **시각 증거:** ZIP 루트 `01_stairs.mp4` … `06_slope_down_10deg.mp4`, 각 50fps, 위 표의 초/프레임 재확인 가능; frame-level 검정 프레임 조사.
- **파일 검사:** 원본 ZIP `testzip()` **PASS**, `SHA256SUMS.txt`의 **MP4 6/6 SHA-256 PASS**, evaluation policy SHA 3개 메타데이터 경로 일치, raw rows **3,072**, 중복 episode ID **0**, 코호트 3,072, 결측 지표 **0**, 7 scenario summary 일치. `.pt` 원본 미포함에 따른 독립 파일 동일성 검증은 수행하지 않음.
- **변경·실행 경계:** 입력 ZIP·기존 파일 변경 없음. Python으로 기존 episode 집계와 로컬 CPU 영상 디코딩/검사를 수행했으며 학습·Isaac Lab/GPU 평가·재렌더·export·외부 업로드·서버 작업은 수행하지 않았다.
