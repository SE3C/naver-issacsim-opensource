# [분석] H1 joint tracking + 자세·고관절 완화 · PERSONAL model2850 · 6영상 + scenario7

Experiment `exp-h1-joint-tracking-posture-relaxation`; source OFFICIAL fresh3K Run `20261017-072659-h1-lintrack-065-angtrack-060-actrate-0003-orient`. 최종 설정은 `h1-submit-2 + action=-0.0003 + orientation=-1.0 + hip=-0.1 + ang=0.60 + lin=0.65`. [학습 Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261017-exp-h1-joint-tracking-posture-relaxation-fresh3k).

평가에 사용한 **model_2850.pt**, SHA256 `4a343750b47920d3b49e5e3ec7a3bf49fd9403d5b51a3727604971e6b7b0025d`는 공식 train checkpoint index와 일치한다. 최신 keeper2950은 다른 SHA이며 이 ZIP의 평가 대상이 아니다. 원시 평가 source_run_id=null은 보존하고 별도 manifest에 SHA 기반 연결을 기록했다.

Windows PERSONAL H1 camera-off scenario7 **COMPLETE/non-smoke**: 128env × seeds4201/4202/4203 ×8case =3072행. maneuver_push 6영상 각20초, H1 경사±10°. 원본 18파일 ZIP의 CRC 및 6개 영상 체크섬 확인 완료. 정책 품질 분석은 수행하지 않았다.

Assets: 받은 원본 ZIP, `.sha256`, `publication_manifest.json`. ZIP **36524950bytes**, SHA256 `af58e8f10165dbce7bd1c0363c09f523db925d9775870549819f94854fe4f6b9`. Canonical raw: Originals `data/raw/private_server_runs/h1/2026-10-17_windows_joint_tracking_posture_model2850_video_evaluation/`.

분석·채택 판단 대기/HOLD. PERSONAL 사후 평가이며 새 학습 Run·공식 점수·제출·A/B 비교가 아니다. Annotated tag는 게시 기록의 commit을 가리킨다. [Eval Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261017-exp-h1-joint-tracking-posture-relaxation-model2850-video-eval).
