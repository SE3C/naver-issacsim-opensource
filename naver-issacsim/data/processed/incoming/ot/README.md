# 2026 온라인 설명회 자료 세트

이 폴더는 `NAVER CONNECT Robotics Cup 2026 온라인 설명회` 원본 영상에 대해 새로 정리된 전사·검증 자료를 보관한다. 원본 MP4는 분석 저장소에 복사하지 않고 `../naver-issacsim-originals/data/raw/external_analysis/`에 보존한다.

## 현재 자료

- [교정 전사](./transcripts/2026_ot_online_briefing_corrected_transcript.md): Whisper 전사, 자동 자막, 공식 용어를 교차검증해 고유명사·파일명·제품명 오인식만 교정한 전체 발화 전사
- [시간자막 SRT](./transcripts/2026_ot_online_briefing_corrected_captions.srt): 같은 전사의 시간자막 형식
- [저신뢰도 교차검증](./analyses/2026_ot_online_briefing_low_confidence_crosscheck.md): Whisper 평균 신뢰도 0.65 미만 구간과 자동 자막을 나란히 둔 검토 목록
- [오디오·영상 통합 분석](./analyses/2026_ot_online_briefing_audio_video_integrated_analysis.md): 영상 화면·전체 오디오·교정 전사·저신뢰도 교차검증을 합친 상세 통합 분석본
- [이전 synthesis 위치 안내](./synthesis/README.md): 통합 분석의 실제 위치를 안내한다.

## 사용 규칙

- 전체 전사는 현재 검토 후보이며, 시간·발화 확인에는 SRT를 함께 사용한다.
- 저신뢰도 목록의 자동 자막은 교차검증 재료일 뿐, 추측성 자동 치환의 근거로 사용하지 않는다.
- 최종 결론은 전사·원본 영상·공식 규정을 교차확인한다. 상세 통합 분석은 `analyses/`에 보존한다.
- AI 핵심팩에는 OT 전용 파일이 없다. 실행 판단은 `05`(실험 루프), `11`(서버 운영), `12`(규정)에 녹여 두었다. 핵심팩의 현행 구성은 [업로드 가이드](../../../../docs/AI_LIBRARY_GUIDE.md)를 따른다(`00`~`08`, `10`~`21`, 전체 21개).
