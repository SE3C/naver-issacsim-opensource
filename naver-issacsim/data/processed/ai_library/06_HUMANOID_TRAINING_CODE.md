---
title: "H1 휴머노이드 학습 코드 판단"
purpose: "AI upload bundle — H1 reward 실험·검증의 코드 지도"
sources:
  - "../naver-issacsim-originals/data/raw/server_backup/extracted/training/humanoid/"
  - "data/processed/server_backup/code/training/humanoid/"
  - "data/processed/experiments/h1/training/2026-08-24_OFFICIAL_SERVER_300ITER_BASELINE.md"
  - "data/processed/experiments/h1/analysis/2026-09-07_BREV_L40S_H1_BASELINE_5K_AND_SCREENING.md"
  - "data/processed/planning/historical/07_H1_SECOND_RUN_PARAMETER_COMPARISON_PLAN.md"
---

# H1 휴머노이드 학습 코드 판단

[lin=.55 최신 4정책 코호트 비교](../experiments/h1/analysis/2026-10-16_H1_LIN055_FOUR_POLICY_COHORT_INTAKE.md): rough 진행 회복과 H3 vy/H4 yaw 비용이 공존해 HOLD 유지. 같은 이름의 model4650은 SHA로 구분한다.

**lin=.55 후속 완료:** Run `20261015-105910-h1-actrate0001-lintrack-055-from2700-plus2k`는 OFFICIAL resume +2000, seed42/4096env, console4699/4700, COMPLETED/exit0/validation PASS다. 부모2700 SHA `e54d3389…93ca7ae`에서 lin .50→.55만 변경(action=-.0001, feet=.20, termination=-50 유지), 최종 preset-relative override는 `h1-submit-2 + lin=.55 + action=-.0001`다. 최신 indexed keeper `model_4650.pt` SHA `e8a358a50832f6653b1e558788a5a676ab9a849d3ec6c64e3ed2430e9ff41814`의 PERSONAL Windows 6영상·scenario7 평가도 COMPLETE(128env×3seed×8case,3072행)로 수납했다. console 종점4699와 keeper4650은 다르다. 원본 parent/source IDs=null·imported provenance=false는 유지하며 별도 SHA로 연결한다. **정책 분석 수납 완료·범용 후보 HOLD, 공식 점수·제출 아님**. [분석 원문·계보·한계](../experiments/h1/analysis/2026-10-15_H1_LINTRACK055_MODEL4650_POLICY_REVIEW.md). [학습 Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261015-exp-h1-action-first-planar-tracking-switch-lin055-resume2700-plus2k) · [평가 Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261015-exp-h1-action-first-planar-tracking-switch-lin055-model4650-video-eval). action=-.0003 fresh는 이후 OFFICIAL Run `20261016-033023-h1-actrate-0003-fresh3k` 완료·keeper2950 PERSONAL 보고서 HOLD로 갱신됐다. 상세는 00/14를 따른다. resume만 별도 미실행이다. Optuna v2의 objective/comparison 미승인·Tell 차단은 별개다.

## 2026-10-15 부모·무변경 연장·action 복원 CPU 비교 반영

[원문·계보·판정](../experiments/h1/analysis/2026-10-15_ACTRATE_PARENT_UNCHANGED_RESTORATION_COMPARISON_INTAKE.md): 제공된 CPU raw 비교에서 부모2700 대비 무변경4699의 H5 진행384/384건 감소 → **현재 세 정책의 범용·전진/험지 대표 선정에서 REJECT**, 학습 COMPLETED/PASS와 별개다. 복원4650(`a8249db4…`)은 무변경보다 H5 평균7.919→8.769m 회복하지만 최악6.239→4.845m·mixed tracking .18596→.19816 악화로 **HOLD**. 부모2700도 정지/횡명령 누수 때문에 HOLD, PROMOTE 없음. 전체 mixed tracking 최소나 생존100%만으로 정책을 선정하지 않는다. 선택 checkpoint와 단일 학습 seed의 한계·imported-parent=false/null을 유지한다. 첨부 스크립트 실행 없이 보고서/CSV를 대조한 수납이다.

## 2026-10-15 H1 ACTION 복원 model_4650 · LINTRACK-065 fresh model_4950 정책 판정

[통합 원문 검토](../experiments/h1/analysis/2026-10-15_H1_MODEL4650_LINTRACK065_POLICY_REVIEW.md) · [ACTION 복원 원문](../incoming/other/reviewed/H1_MODEL4650_POLICY_ANALYSIS_20261015.md) · [LINTRACK fresh 원문](../incoming/other/reviewed/H1_LINTRACK-065_POLICY_ANALYSIS_20261015.md). 사용자 제공 보고서의 Windows PERSONAL `scenario7` 원자료 집계와 6영상 판독 결과를 반영한 것이다. **이번 수납에서 ZIP·MP4·checkpoint를 별도 재검증한 것은 아니다.** 두 보고서 모두 8 case×3 seed×128 env=3,072/3,072회 20초 timeout·contact 종료 0. 생존을 완주로 읽지 않는다.

| 구분 | ACTION 복원 +2K `model_4650` | LINTRACK-065 fresh5K `model_4950` |
| --- | ---: | ---: |
| 평가 SHA | `a8249db4…25b84ea` | `b7528923…f448e31ece` |
| 전체 혼합 tracking ↓ | 0.140944 | 0.17994 |
| H1 body 비의도 전진 ↓ | 0.282m | **0.063m** |
| H3 최종 world XY 순변위 크기 평균 ↓ | **0.167m** | **3.102m** |
| H5 rough body 전진 mean/P05/min ↑ | 8.769/7.970/4.845m | 8.995/8.411/7.943m |
| H5 stall>0.05 | 7/384 | 0/384 |
| 판정 | **HOLD: rough 꼬리** | **HOLD: H3 복귀 + rough 저속** |

**계보:** ACTION 복원 Run은 `20261014-142200-h1-actrate-return2700-2k`, parent ACTRATE-0001 `model_2700`에서 reward `action_rate_l2=-0.0001→-0.0005`로 복원한 **OFFICIAL resume**다. 원 evidence는 imported-parent source provenance **false/null**이므로 외부 checkpoint SHA 연결과 별개로 보존한다. LINTRACK fresh Run `20261014-081901-h1-lintrack-065-fresh5k`는 frozen `h1-submit-2` 기준 `track_lin_vel_xy_exp=0.50→0.65` 단일 변경, action=-0.0005, 부모 없는 **OFFICIAL fresh5K**다. 동명 이전 `model_4650`(ACTRATE→lin=.65 resume, SHA `ce7ad586…`)은 **이번 `a8249d…`와 다른 정책**. 학습 Run/evaluator source/리셋·물리 지형 조건 동일성과 reward 인과를 이름만 보고 확정하지 않는다.

**대조 상태:** ACTION 복원과 같은 부모 `model_2700`·무변경 +2K `model_4699`의 CPU 비교는 위 후속 수납으로 완료됐다. LINTRACK fresh는 기존 TERM-50 `model_2800` raw를 조건 확인 뒤 대응 비교할 별도 질문이다. 두 단독 보고서가 과거 정책에 대해 적은 수치는 문서 인용이지 이번 Git 수납에서 통제된 raw A/B를 직접 수행한 것이 아니다. 영상은 정성 근거이며 계단 중앙 완주·boxes 정량 case 미검증, 공식 점수/제출/Optuna trial 없음.

> 날짜별 업데이트는 해당 시점의 기록이다. 최신 Run·제출 상태는 [현재 Experiment registry](../../../research/EXPERIMENTS.md)를 우선한다.

## 2026-10-11 ACTRATE-0001 fresh10K는 별도 완료 Run

> 2026-10-14 [ACTRATE unchanged continuation](../../../research/experiments/h1/exp-h1-action-rate-relaxation.md) Run `20261014-111135-h1-actrate-0001-unchanged-cont2k`: 부모2700 SHA 일치, reward 그대로 lin=.50/action=-.0001, OFFICIAL resume·seed42·4096env·+2000회·console4699/4700, COMPLETED/exit0/PASS. raw parent_run_id=null/provenance=false는 보존하며 별도 SHA 근거로 연결한다. 학습 완료이지 정책 평가·4650 대비 개선·공식 점수가 아니다.

> 최신 별도 학습: [2026-10-14 LINTRACK065 fresh5K](../../../research/experiments/h1/exp-h1-planar-tracking-weight.md), Run `20261014-081901-h1-lintrack-065-fresh5k`, OFFICIAL fresh/no parent, seed42·4096env, console4999/5000, COMPLETED/exit0/PASS. `h1-submit-2 + lin=0.65`; ang=0.5·feet=0.20·termination=-50·action=-0.0005 유지. 전체 설정은 보존 native env/agent YAML·reward source를 따른다. 행동 평가 대기/HOLD이며 기존 ACTRATE-parent lin065 resume(action=-0.0001)의 결과를 대신하지 않는다.

표시한 아홉 reward 값만으로 전체 resolved snapshot이나 이전 Run과의 source/PPO 동일성을 주장하지 않는다. native YAML과 함께 보상 source·source identity를 확인한다.

[model_9999 정책 검토](../experiments/h1/analysis/2026-10-11_ACTRATE0001_MODEL9999_POLICY_REVIEW.md): OFFICIAL Run `20261011-041745-h1-actrate-0001-fresh10k-official`, fresh/no parent·seed42·4096env·10K·exit0/PASS. 표시 설정은 `h1-submit-2 + action=-0.0001`, feet=+0.20이며 전체 resolved config는 보존된 native env/agent YAML을 기준으로 한다. 최종 keeper model_9999의 PERSONAL 행동 분석은 **HOLD**; 기존 ACTRATE-001(-0.001), fresh3K model_2700 및 lin065 resume model_4650의 결과를 덮어쓰지 않는다.



## 2026-10-11 ACTRATE-001 / model_2850 (SHA `1e6d…bb1`) PERSONAL 행동 분석 — HOLD

[원문 보존](../incoming/other/reviewed/H1_MODEL2850_SHA1E6D_POLICY_ANALYSIS_20261010.md) · [근거·결정 기록](../experiments/h1/analysis/2026-10-11_ACTRATE001_MODEL2850_POLICY_REVIEW.md) · [OFFICIAL 학습 Experiment](../../../research/experiments/h1/exp-h1-action-rate-smoothing.md). 기존 OFFICIAL fresh3K `ACTRATE-001` Run `20261010-125324-h1-actrate-001-fresh3k`의 auto-best `model_2850.pt` **SHA-256 `1e6d0950f5bd981ca1f88044e65ae7ee57505c47b92b5caad8c39263f4d93bb1`**가 Windows PERSONAL 6영상/`scenario7` 평가의 체크포인트 SHA와 일치한다. ZIP 내부 `source_run_id=null`은 그대로 두고 별도 기존 학습 증거로 계보를 연결한다. **같은 파일명인 `ORIENT-100/model_2850` (SHA `6aed…f7b0`)와 다른 정책**이다.

제공된 심층 보고서의 정량 결과: **3,072/3,072개 20초 timeout 생존**, H2 전진 body 적분 **15.470m**(목표 15m), H7 push 전진 **10.656m**(목표 10m), H6 경사 상·하 body 적분 **20.297/20.058m**. 다만 **H1 정지 명령에도 비의도 body 전진 1.164m / world XY 순변위 평균 1.151m**, **H3 횡왕복 비의도 전진 1.109m / world XY 순변위 평균 2.177m**가 남는다. H5 rough 진행 평균/P05/최소는 **9.359/8.921/8.372m**, 추종 평균/P95는 **0.17111/0.18947**이고 stall>0.05는 0/384이다. 6개 영상의 초기 boxes/rough 접지는 정성 근거이나 **계단 중앙 다단 통과와 boxes 정량 성공은 입증되지 않는다**. 영상과 camera-off 평가의 지형·명령 trajectory는 별개다.

**판정: 전진 중심 내부 보행 후보 HOLD, 범용 대표 정책 PROMOTE 보류.** 분석 보고서 수납은 새로운 학습·GPU 평가·영상 재실행·Optuna trial·OFFICIAL 점수가 아니다. 우선 이미 보존된 `h1-submit-2 / TERM-50 model_2800` 평가 원자료와 protocol/source/PPO/command/terrain/seed/horizon parity를 검토해 대응 가능한 초기 cohort만 비교한다. 이번 GitHub 반영에서 평가 ZIP/MP4를 직접 재계산하지 않았으며 행동 수치는 제공 보고서의 기록이다.

## 2026-10-10 planned ACTRATE-0001 combinations — native reward checks

**2026-10-14 완료 상태 갱신:** fresh 조합 중 [action+airtime](../../../research/experiments/h1/exp-h1-action-airtime-fresh-interaction.md) Run `20261013-144616-h1-actrate0001-airtime025-fresh3k`와 [action+feet_slide](../../../research/experiments/h1/exp-h1-action-foot-contact-stability.md) Run `20261013-153313-h1-actrate0001-feet_slide-fresh3k`는 각각 OFFICIAL fresh3K COMPLETED / exit0 / validation PASS다. 각 indexed `model_2950`의 Windows PERSONAL 6영상·full 평가도 완료했고 학습·평가 Release 네 건의 원격 크기·SHA를 확인했다. 아래 proposed는 당시 계획이며 현재 미실행을 뜻하지 않는다. 성능 분석·채택은 대기/HOLD다.

[Five user-selected hypotheses](../planning/2026-10-10_H1_ACTRATE0001_FIVE_COMBINATION_HYPOTHESES.md). Frozen OFFICIAL `h1-submit-2/env.yaml` contains active `feet_slide=-0.25`, `feet_air_time=0.20`, `ang_vel_xy_l2=-0.05`, `track_lin_vel_xy_exp=0.5` and `action_rate_l2=-0.0005`. Proposed **Fresh 0→3K** combinations change `action_rate_l2` to -0.0001 plus either `feet_air_time=0.25` or `feet_slide=-0.35`. Proposed independent **ACTRATE-0001 OFFICIAL 3K→+2K Resume** children each change only `feet_air_time=0.25`, `track_lin_vel_xy_exp=0.65` or `ang_vel_xy_l2=-0.08` while retaining action=-0.0001.

Before actual OFFICIAL execution verify live checkout, actual allowed `training/humanoid/humanoid_rewards.py` values, active reward terms and full resolved env/agent and PPO. For three sibling resumes, inspect index/source_path/checkpoint byte SHA; do not confuse evaluated `model_2700` with latest `model_2950`. Multiple independent sibling Resume Runs are allowed but none of their 5K children should be resumed again to 7K under this plan. 이번 갱신은 기존 완료 산출물의 상태 동기화이며 새 GPU 실행이 아니다. `feet_slide` is a literal native field, not a new descriptor.


## 2026-10-10 ANGTRACK-065 vs TERM-50 원본 대조 — H3 악화와 yaw 이득

[원본 직접 대조 보고서](../experiments/h1/analysis/2026-10-10_H1_ANGTRACK065_TERM50_DEEP_RAW_COMPARISON.md). 두 보존 ZIP에서 3,072 최초 cohort의 evaluator config/코호트 key 일치 확인, ANG 15 H3 접촉 종료 뒤 재시작 15행은 별도로 제외했다. H3 TERM→ANG `vy_error` **0.06848→0.18601**, stall **0.00912→0.34339**, 종료 **0/384→15/384**. H4 yaw error **0.11934→0.07704**로 하락하지만 전 case 혼합 tracking **0.157118→0.130669**와 달리 XY RMSE **0.112589→0.125612**는 악화. H5 평균 진행 **8.8961→8.8949m**로 개선 없음. ANG의 정책 선택 **HOLD**; reward 인과/실제 물리 terrain parity/공식 점수 미확인. 기존 단독 분석의 'TERM 대조 미실행'은 이번 재집계 이전 기록이다. 새로운 학습/평가/GPU 작업 없음.

## 2026-10-10 ANGTRACK-065 / model_2950 — PERSONAL lateral-contact failures, HOLD

[원문](../incoming/other/reviewed/H1_ANGTRACK-065_POLICY_ANALYSIS_20261010.md) · [행동 근거·분모 판정](../experiments/h1/analysis/2026-10-10_ANGTRACK065_MODEL2950_POLICY_REVIEW.md). OFFICIAL fresh3K Run `20261009-155344-h1-angtrack-065-fresh3k` best/last `model_2950.pt` SHA `6a6f456e…68e118c`가 Windows PERSONAL `scenario7`에 사용된 것으로 별도 training/evaluation 증거가 연결된다. **3,072 최초 cohort / 3,087 episode 행**(H3 15 base-contact 종료 뒤 각각 restart). H3 최초 20초 종료 성공은 **369/384**, contact failure **15/384 (3.91%)**이며 짧은 `evaluation_end` 15개를 20초 생존으로 세지 않는다. H3 stall 0.3532, vy error 0.1871m/s, tracking 0.2203(399행 평균). H1 zero command 비의도 body 전진 0.875m. H2 14.703m, H4 yaw abs error 0.0770rad/s, H5 rough 평균 8.895m, H6 경사 상/하 19.571/19.235m, H7 push 9.996m 등 유효 전진도 있다.

**정책 HOLD**: 회전 reward `track_ang_vel_z_exp=0.65`의 인과 개선 증거가 아니라 단일 정책 행동 진단이다. 영상에 순수 lateral H3가 없고 stairs/boxes의 20초 반복 정량 성능은 미측정. 영상의 `06_slope_down_10deg.mp4` 짝수 프레임 검정은 별도 캡처 문제. 기존 TERM-50/ORIENT/ACTRATE 9,216행의 대응 데이터에 **이 정책은 미포함**. TERM-50 raw를 우선 대조하되 새 GPU 자동실행은 없다.

## 2026-10-10 TERM-50/ORIENT/ACTRATE 원본 평가 직접 비교 — 관찰된 trade-off

[직접 재집계 보고서](../experiments/h1/analysis/2026-10-10_H1_SCENARIO7_RAW_3POLICY_MATCHED_ANALYSIS.md). 평가 ZIP 3개, 원본 `episodes.jsonl` 각 3,072개, ZIP SHA+CRC, 동일한 `resolved_configs.json` 바이트와 `evaluation_manifest.protocol`·소스·agent·case/seed fingerprint, 전체 cohort key/ID 대응을 실제 검증했다. 각 평가 3,072/3,072 episode 20초 생존/낙상 종료 0건이며 **기존 자료를 재분석했을 뿐 GPU·학습·제출은 실행하지 않았다**.

동일 evaluator의 tracking 전체 평균은 TERM `0.15712`, ORIENT `0.14041`, ACTRATE `0.14534`. 단, 혼합 지표 감소 대부분에 yaw-rate 오차 감소가 기여하고 x속도 절대오차 평균은 TERM이 가장 낮다. H1 정지 비의도 전진 `1.352 / 1.633 / 1.987m`(TERM/ORIENT/ACTRATE); H5 rough 평균 `8.896 / 9.451 / 9.948m`; H5 최악 `2.639 / 7.831 / 8.815m`. **ORIENT roll/pitch RMS 전체 `0.08015`가 TERM `0.03381`, ACTRATE `0.03019`보다 크며, ACTRATE action 변화 RMS `0.45687`이 가장 높다.** 따라서 tracking·몸통 자세·동작 비용·험지 진행을 구분한다. 동일 cohort 키도 각 terrain/reset 실제 trajectory의 완전 동일성 또는 `reward` 인과를 증명하지 않는다. 정책 모두 HOLD.

## 2026-10-10 H1 행동 비교 — 같은 평가기, 서로 다른 reward/source 계보

[상세 비교와 GitHub 평가 ZIP 보존 경로](../experiments/h1/analysis/2026-10-10_H1_SCENARIO7_CROSS_POLICY_REPORT_LEVEL_COMPARISON.md). `TERM-50/model_2800`, `ORIENT-100/model_2850`, `ACTRATE-0001/model_2700`의 평가 manifest는 H1 `scenario7` protocol `d406a296…7062d34`, Windows evaluator task/handoff, 평가 seed·env·시간 일치를 보인다. 원본 ZIP은 Release/LFS에 존재하지만 여기서는 바이너리 접근 불가로 `episodes.jsonl`을 직접 읽거나 baseline case 결과를 계산하지 못했다. 따라서 숫자는 세 **기존 단일 정책 분석 보고서 간 기술통계**다.

8 case 비교에서 ORIENT tracking은 ACTRATE보다 5개 case에서 낮고, H1/H3 비의도 전진도 각각 `1.633/1.180m`로 ACTRATE `1.987/1.677m`보다 작으며 8 case 전체 action-change RMS가 더 작게 보고됐다. ACTRATE는 H2 및 H6 tracking, H5 rough mean/P05 진행 `9.948/9.592m`(ORIENT `9.451/8.863m`)에 강점이 있으나 H5 worst tracking은 `0.2908` vs ORIENT `0.2412`로 불리한 부분도 있다. `LINTRACK-075`의 정지/횡이동 비의도 전진은 `0.415/0.480m`이지만 이는 PERSONAL corrected5K이고 H5 severe stall 사례(전진 `2.871m`, stall `0.664`)가 있어 같은 OFFICIAL reward test로 세지 않는다. 정책 후보는 **모두 HOLD**; 분석·평가 완료, reward 인과, 공식 채점, 계단 다단 완주는 서로 다르다.

## 2026-10-10 ACTRATE-0001 model_2700 — 단일 정책 행동 분석 완료, HOLD

[원문 보고서](../incoming/other/reviewed/H1_MODEL2700_POLICY_ANALYSIS_20261010.md) · [AI 라이브러리 판정](../experiments/h1/analysis/2026-10-10_ACTRATE0001_MODEL2700_POLICY_REVIEW.md) · [Experiment](../../../research/experiments/h1/exp-h1-action-rate-relaxation.md).

OFFICIAL fresh 3K Run `20261009-142350-h1-actrate-0001-fresh3k`의 auto-best `model_2700.pt` SHA `e54d3389…93ca7ae`는 후속 Windows PERSONAL 6영상+`scenario7`의 정책 SHA와 연결됐다. 3,072/3,072개 20초 생존은 **평가 실행 완료**다. H2 전진 body 15.326m, H7 push 10.542m, H6 경사 상/하 20.052/19.834m는 실제 이동 긍정 근거다. **H1 정지 명령의 비의도 전진 1.987m, H3 횡이동 중 비의도 전진 1.677m**, H5 rough 최악 코호트 tracking 0.2908/전진 8.815m/roll-pitch RMS 0.0999와 **다단 계단 통과 미검증** 때문에 전천후 대표 정책은 **HOLD**다. `01_stairs.mp4`의 검정 프레임은 캡처 문제이고 실제 낙상은 아니다.

이 영상의 전역 maneuver/push 명령과 camera-off `scenario7`의 case별 명령·seed·terrain은 다르다. 평가 설정의 reward와 학습 resolved reward도 혼동하지 않는다. 현재 보고서는 **단일 checkpoint 분석 완료**이지 `action_rate_l2=-0.0001`의 reward 인과효과/공식 점수 증거가 아니다. `TERM-50 model_2800`을 우선 대조, `ORIENT-100/model_2850`을 별도 행동 참고군으로 동일 evaluator raw를 비교하되 신규 GPU 작업은 승인하지 않았다. `ACTRATE-001` 학습·PERSONAL 분석은 완료/HOLD이고 `ANGTRACK-065` 단일 정책 분석은 수신됐으나 대조 raw 비교는 미완료다.

## 2026-10-10 LINTRACK-075 corrected5K 행동 평가 — 실험 계보와 evaluator 구분

[원문](../incoming/other/reviewed/H1_LINTRACK-075_CORRECTED5K_POLICY_ANALYSIS_20261010.md) · [요약](../experiments/h1/analysis/2026-10-10_LINTRACK075_CORRECTED5K_MODEL4997_POLICY_REVIEW.md) · [H-008 Run 연결](../../../research/experiments/h1/H-008.md).

PERSONAL corrected H-008 R04 continuation final `model_4997.pt`(SHA `4349fe56…b6d`)에 연결된 Windows PERSONAL `scenario7`(8 case×3 eval seeds×128 env = 3,072 episode)와 6영상에 대한 **후속 정책 행동 판정은 HOLD**다. 3,072/3,072 20초 생존과 H2 전진 15.015m, H7 push 10.038m, H6 경사 상/하 19.943/19.776m(body-frame)는 실제 이동 성공 근거지만 H5 worst cohort 전진 2.8708m/stall 0.664, H1 zero world drift 0.516m, H3 횡이동 왕복 잔류 1.280m, H6 yaw/action 비용, 계단/boxes 정량 미검증이 남는다.

**주의:** 평가 환경 `resolved_configs.json`에 남은 `track_lin_vel_xy_exp=0.5`와 `termination_penalty=-5`는 evaluator 생성 당시 기본 reward이고 `LINTRACK-075` 정책을 학습한 resolved reward는 아니다. ZIP 내부 `policy.source_run_id/preset=null`은 원형을 유지하며, training checkpoint identity는 별도의 H-008 train record와 SHA로 연결한다. 훈련 완료·PERSONAL evaluator 완료·실제 정책 품질과 OFFICIAL 점수는 별개의 판정이다. 입력 원문이 분석한 MP4/episode를 이 문서 갱신 단계에서 새로 실행·복제한 것은 아니다.

## 2026-10-07 ORIENT-100 실제 행동 진단

OFFICIAL fresh 3K 학습 Run `20261006-133517-h1-orient-100-fresh3k-official`과, checkpoint SHA로 연결된 `model_2850.pt`의 **Windows PERSONAL 6지형 영상 + 별도 `scenario7` 8 case full 평가**를 구분한다. raw episode 3,072/3,072개가 20초 생존했고 H2 전진 15.408m, H7 push 조건 전진 10.530m의 body 전진 적분을 기록했으나, **H1 balance +1.633m**, H3 lateral **+1.180m**의 원치 않는 전진도 있다. H5 rough 평균 tracking 오차 **0.1709**, 전진 최소 **7.831m**로 worst-case 저하가 보인다. 영상의 boxes/rough 초반 진행과 계단 중앙 다단 통과 입증은 다른 주장이다.

**선택 판정 HOLD**: 유효한 보행 후보를 보존하되 현재는 `h1-submit-2 / TERM-50` 3,072 cohort-key raw 대조가 확보돼 tracking·진행·자세 trade-off를 검증했다. 다만 훈련 Run 반복·동일 물리 초기조건·checkpoint 시점 통제가 없어 `flat_orientation_l2=-1.0`의 **인과적 reward 효과는 미확인**. H1 단일 정책 Windows GPU full은 2026-10-07 자료상 완료됐고 2026-10-10에는 보존된 ZIP 3개의 대응-index 분석도 완료됐으나 공식 점수·독립 학습 통제 비교는 없다. [원문](../incoming/other/reviewed/H1_ORIENT-100_POLICY_ANALYSIS_20261007.md) · [Experiment](../../../research/experiments/h1/exp-h1-rough-terrain-orientation-relaxation.md).



## 수정·확인 위치

- 참가자 실험의 중심 파일은 `training/humanoid/humanoid_rewards.py`다.
- 학습·play·환경 설정·결과 정리의 현재 코드 기준은 Originals `server_backup/extracted/training/humanoid/`와 동기화된 NVIDIA `training/humanoid/`다. `data/processed/server_backup/code/training/humanoid/`는 과거 분석용 추출본이다.
- task 설정이나 finalize 구현은 동작 이해·검증용이다. 허용되지 않은 파일을 수정하지 않는다.

## H1 reward 표기 규칙

AI 답변과 새 실험 이름은 가능하면 실제 reward 변수에서 바로 읽히는 아래 약어를 쓴다. **약어와 숫자 값 사이는 항상 하이픈(`-`)으로 분리한다.** 음수 penalty 계열은 값의 부호를 이름에서 별도 음수 기호로 중복 표현하지 않고 절댓값으로 읽는다(예: `TERM-50` = `termination_penalty=-50`, `HIPDEV-030` = `joint_deviation_hip=-0.30`). 숫자 인코딩은 프로젝트 convention이며 정확한 값은 항상 config/evidence가 기준이다.

| 실제 변수 | 기본 약어 | baseline |
| --- | --- | ---: |
| `track_lin_vel_xy_exp` | `LINTRACK` | 0.5 |
| `track_ang_vel_z_exp` | `ANGTRACK` | 0.5 |
| `feet_air_time` | `AIRTIME` | 0.2 |
| `termination_penalty` | `TERM` | -5 |
| `flat_orientation_l2` | `ORIENT` | -1.5 |
| `ang_vel_xy_l2` | `ANGXY` | -0.05 |
| `joint_deviation_hip` | `HIPDEV` | -0.2 |
| `joint_deviation_torso` | `TORSODEV` | -0.1 |
| `action_rate_l2` | `ACTRATE` | -0.0005 |

예: `LINTRACK-075`, `ANGTRACK-075`, `AIRTIME-025`, `TERM-50`, `HIPDEV-030`, `ACTRATE-0025`. 조정 대상 9개 외 활성 reward(`dof_acc_l2`, `dof_pos_limits`, `feet_slide`, `joint_deviation_arms`)는 설정 해석에는 포함하되 현재 대회 실험 이름의 조정축으로 취급하지 않는다.

## H1에서 먼저 볼 것

1. 제자리 균형과 기본 전진 명령 추종을 기준점으로 만든다.
2. 회전·측면 이동·요철·경사·외란 회복을 단계적으로 추가한다.
3. 빠르게 걷게 하려다 자세 안정과 낙상 회복을 잃지 않는지 영상으로 확인한다.

## 첫 공식 서버 기준선에서 확인된 것

2026-08-24 baseline 300회 실행은 4096 envs, seed 42로 완료됐고 report 기준 전체 4분이 걸렸다. 마지막 terrain level은 0.00, fall rate는 100.0%, exploration std 평균은 0.633이었다. 이는 학습·export 파이프라인 확인에는 유효하지만 안정 보행 정책이나 reward 후보의 우열을 판단할 결과는 아니다.

실제 `env.yaml`의 nonzero reward는 참가자 수정 대상 9개 외에 `dof_acc_l2`, `dof_pos_limits`, `feet_slide`, `joint_deviation_arms`가 더 있어 총 13개다. 참가자는 허용된 reward 파일만 수정하되, 결과를 해석할 때 기본 4개의 영향도 포함한다.

`termination_penalty=-5`는 report 추천 구간 밖이지만 300회 실패의 단독 원인으로 단정하지 않는다. 300회 paired 실험은 초기 방향 확인용이며, 성능 후보로 판단하기 전에는 동일 reward의 더 긴 baseline으로 terrain·fall·episode-length 개선 시점을 확인한다.

## 개인 L40S 5K와 1K screening에서 확인된 것

2026-09-07 개인 Brev L40S에서 기본 reward 5K가 완료됐다. 4,096 envs, seed 42 조건의 마지막 값은 episode length 742.97, terrain 5.054, time-out 66.79%, base-contact 종료 33.21%, XY error 0.342, yaw error 0.652였다. 첫 공식 300회보다 학습이 진행된 개인 기준선이지만 공식 제출 성능은 아니다.

동일 환경 1K 단변수 screening에서는 `termination_penalty=-50`만 terrain 4.823, time-out 68.34%, episode length 799.97로 장기 확인 후보가 됐다. `track_ang_vel_z_exp=0.75`는 terrain 0·base-contact 100%였고, hip/torso penalty 완화는 terrain 0.010·base-contact 95.68%여서 standalone 확장을 중단한다. `TERM-50`의 yaw error는 1.577이므로 생존성 후보와 회전 성능 후보를 같은 뜻으로 해석하지 않는다.

legacy `TERM50` 라벨로 표시된 MP4는 baseline 1K 영상과 동일한 잘못 연결된 파일이다. 이 legacy `TERM50` 영상 관찰은 폐기하고 해당 checkpoint에서 다시 렌더한 뒤에만 동작 품질을 판단한다.

## 역사적 공식 300회 진단 설계와 현재 판단

첫 공식 실행의 누락 로그를 복원하려던 당시 제안은 같은 seed·환경의 `H1-B0-RECAPTURE`(reward unchanged, 300회)와 `H1-S1-TERM50`(`termination_penalty -5→-50`만 변경, 300회)를 짝지어 보는 것이었다. 옛 `S1`은 단일변수 스크리닝 이름이지 새 `HS-xxx` reward schedule이나 이미 수행한 Run이 아니다. 이 설계는 **현재 실행 지시가 아니다.**

이후 `h1-submit-2 / TERM-50` 공식 fresh 5K(legacy H-001 R02)는 2라운드 86.37/100을 받았고, `feet=-0.2` 개인 부모의 과거 자식은 상대 비교용으로 정정됐다. 새 `feet=+0.2` corrected PERSONAL Run과 9/27 `AIRTIME-025` fresh·continuation, `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch fresh Run은 완료됐다. 현재 계보·상태와 matched 비교 조건은 [14번](14_H1_NEXT_RUN_PARAMETER_COMPARISON.md) 및 [가설 registry](../../../research/EXPERIMENTS.md)를 따른다. 다른 reward 계수의 총 reward 절댓값만으로 정책을 서열화하지 않는다.

## H1 single-delta sequence — 2026-10-06 접수 갱신

ORIENT-100 Run `20261006-133517-h1-orient-100-fresh3k-official`는 OFFICIAL fresh 3K COMPLETE/PASS다. 2026-10-07 `model_2850` PERSONAL 행동 평가는 HOLD이며 reward 인과효과는 미검증이다. 실제 feet=0.20, term=-50, orientation=-1.0, seed 42, 4096 env를 확인했다. auto best 2850과 마지막 보존 2950은 다르다. [원본/Release 접수](../experiments/h1/training/2026-10-06_ORIENT100_OFFICIAL3K_EVIDENCE_INTAKE.md). 아래는 역사적 사전 설계이며 ACTRATE-001도 이후 OFFICIAL fresh3K COMPLETE/PASS·PERSONAL 분석 수납/HOLD로 갱신됐다.

원래 ORIENT-100·ACTRATE-001 두 가지 질문에서 시작했으며, 2026-10-10까지 ORIENT-100·ACTRATE-0001·ANGTRACK-065와 ACTRATE-001 모두 OFFICIAL fresh3K 학습 완료다. ACTRATE-001 PERSONAL 행동 분석은 이후 수신돼 HOLD다. 다음 문장은 초기 두 가지 가설의 **역사적 계획**을 설명한다. ① `exp-h1-rough-terrain-orientation-relaxation / ORIENT-100`: frozen `h1-submit-2`에서 `flat_orientation_l2 -1.5 → -1.0`만 바꾼 **OFFICIAL fresh 3K**. ② `exp-h1-action-rate-smoothing / ACTRATE-001`: ORIENT evidence를 먼저 검토한 뒤 frozen `h1-submit-2`에서 `action_rate_l2 -0.0005 → -0.001`만 바꾼 **별도 OFFICIAL fresh 3K**. ORIENT는 실제 seed 42·4096 env로 완료됐고 ACTRATE는 같은 조건을 목표로 계획 중이며 서로의 reward 변경이나 checkpoint를 상속하지 않는다. 정확한 실행값은 실제 official reward source와 evidence의 resolved config로 다시 확인한다.

현재 H1 PERSONAL evaluator의 공용 core를 재사용하는 Windows 통합 launcher가 `C:\NCRC\h1_6terrain_video.bat`로 설치됐고 CPU 회귀 테스트 60개와 PowerShell/설치 파일 검증을 통과했다. H1은 경사 ±10°의 고정 6영상 뒤 별도 camera-off `scenario7` 8 case 전체 평가를 사용하며 standalone/integrated smoke 옵션은 제거됐다. 다만 **2026-10-06 설치 검증 때에는 H1 GPU full이 없었으나 2026-10-07 `model_2850` PERSONAL full 결과가 확보됐다. 기존 TERM-50 대비 원본 ZIP 대응-key 비교는 2026-10-10 추가 완료됐다(동일 물리 reset/terrain 완전 일치·Windows 비교 CLI 실행은 별도 미검증).** 따라서 새 3K 결과는 현재 확보된 OFFICIAL fresh3K control 및 동일 평가기 raw를 우선 대조하고, 과거 5K TensorBoard·console은 서로 다른 학습량/질문을 구분하는 보조자료로만 분석하며, native 영상은 정성 evidence로만 사용한다. 설치·CPU 검증 자체를 평가 결과로 세지 않으며 공식 점수 개선은 실제 제출 평가 전에는 주장하지 않는다.

`ORIENT-100` 뒤의 별도 single-delta Experiment인 `ACTRATE-001` (`action_rate_l2 -0.0005 → -0.001`)도 이후 **OFFICIAL fresh3K COMPLETE/PASS · PERSONAL model_2850 행동 HOLD**가 확인됐다. 순서는 ORIENT evidence를 먼저 검토한 뒤 ACTRATE를 실행하는 것이지만, ACTRATE는 ORIENT checkpoint를 resume하지 않고 frozen `h1-submit-2`에서 fresh 3K로 시작한다. 두 설정을 같은 Run에 합치지 않으며 실제 실행 전에는 Run ID를 발급하지 않는다. 세부 계획은 [14번](14_H1_NEXT_RUN_PARAMETER_COMPARISON.md), [ORIENT plan](../../../research/experiments/h1/exp-h1-rough-terrain-orientation-relaxation.md), [ACTRATE plan](../../../research/experiments/h1/exp-h1-action-rate-smoothing.md)을 따른다.

## 2026-10-10 H1 tracking 단일변수 가설 — 완료된 두 OFFICIAL Run과 남은 ACTRATE-001

기존 `ACTRATE-001`(`action_rate_l2=-0.001`)은 이후 **OFFICIAL fresh3K Run `20261010-125324-h1-actrate-001-fresh3k` 완료 / PERSONAL 행동 분석 HOLD**로 갱신됐다. 아래 두 독립 질문은 frozen `h1-submit-2 / TERM-50` 대비 한 reward만 바꾸는 **OFFICIAL fresh 3K (seed42, 4096 env) COMPLETED/PASS**이며 checkpoint 부모가 없다. `ACTRATE-0001`의 PERSONAL `model_2700` 고정평가 3,072 episode와 단일 정책 행동 분석은 완료됐고(HOLD), 기존 TERM-50 대비 동일 프로토콜 raw 대응-index 기술비교는 완료됐지만 독립 학습 반복·인과 검증은 미완료다. `ANGTRACK-065`는 영상·고정평가 및 단일 정책 분석을 수신했고 H3 최초 cohort contact 종료 15/384 때문에 HOLD다.

| Experiment / descriptor | 단일 delta | 질문 |
| --- | --- | --- |
| [`exp-h1-action-rate-relaxation / ACTRATE-0001`](../../../research/experiments/h1/exp-h1-action-rate-relaxation.md) | `action_rate_l2 -0.0005→-0.0001` | 제약 완화로 명령 전환 반응과 전체 x/y/yaw 추종을 높일 수 있는가? |
| [`exp-h1-angular-tracking-boost / ANGTRACK-065`](../../../research/experiments/h1/exp-h1-angular-tracking-boost.md) | `track_ang_vel_z_exp 0.5→0.65` | 회전 보상 강화를 통해 yaw·통합 tracking을 개선하면서 지형 진행을 유지하는가? |

`ACTRATE-0001`: Run `20261009-142350-h1-actrate-0001-fresh3k`, automatic-best `model_2700.pt` SHA `e54d3389…93ca7ae`, final keeper `model_2950.pt` 별개. [OFFICIAL 근거](../experiments/h1/training/2026-10-09_ACTRATE0001_OFFICIAL3K_EVIDENCE_INTAKE.md) / [PERSONAL 모델2700 평가](../operations/windows_h1_video_evaluation/2026-10-10_ACTRATE0001_MODEL2700_PUBLICATION.md). `ANGTRACK-065`: Run `20261009-155344-h1-angtrack-065-fresh3k`, automatic-best·last keeper 둘 다 `model_2950.pt` SHA `6a6f456e…68e118c`. [OFFICIAL 근거](../experiments/h1/training/2026-10-10_ANGTRACK065_OFFICIAL3K_EVIDENCE_INTAKE.md). `ACTRATE-0001/model_2700` 단일 정책 행동 품질 판정은 HOLD이고, 대조군 대비 성능 우위·reward 인과·NCRC 공식 점수는 미확인이다. 이미 보존된 OFFICIAL unchanged `h1-submit-2` fresh3K control `20261008-062732-h1-term-50-fresh3k-control`와 연계된 model_2800 PERSONAL full 자료를 1순위 후보 대조로 삼되, source/PPO parity와 실제 paired A/B는 별도 확인한다. 역사적 PERSONAL BASE `ANGTRACK-075` 1K base-contact 100% 붕괴와 corrected PERSONAL `LINTRACK-075`의 XY 이득·yaw 손실은 위험 prior이며, 신규 H1 OFFICIAL 결과가 아니다. 생존/학습 접촉률과 공식 tracking을 혼동하지 말고 x/y/yaw 추종·정지 drift·terrain 진행/stall·fall·action delta로 평가한다. 문서 반영은 GPU 승인이나 학습 실행이 아니다.

## 자주 생기는 실패

| 증상 | 우선 점검 |
| --- | --- |
| 한 발을 오래 들거나 깡충거림 | 발 체공 보상 과대·접촉 관련 보상 균형. |
| 속도는 나지만 자주 넘어짐 | 자세·낙상·제어 비용의 억제가 너무 약한지 확인. |
| 제자리 회전·진동 | 목표 속도 추종과 방향 안정 reward의 균형, 명령 범위 확인. |
| 평지에서는 좋지만 지형 실패 | 난이도 진행, 지형 노출, recovery 관찰을 분리해 검사. |

## 제출 판단

높은 단일 지표보다 여러 명령·지형에서 재현되는 보행을 우선한다. 최종 제출 파일과 실제 설정·기술 개선 리포트의 설명이 일치해야 한다.

Fresh run의 `model_best.pt`는 `Train/mean_reward` 최고 step에 가장 가까운 저장 checkpoint다. Resume run의 현재 finalizer는 전체 raw 최고를 그대로 쓰지 않고 `lo + max(50, floor((hi-lo)×0.10))` 이전 step을 warm-up으로 제외한 eligible 구간의 최고 reward에 가장 가까운 checkpoint를 고른다. 따라서 raw 전체 최고와 report 최고가 다르다는 사실만으로 report 불일치라고 판정하지 않는다. 먼저 같은 필터를 raw event에 재현한다. 300회 fresh baseline에서는 reward peak step 287에 가장 가까운 iteration 299 checkpoint가 선택됐다. 어느 경우도 공식 시나리오 성능 최고 정책을 뜻하지 않는다.

특히 충분히 긴 resume에서는 curriculum 재적응 구간의 reward peak가 대표 정책을 잘못 가리킬 수 있다. 자동 `model_best.pt` 대신 final numbered checkpoint를 기본으로 쓰고, 마지막 수백 iteration에서 terrain·tracking·낙상이 함께 뚜렷하게 악화된 경우만 직전 checkpoint를 검토한다.

## Optuna 초기 탐색 범위

evaluator가 완성된 뒤 별도 study 두 단계로 좁게 탐색한다.

- Stability: `termination_penalty` 절댓값 5~100, `flat_orientation_l2` 절댓값 0.3~3.0, `ang_vel_xy_l2` 절댓값 0.02~0.30
- Tracking/Gait: `track_lin_vel_xy_exp` 0.5~1.5, `track_ang_vel_z_exp` 0.5~1.5, `feet_air_time` 0.10~0.30

음수 penalty는 양수 절댓값으로 log sampling한 뒤 음수로 적용한다. 두 단계를 한 study에 섞지 않고, Stability 상위 안전 영역을 고정한 뒤 Tracking/Gait를 연다. `Train/mean_reward`만 objective로 사용하지 않는다.
