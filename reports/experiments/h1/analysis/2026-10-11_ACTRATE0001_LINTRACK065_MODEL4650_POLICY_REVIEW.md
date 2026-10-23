> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/experiments/h1/analysis/2026-10-11_ACTRATE0001_LINTRACK065_MODEL4650_POLICY_REVIEW.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# [분석] ACTRATE-0001 → lin=0.65 / model_4650 정책 검토 — HOLD

> 관리 안내 (2026-10-13): **분석** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](<../../../../research/EXPERIMENTS.md>)를 확인한다.

- Experiment: [exp-h1-action-first-planar-tracking-switch](<../../../../research/experiments/h1/exp-h1-action-first-planar-tracking-switch.md>).
- OFFICIAL Run: `20261010-154926-h1-actrate0001-lintrack065-from2700-plus2k`, imported parent `model_2700.pt`에서 +2000, console 4699/4700, exit0, validation PASS. `h1-submit-2 + lin=0.65 + action=-0.0001`, seed42/4096 env/save50. 학습 완료와 정책 승격은 별개다.
- 선택 checkpoint: 최신 keeper `model_4650.pt`, SHA `ce7ad58657f3dd744e7cf2b7531f3d7d455773dfc6fb135f39d8a55aa49dea70`; automatic best `model_2900.pt`와 다르다.
- [사용자 분석 원문](<../../../received/H1_MODEL4650_POLICY_ANALYSIS_20261011.md>)은 byte-for-byte 보존(SHA `f532c3cf5ebb351bb8b9b335b0be36e2b268bb5470f73cb0d01f23d51818db4d`). 원본·Release 수납〔원본 참조: `../../../operations/windows_h1_video_evaluation/2026-10-11_ACTRATE0001_LINTRACK065_MODEL4650_PUBLICATION.md` / 공개 사본 미포함〕.

## 계보와 분석 범위

보고서의 `preset=null/source_run_id=null`, 학습 계보 미확인은 **입력 평가 ZIP 단독의 한계**다. 별도 확인된 OFFICIAL train checkpoint index의 model4650 SHA와 ZIP SHA가 일치하며, 부모 model2700 SHA `e54d3389e20ea913968ef8d3edbea5004368ff225fa6b94f73fcd91cf93ca7ae`는 기존 OFFICIAL ACTRATE-0001 Run과 일치한다. 원문·ZIP·학습 metadata의 `user_imported_checkpoint`, provenance=false/unknown, parent_run_id=null은 수정하지 않고 이 외부 연결을 별도로 기록한다. OFFICIAL source Git commit은 미확인이고 평가 task commit을 대신 쓰지 않는다.

## 확인된 결과

기존 ZIP의 `episodes.jsonl`을 CPU로 읽어 핵심 수치만 재확인했다. 영상은 이번 수납에서 다시 디코딩하지 않았으며 프레임 관찰은 수신 보고서의 판단이다. 신규 GPU 학습/평가를 실행하지 않았다.

| 축 | 결과와 의미 |
| --- | --- |
| 평가 완료 | PERSONAL scenario7 8 case × 3 seed × 128 env = 3,072개 고유 episode; 전부 20초 timeout 생존, base-contact failure 0 |
| H2 전진 / H7 push | body-frame 전진 적분 평균 14.812m / 9.757m (명령 적분 15m / 10m). 비낙상과 실제 전진 모두 관찰되나 밀침 직후 회복시간은 미측정 |
| H1 정지 / H3 횡왕복 | H1 비의도 body 전진 +0.108m, world XY 순변위 평균 0.228m. H3 body 전진 -0.044m여도 world XY 잔류 순변위 평균 2.398m; 횡왕복 후 위치 복귀 성공 아님 |
| H4 회전 | yaw 평균 절대오차 0.179rad/s; 선속도만 좋아도 회전 명령 비용이 남음 |
| H5 rough | body 전진 평균/P05/최소 9.546/9.228/8.974m; tracking 평균/P95 .18466/.20873. P05/P95는 보고서 값이며 낙상보다 진행·추종 꼬리가 약점 |
| 전체 혼합 tracking | .17048은 8 case episode 동일가중 내부 오차 평균. 7 scenario 가중 공식 점수 또는 단일 물리 단위가 아님 |
| 영상 | 보고서는 전진·지형 접촉을 확인했으나 계단 중앙 다단 완주·boxes 정량 성공은 미입증. 초기 검정 1프레임은 캡처 artifact이며 홀짝 교대 검정은 보고되지 않음 |

**판정: HOLD.** 전진·경사·push 보행의 내부 후보로 보존하되 범용 대표/제출 정책으로 PROMOTE하지 않는다. 이번 분석은 수납 완료이며 성능 판단을 더 이상 “보고서 대기”로 표시하지 않는다. matched 비교·reward 인과·제출 성능은 미확인이다.

## 비교 우선순위

기존 ACTRATE-0001/model2700에 대한 보고서 참고값은 raw matched A/B가 아니다. 정지/비의도 전진 누수 감소와 rough 진행·혼합 tracking·자세 비용 악화의 동시 신호만 기록한다. 보존된 부모 평가 raw의 protocol/source/PPO/command/terrain/reset/seed/horizon을 대조하고 최초 cohort key를 대응시키는 CPU 비교가 다음 단계다. 학습량과 resume 효과가 섞이므로 보상 인과를 판별하려면 같은 model2700에서 reward unchanged +2K control이 필요하지만 현재 확인된 완료 자료는 없고 새 학습을 자동 실행하지 않는다.
