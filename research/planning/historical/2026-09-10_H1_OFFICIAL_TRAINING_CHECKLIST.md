> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/planning/historical/2026-09-10_H1_OFFICIAL_TRAINING_CHECKLIST.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# NCRC 공식 학습 — 가져올 운영 규칙

> **역사적 운영안:** 파일명의 날짜는 당시 작성일이다. 아래의 ‘현재’·‘다음’·PLANNED 표기는 보존된 과거 시점의 문구이며 현행 상태가 아니다. 실제 실행은 [현재 registry](<../../EXPERIMENTS.md>)와 서버 운영 문서〔원본 참조: `../../ai_library/11_SERVER_OPERATIONS.md` / 공개 사본 미포함〕를 따른다. 이번 재배치에서는 과거 판단을 새 결과처럼 고쳐 쓰지 않았다.

> **현재 상태:** 실행·보존 체크리스트는 참고할 수 있지만, 아래 `TERM-20`/yaw 후보 선택은 2026-09-10 당시 계획으로 **superseded**됐다. 해당 `ORIENT-100` OFFICIAL fresh 3K는 2026-10-06 완료됐고, 2026-10-07 PERSONAL 단일 정책 행동 판정은 HOLD다. 현재 우선은 `research/EXPERIMENTS.md`에서 **기존 TERM-50 동일 evaluator baseline 대조 가능성**을 확인하는 것이며, `ACTRATE-001`은 별도 PLANNED Experiment다. 이 문서의 후보 목록을 새 실행 승인이나 현재 우선순위로 해석하지 않는다.

작성: 2026-09-10\
용도: 이후 H1/Go2 공식 서버 학습 전에만 참고하는 독립 체크리스트\
출처 아이디어: `KEYSTONE360/Issac-Sim-physics-runtime`의 **운영 습관**\
로컬 원본: `Downloads\NCRC_공식학습_가져올_운영규칙.md`\
대상 작업 공간: `Desktop\코딩\01_working\네이버\` 아래 세 저장소

이 파일은 그 레포를 설치하거나 실행하라는 안내가 아니다.\
공식 Isaac Sim 학습·play를 대체하지 않는다. MuJoCo/native PhysX 점수로 다음 reward를 고르지 않는다.

---

## 한 줄 원칙

공식 서버에서는 reward 숫자 하나만 바꾸고, 나머지 환경은 TERM50과 잠그고, 종료 전에 산출물을 원형+해시로 남긴 뒤, 행동에 가까운 지표로만 판정한다.

---

## 가져오는 것 / 가져오지 않는 것

| 가져온다 | 가져오지 않는다 |
| --- | --- |
| 학습 전 `env.yaml` reward 외 필드 잠금 | `NCRC-Physics-Runtime.exe` / `ncrc-lab` 설치 |
| `humanoid_rewards.py` 숫자 리터럴만 수정 | MuJoCo H1 로컬 평가 점수 |
| 산출물 SHA-256과 중복 지문 | native PhysX 상자 probe를 H1 검증으로 사용 |
| 로컬·개인 서버 학습본은 제출 불가 | 256차원 관측이 맞다는 가정 (저쪽 height scan은 상수) |
| 스크리닝 1회 → 유망할 때만 긴 확인 | `ncrc-lab recommend`로 다음 실험 결정 |
| 공식 서버 산출물만 제출 후보 | `Train/mean_reward` 절댓값으로 run 간 우열 |

개인 NVIDIA/Brev는 공식 `policy`의 play·관찰용이다. 거기서 새로 학습한 정책은 제출하지 않는다.

---

## 현재 H1 기준점

다음 공식 학습의 부모는 **공식 서버 `h1-submit-2 / TERM-50` fresh 5K**다.

- 학생 reward 중 `termination_penalty`만 `-5.0 → -50.0`
- seed 42, 4096 envs, 5000 iterations
- endpoint: terrain 5.825, base-contact 28.93%, timeout 71.07%, XY error 0.378, yaw error 0.935
- `TERM-50`은 당시 **stability anchor**로 사용됐다
- 당시 다음 변경 계획은 `TERM-50` checkpoint에서 **한 변수만**이었다

| ID | 바꿀 값 | 방향 |
| --- | --- | --- |
| A | `termination_penalty` `-50 → -20` | 생존은 유지하고 yaw 여유를 보는지 |
| B | `track_ang_vel_z_exp` `0.5 → 0.6` | yaw 추종만 미세 강화 |

A와 B를 같은 실행에서 같이 바꾸지 않는다.\
H1 resume 시 terrain curriculum이 쉬운 단계로 리셋되므로, 이것은 연속 학습이 아니라 **checkpoint fine-tuning**이다.

고정할 것: 공식 서버 image, seed 42, 4096 envs, 24 steps/env, PPO, observation, action, terrain, `--headless`, camera 없음. 영상은 학습과 별도 play.

---

## 학습 전

먼저 검증 질문을 나타내는 Experiment 이름을 [현재 명명 규칙](<../../EXPERIMENT_NAMING.md>)에 따라 적고, 기준 preset과 최종 override를 별도로 기록한다. 예: `Experiment: exp-h1-termination-20-after-term50`; `Preset/override: h1-submit-2 + term=-20`. 실행 후에는 실제 evidence Run ID, fresh/resume 구분, parent checkpoint와 SHA를 연결한다. 기존 H/HS/G/GS 표기는 legacy alias로만 유지한다.

1. 부모 `h1-submit-2 / TERM-50`의 `env.yaml`을 배경 잠금본으로 삼는다.
2. 참가자 파일이면 `training/humanoid/humanoid_rewards.py`만 연다. Go2면 `quadruped_rewards.py`만.
3. 목표 weight **한 줄**만 바꾼다. 주석, 함수, 다른 항, `agent_cfg.py`, `env_cfg.py`, `train.py`는 건드리지 않는다.
4. diff가 그 숫자뿐인지 확인한다.
5. 실제 명령, `train.py --help`, 코드/파일 SHA-256, GPU·runtime, headless/camera 조건을 기록한다.
6. 기존 `logs/`와 `exported/`가 있으면 먼저 복사한다. 새 실행을 위해 지우거나 덮어쓰지 않는다.

`env.yaml` 검사 요지:

- `rewards` / `reward` 밖의 모든 값은 부모와 **완전 동일**
- reward **이름·함수 바인딩**은 불변
- 허용되는 변경은 기존 term의 유한 숫자(`weight` 또는 기존 `params` 잎)뿐
- `[WARN] skip` 된 term은 적용된 reward로 세지 않는다

제출용 학습은 배포된 PPO 설정을 유지한다. learning rate·KL·RSL-RL을 바꾸는 별도 질문은 새 descriptive Experiment 이름으로 남기고, preset-relative override와 실제 Run을 분리해 기록한다.

---

## 학습 중

- 화면이 필요 없으면 지원되는 `--headless`만 쓴다. `--enable_cameras`는 끈다.
- stdout·stderr 전체를 `tee`로 저장한다.
- 시작·종료 시각, exit code, dashboard 사용시간을 남긴다.
- 가능하면 1~2초 간격 GPU utilization·VRAM·power·temperature.
- NaN, CUDA OOM, simulator error, 반복 warning 시점을 표시한다.
- GUI/headless, camera, viewport, 영상 녹화가 다른 run의 seconds/iteration과 VRAM을 직접 비교하지 않는다.

---

## 종료 전 필수 export

`policy.pt`만 받아 서버를 끄지 않는다. finalize가 checkpoint를 지우기 **전에** `logs/<run>/`를 통째로 복사한다.

```text
experiment_id/
├─ command.txt
├─ train_help.txt
├─ train_console.log
├─ code_sha256.txt
├─ reward_diff.patch
├─ system/
│  ├─ runtime.txt
│  ├─ nvidia_smi_before.txt
│  ├─ nvidia_smi_during.csv
│  └─ nvidia_smi_after.txt
├─ logs/<run>/          # 원형 그대로
│  ├─ events.out.tfevents*
│  ├─ model_*.pt
│  └─ env·agent 설정
├─ exported/
│  ├─ model_best.pt
│  ├─ env.yaml
│  ├─ policy.pt
│  ├─ policy.onnx
│  ├─ report.html
│  └─ play_video.mp4
└─ manifest_sha256.txt  # 상대경로, bytes, SHA-256
```

영상 manifest 한 행에 묶을 것:

- source checkpoint 실제 iteration과 SHA-256
- exported `policy.pt` SHA-256
- MP4 SHA-256
- 요청 frames와 실제 duration

렌더 전 stale `play_video.mp4` / `policy.pt`를 지우고, 렌더 후 세 파일이 비어 있지 않은지 확인한다.\
파일명만으로 같은 정책이라고 단정하지 않는다.

별칭 구분:

- 5K zero-based 최종 저장본은 `model_4999.pt`가 정상이다.
- `model_best.pt`는 `Train/mean_reward` 최고 step에 가까운 저장본일 뿐, 공식 시나리오 최적이 아니다.
- 개인 L40S에서 TERM50 이름 MP4가 baseline 1K와 SHA-256까지 같았던 사례가 있다. 그 영상은 증거로 쓰지 않는다.

원본은 `naver-issacsim-originals`에만 보관한다. 정정이 필요하면 overlay만 쓴다. 원본 archive를 고치지 않는다.

---

## 판정

`Train/mean_reward` 절댓값은 run 사이 우열에 쓰지 않는다. reward 계수가 바뀌면 총점 척도가 바뀐다.

우선 지표:

1. fall rate / termination 빈도
2. episode length last-window 중앙값과 분포
3. terrain 최초 상승, late 중앙값, 최댓값
4. linear / yaw tracking
5. 올바른 checkpoint에서 다시 렌더한 영상
6. action std, action-rate, 정지·진동 (보조)
7. KL, learning rate, entropy, loss (학습 안정 보조)
8. GPU·seconds/iteration (환경 동일성 확인용)

TensorBoard에 **실제로 있는 태그**만 본다. 없는 값을 추정으로 채우지 않는다.\
`report.html`과 raw event가 다르면 raw event를 우선한다. raw reward 최고가 제출 최적은 아니다.

영상에서 탈락:

- 덜 넘어지지만 안 움직임
- 제자리 회전, 명령 반대 이동
- hopping, 한 발 들기, foot dragging
- 상체 경직, 큰 진동
- 평지 후 terrain 진입 즉시 붕괴

채택 조건: 생존성, terrain, linear/yaw tracking, stop-command drift를 **함께** 통과.

| 관찰 | 다음 |
| --- | --- |
| fall↓, episode↑, tracking·terrain 유지 | 같은 설정 장시간 confirmation 후보 |
| fall↓, tracking↓ 또는 정지 | 다른 한 변수 또는 중간값 검토. A였으면 `-20` 재고 |
| 차이 거의 없음 | 학습량·terrain 변동·영향 미약을 분리 |
| fall·진동·KL 악화 | 그 분기 확장 중지, 로그 원인 |
| 설정·처리량 불일치 | reward 결론 보류, 비교환경부터 복구 |

단일 seed 결과를 통계적 개선이나 최적값이라고 부르지 않는다.

---

## 반복 예산

- 원인 섞인 결과는 복제하지 말고 변수부터 분리한다.
- 스크리닝은 1회.
- 유망하면 같은 설정 확인 2~3회 권장, 최대 5회.
- 확연히 나쁘면 서버 시간을 더 쓰지 않고 가설을 바꾼다.

Optuna는 아직 시작하지 않는다. 공통 evaluator, 같은 학습량, 복수 seed가 없다.\
공식 서버에 Optuna·에이전트·임의 패키지를 설치하지 않는다.

---

## 제출 경계

제출물:

- `policy.pt` — play 검증 후 export한 정책
- `env.yaml` — 그 정책을 만든 설정과 일치
- 기술 개선 리포트 — 바꾼 reward, 이유, 관찰이 모순 없이

제출이 아닌 것: `model_best.pt`, `report.html`, TensorBoard, 개인 서버 학습본, MuJoCo 평가 JSON.

공식 서버가 아닌 origin이면 `SUBMISSION_ELIGIBLE=false`로 취급한다.

---

## 세 저장소

| 저장소 | 역할 |
| --- | --- |
| `naver-issacsim-originals` | 원본 archive, 로그, TensorBoard, checkpoint, 영상. 수정 금지 |
| `naver-issacsim` | 검토된 분석, 실험 판정, AI 라이브러리 |
| `naver-issacsim-nvidia` | Brev 환경, 학습·영상·백업 자동화 |

유료 인스턴스 생성·삭제, Git history 재작성, 원본 덮어쓰기는 명시 승인 없이 하지 않는다.

참고 clone 위치(실행하지 않음):\
`Downloads\작업공간\Issac-Sim-physics-runtime`

---

## 학습 당일 짧은 체크

- [ ] Experiment 질문 이름, 기준 submission preset, 최종 override 기록; 완료 후 실제 evidence Run ID 연결
- [ ] A 또는 B 중 하나만 반영, diff 한 줄
- [ ] 부모 `env.yaml`과 reward 외 동일
- [ ] headless, camera 끔, 명령 기록
- [ ] 기존 logs/exported 보존
- [ ] 학습 중 tee + GPU 시계열
- [ ] finalize 전 `logs/<run>/` 통째 복사
- [ ] tfevents, 콘솔, 모든 `model_*.pt`, env, policy, onnx, report
- [ ] manifest SHA-256
- [ ] 올바른 checkpoint에서 영상 재렌더, 해시 한 행으로 연결
- [ ] fall / episode / terrain / tracking / 영상으로 판정
- [ ] 로컬 점수를 제출 후보라고 쓰지 않음
- [ ] Originals에 원본 보관, Analysis에 판정만
