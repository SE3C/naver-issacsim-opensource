# 00 시작 문서 정리 전 상세 기록 — 2026-10-12

이 문서는 시작 안내를 경량화하기 전의 상세 내용을 보존한 역사적 Markdown 사본입니다. 원문 Git blob SHA: `bd17b02090e2536a52b6ef4e250fdf0beb530c9a`. 원문 기준 Git revision: `517a310d39746a9ffb38d8d93c04c0cdf9453802`. 링크가 새 `_history/` 위치에서 동작하도록 상대경로만 한 단계 보정했습니다. **2026-10-11까지의 단락은 당시 상태**이며 2026-10-12 이후의 제출·판정은 [현재 registry](../../../../research/EXPERIMENTS.md)를 우선합니다.

---

---
bundle_title: "프로젝트 맥락과 AI 입력 안내"
source_documents: 21
purpose: AI upload bundle
---

## 2026-10-11 ACTRATE-0001 OFFICIAL fresh10K / model_9999 — 분석 반영, HOLD

Run `20261011-041745-h1-actrate-0001-fresh10k-official`은 fresh/no parent, seed42·4096env·10K, completed/exit0/validation PASS다. `h1-submit-2 + action=-0.0001`(feet=+0.20)의 별도 실행이며 기존 model_2700 3K·model_4650 resume와 구분한다. keeper final `model_9999.pt` SHA `a5020c273bc2b69bea1b20782fe80ba6605b3036b4054a7e5a8ab66151d2cb74`가 공식 index와 PERSONAL 평가 입력에서 일치한다. 자동 best model_9900과 같은 정책이 아니다.

[model_9999 정책 검토](../../experiments/h1/2026-10-11_ACTRATE0001_MODEL9999_POLICY_REVIEW.md) · [학습 근거](../../experiments/h1/2026-10-11_ACTRATE0001_OFFICIAL10K_EVIDENCE_INTAKE.md) · [ZIP 게시 기록](../../operations/windows_h1_video_evaluation/2026-10-11_ACTRATE0001_FRESH10K_MODEL9999_PUBLICATION.md). 보고서는 6영상과 full 평가를 분석했다. 3,072/3,072 timeout 생존이지만 rough 하위 진행 꼬리와 연속 계단 완주 검증 공백으로 **HOLD**다. 실제 제출·공식 점수·새 preset은 아직 기록하지 않는다.


## 2026-10-11 ACTRATE-001 / model_2850 (SHA `1e6d…bb1`) PERSONAL 행동 분석 — HOLD

**체크포인트 역할:** 분석·평가한 auto-best `model_2850`과 마지막 keeper `model_2950`은 다른 정책이다. `model_2950` SHA `8914b6b48e74a6463808f629648f87900efdb853e5253e142e99c738adb2d085`의 행동 품질을 이 보고서로 대신 판정하지 않는다.

[원문 보존](../../incoming/other/reviewed/H1_MODEL2850_SHA1E6D_POLICY_ANALYSIS_20261010.md) · [근거·결정 기록](../../experiments/h1/2026-10-11_ACTRATE001_MODEL2850_POLICY_REVIEW.md) · [OFFICIAL 학습 Experiment](../../../../research/experiments/h1/exp-h1-action-rate-smoothing.md). 기존 OFFICIAL fresh3K `ACTRATE-001` Run `20261010-125324-h1-actrate-001-fresh3k`의 auto-best `model_2850.pt` **SHA-256 `1e6d0950f5bd981ca1f88044e65ae7ee57505c47b92b5caad8c39263f4d93bb1`**가 Windows PERSONAL 6영상/`scenario7` 평가의 체크포인트 SHA와 일치한다. ZIP 내부 `source_run_id=null`은 그대로 두고 별도 기존 학습 증거로 계보를 연결한다. **같은 파일명인 `ORIENT-100/model_2850` (SHA `6aed…f7b0`)와 다른 정책**이다.

제공된 심층 보고서의 정량 결과: **3,072/3,072개 20초 timeout 생존**, H2 전진 body 적분 **15.470m**(목표 15m), H7 push 전진 **10.656m**(목표 10m), H6 경사 상·하 body 적분 **20.297/20.058m**. 다만 **H1 정지 명령에도 비의도 body 전진 1.164m / world XY 순변위 평균 1.151m**, **H3 횡왕복 비의도 전진 1.109m / world XY 순변위 평균 2.177m**가 남는다. H5 rough 진행 평균/P05/최소는 **9.359/8.921/8.372m**, 추종 평균/P95는 **0.17111/0.18947**이고 stall>0.05는 0/384이다. 6개 영상의 초기 boxes/rough 접지는 정성 근거이나 **계단 중앙 다단 통과와 boxes 정량 성공은 입증되지 않는다**. 영상과 camera-off 평가의 지형·명령 trajectory는 별개다.

**판정: 전진 중심 내부 보행 후보 HOLD, 범용 대표 정책 PROMOTE 보류.** 분석 보고서 수납은 새로운 학습·GPU 평가·영상 재실행·Optuna trial·OFFICIAL 점수가 아니다. 우선 이미 보존된 `h1-submit-2 / TERM-50 model_2800` 평가 원자료와 protocol/source/PPO/command/terrain/seed/horizon parity를 검토해 대응 가능한 초기 cohort만 비교한다. 이번 GitHub 반영에서 평가 ZIP/MP4를 직접 재계산하지 않았으며 행동 수치는 제공 보고서의 기록이다.

## 2026-10-11 ACTRATE-0001 → lin=0.65 / model_4650 — 학습·평가 완료, 분석 HOLD

`exp-h1-action-first-planar-tracking-switch` Run `20261010-154926-h1-actrate0001-lintrack065-from2700-plus2k`는 **OFFICIAL +2000 resume COMPLETED/PASS**(부모 model2700, console4699/4700). 최신 keeper/evaluated model4650 SHA `ce7ad58657f3dd744e7cf2b7531f3d7d455773dfc6fb135f39d8a55aa49dea70`는 automatic best2900과 다르다. `h1-submit-2 + lin=0.65 + action=-0.0001`. 원본 standalone-import provenance=false/unknown/null은 유지하고 기존 부모 Run과 SHA로 외부 연결했다.

PERSONAL full **3,072/3,072 20초 생존**; H2/H7 body 진행 **14.812/9.757m**, H1 world XY 순변위 **0.228m**, H3 횡왕복 잔류 **2.398m**, H4 yaw 오차 **.179rad/s**, H5 mean/P05/min 진행 **9.546/9.228/8.974m**. **분석 수납 완료/HOLD**: 실제 전진 후보지만 횡복귀·회전 비용과 계단 중앙 완주 미확인으로 범용 대표 승격 보류. model2700 과거 요약치와의 대조는 matched A/B·reward 인과·공식 점수가 아니다. [원문](../../incoming/other/reviewed/H1_MODEL4650_POLICY_ANALYSIS_20261011.md) · [계보·판정](../../experiments/h1/2026-10-11_ACTRATE0001_LINTRACK065_MODEL4650_POLICY_REVIEW.md) · [Release](../../operations/windows_h1_video_evaluation/2026-10-11_ACTRATE0001_LINTRACK065_MODEL4650_PUBLICATION.md).

## 2026-10-10 selected ACTRATE-0001 H1 hypotheses — 현재 한 완료·네 PLANNED

[Canonical plan for five hypotheses](../../planning/2026-10-10_H1_ACTRATE0001_FIVE_COMBINATION_HYPOTHESES.md) · [Registry](../../../../research/EXPERIMENTS.md). **Fresh 2:** `h1-submit-2 + feet=0.25 + action=-0.0001`, `h1-submit-2 + action=-0.0001 + feet_slide=-0.35` (each 0→3K with two baseline-relative reward changes). **Resume 3:** from the same OFFICIAL ACTRATE-0001 fresh3K parent `20261009-142350-h1-actrate-0001-fresh3k`, independently +2K with one extra delta: `feet=0.25`, `lin=0.65`, or `angxy=-0.08` while keeping `action=-0.0001`.

**One resume step per child branch, not one Resume Run total:** multiple sibling Resume Runs allowed; no 5K→7K repeat from a child. Check actual `model_2700` vs `model_2950` behavior/late trend, official index/`source_path`/SHA before selecting their shared checkpoint parent. Fresh AIRTIME+ACTRATE and resume AIRTIME-after-ACTRATE share final reward, not duration (3K versus total approximately 5K) or lineage, so no schedule causal claim. For newly altered `feet_slide`, keep full native field name; do not invent a short reward descriptor, Experiment legacy H/HS number, or Run ID. **lin=0.65 Resume는 위 완료/HOLD 기록, 나머지 네 갈래만 PLANNED**다. 별도 ACTRATE-001도 독립된 fresh3K 완료 기록이 있다. 제출·공식점수·Optuna 결과는 이 기록으로 생성되지 않는다.


## 2026-10-10 ANGTRACK-065 ↔ TERM-50 기존 평가 RAW 대조 완료 — 최신 판단

[원본 3,072 대응 cohort 심층 보고서](../../experiments/h1/2026-10-10_H1_ANGTRACK065_TERM50_DEEP_RAW_COMPARISON.md). 기존 `ANGTRACK-065/model_2950`과 `TERM-50/model_2800` 평가 ZIP의 SHA·무결성, `resolved_configs.json` 바이트·프로토콜·source/agent/applied-env fingerprint, 최초 `(scenario,case,seed,env_id)` 3,072개 대응을 직접 검증했다. ANG `episodes.jsonl` **3,087행은 3,072개 최초 시도와 H3 종료 뒤 재시작 15행**으로 나눠 집계했다. 같은 key가 물리 초기 지형·상태의 완전 동일성을 뜻하지 않는다.

**핵심:** H3 횡이동 첫 접촉 종료 TERM **0/384** vs ANG **15/384**; `vy_error` **0.06848 vs 0.18601**, stall **0.00912 vs 0.34339**(대응 인덱스 **384/384** ANG 열세). 생존 369개만 봐도 횡제어 악화. H4 yaw error TERM **0.11934 vs ANG 0.07704**(384/384 ANG 우세), H1 정지 비의도 body 전진 **1.3523 vs 0.8751m**로 ANG 이점. 전체 혼합 tracking TERM **0.157118 vs ANG 0.130669**이지만 XY RMSE **0.112589 vs 0.125612**로 ANG 악화. H5 rough 평균 진행 **8.8961 vs 8.8949m** 거의 동일. **ANGTRACK-065 대표 정책 HOLD, ACTRATE-001 학습·PERSONAL 분석 완료/HOLD**. 기존 단독 보고서의 ‘TERM 대조 미실행’은 후속 분석 전 역사적 상태. GPU/공식 평가·Optuna 실행 없음.

## 2026-10-10 ANGTRACK-065 / model_2950 PERSONAL 행동 분석 수신 — HOLD

[원본 심층 분석](../../incoming/other/reviewed/H1_ANGTRACK-065_POLICY_ANALYSIS_20261010.md) · [AI 라이브러리 근거·판정](../../experiments/h1/2026-10-10_ANGTRACK065_MODEL2950_POLICY_REVIEW.md) · [OFFICIAL Run](../../../../research/experiments/h1/exp-h1-angular-tracking-boost.md). 기존 OFFICIAL fresh3K `ANGTRACK-065` Run `20261009-155344-h1-angtrack-065-fresh3k` exit0/PASS의 best=keeper `model_2950.pt` SHA `6a6f456e…68e118c`에 연결된 후속 Windows **PERSONAL** 6영상+`scenario7` 평가 보고서를 수신했다. **3,072 최초 cohort지만 `episodes.jsonl`은 3,087행**: H3 순수 횡이동 **15/384 최초 cohort(3.91%) base-contact 종료**, 각 1개 reset 후 `evaluation_end` 행이 추가됐다. H3 최초 20초 timeout은 **369/384=96.09%**이며 399행 기준 생존 96.24%는 20초 완주율이 아니다. H3 tracking 0.2203, stall 0.3532, vy error 0.1871m/s, H1 정지 비의도 body 전진 0.875m. H2/H4/H5/H6/H7 전진·회전·험지·경사·외란에는 유용한 이동 관찰, 다단 계단 완주는 미검증. 하행 경사 영상의 짝수 500 검정 프레임은 캡처 artifact다.

**전방위 대표 정책 HOLD.** 이는 ANGTRACK 단일 정책 평가 보고서 수납이며 `TERM-50` 등의 기존 9,216행 **3정책 raw 대응 비교에 ANGTRACK가 포함된 것은 아니다**. `TERM-50/model_2800`을 후속 비교 1순위로 기록하지만 별도 ANGTRACK matched A/B·reward 인과·OFFICIAL 점수는 아직 미검증. `ACTRATE-001`은 OFFICIAL fresh3K 완료/PASS·PERSONAL 분석 수납/HOLD.

## 2026-10-10 H1 3개 평가 ZIP 원본 9,216 episode 직접 비교 — 최신 판정

[후속 **원자료 직접 비교 보고서**](../../experiments/h1/2026-10-10_H1_SCENARIO7_RAW_3POLICY_MATCHED_ANALYSIS.md). 이전에는 GitHub ZIP의 위치·메타데이터만 확인했지만, **사용자에게 ZIP 3개를 받아 직접 로드·재집계**했다. ZIP SHA·CRC PASS, 각 3,072 episode×3=9,216, 3,072 대응 cohort 중복 없이 일치; `resolved_configs.json` 바이트 동일, protocol/agent/source/applied-env fingerprint 동일. 과거 “TERM-50 raw 미확인”은 현재 유효하지 않다.

- **TERM-50/model_2800:** 전체 tracking `0.15712`; H1 정지 중 전진 `1.352m`(셋 중 가장 적음); H5 rough 평균/P05/최소 전진 `8.896/8.533/2.639m`, 최악 stall `0.611`(새로 확인). **ORIENT-100/model_2850:** tracking `0.14041`(TERM보다 10.63% 낮음)·H5 평균 `9.451m`, H1 비의도 전진 `1.633m`. 그러나 roll/pitch RMS `0.08015`는 TERM `0.03381` 및 ACTRATE `0.03019`보다 상당히 커서 “가장 안정적”으로 결론내지 않는다. **ACTRATE-0001/model_2700:** tracking `0.14534`(TERM보다 7.50% 낮음), H5 평균/P05/최소 `9.948/9.592/8.815m`, H1 비의도 전진 `1.987m` 및 action Δ RMS `0.45687`로 비용이 큼.
- **현재 판정:** 정지 제어 축 TERM, 평균 혼합 tracking 축 ORIENT, 험지 진행 축 ACTRATE가 각기 유리. 모두 **전지형 대표 정책 HOLD**. 보존된 평가기 설정과 cohort ID는 대응되지만 물리 지형·초기상태의 정책 간 완전 동일성, training source/PPO 단일변수 인과·독립 학습 seed 반복, 다단 계단 완주는 아직 미검증. ANGTRACK-065 PERSONAL 고정평가 및 단일 정책 행동 분석 수신/HOLD, ACTRATE-001은 OFFICIAL 학습·PERSONAL 분석 완료/HOLD. 새 GPU 실행/원본 변경 없음.

## 2026-10-10 H1 고정 `scenario7` 3정책 보고서 비교 · TERM-50 원본 위치 확인

[GitHub 원본 위치·프로토콜·case별 비교·접근 한계 통합 기록](../../experiments/h1/2026-10-10_H1_SCENARIO7_CROSS_POLICY_REPORT_LEVEL_COMPARISON.md). OFFICIAL fresh3K `TERM-50/model_2800`, `ORIENT-100/model_2850`, `ACTRATE-0001/model_2700`의 **PERSONAL 평가 ZIP 3개**를 Originals manifest와 NVIDIA Release에서 모두 찾았다. evaluator checkout `ef10b7a`, handoff `28895d7`, protocol `d406a296…7062d34`, seed 4201–4203, 128 env, 8 case, 20초가 기록상 일치한다. 단, Release 바이너리 ZIP은 연결된 GitHub 읽기 기능으로 추출할 수 없어 **3개 `episodes.jsonl`을 직접 읽거나 cohort A/B를 재집계하지 않았다**. 저장소 ZIP Git 경로는 LFS pointer(TERM-50은 133 bytes)이며 34MB ZIP 본문이 아니다.

기존 세 단일정책 원문 보고서의 **정량표를 대조**하면 ORIENT는 8 case 중 5개에서 ACTRATE보다 낮은 tracking, ACTRATE보다 8 case 전부에서 작은 action-change RMS를 보였지만, TERM-50은 H1/H3/H4에서 ORIENT보다 작았다. ACTRATE는 전진 H2와 10° 경사 H6 상·하 tracking 및 rough H5 평균/P05 전진에 강점이 있다(rough P05 `9.592m` vs ORIENT `8.863m` vs PERSONAL corrected LINTRACK-075 `8.670m`). 반면 zero-command 비의도 전진은 ACTRATE `1.987m`, ORIENT `1.633m`, LINTRACK `0.415m`이며 rough 최악 순위만으로 최종 정책을 결정하지 않는다. **이 문단은 당시 보고서만 비교한 역사적 상태다. TERM-50 case별 raw 수치·대응 비교는 위의 최신 9,216 episode 보고서에서 확보했지만, 단일 reward 인과·정식 정책 승격은 여전히 HOLD**. ANGTRACK-065 단일 정책 행동 분석 수신/HOLD, ACTRATE-001은 이후 OFFICIAL fresh3K와 PERSONAL 분석을 완료했으며 정책 HOLD다.

## 2026-10-10 H1 ACTRATE-0001 / model_2700 행동 분석 수신

[원문 보고서](../../incoming/other/reviewed/H1_MODEL2700_POLICY_ANALYSIS_20261010.md) · [판정/근거 요약](../../experiments/h1/2026-10-10_ACTRATE0001_MODEL2700_POLICY_REVIEW.md) · [실제 OFFICIAL Run](../../../../research/experiments/h1/exp-h1-action-rate-relaxation.md).

OFFICIAL fresh3K `ACTRATE-0001` Run `20261009-142350-h1-actrate-0001-fresh3k`은 COMPLETED/PASS이며, 그 자동 best **`model_2700.pt`**(SHA `e54d3389…93ca7ae`)가 Windows PERSONAL 6영상 + 3,072-episode camera-off `scenario7`에 사용됐다. 평가도 COMPLETE이고 **단일 정책 행동 분석 보고서까지 수신**했다. 이는 최신 keeper `model_2950.pt`, `ANGTRACK-065` 정책, 새로운 training Run 또는 공식 NCRC 점수가 아니다.

보고서에서 3,072/3,072 episode가 20초 생존했고 H2 전진 body 적분 **15.326m**, H7 push **10.542m**, H6 경사 상/하 **20.052/19.834m**로 실제 이동을 확인했다. 그러나 **H1 정지 명령에서 비의도 body 전진 1.987m**(월드 순변위 크기 중앙값 2.012m), **H3 횡이동에서 비의도 전진 1.677m**, H5 rough 최악 cohort의 전진 8.815m·tracking 0.2908·자세 RMS 0.0999, 다단 중앙 계단 통과 미검증이 남는다. **전진형 후보 HOLD**, 전지형 범용 채택/보상 인과 결론 보류. 영상과 camera-off는 다른 trajectory이며 `01_stairs.mp4`의 교대 검정 프레임은 캡처 결함이다.

다음은 새 GPU 실행보다 **보존된 `h1-submit-2 / TERM-50 model_2800` 동등 프로토콜 평가 raw의 조건 확인과 cohort별 대조**가 우선이고, `ORIENT-100/model_2850`은 별도 행동 후보 참고 비교다. 서로 다른 reward의 완료 사실만으로 개선율·공식 점수나 Optuna 결과를 만들지 않는다. `ANGTRACK-065`의 단일 정책 분석은 수신됐으나 matched-control 비교는 미완료, `ACTRATE-001`은 OFFICIAL fresh3K 완료/PASS·PERSONAL 분석 수납/HOLD다.

## 2026-10-10 H1 `LINTRACK-075` corrected5K / `model_4997` 행동 평가 수신

사용자가 전달한 [원문 심층 분석](../../incoming/other/reviewed/H1_LINTRACK-075_CORRECTED5K_POLICY_ANALYSIS_20261010.md)과 [해석·판정 기록](../../experiments/h1/2026-10-10_LINTRACK075_CORRECTED5K_MODEL4997_POLICY_REVIEW.md)을 연결했다. 이전 [legacy H-008 corrected R04](../../../../research/experiments/h1/H-008.md)의 PERSONAL 3K→5K unchanged continuation 최종 `model_4997.pt`(SHA `4349fe5650135c6a77546afc1b165ff60c235bdd83831bd562d618b04c3b5b6d`)에 연결되는 **후속 Windows PERSONAL 6영상 + camera-off scenario7 정책 평가**다. 새 train Run이나 OFFICIAL 제출/채점이 아니다.

보고서에서는 **3,072/3,072개의 20초 평가 episode 생존**, 전진 H2 body 15.015m(목표 15m), push H7 10.038m(목표 10m), 10° 경사 H6 상/하 19.943/19.776m로 **실제 이동 능력**을 확인했다. 그러나 rough H5 한 cohort는 20초 살아도 전진 2.8708m/stall 0.664이고, H1 zero-command 월드 순변위 0.516m/H3 좌우 복귀 1.280m가 남았다. 경사 yaw/action 변화 비용과 **계단 다단 통과·boxes 정량 공백**이 있다. **행동 후보 HOLD**: 평지/경사/push 내부 후보 보존, 범용 정책 PROMOTE 및 reward 인과 판정 보류. 영상과 별도 camera-off 평가는 다른 명령/지형이고, evaluation config의 `lin=0.5/term=-5`는 학습 reward 자체의 증거가 아니다. 우선 기존 `h1-submit-2 / TERM-50` 동일 evaluator의 보존 자료에서 source/PPO/protocol 조건을 확인해 H5 worst-case/H1·H3 잔류/H6 yaw 비용을 비교한다. 별도 GPU 실행 승인으로 확대하지 않는다.

## 현재 Experiment·Run 이름과 legacy 주소

새 명명은 [Experiment naming](../../../../research/EXPERIMENT_NAMING.md)에 따라 제출 preset (`h1-submit-2`, `h1-submit-4`, `g2-submit-3`, `g2-submit-5`), 검증 질문인 Experiment, 실제 학습 Run, 전체 resolved config, 최종 override, parent checkpoint lineage를 분리한다. 기존 세 제출의 byte-for-byte 전체 native `env.yaml`·`agent.yaml`과 출처·해시는 [frozen submission presets](../../../../research/submission_presets/README.md)에 있다. `g2-submit-5`는 2026-10-06 actual submission으로 새로 발급됐고 env/policy/report snapshot은 보존됐지만, native `agent.yaml`은 canonical OFFICIAL 7.5K archive에서 byte-for-byte 추출하기 전까지 full preset 디렉터리를 합성하지 않는다. `h1-submit-4` 제출 policy의 정확한 numbered checkpoint는 여전히 미확인이다. 새 `H/G/HS/GS`·`Rxx` 번호는 발급하지 않는다. 기존 이름은 [registry](../../../../research/EXPERIMENTS.md)의 legacy 주소다. Archive 이름의 `r01`을 registry `R01`로 추정하지 않고, 평가·영상·export를 추가 학습 Run으로 부풀리지 않는다. fresh/resume과 seed·학습량·부모는 Run/lineage에서 확인한다.

**AI 응답의 기본 표기는 현재 이름을 우선한다.** 현재 Go2 실제 제출은 `g2-submit-5 / LINTRACK-125`이며, 직전 Go2 기준 제출은 `g2-submit-3 / LINTRACK-150-LINZ-2`다. 필요할 때만 `legacy G-005, 초기 alias A1`을 괄호에 한 번 덧붙인다. 새 reward descriptor는 약어와 숫자 값을 하이픈으로 분리해 `LINTRACK-125`, `TERM-50`, `AIRTIME-025`처럼 쓴다. 하이픈이 없는 `LINTRACK125`, `TERM50`, `AIRTIME025` 같은 문자열은 과거 원문·파일명·legacy 검색 주소로만 취급하고 새 제목·본문 주어로 발급하지 않는다. 현재 track-only `LINTRACK-125`는 OFFICIAL fresh 3K와 별도 fresh 7.5K까지 분석됐다. 두 Run의 첫 3K 궤적은 exact match라 3K→7.5K 차이는 이 single-seed/config 안의 **학습량 효과**로 강하게 읽을 수 있지만, BASE 대비 `track_lin_vel_xy_exp=1.25` 자체의 reward 효과는 같은 길이 unchanged control이 없어 HOLD다. `legacy G-001 / LIN-TRACK`은 원문·registry를 찾을 때만 쓴다. 아주 오래된 `G5`는 `legacy G-004 ANG-STAB`을 뜻하므로 기본 이름으로 쓰지 않는다. legacy alias는 파일명·과거 보고서 검색이나 동명이인 해소에 필요한 경우 외에는 반복하지 않는다. **옛 `S1–S4`도 문서마다 뜻이 달라** 출처 없이 옮기지 않으며 GS schedule도 아니다.

### Reward descriptor 축약어 사전

특정 reward 설정 이름을 읽거나 만들 때 아래 축약어를 실제 변수명에 대응시킨다. **숫자가 없는 축약어 자체는 변수 축 이름일 뿐 특정 설정 이름이 아니다.** 특정 설정은 AI 라이브러리에 기록된 숫자 포함 descriptor를 사용하고, 정의되지 않은 descriptor를 임의로 만들지 않는다.

| 축약어 | 실제 변수명 |
| --- | --- |
| `LINTRACK` | `track_lin_vel_xy_exp` |
| `ANGTRACK` | `track_ang_vel_z_exp` |
| `AIRTIME` | `feet_air_time` |
| `TERM` | `termination_penalty` |
| `ORIENT` | `flat_orientation_l2` |
| `ANGXY` | `ang_vel_xy_l2` |
| `HIPDEV` | `joint_deviation_hip` |
| `TORSODEV` | `joint_deviation_torso` |
| `ACTRATE` | `action_rate_l2` |
| `LINZ` | `lin_vel_z_l2` |
| `TORQUES` | `dof_torques_l2` |
| `DOFACC` | `dof_acc_l2` |
| `DOFPOSLIM` | `dof_pos_limits` |

예를 들어 `ORIENT`는 `flat_orientation_l2` 축을 뜻하고, 2026-10-06 실행된 `ORIENT-100`은 그 축의 특정 값 `-1.0`을 가리킨다. `ACTRATE`는 `action_rate_l2` 축이고 OFFICIAL fresh3K 학습과 후속 PERSONAL 행동 분석까지 수신되어 **HOLD**인 `ACTRATE-001`은 특정 값 `-0.001`을 가리킨다. **2026-10-10 증거 갱신:** `ACTRATE-0001`(action `-0.0005→-0.0001`)은 OFFICIAL fresh3K Run `20261009-142350-h1-actrate-0001-fresh3k` **COMPLETED/PASS**, 이후 `model_2700` PERSONAL Windows 6영상+full 3,072 episode 평가도 **COMPLETE**(단일 정책 행동 분석과 TERM-50 대비 3,072 cohort-key 원자료 대응 분석 수신·정책 HOLD; 독립 반복/완전 terrain-pair 검증 미완료)다. `ANGTRACK-065`(ang `0.5→0.65`)도 별도 OFFICIAL fresh3K Run `20261009-155344-h1-angtrack-065-fresh3k` **COMPLETED/PASS**이며 PERSONAL 6영상/고정 평가 및 단일 정책 분석 수신(HOLD)다. 두 질문은 각각 [`exp-h1-action-rate-relaxation`](../../../../research/experiments/h1/exp-h1-action-rate-relaxation.md), [`exp-h1-angular-tracking-boost`](../../../../research/experiments/h1/exp-h1-angular-tracking-boost.md)에 기록한다. **세 single-delta 가설(ORIENT-100, ACTRATE-0001, ANGTRACK-065)에 더해 ACTRATE-001도 OFFICIAL fresh3K를 완료했다. ACTRATE-001 행동 판단은 HOLD다.** 각 Run은 fresh이고 reward/checkpoint를 상속하지 않으며, 가설과 Run ID, 제출 preset은 구분한다.

완료된 reward schedule 실행은 없다. Legacy [HS-001](../../../../research/experiments/h1/HS-001.md)은 `exp-h1-stable-first-track-switch`: `AIRTIME-025` fresh 3K Run `20260927-032343-h1-h005-fresh3k-r01-20260927`(legacy H-005 R03) → `lin=0.75`로 +2K다. Legacy [HS-002](../../../../research/experiments/h1/HS-002.md)는 `exp-h1-track-first-stability-switch`: `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch fresh 3K Run `20260927-043527-h1-h010-fresh3k-r01-20260927`(legacy H-010 R03) → `lin=0.5`로 +2K다. 두 질문은 PERSONAL PLANNED이며 현재 실행 예약이 아니다. **2026-10-06 ORIENT-100 OFFICIAL fresh 3K Run `20261006-133517-h1-orient-100-fresh3k-official`는 COMPLETE/PASS이며 `model_2850` PERSONAL 행동 평가 판정은 HOLD다.** frozen `h1-submit-2` 대비 orientation=-1.0, feet=0.20을 확인했다. 별도 ACTRATE-001 fresh 3K도 이후 실제 OFFICIAL Run `20261010-125324-h1-actrate-001-fresh3k`로 완료됐고 해당 PERSONAL model_2850 행동 분석은 HOLD다. ORIENT checkpoint/config를 상속하지 않는다. [접수·원본·Release·SHA](../../../../data/processed/experiments/h1/2026-10-06_ORIENT100_OFFICIAL3K_EVIDENCE_INTAKE.md). HS 질문은 같은 부모의 unchanged control과 비교하며 실행 전에는 Run ID를 예약하지 않는다.

## H1 계보 구분 — 2026-09-21 정정과 2026-09-25 corrected 실행

공식 `TERM-50` 5K의 `feet_air_time`은 `+0.2`, 과거 PERSONAL H-001 Run 04 부모는 `-0.2`다. 그 부모에서 나온 **역사적 `feet=-0.2` 계보**의 H-005~H-011 결과는 상대 비교용이며 단일변수 효과나 최종 채택 근거로 쓰지 않는다. 별도의 `+0.2` corrected 부모와 H-005~H-011의 2026-09-25 Run 02 등은 완료되어 아래 현황과 가설 registry에 등록했다. 9/27의 새 fresh·continuation Run과 과거 Run을 합치지 않는다. [계보·Delta 상세](../14_H1_NEXT_RUN_PARAMETER_COMPARISON.md) / [원문 정정](../../experiments/h1/2026-09-21_H1_PARENT_AIRTIME_LINEAGE_CORRECTION.md).


## Experiment registry

The current Git + Markdown experiment dashboard is
[`research/EXPERIMENTS.md`](../../../../research/EXPERIMENTS.md). It is the authoritative
dashboard for H1 and Go2 decisions, legacy aliases, parent lineage, per-run PERSONAL/OFFICIAL
classification, status, and links to the underlying analyses. It never replaces or moves
canonical evidence: originals remain in `naver-issacsim-originals`, while detailed
interpretation remains under `data/processed/`. When writing performance reports, use only
Runs explicitly marked `Environment: OFFICIAL` in that registry.

# 프로젝트 맥락과 AI 입력 안내

이 폴더의 Markdown 21개를 상담 AI에 업로드하는 핵심팩이다. 검증된 상세 실험 자료는 독립 문서로 승격할 수 있지만, 원문·전사·중간 초안을 그대로 늘리지 않는다.

## 신뢰 순서

1. 인접한 `../naver-issacsim-originals/data/raw`의 최신 공식 규정·공지와 원본 코드·영상·에셋
2. 이 폴더의 현재 서버 코드·엔진·규정·강의 통합 분석
3. `data/processed/experiments/`의 원본 산출물·코드로 교차검증된 실제 실행 결과
4. `data/processed/external_analysis/video_reports/`의 화면 직접 관찰과 공식 자료로 교차검증된 내용
5. 솔루션·검증·서버 운영 청사진과 영상 분석의 권장안·추론

원본 코드와 분석이 충돌하면 원본을 우선한다. 엔진의 버그 후보는 정적 분석이므로 실제 운영 backend나 최신 대회 빌드에서 달라질 수 있음을 함께 표시한다. 영상과 3D 장면은 텍스트만으로 추측하지 않는다.

보존된 H1·Go2 학습/재생 기준 snapshot은 2026-09-13 공식 서버 `/workspace/training`(archive SHA-256 `2c1326e0b58e9c860e32db81f110d2c0de16fac113de4424144b73e39fe01d15`)이다. 실제 실행 source는 각 run evidence로 확인하고, 과거 processed server-backup 분석본으로 대체하지 않는다. 현재 checkout과 보존본의 비교 범위는 NVIDIA [CURRENT_SOURCE.md](https://github.com/SE3C/naver-issacsim-nvidia/blob/main/CURRENT_SOURCE.md)를 따른다.

## 현재 운영 상태 요약

**2026-10-09 Go2 후속:** [R3 original4800 / R5 terminal7450 검증 요약](../../experiments/go2/2026-10-09_GO2_R3_4800_R5_7450_LOCAL_OFFICIAL_COMPARISON.md). 같은 PERSONAL protocol에서 계단 통합 오차 **0.32029→0.14852**, 실패 **15/783→4/772**, G2 오차 **0.09085→0.07699**로 개선됐지만 공식 계단·전방위 Tracking Score는 하락했다. 로컬 고정 12.5cm/직진 조건과 공식10–15cm·미공개 명령/초기조건의 coverage를 우선 확인한다. 같은 scorer/collector/config와 raw 재집계가 일치하므로 점수 보정·scorer 교체·새 reward 학습을 서두르지 않는다. 과거 PERSONAL all-around REJECT를 공식 추종 대조군 제외로 확대하지 않으며, 4800의 공식 추종 상대 우위와7450의 공식 생존 이득을 모두 보존한다. reward-effect HOLD는 유지한다. 4800 통합 ZIP은 NVIDIA PERSONAL Release에 보존했다(상세 `21`).

| 항목 | 현재 기준 |
|---|---|
| sidecar 기준 | 현재 `issacsimz` `b779fb9`. OFFICIAL H1·Go2는 `--import-checkpoint`로 단일 native `.pt` 재개를 지원하며, imported 부모 출처는 unknown/미검증으로 기록한다. 기존 verified indexed resume와 구분하며 실행 절차·제출용 provenance 제한은 `19`를 따른다. bootstrap evidence root를 직접 CLI에도 전달하며 명시적 `ISSACSIMZ_LOG_ROOT` override는 유지한다. 개인 bootstrap은 게시 없는 직접 CLI smoke와 본학습 wrapper의 Release 경로를 구분한다. PERSONAL `issacsimz_video_suite.sh`는 6개 영상과 bundle 검증을 모두 통과하면 Release를 자동 게시하고, `--no-publish`로 로컬 결과만 남길 수 있다. 선택적 Experiment/config 표시는 `19`의 Release naming 규칙을 따른다. **OFFICIAL에서 금지되는 것은 이 PERSONAL 자동 suite 스크립트와 GitHub 게시이지, 6지형 영상 제작 자체가 아니다.** 공식 서버에서는 공식 `play.py`로 지형별 영상을 직접 만든다(`17`). 로컬 WSL 전체 **136/136 PASS**, portable build·생성 pyz checksum PASS이며 실제 서버 학습·GitHub 게시를 실행한 검증은 아니다. |
| official 실행 | `bootstrap_server.sh --mode official` 뒤 mode-aware train/video wrapper를 쓴다. bootstrap state는 선택된 mode의 `ISSACSIMZ_H1_ROOT`·`ISSACSIMZ_GO2_ROOT`·`ISSACSIMZ_ISAACLAB_ROOT`를 공통 계약으로 기록하므로 `doctor`에 경로를 반복 지정하지 않는다. 상주 GPU sampler·범용 checkpoint watcher/mirror·독립 `watch`·외부 publish는 사용하지 않는다. |
| 중간 checkpoint | profile train은 PERSONAL·OFFICIAL 모두 native `agent.save_interval=50`을 자동 전달한다. OFFICIAL에서는 운영진의 공개 keep-all 절차를 run별로 적용한 `organizer_keep_all_ckpt.sh`가 학습 중 `model_*.pt`를 `backup_log/<native-run>/`에 복사하고, 종료 후 evidence `.tar.gz`에 포함한다. 기존 H1 고정 회차 `organizer_keep_ckpt_h1_verbatim.sh` 본문은 역사적 원문으로 변경하지 않았으며 자동 경로가 아니다. 전사본의 합쳐진 셸 블록은 그대로 실행하지 않는다. 실제 보존 회차는 실행 후 확인한다. 상세: `11`, `19`, [운영진 답변 전사본](../../incoming/other/reviewed/2026-09-26_H1_ORGANIZER_CHECKPOINT_QA_SIRIUS_YEOLMU.md). |
| personal 실행 | 첫 접속에는 공개 `issacsimz`를 clone하고, 재접속에는 그 checkout을 `pull --ff-only`한다. 그곳에서 personal bootstrap을 실행하면 GitHub 인증 확인 뒤 비공개 NVIDIA checkout을 clone/fast-forward pull하고 Git tag 작성자 정보를 해당 checkout에만 설정한다(이메일 `ncrcissacsimz@users.noreply.github.com`). READY 뒤 짧은 게시 없는 smoke는 직접 `./issacsimz train ...`; 본학습 wrapper는 완료·evidence validation PASS인 archive만 Release 게시를 시도한다. 실패·중단 archive는 로컬 보존한다. 정확한 명령은 `11`, `19`와 NVIDIA README를 따른다. |
| 운영진 오늘의 🍯TIP | [주제별 색인·전달 원문](../../external_analysis/2026-09-23_ORGANIZER_DAILY_HONEY_TIPS_SOURCE_AND_NOTES.md#주제별-찾아보기)을 단일 입구로 사용한다. 영상 진단 요약은 `17`; 실제 checkpoint·실행 절차는 `19`·`21`을 따른다. |
| R3/R5 운영진 답변과 현재 판단 | [운영진 DM·구성 분석](../../experiments/go2/2026-10-08_GO2_R3_R5_OFFICIAL_SCORE_COMPONENTS_ORGANIZER_REPLY.md): 공식 계단 survival **99.0%→99.8%**, Tracking Score **0.819→0.796**. 생존 이득 약 **+0.07**보다 추종 손실 약 **−0.24**가 커 계단 **8.52→8.35**; 전방위는 survival 100%로 같고 tracking **0.834→0.829**, 약 **−0.06점**. 나머지 다섯은 거의 안정적이다. 학습 contact 종료율과 고정 평가 survival은 다른 지표다. 다음 질문은 **개선된 계단 생존을 유지하며 명령 추종 손실을 회복할 수 있는가**다. 공식 점수 구성은 사용자 제공 답변으로 확인됐지만 로컬·공식 역전 메커니즘·reward 인과·새 reward는 미확정. [판정 방향](../../experiments/go2/2026-10-08_GO2_LOCAL_OFFICIAL_EVALUATION_GAP_AND_ANALYSIS_POLICY.md), `05`, `07`, `10`, `15`, `21`을 따른다. |
| 2026-09-30 예선 순위 snapshot · 역사적 기록 | 사용자가 11:54 기준 포털 표를 제공했다: SE3C **19위**, H1 **86.37**, Go2 **87.55**, 총 **173.92**. 32위는 **173.27**로 당시 간격은 **+0.65점**이다. 이는 사용자 제공 시점 snapshot이며 AI가 독립 조회한 live leaderboard가 아니다. 이후 팀 점수 갱신으로 순위·컷은 변할 수 있다. · 현재 순위로 재사용하지 않는다 |
| 2026-10-08 예선 순위 snapshot | 화면 업데이트 **15:21** 기준 SE3C **29위(10계단 하락)**, H1 **86.37/100**, Go2 **88.32/100**, 총 **174.69/200**. 사용자가 전달한 HTML·이미지 전사이며 live 조회가 아니다. [공식 R5 평가](../../experiments/go2/2026-10-08_OFFICIAL_EVAL_GO2_ROUND5_LINTRACK125.md). R3 대비 종합 +0.77이지만 시뮬레이션 −0.23·계단 −0.17이므로 종합 상승과 시뮬레이션 개선을 혼동하지 않는다. |
| Go2 LINTRACK-125 — 2026-10-05 C4800/C7050/C7450 행동 비교 | OFFICIAL fresh 3K·7.5K COMPLETE/PASS와 첫 3K exact match는 기존 학습량 근거다. 후속 PERSONAL 동일 `scenario7` 3정책 비교에서 terminal `model_7450`은 `model_7050`보다 9개 case 중 8개에서 tracking error가 낮고 8개에서 진행이 크며 계단 하행 stall `2.52%→0.60%`로 개선돼 **현재 내부 행동 주후보 PROMOTE**다. 대신 stair-up base-contact 종료 `2→4`, action/body RMS 증가가 있어 `model_7050`은 **안전성 fallback HOLD**로 보존한다. `g2-submit-3` original 4800은 계단 15회 base-contact 종료 때문에 현재 all-around 후보 기준 REJECT다. 이는 PERSONAL 진단이며 공식 점수·제출 판정이 아니고 `LINTRACK-125` reward 효과는 same-length BASE control 부재로 계속 **HOLD**다. · [3정책 심층 비교](../../incoming/other/reviewed/GO2_C4800_C7050_C7450_POLICY_COMPARISON_20261005.md), [registry](../../../../research/EXPERIMENTS.md), `07`, `15`, `16`, `17`, `21` |
| g2-submit-5 / LINTRACK-125 · 2026-10-06 Round-5 제출 | 사용자가 actual portal 제출 완료를 보고했다. source는 OFFICIAL fresh 7.5K Run `20260929-154342-go2-lintrack-125-fresh7500-official`, 선택 checkpoint는 terminal `model_7450.pt` SHA `b8766030…343a`. 제출 `policy.pt`의 8개 actor tensor는 native 7450과 exact-match이고 `env.yaml` SHA `e7eeff96…47a9`는 OFFICIAL training record와 일치한다. [submission Release](https://github.com/SE3C/naver-issacsim/releases/tag/submission-go2-prelim-r5-20261006)에 policy/env/기술개선 리포트/manifest/checksum 5개 asset을 보존했다. 2026-10-08 사용자 전달 공식 평가에서 제출 시각 2026-10-06 01:10(시간대 미기재), 종합 88.32/100(시뮬레이션 58.32/70·설계 의도 20/20·리포트 품질 10/10)을 수신했다. 별도 포털 receipt 파일은 미보유다. 선택 근거의 PERSONAL 3정책 비교는 공식 점수나 reward 인과효과가 아니며 `LINTRACK-125` reward effect는 HOLD다. · [registry](../../../../research/EXPERIMENTS.md), [manifest](../../experiments/go2/2026-10-06_PRELIM_R5_SUBMISSION/submission_manifest.json), `05`, `07`, `16`, `21` |
| 2026-10-10 H1 single-dial 실행 현황 | ORIENT-100 OFFICIAL fresh3K Run `20261006-133517-h1-orient-100-fresh3k-official` **COMPLETE/PASS**, 이후 `model_2850` PERSONAL 행동 분석은 HOLD(최신 keeper 2950과 구분). OFFICIAL unchanged `h1-submit-2` fresh3K control `20261008-062732-h1-term-50-fresh3k-control` **COMPLETE/PASS**, `model_2800` PERSONAL full 자료 보존. `ACTRATE-0001` OFFICIAL fresh3K `20261009-142350-h1-actrate-0001-fresh3k` **COMPLETE/PASS**; `model_2700` Windows PERSONAL 여섯 영상+full `scenario7` **COMPLETE**(3,072 episode), **단일 정책 행동 분석 수신/HOLD**이며 matched 비교는 미완료. `ANGTRACK-065` OFFICIAL fresh3K `20261009-155344-h1-angtrack-065-fresh3k` **COMPLETE/PASS**, fixed evaluation·심층 분석 미수신으로 **HOLD**. **ACTRATE-001 Run `20261010-125324-h1-actrate-001-fresh3k`도 OFFICIAL fresh3K COMPLETE/PASS, best2850 PERSONAL 분석 수납/HOLD**. frozen `h1-submit-2` 기준 독립 reward delta·seed42·4096 env이며 전체 source/PPO parity와 평가 A/B는 별도 검증해야 한다. 개인 후속 평가 완료를 OFFICIAL 점수/제출로 해석하지 않는다. · [Registry](../../../../research/EXPERIMENTS.md), [ACTRATE-0001](../../../../research/experiments/h1/exp-h1-action-rate-relaxation.md), [ANGTRACK-065](../../../../research/experiments/h1/exp-h1-angular-tracking-boost.md), [baseline Run](../../../../research/EXPERIMENTS.md) |
| 2026-09-27 H1 실행·분석 | 세 PERSONAL Run 모두 exit 0·evidence PASS. `AIRTIME-025` fresh/continuation과 `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch fresh 비교는 TensorBoard·console·영상의 AI 분석 결과이며, H1 통합 launcher 설치·CPU 60개 검증은 완료됐지만 **이 9/27 PERSONAL 후보들의 Windows GPU full 및 paired evaluation은 아직 수행되지 않았다**. 10/07 `ORIENT-100` 단일 정책의 별도 full 자료와 혼동하지 않는다. corrected 3K 대비 동일 reward +2K continuation의 late terrain·XY·yaw·training contact는 개선됐지만, same-parent unchanged 3K control 대비 feet `0.25` 자체의 이득은 작고 trade-off가 있다. `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch fresh는 `AIRTIME-025` fresh보다 XY error가 낮지만 yaw error와 training base-contact가 높고 terrain 우위는 없다. 과거 문서의 `PROMOTE to fixed paired evaluation`은 미래 검증 우선순위라는 뜻이지 완료된 평가 결과가 아니다. · [수신 기록](../../experiments/h1/2026-09-27_H1_FRESH_AND_CONTINUATION_EVIDENCE_INTAKE.md), [해석](../14_H1_NEXT_RUN_PARAMETER_COMPARISON.md) |
| h1-submit-4 / AIRTIME-025 · OFFICIAL fresh 10K·4라운드 제출 | 공식 Run 05는 `termination=-50`, `feet_air_time=0.25`로 fresh 10K를 완료했고 evidence PASS. Round-4 공식 평가는 시뮬레이션 **56.37/70**, 설계 의도 **20/20**, 리포트 품질 **10/10**이며 세 구성 점수 합계는 **86.37/100**으로 Round-2 종합 점수와 수치상 같았다(수신 원문에는 별도 종합 점수 필드 없음). 세부 시나리오는 전진·회전·경사·밀침이 소폭 상승하고 제자리·좌우·요철이 하락했으며 약한 요철은 **8.17→8.00**이었다. 같은 5K 단계의 TERM-50 대비 AIRTIME-025 전체 우위도 확인되지 않았다. 제출 `policy.pt`의 정확한 numbered checkpoint 연결은 여전히 미확인이다. · [공식 실행·평가](../13_H1_OFFICIAL_SERVER_BASELINE_EVIDENCE.md), [심층 원문](../../incoming/other/reviewed/H1_H005_OFFICIAL10K_VS_TERM50_OFFICIAL5K_DEEP_ANALYSIS_20260928.md), [registry](../../../../research/EXPERIMENTS.md) |
| 서버용 복사·실행 카드 | “Brev 서버 셋업 스크립트 완료/서버 켬”은 Isaac Sim/Lab 등 기본 환경 준비만 뜻한다. `issacsimz`·NVIDIA checkout의 clone/pull이나 personal bootstrap `READY`를 뜻하지 않는다. AI는 PERSONAL 첫 접속/재접속과 OFFICIAL 첫 접속/재접속을 구분하고 `19`의 해당 준비 명령부터 제시한다. OFFICIAL은 `/workspace`에서 공개 Codeberg `issacsimz`를 clone하거나 기존 checkout을 `pull --ff-only`한 뒤 official bootstrap을 실행한다. GitHub clone·pull·push·인증·Release 등 GitHub와의 상호작용은 하지 않는다. `READY` 확인 전 doctor·reward·runs·checkpoint 탐색을 준비 완료된 checkout에 대한 명령처럼 앞세우지 않는다. 학습 뒤 evidence 판정 후 유망한 후보의 영상을 조건부로 안내한다. **OFFICIAL 6지형 요청은 PERSONAL suite가 아니라 공식 `play.py`를 지형별로 여섯 번 직접 실행하는 `17`의 H1 예시를 따른다.** OFFICIAL numbered checkpoint를 sidecar `play`에 지정할 때는 실제 evidence root와 index의 `source_path`를 확인한 뒤 명령을 완성한다. AI의 서버 종료 명령은 넣지 않는다. 상세: `11`, `17`, `19`. |
| 보존 경계 | canonical evidence/export가 원본이고, `ISSACSIMZ_DOWNLOAD` handoff·download bundle은 탐색용 복사본이다. 다만 9/25·9/27 PERSONAL H1 train archive는 현재 로컬 Originals Git 경로에서 확인되지 않았으며 NVIDIA private Release와 9/27 Downloads 복사본으로 확인했다. Release mirror를 Originals에 이미 canonical 보존한 것으로 쓰지 않는다. 미래 GitHub Release는 로컬 annotated tag를 먼저 push한 뒤 그 tag를 선택해 게시하며, 기존 Release/tag는 목록 순서만으로 바꾸지 않는다. |
| 외부 공개 관찰 | 2026-09-22 NCRC researchlog 공개 스냅샷은 실패 사례 47개 중 detail 45개, H1 실패 38개(단일 dial 5개), 성공 34개 detail 0개만 제공한다. 9월 23일 보존한 **별도 20초 영상 심층 판독**은 5건에서 낮은 fall과 진행 정체, 높은 reward와 비정상 보행 등이 공존함을 보고했다. 따라서 내부 평가는 생존·실제 진행·추종·보행 품질을 분리하되, 외부 영상·row를 공식 점수나 인과 실험으로 사용하지 않는다. corrected +0.2 TERM-50 parent + unchanged control에서의 단변수 질문과 action-rate 음성 대조는 `20`을 따른다. 외부 row를 내부 Run·Optuna trial로 합치지 않는다. 원본·품질 경계: `reference/public/2026-09-22_ncrc_public_data_audit/`, `incoming/other/reviewed/NCRC_H1_VISUAL_FAILURE_DEEP_ANALYSIS_20260923.md` |
| 공개 웹·평가 응답 분석 | 9/22·9/23 researchlog HTML/JSON은 별개 스냅샷이다. 9/23 `videos.json`은 같은 영상 key 84개를 유지하며 `school` 필드를 제거했고 전체 `stats`는 갱신됐다. 새 보고서는 본인 팀 R3 Go2 평가 `remark`에 서버 학습 run과 다른 checkpoint를 가중치 유사도 0.9952로 연결한 기록이 있다고 보고한다. raw 평가 응답은 현재 snapshot에 보존되지 않아 보고서 기반 단서이며 채점·유사도 알고리즘은 미확인이다. 제출 계보 확인을 완화하지 않는다 · `05`, `reference/public/2026-09-23_ncrc_site_snapshot/`, `incoming/other/reviewed/NCRC_WEBSITE_PUBLIC_ANALYSIS_2026-09-23.md` |
| R3 Go2 가중치 유사도 후속 검증 | 새 `sub-5916` 학습기록 ZIP의 `model_best.pt`는 기존 official recovery 4900과 SHA가 같고, 별도 받은 `policy.pt`는 기존 R3 제출 Release의 original 4800 정책과 SHA가 같다. 보고서는 두 actor의 cosine `0.9952368736`과 평가 `remark`의 `0.9952` 일치를 기록했지만, 이번 intake는 Torch 계산·인증 API raw 응답을 재현하지 못했다. 정확한 백엔드 함수·threshold는 미확인이다. recovery 백업과 `g2-submit-3` original 4800 제출을 혼합하지 않는다 · `05`, `07`, `g2-submit-3` 계보 registry(legacy G-005), `incoming/other/reviewed/NCRC_R3_WEIGHT_SIMILARITY_DISCOVERY_2026-09-23.md` |
| AI 작업 운영 | smoke·짧은 debug/play는 경로·파일 존재·load/import·짧은 실행·exit·치명 오류만 본다. hash는 정책 동일성, 고비용 실행의 직접 산출물, evidence·archive·제출·다운로드 무결성처럼 필요한 경우에만 쓴다. 같은 실행에서 이미 확인한 값은 변경 근거 없이 재검증하지 않는다. **OFFICIAL 서버는 명시적 종료 요청을 받아도 AI가 종료하지 않는다.** PERSONAL 서버 종료와 원본 삭제·archive 교체는 사용자의 명시 요청이 있어야 한다. 상세: `11`, `19` |
| 학습 종료 후 비교 제안 | 분석 가능한 evidence가 생기면 AI는 사용자에게 가장 정보가 큰 대조군 1순위와 필요시 2순위를 제안한다. resume reward 변경은 같은 부모의 unchanged continuation, fresh 변경은 조건을 맞춘 fresh 기준선, 정책 선별은 동일 evaluator가 우선이다. 이미 보존된 학습 archive·6지형 영상을 먼저 확인하고 비교 한계와 필요한 추가 자료를 밝힌다. 제안만으로 새 학습을 실행하지 않는다 · `14`, `15`, `16` |
| 자동평가 Tracking·Survival 공개 답변 | 2026-09-26 제공된 1차·추가 답변 정리본에 따르면 몸통 기준 x·y·yaw-rate 오차는 별도 정규화 없이 Euclidean 크기로 합쳐지고, step→episode 평균→episode 동일 가중 평균을 거친다. Survival 분모는 episode 수이며 반복 낙상은 반복 실패다. 출발·10초 명령 전환·낙상 전 구간도 포함된다. **평균오차→점수 변환식과 시나리오별 command 값은 미공개**. 제공 전사본은 원본 게시 화면·evaluator 코드의 독립 검증이 아니다 · `10`, `15`, [답변 정리본](../../incoming/other/reviewed/01_운영진_자동평가_Tracking_Survival_공개답변_20260926.md), [구조 분석](../../incoming/other/reviewed/02_자동평가_Tracking_Survival_구조_분석보고서_20260926.md) |

## 2026-10-07 H1 ORIENT-100 행동 평가 최신 판정

`exp-h1-rough-terrain-orientation-relaxation / ORIENT-100`의 학습 Run은 **OFFICIAL fresh 3K COMPLETE/PASS**(`20261006-133517-h1-orient-100-fresh3k-official`). 후속 Windows **PERSONAL** `model_2850.pt` 6영상 및 camera-off H1 `scenario7` full 평가가 2026-10-07 완료됐고, 8 case × 3 seed × 128 env = **3,072/3,072 20초 생존** 및 실제 전진·외란 보행을 관찰했다. 정지 H1의 비의도 body 전진 **+1.633m**, 순수 횡이동 H3 **+1.180m**, rough H5 평균 tracking 오차 **0.1709**, 최소 진행 **7.831m**와 계단 중앙 완주 미입증이 남아 **현재 행동 후보는 HOLD(보존·우선 대조), REJECT/PROMOTE 아님**이다.

**평가기 상태:** H1 **단일 정책 GPU full은 자료상 완료**, 동일 evaluator의 `h1-submit-2 / TERM-50` **원본 9,216 episode 대응-key 기술비교는 2026-10-10 완료**(Windows 비교 CLI 별도 실행·동일 물리 terrain 확인·reward 인과 검증은 미실행). 평가·영상 조건이 다르고 일부 검정 프레임은 캡처 결함이다. OFFICIAL 학습 기록과 PERSONAL 사후 검증은 checkpoint SHA로 연결하되 PERSONAL 점수·reward 개선 효과·제출 성능을 OFFICIAL로 승격하지 않는다. [원문 보고서](../../incoming/other/reviewed/H1_ORIENT-100_POLICY_ANALYSIS_20261007.md) · [가설 상세](../../../../research/experiments/h1/exp-h1-rough-terrain-orientation-relaxation.md) · [registry](../../../../research/EXPERIMENTS.md).

rough H5에서도 실패는 **0/384**지만 P05 진행 **8.863m**, P95 tracking **0.1948**로 약점은 낙상보다 진행·추종의 나쁜 꼬리에 나타난다. 이는 단일 후보 내부 특성이며 baseline 대비 열화 판정이 아니다.

## 현재 평가기 구현 상태

**2026-09-30 시점에는** H1/Go2 공용 fixed evaluator/paired harness가 없었고, 과거 seed-4201 fixed batch는 특정 4300/4800/4900 checkpoint 비교용 역사적 PERSONAL evidence였다. 이후 Windows Go2 경로는 실제 GPU full 기록까지 확보했다. 2026-10-06에는 같은 공용 core를 재사용하는 H1 Windows 통합 launcher를 `C:\NCRC\h1_6terrain_video.bat`에 설치하고 CPU 회귀 테스트 60개와 PowerShell/설치 파일 검증을 통과했다. H1은 ±10° 6영상 뒤 camera-off `scenario7` 8 case full 평가를 사용하고 smoke 옵션은 제거됐다. 이는 2026-10-06 시점의 상태이며, **2026-10-07 `ORIENT-100 / model_2850`의 PERSONAL 6영상/full 평가 자료가 추가됐다**. 여전히 H1 paired A/B와 공식 점수는 없다.

2026-10-07 중간 ZIP 저장 위치 변경 이후 H1/Go2 모두 checkpoint 옆에는 영상·평가 **통합 ZIP 하나만** 만들고, 재사용용 영상 ZIP은 내부 로그 폴더에 보존한다. ORIENT-100의 native 영상·평가 성공 뒤 발생한 wrapper 후처리 실패와 CPU 포장 복구는 `21`에 기록하며 최초 BAT 전체 성공으로 바꾸지 않는다.

현재 [21번 Windows Go2 운영 문서](../21_WINDOWS_GO2_VIDEO_AND_EVALUATION.md)의 `C:\NCRC\go2_6terrain_video.bat`는 고정 6영상 ZIP 뒤 별도의 camera-off `scenario7` 개별 평가를 실행한다. 2950·7050 full 평가는 native/BAT exit 0·동일 프로토콜이었다. 이후 제공된 심층 보고서가 raw 수치·영상을 비교했으며 자동 comparison-CLI 보고서·calibration·점수는 생성하지 않았다. 영상은 qualitative evidence이고 2950 boxes 검은 화면은 별도 결함이다. PERSONAL 내부 평가를 공식 채점 함수·제출 우위로 확대하지 않는다. 2026-10-07부터 H1 `ORIENT-100 / model_2850`의 **단일 정책 PERSONAL GPU full 평가 근거가 별도로 존재**한다. 다만 H1 다른 checkpoint 호환·matched A/B·자동 Optuna objective readiness가 완료됐다고 확장하지 않는다.

사용자가 네이버 폴더에서 **“6영상 뽑고 평가 돌려줘”**라고 하면 이 Windows 통합 launcher로 지정 checkpoint의 6영상 ZIP과 개별 평가자료를 만드는 요청으로 해석한다. checkpoint 경로와 GPU 실행 승인이 확인돼야 하며, 승인 범위가 이미 명확하면 다시 묻지 않는다. 문서 반영만 요청한 것은 GPU 승인이 아니다. 비교는 사용자 담당이고 `compare_policies`/`-CompareWith`는 별도 명시 요청 없이는 실행하지 않는다. 6개 BAT/PS1의 실제 역할·검증 경계와 네이버 `AGENTS.md` 계약은 `21`을 따른다.

## 핵심팩 구성

현재 full 완료의 주 전달물은 **6영상 + 개별 평가 원자료·diagnostics 요약을 함께 담은 통합 ZIP**이다. smoke는 통합 full ZIP을 만들지 않는다. 실행 도구·설치기의 재현 가능한 소스는 `naver-issacsim-eval`에 동기화했으며, 상세 계약과 실제 2950·7050 통합 ZIP 검증은 `21`을 따른다.

- `01`~`04`: 강의·용어·시뮬레이션·센서·강화학습·명령
- `05`~`07`: 예선/본선 실무와 H1·Go2 학습 코드
- `08`: 게임 엔진의 관측·보상·시나리오 구조
- `10`~`11`: 솔루션·검증 청사진과 NVIDIA 서버 운영
- `12`: 통합·예선·본선 규정과 공식 Q&A를 합친 단일 규정 기준
- `13`: H1 공식 서버 300회·baseline 1K·TERM-50 5K 실행의 검증된 실측 증거와 한계
- `14`: TERM-50 5K 이후 단일 파라미터 paired 비교와 staged training 검증 프로토콜
- `15`: Optuna Ask-and-Tell reward 탐색의 readiness·범위·objective·중단 기준
- `16`: headless 실행, 전체 run export, TensorBoard·콘솔·GPU 로그 분석 규칙
- `17`: PERSONAL 영상 evidence·6지형 suite와 OFFICIAL H1 공식 `play.py` 수동 6지형 실행 절차
- `18`: H1 finalize/report의 자동 best 선택·std 경고·checkpoint cleanup 한계
- `19`: 서버 준비·train CLI, evidence·archive·download handoff 계약과 공식 Go2 정상 완료 검증 범위. 학습 명령은 **「OFFICIAL 학습 시작·재개 표준 절차」**의 fresh/indexed/단일 `.pt` import 분기를 먼저 적용한다. H1·Go2 공통이며 미검증 import는 공식 부모 출처 증명이 아니다. 영상 실행 명령은 `17`
- `20`: 공개 H1 실패 38건과 내부 계보를 교차해 도출한 실험 prior·실패 경보·통제군/평가 설계. 공개 기록은 OFFICIAL 성능 근거가 아님
- `21`: Windows native Go2 고정 6영상·ZIP과 별도 개별 평가, 6개 BAT/PS1의 역할·안전한 호출·검증 기록. 공식 서버 실행이나 자동 A/B 비교와 구분

Release 보존은 개인 서버 학습·native 영상(NVIDIA) / 새 Windows PC 평가(eval) / 공식 raw(Originals) / 실제 제출 snapshot(analysis)으로 분리한다. 기존 PC 평가 Release는 기존 NVIDIA 주소·애셋을 유지하고 eval의 `EVALUATION_RELEASES.md`에서 연결한다. 위치·tag·manifest·hash 규칙은 `docs/RELEASE_TAXONOMY.md`를 따른다.

OT 화면·오디오 판단은 별도 파일이 아니라 `05`(실험 루프·제출 파일), `11`(서버 시간·접속), `12`(규정)에 녹여 두었다. 상세 전사·시간대는 `incoming/ot/analyses/`에 보존한다.

새 영상 분석 보고서 7개는 핵심팩에 전문으로 추가하지 않는다. 검증된 신규 정보만 `05`, `10`~`12`에 통합하며, 영상의 데모 수치·학습시간·예시 점수는 현재 환경의 사실로 사용하지 않는다. 게임 에이전트·경로계획 참고 분석은 핵심팩 밖 `data/processed/reference/09_GAME_AGENT_NAVIGATION_SENSORS.md`에 보존한다.

2026-08-24 공식 300회, 2026-09-08 공식 baseline 1K와 TERM-50 5K 분석 전문은 핵심팩에 그대로 넣지 않았다. 상세 근거는 `13`을 따른다. 예선 2라운드 `h1-submit-2 / TERM-50` 제출의 공식 점수는 종합 86.37/100, 시뮬 56.37/70이다. 그 이전 학습 내부 지표와 play 영상은 제출 점수로 소급 해석하지 않는다.

## Go2 결과를 읽는 순서

2026-08-30 개인 Go2 분석과 2026-09-13 master tracking report는 기존 문서에 통합했다. `g2-submit-3 / LINTRACK-150-LINZ-2` 계보(원문 파일명에는 legacy A1/G-005 표기가 남아 있음)의 1K·fresh 3K·video·official fresh-interrupted·recovery, 공식 legacy G-004 ANG-STAB 1K failure, 4300/4800/4900 checkpoint 분석 및 최종 4800/4900 비교 원문은 `incoming/other/reviewed/`에 byte-for-byte 보존한다. 최신 통합 원문은 `A1_4800_vs_4900_DEEP_ANALYSIS_AND_LEARNING_RECORD_20260915.md`이며 SHA-256은 `81b79688…c1a8`이다. baseline·checkpoint 판단은 `07`, 제출 경계는 `05`, 영상 운영 원칙은 `11`, 영상 실행 절차는 `17`, 원본 보존·발산 진단은 `16`, 비교 설계는 `15`를 따른다. 아래 H1 표의 상태와 다음 행동은 H1에만 적용한다.

Go2 개인 L40S 12k 시도(2026-08-30)는 9.5k 이후 value loss 발산으로 중단됐다. 발산 전 `model_9500.pt`는 tensor가 finite라 개인 B0로 보존한다. 편의상 “5k”라 부른 후보의 실제 저장본은 reward peak 4509에 가까운 `model_4500.pt`다. 둘 다 120초 play 영상이 있다. 공식 점수·12k 완주가 아니다. 운영진은 장기 발산을 알려진 확률적 수치 불안정으로 보고, 제출용은 배포 PPO를 유지한 채 reward·iteration만 조절하라고 했다. 상세는 `07`, 영상은 `11`, 보존은 `16`이다.

## 현재 실험 상태와 바로 다음 행동

이 표는 현재 판정의 길잡이다. Run별 수치·원본 SHA·영상 source는 [가설 registry](../../../../research/EXPERIMENTS.md)와 주제별 문서에서 확인하고, 아래 요약을 별도의 평가 결과로 세지 않는다.

| 계보 | 현재 판정과 주의점 | 상세 |
| --- | --- | --- |
| `h1-submit-2 / TERM-50` (legacy H-001 R02) | 공식 baseline 1K는 terrain 0·낙상률 100%의 초기 대조군이다. `h1-submit-2 / TERM-50` 공식 fresh 5K는 2라운드 86.37/100(시뮬 56.37/70)을 받았다. 과거 PERSONAL legacy H-001 R04 `feet=-0.2`는 공식 `+0.2`와 다른 부모다. | [공식 증거](../13_H1_OFFICIAL_SERVER_BASELINE_EVIDENCE.md), [계보](../14_H1_NEXT_RUN_PARAMETER_COMPARISON.md) |
| `h1-submit-4 / AIRTIME-025` (legacy H-005 R05) | 공식 서버에서 `termination=-50`, `feet=0.25`로 fresh 10K를 완료하고 evidence PASS. `h1-submit-4 / AIRTIME-025`로 4라운드 제출·공식 평가까지 확인됐고, 시뮬레이션 56.37/70·설계 의도 20/20·리포트 품질 10/10이다(세 구성 점수 합계 86.37/100). 포털 수령증·정확한 제출 시각과 제출 `policy.pt`의 정확한 numbered checkpoint 연결은 여전히 미확인이다. 같은 5K 단계에서 H-001 R02 대비 전면 우위도 확정되지 않았다. | [공식 증거](../13_H1_OFFICIAL_SERVER_BASELINE_EVIDENCE.md), [비교](../14_H1_NEXT_RUN_PARAMETER_COMPARISON.md) |
| H1 PERSONAL corrected | 새 `feet=+0.2` `TERM-50` corrected parent/control과 legacy H-005~H-011의 일부 corrected Run, `AIRTIME-025` fresh 3K·continuation 및 `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch fresh 3K가 완료됐다. `AIRTIME-025`와 `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` branch는 향후 paired 평가 우선 후보이고, 나머지 상태와 서로 다른 부모·영상 checkpoint는 registry를 따른다. 과거 `feet=-0.2` Run을 clean test로 바꾸지 않는다. | [계보·상태](../14_H1_NEXT_RUN_PARAMETER_COMPARISON.md), [final 선택](../18_H1_FINALIZE_REPORT_LIMITATIONS.md) |
| `TERM-100`·HS 계획 | TERM-100(legacy H-012)은 PERSONAL HOLD. HS 질문은 PLANNED이며 실행 예약이 없다. ORIENT-100은 OFFICIAL 3K 완료·PERSONAL 행동 HOLD, ACTRATE-001도 OFFICIAL fresh3K·PERSONAL 분석 완료/HOLD이며 ORIENT 부모를 상속하지 않았다. | [가설 registry](../../../../research/EXPERIMENTS.md) |
| Go2 개인 장기·G-004 | 개인 12K 시도는 9.5K 부근 수치 발산으로 중단됐고 발산 전 `model_9500.pt`는 참고용이다. G-004 R02 공식 1K는 terrain 0의 생존형 local optimum으로 strong negative이며 3K 승격 대상이 아니다. | [Go2 분석](../07_QUADRUPED_TRAINING_CODE.md), [증거 경계](../16_EXPERIMENT_EXPORT_AND_TENSORBOARD.md) |
| Go2 `g2-submit-3 / LINTRACK-150-LINZ-2` 계보 | PERSONAL 1K/3K와 checkpoint 비교는 후보 선택 자료이지 공식 점수가 아니다. 공식 R03 fresh 5K는 약 4.8K에서 중단·validation FAIL; R04는 원본 4800에서 recovery한 별도 Run이다. 원본 4800 계열 R07 제출 snapshot은 3라운드 87.55/100을 받았다. recovery 4900과 원본 4800을 섞지 않는다. | [Go2 분석](../07_QUADRUPED_TRAINING_CODE.md), [제출 경계](../05_TRAINING_RULES_AND_SUBMISSION.md), [registry](../../../../research/EXPERIMENTS.md) |
| Go2 `g2-submit-5 / LINTRACK-125` | OFFICIAL fresh 7.5K terminal `model_7450.pt`에서 export한 policy/env/report를 2026-10-06 actual Round-5 제출했다고 사용자가 확인했다. submission Release와 Originals snapshot이 보존되고 actor/env identity를 검증했다. R5 공식 점수 88.32/100(시뮬 58.32/70·설계 20/20·리포트 10/10)과 표시 제출 시각 2026-10-06 01:10(시간대 미기재)은 2026-10-08 수신했다. 별도 receipt 파일은 미보유이며, PERSONAL C4800/C7050/C7450 비교를 공식 채점 결과나 reward causal proof로 승격하지 않는다. | [제출 경계](../05_TRAINING_RULES_AND_SUBMISSION.md), [Go2 분석](../07_QUADRUPED_TRAINING_CODE.md), [Windows 평가](../21_WINDOWS_GO2_VIDEO_AND_EVALUATION.md), [registry](../../../../research/EXPERIMENTS.md) |
| 타 팀 공개 자료·도구 | 공식 영상 OCR과 공개 실패 사례는 평가 조건이 불명확한 타 팀 관찰이다. 우리 Run의 낙상률·점수나 Optuna trial로 직접 합치지 않는다. Optuna Ask-and-Tell은 개인 PC의 후보 계산에만 허용된다. | [공개 실패](../20_H1_PUBLIC_FAILURES_AND_EXPERIMENT_PRIORS.md), [Optuna](../15_OPTUNA_REWARD_DECISION_ENGINE.md), [규정](../12_2026_UNIFIED_REGULATIONS.md) |
| 실행·보존 | headless 학습과 영상 렌더링을 구분한다. official은 로컬 evidence만 보존하며 GitHub와 상호작용하지 않는다. 최종 archive·checkpoint·로그 보존과 서버 종료 요청 경계는 각 운영 문서를 따른다. | [서버 운영](../11_SERVER_OPERATIONS.md), [CLI](../19_ISSACSIMZ_EXTERNAL_EVIDENCE_CLI.md) |

다음 H1 가설은 부모·seed·학습 길이·평가 조건을 맞춰 XY/yaw, 지형 진행·stall, 낙상·자세를 함께 비교한다. reward 가중치가 다른 Run의 총 `Train/mean_reward` 절댓값만으로 우열을 정하지 않는다. OFFICIAL 서버는 AI가 종료하지 않으며, PERSONAL 서버 종료는 사용자의 명시 요청이 있을 때만 한다.

## 해석 규칙

- 강의 설명과 실제 코드 동작을 구분하고, 코드 질문에는 파일명과 함수·클래스 이름을 함께 제시한다.
- `practice_key.bin`, `.env*`, Git 객체, ETLI 추적, USD/USDZ 등 비밀·바이너리 내용은 추측하지 않는다.
- 원본 저장소의 `official_server_runs/h1/`에는 300회, baseline 1K와 `TERM-50` 5K 공식 실행 증거가 있다. 예선 2라운드 TERM-50 제출의 공식 점수는 `13`에 있다. TERM-50 학습 묶음에는 여전히 train stdout/stderr 전체가 없으므로 완전한 운영 진단으로 취급하지 않는다.
- 원본 저장소의 `official_server_runs/go2/`에는 baseline 1K complete bundle과 legacy `G-004 ANG-STAB`(아주 오래된 alias `G5`) official 1K train archive·받은 최종 산출물이 있다. 해당 Release의 archive·env·model·video·report 원격 digest는 로컬 SHA-256과 일치한다.
- 이 폴더 안에 남아 있을 수 있는 과거 경로 표기(`data/raw`, `corpus`, `archive`)는 당시 생성 시점의 메타데이터다. 현재 저장소 구조는 이 문서와 저장소 루트의 `PROJECT_CONTEXT.md`를 따른다.
