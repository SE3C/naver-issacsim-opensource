---
title: "H1 H-004 TERM20 1.5K 심층 분석"
source_archive: "20260916-152542-h1-h004-term20-1p5k.tar.gz"
source_sha256: "828e98c04f8ee6cec6f15e5f80f8d34a7babd8b63a8748938f42c24524bfa460"
environment: "PERSONAL / Brev L40S"
robot: "H1 / Humanoid-v0"
hypothesis: "H-004"
delta: "termination_penalty -5 -> -20"
iterations: 1500
num_envs: 4096
seed: 42
analysis_date: "2026-09-17"
---

> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/incoming/other/reviewed/2026-09-17_H1_H004_TERM20_1P5K_DEEP_ANALYSIS.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.


# H1 H-004 TERM20 1.5K 심층 분석

## 1. 결론

H-004는 `termination_penalty=-20`을 fresh start부터 적용했을 때 H1이 학습 자체에 실패하거나 수치적으로 발산한 실험은 아니다. 오히려 후반으로 갈수록 episode length, timeout, terrain이 꾸준히 회복된다. 그러나 **안정성을 만드는 속도가 H-001(`-50`)보다 압도적으로 느려**, 1.5K screening 기준으로는 H-005/H-006의 부모 checkpoint로 채택하기 어렵다.

가장 강한 증거는 terrain progression과 termination 구성이다. H-004는 초기 terrain 평균 약 3.44에서 20 iteration 안에 사실상 0으로 붕괴했고, 이후 terrain 0.1을 다시 넘는 데 986 iteration, 0.5를 넘는 데 1373 iteration, 0.75를 넘는 데 1464 iteration이 걸렸다. 최종 1499에서도 terrain은 0.8595이며 base-contact termination은 68.87%다.

반면 H-001 TERM50은 299 iteration에 terrain 0.846, base-contact 48.31%, 999 iteration에 terrain 4.821, base-contact 32.37%, 1499 iteration에 terrain 5.119, base-contact 32.41%였다. 즉 H-004는 최종 시점에도 H-001의 초기 수백 iteration 수준의 terrain에 머문다.

따라서 H-004의 핵심 결론은 **“-20이 학습 불가능한 값”이 아니라 “fresh stability curriculum으로는 -50보다 너무 약하다”**이다. 후반 회복 추세가 강하기 때문에 더 긴 run에서 결국 안정 정책으로 수렴할 가능성은 이 자료만으로 배제할 수 없지만, 제한된 학습 예산의 1.5K parent 후보로는 H-001이 훨씬 효율적이다.

## 2. Evidence 무결성

- archive SHA-256: `828e98c04f8ee6cec6f15e5f80f8d34a7babd8b63a8748938f42c24524bfa460`
- metadata status: `completed`
- child exit code: `0`
- evidence validation: `PASS`
- TensorBoard event: 1개
- mirrored checkpoints: 16개 (`model_0`부터 100회 간격 + `model_1499`)
- source before/after hashes: 전부 동일
- finalize: `completed`
- personal run이라 official backup: `skipped_no_config`
- 내부 `SHA256SUMS`: 전체 검증 통과
- `model_best.pt` SHA-256 = `model_1400.pt` SHA-256 = `0e63afec08075025859877a391e5687122cadbdbb3e23c8401d71e15e6d643a1`
- `model_1499.pt` SHA-256 = `fa93efeaed6ba389591e189bb71840d215a77777f048dc64c3ab0afedbdee6eb`
- `model_1400`, `model_1499`, `model_best`의 actor/critic/optimizer tensor를 직접 검사한 결과 NaN/Inf 없음

이번 archive에는 `policy.pt`와 play video가 없다. 따라서 보행 스타일, 발 들림, 뒤꿈치 접지 같은 시각적 판단은 이 자료만으로 확정하지 않는다.

## 3. 실제 실행 조건

- task: `Humanoid-v0`
- seed: 42
- environments: 4096
- rollout: 24 steps/env/iteration
- iterations: 1500
- physics dt: 0.005 s
- decimation: 4
- episode limit: 20 s
- PPO: 5 epochs / 4 mini-batches
- learning rate: 1e-3 adaptive
- gamma/lambda: 0.99 / 0.95
- entropy coefficient: 0.008
- desired KL: 0.01
- save interval: 100
- headless

학생 reward 중 변경된 항목은 `termination_penalty: -5 -> -20` 하나이며 나머지는 baseline 값 그대로다.

## 4. 학습 곡선 핵심 milestone

| iter | reward | episode | terrain | base-contact | timeout | XY err | yaw err | std |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 99 | -0.49 | 61.71 | 0.0000 | 100.00% | 0.00% | 0.1041 | 0.1483 | 0.75 |
| 299 | -0.07 | 135.22 | 0.0000 | 100.00% | 0.00% | 0.1686 | 0.1709 | 0.77 |
| 499 | 0.30 | 268.49 | 0.0158 | 92.92% | 7.08% | 0.3147 | 0.3170 | 0.86 |
| 999 | 1.26 | 401.27 | 0.1174 | 85.33% | 14.67% | 0.3977 | 0.4493 | 1.00 |
| 1499 | 2.69 | 632.87 | 0.8595 | 68.87% | 31.13% | 0.4715 | 0.6941 | 1.08 |

초기에는 terrain이 3.438에서 시작하지만 정책이 실패하면서 즉시 curriculum이 내려간다. `iter 20` 이후를 회복 구간으로 보면 다음 threshold를 처음 재돌파한 시점은 다음과 같다.

| terrain threshold | 재도달 iter |
|---:|---:|
| 0.10 | 986 |
| 0.25 | 1248 |
| 0.50 | 1373 |
| 0.75 | 1464 |
| 1.00 | 미도달 |

termination도 같은 방향이다.

| 조건 | 최초 도달 iter (초기 붕괴 이후) |
|---|---:|
| base-contact ≤95% / timeout ≥5% | 431 |
| base-contact ≤90% / timeout ≥10% | 581 |
| base-contact ≤80% / timeout ≥20% | 약 1201 |
| base-contact ≤70% / timeout ≥30% | 약 1402 |
| base-contact ≤50% / timeout ≥50% | 미도달 |

## 5. 구간 평균

| 구간 | reward | episode | terrain | base-contact | timeout | XY err | yaw err | std |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 0~299 | -0.487 | 77.5 | 0.0742 | 99.22% | 0.05% | 0.116 | 0.185 | 0.788 |
| 300~599 | 0.568 | 285.4 | 0.0082 | 94.82% | 5.19% | 0.311 | 0.325 | 0.841 |
| 600~899 | 0.942 | 379.8 | 0.0301 | 89.52% | 10.50% | 0.391 | 0.387 | 0.940 |
| 900~1199 | 1.503 | 441.0 | 0.1176 | 85.66% | 14.36% | 0.388 | 0.446 | 1.008 |
| 1200~1499 | 2.034 | 527.7 | 0.4695 | 73.87% | 26.14% | 0.419 | 0.547 | 1.056 |

이 표에서 중요한 점은 `1200~1499` 구간부터 회복 속도가 눈에 띄게 빨라진다는 것이다. terrain 평균은 0.469, timeout은 26.1%, episode length는 528까지 올라왔다. 따라서 H-004는 수치적으로 죽은 run이 아니라 **늦게 안정성을 학습하는 run**이다.

## 6. H-001 TERM50과 동일 시점 비교

`Mean reward`는 reward 함수 자체가 달라졌으므로 직접 우열 비교에서 제외한다.

| iter | 항목 | H-001 -50 | H-004 -20 | 차이 |
|---:|---|---:|---:|---:|
| 99 | Episode length | 90.8000 | 61.7100 | -29.0900 |
| 99 | Terrain | 0.0000 | 0.0000 | +0.0000 |
| 99 | Base-contact % | 100.0000 | 100.0000 | +0.0000 |
| 99 | Timeout % | 0.0000 | 0.0000 | +0.0000 |
| 99 | XY error | 0.1310 | 0.1041 | -0.0269 |
| 99 | Yaw error | 0.2590 | 0.1483 | -0.1107 |
| 299 | Episode length | 706.3000 | 135.2200 | -571.0800 |
| 299 | Terrain | 0.8460 | 0.0000 | -0.8460 |
| 299 | Base-contact % | 48.3100 | 100.0000 | +51.6900 |
| 299 | Timeout % | 51.6900 | 0.0000 | -51.6900 |
| 299 | XY error | 0.5880 | 0.1686 | -0.4194 |
| 299 | Yaw error | 1.6570 | 0.1709 | -1.4861 |
| 499 | Episode length | 781.2000 | 268.4900 | -512.7100 |
| 499 | Terrain | 2.4410 | 0.0158 | -2.4252 |
| 499 | Base-contact % | 39.9100 | 92.9200 | +53.0100 |
| 499 | Timeout % | 60.0900 | 7.0800 | -53.0100 |
| 499 | XY error | 0.4980 | 0.3147 | -0.1833 |
| 499 | Yaw error | 1.6450 | 0.3170 | -1.3280 |
| 999 | Episode length | 819.8000 | 401.2700 | -418.5300 |
| 999 | Terrain | 4.8210 | 0.1174 | -4.7036 |
| 999 | Base-contact % | 32.3700 | 85.3300 | +52.9600 |
| 999 | Timeout % | 67.6300 | 14.6700 | -52.9600 |
| 999 | XY error | 0.4310 | 0.3977 | -0.0333 |
| 999 | Yaw error | 1.4680 | 0.4493 | -1.0187 |
| 1499 | Episode length | 686.0000 | 632.8700 | -53.1300 |
| 1499 | Terrain | 5.1190 | 0.8595 | -4.2595 |
| 1499 | Base-contact % | 32.4100 | 68.8700 | +36.4600 |
| 1499 | Timeout % | 67.5900 | 31.1300 | -36.4600 |
| 1499 | XY error | 0.3710 | 0.4715 | +0.1005 |
| 1499 | Yaw error | 1.1190 | 0.6941 | -0.4249 |

### 비교 해석

- 299 iteration부터 차이가 크게 벌어진다. H-001은 이미 episode 706, terrain 0.846, timeout 51.7%인데 H-004는 episode 135, terrain 0, timeout 0%다.
- 999 iteration에서 H-001은 terrain 4.821에 도달했지만 H-004는 0.117에 불과하다.
- 1499 iteration에는 H-004의 episode length가 633까지 따라오지만, terrain은 0.860 대 5.119, base-contact는 68.9% 대 32.4%다. 단순 episode length 회복만으로 H-001 수준의 안정성/지형 적응에 도달했다고 볼 수 없다.
- H-004의 yaw error는 전 구간에서 H-001보다 낮게 보인다. 그러나 H-004가 훨씬 쉬운 terrain에서 더 짧은 episode를 경험하고 있으므로 이를 `-20`의 회전 성능 우위로 해석하면 안 된다. H-004 내부에서도 생존시간과 terrain이 올라갈수록 yaw error가 같이 커지는 패턴이 강하다.

## 7. Tracking 숫자의 함정

H-004는 초반 XY/yaw error가 매우 낮다. 하지만 초기에는 거의 모든 episode가 base-contact로 짧게 끝나고 terrain도 0으로 내려간다. `iter >= 20` 구간에서 상관계수를 계산하면 episode length와 yaw error는 약 `+0.97`, timeout과 yaw error는 약 `+0.93`, terrain과 yaw error는 약 `+0.73`이다.

이것은 “오래 살수록 본질적으로 회전을 못한다”는 인과 증거가 아니다. 오히려 **정책이 더 오래 살아남고 더 어려운 명령/지형 경험을 쌓을수록 error metric이 평가되는 조건 자체가 어려워진다**는 confound를 강하게 보여준다. 따라서 H-004의 낮은 초기 yaw error를 성능 개선으로 채택하면 안 된다.

## 8. Reward component 변화

마지막 500 iteration 평균:

| reward term | mean |
|---|---:|
| track_lin_vel_xy_exp | +0.14525 |
| track_ang_vel_z_exp | +0.12214 |
| feet_air_time | +0.00475 |
| termination_penalty | -0.01643 |
| action_rate_l2 | -0.02534 |
| flat_orientation_l2 | -0.01167 |
| ang_vel_xy_l2 | -0.01143 |
| feet_slide | -0.02821 |
| joint_deviation_hip | -0.02175 |
| joint_deviation_arms | -0.04485 |
| dof_acc_l2 | -0.01672 |

초기 0~299에서 termination term 평균은 약 -0.01991이고 1200~1499에서는 -0.01574까지 완화된다. 즉 정책이 후반에 실제 종료 빈도를 줄이고 있다는 것과 일치한다.

동시에 action-rate, joint deviation, acceleration 비용의 절댓값이 점차 커진다. 이는 정책이 초반의 거의 움직이지 못하는/짧게 실패하는 상태에서 벗어나 점점 더 큰 동작을 사용하게 됐다는 정황이다. 다만 영상이 없으므로 이를 “좋은 공격적 보행”으로 해석하지 않는다.

## 9. PPO / 수치 안정성

- value loss max: 0.0784 @ iter 1
- value loss p99: 약 0.0077
- last-500 value loss 평균: 약 0.00488
- last-500 surrogate loss 평균: 약 -0.00407
- last-500 entropy loss 평균: 약 18.26
- action std: 최저 0.74 @ iter 136, 최종 1.08
- NaN/Inf: 보존 checkpoint 직접 검사에서 없음
- console상 OOM, broken pipe, 학습 중단, 수치 발산 패턴 없음

따라서 H-004의 낮은 성능은 optimizer/PPO 붕괴 때문이라기보다 **reward가 유도한 학습 경로의 차이**로 해석하는 것이 더 타당하다.

## 10. 처리량 / GPU

- native training time: 1203.58 s ≈ 20분 04초
- report end-to-end: 약 21분 08초
- 평균 SPS: 약 124.4k
- last-500 SPS: 약 122.5k
- 평균 collection time: 0.705 s/iter
- 평균 learning time: 0.086 s/iter
- core iteration 평균: 약 0.791 s
- personal GPU telemetry steady-state 기준 VRAM은 대체로 약 5.27 GiB
- GPU utilization 중앙값 약 53%
- power 중앙값 약 156 W
- GPU temperature 중앙값 약 46°C, 최대 48°C

장기적인 처리량 붕괴나 GPU thermal 문제는 보이지 않는다.

## 11. `model_best.pt`와 final checkpoint

finalizer는 `Train/mean_reward` 최고값을 기준으로:

- reward peak: iter 1404, 2.827
- selected checkpoint: `model_1400.pt`
- `model_best.pt`는 `model_1400.pt`와 SHA-256 exact match

하지만 1499 시점은:

- episode length: 632.87
- terrain: 0.8595
- base-contact: 68.87%
- timeout: 31.13%

으로 1404 부근보다 curriculum 진행과 episode length가 더 높다. 반면 XY/yaw error는 더 커졌다. 따라서 이번에도 `model_best`는 공식 시나리오 기준 최고 정책을 의미하지 않는다.

`model_1400`과 `model_1499` actor parameter relative L2 drift는 약 5.66%로, 마지막 99 iteration 동안 정책이 계속 의미 있게 변했다. 즉 1.5K endpoint가 완전히 포화된 정책이라고 보기 어렵다.

## 12. 보고서 자동 문구 해석 주의

자동 `report.html`은 `termination_penalty -5 -> -20`을 기준으로 “안정 지향 — 안전↑”라고 표시한다. 이는 배포 baseline `-5`와 비교하면 맞는 표현이다.

하지만 H-004의 연구 질문은 H-001 `-50`에 비해 penalty를 완화했을 때의 성격을 보는 것이다. **H-001을 parent/reference로 보면 -20은 오히려 더 공격적인 방향**이다. 따라서 자동 report의 “안정 지향” 문구를 H-001 대비 해석으로 재사용하면 안 된다.

또 report의 “추천 범위 밖”은 현재 reward source 주석의 `termination_penalty 추천 -400~-50` 기준이다. 이번 H-004는 의도적으로 그 밖의 `-20`을 screening한 실험이다.

## 13. H-004 가설 판정

### 채택되는 부분

`-20`에서도 정책은 결국 안정성을 학습하기 시작한다. 1K 이후 terrain, timeout, episode length가 뚜렷하게 상승하고 수치 발산은 없다. 따라서 `-20` 자체가 학습 불가능한 값이라는 가설은 지지되지 않는다.

### 기각되는 부분

fresh start에서 `-20`이 `-50`과 비슷한 시간 안에 충분한 안정성을 만들면서 더 적극적인 정책을 줄 것이라는 기대는 1.5K 자료에서 지지되지 않는다. H-001 대비 terrain과 생존성이 너무 늦게 형성된다.

### 새로 강화되는 가설

`-50`으로 먼저 안정성 표현을 만든 뒤, 중간 checkpoint에서 `-20`으로 완화하는 staged fine-tuning은 여전히 타당하고 오히려 이번 결과로 연구 가치가 커졌다. H-004가 후반에는 회복하고 있으므로, **-20의 장기적인 행동 자유도는 살리되 초기 curriculum 붕괴 비용은 -50 pretraining으로 피할 수 있는지**를 직접 시험할 수 있다.

## 14. 다음 의사결정

H-005/H-006의 공통 부모는 H-004가 아니라 **H-001 1.5K checkpoint**가 더 타당하다.

- H-005: H-001 1.5K → `feet_air_time 0.25` → 총 3K
- H-006: 동일 H-001 1.5K → `feet_air_time 0.30` → 총 3K

두 run은 반드시 동일한 H-001 1.5K checkpoint에서 갈라져야 `0.25 vs 0.30` 효과를 해석할 수 있다.

별도의 후속 가설로는 `H-001 1.5K -> termination -20` staged branch를 보존할 가치가 있다. 이 branch는 H-004 fresh와 비교하면 “같은 -20이지만 stability pretraining 유무”라는 매우 명확한 질문을 만든다.

## 최종 한 줄

**H-004 TERM20 fresh 1.5K는 수치적으로 정상이며 후반 회복도 분명하지만, H-001 TERM50보다 안정성 curriculum 형성이 지나치게 느려 H-005/H-006의 부모로는 부적합하다. 대신 `-50 pretrain -> -20 fine-tune` staged 가설의 필요성을 강하게 뒷받침한다.**
