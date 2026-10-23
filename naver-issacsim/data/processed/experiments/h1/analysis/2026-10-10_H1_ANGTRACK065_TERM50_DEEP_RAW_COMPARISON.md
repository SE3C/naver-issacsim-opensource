# [분석] H1 ANGTRACK-065 대조 심층 분석 — 원자료 재계산 (2026-10-10)

> 관리 안내 (2026-10-13): **분석** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](../../../../../research/EXPERIMENTS.md)를 확인한다.

**보관 상태:** 이 문서는 현재 채팅 작업 공간에서만 생성한 분석 사본이다. GitHub/AI 라이브러리/서버에는 게시하거나 수정하지 않았다. 기존 학습·평가·영상 실행 없음.

## 1. 사용 자료와 직접 검증 범위

- **기준 정책:** `TERM-50 / model_2800`, 평가 `model_2800_h1_6terrain_evaluation_20261008-171331_a8ab9d61.zip`, SHA-256 `d4a47b0e182763e21077b688f44f7d9cdc00759c0f0f78f4217930e1c49975da`.
- **시험 정책:** `ANGTRACK-065 / model_2950`, 평가 `model_best_h1_6terrain_evaluation_20261010-041416_066bf8a3.zip`, SHA-256 `ec1bc325feae5cd6da1643a9fbbe13b0640ad7514b77b79e5532d8b836def93b`.
- 추가 정량 문맥으로 기존 `ORIENT-100/model_2850` 및 `ACTRATE-0001/model_2700` 평가 ZIP도 직접 읽었다. **이 보고서는 새 GPU 평가가 아니라 보존된 원본 JSONL의 CPU 재집계**다.
- 두 주요 ZIP의 `evaluation/resolved_configs.json` SHA-256은 동일한 `3f7d219d03574c10c07911eb1df7aa2cea27c90e6dbd60dfd290b35001631bbc`이고, evaluator protocol, agent fingerprint, source fingerprints 및 `(scenario,case,seed)` applied-env fingerprints가 일치한다. H1~H7(8 case)×3 평가 seed(4201~4203)×128 env×20초, deterministic inference; `(scenario,case,seed,env_id)` 3,072 최초 cohort 1:1 대응. **키/설정 일치가 개별 episode의 실제 물리 초기 상태·terrain realization 일치를 증명하지 않는다.**
- ANG의 `episode_id` 접미사 `-n0`만을 **최초 cohort**로 3,072개 추출해 TERM의 3,072개와 비교했다. ANG에는 H3 접촉 종료 후 `-n1` 재시작 15행이 추가되어 JSONL 전체는 3,087행. 최종 집계는 각각 3,072 최초 cohort에 맞췄다. `episode_id`가 아닌 case/seed/env와 최초시도 표시를 명시적으로 확인했다.

## 2. 핵심 판정

**ANGTRACK-065는 yaw 추종·정지 중 비의도 전진 억제에 장점이 있으나, 순수 횡이동 H3의 실패와 만성 정체가 결정적 약점이다. 정책 대표 채택 HOLD.** OFFICIAL fresh3K 학습 COMPLETE/PASS와 PERSONAL evaluator COMPLETE는 동작 품질·공식 점수·reward 인과를 뜻하지 않는다.

### 두 정책의 대표 비교

| 지표 (최초 episode 기준) | TERM-50 | ANGTRACK-065 | 해석 |
|---|---:|---:|---|
| 전 8 case episode 평균 혼합 tracking↓ | 0.157118 | 0.130669 | ANG 16.83% 낮음. 서로 다른 물리량을 혼합한 evaluator 내부 지표, 공식 점수 아님 |
| 전 8 case episode 평균 `vx_error`↓ | 0.052837 | 0.052362 | 거의 비슷 |
| 전 8 case episode 평균 `vy_error`↓ | 0.060848 | 0.069613 | ANG **14.41% 악화** |
| 전 8 case episode 평균 `yaw_error`↓ | 0.114376 | 0.064730 | ANG **43.41% 개선** |
| 전 8 case episode 평균 `xy_rmse`↓ | 0.112589 | 0.125612 | ANG **11.57% 악화** |
| H1 정지 명령의 비의도 body-frame 전진↓ | 1.3523m | **0.8751m** | ANG 0.477m 줄임 |
| H1 정지 중 world 순변위 크기 평균↓ | 1.3565m | **0.9013m** | 제자리 유지 향상, 성공은 아님 |
| H1 roll/pitch RMS↓ | **0.03434** | 0.05594 | ANG 자세 RMS 약 62.9% 증가 |
| H3 최초 cohort base-contact 종료↓ | **0/384** | **15/384** | ANG 3.91%, 모든 평가 seed에서 발생 |
| H3 최초 cohort 횡속도 `vy_error`↓ | **0.06848** | 0.18601 | ANG 2.72배 |
| H3 최초 cohort `stall_fraction`↓ | **0.00912** | 0.34339 | ANG 만성 정체 |
| H4 회전 명령 `yaw_error`↓ | 0.11934 | **0.07704** | ANG 35.45% 감소, **384/384 동일 인덱스 우세** |
| H5 rough 전진 평균↑ | 8.8961m | 8.8949m | 사실상 동일 |
| H5 rough 전진 P05↑ | **8.5325m** | 8.3990m | 저위 5% ANG 열세 |
| H5 rough 전진 최솟값↑ | 2.6391m | **7.7253m** | TERM 극단 정체가 더 심함. 그러나 ANG 전체 우위는 아님 |
| H6 상행 진행↑ | **20.1995m** | 19.5712m | ANG −0.6283m |
| H6 하행 진행↑ | **19.9852m** | 19.2349m | ANG −0.7503m |

**평균의 함정:** ANG H3에는 20초 전 접촉 종료된 15개 `-n0`가 포함돼 있다. 모든 8-case 최초 3,072개 행을 동일가중한 0.130669는 동일 시간 노출을 보장하지 않는다. 20초 episode 시간으로 가중한 8-case tracking은 TERM **0.157118**, ANG **0.129964**로 우열 방향은 같지만 생존 위험을 포함한 정책 합격 점수는 아니다. 특히 H3에서 짧은 에피소드를 제외하고 **정상 완주 369개만 비교해도** 문제는 지속된다.

## 3. H3 접촉 종료가 전부가 아니다

- ANG의 H3 최초 384개 중 15건 base-contact 종료(`terminated`, `base_contact_failure=true`)는 **4201:6, 4202:4, 4203:5건**; 각 종료는 **6.92~11.50초**, 평균 **9.05초**. H3의 10초 명령 부호 전환 이전에 **10건**, 이후에 **5건** 발생했다. 부호 전환 하나만의 실패로 해석할 수 없다.
- ANG H3 episode 행 기준 `384/399=96.24%` survived는 reset 후 짧은 `-n1` 15행을 포함한다. **최초 20초 timeout 생존은 `369/384=96.09%`**. TERM은 `384/384` timeout.
- 낙상하지 않은 ANG H3 **369개만** 볼 때 ANG `vy_error` **0.18087** vs 같은 cohort의 TERM 약 **0.06847**; ANG stall **0.33889** vs TERM **0.00913**; ANG 복합 tracking **0.21229** vs TERM 약 **0.12748**. 즉 낙상 행을 제거해도 횡속도 오차와 정체는 심각하다.
- H3 **384/384 대응 cohort 모두** ANG의 `vy_error`와 `stall_fraction`이 TERM보다 크다. TERM H3 stall **최대 0.010**, ANG **최소 0.155**: 관측된 두 분포는 완전히 분리된다.
- H3 접촉 종료 15건의 ANG 부분 episode 평균 `roll_pitch_rms=0.20881` vs 대응 TERM 정상 20초 평균 `0.03590`(서로 다른 duration에 주의). 접촉 종료 ANG 15건은 평균 yaw error **0.13735**로 TERM **0.06744**보다 나쁘지만, ANG의 나머지 **369/384 정상 완주 중 368개**에서는 yaw 오차가 TERM보다 작다. 즉 회전 추종 개선도 고장난 에피소드에는 일반화되지 않는다.
- ANG H3 최초 384개 중 **365개에서 stall>25%**. H3 world 순변위 평균은 TERM **0.9725m**, ANG **0.9494m**로 비슷하지만, **적게 움직여도 좌우 명령을 성공한 것은 아니다**. `forward_progress_m`은 body-forward 적분이고 H3에서 원하는 순수 횡이동 거리 지표가 아니다. `lateral_drift_m`도 실제 횡방향 순변위가 아니라 `|Δvy|` 누적이므로 이 둘을 혼동하지 않는다.
- H3 episode 평균만으로 정확히 어느 관절/보상 항이 실패를 유발했는지는 식별할 수 없다. 접촉 시간 전후의 body pose/발 접촉/명령 위상별 time series가 필요한 질문이다.

## 4. 회전 개선과 제어 비용은 함께 봐야 한다

- **H4 순수 yaw-error:** TERM `0.11934 → ANG 0.07704` (**35.45% 감소**)이고, 세 평가 seed 각각 대응된 **128/128**에서 ANG가 낮다. 그러나 action Δ RMS는 TERM `0.35193 → ANG 0.36666` (**+4.19%**), body-forward 10초+10초 적분은 TERM `10.099m → ANG 9.889m`. H4의 world 순변위 3.007→2.661m만으로 회전 성공·실패를 단정하지 않는다.
- H6 경사 상행 yaw error `0.15310 → 0.07651`(−50.0%), 하행 `0.15237 → 0.07691`(−49.5%). 둘 다 384/384 대응 인덱스에서 ANG yaw가 낮지만, 상행 `vx_error`와 `vy_error`는 각각 **10.8%**, **12.7%** 증가, action Δ RMS **9.2%** 증가, 전진 **0.628m** 감소. 하행 `vx_error`·`vy_error` 각각 **19.9%**, **10.2%** 증가, action Δ RMS **7.0%** 증가, 전진 **0.750m** 감소.
- 전체 8-case 초깃값 기준 혼합 tracking 0.157118→0.130669로 **16.8% 낮아졌어도**, 분해하면 yaw-error 평균 **43.4% 감소**, `vy_error` 평균 **14.4% 증가**, `xy_rmse` 평균 **11.6% 증가**다. **좋은 yaw가 lateral 실패를 상쇄한 내부 혼합 오차를 전지형 성능 지표로 단독 사용하는 것은 위험**하다.

## 5. 험지 하위 꼬리: 한 극단 사례와 전체 분포를 분리

- H5 평균 body-forward TERM **8.8961m**, ANG **8.8949m**. 대응 인덱스 전진 우세는 **ANG 179/384, TERM 205/384**. 하위 5% 전진 TERM **8.5325m**, ANG **8.3990m**, ANG가 더 약하다.
- 최솟값 TERM **2.6391m**(seed4201/env16, 큰 정체), ANG **7.7253m**. **TERM의 극단 정체는 더 심각**하지만, 동시에 **진행 8.5m 미만 episode**가 TERM 13개, ANG 31개여서 ANG의 하위권 실현이 항상 더 안전한 것은 아니다.
- TERM의 최저 진행 사례 1개만 양쪽에서 제외하면 나머지 383개에서 TERM 평균 **8.91246m**, ANG **8.89505m**다. **평균 근접은 하나의 극단 실패에 영향을 받는다**는 민감도 점검이지 해당 TERM 실패를 무시해도 된다는 뜻은 아니다.
- H5 yaw error와 전체 tracking은 ANG가 더 낮지만, `vx_error` TERM `0.07122` vs ANG `0.08064`로 더 크고 action Δ RMS TERM `0.35925` vs ANG `0.40047`로 더 큼. 즉 rough 진행 비슷하면서 action 비용이 증가했다.

## 6. 기존 네 정책을 한 자리에 놓으면

| 항목 | TERM-50 | ORIENT-100 | ACTRATE-0001 | ANGTRACK-065 |
| --- | ---: | ---: | ---: | ---: |
| 같은 `scenario7`의 최초 cohort | 3,072 | 3,072 | 3,072 | 3,072 (+H3 재시작 15) |
| 전체 혼합 tracking↓ (초기 3,072행 평균) | 0.15712 | 0.14041 | 0.14534 | **0.13067** |
| H1 비의도 body 전진↓ | 1.352m | 1.633m | 1.987m | **0.875m** |
| H3 base-contact 첫 시도 종료↓ | **0/384** | **0/384** | **0/384** | 15/384 |
| H3 `vy_error`↓ | 0.0685 | **0.0639** | 0.0673 | 0.1860 |
| H3 stall↓ | 0.0091 | 0.0090 | **0.0062** | 0.3434 |
| H4 yaw absolute error↓ | 0.1193 | 0.1026 | 0.1183 | **0.0770** |
| H5 rough 평균 진행↑ | 8.896m | 9.451m | **9.948m** | 8.895m |
| H5 rough 최저 진행↑ | 2.639m | 7.831m | **8.815m** | 7.725m |

**용도별 관찰:** ANG는 이 샘플에서 yaw/zero-forward leakage에 강하나 lateral contact 안정성에서 탈락. ORIENT는 종합 tracking에 강하지만 큰 roll/pitch RMS 비용이 있고, ACTRATE는 rough 진행이 좋지만 정지 누수/action 비용이 크다. TERM은 H3 안정성 측면에서 확실한 기준선이다. 정해진 mission utility, 실전 계단/박스 완주, 여러 독립 training seed 없이 하나를 all-around 대표라고 단정하지 않는다.

## 7. 다음 질문과 작업 경계

1. **추가 GPU 없이 할 수 있는 결론:** `ANGTRACK-065`의 전지형 후보 승격은 보류. H3 접촉 종료 뿐 아니라 생존 cohort의 심각한 측면 명령 오차가 핵심이므로, 단순히 최악 15건만 제외하는 사후 선택은 불가하다.
2. **다음 학습보다 값싼 추가 근거:** 보존된 평가의 step-level H3 joint/base/command/foot contact trace가 있는지 확인해 **0~10초/10~20초 명령 위상과 fall 직전 1초**를 분리하면 yaw·lateral gait 실패 기전을 좁힐 수 있다. 현재 ZIP의 `episodes.jsonl`은 episode aggregate이며 step-level trace는 확인되지 않았다. 새 GPU 평가는 별도 명시적 요청이 있어야 한다.
3. **새 학습은 보류:** `ACTRATE-001`은 기존 Registry의 PLANNED 가설로 유지. 이 분석은 fresh Run이나 checkpoint 평가 추가 실행 지시가 아니다. 다른 독립 seed, 정책 후보의 final numbered checkpoint 검증 및 계단/박스 정량 검증도 현재 결과의 확인 공백으로만 기록한다.

**방법:** Python/pandas로 각 ZIP 내 JSONL 읽기, first-attempt suffix `-n0`로 그룹 필터, 3,072 키 1:1 merge, episode별 수치 평균·분위수와 대응-index 부호 계수. 실제 시각 영상의 재판독이나 simulator/backend 재실행은 이번 작업에서 하지 않았다. 모든 source ZIP/checkpoint/기존 GitHub 파일 보존.
