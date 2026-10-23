# H1 추가 가설 탐색 전달 자료

2026-10-15 현재 보존 자료로 다음 학습 질문을 좁히는 **새 외주 분석 세션용**이다. 파일명은 `H1_NEW_SESSION_HYPOTHESES_20261015.zip`, 함께 보낼 TXT는 `H1_새세션_가설탐색_프롬프트_20261015.txt`다. 이전 대화 맥락을 전제하지 않는다. 새로운 학습·평가·채택 기록이 아니다. **기존 Optuna 분석 세션에서 이어가는 도구 개선과는 별개**이며 기존 lin=.55 resume / action=-.0003 fresh 권고를 확정 계획으로 바꾸지 않는다.

## 읽는 순서와 구성

1. `curated/`: 최신 다음 가설, 부모/무변경/복원, 4정책 및 fresh 조합 수납 문서. 날짜가 오래된 원문과 상태가 다르면 최신 수납 문서의 한정된 판단을 먼저 확인한다.
2. `sources/`: 원문 보고서와 기존 파생 CSV. `next_hypothesis/`와 `parent_comparison/`은 같은 원 평가의 일부를 재사용하므로 독립 반복이 아니다. 첨부 CPU 스크립트는 원문 보존 자료이며 실행 지시가 아니다.
3. `tracking/`: registry·관련 Experiment와 미실행 계획 사본. registry의 날짜별 과거 상태를 현재 상태로 오독하지 않는다. 새 H/HS 번호는 발급하지 않는다.
4. `presets/`: h1-submit-2/4/6 native env·agent snapshot. 이것만으로 각 실제 Run의 source/PPO/최종 reward가 모두 동일하다고 보증하지 않는다.
5. `reference/06_HUMANOID_TRAINING_CODE.md`: reward·학습 코드 설명. 전달 자료 밖의 링크는 자동으로 읽은 자료가 아니며, 확인 불가능한 값은 추정하지 않는다.

원문과 CSV는 수정하지 않고 복사한다. 패킷 경로 재배치로 원문 내부의 저장소 상대링크 일부는 동작하지 않을 수 있다. `INPUT_FILES.json`이 실제 포함 파일과 원본 저장소 상대경로·크기를 기록한다.

## 중요한 구분

- ACTRATE 부모2700 SHA `e54d3389…`와 후기2950 SHA `d4fa7221…`는 다른 정책이다.
- lin=.65 resume4650 SHA `ce7ad586…`와 action 복원4650 SHA `a8249db4…`는 다르다.
- 무변경4699 SHA `722b35a1…`의 rough 진행 손실은 기존 결과다. 동일 비교를 다시 미실행으로 제안하지 않는다.
- 현재 권고 lin=.55/action=-.0001 +2K와 action=-.0003 fresh3K는 미선택 후보다. 더 나은 새 후보가 없으면 유지해도 된다.
- 전체 episode 원자료·MP4·native 학습 archive·checkpoint는 포함하지 않는다. 보고서·파생 CSV 분석을 raw 전수 재검증으로 표현하지 않는다. 공식 점수 추정이나 임의 scalar objective는 범위 밖이다.

## 반환 형식

함께 전달한 TXT 프롬프트에 따라 한국어 보고서·후보 비교표·새 계산 산출물 전체를 **단일 ZIP**으로 받는다. 이번 준비 자체는 사용자에게 실행을 권고하는 최종 결론이나 GPU 실행 승인이 아니다.
