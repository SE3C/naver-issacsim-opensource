---
title: "학습·제출 실행 안내"
purpose: "AI upload bundle — 예선 작업 흐름과 제출 검증을 위한 분석 요약"
authority: "규정·마감·허용 여부는 12_2026_UNIFIED_REGULATIONS.md와 최신 공식 공지를 우선한다."
source_material:
  - "../naver-issacsim-originals/data/raw/server_backup/extracted/training/"
  - "data/processed/server_backup/code/training/PRELIM_RL_GUIDE.md.md"
  - "data/processed/server_backup/code/training/FINALS_GUIDE.md.md"
  - "data/processed/server_backup/code/training/README.md.md"
  - "data/processed/server_backup/code/training/upload_submission.py.md"
  - "data/processed/external_analysis/video_reports/05_preliminary_participation_r4Zq8wQdk1Y.md"
  - "data/processed/external_analysis/video_reports/07_compliance_and_prohibited_actions_VQE9DPn4KAg.md"
  - "data/processed/incoming/other/reviewed/GO2_A1_MODEL_4300_DEEP_ANALYSIS_20260915.md"
  - "data/processed/incoming/other/reviewed/GO2_A1_MODEL_4800_DEEP_ANALYSIS_20260915.md"
  - "data/processed/incoming/other/reviewed/GO2_A1_MODEL_4900_DEEP_ANALYSIS_20260915.md"
  - "data/processed/experiments/go2/analysis/2026-09-15_GO2_G-005_FIXED_EVAL_SEED4201_D1.md"
  - "data/processed/experiments/go2/analysis/2026-09-15_GO2_G-005_4800_4900_NATIVE_VIDEO_AND_SELECTION.md"
  - "data/processed/incoming/other/reviewed/A1_4800_vs_4900_DEEP_ANALYSIS_AND_LEARNING_RECORD_20260915.md"
  - "data/processed/incoming/other/reviewed/GO2_FINAL_TECHNICAL_REPORT_FLOW_DRAFT_20260915.md"
  - "data/processed/incoming/other/reviewed/SE3C_예선3라운드_Go2_평가_및_운영진답변_20260920.md"
  - "data/processed/incoming/other/reviewed/NCRC_WEBSITE_PUBLIC_ANALYSIS_2026-09-23.md"
  - "data/processed/incoming/other/reviewed/NCRC_R3_WEIGHT_SIMILARITY_DISCOVERY_2026-09-23.md"
  - "data/processed/experiments/h1/analysis/2026-09-30_OFFICIAL_EVAL_H1_ROUND4_AIRTIME025.md"
  - "data/processed/incoming/other/reviewed/H1_H005_OFFICIAL10K_VS_TERM50_OFFICIAL5K_DEEP_ANALYSIS_20260928.md"
  - "data/processed/incoming/other/reviewed/2026-10-02_SUBMISSION_REPORT_BASELINE_REFERENCE_ORGANIZER_REPLY.md"
---

# 학습·제출 실행 안내

## 이 문서의 역할

이 문서는 서버 백업에 있던 가이드·제출 코드에서 **현재 작업에 필요한 판단만** 추린 것이다. 현재 command·guide·submission source는 Originals의 2026-09-13 official snapshot `server_backup/extracted/training/`을 우선한다. `data/processed/server_backup/code/training/`은 과거 읽기용 추출본이다.

- 규정의 단일 기준: `12_2026_UNIFIED_REGULATIONS.md`
- 실제 명령·함수·파일 경로: `04_GUIDEBOOK_TRAINING_COMMANDS_APPENDIX.md`, `06_HUMANOID_TRAINING_CODE.md`, `07_QUADRUPED_TRAINING_CODE.md`
- 게임 단계의 세부 규칙·구조: `08_GAME_ENGINE_CORE.md`; 과거 game-agent·경로계획 참고 분석은 핵심팩 밖 `data/processed/reference/game_engine/09_GAME_AGENT_NAVIGATION_SENSORS.md`

## 예선의 핵심 작업

OT 운영 맥락과 가이드가 같은 루프다. 제한된 팀 서버 시간을 연구 예산처럼 쓴다.

1. H1 또는 Go2의 reward 파일에서 검증할 가설 하나를 정한다.
2. 한 번에 한 가지 변경만 적용하고 학습한다. 여러 값을 동시에 바꾸면 원인을 알 수 없다.
3. 학습 지표(`terrain level`, 속도 오차, 평균 보상)와 `play.py` 실제 보행을 함께 본다. 숫자가 좋아도 넘어짐·편향·명령 미추종이면 통과가 아니다.
4. 좋은 체크포인트를 제출 가능한 정책으로 내보내고 설정·리포트와 일치하는지 확인한다.
5. 제출 전 규정집과 최신 공지에서 로봇 선택, 형식, 마감, 수정 가능 시점을 확인한다.

실험 시작 전에 담당자·변경 파일·가설·예상 부작용·예상 시간을 적는다. 실패한 실험도 삭제하지 않고 실패 조건을 남긴다. 라운드 일정·UI 세부·지원 안내는 OT 당시 정보일 수 있으니 최신 공지로 재확인한다.

## 수정 범위와 검증 순서

| 구분 | 기본 판단 |
| --- | --- |
| H1 reward | `training/humanoid/humanoid_rewards.py`만 학생 변경 대상으로 본다. |
| Go2 reward | `training/quadruped/quadruped_rewards.py`만 학생 변경 대상으로 본다. |
| 학습 코드·환경 | 임의 변경하지 않는다. 규정상 허용 범위는 항상 최신 공지를 확인한다. |
| 반복 자동화 | 참가자가 직접 작성한 스크립트로 제공 환경의 정상 학습 절차를 반복하는 방식은 공식 안내 영상에서 허용 사례로 제시됐다. 새 에이전트·도구·외부 연결을 서버에 설치하는 것은 별개이며 금지선으로 본다. |
| 짧은 실험 | 가설을 빠르게 걸러내는 용도다. 긴 실행 전에 안정성·행동을 확인한다. |
| 최종 학습 | 후보를 충분히 검증한 뒤에만 서버 시간을 크게 쓴다. |

## 평가와 파일 흐름의 영상 교차검증

- 예선 참여 안내 영상은 H1·Go2를 각각 7개 격리 시나리오에서 평가하고, 한 시나리오의 성능을 참가자 관점에서 `생존율 × 추종 점수`로 설명한다. 이는 안정성과 명령 추종을 함께 봐야 한다는 진단 기준이며, 공개되지 않은 내부 채점 구현을 정확히 안다는 뜻은 아니다.
- 백업 코드와 안내 영상 모두 `train.py → model_best.pt + env.yaml`, `play.py → policy.pt + 확인 영상`의 흐름을 구분한다. 공식 사이트의 `.pt` 제출 칸에는 `model_best.pt`가 아니라 검증 후 export한 `policy.pt`를 올리는 것으로 안내된다.
- `report.html`, TensorBoard, 학습 로그는 진단 자료다. 영상에 나온 시간·threshold·점수는 데모이므로 현재 서버의 보장값이나 제출 합격선으로 사용하지 않는다.

## 제출 전 반드시 확인할 것

- `policy.pt`가 실제 제출 정책인지 확인한다. `model_best.pt`는 학습 체크포인트이며 자동으로 같은 의미가 되지 않는다.
- 충분히 긴 resume 제출 후보는 자동 `model_best.pt`가 아니라 final numbered checkpoint를 기본으로 한다. 마지막 수백 iteration에서 terrain·tracking·낙상이 함께 뚜렷하게 악화된 경우만 직전 checkpoint를 검토하고, final에서 native play/export를 한 번만 수행한다. PC tournament·여러 checkpoint selector는 만들지 않는다.
- `env.yaml`은 제출 정책을 만든 설정과 일치해야 한다.
- 기술 개선 리포트에는 변경한 reward, 변경 이유, 관찰된 결과를 서로 모순 없이 쓴다.
- `play.py` 결과로 넘어짐, 명령 미추종, 편향 회전, 지형 실패를 확인한다. 보상 숫자만으로 제출을 결정하지 않는다.
- 대시보드·공식 안내가 요구하는 업로드 흐름을 따른다. 서버 백업의 `upload_submission.py`는 참고 구현일 뿐, 현재의 공식 제출 절차를 대체하지 않는다.

### 2026-10-02 운영진 답변 — 기술 개선 리포트의 전→후 비교 기준

[수신한 운영진 답변](../incoming/other/reviewed/2026-10-02_SUBMISSION_REPORT_BASELINE_REFERENCE_ORGANIZER_REPLY.md)에 따르면 기술 개선 리포트의 설정 전→후 표기는 다음 두 기준을 모두 사용할 수 있다. 이 답변은 리포트 작성 기준에 대한 Q&A 보조 해석이며, 원 게시 화면·질문 원문·답변 시각은 이 저장소에서 독립 확인하지 못했다.

- **배포 시작값 기준:** 처음 배포받은 파일의 값 대비 전→후를 적는다. 이 방식은 계속 유효하다.
- **같은 로봇의 직전 라운드 제출 설정 기준:** 이전 제출 설정에서 이어서 변경했다면 첫 줄에 `기준: 4라운드 제출 설정(휴머노이드)`처럼 기준을 명시하고, 그 설정 대비 전→후를 적을 수 있다.
- **기준을 쓰지 않으면 배포 시작값 기준으로 평가된다.**
- 직전 라운드 기준에서 이번에 손대지 않은 항목은 개별로 적거나, 실제로 같은 로봇의 직전 제출과 동일할 때만 `나머지는 직전 제출 그대로`라고 쓸 수 있다.
- 어떤 기준을 택하든 **리포트의 최종값은 제출한 `env.yaml`과 같아야 한다.**
- 실험의 연구 기준 preset과 리포트의 비교 기준은 구분한다. 예를 들어 실제 실험이 오래된 frozen preset에서 출발했더라도 리포트에서 직전 라운드 제출을 비교 기준으로 선택하면, 직전 제출과 달라진 모든 최종 설정을 빠짐없이 전→후로 써야 한다.

## h1-submit-4 / AIRTIME-025 · OFFICIAL fresh 10K · 예선 4라운드 제출 및 공식 평가

`h1-submit-4 / AIRTIME-025` evidence Run `20260927-123428-h005-fresh10k-official`(legacy H-005 R05)은 공식 서버에서 `termination_penalty=-50`, `feet_air_time=0.25`로 이어학습 없이 10K를 완료했고 train evidence validation PASS와 [공식 raw-run Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20260927-airtime-025-fresh10k)가 확인됐다. 사용자는 2026-09-28 예선 4라운드 제출을 알렸고 [직접 작성한 기술 개선 리포트 원문](../experiments/h1/2026-09-28_H005_OFFICIAL_10K_technical_report.txt)을 보존했다. 수신한 제출 폴더의 `policy.pt`·`env.yaml`·`technical_report.txt`는 [별도 제출 Release](https://github.com/SE3C/naver-issacsim/releases/tag/submission-h1-prelim-r4-20260928)와 [manifest](../experiments/h1/2026-09-28_H005_PRELIM_R4_SUBMISSION/submission_manifest.json)에 보존했고 원격 5개 자산의 크기·digest가 일치한다. 이후 [예선 4라운드 공식 평가 기록](../experiments/h1/analysis/2026-09-30_OFFICIAL_EVAL_H1_ROUND4_AIRTIME025.md)을 수신해 시뮬레이션 `56.37/70`, 설계 의도 분석 `20/20`, 리포트 품질 `10/10`을 확인했고 구성 점수 합계는 `86.37/100`이다. 원본 제출 ZIP·포털 수령증·정확한 제출 시각은 아직 없으며, raw-run Release와 제출 snapshot은 다르다. `policy.pt`의 정확한 source numbered checkpoint도 train evidence만으로 독립 확인되지 않는다. [후속 비교 보고서](../incoming/other/reviewed/H1_H005_OFFICIAL10K_VS_TERM50_OFFICIAL5K_DEEP_ANALYSIS_20260928.md)는 같은 5K 단계의 `TERM-50` 대비 전체 우위가 명확하지 않음을 보고한다. 분석 원문의 이전 “미제출” 진술보다 이후 제출·공식 평가 기록을 최신 상태로 사용한다.

## g2-submit-5 / LINTRACK-125 · OFFICIAL fresh 7.5K · 예선 5라운드 제출

후속 [로컬·공식 불일치 대화 및 분석 방향](../experiments/go2/analysis/2026-10-08_GO2_LOCAL_OFFICIAL_EVALUATION_GAP_AND_ANALYSIS_POLICY.md)은 평가기를 유지하되 합산 점수의 단독 채택을 제한한다. [운영진 DM 답변](../experiments/go2/analysis/2026-10-08_GO2_R3_R5_OFFICIAL_SCORE_COMPONENTS_ORGANIZER_REPLY.md)으로 공식 감점 구성은 확인됐다: 계단 survival **99.0%→99.8%**의 약 **+0.07점** 이득보다 Tracking Score **0.819→0.796**의 약 **−0.24점** 손실이 컸다. 학습 contact 종료율과 공식 survival은 환산하지 않는다. 개선된 생존을 유지하며 명령 추종 손실을 회복하는 것이 후속 질문이고, 로컬·공식 역전 메커니즘·구체적 reward 변경·재학습은 아직 확정하지 않았다.

[2026-10-08 수신 공식 평가](../experiments/go2/analysis/2026-10-08_OFFICIAL_EVAL_GO2_ROUND5_LINTRACK125.md): **88.32/100 = 시뮬레이션 58.32/70 + 설계 의도 20/20 + 리포트 품질 10/10**. 표시 제출 시각은 **2026-10-06 01:10**(원문 시간대 미기재)이다. 시나리오 점수는 전진 **8.86/10.5**, 전방위 **8.70/10.5**, 거친 지형 **11.82/14**, 경사 **8.89/10.5**, 계단 **8.35/10.5**, 밀침 **5.83/7**, 도메인 랜덤화 **5.87/7**이다. 공식 AI 코멘트는 전 항목 보통 등급과 구체적 변경 목적·학습 결과 기록을 확인했다. 리포트·코멘트 전문은 평가 기록의 수신 원문 링크를 따른다.

Round-3 대비 종합은 **87.55→88.32(+0.77)**이지만 시뮬레이션은 **58.55→58.32(−0.23)**, 계단은 **8.52→8.35(−0.17)**다. 종합 상승은 구성 점수상 설계 의도 **19→20**과 함께 읽는다. PERSONAL evaluator의 계단 tracking error 개선을 공식 계단 점수 개선으로 바꾸지 않는다.

OFFICIAL Run `20260929-154342-go2-lintrack-125-fresh7500-official`은 fresh 7.5K, seed 42, 4096 env로 COMPLETE/PASS했고 terminal `model_7450.pt` SHA-256은 `b8766030e306dd72160d37292539575d5a1d92c2757f34637dafab3c1582343a`다. automatic training best `model_7050.pt`와 구분한다. 제출용 TorchScript `policy.pt`의 actor tensor 8개는 native 7450과 CPU exact-match했고, 제출 `env.yaml` SHA-256 `e7eeff96dcecd2248fe35071c38e69acf7cf403e06d976f94abafaf1e07847a9`는 OFFICIAL training-record extract와 일치한다.

사용자는 2026-10-06 실제 Round-5 portal 제출 완료를 보고했으므로 현재 submission preset 이름은 `g2-submit-5 / LINTRACK-125`다. [submission Release](https://github.com/SE3C/naver-issacsim/releases/tag/submission-go2-prelim-r5-20261006)는 `policy.pt`, `env.yaml`, 직접 작성한 `technical_report.txt`, manifest, SHA256SUMS 5개 asset을 보존하며 원격 digest와 processed/Originals snapshot identity가 맞는다. 기술 개선 리포트는 Round-3 `g2-submit-3` 기준 `track_lin_vel_xy_exp 1.5→1.25`, `lin_vel_z_l2 -2.0→-3.0`을 설명하고 7.5K 학습 지표와 별도 matched PERSONAL evaluator의 계단 개선을 근거로 든다. 이 PERSONAL 수치는 공식 채점 점수가 아니다.

2026-10-08 사용자 전달 공식 평가에서 제출 시각 2026-10-06 01:10(시간대 미기재), 종합 88.32/100(시뮬레이션 58.32/70·설계 의도 20/20·리포트 품질 10/10)을 수신했다. 별도 포털 receipt 파일은 미보유다. Release/intake manifest는 실제 제출 확인 직전에 만들어진 historical snapshot이라 `submission_preset=null` 문구를 사후 수정하지 않는다. 대신 registry와 현재 AI library에서 후속 확인 상태를 기록한다. `LINTRACK-125` reward 자체의 인과효과는 same-length BASE control이 없으므로 계속 HOLD다.

## 학습 산출물 intake·Release 완료 조건

학습 archive나 제출 산출물의 정리·보존과 Release 게시를 구분한다. raw evidence의 환경(PERSONAL/OFFICIAL)과 provenance를 확인하고 `research/EXPERIMENTS.md`와 해당 Experiment 상세 파일에 기록한다. Release 게시는 명시 요청이나 해당 작업에 유효한 게시 승인이 있을 때만 수행하며, 게시 후 원격 asset 크기·digest를 검증한다. 정리·보존만 요청했다고 외부 게시를 자동 추가하지 않는다. 새 이름은 [명명 규칙](../../../research/EXPERIMENT_NAMING.md)을 따른다. 기존 H/G 상세 파일·ID는 소급 rename하지 않는다.

학습 Run에는 Experiment 질문, 기준 submission preset과 최종 override, resolved config 출처, parent 또는 resume source checkpoint SHA, environment, requested iterations, 마지막 console iteration, 마지막 저장 checkpoint iteration, completed/interrupted/failed 상태, canonical evidence 경로, Release 링크와 결정을 남긴다. resume·다른 seed·다른 길이는 같은 질문의 별도 Run이며, 평가·영상·제출 export는 새 학습 Run이 아니다. identifiable official-server evidence가 확인된 Run만 `OFFICIAL`로 표시하며 중단·실패 run을 완료로 바꾸지 않는다.

실제 제출 후에만 새 `<robot>-submit-N`을 만든다. 현재 실제 제출 이름은 `h1-submit-2`, `h1-submit-4`, `h1-submit-6`, `g2-submit-3`, `g2-submit-5`다. `g2-submit-5`를 제외한 네 preset은 전체 native resolved `env.yaml`·`agent.yaml`을 [동결된 preset](../../../research/submission_presets/README.md)에 보존한다. `g2-submit-5`는 received env와 submission identity는 검증됐지만 loose folder에 `agent.yaml`이 없으므로 canonical OFFICIAL 7.5K archive에서 byte-for-byte 추출하기 전까지 full preset directory를 합성하지 않는다. 후보 설정은 이 파일을 고치지 않고 preset 기준 최종 override와 Run lineage로 기록한다. H1 4라운드 제출 `policy.pt`의 numbered checkpoint는 미확인으로 유지한다.

새 GitHub Release는 Release UI에서 새 tag를 만들지 않는다. 검증한 target commit에 로컬 annotated tag를 `git tag -a <tag> <commit> -m "<description>"`로 만들고 `git push origin <tag>`한 뒤, GitHub의 Release 작성 화면에서 그 기존 tag를 선택한다. 이는 오래된 target commit을 가리키는 Release가 lightweight tag/commit 시각에만 묶여 목록에서 혼동되는 것을 막기 위한 보존 규칙이다. 기존 Release/tag/asset은 목록 순서만을 이유로 삭제·재생성·retag하지 않는다. 전체 명명·분류·검증 절차는 `docs/RELEASE_TAXONOMY.md`를 따른다.

Go2 `g2-submit-3 / LINTRACK-150-LINZ-2` 계보(legacy G-005)의 4300·4800·4900 비교는 이 규칙의 사례다. 세 checkpoint의 paired
fixed evaluation은 단일 seed의 개인 L40S 보조 근거다. 그 결과 original 4800이 당시
안정성 우선 후보가 됐고 native play evidence도 4800 source SHA에 연결됐다. **이 개인 평가
자체는 공식 점수가 아니다.** 이후 matching policy/env를 묶은 별도 original-4800 제출
snapshot이 실제 3라운드 평가를 받았다. Recovery 4900은 recovery run에서 export된 `policy.pt` actor와
checkpoint exact-match가 확인된 progress-first 대안이다. `A1_MODEL_4800_SUBMISSION`처럼
파일명은 4800인데 policy와 smoke video가 recovery 4900인 bundle은 제출 금지다. 제출 묶음의
이름이 아니라 policy tensor/source checkpoint SHA, env lineage, evaluator/video 연결을 확인한다.

Go2 기술 개선 리포트의 보존된 초안은 서술 자료이지 실제 3라운드 제출본이나 새 성능 근거가 아니다. 초안 SHA는
`33f5706e…6152`이며 `[MODEL_XXXX]` placeholder와 작성 주석이 남아 있다. 실제 제출본은
별도 submission snapshot과 manifest로 확인한다. 리포트는 baseline 한계, legacy G-004 실패, `LINTRACK-150-LINZ-2` 조합 가설, official fresh interrupted와
recovery 완료, 개인 fixed evaluator의 보조 결과를 이 순서로 구분한다. 개인 evaluator의
timeout은 traversal 성공률이나 공식 점수로 쓰지 않는다. original 4800의 matching policy/env와
제출 provenance는 Run 07에서 확보되어 실제 Round-3 평가까지 받았다. 다음 제출 후보도 같은
연결을 새로 검증하고 native video evidence run의 source SHA를 함께 연결한다. 4900 선택 시 existing actor exact-match와 함께
hard-obstacle 낙상 열세 및 추가 seed 결과를 숨기지 않는다.

## Go2 예선 3라운드 평가에서 확인된 리포트 원칙

original 4800 matching policy/env 제출 snapshot은 실제 Round-3 평가에서 **87.55/100**
(시뮬레이션 58.55/70, 설계 의도 19/20, 리포트 품질 10/10)을 받았다. 이는 해당 제출
snapshot의 official 결과이지 개인 fixed evaluator·영상의 수치를 official 시나리오 점수로
변환하는 근거는 아니다.

운영진은 설계 의도 19/20의 정확한 단일 판정 지점은 AI 평가라 특정할 수 없으며, 아직 해소되지
않은 문제가 남으면 만점이 아닐 수 있다고 설명했다. 따라서 reward 원복·실패·잔여 접촉 또는
traversal 한계를 감추지 않는다. 변경 이유, 실제 설정, 전후 수치, 원복과 checkpoint 선택 근거를
서로 모순 없이 구체적으로 쓰는 현재 방식은 유지한다. 이번 리포트 품질은 10/10이었고, 운영진은
다음 라운드도 같은 기록 방식을 권고했다. 4라운드부터 만점이 아닌 이유를 평가문에 남기는 방향은
운영진의 향후 개선 계획이지 현재 보장된 규칙으로 표현하지 않는다.

### 2026-09-23 웹 평가 응답 분석에서 추가된 provenance 단서

보존한 분석 보고서에 따르면, 본인 팀의 R3 Go2 `/api/evaluation-report` 응답 `remark`는 제출 정책을 서버 학습 기록 `sub-5916`, iter 4900, run `2026-09-14_22-27-28`과 대조했다고 적는다. 백업된 `model_best`와 해시는 다르지만 **가중치 유사도 0.9952**를 근거로 같은 run의 다른 checkpoint로 판단했고 결과는 `정상 / ACTIVE`였다고 보고한다. 이는 **해당 제출 한 건의 사후 판정 단서**이지 모든 다른 checkpoint의 자동 허용이나 합격 threshold를 뜻하지 않는다. 응답 raw JSON 자체는 현재 보존된 공개 HTML/JSON 스냅샷에 없으므로 이 문단은 수신 분석 보고서의 기록으로 표시하며, 백엔드 수식·비교 tensor·임계값은 미확인이다.

후속 원문 분석과 실물 대조에서 `sub-5916`로 보고된 `submission_1789393113.zip`은 recovery run의 학습기록 백업임을 확인했다. ZIP은 `model_best.pt`·`env.yaml`·`report.html` **세 파일뿐**이며, 내부 `model_best.pt` SHA-256 `250e430c…514cd`는 기존 공식 recovery 4900 기록과 일치한다. 반면 Downloads의 실제 R3 제출 `policy.pt` SHA-256 `38723790…b254`는 기존 [제출 Release](https://github.com/SE3C/naver-issacsim/releases/tag/submission-go2-prelim-r3-20260915)의 원격 자산과 일치하며 original 4800 계열이다. 새 ZIP은 Originals의 같은 recovery Run에 Git LFS로 원문 보존했지만 **제출 ZIP이나 제출 policy로 바꾸지 않았다**. 이 두 파일을 새 `policy.pt`+`env.yaml` 제출 묶음으로 조합하지 않는다.

후속 보고서는 이 recovery `model_best`와 R3 제출 policy의 공통 actor MLP 286,604개 파라미터를 비교한 cosine `0.9952368736`이 `remark`의 네 자리 표시 `0.9952`와 맞는다고 기록한다. 이번 intake에서는 두 파일의 SHA-256 및 ZIP 구성과 원격 제출 asset은 직접 대조했지만, Torch 계산 자체와 인증 API raw 응답은 독립 재현·보존하지 못했다. 더구나 보고서의 weight-only cosine과 Pearson도 네 자리에서 `0.9952`여서 **정확한 백엔드 함수·threshold·fallback 순서는 여전히 미확인**이다. 이 값에 맞춰 제출 checkpoint를 고르거나 유사도만으로 공식 계보를 증명하지 않는다.

따라서 제출 전에는 기존대로 `policy.pt`의 source checkpoint, 공식 서버 run 계보, `env.yaml` 일치와 export 기록을 확보한다. `model_best.pt` 해시가 달라도 된다는 일반 규칙을 만들거나 유사도 판정에 의존해 출처 확인을 생략하지 않는다. 같은 보고서에서 확인한 Go2 7번째 프런트 시나리오 명칭은 `도메인 랜덤화`(7점)이며, 브라우저 JS는 시나리오 배점·서버 반환 점수를 **표시**할 뿐 실제 서버 채점식을 구현하지 않는다.

## H1·Go2 운영 판단

- H1과 Go2의 동작 특성·학습 시간·취약 시나리오는 다르다. 한 로봇에서 통했던 reward 변경을 다른 로봇에 그대로 이식하지 않는다.
- Go2가 더 느리게 학습되는 경우가 있어도, 단순 실행 시간만으로 정책 품질을 판단하지 않는다.
- 각 라운드의 제출 로봇과 점수 반영은 규정집을 따른다. OT·과거 가이드의 점수 예시를 현재 규정처럼 적용하지 않는다.

## 개인 Go2 결과의 사용 범위

2026-08-30 Brev Go2 결과의 “9.5k B0”는 내부 비교 기준이다. 공식 제출 정책·공식 점수 또는 “12k baseline 완주”로 표현하지 않는다. 실제 후보와 한계는 `07`을 따른다.

운영진의 2026-08-30 직접 답변에 따르면, 개인 검증에서는 learning rate·`desired_kl` 변경으로 장기 안정성을 진단할 수 있다. 그러나 **예선 제출 정책은 배포된 학습 설정 그대로** 학습하고, reward 설계와 iteration 수로 조절한다. 따라서 std clamp·learning-rate·RSL-RL 변경 진단은 기본 reward 비교와 별도 실험으로 기록하며 제출 후보와 섞지 않는다. 오류가 사라졌다는 이유만으로 최초 원인 해결·성능 개선·공식 환경 동일성을 인정하지 않는다.

안정화 reward도 임의로 한꺼번에 약화하지 않는다. 운영진은 `lin_vel_z_l2`와 `ang_vel_xy_l2`를 동시에 추천 범위 밖으로 낮추면 수직 진동·몸통 회전과 value-loss 발산 위험이 커질 수 있다고 안내했다. 관련 1차 답변의 전체 판단은 `data/processed/experiments/go2/2026-08-30_ORGANIZER_REPLY_GO2_DIVERGENCE.md`에 보존한다.

## 본선 연결점

본선은 예선에서 검증한 저수준 정책 위에 고수준 자연어 전략을 얹는 구조로 안내되어 있다. 정책의 안정성은 예선에서 확보하고, 목표 우선순위·경로·위험 회피 같은 전략 판단은 게임 단계 분석 문서를 따른다. 본선의 세부 규칙, 허용된 LLM 사용 방식, 프롬프트 제약은 반드시 공식 규정으로 확인한다.

## AI 응답 규칙

- 공식 학습·재생 명령을 작성할 때 `python3 train.py`·`python3 play.py`를 직접 제안하지 않는다. `issacsimz` bootstrap 뒤 mode-aware train/video wrapper를 사용하며, native child는 IsaacLab의 `isaaclab.sh -p` 경로를 유지한다.
- `issacsimz.pyz` 자체를 실행해야 할 때도 `python3`를 하드코딩하지 않는다. 저장소의 `./issacsimz` shell entrypoint 또는 bootstrap이 검증·저장한 `ISSACSIMZ_PYTHON_RUNNER`를 사용한다.
- 학습 artifact의 Release 요청에는 evidence 분류·원격 asset 검증·가설 registry와 상세 Run 갱신을 하나의 완료 조건으로 안내한다. provenance가 혼합되거나 모순되면 publish·registry 표기 전에 사용자 판단을 요청한다.

- 질문이 “어떤 파일을 바꾸나”이면 reward 파일과 가설 검증 절차를 먼저 안내한다.
- 질문이 “무엇을 제출해도 되나·언제 내나”이면 이 문서만으로 단정하지 않고 `12_2026_UNIFIED_REGULATIONS.md`와 최신 공지를 우선한다.
- 영상의 명령·UI·수치를 인용할 때는 `직접 확인된 튜토리얼 흐름`, `현재 규정과 일치`, `데모 예시`를 구분한다.
- 백업 코드의 URL·토큰·업로드 구현은 역사적 참고 자료이며, 실행하라고 제안하지 않는다.
