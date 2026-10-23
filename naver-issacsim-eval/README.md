# naver-issacsim-eval — PERSONAL 정책 평가기 v1

학습이 끝난 선택 정책을 **PERSONAL 환경에서 사후 평가**합니다. H1·Go2에 각각 독립적인 0–100 내부 점수를 내고, 같은 조건의 정책 A/B 차이와 cohort bootstrap 95% 신뢰구간을 계산합니다. 공식 Tracking 변환식과 명령값은 공개되지 않았으므로 공식 점수나 예선 총점을 예측하는 도구가 아닙니다.

v0의 점수 계산 초안에서 확장하여 camera-off 실행기, 종료/reset 전 수집, 평가조건·정책 식별, calibration, paired cohort 비교와 로컬 테스트를 추가했습니다. v0 원본과 기존 evidence는 수정하지 않습니다.

**점수 계산만 다룰 때는 `eval_core.py`와 `SCORING_SPEC.md`를 먼저 사용하세요.** 반복 평가/실행 환경 작업은 `isaac_runner.py`·launcher 쪽으로 분리돼 있습니다.

**Windows Go2 통합 실행기와 실제 개별 full 평가가 검증됐고, 같은 구조의 H1 통합 경로도 추가됐습니다.** `go2_6terrain_video.bat`와 `h1_6terrain_video.bat`는 각각 고정 6영상 ZIP 뒤 별도 camera-off `scenario7` 평가를 실행합니다. Go2 2950·7050 full 기록은 기존 6영상 receipt를 재사용한 개별 실행이며, H1 통합 source는 2026-10-04 단계에서는 구현·CPU 검증만 확보했으나, **2026-10-07 `ORIENT-100 / model_2850`의 Windows PERSONAL 6영상 + camera-off `scenario7` full 결과**가 별도 evidence로 수신됐습니다(8 case × 3 seed × 128 env = 3,072/3,072 episode 20초 timeout). 이 기록은 한 정책의 full 완료 근거이지 H1 matched A/B·모든 checkpoint 호환·공식 점수가 아닙니다. [분석 원문](https://github.com/SE3C/naver-issacsim/blob/main/data/processed/incoming/other/reviewed/H1_ORIENT-100_POLICY_ANALYSIS_20261007.md). Go2는 [Windows Go2 지침](WINDOWS_WORKFLOW.md), H1은 [Windows H1 지침](WINDOWS_H1_WORKFLOW.md)을 따르세요. [최초 인계 문서](WINDOWS_VIDEO_EVAL_HANDOFF.md)는 Go2 실패 당시의 역사 기록입니다. 실제 A/B 점수·비교 보고서는 수행하지 않았습니다.

## 저장소 역할

| 저장소 | 역할 |
| --- | --- |
| [`naver-issacsim`](https://github.com/SE3C/naver-issacsim) | 분석·문서·AI 라이브러리·실험 registry와 실제 제출 snapshot |
| [`naver-issacsim-originals`](https://github.com/SE3C/naver-issacsim-originals) | 원본 자료·대용량 에셋·공식/개인 실행의 canonical evidence 보존 |
| [`naver-issacsim-nvidia`](https://github.com/SE3C/naver-issacsim-nvidia) | H1/Go2 학습 source·개인 NVIDIA 서버 학습 및 native 영상 Release |
| [`naver-issacsim-eval`](https://github.com/SE3C/naver-issacsim-eval) | PERSONAL 사후 평가·Windows H1/Go2 실행기·새 PC 평가 Release·명시적 정책 비교 |
| [`issacsimz`](https://codeberg.org/passerby1/issacsimz) | 별도 공개 실행/evidence sidecar; 공식 학습 source를 수정하지 않음 |

## 빠른 안내

- 사후 평가 Release 위치·기존 자료: [EVALUATION_RELEASES.md](EVALUATION_RELEASES.md)
- 학습·분석·원문 연결: [Analysis 정책 탐색표](https://github.com/SE3C/naver-issacsim/blob/main/data/processed/experiments/RECENT_POLICY_LINKS.md)
- 게시·검증 기록: [Go2 운영 색인](https://github.com/SE3C/naver-issacsim/blob/main/data/processed/operations/windows_go2_video_evaluation/README.md) · [H1 운영 색인](https://github.com/SE3C/naver-issacsim/blob/main/data/processed/operations/windows_h1_video_evaluation/README.md). 이 색인은 Analysis main에 반영됐으며 결과 원문을 재작성하지 않는다.
- Windows Go2 통합 실행·설치: [WINDOWS_WORKFLOW.md](WINDOWS_WORKFLOW.md)
- Windows H1 통합 실행·설치: [WINDOWS_H1_WORKFLOW.md](WINDOWS_H1_WORKFLOW.md)
- 점수 계산과 검증: [SCORING_SPEC.md](SCORING_SPEC.md) · [VERIFICATION.md](VERIFICATION.md)
- 실험 추적: [analysis registry](https://github.com/SE3C/naver-issacsim/blob/main/research/EXPERIMENTS.md)

## 부분 완료·후처리 실패의 안전한 전달

Windows 6영상/평가 통합 실행기에서 사용자가 **별도로** `-CompareWith`를 요청한 경우, 통합 ZIP과 평가가 끝난 다음 비교 단계에서 실패할 수 있다. 이때 전체 요청 exit status는 실패여도 앞 단계의 산출물이 이미 있을 수 있다. **단계별 실제 receipt/manifest/ZIP CRC·identity를 확인하여** `완료된 영상`, `완료된 full 평가`, `완료된 통합 ZIP`, `실패한 비교`, `아직 확인되지 않은 단계`를 분리해서 보고한다. ZIP 파일 존재만으로 검증 PASS를 단정하거나, 후속 비교 실패를 전체 성공으로 바꾸지 않는다.

평가가 성공했고 **포장·게시만 실패**한 경우에는 먼저 기존 video receipt·평가 manifest·episode row completeness·checkpoint SHA·protocol을 확인한다. 충분하면 기존 파일을 사용한 **CPU 포장·검증** 가능성을 점검하고, 새 GPU 영상·평가를 기본 재실행하지 않는다. `-VideoResult`는 영상 재사용 옵션일 뿐 저장된 평가까지 재사용하지 않는다. 원래 실패 receipt·로그를 보존하고 새 복구 기록으로 단계별 결과를 연결한다. 평가 파일이 미완료·손상되었거나 기존 포장 기능의 입력 계약이 맞지 않으면 자동 복구하지 않는다. 이는 **운영 지침**이며 여기서 런처의 런타임 성공·설치본 실행을 재검증한 것은 아니다.

## 두 경로 입력 → 비교 리포트

비교는 사용자가 명시적으로 요청할 때만 실행합니다. “6영상 뽑고 평가 돌려줘”의 기본 산출물은 checkpoint별 영상 ZIP과 개별 raw 평가자료이며 비교 보고서는 포함하지 않습니다. 저장 평가 폴더 입력은 CPU 비교이고 `.pt` 입력은 새 GPU 평가를 시작할 수 있습니다. 아래 standalone 비교는 통합 실행기의 ASCII staging을 제공하지 않으므로 한글 checkpoint 경로의 실제 GPU 성공을 가정하지 않습니다.

Windows에서는 저장소의 **`compare_policies.bat`을 더블클릭**한 뒤 A(후보)와 B(비교 기준)의 `.pt` 경로를 입력합니다. 기본은 Go2·128 env·seed 4201/4202/4203·scenario7이며, A/B를 같은 조건으로 **전체 평가**한 후 `comparison.html`과 `comparison.json`을 만듭니다. 결과는 A 파일 옆의 새로운 `comparison-go2-...` 폴더에 저장합니다. 기존 checkpoint는 이동·수정·삭제하지 않습니다.

```powershell
# C:\NCRC 배치본. 저장소 안에서는 .\compare_policies.ps1로도 실행 가능
& C:\NCRC\compare_policies.ps1 -A "C:\models\candidate.pt" -B "C:\models\reference.pt"
# H1 또는 6지형 정량 진단을 선택할 때
& C:\NCRC\compare_policies.ps1 -Robot h1 -A "C:\models\a.pt" -B "C:\models\b.pt" -Suite terrain6
# 명령만 확인: GPU 실행 없음
& C:\NCRC\compare_policies.ps1 -A "C:\models\a.pt" -B "C:\models\b.pt" -Preview
```

기존 `C:\NCRC\IsaacLab`과 `C:\NCRC\naver-issacsim-nvidia\training\{quadruped,humanoid}`를 사용합니다. 다른 설치 위치는 `-LabRoot`/`-TaskRoot`로 지정합니다. SDK의 `_isaac_sim\python.bat`을 직접 호출해 실패 exit code를 유지하고, native play와 동일한 공개 RSL-RL config 변환 함수를 재사용합니다. 설치·task source 변경은 하지 않습니다. 영상 렌더링이 끝난 뒤 실행하세요. 비교는 2초 smoke가 아니며 simulator 초기화와 전체 평가 시간이 듭니다.

두 파일 모두 export된 TorchScript `policy.pt`이면 `-PolicyA -PolicyB`를 함께 붙입니다. 확장자만으로 형식을 추측하지 않으며 native/TorchScript 혼합 비교는 거부합니다. A/B 평가 중 하나라도 실패하거나 실행 프로토콜이 다르면 리포트를 만들지 않고 raw output을 보존합니다.

**보정 파일을 지정하지 않으면 B를 기준으로 잠정 calibration을 생성**합니다. B를 바꾸거나 A/B를 뒤집으면 점수 척도가 달라지므로 서로 다른 쌍의 점수를 전체 순위처럼 비교하지 않습니다. 공식 점수가 아니며 자동 제출·채택 판정도 하지 않습니다. 기존 보정 파일은 `-Calibration "C:\path\calibration.json"`으로 지정할 수 있고, 적용한 calibration은 결과 폴더에 보존합니다.

이미 완료된 평가 폴더 두 개를 넣으면 GPU 재실행 없이 리포트만 만듭니다. 이 경우 기본 Python으로도 실행할 수 있습니다:

```powershell
py -3 compare_cli.py --a "C:\eval-A" --b "C:\eval-B" --robot go2
```

Linux/Brev에서는 IsaacLab 환경의 Python으로 같은 CLI를 사용합니다. `--a`/`--b`를 생략하면 순서대로 경로를 묻습니다:

```bash
bash /path/IsaacLab/isaaclab.sh -p /path/naver-issacsim-eval/compare_cli.py \
  --a /path/candidate.pt --b /path/reference.pt --robot go2 \
  --isaaclab-root /path/IsaacLab --task-root /path/training/quadruped
```

## 평가 구성

| suite | 목적 | episode 처리 |
| --- | --- | --- |
| `scenario7` | 공개 7시나리오·가중치를 참고한 내부 평가 | 각 환경을 20초 평가. 낙상마다 실패 episode를 기록하고 재시작. 끝까지 진행 중인 episode는 생존으로 기록 |
| `terrain6` | 계단·역계단·박스·요철·상향/하향 경사의 진단 | 환경별 첫 episode만 평가, 최대 20초. timeout을 traversal 성공으로 해석하지 않음 |

`scenario7`의 H1 가중치는 균형 .15 / 전진 .20 / 측면 .10 / 복합회전 .10 / 요철 .15 / 경사 .15 / 밀침 .15입니다. Go2는 전진 .15 / 전방위 .15 / 요철 .20 / 경사 .15 / 계단 .15 / 밀침 .10 / 랜덤화 .10입니다. `terrain6`는 내부 진단용 균등 가중치이며 공식 7시나리오 점수와 섞지 않습니다.

매 step 몸통 좌표계 `sqrt(Δvx²+Δvy²+Δyaw²)`를 계산합니다. episode 평균 → 길이와 무관한 episode 동일가중 평균 → `exp(-ln(2) × error/e50)` 순서로 Tracking을 산출합니다. 시나리오 점수는 Survival × 내부 Tracking, 전체 점수는 시나리오 가중합 ×100입니다. m/s와 rad/s를 별도로 정규화하지 않는 것은 제공된 운영진 답변에 맞춘 것입니다. `e50`은 우리 내부 calibration 값입니다.

**명령 스케줄, randomization 범위, 밀침 강도, 난이도는 내부 기준**입니다. 실제 공식 evaluator의 비공개 값을 재현한 것이 아닙니다. `eval_core.py suite` 명령으로 모든 설정을 확인할 수 있고 manifest에 그대로 남습니다. Go2 경사는 ±20°(`tan20°`), H1은 ±10°(`tan10°`)입니다. Go2 scenario7 계단은 12.5cm로 고정합니다. terrain6는 해당 task 지형의 난이도 1.0을 사용하므로 과거 2026-09-15 evaluator와 완전 동일하다고 주장하지 않습니다.

Go2 랜덤화 case는 요철 지형에 마찰계수 0.6–1.2와 몸통 추가 질량 −1–+1kg을 사용합니다. 적용된 native event 설정도 저장하며 지원하지 않는 source에서는 조용히 생략하지 않고 중단합니다. observation noise와 terrain curriculum, native interval push는 끄고 밀침 case에서만 평가 시작 4·8·12·16초에 정해진 XY 속도 변화를 줍니다. 명령은 각 episode 시작부터 10초 간격으로 전환합니다. 세계 좌표 X/Y 변위와 몸통 전진 속도 적분은 별도 지표입니다. 회전 명령이 있으면 몸통 전진 속도 적분을 실제 세계 X 전진 거리로 읽으면 안 됩니다.

## 운영 규칙과 실행 전 준비

개인 PC/WSL 또는 개인 Brev에서 이미 준비된 Isaac Sim/Lab·task checkout을 사용합니다. 이 패키지는 설치·clone·로그인·학습·export·publish·서버 종료를 하지 않습니다. 공식 서버에서는 실행하지 않습니다.

필요한 입력은 `model_N.pt` 같은 RSL-RL checkpoint 또는 export된 TorchScript `policy.pt` 하나입니다. 원본을 `model_best.pt`로 덮어쓸 필요가 없습니다. `policy.onnx`는 지원하지 않습니다. native checkpoint는 설치된 RSL-RL runner가 optimizer를 로드하지 않고 inference policy를 만듭니다. TorchScript는 export에 포함된 normalization을 사용합니다. task source·observation/action 구성은 정책과 호환되어야 합니다. 저장된 env.yaml과 source evidence를 먼저 확인해 해당 task checkout을 선택하세요. YAML을 임의 실행하거나 현재 reward 파일에 쓰지 않습니다.

`--source-run-id`, `--preset`은 출처 표기입니다. OFFICIAL checkpoint를 PERSONAL에서 평가해도 평가 결과의 환경은 PERSONAL입니다. 제출 provenance의 증명은 기존 canonical evidence가 담당하며 이름이나 사용자 표기만으로 공식 출처를 인증하지 않습니다.

## 1. GPU 없는 로컬 검증

Python 3.10 이상이면 scorer와 테스트는 추가 패키지가 필요 없습니다. Linux에서는 해당 환경의 `python`, Windows에서는 `py -3`를 사용하세요.

```bash
cd /path/se3c_policy_evaluator_v1
python -m unittest discover -s tests -v
python eval_core.py demo --out ./demo-results --robot go2
python eval_core.py compare --a ./demo-results/a --b ./demo-results/b \
  --calibration ./demo-results/calibration.json --out ./demo-comparison.json --bootstrap 200
```

demo는 **합성 데이터**이며 실제 checkpoint 결과가 아닙니다. JSON과 HTML을 열어 출력 흐름만 확인합니다. demo 출력 폴더는 새 경로로 지정하세요.

## 2. Windows 통합 실행 — full 전용

H1에서 영상 없이 full 평가만 실행하려면 `C:\NCRC\h1_6terrain_video.bat -Path "C:\path\model_N.pt" -EvaluationOnly`를 사용한다. 영상 receipt가 필요 없으며 checkpoint 옆에 평가 원자료 7개 폴더를 저장한다. 영상·통합 ZIP은 생성하지 않는다. 옵션 생략 시 기존 6영상+full 흐름을 유지한다. [H1 실행 계약](WINDOWS_H1_WORKFLOW.md).

`C:\NCRC\h1_6terrain_video.bat` 또는 `go2_6terrain_video.bat`에 native checkpoint 경로를 입력한다. 고정 6영상 후 별도 camera-off scenario7 full 평가를 수행하고, 18개 파일의 단일 ZIP을 checkpoint 옆에 만든다. 기존 video receipt는 `-VideoResult`로 재사용할 수 있다. 별도 eval_smoke 실행기와 통합 `-EvaluationSmoke` 옵션은 제거했다. core의 내부 진단과 과거 실패 증거는 보존하며, smoke/incomplete 데이터는 full 결과로 포장하지 않는다. 설치·CPU 검증은 GPU 검증이 아니다.

## 3. 전체 평가

같은 source checkout·IsaacLab·device·env 수·seed·suite로 A와 B를 각각 실행합니다. checkpoint 파일만 바꿉니다. 각 출력은 비어 있는 새 디렉터리여야 합니다.

```bash
bash run_evaluation.sh --isaaclab-root /path/IsaacLab \
  --robot go2 --task-root /path/naver-issacsim-nvidia/training/quadruped \
  --checkpoint /path/model_7050.pt --output /path/eval-A \
  --suite scenario7 --num-envs 128 --seeds 4201,4202,4203

bash run_evaluation.sh --isaaclab-root /path/IsaacLab \
  --robot go2 --task-root /path/naver-issacsim-nvidia/training/quadruped \
  --checkpoint /path/model_2950.pt --output /path/eval-B \
  --suite scenario7 --num-envs 128 --seeds 4201,4202,4203
```

H1은 `--robot h1 --task-root /path/naver-issacsim-nvidia/training/humanoid`로 바꿉니다. TorchScript는 `--checkpoint` 대신 `--policy /path/policy.pt`를 지정합니다. 같은 파일을 한꺼번에 여러 GPU 프로세스로 실행하지 않습니다.

runner는 raw episode JSONL, 평가 manifest, 적용된 환경/agent 설정과 runtime 정보를 남깁니다. 실패·중단하면 raw 결과와 `complete=false`를 보존합니다. scenario/case/seed/env cohort가 누락되거나 평가 시간창이 짧으면 scorer가 점수를 거부합니다. checkpoint를 자동 탐색하거나 가장 좋아 보이는 모델을 선택하지 않습니다.

`evaluation_manifest.json`은 실행환경·정책 SHA·프로토콜을, `resolved_configs.json`은 적용된 전체 native 설정을, `episodes.jsonl`은 시나리오/seed/env별 모든 episode와 종료 사유·진단 수치를 담습니다. source와 runtime/config identity가 다른 결과를 같은 프로토콜이라고 비교하지 않습니다. GPU 없는 검증 범위와 실제 smoke에서 확인할 항목은 `VERIFICATION.md`를 참고하세요.

## 4. calibration과 비교

먼저 적절한 고정 reference 정책을 **동일 suite**로 평가합니다. 각 시나리오 reference episode-error의 중앙값을 초기 e50으로 만드는 명령입니다.

```bash
python eval_core.py calibrate --evaluation /path/eval-reference \
  --id go2-scenario7-reference-v1 --out /path/calibration.json
python eval_core.py score --evaluation /path/eval-A \
  --calibration /path/calibration.json --out /path/score-A.json
python eval_core.py compare --a /path/eval-A --b /path/eval-B \
  --calibration /path/calibration.json --out /path/comparison.json
```

초기 calibration은 `provisional`입니다. 실제 정책·negative control을 여러 개 확인하고 e50 값/방법/근거를 선택한 뒤 별도 버전의 calibration을 동결해 사용하세요(`status: frozen`). 후보마다 재calibration하지 않습니다. 새 suite/평가 길이를 쓰면 별도 calibration이 필요합니다. reference의 어떤 시나리오 오차 중앙값이 0이면 e50을 추측하지 않고 오류로 중단합니다.

같은 calibration을 사용한 정책 점수는 독립적으로 계산됩니다. A/B 비교에서는 calibration·suite·실행 프로토콜·cohort 집합이 같아야 합니다. episode ID 수는 정책의 낙상/reset에 따라 달라지므로 episode 한 개씩 억지로 짝짓지 않습니다. 같은 `(scenario, case, seed, env_id)` 블록을 함께 bootstrap하고 블록 안 모든 episode를 보존합니다. 동일 seed도 낙상 이후 완전히 동일한 trajectory를 보장하지 않습니다. seed가 3개 미만이면 해당 seed 안에서만 해석해야 한다는 경고를 출력합니다.

scorer의 `--out`은 새 `.json` 경로를 지정해야 합니다. JSON이나 같은 이름의 HTML이 이미 있으면 덮어쓰지 않습니다. native checkpoint와 task source는 신뢰할 수 있는 프로젝트 원본만 사용하세요. 특히 pickle 기반 native checkpoint는 임의의 외부 파일을 안전하게 읽는 포맷이 아닙니다.

## 결과를 읽는 기준

- 전체 점수와 95% CI에 더해 worst-scenario, worst-seed, Survival, 통합·축별 추종 오차를 확인합니다.
- 전진 변위·stall을 함께 봅니다. 역계단에서 100% 생존하지만 제자리인 정책을 traversal 성공으로 기록하지 않습니다.
- base-contact 실패·pitch/roll 흔들림·action delta를 별도 진단합니다. 이 진단을 몰래 점수에 곱하지 않습니다.
- `A_HIGHER`는 내부 점수 차이의 bootstrap 구간이 0보다 크다는 뜻입니다. 제출 승격, 공식 우위, reward 인과효과 확정은 아닙니다.
- raw reward 절댓값이나 native 영상 몇 장면을 fixed numeric 평가 점수로 섞지 않습니다.
- 공개 타 팀 실패 사례는 stall/비대칭 보행/진동 같은 진단 질문의 근거이며 점수 calibration anchor나 인과 label로 사용하지 않습니다.

초기 v1 제작 당시에는 전체 GPU 실행을 수행하지 않았습니다. 이후 Windows Go2 2950·7050 개별 full 평가는 기존 영상 receipt 재사용 경로에서 검증됐으며, 그 범위는 [Windows Go2 지침](WINDOWS_WORKFLOW.md)을 따릅니다. H1은 [Windows H1 지침](WINDOWS_H1_WORKFLOW.md)의 통합 source가 추가됐고, **2026-10-07 `model_2850` 한 건에 한하여** 기존 full 평가 기록(3,072/3,072 episode·exit 0)을 확인했습니다. 이외 checkpoint 호환, matched A/B·공식 점수 및 H1 전반적 신뢰도는 아직 주장하지 않습니다.
