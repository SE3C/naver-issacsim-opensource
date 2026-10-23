---
id: h1-official-server-baseline-20260824
source_type: reviewed_experiment_analysis
category: official_server_experiment
robot: H1
run_started_at: "2026-08-24 12:44:13 KST"
reviewed_at: "2026-08-24"
trust_level: artifact_verified_with_explicit_evidence_gaps
original_draft_sha256: "575629025D4F640374459CB61C7D183C9C73494BDD8FB6F532E653FE998A1220"
authority: "실행 산출물과 코드로 확인되는 기술 기준선이며 공식 평가 점수나 장기 성능 예측이 아니다."
---

# [학습] H1 공식 서버 300-iteration 기준선 분석

> 관리 안내 (2026-10-13): **학습** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](../../../../../research/EXPERIMENTS.md)를 확인한다.

## 기술 요약

이번 실행은 **학습·finalize·export·play 산출물이 정상 생성되는지와 실제 환경 설정을 확인한 파이프라인 기준선**으로는 성공했다. 그러나 300 iterations에서 나온 정책은 마지막 지형 단계 `0.00`, 낙상률 `100.0%`였으므로 성능 기준선이나 Optuna 비교 trial로 사용하기에는 이르다.

저장된 `report.html`이 확인하는 전체 소요시간은 4분이다. 이 값으로 계산할 수 있는 end-to-end 평균은 `0.80 s/iteration`이다. 원래 분석 초안의 `0.69~0.71 s/iteration`은 터미널 관찰값으로 적혀 있지만 해당 콘솔 로그가 보관되지 않아 확정값으로 승격하지 않았다. 같은 이유로 5,000~25,000 iterations의 장기 실행시간 선형 외삽도 이 문서에서 제거했다.

가장 중요한 환경 발견은 두 가지다.

1. 학생이 수정하는 H1 reward 9개 외에도 실제 `env.yaml`에는 nonzero 기본 reward 4개가 더 있어, 실질 활성 reward는 13개다.
2. 지형 6종의 설정 weight 합은 `0.90`이다. Isaac Lab은 이를 합계 1로 정규화하므로 raw weight를 그대로 200개 patch 수로 환산하면 안 된다.

## 증거 등급과 범위

| 등급 | 의미 | 이번 문서에서의 예 |
| --- | --- | --- |
| A — 산출물 확인 | 보관된 실행 파일에서 직접 읽힘 | 300 iterations, 4분, seed 42, 4096 envs, 지형 0.00, 낙상률 100% |
| B — 코드 교차검증 | 보관된 서버 백업 코드와 산출물 설정이 일치 | PPO 설정, checkpoint 선택 로직, `num_steps_per_env=24` |
| C — 원본 미보관 관찰 | 분석 초안에는 있으나 터미널 원본이 없음 | 상세 GPU/CPU/OS, 코어 iteration 0.69~0.71초 |
| D — 탐색적 분석 | 인공 관측 또는 별도 계산이며 공식 성능이 아님 | 단일 관측 policy probe, Jacobian sensitivity |

이 보고서는 A와 B만 핵심 결론에 사용한다. C는 재측정 대상으로만 남기며, D는 재현 스크립트가 보관되지 않아 AI 핵심팩에 반영하지 않는다.

## 보관된 증거

원본 저장소 위치:

```text
naver-issacsim-originals/data/raw/official_server_runs/h1/
  2026-08-24_124413_baseline_300iter/
```

보관 파일은 `env.yaml`, `model_best.pt`, `report.html`, `policy.pt`, `policy.onnx`, `play_video.mp4`와 동일 내용의 timestamp 별칭 파일이다. 현재 묶음에는 콘솔 학습 로그, TensorBoard event, `nvidia-smi` 출력, GPU 시계열, 실행 당시 코드 hash가 없다.

## 실행 결과에서 직접 확인되는 기준선

| 항목 | 값 | 등급 |
| --- | ---: | --- |
| task/robot | Humanoid / Unitree H1, 19 actions | A |
| 실행 시작 | 2026-08-24 12:44:13 | A (`env.yaml` log path) |
| seed | 42 | A |
| 병렬 환경 수 | 4096 | A |
| 총 iterations | 300 (`iter 299`까지) | A |
| end-to-end 실행시간 | 4분 0초 | A |
| end-to-end 평균 | 0.80 s/iteration | A 값의 계산 |
| report 최고 mean reward | 0.16, step 287 | A — 화면 표시 정밀도 |
| 선택된 checkpoint | iteration 299 | A |
| 마지막 terrain level | 0.00 | A |
| 마지막 fall rate | 100.0% | A |
| 마지막 exploration std 평균 | 0.633 | A |
| NaN | report상 없음 | A |

`report.html`은 정상 UTF-8 파일이다. 한글이 깨져 보이면 파일 손상이 아니라 읽는 도구의 인코딩 설정을 먼저 확인한다.

## 데이터량은 계산 가능하지만 장기시간은 아직 예측하지 않는다

백업 `agent_cfg.py`의 `num_steps_per_env=24`와 `env.yaml`의 4096개 환경을 사용하면 다음 값은 산술적으로 계산된다.

| 항목 | 계산 | 값 |
| --- | --- | ---: |
| transitions/iteration | `4096 × 24` | 98,304 |
| physics ticks/iteration | `4096 × 24 × 4` | 393,216 |
| 300회 transitions | `98,304 × 300` | 29,491,200 |
| 300회 physics ticks | `393,216 × 300` | 117,964,800 |
| env 하나의 누적 시뮬 시간 | `24 × 0.02 × 300` | 144초 |
| 전체 env aggregate 경험 | `144 × 4096 / 3600` | 163.84 robot-hours |

다만 4분에는 초기화·학습·checkpoint·finalize·export가 함께 들어간다. 안정 구간 iteration 로그가 없으므로 고정 오버헤드와 학습 코어 시간을 분리하지 않는다. 장기시간은 다음 실행에서 전체 로그와 안정 구간 표본을 확보한 뒤 다시 계산한다.

## 학습 실행 모드는 headless를 기본으로 한다

PPO 학습과 처리량 측정처럼 화면을 볼 필요가 없는 실행은 **공식 스크립트가 지원하는 `--headless` 옵션을 기본값으로 사용한다.** Isaac Lab의 `--headless`는 화면 표시를 끄며, NVIDIA도 센서가 요구하지 않는 렌더링을 완전히 끄려면 headless application workflow를 사용하라고 안내한다. GUI·viewport·렌더링 경로를 생략하면 불필요한 CPU/GPU 작업과 관련 메모리 사용을 줄일 여지가 있어, 같은 서버 자원을 물리 시뮬레이션과 학습에 더 집중할 수 있다.

다만 절감량은 scene, Isaac Sim/Lab 버전, 실행 experience에 따라 달라지므로 “RAM이 항상 특정 비율만큼 감소한다”고 단정하지 않는다. 또한 headless는 물리 상태, 4096개 병렬 환경 tensor, terrain, policy, CUDA allocation까지 제거하는 모드가 아니다. **카메라나 이미지 센서를 켜면 GUI가 없어도 오프스크린 렌더러가 작동해 GPU 연산과 VRAM을 계속 사용한다.** 영상·이미지 관측이 필요 없는 학습에서는 `--enable_cameras`를 사용하지 않고, play 영상 생성이나 시각 검증은 학습과 분리해 필요한 구간에만 렌더링한다.

NVIDIA 문서에 따르면 Python headless 실행도 기본 viewport를 렌더해 불필요한 overhead가 남을 수 있다. 자체 `SimulationApp` 기반 개인 검증 도구에서는 카메라·streaming이 필요 없을 때 `disable_viewport_updates=True`를 별도로 검토할 수 있다. 이 설정은 headless에서만 지원되고 streaming에는 사용하면 안 된다. 공식 대회 서버에서는 이 최적화를 위해 제공 코드를 임의 수정하지 말고, 먼저 `train.py --help`에 공개된 `--headless` 같은 CLI만 사용한다.

처리량 비교는 `headless`, camera/offscreen rendering, viewport update, video recording 조건을 동일하게 맞춘 실행끼리만 한다. GUI 실행과 무렌더 headless 실행의 seconds/iteration을 같은 기준선으로 섞으면 안 된다.

공식 참고:

- Isaac Lab `AppLauncher`: <https://isaac-sim.github.io/IsaacLab/main/source/tutorials/00_sim/launch_app.html>
- NVIDIA Isaac Sim Performance Optimization Handbook: <https://docs.isaacsim.omniverse.nvidia.com/latest/reference_material/sim_performance_optimization_handbook.html>

## 확인된 환경 시간축과 정책 크기

| 항목 | 값 | 근거 |
| --- | ---: | --- |
| physics dt | 0.005초, 200 Hz | `env.yaml` |
| decimation | 4 | `env.yaml` |
| control dt | 0.020초, 50 Hz | 계산 |
| episode limit | 20초 | `env.yaml` |
| command resampling | 10초 | `env.yaml` |
| rollout length | env당 24 control steps = 0.48초 | B + 계산 |
| observation | 256차원 | env 구성 + 정책 입력 |
| action | 19차원 joint-position action | env 구성 + 정책 출력 |
| actor hidden dims | `[512, 256, 128]`, ELU | `agent_cfg.py` |
| critic hidden dims | `[512, 256, 128]`, ELU | `agent_cfg.py` |

관측 256차원은 다음 순서다.

```text
base linear velocity   3
base angular velocity  3
projected gravity      3
velocity command       3
joint position        19
joint velocity        19
last action           19
height scan          187
------------------------
total                256
```

action 설정은 `JointPositionAction(scale=0.5, use_default_offset=True)`다. 따라서 백업 코드와 현재 Isaac Lab 동작이 동일하다는 조건에서 정책 출력은 기본 관절 위치에 0.5배로 더해지는 joint target으로 해석된다. 관절별 정확한 순서는 런타임 `dof_names`를 함께 저장해야 완전히 재검증할 수 있다.

## PPO 설정은 reward 탐색 대상이 아니다

백업 `agent_cfg.py`에서 확인되는 PPO 설정은 다음과 같다.

| 항목 | 값 |
| --- | ---: |
| algorithm | PPO |
| learning epochs | 5 |
| mini-batches | 4 |
| initial learning rate | 1.0e-3 |
| schedule | adaptive |
| gamma / lambda | 0.99 / 0.95 |
| desired KL | 0.01 |
| entropy coefficient | 0.008 |
| PPO clip | 0.2 |
| max grad norm | 1.0 |
| save interval | 100 |

한 iteration에는 4 mini-batches를 5 epochs 처리하므로 이론상 20번의 optimizer update가 있다. 300 iterations라면 6,000 updates다. 이 값들은 환경 이해용이며 참가자 reward 탐색에서 PPO 설정을 변경하라는 뜻이 아니다.

## 실제 활성 reward는 13개다

### 참가자 수정 대상 9개

| reward | baseline weight |
| --- | ---: |
| `track_lin_vel_xy_exp` | +0.5 |
| `track_ang_vel_z_exp` | +0.5 |
| `feet_air_time` | +0.2 |
| `termination_penalty` | -5.0 |
| `flat_orientation_l2` | -1.5 |
| `ang_vel_xy_l2` | -0.05 |
| `joint_deviation_hip` | -0.2 |
| `joint_deviation_torso` | -0.1 |
| `action_rate_l2` | -0.0005 |

### 프레임워크 기본 nonzero 4개

| reward | weight | 대상 |
| --- | ---: | --- |
| `dof_acc_l2` | -1.25e-7 | 모든 관절 가속도 |
| `dof_pos_limits` | -1.0 | 발목 관절 한계 |
| `feet_slide` | -0.25 | 발목 접촉 중 미끄러짐 |
| `joint_deviation_arms` | -0.2 | 어깨·팔꿈치 편차 |

`dof_torques_l2`는 weight 0이라 비활성이고, `lin_vel_z_l2`와 `undesired_contacts`는 `null`이다. Optuna가 수정하는 범위는 참가자에게 허용된 reward 파일로 제한하되, 결과 해석에서는 기본 4개가 이미 작동한다는 사실을 잊지 않는다.

`termination_penalty=-5`는 report가 표시하는 추천 구간 `-50~-400` 밖이다. 이는 중요한 sweep 후보지만, **300회 정책의 실패만으로 -5를 원인으로 확정할 수 없다.** 학습량 부족과 reward 효과를 분리하려면 먼저 동일 reward의 더 긴 baseline이 필요하다.

## 지형 weight는 정규화된다

`env.yaml`에는 10행 × 20열, 총 200개 sub-terrain과 아래 raw weight가 저장되어 있다.

| terrain | raw weight | 정규화 비중 |
| --- | ---: | ---: |
| pyramid stairs | 0.15 | 16.67% |
| inverted stairs | 0.15 | 16.67% |
| boxes/random grid | 0.30 | 33.33% |
| random rough | 0.10 | 11.11% |
| pyramid slope | 0.10 | 11.11% |
| inverted slope | 0.10 | 11.11% |
| 합계 | 0.90 | 100% |

Isaac Lab `TerrainGenerator`는 sub-terrain proportion 배열을 합계로 나눠 정규화한다. curriculum 모드에서는 정규화된 누적 비중을 열에 배치하므로, raw weight에 200을 곱한 `30/30/60/20/20/20`은 전체 180개만 설명하는 잘못된 환산이다. 라이브 Isaac Lab 버전과 생성 결과를 보관하지 않았으므로 이 문서에서는 terrain별 정확한 정수 patch 수를 단정하지 않는다.

또한 terrain generator의 seed는 `null`, cache는 `False`다. NVIDIA 공식 Isaac Lab 문서도 이 조합에서는 지형 생성이 완전히 재현되지 않을 수 있다고 설명한다. 이후 비교 실험에서는 reward·학습 seed가 같아도 생성 지형 차이가 섞일 가능성을 기록해야 한다.

공식 구현 참고: <https://github.com/isaac-sim/IsaacLab/blob/release/3.0.0-beta2/source/isaaclab/isaaclab/terrains/terrain_generator.py>

## checkpoint 선택 결과는 정상 동작이다

백업 `_finalize.py`는 TensorBoard의 `Train/mean_reward` 최고 step을 찾고, 저장된 `model_*.pt` 중 그 step에 가장 가까운 checkpoint를 복사한다. 이번 report의 peak는 step 287이고 저장 간격은 100이므로, 마지막 `model_299.pt`가 `model_best.pt`로 선택될 수 있다.

따라서 `model_best.pt`는 대회 시나리오 점수가 가장 높은 정책이라는 뜻이 아니라 **training mean reward peak에 가장 가까운 저장 checkpoint**다. Optuna objective와 최종 제출 판단은 별도 evaluator·영상·낙상·추종 지표를 사용해야 한다.

## 300회 결과가 말하는 것과 말하지 않는 것

확정할 수 있는 결론:

- baseline 코드로 학습부터 checkpoint·환경·정책·영상 export까지 완료됐다.
- 300회 시점 정책은 report 지표상 안정 보행 정책이 아니다.
- 환경·PPO·관측·action·reward·terrain의 실제 구성값을 기준선으로 확보했다.
- 300회는 다음 진단의 비교 기준이지만 reward 후보의 우열을 가르는 학습량은 아니다.

확정할 수 없는 결론:

- `termination_penalty=-5`가 실패의 단독 원인인지
- 1,000·5,000·25,000회에서의 보행 품질과 수렴 시점
- 장기 실행의 steady-state seconds/iteration
- iteration별 reward·episode length·terrain·KL·learning-rate 변화
- 공식 평가기의 비공개 점수와 이번 policy의 공식 점수
- 원래 초안의 인공 policy probe와 Jacobian이 실제 episode 행동을 대표하는지

## 다음 공식 baseline에서 반드시 보강할 자료

reward를 바꾸기 전에 동일 baseline을 더 길게 실행해 학습량 부족과 reward 문제를 분리한다. 서버를 켜기 전 종료 조건을 정하고, **학습이 끝난 뒤 서버를 종료하기 전에 `logs/<run>/` 디렉터리 전체를 원형 그대로 export한다.** `policy.pt`·`model_best.pt`·`report.html`만 받으면 최종 요약은 볼 수 있어도 학습 과정 전체를 복원할 수 없다.

1. `train.py --help` 출력과 실제 실행 명령, `headless`·camera·viewport·video 조건
2. 실행 코드 SHA-256 또는 Git commit/diff
3. `logs/<run>/` 전체 디렉터리와 그 내부의 모든 checkpoint·설정·메타데이터
4. TensorBoard `events.out.tfevents*` 원본 전체
5. `tee`로 저장한 전체 콘솔 학습 로그와 오류·경고 출력
6. 시작 전·학습 중·종료 시 `nvidia-smi` 및 가능하면 시간축 GPU utilization·VRAM·power 기록
7. `env.yaml`, agent/PPO 설정, reward 파일 원본 또는 hash
8. `model_*.pt`, `model_best.pt`, `report.html`
9. `policy.pt`, `policy.onnx`, play 영상과 export 로그
10. 시작·종료 시각, 대시보드 기준 실제 서버 사용시간, 실행 중단 여부

TensorBoard event가 있으면 iteration 0→마지막까지의 `Train/mean_reward`, episode length, terrain progression, reward term별 시계열, KL, learning rate 등 **실제로 기록된 scalar**를 다시 추출할 수 있다. 다만 태그 이름과 기록 범위는 학습 코드에 따라 달라지므로, event에 없는 항목을 사후에 추정하지 않는다. 콘솔 로그는 seconds/iteration, FPS, collection/learning time, 경고와 발산 시점을 확인하는 데 필요하고, checkpoint 전체는 특정 시점 정책을 재평가하는 데 필요하다.

권장 export 단위:

```text
experiment_id/
├─ command.txt
├─ train_help.txt
├─ train_console.log
├─ code_hashes.txt
├─ system/
│  ├─ nvidia_smi_before.txt
│  ├─ nvidia_smi_during.csv
│  └─ nvidia_smi_after.txt
└─ logs/<run>/
   ├─ events.out.tfevents*
   ├─ env.yaml
   ├─ model_*.pt
   ├─ model_best.pt
   ├─ policy.pt
   ├─ policy.onnx
   ├─ report.html
   └─ videos/ 또는 play_video.mp4
```

실제 폴더명은 공식 코드가 생성한 구조를 보존한다. 파일을 골라 이동하거나 이름을 덮어쓰지 말고, 원본 run 디렉터리를 통째로 복사한 뒤 별도 manifest에 상대경로·bytes·SHA-256을 기록한다. credential이나 비밀값이 섞였는지는 외부 업로드 전에 별도로 점검한다.

비교할 최소 지표는 end-to-end 시간, 안정 구간 iteration 시간, mean reward/episode length의 시계열, terrain level, fall rate, tracking error, policy hash다. 성능 비교 실행은 같은 headless·렌더링 조건으로 고정한다. reward 변경은 이 동일-reward 장기 기준선 뒤에 한 번에 한 묶음만 적용한다.

## 아직 답이 필요한 질문

- 전체 로그에서 안정 구간의 실제 seconds/iteration과 FPS는 얼마인가?
- 동일 reward를 더 오래 학습할 때 terrain level과 fall rate가 언제부터 개선되는가?
- 300회 policy를 개인 evaluator가 명백한 실패 정책으로 일관되게 낮게 평가하는가?
- terrain generator seed가 `null`인 상태에서 같은 학습 seed의 실행 간 지형·성과 분산은 어느 정도인가?

## 파일 무결성

| 파일 | bytes | SHA-256 |
| --- | ---: | --- |
| `env.yaml` | 33,529 | `6e04eb361c49d3de8ff43c05f1a08434ae865b427ea5db446f5795b6916ff778` |
| `model_best.pt` | 7,151,403 | `b0bd703339adfe36a67fbf896f8e115b836c547c09a15c7628433635f81ce23d` |
| `report.html` | 12,796 | `4b2e225d79bfa3a03efde37a2ee02faec1569b82c6f21e377a4d5adaa57e2486` |
| `policy.pt` | 1,206,102 | `d4332260025926050c2fe38e410059bb78de84819f1d31c1ee2c3b0df689334d` |
| `policy.onnx` | 1,194,183 | `0ec4aa99a05922212516fe1021e82f933e156cd500438ae749b6e566085a22b3` |
| `play_video.mp4` | 3,071,312 | `caabfb3d84c3c6a11d3bc3e735e405c13e107d9d4f39ac5fcc39566a4ecd694a` |

일반 이름과 timestamp 별칭은 각각 같은 SHA-256이다. 이 중복은 다운로드 묶음의 원본 파일명을 보존하기 위한 것이며, 원본 저장소에서는 Git LFS가 동일 콘텐츠를 해시 기반 객체 하나로 관리한다.
