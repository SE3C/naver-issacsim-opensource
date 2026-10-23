> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/experiments/h1/analysis/2026-10-11_ACTRATE001_MODEL2850_POLICY_REVIEW.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# [분석] ACTRATE-001 / model_2850 (SHA 1e6d…bb1) PERSONAL 정책 행동 검토 — 2026-10-11

> 관리 안내 (2026-10-13): **분석** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](<../../../../research/EXPERIMENTS.md>)를 확인한다.

- **Experiment:** [exp-h1-action-rate-smoothing](<../../../../research/experiments/h1/exp-h1-action-rate-smoothing.md>), descriptor `ACTRATE-001` (`action_rate_l2=-0.001`).
- **기존 OFFICIAL 학습 Run:** `20261010-125324-h1-actrate-001-fresh3k`; fresh 3,000 iterations, seed 42, 4096 env, no parent, exit 0, evidence validation PASS. 본 검토는 학습 Run을 추가하지 않는다.
- **선택 정책:** auto-best `model_2850.pt` SHA-256 `1e6d0950f5bd981ca1f88044e65ae7ee57505c47b92b5caad8c39263f4d93bb1`; 최종 보존 `model_2950.pt`와 구별.
- **평가:** Windows **PERSONAL** H1 `scenario7`, 8 case × 3 evaluation seeds(4201–4203) × 128 env = 3,072개 최초 20초 episode; 6개 MP4는 별도의 command/terrain trajectory. OFFICIAL 제출·채점이나 새 학습이 아니다.
- **원문 분석:** [2026-10-10 사용자 제공 심층 보고서](<../../../received/H1_MODEL2850_SHA1E6D_POLICY_ANALYSIS_20261010.md>) — 입력 파일 내용을 변경 없이 보존. 이 기록을 작성하며 원본 평가 ZIP/MP4를 다시 내려받아 독립 재계산하지는 않았다.
- **보존된 평가 ZIP:** `model_2850_h1_6terrain_evaluation_20261010-233937_1cc2ab9d.zip` (기존 publication 기록에 따라 SHA-256 `1906880030393b904d7323bdbf71352f408a067328a09ac8bf87604438c07351`). [PERSONAL 영상/평가 Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261010-exp-h1-action-rate-smoothing-model2850-video-eval).

## 보고서에서 확인했다고 기록한 행동 증거

| 축 | 보고서 수치 / 해석 |
| --- | --- |
| 평가 완료와 생존 | 3,072/3,072 episode가 20초 timeout, base-contact failure 0. 이는 정책 명령 정확도 또는 계단 완주의 보증이 아님 |
| 전진 H2 / 외란 H7 | body-frame 전진 적분 **15.470m / 10.656m** (명령 적분 15m / 10m). world 직선거리나 지형 완주 거리 아님 |
| 경사 H6 (+10°/−10°) | body-frame 전진 **20.297m / 20.058m**, 통합 tracking **0.18801 / 0.18802**, action Δ RMS **0.3943 / 0.3955** |
| 정지 H1 | 명령 `[0,0,0]`에도 비의도 body 전진 **+1.164m**, world XY 순변위 **평균 1.151m**; 384/384 cohort가 1m 초과. 정지 `stall=0`은 성공 지표가 아님 |
| 횡이동 H3 | 상반된 lateral 명령 이후 body 비의도 전진 **+1.109m**, world XY 순변위 크기 **평균 2.177m** |
| Rough H5 | 평균/P05/최소 body 전진 **9.359/8.921/8.372m** (명령 10m), tracking 평균/P95 **0.17111/0.18947**, max stall **0.028**, stall>0.05 **0/384**. 이번 실패 신호는 낙상/장기 stall보다 진행·추종 저하 |
| 계단 / 박스 | 6개 영상의 초기 구간은 접지/보행을 시사하나 계단 중앙 다단 완주 및 장시간 박스 통과의 정량 증빙 없음. camera-off에는 stairs/boxes case 없음 |

**판정: HOLD.** 제한된 전진·rough·경사·push 중 이동하는 보행 후보로 보존한다. 정지 위치 유지·횡이동 왕복 복귀·계단 중앙 통과가 검증되지 않아 범용 대표 정책으로 PROMOTE하지 않는다. 높은 20초 생존률과 평가 프로세스 완료를 정책 행동 품질·reward 인과효과·OFFICIAL 점수로 바꾸지 않는다.

## 계보 해석 및 다음 비교

이번 분석 ZIP만 보면 `source_run_id=null`, `preset=null`이고 학습 증거가 없지만, **이미 보존된 별도 OFFICIAL 학습 기록**의 `ACTRATE-001` Run `model_2850.pt` 체크포인트 SHA-256가 평가 SHA와 일치하므로 후속 PERSONAL 평가로 연결한다. ZIP 안의 null 값을 수정하지 않는다. 같은 파일명인 **`ORIENT-100/model_2850.pt` SHA `6aedeced…f7b0`**는 다른 정책이다. `ACTRATE-0001`(완화 `-0.0001`)과 `ACTRATE-001`(강화 `-0.001`)을 혼동하지 않는다.

**1순위 기존 대조군:** 기존 `h1-submit-2 / TERM-50` unchanged OFFICIAL fresh3K 모델 `model_2800.pt`의 보존된 PERSONAL `scenario7` 원자료. checkpoint SHA/protocol/source/PPO/command/terrain/seed/horizon/initialization parity를 먼저 검토하고 대응 가능한 `(scenario, case, seed, env_id)` 최초 episode끼리 H1/H3 drift, H5 P05/P95 tail, H6 yaw/action, H7 진행/종료를 비교한다. 보고서의 과거 후보 요약치 표는 **matched raw A/B가 아니므로** reward 개선율을 확정할 수 없다.

**2순위 참고:** `ORIENT-100/model_2850` 및 `ACTRATE-0001/model_2700`의 보존 평가 raw (별도 reward/학습 계보). 이들의 요약치가 비슷해도 단일 변수 인과 비교는 아니다. 새 GPU 평가·학습·영상 생성/export는 이번 수납 범위에 없다.

**보존/검증 경계:** 분석 원문은 byte-for-byte 보존 대상이다. 이 문서의 행동 수치는 그 사용자 제공 분석에서 인용했고, 학습 Run ↔ checkpoint SHA 연결은 GitHub에 이미 보존된 Experiment/Release 기록과 대조했다. 제출 정책 승격·Optuna 완료 trial·공식 점수를 추가로 만들지 않는다.
