# [학습] H1 joint tracking + 자세·고관절 완화 — OFFICIAL fresh3K

Experiment `exp-h1-joint-tracking-posture-relaxation`; 사용자 후보 2번의 실제 Run `20261017-072659-h1-lintrack-065-angtrack-060-actrate-0003-orient`. 최종 override는 `h1-submit-2 + action=-0.0003 + orientation=-1.0 + hip=-0.1 + ang=0.60 + lin=0.65`. 전체 resolved config는 받은 archive와 추출한 `env.yaml`, `agent.yaml`, `humanoid_rewards.py`에 보존한다.

OFFICIAL **COMPLETED / exit 0 / validation PASS**, fresh/no parent, seed42, 4096env, 3000회 요청, console2999/3000, save_interval50. UTC `2026-10-17T07:26:59.814138+00:00`–`2026-10-17T08:03:36.921214+00:00`. Native Run `/workspace/training/humanoid/logs/rsl_rl/humanoid/2026-10-17_16-27-05`. Finalize와 공식 backup 성공, organizer checkpoint60개 보존. 실행 전후 task-source identity가 같고 `changed_during_run=false`다. 캡처 commit `3e73d6dd79080fd7632488c061052a6edd52e230`은 IsaacLab 기록으로 취급하며 별도 task-source revision이라고 확장하지 않는다.

확인한 활성 주요 weight: lin=.65, ang=.60, feet=.20, termination=-50, orientation=-1.0, angxy=-.05, hip=-.1, torso=-.1, action=-.0003. 나머지 reward는 h1-submit-2와 일치한다. 다른 전체 설정은 resolved config를 따른다.

- 평가에 사용한 **model_2850.pt** SHA256 `4a343750b47920d3b49e5e3ec7a3bf49fd9403d5b51a3727604971e6b7b0025d`: native `.../2026-10-17_16-27-05/model_2850.pt`와 organizer `backup_log/2026-10-17_16-27-05/model_2850.pt`가 모두 인덱스에 있다. 자동 best의 reward event iteration2840과 파일 번호2850은 별개다.
- 최신 keeper **model_2950.pt** SHA256 `c342e995ec77a2fb5f2845778d4e85146a244a4b4e311c29fe6f4275c539c216`: `/workspace/training/humanoid/backup_log/2026-10-17_16-27-05/model_2950.pt`. 평가 ZIP은 이 최신 keeper가 아닌 2850의 결과다.

원본 `evidence_archives/20261017-072659-h1-lintrack-065-angtrack-060-actrate-0003-orient-download.tar.gz`: **418915262 bytes**, SHA256 `be11dd838a3991f059b805477f015a9134831fc242d93b46960976214612e83c`. 내부 학습 archive412384068bytes SHA256 `a8fa4b708681355617fd548a8760234489526651ad1a348b4297c5d08c49c60f`는 받은 sidecar와 일치했다. 원본 archive는 수정·재압축하지 않았다. Console, TensorBoard, source와 모든 checkpoint는 archive에 남아 있다.

[학습 Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261017-exp-h1-joint-tracking-posture-relaxation-fresh3k). Annotated tag는 이 보존 기록의 commit을 가리키며 학습 source commit이 아니다. 별도 [Windows PERSONAL 평가](../../../private_server_runs/h1/2026-10-17_windows_joint_tracking_posture_model2850_video_evaluation/README.md)는 정상 완료했다. 정책 분석·채택은 대기/HOLD이며 제출·공식 점수는 없다.
