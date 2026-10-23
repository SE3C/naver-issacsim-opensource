# H1 `LINTRACK-075` corrected5k / `model_4997` — 6지형 영상·평가 원자료 통합 분석

- **작성일:** 2026-10-10 (KST)
- **분석 입력:** `h1_LINTRACK-075_corrected5k_model_4997_h1_6terrain_evaluation_20261009-235216_59e47db4.zip` 한 개. 내부 18개 항목(6 MP4 + 메타데이터/평가 12개)을 열어 조사했다. 비교 정책 ZIP은 제공되지 않았다.
- **결론의 범위:** H1 정책 하나에 대한 **Windows PERSONAL 고정 평가와 정성 영상 판정**이다. 공식 NCRC 채점, 제출 성공, reward 효과, 학습 완료 여부를 판정한 문서가 아니다.

## 1. 결론과 후보 판정

**정책 후보: HOLD — 기능하는 보행 정책이지만, 범용 험지·계단 정책으로 바로 채택하지 않는다.**

이 정책은 단순히 넘어지지 않고 시간을 버틴 것이 아니다. 평가 원자료에서 전진 H2는 명령 적분 15.0 m에 대해 실제 **body-frame 전진 15.015 m**, 외란 H7은 명령 10.0 m에 대해 **10.038 m**, 상·하 경사 H6은 각각 **19.943/19.776 m**를 기록했다. H2의 월드 **순변위 크기도 14.854 m**이며, 3,072개 episode는 모두 20초 동안 base-contact 종료 없이 생존했다. 고정 영상에서도 boxes의 블록 사이 이동과 random rough 초반의 거친 접지 후 이동이 확인된다. **평지 전진·정해진 경사·push 상황에서 계속 이동하는 능력은 확인된 강점**이다.

그러나 이것이 **6지형 전부의 장애물 완주**를 뜻하지는 않는다. 계단 영상은 다단 중앙 통과를 보여주지 않고, 별도 camera-off 평가 8개 case에도 stairs/boxes case는 없다. 더 중요하게는 rough H5에 **20초 생존하지만 전진 2.871 m, stall 0.664**인 cohort가 있다. 이 실패는 평균 survival 100%와 평균 stall 0.0076만 보면 놓친다. 또한 정지 H1의 20초 월드 순변위는 평균 **0.516 m**, 좌우 명령 H3의 왕복 종료 순변위는 평균 **1.280 m**로 위치 유지·역방향 전환도 완전하지 않다. slope의 tracking 오차는 특히 yaw 축에서 커지고, action 변화와 몸통 기울기 RMS도 커진다.

**따라서:** 평지·정해진 경사·외란 하 보행의 *유효한 내부 후보*로 유지한다. 그러나 **계단 검증 미비, rough 하위 꼬리, 정지·횡이동 잔류 이동**이 있어 전지형 대표 후보의 **PROMOTE는 보류**한다. 다른 정책 대비 우위는 이 한 ZIP으로 주장하지 않는다. 이는 행동 후보 판정이지 실제 `LINTRACK-075` 보상 변경의 인과 판정이 아니다.

## 2. 정책 identity·평가 계약

| 항목 | ZIP에서 직접 확인한 값 |
|---|---|
| 표시명 | **H1 `LINTRACK-075` corrected5k / `model_4997`** — 입력 파일명 기반의 표시명, Run ID 아님 |
| checkpoint SHA-256 | `4349fe5650135c6a77546afc1b165ff60c235bdd83831bd562d618b04c3b5b6d` |
| 연결 근거 | `source_checkpoint.txt`, `BUNDLE_README.txt`, `evaluation/video_evaluation_link.json`, 평가 manifest의 `policy.sha256`가 동일 SHA를 기록 |
| 로봇·파일 형식 | `h1`, `Humanoid-v0`, `rsl_rl_checkpoint`; native `.pt` 원본은 ZIP에 없음 |
| 평가 상태 | `execution_status=COMPLETE`, `complete=true`, `smoke=false`; `evaluation.log`의 `[CHILD EXIT] 0`, 치명적 예외 없음 |
| 출처 | `evaluation_environment=PERSONAL`, `official_score=false`, `raw_diagnostics_only=true` |
| 평가 protocol ID | `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34` |
| 평가 구조 | `scenario7`: **7 scenario / 8 case × 3 seeds(4201/4202/4203) × 128 env = 3,072 cohort**, 각 20 s(1,000 step) |
| 종료·실패 | 3,072/3,072 `timeout`/`survived=true`; `terminated` 0; `base_contact_failure=false` 3,072건; `duration_s=20` 전체 |
| 평가 조건 | deterministic actor, camera-off, episode-clock 명령(10초 전환), observation corruption off, terrain curriculum off, 10×20 지형 생성기(험지·경사) |
| 평가 소스 | `source_fingerprints`에 H1 task 3개와 `humanoid_rewards.py` digest 저장; agent fingerprint·각 case/seed의 effective config fingerprint 기록 |
| 영상 조건 | 6×20 s, 50 fps/1,000 decoded frames; seed 42, env 1, 1×1 tile, 초기 XY/yaw=0, observation noise off, added base mass=0 |
| 계보 | `policy.source_run_id=null`, `policy.preset=null` — **training Run/부모/fresh·resume/OFFICIAL 학습 여부는 이 ZIP만으로 미확인** |

**Identity 검사 수준:** 연결된 메타데이터의 정책 SHA가 일치하는 것은 확인했다. ZIP에 원래 checkpoint bytes가 없어 그 `.pt`의 SHA를 직접 다시 계산할 수는 없다. `video_evaluation_link.json`의 source checkpoint와 staged checkpoint도 기록상 연결이며, Windows 현지 경로에 접속해 재검증한 것은 아니다.

**중요한 provenance 함정:** `evaluation/resolved_configs.json`과 `evaluation.log`의 평가 환경에는 `track_lin_vel_xy_exp=0.5`, `termination_penalty=-5` 등의 **evaluator 측 reward 기본값**이 남아 있다. 이는 **checkpoint 이름의 `LINTRACK-075`와 다르지만 추론 시 사용한 학습 reward가 `0.5`였다는 증거가 아니다.** evaluator 환경을 구성한 값과 policy를 학습한 resolved reward·lineage를 혼동해서는 안 된다. 마찬가지로 평가 agent 설정의 `max_iterations=5000`, `resume=false`, `seed=42`를 실제 학습 내역으로 읽지 않는다.

**비교 조건 차이:** 영상은 전역 명령 0–6 s `[vx,vy,yaw]=[1,0,0]`, 6–10 s `[0.5,0.3,0]`, 10–14 s `[0.5,-0.3,0]`, 14–17 s `[0.5,0,+0.5]`, 17–20 s `[0.5,0,-0.5]`이며, 4/8/12/16 s에 world-Y 속도 ±0.5 m/s를 가하는 영상용 일정이다. camera-off 평가는 case별 전혀 다른 명령, 무작위 초기 XY/yaw, episode-local 명령 clock, 다중 지형 타일을 이용한다. 영상과 평가의 20초는 **같은 trajectory나 동일 조건 반복 측정이 아니다**. `scenario7` H7 push 또한 별도 평지 실험이다. 두 소스는 동일 checkpoint와 문제 유형의 *교차 관찰*로만 연결한다.

## 3. episode 원자료 재집계 — 성공과 실패를 함께 보기

아래 표는 **`evaluation/episodes.jsonl`의 모든 3,072개 행을 직접 집계**했다. 각 case는 384개 episode이며, 생존률은 전부 100%여서 반복 표기하지 않는다. 같은 방식으로 시나리오별 `mean_tracking_error`를 다시 계산했을 때 `evaluation/diagnostics.json`의 값과 일치했다. 아래 `world |Δ|`는 원자료에서 **각 episode마다** `sqrt(world_dx_m² + world_dy_m²)`를 구해 평균한 보조값이다. 서로 다른 초기 yaw 때문에 signed `world_dx_m`·`world_dy_m`를 먼저 평균하면 실제 진행을 심하게 과소평가한다.

| Case (20초 명령) | Tracking† ↓ | vx / yaw 절대오차‡ ↓ | Body 전진 m | World 순변위 크기 m | Stall | Roll/Pitch RMS | Action Δ RMS |
|---|---:|---:|---:|---:|---:|---:|---:|
| H1 정지 `[0,0,0]` | 0.1351 | 0.0216 / 0.1127 | **+0.415** | **0.516** | 0.0000§ | 0.0206 | 0.3405 |
| H2 전진 `0.5→1.0` | 0.2343 | 0.0282 / 0.2191 | **15.015** | **14.854** | 0.0040 | 0.0430 | 0.4177 |
| H3 횡이동 `+0.3→−0.3` | 0.1357 | 0.0250 / 0.1041 | **+0.480** | **1.280** | 0.0100 | 0.0302 | 0.3422 |
| H4 전진+회전 `yaw +0.5→−0.5` | 0.2186 | 0.0207 / 0.2012 | **10.112** | **4.770** | 0.0040 | 0.0335 | 0.3652 |
| H5 rough, `vx=0.5` | **0.2470** | 0.0619 / 0.2167 | **9.089** | **8.552** | **0.0076** | 0.0436 | 0.3963 |
| H6 경사 상행 10°, `vx=1` | 0.2765 | 0.0425 / **0.2573** | **19.943** | **19.899** | 0.0050 | **0.0537** | **0.4958** |
| H6 경사 하행 10°, `vx=1` | **0.2806** | 0.0415 / **0.2613** | **19.776** | **19.743** | 0.0050 | 0.0514 | **0.5098** |
| H7 평지 push, `vx=0.5` | 0.2104 | 0.0298 / 0.1897 | **10.038** | **9.810** | 0.0040 | 0.0368 | 0.3672 |

† `mean_tracking_error`: 각 step의 `sqrt(Δvx²+Δvy²+Δyaw_rate²)`를 episode 안에서 평균한 뒤 episode별 동일 가중 평균. **m/s 등의 한 단위를 붙일 수 없는 혼합 내부 지표.**  
‡ `vx_error`는 m/s, `yaw_error`는 rad/s의 step별 **절대**오차 평균. 서로 다른 단위이며 `xy_rmse`·`yaw_rmse`와 같지 않다. H5의 `vy_error=0.0470 m/s`, `xy_rmse=0.1079 m/s`, `yaw_rmse=0.2617 rad/s`; H6 하행의 `xy_rmse=0.1181 m/s`, `yaw_rmse=0.2941 rad/s`도 원자료에서 확인했다.  
§ H1은 명령 XY 크기가 0이어서 stall 유효 분모가 없다. 기록된 0은 **제자리 균형 성공 지표가 아니다**.  
`Body 전진`은 `forward_progress_m` = `integrated_body_forward_m`로, 한 근거의 중복 필드다. `lateral_drift_m`는 위치 횡변위가 아니라 `|Δvy|`의 적분이므로 월드 이동량으로 재해석하지 않았다. foot sliding, foot air time, 관절 deviation 정량 원자료는 이 ZIP에 없다.

**전체 가중:** episode 균등 가중 tracking 평균은 **0.21727**(H6 상/하 768행이 포함되어 H6의 비중 25%). 7개 scenario를 다시 동일 가중으로 평균하면 **0.20852**이지만 이는 별도 보조 집계일 뿐 점수·개선율이 아니다. case별 모든 행 수가 384여서 *8-case 동일가중*은 episode 평균과 같다. 모두 20초 생존해 여기서는 짧은 실패 episode 과대표집은 없지만, 향후 실패가 생기면 집계의 성질은 달라진다.

### 가장 중요한 세 가지 발견

**(1) 속도 진행은 실제지만 정지·횡방향의 위치 오차가 남는다.** H2의 15.015 m는 명령 적분 15.0 m와 근접하고, 매 episode의 world 순변위도 평균 14.854 m(최소값이나 평균 signed X가 아님)이다. H6에서도 body 적분과 순변위 크기가 근접해 직진성에 대한 긍정적 신호를 준다. 반면 H1은 정지 명령에 world displacement 0.516 m, H3은 좌우 10초씩 상쇄하는 명령 뒤 1.280 m가 남는다. H3 body 전진도 +0.480 m이다. 따라서 **명령에 반응하여 걷는 능력**과 **정지 유지/횡이동 후 원위치 복귀 정확도**는 분리해야 한다. H4의 world 순변위 4.770 m는 회전 명령이 있으므로 body 전진 10.112 m와 다르다고 stall로 단정하지 않는다.

**(2) 핵심 위험은 rough의 소수 정체 cohort — 낙상으로는 드러나지 않는다.** H5 384 episode의 body 전진은 **중앙값 9.109 m, P05 8.670 m, 최소 2.871 m**이고 tracking은 **중앙값 0.2461, P95 0.2675, 최대 0.4483**이다. 명령은 20초 내내 body `vx=0.5 m/s`(적분 목표 10 m)이다. 최악의 **`(H5, rough, seed 4202, env_id 41)`**은 `forward_progress_m=2.8708`, world 순변위 `2.9470`, tracking `0.4483`, `vx_error=0.3677 m/s`, `stall_fraction=0.664`, `roll_pitch_rms=0.0967`이면서 `duration_s=20`, `end_reason=timeout`, `base_contact_failure=false`다. **stall >0.05인 것은 384개 중 단 1개**, `stall >0.02`는 3개다. 즉 전반이 정체됐다는 뜻이 아니라 **특정 환경에서 심각한 기능 실패 꼬리**가 존재한다. 3개 seed 평균 tracking/전진/평균 stall은 각각 아래와 같다.

| H5 seed (각 128 cohort) | Tracking | Body 전진 m | Stall |
|---|---:|---:|---:|
| 4201 | 0.2461 | 9.110 | 0.0060 |
| 4202 | 0.2476 | 9.076 | **0.0110** |
| 4203 | 0.2472 | 9.081 | 0.0059 |

seed별 평균은 비슷하지만 **4202의 단일 하위 사례가 위험을 집중**시킨다. seed 3개는 독립 학습 seed가 아니라 서로 다른 **평가 seed**이고, 384 env를 384개 독립 학습 시도로 계산하지 않았다. `episode_id` 중복 0, 누락 필드 0, 3,072 distinct cohort 전부 episode 1회(n0)라서 reset·재종료에 의한 episode 가중 왜곡은 **이번 자료에서는 발생하지 않았다**. 20초 고정 시간창 내 `terminated` 발생 cohort 비율도 **0/3,072**이다.

**(3) yaw 추종과 동작 비용에서 trade-off가 크다.** H2/H5/H6 하행의 yaw 평균 절대오차는 각각 **0.2191/0.2167/0.2613 rad/s**, vx 오차는 **0.0282/0.0619/0.0415 m/s**다. 통합 tracking이 H6에서 나쁜 것은 진행 상실보다 **회전축 흔들림/미추종**의 기여가 크다는 해석과 부합한다(축별 절대오차를 Euclidean 평균에 단순 가산한 수치는 아니다). H6 하행의 `action_delta_rms=0.5098`은 H1의 0.3405보다 크고 `roll_pitch_rms`도 0.0514 대 0.0206이다. 경사에서 진행을 확보하는 대신 **자세 변화·조작 변화 비용**이 증가하는 신호다. action RMS는 실제 에너지·토크·발 미끄러짐의 직접 측정이 아니다. 경사 상·하행 간 tracking 차이 **0.0041**, body 전진 차이 **0.167 m**는 이 조건에서 상대적으로 작으며 상·하 한쪽이 일관되게 크게 실패했다고 판단할 근거는 없다.

## 4. MP4 여섯 개의 시각 행동 관찰

각 영상을 직접 디코딩해 **20초 전체 구간을 1초 간격으로 확인**하고, `01_stairs.mp4`, `03_boxes.mp4`, `04_random_rough.mp4`에서는 **push 직전/직후(3.80·4.02·4.20·4.60 s, 7.80·8.02·8.20·8.60 s, 11.80·12.02·12.20·12.60 s, 15.80·16.02·16.20·16.60 s)**를 추가 비교했다. `03_boxes.mp4`의 2초대와 `04_random_rough.mp4`의 2초대는 원본 1920×1080 프레임으로도 확인했다. 카메라는 이동 로봇을 추적하므로 로봇의 화면 좌표 대신 **주변 지형 패치의 상대 이동·발 디딤·자세**를 근거로 삼았다. 표에서 시간은 영상 자체의 시각, `f`는 0-base 디코드 프레임이다.

| MP4 / 관찰 구간 | 접근·실제 접촉·진행 | 회복·약점과 평가 수치의 관계 |
|---|---|---|
| **`01_stairs.mp4`** — 0.02–3 s (`f1–150`), 3.80–4.60 s (`f190–230`) | 계단 끝/상단 모서리 부근에서 양발 교대하며 이동하지만, 계단 윤곽이 점점 화면 뒤·측면으로 밀려난다. **여러 단을 중앙으로 올라가거나 내려가는 연속 시퀀스는 확인되지 않는다.** | 4초 push 전후 화면상 주저앉지 않고 발걸음을 잇고 이후 평지 보행을 유지한다. **계단 통과율에 대응하는 정량 case는 ZIP에 없다.** |
| **`02_inverted_stairs.mp4`** — 0.02–4 s (`f1–200`), 5–19 s | 역계단의 모서리 가까이에서 보행을 시작하고, 계단 패치가 옆/뒤로 멀어지며 평지로 이동한다. 낙상은 관찰되지 않는다. | 다단 **역계단 중앙 통과 또는 구조적 발 걸림을 극복하는 능력은 미검증**. 검은 프레임이 있더라도 아래의 06 영상 문제와 혼동하지 않는다. |
| **`03_boxes.mp4`** — 1–4 s (`f50–200`), 7.80–8.60 s (`f390–430`), 11.80–12.60 s (`f590–630`), 15.80–16.60 s (`f790–830`) | **실제 높낮이가 있는 블록의 상단·사이에서 교대 발 디딤과 이동**이 확인된다. 특히 약 2.06 s에는 한 발이 블록 경계로 뻗고 반대쪽을 지지하는 모습이다. 이후도 블록 주변에서 이동/방향 전환을 이어간다. | 12초 전후 몸통·상체/보행 방향이 변하면서도 다시 발을 내딛고 서 있는 장면이 이어진다. 순간적인 불균형과 발 걸림이 **전혀 없다**고는 할 수 없고, 각 push의 회복시간을 측정할 자료도 없다. `scenario7`에는 boxes case가 없어 3,072 episode 성능으로 환산하지 않는다. |
| **`04_random_rough.mp4`** — 0.02–5 s (`f1–250`), 3.80–4.60 s (`f190–230`), 6–19 s | 초반 0–4초대 울퉁불퉁한 패치 위에서 발을 번갈아 디디며 **경계까지 전진**하고, 약 5–6초부터는 매끄러운 바닥으로 빠져나간다. 영상에서 최소한 초기 험지 접지·이동은 성공한다. | 4초 push 부근에도 자세를 유지하지만, 6–19초의 안정 보행 대부분은 **험지가 아니라 평지 위**다. 이것만으로 camera-off H5의 `seed 4202/env 41` stall 사례가 없다고 부정할 수 없다. 반대로 그 예외 한 건이 영상의 초반 보행을 무효화하지도 않는다. |
| **`05_slope_up_10deg.mp4`** — 0.02–5 s (`f1–250`), 8–19 s | 초기 경사 형상이 있는 구간을 밟고 서서 전진한다. 낙상·초기 큰 자세 상실은 보이지 않지만, 후반에는 추적 화면에서 거의 평평한 영역을 걷는다. | 평가 H6 상행은 평균 body 전진 **19.943 m**로 강하나 영상 20초 전체가 10° 상행인 것은 아니다. 경사 전체 길이 통과·최대 pitch를 프레임에서 정밀 측정하지 않는다. |
| **`06_slope_down_10deg.mp4`** — 0.02–5 s (`f1–251`, 홀수 프레임), 8–19 s | 검정 프레임을 제외한 **홀수 프레임에서 경사 하행 초기의 연속 발 디딤 및 후반 보행**이 보인다. 명백한 낙상은 보이지 않는다. | 평가 H6 하행 body 전진 **19.776 m**, tracking **0.2806**은 실제 별도 camera-off 시험의 결과다. 영상 캡처 결함 때문에 진동·미세한 발 sliding의 시간 연속성을 정상 50 fps처럼 평가할 수 없다. |

**캡처 검증:** 6개 MP4 모두 프레임 1,000개/20 s/50 fps를 디코딩했다. 각 영상 첫 `f0`은 검정이다. 이 외에 **`06_slope_down_10deg.mp4`에서는 짝수 `f0,f2,…,f998` 500개가 검정, 홀수 `f1,f3,…,f999` 500개가 유효 영상**인 교대 패턴을 전체 프레임 축소 디코드로 확인했다. 0·50·100…만 추출하면 06 전체를 검정으로 잘못 판정한다. 유효 홀수 프레임을 별도 확인했으며 **이는 영상 캡처 artifact이지 정책 낙상 기록이 아니다.** 다른 다섯 MP4에는 첫 `f0` 외 전면 검정 프레임이 없다.

**영상↔수치 종합:** boxes/rough에서 실제 접지하고 이동하는 장면은 H2/H5/H7의 **생존 이외 진행 능력**과 방향성이 맞는다. 그러나 카메라 영상의 rough는 초반 짧은 patch이고, 별도 H5 384회 평가에는 심각한 stall 꼬리가 있어 **전부 성공**으로 일반화할 수 없다. 영상의 push는 지형·명령 변화가 섞여 있어 평가 H7 384회의 정량적 회복 시간이나 충격 저항 한계와 등치시킬 수 없다. 미세 발 미끄러짐·공중 시간·관절 오프셋은 계측 필드가 없어 정량 평가하지 않는다.

## 5. 종합 의사결정과 다음 확인 1건

- **확인한 성공:** 20초 고정 window에서 낙상 없이 목표 속도에 가깝게 전진하고, camera-off 경사와 push 조건에서도 body-frame 이동을 지속한다. boxes·rough 초기 영상에서는 실제 보폭 및 장애물 접촉이 보인다. **이는 생존만 하는 정책이 아니라 실용적 이동 기능이 있는 정책**이라는 판단 근거다.
- **치명적/미검증 약점:** rough 단일 cohort의 66.4% stall(생존 상태), H1/H3의 잔류 순변위, yaw 추종 비용, stairs/inverted stairs 다단 통과와 boxes에 대한 별도 정량 검증 부재. 이 때문에 범용 지형 고신뢰 정책으로는 **HOLD**가 맞다.
- **채택 범위:** **내부 보행 베이스라인·평지/경사/push 동작 후보로 보존**할 만하다. 다른 H1 정책보다 우수하거나 현장 장애물을 확실히 통과하는 **최종 대표 정책으로는 아직 승격하지 않는다.** 동일 checkpoint 이전/이후 변화 또는 reward 원인도 미확인이다.

**다음 행동 한 가지(새 GPU 없이 우선):** 기존 보존 자료에서 **동일 H1 `scenario7` protocol의 `h1-submit-2 / TERM-50` 완료 평가 ZIP**이 이미 존재하는지 먼저 찾아, 있다면 `episodes.jsonl`과 `evaluation_manifest.json`·`resolved_configs.json`의 SHA/protocol/source·case·seed/num_env를 대조한 후 **H5 rough 하위 꼬리, H1/H3 정지·횡이동 잔류, H6 yaw/action 비용, H7 전진·생존**을 cohort 단위로 비교한다. 현재 첨부에는 이 대조 ZIP이 없으므로 비교 결과를 만들어내지 않는다. 기존 대조 자료가 없다면 **현재 HOLD를 유지**하고, 별도의 승인 없이는 신규 평가·렌더·학습을 하지 않는다. 이 비교에서 추종/진행 손실 없이 위험 꼬리가 줄었다는 근거가 나와도 계단 통과 미검증은 별개로 남는다.

## 6. 재검증 출처와 수행 범위

- **정책/완료/조건:** `source_checkpoint.txt`, `environment.txt`, `BUNDLE_README.txt`, `evaluation/evaluation_manifest.json`, `evaluation/video_evaluation_link.json`, `evaluation/evaluation.log`.
- **정량 직접 계산:** `evaluation/episodes.jsonl` — 3,072 전체 episode의 case/seed/`env_id`별 group-by, field-null/ID 중복/종료 사유, 추종/진행/전역 순변위·P05/P95/stall 재계산; `evaluation/diagnostics.json`과 모든 scenario tracking 평균 교차확인.
- **명령·지형·소스 재검사:** `evaluation/resolved_configs.json`의 `H1/flat/*`, `H2/flat/*`, `H3/flat/*`, `H4/flat/*`, `H5/rough/*`, `H6/slope_up/*`, `H6/slope_down/*`, `H7/push/*` 및 manifest `suite`·`source_fingerprints`.
- **시각 출처:** ZIP 루트 `01_stairs.mp4`, `02_inverted_stairs.mp4`, `03_boxes.mp4`, `04_random_rough.mp4`, `05_slope_up_10deg.mp4`, `06_slope_down_10deg.mp4`; 영상 시간과 frame anchors는 §4 참조.
- **수행한 검증:** ZIP을 직접 추출했고 18개 항목에 대한 ZIP CRC 검사가 통과했으며, 원자료를 재계산·프레임을 디코딩했다. ZIP 내 checkpoint 재해시, 원본 trainer/TensorBoard 접근, 새 평가·렌더·export/학습, 서버 작업 또는 원본 ZIP 수정·삭제는 하지 않았다. 입력 ZIP의 평가 종료 정상과 행동 정책 품질은 독립적으로 판정했다.
