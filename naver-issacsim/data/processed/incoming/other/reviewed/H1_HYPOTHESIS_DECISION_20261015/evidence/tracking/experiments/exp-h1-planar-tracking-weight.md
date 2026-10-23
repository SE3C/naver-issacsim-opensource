# exp-h1-planar-tracking-weight

## 2026-10-15 LINTRACK-065 fresh5K 심층 행동 판정 — HOLD

[보존된 제공 원문](../../../data/processed/incoming/other/reviewed/H1_LINTRACK-065_POLICY_ANALYSIS_20261015.md) · [통합 판정](../../../data/processed/experiments/h1/analysis/2026-10-15_H1_MODEL4650_LINTRACK065_POLICY_REVIEW.md). 이미 등록된 OFFICIAL fresh5K `20261014-081901-h1-lintrack-065-fresh5k`의 indexed `model_4950.pt` SHA `b7528923…ece`에 **외부 checkpoint index와 정책 SHA 기록**으로 연결되는 PERSONAL 6영상+camera-off 3,072 episode 보고서다. 이번 Git 작업에서 ZIP/MP4를 직접 재계산·재디코딩하지 않았다.

보고서는 **3,072/3,072 timeout 생존**, H1 body 비의도 전진 0.063m / world 순변위 0.171m, H2 전진 15.088m, H6 ±10° 전진 20.176/19.989m, H7 10.046m를 기록한다. 다만 **H3 횡왕복 world 최종 순변위 3.102m** (body `vy` 추종 오차가 작아도 world 복귀가 안 됨), rough H5 진행 평균/P05/최소 **8.995/8.411/7.943m**, 전체 혼합 tracking 0.17994이며 중앙 다단 계단 완주는 입증되지 않는다. `03_boxes.mp4`의 501/1000 검정 프레임은 짝수 프레임에 행동이 보이는 교대 **캡처 결함**으로 분리한다. **범용 정책 HOLD**이며 개인 평가 완료는 공식 채점이 아니다.

원문은 ZIP 내부 `source_run_id=null`로 학습 계보·reward를 단독 확인하지 못한다. 현재 Experiment의 OFFICIAL fresh/override 증명은 별도 학습 evidence에 기반한다. 우선 보존된 TERM-50 `model_2800` PERSONAL `scenario7` raw를 CPU로 비교하고 source/PPO·평가 설정·seed/cohort·지형 parity를 따로 표시한다. 새로운 학습·GPU 평가/영상·Optuna trial을 시작하지 않았다. 아래 ‘behavior assessment pending’은 이 보고서 수납 이전 기록이다.


## 2026-10-15 PERSONAL 사후 평가 완료

OFFICIAL Run `20261014-081901-h1-lintrack-065-fresh5k`의 `model_4950.pt`(SHA `b7528923eef5b1368ba2299f4e0538804ba00dd358049bfdff5027f448e31ece`)로 Windows 6영상 + full H1 scenario7 평가가 완료됐다. [평가 Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261015-exp-h1-planar-tracking-weight-model4950-video-eval). 원본 평가의 source_run_id는 null이며 외부 checkpoint SHA/index로 학습에 연결한다. 신규 학습/공식 점수/A/B 비교가 아니며 HOLD / 분석 대기. 아래 평가 대기는 과거 수납 시점 상태다.

- Robot: H1
- Status: **OFFICIAL training COMPLETED/PASS; policy behavior assessment pending** (received 2026-10-14)
- Baseline: frozen `h1-submit-2`
- Final reward override: `h1-submit-2 + lin=0.65`
- Experiment question: Does increasing only the planar linear-velocity tracking reward from 0.50 to 0.65 in a fresh 5K run improve commanded locomotion while retaining terrain and balance performance?

## Run

- Actual Run ID: `20261014-081901-h1-lintrack-065-fresh5k`
- Mode/operation: OFFICIAL / H1 / train / fresh; no parent or resume checkpoint.
- Environment: seed 42, 4096 environments.
- Iterations: 5000 requested; console reaches `Learning iteration 4999/5000`; metadata status completed, exit 0, evidence validation PASS.
- Native run directory: `/workspace/training/humanoid/logs/rsl_rl/humanoid/2026-10-14_17-19-07`.
- Resolved-config sources: nested archive `native_run/params/env.yaml`, `native_run/params/agent.yaml`, and `source/humanoid_rewards.py`. Verified reward values: `track_lin_vel_xy_exp=0.65`, `track_ang_vel_z_exp=0.5`, `feet_air_time=0.2`, `termination_penalty=-50`, `flat_orientation_l2=-1.5`, `ang_vel_xy_l2=-0.05`, `joint_deviation_hip=-0.2`, `joint_deviation_torso=-0.1`, `action_rate_l2=-0.0005`. The archive is the authority for complete resolved settings.
- Checkpoint lineage: fresh from iteration 0; `parent_run_id=null`, no source checkpoint. No policy evaluation or official submission is recorded.
- Source identity: the evidence reports the selected source files unchanged before/after the Run; an official source commit is not recorded.

## Evidence and current decision

- Canonical Originals directory: [`2026-10-14_171907_lintrack065_fresh5k`](https://github.com/SE3C/naver-issacsim-originals/tree/main/data/raw/official_server_runs/h1/2026-10-14_171907_lintrack065_fresh5k).
- OFFICIAL raw training Release: [official-h1-20261014-exp-h1-planar-tracking-weight-fresh5k](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261014-exp-h1-planar-tracking-weight-fresh5k).
- Received wrapper: 685,424,409 bytes, SHA-256 `61142daf19b260438360e7b517fb35a9a826f5d57196060d3eb4fce72a1c0bac`; nested evidence archive SHA-256 `e64da2230365bef6e07842bf81d206a0d2e3427d6dd378e1d8dc08000b9346f1` matches its embedded sidecar.
- **Decision: HOLD pending a behavior evaluation.** Training completion and validation do not establish policy quality, reward causality, a submission, or an official score. The related ACTRATE-parent `lin=0.65` resume Run is a separate experiment and lineage.
