# NCRC Robotics Research Tools

H1·Go2 실험 과정에서 작성한 평가·evidence·실험 관리 도구의 공개 준비 저장소입니다.

**준비 중:** 라이선스는 아직 결정되지 않았습니다. 공개 열람과 재사용 허가는 다르며, 현재 이 저장소가 포괄적인 오픈소스 라이선스를 제공한다고 가정하지 마세요.

## 구성

- `evaluation/`: 정책 비교·정량 평가·6지형 영상 실행 도구. 공식 평가기를 복제한 것이 아니며 결과는 자체 진단용입니다.
- `sidecar/`: 외부 학습 코드의 실행과 evidence 수집을 돕는 `issacsimz` 도구의 공개 후보.
- `server_tools/`: 독립적인 환경 준비·TensorBoard/checkpoint 보조 도구.
- `knowledge/`: 공개 가능한 자체 실험 방법·판단 원칙. 제공 원문과 내부 대화는 포함하지 않습니다.
- [공개 범위와 상태](PUBLICATION_STATUS.md)
- [CPU 검증 결과와 한계](VERIFICATION.md)

각 도구는 독립된 하위 폴더에서 사용합니다. 평가 명령은 `evaluation/`, sidecar 명령은 `sidecar/`에서 실행하세요. 이 저장소 전체를 자동 설치·실행하는 통합 명령은 없습니다.

Isaac Sim·Isaac Lab 및 학습 task는 별도로 준비해야 합니다. 이 저장소는 공식 training 코드·강의·실습 배포본, 원본 정책 checkpoint, 개인 자격증명을 제공하지 않습니다. 원래 비공개 저장소의 Git 이력과 Release도 가져오지 않습니다.

GPU 작업, 외부 업로드, 서버 종료는 설치나 문서 열람의 일부로 자동 실행하지 않습니다. 공개 후보의 CPU 검증과 실제 GPU/서버 검증은 구분해서 기록합니다.
