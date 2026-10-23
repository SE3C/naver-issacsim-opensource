# 개인 학습·사후 분석 원본

- [2026-10-18 H1 TOP07 model9950 A4000 evaluation](h1/2026-10-18_a4000_top07_model9950_evaluation/README.md): PERSONAL scenario7 COMPLETE/non-smoke; linked to OFFICIAL training keeper by SHA-256. Eval Release published/verified; not an official score.
- [2026-10-18 H1 TOP08 model9999 A4000 evaluation](h1/2026-10-18_a4000_top08_model9999_evaluation/README.md): PERSONAL scenario7 COMPLETE/non-smoke; linked to PERSONAL L40S training keeper by SHA-256. Eval Release published/verified; not an official score.

- [2026-10-18 H1 TOP08 L40S continuation toward 10K](h1/2026-10-18_l40s_lintrack065_actrate0001_resume10k/README.md): PERSONAL L40S Run `20261018-090630-h1-top08-same-reward-to10k`, completed/exit 0/validation PASS; resumed from 4650 for 5350 requested iterations, final `model_9999.pt`. Checkpoint index was not included; imported-parent provenance remains unverified. Separate A4000 evaluation; training Release published and verified.

- [2026-10-18 H1 LINTRACK-065 continuation toward 10K](h1/2026-10-18_l40s_lintrack065_resume10k/README.md): PERSONAL L40S Run `20261018-074037-h1-top06-same-reward-to10k`, completed/exit 0/validation PASS; `h1-submit-2 + lin=0.65`, final `model_9999.pt`. Checkpoint index was not included; imported-parent provenance remains unverified.
- [2026-10-18 H1 ORIENT-100 model9999 A4000 evaluation](h1/2026-10-18_a4000_orient100_model9999_evaluation/README.md): PERSONAL Linux A4000 scenario7 COMPLETE/non-smoke; 3,072 cohorts / 3,073 episode rows; no video or official score.
- [2026-10-18 H1 LINTRACK-065 model9999 A4000 evaluation](h1/2026-10-18_a4000_lintrack065_model9999_evaluation/README.md): PERSONAL Linux A4000 scenario7 COMPLETE/non-smoke; 3,072 cohorts / 3,072 episode rows; no video or official score.

- [2026-10-18 H1 ACTRATE-0001 + FEETSLIDE-035 model9950 A4000 평가](h1/2026-10-18_a4000_actrate0001_feetslide035_model9950_evaluation/README.md): PERSONAL camera-off scenario7 COMPLETE, 3,072 cohort/3,074 episode rows; 영상 없음. OFFICIAL 학습 원본과 별도 보존.

- [2026-10-17 H1 joint tracking + 자세·고관절 완화 model2850](h1/2026-10-17_windows_joint_tracking_posture_model2850_video_evaluation/README.md): Windows PERSONAL 6영상·full scenario7 완료, 학습은 별도 OFFICIAL Run. 정책 분석 대기.

공식 운영 서버의 학습·제출 결과와 개인 NVIDIA/Brev 학습·사후 평가 및 Windows 분석을 구분한다. 개인 실행물은 공식 점수나 제출 정책으로 해석하지 않는다. 역사적 폴더 이름은 유지하고 작업 목적별로 아래에서 찾는다.

- 대용량 원본 archive, TensorBoard event, checkpoint, 영상, chart는 이 저장소에 둔다.
- 분석·판정 문서는 `naver-issacsim/data/processed/experiments/`에 둔다.
- NVIDIA 재현용 저장소에는 작은 config, metrics, manifest만 둔다.
- binary archive는 Git LFS로 관리하므로 필요할 때만 명시적으로 가져온다.

## 학습 — H1

- [LINTRACK-065 model9999 continuation](h1/2026-10-18_l40s_lintrack065_resume10k/README.md): PERSONAL L40S training; policy analysis/adoption pending.

- [장기 TERM50 실행](h1/2026-08-25_exp1_termination_m50_long_25000iter/README.md)
- [L40S baseline 5K와 reward screening 1K](h1/2026-09-06_07_brev_l40s_baseline_5k_and_screening_1k/README.md)
- [역사적 LINTRACK075 continuation](h1/2026-09-18_h008_cont2k_from_model2998/README.md): corrected 2026-09-25 계보와 구분한다.
- [TERM100 fresh5K](h1/2026-09-21_h012_term100_fresh_5k/README.md)

## 학습 — Go2

- [Brev baseline 실행 폴더](go2/2026-08-30_brev_l40s_baseline_5k_9500iter/): 12k 요청, 9.5k 부근 발산. 발산 전 `model_9500`과 5k-best(`model_4500`) 보존. 해석은 분석 저장소 `experiments/go2/`.

## 분석 — NVIDIA 서버 보조평가

- [checkpoint 정량 비교](go2/2026-09-15_a1_checkpoint_quant_eval_seed4201_d1/README.md): 공식 A1 checkpoint 4300·원본 4800·recovery 4900의 개인 L40S 고정 조건 비교. 보조 평가 근거이며 공식 대회 점수가 아님.
- [4800/4900 native 영상 비교](go2/2026-09-15_a1_4800_vs_4900_native_video_comparison/README.md): stairs·boxes·inverted-stairs native play 6개 및 개별 evidence. 개인 L40S 시각 sanity check이며 프레임 판정은 후속 분석 문서에서 수행.

## 분석 — Windows H1 영상·평가

- [joint tracking lin=.65 / ang=.60 / action=-.0003 model4950](h1/2026-10-17_windows_joint_tracking_model4950_video_evaluation/README.md): OFFICIAL fresh5K keeper SHA와 연결한 PERSONAL 6영상·scenario7 COMPLETE, 정책 분석 대기.
- [ACTRATE-0001 + AIRTIME-025 model2950](h1/2026-10-14_windows_actrate0001_airtime025_model2950_video_evaluation/README.md): PERSONAL full 완료; OFFICIAL 학습 Run과 SHA로 연결.
- [ACTRATE-0001 + feet_slide=-0.35 model2950](h1/2026-10-14_windows_actrate0001_feet_slide_model2950_video_evaluation/README.md): PERSONAL full 완료; 앞 model2950과 다른 SHA.
- [ORIENT-100 model2850](h1/2026-10-07_windows_model2850_video_evaluation/README.md)
- [TERM-50 control model2800](h1/2026-10-08_windows_model2800_video_evaluation/README.md)
- [corrected LINTRACK075 model4997](h1/2026-10-09_windows_lintrack075_model4997_video_evaluation/README.md)
- [ACTRATE-0001 model2700](h1/2026-10-10_windows_actrate0001_model2700_video_evaluation/README.md)
- [ANGTRACK065 model2950](h1/2026-10-10_windows_angtrack065_model2950_video_evaluation/README.md)
- [ACTRATE-0001 fresh10K model9999](h1/2026-10-11_windows_actrate0001_fresh10k_model9999_video_evaluation/README.md)
- [ACTRATE-0001→lin=.65 model4650](h1/2026-10-11_windows_actrate0001_lintrack065_model4650_video_evaluation/README.md)

## 분석 — Windows Go2 영상·평가

- [LINTRACK125 model7050](go2/2026-10-04_windows_model7050_video_evaluation/README.md): automatic best이며 terminal7450과 구분한다.
- [g2-submit-3 original4800](go2/2026-10-09_windows_model4800_video_evaluation/README.md): PERSONAL 평가 성공으로 원래 학습의 INTERRUPTED 상태를 바꾸지 않는다.

## 분석 — 다른 역사적 원본 경로에 보존된 자료

ACTRATE-001 model2850은 [공식 학습 폴더 안의 PERSONAL Windows 원본](../official_server_runs/h1/2026-10-10_215330_actrate001_fresh3k/personal_windows_eval_20261010/README.md)에서 찾는다. 과거에 안내된 `../official_server_runs/h1/2026-10-10_215330_actrate001_fresh3k/post_training_personal_evaluations/`는 **2026-10-14 현재 Git `main` tree에서 확인되지 않는다**(외부 보존 여부는 미확인). 원본을 중복 복사·이동하지 않는다. ORIENT-100 model2850과는 다른 SHA의 정책이다.

위 목록은 로봇별 보존 폴더와 별도 경로 예외를 안내한다. 후속 분석·공식 점수·현재 HOLD/PROMOTE 판단은 [registry](https://github.com/SE3C/naver-issacsim/blob/main/research/EXPERIMENTS.md)를 따른다. 폴더별 README는 당시 수납 기록이며 현재 상태의 자동 갱신본이 아니다.
