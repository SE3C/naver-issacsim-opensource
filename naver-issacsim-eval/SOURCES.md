# 설계 근거와 확인 범위 — 2026-10-02

2026-10-12 게시 분류 변경: 새 Windows PC 통합 영상·평가 Release는 이 저장소에 게시한다. 기존 NVIDIA Release는 보존한다. 실행기가 자동 publish하지 않는다는 아래 구현 경계는 그대로다. 게시 기록 tag와 실제 source provenance의 구분은 [EVALUATION_RELEASES.md](EVALUATION_RELEASES.md)를 따른다.

이번 구현은 전달받은 `se3c_policy_evaluator_v0.zip`와 `HANDOFF.md`, 현재 네 저장소의 source/운영 경계/평가 기록을 검토해 만들었다. 다음 경로는 workspace 기준이며 원문 파일은 변경하지 않았다.

| 근거 | 구현에 반영한 내용 |
| --- | --- |
| `naver-issacsim/data/processed/reference/regulations/2026_source_snapshots/2026-09-21_preliminary_regulations/preliminary_regulations_2026-09-21.html` | H1·Go2 공개 7시나리오와 가중치. 내부 0–100점으로 표시하고 공식 자동평가 70점/리포트 30점으로 환산하지 않음 |
| `naver-issacsim/data/processed/incoming/other/reviewed/01_운영진_자동평가_Tracking_Survival_공개답변_20260926.md` | body-frame 3축 동일 비중, step→episode→episode 동일가중 평균, 반복 낙상마다 실패 episode, timeout·평가 종료 진행 episode는 생존 |
| `naver-issacsim/data/processed/experiments/go2/2026-09-15_GO2_G-005_FIXED_EVAL_SEED4201_D1.md` | first episode20s·seed4201·6지형·deterministic inference 전례, survival와 traversal의 구분. 과거 4800·4900은 안정성/진행성 trade-off이며 calibration 정답이 아님 |
| `naver-issacsim/data/processed/ai_library/10_SOLUTION_AND_VALIDATION_BLUEPRINTS.md`, `16_EXPERIMENT_EXPORT_AND_TENSORBOARD.md`, `20_H1_PUBLIC_FAILURES_AND_EXPERIMENT_PRIORS.md` | camera 없는 headless 사후 평가, 정체·진동·보행 품질 진단, 공개 실패 표본의 선택편향과 인과 해석 제한 |
| `naver-issacsim/research/EXPERIMENTS.md`, `EXPERIMENT_NAMING.md` | preset/Experiment/Run/lineage 분리. 파일명이나 legacy H/G alias로 출처·completion을 추론하지 않음 |
| `naver-issacsim-nvidia/CURRENT_SOURCE.md`, `training/{humanoid,quadruped}/*_task/{env_cfg.py,agent_cfg.py,__init__.py}` | 실제 task 등록·RSL agent 구성, 현재 task source를 읽기만 함. reward/config/공식 train/play/finalize 수정 없음 |
| `naver-issacsim/data/processed/ai_library/17_ISSACSIMZ_VIDEO_OPERATIONS.md`와 H1 6-terrain 보존 분석 | H1 고정 6지형은 Go2와 같은 terrain 종류를 쓰되 slope up/down은 10°(`0.176326981`)로 구분. Windows H1 통합 launcher의 qualitative video 계약 근거 |
| `naver-issacsim-originals/data/raw/server_backup/extracted/training/` | 보존 공식 snapshot은 비교 근거이며 현재 executable source와 동일하다고 자동 가정하지 않음 |
| `issacsimz/scripts/python_runner.sh`, provenance·archive 관련 source | Python 명령을 하드코딩하지 않고 IsaacLab launcher 사용. 기존 evidence/다운로드 산출물에 쓰거나 publish하지 않는 별도 사후 평가 결과 |

상류 API도 확인했다. [IsaacLab ManagerBasedRLEnv v2.2.1](https://github.com/isaac-sim/IsaacLab/blob/v2.2.1/source/isaaclab/isaaclab/envs/manager_based_rl_env.py)은 termination을 계산한 뒤 reset하므로 종료 step 수치는 reset 전에 수집해야 한다. [TerminationManager](https://github.com/isaac-sim/IsaacLab/blob/v2.2.1/source/isaaclab/isaaclab/managers/termination_manager.py)의 terminated/time_outs를 분리해 낙상과 시간초과가 동시에 발생하면 실패를 우선한다. [native RSL play](https://github.com/isaac-sim/IsaacLab/blob/v2.2.1/scripts/reinforcement_learning/rsl_rl/play.py)의 inference 경로와 [RSL-RL runner](https://github.com/leggedrobotics/rsl_rl/blob/v2.3.1/rsl_rl/runners/on_policy_runner.py)의 checkpoint load를 참고했다. 현재 사용자 설치 버전이 이 tag와 같다고 가정하지 않으며 실제 package 버전과 runtime config를 기록한다.

공식 command 값·error→score 함수·최종 시나리오 내부 물리설정은 미확인이다. 내부 suite의 command·20초 horizon·지형 난이도·push·randomization 설정은 공개 근거를 참고한 우리 자체 정의다. WSL camera-off 실측·처리량 최적값·official score 상관 calibration은 아직 확인하지 않았다.

신규 RSL-RL의 actor/critic·TensorDict 경로는 [RSL-RL v5.0.1 runner](https://github.com/leggedrobotics/rsl_rl/blob/v5.0.1/rsl_rl/runners/on_policy_runner.py)와 [PPO loader](https://github.com/leggedrobotics/rsl_rl/blob/v5.0.1/rsl_rl/algorithms/ppo.py)를 함께 확인했다. `load_cfg`와 기존 `load_optimizer=False`를 구분하며 호환되지 않는 task config를 임의 변환하지 않는다. checkpoint 내부 optimizer는 불러오지 않고 학습/update도 호출하지 않는다.


2026-10-04 Windows H1 확장은 기존 H1 collector/scorer 계산을 바꾸지 않고 Go2와 동일한 설치·ASCII staging·video/evaluation linkage·18-entry packaging 구조만 추가했다. 실제 H1 GPU smoke/full evidence는 아직 없으므로 source 구현과 runtime 검증을 구분한다.
