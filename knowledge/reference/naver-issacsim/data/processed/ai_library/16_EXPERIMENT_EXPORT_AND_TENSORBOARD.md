---
title: "실험 전체 export와 TensorBoard 복원 규칙"
purpose: "AI upload bundle — 서버 종료 전 증거 보존, headless 실행, 사후 시계열 분석 체크리스트"
sources:
  - "data/processed/experiments/h1/analysis/2026-10-11_ACTRATE0001_LINTRACK065_MODEL4650_POLICY_REVIEW.md"
  - "data/processed/incoming/other/reviewed/GO2_A1_1K_3K_VIDEO_FULL_EVIDENCE_ANALYSIS_20260914.md"
  - 'data/processed/incoming/other/reviewed/GO2_OFFICIAL_BASELINE_1K_AND_ISSACSIMZ_LOGGING_ANALYSIS_20260914.md'
  - "data/processed/planning/historical/06_H1_OFFICIAL_SERVER_BASELINE_DIAGNOSTIC.md"
  - "data/processed/experiments/h1/training/2026-08-24_OFFICIAL_SERVER_300ITER_BASELINE.md"
  - "data/processed/experiments/h1/analysis/2026-09-07_BREV_L40S_H1_BASELINE_5K_AND_SCREENING.md"
  - "data/processed/incoming/other/reviewed/GO2_A1_1K_DEEP_EVIDENCE_ANALYSIS_20260913.md"
  - "data/processed/incoming/other/reviewed/GO2_G5_OFFICIAL_1K_LIGHTWEIGHT_FAILURE_ANALYSIS_20260914.md"
  - "data/processed/incoming/other/reviewed/GO2_A1_THREE_EXPORTS_DEEP_ANALYSIS_20260914.md"
  - "data/processed/incoming/other/reviewed/GO2_A1_MODEL_4300_DEEP_ANALYSIS_20260915.md"
  - "data/processed/incoming/other/reviewed/GO2_A1_MODEL_4800_DEEP_ANALYSIS_20260915.md"
  - "data/processed/incoming/other/reviewed/GO2_A1_MODEL_4900_DEEP_ANALYSIS_20260915.md"
  - "data/processed/experiments/go2/analysis/2026-09-15_GO2_G-005_FIXED_EVAL_SEED4201_D1.md"
  - "data/processed/experiments/go2/analysis/2026-09-15_GO2_G-005_4800_4900_NATIVE_VIDEO_AND_SELECTION.md"
  - "data/processed/experiments/h1/analysis/2026-09-18_H-008_CONT2K_FROM_MODEL2998_ANALYSIS.md"
  - "data/processed/incoming/other/reviewed/H1_H009_HIPDEV030_FROM_H008_3K_DEEP_ANALYSIS_20260920.md"
  - "data/processed/incoming/other/reviewed/H1_H010_AIRTIME025_3K_TO_5K_DEEP_ANALYSIS_REVISED.md"
  - "data/processed/incoming/other/reviewed/H1_H011_HIPDEV010_MODEL4997_DEEP_ANALYSIS.md"
  - "data/processed/incoming/other/reviewed/A1_4800_vs_4900_DEEP_ANALYSIS_AND_LEARNING_RECORD_20260915.md"
  - "data/processed/incoming/other/reviewed/GO2_FINAL_TECHNICAL_REPORT_FLOW_DRAFT_20260915.md"
  - "https://isaac-sim.github.io/IsaacLab/main/source/tutorials/00_sim/launch_app.html"
  - "https://docs.isaacsim.omniverse.nvidia.com/latest/reference_material/sim_performance_optimization_handbook.html"
  - "data/processed/incoming/other/reviewed/H1_H010_FRESH3K_R01_VS_H005_FRESH3K_R01_DEEP_ANALYSIS_20260927.md"
  - "data/processed/incoming/other/reviewed/GO2_20260929-154342-go2-lintrack-125-fresh7500-official_VS_20260928-230114-go2-lintrack125-fresh3k-r5-official_DEEP_ANALYSIS_20260930.md"
type: "operations_checklist"
---

> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/ai_library/16_EXPERIMENT_EXPORT_AND_TENSORBOARD.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.


# 실험 전체 export와 TensorBoard 복원 규칙
> 날짜별 업데이트는 해당 시점의 기록이다. 최신 Run·제출 상태는 [현재 Experiment registry](<../../../../../../research/EXPERIMENTS.md>)를 우선한다.

## 2026-10-11 fresh10K 체크포인트 식별

[공식 intake](<../../../../../../reports/experiments/h1/training/2026-10-11_ACTRATE0001_OFFICIAL10K_EVIDENCE_INTAKE.md>) · [model_9999 정책 검토](<../../../../../../reports/experiments/h1/analysis/2026-10-11_ACTRATE0001_MODEL9999_POLICY_REVIEW.md>). Run `20261011-041745-h1-actrate-0001-fresh10k-official`의 keeper `model_9999.pt` SHA `a5020c273bc2b69bea1b20782fe80ba6605b3036b4054a7e5a8ab66151d2cb74`, origin=`organizer_keeper_backup`, source_path=`/workspace/training/humanoid/backup_log/2026-10-11_13-17-54/model_9999.pt`가 index와 평가 입력에 연결된다.

자동 best `model_9900.pt` SHA `6dd795e32383bc21ac487ea039bb2a03a565ec2ee6da893a3dc4ffaa844c769d`는 다른 정책이다. 최고보상 step9880도 checkpoint 번호9900과 구분한다. 이번 train wrapper에는 제출용 TorchScript `policy.pt`가 없으며 native model_best를 이름만 바꿔 제출하지 않는다. model9999 평가 ZIP이 있다는 사실은 공식 policy export가 존재한다는 증거가 아니다.



## 2026-10-11 단일 .pt resume 증거 연결 예시

OFFICIAL `20261010-154926-h1-actrate0001-lintrack065-from2700-plus2k`는 imported model2700에서 +2000 완료/PASS, console4699/4700, 최신 보존 model4650이며 best2900과 다르다. model4650 SHA를 후속 PERSONAL 평가 ZIP과 연결하되 원본 standalone-import `source_provenance_verified=false/source_run_mode=unknown/parent_run_id=null`은 그대로 둔다. 분석 원문의 “학습 계보 미확인”은 ZIP 단독 범위이고 별도 공식 archive 연결은 [계보·분석 기록](<../../../../../../reports/experiments/h1/analysis/2026-10-11_ACTRATE0001_LINTRACK065_MODEL4650_POLICY_REVIEW.md>)을 따른다. 학습·평가·보고서 수납 완료와 정책 HOLD를 구분한다.

## AI가 먼저 알려야 하는 것

사용자가 학습 실행·export·다운로드·서버 종료를 말하면 완성된 `policy.pt`만 받으라고 안내하지 않는다. 종료 전에는 **`logs/<run>/` 전체와 진단 증거를 원형 그대로 export하도록 알린다.** OFFICIAL 서버는 명시적 종료 요청을 받아도 AI가 종료하지 않으며 사용자 본인이 종료를 처리한다. PERSONAL 서버도 명시적 요청이 없으면 export 후 서버 상태를 바꾸지 않는다.

첫 H1 실행에서는 policy·checkpoint·env·report·ONNX·MP4는 보존했지만 tfevents·콘솔·GPU 시계열·코드 hash를 놓쳤다. 같은 누락을 반복하지 않는 것이 이 문서의 목적이다.

`ncrc-h1-train-logged`와 `ncrc-h1-release`는 이전 NVIDIA 내부 orchestration의 **historical** 기록이다. 현재 공개 `issacsimz` sidecar는 공통으로 console·명령·source hash·native run·실행 전후 GPU snapshot·tar+SHA-256을 evidence root에 남긴다. personal에서는 주기 GPU telemetry와 범용 checkpoint mirror도 유지한다. official에서는 상주 GPU sampler·범용 checkpoint watcher/mirror를 시작하지 않고 독립 `watch`도 거부하며, 종료 뒤 새 native run을 한 번 찾아 TensorBoard와 native 산출물을 수집한다. sidecar는 official에서 외부 업로드나 서버 삭제를 수행하지 않는다. 개인/공식 서버 모두 같은 portable `issacsimz.pyz`를 사용하되, 공식 제출·자동 backup은 원래 `train.py`/`_finalize.py` 흐름에 맡긴다.

현재 sidecar 기준은 `issacsimz` `bea81fa`이며, runtime 동작 변경은 `9f78009`, `bea81fa`는 그 선택적 preset-aware Release label을 README에 문서화한 후속 commit이다. 로컬 WSL 전체 테스트는 **129/129 PASS**이고 portable build·archive checksum도 PASS다. Windows 로컬에서는 129개 중 78개 실행 PASS·51개 skip였으며 한글 경로 Python runner 문제로 build를 끝내지 못했지만, 뒤이어 WSL에서 build를 확인했다. 이는 최신 sidecar의 실제 OFFICIAL 서버 학습·resume 또는 GitHub Release 게시를 직접 검증했다는 뜻은 아니다. 과거 `16e07f8`의 evidence-root 관련 52/52 PASS와 `c6bed9f`의 121/121·portable build PASS는 역사적 회귀 기록으로만 유지한다. PERSONAL·OFFICIAL profile train은 native `agent.save_interval=50`을 전달하고, OFFICIAL에서는 run별 organizer keep-all 절차로 checkpoint를 evidence/archive에 보존한다. PERSONAL 일반 train/video publisher도 checkout commit의 annotated tag를 먼저 push한다. 이전 `018330b`는 로컬 WSL 119/119 PASS, `77f6bb9`의 최종 Git ZIP 검사는 118/118 PASS였고 `py_compile`·portable build·archive SHA 검사도 PASS였다. 당시 확장자 없는 bash launcher가 ZIP에서 CRLF로 바뀌던 문제를 LF 속성 및 회귀 테스트로 막았다. 로컬 검사는 file/process/finalize/backup lifecycle, reward state, official video, publisher/tmux/runner 분리, archive 생성 뒤 evidence 불변, archive metadata sidecar handoff, validation FAIL loose artifact 차단, official user `--collect` 거부, checkpoint symlink·승인 root containment, task 전체 Python source fingerprint 등을 포함한다. personal bootstrap READY는 게시 없는 직접 CLI smoke를 안내하고 장기 실행은 state를 source하는 `issacsimz_tmux_train.sh`를 사용한다. 실제 train/play는 확인된 `isaaclab.sh -p`를 사용한다. child execution과 evidence validation은 별개이며, FAIL evidence/archive는 보존하되 제출형 loose handoff는 만들지 않는다. 공식 Go2 baseline 1K의 정상 경로는 과거 실제 evidence로 확인됐지만 최신 sidecar build의 실전 official 검증은 별도다.

## 2026-10-07 ORIENT-100 raw/evaluator provenance 점검 예시

`ORIENT-100`의 OFFICIAL fresh 3K Run은 `20261006-133517-h1-orient-100-fresh3k-official` (seed 42, 4,096 env, auto best `model_2850.pt`, latest preserved `model_2950.pt`)이고, 사후 Windows PERSONAL **별도** `model_2850` 통합 영상·camera-off `scenario7` full 평가(8 case × seed 4201/4202/4203 × env 128)는 checkpoint SHA `6aedeced60562c1d496d5319d29b76cf9e26ff43df06827cb370f24f5313f7b0`로 외부 연결한다. ZIP 내부의 `policy.source_run_id=null`을 training source 미존재로 오해하거나 임의 기입하지 않는다. [OFFICIAL intake](<../../../../../../reports/experiments/h1/training/2026-10-06_ORIENT100_OFFICIAL3K_EVIDENCE_INTAKE.md>), [PERSONAL 정책 분석](<../../../../../../reports/received/H1_ORIENT-100_POLICY_ANALYSIS_20261007.md>).

- **3,072/3,072 episode 20초 생존**과 `base_contact_failure=0`이 관찰돼도 정지 H1 **+1.633m**, lateral H3 **+1.180m** 비의도 body 전진, rough H5 최소 진행 **7.831m**를 함께 남긴다. `forward_progress_m`와 `integrated_body_forward_m`는 중복 집계하지 않는다; `lateral_drift_m`는 실제 횡변위가 아닌 `|Δvy|` 적분이다.
- 영상/평가는 서로 다른 command·terrain·episode이므로 MP4의 성공 장면을 3,072 episode의 계단 완주율로 바꾸지 않는다. `02_inverted_stairs.mp4`의 교대 검정 프레임은 녹화 문제로 따로 기록한다.
- 이 full 결과는 **PERSONAL 단일 정책 평가**이며 당시 A/B CLI comparison, Optuna trial, OFFICIAL 채점/제출이 아니었다. **2026-10-07 원문 당시에는** `h1-submit-2 / TERM-50` baseline을 같은 보고서에 제공받지 못했으나, **2026-10-10 기존 3개 ZIP 9,216 episode raw 대응-index 비교는 완료**됐다([후속 분석](<../../../../../../reports/experiments/h1/analysis/2026-10-10_H1_SCENARIO7_RAW_3POLICY_MATCHED_ANALYSIS.md>); [case JSON](<../../../../../../reports/experiments/h1/2026-10-10_H1_SCENARIO7_RAW_SUMMARY.json>), [delta JSON](<../../../../../../reports/experiments/h1/2026-10-10_H1_SCENARIO7_PAIRED_DELTAS.json>)). 학습 seed 반복·물리 terrain 동일성·reward 인과와 공식 점수는 여전히 HOLD이며 별도 Windows A/B CLI는 실행하지 않았다.

## 학습 종료 후 AI가 제안할 대조군

학습이 정상 종료되거나 중단되어 분석 가능한 evidence가 남으면, AI는 실행 상태를 확인한 뒤 **사용자에게 무엇과 비교하면 이번 결과를 가장 잘 해석할 수 있는지** 1순위와 필요할 때 2순위를 제안한다. 각 후보에는 비교할 Run/checkpoint, 답할 질문, 공통으로 맞춰야 할 조건, 이미 있는 원본·영상의 위치 또는 부족한 자료, 결과에 따른 다음 결정을 짧게 붙인다. 후보가 확인되지 않으면 임의의 Run을 지목하지 않고 필요한 대조 자료를 명시한다. 제안은 새 학습이나 평가의 실행 승인이 아니다.

- reward를 바꾼 **resume**은 같은 부모 checkpoint에서 reward를 유지하고 같은 추가 iteration을 진행한 continuation이 우선 대조군이다. 부모의 이전 endpoint만 비교하면 추가 학습 효과가 섞인다.
- reward를 바꾼 **fresh** Run은 같은 모드·source·학습량·평가 조건의 fresh 기준선이 우선이다. OFFICIAL과 PERSONAL을 섞어 reward의 인과 효과를 주장하지 않는다.
- **checkpoint/제출 정책 선택**은 후보들을 동일 evaluator에 놓고 terrain별 실제 진행·추종·낙상·최악 지형을 비교한다. 서로 다른 학습 이력의 정책 성능 비교와 reward 단일변수 검증은 다른 질문이다.
- 기존 Release의 통합 학습 archive와 checkpoint가 연결된 6지형 영상 묶음을 먼저 재사용한다. 영상은 행동 확인 자료이며 fixed evaluator와 command·난이도·curriculum이 다르면 정량평가로 대체하지 않는다. 영상·archive의 source checkpoint가 맞지 않으면 그 이유를 밝히고 행동 우열을 보류한다.

비교를 추천하기 전에 실제 부모·reward·mode·seed·num_envs·추가 iteration·source/PPO·terrain/evaluator 조건을 점검한다. 같은 seed만으로 같은 terrain 실현이나 대응 episode를 보장하지 않는다. 대조군 raw TensorBoard가 없으면 요약값 비교라고 표시하고 작은 차이로 우열을 확정하지 않는다. 기존 자료의 재분석으로 해결할 수 있는 질문을 먼저 제시하고, 새 GPU 작업이 필요한 경우에는 그 정보가 어떤 결정을 바꾸는지 설명한다. H1의 계보 정정과 현재 후보 우선순위는 `14`, Go2의 evaluator/Optuna 비교 경계는 `15`를 따른다.

## 결과 주장 등급

AI와 보고서는 다음 네 층을 섞지 않는다. (1) `execution=COMPLETED`는 native child가 끝난 사실, (2) `evidence_validation=PASS`는 기록·freshness·lineage 검사가 통과한 사실, (3) 고정 evaluator의 수치 비교는 그 evaluator 조건 안의 정량 근거, (4) native play video는 자세·접촉·stall·회복을 보는 정성 sanity check다. `OFFICIAL` 표시는 식별 가능한 공식 서버 evidence가 있는 Run에만 쓰며, 어느 층도 다른 층의 성공·대회 점수·일반화를 자동으로 뜻하지 않는다.

## 이번 공식 Go2 evidence의 검증 범위

수신 보고서 원문 SHA-256은 `922cff2377e85df65201fabee98d5867a3adb3bd7ea67b1b8bc7f675a6f61404`다. 문서 통합 시 canonical bundle SHA와 내부 train 33개·video 20개 manifest, console 0~999 전체, endpoint, best/800 checkpoint 동일 hash, video manifest 연결을 다시 확인했다. checkpoint tensor finite·GPU 집계·ffprobe·행동 관찰은 수신 보고서의 분석 결과로 구분한다.

보고서의 evidence 품질 95/100과 정확도 99%는 작성자의 자체 평가이며 검증된 확률·공식 인증·대회 점수로 인용하지 않는다. source before/after hash 일치는 해당 시점의 변경 감지 결과이며 실행 중 일시 변경까지 모두 배제하는 증거로 확대하지 않는다.

## OFFICIAL Go2 LINTRACK-125 3K↔7.5K — exact trajectory와 장기 불안정 해석

[심층 분석](<../../../../../../reports/received/GO2_20260929-154342-go2-lintrack-125-fresh7500-official_VS_20260928-230114-go2-lintrack125-fresh3k-r5-official_DEEP_ANALYSIS_20260930.md>)은 서로 별도 fresh 실행인 3K와 7.5K의 비교에서도 **동일 seed만 보고 동일 trajectory라고 가정하지 않고 실제 evidence로 확인**한 사례다. wall-time/Perf tag를 제외한 substantive TensorBoard scalar 22개가 iteration 0–2999에서 전 점 exact match했고, `model_0.pt`~`model_2950.pt`의 50-step checkpoint SHA가 60/60 동일했다. 실제 archive bytes로 다시 계산한 `model_2000.pt`와 `model_2950.pt`도 양쪽에서 일치했다. 이런 검증이 있을 때만 “첫 3K가 같은 trajectory”라고 쓴다.

반대로 exported `env.yaml` 파일 SHA가 다르다는 이유만으로 환경 차이를 선언하지 않는다. 이 쌍의 구조적 diff는 agent의 `max_iterations 3000→7500`과 run별 `log_dir`뿐이며 reward/source/PPO/env 실질 설정은 같다. 파일 hash 차이와 resolved config 차이를 구분한다.

장기 안정성은 endpoint reward 하나가 아니라 전체 시계열로 본다. 7.5K의 3000–7499 구간에서 value loss >100이 11회, max `273.12 @ 4711`까지 증가했지만 모든 scalar가 finite이고 NaN/Inf·terrain collapse가 없으며 후기 terrain/XY/contact가 회복했다. 따라서 **numerical collapse가 아니라 critic instability 증가 경고**로 기록한다. 추가 학습을 권하기 전에 실제 행동/evaluator 정보가 더 가치 있는지 판단한다.

checkpoint alias도 분리한다. 3K `model_best.pt=model_2000.pt`는 terminal `model_2950.pt`보다 reward peak에는 가깝지만 후기 terrain/XY 발전을 대표하지 못한다. 7.5K는 `model_best.pt=model_7050.pt`이고 terminal `model_7450.pt`와 다르다. 자동 best·last saved·실제 평가 후보를 각각 filename+SHA로 기록하고, “best”나 “final”이라는 짧은 이름만으로 정책을 선택하지 않는다.

[2026-10-05 후속 3정책 행동 분석](<../../../../../../reports/received/GO2_C4800_C7050_C7450_POLICY_COMPARISON_20261005.md>)은 PERSONAL raw `scenario7`에서 final `model_7450`까지 측정해 7050보다 9개 case 중 8개 tracking·8개 진행을 개선한 **현재 내부 행동 주후보 PROMOTE**로 판단했다. 동시에 stair-up base-contact 종료가 2→4회로 늘고 action/body RMS가 커져 automatic-best `model_7050`은 안전성 fallback HOLD다. 이 사례는 `model_best.pt`와 terminal numbered checkpoint의 의미를 분리해야 한다는 직접 근거다. Windows checkpoint metadata 연결이 있어도 evaluator task source는 OFFICIAL training source와 byte-identical하지 않으므로 공식 환경 재현·공식 점수로 쓰지 않는다. 상세 판정은 `07`·`21`을 따른다. 이후 terminal `model_7450.pt`는 `g2-submit-5 / LINTRACK-125`의 source checkpoint로 선택됐고, submitted TorchScript actor tensor 8개 exact-match와 env SHA 일치를 확인한 Round-5 snapshot Release가 보존됐다. 사용자는 2026-10-06 실제 제출 완료를 보고했지만 2026-10-08 사용자 전달 공식 평가에서 제출 시각 2026-10-06 01:10(시간대 미기재), 종합 88.32/100(시뮬레이션 58.32/70·설계 의도 20/20·리포트 품질 10/10)을 수신했다. 별도 포털 receipt 파일은 미보유다. automatic best 7050과 submitted terminal 7450의 구분을 계속 유지한다.

## 실행 전

- experiment ID, robot, 단일 가설
- 실제 실행 명령과 `train.py --help`
- Git commit·status·diff 또는 코드 SHA-256
- reward 변경 전·후 파일과 diff
- 시작 시각과 dashboard 남은 시간
- `nvidia-smi`, GPU·driver·VRAM
- Python·PyTorch·CUDA runtime
- headless·camera·viewport·video 조건

기존 `logs/`와 `exported/`가 있으면 먼저 보존한다. 새 실행을 위해 이전 결과를 삭제하거나 덮어쓰지 않는다.

## 실행 모드

화면이 필요 없는 학습·batch 평가·처리량 진단은 공식 스크립트가 지원하는 `--headless`를 기본으로 한다. GUI·viewport 렌더링을 줄이면 렌더 연산과 관련 RAM·VRAM 부담을 줄일 여지가 있다.

단, headless는 물리 상태·환경 tensor·terrain·policy·CUDA allocation을 제거하지 않는다. `--enable_cameras`를 쓰면 GUI 없이도 offscreen renderer가 작동해 GPU와 VRAM을 사용한다. 영상·이미지 센서가 필요 없는 학습에서는 camera를 켜지 않고, play 영상은 학습 처리량 측정 뒤 별도 실행한다.

자체 `SimulationApp` 도구는 headless에서도 기본 viewport overhead가 남을 수 있다. camera와 streaming이 모두 없을 때만 `disable_viewport_updates=True`를 검토하며 streaming에는 쓰지 않는다. 공식 서버에서는 최적화를 위해 제공 설정을 임의 수정하지 않고 지원 CLI만 사용한다.

## 실행 중

- stdout·stderr 전체를 `tee`로 저장
- exit code, 시작·종료 epoch와 ISO 시각
- personal에서는 1~2초 간격 GPU utilization·memory·power·temperature 시계열; official sidecar에서는 상주 sampler 없이 실행 전·후 snapshot만 수집
- NaN, CUDA OOM, simulator error, 반복 warning 시점
- 실제 run directory와 checkpoint 생성 여부

GUI/headless, camera/offscreen, viewport update, video recording 조건이 다른 실행의 seconds/iteration과 VRAM을 직접 비교하지 않는다.

## 종료 전 필수 export

1. `logs/<run>/` 전체
2. 모든 `events.out.tfevents*`
3. 전체 콘솔·오류·경고 로그
4. 모든 중간 `model_*.pt`와 `model_best.pt`
5. `env.yaml`, agent/PPO 설정, reward 파일 또는 hash
6. `policy.pt`, `policy.onnx`
7. `report.html`, play 영상, finalize/export 로그
8. 실행 전·후 GPU 기록과 personal의 실행 중 시계열(official sidecar의 주기 시계열은 없음)
9. 명령·help·코드 hash·시각·dashboard 사용시간

파일 몇 개를 골라 이름을 바꾸지 않는다. 원본 run 폴더의 구조와 파일명을 통째로 보존한다.

## Go2 사례의 보존·진단 보완

출처: `data/processed/experiments/go2/2026-08-30_GO2_BASELINE_CONVERSATION_SUMMARY.md`.

- **finalize/cleanup 전에** checkpoint를 별도 보존한다. 이 Go2 run에는 9500과 사전 분리한 best-through-5k가 남았고 정확한 9000은 없었다. 남은 파일의 전체 백업을 “모든 중간 모델 확보”로 표현하지 않는다.
- 별칭·실제 iteration·reward peak·선택 규칙·hash를 분리한다. 이 사례는 5k best → model_4500 / peak 4509, 9.5k → model_9500 / peak 9512였다.
- 최종 예외 이전 로그를 읽는다. 관찰 순서는 value loss 급증(9512) → reward/action-rate 극단값(9515) → 재발산 → inf/nan(9532~9535) → std 오류였다. 순서만으로 최초 trigger를 확정하지 않는다.
- 평균 std 외에 action 차원별 std와 actor/critic/optimizer tensor의 finite 여부를 확인한다. 정상 checkpoint가 이후 재개의 안정성을 보장하지는 않는다.
- 운영진은 장기 Go2 발산을 알려진 확률적 수치 불안정으로 설명했다. 그러므로 특정 iteration만으로 실패를 예측하지 말고, checkpoint 100회 간격 보존·value loss·reward term·action std·영상·terrain/fall 지표를 함께 export한다. 발산 시 report의 조언은 운영진이 수정 예정이라고 밝힌 항목이므로, 현재 report 문구만으로 원인이나 다음 reward를 확정하지 않는다.
- 나중에 만든 MP4는 먼저 만든 recovery archive에 자동 포함되지 않는다. archive·Release asset·로컬 파일의 포함 목록과 hash를 각각 확인한다.

원본 recovery 위치는 originals의 `data/raw/private_server_runs/go2/2026-08-30_brev_l40s_baseline_5k_9500iter/`다. 릴리스는 `SE3C/naver-issacsim-nvidia`의 `brev-go2-recovery-20260830_125132_KST`다. 이는 보존 위치이며 현재 서버 상태·추가 업로드 완료를 뜻하지 않는다.

공식 Go2 baseline 1K complete bundle은 Originals의 `official_server_runs/go2/2026-09-13_145026_baseline_1k/`에 바깥 archive 그대로 보존한다. 바깥 SHA-256은 `db659cdad4bf4a61de6c40c6185f80bb2465054e67abda91da4cfa8d0408a5bf`다. 내부 train/video archive sidecar와 합계 53개 `SHA256SUMS`가 일치하고 train validation PASS·checkpoint 11개·video parent/checkpoint 연결을 확인했지만, 이것은 evaluator 점수나 정책 채택 판정이 아니다.

공식 legacy `G-004 ANG-STAB` 1K train archive(아주 오래된 alias G5)는 Originals와 run별 Release에 byte-for-byte 보존됐다. archive
SHA-256 `1e162fdf640a715f19c564e21bff1011cd7ed91287db2f8d3586c3e0382d4359`, 내부 `SHA256SUMS`
33/33 일치, validation·finalize·official backup PASS, TensorBoard event 1개와 checkpoint 11개를
직접 확인했다. loose `env.yaml`·`model_best.pt`·`report.html`은 archive 내부 export와 각각
동일 hash다. 받은 MP4는 SHA-256 `35d7b9ebe128d23447d2b3e0b1737cf5d37a555a4995f4a36618b8c4e9eafe4b`,
H.264 1920×1080, 50 fps, 19.98초지만 별도 video evidence archive는 없다. terrain `0.00`, XY error
`1.7363`과 비정상 자세 영상은 정책을 strong negative로 만든다. evidence PASS는 “분석 가능한
실행이 보존됐다”는 뜻이지 “좋은 정책”이라는 뜻이 아니다.

Go2 `LINTRACK-150-LINZ-2` 3K 보고서(원문 파일의 legacy A1 표기)는 31개 checkpoint finite·std 양수와 archive 내부 53개 SHA 검증을 기록한다. 학습은 완료됐지만 value loss가 median `0.0265`에 비해 max `104.1677 @ 2912`까지 일시적으로 튀고 회복했다. “NaN이 없다”만으로 안정성을 확정하지 않고 p95/p99/max, 임계 초과 횟수, 연속 상승 여부, spike 뒤 reward·terrain 회복을 함께 기록한다. `model_best=model_2900`과 final `model_2999`를 둘 다 보존해 동일 평가에서 비교한다.

공식 `LINTRACK-150-LINZ-2` fresh attempt wrapper(legacy G-005 계보)는 SHA-256 `d2919617dbb2121652fb0c38fc12efe8d874280d55adf4416b39c7e5adfe30ef`로 보존한다. direct interrupted archive 내부 SHA 66/66이 맞고 console 0~약 4837, TensorBoard event, checkpoint 49개가 있다. metadata의 interrupted·exit 1·finalize not started·backup unknown·validation FAIL은 증거 손상이 아니라 실제 중단 상태다. 원본 `model_4800.pt` SHA-256은 `ea93f9b5b04d91a91d1cdb97c6d328978017991e0602745f9269c7190bfaba65`다.

공식 recovery final wrapper SHA-256은 `265c3c5533ac2be5037cab0ea668b07990ccc8025a816b22178b7df7bd7257c5`다. direct archive 내부 SHA 24/24, validation·finalize·backup PASS이고 console은 4999/5000까지 있다. mirror checkpoint는 4800·4900뿐이므로 `last logged iteration=4999`, `last saved checkpoint=4900`, `selected checkpoint=4900`, `best reward step=4872`를 분리한다. final handoff는 원본 4800 fallback, recovery 4900 `model_best`/`policy`, env/report/lineage와 6개 MP4를 보존하지만 개별 video manifest/archive는 없다.

영상 전 32MB wrapper는 final 79MB wrapper의 공통 5개 파일과 byte-identical한 의도적 stage snapshot이다. 둘을 별도 run으로 세지 않는다. 과거 파일명 `A1_MODEL_4800_SUBMISSION`은 원본 4800 model/env와 recovery 4900 policy/video를 섞었으므로 폐기됐고 제출 근거로 사용하지 않는다.

checkpoint 식별표는 별칭보다 SHA를 우선한다. Fresh 4300은 `82efb1a59bfad74c5b03b7584fe7cf27865dcd0603550f11340c4134c6a802c8`, original 4800은 `ea93f9b5b04d91a91d1cdb97c6d328978017991e0602745f9269c7190bfaba65`, recovery 4900/model_best는 `250e430cbb74f837af15384c145e865f7c8d8155fc65a7fe8b21dda1c27514cd`, recovery policy는 `22957506fefe1cde249548705fef30147fe149e1086c926ff447ff001c2cc277`다. recovery archive 안의 다시 저장된 `model_4800.pt`는 original 4800과 다른 파일이므로 이름만으로 source checkpoint를 고르지 않는다.

개인 L40S fixed-eval archive(과거 파일명 `A1_QUANT_EVAL_SEED4201_D1.tar.gz`) SHA-256은 `72c00b43345e9438647e30a6e01905391c3aea085b90042c75fdbbb5ad2695bd`다. archive의 세 checkpoint SHA가 위 canonical 값과 일치하고, 내부 export checksum 45/45, 18 CSV×64행, 18 JSON 집계가 검증됐다. 원본은 Originals의 `private_server_runs/go2/2026-09-15_a1_checkpoint_quant_eval_seed4201_d1/`에 둔다. 이 bundle의 checkpoint는 기존 공식 원본을 재포장한 비교 입력이므로 새 canonical checkpoint로 중복 등록하지 않으며, 평가 자체도 공식 서버 학습이나 공식 점수로 승격하지 않는다.

별도 native 비교 bundle(과거 파일명 `A1_4800_vs_4900_FINAL_BUNDLE_20260915.tar.gz`) SHA-256은 `424467b9c5b61666957ff22cc3395803f45d5c48bfc7797e3c85749a29902a7d`다. 4800/4900 × stairs/boxes/inverted-stairs의 6 evidence run은 validation 6/6과 최종 MP4 checksum 6/6을 통과했다. 각 run의 source checkpoint SHA와 영상 hash가 연결되므로 과거 recovery handoff의 loose 6-video 묶음과 구분한다. PyTorch `policy.pt`의 outer SHA가 run마다 달라도 ZIP 내부 tensor가 같고 serialization ID/generated-code metadata만 다른 경우가 있으므로, policy identity는 source checkpoint SHA·actor tensor·evidence lineage를 함께 사용한다.

최종 기술 개선 리포트 초안 원문은 SHA-256 `33f5706e6fbd5626560d45e3eaeea199a00c37009ff2f27365d8b8bf1bc66152`로 reviewed incoming에 보존한다. 원문 안의 placeholder·주석·표현 수정은 raw 파일을 덮어쓰지 않고 별도 최종본에서 한다. 최종본의 checkpoint 이름, policy SHA, env lineage, play 근거는 실제 제출 파일과 다시 대조한다.

이번 workspace에는 `LINTRACK-150-LINZ-2` 3K train/video archive가 없으므로 새 보고서의 SHA·TensorBoard exact-match·checkpoint finite·ffprobe 결과를 독립 재검산하지 못했다. 원문을 byte-for-byte 보존하고, 보고서 기반 사실과 workspace에서 직접 재검증한 공식 baseline bundle 사실을 구분한다.

## Corrected feet=+0.2 H1 PERSONAL evidence (2026-09-25)

The corrected `TERM-50` PERSONAL parent (legacy H-001 Run 05) is a fresh 1.5K run with `termination=-50`, `feet=+0.2`; its final `model_1499.pt` SHA is `5e3a31502d229884f91faf38962ffd32d63db69a64ca46ed7c1c404671b8ad82`. The unchanged 3K control and corrected `AIRTIME-025` / `AIRTIME-030` / `LINTRACK-100` / `LINTRACK-075` branches (legacy H-005/006/007/008) all resume this recorded parent. The branch train/video evidence is COMPLETE/PASS. Treat six-terrain clips as qualitative native-play checks only, not command-fixed paired evaluation or OFFICIAL scoring.

For representative policies use each branch's final numbered `model_2998.pt`, not a resume reward-best alias: corrected `AIRTIME-025`'s automatic best is `model_2900`, while corrected `LINTRACK-100`/`LINTRACK-075` automatic best maps to `model_1700`. The `AIRTIME-025`/`AIRTIME-030` report did not itself receive the parent archive and notes `source_provenance_verified=false` in child metadata; the separately preserved H-001 parent report/archive and matching recorded SHA supply additional lineage context, not a retroactive rewrite of the child validation field. [Parent source](<../../../../../../reports/received/H1_H001_R05_CORRECTED_PARENT_1P5K_DEEP_ANALYSIS_20260925.md>) · [H-005/006 source](<../../../../../../reports/received/H1_H005_VS_H006_DEEP_ANALYSIS_20260925.md>) · [H-007/008 source](<../../../../../../reports/received/H1_H-007_VS_H-008_DEEP_ANALYSIS_20260925.md>). Decisions and last-500 comparison: 14〔원본 참조: `14_H1_NEXT_RUN_PARAMETER_COMPARISON.md` / 공개 사본 미포함〕.

The next corrected 5K sibling set starts from `LINTRACK-075` final `model_2998.pt` (legacy H-008 Run 03) (recorded SHA `49fdb297…14983`): the unchanged control, `HIPDEV-030`, `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch, and `HIPDEV-010` branches. All four train/video comparisons report COMPLETE/PASS and a final `model_4997.pt` linked by SHA to the respective six-video suite. Final checkpoint SHA: control `4349fe56…3b5b6d`, `HIPDEV-030` `4c13ecd2…67c0`, `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch `fd497dcb…47e5df`, `HIPDEV-010` `9881687e…34fcf6`. Automatic best differs: control `model_4900`, `HIPDEV-030`/`HIPDEV-010` `model_4800`, `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch final `model_4997`. None has a joint late terrain/tracking/contact collapse warranting replacement of the final numbered representative. Videos lack matched numeric command/terrain seed/difficulty, so clip traversal is qualitative, not paired policy evaluation. H-011's train archive must be referenced through the corrected-source `source75123c7` Release, not the earlier incorrect-provenance Release. [H-009 report](<../../../../../../reports/received/H1_H009_R02_VS_H008_CORRECTED_CONTROL_DEEP_ANALYSIS_20260925.md>) · [H-010 report](<../../../../../../reports/received/H1_H010_R02_AIRTIME025_CORRECTED_VS_H008_CORRECTED_CONTROL_TO5K_DEEP_ANALYSIS_20260926.md>) · [H-011 report](<../../../../../../reports/received/H1_H011_R02_HIPDEV010_CORRECTED_VS_H008_CORRECTED_CONTROL_DEEP_ANALYSIS_20260926.md>).

## 2026-09-27 PERSONAL H1 fresh·continuation evidence

`AIRTIME-025` fresh, `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch fresh, corrected `AIRTIME-025`에서 이어진 unchanged continuation은 train exit 0·evidence PASS로 완료됐다. H-005 분석 원문은 세 archive의 raw TensorBoard와 18개 MP4·manifest를 대조했고, H-010 fresh 비교 원문은 두 fresh Run의 late-window training 지표와 영상 조건을 대조했다고 보고한다. `AIRTIME-025` fresh final은 `model_2999.pt`지만 영상은 자동 best `model_2750.pt`; `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch fresh final도 `model_2999.pt`지만 영상은 자동 best `model_2700.pt`; `AIRTIME-025` continuation final은 `model_4997.pt`지만 영상은 자동 best `model_4800.pt`다. 따라서 **이 세 final checkpoint의 행동은 해당 영상으로 확인되지 않았다.** corrected `AIRTIME-025` 영상만 final `model_2998.pt`에서 생성됐다. Run 04의 첫 시도는 손상된 staged checkpoint 로드에서 실패했고, 성공한 재시도의 parent `model_2998.pt` SHA는 기존 corrected Run 02 실제 checkpoint와 일치한다. 다만 metadata의 `source_provenance_verified=false`는 그대로 유지한다. resume 경계 global step `2998`은 두 event에 중복되며 curriculum/episode accumulator가 재시작되므로 초반 급변을 정책의 즉시 개선으로 읽지 않는다. `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch fresh는 `AIRTIME-025` fresh보다 late-500 XY error가 낮고 yaw error·training base-contact는 높아 전체 승자가 아니다. 14〔원본 참조: `14_H1_NEXT_RUN_PARAMETER_COMPARISON.md` / 공개 사본 미포함〕에 이 비교를 반영했지만 동일 command/terrain/seed의 고정 evaluator는 아직 없다. 정확한 Release는 [9/27 수신 기록](<../../../../../../reports/experiments/h1/training/2026-09-27_H1_FRESH_AND_CONTINUATION_EVIDENCE_INTAKE.md>)을 따른다.

## Historical feet=-0.2 H1 PERSONAL resume evidence (2026-09-17–21)

이 구간은 **corrected feet=+0.2 계보나 공식 `TERM-50`이 아닌 과거 개인 계보**다. H-005~008 Run 01은 공통 parent `model_1499.pt`(SHA-256 `68fa0a9fe5334f8a3ecea110c4ccc9adb81ec07ac50169eaf8009b1a6e88f0c1`)에서 1499→2998까지 1,500회를 resume했다. 네 archive에는 seed 42·4096 env·16 checkpoints·raw events·console·source hash와 PASS train/video evidence가 있으나 parent 파일 자체는 들어 있지 않다. 별도 보존 parent의 feet 값은 `-0.2`로 확인됐다. 이 계보의 숫자·영상은 공식 결과나 corrected 가설의 효과로 옮기지 않는다.

`model_best`는 제출 정책 선택이 아니다. H-005는 `model_2998`, H-006은 `model_2700`, H-007/008은 `model_1700`을 가리켰다. H-007/008의 raw 최고점(1564/1545)이 아닌 1700이 선택된 이유는 native finalizer의 resume warmup 필터다. final numbered `model_2998` 영상은 H-007/008 각각 6지형 정성 자료로 보존됐지만 단일 궤적은 낙상률·공식 점수 증거가 아니다. 당시 H-007/008은 feet와 track이 함께 바뀐 Run 01이므로 가설 판단도 HOLD/재실험 필요였다.

후속 H-008 unchanged 5K continuation은 `model_2998`에서 global 4997까지 갔지만 generic `issacsimz run`의 실행시점 profile·parent metadata가 없어 validation WARN이다. 사후 SHA 복원으로 WARN을 PASS로 바꾸지 않는다. H-009/010/011 Run 01은 이 5K 결과가 아니라 **이전 H-008 3K final `model_2998`**에서 분기한 형제 run이다. 세 run 모두 2998→4997, exit 0·validation PASS, 21 numbered checkpoints이며 대표는 final `model_4997`이다. H-009는 hip `-0.20→-0.30`, H-010은 feet `0.20→0.25`, H-011은 hip `-0.20→-0.10`만 바꿨다. 세 historical Run 01 가설은 unchanged control 대비 결정적 승리가 없어 HOLD다. 이는 corrected H-010 Run 02의 “고정 평가에만 PROMOTE”와 다르다. H-009의 기존 policy/ONNX/MP4는 fresh 산출물이 아니었다.

자동 best의 warmup 수식, raw 최고점과 report 최고점의 차이, 각 checkpoint 대응 및 late-window 수치는 18〔원본 참조: `18_H1_FINALIZE_REPORT_LIMITATIONS.md` / 공개 사본 미포함〕과 14〔원본 참조: `14_H1_NEXT_RUN_PARAMETER_COMPARISON.md` / 공개 사본 미포함〕에 모아둔다. 이 절은 원본 evidence의 범위·계보·한계만 요약한다.

## H1 2026-09-07에서 확인된 파일 연결 실패

- legacy `TERM50` 라벨의 MP4가 baseline 1K MP4와 SHA-256까지 동일했다. checkpoint는 서로 달랐으므로 영상 파일명만 믿고 정책 동작을 분석하면 안 된다.
- baseline의 `exported/model_best.pt`는 `model_1000.pt`와 같았지만 마지막 `policy.pt`와 MP4는 `model_4999.pt` 렌더 결과였다. staging checkpoint만 복원하면서 policy·video를 함께 복원하지 않은 결과로 볼 수 있다.
- 5K 요청의 마지막 loop와 checkpoint는 `4999/5000`, `model_4999.pt`였다. `h1_baseline_5000.pt` 같은 별칭은 실제 source iteration과 함께 기록한다.
- 실제 H1 MP4는 999 frames, 50fps, 약 19.98초였다. 설정의 6000 frames를 실제 생성 길이로 보고하지 않는다.

후속 `issacsimz video` evidence에는 source checkpoint 실제 iteration·hash, fresh official `exported/play_video.mp4` hash, 요청 frames와 가능한 경우 실제 duration을 남긴다. task tree의 stale `play_video.mp4`나 `policy.pt`를 삭제하지 않는다. 대신 실행 전후 provenance로 새롭거나 수정된 non-empty 공식 MP4만 성공으로 판정하며, `policy.pt` 존재는 video 성공 조건이 아니다.

## 권장 묶음

```text
experiment_id/
├─ command.txt
├─ train_help.txt
├─ train_console.log
├─ code_sha256.txt
├─ reward_diff.patch
├─ system/
│  ├─ runtime.txt
│  ├─ nvidia_smi_before.txt
│  ├─ nvidia_smi_during.csv  # personal only
│  └─ nvidia_smi_after.txt
├─ logs/<run>/
│  ├─ events.out.tfevents*
│  ├─ model_*.pt
│  └─ run 설정·메타데이터
├─ exported/
│  ├─ model_best.pt
│  ├─ env.yaml
│  ├─ policy.pt
│  ├─ policy.onnx
│  ├─ report.html
│  └─ play_video.mp4
└─ manifest_sha256.txt
```

manifest에는 상대경로, bytes, SHA-256을 기록한다. 외부 저장소 업로드 전 credential·token·개인정보를 검사한다.

`issacsimz` evidence에서는 source snapshot을 allowlist로 제한하고 `submit_config.txt`, `.env`, credential/secret/token 이름, private key를 broad collect에서 제외한다. `SUBMIT_HOST`·`SUBMIT_TOKEN`은 존재 여부만 metadata에 남기고 값을 저장하지 않는다. archive는 성공/실패/중단 suffix를 구분하고 `.sha256` 및 pack metadata sidecar를 함께 둔다. 같은 이름을 명시적 `--force` 없이 덮어쓰지 않는다.

milestone은 두 의미를 분리한다. `h1_milestone_5000.pt`는 5K 경계의 마지막 저장 checkpoint이고 zero-based 실행에서는 `model_4999.pt`일 수 있다. `h1_best_through_5000.pt`는 5K 이내 최고 training reward에 매핑된 checkpoint다. 둘을 모두 보존하되 evaluator 없이 “best policy”라고 부르지 않는다.

## tfevents로 복원할 수 있는 것

실제 event tag가 존재할 경우 다음 시계열을 iteration 0→마지막까지 추출할 수 있다.

- `Train/mean_reward`
- episode length
- terrain progression
- reward term별 값
- KL과 learning rate
- entropy·value·surrogate loss
- action std 등 logger가 기록한 scalar

먼저 tag 목록, 각 tag의 step 범위·point 수·누락률을 저장한다. 서로 비교할 때는 공통 tag와 공통 step만 사용한다. event에 없는 항목을 억지로 추정하지 않는다.

## 콘솔과 GPU 로그의 역할

콘솔 로그는 seconds/iteration, FPS, collection time, learning time, 경고·발산 시점을 확인한다. GPU 시계열은 utilization, VRAM, power와 병목을 확인한다. 처리량과 자원 지표는 정책 품질이 아니라 실행환경·성능 비교 근거다.

end-to-end 시간은 simulator 초기화·학습·checkpoint·finalize·export를 포함할 수 있다. 장기시간 계산에는 안정 구간 seconds/iteration의 중앙값과 별도 startup/finalize 시간을 사용한다.

## 다운로드 완료 판정

`ISSACSIMZ_DOWNLOAD/<RUN_ID>/` handoff는 탐색기용 최종 복사본일 뿐 원본 evidence/export를 대체하지 않는다. label 없는 video는 `play_video.mp4`, label video는 덮어쓰기 없는 `videos/<label>.mp4`다. **PERSONAL** H1/Go2 6-terrain 자동 suite가 모두 성공하면 네 공통 terrain과 profile별 고정 경사 두 파일이 한 폴더에 있다. Go2 경사 파일은 `slope_up_20deg`·`slope_down_20deg`, H1은 `slope_up_10deg`·`slope_down_10deg`다. 중간 실패 시 남은 실행을 시작하지 않으므로 완료로 해석하지 않는다. 형제 download bundle은 매 성공 video 뒤 현재 handoff 전체를 다시 감싸며 원래 폴더는 유지된다. **OFFICIAL에서도 6지형 영상 제작은 가능하다.** [17의 native `play.py` 수동 6회 절차](<17_ISSACSIMZ_VIDEO_OPERATIONS.md>)로 매 영상을 별도 복사하며 PERSONAL 자동 suite manifest·bundle이 생성된 것으로 간주하지 않는다. 서버 종료 판단은 계속 canonical archive와 원본 evidence를 기준으로 한다.

- run 폴더와 event가 로컬에서 열림
- console 시작·종료와 exit code가 있음
- 중간 checkpoint와 최종 산출물이 있음
- env·reward·code identity를 연결할 수 있음
- GPU 시계열과 dashboard 시간이 있음
- manifest hash가 실제 파일과 일치함
- `metadata.json`의 child 상태, native finalize, official backup, evidence validation을 각각 확인함
- archive `.sha256`과 내부 `SHA256SUMS`를 `issacsimz verify ... --require-sidecar`로 확인함
- 로컬 복사본을 확인함; OFFICIAL 서버는 AI가 종료하지 않고, PERSONAL 서버는 사용자의 명시 요청이 있을 때만 별도 종료함

누락이 발견되면 서버를 먼저 종료하지 말고 실제 경로와 logger 설정을 확인한다.
