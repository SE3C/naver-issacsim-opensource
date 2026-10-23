# H1 joint tracking + 자세·고관절 완화 model2850 — 보고서 수납 / HOLD

## 원문과 확인 범위

- [받은 보고서](../../../incoming/other/reviewed/H1_JOINTTRACK_ORIENT_MODEL2850_POLICY_ANALYSIS_20261017/H1_JOINTTRACK_ORIENT_MODEL2850_POLICY_ANALYSIS_20261017.md), [원본 ZIP](../../../incoming/other/reviewed/H1_JOINTTRACK_ORIENT_MODEL2850_POLICY_ANALYSIS_20261017/H1_JOINTTRACK_ORIENT_MODEL2850_POLICY_ANALYSIS_20261017.zip)과 내부 14파일을 bytes 그대로 보존했다. ZIP 1,819,711bytes, SHA256 `7cfdb1317c39bf051da463b9a5e9fb38a3ba269c5343c57e90e5edb4b4c67547`; CRC PASS.
- 본 수납은 보고서와 첨부 case/seed CSV·검증 JSON의 대조다. 원 episode 재집계·첨부 `reproduce_analysis.py` 실행·MP4 재판독·GPU 작업은 하지 않았다. 아래 영상·생존 수치는 보고서의 분석 결과이지 수납자의 독립 재실행 결과가 아니다.
- [case metrics](../../../incoming/other/reviewed/H1_JOINTTRACK_ORIENT_MODEL2850_POLICY_ANALYSIS_20261017/case_metrics.csv), [seed metrics](../../../incoming/other/reviewed/H1_JOINTTRACK_ORIENT_MODEL2850_POLICY_ANALYSIS_20261017/case_seed_metrics.csv), [verification](../../../incoming/other/reviewed/H1_JOINTTRACK_ORIENT_MODEL2850_POLICY_ANALYSIS_20261017/verification.json), [영상 검사](../../../incoming/other/reviewed/H1_JOINTTRACK_ORIENT_MODEL2850_POLICY_ANALYSIS_20261017/video_inspection.json)도 보존한다. 이 보고서 패키지 자체에는 checkpoint·원 episode JSONL·MP4가 없다.

## 실제 학습 Run과 평가 연결

[Experiment·학습 원본·Release](../../../../../research/experiments/h1/exp-h1-joint-tracking-posture-relaxation.md): 사용자 후보2, OFFICIAL Run `20261017-072659-h1-lintrack-065-angtrack-060-actrate-0003-orient`, fresh/no parent·seed42·4096env·3000요청/console2999, save_interval50, **COMPLETED/exit0/PASS**. 최종 override는 `h1-submit-2 + action=-0.0003 + orientation=-1.0 + hip=-0.1 + ang=0.60 + lin=0.65`다. Full resolved source는 보존된 train archive의 env/agent/reward source다.

- 평가 **model_2850.pt** SHA `4a343750b47920d3b49e5e3ec7a3bf49fd9403d5b51a3727604971e6b7b0025d`는 앞선 수납에서 official checkpoint index·보존 bytes·평가 manifest 사이에 연결됐다. 최신 keeper **model_2950.pt** SHA `c342e995ec77a2fb5f2845778d4e85146a244a4b4e311c29fe6f4275c539c216`는 별도 미평가 정책이다.
- 보고서 입력 ZIP SHA `af58e8f10165dbce7bd1c0363c09f523db925d9775870549819f94854fe4f6b9`는 [기존 publication manifest](https://github.com/SE3C/naver-issacsim-eval/blob/main/publications/2026-10-17_h1_joint_tracking_posture_model2850/publication_manifest.json)와 같다. PERSONAL Windows H1 scenario7 **COMPLETE/non-smoke**, 128env × seeds4201/4202/4203 ×8cases, 20초·3072행, protocol `d406a296d2c0e5a7deee4138de7df87532d2815ae9b65af999d7a8f0b7062d34`다.
- 원 평가의 `source_run_id/preset=null`과 보고서의 “조회 범위에서 학습 계보 미확인”은 보존한다. 위 연결은 팀의 별도 train index와 publication 근거로 보완한 것이며 원문이나 null을 덮어쓰지 않는다. 평가 snapshot의 baseline reward는 실제 학습 reward가 아니다.

## 보고서 핵심 결과

| 축 | 보고된 수치와 해석 |
| --- | --- |
| 생존 | 3072/3072가 20초 timeout; terminated/contact 종료0. 생존은 명령 추종·지형 완주와 별도다. |
| H1 정지 | body-frame 전진 적분 **−0.719m**, world XY 종료 잔류 평균0.883m. 의도치 않은 후진 성분. |
| H2 전진 | body 전진13.465/15m, tracking0.15778. |
| H3 좌우 | body 전진 **−0.679m**, vy 절대오차0.06271m/s, world 종료 잔류1.160m. 원점 복귀는 공식 독립 채점 요구가 아니라 보조 진단이다. |
| H4 회전 | yaw 절대오차0.08520rad/s. |
| H5 rough | 전진 평균/P05/최소 **8.024/7.460/6.721m**(명령 적분10m), tracking0.21625, vx 오차0.10904m/s. stall 평균0.00952, stall>.05는1/384로 **주된 약점은 완전 정체보다 지속 속도 손실**이다. |
| H6·H7 | 경사 상/하 전진19.165/18.974m(목표20m), 밀침8.875m(목표10m). |

전체 episode 평균 tracking0.1461466193은 내부 8-case 동일가중 지표이며 공식 점수/Tracking Score가 아니다. 평가 seed3개는 독립 학습 seed3회가 아니다.

## 영상과 판정

보고서는 6개 영상 각1000프레임의 축소 픽셀 검정 검사와 선택 시점 관찰을 기록했다. stairs의 f0/f2, 나머지5영상의 f0가 검정이고 **교대 black/valid 결함은 관찰되지 않았다**고 한다. 이는 전 프레임 행동의 수동 판독이나 본 수납자의 재검사가 아니다. 직립·이동과 일부 장애물 접근은 보이나 계단 중앙 다단 완주·20초 내내 rough/경사 접촉은 미입증이다. 공식 H1 정량 case에 없는 계단·박스의 완주 미입증만으로 자동 탈락시키지 않는다.

**정책 판정 HOLD, 기존 제출 대체·승격 없음.** 생존에도 H1/H3 후진 성분과 H5 속도 손실이 남는다. 이전 JOINT fresh5K4950(`2df05840…`)보다 보고서 수치상 rough·정지·잔류가 불리하지만, 학습량3K 대5K와 여러 reward가 달라 자세·hip 완화의 독립 효과나 matched A/B 우열로 단정하지 않는다. 다른 ORIENT-100/ACTRATE-001 model2850과도 다른 정책이다.

다음 대상으로 기존 저장 평가끼리 조건 확인 후 CPU 비교를 제안했을 뿐, 이번 보고서에서 비교를 수행한 것은 아니다. 공식 점수·새 제출·새 GPU 실행·자동 추가 학습 승인은 없다.
