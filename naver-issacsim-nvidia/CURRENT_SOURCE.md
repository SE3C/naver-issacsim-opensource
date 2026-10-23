# Current H1 / Go2 source

For a new PERSONAL run, the executable task source is this checkout's tracked `training/` tree at the run's recorded NVIDIA commit. For an OFFICIAL run, the executable source is the organizer-provided `/workspace/training` on that server; verify it from that run's evidence. Neither a processed analysis copy nor a Release title establishes the code that actually ran.

The preserved 2026-09-13 official snapshot is `naver-issacsim-originals/data/raw/server_backup/extracted/training/`. On 2026-09-25, the NVIDIA `training/` tree at `75123c724a12` was compared with that extracted tree: tracked task/source content matched; the only directory difference was a generated `__pycache__/train.cpython-313.pyc` file in the preserved tree. This is a comparison at those revisions, not a perpetual equality guarantee.

`naver-issacsim/data/processed/server_backup/code/training/` is a historical, readable analysis copy, not the execution source. Personal bootstrap and publishing helpers live outside `training/` and do not make PERSONAL results OFFICIAL.
