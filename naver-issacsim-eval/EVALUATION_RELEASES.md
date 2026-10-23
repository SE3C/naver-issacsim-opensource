# PERSONAL 사후 평가 Release

## 2026-10-19 H1 local evaluations — preserved with recorded seed counts

- [model40300 / two-seed PERSONAL evaluation](publications/2026-10-19_h1_model40300_2seed/README.md): Windows H1 camera-off `scenario7`, 128 envs, seeds 4201/4202, manifest `complete=true`, `smoke=false`, 2,048 episode rows. ZIP 377,570 bytes, SHA-256 `046359f52f88035b79866b17469c49ad8bd62c3af2135b3ebe72ec1a5f535ceb`. The archive records a failed post-run source-integrity check; see its receipt. No training provenance or official score is asserted.
- [TOP01 ANG070 +3K / model12900 PERSONAL evaluation](publications/2026-10-19_h1_top01_angtrack060_model12900/README.md): Windows H1 camera-off `scenario7`, 128 envs, seed 4201, manifest `complete=true`, `smoke=false`, 1,024 episode rows. Original archive and folder retain their `angtrack060` names; archived config identifies `ang=0.70`. ZIP 187,666 bytes, SHA-256 `abf37b45d32c28c26de232214313641d7e3fcd289e422df16ba8cae72b030eb2`. A separate checkpoint-index SHA match links the OFFICIAL training Run; raw evaluation `source_run_id` remains null. No official score is established.

Both records preserve the supplied ZIP bytes and document archive metadata, checkpoint identity, protocol settings, and episode-file completeness. Releases: [model40300 / two seeds](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261019-model40300-2seed-personal-eval) · [ANG070 model12900 / one seed](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261019-exp-h1-joint-tracking-balance-ang070-model12900-local-eval). Remote asset verification receipts are retained with each publication.

## 2026-10-18 H1 LINTRACK-065 continuation / model9999 / A4000 평가 전용

[Publication record](publications/2026-10-18_h1_lintrack065_model9999_a4000/README.md): PERSONAL L40S training Run `20261018-074037-h1-top06-same-reward-to10k`의 `model_9999.pt` SHA와 연결한 PERSONAL Linux A4000 camera-off scenario7. COMPLETE/non-smoke, 3,072 time-window cohorts / 3,072 episode rows, 세 파일 ZIP, 영상 없음. 학습 archive에 checkpoint index가 없어 이를 생성하지 않았으며 raw evaluation `source_run_id`는 null 그대로다. 정책 분석·채택 대기/HOLD; 공식 점수나 비교 보고서가 아니다.

## 2026-10-18 H1 ORIENT-100 continuation / model9999 / A4000 평가 전용

[Publication record](publications/2026-10-18_h1_orient100_model9999_a4000/README.md): OFFICIAL TOP03 continuation의 checkpoint SHA와 연결한 PERSONAL Linux A4000 camera-off scenario7 COMPLETE/non-smoke. 3,072 time-window cohorts / 3,073 episode rows, three-file ZIP, 영상 없음. 학습과 평가 원본은 별도 보존하며 정책 판정은 HOLD다.

## 2026-10-18 H1 ACTRATE-0001 + FEETSLIDE-035 continuation / model9950 / A4000 평가 전용

[Publication record](publications/2026-10-18_h1_actrate0001_feetslide035_model9950_a4000/README.md): OFFICIAL Run `20261018-062435-h1-top04-same-reward-to10k`의 keeper9950 SHA로 연결한 PERSONAL Linux A4000 camera-off scenario7. COMPLETE/non-smoke, 3,072개 time-window cohort 검증 PASS, 재시작 포함 3,074 episode rows. 원본 ZIP 3파일, 영상·비교 보고서·공식 점수 없음. 정책 분석·채택 대기/HOLD.

## 2026-10-18 H1 ACTRATE-0003 same-reward continuation / model9950 / A4000 평가 전용

[Publication record](publications/2026-10-18_h1_actrate0003_model9950_a4000/README.md): OFFICIAL Run `20261018-032205-h1-top02-same-reward-to10k`의 keeper `model_9950.pt` SHA로 연결한 PERSONAL Linux A4000 camera-off scenario7. COMPLETE/non-smoke, 128env × 3seed × 8case = 3,072행. 원본 ZIP은 3파일이며 **6영상·비교 보고서·공식 점수는 없다**. 학습 archive와 별도인 평가 결과다.

## 2026-10-18 H1 joint tracking continuation / model9950 / A4000 평가 전용

[Publication record](publications/2026-10-18_h1_joint_tracking_model9950_a4000/README.md): OFFICIAL continuation Run `20261018-021823-h1-top01-same-reward-to10k`의 keeper9950 SHA로 연결한 PERSONAL Linux A4000 camera-off scenario7. COMPLETE/non-smoke, 128env × 3seed × 8case = 3,072행 검증 PASS. 원본 ZIP은 3파일이며 **6영상·비교 보고서·공식 점수는 없다**. 학습 원본과 별도로 보존한다.

## 2026-10-18 H1 lin=.75 + action=-.0001 fresh3K / model2850

[Publication record](publications/2026-10-18_h1_lin075_action0001_model2850/README.md): OFFICIAL train Run `20261017-140610-h1-lintrack-075-actrate-0001-term-50-fresh3k`의 checkpoint-index SHA와 연결한 Windows PERSONAL 6영상 + camera-off scenario7 평가. COMPLETE/non-smoke, 18-file ZIP, 3,072 episode rows. 정책 채택이나 공식 점수 판정은 포함하지 않는다.

## 2026-10-17 H1 lin=.65 / ang=.60 / action=-.0003 fresh5K / model4950

[Publication record](publications/2026-10-17_h1_joint_tracking_model4950/README.md): OFFICIAL joint-tracking keeper4950 SHA로 연결한 Windows PERSONAL 6영상·scenario7 COMPLETE/non-smoke. 18파일 CRC·6영상 체크섬 PASS, 128env×3seed×8case·3072행. 정책 보고서 대기/HOLD; 새 학습·공식 점수가 아니다.

## 2026-10-17 H1 action=-0.0002 fresh3K / model2950

[Publication record](publications/2026-10-17_h1_action0002_model2950/README.md): OFFICIAL ACTRATE-0002 fresh3K keeper SHA matches this PERSONAL Windows six-video + scenario7 completed record. The 18-file ZIP CRC and video SHA checks pass; 3,072 episode rows, non-smoke.

## 2026-10-16 H1 action=-0.0003 fresh3K / model2950

[Publication record](publications/2026-10-16_h1_action0003_model2950/README.md): OFFICIAL Run `20261016-033023-h1-actrate-0003-fresh3k` keeper SHA로 연결한 PERSONAL Windows 6영상·scenario7 완료 자료. 원본18파일·CRC·영상 체크섬 확인, 3072행/non-smoke. 정책 분석 대기/HOLD; 새 학습·공식 점수가 아니다.

## 2026-10-15 H1 lin=.55 resume 평가 수납

- [lin=.55 + action=-.0001 / model4650](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261015-exp-h1-action-first-planar-tracking-switch-lin055-model4650-video-eval): OFFICIAL train Run `20261015-105910-h1-actrate0001-lintrack-055-from2700-plus2k`에 SHA `e8a358a50832f6653b1e558788a5a676ab9a849d3ec6c64e3ed2430e9ff41814`로 연결한 PERSONAL Windows 평가. 18파일·6영상·scenario7 COMPLETE, 정책 분석·채택 대기. [게시 manifest](publications/2026-10-15_h1_lin055_model4650/publication_manifest.json).

## 현재 게시 기준 — 2026-10-13

새 Windows H1/Go2 통합 6영상·camera-off 평가 ZIP의 게시 위치는 비공개 `SE3C/naver-issacsim-eval`이다. 실행기는 로컬 결과를 생성하며, Release 게시는 별도 명시적 작업이다. 개인 서버 학습·native 영상의 자동 게시 위치는 NVIDIA 저장소로 유지한다. 공용 publisher의 기본 repo를 일괄 변경하지 않는다.

기존 NVIDIA Release는 링크와 애셋을 그대로 보존한다. 아래 역사적 목록은 원본 주소이며, 2026-10-15 복사 이관 상태와 새 Eval 주소는 별도 표에서 확인한다. 분석 Markdown은 analysis 저장소에 보존한다.

## 2026-10-15 기존 통합 평가 10개 복사 이관

완료: 10/10 Release 게시 및 30/30 애셋 원격 크기·SHA-256 대조 PASS. 기존 NVIDIA 제목·본문·애셋도 변경 없음 확인. [최종 검증 기록](publications/migration_2026-10-15/verification.json). 기존 원본 삭제는 수행하지 않았다.

원본 세 애셋(ZIP·checksum·publication manifest)을 바이트 변경 없이 Eval Release로 복사한다. 기존 manifest 안의 NVIDIA 게시 주소는 역사적 필드로 보존하며, 새 게시 위치는 [이관 manifest](publications/migration_2026-10-15/migration_manifest.json)가 정의한다. 원본 Release/tag는 삭제·변경하지 않는다. 새 annotated tag는 Eval 이관 기록 commit을 가리키며 실제 실행 source commit이 아니다. 영상 재생성이나 새 평가를 수행한 것이 아니다.

| 평가 | 원본 | 새 게시 위치 |
| --- | --- | --- |
+| [분석] H1 ACTRATE-0001 fresh 10K · model_9999 · PERSONAL videos + full evaluation | [NVIDIA 원본](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261011-exp-h1-action-rate-relaxation-model9999-video-eval) | [Eval 복사본](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261011-exp-h1-action-rate-relaxation-model9999-video-eval) |
| [분석] H1 ACTRATE-0001 → lin=0.65 · PERSONAL model_4650 videos + evaluation | [NVIDIA 원본](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261011-exp-h1-action-first-planar-tracking-switch-model4650-video-eval) | [Eval 복사본](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261011-exp-h1-action-first-planar-tracking-switch-model4650-video-eval) |
| [분석] H1 ANGTRACK-065 · model_2950 · PERSONAL videos + full evaluation | [NVIDIA 원본](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261010-exp-h1-angular-tracking-boost-model2950-video-eval) | [Eval 복사본](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261010-exp-h1-angular-tracking-boost-model2950-video-eval) |
| [분석] H1 ACTRATE-001 model_2850 PERSONAL 6-terrain video + scenario7 evaluation | [NVIDIA 원본](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261010-exp-h1-action-rate-smoothing-model2850-video-eval) | [Eval 복사본](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261010-exp-h1-action-rate-smoothing-model2850-video-eval) |
| [분석] H1 ACTRATE-0001 · model_2700 · PERSONAL videos + full evaluation | [NVIDIA 원본](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261010-exp-h1-action-rate-relaxation-model2700-video-eval) | [Eval 복사본](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261010-exp-h1-action-rate-relaxation-model2700-video-eval) |
| [분석] H1 LINTRACK-075 corrected 5K · model_4997 · PERSONAL videos + full evaluation | [NVIDIA 원본](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261009-lintrack-075-corrected5k-model4997-video-eval) | [Eval 복사본](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261009-lintrack-075-corrected5k-model4997-video-eval) |
| [분석] H1 h1-submit-2 / TERM-50 · model_2800 · PERSONAL Windows 6영상 + 평가 | [NVIDIA 원본](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261008-exp-h1-rough-terrain-orientation-relaxation-model2800-control-video-eval) | [Eval 복사본](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261008-exp-h1-rough-terrain-orientation-relaxation-model2800-control-video-eval) |
| [분석] Go2 g2-submit-3 · original model_4800 · PERSONAL · 6-terrain + scenario7 evaluation | [NVIDIA 원본](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-go2-20261009-g2-submit-3-model4800-video-eval) | [Eval 복사본](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-go2-20261009-g2-submit-3-model4800-video-eval) |
| [분석] H1 ORIENT-100 · model_2850 · PERSONAL Windows 6영상 + 평가 | [NVIDIA 원본](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261007-exp-h1-rough-terrain-orientation-relaxation-model2850-video-eval) | [Eval 복사본](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261007-exp-h1-rough-terrain-orientation-relaxation-model2850-video-eval) |
| [분석] Go2 LINTRACK-125 · PERSONAL Windows · model_7050 · 6영상 + scenario7 평가 | [NVIDIA 원본](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-go2-20261004-exp-go2-planar-tracking-terrain-progression-model7050-video-eval) | [Eval 복사본](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-go2-20261004-exp-go2-planar-tracking-terrain-progression-model7050-video-eval) |

## 출처와 tag 경계

새 평가 Release의 annotated tag는 eval 저장소의 게시 기록 commit을 가리킨다. 이 commit은 실제 task/training source commit이 아니다. 본문·manifest에는 원본 checkpoint SHA, 부모 train Run/Release, 실제 task source repo/commit, evaluator source/fingerprint, ZIP SHA를 구분해서 기록한다. 확인하지 못한 provenance는 추측하지 않는다. 기존 NVIDIA tag는 재작성하지 않는다. canonical raw 보존 위치는 Originals를 유지한다.

## 현행 eval 저장소의 게시 현황

2026-10-15 신규 게시 기록 (Windows PERSONAL; 정책 분석/채택은 대기):

- [ACTRATE-0001 무변경 +2K · model_4699](publications/2026-10-15_h1_actrate0001_unchanged_cont2k_model4699/README.md)
- [action-rate 복원 +2K · model_4650](publications/2026-10-15_h1_actrate_return2700_model4650/README.md) — 학습 terminal model_4699와 구별.
- [LINTRACK-065 fresh5K · model_4950](publications/2026-10-15_h1_lintrack065_fresh5k_model4950/README.md)

각 원본 ZIP은 6영상과 별도 full camera-off H1 scenario7을 포함한다. 학습 Run과의 연결은 checkpoint SHA/index로 기록하며 원본의 null source_run_id나 imported-parent provenance는 고쳐 쓰지 않는다. 공식 점수나 A/B 비교가 아니다.

2026-10-14 신규 게시 기록:

- [H1 ACTRATE-0001 + feet=0.25 · model_2950](publications/2026-10-14_h1_action_airtime/README.md): PERSONAL Windows 6영상 + full 평가. 원본 학습 Run과 checkpoint SHA로 연결한다.
- [H1 ACTRATE-0001 + feet_slide=-0.35 · model_2950](publications/2026-10-14_h1_action_feet_slide/README.md): PERSONAL Windows 6영상 + full 평가. 위 정책과 파일명은 같지만 SHA는 다르다.

역사적 상태: 2026-10-13 GitHub API 조회 시 이 저장소의 Release는 0개였다. 현재 게시/이관 상태는 위의 날짜별 기록과 이관 표를 따른다.

## 분석 — Windows PC 영상·평가 보존 목록 10개 (기존 EVAL-PC)

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

## 분석 — 개인 NVIDIA 서버 보조평가 보존 목록 2개 (기존 EVAL)

아래 두 건은 개인 L40S에서 수행한 보조평가·native 시각 비교다. Windows 통합 평가나 신규 학습 Run, 공식 점수가 아니며 원래 Release에서 계속 찾는다.

- [[분석] LINTRACK-150-LINZ-2 · PERSONAL · fixed checkpoint evaluation · seed 4201, d1](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-go2-20260915-lintrack-150-linz-2-checkpoint-quant-eval-seed4201-d1)
- [[분석] LINTRACK-150-LINZ-2 · PERSONAL · native video comparison · checkpoints 4800/4900](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-go2-20260915-lintrack-150-linz-2-4800-vs-4900-native-video)

## 2026-10-18 H1 TOP07 / TOP08 A4000 scenario7 evaluations — Releases published and verified

- **TOP07 / ACTRATE-001, `model_9950.pt`:** COMPLETE/non-smoke PERSONAL Linux RTX A4000 camera-off scenario7, 128 envs × seeds 4201/4202/4203 × eight cases, 3,072 episode rows, 20 seconds/case. Policy SHA-256 `642255c41cf09dac6a9401985f70cce0177c41cd87b85aa085a5f35bbbdf09c6`. ZIP `h1-top07-same-reward-to10k_model_9950_A4000_evaluation_20261018.zip`, 547,067 bytes, SHA-256 `00967e49176bcd03742db776f2d8ae4ce8ea633a6a9d9435cdac0cc26fcb953a`. Training linkage by checkpoint SHA; raw `source_run_id` is null. Receipt: [TOP07 evaluation](publications/2026-10-18_h1_actrate001_model9950_a4000/README.md). [Verified Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261018-exp-h1-action-rate-smoothing-model9950-a4000-eval).
- **TOP08 / LINTRACK-065 + ACTRATE-0001, `model_9999.pt`:** COMPLETE/non-smoke PERSONAL Linux RTX A4000 camera-off scenario7, same 128-env/three-seed/eight-case protocol, 3,072 episode rows, 20 seconds/case. Policy SHA-256 `852c95fa0fcfabec456572541c24dad68385084ce480aa09b8422597b704929b`. ZIP `h1-top08-same-reward-to10k_model_9999_A4000_evaluation_20261018.zip`, 546,055 bytes, SHA-256 `551b3683ae1b618a49180e9528159e1636fe391c383bdae208f5d1515da22c48`. Training linkage by checkpoint SHA; raw `source_run_id` is null. Receipt: [TOP08 evaluation](publications/2026-10-18_h1_lin065_actrate0001_model9999_a4000/README.md). [Verified Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261018-exp-h1-action-first-planar-tracking-switch-model9999-a4000-eval).

These evaluation-only records include no videos, comparison report, policy analysis, or official score. Original ZIPs remain untouched in Downloads; byte-preserving copies and the three exact ZIP members are preserved at the canonical Originals paths recorded in each manifest. Both Eval Releases and their asset size/digests are verified.
