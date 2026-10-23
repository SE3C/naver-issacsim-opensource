# 2026-10-15 H1 행동 분석 수납 — ACTION 복원 model_4650 · LINTRACK-065 fresh model_4950

## 수납과 증거 범위

- **원문 1:** [MODEL4650 6영상·scenario7 분석](../../../incoming/other/reviewed/H1_MODEL4650_POLICY_ANALYSIS_20261015.md). 사용자 제공 보고서는 PERSONAL Windows ZIP `h1-actrate-return2700-2k_model_4650_h1_6terrain_evaluation_20261015-032125_3fb52eff.zip`의 `episodes.jsonl` 3,072행과 MP4 6개를 직접 분석했다고 기록한다. ZIP SHA-256 `f3c5bd802479ab50b347984a122615a895343ccf418f9e66b4d846f83399f84c`.
- **원문 2:** [LINTRACK-065 6영상·scenario7 분석](../../../incoming/other/reviewed/H1_LINTRACK-065_POLICY_ANALYSIS_20261015.md). 보고서는 PERSONAL Windows ZIP `h1-lintrack-065-fresh5k_model_4950_h1_6terrain_evaluation_20261015-014027_cf736cea.zip`의 같은 형식 3,072행과 MP4 6개를 직접 분석했다고 기록한다.
- **이번 수납에서 직접 읽은 것은 두 MD 원문이다.** 그 보고서의 ZIP CRC·episode 재계산·프레임 디코딩 결과는 **보고서에 기재된 분석**으로 인용하며, 이번 Git 반영에서 ZIP/MP4/native `.pt`를 다시 열어 검산하지 않았다. 보고서와 공식 학습 Run의 연결은 별도로 보존된 checkpoint SHA/index 기록에 의존한다. 두 보고서의 `policy.source_run_id=null` 및 `policy.preset=null`은 수정하지 않는다.

## 정책 ID·행동 결론

| 항목 | ACTION 복원 MODEL4650 | LINTRACK-065 model_4950 |
| --- | --- | --- |
| Experiment · 학습 Run | [`exp-h1-action-rate-restoration`](../../../../../research/experiments/h1/exp-h1-action-rate-restoration.md) · `20261014-142200-h1-actrate-return2700-2k` | [`exp-h1-planar-tracking-weight`](../../../../../research/experiments/h1/exp-h1-planar-tracking-weight.md) · `20261014-081901-h1-lintrack-065-fresh5k` |
| 학습 성격 | OFFICIAL `model_2700`에서 +2K resume, `action_rate_l2=-0.0001→-0.0005` 복원. **원 evidence의 imported-parent provenance는 미검증** | OFFICIAL `h1-submit-2` 기준 `track_lin_vel_xy_exp=0.50→0.65` 단독 override의 fresh5K (action=-0.0005), 부모 없음 |
| 평가 체크포인트 | `model_4650.pt`, SHA `a8249db467a60015036bf229b0026b215a61e17859f1d302efe283af225b84ea`. **terminal `model_4699` 아님** | `model_4950.pt`, SHA `b7528923eef5b1368ba2299f4e0538804ba00dd358049bfdff5027f448e31ece` |
| PERSONAL 평가 | 3,072/3,072 20초 timeout, 종료/접촉 실패 0 | 3,072/3,072 20초 timeout, 종료/접촉 실패 0 |
| 전체 혼합 tracking ↓ | **0.140944** | **0.17994** |
| H1 정지 중 body 전진 / world XY 순변위 크기 평균 ↓ | 0.282m / 0.304m | **0.063m / 0.171m** |
| H3 횡왕복 중 body 전진 / world XY 최종 순변위 크기 평균 ↓ | 0.276m / **0.167m** | 0.173m / **3.102m** |
| H5 rough body 진행 평균 / P05 / 최소 ↑ | 8.769 / 7.970 / 4.845m | 8.995 / 8.411 / 7.943m |
| H5 stall fraction > 0.05 | 7/384, 최악 0.386 (`seed4201/env60`) | 0/384, 최대 0.039 |
| H2 전진 / H7 push 전진 (body 적분) | 15.297 / 10.364m | 15.088 / 10.046m |
| 행동 판정 | **HOLD**, rough 진행 하위 꼬리 위험 | **HOLD**, H3 월드 복귀 잔류 + rough 지속 저속 |

숫자는 **각 MD의 보고 값**이다. 혼합 tracking은 `vx/vy (m/s)`와 `yaw-rate (rad/s)` 오차를 합친 평가기 내부량이므로 m/s 점수처럼 표기하지 않는다. H1의 `stall=0`은 명령 속력 0으로 유효 분모가 없는 상태이지 정지 성공률이 아니다. `forward_progress_m`와 `integrated_body_forward_m`는 동일 기록이므로 독립 증거 두 개로 사용하지 않는다. H3 world 최종 순변위는 각 episode의 `hypot(world_dx,world_dy)`를 구한 후 평균해야 한다. LINTRACK의 H3 +3.102m는 body-frame 속도 추종 evaluator의 공식 실패율이 아니라 **world 위치 복귀 응용의 약점**이다.

**학습 근거의 별도 연결:** MODEL4650은 OFFICIAL resume의 index와 평가 checkpoint SHA를, LINTRACK-065은 OFFICIAL fresh5K index와 평가 checkpoint SHA를 통해 외부 연결한다. 해당 ZIP 자체는 부모 Run과 reward를 독립 검증하지 못한다. 같은 `model_4650.pt`라도 2026-10-11 **ACTRATE-0001→lin=.65** resume의 SHA `ce7ad586…9dea70`와 이번 ACTION 복원 SHA `a8249db4…25b84ea`는 **완전히 다른 정책**이다. 마찬가지로 ACTRATE-parent LINTRACK resume와 본 `h1-submit-2` 기반 LINTRACK fresh5K를 혼동하지 않는다.

## 영상과 평가 구분

두 보고서의 6영상은 각 단일 환경에서 20초 `maneuver_push`, camera-off 3,072 episode는 8 case·3 평가 seed·128 env·20초의 별도 조건이다. 초기 boxes/rough 패치에서 이동하는 모습은 보고되나 stairs/inverted stairs **중앙 다단 완주** 또는 boxes 반복 정량 성공은 입증되지 않는다. LINTRACK의 `03_boxes.mp4`는 f0+홀수 500프레임, **총 501개 검정 프레임**인 교대 렌더 artifact가 보고됐다(나머지 짝수 프레임은 정상 장면). MODEL4650 영상은 **6개 모두 f0 검정**, 교대 검정 결함은 보고되지 않았다. 영상 검정 프레임을 정책 낙상으로 취급하지 않는다. Push 후 복귀 시간·관절 슬립/토크/에너지는 평가 원자료에 없어서 측정했다고 쓰지 않는다.

## 판정·권장 대조

**후속:** [부모2700/무변경4699/ACTION 복원4650 CPU 비교](2026-10-15_ACTRATE_PARENT_UNCHANGED_RESTORATION_COMPARISON_INTAKE.md)를 수납해 아래 1번 대조는 완료됐다. 복원4650 HOLD는 유지하며 무변경4699는 해당 범용·전진/험지 대표 선정에서만 REJECT다. 아래 2번 LINTRACK fresh4950 대 TERM-50 비교는 이 보고서에 포함되지 않는다.

**정책 모두 범용 대표 승격 HOLD.** 단, MODEL4650은 H3 world 복귀에 유리하고 H5 worst-tail이 매우 약하다. LINTRACK-065은 H1 제자리 body leak가 낮지만 H3 world 최종 복귀 잔류 3.10m와 H5 낮은 진행 속도가 문제다. 생존 100%는 완주나 완전 명령 추종을 보장하지 않는다.

1. **MODEL4650 1순위:** 이미 평가 ZIP이 존재하는 같은 부모 `model_2700`의 unchanged-reward +2K `model_4699`(Run `20261014-111135-h1-actrate-0001-unchanged-cont2k`)와 먼저 CPU raw 대응 비교. 둘 다 imported-parent provenance의 미검증 필드가 존재하므로 외부 checkpoint SHA/서로 같은 부모 기재와 실현된 평가 조건을 각각 확인한다. 같은 부모의 이전 `model_2700`은 보조 참고군. **이것이 원 보고서의 과거 `model_2700` 단독 참고 비교보다 reward-change 가설에 가까운 통제 비교**지만, evaluator/source/PPO/terrain·실제 reset parity, 반복 학습 seed가 없어 인과 확정은 불가.
2. **LINTRACK fresh 1순위:** 기존 TERM-50 `model_2800`의 보존된 PERSONAL `scenario7` raw와 protocol·source/agent fingerprint·cohort 구성·명령·환경 차이를 명시해 CPU 기술 비교. 둘은 서로 다른 fresh 학습 길이/체크포인트 선택 기준일 수 있어 `lin=0.65` 단일 reward 효과를 분리할 수 없다.

비교 후보는 실행 지시가 아니다. 새 GPU 학습·평가·영상·export·Optuna trial·OFFICIAL 제출/채점은 이번 문서 수납에서 수행하지 않았다. 기존 평가 Release는 [ACTION 복원 4650](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261015-exp-h1-action-rate-restoration-model4650-video-eval), [LINTRACK fresh 4950](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261015-exp-h1-planar-tracking-weight-model4950-video-eval). 
