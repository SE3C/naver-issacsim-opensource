# Stage 4 — 수신 원문↔해석 문서 관계 분류 (2026-10-12)

- 선별된 관계 12건을 [REPORT_CROSSWALK.md](../../data/processed/incoming/REPORT_CROSSWALK.md)로 조회한다. 각 연결에 존재하는 원문/후속 문서와 출처 역할을 구분하고, 원본을 변경하지 않는다.
- 유형별 건수: `extends` 2, `intake_interpretation` 7, `experiment_context` 1, `transcript_to_analysis` 2. `supersedes` 강제 분류 0건.
- H1 ACTRATE-001/ORIENT-100의 동명 `model_2850` 식별 충돌, OFFICIAL/PERSONAL/실제 제출·채점, Go2 7050 PERSONAL 비교와 7450 공식 제출 차이를 명시한다.
- 오직 새 noncanonical Markdown 색인·상위 안내 링크·검사 대상만 변경한다. 수신 원문 63개·inbox 5개·실험 원본 H1 48개/Go2 28개와 RAW 자료 byte는 유지한다.
- 등록된 경로는 새 색인 생성 전 현재 Draft branch Git tree에서 검사했다. Markdown anchor/외부 URL/원본 ZIP 실물까지 이번에 검사했다는 뜻은 아니다.

## 변경 반영 후 확인

- 12개 source-to-interpretation 관계를 담은 새 표의 **Markdown 링크 31개 모두** 검토 브랜치 Git tree에서 대상을 찾았다.
- 동일 브랜치의 **변경 Markdown 83개 / 상대 링크 999개**를 정적 검사하여 누락 파일 경로 **0건**을 확인했다. 외부 URL·마크다운 heading fragment/앵커·실제 런타임은 확인하지 않았다.
- `main` 대 검토 브랜치 비교: `incoming/other/reviewed/` 기존 64개 파일(README + 63 수신 자료) 원본 blob SHA가 모두 동일, `incoming/other/inbox/` 기존 6개 파일도 동일, Go2 `experiments/go2/` 기존 28개 파일도 동일하다.
- H1 `experiments/h1/`의 원래 48개 중 달라진 것은 앞선 3차 단계에서 이동 안내로 바뀐 `2026-09-27_H1_PERSONAL_FRESH_AND_CONTINUATION_PLAN.md`와 해당 계획의 canonical 경로를 보정한 `2026-09-27_H1_FRESH_AND_CONTINUATION_EVIDENCE_INTAKE.md` 두 경로뿐이다. 실제 원문 사전 계획은 `planning/historical/`에 있고 4개 상대 링크 외에는 본문이 동일함이 3차에서 검증됐다.
- 이 관계표는 12건의 선별 사례이며 `reviewed` 63개 전체의 원인관계 전수 감사가 아니다. Run provenance, 종결/채택/제출 판정의 최종 기준은 별도 registry와 evidence다.
