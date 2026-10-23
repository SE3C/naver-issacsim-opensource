# Go2 G5 Official 1K — Lightweight Failure Analysis

작성일: 2026-09-14  
Run ID: `20260914-012909-go2-g5-angvelxy-m012-1k-official`  
분류: **공식 서버 / fresh 1K / strong negative / 3K 연장 안 함**

## 1. 실험 목적

G5는 Go2 official baseline에서 아래 한 항목만 변경한 가설이다.

```text
ang_vel_xy_l2: -0.08 → -0.12
```

목적은 몸통의 좌우/앞뒤 각속도 흔들림 억제를 강화했을 때 생존성과 보행 안정성이 좋아지는지 확인하는 것이었다.

다른 주요 reward는 baseline을 유지했다.

```text
track_lin_vel_xy_exp = 1.0
lin_vel_z_l2         = -3.0
action_rate_l2       = -0.01
feet_air_time        = 0.01
```

## 2. 실행 및 evidence 상태

- 공식 서버
- Go2 / `Quadruped-v0`
- 4096 environments
- 1000 iterations
- fresh start
- seed 42
- 학습 정상 종료
- `exit_code = 0`
- `evidence_validation = PASS`
- `official_finalize_status = completed`
- `official_backup_status = success`
- TensorBoard event 보존
- checkpoint 11개 mirror
- source identity PASS
- archive 내부 33개 파일 검증 PASS
- video evidence PASS
- 학습 후 reward baseline restore 완료

즉, **실험 실행과 증거 수집 파이프라인 자체는 정상**이었다.

## 3. 최종 수치의 핵심

`report.html` 기준:

```text
최고 reward          = 14.41 (iter 972)
terrain level        = 0.00
마지막 10회 낙상률   = 1.5%
마지막 exploration std = 0.394
```

학습 중 확인한 iter 613에서도:

```text
terrain level        = 0.0000
XY velocity error    = 1.7363
time_out             = 97.71%
base_contact         = 2.29%
mean episode length  = 973.45
mean action std      = 0.40
value loss           = 0.0076
```

따라서 학습은 수치적으로 발산한 것이 아니라, **매우 오래 버티지만 locomotion 성능은 좋지 않은 방향으로 수렴**한 것으로 보인다.

## 4. 영상 관찰

`play_video.mp4`를 직접 확인하면 정상적인 사족 보행 안정화로 보기 어렵다.

관찰된 핵심:

- 로봇이 정상적인 네 발 지지 자세를 안정적으로 유지하지 못한다.
- 옆으로 눕거나 거의 뒤집힌 비정상 자세가 반복적으로 보인다.
- 몸통이 바닥에 닿은 상태에서도 다리를 움직이며 episode가 계속되는 장면이 있다.
- 정상적인 지형 진행 또는 명령 추종 보행의 증거로 보기 어렵다.

따라서 낮은 `base_contact` 종료율과 높은 `time_out`을 곧바로 “안정성 향상”으로 해석하면 안 된다.

## 5. 판정

### 최종 판정: **STRONG NEGATIVE**

G5는 “안 넘어지는 안정적인 보행 정책”이 아니라,

> **비정상 자세에서도 termination을 잘 피하면서 episode를 길게 유지하는 생존 편향 정책**

에 더 가깝다.

즉 reward가 의도한 보행 안정성보다 **termination 회피 / 생존 시간 유지 쪽으로 최적화된 failure mode**로 판단한다.

## 6. 의미

이 실험의 가장 중요한 교훈은 다음이다.

```text
낮은 base-contact 종료율
+ 높은 timeout
+ 긴 episode length
≠ 안정적인 locomotion
```

특히 실제 play 영상에서 정상 보행이 확인되지 않으면 생존 지표만으로 정책 품질을 판단하면 안 된다.

## 7. 다음 행동

- G5는 3K 또는 5K로 연장하지 않는다.
- 최종 제출 후보로 사용하지 않는다.
- 향후 비교에서는 terrain progression, XY tracking, termination 지표와 함께 영상을 반드시 확인한다.
- G5는 “생존형 local optimum / termination metric 함정” 사례로만 기록한다.
- 추가 분석 시간과 공식 서버 시간은 A1 등 더 유망한 후보에 우선 배정한다.

## 한 줄 결론

> **G5 official 1K는 실행·evidence 수집에는 성공했지만, 정책 성능 관점에서는 정상 보행 대신 비정상 자세로 생존하는 strong negative failure case다.**
