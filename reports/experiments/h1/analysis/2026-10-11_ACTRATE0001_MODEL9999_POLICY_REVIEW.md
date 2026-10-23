> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/experiments/h1/analysis/2026-10-11_ACTRATE0001_MODEL9999_POLICY_REVIEW.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# [분석] ACTRATE-0001 fresh10K / model_9999 정책 분석 수납 — HOLD

> 관리 안내 (2026-10-13): **분석** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](<../../../../research/EXPERIMENTS.md>)를 확인한다.

- Experiment: [exp-h1-action-rate-relaxation](<../../../../research/experiments/h1/exp-h1-action-rate-relaxation.md>).
- [사용자 보고서 원문](<../../../received/H1_MODEL9999_POLICY_ANALYSIS_20261011.md>)은 변경 없이 보존했다. SHA-256 `fc8ae62a28dfe79b0c1a6beabe675d5ef10ade1efcb8fe598400f0c85f971db9`.
- OFFICIAL fresh10K 학습 기록〔원본 참조: `../2026-10-11_ACTRATE0001_OFFICIAL10K_EVIDENCE_INTAKE.md` / 공개 사본 미포함〕: Run `20261011-041745-h1-actrate-0001-fresh10k-official`, exit0/validation PASS, no parent/resume, `h1-submit-2 + action=-0.0001`.
- PERSONAL 6영상·평가 publication〔원본 참조: `../../../operations/windows_h1_video_evaluation/2026-10-11_ACTRATE0001_FRESH10K_MODEL9999_PUBLICATION.md` / 공개 사본 미포함〕: keeper `model_9999.pt` SHA `a5020c273bc2b69bea1b20782fe80ba6605b3036b4054a7e5a8ab66151d2cb74`는 공식 train checkpoint index와 일치한다. 자동 best model_9900과 과거 fresh3K model_2700은 다른 정책이다.

## 보고서의 관찰 및 해석

보고서는 입력 ZIP의 3,072개 episode를 직접 재집계하고 여섯 영상의 약 0.5초 간격 표본·초기/후반·연속 프레임을 확인했다고 기록한다. 이번 수납에서는 그 수치와 관찰을 출처와 함께 요약했으며, raw episode를 다시 계산하거나 영상을 다시 디코딩하거나 GPU 평가를 실행하지 않았다.

- 3,072/3,072개의 20초 timeout 생존, 몸통 접촉 종료 0회. 전진 H2 body 적분 14.885m/명령 15m, push H7 9.974m/10m, 경사 H6 상·하 19.788/19.730m/20m.
- 정지 H1 world 순변위 평균 0.287m와 비의도 body 전진 0.231m, 횡왕복 H3 순변위 0.395m와 비의도 전진 0.273m. 회전 H4 yaw 평균 절대오차 0.06655rad/s.
- 주요 약점은 rough H5 body 전진 평균/P05/최소 **8.915/8.251/6.492m** 및 tracking 평균 0.18561. 최악 seed4202/env57은 tracking 0.28957, stall 0.104이지만 살아 있다. 생존만으로 목표 속도의 험지 통과를 주장하지 않는다.
- 전체 episode 동일가중 tracking 0.122384는 8-case 혼합 단위 내부 진단값이지 공식 점수가 아니다. 경사 action Δ RMS 상·하 0.66371/0.68840은 행동 변화량이며 에너지·토크의 직접 측정값이 아니다.
- 영상에서 초기 boxes/rough 패치 진행과 후반 보행을 관찰했지만 중앙 연속 다단 계단 완주는 미입증이다. 각 영상 frame0의 검정은 초기 capture artifact이며, 조사 구간의 짝홀 교대 검정은 보고되지 않았다. 영상과 camera-off scenario7은 별도 명령·지형·시드의 증거다.

**분석 수납 완료; 보고서 판정 HOLD.** 유용한 전진·경사·정지·횡명령 후보이지만 rough 하위 꼬리, 계단 검증 공백과 직접 대조 부재가 남는다. 제출 여부는 사용자의 결정이며 이번 수납에서 실제 제출·공식 점수·reward 인과 개선·새 preset 승격을 기록하지 않는다.

보고서의 Run/preset 미확인은 ZIP 단독의 한계다. 별도 공식 index와 checkpoint SHA를 대조한 외부 publication이 학습 연결 근거이며 원문·ZIP의 source_run_id/preset=null을 고치지 않는다. 다음 권장 작업은 이미 보존된 TERM-50/model2800 평가의 protocol/source/command/terrain/seed/horizon 및 cohort 기준을 확인한 CPU raw 비교다. fresh3K/model2700은 참고 후보이고 두 Run의 학습량 차이를 reward 효과로 해석하지 않는다. 새 학습·평가를 자동 실행하지 않는다.
