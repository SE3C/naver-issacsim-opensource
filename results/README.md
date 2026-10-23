# 자체 평가 데이터·영상

[공개 평가 snapshot Release](https://github.com/SE3C/naver-issacsim-opensource/releases/tag/public-evaluation-snapshot-20261023)에서 공개용 평가 ZIP을 받습니다. 파일별 크기·SHA-256과 원본 asset SHA는 [PUBLIC_RESULTS_MANIFEST.json](PUBLIC_RESULTS_MANIFEST.json)에 있습니다. 원본 ZIP은 별도로 보존합니다.

## 포함·변환 범위

- 자체 evaluator의 episode JSONL, 진단·평가 manifest와 해당 ZIP에 원래 들어 있던 MP4를 선별합니다. 영상 없는 정량 평가를 6영상 완료로 간주하지 않습니다.
- MP4와 episode JSONL은 원본과 **바이트 동일**하게 보존합니다. JSON의 숫자·체크포인트 SHA·Run ID·null·실패 상태를 교정하거나 승격하지 않습니다.
- 사용자 프로필 경로만 `C:/Users/<USER>`로 일반화하고 런타임 `.log`는 제외합니다. 환경별 일반 task 경로는 출처 맥락으로 남을 수 있으며 그대로 실행하라는 뜻이 아닙니다.
- 각 ZIP의 `PUBLICATION.json`은 원본 asset SHA와 멤버별 원본/공개 SHA·제외 이유를 기록합니다. `PUBLIC_SHA256SUMS.txt`는 새 공개 사본 기준입니다. 원본 checksum 파일은 새 체크섬으로 대체하며, 원본 archive checksum이 새 ZIP에도 일치한다고 주장하지 않습니다.

## 해석 경계

공식 채점기가 아니며 공식 점수의 예측·동일성을 보장하지 않습니다. Windows와 Linux, seed 수·평가 버전이 다른 결과를 무조건 같은 cohort로 합치지 않습니다. `source_run_id=null`, unverified parent, launcher 실패 등 원시 상태는 그대로입니다. 파일이 완성됐다는 사실은 정책 우위나 제출 채택을 뜻하지 않습니다.

역사적 영상에는 검정/정상 프레임 교대 등 알려진 capture artifact가 있을 수 있습니다. 공개를 위해 재렌더하거나 프레임을 고치지 않았으며, 영상 존재만으로 지형 완주를 입증하지 않습니다. 대응 보고서의 한계를 함께 읽어야 합니다.

학습 checkpoint·정책 파일·공식 training 소스·운영진 대화 원문은 이 Release에 포함하지 않습니다. 새 GPU 평가를 실행하지 않았습니다.
