# 실험 결과 분석

학습 Run 기록과 후속 정책 분석을 **작업 목적별**로 보관한다. 각 로봇의 `training/`은 실제 학습 수납·진단, `analysis/`는 영상·평가·보조평가·비교·공식 점수 해석이다. NVIDIA 보조평가도 분석이다. 실행 환경은 출처 정보로 남긴다. canonical 원본은 Originals의 `official_server_runs/` 또는 `private_server_runs/`에 보존하며 여기는 가공 문서와 근거 연결을 담는다.

## 수신 보고서와 실험 해석 연결

- [2026-10-15 H1 ACTION 복원·LINTRACK fresh 행동 비교](./h1/analysis/2026-10-15_H1_MODEL4650_LINTRACK065_POLICY_REVIEW.md): 두 제공 원문, 학습 Run·평가 SHA 분리, 정책 HOLD 및 기존 CPU 대조 우선.
- [최근 정책 선별 빠른 연결](./RECENT_POLICY_LINKS.md): 학습 Run → 후속 분석 → 수신 원문 → 평가 게시·receipt를 한 표에서 찾는다. 새 registry나 전체 상태 전수검사는 아니다.

- [수신 원문 ↔ 해석·Experiment 관계 12쌍](../incoming/REPORT_CROSSWALK.md): 원문은 `incoming/other/reviewed/`, 가공 수납은 `experiments/h1|go2/`라는 출처 역할을 분리한다. `model_2850`은 Experiment별 SHA로 구별하고 OFFICIAL 훈련·PERSONAL 행동·공식 제출/채점 상태를 혼합하지 않는다.

## H1·Go2 전수 파일 탐색

- [H1 학습·분석 색인](h1/README.md): 학습 8건·분석 30건(2026-10-15까지 등록된 가공 기록)과 보존 데이터·제출 snapshot·이전 주소 안내.
- [Go2 학습·분석 색인](go2/README.md): 학습 5건·분석 9건과 보존 그래프·CSV·제출 snapshot·이전 주소 안내.
- [2026-09-27 H1 사전 계획](../planning/historical/2026-09-27_H1_PERSONAL_FRESH_AND_CONTINUATION_PLAN.md)은 이후 세 PERSONAL 학습 Run의 evidence intake와 별도다. 새 가공 기록은 목적별 하위 폴더에 두고 옛 주소는 링크 호환용 안내로 남긴다.

이 색인은 추가 Run이나 공식 점수를 만들지 않으며 **파일별 원본 evidence를 옮기지 않는다**. 아래는 선별 주요 기록이고 전체 목록은 위 두 색인을 참고한다.

## H1

- [2026-08-24 공식 서버 300-iteration 기준선](./h1/training/2026-08-24_OFFICIAL_SERVER_300ITER_BASELINE.md): 환경·PPO·reward·terrain 확인, 4분 end-to-end 기준선, 증거 누락과 후속 실험 조건
- [2026-08-25 개인 서버 H1 `termination_penalty=-50` 25k 실행](./h1/training/2026-08-25_PERSONAL_SERVER_TERMINATION_M50_25K.md): TensorBoard·console·config가 보존된 장기 검증 실행. 공식 서버 결과나 제출 성능으로 해석하지 않음
- [2026-08-26 H1 finalize/report 버그 검토](./h1/analysis/2026-08-26_H1_FINALIZE_REPORT_BUG_REVIEW.md): full scalar와 자동 best/경고의 불일치, checkpoint cleanup의 운영 위험
- [2026-09-07 개인 Brev L40S H1 baseline 5K 및 screening 1K](./h1/analysis/2026-09-07_BREV_L40S_H1_BASELINE_5K_AND_SCREENING.md): baseline 5K 실측, TERM50·YAW075·RECOVERY 비교, 잘못 연결된 영상·checkpoint 경고
- [2026-09-08 공식 서버 H1 baseline 1K](./h1/training/2026-09-08_OFFICIAL_SERVER_H1_BASELINE_1K.md): 1K 완료·환경·무결성 검증, terrain 0·낙상률 100% 판정, 결과 묶음의 증거 범위
- [2026-09-09 공식 서버 H1 TERM50 5K 심층 분석](./h1/analysis/2026-09-09_OFFICIAL_SERVER_H1_TERM50_5K_DEEP_ANALYSIS.md): 낙상·terrain 개선과 yaw tracking trade-off. 호스트는 Ubuntu 24.04.2 + RTX 5080 + driver 580.126.09
- [2026-09-10 예선 2라운드 H1 TERM50 공식 평가](./h1/analysis/2026-09-10_OFFICIAL_EVAL_H1_ROUND2_TERM50.md): 종합 86.37/100, 시뮬 56.37/70. 7항목 77.8~82.1%. 비율 최저 요철, 절대 공백 최대 전진. 회전은 특이 약점 아님
- [2026-09-30 예선 4라운드 H1 AIRTIME-025 공식 평가](./h1/analysis/2026-09-30_OFFICIAL_EVAL_H1_ROUND4_AIRTIME025.md): 시뮬 56.37/70, 설계 의도 20/20, 리포트 품질 10/10; 구성 점수 합계 86.37/100. 7개 시나리오 점수와 공식 AI 코멘트 보존

## Go2

- [2026-10-08 Go2 로컬·공식 평가 불일치와 분석 방향](./go2/analysis/2026-10-08_GO2_LOCAL_OFFICIAL_EVALUATION_GAP_AND_ANALYSIS_POLICY.md): R3/R5 대화 기록. 평가기 유지·합산 점수 단독 채택 제한·목표/seed/취약 조건별 기존 자료 대조; 원인 미확정, 코드·GPU 작업 미실행

- [2026-10-08 예선 5라운드 Go2 공식 평가](./go2/analysis/2026-10-08_OFFICIAL_EVAL_GO2_ROUND5_LINTRACK125.md): `g2-submit-5 / LINTRACK-125`, 88.32/100(시뮬 58.32/70·설계 20/20·리포트 10/10), 7개 시나리오·원문·3라운드 수치 대조·10/08 순위 snapshot

- [2026-08-30 개인 Go2 12k baseline 분석](./go2/training/2026-08-30_GO2_BASELINE_CONVERSATION_SUMMARY.md): 9.5k 이후 value-loss 발산, 발산 전 checkpoint와 영상·원본 보존 상태
- [2026-08-30 Go2 발산에 대한 운영진 답변](./go2/training/2026-08-30_ORGANIZER_REPLY_GO2_DIVERGENCE.md): 알려진 확률적 장기 불안정, 제출용 설정 경계, iteration·reward 운영 판단
- [2026-09-11 Go2 12k 로그 실측 벽시계](./go2/training/2026-09-11_GO2_12K_WALLCLOCK_FROM_LOG.md): `go2-12k.log` 파싱. 5k=5:56:33, 9k=10:34:00. 9.5k 11:21:55는 9451 stall 포함이라 일반화 금지. 예산은 5k≈6 GPU-hours
- [2026-09-20 예선 3라운드 Go2 공식 평가](./go2/analysis/2026-09-20_SE3C_PRELIM_R3_GO2_EVALUATION_AND_ORGANIZER_REPLY.md): g2-submit-3 / LINTRACK-150-LINZ-2 제출 결과 87.55/100(시뮬 58.55/70, 설계 의도 19/20, 리포트 품질 10/10)과 운영진 답변을 분리 보존
- [2026-09-30 Go2 LINTRACK-125 OFFICIAL fresh 3K↔7.5K 심층 분석](../incoming/other/reviewed/GO2_20260929-154342-go2-lintrack-125-fresh7500-official_VS_20260928-230114-go2-lintrack125-fresh3k-r5-official_DEEP_ANALYSIS_20260930.md): 첫 3K scalar/checkpoint exact match로 추가 학습량 효과를 분리. 7.5K policy는 future paired evaluation 후보, reward-effect는 HOLD

## 규칙

- 원본 산출물 hash와 실행 ID를 기록한다.
- 측정값, 계산값, 코드 교차검증값, 원본 미보관 관찰값을 구분한다.
- 짧은 진단 정책의 성능을 장기 학습이나 공식 점수로 외삽하지 않는다.
- AI 핵심팩에는 전문을 추가하지 않고 검증된 결론만 기존 문서에 흡수한다.
