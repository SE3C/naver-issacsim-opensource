# H1 Brev L40S baseline 5K 및 screening 1K 원본

## 범위

- 실행 시기: 2026-09-06~07 KST
- 실행 환경: 개인 NVIDIA Brev L40S
- baseline: 기본 H1 reward, 4096 environments, seed 42, 5000 iterations
- screening: TERM50, YAW075, RECOVERY를 각각 1000 iterations 실행
- 용도: 재현·감사 가능한 원본 보존. 공식 운영 서버 결과나 제출 점수로 해석하지 않는다.

`received/`의 두 archive는 다운로드받은 바이트를 변경하지 않고 Git LFS로 보존한다. 상세 판정은 analysis 저장소의 검토 문서를 기준으로 한다.

## 수신 원본 manifest

| 파일 | bytes | SHA-256 |
| --- | ---: | --- |
| `h1-baseline-5k-20260907_102236_KST.tar.gz` | 473,643,918 | `a3499ca1776cf2dd61180f5b8b1c4356fe9e80c8c17402c3dfa7765c544cbcb4` |
| `H1_SCREENING_ALL_20260907_122939_KST.tar.gz` | 277,949,983 | `aa63a897391e6d6577181cef51d7bacf388066e28a606e51afcbea02798105df` |

## 중대한 원본 주의사항

원본을 임의로 수정하지 않고 아래 결함을 그대로 기록한다.

1. screening archive의 `H1A_TERM50_20s.mp4`는 baseline 1K 영상과 바이트 단위로 동일하다. TERM50의 로그·TensorBoard 결과는 사용할 수 있지만 이 영상은 TERM50 정책의 시각적 증거로 사용하면 안 된다.
2. baseline archive의 `training/humanoid/exported/model_best.pt`는 최종 5K 모델이 아니라 1K 체크포인트와 동일하다. 최종 모델은 run의 `model_4999.pt`이며, 결과 폴더의 `h1_baseline_5000.pt`도 해당 파일과 동일하다.
3. 보존 영상은 약 20초(999 frames, 50 fps)이다. 설정 문서의 6000 frames/120초 설명과 실제 산출물이 다르므로 실제 파일 메타데이터를 우선한다.

## 해석 원칙

- 체크포인트는 전부 내부 해석하지 않는다. iteration, 파일 존재, 해시 및 영상과의 연결만 확인한다.
- 학습 품질 판단은 전체 로그, TensorBoard 지표, 환경·reward 설정과 올바르게 연결된 영상에 근거한다.
- 기존 원본의 이름이나 내용을 고쳐치지 않는다. 잘못 연결된 파일은 분석에서 제외하고 올바른 대체 파일을 명시한다.

## 교정 overlay

`corrections/baseline_exported_model_best_20260908/model_best.pt`는 원본 run의 `model_4999.pt`를 별도 보존한 올바른 최종 baseline 모델이다. raw archive를 덮어쓰지 않으며, exported `model_best.pt`가 필요할 때 이 overlay를 우선 사용한다. 자세한 source path와 hash는 overlay README를 따른다.
