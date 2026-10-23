> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/incoming/other/reviewed/H1_JOINTTRACK_ORIENT_MODEL2850_POLICY_ANALYSIS_20261017/H1_JOINTTRACK_ORIENT_MODEL2850_POLICY_ANALYSIS_20261017.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# H1 JOINTTRACK–ORIENT / model_2850 정책 행동 심층 분석

- **작성·확인 기준일:** 2026-10-17 (KST)
- **주요 근거:** 사용자 첨부 `20261017-072659-h1-lintrack-065-angtrack-060-actrate-0003-orient_model_2850_h1_6terrain_evaluation_20261017-181149_f1f8e371.zip` 내부 원본. ZIP SHA-256 `af58e8f10165dbce7bd1c0363c09f523db925d9775870549819f94854fe4f6b9`.
- **표시명 주의:** `JOINTTRACK–ORIENT / model_2850`은 **첨부 파일명에 근거한 임시 표시명**이다. lin=.65/ang=.60/action=-.0003/orientation 변경의 **실제 OFFICIAL 학습 설정·Run ID를 입증한 명칭이 아니다.** 평가 시 로드된 정책의 SHA가 이 보고서의 기본 identity다.
- **판단 목적:** H1 **공식 7시나리오 제출 경쟁력에 활용할 정책 후보**인지 우선 검토하고, 계단·박스 등 광의 보행 능력은 보조로 평가한다.

## 1. 결론 — 움직이고 버티지만, 현재 주후보로 승격하지 않는다

**정책 후보 판단: HOLD.** `scenario7` 3,072개 20초 평가에서 몸통 접촉 종료 없이 전부 생존했고, H2 전진, H6 ±10° 경사, H7 밀침 조건에서 실제 body-frame 이동과 명령 추종의 유효 신호가 있다. 그러나 **H1 정지 시 불필요한 후진, H3 횡이동 시 후진·최종 위치 잔류, H5 rough의 전진 속도 손실·하위 꼬리**가 동시에 남는다. 공식 제출의 새 주후보로 추천할 만큼 우세한 방향은 확인되지 않았다. 기존 제출을 이 정책으로 대체하지 않는다.

가장 중요한 trade-off는 **20초 100% 생존 vs 명령 목적의 정확성**이다. 구체적으로 H1 제자리에서 실제 body 전진 적분 `−0.719m`, H3 측면 왕복에서 `−0.679m`, H5 명령 `0.5m/s × 20s = 10m` 대비 실제 전진 평균 `8.024m`이다. H5의 평균 stall은 `0.00952`이고 큰 stall은 드물어, 여기서는 **완전 정체보다 지속적인 속도 손실**이 주요 문제다.

여섯 영상에서 로봇은 전반적으로 직립하며 보행을 계속한다. 다만 계단 영상은 주요 다단 중앙 구간을 명확히 완주하는 장면이 아니고, rough·slope의 후반부 상당 시간은 카메라상 해당 초기 패치 바깥으로 이동한다. **이는 공식 H1 평가에 계단·박스 정량 case가 없다는 점에서 자동 탈락 사유는 아니며, 넓은 의미의 지형 통과 실증에는 공백**이다. 별도의 공식 제출·평가 성공으로 표현하지 않는다.

H5 rough episode별 전진 거리 분포〔원본 참조: `h5_progress_histogram.png` / 공개 사본 미포함〕

## 2. 식별·완료 상태·비교 조건

| 항목 | 첨부 ZIP에서 직접 확인한 값 |
| --- | --- |
| Robot / 입력 | `h1` / `Humanoid-v0`, native `rsl_rl_checkpoint`, 파일명 `model_2850` |
| **정책 SHA-256** | **`4a343750b47920d3b49e5e3ec7a3bf49fd9403d5b51a3727604971e6b7b0025d`** |
| 영상↔평가 연결 | `source_checkpoint.txt`, `video_evaluation_link.json`, `evaluation_manifest.json`, 3,072개 episode의 SHA가 일치. 원본 `.pt` 바이트는 ZIP에 없음 |
| 평가 상태 | `COMPLETE`, `complete=true`, `smoke=false`, `official_score=false`, PERSONAL Windows camera-off |
| 프로토콜 | `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34` |
| Camera-off 평가 | 3 seeds `4201/4202/4203` × 128 env × 8 case = 3,072 최초 cohort·3,072 episode / 케이스별 384행 |
| 시간·종료 | 전원 1,000 step / 20.0s `timeout`; `terminated` 0, 몸통 접촉 종료 0, 누락 `base_contact_failure` 0 |
| 시나리오 | H1 balance, H2 forward, H3 lateral, H4 rotation, H5 rough, H6 slope_up·slope_down, H7 push |
| Source | task/reward 4개 SHA fingerprint 기록, `agent_config_fingerprint` 기록; 평가 seed별 적용 환경 fingerprint 기록 |
| 원 학습·제출 이력 | `policy.source_run_id=null`, `preset=null`; 이번 SHA에 대응하는 실제 OFFICIAL 학습 Run·부모·submission `policy.pt` **확인되지 않음** |

**개별 case·command:** H1 정지 `(0,0,0)`; H2 10초씩 `vx=0.5→1.0`; H3 10초씩 `vy=+0.3→−0.3`; H4 `vx=0.5`, `yaw=+0.5→−0.5rad/s`; H5 rough `vx=0.5`; H6 상·하 10° `vx=1.0`; H7 평지 밀침 `vx=0.5`. Windows PERSONAL 20초 window이고, H7 평가 외란은 평가 프로토콜에 기록된 고정 XY 속도 변화다. 명령 시간표는 camera-off의 **episode 기준**이며 MP4의 전역 시간표와 같다고 취급하지 않는다.

**영상별 고정 조건:** 각각 1 env, seed42, 50fps, 1,000프레임/20초, `maneuver_push` SHA `b719e60d4226b95ba8c533c18c10fdeda44359bd8f2ed6135c4c3d7c296d7dea`, command trace SHA `0d7e2ef1da1aba7d713f0ffafba7ead7863813625dd7a3e948b16688dd2673f6`. 전역 0–6초 `vx=1`; 6–10초 `(vx,vy)=(.5,+.3)`; 10–14초 `(.5,-.3)`; 14–17초 `vx=.5,yaw=+.5`; 17–20초 `vx=.5,yaw=−.5`; world-Y 속도 impulse `+0.5/−0.5/+0.5/−0.5m/s`를 4/8/12/16초에 가함. 관측 noise off, base mass add 0, heading command off, terrain seed42. MP4 밀침은 비공개 공식 밀침 조건의 재현이 아니다.

**평가 설정과 실제 학습 설정을 혼동하면 안 된다.** `evaluation/resolved_configs.json`에는 평가 실행 task의 reward snapshot, 예를 들어 `action_rate_l2=-0.0005`가 있다. 이 값은 ZIP 파일명에 암시된 학습 action 값 `-0.0003`을 반증하거나 확정하는 **학습 config 증거가 아니다**. 전체 reward 변경·orientation/hip 값·fresh/resume 여부는 원 native 학습 archive 없이는 확정 불가다.

## 3. 원자료 직접 재집계 — 통과의 내용과 비용

### Case별 핵심 지표

다음은 `evaluation/episodes.jsonl` 직접 계산이며 케이스 내 episode **동일 가중**(각 384행)이다. `tracking`은 episode의 `mean_tracking_error` 산술평균으로 선속도와 yaw-rate가 혼합된 내부 지표이며 단일 물리 단위를 붙이지 않는다. `body전진`은 `forward_progress_m`(=`integrated_body_forward_m`)으로 world X 변위와 다르다. `P05`는 해당 case episode 전진 거리의 5백분위, `RP RMS`는 `roll_pitch_rms`(rad), `action Δ`는 `action_delta_rms`다.

| case | 생존 | tracking ↓ | vx 절대오차 m/s ↓ | vy 절대오차 m/s ↓ | yaw 절대오차 rad/s ↓ | body전진 평균 / P05 (m) ↑ | RP RMS ↓ | action Δ ↓ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| H1 정지 | 384/384 | 0.09810 | 0.03782 | 0.05987 | 0.05023 | **−0.719 / −0.798** | 0.11501 | 0.40816 |
| H2 전진 | 384/384 | 0.15778 | 0.07688 | 0.06866 | 0.09720 | **13.465 / 13.414** | 0.08777 | 0.43207 |
| H3 좌우 | 384/384 | 0.11658 | 0.03740 | 0.06271 | 0.06814 | **−0.679 / −0.696** | 0.11275 | 0.39499 |
| H4 회전복합 | 384/384 | 0.13732 | 0.05809 | 0.06298 | 0.08520 | 8.863 / 8.822 | 0.10029 | 0.39039 |
| **H5 rough** | **384/384** | **0.21625** | **0.10904** | 0.06252 | **0.14645** | **8.024 / 7.460** | 0.08408 | 0.39492 |
| H6 경사 상승 | 384/384 | 0.14285 | 0.05489 | 0.06230 | 0.09625 | **19.165 / 19.055** | 0.08761 | 0.47695 |
| H6 경사 하강 | 384/384 | 0.14950 | 0.06031 | 0.06460 | 0.09946 | **18.974 / 18.865** | 0.08325 | 0.48418 |
| H7 밀침 | 384/384 | 0.15078 | 0.06531 | 0.06816 | 0.09412 | **8.875 / 8.790** | 0.09846 | 0.40845 |

- **전체 episode 가중 tracking = 0.1461466193**, survival = 1.00000. 모든 case가 정확히 384행이어서 이번 자료의 **8-case 동일가중 tracking도 0.1461466193**으로 같다. 그러나 공식 7시나리오 가중 평균이나 공식 Tracking Score가 아니다. `diagnostics.json`의 각 시나리오 episode 수·survival·tracking과 원자료 재계산값이 일치한다. H6은 768행(상·하 각 384)이므로 7개 시나리오를 같은 비중으로 평균한 값과는 구분해야 한다.
- **H1 정지·H3 횡이동:** H1은 정지인데 body-frame 앞방향 적분이 평균 **−0.719m**이고 실제 `sqrt(world_dx²+world_dy²)` episode별 평균은 **0.883m**다. H3는 `vy`를 ±0.3m/s로 추종하면서 body 전진 **−0.679m**, world XY 종료 잔류 평균 **1.160m**가 발생한다. 음수는 의도치 않은 **후진 성분**이지 전진 성공이 아니다. H3의 종료 world 원점 복귀는 공식 채점의 독립 요구사항이 아니라 추종·위치 제어를 진단하는 보조 지표다.
- **H2·H6·H7 실제 진행:** H2는 명령 적분 목표 15m에 대해 평균 13.465m, H6 ±10°는 목표 20m에 대해 상승 19.165m·하강 18.974m, H7은 목표 10m에 대해 8.875m다. 해당 명령의 body-frame 실제 진행이 확인되므로 **제자리 버티기만 하는 정책은 아니다**. H4는 회전 중 `vx=.5` 명령이므로 world X 순변위만 보고 stall을 판정하지 않았다. H4 yaw 절대오차 평균은 0.08520rad/s이며 회전 추종 신호가 있다.
- **H5 rough 가장 약한 case:** tracking 0.21625, vx 절대오차 0.10904m/s, yaw 절대오차 0.14645rad/s로 전체 case 중 최대다. 목표 전진 적분 10m 중 실제 평균 **8.024m**; P05 **7.460m**, 최소 **6.721m**, tracking P95 **0.24748**. 평균 `stall_fraction=0.00952`이고 `stall_fraction>0.05`가 **1/384**뿐이므로 대부분은 완전히 멈추는 것이 아니라 **진행하되 느리다**. worst `seed4201/env74`: 진행 **6.721m**, stall **0.052**, tracking **0.28670**, 20초 timeout 생존. 후반 low-speed 꼬리를 평균만으로 지우면 안 된다.
- **자세·행동 비용:** H1 RP RMS 0.11501, H3 0.11275로 경사 H6(0.08325–0.08761)보다 큰 수치다. H6 action Δ RMS(상 0.47695, 하 0.48418)는 H5(0.39492)보다 크다. 경사 진행력이 좋더라도 action 변화 비용까지 개선됐다고 할 수 없다. action Δ는 foot sliding, airtime, 관절 편차의 측정값이 아니다.

### Seed·실패 집중·집계의 의미

- H5 평균 진행은 seed **4201: 8.033m / 4202: 8.053m / 4203: 7.985m** (각 128 env)로, rough 약점이 한 seed 평균에만 국한된 것은 아니다. H5 tracking seed별 평균은 **0.21682 / 0.21433 / 0.21761**. 하지만 가장 나쁜 개별 지형/env의 6.721m는 평균보다 크게 뒤처진다. **3개 평가 seed를 독립 학습 seed 3회로 세지 않는다.**
- 모든 `episode_id`는 고유하고, `(scenario,case,seed,env_id)` 3,072 cohort 각각 **episode 1개**였다. `terminated` episode 0/3,072 및 20초 중 **한 번 이상 terminated된 cohort 0/3,072**로 이번에는 episode 종료율과 cohort 종료율이 같다. 원자료 전체 실패·짧은 episode 누락은 없다. `survived=true`는 `timeout` 생존이며 지형 완주 증거가 아니다.
- `lateral_drift_m`는 world Y 횡변위가 아니라 **횡속도 오차 절댓값의 시간적분**이다. 진짜 위치 잔류는 이 보고서에서 `world_dx_m/world_dy_m`으로 별도 계산했다. H1의 `stall_fraction=0`은 유효한 이동속도 명령 step이 없기 때문이므로 정지 유지에 성공했다는 의미가 아니다.

## 4. 여섯 MP4 프레임 조사 — 보이는 행동과 보이지 않는 완주

실제 ZIP에서 6개 MP4를 디코딩했다. 각 **1,000프레임(50fps)의 픽셀 기반 검정 프레임 검사**와 파일별 **20개 시점의 전체 화면 + 15개 시점의 확대 프레임 시각 조사**를 수행했다. 이는 **전 6,000프레임의 연속적인 발 접촉/관절 움직임 수동 판독은 아니다**. 확대 프레임은 `video_frames/*.jpg`에 포함된다. 20초간 보이는 locomotion은 단일 env의 정성 근거이며 camera-off 3,072 episode와 같은 trajectory가 아니다.

| MP4 | 직접 확인한 시간/프레임과 장면 | 행동 판단·제약 |
| --- | --- | --- |
| `01_stairs.mp4` | **f75–175(1.5–3.5s)**에서 계단의 선형 단차 가장자리 부근을 지나 로봇이 직립. **f225–975(4.5–19.5s)** 대부분 단차가 뒤로 사라진 평지에서 전진·횡이동·회전 자세 변화 | 앞부분의 접촉/통과 움직임은 보이지만 **중앙 다단 계단을 순서대로 올라 완주했다는 증거는 아님**. 완전 정지·명백한 낙상은 sampled frames에서 보이지 않음 |
| `02_inverted_stairs.mp4` | **f25–125(0.5–2.5s)**에 역계단 단차가 로봇의 측면/후방에 보이고 **f175(3.5s)** 이후 단차가 화면 밖으로 이탈 | 중앙 역계단 정면 하강 코스 완주는 미입증. 영상 대부분은 평지 보행, 쓰러짐으로 보이는 프레임은 없음 |
| `03_boxes.mp4` | **f25–775(0.5–15.5s)** 장애물 군집 안/주변에서 발을 들어 전진하고 몸통 전경사도 보임. **f875–975(17.5–19.5s)** 군집 바깥 평지로 이동 | 장애물에 가까이 접근하고 여러 블록 사이에서 **실제 이동을 지속한 강한 정성 신호**. 단, 정량 박스 성공률·전 발 접촉 품질·슬라이딩 정도는 측정 불가 |
| `04_random_rough.mp4` | **f25–225(0.5–4.5s)** 요철 패치 내부에 발이 놓이고, **f275–375(5.5–7.5s)** 가장자리 이탈, 이후 평지 | 초기 요철 보행은 보이나 20초 전체가 rough 접촉은 아님. camera-off H5의 `8.024m`는 **별도의 rough 평가 실행**에서 나온 값으로 영상의 눈대중 거리와 동일시하지 않음 |
| `05_slope_up_10deg.mp4` | **f25–175(0.5–3.5s)** 경사 형상과 로봇 보행이 함께 확인됨. f375 이후 평탄한 타일 중심 | 상승측 영상에서 직립·진행 신호. 전체 20초 경사면 연속 등반과 고도 이득 정량값은 미확인. camera-off H6 상승 19.165m는 별도 근거 |
| `06_slope_down_10deg.mp4` | **f25–175(0.5–3.5s)** 하강측 경사 형상과 보행 확인, **f375–975(7.5–19.5s)** 대부분 평지 | 하강 중 넘어지는 샘플은 없으나 자세·발 접촉의 지속 품질을 영상만으로 확정하지 않음. H6 하강 진행은 18.974m |

**명령·밀침 변화와 시간대:** 여섯 영상 모두 f200/400/600/800(4/8/12/16s) 직후의 전체 화면 시점, f300/500/700/850(6/10/14/17s) 인접 시점을 포함하도록 확인했다. 확대 판독에도 f225/425/575/775/875 등 전후 대표 프레임을 포함한다. 밀침 이후 직립한 프레임은 있으나 **복구에 걸린 초·자세 peak·즉시 재가속**은 이 자료로 산출하지 않았다. 6–14초 횡속도 명령, 14–20초 yaw 명령 때문에 후반의 영상 world X 전진이 작아도 곧바로 보행 실패가 아니다. 추적 카메라에서 몸체가 중앙에 있다는 것도 제자리 보행을 뜻하지 않는다.

**캡처 artifact 분리:** 50fps로 전체 1,000프레임의 축소 픽셀을 검사한 결과 `01_stairs.mp4`의 **f0,f2**, 다른 5개 영상의 **f0**에서 검정 프레임이 확인됐다(검정 기준 축소 샘플 픽셀 최댓값 `<10`). 반대 parity의 인접 프레임과 후반 프레임은 정상 이미지여서 **검정/유효 격프레임 교대 결함은 이번 6영상에서 확인되지 않았다**. 검정 화면을 정책 낙상으로 해석하지 않았다. 각 영상 SHA-256은 `SHA256SUMS.txt`와 **6/6 일치**했고 ZIP CRC도 통과했다. 파일명과 체크포인트 SHA 연결이 확인되지만 원본 `.pt` bytes 재해시는 불가능하다.

대표 프레임 이미지: stairs〔원본 참조: `video_frames/01_stairs_zoom.jpg` / 공개 사본 미포함〕 · inverted〔원본 참조: `video_frames/02_inverted_stairs_zoom.jpg` / 공개 사본 미포함〕 · boxes〔원본 참조: `video_frames/03_boxes_zoom.jpg` / 공개 사본 미포함〕 · rough〔원본 참조: `video_frames/04_random_rough_zoom.jpg` / 공개 사본 미포함〕 · up〔원본 참조: `video_frames/05_slope_up_10deg_zoom.jpg` / 공개 사본 미포함〕 · down〔원본 참조: `video_frames/06_slope_down_10deg_zoom.jpg` / 공개 사본 미포함〕. 그림은 지정된 프레임 캡처이며 연속 재생의 대체물은 아니다.

## 5. 관련 GitHub 학습·제출 기록 — 이번 정책의 공식 점수와 구분

2026-10-17에 **GitHub 연결의 읽기 전용**으로 `SE3C/naver-issacsim`의 `research/EXPERIMENTS.md`, `research/submission_presets/README.md`, H1 관련 Experiment 및 공식 평가 기록을 읽었다. 정확히 이 ZIP의 체크포인트 **SHA `4a343750…b0025d`와 연결되는 학습 Run·보존 indexed checkpoint·제출 policy 바이트의 일치 정보는 해당 조회 범위에서 확보하지 못했다**. ZIP의 `source_run_id/preset`도 null이다. 따라서 아래 값은 **확인된 과거 *다른 제출*의 결과**이지 첨부 정책의 공식 점수가 아니다. 전체 GitHub 저장소에서 해당 SHA가 존재하지 않는다고 단언하는 것도 아니다.

| 공식 H1 시나리오 (배점) | R2 TERM-50 (9/9 제출) | R4 AIRTIME-025 (9/28 제출) | R6 ACTRATE-0001 (10/11 제출) |
| --- | ---: | ---: | ---: |
| 제자리 균형 (10.5) | 8.62 | 8.58 | 8.60 |
| 전진 추종 (14) | 11.24 | 11.34 | 11.30 |
| 좌우 추종 (7) | 5.73 | 5.72 | 5.73 |
| 회전 복합 (7) | 5.66 | 5.68 | 5.68 |
| 약한 요철 (10.5) | **8.17** | **8.00** | **8.02** |
| ±10° 경사 (10.5) | 8.47 | 8.53 | 8.52 |
| 밀침 회복 (10.5) | 8.48 | 8.52 | 8.50 |
| **시뮬레이션 (70)** | **56.37** | **56.37** | **56.35** |
| 설계 의도 / 보고서 | 20/20 · 10/10 | 20/20 · 10/10 | 20/20 · 10/10 |
| 종합/구성합 (100) | 86.37 | 86.37(구성합) | 86.35 |

- **출처:** [R2 공식 점수 검토](https://github.com/SE3C/naver-issacsim/blob/main/data/processed/experiments/h1/analysis/2026-09-10_OFFICIAL_EVAL_H1_ROUND2_TERM50.md), [R4 공식 점수 검토](https://github.com/SE3C/naver-issacsim/blob/main/data/processed/experiments/h1/analysis/2026-09-30_OFFICIAL_EVAL_H1_ROUND4_AIRTIME025.md), [R6 후속 원문 수신·세부 7점](https://github.com/SE3C/naver-issacsim/blob/main/data/processed/experiments/h1/analysis/2026-10-16_H1_ANGXY008_MODEL4650_POLICY_REVIEW.md), [제출 연결·preset 기록](https://github.com/SE3C/naver-issacsim/blob/main/research/submission_presets/README.md).
- **원문 등급:** R2/R4는 팀이 수신한 운영진 공식 결과를 정리한 보존 문서다. R6의 7개 시나리오 점수와 56.35/86.35는 후속 **사용자 전달 공식 결과**가 팀 문서에 반영된 값으로, 이번 조사에서 대회 포털 원본을 직접 열람한 것은 아니다. 과거 preset README 일부 문구에 R6 점수 *unknown*이 남아 있으나, 이보다 나중에 갱신된 R6 결과 수신 기록을 위 표에 사용했다. R4의 86.37은 원문 내 별도의 종합 필드가 아닌 구성합이다. 공식 Survival Rate / Tracking Score의 시나리오별 구성 값은 위 조회 문서에 없어 만들지 않았다.
- **시나리오 해석:** R2→R4에서 rough 실점은 `8.17→8.00`으로 떨어지고 전진은 `11.24→11.34`로 상승했으며 R6에서도 rough는 `8.02`다. 과거 공식 기록에서 **rough가 계속 주의 축**이었다는 맥락과 이번 로컬 H5 진행 손실은 *정성적으로 일관된 위험 신호*다. 다른 제출·훈련 설정·평가 프로토콜이므로 이 정책의 공식 rough 점수를 예측하거나 reward의 인과 효과를 설명하지는 못한다.

**가장 직접적인 관련 후보의 문헌 비교(일치 조건 미검증):** GitHub의 [JOINT tracking 기존 `model_4950` 보고서](https://github.com/SE3C/naver-issacsim/blob/main/research/experiments/h1/exp-h1-joint-tracking-balance.md)는 **다른 SHA** `2df05840…62bc478`의 PERSONAL H5 진행 평균/P05 `8.853/8.403m`, H1 body 전진 `−0.259m`, H3 world 잔류 `0.739m`을 기록한다. 이번 단독 ZIP은 각각 **8.024/7.460m, −0.719m, 1.160m**다. 겉으로는 rough·정지·횡잔류가 모두 불리하지만, 상대 원자료·resolved config·실제 경로를 이 입력에서 재대조하지 않았으므로 **정식 matched A/B 우열·새 조합의 원인**이라고 하지 않는다. 이 비교는 다음 CPU 확인의 우선순위를 잡는 데만 사용한다. 새 `model_2850`을 이전의 다른 `model_2850` 정책들(ORIENT-100, ACTRATE-001)과도 이름으로 합치지 않는다.

## 6. 최종 판단과 다음 행동 *한 가지*

**현재 상태: HOLD — 이미 충분한 독립적 이동 능력의 신호는 있지만, 정지·횡명령의 불필요한 후진과 rough 저속 꼬리 때문에 공식 제출 주후보 PROMOTE 근거가 부족하다.** H2·H6·H7의 안정 보행·고정 시간창 무접촉 종료는 긍정적이다. 경사 단독 목적이면 유망할 수 있지만, 이는 8 case 중 일부의 강점이다. 계단·박스와 같은 광의 보행의 20초 연속 완주는 별도로 입증되지 않았으며, 그 공백 하나로 공식 H1 후보를 REJECT하지도 않는다. 공식 7시나리오에 이 두 지형의 정량 case가 없기 때문이다.

**다음 행동은 GPU 없이 저장된 평가 원자료의 CPU 대조 *한 가지*:** 이번 체크포인트 `4a343750…`와 기존 JOINT `2df05840…`의 **완료된** Windows `scenario7` ZIP 원자료를 같은 기준으로 재집계한다. 우선 policy SHA, `protocol_id`, 전체 `resolved_configs.json`, source fingerprint, case/command·seed·num_envs·난수/terrain 조건의 parity를 확인하고, H5 전진의 cohort 대응 차이 분포·P05·최악 tail, H1 signed body drift, H3 vy error/세계좌표 잔류, H4 yaw, H6 action/RP의 동시 trade-off를 제시한다. **상대 ZIP은 이번 사용자 첨부에 없으므로 이번 보고서에서 대응 계산을 실행했다고 말하지 않는다.** 비교 조건이 다르면 그 차이만큼 결론을 제한한다. 이 CPU 비교 결과가 rough 손실 없이 다른 공식 목적축의 뚜렷한 이득을 보인다면 HOLD 재검토, 반대로 정지·rough 모두 악화가 확인되면 주후보 REJECT로 조정할 근거가 생긴다. 새 학습·GPU 평가·영상 생성·export·제출은 권고 또는 실행하지 않는다.

### 재현 파일과 원자료 위치

| 파일 | 역할 |
| --- | --- |
| **원본 입력 ZIP 내부** `evaluation/episodes.jsonl` | 개별 episode 수치와 `episode_id`/cohort/종료 사유; 수치의 1차 출처 |
| **원본 입력 ZIP 내부** `evaluation/diagnostics.json`, `evaluation/evaluation_manifest.json`, `evaluation/resolved_configs.json` | summary 교차검산과 실제 평가 조건·policy/protocol identity |
| **원본 입력 ZIP 내부** `environment.txt`, `source_checkpoint.txt`, `evaluation/video_evaluation_link.json`, `SHA256SUMS.txt`, 여섯 MP4 | 영상 시간표·영상/평가 연결 및 영상 관찰 근거 |
| `verification.json` | 체크포인트·프로토콜·episode ID·cohort·실패 분모·진단 요약 일치·영상 SHA6/6 결과 |
| `case_metrics.csv` / `case_seed_metrics.csv` | 직접 계산한 case 평균·quantile·seed별 평균 |
| `outlier_episodes.csv` | H5 전진/stall, H1·H3·H4 대표 하위·상위 꼬리의 raw episode 위치 |
| `video_inspection.json`, `video_frames/*.jpg` | 6영상 프레임 디코딩·검정 프레임 검사 및 명시 시점 시각 표본 |
| `reproduce_analysis.py` | 입력 ZIP을 열어 case/seed CSV, outlier, verification, H5 히스토그램 생성하는 **CPU-only** 재현 코드 (Python + pandas/numpy; matplotlib 있으면 그림 출력) |

**검증 완료:** ZIP CRC PASS, 6영상 MP4 manifest SHA PASS, episode ID 3,072/3,072 유일, cohort 3,072/3,072 유일, 8 case 전체 384행, policy/protocol SHA 모든 행 일치, diagnostics tracking·survival 교차검산 일치, `forward_progress_m == integrated_body_forward_m` 전 행 일치. 대상 입력·원본 MP4·원본 checkpoint는 수정하지 않았다. 현재 분석에서 GPU 작업·외부 업로드/게시·공식 서버 변경은 수행하지 않았다.
