# NCRC 5개 저장소 공개 전 점검 — 2026-10-23

## 결론과 작업 경계

현재 비공개 자료까지 포함한 5개 저장소 전체를 그대로 공개하는 것은 보류한다. 자체 코드와 대회 제공 자료의 공개 범위를 먼저 나눌 필요가 있다. 이번 검사는 위반 사실을 판정하는 감사나 법률 검토가 아니라, 로컬에 보존된 규정·파일·이력·Release에서 공개 전에 처리할 사항을 찾는 작업이다. 대회 종료 후 공개 허용 여부는 확인되지 않았다.

서브에이전트 3개가 보안/이력, 권리/출처, Release/압축본을 나누어 읽기 전용으로 조사했다. 메인은 규정 문구, LICENSE 부재, DM 원문 존재, 현재 HEAD 이메일 메타데이터와 경로 노출의 핵심 근거를 재확인했다. 저장소 파일·이력·원격 Release·공개 설정은 변경하지 않았다. 이 문서는 저장소 바깥 로컬 점검 기록이다.

검사 기준 HEAD:

| 저장소 | HEAD |
| --- | --- |
| naver-issacsim | aa11f96 |
| naver-issacsim-originals | d31cea7 |
| naver-issacsim-nvidia | 91b32f6 |
| naver-issacsim-eval | ddd12bc |
| issacsimz | b01a397 |

## 공개 전 우선 처리

### 1. 대회 제공 코드·강의·실습 자료의 공개 권한

- `naver-issacsim/data/processed/reference/official/2026-08-14_OFFICIAL_BRIEFING_QA_ANALYSIS.md:31,45`에 가이드북·실습 코드의 외부 공개/공개 저장소 업로드 제한이 보존되어 있다.
- 같은 제한은 `data/processed/ai_library/12_2026_UNIFIED_REGULATIONS.md:31,110,113`에도 반영돼 있다. 이는 보존된 안내/요약의 근거이며 현재 운영진의 새로운 공개 허가를 확인한 것은 아니다.
- `naver-issacsim-originals/data/raw/server_backup/official_training_snapshots/2026-09-13_195915/README.md` 및 `data/raw/server_backup/extracted/training/README.md`가 공식 서버 코드 출처를 기록한다. 강의 HTML 22개와 연결 자산, 실습 자료도 포함한다.
- `naver-issacsim-nvidia/training/`은 공식 코드 계보를 갖는다. `CURRENT_SOURCE.md`의 원본 대조 기록은 재배포 허가를 뜻하지 않는다.
- 분석 저장소에는 강의 변환물·규정 원문/스냅샷도 있다. 자체 해석·실험 결론과 제공 원문을 구분해야 한다.
- 공식 공지 보존본 `naver-issacsim/data/processed/reference/public/2026-09-23_ncrc_site_snapshot/notice.json`에는 준수사항 영상의 외부 공유·재업로드 금지 문구도 있다. 해당 영상 원본을 공개 대상으로 포함한다면 별도 확인해야 한다.

선택지: 제공 자료는 비공개 보관하거나, 공개용 저장소에서 제외하거나, 운영진의 자료별 공개 허가를 확인한다. 코드 일부 삭제나 LICENSE 추가만으로 제3자 자료의 권리가 해결되지는 않는다.

### 2. 라이선스 범위 결정

5개 저장소의 현재 추적 파일에서 LICENSE/NOTICE 파일을 확인하지 못했다. `issacsimz/README.md:524–527`도 라이선스 미선택을 명시한다. 공개 저장소와 오픈소스 재사용 허가는 같은 의미가 아니다.

자체 작성 코드의 권리·기여분을 확인한 뒤 라이선스를 선택하고, 제3자 구성요소 및 코드·모델·데이터의 적용 범위를 구분한다. CONTRIBUTING/SECURITY 문서의 부재 자체를 공개 금지 사유로 취급하지 않는다.

### 3. 운영진 DM·메일과 개인 식별정보

- `naver-issacsim/data/processed/incoming/other/reviewed/GO2_R3_R5_SURVIVAL_TRACKING_ORGANIZER_DM_RECEIVED_20261008.md`는 팀별 점수를 포함한 DM 원문이다. 공개 동의를 확인하지 못했다. 비공개 보관 또는 동의된 요약 공개를 검토한다.
- 5개 저장소 모두 현재 HEAD의 author/committer 메타데이터에 noreply가 아닌 메일 주소가 있다. 이력 검사에서도 개인 메일 노출이 보고됐다. 값은 이 보고서에 재기재하지 않는다. 공개 의도 확인 후 유지/비식별 공개본 중 선택한다.
- 사용자 프로필 경로: 분석 저장소 `data/processed/ai_library/21_WINDOWS_GO2_VIDEO_AND_EVALUATION.md:265,266,269`; Originals `data/raw/external_analysis/single_videos/README.md:3`; eval `publications/2026-10-19_h1_model40300_2seed/README.md:13` 등.
- 사설 네트워크 주소: Originals `data/raw/official_server_runs/h1/2026-09-08_230725_baseline_1k/isaac_pip_freeze.txt:140–141`. 주소는 인증정보와 구별하며, 공개 필요성에 따라 비식별 처리한다.

현재 파일만 정리해도 과거 커밋·태그·Release 첨부에는 남을 수 있다. 이력 공개/새 공개본 생성은 별도 사용자 결정 사항이다. 아직 이력 재작성이나 브랜치 삭제를 하지 않았다.

## Release와 압축본

백업 인벤토리 범위: 152 Release, 600 asset, 33,033,433,028 asset bytes.

| 저장소 | Release | asset |
| --- | ---: | ---: |
| naver-issacsim | 7 | 34 |
| naver-issacsim-originals | 40 | 116 |
| naver-issacsim-nvidia | 72 | 351 |
| naver-issacsim-eval | 33 | 99 |
| issacsimz | 0 | 0 |

인벤토리 전체와 바깥 파일 목록을 확인했다. Release 본문 내용 검사는 다음 4개 표본이며, 152개 전부를 읽은 것은 아니다.

- analysis: `submission-h1-prelim-r7-20261019-model11650`
- originals: `backup-ncrc-20261020-local-working-materials`
- nvidia: `private-h1-20261018-exp-h1-action-first-planar-tracking-switch-resume10k`
- eval: `private-h1-20261019-exp-h1-joint-tracking-balance-ang070-model12900-local-eval`

표본 본문/메타데이터의 제한적 패턴 검색에서 토큰·암호 등의 일치는 보고되지 않았다. GitHub 작성자 로그인은 포함된다. `private-` 태그는 접근제어 장치가 아니므로 저장소 공개 전환 시 첨부까지 공개되는 범위를 따로 검토해야 한다.

Originals의 작업 자료 보존 Release는 `NCRC_remaining_local_working_materials_20261020.zip`을 포함한다. preservation manifest 167개 상대경로에서는 credential 유사 경로를 찾지 못했지만, 중첩 ZIP 본문은 미검사다. 학습 tar/ZIP과 모델도 전체 내용 검사가 끝난 것이 아니다.

평가 ZIP `naver-issacsim-eval/publications/2026-10-19_h1_top01_angtrack060_model12900/h1-top01-angtrack060-plus3k_model_12900_LOCAL_evaluation_20261019.zip`에서 `evaluation_manifest.json`, `diagnostics.json`, `video_evaluation_link.json`을 표본 확인했다. 위 eval Release의 첨부와 연결되며, `evaluation_manifest.json`의 `task_root`에 Windows 절대 경로가 있다. 메인도 해당 필드를 ZIP에서 읽어 재확인했다. 경로 존재 자체가 비밀 유출이나 공개 차단 사유는 아니지만, 공개 사본의 이식성·식별정보 정리에 참고한다. 원본 evidence를 덮어쓰지 않고 공개용 사본을 별도 생성하는 방식이 적절하다.

## 검사 범위와 한계

- 보안 에이전트: 추적된 텍스트 및 로컬 `--all` ref 변경 이력에서 주요 AWS/GitHub 키 형식, 개인키 헤더, 긴 Bearer 값, 인증정보 포함 URL 등을 검색했다. 사용 가능한 자격증명은 발견하지 못했다. 포괄적인 무비밀정보 보증은 아니다.
- 원격에서 다시 fetch하지 않았으므로 검사 기준은 현재 로컬 refs와 방금 만든 백업 인벤토리다.
- 바이너리 모델, 영상 프레임, 모든 중첩 압축파일, 미추적/ignored 임시 파일을 전수 검사하지 않았다. 접근 거부가 발생한 ignored 테스트 임시 폴더는 우회 접근하지 않았다.
- eval의 미추적 publication 파일 7개는 사용자 자료로 보존했다. 공개 커밋 범위와 구별한다.
- 루트 로컬 전용 `AGENTS.md`/`AGENTS.disabled.md`는 공개 대상이 아니다. eval의 추적된 `AGENTS.md`는 별도 평가기 지침이며 루트 로컬 전용 파일과 혼동하지 않는다.

## 권장 후속 순서 — 아직 실행하지 않음

1. 공식 제공 코드·강의·실습·DM·정책/결과물 중 공개할 범위를 사용자와 확정하고 필요한 공개 허가를 확인한다.
2. 자체 작성 코드 중심의 공개용 사본을 준비하고, 데이터/원본 보관 저장소는 비공개로 분리하는 방안을 검토한다.
3. 범위가 정해진 Release 첨부와 중첩 압축본의 텍스트·설정·자격증명 경로를 검사한다. 공개용 정리본과 원본의 provenance/hash를 구분한다.
4. 개인 이메일/경로 공개 여부와 자체 코드 라이선스를 결정한다. 이후에만 필요한 이력 정리와 공개 전환을 수행한다.
5. 보관본은 `Downloads/NCRC_5REPO_ARCHIVE_20261023_PARTIAL_LFS`에 있다. 과거 LFS 이미지 96개(306,487,951 bytes)가 미복구이므로 기존 이력/다른 백업을 파기할 근거로 사용하지 않는다.

이번 작업에서 원격 변경, 브랜치 삭제, 이력 재작성, 라이선스 부여, 제공 자료 삭제는 하지 않았다.
