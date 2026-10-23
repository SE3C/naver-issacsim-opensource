# H1 fresh 조합 두 정책 보고서 수신·보존

2026-10-14 사용자 제공 분석 원문 두 건을 byte-for-byte 보존했다. 이번 작업은 수신·연결·백업이며 원자료 재분석, 정책 채택 또는 공식 점수 판정이 아니다.

| 수신 원문 | 원문 SHA-256 | 연결한 Experiment / checkpoint |
| --- | --- | --- |
| [H1_SHA14FD_MODEL2950_POLICY_ANALYSIS_20261014.md](../../../incoming/other/reviewed/H1_SHA14FD_MODEL2950_POLICY_ANALYSIS_20261014.md) | `925495f3ed90e409237c9ef95f99b14e80f76a0352fd2120e2ff2f22d7e0f0f7` | [action+airtime](../../../../../research/experiments/h1/exp-h1-action-airtime-fresh-interaction.md), `model_2950` / `14fd9ad432dfc2ba7696b0d48d9a31753f42c74727083429cc9f2c7299aaffd6` |
| [H1_C4B2_POLICY_ANALYSIS_20261014.md](../../../incoming/other/reviewed/H1_C4B2_POLICY_ANALYSIS_20261014.md) | `6112a9e887a1a839884b194175bce91bbec0e2cc42620f4ee577e9cd17cf6191` | [action+feet_slide](../../../../../research/experiments/h1/exp-h1-action-foot-contact-stability.md), `model_2950` / `c4b283509cc659e7bd47f5bf49eddbc387a43963d751ef353c632f48c7da1374` |

두 보고서의 입력 ZIP 이름·checkpoint SHA는 이미 보존된 해당 Windows PERSONAL 평가 ZIP과 일치한다. 원문의 `source_run_id=null` / `preset=null`은 변경하지 않는다. OFFICIAL 학습 연결은 보고서 단독으로 추정하지 않고, 위 Experiment 문서의 별도로 검증된 train index·SHA를 근거로 한다.

## 확인된 학습 Run ID — 원문 null을 보완하는 외부 연결

| 보고서 | Source training Run ID | 출처 |
| --- | --- | --- |
| H1_SHA14FD_MODEL2950_POLICY_ANALYSIS_20261014.md | `20261013-144616-h1-actrate0001-airtime025-fresh3k` | OFFICIAL train index의 `model_2950` SHA와 평가 policy SHA 일치; 위 action+airtime Experiment |
| H1_C4B2_POLICY_ANALYSIS_20261014.md | `20261013-153313-h1-actrate0001-feet_slide-fresh3k` | OFFICIAL train index의 `model_2950` SHA와 평가 policy SHA 일치; 위 action+feet_slide Experiment |

이는 학습 Run ID이며 Windows 평가 ID와 구분한다. 원문 입력에 없던 근거를 원문 자체가 확인했다고 소급하지 않는다.

원문 내용·결론과 기존 채택 판단은 변경하지 않는다. 원문 2건은 Analysis Git에 보관하며 학습 압축본 2건·평가 ZIP 2건은 기존 Release와 Originals LFS에 보존했다. Downloads의 해당 6파일은 보존·푸시 확인 후 복구 가능한 휴지통으로만 이동한다.
