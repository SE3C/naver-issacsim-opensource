> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/incoming/other/reviewed/H1_LINTRACK075_ACTRATE0001_TERM50_FRESH3K_MODEL2850_POLICY_ANALYSIS_20261018/H1_LINTRACK075_ACTRATE0001_TERM50_FRESH3K_MODEL2850_POLICY_ANALYSIS_20261018.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# H1 LINTRACK-075 + ACTRATE-0001 + TERM-50 / `model_2850` 정책 심층 분석

**작성·조회 기준:** 2026-10-18 KST · **주판정: HOLD — 현재 H1 공식 제출 대표로 채택 보류.**\
**대상:** 입력 통합 ZIP 1개, Windows PERSONAL H1 고정 6영상 + camera-off `scenario7`. 아래 숫자는 별도 표기가 없으면 **이번 ZIP의 `evaluation/episodes.jsonl` 3,072행을 직접 계산**했다. 학습 이력과 실제 공식 제출은 이번 ZIP만으로 입증되지 않는다.

## 1. 결론 — 걸어서 진행한다. 그러나 회전·방향 추종 비용이 크다

이 정책은 **단순히 쓰러지지 않는 정책을 넘어** H2 전진에서 **15.107 m**, H5 요철에서 **9.867 m**(P05 **9.640 m**, 최소 **9.514 m**), H6 상·하 경사에서 각각 **20.113/19.967 m**, H7 밀침 case에서 **10.126 m**의 **body-frame 전진속도 적분**을 기록했다. H5에서 `stall_fraction > 0.05`인 episode는 **0/384**, 최대도 **0.009**로, 측정된 험지 약점은 장시간 정지나 낙상이 아니다. 모든 **3,072/3,072개** 평가 episode가 20초 `timeout`으로 종료됐고 `base_contact_failure=true`는 없다. 초기 요철·박스 지형을 지나 빠져나오는 시각적 진행도 확인했다.

반면 **yaw 추종과 의도된 경로 유지**가 주요 약점이다. 전체 episode 동일가중 `mean_tracking_error` **0.251289**(서로 다른 단위의 3축 오차를 합친 내부 진단값), 전체 `yaw_error` **0.22279 rad/s**. H4 회전의 yaw 절대오차 평균 **0.2725 rad/s**, H5 요철 직진 명령의 yaw 절대오차 **0.2730 rad/s**가 특히 높다. 제자리 H1에서 명령 `0,0,0`인데 **body 전진 누수 0.298 m**와 **최종 월드 XY 순변위 크기 평균 0.857 m**가 있고, H3 좌우 `vy=+0.3→-0.3 m/s` 왕복에서는 body 전진 누수는 **0.277 m**에 그치지만 **최종 월드 XY 순변위 크기 평균이 2.605 m**이다. *월드 원점 복귀는 공식 독립 채점 항목이 아니나, 방향·위치 제어의 중요한 비용 신호다.*

**추천:** 공식 7시나리오 기준 **HOLD(주후보 승격 보류)**. *험지 저속 꼬리 감소와 정지 중 body 전진 감소 가능성*은 보존할 가치가 있다. 그러나 H3 위치 잔류, 거의 전 case에 나타난 yaw 오차, H6 큰 action 변화가 경쟁력 리스크다. 다단 계단 중앙 완주 미입증 **그 자체**는 공식 후보 탈락 사유가 아니다. 기존 같은 evaluator 자료와 CPU에서 비교해 **얻은 진행 이점이 yaw·횡이동 비용을 정당화하는지** 먼저 판정한다. 이번 평가의 완료(`COMPLETE`)는 채택 또는 공식 점수의 성공이 아니다.

## 2. 정책 identity·평가 조건과 신뢰성

| 확인 항목 | 이번 자료에서 확인된 값 |
| --- | --- |
| 표시명 | `LINTRACK075_ACTRATE0001_TERM50_FRESH3K_MODEL2850` — ZIP 파일명의 **표시명**이며 학습 config/Run 검증 결과가 아님 |
| checkpoint 기록 | `model_2850.pt`로 지칭된 Windows staging 입력; SHA-256 `8238421049335a19c288986ed58aa84f01468da315fbf6c355ee45088934f959` |
| 정책 연결 | `source_checkpoint.txt`·`evaluation_manifest.json`·`video_evaluation_link.json`·전체 episode 행에 동일 SHA. **원본 `.pt` 자체는 ZIP에 없어 체크포인트 바이트 독립 SHA 재계산 불가** |
| 평가 ID | `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34`, `internal-suite-v1`, deterministic actor |
| 평가 실행 | `PERSONAL`, `COMPLETE`, `complete=true`, `smoke=false`, evaluator child exit 0; 2026-10-18 **01:01:32 KST** 종료 |
| 분모 | H1~H5/H7 각 **384**행, H6 상/하 각 **384**행 → **8 case×3 평가 seed(4201~4203)×128 env=3,072**; 20초·1,000 steps/episode |
| cohort·종료 | `(scenario,case,seed,env_id)` **3,072개**, 중복 episode ID 0, reset 후 추가 episode 0, **terminated 발생 cohort 0/3,072**; 모두 `timeout` |
| source | 평가 task repo `ef10b7a4…655f72214`, IsaacLab `3e73d6d…`; 평가 `source_fingerprints`와 applied env·agent fingerprint 존재. 평가 당시 RTX 3060 Laptop GPU |
| 학습 이력 | ZIP 내부 `policy.preset=null`, `source_run_id=null`. **fresh 3K·reward 값·원 학습 Run·OFFICIAL 학습 출처는 파일명만으로 미검증**. 실제 제출·공식 채점 근거 없음 |

ZIP CRC 전체 검사와 `SHA256SUMS.txt`의 **6/6개 MP4 SHA 검증 통과**. `evaluation/evaluation.log`에는 `execution_status=COMPLETE`, `[CHILD EXIT] 0`이 있고 `Traceback`/`FATAL`/`ERROR`를 찾지 못했다. `diagnostics.json`의 7시나리오별 tracking 평균과 survival은 raw 재집계와 부동소수점 오차 범위에서 일치한다. 원자료 NaN/누락 없음. `forward_progress_m == integrated_body_forward_m`는 **3,072/3,072행**에서 성립하며 별개 독립 근거로 세지 않는다.

**주의할 설정 차이:** `evaluation/resolved_configs.json`과 evaluator 로그의 reward manager 스냅샷에는 `track_lin_vel_xy_exp=0.50`, `action_rate_l2=-0.0005`, `termination_penalty=-5`가 표시된다. 반면 ZIP **이름**은 `lin=.75`, `action=-.0001`, `term=-50`을 암시한다. 전자는 **평가 때 로드된 환경 설정**이지 원 학습의 resolved reward 증거가 아니다. actor의 deterministic inference에서 보상 가중치를 training identity로 역추정하지 않았다. 실제 학습 reward/seed/PPO/resume 계보가 필요한 판단에는 별도 학습 evidence가 필요하다. 또한 이번 source 및 명령·지형·noise 조건을 *기존 후보와 비교하여 동일하다고* 확정한 것은 아니다.

**case 입력:** H1 정지 `vx=vy=yaw=0`; H2 전진 `vx=0.5→1.0`; H3 횡이동 `vy=+0.3→-0.3`; H4 회전 복합 `vx=0.5,yaw=+0.5→-0.5`; H5 rough `vx=0.5`; H6 오르막·내리막 각 `vx=1.0`(slope 설정 10°); H7 flat+push `vx=0.5`, push delta 0.5. 평가 명령은 episode **10초**에 전환, 카메라 없음. 한 episode 20초. H1 공식 제출 7시나리오와 로컬 8 case에 **계단·박스 정량 case는 없다**. `stall_fraction`은 유효 명령속도가 0.2 m/s 이상인 step의 속도 부족 비율이며 **H1의 0은 제자리 유지 성공의 증거가 아니다**.

## 3. 정량 분석 — 진행 이점과 yaw/경로 비용을 분리

| 로컬 case (각 n=384) | tracking ↓ (혼합 단위) | `vx` 오차 ↓ m/s | `vy` 오차 ↓ m/s | yaw 오차 ↓ rad/s | body 전진 적분 ↑ m | 진행 P05 / 최소 m | stall 평균 | roll/pitch RMS | action Δ RMS |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| H1 정지 | 0.1903 | 0.0219 | 0.0766 | 0.1648 | 0.298 | 0.293 / 0.291 | 0.0000* | 0.0203 | 0.5011 |
| H2 전진 | 0.2345 | 0.0288 | 0.0673 | 0.2048 | **15.107** | 15.096 / 15.083 | 0.0030 | 0.0338 | 0.6037 |
| H3 횡왕복 | 0.2016 | 0.0227 | 0.0740 | 0.1734 | **0.277**† | 0.266 / 0.262 | 0.0080 | 0.0323 | 0.4984 |
| H4 회전 복합 | 0.2933 | 0.0256 | 0.0682 | **0.2725** | 10.199 | 10.197 / 10.195 | 0.0030 | 0.0319 | 0.5469 |
| H5 rough | **0.3019** | 0.0498 | 0.0607 | **0.2730** | **9.867** | **9.640 / 9.514** | 0.0041 | 0.0366 | 0.5717 |
| H6 상행 +10° | 0.2838 | 0.0438 | 0.0608 | 0.2566 | 20.113 | 19.987 / 19.950 | 0.0020 | 0.0463 | **0.6621** |
| H6 하행 −10° | 0.2901 | 0.0423 | 0.0619 | 0.2616 | 19.967 | 19.862 / 19.805 | 0.0020 | 0.0427 | **0.6609** |
| H7 밀침 | 0.2149 | 0.0348 | 0.0732 | 0.1756 | 10.126 | 10.071 / 10.058 | 0.0030 | 0.0341 | 0.5597 |

*`H1`의 분모 없는 stall=0 해석 주의. †`H3`의 0.277m는 본래 전진 명령이 없는 구간의 **비의도 전진 성분**, 횡이동 거리나 왕복 성공거리가 아니다. `lateral_drift_m`는 실제 횡변위가 아니라 `|vy 오차|`의 시간적분이다. `world_dx_m/world_dy_m`은 월드 **최종 순변위**이며 총 이동 경로 길이가 아니다. 모든 평균은 **episode 동일가중**; 이번에는 case별 384행으로 **8-case 동일가중 평균도 0.251289**와 같다. H6를 768행인 하나의 시나리오로 본 `diagnostics.json`과 case 동일가중 비교를 혼동하지 않는다.

8 case tracking 비교〔원본 참조: `figures/tracking_by_case.png` / 공개 사본 미포함〕
8 case yaw 절대오차〔원본 참조: `figures/yaw_error_by_case.png` / 공개 사본 미포함〕

**강점의 범위.** H2의 body-frame 15.107m는 명령상 `0.5×10s + 1.0×10s = 15m`에 가깝다. H5는 최소·P05도 평균 근처여서 이번 3개 **평가** seed의 극단적 저속 정체 신호가 작다. H5 `stall>0.05` **0/384**, P95 tracking **0.32259**, 최악 tracking episode는 `seed4203/env27`: 0.34070, body 진행 9.539m, stall 0.008. 즉 **느린 보행·yaw 편차는 있어도 극단 정체는 아니다**. H7는 진행 10.126m·20초 384/384 생존으로 push 조건 하 계속 움직일 수 있으나 **충격 직후 수 초 회복시간**을 산출하는 필드는 없다.

**치명적 trade-off.** H3 순월드변위 크기 평균 **2.605m**(개별 최대 **2.691m**, `seed4202/env111`)는 같은 case에서 ±0.3m/s 좌우 왕복을 수행하면서 위치·방향이 적지 않게 벗어났음을 시사한다. H1 순월드변위 0.857m도 body 누수 0.298m보다 커, body 적분 하나만으로 정지 정밀도를 주장하면 안 된다. H2 직진은 body 적분 **15.107m** vs 종료 순월드변위 크기 **13.400m**, H6 상·하는 **20.113/19.967m** vs **17.848/17.033m**다. 이것은 방향 회전·경로 굽음·횡운동과 일관되지만, 영상으로 물리 slip의 정밀량을 확정할 수는 없다. H6 roll/pitch RMS **0.0463/0.0427**, action Δ RMS **0.6621/0.6609**도 평지보다 높은 행동 비용이다. `action_delta_rms`가 높다고 발 미끄럼·관절 torque를 직접 측정했다고 쓰지 않는다.

H5 progress 384 episodes 분포〔원본 참조: `figures/h5_progress_distribution.png` / 공개 사본 미포함〕

**평가 seed·최악 꼬리:** H5 전진 평균은 seed 4201/4202/4203에서 각각 **9.860/9.865/9.875m**, P05 **9.637/9.660/9.641m**, 최소 **9.575/9.567/9.514m**다. 최악 진행 `4203/env121` **9.514m**는 낙상·장시간 stall 사례가 아니다(`stall=0.003`). H5 stall 최대 `4201/env10` **0.009**. H3 세계 좌표 종료 잔류는 세 평가 seed 모두 평균 **2.604~2.607m**다. 이 128env×3seed는 **독립 학습 seed 반복이 아니고**, 시나리오가 같다고 실제 terrain/reset 궤적이 정책 간 동일한 것도 아니다. 개별 숫자·전체 분포는 `derived/seed_case_metrics.csv`, `derived/tail_episodes.csv`에 보존했다.

## 4. 6영상 확인 — 장애물 접촉·진행·캡처 결함

**서로 다른 실험:** 영상은 seed=42, **1 env**, 50fps×1,000프레임(20초), 시작 명령 `vx=1.0`(0~6s), 다음 `vx=0.5,vy=+0.3`(6~10s), `vx=0.5,vy=-0.3`(10~14s), `vx=0.5,yaw=+0.5`(14~17s), `vx=0.5,yaw=-0.5`(17~20s). 월드 Y 방향 ±0.5m/s 속도 impulse는 **4/8/12/16초**. camera-off evaluator의 10초 전환·독립 terrain/reset 조건과 동일 재측정이 아니다. 추적 카메라 기준 화면 중앙 체류는 제자리 정체의 증거가 아니다.

**실제로 조사한 범위:** 각 영상 **전체 1,000프레임을 순차 디코딩해 검정 프레임을 검사**했고, **f1,100,200,300,400,500,600,700,800,900,975,999 및 그 인접 프레임**의 화면을 조사했다. 종료 구간은 추가로 f996~999를 6개 영상 모두 대조했다. 즉 *전 프레임 행동·접촉 궤적의 수동 판독 완료*가 아니라 대표 시각과 인접 프레임의 행동 확인이다. 발 접촉의 ms 수준, 진동 주파수, push 이후 초 단위 복귀는 미측정.

| 영상 | 직접 본 시각·프레임과 실제 관찰 | 행동 판단 및 검증 경계 |
| --- | --- | --- |
| `01_stairs.mp4` | f1(0.02s) 계단 가장자리 부근에서 직립; f100(2s) 계단 모서리 근처 이동; f200~400(4~8s) 계단 띠가 뒤·구석으로 빠지고 로봇은 직립 보행; f500~975(10~19.5s) 화면상 평지에서 계속 발걸음 | **접근·가장자리 경유 후 진행**은 관찰, 중앙 다단 계단의 단계별 승·하강이나 전체 완주는 불명확. f999만 몸체 렌더 소실 |
| `02_inverted_stairs.mp4` | f1,100(0~2s) 역계단의 가장자리·모서리 근처를 경유; f200~300(4~6s) 계단 구조가 화면 밖으로 이동; f400~975 서 있는 채 전진 동작 | 모서리 주변 진행·균형 관찰. **중앙부 다단 하강 완주**는 보이지 않아 증명하지 않음. 전부 검정인 영상 아님 |
| `03_boxes.mp4` | **유효 홀수 프레임** f1(0.02s), f101(2.02s)은 박스 군집 속/경계에서 보행; f201(4.02s) 박스 가장자리로 빠져나옴; f301(6.02s) 이후 평지 구간. f401/601/801/997도 계속 서 있음 | **실제 박스 구간 접촉·통과 구간 존재**. 다만 전체 박스 패치의 중앙 횡단·foot slip/충격 반응 정량 판정은 불가. **짝수 f0,2,…,998 총 500/1000 검정**, 인접 홀수 정상 — capture artifact이며 낙상 아님 |
| `04_random_rough.mp4` | f1(0.02s), f100(2s) 요철 패치 위 보행; f200(4s) 패치 가장자리; f300(6s)부터 패치가 뒤로 빠짐; f400~975는 평지성 배경에서 자세 유지·보행 | **초기 rough 구간을 실제 진행**하며 정량 H5의 저정체 결과와 방향성 부합. 영상 후반 20초 생존을 *20초 연속 rough 전진*으로 오독하지 않음. f0·f2 검정 |
| `05_slope_up_10deg.mp4` | f1,100,200(0~4s) 경사 지형으로 구성된 표면에서 직립 보행, f300~975 지속 보행; 지면 대비 각도 판독은 카메라 때문에 어려움 | +10° 설정은 `environment.txt` 근거, **경사 실제 거리/경사 정상 통과**는 화면만으로 계측 불가. camera-off H6 상행 20.113m는 별도 조건 |
| `06_slope_down_10deg.mp4` | f1,100,200(0~4s) 하행 경사 설정의 표면에서 보행, f300~975 자세 유지·이동, 명령 회전 구간에서도 보행 | −10° 구성과 보행 지속 확인. 경사 중심부 전체 하강이나 슬라이딩 양적 판정은 못 함. H6 하행의 19.967m는 별도 평가 |

**푸시/전환을 관찰한 범위:** push 예정 f200/400/600/800 및 뒤 인접 프레임, 명령전환 f300/500/700/850 전후 대표 표본에서 급격한 낙상 없이 지속 직립·보행이 보인다. 이는 **연속 자세 유지와 행동 재개 정성 신호**이며, 한 프레임만으로 순간 밀림이 없었다거나 규정 시간 내 회복했다고 주장하지 않는다. **6개 영상의 마지막 f999에서 로봇 몸체가 사라지고 시각화 마커만 남는 공통 렌더/종료 아티팩트**가 있으며 바로 앞 **f996~998에는 몸체가 직립**해 있다. 이 화면 소실은 정책 낙상으로 세지 않았다. 나머지 5영상은 초기 검정이 `f0` 1개(rough는 `f0,f2` 2개)이고 1,000프레임 디코딩 가능하다. 인접 프레임과 마지막 프레임 증거는 `video_keyframes/` 및 `derived/video_probe.json`에 기록했다.

## 5. 기존 제출·정책 기록과의 연결 (직접 동일조건 A/B와 구분)

**GitHub 연결 읽기 전용 확인(2026-10-18):** `SE3C/naver-issacsim`의 [`research/EXPERIMENTS.md`](https://github.com/SE3C/naver-issacsim/blob/main/research/EXPERIMENTS.md), [`research/submission_presets/README.md`](https://github.com/SE3C/naver-issacsim/blob/main/research/submission_presets/README.md) 및 이전 H1 원자료 재집계 JSON을 조회했다. 이번 ZIP의 SHA `82384210…34f959`를 해당 두 연구기록·연결 검색에서 확인하지 못했으므로 **어느 공식 학습 Run/제출 정책에도 귀속하지 않는다.** 비슷한 `model_2850`이라는 이름의 `ORIENT-100`(SHA `6aed…`) 및 `ACTRATE-001`(SHA `1e6d…`)과 명백히 다르다.

**과거 PERSONAL evaluator 저장 집계(참고만, 새로운 raw 대응 비교 아님):** [`2026-10-10 H1 3정책 raw 요약 JSON`](https://github.com/SE3C/naver-issacsim/blob/main/data/processed/experiments/h1/2026-10-10_H1_SCENARIO7_RAW_SUMMARY.json)은 이전 `TERM-50/model_2800` SHA `dffaa7…09ad6`, `ACTRATE-0001/model_2700` SHA `e54d…ca7ae`의 독립 보존 ZIP에서 나온 수치다. 그 작업은 이전 세 후보의 protocol/평가 설정 일치를 확인했으나, **이번 신정책 ZIP과 이 두 원본 ZIP을 다시 직접 결합·대응 검증하지는 않았다.** 아래 값은 의사결정 방향을 위한 *출처가 다른 참고 집계*로만 본다.

| 지표 (같은 로컬 정의, **미대응 참고**) | 이번 823842 / 2850 | 기존 TERM50 / 2800 | 기존 ACTRATE-0001 / 2700 |
| --- | ---: | ---: | ---: |
| 전체 episode tracking ↓ (혼합 단위) | **0.25129** | 0.15712 | 0.14534 |
| H1 정지 시 body 비의도 전진 ↓ m | **0.298** | 1.352 | 1.987 |
| H3 최종 월드 XY 순변위 크기 ↓ m | **2.605** | 0.973 | 0.669 |
| H4 yaw 절대오차 ↓ rad/s | **0.2725** | 0.1193 | 0.1183 |
| H5 body 진행 평균 / P05 ↑ m | **9.867 / 9.640** | 8.896 / 8.533 | 9.948 / 9.592 |
| H5 yaw 절대오차 ↓ rad/s | **0.2730** | 0.1322 | 0.1343 |
| 전체 action Δ RMS ↓ | **0.57558** | 약 0.36529 | 약 0.45687 |

이번 후보는 과거 TERM50 참고 대비 **정지 중 body 전진 누수는 작고 H5 하위 진행은 좋지만**, 순월드 이동의 H3 잔류와 **H4/H5 yaw 및 전체 추종·action 비용은 크게 악화한 방향**이다. ACTRATE2700 대비 H5 최저 꼬리는 좋아도 **평균 진행은 낮으며 tracking은 더 높다**. 이는 **학습 reward 효과·과거 제출 대비 실제 개선률**로 계산하거나 확정한 결과가 아니다. 실제 A/B에는 평가 resolved config/source fingerprint, command, noise, terrain, checkpoint 선택 및 cohort 키의 직접 대조가 선행돼야 한다.

**확인된 과거 H1 공식 시뮬레이션 점수** — 각각 *다른 실제 제출물*의 수신 기록, 이번 SHA의 점수가 아님:

| 공식 시나리오 / 배점 | R2 TERM50 (2026-09-09 제출) | R4 AIRTIME025 (2026-09-28 제출) | R6 ACTRATE0001 (2026-10-11 제출) |
| --- | ---: | ---: | ---: |
| 제자리 / 10.5 | 8.62 | 8.58 | 8.60 |
| 전진 / 14 | 11.24 | 11.34 | 11.30 |
| 좌우 / 7 | 5.73 | 5.72 | 5.73 |
| 회전 / 7 | 5.66 | 5.68 | 5.68 |
| 요철 / 10.5 | **8.17** | **8.00** | **8.02** |
| 경사 / 10.5 | 8.47 | 8.53 | 8.52 |
| 밀침 / 10.5 | 8.48 | 8.52 | 8.50 |
| **시뮬레이션 합 / 70** | **56.37** | **56.37** | **56.35** |

출처: [R2 사용자 전달 공식 결과 검토](https://github.com/SE3C/naver-issacsim/blob/main/data/processed/experiments/h1/analysis/2026-09-10_OFFICIAL_EVAL_H1_ROUND2_TERM50.md) · [R4 공식 결과 검토](https://github.com/SE3C/naver-issacsim/blob/main/data/processed/experiments/h1/analysis/2026-09-30_OFFICIAL_EVAL_H1_ROUND4_AIRTIME025.md) · [R6 사용자 전달 공식 결과 후속 기록](https://github.com/SE3C/naver-issacsim/blob/main/data/processed/experiments/h1/analysis/2026-10-16_H1_ANGXY008_MODEL4650_POLICY_REVIEW.md) · [실제 제출 Release R2/R4/R6 및 preset 안내](https://github.com/SE3C/naver-issacsim/blob/main/research/submission_presets/README.md). R4 **86.37/100은 56.37+20+10의 구성 합산**, R2 종합 86.37, R6 수신 종합 86.35. R6 점수 갱신은 일부 오래된 preset README의 “score unknown” 문장보다 후속 사용자 수신 기록을 우선했다. **운영진이 공개한 시나리오별 Survival Rate/Tracking Score의 분리 값은 조회 자료에 없어 역산하지 않았다.** 공식 요철의 R2→R4 8.17→8.00 및 R6 8.02는 개선 필요 배경이지만, 이번 H5 진행 증가가 공식 요철 점수를 올릴지 예측할 수 없다.

## 6. 최종 판정과 다음 한 단계

**HOLD, 현재 공식 H1 대표 정책 대체 비추천.** 의미 있는 **전진·요철 진행·20초 무접촉 종료**는 확인됐고, rough P05·최소 진행은 보존 가치가 있다. 하지만 **H4·H5 yaw 오차 0.27rad/s대, H3 큰 종료 순변위, 높은 action Δ**는 현 목표인 **7시나리오 균형 있는 추종·안정성**의 직접적인 불리 신호다. 정성 보조 목표인 계단 중앙 완주 여부는 이번 시각근거의 빈칸이지 현재 HOLD의 주원인이 아니다. 광의의 초반 요철·박스 통과 가능성은 **긍정적**, 전지형·경로정확도·단차 완주까지 입증된 것은 **아님**. 고정 평가에서 종료가 없으므로 회복 능력의 stress test를 통과했다기보다는 *지정된 작은 perturbation에서 20초 동안 낙상 없이 계속 움직였다*고 판단한다.

**다음 행동 한 가지(새 GPU 비용 0):** 이미 보존된 `TERM-50/model_2800`과 필요시 `ACTRATE-0001/model_2700`의 원본 `episodes.jsonl`을 확보해, 이번 3,072개 cohort와 **평가 protocol·resolved config/source fingerprints를 먼저 대조한 후 CPU에서 동일 key 비교**한다. 우선 질문은 `H5 P05/최소 진행 증가`가 `H3 세계순변위·H4/H5 yaw·전체 action Δ/추종 손해`를 동반해도 **공식 7시나리오 대표 후보로 바꿀 가치가 있느냐**다. 대응 명령·지형 실체가 다르면 case 단위 참고 비교만 허용한다. 동일 조건에서 yaw/횡이동 손해가 재현되고 진행 이점이 충분하지 않으면 이 후보를 **REJECT로 내린다**. 반대로 실제 H3 추종·H4 yaw 비용이 감당 가능하고 진행의 하위 꼬리 이점이 유지되면 PROMOTE 후보로 재검토한다. 지금 단계에서 새 학습·렌더·evaluation을 실행할 이유는 없다.

**재현 근거:** 입력 ZIP의 `source_checkpoint.txt`, `environment.txt`, `evaluation/evaluation_manifest.json`, `resolved_configs.json`, `episodes.jsonl`, `diagnostics.json`, `video_evaluation_link.json`, `evaluation.log`, MP4 6개. 결과 ZIP에는 raw 파일을 중복하지 않고 `derived/case_metrics.csv`, `seed_case_metrics.csv`, `tail_episodes.csv`, `summary.json`, `video_probe.json`과 재집계·영상 점검 스크립트, 그림·선택 프레임 montage를 동봉한다. 직접 계산하지 않은 역사 점수는 위 출처 링크로 확인한다. **원본 ZIP·MP4·checkpoint/서버/평가기 변경 없음.**
