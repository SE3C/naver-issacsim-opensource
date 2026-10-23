# 재현 방법

1. 사용자가 보존한 원래 6영상+camera-off 통합 ZIP을 별도 작업 폴더에 안전하게 추출한다. 원본 파일은 변경하지 않는다.
2. 필요한 CPU 패키지: `pandas`, `numpy`. `scripts/analyze_episodes.py`의 입력은 `evaluation/episodes.jsonl`이다.
3. 실행 예시: `python scripts/analyze_episodes.py /path/to/extracted/evaluation/episodes.jsonl --out /path/to/output`.
4. `scripts/video_probe.py`는 **원본 MP4 6개가 놓인 분석 작업 디렉터리**를 필요로 한다. `opencv-python`, `Pillow`, `numpy`가 있을 때 `python scripts/video_probe.py /path/to/extracted --out /path/to/video_probe_output`로 실행한다. 출력은 비디오 전체 프레임의 기초 밝기/검정 검사와 키프레임 montage이며, **연속 행동 추적 알고리즘이 아니다**.
5. `derived/*.csv`와 `derived/summary.json`은 원본 평가 원자료에서 재계산한 수치다. `derived/video_probe.json`은 MP4 전체 프레임 디코딩을 통한 기초 검사다. `figures/`는 보고서용 플롯, `video_keyframes/`는 비디오의 선택된 프레임이고 원본 비디오를 대체하지 않는다.
6. 이전 TERM50/ACTRATE 참고 집계와 과거 공식 점수는 **이번 ZIP에서 재계산한 결과가 아니다**. 단일 Markdown 보고서 안의 GitHub 출처를 참조한다.
