# H1 `model_4650` 6영상·평가 원자료 심층 분석

**분석일:** 2026-10-11 (KST)  
**범위:** 사용자 제공 `model_4650_h1_6terrain_evaluation_20261011-030854_89b4c4a0.zip` 단일 정책, 6 MP4 및 Windows PERSONAL camera-off `scenario7` 평가. 프로젝트의 과거 `ACTRATE-0001/model_2700` 수치는 **독립적으로 재계산하지 않은 역사적 참고값**으로만 대조한다.

## 1. 결론 — **HOLD (전진·안정 보행은 성공, 범용 대표 후보 승격은 보류)**

**목표 행동 수행 여부:** 전진, 10° 상·하 경사 평가, 거친 지형의 지속 진행, 지정된 밀침 환경의 *비낙상·재진행*은 유용하게 수행한다. 단순히 서 있기만 한 정책이 아니다. camera-off 평가 3,072개 전부가 20초 `timeout`이며, H2 전진 명령 적분 15m 대비 **실제 body-frame 진행 평균 14.812m**, H7 밀침 환경에서 10m 대비 **9.757m**, H5 rough에서 10m 대비 **9.546m**다. 영상의 장애물 구간에서도 발을 교대로 내딛고 쓰러지지 않은 채 전진하는 장면이 보인다.

**승격을 막는 trade-off:** H1 제자리 명령의 world XY 순변위는 **0.228m/20초**로 비교적 작지만, H3에서 좌·우 횡이동 명령의 적분 합이 0임에도 **world XY 잔류 순변위 평균 2.398m**다. H4 회전의 yaw 절대오차 평균 **0.179rad/s**이고, H5 rough에는 진행 하위 꼬리(최소 **8.974m**)와 높은 혼합 추종오차 사례(최대 **0.282**)가 있다. 특히 과거 `ACTRATE-0001/model_2700` **보고서의 참고값**과 나란히 놓으면 H1/H3의 불필요한 body 전진은 크게 줄어든 반면, rough 진행·전체 혼합 tracking·자세 및 action-change 비용은 불리해지는 양상이다. 이것을 LINTRACK 보상 변경의 인과 효과로 단정할 수는 없다.

**결정:** 전진·밀침 후 이동을 관찰할 *내부 후보로 보존*하되, **범용 대표/최종 활용 정책으로 바로 PROMOTE하지 않는다.** 계단 중앙 다단 통과와 횡이동 왕복의 위치 복귀까지 성공했다고 주장할 자료가 없다. REJECT할 정도의 전반적 보행 실패도 아니다. 이 상태는 정책 행동 후보 판단이지 학습 완료·제출·공식 채점 판정이 아니다.

## 2. 정책 identity, 평가 범위, 검증 상태

- **표시명:** `H1-4650`; ZIP 안 checkpoint 경로의 파일명은 `model_4650.pt`. **정책 SHA-256** `ce7ad58657f3dd744e7cf2b7531f3d7d455773dfc6fb135f39d8a55aa49dea70` (ZIP 메타데이터 기록). `source_checkpoint.txt`, `evaluation_manifest.json`, `video_evaluation_link.json`, `BUNDLE_README.txt`의 SHA가 일치한다. 원 `.pt` 바이트는 ZIP에 없어 **체크포인트 자체의 SHA를 재계산한 것은 아니다.** MP4 6개의 SHA256SUMS 일치와 ZIP CRC 검사는 통과했다.
- **학습 identity 경계:** `preset=null`, `source_run_id=null`. checkpoint 입력 경로에는 `...h1-actrate0001-lintrack065-from2700-plus2k...`가 기재되어 있어 후보 계보에 관한 **경로상 단서**는 있으나, 원본 학습 evidence·부모 checkpoint SHA·resolved reward 값·실제 iteration 로그는 이 ZIP에 없다. 따라서 `LINTRACK-065`의 verified Run, 변경된 reward, 2700 부모 상속 및 `4650`의 학습량을 확정하지 않는다.
- **평가 완료:** `complete=true`, `execution_status=COMPLETE`, `smoke=false`, 자식 프로세스 `exit=0`; 로그에서 fatal/traceback 미발견. PERSONAL Windows RTX 3060 Laptop GPU, deterministic inference, Isaac Sim `5.1.0-rc.19...`, Isaac Lab `3e73d6d...`, task checkout `ef10b7a...`. `official_score=false`, `raw_diagnostics_only=true`.
- **프로토콜:** `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34`; H1 `scenario7`, **7 scenario / 8 case**, 평가 seed **4201·4202·4203**, seed별 **128 env/case**, case별 **384 cohort**, 총 **3,072 최초 cohort / 3,072 episode**, 각 **1,000 step × 0.02s = 20초**. episode ID 중복·누락값·종료 후 재시작 episode 없음. 모든 episode는 `timeout`, `survived=true`, `base_contact_failure=false`. 고정 시간창 내 한 번 이상 `terminated`된 cohort도 **0/3,072**다.
- **실제 평가 조건:** `resolved_configs.json`에서 observation corruption 비활성, mass/physics randomization 이벤트 비활성, reset 시 시작 위치·방향은 랜덤 범위(위치 ±0.5m, yaw ±3.14rad), terrain difficulty=0.5. H5 random rough, H6 slope 상·하를 각각 별도 case로 취급한다. H1–H4·H7은 flat; H7에는 정해진 횡방향 속도 외란이 있다. 10초마다 명령을 바꾸는 episode 시계다. 여섯 MP4는 반대로 **seed42·1 env·고정 초기 pose·20초 전역 영상 시계·별도 지형·외란**으로 촬영한 정성 자료여서 동일 episode가 아니다.

**지표·집계 규칙:** 아래 표는 `evaluation/episodes.jsonl`에서 직접 계산한 **case별 episode 행 평균(각 case 384행)**이다. `diagnostics.json`의 scenario별 혼합 tracking 평균 및 생존률과 대조 일치한다. `mean_tracking_error`는 step별 `sqrt(Δvx²+Δvy²+Δyaw_rate²)`의 episode 평균을 다시 단순 평균한 **혼합 내부 수치(단일 물리 단위 없음)**; `vx_error`, `vy_error`는 m/s, `yaw_error`는 rad/s의 평균 절대오차다. `forward_progress_m`와 `integrated_body_forward_m`는 동일한 **body-frame vx 적분**으로 독립 근거가 아니다. `world XY 순변위`는 `sqrt(world_dx_m² + world_dy_m²)`를 **episode마다 계산하여 평균**했다. `lateral_drift_m`는 실제 world 횡변위가 아니라 `|Δvy|`의 시간적분이다. `stall_fraction`은 명령 XY≥0.2m/s일 때 실제 XY속도<0.1m/s인 step의 비율이므로 **정지 H1의 stall=0은 제자리 유지 성공 신호가 아니다.**

## 3. 핵심 정량 결과: 진행, 명령 추종, 자세 비용

| case (20초 명령) | tracking 혼합↓ | `vx / vy / yaw` 평균 절대오차↓ | body 진행 평균 m (P05) | stall 평균 | roll/pitch RMS | action Δ RMS |
|---|---:|---:|---:|---:|---:|---:|
| **H1** 정지 `(0,0,0)` | 0.13608 | .016 / .051 / .109 | **+0.108** (0.101) | 0.0000* | .07228 | .42987 |
| **H2** 전진 `0.5→1.0` | 0.16205 | .025 / .054 / .136 | **14.812** (14.788) | .00600 | .06544 | .46470 |
| **H3** 횡왕복 `vy +.3→−.3` | 0.13885 | .014 / .057 / .112 | **−0.044** (−0.053) | .00938 | .07256 | .46186 |
| **H4** 회전 `vx=.5, yaw ±.5` | **0.19634** | .019 / .056 / **.179** | 9.842 (9.834) | .00500 | .06810 | .43211 |
| **H5** rough `vx=.5` | 0.18466 | **.051** / .050 / .152 | **9.546** (9.228) | .00685 | .06293 | .51814 |
| **H6** 경사 상행 `vx=1` | 0.19034 | .045 / .053 / .160 | **19.872** (19.707) | .00500 | .07099 | .54202 |
| **H6** 경사 하행 `vx=1` | 0.19368 | .048 / .054 / .161 | **19.633** (19.446) | .00500 | .06497 | **.55849** |
| **H7** push `vx=.5` | 0.16183 | .032 / .057 / .129 | **9.757** (9.691) | .00626 | .06699 | .45007 |

*H1은 유효한 nonzero-speed 명령 step이 없어 정의상 0. yaw 단위는 rad/s, 직선 속도 오차는 m/s이며 자세 RMS는 기록된 각도 지표, action Δ RMS는 평가기 내부 action 차이 크기다. 진행 P05는 episode별 body 적분의 하위 5백분위수. 전 case episode 동일가중 전체 혼합 tracking은 **0.17048**, `xy_rmse` **0.09256m/s**, `yaw_rmse` **0.17765rad/s**, roll/pitch RMS **0.06803**, action Δ RMS **0.48216**. 이는 H6 상·하를 각각 384행으로 계산한 **8 case 동일가중 평균**이지 7 scenario 동일가중치나 공식 점수가 아니다.

### 실제 행동을 가르는 네 가지 발견

**① 전진과 밀침은 생존 이상이다.** H2 실제 body 진행 **14.812/명령 적분 15m**, H7 **9.757/10m**이며 각각 최소 episode **14.773m**, **9.675m**이다. H7은 push 후 전체 20초 동안 진행을 유지하고 종료 없이 마친다는 증거다. 하지만 이 숫자에는 외란 직후 속도 회복시간·최대 자세 이탈이 없으므로 *밀침마다 즉각 완전 회복*했다는 뜻은 아니다. H6 상·하도 평균 **19.872/19.633m**(명령 적분 20m)로 진행은 견고하다. 다만 body 적분을 물리 지형의 완주 거리로 바꾸지 않는다.

**② 정지는 개선 여지가 작아졌지만 횡이동 목표 복귀는 핵심 결함이다.** H1 평균 body 비의도 진행은 **0.108m**, world XY 순변위 **0.228m**(P95 **0.233m**)이다. H3는 body의 불필요한 전진 적분이 **−0.044m**로 작고 vy 절대오차 평균이 **0.057m/s**인데도, 양·음 횡속도 명령 10초씩 후 **world XY 순변위 평균 2.398m**(P05 **2.377m**, P95 **2.418m**)가 남는다. 이는 지속적으로 서 있고 속도를 따라가는 것과 **원래 위치로 돌아오는 것**이 다르다는 직접적인 반례다. `lateral_drift_m=1.142m`를 실제 2.398m의 대체 측정값으로 쓰지 않았다. 명령 회전이 0이라도 yaw 추종 오차·body/world 프레임 변환의 영향이 있을 수 있으나, step별 궤적이 없어 기전을 확정하지 않는다.

**③ H4 회전이 전체 tracking의 약점이다.** H4의 혼합 tracking **0.19634**가 8 case 중 가장 크고, `yaw_error=0.17906rad/s`도 가장 크다. 반면 `vx_error=0.01921m/s`로 선속도 추종은 작게 어긋난다. **XY가 아니라 yaw-rate 비용이 지배적**인 회전 trade-off다. H4의 world 순변위가 평균 **4.719m**인 것은 회전하며 곡선 이동하는 명령 특성상 stall 증거가 아니다(body-frame 전진은 **9.842m**, stall **0.005**).

**④ H5 rough는 정체하지 않지만 상단 추종오차와 하단 진행거리의 꼬리가 있다.** 진행 **평균 9.546 / P05 9.228 / 최소 8.974m**(명령 적분 10m). tracking **평균 .18466 / P95 .20873 / 최대 .28193**. 384회 중 **142회**가 9.5m 미만 진행(9.5m는 서술용 참고점이며 합격 기준 아님); 대신 **stall>0.05인 episode는 0회**, 최악 stall도 **0.022**이므로 '멈춘다'보다 **속도·방향·지형 때문에 진행과 추종 품질이 출렁인다**가 정확하다. 가장 느린 `H5-rough-s4202-e101-n0`는 **8.974m**, tracking **.24711**, world XY 순변위 **7.706m**. 반면 가장 큰 tracking 오차 `H5-rough-s4201-e81-n0`는 **.28193**이지만 진행 **9.776m**: 최악 추종과 최악 전진이 반드시 같은 episode가 아님을 보여 준다. 시드별 rough 진행 평균 **4201: 9.533 / 4202: 9.557 / 4203: 9.548m**, tracking **.18672 / .18383 / .18342**다. 이는 평가 seed 간 기술통계일 뿐 학습 seed 반복의 통계적 유의성을 뜻하지 않는다.

### 역사적 후보와의 *간접* 참고 대조 — 정식 matched A/B 아님

프로젝트 문서 `14_H1_NEXT_RUN_PARAMETER_COMPARISON.md`와 `00_START_HERE_CONTEXT_AND_MAP.md`에 과거 `ACTRATE-0001/model_2700` PERSONAL 같은 protocol 계열의 **원자료 분석 결과로 기록된 값**이 있다. 이번 입력에는 그 평가 ZIP이 없어 그 행을 재계산하거나 `resolved_configs.json`·전 cohort를 **직접 동일성 검증하지 않았다.** 아래 왼쪽은 문서 기록, 오른쪽은 **이번 ZIP 직접 계산**이다. 현 파일명 및 Windows 경로만으로 실제 부모–자식 관계나 reward 단일변경을 증명하지 않는다.

| 축 | 과거 기록 `ACTRATE-0001 / model_2700` | 이번 `H1-4650` | 참고상 방향 |
|---|---:|---:|---|
| H1 명령 0의 비의도 **body 전진 적분** m | +1.987 | **+0.108** | 정지 누수 감소 |
| H3 횡왕복의 비의도 **body 전진 적분** m | +1.677 | **−0.044** | 전후방 누수 감소; 위치 복귀 2.398m는 별개 |
| H5 rough 진행 평균 / P05 m | **9.948 / 9.592** | 9.546 / 9.228 | 거친 지형 전진·하위 꼬리 후퇴 |
| H2 전진 / H7 push 진행 m | **15.326 / 10.542** | 14.812 / 9.757 | 전진량 감소 |
| 전체 혼합 tracking↓ | **.14534** | .17048 | 추종 혼합치 악화 |
| 전체 roll/pitch RMS↓ / action Δ RMS↓ | **.03019 / .45687** | .06803 / .48216 | 자세·행동변화 비용 증가 |

참고 대조에서 핵심은 *정지/전후방 누수 개선과 전진·추종·자세 비용 악화가 동시 발생할 수 있다*는 방향 신호다. 시각 검증용 자료도 평가 command도 각각 다르며, parent SHA/학습 source/PPO/reward 실제 override/seed와 동일 지형 초기조건 및 대응 raw를 검증하지 않은 상태에서 **`track_lin_vel_xy_exp` 변경의 인과 개선/악화**나 범용 정책 우위를 확정하지 않는다.

## 4. 6개 MP4 직접 프레임 검사: 장애물 접촉·진행·회복

검사 방법: ZIP의 여섯 MP4를 각각 **1,000프레임·50fps·20초** 디코딩하고, 전 시간대 초별 프레임과 초기 장애물 구간의 0.5초 간격 프레임을 확대 확인했다. 아래는 **실제로 확인한 프레임·행동**이며 영상으로 속도·거리·foot sliding을 정밀 측정한 것은 아니다. 여섯 영상 모두 **0번 프레임이 검정이고 1번부터 가시**; 이번 ZIP에는 알려진 다른 후보의 '홀짝 500개 교대 검정' 결함이 없다(샘플이 아니라 전체 프레임 평균 밝기로 확인). 이 초기 1프레임은 **캡처 artifact**이지 낙상이나 동작 실패가 아니다.

영상 공통 `environment.txt` 명령: **0–6초** `vx=1`, **6–10초** `vx=.5,vy=+.3`, **10–14초** `vx=.5,vy=−.3`, **14–17초** `vx=.5,yaw=+.5`, **17–20초** `vx=.5,yaw=−.5`. 모든 영상의 **4·8·12·16초**에 world-Y 방향 속도 변화 ±0.5m/s의 push가 예정돼 있다. 이는 H3 camera-off의 `vx=0` 순수 lateral 테스트와 다르므로 **영상 후반 횡·회전을 순수 lateral 평가로 해석하면 안 된다**. 카메라는 로봇을 추적하므로 화면 가운데에 있다는 사실은 정체 증거가 아니다.

| 파일·확인 구간 | 관찰된 실제 행동과 허용되는 판단 |
|---|---|
| `01_stairs.mp4` **#75–200 (1.5–4.0초)**, **#250 (5초)** | 계단 줄무늬가 발 주변으로 접근·지나가고 로봇은 길게 다리를 교대로 디디며 계속 직립한다. 계단 **가장자리와 인접한 진행**이 주로 보이고, 여러 단을 정중앙으로 연속 승강했다는 명확한 장면은 없다. 이후 **#300–950**은 대부분 평지 보행. *계단 중앙 완주 미입증*. |
| `02_inverted_stairs.mp4` **#20–200 (0.4–4초)**, **#250–400** | 검은 단차 면을 **옆에 두고** 진행하는 장면이 두드러진다. 몸통이 서 있고 발의 교대 이동이 보이지만, 발이 다단 단차 중앙을 차례로 통과한다는 근거는 부족하다. **#400 이후** 평지 위주. *실패 낙상도, 다단 완주도 관찰되지 않음*. |
| `03_boxes.mp4` **#20–200 (0.4–4초)**, **#300–700 (6–14초)**, **#800–900 (16–18초)** | 로봇 주변에 높이가 다른 블록과 좁은 간극이 지속적으로 보이며, 다리를 번갈아 뻗어 **블록 지형 안팎으로 위치를 바꾸며 직립 보행**한다. **#800–900** 무렵 블록 패치가 뒤로 멀어지며 평지로 이행한다. 고속 foot-sole 접촉이나 슬립은 화면 해상도·카메라만으로 정량화 불가. 평가 `scenario7`에는 boxes case가 없어 **boxes의 다환경 완료율은 없음**. |
| `04_random_rough.mp4` **#20–200 (0.4–4초)**, **#250–400** | 좁고 울퉁불퉁한 패치 위에서 직립하며 보폭을 이어 간다. **#200–300** 경계부를 지나 패치가 뒤로 남고, **#400 이후** 주로 평지다. 이는 rough 위에서 일부 실진행이 있다는 긍정 신호이고, camera-off H5 평균 진행 9.546m와 방향상 양립한다. 그러나 **영상 20초 전체를 rough에서 통과한 것**은 아니다. |
| `05_slope_up_10deg.mp4` **#20–200 (0.4–4초)**, **#300–500** | 초기에 완만한 격자/높이 형상의 경사 주변에서 보행하고, 이후 무늬가 멀어지며 평지 유사 표면을 계속 이동한다. 넘어짐·완전 정지 장면은 없음. 영상만으로 경사면 위 실제 높이 변화량이나 10° 구간 완주 거리를 측정하지 않음. camera-off **H6 상행 body 진행 19.872m**가 별도 수치 근거. |
| `06_slope_down_10deg.mp4` **#20–200 (0.4–4초)**, **#300–500** | 하행 지형 초기 패턴을 지나 자세를 유지하며 교대 보행한다. **#500–950**는 평지 유사 영역에서 횡이동·yaw 포함 명령을 수행하며 직립. 정량 H6 **하행 body 진행 19.633m**와 양립하지만, 영상으로 내리막 높이/속도·회복시간을 측정할 수 없음. |

**push와 보행 질의 해석:** 여섯 영상에서 예정된 push 시점 **#200/#400/#600/#800 전후**에 로봇이 장시간 쓰러져 있거나 계속 누워 있는 장면은 없고, 전후 프레임에서 교대 보행을 이어 간다. 따라서 **유한 외란 뒤 넘어지지 않고 이동을 지속하는 정성 근거**는 있다. 다만 push 반응 지연·최대 roll/pitch·발 접지 지속시간은 이 영상 관찰만으로 수치화하지 않는다. 일부 프레임에서 보폭이 길고 몸통 방향이 변하는 것은 관찰되지만, 지속적 발끌림·sliding/hopping의 빈도나 회복 시간을 단정할 고해상도 접촉 시계열이 없다. 이 항목의 계량치도 `episodes.jsonl`에 없다.

## 5. 종합 판단 및 다음 행동 **한 가지**

**확인된 강점:** (a) 테스트된 8 case에서 종료 후 reset 없이 20초를 지속, (b) 명령을 바꾼 전진·회전 상황에서도 실질적인 body-frame 이동, (c) rough 하위 진행 사례도 8.974m까지는 계속 이동하고 큰 stall 집중 없음, (d) 10° 상·하행과 4회 밀침이 포함된 각기 다른 평가/영상 조건에서 낙상 없는 이동 근거. **치명적 채택 약점:** (a) 순수 H3 왕복 lateral 종료 뒤 2.398m world 위치 오차, (b) H4 yaw 추종오차, (c) rough 추종 하위 꼬리와 (역사 참고상) 감소한 진행, (d) action-change 및 자세 비용. 여섯 영상은 **stairs/boxes의 정량 시나리오 평가를 대체하지 않는다**.

**권고: `HOLD` 유지, H1-4650의 활용 범위는 '전진·경사·push 보행 대체 후보'로 한정.** 단순 생존을 넘어선 유용성은 확인됐지만, 횡왕복 종료 위치 유지가 중요한 범용 이동 제어에 대표 후보로 채택하기에는 부족하다.

**다음 행동(기존 자료만 활용):** 프로젝트에 보존됐다고 기록된 `ACTRATE-0001/model_2700`의 **기존 Windows 평가 원본 ZIP**을 이번 `H1-4650` ZIP과 함께 CPU에서 **cohort `(scenario,case,seed,env_id)` 대응 재집계**한다. 재실행 전에 두 ZIP의 robot, `protocol_id`, `resolved_configs.json`, agent/source/applied-environment fingerprint, seed, noise, 명령, 지형·난이도, 시간창 및 최초 episode 여부를 확인하고, 서로 같을 때 H1 body/world 이동, H3 world 잔여 이동·`vy_error`·종료, H4 yaw, H5 mean/P05/P95·최악·stall, H6 action/자세, H7 진행의 대응 분포를 비교한다. **그 결과 전후방 누수 감소가 H3 위치 복귀에도 연결되고 rough/yaw/action 비용이 받아들일 만한지**를 판단해 PROMOTE/HOLD를 갱신한다. source parity가 충족돼도 동일 물리 terrain/학습 단일변수 인과가 자동 입증되지는 않는다. 새 학습, GPU 평가, 재렌더, export, 서버 조작은 이 보고서에서 수행하거나 요구하지 않는다.

### 재확인 가능한 원본 위치·검증 메모

- **이번 ZIP:** `source_checkpoint.txt`(체크포인트 이름/SHA), `environment.txt`(6 MP4의 지형·command·push·seed), `README.txt`(영상 계약), `SHA256SUMS.txt`(MP4 6개 일치), `evaluation/video_evaluation_link.json`(영상–평가 SHA 연결), `evaluation/evaluation_manifest.json`(로봇·프로토콜·완료 상태·source fingerprint), `evaluation/resolved_configs.json`(case별 설정), `evaluation/episodes.jsonl`(**3,072행 직접 재계산**), `evaluation/diagnostics.json`(**시나리오 평균 교차확인**), `evaluation/evaluation.log`(complete/child exit 0), 루트 6개 MP4(각 위 시각/프레임).
- **간접 역사 참고:** 프로젝트 첨부 `14_H1_NEXT_RUN_PARAMETER_COMPARISON.md`의 **2026-10-10 ACTRATE-0001 원자료 비교 기록** 및 `00_START_HERE_CONTEXT_AND_MAP.md`의 model_2700 행동 요약. 기존 2700 ZIP 실물은 이번 요청의 업로드 목록에 없으므로 *그 정책의 원자료를 직접 재열람했다고 표기하지 않았다*.
- **검증 결과:** ZIP CRC 정상, 지정된 6 MP4 각각 checksum 일치, 6 MP4 × 1,000프레임 디코딩 가능, 검정 프레임은 각 첫 프레임만, 3,072 unique cohort=3,072 unique episode ID, 누락 필드 0, `forward_progress_m == integrated_body_forward_m` 전 행, 모든 `timeout`과 `base_contact_failure=false`, diagnostics tracking·survival과 원자료 재집계 일치. 외부 공개·원본 변경 없음.
