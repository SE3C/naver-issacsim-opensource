# PERSONAL Release 색인 — 작업 목적별 2026-10-13

주분류는 `[학습]`·`[분석]`이다. TRAIN/VIDEO/EVAL-PC/EVAL은 역사적 검색용 하위 유형이며 Experiment/Run ID나 품질 판정이 아니다. 실패·대체됨·검증 대기 표시는 별도로 유지한다.

앞으로 Windows PC 통합 영상·평가는 비공개 `SE3C/naver-issacsim-eval` Release에 게시한다. 개인 NVIDIA 서버 학습 및 native 영상 게시기는 그대로 유지한다. 기존 Release의 태그·주소·애셋과 관리 안내 아래의 원래 본문은 보존한다. 아래 제목은 2026-10-13 표시 정리를 반영하며, 이후 게시물 전부를 자동 수집하는 색인은 아니다.

- [PC 평가 게시 기준](https://github.com/SE3C/naver-issacsim-eval/blob/main/EVALUATION_RELEASES.md)
- [공통 Release 분류](https://github.com/SE3C/naver-issacsim/blob/main/docs/RELEASE_TAXONOMY.md)

## 학습 — 기존 TRAIN 및 후속 게시

- [[학습] H1 LINTRACK-065 + ACTRATE-0001 · PERSONAL L40S · continuation to 10K](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261018-exp-h1-action-first-planar-tracking-switch-resume10k): Run `20261018-090630-h1-top08-same-reward-to10k`, COMPLETED/exit0/validation PASS. Archive 739,533,489 bytes, SHA-256 `416b10bd9c921d3b0f58df9332a3f809c104409b25c5dd6b079f801d284406a8`; remote size/digest verified. Separate [PERSONAL A4000 evaluation](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261018-exp-h1-action-first-planar-tracking-switch-model9999-a4000-eval) matches final `model_9999.pt`. Analysis/adoption HOLD.

- [[학습] LINTRACK-065 · PERSONAL L40S · continuation toward 10K · train evidence](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261018-exp-h1-planar-tracking-weight-lin065-resume10k)

- [[학습] AIRTIME-025 · PERSONAL · corrected 3K→5K continuation · attempt 02 · train evidence](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260927-054950-h1-airtime-025-corrected3kto5k-r02-20260927)
- [실패 · [학습] AIRTIME-025 · PERSONAL · corrected 3K→5K continuation · attempt 01](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260927-053754-h1-airtime-025-corrected3kto5k-r01-20260927_FAILED)
- [[학습] AIRTIME-025 · LINTRACK-075 · PERSONAL · fresh 3K · train evidence](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260927-043527-h1-airtime-025-lintrack-075-fresh3k-r01-20260927)
- [[학습] AIRTIME-025 · PERSONAL · fresh 3K · train evidence](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260927-032343-h1-airtime-025-fresh3k-r01-20260927)
- [[학습] HIPDEV-010 · LINTRACK-075 · PERSONAL · corrected 5K train evidence · verified source 75123c7](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260925-110346-h1-hipdev-010-lintrack-075-r02-corrected-h1-corrected-202-source75123c7)
- [대체됨 · [학습] HIPDEV-010 · LINTRACK-075 · PERSONAL · corrected 5K train evidence · incorrect tag source](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260925-110346-h1-hipdev-010-lintrack-075-r02-corrected-h1-corrected-202)
- [[학습] AIRTIME-025 · LINTRACK-075 · PERSONAL · corrected 5K train evidence](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260925-102659-h1-airtime-025-lintrack-075-r02-corrected-h1-corrected-20)
- [[학습] HIPDEV-030 · LINTRACK-075 · PERSONAL · corrected 5K train evidence](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260925-095000-h1-hipdev-030-lintrack-075-r02-corrected-h1-corrected-202)
- [[학습] LINTRACK-075 · PERSONAL · corrected unchanged 5K control · train evidence](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260925-091257-h1-lintrack-075-corrected-control-to5k-h1-corrected-2026)
- [[학습] LINTRACK-075 · PERSONAL · corrected 3K train evidence](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260925-084248-h1-lintrack-075-r03-corrected-h1-corrected-2)
- [[학습] LINTRACK-100 · PERSONAL · corrected 3K train evidence](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260925-081241-h1-lintrack-100-r02-corrected-h1-corrected-2)
- [[학습] AIRTIME-030 · PERSONAL · corrected 3K train evidence](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260925-074219-h1-airtime-030-r02-corrected-h1-corrected-20260)
- [[학습] AIRTIME-025 · from TERM-50 parent · PERSONAL · corrected 3K train evidence](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260925-071158-h1-airtime-025-from-term-50-r02-corrected-h1-corrected-20260)
- [[학습] TERM-50 · PERSONAL · corrected unchanged 3K control · train evidence](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260925-064143-h1-term-50-corrected-control-to3k-h1-corrected-2026)
- [[학습] TERM-50 · PERSONAL · corrected +0.2 parent 1.5K · batch -03](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260925-061112-h1-term-50-r05-corrected-parent-1p5k-h1-corrected-2)
- [검증 대기 · [학습] TERM-50 · corrected-parent earlier -02 batch · PERSONAL](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260925-050146-h1-term-50-r05-corrected-parent-1p5k-h1-corrected-2)
- [[학습] TERM-100 · PERSONAL · fresh 5K train evidence](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260921-033633-h1-term-100-5k)
- [[학습] HIPDEV-010 · LINTRACK-075 · PERSONAL · historical 3K→5K continuation · relative comparison only](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260920-150652-h1-hipdev-010-lintrack-075)
- [[학습] AIRTIME-025 · LINTRACK-075 · PERSONAL · historical 3K→5K continuation · relative comparison only](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260920-134309-h1-airtime-025-lintrack-075-rerun)
- [[학습] HIPDEV-030 · LINTRACK-075 · PERSONAL · historical 3K→5K continuation · relative comparison only](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260918-010042-h1-hipdev-030-lintrack-075-from-h008-3k)
- [[학습] LINTRACK-075 · PERSONAL · historical 1.5K train evidence · relative comparison only](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260917-004530-h1-lintrack-075-from-term-50-feet-minus-0.2-1p5k)
- [[학습] LINTRACK-100 · PERSONAL · historical 1.5K train evidence · relative comparison only](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260917-002225-h1-lintrack-100-from-term-50-feet-minus-0.2-1p5k)
- [[학습] AIRTIME-030 · PERSONAL · historical 1.5K train evidence · relative comparison only](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260916-235914-h1-airtime-030-from-term-50-feet-minus-0.2-1p5k)
- [[학습] AIRTIME-025 · PERSONAL · historical 1.5K train evidence · relative comparison only](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260916-233344-h1-airtime-025-from-term-50-feet-minus-0.2-1p5k)
- [[학습] TERM-50 · PERSONAL · historical 1.5K parent · feet_air_time=-0.2](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260916-230730-h1-term-50-feet-minus-0.2-1p5k)
- [[학습] TERM-20 · PERSONAL · fresh 1.5K · relative comparison only](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260916-152542-h1-term-20-1p5k)
- [[학습] LINTRACK-150-LINZ-2 · PERSONAL · fresh 3K train evidence](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260913-144615-go2-lintrack-150-linz-2-train-3k)
- [[학습] LINTRACK-150-LINZ-2 · PERSONAL · fresh 1K train evidence](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260913-132700-go2-lintrack-150-linz-2-train-1k)
- [[학습] ANGXY-012 · PERSONAL · fresh 1K train evidence · legacy G5](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260913-070026-go2-angxy-012-1k-20260913)
- [[학습] Go2 · PERSONAL · 1-iteration smoke evidence](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260913-061236-smoke-go2-20260913)

## 분석 — 개인 서버 영상 23개 (기존 VIDEO)

- [[분석] AIRTIME-025 · PERSONAL · video suite · model_4800 (intermediate; final model_4997)](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-checkpoint-h1-model_4800-40c6a4a8273c-videos)
- [[분석] AIRTIME-025 · PERSONAL · video suite · automatic-best model_2750 (final model_2999)](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-checkpoint-h1-model_2750-6d7d0ecb13c7-videos)
- [[분석] AIRTIME-025 · LINTRACK-075 · PERSONAL · video suite · automatic-best model_2700 (final model_2999)](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-checkpoint-h1-model_2700-5d19578749df-videos)
- [[분석] TERM-50 · PERSONAL · corrected +0.2 parent · video suite · model_1499](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-term-50-r05-parent-h1-corrected-20260925-03-videos)
- [[분석] TERM-50 · PERSONAL · unchanged 3K control · video suite · model_2998](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-term-50-control-3k-h1-corrected-20260925-03-videos)
- [[분석] LINTRACK-100 · PERSONAL · corrected-lineage video suite · model_2998](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-lintrack-100-r02-h1-corrected-20260925-03-videos)
- [[분석] LINTRACK-075 · PERSONAL · corrected-lineage video suite · model_2998](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-lintrack-075-r03-h1-corrected-20260925-03-videos)
- [[분석] LINTRACK-075 · PERSONAL · unchanged 5K control video suite · model_4997](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-lintrack-075-control-5k-h1-corrected-20260925-03-videos)
- [[분석] HIPDEV-030 · LINTRACK-075 · PERSONAL · corrected-lineage video suite · model_4997](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-hipdev-030-lintrack-075-r02-h1-corrected-20260925-03-videos)
- [[분석] HIPDEV-010 · LINTRACK-075 · PERSONAL · corrected-lineage video suite · model_4997](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-hipdev-010-lintrack-075-r02-h1-corrected-20260925-03-videos)
- [[분석] AIRTIME-030 · PERSONAL · corrected-lineage video suite · model_2998](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-airtime-030-r02-h1-corrected-20260925-03-videos)
- [[분석] AIRTIME-025 · from TERM-50 parent · PERSONAL · corrected-lineage video suite · model_2998](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-airtime-025-from-term-50-r02-h1-corrected-20260925-03-videos)
- [[분석] AIRTIME-025 · LINTRACK-075 · PERSONAL · corrected-lineage video suite · model_4997](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-airtime-025-from-lintrack-075-r02-h1-corrected-20260925-03-videos)
- [[분석] TERM-100 · PERSONAL · video suite · model_4700](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/h1-term-100-5k-videos)
- [[분석] LINTRACK-100 · PERSONAL · historical video suite · model_2998 · relative comparison only](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260918-h1-lintrack-100-model2998-video-suite)
- [[분석] HIPDEV-010 · LINTRACK-075 · PERSONAL · historical video suite · model_4997 · relative comparison only](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260920-h1-hipdev-010-lintrack-075-model4997-video-suite)
- [[분석] AIRTIME-025 · LINTRACK-075 · PERSONAL · historical video suite · model_4997 · relative comparison only](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260920-h1-airtime-025-lintrack-075-model4997-video-suite)
- [[분석] LINTRACK-075 · PERSONAL · historical native-play video · relative comparison only](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260917-010854-20260917-004530-h1-lintrack-075-from-term-50-feet-minus-0.2-1p)
- [[분석] LINTRACK-100 · PERSONAL · historical native-play video · relative comparison only](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260917-004341-20260917-002225-h1-lintrack-100-from-term-50-feet-minus-0.2-1p)
- [[분석] AIRTIME-030 · PERSONAL · historical native-play video · relative comparison only](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260917-002012-20260916-235914-h1-airtime-030-from-term-50-feet-minus-0.2-1p5k-v)
- [[분석] AIRTIME-025 · PERSONAL · historical native-play video · relative comparison only](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260916-235551-20260916-233344-h1-airtime-025-from-term-50-feet-minus-0.2-1p5k-v)
- [[분석] LINTRACK-150-LINZ-2 · PERSONAL · native-play video · 3K run](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260913-173221-20260913-144615-go2-lintrack-150-linz-2-video-3k)
- [[분석] LINTRACK-150-LINZ-2 · PERSONAL · native-play video · 1K run](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260913-142759-20260913-132700-go2-lintrack-150-linz-2-video-1k)

## 분석 — Windows PC 영상·평가 10개 (기존 EVAL-PC)

- [[분석] H1 ACTRATE-0001 fresh 10K · model_9999 · PERSONAL videos + full evaluation](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261011-exp-h1-action-rate-relaxation-model9999-video-eval)
- [[분석] H1 ACTRATE-0001 → lin=0.65 · PERSONAL model_4650 videos + evaluation](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261011-exp-h1-action-first-planar-tracking-switch-model4650-video-eval)
- [[분석] H1 ANGTRACK-065 · model_2950 · PERSONAL videos + full evaluation](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261010-exp-h1-angular-tracking-boost-model2950-video-eval)
- [[분석] H1 ACTRATE-001 model_2850 PERSONAL 6-terrain video + scenario7 evaluation](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261010-exp-h1-action-rate-smoothing-model2850-video-eval)
- [[분석] H1 ACTRATE-0001 · model_2700 · PERSONAL videos + full evaluation](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261010-exp-h1-action-rate-relaxation-model2700-video-eval)
- [[분석] H1 LINTRACK-075 corrected 5K · model_4997 · PERSONAL videos + full evaluation](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261009-lintrack-075-corrected5k-model4997-video-eval)
- [[분석] H1 h1-submit-2 / TERM-50 · model_2800 · PERSONAL Windows 6영상 + 평가](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261008-exp-h1-rough-terrain-orientation-relaxation-model2800-control-video-eval)
- [[분석] Go2 g2-submit-3 · original model_4800 · PERSONAL · 6-terrain + scenario7 evaluation](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-go2-20261009-g2-submit-3-model4800-video-eval)
- [[분석] H1 ORIENT-100 · model_2850 · PERSONAL Windows 6영상 + 평가](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261007-exp-h1-rough-terrain-orientation-relaxation-model2850-video-eval)
- [[분석] Go2 LINTRACK-125 · PERSONAL Windows · model_7050 · 6영상 + scenario7 평가](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-go2-20261004-exp-go2-planar-tracking-terrain-progression-model7050-video-eval)

## 분석 — 개인 NVIDIA 서버 보조평가 2개 (기존 EVAL)

- [[분석] LINTRACK-150-LINZ-2 · PERSONAL · fixed checkpoint evaluation · seed 4201, d1](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-go2-20260915-lintrack-150-linz-2-checkpoint-quant-eval-seed4201-d1)
- [[분석] LINTRACK-150-LINZ-2 · PERSONAL · native video comparison · checkpoints 4800/4900](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-go2-20260915-lintrack-150-linz-2-4800-vs-4900-native-video)

## ARCHIVE — 복합·역사적 보존 5개

- [ARCHIVE LINTRACK-075 · PERSONAL · historical 3K→5K continuation · relative comparison only](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/20260917-234047-h1-lintrack-075-cont2k-from-2998)
- [ARCHIVE H1 · historical 1K screening bundle · TERM-50 / ANGTRACK-075 / HIPDEV-010-TORSODEV-005](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/h1-screening-20260907_122939_KST)
- [ARCHIVE H1 · historical baseline 5K backup](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/h1-baseline-5k-20260907_102236_KST)
- [ARCHIVE Go2 · historical Brev recovery bundle](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/brev-go2-recovery-20260830_125132_KST)
- [ARCHIVE H1 · historical training backup](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/brev-backup-20260826_075522_KST)
