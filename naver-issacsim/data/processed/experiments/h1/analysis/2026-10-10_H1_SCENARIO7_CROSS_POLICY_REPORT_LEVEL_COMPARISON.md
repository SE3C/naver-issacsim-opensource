# [분석] H1 scenario7 three-policy report-level comparison and TERM-50 raw-access status (2026-10-10)

> 관리 안내 (2026-10-13): **분석** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](../../../../../research/EXPERIMENTS.md)를 확인한다.
> **후속 갱신 (2026-10-10, 원본 직접 수납):** 이 문서는 ZIP 직접 접근 이전의 **역사적 잠정 비교**다. 사용자로부터 동일 ZIP 3개를 전달받아 SHA·CRC와 `episodes.jsonl` 총 9,216행, 바이트 동일한 평가 config, 전 3,072개 대응 cohort 키를 검증한 [최신 원본 직접 대조 보고서](../2026-10-10_H1_SCENARIO7_RAW_3POLICY_MATCHED_ANALYSIS.md)가 작성됐다. 아래의 “ZIP을 열지 못했다/TERM-50 case 수치 미확인”은 **당시 상태**이며 현재 판단으로 사용하지 않는다. 새 분석은 TERM-50의 H1 비의도 전진 1.352m·H5 평균 전진 8.896m/최소 2.639m, ORIENT roll/pitch RMS 증가, ACTRATE action 비용을 직접 확인했다. 원본 archive는 그대로 보존했다.



**Scope/decision:** This is a **PERSONAL fixed-evaluator, cross-report descriptive comparison**, **not** a newly executed 3-way raw `episodes.jsonl` matched/cohort analysis, official NCRC score, reward-causality trial or automatic policy promotion. `ORIENT-100/model_2850` is the first **balanced-tracking/smoothness review candidate**; `ACTRATE-0001/model_2700` the first **rough-progression / forward review candidate**; `LINTRACK-075/model_4997` is a **forward-leakage-lower but rough-worst-tail-risk candidate**. **All three remain policy HOLD**. Whether either OFFICIAL reward delta improves on unchanged `TERM-50/model_2800` is **unknown**.

## What was actually retrieved from GitHub

Directly fetched the three GitHub Originals `publication_manifest.json` files and the three separately preserved policy-analysis Markdown reports. Also checked the three `naver-issacsim-nvidia` GitHub Release records, names/sizes/checkpoint SHA mappings, and verified an Originals `model_2800` `.zip` path contains a **133-byte Git LFS pointer rather than ZIP bytes**. The current connected GitHub reader does **not** support downloading non-UTF-8/binary release assets. Hence `evaluation/episodes.jsonl`, `evaluation_manifest.json` and per-case `resolved_configs.json` **were not extracted or reaggregated in this update**. GitHub sources were located without user reupload. The reports below claim their *authors* did the original ZIP decoding/episode analysis; do not attribute that decoding to the present comparison.

| Policy, evaluator checkpoint (different from latest keeper) | Preserved Windows PERSONAL evaluation | Archive SHA-256 | Existing analysis |
| --- | --- | --- | --- |
| **TERM-50 / `model_2800.pt`**, OFFICIAL fresh3K Run `20261008-062732-h1-term-50-fresh3k-control`, native checkpoint SHA `dffaa77848741fed1f4d22d0b78d4d8911af49057541107845e4d1df02c09ad6` | [Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261008-exp-h1-rough-terrain-orientation-relaxation-model2800-control-video-eval); [Originals preserved manifest](https://github.com/SE3C/naver-issacsim-originals/blob/main/data/raw/private_server_runs/h1/2026-10-08_windows_model2800_video_evaluation/publication_manifest.json) | `d4a47b0e182763e21077b688f44f7d9cdc00759c0f0f78f4217930e1c49975da` | **No per-case analysis or raw rows accessible here**; only evidence of complete 3,072-episode evaluation |
| **ORIENT-100 / `model_2850.pt`**, OFFICIAL fresh3K Run `20261006-133517-h1-orient-100-fresh3k-official`, checkpoint SHA `6aedeced60562c1d496d5319d29b76cf9e26ff43df06827cb370f24f5313f7b0` | [Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261007-exp-h1-rough-terrain-orientation-relaxation-model2850-video-eval); [Originals manifest](https://github.com/SE3C/naver-issacsim-originals/blob/main/data/raw/private_server_runs/h1/2026-10-07_windows_model2850_video_evaluation/publication_manifest.json) | `aecc82b13671d54c96813af6c02c1b2a7769ee001b30aa4a5c2761457110eb7a` | [Original policy analysis](../../../incoming/other/reviewed/H1_ORIENT-100_POLICY_ANALYSIS_20261007.md) |
| **ACTRATE-0001 / `model_2700.pt`**, OFFICIAL fresh3K Run `20261009-142350-h1-actrate-0001-fresh3k`, checkpoint SHA `e54d3389e20ea913968ef8d3edbea5004368ff225fa6b94f73fcd91cf93ca7ae` | [Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261010-exp-h1-action-rate-relaxation-model2700-video-eval); [Originals manifest](https://github.com/SE3C/naver-issacsim-originals/blob/main/data/raw/private_server_runs/h1/2026-10-10_windows_actrate0001_model2700_video_evaluation/publication_manifest.json) | `6270d299def2a3bcb8cc10253027898621dd65a00ad30baafde0cbcde03076e3` | [Original policy analysis](../../../incoming/other/reviewed/H1_MODEL2700_POLICY_ANALYSIS_20261010.md) |

**Metadata-level parity confirmed across all three manifests:** evaluator task checkout `ef10b7a4c9a83481346d446e8a75aed655f72214`, evaluator handoff `28895d75edf3095607e392a07207a62e768478c7`, upstream `9c774a322f2f7d4944444de57f01308987bcb3da`, protocol `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34`, `scenario7`, evaluator seeds `4201/4202/4203`, 128 env, 8 cases/7 scenarios (explicit in each suite or corroborated completed evaluation), 20 s, camera off. All are **post-training PERSONAL evaluations of OFFICIAL checkpoints**. The 6 videos are different maneuver/terrain/seed trajectories, not the camera-off episodes. **Training task/PPO byte-level parity and per-cohort effective reset/terrain fingerprint agreement are not established by these publication manifests alone.**

## Descriptive numbers already computed by separate analyses (8 cases × 384 episodes)

`mean_tracking_error` is an unnormalized numerical Euclidean mixture of body x/y-velocity and yaw-rate errors, **not a single physical unit or official score**. Body forward is an integrated body-frame velocity, **not world displacement, finish distance, or obstacle-completion rate**. No invented TERM-50 per-case values.

| Case / report metric | ORIENT-100 `2850` | ACTRATE-0001 `2700` | LINTRACK-075 `4997` |
| --- | ---: | ---: | ---: |
| Overall 8-case/episode-weighted tracking ↓ | **0.14041** | 0.14534 | 0.21727 |
| H1 zero-command tracking ↓ | **0.1171** | 0.1537 | 0.1351 |
| H1 zero-command unintended body-forward integral ↓ | 1.633 m | 1.987 m | **0.415 m** |
| H2 forward tracking ↓ | 0.1270 | **0.1188** | 0.2343 |
| H2 body-forward integral (15 m commanded) | 15.408 m | 15.326 m | 15.015 m |
| H3 lateral tracking ↓ | **0.1200** | 0.1526 | 0.1357 |
| H3 lateral-command unintended body-forward integral ↓ | 1.180 m | 1.677 m | **0.480 m** |
| H4 forward/turn tracking ↓ | **0.1429** | 0.1535 | 0.2186 |
| H5 rough tracking ↓ | **0.1709** | 0.1781 | 0.2470 |
| H5 rough mean body-forward (10 m commanded) ↑ | 9.451 m | **9.948 m** | 9.089 m |
| H5 rough P05 body-forward ↑ | 8.863 m | **9.592 m** | 8.670 m |
| H5 rough observed minimum forward ↑ (different row per policy) | 7.831 m | **8.815 m** | 2.871 m |
| H5 rough P95 tracking ↓ | 0.1948 | **0.1916** | 0.2675 |
| H5 rough observed maximum tracking error ↓ (different row per policy) | **0.2412** | 0.2908 | 0.4483 |
| H6 10° up tracking ↓ | 0.1578 | **0.1361** | 0.2765 |
| H6 10° down tracking ↓ | 0.1586 | **0.1367** | 0.2806 |
| H6 down action-change RMS ↓ | **0.464** | 0.540 | 0.5098 |
| H7 push tracking ↓ | **0.1291** | 0.1333 | 0.2104 |
| 20-second camera-off episode survival | 3,072/3,072 | 3,072/3,072 | 3,072/3,072 |

`LINTRACK-075` differs in **training environment and lineage**: PERSONAL corrected H-008 3K→5K unchanged continuation final numbered checkpoint, **not** a fresh OFFICIAL 3K sibling. Its separate [original report](../../../incoming/other/reviewed/H1_LINTRACK-075_CORRECTED5K_POLICY_ANALYSIS_20261010.md) is included as *descriptive behavioral context only*, excluded from single-delta reward causality.

## Interpretation and decision (inferences, not controlled effects)

1. **ORIENT-100 (review priority for overall tracking/smoothness):** its report values show lower tracking than ACTRATE in **5/8 cases**, while ACTRATE leads H2 and both H6 slopes (**3/8 cases**). ORIENT has the lowest action-change RMS among the three in **all 8 cases**, although no torque/energy claim follows. ORIENT's H1 1.633 m and H3 1.180 m unintended forward leakage prevent claims of satisfactory stationary/lateral control.
2. **ACTRATE-0001 (review priority for forward/rough progress):** compared with ORIENT report means its H5 forward is 9.948 vs 9.451 m, H5 P05 is 9.592 vs 8.863 m and slope tracking is lower. However H1 unintended forward is 1.987 vs 1.633 m, H3 1.677 vs 1.180 m, H6 down action RMS 0.540 vs 0.464 and H5 worst tracking 0.2908 vs 0.2412. More forward progress is not uniformly better control.
3. **LINTRACK-075 (context/failure-tail retention):** H1/H3 leakage is the lowest among these separate reports, but its H5 extreme `seed 4202/env 41` records **2.8708 m forward and 66.4% stall despite survival**, and its rough tracking is much higher. This is one recorded worst-case in 384 H5 episodes, **not** overall rough collapse or proof of the effect of `lin=0.75`.
4. **TERM-50:** baseline full evaluation ZIP is **present** with matching publication-level evaluator contract, so older wording "there is no baseline evaluation" is obsolete. **Its per-case figures remain unextracted; no win/loss or reward-attribution result against TERM-50 is established.**
5. **All policy decisions HOLD** as all-terrain representatives: 20-second survival does not prove stop/sideways commands, multi-step stairs, boxes completion or official scenario scores. ACTRATE and ORIENT training are OFFICIAL fresh3K COMPLETE/PASS; this comparison uses PERSONAL post-training diagnostics. `ANGTRACK-065` training is COMPLETE/PASS but no matching scenario7 evaluation/behavior analysis is received. `ACTRATE-001` remains PLANNED without a verified completed Run.

## What is still required for a *true* matched raw-cohort comparison (no new GPU training/evaluation needed)

The three already identified release ZIPs each contain `evaluation/episodes.jsonl`, `evaluation/evaluation_manifest.json`, `evaluation/resolved_configs.json` and diagnostics; **do not reupload or rebuild them**. A reader with authenticated binary Release/LFS access can extract these from the **existing GitHub releases** (links and SHA above). Validate ZIP SHA/CRC, per-checkpoint policy SHA, protocol/source/effective-agent/terrain/command/fingerprint parity, then join exactly on `(scenario,case,seed,env_id)` (3,072 initial cohorts per policy). Compare paired deltas and H5 P05/min/stall, H1/H3 body-forward and world displacement, H6 yaw/action/posture, H7 progress/failure, and whether resets preserve truly corresponding initial states/terrain. **Identical seed or protocol alone does not prove identical individual terrain/episode.** Determine baseline `TERM-50` case values first. Do not create p-values, official-score conversions or `study.tell()` observations before the raw data and parity are checked.

**Access limitation observed:** The connected GitHub fetch action explicitly rejects oversized/non-UTF-8 binary content; the Originals `model_2800` `.zip` file retrieved by `fetch_file` is a 133-byte `git-lfs.github.com/spec/v1` pointer with `oid sha256:d4a47b0e...`, not the 34,012,853-byte archive. Release metadata and manifests were readable, but attempting to fetch the binary archive via this connector did not supply its bytes. This document deliberately does **not** claim raw ZIP ingestion, cohort-matched statistics, byte-level full-source/PPO parity, GPU execution, or checkpoint/export/official submission.

## Evidence/decision status

- GitHub releases and stored Originals manifests: **FOUND, metadata checked**.
- Three existing detailed Markdown report values: **READ, cross-report descriptive comparison documented**.
- Actual release ZIP bytes / all three `episodes.jsonl` files: **NOT READ in this session**.
- Baseline TERM-50 raw diagnostics: **NOT RECALCULATED**.
- Reward causal effect and policy representative selection: **HOLD**.
