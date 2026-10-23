> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/incoming/other/reviewed/H1_ACTRATE0002_MODEL2950_POLICY_ANALYSIS_20261017/H1_ACTRATE0002_MODEL2950_POLICY_ANALYSIS_20261017.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# H1 ACTRATE0002 / model_2950 — 6영상·camera-off 정책 심층 분석

- **판정일:** 2026-10-17 (KST) · **정책 판단: HOLD** · **분석 목적:** H1 공식 7시나리오의 후보 경쟁력을 우선 판단하고, 계단·박스 등의 보조 보행 능력을 따로 검토.
- **분석 입력:** `20261016-150803-h1-actrate0002-fresh3k_model_2950_h1_6terrain_evaluation_20261017-020342_54af98b1.zip` (원 ZIP SHA-256 `f658b2217737e5271caaf4eaa3c0ac48f29d1929d680a1688da509a0d87b3c3c`). 원본 입력은 수정하지 않았다.
- **판정 범위:** ZIP 내 한 정책의 Windows **PERSONAL** 평가와 6영상. 다른 정책의 원 episode/동조건 ZIP은 이 입력에 없으므로 A/B 우열이나 공식 점수 개선은 판단하지 않는다.

## 1. 핵심 결론

**유용하게 전진하고 20초 동안 서서 이동하는 정책이지만, 전 시나리오 대표·공식 제출 우선 후보로는 아직 승격하지 않는다(HOLD).** 정량적으로 H2 전진은 명령 body-vx 적분 15m 대비 실제 14.60m, H6 경사 상행/하행은 각각 20m 대비 19.78m/19.66m로 안정적인 진행 신호가 있다. H7 밀침 case도 평균 전진 10.12m와 timeout 384/384이다. 영상에서는 boxes·rough 구간에서 로봇이 실제 위치를 바꾸며 이동한다.

반대로 **정지 H1은 0속도 명령인데 평균 body 전진 적분 1.842m, 종료 world XY 순변위 1.835m**이다. 이는 제자리 균형의 위치 유지 실패다. H3 순수 횡이동 왕복에서도 **원치 않는 body 전진 적분 1.225m, world XY 종료 순변위 1.046m**로 제자리/측면 제어 비용이 크다. H5 rough는 평균 8.941m/20초로 명령 적분 10m보다 뒤처지며, 최악 6.983m와 stall >0.05인 3/384 cohort가 존재한다. 따라서 **“생존 100%”는 “목표를 잘 수행함”과 동의어가 아니다.**

- **성공한 축:** H2/H6/H7의 지속 전진, 8개 평가 case의 20초 생존, 영상의 일부 rough·boxes 통과와 여러 command/push 전환 뒤 서 있는 모습.
- **부족한 축:** H1 정지 유지, H3 횡왕복의 의도치 않은 전진/종료 잔류, H5 일부 환경의 진행·stall 하위 꼬리. 회전 H4는 주행과 yaw를 결합하므로 world XY 순변위만으로 실패로 판정하지 않음.
- **추천 범위:** 전진·경사 움직임의 **보존 가치가 있는 연구 후보**. 공식 제출용 범용 대표 정책 선정은 **HOLD**. 계단 **중앙 다단 완주** 및 박스 **20초 전 구간 완주**는 별도로 입증되지 않았다. 한 정책 자료이므로 특정 과거 정책보다 나아졌다는 주장은 하지 않는다.

명령 적분 대비 실제 body 전진 거리〔원본 참조: `figures/body_progress_vs_command.png` / 공개 사본 미포함〕

## 2. 정책 identity·평가 조건

| 항목 | 첨부 ZIP에서 확인한 내용 |
|---|---|
| 로봇·표시명 | H1 · `ACTRATE0002/model_2950` (**파일명 기반 식별 라벨**, 학습 reward 실측값 아님) |
| checkpoint SHA-256 | `eaa7a50c51fbdf3b39c15fe4278d1c9def38f96e9af872eb37111b66ac4d34fb` |
| 영상↔평가 연결 | `source_checkpoint.txt`, `evaluation/video_evaluation_link.json`, `evaluation/evaluation_manifest.json` 내 SHA가 **동일**. staged checkpoint 원본은 ZIP에 없어 bytes 재해시 불가 |
| 평가 상태 | `complete=true`, `execution_status=COMPLETE`, `smoke=false`; `official_score=false` |
| 평가 계약 | H1 `scenario7`, protocol `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34` |
| 분모 | 3 seeds `4201/4202/4203` × 128 env × 8 `(scenario,case)` = **3,072 최초 cohort**, episode 3,072행, 7 scenario(경사 상/하 별도) |
| 시간·행동 | episode당 1,000 control step, 20s; deterministic inference; 10s마다 per-episode command 전환. source fingerprint 및 applied per-case/seed config 해시 기록됨 |
| 입력 출처 | PERSONAL Windows camera-off camera disabled, NVIDIA RTX 3060 Laptop; 영상과 별도 실행. training `source_run_id=null`, `preset=null` |

`resolved_configs.json`과 manifest에서 H1/H2/H3/H4 평지, H5 random_rough, H6 `slope_up`·`slope_down`(파라미터 0.17632698 ≈ 10° 설정), H7 평지 외란을 구별했다. 명령은 H1 정지 `(0,0,0)`, H2 전진 `(0.5→1.0,0,0)`, H3 횡왕복 `(0,+0.3→-0.3,0)`, H4 전진+회전 `(0.5,0,+0.5→-0.5)`, H5 `(0.5,0,0)`, H6 `(1,0,0)`, H7 `(0.5,0,0)`이며 각 화살표는 10초 구간 전환이다. 정량 목표 거리는 **지형 완주 거리**가 아니라 명령 **body-vx 적분**의 참고치다.

평가에서 policy 관측 `enable_corruption=false`라 관측 항목에 정의된 noise 범위를 실제 주입으로 해석하지 않는다. resolved 이벤트의 mass/material/push 등 도메인 랜덤화 항목은 `null`, reset pose는 seeded random pose range이며 evaluator의 H7 외란은 별도 고정 시간표다. 영상은 seed42/1env/20s, 전역 command 일정과 밀침(4·8·12·16s)이므로 camera-off 3seed×128env episode와 동일 궤적이 아니다. 영상 command 세부는 §4 참조.

**중요한 provenance 주의:** 평가 `resolved_configs.json`의 reward `action_rate_l2.weight`는 `-0.0005`로 적혀 있다. 그러나 이 값은 **평가 환경 snapshot**이고 파일명 `actrate0002`가 암시하는 **학습 reward**의 검증 근거가 아니다. 마찬가지로 평가 agent `max_iterations=5000`은 학습 5K를 증명하지 않는다. 실제 학습 reward/fresh3K/부모·Run 연결은 이 ZIP만으로 확정할 수 없으며, 이를 이유로 위 행동 결과 자체를 버리지는 않는다.

## 3. 원 episode 재집계 — 성능과 실패 집중

아래 표는 `evaluation/episodes.jsonl`에서 직접 계산한 **case별 384 episode 동일가중 산술평균**이다. H6만 상/하 384행씩이다. `progress`는 **실제 body 기준 전진속도 적분**, `XY 순변위`는 **시작→종료 world 좌표 벡터 크기 평균**이다. `tracking`은 `(vx,vy,yaw-rate)` 순간 오차 Euclidean 크기의 episode 평균(서로 다른 단위 혼합, 단일 물리 단위 없음). 낮을수록 좋다.

| case / 명령 | tracking ↓ | vx abs.err ↓ m/s | vy abs.err ↓ m/s | yaw abs.err ↓ rad/s | body 전진 ↑ m | world XY 순변위 m | stall 평균 | roll/pitch RMS rad | action Δ RMS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| H1 정지 | .1160 | .0922 | .0398 | .0392 | **1.842** | **1.835** | .0000* | .0487 | .3065 |
| H2 전진 | .1610 | .0378 | .0803 | .1151 | **14.599** | 12.784 | .0070 | .0443 | .4870 |
| H3 횡왕복 | .1406 | .0688 | .0779 | .0672 | **1.225** | **1.046** | .0101 | .0406 | .3591 |
| H4 회전+전진 | .1432 | .0227 | .0749 | .1059 | **10.084** | 3.055† | .0060 | .0384 | .4007 |
| H5 rough | .1757 | .0711 | .0724 | .1180 | **8.941** | 8.430 | .0093 | .0326 | .3977 |
| H6 경사 상행 | .1755 | .0428 | .0827 | .1268 | **19.775** | 16.995 | .0080 | .0534 | .5522 |
| H6 경사 하행 | .1761 | .0435 | .0839 | .1266 | **19.661** | 16.919 | .0080 | .0535 | .5550 |
| H7 외란+전진 | .1484 | .0371 | .0780 | .0997 | **10.115** | 9.315 | .0074 | .0367 | .4092 |

\* H1 정지에서는 stall 판별의 명령 크기 분모가 없어 0으로 기록된다. **stall=0은 제자리 유지 성공이 아니다.**  † H4는 10초마다 yaw 방향이 전환되는 곡선 이동이다. world X/최종 XY만으로 “진행 부족”이라 해석할 수 없다. `integrated_body_forward_m`은 `forward_progress_m`과 전 행이 같아 중복 독립 지표로 세지 않았다. `lateral_drift_m`은 실제 월드 횡위치 변화가 아니라 `|vy_error|` 적분이므로 본 표에 별도 횡변위로 넣지 않았다.

**집계 재현:** 3,072행 모두 `steps=1000`, `duration_s=20`, `end_reason=timeout`, `survived=true`, `base_contact_failure=false`. episode ID 중복 0; 서로 다른 `(scenario,case,seed,env_id)` 3,072개; cohort 중 terminated 발생 **0/3,072**. 따라서 이번 자료에서는 episode 생존 3,072/3,072와 최초 cohort의 무종료 3,072/3,072가 우연히 같지만 일반적으로는 서로 다른 분모다. `diagnostics.json`의 H1~H7 tracking 평균/건수/생존과 episode 재집계가 모두 수치 오차 수준 내 일치한다. 전체 **episode 가중 tracking 평균 0.154570**, **scenario 7개 동일 가중 평균 0.151535**로 다르다. 이번 8개 case는 행 수가 모두 384이므로 case 동일가중 평균과 episode 가중 평균은 같다. 공식 점수로 환산하지 않았다.

### 중요한 하위 꼬리와 seed 검토

1. **H1의 실패는 희귀 꼬리가 아닌 광범위한 제자리 drift다.** world XY 순변위 **P05/중앙값/P95 = 1.820/1.835/1.851m**, body 전진 최소 1.814m. 3개 평가 seed의 평균 전진도 각각 **1.841/1.842/1.843m**로 사실상 모두 이동한다. H1 tracking .116이 상대적으로 작다는 사실이 제자리 실패를 가리지 못한다.
2. **H3는 생존과 횡이동 자체가 같지 않다.** 384행 모두 timeout이나 world XY 순변위 **P05/중앙값/P95 = .907/1.055/1.158m**, 평균 body 비의도 전진 1.225m. 최악 `seed4202/env11`은 world 종료 잔류 1.388m, body 전진 -0.118m, tracking .2125, stall .076이다. 평균 `vy_error=.0779m/s`(방향전환 포함)는 무시할 수 없다. 횡명령 구간의 body 전진과 순변위는 서로 다른 진단이며 동일시하지 않는다.
3. **H5는 대부분 움직이지만 일부 정체 꼬리가 있다.** body 전진 **평균/P05/최소=8.941/8.573/6.983m**, tracking P95 .1882, 최대 .2632. stall >.05는 **3/384**: `4201/env91`(7.733m, stall .130), `4202/env58`(6.983m, .209), `4203/env32`(6.983m, .246). 이 셋도 20초 timeout으로 낙상 사례가 아니다. seed별 H5 평균 8.915/8.958/8.949m이나 각 seed에 약점이 한 개씩 확인되므로 평균만으로 꼬리를 숨기면 안 된다. 스크리닝의 관찰이지 서로 다른 학습 seed 3회의 재현성 결과가 아니다.
4. **H6 진행과 행동 비용의 교환:** 상/하 경사 모두 약 19.7m body 전진이며 차이는 0.114m 수준. 하지만 `roll_pitch_rms≈.0535rad`, `action_delta_rms≈.55`로 H5의 `.0326rad/.398`보다 크다. 서로 다른 지형·속도 명령이므로 action 비용 차이를 reward의 인과로 돌리지 않는다. H6 추종 .176은 H5와 비슷하지만 H6의 `vx_error≈.043m/s`는 H5의 `.071m/s`보다 작고 yaw 오차는 오히려 더 큰 형태다.
5. **H7은 외란 중에도 계속 전진한 증거이지 회복 시간 측정은 아니다.** body 전진 10.115m(참고 command 적분 10m), timeout 384/384, `yaw_error=.0997rad/s`. step별 순간 복구시간·최대 기울기·푸시 직후 episode별 trajectory가 없어 “몇 초 내 회복”으로 수치화하지 않는다.

정지/횡명령의 원치 않는 이동〔원본 참조: `figures/unwanted_motion.png` / 공개 사본 미포함〕

## 4. 여섯 MP4 직접 조사 — 실제로 본 구간과 해석 한계

**영상 일정 (모든 파일 공통, `environment.txt`):** 50fps·1,000프레임·20초, 명령 `0–6s vx=1.0`, `6–10s (vx=.5,vy=+.3)`, `10–14s (vx=.5,vy=-.3)`, `14–17s (vx=.5,yaw=+.5)`, `17–20s (vx=.5,yaw=-.5)`. `t=4/8/12/16s`에 월드 Y방향 속도 `+0.5/-0.5/+0.5/-0.5m/s`를 더하는 밀침. 이는 영상의 **전역 시각**이고, 별개 평가의 H1~H7 10s 명령/시나리오와 같지 않다. 영상 하나는 하나의 env만 보여준다.

| MP4 | 실제 확인한 구간·프레임 (50fps) | 행동 관찰과 판정 |
|---|---|---|
| `01_stairs.mp4` | f25–250 (0.5–5s), f300–500 (6–10s), f600–975 (12–19.5s) | 초반 계단 스트립 근처로 접근하고, f100–200에서 계단이 카메라 옆/뒤로 이동; f300 이후 주변은 주로 평지. 이후 방향 변경 구간에서도 기립 보행 모습. **중앙 여러 단을 일관되게 올라간 완주 증거는 아님**; 우측 경로/가장자리 통과 가능성을 배제하지 못함. |
| `02_inverted_stairs.mp4` | f25–200 (0.5–4s), f250–500 (5–10s), f600–975 (12–19.5s) | 초반 큰 역계단 스트립이 로봇 옆으로 지나가고 f150–250에 로봇이 스트립 바깥쪽 평면에 위치. 생존·이동 모습은 있으나 중앙 다단 하행을 입증하지 않음. |
| `03_boxes.mp4` | f25/50/100/150/200/250/300/375/450/500/600/700/800/900/975 | **박스 군집 내부**에서 초기 이동·위치 변경을 여러 장면으로 확인. 6–16s에도 군집 인접/사이에 기립해 명령·외란 이후 움직임이 이어지고, 17–18s 경계 평지 근처에 도달한 듯 보임. 다만 발별 정확한 착지·걸림/sliding 여부와 20초 내 전체 박스 통과 경로는 와이드 추적 카메라로 확정하지 않음. |
| `04_random_rough.mp4` | 약 0.5–4.5s, 5.5–10.5s, 11.5–19.5s (1fps 표본) | f≈25–225에서 **초기 rough 패치 위→경계→평지**로 이동하는 모습을 확인. rough에서 주저앉는 장면은 표본에 없으나 후반 대부분은 평지라 “20초 rough 통과”로 오인하면 안 됨. 정량 H5의 3개 low-progress cohort는 이 단일 영상에 반드시 나타날 필요 없음. |
| `05_slope_up_10deg.mp4` | 약 0.5–5.5s, 6.5–13.5s, 14.5–19.5s (1fps 표본) | 경사로 표시된 지형에서 지속적인 두 발 이동과 후반 회전 명령 중 기립을 관찰. 고정 카메라 원근만으로 실제 고도 변화량·경사 구간 완주 거리를 계측하지 않음. H6 상행 정량 진행은 별도 camera-off run 결과. |
| `06_slope_down_10deg.mp4` | 약 0.5–5.5s, 6.5–13.5s, 14.5–19.5s (1fps 표본) | 하행 설정에서도 연속된 시점에 로봇이 움직이고 외란/회전 전환 후 기립. 급격한 낙상은 표본상 없지만 하강 접촉 품질·정확한 속도는 계측되지 않음. |

**프레임 조사 정확도:** 앞의 세 MP4는 1,000프레임 모두 디코딩하여 검정 프레임을 검사했고 각 파일에서 **f0 한 장만 검정**(1000장 중 1장). 뒤 세 MP4는 매초 대표 프레임 20장과 parity 확인을 위해 f0·f1·f50·f51… 총 40장/영상의 프레임 값을 검사했으며 그 표본의 검정 프레임은 **없었다**. 뒤 세 파일 **전체 1,000프레임 무결성을 검증한 것은 아니다**. 검정 이미지는 정책 낙상 근거가 아니라 캡처 artifact 여부로 분리했다. 보고서의 행동 주장은 명시한 시간대의 시각 표본에 한정되며 전 프레임 접촉 동작을 봤다는 주장이 아니다.

영상 세부를 다시 보기 위한 실제 프레임 contact sheet를 `figures/01_stairs_contact.jpg` 등 **6개** 동봉했다. 첫 세 영상의 시트는 f0·f25·f50·f100·f150·f200·f250·f300·f375·f450·f500·f550·f600·f650·f700·f750·f800·f850·f900·f975, 뒤 세 영상은 출력 표본 중심이 약 0.5,1.5,…,19.5초다. **정량 평가 명령을 이 시트의 영상 명령과 혼동하지 않는다.**

## 5. 종합 판단 및 다음 한 가지 행동

**최종 후보 판정: HOLD (목표 지향 행동은 부분 성공).** 정량 평가는 COMPLETE이고 전진·경사·외란 중 보행 능력도 확인됐다. 그러나 **정지 유지와 횡이동 복귀 실패는 H1 공식 7시나리오의 본질적인 목표**에 직접 연결되며, rough에서의 생존과 실제 전진 손실 역시 남는다. 박스·계단 같은 영상 지형은 보조 능력 확인이지 공식 H1 시나리오 점수가 아니다. 상행/하행 진행은 이 정책이 무용하다는 가설에 대한 반대 근거이지만, 정지·횡제어 비용 때문에 범용 PROMOTE까지는 어렵다. 단독 ZIP이라 비교 후보 대비 reward 변경 효과나 공식 시뮬레이션 점수의 개선은 확정할 수 없다.

**다음 행동 한 가지:** **이미 보존된 동일 evaluator의 H1 기준 정책 원자료와 CPU 대응 case/cohort 비교**를 우선한다(새 GPU 평가·학습 불필요). 우선 정지 H1의 비의도 body 진행 및 world XY 종료 잔류, 횡왕복 H3의 body 진행·vy 오차·world 잔류, rough H5의 평균/P05/최소와 `stall>.05` 빈도, H2/H6/H7 추종/진행을 함께 대조한다. 부모·기준 정책 SHA와 protocol/source fingerprint, resolved command/terrain/noise/reset parity가 확인되는 ZIP만 채택한다. **H1·H3 문제가 기준 후보보다 줄고 H5 꼬리·경사 진행을 유의미하게 잃지 않으면 PROMOTE 재검토**, 반대로 모두 비슷하거나 H2/H5/H6 손실만 크다면 HOLD 또는 REJECT 쪽으로 판정을 수정한다. 독립 학습 반복이나 reward 인과는 이 CPU 비교만으로 증명되지 않는다.

비교가 준비되지 않았을 경우 현재 단독 결론은 HOLD로 충분하다. 공식 실점이나 제출을 확인하려면 **해당 SHA→검증된 OFFICIAL 학습 Run→실제 제출 snapshot/policy** 연결과 운영진 원문이 별도로 필요하다. 이번 분석에서는 연결된 GitHub 커넥터를 이용할 수 없어 읽기 전용 제출 Release 조회는 수행하지 않았다. 이 ZIP의 `source_run_id`·`preset`는 원형대로 미확인이다.

## 6. 근거·재현 파일 인덱스

- **정책/SHA·영상 일정:** ZIP `source_checkpoint.txt`, `environment.txt`, `README.txt`, `evaluation/video_evaluation_link.json`.
- **평가 identity·환경·완료:** `evaluation/evaluation_manifest.json`, `evaluation/resolved_configs.json`, `evaluation/evaluation.log`, `evaluation/README.txt`.
- **숫자:** `evaluation/episodes.jsonl`을 원본으로 `recompute_metrics.py` 실행. `diagnostics.json`은 집계 검증용; 원본 요약을 그대로 분석 수치로 옮기지 않았음.
- **생성된 수치 파일:** `evidence/case_summary.csv`(각 case 모든 주요 지표의 평균/P05/중앙/P95/최소/최대), `evidence/seed_case_summary.csv`(case×seed 24행), `evidence/outlier_cohorts.csv`(H5 stall 또는 H3 큰 잔류 사례), `evidence/recompute_validation.json`(원본 ZIP SHA·protocol·요약 일치).
- **재현 명령:** `python recompute_metrics.py <원본_통합_ZIP> <출력_폴더>` (Python·numpy·pandas, CPU 전용). 원본 입력 18파일·MP4 전체는 이 결과 ZIP에 중복 포함하지 않았다.
- **영상 프레임 근거:** `figures/*_contact.jpg` 6개. chart `figures/body_progress_vs_command.png`, `figures/unwanted_motion.png`는 재집계한 수치의 시각화.

**검증 결과:** 원본 ZIP CRC 검사 PASS(18개 파일), metadata checkpoint SHA 연결 일치, episode ID/행/cohort 수/사망 종료 분모 확인, `diagnostics.json` 일치, 재현 스크립트 실제 실행 완료. 영상은 6개에서 표시한 시각 샘플을 시각 확인했으며 완전한 6,000프레임 수작업 판독, 영상 기반 접촉·복구 시간 측정, 원 checkpoint bytes 검증, 공식 채점 재실행은 수행하지 않았다. 원본 데이터·학습·렌더·서버·게시 상태는 변경하지 않았다.
