# H1 다음 가설 권고 수납 — 기존 CSV 교차 비교와 미실행 제안

## 출처·검토 범위

- [받은 보고서 원문](../../../incoming/other/reviewed/H1_NEXT_HYPOTHESIS_DECISION_20261015/H1_다음_학습가설_선택_보고서_20261015.md)과 CSV·JSON·Python·SVG **7개**를 내용 bytes 그대로 보존했다. ZIP의 UTF-8 filename flag 누락만 명시적으로 해석해 한글 파일명을 복원했다. 원문 수정·첨부 코드 실행·새 GPU 작업은 없다.
- [Originals 원본 ZIP](https://github.com/SE3C/naver-issacsim-originals/blob/main/data/raw/external_analysis/h1/2026-10-15_next_hypothesis_decision/H1_NEXT_HYPOTHESIS_DECISION_20261015.zip): 26,055 bytes, SHA-256 `befb4a37c61cbd2084621a9c404cb600587e764f411ac9910682cd4e8200d2d8`, CRC PASS.
- 외부 분석은 이전 4정책·부모/무변경/복원 비교의 **기존 파생 CSV를 교차 계산**했다. 이번 수납에서 보고서·CSV 및 기존 두 번들의 대응 수치를 대조했으며, 원본 episode/MP4를 다시 처리하거나 물리 궤적을 재현한 것은 아니다. 당시 진행 중이던 Optuna 도구 분석은 이후 [별도 CPU 검토 기록](../../../operations/2026-10-15_OPTUNA_EXTERNAL_CPU_REVIEW_INTAKE.md)에 수납했으며 이 H1 보고서가 그 결과를 대신하지 않는다.

## 새로 확인된 비교 — 옛 lin=.65 resume L 대 무변경 B

| 구분 | OFFICIAL source training Run | checkpoint / SHA |
|---|---|---|
| 부모 A | `20261009-142350-h1-actrate-0001-fresh3k` | model2700 / `e54d3389…93ca7ae` |
| LINTRACK 전환 L | `20261010-154926-h1-actrate0001-lintrack065-from2700-plus2k` | model4650 / `ce7ad586…9dea70` |
| 무변경 연장 B | `20261014-111135-h1-actrate-0001-unchanged-cont2k` | model4699 / `722b35a1…48f646` |

L은 같은 부모2700에서 lin .50→.65, action -.0001 유지 +2K다. ACTION 복원 model4650/SHA `a8249db4…`와 다르다. 원 평가의 source_run_id=null과 imported-parent provenance=false/null은 외부 SHA 연결로 덮어쓰지 않는다.

| 기존 CSV 기준 | L | B | L−B |
|---|---:|---:|---:|
| H5 rough body 진행 평균 (m) ↑ | 9.546 | 7.919 | **+1.626684** |
| H5 진행 주변 분포 P05 (m) ↑ | 9.228 | 7.427 | +1.801 |
| H4 yaw 절대오차 (rad/s) ↓ | .179056 | .091892 | **+.087164** |
| H3 world 종료 잔류 (m) ↓ | 2.397547 | .581193 | **+1.816354** |

[H5 파생 CSV](../../../incoming/other/reviewed/H1_NEXT_HYPOTHESIS_DECISION_20261015/derived_H5_L_vs_B.csv)에서 대응 키 **384/384건의 진행 차이가 양수**이며, 짝 차이의 P05는 **+1.126082m**, 최소는 **+.664268m**다. 이 값은 두 주변 분포 P05의 차이와 다른 통계다. Mixed tracking 차이는 −.001305지만 서로 다른 단위의 혼합 지표이며 yaw·횡잔류 손실을 상쇄했다고 보지 않는다. L은 부모 A보다 H5 평균 진행이 .402305m 낮다.

**판단:** 기존 CSV 수준의 L 대 B 비교 대기는 해소됐다. lin=.65가 무변경 연장보다 진행을 유지하는 신호와 yaw/횡잔류 비용이 함께 있으므로 L의 **HOLD 유지**, 범용 PROMOTE 없음. L4650은 선택 checkpoint, B4699는 endpoint다. 동일 키·단일 학습 seed·서로 다른 checkpoint 선택 및 train-side 전체 조건 미독립검증 때문에 reward 인과효과나 공식 점수 개선은 미확정이다. 원본 episode 직접 재집계와 구분한다.

## 다음 가설 권고 — 사용자 미선택·Run 미발급

| 순위 | 외부 권고 | 비교 질문 |
|---|---|---|
| 1 | 같은 ACTRATE 부모2700에서 **lin .50→.55**, action **-.0001 유지**, +2K resume | .65보다 약한 변경으로 진행 유지와 yaw/횡잔류 비용을 절충할 수 있는가? |
| 2 | `h1-submit-2` 기준 **action -.0005→-.0003만 변경**, fresh3K | action 완화의 중간값에서 정지·추종·rough 균형을 얻는가? |

이들은 최적값·확정 계획·새 실행 기록이 아니다. 사용자 선택 전 새 Experiment/Run·PLANNED 실행을 만들거나 기존 미실행 body-rate/airtime 계획을 대체하지 않는다. 선택하면 preset-relative override·실제 full resolved config·parent SHA·fresh/resume·학습량을 분리해 기록한다. 보고서의 진행/yaw 임계값은 **외부 제안 기준**이며 검증된 공통 채택 gate로 승격하지 않는다.

## 그대로 채택하지 않는 서술

- 보고서는 전달 패킷에 없던 `06_HUMANOID_TRAINING_CODE.md`, `01_현재상태와자료안내.md`를 입력 근거처럼 인용했다. 현재 저장소에 13개 활성 reward·feet_slide=-.25 설명이 있더라도 이 보고서 자체가 부모의 **전체 native resolved config를 검증한 증거는 아니다**. 보존 evidence의 9개 변경 가능 값과 전체 활성 항목의 확인 범위를 구분한다.
- “indexed resume만”이라는 결론은 현행 절차와 다르다. [19번](../../../ai_library/19_ISSACSIMZ_EXTERNAL_EVIDENCE_CLI.md)은 기존 evidence/index가 있으면 `--from-run`과 검증한 `source_path`, 단일 native `.pt`만 있으면 **`--import-checkpoint`** 경로를 지원한다. import는 부모 provenance를 자동으로 verified로 만들지 않는다. 실행을 선택할 때 실제 서버 파일·index/지원 경로·checkpoint SHA를 확인하고 경로를 추측하지 않는다.
- 선택 checkpoint 차이를 이유로 자동 checkpoint 토너먼트·새 GPU 평가·추가 학습을 실행하지 않는다. 충분한 resume의 대표 정책은 기존 원칙대로 final native checkpoint가 기본이며, 예외는 후반 terrain/tracking/fall의 공동 악화 근거가 필요하다.

[Registry](../../../../../research/EXPERIMENTS.md) · [LINTRACK 전환 Run](../../../../../research/experiments/h1/exp-h1-action-first-planar-tracking-switch.md) · [부모/무변경/복원 비교](./2026-10-15_ACTRATE_PARENT_UNCHANGED_RESTORATION_COMPARISON_INTAKE.md).
