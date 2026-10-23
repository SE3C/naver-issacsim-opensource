---
title: "Windows Go2/H1 고정 6영상과 camera-off 평가"
purpose: "PERSONAL Windows 실행기 6종의 역할, 기본 인자, 산출물, 검증 근거와 해석 한계"
sources:
  - "C:/NCRC/go2_6terrain_video.bat 및 go2_6terrain_video.ps1"
  - "C:/NCRC/compare_policies.bat 및 compare_policies.ps1"
  - "C:/NCRC/h1_6terrain_video.bat 및 h1_6terrain_video.ps1"
  - "naver-issacsim-eval/WINDOWS_H1_WORKFLOW.md"
  - "../operations/windows_go2_video_evaluation/evaluation_2950_verified.json"
  - "../operations/windows_go2_video_evaluation/evaluation_7050_verified.json"
  - "../operations/windows_go2_video_evaluation/installed_tools_manifest.json"
  - "../incoming/other/reviewed/GO2_20260929-154342-go2-lintrack-125-fresh7500-official_VS_20260928-230114-go2-lintrack125-fresh3k-r5-official_DEEP_ANALYSIS_20260930.md"
  - "00_START_HERE_CONTEXT_AND_MAP.md, 07_QUADRUPED_TRAINING_CODE.md, 11_SERVER_OPERATIONS.md, 15_OPTUNA_REWARD_DECISION_ENGINE.md, 17_ISSACSIMZ_VIDEO_OPERATIONS.md, 19_ISSACSIMZ_EXTERNAL_EVIDENCE_CLI.md"
---

# Windows Go2/H1 고정 6영상과 camera-off 평가

**2026-10-18 LIN075 + ACT0001/2850 보고서 수신:** [Run·SHA·검토](../experiments/h1/analysis/2026-10-18_H1_LIN075_ACTION0001_MODEL2850_POLICY_REVIEW.md). 평가2850 SHA`82384210…934f959`는 OFFICIAL140610 train index와 연결되고 raw source_run_id/preset=null은 유지한다. 3072행 COMPLETE/non-smoke 보고서 판정은 **HOLD**, keeper2950은 미평가. 보고된 boxes 짝수500/1000black·홀수정상과6영상f999몸체소실은 capture/종료 시각 결함으로 정책 낙상과 구분한다. 원인 확정이나 수납자의 새 렌더 재현은 아니며 MP4·첨부 코드·원 episode를 재실행하지 않았다.

**2026-10-17 후보2 자세·고관절 완화 수납:** [model2850/4a343750의 원문·실제 Run·검토](../experiments/h1/analysis/2026-10-17_H1_JOINT_TRACKING_POSTURE_MODEL2850_POLICY_REVIEW.md). OFFICIAL fresh3K와 기존 index/publication SHA로 연결된 Windows PERSONAL 6영상·scenario7 COMPLETE(128env×3seed×8case·3072행)의 보고서는 **HOLD**다. 생존3072/3072에도 정지/횡이동 후진과 rough 속도 손실이 남는다. 원 source_run_id/preset=null은 보존하고 평가 baseline snapshot을 학습 reward로 바꾸지 않는다. 보고서상 전1000프레임 축소 픽셀 검사에서 stairs f0/f2·나머지 f0만 black, 교대 결함은 없었다. 수납자의 MP4/원 episode 재실행 검증은 아니다. 최신 keeper2950은 미평가이며 공식 점수·제출·A/B 없음.

**2026-10-17 joint tracking 수납 완료:** [keeper4950/2df05840의 원문·Run·검토](../experiments/h1/analysis/2026-10-17_H1_JOINT_TRACKING_MODEL4950_POLICY_REVIEW.md). OFFICIAL joint-tracking fresh5K와 SHA로 연결된 Windows PERSONAL 6영상·128env×3seed×8case·3072행 평가 및 보고서를 보존했다. **행동 HOLD**, 공식 점수·제출 아님. 수납자는 원문 표/JSON을 대조했으나 원 episode·첨부 코드·MP4를 재실행하지 않았다. 보고서의 첫4영상 검정프레임 전수검사(f0만black), 경사2개 선택프레임 검사와 6영상 f999 본체 소실을 구분한다. 이는 전 영상 전프레임 무결함 검증도, 정책 낙상 판정도 아니다. 원 null source_run_id/preset 및 평가 baseline snapshot은 학습 계보·reward를 대체하지 않는다. 기존 LINTRACK0654950과 다른 SHA며 raw CPU 비교는 미실행이다.

**2026-10-17 action=-.0002 수납 완료:** [원문 ZIP·Run/SHA·HOLD 검토](../experiments/h1/analysis/2026-10-17_H1_ACTION0002_MODEL2950_POLICY_REVIEW.md). OFFICIAL fresh3K Run `20261016-150803-h1-actrate0002-fresh3k`의 keeper2950 SHA `eaa7a50c…ac4d34fb`와 연결된 PERSONAL 평가(128env×3seed×8case,3072행) 및 정책 보고서가 보존됐다. 원 source_run_id/preset=null은 유지한다. 수납자는 패키지 표/JSON과 본문을 대조했으며 원 episode 재집계·영상 재판독·첨부 코드 실행은 하지 않았다. 평가 snapshot의 action=-.0005를 실제 학습값 -.0002로 오인하지 않는다. 상대 정책 CPU 비교는 별도 미실행이다.

**판정 범위:** H1 공식 7시나리오와 로컬 scenario7의 8 case에는 계단·박스가 없다. 두 지형의 영상은 보조 관찰이며 완주 미입증만으로 공식 후보를 자동 REJECT하지 않는다. 영상·내부 지표의 이점도 공식 점수 개선을 보증하지 않는다. 기존 보고서 HOLD는 보존하고 제출 경쟁력과 광의의 보행 능력 중 어떤 목표의 판정인지 밝힌다. [현재 의사결정 원칙](14_H1_NEXT_RUN_PARAMETER_COMPARISON.md).

**2026-10-16 action=-.0003 수납 완료:** OFFICIAL fresh3K Run `20261016-033023-h1-actrate-0003-fresh3k` keeper2950 SHA `1cc2c03197097c21c642e8373c760b25664b9c859ed75b5dc07582a770473c4b`와 연결된 PERSONAL Windows 18파일/6영상·scenario7 COMPLETE/non-smoke(3072행) 및 [정책 보고서](../experiments/h1/analysis/2026-10-16_H1_ACTION0003_MODEL2950_POLICY_REVIEW.md)를 수신했다. [Eval Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261016-exp-h1-action-rate-relaxation-action0003-model2950-video-eval), ZIP SHA `55adccbbed0d4022f27fd6908d4dfe78b34b1f04918b04782870fae17fa0346e`. **행동 HOLD**이며 새 학습·공식 점수·A/B가 아니다. 원문은 선택·인접 프레임에서 f0 black/f999 몸체 소실 경계 이상을 보고했고 중앙 계단 통과는 미입증이다. 전프레임 무결함 검증이나 이번 반영자의 영상 재판독이 아니다. 원본 source_run_id/preset=null은 외부 checkpoint SHA 연결과 구분해 보존한다.

**2026-10-16 기존자료 비교 수납:** [lin=.55 4정책 코호트 비교](../experiments/h1/analysis/2026-10-16_H1_LIN055_FOUR_POLICY_COHORT_INTAKE.md)는 기존 camera-off episode만 비교했고 영상·GPU를 다시 실행하지 않았다. `.55` 범용 HOLD 유지; 동일 protocol/key를 동일 실제 지형이나 독립 학습 반복으로 확대 해석하지 않는다. 이전 ‘raw 비교 대기’는 이 후속 이전 상태다.

**2026-10-15 실행기 진단 추가:** H1/Go2는 캡처 직후와 인코딩 직전의 프레임 번호·shape/dtype/픽셀 최댓값을 `<terrain>.capture_diagnostics.json`에 기록한다. 성공 시 `C:\NCRC\<robot>-video-suite-logs\suite-<id>\`, 실패 시 보존된 work에 남으며 기존 18파일 ZIP에는 추가하지 않는다. 첫 프레임 외 완전 검정이나 두 시점의 probe 변화는 경고만 출력한다. 추가 렌더·프레임 보정·자동 재시도·평가 변경은 없다. 이 기록은 캡처 시점부터 검정인지 구분하는 단서이며 encoder 출력 검사나 원인 해결은 아니다. 이번 변경의 GPU 재현 검증은 하지 않았다.

**2026-10-15 lin=.55 후속 분석 수납:** [model4650/e8a358a5](../experiments/h1/analysis/2026-10-15_H1_LINTRACK055_MODEL4650_POLICY_REVIEW.md)의 학습·PERSONAL full 평가·보고서는 완료, 행동 후보 **HOLD**다. 보고서상 stairs는 f0+홀수500개,총501/1000 black이고 유효 짝수 프레임에 이동이 보인다. 다른5영상은 f0만 black. 캡처 결함과 정책 실패를 분리하며 이번 수납에서 재렌더하지 않았다.

**2026-10-15 기존 CSV 후속 비교:** [다음 가설 수납](../experiments/h1/analysis/2026-10-15_H1_NEXT_HYPOTHESIS_DECISION_INTAKE.md)은 옛 lin=.65 resume4650(`ce7ad586…`) 대 무변경4699의 저장 집계 CSV 비교다. 진행 이득과 yaw/횡잔류 비용이 공존하며 HOLD 유지. 원 episode·6 MP4 재검증·비교 CLI/GPU 실행이 아니다. 당시 lin=.55 제안은 이후 실행·보고서 수납 완료됐고 당시 action=-.0003 fresh 제안은 위 완료·보고서 HOLD로 갱신됐고 resume만 미실행이다. 실행기나 평가 프로토콜을 바꾸지 않는다.

## 2026-10-15 부모·무변경·복원 3정책 CPU 비교 보고서 수납

[원문·CSV·수납](../experiments/h1/analysis/2026-10-15_ACTRATE_PARENT_UNCHANGED_RESTORATION_COMPARISON_INTAKE.md): A2700/B4699/C 복원4650(`a8249db4…`)의 기존PERSONAL 결과를 외부 에이전트가 CPU 비교했다. 각3,072 episode·source/config/cohort key 일치가 보고됐고 B는 **이번 범용·전진/험지 대표 후보에서 REJECT**, A/C는 HOLD다. 원 null preset/source_run_id와 imported-parent provenance는 유지한다. 영상 감사는 A stairs502/1000·B rough501/1000 black, 나머지16영상은 f0만 black으로 보고한다. 유효 프레임 관찰을 보존하며 캡처 결함을 낙상으로 세지 않는다. 이번 수납은 보고서/CSV 검토이며 첨부 스크립트 실행·GPU 재평가·재렌더가 아니다.

## 2026-10-15 H1 두 정책 6영상·camera-off 평가 **사후 행동 보고서** 수납

[원문 및 통합 판정](../experiments/h1/analysis/2026-10-15_H1_MODEL4650_LINTRACK065_POLICY_REVIEW.md). ACTION 복원 +2K `model_4650.pt`(SHA `a8249db4…25b84ea`), LINTRACK-065 fresh5K `model_4950.pt`(SHA `b7528923…ece`)의 기존 PERSONAL Windows 통합 ZIP 2건(각 6 MP4+camera-off H1 `scenario7` 3,072 episode)의 **사용자 제공 원자료 분석 MD**를 보존·수납했다. 두 보고서상 3,072/3,072 timeout, contact 종료 0, 실행 COMPLETE/non-smoke이며 범용 행동 후보 **모두 HOLD**. 본 Git 수납은 원본 ZIP/MP4/체크포인트를 다시 디코딩·재실행하거나 GPU를 사용한 작업이 아니다.

- ACTION 복원 4650: H1 body 전진 leak 0.282m, H3 world 최종 순변위 0.167m, rough H5 mean/P05/min 진행 8.769/7.970/4.845m (stall>0.05 7/384). 모든 여섯 영상은 첫 f0 검정 프레임을 포함하지만 교대 검정 문제는 보고되지 않았다.
- LINTRACK fresh4950: H1 body leak 0.063m, H3 world 최종 순변위 **3.102m**, H5 mean/P05/min 8.995/8.411/7.943m. **`03_boxes.mp4` 1,000프레임 중 검정 501개**(f0 및 홀수 500)이고 나머지 짝수 프레임에서 발·박스·이동이 보이는 **캡처 artifact**. 이 영상만 완전 검정 또는 정책 낙상이라고 판정하지 않는다.

두 정책의 영상은 단일 env, seed42, 20초/1,000 frame `maneuver_push`이며 camera-off scenario7의 명령 전환·random reset·지형 타일·평가 seed와 같지 않다. box/stair 영상의 초기 진행은 정성 근거지만 **중앙 다단 stairs 완주, 20초 전 구간 boxes 통과, push recovery seconds**나 별도 stairs/boxes 성공률을 증명하지 않는다. ZIP 내부 `source_run_id=null`은 유지하고 외부 OFFICIAL checkpoint index/SHA를 사용해 원 학습 Run에 연결하며, 동명 옛 `model_4650`(`ce7ad586…`)과 이번(`a8249db4…`)을 분리한다. 실제 채점/출시는 이 보고서로 변경되지 않는다.

> 날짜별 업데이트는 해당 시점의 기록이다. 최신 Run·제출 상태는 [현재 Experiment registry](../../../research/EXPERIMENTS.md)를 우선한다.

## 2026-10-14 H1 fresh 조합 두 건 — 영상·평가·게시 완료만 확인

**후속 사용자 보고서 수신:** [원문·정확한 학습 Run ID 연결](../experiments/h1/analysis/2026-10-14_ACTRATE0001_FRESH_COMBINATION_REPORT_INTAKE.md). 두 원문 모두 HOLD이며 action+airtime 보고서는 rough 저속·정지/횡이동 잔류를, action+feet_slide 보고서는 rough 접촉 1건과 자세·행동 비용 교환을 지적한다. 이는 사용자 제공 분석의 요약이며 이번 작업의 새 GPU 실행·독립 raw 검산·matched A/B가 아니다. 기존 정책보고서의 빈 `source_run_id`는 [SHA 근거를 가진 학습 Run 연결표](../experiments/RECENT_POLICY_LINKS.md)로 보완하고 원문 metadata는 보존한다.

[action+airtime](../../../research/experiments/h1/exp-h1-action-airtime-fresh-interaction.md) / [action+feet_slide](../../../research/experiments/h1/exp-h1-action-foot-contact-stability.md)의 서로 다른 indexed `model_2950`로 생성된 Windows PERSONAL ZIP은 각각 6영상 + 별도 camera-off H1 scenario7 full 평가 COMPLETE/non-smoke, 18파일/CRC PASS다. 평가 조건은 128env × 3seed × 8case × 20초다. 공식 학습 원본 두 건은 Originals, 평가 ZIP 두 건은 Eval Release에 게시했고 실제 압축본의 원격 크기·SHA 확인도 완료했다. 동일 파일명만으로 두 정책을 합치지 않는다. **성능 분석·비교·채택은 아직 대기/HOLD**이며 이 기록은 공식 점수·추가 학습·A/B 보고서가 아니다.

## 2026-10-11 H1 model_9999 통합 ZIP·정책 보고서 — HOLD

[게시 근거](../operations/windows_h1_video_evaluation/2026-10-11_ACTRATE0001_FRESH10K_MODEL9999_PUBLICATION.md) · [model_9999 정책 검토](../experiments/h1/analysis/2026-10-11_ACTRATE0001_MODEL9999_POLICY_REVIEW.md). `model_9999_h1_6terrain_evaluation_20261011-162017_8438c90e.zip`는 18파일/CRC PASS, PERSONAL Windows H1 full scenario7(128env×3seed×8case=3,072episode), COMPLETE·최상위 smoke=false다. raw `source_run_id/preset=null` 및 nested protocol.smoke=null은 원문 그대로 보존하고, 별도 공식 train index의 checkpoint SHA로 계보를 연결한다.

ZIP SHA `ecb6df0e03bf11ec1e2259f5e0fd8b7d4b57e6e63ca09c482f31a8adcf63bfbe`. checkpoint SHA `a5020c273bc2b69bea1b20782fe80ba6605b3036b4054a7e5a8ab66151d2cb74`는 공식 fresh10K keeper model9999다. 보고서는 영상 0.5초 표본·초기/후반·연속 프레임을 확인했다고 기록했다. frame0 black과 교대 black artifact는 구분하며 후자는 보고되지 않았다. 생존 100%에도 rough 꼬리·계단 완주 공백으로 HOLD. 영상과 camera-off 평가는 별도 조건이며 공식 점수·A/B 결과가 아니다.



## Release 게시 위치 — 2026-10-12

새 Windows PC 통합 영상·평가 ZIP는 비공개 `naver-issacsim-eval` Release에 게시하며, 기존 NVIDIA 링크·애셋은 유지한다. 서버용 publisher의 NVIDIA 대상은 변경하지 않고 PC 자동 게시를 추가한 것도 아니다. 게시 절차와 tag/source 구분은 eval의 `EVALUATION_RELEASES.md`, analysis의 `docs/RELEASE_TAXONOMY.md`를 따른다.

## 2026-10-11 H1 model_4650 통합 ZIP·보고서 수납 — HOLD

> [2026-10-14 4정책 후속 비교](../experiments/h1/analysis/2026-10-14_H1_4POLICY_LINTRACK065_COMPARISON_INTAKE.md) 수신·CSV 확인 완료. 평가 COMPLETE와 정책 HOLD를 유지하며, 신규 영상/GPU 평가 또는 공식 점수 검증이 아니다. 후속 보고서의 protocol parity 주장과 이번 수납에서 직접 확인한 범위를 구분한다.

`model_4650_h1_6terrain_evaluation_20261011-030854_89b4c4a0.zip`는 **18파일/CRC PASS**, 6영상 뒤 별도 PERSONAL full scenario7 8 case×3 seed×128 env, COMPLETE/non-smoke다. 체크포인트 SHA `ce7ad58657f3dd744e7cf2b7531f3d7d455773dfc6fb135f39d8a55aa49dea70`가 OFFICIAL lin=.65/action=-.0001 resume Run index의 최신 keeper4650과 일치한다(best2900 아님). 원본·checksum·manifest 두 Release 게시와 원격 size/digest 확인 완료: [수납](../operations/windows_h1_video_evaluation/2026-10-11_ACTRATE0001_LINTRACK065_MODEL4650_PUBLICATION.md).

보고서와 raw 핵심 수치는 3,072회 20초 생존이나 H3 world XY 잔류2.398m·H4 yaw .179rad/s가 남아 **HOLD**. 영상 중앙 계단 완주는 미입증, 초기 검정 1프레임은 보고서상 capture artifact다. 이번 문서 수납에서 영상 재디코딩/GPU 실행이나 matched comparison CLI 실행은 하지 않았다. [원문](../incoming/other/reviewed/H1_MODEL4650_POLICY_ANALYSIS_20261011.md) · [판정](../experiments/h1/analysis/2026-10-11_ACTRATE0001_LINTRACK065_MODEL4650_POLICY_REVIEW.md).

## 2026-10-11 H1 ACTRATE-001 / model_2850 PERSONAL Windows 영상·평가 행동 분석 — HOLD

[2026-10-10 원문 분석](../incoming/other/reviewed/H1_MODEL2850_SHA1E6D_POLICY_ANALYSIS_20261010.md) · [2026-10-11 정책 검토](../experiments/h1/analysis/2026-10-11_ACTRATE001_MODEL2850_POLICY_REVIEW.md) · [Experiment](../../../research/experiments/h1/exp-h1-action-rate-smoothing.md). 이미 게시·보존된 2026-10-10 H1 `model_2850_h1_6terrain_evaluation_20261010-233937_1cc2ab9d.zip`(기존 확인 SHA `19068800…c07351`)의 6 MP4와 별도 camera-off `scenario7` 8 case×3 seed×128 env=**3,072** 최초 episode에 대한 사용자 제공 심층 분석을 수납했다. 정책 SHA `1e6d0950f5bd981ca1f88044e65ae7ee57505c47b92b5caad8c39263f4d93bb1`은 기존 OFFICIAL `ACTRATE-001` 학습 Run의 best 2850과 일치한다. 평가 ZIP 안의 `source_run_id=null`은 변경하지 않는다. 이 파일명은 ORIENT-100의 2850과 겹치므로 SHA로 구분한다.

**3,072/3,072 timeout 생존**·H2/H7 body 전진 **15.470/10.656m**·경사 H6 상/하 **20.297/20.058m**에도 H1 정지 비의도 world XY 평균 **1.151m**, H3 횡왕복 **2.177m**, rough H5 P05 **8.921m**, 중앙 다단 계단 정량 공백이 있다. **행동 후보 HOLD**. 영상은 1 env/seed 42의 별도 command/terrain이고 정량 camera-off episode와 동일 궤적이 아니다. 이번 보고서 수납에서 Windows GPU를 다시 구동하거나 기존 6 MP4·ZIP을 재생성하지 않았으며 실제 공식 NCRC 점수도 아니다.


이 문서는 이 PC의 Windows native Go2 실행 절차와 실제 검증 기록, 그리고 같은 공용 evaluator core를 재사용하는 H1 통합 실행 계약을 함께 정리한다. 서버용 `issacsimz`와 OFFICIAL 수동 영상은 [17](17_ISSACSIMZ_VIDEO_OPERATIONS.md), H1 상세 계약은 `naver-issacsim-eval/WINDOWS_H1_WORKFLOW.md`, 라이브러리의 현재 상태는 [00](00_START_HERE_CONTEXT_AND_MAP.md)을 따른다.

## H1 통합 실행기 — 2026-10-08 기준

`C:\NCRC\h1_6terrain_video.bat`에 native checkpoint 경로를 입력하면 H1 고정 6영상(경사 ±10°) 뒤 별도 camera-off `scenario7` 전체 평가(128 환경 × seed 4201/4202/4203 × 8 case)를 실행하고 18개 파일의 통합 ZIP을 checkpoint 옆에 만든다. 동일 checkpoint의 검증된 `-VideoResult` receipt는 영상 재사용에만 사용한다. Go2는 기존 실행기를 유지한다.

현재 Windows 실행기에서는 standalone `eval_smoke`와 `-EvaluationSmoke`를 제거했다. 기존 결과·로그와 내부 진단 데이터 형식은 보존하며, smoke/incomplete 자료는 full ZIP에 넣지 않는다. H1/Go2 CPU 회귀 테스트 60개, PowerShell 문법 및 설치 파일 일치 검증은 통과했다. **2026-10-06 설치 검증 시점에는 H1 GPU full이 미실행**이었으나, 2026-10-07 `ORIENT-100 / model_2850`의 PERSONAL 6영상 및 full `scenario7` 평가 완료 자료가 확보됐다. 그 시점에는 다른 checkpoint GPU 검증과 paired comparison이 입증되지 않았지만 **2026-10-10 후속 기존 ZIP 3개 raw 대응-index 비교는 완료**됐다(새 GPU/Windows A/B CLI 없이). 설치·문서 수정은 GPU 작업 승인이 아니다.

## 2026-10-10 H1 동일 프로토콜 기존 평가 ZIP 3개 raw 대조 완료

[원자료 직접 분석 보고서](../experiments/h1/analysis/2026-10-10_H1_SCENARIO7_RAW_3POLICY_MATCHED_ANALYSIS.md) · [case summary JSON](../experiments/h1/2026-10-10_H1_SCENARIO7_RAW_SUMMARY.json) · [cohort delta JSON](../experiments/h1/2026-10-10_H1_SCENARIO7_PAIRED_DELTAS.json). 기존 GitHub Release에 보존된 TERM-50 `model_2800`, ORIENT-100 `model_2850`, ACTRATE-0001 `model_2700` 평가 ZIP 세 개를 사용자가 업로드해 **새 GPU 실행 없이** 9,216행 `episodes.jsonl`과 evaluator resolved config 바이트 동일성, policy SHA, 전체 3,072 대응 cohort 키 및 20초 timeout을 확인했다. 결과는 기존 PERSONAL video/evaluation의 CPU 재분석이다. camera-off 평가와 MP4는 동일 경로·명령을 재현하지 않으며 공식 NCRC 점수/동일 initial terrain/훈련 인과를 뜻하지 않는다. 원본 ZIP·정책·영상·수령 영수증은 변경하지 않는다.

## 2026-10-07 H1 PERSONAL Windows 단일 정책 실전 평가

[H1 `ORIENT-100 / model_2850` 통합 분석](../incoming/other/reviewed/H1_ORIENT-100_POLICY_ANALYSIS_20261007.md)은 6개 고정 MP4(각 20초, 경사 ±10°)와 별도 camera-off `scenario7` full 원자료를 담은 기존 18파일 ZIP을 읽고 판정했다. 7 scenario, H6 상/하를 분리한 8 case × 3 평가 seed × 128 env = **3,072 episode 모두 20초 timeout / base-contact 종료 0**; child exit 0, `complete=true`, `smoke=false`; protocol ID `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34`. 이는 **H1 Windows PERSONAL full 평가 한 건의 완료 근거**이지 모든 H1 checkpoint·paired harness 검증이나 공식 NCRC 점수가 아니다.

영상은 단일 tile/고정 pose/전역 명령시계, 평가기는 10×20 tile/random reset/episode별 명령시계다. 같은 20초라도 대응 episode가 아니며 6영상의 초기 거친 지형 진행을 20초 전체 통과로 확장하지 않는다. `02_inverted_stairs.mp4`에는 검정 짝수 500프레임/가시 홀수 500프레임의 캡처 결함이 기록돼 있다(원본 보존, 정책 실패 아님). 이 후보의 **HOLD 판정**과 다음 `h1-submit-2` 대조 기준은 [가설 기록](../../../research/experiments/h1/exp-h1-rough-terrain-orientation-relaxation.md)을 따른다.

통합본은 `model_2850_ORIENT-100_h1_6terrain_evaluation_20261007-010444_f6b3b8b3.zip`(33,323,164 bytes, SHA `aecc82b1…110eb7a`)이다. 원본은 `naver-issacsim-originals/data/raw/private_server_runs/h1/2026-10-07_windows_model2850_video_evaluation/`에 보존하고 [PERSONAL 영상·평가 Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261007-exp-h1-rough-terrain-orientation-relaxation-model2850-video-eval)에 ZIP·checksum·publication manifest를 게시했다. source checkpoint SHA `6aedeced…f7b0`는 [OFFICIAL 3K 학습 접수 기록](../experiments/h1/training/2026-10-06_ORIENT100_OFFICIAL3K_EVIDENCE_INTAKE.md)의 automatic-best 2850과 일치한다. 내부 `source_run_id=null`은 그대로 두고 별도 manifest로 계보를 연결한다.

이번 실행은 6개 영상과 native full evaluator가 성공한 뒤 wrapper의 후처리에서 남은 `smoke` 변수 참조로 실패했다. 수정 후 기존 결과를 CPU에서 검증·포장해 통합 ZIP을 복구했으며 GPU 재실행은 없었다. 따라서 native child exit 0과 최종 ZIP 검증을 기록하고, 최초 BAT 전체 exit 0으로 바꾸지 않는다. 복구 receipt는 `C:\NCRC\h1-video-suite-work\suite-c64f3cec24454cf58a9f88c1224f2c34\recovery_result.json`이며 원 실패 기록도 보존한다.

## 요청 해석과 실행 경계

기본 통합 실행의 주 전달물은 **6영상과 개별 평가 원자료·진단 요약을 함께 담은 단일 통합 ZIP**이다. 기존 영상 ZIP과 평가자료는 보존한다. 기본 실행은 여전히 영상 뒤 별도 시뮬레이션 평가이며 MP4를 AI가 읽어 점수를 내는 방식이 아니다. H1은 `-EvaluationOnly`로 receipt 없이 평가만 실행할 수 있다. 특정 지형 영상 하나 또는 영상만 만드는 옵션은 현재 없다.

사용자가 “6영상 뽑고 평가 돌려줘”라고 직접 요청하면 **요청된 robot의 통합 launcher**로 지정 checkpoint의 고정 6영상과 ZIP을 만들고, 이어서 별도 camera-off `scenario7` full 평가를 수행하는 요청으로 해석한다. Go2는 9 case, H1은 8 case이며 H1 slope는 ±10°다. 이 실행은 GPU를 사용한다. 실제 실행을 분명히 요청한 경우에는 해당 checkpoint 작업을 승인한 것으로 보고 같은 승인 범위의 진단·재시도를 다시 묻지 않는다. 문서 작성·절차 문의·준비 요청은 GPU 실행 승인이 아니다. 정확한 native `.pt` 경로가 현재 맥락에 없으면 한 번 묻고 파일명을 추측하지 않는다. 승인은 지정된 checkpoint와 현재 요청 범위에만 적용된다. 사용자가 작업을 보류하거나 별도 실행 승인을 요구했다면 재개·승인 전에는 시작하지 않는다.

이 Windows 절차는 PERSONAL 환경의 정성 영상과 내부 수치 진단이다. 대회 OFFICIAL score가 아니며 학습을 재개하거나 optimizer를 복원하지 않는다. 영상·평가는 원 학습 Run의 후속 기록으로 연결한다. 생성 완료만으로 채택 판정을 바꾸지 않으며, 이후 근거를 검토한 분석의 HOLD/PROMOTE/REJECT는 registry에 기록한다. 사용자가 담당하는 A/B 비교 보고서를 자동 작성하지 않는다.

## Windows 통합·비교 실행 파일

각 BAT는 같은 디렉터리의 동명 PS1에 인자를 전달한다. 대화형 실행의 기본 진입점은 BAT다.

| 파일 | 역할과 기본 동작 |
|---|---|
| `C:\NCRC\go2_6terrain_video.bat` | 고정 6영상 도구의 대화형 진입점. `-Path`가 없으면 checkpoint 경로를 한 번 묻는다. 기본 설정은 6개 영상·ZIP 검증 후 별도 전체 평가까지 이어진다. `GO2_VIDEO_NO_PAUSE=1`이면 종료 대기를 생략한다. |
| `C:\NCRC\go2_6terrain_video.ps1` | Go2 통합 실행 로직. `C:\NCRC\go2-video-evaluator`의 manifest로 evaluator 파일 SHA256을 확인하고 ASCII 작업 경로에서 실행한다. 일치하는 `-VideoResult` receipt가 있으면 영상을 재생성하지 않고 평가만 할 수 있다. |
| `C:\NCRC\h1_6terrain_video.bat` | H1 통합 실행의 대화형 진입점. native checkpoint를 받아 ±10° 고정 6영상 뒤 `scenario7` 8 case full 평가와 18개 항목 통합 ZIP까지 수행한다. |
| `C:\NCRC\h1_6terrain_video.ps1` | H1 통합 실행 로직. `C:\NCRC\h1-video-evaluator`의 공용 bundle을 검증하고 원본 checkpoint를 ASCII work path에 staging한다. 동일 checkpoint의 `-VideoResult`는 영상 재사용에만 쓴다. |
| `C:\NCRC\compare_policies.bat` | PERSONAL 두 정책 비교기의 BAT 진입점. 사용자가 비교를 명시적으로 맡긴 경우에만 쓴다. |
| `C:\NCRC\compare_policies.ps1` | PERSONAL 비교기. 두 완료 평가자료 폴더를 읽어 CPU에서 비교하거나, `.pt` 입력을 받아 새 평가를 실행한 뒤 비교한다. `.pt` 경로는 GPU 실행을 일으킬 수 있다. |

### PowerShell 인자와 기본값

| 실행기 | 인자 | 기본값·의미 |
|---|---|---|
| `go2_6terrain_video.ps1` | `-Path`, `-ExpectedSHA256` | 원본 native checkpoint 경로와 선택적 기대 SHA256. `-Path` 생략 시 대화형 입력을 받는다. |
| | `-Scenario` | 허용값은 `maneuver_push` 하나뿐이며 기본값도 `maneuver_push`다. |
| | `-VideoResult` | 기존 suite의 `result.json` receipt. source checkpoint 경로·SHA, 6개 영상 및 ZIP이 일치해야 재사용한다. |
| | `-EvaluationNumEnvs`, `-EvaluationSeeds` | 기본 `128`, `4201,4202,4203`; 환경 수 허용 범위는 1–4096이다. 전체 평가에 적용한다. |
| | `-CompareWith` | 저장 평가자료 디렉터리를 추가로 비교한다. 전체 평가 모드에서만 유효하다. 사용자 담당 비교가 별도 요청되지 않으면 생략한다. |
| `compare_policies.ps1` | 위치 인자 `A`, `B` | 각각 후보 A와 기준 B의 `.pt` 또는 완료 평가자료 디렉터리. 누락 시 묻는다. 두 입력이 모두 저장 디렉터리면 CPU 비교 경로다. |
| | `-Robot`, `-NumEnvs`, `-Seeds`, `-Suite` | 기본 `go2`, `128`, `4201,4202,4203`, `scenario7`. `Robot`은 `go2`/`h1`, `Suite`는 `scenario7`/`terrain6`; 환경 수는 1–4096이다. |
| | `-PolicyA`, `-PolicyB` | 해당 입력이 native checkpoint 대신 TorchScript `policy.pt`임을 표시한다. |
| | `-Preview` | 명령만 표시하고 프로세스와 출력 폴더를 만들지 않는다. |
| | `-Calibration`, `-Output`, `-EvalRoot`, `-LabRoot`, `-TaskRoot` | 비교 calibration·결과 경로·evaluator·IsaacLab·task 경로를 지정한다. 기본 `LabRoot`는 `C:\NCRC\IsaacLab`; `TaskRoot`는 Go2면 `C:\NCRC\naver-issacsim-nvidia\training\quadruped`, H1이면 `...\training\humanoid`다. 저장자료 CPU 비교에 patched driver를 명시하려면 `-EvalRoot C:\NCRC\go2-video-evaluator`를 준다. |


통합 실행기의 일반적인 명령은 다음과 같다. 둘 다 실제 GPU 실행을 시작하므로 위 승인 경계를 따른다.

```powershell
# Go2
& C:\NCRC\go2_6terrain_video.bat -Path '<native-checkpoint.pt>'

# H1
& C:\NCRC\h1_6terrain_video.bat -Path '<native-checkpoint.pt>'
```

기존 receipt를 재사용하는 전체 평가 명령은 `-VideoResult`를 지정한다. 영상과 평가를 모두 새로 수행하려면 receipt 없이 실행한다. 현재 Windows 실행기는 full 전용이다.

**H1 평가만 요청할 때(2026-10-18 추가):** `C:\NCRC\h1_6terrain_video.bat -Path "C:\path\model_N.pt" -EvaluationOnly`. 영상·receipt 없이 기존 camera-off full scenario7(128 env × 3 seeds × 8 case × 20초)을 실행하고 checkpoint 옆 새 `*_h1_evaluation_<timestamp>_<id>` 폴더에 평가 원자료 7개를 저장한다. MP4·통합 ZIP은 없고 `video_evaluation_link.json`의 video ZIP 두 필드는 null이다. `-VideoResult`와 병용하지 않는다. 옵션 생략 시 기본 6영상+평가 흐름은 동일하다. CPU 회귀·구문 검사만 수행했으며 이 새 경로의 GPU 실행은 미검증이다. 영상 생성을 추가로 요구하거나 권한을 다시 묻지 않는다.

## Go2 고정 영상 계약과 H1 차이

각 checkpoint에서 아래 여섯 지형을 같은 조건으로 한 번씩 촬영한다.

| ZIP 내 MP4 | 지형 | `sub_terrains` key |
|---|---|---|
| `01_stairs.mp4` | stairs | `pyramid_stairs` |
| `02_inverted_stairs.mp4` | inverted stairs | `pyramid_stairs_inv` |
| `03_boxes.mp4` | boxes | `boxes` |
| `04_random_rough.mp4` | random rough | `random_rough` |
| `05_slope_up_20deg.mp4` | 20도 오르막 | `hf_pyramid_slope` |
| `06_slope_down_20deg.mp4` | 20도 내리막 | `hf_pyramid_slope_inv` |

task는 `Quadruped-v0`이고 native play 조건은 `--num_envs 1 --headless --video --video_length 1000 --enable_cameras --seed 42`다. `env.scene.terrain.terrain_generator` 아래 rows/cols 1·horizontal scale 0.05와 선택 key의 `proportion=1.0`, 다른 다섯 key의 `proportion=0.0`을 지정한다. 두 slope의 해당 `slope_range`는 `[0.363970234,0.363970234]`다. pinned IsaacLab 공식 `play.py`를 task 등록용 ASCII runner로 호출하며 tracked task source나 기존 `exported/model_best.pt`는 교체하지 않는다.

H1은 `Humanoid-v0`와 같은 여섯 terrain key를 사용하되 slope 값은 `[0.176326981,0.176326981]`(10°)이고 파일명은 `05_slope_up_10deg.mp4`, `06_slope_down_10deg.mp4`다. 아래 20° 값과 Go2 task명을 H1 명령에 그대로 적용하지 않는다.

모든 영상은 20초, 50Hz 제어 1,000 step, 환경 1개, seed 42, headless camera capture다. 지형은 한 번에 하나만 켜며 `num_rows=num_cols=1`, `horizontal_scale=0.05`; slope는 `0.363970234`(20도)로 고정한다. `maneuver_push`의 몸체 기준 명령은 전진 0–6초 `(vx,vy,yaw)=(1.0,0,0)`, 양의 횡이동 6–10초 `(0.5,+0.3,0)`, 음의 횡이동 10–14초 `(0.5,-0.3,0)`, 회전 14–17초 `(0.5,0,+0.5)`, 반대 회전 17–20초 `(0.5,0,-0.5)`다. 속도 단위는 m/s, yaw rate는 rad/s다. 4·8·12·16초에는 world Y 방향 순간 속도 변화 `+0.5,-0.5,+0.5,-0.5 m/s`를 준다. 이는 로컬 정성 시험이며 공식 G6 조건을 재현한다고 주장하지 않는다.

평가 전의 video-only ZIP은 정확히 10개 항목이다. 6개 MP4 외에 `SHA256SUMS.txt`(각 영상 hash), `source_checkpoint.txt`(원본 경로와 SHA256), `environment.txt`(실행 환경·코드 식별자·시나리오 조건), `README.txt`(해석 범위)를 담는다. `result.json`은 ZIP 안이 아니라 작업 receipt다. ZIP 안의 `video_suite_manifest.json`을 전제로 하지 않는다. receipt와 ZIP의 SHA, ZIP CRC·정확한 이름·항목 수, 각 MP4 frame·길이, 입력 checkpoint와 staged copy SHA를 검증한다. full 후 최종 통합 ZIP의 18개 항목은 아래 별도 계약을 따른다.

Kit stdout/stderr는 사용자 콘솔에 실시간으로 표시하고 로그에도 보존한다. 각 terrain에서 native exit 0, 이번 실행 이후 생성된 nonempty MP4와 1,000 frame을 확인한 뒤 다음 terrain으로 진행한다. 치명 오류가 나면 진행을 중단하고 로그를 진단한다. 2026-10-07 변경 이후 중간 영상 ZIP은 `C:\NCRC\<robot>-video-suite-logs\suite-<id>\video_source.zip`에 보존한다(`robot`은 `go2` 또는 `h1`). 원본 `.pt` 옆에는 full 성공 후의 통합 ZIP 하나만 만든다. 기존 Downloads 영상 ZIP과 receipt는 역사적 입력으로 계속 재사용할 수 있다. 완전 성공한 이번 작업의 ASCII 임시 폴더만 정리할 수 있고 실패 작업은 경로를 출력하고 남긴다.

## 최종 통합 ZIP과 Git 소스

full 성공 후 `<checkpoint-stem>_<robot>_6terrain_evaluation_<timestamp>_<id>.zip`을 원본 `.pt` 옆에 새로 만든다. root의 video-only ZIP 항목 10개, `evaluation/`의 `episodes.jsonl`, `evaluation_manifest.json`, `resolved_configs.json`, `video_evaluation_link.json`, `diagnostics.json`, `evaluation.log`, `README.txt` 7개, root의 `BUNDLE_README.txt`를 합친 정확히 18개 파일이다. 각 항목이 nonempty인지, CRC·영상/평가 SHA와 동일 checkpoint/protocol인지를 검증한다. 콘솔의 최종 ZIP 안내는 이 통합본이며 receipt의 `combined_archive`에 path·SHA·size·entry count를 남긴다. `zip_path`는 내부 영상 ZIP 또는 과거 receipt의 영상 ZIP을 가리켜 재사용 계약을 유지한다. smoke/incomplete 평가는 통합 full ZIP 생성에서 거부한다. A/B 보고서·calibration은 담지 않는다.

원본 full 평가 폴더가 보관용 ZIP으로 바뀐 기존 2950·7050 자료는 ZIP 안의 7개 파일을 원 receipt hash와 대조한 뒤 새 통합 ZIP을 만들었다. GPU나 비교 분석은 다시 실행하지 않았다. [통합본 검증 기록](../operations/windows_go2_video_evaluation/combined_archives_verified.json)에 두 파일의 출처·SHA와 18개 항목 검증 결과를 보존한다.

| checkpoint | 실제 통합 ZIP 파일명 | SHA256 |
|---|---|---|
| 2950 | `model_2950_go2_6terrain_evaluation_20261004-030709_471ae945.zip` | `d1a38155dc0bcf057d07ed5cf2ed41dd1dc9a26da1ea2578a1a690961692d612` |
| 7050 | `model_7050_go2_6terrain_evaluation_20261004-030710_e8bd9e18.zip` | `34d45711d121a4bb59a92b6424f2652eeb915ed4f6436d49070389eacc33d1e1` |

두 파일은 원본 checkpoint와 같은 Downloads 폴더에 있다. 기존 개별 평가자료의 현재 보관 위치는 아래 당시 폴더 경로에 `.zip`을 붙인 archive다. 과거 폴더·receipt 경로는 원 실행 provenance로 유지하며 지금 폴더가 존재한다고 주장하지 않는다.

역사적 최초 동기화는 `naver-issacsim-eval` commit `45368dacbbbd1a365d32b2a05fd58c093e5441a3`이다. 이후 H1 inactive event 처리 `0915b9a`, full 평가 후처리 `d7c1c1a`, 중간 ZIP 내부 보존 `ac1956b`가 반영됐고 2026-10-08 확인한 main은 `5153b98`이다. 후처리·ZIP 변경까지 CPU 회귀 63개가 통과했으며 새 GPU 재실행으로 검증한 것은 아니다. 그 저장소의 `AGENTS.md`·`WINDOWS_WORKFLOW.md`를 읽고 `install_windows.ps1 -Preview`로 copy/hash/구문만 확인하거나 명시적인 설치 요청에서 `-Destination C:\NCRC`로 복원한다. 설치는 GPU를 실행하지 않고 differing 파일을 먼저 백업한다. `.gitattributes`로 hash 대상 파일의 BOM·CRLF를 보존하므로 clone의 개행 변환으로 bundle identity를 바꾸지 않는다.

역사적 통합 ZIP 도입 때의 설치 PS1 SHA는 `76a68fec34d4be74c4438e8bd9f7b87f41b0ae83d76354239c8081a844ef9402`다. 아래 최초 full 시점의 `dbd9...` SHA 및 [당시 inventory](../operations/windows_go2_video_evaluation/installed_tools_manifest.json)도 역사 snapshot이며 현재 launcher를 검증하는 고정값으로 재사용하지 않는다. 당시 source의 CPU tests는 52/52 PASS, installer Preview·fixture 백업/동일 파일 재설치 및 실제 launcher 백업 갱신을 확인했다. GPU 재실행이나 actual A/B score/calibration은 그 source 동기화에서 수행하지 않았다.

[현재 동기화 검증 기록](../operations/windows_go2_video_evaluation/windows_sync_verified.json)에 설치 SHA·이전 launcher 백업·CPU 및 설치 검증을 기록했다. commit에서 export한 파일의 bundle/launcher bytes도 실제 설치본과 같았다. 네이버 평가기 저장소와 `C:\NCRC\naver-issacsim-eval` checkout은 위 commit으로 동기화했지만 standalone 경로의 실제 GPU PASS는 추가로 주장하지 않는다.

## 별도 Go2 `scenario7` 평가

전체 평가는 영상 촬영과 별도인 camera-off deterministic inference다. 기본값은 128 환경, seed `4201,4202,4203`, 20초 time window다. 7 scenario에는 총 9 case가 있다.

| Scenario | case 구성 |
|---|---|
| `G1 forward_tracking` | flat 전진 명령 1 case |
| `G2 omnidirectional_tracking` | flat 전진·좌우·회전 명령 1 case |
| `G3 rough_terrain` | random rough 1 case |
| `G4 slope` | slope up·down 2 cases |
| `G5 stairs` | stairs up·down, step height 0.125 m, 2 cases |
| `G6 push_recovery` | flat push recovery 1 case |
| `G7 domain_randomization` | random rough, friction 0.6–1.2와 added mass −1.0–1.0, 1 case |

몸체 기준 `(vx,vy,yaw rate)` 명령은 G1의 첫 10초 `[1,0,0]`·다음 10초 `[1.5,0,0]`, G2의 `[0.6,0.3,0.5]`·`[0.6,-0.3,-0.5]`다. G3–G7의 각 case는 `[1,0,0]`을 유지한다. 명령 시간표는 **episode step clock**을 따르므로 reset 뒤 첫 명령부터 다시 시작한다. 영상의 시간표는 reset 뒤에도 **전역 video step**을 따르며 평가와 다르다. G6는 전역 4·8·12·16초에 world XY 속도 delta `(+0.5,0),(-0.5,0),(0,+0.5),(0,-0.5)` m/s를 순서대로 주고, G7의 added mass 단위는 kg다. 이 값과 시나리오 weight는 설치 `eval_core.py::load_suite()`의 내부 규약이며 미공개 공식 값을 재현한 것으로 해석하지 않는다.

따라서 전체 정책당 `128 × 3 × 9 = 3,456` cohort 조합이다. time window 안에서 낙상 후 reset이 생길 수 있어 저장 episode 수는 cohort 수와 다를 수 있다. 완전 자료에는 `episodes.jsonl`, `evaluation_manifest.json`, `resolved_configs.json`, `video_evaluation_link.json`, `diagnostics.json`, `evaluation.log`, `README.txt`가 있다. episode 원자료에는 scenario/case/seed/env/episode ID, steps·duration, end reason·survival, policy SHA·protocol ID와 `mean_tracking_error`, `vx_error`, `vy_error`, `yaw_error`, `xy_rmse`, `yaw_rmse`, `forward_progress_m`, `world_dx_m`, `world_dy_m`, `lateral_drift_m`, `stall_fraction`, `roll_pitch_rms`, `action_delta_rms`, `base_contact_failure` 같은 진단값을 보존한다. `diagnostics.json`은 scenario별 episode 수·실패 수·survival rate·평균 tracking error를 요약한다. 이 값은 내부 진단이다. 공식 점수·공식 평가 구현과 동일하다고 말하지 않는다.

**역사적 기록(현재 실행 옵션 아님):** 2026-10-03 KST 통합 smoke는 기존 receipt를 재사용해 첫 scenario/case·seed 4201·128 환경·2초를 실행했고 exit 0이었다. `smoke=true`, `complete=false` 자료와 실패 traceback은 보존한다. 이 옵션은 2026-10-06 제거했으며 전체 평가/점수로 해석하지 않는다.

## 보존·ASCII 경로·설치 환경

native Isaac 실행에는 ASCII 경로의 checkpoint copy, runner, evaluator, output을 전달한다. 원본 `.pt`는 수정하지 않고 source SHA를 기록한 뒤 copy SHA를 다시 확인한다. Windows checkpoint나 다운로드 경로에 한글이 있어도 native child에 그 경로를 직접 넘기지 않는 것이 통합 PS1 경로다. 영상·평가를 순차 실행하고 `C:\ov\warp-cache`를 `WARP_CACHE_PATH`로 둔다. 평가 로그와 suite 작업 디렉터리는 `C:\NCRC\go2-video-suite-logs\suite-<guid>` 및 `C:\NCRC\go2-video-suite-work\suite-<guid>`에 기록한다. 실패·중단 시 ZIP, 로그, traceback, 작업 자료를 보존하고 stale 산출물을 새 성공으로 착각하지 않는다.

통합 PS1은 `C:\NCRC\go2-video-evaluator\bundle_manifest.json`을 사용해 `isaac_runner.py`, `eval_core.py`, `compare_cli.py`의 SHA를 확인한다. bundle hash는 각각 `c5e157e488f99c84bfae7d719a8d59a7235e509f1f7e8ef6f1e052d2bdf5fe32`, `4c201c58bfbc267f34e0615407021dabb8e799ea476e01f00602fce9af58b14a`, `cc2cc801ef49c7eae74181332fb170d1bc71d471798ea86459afa90bd43576cb`다. 구현 기반은 `9c774a322f2f7d4944444de57f01308987bcb3da`, handoff 문서는 `28895d75edf3095607e392a07207a62e768478c7`이다. 첫 GPU smoke에서 CUDA 미초기화 상태의 `torch.cuda.reset_peak_memory_stats(device_index)`가 `Invalid device argument`로 실패한 뒤, 설치 bundle에서 reset 전에 `torch.cuda.init()`을 호출하도록 고쳤고 오류·중단 traceback 보존도 추가했다. 당시 수정은 설치 copy에 한정했고 원 evaluator checkout을 바꾸지 않았다. 이후 위 Git 동기화에서 검증된 수정본을 평가기 source에 반영했다. IsaacLab/task source, CUDA driver와 패키지는 수정·업그레이드하지 않았다.

통합 PS1의 preflight는 다음 버전을 기대한다. 영상 ZIP의 `environment.txt`에는 실제 버전, GPU, Git HEAD와 실행 파일 hash도 기록된다.

| 항목 | 검증 환경 |
|---|---|
| Python | `3.11.13` |
| PyTorch | `2.7.0+cu128` |
| TensorDict | `0.9.0` |
| `rsl-rl-lib` | `5.0.1` |
| IsaacLab | `3e73d6dd79080fd7632488c061052a6edd52e230` |
| Isaac Sim | `C:\isaacsim`, `5.1.0-rc.19+release.26219.9c81211b.gl` |
| `OMNI_CONFIG_PATH` / `ISAACLAB_PATH` | `C:\ov-config` / `C:\NCRC\IsaacLab` |
| `WARP_CACHE_PATH` | `C:\ov\warp-cache` |
| 기록된 CUDA / GPU | CUDA `12.8`, `NVIDIA GeForce RTX 3060 Laptop GPU` |
| Go2 task source HEAD | `ef10b7a4c9a83481346d446e8a75aed655f72214` |

기존 영상 ZIP의 `suite_driver_sha256`는 `1b6974fd0d054f7f68b29228a07ac22274eb60c1d218be037de660edce998314`, 그 ZIP을 만들 때 기록된 video-only launcher SHA는 `24b380809939fa49799b9a066f14ac3c7d3f73d7758df0d04741969e7cd0b50e`다. 최초 full 평가 시점의 통합 PS1 SHA는 `dbd9eb063cedfefc48ba9e41f4a0b985b79b46622291e66c74269f63745b5bcd`였고 그 뒤 통합 ZIP 도입 당시 설치본은 위 `76a68...`이다. 각 launcher hash는 서로 다른 시점의 파일이므로 현재 버전의 고정값으로 재사용하지 않는다. 두 영상 ZIP은 평가 시점에 다시 만들지 않고 검증된 기존 receipt로 재사용했다.

### 과거 standalone smoke 기록(현재 실행 안내 아님)

과거 standalone smoke는 ASCII staging과 patched bundle 기본 경로를 보장하지 않았고 GPU 통과 근거가 없었다. 현재 실행기에서 제거했으며 이 경로를 안내하지 않는다.

### 과거 CPU 문법 및 Preview 점검(설치 당시 기록)

전달된 설치본 정적 점검 기록에서는 `go2_6terrain_video.ps1`, `compare_policies.ps1`, `go2_eval_smoke.ps1` 세 파일 모두 syntax error 0이었다. Preview는 인자와 실행 경로를 구성할 뿐 child process나 결과 디렉터리를 만들지 않는다.

| 점검 | Preview 계획과 관찰된 결과 | 검증 경계 |
|---|---|---|
| standalone smoke | `go2_eval_smoke.ps1 -Path <원본 model_2950.pt> -EvalRoot C:\NCRC\go2-video-evaluator -Preview`는 exit 0. 원본 checkpoint 및 checkpoint 옆 smoke output 경로를 native 실행 인자로 직접 전달하는 계획이 표시됐고, child와 output directory는 없었다. | patched bundle을 지정해도 Korean 경로가 native child에 전달되는 계획은 바뀌지 않는다. Preview는 그 경로의 실제 GPU 동작을 입증하지 않는다. |
| 저장자료 비교 | `compare_policies.ps1 -A <완료된 7050 평가 폴더> -B <완료된 2950 평가 폴더> -EvalRoot C:\NCRC\go2-video-evaluator -Preview`는 exit 0. `py.exe -3`를 이용하는 CPU saved-folder 비교 계획을 표시했고, child와 output directory는 없었다. | 비교 driver가 선택된 것을 확인했을 뿐 실제 자료 비교, 점수, calibration, HTML 결과를 만들지 않았다. |

이 점검에서는 실제 score나 calibration을 계산하지 않았고 추가 GPU 실행도 하지 않았다. Preview는 launcher 인자·경로 선택만 확인한다. 위 세 PS1의 문법 점검과도 구분하며, GPU에서의 정상 실행 근거는 앞 절의 기존 smoke/full-evaluation 기록만 사용한다.

## 2950·7050 개별 전체 평가 기록

아래 hash는 verified JSON, 실행 receipt, 기존 영상 ZIP metadata에서 가져왔다. 두 checkpoint file SHA는 원본 분석 자료의 선택 checkpoint SHA와 완전히 일치한다. 다만 여기 기록된 Windows 평가는 PERSONAL 환경 평가이며 OFFICIAL 점수나 학습 작업 자체의 재검증이 아니다.

| 항목 | 2950 | 7050 |
|---|---|---|
| checkpoint | `C:/Users/[USER]\Downloads\model_2950.pt`<br>`6b72c530e571f7e9fc826c3917bd6199a22c9b1a2a1028ca7bf981231485992a` | `C:/Users/[USER]\Downloads\model_7050.pt`<br>`d40f2666da6063c16c88353163115dcac1a2bd8b98011bf745543737a2188015` |
| 영상 ZIP | `C:/Users/[USER]\Downloads\model_2950_go2_6terrain_20261003-154646.zip`<br>SHA `65e2c5db8571718df25f42f770cd035044a48374604a605fb3b644f8d13a3b82` | `C:/Users/[USER]\Downloads\model_7050_go2_6terrain_20261003-160918.zip`<br>SHA `d770d763244af220d8691025876084fb340ae9e1c436aaa2a45cd5200934c1f4` |
| 재사용 `-VideoResult` receipt | `C:\NCRC\go2-video-suite-logs\suite-a5bd048e4718436abe44b62f7218c13b\result.json` | `C:\NCRC\go2-video-suite-logs\suite-51ccbd63360f4766bbaf229dadcfb2a4\result.json` |
| Full suite receipt | `C:\NCRC\go2-video-suite-logs\suite-f108c21571674b0d9c924161348c51cf\result.json` | `C:\NCRC\go2-video-suite-logs\suite-d7ccdc3f00d7484891a02e8b4f116e78\result.json` |
| 평가자료 폴더 | `C:/Users/[USER]\Downloads\model_2950_go2_evaluation_20261004-001124_8f0b655c` | `C:/Users/[USER]\Downloads\model_7050_go2_evaluation_20261004-004816_9981f1f5` |
| 결과 수치 | 3,456 cohorts, 3,488 episodes, `1,721.047`초 | 3,456 cohorts, 3,458 episodes, `1,749.031`초 |
| `episodes.jsonl` SHA256 | `360685e9f823e939e57fba1f9cbcf720061d76e8a814e195ca75a6c9e805bb05` | `49a622b8d0d9458b3767c278d80d38e4b624cc1fff593d7cf8f68b0448c5a89e` |
| `evaluation_manifest.json` SHA256 | `debe3fc5f8e9cc28bad32e628f11143b96f1e3cbcbd707e334a9c56334b1b782` | `6efa544854e290f1d9f35d975c3cbecc94d76da84d41ca1e88540fae68633027` |

두 자료 모두 native evaluator와 BAT가 exit 0, `complete=true`, `smoke=false`였고 protocol ID는 `806d7e8280d8fac8bbbb6015013b1752335fe0446c8e39bf8f9dd4fbf7c145ad`로 같다. [2950 개별 검증 JSON](../operations/windows_go2_video_evaluation/evaluation_2950_verified.json)과 [7050 개별 검증 JSON](../operations/windows_go2_video_evaluation/evaluation_7050_verified.json)은 실제 로컬 검증 기록의 byte-for-byte 복사본이다. [설치 파일 inventory](../operations/windows_go2_video_evaluation/installed_tools_manifest.json)에 6개 BAT/PS1의 SHA256·크기·patched bundle과 문서 작업의 CPU 점검 범위를 보존했다. 원본 checkpoint·영상·full dataset·실패 작업은 위 로컬 경로에 그대로 남으며, 이 JSON들은 가공 검증 snapshot이다. 두 평가용 `video_evaluation_link.json`은 collector SHA `c5e157e488f99c84bfae7d719a8d59a7235e509f1f7e8ef6f1e052d2bdf5fe32`, scorer SHA `4c201c58bfbc267f34e0615407021dabb8e799ea476e01f00602fce9af58b14a`와 protocol ID를 기록한다.

실행 기록의 Windows 시각은 Asia/Seoul(+09:00)이다. 2950 전체 평가는 2026-10-03 23:42경 시작해 2026-10-04 00:11경 끝났고, 7050은 2026-10-04 00:18경부터 00:48경까지 실행됐다. JSON의 `verified_at`은 UTC이며 2026-10-03 날짜로 저장되어 있다. 이들은 이미 존재한 여섯 영상 ZIP을 재사용한 **개별 평가**이며 두 checkpoint를 한 번에 A/B 비교한 실행도, 통합된 새 6영상 재렌더 실행도 아니다.

## checkpoint identity와 판정 범위

### 2026-10-08 로컬·공식 불일치에 따른 판정 방향

[R3/R5 후속 논의](../experiments/go2/analysis/2026-10-08_GO2_LOCAL_OFFICIAL_EVALUATION_GAP_AND_ANALYSIS_POLICY.md)와 [운영진 DM 답변](../experiments/go2/analysis/2026-10-08_GO2_R3_R5_OFFICIAL_SCORE_COMPONENTS_ORGANIZER_REPLY.md): 공식 계단 survival **99.0%→99.8%**의 약 **+0.07점** 이득보다 Tracking Score **0.819→0.796**의 약 **−0.24점** 손실이 컸다는 구성 분해는 제공된 답변으로 확인됐다. 전방위는 survival 100%로 같고 tracking **0.834→0.829**로 약 **−0.06점**이다. 학습 contact는 공식 survival과 다른 척도이며 로컬 tracking error도 공식 Tracking Score와 동일하지 않다. **로컬·공식 tracking 역전 메커니즘·reward 인과는 미확인**이고 로컬 합산 점수 값·산식·calibration도 이 대화에서 새로 검증하지 않았다.

평가기 전면 재작성보다 **합산 점수만으로 채택하지 않는 판정**을 우선한다. 다음 질문은 **계단 생존 이득을 유지하면서 명령 추종 손실을 회복할 수 있는가**다. 저장된 R3 original 4800과 R5 terminal 7450의 실제 명령 대비 x/y/yaw-rate 오차, 상행·하행, 진행/통과·stall·종료/접촉·자세와 seed별 손해를 우선 대조한다. 운영진의 공식 `play.py` 계단 비교 권고는 영상 속도만으로 tracking을 판정하라는 뜻이 아니다. 7050을 R5 제출 정책으로 대신 쓰거나 미측정 지표를 추정해 채우지 않는다. 한 쌍에 맞춘 가중치 보정과 reward 원인 단정은 보류한다. 이 논의는 새 GPU 실행·scorer 수정·자동 비교 실행 승인이 아니다.

[2026-09-30 Go2 분석](../incoming/other/reviewed/GO2_20260929-154342-go2-lintrack-125-fresh7500-official_VS_20260928-230114-go2-lintrack125-fresh3k-r5-official_DEEP_ANALYSIS_20260930.md)의 7.1 checkpoint 표에서 2950 전체 SHA는 `6b72c530e571f7e9fc826c3917bd6199a22c9b1a2a1028ca7bf981231485992a`, 7050은 `d40f2666da6063c16c88353163115dcac1a2bd8b98011bf745543737a2188015`다. 해당 분석의 hash 대조는 각각 3K terminal checkpoint와 fresh 7.5K candidate로 연결하는 근거다. 이는 그 원 archive들을 이번 Windows 평가에서 다시 열어 검증했다는 뜻이 아니다. 모델 이름만으로 reward/Experiment/Run lineage를 새로 추정하지 않는다.

두 checkpoint의 개별 평가 receipt에는 A/B comparison path가 없고 자동 CPU 비교·공통 calibration·비교 점수는 생성하지 않았다. 이후 제공된 아래 심층 보고서의 **raw 진단 비교**와 이 실행기 산출물 부재를 구분한다. `compare_policies.bat`는 별도 명시 요청 때만 실행한다. 완료 자료 폴더끼리는 CPU 비교지만 `.pt`는 새 GPU 평가를 시작할 수 있고 통합 runner의 ASCII staging을 제공한다고 가정하지 않는다. provisional calibration은 B 변경에 따라 달라지므로 공식 score나 전역 순위로 쓰지 않는다.

개별 자료 생성·무결성 성공만으로 정책 우위를 선언하지 않는다. 두 Windows 평가는 새 training Run이 아니다. 아래 후속 분석은 생성 성공이 아니라 실제 raw 행동 측정을 근거로 후보 판단을 갱신한다.

## 2026-10-04 후속 raw 행동 분석

[받은 심층 보고서 원문](../incoming/other/reviewed/GO2_20260929-154342-go2-lintrack-125-fresh7500-official_VS_20260928-230114-go2-lintrack125-fresh3k-r5-official_DEEP_ANALYSIS_20261004.md)을 변경 없이 보존했다. 동일 protocol ID의 2950·7050 원자료를 비교한 결과, 7050은 일곱 scenario의 tracking error가 모두 낮았다. G5 계단 aggregate error `0.60996→0.17085`, survival `96.0%→99.740%`; 상승 progress `9.23→18.67 m`, stall `34.51%→1.18%`; 하강 progress `7.20→18.89 m`, stall `53.44%→2.52%`다. **model_7050 행동 후보는 PERSONAL 진단 범위에서 PROMOTE**, `LINTRACK-125` reward 자체의 효과는 same-length BASE control 부재로 **HOLD**다.

해석 한계: reset 때문에 episode 분모가 달라 episode-level paired 비교나 독립 표본 유의성 주장이 아니다. Windows task source는 OFFICIAL training source와 byte-identical하지 않으며 공식 점수·환경 재현·제출 우위를 증명하지 않는다. G2 roll/pitch와 일부 action delta는 증가하므로 모든 지표가 개선되거나 더 부드럽다고 쓰지 않는다. 원문 정정: `official_score=false`·`raw_diagnostics_only=true`는 `evaluation/diagnostics.json`의 필드이고 `evaluation_manifest.json`에는 없다. manifest는 PERSONAL·완료 상태를 기록한다. 원문은 보존하고 이 파생 지침에서 필드 위치를 바로잡는다.

2950 `03_boxes.mp4`는 보고서의 20개 샘플 frame에서 RGB mean/std가 모두 0인 검은 캡처였다. decode·frame 수·checksum PASS만으로 시각적 evidence의 유효성을 보장하지 않는다. 정책 실패가 아니고 scenario7에 boxes case도 없어 해당 시각 비교는 미확인이다. 원본 ZIP은 수정하지 않는다.

## 2026-10-05 C4800 · C7050 · C7450 3정책 후속 비교

[수신한 심층 비교 원문](../incoming/other/reviewed/GO2_C4800_C7050_C7450_POLICY_COMPARISON_20261005.md)을 변경 없이 보존했다(SHA-256 `57d3edf266ed77e1fa294270643cec15dbdadb8e87486e98295e2429a9965474`). 보고서가 직접 확인한 세 ZIP은 모두 PERSONAL camera-off `scenario7/internal-suite-v1`, 128 env, seeds 4201/4202/4203, 9 cases, initial cohort 3,456이고 세 `resolved_configs.json`과 protocol/evaluator fingerprints가 맞아 정량 A/B/C 비교가 가능하다. 영상은 정책별 6개, 총 18개이며 seed 42·20초 고정 maneuver/push 조건이다. 다만 평가와 영상은 별도 실행이고 C7050 video launcher/driver bytes는 다른 두 정책과 같지 않다.

**현재 행동 판정은 C7450 PROMOTE / C7050 HOLD / C4800 REJECT(all-around 후보 기준)**다. C7450은 C7050 대비 9개 case 중 8개에서 평균 tracking error가 낮고 8개에서 body-forward 진행이 크며, stairs-down tracking `0.174→0.141`, progress `18.89→19.76 m`, stall `2.52%→0.60%`로 개선했다. 반면 stair-up 20초 cohort base-contact 종료는 C7050 `2/384`에서 C7450 `4/384`로 늘었고 모두 seed 4201에 집중됐으며, `action_delta_rms`와 `roll_pitch_rms`도 커졌다. 따라서 7450은 더 잘 가지만 더 거칠고 특정 stair-up 초기조건에서 드물게 더 실패하는 정책이며, 7050은 안전성 fallback으로 보존한다.

C4800은 비계단 tracking 일부가 가장 좋지만 stairs-up/down에서 총 15개 cohort가 base-contact 종료되고 progress/stall/tail이 크게 악화해 현재 all-around 후보로는 REJECT다. 이 판정은 정책 행동 evidence에 한정된다. 세 manifest의 `preset`·`source_run_id`는 `null`이고 원 checkpoint bytes가 ZIP에 없으므로 이 보고서만으로 training Run, fresh/resume, reward 인과를 추정하지 않는다. 특히 7050과 7450은 registry에서 같은 OFFICIAL 7.5K Run의 서로 다른 checkpoint로 추적하지만 이 PERSONAL 비교를 새 training Run이나 Optuna trial로 만들지 않는다. `LINTRACK-125` reward 효과는 same-length BASE control 부재로 계속 HOLD다.

## 2026-10-06 g2-submit-5 / LINTRACK-125 제출 연결

2026-10-05의 PERSONAL 3정책 비교 뒤 terminal `model_7450.pt`가 제출 checkpoint로 선택됐다. 사용자는 2026-10-06 실제 Round-5 portal 제출 완료를 보고했으며, [submission Release](https://github.com/SE3C/naver-issacsim/releases/tag/submission-go2-prelim-r5-20261006)에 `policy.pt`, `env.yaml`, user-written `technical_report.txt`, manifest, checksums가 보존됐다. 제출 `policy.pt`의 actor tensor 8개는 OFFICIAL native `model_7450.pt` SHA `b8766030e306dd72160d37292539575d5a1d92c2757f34637dafab3c1582343a`와 CPU exact-match하고, 제출 env SHA `e7eeff96dcecd2248fe35071c38e69acf7cf403e06d976f94abafaf1e07847a9`도 OFFICIAL 7.5K training record와 일치한다. 현재 submission preset 이름은 `g2-submit-5 / LINTRACK-125`다.

이 제출 사실과 이 문서의 PERSONAL evaluator 성격을 섞지 않는다. C4800/C7050/C7450 결과는 checkpoint 선택 근거이고, 2026-10-08 사용자 전달 공식 평가에서 제출 시각 2026-10-06 01:10(시간대 미기재), 종합 88.32/100(시뮬레이션 58.32/70·설계 의도 20/20·리포트 품질 10/10)을 수신했다. 별도 포털 receipt 파일은 미보유다. `LINTRACK-125` reward effect는 same-length BASE control 부재로 HOLD다. Release/intake manifest는 actual-submission 확인 직전에 생성된 snapshot이므로 사후 상태는 registry/AI library에서 이어 기록하고 원본 snapshot을 재작성하지 않는다.

발행된 `model_7050_go2_6terrain_evaluation_20261004-030710_e8bd9e18.zip`은 기존 평가 `004816_9981f1f5`를 감싼 전달본이며 다른 평가 Run이 아니다. [PERSONAL Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-go2-20261004-exp-go2-planar-tracking-terrain-progression-model7050-video-eval)와 [registry 상세](../../../research/experiments/go2/G-001.md)를 연결한다. 이번 2026-10-05 반영은 **보고서와 tracking 문서 갱신**이며 새 GPU 학습·평가·render·comparison-CLI나 새 Release 게시를 실행한 것이 아니다.

## 기존 라이브러리에서 이어 읽기

- [00 시작 안내와 맥락 지도](00_START_HERE_CONTEXT_AND_MAP.md): 핵심팩의 현재 상태와 평가 한계. 2026-09-30의 “재사용 evaluator 미구현”은 과거 상태이며 현재 Windows Go2 구현·실제 검증 범위를 구분한다.
- [07 Go2 학습 코드](07_QUADRUPED_TRAINING_CODE.md): 공식 Go2 task와 학습 코드.
- [11 서버 운영](11_SERVER_OPERATIONS.md): NVIDIA 환경·작업 보존 경계.
- [15 reward 의사결정](15_OPTUNA_REWARD_DECISION_ENGINE.md): 비교 결과와 학습 채택 판단은 분리한다.
- [17 영상 실행](17_ISSACSIMZ_VIDEO_OPERATIONS.md): PERSONAL 영상과 OFFICIAL native play 절차를 구분한다.
- [19 evidence CLI](19_ISSACSIMZ_EXTERNAL_EVIDENCE_CLI.md): server evidence와 artifact provenance 계약.
- [20 H1 공개 실패와 실험 prior](20_H1_PUBLIC_FAILURES_AND_EXPERIMENT_PRIORS.md): 별도 H1 분석 문서로 보존한다.
- H1 companion: `naver-issacsim-eval/WINDOWS_H1_WORKFLOW.md`. 공용 evaluator core를 재사용한다. H1은 설치·CPU 검증에 이어 2026-10-07 `model_2850` PERSONAL 단일 정책 GPU full 자료까지 확보했으나, 2026-10-10 TERM-50/ORIENT/ACTRATE 원본 9,216 episode 대응-index 비교가 완료됐으나 동일 물리 terrain·독립 train 반복과 OFFICIAL 점수는 여전히 미확인이다.

이 문서는 Windows Go2 절차와 검증 증거의 상세 원본이다. 짧은 AGENTS 작업 규칙에서는 H1/Go2 통합 실행기, 직접 실행 요청의 GPU 승인 범위, receipt 재사용 조건, full 전용 및 비교의 사용자 담당 경계를 요약하고 상세는 이 문서로 연결한다.

## 2026-10-09 original4800 / terminal7450 후속 평가·분석

[원문·검증 요약](../experiments/go2/analysis/2026-10-09_GO2_R3_4800_R5_7450_LOCAL_OFFICIAL_COMPARISON.md)의 두 PERSONAL ZIP은 각18파일·6영상, 같은 protocol `806d7e82…45ad`, 128 env × 3 seeds × 9 cases × 20초, complete=true/smoke=false/native exit 0이다. episode **3,471/3,460**, ZIP SHA **f2bb7917…d221 / 4c6aba67…c854**다. 4800 [NVIDIA Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-go2-20261009-g2-submit-3-model4800-video-eval)는 ZIP·checksum·외부 publication manifest만 담는다. Originals `data/raw/private_server_runs/go2/2026-10-09_windows_model4800_video_evaluation/`가 canonical이다. 원 학습 INTERRUPTED 상태와 ZIP 내부 null lineage는 변경하지 않는다.

같은 PERSONAL protocol에서 계단 통합 오차 **0.32029→0.14852**, 실패 **15/783→4/772**, G2 오차 **0.09085→0.07699**로 개선됐지만 공식 계단·전방위 Tracking Score는 하락했다. 로컬 고정 12.5cm/직진 조건과 공식10–15cm·미공개 명령/초기조건의 coverage를 우선 확인한다. 같은 scorer/collector/config와 raw 재집계가 일치하므로 점수 보정·scorer 교체·새 reward 학습을 서두르지 않는다. 과거 PERSONAL all-around REJECT를 공식 추종 대조군 제외로 확대하지 않으며, 4800의 공식 추종 상대 우위와7450의 공식 생존 이득을 모두 보존한다. reward-effect HOLD는 유지한다. G2 세 축 절대 오차는 개선됐지만 xy_rmse **0.09327→0.09493**, roll_pitch_rms **0.04330→0.15349**는 악화했다. 영상은 짧은 지형 패치 후 평지로 나오는 조건이며20초 전체 traversal·camera-off 동일 episode가 아니다. 현재 원인 확정·새 GPU 실행·scorer 수정은 하지 않는다.
