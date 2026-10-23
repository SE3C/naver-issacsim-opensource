# [분석] H1 joint tracking + 자세·고관절 완화 model2850 — Windows PERSONAL

OFFICIAL fresh3K Run `20261017-072659-h1-lintrack-065-angtrack-060-actrate-0003-orient`의 **model_2850.pt**, SHA256 `4a343750b47920d3b49e5e3ec7a3bf49fd9403d5b51a3727604971e6b7b0025d`와 학습 checkpoint index로 연결한다. 최신 keeper2950과는 다른 정책이다. 학습 원본은 `data/raw/official_server_runs/h1/2026-10-17_072659_joint_tracking_posture_fresh3k/`에 있다.

`evidence_archives/`의 원본 ZIP은 **36524950bytes**, SHA256 `af58e8f10165dbce7bd1c0363c09f523db925d9775870549819f94854fe4f6b9`. 18파일·CRC·6 MP4 체크섬 확인 완료. Windows PERSONAL H1 camera-off scenario7 **COMPLETE/non-smoke**, 128env × seeds4201/4202/4203 ×8case =3072행. 6영상은 maneuver_push 각20초, H1 경사±10°. 평가와 영상은 별도 실행이다.

추출한 `evaluation_manifest.json`, `video_evaluation_link.json`은 받은 바이트 그대로 보존한다. 원시 source_run_id=null을 편집하지 않고 별도 publication manifest에 SHA 근거 연결을 기록했다. 행동 분석·정책 채택은 대기/HOLD이며 공식 점수·제출·A/B 비교가 아니다.

[Eval Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261017-exp-h1-joint-tracking-posture-relaxation-model2850-video-eval) · [게시 기록](https://github.com/SE3C/naver-issacsim-eval/tree/main/publications/2026-10-17_h1_joint_tracking_posture_model2850). 이번 보존·게시 중 GPU 작업을 실행하지 않았다.
