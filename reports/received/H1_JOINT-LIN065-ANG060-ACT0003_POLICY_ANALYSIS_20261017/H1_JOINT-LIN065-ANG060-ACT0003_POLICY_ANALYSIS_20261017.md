> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/incoming/other/reviewed/H1_JOINT-LIN065-ANG060-ACT0003_POLICY_ANALYSIS_20261017/H1_JOINT-LIN065-ANG060-ACT0003_POLICY_ANALYSIS_20261017.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# H1 JOINT-LIN065-ANG060-ACT0003 / model_4950 정책 심층 분석

**분석일:** 2026-10-17 (KST)\
**목표:** 우선 **H1 공식 7시나리오 제출 후보로서의 행동 경쟁력** 판단. 계단·박스 등 광의의 지형 보행은 보조 목표로 구별한다.\
**결론: HOLD — 목표 속도 주행·경사·외란 중 생존 및 추종은 실용적인 수준이나, rough의 일관된 저속과 제자리·횡이동의 위치 편차를 상쇄할 만큼의 검증된 상대 우위가 없다.** 공식 후보로 즉시 교체하지 않는다. 그렇다고 계단 중앙 완주가 미입증이라는 이유만으로 공식 후보를 REJECT하지 않는다.

## 1. 정책 판단 요약

| 판단 축 | 직접 확인한 결과 | 해석 및 결론 |
|---|---|---|
| 시간창 생존·접촉 | **3,072/3,072** episode 모두 `timeout`, 20.0s; `terminated=0`, `base_contact_failure=true` 0 | **안정성 강점**. 낙상이 적다는 신호이지만 경로 완주·명령 충실도와 다름 |
| 전진 H2 | body 전진 적분 **14.820m**, 0.5→1.0m/s 목표 적분 **15m** | 실제 명령 전진 수행은 **성공**에 가까움. 월드 좌표 `dx` 평균을 속도 실패로 읽으면 안 됨 |
| 회전·경사·밀침 | H4 yaw 절대오차 **0.07308rad/s**; H6 상·하 body 진행 **19.992/19.814m**; H7 진행 **9.688m** | **이동 능력 존재**, 다만 pose·action 비용과 별도 영상 조건을 동반해 해석 |
| 거친 지형 H5 | body 전진 **평균 8.853m / P05 8.403m / 최소 7.930m**; 명령 적분 10m; `stall>0.05`는 0/384 | 완전 제자리 정체가 아니라 **지속적 속도 부족**. 평균·하위 꼬리 모두 개선 대상 |
| 제자리 H1 | body x 적분 **−0.259m**(뒤로 치우침); world XY 최종 순변위 크기 평균 **0.460m** | 제자리 명령에서도 의미 있는 위치 잔류. `stall=0`은 이 case에서 무의미 |
| 좌우 H3 | `vy_error` **0.07476m/s**, body x 적분 **−0.202m**, world XY 종료 순변위 **0.739m** | 횡속도 추종은 작동하나 **횡왕복 후 위치 잔류**. 위치 복귀 자체는 공식 명령이 아님 |
| 행동 비용 | H6 상·하 `action_delta_rms` **0.546/0.556**, H1 **0.397** | 경사에서 행동 변화량이 큼. 이 지표만으로 발 sliding/피로/토크 비용을 추정할 수 없음 |

**채택 구분:** **공식 제출 주후보: HOLD**, **전진·경사·밀침 능력: 유용한 긍정 신호**, **보조 계단·박스 완주: 증거 불충분**. 입력은 *한 정책*이므로 상대적 승자나 보상 가중치 조합의 인과 개선을 선언하지 않는다. 현재 우선 보존할 것은 기존 제출 정책이며, 다음 단계는 저장된 다른 H1 평가 ZIP과의 CPU 동등조건 비교다.

## 2. 입력 무결성·정책 ID와 평가 계약

| 항목 | 직접 확인한 사실 / 분리해야 할 사실 |
|---|---|
| 입력 | 제공 통합 ZIP **18개 항목**, MP4 6개, JSONL 3,072행, manifest·resolved configs·diagnostics·log. ZIP CRC 검사 통과, `SHA256SUMS.txt`의 **6 MP4 SHA256 모두 일치** |
| 정책 표시명 | **JOINT-LIN065-ANG060-ACT0003 / model_4950** (파일명은 식별 보조이고 SHA가 정책 identity) |
| checkpoint SHA256 | `2df0584057deb4dc15ab3c4470d52da29e5468bbb819fe3e4c66a928462bc478` |
| 정책 연결 | `source_checkpoint.txt`, `video_evaluation_link.json`, `evaluation_manifest.json`의 SHA **일치**. 원 checkpoint `.pt`는 ZIP에 없어 정책 파일 **바이트 자체는 재검증하지 않음** |
| 학습 증거(별도 GitHub 연결) | Experiment `exp-h1-joint-tracking-balance`; OFFICIAL fresh/no parent Run `20261017-015509-h1-lintrack-065-angtrack-060-actrate-0003-fresh5`, seed 42, 4096env, 5000 요청·console4999, `COMPLETED/exit0/PASS`; checkpoint index의 keeper4950 SHA가 위와 일치. 자동 best4800 SHA `9dadfcad…fd03095`와는 **별개**. **학습 완료는 행동 성공·제출이 아님** |
| 학습 설정(외부 공식 archive 기록) | `h1-submit-2` 기준 `track_lin_vel_xy_exp=0.65`, `track_ang_vel_z_exp=0.60`, `action_rate_l2=-0.0003`; `feet_air_time=0.20`, `termination_penalty=-50` 등 나머지는 해당 archive 기준. **세 축 동시 변경**이므로 어느 가중치의 독립 효과인지 말할 수 없음 |
| ZIP 내 학습 식별 | `policy.source_run_id=null`, `policy.preset=null` 그대로 유지. GitHub에서 SHA를 통해 연결한 실제 OFFICIAL Run은 **ZIP 내부 필드를 채운 것이 아님** |
| 내부 평가 | `evaluation_manifest.json`: PERSONAL, `COMPLETE=true`, non-smoke, robot=h1, deterministic policy, camera-off, **3 seed(4201/4202/4203)×128 env×8 case**; 총 3,072 episode/3,072 최초 cohort, 각 20초. `protocol_id=d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34` |
| 평가 조건 | H1~H4 flat, H5 random_rough, H6 slope_up·slope_down 각각 ±10° 계열, H7 flat+push. 환경 설정 fingerprint는 **case×seed별로 다름**; 평가 source fingerprint 및 resolved configs 수록. 실제 공식 비공개 시나리오·점수 함수 복제품이 아님 |
| 영상 조건 | 별도 seed42/num_envs1, `maneuver_push`, 1000 step×0.02s/50fps, 영상별 20s, noise off, global clock 명령·외란, ±10° 경사. **평가와 같은 episode가 아님** |

**설정 주의:** ZIP의 `evaluation/resolved_configs.json` 속 `environment_by_case_seed` 보상 스냅샷에는 `action_rate_l2=-0.0005`, `track_lin_vel_xy_exp=0.5`, `track_ang_vel_z_exp=0.5`, `termination_penalty=-5` 등의 값이 있다. 이 설정은 **평가 task 구성 스냅샷**이며, 앞 표의 학습 Run/보상값을 대체하지 않는다. 학습 설정은 별도 OFFICIAL evidence의 native source/resolved config에서 연결한다. 독립 평가의 환경·명령·물리 조건은 입력 manifest를 우선한다.

**지표 정의:** `mean_tracking_error`는 step별 `sqrt(Δvx²+Δvy²+Δyaw²)`의 episode 평균(선속도·각속도 혼합; 단일 `m/s` 단위 불가). `vx_error`, `vy_error`는 m/s, `yaw_error`는 rad/s의 절대 오차 평균; RMSE와 혼동하지 않는다. `forward_progress_m` = `integrated_body_forward_m`(같은 계산), **body-frame x속도 적분**이며 경로상의 지형 통과 길이와 동일하지 않다. `lateral_drift_m`는 실제 world 횡변위가 아니라 `|Δvy|` 적분이다. `stall_fraction`은 목표 body XY 속도≥0.2이고 실제 body XY 속도<0.1인 step의 비율이므로 명령 0인 H1의 0은 정지 유지 성취가 아니다.

## 3. 원자료 직접 재집계

기본 집계는 **각 episode를 동일가중**(짧은 종료 episode도 1개 행)하며 scenario H6의 두 case는 분리했다. 이번엔 모든 cohort가 **1 episode씩, 1000 step**이어서 reset 후 중복 생성은 없었다. `episode_id` 중복·결측 0, `(scenario,case,seed,env_id)` 고유 3,072. scenario 집계 `mean_tracking_error`를 `diagnostics.json`과 다시 계산했을 때 최대 차이는 floating point 오차(약 7×10⁻¹⁷)다. `survived` 모두 true이고 실제 접촉 종료가 0이므로 **고정 시간창 안에서 terminated 경험 cohort는 0/3,072**다.

### Case별 핵심 수치 (정확한 수치는 `case_metrics.csv`)

| case | N | tracking 혼합 ↓ | vx / vy / yaw 절대오차 ↓ | body x적분 (m) ↑† | stall 비율 ↓ | roll/pitch RMS ↓ | action Δ RMS ↓ |
|---|---:|---:|---:|---:|---:|---:|---:|
| H1 balance | 384 | 0.09715 | .01645 / .07156 / .04790 | **−0.259** | .00000‡ | .05565 | .39685 |
| H2 forward | 384 | .12067 | .02747 / .06980 / .07306 | **14.820** | .00400 | .05363 | .45048 |
| H3 lateral | 384 | .10352 | .01581 / .07476 / .05425 | **−0.202** | .00806 | .05764 | .39272 |
| H4 rotation | 384 | .11655 | .02523 / .07071 / .07308 | **9.608** | .00500 | .05503 | .38760 |
| H5 rough | 384 | **.17339** | .07676 / .06792 / **.11114** | **8.853** | .00601 | **.04542** | .43312 |
| H6 slope up | 384 | .14472 | .04574 / .06474 / .09671 | **19.992** | .00500 | .05551 | **.54648** |
| H6 slope down | 384 | .14268 | .04377 / .06815 / .09224 | **19.814** | .00500 | .05168 | **.55565** |
| H7 push | 384 | .12390 | .03362 / .07496 / .06765 | **9.688** | .00414 | .05538 | .39093 |

† H1·H3는 전진을 요구하지 않으므로 **0에 가까울수록 적절**하다. 나머지는 각 case의 명령 적분과 함께 판단한다. ‡ H1 분모가 되는 유효 속도 명령이 없으므로 `stall=0` 해석 불가. 표의 yaw는 rad/s, vx/vy는 m/s, RMS 자세는 rad 계열이며 서로 더하지 않는다. **전 case survived 384/384**, 종료 `timeout`. 요약의 전체 episode 동일가중 tracking 혼합 평균은 **0.12782164**(8 case 동수); 7 scenario를 각각 같은 가중치로 평균하면 **0.12555384**로 달라진다. 어느 것도 공식 총점이나 보정된 100점 점수가 아니다.

case별 tracking (내부 혼합오차)〔원본 참조: `figures/tracking_by_case.png` / 공개 사본 미포함〕

### 가장 큰 실패 패턴은 낙상이 아니라 H5 속도 부족

H5의 명령은 `vx=0.5m/s` 20초 → body x 적분 기준 목표 **10m**다. 실제는 평균 8.853m(**−1.147m**), P05 8.403m, 최소 7.930m로 전진은 있으나 목표 속도보다 느리다. 384개 중 **265개(69.0%)가 9m 미만**이며, `stall_fraction>0.05`는 **0/384**(완전 정체와 구별). P95 추종 혼합오차 **0.19977**, 가장 낮은 진행은 seed4201/env0 **7.930m**, stall .025, tracking .21185. 최대 stall은 seed4202/env96 **.030**에서 발생한다. 전부 20초 생존했기 때문에 진행 차이를 짧은 실패 에피소드 삭제의 효과로 만들지 않았다. H5는 전체에서 자세 RMS가 작은 편(.04542)인데도 오차와 속도 손실이 가장 크므로 **자세 생존을 위해 보수적으로 이동하는 행동일 가능성**은 있지만 실제 reward·마찰·발 끌림 기전은 이 자료만으로 확정할 수 없다.

H5 body 전진 적분 분포〔원본 참조: `figures/H5_progress_histogram.png` / 공개 사본 미포함〕

반면 H2는 명령 0.5m/s 10초 + 1m/s 10초에 대해 평균 body 적분 **14.820/15m**이고, H6 상·하는 1m/s 20초에 대해 **19.992/19.814m**, H7은 0.5m/s 20초에 대해 **9.688/10m**다. H6의 `world_xy_net_m` 평균은 **19.350m(상) / 19.222m(하)**. 이는 상당한 실제 월드 이동과도 양립하는 강점이지만, 전체 이동이 경사면 패치 위에서만 일어났다는 증명은 아니다. H4의 월드 최종 순변위 2.940m는 방향 전환 때문에 body 적분 9.608m와 다른 것이며 world X 평균이 작은 현상을 정체로 부르지 않는다.

### 횡이동·제자리와 seed별 일관성

H1의 body 진행 `−0.259m`는 뒤로 치우친 누수다. 시작 임의 yaw가 있으므로 world `dx`, `dy`의 부호 평균 대신 **`sqrt(dx²+dy²)`의 episode별 평균 0.460m**를 보조적으로 썼다. H3는 방향을 바꾸는 `vy +0.3→−0.3m/s` 명령에서 `vy_error 0.07476m/s` 및 종료 world XY 순변위 0.739m, body x누수 −0.202m가 있다. **최종 원점 복귀는 직접 command가 아니므로** 이를 곧장 공식 실패 수로 환산할 수 없지만, 경로 추종·위치 정밀도 사용에는 불리한 잔류다.

| 평가 seed | H5 mean body 전진(m) | H5 mean tracking | H3 mean vy_error(m/s) | H4 mean yaw_error(rad/s) |
|---|---:|---:|---:|---:|
| 4201 | 8.851 | .1744 | .0748 | .0730 |
| 4202 | 8.874 | .1721 | .0748 | .0731 |
| 4203 | 8.833 | .1737 | .0748 | .0731 |

세 평가 seed의 차이가 작고 주요 현상이 지속되지만 **학습 seed는 1개(seed42)**다. 다수 env/episode를 독립 학습 반복으로 세거나 형식적 유의성·reward 인과 우위의 p-value를 계산하지 않았다. 전 case의 P05/P95/min/max, seed×case, worst cohort는 제공 CSV에서 복원 가능하다.

## 4. 여섯 MP4의 실제 프레임 조사

**조사 방법·범위:** 각 MP4는 1920×1080, 50fps, 1000프레임이다. 모든 영상에서 **명령 경계(300·500·700·850), 밀침(200·400·600·800) 주변과 처음·중간·끝을 포함한 다수 선택 프레임**을 디코딩하여 contact sheet로 확인했다(지형별 36~45개 선택 프레임). 첫 4개 영상은 픽셀 검정 여부를 **1000프레임 전체** 검사해 `f0`만 완전 검정임을 확인했고, 경사 2개는 선택한 36개 프레임 중 `f0`만 완전 검정임을 확인했다(경사 2개 전체 검정 프레임 전수조사는 아님). **모든 프레임을 동작에 대해 연속 판독한 것은 아니고**, 아래의 보행·회복 관찰은 명시된 구간에 한정된다. 6개 모두 `f996–998` 본체 표시와 달리 **f999에서 본체가 사라지고 색 marker가 남는 마지막 프레임 경계 이상**을 관찰했다. 종료 직전 화면 이상을 물리 낙상으로 판정하지 않는다. 여섯 영상 자체의 SHA는 전부 통과했다.

**영상의 공통 global 명령표:** `f0–299`(0–6s) vx=1,vy=0,yaw=0 → `f300–499`(6–10s) (0.5,+0.3,0) → `f500–699`(10–14s) (0.5,−0.3,0) → `f700–849`(14–17s) (0.5,0,+0.5) → `f850–999`(17–20s) (0.5,0,−0.5). world-Y ±0.5m/s add-velocity push는 **f200/400/600/800**(4/8/12/16s)이다. 카메라가 따라오므로 로봇이 화면 중앙이라는 사실만으로 제자리라고 판단하지 않는다. 약한 밀침에도 이후 자세를 대체로 유지하는 선택프레임은 긍정적이나 **회복시간(초)을 직접 측정하지 않음**. 영상의 world push와 camera-off 평가 H7의 조건·시간표는 같지 않다.

| 영상·terrain | 직접 확인한 프레임 / 관찰 | 지형 통과·접촉에 대한 판정 |
|---|---|---|
| `01_stairs.mp4` / pyramid stairs | f50–200 (1.0–4.0s): 계단 줄이 몸체 가까이 놓이고 위치가 바뀌며 보행 자세 유지. f280–400 (5.6–8.0s): 계단 줄이 멀어지고 평지 패치가 커짐. f700–950(14–19s): yaw 전환 구간 기립 유지 | 초기 계단 경계에서 **이동 관찰**, 하지만 중앙 다단 계단을 발 접촉과 함께 전부 밟고 완주했는지는 불명확. 전진 방향과 계단 중심선 정렬도 불확실 |
| `02_inverted_stairs.mp4` / inverted stairs | f50–225 (1.0–4.5s): 역계단 모서리·줄이 로봇 뒤/옆으로 이동. f300–400 (6–8s): 구조물이 화면에서 멀어짐. f700–950: 방향 전환 중 기립 유지 | 경계/인접 영역을 벗어나는 이동은 보임. **중앙 역계단 전단/후단 완주·높낮이 통과는 증명 부족**. 이번 영상에 과거 다른 정책에서 보고된 짝홀 검정 교대는 **관찰되지 않음** |
| `03_boxes.mp4` / boxes | f50–225 (1.0–4.5s): 복수 박스와 로봇의 상대 위치 변화, 박스 군집 주변을 지나감. f310–500 (6.2–10.0s): 박스 패치가 화면에서 벗어나 평지 지속. f700–950: 횡/회전 구간 기립 | **박스 인접 실제 이동**은 확인. 중앙 밀집 박스 전부를 직접 넘어간 성공이라 단정 불가(경로가 가장자리에 걸쳐 있을 수 있음). 이 case는 정량 평가에 없음 |
| `04_random_rough.mp4` / rough | f50–225 (1.0–4.5s): 울퉁불퉁한 패치 위/경계에서 로봇 위치가 바뀌며 자세 유지. f280–400 (5.6–8s): 패치 대부분이 뒤로 사라짐. f700–950: 평지에서 회전 대응 | **초기 rough 접근·이탈은 긍정적**. 다만 후반은 평지이므로 20초 전체를 rough 통과 능력 증거로 세지 않는다. 별도 camera-off H5의 8.853m는 느리지만 계속 움직였다는 신호와 양립 |
| `05_slope_up_10deg.mp4` / ↑10° | f50–225 (1–4.5s), f300–500 (6–10s), f700–950(14–19s): 기립 상태의 이동·명령 후 자세 유지. 경사면 질감/윤곽은 먼 overhead 시점에서 구분이 어려움 | 평가 H6 상향 19.992m와 정성적으로 모순되지 않음. 영상만으로 **경사 시작·끝 지점의 정확한 통과 거리, 실제 발 sliding**은 미측정 |
| `06_slope_down_10deg.mp4` / ↓10° | f50–225, f300–500, f700–950: 하향 terrain 실행 중 몸체 기립·이동이 선택 프레임에서 보이며 회전 단계 뒤도 살아 있음 | camera-off 하향의 19.814m 진행과 정성적으로 양립. 전 구간이 10° 경사면이라는 증명 또는 밀침의 정량 복구시간은 아님 |

선택 프레임을 시간순으로 배치한 6개 이미지가 ZIP의 `video_contact_sheets/`에 있으며, 점검 범위를 `video_frame_audit.csv`에 적었다. 전체 영상은 **입력 ZIP에 그대로 있고 재렌더·재인코딩·재배포하지 않았다**. 특정 시각에서 발이 정확히 미끄러졌는지, 과도한 hop인지, 최종 복구시간이 얼마인지까지는 단절된 샘플로 확정하지 않는다. 마지막 `f999`의 본체 소실은 6개 공통 capture/end-boundary 현상이므로 별도 행동 실패가 아니다.

## 5. GitHub에서 확인한 공식 제출·점수 이력의 정확한 위치

**GitHub 커넥터 읽기 전용 직접 조회: 2026-10-17(KST).** 현재 후보 `2df05840…62bc478`은 GitHub의 OFFICIAL **학습 Run과 SHA 연결**은 확인되지만, 해당 checkpoint의 제출 `policy.pt`로의 변환·실제 제출·공식 채점은 **확인되지 않았다**. 아래 점수는 **기존 다른 H1 제출 정책**의 과거 공식 평가를 사용자가 전달하고 저장소에 보존한 수치이지 이번 ZIP의 점수가 아니다. R6은 포털에 직접 로그인해 확인한 것이 아니라 저장된 사용자 전달 공식 결과다.

| 공식 예선 H1 시나리오 | Round 2 TERM-50 (2026-09) | Round 4 AIRTIME-025 (2026-09-28 제출) | Round 6 ACTRATE-0001 / `model_9999` (2026-10-11 제출) |
|---|---:|---:|---:|
| H1 제자리 (10.5) | 8.62 | 8.58 | 8.60 |
| H2 전진 (14) | 11.24 | 11.34 | 11.30 |
| H3 좌우 (7) | 5.73 | 5.72 | 5.73 |
| H4 회전 (7) | 5.66 | 5.68 | 5.68 |
| H5 약한 요철 (10.5) | **8.17** | 8.00 | 8.02 |
| H6 경사 (10.5) | 8.47 | **8.53** | 8.52 |
| H7 밀침 (10.5) | 8.48 | 8.52 | 8.50 |
| **시뮬 합계 (70)** | **56.37** | **56.37** | **56.35** |

과거 제출은 요철에서 **R2 8.17→R4 8.00→R6 8.02**로 작은 하락/부분 회복, 경사에서는 **8.47→8.53→8.52**로 소폭 상승했지만 시뮬 총점은 거의 같았다. 이력상 현재 새 정책의 **H5 저속**, H1 정지 drift, H3 횡 추종·H4 yaw trade-off를 우선 확인할 이유는 있다. 그러나 내부 H5 속도 적분이나 혼합 tracking error를 위 채점의 `Tracking Score`, `Survival Rate` 혹은 예측 공식점수로 환산할 수 없고, 두 정책 집단의 학습량·기본설정·검증 조건도 다르다.

**검증한 저장소 링크:**

- [실제 JOINT 학습 Experiment / keeper·best SHA·OFFICIAL provenance](https://github.com/SE3C/naver-issacsim/blob/main/research/experiments/h1/exp-h1-joint-tracking-balance.md) · [OFFICIAL 학습 evidence Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261017-exp-h1-joint-tracking-balance-fresh5k)
- [현재 Experiment registry](https://github.com/SE3C/naver-issacsim/blob/main/research/EXPERIMENTS.md) · [submission presets](https://github.com/SE3C/naver-issacsim/tree/main/research/submission_presets)
- [Round 2 TERM-50 결과](https://github.com/SE3C/naver-issacsim/blob/main/data/processed/experiments/h1/analysis/2026-09-10_OFFICIAL_EVAL_H1_ROUND2_TERM50.md) · [Round 4 AIRTIME-025 결과](https://github.com/SE3C/naver-issacsim/blob/main/data/processed/experiments/h1/analysis/2026-09-30_OFFICIAL_EVAL_H1_ROUND4_AIRTIME025.md) · [Round 4 제출 snapshot](https://github.com/SE3C/naver-issacsim/releases/tag/submission-h1-prelim-r4-20260928)
- [Round 6 점수 수신·7개 항목 기록](https://github.com/SE3C/naver-issacsim/blob/main/data/processed/experiments/h1/analysis/2026-10-16_H1_ANGXY008_MODEL4650_POLICY_REVIEW.md) · [Round 6 제출 snapshot](https://github.com/SE3C/naver-issacsim/releases/tag/submission-h1-prelim-r6-20261011)

### 이전 PERSONAL 후보 결과와의 제한적 맥락 (이번 첨부는 단독 정책)

기존 문서의 **LINTRACK-065 fresh5K / model_4950, SHA `b7528923…`**는 이번 **JOINT / model_4950, SHA `2df05840…`**와 **다른 정책**이다. 그 기존 자료의 H3 world 종료 잔류 **3.102m**, H5 진행 평균/P05/최소 **8.995/8.411/7.943m**, H1 비의도 body 진행 **+0.063m**가 기록되어 있다. 이번 JOINT는 H3 world 잔류 **0.739m**라는 개선 후보 신호와, H5 평균 **8.853m**·H1 signed −0.259m라는 손실 후보 신호가 **동시에** 나타난다. 그러나 이번에 과거 ZIP의 원 episode 3,072행을 재열거나 protocol·source fingerprint·동등 초기조건을 대조하지는 않았으므로 이는 **서로 다른 시점에 작성된 보고서 숫자 비교**, 통제된 matched A/B나 인과효과가 아니다. 동일한 model 번호가 학습 모델의 동일성을 뜻하지 않는다는 점이 특히 중요하다.

## 6. 최종 권고와 단일 다음 행동

**최종 HOLD**를 유지한다. 성공 판정의 적용 범위는 **H2 명령 전진과 H6 경사 케이스의 body 진행, H7 밀침 하의 생존·이동**이다. H5의 저속과 꼬리, H1 뒤쪽 drift, H3 위치 잔류가 현재 **범용 H1 공식 제출 대체 후보**로 승격을 막는 관찰이다. 계단과 박스는 공식 H1 7시나리오에 없으므로 초기 영상에서 중앙 완주가 확인되지 않았다는 사실은 **보조 공백**이며 단독 REJECT 사유가 아니다. 보조 지형에서도 발 접촉·완전 통과는 미증명이다.

**다음 행동 한 가지:** 이미 보존된 **LINTRACK-065 fresh5K / model4950 (`b7528923…`) PERSONAL 평가 ZIP**과 이번 **JOINT4950 (`2df05840…`) 평가 원자료**를 **GPU 없이 CPU에서 고정 protocol·resolved config·source fingerprint·command·seed×env cohort 키** 순으로 확인하여, **H3의 vy·world 종료 잔류 개선 vs H1 drift/H5 속도 꼬리/H6 action 비용**을 대응 집계한다. 실패 또는 reset이 다르면 episode ID 대신 cohort 종료 횟수/여부를 비교한다. 동등성이 깨지면 가능한 지표만 기술 비교하며 원인 효과는 보류한다. 이미 존재하는 결과의 재집계로 판정할 수 있다면 새 학습·새 평가·추가 렌더는 필요 없다. **이 제안은 실행 승인이 아니다.** 비교에서 H3 이득이 재확인되면서 H5 손실이 작고 안정적인지에 따라 특정 횡이동 용도로 PROMOTE할 여지는 있지만, 반대면 범용 HOLD/기준 정책 유지가 타당하다.

### 근거 파일·재현 경로

- **원본 ZIP(별도 사용자 입력, 결과 ZIP에 재포장하지 않음):** `evaluation/episodes.jsonl`(개별 3,072행), `diagnostics.json`(대조), `evaluation_manifest.json`(identity/protocol), `resolved_configs.json`(실제 평가 조건), `video_evaluation_link.json`, `source_checkpoint.txt`, `environment.txt`, MP4 여섯 개.
- **이번 결과 ZIP:** 본 `.md`, `case_metrics.csv`, `seed_case_metrics.csv`, `H5_worst20_cohorts.csv`, `validation.json`, `video_frame_audit.csv`, `figures/`의 내부 수치 시각화, `video_contact_sheets/`의 실제 선택 프레임 모음, `recompute_metrics.py`.
- **재계산:** `python recompute_metrics.py <원본-통합-ZIP-실제경로> <빈-출력폴더>` (Python/pandas/numpy 필요, CPU-only). 스크립트가 ZIP CRC, 6개 video SHA, episode/cohort uniqueness, 동일 checkpoint SHA, diagnostics 평균 일치를 확인하고 CSV 생성. 영상 동작의 해석은 자동 계산이 아니라 보고서의 특정 선택 프레임 관찰이다.

**검증 완료:** ZIP 18항목 CRC 정상, 6개 MP4 영상 checksum 정상, 3,072행 raw/diagnostics 평균 일치, 모든 case·seed·cohort·실패 집계 일치, 실제 프레임 시각 확인, 공식 학습 Run SHA GitHub 연결 확인. **제약:** 단일 선택 checkpoint, 단일 OFFICIAL 학습 seed, PERSONAL evaluator, 기존 비교 ZIP 미첨부, 원 checkpoint 바이트 미포함, 선택프레임 시각 판독, 공식 채점 점수 없음. 원본·GPU·공식 서버·GitHub 원격 자료는 수정하지 않았다.
