from __future__ import annotations

import tempfile
import tarfile
import unittest
import sys
import os
import json
import subprocess
from types import SimpleNamespace
from pathlib import Path
from unittest.mock import Mock, patch

from issacsimz_cli.artifacts import VIDEO_LABELS, copy_download_handoff, download_handoff_root, sha256_file, write_manifest
from issacsimz_cli.checkpoints import CheckpointWatcher, parse_keep
from issacsimz_cli.cli import _environment_present, build_parser, doctor, main, play, train
from issacsimz_cli.core import _backup_line_status, _capture_source_identity, _checkpoint_index, _compare_source_identity, _finalize_line_state, _interrupt_then_wait, archive_run, verify_archive
from issacsimz_cli.profiles import resolve_isaaclab_launcher, resolve_task_root


class CoreTests(unittest.TestCase):
    def test_publishable_verify_requires_completed_pass_evidence(self) -> None:
        for status, validation, expected in (
            ("completed", "PASS", 0), ("failed", "PASS", 1),
            ("completed", "FAIL", 1), ("interrupted", "WARN", 1),
        ):
            with self.subTest(status=status, validation=validation), \
                 patch("issacsimz_cli.cli.verify_archive", return_value={
                     "ok": True, "errors": [], "metadata": {
                         "status": status, "evidence_validation": validation,
                     },
                 }):
                self.assertEqual(main(["verify", "fixture.tar.gz", "--publishable"]), expected)

    @unittest.skipIf(os.name == "nt", "bash launcher fixture")
    def test_launcher_uses_bootstrap_evidence_root_unless_overridden(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            state_root = base / "state-evidence"
            override_root = base / "override-evidence"
            (state_root / "runs" / "state-run").mkdir(parents=True)
            (override_root / "runs" / "override-run").mkdir(parents=True)
            state = base / "mode.env"
            state.write_text(
                f'ISSACSIMZ_MODE="official"\n'
                f'ISSACSIMZ_PYTHON_RUNNER="{sys.executable}"\n'
                f'ISSACSIMZ_EVIDENCE_ROOT="{state_root}"\n',
                encoding="utf-8",
            )
            env = {**os.environ, "ISSACSIMZ_STATE_FILE": str(state)}
            env.pop("ISSACSIMZ_LOG_ROOT", None)
            root = Path(__file__).resolve().parents[1]
            result = subprocess.run(
                ["bash", "issacsimz", "runs", "list"], cwd=root, env=env,
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)[0]["run_id"], "state-run")
            env["ISSACSIMZ_LOG_ROOT"] = str(override_root)
            overridden = subprocess.run(
                ["bash", "issacsimz", "runs", "list"], cwd=root, env=env,
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(overridden.returncode, 0, overridden.stderr)
            self.assertEqual(json.loads(overridden.stdout)[0]["run_id"], "override-run")

    def test_explicit_task_root_does_not_fall_back(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            fallback = base / "fallback"
            fallback.mkdir()
            (fallback / "train.py").write_text("# fixture", encoding="utf-8")
            with patch.dict(os.environ, {"ISSACSIMZ_GO2_ROOT": str(fallback)}, clear=False):
                with self.assertRaisesRegex(FileNotFoundError, "explicit --task-root is invalid"):
                    resolve_task_root("go2", str(base / "missing"))

    def test_explicit_isaaclab_root_does_not_fall_back(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            fallback = base / "fallback"
            fallback.mkdir()
            launcher = fallback / ("isaaclab.bat" if os.name == "nt" else "isaaclab.sh")
            launcher.write_text("fixture", encoding="utf-8")
            with patch.dict(os.environ, {"ISSACSIMZ_ISAACLAB_ROOT": str(fallback)}, clear=False):
                with self.assertRaisesRegex(FileNotFoundError, "explicit --isaaclab-root is invalid"):
                    resolve_isaaclab_launcher(str(base / "missing"))

    def test_download_handoff_default_roots_and_override(self) -> None:
        with patch.dict(os.environ, {"ISSACSIMZ_MODE": "personal"}, clear=True):
            self.assertEqual(download_handoff_root(Path("/ephemeral/task")), Path("/home/shadeform/ISSACSIMZ_DOWNLOAD"))
        with patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}, clear=True):
            self.assertEqual(download_handoff_root(Path("/workspace/training/go2")), Path("/workspace/ISSACSIMZ_DOWNLOAD"))
        with patch.dict(os.environ, {"ISSACSIMZ_DOWNLOAD_ROOT": "/tmp/issacsimz-download"}, clear=True):
            self.assertEqual(download_handoff_root(Path("/workspace/training/go2")), Path("/tmp/issacsimz-download"))

    def test_train_download_handoff_copies_only_final_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            evidence = base / "evidence" / "runs" / "run-1"
            exported = evidence / "collected" / "exported"
            exported.mkdir(parents=True)
            for name, content in (("model_best.pt", b"model"), ("env.yaml", b"env"), ("report.html", b"report")):
                (exported / name).write_bytes(content)
            (evidence / "console.log").write_text("canonical console", encoding="utf-8")
            archive = base / "evidence" / "exports" / "run-1.tar.gz"
            archive.parent.mkdir(parents=True)
            archive.write_bytes(b"archive")
            archive.with_suffix(archive.suffix + ".sha256").write_text(f"{sha256_file(archive)}  {archive.name}\n", encoding="utf-8")
            source_before = archive.read_bytes()
            with patch.dict(os.environ, {"ISSACSIMZ_DOWNLOAD_ROOT": str(base / "download")}, clear=True):
                handoff, errors = copy_download_handoff(evidence, task_root=base / "task", operation="train", archive=archive)
            assert handoff is not None
            self.assertEqual(errors, [])
            self.assertEqual((handoff / "LATEST.txt").exists(), False)
            self.assertEqual((handoff.parent / "LATEST.txt").read_text(encoding="utf-8"), "run-1\n")
            self.assertEqual(sha256_file(handoff / archive.name), sha256_file(archive))
            sidecar = archive.with_suffix(archive.suffix + ".sha256")
            self.assertEqual((handoff / sidecar.name).read_text(encoding="utf-8"), sidecar.read_text(encoding="utf-8"))
            bundle = handoff.parent / "run-1-download.tar.gz"
            bundle_sidecar = bundle.with_suffix(bundle.suffix + ".sha256")
            self.assertTrue(bundle.is_file())
            self.assertEqual(bundle_sidecar.read_text(encoding="utf-8"), f"{sha256_file(bundle)}  {bundle.name}\n")
            with tarfile.open(bundle, "r:gz") as packed:
                names = set(packed.getnames())
            self.assertTrue(all(name == "run-1" or name.startswith("run-1/") for name in names))
            self.assertIn("run-1/model_best.pt", names)
            self.assertNotIn("run-1/console.log", names)
            self.assertEqual(archive.read_bytes(), source_before)
            self.assertTrue((evidence / "console.log").is_file())
            self.assertFalse((handoff / "console.log").exists())

    def test_download_handoff_tolerates_missing_optional_files_and_links_video_to_train_run(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            train = base / "runs" / "train-run"
            (train / "collected" / "exported").mkdir(parents=True)
            (train / "collected" / "exported" / "model_best.pt").write_bytes(b"model")
            video = base / "runs" / "video-run"
            (video / "collected" / "exported").mkdir(parents=True)
            (video / "collected" / "exported" / "play_video.mp4").write_bytes(b"legacy-video")
            with patch.dict(os.environ, {"ISSACSIMZ_DOWNLOAD_ROOT": str(base / "download")}, clear=True):
                train_handoff, train_errors = copy_download_handoff(train, task_root=base / "task", operation="train")
                assert train_handoff is not None
                video_handoff, video_errors = copy_download_handoff(video, task_root=base / "task", operation="video", parent_run_id="train-run", validation="PASS")
                label_errors = []
                for label in VIDEO_LABELS:
                    labeled = base / "runs" / f"video-{label}"
                    exported = labeled / "collected" / "exported"
                    exported.mkdir(parents=True)
                    exported.joinpath("play_video.mp4").write_bytes(label.encode())
                    _, errors = copy_download_handoff(
                        labeled, task_root=base / "task", operation="video",
                        parent_run_id="train-run", validation="PASS", video_label=label,
                    )
                    label_errors.extend(errors)
            self.assertEqual(train_errors, [])
            self.assertEqual(video_errors, [])
            self.assertEqual(label_errors, [])
            self.assertEqual(train_handoff, video_handoff)
            assert train_handoff is not None
            self.assertTrue((train_handoff / "model_best.pt").is_file())
            self.assertEqual((train_handoff / "play_video.mp4").read_bytes(), b"legacy-video")
            for label in VIDEO_LABELS:
                self.assertEqual((train_handoff / "videos" / f"{label}.mp4").read_bytes(), label.encode())
            bundle = train_handoff.parent / "train-run-download.tar.gz"
            with tarfile.open(bundle, "r:gz") as packed:
                names = set(packed.getnames())
            self.assertTrue(all(name == "train-run" or name.startswith("train-run/") for name in names))
            self.assertIn("train-run/play_video.mp4", names)
            for label in VIDEO_LABELS:
                self.assertIn(f"train-run/videos/{label}.mp4", names)
            self.assertEqual(
                bundle.with_suffix(bundle.suffix + ".sha256").read_text(encoding="utf-8"),
                f"{sha256_file(bundle)}  {bundle.name}\n",
            )

    def test_parse_keep(self) -> None:
        self.assertEqual(parse_keep("1, 3,3"), {1, 3})
        with self.assertRaises(ValueError):
            parse_keep("")

    def test_watch_is_rejected_in_official_mode(self) -> None:
        with patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}, clear=False):
            self.assertEqual(main([
                "watch", "--run-dir", "unused", "--destination", "unused", "--all",
            ]), 2)

    def test_generic_run_is_rejected_in_official_mode(self) -> None:
        with patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}, clear=False), \
             patch("issacsimz_cli.cli.run_command") as run:
            self.assertEqual(main(["run", "--name", "blocked", "--", "echo", "no"]), 2)
        run.assert_not_called()

    def test_execution_commands_fail_closed_without_valid_mode(self) -> None:
        commands = (
            ["run", "--name", "blocked", "--", "echo", "no"],
            ["watch", "--run-dir", "unused", "--destination", "unused", "--all"],
            ["train", "h1", "--name", "blocked", "--iters", "1"],
            ["play", "h1", "--name", "blocked", "--checkpoint", "model.pt"],
            ["video", "h1", "--from-run", "blocked"],
        )
        for mode in (None, "invalid"):
            environment = {} if mode is None else {"ISSACSIMZ_MODE": mode}
            for command in commands:
                with self.subTest(mode=mode, action=command[0]), \
                     patch.dict(os.environ, environment, clear=True), \
                     patch("issacsimz_cli.cli.run_command") as execute:
                    self.assertEqual(main(command), 2)
                    execute.assert_not_called()

    def test_run_and_watch_require_personal_mode(self) -> None:
        for command in (
            ["run", "--name", "blocked", "--", "echo", "no"],
            ["watch", "--run-dir", "unused", "--destination", "unused", "--all"],
        ):
            with self.subTest(action=command[0]), \
                 patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}, clear=True), \
                 patch("issacsimz_cli.cli.run_command") as execute:
                self.assertEqual(main(command), 2)
                execute.assert_not_called()

    def test_official_train_rejects_extra_and_private_bypass_flags(self) -> None:
        blocked = (
            ["--extra", "env.foo=bar"],
            ["--allow-no-auto-submit"],
            ["--allow-submit-debug"],
        )
        for extra in blocked:
            with self.subTest(extra=extra), patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}, clear=False), \
                 patch("issacsimz_cli.cli.run_command") as run:
                self.assertEqual(main(["train", "h1", "--name", "blocked", "--iters", "1", *extra]), 2)
                run.assert_not_called()

    def test_official_profile_commands_reject_user_collect_but_personal_allows_it(self) -> None:
        official_commands = (
            ["train", "h1", "--name", "blocked", "--iters", "1", "--collect", "/tmp/foo"],
            ["play", "h1", "--name", "blocked", "--checkpoint", "model.pt", "--collect", "/tmp/foo"],
            ["video", "h1", "--from-run", "blocked", "--collect", "/tmp/foo"],
        )
        for command in official_commands:
            with self.subTest(action=command[0]), \
                 patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}, clear=True), \
                 patch("issacsimz_cli.cli.run_command") as execute:
                self.assertEqual(main(command), 2)
                execute.assert_not_called()
        with patch.dict(os.environ, {"ISSACSIMZ_MODE": "personal"}, clear=True), \
             patch("issacsimz_cli.cli.train", return_value=0) as execute:
            self.assertEqual(main([
                "train", "h1", "--name", "allowed", "--iters", "1", "--collect", "/tmp/foo",
            ]), 0)
            self.assertEqual(execute.call_args.args[0].collect, ["/tmp/foo"])

    def test_official_doctor_rejects_private_bypass_flags(self) -> None:
        for flag in ("--allow-no-auto-submit", "--allow-submit-debug"):
            with self.subTest(flag=flag), patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}, clear=False):
                self.assertEqual(main(["doctor", flag]), 2)

    def test_official_roots_are_fixed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary, \
             patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}, clear=True):
            with self.assertRaisesRegex(ValueError, "official --task-root override is disabled"):
                resolve_task_root("h1", temporary)
            with self.assertRaisesRegex(ValueError, "official --isaaclab-root override is disabled"):
                resolve_isaaclab_launcher(temporary)
        with tempfile.TemporaryDirectory() as temporary, \
             patch.dict(os.environ, {
                 "ISSACSIMZ_MODE": "official",
                 "ISSACSIMZ_H1_ROOT": temporary,
                 "ISSACSIMZ_ISAACLAB_ROOT": temporary,
             }, clear=True):
            with self.assertRaisesRegex(ValueError, "ISSACSIMZ_H1_ROOT override is disabled"):
                resolve_task_root("h1")
            with self.assertRaisesRegex(ValueError, "ISSACSIMZ_ISAACLAB_ROOT override is disabled"):
                resolve_isaaclab_launcher()

    def test_official_additional_interrupt_does_not_force_stop(self) -> None:
        process = SimpleNamespace(wait=Mock(side_effect=[KeyboardInterrupt(), 0]), poll=lambda: None)
        with patch("issacsimz_cli.core._send_sigint"), patch("issacsimz_cli.core._force_stop") as force:
            self.assertEqual(_interrupt_then_wait(process, allow_force_stop=False), (0, False))
        force.assert_not_called()

    def test_watcher_only_copies_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "runs"
            native = root / "native"
            native.mkdir(parents=True)
            source = native / "model_10.pt"
            source.write_bytes(b"checkpoint")
            destination = Path(temporary) / "mirror"
            watcher = CheckpointWatcher(root, destination, start_time=0, native_run=native)
            watcher.scan(final=True)
            self.assertTrue(source.is_file())
            self.assertEqual((destination / source.name).read_bytes(), b"checkpoint")

    def test_watcher_skips_hashing_unchanged_preserved_checkpoint(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "runs"
            native = root / "native"
            native.mkdir(parents=True)
            (native / "model_10.pt").write_bytes(b"checkpoint")
            watcher = CheckpointWatcher(root, Path(temporary) / "mirror", start_time=0, native_run=native)
            with patch("issacsimz_cli.checkpoints.sha256_file", wraps=sha256_file) as hashed:
                watcher.scan(final=True)
                first_scan_calls = hashed.call_count
                watcher.scan(final=True)
                self.assertEqual(hashed.call_count, first_scan_calls)

    def test_watcher_detects_only_directory_created_after_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "runs"
            (root / "old").mkdir(parents=True)
            watcher = CheckpointWatcher(root, Path(temporary) / "mirror", start_time=0)
            watcher.scan(final=True)
            self.assertIsNone(watcher.native_run)
            fresh = root / "fresh"
            fresh.mkdir()
            (fresh / "model_1.pt").write_bytes(b"checkpoint")
            watcher.scan(final=True)
            self.assertEqual(watcher.native_run, fresh)
            self.assertTrue((Path(temporary) / "mirror" / "model_1.pt").is_file())

    def test_archive_rejects_path_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(ValueError):
                archive_run(Path(temporary), "../../outside")

    def test_archive_rejects_insufficient_disk(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "runs" / "fixture"
            source.mkdir(parents=True)
            (source / "metadata.json").write_text('{"status":"completed"}\n', encoding="utf-8")
            (source / "payload.bin").write_bytes(b"payload")
            with patch("issacsimz_cli.core.shutil.disk_usage", return_value=SimpleNamespace(free=0)):
                with self.assertRaisesRegex(OSError, "insufficient free disk"):
                    archive_run(root, "fixture")

    def test_archive_preserves_finalized_evidence_bytes_and_copies_pack_sidecar(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            evidence = base / "runs" / "fixture"
            exported = evidence / "collected" / "exported"
            exported.mkdir(parents=True)
            (evidence / "metadata.json").write_text('{"status":"completed"}\n', encoding="utf-8")
            (exported / "model_best.pt").write_bytes(b"model")
            write_manifest(evidence)
            metadata_before = (evidence / "metadata.json").read_bytes()
            manifest_before = (evidence / "SHA256SUMS").read_bytes()
            archive, _ = archive_run(base, evidence.name)
            with tarfile.open(archive, "r:gz") as packed:
                archived_metadata = packed.extractfile(f"{evidence.name}/metadata.json")
                archived_manifest = packed.extractfile(f"{evidence.name}/SHA256SUMS")
                self.assertIsNotNone(archived_metadata)
                self.assertIsNotNone(archived_manifest)
                self.assertEqual(archived_metadata.read(), metadata_before)
                self.assertEqual(archived_manifest.read(), manifest_before)
            self.assertEqual((evidence / "metadata.json").read_bytes(), metadata_before)
            self.assertEqual((evidence / "SHA256SUMS").read_bytes(), manifest_before)
            with patch.dict(os.environ, {"ISSACSIMZ_DOWNLOAD_ROOT": str(base / "download")}, clear=True):
                handoff, errors = copy_download_handoff(
                    evidence, task_root=base / "task", operation="train",
                    archive=archive, validation="PASS",
                )
            self.assertEqual(errors, [])
            assert handoff is not None
            self.assertTrue((handoff / f"{archive.name}.metadata.json").is_file())

    def test_failed_validation_handoff_contains_evidence_archive_only(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            evidence = base / "runs" / "failed"
            exported = evidence / "collected" / "exported"
            exported.mkdir(parents=True)
            for name in ("model_best.pt", "env.yaml", "report.html"):
                (exported / name).write_bytes(b"not-for-handoff")
            (evidence / "metadata.json").write_text('{"status":"failed"}\n', encoding="utf-8")
            write_manifest(evidence)
            archive, _ = archive_run(base, evidence.name)
            with patch.dict(os.environ, {"ISSACSIMZ_DOWNLOAD_ROOT": str(base / "download")}, clear=True):
                handoff, errors = copy_download_handoff(
                    evidence, task_root=base / "task", operation="train",
                    archive=archive, validation="FAIL",
                )
            self.assertEqual(errors, [])
            assert handoff is not None
            self.assertTrue((handoff / archive.name).is_file())
            self.assertTrue((handoff / f"{archive.name}.sha256").is_file())
            self.assertTrue((handoff / f"{archive.name}.metadata.json").is_file())
            for name in ("model_best.pt", "env.yaml", "report.html"):
                self.assertFalse((handoff / name).exists())

    def test_checkpoint_index_rejects_symlink_and_empty_checkpoint(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            native, keeper = base / "native", base / "backup_log"
            native.mkdir(); keeper.mkdir()
            valid = native / "model_100.pt"
            valid.write_bytes(b"checkpoint")
            (native / "model_200.pt").touch()
            outside = base / "outside.pt"
            outside.write_bytes(b"outside")
            linked = native / "model_300.pt"
            try:
                linked.symlink_to(outside)
            except OSError:
                self.skipTest("symlinks unavailable")
            records, errors = _checkpoint_index({}, native, keeper)
            self.assertEqual([item["filename"] for item in records], ["model_100.pt"])
            self.assertTrue(any(item["path"].endswith("model_200.pt") for item in errors))

    def test_source_identity_fingerprints_full_python_tree_and_excludes_dynamic_dirs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            task = Path(temporary)
            required = ("train.py", "play.py", "humanoid_rewards.py", "pyproject.toml")
            for name in required:
                (task / name).write_text(f"# {name}\n", encoding="utf-8")
            package = task / "h1_task"
            package.mkdir()
            for name in ("_finalize.py", "env_cfg.py", "agent_cfg.py", "__init__.py", "helper.py"):
                (package / name).write_text(f"# {name}\n", encoding="utf-8")
            (task / "logs").mkdir()
            (task / "logs" / "ignored.py").write_text("ignored = True\n", encoding="utf-8")
            profile = SimpleNamespace(robot="h1", task_package="h1_task", reward_file="humanoid_rewards.py")
            identity = _capture_source_identity(task, profile, task / "identity-copy")
            paths = set(identity["hashed_paths"])
            self.assertIn("h1_task/helper.py", paths)
            self.assertNotIn("logs/ignored.py", paths)
            (package / "helper.py").write_text("changed = True\n", encoding="utf-8")
            compared = _compare_source_identity(identity, task, profile)
            self.assertTrue(compared["changed_during_run"])
            self.assertIn("h1_task/helper.py", compared["changed_paths"])

    def test_presence_semantics_and_profile_guards_include_zero(self) -> None:
        path = os.environ.get("PATH", "")
        for name in ("NO_AUTO_SUBMIT", "SUBMIT_DEBUG"):
            with self.subTest(name=name), patch.dict(os.environ, {"PATH": path, "ISSACSIMZ_MODE": "personal", name: "0"}, clear=True):
                self.assertTrue(_environment_present(name))
                self.assertEqual(main(["train", "h1", "--name", "guard", "--iters", "1"]), 2)

    def test_doctor_fail_has_nonzero_exit(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            with patch.dict(os.environ, {"PATH": os.environ.get("PATH", "")}, clear=True):
                self.assertEqual(doctor(base / "logs", True, "h1", str(base / "missing-task"), str(base / "missing-lab")), 1)

    def test_backup_status_parser(self) -> None:
        self.assertEqual(_backup_line_status("[backup] ✅ 백업 완료"), "success")
        self.assertEqual(_backup_line_status("[backup] NO_AUTO_SUBMIT 설정됨"), "skipped_disabled")
        self.assertEqual(_backup_line_status("[backup] model_best.pt/env.yaml 없음 — 자동 백업 skip"), "skipped_missing_artifacts")
        self.assertEqual(_backup_line_status("[backup] ⚠️ 연결 실패"), "failed")

    def test_finalize_status_parser(self) -> None:
        self.assertEqual(_finalize_line_state("[POST] 학습 종료 (exit=0)"), "started")
        self.assertEqual(_finalize_line_state("[DONE] 예선 제출 결과물 → exported/"), "completed")

    def test_run_always_archives_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "evidence"
            with patch.dict(os.environ, {"ISSACSIMZ_MODE": "personal"}, clear=False), \
                 patch("issacsimz_cli.core._backup_environment", return_value={
                     "submit_config_present": False,
                     "submit_host_present": False,
                     "submit_token_present": False,
                     "submit_credentials_present": False,
                 }), \
                 patch("builtins.print") as printed:
                code = main(["run", "--name", "failure", "--log-root", str(root), "--", sys.executable, "-c", "import sys; print('fixture'); sys.exit(7)"])
            self.assertEqual(code, 7)
            messages = [str(call.args[0]) for call in printed.call_args_list if call.args]
            self.assertIn("[issacsimz] execution=FAILED exit=7 evidence_validation=WARN", messages)
            metadata = next((root / "runs").glob("*/metadata.json"))
            self.assertIn('"status": "failed"', metadata.read_text(encoding="utf-8"))
            archive = next((root / "exports").glob("*.tar.gz"))
            self.assertEqual(len(sha256_file(archive)), 64)
            self.assertTrue(verify_archive(archive, require_sidecar=True)["ok"])

    def test_missing_native_run_is_explicit_warning(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            with patch.dict(os.environ, {"ISSACSIMZ_MODE": "personal"}, clear=False):
                code = main([
                    "run", "--name", "no-native", "--log-root", str(base / "evidence"),
                    "--run-root", str(base / "empty-runs"), "--no-pack", "--",
                    sys.executable, "-c", "print('done')",
                ])
            self.assertEqual(code, 0)
            metadata = next((base / "evidence" / "runs").glob("*/metadata.json")).read_text(encoding="utf-8")
            self.assertIn('"native_run_detected": false', metadata)
            self.assertIn('native run was not detected', metadata)

    def test_success_collects_native_run_and_checkpoint(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            logs, native_root, collected = base / "evidence", base / "native", base / "exported"
            collected.mkdir()
            (collected / "stale.txt").write_text("old")
            script = (
                "from pathlib import Path; import sys; "
                "run=Path(sys.argv[1])/'trial'; out=Path(sys.argv[2]); "
                "run.mkdir(parents=True); (run/'model_100.pt').write_bytes(b'checkpoint'); "
                "(run/'events.out.tfevents.fixture').write_text('event'); "
                "out.mkdir(parents=True, exist_ok=True); (out/'result.txt').write_text('result')"
            )
            with patch.dict(os.environ, {"ISSACSIMZ_MODE": "personal"}, clear=False):
                code = main([
                    "run", "--name", "success", "--log-root", str(logs),
                    "--run-root", str(native_root), "--collect", str(collected), "--",
                    sys.executable, "-c", script, str(native_root), str(collected),
                ])
            self.assertEqual(code, 0)
            evidence = next((logs / "runs").iterdir())
            self.assertTrue((evidence / "checkpoints" / "model_100.pt").is_file())
            self.assertTrue((evidence / "native_run" / "events.out.tfevents.fixture").is_file())
            self.assertTrue((evidence / "collected" / "exported" / "result.txt").is_file())
            self.assertFalse((evidence / "collected" / "exported" / "stale.txt").exists())
            self.assertIn('"status": "UNCHANGED"', (evidence / "collected" / "provenance.json").read_text(encoding="utf-8"))
            self.assertTrue((evidence / "SHA256SUMS").is_file())
            self.assertTrue(any((logs / "exports").glob("*.tar.gz")))

    def test_train_profile_uses_task_relative_native_run_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            task_root, lab_root = base / "training" / "humanoid", base / "IsaacLab"
            task_root.mkdir(parents=True)
            lab_root.mkdir()
            (task_root / "train.py").write_text("# fixture")
            launcher = lab_root / ("isaaclab.bat" if os.name == "nt" else "isaaclab.sh")
            launcher.write_text("fixture")
            args = build_parser().parse_args([
                "train", "h1", "--name", "profile", "--iters", "1",
                "--task-root", str(task_root), "--isaaclab-root", str(lab_root),
            ])
            with patch.dict(os.environ, {"ISSACSIMZ_MODE": "personal"}, clear=False), \
                 patch("issacsimz_cli.cli.run_command", return_value=0) as run:
                self.assertEqual(train(args), 0)
            forwarded = run.call_args.args[0]
            self.assertEqual(forwarded.workdir, str(task_root.resolve()))
            self.assertEqual(forwarded.run_root, str((task_root / "logs/rsl_rl/humanoid").resolve()))
            self.assertIn("Humanoid-v0", forwarded.command)
            self.assertEqual(forwarded.command[-1], "agent.save_interval=50")

    def test_play_uses_isolated_checkpoint_without_replacing_task_export(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            task_root, lab_root = base / "training" / "quadruped", base / "IsaacLab"
            task_root.mkdir(parents=True)
            lab_root.mkdir()
            (task_root / "train.py").write_text("# fixture", encoding="utf-8")
            launcher = lab_root / ("isaaclab.bat" if os.name == "nt" else "isaaclab.sh")
            launcher.write_text("fixture", encoding="utf-8")
            source = base / "incoming" / "model_4800.pt"
            source.parent.mkdir()
            source.write_bytes(b"source-checkpoint")
            target = task_root / "exported" / "model_best.pt"
            target.parent.mkdir()
            target.write_bytes(b"previous-task-checkpoint")
            args = build_parser().parse_args([
                "play", "go2", "--name", "arbitrary", "--checkpoint", str(source),
                "--task-root", str(task_root), "--isaaclab-root", str(lab_root),
                "--log-root", str(base / "evidence"),
            ])

            def inspect_staged(forwarded):
                execution = Path(forwarded.command[forwarded.command.index("--checkpoint") + 1])
                self.assertNotEqual(execution, target.resolve())
                self.assertEqual(execution.read_bytes(), source.read_bytes())
                self.assertEqual(target.read_bytes(), b"previous-task-checkpoint")
                self.assertEqual(forwarded.source_checkpoint, str(source.resolve()))
                self.assertEqual(forwarded.source_checkpoint_sha256, sha256_file(source))
                self.assertEqual(forwarded.native_output_roots, {
                    "exported": str(task_root / "exported"),
                    "videos": str(task_root / "videos"),
                    "isolated_checkpoint": str(execution.parent),
                })
                (execution.parent / "exported").mkdir()
                (execution.parent / "exported" / "policy.pt").write_bytes(b"fresh-policy")
                (execution.parent / "videos" / "play").mkdir(parents=True)
                (execution.parent / "videos" / "play" / "clip.mp4").write_bytes(b"fresh-video")
                forwarded._post_run()
                self.assertEqual(
                    forwarded.prepared_checkpoint["promoted_outputs"],
                    ["policy.pt", "play_video.mp4"],
                )
                self.assertEqual((target.parent / "policy.pt").read_bytes(), b"fresh-policy")
                self.assertEqual((target.parent / "play_video.mp4").read_bytes(), b"fresh-video")
                return 0

            with patch("issacsimz_cli.cli.run_command", side_effect=inspect_staged):
                self.assertEqual(play(args), 0)
            self.assertEqual(source.read_bytes(), b"source-checkpoint")
            self.assertEqual(target.read_bytes(), b"previous-task-checkpoint")

    def test_play_refuses_to_create_missing_canonical_checkpoint(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            task_root, lab_root = base / "training" / "quadruped", base / "IsaacLab"
            task_root.mkdir(parents=True)
            lab_root.mkdir()
            (task_root / "train.py").write_text("# fixture", encoding="utf-8")
            (lab_root / ("isaaclab.bat" if os.name == "nt" else "isaaclab.sh")).write_text("fixture", encoding="utf-8")
            source = base / "model.pt"
            source.write_bytes(b"source")
            target = task_root / "exported" / "model_best.pt"
            args = build_parser().parse_args([
                "play", "go2", "--name", "temporary", "--checkpoint", str(source),
                "--task-root", str(task_root), "--isaaclab-root", str(lab_root),
                "--log-root", str(base / "evidence"),
            ])
            with patch("issacsimz_cli.cli.run_command") as run:
                with self.assertRaisesRegex(FileNotFoundError, "refusing to create or replace"):
                    play(args)
            run.assert_not_called()
            self.assertFalse(target.exists())

    def test_personal_resume_forwards_native_arguments_and_records_lineage(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            task_root, lab_root = base / "training" / "humanoid", base / "IsaacLab"
            parent = task_root / "logs" / "rsl_rl" / "humanoid" / "parent-run"
            parent.mkdir(parents=True)
            checkpoint = parent / "model_500.pt"
            checkpoint.write_bytes(b"official-checkpoint")
            lab_root.mkdir()
            (task_root / "train.py").write_text("# fixture", encoding="utf-8")
            (lab_root / "isaaclab.sh").write_text("fixture", encoding="utf-8")
            args = build_parser().parse_args([
                "train", "h1", "--name", "resume", "--iters", "1000", "--resume",
                "--load-run", "parent-run", "--checkpoint", "model_500.pt",
                "--task-root", str(task_root), "--isaaclab-root", str(lab_root),
            ])
            with patch.dict(os.environ, {"ISSACSIMZ_MODE": "personal"}, clear=False), \
                 patch("issacsimz_cli.cli.resolve_task_root", return_value=task_root.resolve()), \
                 patch("issacsimz_cli.cli.resolve_isaaclab_launcher", return_value=(lab_root / "isaaclab.sh").resolve()), \
                 patch("issacsimz_cli.cli.run_command", return_value=0) as run:
                self.assertEqual(train(args), 0)
            forwarded = run.call_args.args[0]
            self.assertIn("--resume", forwarded.command)
            self.assertIn("--load_run", forwarded.command)
            self.assertIn("--checkpoint", forwarded.command)
            self.assertEqual(forwarded.parent_run_id, "parent-run")
            self.assertEqual(forwarded.source_checkpoint, str(checkpoint.resolve()))
            self.assertEqual(forwarded.source_checkpoint_sha256, sha256_file(checkpoint))
            self.assertEqual(forwarded.resume_lineage["start_iteration"], 500)
            self.assertEqual(forwarded.resume_lineage["requested_max_iterations"], 1000)
            self.assertFalse(forwarded.resume_lineage["official_resume"])


if __name__ == "__main__":
    unittest.main()
