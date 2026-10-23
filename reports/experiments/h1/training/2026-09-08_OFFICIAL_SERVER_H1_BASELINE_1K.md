---
id: h1-official-server-baseline-20260908-1k
source_type: reviewed_experiment_analysis
category: official_server_experiment
robot: H1
run_started_at: '2026-09-08 23:07:25 KST'
reviewed_at: '2026-09-09'
trust_level: artifact_verified_with_documented_evidence_gaps
authority: '공식 서버 실행 산출물의 기술 결과이며 공식 evaluator 점수나 제출 성능 판정은 아니다.'
---

> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/experiments/h1/training/2026-09-08_OFFICIAL_SERVER_H1_BASELINE_1K.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.


# [학습] H1 공식 서버 baseline 1K 검토

> 관리 안내 (2026-10-13): **학습** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](<../../../../research/EXPERIMENTS.md>)를 확인한다.

## 기술 요약

공식 서버의 기본 H1 reward로 seed `42`, `4096` environments, `1000` iterations 실행이 완료됐고 checkpoint·policy·ONNX·report·영상·TensorBoard event가 생성됐다. 실행과 export 파이프라인은 성공했지만 report의 마지막 terrain level은 `0.00`, 마지막 10회 평균 낙상률은 `100.0%`다. 따라서 이 정책은 안정 보행 기준선이나 제출 후보가 아니다.

300-iteration 공식 baseline보다 표시 최고 mean reward는 `0.16`에서 `0.38`로 증가했지만 terrain과 낙상률은 개선되지 않았다. 단일 seed이고 지형 생성 seed가 고정되지 않았으므로 정밀 paired 비교는 아니지만, 기본 reward를 1K까지 늘린 이번 한 실행만으로는 안정성이 확보되지 않았다는 결론은 직접 지지한다.

## 증거와 보존 위치

원본은 다음 위치에 다운로드 당시 이름과 바이트 그대로 보존한다.

```text
naver-issacsim-originals/data/raw/official_server_runs/h1/
  2026-09-08_230725_baseline_1k/
```

수신 자료는 작업공간 전체 백업이 아니라 공식 서버 결과·환경·출처 증거 묶음이다. TAR SHA-256은 `000b07bdc91bd458770ad14d568bddb7261fa4fa3b89e6511080398ebea1dd79`이며 내부에는 파일 17개가 있다.

## 직접 확인된 실행값

| 항목 | 값 | 근거 |
| --- | ---: | --- |
| robot/task | Unitree H1 / Humanoid, 19 actions | report·env |
| 시작 시각 | 2026-09-08 23:07:25 KST | run 경로 |
| seed / 병렬 환경 | 42 / 4096 | agent·env |
| iterations | 1000, step 999까지 | agent·report·checkpoint |
| 표시 학습시간 | 12분 14초 | report |
| 단순 평균 | 0.734초/iteration | report 값 계산 |
| 표시 최고 mean reward | 0.38, step 971 | report |
| 선택 checkpoint | `model_999.pt` | SHA-256 일치 |
| 마지막 terrain / 낙상률 | 0.00 / 100.0% | report |
| 마지막 exploration std | 0.653 | report |
| 제출 파일 NaN | 없음 | report |

12분 14초에는 초기화·학습·finalize·export가 섞일 수 있으므로 안정 구간 학습 처리량으로 사용하지 않는다. report 값은 화면 표시 정밀도로 반올림돼 있다.

## 환경과 provenance

- Isaac Sim: `5.1.0-rc.19+release.26219.9c81211b.gl`
- Isaac Lab: commit `3e73d6dd79080fd7632488c061052a6edd52e230`, 기록상 clean tree
- PyTorch: `2.7.0+cu128`
- baseline reward: linear/yaw tracking `0.5/0.5`, termination `-5.0`, hip/torso `-0.2/-0.1`

`model_999.pt`와 두 `model_best`는 같은 SHA-256이다. 일반 이름과 timestamp 별칭의 policy·ONNX·MP4·env도 각각 동일하며, MP4는 1920×1080, 50 fps, 999 frames, 19.98초다.

코드 해시 목록의 live `humanoid_rewards.py`와 TAR root 파일 해시는 다르다. TAR root 파일은 같은 목록의 `humanoid_rewards_baseline_1k.py`와 일치하므로 baseline reward 스냅샷으로 분류한다. 해시 파일은 관련 결과값 증거이지 전체 작업공간 복원 manifest가 아니다.

## 300회 공식 baseline과의 제한적 비교

| 항목 | 2026-08-24 300회 | 2026-09-08 1K |
| --- | ---: | ---: |
| 표시 시간 | 4분 0초 | 12분 14초 |
| 단순 평균 | 0.800초/iter | 0.734초/iter |
| 표시 최고 mean reward | 0.16 @ 287 | 0.38 @ 971 |
| 마지막 terrain | 0.00 | 0.00 |
| 마지막 낙상률 | 100.0% | 100.0% |
| 마지막 std | 0.633 | 0.653 |

시간의 단순 평균 차이는 고정비가 더 많은 iteration에 분산된 영향일 수 있으므로 서버 처리량 향상으로 단정하지 않는다. 두 실행 모두 공식 evaluator 점수가 없고 terrain generator seed가 `null`이라 통계적 비교로 취급하지 않는다.

## 판정과 다음 사용법

확정할 수 있는 것은 공식 서버에서 baseline 1K 학습과 export가 완료됐고 이번 정책은 report 지표상 안정 보행 정책이 아니라는 점이다. TensorBoard event, 설정, 최종 checkpoint, policy와 영상은 함께 보존됐다.

`termination_penalty=-5`가 실패의 단독 원인인지, 공식 evaluator 점수와 제출 성능, GPU 처리량, 1K 이후 장기 수렴 시점과 단일 seed의 재현 분산은 이 자료만으로 확정할 수 없다. 개인 Brev 5K와도 출처를 구분한다.

이 결과는 official-server failure control과 1K 학습량 기준점으로 사용한다. reward 후보 채택은 공식 서버의 같은 조건 paired 실행 또는 공통 evaluator를 확보한 뒤 판단한다.

## 데이터 품질 판정

| 항목 | 판정 | 영향 |
| --- | --- | --- |
| 원본 5개 무결성 | 복사 전후 SHA-256 일치 | 통과 |
| TAR 경로 | 안전한 상대경로만 포함 | 통과 |
| checkpoint 별칭 | final과 model_best 일치 | 통과 |
| policy·영상 별칭 | 중복 관계를 SHA-256으로 확인 | 통과 |
| reward provenance | live와 baseline snapshot 관계 문서화 | 사용 가능 |
| 전체 콘솔·GPU 시계열 | 미포함 | 처리량 진단 제한 |
| 공식 evaluator 점수 | 미포함 | 제출 성능 판단 금지 |
