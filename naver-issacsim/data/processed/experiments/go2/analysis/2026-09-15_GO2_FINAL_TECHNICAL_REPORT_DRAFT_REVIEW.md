# [분석] Go2 최종 기술 개선 리포트 초안 검토

> 관리 안내 (2026-10-13): **분석** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](../../../../../research/EXPERIMENTS.md)를 확인한다.

> 2026-09-15 당시 초안 검토 기록이다. 아래의 "현재"와 미제출 판정은 초안 파일에만 적용된다. 실제 original-4800 제출 snapshot은 이후 별도로 제출·평가되어 87.55/100을 받았다. 현재 상태는 [실험 registry](../../../../../research/EXPERIMENTS.md)의 G-005 Run 07과 제출 Release 기록을 따른다.

## 판정

`GO2_FINAL_TECHNICAL_REPORT_FLOW_DRAFT_20260915.md`는 제출용 기술 개선
리포트의 **near-final source draft**로 보존한다. Baseline → G5 실패 → A1 설계 →
공식 fresh 중단 → 공식 recovery 완료 → 개인 fixed checkpoint 비교로 이어지는
서술 구조는 현재 evidence와 대체로 일치한다.

이 파일 자체는 아직 제출본이 아니다. `[MODEL_XXXX]`와 최종 선택 근거가 비어
있고 작성 메모·HTML 주석이 남아 있으며, 4800 SHA 앞에 선행 공백이 있다. 원문은
수정하지 않고 reviewed incoming에 byte-for-byte 보존한다.

## 그대로 유지할 핵심 논리

1. Baseline의 높은 timeout과 약한 XY 추종을 분리한다.
2. G5는 낮은 낙상만 최적화한 비정상 locomotion 사례로 사용한다.
3. A1은 `track_lin_vel_xy_exp 1.0→1.5`와 `lin_vel_z_l2 -3.0→-2.0`의
   **조합 가설**이며 개별 항의 독립 인과를 주장하지 않는다.
4. Official fresh 0→4837 중단과 original 4800, official recovery 4800→4999 및
   recovery 4900을 서로 다른 lineage 단계로 쓴다.
5. Resume curriculum reset 때문에 original 4800과 recovery 4900 training scalar를
   동난이도 성능 비교로 사용하지 않는다.
6. 개인 fixed evaluator는 후보 비교용 보조 근거이며 공식 점수로 쓰지 않는다.
7. `success_timeout_pct`는 20초 생존이지 terrain traversal 성공이 아니다.

## 제출 전 필수 수정

- `[MODEL_XXXX]`와 `[최종 ... 기입]` placeholder를 실제 선택 후 한 번만 채운다.
- 모든 작성 메모와 HTML 주석을 제거한다.
- `model_4800.pt` SHA 줄의 선행 공백을 제거한다.
- 중단 원인은 단순한 정상 완료로 보이지 않게 `Ctrl+C가 기록된 interrupted run;
  finalize 미실행, evidence validation FAIL`로 쓴다. 보존된 4800까지의 lineage가
  유효하다는 사실과 run 전체가 complete가 아니라는 사실을 함께 둔다.
- “공식 play 영상”은 source checkpoint→policy→video 연결이 확인된 영상만 뜻하게
  한다. Recovery handoff의 6개 MP4에는 per-video manifest/evidence archive가 없으므로
  개별 정량 검증 영상처럼 과장하지 않는다.
- 4800을 선택하면 original SHA `ea93f9b5…aba65`에서 새 `policy.pt`를 export하고
  matching `env.yaml`·영상·hash를 확보한 뒤 기입한다.
- 4900을 선택하면 existing policy actor 8/8 exact-match를 유지하되 seed-4201
  boxes/stairs 낙상 열세와 추가 seed 확인 결과를 선택 근거에 반영한다.

## 현재 선택 상태

현재는 original 4800이 **multi-seed 우선 재검증 후보**, recovery 4900이
**tracking challenger**, fresh 4300이 **control**이다. Seed 4201에서 4800은 평균
timeout 생존 `98.18%`, worst-terrain 생존 `93.75%`, base-contact `1.82%`로 가장
균형적이었다. 4900은 평균 XY RMSE `0.4099`와 전진 변위 `12.56 m`가 가장 좋지만
boxes `17.19%`, stairs `14.06%` base-contact가 관측됐다.

따라서 초안의 최종 checkpoint placeholder는 아직 채우지 않는다. 동일 evaluator의
추가 seed, 명시적 inverted-stairs 진행 성공 기준, 4800/4900의 matching export·영상
provenance를 확인한 뒤 선택한다.

## 원문과 근거

- 원문: `data/processed/incoming/other/reviewed/GO2_FINAL_TECHNICAL_REPORT_FLOW_DRAFT_20260915.md`
- 원문 SHA-256: `33f5706e6fbd5626560d45e3eaeea199a00c37009ff2f27365d8b8bf1bc66152`
- fixed 평가: `data/processed/experiments/go2/2026-09-15_GO2_G-005_FIXED_EVAL_SEED4201_D1.md`
- checkpoint 판단: `data/processed/experiments/go2/2026-09-15_GO2_G-005_CHECKPOINT_4300_4800_4900_DECISION.md`
