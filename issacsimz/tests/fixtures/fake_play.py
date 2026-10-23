from __future__ import annotations

import os
import sys
from pathlib import Path


exported = Path.cwd() / "exported"
exported.mkdir(parents=True, exist_ok=True)
required = {"--video", "--video_length", "--enable_cameras"}
if not required.issubset(set(sys.argv)):
    raise SystemExit("missing official video options")
if sys.argv[sys.argv.index("--video_length") + 1] != "1000":
    raise SystemExit("unexpected video length")
if os.environ.get("ISSACSIMZ_PLAY_SCENARIO") != "stale":
    checkpoint = Path(sys.argv[sys.argv.index("--checkpoint") + 1])
    video = checkpoint.parent / "videos" / "play" / "play_video.mp4"
    video.parent.mkdir(parents=True, exist_ok=True)
    video.write_bytes(b"video-current")
    policy = checkpoint.parent / "exported" / "policy.pt"
    policy.parent.mkdir(parents=True, exist_ok=True)
    policy.write_bytes(b"policy-current")
    (exported / "play_args.txt").write_text("\n".join(sys.argv[1:]), encoding="utf-8")
print("[fixture] play", flush=True)
