# 실행환경과 외부 구성요소

이 목록은 실제 코드의 import/명령 사용에 근거한 실행환경 안내이며, 모든 upstream 라이선스를 대신하는 고지가 아니다. 자체 코드 라이선스와 제3자 이용 조건은 별도로 확인 중이다.

Python 코드는 3.10 이상을 전제로 한다. 실제 simulator Python과 호환되는 버전을 사용한다.

| 구성 | 필요한 환경 | 포함 여부 |
| --- | --- | --- |
| 평가 core·저장 결과 비교 | Python 표준 라이브러리 | 자체 Python 코드 포함 |
| 시뮬레이터 평가·영상 | Isaac Sim, Isaac Lab, PyTorch, RSL-RL, Gymnasium 및 task에 필요한 패키지 | 외부 설치 필요 |
| 영상 저장 경로 | 실행 환경의 MoviePy/영상 인코딩 도구, H1 경로의 imageio-ffmpeg | 외부 설치 필요 |
| sidecar CLI | Python 표준 라이브러리 | 자체 코드 포함 |
| sidecar 셸 | Bash, Git, tmux 및 일반 Linux CLI | 외부 설치 필요 |
| 선택적 개인 Release 게시 | GitHub CLI 및 사용자 인증 | 자격증명 미포함 |
| checkpoint milestone 선택 | TensorBoard | 외부 설치 필요 |

버전은 실제 Isaac/task 설치와 호환되는 조합을 사용해야 한다. 과거 setup 스크립트에 적힌 고정 버전이 모든 시스템에서 동작하거나 최신이라는 뜻은 아니다. upstream 바이너리·task 소스·학습 에셋은 묶어 배포하지 않는다.

`sidecar/scripts/organizer_keep_all_ckpt.sh`는 run별 보존을 위한 변형 도구라는 출처 설명을 유지한다. 별도로 제공됐던 원문 keeper와 그 내용을 내장한 byte-identity 테스트는 이 배포본에서 제외했다. 그 외 코드의 출처·기여 권리 검토와 라이선스 결정은 계속 진행 중이다.
