# Go2 model_7050 — PERSONAL Windows 영상·평가 원본

받은 통합 ZIP을 재압축·rename·내부 수정 없이 보존한다. 공식 학습 Run `20260929-154342-go2-lintrack-125-fresh7500-official`의 automatic-best `model_7050.pt`를 Windows PERSONAL에서 촬영·평가한 자료다. terminal `model_7450.pt` 평가가 아니며, 추가 학습 Run·공식 점수·제출 snapshot이 아니다.

- 원본: `model_7050_go2_6terrain_evaluation_20261004-030710_e8bd9e18.zip`
- 크기: 34,310,566 bytes
- SHA-256: `34d45711d121a4bb59a92b6424f2652eeb915ed4f6436d49070389eacc33d1e1`
- 검증: 기존 통합 ZIP 기록과 SHA/크기 일치, ZIP CRC PASS, 18개 파일, 영상·평가 checkpoint SHA 일치, 평가 manifest COMPLETE/full/camera-off 확인.
- 구성: MP4 6개 + 영상 metadata 4개 + `evaluation/` 원자료·diagnostics 7개 + `BUNDLE_README.txt`.
- 평가: scenario7, 128 env × seed 4201/4202/4203 × 9 case × 20초. 기존 6영상 receipt를 재사용했다. A/B 리포트·calibration·공식 점수는 포함하지 않는다.
- 별도 `publication_manifest.json`은 게시 출처를 설명한다. 원본 내부 manifest의 `source_run_id=null`을 수정하지 않으며, 학습 계보는 기존 분석·공식 Release의 checkpoint SHA 대응에 근거한다.
- 배포: [PERSONAL Windows Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-go2-20261004-exp-go2-planar-tracking-terrain-progression-model7050-video-eval).

원본 공식 training archive와 개인 평가 ZIP을 혼합하거나 서로 대체하지 않는다. 사용자의 Downloads 원본도 그대로 유지한다.
