# Release 분류와 보존 규칙

작성일: 2026-09-12 KST  
목적: 개인 실험, 공식 raw run, 실제 제출물을 혼동 없이 보존하고 다음 작업자가 source-to-submission 연결을 재검증할 수 있게 한다.

## Release 유형과 게시 위치

### 작업 목적과 실행 환경은 별도 축

표시 제목의 주분류는 `[학습]` / `[분석]`으로 둔다. 학습 Run archive는 학습, 6영상·평가기·보조평가는 분석이다. **NVIDIA 서버에서 한 보조평가도 분석**이며 Windows만 분석인 것은 아니다. PERSONAL/OFFICIAL·실행 장소·완료/실패 상태는 별도 출처 정보로 유지한다. 기존 복합 backup은 하나의 목적을 추측해 붙이지 않는다.

이 구분은 아래 게시 저장소 정책을 바꾸지 않는다. 기존 Release는 태그·애셋·원문 본문을 유지하고 제목 및 상단 관리 안내만 정리한다. NVIDIA에 이미 게시된 분석 Release는 이전 주소를 유지하며, 새 Windows 평가 게시 위치는 eval이다. 상단 안내는 현재 분류·보존 정책을 설명하고 구 본문의 역사적 이름·절차를 최신 실행 지시로 오해하지 않게 한다.

기존 색인·게시 기록의 `TRAIN`은 학습, `VIDEO/EVAL/EVAL-PC`는 분석의 역사적 검색 분류로 읽는다. 제목 정리 때문에 기존 receipt나 게시 당시 snapshot을 고쳐 쓰지 않는다. 실제 제출·공개 참조·복합 backup은 각자의 보존 분류를 유지한다.

| 분류 | Release 저장소 | 담는 것 | canonical 원본 |
| --- | --- | --- | --- |
| 개인 NVIDIA/L40S 서버 실행 | `SE3C/naver-issacsim-nvidia` | 학습 run archive, checkpoint, 서버 native 영상, hash | `SE3C/naver-issacsim-originals/data/raw/private_server_runs/...`의 raw archive; 실행 source 기록 |
| Windows PC PERSONAL 사후 평가 | `SE3C/naver-issacsim-eval` | 새 통합 6영상·평가 ZIP, checksum, publication manifest | Originals의 private raw 보존; 기존 NVIDIA Release는 기존 주소 유지 |
| 공식 서버 전체 실행 | `SE3C/naver-issacsim-originals` | 공식 서버에서 받은 raw run archive 전체 | `data/raw/official_server_runs/`의 원본 바이트 |
| 실제 공식 제출 snapshot | `SE3C/naver-issacsim` | 수신했다면 실제 제출 ZIP, `policy.pt`, `env.yaml`, 제출 리포트, `submission_manifest.json`, `SHA256SUMS` | 해당 Originals raw run; submission Release는 제출 시점의 고정 사본 |
| 운영진 공개 연구기록 참조 영상 | `SE3C/naver-issacsim`의 별도 `reference-*` Release | 공개 researchlog에서 내려받은 원본 MP4만; 개인/공식 학습 evidence나 제출 snapshot과 혼합하지 않음 | 공개 원본 URL과 날짜별 `reference/public/` 메타데이터; Git blob에는 대용량 MP4를 넣지 않음 |

분석 Markdown은 `naver-issacsim` Git history가 canonical이다. 반복해서 Release asset으로 올리지 않는다. `issacsimz`는 Release 저장소가 아니라 학습·제출 세 계층에서 공용으로 쓰는 실행·evidence sidecar다.
공개 참조 영상의 `reference-*` Release는 **우리 학습/제출 Release가 아니다**. 외부 공개 클립을 우리 팀의 OFFICIAL 점수·Run·검증 영상으로 표시하거나 가설 registry에 등록하지 않는다.

## 이름 규칙

새 Release는 아래 tag 형식을 쓴다.

```text
private-<robot>-<YYYYMMDD>-<experiment>-<iterations-or-run-id>
official-<robot>-<YYYYMMDD>-<experiment>-<iterations-or-run-id>
submission-<robot>-prelim-r<round>-<YYYYMMDD>
```

새 형식의 가상 예시: `private-h1-20261001-exp-h1-linear-tracking-<evidence-run-id>`, `official-go2-20261001-exp-go2-gait-stability-<evidence-run-id>`, `submission-go2-prelim-r3-20260915`. 실제 과거 tag는 아래에 별도로 기록한다.

새 개인·공식 raw Release의 `<experiment>`에는 [새 Experiment 질문 주소](../research/EXPERIMENT_NAMING.md)를 사용하고, 실제 evidence run ID·자산 종류·checkpoint를 별도로 명시한다. `H/G/HS/GS`와 `Rxx`, `A1`·`G5`·`TERM50`은 legacy 검색 별칭이며 신규 tag의 식별 체계로 확장하지 않는다. `S1–S4`는 9/12 제안서와 9/13 실행 분석본에서 뜻이 달라 출처 없이 변환하지 않는다. 실제 ID↔Run 대응은 [registry](../research/EXPERIMENTS.md)를 따른다.

기본 보존 원칙은 Release asset의 이름·바이트를 소급 변경하지 않는 것이다. 표시 제목은 확인된 Experiment·evidence Run·preset을 구분하고, 설명은 **자산 파일명 → 실제 Run 또는 제출 export → source checkpoint → legacy 별칭**의 대응을 남긴다. 기존 archive 이름의 `r01`이 registry `R03`을 뜻하는 경우에는 이를 명시한다. 제출 snapshot·baseline·공개 참고자료·여러 Run이 섞인 Release에 단일 학습 Run을 억지로 부여하지 않는다. 옛 `G5`는 G-004, `A1`은 G-005 별칭이다.

**2026-09-29 사용자 승인 naming migration 예외:** 기존 Release의 title·body·tag는 현재 표준 이름으로 정리할 수 있다. 이 migration에서는 asset 파일명·asset bytes·digest는 변경하지 않고, 새 body에 이전 title/tag를 legacy 주소로 남겨 추적 가능하게 한다. Git tag를 바꿀 때는 같은 target을 가리키는 새 tag를 만든 뒤 Release를 새 tag로 연결하고 old→new 대응을 기록한다. 과거 evidence Run ID·archive/file 이름·historical report prose는 이 migration 때문에 이름을 바꾸지 않는다.

## 미래 Release의 tag 생성 순서

GitHub Releases 목록은 제목·본문·Latest 지정만으로 수동 정렬할 수 없다. 앞으로 새 Release를 만들 때 GitHub Release 화면에서 tag를 새로 만들지 않는다. 먼저 로컬에서 **annotated tag**를 만들고 원격에 push한 뒤, GitHub에서는 그 기존 tag를 선택해서 Release를 게시한다. annotated tag는 target commit과 별도의 tagger 시각을 가지므로, 오래된 target commit을 가리켜도 lightweight tag처럼 commit 시각에만 묶이는 것을 피한다.

```bash
# <target-commit>은 검증한 source commit으로 바꾼다.
git tag -a <release-tag> <target-commit> -m "<concise release description>"
git push origin <release-tag>
```

수동 게시는 GitHub에서 **Draft a new release → Choose a tag → 이미 push한 `<release-tag>` 선택 → Publish release** 순서로 진행한다. 기존 Release/tag/asset은 목록 순서만을 이유로 삭제·재생성·retag하지 않는다. 현재 `issacsimz`의 personal 6-video suite publisher는 NVIDIA checkout에서 annotated tag를 먼저 push한다. 일반 train archive publisher는 이 동작을 공유한다고 가정하지 말고, tagger 시각이 중요한 새 Release는 위 수동 절차로 만든다.

## Release 전 확인 순서

1. 먼저 작업 목적(학습 / 분석 / 복합 보존 / 실제 제출)을 판별하고 실행 환경과 출처를 별도로 기록한 뒤 아래 저장소 정책을 적용한다. 서버 보조평가는 분석이며 실제 제출 snapshot과 혼합하지 않는다.
2. canonical 원본의 파일명, bytes, SHA-256을 기록한다. 개인 raw는 `data/raw/private_server_runs/`, 공식 raw는 `data/raw/official_server_runs/`에도 같은 바이트가 있어야 한다.
3. 제출 snapshot은 `submission_manifest.json`에 robot, round, 제출 시각, 점수, source Originals release/archive/hash와 artifact hash를 기록한다.
4. Release 생성 뒤 GitHub asset의 bytes와 `digest`를 원본 SHA-256과 대조한다.
5. 교체 Release를 만들더라도 기존 Release·원본 evidence·archive는 기본적으로 보존한다. 이전 Release 제거는 사용자가 정확한 대상을 명시적으로 요청하고 새 Release의 asset 검증이 끝난 경우에만 별도 수행한다.

비밀값, `submit_config.txt`, `.env`, token·credential·private key는 어떤 Release에도 넣지 않는다.

### Windows 영상·평가 통합 ZIP

2026-10-15 사용자 승인 복사 이관: 기존 NVIDIA Windows 통합 평가 10개는 원본 애셋 그대로 Eval에도 게시한다. 원래 NVIDIA 주소·태그·애셋·본문은 그대로 보존하며 삭제하지 않는다. 기존 내부 manifest의 게시 위치 필드는 역사적 기록으로 유지하고, 새 주소와 대응은 [Eval 이관 manifest](https://github.com/SE3C/naver-issacsim-eval/blob/main/publications/migration_2026-10-15/migration_manifest.json)에서 확인한다. 학습·서버 영상 전용·보조평가 Release는 이번 10개 이관 범위 밖이다.

공식 checkpoint를 개인 Windows에서 평가해도 **평가 Release는 PERSONAL**이다. 2026-10-12부터 새 PC 통합 영상·평가 Release는 `SE3C/naver-issacsim-eval`에 둔다. 기존 NVIDIA Release의 주소·태그·애셋은 유지하고 병합된 Eval PR #2의 [평가 인덱스](https://github.com/SE3C/naver-issacsim-eval/blob/main/EVALUATION_RELEASES.md)로 연결한다. 공식 training 원본 Release에 개인 평가를 섞지 않고 출처 링크·checkpoint SHA로 연결한다. 평가·영상은 원래 학습 Run의 후속 기록이지 추가 학습 Run이나 제출 preset이 아니다.

검증된 통합 ZIP은 원래 파일명·바이트 그대로 보존·게시한다. 기본 asset은 **통합 ZIP + 같은 파일명의 `.sha256` + 별도 `publication_manifest.json`**이다. 이미 ZIP에 있는 MP4·평가 원자료는 중복 첨부하지 않는다. 게시 manifest는 source training Run/Release·checkpoint SHA, PERSONAL 평가 환경·protocol, ZIP filename/bytes/SHA를 기록하며 원본 내부 manifest를 수정하지 않는다. 기존 full 검증을 재사용하고 배포 ZIP CRC·출처·원격 size/digest를 확인한다. smoke/incomplete 자료는 full 완료로 표시하지 않는다. 공식 score·A/B 비교·calibration이 없는 ZIP에는 이를 명시한다.

기존 NVIDIA 평가 Release의 annotated tag는 검증된 영상/평가 task checkout commit을 가리키며 변경하지 않는다. 새 eval 저장소 Release의 tag는 해당 저장소의 게시 기록 commit을 가리키고, 실제 task source repo/commit과 evaluator source는 본문·manifest에 별도로 기록한다. 게시 기록 commit을 실제 실행 source라고 표시하지 않는다. canonical 원본은 Originals의 `private_server_runs/`에 유지한다.

첫 적용: [Go2 LINTRACK-125 model_7050 PERSONAL Windows 영상·평가](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-go2-20261004-exp-go2-planar-tracking-terrain-progression-model7050-video-eval). 통합 ZIP SHA-256 `34d45711d121a4bb59a92b6424f2652eeb915ed4f6436d49070389eacc33d1e1`, 34,310,566 bytes. 세 asset의 원격 크기·digest와 annotated tag target을 확인했다. [게시 검증 기록](../data/processed/operations/windows_go2_video_evaluation/model7050_release_verified.json).

2026-10-07 H1 두 층 연결: [`ORIENT-100` OFFICIAL fresh 3K training Release](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261006-exp-h1-rough-terrain-orientation-relaxation-fresh3k)는 Run `20261006-133517-h1-orient-100-fresh3k-official`의 train 원본을 보존한다(archive 418,957,086 bytes, SHA `85ea5dd5e6ccd4f9edee587fb7a4dacd2f311caa4dd256e3c1b57744bd4fed83`). [별도 H1 `ORIENT-100 / model_2850` Windows PERSONAL 영상·평가 Release](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-h1-20261007-exp-h1-rough-terrain-orientation-relaxation-model2850-video-eval)는 18개 항목 통합 ZIP `model_2850_ORIENT-100_h1_6terrain_evaluation_20261007-010444_f6b3b8b3.zip` (33,323,164 bytes, SHA `aecc82b13671d54c96813af6c02c1b2a7769ee001b30aa4a5c2761457110eb7a`) 및 기존 sidecar/manifest **3 asset만** 게시했다. 현재 GitHub Release의 3 asset 이름·크기·digest를 확인했다. PERSONAL ZIP은 평가 내부 `source_run_id=null`을 그대로 보존하며 공식 학습과의 연결은 **별도 checkpoint `model_2850.pt` SHA** `6aedeced60562c1d496d5319d29b76cf9e26ff43df06827cb370f24f5313f7b0` 및 [Run intake](../data/processed/experiments/h1/training/2026-10-06_ORIENT100_OFFICIAL3K_EVIDENCE_INTAKE.md)에서 확인한다. 이는 별도 학습 Run이나 제출/공식 채점 결과가 아니다. [분석 Markdown canonical](../data/processed/incoming/other/reviewed/H1_ORIENT-100_POLICY_ANALYSIS_20261007.md)은 **PERSONAL 행동 HOLD**, 같은 조건의 `h1-submit-2` 대조 평가 부재를 기록한다. **분석 .md를 기존 영상 ZIP Release 자산에 중복 첨부하지 않는다.**

2026-08-24 H1 baseline 300-iteration 묶음은 초기 참고자료이고 콘솔·TensorBoard가 없는 불완전한 진단 묶음이므로, 사용자 결정에 따라 Originals의 canonical Git 보존만 유지하고 Release 대상에서는 제외한다.

## 현재 기준선

- 공식 H1 baseline 1K raw: [`official-h1-20260908-baseline-1k`](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20260908-baseline-1k), SHA-256 `000b07bdc91bd458770ad14d568bddb7261fa4fa3b89e6511080398ebea1dd79`.
- 공식 H1 `TERM-50` 5K raw: [`official-h1-20260909-term-50-5k`](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20260909-term-50-5k), SHA-256 `723208aafa89e811d8c464b1482949df3259e935bff5f1ea1da7f8da61b806fb`.
- 공식 H1 `h1-submit-4 / AIRTIME-025` fresh 10K raw (legacy H-005): [`official-h1-20260927-airtime-025-fresh10k`](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20260927-airtime-025-fresh10k), canonical Git LFS download wrapper SHA-256 `3ff1dc0a820df63870c445260c2acf7d66781ab282325f3889d4d1ba669c0566`. 사용자 요청에 따라 1.35GB wrapper는 Release asset으로 중복 업로드하지 않고 Release 본문에서 canonical LFS 경로를 연결한다. Train evidence PASS; 이후 수신·게시한 4라운드 제출 파일은 아래의 별도 snapshot으로 구분하며 `policy.pt`의 특정 numbered checkpoint 계보는 미확인이다.
- 공식 Go2 baseline 1K raw: [`official-go2-20260913-baseline-1k`](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-go2-20260913-baseline-1k), SHA-256 `db659cdad4bf4a61de6c40c6185f80bb2465054e67abda91da4cfa8d0408a5bf`.
- 공식 Go2 `ANGXY-012` 1K raw (legacy G-004, 아주 오래된 alias G5): [`official-go2-20260914-angxy-012-1k`](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-go2-20260914-angxy-012-1k), train archive SHA-256 `1e162fdf640a715f19c564e21bff1011cd7ed91287db2f8d3586c3e0382d4359`. 같은 수신 폴더의 `env.yaml`, `model_best.pt`, `play_video.mp4`, `report.html`도 해당 Release에 첨부했다.
- 공식 Go2 LINTRACK-125 fresh 3K raw: [`official-go2-20260928-lintrack-125-fresh3k-r5`](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-go2-20260928-lintrack-125-fresh3k-r5), wrapper SHA-256 `a20df5f67bbc65c286ba06c082d20ce47c043505eb41dfbc521aeab19d56ca00`. Release에는 `model_best.pt=model_2000.pt`, terminal `model_2950.pt`, env·policy·ONNX·report와 loose `play_video.mp4`가 보존돼 있다. 이 단일 영상은 6지형 suite가 아니다.
- 공식 Go2 LINTRACK-125 fresh 7.5K raw: [`official-go2-20260929-lintrack-125-fresh7500`](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-go2-20260929-lintrack-125-fresh7500), wrapper SHA-256 `89449fe89d12107e9dcea0a67cd5d78b1611850f86d1bbeaf8b0611bd55bf13c`. Release의 `model_best.pt` SHA는 `d40f2666…8015`이며 numbered `model_7050.pt`와 일치한다. 6지형 MP4/manifest는 이 Release에 없고, 3K↔7.5K reward-effect 자체는 same-length BASE control 부재로 HOLD다.
- 공식 Go2 `LINTRACK-150-LINZ-2` fresh 5K interrupted raw (legacy G-005/A1): [`official-go2-20260914-lintrack-150-linz-2-5k-interrupted`](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-go2-20260914-lintrack-150-linz-2-5k-interrupted), wrapper SHA-256 `d2919617dbb2121652fb0c38fc12efe8d874280d55adf4416b39c7e5adfe30ef`. 약 iter 4837 중단·validation FAIL 상태를 그대로 보존한다.
- 공식 Go2 `LINTRACK-150-LINZ-2` recovery 4800→4999 raw (legacy G-005/A1): [`official-go2-20260914-lintrack-150-linz-2-resume4800-to5k`](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-go2-20260914-lintrack-150-linz-2-resume4800-to5k), final wrapper SHA-256 `265c3c5533ac2be5037cab0ea668b07990ccc8025a816b22178b7df7bd7257c5`. 완료된 recovery이며 uninterrupted fresh 5K로 분류하지 않는다.
- g2-submit-3 original model_4800 submission export raw: [`official-go2-20260915-lintrack-150-linz-2-original4800-submission`](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-go2-20260915-lintrack-150-linz-2-original4800-submission), ZIP SHA-256 `a16f26b6e4b3ba15cf333c35e9111bfa64b7a9aedb411b1c09c849bcba7a10df`. 이는 Round-3 실제 제출 snapshot의 source export인 original `model_4800` 계열이며 recovery `model_4900`으로 대체하지 않는다.
- 개인 Go2 `LINTRACK-150-LINZ-2` checkpoint 정량평가 (legacy A1): [`private-go2-20260915-lintrack-150-linz-2-checkpoint-quant-eval-seed4201-d1`](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-go2-20260915-lintrack-150-linz-2-checkpoint-quant-eval-seed4201-d1), bundle SHA-256 `72c00b43345e9438647e30a6e01905391c3aea085b90042c75fdbbb5ad2695bd`. PERSONAL L40S 보조평가이며 공식 점수나 제출 snapshot이 아니다.
- 개인 Go2 `LINTRACK-150-LINZ-2` 4800/4900 native-video 비교 (legacy A1): [`private-go2-20260915-lintrack-150-linz-2-4800-vs-4900-native-video`](https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/private-go2-20260915-lintrack-150-linz-2-4800-vs-4900-native-video), bundle SHA-256 `424467b9c5b61666957ff22cc3395803f45d5c48bfc7797e3c85749a29902a7d`. PERSONAL L40S 보조 검증이며 공식 점수나 제출 snapshot이 아니다.
- 실제 H1 예선 2라운드 제출: [`submission-h1-prelim-r2-20260909`](https://github.com/SE3C/naver-issacsim/releases/tag/submission-h1-prelim-r2-20260909). 제출 `policy.pt`·`env.yaml` hash는 위 `TERM-50` 5K 현재 export와 일치한다. 점수는 종합 86.37/100, 시뮬 56.37/70이며 공식 평가 기록 asset도 같은 Release에 둔다.
- Go2 예선 3라운드 제출 snapshot: [`submission-go2-prelim-r3-20260915`](https://github.com/SE3C/naver-issacsim/releases/tag/submission-go2-prelim-r3-20260915). 받은 `3.zip`과 풀린 `policy.pt`·`env.yaml`·기술 개선 리포트의 SHA-256을 함께 보존한다. canonical 원본은 Originals의 4800 official export다. Release 생성 당시에는 점수가 없었지만 이후 공식 평가 **87.55/100**을 수신했다. 제출 snapshot과 사후 평가 기록은 구분한다.
- Go2 예선 5라운드 제출 snapshot: [`submission-go2-prelim-r5-20261006`](https://github.com/SE3C/naver-issacsim/releases/tag/submission-go2-prelim-r5-20261006). `g2-submit-5 / LINTRACK-125`, OFFICIAL fresh 7.5K terminal `model_7450.pt`의 policy/env/report snapshot이다. 이후 [2026-10-08 공식 평가](../data/processed/experiments/go2/analysis/2026-10-08_OFFICIAL_EVAL_GO2_ROUND5_LINTRACK125.md) **88.32/100(58.32+20+10)**과 표시 제출 시각 **2026-10-06 01:10**을 수신했다. 별도 사후 평가 기록으로 연결하며 frozen 제출 파일·intake manifest를 덮어쓰지 않는다.
- `h1-submit-4 / AIRTIME-025` 예선 4라운드 제출 snapshot: [`submission-h1-prelim-r4-20260928`](https://github.com/SE3C/naver-issacsim/releases/tag/submission-h1-prelim-r4-20260928). 사용자 제출 알림과 수신한 폴더의 `policy.pt`·`env.yaml`·`technical_report.txt`를 manifest·SHA256SUMS와 함께 보존하고 원격 크기·digest 5/5를 확인했다. 이후 [공식 평가 기록](../data/processed/experiments/h1/analysis/2026-09-30_OFFICIAL_EVAL_H1_ROUND4_AIRTIME025.md)을 수신해 시뮬 56.37/70, 설계 의도 20/20, 리포트 품질 10/10을 기록했다(구성 점수 합계 86.37/100). 원본 제출 ZIP·포털 수령증·정확한 제출 시각은 아직 없고, `env.yaml`은 공식 train archive와 동일하지만 loose `policy.pt`의 source numbered checkpoint는 미확인이다. [manifest](../data/processed/experiments/h1/2026-09-28_H005_PRELIM_R4_SUBMISSION/submission_manifest.json).
- 운영진 공개 H1 연구기록 참조 영상: `reference-h1-researchlog-20260922-selected31`. 당시 공개 페이지의 H1 MP4 31개(실패 분류 22, 성공 분류 9)만 개별 asset으로 게시하고 원격 크기·SHA-256 31/31을 확인한 기록이 있다. **2026-10-01 consistency audit에서는 해당 Release tag endpoint가 404이고 현재 Release 목록에도 없으므로 현재 접근 가능한 Release로 취급하지 않는다.** 작업용 분석 ZIP과 삭제된 공개 필드의 메타데이터는 첨부하지 않았으며, 우리 팀 공식 학습·제출·평가 evidence도 아니다. 현재 저장소에 남은 공개 snapshot 메타데이터는 [`2026-09-22_ncrc_public_data_audit`](../data/processed/reference/public/2026-09-22_ncrc_public_data_audit/README.md)를 따른다.
