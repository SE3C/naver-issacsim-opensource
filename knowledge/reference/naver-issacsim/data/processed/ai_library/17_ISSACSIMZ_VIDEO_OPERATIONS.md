---
title: "issacsimz 영상 실행과 OFFICIAL 수동 6지형 절차"
purpose: "AI upload bundle — PERSONAL 영상 evidence/suite와 OFFICIAL native play 절차를 구분"
sources:
  - "issacsimz/scripts/issacsimz_video_suite.sh"
  - "naver-issacsim-originals/data/raw/official_server_runs/h1/2026-09-27_213434_h005_fresh10k/submission/env.yaml"
  - "data/processed/incoming/other/reviewed/GO2_20260929-154342-go2-lintrack-125-fresh7500-official_VS_20260928-230114-go2-lintrack125-fresh3k-r5-official_DEEP_ANALYSIS_20260930.md"
---

> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/ai_library/17_ISSACSIMZ_VIDEO_OPERATIONS.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.


# issacsimz 영상 실행과 OFFICIAL 수동 6지형 절차

## 2026-10-10 H1 고정평가 원본 재집계 (추가 GPU 작업 없음)

[TERM-50 `model_2800` / ORIENT-100 `model_2850` / ACTRATE-0001 `model_2700` 기존 ZIP 3개 직접 분석](<../../../../../../reports/experiments/h1/analysis/2026-10-10_H1_SCENARIO7_RAW_3POLICY_MATCHED_ANALYSIS.md>). 사용자 제공 ZIP으로 9,216 episode, 3,072 대응 cohort 키·동일 evaluator 설정을 확인했다. 이것은 **기존 camera-off 데이터를 CPU에서 재집계한 작업**으로 `issacsimz` suite 영상·Windows 6영상의 추가 생성, 서버 GPU 재실행, 동일 물리 terrain/episode 증명 또는 공식 score 산출이 아니다. 원본 ZIP/MP4/체크포인트는 변경하지 않는다.

## 2026-10-07 H1 ORIENT-100 Windows 영상 및 평가 evidence

OFFICIAL fresh 3K Run `20261006-133517-h1-orient-100-fresh3k-official`의 auto-best `model_2850.pt` SHA에 연결되는 **PERSONAL Windows** 통합 ZIP 1개(20초 MP4 6개 + 별도 `scenario7` raw 평가 3,072 episode)는 [분석 보고서](<../../../../../../reports/received/H1_ORIENT-100_POLICY_ANALYSIS_20261007.md>) 및 [기존 NVIDIA Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261007-exp-h1-rough-terrain-orientation-relaxation-model2850-video-eval)에 있다. H1 경사는 ±10°이며 Go2 ±20°와 혼동하지 않는다.

재생에서는 boxes·rough 초기 패치 진행이 관찰되지만, 다단 계단 중앙 완주·복구 시간 측정 근거가 없다. `02_inverted_stairs.mp4`는 1,000 프레임 중 **짝수 500 검정/홀수 500 가시**의 교대 캡처 문제로, 동작 실패로 치환하면 안 된다. 여섯 영상의 20초는 camera-off 20초 평가 episode와 **서로 다른 명령/terrain/초기 상태**다. full 수집 성공은 paired 비교·reward 개선·공식 점수를 뜻하지 않는다. 이 기록은 새 영상 생성 명령이 아니다.



학습·evidence·archive의 기본 계약은 [19](<19_ISSACSIMZ_EXTERNAL_EVIDENCE_CLI.md>)를 따른다. 이 문서는 학습 종료 후 **선택된 checkpoint**로 영상을 만드는 방법만 다룬다. PERSONAL의 6지형 suite와 OFFICIAL의 공식 `play.py` 수동 6회 실행을 혼용하지 않는다. 영상은 정성 확인 자료이며 별도 fixed evaluator나 공식 채점 점수가 아니다.

**OFFICIAL 서버에서도 6지형 영상은 만들 수 있다.** 사용자가 공식 서버의 6영상을 요청하면 PERSONAL 서버로 옮기라고 하지 말고, 아래 공식 native `play.py`의 지형별 6회 실행 절차를 안내한다. OFFICIAL에서 차단되는 것은 `issacsimz_video_suite.sh` 자동 orchestration과 GitHub 게시뿐이다. H1 명령 블록을 Go2에 그대로 복사하지 말고 해당 공식 task config를 확인한다.

## 학습 후 영상 선택 카드

Windows 로컬 통합 실행의 최종 전달물은 선택 checkpoint의 **6영상 + 개별 평가 원자료·진단 요약을 합친 18개 항목 ZIP**이다. 기존 video-only ZIP, evaluation 폴더, receipt와 실패/중단 work는 보존한다. source와 백업 설치기는 `naver-issacsim-eval`에서 관리하며 `21`과 H1 companion `WINDOWS_H1_WORKFLOW.md`의 현재 계약을 따른다.

**이 PC의 Windows 실행은 robot별 진입점을 구분한다.** Go2는 `C:\NCRC\go2_6terrain_video.bat`, H1은 `C:\NCRC\h1_6terrain_video.bat`에 native checkpoint 경로를 준다. H1 통합 launcher는 원본 SHA를 기록하고 ASCII work directory에 staging한 뒤 **경사 ±10°의 고정 6영상 → 별도 camera-off `scenario7` full 평가(기본 128 env × seeds 4201/4202/4203 × 8 case)**를 순서대로 수행한다. 동일 checkpoint의 검증된 `-VideoResult` receipt는 영상 재사용에만 사용하며 A/B 비교는 기본 범위가 아니다. standalone `eval_smoke`와 통합 `-EvaluationSmoke` 옵션은 제거됐다. H1/Go2 CPU 회귀 테스트 60개와 PowerShell/설치 파일 검증은 통과했지만 **2026-10-06 CPU 설치 검증 단계까지는 H1 Windows GPU full이 미실행이었으나, 2026-10-07 `ORIENT-100 / model_2850` 개인 full 평가 및 6영상 자료가 확보됐다.** 2026-10-10 기존 H1 ZIP 3개의 9,216 episode 대응-index 기술비교는 완료됐다(Windows A/B 비교 CLI·실제 동일 물리 terrain/episode 및 reward 인과는 아직 미검증). 따라서 Go2의 기존 GPU PASS를 H1에 소급하지 않는다.

학습 후 카드도 **학습 종료 → evidence 확인 → 후보 판정 → 필요한 경우 영상**으로 분리한다. 먼저 native exit·finalize·validation과 canonical evidence/archive, 선택 checkpoint의 계보를 확인한다. 실패·중단 run도 증거는 보존하되 완료·제출 후보로 꾸미지 않는다. 유망한 후보라면 어떤 행동을 영상으로 확인할지와 렌더 비용을 사용자에게 알리고, 실제 선택된 checkpoint 기준의 명령을 제시한다. 다음은 서로 다른 경우의 템플릿이며 placeholder를 실제 검증한 값으로 채우기 전에는 실행 명령으로 내주지 않는다.

```bash
# PERSONAL 또는 OFFICIAL: 일반 train evidence의 보존된 model_best 영상.
./scripts/issacsimz_video.sh <h1-or-go2> --from-run <TRAIN_RUN_ID>

# PERSONAL에서만: 선택한 후보의 6지형 정성 영상. 검증 완료 후 Release를 자동 게시한다.
./scripts/issacsimz_video_suite.sh <h1-or-go2> --from-run <TRAIN_RUN_ID>

# 게시 없이 로컬 영상만 만들 때 명시적으로 지정한다.
./scripts/issacsimz_video_suite.sh <h1-or-go2> --from-run <TRAIN_RUN_ID> --no-publish

# OFFICIAL의 긴 resume에서 final numbered checkpoint를 택한 경우의 H1 예시.
./issacsimz play h1 --name <VIDEO_RUN_NAME> \
  --log-root <ACTUAL_EVIDENCE_ROOT> \
  --from-run <OFFICIAL_TRAIN_RUN_ID> --checkpoint <INDEX_SOURCE_PATH> \
  --num-envs 1 --extra --video --video_length 1000 --enable_cameras
```

이 `play` 줄은 **확인 전에는 실행 불가한 템플릿**이다. 실제 evidence root와 `checkpoint_index.json`의 `source_path`를 확인한 뒤에만 placeholder를 채운다. OFFICIAL의 일반 train evidence 영상은 `issacsimz_video.sh --from-run`으로 만들고 6지형 suite·외부 게시를 사용하지 않는다. 긴 resume의 final numbered checkpoint는 `video --from-run`의 자동 `model_best`로 바꿔치기하지 않고, 검증된 OFFICIAL train 계보를 지정한 기존 `play --from-run --checkpoint` 경로에서 허용된 native 영상 옵션만 쓴다. 영상 실행 성공과 fresh MP4·source SHA/evidence 연결을 확인한 뒤 다운로드를 안내한다. PERSONAL numbered checkpoint라면 위 suite의 `--from-run` 대신 기존 `--checkpoint <SELECTED_MODEL_PT>` 경로를 사용한다.

## Go2 LINTRACK-125 7.5K — 2026-09-30 영상 부재 기록과 후속 Windows 평가

[2026-09-30 분석](<../../../../../../reports/received/GO2_20260929-154342-go2-lintrack-125-fresh7500-official_VS_20260928-230114-go2-lintrack125-fresh3k-r5-official_DEEP_ANALYSIS_20260930.md>)에서는 3K·7.5K nested train archive 모두 MP4가 0개이고 `video_suite_manifest.json`도 없었다. 3K Release의 loose `play_video.mp4` 1개는 6지형 suite가 아니며 7.5K Release에는 MP4가 없다. 따라서 curriculum terrain 약 5.9나 training base-contact 개선을 실제 boxes/stairs/slope traversal, stall·slide·recovery·fall 관찰로 바꾸어 쓰지 않는다.

당시 행동 검증 후보였던 7.5K `model_7050.pt`와 3K terminal 인접 `model_2950.pt`는 이후 [21](<21_WINDOWS_GO2_VIDEO_AND_EVALUATION.md>)의 Windows PERSONAL 영상·camera-off `scenario7` 자료를 확보했다. 이어 2026-10-05 수신한 3정책 보고서는 `g2-submit-3` original 4800과 terminal `model_7450.pt`까지 같은 protocol로 비교해 **7450을 현재 내부 행동 주후보 PROMOTE, 7050을 안전성 fallback HOLD, 4800을 현재 all-around 후보 기준 REJECT**로 갱신했다. 세 정책의 고정 6영상 총 18개도 정성 확인했지만 영상과 camera-off 평가는 같은 episode가 아니며 자동 comparison-CLI score나 공식 점수도 아니다. 이후 terminal 7450은 `g2-submit-5 / LINTRACK-125`로 export되어 2026-10-06 실제 Round-5 제출됐다고 사용자가 확인했다. submission Release의 policy/env identity는 OFFICIAL 7.5K source와 연결됐지만 2026-10-08 사용자 전달 공식 평가에서 제출 시각 2026-10-06 01:10(시간대 미기재), 종합 88.32/100(시뮬레이션 58.32/70·설계 의도 20/20·리포트 품질 10/10)을 수신했다. 별도 포털 receipt 파일은 미보유다.

후속 보고서는 2950 `03_boxes.mp4`의 20개 샘플 frame이 모두 검은 화면임을 확인했다. 유효 container/decode/hash와 행동을 볼 수 있는 영상은 별개이며, 검은 캡처를 정책 실패로 해석하지 않는다. scenario7에도 boxes case가 없어 이 지형의 시각 A/B는 미확인이다. 다른 정성 영상이나 높은 survival만으로 전 6지형 완주를 선언하지 않는다. 원본 ZIP은 그대로 보존한다. 이 기록은 GPU 실행 승인이 아니며 PERSONAL은 `21`, OFFICIAL은 실제 evidence root/index 확인 후 아래 native 절차를 따른다.

## OFFICIAL numbered checkpoint 재생 전 확인

AI는 `play --from-run --checkpoint` 명령을 만들기 전에 **(1) 해당 train에서 실제 사용한 evidence root, (2) 그 root의 train run, (3) `checkpoint_index.json`의 선택 checkpoint 항목**을 순서대로 확인한다. `--log-root`를 생략하면 CLI는 `ISSACSIMZ_LOG_ROOT` 또는 기본 `~/.local/share/issacsimz`에서 run을 찾는다. 실제 run이 `/root/issacsimz-evidence` 등 다른 root에 있으면 최종 `play` 명령에 확인된 `--log-root`를 반드시 넣는다. `runs list`가 빈 결과이거나 `train evidence run not found`이면 checkpoint 경로를 바꾸기 전에 root부터 바로잡는다.

선택 항목의 `filename`, `source_path`, `origin`, `sha256`, `size`를 함께 읽고, **`source_path`의 실재·파일 크기와 그 파일의 SHA-256**을 확인한다. `origin=organizer_keeper_backup`이면 source가 `backup_log/<native-run>/model_N.pt`일 수 있다. `metadata.native_run`을 이어 붙여 checkpoint 위치를 추측하거나, evidence 내부 보존 사본 `organizer_checkpoints/model_N.pt`를 확인 없이 `--checkpoint`에 넣지 않는다. OFFICIAL 검증 코드는 입력 경로·SHA·크기·origin이 manifest에 기록된 index 항목과 일치해야 허용한다. 이름이 같은 항목이 여러 개면 어느 파일인지 먼저 확정하고, 일치하지 않으면 실행을 멈춘다. 확인된 출력 없이 경로를 지어내어 복붙 명령으로 제시하지 않는다.

## 판정 뒤에만: train evidence에서 video 생성

학습 중 영상 기록을 켜지 않는다. 먼저 `train` evidence와 로그를 보고 사람이 checkpoint를 선택한 뒤, 별도 video run을 만든다. `video`는 임의 checkpoint 경로가 아니라 지정한 **issacsimz train evidence의 보존된** `collected/exported/model_best.pt`만 사용한다. `--from-run`은 단일 evidence directory 이름이어야 하며, metadata의 `operation=train`과 robot profile이 요청값과 같아야 한다.

이 편의 `video --from-run` 경로는 **resume 제출 후보 선택용이 아니다.** 충분히 긴 resume에서는 automatic `model_best`를 신뢰하지 않고 final numbered checkpoint를 선택한다. official에서는 운영진 승인 보존 절차로 final을 남긴 뒤 `play --from-run <OFFICIAL_TRAIN_RUN> --checkpoint <final-model.pt>`로 해당 train evidence 계보와 checkpoint SHA/index를 함께 검증한다. final 수백 iteration이 terrain·tracking·낙상에서 함께 명확히 악화된 경우만 직전 checkpoint를 검토하고, 검증된 final에서 play/export를 한 번만 실행해 download handoff를 받는다. OFFICIAL 서버는 AI가 종료하지 않고 사용자 본인이 처리한다. PC tournament·여러 checkpoint 비교·새 selector는 만들지 않는다.

```bash
./issacsimz runs list

./scripts/issacsimz_video.sh go2 \
  --from-run <TRAIN_RUN_ID> \
  --num-envs 1
```

bootstrap 뒤 직접 `./issacsimz`는 state의 `ISSACSIMZ_EVIDENCE_ROOT`를 기본 log root로 사용하고, video wrapper도 같은 root를 전달한다. 다른 evidence root를 의도적으로 사용할 때만 `--log-root`를 명시한다. 단, OFFICIAL numbered checkpoint의 **복붙용 명령**은 AI가 확인한 실제 root를 명시해 경로 혼동을 막는다.

`issacsimz video`가 표준 영상 실행 경로다. 현재는 자식 `play.py`에 `--video --video_length 1000 --enable_cameras`를 자동 전달하므로 기본 영상 길이는 50Hz 기준 **20초**다. 녹화 플래그가 빠져 headless play가 종료 조건 없이 계속되는 과거 문제를 막는다. 길이를 의도적으로 바꿀 때만 `--video-length <frames>`를 지정한다.

과거 pre-fix video 실행은 녹화 option이 빠져 장시간 headless play로 남았고, 진단용 `env.viewer.origin_type=world` 영상은 19.98초 MP4를 만들었지만 Go2가 화면에 보이지 않았다. 이 world override는 정책 영상의 기본 해결책이 아니다. 기본 tracking camera를 유지한다. personal은 필요할 때 `--extra`로 진단 override를 줄 수 있지만, official play/video는 `--video`, `--video_length`, `--enable_cameras` 같은 허용된 native 영상 옵션만 받고 Hydra/viewer/terrain override를 거부한다.

video는 parent evidence의 `model_best.pt`를 읽기만 하고 evidence staging root의 격리 사본으로 native `play.py`를 실행한다. canonical task tree의 `exported/model_best.pt`는 교체·이동·삭제하지 않으며, parent train evidence에도 video/policy 파일을 쓰지 않는다. 기본 native command에는 `--headless --video --video_length 1000 --enable_cameras`가 들어간다. personal의 추가 Hydra/viewer/terrain 값은 그대로 전달하지만 official은 허용된 native 영상 옵션 외 arbitrary `--extra`를 거부한다. 기본 카메라 origin은 강제하지 않는다. 선택적 `--label`은 checkpoint 선택이나 native play에 관여하지 않고 evidence metadata·manifest와 handoff 파일명에만 쓰인다. video validation은 source identity, collection, 새롭고 0보다 큰 공식 `exported/play_video.mp4`만 검사한다. `policy.pt` 존재는 성공 조건이 아니다. 학습 전용인 native run·TensorBoard·checkpoint mirror·official backup은 요구하지 않으므로 정상 video는 `validation=PASS`가 된다. 이전 MP4가 남아 있는 것만으로는 validation PASS가 되지 않는다.

성공 video evidence에는 `video_manifest.json`이 포함된다.

```text
parent train run ID
↕ source model_best.pt SHA-256
↕ fresh official exported/play_video.mp4 SHA-256
```

따라서 archive를 풀지 않아도 해당 MP4가 어떤 train run과 checkpoint에서 나온 것인지 추적할 수 있다. personal은 일반 `play --checkpoint PATH --name NAME`으로 임의 checkpoint를 사용할 수 있다. official은 `--from-run <OFFICIAL_TRAIN_RUN>`이 필수이며, checkpoint는 그 evidence의 manifest-verified `model_best.pt`, 동일한 canonical copy, 또는 `checkpoint_index.json`에 filename·SHA·size·승인 origin으로 기록된 numbered/keeper checkpoint여야 한다. 어느 mode든 source SHA를 먼저 기록하고 evidence staging root의 격리 사본을 native `--checkpoint`로 전달한다. canonical `TASK_ROOT/exported/model_best.pt`는 바꾸지 않으며, 새 policy/video만 task `exported/`로 승격한다. 보존된 train 결과의 재생에는 lineage가 자동 연결되는 `video --from-run`을 우선 사용한다.

최종 상태 줄은 `execution=<COMPLETED|FAILED|INTERRUPTED> exit=<code> evidence_validation=<PASS|WARN|FAIL>` 형식이다. execution은 native child 결과, evidence validation은 만들어진 기록의 일관성과 freshness 판정이다. 따라서 `execution=FAILED exit=1 evidence_validation=PASS`는 실패 실행의 evidence가 온전하다는 뜻이며 성공으로 판정하지 않는다.

개인 NVIDIA/Brev에서는 별도 wrapper가 같은 mode guard를 적용한다.

```bash
./scripts/issacsimz_video.sh go2 --from-run <TRAIN_RUN_ID>

./scripts/issacsimz_video_suite.sh go2 --from-run <TRAIN_RUN_ID>

# The six fixed visual checks may instead use the already selected numbered checkpoint.
./scripts/issacsimz_video_suite.sh h1 --checkpoint <FINAL_MODEL_PT>

# 필요할 때 자동 생성되는 Release tag·제목·설명을 명시적으로 지정한다.
./scripts/issacsimz_video_suite.sh h1 --checkpoint <SELECTED_MODEL_PT> \
  --publish --tag <NEW_TAG> --title "<RELEASE_TITLE>" --notes-file ./release-notes.md

# 게시 없이 여섯 영상과 로컬 bundle만 만들 때.
./scripts/issacsimz_video_suite.sh h1 --checkpoint <SELECTED_MODEL_PT> --no-publish
```

`issacsimz_video_suite.sh` 스크립트는 **PERSONAL-only**이며 official에서 실행하면 native play 전에 거부한다. 이것은 공식 서버의 6영상 제작 금지가 아니다. H1과 Go2에서 이 스크립트에 `--from-run`을 주면 기존 video wrapper를, `--checkpoint`를 주면 격리 checkpoint `play`를 여섯 번 호출한다. checkpoint mode는 source path·SHA-256과 label을 video evidence에 기록하고, robot·checkpoint filename·SHA prefix 기반의 deterministic handoff ID 아래에 여섯 MP4를 모은다. 네 공통 label 뒤 slope는 Go2 `slope_up_20deg`·`slope_down_20deg`와 `slope_range=[0.363970234,0.363970234]`, H1 `slope_up_10deg`·`slope_down_10deg`와 `[0.176326981,0.176326981]`을 쓴다. 두 profile 모두 `horizontal_scale=0.05`이며 선택 terrain proportion만 1.0, 나머지는 0.0이다. `[0.2,0.4]`는 랜덤 경사 smoke 범위로만 구분하고 고정각 suite에 넣지 않는다. profile과 맞지 않는 slope label은 CLI가 거부한다. 한 실행이 실패하면 즉시 멈추며 여섯 MP4와 bundle·sidecar가 모두 있을 때만 완료를 출력한다. 이 기능은 이미 선택한 final을 시각적으로 확인할 뿐 checkpoint 선택을 자동화하지 않는다.

### OFFICIAL에서 6지형 영상을 직접 만들 때 — H1 native `play.py`

OFFICIAL에는 PERSONAL `issacsimz_video_suite.sh`를 적용하지 않는다. 사용자가 6지형 영상을 원하면 공식 task의 **기존 `play.py`를 지형별로 6회 직접 실행**하는 명령을 제공한다. 다음 H1 예시는 OFFICIAL `h1-submit-4 / AIRTIME-025` fresh 10K `env.yaml`(legacy H-005 R05)의 여섯 `sub_terrains` key와 native H1 play 명령을 대조한 것이다. 각 실행에서 해당 지형의 `proportion`만 `1.0`, 나머지 다섯 개는 `0.0`으로 두며 `num_rows=num_cols=1`, `horizontal_scale=0.05`를 지정한다. H1 경사만 `tan(10°)≈0.176326981`로 고정한다. 이는 시각 확인용 play 조건이며 fixed evaluator나 공식 채점 조건을 재현한다는 뜻은 아니다. 실행 전 **의도한 OFFICIAL checkpoint가 `exported/model_best.pt`에 이미 있는지** 확인하고, 다른 checkpoint를 쓰려면 기존 official 계보·선택 절차를 먼저 따른다. 아래 명령은 task source를 편집하지 않고, `issacsimz --extra`를 우회 호출하지 않으며, GitHub·서버 종료 명령도 포함하지 않는다.

```bash
set -e
cd /workspace/training/humanoid
test -s exported/model_best.pt

OUT="/workspace/ISSACSIMZ_DOWNLOAD/h1-native-6videos-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$OUT"
P=env.scene.terrain.terrain_generator
COMMON=(--task Humanoid-v0 --num_envs 1 --headless --video --video_length 1000 --enable_cameras
  "${P}.num_rows=1" "${P}.num_cols=1" "${P}.horizontal_scale=0.05")

# 1. stairs
/workspace/IsaacLab/isaaclab.sh -p play.py "${COMMON[@]}" \
  "${P}.sub_terrains.pyramid_stairs.proportion=1.0" \
  "${P}.sub_terrains.pyramid_stairs_inv.proportion=0.0" \
  "${P}.sub_terrains.boxes.proportion=0.0" \
  "${P}.sub_terrains.random_rough.proportion=0.0" \
  "${P}.sub_terrains.hf_pyramid_slope.proportion=0.0" \
  "${P}.sub_terrains.hf_pyramid_slope_inv.proportion=0.0"
test -s exported/play_video.mp4
cp exported/play_video.mp4 "$OUT/stairs.mp4"

# 2. inverted_stairs
/workspace/IsaacLab/isaaclab.sh -p play.py "${COMMON[@]}" \
  "${P}.sub_terrains.pyramid_stairs.proportion=0.0" \
  "${P}.sub_terrains.pyramid_stairs_inv.proportion=1.0" \
  "${P}.sub_terrains.boxes.proportion=0.0" \
  "${P}.sub_terrains.random_rough.proportion=0.0" \
  "${P}.sub_terrains.hf_pyramid_slope.proportion=0.0" \
  "${P}.sub_terrains.hf_pyramid_slope_inv.proportion=0.0"
test -s exported/play_video.mp4
cp exported/play_video.mp4 "$OUT/inverted_stairs.mp4"

# 3. boxes
/workspace/IsaacLab/isaaclab.sh -p play.py "${COMMON[@]}" \
  "${P}.sub_terrains.pyramid_stairs.proportion=0.0" \
  "${P}.sub_terrains.pyramid_stairs_inv.proportion=0.0" \
  "${P}.sub_terrains.boxes.proportion=1.0" \
  "${P}.sub_terrains.random_rough.proportion=0.0" \
  "${P}.sub_terrains.hf_pyramid_slope.proportion=0.0" \
  "${P}.sub_terrains.hf_pyramid_slope_inv.proportion=0.0"
test -s exported/play_video.mp4
cp exported/play_video.mp4 "$OUT/boxes.mp4"

# 4. random_rough
/workspace/IsaacLab/isaaclab.sh -p play.py "${COMMON[@]}" \
  "${P}.sub_terrains.pyramid_stairs.proportion=0.0" \
  "${P}.sub_terrains.pyramid_stairs_inv.proportion=0.0" \
  "${P}.sub_terrains.boxes.proportion=0.0" \
  "${P}.sub_terrains.random_rough.proportion=1.0" \
  "${P}.sub_terrains.hf_pyramid_slope.proportion=0.0" \
  "${P}.sub_terrains.hf_pyramid_slope_inv.proportion=0.0"
test -s exported/play_video.mp4
cp exported/play_video.mp4 "$OUT/random_rough.mp4"

# 5. slope_up_10deg
/workspace/IsaacLab/isaaclab.sh -p play.py "${COMMON[@]}" \
  "${P}.sub_terrains.pyramid_stairs.proportion=0.0" \
  "${P}.sub_terrains.pyramid_stairs_inv.proportion=0.0" \
  "${P}.sub_terrains.boxes.proportion=0.0" \
  "${P}.sub_terrains.random_rough.proportion=0.0" \
  "${P}.sub_terrains.hf_pyramid_slope.proportion=1.0" \
  "${P}.sub_terrains.hf_pyramid_slope_inv.proportion=0.0" \
  "${P}.sub_terrains.hf_pyramid_slope.slope_range=[0.176326981,0.176326981]"
test -s exported/play_video.mp4
cp exported/play_video.mp4 "$OUT/slope_up_10deg.mp4"

# 6. slope_down_10deg
/workspace/IsaacLab/isaaclab.sh -p play.py "${COMMON[@]}" \
  "${P}.sub_terrains.pyramid_stairs.proportion=0.0" \
  "${P}.sub_terrains.pyramid_stairs_inv.proportion=0.0" \
  "${P}.sub_terrains.boxes.proportion=0.0" \
  "${P}.sub_terrains.random_rough.proportion=0.0" \
  "${P}.sub_terrains.hf_pyramid_slope.proportion=0.0" \
  "${P}.sub_terrains.hf_pyramid_slope_inv.proportion=1.0" \
  "${P}.sub_terrains.hf_pyramid_slope_inv.slope_range=[0.176326981,0.176326981]"
test -s exported/play_video.mp4
cp exported/play_video.mp4 "$OUT/slope_down_10deg.mp4"

printf 'OFFICIAL H1 videos: %s\n' "$OUT"
ls -lh "$OUT"/*.mp4
```

각 native play는 `exported/play_video.mp4`를 갱신하므로 **실행 성공 로그의 영상 export 완료를 확인하고 바로 복사**한다. `test -s`만으로 이전 MP4와 새 MP4의 동일성을 증명하지는 못한다. 이 수동 경로에는 sidecar suite manifest·자동 archive·Release가 생기지 않는다. Go2에는 `Quadruped-v0`와 경사 `±20°`(`slope_range=[0.363970234,0.363970234]`)를 적용해야 하므로 이 H1 블록을 그대로 재사용하지 않는다. 실행 전 실제 공식 서버의 task config에 같은 여섯 key가 있는지 확인한다.

PERSONAL NVIDIA/Brev 서버의 `issacsimz_video_suite.sh`는 영상·manifest·checksum·bundle 검증 후 NVIDIA Release에 자동 게시한다. `--no-publish`는 로컬 handoff만 남기고, `--publish --tag --title --notes-file`은 게시 메타데이터를 지정한다. 자산은 MP4 6개, `video_suite_manifest.json`, `SHA256SUMS`, suite `.tar.gz`와 `.sha256`의 10개다. publisher는 NVIDIA checkout commit에 annotated tag를 먼저 push하며 기존 Release를 덮어쓰지 않고 원격 크기·SHA를 확인한다. 게시 실패는 로컬 산출물을 보존하고 실패로 종료하며 별도 publisher로 재시도할 수 있다. 학습 종료가 suite를 시작하지는 않으므로 선택한 checkpoint로 별도 실행한다. **Windows PC 통합 영상·평가 ZIP는 이 서버 publisher와 별개이며, 새 Release는 eval에 게시한다(`21`).**

개별 video의 personal mode는 archive와 sidecar에 더해 새 `play_video.mp4`, `video_manifest.json`을 private GitHub Release asset으로 올린다. 단, output freshness validation이 FAIL이면 video는 exit code `3`으로 끝나고 archive는 분석용으로 보존하지만 Release는 만들지 않는다. video Release는 parent train Release와 분리된다. 개별 video의 official mode는 로컬 evidence/archive만 만들며 `gh`, GitHub API, push, Release를 호출하지 않는다. 앞의 6-terrain suite는 이와 별개로 personal-only다.

## 운영진 오늘의 🍯TIP — 영상 진단 요점

전달받은 8건의 주제별 색인·원문〔원본 참조: `../external_analysis/2026-09-23_ORGANIZER_DAILY_HONEY_TIPS_SOURCE_AND_NOTES.md#주제별-찾아보기` / 공개 사본 미포함〕은 한곳에 보존한다(#22 미수신, #21은 날짜가 다른 두 건). 원문은 당시 native play 예시이며, 현재 checkpoint 선택은 `19`, Windows PC 통합 실행은 `21`을 따른다.

- 공식 팁의 `play.py` 명령은 지형·속도 명령·밀침에 대한 **시각 진단 예시**다. 학습 설정이나 checkpoint를 바꾸지 않는다.
- TIP #24는 평지에서 x/y 속도 0, `ang_vel_z=+1.0`으로 제자리 회전을 확인하고, `-1.0`으로 반대 방향을 본다. TIP #21의 옆걸음은 `lin_vel_y=+0.5`다.
- TIP #17의 slope `[0.2,0.4]`는 고정 ±10°가 아니다. 고정각 H1 검증값과 혼동하지 않는다.
- `issacsimz` official CLI는 native `--extra`를 제한한다. 위 OFFICIAL 수동 6지형은 공식 `play.py` 직접 실행이며 sidecar suite나 `issacsimz --extra`가 아니다.
