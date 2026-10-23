# [분석] H1 `LINTRACK-075` corrected5K / `model_4997` — Windows PERSONAL 정책 분석 반영 (2026-10-10)

> 관리 안내 (2026-10-13): **분석** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](../../../../../research/EXPERIMENTS.md)를 확인한다.

- **판정:** 정책 행동 **HOLD**. 평지 전진·10° 경사·push 상황에서 유효한 이동 능력이 확인된 내부 후보이나, 계단/boxes 정량 검증 및 rough worst-case가 부족해 전지형 대표 정책으로 승격하지 않는다.
- **원문(입력 보존):** [H1_LINTRACK-075_CORRECTED5K_POLICY_ANALYSIS_20261010.md](../../../incoming/other/reviewed/H1_LINTRACK-075_CORRECTED5K_POLICY_ANALYSIS_20261010.md). 이 요약은 사용자가 제공한 완성 분석 보고서의 내용을 정리했으며, 현재 작업에서 원본 평가 ZIP이나 MP4를 다시 읽고 디코딩한 것은 아니다.
- **정책:** H1 corrected `LINTRACK-075`, final `model_4997.pt`, 체크포인트 SHA-256 `4349fe5650135c6a77546afc1b165ff60c235bdd83831bd562d618b04c3b5b6d`. 기존 [legacy H-008 corrected R04](../../../../../research/experiments/h1/H-008.md) 기록의 학습 Run `20260925-091257-h1-h008-corrected-control-to5k-h1-corrected-2026` 및 SHA와 일치한다. 학습은 별도 PERSONAL corrected lineage의 3K→5K unchanged continuation이며 이번 평가는 **새 training Run이 아니다**.
- **평가 원본 ZIP:** `h1_LINTRACK-075_corrected5k_model_4997_h1_6terrain_evaluation_20261009-235216_59e47db4.zip` (6 MP4 + 평가/메타 12개), [기존 PERSONAL Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261009-lintrack-075-corrected5k-model4997-video-eval), [기존 Originals raw snapshot](https://github.com/SE3C/naver-issacsim-originals/tree/main/data/raw/private_server_runs/h1/2026-10-09_windows_lintrack075_model4997_video_evaluation). ZIP 바이트는 이번 수신에 첨부되지 않았으므로 새로 검증하거나 재게시하지 않았다.
- **평가 프로토콜:** Windows **PERSONAL** `scenario7`, 7 scenario/8 case × 3 evaluation seeds(4201/4202/4203) × 128 env = **3,072 episodes**, 20초; deterministic actor, camera-off, corruption/curriculum off. Protocol SHA `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34`. **3,072/3,072 timeout, 0 base-contact failures**는 이 고정 20초 평가의 생존이지 모든 지형의 장애물 완주가 아니다.

## 보고서에서 확인한 행동 근거

| 관측 (20초 camera-off 고정평가, 384 episodes/case) | 결과 | 해석 |
| --- | --- | --- |
| H2 평지 전진 (명령 적분 15 m) | body 전진 **15.015 m**, episode별 world 순변위 크기 평균 **14.854 m** | 실제 전진 능력이 있고 정지형 생존 정책만은 아님 |
| H7 평지 push (명령 적분 10 m) | body 전진 **10.038 m**, world 순변위 **9.810 m** | 외란 조건에서 이동 지속 |
| H6 10° 경사 상행 / 하행 | body 전진 **19.943 / 19.776 m** | camera-off 경사 조건에서 강한 진행, 단 yaw 오차·action 변화 비용 높음 |
| H5 rough (명령 적분 10 m) | 평균 전진 **9.089 m**, tracking **0.2470**; **seed 4202/env 41** 최소 전진 **2.8708 m**, stall **0.664**, 20초 timeout | 평균 생존 100%로 가려지는 특정 심각한 정체 꼬리; stall>0.05는 384건 중 1건 |
| H1 zero command | world 순변위 크기 **0.516 m** | 정지 위치 유지 오차 |
| H3 좌우 반전 명령 | world 최종 순변위 크기 **1.280 m** | 횡이동 후 위치 복귀·방향 전환 잔류 |
| H6 하행 | tracking **0.2806**, yaw 절대오차 **0.2613 rad/s**, action Δ RMS **0.5098** | 경사 이동에 따른 yaw 및 조작 비용의 위험 신호 |

8-case episode 균등 가중 전체 tracking 평균 **0.21727**은 내부 혼합 지표이며 공식 NCRC score, 단위 통일 속도오차, 기존 정책 대비 개선율이 아니다. 영상은 전진/횡이동/yaw/push 스케줄과 terrain tile이 camera-off 평가와 다르므로 **같은 trajectory로 취급하지 않는다**. Boxes 영상은 블록 접촉과 이동을 보여주지만 정량 boxes case는 없다. 계단·역계단 **다단 중앙 통과는 미입증**. Rough 영상의 상당 부분은 평지 이동이다. `06_slope_down_10deg.mp4`의 짝수 프레임 전체 검정은 입력 보고서에서 캡처 결함으로 분류했고, 정책 낙상으로 세지 않는다.

## 출처 경계와 다음 비교

1. ZIP의 `source_checkpoint.txt`, `video_evaluation_link.json`, manifest 등은 정책 SHA를 일치시킨다. 그러나 ZIP 안에 원본 `.pt` bytes가 없고 `policy.source_run_id=null`, `policy.preset=null`이므로 **ZIP 단독으로 학습 계보를 확정하지 않는다**. 위 학습 Run 연결은 별도 H-008 기록과 checkpoint SHA 대조에 근거한다.
2. 평가 `resolved_configs.json`의 `track_lin_vel_xy_exp=0.5`, `termination_penalty=-5`는 **평가 환경 기본 reward 값**이며 학습 checkpoint의 실제 reward를 뒤집는 증거가 아니다. H-008 학습 resolved config는 학습 evidence에서 별도로 판단한다.
3. **1순위, 새 GPU 없이:** 보존된 `h1-submit-2 / TERM-50`의 동일 `scenario7` 평가 raw data가 있는지 먼저 확인하고, 프로토콜/소스/PPO/command/terrain/seed/horizon 정합성을 확인한 뒤 case 및 cohort 기준으로 H5 worst-case stall, H1/H3 잔류, H6 yaw/action 변화, H7 진행/실패를 비교한다. 데이터 또는 parity가 없으면 **HOLD 유지**.
4. **2순위 선택적:** 기타 보존 H1 평가(예: `ORIENT-100`)는 **별도 reward/source가 다른 참고 정책**이다. 같은 protocol과 필드·단위 검증 없는 숫자 직접 비교나 인과 판정은 보류한다. 다단 계단 정량 평가 공백은 별도로 명시한다.
5. 이 등록은 **PERSONAL 행동 근거의 접수/해석**이다. 새 GPU 평가·영상·export·학습/공식 제출이나 정책 승격을 승인 또는 수행하지 않는다.
