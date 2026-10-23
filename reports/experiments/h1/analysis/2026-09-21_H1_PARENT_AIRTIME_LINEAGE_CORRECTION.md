> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/experiments/h1/analysis/2026-09-21_H1_PARENT_AIRTIME_LINEAGE_CORRECTION.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# [분석] H1 부모 airtime 계보 정정 및 재실험 계획 — 2026-09-21

> 관리 안내 (2026-10-13): **분석** 작업으로 분류했다. 실행 장소와 OFFICIAL/PERSONAL은 출처 정보다. 기존 본문은 당시 기록으로 보존하며 현재 상태는 [Experiment registry](<../../../../research/EXPERIMENTS.md>)를 확인한다.

## 현재 판단

H-005~H-011은 **상대 비교용 / HOLD / 재실험 필요**다. 기존 Run의 COMPLETE, validation 결과, TensorBoard 수치와 영상은 실제 과거 실행 기록으로 보존한다. 이를 최종 reward 채택이나 OFFICIAL 성능 근거로 사용하지 않는다. 재실험은 PLANNED이며 이번 정정에서 서버 작업을 실행하지 않았다.

공식 TERM50 5K의 feet_air_time은 **+0.2**다. 개인 H-001 1.5K 부모는 **-0.2**다. 같은 TERM50/H-001 이름으로 설정 동일성을 추정한 분석이 오류의 원인이다. 공식 제출이 잘못된 -0.2 정책이었다는 해석은 철회한다.

## 원본에서 확인한 설정과 계보

검증 근거는 Release asset digest, archive 내부 metadata/source reward/env.yaml 및 checkpoint checksum이다. 이 표는 기존 보고서의 의도값이 아니라 실제 실행 설정을 기록한다.

| Run | termination | feet_air_time | track_lin_vel_xy_exp | joint_deviation_hip | 계보 및 해석 |
| --- | ---: | ---: | ---: | ---: | --- |
| 공식 TERM50 5K | -50 | +0.2 | 0.5 | -0.2 | 공식 baseline 대비 termination -5→-50만 변경; 2라운드 제출 |
| 개인 H-001 1.5K | -50 | -0.2 | 0.5 | -0.2 | fresh; H-005~008 실제 checkpoint 부모 |
| H-004 | -20 | +0.2 | 0.5 | -0.2 | fresh; 개인 H-001과 termination뿐 아니라 feet도 다름 |
| H-005 | -50 | +0.25 | 0.5 | -0.2 | 개인 H-001에서 feet -0.2→+0.25 |
| H-006 | -50 | +0.30 | 0.5 | -0.2 | 개인 H-001에서 feet -0.2→+0.30 |
| H-007 | -50 | +0.2 | 1.0 | -0.2 | 개인 H-001에서 feet와 track 동시 변경 |
| H-008 3K 및 unchanged 5K | -50 | +0.2 | 0.75 | -0.2 | 최초 분기는 feet와 track 동시 변경; 이후 continuation은 설정 유지 |
| H-009 | -50 | +0.2 | 0.75 | -0.3 | H-008 3K에서 hip만 변경 |
| H-010 | -50 | +0.25 | 0.75 | -0.2 | H-008 3K에서 feet만 변경 |
| H-011 | -50 | +0.2 | 0.75 | -0.1 | H-008 3K에서 hip만 변경 |
| H-012 | -100 | +0.2 | 0.5 | -0.2 | PERSONAL fresh BASE 분기; 이번 잘못된 부모 계보에 속하지 않음 |

- 공식 TERM50 archive SHA-256: `723208aafa89e811d8c464b1482949df3259e935bff5f1ea1da7f8da61b806fb`.
- 개인 H-001 archive SHA-256: `25252b3425012faeaf450c07004a70c4699c998814940a6a52475370a1ff8443`.
- 개인 H-001 `model_1499.pt`: `68fa0a9fe5334f8a3ecea110c4ccc9adb81ec07ac50169eaf8009b1a6e88f0c1`. 부모 archive checksum과 H-005~008 source checkpoint SHA가 일치한다. 공식 TERM50의 1.5K checkpoint로 취급하지 않는다.
- H-008 `model_2998.pt`: `d9a30c8a117f69cac49c4e640500f0fa8d88de72d6c61855f1e147ea6c1912ae`. H-009~011의 직접 부모이며 H-008 5K final이 아니다.
- H-005~008의 전체 reward-weight 비교는 위 Delta와 일치한다. 해당 비교에서 agent 설정의 resume 차이와 log 경로 외 추가 설정 변경은 확인되지 않았고 source 차이는 reward 파일이었다.

## 해석 제한

H-005/006은 실제 부모 대비 단일 feet 변경 실험이다. 다만 의도했던 +0.2 부모의 작은 조정 실험이 아니므로 그 질문에 대한 재실험이 필요하다. 기존 -0.2 부모에서 +0.2로 resume한 run도 reward 변경 run이므로 'unchanged control'이라고 부를 수 없다.

H-007/008의 track 단독 효과 주장은 철회한다. 동일 부모에서 나온 두 결과의 상대 비교는 가능하지만 feet와 추가 학습의 효과까지 분리하는 근거는 아니다.

H-009~011과 기존 H-008 unchanged continuation은 실제 H-008 설정 안의 형제 비교로 보존한다. 즉시 부모 대비 단일변수라는 사실은 유지한다. 사용자의 결정에 따라 이들 역시 새 정상 부모 계보에서 재검증하며, 기존 결과만으로 최종 채택하지 않는다.

H-004의 과거 parent 선택 판단은 당시 판단으로 보존하되 termination 단독 우열 결론은 철회한다. 공식 TERM50 5K 및 제출 점수 86.37/100(시뮬레이션 56.37/70)은 이번 개인 계보 정정으로 바뀌지 않는다. H-012와 공식 TERM50은 reward 설정상 termination만 다르지만 실행 환경과 학습 조건을 맞춘 인과 비교는 아니다.

## 재실험 계획 — 전부 PLANNED

1. 개인 H-001의 새 Run으로 TERM50 / feet=+0.2 / track=0.5 / hip=-0.2를 처음부터 1.5K 학습한다. 다른 reward는 검증된 기준 설정을 유지한다. 기존 -0.2 부모를 단순 resume해서 정상 부모로 재명명하지 않는다.
2. 새 부모의 final checkpoint를 공유해 unchanged +1.5K control과 H-005(feet=.25), H-006(feet=.30), H-007(track=1.0), H-008(track=.75)을 각각 실행할 계획이다. seed=42, envs=4096 및 source/학습 조건을 동일하게 기록한다.
3. 새 H-008 3K final에서 unchanged +2K continuation과 H-009(hip=-.3), H-010(feet=.25), H-011(hip=-.1)을 병렬 가설 Run으로 등록한다. 실제 실행 시점은 별도 사용자 요청에 따른다.
4. 가설 ID는 유지하고 새 Run ID·checkpoint path/SHA를 기록한다. 기존 Run과 파일을 덮어쓰지 않는다. parent identity가 확인되기 전 PLANNED 항목에 SHA를 임의로 채우지 않는다.
5. 충분한 resume의 대표는 late joint collapse가 없는 한 final numbered checkpoint다. 과거 영상은 새 Run의 영상으로 재사용하지 않는다. 서버 종료는 별도 명시 요청이 있어야 한다.

## Release 및 문서 복구

관련 NVIDIA Release 17개의 제목/본문에 경고를 추가했다. 태그, asset ID/이름/size/digest와 draft/prerelease 상태는 변경하지 않는다. 변경 전 내용은 [Release 원래 제목·본문·자산 목록](<../2026-09-21_H1_LINEAGE_RELEASES_BEFORE_CORRECTION.json>)에 보존한다.

적용 후 GitHub API 재조회에서 17/17 제목·본문 일치 및 tag/asset ID·이름·size·digest/draft/prerelease 불변을 확인했다. 원본을 다시 업로드하거나 삭제하지 않았다.

incoming/reviewed 원문과 raw evidence는 그대로 보존한다. processed 분석, registry, AI library의 현재 해석은 본 정정을 우선한다. Downloads의 기존 `H012_vs_H001_TERM50_COMPARISON_INPUTS_20260921`는 개인 -0.2 부모 자료를 포함하므로 공식 TERM50 비교 입력으로 사용하지 않는다.

## 원본 위치

- [공식 TERM50 raw Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20260909-term-50-5k)
- [개인 H-001 1.5K raw Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-20260916-230730-h1-term-50-feet-minus-0.2-1p5k)
- 공식 archive: `naver-issacsim-originals/data/raw/official_server_runs/h1/2026-09-08_232333_term50_5k/H1_TERM50_5k_complete_20260909_003012.tar.gz`
- 공식 env: `H1_TERM50_5k_complete_20260909_003012/logs/rsl_rl/humanoid/2026-09-08_23-23-33/params/env.yaml`
- [가설 dashboard](<../../../../research/EXPERIMENTS.md>)
