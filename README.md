# NCRC 프로젝트 공개 보관본

기존 프로젝트의 저장소 이름과 내부 폴더 구조를 유지한 선별 공개 snapshot입니다. 파일의 제목·본문·수치·Run ID·파일명·링크는 원본 그대로 두며, 필요한 개인정보만 블라인드합니다. 공개하기 곤란한 파일은 내용을 재작성하지 않고 파일 단위로 제외합니다.

```text
naver-issacsim-opensource/
├─ naver-issacsim/            # 분석·문서·실험 registry
├─ naver-issacsim-originals/  # 선별한 원본 보존·결과 메타데이터
├─ naver-issacsim-nvidia/     # 자체 서버 도구·운영 문서
├─ naver-issacsim-eval/       # 자체 평가기·실행기·문서
├─ issacsimz/                # 실행·evidence sidecar
└─ _publication/             # 공개 범위·블라인드·제외·Release 색인
```

- [공개 범위와 원본 보존 원칙](_publication/README.md)
- [파일별 출처·원본/공개 SHA](_publication/FILES.json)
- [파일 단위 제외 목록](_publication/EXCLUDED.json)
- [원래 실험 단위의 Release 색인](_publication/RELEASES.md)
- [검증·변경 기록](_publication/VERIFICATION.md)

각 폴더의 README는 원래 저장소의 설명을 그대로 보존한 것입니다. **원래 5개 저장소의 전체 복제는 아닙니다.** 공식 training·강의·실습, 운영진 대화 원문, 모델·제출 정책·전체 학습 archive 등 제외 대상은 포함하지 않습니다. 원문 링크나 코드가 참조하는 외부 task·누락 자료를 이 snapshot만으로 제공하거나 재현한다고 주장하지 않습니다.

기존 비공개 저장소의 Git 이력·Release·원본 자료는 변경하지 않습니다. 공개용 Release도 원본 실험 단위·제목·설명·asset 파일명을 보존하며, 한 저장소 안에서 구분하기 위한 `eval--`·`analysis--` tag 접두어만 추가합니다. 기술 보고서만 선별한 Release에는 policy·env·전체 제출 snapshot을 넣지 않습니다. 이전 두 묶음 Release는 과거 공개 snapshot으로 남습니다.

**라이선스는 아직 미정입니다.** 공개 열람과 포괄적 재사용 허가는 구분합니다. GPU 작업·학습·영상·서버 종료는 이 공개 작업에서 실행하지 않았습니다.
