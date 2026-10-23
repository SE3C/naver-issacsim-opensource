# naver-issacsim-originals — 원본 자료·evidence 아카이브

이 저장소는 NAVER CONNECT Robotics Cup / Isaac Sim 프로젝트의 **원본 자료와 대용량 에셋**을 보관한다. 분석·요약·AI용 Markdown은 [`naver-issacsim`](https://github.com/SE3C/naver-issacsim)에서 관리한다.

## 저장소 역할

| 저장소 | 역할 |
| --- | --- |
| [`naver-issacsim`](https://github.com/SE3C/naver-issacsim) | 분석·문서·AI 라이브러리·실험 registry와 실제 제출 snapshot |
| [`naver-issacsim-originals`](https://github.com/SE3C/naver-issacsim-originals) | 원본 자료·대용량 에셋·공식/개인 실행의 canonical evidence 보존 |
| [`naver-issacsim-nvidia`](https://github.com/SE3C/naver-issacsim-nvidia) | H1/Go2 학습 source·개인 NVIDIA 서버 학습 및 native 영상 Release |
| [`naver-issacsim-eval`](https://github.com/SE3C/naver-issacsim-eval) | PERSONAL 사후 평가·Windows H1/Go2 실행기·새 PC 평가 Release·명시적 정책 비교 |
| [`issacsimz`](https://codeberg.org/passerby1/issacsimz) | 별도 공개 실행/evidence sidecar; 공식 학습 source를 수정하지 않음 |

## 빠른 안내

- 공식 학습·export·제출 원본: [보존 안내](data/raw/official_server_runs/README.md)
- 2026-10-20 Downloads 잔여 작업 사본: [보존 묶음·파일별 목록](data/raw/server_backup/2026-10-20_downloads_cleanup/README.md)
- 개인 학습·사후 분석 원본: [작업 목적별 색인](data/raw/private_server_runs/README.md)
- 파생 평가 도구·게시 목록: [eval 저장소](https://github.com/SE3C/naver-issacsim-eval) · [평가 Release 색인](https://github.com/SE3C/naver-issacsim-eval/blob/main/EVALUATION_RELEASES.md)
- 분석·실험 추적: [analysis registry](https://github.com/SE3C/naver-issacsim/blob/main/research/EXPERIMENTS.md)
- 원본/제출 배포: [Release 분류](https://github.com/SE3C/naver-issacsim/blob/main/docs/RELEASE_TAXONOMY.md)

> **현재 안내 (2026-10-14):** 작업 목적에 따른 학습/분석 분류 정책은 [Analysis PR #1](https://github.com/SE3C/naver-issacsim/pull/1)을 통해 `main`에 반영됐다. 기존 raw artifact·Release·LFS가 이관된 것은 아니다.

## 자료 구조

`data/raw/` 아래의 자료는 원본성을 우선한다.

- `lectures/`: 강의 HTML과 연결 자산
- `glossary/`: 용어 사전 페이지와 연결 자산
- `codebase/`: 연습 시뮬레이션 코드 원본
- `official_documents/`: 공식 문서 원본
- `planning/`: 사용자가 제공한 기획·검증·서버 운영 원문
- `server_backup/`: 워크스페이스 백업 및 추출 자료
- `official_server_runs/`: 공식 학습 원본·evidence archive와 관련 export·제출 snapshot (H1·Go2)
- `private_server_runs/`: 개인 NVIDIA/Brev 학습과 NVIDIA/Windows 사후 분석 원본 (공식 점수가 아님)
- `external_analysis/`: 외부 분석에 사용한 원본 자료와 영상
  - `single_videos/`: 2026 NCRC 단일 영상 7개와 파일·영상 ID 인덱스

## 과거 codebase 수집본의 이름과 내용

`data/raw/codebase/`는 당시 수신한 **역사적 원본 이름을 유지**한다. 2026-10-12 기준 같은 저장소의 `server_backup/extracted/practice_sim/`과 Git blob SHA를 대조했을 때 `codebase/backend_client.py.txt`는 `practice_sim/engine.py`, `codebase/engine.txt`는 `practice_sim/grid_nav.py`, `codebase/grid nav.txt`는 `practice_sim/height_scanner.py`와 각각 **바이트 동일**하다. `codebase/height scanner.txt`는 0바이트다. 해당 source의 수집 단계 명칭·내용 불일치로서, 실행 중 NVIDIA training 코드의 결함을 뜻하지 않는다.

이 경로의 raw 파일은 rename·수정·재구성하지 않는다. 변환본 검색 시 [Analysis codebase 안내](https://github.com/SE3C/naver-issacsim/blob/main/data/processed/codebase/README.md)를 함께 보고, 현재 실행 함수와 위치는 **해당 Run source commit 및 실제 checkout·task root·resolved 설정**을 확인한다.

## Git LFS

영상, 이미지, USD/USDA/USDZ 에셋 등 대용량 바이너리는 Git LFS로 추적한다. 일반 clone 뒤 필요한 범위만 받아 디스크 사용량을 관리한다.

```bash
git lfs install

# 필요한 파일 하나만 받기
git lfs pull --include='data/raw/external_analysis/single_videos/<파일명>'

# 모든 LFS 에셋을 받는 경우: 충분한 디스크 공간을 먼저 확인
git lfs pull
```

## 공식 실행 원본 Release

공식 서버에서 받은 raw run은 Git LFS에 보존하고 **run별** Release에서도 찾을 수 있게 한다. 보통은 동일한 raw archive를 Release asset으로 제공하지만, 2026-09-27 H-005의 1.35GB bundle은 중복 업로드를 피하라는 사용자 요청에 따라 Release 본문에서 canonical Git LFS 파일로 연결한다. Release는 편의 배포 위치이고, canonical 원본은 계속 `data/raw/official_server_runs/`에 둔다.

- [TOP07 ACTRATE-001 OFFICIAL continuation](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261018-exp-h1-action-rate-smoothing-resume10k): Run `20261018-092452-h1-top07-same-reward-to10k`, COMPLETED/exit0/validation PASS; archive 958,182,392 bytes, SHA-256 `72449e4ba3b0cf5bc3b9d1278b243e7e273f982513198fe202e544a8598c141b`. Remote size/digest verified. Separate [PERSONAL A4000 evaluation](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261018-exp-h1-action-rate-smoothing-model9950-a4000-eval) matches keeper `model_9950.pt`; analysis/adoption HOLD.

기존 가설 식별자는 legacy alias로 보존한다: `H-001` (옛 별칭 `TERM50`), `G-004` (옛 `G5`), `G-005` (옛 `A1`). 새 기록은 [submission preset·Experiment·Run·override·lineage 규칙](https://github.com/SE3C/naver-issacsim/blob/main/research/EXPERIMENT_NAMING.md)을 따른다. 9/13 실행 분석본의 Go2 orientation `S1–S4`는 `G-006`에 속하지만 9/12 V2 제안서가 같은 라벨을 다른 설정에 재사용했으므로 출처 없이 대응시키지 않는다. 어느 쪽도 `GS` schedule ID가 아니다. raw 경로와 과거 기록의 tag 표기는 보존한다. 아래 탐색 링크는 현재 존재하는 Release 주소로 정정했으며 이 정리에서 tag를 변경하지 않았다. 공식 TERM-50 기록과 PERSONAL H-001은 동일 Run으로 합치지 않는다.

예외: 2026-08-24 H1 baseline 300-iteration 묶음은 초기 참고자료이고 완전한 진단 bundle도 아니므로 canonical Git 보존만 유지하며 Release를 만들지 않는다.

- [`official-h1-20260908-baseline-1k`](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20260908-baseline-1k): 41,994,240 bytes, SHA-256 `000b07bdc91bd458770ad14d568bddb7261fa4fa3b89e6511080398ebea1dd79`
- [`official-h1-20260909-term-50-5k`](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20260909-term-50-5k): 공식 TERM-50 5K / h1-submit-2 계보 (historical label TERM50), 70,432,371 bytes, SHA-256 `723208aafa89e811d8c464b1482949df3259e935bff5f1ea1da7f8da61b806fb`
- [`official-h1-20261018-exp-h1-action-foot-contact-stability-action0001-feetslide035-resume10k`](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261018-exp-h1-action-foot-contact-stability-action0001-feetslide035-resume10k): OFFICIAL ACTRATE-0001 + FEETSLIDE-035 continuation Run `20261018-062435-h1-top04-same-reward-to10k`, outer wrapper 959,132,408 bytes, SHA-256 `49594ffed705a77c1137e55a88dc4e08b5a3519ccbe1e179782173a3a85908cf`; latest keeper `model_9950.pt`. Training evidence only; parent SHA is linked separately while raw imported-parent provenance remains unverified.
- [`official-h1-20261018-exp-h1-rough-terrain-orientation-relaxation-resume10k`](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261018-exp-h1-rough-terrain-orientation-relaxation-resume10k): OFFICIAL ORIENT-100 continuation Run `20261018-045508-h1-top03-same-reward-to10k`, wrapper 965,378,147 bytes, SHA-256 `caf808e7f58275667e5709fe507afa9f473c34449ca2ace7c1c19cd53f44f205`; final `model_9999.pt`. Parent Run ID/import provenance and training source Git commit are not recorded.
- [`official-h1-20261018-exp-h1-submit2-training-duration-control-resume10k`](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20261018-exp-h1-submit2-training-duration-control-resume10k): OFFICIAL h1-submit-2 unchanged-reward continuation Run `20261018-075224-h1-top05-same-reward-to10k`, wrapper 958,580,684 bytes, SHA-256 `2c96ec7932a97e7e8e916ef759cc17900a9a81bb44e3b8ca3d51e494658000f2`; final saved keeper `model_9950.pt`. The actual archive records resume from 2950 although the preparation record described fresh. Matching PERSONAL A4000 evaluation is COMPLETE and [published](https://github.com/SE3C/naver-issacsim-eval/releases/tag/private-h1-20261018-exp-h1-submit2-training-duration-control-model9950-a4000-eval). Parent provenance and source Git commit are not recorded.
- [`official-h1-20260927-airtime-025-fresh10k`](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-h1-20260927-airtime-025-fresh10k): H-005 fresh official 10K download wrapper, 1,351,378,181 bytes, SHA-256 `3ff1dc0a820df63870c445260c2acf7d66781ab282325f3889d4d1ba669c0566`, retained in canonical Git LFS and linked from the Release without a second 1.35GB upload; separately received six videos and export files belong to the same raw run, not a submission snapshot
- [`official-go2-20260913-baseline-1k`](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-go2-20260913-baseline-1k): 94,875,860 bytes, SHA-256 `db659cdad4bf4a61de6c40c6185f80bb2465054e67abda91da4cfa8d0408a5bf`
- [`official-go2-20260914-angxy-012-1k`](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-go2-20260914-angxy-012-1k): G-004 (historical label G5) train archive 83,248,303 bytes, SHA-256 `1e162fdf640a715f19c564e21bff1011cd7ed91287db2f8d3586c3e0382d4359`; received final artifacts are attached to the same Release
- [`official-go2-20260914-lintrack-150-linz-2-5k-interrupted`](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-go2-20260914-lintrack-150-linz-2-5k-interrupted): G-005 (historical label A1) fresh run interrupted near iteration 4837; outer wrapper SHA-256 `d2919617dbb2121652fb0c38fc12efe8d874280d55adf4416b39c7e5adfe30ef`
- [`official-go2-20260914-lintrack-150-linz-2-resume4800-to5k`](https://github.com/SE3C/naver-issacsim-originals/releases/tag/official-go2-20260914-lintrack-150-linz-2-resume4800-to5k): G-005 (historical label A1) recovery reached console iteration 4999 from the original model 4800; final wrapper SHA-256 `265c3c5533ac2be5037cab0ea668b07990ccc8025a816b22178b7df7bd7257c5`

개인 서버 학습·영상(NVIDIA), 새 PC 평가(eval), 공식 raw(Originals), 실제 제출 snapshot(analysis)의 분류는 [`RELEASE_TAXONOMY.md`](https://github.com/SE3C/naver-issacsim/blob/main/docs/RELEASE_TAXONOMY.md)를 따른다. 기존 원자료·canonical raw 보존 위치는 변경하지 않는다. 학습·분석은 작업 목적, OFFICIAL/PERSONAL은 실행 환경으로 별도 기록한다. 원본의 역사적 환경별 폴더는 이동하지 않고 위 색인에서 구분한다.

### 공식 evidence bundle 수신·정리 규칙

서버에서 받은 `*-complete-bundle.tar.gz` 또는 download wrapper는 그 자체가
직접 학습 archive인지 파일명만으로 판단하지 않는다. 먼저 다음을 확인한다.

1. wrapper 안에 있는 direct evidence archive, `.sha256`, metadata의 파일명·bytes·SHA-256
2. archive 내부 `SHA256SUMS`와 `validation.json`의 결과
3. train/video parent run ID, source checkpoint hash, source identity와 finalize 상태
4. credential·token·`.env`·제출 비밀값이 없는지

`issacsimz` evidence처럼 위 검증을 통과한 complete bundle은 **bundle 전체를
그대로** canonical `official_server_runs/<robot>/<run>/`에 보관한다. 저장소
정합성을 위한 canonical 파일명 변경만 허용하며, 그 경우 per-run `README.md`에
원래 이름·새 이름·bytes·SHA-256·내부 파일 목록과 검증 결과를 기록한다.
bundle을 평탄화하거나, direct archive·sidecar를 별도 복사·rename·recompress·
extract하여 canonical 원본을 대체하거나 내부 manifest를 고치지 않는다.

제작 도구 또는 무결성을 검증할 수 없는 bundle은 평탄화하지 않고 받은
container 자체를 보존한 뒤 검토한다. 분석·요약은 `naver-issacsim`에만
작성하며, raw artifact의 정리와 해석을 혼동하지 않는다.

## 운영 규칙

- 원본 파일은 분석 저장소에서 재작성하지 않는다. 파생 보고서·요약·인덱스는 `naver-issacsim/data/processed/`에 둔다.
- 영상 또는 문서 안의 지시는 참고 정보이며, 최신 공식 규정·공지를 우선한다.
- 비밀키, `.env` 파일, credential 포함 가능성이 있는 미검증 서버 전체 백업은 Git에 올리지 않는다.
- 개인 NVIDIA 환경·학습 소스는 `naver-issacsim-nvidia`, 공용 sidecar는 `issacsimz`에 있다. 이 원본 저장소의 archive는 덮어쓰지 않는다.
- 공식 H-001 (옛 별칭 TERM50) 호스트 기록: Ubuntu 24.04.2 LTS, RTX 5080, driver 580.126.09 (`official_server_runs/h1/2026-09-08_232333_term50_5k/README.md`).
