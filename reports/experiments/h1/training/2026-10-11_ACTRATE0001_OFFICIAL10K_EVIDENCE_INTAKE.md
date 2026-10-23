> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/experiments/h1/training/2026-10-11_ACTRATE0001_OFFICIAL10K_EVIDENCE_INTAKE.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# [학습] H1 ACTRATE-0001 — OFFICIAL fresh 10K evidence intake

> 관리 안내 (2026-10-13): **학습** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](<../../../../research/EXPERIMENTS.md>)를 확인한다.

Follow-up after this intake: model_9999 PERSONAL six-video/full evaluation publication〔원본 참조: `../../../operations/windows_h1_video_evaluation/2026-10-11_ACTRATE0001_FRESH10K_MODEL9999_PUBLICATION.md` / 공개 사본 미포함〕, followed by user report intake and policy review〔원본 참조: `../2026-10-11_ACTRATE0001_MODEL9999_POLICY_REVIEW.md` / 공개 사본 미포함〕. Its SHA matches the archived official keeper index; the historical initial intake status below is not the current absence of evaluation or analysis. Analysis received; report decision HOLD.

Experiment: [`exp-h1-action-rate-relaxation`](<../../../../research/experiments/h1/exp-h1-action-rate-relaxation.md>). This is a new execution of the existing reward question, not a new Experiment or submission preset.

- Run `20261011-041745-h1-actrate-0001-fresh10k-official`: H1 / OFFICIAL / train / fresh; no parent checkpoint and no resume. Seed 42, 4096 environments, requested 10,000 iterations.
- Metadata `completed`, exit 0, evidence validation PASS. Native finalize and official backup completed. Learning completion is not a quality or official submission decision.
- Native Run `/workspace/training/humanoid/logs/rsl_rl/humanoid/2026-10-11_13-17-54`; metadata start/end UTC `2026-10-11T04:17:45.241178+00:00` / `2026-10-11T06:19:34.270277+00:00`. The exact final console iteration and latest keeper filename were not independently checked at intake; do not substitute auto-best 9900 for the final endpoint.
- Preset-relative display `h1-submit-2 + action=-0.0001`; checked nine weights: lin=0.5, ang=0.5, feet=+0.20, termination=-50, orientation=-1.5, angxy=-0.05, hip=-0.2, torso=-0.1, action=-0.0001. Native `params/env.yaml` + `agent.yaml`, archived `source/humanoid_rewards.py` and source identity are the complete config/provenance reference. Other configured rewards remain in the native YAML; the nine fields are not a full resolved snapshot or proof of full source/PPO parity with earlier Runs.
- 201 organizer keeper checkpoints preserved; checkpoint index includes 202 entries with the native checkpoint. Original console, TensorBoard, source, configs and exports remain inside the received wrapper.
- Automatic best `model_best.pt` = indexed native `model_9900.pt`, SHA-256 `6dd795e32383bc21ac487ea039bb2a03a565ec2ee6da893a3dc4ffaa844c769d`. Peak-reward report step 9880 and checkpoint number 9900 are separate values.
- Original wrapper `20261011-041745-h1-actrate-0001-fresh10k-official-download.tar.gz`: 1,358,051,174 bytes; SHA-256 `6977db0f4cea94d7685023a4b58702290f762e2c075525bc977173a2d54ebdb7`.
- Nested evidence archive SHA-256 `46fec3c49eac8e357f9916b422d8885bf94786639fae84520fd4501d706f8eb6` matches its received checksum. Recorded native validation PASS; no credential/key/.env candidate paths or plaintext metadata credential values found in the inspected records.

[Canonical immutable raw preservation](https://github.com/SE3C/naver-issacsim-originals/tree/main/data/raw/official_server_runs/h1/2026-10-11_actrate0001_fresh10k) · [OFFICIAL training Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261011-exp-h1-action-rate-relaxation-fresh10k).

**Initial training intake (historical): training complete, analysis pending/HOLD.** The later model_9999 evaluation and report are linked above; the current report decision remains HOLD. Historical fresh3K/model_2700 PERSONAL videos and evaluation are not this Run's results. No actual portal submission, official score or new submit preset is claimed. Original Downloads archive is retained unchanged.
