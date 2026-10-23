# H1 가설 재심사 산출물 — 2026-10-15

- `REPORT_H1_HYPOTHESES_20261015.md`: 한국어 보고서, 오늘 1순위와 예비 1개, 한계.
- `CANDIDATE_COMPARISON.csv`: 최대 3개 후보(새 action 중간강도 resume 포함); UTF-8 BOM, 표 헤더 영어/값 한국어.
- `calculations/targeted_check.py` / `targeted_numeric_checks.csv` / `verification.txt`: 첨부 **파생 CSV만** 검산한 CPU 작업.
- `evidence/`: 원본 ZIP 중 **실제로 참조한** 상태 수납/기존 보고서/preset/native 설명/파생 CSV의 변경 없는 사본.
- `EVIDENCE_INDEX.csv`: ZIP 안의 사본 원 경로·SHA256·크기. 참고로 이 출처의 다른 보고서와 본 보고서 사이에 겹치는 평가가 있으며 독립 증거로 중복 계수하지 않는다.

입력 ZIP SHA-256: `90842fc461a7d6c6c65a85ed4526110f6d38d64332c983d6819c38199eb05399`
기준 시간: 2026-10-15 KST. 입력 ZIP 외 다른 프로젝트·웹·서버 파일 미사용. 원 episode/MP4/native 학습 archive 미포함.
새 학습·평가·영상·export·서버 작업·Optuna trial·Run ID: **실행/생성 없음**.

검산 재현 (이 ZIP 압축 해제 후): `python calculations/targeted_check.py` — 일반 CPU Python 표준 라이브러리만 사용, 서버/GPU 불필요.
