# Go2 LINTRACK-125 · PERSONAL Windows · model_7050 · 6영상 + scenario7 평가

공식 서버에서 학습한 checkpoint를 **Windows PERSONAL 환경에서 사후 촬영·평가**한 결과입니다. 공식 학습 원본, 공식 점수 또는 제출 snapshot이 아닙니다. 새로운 학습 Run으로 등록하지 않습니다.

## 다운로드

- `model_7050_go2_6terrain_evaluation_20261004-030710_e8bd9e18.zip`: 필요한 영상·개별 평가 원자료를 모두 담은 원본 통합 ZIP. 34,310,566 bytes, SHA-256 `34d45711d121a4bb59a92b6424f2652eeb915ed4f6436d49070389eacc33d1e1`.
- 같은 파일명의 `.sha256`: 다운로드 무결성 확인.
- `publication_manifest.json`: 공식 학습 계보와 PERSONAL 평가 환경을 구분하는 출처 기록.

ZIP에는 6개 MP4, 영상 metadata 4개, `evaluation/` 원자료·diagnostics 7개, `BUNDLE_README.txt`까지 총 18개 파일이 있습니다. 영상은 stairs / inverted stairs / boxes / random rough / slope up 20° / slope down 20°이며 각 20초입니다. 별도 MP4·평가 파일을 중복 첨부하지 않습니다.

## 출처와 검증 범위

- Experiment: `exp-go2-planar-tracking-terrain-progression`; 표시 descriptor `LINTRACK-125`, legacy 검색 alias `G-001`.
- 공식 source Run: `20260929-154342-go2-lintrack-125-fresh7500-official`, fresh 7,500회 COMPLETE/PASS. [공식 training 원본 Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-go2-20260929-lintrack-125-fresh7500).
- 선택 checkpoint: automatic-best `model_7050.pt`, SHA-256 `d40f2666da6063c16c88353163115dcac1a2bd8b98011bf745543737a2188015`. 마지막 보존 checkpoint `model_7450.pt`와 구분합니다.
- 영상/평가 task checkout 및 이 annotated tag의 target: `ef10b7a4c9a83481346d446e8a75aed655f72214`.
- Windows 실행기·patched evaluator 재현 source: `SE3C/naver-issacsim-eval` commit `45368dacbbbd1a365d32b2a05fd58c093e5441a3`. 영상 생성 당시·평가 당시 파일 SHA는 ZIP 내부 기록을 따릅니다.
- 평가: camera-off deterministic scenario7, 128 env, seeds 4201/4202/4203, 9 case ×20초; COMPLETE, smoke=false, native exit 0. protocol `806d7e8280d8fac8bbbb6015013b1752335fe0446c8e39bf8f9dd4fbf7c145ad`.
- 기존 6영상 receipt를 재사용한 개별 full 평가입니다. 새 6영상 렌더와 full 평가를 한 invocation으로 실행했다는 주장이 아닙니다.
- A/B 리포트·calibration·공식 점수를 포함하지 않으며 reward-effect/adoption 판정을 변경하지 않습니다.
- 원본 ZIP의 출처·bytes·SHA·CRC/18개 파일을 확인했습니다. 내부 `source_run_id=null`은 그대로 보존하고 공식 학습 연결은 기존 분석과 checkpoint SHA 대응으로 별도 기록합니다.

canonical 개인 평가 ZIP은 `SE3C/naver-issacsim-originals/data/raw/private_server_runs/go2/2026-10-04_windows_model7050_video_evaluation/`에 보존합니다. 원본 ZIP·공식 training evidence·기존 Release·Downloads 파일은 수정하거나 삭제하지 않았습니다.
