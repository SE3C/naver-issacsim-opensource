> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/research/experiments/h1/README.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# H1 Experiment 디렉터리 안내

- [전진 planar tracking + action fresh 조합](<exp-h1-action-planar-tracking-fresh-interaction.md>): 사용자 후보3 OFFICIAL fresh3K 완료/PASS; model2850 평가 SHA는 train index와 일치, 행동 분석 대기.
- [회전 우선 planar/angular tracking 조합](<exp-h1-rotation-priority-tracking.md>): 사용자 후보1 OFFICIAL fresh3K 완료/PASS; 최신 keeper2950, 정책 평가 대기.
- [joint tracking + 자세·고관절 완화](<exp-h1-joint-tracking-posture-relaxation.md>): 사용자 후보2 OFFICIAL fresh3K COMPLETED/PASS, model2850 PERSONAL 6영상·full 평가 완료. 최신 keeper2950과 구분; 행동 보고서 수신/HOLD.

- [joint tracking balance](<exp-h1-joint-tracking-balance.md>): lin=.65 / ang=.60 / action=-.0003 OFFICIAL fresh5K 완료/PASS. 실제 Run과 keeper4950/auto-best4800 구분; 행동 평가·분석 대기.

**2026-10-14:** [action-airtime fresh](<exp-h1-action-airtime-fresh-interaction.md>), [action-feet_slide fresh](<exp-h1-action-foot-contact-stability.md>)가 OFFICIAL 학습/PERSONAL 평가 완료로 전환됐다. 옛 planned 문서는 계획 당시 원문으로 보존하며 현재 미실행 질문은 네 건이다.

- [현재 Experiment / Run registry](<../../EXPERIMENTS.md>): 학습 실행 완료·중단·판정의 canonical 표. 완료된 학습/평가 질문은 이 폴더 최상위의 `exp-h1-*.md`에 둔다.
- [기존 계획 자료 6건](<planned/README.md>): 계획 수립 당시 여섯 질문의 역사적 탐색 주소. **2026-10-14 기준 실행된 fresh 조합 2건은 최상위 Experiment 문서로 전환됐으며, 남은 미실행 질문은 4건**이다. 실제 상태는 registry 우선. legacy HS-001/002는 미실행 schedule. 이 폴더 이름만으로 실행 승인·새 Run ID를 만들지 않는다.
- `H-001`–`H-012`는 역사적 **식별자**이지만 실제 Run/evidence의 계보가 들어 있으므로 기존 파일명을 유지한다. 이를 모두 historical로 이동하면 원본 연결을 오히려 깨뜨릴 수 있다.
- [현행 이름 규칙](<../../EXPERIMENT_NAMING.md>) · [제출 설정](<../../submission_presets/README.md>): 제출 preset은 Experiment가 아니며 actual Run·평가·출처를 분리해 읽는다.

**2026-10-12 분류 유의:** 다섯 `ACTRATE-0001` 조합 연구 질문 중 `exp-h1-action-first-planar-tracking-switch`는 OFFICIAL resume 학습 완료/PASS 및 PERSONAL 평가 완료/행동 HOLD이므로 planned에 분류하지 않는다. 그 외 4건은 아직 Run이 발급되지 않았다. 어떤 질문의 상태가 바뀌면 registry를 우선한다.
