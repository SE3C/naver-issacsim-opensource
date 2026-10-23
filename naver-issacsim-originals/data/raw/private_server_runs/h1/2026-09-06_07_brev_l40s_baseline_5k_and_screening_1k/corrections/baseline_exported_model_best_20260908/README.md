# Baseline exported model_best 교정 overlay

## 목적

원본 baseline archive의 `training/humanoid/exported/model_best.pt`는 1K checkpoint와 동일하다. 이 폴더의 `model_best.pt`는 같은 archive 안의 올바른 최종 파일 `model_4999.pt`를 추출해 만든 대체본이다.

## 교정 파일

| 파일 | bytes | SHA-256 |
| --- | ---: | --- |
| `model_best.pt` | 7,151,477 | `12882ba1da69a71e4249f348da075d71aae726314a5d66431b679f21e89b8bfd` |

## 원본 source

```text
naver-issacsim-nvidia/training/humanoid/logs/rsl_rl/humanoid/
2026-09-06_23-42-45_h1-baseline-5k-l40s-20260906_234238/model_4999.pt
```

동일 hash를 가진 원본 결과 별칭은 다음이다.

```text
results/h1_baseline_5k/h1-baseline-5k-l40s-20260906_234238/
checkpoints/h1_baseline_5000.pt
```

이 overlay는 raw archive를 수정하거나 삭제하지 않는다. archive를 풀어 exported `model_best.pt`가 필요할 때만 이 파일로 교체해 사용한다.

TERM50 영상의 잘못된 연결은 이 overlay로 고쳐지지 않는다. 해당 영상은 L40S/Isaac Sim에서 TERM50 checkpoint로 재렌더해야 한다.
