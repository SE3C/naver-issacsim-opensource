> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/incoming/other/reviewed/H1_LINTRACK-065_POLICY_ANALYSIS_20261015.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# H1 LINTRACK-065 / `model_4950` — 6지형 영상·camera-off 평가 통합 행동 분석

**분석일:** 2026-10-15 (KST)\
**자료:** `h1-lintrack-065-fresh5k_model_4950_h1_6terrain_evaluation_20261015-014027_cf736cea.zip` (원본 18개 항목).\
**범위:** 제공 ZIP 내부 원자료 3,072행 직접 재계산 및 MP4 6개 디코딩·다시점/장애물 근접 프레임 관찰. 다른 checkpoint에 대한 원본 ZIP은 이번 입력에 포함되지 않았다.

## 1. 결론 — **HOLD** (범용 주후보 채택 보류)

**실질적인 전진 보행은 성공했다. 그러나 범용 명령 제어·험지·계단까지 성공한 정책이라고 판단할 수는 없다.** 이 정책은 flat 전진(H2), 경사 ±10°(H6), 외란 조건(H7)에서 목표 속도 적분에 가까운 body-frame 전진량을 기록하고, 3,072개 20초 episode에서 접촉 종료 없이 생존했다. 영상에서도 거친 표면과 박스 구간의 초기 보행 및 외란 시간대를 지난 뒤 자세 유지가 관찰된다. 따라서 단순히 제자리에서 termination을 피하는 정책은 **아니다**.

반대로 **H3 횡이동 왕복 후 위치가 돌아오지 않는 현상**과 **H5 rough 전진 속도 추종의 체계적 손실**이 크다. H3 명령은 처음 10초 `vy=+0.3 m/s`, 다음 10초 `vy=-0.3 m/s`인데, 20초 종료 후 world XY 순변위의 **크기**는 평균 **3.102 m**(384/384개에서 3.050–3.146 m)이다. 부호 있는 `world_dx`/`world_dy`를 먼저 평균하면 임의 초기 yaw가 상쇄해 이 현상이 가려진다. 다만 이 평가의 명시적 목표는 **body-frame 속도 추종**이고 world-origin 복귀 제어가 아니다. 따라서 이것을 H3 episode 실패/낙상이라고 바꾸지 않는다. 대신 **왕복 위치 복귀·경로 재방문을 요하는 실제 응용에서 중요한 제어 약점**으로 판정한다. yaw-rate 절대오차 0.132 rad/s와의 연관은 가능한 설명이지만 원인을 확정할 step-level 궤적은 없다.

H5는 명령 `vx=0.5 m/s`의 20초 적분 목표 **10.0 m**에 대해 body-frame 평균 **8.995 m**, P05 **8.411 m**, 최소 **7.943 m**다. 384개 모두 10m 미만이고 360/384개가 9.5m 미만이다. **심한 stall 붕괴가 아니라, 계속 걸으면서 속도를 충분히 못 내는 유형**이다(stall 최대 0.039, stall>0.05 0/384). 혼합 tracking error도 H5 **0.21854**로 8개 case 중 가장 높다.

**종합 방향:** 전진·정지 위치 유지 측면에선 검토할 만한 **제한적 보행 후보**다. 하지만 **범용 최종 대표 정책으로 PROMOTE하지 않고 HOLD**한다. 특히 중앙 계단의 연속 단차 통과 성공은 이번 6영상에 의해 입증되지 않는다. **REJECT는 하지 않는다**—전진·경사·push 조건에서 이미 유의미한 움직임이 측정됐기 때문이다. 여기서의 HOLD는 공식 제출 여부나 reward 가설 판정이 아닌 **이번 입력의 정책 후보 결정**이다.

## 2. 정책 식별과 평가 조건

| 항목 | 확인된 값 |
|---|---|
| 표시명 | **LINTRACK-065** (제공 ZIP의 구분명; 학습 reward 적용값 자체는 입증하지 않음) |
| 로봇·checkpoint | H1 / `model_4950.pt` |
| checkpoint SHA-256 | `b7528923eef5b1368ba2299f4e0538804ba00dd358049bfdff5027f448e31ece` |
| identity 연결 | `source_checkpoint.txt` = `BUNDLE_README.txt` = `evaluation/video_evaluation_link.json` = `evaluation_manifest.json` = **전체 episode의 `policy_sha256`** |
| 학습 provenance | ZIP `policy.source_run_id=null`, `preset=null`. `fresh5k`/Run처럼 보이는 경로명만으로 학습 완료·부모·OFFICIAL 출처를 판정하지 않음. 원 checkpoint `.pt`는 ZIP에 없어 그 바이트를 재해시할 수 없음 |
| 평가 상태 | **PERSONAL**, `execution_status=COMPLETE`, `complete=true`, `smoke=false`, child exit 0; official_score=`false` |
| 평가 | `scenario7`, 7 scenario / **8 case**, seed **4201·4202·4203**, 각 case×seed당 128 env, **3,072 cohort/3,072 raw episode**, 20초·1,000 step, deterministic inference |
| 프로토콜 | `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34` |
| 환경·출처 | Windows PERSONAL GPU RTX 3060 Laptop. `resolved_configs.json`에 24개 case×seed 환경설정; `source_fingerprints`, agent fingerprint, applied-environment fingerprints 존재 |
| 영상 | 단일 env/seed **42**, H1 `maneuver_push`, 6종 1,000프레임·50 fps·20초; 경사 **±10°**, `terrain_seed=42`, noise off, 초기 x/y/yaw=0. 평가와 다른 명령 및 지형/리셋 실행 |

**분모·무결성 직접 확인:** ZIP 18개 항목 CRC 검사 정상, `SHA256SUMS.txt`의 **MP4 6/6 일치**; 나머지 항목은 ZIP CRC로 점검. `episodes.jsonl`에 필드 누락 0, 중복 `episode_id` 0, 3,072개 고유 `(scenario, case, seed, env_id)`의 각 1개 episode만 존재한다. 모든 행 1,000step/20.0s, `end_reason=timeout`, `survived=true`, `base_contact_failure=false`다. 따라서 **episode 생존 3,072/3,072**, **한 번 이상 terminated된 cohort 0/3,072**, 재시작으로 인한 중복 가중 없음. `diagnostics.json`의 scenario별 행 수/episode tracking 평균/생존률은 직접 재집계와 일치했다. 로그에서 최종 `COMPLETE`·`[CHILD EXIT] 0` 확인. 심각한 실행 오류는 기록되지 않았다.

**평가 조건의 실제 차이:** H1 balance=0속도, H2는 앞 10초 `vx=.5` 뒤 10초 `vx=1`, H3는 `vy=±.3`, H4는 `vx=.5` 및 `yaw-rate=±.5`, H5 rough는 `vx=.5`, H6 slope up/down은 각각 `vx=1`, H7 flat push는 `vx=.5`와 정해진 외란이다. H1/H2/H3/H4/H7은 평지이며 **stairs/boxes에 대응하는 camera-off case는 없다**. 평가 reset yaw 범위는 ±3.14 rad로 영상의 초기 yaw=0과 달라, world 방향의 부호 있는 평균을 진행 지표로 사용하지 않았다. 관찰 noise 및 추가 질량/마찰 event는 resolved 설정에서 비활성이고, seed별 적용 terrain fingerprint는 다르다. `source_fingerprints`는 평가 시 task 파일의 기록이지 OFFICIAL 학습 코드의 byte-identical 증명은 아니다.

## 3. 정량 분석 — episode 원자료에서 재집계

아래는 **각 case 내 384 episode의 단순 행 평균**이다. 8개 case가 모두 384행이어서 전체 episode 평균과 case 동일가중 평균은 이번 입력에서는 같다. `mean_tracking_error`는 `sqrt(Δvx²+Δvy²+Δyaw²)`의 step별 episode 평균(서로 다른 단위를 합친 **무단위 표기 내부 혼합량**); 축별 오차는 절댓값 평균(`vx`·`vy`는 m/s, `yaw`는 rad/s). *body 전진*은 `forward_progress_m`이며 `integrated_body_forward_m`와 **전체 3,072행에서 정확히 동일**하므로 독립 근거가 아니다. stall은 유효 이동 명령 step 기준의 비율이다.

| Case (384개씩) | 혼합 tracking ↓ | vx 절대오차 ↓ | vy 절대오차 ↓ | yaw 절대오차 ↓ | body 전진 (m) | stall (%) | action Δ RMS ↓ |
|---|---:|---:|---:|---:|---:|---:|---:|
| H1 정지 | 0.15717 | 0.01612 | 0.05544 | 0.13477 | **+0.063** (목표 0) | 0.000¹ | 0.34797 |
| H2 전진 | 0.17786 | 0.03054 | 0.06210 | 0.14777 | **15.088** (명령 적분 15) | 0.500 | 0.34967 |
| H3 횡왕복 | 0.15848 | 0.01812 | 0.06134 | 0.13215 | **+0.173** (비의도 전진) | 0.952 | 0.33840 |
| H4 전진+회전 | 0.17510 | 0.02357 | 0.05900 | 0.14890 | **10.093** (전진명령 적분 10) | 0.400 | **0.30618** |
| H5 거친 지형 | **0.21854** | **0.07888** | 0.05753 | **0.16988** | **8.995** (명령 적분 10) | 0.738 | 0.35332 |
| H6 상행 10° | 0.18570 | 0.04774 | 0.06226 | 0.14812 | **20.176** (명령 적분 20) | 0.600 | 0.42976 |
| H6 하행 10° | 0.18704 | 0.04835 | 0.06348 | 0.14796 | **19.989** (명령 적분 20) | 0.600 | **0.45173** |
| H7 push | 0.17961 | 0.03275 | 0.06551 | 0.14489 | **10.046** (명령 적분 10) | 0.513 | 0.32032 |

¹ **H1은 명령 속도가 0이므로 stall 유효 분모가 없다.** evaluator의 0은 정지 성공률이 아니며, 정지 유지의 적합성은 `world displacement`, `vx/vy`, yaw를 함께 판정했다. **전체 혼합 tracking 행 평균=0.17994**, 전체 `xy_rmse`=0.10291 m/s, `yaw_rmse`=0.17668 rad/s, `roll_pitch_rms`=0.08379 rad, `action_delta_rms`=0.36217. `xy_rmse`/`yaw_rmse`는 위 절대오차의 다른 집계법이므로 교환하지 않는다. **실제로 foot sliding·foot air time·관절 deviation은 이 평가의 기록 필드가 없어 정량 비교할 수 없다.**

### 목표별 강점과 그 반대 증거

**정지(H1):** 20초 전체 body 전진 적분은 +0.063m로 매우 작고, 세계좌표 순변위 크기 `hypot(world_dx_m,world_dy_m)` 평균 **0.171m**, P95 **0.175m**다. `world_dx` 평균 +0.009m와 `world_dy` +0.006m만 보고 실제 거의 0이라고 판단하지 않았다. 정지 위치는 잘 지키지만 yaw 절대오차 0.13477rad/s, roll/pitch RMS 0.08648rad는 별도 흔들림·회전 비용이다. 즉 **위치 유지와 완전한 자세/방향 고정은 다른 성능**이다.

**직진·경사·외란(H2/H6/H7):** H2 평균 15.088m, H6 상/하 20.176/19.989m, H7 10.046m는 각각 command 적분 15/20/10m와 가깝고 stall이 1% 미만이라 **실제 이동의 강한 증거**다. H7 전진 완료는 네 차례 고정 push 조건에서 지속 보행한 사실이지만, episode 집계에는 **push 후 몇 초에 회복했는지**가 없어 '즉시 회복'을 입증하지 못한다. H7의 월드 XY 순변위 크기는 평균 **9.205m**로 body 전진 10.046m와 다르다—방향/횡방향 손실을 포함한 경로 추적 정확도는 단순 전진 적분만으로 보증되지 않는다. 경사에서는 하행 action Δ RMS **0.45173**, 상행 **0.42976**으로 하행에서 동작 변화량이 크다. 큰 차이가 아니라도 **속도 추종만 보면 놓치는 비용**이다.

**횡왕복(H3):** `vy_error=0.06134m/s`, `xy_rmse=0.07895m/s`, stall 평균 **0.00952**, contact 종료 0이고 전방 누수도 +0.173m로 작다. 단순 속도 추종 수치만 보면 H3는 양호하다. 그러나 **world XY 최종 순변위 평균 3.102m, 중앙값 3.103m, P95 3.127m**, 세 seed별 평균 **3.103/3.100/3.101m**로 일관된다. signed world X/Y 평균(-0.035/+0.187m)과 완전히 다른 결론이다. 명령은 몸체 기준이고 heading 제어가 꺼져 있으므로 *좌우 제어 자체가 전혀 안 된다*거나 *월드 좌표 복귀가 evaluator 합격 기준*이라고 말하지 않는다. **실제 궤적 복귀를 원하는 응용에는 명백한 미해결 위험**이며, yaw drift·lateral velocity 적분 오차 기여 분해는 step time series가 필요하다.

**rough(H5):** 추종 평균 **0.21854**, P95 **0.24279**, 최대 **0.26450**. 전진 평균 **8.9946m**, P05 **8.4107m**, 최소 **7.9428m** (`seed=4203, env=80`, mixed tracking **0.2551**, stall **0.023**). 진행이 느린 최하위 사례가 있는 반면 **stall>0.05는 0/384**, 최대 0.039다. `seed=4202, env=18`은 진행 **7.990m**, mixed tracking **0.2626**, stall **0.023**이다. 즉 낙상/장시간 정체가 아니라 **앞으로 계속 걸어도 목표 속도가 모자라는 worst tail**이다. 비교적 낮은 H5 roll/pitch RMS **0.06518rad**는 몸통이 정렬되어 있다는 신호일 수 있으나 **진행 성능이 좋아졌다는 뜻이 아니다**.

### seed·분포 검증

| 관찰축 | seed 4201 | seed 4202 | seed 4203 | 해석 |
|---|---:|---:|---:|---|
| H5 평균 전진 (m) | 8.967 | 9.048 | 8.969 | 세 평가 seed 모두 10m 미만. 4202가 상대적으로 우수하지만 위약한 격차 |
| H5 평균 mixed tracking | 0.2194 | 0.2165 | 0.2197 | H5 약점은 단일 seed만의 실패가 아님 |
| H3 평균 월드 순변위 크기 (m) | 3.103 | 3.100 | 3.101 | 회귀 잔류도 재현됨 |

H5 전진 `<8.5m` **27/384**, `<9.0m` **195/384**, `<9.5m` **360/384**. H5 진행 P95=**9.565m**, 최댓값 **9.795m**로 양호한 사례도 목표 10m에 소폭 미달한다. 서로 다른 env 128개×평가 seed 3개는 **384개의 초기조건/환경 관측**이지 독립 **학습** seed 384개가 아니다. 특별한 통계적 우월성, p-value 또는 공식 환산점수는 계산하지 않았다.

## 4. 여섯 MP4의 실제 시각 행동 (각 50fps/20초)

**읽은 구간:** 각 영상 0–19초를 매초 인접 parity와 함께 확인했으며, 0–4초 전후 장애물 접촉을 추가로 약 **0.4초 간격**으로 확인했다. 렌더 프레임의 신체·지형 상대 위치와 발 교대 자세를 따라갔고, 추적 카메라의 화면상 고정 위치를 정체 증거로 쓰지 않았다. 시각 판단은 한 env의 영상이다. 명령은 공통으로 **0–6초** `vx=1`, **6–10초** `vx=.5,vy=+.3`, **10–14초** `vx=.5,vy=-.3`, **14–17초** `vx=.5,yaw=+.5`, **17–20초** `vx=.5,yaw=-.5`; **4·8·12·16초**에 world-Y 방향 ±0.5m/s 속도 impulse. 이 *global video clock*은 평가의 *case별 episode clock*과 다르다. 6–20초에 줄어드는 화면상 전진이나 방향 변화는 명령 변경과 함께 읽어야 한다.

| 파일 / 시각·프레임 | 관찰과 판정 | 정량 연결 |
|---|---|---|
| **`01_stairs.mp4`**: 0.02s/f1 → 2.42s/f121 → 3.22s/f161 → 5.02s/f251 | 직립 자세로 교대로 발을 내딛고 계단 줄무늬의 **측면 경계**를 따라 지나간다. 계단 줄무늬가 화면 왼쪽 뒤로 물러나지만 **중앙 여러 단을 순서대로 밟아 통과하는 장면은 확인되지 않음**. 5초 이후 대부분 평탄부 보행. | 계단 camera-off case 없음. 낙상 없는 영상 ≠ 다단 계단 통과율. |
| **`02_inverted_stairs.mp4`**: 0.02s/f1 → 1.62s/f81 → 3.62s/f181 → 5.02s/f251 | 역계단 줄무늬 바로 옆에서 연속 발 교대와 앞으로 진행하는 모습. 계단 본체를 중심으로 내딛는 안정적 **연속 하강·상승 완료를 확증하지 못함**. 이후 주로 평탄부. | 역계단 camera-off case 없음; H6 slope 생존으로 대체할 수 없음. |
| **`03_boxes.mp4`**: **1.00s/f50, 2.20s/f110, 3.80s/f190, 4.60s/f230** | **실제 높이가 다른 box 주변/위에 발을 짚고 직립한 채 앞으로 이동**, 4–5초 무렵 패치에서 빠져나와 이후 평지에서 보행한다. 적어도 초기 구간은 단순 제자리 생존이 아니다. 발 걸림 직후 미세한 접지·sliding 크기를 화상만으로 계측할 수는 없음. | 별도 정량 box case 없음. 첫 몇 초의 이동을 20초 전구간 박스 통과 능력으로 확장하지 않음. |
| **`04_random_rough.mp4`**: 0.02s/f1 → 2.42s/f121 → 3.62s/f181 → 4.02s/f201 → 7.02s/f351 | 초기 거친 패치에서 발 교대·전진하며 넘어지지 않고 가장자리로 나가는 모습; 대략 4초 전후 패치 종료, 이후 평탄 지면. 촬영에서 명백한 장시간 뻗음·전도는 없음. | H5 다수 환경에서도 낙상 0, **진행 8.995/10m**로 **저속 추종 손실**. 영상의 4초 rough 접촉과 camera-off 20초 rough case를 같은 episode로 해석하지 않음. |
| **`05_slope_up_10deg.mp4`**: 0.02s/f1 → 2.02s/f101 → 4.02s/f201 → 8.02s/f401 → 16.02s/f801 | 전진 발 교대, 넘어지지 않고 이후 횡이동/회전이 섞인 전진을 지속한다. 높낮이/경사 경계가 화면에서 희미하여 영상만으로 특정 수직 획득 고도·완주 거리를 확정할 수 없음. | H6 **상행** body 적분 **20.176m**, action Δ **0.42976**는 별도 camera-off에서 얻은 값. |
| **`06_slope_down_10deg.mp4`**: 0.02s/f1 → 2.02s/f101 → 4.02s/f201 → 8.02s/f401 → 16.02s/f801 | 하행 template에서도 연속적인 직립 보행을 이어감. global push와 명령 전환 구간을 지난 뒤에도 화면에서 전도/정지 상태는 관찰되지 않음. 복구 시간·발 미끄러짐은 계측 불가. | H6 **하행** body 적분 **19.989m**, action Δ **0.45173**; 상행보다 동작 변화가 큰 비용 신호. |

**capture 결함을 분리 확인:** 여섯 파일 전 프레임을 낮은 해상도 명도로 검사했다. `03_boxes.mp4`는 **1,000프레임 중 501개 검정**(f0 및 홀수 frame 500개), 나머지 짝수 f2·f50·f100·f190·f230 등은 정상적으로 로봇·박스를 보여준다. **정책 실패/박스 낙상이 아니라 교대 캡처 artifact**다. 나머지 다섯 파일에서는 **f0 한 프레임만 검정**, 후속 프레임은 정상. 따라서 `03_boxes`에서 `f1, f51, f101…`만 샘플링한 결과를 ‘영상 전체가 검정’이라고 결론 내릴 수 없다. 원본 재렌더·교체는 수행하지 않았다.

**관찰-수치의 접점:** 박스·rough의 앞부분에서 실제 전진과 두 발 보행이 확인되므로 높은 timeout을 '제자리 생존'으로만 보는 해석은 틀리다. 동시에 H5 평가에서 측정된 **지속적 10–20% 수준의 진행 부족 사례**는 초반 rough 영상의 넘어지지 않는 모습과 충돌하지 않는다—서로 다른 seed·지형 타일·명령 스케줄의 실험이기 때문이다. 여섯 영상 중 H3 **정지/순수 lateral 왕복 case는 아예 없으므로** H3의 3.10m 종료 위치 잔류를 영상으로 보았다고 서술하지 않는다. H7도 이 여섯 global push 영상이 동일 H7 case가 아니므로 **응답 지연**은 판단하지 않았다.

## 5. 비교 정책 및 최종 활용 범위

이번에는 **LINTRACK-065 ZIP 한 개만 직접 재집계·영상 검증**했다. 프로젝트에서 제공된 기존 문서(`06_HUMANOID_TRAINING_CODE.md`, `14_H1_NEXT_RUN_PARAMETER_COMPARISON.md`, `21_WINDOWS_GO2_VIDEO_AND_EVALUATION.md`)에는 **이전** Windows PERSONAL 같은 계열 평가의 재집계 결과가 요약돼 있다. *아래는 그 과거 보고서의 숫자를 별도 인용한 참고값이지, 이번에 해당 ZIP을 열어 같은 resolved config/source/cohort를 대응 검증한 결과가 아니다.* `source_run_id`/학습 reward 계보를 임의로 연결하지 않는다.

| 지표 | **이번 LINTRACK-065** (원자료 직접 계산) | 과거 TERM-50 `model_2800` (기존 보고서) | 과거 ORIENT-100 `model_2850` (기존 보고서) | 과거 ACTRATE-0001 `model_2700` (기존 보고서) |
|---|---:|---:|---:|---:|
| H1 정지 중 비의도 body 전진 (m, 작을수록 좋음) | **0.063** | 1.352 | 1.633 | 1.987 |
| H5 rough body 평균 진행 (m, 클수록 좋음) | 8.995 | 8.896 | 9.451 | 9.948 |
| 8 case 전체 episode 혼합 tracking (작을수록 좋음) | **0.17994** | 0.15712 | 0.14041 | 0.14534 |

**조건부 해석:** 기존 요약대로 평가 정의와 명령이 실질적으로 같았다면, LINTRACK-065는 **정지 시 비의도 body 전진을 큰 폭으로 줄인 대신, rough 전진에서 ACTRATE/ORIENT보다 느리고 전체 혼합 추종도 상대적으로 나쁜** 방향이다. 그러나 이번 보고서는 **과거 ZIP들의 resolved 설정 바이트·source fingerprint·정확한 episode 배열 일치를 다시 확인하지 않았으므로** 이를 통제된 A/B 결과나 reward `track_lin_vel_xy_exp` 변경의 인과효과라고 쓰지 않는다. 특히 ‘정지 누수 개선’과 ‘H3 월드 왕복 위치 복귀’는 다른 성공 기준이며 후자가 자동 해결된 것은 아니다. **현재 자료만으로 다른 정책보다 범용 우승자라는 판정은 불가**하다.

**용도별 결정:**
- **정지·전진 중심 정책의 내부 후보로는 보존:** 정지 H1 body 누수가 작고 H2/H6/H7에서 충분한 실질 진행을 보여 재검토 가치가 있다.
- **횡왕복 위치 복귀·rough 속도 유지·계단 중심 범용 대표로는 HOLD:** H3 위치 잔류, H5 전반적 under-tracking, stairs/inverted stairs 중앙 다단 주행의 미입증이 직접적인 판단 근거다.
- **'회복 정책으로 검증 완료'라고 부르지 않음:** 고정 외란 후 20초 생존/지속 이동은 긍정적이나 상세 transient 회복 시간이나 넘어졌다가 일어나는 recovery 기전은 측정되지 않았다.

## 6. 다음 행동 **한 가지**와 재확인 경로

**추가 GPU 사용 전에, 기존에 보존된 TERM-50 `model_2800`의 `scenario7` 원본 ZIP과 이번 `episodes.jsonl`을 CPU에서 짝지어 재집계하는 것**을 1순위로 추천한다. `protocol_id`뿐 아니라 `resolved_configs`의 실제 명령·noise/randomization·terrain case, 평가 task/agent/source fingerprint, 20초 시간창, `(scenario,case,seed,env_id)`의 대응 여부를 확인한다. 호환되면 **H1 world 순변위·body 누수, H3 body `vy` 추종과 world 순변위, H5 P05/worst/평균 진행·tracking, H6 yaw/action 비용**을 함께 비교한다. **정지 개선이 rough·yaw·횡왕복 비용을 정당화하는가**가 다음 채택 결정을 바꿀 질문이다. 원본이 확보되지 않거나 setting parity가 깨지면 비대응 참고 비교로만 남기고 본 정책 HOLD를 유지한다. **새 학습·GPU 평가·영상 렌더·export·서버 조작은 실행하지 않았다.**

**이번 결론을 ZIP에서 재현할 최소 파일:**

1. `source_checkpoint.txt`, `BUNDLE_README.txt`, `evaluation/evaluation_manifest.json`, `evaluation/video_evaluation_link.json` — checkpoint SHA, 출처 공백, 평가/영상 identity·프로토콜.
2. `evaluation/resolved_configs.json` — 24개 case×seed 실제 설정, random yaw reset, terrain·명령·noise 및 fingerprints.
3. `evaluation/episodes.jsonl` — case별 384행, H3 `hypot(world_dx_m, world_dy_m)` **행별 계산 후 평균**, H5 분위수·seed·worst, H1 world displacement, 종료/코호트 재집계.
4. `evaluation/diagnostics.json`, `evaluation/evaluation.log` — 재현된 scenario 요약과 완료/child exit 확인.
5. 루트 6 MP4, `environment.txt`, `README.txt`, `SHA256SUMS.txt` — f/50초 영상 명령 타임라인·정상/검정 parity·정성 행동 확인.

**판단 범위:** 원 checkpoint 바이너리/학습 로그가 없는 ZIP의 SHA 기록은 평가와 영상의 *기록상 동일 checkpoint* 연결이다. 학습 reward 실제 변경·fresh/resume 계보·공식 서버 사용·훈련 중 성능 개선·공식 제출 및 NCRC score에 대한 별도 증명은 아니다. 따라서 **정량 행동과 영상 강약에는 결론을 내리고, 학습 원인·공식 성적에는 결론을 내리지 않는다.**
