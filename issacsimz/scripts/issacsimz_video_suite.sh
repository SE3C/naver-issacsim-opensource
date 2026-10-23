#!/usr/bin/env bash
# Render six profile-specific terrain views through the existing video wrapper.
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE="${ISSACSIMZ_STATE_FILE:-$ROOT/.issacsimz-mode.env}"
[[ -f "$STATE" ]] || { echo "[issacsimz] ERROR: bootstrap first" >&2; exit 2; }
source "$STATE"

if [[ "${ISSACSIMZ_MODE:-}" != "personal" ]]; then
  echo "[issacsimz] ERROR: video suite is available only in personal mode" >&2
  exit 2
fi

[[ $# -ge 3 && ( "$1" == "go2" || "$1" == "h1" ) && ( "$2" == "--from-run" || "$2" == "--checkpoint" ) && -n "$3" ]] || {
  echo "[issacsimz] ERROR: usage: $0 h1|go2 (--from-run RUN_ID | --checkpoint PATH) [--release-experiment SLUG --release-config DISPLAY | --no-publish | --publish --tag TAG --title TITLE --notes-file FILE [--repo OWNER/REPO]]" >&2
  exit 2
}
ROBOT="$1"
SOURCE_KIND="$2"
SOURCE_VALUE="$3"
shift 3
PUBLISH_MODE="auto"
PUBLISH_TAG=""
PUBLISH_TITLE=""
PUBLISH_NOTES_FILE=""
PUBLISH_REPO=""
RELEASE_EXPERIMENT=""
RELEASE_CONFIG=""
while (( $# )); do
  case "$1" in
    --publish) [[ "$PUBLISH_MODE" != "off" ]] || { echo "[issacsimz] ERROR: --publish conflicts with --no-publish" >&2; exit 2; }; PUBLISH_MODE="custom"; shift ;;
    --no-publish) [[ "$PUBLISH_MODE" != "custom" ]] || { echo "[issacsimz] ERROR: --no-publish conflicts with --publish" >&2; exit 2; }; PUBLISH_MODE="off"; shift ;;
    --tag) [[ $# -ge 2 ]] || { echo "[issacsimz] ERROR: --tag requires a value" >&2; exit 2; }; PUBLISH_TAG="$2"; shift 2 ;;
    --title) [[ $# -ge 2 ]] || { echo "[issacsimz] ERROR: --title requires a value" >&2; exit 2; }; PUBLISH_TITLE="$2"; shift 2 ;;
    --notes-file) [[ $# -ge 2 ]] || { echo "[issacsimz] ERROR: --notes-file requires a value" >&2; exit 2; }; PUBLISH_NOTES_FILE="$2"; shift 2 ;;
    --repo) [[ $# -ge 2 ]] || { echo "[issacsimz] ERROR: --repo requires a value" >&2; exit 2; }; PUBLISH_REPO="$2"; shift 2 ;;
    --release-experiment) [[ $# -ge 2 ]] || { echo "[issacsimz] ERROR: --release-experiment requires a value" >&2; exit 2; }; RELEASE_EXPERIMENT="$2"; shift 2 ;;
    --release-config) [[ $# -ge 2 ]] || { echo "[issacsimz] ERROR: --release-config requires a value" >&2; exit 2; }; RELEASE_CONFIG="$2"; shift 2 ;;
    *) echo "[issacsimz] ERROR: unknown video suite option: $1" >&2; exit 2 ;;
  esac
done
if [[ "$PUBLISH_MODE" == "custom" ]]; then
  [[ -n "$PUBLISH_TAG" && -n "$PUBLISH_TITLE" && -f "$PUBLISH_NOTES_FILE" ]] || {
    echo "[issacsimz] ERROR: --publish requires --tag, --title, and an existing --notes-file" >&2
    exit 2
  }
elif [[ -n "$PUBLISH_TAG$PUBLISH_TITLE$PUBLISH_NOTES_FILE$PUBLISH_REPO" ]]; then
  echo "[issacsimz] ERROR: Release options require --publish" >&2
  exit 2
fi
if [[ -n "$RELEASE_EXPERIMENT$RELEASE_CONFIG" ]]; then
  [[ "$PUBLISH_MODE" == auto && -n "$RELEASE_EXPERIMENT" && -n "$RELEASE_CONFIG" ]] || {
    echo "[issacsimz] ERROR: release naming requires auto publish and both --release-experiment/--release-config" >&2
    exit 2
  }
  source "$ROOT/scripts/github_release_common.sh"
  issacsimz_named_release "$ROBOT" preview videos "$RELEASE_EXPERIMENT" "$RELEASE_CONFIG"
fi
source "$ROOT/scripts/python_runner.sh"
LAB_ROOT="${ISSACSIMZ_ISAACLAB_ROOT:?IsaacLab path missing; re-run bootstrap}"
PYTHON_RUNNER="$(issacsimz_find_python_runner "$LAB_ROOT")" || exit 2
EVIDENCE_ROOT="${ISSACSIMZ_EVIDENCE_ROOT:?evidence root missing; re-run bootstrap}"
SUITE_STARTED_UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
if [[ "$SOURCE_KIND" == "--from-run" ]]; then
  RUN_ID="$SOURCE_VALUE"
  CHECKPOINT="$EVIDENCE_ROOT/runs/$RUN_ID/collected/exported/model_best.pt"
  [[ -f "$CHECKPOINT" ]] || { echo "[issacsimz] ERROR: checkpoint not found in train evidence: $RUN_ID" >&2; exit 2; }
  CHECKPOINT_SHA="$(sha256sum "$CHECKPOINT" | awk '{print $1}')"
else
  CHECKPOINT="$(cd "$(dirname "$SOURCE_VALUE")" && pwd)/$(basename "$SOURCE_VALUE")"
  [[ -f "$CHECKPOINT" ]] || { echo "[issacsimz] ERROR: checkpoint not found: $SOURCE_VALUE" >&2; exit 2; }
  CHECKPOINT_SHA="$(sha256sum "$CHECKPOINT" | awk '{print $1}')"
  [[ "$CHECKPOINT_SHA" =~ ^[0-9a-fA-F]{64}$ ]] || { echo "[issacsimz] ERROR: cannot hash checkpoint: $CHECKPOINT" >&2; exit 2; }
  CHECKPOINT_STEM="${CHECKPOINT##*/}"
  CHECKPOINT_STEM="${CHECKPOINT_STEM%.pt}"
  CHECKPOINT_STEM="$(printf '%s' "$CHECKPOINT_STEM" | tr -cs 'A-Za-z0-9._-' '-')"
  RUN_ID="checkpoint-${ROBOT}-${CHECKPOINT_STEM}-${CHECKPOINT_SHA:0:12}"
  if [[ "$ROBOT" == "h1" ]]; then TASK_ROOT="${ISSACSIMZ_H1_ROOT:?H1 task root missing; re-run bootstrap}"
  else TASK_ROOT="${ISSACSIMZ_GO2_ROOT:?Go2 task root missing; re-run bootstrap}"; fi
  export ISSACSIMZ_MODE
  [[ -z "${ISSACSIMZ_DOWNLOAD_ROOT:-}" ]] || export ISSACSIMZ_DOWNLOAD_ROOT
  echo "[issacsimz] video_suite checkpoint=$CHECKPOINT handoff_run=$RUN_ID"
fi
[[ "$CHECKPOINT_SHA" =~ ^[0-9a-fA-F]{64}$ ]] || { echo "[issacsimz] ERROR: cannot hash checkpoint: $CHECKPOINT" >&2; exit 2; }
if [[ "$ROBOT" == "go2" ]]; then
  SLOPE=0.363970234
  DEG=20
else
  SLOPE=0.176326981
  DEG=10
fi
LABELS=(stairs inverted_stairs boxes random_rough "slope_up_${DEG}deg" "slope_down_${DEG}deg")
TERRAINS=(pyramid_stairs pyramid_stairs_inv boxes random_rough hf_pyramid_slope hf_pyramid_slope_inv)

for index in "${!LABELS[@]}"; do
  label="${LABELS[$index]}"
  selected="${TERRAINS[$index]}"
  overrides=(
    env.scene.terrain.terrain_generator.num_rows=1
    env.scene.terrain.terrain_generator.num_cols=1
    env.scene.terrain.terrain_generator.horizontal_scale=0.05
  )
  for terrain in "${TERRAINS[@]}"; do
    value=0.0
    [[ "$terrain" == "$selected" ]] && value=1.0
    overrides+=("env.scene.terrain.terrain_generator.sub_terrains.${terrain}.proportion=${value}")
  done
  if [[ "$selected" == "hf_pyramid_slope" || "$selected" == "hf_pyramid_slope_inv" ]]; then
    overrides+=("env.scene.terrain.terrain_generator.sub_terrains.${selected}.slope_range=[${SLOPE},${SLOPE}]")
  fi
  echo "[issacsimz] video_suite=$label terrain=$selected"
  set +e
  if [[ "$SOURCE_KIND" == "--from-run" ]]; then
    ISSACSIMZ_DISABLE_PUBLISH=1 bash "$ROOT/scripts/issacsimz_video.sh" "$ROBOT" --from-run "$RUN_ID" --label "$label" \
      --extra --video --video_length 1000 --enable_cameras "${overrides[@]}"
  else
    "$PYTHON_RUNNER" "$ISSACSIMZ_PYZ" play "$ROBOT" \
      --name "${RUN_ID}-${label}" --checkpoint "$CHECKPOINT" \
      --video-label "$label" --handoff-run-id "$RUN_ID" \
      --log-root "$ISSACSIMZ_EVIDENCE_ROOT" --task-root "$TASK_ROOT" --isaaclab-root "$LAB_ROOT" \
      --num-envs 1 --extra --video --video_length 1000 --enable_cameras "${overrides[@]}"
  fi
  code=$?
  set -e
  if (( code != 0 )); then
    echo "[issacsimz] ERROR: video suite stopped at $label (exit=$code)" >&2
    exit "$code"
  fi
done

if [[ -n "${ISSACSIMZ_DOWNLOAD_ROOT:-}" ]]; then
  DOWNLOAD_ROOT="$ISSACSIMZ_DOWNLOAD_ROOT"
else
  DOWNLOAD_ROOT="/home/shadeform/ISSACSIMZ_DOWNLOAD"
fi
for label in "${LABELS[@]}"; do
  [[ -s "$DOWNLOAD_ROOT/$RUN_ID/videos/$label.mp4" ]] || {
    echo "[issacsimz] ERROR: missing suite video: $label" >&2
    exit 1
  }
done
HANDOFF="$DOWNLOAD_ROOT/$RUN_ID"
"$PYTHON_RUNNER" "$ROOT/scripts/video_suite_artifacts.py" finalize \
  --robot "$ROBOT" --run-id "$RUN_ID" --checkpoint "$CHECKPOINT" \
  --checkpoint-sha "$CHECKPOINT_SHA" --handoff "$HANDOFF" \
  --evidence-root "$EVIDENCE_ROOT" --started-utc "$SUITE_STARTED_UTC"

BUNDLE="$DOWNLOAD_ROOT/$RUN_ID-download.tar.gz"
SIDECAR="$BUNDLE.sha256"
TMP_BUNDLE="$DOWNLOAD_ROOT/.$RUN_ID-download.tar.gz.tmp"
TMP_SIDECAR="$DOWNLOAD_ROOT/.$RUN_ID-download.tar.gz.sha256.tmp"
rm -f -- "$TMP_BUNDLE" "$TMP_SIDECAR"
tar -C "$DOWNLOAD_ROOT" -czf "$TMP_BUNDLE" "$RUN_ID"
printf '%s  %s\n' "$(sha256sum "$TMP_BUNDLE" | awk '{print $1}')" "$(basename "$BUNDLE")" > "$TMP_SIDECAR"
mv -f -- "$TMP_BUNDLE" "$BUNDLE"
mv -f -- "$TMP_SIDECAR" "$SIDECAR"
"$PYTHON_RUNNER" "$ROOT/scripts/video_suite_artifacts.py" verify \
  --suite-dir "$HANDOFF" --archive "$BUNDLE" --archive-sidecar "$SIDECAR"
if [[ "$PUBLISH_MODE" != "off" ]]; then
  if [[ "$PUBLISH_MODE" == "custom" ]]; then
    PUBLISH_ARGS=(--suite-dir "$HANDOFF" --tag "$PUBLISH_TAG" --title "$PUBLISH_TITLE" --notes-file "$PUBLISH_NOTES_FILE")
  else
    PUBLISH_TAG="private-${RUN_ID}-videos"
    PUBLISH_TITLE="$PUBLISH_TAG"
    PUBLISH_NOTES="Personal NVIDIA/Brev six-terrain video suite. Checkpoint: $(basename "$CHECKPOINT"); SHA-256: $CHECKPOINT_SHA. Preserve canonical evidence separately."
    if [[ -n "$RELEASE_EXPERIMENT" ]]; then
      issacsimz_named_release "$ROBOT" "$RUN_ID" videos "$RELEASE_EXPERIMENT" "$RELEASE_CONFIG"
      PUBLISH_TAG="$ISSACSIMZ_NAMED_TAG"; PUBLISH_TITLE="$ISSACSIMZ_NAMED_TITLE"
      PUBLISH_NOTES="Personal NVIDIA/Brev six-terrain video suite. Experiment: $RELEASE_EXPERIMENT. Final config display: $RELEASE_CONFIG. Suite handoff: $RUN_ID. Checkpoint: $(basename "$CHECKPOINT"); SHA-256: $CHECKPOINT_SHA. Preserve canonical evidence separately."
    fi
    PUBLISH_ARGS=(--suite-dir "$HANDOFF" --tag "$PUBLISH_TAG" --title "$PUBLISH_TITLE" --notes "$PUBLISH_NOTES")
  fi
  [[ -z "$PUBLISH_REPO" ]] || PUBLISH_ARGS+=(--repo "$PUBLISH_REPO")
  bash "$ROOT/scripts/publish_video_suite_release.sh" "${PUBLISH_ARGS[@]}"
fi
echo "[issacsimz] video_suite=COMPLETE run=$RUN_ID download=$DOWNLOAD_ROOT"
