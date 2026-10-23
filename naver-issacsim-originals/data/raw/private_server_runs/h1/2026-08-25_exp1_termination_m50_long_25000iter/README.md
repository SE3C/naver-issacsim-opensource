# H1 개인 서버 장기 실행 원본 보관

## 분류

- 실험: `exp1_termination_m50_long`
- 실행 폴더 timestamp: `2026-08-25_16-11-27`
- 성격: 개인 NVIDIA/Brev 검증 실행
- 금지 해석: 공식 서버 결과, 공식 점수, 제출 정책의 성능 증명

`received/`에는 받은 원본 archive를 이름·바이트·내용 그대로 보관한다. archive 내부를 Git 작업트리에 다시 풀어 중복 보관하지 않는다. 검증 분석은 분석 저장소의 `data/processed/experiments/h1/2026-08-25_PERSONAL_SERVER_TERMINATION_M50_25K.md`를 본다.

## 수신 원본 manifest

| 수신 파일 | bytes | SHA-256 |
| --- | ---: | --- |
| `h1-training-20260826_075522_KST.tar.gz` | 81,871,116 | `b8ce2688a69067b9bdab24fd7232d04d04c5622064919cacf4c6f5dec072ffc7` |
| `h1_training_visualizations.zip` | 7,615,712 | `e071a12fdff61801bb044082719efecab4be996a1a345f9957c2f33489360ec7` |
| `H1_exp1_termination_m50_long_25000iter_통합분석.zip` | 11,023 | `ad00d07f6c486eaed3e75e7335a68a31e99054c3a79ed6f3fda5a1528ad48043` |

세 archive는 Git LFS 대상으로 보관한다. 통합분석 ZIP을 풀어 얻은 Markdown은 원문 보존용으로 analysis repository의 `incoming/other/inbox/personal_server/`에 따로 둔다. 그것은 검증 전 수신 분석 원문이며, 이 README 또는 AI 핵심팩의 결론 근거가 아니다.

## 핵심 산출물 식별

archive의 long-run `model_23100.pt`와 `exported/model_best.pt`는 다음 hash로 같다.

```text
974f97f7ad58c01ccd77568e0e536a8c1dfeaa57392f526f1486ffe699dd7f48
```

이 hash는 파일 동일성만 뜻한다. 공식 시나리오 점수나 정책 품질을 뜻하지 않는다.

## 버그 재현 증거 ZIP의 중복 판정

2026-08-26에 받은 `ncrc bug files.zip`(SHA-256 `b60868c71ff425c6c9596bf781fc70f08f38a17dcca4e20faf9d4a54cf8426`)은 이 archive의 exported YAML/checkpoint/report, run YAML/checkpoint/TensorBoard event와 모두 SHA-256이 일치하는 부분 묶음이다. 따라서 중복 ZIP은 다시 LFS에 보관하지 않는다. 검토 결과는 analysis repository의 `data/processed/experiments/h1/2026-08-26_H1_FINALIZE_REPORT_BUG_REVIEW.md`에 기록한다.
