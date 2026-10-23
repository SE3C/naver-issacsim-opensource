> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/docs/EXTERNAL_ANALYSIS.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# 외부 미디어 분석 전달 절차

## 영상 분석 요청

`data/processed/external_analysis/video_analysis_requests.jsonl`을 영상 분석 전문 AI에 전달하고 아래처럼 요청한다.

> 각 JSONL 행의 YouTube 영상을 분석해 주세요. 원래 `requestId`를 유지하고, 결과를 JSONL 한 줄씩 반환해 주세요. 필드는 `requestId`, `summary`, `timestamped_scenes`, `technical_concepts`, `visible_code_or_commands`, `procedures`, `warnings`입니다. 영상에서 확인되지 않은 내용은 추측하지 말고 `null` 또는 빈 배열로 남겨 주세요.

## 이미지 분석 요청

`image_analysis_requests.jsonl`에서 `status=pending_external_analysis`인 행만 고르고, 각 `localSource` 파일과 함께 이미지 분석 전문 AI에 전달한다.

> 각 이미지와 요청 JSON을 분석해 주세요. 원래 `requestId`를 유지하고, 결과를 JSONL 한 줄씩 반환해 주세요. 필드는 `requestId`, `visual_summary`, `visible_text`, `ui_steps_or_controls`, `code_or_commands`, `diagram_relationships`, `warnings`입니다. 이미지에서 판독할 수 없는 내용은 추측하지 마세요.

## 결과 저장 위치

- 영상 결과: `data/processed/external_analysis/video_analysis_results.jsonl`
- 이미지 결과: `data/processed/external_analysis/image_analysis_results.jsonl`

결과 파일이 생기면 통합 생성기를 확장해 원래 강의 `documentId`와 결합한다.
