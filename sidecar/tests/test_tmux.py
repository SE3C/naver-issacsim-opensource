from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from issacsimz_cli.cli import _tmux_session_name, _without_tmux_options, build_parser, launch_train_tmux, main


class TmuxCliTests(unittest.TestCase):
    def _args(self, *extra: str):
        source = ["train", "go2", "--iters", "10", "--name", "go2: final run", "--tmux", *extra]
        args = build_parser().parse_args(source)
        args._source_argv = source
        return args

    def test_session_name_is_safe_and_bounded(self) -> None:
        self.assertEqual(_tmux_session_name("go2", "a run:1", None), "issacsimz-go2-a-run-1")
        self.assertEqual(_tmux_session_name("go2", "x", "custom name:1"), "custom-name-1")
        self.assertLessEqual(len(_tmux_session_name("go2", "x" * 200, None)), 100)
        with self.assertRaises(ValueError):
            _tmux_session_name("go2", "x", "???")

    def test_launcher_removes_only_tmux_options(self) -> None:
        self.assertEqual(
            _without_tmux_options(["train", "go2", "--tmux", "--tmux-session", "one", "--name", "x", "--tmux-session=two"]),
            ["train", "go2", "--name", "x"],
        )

    def test_launcher_creates_detached_session_without_recursion(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            pyz = Path(raw) / "issacsimz.pyz"
            pyz.write_bytes(b"fixture")
            args = self._args("--tmux-session", "custom name")
            calls = []

            def run(command, **kwargs):
                calls.append((command, kwargs))
                return SimpleNamespace(returncode=1)

            with patch.dict(os.environ, {}, clear=False), \
                 patch("issacsimz_cli.cli.shutil.which", return_value="/usr/bin/tmux"), \
                 patch("issacsimz_cli.cli.subprocess.run", side_effect=run), \
                 patch("issacsimz_cli.cli.train", return_value=0) as preflight, \
                 patch("issacsimz_cli.cli.sys.argv", [str(pyz)]):
                os.environ.pop("TMUX", None)
                self.assertEqual(launch_train_tmux(args), 0)

            self.assertTrue(preflight.call_args.args[0].preflight_only)
            self.assertFalse(args.preflight_only)
            self.assertEqual(calls[0][0], ["/usr/bin/tmux", "has-session", "-t", "custom-name"])
            command = calls[1][0]
            self.assertEqual(command[:5], ["/usr/bin/tmux", "new-session", "-d", "-s", "custom-name"])
            self.assertTrue(calls[1][1]["check"])
            self.assertIn(str(pyz), command[-1])
            self.assertNotIn("--tmux", command[-1])
            self.assertNotIn("--tmux-session", command[-1])

    def test_launcher_does_not_start_tmux_when_preflight_fails(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            pyz = Path(raw) / "issacsimz.pyz"
            pyz.write_bytes(b"fixture")
            with patch.dict(os.environ, {}, clear=False), \
                 patch("issacsimz_cli.cli.shutil.which", return_value="/usr/bin/tmux"), \
                 patch("issacsimz_cli.cli.subprocess.run", return_value=SimpleNamespace(returncode=1)) as tmux_run, \
                 patch("issacsimz_cli.cli.train", side_effect=ValueError("bad checkpoint")), \
                 patch("issacsimz_cli.cli.sys.argv", [str(pyz)]):
                os.environ.pop("TMUX", None)
                with self.assertRaisesRegex(ValueError, "bad checkpoint"):
                    launch_train_tmux(self._args())
            self.assertEqual(tmux_run.call_count, 1)

    def test_launcher_rejects_existing_session(self) -> None:
        args = self._args()
        with patch.dict(os.environ, {}, clear=False), \
             patch("issacsimz_cli.cli.shutil.which", return_value="tmux"), \
             patch("issacsimz_cli.cli.subprocess.run", return_value=SimpleNamespace(returncode=0)):
            os.environ.pop("TMUX", None)
            with self.assertRaisesRegex(ValueError, "already exists"):
                launch_train_tmux(args)

    def test_launcher_requires_tmux(self) -> None:
        with patch("issacsimz_cli.cli.shutil.which", return_value=None):
            with self.assertRaisesRegex(FileNotFoundError, "tmux not found"):
                launch_train_tmux(self._args())

    def test_launcher_reuses_current_tmux_without_nesting(self) -> None:
        args = self._args()
        with patch.dict(os.environ, {"TMUX": "fixture"}, clear=False), \
             patch("issacsimz_cli.cli.shutil.which", return_value="tmux"), \
             patch("issacsimz_cli.cli.train", return_value=17) as train_run, \
             patch("issacsimz_cli.cli.subprocess.run") as tmux_run:
            self.assertEqual(launch_train_tmux(args), 17)
        self.assertFalse(args.tmux)
        train_run.assert_called_once_with(args)
        tmux_run.assert_not_called()

    def test_main_preserves_source_argv_for_tmux_launcher(self) -> None:
        with patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}, clear=False), \
             patch("issacsimz_cli.cli.launch_train_tmux", return_value=0) as launcher:
            self.assertEqual(main(["train", "h1", "--iters", "1", "--name", "x", "--tmux"]), 0)
        forwarded = launcher.call_args.args[0]
        self.assertEqual(forwarded._source_argv[-1], "--tmux")

    def test_main_rejects_train_without_mode_before_tmux_launch(self) -> None:
        with patch.dict(os.environ, {}, clear=True), \
             patch("issacsimz_cli.cli.launch_train_tmux") as launcher:
            self.assertEqual(main(["train", "h1", "--iters", "1", "--name", "x", "--tmux"]), 2)
        launcher.assert_not_called()


@unittest.skipIf(os.name == "nt", "Linux/WSL shell fixture")
class TmuxWrapperTests(unittest.TestCase):
    def _stub(self, folder: Path, name: str, body: str) -> None:
        path = folder / name
        path.write_text("#!/usr/bin/env bash\nset -eu\n" + body, encoding="utf-8")
        path.chmod(0o755)

    def test_wrapper_launches_entire_issacsimz_train_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base, bin_dir = Path(raw), Path(raw) / "bin"
            bin_dir.mkdir()
            calls = base / "tmux.calls"
            preflight_calls = base / "preflight.calls"
            evidence = base / "evidence"
            evidence.mkdir()
            state = base / "state.env"
            state.write_text(
                f'ISSACSIMZ_MODE=official\nISSACSIMZ_GO2_ROOT="{base / "go2"}"\n'
                f'ISSACSIMZ_ISAACLAB_ROOT="{base / "lab"}"\n'
                f'ISSACSIMZ_EVIDENCE_ROOT="{evidence}"\n'
                f'ISSACSIMZ_PYZ="{base / "issacsimz.pyz"}"\n', encoding="utf-8",
            )
            self._stub(bin_dir, "fake-python", f'printf "%s\\n" "$@" > "{preflight_calls}"\n')
            self._stub(bin_dir, "tmux", f'if [[ "$1" == has-session ]]; then exit 1; fi\nprintf "%s\\n" "$@" > "{calls}"\n')
            env = {**os.environ, "PATH": f"{bin_dir}:{os.environ['PATH']}",
                   "ISSACSIMZ_STATE_FILE": str(state), "ISSACSIMZ_PYTHON_RUNNER": str(bin_dir / "fake-python")}
            env.pop("TMUX", None)
            result = subprocess.run(
                ["bash", "scripts/issacsimz_tmux_train.sh", "go2", "--iters", "1000", "--envs", "4096", "--name", "go2: final run"],
                cwd=Path(__file__).resolve().parents[1], env=env, text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("issacsimz-go2-go2-final-run", result.stdout)
            command = calls.read_text(encoding="utf-8")
            self.assertIn("new-session", command)
            self.assertIn("issacsimz_train.sh", command)
            self.assertIn("--iters", command)
            self.assertIn("--envs", command)
            self.assertNotIn("--preflight-only", command)
            self.assertIn("--preflight-only", preflight_calls.read_text(encoding="utf-8"))
            custom = subprocess.run(
                ["bash", "scripts/issacsimz_tmux_train.sh", "go2", "--iters", "1000", "--name", "go2: final run",
                 "--tmux-session", "custom-session"],
                cwd=Path(__file__).resolve().parents[1], env=env, text=True, capture_output=True,
            )
            self.assertEqual(custom.returncode, 0, custom.stderr)
            self.assertIn("tmux session=custom-session", custom.stdout)

    def test_wrapper_rejects_preflight_only_without_starting_tmux(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base, bin_dir = Path(raw), Path(raw) / "bin"
            bin_dir.mkdir()
            calls = base / "tmux.calls"
            self._stub(bin_dir, "tmux", f'printf "%s\\n" "$@" > "{calls}"\nexit 1\n')
            env = {**os.environ, "PATH": f"{bin_dir}:{os.environ['PATH']}"}
            result = subprocess.run(
                ["bash", "scripts/issacsimz_tmux_train.sh", "go2", "--name", "x", "--preflight-only"],
                cwd=Path(__file__).resolve().parents[1], env=env, text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("without tmux", result.stderr)
            self.assertFalse(calls.exists())

    def test_personal_train_failure_preserves_archive_without_publishing(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base, bin_dir = Path(raw), Path(raw) / "bin"
            bin_dir.mkdir()
            evidence = base / "evidence"
            evidence.mkdir()
            archive = evidence / "failed_FAILED.tar.gz"
            archive.write_bytes(b"fixture")
            gh_calls = base / "gh.calls"
            self._stub(bin_dir, "gh", f'printf "%s\\n" "$*" >> "{gh_calls}"\n')
            self._stub(bin_dir, "fake-python", f'''printf '[issacsimz] archive={archive}\\n'
printf '[issacsimz] execution=FAILED exit=7 evidence_validation=PASS\\n'
exit 7
''')
            state = base / "state.env"
            state.write_text(
                f'ISSACSIMZ_MODE=personal\nISSACSIMZ_GO2_ROOT="{base / "go2"}"\n'
                f'ISSACSIMZ_ISAACLAB_ROOT="{base / "lab"}"\n'
                f'ISSACSIMZ_EVIDENCE_ROOT="{evidence}"\n'
                f'ISSACSIMZ_PYZ="{base / "issacsimz.pyz"}"\n', encoding="utf-8",
            )
            env = {**os.environ, "PATH": f"{bin_dir}:{os.environ['PATH']}",
                   "ISSACSIMZ_STATE_FILE": str(state), "ISSACSIMZ_PYTHON_RUNNER": str(bin_dir / "fake-python")}
            result = subprocess.run(
                ["bash", "scripts/issacsimz_train.sh", "go2", "--iters", "1", "--name", "failed"],
                cwd=Path(__file__).resolve().parents[1], env=env, text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 7)
            self.assertTrue(archive.is_file())
            self.assertFalse(gh_calls.exists())

    def test_release_asset_verifier_rejects_missing_remote_asset(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base, bin_dir = Path(raw), Path(raw) / "bin"
            bin_dir.mkdir()
            asset = base / "evidence.tar.gz"
            asset.write_bytes(b"fixture")
            self._stub(bin_dir, "gh", "echo 'unrelated.tar.gz\t7\tsha256:bad'\n")
            env = {**os.environ, "PATH": f"{bin_dir}:{os.environ['PATH']}"}
            result = subprocess.run(
                ["bash", "-c", f'source scripts/github_release_common.sh; issacsimz_verify_remote_assets owner/repo tag "{asset}"'],
                cwd=Path(__file__).resolve().parents[1], env=env, text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 20)
            self.assertIn("published asset is missing", result.stderr)

    def test_wrapper_rejects_existing_session(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            bin_dir = Path(raw) / "bin"
            bin_dir.mkdir()
            self._stub(bin_dir, "tmux", "exit 0\n")
            env = {**os.environ, "PATH": f"{bin_dir}:{os.environ['PATH']}"}
            result = subprocess.run(
                ["bash", "scripts/issacsimz_tmux_train.sh", "h1", "--iters", "1", "--name", "same"],
                cwd=Path(__file__).resolve().parents[1], env=env, text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("already exists", result.stderr)
