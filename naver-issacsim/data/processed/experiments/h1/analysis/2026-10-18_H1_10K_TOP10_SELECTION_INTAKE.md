# H1 기존 설정 10K 후보 TOP10 — 외주 의사결정 보고서 수납

## 원문·검증 범위

[받은 보고서](../../../incoming/other/reviewed/H1_10K_TOP10_SELECTION_20261018/H1_기존설정_10K_우선순위_TOP10_20261018.md) · [검토표 CSV](../../../incoming/other/reviewed/H1_10K_TOP10_SELECTION_20261018/H1_10K_전체후보_검토표_20261018.csv) · [수신 ZIP 원본](../../../incoming/other/reviewed/H1_10K_TOP10_SELECTION_20261018/received_original.zip).

2026-10-18 수신. ZIP 25,376bytes, SHA256 `37f90d47357792e50faa43bc4c34803caafaa3118ff5a76955497d0217f4b58b`, CRC PASS, 내부 MD/CSV 2파일을 bytes 그대로 보존했다. 다운로드 파일명은 `H1_10K_TOP10_%ED%8C%90%EB%8B%A8%EB%B3%B4%EA%B3%A0%EC%84%9C_%EA%B2%80%ED%86%A0%ED%91%9C_20261018.zip`; 저장소에서는 ZIP 이름만 `received_original.zip`으로 정리했다.

입력은 분석 snapshot `0793903`의 후보선정 묶음229파일이다. CSV는 **52행: OFFICIAL22/PERSONAL26/PLANNED4**, 순위1~10은 서로 다른 최종 설정10개다. 보고서·CSV의 상위3개 Run/config/평가 checkpoint SHA를 기존 상세 기록과 대조했다. 모든52행의 역사적 provenance를 재감사한 것은 아니다. 외주자의 GitHub 조회 주장은 원문에 귀속하며 수납자가 재현했다고 표시하지 않는다. 원 archive·episode·MP4 재집계, GPU 작업, 새 학습·평가는 없다.

## 외주 TOP10 — 실행 우선순위 제안, 승인 아님

Delta는 `h1-submit-2` 기준이며 전체 설정은 frozen preset과 각 Run의 resolved source로 확인한다. 동일 reward 연장은 총 학습 이력을 약10K까지 늘리는 제안이고 연속 fresh10K와 같다고 보장하지 않는다.

| 순위 | 최종 설정 delta | 제안 경로 |
| --- | --- | --- |
| 1 | lin=.65, ang=.60, action=-.0003 | JOINT fresh5K keeper4950에서 약+5K |
| 2 | action=-.0003 | fresh3K keeper2950에서 약+7K |
| 3 | orientation=-1.0 | fresh3K keeper2950에서 약+7K; 평가2850과 다름 |
| 4 | action=-.0001, feet_slide=-.35 | fresh3K keeper2950에서 약+7K; **OFFICIAL Run 완료 2026-10-18** |
| 5 | preset 그대로 / TERM50 | Fresh10K 대조 |
| 6 | lin=.65 | fresh5K keeper4950에서 약+5K |
| 7 | action=-.001 | fresh3K keeper2950에서 약+7K; 평가2850과 다름 |
| 8 | lin=.65, action=-.0001 | Fresh10K; 기존 resume와 별도 질문 |
| 9 | lin=.75, action=-.0001 | fresh3K keeper2950에서 약+7K; 평가2850과 다름 |
| 10 | lin=.55, action=-.0001 | Fresh10K; 기존 resume와 별도 질문 |

1위는 다축 추종 균형을 보인 JOINT5K의 rough 저속 개선, 2위는 정지·횡명령 제어와 rough 하위 꼬리, 3위는 자세 완화의 추종·균형 유지가 질문이다. 이는 외주자의 상대적 정보 가치 판단이지 성공 확률·공식 점수 예측이 아니다. TOP10 전부 실행을 뜻하지 않는다.

## 상위 Run 연결과 원문 보완

- **1위:** [JOINT Experiment](../../../../../research/experiments/h1/exp-h1-joint-tracking-balance.md), OFFICIAL Run `20261017-015509-h1-lintrack-065-angtrack-060-actrate-0003-fresh5`, 평가·keeper4950 SHA `2df0584057deb4dc15ab3c4470d52da29e5468bbb819fe3e4c66a928462bc478`. 원문이 auto-best4800/keeper4950 뒤 SHA 하나를 표기했지만 위 SHA는 **4950에만 해당**한다. auto-best4800 SHA는 `9dadfcad13f1cb9bfdb156330d9ec2a7ac4c25e6064e99e5701337ae8fd03095`로 다르다. 원문은 수정하지 않았다.
- **2위:** [ACTRATE Experiment](../../../../../research/experiments/h1/exp-h1-action-rate-relaxation.md), OFFICIAL Run `20261016-033023-h1-actrate-0003-fresh3k`, 평가·keeper2950 SHA `1cc2c03197097c21c642e8373c760b25664b9c859ed75b5dc07582a770473c4b`.
- **3위:** [ORIENT Experiment](../../../../../research/experiments/h1/exp-h1-rough-terrain-orientation-relaxation.md), OFFICIAL Run `20261006-133517-h1-orient-100-fresh3k-official`, 평가2850 SHA `6aedeced60562c1d496d5319d29b76cf9e26ff43df06827cb370f24f5313f7b0`; keeper2950 SHA `a0748cd294c52710806ef9dbd4c9ade3d20b40461b7e5f238f67c7eb36a76e5f`는 **미평가**다. 2850의 장점이2950에도 검증됐다고 쓰지 않는다.
- **4위:** [ACTRATE-0001 + FEETSLIDE-035 Experiment](../../../../../research/experiments/h1/exp-h1-action-foot-contact-stability.md), OFFICIAL Run `20261018-062435-h1-top04-same-reward-to10k`, parent keeper2950 SHA `c4b283509cc659e7bd47f5bf49eddbc387a43963d751ef353c632f48c7da1374`, +7050 requested / latest keeper9950 SHA `2008e2f4c93a820c1ab396839ede1ba493e7b8dca7fffc3bbacb8de5ea257569`. Completed/exit0/validation PASS; imported-parent provenance fields remain unverified. The keeper9950 PERSONAL A4000 camera-off scenario7 evaluation is COMPLETE/non-smoke: 3,072 validated cohorts / 3,074 episode rows, three-file ZIP without videos. Policy analysis/adoption remain pending/HOLD; see the detail's evaluation Release.

## 현재 상태

**REVIEWED / 일부 순위 실행됨.** TOP01, TOP02, TOP04의 실제 OFFICIAL continuation은 별도 Run 기록에 수납됐다. TOP04는 completed/PASS이며 model_9950 PERSONAL A4000 평가도 COMPLETE다. 정책 분석·채택은 대기/HOLD다. 나머지 순위의 상태는 개별 registry로 확인하며 완료로 일괄 처리하지 않는다. 기존 HOLD와 submission preset은 유지한다. 추천 수신이나 continuation 완료만으로 승격·제출 승인을 뜻하지 않는다.

새 reward 조합 대신 기존 설정의 장기 확인을 우선하자는 사용자 방향에 대한 자문 결과다. 로컬 혼합 지표·학습 reward만으로 제출을 대체하지 않으며 R2/R4/R6 공식 결과56.37/56.37/56.35를 개선했다고 주장하지 않는다. 매회 영상 생성 여부와 정량 평가 실행 방식은 이 수납으로 변경하지 않았다.
