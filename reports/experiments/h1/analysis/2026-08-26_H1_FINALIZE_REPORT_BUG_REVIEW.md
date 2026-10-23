---
id: h1-finalize-report-bug-review-20260826
source_type: reviewed_bug_evidence
category: personal_server_tooling
robot: H1
reviewed_at: "2026-08-26"
trust_level: artifact_verified_plus_reported_official_runtime_evidence
authority: "개인 NVIDIA/Brev 실행 원본과 보관 코드를 직접 대조하고, 2026-08-26 수신 상태 보고서에 기록된 공식 서버 code/runtime 확인값을 구분해 반영한 도구 신뢰성 검토다. 공식 평가·정책 품질 판단은 포함하지 않는다."
---

> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/experiments/h1/analysis/2026-08-26_H1_FINALIZE_REPORT_BUG_REVIEW.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.


# [분석] H1 finalize/report 버그 검토

> 관리 안내 (2026-10-13): **분석** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](<../../../../research/EXPERIMENTS.md>)를 확인한다.

## 결론

이번 `exp1_termination_m50_long` 실행의 자동 `report.html`은 **파일 무결성·기본 설정 표시는 쓸 수 있지만, 자동 정책 판정과 best checkpoint의 전역 최적 보장에는 쓰면 안 된다.**

확정된 문제는 두 가지다.

1. report는 action std `1.206`만으로 “거의 학습이 안 됨(iter 부족 의심)” 경고를 낸다. 하지만 같은 run의 전체 scalar 자료에는 후반 episode length 약 869, terrain 약 5.90, timeout 약 79%, base-contact termination 약 21%가 기록되어 있다. 따라서 이 규칙은 이 run에서 false-positive다.
2. report/finalize가 고른 reward `6.749` at step 23101과 전체 25,000 scalar CSV의 최대 reward `6.904` at step 24012가 다르다. 이어서 finalize가 intermediate checkpoint 250개를 삭제해, 현 아카이브에서는 후보 checkpoint를 다시 고를 수 없다.

## 증거와 재현성

`ncrc bug files.zip`은 설명문이 아니라 report, event, checkpoint, YAML의 재현 증거 묶음이다. SHA-256은 다음과 같다.

```text
b60868c71ff425c6c9596bf781fc70f08f38a17dcca4e20faf9d4a54cf8426
```

ZIP 안의 7개 파일은 이미 보관한 H1 long-run tar archive의 대응 파일과 모두 SHA-256이 일치한다. 즉 새 원본을 추가 보관하지 않고 기존 archive를 정본으로 유지한다.

| 비교 대상 | 결과 |
| --- | --- |
| exported `env.yaml`, `model_best.pt`, `report.html` | 기존 long-run archive와 동일 |
| run `env.yaml`, `agent.yaml`, `model_23100.pt`, TensorBoard event | 기존 long-run archive와 동일 |
| full scalar CSV | 25,000 rows, `Train/mean_reward` max 6.903780 at 24012 |
| report/finalize console | 6.749 at 23101, `model_23100.pt` 선택 |

수신 상태 보고서에는 공식 서버에서 다음 Python 확인 명령을 실행했다고 기록돼 있다.

```text
DEFAULT_SIZE_GUIDANCE['scalars'] = 10000
STORE_EVERYTHING_SIZE_GUIDANCE['scalars'] = 0
```

이는 이 작업공간에서 독립적으로 다시 실행한 출력은 아니며, 사용자가 제공한 공식 서버 확인 기록이다. 원문 두 개는 `data/processed/incoming/other/inbox/h1_finalize_bug_status/`에 보존한다. 짧은 문서는 긴 상태 보고서의 중복 요약이다.

## 코드 수준 확인

보관된 H1 `_finalize.py`의 `find_best_model()`은 `EventAccumulator(str(run_dir))`를 size guidance 없이 만들고 그 `Scalars()` 결과에서 최대값을 고른다. 위 공식 서버 확인 기록의 default scalar limit 10,000과 개인 run의 25,000개 scalar/실제 peak 불일치는 이 선택이 전체 기록이 아닌 제한된 EventAccumulator 결과에 의존한다는 강한 근거다.

따라서 “25,000개의 raw scalar 전체 최고점을 고르지 못한 사례”는 확인됐고, 기본 10,000 scalar 제한은 원인으로 **높은 신뢰도**로 연결된다. 다만 모든 장기 run에서 반드시 다른 checkpoint가 고르거나, raw reward 최고 checkpoint가 실제 대회 성능도 더 좋다고 일반화하지 않는다.

같은 코드의 `_diag_verdict()`는 `action_std > 0.9`이면 다른 지표와 관계없이 학습 부족 경고를 붙인다. 이번 run의 long-horizon 지표와 모순되므로, 이 임계값은 정책 품질 또는 학습 성공의 단독 판정 규칙으로 사용하지 않는다.

## 영향과 우선순위

| 항목 | 심각도 | 이유 |
| --- | --- | --- |
| 10k 제한 아래의 자동 best 선택 후 intermediate checkpoint 삭제 | 높음 | 전체 raw peak가 누락될 수 있고, 더 높은 raw reward 시점 또는 evaluator 우수 checkpoint를 사후 검증할 수 없음 |
| action std 단독 실패 경고 | 중간 | 사용자가 정상 진행 run을 불필요하게 실패로 오판할 수 있음 |
| report의 설정·hash·종료 정보 | 낮음 | 이번 자료에서는 원본과 일치하며 계속 참고 가능 |

## 운영 규칙

1. `report.html`의 `best reward`, 자동 경고는 진단 힌트로만 보고 TensorBoard 전체 event·scenario evaluator·play 영상으로 교차검증한다.
2. finalize 전에 `logs/<run>/` 전체와 모든 `model_*.pt`를 별도 archive로 복사한다. cleanup 이후에는 후보 재선정이 제한된다.
3. 공식 서버 제공 파일은 직접 수정하지 않는다. 수신 상태 보고서 기준으로 운영진·개발팀에 제보와 원본 출력 전달은 완료됐고, 현재는 개발팀 검토 답변을 기다린다.
4. 다음 실행에서는 선택 로그, TensorBoard runtime version, exact dependency version을 함께 export한다. cleanup 방지 CLI가 보이더라도 공식 안내 또는 운영진 지시가 있을 때만 사용한다.

## 비결론

이 검토는 `termination_penalty=-50`의 최적성, 보행 품질, 공식 점수, 공식 서버 코드의 일반적 결함을 증명하지 않는다. 이번 개인 run과 이 버전의 report/finalize 조합에서 확인된 제한만 다룬다.
