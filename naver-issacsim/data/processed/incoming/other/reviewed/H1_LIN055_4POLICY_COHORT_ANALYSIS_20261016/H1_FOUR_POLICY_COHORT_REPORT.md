# H1 scenario7 4정책 기존 원자료 코호트 비교

> 검토: 2026-10-16(KST) | 기존 PERSONAL Windows camera-off episode 원자료 CPU 재집계 | **새 GPU 평가·렌더·학습 없음**

## 결론

**C는 B의 rough H5 평균 진행 손실을 일부 복구했습니다**: 7.919→9.242m (Δ +1.322m), 개선 384/384, 악화 0/384 (0.0%). 그러나 A의 rough 평균 9.948m와 P05 9.592m에는 미달하며 H3 vy 오차가 B보다 커집니다. **A의 강점을 온전히 유지하며 B의 약점을 해결했다고 판정할 수 없습니다.**

**C가 D보다 균형상 우월하다고 결론낼 수 없습니다.** C는 H4 yaw 오차가 0.179→0.113rad/s (낮을수록 양호)로 감소하지만, H3 vy 오차는 0.057→0.071m/s로 증가하고 H5 평균/P05/min 진행에서 D가 우세합니다. 서로 다른 축의 trade-off이며 별도 합성점수/승자 선정은 하지 않았습니다.

**결정: C는 범용 대표 PROMOTE 보류(HOLD).** B는 H5 지속적 진행 손실이 있는 참고 대조군, A는 H5 진행 기준선, D는 rough·H3 vy 참고 후보로 분리합니다. 아래의 전체 8개 case 결과를 판단에 포함했습니다.

## 1. 원본 감사, 계보 및 평가 조건

- 입력 파일명: `H1_LIN055_4POLICY_COHORT_INPUT_20261015.zip`. 입력 ZIP SHA-256: `eff60bee8fd66a5703110f3240626945a499476a9493f0256561d9deef6a9f21`. `SHA256SUMS.txt`의 48개 멤버 해시 모두 재계산 일치(자기 자신 제외). ZIP 내부 평가 raw만 재집계했고 checkpoint `.pt` 본체는 제공되지 않아 checkpoint 바이트 SHA를 새로 계산한 것은 아닙니다.
- `INPUT_MANIFEST.json` → 평가 `policy.sha256` → `video_evaluation_link` → `publication_manifest.source_checkpoint_sha256`의 **기재 SHA 4-way 일치**를 확인했습니다. `publication_manifest`의 학습 Run 연결은 **외부 메타데이터를 통한 매핑**이고 평가 원문 `policy.source_run_id=null`, `preset=null`은 원형 보존했습니다. 부모 import provenance도 null/false를 변경하지 않았습니다.

| 정책 | 평가 checkpoint SHA-256 | 학습 run (publication 매핑) | 선택·설정 (INPUT 기준) |
|---|---|---|---|
| A 부모2700 | `e54d3389e20ea913968ef8d3edbea5004368ff225fa6b94f73fcd91cf93ca7ae` | `20261009-142350-h1-actrate-0001-fresh3k` | fresh3K automatic best; not latest keeper; lin=0.5, action=-0.0001 |
| B unchanged4699 | `722b35a127f7ae4209d94a9111ac5ee02071ba7f3b985dc9cdc0760bbe48f646` | `20261014-111135-h1-actrate-0001-unchanged-cont2k` | unchanged continuation from A; endpoint4699; lin=0.5, action=-0.0001 |
| C lin=.55/4650 | `e8a358a50832f6653b1e558788a5a676ab9a849d3ec6c64e3ed2430e9ff41814` | `20261015-105910-h1-actrate0001-lintrack-055-from2700-plus2k` | lin=.55 continuation from A; keeper4650, console endpoint4699/4700; lin=0.55, action=-0.0001 |
| D lin=.65/4650 | `ce7ad58657f3dd744e7cf2b7531f3d7d455773dfc6fb135f39d8a55aa49dea70` | `20261010-154926-h1-actrate0001-lintrack065-from2700-plus2k` | lin=.65 continuation from A; selected4650; lin=0.65, action=-0.0001 |

**평가 parity:** 네 `evaluation_manifest.protocol` 전체, `source_fingerprints`, 적용 환경 fingerprint 전 24개(8 case×3 seed), `agent_config_fingerprint`, `task_config`, `suite`, `resolved_configs.json` 961,753바이트의 **동일 SHA**(`c1bb080ceb41a6b4988fbde8ef2f2081d35e09bb44c83926a2e702d9b1a4987d`는 canonical JSON 해시), 원본 JSON 바이트도 네 파일 동일합니다. Protocol ID: `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34`.
- 환경: PERSONAL Windows H1 `Humanoid-v0`, deterministic actor, 카메라 비활성, 평가 GPU RTX 3060 Laptop. 동일 `source_fingerprints` 4개. RSL-RL 5.0.1, Isaac Lab 0.54.3 및 commit이 같은 protocol에 기록되어 있습니다. Isaac Sim 버전 `unavailable`은 미검증.
- Case: H1 flat 정지, H2 flat 0.5→1.0 m/s 전진, H3 flat body-frame vy +0.3→-0.3 m/s, H4 flat vx 0.5m/s 및 yaw +0.5→-0.5rad/s, H5 rough vx0.5m/s, H6 up/down vx1m/s, H7 push vx0.5m/s. 명령 주기 10초, 총 20초. H7 외란은 fixed XY velocity deltas 4/8/12/16초(프로토콜 명시)이며 `command_schedule=per_episode_step_clock_without_rng_v1`.
- Randomization: 평가 `resolved_configs`의 `events.add_base_mass`, `events.base_com`, `events.base_external_force_torque`, `events.physics_material`, `events.push_robot`은 모두 `null`. 단 `events.reset_base`는 reset마다 x/y 각 -0.5..0.5m, yaw -3.14..3.14rad의 균등 초기 자세 범위를 적용하며 `reset_robot_joints`는 position scale [1,1], velocity [0,0]으로 기록됩니다. H5 random rough terrain generator와 seed·difficulty 설정/적용 fingerprint가 같습니다. 하지만 실제 난수 draw/reset 자세·generated tile 자체가 정책 간 동일했다고 증명할 수는 없습니다. 개별 step/terrain realization ID가 원자료에 없습니다.
- 동일하지 않은 manifest 필드 7개(A 대비): `policy.sha256`, 임시 staging `policy.path`, `started_at`, `finished_at`, `elapsed_wall_s`, `gpu_info_before`, `gpu_info_after`. 평가 시작·종료 날짜가 각기 다릅니다. 평가에 사용한 GPU·명령·task source 설정의 차이는 발견되지 않았습니다.
- **중요:** 네 평가 `resolved_configs`에 기록된 reward는 평가 중 로드한 환경 설정을 뜻합니다(예: action weight -0.0005). A/B/C/D 학습 reward를 식별하는 근거로 전용할 수 없으며, 학습 설정 .50/.55/.65 및 action=-.0001은 `INPUT_MANIFEST`/publication의 외부 연결 주장입니다. OFFICIAL train resolved source·PPO 전체를 이 입력으로 재감사한 것은 아닙니다.

## 2. 코호트 구조·독립성

- 각 3,072 행 = 8 case × 3 evaluator seed × 128 env. 전체 12,288 episode행. 모든 정책·case·seed마다 128개 고유 env ID이며 3,072개의 동일 `(scenario,case,seed,env_id)` 키를 1:1 매칭했습니다. 중복 0, 누락 0.
- `episode_id`는 전부 `-n0`, 1,000 step(20.0초), `end_reason=timeout`, `survived=true`, `base_contact_failure=false`. 후속 reset/restart episode나 조기 종료는 기록되지 않습니다. H1/H3 등 모두 고정 명령 시간창이 동일합니다.
- 동일 key의 **대응 변화량은 유용한 기술통계**지만 동일 terrain realization·관절 trajectory를 의미하지 않습니다. 128개 env는 같은 훈련의 128번 독립 실험이 아니고 evaluator seed 3개도 학습 seed 반복 3개가 아닙니다. 유의성 p값/독립 샘플 3072개인 CI를 계산하지 않았습니다. seed 3개 범위와 paired 방향을 기술합니다.

## 3. 핵심 지표 절댓값과 주요 변화량

값은 cohort 전체 산술평균(별도 표시된 H5 P05/min은 분포 통계)입니다. Δ는 **앞 정책 − 뒤 정책**; forward progress는 증가가 좋고 오차·절대 누수·stall은 감소가 좋습니다. yaw는 rad/s, 선속도 오차는 m/s, 진행·world XY는 m입니다.

| 진단 | A | B | C | D | C−B | C−D | C−A |
|---|---:|---:|---:|---:|---:|---:|---:|
| H1 절대 body forward 누수 (m) | 1.987 | 0.724 | 0.209 | 0.108 | -0.515 | +0.101 | -1.778 |
| H1 world XY 순변위 (m) | 2.011 | 0.692 | 0.702 | 0.228 | +0.009 | +0.474 | -1.310 |
| H3 vy 오차 (m/s) | 0.067 | 0.068 | 0.071 | 0.057 | +0.003 | +0.014 | +0.004 |
| H3 yaw 오차 (rad/s) | 0.088 | 0.069 | 0.097 | 0.112 | +0.028 | -0.015 | +0.009 |
| H3 절대 body forward 누수 (m) | 1.677 | 0.741 | 0.197 | 0.044 | -0.545 | +0.153 | -1.480 |
| H3 world XY 순변위—보조 (m) | 0.669 | 0.581 | 2.363 | 2.398 | +1.782 | -0.034 | +1.694 |
| H4 yaw 오차 (rad/s) | 0.118 | 0.092 | 0.113 | 0.179 | +0.021 | -0.066 | -0.006 |
| H5 rough 진행 평균 (m) | 9.948 | 7.919 | 9.242 | 9.546 | +1.322 | -0.304 | -0.707 |
| H5 rough mean tracking (혼합) | 0.178 | 0.186 | 0.179 | 0.185 | -0.007 | -0.006 | +0.001 |
| H5 rough mean stall | 0.006 | 0.010 | 0.006 | 0.007 | -0.003 | -0.001 | +0.001 |
| H5 rough stall>0.05 비율 | 0.000 | 0.003 | 0.000 | 0.000 | -0.003 | +0.000 | +0.000 |

H5 진행 lower-tail (모든 384 cohort를 포함; **하위 10% 제거 또는 채택 규칙 사용하지 않음**):

| 정책 | 평균 (m) | P05 (m) | min (m) | P95 (m) | stall>0.05 |
|---|---:|---:|---:|---:|---:|
| A 부모2700 | 9.948 | 9.592 | 8.815 | 10.328 | 0/384 |
| B unchanged4699 | 7.919 | 7.427 | 6.239 | 8.377 | 1/384 |
| C lin=.55/4650 | 9.242 | 8.859 | 8.256 | 9.579 | 0/384 |
| D lin=.65/4650 | 9.546 | 9.228 | 8.974 | 9.826 | 0/384 |

### 우선 비교: C 대 B

- H5 진행 +1.322m; 개선 384/384, 악화 0/384 (0.0%). C의 P05 8.859m vs B 7.427m; 최저값도 C 8.256m vs B 6.239m. 전체 tail 및 seed별 분리 표 참조.
- H1 body 누수 절댓값 -0.515m (개선 384/384, 악화 0/384 (0.0%)). 단 **world XY 순변위 평균**은 B 0.692→C 0.702m로 반드시 같이 기록합니다.
- H3 body-frame vy 오차 +0.003m/s (개선 0/384, 악화 384/384 (100.0%)); yaw 오차 +0.028rad/s (개선 0/384, 악화 384/384 (100.0%)). H3 world XY 종료 순변위는 응용 진단일 뿐 필수 복귀/성공 문턱이 아닙니다.
- H4 회전 yaw 오차 +0.021rad/s (개선 0/384, 악화 384/384 (100.0%)); C는 회전 축에서 B의 이점을 지키는지 별도 확인이 필요합니다.

### 두 번째 비교: C 대 D

- H3 vy 오차 +0.014m/s (개선 0/384, 악화 384/384 (100.0%)), yaw 오차 -0.015rad/s (개선 384/384, 악화 0/384 (0.0%)) — 횡속도/회전 누수의 상충.
- H4 yaw 오차 -0.066rad/s (개선 384/384, 악화 0/384 (0.0%)). H5 진행 -0.304m (개선 48/384, 악화 336/384 (87.5%)); P05 C 8.859 vs D 9.228m, min C 8.256 vs D 8.974m.

## 4. 8개 case 모두 검토: 추종·전진·자세·action 변화량

Mixed tracking은 평가기의 episode summary 혼합값이며 물리 단위가 하나가 아닙니다. 서로 다른 축의 지표를 합산한 승자 점수는 계산하지 않았습니다.

| case | track A/B/C/D (↓) | C−B / C−D track Δ | forward A/B/C/D (m) | C−B / C−D forward Δ (m) |
|---|---|---|---|---|
| H1/flat | 0.154/0.108/0.129/0.136 | +0.022 / -0.007 | 1.987/-0.724/0.209/0.108 | +0.933 / +0.101 |
| H2/flat | 0.119/0.125/0.142/0.162 | +0.017 / -0.020 | 15.326/13.972/14.715/14.812 | +0.744 / -0.096 |
| H3/flat | 0.153/0.118/0.135/0.139 | +0.017 / -0.004 | 1.677/-0.741/0.197/-0.044 | +0.938 / +0.241 |
| H4/flat | 0.154/0.133/0.148/0.196 | +0.016 / -0.048 | 10.556/9.084/9.847/9.842 | +0.763 / +0.006 |
| H5/rough | 0.178/0.186/0.179/0.185 | -0.007 / -0.006 | 9.948/7.919/9.242/9.546 | +1.322 / -0.304 |
| H6/slope_up | 0.136/0.151/0.150/0.190 | -0.001 / -0.040 | 20.052/19.007/19.684/19.872 | +0.677 / -0.188 |
| H6/slope_down | 0.137/0.154/0.146/0.194 | -0.008 / -0.048 | 19.834/18.834/19.581/19.633 | +0.747 / -0.052 |
| H7/push | 0.133/0.126/0.156/0.162 | +0.030 / -0.006 | 10.542/8.981/9.887/9.757 | +0.906 / +0.129 |

사전 지정한 나머지 회귀 검사(H2 forward, H6 slope-up/down, H7 push 포함)는 위 **전 case** 결과로 수행했습니다. H1/H3 `forward_progress_m`은 목표가 전진 0이므로 signed mean을 우열로 해석하지 말고 절대 누수와 vx 추종을 사용하십시오. H4에는 동시에 전진 0.5m/s 명령이 들어가므로 yaw만으로 전진 성능을 대신하지 않습니다.

### 사전 정의된 case별 대응 악화 방향

| 비교 | case | metric | 평균 Δ (candidate−reference) | 악화 / 전체 (%) |
|---|---|---|---:|---|
| C−B | H1/flat | `abs_forward_m` | -0.5153 | 0/384 (0.0%) |
| C−B | H3/flat | `vy_error` | +0.0031 | 384/384 (100.0%) |
| C−B | H3/flat | `yaw_error` | +0.0279 | 384/384 (100.0%) |
| C−B | H4/flat | `yaw_error` | +0.0207 | 384/384 (100.0%) |
| C−B | H5/rough | `forward_progress_m` | +1.3223 | 0/384 (0.0%) |
| C−B | H5/rough | `mean_tracking_error` | -0.0069 | 142/384 (37.0%) |
| C−B | H5/rough | `stall_fraction` | -0.0032 | 22/384 (5.7%) |
| C−B | H2/flat | `forward_progress_m` | +0.7435 | 0/384 (0.0%) |
| C−B | H6/slope_up | `forward_progress_m` | +0.6766 | 0/384 (0.0%) |
| C−B | H6/slope_down | `forward_progress_m` | +0.7470 | 0/384 (0.0%) |
| C−B | H7/push | `forward_progress_m` | +0.9059 | 0/384 (0.0%) |
| C−D | H1/flat | `abs_forward_m` | +0.1012 | 384/384 (100.0%) |
| C−D | H3/flat | `vy_error` | +0.0143 | 384/384 (100.0%) |
| C−D | H3/flat | `yaw_error` | -0.0147 | 0/384 (0.0%) |
| C−D | H4/flat | `yaw_error` | -0.0665 | 0/384 (0.0%) |
| C−D | H5/rough | `forward_progress_m` | -0.3044 | 336/384 (87.5%) |
| C−D | H5/rough | `mean_tracking_error` | -0.0056 | 148/384 (38.5%) |
| C−D | H5/rough | `stall_fraction` | -0.0005 | 22/384 (5.7%) |
| C−D | H2/flat | `forward_progress_m` | -0.0963 | 384/384 (100.0%) |
| C−D | H6/slope_up | `forward_progress_m` | -0.1880 | 355/384 (92.4%) |
| C−D | H6/slope_down | `forward_progress_m` | -0.0516 | 248/384 (64.6%) |
| C−D | H7/push | `forward_progress_m` | +0.1294 | 0/384 (0.0%) |
| B−A | H1/flat | `abs_forward_m` | -1.2626 | 0/384 (0.0%) |
| B−A | H3/flat | `vy_error` | +0.0010 | 382/384 (99.5%) |
| B−A | H3/flat | `yaw_error` | -0.0185 | 0/384 (0.0%) |
| B−A | H4/flat | `yaw_error` | -0.0264 | 0/384 (0.0%) |
| B−A | H5/rough | `forward_progress_m` | -2.0290 | 384/384 (100.0%) |
| B−A | H5/rough | `mean_tracking_error` | +0.0079 | 256/384 (66.7%) |
| B−A | H5/rough | `stall_fraction` | +0.0040 | 356/384 (92.7%) |
| B−A | H2/flat | `forward_progress_m` | -1.3545 | 384/384 (100.0%) |
| B−A | H6/slope_up | `forward_progress_m` | -1.0448 | 384/384 (100.0%) |
| B−A | H6/slope_down | `forward_progress_m` | -0.9997 | 384/384 (100.0%) |
| B−A | H7/push | `forward_progress_m` | -1.5617 | 384/384 (100.0%) |
| C−A | H1/flat | `abs_forward_m` | -1.7780 | 0/384 (0.0%) |
| C−A | H3/flat | `vy_error` | +0.0041 | 384/384 (100.0%) |
| C−A | H3/flat | `yaw_error` | +0.0094 | 384/384 (100.0%) |
| C−A | H4/flat | `yaw_error` | -0.0058 | 0/384 (0.0%) |
| C−A | H5/rough | `forward_progress_m` | -0.7067 | 382/384 (99.5%) |
| C−A | H5/rough | `mean_tracking_error` | +0.0009 | 191/384 (49.7%) |
| C−A | H5/rough | `stall_fraction` | +0.0008 | 274/384 (71.4%) |
| C−A | H2/flat | `forward_progress_m` | -0.6109 | 384/384 (100.0%) |
| C−A | H6/slope_up | `forward_progress_m` | -0.3681 | 384/384 (100.0%) |
| C−A | H6/slope_down | `forward_progress_m` | -0.2527 | 384/384 (100.0%) |
| C−A | H7/push | `forward_progress_m` | -0.6559 | 384/384 (100.0%) |
| D−A | H1/flat | `abs_forward_m` | -1.8792 | 0/384 (0.0%) |
| D−A | H3/flat | `vy_error` | -0.0102 | 0/384 (0.0%) |
| D−A | H3/flat | `yaw_error` | +0.0241 | 384/384 (100.0%) |
| D−A | H4/flat | `yaw_error` | +0.0607 | 384/384 (100.0%) |
| D−A | H5/rough | `forward_progress_m` | -0.4023 | 360/384 (93.8%) |
| D−A | H5/rough | `mean_tracking_error` | +0.0065 | 248/384 (64.6%) |
| D−A | H5/rough | `stall_fraction` | +0.0013 | 332/384 (86.5%) |
| D−A | H2/flat | `forward_progress_m` | -0.5147 | 384/384 (100.0%) |
| D−A | H6/slope_up | `forward_progress_m` | -0.1802 | 382/384 (99.5%) |
| D−A | H6/slope_down | `forward_progress_m` | -0.2011 | 377/384 (98.2%) |
| D−A | H7/push | `forward_progress_m` | -0.7853 | 384/384 (100.0%) |

세 축 회귀에서 보이는 추가 상충: C는 B보다 대부분 case에서 `vx_error`가 낮고 전진 적분은 개선되지만, H3/H4의 `vy_error`/`yaw_error`, 자세 `roll_pitch_rms`와 `action_delta_rms`(행동 변화 크기)는 B보다 증가합니다. 반면 D에 비해서는 C가 대부분 case의 yaw 축에서 유리하지만 lateral `vy_error`가 지속적으로 큽니다. 자세·action RMS는 별도 기록된 proxy이며 영상/물리적 보행 우열과 일대일 대응하지 않습니다.

| case | C−B vx / vy / yaw 오차 Δ | C−B roll/pitch RMS Δ | C−B action Δ RMS 변화 |
|---|---|---:|---:|
| H1/flat | -0.022 / +0.005 / +0.032 | +0.021 | +0.044 |
| H2/flat | -0.028 / +0.005 / +0.032 | +0.016 | +0.076 |
| H3/flat | -0.024 / +0.003 / +0.028 | +0.020 | +0.076 |
| H4/flat | -0.025 / +0.006 / +0.021 | +0.014 | +0.111 |
| H5/rough | -0.046 / +0.002 / +0.026 | +0.014 | +0.057 |
| H6/slope_up | -0.020 / +0.003 / +0.008 | +0.013 | +0.069 |
| H6/slope_down | -0.027 / +0.003 / +0.002 | +0.012 | +0.068 |
| H7/push | -0.030 / +0.005 / +0.053 | +0.016 | +0.107 |

평가 전체 episode `mean_tracking_error` (사전에 존재한 진단 요약·새 합성 점수 아님): A 부모2700 0.145339, B unchanged4699 0.137377, C lin=.55/4650 0.148092, D lin=.65/4650 0.170479. 이 수치만으로 후보를 고르지 않습니다.

### 주요 개선/악화의 평가 seed별 확인

| 비교 | case / 지표 | seed4201 Δ | seed4202 Δ | seed4203 Δ |
|---|---|---:|---:|---:|
| C−B | H1/flat `abs_forward_m` | -0.5146 | -0.5155 | -0.5159 |
| C−B | H3/flat `vy_error` | +0.0032 | +0.0031 | +0.0031 |
| C−B | H3/flat `yaw_error` | +0.0278 | +0.0278 | +0.0281 |
| C−B | H4/flat `yaw_error` | +0.0207 | +0.0207 | +0.0206 |
| C−B | H5/rough `forward_progress_m` | +1.2798 | +1.3580 | +1.3292 |
| C−D | H1/flat `abs_forward_m` | +0.1019 | +0.1010 | +0.1009 |
| C−D | H3/flat `vy_error` | +0.0143 | +0.0143 | +0.0143 |
| C−D | H3/flat `yaw_error` | -0.0146 | -0.0148 | -0.0147 |
| C−D | H4/flat `yaw_error` | -0.0664 | -0.0664 | -0.0666 |
| C−D | H5/rough `forward_progress_m` | -0.3038 | -0.2990 | -0.3102 |

## 5. seed별 H5 rough 꼬리와 개선의 일관성

| 정책 | 평가 seed | 진행 mean / P05 / min (m) | stall>0.05 | 최대 stall |
|---|---:|---|---:|---:|
| A 부모2700 | 4201 | 9.946 / 9.583 / 9.477 | 0/128 | 0.0070 |
| A 부모2700 | 4202 | 9.959 / 9.592 / 8.815 | 0/128 | 0.0190 |
| A 부모2700 | 4203 | 9.939 / 9.651 / 9.406 | 0/128 | 0.0230 |
| B unchanged4699 | 4201 | 7.949 / 7.488 / 6.740 | 0/128 | 0.0440 |
| B unchanged4699 | 4202 | 7.900 / 7.421 / 6.894 | 0/128 | 0.0330 |
| B unchanged4699 | 4203 | 7.908 / 7.336 / 6.239 | 1/128 | 0.0740 |
| C lin=.55/4650 | 4201 | 9.229 / 8.892 / 8.610 | 0/128 | 0.0130 |
| C lin=.55/4650 | 4202 | 9.258 / 8.822 / 8.658 | 0/128 | 0.0130 |
| C lin=.55/4650 | 4203 | 9.238 / 8.884 / 8.256 | 0/128 | 0.0180 |
| D lin=.65/4650 | 4201 | 9.533 / 9.197 / 9.038 | 0/128 | 0.0140 |
| D lin=.65/4650 | 4202 | 9.557 / 9.266 / 8.974 | 0/128 | 0.0220 |
| D lin=.65/4650 | 4203 | 9.548 / 9.233 / 9.098 | 0/128 | 0.0190 |

H5 seed별 paired 진행 변화량(각 seed에 128 env, 이들이 독립 학습 반복은 아님):

| 비교 | seed 4201 (m) | seed 4202 (m) | seed 4203 (m) | seed Δ 최소..최대 (m) |
|---|---:|---:|---:|---|
| C−B | +1.280 | +1.358 | +1.329 | +1.280..+1.358 |
| C−D | -0.304 | -0.299 | -0.310 | -0.310..-0.299 |
| B−A | -1.997 | -2.059 | -2.030 | -2.059..-1.997 |
| C−A | -0.717 | -0.702 | -0.701 | -0.717..-0.701 |
| D−A | -0.413 | -0.402 | -0.391 | -0.413..-0.391 |

## 6. 부모 A 대비 무엇을 유지했는가

- **H5 rough:** A 평균/P05/min 9.948/9.592/8.815m; B 7.919/7.427/6.239m; C 9.242/8.859/8.256m; D 9.546/9.228/8.974m. C는 B보다 회복되었지만 A의 강한 험지 진행을 유지하지 못했습니다.
- **H2/H6/H7 진행:** A→C 각각 H2 15.326→14.715m, H6 up 20.052→19.684m, down 19.834→19.581m, H7 10.542→9.887m. 전진은 유지에 가까운 정도가 있으나 원본 수준과 동일하지는 않습니다.
- **정지/횡명령:** A H1 절대 누수 1.987→C 0.209m, H3 절대 누수 1.677→C 0.197m로 감소. 그러나 H3 vy 오차 A 0.067→C 0.071m/s 증가: 전진 누수의 감소가 횡속도 명령 추종 개선을 의미하지는 않습니다.
- A는 fresh3K 자동 best2700, B는 continuation endpoint4699, C/D는 keeper/selected4650이며 평가 날짜도 다릅니다. 동일 부모라는 external lineage 주장만으로 학습 길이·PPO 전체·checkpoint selector를 통제한 단일 reward 인과 실험이라고 단정할 수 없습니다.

## 7. 지표·불확실성·미확인 근거

- `forward_progress_m`와 `integrated_body_forward_m`는 **모든 행에서 정확히 동일 값**입니다. body-frame forward velocity의 signed 시간적분(단위 m)이고 world pathlength 또는 rough tile 실제 통과 거리가 아닙니다. H1/H3는 `abs_forward_m`를 비의도 전진 누수 보조 지표로 사용했습니다.
- `world_xy_net_m=hypot(world_dx_m, world_dy_m)`은 **최종 세계좌표 순변위**이며 누적 path length가 아닙니다. 특히 H3 body-frame ±vy 명령은 world XY 원점 복귀 의무가 없습니다. `lateral_drift_m`는 evaluator 맥락상 vy 오차 크기의 시간적분으로, 실제 물리적 world-side displacement가 아닙니다.
- `vx_error`/`vy_error`는 episode summary 속도축 오차(m/s), `yaw_error`는 yaw 각속도 오차(rad/s), `xy_rmse`/`yaw_rmse`는 해당 summary RMS. 세 축 통합 `mean_tracking_error`는 물리적으로 단일 단위가 없으며 공식 Tracking Score와 같지 않습니다. 이 입력에는 evaluator의 계산 함수 전체 소스가 없어 절댓값/평균의 exact 코드식·step별 가중과 제외 방식은 파일명/필드만으로 독립 증명할 수 없습니다.
- `stall_fraction`은 명령 속도>0.2m/s 구간 중 관측 진행 속도<0.1m/s의 비율이라는 suite 임계값(코드 구현은 미동봉)을 사용한 evaluator summary입니다. H1 stall=0은 정지 유지 증거가 아닙니다. `stall>0.05`는 관찰 보고용 보조 빈도이며 채택/trim 기준이 아닙니다.
- H5 P05는 **모든 n=384**를 포함한 선형보간 경험적 5백분위수(정렬 후 (n−1)×0.05 위치)입니다. 3개의 평가 seed에 의한 편차와 case별 차이를 보고하되 CI/p-value는 제공하지 않습니다(평가 seed 3개, 학습 seed 반복 부재). 각 seed는 128 env 관측값을 포함해 군집되어 있습니다.
- 원자료는 case별 episode endpoint aggregate만 담고 있어 **H3 전반/후반 ±vy별 추종, 10초 전환 직후 과도응답, H4 ±yaw 구간별 추종, push 후 몇 초 내 회복, H5 rough 지형의 실제 patch 통과/슬립/계단·상자 성공, 발생시각/접촉 시계열**은 미확인입니다. 영상 파일도 이번 입력에는 없으므로 보행 동작을 직접 관찰하지 않았습니다.
- 본 결과는 PERSONAL camera-off diagnostic이며 **공식 채점·공식 성공률·공식 점수 예측 또는 새로운 합성 점수**가 아닙니다. 원본 source_run_id/provenance를 임의 보완하지 않았습니다.

## 8. 다음 행동 한 가지

**새 평가·렌더·학습 없이 이 비교를 기록하고 C의 범용 후보 승격을 보류(HOLD)한다.** H5 하위꼬리/진행과 H3 vy·H4 yaw의 축별 trade-off를 기존 checkpoint/보고서의 판단 근거로 보존하고, 선택 기준을 사후 변경하지 않습니다.

## 재현 산출물

`csv/policy_case_metrics.csv`(모든 8 case × 4정책 × 지표), `csv/policy_seed_case_metrics.csv`(seed별), `csv/paired_case_metrics.csv`(5개 사전 정의 비교 × 8 case × 지표), `csv/paired_seed_case_metrics.csv`, `csv/paired_cohorts_key_metrics.csv`(키별 후보/reference 값과 Δ), `csv/h5_tail_by_seed.csv`, `csv/manifest_parity.csv`, `csv/policy_provenance.csv`, `csv/cohort_integrity.csv`, `PROVENANCE_AND_RUN.md`, `analyze_cohorts.py`. 후자는 동일 입력 ZIP을 직접 읽고 모든 표와 이 보고서를 다시 생성합니다.
