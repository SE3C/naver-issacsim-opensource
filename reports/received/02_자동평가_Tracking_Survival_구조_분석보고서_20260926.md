> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/incoming/other/reviewed/02_자동평가_Tracking_Survival_구조_분석보고서_20260926.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# 자동평가 Tracking Score · Survival Rate 구조 분석 보고서

- 작성일: 2026-09-26
- 근거: 운영진이 공개한 1차 답변 및 추가 답변
- 목적: H1 정책 학습·평가 결과를 해석하기 위해 자동평가 구조를 확인 사실과 해석으로 분리해 정리
- 주의: 아래에서 `확정 사실`은 운영진 답변으로 직접 확인된 내용, `해석`은 그 사실에서 도출한 분석을 뜻한다.

---

## 1. 핵심 요약

운영진 답변으로 자동평가의 Tracking 및 Survival 집계 구조가 상당 부분 확정되었다.

1. 매 step에서 x 선속도 오차, y 선속도 오차, yaw 각속도 오차를 하나의 벡터 크기로 합친다.
2. 세 성분 사이에 별도의 단위·범위 보정이 없다.
3. 선속도 1 m/s 오차와 yaw 각속도 1 rad/s 오차는 수치상 같은 크기의 오차로 들어간다.
4. 매 episode에서 step 오차를 단순 평균한다.
5. episode별 평균 오차를 다시 동일 가중치로 평균한다.
6. episode 길이는 최종 Tracking 평균의 가중치가 아니다.
7. episode마다 Tracking Score를 먼저 계산한 뒤 평균하는 구조는 아니다.
8. 낙상 episode도 낙상 전까지의 Tracking 오차가 반영된다.
9. 명령 변경 직후의 가속·감속과 episode 시작 직후의 출발 구간도 평가한다.
10. 속도는 robot/body frame 기준이다.
11. Survival은 episode 단위로 집계한다.
12. 한 로봇이 여러 번 넘어지면 그 횟수만큼 실패 episode가 추가된다.
13. 제한시간 도달 episode와 평가 종료 시점에 진행 중인 episode는 생존으로 센다.
14. 명령은 episode 시작 시 생성되고 10초마다 다시 뽑힌다.
15. 모든 제출은 같은 seed를 사용하지만, 정책별 낙상 시점 차이 때문에 이후 command sequence가 완전히 동일하다고 보장되지는 않는다.

현재 가장 큰 미공개 요소는 **최종 평균오차를 실제 Tracking Score 값으로 변환하는 함수**다.

---

## 2. Tracking의 step 단위 오차

### 확정 사실

운영진은 매 step에서 다음 세 오차를 묶어 하나의 벡터 크기를 만든다고 밝혔다.

- x 선속도 오차
- y 선속도 오차
- yaw 각속도 오차

별도의 단위·범위 normalization은 없다.

구조는 다음과 같이 표현할 수 있다.

```text
e_t = sqrt(
    (v_x - v_x_cmd)^2
  + (v_y - v_y_cmd)^2
  + (yaw_rate - yaw_rate_cmd)^2
)
```

추가 답변으로 다음 해석도 직접 확인되었다.

```text
1 m/s의 선속도 오차
=
1 rad/s의 yaw 각속도 오차
```

즉 수치상 같은 크기의 오차 성분으로 취급된다.

### 해석

전진 시나리오에서 목표가 다음과 같다고 하자.

```text
vx_cmd > 0
vy_cmd = 0
yaw_cmd = 0
```

이 경우 정책이 앞으로 잘 움직이더라도 다음 현상은 Tracking을 직접 악화시킨다.

- 좌우 drift
- 좌우 sway
- yaw wobble
- 진행 중 불필요한 회전

따라서 실제 evaluator 관점에서 전진 성능은 단순한 vx 추종만이 아니다.

```text
전진 속도 정확도
+
횡방향 흔들림 억제
+
yaw 흔들림 억제
```

를 동시에 본다.

---

## 3. Episode 내부 Tracking 평균

### 확정 사실

매 step의 오차를 episode 동안 단순 평균한다.

episode i의 길이가 T_i라면 개념적으로:

```text
E_i = (1 / T_i) * sum(e_t)
```

이다.

최댓값을 따로 보거나 큰 순간 오차에 추가적인 비선형 penalty를 주지는 않는다.

### 해석

큰 오차의 영향은 주로 다음 두 요소로 결정된다.

- 오차 크기
- 지속 시간

아주 짧은 순간의 큰 spike보다, 작더라도 오랫동안 유지되는 tracking bias가 전체 평균을 더 크게 악화시킬 수 있다.

정책 비교에서는 다음을 따로 볼 가치가 있다.

- 지속적인 vx 부족 또는 과속
- 지속적인 vy drift
- 지속적인 yaw 편향
- command 변경 후 새로운 목표에 수렴하는 시간
- 낙상 직전 tracking 붕괴

---

## 4. Episode 간 Tracking 집계

### 확정 사실

운영진이 밝힌 최종 집계 순서는 다음과 같다.

```text
step별 3축 오차
→ episode별 평균 오차
→ 모든 episode 평균 오차를 동일 가중치로 평균
→ 하나의 최종 평균오차
→ Tracking 결과 결정
```

즉 episode별로 Tracking Score를 먼저 만든 뒤 그 score들을 평균하는 구조가 아니다.

전체 평균오차는 개념적으로:

```text
E_total = (1 / N) * sum(E_i)
```

로 표현할 수 있다.

여기서 episode 길이와 관계없이 E_i가 하나의 동일 가중치 sample이다.

### 해석

20초 동안 생존한 episode와 2초 만에 종료된 episode가 Tracking 집계에서는 각각 episode 하나다.

예:

```text
Episode A: 20초 생존, 평균오차 0.4
Episode B:  2초 후 낙상, 평균오차 1.2
```

두 episode의 평균은:

```text
(0.4 + 1.2) / 2 = 0.8
```

이다.

짧은 episode라고 해서 step 수가 적다는 이유로 영향력이 자동으로 작아지지 않는다.

---

## 5. 낙상과 Tracking의 관계

### 확정 사실

낙상 episode도 Tracking에서 제외되지 않는다.

넘어지기 전까지의 구간으로 해당 episode의 평균 오차를 계산한다.

운영진은 넘어지는 순간 속도가 크게 어긋나기 때문에 해당 episode의 평균 오차가 나빠지기 쉽다고 설명했다.

### 해석

낙상은 두 경로로 평가 결과에 영향을 줄 수 있다.

```text
낙상
├─ Survival 실패 episode +1
└─ Tracking에서 짧고 오차가 큰 episode 생성 가능
```

따라서 안정성 개선은 단순히 Survival만 보호하는 요소가 아니다.

반대로 안정성을 지나치게 우선하여 움직임이 둔해지고 command response가 느려지면 Tracking이 악화될 수도 있다.

실험에서는 반드시 다음 두 축을 함께 확인해야 한다.

- 얼마나 잘 살아남는가
- 살아 있는 동안 command를 얼마나 정확히 따라가는가

---

## 6. Survival 집계 구조

### 확정 사실

Survival의 평가 단위는 episode다.

다음 episode가 각각 하나씩 누적된다.

- 낙상으로 끝난 episode
- 제한시간까지 진행한 episode
- 전체 평가 종료 시점에 아직 진행 중인 episode

Survival Rate는 다음과 같은 구조다.

```text
Survival Rate
=
생존 episode 수
/
전체 episode 수
```

낙상 episode는 실패다.

제한시간까지 간 episode는 생존이다.

평가 종료 시점에 아직 넘어지지 않고 진행 중인 episode도 생존이다.

### 반복 낙상

한 로봇이 평가 중 여러 번 넘어지면 매 낙상마다 새로운 실패 episode가 하나씩 누적된다.

예:

```text
Robot A
Episode 1 → 낙상
Episode 2 → 낙상
Episode 3 → 낙상
Episode 4 → 평가 종료까지 생존
```

이라면 개념적으로:

```text
실패 3
생존 1
```

을 만든다.

### 해석

따라서 `넘어진 로봇 수`보다 `넘어진 횟수`가 Survival에 더 직접적으로 반영된다.

같은 평가 시간 동안:

```text
정책 A: 늦게 한 번 낙상
정책 B: 짧게 여러 번 반복 낙상
```

이라면 B는 실패 episode를 더 많이 생성할 수 있다.

평균 episode length와 Survival이 밀접하게 연결되는 이유도 여기 있다.

다만 평균 episode length 자체가 Survival Rate와 동일한 지표는 아니다.

---

## 7. Tracking과 Survival의 결합 관계

두 지표는 계산상 별개의 값이지만 정책 행동 수준에서는 강하게 연결된다.

낙상이 증가하면:

```text
실패 episode 증가
→ Survival Rate 감소
```

할 뿐 아니라:

```text
짧은 Tracking episode 증가
→ episode 동일 가중 평균에 직접 반영
```

될 수 있다.

따라서 다음처럼 단순하게 나누면 위험하다.

```text
안정성 reward → Survival만 개선
tracking reward → Tracking만 개선
```

reward 하나의 변경이 두 평가 축 모두에 영향을 줄 수 있다.

---

## 8. Command transition 평가

### 확정 사실

다음 구간도 Tracking에서 제외되지 않는다.

- episode 시작 직후 정지 상태에서 출발
- command 변경 직후 가속
- command 변경 직후 감속
- command 변경 직후 회전 응답

명령은 episode 시작 시 설정되고 이후 10초마다 다시 생성된다.

고정값 시나리오는 다시 뽑아도 같은 값이므로 사실상 일정하다.

범위형 시나리오는 10초마다 범위 안에서 새 명령이 나온다.

### 해석

evaluator는 steady-state tracking만 보는 것이 아니다.

실제 정책의 반응은 다음 전체 과정으로 봐야 한다.

```text
정지
→ 출발
→ 목표 속도 접근
→ 정상 추종
→ command 변경
→ 새로운 목표로 가속/감속/회전
→ 재수렴
```

따라서 자체 영상이나 evaluator에서도 고정 command에서 오래 걷는 모습만 보는 것은 충분하지 않다.

특히 다음을 따로 보는 것이 유용하다.

- command 변경 직후 overshoot
- 수렴 시간
- 감속 시 균형 유지
- yaw 변경 시 lateral drift
- 정지 후 재출발 안정성

---

## 9. 좌표계

### 확정 사실

선속도와 명령은 world frame이 아니라 로봇 몸통 기준 frame을 사용한다.

- 로봇이 바라보는 방향 = x
- 옆 방향 = y

### 해석

회전 중에는 world 기준 위치 변화만 보고 Tracking을 판단하면 안 된다.

정책이 현재 바라보는 방향 기준으로 command를 제대로 수행하는지를 봐야 한다.

특히 yaw와 선속도가 동시에 명령되는 경우 body-frame 해석이 중요하다.

---

## 10. Same seed의 의미

### 확정 사실

모든 제출은 같은 seed로 평가한다.

운영진은 시작 조건이 같고 수백 대 결과를 평균하므로 평가 결과 차이가 적다고 설명했다.

하지만 정책마다 낙상 시점이 달라지면 reset 이후 새로 뽑히는 command가 달라질 수 있으므로 모든 조건이 완전히 같다고 보장할 수는 없다.

### 해석

same seed는 높은 재현성을 제공하지만 다음을 의미하지는 않는다.

```text
모든 정책이
모든 episode에서
정확히 같은 command sequence와
정확히 같은 reset sequence를 경험한다
```

정책 행동 차이가 이후 평가 진행 경로를 갈라놓을 수 있다.

따라서 미세한 점수 차이를 지나치게 강한 인과 증거로 해석하면 안 된다.

---

## 11. H1 reward tuning에 대한 시사점

이번 공개 답변은 H1 reward 실험을 해석할 때 다음 기준을 강화한다.

### 11.1 직진 성능

직진에서는 단순한 vx tracking만 봐서는 부족하다.

함께 봐야 할 항목:

```text
vx error
vy error
yaw error
낙상 빈도
episode length
command transition 직후 흔들림
```

전진 시나리오에서 vy=0, yaw=0이라면 lateral sway와 yaw wobble 자체가 Tracking 손실이다.

### 11.2 yaw 병목

yaw error가 큰 정책은 yaw 시나리오뿐 아니라 command가 0인 다른 시나리오에서도 불필요한 yaw 흔들림이 있다면 Tracking에서 손해를 볼 수 있다.

따라서 yaw 관련 reward 조정은 단순한 회전 명령 추종뿐 아니라 `yaw=0 유지 능력`도 함께 확인해야 한다.

### 11.3 안정성 reward

termination penalty나 자세 안정화 reward로 낙상 횟수가 줄어들면 Survival에는 직접적인 이점이 있을 수 있다.

동시에 반복되는 짧은 실패 episode 감소를 통해 Tracking에도 간접 효과가 생길 수 있다.

그러나 안정성이 높아졌다는 이유만으로 Tracking이 좋아졌다고 단정해서는 안 된다.

반드시 실제 x/y/yaw error를 함께 확인해야 한다.

---

## 12. 정책 비교 시 권장 관찰 항목

동일 evaluator에서 정책을 비교할 때 다음을 함께 보는 것이 적절하다.

```text
1. Survival Rate
2. 전체 episode 수
3. 실패 episode 수
4. 평균 episode length
5. x tracking error
6. y tracking error
7. yaw tracking error
8. 3축 통합 error
9. command 변경 후 수렴 시간
10. 낙상 직전 tracking 붕괴
11. 반복 낙상 여부
12. terrain/scenario별 최악 조건
```

가능하면 단일 평균값만 보지 말고 scenario별로 분리해서 확인하는 것이 좋다.

---

## 13. 아직 미공개인 핵심 요소

### 13.1 평균오차 → Tracking Score 변환식

가장 중요한 미공개 요소다.

현재까지 확정된 것은:

```text
episode별 평균 error
→ episode 동일 가중 평균
→ 하나의 전체 평균 error
```

까지다.

그 뒤 전체 평균 error를 실제 Tracking Score로 바꾸는 함수는 공개되지 않았다.

따라서 다음은 알 수 없다.

- 선형 변환 여부
- exponential 변환 여부
- threshold 존재 여부
- clipping 여부
- score scale
- error가 특정 범위를 넘었을 때의 처리

### 13.2 시나리오별 command 값

명령 생성 방식은 공개되었지만 구체적인 command 값과 범위는 공개되지 않았다.

따라서 evaluator의 정확한 command distribution을 복제했다고 주장하면 안 된다.

---

## 14. 현재 평가 구조 개념도

```text
[command 생성]
episode 시작 + 10초마다 resample
        |
        v
[매 step]
body-frame에서
Δvx, Δvy, Δyaw 계산
        |
        v
sqrt(Δvx² + Δvy² + Δyaw²)
        |
        v
[episode 내부 단순 평균]
E_i
        |
        v
[모든 episode 동일 가중 평균]
E_total
        |
        v
[비공개 변환]
Tracking Score


동시에:


[episode 종료]
        |
        +-- 몸통 바닥 접촉 → 실패 episode
        |
        +-- 제한시간 도달 → 생존 episode
        |
        +-- 평가 종료 시 진행 중 → 생존 episode
        |
        v
Survival Rate
=
생존 episode / 전체 episode
```

---

## 15. 최종 결론

운영진 답변으로 evaluator의 중요한 구조가 다음과 같이 확정되었다.

- 3축 tracking error는 별도 normalization 없이 하나의 Euclidean error로 합쳐진다.
- 1 m/s와 1 rad/s의 오차가 동일한 수치 크기로 취급된다.
- command가 0인 축에서 발생하는 흔들림도 그대로 손실이다.
- step error는 episode별로 평균한다.
- episode별 평균 error는 episode 길이와 관계없이 동일 가중치로 다시 평균한다.
- 낙상 episode도 Tracking에서 제외되지 않는다.
- command transition 구간도 그대로 평가된다.
- body frame 속도를 사용한다.
- Survival은 episode 단위 성공률이다.
- 반복 낙상은 실패 episode를 반복 생성한다.
- same seed라도 정책 행동 차이 때문에 이후 episode 조건의 완전한 일치는 보장되지 않는다.

따라서 H1 정책을 개선할 때는 `생존`, `전진`, `횡방향 안정성`, `yaw 안정성`, `command transition`을 따로 관찰하면서도 최종 evaluator에서는 서로 연결된다는 점을 고려해야 한다.

현재 남은 가장 중요한 미공개 정보는 **전체 평균 Tracking error를 최종 Tracking Score로 변환하는 함수**다. 이 부분이 공개되지 않는 한 최종 점수를 수학적으로 완전히 복제했다고 판단해서는 안 된다.
