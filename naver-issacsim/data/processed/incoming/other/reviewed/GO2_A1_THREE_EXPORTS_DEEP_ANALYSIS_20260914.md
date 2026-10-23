# Go2 A1 공식 서버 3개 Export 심층 분석

- 분석일: 2026-09-14
- 대상: 사용자가 업로드한 3개 tar.gz
- 범위: archive 무결성, provenance, checkpoint/policy 연결, 학습 로그, reward/env 일치, 영상 파일 구조
- 제외: 영상의 실제 보행 행동 판정(프레임 기반 시각 분석은 수행하지 않음)

---

## 1. 결론 요약

세 파일은 서로 독립적인 세 실험이 아니라, **하나의 A1 공식 fresh run + 그 run의 4800 checkpoint에서 이어진 recovery run + recovery handoff의 전/후 버전**이다.

가장 중요한 판정은 다음과 같다.

1. **원본 A1 공식 run은 0→4837에서 Ctrl+C로 중단되었지만, 0~4800 checkpoint 49개와 전체 console/TensorBoard/source/config evidence가 정상 보존되어 있다.**
2. **recovery는 원본 `model_4800.pt` SHA-256 `ea93f9...aba65`를 정확히 source로 사용했고, 4800→4999까지 200 iteration을 정상 완료했다.**
3. recovery evidence는 `status=completed`, `official_finalize_status=completed`, `official_backup_status=success`, `evidence_validation=PASS`다.
4. recovery의 실제 선택 checkpoint는 **`model_4900.pt`**이며, outer `model_best.pt`와 byte-identical하다.
5. 최종 bundle의 **`policy.pt`는 `model_4900.pt`의 deterministic actor와 8개 MLP tensor가 전부 exact-match**한다. 즉 **최종 recovery 제출 후보의 policy/model_best 연결은 정상**이다.
6. 반대로, 세 업로드 안에는 **4800 전용 `policy.pt`는 없다.** `fallback_model_4800.pt`는 있으므로 나중에 다시 export 가능하다.
7. 최종 recovery bundle에는 Go2 6-terrain 영상이 모두 존재하며, 전부 H.264 / 1920×1080 / 50 fps / 999 frames / 19.98 s로 정상 디코딩된다.
8. 세 번째(작은 recovery bundle)는 첫 번째(최종 recovery bundle)의 **완전한 이전 단계 subset**이다. 핵심 공통 파일들의 SHA가 모두 동일하다.
9. 현재 제출 후보로는 **recovery `model_4900 → policy.pt`가 가장 완성도가 높다.** 다만 4900의 terrain metric은 resume 뒤 curriculum reset 상태이므로 원본 4800의 terrain 5.7367과 직접 비교하면 안 된다.
10. 공식 제출 요구 기준으로 보면 `policy.pt + env.yaml`은 준비되어 있으나, **기술 개선 리포트는 이 세 bundle 안에는 별도로 없다** (`report.html`은 진단용).

---

## 2. 업로드 3개 파일의 역할

| 구분 | 파일 | 크기 | 역할 |
|---|---|---:|---|
| A | `20260914-132725-...-download (1).tar(1).gz` | 79,246,903 B | **최종 recovery handoff**. policy, env, model_best, fallback 4800, lineage, 영상 6개 포함 |
| B | `20260914-084321-...-5k-official-download.tar(1).gz` | 315,276,597 B | **원본 interrupted fresh run 전체 evidence** |
| C | `20260914-132725-...-download.tar(1).gz` | 32,098,775 B | recovery의 **초기/basic handoff**. A의 이전 버전 |

외부 archive SHA-256:

```text
A  265c3c5533ac2be5037cab0ea668b07990ccc8025a816b22178b7df7bd7257c5
B  d2919617dbb2121652fb0c38fc12efe8d874280d55adf4416b39c7e5adfe30ef
C  cb6a31a93afecd66492a172861a76af53ced41723d9c4628f48c2cfec2847f14
```

### A와 C의 관계

A와 C의 공통 파일 5개는 모두 byte-identical이다.

- nested recovery evidence tar.gz
- nested tar.gz sidecar
- `env.yaml`
- `model_best.pt`
- `report.html`

A가 C에 추가한 것은 다음이다.

- `RECOVERY_LINEAGE.txt`
- `fallback_model_4800.pt`
- fallback SHA sidecar
- `policy.pt`
- policy SHA sidecar
- 6개 terrain 영상

따라서 **A를 보존하면 C는 내용상 중복**이다. 단, 원본 보존 원칙상 저장공간이 충분하면 C도 그대로 보관해도 된다.

---

## 3. Archive 무결성

### 원본 interrupted evidence

nested archive:

```text
20260914-084321-go2-a1-tracklin150-lvz-m2-5k-official_INTERRUPTED.tar.gz
SHA-256:
143dc6162ac2666e8902203e80d88ebf219c1a20fb0f85e1f3090a562cc643d5
```

내부 `SHA256SUMS` 66개 항목을 직접 재계산한 결과:

```text
PASS 66 / 66
FAIL 0
MISSING 0
```

### recovery evidence

nested archive:

```text
20260914-132725-go2-a1-tracklin150-lvz-m2-resume4800-to5k-offici.tar.gz
SHA-256:
868361827a31eae25d98f99a4e48948f7bf659e29c926bc78c83c4c814811d9c
```

내부 `SHA256SUMS` 24개 항목:

```text
PASS 24 / 24
FAIL 0
MISSING 0
```

### 최종 handoff의 핵심 sidecar

```text
policy.pt
22957506fefe1cde249548705fef30147fe149e1086c926ff447ff001c2cc277
→ sidecar 일치

fallback_model_4800.pt
ea93f9b5b04d91a91d1cdb97c6d328978017991e0602745f9269c7190bfaba65
→ sidecar 일치

nested recovery archive
868361827a31eae25d98f99a4e48948f7bf659e29c926bc78c83c4c814811d9c
→ sidecar 일치
```

---

## 4. 원본 A1 fresh run 분석

Run ID:

```text
20260914-084321-go2-a1-tracklin150-lvz-m2-5k-official
```

실행:

```text
5000 requested iterations
4096 envs
seed 42
fresh run
```

실제 상태:

```text
status                    = interrupted
training_status           = interrupted
exit_code                 = 1
official_finalize_status  = not_started
official_backup_status    = unknown
evidence_validation       = FAIL
launch_error              = BrokenPipeError: [Errno 32] Broken pipe
```

여기서 validation FAIL은 **정책 tensor가 깨졌다는 의미가 아니라**, Ctrl+C 때문에 official finalize/backup chain이 끝나지 않았기 때문이다.

### 보존 상태

- console 전체: 0~4837
- TensorBoard event 존재
- checkpoint: `model_0.pt` ~ `model_4800.pt`, 총 49개
- source identity
- reward source
- env/agent yaml
- GPU/system 기록
- watcher log
- validation/provenance

49개 checkpoint의 actor+critic tensor를 직접 검사한 결과:

```text
NaN = 0
Inf = 0
```

즉 **중단 시점까지 저장된 checkpoint 자체는 모두 finite**다.

### A1 reward 설정

원본 env.yaml:

```text
track_lin_vel_xy_exp =  1.5
track_ang_vel_z_exp  =  0.75
lin_vel_z_l2         = -2.0
ang_vel_xy_l2        = -0.08
action_rate_l2       = -0.01
feet_air_time        =  0.01
```

A1 핵심 변경은 baseline 대비:

```text
track_lin_vel_xy_exp : 1.0  → 1.5
lin_vel_z_l2         : -3.0 → -2.0
```

### 원본 iter 4800

| 지표 | iter 4800 |
|---|---:|
| Mean reward | 20.14 |
| Terrain | 5.7367 |
| XY error | 0.5017 |
| Yaw error | 0.4278 |
| Episode length | 968.01 |
| Timeout | 91.89% |
| Base contact | 8.11% |
| Action std | 0.66 |
| Value loss | 0.0259 |
| Track linear reward | 1.1642 |
| Track yaw reward | 0.5762 |

### 원본 후반 안정 구간

마지막 200 iteration 평균:

```text
reward          19.1343
terrain          5.6809
XY error         0.5907
yaw error        0.4304
episode length 964.4572
base contact      7.34%
timeout          92.67%
action std        0.6550
value loss        0.5413
```

마지막 500 iteration 평균:

```text
reward          18.2534
terrain          5.6409
XY error         0.6208
yaw error        0.4374
episode length 962.9586
base contact      7.69%
timeout          92.31%
action std        0.6663
```

### critic 불안정성

원본 5K trajectory는 완전히 매끈하지 않았다.

주요 value-loss spike:

```text
iter 3747 : 283.8869
iter 4415 : 265.3461
iter 1121 : 171.8605
iter 1369 : 133.0419
iter 3748 : 132.8495
```

가장 큰 reward 급락:

```text
iter 3748 : reward -105.28
```

그럼에도 이후 terrain, episode length, timeout, reward가 다시 회복했고 checkpoint tensor에는 NaN/Inf가 없다.

따라서 판정은:

> **persistent divergence는 아니지만, 장기 학습 중 recurrent critic instability가 분명히 존재했다.**

단순히 “value loss가 한번 튀었지만 문제 없음”보다 강한 표현이 맞다. 특히 3747/4415처럼 200+ spike가 반복됐다.

---

## 5. 원본 run의 숨은 `model_4300` 후보

recovery 시작 전 provenance에는 이전 exported 파일로 다음이 기록돼 있다.

```text
model_best_20260914174326.pt
SHA-256:
82efb1a59bfad74c5b03b7584fe7cf27865dcd0603550f11340c4134c6a802c8
```

원본 interrupted archive의 49개 checkpoint를 전부 hash 대조한 결과 이 값은 정확히:

```text
model_4300.pt
```

와 일치한다.

또한 원본 console의 최고 mean reward는:

```text
21.85 @ iter 4284
```

이므로, 저장 간격 100 기준으로 4300이 당시 자동 best 후보가 된 것은 논리적으로 일치한다.

iter 4300:

```text
reward          20.65
terrain          5.5469
XY error         0.5636
yaw error        0.3999
episode length 951.37
base contact      7.86%
timeout          92.14%
std               0.64
value loss        0.1777
```

즉 원본 fresh trajectory에서 자동선택된 checkpoint 계열은 사실 4800이 아니라 **4300**이었다는 forensic evidence가 있다.

다만 현재 사용자 비교 기준은 4800 fallback vs recovery 4900으로 유지해도 된다. 4300은 별도 후보로 보존 가능하다는 의미다.

---

## 6. Recovery run 분석

Run ID:

```text
20260914-132725-go2-a1-tracklin150-lvz-m2-resume4800-to5k-offici
```

실행:

```text
--max_iterations 200
--num_envs 4096
--resume
--load_run a1-recovery-4800-source
--checkpoint model_4800.pt
```

source checkpoint:

```text
/root lineage source SHA-256
ea93f9b5b04d91a91d1cdb97c6d328978017991e0602745f9269c7190bfaba65
```

이 hash는 원본 fresh run의 `model_4800.pt`와 정확히 일치한다.

상태:

```text
exit_code                 = 0
status                    = completed
training_status           = completed
official_finalize_status  = completed
official_backup_status    = success
evidence_validation       = PASS
```

validation 9개 항목 모두 PASS다.

### 코드/config 연속성

원본과 recovery의 `source/identity.json` hash가 완전히 동일하며:

```text
changed_during_run = false
```

주요 source file hash도 동일하다.

- train.py
- play.py
- quadruped_rewards.py
- env_cfg.py
- agent_cfg.py
- finalize source

원본과 recovery의 env.yaml 차이는 실제로 **`log_dir` 한 줄뿐**이다.

따라서 reward/environment 설정 drift는 확인되지 않았다.

agent.yaml 차이는 예상된 resume control뿐이다.

```text
max_iterations : 5000 → 200
resume         : false → true
load_run       : .* → a1-recovery-4800-source
checkpoint     : model_.*.pt → model_4800.pt
```

---

## 7. Recovery curriculum reset

recovery 첫 iteration:

```text
iter 4800
terrain       3.5275
reward        0.07
episode       11.87
timeout       1.15%
```

이 값은 원본 iter 4800의 terrain 5.7367과 이어지지 않는다.

즉 resume에서 network/optimizer는 이어졌지만, environment-side curriculum/episode statistics는 새 run으로 초기화됐다.

recovery terrain:

```text
4813  3.3171  (저점)
4872  4.1688
4900  4.6251
4999  5.7940
```

따라서:

> **4800 vs 4900의 terrain 또는 raw reward는 같은 난이도 조건의 정면 비교가 아니다.**

4900에서 reward가 높아진 일부 이유는 당시 curriculum이 아직 원본 4800보다 쉬웠기 때문일 수 있다.

반대로 recovery가 4999에서 terrain 5.794까지 다시 올라갔다는 점은 “resume 후 curriculum 재적응 실패”는 아니었다는 강한 증거다.

---

## 8. Recovery의 성능 변화

최고 logged reward:

```text
26.39 @ iter 4872
```

하지만 exact checkpoint는 100 iteration 간격으로만 저장되어 있다.

보존 checkpoint:

```text
model_4800.pt
model_4900.pt
```

자동 선택 결과:

```text
model_best.pt == model_4900.pt
SHA-256:
250e430cbb74f837af15384c145e865f7c8d8155fc65a7fe8b21dda1c27514cd
```

### iter 4900

| 지표 | recovery 4900 |
|---|---:|
| Mean reward | 24.40 |
| Terrain | 4.6251 |
| XY error | 0.5489 |
| Yaw error | 0.3741 |
| Episode length | 982.37 |
| Timeout | 96.18% |
| Base contact | 3.82% |
| Action std | 0.57 |
| Value loss | 0.0201 |
| Track linear reward | 1.1910 |
| Track yaw reward | 0.6170 |

### iter 4999

```text
reward          21.08
terrain          5.7940
XY error         0.5697
yaw error        0.4575
episode length 990.14
base contact      6.57%
timeout          93.43%
std               0.62
value loss        0.0236
```

### 구간 평균

```text
4870–4919
reward          24.4456
terrain          4.5338
XY error         0.4410
yaw error        0.3691
episode length 977.6818
base contact      3.79%
timeout          96.21%
std               0.5674
value loss        0.0695
```

```text
4970–4999
reward          21.5807
terrain          5.6778
XY error         0.5323
yaw error        0.4107
episode length 968.0503
base contact      6.42%
timeout          93.58%
std               0.6123
value loss        0.3160
```

해석:

- 4870~4919가 가장 “깔끔한” 성능 구간이다.
- 이후 terrain이 상승하면서 reward/추종 지표가 다소 악화되고 base-contact/std가 다시 오른다.
- 이는 단순 후반 붕괴라기보다 **난이도 재상승과 함께 비용이 증가한 형태**에 가깝다.
- 4999에서도 terrain 5.794, episode 990 수준이므로 policy가 무너진 것은 아니다.

---

## 9. Recovery critic 안정성

recovery 최대 value loss:

```text
5.3492 @ iter 4941
```

원본의 max 283.8869보다 훨씬 작다.

recovery의 특이점:

```text
iter 4942
reward      -3.60
value loss   1.6847
terrain      5.2562
base-contact 4.73%
timeout     95.27%
```

한 번의 reward 급락은 있었지만 바로 회복한다.

따라서 recovery 200 iteration은:

> **원본 장기 trajectory보다 critic 쪽 수치 불안정성이 훨씬 작았으며, 지속적 발산 징후는 없다.**

---

## 10. `policy.pt` ↔ `model_best.pt` forensic 검증

최종 handoff:

```text
policy.pt SHA-256
22957506fefe1cde249548705fef30147fe149e1086c926ff447ff001c2cc277
```

TorchScript 로드 결과:

```text
input  : 235-dim observation
output : 12-dim action
deterministic actor MLP:
235 → 512 → 256 → 128 → 12
```

`policy.pt`의 8개 MLP parameter tensor를 다음 checkpoint들과 직접 비교했다.

| checkpoint | policy MLP exact-match |
|---|---|
| original model_4800 | NO |
| recovery model_4800 | NO |
| recovery model_4900 | **YES, 8/8 exact** |
| outer model_best.pt | **YES, 8/8 exact** |
| fallback model_4800 | NO |

즉:

> **최종 `policy.pt`는 recovery `model_4900/model_best`에서 export된 정책이다.**

이것은 제출 후보 관점에서 좋은 결과다. `policy.pt`와 `model_best.pt`가 뒤섞인 stale artifact가 아니다.

### 중요한 정정: 4800 policy는 아직 없음

사용자가 이후 원본 model_4800을 직접 play했을 때 console에는 checkpoint loading이 성공했지만, 업로드된 최종 bundle의 `policy.pt`는 여전히 recovery 4900과 exact-match한다.

따라서 이 세 파일만 기준으로 하면:

```text
4800 checkpoint     있음
4800 policy.pt      없음
4900 model_best     있음
4900 policy.pt      있음
```

원본 4800 policy가 필요하면 나중에 `fallback_model_4800.pt`로 재-export해야 한다.

---

## 11. Recovery archive 안의 `model_4800.pt` 주의사항

recovery nested evidence에 있는:

```text
checkpoints/model_4800.pt
SHA:
1bfeb75d36f0306afa92ab1360a4d8aea64ef9388098f60807bf50182e5e30b4
```

는 원본 source checkpoint:

```text
ea93f9b5b04d91a91d1cdb97c6d328978017991e0602745f9269c7190bfaba65
```

와 다르다.

두 checkpoint 모두 metadata `iter=4800`이지만 actor/critic tensor가 약간 변해 있다.

이는 resume 시작 뒤 iteration 4800 update/save가 다시 발생했기 때문으로 해석된다.

따라서 나중에 “원본 4800”을 재현할 때는 반드시:

```text
fallback_model_4800.pt
SHA ea93f9...
```

를 써야 한다.

최종 bundle이 이 원본 fallback을 따로 보존한 것은 매우 잘 된 구성이다.

---

## 12. 4800 vs recovery model_best 4900

동일한 training-log snapshot끼리 수치 비교하면:

| 지표 | 원본 4800 | recovery 4900 | 변화 |
|---|---:|---:|---:|
| Reward | 20.14 | **24.40** | +4.26 |
| Terrain | **5.7367** | 4.6251 | 직접 비교 금지 |
| XY error | **0.5017** | 0.5489 | +0.0472 (4900 불리) |
| Yaw error | 0.4278 | **0.3741** | -0.0537 |
| Episode | 968.01 | **982.37** | +14.36 |
| Base contact | 8.11% | **3.82%** | -4.29%p |
| Timeout | 91.89% | **96.18%** | +4.29%p |
| Action std | 0.66 | **0.57** | -0.09 |
| Value loss | 0.0259 | **0.0201** | -0.0058 |
| Track lin reward | 1.1642 | **1.1910** | +0.0268 |
| Track yaw reward | 0.5762 | **0.6170** | +0.0408 |

### 해석

4900의 강점:

- base-contact 약 53% 상대 감소
- timeout 증가
- yaw tracking 개선
- episode length 증가
- action std 감소
- 낮은 instantaneous value loss
- 더 높은 track rewards

4800의 강점:

- 같은 snapshot 기준 XY error가 더 낮음
- 훨씬 높은 curriculum terrain에서 나온 수치

따라서 “4900이 무조건 압도적으로 우수”라고 숫자만으로 결론 내리면 과장이다.

정확한 표현은:

> **4900은 생존·base-contact·yaw·reward 측면에서 더 매력적인 제출 후보지만, resume curriculum reset 때문에 4800과 raw reward/terrain을 공정하게 정면 비교할 수 없다.**

동일 terrain evaluator 또는 두 checkpoint의 동일 6-terrain video가 있으면 최종 결론이 더 강해진다.

---

## 13. 4800→4900 parameter drift

원본 `model_4800`과 recovery `model_4900`의 deterministic actor weight를 비교했다.

```text
deterministic actor params : 286,604
L2 parameter delta         : 4.97097
original actor L2 norm     : 50.58088
relative L2 drift          : 약 9.83%
mean absolute delta        : 0.006958
max absolute delta         : 0.071932
```

즉 100 saved-iteration 구간에서 policy가 단순 미세복사 수준이 아니라 의미 있게 업데이트됐다.

stochastic distribution std parameter도 감소했다.

원본 4800 action-dim std parameter:

```text
[0.4377, 0.4480, 0.4378, 0.4212, 0.7771, 0.7605,
 0.7135, 0.6864, 0.7803, 0.8097, 0.8463, 0.8447]
```

recovery 4900:

```text
[0.3552, 0.3466, 0.3525, 0.3477, 0.6760, 0.6639,
 0.6085, 0.6105, 0.6806, 0.7183, 0.7314, 0.6922]
```

training log의 mean action std `0.66 → 0.57`과 방향이 일치한다.

---

## 14. 영상 6개 구조 검증

최종 recovery bundle에 존재:

```text
stairs.mp4
inverted_stairs.mp4
boxes.mp4
random_rough.mp4
slope_up_20deg.mp4
slope_down_20deg.mp4
```

모든 파일 공통:

```text
codec     H.264
resolution 1920×1080
fps       50
frames    999
duration  19.98 s
```

파일 크기:

```text
stairs             6,268,378 B
inverted_stairs    4,694,424 B
boxes              6,615,603 B
random_rough       9,818,097 B
slope_up_20deg     6,152,191 B
slope_down_20deg   6,218,109 B
```

Go2 고정 경사 파일명이 ±20° 규칙과 일치한다.

이 분석에서는 **영상 내용의 보행 성공/실패를 시각 판정하지 않았다.**

### 영상 provenance 한계

최종 handoff에는 MP4는 들어 있지만 개별 `video_manifest.json`/각 video evidence archive는 포함되지 않았다.

따라서 **이 handoff 파일 하나만으로는 각 MP4의 source checkpoint SHA를 cryptographically chain-link할 수 없다.**

다만 제출 자체의 핵심은 policy/env이고, 영상은 검증 자료다. canonical video evidence가 별도 보존돼 있다면 이 문제는 없다.

---

## 15. 제출 준비 상태

프로젝트 규정 정리 기준 제출 핵심:

```text
policy.pt
env.yaml
보상 변경 의도/결과 기술 개선 리포트
```

최종 recovery handoff에는:

```text
policy.pt       있음 — model_4900 actor exact-match
env.yaml        있음 — A1 설정 정상
model_best.pt   있음 — model_4900
report.html     있음
fallback 4800   있음
6 videos        있음
lineage         있음
```

### env/policy 정합성

recovery outer `env.yaml`은 recovery native/export env와 byte-identical하다.

원본 env와 recovery env 차이는 `log_dir`뿐이므로 reward config도 동일하다.

따라서:

> **4900 policy + recovery env.yaml 조합은 설정 lineage상 정합하다.**

### 남은 제출 문서

세 archive 내부에는 별도 기술 개선 리포트 파일이 없다.

`report.html`은 자동 진단 자료이므로 공식 제출용 기술 개선 리포트를 대체한다고 단정하면 안 된다.

---

## 16. 최종 후보 판정

### 제출 후보 1 — Recovery model_4900 / policy.pt

현재 가장 완성된 후보.

장점:

- official recovery 완료
- backup success
- evidence PASS
- model_best/checkpoint/policy tensor 연결 검증 완료
- env 정합
- 6 terrain 영상 존재
- source 4800 lineage 명시
- low base-contact / high timeout
- no NaN/Inf

주의:

- curriculum reset 때문에 4800과 raw reward/terrain 공정 비교 불가
- 4900 시점 terrain은 아직 4.625
- 4999까지 가면 terrain은 5.794로 회복하지만 4900 policy와 4999 policy는 다름
- 4800 동일-terrain 영상이 없어 행동 A/B 비교는 미완

### 후보 2 — Original model_4800

장점:

- fresh 0→4800 uninterrupted lineage
- terrain 5.7367의 고난도 단계
- XY error 0.5017
- 원본 checkpoint SHA가 명확하고 fallback으로 보존

주의:

- 4800 전용 `policy.pt`는 현재 세 bundle에 없음
- 6-terrain 4800 영상 없음
- original run 자체는 interrupted / evidence FAIL
- 장기 critic spike가 recurrent

### 후보 3 — Original model_4300

forensic하게 원본 run의 자동 best였던 후보.

장점:

- 원본 fresh trajectory
- 최고 reward region 4284 근처
- exact checkpoint가 원본 archive에 있음

주의:

- 별도 policy/video 없음
- 현재 사용자의 주력 비교 대상이 아님

---

## 17. 보존 우선순위

반드시 보존:

```text
1. 최종 recovery handoff (A)
2. 원본 interrupted full evidence (B)
```

A에는 제출 후보와 fallback이 있고, B에는 전체 fresh trajectory/checkpoints/TensorBoard가 있다.

중복:

```text
3. 초기 recovery handoff (C)
```

C의 핵심 파일은 A와 hash-identical이므로 저장공간이 부족하면 A+B를 남기는 쪽이 정보 보존 측면에서 더 합리적이다.

---

## 18. 최종 판정

### 데이터/증거 무결성
**매우 좋음**

- original 66/66 internal SHA PASS
- recovery 24/24 internal SHA PASS
- source identity 불변
- 49+2 checkpoint 모두 finite
- fallback source hash 명확
- recovery lineage 명확

### 학습 결과
**A1은 실패 가설이 아니다.**

원본은 terrain 5.7까지 올라갔고, recovery도 reset 뒤 5.794까지 재상승했다.

다만 원본 장기 trajectory에는 강한 critic spike가 반복되어 수치적으로 완전히 평온한 run은 아니었다.

### recovery의 가치
**실질적 개선 신호가 있다.**

특히 4870~4919 구간의 낮은 base-contact, 높은 timeout, 낮은 std, yaw 개선은 긍정적이다.

단, curriculum reset을 고려하면 reward 24.4를 원본 20.14와 단순 비율로 “21% 향상”이라고 보고서에 쓰는 것은 피하는 편이 정확하다.

### 현재 제출 정책
**`policy.pt = recovery model_4900`으로 확인됨.**

이것이 이번 분석의 가장 중요한 artifact-level 결론이다.

---

## 19. 한 줄 결론

> **현재 최종 recovery bundle은 4900 `model_best`와 실제 제출 `policy.pt`가 정확히 연결된 정상적인 완성 후보이며, 원본 4800은 fallback checkpoint로 안전하게 보존되어 있다. 원본 전체 evidence까지 남아 있어 재현성과 소명 가능성도 높다. 단, 4800 전용 policy/video와 기술 개선 리포트는 이 세 파일 안에는 없다.**
