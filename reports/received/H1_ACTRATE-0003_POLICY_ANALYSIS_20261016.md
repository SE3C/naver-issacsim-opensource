> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/incoming/other/reviewed/H1_ACTRATE-0003_POLICY_ANALYSIS_20261016.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# H1 ACTRATE-0003 / model_2950 정책 6영상·camera-off 평가 심층 분석

- **분석일:** 2026-10-16 (KST)
- **대상:** 사용자 제공 Windows 통합 ZIP 1개, 단일 후보 `H1 ACTRATE-0003` (`action_rate_l2=-0.0003`, 공식 fresh3K에서 보존된 `model_2950.pt`)
- **판정:** **HOLD — 유용한 전진·횡이동·회전·밀침 대응을 확인했지만, 험지 하위 꼬리와 계단 중앙 통과 검증 공백 때문에 현재 범용/제출 대체 대표로 채택하지 않음.**
- **증거 구분:** 이 보고서의 3,072행 통계는 ZIP의 `evaluation/episodes.jsonl`을 **직접 재집계**했다. 비디오 관찰은 ZIP의 실제 MP4에서 시간표 기반으로 **선택 프레임과 인접 프레임**을 디코딩해 수행했다. 학습 Run·과거 점수는 연결된 GitHub 저장소의 **별도 기록**이며 이번 ZIP의 점수가 아니다.

## 1. 결론: 살아 있을 뿐 아니라 실제 이동하지만 전지형 완성은 아니다

**목표 행동 수행:** 이 정책은 20초 카메라 없는 H1 `scenario7`의 8개 case, 각 384 cohort에서 모두 `timeout`까지 유지했다(3,072/3,072; `base_contact_failure=false` 3,072행). 평지 가속 전진 **14.930m/목표 속도 적분 15m**, 밀침 전진 **9.796m/명령 적분 10m**, 회전 결합 전진 **9.796m/10m**, 상·하 경사 **20.049/19.856m/20m**로, 적어도 해당 *body-frame* 명령을 따라 실제 전진한다. H3 횡이동 왕복은 `vy_error=0.07035m/s`, 종단 world XY 순변위 크기 평균 **0.407m**이며 심한 정체가 없다. 이는 **20초 생존만 한 정책**과 구분되는 긍정적 행동 신호다.

**가장 중요한 약점:** H5 rough의 전진은 평균 **9.018m/명령 적분 10m**, 하위 5%값 **8.664m**, 최저 **6.771m**다. 최저 두 cohort에서는 `stall_fraction=0.225/0.085`와 높은 추종 오차가 동반되어, 넘어지지 않았지만 제때 나아가지 못하는 **국소적 저속·정체 취약성**이 분명하다. 정지 H1도 비의도 body 전진 적분 **0.382m**, world XY 최종 순변위 평균 **0.455m**가 남는다. 가시 영상에서 boxes·rough 초기 패치의 이동을 확인했지만 계단을 중앙으로 연속 완주했다고 볼 근거는 없다.

**추천:** 현재 성과를 부정하는 REJECT는 과하다. 평지 명령 추종과 10° 경사/밀침 고정 평가에는 유용하다. 그러나 더 넓은 조건에서 기존 대표를 대체하는 **PROMOTE도 이르다**. 평가가 COMPLETE인 것, 공식 서버에서 학습한 것, 정책 후보로 채택하는 것, 실제 제출/공식 점수는 전부 다른 상태다.

## 2. 체크포인트·실행 조건·무결성

| 구분 | 직접 확인한 값 / 출처 |
| --- | --- |
| 체크포인트 | `model_2950.pt`; SHA-256 **`1cc2c03197097c21c642e8373c760b25664b9c859ed75b5dc07582a770473c4b`**. `source_checkpoint.txt` · `evaluation_manifest.json` · `video_evaluation_link.json` · 3,072 episode의 SHA가 일치함 |
| OFFICIAL 학습 연결 | GitHub 기록의 Run **`20261016-033023-h1-actrate-0003-fresh3k`**, `h1-submit-2 + action_rate_l2=-0.0003`, fresh/no parent, 학습 seed42·4096env, 3000회 요청/콘솔2999, exit0·evidence validation PASS. 같은 SHA의 indexed keeper 2950에 연결. **자동 best2900 (`d12a7a86…`)은 다른 checkpoint** |
| 이번 PERSONAL 평가 | H1 `Humanoid-v0`, `scenario7`/`internal-suite-v1`, protocol **`d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34`**, `COMPLETE`, `complete=true`, `smoke=false`, `official_score=false` |
| 평가 개수 | **128 env × seed 4201·4202·4203 × 8 case = 3,072 최초 cohort**. 모든 case 20초·1000 step, 각 384행; H6은 상행384 + 하행384 |
| 평가 source | `source_fingerprints`: `h1_task/env_cfg.py=9116769a…`, `humanoid_rewards.py=050b8ee7…`; agent fingerprint `976cb139…`. 이번 ZIP 내 모든 case/seed의 resolved config 존재. 비교 ZIP이 없어 타 정책과의 fingerprint 동등성은 별도 확인하지 못함 |
| 6영상 | seed42·1env·20초·50fps/1000프레임·1920×1080, fixed `maneuver_push`, 지형 하나씩, slope ±10°, `video_evaluation_link.json`에 위 SHA가 연결됨 |
| 영상 무결성 | ZIP 18항목, CRC 검사 통과. `SHA256SUMS.txt`에 기록된 **여섯 MP4 각각의 SHA를 직접 계산하여 모두 일치** 확인 |
| ZIP 자체의 한계 | 원본 `.pt`의 바이트는 ZIP에 없음. 따라서 일치한 SHA 메타데이터와 GitHub index가 연결 근거이며 원 `.pt` 자체를 다시 해시한 것은 아님. ZIP 내부 `policy.preset=null`, `source_run_id=null`은 그대로 미기재 값 |

**서로 다른 실행 계약:** 영상 명령은 전역 비디오 step 기준 `0–299: (vx=1, vy=0, yaw=0)`, `300–499: (0.5,+0.3,0)`, `500–699: (0.5,-0.3,0)`, `700–849: (0.5,0,+0.5)`, `850–999: (0.5,0,-0.5)`이며, step 200/400/600/800에 world-Y ±0.5m/s push를 준다(`environment.txt`). 시각으로는 **0–6s 전진 → 6–10s 횡+ → 10–14s 횡− → 14–17s yaw+ → 17–20s yaw−**, **4·8·12·16s push**다. 이것은 6영상 각각 동일한 일정이다. 별도의 `scenario7` 평가는 case별 정지/전진/횡/회전/rough/경사/push 명령, 10초 전환 및 별도 seed·reset·지형 타일·noise와 randomization 설정을 가진다. 영상의 시간별 이동과 원자료 행은 **같은 episode가 아니다**.

`resolved_configs.json`과 manifest를 기준으로 평가 case는 H1=flat/정지, H2=flat/(0.5→1.0)m/s, H3=flat/vy(+0.3→−0.3)m/s, H4=flat/vx0.5+yaw(+0.5→−0.5)rad/s, H5=random_rough/vx0.5, H6=10° slope_up 및 slope_down/vx1.0, H7=flat/push/vx0.5다. **계단·박스는 시각 영상 전용**이고 `scenario7`의 정량 case가 아니다. 학습 reward 상세, train-side 교란과 평가 설정을 동등한 것으로 임의 확장하지 않았다.

## 3. 원자료 재집계 및 실패 집중도

다음은 `evaluation/episodes.jsonl`의 **episode 행 동일가중 평균**이며, 두 경사 case는 따로 집계했다. 추종 `mean_tracking_error`는 vx·vy·yaw-rate 오차의 step별 Euclidean 크기를 episode에서 평균한 **혼합단위 내부 지표**(↓)로, 일괄 m/s 단위를 붙이지 않는다. `vx_error`·`vy_error`는 절대 속도오차 평균(m/s), `yaw_error`는 절대 yaw-rate 오차 평균(rad/s)이며 `xy_rmse`·`yaw_rmse`와 다르다. 전진(m)은 **body-frame vx 적분**이다.

| Case (각 n=384) | 추종오차 ↓ | vx / vy 오차(m/s) ↓ | yaw 오차(rad/s) ↓ | 전진 적분(m) ↑ | stall 평균 ↓ | 자세 roll/pitch RMS ↓ | action Δ RMS ↓ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| H1 정지 | 0.08139 | 0.01930 / 0.06093 | 0.03996 | **0.382*** | 0.00000† | 0.06319 | 0.31236 |
| H2 전진 | 0.13897 | 0.02857 / 0.07922 | 0.08979 | 14.930 | 0.00600 | 0.04478 | 0.47423 |
| H3 횡왕복 | 0.09564 | 0.01483 / 0.07035 | 0.05068 | **0.192*** | 0.00911 | 0.06210 | 0.31555 |
| H4 회전+전진 | 0.11496 | 0.02005 / 0.07462 | 0.07047 | 9.796 | 0.00500 | 0.04863 | 0.40242 |
| H5 요철 | **0.16031** | 0.06897 / 0.06887 | 0.10004 | **9.018** | 0.00807 | 0.04377 | 0.40436 |
| H6 상행 10° | 0.18005 | 0.04983 / 0.07856 | 0.12787 | **20.049** | 0.00600 | 0.04224 | 0.55224 |
| H6 하행 10° | 0.18058 | 0.04874 / 0.08215 | 0.12535 | **19.856** | 0.00600 | 0.04195 | 0.55778 |
| H7 밀침 | 0.12904 | 0.03295 / 0.08003 | 0.07200 | **9.796** | 0.00694 | 0.04946 | 0.40911 |

\* H1/H3의 forward_progress_m는 목표 전진량이 아니라 **비의도 body 전진 누적량**이라 작은 값이 낫다. H3의 순수 lateral 왕복 목표는 vx=0이고, 전체 왕복 후 world 순변위는 0에 가까워야 한다. † H1은 명령 XY 크기가 0으로 stall 유효 분모가 없으므로 기록된 0은 정지 성공 근거가 아니다. `forward_progress_m`와 `integrated_body_forward_m`는 3,072행 모두 같아서 독립 증거로 중복 사용하지 않았다. `lateral_drift_m` 역시 world 횡거리 아닌 `|vy error|` 적분이라 실제 횡변위로 사용하지 않았다.

**요약 일치·분모:** 직접 집계한 scenario별 episode 추종 평균은 `diagnostics.json`의 H1 0.081393, H2 0.138970, H3 0.095639, H4 0.114959, H5 0.160307, H6 0.180317, H7 0.129044와 부동소수 오차 수준에서 같다. 전체 **3,072 episode 동일가중** 혼합오차 평균은 **0.135118**(H6 768행이 2배 가중). scenario 7개 평균을 각각 1/7 합한 값이나 공식 종합 점수가 아니다. `episode_id`·cohort `(scenario,case,seed,env_id)` 중복 0, 결측 0, 3,072행 전부 1000 step `timeout`, `survived=true`, `base_contact_failure=false`. 고정 20초당 한 번도 `terminated`되지 않은 cohort 3,072/3,072이므로 **'한 번이라도 종료' cohort 실패율 0/3,072**이며 raw 행 실패율과 이번에는 일치한다. 반복 reset의 긴 꼬리를 숨긴 결과는 아니다.

### 실제 의사결정에 중요한 발견

1. **정지/횡왕복의 남는 위치 제어 손실.** H1 명령 `0,0,0`에서 body 전진 +0.382m/20s, 최종 world XY 거리 `hypot(world_dx_m,world_dy_m)`의 **episode별 평균 0.455m**(중앙 0.455, P95 0.459). H3은 body 비의도 전진 +0.192m, 종료 world XY 순변위 **0.407m**(P95 0.435, 최대 0.458). `mean(world_dx),mean(world_dy)`를 계산 후 norm을 취하면 초기 yaw와 reset 위치가 다른 env들의 부호가 상쇄돼 이 값을 숨기므로 반드시 **각 episode에서 norm을 구한 뒤 평균**했다. 이는 해당 평가에서 심각한 횡정체보다는 작은 잔류 위치오차가 핵심임을 뜻한다. 단, 최종 위치잔류는 지정된 공식 Tracking Score 그 자체가 아니다.
2. **H5 요철의 평균은 쓸 만하지만 worst tail이 핵심 위험.** 384행 진행 **mean 9.018 / P05 8.664 / median 9.007 / P95 9.416 / min 6.771m**. 특히 `seed4202/env109`: 진행 **6.771m**, `stall=0.225`, `vx_error=0.1752m/s`, 혼합오차 0.2500. `seed4203/env65`: 진행 **7.493m**, `stall=0.085`, 혼합오차 **0.2769**, 자세 RMS **0.0781**. 두 행이 최저 진행과 집중된 stall을 만든다(`progress<8m` 2/384, `stall>0.05` 2/384, `stall>0.1` 1/384). 두 행 모두 낙상이 아니라 **속도를 유지하지 못한 20초 timeout**이다. H5의 최소/하위 꼬리를 평균 생존 100%로 가리면 안 된다.
3. **H6·H7은 진행과 자세 유지가 공존하지만 비용이 있다.** H6 상·하 각각 body 이동 약 20m, stall 평균 0.006, 자세 RMS ~0.042다. 동시에 H6 `yaw_error≈0.126–0.128rad/s`, `action_delta_rms≈0.55`로 H1 정지 0.312보다 행동 변화가 크다. 다른 명령·속도 조건이므로 바로 불필요한 에너지 낭비 또는 reward 원인으로 단정할 수 없다. H7은 외란 동안 9.796m 전진과 20초 timeout 384/384로 **비낙상 외란 견딤**은 확인되지만, per-push recovery time, 넘어졌다가 재기립한 성공률은 측정되지 않았다.
4. **seed별 일관성과 독립성 한계.** H5 진행 평균은 seed4201 **9.030m**, 4202 **9.019m**, 4203 **9.003m**; H5 tracking 평균은 각각 **0.1603 / 0.1597 / 0.1610**. 상행 진행 **20.042/20.057/20.050m**, 하행 **19.862/19.857/19.849m**(seed 순서 4201/4202/4203). 서로 비슷하지만 최저 두 episode가 다른 seed에서 나오므로 tail을 놓치지 말아야 한다. 이는 **평가 seed 3개이지 독립 training seed 3개가 아님**. `env_id`와 같은 seed는 원본 key로 유효해도 새 비교 정책의 실제 물리 initial state/terrain 동일성을 보장하지 않는다.

## 4. 여섯 실제 MP4의 행동 관찰

**판독 방법:** 6개 파일 모두 실제 디코딩. 각 1,000프레임·50fps를 검사하고 1–20s의 대표 지형 접근/이동/명령 전환(특히 f≈200/400/600/800와 인접 프레임) 및 후반 프레임, f994–999를 표본 확인했다. 여러 시점·인접 프레임에서 몸통과 발 자세·장애물/배경 상대위치를 검토했으나 **전체 6,000프레임의 연속 contact·foot sliding 정밀 추적은 수행하지 않았음**. tracking camera가 로봇을 화면 중앙에 두므로 배경 패치 이동을 함께 보았다. 6영상 공통 `f0`는 검정이며 f1·f2, push 전후 짝수·홀수 인접 표본은 유효 화면이다. **f999에서는 6영상 모두 몸체 대부분이 갑자기 사라져 작은 색 점처럼 보이고 f998은 정상 자세**다. 이는 캡처 종료 경계 이상으로 취급하며 낙상/회복 실패로 세지 않는다. 조사한 중간 프레임에서는 교대 검정 artifact가 보이지 않았다. **전체 프레임 자동 블랙 검사가 아니므로** 완전 무결함을 선언하지 않는다.

| 영상·핵심 확인 구간 | 관찰(선택 프레임에 근거한 사실) | 성능 해석·검증 범위 |
| --- | --- | --- |
| `01_stairs.mp4` f50–300 (1–6s), f395/400/401 (약 8s), f795/800/801 (16s) | 몸체가 선 자세로 번갈아 디디며 진행하고, 계단의 검은 단차 띠가 로봇 좌측 아래 방향으로 이동·화면 밖으로 이탈한다. 로봇은 주요 띠의 한쪽 가장자리 쪽에 보인다. push 전후 표본에서 쓰러진 모습은 없다. | **계단 인접 이동은 확인, 계단 중앙 다단을 실제 발로 연속 올랐다는 증거는 부족.** H2/H5/H6 수치는 stair case가 아니어서 계단 정량 완주로 사용할 수 없음. |
| `02_inverted_stairs.mp4` f50–250 (1–5s), f300–400 (6–8s), f700–900 (14–18s) | 역계단의 어두운 띠가 왼쪽으로 멀어지는 동안 로봇은 보행하며 자세를 유지한다. 중앙 다단 위에서 연속 착지하는 뚜렷한 구간은 표본에서 보이지 않는다. 이후 평탄한 외관의 타일에서 회전/전진 구간이 나타난다. | **단차 인접 탈출·계속 걷기**와 **단차 전체 성공 통과**를 구분. 사진 몇 장으로 발 끌림/슬라이딩 없음을 확정하지 않음. |
| `03_boxes.mp4` f50–300 (1–6s), f350–500 (7–10s), f600–800 (12–16s) | 초반 박스들이 로봇 주변·발밑 시야에 보이고, 로봇과 장애물의 상대위치가 바뀌며 경계 쪽으로 진행한다. 약 f350 이후 박스가 뒤로 남고 후반은 매끄러운 영역이다. 전환·push 구간 표본에서 몸통이 유지된다. | **실제 박스 패치에서 이동하는 긍정 신호**. 정확한 접촉력, 박스를 밟은 개수, 20초 전체가 박스 통과였는지, 단일 영상의 성공률은 미확인. |
| `04_random_rough.mp4` f50–250 (1–5s), f300–400 (6–8s), f700–850 (14–17s) | 초반 거친 표면에서 로봇이 이동하고 rough 패치 경계가 뒤쪽으로 빠져나간다. 후반에는 평탄한 패치에서 횡/회전 명령이 이어진다. 초기 거친 표면 표본에서 무너지지 않고 보행하는 형상이 보인다. | **요철 초기 진행은 H5 수치와 정성적으로 부합**. 그러나 영상 1env는 H5 `env109/65` 저속 꼬리를 보여주는 대응 episode가 아니다. 후반 평지 보행을 rough 완주 지속으로 과장하지 않음. |
| `05_slope_up_10deg.mp4` f50–300 (1–6s), f399–601 (8–12s), f799–850 (16–17s), f994–999 (끝) | 밝은 경사 템플릿 위에서 선 자세로 반복 보행한다. 밀침·횡/회전 명령 경계의 인접 표본도 자세를 유지한다. 마지막 **f998 정상 → f999 몸체 표시 이상**. | H6 상행 고정 평가의 20.049m/timeout은 **별도 case**에서 이동 능력을 정량 지지. 영상 카메라만으로 정확한 상향 고도차, 고정 지형 끝까지 완주를 산정하지 않음. |
| `06_slope_down_10deg.mp4` f50–300 (1–6s), f399–601 (8–12s), f799–850 (16–17s), f994–999 (끝) | 하행 템플릿에서도 전진/명령 전환에 맞춰 보행 형태를 유지하고 명백한 지속적인 바닥 몸통 접촉은 표본에서 보이지 않는다. **f998 정상 → f999만 몸체 표시 이상**. | 상행 대비 별도 H6 하행은 진행 19.856m·100% timeout으로 유용. 외형상 보이지 않는 접촉·발 슬립 또는 순간 자세 진동을 정량으로 만들어내지 않음. |

모든 비디오에서 명령은 **6초 이후 순수 전진이 아니다**. 따라서 횡·yaw 전환 이후 world X 증가가 작아 보이는 화면을 무조건 stall이라고 해석하지 않았다. f200/400/600/800의 밀침은 **외란 후 영상 표본의 비낙상 상태를 보여줄 뿐**, 재균형에 소요된 초나 공식 밀침 회복 성공률은 아니다.

## 5. 과거 기록과의 정확한 연결 — 이 후보의 공식 점수는 없음

GitHub 커넥터로 2026-10-16 KST에 `SE3C/naver-issacsim`의 [Experiment Registry](https://github.com/SE3C/naver-issacsim/blob/main/research/EXPERIMENTS.md), [ACTRATE Experiment 기록](https://github.com/SE3C/naver-issacsim/blob/main/research/experiments/h1/exp-h1-action-rate-relaxation.md), [제출 preset 표](https://github.com/SE3C/naver-issacsim/blob/main/research/submission_presets/README.md)를 읽었다. 이번 SHA `1cc2…0473c4b`는 **새 공식 fresh3K 학습 Run의 keeper2950**과 연결된다. 기록상 이 checkpoint의 **실제 제출이나 공식 평가 점수는 아직 없음**. [학습 evidence Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261016-exp-h1-action-rate-relaxation-action0003-fresh3k)는 레지스트리에서 제시된 원본 주소이며 Release archive의 내부 내용 전체를 이번에 재다운로드하지는 않았다.

기존 *다른 정책들의* 공식 이력은 H1 [R2 TERM-50](https://github.com/SE3C/naver-issacsim/blob/main/data/processed/experiments/h1/analysis/2026-09-10_OFFICIAL_EVAL_H1_ROUND2_TERM50.md) **56.37/70**(제자리8.62, 전진11.24, 횡5.73, 회전5.66, 요철8.17, 경사8.47, 밀침8.48), [R4 AIRTIME-025](https://github.com/SE3C/naver-issacsim/blob/main/data/processed/experiments/h1/analysis/2026-09-30_OFFICIAL_EVAL_H1_ROUND4_AIRTIME025.md) **56.37/70**(제자리8.58, 전진11.34, 횡5.72, 회전5.68, 요철8.00, 경사8.53, 밀침8.52), [R6 ACTRATE-0001 fresh10K/model_9999](https://github.com/SE3C/naver-issacsim/blob/main/data/processed/experiments/h1/analysis/2026-10-16_H1_ANGXY008_MODEL4650_POLICY_REVIEW.md#원문과-현재-기록의-차이) **56.35/70**(제자리8.60, 전진11.30, 횡5.73, 회전5.68, 요철8.02, 경사8.52, 밀침8.50)이다. R6 종합은 사용자 전달 기록에서 **86.35/100**, R2는 **86.37/100**, R4는 구성합 **86.37/100**이다. 이 값은 *제출 정책들의* 점수이며 포털 원문을 이번에 직접 열람한 것은 아니다. R2→R4→R6에서 요철은 **8.17→8.00→8.02/10.5**로 낮은 축이 남았다는 과거 관측은 이번 H5 하위 꼬리를 우선 점검할 이유지만, **이 후보의 다음 공식 점수를 예측하는 근거가 아니다**. 운영진의 공개 Survival Rate·Tracking Score 구성 수치는 이 자료에서 확인되지 않았으므로 만들지 않았다.

**참고할 내부 과거 행동치(이번에 raw 재집계한 상대 정책 아님):** 보존된 [Experiment 기록](https://github.com/SE3C/naver-issacsim/blob/main/research/experiments/h1/exp-h1-action-rate-relaxation.md)과 사용자 제공 프로젝트 문서 `20_H1_PUBLIC_FAILURES_AND_EXPERIMENT_PRIORS.md`에서 이전 `ACTRATE-0001` fresh3K **model_2700**의 H1 비의도 body 전진 **1.987m**, H3 비의도 body 전진 **1.677m**, H5 rough 평균/P05 **9.948/9.592m**가 보고돼 있다. 현재 `ACTRATE-0003`은 같은 종류의 지표에서 **H1 0.382m / H3 0.192m / H5 9.018/8.664m**다. 따라서 **정지·횡명령에서의 전진 누수 개선 가능성과 rough 진행 손해 가능성이 동시에 보인다**. 그러나 앞 정책의 전체 episodes·`resolved_configs.json`·source fingerprint를 이 작업에서 직접 대조하지 않았고 서로 다른 checkpoint 학습 이력이다. 이 차이를 **통제된 A/B 효과·reward=-0.0003의 인과효과·공식 점수 향상**으로 확정하지 않는다. 명목상 중간 reward 값 자체가 최적이라는 주장도 하지 않는다.

## 6. 최종 판단 및 다음 행동 한 가지

**HOLD (전지형 대표 후보):** 이번 정책은 정상 보행과 20초의 지속 진행·추종·외란 중 균형 유지를 재현한다. H3의 횡이동 정체나 H5 대량 낙상 같은 치명적 전면 실패가 없고, H1/H3 잔류 위치오차도 기록된 과거 일부 후보보다 작을 가능성이 있다. 반면 H5 최저 **6.771m**의 저속 실패, **두 outlier cohort**의 명백한 stall, 정지 잔류 **0.455m**, 계단/역계단의 **다단 중심 통과 부재**, 행동 Δ·yaw 손실은 범용 승격을 막는다. 목표가 *평지·경사 전진과 안정적 20초 밀침 견딤*으로 한정되면 활용 가치가 높다. 계단/박스를 포함하는 전지형 통과 또는 정밀 정지·장애물 근접 이동의 대표로는 보류한다. **새 정책의 공식 점수와 reward 인과효과는 판단하지 않는다.**

**다음 행동 딱 한 가지 (추가 학습/GPU 없이):** 보존된 기존 `ACTRATE-0001/model_2700` 또는 `TERM-50/model_2800`의 camera-off 통합 ZIP에서 `evaluation_manifest.json`, `resolved_configs.json`, `source_fingerprints`, `episodes.jsonl`을 읽고 **현재 SHA `1cc2…`와 동일 case·seed·env_id의 3,072 cohort 대응 CPU 재집계**를 수행한다. 1순위는 *같은 fresh3K 구조에서 action=-0.0001인 model2700*으로 **H1/H3 누수 감소와 H5 mean/P05/min 진행 손해가 같은 평가 계약에서 유지되는가**를 보는 것이다. 확인할 핵심은 (a) protocol 및 case/command/terrain/noise·source/agent fingerprint 동등성, (b) H5 낮은 5%·stall 집중도의 대응 cohort 분포, (c) H3 world XY 종료잔류·vy error와 H4 yaw error의 상쇄다. 기존 비교 ZIP이 현재 입력에 없으므로 이 작업은 **이번 보고서에서 실행하지 않았다**. 새로운 GPU 실행 없이 기존 자료만으로 상대 판정을 먼저 좁힐 수 있다. source가 서로 다르면 동일 기준의 직접 개선율을 보류하고 각자의 관찰은 유지한다.

### 재확인 근거 위치 및 검산

- **첨부 ZIP 내부:** `source_checkpoint.txt`, `environment.txt`, `README.txt`, `SHA256SUMS.txt`, `BUNDLE_README.txt`; `evaluation/evaluation_manifest.json`, `resolved_configs.json`, `episodes.jsonl`, `diagnostics.json`, `video_evaluation_link.json`, `evaluation.log`, `README.txt`; 루트 MP4 6종.
- **재집계 규칙:** `(scenario,case,seed,env_id)`는 cohort, `episode_id`는 개별 시도. 실패 `end_reason=terminated`만 종료로 세고 이번 데이터는 전부 timeout. 결측을 0으로 채우지 않았고 `survived=true`를 지형 완주로 읽지 않았다. scenario 수치는 행가중이며 H6만 2case/768행. P05는 해당 case 384 episode의 경험적 5% 분위수. 최저 cohort의 seed/env ID는 원본 행에서 직접 확인.
- **독립성·미확인:** training Run 정보와 제출 이력은 GitHub 문서/저장소 기록, 직접 계산값은 ZIP. 원 `.pt` 바이트 및 별도 대조 평가 ZIP은 미제공. 선택 프레임의 보행은 실제 시각 근거지만 전 20초 foot contact tracking 또는 복구시간 계측은 미수행. 동일 seed/env index는 물리적으로 같은 상태라는 보증이 아님.
- **자체 최종 검사:** 체크포인트 SHA는 TXT·manifest·link·episode·GitHub keeper 기록과 동일; 6영상 SHA 6/6 및 ZIP CRC 통과; diagnostics 7scenario 평균 직접 재현; 3,072 unique cohort와 end_reason 정합성 확인; H6 상/하, body/world 거리, H1/H3의 작은 값 유리한 방향, 영상 시간표를 바꾸지 않았음. 원본 ZIP·MP4·서버·저장소는 수정하지 않음.
