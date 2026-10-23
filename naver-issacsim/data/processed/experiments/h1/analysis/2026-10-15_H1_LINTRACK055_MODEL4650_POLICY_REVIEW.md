# H1 lin=.55 / action=-.0001 resume model4650 — 보고서 수납·HOLD

**2026-10-16 후속:** [4정책 원자료 코호트 비교](2026-10-16_H1_LIN055_FOUR_POLICY_COHORT_INTAKE.md)가 수납됐다. C는 무변경 B의 rough 진행을 일부 복구하지만 부모 A·lin=.65 D에 전반적 우월성은 없으며 HOLD 유지다. 아래 CPU 비교 권고는 이미 이 후속에서 수행된 범위이며 새 GPU 실행 요청이 아니다.

## 원문과 계보

- [사용자 제공 원문](../../../incoming/other/reviewed/H1_ACTRATE0001-LINTRACK055_POLICY_ANALYSIS_20261015.md): 17752 bytes, SHA-256 `8bda314c32a82cc5a075c501a8a3444fc8fdd303ee8682d51223be821b703bf0`. 내용 bytes 그대로 보존했다.
- Experiment: [action-first planar tracking switch](../../../../../research/experiments/h1/exp-h1-action-first-planar-tracking-switch.md). 실제 OFFICIAL Run `20261015-105910-h1-actrate0001-lintrack-055-from2700-plus2k`, 부모2700에서 +2000, COMPLETED/exit0/validation PASS, console4699/4700. 최종 preset-relative config는 `h1-submit-2 + lin=.55 + action=-.0001`.
- 보고서 정책 SHA `e8a358a50832f6653b1e558788a5a676ab9a849d3ec6c64e3ed2430e9ff41814`는 앞서 보존한 OFFICIAL checkpoint index의 keeper `model_4650.pt`와 일치한다. 최신 keeper4650은 console terminal4699와 다르다. 원 평가의 source_run_id/preset=null 및 imported-parent provenance=false/null은 유지하며 학습 연결은 별도 SHA 대조다. 다른 model4650(lin=.65/ce7ad586, ACTION 복원/a8249db4)과 구분한다.
- [학습 Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261015-exp-h1-action-first-planar-tracking-switch-lin055-resume2700-plus2k) · [PERSONAL 평가 Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261015-exp-h1-action-first-planar-tracking-switch-lin055-model4650-video-eval).

## 제공 보고서의 주요 결과

보고서는 기존 18파일 ZIP의 raw episode 재집계·MP4 프레임 감사를 수행했다고 기록한다. **이번 수납은 MD·기존 identity 기록 대조이며 episode 재계산·영상 디코딩·새 GPU 실행을 하지 않았다.** 아래 수치는 제공 보고서의 값이다.

| 진단 | 보고 값 |
|---|---|
| PERSONAL full 평가 | 128env ×3평가seed ×8case,3072/3072 20초 timeout; 접촉 종료0 |
| H2 전진 / H7 push body 진행 | 14.715/15m,9.887/10m |
| H6 상·하경사 body 진행 | 19.684/19.581m (각 nominal20m) |
| H1 정지 world XY 종료 순변위 크기 | 평균 .702m |
| H3 횡왕복 world XY 종료 순변위 크기 | 평균2.363m,최소2.294/최대2.410m; vy 절대오차 .0714m/s |
| H5 rough body 진행 mean/P05/min | 9.242/8.859/8.256m; stall>.05는0/384 |
| H4 yaw 절대오차 | .1126rad/s |
| 전체 혼합 tracking | episode 가중평균 .148092; 단일 물리 단위·공식 점수 아님 |

## 판정과 해석 경계

**보고서 수납 완료 / 범용 후보 HOLD.** 전진·경사·push 보행은 조건부 참고 후보로 유지하되, 정지 위치 유지·횡이동 경로 진단 및 계단 중앙 다단 통과의 증거가 부족하다. 단일 정책 분석이므로 lin=.55의 상대 우월성·reward 인과효과·공식 점수 개선은 확인되지 않았다. H3 body-frame 횡속도 명령을 왕복했다고 world 원점 복귀가 필수인 것은 아니다. world 순변위는 응용상 경로/위치 진단이며 그 자체를 공식 추종 실패·낙상 판정으로 바꾸지 않는다.

보고서상 `01_stairs.mp4`는 f0+모든 홀수500개,총501/1000 black이고 유효 짝수 프레임에서 이동이 관찰됐다. 나머지5개는 f0만 black이다. capture 결함을 정책 낙상으로 세지 않으며, 영상 초반 rough/boxes 패치를 벗어난 뒤 평지를 20초 전부 험지 주행으로 취급하지 않는다. 계단 완주·복구시간·slip 정량은 미입증이다.

다음 판단은 기존 부모2700·무변경4699·lin=.65 등 보존 원자료의 source/config/cohort 호환을 확인한 **CPU 비교**에서 H1 drift,H3 vy/yaw와 world 진단,H4 yaw,H5 mean/P05/min을 함께 보는 것이다. 이 권고는 새 GPU·학습·렌더 또는 비교 실행 승인이 아니다. 원문을 수정하거나 재게시용 Release asset으로 중복 첨부하지 않는다.
