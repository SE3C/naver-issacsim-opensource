> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/experiments/h1/analysis/2026-10-15_ACTRATE0001_UNCHANGED_MODEL4699_POLICY_REVIEW.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# ACTRATE-0001 unchanged +2K model_4699 정책 보고서 수납

> **후속 판정:** [부모2700·무변경4699·복원4650 CPU 비교](<2026-10-15_ACTRATE_PARENT_UNCHANGED_RESTORATION_COMPARISON_INTAKE.md>)가 완료됐다. 이 단독 보고서의 HOLD는 당시 판단이며, 현재는 세 후보의 범용·전진/험지 대표 선정에 한해 **4699 REJECT**다. 학습 COMPLETED/PASS·원본·정지/yaw 참고 역할은 유지한다. 아래 ‘다음 대조’는 이 후속 수신 전 제안이다.

## 원문·신원·검토 범위

- [수신 원문](<../../../received/H1_ACTRATE-0001-UNCHANGED-CONT2K_POLICY_ANALYSIS_20261015.md>)은 바이트 그대로 보존한다. 이번 수납은 MD 검토이며 ZIP/MP4/GPU 평가를 다시 수행한 것이 아니다. 아래 숫자와 영상 관찰은 제공 보고서의 결과다.
- [Experiment](<../../../../research/experiments/h1/exp-h1-action-rate-relaxation.md>): OFFICIAL 학습 Run `20261014-111135-h1-actrate-0001-unchanged-cont2k`, model_2700에서 reward 변경 없이 +2K, 완료 4699/4700. 평가 model_4699 SHA `722b35a127f7ae4209d94a9111ac5ee02071ba7f3b985dc9cdc0760bbe48f646`는 이미 확인된 학습 checkpoint index와 연결된다.
- [PERSONAL Windows 평가 Release](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261015-exp-h1-action-rate-relaxation-model4699-video-eval): 6영상과 별도 camera-off H1 scenario7, 128 env × 3 seeds × 8 cases, COMPLETE/non-smoke. 원문 preset/source_run_id=null 및 학습 imported-parent provenance=false/null은 외부 SHA 연결로 고쳐 쓰지 않는다.

## 보고된 결과와 판정

3,072/3,072 episode가 20초 생존했고 base-contact 종료는 0이다. 하지만 H5 rough 진행 평균/P05/최소는 **7.919/7.427/6.239m**(명령 10m), 384건 모두 9m 미만이다. 세 평가 seed 모두 평균 7.9m 수준이므로 단일 최악 사례만의 문제가 아니다. H2/H6 상·하/H7 진행은 **13.972/19.007/18.834/8.981m**(명령 15/20/20/10m). H1/H3 body-frame 전진 적분은 **−0.724/−0.741m**이다. 정지 stall=0은 이동 명령 분모가 없다는 뜻이지 완벽한 정지 성공이 아니다.

**HOLD**: 범용 대표나 전진/험지 주후보로 승급하지 않는다. 생존과 action 변화 비용 측면의 참고 후보로 보존하되 기존 model_2700을 대체할 근거는 없다. 보고서의 2700 대조 표는 보고서 수준 비교이며 새 matched raw A/B나 +2K 학습의 인과 효과를 검증한 것이 아니다. 물리 torque/foot slip도 직접 측정하지 않았다.

`04_random_rough.mp4`는 f0와 홀수 프레임 포함 **501/1000 검정 프레임**이 보고됐다. 캡처 결함을 정책 낙상으로 세지 않는다. 계단 중앙 다단 완주·정량 boxes 성공은 입증되지 않았으며, 6영상과 camera-off 평가는 다른 episode다.

## 다음 대조

새 GPU 실행 대신 기존 model_2700 raw와 CPU 조건 대조를 먼저 한다. [ACTION 복원 model_4650](<2026-10-15_H1_MODEL4650_LINTRACK065_POLICY_REVIEW.md>)과의 같은 부모 control 비교도 이제 양쪽 보고서·raw가 존재한다. 서로 다른 평가 checkpoint 선택 번호(4699 대 4650), source/PPO/terrain/reset parity와 단일 학습 seed 한계를 명시하고 원문 표만으로 reward 효과를 확정하지 않는다. 이번 수납은 신규 학습·제출·공식 점수·추가 GPU 실행 승인이 아니다.
