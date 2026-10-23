---
id: h1-personal-server-termination-m50-20260825
source_type: reviewed_experiment_analysis
category: personal_server_experiment
robot: H1
run_started_at: "2026-08-25 16:11:27 (run-directory timestamp)"
reviewed_at: "2026-08-26"
trust_level: artifact_verified_with_scope_limits
authority: "개인 NVIDIA/Brev 검증 환경의 실행 로그와 설정을 확인한 기술 기록이다. 공식 서버 점수·제출 성능의 증거가 아니다."
---

> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/experiments/h1/training/2026-08-25_PERSONAL_SERVER_TERMINATION_M50_25K.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.


# [학습] H1 개인 서버 `termination_penalty=-50` 장기 실행: 검증 기록

> 관리 안내 (2026-10-13): **학습** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](<../../../../research/EXPERIMENTS.md>)를 확인한다.

## 판정

이 실행은 개인 NVIDIA/Brev 환경에서 H1 학습 파이프라인이 장기 실행된 사례다. 콘솔에 `24999/25000` 및 `exit=0`이 남고, run 설정과 TensorBoard에서 파생한 CSV가 보존되어 학습 추세와 처리량을 검토할 수 있다. 그러나 공식 서버가 아니며, play 영상·공식 시나리오 평가·복수 seed가 없으므로 정책의 공식 성능이나 `-50`의 최적성은 판정하지 않는다.

## 보관 위치와 증거 등급

원본 아카이브는 아래 경로에 원형으로 보관한다.

```text
naver-issacsim-originals/data/raw/private_server_runs/h1/
  2026-08-25_exp1_termination_m50_long_25000iter/
```

| 등급 | 이 문서에서 쓰는 자료 | 사용 범위 |
| --- | --- | --- |
| A | 실행 console, `env.yaml`, `agent.yaml`, checkpoint hash | 실행 조건·종료·파일 동일성 |
| B | 이번 실행의 TensorBoard에서 만들어진 summary/milestone CSV | 추세와 구간 요약 |
| C | 함께 받은 통합 분석 원문 | 추가 조사 단서. 독립 확인 전에는 결론 근거로 사용하지 않음 |

수신 원문은 `data/processed/incoming/other/inbox/personal_server/`에 별도 보관한다. 원문에 적힌 입력 아카이브 이름은 실제 수신 파일명과 다르므로, 이 문서는 원본 저장소의 manifest SHA-256을 정본으로 쓴다.

## 직접 확인된 실행 조건

| 항목 | 값 | 근거 |
| --- | ---: | --- |
| task | `Humanoid-v0` / H1 | console·config |
| 환경 수 | 4,096 | `env.yaml` |
| seed | 42 | `env.yaml`, `agent.yaml` |
| rollout | 24 steps/env/iteration | `agent.yaml` |
| max iterations | 25,000 | `agent.yaml` |
| 실제 termination penalty | `-50.0` | run `env.yaml`, console override |
| 실행 모드 | `--headless` | console |
| logger | TensorBoard | `agent.yaml` |
| transitions/iteration | 98,304 | `4096 × 24` 계산 |
| 총 transitions | 2,457,600,000 | `98,304 × 25,000` 계산 |

PPO와 terrain 관련 설정은 저장된 YAML에 남아 있다. 비교 실험에서 reward 이외 설정을 고정했다고 단정하려면 이후에는 설정 파일 전체 diff와 코드 commit/hash를 함께 기록해야 한다.

## 종료 및 checkpoint

- console은 iteration `24999/25000` 뒤 `[POST] 학습 종료 (exit=0)`를 기록한다.
- 콘솔의 학습 loop 경과 시간 마지막 값은 `05:44:36`이다. 이는 finalize/export를 포함한 전체 wall-clock이라고 단정하지 않는다.
- console은 `Train/mean_reward` 기준으로 step 23101의 `model_23100.pt`를 선택했다고 기록한다.
- run의 `model_23100.pt`와 exported `model_best.pt`는 같은 SHA-256이다.

```text
974f97f7ad58c01ccd77568e0e536a8c1dfeaa57392f526f1486ffe699dd7f48
```

콘솔은 finalize 단계가 intermediate `.pt` 250개를 삭제했다고도 기록한다. 현재 아카이브에서 보존된 checkpoint 하나만으로 다른 iteration의 정책을 사후 비교할 수는 없다.

## 기록된 지표

아래는 보존된 TensorBoard 파생 CSV의 마지막 지점과 마지막 500 iteration 평균이다. 이는 학습 내부 지표이며 공식 점수나 시나리오 점수가 아니다.

| 지표 | 마지막 | 마지막 500 평균 |
| --- | ---: | ---: |
| Train/mean_reward | 5.882 | 5.993 |
| mean episode length | 867.16 | 869.23 |
| terrain level | 5.876 | 5.897 |
| timeout | 78.57% | 78.96% |
| base-contact termination | 21.43% | 21.05% |
| linear XY velocity error | 0.372 | 0.360 |
| yaw velocity error | 0.803 | 0.811 |
| total throughput | 116,670 steps/s | 119,471 steps/s |
| collection time | 0.754 s/iteration | 0.736 s/iteration |
| learning time | 0.088 s/iteration | 0.088 s/iteration |

파생 CSV상 `Train/mean_reward` 최대값은 iteration 24012에서 약 6.904지만 finalize가 고른 checkpoint와 다르다. 두 값의 차이는 확인된 사실이고 EventAccumulator sampling 등 구체 원인은 아직 가설이다. 학습 reward peak만으로 checkpoint를 채택하지 않는다.

## 비교에서 읽을 수 있는 것과 읽을 수 없는 것

아카이브에는 `exp0_baseline` 200-iteration run도 있다. 저장된 YAML에서 양쪽은 seed 42, 4096 envs, rollout 24, terrain curriculum을 공유하며 baseline의 termination penalty는 `-5.0`, 장기 run은 `-50.0`이다. 다만 baseline이 200 iteration뿐이고 단일 seed이며 전체 실험 조건의 정규화된 diff가 없으므로, 이것은 초기 관찰용 paired 참고이지 `-50`의 인과 효과나 최적성 증명이 아니다.

이 run에서 안전하게 말할 수 있는 것은 장기 학습 중 episode length·terrain·timeout 지표가 후반까지 개선/유지되었다는 점이다. 안전하게 말할 수 없는 것은 공식 순위, 보행 품질, reward hacking 부재, 다른 seed 재현성, 또는 `-20`·`-100`보다의 우위다.

## 다음 행동

1. 개인 검증 환경에서 이 `model_best.pt`를 load해 영상과 시나리오별 evaluator 결과를 만든다. 영상 없이 수치만으로 채택하지 않는다.
2. 다음 reward 실험은 baseline과 candidate를 같은 run length, seed, headless/camera 조건으로 맞추고, 모든 설정의 hash/diff를 남긴다.
3. finalize 전에 `logs/<run>/`, event, 모든 checkpoint, console, GPU 시계열을 복제한다. 이번처럼 intermediate checkpoint가 정리되면 사후 최적 checkpoint 재선정이 제한된다.
4. Optuna는 공식 서버에 자동 설치하지 않고, 개인 측 evaluator의 robust proxy score를 `ask/tell`로 기록해 다음 reward 후보를 추천하는 용도로만 쓴다.

## 자료 배치

- raw archive·checkpoint·event·large CSV/chart: originals repository
- 검증 분석과 이 문서: analysis repository
- 작은 config·milestone·summary와 재현 방법: NVIDIA repository

이 분리는 대용량 LFS 다운로드를 피하면서도 실험의 추적성과 개인 서버 재현성을 유지한다.
