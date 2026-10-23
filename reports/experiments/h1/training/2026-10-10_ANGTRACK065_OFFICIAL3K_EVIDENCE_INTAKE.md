> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/experiments/h1/training/2026-10-10_ANGTRACK065_OFFICIAL3K_EVIDENCE_INTAKE.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# [학습] H1 ANGTRACK-065 — OFFICIAL fresh 3K training evidence

> 관리 안내 (2026-10-13): **학습** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](<../../../../research/EXPERIMENTS.md>)를 확인한다.

Experiment: `exp-h1-angular-tracking-boost`; question: can higher angular tracking weight improve yaw/combined tracking without unacceptable XY, terrain and fall costs?

- Run `20261009-155344-h1-angtrack-065-fresh3k`; native run `/workspace/training/humanoid/logs/rsl_rl/humanoid/2026-10-10_00-53-50`.
- OFFICIAL train/fresh, no parent/resume. 3,000 requested/completed iterations (console 2999/3000), seed 42, 4096 envs, save_interval=50.
- UTC start/end: 2026-10-09T15:53:44.601980+00:00 / 2026-10-09T16:30:54.836589+00:00. Native run is dated 2026-10-10 KST; archive Run ID uses UTC.
- COMPLETED, exit 0, validation PASS; native finalize completed, native backup successful. Backup is not a portal submission.
- Preset-relative reward display: `h1-submit-2 + ang=0.65`. Checked weights: lin=0.5, ang=0.65, feet=+0.20, termination=-50, orientation=-1.5, angxy=-0.05, hip=-0.2, torso=-0.1, action=-0.0005. ACTRATE-0001 is not stacked.
- Full resolved config stays in nested `native_run/params/env.yaml` and `agent.yaml`; reward/source identity records stay in the immutable evidence. Full source/PPO parity with frozen preset/control is not independently established by these nine weights. Official training Git commit is unknown; tag targets preservation, not inferred training source.
- Organizer checkpoints: 60 at 50-step intervals, model_0 through model_2950. Latest keeper and automatic best both correspond to `model_2950.pt`, SHA-256 `6a6f456eb3f25a7d2764af576e30b1a8169674256ae5c2ba0a1b79ed368e118c`; native best selected at step 2961.
- Unchanged wrapper: `20261009-155344-h1-angtrack-065-fresh3k-download.tar.gz`, 418,869,368 bytes, SHA-256 `a923f18fe4e7fad931e5b9b35d40c93faf38eb2c5a918d1870fbc4774ac8fe11`.
- Nested evidence: `20261009-155344-h1-angtrack-065-fresh3k.tar.gz`, 412,338,336 bytes, SHA-256 `8388f784301b55068e8e76ede75cda988e49cee32275f183e89d01fc824f5f6e`, matched received checksum. One Run, not two.
- source_provenance_verified=false remains unchanged for this fresh/no-parent Run.

Canonical: `data/raw/official_server_runs/h1/2026-10-10_005350_angtrack065_fresh3k/evidence_archives/`.
Release: https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261010-exp-h1-angular-tracking-boost-fresh3k

Assets: unchanged archive + .sha256 + preservation README. Console/TensorBoard/config/checkpoints are retained inside the archive. No policy export, videos, fixed evaluation, analysis report or submission score is claimed for ANGTRACK-065. **HOLD — analysis and matched evaluation pending.** Downloads original preserved.

[Canonical raw](https://github.com/SE3C/naver-issacsim-originals/tree/main/data/raw/official_server_runs/h1/2026-10-10_005350_angtrack065_fresh3k).
