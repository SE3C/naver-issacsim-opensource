# AI 프로젝트 컨텍스트 — 2026-10-12 정리 전 보존본

정리 전 Git blob SHA: `ac52a039bf8dafdd61295366d057beb132cf5015`. Git revision: `517a310d39746a9ffb38d8d93c04c0cdf9453802`. 상대 Markdown 링크만 archive 위치에 맞게 수정했습니다. 수신·실험·제출 상태는 기록된 당시 시점을 뜻하며 [현재 registry](../../research/EXPERIMENTS.md)를 우선합니다.

---

# AI 프로젝트 컨텍스트

## 목적

이 프로젝트는 NAVER CONNECT Robotics Cup의 Isaac Sim·Isaac Lab 교육자료, 연습 시뮬레이터 코드, 서버 워크스페이스 백업을 AI가 검색하고 설명할 수 있는 형태로 정리한 지식 베이스다.

## 신뢰 순서

1. `../naver-issacsim-originals/data/raw`: 저장 당시의 원본 HTML·코드. 사실 확인의 최종 근거다.
2. `data/processed/ai_library/12_2026_UNIFIED_REGULATIONS.md`: 일반·예선·본선 규정과 공식 Q&A를 정리한 단일 규정 기준이다. 일정·마감은 최신 공지를 확인한다.
3. `data/processed/lessons`, `glossary`, `codebase`, `reference`: 원본을 읽기 쉽게 변환하거나 공식 자료를 분석한 참고 자료다.
4. `data/processed/external_analysis`: 사용자가 제공한 별도 분석본과 영상 전문이다. 유용한 추론을 포함하지만 원본 코드와 충돌하면 원본을 우선한다.

## AI 해석 규칙

- 강의 설명과 코드베이스의 동작을 구분한다. 강의는 교육자료이고 `../naver-issacsim-originals/data/raw/codebase`는 본선 연습 시스템 관련 코드다.
- 코드 질문에는 관련 파일명과 함수·클래스 이름을 함께 제시한다.
- 영상 내용은 URL과 제목만으로 추측하지 않는다. 외부 분석 결과가 들어오기 전에는 `분석 대기`라고 표시한다.
- 단어 사전은 저장된 첫 페이지 15개만 포함한다. 원본 화면의 전체 개수 556개와 혼동하지 않는다.
- 이미지 속 내용은 파일명만으로 추론하지 않는다. 필요한 경우 외부 이미지 분석을 요청한다.
- 답변에 근거 문서의 `id` 또는 `source`를 함께 남긴다.
- 서버 백업에서는 `training`, `practice_sim`, `examples`를 프로젝트 자료로 우선한다. `IsaacLab`은 벤더 프레임워크라 코퍼스에서 제외되어 있다.
- 현재 H1·Go2 학습/재생 코드의 기준은 Originals에 보존한 2026-09-13 공식 `/workspace/training` snapshot과 동기화된 NVIDIA `training/`이다. 더 오래된 `server_backup/extracted`는 당시 코드의 비교 자료로 사용한다. 차이 목록은 서버 백업 `inventory.json`의 `legacyCodebaseComparison`을 본다.
- `practice_key.bin`, `.env*`, Git 객체, ETLI 추적, USD/USDZ 및 기타 바이너리 내용은 인벤토리만 참고하고 비밀이나 내부 내용을 추측하지 않는다.
- 정적 `server_backup` 스냅샷에는 학습 산출물이 없지만, 원본 저장소의 `data/raw/official_server_runs/h1/2026-08-24_124413_baseline_300iter/`에는 첫 H1 실행의 `model_best.pt`, `env.yaml`, `policy.pt`, ONNX, report, MP4가 보존돼 있다. 전체 콘솔·TensorBoard·GPU 로그는 없으므로 완전한 진단 묶음으로 간주하지 않는다.
- 경기 엔진의 버그·불일치 후보는 `UNIFIED_ANALYSIS.md`의 정적 분석 결과다. 실제 운영 backend나 최신 대회 빌드에서 수정됐을 가능성을 함께 표시한다.
- `data/processed/planning`은 구현·평가·서버 운영 권장안이다. 코드 확인 사실과 제안이 섞여 있으므로 공식 규정이나 원본 코드보다 우선하지 않는다.
- `data/processed/experiments`는 실제 실행 산출물의 검토 결과다. 측정값·계산값·미보관 관찰값의 등급을 유지하고, 짧은 실행 결과를 장기 정책 성능으로 확대하지 않는다.
- 상담 AI 핵심팩은 `data/processed/ai_library/`의 21개(`00`~`08`, `10`~`21`)다. 게임 에이전트·경로계획 참고 분석 `09`는 `data/processed/reference/`에 보존한다. 현재 상태 표는 `00_START_HERE_CONTEXT_AND_MAP.md`가 입구다. Windows Go2 고정 6영상·개별 평가의 실제 검증 기록은 [21번 운영 문서](../../data/processed/ai_library/21_WINDOWS_GO2_VIDEO_AND_EVALUATION.md)를 따른다. 동일 구조의 H1 Windows companion source는 `../naver-issacsim-eval/WINDOWS_H1_WORKFLOW.md`에 있으며 2026-10-04 시점에는 H1 GPU full evidence가 없었으나, 2026-10-07 `ORIENT-100 / model_2850.pt`의 Windows PERSONAL 6영상 + `scenario7` full(3,072 episode, 20초 생존/종료 0) 자료가 확보됐다. **H1 matched A/B·공식 평가 점수는 여전히 없다.** [원문 분석](../../data/processed/incoming/other/reviewed/H1_ORIENT-100_POLICY_ANALYSIS_20261007.md)과 [실험 판정](../../research/experiments/h1/exp-h1-rough-terrain-orientation-relaxation.md)을 참고한다. 두 로봇 모두 full 성공 시 단일 최종 ZIP은 6개 지형 영상과 개별 평가 산출물을 묶고 smoke에는 만들지 않으며, 기존 영상 ZIP·receipt는 보존하고 A/B 보고서는 기본 산출물에 포함하지 않는다. 실행 도구·설치기의 재현 가능한 Git 소스는 `../naver-issacsim-eval`이다.
- 새 실험 명명은 `research/EXPERIMENT_NAMING.md`가 기준이다. 제출 preset, 검증 질문인 Experiment, 실제 학습 Run, 최종 override와 부모 checkpoint lineage를 구분한다. 기존 세 제출의 전체 native env/agent 설정은 `research/submission_presets/`에 동결했고 원본 archive는 Originals에 그대로 둔다. 2026-10-06 사용자가 실제 Go2 Round-5 제출을 확인해 `g2-submit-5 / LINTRACK-125` 이름을 발급했으며, 제출 env/policy/report snapshot은 보존됐다. 다만 full preset의 native `agent.yaml`은 OFFICIAL 7.5K archive에서 byte-for-byte 추출하기 전까지 별도 preset 디렉터리를 합성하지 않는다. 기존 `H/G/HS/GS`와 `Rxx`는 원본을 찾기 위한 legacy 주소이며 새 번호를 발급하지 않는다. 현재 판단은 `research/EXPERIMENTS.md`를 따른다.
- 공식 H1 원본은 Originals `official_server_runs/h1/`의 300회, baseline 1K, `h1-submit-2 / TERM-50` fresh 5K(legacy H-001 R02), `h1-submit-4 / AIRTIME-025` fresh 10K evidence Run `20260927-123428-h005-fresh10k-official`(legacy H-005 R05)다. `h1-submit-4 / AIRTIME-025`는 4라운드 제출 snapshot과 공식 평가까지 수신했고, 시뮬레이션 56.37/70·설계 의도 20/20·리포트 품질 10/10, 구성 점수 합계 86.37/100이다. 포털 수령증·정확한 제출 시각과 제출 `policy.pt`의 정확한 numbered checkpoint 연결은 아직 없다. Go2 공식 baseline 1K, `ANGXY-012` 1K(legacy G-004), `g2-submit-3 / LINTRACK-150-LINZ-2` 계보의 interrupted fresh/recovery/original-4800 submission export도 `official_server_runs/go2/`에 구분해 보존한다. 이후 `LINTRACK-125` OFFICIAL fresh 3K와 별도 fresh 7.5K도 수신·분석됐고, 두 Run의 첫 3K TensorBoard scalar 22개와 공통 checkpoint 60개가 exact match한다. 이 비교는 추가 학습량 효과를 강하게 보여 주지만 BASE 대비 reward 인과효과는 HOLD다. 2026-10-05 PERSONAL 3정책 비교는 `g2-submit-3` original 4800, 7.5K automatic-best `model_7050.pt`, terminal `model_7450.pt`를 동일 `scenario7` protocol과 고정 6영상 조건에서 비교해 **7450을 내부 행동 주후보 PROMOTE, 7050을 안전성 fallback HOLD, 4800을 현재 all-around 후보 기준 REJECT**로 판정했다. 이후 terminal 7450은 `g2-submit-5 / LINTRACK-125`로 export되어 2026-10-06 사용자가 실제 Round-5 제출 완료를 보고했고, [submission Release](https://github.com/SE3C/naver-issacsim/releases/tag/submission-go2-prelim-r5-20261006)에 policy/env/기술개선 리포트 snapshot이 보존됐다. 제출 `policy.pt` actor는 native 7450과 exact-match이고 env도 OFFICIAL 7.5K record와 일치한다. R5 공식 평가와 표시 제출 시각은 2026-10-08 수신했다: 2026-10-06 01:10(시간대 미기재), 88.32/100 = 58.32/70 + 20/20 + 10/10. 별도 포털 receipt 파일은 미보유이며, 앞선 PERSONAL 진단 자체를 공식 점수나 `LINTRACK-125` reward 인과효과로 바꾸지 않는다. H1 2라운드 점수는 86.37/100, Go2 3라운드 점수는 87.55/100이며 각 근거는 `research/EXPERIMENTS.md`의 OFFICIAL Run과 제출 기록을 따른다. 과거 `feet=-0.2` legacy H-005~H-011 개인 계보는 역사적 상대 비교용이다. 새 `feet=+0.2` corrected PERSONAL 계보와 `AIRTIME-025` fresh/continuation, `track_lin_vel_xy_exp=0.75`, `feet_air_time=0.25` fresh branch은 PERSONAL에서 완료됐으며 `exp-h1-stable-first-track-switch`·`exp-h1-track-first-stability-switch`와 같은 부모 control은 미실행 계획이다.
- 개인 Go2 12k 시도의 벽시계 실측은 `experiments/go2/2026-09-11_GO2_12K_WALLCLOCK_FROM_LOG.md`다. A1 fresh 3K 완료 분석은 `incoming/other/reviewed/GO2_A1_1K_3K_VIDEO_FULL_EVIDENCE_ANALYSIS_20260914.md`다. 둘 다 개인 L40S 자료이며 공식 서버 결과가 아니다.
- `issacsimz` CLI 사용법·공식 Go2 정상 완료 실전 검증 범위와 H1·장애·resume 검증 경계는 `ai_library/19_ISSACSIMZ_EXTERNAL_EVIDENCE_CLI.md`다.

## 추천 검색 파일

Go2 R3/R5의 최신 판단 근거는 [운영진 Survival/Tracking 답변 분석](../../data/processed/experiments/go2/2026-10-08_GO2_R3_R5_OFFICIAL_SCORE_COMPONENTS_ORGANIZER_REPLY.md)이다. 사용자 제공 DM에 따르면 공식 계단 survival **99.0%→99.8%**는 개선됐으나 Tracking Score **0.819→0.796** 손실이 더 커 계단 점수는 **8.52→8.35**로 하락했다. 학습 contact와 공식 survival을 환산하지 않고, 로컬 지표 개선을 공식 tracking 개선으로 바꾸지 않는다. 공식 구성 기여는 확인됐지만 reward 인과와 로컬·공식 역전 메커니즘은 아직 미확인이다. 후속 질문은 개선된 생존을 유지하며 명령 추종 손실을 회복할 수 있는가다.

일반 질의는 관련 `data/processed` 문서를 직접 확인한다. 서버 백업 분석은 `data/processed/server_backup/reports/UNIFIED_ANALYSIS.md`, 전체 구조는 `reports/OVERVIEW.md`와 `catalog/inventory.json`에서 확인한다. 외부 AI 라이브러리에 올릴 파일 선택은 `docs/AI_LIBRARY_GUIDE.md`를 따른다.
