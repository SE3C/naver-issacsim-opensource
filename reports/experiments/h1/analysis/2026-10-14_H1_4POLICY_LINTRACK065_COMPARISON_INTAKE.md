> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/experiments/h1/analysis/2026-10-14_H1_4POLICY_LINTRACK065_COMPARISON_INTAKE.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# H1 4정책 LINTRACK-065 비교 — 수신·검토 기록

## 2026-10-15 상태 정정 — 기존 CSV 비교 완료와 인과 검증 구분

이 파일의 **2026-10-14 CPU 4정책 비교는 ACTRATE-0001 부모에서 `lin=.65`로 바꾼 resume `model_4650`(SHA `ce7ad586…9dea70`)의 역사적 결과**다. **2026-10-15 새 ACTION 복원 `model_4650`(SHA `a8249db4…25b84ea`)과 다른 정책**이며, 새로운 LINTRACK-065 **fresh5K `model_4950`(SHA `b7528923…f448e31ece`)과도 별개다. [두 신규 원문 수납·정책 판정](<2026-10-15_H1_MODEL4650_LINTRACK065_POLICY_REVIEW.md>)은 두 후속 PERSONAL 평가를 각각 HOLD로 분류한다. 이 파일의 9.546m rough 및 H3 2.398m는 **옛 lin=.65 resume 4650만의 수치**이며, ACTION 복원 4650의 rough 8.769m/H3 0.167m나 fresh4950의 rough 8.995m/H3 3.102m를 덮어쓰지 않는다.

동일 부모 **reward-unchanged +2K `model_4699`의 PERSONAL 영상·scenario7 full 평가도 2026-10-15 완료**됐으며 [Experiment 연결](<../../../../research/experiments/h1/exp-h1-action-rate-relaxation.md>)에 수납돼 있다. [다음 가설 보고서](<2026-10-15_H1_NEXT_HYPOTHESIS_DECISION_INTAKE.md>)에서 **기존 lin=.65 resume4650 대 4699의 파생 CSV 교차 비교도 완료**됐다. rough 진행 이득과 yaw/횡잔류 비용이 공존해 HOLD다. 원 episode 직접 재집계와 checkpoint 선택 통제·reward 인과 검증은 별개로 미확정이다. 아래 원문의 'control 없음/행동 평가 대기'는 원래 보고서 수납 시점의 서술이므로 새로운 학습을 다시 제안하지 않는다.

2026-10-14 사용자 제공 CPU 분석 번들 수납. 신규 학습·영상·GPU 평가가 아니라 기존 Windows PERSONAL camera-off 평가의 비교 보고서다.

- [보고서 원문](<../../../received/H1_4policy_LINTRACK065_review_20261014.md>)은 ZIP 내부 bytes 그대로 보존한다.
- [보존 ZIP](https://github.com/SE3C/naver-issacsim-originals/blob/main/data/raw/external_analysis/h1/2026-10-14_lintrack065_four_policy_analysis/H1_4policy_LINTRACK065_analysis_bundle_20261014.zip): 원문·CSV·재집계 코드·프로토콜·이미지 포함, 433,962 bytes, SHA-256 `95f7257f366bf2b5636584317e6eceea6ed5aedf924fd01241acc2779950c917`, Originals 보존/push commit `24aeb98f2137b2e4aeed92ea82be4a8293fd642f`. 분석 산출물이며 OFFICIAL 학습 archive가 아니다.
- 정책: TERM-50 fresh3K `model_2800`, ACTRATE-0001 fresh3K 부모 `model_2700`, ACTRATE-0001 fresh10K `model_9999`, 부모2700에서 lin=.65로 +2K resume한 `model_4650`. 각각 별도 checkpoint/학습 계보다. 2800은 실제 Round-2 제출 정책이 아니며 9999는 2700의 연장 Run이 아니다.
- 외부 학습 연결: [ACTRATE Experiment](<../../../../research/experiments/h1/exp-h1-action-rate-relaxation.md>), [LINTRACK 전환 Experiment](<../../../../research/experiments/h1/exp-h1-action-first-planar-tracking-switch.md>). 평가 ZIP 내부 null identity와 OFFICIAL 학습 연결을 구분한다.

## 확인된 핵심과 경계

후속 상태: [reward-unchanged +2K control](<../../../../research/experiments/h1/exp-h1-action-rate-relaxation.md>) `20261014-111135-h1-actrate-0001-unchanged-cont2k` 학습 COMPLETED/PASS와 `model_4699` PERSONAL 영상·full 평가 COMPLETE가 **10/15까지 확인**됐다. 본 보고서의 lin=.65 resume4650과 기존 CSV 비교도 위 후속 수납으로 완료됐고 직접 원 episode 재집계와 구분한다. 원문 당시 'control 부재' 주장은 역사적 제한으로 보존한다.

번들 CSV와 기존 개별 기록을 대조했다. 부모2700→4650에서 H2 vx error 0.0427→0.0254m/s, H3 vy error 0.0673→0.0571m/s는 개선되지만, H4 yaw error 0.1183→0.1791rad/s, H3 world XY 종료 잔류 0.669→2.398m는 악화한다. H5 body-frame 진행 평균/P05는 9.948/9.592→9.546/9.228m로 낮아지고, 최소값은 8.815→8.974m로 높아져 tail 전체의 일률 악화는 아니다. H5 평균 감소는 평가 seed 세 개 모두 약 0.39~0.41m로 나타난다. body 진행 적분은 실제 world 구간 통과거리와 동일하지 않다.

원문은 4개 원본 평가 ZIP의 protocol/source/config 일치 및 3,072 최초 cohort/정책을 보고한다. 이번 수납은 제공된 CSV·보고서·기존 기록을 확인했으며, 4개 원본 평가 ZIP 전체의 CRC/hash나 rollout을 재검증하지 않았다. 동일 cohort key는 동일 terrain/reset/물리 궤적 또는 독립 학습 반복을 보장하지 않는다. 공식 점수·reward 인과효과·범용 승격을 입증하지 않는다.

**판단: LINTRACK 전환 후보 HOLD 유지.** 10/15 현재 같은 부모 control의 학습·평가와 기존 CSV 교차 비교는 수납됐다. 선택 checkpoint4650 대 endpoint4699의 차이와 전체 training-side 조건 미독립검증 때문에 **lin 변경 인과 효과는 미확정**이다. 기존 데이터 비교가 자동 GPU 학습/평가 승인은 아니며, 원문의 임시 임계값은 공식 검증된 채택 gate가 아니다.

당일 새 `20261014-081901-h1-lintrack-065-fresh5k`는 fresh, action=-0.0005인 별도 OFFICIAL 학습이다. 이 보고서의 4650(action=-0.0001, resume)과 혼합하지 않는다. fresh4950의 행동 평가는 이후 별도 10/15 보고서로 수납/HOLD이며 본 4정책 입력에 포함된 것은 아니다.
