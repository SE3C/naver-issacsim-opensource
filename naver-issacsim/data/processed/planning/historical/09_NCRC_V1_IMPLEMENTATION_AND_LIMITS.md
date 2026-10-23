---
title: NCRC v1 implementation and limits (historical)
reviewed_at: '2026-09-12'
status: superseded_by_issacsimz
---

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
