> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/incoming/other/reviewed/H1_ORIENT-100_POLICY_ANALYSIS_20261007.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# H1 `ORIENT-100` (`model_2850`) — 6지형 영상·개별 평가 통합 정책 분석

- **분석일:** 2026-10-07
- **입력:** `model_2850_ORIENT-100_h1_6terrain_evaluation_20261007-010444_f6b3b8b3.zip` (단일 후보·18개 엔트리: MP4 6개, 텍스트/평가 원자료 12개)
- **증거 등급:** Windows **PERSONAL** 재생·camera-off fixed-scenario 진단. 대회 OFFICIAL 점수, 학습 성공 판정, 제출 상태가 아님.
- **판정 대상:** ZIP에 연결된 checkpoint의 **관찰 가능한 행동**. `ORIENT-100`은 제공 파일의 표시명이며 reward 변경 효과를 검증한 비교 실험명이 아님.

## 1. 결론 — 현재 후보 **HOLD**, 그러나 보존할 가치가 높은 보행 정책

**확인된 성공:** 7개 시나리오·8개 case·3개 평가 seed·128개 env에서 **3,072/3,072 episode가 20초 timeout으로 생존**, `terminated`·`base_contact_failure`가 **0건**이다. 이는 단순히 서 있기만 한 결과가 아니다. 평지 가속 전진(H2)은 몸체 기준 **15.41 m/20초**(명령 적분 15.0 m), 외란 조건(H7)은 **10.53 m**(명령 적분 10.0 m), 10° 상·하 경사(H6)는 각각 **20.43/20.17 m**(명령 적분 각 20.0 m)의 실제 전진 적분을 남겼다. 6개 영상에서도 관찰 가능한 구간 내 넘어짐 없이 보행하고, 박스와 거친 지면의 **초반 구간을 빠져나가는 행동**이 보인다. 따라서 **안정적 이동·기본 속도 추종·외란을 받으면서 보행 지속하는 능력은 있다.**

**가장 큰 약점:** (1) *정지 명령* H1에서도 몸체 전진 적분 **+1.63 m/20초**로 미세하지만 누적되는 **원치 않는 전진**이 있으며, 순수 횡이동 H3에서도 **+1.18 m** 전진한다. (2) **random rough(H5)**에서 통합 tracking 오차가 가장 크고(`0.1709`), 최저 진행 episode는 **7.83 m/20초**로 10 m 명령 적분에 크게 못 미친다. (3) 6개 영상 중 계단 중앙의 확실한 반복 단차 극복·정량적 복원 시간은 입증되지 않고, 약 **5~6초 이후 대부분의 화면은 해당 지형 패치 밖의 평지**다. (4) 동일 평가의 `h1-submit-2 / TERM-50` 대조군이 없어 `flat_orientation_l2` 완화가 실제 개선을 만들었는지 말할 수 없다.

**결정:** **HOLD — 현재 대표·제출 정책으로 확정 채택하지 않는다.** 다만 **REJECT가 아니다.** 실제 진행과 다조건 생존이 충분히 좋아 동일 protocol 대조의 **우선 비교 후보**로 보존한다. 단일 정책에서 절대 행동 능력은 긍정적으로 판정하되, **계단 통과/정지 품질과 기준 정책 대비 개선**을 확인하기 전 `PROMOTE`로 승격하지 않는다. `ORIENT-100`의 reward 효과나 OFFICIAL 점수 향상은 별개로 미검증이다.

## 2. 정책 identity 및 실제 비교 가능 범위

| 확인 항목 | 이번 입력에서 확인한 값 |
|---|---|
| 정책 표시명 / 파일 | `ORIENT-100` / `model_2850_ORIENT-100.pt` (ZIP의 `source_checkpoint.txt`) |
| 원본 checkpoint **기록된** SHA-256 | `6aedeced60562c1d496d5319d29b76cf9e26ff43df06827cb370f24f5313f7b0` |
| 로봇 / actor | `Humanoid-v0` / deterministic inference; `rsl_rl_checkpoint` |
| 평가 상태 | `complete=true`, `execution_status=COMPLETE`, `smoke=false`, child exit 0, fatal traceback 없음 |
| 평가 범위 | `scenario7` · H1~H7, H6 상/하 별도 → 8 case × seed `4201,4202,4203` × 128 env × 20 s |
| 평가 protocol ID | `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34` |
| 평가 실행 환경 | Windows PERSONAL, RTX 3060 Laptop; Isaac Lab commit `3e73d6dd79080fd7632488c061052a6edd52e230`, PyTorch `2.7.0+cu128` |
| 영상 환경 | 6 × 20 s × 50 fps × 1 env, seed 42, `maneuver_push`; Isaac Sim `5.1.0-rc.19`, 위와 같은 Isaac Lab commit |
| source 구분 | 영상 `task_repo_git_head=ef10b7a4…`; 평가 `humanoid_rewards.py` fingerprint `050b8ee7…`, `h1_task/env_cfg.py` fingerprint `9116769a…`. 실행기의 서로 다른 fingerprint 형식이며 task source **byte 동일성을 독립 검증한 것은 아님** |
| 학습 identity | 평가 manifest의 `preset=null`, `source_run_id=null`; 부모 checkpoint·fresh/resume·training seed/iterations·실제 reward 값·제출 여부는 **이 ZIP만으로 미확인** |

`evaluation/evaluation_manifest.json`, `evaluation/video_evaluation_link.json`, `source_checkpoint.txt`, `BUNDLE_README.txt`에 기재된 **policy SHA가 네 곳에서 동일**하고 video link의 protocol ID도 manifest와 같다. **영상·평가의 기록상 checkpoint 연결은 성립**한다. 다만 `.pt` 원본 자체는 ZIP에 없으므로 이 SHA는 **원본 checkpoint를 새로 hash해 검증한 값이 아니라 수집 metadata의 일치**다. ZIP 전체 CRC 검사는 통과했고 6개 MP4는 프레임 디코딩 가능하다(02번의 캡처 결함은 §4 참조).

**조건을 섞지 않는 이유:** camera-off 평가의 명령은 episode별 H1 정지, H2 전진 `0.5→1.0`, H3 횡이동 `+0.3→-0.3`, H4 `(vx=0.5, yaw=+0.5→-0.5)`, H5 rough `vx=0.5`, H6 slope 상·하 `vx=1.0`, H7 flat `vx=0.5`와 ±0.5 m/s 외란이다. 명령 전환은 기본 10초 episode clock이며 H7 외란은 4·8·12·16초. 평가에서는 평지/rough/경사, case별 난이도 `0.5`가 설정되고 terrain generator case는 **10×20 tile, 각 8×8 m**이다(`evaluation/resolved_configs.json`). 초기 위치·yaw도 범위 내 무작위 reset이다. 반면 영상은 **지형 하나의 1×1 tile, 영상용 10° 경사, 고정 pose·noise off**, 다섯 단계의 별도 명령과 전역 영상시계 외란을 쓴다(`environment.txt`, `README.txt`). **영상의 20초와 평가의 20초는 대응 episode가 아니다.** H1 영상 경사는 **10°**이지 다른 로봇용 20° 조건이 아니다.

## 3. episodes.jsonl 직접 재집계: 전진은 실재하지만 험지·정지에 비용

**집계 계약:** 총 **3,072 raw episode = 3,072 최초 `(scenario,case,seed,env_id)` cohort**, 각 cohort당 episode 1개(`n0`, 중복 ID 0). 재시작으로 생성된 추가 episode는 없다. 전 행이 `steps=1000`, `duration_s=20.0`, `end_reason=timeout`, `survived=true`, `base_contact_failure=false`; 필드 누락 없음. 다음 표는 **각 case의 384개 episode 단순 평균**, H6 상·하를 합치지 않았다. `diagnostics.json`의 scenario별 episode 가중 tracking/생존과 재계산 차이는 부동소수점 반올림 수준이다.

| scenario / case (명령) | tracking 오차¹ | 절대 `vx / vy / yaw` 오차² | `xy_rmse / yaw_rmse`² | body 전진 적분 (m) | stall (%) | action Δ RMS |
|---|---:|---:|---:|---:|---:|---:|
| H1 balance, flat (0,0,0) | **0.1171** | .0818 / .0527 / .0492 | .1046 / .0662 | **+1.633** | **0.00³** | .256 |
| H2 forward, flat (vx .5→1.0) | .1270 | .0476 / .0626 / .0800 | .1060 / .1085 | **15.408** | 0.70 | .373 |
| H3 lateral, flat (vy +.3→−.3) | .1200 | .0592 / .0639 / .0604 | .1054 / .0823 | **+1.180** | 0.90 | .276 |
| H4 rotation, flat (vx .5; yaw +.5→−.5) | .1429 | .0442 / .0625 / **.1026** | .0968 / .1281 | 10.525 | 0.60 | .353 |
| H5 random rough (vx .5) | **.1709** | .0695 / .0613 / **.1190** | .1241 / **.1557** | **9.451** | **0.96** | .355 |
| H6 slope **up 10°** (vx 1.0) | .1578 | .0651 / .0622 / .1051 | .1403 / .1388 | **20.426** | 0.70 | .452 |
| H6 slope **down 10°** (vx 1.0) | .1586 | .0602 / .0657 / .1087 | .1392 / .1419 | **20.173** | 0.70 | **.464** |
| H7 flat + push (vx .5) | .1291 | .0535 / .0659 / .0745 | .1205 / .1029 | **10.530** | 0.72 | .332 |

¹ `mean_tracking_error`는 step별 `sqrt(Δvx²+Δvy²+Δyaw-rate²)` 후 episode 평균이므로 **단일 물리 단위 없음**. 전체 episode 동일가중 평균은 **0.14041**, 7개 scenario 동일가중 평균은 **0.13787**(H6가 2 case라서 다름). 이것을 공식 점수로 환산하지 않는다. ² `vx/vy` 절대오차·`xy_rmse`는 m/s, `yaw` 절대오차·`yaw_rmse`는 rad/s. 절대오차 평균과 RMSE는 다른 집계다. ³ 정지 H1은 stall 분모가 되는 명령 XY 속력 `≥0.2 m/s` step이 없어 evaluator 구현상 **0으로 기록**된다. 이는 정지 위치를 지켰다는 증거가 아니다. 전진 적분은 `forward_progress_m=integrated_body_forward_m`로 전 행 일치하며 **중복 측정 아님**. `lateral_drift_m`는 실제 횡변위가 아니라 `|Δvy|`의 시간 적분이다.

### 핵심 발견과 반대 근거

**A. 진행·추종:** H2의 명령 전진 적분 15.0 m 대비 실제 15.408 m는 **평지 목표 전진을 실질적으로 수행**했다는 강한 신호다. H7도 명령 10.0 m 대비 10.530 m로 4회의 외란 환경에서 전진·비낙상을 모두 유지한다. 반면 H1은 명령이 완전 정지인데 실전진 +1.633 m, `vx_error=.0818 m/s`로 누적 위치 유지가 약하다. H3은 순수 횡속도 명령 중 +1.180 m 전진하므로, 낮은 H3 tracking 총오차만으로 **깨끗한 측면 평행이동**이라고 부를 수 없다. H3의 `vy_error=.0639 m/s`, 횡오차 적분 `1.278 m`; 실제 좌우 변위의 시간별 분해 기록은 없다. `world_dx/world_dy` 평균은 무작위 시작 yaw 때문에 서로 상쇄되므로 제자리 움직임 판정에 쓰지 않았다. 특히 회전 H4의 몸체 전진 10.525 m에도 episode별 **world XY 순변위 크기 평균은 약 4.64 m**인데, 이는 회전 명령 아래 곡선 이동과 부합하며 stall 근거가 아니다.

**B. 지형 trade-off:** H5는 동일 `vx=.5`인 H7보다 body 전진 적분이 **1.079 m 적고**(`9.451` 대 `10.530`), tracking은 `0.0418` 높다. 다만 H7에는 push가 있고 H5에는 rough가 있어 **순수 terrain 효과의 통제 비교는 아니다**. H5의 명령 10 m 대비 평균 진행은 9.451 m, 최악 episode는 7.831 m. 각 episode가 20초 생존함에도 **진행 부족 + 추종 저하**가 동시에 발생한다. H5의 `roll_pitch_rms=.0587`은 H6 상·하의 `.0949/.0903`보다 작지만, 그 자체는 더 나은 요철 적응을 뜻하지 않는다. 보폭 축소/보수적 자세 같은 기전은 가능성일 뿐 관절·접촉 데이터 없이 확정할 수 없다.

**C. yaw와 동작 비용:** 회전 H4의 yaw 절대오차는 `.1026 rad/s`, yaw RMSE `.1281 rad/s`로 H2의 `.0800/.1085`보다 커져 회전 명령의 추가 부담이 나타난다. H6 상·하에서 `action_delta_rms=.452/.464`는 H2 `.373`, H7 `.332`보다 크다. 10° 경사 보행 시 출력 변화 비용이 커지는 신호이나 에너지/foot sliding/관절 편차 값이 직접 기록된 것은 아니다. 같은 H6에서 상행은 하행보다 평균 body 진행이 `0.253 m` 많지만 yaw 추종·자세 비용을 함께 보면 **상행 전면 우위라고 할 차이는 아니다.**

### 평균이 숨기는 거친 지면 최악 꼬리

- H5 `mean_tracking_error`: **중앙값 .1712 / P95 .1948 / 최대 .2412**. H2의 P95는 `.1285`다. H5 전진 적분은 **P05 8.863 m / 중앙값 9.450 m / 최소 7.831 m**이며 진행 ≤0인 행은 없다.
- H5 진행 **최하위 10% cohort 39개**에서 평균 진행 **8.790 m**, tracking **.1953**, stall **2.10%**. 최상위 10% 39개는 **10.061 m**, tracking **.1450**, stall **0.78%**다. 진행과 tracking 오차의 episode 간 상관은 **−0.897**. 이는 **동반 악화**의 기술통계이지 원인/독립 통계검정이 아니다. H5에서 stall >2%는 15/384, 최대 7.3%다.
- H5 seed별 tracking 평균은 `4201=.1712`, `4202=.1701`, `4203=.1714`, 진행은 각각 **9.441 / 9.475 / 9.438 m**. 평균 seed 간 방향은 유사하지만 **꼬리는 env/cohort에 집중**된다. 대표 최악은 `(H5,rough,4201,env6)`의 tracking `.2412`, 전진 `7.831 m`, stall `7.2%`; `(4203,env105)`도 tracking `.2231`, 전진 `8.385 m`, stall `7.3%`다. 많은 env를 별도 학습 seed로 세지 않는다.
- **실패 분모 별도 확인:** raw episode 실패 **0/3,072**, 한 번이라도 `terminated`된 최초 cohort **0/3,072**. H5 역시 **0/384**로, 나쁜 꼬리가 **낙상이 아니라 진행·추종 열화**에 나타난다. 반복 reset으로 실패가 가려진 데이터는 아니다.

## 4. 6개 MP4 직접 프레임 조사 — 지형 접촉과 생존을 분리

영상 메타데이터의 **영상 전역 시간표**: **0–6 s `(1.0,0,0)` → 6–10 s `(0.5,+0.3,0)` → 10–14 s `(0.5,−0.3,0)` → 14–17 s `(0.5,0,+0.5)` → 17–20 s `(0.5,0,−0.5)`**; 4·8·12·16 s에 world-Y **속도 변화 ±0.5 m/s**. `fps=50`, 1,000프레임/편이며 6편 모두 실제 프레임 표본을 여러 시간대에서 조사했다. 초반 지형 구간은 더 촘촘히 프레임을 대조했고, 8·16초 push 주변의 인접 표본도 조사했다. 정량적인 slip·clearance·회복 소요시간을 영상만으로 역산하지 않았다.

| 영상 (정확한 파일명) | 실제 관찰 장면 (초, 프레임) | 행동 해석과 남은 경계 |
|---|---|---|
| `01_stairs.mp4` | **2.0–4.0 s (f100–200)** 계단 줄무늬/단차 가장자리와 보행 경로가 교차하고 몸통은 계속 세워져 있음; **5–6 s (f250–300)** 계단 패치가 뒤로 멀어짐 | 접근·가장자리 보행과 패치 이탈은 보이나, **중앙 다단 계단을 위/아래로 완주**한 모습까지 판정하기 어렵다. 계단 접촉 모든 발의 높이·슬립 불명. |
| `02_inverted_stairs.mp4` | **0.1–4.0 s (f5,51,101,151,201: 홀수 프레임)** 계단 띠가 화면 왼쪽에 남은 채 평지 쪽으로 이동; **5 s 이후** 평탄 화면 | **역계단의 반복 단차를 직접 넘는 것까지 확인되지 않는다.** **프레임 0,2,…,998은 검정 500개 / 홀수 1,3,…,999는 가시 500개**인 교대 캡처 결함. 홀수 프레임으로 동작을 관찰했으며 정책 낙상으로 오인하지 않음. |
| `03_boxes.mp4` | **1.0–3.9 s (f50–194)** 크고 작은 블록 사이/인접 면에서 두 다리로 연속 스텝, 몸통이 무너지지 않음; **4.1–5.0 s (f206–250)** 블록 지역을 빠져나감 | **짧은 박스 지역 진행의 긍정적 영상 근거**. 모든 장애물 상면을 밟거나 박스 전체를 완주했다는 수치 증거는 아님. |
| `04_random_rough.mp4` | **1.0–3.9 s (f50–194)** 요철 지역 위에서 반복 지지 전환, 큰 넘어짐 없이 전진; **4.1–5.0 s (f206–250)** 패치 밖으로 이탈 | **거친 면에서 실제 초반 진행**을 확인. 그러나 이후 길게 보이는 동작은 대체로 평지 보행이고, camera-off H5의 하위 꼬리 저하를 이 **1개 seed/1개 경로**가 배제하지 못함. |
| `05_slope_up_10deg.mp4` | **1.0–5.0 s (f50–250)** 완만한 경사 굴곡처럼 보이는 표면에서 상체를 유지하며 보행; **6–19 s (f300–950)** 지형 패치가 시야에서 멀어진 후 지속 보행 | metadata는 **10° 상행**. 영상상 정확한 고도 상승/상단 도달 위치를 읽기 어려워 **경사 전구간 통과 거리**를 확정하지 않음. H6 camera-off의 20.426 m는 body 전진 적분이지 고도 상승량 아님. |
| `06_slope_down_10deg.mp4` | **1.0–5.0 s (f50–250)** 대응되는 완경사 질감과 보행, 큰 자세 붕괴 없음; **6–19 s (f300–950)** 지속 보행 | metadata는 **10° 하행**. 하강 후 착지 충격/수직 진동의 정량적 비교는 불가. H6 하행 `.1586` tracking·`.464` action Δ는 별도 camera-off 평가 자료. |

**명령·push 대응:** 공통으로 **6/10 s(f300/f500)** 횡이동 명령 변화 후 발을 교대로 움직이며 진행하고, **14–19 s(f700–950)** 회전 명령 구간에서 몸 방향이 변한다. 후반의 world X 화면 이동이 작더라도 횡/회전 명령이 들어가므로 정체 판정에 쓰지 않았다. `03_boxes.mp4`의 **7.70–8.48 s(f385–424)**, **15.70–16.48 s(f785–824)** 인접 표본에서 8·16초 외란 전후 **전도 없이 보행 자세가 이어지는 모습**은 확인된다. 다만 영상에서는 가해진 외란의 실제 상태 변화량·정상 궤도로 복귀한 시간을 측정할 수 없으며, H7은 별도의 다중 env camera-off run이다. **따라서 ‘밀침에도 진행을 지속함’은 지지하지만, ‘완벽하고 빠른 회복’은 미확정**이다.

**영상 공통 해석:** 추적 카메라는 로봇을 화면 비슷한 곳에 유지한다. 정체 여부는 **지면 특징이 상대적으로 이동하는지**와 명령 단계로 판단했다. 박스·요철은 실제로 화면 뒤로 사라지며, 반대로 영상 후반 14초간의 안정성이 **계속 박스·계단·거친 지면을 달린 증거는 아니다**. 화면에서는 몸통의 명백한 전도·장기간 접지 불능은 관찰되지 않았지만, 낮은 해상도/표본 간격으로 **발 끌림·미끄럼·양발 동시 체공·고주파 흔들림의 유무**를 확정하지 않는다. `02`의 50% 검정 교대는 렌더 캡처 결함이고 원본 MP4는 변경하지 않았다.

## 5. 종합 해석: 좋은 방향이지만 아직 채택을 서두를 단계는 아님

1. **목표 행동의 성취:** 좁은 이번 protocol에서는 **전진·측면/회전 명령 반응·다조건 보행 생존·push 내성에 의미 있는 성과**가 있다. 3,072회 timeout은 안정성의 강한 관찰이다. 특히 일정 전진이 실제로 기록되므로 ‘제자리 생존’ 정책은 아니다.
2. **특정 약점:** `balance`와 `lateral`에서 의도하지 않은 body 전진이 누적된다. 거친 지형은 평균에서도 어렵고 최악 cohort의 추종·진행 저하가 집중되며, **생존률 100%가 이를 드러내지 않는다.** yaw 관련 오차와 경사에서의 action 변화 비용도 있다.
3. **원인·비교 구분:** `ORIENT-100` 이름 또는 프로젝트의 orientation-penalty 완화 가설만으로 reward가 이 행동을 *개선시켰다*고 주장할 수 없다. `h1-submit-2 / TERM-50`의 같은 evaluator 원자료가 입력에 없으므로 후보 간 승자는 없다. OFFICIAL 학습 여부·학습량·계보도 ZIP이 증명하지 않는다. `official_score=false`, calibration 없음: 100점 환산 금지.
4. **판정 범위:** **HOLD**는 동작 불능 판정이 아니라 **유망한 후보를 잘못 승격시키지 않기 위한 정책 선택 판정**이다. 이번 증거만으로는 10° 경사 실질 보행과 거친 면 초반 진행은 긍정, 계단 중앙 다단 통과·정지 정밀도·고난도 일반화·기준 정책 대비 우수성은 아직 부족하다.

## 6. 다음 행동 하나 — 기존 대조 원자료를 우선 확보해 동일 조건 재집계

**권장 1순위:** 새 학습·영상·GPU 평가를 시작하기보다, **이미 보존되어 있다면 `h1-submit-2 / TERM-50`의 동일 `scenario7` H1 camera-off `episodes.jsonl` + `evaluation_manifest.json` + `resolved_configs.json`을 찾아 이번 `ORIENT-100`과 case/seed/cohort로 비교**한다. 현재 ZIP에는 그 대조군이 없으므로 여기서는 수행하지 않았다. 동일 protocol ID가 아니더라도 command/terrain/seed/num_envs/평가시간/actor/source fingerprint를 점검해 **실제로 비교 가능한 축만** 사용한다. 대응 episode ID가 아니라 `(scenario,case,seed,env_id)`로 묶고, **H1 정지 전진 drift, H3 측면 명령의 비의도 전진, H5 P05 진행·P95 tracking·stall 꼬리, H6 상/하, H7 push**를 우선 대조한다.

판정 전환 조건은 임의 합산점수가 아니라 **같은 조건에서 더 나은 rough 진행/추종 하위 꼬리가 확인되고, 정지·측면 drift와 다른 case의 생존·yaw·action 비용을 크게 희생하지 않는지**다. 해당 원자료가 존재하지 않을 때만 별도 **GPU 비교 평가가 필요한지** 판단한다(이 보고서는 실행 승인 아님). 계단은 이미 있는 영상 중 발·단차가 동시에 보이는 원본 구간을 먼저 정밀 검토하고, **유효한 반복 단차 접촉 장면 자체가 없으면** 미입증으로 남긴다.

### 재현 파일 지도와 검증

- identity/수집 상태: `source_checkpoint.txt`, `evaluation/evaluation_manifest.json`, `evaluation/video_evaluation_link.json`, `BUNDLE_README.txt`.
- 명령/지형/랜덤화: `environment.txt`, `README.txt`, `evaluation/resolved_configs.json`, `evaluation/README.txt`.
- 재계산의 원자료: `evaluation/episodes.jsonl`(3072행); 요약 대조: `evaluation/diagnostics.json`; 실행 확인: `evaluation/evaluation.log`(child exit 0).
- 화면 근거: 루트 `01_stairs.mp4` ~ `06_slope_down_10deg.mp4` 6개. 각 1,000프레임 / 50fps 확인, `02`의 홀짝 프레임 결함 별도 검토.
- **검증 결과:** ZIP CRC PASS; episode ID 중복 0; policy SHA/protocol ID 불일치 0; `forward_progress_m`와 `integrated_body_forward_m` 행별 차이 0; diagnostics scenario 수치 재현; 0 missing/0 failure/0 reset episode 확인. 입력 ZIP·원본 영상·평가 자료 **미수정**, 학습·GPU 평가·렌더·export·게시 **미실행**.
