# 새 분석 자료 수신함

이 폴더는 새 자료의 검토 공간과 수신 원문 보존 위치다. `inbox`와 `reviewed`를 구분하며, 여기 보관됐다는 사실만으로 핵심팩 미반영 또는 반영 완료를 판단하지 않는다. `data/processed/ai_library/`에는 검토한 요약과 출처를 통합하며, 현재 핵심팩은 최상위 Markdown 21개(`00`~`08`, `10`~`21`)다. 파일 수 상한보다 근거의 중복·신뢰·탐색성을 우선한다.

## 전체 수신 파일 탐색

- [2026-10-17 joint tracking model4950 분석 ZIP](../experiments/h1/analysis/2026-10-17_H1_JOINT_TRACKING_MODEL4950_POLICY_REVIEW.md): 원본 ZIP·15파일 보존, CSV/validation 본문 대조/HOLD. AI 핵심팩 00/14/20/21 반영. 기존 LINTRACK0654950과의 CPU raw 비교·새 GPU 작업 없음.

- [2026-10-17 action=-.0002 model2950 분석 ZIP 수납](../experiments/h1/analysis/2026-10-17_H1_ACTION0002_MODEL2950_POLICY_REVIEW.md): 원본 ZIP·내부14파일 보존, CSV/validation 본문 대조·HOLD. H3 world 잔류의 해석을 별도 보정했으며 상대 비교·원문 수정·GPU 실행 없음. AI 핵심팩 00/14/20/21 반영 완료.

- [2026-10-16 action=-.0003 model2950 보고서 수납](../experiments/h1/analysis/2026-10-16_H1_ACTION0003_MODEL2950_POLICY_REVIEW.md): 원문 bytes 보존, 식별·3072행/diagnostics 확인, HOLD. 후속 요청에 따라 AI 핵심팩 00/06/14/15/20/21 및 가이드에 반영했다.

- [2026-10-16 angxy=-.08 정책 보고서 수납·CPU 비교](../experiments/h1/analysis/2026-10-16_H1_ANGXY008_MODEL4650_POLICY_REVIEW.md): 원문 bytes 보존·AI 핵심팩 반영/HOLD, 기존 5정책 raw 비교 완료.

- [2026-10-15 lin=.55 후속 보고서 수납](../experiments/h1/analysis/2026-10-15_H1_LINTRACK055_MODEL4650_POLICY_REVIEW.md): OFFICIAL 학습·PERSONAL 평가·분석 완료, 범용 후보 HOLD. [기존 가설 재심사](../experiments/h1/analysis/2026-10-15_H1_NEXT_HYPOTHESIS_DECISION_INTAKE.md)의 action=-.0003 resume/fresh 후보는 미선택이다. [Optuna v2](../operations/2026-10-15_OPTUNA_PC_ASK_TELL_V2_INTAKE.md)는 별도 수신·정적 검토 완료, 실제 Tell·운영 최적화 미준비다.

- [기타 수신 통합 안내](other/README.md) · [2026-10-12 기준 검토 원문 63개 + 이후 추가 수신 탐색](other/reviewed/README.md) · [미검토/inbox 파일 5개 색인](other/inbox/README.md)
- [2026-10-12 당시 수신 원문 63개 참조 추적 장부](REPORT_PROVENANCE_TRIAGE.md): 원문별 참조 수준과 현재 집계는 이 장부를 따른다. metadata/본문 출처와 문맥 대조를 구분하며, 핵심팩 반영률이 아니다.
- [원문 ↔ 후속 해석 관계 14쌍](REPORT_CROSSWALK.md): `extends`와 `intake_interpretation`을 구분한 **선별적** source-to-interpretation 안내. 2026-10-12 원문 63건과 추가 수신의 전체 통합률이 아니다.
- OT 전사·분석은 [OT 기준 안내](ot/README.md)를 따른다. 원본 보존과 `reviewed` 통합 완료는 다르다.

**2026-10-15 후속:** [ACTION 복원 4650 원문](other/reviewed/H1_MODEL4650_POLICY_ANALYSIS_20261015.md) · [LINTRACK-065 fresh4950 원문](other/reviewed/H1_LINTRACK-065_POLICY_ANALYSIS_20261015.md)은 보존·해석 완료, [H1 분석 수납](../experiments/h1/analysis/2026-10-15_H1_MODEL4650_LINTRACK065_POLICY_REVIEW.md)과 기존 21개 AI 핵심팩 일부에 반영됐다. 두 정책 모두 **HOLD**다. 이들은 2026-10-12 당시 63건 원문 전수조사에 **포함되지 않은** 새 수신 문서다.

## 배치 규칙

- `ot/transcripts/`: OT 영상에서 추출한 오디오 전사 원문과 정리본
- `ot/analyses/`: 장면·발화·규정·기술 내용을 개별적으로 분석한 문서
- `ot/synthesis/`: 쓰지 않음. OT 통합 분석은 `ot/analyses/`에 있다.
- `other/inbox/`: 출처·품질·최신성이 아직 확인되지 않은 기타 분석 자료
- `other/reviewed/`: 검토가 끝난 기타 근거 문서. 핵심팩 반영 여부는 각 문서와 `00_START_HERE`에서 확인

사용자가 제공한 장문 통합정리는 검토 후 [NCRC 2026 검증된 프로젝트 현황](./other/reviewed/NCRC_2026_검증된_프로젝트_현황.md)으로 정제했다. 확인되지 않은 로컬 환경·과거 대화·시간 추정·예시 결과는 제거했으며, 원문은 Git 이력에 남아 있다. `data/processed/planning/historical/05_PROJECT_STATUS_AND_EVIDENCE_BASED_STRATEGY.md`는 **2026-08-24 당시 historical/superseded 전략**이다. 현재 실험·실행 판단은 [Experiment registry](../../../research/EXPERIMENTS.md), [현재 컨텍스트](../../../PROJECT_CONTEXT.md) 및 실제 실행 문서를 따른다.

현재 수신한 2026 온라인 설명회 전사·자막·저신뢰도 검증 자료의 관계는 `ot/README.md`를 따른다.

공식 서버·개인 검증환경에서 실제로 생성된 산출물의 분석은 수신함이 아니라 `data/processed/experiments/`에 둔다.

## 관련 보고서와 반영 상태

같은 Run·checkpoint를 다룬 후속 분석이라도 `extends`(범위 확장)와 `supersedes`(명시적 대체)를 구분한다. `reviewed`는 검토 단계이지 AI 핵심팩 반영 완료를 의미하지 않는다. 보조 색인 [RELATIONSHIPS.md](RELATIONSHIPS.md)는 **조회 편의용**이며 원본 Markdown·Experiment registry를 대신하지 않는다. 근거가 확인되지 않으면 상태를 `unknown`으로 남긴다.

## 핵심팩 반영 규칙

새 자료가 신뢰할 만하면 독립 파일을 계속 추가하지 말고, 가장 가까운 `ai_library` 문서에 근거와 함께 통합하거나 기존 파일을 교체한다. 핵심팩의 현행 구성은 21개이며 독립 파일을 추가할 때 [구성 가이드](../../../docs/AI_LIBRARY_GUIDE.md)를 확인한다. 원본 영상·오디오·이미지·에셋은 이 저장소가 아니라 `../naver-issacsim-originals/data/raw`에 보관한다.
