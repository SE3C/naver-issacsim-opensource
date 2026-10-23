# H1 2026-10-15 추가 학습 가설 재심사 — 의사결정 보고서

> **오늘 1순위:** `h1-submit-2 + {action_rate_l2=-0.0001, track_lin_vel_xy_exp=0.55}`. **ACTRATE-0001 기존 부모 `model_2700`에서 resume +2,000 iteration**. 부모 checkpoint SHA-256 `e54d3389e20ea913968ef8d3edbea5004368ff225fa6b94f73fcd91cf93ca7ae`. **기존 1순위를 유지**한다. 새로운 탐색에서 더 강한 1순위 근거는 찾지 못했다. `.65` sibling의 H5 진행 회복 및 H4 yaw·H3 세계좌표 잔차 손실을 **한 항목의 더 작은 전환**으로 가려 보는 실험이다. 실패해도 “`.65`에서 관찰된 진행 이득이 `.55`에서는 생기지 않는가 / yaw·복귀 비용이 필수 동반인가 / 단순 +2K 손실이 우세한가”를 구분할 단서를 얻는다. 이는 실행 기록이나 성공 예측이 아니다.
>
> **오늘 예비 1개 — 기존 2순위 조정 제안:** 같은 ACT 부모 `model_2700`에서 `h1-submit-2 + {action_rate_l2=-0.0003}`로 **action 한 항목 전환, resume +2,000**. 부모 SHA는 위와 같다. 이는 기존 `action=-0.0003 fresh3K`와 **학습 질문·부모·비용이 다른 새 탐색 후보**다. 무변경 B와 action 복원 C가 이미 같은 부모에 있어서 기존 fresh안보다 **식별력/iteration**이 유리하지만, C의 H5 최악 4.845m·stall .386이 보여 주는 꼬리 위험이 있어 1순위가 아니다. 예비안 실행 시 실패해도 action 중간 강도가 연장학습의 rough 손실과 C의 극단적 꼬리를 동시에 피하는지 여부를 배울 수 있다.

## 1. 범위, 관측 수준, 상태

이번 검토의 **유일한 입력은 `H1_NEW_SESSION_HYPOTHESES_20261015.zip`**이다. 그 안의 `START_HERE.md`, 2026-10-14~15 `curated/` 5개, `tracking/`, `presets/`, `reference/06_HUMANOID_TRAINING_CODE.md`, `sources/` 보고서·이미 계산된 CSV를 구분하여 읽었다. `sources/next_hypothesis/`와 `sources/parent_comparison/`은 겹치는 PERSONAL 평가를 다시 사용한다. **동일 평가를 인용하는 별도 보고서들을 독립 검증·독립 seed로 세지 않았다.** `curated/`가 말하는 후속 완료 상태를 과거 계획·과거 보고서의 “대조군 없음/대기”보다 우선했다.

직접 수행한 일은 첨부의 **파생 CSV 행 값 제한적 재계산·교차검산**과 H1 native **preset 스냅샷의 reward 필드 확인**뿐이다. 이번 세션은 `episodes.jsonl`, 전체 MP4, 원 `.pt`, native train archive, 라이브 OFFICIAL 서버, evaluator 내부 구현을 받지 않았다. 과거 보고서 저자가 원 ZIP 9,216 episode와 영상 등을 검사했다는 **보고**는 해당 원본을 이 세션이 다시 읽었다는 의미가 아니다. CPU 분석 Python 스크립트는 검토 대상이지 사용자 원 스크립트를 실행하지 않았다. 별도 `calculations/targeted_check.py`만 재현용으로 만들고 실제 실행했다.

현재 완료된 학습과 **정책 행동 판정**은 다르다. ACTRATE-0001 fresh3K `model2700`(A), 같은 부모 무변경 +2K `model4699`(B), action 복원 +2K `model4650`(C), lin=.65 전환 +2K `model4650`(L), h1-submit-2 lin=.65 **fresh5K** `model4950`(F), action+airtime 및 action+feet_slide 각각 **fresh3K**는 자료상 OFFICIAL 학습 완료/PASS이고 해당 PERSONAL 행동 분석은 수납됐지만 범용 성능 채택은 HOLD/제한적 REJECT 상태다. B는 세 정책의 **범용/전진/험지 대표 용도로만 REJECT**다. 계획 문서의 `feet_air_time=.25` **ACT-parent resume**와 `ang_vel_xy_l2=-.08` **ACT-parent resume**는 지금도 **미실행**이다. `lin=.55 resume`, `action=-.0003 fresh`, 이 보고서의 `action=-.0003 resume`는 모두 **미선택·미실행**, 새 Run ID 없음이다. Fresh 조합 실행을 한 항목 변경 resume 실험으로 읽지 않는다.

정체성: 부모 A는 Run `20261009-142350-h1-actrate-0001-fresh3k`, **평가된 자동 best2700** SHA `e54d3389…93ca7ae`; 후기 keeper2950 SHA `d4fa7221…9b70`와 다르다. B는 Run `20261014-111135-h1-actrate-0001-unchanged-cont2k`, **endpoint4699** SHA `722b35a1…48f646`; C는 Run `20261014-142200-h1-actrate-return2700-2k`, **선택4650** SHA `a8249db4…25b84ea`; L은 Run `20261010-154926-h1-actrate0001-lintrack065-from2700-plus2k`, **선택4650** SHA `ce7ad586…9dea70`. 동일 이름 `model_4650` 둘은 *다른 바이트/다른 reward*다. F는 Run `20261014-081901-h1-lintrack-065-fresh5k`, **fresh/부모 없음/model4950** SHA `b7528923…ece`이며 L과 혼동하지 않는다. 모든 SHA는 **첨부된 수납/인덱스 기록에 기재된 값**이고 이번 입력에 `.pt` 바이트가 없으므로 새로 해시 검증한 것은 아니다.

원 평가의 `source_run_id=null`·`preset=null`, 단일 native checkpoint import에서의 `source_provenance_verified=false`, `parent_run_id=null`, `source_run_mode=unknown`은 **그대로 유지**한다. 별도로 전해진 OFFICIAL Run/index의 SHA 연결은 유용하지만 위 원 provenance를 verified로 바꾸지 않는다. PERSONAL Windows 평가(각 case 384개 = evaluator seed 3 × env128)는 **학습 seed 반복이 아니라 하나의 정책에 대한 평가 cohort**다. 정책의 OFFICIAL 학습 기록과 PERSONAL 평가 성적, 실제 대회 제출/공식 채점을 합치지 않는다.

## 2. 먼저 정의한 병목 3개와 메커니즘·반례

**병목 A — H1 정지와 H3 횡명령의 body/world 불일치.** H1 zero-command에서 A의 **부호 있는 body x 적분 +1.987m**, B **−0.724m**, L **+0.108m**, C **+0.282m**이다. 절댓값을 무시한 “전진량 감소”는 B의 **후진 누수**를 놓친다. H1은 `stall=0`으로 정지 성공을 판정할 수 없다(유효 이동명령 분모가 없음). H3은 lateral `vy` 목표와 body 비명령 `vx`, yaw, world 최종 `hypot(dx,dy)`가 서로 다르다. L은 B보다 H3 `vy` 오차가 낮지만(**0.0571 vs 0.0682m/s**) world 잔차는 **2.398 vs 0.581m**로 높다. C의 world 잔차 **0.167m**는 작아도 `vy` 오차 **0.0771m/s**는 B보다 나쁘다. **물리적 해석:** 선속도 추종 가중치를 높이면 몸체 yaw-frame에서 목표하지 않은 x 속도에 페널티를 상대적으로 더 주지만, `yaw`가 계속 회전하고 10초 후 `vy`가 역전되면 world 위치 복귀는 보장되지 않는다. `action_rate_l2` 강화는 행동 변화 비용을 통해 진동/속도 전환 양상을 바꿀 수 있으나 **위치 오차 자체를 보상하지 않는다**. **반례:** F fresh lin=.65는 H1 body 누수가 0.063m지만 H3 world 잔차 3.102m다. 또한 순변위가 우연히 작다고 전체 20초 trajectory의 body 추종 성공이 아니다. H3 world-origin 복귀는 evaluator의 공식 합격 기준이 아니라 응용상 안전/재방문 진단이다.

**병목 B — H4 yaw 추종과 XY 추종·자세 보상의 경쟁.** 같은 부모 B의 H4 yaw 절대오차는 **0.091892rad/s**이나 L은 **0.179056rad/s**, A는 약 **0.1183rad/s**. L에서 XY 보상 가중치를 `.50→.65`로 올린 뒤 H2/H3 일부 평면 오차는 좋아지지만 H4 회전 및 몸통 roll/pitch 비용이 악화됐다. yaw 제어는 접촉/발 위치/몸체 방향 운동을 요구해 XY 축 목표와 정책 표현을 공유한다. 반대로 `ang_vel_xy_l2`는 **roll·pitch 각속도 페널티**로 yaw-rate `z`를 직접 벌하지 않으며, `flat_orientation_l2`는 각도 기울기 비용이다. `track_ang_vel_z_exp` 강화는 H4 추종을 직접 노릴 수 있지만 실제 ANGTRACK-065 fresh3K의 H4 yaw 오차(TERM 대조) 개선이 H3 `vy` 악화·15/384 최초 contact 종료와 공존했다. **반례:** yaw를 직접 강화하더라도 H3 및 terrain 안정성이 나빠질 수 있고, L의 yaw 악화는 train-side 동일성·체크포인트 선택과 독립 훈련 반복이 미통제여서 단독 reward 원인으로 확정할 수 없다.

**병목 C — H5 rough 평균 진행과 하위 꼬리/stall의 비대칭.** 20초 `vx=.5m/s`의 body 명령 적분은 10m다. A의 H5 진행(mean/P05/min)은 **9.948/9.592/8.815m**, B **7.919/7.427/6.239m**, L **9.546/9.228/8.974m**, C **8.769/7.970/4.845m**다. 기존 H5 cohort-key 비교에서 B−A 진행은 **384/384 감소**; L−B는 **384/384 증가**, 평균 **+1.626684m**; C−B는 **373/384 증가**, 평균 **+0.850111m**인데 **11/384 악화**, C의 stall 최악 **0.386**(B 0.074), C에서 stall>0.05 **7/384**다. 여기의 `P05(L)−P05(B)`와 `P05(L−B)`는 다른 값이다(각각 약 **1.801m**, **1.126m**). **메커니즘:** 큰 action-rate 벌점은 변화가 큰 발착지/복구 움직임을 억제해 평탄한 보행을 만들 가능성이 있지만 rough 미세 발판 적응을 제한할 수도 있다. 선속도 추종 강화는 저속 보행을 덜 보상하지만 과한 발 움직임과 회전 성능 희생을 부를 수 있다. **반례:** F의 H5 평균/P05 **8.995/8.411m**는 0/384 `stall>0.05`에도 목표 10m에 꾸준히 못 미치는 *지속적 under-tracking*이다. C에서는 평균이 회복돼도 최악 사례가 악화한다. **body x 적분은 world 지형 통과거리, stairs/boxes 완주가 아니다.**

이 세 병목은 하나의 혼합 tracking scalar나 3,072/3,072 timeout 생존으로 환원할 수 없다. H4/H5/C는 단일 evaluator training seed를 반복한 시험이 아니고, H1/H3 end-world 잔차가 작은 정책을 곧바로 통과 처리할 근거도 없다.

## 3. 변경 가능/활성화 경계와 기타 가설 재심사

이번 ZIP의 `presets/h1-submit-2/env.yaml`에서 직접 확인되는 `weight` 항목 중 **비영(非零)인 13개**는 `track_lin_vel_xy_exp=.5`, `track_ang_vel_z_exp=.5`, `ang_vel_xy_l2=-.05`, `dof_acc_l2=-1.25e-7`, `action_rate_l2=-.0005`, `feet_air_time=.2`, `flat_orientation_l2=-1.5`, `dof_pos_limits=-1`, `termination_penalty=-50`, `feet_slide=-.25`, `joint_deviation_hip=-.2`, `joint_deviation_arms=-.2`, `joint_deviation_torso=-.1`이다. `dof_torques_l2`는 비null이나 **weight=0**, `lin_vel_z_l2`와 `undesired_contacts`는 **null**이다. 모두 제공 preset 스냅샷의 상태이지 현재 서버의 실제 source나 **부모 Run의 전체 native 설정을 이번 세션에서 검증**한 결과는 아니다. 부모 기록은 대표 9개 항목을 제공하고 별도 실제 전체 train archive는 ZIP에 없다. 값이 없는 항목을 임의 활성화하거나 없는 reward를 만들어내지 않는다. `feet_slide`의 실제 측정된 slip 양은 첨부 evaluator에 없으므로 그 효과의 직접 근거가 아니다.

- **미실행 `ang_vel_xy_l2 −.05→−.08` 동일 부모 +2K:** roll/pitch 진동·H6 경사 움직임을 겨냥하는 기전은 명확하다. 그러나 yaw z 추종은 직접 노리지 못하고 contact recovery를 막을 반례가 있다. ORIENT-100의 별개 `flat_orientation_l2=-1.0` fresh3K에서 자세 흔들림 비용이 컸다고 해서 body-rate 강화가 성공/실패했다고 결론낼 수 없다. 현 H1/H3+rough/yaw 동시 병목의 1~2순위보다 근접한 sibling 근거가 부족해 **PLANNED 유지, 오늘 제외**.
- **미실행 `feet_air_time .20→.25` 동일 부모 +2K:** 착지 주기·스윙 보상으로 걸음 패턴을 바꿀 수 있지만 rough에서 불필요한 유각 연장·접촉 부족이 위험이다. action+airtime **fresh3K 조합**은 별도 완료되어 H5 평균/P05 **7.826/7.153m**, H3 world **1.690m**로 보고됐다. 이는 다른 학습 경로에서 **두 항목 변경**한 결과이고 단독 AIRTIME resume 실패의 증명은 아니다. Round4 AIRTIME fresh10K 역시 길이·preset이 달라 직접 판정에 쓰지 않았다. **PLANNED 유지, 오늘 제외**.
- **완료된 action+feet_slide=-.35 fresh3K:** H5 최초 cohort 진행 평균 약 9.639m지만 H5 **1/384 contact 종료**, H3 world 0.766m, action Δ RMS 0.49010 및 실제 발 slip 계측 부재. fresh 조합의 한 항목 효과로 나눌 수 없어 동일 조합의 즉시 반복은 밀린다. **훈련 완료 ≠ 채택**.
- `track_ang_vel_z_exp=.65` 재반복, `flat_orientation_l2=-1.0` 재반복, lin=.65 재반복/조합 추가는 이미 각기 yaw/contact·posture·rough/H3 trade-off가 있어 제한된 오늘 budget에서 정보 이득이 낮다. 새 보상 항목 활성화, PPO/terrain/command/curriculum/termination logic 변경은 모두 제외했다.

## 4. 최종 후보 3개 — 실제 우선 실행 1 + 예비 1

모든 항목은 **가설 설계**다. 여기서 나열하는 표는 **preset-relative 전체 override**이며 전체 native resolved YAML을 작성했다고 주장하지 않는다. 기준 `h1-submit-2` 외 weight·PPO/terrain/command는 **변경 없음으로 의도**한다. 실제 실행 전에 reward 소스 내 활성 상태, 동결 preset과 현재 파일 차이, 부모의 resolved `env/agent`·source identity, parent checkpoint/index/SHA를 확인해야 한다. 별도 실행 명령이나 추정 경로는 제공하지 않는다.

### ① 오늘 1순위 — ACT-parent lin=.55 resume +2K (기존 1순위 유지)

- **Preset/전체 override:** `h1-submit-2` + `action_rate_l2=-0.0001`, `track_lin_vel_xy_exp=0.55` (ang=.5, feet=.2, orient=-1.5 등 preset 값 유지).
- **부모 대비 실제 차이:** `track_lin_vel_xy_exp: 0.50→0.55` **하나**, action은 부모의 `-.0001` 유지. **OFFICIAL resume**, 요청 **2,000 iterations**. 부모 Run `20261009-142350-h1-actrate-0001-fresh3k`, **평가된 `model_2700.pt`**, SHA `e54d3389e20ea913968ef8d3edbea5004368ff225fa6b94f73fcd91cf93ca7ae`. 미평가 keeper2950로 몰래 바꾸지 않는다.
- **대조군:** 동일 부모/무변경 +2K B4699(`722b35a1…48f646`) **주대조**; lin=.65 전환 +2K L4650(`ce7ad586…9dea70`) **강도 참고**; A2700 **부모 행동 anchor**. B4699는 끝 checkpoint, L4650은 선택 checkpoint이므로 회차·선택방식이 불일치한다. 새 후보도 충분히 긴 resume라면 후반 trend를 보고 **final numbered checkpoint 우선**으로 하되 B/L와 동수준 평가를 이미 완료한 것처럼 쓰지 않는다.
- **기대/반증:** H1 body 누수와 H3 vx 억제 및 B보다 rough 진행 유지, L보다 H4 yaw/H3 world 잔차 비용 감소의 Pareto 가능성. **단조 중간값 가정 금지**: B와 유사한 rough 붕괴, L과 같은 yaw/H3 악화, 정지 시 후진 누수/왕복 오류가 나타나면 절충 가설 반증. H5 P05/min/stall을 평균보다 먼저 함께 본다.

### ② 오늘 예비 — **새** ACT-parent action=−.0003 단일 전환 resume +2K

- **Preset/전체 override:** `h1-submit-2` + `action_rate_l2=-0.0003`; `track_lin_vel_xy_exp=0.50` 등 나머지는 preset 유지. **부모 대비** `action_rate_l2: -0.0001→-0.0003` 단 **한 항목**. **OFFICIAL resume +2,000 iterations**, 부모 A의 **동일** Run/`model_2700.pt`/SHA `e54d3389e20ea913968ef8d3edbea5004368ff225fa6b94f73fcd91cf93ca7ae`. 기존 `-.0003 fresh3K`와 섞지 않는다.
- **왜 새 후보인가:** 같은 부모/동일 +2K 설계의 B(`-.0001`)와 C(`-.0005`)는 각각 H1 **−0.724/+0.282m**(부호 있는 body x), H3 world **0.581/0.167m**, rough mean **7.919/8.769m**다. 중간 강도로 *추가 regularization과 발 회복 자유도*의 균형을 시험할 수 있다. B/C가 이미 존재해 기존 fresh3K 양끝점보다 **학습 출발 상태·길이의 비교력이 높고 1K 적게** 요구한다.
- **주대조:** B4699 및 C복원4650(`a8249db4…25b84ea`)의 이미 수납된 PERSONAL 평가, A2700 보조. C는 **selected4650**, B는 **endpoint4699**여서 해당 checkpoint 선택·train-side parity 한계를 그대로 명시한다. 새 후보가 이 둘 사이에서 성능도 선형보간될 것이라는 증거는 **전혀 없다**.
- **기대/반증:** C보다 H5 최악 진행·stall을 보존하면서 B보다 H1/H3 drift와 H5 평균을 개선할 가능성. 그러나 C는 rough 진행이 B보다 증가한 **373/384**에도 **11/384는 역행**했고 최악 **4.845m / stall .386**으로 심각한 실패 신호가 있다. 새 후보에서 한 번이라도 꼬리/접촉 부작용이 재현되거나 H5 전체가 B처럼 느리면 목적상 실패다. 가장 뚜렷한 학습은 *action 중간값이 거친 지형의 꼬리 부작용을 피하는가*이다. 오늘 1순위를 넘지 못하는 이유는 중간 강도 효과와 tail 안전을 뒷받침할 기존 직접 자료가 부족해서다.

### ③ 대기 — 기존 action=−.0003 **fresh3K** (기존 2순위는 경쟁 후보로 유지)

- **Preset/전체 override:** `h1-submit-2` + `action_rate_l2=-0.0003`만. `track_lin_vel_xy_exp=.50` 유지. **OFFICIAL fresh**, **부모 Run/checkpoint/SHA 없음**, 요청 **3,000 iterations**. 동일 최종 weight여도 후보②의 resume와 완전히 다른 학습 질문이다.
- **대조군:** ACTRATE-0001 **fresh3K** A2700(action −.0001), `h1-submit-2` 기반 기존 TERM-50 `model_2800`(action −.0005) 및 별도 ACTRATE-001 fresh3K(action −.001)은 행동 참고. 특히 TERM은 5K Run의 2800 선택본일 수 있어 학습 종료 시점·체크포인트 선택/소스 차이가 있으며 A/B 동일 학습량·정책 비교로 간주하지 않는다. ACTION fresh10K model9999는 다른 길이/정책으로 섞지 않는다.
- **기대/반증:** 같은 부모에서 연장할 때 발생한 rough 열화 경로를 피하면서 fresh 중간 페널티의 정지·rough trade-off를 확인할 수 있다. 반대로 ACTRATE-001(강화)도 H1 누수가 남았고 action rate가 직접 vx/yaw/world를 목표로 하지 않아 개선이 없을 수 있다. **예비②보다 1K 많고 같은-parent control이 없어** 오늘은 3순위지만, resume의 최악 꼬리 문제가 반복되는 경우 별도 fresh 질문으로 유지할 의미는 있다.

## 5. 후보 간 비교: 가설 식별력 / 기존 증거 / 비용 / 최악 실패 위험

| 후보 | 가설 식별력 | 기존 증거의 근접성 | 오늘 추가 학습 비용 | 최악 실패 위험·의사결정 |
|---|---|---|---|---|
| **① lin=.55 ACT-parent resume** | 동일 부모 B/L이 있고 `.50/.65` 변경축만 달라 강도별 Pareto를 시험. 단 checkpoint 선택·훈련 반복 한계 | **가장 직접적:** L−B H5 +1.627m(384/384 개선), H4 yaw +.087rad/s·H3 world +1.816m 손실 | **+2K** | yaw/H3/world trade-off 잔존, B형 rough 붕괴. **오늘 1순위 유지** |
| **② action=−.0003 ACT-parent resume (신규)** | B/복원C와 같은 부모·같은 +2K 전환이라 fresh③보다 학습 경로를 통제. 선택 checkpoint 차이 있음 | C−B rough +.850m(373/384 개선)·정지/왕복 잔류 감소 **그러나 C worst 4.845m** | **+2K** | rough 최저/급성 stall 위험이 **크다**. 연구정보/iteration은 매력적이나 새 값의 안전성 약함. **오늘 예비** |
| **③ action=−.0003 fresh3K (기존)** | parent 미공유. fresh 행동 자체의 가능성은 검증하지만 reward 순수 효과 분리 약함 | A/TERM/ACTRATE-001 fresh 비교는 있으나 동일 단계/모델선택 불일치; 중간값 보간 보증 없음 | **3K** | 적어도 resume의 B/C 열화 경로를 그대로 상속하지 않을 수 있지만 fresh rough·정지 실패 가능. **대기** |

이 비교는 **기술적 정성 우선순위**이며 가중 점수, 성공 확률, 추정 OFFICIAL 점수, 임의의 채택 gate가 아니다. 후보②를 새로 올린 것은 **①을 앞서는 입증**이 아니라, 동일 비용으로 보다 공정한 action 전환 질문을 묻는다는 이유로 기존 fresh③의 **예비 순위만 교체**한 것이다. 최대 2개의 추가 Run을 자동 승인한다는 뜻이 아니다. 오늘 단 **1개만** 추가 학습 가능하다면 ①을 선택하고, ②는 예비 질문으로 남긴다.

## 6. 실행 전 검증 항목과 실패 시 배울 점 (실행 명령 없음)

현재 입력으로 확정 가능한 것은 `h1-submit-2` 동결 env/agent 스냅샷과 수납 기록의 부모/비교 checkpoint identity, reward 설계뿐이다. **실행 전 사용자가 실제 환경에서 확인할 것**은 (a) 허용 H1 reward 파일의 변경 항목이 여전히 활성인지, 실제 현재 모든 reward weight와 preset 상대 차이, (b) 부모 `model_2700` 실물 bytes/SHA 및 evidence index/source·native `params/env.yaml`/`agent.yaml`/reward source/PPO, (c) 현재 checkout의 학습·evaluator task/source/seed/env·curriculum/terrain/command 동일성, (d) final numbered checkpoint 보존·selector 근거 및 비교군과의 시점 정합성이다. 없는 경로나 옵션·Run ID를 추정하지 않는다. 기존 imported-parent provenance=false/null 또는 evaluator `source_run_id=null`은 검증 과정에서도 원형으로 둔다.

**판정 관측은 사후 같은 조건에서 분리한다:** H1 (signed/absolute body x, `vx/vy/yaw`, 행별 world 순변위 평균), H3 (명령 ±vy 구간별 `vy` 오차, 비명령 x, yaw, stall/contact, world 잔차 *별도*), H4 yaw-rate 오차, H5 (10m 목표 대비 body 진행 mean/P05/min, 대응키 차이/최악 사례, stall>0.05/contact), H6 경사 roll/pitch/action Δ와 실제 진행, H2/H7 전진과 행동 안정성. 384 평가 초기조건은 학습 재현 실험이 아니며 같은 evaluator cohort key는 같은 실제 terrain·episode 궤적을 보증하지 않는다. 기존 자료로 world drift 원인을 step별 yaw와 velocity로 분해할 수 없고 stairs/boxes 정량 case/MP4 전수가 없어 다단 완주 개선은 주장할 수 없다.

**① 실패**가 의미하는 바: 약한 XY 추종 변경으로는 B의 rough 손실을 구제하지 못했는지, 또는 `.65`에서만 나타난 XY 진행 이득이 yaw/H3 비용과 함께 나타났는지 가려볼 수 있다. **② 실패**가 의미하는 바: action 중간 벌점도 같은 부모에서 보존된 rough worst-tail 문제를 회피하지 못하거나 B의 저속 보행을 벗어나지 못했음을 알 수 있다. **③ 실패**가 의미하는 바: 문제가 단순 resume 선택만이 아니라 fresh action 강도 선택에도 남는다는 가설을 뒷받침할 수 있다. 단일 Run 결과로 각 reward의 보편적 인과/독립 seed 재현성을 확정하지 않는다.

## 7. 출처·재계산·검증 경계

- 우선 자료: `evidence/START_HERE.md`, `evidence/curated/2026-10-15_H1_NEXT_HYPOTHESIS_DECISION_INTAKE.md`, `...ACTRATE_PARENT_UNCHANGED_RESTORATION_COMPARISON_INTAKE.md`, `...H1_MODEL4650_LINTRACK065_POLICY_REVIEW.md`, `...2026-10-14_H1_4POLICY_LINTRACK065_COMPARISON_INTAKE.md`, `...2026-10-14_ACTRATE0001_FRESH_COMBINATION_REPORT_INTAKE.md`.
- 직접 참조한 숫자 원계열: `evidence/sources/parent_comparison/csv/case_summary.csv`, `rough_paired_direction.csv`, `rough_matched_episodes.csv` / `evaluation_parity.json`; `evidence/sources/next_hypothesis/derived_case_L_vs_B.csv`, `derived_H5_L_vs_B.csv`, `method_and_checks.json`. 같은 입력 평가를 재사용하므로 독립 원시 evidence로 두 번 세지 않는다.
- 이 세션의 계산 파일: `calculations/targeted_check.py`가 첨부 **파생 CSV에서만** 필요한 셀/방향을 검산해 `calculations/targeted_numeric_checks.csv` 생성; Python `csv` 표준 라이브러리 사용. `calculations/verification.txt`는 실행·행 검사 결과. **원 episode 재계산이나 원본 영상 분석 아님**.
- Reward와 상태 근거: `evidence/presets/h1-submit-2/env.yaml` 및 `...h1-submit-6/env.yaml` (**동결 snapshot**), `evidence/tracking/`의 ACT 부모·무변경·복원·lin전환·미실행 계획, `evidence/sources/reports/`의 각 정책 보고서. 경로·SHA 기록은 첨부 내 주장에 대한 추적용이며 이번 세션의 원 train archive 독립 인증은 아니다.
- **결론:** `.55 lin resume +2K`의 1순위 유지는 타당하다. 새로 제안하는 `.0003 action resume +2K`가 **기존 `.0003 fresh3K`보다 더 강한 오늘의 *예비***이지만 고위험 탐색이고, 근거 부족 때문에 1순위를 바꾸지 않는다. GPU 학습·평가·영상·export·서버 조작·Optuna trial·신규 Run 등록은 **0건**.
