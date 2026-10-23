# 2026-09-27 H1 PERSONAL: fresh 설정 비교와 H-005 장기 확인 계획

상태: **사전 계획 기록**. 세 Run은 이후 PERSONAL에서 완료됐으며 실제 evidence·실패한 첫 resume 시도·세 비교 입력은 [2026-09-27 수신 기록](../../experiments/h1/2026-09-27_H1_FRESH_AND_CONTINUATION_EVIDENCE_INTAKE.md)에 별도로 정리했다. 아래는 실행 전 질문과 판정 경계를 보존한 것으로, evaluator 결과나 내일 OFFICIAL 설정 채택을 보고하지 않는다. 현재 판단과 Run 계보는 [실험 registry](../../../../research/EXPERIMENTS.md), [H-005](../../../../research/experiments/h1/H-005.md), [H-010](../../../../research/experiments/h1/H-010.md)를 기준으로 한다.

## 범위와 순서

| 순서 | Run | 시작점 | 목표 reward 핵심 | 요청 길이 | 목적 |
| --- | --- | --- | --- | --- | --- |
| 1 | H-005 Run 03 | checkpoint 없는 fresh | TERM `-50`, track-lin `0.5`, feet `0.25` | 0→3K | H-005 설정을 처음부터 학습한 결과 |
| 2 | H-010 Run 03 | checkpoint 없는 fresh | TERM `-50`, track-lin `0.75`, feet `0.25` | 0→3K | H-005 fresh와 track 설정 비교 |
| 3 | H-005 Run 04 | corrected H-005 Run 02 final `model_2998.pt` | Run 02 reward 그대로 | +2K, 목표 global 5K | 기존 H-005의 후반 안정성 |

`fresh`는 **checkpoint를 불러오지 않고 iteration 0부터 시작한다는 뜻**이지 BASE reward로 되돌린다는 뜻이 아니다. H-010 Run 03은 기존 H-008에서 상속한 `track_lin_vel_xy_exp=0.75`와 `feet_air_time=0.25`를 시작부터 함께 적용한다. 세 핵심 값 외의 실제 effective reward 전체와 PPO/source 설정은 실행 전에 기존 corrected 설정과 대조해야 한다. H-005 Run 04는 reward를 하나도 바꾸지 않는다. 세 Run 모두 PERSONAL이며 H-012·Go2·새 reward 분기는 오늘 범위 밖이다.

## 실행 경계

- Brev 기본 Setup Script 완료만으로 `issacsimz`·NVIDIA checkout이나 personal bootstrap `READY`가 있다고 가정하지 않는다. 첫 접속이면 공개 sidecar clone → personal bootstrap → 비공개 training checkout 준비와 두 doctor `READY`를 먼저 확인한다. 재접속이면 실제 checkout 존재와 로컬 변경을 확인하고 fast-forward만 허용한다. 이 단계가 끝나야 reward/run 점검을 한다.
- H-005 Run 04의 parent는 **corrected Run 02** final `model_2998.pt`다. historical Run 01이나 자동 `model_best.pt`를 파일명만 보고 대신 쓰지 않는다. 실제 source path와 SHA-256을 학습 전에 확인해 기록한다. 이 계획 문서는 확인되지 않은 SHA를 새로 단정하지 않는다.
- 가능한 한 fresh pair의 seed=42, envs=4096, source commit, PPO 설정, simulator/Isaac Lab, headless 조건을 같게 한다. 세 Run 모두 실제 실행 명령·effective reward·resume 여부를 evidence에서 확인한다. 같은 seed는 동일 terrain·command 순서를 보증하지 않는다.
- 장기 학습은 PERSONAL mode-aware tmux wrapper를 사용한다. 1K는 추세 확인이며 작은 열세만으로 유망 후보를 REJECT하지 않는다. 치명 오류 또는 명확한 붕괴는 중단·보존·조사한다. 실행 실패·validation FAIL도 원본 evidence/archive를 지우지 않는다.
- Run별 console/exit, TensorBoard, source·reward/config identity, numbered/final checkpoint, archive/validation을 보존한다. H-005 Run 04는 source checkpoint SHA와 실제 resume 계보를 반드시 연결한다. final filename이나 global endpoint는 미리 확정하지 않는다. 긴 resume의 대표 정책은 후반 terrain·tracking·낙상이 함께 뚜렷하게 악화되지 않는 한 final numbered checkpoint가 기본이다.

## 사전 지정 비교와 판정 한계

1. **H-005 Run 03 fresh vs H-010 Run 03 fresh:** 동일 조건을 확인한 후 `track-lin 0.5`와 `0.75`의 **전체 설정**을 비교한다. 둘 다 feet `0.25`이지만 다른 reward/PPO 값까지 동일하다는 것은 실제 config 검증 전에는 가정하지 않는다. 내일 OFFICIAL fresh reward 후보 선정의 1차 질문이다.
2. **H-005 Run 03 fresh vs 기존 corrected H-005 Run 02:** 처음부터 feet `0.25`를 쓰는 경로와 corrected H-001 1.5K parent에서 H-005로 바꿔 3K까지 가는 경로를 비교한다. 동일 reward 항의 독립적 인과효과 실험이 아니라 **학습 경로 비교**다.
3. **corrected H-005 Run 02 3K vs Run 04 5K:** 같은 계보의 장기 유지·악화 여부를 본다. 오늘 H-001 unchanged 3K→5K control은 없으므로 “H-005 reward가 5K에서 control보다 우월하다”는 결론은 낼 수 없다.

Training reward나 XY 하나로 승자를 정하지 않는다. terrain progression, XY/yaw, base-contact/fall, 실제 전진·stall과 자세를 분리해서 본다. 가능하면 기존의 동일 command/terrain/seed fixed evaluator로 fresh pair를 직접 비교하고, 시간이 허락하면 이미 보존된 corrected H-010 5K와 H-008 unchanged 5K를 **새 학습 없는 reference**로 추가한다. 동일 evaluator가 없거나 조건이 맞지 않으면 paired 성능·공식 점수·채택을 주장하지 않는다. 6지형 영상은 필요한 후보를 고른 뒤 정성 확인에 사용하며 fixed evaluator를 대신하지 않는다.

오늘 PERSONAL 결과는 내일 OFFICIAL에서 **어떤 reward configuration을 fresh로 시험할지** 고르는 근거일 뿐이다. PERSONAL checkpoint나 정책을 공식 제출 계보로 넘기지 않는다. 세 Run의 완료·Release·실제 수치와 결정은 수신 evidence를 검증한 뒤에만 registry와 분석에 추가한다.
