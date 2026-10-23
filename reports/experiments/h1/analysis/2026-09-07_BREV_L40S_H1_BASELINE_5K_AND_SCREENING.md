> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/experiments/h1/analysis/2026-09-07_BREV_L40S_H1_BASELINE_5K_AND_SCREENING.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# [분석] H1 Brev L40S baseline 5K 및 reward screening 1K 검토

> 관리 안내 (2026-10-13): **분석** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](<../../../../research/EXPERIMENTS.md>)를 확인한다.

## 기술 요약

개인 Brev L40S에서 기본 H1 reward로 수행한 5K 실행은 학습 파이프라인 확인을 넘어 실제 locomotion 기준선으로 사용할 수 있는 수준까지 개선됐다. 마지막 iteration에서 평균 episode length는 742.97 step, terrain level은 5.054, time-out 종료는 66.79%였다. 다만 base-contact 종료가 33.21%이고 yaw 오차가 XY 오차보다 커서 최종 안정 정책으로 확정할 단계는 아니다.

1K 단변수 screening 중에는 `termination_penalty -5 → -50`만 바꾼 TERM50이 가장 강한 후속 후보였다. 1K 안에서 terrain 4.823, time-out 68.34%, 평균 episode length 799.97에 도달했다. 반면 YAW075는 100% base contact와 terrain 0으로 실패했고, RECOVERY는 후반 회복 신호가 있었지만 1K 종료 시 base contact가 95.68%였다.

이 결론은 개인 서버의 학습 내부 지표이며 공식 제출 성능을 뜻하지 않는다. 또한 TERM50으로 표시된 영상이 baseline 1K 영상과 동일하고, baseline의 `exported/model_best.pt`가 1K 체크포인트를 가리키는 중대한 자료 연결 오류가 있다. 두 원본은 수정하지 않았고 영상 기반 TERM50 평가는 제외했다.

## Baseline 5K는 유효한 개인 기준선이 됐다

### 실행 조건

| 항목 | 값 |
| --- | --- |
| task | H1 `Humanoid-v0` |
| environments | 4,096 |
| seed | 42 |
| rollout | 24 steps/environment/iteration |
| iterations | 5,000 요청, 실제 마지막 loop `4999/5000` |
| reward | 배포 baseline 그대로 |
| GPU | NVIDIA L40S |
| Isaac Sim | `5.1.0-rc.19` |
| Isaac Lab | `2.3.2`, commit `3e73d6dd79080fd7632488c061052a6edd52e230` |
| Python / PyTorch | 3.11.13 / 2.7.0+cu128 |
| 학습 loop 시간 | 4,208.45초, 약 70분 8초 |

### 마지막 iteration 측정값

| 지표 | 값 | 해석 |
| --- | ---: | --- |
| `Train/mean_reward` | 4.944946 | 동일 run 내부 진행 확인용 |
| 평균 episode length | 742.969971 step | 20초 episode 상한의 약 74% |
| terrain level | 5.054047 | curriculum 진행 확인 |
| base-contact 종료 | 33.2082% | 여전히 낙상·접촉 실패가 큼 |
| time-out 종료 | 66.7918% | 상당수 episode가 제한시간 도달 |
| linear tracking reward | 0.279635 | 추종 학습 진행 |
| yaw tracking reward | 0.189856 | 선형 추종보다 약함 |
| XY velocity error | 0.342473 | 개선 여지 있음 |
| yaw velocity error | 0.651832 | 현재 주요 병목 |
| action std | 1.131 | 탐색이 남은 중간 수렴 상태 |

학습 중 최고 mean reward는 step 4,958의 5.972였다. 저장 주기 때문에 해당 step과 정확히 일치하는 checkpoint가 없으며 최종 보존 후보는 `model_4999.pt`다. mean reward 최고 checkpoint가 실제 시나리오 최고 정책이라는 뜻은 아니므로 영상과 evaluator가 필요하다.

## TERM50만 장기 확인 후보로 남는다

세 screening은 동일한 seed, environments, PPO, terrain과 1,000 iterations를 사용했고 reward 변경만 달랐다.

| 실험 | 유일한 변경 | terrain | base contact | time-out | episode length | XY error | yaw error | 판정 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| TERM50 | termination `-5 → -50` | 4.8232 | 31.69% | 68.34% | 799.97 | 0.4065 | 1.577 | 장기 확인 후보 |
| YAW075 | yaw tracking `0.5 → 0.75` | 0.0000 | 100% | 0% | 103.15 | 미채택 | 0.0581 | 실패한 정지/낙상 해 |
| RECOVERY | hip `-0.2 → -0.1`, torso `-0.1 → -0.05` | 0.01025 | 95.68% | 4.37% | 292.80 | 미채택 | 미채택 | standalone 중단 |

TERM50은 약 iteration 200부터 생존·terrain 지표가 함께 상승하는 phase transition을 보였다. reward 계수가 baseline과 다르므로 mean reward 절댓값은 비교하지 않는다. 또한 TERM50의 yaw error가 1.577로 높아 “안정성과 회전 추종을 동시에 해결했다”고 결론 내릴 수 없다.

YAW075의 낮은 yaw error는 좋은 회전 정책의 증거가 아니다. terrain 0에서 모든 episode가 base contact로 종료됐으므로, 거의 움직이지 못하는 상태에서 계산된 낮은 오차일 가능성을 우선한다.

RECOVERY는 약 iteration 800 이후 일부 지표가 좋아졌지만 종료 시점의 생존성과 terrain이 부족하다. 단독 5K 확장은 보류하고, TERM50 같은 안정성 anchor를 먼저 확인한 뒤 제한된 interaction 실험에서만 다시 검토한다.

## 자료 연결 오류는 원본을 고치지 않고 분석에서 차단했다

### 중대한 오류

1. `H1A_TERM50_20s.mp4`와 baseline 1K 영상의 SHA-256이 모두 `43072555b7ff7ae7a51ae38e5024f42d11af8d33bfac41c6cfde308bf593d2bd`다. TERM50 checkpoint 자체는 baseline 1K와 다르므로 정책 중복이 아니라 잘못 복사되거나 남은 영상으로 판단한다. TERM50 분석 원문의 모든 영상 관찰 문장은 검증 근거에서 제외한다.
2. baseline archive의 `training/humanoid/exported/model_best.pt`는 `model_1000.pt`와 동일하다. 올바른 최종 checkpoint는 run의 `model_4999.pt`이며 `results/.../h1_baseline_5000.pt`와 동일하다.

### 사소한 표기 보정

- 5,000 iterations 실행의 실제 마지막 checkpoint를 `model_5000.pt`가 아니라 `model_4999.pt`로 표기한다.
- 결과 이름 `h1_baseline_5000.pt`는 기존 별칭으로 보존하되 manifest에 실제 iteration 4,999를 병기한다.
- 보존된 baseline·screening 영상은 1920×1080, 50fps, 999 frames로 약 19.98초다. `6000 frames/120초`는 실행 의도 또는 기본 설정일 뿐 실제 산출물 설명으로 쓰지 않는다.

## 근거와 검토 방법

- 네 수신 분석 원문을 모두 읽고 결론·수치·한계를 비교했다.
- baseline 전체 console의 시작, 마지막 iteration, exit code, 처리시간과 오류·경고를 확인했다.
- TensorBoard scalar로 endpoint와 reward peak를 확인했다.
- 세 screening의 `env.yaml`, agent 설정과 reward 파일을 비교해 의도한 reward 외 차이가 없는지 확인했다.
- 체크포인트는 전부 내부 해석하지 않고 주요 milestone의 파일명, iteration, 크기, 해시와 영상 연결만 확인했다.
- 영상은 duration·frame metadata와 대표 프레임을 확인했다. TERM50 영상은 중복 판정 후 시각적 근거에서 제외했다.

원본 archive는 Originals 저장소의 `data/raw/private_server_runs/h1/2026-09-06_07_brev_l40s_baseline_5k_and_screening_1k/`에 있다. 입수했던 네 분석 Markdown에는 TERM50 영상의 잘못된 관찰과 checkpoint 연결 오류가 있어, 정정 후 원문 사본을 현재 분석 트리에서 제거했다. 이 문서가 그 자료를 대체하는 정정된 단일 분석본이다.

## TERM50 reward schedule 제안 검토

외부 분석 원문은 TERM50으로 안정성을 먼저 확보한 뒤 yaw·tracking을 단계적으로 강화하는 reward schedule을 제안한다. 단계별 shaping 자체는 가능한 연구 가설이지만 현재 자료는 schedule 실험 결과를 포함하지 않는다. 특히 1K·2.5K·5K 전환 시점의 우열과 별점 평가는 근거가 없어 채택하지 않는다.

보존된 H1 코드는 `--resume`을 지원하지만 resume 시 terrain curriculum이 쉬운 단계로 리셋된다. 현재 Brev 5K wrapper도 phase 중간 reward 변경을 구현하지 않는다. 따라서 reward를 바꾸고 resume하는 방식은 현재 환경에서 완전히 연속적인 curriculum이 아니라 checkpoint 기반 fine-tuning phase로 취급한다.

현재 판정은 바꾸지 않는다. 먼저 TERM50 5K standalone을 baseline 5K와 같은 조건으로 확인하고, yaw 계수를 섞지 않는다. schedule은 TERM50 안정성이 확인된 뒤 같은 2.5K checkpoint에서 두 분기를 만들어 남은 학습량을 고정한 대조 실험으로만 검토한다. 두 분기 모두 동일한 resume·terrain reset 조건, 별도 run ID, checkpoint·설정 hash와 공통 evaluator를 사용해야 한다.

## 다음 실행

1. 기본 5K를 개인 H1 baseline B0로 유지한다.
2. TERM50 checkpoint에서 영상을 새로 렌더링해 checkpoint hash와 영상 manifest를 연결한다.
3. TERM50을 동일 환경에서 장시간 confirmation하되 baseline과 같은 seed·iterations·headless 조건을 유지한다.
4. yaw tracking 계수는 TERM50 안정성 확인 전 직접 올리지 않는다.
5. RECOVERY 완화는 TERM50 확정 뒤 단일 interaction 후보로만 시험한다.
6. 채택 전에는 복수 seed와 별도 evaluator로 생존, tracking, terrain, 동작 품질을 재검증한다.

## 남은 질문

- TERM50의 높은 yaw error가 더 긴 학습에서 내려가는가?
- 새로 렌더한 TERM50 영상에서도 로그의 생존성 개선이 보이는가?
- baseline 5K와 TERM50 장기 run을 같은 evaluator로 비교했을 때 실제 명령 추종과 낙상률이 유지되는가?
