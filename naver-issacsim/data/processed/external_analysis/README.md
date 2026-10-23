# 외부 분석 요청

`video_analysis_requests.jsonl`의 각 행을 영상 분석 전문 AI에 전달합니다.
결과는 같은 `requestId`를 유지한 JSONL로 받아야 강의 문서와 다시 결합할 수 있습니다.

필수 결과 필드: `requestId`, `summary`, `timestamped_scenes`, `technical_concepts`,
`visible_code_or_commands`, `procedures`, `warnings`.

`image_analysis_requests.jsonl`은 강의 이미지 분석 요청입니다. `localSource`가 있는 파일을
이미지 분석 전문 AI에 전달하고 같은 `requestId`로 결과를 받습니다.
`status`가 `missing_source_file`인 항목은 실제 파일이 없으므로 분석 대상에서 제외합니다.

사용자가 제공한 Markdown 기반 영상 분석 보고서는 [`video_reports/README.md`](./video_reports/README.md)에 별도 보관합니다.
이 보고서는 분석 자료이므로 최신 공식 규정·공지보다 우선하지 않습니다.

운영진 오늘의 🍯TIP은 [주제별 색인·전달 원문](./2026-09-23_ORGANIZER_DAILY_HONEY_TIPS_SOURCE_AND_NOTES.md#주제별-찾아보기)에서 찾습니다. 번호·날짜는 사용자 전달 Discord 발췌 기준이며, 게시물 전체·첨부 이미지를 독립 확인한 자료는 아닙니다. 원문을 AI 문서에 중복 복제하지 않고 필요한 진단 요약만 연결합니다.
