# exp-h1-action-rate-restoration

## 2026-10-15 같은 부모 CPU 비교 완료 — 복원4650 HOLD

[CPU 비교 원문·CSV·수납](../../../data/processed/experiments/h1/analysis/2026-10-15_ACTRATE_PARENT_UNCHANGED_RESTORATION_COMPARISON_INTAKE.md): 부모2700/무변경4699/복원4650(`a8249db4…`)의 기존 PERSONAL 평가 raw 대조 완료. 복원은 무변경보다 H5 진행373/384건 증가·평균7.919→8.769m이나 tracking283/384건 악화(.18596→.19816), 최악 진행6.239→4.845m·stall .074→.386이다. **복원 HOLD, PROMOTE 없음**. 무변경은 이번 범용·전진/험지 대표에서만 REJECT, 부모는 HOLD다. 평가 checkpoint4650과 endpoint4699 차이·단일 학습 seed·원 imported-parent provenance 한계 때문에 action reward 인과효과는 미확정이다. 아래 개별 보고서의 CPU 비교 제안은 이제 해소된 당시 과제이며 옛 lin=.65 resume4650은 이번 비교가 아니다.

[보존된 제공 원문](../../../data/processed/incoming/other/reviewed/H1_MODEL4650_POLICY_ANALYSIS_20261015.md) · [통합 판정](../../../data/processed/experiments/h1/analysis/2026-10-15_H1_MODEL4650_LINTRACK065_POLICY_REVIEW.md). 이미 등록된 OFFICIAL action-rate 복원 +2K Run의 `model_4650.pt` **SHA `a8249db4…25b84ea`**를 사후 PERSONAL Windows `scenario7` 3,072 episode+6영상으로 분석한 **사용자 제공 보고서**다. 평가 ZIP 18항목/CRC, 3,072 timeout, 0 base-contact 종료 등은 보고서의 검증 기록이며 이번 Git 반영에서 ZIP·MP4를 다시 열지 않았다.

H1 정지 body 비의도 전진 **0.282m**, H3 횡왕복 중 비의도 전진 **0.276m**, H3 world 최종 순변위 **0.167m**, H2/H7 body 전진 **15.297/10.364m**는 활용 가능한 신호다. 반면 rough H5 body 진행 평균/P05/최소 **8.769/7.970/4.845m**, stall>0.05 **7/384**, 최악 seed4201/env60 stall **0.386**으로 **전지형 대표 후보 HOLD**. 계단 중앙 다단 완주, boxes 정량, 공식 점수, reward 인과 미확정.

**같은 부모 무변경 대조군** `20261014-111135-h1-actrate-0001-unchanged-cont2k / model4699`와 부모2700의 CPU 원자료 비교는 위 후속 보고서로 완료됐다. 두 Run의 입력 SHA 연결과 imported-parent provenance null/unverified는 구분한다. 아래 개별 보고서 당시2700 대조는 기술적 참고였고 후속 raw 비교와 근거 수준이 다르다. 복원 `model4650`은 terminal4699 또는 10/11 `ce7ad586…` LINTRACK resume 동명 checkpoint가 아니다. 이후 ‘평가 대기’는 기존 수납 당시 문구다.


## 2026-10-15 PERSONAL 사후 평가 완료

OFFICIAL Run `20261014-142200-h1-actrate-return2700-2k`의 `model_4650.pt`(SHA `a8249db467a60015036bf229b0026b215a61e17859f1d302efe283af225b84ea`)로 Windows 6영상 + full H1 scenario7 평가가 완료됐다. 평가 checkpoint는 terminal model_4699가 아니다. [평가 Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261015-exp-h1-action-rate-restoration-model4650-video-eval). 원본 평가의 source_run_id=null과 학습 imported-parent provenance 한계는 유지하고 외부 checkpoint SHA/index로 연결한다. 신규 학습/공식 점수/A/B 비교가 아니며 HOLD / 분석 대기. 아래 평가 대기는 과거 수납 시점 상태다.

## 2026-10-14 OFFICIAL action-rate restoration resume +2K

- Question: after the ACTRATE-0001 fresh3K policy was trained with `action_rate_l2=-0.0001`, what happens when returning to the h1-submit-2 baseline action-rate weight for one +2K resume step?
- Actual Run `20261014-142200-h1-actrate-return2700-2k`: H1 / OFFICIAL / train / resume; seed 42, 4096 envs, requested +2,000 from iteration 2700, final 4699/4700; exit 0, COMPLETED/PASS; finalize and official backup succeeded.
- Archived effective rewards: lin=0.5, ang=0.5, feet=0.2, termination=-50, orientation=-1.5, angxy=-0.05, hip=-0.2, torso=-0.1, action=-0.0005. Compared with ACTRATE-0001 parent model_2700, only `action_rate_l2` changes from -0.0001 back to -0.0005.
- Parent checkpoint SHA `e54d3389e20ea913968ef8d3edbea5004368ff225fa6b94f73fcd91cf93ca7ae` matches preserved OFFICIAL ACTRATE-0001 fresh3K `model_2700.pt`. Raw metadata remains `source_checkpoint_origin=user_imported_checkpoint`, `source_evidence_run_id=null`, `parent_run_id=null`, `source_run_mode=unknown`, and `source_provenance_verified=false`; external SHA matching does not rewrite this provenance.
- Same-parent unchanged-reward control: Run `20261014-111135-h1-actrate-0001-unchanged-cont2k`, whose reward values match the parent. Both are separate one-step resume Runs from the same recorded parent SHA; source metadata provenance is unverified in each.
- [Canonical raw evidence README](https://github.com/SE3C/naver-issacsim-originals/blob/main/data/raw/official_server_runs/h1/2026-10-14_232208_actrate0001_return2700_2k/README.md) · [OFFICIAL Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261014-exp-h1-action-rate-restoration-resume2700-plus2k).
- No video/policy evaluation, submission, official score, or adoption decision is recorded. Behavior assessment remains pending/HOLD.
