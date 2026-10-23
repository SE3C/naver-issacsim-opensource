> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim-nvidia/docs/RESULT_UPLOAD_PROTOCOL.md` (`91b32f6fc0bc`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# Result preservation protocol

This private source repository does not define a scheduled upload or deletion
job. In particular, `brev_nightly_backup_delete.sh` is not part of this
checkout and must not be treated as a current procedure.

For a new H1 or Go2 run, keep the task source and finalizer unchanged and run
the public `issacsimz` sidecar from outside this repository. It records the
command, console, newly created native run files, source identity, and an
evidence archive. Personal mode also records periodic GPU telemetry and mirrors
numbered checkpoints. Official mode keeps only one-shot GPU snapshots and does
not start the generic checkpoint mirror. The sidecar never moves or deletes
native files.

If the user explicitly requests server shutdown, first confirm that the
canonical sidecar archive and its `.sha256` file are preserved. Finishing a run
or a download does not itself authorize shutdown. Current `issacsimz` also
makes a finder-friendly copy at
`/home/shadeform/ISSACSIMZ_DOWNLOAD/<RUN_ID>/` in personal mode or
`/workspace/ISSACSIMZ_DOWNLOAD/<RUN_ID>/` in official mode;
`ISSACSIMZ_DOWNLOAD_ROOT` overrides only this handoff root. The archive keeps
its name, so the matching `.sha256` and `.metadata.json` sidecars are copied;
the handoff does not rename the archive or regenerate its checksum. A train
with PASS/WARN validation may also copy available `model_best.pt`, `env.yaml`,
and `report.html`. On FAIL it preserves the evidence archive and sidecars but
does not distribute submission-like loose artifacts. A successful linked video
may add `play_video.mp4`. The folder also has a sibling `-download.tar.gz`
bundle and its own checksum. None of these copies move or delete canonical
files. Also retain any native official
backup/report produced by the task finalizer. The handoff is a convenience
copy, not a replacement for evidence, an official submission, or server-side
backup.

Do not label an exported policy or video as belonging to a run unless its
provenance record marks it `NEW` or `MODIFIED` for that run. The sidecar avoids
copying unchanged stale exports, but the native run, checkpoint and rendered
video still need to be checked together before making a result claim.
