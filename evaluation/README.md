# 정책 평가와 6지형 영상

외부 Isaac Sim/Lab 및 H1·Go2 task를 이용하는 자체 진단 도구입니다. 공식 평가 서버의 구현이나 점수 변환식을 재현한다고 주장하지 않습니다. `SCORING_SPEC.md`는 자체 지표 계산 계약입니다.

아래 상대 경로 명령은 이 저장소의 `evaluation/` 폴더에서 실행합니다.

## CPU 비교

완료된 평가 폴더 두 개를 비교합니다. checkpoint 경로를 주면 별도의 GPU 수집이 필요하므로, 기존 결과 비교와 구별하세요.

```powershell
py -3 compare_cli.py --a C:\results\candidate --b C:\results\reference --output C:\results\comparison
```

## Windows 설치·영상·정량 평가

설치 미리보기는 GPU를 사용하지 않습니다. 실제 설치는 대상에 파일을 복사하므로 출력 내용을 확인한 뒤 실행합니다.

```powershell
.\install_windows.ps1 -Preview
.\install_windows.ps1 -Destination C:\NCRC
```

외부 Isaac 설치와 task 경로는 실행기의 인수/환경 설정에 맞춰 준비해야 합니다. 기존 기본 경로 `C:\NCRC`, `C:\isaacsim`은 예시 설치 관례이며 이 저장소가 해당 프로그램이나 task를 포함한다는 뜻이 아닙니다. 상세 인수는 각 `.ps1`의 `param` 블록과 CLI `--help`를 확인하세요.

```powershell
C:\NCRC\h1_6terrain_video.bat -Path C:\models\model_N.pt
C:\NCRC\go2_6terrain_video.bat -Path C:\models\model_N.pt
```

H1에서 영상 없이 정량 평가만 할 때는 `-EvaluationOnly`를 붙입니다. Go2에도 같은 옵션이 있다고 가정하지 마세요. 위 명령은 실제 GPU 작업이므로 설치 검증의 일부로 자동 실행하지 않습니다.

## CPU 검증

```powershell
py -3 -m unittest discover -s tests -v
```

평가 데이터·정책·영상·개인 실행 이력은 배포하지 않습니다. 결과에는 실행 경로·장비 정보가 기록될 수 있으므로 외부 공개 전에 별도로 확인하세요. Python 소스를 바꾸면 `windows_bundle_manifest.json`의 해당 SHA도 갱신해야 합니다.
