---
title: NCRC v1 implementation and limits (historical)
reviewed_at: '2026-09-12'
status: superseded_by_issacsimz
---

> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/planning/historical/09_NCRC_V1_IMPLEMENTATION_AND_LIMITS.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.


# Historical NCRC v1 record

This document preserves the planning record for the former NVIDIA-internal
`ncrc` orchestration implementation. It is not the current operational guide.

The current split is:

- `naver-issacsim-nvidia`: private NVIDIA environment and H1/Go2 task source.
- public Codeberg `issacsimz`: portable external sidecar for command logging,
  checkpoint mirroring, provenance, validation and archive creation.
- `naver-issacsim`: analysis, evidence interpretation and AI library.

`issacsimz` must not edit official or private `train.py`, `play.py`,
`_finalize.py`, Isaac Lab or RSL-RL. Its hardened v1.1 behavior is documented
in AI library `19`: first Ctrl+C waits for native finalize/backup, source
identity is captured before and after a run, evidence validation is explicit,
and path/disk safety checks protect archives.

Local unit and portable-build verification has passed. Personal NVIDIA and
official-server smoke tests remain operator-run validation; they are not
claimed completed by this historical document.
