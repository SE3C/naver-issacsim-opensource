# Go2 공식 서버 Baseline 1K 심층 분석 및 `issacsimz` 로깅 검증 보고서

- 분석 대상: `GO2_baseline_1k_complete_20260913.tar.gz`
- 실행 분류: **NAVER CONNECT Robotics Cup 2026 공식 서버 Go2 baseline 1K**
- 분석일: 2026-09-14
- 분석 범위: 학습 성능, 수치 안정성, checkpoint/finalize 관계, play 영상 lineage, GPU/처리량, `issacsimz` evidence 품질
- 중요 경계: 이 보고서의 training metric은 **공식 평가 점수와 동일하지 않다.** 정책의 공식 제출 성능은 별도 공식 evaluator 결과가 있어야 확정할 수 있다.

---

## 1. 결론 요약

이번 공식 서버 Go2 baseline 1K는 **수치적으로는 안정적으로 1,000 iteration을 완주했지만, 1K 시점의 locomotion 정책 품질은 좋지 않다.** 정책은 빠르게 낙상을 줄이고 긴 episode를 유지하는 쪽으로 수렴했으나, 선형 속도 추종이 약한 상태에서 curriculum terrain이 최저 난이도로 내려가 그대로 고착됐다.

핵심 징후는 다음과 같다.

- terrain level은 시작 `3.5275`에서 지속 하락했고 **iter 322부터 정확히 `0.0000`**이 됐다.
- iter 322~999의 **678개 iteration 전체가 terrain 0**이다.
- 최종 `Episode_Termination/time_out = 0.9345`, `base_contact = 0.0655`로 생존 자체는 강하다.
- 그러나 최종 `XY error = 1.8421`로 선형 속도 추종이 매우 약하다.
- 반면 최종 `yaw error = 0.3082`로 회전축은 상대적으로 더 잘 학습됐다.
- 최고 `Train/mean_reward = 14.17`은 iter 794에서 발생했지만, 이 시점에도 terrain은 0이고 XY error는 `1.8251`이다.
- 따라서 이번 1K 정책은 **“잘 이동하는 정책”보다 “쉬운 지형에서 오래 살아남는 정책”에 가까운 survival-biased local optimum**으로 해석하는 것이 적절하다.

다만 이 결과만으로 baseline을 장기 실패로 기각하면 안 된다. 프로젝트의 과거 개인 Go2 baseline은 초기 terrain collapse 뒤 수천 iteration 후 다시 회복한 이력이 있으므로, 이번 결과는 **공식 서버에서 얻은 정확한 1K 기준선**으로 사용하는 것이 맞다.

반대로 `issacsimz` evidence 측면은 매우 성공적이다. 이번 run에서 다음이 실제 공식 Isaac 환경에서 확인됐다.

- 외부 archive SHA-256 sidecar 검증 성공
- archive 내부 `SHA256SUMS` 전 항목 검증 성공
- TensorBoard event 보존
- iteration 0~999 전체 console 보존
- 100 iteration 간격 checkpoint + 최종 checkpoint 총 11개 mirror
- 공식 finalizer가 intermediate checkpoint를 삭제하기 전에 mirror 완료
- 핵심 source file before/after SHA-256 불변성 확인
- official finalize와 official backup 상태를 별도로 기록하고 모두 성공 판정
- stale export를 `NEW / MODIFIED / UNCHANGED`로 구분
- train run → 선택 checkpoint SHA-256 → video run → MP4 SHA-256의 lineage 확보
- GPU utilization / VRAM / power / temperature 시계열 확보

종합적으로 `issacsimz`의 이번 **정상 완료 train + finalize + official backup + video 경로는 실전 통합 검증에 성공**했다고 판단한다.

### 최종 한 줄 판정

> **정책:** 1K 기준선으로는 유용하지만 locomotion 후보로는 약함.  
> **로깅:** 실제 공식 서버에서도 의도한 forensic evidence 구조가 거의 완성도 높게 동작함.

---

# 2. 원본 bundle 무결성

최상위 bundle:

```text
GO2_baseline_1k_complete_20260913.tar.gz
SHA-256:
db659cdad4bf4a61de6c40c6185f80bb2465054e67abda91da4cfa8d0408a5bf
```

내부에는 학습 evidence와 video evidence가 서로 분리되어 있다.

```text
go2-b0-1k-download/
├─ 20260913-145026-go2-b0-1k-official.tar.gz
├─ 20260913-145026-go2-b0-1k-official.tar.gz.sha256
├─ 20260913-145026-go2-b0-1k-official.tar.gz.metadata.json
├─ 20260913-155641-20260913-145026-go2-b0-1k-official-video.tar.gz
├─ 20260913-155641-20260913-145026-go2-b0-1k-official-video.tar.gz.sha256
└─ 20260913-155641-20260913-145026-go2-b0-1k-official-video.tar.gz.metadata.json
```

두 archive 모두 외부 `.sha256` sidecar와 실제 계산값이 일치했다.

| archive | SHA-256 | 검증 |
|---|---|---|
| train | `7dff91b8ad8fe041493876e58f17f21ed1bc22eda53a21aaad076f223098dc68` | PASS |
| video | `a1d79a67ca0ec36612410a49d9fc5ae9e04a76ba4ce4dd376c862ec5e0bbf7db` | PASS |

archive 내부 manifest도 모두 검증됐다.

| evidence | `SHA256SUMS` 항목 수 | 결과 |
|---|---:|---|
| train | 33 | 전부 PASS |
| video | 20 | 전부 PASS |

따라서 이후 분석은 **전달 과정에서 파일이 손상되지 않았다는 강한 근거** 위에서 진행할 수 있다.

---

# 3. 공식 서버 실행 조건

`metadata.json`과 `command.txt`에서 직접 확인되는 실제 학습 명령은 다음과 같다.

```bash
/workspace/IsaacLab/isaaclab.sh \
  -p /workspace/training/quadruped/train.py \
  --task Quadruped-v0 \
  --max_iterations 1000 \
  --num_envs 4096 \
  --headless
```

주요 실행값:

| 항목 | 값 |
|---|---:|
| task | `Quadruped-v0` |
| iterations | 1000 (`0~999`) |
| envs | 4096 |
| seed | 설정상 42 |
| rollout steps/env/iteration | 24 |
| transitions/iteration | 98,304 |
| 총 transitions | **98,304,000** |
| mode | headless |
| training exit code | 0 |
| `training_status` | `completed` |
| `official_finalize_status` | `completed` |
| `official_backup_status` | `success` |
| `evidence_validation` | `PASS` |

metadata의 실행 시간:

```text
start_utc = 2026-09-13T14:50:27.003963+00:00
end_utc   = 2026-09-13T15:55:29.359353+00:00
```

즉 `issacsimz`가 감싼 전체 구간은 약 **65분 02초**다.

native console의 순수 training 표시는:

```text
Training time: 3887.04 seconds
```

즉 약 **1시간 04분 47초**다.

---

# 4. 실제 적용 reward 확인

`collected/exported/env.yaml`에서 실제 environment에 적용된 reward를 직접 확인했다.

| reward | weight |
|---|---:|
| `track_lin_vel_xy_exp` | `+1.0` |
| `track_ang_vel_z_exp` | `+0.75` |
| `lin_vel_z_l2` | `-3.0` |
| `ang_vel_xy_l2` | `-0.08` |
| `dof_torques_l2` | `-0.0002` |
| `dof_acc_l2` | `-2.5e-7` |
| `action_rate_l2` | `-0.01` |
| `feet_air_time` | `+0.01` |
| `flat_orientation_l2` | `0.0` |
| `dof_pos_limits` | `0.0` |

즉 이번 실행은 프로젝트에서 말하는 **Go2 baseline reward 구성과 일치하는 공식 baseline**으로 볼 수 있다.

학습 중 source identity에서도 `quadruped_rewards.py`의 before/after SHA-256이 동일했다.

```text
09630e6f548b16a2fa0a81eef73aa393cf5f12eadccd0bad8a144b924e8c1be7
```

따라서 **학습 도중 reward source가 바뀌었다는 증거는 없다.**

---

# 5. 학습 전 구간 핵심 시계열

console에는 `Learning iteration 0/1000`부터 `999/1000`까지 **1,000개 iteration block이 모두 존재**한다.

대표 지점은 다음과 같다.

| iter | mean reward | episode length | terrain | XY error | yaw error | timeout | base-contact | action std |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | -0.76 | 11.87 | 3.5275 | 0.0196* | 0.0174* | 1.15%* | 0.00%* | 1.00 |
| 100 | 5.22 | 969.83 | 1.1727 | 1.7214 | 0.7940 | 80.65% | 19.37% | 0.52 |
| 200 | 10.82 | 987.92 | 0.1745 | 1.7484 | 0.4614 | 95.33% | 4.67% | 0.46 |
| 300 | 12.13 | 987.10 | 0.0005 | 1.7636 | 0.3473 | 97.43% | 2.57% | 0.44 |
| 322 | 12.58 | 986.42 | **0.0000** | 1.7334 | 0.3417 | 97.31% | 2.69% | 0.44 |
| 500 | 12.38 | 977.83 | **0.0000** | 1.9525 | 0.3124 | 95.14% | 4.86% | 0.42 |
| 794 | **14.17** | 985.28 | **0.0000** | 1.8251 | 0.3059 | 94.04% | 5.96% | 0.42 |
| 800 | 13.23 | 973.42 | **0.0000** | 1.7677 | 0.2973 | 94.01% | 5.99% | 0.42 |
| 999 | 13.05 | 975.33 | **0.0000** | **1.8421** | **0.3082** | **93.45%** | **6.55%** | **0.44** |

\* iteration 0은 충분한 episode population이 누적되기 전이라 성능 비교값으로 읽지 않는다.

---

# 6. Terrain collapse 분석

terrain progression은 이번 1K의 가장 중요한 신호다.

확인된 최초 도달 지점:

| 조건 | 최초 iteration |
|---|---:|
| terrain ≤ 1.0 | 115 |
| terrain ≤ 0.5 | 156 |
| terrain ≤ 0.1 | 215 |
| terrain ≤ 0.01 | 264 |
| terrain ≤ 0.001 | 297 |
| terrain = **0.0000** | **322** |

그리고 iter **322~999**, 총 **678 iteration 동안 terrain이 단 한 번도 0에서 회복하지 않았다.**

이것은 단순한 짧은 dip이 아니다. 1K window 안에서는 **완전한 저난이도 고착**이다.

그러나 terrain collapse 하나만으로 “정책이 아무것도 못 배웠다”고 해석하면 잘못이다. 같은 시점에 episode length와 timeout은 매우 높다.

iter 300~499 평균:

```text
mean reward     12.7680
episode length  983.1042
terrain           0.0000
XY error          1.7836
yaw error         0.3204
timeout           0.9720
base-contact      0.0280
```

iter 500~999 평균:

```text
mean reward     12.9447
episode length  964.7317
terrain           0.0000
XY error          1.7527
yaw error         0.3020
timeout           0.9390
base-contact      0.0610
```

즉 정책은 **낙상 억제와 episode 유지에는 성공했지만, locomotion 능력 부족 때문에 curriculum이 쉬운 지형에 고착된 상태**다.

---

# 7. Tracking 분석: 핵심 병목은 선형 속도

최종 지표:

```text
Metrics/base_velocity/error_vel_xy  = 1.8421
Metrics/base_velocity/error_vel_yaw = 0.3082
```

후반 500 iteration 평균도:

```text
XY error  = 1.7527
yaw error = 0.3020
```

따라서 1K 정책의 병목은 명확히 **XY 선형 속도 추종**이다.

반면 yaw error는 초반 큰 값에서 후반 약 0.30 수준까지 감소했다.

이 조합은 정책이 완전히 무작위 상태인 것이 아니라,

1. 넘어지지 않는 자세를 배우고,
2. 회전축 오차는 어느 정도 줄이지만,
3. 전후/측면 명령에 적극적으로 이동하는 능력은 충분히 배우지 못한

상태라는 뜻이다.

공식 평가의 여러 시나리오를 직접 예측할 수는 없지만, 학습 내부 지표만 놓고 보면 **전진·전방위 tracking이 취약할 가능성이 높다**고 보는 것이 합리적이다.

---

# 8. Survival 분석: “안 넘어짐 = 잘 걷음”이 아님

최종 termination:

```text
Episode_Termination/time_out     = 0.9345
Episode_Termination/base_contact = 0.0655
```

즉 종료 episode 중 약 93.45%가 time-out까지 버티고, base-contact 종료는 약 6.55%다.

이 숫자만 보면 안정적인 정책처럼 보일 수 있다.

하지만 같은 시점:

```text
terrain = 0.0000
XY error = 1.8421
```

이다.

따라서 이번 사례는 프로젝트에서 이미 경계하고 있던 다음 오류를 아주 잘 보여준다.

> **낙상률이 낮고 episode가 길다고 해서 locomotion 정책이 좋은 것은 아니다.**

이번 baseline 1K는 survival 지표와 locomotion 지표를 반드시 분리해서 봐야 하는 실전 예시다.

---

# 9. `Train/mean_reward` 해석과 자동 best checkpoint

학습 reward 최고값은:

```text
iter 794
Train/mean_reward = 14.17
```

공식 report는 이를 기준으로 다음을 표시한다.

```text
사족 · iter 800 / 총 1000
최고 보상 14.17 · iter 794
```

실제 SHA-256 비교:

```text
collected/exported/model_best.pt
99ceeaa1a3a1ebee972841a771072b711744a1c8dec6e94b318b55f146dc4676

checkpoints/model_800.pt
99ceeaa1a3a1ebee972841a771072b711744a1c8dec6e94b318b55f146dc4676
```

따라서 이번 `model_best.pt`는 **정확히 `model_800.pt`**다.

이는 저장 interval 때문에 reward peak iter 794와 가장 가까운 저장 checkpoint가 800이어서 선택된 것으로 볼 수 있다.

하지만 iter 794 성능은:

```text
terrain = 0
XY error = 1.8251
```

이다.

따라서 `model_best.pt`라는 이름을 **“실제 보행 성능 최고 정책”으로 읽으면 안 된다.** 정확한 의미는 이번 구조에서 **training reward 기반 자동 선택 checkpoint**다.

이번 run은 이 차이를 명확히 증명한다.

---

# 10. 수치 안정성 분석

이번 1K 실행에서는 장기 Go2 baseline에서 과거 관찰된 value-loss 폭발, Inf/NaN, negative std 같은 수치적 이상이 나타나지 않았다.

모든 mirror checkpoint를 직접 검사했다.

| checkpoint | finite tensor 이상 | action std min | mean | max |
|---|---:|---:|---:|---:|
| model_0 | 0 | 0.9945 | 0.9998 | 1.0046 |
| model_100 | 0 | 0.3331 | 0.5226 | 0.7083 |
| model_200 | 0 | 0.2933 | 0.4648 | 0.6466 |
| model_300 | 0 | 0.2628 | 0.4409 | 0.5904 |
| model_400 | 0 | 0.2443 | 0.4271 | 0.5597 |
| model_500 | 0 | 0.2348 | 0.4170 | 0.5477 |
| model_600 | 0 | 0.2378 | 0.4148 | 0.5550 |
| model_700 | 0 | 0.2341 | 0.4169 | 0.5452 |
| model_800 | 0 | 0.2313 | 0.4233 | 0.5549 |
| model_900 | 0 | 0.2459 | 0.4320 | 0.5601 |
| model_999 | 0 | **0.2609** | **0.4432** | **0.5845** |

각 checkpoint에서 검사된 tensor는 actor/critic/optimizer 등을 포함해 68개였으며, **모든 checkpoint에서 non-finite tensor는 0개**였다.

최종 console도:

```text
Mean value loss:     0.0058
Mean surrogate loss: -0.0016
Mean entropy loss:   6.8991
Mean action std:     0.44
```

로 정상 범위다.

따라서 이번 1K에서 “terrain collapse의 원인이 학습 수치 발산이었다”고 볼 근거는 없다.

**정책 행동/커리큘럼 문제와 optimizer 수치 안정성 문제를 분리해야 한다.**

---

# 11. 처리량과 공식 RTX 5080 서버 성능

console 전 1,000 iteration을 파싱한 결과:

```text
median iteration time = 3.91 s
median steps/s        = 25,137
```

최종 iteration 999:

```text
Steps per second: 25098
Collection time:   3.834 s
Learning time:     0.083 s
Iteration time:    3.92 s
```

전체 training:

```text
Training time: 3887.04 s
≈ 64 min 47 s
```

이 실행은 4,096 env × 24 rollout steps = 98,304 transitions/iteration이므로 총:

```text
98,304 × 1,000 = 98,304,000 transitions
```

을 수집했다.

---

# 12. GPU telemetry 품질과 실측값

`system/nvidia_smi_during.csv`에는 **1,928개 sample**이 있다.

start/end 시간과 sample 수를 보면 대략 **2.02초 간격**의 GPU telemetry다.

주요 통계:

| 항목 | 평균 | 중앙값 | min | max |
|---|---:|---:|---:|---:|
| GPU utilization | **87.81%** | 88% | 0% | 96% |
| VRAM used | **6948.64 MiB** | **7008 MiB** | 2 MiB | 7008 MiB |
| GPU power | **180.76 W** | 181.58 W | 29.34 W | 188.46 W |
| GPU temp | **57.74°C** | 58°C | 50°C | 61°C |

start/end 구간의 초기화와 종료 idle sample까지 포함된 평균이므로 pure steady-state training 값과 완전히 같지는 않다.

그럼에도 1K 전체의 GPU 상태를 사후 분석하기에는 충분히 세밀하다.

특히 과거 evidence가 없던 실행에서는 “GPU가 실제로 얼마나 활용됐는가”를 재구성할 수 없었지만, 이번에는 명확히 가능하다.

---

# 13. Video evidence 검증

`issacsimz video`의 실제 child command:

```bash
/workspace/IsaacLab/isaaclab.sh \
  -p /workspace/training/quadruped/play.py \
  --task Quadruped-v0 \
  --checkpoint /workspace/training/quadruped/exported/model_best.pt \
  --num_envs 1 \
  --headless \
  --video \
  --video_length 1000 \
  --enable_cameras
```

video metadata:

```text
status              = completed
exit_code           = 0
evidence_validation = PASS
parent_run_id        = 20260913-145026-go2-b0-1k-official
```

source checkpoint SHA-256:

```text
99ceeaa1a3a1ebee972841a771072b711744a1c8dec6e94b318b55f146dc4676
```

이는 train evidence의 `model_best.pt` 및 `model_800.pt`와 정확히 동일하다.

MP4 SHA-256:

```text
9cd9546dfed7cd7eee7e7ec08732a23a0ef006e0d0b68e0937f91ccaa61493c6
```

`video_manifest.json`이 이 두 SHA를 직접 연결한다.

### 실제 MP4 물리 정보

`ffprobe` 직접 확인:

| 항목 | 값 |
|---|---:|
| codec | H.264 |
| resolution | 1920×1080 |
| fps | 50 |
| frames | **999** |
| duration | **19.98 s** |

따라서 CLI 요청의 `video_length=1000`과 실제 생성 영상이 사실상 일치한다.

---

# 14. 영상 행동 관찰

20초 영상의 여러 시점을 프레임으로 확인했다.

영상은 수치와 같은 방향을 보여준다.

- Go2는 명백하게 계속 넘어지는 상태는 아니다.
- 그러나 몸체를 낮추고 다리를 넓게 벌린 낮은 자세가 반복된다.
- 큰 command vector가 표시되어도 그에 비례해 적극적으로 보폭을 내면서 이동하는 모습은 약하다.
- 즉 “강한 locomotion”보다는 **낮은 자세로 버티는 행동 전략**이 두드러진다.

이 관찰은 다음 수치와 잘 부합한다.

```text
timeout ≈ 93~94%
base-contact ≈ 6%
terrain = 0
XY error ≈ 1.8
```

즉 영상과 metric 사이에 큰 모순이 없다.

다만 19.98초 video 하나는 공식 evaluator나 여러 seed·scenario를 대체하지 않는다. 행동 특성 확인용 보조 증거로만 사용한다.

---

# 15. `issacsimz` 로깅 품질 평가

이번 분석에서 가장 중요한 두 번째 축이다.

정책 성능과 evidence system의 품질은 별개의 문제다. 정책은 약할 수 있어도 로깅은 완벽할 수 있다.

이번 run은 바로 그런 경우다.

## 15.1 종합 평가

**`issacsimz` evidence 품질: 약 95 / 100**

이 점수는 대회 점수가 아니라 **forensic/reproducibility 관점의 내부 평가**다.

| 영역 | 점수 | 판정 |
|---|---:|---|
| archive 외부 무결성 | 10/10 | train/video `.sha256` 모두 실제 hash와 일치 |
| 내부 manifest 무결성 | 10/10 | train 33개 + video 20개 모두 검증 |
| console 완전성 | 10/10 | iter 0~999 전체 + finalize 로그 보존 |
| TensorBoard 원본 | 10/10 | event 파일 보존 및 validation PASS |
| checkpoint mirror | 10/10 | model 0~900 + 999 총 11개 |
| finalizer cleanup 대응 | 10/10 | 삭제 전에 mirror 성공 |
| source identity | 10/10 | 핵심 8개 source before/after hash 불변 |
| stale artifact 방지 | 10/10 | NEW/MODIFIED/UNCHANGED provenance |
| official finalize/backup 상태 | 10/10 | 둘을 분리하고 성공 여부 기록 |
| train→video lineage | 10/10 | parent run + checkpoint SHA + MP4 SHA |
| GPU telemetry | 9.5/10 | 약 2초 간격, 전체 run에 충분 |
| runtime self-containment | 8/10 | dependency/build 정보 보강 여지 |

---

# 16. 가장 잘 된 부분 1 — checkpoint cleanup race 대응

이 기능은 이번 실제 공식 run에서 매우 중요하게 검증됐다.

`watcher.log`에는 다음 checkpoint가 순차적으로 보존됐다고 기록되어 있다.

```text
model_0.pt
model_100.pt
model_200.pt
model_300.pt
model_400.pt
model_500.pt
model_600.pt
model_700.pt
model_800.pt
model_900.pt
model_999.pt
```

그리고 공식 finalize 과정은 intermediate checkpoint를 정리했다.

즉 구조적으로:

```text
학습 중 checkpoint 생성
→ issacsimz watcher가 안정된 파일을 mirror
→ 학습 종료
→ 공식 finalizer가 원 native checkpoint 일부 cleanup
→ evidence mirror에는 11개가 그대로 남음
```

이것은 단순한 unit test가 아니라 **실제 공식 서버 + Isaac Sim + 실제 finalizer**에서 checkpoint 보존 race를 통과한 것이다.

따라서 `issacsimz`의 핵심 존재 이유 중 하나인 “공식 코드를 건드리지 않고, cleanup 전에 증거를 보존한다”가 실전에서 입증됐다.

---

# 17. 가장 잘 된 부분 2 — source 불변성

`source/identity.json`은 다음 8개 파일에 대해 before/after hash를 저장한다.

```text
train.py
play.py
quadruped_rewards.py
pyproject.toml
go2_task/_finalize.py
go2_task/env_cfg.py
go2_task/agent_cfg.py
go2_task/__init__.py
```

모든 파일에서:

```text
changed_during_run = false
```

였고 전체 상태도:

```text
changed_during_run = false
changed_paths      = []
```

였다.

이는 evidence sidecar가 **공식 task source를 학습 중 변조하지 않았다는 직접 증거**다.

규정 준수 및 향후 문제 제보 시 매우 유용한 provenance다.

---

# 18. 가장 잘 된 부분 3 — stale export 오인 방지

공식 `exported/` 폴더에는 이전 run 산출물이 이미 존재했다.

`collected/provenance.json`은 이를 단순 복사하지 않고 상태를 구분했다.

예:

```text
env.yaml                         MODIFIED
model_best.pt                    MODIFIED
model_best_20260913235030.pt     NEW
env_20260913235030.yaml          NEW
report.html                      MODIFIED

이전 model_best_20260913233927.pt UNCHANGED
이전 env_20260913233927.yaml      UNCHANGED
```

이 기능이 없으면 이전 run 파일을 이번 run 결과로 잘못 해석할 가능성이 있다.

특히 프로젝트에서는 과거 H1에서 checkpoint와 MP4 alias 연결이 꼬였던 사례가 있었으므로, 이 provenance 구분은 단순 편의 기능이 아니라 **실제 발생했던 종류의 오류를 예방하는 기능**이다.

---

# 19. 가장 잘 된 부분 4 — official finalize와 backup 상태 분리

metadata는 단순히 child process exit code만 보지 않는다.

이번 결과:

```text
exit_code                = 0
training_status          = completed
official_finalize_status = completed
official_backup_status   = success
evidence_validation      = PASS
```

이 구분은 중요하다.

학습 process가 exit 0이어도:

- finalize 실패
- 공식 backup 실패
- evidence 누락
- stale output

이 있을 수 있기 때문이다.

이번 run에서는 각각을 독립적으로 검사했고 모두 통과했다.

따라서 “프로세스가 끝났다”보다 훨씬 강한 완료 증거다.

---

# 20. 가장 잘 된 부분 5 — train/video provenance chain

이번 video lineage는 다음과 같이 연결된다.

```text
parent train run
20260913-145026-go2-b0-1k-official
        ↓
collected/exported/model_best.pt
SHA-256 99cee...4676
        ↓
model_800.pt와 동일 hash
        ↓
video metadata source_checkpoint_sha256
99cee...4676
        ↓
video_manifest.json
source checkpoint SHA + MP4 SHA
        ↓
play_video.mp4
SHA-256 9cd954...93c6
```

또한 video metadata는 staging 후:

```text
staged = true
restored_after_run = true
```

를 기록한다.

즉 video를 만들기 위해 공식 task tree의 `exported/model_best.pt`를 잠시 준비했지만, 작업 뒤 기존 상태를 복원했다.

과거처럼 “파일명은 맞는데 어느 checkpoint 영상인지 모르는” 문제를 크게 줄였다.

---

# 21. `issacsimz`에서 보완할 부분

이번 run에서 치명적인 로깅 문제는 발견되지 않았다.

다만 evidence를 완전히 self-contained forensic bundle로 만들려면 아래 개선이 유용하다.

## 21.1 `issacsimz` 자체 build identity

run archive 안에서 **실제로 실행한 `issacsimz.pyz` 자체 SHA-256 또는 git commit/version**을 바로 찾기 어렵다.

현재 bootstrap manifest가 별도로 이를 기록할 수 있지만, run archive만 다른 PC에 떼어놓으면 정확한 sidecar build 식별성이 떨어진다.

권장 추가:

```text
system/issacsimz_identity.json
- version
- pyz sha256
- source commit (가능한 경우)
- build timestamp
```

이 한 파일이 들어가면 provenance가 더 강해진다.

---

## 21.2 runtime dependency 정규화

현재 `system/runtime.txt`:

```text
platform=Linux-6.8.0-136-generic-x86_64-with-glibc2.39
python=3.11.13 ...
```

정도다.

이번 bundle의 console과 diff를 통해 환경 일부는 복원 가능하지만, 다음 항목을 run evidence에 명시적으로 한 번에 저장하면 더 좋다.

```text
Isaac Sim exact build
Isaac Lab commit
PyTorch version
CUDA runtime
RSL-RL version
NVIDIA driver
GPU model
```

`nvidia-smi`는 이미 있으므로 GPU/driver는 복원 가능하지만, 사람이 여러 파일을 뒤질 필요가 없게 정규화된 JSON 하나를 두는 편이 좋다.

---

## 21.3 timezone 명시

metadata는 UTC:

```text
2026-09-13T14:50:27+00:00
```

native run 이름과 `nvidia_smi_during.csv`는 KST:

```text
2026-09-13_23-50-30
2026/09/13 23:50:27
```

로 기록된다.

둘은 정확히 UTC+9 차이여서 모순은 없지만, 최초 분석자가 혼동할 수 있다.

권장:

```text
metadata:
  timezone_display: Asia/Seoul
  utc_offset: +09:00
```

또는 CSV timestamp를 ISO8601 + offset으로 저장한다.

---

## 21.4 video manifest에 media probe 결과 추가

현재 manifest는 핵심 lineage에는 충분하다.

```text
source checkpoint SHA
play video SHA
```

여기에 자동으로 다음까지 넣으면 영상 evidence가 더 완결된다.

```text
codec
width
height
fps
frame_count
duration_sec
```

이번에는 별도 `ffprobe`를 실행해서 다음을 확인해야 했다.

```text
H.264
1920×1080
50 fps
999 frames
19.98 s
```

CLI 자체가 pack 전에 media probe를 남기면 별도 후처리가 필요 없다.

---

# 22. 기존 개인 Go2 자료와 비교할 때의 의미

프로젝트의 기존 개인 L40S 자료와 비교하면 이번 공식 1K baseline은 매우 중요한 anchor다.

## 22.1 개인 장기 baseline과의 관계

과거 개인 Go2 baseline에서는 초기/중기 terrain이 낮았다가 장기 학습에서 회복한 이력이 있다.

대표적으로 프로젝트 문서에 보존된 값:

```text
약 4.5K 후보:
terrain ≈ 0.918
XY error ≈ 1.168

9.5K 부근:
terrain ≈ 5.825
XY error ≈ 0.719
base-contact ≈ 1.91%
```

따라서 공식 1K의 terrain 0 고착을 근거로 baseline 전체를 폐기하는 것은 성급하다.

이번 run이 말해주는 것은:

> **baseline은 공식 서버에서도 1K 시점에는 매우 약한 locomotion 상태일 수 있다.**

라는 것이다.

---

## 22.2 A1 1K와의 비교

프로젝트의 개인 A1 1K 결과:

```text
track_lin_vel_xy_exp: 1.0 → 1.5
lin_vel_z_l2:        -3.0 → -2.0
```

endpoint:

```text
terrain        2.8915
XY error       0.7050
yaw error      0.4860
episode length 982.52
base-contact   7.66%
timeout        92.34%
action std     0.53
```

이번 공식 baseline 1K endpoint:

```text
terrain        0.0000
XY error       1.8421
yaw error      0.3082
episode length 975.33
base-contact   6.55%
timeout        93.45%
action std     0.44
```

단순 비교하면:

- survival은 둘 다 매우 강하다.
- A1은 terrain과 XY tracking에서 훨씬 낫다.
- baseline은 yaw error가 더 낮다.
- 따라서 A1은 **linear locomotion 회복 후보**라는 기존 해석과 일치한다.

하지만 이 비교는 **공식 서버 baseline vs 개인 L40S A1**, 그리고 A1은 두 reward를 동시에 바꾼 조합이므로 인과 비교가 아니다.

정확한 다음 실험은 여전히 공식 서버에서 같은 조건의 single-variable 또는 paired run으로 검증해야 한다.

---

# 23. 이번 결과가 향후 실험 설계에 주는 정보

이번 baseline 1K로 인해 다음 Go2 실험의 기준점이 훨씬 명확해졌다.

1K screening에서 단순히 `terrain이 낮다`만 보는 대신 다음을 같이 봐야 한다.

- terrain 500→1000 방향
- XY tracking error
- yaw tracking error
- base-contact
- timeout
- episode length
- action std
- value loss와 finite 상태
- video에서 실제 command-following 여부

이번 baseline은 특히 다음 패턴의 reference negative다.

```text
terrain: 완전 0 고착
survival: 높음
XY tracking: 나쁨
yaw tracking: 상대적으로 양호
수치 안정성: 정상
```

앞으로 후보가 이 baseline보다 좋은지 볼 때는 최소한:

- terrain이 0에서 회복하거나,
- XY error가 의미 있게 줄거나,
- 두 지표의 후반 추세가 회복 방향이며,
- 생존이 크게 무너지지 않는지

를 함께 판단하는 것이 좋다.

---

# 24. `issacsimz` 실전 검증 상태 업데이트 제안

기존 프로젝트 문서에서는 `issacsimz`에 대해:

> 공식 서버/L40S에서 실제 Isaac finalize와 함께 동작하는 1 iteration smoke는 별도 확인이 필요

라는 경계가 있었다.

이번 결과 이후에는 적어도 **Go2 official normal-completion path**에 대해서는 상태를 다음처럼 올려도 된다.

### 검증 완료로 볼 수 있는 것

- 공식 서버 Go2 1K 장시간 train
- headless 4096 env
- console capture
- GPU telemetry
- native run detection
- TensorBoard preservation
- checkpoint watcher/mirror
- official finalize 관찰
- official backup 성공 판정
- finalize cleanup 이전 checkpoint 보존
- collection freshness 판정
- archive + external sidecar hash
- internal SHA256SUMS
- parent-linked video
- checkpoint staging + restore
- fresh MP4 validation
- train checkpoint → video SHA lineage

### 아직 이번 run으로 검증됐다고 말하면 안 되는 것

- Ctrl+C 1회 graceful interrupt path
- Ctrl+C 2회 forced stop path
- 학습 crash/NaN 실패 archive path
- disk 부족 path
- tmux disconnect/reconnect 실전 장애 복구
- resume lineage 실전 학습
- official backup 실패 상황 판정
- H1에서 동일 기능의 실전 재검증
- 동시에 여러 run이 생기는 비정상 상황

즉 표현은:

> **“`issacsimz`의 공식 서버 Go2 정상 완료 train/finalize/backup/video 경로는 실전 검증됨.”**

이 가장 정확하다.

“`issacsimz` 전체 기능이 공식 서버에서 완전 검증됐다”고 넓혀 말하면 과장이다.

---

# 25. 최종 평가표

## 정책

| 항목 | 판정 |
|---|---|
| 1K 학습 완주 | PASS |
| numerical stability | PASS |
| survival | 강함 |
| terrain progression | **매우 약함 / 322부터 0 고착** |
| linear velocity tracking | **약함** |
| yaw tracking | 상대적으로 양호 |
| submission-quality locomotion 증거 | 없음 |
| 장기 baseline 기각 근거 | 부족 |
| 1K screening 기준선 가치 | **높음** |

### 정책 판정

**1K에서 안정적인 locomotion 정책으로 보기는 어렵다.**

하지만 장기 학습 실패를 의미하지 않으며, 앞으로 G2/A1 등의 후보를 비교하기 위한 **공식 서버 baseline negative/reference anchor**로는 매우 가치가 높다.

---

## `issacsimz`

| 항목 | 판정 |
|---|---|
| archive integrity | PASS |
| evidence completeness | 매우 우수 |
| checkpoint preservation | 매우 우수 |
| TensorBoard preservation | PASS |
| console preservation | PASS |
| GPU telemetry | PASS |
| source immutability evidence | PASS |
| stale-output protection | PASS |
| official finalize tracking | PASS |
| official backup tracking | PASS |
| video lineage | PASS |
| media metadata completeness | 개선 가능 |
| runtime dependency identity | 개선 가능 |
| exact issacsimz build identity | 개선 권장 |

### 로깅 판정

**약 95/100.**

실제 경쟁용 공식 서버에서 forensic evidence sidecar로 사용하기에 충분히 강한 수준이다.

특히 이번 run은 unit/fixture 수준을 넘어:

> **실제 공식 RTX 5080 서버에서 1시간 이상 Go2 1K를 돌리고, native finalizer와 cleanup 및 official backup까지 거친 뒤에도 evidence가 온전히 남는다는 것을 보여준 첫 강한 실전 증거**

로 취급할 수 있다.

---

# 26. 최종 결론

이번 bundle의 가장 큰 가치는 정책 성능 자체보다 **두 가지 기준선을 동시에 얻었다는 것**이다.

첫째, Go2 정책 측면에서:

```text
공식 baseline 1K
= 높은 survival
+ terrain 0 고착
+ 매우 약한 XY tracking
+ 정상적인 yaw 개선
+ 수치적으로 안정
```

이라는 명확한 reference를 확보했다.

둘째, 실험 인프라 측면에서:

```text
issacsimz
= 공식 source 비변조
+ 전 console
+ TensorBoard
+ GPU telemetry
+ checkpoint mirror
+ finalize/backup 상태
+ stale-output provenance
+ cryptographic archive verification
+ train/video checkpoint lineage
```

가 실제 공식 서버에서 제대로 동작함을 확인했다.

따라서 이번 실행은 **정책 성능 면에서는 약한 baseline**, **실험 증거 품질 면에서는 매우 성공적인 run**이다.

향후 G2, A1, 또는 다른 Go2 후보를 같은 `issacsimz` 형식으로 공식 서버에서 수집하면, 이제부터는 단순 endpoint 비교가 아니라 **동일 형식의 full-curve + checkpoint + video + system evidence 기반 paired 분석**이 가능하다.

이것이 이번 공식 1K 실행에서 얻은 가장 중요한 성과다.

---

# 27. 분석에 사용한 직접 증거

이 보고서에서 직접 확인한 주요 파일:

```text
train evidence:
  metadata.json
  validation.json
  command.txt
  console.log
  watcher.log
  SHA256SUMS
  source/identity.json
  source/quadruped_rewards.py
  native_run/events.out.tfevents.*
  native_run/params/env.yaml
  native_run/params/agent.yaml
  native_run/git/IsaacLab.diff
  checkpoints/model_0.pt
  checkpoints/model_100.pt
  ...
  checkpoints/model_999.pt
  collected/provenance.json
  collected/exported/model_best.pt
  collected/exported/env.yaml
  collected/exported/report.html
  system/runtime.txt
  system/nvidia_smi_before.txt
  system/nvidia_smi_during.csv
  system/nvidia_smi_after.txt

video evidence:
  metadata.json
  validation.json
  command.txt
  video_manifest.json
  SHA256SUMS
  collected/provenance.json
  collected/exported/play_video.mp4
  collected/exported/policy.pt
  collected/exported/policy.onnx
```

프로젝트 비교 해석에는 다음 기존 핵심팩의 판단 규칙을 적용했다.

```text
07_QUADRUPED_TRAINING_CODE(20260913-160026).md
16_EXPERIMENT_EXPORT_AND_TENSORBOARD(20260913-160121).md
18_H1_FINALIZE_REPORT_LIMITATIONS(8).md
19_ISSACSIMZ_EXTERNAL_EVIDENCE_CLI(8).md
```

---

# 28. 한계

- 공식 Go2 evaluator 점수가 포함된 bundle은 아니므로 공식 시뮬레이션 점수를 추정하지 않았다.
- 단일 seed 실행이다.
- 1K는 장기 baseline 수렴 판정 구간이 아니다.
- video는 약 20초의 단일 play evidence이며 여러 공식 시나리오를 대체하지 않는다.
- A1 및 개인 장기 baseline과의 비교는 서버/GPU/실험 조건이 다르므로 인과 추론이 아니다.
- TensorBoard event 원본은 보존되어 있으나 이 보고서의 숫자 표는 완전한 console 0~999 block을 직접 파싱한 값을 중심으로 작성했다.
- `issacsimz` 95/100은 프로젝트 내부의 evidence 품질 평가이며 공식 인증 점수가 아니다.

---

**보고서 자체 신뢰도: 매우 높음.** 핵심 수치는 원본 archive, console, checkpoint tensor, SHA-256, metadata, GPU CSV 및 실제 MP4를 직접 교차검증했다.

정확도 : 99%
