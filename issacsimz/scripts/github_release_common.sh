#!/usr/bin/env bash
# Shared personal-only GitHub Release checks used by explicit publishers.

issacsimz_publish_die() {
  echo "[issacsimz] ERROR: $*" >&2
  exit 20
}

issacsimz_require_personal_github() {
  [[ "${ISSACSIMZ_MODE:-}" == "personal" ]] || issacsimz_publish_die "GitHub publishing is disabled outside personal mode"
  command -v gh >/dev/null || issacsimz_publish_die "gh is unavailable"
  gh auth status --hostname github.com >/dev/null || issacsimz_publish_die "GitHub CLI is not authenticated"
}

issacsimz_named_release() {
  local robot="$1" run_id="$2" kind="$3" experiment="$4" config="$5" day config_pattern preset_robot
  [[ "$robot" == h1 || "$robot" == go2 ]] || issacsimz_publish_die "invalid release robot: $robot"
  [[ "$experiment" =~ ^exp-${robot}-[a-z0-9]+(-[a-z0-9]+)*$ ]] ||
    issacsimz_publish_die "release experiment must be an exp-${robot}-... slug"
  preset_robot="$robot"
  [[ "$robot" != go2 ]] || preset_robot=g2
  config_pattern="^${preset_robot}-submit-[0-9]+( \\+ [a-z][a-z0-9]*=[-+]?[0-9]+(\\.[0-9]+)?)*$"
  [[ "$config" =~ $config_pattern ]] ||
    issacsimz_publish_die "release config must use ${preset_robot}-submit-N + key=value notation"
  [[ "$kind" == train || "$kind" == videos ]] || issacsimz_publish_die "invalid release kind: $kind"
  if [[ "$run_id" =~ ^([0-9]{8})- ]]; then day="${BASH_REMATCH[1]}"; else day="$(date -u +%Y%m%d)"; fi
  ISSACSIMZ_NAMED_TAG="private-${robot}-${day}-${experiment}-${run_id}"
  [[ "$kind" == train ]] || ISSACSIMZ_NAMED_TAG+="-videos"
  ISSACSIMZ_NAMED_TITLE="${robot^^} · ${experiment} · ${config} · PERSONAL ${kind} · ${run_id}"
}

issacsimz_require_new_release_tag() {
  local repo="$1" tag="$2"
  if gh release view "$tag" --repo "$repo" >/dev/null 2>&1; then
    issacsimz_publish_die "Release already exists; refusing overwrite: $tag"
  fi
}

issacsimz_prepare_annotated_tag() {
  local checkout="$1" repo="$2" tag="$3" title="$4"
  local origin commit remote_line remote_status local_object remote_object tagged_commit
  [[ -d "$checkout/.git" ]] || issacsimz_publish_die "personal repository checkout is missing: $checkout"
  git check-ref-format "refs/tags/$tag" || issacsimz_publish_die "invalid Release tag: $tag"
  origin="$(git -C "$checkout" remote get-url origin)" || issacsimz_publish_die "cannot read personal repository origin"
  case "$origin" in
    "https://github.com/$repo"|"https://github.com/$repo.git"|"git@github.com:$repo"|"git@github.com:$repo.git") ;;
    *) issacsimz_publish_die "personal repository origin does not match $repo" ;;
  esac
  commit="$(git -C "$checkout" rev-parse --verify 'HEAD^{commit}')" ||
    issacsimz_publish_die "cannot resolve personal checkout commit"
  [[ -n "$commit" ]] || issacsimz_publish_die "personal checkout commit is empty"
  set +e
  remote_line="$(git -C "$checkout" ls-remote --exit-code --tags origin "refs/tags/$tag")"
  remote_status=$?
  set -e
  [[ "$remote_status" == 0 || "$remote_status" == 2 ]] || issacsimz_publish_die "cannot check remote tag: $tag"
  if git -C "$checkout" show-ref --verify --quiet "refs/tags/$tag"; then
    [[ "$(git -C "$checkout" cat-file -t "refs/tags/$tag")" == tag ]] ||
      issacsimz_publish_die "existing local tag is not annotated: $tag"
  else
    [[ "$remote_status" == 2 ]] || issacsimz_publish_die "remote tag exists without matching local annotated tag: $tag"
    git -C "$checkout" tag -a -m "$title" -- "$tag" "$commit" || issacsimz_publish_die "cannot create annotated tag: $tag"
  fi
  tagged_commit="$(git -C "$checkout" rev-parse --verify "refs/tags/$tag^{commit}")" ||
    issacsimz_publish_die "cannot resolve annotated tag commit: $tag"
  [[ -n "$tagged_commit" ]] || issacsimz_publish_die "annotated tag commit is empty: $tag"
  [[ "$tagged_commit" == "$commit" ]] ||
    issacsimz_publish_die "annotated tag does not point to personal checkout commit: $tag"
  local_object="$(git -C "$checkout" rev-parse "refs/tags/$tag")" || issacsimz_publish_die "cannot resolve local tag: $tag"
  if [[ "$remote_status" == 0 ]]; then
    remote_object="${remote_line%%[[:space:]]*}"
    [[ "$remote_object" == "$local_object" ]] || issacsimz_publish_die "remote tag differs from local annotated tag: $tag"
  else
    git -C "$checkout" push origin "refs/tags/$tag:refs/tags/$tag" ||
      issacsimz_publish_die "cannot push annotated tag: $tag"
  fi
}

issacsimz_verify_remote_assets() {
  local repo="$1" tag="$2"
  shift 2
  local remote name size digest expected_size expected_digest
  remote="$(gh api "repos/$repo/releases/tags/$tag" --jq '.assets[] | [.name, .size, .digest] | @tsv')" ||
    issacsimz_publish_die "cannot read published Release assets"
  for asset in "$@"; do
    name="$(basename "$asset")"
    size=""
    digest=""
    while IFS=$'\t' read -r remote_name remote_size remote_digest; do
      if [[ "$remote_name" == "$name" ]]; then
        size="$remote_size"
        digest="$remote_digest"
        break
      fi
    done <<< "$remote"
    [[ -n "$size" ]] || issacsimz_publish_die "published asset is missing: $name"
    expected_size="$(stat -c '%s' "$asset")"
    expected_digest="sha256:$(sha256sum "$asset" | awk '{print $1}')"
    [[ "$size" == "$expected_size" ]] || issacsimz_publish_die "published asset size mismatch: $name"
    [[ "$digest" == "$expected_digest" ]] || issacsimz_publish_die "published asset digest mismatch: $name"
  done
}
