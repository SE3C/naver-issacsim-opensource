> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/docs/AI_LIBRARY_GUIDE.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# 대회 대비 AI 라이브러리 구성 가이드

**2026-10-17 joint tracking 후속:** [lin=.65/ang=.60/action=-.0003 keeper4950 보고서 수납](<../../../../reports/experiments/h1/analysis/2026-10-17_H1_JOINT_TRACKING_MODEL4950_POLICY_REVIEW.md>)을 핵심팩 00/14/20/21에 흡수했다. 학습·PERSONAL 평가·보고서는 완료/HOLD이며 기존 LINTRACK0654950과 다른 SHA다. 원문 ZIP/15파일을 보존하고 핵심팩21개·history 제외 전달 원칙을 유지한다. 상대 raw 비교·공식 제출/점수는 새로 확인되지 않았다.

## 2026-10-16 action=-0.0003 fresh3K 후속 반영

[실제 Run·보존 원문·검토](<../../../../reports/experiments/h1/analysis/2026-10-16_H1_ACTION0003_MODEL2950_POLICY_REVIEW.md>)를 기존 핵심팩 00/06/14/15/20/21에 흡수했다. OFFICIAL Run `20261016-033023-h1-actrate-0003-fresh3k` 완료/PASS, keeper2950의 PERSONAL 평가3072행 및 정책 보고서 수신 완료/HOLD다. fresh를 미실행이라고 안내하지 않으며, -.0003 resume는 별도 미실행이다. 원문·기존 archive/Release는 변경하지 않고 핵심팩21개를 유지한다. 상대 정책 CPU 비교·공식 점수·Optuna Tell이 완료됐다는 뜻은 아니다.

**lin=.55 후속 완료:** Run `20261015-105910-h1-actrate0001-lintrack-055-from2700-plus2k`는 OFFICIAL resume +2000, seed42/4096env, console4699/4700, COMPLETED/exit0/validation PASS다. 부모2700 SHA `e54d3389…93ca7ae`에서 lin .50→.55만 변경(action=-.0001, feet=.20, termination=-50 유지), 최종 preset-relative override는 `h1-submit-2 + lin=.55 + action=-.0001`다. 최신 indexed keeper `model_4650.pt` SHA `e8a358a50832f6653b1e558788a5a676ab9a849d3ec6c64e3ed2430e9ff41814`의 PERSONAL Windows 6영상·scenario7 평가도 COMPLETE(128env×3seed×8case,3072행)로 수납했다. console 종점4699와 keeper4650은 다르다. 원본 parent/source IDs=null·imported provenance=false는 유지하며 별도 SHA로 연결한다. **정책 분석 수납 완료·범용 후보 HOLD, 공식 점수·제출 아님**. [분석 원문·계보·한계](<../../../../reports/experiments/h1/analysis/2026-10-15_H1_LINTRACK055_MODEL4650_POLICY_REVIEW.md>). [학습 Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261015-exp-h1-action-first-planar-tracking-switch-lin055-resume2700-plus2k) · [평가 Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261015-exp-h1-action-first-planar-tracking-switch-lin055-model4650-video-eval). action=-.0003 fresh는 2026-10-16 실제 Run 완료·보고서 HOLD로 갱신됐고 resume만 별도 미실행이다. Optuna v2의 objective/comparison 미승인·Tell 차단은 별개다.

## 2026-10-15 두 H1 정책 행동 분석 반영

새 H1 MD 2개는 **21개 상담 핵심팩을 늘리지 않고** `data/processed/incoming/other/reviewed/`에 원문을 보존했다. [2026-10-15 두 정책 행동 판정](<../../../../reports/experiments/h1/analysis/2026-10-15_H1_MODEL4650_LINTRACK065_POLICY_REVIEW.md>)을 새 파생 검토로 기록하고, 기존 `00`, `06`, `14`, `21` 및 `research/EXPERIMENTS.md`의 요약을 최신화했다. 복원 action-rate `model_4650`와 LINTRACK fresh5K `model_4950`은 서로 다른 OFFICIAL Run의 별도 PERSONAL 후속 평가이며 둘 다 HOLD. 기존 동명 `model_4650`의 checkpoint SHA까지 구분한다. 제공 원문이 수행했다고 기록한 ZIP/MP4 재분석을 이번 Git 반영자가 새로 수행했다고 주장하지 않는다. 같은 부모 unchanged+2K 평가 raw와 TERM-50 보존 raw가 다음 CPU 대조 1순위다. 기존 문서 중 과거 ‘분석 대기’는 보고서 수납 이전 상태다.


## 상담 AI 핵심팩 — 현재 21개

상담용 AI에는 `data/processed/ai_library/`의 Markdown 21개를 업로드한다. 이 폴더의 자료는 강의, 단일 통합 규정집, 현재 서버 코드·엔진 분석, 운영 청사진, OT 판단과 공식·개인 서버 실험 자료를 주제별로 통합한 결과다.

- 현재 구성: **21개** (`00`~`08`, `10`~`21`; `09`는 핵심팩 밖)
- Downloads 전달본에는 현재 핵심팩 전체를 복사하되 `_history`·`history` 폴더는 제외한다. 역사 원문은 저장소에서 보존하고, 복사본의 파일 수는 제외 후 기준으로 확인한다.
- `00_START_HERE_CONTEXT_AND_MAP.md`를 항상 함께 넣는다. 그 파일의 `_history/` 링크는 이전 상세 기록을 조회하기 위한 보존본이며 21개 최상위 업로드 대상에 포함하지 않는다. 현재 H1 Round-6 `h1-submit-6` 제출 상태는 registry 및 제출 preset을 우선하고, 정책 분석의 별도 HOLD를 변경하지 않는다.
- 새 명명은 [Experiment naming](<../../../../research/EXPERIMENT_NAMING.md>)의 submission preset·Experiment 질문·실제 학습 Run·override·lineage 구분을 따른다. `H/HS/G/GS-xxx`와 registry `Rxx`, 옛 `A1`·`TERM50`·Go2 `G5`는 기존 자료 검색용 legacy 주소다. 옛 `S1–S4`는 9/12 제안서와 9/13 실행 분석본에서 다른 뜻이므로 출처 없이 매핑하지 않는다. HS-001/002는 미실행 계획이며 새 번호를 발급하지 않는다.

최근 공식 서버 실험 정보는 새 파일로 늘리지 않고 다음처럼 기존 핵심 문서에 흡수한다.

- `00`: 현재 상태, 근거 우선순위, 다음 행동을 한눈에 보는 입구
- `06`: H1 reward 코드·과거 실행 해석·완료된 `ORIENT-100` OFFICIAL 3K·PERSONAL 행동 HOLD
- `10`: evaluator·Optuna로 넘어가기 전 비교 원칙과 실험 순서
- `11`: headless 실행, 전체 로그 export, 서버 운영·증거 보존
- `13`: H1 공식 서버 baseline·`TERM-50` 5K·`h1-submit-4 / AIRTIME-025` fresh 10K 및 Round-4 평가 근거
- `14`: H1 corrected lineage 비교·Round-4 이후 우선순위·ORIENT 단일 정책 평가 결과·matched 비교 프로토콜
- `15`: Optuna reward 의사결정 엔진
- `16`: 전체 run export·TensorBoard 복원·Go2 LINTRACK-125 exact-trajectory 비교 규칙
- `17`: `issacsimz` 영상 실행, PERSONAL 6지형 suite와 OFFICIAL native `play.py` 수동 6지형 절차
- `18`: H1 finalize/report 자동 선택·경고·checkpoint cleanup의 검증된 한계
- `19`: `issacsimz` 외부 evidence CLI, personal checkpoint mirror와 official 비활성 경계, archive·smoke·게시 경로
- `20`: 공개 H1 실패 사례의 관찰 근거와 내부 가설을 구분하는 prior·Round-4 이후 H1 실험 우선순위
- [`21`](<../data/processed/ai_library/21_WINDOWS_GO2_VIDEO_AND_EVALUATION.md>): Windows Go2/H1 고정 6영상·개별 평가와 통합 ZIP 운용. 단일 최종 ZIP은 full evaluation에서만 만들고 smoke는 제외하며, A/B 비교 보고서는 포함하지 않는다. Windows 실행 도구의 Git 소스·설치 절차와 2950·7050 실제 통합 ZIP 검증도 이 문서를 따른다.

## 날짜별 역사 기록의 적용 범위

아래 2026-10-07 `ORIENT-100` 사례는 당시의 흡수 기록이다. 새로운 H1 `ACTRATE-0001` fresh10K와 Round-6 제출 여부를 판단할 때는 [최신 registry](<../../../../research/EXPERIMENTS.md>) 및 [Round-6 snapshot](<../../../../research/submission_presets/README.md>)을 먼저 확인한다. 기존 세 제출이라는 역사적 표현을 모든 발급 preset의 현재 개수로 쓰지 않는다.

## ORIENT-100 당시 분석의 흡수 범위 (역사적 2026-10-07 기록)

아래는 수납 당시 기록이며 현재 비교 가용성을 뜻하지 않는다. 2026-10-10 [3정책 raw 후속 비교](<../../../../reports/experiments/h1/analysis/2026-10-10_H1_SCENARIO7_RAW_3POLICY_MATCHED_ANALYSIS.md>)에서 TERM-50 대조 자료를 직접 확인했다. ACTRATE-001도 [별도 완료 Run과 HOLD 검토](<../../../../research/experiments/h1/exp-h1-action-rate-smoothing.md>)가 있으므로 아래 PLANNED 표현을 현재 상태로 사용하지 않는다.

- 분석 원문 canonical: [H1 ORIENT-100 model_2850 정책 분석](<../../../../reports/received/H1_ORIENT-100_POLICY_ANALYSIS_20261007.md>). 별도 핵심팩 22번째 파일로 만들지 않는다.
- Experiment/Run/HOLD 판단: [현재 registry](<../../../../research/EXPERIMENTS.md>)와 [질문별 기록](<../../../../research/experiments/h1/exp-h1-rough-terrain-orientation-relaxation.md>). OFFICIAL fresh 3K 완료와 Windows PERSONAL 단일 정책 진단을 분리한다.
- 핵심팩 `00`, `06`, `10`, `11`, `13`~`21` 중 해당 주제에는 직접 재사용 가능한 사실만 요약했다. H1 `model_2850`의 3,072/3,072 생존은 유효하지만 정지 +1.633m/횡이동 +1.180m 비의도 전진과 rough 하위 꼬리, 계단 통과 미입증 때문에 **행동 선택 HOLD**; `h1-submit-2` 동일 조건 대조가 없어 reward 효과·OFFICIAL 점수·승격은 미확정이다.
- **문서 정합성 원칙:** 역사적 계획의 날짜와 미실행 당시 표현은 보존하되, 현재 판단은 위 registry·10/07 원문을 우선한다. `ACTRATE-001`은 별도 PLANNED Experiment이며, 영상은 camera-off 평가와 다른 episode다.

## 새 분석의 반영 규칙

새 자료는 곧바로 핵심팩에 추가하지 않고 `data/processed/incoming/`에서 검토한다. 실제 실행 근거는 로봇별 `experiments/*/training/`, 사후 평가·해석은 `experiments/*/analysis/`에서 확인한다. NVIDIA 보조평가도 분석이다. 정책 연결표〔원본 참조: `../data/processed/experiments/RECENT_POLICY_LINKS.md` / 공개 사본 미포함〕는 탐색용이며 현재 판정은 registry를 따른다. 기존 21개 중 가장 가까운 주제의 문서를 먼저 보완·교체하되, 반복해서 참조할 독립 주제이거나 기존 문서가 과도하게 길어질 때만 구성을 다시 검토한다. 숫자 제한보다 중복·출처·신뢰 구분을 우선한다.

## 업로드에서 제외할 자료

- `data/processed/lessons/`, `codebase/`, `server_backup/`, `planning/`, `experiments/`의 세부 원문
- `data/processed/external_analysis/`의 요청 목록과 미검토 자료
- `data/processed/reference/game_engine/09_GAME_AGENT_NAVIGATION_SENSORS.md`의 게임 에이전트·경로계획 참고 분석 — 현재 H1/Go2 학습·증거 판단의 핵심 근거가 아님
- `inventory.json`, JSONL 목록, 재생성 가능한 인덱스, 이전 변환본

사실 충돌 시 원본 아카이브와 현재 서버 코드 분석을 우선하고, 기획·OT·외부 분석은 권장안 또는 추론으로 구분한다.
