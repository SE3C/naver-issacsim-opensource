> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/experiments/go2/analysis/2026-10-09_GO2_R3_4800_R5_7450_LOCAL_OFFICIAL_COMPARISON.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# [분석] Go2 R3 original 4800 / R5 terminal 7450 — 2026-10-09 후속 판정

> 관리 안내 (2026-10-13): **분석** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](<../../../../research/EXPERIMENTS.md>)를 확인한다.

## 출처와 보존

- [수신 보고서 원문](<../../../received/GO2_R3_4800_VS_R5_7450_DEEP_ANALYSIS_20261009.md>)을 바이트 그대로 보존했다. 수신명: `GO2_R3_4800_vs_R5_7450_20261009_%EC%8B%AC%EC%B8%B5%EB%B6%84%EC%84%9D (1).md`; 34,271 bytes; SHA-256 `5a681189f249ff14040fda63702f15d48c4dd7a84a603db693ad9d74a5ff47b2`.
- 공식 수치는 운영진 DM·공식 구성 요약〔원본 참조: `../2026-10-08_GO2_R3_R5_OFFICIAL_SCORE_COMPONENTS_ORGANIZER_REPLY.md` / 공개 사본 미포함〕이 근거다. 이번 보고서의 PERSONAL 통계는 두 ZIP의 raw episodes/diagnostics와 독립 대조해 주요 건수·평균이 일치함을 확인했다.
- 이 문서화에서 새 GPU 실행, evaluator/reward/source 변경, calibration 생성은 하지 않았다. 영상 관찰은 받은 보고서의 표본 관찰이며 이번 정리에서 프레임을 다시 분석하지 않았다.

## 비교한 실제 산출물

| 항목 | R3 / g2-submit-3 | R5 / g2-submit-5 |
| --- | --- | --- |
| checkpoint | original `model_4800.pt` | terminal `model_7450.pt` |
| checkpoint SHA-256 | `ea93f9b5b04d91a91d1cdb97c6d328978017991e0602745f9269c7190bfaba65` | `b8766030e306dd72160d37292539575d5a1d92c2757f34637dafab3c1582343a` |
| ZIP | `g2-submit-3_model_4800_go2_6terrain_evaluation_20261009-021618_04460d33.zip` | `model_7450_go2_6terrain_evaluation_20261009-115152_19467d0a.zip` |
| ZIP bytes | 36,843,939 | 35,961,918 |
| ZIP SHA-256 | `f2bb7917fd325544858ce5aecf801f54e24572c164ed5c6d38ed17c316a1d221` | `4c6aba677ccb1740014bcd94e962b924f54dc07686d2927d6e183e6493e6c854` |
| full evaluation episodes | 3,471 | 3,460 |

둘 다 PERSONAL Windows, 128 env × seeds 4201/4202/4203 × 9 cases × 20초, camera-off `scenario7`, complete=true / smoke=false / native exit 0이다. 각 ZIP은 6영상을 포함한 18파일이다.

같은 protocol `806d7e8280d8fac8bbbb6015013b1752335fe0446c8e39bf8f9dd4fbf7c145ad`, task checkout `ef10b7a4c9a83481346d446e8a75aed655f72214`, scorer/collector 및 resolved configs가 확인됐다. ZIP 내부 `preset/source_run_id=null`은 수정하지 않는다. OFFICIAL 학습·제출 계보는 기존 registry와 checkpoint SHA로 별도 연결한다. 4800의 원 학습은 INTERRUPTED 상태이며 완료된 PERSONAL 평가로 이를 COMPLETE로 바꾸지 않는다.

4800 원본 ZIP은 Originals `data/raw/private_server_runs/go2/2026-10-09_windows_model4800_video_evaluation/`에 보존하고 [NVIDIA PERSONAL Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-go2-20261009-g2-submit-3-model4800-video-eval)에 게시한다. 이번 요청은 4800 게시이며 7450 ZIP은 Downloads `비교분석`에 보존된 분석 입력이다.

## 확인된 변화: 공식과 PERSONAL을 분리

| 지표 | 4800 → 7450 | 근거 / 해석 |
| --- | --- | --- |
| 공식 계단 survival | 99.0% → 99.8% | 운영진 답변: 개선 |
| 공식 계단 Tracking Score | 0.819 → 0.796 | 운영진 답변: 하락 |
| 공식 계단 점수 | 8.52 → 8.35 | 생존 약 +0.07보다 추종 약 −0.24 손실이 큼 |
| 공식 전방위 Tracking Score | 0.834 → 0.829 | 둘 다 survival 100%; 약 −0.06점 |
| 공식 시뮬레이션 / 종합 | 58.55 → 58.32 / 87.55 → 88.32 | 설계 의도 +1점 때문에 종합은 상승 |
| PERSONAL 계단 상행 오차 / 실패 | 0.28180 → 0.15570 / 8/392 → 4/388 | raw episode 평균; 낮을수록 좋은 오차 |
| PERSONAL 계단 하행 오차 / 실패 | 0.35888 → 0.14126 / 7/391 → 0/384 | raw episode 평균 |
| PERSONAL 계단 통합 오차 / 실패 | 0.32029 → 0.14852 / 15/783 → 4/772 | 공식 survival/Tracking Score로 환산하지 않음 |
| PERSONAL G2 평균 오차 | 0.09085 → 0.07699 | 로컬 개선인데 공식 추종은 하락 |
| PERSONAL G2 vx/vy/yaw 오차 | 0.03627/0.04592/0.05832 → 0.03189/0.04058/0.04518 | 세 축 평균 절대 오차 개선 |
| PERSONAL G2 xy_rmse / roll_pitch_rms | 0.09327 → 0.09493 / 0.04330 → 0.15349 | 다른 지표의 비용; 공식 감점 원인으로 단정하지 않음 |

계단의 최초 cohort는 각 정책 768개다. 실패 후 reset episode 때문에 783/772로 달라지므로 paired 독립 시행이나 공식 99.0/99.8%와 같은 분모로 취급하지 않는다. 보고서의 episode/step/n0/방향별 집계와 6개 seed×방향 조합에서도 로컬 계단 개선의 방향이 유지된다. G2에는 양쪽 384 timeout episode만 있어 reset 분모 차이가 없다.

## 현재 판단과 다음 질문

1. **평가 분포 coverage 차이를 먼저 조사한다.** 로컬 G5는 고정 12.5cm·vx=1/vy=0/yaw=0이고 공식은 10–15cm 범주에 명령·초기조건 분포가 미공개다. G2의 측면/회전 명령 범위·전환, 출발·계단 체류·reset/time 구간을 확인해야 한다. 특정 차이가 실제 원인인지는 아직 미확정이다.
2. **행동 trade-off는 조건부 후보로 남긴다.** G2 자세 RMS 증가, 일부 비계단 case의 횡오차·평균 오차 악화, 소수 stall 꼬리는 추가 진단 근거이지 공식 Tracking 구성이나 공식 yaw 문제의 직접 증명이 아니다. body-forward 진행 적분도 계단 완주 판정이 아니다.
3. **scorer/calibration 교체와 새 학습은 보류한다.** 같은 로컬 scorer/collector/config와 raw 재집계 일치는 현재 A/B 버전 불일치·로컬 집계 버그를 지지하지 않는다. 한 쌍에 맞춰 점수 가중치를 보정하지 않는다.
4. **과거 판정의 범위를 명확히 한다.** 10/05의 7450 PROMOTE·7050 fallback HOLD·4800 all-around REJECT는 당시 PERSONAL suite 후보 판단이다. 4800은 공식 계단·전방위 추종에서 상대 우위가 있는 필수 대조군이며 광범위 REJECT하지 않는다. R5의 공식 생존 이득도 유지한다. reward-effect HOLD는 그대로다.

가장 유용한 다음 질문은 **공식 G5/G2에서 R5 추종 손실이 어떤 높이·명령·출발/전환·초기조건에 집중되는가**다. 공식 수치 분해는 이미 받았으므로 재문의 대신 조건별 누락만 최소 확인한다. 이후 telemetry/coverage 확장은 별도 승인·범위 판단 사항이지 이번 반영으로 자동 실행하지 않는다.
