from __future__ import annotations

import os
import json
import hashlib
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEST_PYTHON_RUNNER = os.environ.get("ISSACSIMZ_PYTHON_RUNNER") or sys.executable


def public_tree_files(root: Path) -> list[str]:
    if (root / ".git").is_dir():
        result = subprocess.run(
            ["git", "ls-files", "-co", "--exclude-standard"], cwd=root,
            text=True, capture_output=True, check=True,
        )
        return result.stdout.splitlines()
    excluded = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", "dist"}
    files: list[str] = []
    for directory, names, filenames in os.walk(root):
        names[:] = [name for name in names if name not in excluded]
        parent = Path(directory)
        for name in filenames:
            if name.endswith((".pyc", ".pyo")):
                continue
            files.append((parent / name).relative_to(root).as_posix())
    return sorted(files)


def assert_public_tree_clean(root: Path) -> None:
    reserved = bytes((110, 99, 114, 99)).decode("ascii")
    for relative in public_tree_files(root):
        if reserved in relative.lower():
            raise AssertionError(relative)
        path = root / relative
        if not path.is_file():
            continue
        raw = path.read_bytes()
        if b"\0" not in raw and reserved in raw.decode("utf-8").lower():
            raise AssertionError(relative)


class PublicTreeDiscoveryTests(unittest.TestCase):
    def test_portable_launcher_uses_lf_line_endings(self) -> None:
        # A Git ZIP can otherwise export this extensionless bash launcher as CRLF.
        launcher = (ROOT / "issacsimz").read_bytes()
        self.assertTrue(launcher.startswith(b"#!/usr/bin/env bash\n"))
        self.assertNotIn(b"\r\n", launcher)

    def test_git_checkout_public_tree_is_clean(self) -> None:
        assert_public_tree_clean(ROOT)

    def test_zip_style_fallback_detects_forbidden_file(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "package").mkdir()
            (root / "package" / "safe.py").write_text("safe = True\n", encoding="utf-8")
            (root / "__pycache__").mkdir()
            (root / "__pycache__" / "ignored.pyc").write_bytes(b"ignored")
            assert_public_tree_clean(root)
            reserved = bytes((110, 99, 114, 99)).decode("ascii")
            (root / f"{reserved}-marker.txt").write_text("fixture\n", encoding="utf-8")
            with self.assertRaises(AssertionError):
                assert_public_tree_clean(root)


@unittest.skipIf(os.name == "nt", "Linux/WSL shell fixtures")
class IssacsimzOrchestrationTests(unittest.TestCase):
    def stub(self, folder: Path, name: str, body: str) -> None:
        path = folder / name
        path.write_text("#!/usr/bin/env bash\nset -eu\n" + body, encoding="utf-8")
        path.chmod(0o755)

    def _clean_env(self, **updates: str) -> dict[str, str]:
        """Isolate fake Python fixtures from a bootstrap-exported runner."""
        env = {**os.environ, **updates}
        env.pop("ISSACSIMZ_PYTHON_RUNNER", None)
        return env

    def suite_runner(self, folder: Path, *, evidence: Path, download: Path,
                     calls: Path, fail_at: int = 0) -> None:
        real_python = TEST_PYTHON_RUNNER
        helper = ROOT / "scripts" / "video_suite_artifacts.py"
        self.stub(folder, "python3", f'''if [[ "${{1:-}}" == "{helper}" ]]; then exec "{real_python}" "$@"; fi
printf "%s\\n" "$*" >> "{calls}"
count="$(wc -l < "{calls}")"
if (( {fail_at} > 0 && count == {fail_at} )); then exit 7; fi
run=""; label=""; checkpoint=""; robot=""
while (( $# )); do
  case "$1" in
    h1|go2) robot="$1"; shift;;
    --from-run) run="$2"; checkpoint="{evidence}/runs/$2/collected/exported/model_best.pt"; shift 2;;
    --handoff-run-id) run="$2"; shift 2;;
    --label|--video-label) label="$2"; shift 2;;
    --checkpoint) checkpoint="$2"; shift 2;;
    *) shift;;
  esac
done
sha="$(sha256sum "$checkpoint" | awk '{{print $1}}')"
evidence_id="video-$label"
mkdir -p "{download}/$run/videos" "{evidence}/runs/$evidence_id/collected/exported"
printf 'video-%s' "$label" > "{download}/$run/videos/$label.mp4"
cp "{download}/$run/videos/$label.mp4" "{evidence}/runs/$evidence_id/collected/exported/play_video.mp4"
printf '{{"operation":"video","profile":"%s","video_label":"%s","parent_run_id":"%s","source_checkpoint_sha256":"%s","start_utc":"2099-01-01T00:00:00Z"}}\\n' "$robot" "$label" "$run" "$sha" > "{evidence}/runs/$evidence_id/metadata.json"
printf '{{"overall":"PASS"}}\\n' > "{evidence}/runs/$evidence_id/validation.json"
''')

    def make_suite(self, base: Path, robot: str = "go2") -> tuple[Path, Path, Path, list[Path]]:
        labels = (
            "stairs", "inverted_stairs", "boxes", "random_rough",
            "slope_up_20deg", "slope_down_20deg",
        ) if robot == "go2" else (
            "stairs", "inverted_stairs", "boxes", "random_rough",
            "slope_up_10deg", "slope_down_10deg",
        )
        terrains = ("pyramid_stairs", "pyramid_stairs_inv", "boxes", "random_rough", "hf_pyramid_slope", "hf_pyramid_slope_inv")
        suite = base / "suite-run"
        (suite / "videos").mkdir(parents=True)
        checkpoint_sha = hashlib.sha256(b"checkpoint").hexdigest()
        entries = []
        videos = []
        for index, (label, terrain) in enumerate(zip(labels, terrains), 1):
            video = suite / "videos" / f"{label}.mp4"
            video.write_bytes(f"video-{index}".encode())
            digest = hashlib.sha256(video.read_bytes()).hexdigest()
            videos.append(video)
            entries.append({
                "label": label, "terrain": terrain, "mp4": f"videos/{label}.mp4",
                "mp4_sha256": digest, "video_evidence_id": f"evidence-{index}",
                "source_checkpoint_sha256": checkpoint_sha,
            })
        manifest = suite / "video_suite_manifest.json"
        manifest.write_text(json.dumps({
            "schema_version": 1, "suite_run_id": suite.name, "robot": robot,
            "checkpoint_filename": "model_2998.pt", "checkpoint_sha256": checkpoint_sha,
            "generated_at_utc": "2026-09-21T00:00:00+00:00", "terrains": entries,
        }, indent=2) + "\n", encoding="utf-8")
        checksum = suite / "SHA256SUMS"
        checksum.write_text("".join(
            f"{hashlib.sha256(path.read_bytes()).hexdigest()}  videos/{path.name}\n" for path in videos
        ) + f"{hashlib.sha256(manifest.read_bytes()).hexdigest()}  video_suite_manifest.json\n", encoding="utf-8")
        archive = base / f"{suite.name}-download.tar.gz"
        with tarfile.open(archive, "w:gz") as bundle:
            bundle.add(suite, arcname=suite.name)
        sidecar = Path(f"{archive}.sha256")
        sidecar.write_text(f"{hashlib.sha256(archive.read_bytes()).hexdigest()}  {archive.name}\n", encoding="utf-8")
        return suite, archive, sidecar, videos + [manifest, checksum, archive, sidecar]


    def test_python_runner_falls_back_to_isaac_python(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw)
            bin_dir, lab_root = base / "bin", base / "IsaacLab"
            bin_dir.mkdir()
            isaac_python = lab_root / "_isaac_sim" / "python.sh"
            isaac_python.parent.mkdir(parents=True)
            isaac_python.write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
            isaac_python.chmod(0o755)
            env = self._clean_env(PATH=str(bin_dir))
            result = subprocess.run(
                ["/bin/bash", "-c", 'source "$1"; issacsimz_find_python_runner "$2"', "fixture", str(ROOT / "scripts" / "python_runner.sh"), str(lab_root)],
                cwd=ROOT, env=env, text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), str(isaac_python))

    def test_public_tree_omits_reserved_project_keyword(self) -> None:
        assert_public_tree_clean(ROOT)

    def test_public_tree_files_falls_back_without_git_and_finds_forbidden_file(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "package").mkdir()
            (root / "package" / "safe.py").write_text("safe = True\n", encoding="utf-8")
            reserved = bytes((110, 99, 114, 99)).decode("ascii")
            forbidden = f"{reserved}-marker.txt"
            (root / forbidden).write_text("fixture\n", encoding="utf-8")
            (root / "__pycache__").mkdir()
            (root / "__pycache__" / "ignored.pyc").write_bytes(b"ignored")
            files = public_tree_files(root)
            self.assertIn("package/safe.py", files)
            self.assertIn(forbidden, files)
            self.assertNotIn("__pycache__/ignored.pyc", files)

    def test_official_bootstrap_never_calls_github_or_forwards_tokens(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base, bin_dir = Path(raw), Path(raw) / "bin"
            bin_dir.mkdir()
            marker, pylog, pyz = base / "gh.called", base / "python.env", base / "fake.pyz"
            pyz.write_text("", encoding="utf-8")
            self.stub(bin_dir, "gh", f'echo called > "{marker}"; exit 91\n')
            self.stub(bin_dir, "python3", f'printf "%s,%s" "${{GH_TOKEN-}}" "${{GITHUB_TOKEN-}}" > "{pylog}"\n')
            env = self._clean_env(
                PATH=f"{bin_dir}:{os.environ['PATH']}", HOME=str(base / "home"),
                GH_TOKEN="secret", GITHUB_TOKEN="secret", ISSACSIMZ_SKIP_BUILD="1",
                ISSACSIMZ_PYZ=str(pyz), ISSACSIMZ_EVIDENCE_ROOT=str(base / "evidence"),
                ISSACSIMZ_MANIFEST_ROOT=str(base / "manifest"), ISSACSIMZ_STATE_FILE=str(base / "state"),
            )
            result = subprocess.run(["bash", "scripts/bootstrap_server.sh", "--mode", "official"], cwd=ROOT, env=env, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("READY: ./scripts/issacsimz_tmux_train.sh go2 --iters 1 --envs 64 --name smoke-go2", result.stdout)
            self.assertFalse(marker.exists())
            self.assertEqual(pylog.read_text(encoding="utf-8"), ",")
            state_text = (base / "state").read_text(encoding="utf-8")
            self.assertIn('ISSACSIMZ_H1_ROOT="/workspace/training/humanoid"', state_text)
            self.assertIn('ISSACSIMZ_GO2_ROOT="/workspace/training/quadruped"', state_text)
            self.assertIn('ISSACSIMZ_ISAACLAB_ROOT="/workspace/IsaacLab"', state_text)
            for name in ("mode.txt", "environment.txt", "nvidia-smi.txt", "python.txt", "pip-packages.txt", "isaaclab-path.txt", "isaaclab-commit.txt", "naver-repo-commit.txt", "naver-repo-remote.txt", "issacsimz-commit.txt", "bootstrap-validation.txt"):
                self.assertTrue((base / "manifest" / name).is_file(), name)
            self.assertNotIn("secret", (base / "manifest" / "environment.txt").read_text(encoding="utf-8"))

    def test_official_bootstrap_rejects_root_override(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base, bin_dir = Path(raw), Path(raw) / "bin"
            bin_dir.mkdir()
            env = self._clean_env(
                PATH=f"{bin_dir}:{os.environ['PATH']}", HOME=str(base / "home"),
                ISSACSIMZ_OFFICIAL_H1_ROOT=str(base / "alternate-h1"),
                ISSACSIMZ_STATE_FILE=str(base / "state"),
            )
            result = subprocess.run(
                ["bash", "scripts/bootstrap_server.sh", "--mode", "official"],
                cwd=ROOT, env=env, text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("official H1 root override is disabled", result.stderr)
            self.assertFalse((base / "state").exists())

    def test_personal_bootstrap_state_uses_generic_roots_for_doctor(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base, bin_dir = Path(raw), Path(raw) / "bin"
            bin_dir.mkdir()
            personal_root, lab_root = base / "personal", base / "IsaacLab"
            (lab_root / "isaaclab.sh").parent.mkdir(parents=True)
            (lab_root / "isaaclab.sh").write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
            (lab_root / "isaaclab.sh").chmod(0o755)
            pyz = base / "bootstrap.pyz"
            pyz.write_text("raise SystemExit(0)\n", encoding="utf-8")
            self.stub(bin_dir, "nvidia-smi", "exit 0\n")
            self.stub(bin_dir, "gh", f'''case "$1 $2" in
  "auth status") exit 0 ;;
  "repo clone")
    target="$4"
    git init -q "$target"
    git -C "$target" -c user.email=fixture@example.invalid -c user.name=fixture commit -q --allow-empty -m fixture
    mkdir -p "$target/training/humanoid" "$target/training/quadruped"
    : > "$target/training/humanoid/train.py"
    : > "$target/training/quadruped/train.py"
    exit 0 ;;
  "api user") echo "fixture-login"; exit 0 ;;
  *) exit 0 ;;
esac
''')
            state = base / "state"
            env = self._clean_env(
                PATH=f"{bin_dir}:{os.environ['PATH']}", HOME=str(base / "home"),
                ISSACSIMZ_SKIP_BUILD="1", ISSACSIMZ_PYZ=str(pyz),
                ISSACSIMZ_PERSONAL_ROOT=str(personal_root),
                ISSACSIMZ_PERSONAL_ISAACLAB_ROOT=str(lab_root),
                ISSACSIMZ_EVIDENCE_ROOT=str(base / "evidence"),
                ISSACSIMZ_MANIFEST_ROOT=str(base / "manifest"), ISSACSIMZ_STATE_FILE=str(state),
            )
            bootstrap = subprocess.run(
                ["bash", "scripts/bootstrap_server.sh", "--mode", "personal"],
                cwd=ROOT, env=env, text=True, capture_output=True,
            )
            self.assertEqual(bootstrap.returncode, 0, bootstrap.stderr)
            self.assertIn("READY: ./issacsimz train go2 --iters 1 --num-envs 64 --name smoke-go2 (local smoke; no Release)", bootstrap.stdout)
            self.assertNotIn("READY: ./scripts/issacsimz_tmux_train.sh go2 --iters 1", bootstrap.stdout)
            text = state.read_text(encoding="utf-8")
            self.assertIn(f'ISSACSIMZ_H1_ROOT="{personal_root}/training/humanoid"', text)
            self.assertIn(f'ISSACSIMZ_GO2_ROOT="{personal_root}/training/quadruped"', text)
            self.assertIn(f'ISSACSIMZ_ISAACLAB_ROOT="{lab_root}"', text)
            self.assertNotIn("ISSACSIMZ_OFFICIAL_H1_ROOT=", text)
            self.assertEqual(subprocess.check_output(
                ["git", "-C", str(personal_root), "config", "--local", "user.name"], text=True,
            ).strip(), "fixture-login")
            self.assertEqual(subprocess.check_output(
                ["git", "-C", str(personal_root), "config", "--local", "user.email"], text=True,
            ).strip(), "nc" + "rcissacsimz@users.noreply.github.com")
            doctor = subprocess.run(
                ["bash", "./issacsimz", "doctor", "--robot", "h1"],
                cwd=ROOT, env=env, text=True, capture_output=True,
            )
            self.assertEqual(doctor.returncode, 0, doctor.stdout + doctor.stderr)

    def test_personal_local_only_bootstrap_and_train_never_call_github(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base, bin_dir = Path(raw), Path(raw) / "bin"
            bin_dir.mkdir()
            personal_root, lab_root = base / "personal", base / "IsaacLab"
            (personal_root / "training" / "humanoid").mkdir(parents=True)
            (personal_root / "training" / "quadruped").mkdir(parents=True)
            (personal_root / "training" / "humanoid" / "train.py").write_text("# fixture\n", encoding="utf-8")
            (personal_root / "training" / "quadruped" / "train.py").write_text("# fixture\n", encoding="utf-8")
            lab_root.mkdir()
            (lab_root / "isaaclab.sh").write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
            (lab_root / "isaaclab.sh").chmod(0o755)
            pyz, state = base / "bootstrap.pyz", base / "state"
            pyz.write_text("# fixture\n", encoding="utf-8")
            archive = base / "fake-run.tar.gz"
            archive.write_bytes(b"fixture")
            gh_calls, git_calls = base / "gh.calls", base / "git.calls"
            self.stub(bin_dir, "gh", f'echo called >> "{gh_calls}"; exit 91\n')
            self.stub(bin_dir, "git", f'''printf '%s\\n' "$*" >> "{git_calls}"
case "$*" in *pull*|*config*|*remote*|*ls-remote*) exit 92;; esac
exit 1
''')
            self.stub(bin_dir, "nvidia-smi", "echo fixture-gpu\n")
            self.stub(bin_dir, "python3", f'''if [[ "${{1:-}}" == "{pyz}" && "${{2:-}}" == "train" ]]; then
  test -z "${{SUBMIT_HOST+x}}" && test -z "${{SUBMIT_TOKEN+x}}" && test "${{NO_AUTO_SUBMIT:-}}" = 1
  printf '%s\\n' "$*" > "{base / 'train.args'}"
  printf '[issacsimz] execution=COMPLETED exit=0 evidence_validation=PASS\\n'
  printf '[issacsimz] archive={archive}\\n'
fi
exit 0
''')
            env = self._clean_env(
                PATH=f"{bin_dir}:{os.environ['PATH']}", HOME=str(base / "home"),
                ISSACSIMZ_SKIP_BUILD="1", ISSACSIMZ_PYZ=str(pyz),
                ISSACSIMZ_PERSONAL_ROOT=str(personal_root),
                ISSACSIMZ_PERSONAL_ISAACLAB_ROOT=str(lab_root),
                ISSACSIMZ_EVIDENCE_ROOT=str(base / "evidence"),
                ISSACSIMZ_MANIFEST_ROOT=str(base / "manifest"),
                ISSACSIMZ_STATE_FILE=str(state),
                SUBMIT_HOST="must-not-leak", SUBMIT_TOKEN="must-not-leak",
            )
            bootstrap = subprocess.run(
                ["bash", "scripts/bootstrap_server.sh", "--mode", "personal", "--local-only"],
                cwd=ROOT, env=env, text=True, capture_output=True,
            )
            self.assertEqual(bootstrap.returncode, 0, bootstrap.stderr)
            state_text = state.read_text(encoding="utf-8")
            self.assertIn('ISSACSIMZ_LOCAL_ONLY="1"', state_text)
            self.assertFalse(gh_calls.exists())
            git_text = git_calls.read_text(encoding="utf-8")
            self.assertNotIn("pull", git_text)
            self.assertNotIn("config", git_text)
            self.assertNotIn("remote", git_text)

            train = subprocess.run(
                ["bash", "scripts/issacsimz_train.sh", "go2", "--iters", "1", "--name", "local-smoke"],
                cwd=ROOT, env=env, text=True, capture_output=True,
            )
            self.assertEqual(train.returncode, 0, train.stdout + train.stderr)
            self.assertIn("--allow-no-auto-submit", (base / "train.args").read_text(encoding="utf-8"))
            self.assertFalse(gh_calls.exists())

    def test_personal_local_only_bootstrap_rejects_submit_config(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base, bin_dir = Path(raw), Path(raw) / "bin"
            bin_dir.mkdir()
            personal_root = base / "personal"
            (personal_root / "training" / "humanoid").mkdir(parents=True)
            (personal_root / "training" / "quadruped").mkdir(parents=True)
            (personal_root / "training" / "humanoid" / "train.py").write_text("# fixture\n", encoding="utf-8")
            (personal_root / "training" / "quadruped" / "train.py").write_text("# fixture\n", encoding="utf-8")
            (personal_root / "submit_config.txt").write_text("secret fixture\n", encoding="utf-8")
            env = self._clean_env(
                PATH=f"{bin_dir}:{os.environ['PATH']}",
                ISSACSIMZ_PERSONAL_ROOT=str(personal_root),
            )
            result = subprocess.run(
                ["bash", "scripts/bootstrap_server.sh", "--mode", "personal", "--local-only"],
                cwd=ROOT, env=env, text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("refuses task submit_config.txt", result.stderr)
            self.assertNotIn("secret fixture", result.stdout + result.stderr)

    def test_zip_style_bootstrap_records_missing_git_metadata_without_failing(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base, zip_root, bin_dir = Path(raw), Path(raw) / "issacsimz-zip", Path(raw) / "bin"
            (zip_root / "scripts").mkdir(parents=True); bin_dir.mkdir()
            shutil.copy2(ROOT / "scripts" / "bootstrap_server.sh", zip_root / "scripts" / "bootstrap_server.sh")
            shutil.copy2(ROOT / "scripts" / "python_runner.sh", zip_root / "scripts" / "python_runner.sh")
            pyz, manifest = base / "fake.pyz", base / "manifest"; pyz.write_text("", encoding="utf-8")
            self.stub(bin_dir, "python3", "exit 0\n")
            env = self._clean_env(
                PATH=f"{bin_dir}:{os.environ['PATH']}", HOME=str(base / "home"), ISSACSIMZ_SKIP_BUILD="1",
                ISSACSIMZ_PYZ=str(pyz), ISSACSIMZ_EVIDENCE_ROOT=str(base / "evidence"),
                ISSACSIMZ_MANIFEST_ROOT=str(manifest), ISSACSIMZ_STATE_FILE=str(base / "state"),
            )
            result = subprocess.run(["bash", "scripts/bootstrap_server.sh", "--mode", "official"], cwd=zip_root, env=env, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((manifest / "issacsimz-commit.txt").read_text(encoding="utf-8"), "git metadata unavailable\n")

    def test_personal_publisher_uploads_archive_sidecars_and_explicit_assets(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base, bin_dir = Path(raw), Path(raw) / "bin"
            bin_dir.mkdir(); archive = base / "run.tar.gz"; archive.write_bytes(b"x")
            (base / "run.tar.gz.sha256").write_text("x", encoding="utf-8")
            (base / "run.tar.gz.metadata.json").write_text("{}", encoding="utf-8")
            video, manifest = base / "play_video.mp4", base / "video_manifest.json"
            video.write_bytes(b"video"); manifest.write_text("{}", encoding="utf-8")
            checkout = base / "repo"
            (checkout / ".git").mkdir(parents=True)
            pyz, calls, state = base / "fake.pyz", base / "publish.calls", base / "state"
            pyz.write_text("", encoding="utf-8")
            self.stub(bin_dir, "python3", "exit 0\n")
            assets = (archive, base / "run.tar.gz.sha256", base / "run.tar.gz.metadata.json", video, manifest)
            remote_rows = "\\n".join(
                f"{asset.name}\\t{asset.stat().st_size}\\tsha256:{hashlib.sha256(asset.read_bytes()).hexdigest()}"
                for asset in assets
            )
            self.stub(bin_dir, "gh", f'''printf "gh %s\\n" "$*" >> "{calls}"
if [[ "$1" == release && "$2" == view ]]; then exit 1; fi
if [[ "$1" == api ]]; then
  if [[ "${{ISSACSIMZ_FIXTURE_BAD_REMOTE:-0}}" == 1 ]]; then echo bad; else printf '%b\\n' '{remote_rows}'; fi
fi
''')
            self.stub(bin_dir, "git", f'''printf "git %s\\n" "$*" >> "{calls}"
case "$*" in
  *"remote get-url origin") echo "https://github.com/owner/private.git" ;;
  *"rev-parse --verify HEAD^{{commit}}"*) echo "checkout-commit" ;;
  *"ls-remote --exit-code"*) exit 2 ;;
  *"show-ref --verify --quiet"*) exit 1 ;;
  *"rev-parse --verify refs/tags/"*) echo "checkout-commit" ;;
  *"rev-parse refs/tags/"*) echo "annotated-tag-object" ;;
esac
''')
            state.write_text(f'ISSACSIMZ_MODE="personal"\nISSACSIMZ_PYZ="{pyz}"\nISSACSIMZ_PERSONAL_REPO="owner/private"\nISSACSIMZ_PERSONAL_ROOT="{checkout}"\n', encoding="utf-8")
            env = self._clean_env(PATH=f"{bin_dir}:{os.environ['PATH']}", ISSACSIMZ_STATE_FILE=str(state))
            result = subprocess.run(["bash", "scripts/publish_github_release.sh", str(archive), str(video), str(manifest)], cwd=ROOT, env=env, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            output = calls.read_text(encoding="utf-8")
            self.assertIn("release create", output)
            self.assertIn(str(archive), output)
            self.assertIn(str(video), output)
            self.assertIn(str(manifest), output)
            self.assertIn("tag -a -m private-run -- private-run checkout-commit", output)
            self.assertLess(output.index("push origin refs/tags/private-run:refs/tags/private-run"), output.index("release create"))
            named_env = {**env, "ISSACSIMZ_RELEASE_ROBOT": "h1",
                         "ISSACSIMZ_RELEASE_EXPERIMENT": "exp-h1-airtime-effect",
                         "ISSACSIMZ_RELEASE_CONFIG": "h1-submit-2 + feet=0.25"}
            named = subprocess.run(["bash", "scripts/publish_github_release.sh", str(archive)],
                                   cwd=ROOT, env=named_env, text=True, capture_output=True)
            self.assertEqual(named.returncode, 0, named.stdout + named.stderr)
            named_tag = "private-h1-" + datetime.now(timezone.utc).strftime("%Y%m%d") + "-exp-h1-airtime-effect-run"
            create = [line for line in calls.read_text(encoding="utf-8").splitlines()
                      if line.startswith("gh release create ")][-1]
            self.assertIn(f"release create {named_tag} ", create)
            self.assertIn("H1 · exp-h1-airtime-effect · h1-submit-2 + feet=0.25 · PERSONAL train · run", create)

    def test_personal_publisher_refuses_existing_release_before_tag_push(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base, bin_dir = Path(raw), Path(raw) / "bin"
            bin_dir.mkdir(); archive = base / "run.tar.gz"; archive.write_bytes(b"x")
            for suffix in (".sha256", ".metadata.json"):
                (base / f"run.tar.gz{suffix}").write_text("x", encoding="utf-8")
            pyz, calls, state = base / "fake.pyz", base / "publish.calls", base / "state"
            pyz.write_text("", encoding="utf-8")
            self.stub(bin_dir, "python3", "exit 0\n")
            self.stub(bin_dir, "gh", f'printf "gh %s\\n" "$*" >> "{calls}"\n')
            self.stub(bin_dir, "git", f'printf "git %s\\n" "$*" >> "{calls}"\n')
            state.write_text(f'ISSACSIMZ_MODE="personal"\nISSACSIMZ_PYZ="{pyz}"\n', encoding="utf-8")
            env = self._clean_env(PATH=f"{bin_dir}:{os.environ['PATH']}", ISSACSIMZ_STATE_FILE=str(state))
            result = subprocess.run(["bash", "scripts/publish_github_release.sh", str(archive)], cwd=ROOT, env=env, text=True, capture_output=True)
            self.assertEqual(result.returncode, 20)
            self.assertIn("Release already exists", result.stderr)
            self.assertNotIn("git ", calls.read_text(encoding="utf-8"))
            self.assertNotIn("release create", calls.read_text(encoding="utf-8"))

    def test_personal_publisher_refuses_conflicting_remote_tag(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base, bin_dir = Path(raw), Path(raw) / "bin"
            bin_dir.mkdir(); archive = base / "run.tar.gz"; archive.write_bytes(b"x")
            for suffix in (".sha256", ".metadata.json"):
                (base / f"run.tar.gz{suffix}").write_text("x", encoding="utf-8")
            checkout = base / "repo"
            (checkout / ".git").mkdir(parents=True)
            pyz, calls, state = base / "fake.pyz", base / "publish.calls", base / "state"
            pyz.write_text("", encoding="utf-8")
            self.stub(bin_dir, "python3", "exit 0\n")
            self.stub(bin_dir, "gh", f'printf "gh %s\\n" "$*" >> "{calls}"\nif [[ "$1 $2" == "release view" ]]; then exit 1; fi\n')
            self.stub(bin_dir, "git", f'''printf "git %s\\n" "$*" >> "{calls}"
case "$*" in
  *"remote get-url origin") echo "https://github.com/owner/private.git" ;;
  *"rev-parse --verify HEAD^{{commit}}"*) echo "checkout-commit" ;;
  *"ls-remote --exit-code"*) printf 'other-tag-object\\trefs/tags/private-run\\n' ;;
  *"show-ref --verify --quiet"*) exit 1 ;;
esac
''')
            state.write_text(f'ISSACSIMZ_MODE="personal"\nISSACSIMZ_PYZ="{pyz}"\nISSACSIMZ_PERSONAL_REPO="owner/private"\nISSACSIMZ_PERSONAL_ROOT="{checkout}"\n', encoding="utf-8")
            env = self._clean_env(PATH=f"{bin_dir}:{os.environ['PATH']}", ISSACSIMZ_STATE_FILE=str(state))
            result = subprocess.run(["bash", "scripts/publish_github_release.sh", str(archive)], cwd=ROOT, env=env, text=True, capture_output=True)
            self.assertEqual(result.returncode, 20)
            self.assertIn("remote tag exists without matching local annotated tag", result.stderr)
            output = calls.read_text(encoding="utf-8")
            self.assertNotIn("tag -a", output)
            self.assertNotIn("push origin", output)
            self.assertNotIn("release create", output)

    def test_video_suite_publisher_uploads_only_verified_explicit_assets(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base, bin_dir = Path(raw), Path(raw) / "bin"
            bin_dir.mkdir()
            suite, _, _, assets = self.make_suite(base)
            checkout = base / "repo"
            (checkout / ".git").mkdir(parents=True)
            calls, git_calls, state = base / "gh.calls", base / "git.calls", base / "state"
            remote = "".join(
                f"{asset.name}\\t{asset.stat().st_size}\\tsha256:{hashlib.sha256(asset.read_bytes()).hexdigest()}\\n"
                for asset in assets
            )
            self.stub(bin_dir, "gh", f'''printf "%s\\n" "$*" >> "{calls}"
if [[ "$1 $2" == "release view" ]]; then exit 1; fi
if [[ "$1" == "api" ]]; then printf '{remote}'; fi
''')
            self.stub(bin_dir, "git", f'''printf "%s\\n" "$*" >> "{git_calls}"
case "$*" in
  *"remote get-url origin") echo "https://github.com/owner/private.git" ;;
  *"rev-parse --verify HEAD^{{commit}}"*) echo "checkout-commit" ;;
  *"ls-remote --exit-code"*) exit 2 ;;
  *"show-ref --verify --quiet"*) exit 1 ;;
  *"rev-parse --verify refs/tags/"*) echo "checkout-commit" ;;
  *"rev-parse refs/tags/"*) echo "annotated-tag-object" ;;
esac
''')
            state.write_text(
                f'ISSACSIMZ_MODE="personal"\nISSACSIMZ_PERSONAL_REPO="owner/private"\nISSACSIMZ_PERSONAL_ROOT="{checkout}"\nISSACSIMZ_ISAACLAB_ROOT="/unused"\n',
                encoding="utf-8",
            )
            env = self._clean_env(
                PATH=f"{bin_dir}:{os.environ['PATH']}", ISSACSIMZ_STATE_FILE=str(state),
            )
            # _clean_env intentionally removes an inherited runner; set the test runner afterwards.
            env["ISSACSIMZ_PYTHON_RUNNER"] = TEST_PYTHON_RUNNER
            result = subprocess.run([
                "bash", "scripts/publish_video_suite_release.sh", "--suite-dir", str(suite),
                "--tag", "h1-suite-test", "--title", "Reviewed suite", "--notes", "approved",
            ], cwd=ROOT, env=env, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            output = calls.read_text(encoding="utf-8")
            create = next(line for line in output.splitlines() if line.startswith("release create "))
            for asset in assets:
                self.assertIn(str(asset), create)
            self.assertIn("--title Reviewed suite", create)
            self.assertIn("--notes approved", create)
            self.assertIn("tag -a -m Reviewed suite -- h1-suite-test", git_calls.read_text(encoding="utf-8"))
            self.assertIn("push origin refs/tags/h1-suite-test:refs/tags/h1-suite-test", git_calls.read_text(encoding="utf-8"))
            self.assertIn("video_suite_release=https://github.com/owner/private/releases/tag/h1-suite-test", result.stdout)

    def test_video_suite_publisher_rejects_official_before_github(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base, bin_dir = Path(raw), Path(raw) / "bin"
            bin_dir.mkdir(); marker, state = base / "gh.called", base / "state"
            self.stub(bin_dir, "gh", f'echo called > "{marker}"\n')
            state.write_text('ISSACSIMZ_MODE="official"\n', encoding="utf-8")
            env = self._clean_env(PATH=f"{bin_dir}:{os.environ['PATH']}", ISSACSIMZ_STATE_FILE=str(state))
            result = subprocess.run([
                "bash", "scripts/publish_video_suite_release.sh", "--suite-dir", str(base / "missing"),
                "--tag", "tag", "--title", "title", "--notes", "notes",
            ], cwd=ROOT, env=env, text=True, capture_output=True)
            self.assertEqual(result.returncode, 20)
            self.assertIn("disabled outside personal mode", result.stderr)
            self.assertFalse(marker.exists())

    def test_video_suite_publisher_does_not_upload_tampered_suite(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base, bin_dir = Path(raw), Path(raw) / "bin"
            bin_dir.mkdir(); suite, _, _, _ = self.make_suite(base)
            (suite / "videos" / "stairs.mp4").write_bytes(b"tampered")
            calls, state = base / "gh.calls", base / "state"
            self.stub(bin_dir, "gh", f'printf "%s\\n" "$*" >> "{calls}"\nif [[ "$1 $2" == "release view" ]]; then exit 1; fi\n')
            state.write_text('ISSACSIMZ_MODE="personal"\nISSACSIMZ_ISAACLAB_ROOT="/unused"\n', encoding="utf-8")
            env = self._clean_env(PATH=f"{bin_dir}:{os.environ['PATH']}", ISSACSIMZ_STATE_FILE=str(state))
            env["ISSACSIMZ_PYTHON_RUNNER"] = TEST_PYTHON_RUNNER
            result = subprocess.run([
                "bash", "scripts/publish_video_suite_release.sh", "--suite-dir", str(suite),
                "--tag", "tag", "--title", "title", "--notes", "notes",
            ], cwd=ROOT, env=env, text=True, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("MP4 SHA mismatch", result.stderr)
            self.assertNotIn("release create", calls.read_text(encoding="utf-8"))

    def test_video_suite_publisher_refuses_existing_tag(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base, bin_dir = Path(raw), Path(raw) / "bin"
            bin_dir.mkdir(); suite, _, _, _ = self.make_suite(base)
            calls, state = base / "gh.calls", base / "state"
            self.stub(bin_dir, "gh", f'printf "%s\\n" "$*" >> "{calls}"\nexit 0\n')
            state.write_text('ISSACSIMZ_MODE="personal"\nISSACSIMZ_ISAACLAB_ROOT="/unused"\n', encoding="utf-8")
            env = self._clean_env(PATH=f"{bin_dir}:{os.environ['PATH']}", ISSACSIMZ_STATE_FILE=str(state))
            env["ISSACSIMZ_PYTHON_RUNNER"] = TEST_PYTHON_RUNNER
            result = subprocess.run([
                "bash", "scripts/publish_video_suite_release.sh", "--suite-dir", str(suite),
                "--tag", "existing", "--title", "title", "--notes", "notes",
            ], cwd=ROOT, env=env, text=True, capture_output=True)
            self.assertEqual(result.returncode, 20)
            self.assertIn("Release already exists", result.stderr)
            self.assertNotIn("release create", calls.read_text(encoding="utf-8"))

    def test_official_video_never_calls_publisher_or_forwards_tokens(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base, bin_dir = Path(raw), Path(raw) / "bin"
            bin_dir.mkdir(); marker, pylog, pyz = base / "gh.called", base / "python.env", base / "fake.pyz"
            pyz.write_text("", encoding="utf-8")
            self.stub(bin_dir, "gh", f'echo called > "{marker}"; exit 91\n')
            self.stub(bin_dir, "python3", f'printf "%s,%s|%s" "${{GH_TOKEN-}}" "${{GITHUB_TOKEN-}}" "$*" > "{pylog}"\n')
            state = base / "state"
            state.write_text(f'ISSACSIMZ_MODE="official"\nISSACSIMZ_PYZ="{pyz}"\nISSACSIMZ_EVIDENCE_ROOT="{base / "evidence"}"\nISSACSIMZ_H1_ROOT="/workspace/training/humanoid"\nISSACSIMZ_GO2_ROOT="/workspace/training/quadruped"\nISSACSIMZ_ISAACLAB_ROOT="/workspace/IsaacLab"\n', encoding="utf-8")
            (base / "evidence").mkdir()
            env = self._clean_env(
                PATH=f"{bin_dir}:{os.environ['PATH']}", GH_TOKEN="secret", GITHUB_TOKEN="secret",
                ISSACSIMZ_STATE_FILE=str(state),
            )
            result = subprocess.run(["bash", "scripts/issacsimz_video.sh", "go2", "--from-run", "official-fixture"], cwd=ROOT, env=env, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(marker.exists())
            self.assertTrue(pylog.read_text(encoding="utf-8").startswith(",|"))

    def test_personal_video_publishes_mp4_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base, bin_dir = Path(raw), Path(raw) / "bin"
            bin_dir.mkdir(); archive, evidence = base / "video.tar.gz", base / "video-evidence"
            archive.write_bytes(b"x")
            (base / "video.tar.gz.sha256").write_text("x", encoding="utf-8")
            (base / "video.tar.gz.metadata.json").write_text("{}", encoding="utf-8")
            (evidence / "collected" / "exported").mkdir(parents=True)
            video, manifest = evidence / "collected" / "exported" / "play_video.mp4", evidence / "video_manifest.json"
            video.write_bytes(b"video"); manifest.write_text("{}", encoding="utf-8")
            checkout = base / "repo"
            (checkout / ".git").mkdir(parents=True)
            pyz, calls, state = base / "fake.pyz", base / "gh.calls", base / "state"
            pyz.write_text("", encoding="utf-8")
            self.stub(bin_dir, "python3", f'echo "[issacsimz] archive={archive}"\necho "[issacsimz] evidence={evidence}"\n')
            assets = (archive, base / "video.tar.gz.sha256", base / "video.tar.gz.metadata.json", video, manifest)
            remote_rows = "\\n".join(
                f"{asset.name}\\t{asset.stat().st_size}\\tsha256:{hashlib.sha256(asset.read_bytes()).hexdigest()}"
                for asset in assets
            )
            self.stub(bin_dir, "gh", f'''printf "%s\\n" "$*" >> "{calls}"
if [[ "$1" == release && "$2" == view ]]; then exit 1; fi
if [[ "$1" == api ]]; then printf '%b\\n' '{remote_rows}'; fi
''')
            self.stub(bin_dir, "git", '''case "$*" in
  *"remote get-url origin") echo "https://github.com/owner/private.git" ;;
  *"rev-parse --verify HEAD^{commit}"*) echo "checkout-commit" ;;
  *"ls-remote --exit-code"*) exit 2 ;;
  *"show-ref --verify --quiet"*) exit 1 ;;
  *"rev-parse --verify refs/tags/"*) echo "checkout-commit" ;;
  *"rev-parse refs/tags/"*) echo "annotated-tag-object" ;;
esac
''')
            state.write_text(f'ISSACSIMZ_MODE="personal"\nISSACSIMZ_PYZ="{pyz}"\nISSACSIMZ_EVIDENCE_ROOT="{base}"\nISSACSIMZ_GO2_ROOT="/ephemeral/naver/training/quadruped"\nISSACSIMZ_ISAACLAB_ROOT="/isaac"\nISSACSIMZ_PERSONAL_ROOT="{checkout}"\nISSACSIMZ_PERSONAL_ISAACLAB_ROOT="/isaac"\nISSACSIMZ_PERSONAL_REPO="owner/private"\n', encoding="utf-8")
            env = self._clean_env(PATH=f"{bin_dir}:{os.environ['PATH']}", ISSACSIMZ_STATE_FILE=str(state))
            result = subprocess.run(["bash", "scripts/issacsimz_video.sh", "go2", "--from-run", "train-run"], cwd=ROOT, env=env, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            output = calls.read_text(encoding="utf-8")
            self.assertIn(str(video), output)
            self.assertIn(str(manifest), output)

    def test_personal_video_does_not_publish_when_video_fails_validation(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base, bin_dir = Path(raw), Path(raw) / "bin"
            bin_dir.mkdir(); archive = base / "video.tar.gz"; archive.write_bytes(b"x")
            pyz, marker, state = base / "fake.pyz", base / "gh.called", base / "state"; pyz.write_text("", encoding="utf-8")
            self.stub(bin_dir, "python3", f'echo "[issacsimz] archive={archive}"\nexit 3\n')
            self.stub(bin_dir, "gh", f'echo called > "{marker}"\n')
            state.write_text(f'ISSACSIMZ_MODE="personal"\nISSACSIMZ_PYZ="{pyz}"\nISSACSIMZ_EVIDENCE_ROOT="{base}"\nISSACSIMZ_GO2_ROOT="/ephemeral/naver/training/quadruped"\nISSACSIMZ_ISAACLAB_ROOT="/isaac"\nISSACSIMZ_PERSONAL_ROOT="/ephemeral/naver"\nISSACSIMZ_PERSONAL_ISAACLAB_ROOT="/isaac"\n', encoding="utf-8")
            env = self._clean_env(PATH=f"{bin_dir}:{os.environ['PATH']}", ISSACSIMZ_STATE_FILE=str(state))
            result = subprocess.run(["bash", "scripts/issacsimz_video.sh", "go2", "--from-run", "train-run"], cwd=ROOT, env=env, text=True, capture_output=True)
            self.assertEqual(result.returncode, 3, result.stderr)
            self.assertFalse(marker.exists())

    def test_personal_video_suite_can_explicitly_suppress_per_video_publish(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base, bin_dir = Path(raw), Path(raw) / "bin"
            bin_dir.mkdir(); archive, evidence = base / "video.tar.gz", base / "video-evidence"
            archive.write_bytes(b"archive")
            (evidence / "collected" / "exported").mkdir(parents=True)
            (evidence / "collected" / "exported" / "play_video.mp4").write_bytes(b"video")
            (evidence / "video_manifest.json").write_text("{}", encoding="utf-8")
            pyz, marker, state = base / "fake.pyz", base / "gh.called", base / "state"
            pyz.write_text("", encoding="utf-8")
            self.stub(bin_dir, "python3", f'echo "[issacsimz] archive={archive}"\necho "[issacsimz] evidence={evidence}"\n')
            self.stub(bin_dir, "gh", f'echo called > "{marker}"\n')
            state.write_text(
                f'ISSACSIMZ_MODE="personal"\nISSACSIMZ_PYZ="{pyz}"\nISSACSIMZ_EVIDENCE_ROOT="{base}"\n'
                'ISSACSIMZ_GO2_ROOT="/ephemeral/naver/training/quadruped"\n'
                'ISSACSIMZ_ISAACLAB_ROOT="/isaac"\n',
                encoding="utf-8",
            )
            env = self._clean_env(
                PATH=f"{bin_dir}:{os.environ['PATH']}", ISSACSIMZ_STATE_FILE=str(state),
                ISSACSIMZ_DISABLE_PUBLISH="1",
            )
            result = subprocess.run(
                ["bash", "scripts/issacsimz_video.sh", "go2", "--from-run", "train-run"],
                cwd=ROOT, env=env, text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(marker.exists())

    def test_video_suite_runs_six_labeled_fixed_terrains(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base, bin_dir = Path(raw), Path(raw) / "bin"
            bin_dir.mkdir()
            evidence, download, calls, pyz, state = base / "evidence", base / "download", base / "calls", base / "fake.pyz", base / "state"
            evidence.mkdir(); pyz.write_text("", encoding="utf-8")
            checkpoint = evidence / "runs" / "train-run" / "collected" / "exported" / "model_best.pt"
            checkpoint.parent.mkdir(parents=True); checkpoint.write_bytes(b"train-checkpoint")
            self.suite_runner(bin_dir, evidence=evidence, download=download, calls=calls)
            state.write_text(
                f'ISSACSIMZ_MODE="personal"\nISSACSIMZ_PYZ="{pyz}"\nISSACSIMZ_EVIDENCE_ROOT="{evidence}"\n'
                'ISSACSIMZ_GO2_ROOT="/workspace/training/quadruped"\n'
                'ISSACSIMZ_ISAACLAB_ROOT="/workspace/IsaacLab"\n',
                encoding="utf-8",
            )
            env = self._clean_env(
                PATH=f"{bin_dir}:{os.environ['PATH']}", ISSACSIMZ_STATE_FILE=str(state),
                ISSACSIMZ_DOWNLOAD_ROOT=str(download),
            )
            result = subprocess.run(
                ["bash", "scripts/issacsimz_video_suite.sh", "go2", "--from-run", "train-run", "--no-publish"],
                cwd=ROOT, env=env, text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            lines = calls.read_text(encoding="utf-8").splitlines()
            labels = ("stairs", "inverted_stairs", "boxes", "random_rough", "slope_up_20deg", "slope_down_20deg")
            terrains = ("pyramid_stairs", "pyramid_stairs_inv", "boxes", "random_rough", "hf_pyramid_slope", "hf_pyramid_slope_inv")
            self.assertEqual(len(lines), 6)
            for line, label, selected in zip(lines, labels, terrains):
                self.assertIn(f"--label {label}", line)
                self.assertIn("env.scene.terrain.terrain_generator.num_rows=1", line)
                self.assertIn("env.scene.terrain.terrain_generator.num_cols=1", line)
                self.assertIn("env.scene.terrain.terrain_generator.horizontal_scale=0.05", line)
                for terrain in terrains:
                    expected = 1.0 if terrain == selected else 0.0
                    self.assertIn(f"sub_terrains.{terrain}.proportion={expected}", line)
                if selected in {"hf_pyramid_slope", "hf_pyramid_slope_inv"}:
                    self.assertIn(f"sub_terrains.{selected}.slope_range=[0.363970234,0.363970234]", line)
                else:
                    self.assertNotIn(".slope_range=", line)
            self.assertIn("video_suite=COMPLETE", result.stdout)
            manifest = json.loads((download / "train-run" / "video_suite_manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["checkpoint_filename"], "model_best.pt")
            self.assertEqual(len(manifest["terrains"]), 6)
            self.assertEqual(len({item["video_evidence_id"] for item in manifest["terrains"]}), 6)
            self.assertEqual(len((download / "train-run" / "SHA256SUMS").read_text(encoding="utf-8").splitlines()), 7)
            self.assertTrue((download / "train-run-download.tar.gz").is_file())
            self.assertTrue((download / "train-run-download.tar.gz.sha256").is_file())

    def test_video_suite_explicit_publish_uploads_verified_ten_assets(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base, bin_dir = Path(raw), Path(raw) / "bin"
            bin_dir.mkdir()
            evidence, download = base / "evidence", base / "download"
            calls, gh_calls, pyz, state = base / "calls", base / "gh.calls", base / "fake.pyz", base / "state"
            checkout = base / "repo"
            (checkout / ".git").mkdir(parents=True)
            notes = base / "notes.md"
            notes.write_text("Reviewed model_4700 suite.\n", encoding="utf-8")
            evidence.mkdir(); pyz.write_text("", encoding="utf-8")
            checkpoint = evidence / "runs" / "train-run" / "collected" / "exported" / "model_best.pt"
            checkpoint.parent.mkdir(parents=True); checkpoint.write_bytes(b"train-checkpoint")
            self.suite_runner(bin_dir, evidence=evidence, download=download, calls=calls)
            self.stub(bin_dir, "gh", f'''printf "%s\\n" "$*" >> "{gh_calls}"
if [[ "$1 $2" == "release view" ]]; then exit 1; fi
if [[ "$1" == "api" ]]; then
  for asset in "{download}/train-run/videos/"*.mp4 "{download}/train-run/video_suite_manifest.json" "{download}/train-run/SHA256SUMS" "{download}/train-run-download.tar.gz" "{download}/train-run-download.tar.gz.sha256"; do
    printf '%s\\t%s\\tsha256:%s\\n' "$(basename "$asset")" "$(stat -c '%s' "$asset")" "$(sha256sum "$asset" | awk '{{print $1}}')"
  done
fi
''')
            self.stub(bin_dir, "git", '''case "$*" in
  *"remote get-url origin") echo "https://github.com/SE3C/naver-issacsim-nvidia.git" ;;
  *"rev-parse --verify HEAD^{commit}"*) echo "checkout-commit" ;;
  *"ls-remote --exit-code"*) exit 2 ;;
  *"show-ref --verify --quiet"*) exit 1 ;;
  *"rev-parse --verify refs/tags/"*) echo "checkout-commit" ;;
  *"rev-parse refs/tags/"*) echo "annotated-tag-object" ;;
esac
''')
            state.write_text(
                f'ISSACSIMZ_MODE="personal"\nISSACSIMZ_PYZ="{pyz}"\nISSACSIMZ_EVIDENCE_ROOT="{evidence}"\n'
                f'ISSACSIMZ_PERSONAL_ROOT="{checkout}"\n'
                'ISSACSIMZ_GO2_ROOT="/workspace/training/quadruped"\n'
                'ISSACSIMZ_ISAACLAB_ROOT="/workspace/IsaacLab"\n', encoding="utf-8",
            )
            env = self._clean_env(
                PATH=f"{bin_dir}:{os.environ['PATH']}", ISSACSIMZ_STATE_FILE=str(state),
                ISSACSIMZ_DOWNLOAD_ROOT=str(download),
            )
            result = subprocess.run([
                "bash", "scripts/issacsimz_video_suite.sh", "go2", "--from-run", "train-run",
                "--publish", "--tag", "h012-model4700-videos", "--title", "H-012 model_4700",
                "--notes-file", str(notes),
            ], cwd=ROOT, env=env, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            create = next(line for line in gh_calls.read_text(encoding="utf-8").splitlines()
                          if line.startswith("release create "))
            self.assertIn("--notes-file", create)
            for name in ("video_suite_manifest.json", "SHA256SUMS", "train-run-download.tar.gz",
                         "train-run-download.tar.gz.sha256"):
                self.assertIn(name, create)
            self.assertEqual(create.count(".mp4"), 6)
            self.assertIn("video_suite_release=https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/h012-model4700-videos", result.stdout)
            automatic = subprocess.run([
                "bash", "scripts/issacsimz_video_suite.sh", "go2", "--from-run", "train-run",
            ], cwd=ROOT, env=env, text=True, capture_output=True)
            self.assertEqual(automatic.returncode, 0, automatic.stdout + automatic.stderr)
            auto_tag = "private-train-run-videos"
            self.assertIn(f"video_suite_release=https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/{auto_tag}", automatic.stdout)
            creates = [line for line in gh_calls.read_text(encoding="utf-8").splitlines()
                       if line.startswith("release create ")]
            self.assertEqual(len(creates), 2)
            self.assertIn(f"release create {auto_tag} ", creates[1])
            self.assertEqual(creates[1].count(".mp4"), 6)
            self.assertIn("--notes Personal NVIDIA/Brev six-terrain video suite.", creates[1])
            named = subprocess.run([
                "bash", "scripts/issacsimz_video_suite.sh", "go2", "--from-run", "train-run",
                "--release-experiment", "exp-go2-gait-stability",
                "--release-config", "g2-submit-3 + feet=0.03",
            ], cwd=ROOT, env=env, text=True, capture_output=True)
            self.assertEqual(named.returncode, 0, named.stdout + named.stderr)
            day = datetime.now(timezone.utc).strftime("%Y%m%d")
            named_tag = f"private-go2-{day}-exp-go2-gait-stability-train-run-videos"
            self.assertIn(f"video_suite_release=https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/{named_tag}", named.stdout)
            named_create = [line for line in gh_calls.read_text(encoding="utf-8").splitlines()
                            if line.startswith("release create ")][-1]
            self.assertIn("GO2 · exp-go2-gait-stability · g2-submit-3 + feet=0.03 · PERSONAL videos · train-run", named_create)

    def test_video_suite_publish_requires_explicit_review_details(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw)
            state = base / "state"
            state.write_text('ISSACSIMZ_MODE="personal"\n', encoding="utf-8")
            env = self._clean_env(ISSACSIMZ_STATE_FILE=str(state))
            result = subprocess.run([
                "bash", "scripts/issacsimz_video_suite.sh", "h1", "--checkpoint", "missing.pt",
                "--publish", "--tag", "h012-model4700-videos",
            ], cwd=ROOT, env=env, text=True, capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("--publish requires", result.stderr)

    def test_official_video_suite_is_rejected_before_python_or_native_play(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base, bin_dir = Path(raw), Path(raw) / "bin"
            bin_dir.mkdir()
            marker, state = base / "python.called", base / "state"
            self.stub(bin_dir, "python3", f'echo called > "{marker}"\n')
            state.write_text(
                'ISSACSIMZ_MODE="official"\n'
                'ISSACSIMZ_EVIDENCE_ROOT="/tmp/evidence"\n'
                'ISSACSIMZ_GO2_ROOT="/workspace/training/quadruped"\n'
                'ISSACSIMZ_ISAACLAB_ROOT="/workspace/IsaacLab"\n',
                encoding="utf-8",
            )
            env = self._clean_env(PATH=f"{bin_dir}:{os.environ['PATH']}", ISSACSIMZ_STATE_FILE=str(state))
            result = subprocess.run(
                ["bash", "scripts/issacsimz_video_suite.sh", "go2", "--from-run", "unused"],
                cwd=ROOT, env=env, text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("only in personal mode", result.stderr)
            self.assertFalse(marker.exists())

    def test_video_suite_accepts_numbered_checkpoint(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base, bin_dir = Path(raw), Path(raw) / "bin"
            bin_dir.mkdir()
            evidence, download, calls, pyz, state = base / "evidence", base / "download", base / "calls", base / "fake.pyz", base / "state"
            evidence.mkdir(); pyz.write_text("", encoding="utf-8")
            checkpoint = base / "received" / "model_4997.pt"
            checkpoint.parent.mkdir(); checkpoint.write_bytes(b"numbered-checkpoint")
            self.suite_runner(bin_dir, evidence=evidence, download=download, calls=calls)
            state.write_text(
                f'ISSACSIMZ_MODE="personal"\nISSACSIMZ_PYZ="{pyz}"\nISSACSIMZ_EVIDENCE_ROOT="{evidence}"\n'
                'ISSACSIMZ_GO2_ROOT="/workspace/training/quadruped"\n'
                'ISSACSIMZ_ISAACLAB_ROOT="/workspace/IsaacLab"\n',
                encoding="utf-8",
            )
            env = self._clean_env(
                PATH=f"{bin_dir}:{os.environ['PATH']}", ISSACSIMZ_STATE_FILE=str(state),
                ISSACSIMZ_DOWNLOAD_ROOT=str(download),
            )
            result = subprocess.run(
                ["bash", "scripts/issacsimz_video_suite.sh", "go2", "--checkpoint", str(checkpoint), "--no-publish"],
                cwd=ROOT, env=env, text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            lines = calls.read_text(encoding="utf-8").splitlines()
            labels = ("stairs", "inverted_stairs", "boxes", "random_rough", "slope_up_20deg", "slope_down_20deg")
            self.assertEqual(len(lines), 6)
            handoff_ids = set()
            for line, label in zip(lines, labels):
                self.assertIn("play go2", line)
                self.assertIn(f"--checkpoint {checkpoint.resolve()}", line)
                self.assertIn(f"--video-label {label}", line)
                self.assertIn("--num-envs 1", line)
                self.assertNotIn("--from-run", line)
                handoff_ids.add(line.split("--handoff-run-id ", 1)[1].split()[0])
            self.assertEqual(len(handoff_ids), 1)
            handoff = handoff_ids.pop()
            self.assertTrue(handoff.startswith("checkpoint-go2-model_4997-"))
            self.assertIn(f"video_suite=COMPLETE run={handoff}", result.stdout)

    def test_h1_video_suite_uses_ten_degree_slope_labels(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base, bin_dir = Path(raw), Path(raw) / "bin"
            bin_dir.mkdir()
            evidence, download, calls, pyz, state = base / "evidence", base / "download", base / "calls", base / "fake.pyz", base / "state"
            evidence.mkdir(); pyz.write_text("", encoding="utf-8")
            checkpoint = evidence / "runs" / "train-run" / "collected" / "exported" / "model_best.pt"
            checkpoint.parent.mkdir(parents=True); checkpoint.write_bytes(b"h1-train-checkpoint")
            self.suite_runner(bin_dir, evidence=evidence, download=download, calls=calls)
            state.write_text(
                f'ISSACSIMZ_MODE="personal"\nISSACSIMZ_PYZ="{pyz}"\nISSACSIMZ_EVIDENCE_ROOT="{evidence}"\n'
                'ISSACSIMZ_H1_ROOT="/workspace/training/humanoid"\n'
                'ISSACSIMZ_ISAACLAB_ROOT="/workspace/IsaacLab"\n',
                encoding="utf-8",
            )
            env = self._clean_env(
                PATH=f"{bin_dir}:{os.environ['PATH']}", ISSACSIMZ_STATE_FILE=str(state),
                ISSACSIMZ_DOWNLOAD_ROOT=str(download),
            )
            result = subprocess.run(
                ["bash", "scripts/issacsimz_video_suite.sh", "h1", "--from-run", "train-run", "--no-publish"],
                cwd=ROOT, env=env, text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            lines = calls.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 6)
            self.assertIn("--label slope_up_10deg", lines[4])
            self.assertIn("sub_terrains.hf_pyramid_slope.slope_range=[0.176326981,0.176326981]", lines[4])
            self.assertIn("--label slope_down_10deg", lines[5])
            self.assertIn("sub_terrains.hf_pyramid_slope_inv.slope_range=[0.176326981,0.176326981]", lines[5])

    def test_video_suite_stops_on_fourth_failure(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base, bin_dir = Path(raw), Path(raw) / "bin"
            bin_dir.mkdir()
            evidence, download, calls, pyz, state = base / "evidence", base / "download", base / "calls", base / "fake.pyz", base / "state"
            evidence.mkdir(); pyz.write_text("", encoding="utf-8")
            checkpoint = evidence / "runs" / "train-run" / "collected" / "exported" / "model_best.pt"
            checkpoint.parent.mkdir(parents=True); checkpoint.write_bytes(b"train-checkpoint")
            self.suite_runner(bin_dir, evidence=evidence, download=download, calls=calls, fail_at=4)
            state.write_text(
                f'ISSACSIMZ_MODE="personal"\nISSACSIMZ_PYZ="{pyz}"\nISSACSIMZ_EVIDENCE_ROOT="{evidence}"\n'
                'ISSACSIMZ_GO2_ROOT="/workspace/training/quadruped"\n'
                'ISSACSIMZ_ISAACLAB_ROOT="/workspace/IsaacLab"\n',
                encoding="utf-8",
            )
            env = self._clean_env(
                PATH=f"{bin_dir}:{os.environ['PATH']}", ISSACSIMZ_STATE_FILE=str(state),
                ISSACSIMZ_DOWNLOAD_ROOT=str(download),
            )
            result = subprocess.run(
                ["bash", "scripts/issacsimz_video_suite.sh", "go2", "--from-run", "train-run"],
                cwd=ROOT, env=env, text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 7)
            self.assertEqual(len(calls.read_text(encoding="utf-8").splitlines()), 4)
            self.assertIn("stopped at random_rough", result.stderr)
            self.assertNotIn("video_suite=COMPLETE", result.stdout + result.stderr)

    def test_official_train_never_calls_publisher_or_forwards_tokens(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base, bin_dir = Path(raw), Path(raw) / "bin"
            bin_dir.mkdir(); marker, pylog, pyz = base / "gh.called", base / "python.env", base / "fake.pyz"
            pyz.write_text("", encoding="utf-8")
            self.stub(bin_dir, "gh", f'echo called > "{marker}"; exit 91\n')
            self.stub(bin_dir, "python3", f'printf "%s,%s|%s" "${{GH_TOKEN-}}" "${{GITHUB_TOKEN-}}" "$*" > "{pylog}"\n')
            state = base / "state"
            state.write_text(f'ISSACSIMZ_MODE="official"\nISSACSIMZ_PYZ="{pyz}"\nISSACSIMZ_EVIDENCE_ROOT="{base / "evidence"}"\nISSACSIMZ_H1_ROOT="/workspace/training/humanoid"\nISSACSIMZ_GO2_ROOT="/workspace/training/quadruped"\nISSACSIMZ_ISAACLAB_ROOT="/workspace/IsaacLab"\n', encoding="utf-8")
            (base / "evidence").mkdir()
            env = self._clean_env(
                PATH=f"{bin_dir}:{os.environ['PATH']}", GH_TOKEN="secret", GITHUB_TOKEN="secret",
                ISSACSIMZ_STATE_FILE=str(state),
            )
            result = subprocess.run(["bash", "scripts/issacsimz_train.sh", "go2", "--iters", "1", "--envs", "64", "--name", "official-fixture"], cwd=ROOT, env=env, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(marker.exists())
            self.assertTrue(pylog.read_text(encoding="utf-8").startswith(",|"))

    def test_example_config_has_no_secret_assignments(self) -> None:
        text = (ROOT / "config/issacsimz.conf.example").read_text(encoding="utf-8")
        self.assertNotIn("GH_TOKEN=", text)
        self.assertNotIn("SUBMIT_TOKEN=", text)
        self.assertIn('ISSACSIMZ_PERSONAL_ROOT="/ephemeral/naver-issacsim-nvidia"', text)
