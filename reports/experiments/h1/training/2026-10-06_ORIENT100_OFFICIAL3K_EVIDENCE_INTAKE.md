> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/experiments/h1/training/2026-10-06_ORIENT100_OFFICIAL3K_EVIDENCE_INTAKE.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# [학습] ORIENT-100 OFFICIAL fresh 3K — evidence intake, PERSONAL candidate HOLD

> 관리 안내 (2026-10-13): **학습** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](<../../../../research/EXPERIMENTS.md>)를 확인한다.

- Experiment: `exp-h1-rough-terrain-orientation-relaxation`
- Run: `20261006-133517-h1-orient-100-fresh3k-official`
- OFFICIAL fresh 0→3000, seed 42, 4096 environments; no parent checkpoint.
- Evidence execution `completed`, exit 0, validation PASS; native finalize completed and organizer backup succeeded. Console reaches iteration 2999/3000. Completion is not a performance judgment or a portal submission.
- Confirmed reward display: `h1-submit-2 + orientation=-1.0`; feet 0.20, term -50, lin/ang 0.5/0.5, orientation -1.0, angxy -0.05, hip -0.2, torso -0.1, action -0.0005.
- Full config and source identity remain in nested evidence `native_run/params/env.yaml`, `agent.yaml`, `source/identity.json`; preset-relative reward identity does not establish full historical source/PPO parity.
- Native run: `/workspace/training/humanoid/logs/rsl_rl/humanoid/2026-10-06_22-35-21`.
- `agent.save_interval=50`; 60 organizer-preserved checkpoints. Auto best is `model_2850.pt`, SHA `6aedeced60562c1d496d5319d29b76cf9e26ff43df06827cb370f24f5313f7b0`; latest preserved is `model_2950.pt`, SHA `a0748cd294c52710806ef9dbd4c9ade3d20b40461b7e5f238f67c7eb36a76e5f`, keeper origin. They are not interchangeable.
- Canonical: `naver-issacsim-originals/data/raw/official_server_runs/h1/2026-10-06_223521_orient100_fresh3k/` (immutable wrapper and received loose exports).
- Wrapper `20261006-133517-h1-orient-100-fresh3k-official-download.tar.gz`: 418957086 bytes; SHA `85ea5dd5e6ccd4f9edee587fb7a4dacd2f311caa4dd256e3c1b57744bd4fed83`.
- Nested direct archive: 412424848 bytes; SHA `c589ff4d5c4d3b5559d96ab0195610eebb492082bb70d5331654cb77c0ec2fbf`, verified against received sidecar. Wrapper and nested archive represent one Run.
- [Official raw Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261006-exp-h1-rough-terrain-orientation-relaxation-fresh3k).

Decision after the [2026-10-07 PERSONAL policy analysis](<../../../received/H1_ORIENT-100_POLICY_ANALYSIS_20261007.md>): **HOLD**, preserve for matched comparison. No official score, promotion/rejection or submission is recorded. ACTRATE-001 remains a separate PLANNED fresh test after review, not a resume of ORIENT.

Follow-up received 2026-10-07 KST: the automatic-best `model_2850.pt` has a completed PERSONAL Windows six-terrain/full H1 evaluator combined ZIP (18 files), linked by the exact checkpoint SHA above. See the [Experiment detail](<../../../../research/experiments/h1/exp-h1-rough-terrain-orientation-relaxation.md#linked-personal-windows-evaluation--model_2850-2026-10-07-kst>). This does not change the OFFICIAL training record or establish a competition score.
