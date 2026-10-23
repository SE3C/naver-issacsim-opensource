> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/incoming/other/reviewed/H1_ACTRATE0001_ANGXY008_MODEL4650_POLICY_ANALYSIS_20261016.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# H1 ACTRATE-0001 → ang_vel_xy_l2=-0.08 · model_4650 정책 심층 분석

> **판정: HOLD — 실질적 보행·횡왕복 복귀·경사·외란 대응 신호는 유효하지만, 험지 저속 및 계단 완주 검증 공백 때문에 범용 대표 정책으로는 채택 보류.**\
> 분석일: 2026-10-16 (KST) · 원본: 첨부 Windows 통합 ZIP 1개 · 평가: PERSONAL, `official_score=false`.\
> 새 학습·GPU 평가·렌더·export·서버 변경은 수행하지 않았다.

## 1. 결론 — 무엇을 실제로 할 수 있는가

- **생존·기본 보행:** H1 `scenario7` 8 case, seed 4201/4202/4203, 각 128 env의 **3,072/3,072 episode가 정확히 20초 timeout**이다. 실제 전진 명령에서 body-frame 진행과 월드 순이동도 발생한다. 단순히 서서 살아남는 정책은 아니다.
- **강점:** H1 정지의 body 전진 적분 **0.010m**, H3 횡왕복 종료 월드 XY 잔류거리 평균 **0.258m**, H6 상·하 경사의 body 전진 **19.175/19.023m**(20초 명령상 이상적 20m), H7 외란 전진 **9.201m**(이상적 10m). H3 최종 위치 복귀는 긍정적이나 시간별 횡속도 추종이 완벽하다는 뜻은 아니다.
- **핵심 약점:** H5 불규칙 요철에서 body 전진 **평균 7.972m / P05 7.230m / 최소 6.374m**, 이상적 10m에 비해 느리다. **384/384개가 10m 미달**, 194/384개가 8m 미만이다. 반면 `stall_fraction` 평균 **0.01145**, `>0.05`는 **1/384**뿐이다. 즉 주요 문제는 *완전한 정체·잦은 낙상*이 아니라 **진행은 하지만 목표 속도에 미달하는 상태**다.
- **영상상 보행:** boxes·rough 초기 장애물 구간에서 다리 교대와 전진이 보이며 후반에도 큰 자세 붕괴 없이 움직인다. 다만 stairs·inverted stairs에서는 계단 경계 주변을 지나가는 장면이 중심이므로 **중앙 다단 계단 완주로 인증할 수 없다**. 영상은 단일 env의 20초 정성 검증이고, camera-off 정량평가와 같은 episode는 아니다.
- **최종 판단:** 목표 행동 일부는 **성공**, 전지형에 걸친 충분한 속도·접촉 능력은 **미달/미검증**, 후보로서는 **HOLD**. 이 데이터만으로 `ang_vel_xy_l2 -0.05→-0.08`의 **부모/무변경 연장 대비 개선** 또는 공식 대회 점수 향상을 인정하지 않는다.

## 2. 정책 identity · 평가 계약 · 무결성

| 항목 | 직접 확인한 ZIP 내용 및 별도 계보 연결 |
|---|---|
| 표시명 | `H1 / ACTRATE-0001 부모2700 → ang_vel_xy_l2=-0.08 / model_4650` |
| 정책 파일 정체 | `model_4650.pt` · **SHA-256 `c272b13b5d3702c8a84c1470b597526efe2214d0ee38f34f65918c5f912a335f`** |
| ZIP identity | SHA-256 `522c8b6a6bc2e1a9ae99e1fdf86308b7a335c7bb6c2964c03ad6b3875be51d22`; **18개 파일 / CRC PASS**, 여섯 MP4 각각 `SHA256SUMS.txt` 일치 |
| 출처 연결 | 별도 GitHub Experiment/공식 evidence index상 OFFICIAL Run `20261015-143107-h1-actrate0001-angxy008-from2700-plus2k`의 indexed keeper4650과 SHA 일치. 부모 ACTRATE-0001 `model_2700.pt` SHA `e54d3389e20ea913968ef8d3edbea5004368ff225fa6b94f73fcd91cf93ca7ae` |
| 학습 관련 **외부 근거** | 부모 checkpoint부터 +2,000회 요청, console 4699/4700, 완료/validation PASS, seed42·4,096 env. 부모 대비 `ang_vel_xy_l2=-0.05→-0.08` 변경, `action_rate_l2=-0.0001` 유지. 자동 best `model_3400`·console endpoint4699는 여기 평가한 keeper4650과 **다름** |
| ZIP 자체 provenance 경계 | `evaluation_manifest.json`의 `policy.source_run_id=null`, `policy.preset=null`; 부모 import raw provenance `false/null/unknown`을 외부 SHA 연결로 소급 수정하지 않음. ZIP에는 원 checkpoint 바이트가 없어 파일 자체 SHA를 새로 산출한 것은 아님 |
| 평가 상태 | `execution_status=COMPLETE`, `complete=true`, 최상위 `smoke=false`, `evaluation.log` child exit 0, PERSONAL RTX 3060 Laptop GPU |
| 동일성 설정 | `Humanoid-v0`, `scenario7/internal-suite-v1`, **protocol ID** `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34`, deterministic inference, 128 env × 3 seed × 8 case, 20초·1,000 steps |
| 평가 케이스 | H1 정지, H2 전진, H3 횡왕복, H4 전진+좌우 회전, H5 rough, H6 ±10° 경사(상행/하행 분리), H7 push. 평지·rough·경사는 각 case의 `difficulty=0.5` |
| 평가 source·랜덤화 | 평가 manifest의 task source fingerprint 4개, 24개 case×seed applied environment fingerprint 및 resolved config 존재. 카메라 off, observation `enable_corruption=false`, 각 평가 episode 초기 위치·yaw는 랜덤 reset 범위; command는 episode clock 기준, H7 push는 4·8·12·16초 |
| 영상 계약 | 별도의 6개 MP4, 각 **1,000frame/50fps/20초**, `maneuver_push`, video seed42·env1, 초기 XY/yaw 고정 0, noise off, 전역 명령·외란 clock. `video_evaluation_link.json`의 checkpoint SHA·protocol ID 일치 |
| 영상 command | 0–6초 `[1,0,0]`; 6–10초 `[0.5,+0.3,0]`; 10–14초 `[0.5,-0.3,0]`; 14–17초 `[0.5,0,+0.5]`; 17–20초 `[0.5,0,-0.5]` (`vx/vy` m/s, yaw rad/s), world Y push ±0.5m/s @ 4/8/12/16초 |

**검증 수준:** ZIP 자체 CRC·해시 및 정책 SHA의 *기록상 일치*를 확인했다. 별도 GitHub 저장소의 Experiment/evidence index는 외부 출처이며, 여기서 OFFICIAL 서버에 접속하거나 학습 archive/checkpoint 자체를 재다운로드·재검증하지는 않았다. 현재 케이스와 seed key가 과거 다른 ZIP과 같아도 정확히 동일한 물리 지형·초기상태·reset 후 궤적을 보장하지 않는다.

## 3. 정량 원자료: 3,072행 전체 재집계

`evaluation/episodes.jsonl` 3,072행을 직접 읽어 `evaluation/diagnostics.json`의 시나리오별 episode 수, survival과 평균 `mean_tracking_error`를 재현했다. **episode ID 중복 0, 결측 0, policy SHA·protocol ID 각각 단일값, 고유 `(scenario,case,seed,env_id)` cohort 3,072개**. 모든 episode는 1,000steps, 20초 `timeout`, `base_contact_failure=false`; 따라서 cohort별 종료 경험률/종료횟수도 0/3,072·0회이며 reset 후 중복 episode는 없었다.

다음 표는 **각 case 384 episode의 단순 평균**(`H6`은 두 case 별도)이며, tracking은 서로 다른 물리 단위의 축 오차를 합친 **무차원 점수가 아니라 단위 혼합 내부 값**이다. `vx/vy`는 m/s, `yaw_error`는 rad/s, 진행과 최종 월드 XY 순변위 크기는 m이다.

| 시나리오(case) | 혼합 tracking ↓ | `vx / vy / yaw` 절대오차 ↓ | body 전진 평균 m ↑ | 진행 P05 / 최소 m ↑ | 월드 XY 종료 순변위 크기 평균 m | stall 평균 |
|---|---:|---:|---:|---:|---:|---:|
| H1 정지 | 0.11134 | .0230 / .0779 / .0677 | **0.010** | -0.016 / -0.032 | **0.286** | 0 |
| H2 전진 | 0.16642 | .0507 / .0869 / .1054 | **14.104** | 14.086 / 14.076 | 13.502 | .00500 |
| H3 횡왕복 | 0.11414 | .0236 / .0825 / .0642 | **0.064** (비의도 전진) | 0.048 / 0.034 | **0.258** | .00728 |
| H4 전진+회전 | 0.16641 | .0454 / .0859 / **.1169** | 9.196 | 9.184 / 9.174 | 3.297 | .00600 |
| **H5 rough** | **0.22258** | **.1132** / .0859 / **.1339** | **7.972** | **7.230 / 6.374** | 7.939 | **.01145** |
| H6 경사 상행 | 0.17864 | .0553 / .0864 / .1166 | **19.175** | 19.081 / 19.035 | 17.941 | .00700 |
| H6 경사 하행 | 0.18062 | .0594 / .0899 / .1130 | **19.023** | 18.864 / 18.802 | 17.850 | .00701 |
| H7 밀침 | 0.16751 | .0563 / .0880 / .1037 | **9.201** | 9.145 / 9.117 | 8.931 | .00625 |

전체 **episode-가중 mixed tracking 평균 = 0.163458**. 전체 축별 `xy_rmse` 평균은 **0.13187m/s**, `yaw_rmse`는 **0.13298rad/s**로 별도 집계했다. 특히 H4의 `yaw_rmse=0.14303rad/s` 및 H5의 `xy_rmse=0.17970m/s`, `yaw_rmse=0.17612rad/s`는 회전·험지의 다른 손실축을 보여 준다. 이 RMSE는 `vx/vy/yaw_error`의 절대오차 평균과 정의가 다르다. 이번 구성은 여덟 case가 각각 384행이므로 case-동일가중 평균과 숫자가 같지만, 일곱 `scenario`를 동일가중할 때는 H6 상·하를 하나로 묶는 다른 집계다. 내부 scenario 가중치를 공식 점수 또는 임의 총점으로 환산하지 않았다.

### 중요한 행동 해석과 반대 근거

1. **정지는 거의 완성된 듯 보여도 월드 위치는 완전 고정되지 않는다.** H1 body-forward 적분은 평균 **+0.010m**에 불과하지만 `hypot(world_dx_m, world_dy_m)`의 *행별 크기 평균*은 **0.286m**다. `world_dx`/`world_dy`의 부호 있는 평균이 0에 가깝다고 위치 이동이 0이었다고 오판하면 안 된다. H1 `stall=0`은 정지 명령에서 유효 분모가 없기 때문이며 합격 신호가 아니다.
2. **횡왕복은 순위치 복귀가 좋지만 속도 추종은 별도다.** H3 잔류 **0.258m**이고 body 비의도 전진 **0.064m**, `vy_error=0.08246m/s`, `xy_rmse=0.10106m/s`다. `lateral_drift_m=1.649m`는 실제 횡변위가 아니라 횡속도 절대 추종오차를 적분한 값이다. 순변위가 작아도 경로상 오버슈트·방향 전환 지연은 이 episode 집계만으로 배제할 수 없다.
3. **전진과 경사는 유효하다.** H2 명령상 이상적 body 적분 15m 대비 **14.104m**이며 진행의 하위 꼬리가 매우 작다(최소 14.076m). H6 ±10°는 이상적 20m 대비 상행 **19.175m**, 하행 **19.023m**로 두 방향 모두 보행 진행 신호가 강하다. 다만 경사 영상 후반은 평지이므로 20초 전체를 경사 접촉 성공 시간으로 세지 않는다.
4. **험지에서는 저속이 우세한 실패 양상이다.** H5 이상적 10m 대비 평균 **7.972m**, 5백분위 **7.230m**, 최악 **6.374m**. `world XY` 순변위 크기 평균도 **7.939m**이어서 유효 이동이 존재하지만, 평균 XY 속도 명령을 잘 따르는 것은 아니다. `vx_error=0.11318m/s`는 8 case 중 최악이고 tracking P95 **0.25714**, 최댓값 **0.29426**. 반면 막혀 서는 `stall`은 평균 1.145%이므로 **자주 멈춰 서는 정책**이라고 표현하는 것은 부정확하다.
5. **자세·행동 비용 trade-off:** `roll_pitch_rms` H1 **0.09773**, H3 **0.09755**, H5 **0.06307**, H6 상/하 **0.07930/0.07557**. H6 `action_delta_rms` **0.56005/0.57921**는 H1 **0.34153**, H2 **0.44277**보다 크다. 이는 경사 진행의 행동 변화 비용이 높다는 관찰이지 관절 토크·발 미끄럼 수치나 `ang_vel_xy_l2` 강화의 인과효과가 아니다. 회전 H4는 body 전진 9.196m에도 월드 순변위 크기가 3.297m일 수 있다. 회전 명령이 있으므로 이것을 stall로 취급하면 안 된다.

### rough 하위 꼬리·seed 집중도

| H5 seed (각 128 env) | 진행 평균 m | P05 m | 최소 m | 7m 미만 수 | 8m 미만 수 |
|---|---:|---:|---:|---:|---:|
| 4201 | 7.994 | 7.348 | 6.540 | 1 | 62 |
| 4202 | 7.992 | 7.273 | 6.701 | 2 | 63 |
| 4203 | **7.929** | **7.072** | **6.374** | **6** | **69** |
| **전체** | **7.972** | **7.230** | **6.374** | **9/384** | **194/384** |

- H5 전체 분포: **6–7m 9건, 7–8m 185건, 8–9m 188건, 9–10m 2건, 10m 이상 0건**. 최악은 **seed4203/env16**: 진행 **6.374m**, mixed tracking **0.29337**, `vx_error=0.18942m/s`, stall **0.042**. stall 최댓값은 **seed4203/env109, 0.052**(진행 6.628m). 즉 최악 진행도 20초 timeout까지 생존했고 완전 정체가 아니었다.
- Seed별 평균과 하위 꼬리 모두 4203이 가장 낮다. 다만 세 평가 seed와 많은 env는 **독립 학습 seed 384개**가 아니다. 새로운 p-value나 통계적 우월성을 만들지 않았다.
- `forward_progress_m`와 `integrated_body_forward_m`는 모든 행에서 정확히 일치했다. 독립 근거 두 개로 세지 않았다. `survived=true`도 모두 실제 지형 완주가 아닌 timeout이다.

## 4. 6영상: 시간·프레임을 가진 정성 관찰

**실제 검사 범위:** MP4 6개 각각 1,000프레임/50fps를 확인했고, 지형당 초반 0.02–6.02초에 0.5초 안팎 간격, 이후 8/10/12/16/19초 전후 등 **각 영상 약 26개의 서로 다른 실제 프레임을 시각 검사**했다. 추적 카메라 화면 안 로봇의 자세·장애물 상대 위치를 비교했다. 전 프레임의 발 접촉을 하나씩 수작업 판독한 것이 아니다. 별도 FFmpeg 전 구간 검정화면 탐지에서는 **여섯 MP4 모두 f0(0.00–0.02초)만 검정**, 나머지 구간의 교대 검정/연속 검정은 검출되지 않았다. 이것은 capture artifact이지 낙상 근거가 아니다.

| 영상 | 확인한 구간/프레임과 동작 | 성능 판정 범위 |
|---|---|---|
| `01_stairs.mp4` | f1–201(0.02–4.02초) 로봇이 계단 구조물 **경계/옆의 표면**을 지나며 다리 교대·위치 이동. f251–301(5.02–6.02초)에는 계단 구조가 뒤로 물러나고, f701/801/951(14.02/16.02/19.02초) 평지 보행·회전이 보인다. | 해당 1 env의 *계단 인접 이동*과 붕괴 없는 후속 보행은 보이나 중앙 여러 단을 연속으로 올라 완주했다는 근거는 **없다**. |
| `02_inverted_stairs.mp4` | f1–176(0.02–3.52초) 좌측 다단 구조 **경계 바깥쪽/상단 주변**에서 보행; f226–301 이후 지형 구조가 멀어지고 f701–951 평지 명령 전환에 따른 자세/진로 변화가 보인다. | 전체 다단 하강 성공으로 단정할 수 없다. 큰 낙상은 확인 프레임에서 보이지 않는다. |
| `03_boxes.mp4` | f1–176(0.02–3.52초) 박스 사이의 발디딤과 몸통 이동, f201–251(4.02–5.02초) 높은 블록 경계에서 전진해 벗어나는 장면, f301 이후 평지 이동. | **초기 boxes 구간 통과 신호는 긍정적**. 하지만 별도 boxes 평가 case가 없으므로 다수 난이도에서의 성공률·발 충돌률을 제시할 수 없다. |
| `04_random_rough.mp4` | f1–151(0.02–3.02초) 작은 돌기 지면 위에서 발을 교대하며 전진, f176–226(3.52–4.52초) rough→평지 경계 통과, f301 이후 평지. | **초기 rough 패치 유효 진행**은 시각적으로 확인되지만, 20초 평가 H5의 느린 평균 전진과 모순되지 않는다. 영상에서는 rough 위에 있는 시간이 짧다. |
| `05_slope_up_10deg.mp4` | f1–151(0.02–3.02초) 완만한 경사 무늬 위로 이동하는 장면, f201–301 이후 평탄 지면, f701–951 회전 시 다리 교대 및 자세 유지가 보인다. | H6 상행 body 진행 19.175m와 **경사 방향 이동 신호**가 일치한다. 20초 전체의 경사 체류·고도 획득량은 확인되지 않는다. |
| `06_slope_down_10deg.mp4` | f1–151 경사 무늬 주변 이동, f201–301 평탄 영역, f701/801/951(14.02/16.02/19.02초) 회전 명령 중에도 수직 자세와 교대 보행이 보인다. | 하행 H6 진행 19.023m 및 timeout과 일치하는 생존·이동 신호. 카메라만으로 경사 수직 고도차나 미끄럼량을 수치화할 수 없다. |

**명령·외란 해석:** 모든 영상의 0–6초는 빠른 전진, 6–10초·10–14초는 좌우 복합 전진, 14–17초·17–20초는 전진+반대방향 회전이다. 고정 world-Y push는 4, 8, 12, 16초에 적용된다. 예컨대 `03_boxes.mp4` f201→251과 `04_random_rough.mp4` f201→251의 이동은 *4초 push 뒤에도 자세가 무너지지 않는 정성 신호*이지만, 해당 영상에서 push 이전/이후 속도 시계열이 없어 **회복에 몇 초 걸렸는지는 미확인**. 후반 화면 중앙에 유지되는 것만으로 정체라고 보지 않았으며, 14초 이후 회전 장면의 월드 X 변화가 작아도 전진 실패로 판정하지 않았다.

**정량과 영상의 대응 한계:** 비디오와 camera-off `scenario7`은 같은 checkpoint·protocol 연결 정보를 가지지만 `maneuver_push`의 단일 env/seed42·전역 명령·지형 패치와, 평가의 seed4201–4203/128env·episode clock/reset·terrain case는 별개다. 계단·박스 정량 case가 없다. 발 미끄럼, 에어타임, 장애물 접촉 충격, 실제 관절 편차를 수치화한 필드도 없다.

## 5. 과거 제출 이력과의 관계 — **현재 정책 점수가 아님**

2026-10-16 KST에 GitHub 연결로 [`SE3C/naver-issacsim` Experiment registry](https://github.com/SE3C/naver-issacsim/blob/main/research/EXPERIMENTS.md), [본 angxy 실험 기록](https://github.com/SE3C/naver-issacsim/blob/main/research/experiments/h1/planned/exp-h1-action-first-body-rate-switch.md), [제출 preset 이력](https://github.com/SE3C/naver-issacsim/blob/main/research/submission_presets/README.md), [Round-2 기록](https://github.com/SE3C/naver-issacsim/blob/main/data/processed/experiments/h1/analysis/2026-09-10_OFFICIAL_EVAL_H1_ROUND2_TERM50.md), [Round-4 기록](https://github.com/SE3C/naver-issacsim/blob/main/data/processed/experiments/h1/analysis/2026-09-30_OFFICIAL_EVAL_H1_ROUND4_AIRTIME025.md)를 **읽기 전용** 조회했다. 공식 결과 원본 포털을 직접 관람한 것이 아니라 저장소에 보존된 **사용자 전달 공식 결과 정리**를 읽은 것이다.

| 제출/공식 평가 | 정책 연결 및 시점 | 공식 시뮬레이션 / 전체 | 이전 대비 사례별 변화 |
|---|---|---|---|
| 예선 R2 `h1-submit-2 / TERM-50` | OFFICIAL TERM-50 5K, 제출 2026-09-09; 제출 policy↔특정 numbered checkpoint는 완전 확증 안 됨 | **56.37/70; 종합 86.37/100** | 제자리 8.62, 전진 11.24, 좌우 5.73, 회전 5.66, rough 8.17, 경사 8.47, 밀침 8.48 |
| 예선 R4 `h1-submit-4 / AIRTIME-025` | OFFICIAL fresh10K 계보, 2026-09-28 제출 보고; 정확한 numbered source 미확정 | **56.37/70; 구성합 86.37/100** | R2 대비 **rough 8.17→8.00(-0.17/10.5)**, 전진 11.24→11.34(+0.10/14), 경사 8.47→8.53(+0.06/10.5). 나머지 변화는 ±0.04 이내 |
| 예선 R6 `h1-submit-6 / ACTRATE-0001` | **별도 OFFICIAL fresh10K `model_9999`**가 실제 제출 actor와 연결됨, 2026-10-11 사용자 제출 확인 | **공식 점수 미수신** | 이번 angxy 자식 `model_4650`이 아니다 |

운영진 공개 결과에는 H1 R2·R4 각 시나리오별 **Survival Rate·Tracking Score 구성 값이 제공되지 않았으므로 만들지 않았다**. R2/R4의 종합점수 동률과 rough 소폭 하락은 해당 *제출들*의 관찰이지 본 `c272b13b…` 정책의 추정 점수가 아니다. 공식 약한 요철 점수가 상대적으로 낮았던 사실은 본 평가의 rough 저속을 **확인할 이유**로는 유용하지만, 서로 다른 정책/실행조건/채점식의 동일 결과를 보장하지 않는다.

이번 모델의 OFFICIAL 학습/정책 ID를 구분해야 한다. 부모 `model_2700` (`e54d…`), 무변경 +2K `model_4699`(별도 SHA), action-rate 복원 자식 `model_4650` (`a824…`), LINTRACK 자식 `model_4650` (`ce7…`), LINTRACK-.55 자식 `model_4650` (`e8a…`)와 모두 다르다. 2026-10-16 registry의 lin=.55 4정책 분석에도 **이번 angxy 자식은 포함되지 않는다**. 따라서 이전 비교 보고서의 결과를 이번 자식과 직접 대응 원자료 계산을 끝낸 결과로 읽지 않는다.

## 6. 최종 후보 판정과 다음 행동 **한 가지**

**HOLD 유지.** 정지 body 누수 작음, H3 왕복 종료 잔류 작음, 경사·push에서 장시간 진행, 3,072/3,072 timeout은 분명한 강점이다. 동시에 H5 **평균 7.972m/이상적 10m**, **최저 6.374m**, 높은 `vx_error`, H6 상대적으로 큰 action Δ, 중앙 다단 계단 미확인은 범용 PROMOTE를 막는다. 현재 H5 문제는 주로 *목표보다 느리게 계속 전진*하는 형태다. **REJECT할 정도의 전반적 붕괴 근거도 없다.**

**다음 행동 하나:** 새 GPU 작업 없이 **보존된 부모 `model_2700` 대 무변경 +2K `model_4699` 대 이번 `angxy=-0.08/model_4650`의 `episodes.jsonl`을 CPU에서 동일 cohort key로 대응 재집계**한다. 우선 H5 `forward_progress_m` 평균/P05/최소·`vx_error`·stall 최악, H3 `vy_error`/월드 XY 잔류, H6 `roll_pitch_rms`/`action_delta_rms`, H4 yaw를 비교한다. 동일 `protocol_id`뿐 아니라 `resolved_configs.json`/source fingerprints, case, command, terrain, noise, 20초 horizon/seed/env 수를 함께 맞춰야 한다. 이미 존재하는 비교 보고서에서 검증된 부모/무변경 두 정책 수치는 **기존 자료**로 재사용하고 이번 ZIP을 추가하면 된다. 이 분석에서 비교용 타 ZIP 원본을 직접 열지 않았으므로 **`angxy` 변경에 의한 개선·악화의 독립 직접 비교는 아직 수행되지 않았다**.

채택 판단을 바꿀 정보는 구체적이다. 같은 부모/무변경 연장 대비 **H3·H6 자세·횡이동 지표가 실제로 좋아지면서 H5 하위 진행이 보존되는지**가 확인되면 다음 활용·확인 후보 승격을 재검토할 수 있다. 반대로 자세 이득 없이 rough 진행만 희생되면 현재 범용 후보 순위를 낮춘다. 이 결과 역시 서로 다른 학습 Run·checkpoint 선택에서 보상의 단독 인과효과로 자동 귀속하지 않는다.

### 원자료 재확인 경로

- **첨부 원본 ZIP**: `h1-actrate0001-angxy008-from2700-plus2k_model_4650_h1_6terrain_evaluation_20261016-082140_edfb8cad.zip`
- **기본 identity:** `source_checkpoint.txt`, `evaluation/evaluation_manifest.json`, `evaluation/video_evaluation_link.json`, `environment.txt`, `SHA256SUMS.txt`
- **정량 재계산:** `evaluation/episodes.jsonl` (3,072 JSONL), `evaluation/diagnostics.json`, `evaluation/resolved_configs.json`, `evaluation/evaluation.log`
- **영상 근거:** `01_stairs.mp4` · `02_inverted_stairs.mp4` · `03_boxes.mp4` · `04_random_rough.mp4` · `05_slope_up_10deg.mp4` · `06_slope_down_10deg.mp4`
- **같은 부모 CPU 비교용 기존 자료:** [부모2700 평가 배포 기록](https://github.com/SE3C/naver-issacsim/blob/main/data/processed/operations/windows_h1_video_evaluation/2026-10-10_ACTRATE0001_MODEL2700_PUBLICATION.md), [무변경 +2K 평가 Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261015-exp-h1-action-rate-relaxation-model4699-video-eval), [이번 angxy 평가 Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261016-exp-h1-action-first-body-rate-switch-angxy008-model4650-video-eval), [공식 angxy 학습 evidence Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261015-exp-h1-action-first-body-rate-switch-angxy008-resume2700-plus2k)

**계산·검증 범위:** ZIP 18파일 직접 개봉, CRC 및 6영상 SHA 검사, 3,072 raw행 통계 재산출, case/seed/하위꼬리·cohort 재확인, 6영상 실제 프레임 표본 및 전체 구간 검정 프레임 탐지, GitHub 관련 기록 읽기만 수행했다. 원본 변경·게시·새 학습/평가는 없다.
