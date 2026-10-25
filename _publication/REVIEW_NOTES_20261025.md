# 추가 공개 검토와 역사적 표현의 해석 — 2026-10-25

이 문서는 공개 사본의 개인정보 보정과 아직 확인하지 못한 공개 범위를 구분한다. 원본 기록·실제 작업 이력·수치는 사후 변경하지 않는다. 공개된 요약이 모두 허가받았다는 보증이나 규정 위반 판정이 아니다.

## 완료한 개인정보 보정

`naver-issacsim/data/processed/operations/windows_go2_video_evaluation/combined_archives_verified.json`의 여섯 경로에서 JSON Unicode escape로 남아 있던 Windows 프로필 계정명 일부를 제거했다. `[USER]` 뒤에는 경로 구분자만 남는다. 계정명 외의 바이트와 private 원본은 유지하며 `FILES.json`의 공개 SHA를 갱신했다. checkpoint·ZIP의 기존 해시·크기·평가 상태는 바꾸지 않았다.

로컬 공개 생성기도 기존 제외목록과 검토 제외목록을 출력 전에 적용하도록 보완했다. 재생성 전체는 실행하지 않았으며, 경로 블라인드와 제외 후보의 읽기·쓰기 차단에 대한 회귀 테스트 3개를 통과했다. 공개 manifest 1,070개 해시, 제외목록과의 충돌 부재, 해당 JSON의 원본 대비 계정명 외 바이트 보존을 확인했다. 생성기와 테스트는 로컬 준비 도구이며 이 공개 snapshot에 포함된 실행기는 아니다.

### Release ZIP 추가 보정

`eval--private-h1-20261019-model40300-2seed-personal-eval`의 `model_40300_h1_LOCAL_evaluation_2seed_20261019.zip`에서도 `launcher_result.json`에 JSON escape로 남은 계정명 일부를 확인해 공개 ZIP을 교체했다. 원격 digest는 새 공개 SHA `72dd91f30d8c6dcaf5f1cf035bf5c4ba042e48ae2c0c6ccb1a5c846b2c90f77f`, 크기는 377,556 bytes로 확인했다. 원래 ZIP 8개 구성원 중 이전 공개 사본 대비 해당 JSON만 변경됐으며 평가 원자료·다른 구성원·private 원본은 그대로다. 부속 원본 checksum은 원본 자료 기준으로 보존하므로 공개 asset 검증에는 `RELEASES.json`을 사용한다.

별도 Release 생성기의 동일한 정규식도 보완했고 4가지 경로 fixture의 회귀 테스트를 통과했다. 기존 로컬 공개 캐시 사본은 이전 상태 확인용으로 보존하며 최신 manifest SHA와 일치하는 보정 ZIP을 게시본으로 구분한다. 과거 다운로드 사본까지 회수했다는 뜻은 아니다.

## 운영진 승인 표현은 보존 방법의 범위로 읽어야 함

`naver-issacsim/data/processed/ai_library/17_ISSACSIMZ_VIDEO_OPERATIONS.md:73` 및 `14_H1_NEXT_RUN_PARAMETER_COMPARISON.md:441`의 승인 표현은 checkpoint 보존 방법과 프로젝트 구현물을 구분해서 읽어야 한다. 보존된 운영진 답변에는 저장 주기 지정, 학습 중 checkpoint 복사, 선택 checkpoint를 공식 play 경로에 두는 방법에 대한 안내가 있다. 이 기록만으로 `issacsimz`나 wrapper 전체에 대한 별도 승인을 확인한 것은 아니다. 공개 `issacsimz/README.md`도 프로젝트 keeper가 원래 안내를 run별 orchestration에 맞게 변형한 구현물임을 구분한다.

## 공개 허용 범위가 아직 확인되지 않은 요약

다음은 개인정보 누출이나 위반으로 확정한 목록이 아니다. 원문 공개·일반 지식·자체 결과·사적 응답의 파생 요약을 구분하기 위한 검토 상태다. 요약 공개에 대한 허가는 이번 확인 자료에서 확보하지 못했으므로 허가 완료로 취급하지 않는다.

| 대상 | 확인된 내용 | 남은 판단 |
| --- | --- | --- |
| `ai_library/12_2026_UNIFIED_REGULATIONS.md:111-112` | 현재 제외한 준수사항 영상의 짧은 요약이 남아 있음. | 영상 공유 제한이 이 요약에 적용되는지 별도 확인 필요. 상세 재구성 문서의 제외와 동일시하지 않음. |
| `ai_library/02_GUIDEBOOK_SIMULATION_BASICS.md`, `03_GUIDEBOOK_SENSORS_CONTROL_RL.md`, `04_GUIDEBOOK_TRAINING_COMMANDS_APPENDIX.md` | 강의를 출처로 밝히며 일반 기술 개념과 자체 운영 판단도 포함함. | 출처만으로 일괄 금지라고 단정하지 않음. 제공 원문 표현·코드의 실질적 재현 및 허가 범위를 확인해야 함. |
| `ai_library/05_TRAINING_RULES_AND_SUBMISSION.md:149-153`, `07_QUADRUPED_TRAINING_CODE.md:151`와 관련 연구 문서 | 자기 팀의 비공개 평가 응답에서 유래했다고 기록된 판정·유사도 요약. | 해당 응답 요약의 공개 동의 범위 미확인. 타 팀 자료·credential로 확인된 것은 아님. |
| `ai_library/07_QUADRUPED_TRAINING_CODE.md:60`, `15_OPTUNA_REWARD_DECISION_ENGINE.md:232`, `research/experiments/go2/G-001.md:57` 등 | 운영진 DM에서 제공받은 자기 팀 점수 구성의 파생 요약. | 수신 내용의 공개 동의 범위 미확인. 팀 자체 실험 결과의 권리와 별개로 검토. |

표의 경로는 공개본 `naver-issacsim/data/processed/` 또는 `naver-issacsim/` 아래의 상대 경로다. 문서는 역사적 내용 그대로 유지하며, 이 안내가 공개 허가를 대신하지 않는다. 원본·과거 Git 이력·Release 삭제나 이력 재작성은 수행하지 않았다.
