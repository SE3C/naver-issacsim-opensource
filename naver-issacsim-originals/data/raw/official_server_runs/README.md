# 공식 서버 실행 결과 원본

- [2026-10-18 H1 TOP07 ACTRATE-001 continuation toward 10K](h1/2026-10-18_actrate001_resume10k/README.md): OFFICIAL Run `20261018-092452-h1-top07-same-reward-to10k`, completed/exit 0/validation PASS; resumed from 2950 for 7050 requested iterations, final keeper `model_9950.pt`. Separate PERSONAL A4000 evaluation. Training and evaluation Releases published/verified; policy analysis remains pending/HOLD. Imported-parent provenance remains unverified.

- [2026-10-18 H1 TOP09 LINTRACK-075 + ACTRATE-0001 continuation toward 10K](h1/2026-10-18_105744_lin075_action0001_resume10k/README.md): OFFICIAL Run `20261018-105744-h1-top09-same-reward-to10k`, completed/exit0/validation PASS, imported2950 +7050 requested, final saved keeper9950. Parent SHA matches the earlier OFFICIAL fresh3K index; raw imported-parent metadata remains unverified. Separate A4000 evaluation is PERSONAL, not an official score.

- [2026-10-18 H1 ORIENT-100 continuation toward 10K](h1/2026-10-18_orient100_resume10k/README.md): OFFICIAL Run `20261018-045508-h1-top03-same-reward-to10k`, completed/exit 0/validation PASS; `h1-submit-2 + flat_orientation_l2=-1.0`, final `model_9999.pt`. Imported-parent provenance remains unverified.
- [2026-10-18 H1 h1-submit-2 unchanged continuation toward 10K](h1/2026-10-18_term50_resume10k/README.md): OFFICIAL Run `20261018-075224-h1-top05-same-reward-to10k`, completed/exit 0/validation PASS; actual resume from 2950, final saved keeper `model_9950.pt`. Plan had described fresh training; archive proves resume. Imported-parent provenance remains unverified; the separate PERSONAL A4000 evaluation is complete and its publication record is in `naver-issacsim-eval/publications/2026-10-18_h1_submit2_model9950_a4000/`.

- [2026-10-18 H1 ACTRATE-0001 + FEETSLIDE-035 continuation toward 10K](h1/2026-10-18_actrate0001_feetslide035_resume10k/README.md): OFFICIAL Run `20261018-062435-h1-top04-same-reward-to10k`, completed/exit 0/validation PASS; latest keeper `model_9950.pt`. Imported-parent provenance remains explicitly unverified in raw metadata.

- [2026-10-17 H1 joint tracking + 자세·고관절 완화 fresh3K](h1/2026-10-17_072659_joint_tracking_posture_fresh3k/README.md): 후보2 OFFICIAL COMPLETED/exit0/PASS. 평가2850과 최신 keeper2950을 구분한다.

- [2026-10-17 H1 joint tracking fresh5K](h1/2026-10-17_joint_tracking_fresh5k/README.md): OFFICIAL COMPLETED/exit0/PASS; lin=.65, ang=.60, action=-.0003. 원본 archive와 keeper4950/auto-best4800 identity 보존. 행동 평가·분석 대기.

공식 서버에서 내려받은 학습 결과와 관련 export·제출 snapshot을 로봇과 실행 시작 시각별로 보관한다. 아래는 원본 탐색 색인이며 현재 성능 판정은 [analysis registry](https://github.com/SE3C/naver-issacsim/blob/main/research/EXPERIMENTS.md)를 따른다.

## 경로 규칙

```text
<robot>/<YYYY-MM-DD_HHMMSS>_<experiment>/
```

- 파일 내용과 다운로드 당시 파일명은 변경하지 않는다.
- 동일한 내용의 별칭 파일도 원본 묶음에 포함하고 실행별 `README.md`에 해시 관계를 기록한다.
- `.pt`, `.onnx`, 영상 등 바이너리는 Git LFS로 관리한다.
- 해석·성능 비교·전략 문서는 분석 저장소에 별도로 작성한다.

## 학습 원본 — 기존 수납 기록

아래 상태는 당시 수납 기록이다. 후속 점수·분석·제출 여부는 registry에서 확인하고 보존된 README의 미확인 표현을 현재 상태로 확대하지 않는다.

| 로봇 | canonical 폴더 | 상태 |
| --- | --- | --- |
| H1 | [baseline 300iter](h1/2026-08-24_124413_baseline_300iter/README.md) | 초기 300회 참고용; 진단 증거 불완전 |
| H1 | [baseline 1K](h1/2026-09-08_230725_baseline_1k/README.md) | 공식 baseline 1K |
| H1 | [TERM50 5K](h1/2026-09-08_232333_term50_5k/README.md) | 공식 TERM50 5K·2라운드 정책 계보 |
| H1 | [AIRTIME-025 fresh10K](h1/2026-09-27_213434_h005_fresh10k/README.md) | H-005 R05 공식 fresh 10K 완료·evidence PASS; 사용자 4라운드 제출 보고 및 별도 제출 snapshot Release 확인. 수납 당시 포털 수령증·점수와 `policy.pt`의 정확한 numbered checkpoint 연결은 미확인 |
| Go2 | [baseline 1K](go2/2026-09-13_145026_baseline_1k/README.md) | 공식 baseline 1K 완료 |
| Go2 | [ANGXY-012 1K](go2/2026-09-14_012909_g5_angvelxy_m012_1k/README.md) | G-004 1K 완료; 성능 판정은 분석 저장소 참조 |
| Go2 | [LINTRACK-150-LINZ-2 interrupted](go2/2026-09-14_084321_a1_fresh_5k_interrupted/README.md) | G-005 fresh 5K 중단·validation FAIL |
| Go2 | [4800→5K recovery](go2/2026-09-14_132725_a1_resume_4800_to_5k/README.md) | G-005 4800 출발 recovery 완료; uninterrupted fresh 5K가 아님 |

## 학습 원본 — 최근 수납 자료

2026-10-18 수납: [TOP01 ANG070 +3K continuation](h1/2026-10-18_230639_top01_angtrack060_plus3k/README.md). OFFICIAL Run `20261018-140635-h1-top01-angtrack060-plus3k`, COMPLETED/exit 0/validation PASS; 3,000 requested iterations, automatic-best `model_11650.pt`, latest keeper `model_12900.pt`. Imported `model_9950.pt` SHA matches the known TOP01 parent continuation, while raw parent metadata stays null/unverified. Outer archive SHA-256 `8a0c8c8e36ab34ed25357e70a7963d5613a72d6a9f5802f98113c64e0b0c6b31`.

2026-10-16 수납: [action=-0.0003 fresh3K](h1/2026-10-16_actrate0003_fresh3k/README.md). OFFICIAL H1 Run `20261016-033023-h1-actrate-0003-fresh3k`, COMPLETED/PASS. 원본 다운로드 archive와 체크섬을 보존했으며, 행동 평가·채택 판단은 아직 진행하지 않았다.

2026-10-16 수납: [action=-0.0002 fresh3K](h1/2026-10-16_actrate0002_fresh3k/README.md). OFFICIAL H1 Run `20261016-150803-h1-actrate0002-fresh3k`, COMPLETED/PASS. 원본 다운로드 archive와 체크섬을 보존했으며, 행동 평가·채택 판단은 별도 분석 registry에서 추적한다.

2026-10-14 수납: [ACTRATE-0001 + AIRTIME-025 fresh3K](h1/2026-10-13_234624_actrate0001_airtime025_fresh3k/README.md), [ACTRATE-0001 + feet_slide=-0.35 fresh3K](h1/2026-10-14_003321_actrate0001_feet_slide_fresh3k/README.md). 둘 다 OFFICIAL COMPLETED/PASS이며 별도의 PERSONAL Windows 평가와 SHA로 연결한다.

2026-10-14 수납: [LINTRACK-065 fresh5K](h1/2026-10-14_171907_lintrack065_fresh5k/README.md). OFFICIAL H1 fresh Run `20261014-081901-h1-lintrack-065-fresh5k`, COMPLETED/PASS; 행동 평가와 채택 판단은 미완료다.

2026-10-14 수납: [ACTRATE-0001 unchanged model_2700 continuation +2K](h1/2026-10-14_201142_actrate0001_unchanged_cont2k/README.md). OFFICIAL Run `20261014-111135-h1-actrate-0001-unchanged-cont2k`, COMPLETED/PASS. Parent checkpoint SHA matches the earlier ACTRATE-0001 `model_2700`; raw metadata's imported-checkpoint provenance flags remain explicitly unverified.

2026-10-14 수납: [ACTRATE-0001 parent에서 action-rate baseline 복원 +2K](h1/2026-10-14_232208_actrate0001_return2700_2k/README.md). OFFICIAL Run `20261014-142200-h1-actrate-return2700-2k`, COMPLETED/PASS. Parent SHA matches ACTRATE-0001 `model_2700`; raw metadata의 imported-checkpoint provenance flag는 미검증 상태로 보존한다.

| 로봇 | canonical 안내 | 구분 |
| --- | --- | --- |
| H1 | [ORIENT-100 fresh3K](h1/2026-10-06_223521_orient100_fresh3k/README.md) | OFFICIAL 학습 |
| H1 | [TERM-50 fresh3K control](h1/2026-10-08_152738_term50_fresh3k_control/README.md) | OFFICIAL 학습; 새 제출 preset 아님 |
| H1 | [ACTRATE-0001 fresh3K](h1/2026-10-09_232356_actrate0001_fresh3k/README.md) | OFFICIAL 학습 |
| H1 | [ANGTRACK-065 fresh3K](h1/2026-10-10_005350_angtrack065_fresh3k/README.md) | OFFICIAL 학습; Run ID UTC / native 폴더 KST 구분 |
| H1 | [ACTRATE-001 fresh3K](h1/2026-10-10_215330_actrate001_fresh3k/README.md) | OFFICIAL 학습; ACTRATE-0001과 다른 설정 |
| H1 | [ACTRATE-0001→lin=.65 resume+2K](h1/2026-10-11_004932_actrate0001_lintrack065_resume2700_plus2k/README.md) | OFFICIAL 이어학습; 부모 model_2700 |
| H1 | [ACTRATE-0001 fresh10K](h1/2026-10-11_actrate0001_fresh10k/README.md) | OFFICIAL 학습; fresh3K와 별도 Run |

## export·실제 제출 snapshot — 학습 Run과 구분

| 로봇 | canonical 안내 | 구분 |
| --- | --- | --- |
| Go2 | [original4800 export](go2/2026-09-15_a1_original4800_submission/README.md) | G-005 original-4800 공식 서버 export·제출 ZIP 원본 |
| Go2 | [Round-5 model7450 제출 manifest](go2/2026-10-06_round5_model7450_submission/submission_manifest.json) | policy·env·기술 리포트 snapshot; 별도 학습 아님 |
| H1 | [Round-6 model9999 제출](h1/2026-10-11_round6_model9999_submission/README.md) | policy·env·기술 리포트 snapshot; 별도 학습 아님 |

## 역사적 경로에 함께 보존된 PERSONAL 분석

ACTRATE-001 아래 [Windows model2850 평가 원본](h1/2026-10-10_215330_actrate001_fresh3k/personal_windows_eval_20261010/README.md)은 **PERSONAL 분석**이다. 기존에 안내한 `h1/2026-10-10_215330_actrate001_fresh3k/post_training_personal_evaluations/`는 **2026-10-14 현재 Git `main` tree에 없으므로 유효한 저장소 탐색 링크로 취급하지 않는다**(외부 보존본의 존재 여부는 미확인). 부모 폴더가 공식 학습 원본이어도 이 결과를 OFFICIAL 평가로 분류하지 않는다. 원본 경로·bytes는 유지하며 [개인 학습·분석 색인](../private_server_runs/README.md)에도 연결한다.

위 목록은 현재 Git에 있는 로봇별 보존 폴더 18개를 안내한다. Release에만 연결된 추가 raw run을 임의로 로컬 보존 완료라고 표시하지 않는다. 전체 공식 Release는 [Originals Releases](https://github.com/SE3C/naver-issacsim-originals/releases)에서 확인한다.

`baseline_300iter`는 초기 참고자료이자 불완전한 진단 묶음이므로 Release 대상에서 제외하고 이 canonical 경로에만 보존한다.
