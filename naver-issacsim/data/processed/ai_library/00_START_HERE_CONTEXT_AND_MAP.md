---
bundle_title: "프로젝트 맥락과 AI 입력 안내"
source_documents: 21
purpose: AI upload bundle
---

# 프로젝트 맥락과 AI 입력 안내

## 2026-10-22 실제 접수11650과 별도 직접 평가40500

[원본 PDF·계보·표시 정밀도·비교](../experiments/h1/analysis/2026-10-22_H1_MODEL40500_ORGANIZER_DIRECT_EVALUATION.md): model40500/ang=.60의 운영진 별도 직접 평가는 자동56.9/70·의도20·코멘트10·총86.9/100이다. 실제 7라운드 접수 model11650/ang=.70·자동57.05/70과 `h1-submit-7` identity는 그대로다.40500은 R6 model9999에서 이어학습한 별도 Run이다. 표시 시나리오 합56.8과 보고총계56.9를 함께 보존한다. 학습 지표 개선에도 이번 점수 상승은 확인되지 않았다. 서로 다른 부모·reward 경로를 단순 학습량 효과로 해석하지 않으며, 장기 학습 무효·평가기 오류·합격 여부를 확정하지 않는다.

## 2026-10-18 기존 설정 10K TOP10 외주 자문 수신

[원문·52행 검토표·Run/SHA 보완](../experiments/h1/analysis/2026-10-18_H1_10K_TOP10_SELECTION_INTAKE.md): 외주 실행 우선순위는 JOINT lin=.65/ang=.60/action=-.0003 fresh5K4950 연장 → action=-.0003 fresh3K2950 연장 → ORIENT-100 연장이다. **자문이며 실행 확정·승격 아님**, 기존 HOLD·제출 preset 유지. ORIENT 평가2850과 keeper2950은 다르며2950은 미평가다. JOINT keeper4950 SHA와 auto-best4800 SHA도 다르다. TOP10 전부 실행이나 새 reward 발굴을 뜻하지 않는다.

## 2026-10-18 후보3 LIN075 + ACT0001 보고서 수신 — HOLD

[원문·실제 Run/SHA·검토](../experiments/h1/analysis/2026-10-18_H1_LIN075_ACTION0001_MODEL2850_POLICY_REVIEW.md): OFFICIAL fresh3K Run `20261017-140610-h1-lintrack-075-actrate-0001-term-50-fresh3k`, `h1-submit-2 + lin=.75 + action=-.0001`의 평가2850(`82384210…934f959`) 보고서를 수신했다. 진행 H5 평균/P05/최소9.867/9.640/9.514m·stall>.05 0/384이나 H4/H5 yaw .2725/.2730rad/s, H3 world 잔류2.605m로 **HOLD**. keeper2950은 미평가다. 보고서의 학습 출처 미확인은 현재 index/publication SHA 연결로 보완하고 원문·raw null은 유지한다. boxes 짝수500프레임 black은 보고된 capture 결함이며 새 렌더 재현·정책 낙상이 아니다. 후보1도 OFFICIAL 학습 완료/PASS이나 별도 평가·보고서 미수신이다. 새 제출·공식 점수·paired 비교 없음.

## 2026-10-17 자세·고관절 완화형 fresh3K 보고서 완료 — HOLD

[후보2 원문·실제 Run/SHA·검토](../experiments/h1/analysis/2026-10-17_H1_JOINT_TRACKING_POSTURE_MODEL2850_POLICY_REVIEW.md): OFFICIAL Run `20261017-072659-h1-lintrack-065-angtrack-060-actrate-0003-orient`, `h1-submit-2 + action=-.0003 + orientation=-1.0 + hip=-.1 + ang=.60 + lin=.65`, 평가2850 SHA `4a343750…b0025d`의 PERSONAL 보고서를 수신했다. **HOLD**: 생존3072/3072에도 H1/H3 비의도 body 후진−.719/−.679m, H5 전진 평균/P05/최소8.024/7.460/6.721m와 지속 속도 손실이 남는다. 최신 keeper2950은 미평가다. 보고서의 학습 계보 미확인은 기존 train index/publication의 SHA 연결로 보완하되 원 null metadata는 유지한다. 이전 JOINT5K와의 정식 A/B·공식 점수·제출은 없고, 수납자는 원 episode/영상을 재실행하지 않았다.

## 2026-10-17 joint tracking fresh5K 학습·평가·보고서 완료 — HOLD

[원문·Run/SHA·수납 범위](../experiments/h1/analysis/2026-10-17_H1_JOINT_TRACKING_MODEL4950_POLICY_REVIEW.md): OFFICIAL Run `20261017-015509-h1-lintrack-065-angtrack-060-actrate-0003-fresh5`, `h1-submit-2 + lin=.65 + ang=.60 + action=-.0003`, keeper4950 SHA `2df05840…62bc478`의 PERSONAL 분석은 **HOLD**다. 생존3072/3072, H5 진행평균/P05/최소8.853/8.403/7.930m·stall>.05 0/384로 정체보다는 저속이 문제다. H1 body x−.259m, H3 world 잔류.739m는 별도 진단. 같은 이름인 이전 LINTRACK0654950(`b7528923…`)과 다른 정책이며 상대 raw CPU 비교·공식 점수·제출은 미확인/미실행이다. 세 reward 동시 변경의 개별 인과효과를 말하지 않는다.

## 2026-10-17 action=-.0002 fresh3K 보고서 완료 — HOLD

[원문·Run/SHA·검토 범위](../experiments/h1/analysis/2026-10-17_H1_ACTION0002_MODEL2950_POLICY_REVIEW.md): OFFICIAL Run `20261016-150803-h1-actrate0002-fresh3k`, `h1-submit-2 + action=-.0002`, keeper2950 SHA `eaa7a50c…ac4d34fb`의 PERSONAL 평가·보고서 수신 완료. **HOLD**. 3072/3072 생존에도 H1 비의도 body전진1.842m, H3 1.225m, H5 진행 평균/P05/최소8.941/8.573/6.983m·stall>.05 3/384다. H3 world 잔류는 공식 원점복귀 실패 기준이 아니다. 단독 분석이며 -.0003 등과의 직접 비교·공식 점수 개선·Optuna Tell은 미실행이다.

**2026-10-17 판단 원칙:** [다음 실험의 질문·목표 구분](../planning/2026-10-16_H1_EVIDENCE_AND_RESEARCH_NEXT_EXPERIMENTS.md). H1 공식 제출 판단과 계단·박스 등 보조 행동 관찰을 구분한다. 보조 영상의 완주 미입증만으로 공식 후보를 자동 탈락시키지 않으며, 로컬 순위를 공식 점수 예측으로 쓰지 않는다. config 탐색·독립 학습 seed 확인·고정 config 추가 학습·reward 전환 resume는 별도 질문이다. 무한 resume나 미세 sweep을 기본 권고하지 않는다.

## 2026-10-16 action=-.0003 fresh3K 학습·평가·보고서 완료 — HOLD

[원문·검토·계보](../experiments/h1/analysis/2026-10-16_H1_ACTION0003_MODEL2950_POLICY_REVIEW.md): Experiment `exp-h1-action-rate-relaxation`, 실제 OFFICIAL Run `20261016-033023-h1-actrate-0003-fresh3k`, **h1-submit-2 + action_rate_l2=-0.0003**, fresh/no parent·seed42/4096env·3000요청/console2999, COMPLETED/exit0/validation PASS. keeper **model_2950** SHA `1cc2c03197097c21c642e8373c760b25664b9c859ed75b5dc07582a770473c4b`의 PERSONAL 6영상·camera-off scenario7(128env×3seed×8case,3072행) 및 보고서 수신 완료. auto-best2900과 다르다. **HOLD**: 생존3072/3072에도 H5 진행 mean/P05/min **9.018/8.664/6.771m**, 국소 stall·계단 중앙 통과 공백이 남는다. 정지 body 누수 .382m/world 잔류 .455m. 공식 점수·제출·reward 개선 확정은 아니다. 기존 model2700/TERM50 model2800 저장 ZIP CPU 비교는 이번 보고서에서 미실행이며, 이전 angxy 5정책 비교와 다른 작업이다. -.0003 **resume** 제안은 별도 미실행 계획이다.

## 2026-10-16 angxy 분석·5정책 CPU 비교 완료 — 다음 제안 갱신

[원문·Run/SHA·15,360행 검산](../experiments/h1/analysis/2026-10-16_H1_ANGXY008_MODEL4650_POLICY_REVIEW.md): angxy=-.08 keeper4650(`c272b13b…`) **HOLD**. 무변경4699 대비 H5 평균 +.053m뿐이며 P05·H3 vy·H4 yaw·H6 자세 RMS는 악화해 범용 승격 근거 없음. 동일 평가 config/키≠동일 실제 지형·독립 학습 반복. [1차 연구 근거·다음 계획](../planning/2026-10-16_H1_EVIDENCE_AND_RESEARCH_NEXT_EXPERIMENTS.md)은 당시 **h1-submit-2 + action=-.0003 fresh3K**를 제안했으며 이후 위 실제 Run·평가·보고서 수신으로 갱신됐다. 중간값 성능 보장 없음; 기존 airtime resume는 PLANNED 유지. CPU 비교를 다시 대기라고 제안하지 않는다. R6 사용자 전달 공식 결과는 **56.35/70·86.35/100**이며 angxy 정책 점수가 아니다.

## 2026-10-16 lin=.55 4정책 코호트 비교 — HOLD 유지

[원문·Run/SHA·정량 결과](../experiments/h1/analysis/2026-10-16_H1_LIN055_FOUR_POLICY_COHORT_INTAKE.md). 부모2700/무변경4699/lin=.55 keeper4650/lin=.65 selected4650의 기존 평가를 CPU 비교했다. `.55`는 무변경보다 H5 진행 +1.322m지만 H3 vy·H4 yaw가 악화하고, `.65`보다 yaw는 좋으나 rough 꼬리와 H3 vy는 나쁘다. **범용 HOLD·PROMOTE 없음**. 동일 코호트 키는 독립 학습 반복·동일 실제 지형의 증명이 아니다. angxy=-.08은 위 후속 5정책 비교에 포함됐으며 분석 수신/HOLD다.

## 2026-10-15 lin=.55 학습·평가·보고서 수납 완료 — HOLD

[완료 기록·기존 제안의 시점 구분](../experiments/h1/analysis/2026-10-15_H1_NEXT_HYPOTHESIS_DECISION_INTAKE.md).

**lin=.55 후속 완료:** Run `20261015-105910-h1-actrate0001-lintrack-055-from2700-plus2k`는 OFFICIAL resume +2000, seed42/4096env, console4699/4700, COMPLETED/exit0/validation PASS다. 부모2700 SHA `e54d3389…93ca7ae`에서 lin .50→.55만 변경(action=-.0001, feet=.20, termination=-50 유지), 최종 preset-relative override는 `h1-submit-2 + lin=.55 + action=-.0001`다. 최신 indexed keeper `model_4650.pt` SHA `e8a358a50832f6653b1e558788a5a676ab9a849d3ec6c64e3ed2430e9ff41814`의 PERSONAL Windows 6영상·scenario7 평가도 COMPLETE(128env×3seed×8case,3072행)로 수납했다. console 종점4699와 keeper4650은 다르다. 원본 parent/source IDs=null·imported provenance=false는 유지하며 별도 SHA로 연결한다. **정책 분석 수납 완료·범용 후보 HOLD, 공식 점수·제출 아님**. [분석 원문·계보·한계](../experiments/h1/analysis/2026-10-15_H1_LINTRACK055_MODEL4650_POLICY_REVIEW.md). [학습 Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261015-exp-h1-action-first-planar-tracking-switch-lin055-resume2700-plus2k) · [평가 Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261015-exp-h1-action-first-planar-tracking-switch-lin055-model4650-video-eval). 당시 action=-.0003 제안 중 fresh는 이후 완료·보고서 HOLD이며, resume만 별도 미실행이다. Optuna v2의 objective/comparison 미승인·Tell 차단은 별개다.

## 2026-10-15 같은 부모 CPU 비교 완료 — 2700 HOLD / 4699 대표 후보 제외 / 복원4650 HOLD

[비교 보고서·계보·CSV 수납](../experiments/h1/analysis/2026-10-15_ACTRATE_PARENT_UNCHANGED_RESTORATION_COMPARISON_INTAKE.md): 부모2700, 무변경 +2K 4699, ACTION 복원4650(`a8249db4…`)의 기존 PERSONAL 평가 raw를 외부 에이전트가 CPU 비교했다. B4699는 A2700보다 rough 진행 **384/384건 감소**해 **이번 세 후보의 범용·전진/험지 대표 선정에서 REJECT**(학습 COMPLETED/PASS·원본 보존은 유지). A2700과 C4650은 **HOLD**, PROMOTE 없음. C는 B보다 진행373/384건 증가하나 tracking283/384건 악화·최악 진행4.845m다. 원문/CSV를 대조해 반영했으며 첨부 코드 실행·새 GPU 작업은 없다. 선택 checkpoint 차이와 imported-parent null/unverified는 유지하고 reward 인과·공식 점수로 환산하지 않는다.

## 2026-10-15 H1 정책 보고서 추가 — ACTION 복원 4650 · LINTRACK fresh 4950 (모두 HOLD)

[두 원문 수납·계보·판정 통합](../experiments/h1/analysis/2026-10-15_H1_MODEL4650_LINTRACK065_POLICY_REVIEW.md) · [최신 Experiment registry](../../../research/EXPERIMENTS.md). 기존 OFFICIAL 학습의 **PERSONAL Windows 6영상 + camera-off `scenario7`** 각 3,072 episode를 분석한 사용자 제공 MD 2건을 접수했다. 두 보고서의 수치를 Git 반영에서 ZIP/MP4를 재실행·재계산한 결과라고 쓰지 않는다.

- **Action-rate 복원 +2K `model_4650` / SHA `a8249d…25b84ea`**: 정지 body 누수 0.282m, 횡왕복 world 종료 순변위 0.167m. 하지만 **rough 전진 평균/P05/최소 8.769/7.970/4.845m, stall>0.05 7/384** → 전지형 **HOLD**. OFFICIAL resume Run `20261014-142200-h1-actrate-return2700-2k`과는 별도 checkpoint SHA/index로 연결하며 원 raw parent provenance는 null/unverified. 과거 10/11의 lin=.65 `model_4650` SHA `ce7ad586…`와 혼동 금지.
- **LINTRACK-065 fresh5K `model_4950` / SHA `b75289…ece`**: 정지 body 누수 0.063m, 전진 H2 15.088m이나 **횡왕복 world 종료 순변위 3.102m**, rough 평균/P05 8.995/8.411m → 전지형 **HOLD**. OFFICIAL fresh Run `20261014-081901-h1-lintrack-065-fresh5k`와는 별도 index/SHA 연결. `03_boxes.mp4`의 교대 검정 프레임은 캡처 결함이다.

같은 부모 **2700/4699/복원4650의 CPU 비교는 완료**됐다. 옛 lin=.65 resume4650(`ce7ad586…`) 대 4699도 위 후속 보고서에서 기존 CSV 수준으로 비교됐다. LINTRACK fresh5K vs TERM-50 저장 raw의 조건 점검은 별도다. **20초 생존=계단/박스 완주 아님**, PERSONAL 평가=공식 제출/점수 아님. 이 추가 기록은 새 학습·GPU 평가·Optuna trial 승인이 아니다.


> 현재 입구 기준: **2026-10-15**. 상세 수치·날짜별 업데이트는 이 문서에 중복 복사하지 않고 원래 Experiment/Run·평가·제출 기록으로 연결한다. [정리 전 상세 기록](_history/00_START_HERE_20261012_PRE_CLEANUP.md)은 검색·역사 보존용이며, **AI 업로드 핵심팩 21개에는 포함하지 않는다**.

## 현재 상태 — 서로 다른 판정을 분리

**무변경 +2K 대조군 현재 상태:** [ACTRATE continuation 기록](../../../research/experiments/h1/exp-h1-action-rate-relaxation.md), Run `20261014-111135-h1-actrate-0001-unchanged-cont2k`. OFFICIAL 학습 COMPLETED/exit0/PASS 및 원본 Release 게시, PERSONAL 영상·평가와 2700/복원4650 CPU 비교 완료. 현재 세 후보 중 **범용·전진/험지 대표에서만 REJECT**이며 별도 정지/yaw 참고군·증거는 유지한다. raw imported-checkpoint provenance=false/null은 외부 SHA 연결로 덮어쓰지 않는다.

| 항목 | 확인된 상태 | 정확한 근거 |
| --- | --- | --- |
| H1 ACTRATE-0001 두 fresh 조합 | `feet_air_time=0.25` 및 `feet_slide=-0.35` 각각 OFFICIAL fresh3K **COMPLETED / exit0 / PASS**. 각 `model_2950`의 Windows PERSONAL 6영상·full 평가도 COMPLETE. 학습 2개·평가 2개 Release 게시 및 원격 크기·SHA 확인 완료. **분석 원문 수신 완료, 채택 HOLD**이며 두 checkpoint는 서로 다르다. | [action+airtime](../../../research/experiments/h1/exp-h1-action-airtime-fresh-interaction.md) · [action+feet_slide](../../../research/experiments/h1/exp-h1-action-foot-contact-stability.md) |
| H1 `ACTRATE-0001` / `h1-submit-6` | **2026-10-11 실제 Round-6 제출 사용자 확인**. OFFICIAL fresh10K `20261011-041745-h1-actrate-0001-fresh10k-official` 완료/검증 PASS. 제출 policy actor는 indexed final keeper `model_9999.pt`와 일치. 사용자 전달 포털 시각 **2026-10-11 23:19**, 공식 점수 **56.35/70·86.35/100** 수신; 포털 원본·수령증 직접 확인은 아님. | [Registry](../../../research/EXPERIMENTS.md) · [제출 preset](../../../research/submission_presets/README.md) · [제출 manifest](../experiments/h1/2026-10-11_PRELIM_R6_SUBMISSION/submission_manifest.json) |
| H1 `model_9999` PERSONAL 검토 | Windows full 평가·영상·사용자 정책 분석은 수신. **행동 판단 HOLD**. 이는 사용자의 실제 제출을 취소하거나 공식 채점 결과를 의미하지 않는다. 자동 best `model_9900.pt`와 다른 정책. | [정책 검토](../experiments/h1/analysis/2026-10-11_ACTRATE0001_MODEL9999_POLICY_REVIEW.md) · [평가 게시 기록](../operations/windows_h1_video_evaluation/2026-10-11_ACTRATE0001_FRESH10K_MODEL9999_PUBLICATION.md) |
| H1 다른 후보 | `ACTRATE-001/model_2850`, `ANGTRACK-065/model_2950`, `ORIENT-100/model_2850`, `ACTRATE-0001/lin=0.65/model_4650`은 각각 별도 Run/checkpoint이며 기존 행동 판단은 개별 기록의 HOLD/조건부 판정을 유지. **같은 번호의 model_2850은 동일 정책이 아님**. | [H1 registry](../../../research/EXPERIMENTS.md) · [질문별 Experiment](../../../research/experiments/h1/) |
| Go2 `g2-submit-5 / LINTRACK-125` | 2026-10-06 실제 Round-5 제출 보고, 2026-10-08 수신 공식 점수 **88.32/100**. 제출 policy와 `model_7450.pt` actor 연결은 확인됨. 하지만 `g2-submit-5` 전체 `agent.yaml` 사본은 아직 동결되지 않아 미완성을 유지. | [Go2 공식 평가](../experiments/go2/analysis/2026-10-08_OFFICIAL_EVAL_GO2_ROUND5_LINTRACK125.md) · [제출 preset](../../../research/submission_presets/README.md) |

**상태 출처의 우선순위:** 현재 변경 상태는 [Experiment/Run registry](../../../research/EXPERIMENTS.md)와 [제출 snapshot](../../../research/submission_presets/README.md)을 보고, 원본 archive·resolved YAML·SHA·평가 산출물로 증명한다. 여기 적힌 상태는 독립적인 canonical 데이터베이스가 아니다.

**2026-10-14 분석 원문 수신:** 두 fresh 조합의 [보고서·학습 Run 연결](../experiments/h1/analysis/2026-10-14_ACTRATE0001_FRESH_COMBINATION_REPORT_INTAKE.md)을 보존했다. 제공된 단일 정책 보고서 모두 후보 **HOLD**이며 기존 ACTRATE-0001/model2700 원자료와 CPU 대응 비교를 먼저 제안한다. 이번 수납에서 영상·raw를 재분석하거나 reward 인과·공식 점수·채택을 확정하지 않았다. 기존 보고서에 Run ID가 비어 있으면 [확인된 정책↔학습 Run 표](../experiments/RECENT_POLICY_LINKS.md)를 함께 읽고, 원문 null과 외부 SHA 연결 근거를 구분한다.

## 자료를 찾는 순서

**2026-10-14 LINTRACK065 fresh5K 학습 완료:** [exp-h1-planar-tracking-weight](../../../research/experiments/h1/exp-h1-planar-tracking-weight.md), 실제 Run `20261014-081901-h1-lintrack-065-fresh5k`. OFFICIAL fresh/no parent, 5000회 요청·console4999/5000, seed42·4096env, exit0·COMPLETED/PASS. `h1-submit-2 + lin=0.65`이며 action=-0.0005·feet=0.20 유지. Originals 원본 Release 게시·원격 SHA 확인 완료. **행동 평가·채택 대기/HOLD**, 제출·공식 점수는 없음. model2700 부모/action=-0.0001의 model4650 resume와 별도 실행이다.

**2026-10-14 4정책 CPU 비교 수신:** [LINTRACK-065 비교 기록](../experiments/h1/analysis/2026-10-14_H1_4POLICY_LINTRACK065_COMPARISON_INTAKE.md). 부모2700→4650은 x/y 오차 개선 대신 회전·횡왕복 잔류·rough 평균/P05 진행에서 손해가 있어 HOLD 유지. 원 보고서 시점의 control 부재는 역사적 상태다. 이후 unchanged +2K 학습·평가 및 10/15 기존 CSV 교차 비교가 완료됐다. 새 lin=.65 fresh5K/action=-.0005 학습과 섞지 않는다. OFFICIAL 점수나 인과효과를 확정한 분석이 아니다.

| 질문 | 먼저 확인할 문서 |
| --- | --- |
| 프로젝트 전체 역할·데이터 출처 | [PROJECT_CONTEXT](../../../PROJECT_CONTEXT.md) · [데이터 구조](../../../docs/DATA_LAYOUT.md) |
| 제출 preset, Experiment 이름, Run·부모 계보 | [명명 규칙](../../../research/EXPERIMENT_NAMING.md) · [registry](../../../research/EXPERIMENTS.md) · [제출 설정](../../../research/submission_presets/README.md) |
| H1/Go2 reward와 코드 | [06 H1](06_HUMANOID_TRAINING_CODE.md) · [07 Go2](07_QUADRUPED_TRAINING_CODE.md) · [NVIDIA 현재 실행 source](https://github.com/SE3C/naver-issacsim-nvidia/blob/main/CURRENT_SOURCE.md) |
| OFFICIAL/PERSONAL 실행, checkpoint·archive 계보 | [11 서버 운영](11_SERVER_OPERATIONS.md) · [19 sidecar](19_ISSACSIMZ_EXTERNAL_EVIDENCE_CLI.md) · [16 export](16_EXPERIMENT_EXPORT_AND_TENSORBOARD.md) |
| 영상·사후 평가·부분 실패 | [17 영상](17_ISSACSIMZ_VIDEO_OPERATIONS.md) · [21 Windows Go2/H1 평가](21_WINDOWS_GO2_VIDEO_AND_EVALUATION.md) · [평가기 워크플로](https://github.com/SE3C/naver-issacsim-eval/blob/main/README.md) |
| 규정·제출 허용 범위 | [12 통합 규정](12_2026_UNIFIED_REGULATIONS.md), 필요하면 최신 공식 공지 확인 |
| 받은 분석보고서의 반영 관계 | [수신함 안내](../incoming/README.md) · [보조 관계 색인](../incoming/RELATIONSHIPS.md) (있으면 확인) |
| 학습 기록과 후속 분석을 따로 찾기 | [H1 목적별 색인](../experiments/h1/README.md) · [Go2 목적별 색인](../experiments/go2/README.md). NVIDIA 보조평가도 분석이며 서버/Windows는 출처 정보. |

## 반드시 지킬 해석 경계

- **새로 제공된 OFFICIAL 서버의 초기 reward는 운영진 baseline이지 제출 preset이 아니다.** `h1-submit-2` 등은 비교·목표 설정이다. bootstrap이나 checkpoint import가 그 preset을 적용했다고 가정하지 않는다. 실행 명령 전 실제 reward 전체를 읽고 목표 resolved config와의 모든 차이를 적용한다(`11`, `19`). 기존 서버 재접속·재부팅은 초기화가 아니며 이전 수정이 남을 수 있다.
- **PERSONAL 학습·영상·평가 / OFFICIAL 학습·evidence / 실제 제출 / 공식 채점**은 각각 다른 사실이다. 완료 여부·정책 행동 품질·제출 사실·점수를 서로 대체하지 않는다.
- Experiment는 비교 질문, Run은 개별 학습 실행. fresh/resume·부모 checkpoint SHA·seed·환경·평가 프로토콜을 확인한다. 기존 H/G/HS/GS/Rxx는 검색용 역사 주소이며 새 번호를 발급하지 않는다.
- `model_best.pt` 또는 `model_2850.pt` 등 이름만으로 source를 특정하지 않는다. 동일 정책 여부는 원본 index·checkpoint SHA·actor export 근거로만 판단한다.
- 영상은 장면을 실제로 확인했을 때만 정성 evidence로 설명한다. 20초 생존과 지형 완주·tracking·OFFICIAL score는 다르다. 사용자 제공 분석 수치는 원문·프로토콜을 함께 밝힌다.
- 현재 실행 코드는 해당 NVIDIA/PERSONAL checkout 또는 OFFICIAL `/workspace/training`을 확인한다. `data/processed/codebase/`와 server_backup은 보존된 분석용 source이지 항상 현재 실행 source는 아니다.
- OFFICIAL 서버에서는 GitHub 게시·업로드·서버 종료를 AI가 수행하지 않는다. PERSONAL 서버 종료는 명시 요청 때만. 새 학습·영상·GPU 평가와 게시·삭제는 작업 범위 밖에서 자동 실행하지 않는다.
- 과거 결론과 최신 상태가 어긋나면 해당 문서의 기록 시각·근거 출처를 구분한다. 원본·archive·받은 보고서는 소급 수정하지 않는다.

## 핵심팩 범위

`data/processed/ai_library/` **최상위 Markdown 21개** (`00`–`08`, `10`–`21`)가 AI 업로드 대상이다. `09`는 [reference](../reference/game_engine/09_GAME_AGENT_NAVIGATION_SENSORS.md)로 이동한 참고자료이고 `_history/`는 핵심팩에서 제외한다. 전체 업로드 지침은 [AI_LIBRARY_GUIDE](../../../docs/AI_LIBRARY_GUIDE.md)를 따른다.
