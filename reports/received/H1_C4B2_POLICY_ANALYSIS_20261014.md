> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/incoming/other/reviewed/H1_C4B2_POLICY_ANALYSIS_20261014.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# H1 `c4b2` / `model_2950` — 6지형 영상·camera-off 평가 심층 분석

- **작성·분석 기준일:** 2026-10-14 (KST)
- **입력:** `model_2950_h1_6terrain_evaluation_20261014-032520_aaa76aa8.zip` (정책 1개; 원본 수정 없음)
- **분석 대상:** H1 `model_2950.pt`, SHA-256 `c4b283509cc659e7bd47f5bf49eddbc387a43963d751ef353c632f48c7da1374` (이하 **H1-c4b2**)
- **평가의 성격:** Windows **PERSONAL** camera-off 정량 평가 + 별도 1-env 고정 6영상. `official_score=false`, `raw_diagnostics_only=true`. 공식 제출·채점 결과가 아님.

## 1. 결론과 후보 판단

**판정: HOLD — 실제 전진·횡이동·회전·경사·외란 대응이 가능한 보행 정책이지만, 범용 대표 후보로의 즉시 PROMOTE는 보류.** 단순 20초 생존 정책은 아니다. H2 평지 전진은 목표 body 전진 적분 15 m에 대해 **14.769 m**, H6 오르막/내리막 명령 20 m에 대해 **20.043/19.842 m**, H7 push 중 명령 10 m에 대해 **9.725 m**를 기록했다. 6영상의 boxes와 rough 초반에는 실제 장애물 구간에서 걸으며 빠져나오는 장면도 있다. H3는 순수 횡이동 왕복 명령을 대부분 추종하고, 명령이 있는 구간의 정체도 낮다.

그러나 **H5 rough에서 384개 최초 cohort 중 하나가 9.58초에 base contact로 실제 종료**됐다. 그 사례는 추종 오차 **0.425**와 roll/pitch RMS **0.257**로 나머지 분포와 뚜렷하게 다르다. H1 정지 중에도 body 기준 **−0.504 m** 후진하고 월드 XY 최종 순변위는 평균 **0.529 m**이며, H3 좌우 왕복 후에도 평균 **0.766 m**의 월드 순변위가 남는다. 게다가 영상 두 계단에서는 **중앙 다단 통과**가 확인되지 않고, 일반 보행과 장애물 전 구간의 정량 성과를 직접 등치할 수 없다.

**가장 중요한 trade-off:** 역사적 `ACTRATE-0001/model_2700` 보고치와 방향성만 비교하면 정지·횡이동 중 불필요한 전후방 이동의 절댓값은 작아진 반면, **rough 평균 진행, 전신 자세 RMS, action 변화량, rough 접촉 실패**에서는 불리한 신호가 있다. 이는 동일한 원시 ZIP을 맞춰 재집계한 직접 A/B 결과도, `feet_slide` reward 변경의 인과 결과도 아니다. 현재 후보는 **제어 균형을 확인할 가치가 있는 비교 후보로 유지(HOLD)**하되, 기존 전지형 대표 정책을 대체하지 않는다.

## 2. 정책 identity·평가 조건·검증

| 구분 | ZIP에서 직접 확인한 내용 |
|---|---|
| 표시명 / 모델 | **H1-c4b2** / `model_2950.pt`; 전체 SHA-256 `c4b283509cc659e7bd47f5bf49eddbc387a43963d751ef353c632f48c7da1374` |
| policy 연결 | `source_checkpoint.txt`, `BUNDLE_README.txt`, `evaluation_manifest.json`의 `policy.sha256`, `video_evaluation_link.json` SHA **4곳 일치**. `source_run_id=null`, `preset=null` 그대로 보존. 원 `.pt`가 ZIP에 없어 checkpoint bytes 자체는 재검증하지 못함 |
| 출처의 경계 | Windows의 source **경로명**에 `h1-actrate0001-feet_slide-fresh3k`가 포함되지만, 이것만으로 학습 Run ID·reward 실제 변경값·fresh 완료·OFFICIAL 계보를 확정하지 않음. 기존 `ANGTRACK-065/model_2950` SHA `6a6f…118c`와 **다른 정책** |
| 실행 상태 | manifest `COMPLETE`, `complete=true`, `smoke=false`; 평가 로그 `[CHILD EXIT] 0`, 끝의 COMPLETE 기록; log에 치명적 traceback 없음. **실행 완료 ≠ 정책 무실패** |
| robot / protocol | `h1` / `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34` / deterministic inference, `scenario7`, 20초 고정 시간창, 10초마다 명령 변경 |
| camera-off 집계 | H1–H7: **7 scenario, 8 case** (H6 상·하 분리), seed **4201·4202·4203**, 각 **128 env**, 난이도 **0.5**. flat H1·H2·H3·H4, rough H5, 경사 **±10°** H6, flat+push H7. **최초 cohort 3,072개**, reset 후 추가 episode 1개로 **원시 행 3,073개** |
| 실제 명령 | H1 `[0,0,0]`; H2 전진 `0.5→1.0 m/s`; H3 횡 `+0.3→−0.3 m/s`; H4 전진 `0.5 m/s`+yaw `+0.5→−0.5 rad/s`; H5 전진 `0.5`; H6 상·하 `1.0`; H7 전진 `0.5` + 설정된 속도 외란 |
| 평가 환경 | RTX 3060 Laptop GPU, Isaac Sim `5.1.0-rc.19`, Isaac Lab commit `3e73d6dd…`, task commit `ef10b7a4…`; manifest에 `agent_config_fingerprint=976cb139…` 및 case×seed별 applied env fingerprint 기록. `resolved_configs.json`의 실제 24 case/seed config와 평가 source fingerprint 확인 |
| 영상 측정 조건 | 각 1920×1080, 50 fps×1000프레임(20초), `num_envs=1`, seed/terrain seed=42, 1×1 지형, observation noise=false, 추가 base mass 0, reset pose (0,0,0). 영상의 **별도** `maneuver_push` 명령·4회 push는 camera-off episode와 같지 않음 |

**영상 command 시간표 (global video time):** 0–6초 `vx=1`; 6–10초 `(vx,vy)=(0.5,+0.3)`; 10–14초 `(0.5,−0.3)`; 14–17초 `(vx,yaw)=(0.5,+0.5)`; 17–20초 `(0.5,−0.5)` (`vx`,`vy` m/s, yaw rad/s). 4/8/12/16초에 **월드 Y 속도 ±0.5 m/s** push를 추가한다. 따라서 10초 이후 낮은 월드 X 변위 또는 영상상의 방향 변화는 전진 정체의 증거가 아니다.

**무결성 확인:** ZIP 18개 entry의 CRC 검사 통과; 여섯 MP4의 SHA-256은 ZIP 안 `SHA256SUMS.txt` 6개와 각각 일치. `episodes.jsonl`의 ID 중복 0, null 지표 0, 정책 SHA·protocol 값 전 행 동일; `n0` 최초 3,072개와 `n1` 재시작 1개가 식별된다. 동일 seed/env는 집계 대응 키일 뿐 정책 간 동일 물리 궤적의 증명이 아니다.

## 3. 원시 episode 재집계와 핵심 행동

### 3.1 case별 요약 — **episode 행 동일 가중**

아래 수치는 **직접 재집계**한 `evaluation/episodes.jsonl` 원시 행 평균이다. H5는 종료 후 재시작 1행을 포함해 **n=385**이며, 나머지 각 case는 **n=384**다. `tracking`은 내부 혼합 오차(단일 물리 단위 없음), `xy_rmse`는 m/s, `yaw_error`는 rad/s, `action Δ`는 evaluator의 action 변화 RMS(별도 물리 단위 부여 금지). `body 전진`은 body-frame 전진속도 적분(m)이며 `integrated_body_forward_m`와 **중복 동일값**이다.

| case (실제 목적) | 종료 / episode | tracking ↓ | XY RMSE ↓ | yaw 절대오차 ↓ | body 전진 m | stall ↓ | roll/pitch RMS ↓ | action Δ RMS ↓ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| H1 balance / 정지 | 0 / 384 | 0.13286 | 0.09830 | 0.07746 | **−0.504** | 0.0000* | 0.07566 | **0.53749** |
| H2 전진 0.5→1.0 | 0 / 384 | 0.13458 | 0.10961 | 0.08493 | **14.769** | 0.0080 | 0.05585 | 0.45649 |
| H3 횡 +0.3→−0.3 | 0 / 384 | 0.13089 | 0.10604 | 0.07455 | **−0.335**† | 0.0254 | 0.07274 | **0.52269** |
| H4 전진+yaw 반전 | 0 / 384 | 0.14353 | 0.10210 | 0.10304 | **9.769** | 0.0060 | 0.05864 | 0.41113 |
| H5 random rough | **1 / 385** | **0.17160** | 0.12527 | **0.11873** | **9.614**‡ | 0.0078 | 0.06096 | 0.49017 |
| H6 상행 10° | 0 / 384 | 0.16171 | 0.13020 | 0.11722 | **20.043** | 0.00495 | 0.06421 | 0.53196 |
| H6 하행 10° | 0 / 384 | 0.16286 | 0.13076 | 0.11827 | **19.842** | 0.00495 | 0.05820 | **0.54095** |
| H7 flat+push | 0 / 384 | 0.14005 | 0.12740 | 0.07992 | **9.725** | 0.00837 | 0.05960 | 0.42990 |

\* H1의 `stall=0`은 명령 XY 속도가 0이어서 **유효 분모가 없기 때문**이다. 정지 유지 성공률 100%가 아니다.\
† H3의 forward progress는 *횡이동 성취도*가 아니라 명령되지 않은 전후방 누수이므로 절댓값이 작을수록 좋다. H3 `vy_error=0.08651 m/s`이고, `lateral_drift_m=1.730 m`는 실제 월드 횡변위가 아닌 `|vy 명령−실제|`의 시간 적분이다.\
‡ H5 9.614 m는 **385 episode 행 평균**으로, 9.58초 실패 episode도 같은 가중치다. 동일한 384개 cohort의 20초 창에서 재시작 진행까지 합한 평균은 **9.639 m**(아래).\

**전체 episode 평균 tracking 0.14727** (`n=3,073`), 8 case 동일 가중 평균 **0.14726**, 7 scenario 동일 가중 평균 **0.14512**. 평균 정의가 달라지는 수치이며 공식 점수로 환산하거나 합산하지 않는다. `evaluation/diagnostics.json`의 scenario별 행수·실패수·episode tracking 평균은 원시 재계산과 일치(표시 자리 반올림 범위)한다.

### 3.2 생존과 성공: 한 번의 실패를 reset 생존으로 덮지 않음

- **전체 episode 기준:** `survived=true` **3,072/3,073 = 99.967%**. 모든 비실패 종료 3,071회 `timeout` + 1회 `evaluation_end`이며, 이것은 전부 20초 완주 3,072회를 뜻하지 않는다.
- **전체 최초 cohort의 20초 창:** **3,071/3,072** cohort에서 `terminated` 없이 종료. 1개 cohort에서 종료 **1회**. **H5 rough 최초 cohort에서 383/384 = 99.740%가 무종료**, **1/384 = 0.260%가 1회 종료**했다. H1·H2·H3·H4·H6상·하·H7은 이 창에 종료 0회다.
- **문제 cohort:** `H5-rough-s4203-e122-n0`는 479 step/**9.58초** 시 `terminated`, `base_contact_failure=true`; tracking **0.42515**, `xy_rmse=0.47440`, `yaw_rmse=0.62468`, roll/pitch **0.25655**, 전진 **3.917 m**, stall **0.03967**. 동일 cohort `…-n1`은 reset 뒤 **10.42초**만 평가되어 `evaluation_end`/`survived=true`, 전진 **4.952 m**. 두 episode의 **시간창 합산 body 전진 8.869 m**이며, 재시작 생존이 초기 낙상·접촉 종료를 취소하지 않는다.
- 따라서 H5 실패의 원인은 `end_reason`과 `base_contact_failure` 관점에서 **base contact에 따른 강제 종료**로 확정된다. 발 걸림·구체적 관절 동작·해당 시점의 시각적 실패 형태는 다환경 camera-off 원시 기록에 없어 단정하지 않는다. 6영상의 단일 seed=42 로봇은 **이 실패 cohort가 아니다**.

### 3.3 평균이 감추는 차이: 최악 구간과 seed

- **H5 rough episode 행 분포:** tracking 평균 / P95 / 최대 **0.17160 / 0.19100 / 0.42515**. body 전진 평균 / P05 / 최소 **9.614 / 9.174 / 3.917 m**. 최소는 짧은 실패 episode라 20초 값처럼 취급하지 않는다. **384 cohort** 합산 body 전진 평균 / P05 / 최소는 **9.639 / 9.194 / 8.725 m**다. 가장 낮은 정상 20초 cohort는 **seed4202/env68**, 전진 **8.725 m**, tracking **0.20358** (`timeout`, 미낙상). 즉 **생존하면서 진행·추종이 나쁜 사례**도 존재한다.
- **H5 실패 집중:** `seed4203/env122` 단 하나에서 종료. raw H5 `seed4201/4202/4203`별 episode 평균 tracking **0.17159/0.17069/0.17252**, body 전진 **9.662/9.658/9.523 m** (4203은 재시작 행 포함). 다른 두 seed에도 전진 저하 사례가 있어 실패가 4203에서만 났다고 다른 seed가 완전히 안전한 것은 아니다.
- **H1 정지:** 384/384 cohort 모두 **음의 body 전진**. 평균 **−0.504 m**, 5–95% 약 **−0.516~−0.492 m**. 월드 X와 Y의 부호 있는 전체 평균은 회전·초기 방위 차이로 상쇄되므로 정지 유지 판정에는 `hypot(world_dx,world_dy)`를 개별 episode에서 계산했다. 그 평균은 **0.529 m**, P95 **0.535 m**. `vx_error=0.02659`, `vy_error=0.08380`, `yaw_error=0.07746`이므로 20초 서 있는 동안 운동·방위 흔들림이 남는다. 정지 중 action Δ도 **0.53749**로 큰 편이다.
- **H3 횡 왕복:** 384/384 cohort에서 음의 body 누수, 평균 **−0.335 m**. 월드 순변위 길이 평균 **0.766 m**(P95 **0.814 m**). `vy_error=0.08651 m/s`, stall **0.02542**이므로 **대체로 이동은 하나 정확한 왕복 복귀/속도 추종은 미완성**이다. world 순변위만으로 실제 순간 횡이동 방향·거리를 복원할 수 없다.
- **H2/H6/H7:** H2 body 전진 **14.769 m**, P05 **14.761 m**, 월드 XY 최종 거리 평균 **14.019 m**. H6 상/하 평균 **20.043/19.842 m**, 상/하 roll/pitch RMS **0.06421/0.05820** 및 action Δ **0.53196/0.54095**여서 *방향별 미세한 제어 비용 차이*가 있다. H7 전진 **9.725 m**, P05 **9.619 m**이며 384회 종료 없음. 별도 외란 case에서도 진전하지만, 오차 적분만으로 push 직후 수백 ms의 **회복 시간**을 재구성하지는 못한다.
- **seed 변화의 범위:** flat case의 3개 seed 평균은 매우 가깝다(예: H2 `14.7697 / 14.7688 / 14.7693 m`, H3 tracking `0.1309` 수준). 반면 rough는 분산과 실패 꼬리가 뚜렷하다. **3개 evaluator seed/다수 env를 3,072개의 독립 학습 seed 또는 재현된 동일 물리 trajectory로 간주하지 않는다.**

### 3.4 물리적으로 무엇을 말할 수 있는가

`mean_tracking_error`는 step당 `sqrt(vx_error² + vy_error² + yaw_error²)`의 episode 평균인 **서로 단위가 섞인 내부 지표**다. `vx_error/vy_error/yaw_error`는 축별 절댓값 평균이지 `xy_rmse/yaw_rmse`가 아니다. `forward_progress_m`와 `integrated_body_forward_m`는 같은 body-frame 적분이므로 독립 근거 두 개로 세지 않았다. `world_dx/world_dy`는 기준 방향에 따라 부호가 달라 각 열의 평균 대신 **episode별 XY 최종 거리**를 별도로 계산했다. `stall_fraction`은 명령 XY 속도≥0.2 m/s인 step 중 실제 body XY 속도<0.1 m/s의 비율이므로 H1에는 적용되지 않는다. foot sliding, air time, 관절 deviation, 실측 발 마찰력은 이 ZIP에 정량 지표로 없다.

정량 근거를 종합하면 **속도 명령을 대체로 수행하며 실제 전진/평지 왕복/회전/경사 이동이 된다**. 반면 특히 **정지 누수, 거친 지형의 매우 드문 접촉 종료와 하위 꼬리, action·몸통 자세 비용**을 별도로 관리해야 한다. 현재 수치는 `goal complete`·지형 끝 통과·장시간 사용 가능성을 보장하는 지표가 아니다.

## 4. 여섯 MP4의 실제 프레임 관찰

모든 영상의 시작·장애물 접촉/접근·탈출·명령 변경·외란 전후·후반 구간을 직접 프레임 조사했다. **표시 시각은 50 fps 기준 `frame/50`초**이다. 아래의 사실은 **한 env/seed42 고정영상**에서 보이는 정성 관찰이며, H5 camera-off의 seed4203/env122 종료 사건과 대응하는 장면이 아니다.

| MP4 | 확인 프레임·시각 | 관찰 / 판단 한계 |
|---|---|---|
| `01_stairs.mp4` | f25–200(**0.5–4.0초**), f400(**8초**), f800–998(**16–19.96초**) | 계단 띠의 **가장자리 인접으로 보행하며 전진**하고 후반에는 지형을 벗어난 평지에서 서서/걸으며 명령 변화에 반응한다. 계단 중앙의 여러 단을 연속해 밟고 오르내리는 장면은 확인되지 않아 **다단 통과 성공이라고 할 수 없음**. f200/400/800 전후에 장시간 쓰러진 모습은 보이지 않지만 발 마찰·높이 회복량은 미측정. |
| `02_inverted_stairs.mp4` | **가시 홀수 프레임** f1/51/101/151/201/251(**0.02–5.02초**), f401(**8.02초**), f801/901/975(**16.02/18.02/19.50초**) | 하향 계단 띠 **옆으로 이동해 멀어지는 장면**이며, 중앙 계단 전 구간 하강은 입증되지 않는다. 마지막 19초대에도 보행 형태는 보이나 **짝수 프레임 500/1000개가 순수 검정, 홀수 500개는 가시**인 교대 캡처 결함이다(전체 1,000 프레임 저해상도 휘도 검사 및 짝 확인). 영상 전체가 검정이거나 로봇이 사라진 정책 실패로 해석하지 않음. |
| `03_boxes.mp4` | f25/50/100/125/150/200(**0.5–4.0초**), f250(**5초**), f600/800/950(**12/16/19초**) | 첫 수초 **상자 장애물 군집의 안쪽에 있는 로봇이 다리를 번갈아 옮겨 경계 밖으로 빠져나오고** 5초 이후 평지에서 계속 걷는다. **초기 boxes 대응의 가장 분명한 긍정적 시각 근거**. 하지만 미끄럼 없는 모든 발 접촉·모든 장애물 완주율은 이 영상 한 건으로 증명되지 않는다. 해당 정량 scenario7에는 boxes case가 없다. |
| `04_random_rough.mp4` | f25/50/75/125/150/200(**0.5–4초**), f250(**5초**), f400/600/800/975(**8/12/16/19.5초**) | 초기 rough 패치 위에서 균형을 잃지 않고 걸으며 **약 4–5초 사이 패치를 떠나 평지 보행**으로 전환. 이후 전역 횡/회전 명령·push 구간에서도 계속 서 있다. 이는 H5 대부분의 실제 진행과 **방향성은 일치**하나 9.58초 contact로 끝난 H5 최악 cohort의 영상을 대체하지 못한다. |
| `05_slope_up_10deg.mp4` | f25–250(**0.5–5초**), f400/600/800/950(**8/12/16/19초**) | 완만한 높이 변화 텍스처 구간에서 **걸음을 이어가고 이후에도 전진/방향 변경 보행**. H6 상행 진행 적분 20.043 m와 양립하지만 **20초 전체를 10° 실경사로 오른 거리**로 추정하지 않는다(후반은 지형 패치 밖 평지 가능). |
| `06_slope_down_10deg.mp4` | f25–250(**0.5–5초**), f400/600/800/950(**8/12/16/19초**) | 하향 경사 템플릿에서 초반 보행 유지, 4·8·12·16초 push/명령 시간대를 지나 후반까지 이동. H6 하행 19.842 m·384/384 무종료와 정성적으로 부합. 정확한 **경사 위 접지/회복 시간/슬라이딩**은 고각 추적 카메라의 제한으로 확정하지 않음. |

**영상의 push·방향 전환:** 모든 영상에서 4/8/12/16초 push가 설정되며, 예를 들어 `03_boxes.mp4` f200(4초)→f250(5초), `04_random_rough.mp4` f400(8초)→f600(12초), 각 영상 f800(16초)→f950(19초)의 프레임에서는 보행 지속이 보인다. **외란 이후 걷기 재개/유지는 확인되지만, push 순간의 자세 peak·발 끌림·유한 시간 회복 latency까지 검증한 것은 아니다.** 이 영상은 평가 H7의 command, terrain, reset, 타임베이스가 다른 정성 시험이다.

**추가 캡처 주의:** 영상 **모두 f0은 검정**, 마지막 **f999(19.98초)**에서는 직전 f998까지 존재하던 몸통/다리가 공통으로 대부분 사라지고 작은 색 영역만 남는다. 여섯 영상에서 동일 종료 프레임에 일어나는 현상이므로 개별 정책이 동시에 낙상한 근거보다 **녹화/시뮬레이션 종료 아티팩트**로 해석한다. 원본 재렌더·수정은 수행하지 않았다. 한편 `02`는 f0만 아니라 전 시간대 짝수 500프레임이 검정이므로 연속 보행을 판독할 때 홀수 인접 프레임을 사용했다.

## 5. 기존 정책과의 **참고 비교** — 원시 A/B로 승격하지 않음

현재 업로드는 **한 정책 ZIP만** 포함한다. 아래 `ACTRATE-0001/model_2700` 값은 프로젝트에 이미 기록된 **2026-10-10 세 정책 원본 비교 요약**(`06_HUMANOID_TRAINING_CODE.md`, `20_H1_PUBLIC_FAILURES_AND_EXPERIMENT_PRIORS.md`, `21_WINDOWS_GO2_VIDEO_AND_EVALUATION.md`)에서 가져온 **과거 참고값**이다. 본 작업에서 그 정책의 원시 ZIP·checkpoint·config를 다시 열어 대응 cohort/parity를 독립 검증하지 않았다. 정책·Run·reward 인과나 실물 matched 영상 비교로 오인하면 안 된다.

| 행동축 | 기존 ACTRATE-0001/model_2700 (과거 보고치) | **이번 H1-c4b2 직접 재계산** | 의사결정 시 읽을 점 |
|---|---:|---:|---|
| H1 정지 body 전진 누수 | **+1.987 m** | **−0.504 m** | 절댓값은 작아졌으나 **편향 방향이 후진으로 뒤집힘**. 세계좌표 0.529 m 이동이 남아 완전 제자리 유지 아님 |
| H3 순수 횡이동 body 전진 누수 | **+1.677 m** | **−0.335 m** | 횡명령 중 불필요한 전후방 이동 억제 신호. 그러나 world 왕복 잔차 0.766 m, `vy_error=0.0865 m/s` |
| H5 rough episode 평균 body 전진 | **9.948 m** | **9.614 m** | 주행 진행이 낮은 방향. 현재 H5는 **1 contact 종료**, 이전 보고는 무종료. 여기서 정책이 결정적으로 열세라는 통계적 확정은 불가 |
| 전체 episode 평균 tracking | **0.14534** | **0.14727** | 차이는 작고 다른 case 가중치·reset 구성 확인 전 성능 우열로 단정 불가 |
| 전체 roll/pitch RMS | **0.03019** | **0.06323** | 자세 변동 비용 증가 가능성이 큼. 단, 동일 원시 evaluator config 및 cohort 비교 선행 필요 |
| 전체 action Δ RMS | **0.45687** | **0.49010** | 동작 변화 비용이 더 큰 방향. 발 미끄럼 또는 관절 손상 자체의 측정은 아님 |

**해석:** 정지/횡이동 전후방 편향을 억제하는 움직임은 유망하다. 그러나 그 대신 rough contact·자세 변동·action 비용이 악화한 듯한 신호도 있어 전지형 대체 **PROMOTE 근거가 성립하지 않는다**. `feet_slide`가 원인이라는 주장은 금물이다. ZIP 내부에는 reward/학습 계보의 확정 증거가 없고, 위 표는 **원시 대응키 비교가 아닌 과거 요약과의 서술적 대비**이기 때문이다. 과거 모델명의 숫자 2950 또는 경로의 `fresh3k`만으로 새 학습 효과를 소급하지 않는다.

## 6. 최종 판단과 다음 행동 하나

- **목표 행동 성공?** **상당 부분 예.** H2/H4/H6/H7의 명령 방향 이동, H3 횡명령 대응, boxes·rough 초기 통과 동작은 실질적. **완전 성공은 아님:** H1 정지·H3 왕복 잔차, H5 contact 종료/꼬리, 경사·계단 전체 통과의 관찰 한계.
- **안정·회복?** 3,071/3,072 최초 cohort가 한 번의 `terminated` 없이 20초를 완료했고, push case에서도 384/384 무종료다. **실제 H5 접촉 실패 1건**을 그대로 유지하고, 순간 외란 회복속도와 물리 접촉 원인은 미측정이라고 판정한다.
- **후보 가치?** **HOLD.** 정지/횡이동 누수를 줄이려는 검토 후보로는 남기지만 rough 및 몸통/행동 비용 교환을 확인하기 전에는 주력 정책을 교체하지 않는다. 계단 능력은 이 ZIP 기준 **미확정**이다.

**다음 행동 한 가지 — 새 GPU 작업 없이 보존된 `ACTRATE-0001/model_2700`의 기존 `evaluation/episodes.jsonl`과 `resolved_configs.json`을 확보하여 이 H1-c4b2와 직접 대응 cohort 비교.** 먼저 두 policy SHA, robot, `protocol_id`, source·agent·applied-env fingerprints, 24 case×seed 실제 설정, 초기 조건, command·push, noise/randomization, horizon, cohort ID를 대조한다. 호환된다면 **H1 정지 body 누수+월드 순변위, H3 `vy_error`+world 복귀 오차, H5 384개 최초 cohort의 실패 발생·누적 진행 P05/최악, roll/pitch/action 비용**을 같은 기준으로 비교한다. *정지/횡이동 개선이 여러 seed/cohort에서 유지되고 rough 접촉·하위 꼬리·자세 비용이 수용 가능한지*에 따라 HOLD→PROMOTE(용도 한정 포함) 또는 HOLD→REJECT를 결정한다. 설정이 맞지 않으면 A/B를 중단하고 서술적 참고 비교에 머문다. **추가 학습·평가·렌더링·export·서버 조작·게시 요청이 아니다.**

### 보고서를 재확인할 수 있는 원본 위치

- 정책 연결·영상 조건: ZIP 루트 `source_checkpoint.txt`, `environment.txt`, `README.txt`, `BUNDLE_README.txt`, `SHA256SUMS.txt`; `evaluation/video_evaluation_link.json`.
- 평가 complete/protocol/seed/source: `evaluation/evaluation_manifest.json`, `evaluation/resolved_configs.json`, `evaluation/evaluation.log`, `evaluation/README.txt`.
- **직접 재계산** 대상: `evaluation/episodes.jsonl`, 대조용 요약 `evaluation/diagnostics.json`; cohort 키 `(scenario,case,seed,env_id)` 및 `episode_id`의 `n0/n1`을 분리.
- **실제 조사한 영상:** ZIP 루트 `01_stairs.mp4`, `02_inverted_stairs.mp4`, `03_boxes.mp4`, `04_random_rough.mp4`, `05_slope_up_10deg.mp4`, `06_slope_down_10deg.mp4`. 시간/프레임은 본문 표에 기재.
- 역사적 참고값만: 제공된 프로젝트 문서 `06_HUMANOID_TRAINING_CODE.md`, `20_H1_PUBLIC_FAILURES_AND_EXPERIMENT_PRIORS.md`, `21_WINDOWS_GO2_VIDEO_AND_EVALUATION.md`. **이번 ZIP의 직접 원자료 관찰과 구분.**

**검산 결과:** SHA identity 네 metadata의 일치, CRC·영상 6 SHA, `3,072 cohort + restart 1 = 3,073 episode`, `H5 terminated=1`, H6 상·하 분리, episode vs cohort 평균, units와 black-frame parity를 확인했다. 원본의 단일 정책·Windows PERSONAL 신분과 후보 HOLD 판정을 유지했다.
