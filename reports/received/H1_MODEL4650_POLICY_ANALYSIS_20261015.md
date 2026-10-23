> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/incoming/other/reviewed/H1_MODEL4650_POLICY_ANALYSIS_20261015.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# H1 `model_4650` 정책 행동 심층 분석 — 6영상 + `scenario7` 원자료

- **판정일:** 2026-10-15 (KST)\
- **주 입력:** `h1-actrate-return2700-2k_model_4650_h1_6terrain_evaluation_20261015-032125_3fb52eff.zip` (ZIP SHA-256 `f3c5bd802479ab50b347984a122615a895343ccf418f9e66b4d846f83399f84c`)\
- **정책 표시명:** **MODEL4650**. `actrate-return2700-2k`는 입력 파일·저장 경로에 나타나는 문자열이지, 이 ZIP만으로 검증된 부모 Run·reward 변경 내역이 아니다.\
- **근거 범위:** 이 ZIP의 `episodes.jsonl` 3,072행 직접 계산, `diagnostics.json` 재현, 6개 MP4의 시간 분산 프레임·장애물 구간 상세 프레임 직접 판독. 보존 문서의 과거 ACTRATE-0001 `model_2700` 수치는 **별도 이전 분석 기록을 인용**하며, 이번 ZIP에서 그 정책의 원자료를 재계산한 것은 아니다.

## 1. 결정 — 전진·횡이동은 유용하지만 전지형 주후보는 **HOLD**

**목표 행동은 부분적으로 성공한다.** 단순한 생존형 제자리 정책이 아니다. 평지 전진(H2)은 20초 body-frame 전진 적분 **15.297m**(명령 적분 15m), 회전 복합(H4)은 **10.439m**(목표 전진 적분 10m), 밀침 조건(H7)은 **10.364m**(명령 10m), 경사 상·하(H6)는 **20.187/19.975m**(각 명령 20m)로 움직였다. H3는 명령이 10초마다 `vy=+0.3→−0.3m/s`로 뒤집히는 조건에서 `vy_error=0.0771m/s`, `stall_fraction=0.010`이고 종료 시 **world XY 순변위 크기 평균 0.167m**여서, 횡이동 후 복귀 방향의 실질적인 추종 근거도 있다. 다만 *최종 위치가 가깝다*는 사실만으로 왕복 궤적 전체를 증명하지는 않는다.

**가장 중요한 반대 근거는 H5 rough다.** 384/384 episode가 20초 생존했지만 전진 적분은 평균 **8.769m**(명령 적분 10m), 하위 5백분위 **7.970m**, 최저 **4.845m**였다. 최악 `seed=4201/env_id=60`은 **stall 0.386**, tracking **0.33263**, body 전진 **4.845m**인데도 timeout 생존했다. 즉 *넘어지지 않으면서 충분히 전진하지 못하는 실패*가 실제로 존재한다. H5에서 `forward_progress<8m`가 **21/384**, `stall_fraction>0.05`가 **7/384**이고 이 사례들은 seed 4201~4203에 분산된다. 이 하위 꼬리를 전체 384개가 실패한 것으로 확대해서도 안 된다.

**주된 trade-off는 정지·횡이동의 누수 감소 ↔ rough 진행의 악화 가능성**이다. 이전 문서에 기록된 ACTRATE-0001 `model_2700` 대비 H1 정지 명령의 비의도 body 전진 **1.987→0.282m**, H3 횡이동 중 비의도 body 전진 **1.677→0.276m**로 크게 줄었다. 반대로 H5 rough 평균 **9.948→8.769m**, P05 **9.592→7.970m**, 최소 **8.815→4.845m**로 낮아졌다. 이 비교는 평가 프로토콜 ID와 명목 case 구성은 같은 이전 기록과의 *기술적 참고 비교*이지, 이번 요청에서 이전 ZIP의 전체 resolved config·cohort·실제 물리 궤적을 재검증한 matched A/B 또는 reward 인과 실험이 아니다.

**결론:** 제한된 평지 명령 추종·전진 및 외란 대응을 검토할 가치는 충분하다. 그러나 **현재 범용 H1 대표/전지형 활용 후보로는 PROMOTE하지 않고 HOLD**한다. 특히 uneven terrain에서 최소 진행을 보장해야 하는 용도에는 아직 권하지 않는다. 공식 제출·채점·학습 성공 여부에 관한 판정이 아니다.

## 2. 정책 식별과 평가 조건

| 항목 | 이번 MODEL4650의 직접 확인값 |
|---|---|
| Robot / 체크포인트 | `h1` / `model_4650.pt` (경로 기록) |
| 체크포인트 SHA-256 | `a8249db467a60015036bf229b0026b215a61e17859f1d302efe283af225b84ea` |
| ZIP 내부 학습 계보 | `policy.source_run_id=null`, `policy.preset=null`; 부모·resume·학습 reward·선택 기준 **미검증** |
| 평가 | **PERSONAL Windows**, `execution_status=COMPLETE`, `complete=true`, `smoke=false`, native child exit `0` |
| 정책·프로토콜 | deterministic inference / `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34` |
| 정량 평가 분량 | `scenario7`, **7 scenario·8 case × 3 seed(4201/4202/4203) × 128 env = 3,072** 최초 cohort, case당 384, 20초/1,000 step, command 전환은 10초 |
| 유효 종료 | **3,072 timeout / 0 terminated / 0 base-contact failure**; 초기 cohort 3,072, 원자료 episode 3,072, restart 0 |
| 지형과 명령 | H1 제자리, H2 전진, H3 횡이동 왕복, H4 전진+양방향 yaw, H5 rough, H6 ±10° 경사 분리, H7 전진+world XY 외란; 평가 지형 difficulty `0.5` |
| 정량 평가 source | manifest `source_fingerprints` 4개, agent fingerprint `976cb139…729b2`, 24개 case×seed 적용 환경 fingerprint 존재. **동일 조건 외부 정책의 재검증은 이번 ZIP만으로 불가** |
| 영상 | `maneuver_push`, seed/terrain seed `42`, num_envs=1, 50 fps × 1,000 frame × 6개, observation noise off, reset pose `(0,0,0)`, ±10° 영상 경사 |
| 영상 ↔ 평가 identity | `source_checkpoint.txt`, `BUNDLE_README.txt`, `evaluation_manifest.json`, `video_evaluation_link.json`의 **동일 정책 SHA** 및 protocol 연결 일치 |

ZIP 중앙 디렉터리 **18개 항목**이 정상이며 ZIP CRC 검사 통과. `evaluation.log` 종료는 `COMPLETE`, child exit 0이고 fatal/traceback은 발견되지 않았다. 단, 원본 `.pt` 바이트가 ZIP에는 없으므로 **체크포인트 해시의 상호 기재 일치**를 확인했지 원 체크포인트 자체를 다시 SHA 계산한 것은 아니다. `official_score=false`, `raw_diagnostics_only=true`다.

정량 `resolved_configs.json`은 **camera off**, 128 env, `num_rows=10/num_cols=20`의 지형 생성 설정(rough·slope), 무작위 reset 위치·yaw, seed별 적용 설정을 가진다. 반면 영상은 1×1 고정 패치·고정 reset 방향과 전역 명령 시간표를 사용한다. 영상은 0–6초 `vx=1`, 6–10초 `(vx,vy)=(0.5,+0.3)`, 10–14초 `(0.5,−0.3)`, 14–17초 `(vx,yaw)=(0.5,+0.5)`, 17–20초 `(0.5,−0.5)`이며 **4/8/12/16초에 world-Y 방향 ±0.5m/s 속도 외란**이 있다. 영상 한 명의 동작을 camera-off 평가의 특정 episode와 동일 궤적으로 취급하지 않았다. 회전·횡이동 구간에서 월드 X 이동이 작다고 정체로 판정하지도 않았다.

## 3. 직접 재집계한 성능과 실패 집중도

### 3.1 Case별 행동·비용

아래 값은 **`evaluation/episodes.jsonl`의 각 case 384 episode 동일가중 산술평균**이다. `tracking`은 혼합 단위 내부 오차, `vx/vy`는 m/s 절대오차 평균, `yaw`는 rad/s 절대오차 평균, `body 전진`은 m, `stall`은 유효 명령 구간의 비율, `action Δ`는 기록된 action RMS 변화다. `world_dx/dy`는 임의 초기 yaw에서의 월드 변위이므로 전진 거리의 대체물이 아니다.

| Case | Tracking | vx 오차 | vy 오차 | yaw 오차 | Body 전진 m | Stall | Action Δ RMS |
|---|---:|---:|---:|---:|---:|---:|---:|
| H1 정지 | 0.09500 | 0.0201 | 0.0733 | 0.0473 | **0.282** (비의도) | 0.000 | 0.264 |
| H2 전진 | 0.13732 | 0.0398 | 0.0620 | 0.0994 | **15.297** | 0.005 | 0.442 |
| H3 횡왕복 | 0.10151 | 0.0228 | 0.0771 | 0.0511 | **0.276** (비의도 전진) | 0.010 | 0.293 |
| H4 전진+회전 | 0.13351 | 0.0346 | 0.0676 | 0.0939 | **10.439** | 0.006 | 0.367 |
| H5 rough | **0.19816** | **0.0969** | 0.0638 | **0.1303** | **8.769** | **0.0127** | 0.364 |
| H6 경사 상승 | 0.15838 | 0.0586 | 0.0562 | 0.1139 | **20.187** | 0.005 | **0.537** |
| H6 경사 하강 | 0.15779 | 0.0552 | 0.0585 | 0.1131 | **19.975** | 0.005 | **0.548** |
| H7 외란+전진 | 0.14589 | 0.0473 | 0.0714 | 0.0952 | **10.364** | 0.0053 | 0.361 |

- **분모·검산:** 전체 3,072행 episode-weighted tracking **0.140944**. 이번에는 8 case의 episode 수가 동일하여 **8 case 동일가중 평균도 0.140944**로 같지만, H6 상·하를 합친 **7 scenario 동일가중 평균은 0.138496**으로 다르다. `diagnostics.json`의 7개 scenario tracking/episode/survival은 `episodes.jsonl`로 재현된다(부동소수점 반올림 오차만 존재). 전체 survival 3,072/3,072은 **각 20초 timeout 생존**이라는 뜻이지 장애물 완주율이 아니다.
- **추종의 분해:** 전체 `xy_rmse=0.11757m/s`, `yaw_rmse=0.11474rad/s`; `mean_tracking_error`를 일괄 m/s로 표시하면 안 된다. rough의 오차는 단순 yaw 문제가 아니라 `vx_error=0.0969m/s` 및 최악 사례 `0.2682m/s`가 동반되어 실질적 전진 손실과 연결된다. H4는 목표에 yaw 부호 전환이 있으므로 `world_dx` 작음을 실패로 취급하지 않았다.
- **평지 제어가 개선됐어도 완전 정지는 아님:** H1 body 전진 **0.282m**, world XY **순변위 크기 평균 0.304m**, `roll_pitch_rms=0.0782`이다. H1 `stall=0`은 명령 XY 속력 ≥0.2m/s step이 없어서 정의상 0으로 기록된 것이지, 제자리 유지 성공 지표가 아니다. H3는 world XY 순변위 크기 평균 **0.167m**, `xy_rmse=0.0961m/s`, `yaw_rmse=0.0711rad/s`; 돌아온 최종 위치와 추종 오차를 함께 보아야 한다.
- **경사 움직임은 행동 비용이 큼:** H6 action Δ RMS **0.537/0.548**은 전체 평균 **0.397**보다 높다. 이는 제어 명령 변화의 지표이며 에너지·토크·foot sliding의 측정값이 아니다. `roll_pitch_rms`는 H6 상/하 **0.0505/0.0482**로 정지 H1(0.0782)보다 낮아, 큰 action 변화가 곧 자세 붕괴라는 근거도 없다.

### 3.2 Rough가 유일한 뚜렷한 하위 꼬리

H5 `rough` 384개 원자료에서 body 전진 **평균 8.769 / 중앙값 8.796 / P05 7.970 / 최소 4.845m**, tracking **평균 0.19816 / P95 0.23468 / 최대 0.33263**, stall **평균 0.0127 / P95 0.030 / 최대 0.386**이다. `forward_progress<9m`은 **258/384**, `<8m`은 **21/384**이며, 7개 cohort에서 `stall>0.05`이다. 반면 다른 case의 최대 episode tracking은 약 0.172 이하로서 rough 쪽에 불량 꼬리가 집중된다.

| H5 평가 seed | 128 episode 평균 전진 m | 평균 tracking | 전진 `<8m` 건수 | stall `>0.05` 건수 |
|---|---:|---:|---:|---:|
| 4201 | 8.802 | 0.19744 | 5 | 3 |
| 4202 | 8.772 | 0.19775 | 7 | 1 |
| 4203 | 8.734 | 0.19929 | 9 | 3 |

**실패 형태를 보여주는 두 cohort:** `H5-rough-s4201-e60-n0`은 진행 **4.8446m**, tracking **0.33263**, `vx_error=0.26817m/s`, stall **0.386**, `roll_pitch_rms=0.10261`인데도 `end_reason=timeout`이다. `H5-rough-s4203-e61-n0`도 진행 **5.8853m**, tracking **0.33212**, stall **0.123**이며 timeout이다. 첫 사례의 action Δ RMS **0.2989**는 rough 평균 0.3642보다 *낮다*. 따라서 지형 앞에서의 저속/정체와 자세 악화가 동반된다는 관찰은 강하지만, 관절 불안정·reward·발 끌림을 특정 원인으로 단정할 자료는 없다. 각 `seed`는 **평가 seed**이며 128개의 env를 독립 학습 seed로 취급하지 않는다.

현재 원자료에는 missing field가 없고 `episode_id` 중복 0, `(scenario,case,seed,env_id)` cohort 중복 0이다. **cohort 고정 20초 내 terminated 경험률도 0/3,072, 종료 횟수도 0**으로 episode 실패율과 일치한다(이번에는 reset 재시작이 없기 때문). 실패 episode를 삭제하거나 `base_contact_failure`의 null을 false로 메우는 처리도 없었다. `forward_progress_m`와 `integrated_body_forward_m`가 **행별 완전 동일**하므로 중복 근거로 세지 않았고, `lateral_drift_m`(H3 평균 1.543m)는 실제 월드 횡변위가 아니라 **횡속도 추종 절대오차의 시간 적분**이다.

### 3.3 보존된 이전 ACTRATE-0001 `model_2700`과의 *문서 기반 참고 비교*

기준 수치는 첨부 프로젝트 참고 문서 `06_HUMANOID_TRAINING_CODE.md`, `14_H1_NEXT_RUN_PARAMETER_COMPARISON.md`, `20_H1_PUBLIC_FAILURES_AND_EXPERIMENT_PRIORS.md`에 기록된 이전 **ACTRATE-0001 / `model_2700`** Windows PERSONAL `scenario7` 원자료 분석값이다. 이전 체크포인트는 `e54d3389…93ca7ae`로 기록되어 **이번 `a8249d…b84ea`와 다른 정책**이다. 당시에도 3,072 episode, 8 case·3 seed·128 env, 동일한 protocol ID로 보고되지만 이번에는 **그 기존 ZIP 바이트·전체 resolved 설정·대응 cohort를 직접 열어 재검증하지 않았다**. 또한 이번 ZIP의 명칭 `return2700`만으로 `model_2700`이 검증된 resume 부모라고 주장할 수 없다.

| 비교 항목 | 이전 `model_2700` (기존 분석 인용) | 이번 MODEL4650 (직접 재계산) | 변화 방향 |
|---|---:|---:|---|
| H1 정지 비의도 body 전진 | 1.987m | **0.282m** | **뚜렷한 감소** |
| H3 횡명령 중 비의도 body 전진 | 1.677m | **0.276m** | **뚜렷한 감소** |
| H2 전진 적분 | 15.326m | 15.297m | 사실상 비슷한 전진 규모 |
| H5 rough 평균 / P05 / 최소 전진 | 9.948 / 9.592 / 8.815m | **8.769 / 7.970 / 4.845m** | **평균·하위 꼬리 악화 신호** |
| H7 외란 전진 | 10.542m | 10.364m | 소폭 감소 |
| H6 상·하 전진 | 20.052 / 19.834m | 20.187 / 19.975m | 소폭 증가 |
| 전체 action Δ RMS | 0.45687 | 0.39707 | 평균 변화량 감소. 단, 이번 H6 하행은 0.548로 여전히 높음 |

**해석:** 정지·횡이동 leak의 감소는 작다고 지워버릴 수 없는 유리한 행동 신호다. 동시에 rough의 평균뿐 아니라 P05와 최저가 함께 나빠진 것도 중요하다. 다만 위 변화는 **시점별 원자료가 동일 물리 trajectory임을 검증한 짝비교가 아니며**, reward `action_rate_l2`나 resume 자체가 원인이라는 판단은 불가능하다. 이번 정책에 없는 과거 지표를 추정하여 채워 넣지도 않았다.

## 4. 6개 영상에 기록된 실제 행동 — 시간·프레임 근거

영상의 20초/1,000프레임 전체 구간에서 분산 시점과 초기 장애물 진입부의 더 촘촘한 시점을 확인했다. 아래는 **영상 단일 env에 대한 정성 판독**이며, 완전한 발 접촉 궤적·관절 측정·수치적 push 회복시간을 프레임 샘플만으로 만들지 않았다. `t=초, f=50×t`이다. 파란색/초록색 화살표는 명령/현재 속도 **debug marker**라서 이것을 몸통 기울기나 발이라고 오판하지 않았다.

| MP4 | 실제 프레임에서 보이는 행동 | 정량과 연결한 판단 |
|---|---|---|
| `01_stairs.mp4` | **0.5–3.0초(f25–150)** 전방 계단 띠에 접근하면서 계단 경계 부근을 지나고, **4–6초(f200–300)** 계단 패치는 화면 한쪽으로 멀어진다. **8–19.5초(f400–975)**에는 눈에 보이는 중앙 계단이 없고 보행 자세가 유지된다. | 넘어지지 않고 이동한 증거지만 **계단 중앙의 여러 단을 실제 연속 등·하강해 완주했다는 근거는 부족**하다. `scenario7`에 별도 계단 정량 case 없음. |
| `02_inverted_stairs.mp4` | **0.5–3초(f25–150)** 역계단 띠가 로봇의 옆(영상 왼쪽)에 보이는 동안 로봇이 이동하고, **4–7초(f200–350)** 계단이 뒤로 멀어진다. | **역계단 패치 주변 이동**은 보이나 중심부 반복 단차 통과 성공으로 승격할 수 없다. |
| `03_boxes.mp4` | **0.5–5초(f25–250)** 높낮이 다른 블록 사이/가장자리에서 발과 블록이 가까워지며 위치가 변한다. **11–18초(f550–900)**에도 블록 영역 근처에서 방향을 바꾸고 서 있는 자세가 관찰된다. 일부 큰 파랑/초록 형상은 몸통이 아니라 debug 화살표다. | **박스 밀집 환경에서 이동·직립 유지의 정성적 긍정 신호**. 그러나 블록마다 확실한 접지, foot sliding, 회복시간 또는 지형 전 구간 완주를 수치화할 근거는 아니다. boxes 대응 camera-off case도 없다. |
| `04_random_rough.mp4` | **0.4–4.5초(f20–225)** 울퉁불퉁한 패치 내부에서 로봇 위치가 변하며, **약 5초(f250)** 패치 경계 근처를 지나 **6–19.5초(f300–975)** 대부분 평지 쪽으로 이동한다. 명확한 전도 장면은 표본 프레임에서 보이지 않는다. | 영상 한 환경의 초기 rough 이동은 **가능**하지만 정량 H5에는 **20초 생존하면서 4.845m만 진행한 다른 cohort**가 있어 모순이 아니다. 영상 후반을 전부 험지 통과로 세면 안 된다. |
| `05_slope_up_10deg.mp4` | **0.4–4초(f20–200)** 완만한 표면에서 보행하며 자세를 유지하고 **6–19.5초(f300–975)** 이동 모습이 계속 보인다. 시점·바닥 명암만으로 등판 높이나 실제 경사 구간 체류를 계측하기 어렵다. | H6 **20.187m body 적분, 0 terminated**와 전진 능력의 방향은 일치. 이 적분만으로 ±10° 구간 전체를 20m 진행했다고 단정하지 않는다. |
| `06_slope_down_10deg.mp4` | **0.4–4초(f20–200)** 하행용 표면에서 자세를 유지하는 프레임이 보이고, **6–19.5초(f300–975)** 후반 명령 변경 뒤에도 화면상 전도 징후가 뚜렷하지 않다. | H6 하행 **19.975m body 적분**, 0 terminated와 부합. 그러나 하행의 action Δ RMS **0.548**은 높은 행동 비용 신호이며 영상만으로 foot slip을 부정할 수 없다. |

외란이 예약된 **4초(f200), 8초(f400), 12초(f600), 16초(f800)**와 인접 프레임을 확인했다. 표본상 즉각적인 장시간 전도 상태나 영상 중단은 관찰되지 않고, 정량 H7 역시 384/384 timeout, 평균 전진 10.364m와 낮은 stall을 기록한다. 이는 **외란을 받으면서 계속 움직이는 능력**을 지지하지만, push마다 몇 초 만에 자세·속도가 원상회복됐는지는 per-push 시계열 부재로 판정하지 않는다. 6초 이후의 횡명령, 14초 이후의 yaw 부호 전환에 따른 움직임을 전진 실패·정체로 해석하지 않았다.

**캡처 판정:** 6개 MP4의 **첫 프레임 f0은 검정**이나 모두 **f1–f10에서 가시 프레임**이다. f199–201, f399–401, f599–601, f799–801에 parity에 따른 반복 검정은 확인되지 않았다. 일부 영상의 마지막 **f999에는 로봇 메시 표시가 급변**하지만 f995–998에는 일반적인 모습이므로 단일 종단 렌더링/표시 artifact 가능성으로 분리했다. 이 프레임을 낙상으로 세지 않았다. 영상 파일 6개 모두 1920×1080, 50fps, 디코딩 가능한 1,000프레임으로 확인했다.

## 5. 해석 및 활용 경계

1. **성공이라고 할 수 있는 것:** 고정 evaluator의 전진·회전 복합·경사·push 조건에서 20초 안정적으로 움직이며 평균 목표 전진 적분에 대체로 근접한다. 정지/횡왕복에서 비의도 전진이 이전 참고 기록보다 작다. 이는 범용 점수나 계단 완주가 아닌 **해당 명령 추종·이동 목표에서의 성공**이다.
2. **실질적으로 위험한 것:** rough에서 큰 `vx_error`·높은 tracking·높은 stall·낮은 진행이 **동일한 실패 cohort에서 동반**된다. 전도 판정만으로 걸러지지 않으며, 특히 최소 진행을 요구하는 실제 경로에서는 장애가 될 수 있다. video 한 환경의 rough 통과 장면으로 이 분포 꼬리를 지울 수 없다.
3. **작거나 미확정인 것:** 이전 기록 대비 H2 전진 15.326↔15.297m 같은 차이는 주요 개선 증거로 삼기 어렵다. 별도 영상에는 pure H3 정지-횡왕복이나 제자리 H1 실험이 없으므로 그 행동은 원자료가 핵심 근거다. action Δ는 torque/energy/foot sliding이 아니며, 큰 marker 움직임을 몸통 진동으로 치환하지 않는다.
4. **비교의 인과 한계:** 이번 ZIP은 training checkpoint·reward·parent index·TensorBoard 자체를 포함하지 않는다. 외부 보존 문서의 이전 정책과 nominal protocol ID가 같아도, 평가 source/지형 설정·PPO·학습 lineage·실제 reset 후 trajectory를 이번에 재검증하지 않았으며 **정책 간 보상 변경 인과효과는 판정하지 않는다**. 모든 값은 Windows **PERSONAL 내부 진단**이며 공식 score 또는 제출 완료를 뜻하지 않는다.

**후보 채택 판단:** **HOLD.** 평지 위치 누수 개선과 전진 유지라는 방향은 좋다. 하지만 전지형 일반화의 가장 불리한 H5 tail이 이전 참고 정책보다 나빠진 신호가 크므로, **현재 기준 전지형 정책으로 채택하지 않는다**. 별도의 *평지 정지·횡이동 명령 추종 검증 후보*로는 보존할 가치가 있다.

## 6. 다음 행동 **한 가지**와 재확인 자료

**새 GPU 작업 대신, 이미 보존된 ACTRATE-0001 `model_2700`의 PERSONAL full `episodes.jsonl`·`resolved_configs.json`을 확보해 이번 MODEL4650과 `H5/rough` 중심으로 동일 `(scenario,case,seed,env_id)` cohort 키에서 직접 대응 재집계한다.** protocol·task/agent/source fingerprint, 지형 difficulty/seed·command·episode 20초·reset 조건이 비교 가능한지 먼저 표시한다. 이어 **H5 진행 P05/최악/`stall>0.05` 및 H1·H3 비의도 전진**을 동일 분모로 나란히 검증한다. 이것이 이번 HOLD를 유지할지, 용도 제한 PROMOTE 검토 가치가 있는지 판단하는 데 가장 직접적인 기존 자료 검증이다. 같은 cohort 키로 묶더라도 실제 물리 terrain·trajectory가 동일하다는 증명은 별도다. 새 학습·렌더·평가·export는 요청/실행하지 않았다.

**재확인 지점:** 이번 ZIP 안의 `source_checkpoint.txt`·`environment.txt`·`evaluation/evaluation_manifest.json`·`evaluation/video_evaluation_link.json`(identity), `evaluation/resolved_configs.json`·`evaluation/episodes.jsonl`·`evaluation/diagnostics.json`(case·seed·분모·원수치), `evaluation/evaluation.log`(종료 상태), 루트 **6개 원본 MP4**(위 파일명·시각/프레임), `README.txt`(영상 전역 command/push). 프로젝트 참고 기록은 `06_HUMANOID_TRAINING_CODE.md`, `14_H1_NEXT_RUN_PARAMETER_COMPARISON.md`, `20_H1_PUBLIC_FAILURES_AND_EXPERIMENT_PRIORS.md`의 ACTRATE-0001 `model_2700` 항목. **원본 ZIP·MP4·checkpoint·서버·학습 환경은 변경하지 않았다.**
