> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/experiments/go2/training/2026-08-30_GO2_BASELINE_CONVERSATION_SUMMARY.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# [학습] Go2 Baseline 12k 시도 — 수치 발산·체크포인트·영상·제보 통합 정리

> 관리 안내 (2026-10-13): **학습** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](<../../../../research/EXPERIMENTS.md>)를 확인한다.

- 정리 시점: 2026-08-30
- 대상: Unitree Go2 / `Quadruped-v0`
- 목적: 개인 NVIDIA 검증 환경에서 진행한 Go2 기본 baseline 장기 학습 결과를 정리하고, 이후 reward 실험의 기준점과 공식 제보 근거를 확정
- 성격: **개인 검증 실행 분석**. 공식 제출 정책 또는 공식 평가 점수로 해석하지 않음.

---

## 1. 이번 분석에 사용한 주요 원본

이번 대화에서 확인한 핵심 자료는 다음과 같다.

- `go2_std_crash_diagnosis.tar.gz`
  - recovery bundle 2개
  - 전체 `go2-12k.log`
- `go2-recovery-20260830_125132_KST(1).tar.gz`
  - Go2/H1 학습 worktree
  - Go2 `agent_cfg.py`, `env_cfg.py`, `_finalize.py`, reward 파일 등
- `go2_original_outputs(3).zip`
  - `go2-12k.log`
  - 원본 TensorBoard event
  - `model_9500.pt`
  - 5k 이전 best snapshot
  - `env.yaml`, `agent.yaml`
  - environment metadata
  - exported policy/report 파일
- `go2_best_9500_120s.mp4`
- `go2_best_5k_120s.mp4`

분석 우선순위는 **raw console/TensorBoard/checkpoint/config → 자동 report → 해석** 순서로 두었다.

---

# 2. 실행 환경과 baseline 조건

확인된 실제 학습 명령:

```bash
isaaclab.sh -p train.py \
  --task Quadruped-v0 \
  --num_envs 4096 \
  --max_iterations 12000 \
  --headless
```

주요 환경:

| 항목 | 확인값 |
|---|---|
| Isaac Sim | `5.1.0-rc.19+release.26219.9c81211b.gl` |
| IsaacLab commit | `3e73d6dd79080fd7632488c061052a6edd52e230` |
| RSL-RL | `rsl-rl-lib==5.0.1` |
| PyTorch | `2.7.0+cu128` |
| GPU | NVIDIA L40S 46 GB |
| environments | 4096 |
| rollout steps/env | 24 |
| requested iterations | 12,000 |
| seed | 42 |
| PPO LR | `1.0e-3`, adaptive |
| desired KL | `0.01` |
| max grad norm | `1.0` |
| action distribution | Gaussian, `init_std=1.0`, `std_type=scalar` |
| checkpoint interval | 100 iterations |

사용자 측 검증 환경은 공식 서버 환경 재현을 목표로 구성됐다. 이번 archive에서 IsaacLab commit과 실행 설정은 명확히 확인되며, 해당 worktree의 IsaacLab 관련 상태도 재현 근거가 된다. 다만 현재 보존 자료만으로 **공식 서버의 모든 드라이버·패키지·런타임 요소까지 바이트 단위로 동일했다고 독립적으로 확정하지는 않는다.**

---

# 3. 가장 중요한 결론

## 3.1 12k baseline은 완주하지 못했다

요청은 12,000 iterations였지만 학습은 9.5k 이후 수치적으로 발산했다.

최종 예외:

```text
RuntimeError: normal expects all elements of std >= 0.0
```

Traceback은 PPO update 중 actor가 Gaussian distribution에서 action을 sample하는 구간까지 이어진다.

즉 최종적으로는 **Gaussian action standard deviation에 음수 값이 생겨 PyTorch `Normal` sampling이 실패한 것**이다.

하지만 이것을 최초 원인으로 보면 안 된다.

---

## 3.2 최초로 관찰되는 핵심 이상은 action std가 아니라 value loss 발산이다

raw console에서 확인되는 실제 순서는 다음과 같다.

| Iteration | Mean value loss | Mean reward | `action_rate_l2` | 상태 |
|---:|---:|---:|---:|---|
| 9500 | 0.0143 | 18.03 | -0.0812 | 정상 |
| 9512 | 2.3410 | 19.65 | -0.0842 | 첫 뚜렷한 이상 |
| 9513 | 103.2360 | 18.01 | -0.0826 | 발산 |
| 9514 | 52,437.0686 | 18.86 | -0.0829 | 심각한 발산 |
| 9515 | 1,038,605.3844 | **-2008.65** | **-105.6747** | 정책/행동 측 이상까지 발생 |
| 9516 | 0.0124 | 16.97 | -0.0838 | 일시 정상화 |
| 9517 | 0.0147 | 17.92 | -0.0840 | 일시 정상 |
| 9518 | 0.0158 | 19.07 | -0.0840 | 일시 정상 |
| 9519 | 0.0149 | 17.99 | -0.0850 | 일시 정상 |
| 9520 | 0.0140 | 18.55 | -0.0843 | 일시 정상 |
| 9524 | 0.2390 | 17.64 | -0.0834 | 재이상 시작 |
| 9525 | 46.0153 | 17.61 | -0.0837 | 재발산 |
| 9526 | 54,238.5757 | 17.64 | -0.0816 | 발산 |
| 9527 | 5.328×10^8 | 17.89 | -0.0851 | 폭발 |
| 9528 | 2.238×10^13 | 18.27 | -0.0831 | 폭발 |
| 9529 | 3.504×10^18 | 17.98 | -0.0834 | 폭발 |
| 9530 | 7.775×10^23 | 18.61 | -0.0843 | 폭발 |
| 9531 | 2.511×10^29 | 19.43 | -0.0829 | 폭발 |
| 9532 | `inf` | 19.25 | -0.0848 | 수치 붕괴 |
| 9533 | `inf` | 18.32 | -0.0830 | 수치 붕괴 |
| 9534 | `inf` | 19.41 | -0.0841 | 수치 붕괴 |
| 9535 | `nan` | 19.33 | -0.0837 | 완전 붕괴 |
| 이후 PPO update | — | — | — | negative std RuntimeError |

따라서 가장 타당한 해석은:

```text
정상 학습
→ critic/value 쪽 수치 불안정 시작
→ value loss 급격한 발산
→ 중간에 action-rate 극단값까지 발생
→ 잠깐 정상화
→ value loss 재발산
→ inf / nan
→ PPO update 상태가 무너짐
→ Gaussian std 중 음수 발생
→ torch.normal() RuntimeError로 최종 종료
```

### 핵심 판정

**최종 std 오류는 “종료를 발생시킨 직접 증상”이고, 최초로 확인되는 이상은 value loss 발산이다.**

현재 자료만으로는 value loss 발산의 최초 trigger를 한 가지로 확정할 수 없다.

---

# 4. `model_9500.pt`는 깨진 모델이 아니다

이 부분은 baseline 사용 여부를 결정하는 데 매우 중요하다.

`model_9500.pt` 내부를 직접 검사한 결과 action std 12개는:

```text
min  = 0.3000416
mean = 0.4767875
max  = 0.5927571
```

전부 정상적인 양수다.

또한 checkpoint 전체의 actor/critic/optimizer tensor에서 NaN/Inf가 확인되지 않았다.

즉:

> **9500 checkpoint 시점까지 정책 자체는 정상이다.**

이 때문에 “action std가 장기간 0을 향해 서서히 줄다가 9500 즈음 음수가 됐다”는 초기 가설은 폐기한다.

---

# 5. 5k 이전 best와 std 비교

`best_through_5k/selection.txt`의 실제 선택 결과:

```text
tag=Train/mean_reward
reward_step=4509
reward=16.573978424072266
checkpoint=model_4500.pt
```

즉 대화에서 편의상 “5k 모델”이라고 불렀지만 정확히는:

> **5k 이전 최고 reward에 대응해 선택된 `model_4500.pt`**

이다.

이 checkpoint의 action std:

```text
min  = 0.2919945
mean = 0.4824483
max  = 0.6597513
```

9500과 비교하면 평균 std는 오히려 거의 비슷하다.

| checkpoint | min std | mean std | max std |
|---|---:|---:|---:|
| 5k 이전 best (`model_4500`) | 0.2920 | 0.4824 | 0.6598 |
| `model_9500` | 0.3000 | 0.4768 | 0.5928 |

따라서 이번 crash는 **장기적으로 std가 0으로 수축해 생긴 단순 현상으로 설명되지 않는다.**

---

# 6. Go2 코드 자체에 과거 value-loss 발산 이력이 남아 있음

제공된 Go2 `training/quadruped/go2_task/agent_cfg.py`에는 다음 취지의 주석이 있다.

```text
2026-05-25 발산(iter 7097 value_loss=inf) 후 보수화했었음
(lr 5e-4 / desired_kl 0.008 / grad_norm 0.5)
...
발산 재발 시 lr만 7e-4로 한 단계 내릴 것
```

현재 실제 설정은 다시:

```text
learning_rate = 1.0e-3
desired_kl    = 0.01
max_grad_norm = 1.0
```

으로 되어 있다.

이번 실행에서도 9.5k 이후 `value_loss → inf/nan`이 재현됐다.

### 의미

이번 사건을 **단 한 번의 우연한 GPU 오류**로 보기 어렵게 만드는 강한 정황이다.

다만 코드 주석은 과거 사건에 대한 개발 기록이며, 이번 run과 과거 7097 run의 최초 trigger가 완전히 동일하다고까지 증명하지는 않는다.

---

# 7. 9515의 `action_rate_l2` 극단값

평상시 `Episode_Reward/action_rate_l2`는 대략:

```text
-0.08 전후
```

인데 iteration 9515에서:

```text
-105.6747
```

까지 급격히 변했다.

동시에 mean reward도:

```text
-2008.65
```

까지 내려갔다.

이는 단순히 critic의 숫자만 이상해진 것이 아니라 **그 시점에 실제 action 변화 측에서도 극단적인 rollout이 발생했음을 보여주는 증거**다.

하지만 순서상 value loss는 이미 9512부터 이상해졌다.

따라서 현재 해석은:

- `action_rate_l2` spike = 중요 증상/악화 요인
- `action_rate_l2` spike = 최초 원인이라고 확정 불가

이다.

---

# 8. 자동 report와 raw log가 다를 때 raw log를 우선해야 함

자동 `report.html`에는 대략:

```text
최고보상 19.65(iter 9512)
지형 5.85
낙상률 1.7%
std 약 0.485
```

가 표시된다.

또한 report의 자동 문구에는 발산 iteration을 다소 단순화해 표현하는 부분이 있다.

raw console에서는 정확히:

```text
9532 = inf
9533 = inf
9534 = inf
9535 = nan
```

이다.

따라서 자동 report의 요약 문구가 raw log와 다를 경우 **raw console/TensorBoard를 우선**한다.

또한 report가 보여주는 마지막 `mean action std ≈ 0.48~0.49`는 평균값이다. 평균 std가 정상이어도 특정 action dimension 하나가 음수가 될 수 있으므로, 평균 std 하나만으로 최종 오류를 배제할 수 없다.

---

# 9. `model_9500.pt`를 baseline으로 사용할 수 있는가?

## 판정: 사용할 수 있다. 단, 이름을 정확히 붙여야 한다.

권장 명칭:

```text
Go2 B0 Vanilla Baseline
checkpoint: model_9500.pt
training horizon: 9500 iterations
12k run truncated by PPO numerical divergence
```

또는 짧게:

```text
Go2 Vanilla 9.5k Truncated Baseline
```

### 중요한 구분

- ❌ `Go2 12k baseline 완주`
- ✅ `Go2 vanilla baseline, 9.5k 정상 checkpoint 확보 / 12k 시도는 수치 발산으로 중단`

9500은 발산 전 정상 checkpoint이므로 이후 reward 실험의 비교 기준으로 충분한 가치가 있다.

---

# 10. 이후 reward 실험의 iteration 전략

현재 결과로 보면 Go2의 실험 단계는 다음처럼 나누는 것이 적절하다.

## 10.1 5k = screening

5k 정도는 **가설 방향성 확인용**으로 쓴다.

판정 질문:

- baseline보다 tracking이 빨리 좋아지는가?
- terrain progression이 개선되는가?
- fall/base-contact가 악화되지 않는가?
- 영상에서 실제 행동 방향이 좋아지는가?

5k만 보고 “최종적으로 잘 걷는 정책”이라고 판단하지 않는다.

## 10.2 약 9.5k = baseline 공정 비교 지점

현재 B0가 9500에서 정상적으로 남아 있으므로 향후 후보도:

```text
B0 vanilla       → 9500 snapshot
S1 reward change → 9500 snapshot
S2 reward change → 9500 snapshot
```

처럼 같은 학습량에서 비교하는 것이 가장 깔끔하다.

## 10.3 12k 이상 = 추가 confirmation

reward 후보가 9500을 지나 12k까지 정상 생존한다면:

1. 9500 시점 성능을 B0와 동일 horizon으로 비교
2. 12k까지 추가 개선되는지 확인
3. 장기 수치 안정성까지 별도 장점으로 기록

하는 방식이 적절하다.

---

# 11. 5k 영상에서 “명령은 있는데 왜 안 움직이는가?”

`go2_best_5k_120s.mp4`는 정확히는 `model_4500.pt`를 사용한 영상이다.

4509 iteration의 주요 지표:

| 지표 | 값 |
|---|---:|
| mean reward | 16.57 |
| mean episode length | 1000.00 |
| `track_lin_vel_xy_exp` | 0.5140 |
| `error_vel_xy` | **1.1683 m/s** |
| terrain level | **0.9181** |
| base-contact termination | 1.60% |

이 상태는:

> **넘어지지 않고 버티는 능력은 많이 배웠지만, 명령된 선형 속도를 실제 움직임으로 따라가는 능력은 아직 부족한 상태**

로 해석하는 것이 가장 타당하다.

영상에서 목표 velocity command는 존재하지만 실제 이동 속도가 작게 보이는 현상과 수치가 일치한다.

즉 “명령 입력 버그”라기보다 **4.5k 시점 정책 미성숙**이다.

---

# 12. 4.5k → 9.5k 동안 실제 개선

9500과 비교하면 Go2가 5k 이후에도 크게 발전하고 있음을 볼 수 있다.

| 지표 | 4509 / model_4500 계열 | 9500 |
|---|---:|---:|
| mean reward | 16.57 | 18.03 |
| `track_lin_vel_xy_exp` | 0.5140 | **0.7101** |
| `error_vel_xy` | **1.1683** | **0.7192** |
| terrain level | **0.9181** | **5.8252** |
| base-contact termination | 1.60% | 1.91% |
| mean action std | ≈0.48 | ≈0.48 |

9512에서는 저장 checkpoint는 아니지만 로그상:

```text
mean reward              19.65
track_lin_vel_xy_exp      0.7953
error_vel_xy              0.5611
terrain level             5.8001
base-contact termination  1.83%
```

까지 올라갔다.

따라서 이번 실행은 **정책 성능이 정체돼 실패한 run이 아니라, 상당히 발전한 상태에서 수치 안정성 문제로 장기 학습이 중단된 run**에 가깝다.

---

# 13. 120초 영상이 20초마다 계단 근처로 돌아오는 이유

실제 `env.yaml`:

```yaml
episode_length_s: 20.0
```

그리고:

```yaml
terminations:
  time_out:
    time_out: true
```

로 되어 있다.

즉 episode 최대 길이가 **20초**다.

`go2_best_9500_120s.mp4`는 50 FPS, 총 약 119.98초인데, 영상 프레임 변화와 config가 일치하며 약:

```text
20s
40s
60s
80s
100s
```

부근에서 episode timeout reset이 발생한다.

따라서 120초 영상은:

```text
0~20s      episode 1
20~40s     episode 2
40~60s     episode 3
60~80s     episode 4
80~100s    episode 5
100~120s   episode 6
```

에 가까운 구조다.

### 의미

120초 영상으로:

- ✅ 여러 episode에서 반복적으로 행동하는지 볼 수 있음
- ❌ “120초 연속으로 안 넘어지고 걸었다”고 주장할 수 없음

---

# 14. 30초 부근에서 방향이 다시 바뀌는 이유

실제 command config:

```yaml
commands:
  base_velocity:
    resampling_time_range:
    - 10.0
    - 10.0
```

즉 이동 명령이 **10초마다 다시 샘플링**된다.

따라서 예를 들면:

```text
20s → episode reset
30s → velocity command 재샘플링
40s → episode reset
```

이 된다.

그래서 30초 부근에서 로봇이 다시 계단 방향 등 다른 방향으로 가려는 것은 순간이동이 아니라 **새 velocity command에 대한 반응**으로 볼 수 있다.

---

# 15. 영상 export 길이 운영 결론

현재 play 환경에서 단일 episode가 최대 20초이므로:

## 단일 행동 품질 확인

```text
18~20초면 충분
```

특히 20초 끝에서 reset 장면이 들어갈 수 있으므로 보기 좋은 clip은 18~19초 정도도 적절하다.

## 60~120초 영상의 의미

완전히 무의미한 것은 아니다.

긴 영상은:

- 여러 reset 후에도 행동이 반복되는지
- 여러 velocity command에서 이상행동이 있는지
- 특정 episode에서만 붕괴하는지

를 보는 robustness 관찰용으로 사용할 수 있다.

하지만 **장시간 연속 생존 증명용으로는 사용하지 않는다.**

---

# 16. finalizer 때문에 중간 checkpoint가 사라진 문제

Go2 `_finalize.py`에는 기본 cleanup 동작이 있다.

핵심 구조:

```text
_cleanup_intermediate_checkpoints(...)
→ 선택된 best checkpoint 한 개만 보존
→ 나머지 model_*.pt 삭제
```

실제 코드 설명에도 기본 `cleanup=True`일 때 intermediate checkpoint를 삭제하도록 되어 있다.

이번 실행에서는 최종적으로:

```text
reward best step = 9512
nearest saved checkpoint = model_9500.pt
```

가 선택되어 `model_9500.pt`가 보존됐다.

그 결과 현재 정확한 9k checkpoint 등 다른 중간 모델은 보존본에 없다.

## 이후 원칙

장기 run에서는 **finalizer/cleanup 전에** 다음을 먼저 별도 복사한다.

- `logs/<run>/` 전체
- 모든 `model_*.pt`
- TensorBoard event
- params
- console log

그 뒤 finalize를 실행한다.

---

# 17. 공식 제보 여부

## 판정: 제보할 가치가 충분함

이유:

1. vanilla/baseline 장기 run에서 발생
2. 9500까지 정상 학습 후 value loss가 급격히 발산
3. 최종적으로 학습 자체가 12k 전에 종료
4. Go2 `agent_cfg.py`에 과거 `iter 7097 value_loss=inf` 이력이 이미 기록돼 있음
5. 참가자가 reward 외 PPO/RSL-RL 내부를 임의로 수정해서 해결하기 애매한 유형

따라서 단순히 “개인 서버가 이상했다”로 넘기기보다는 운영진/개발팀에 재현 자료를 전달할 가치가 있다.

---

# 18. 실제로 올린 버그 리포트의 핵심 내용

사용자가 공식 채널에 전달한 내용의 핵심은 다음과 같다.

```text
Go2 기본 설정으로 12,000 iteration baseline을 실행하던 중
약 9,500 이후 value loss가 급격히 증가했고,
최종적으로
RuntimeError: normal expects all elements of std >= 0.0
로 종료됨.

TensorBoard/raw log에서 value loss:
9512: 2.34
9513: 103.24
9514: 52,437
9515: 1,038,605
9532~9534: inf
9535: nan

model_9500.pt의 action std 12개는 모두 약 0.30~0.59의 정상 양수이고,
checkpoint 내부 parameter에서도 NaN/Inf는 확인되지 않음.

또한 제공 Go2 agent_cfg.py에 과거 iter 7097 value_loss=inf 발산 이력이 남아 있어
동일 장기 학습 안정성 문제 재발 여부를 문의.
```

이 보고 방식은 적절하다.

특히 **“공식 서버 버그 확정”이라고 단정하지 않고 개인 검증 환경에서 관찰한 재현 현상으로 제보한 점**이 좋다.

---

# 19. 운영진에게 추가로 보낼 ZIP

현재 준비된:

```text
go2_original_outputs.zip
```

계열 archive는 후속 증거 제출용으로 적절하다.

실제 포함된 핵심 원본:

- `go2-12k.log`
- `events.out.tfevents*`
- `model_9500.pt`
- 5k 이전 selected checkpoint
- `env.yaml`
- `agent.yaml`
- 환경/패키지 정보
- IsaacLab git 정보
- exported policy/report

즉 운영진이 재현/원인 확인을 요청하면 **가공된 요약만 보내기보다 이 원본 bundle을 그대로 전달하는 방식**이 좋다.

파일명과 내부 원본 구조는 임의로 바꾸지 않는 것을 권장한다.

---

# 20. 지금 당장 PPO/RSL-RL을 고칠 것인가?

## 공식 환경 재현용 baseline에서는 수정하지 않는 것이 맞다

예를 들어:

- std clamp 추가
- RSL-RL 버전 업데이트
- PPO learning rate 수정
- max grad norm 수정

등을 해버리면 그 순간부터 **현재 공식 제공 환경 재현 baseline과 다른 실험**이 된다.

따라서 현재 B0는 그대로 보존한다.

개인 서버에서 원인 규명 목적으로 별도 진단 run을 한다면:

```text
DIAG-LR7e-4
DIAG-STD-GUARD
DIAG-RSLRL-NEW
```

처럼 **baseline과 별도 실험 ID로 분리**해야 한다.

---

# 21. 현재 확정된 것 / 아직 확정되지 않은 것

## 확정도가 높은 사실

- 12k는 완주하지 못함.
- 실제 정상 checkpoint `model_9500.pt`가 존재함.
- 9500 checkpoint의 std는 모두 양수이고 전체 tensor가 finite임.
- 9512부터 value loss가 뚜렷하게 이상해짐.
- 9515에서 reward/action-rate 극단값 발생.
- 9524 이후 value loss가 다시 폭발.
- 9532~9534 `inf`, 9535 `nan`.
- 이후 Gaussian sampling에서 std 음수 오류로 종료.
- Go2 agent config에 과거 `iter 7097 value_loss=inf` 이력이 기록돼 있음.
- 5k 이전 best는 실제로 `model_4500.pt`.
- 4.5k에서는 선형 velocity tracking이 아직 상당히 부족함.
- 9.5k에서는 tracking/terrain이 4.5k보다 크게 개선됨.
- episode 최대 길이는 20초.
- velocity command는 10초마다 resample됨.
- 120초 영상은 여러 20초 episode의 연속 기록임.

## 아직 확정할 수 없는 것

- value loss 폭발을 최초로 촉발한 단일 원인
- 특정 observation/return outlier가 최초 trigger였는지
- 9512 이전 일부 environment에서 극단값이 있었는지
- 공식 서버에서도 동일 iteration 부근에서 반드시 재현되는지
- 동일 설정의 다른 seed/run에서도 같은 빈도로 발생하는지
- PPO LR 하나만 낮추면 재발이 사라지는지

이 항목들은 추가 진단 run 또는 운영진 답변이 필요하다.

---

# 22. 현재 baseline 판정

## 최종 정리

### B0

```text
Robot: Go2
Type: Vanilla baseline
Checkpoint: model_9500.pt
Status: valid pre-divergence checkpoint
Requested run: 12,000 iterations
Actual training: ~9,536 iterations before failure
Failure mode: value-loss divergence → inf/nan → Gaussian std RuntimeError
```

### 5k snapshot

```text
Label: best through 5k
Actual checkpoint: model_4500.pt
Use: early screening reference
Limitation: linear velocity tracking still weak
```

---

# 23. 이후 실험에 적용할 실무 규칙

1. **Go2 5k는 screening 용도**로 사용한다.
2. **Go2 B0 비교 기준은 `model_9500.pt`**로 고정한다.
3. reward 후보도 가능하면 9500 snapshot을 남겨 같은 horizon끼리 비교한다.
4. 12k까지 살아남는 후보는 “추가 성능 + 장기 안정성”을 별도로 평가한다.
5. mean reward 하나만 보고 best를 판단하지 않는다.
6. tracking error, terrain progression, fall/base-contact, 영상까지 함께 본다.
7. play 영상은 단일 행동 비교라면 18~20초 정도면 충분하다.
8. 60~120초 영상은 여러 episode 반복 안정성 확인용으로만 쓴다.
9. 장기 run에서는 finalizer 실행 전에 모든 checkpoint와 event/log를 먼저 백업한다.
10. 공식 답변 전에는 제공 PPO/RSL-RL 설정을 baseline에서 임의 수정하지 않는다.
11. 운영진이 자료를 요청하면 `go2_original_outputs.zip` 계열 원본 bundle을 그대로 전달한다.

---

# 24. 한 줄 결론

> **이번 Go2 vanilla 12k 시도는 정책이 못 배워서 실패한 것이 아니라, 약 9.5k까지 상당히 정상적으로 학습된 뒤 value network가 수치적으로 발산하고 최종적으로 Gaussian action std 오류까지 이어져 중단된 실행이다. `model_9500.pt`는 발산 전 정상 checkpoint이므로 Go2 B0 baseline으로 사용할 수 있으며, 5k 이전 best는 아직 명령 추종이 미성숙한 screening 단계로 보는 것이 적절하다.**

---

## 부록 A. 핵심 수치 빠른 참조

### `model_4500` 계열 (best through 5k)

```text
reward best step       4509
reward                 16.574
track_lin_vel_xy_exp    0.5140
error_vel_xy            1.1683 m/s
terrain level           0.9181
base_contact            1.60%
checkpoint std          0.2920 ~ 0.6598
```

### `model_9500`

```text
iteration               9500
mean reward             18.03
value loss              0.0143
track_lin_vel_xy_exp    0.7101
error_vel_xy            0.7192 m/s
terrain level           5.8252
base_contact            1.91%
checkpoint std          0.3000 ~ 0.5928
all checkpoint tensors  finite
```

### reward peak 로그

```text
iteration               9512
mean reward             19.652
value loss              2.3410
track_lin_vel_xy_exp    0.7953
error_vel_xy            0.5611 m/s
terrain level           5.8001
base_contact            1.83%
nearest saved model     model_9500.pt
```

### 최종 발산

```text
9532 value loss = inf
9533 value loss = inf
9534 value loss = inf
9535 value loss = nan
→ PPO update
→ RuntimeError: normal expects all elements of std >= 0.0
```

---

## 부록 B. 자료 보존 우선순위

다음 Go2/H1 장기 실행부터 최소한 아래를 종료 전에 보존한다.

```text
logs/<run>/ 전체
├── events.out.tfevents*
├── model_*.pt 전체
├── params/env.yaml
├── params/agent.yaml
└── git diff / metadata

console log
실제 실행 command
환경/package 정보
GPU/runtime 정보
play 영상
exported policy/report
```

특히 **중간 checkpoint는 finalize cleanup 전에 복사**한다.
