# H1 공식 서버 baseline 300-iteration 실행 원본

## 출처와 범위

- 수집 위치: 사용자 PC `Downloads`
- 수집 기준: 2026-08-24 12:50 이후 생성·다운로드된 파일
- 실행 식별 시각: `env.yaml`의 `log_dir`에 기록된 `2026-08-24_12-44-13`
- 보존 원칙: 파일 내용과 다운로드 당시 파일명을 수정하지 않음

## 파일에서 직접 확인되는 실행 정보

| 항목 | 값 | 근거 파일 |
| --- | --- | --- |
| 로봇 | Unitree H1 | `env.yaml`의 H1 USD 경로 |
| device | `cuda:0` | `env.yaml` |
| seed | `42` | `env.yaml` |
| 병렬 환경 수 | `4096` | `env.yaml`의 `scene.num_envs` |
| 총 반복 수 | `300` | `report.html` |
| 보고된 실행 시간 | 약 4분 | `report.html` |

`report.html`은 정상 UTF-8 원본이다. PowerShell 5.1 등에서 기본 인코딩으로 읽으면 한글이 깨져 보일 수 있으므로 `Get-Content -Encoding UTF8`처럼 UTF-8을 명시한다. 위 표는 파일에서 명확히 식별되는 값만 기록하며 정책 성능에 대한 판정은 포함하지 않는다.

## 포함 파일

| 파일 | 크기(byte) | SHA-256 |
| --- | ---: | --- |
| `env.yaml` | 33,529 | `6E04EB361C49D3DE8FF43C05F1A08434AE865B427EA5DB446F5795B6916FF778` |
| `env_20260824124413.yaml` | 33,529 | `6E04EB361C49D3DE8FF43C05F1A08434AE865B427EA5DB446F5795B6916FF778` |
| `model_best.pt` | 7,151,403 | `B0BD703339ADFE36A67FBF896F8E115B836C547C09A15C7628433635F81CE23D` |
| `model_best_20260824124413.pt` | 7,151,403 | `B0BD703339ADFE36A67FBF896F8E115B836C547C09A15C7628433635F81CE23D` |
| `play_video.mp4` | 3,071,312 | `CAABFB3D84C3C6A11D3BC3E735E405C13E107D9D4F39AC5FCC39566A4ECD694A` |
| `play_video_20260824_125054.mp4` | 3,071,312 | `CAABFB3D84C3C6A11D3BC3E735E405C13E107D9D4F39AC5FCC39566A4ECD694A` |
| `policy.onnx` | 1,194,183 | `0EC4AA99A05922212516FE1021E82F933E156CD500438AE749B6E566085A22B3` |
| `policy_20260824_125054.onnx` | 1,194,183 | `0EC4AA99A05922212516FE1021E82F933E156CD500438AE749B6E566085A22B3` |
| `policy.pt` | 1,206,102 | `D4332260025926050C2FE38E410059BB78DE84819F1D31C1EE2C3B0DF689334D` |
| `policy_20260824_125054.pt` | 1,206,102 | `D4332260025926050C2FE38E410059BB78DE84819F1D31C1EE2C3B0DF689334D` |
| `report.html` | 12,796 | `4B2E225D79BFA3A03EFDE37A2EE02FAEC1569B82C6F21E377A4D5ADAA57E2486` |

## 동일 내용의 별칭 파일

다음 쌍은 파일명이 다르지만 SHA-256과 바이트 크기가 완전히 같다.

- `env.yaml` = `env_20260824124413.yaml`
- `model_best.pt` = `model_best_20260824124413.pt`
- `play_video.mp4` = `play_video_20260824_125054.mp4`
- `policy.onnx` = `policy_20260824_125054.onnx`
- `policy.pt` = `policy_20260824_125054.pt`

원본 다운로드 묶음을 그대로 남기기 위해 두 이름을 모두 보관했다. Git LFS에서는 동일 콘텐츠가 해시 기반 객체 하나로 처리된다.

## 이 묶음에 없는 진단 자료

이번 다운로드 묶음에는 다음 파일이 없으므로 GPU 처리량이나 iteration별 시간을 이 자료만으로 정밀 재현할 수 없다.

- 콘솔 학습 로그
- `nvidia-smi` 출력 또는 시계열 측정값
- `train.py --help` 출력
- TensorBoard 원본 이벤트 파일
- 실행 당시 reward 파일의 별도 해시 또는 diff

따라서 이 폴더는 정책 산출물과 환경 설정의 원본 아카이브이며, 완전한 성능 진단 패키지는 아니다.
