# H1 ACTRATE 원자료 비교 결과 (2026-10-15)

## 내용

- `H1_ACTRATE_PARENT_UNCHANGED_RESTORATION_REPORT_20261015.md`: 한국어 최종 비교 보고서
- `csv/`: 직접 재집계한 정책/시나리오/케이스/평가 seed, H5 대응 episode, case paired delta, diagnostics 검산, source/checkpoint identity, MP4 디코드 감사
- `figures/`: H5 누적분포·평균/P05/최악·seed 일관성, case 혼합 tracking
- `video_contact_sheets/`: 고정 6영상의 동일 시각별 A/B/C early/late 샘플 프레임(원본 MP4는 포함하지 않음)
- `analyze_h1_cpu.py`, `inspect_h1_video_cpu.py`: CPU 재현 스크립트

## 재현

원래 받은 상위 통합 ZIP이 현재 디렉터리의 **외부**에 있다고 가정한다.

```bash
python analyze_h1_cpu.py --input '/path/to/H1_ACTRATE_PARENT_CONTINUATION_COMPARISON_20261015.zip' --output '/path/to/new_result'
```

의존성: `pandas`, `numpy`, `matplotlib`. 이 명령은 원본 상위 ZIP을 변경하지 않고 nested ZIP의 CRC, 내부 SHA256SUMS, checksum, 평가 raw와 diagnostics를 대조하고 CSV·PNG를 만든다. 실제 분석에서 통합 평가 9,216행과 checksum 검증을 완료했다.

영상 재분석은 **원래 세 내부 통합 ZIP의 MP4만** A/B/C 하위 폴더에 추출(원본 보존)한 다음:

```bash
python inspect_h1_video_cpu.py --extracted-root /path/to/A_B_C_root --output /path/to/contact_sheets
```

의존성: `opencv-python`, `Pillow`, `numpy`. A=`model_2700`, B=`unchanged-cont2k_model_4699`, C=`return2700-2k_model_4650`. 추출 구조: `A/01_stairs.mp4` ... `A/06_slope_down_10deg.mp4`, B/C도 동일. 모든 MP4에서 1,000프레임을 순차 디코드하고 black-frame parity를 검사한 뒤 정해진 시각의 근접 유효 프레임을 contact sheet에 배치한다. 실제 분석에서는 18개 영상의 CPU 전체 디코딩을 진행했다.

명령들은 예시이며 서버/Isaac Sim/GPU/학습·재렌더 프로세스를 호출하지 않는다. 결과는 PERSONAL Windows 평가의 관찰이며 공식 점수·동일 물리 궤적·인과 분석으로 환산하지 않는다.
