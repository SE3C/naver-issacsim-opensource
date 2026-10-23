# H1_H009_R02_VS_H008_CORRECTED_CONTROL_DEEP_ANALYSIS_20260925

## 1. 결론 요약

이번 비교의 A는 **H-009 R02 (`joint_deviation_hip=-0.3`)**, B는 **corrected H-008 unchanged continuation (`joint_deviation_hip=-0.2`)**로 식별했다. 두 학습은 모두 PERSONAL 환경에서 같은 기록상 parent `NCRC_BATCH_h1-corrected-20260925-03_h008_corrected_2998 / model_2998.pt` (metadata SHA-256 `49fdb297...14983`)에서 시작해, seed 42, 4096 env, `--max_iterations 2000`, global iteration `2998→4997`로 완료된 sibling이다. `source/humanoid_rewards.py`와 native `env.yaml`을 직접 diff하면 실행 설정의 의미 있는 reward 차이는 **`joint_deviation_hip -0.2 → -0.3` 한 줄**이다. 두 archive 모두 `exit_code=0`, validation `PASS`, TensorBoard 2,000점, 21개 mirrored checkpoint를 가진다.

핵심 결과는 **H-009가 corrected control보다 yaw tracking error를 일관되게 낮췄지만, terrain·XY tracking·base-contact·episode length에서는 사실상 동률 범위이고, 6지형 영상에서도 H-009만의 명확한 자세/통과 우위를 확인하지 못했다**는 것이다. late-500에서 H-009−control은 terrain `-0.0329`, base-contact `-0.00355`(약 -0.36%p), episode length `+2.55`, XY error `-0.00017`, yaw error `-0.10005`였다. late-300에서도 yaw error 차이는 `-0.09807`로 유지됐지만 terrain `+0.0021`, XY `+0.00008`, base-contact `+0.00094`로 사실상 같다. 즉, 가장 반복적으로 보이는 차이는 yaw 오차 감소다.

다만 이 yaw 개선을 **hip penalty 강화의 일반적 인과 효과**로 확정할 수는 없다. 두 run이 같은 parent·source·학습량·seed로 잘 맞아 이 계보 내부의 단일변수 비교로는 적합하지만, 단일 seed이고 terrain generator/episode realization이 paired evaluator로 고정됐다는 증거가 없으며, training scalar는 독립 반복이 아니다. 또한 `Episode_Reward/joint_deviation_hip` 값이 H-009에서 더 음수인 것은 weight 자체가 -0.3으로 강해졌기 때문에, term 정의/비가중 deviation을 확인하지 않은 채 “실제 hip deviation이 감소했다”고 역산할 수 없다.

**현재 결정:** 실행은 두 run 모두 `COMPLETE`; evidence 연결은 `PASS`; H-009 가설은 **HOLD**. 정책 자체는 6개 native play에서 모두 upright locomotion과 실제 진행을 보였고 샘플 프레임에서 낙상은 확인되지 않았지만, control 대비 결정적인 traversal/자세 우위는 없다. 이번 자료만으로 `PROMOTE`할 근거는 부족하다. 다음 한 번의 최우선 행동은 **새 학습이 아니라, 두 final `model_4997.pt`를 동일 fixed evaluator의 동일 command/terrain/seed/window에 넣어 yaw, XY, 실제 진행, fall/base-contact, hip/torso deviation을 직접 paired 측정하는 것**이다. 이 평가가 late-TB의 yaw 차이를 재현하면 H-009 승격 근거가 생기고, 재현되지 않으면 현재 차이는 training trajectory/episode 구성 효과로 보는 편이 타당하다.

---

## 2. 실제 Run·checkpoint·영상 identity

### 2.1 A: H-009 R02 HIPDEV030 corrected

- 학습 archive: `20260925-095000-h1-h009-r02-hipdev030-corrected-h1-corrected-202.tar.gz`
- mode: `personal`
- task: `Humanoid-v0`
- command 핵심: `--max_iterations 2000 --num_envs 4096 --seed 42 --resume --load_run NCRC_BATCH_h1-corrected-20260925-03_h008_corrected_2998 --checkpoint model_2998.pt --headless`
- parent metadata: `model_2998.pt`, SHA-256 `49fdb297924c861493d377f22b9de135d83c73969ef3d8a2e4a56c9879414983`
- global iteration: `2998→4997`
- 상태: `completed`, `exit_code=0`, validation `PASS`
- checkpoint 수: 21
- final: `model_4997.pt`, SHA-256 `4c13ecd239cbfc35f3661a670516ff1dc3f6651dc07d4e7a3fb88a109bbf67c0`
- automatic `model_best.pt`는 보존 checkpoint hash 대조상 `model_4800.pt`와 동일
- 6지형 video suite manifest source checkpoint: 위 `model_4997.pt` SHA와 정확히 일치
- video suite: `checkpoint-h1-model_4997-4c13ecd239cb`; 6개 MP4 모두 manifest에서 같은 source SHA를 기록

### 2.2 B: corrected H-008 unchanged continuation

- 학습 archive: `20260925-091257-h1-h008-corrected-control-to5k-h1-corrected-2026.tar.gz`
- mode: `personal`
- task/seed/env/resume parent/학습량: A와 동일
- parent metadata: 같은 `model_2998.pt`, 같은 기록상 SHA-256 `49fdb297...14983`
- global iteration: `2998→4997`
- 상태: `completed`, `exit_code=0`, validation `PASS`
- checkpoint 수: 21
- final: `model_4997.pt`, SHA-256 `4349fe5650135c6a77546afc1b165ff60c235bdd83831bd562d618b04c3b5b6d`
- automatic `model_best.pt`는 보존 checkpoint hash 대조상 `model_4900.pt`와 동일
- 6지형 video suite manifest source checkpoint: 위 `model_4997.pt` SHA와 정확히 일치
- video suite: `checkpoint-h1-model_4997-4349fe565013`

### 2.3 provenance 한계

이번 4개 입력에는 parent `model_2998.pt` 자체가 포함되지 않았다. 따라서 두 archive의 metadata가 같은 parent path/SHA를 기록한다는 사실은 직접 확인했지만, **parent 원본 바이트를 이번 입력 안에서 다시 hash해 검증한 것은 아니다**. 반면 각 final checkpoint와 각 video manifest 사이의 SHA 연결은 이번 파일에서 직접 대조했다.

영상은 6개 모두 H.264 1920×1080, 50 fps, 999 frames, 약 19.98초다. manifest에는 terrain label과 source checkpoint SHA는 있으나 **command 값, difficulty, video seed, curriculum level의 상세값은 없다**. 따라서 화면상 진행은 행동 근거로 쓸 수 있지만 command tracking 정답 판정에는 쓰지 않는다.

---

## 3. 실제 설정 차이와 비교 설계

`source/humanoid_rewards.py` 직접 diff:

```diff
-    "joint_deviation_hip": -0.2,
+    "joint_deviation_hip": -0.3,
```

native `params/env.yaml`도 reward weight가 `-0.2 → -0.3`인 것 외에는 실행 log_dir 차이만 확인됐다. `agent.yaml`은 diff가 없었다.

| 조건 | H-009 | corrected control | 비교 해석 |
|---|---:|---:|---|
| parent identity | 같은 기록상 model_2998 SHA | 같음 | 직접 sibling 비교에 적합 |
| reward 차이 | hip -0.3 | hip -0.2 | 단일변수 |
| mode | PERSONAL | PERSONAL | 동일 |
| seed / num_envs | 42 / 4096 | 42 / 4096 | 동일 |
| 추가 학습량 | 2000 iter | 2000 iter | 동일 |
| global range | 2998–4997 | 2998–4997 | 동일 |
| PPO/agent | 동일 `agent.yaml` | 동일 | 동일 |
| video checkpoint | final 4997 | final 4997 | 동일 checkpoint 위치 |
| video command/seed | manifest에 없음 | 없음 | 행동 정성 비교만 가능 |
| fixed evaluator | 제공되지 않음 | 제공되지 않음 | 공식/정량 정책 우열 판단 불가 |

**판정:** reward 변경 효과 질문에는 **직접 비교에 적합하되 단일-seed/비고정 episode 때문에 조건부 인과 해석**, 완성 정책의 행동 비교에는 **조건부 비교**, 공식 성능/제출 점수 질문에는 **판단 불가**다.

---

## 4. TensorBoard raw 시계열 재분석

각 archive의 `native_run/events.out.tfevents*`를 직접 파싱했다. 두 event 모두 `Train/mean_reward` 기준 정확히 2,000점이며 step 범위는 `2998..4997`; step reset이나 다중 event 중복은 없었다. 비교 window는 resume 재적응과 finalizer warm-up의 영향을 줄이기 위해 주로 **late-500 (`4498..4997`)**을 사용했고, 경계 민감성 확인용으로 **late-300 (`4698..4997`)**과 last-100도 함께 확인했다. late-500/late-300 결론 방향이 다른 경우는 따로 표시했다.

### 4.1 핵심 late window

| tag (평균) | control late-500 | H-009 late-500 | H009-control | control late-300 | H-009 late-300 | H009-control |
|---|---:|---:|---:|---:|---:|---:|
| `Curriculum/terrain_levels` | 5.67184 | 5.63891 | -0.03294 | 5.65162 | 5.65373 | +0.00212 |
| `Episode_Termination/base_contact` | 0.29420 | 0.29065 | -0.00355 | 0.29095 | 0.29189 | +0.00094 |
| `Episode_Termination/time_out` | 0.70595 | 0.70950 | +0.00355 | 0.70912 | 0.70829 | -0.00084 |
| `Train/mean_episode_length` | 774.94 | 777.49 | +2.55 | 778.69 | 777.42 | -1.27 |
| `Metrics/base_velocity/error_vel_xy` | 0.32938 | 0.32921 | -0.00017 | 0.32806 | 0.32814 | +0.00008 |
| `Metrics/base_velocity/error_vel_yaw` | 1.42790 | 1.32786 | **-0.10005** | 1.40977 | 1.31170 | **-0.09807** |
| `Policy/mean_std` | 1.47776 | 1.46223 | -0.01553 | 1.47352 | 1.45951 | -0.01401 |

해석:

- **terrain:** window 선택에 따라 부호가 바뀌며 차이도 작다. H-009의 지형 진행 향상이라고 볼 수 없다.
- **base-contact / timeout / episode length:** late-500은 H-009가 약간 좋아 보이지만 late-300에서 거의 사라지거나 반전된다. 결정적 차이로 취급하지 않는다.
- **XY tracking:** 거의 동일하다.
- **yaw tracking:** late-500과 late-300 모두 H-009가 약 `0.10` 낮다. last-100에서도 `1.37965 → 1.31038` (`-0.06927`)로 같은 방향이 남아 있다. 이번 run의 가장 일관된 차이다.
- **policy std:** H-009가 소폭 낮지만 둘 다 약 1.46–1.48 수준이다. std 단독으로 정책 수렴/품질을 판정하지 않는다.

### 4.2 endpoint와 reward peak

- control endpoint: terrain `5.61237`, XY `0.32572`, yaw `1.39123`, base-contact `0.30246`, episode length `764.63`, std `1.47221`.
- H-009 endpoint: terrain `5.58274`, XY `0.32578`, yaw `1.27797`, base-contact `0.28846`, episode length `778.59`, std `1.45305`.
- control raw reward maximum: `6.19254 @ step 3125`; H-009 raw reward maximum: `5.74689 @ 4792`.
- resume finalizer의 약 10% warm-up을 적용해 `step>=3197`만 보면 control eligible reward max는 `5.75723 @ 4874`, H-009는 `5.74689 @ 4792`.

총 reward는 hip reward weight가 다르므로 정책 성능의 직접 척도로 쓰지 않는다. control의 early raw reward max `@3125`는 warm-up 밖이며 대표 checkpoint 근거로 쓰지 않는다.

### 4.3 reward term과 최적화 안정성

late-500의 weighted hip reward term은 control `-0.03686`, H-009 `-0.04748`. 이 값은 H-009의 weight 절댓값이 50% 커졌기 때문에 **underlying hip deviation을 복원할 근거가 아니다**. 오히려 hip posture의 실제 개선 여부는 비가중 deviation metric 또는 evaluator/video가 필요하다.

value/surrogate loss의 가장 큰 절댓값은 두 run 모두 resume 첫 step 2998 부근이며 각각 control value `0.01988`, H-009 `0.01815` 수준으로, NaN/Inf나 발산 신호는 확인하지 못했다. 두 validation도 PASS이고 학습은 정상 완료됐다.

---

## 5. 6지형 행동 비교

### 판독 방법과 한계

이번 분석에서는 각 MP4를 디코딩해 **1, 4, 7, 10, 13, 16, 19초 프레임을 양쪽 동일 시각으로 비교**했고, 차이가 가장 커 보인 boxes는 **14, 15, 16, 17, 18, 19, 19.8초**를 추가 확인했다. 따라서 아래는 실제 영상 프레임 기반 관찰이지만, 전 프레임 연속 시청으로 보행 주기·진동 주파수를 정량화한 것은 아니다. manifest에 command가 없으므로 명령 추종 위반은 판정하지 않는다.

| terrain | corrected control 관찰 | H-009 관찰 | 공통/차이와 한계 |
|---|---|---|---|
| stairs | 1–10s 접근, 약 13s 계단 접촉/상승, 16s 이후 반대편으로 진행, 19s에는 계단을 벗어난 위치. 샘플 프레임에서 낙상 없음. | 거의 같은 시간대에 계단 접근·접촉·통과, 19s에 반대편 진행. 샘플 프레임에서 낙상 없음. | 둘 다 명확한 실제 traversal. H-009만의 뚜렷한 자세 우위는 프레임 표본에서 확인 못함. |
| inverted_stairs | 1–10s 계단 구조를 따라 이동, 13–16s 구조를 벗어나며 19s까지 upright. | 유사한 진행과 통과. | 둘 다 진행/통과. command·동일 접촉점이 보장되지 않아 미세 속도 비교 금지. |
| boxes | 1–13s 장애물 영역 내부 진행. 14–18s에도 upright하며 이동, 19–19.8s에 상체/보폭이 크게 기울어 보이는 순간이 있으나 body-floor 낙상은 표본에서 확정되지 않음. | 1–13s 진행, 14–19.8s에도 장애물 사이에서 upright 진행. 후반 프레임은 control보다 덜 극단적으로 기울어 보이는 순간이 있음. | **가장 차이가 보이는 지형**이지만 1개 짧은 clip의 순간 자세 차이다. H-009의 hip penalty 효과로 단정할 수 없음. 둘 다 clip 끝까지 장애물 영역을 완전히 벗어났다고 말하기 어렵다. |
| random_rough | 1–16s 거친 패치 내부를 진행하고 19s에는 패치 바깥쪽까지 나감. upright. | 유사하게 패치를 지나 19s 바깥쪽 진행. upright. | 둘 다 traversal 확인. 뚜렷한 차이 없음. |
| slope_up_10deg | 전 구간 upright하며 지형 위 실제 위치가 변함. 큰 자세 붕괴/낙상 없음. | 동일하게 upright 진행. | 영상만으로 경사 방향 command를 확인할 수 없어 추종 우열은 보류. |
| slope_down_10deg | 전 구간 upright하며 진행. 큰 낙상 없음. | 동일하게 upright 진행. | 뚜렷한 차이 없음. |

### 영상과 수치의 교차검증

- training scalar의 base-contact가 약 29%라고 해서 영상에서 29% 낙상률이 보여야 하는 것은 아니다. training aggregate와 각 19.98초 native play clip은 다른 집계다. 실제 샘플 프레임에서는 양쪽 모두 6개 지형에서 body-floor 낙상을 확인하지 못했다.
- late-TB에서 H-009 yaw error가 더 낮지만 영상 manifest에 command 방향·크기가 없으므로 “영상에서도 yaw tracking이 더 좋다”고 독립 확인할 수 없다.
- boxes 후반의 H-009가 상대적으로 덜 기울어 보이는 장면은 hip-penalty 가설과 정성적으로 맞지만, 다른 5지형에서 일관된 posture 차이가 보이지 않고 비가중 hip deviation metric도 없어 강한 근거로 승격하지 않는다.

---

## 6. 핵심 발견과 경쟁 설명

### 발견 A — yaw error 감소는 반복되는 차이다

**관찰:** late-500 `1.42790 → 1.32786`, late-300 `1.40977 → 1.31170`, last-100 `1.37965 → 1.31038`로 H-009가 낮다.

**해석 가설:** hip deviation penalty 강화가 하체 자세의 자유도를 줄여 yaw 축 흔들림/heading error를 간접적으로 줄였을 가능성이 있다.

**경쟁 설명:** 단일 seed training에서 episode/terrain realization 차이, curriculum의 미세 차이, stochastic PPO trajectory가 같은 방향의 yaw 차이를 만들었을 수 있다.

**반대 근거:** XY, terrain, base-contact, episode length에서는 같은 수준의 일관된 개선이 없다. 영상에서도 회전 command를 알 수 없어 yaw 개선을 직접 재현하지 못했다.

**판별:** 두 final checkpoint를 동일 yaw/linear command sequence와 고정 terrain/seed evaluator에서 paired 측정한다.

### 발견 B — 안정성/terrain 개선 주장은 성립하지 않는다

**관찰:** late-500에서는 H-009 base-contact가 -0.36%p이고 episode length +2.55지만, late-300에서는 base-contact +0.09%p, episode length -1.27로 차이가 사라진다. terrain도 late-500 -0.033에서 late-300 +0.002로 부호가 바뀐다.

**해석:** 이 축에서는 두 정책이 사실상 비슷한 영역에 있다.

**경쟁 설명:** window 경계와 curriculum 상태 변화가 작은 차이를 좌우한다.

**반대 근거:** endpoint 하나만 보면 H-009 base-contact와 episode length가 좋아 보이지만, window 평균이 이를 안정적으로 지지하지 않는다.

**판별:** 고정 evaluator의 repeated episode에서 fall/traversal을 직접 센다.

### 발견 C — hip posture 자체는 아직 미측정이다

**관찰:** H-009의 weighted `Episode_Reward/joint_deviation_hip`가 더 음수다.

**해석 제한:** weight가 -0.2→-0.3으로 바뀌었으므로 이 weighted term을 나눠 posture deviation으로 복원하지 않는다. term의 normalization/aggregation을 이번 입력에서 검증하지 않았다.

**반대 근거:** boxes 후반 프레임에 H-009가 상대적으로 덜 기울어 보이는 순간은 있으나 다른 지형에서 반복되는 명확한 차이는 없다.

**판별:** evaluator에서 실제 hip joint deviation 또는 reward 함수의 pre-weight metric을 직접 기록한다.

---

## 7. checkpoint 판단·가설 결정·다음 행동

### 7.1 실행 / evidence / 가설 / 정책

- **실행:** A H-009 `COMPLETE`; B corrected control `COMPLETE`.
- **evidence:** 두 archive validation `PASS`; final checkpoint ↔ video manifest SHA 직접 일치. parent는 metadata상 동일 SHA이나 parent 원본 바이트는 이번 입력에 없어 “기록상 동일” 수준.
- **가설:** **HOLD** — H-009의 yaw tracking 개선 신호는 유망하지만, posture/terrain/survival/영상에서 결정적이고 재현된 control-relative 이득이 없다.
- **정책:** 두 final `model_4997` 모두 6지형 native play에서 upright 진행과 여러 지형 traversal을 보이는 질적 sanity evidence가 있다. H-009가 boxes 후반에서 상대적으로 덜 기울어 보이는 장면이 있으나 정책 우월성의 충분한 근거는 아니다.

### 7.2 대표 checkpoint

프로젝트 운영 원칙과 이번 late trajectory를 따르면 두 run 모두 **final numbered `model_4997.pt`를 대표 후보로 유지**하는 것이 맞다. 마지막 수백 iteration에서 terrain·tracking·낙상이 함께 뚜렷하게 붕괴하지 않았다. 자동 `model_best`는 control `model_4900`, H-009 `model_4800`이지만 이는 training reward selector의 결과이며, 실제 6지형 영상은 final 4997에서 생성돼 있다. 따라서 행동 분석은 final 4997에만 귀속했다.

### 7.3 다음 한 번의 행동 — 1순위

**새 학습 없이 두 final checkpoint의 동일 fixed evaluator paired 비교.**

- 대상: H-009 `model_4997` SHA `4c13ecd...67c0` vs control `model_4997` SHA `4349fe...5b6d`.
- 맞출 조건: 동일 evaluator version, terrain set/difficulty, command sequence, seed set, episode horizon, camera 불필요, 동일 metric window.
- 최소 지표: x/y/yaw tracking error, forward/terrain progress, fall/base-contact, timeout, hip deviation, torso deviation; boxes/stairs에서 stall과 회복 annotation.
- 답할 질문: TB에서 보인 약 `0.07~0.10` yaw-error 방향이 고정 조건에서도 재현되는가? 그때 hip posture가 실제로 좋아지는가? terrain/survival trade-off는 없는가?
- 결과별 결정: yaw 개선 + posture 개선/비악화 + survival/progress 유지가 재현되면 H-009를 `PROMOTE` 검토. yaw 차이가 사라지거나 progress/survival이 악화되면 `REJECT` 또는 `HOLD` 유지.

현재 자료로 이미 해결 가능한 학습 provenance/TB/video sanity 질문은 대부분 소진됐으므로, **같은 archive를 더 재집계하는 것보다 이 paired evaluator가 가장 큰 정보 증가를 준다**. 새로운 GPU 학습은 이 평가 뒤에도 hip penalty 효과가 불명확할 때만 검토한다.

---

## 8. 한계와 재확인 가능한 근거 목록

1. 입력 train archives의 `metadata.json`, `validation.json`, `command.txt`, `source/humanoid_rewards.py`, `native_run/params/{env,agent}.yaml`, raw TensorBoard event, mirrored checkpoints를 직접 확인했다.
2. 두 final checkpoint SHA를 직접 계산하고 각 `video_suite_manifest.json`의 source SHA와 대조했다.
3. 6개 MP4를 실제 디코딩해 공통 시각 프레임을 조사했다. 다만 전 구간 연속 프레임 기반 gait-cycle 정량분석은 하지 않았다.
4. manifest에 command/difficulty/video seed의 상세값이 없어 영상으로 command tracking 수치를 판정하지 않았다.
5. parent checkpoint 원본은 이번 입력에 없어 metadata의 parent SHA를 원본 바이트와 재검증하지 못했다.
6. 단일 seed이며 training TensorBoard 점들은 독립 seed 표본이 아니다. p-value/신뢰구간으로 통계적 우월성을 주장하지 않았다.
7. PERSONAL 결과이므로 OFFICIAL 제출 성능·공식 점수 증거로 승격하지 않는다.
8. project reference의 checkpoint 해석 원칙상 충분히 긴 resume에서는 final numbered checkpoint를 기본 대표로 두고, late terrain/tracking/fall의 공동 붕괴가 있을 때만 predecessor를 검토한다. 이번 두 run에는 그 공동 붕괴가 보이지 않았다.

## 최종 판정

**H-009 HIPDEV030 corrected: HOLD.**  
동일-parent 단일변수 sibling 비교에서 yaw tracking error 감소라는 반복적인 신호가 확인됐지만, terrain·XY·survival·행동 영상의 control-relative 개선은 결정적이지 않고 hip posture 자체도 비가중 metric으로 확인되지 않았다. final 4997은 대표 checkpoint로 유지하고, 다음 결정은 두 final checkpoint의 고정 paired evaluator에서 내려야 한다.
