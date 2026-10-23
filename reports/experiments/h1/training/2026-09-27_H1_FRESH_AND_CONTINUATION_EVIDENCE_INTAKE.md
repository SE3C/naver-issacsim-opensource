> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/experiments/h1/training/2026-09-27_H1_FRESH_AND_CONTINUATION_EVIDENCE_INTAKE.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# [학습] 2026-09-27 H1 PERSONAL fresh·continuation evidence intake

> 관리 안내 (2026-10-13): **학습** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](<../../../../research/EXPERIMENTS.md>)를 확인한다.

이 문서는 세 학습 Run과 여섯 지형 영상 Release의 **수신·계보·비교 설계**를 기록한 최초 intake다. 이후 H-005 비교·후속 재분석과 H-010 fresh 비교 보고서가 도착했다. 고정 evaluator는 아직 없으므로 최종 성능 순위나 OFFICIAL 후보 채택을 주장하지 않는다. 사전 질문은 [원래 계획](<../../../../research/planning/historical/2026-09-27_H1_PERSONAL_FRESH_AND_CONTINUATION_PLAN.md>)에 있다.

| 실행 | 확인된 설정과 상태 | Train Release | 6-terrain video Release |
| --- | --- | --- | --- |
| H-005 Run 03 fresh 3K | checkpoint 없이 0부터; TERM `-50`, track `0.5`, feet `0.25`; seed 42, 4096 env; exit 0, evidence PASS, 61 checkpoints | [train](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260927-032343-h1-airtime-025-fresh3k-r01-20260927) | [model_2750](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-checkpoint-h1-model_2750-6d7d0ecb13c7-videos) |
| H-010 Run 03 fresh 3K | checkpoint 없이 0부터; TERM `-50`, track `0.75`, feet `0.25`; seed 42, 4096 env; exit 0, evidence PASS, 61 checkpoints | [train](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260927-043527-h1-airtime-025-lintrack-075-fresh3k-r01-20260927) | [model_2700](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-checkpoint-h1-model_2700-5d19578749df-videos) |
| H-005 Run 04 unchanged continuation, attempt 02 | corrected Run 02 `model_2998.pt`에서 +2K; TERM `-50`, track `0.5`, feet `0.25`; seed 42, 4096 env; global iteration 4997, exit 0, evidence PASS, 41 checkpoints | [train](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260927-054950-h1-airtime-025-corrected3kto5k-r02-20260927) | [model_4800](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-checkpoint-h1-model_4800-40c6a4a8273c-videos) |

값은 각 archive의 `metadata.json`, `native_run/params/env.yaml`, `source/humanoid_rewards.py`에서 확인했다. H-005 fresh와 H-005 continuation의 reward source 내용은 동일하고, 기존 corrected H-005 Run 02와는 `termination_penalty: -50` 대 `-50.0` 표기 한 곳만 다르다. H-010 fresh의 reward source는 H-005 fresh와 `track_lin_vel_xy_exp: 0.75` 대 `0.5` 한 곳만 다르다. 이는 최초 reward source 비교이며 이후 H-010 보고서는 env/PPO와 지정 source 파일의 동일성도 확인했다. 그러나 한 seed의 학습이나 명령·지형이 맞지 않은 영상만으로 공식 평가 우위를 확정하지 않는다. 영상의 checkpoint 번호는 각 `video_suite_manifest.json`과 해당 train archive의 `SHA256SUMS`로 대조했다. **영상은 각각 2750·2700·4800에서 생성되었으며 fresh final 2999·Run 04 final 4997 영상이라고 부르지 않는다.** 초기 수신 시점에는 영상 내용의 우열을 판정하지 않았다.

H-005 Run 04의 `metadata.json`에는 staging된 parent 경로 `h005-corrected-parent-2998-reupload-20260927/model_2998.pt`, source SHA-256 `9454afa964bb4dd7168dba1dfbef2d0acd1aaafa11d02026550cfdb5d6a485cc`, `source_provenance_verified=false`가 함께 남아 있다. 해당 SHA는 기존 [corrected H-005 Run 02 train Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260925-071158-h1-airtime-025-from-term-50-r02-corrected-h1-corrected-20260)의 `checkpoints/model_2998.pt` 기록과 일치한다. 이는 별도 바이트 동일성 대조이지 metadata의 provenance 필드를 소급 변경한 것이 아니다. Run 04의 final `model_4997.pt`는 archive에 존재하지만 대표 정책 선정·영상 확인은 별도 판단이다.

첫 resume 시도 [실패 evidence](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260927-053754-h1-airtime-025-corrected3kto5k-r01-20260927_FAILED)는 별도 보존한다. `exit_code=1`, native run/checkpoint 없음, checkpoint 로드 중 `PytorchStreamReader ... invalid header or archive is corrupted` 오류였다. 실패한 staged checkpoint SHA `98b2eab8…05bd9b`는 corrected Run 02의 위 SHA와 달랐다. 이것을 완료된 5K Run이나 비교 자료로 세지 않는다.

## 분석 입력 3묶음

1. **학습 경로:** H-005 fresh Run 03, 기존 corrected H-005 Run 02, corrected H-001 unchanged 3K control의 train·video 각 1개씩. Fresh vs resume 경로와 control 대비 방향을 분리한다. reward 단독 인과효과라고 해석하지 않는다.
2. **fresh 전체 설정:** H-010 fresh Run 03, H-005 fresh Run 03, 기존 corrected H-010 Run 02 5K의 train·video 각 1개씩. 앞의 두 fresh는 track `0.75` vs `0.5` 질문이지만, 기존 H-010 5K는 부모·학습 경로·길이가 다른 참고군이다.
3. **H-005 지속성:** H-005 Run 04 3K→5K, 기존 corrected Run 02 3K, 오늘 fresh Run 03 3K의 train·video 각 1개씩. Run 04 영상은 final이 아닌 `model_4800.pt`다. matched unchanged 5K control이 없어 5K reward 우월성은 결론내리지 않는다.

세 묶음은 Downloads에 각각 여섯 개의 통합 `.tar.gz`로 준비했고 Release 자산 크기·SHA-256과 일치했다. 동일 archive가 묶음 사이에 재사용된다. 이후 (1)은 [fresh H-005 vs corrected 3K 분석](<../../../received/H1_H005_FRESH3K_R01_VS_H005_R02_DEEP_ANALYSIS_20260927.md>), (2)는 [H-010 vs H-005 fresh 분석](<../../../received/H1_H010_FRESH3K_R01_VS_H005_FRESH3K_R01_DEEP_ANALYSIS_20260927.md>), (3)은 [H-005 5K continuation 분석](<../../../received/H1_H005_CORRECTED5K_R02_VS_H005_FRESH3K_R01_DEEP_ANALYSIS_20260927.md>)으로 원문 보존했다. H-005 Run 04는 late-window가 개선됐지만 final 4997 영상이 없고 5K unchanged control도 없다. H-010 fresh는 H-005 fresh보다 XY error가 크게 낮지만 yaw error가 크게 높고 contact·episode length도 불리하다. 둘 다 PERSONAL 단일 seed와 unmatched 영상에서 최종 승자를 정하지 않는다. 현재 판단은 [H-005 registry](<../../../../research/experiments/h1/H-005.md>), [H-010 registry](<../../../../research/experiments/h1/H-010.md>)를 따른다. 다음 단계는 동일 command·terrain·seed의 고정 evaluator에서 진행·stall·낙상·XY/yaw·자세를 비교하는 것이다. PERSONAL 결과를 공식 점수나 제출 정책으로 쓰지 않는다.

[H-005 후속 재분석](<../../../received/H1_H005_FRESH3K_R01_VS_H005_CORRECTED3KTO5K_R02_DEEP_ANALYSIS_20260927.md>)은 (3)의 **같은 3개 train archive와 3개 video bundle**을 다시 사용했다. 별도 Run이나 독립 반복 실험으로 세지 않는다. 이전에 샘플링하지 않은 fresh boxes 9초대 자세 손실·회복 관찰을 추가했지만, 비교 조건이 matched되지 않아 결론·가설 상태는 바꾸지 않는다. 원문의 4800↔4997 우선 비교 제안은 checkpoint 대표성 질문으로만 구분하고, reward 효과 판단에는 unchanged control을 포함해야 한다.

보존 상태: 이 문서에서 확인한 9/27 train archive의 지속적인 배포 근거는 NVIDIA private Release다. 현재 로컬 `naver-issacsim-originals/data/raw/private_server_runs/h1/`에는 9/27 canonical 보관 폴더가 확인되지 않는다. Downloads의 세 분석 폴더도 임시 비교용 복사본이지 Originals에 이미 수납됐다는 증거가 아니다. Originals 수납 전에는 Release mirror와 canonical raw archive 보존 완료를 혼동하지 않는다.
