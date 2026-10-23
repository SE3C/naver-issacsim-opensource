# 서버·체크포인트 보조 도구

공식 training 소스와 분리한 자체 설치·운영 유틸리티의 보존 사본입니다. 외부 Isaac 설치·학습 task는 포함하지 않습니다.

- `scripts/select_h1_milestone_bests.py`: TensorBoard의 `Train/mean_reward`와 numbered checkpoint를 연결해 milestone별 후보를 선택합니다. `tensorboard`가 필요합니다. 최고 reward가 곧 최선 정책이라는 보장은 없습니다.
- `NCRC_H1_Brev_L40S_A6000_setup_script.txt`, `scripts/prepare_brev_rc19.sh`: 특정 시기의 NVIDIA 환경 설치 절차입니다. 패키지 설치·다운로드·기존 환경 변경이 있으므로 내용과 upstream 이용 조건을 확인한 후 명시적으로 실행하세요. 최신 환경을 보장하지 않습니다.
- `scripts/ncrc_l40s_prepare.sh`: 개인 환경의 선택적인 GitHub CLI 인증 준비입니다. 토큰을 배포하지 않습니다. 공식 대회 서버용 절차가 아닙니다.

추가로 보존된 `record*`, `run*`, `issacsimz_train_release.sh`는 과거 학습/영상/게시 wrapper입니다. 일부는 이 폴더에 없는 `training/`과 기존 저장소 배치를 전제로 하므로 standalone 진입점으로 제공하지 않습니다. 일부 패키징 경로는 외부 소스 파일을 산출물에 복사하거나 GitHub 게시를 수행할 수 있습니다. 결과물의 재배포 권한은 도구 자체와 별도로 확인해야 합니다.

이 폴더를 복사하거나 읽는 작업은 설치·GPU 실행·게시·서버 중지 권한을 의미하지 않습니다. 어떤 스크립트도 공개 준비 과정에서 서버에 실행하지 않았습니다.
