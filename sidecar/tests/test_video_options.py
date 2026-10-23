from __future__ import annotations

import json
import os
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from issacsimz_cli.cli import build_parser, play, train, video
from issacsimz_cli.artifacts import sha256_file, write_manifest
from issacsimz_cli.profiles import PROFILES


class VideoOptionTests(unittest.TestCase):
    def _official_train_run(self, log_root: Path, *, mode: str = "official",
                            validation: str = "PASS") -> Path:
        run = log_root / "runs" / "official-run"
        checkpoint = run / "collected" / "exported" / "model_best.pt"
        checkpoint.parent.mkdir(parents=True)
        checkpoint.write_bytes(b"official-checkpoint")
        (run / "metadata.json").write_text(json.dumps({
            "operation": "train", "profile": "go2", "mode": mode,
            "status": "completed", "training_status": "completed",
            "evidence_validation": validation,
            "native_run": "/workspace/training/quadruped/logs/rsl_rl/go2/native-run",
        }), encoding="utf-8")
        write_manifest(run)
        return run

    def _index_checkpoint(self, run: Path, checkpoint: Path, origin: str) -> None:
        (run / "checkpoint_index.json").write_text(json.dumps({
            "schema_version": 1,
            "run_id": run.name,
            "mode": "official",
            "checkpoints": [{
                "filename": checkpoint.name,
                "source_path": str(checkpoint.resolve()),
                "origin": origin,
                "size": checkpoint.stat().st_size,
                "sha256": sha256_file(checkpoint),
            }],
            "errors": [],
        }), encoding="utf-8")
        write_manifest(run)

    def _args(self, root: Path, *extra: str):
        run = root / "runs" / "train-run"
        checkpoint = run / "collected" / "exported" / "model_best.pt"
        checkpoint.parent.mkdir(parents=True)
        checkpoint.write_bytes(b"checkpoint")
        (run / "metadata.json").write_text(json.dumps({"operation": "train", "profile": "go2"}), encoding="utf-8")
        task = root / "training" / "quadruped"
        task.mkdir(parents=True)
        (task / "train.py").write_text("# fixture\n", encoding="utf-8")
        return build_parser().parse_args(["video", "go2", "--from-run", "train-run", "--log-root", str(root), "--task-root", str(task), *extra])

    def _import_args(self, base: Path, source: Path, robot: str = "go2", *extra: str):
        task, lab = base / "training" / robot, base / "IsaacLab"
        task.mkdir(parents=True)
        lab.mkdir(parents=True)
        (task / "train.py").write_text("# fixture\n", encoding="utf-8")
        args = build_parser().parse_args([
            "train", robot, "--name", "import-resume", "--iters", "5000",
            "--import-checkpoint", str(source), "--task-root", str(task),
            "--isaaclab-root", str(lab), "--log-root", str(base / "evidence"), *extra,
        ])
        return args, task, lab

    def test_official_import_resume_stages_native_checkpoint_with_unknown_lineage(self) -> None:
        for robot in ("h1", "go2"):
            with self.subTest(robot=robot), tempfile.TemporaryDirectory() as raw:
                base = Path(raw)
                source = base / "incoming" / "model_2700.pt"
                source.parent.mkdir()
                source_bytes = b"native-checkpoint-fixture"
                source.write_bytes(source_bytes)
                source_sha = sha256_file(source)
                args, task, lab = self._import_args(base, source, robot)
                with patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}, clear=False), \
                     patch("issacsimz_cli.cli.resolve_task_root", return_value=task), \
                     patch("issacsimz_cli.cli.resolve_isaaclab_launcher", return_value=lab / "isaaclab.sh"), \
                     patch("issacsimz_cli.cli.run_command", return_value=0) as execute, \
                     patch("issacsimz_cli.cli.ProfileLock"):
                    self.assertEqual(train(args), 0)

                forwarded = execute.call_args.args[0]
                native_root = task / PROFILES[robot].native_run_root
                expected_load_run = f"issacsimz-import-{source_sha[:16]}"
                staged = native_root / expected_load_run / source.name
                self.assertEqual(staged.read_bytes(), source_bytes)
                self.assertEqual(source.read_bytes(), source_bytes)
                self.assertIn("--resume", forwarded.command)
                self.assertEqual(forwarded.command[forwarded.command.index("--load_run") + 1], expected_load_run)
                self.assertEqual(
                    forwarded.command[forwarded.command.index("--checkpoint") + 1],
                    re.escape(source.name),
                )
                self.assertEqual(forwarded.source_checkpoint, str(source.resolve()))
                self.assertEqual(forwarded.source_checkpoint_sha256, source_sha)
                self.assertEqual(forwarded.source_checkpoint_origin, "user_imported_checkpoint")
                self.assertEqual(forwarded.source_run_mode, "unknown")
                self.assertFalse(forwarded.source_provenance_verified)
                self.assertIsNone(forwarded.source_evidence_run_id)
                self.assertIsNone(forwarded.parent_run_id)
                self.assertIsNone(forwarded.resume_lineage["parent_run_id"])
                self.assertFalse(forwarded.resume_lineage["source_provenance_verified"])
                self.assertEqual(forwarded.resume_lineage["start_iteration"], 2700)

    def test_official_import_preflight_does_not_stage_or_start_training(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw)
            source = base / "model_2700.pt"
            source.write_bytes(b"native-checkpoint-fixture")
            args, task, lab = self._import_args(base, source, "h1", "--preflight-only")
            native_root = task / PROFILES["h1"].native_run_root
            with patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}, clear=False), \
                 patch("issacsimz_cli.cli.resolve_task_root", return_value=task), \
                 patch("issacsimz_cli.cli.resolve_isaaclab_launcher", return_value=lab / "isaaclab.sh"), \
                 patch("issacsimz_cli.cli.run_command") as execute, \
                 patch("issacsimz_cli.cli.ProfileLock") as lock:
                self.assertEqual(train(args), 0)
            execute.assert_not_called()
            lock.assert_not_called()
            self.assertFalse(native_root.exists())
            self.assertEqual(source.read_bytes(), b"native-checkpoint-fixture")

    def test_import_resume_rejects_invalid_inputs_and_conflicting_sources(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw)
            args_by_case = []
            missing = base / "missing.pt"
            empty = base / "empty.pt"
            empty.write_bytes(b"")
            policy = base / "policy.pt"
            policy.write_bytes(b"torchscript-fixture")
            non_pt = base / "model_2700.bin"
            non_pt.write_bytes(b"checkpoint-fixture")
            args_by_case.extend((
                ("missing", missing, "regular native checkpoint"),
                ("empty", empty, "regular native checkpoint"),
                ("policy", policy, "native .pt checkpoint"),
                ("non_pt", non_pt, "native .pt checkpoint"),
            ))
            for label, source, expected in args_by_case:
                with self.subTest(case=label):
                    case_root = base / label
                    args, task, lab = self._import_args(case_root, source)
                    with patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}, clear=False), \
                         patch("issacsimz_cli.cli.resolve_task_root", return_value=task), \
                         patch("issacsimz_cli.cli.resolve_isaaclab_launcher", return_value=lab / "isaaclab.sh"), \
                         patch("issacsimz_cli.cli.run_command") as execute:
                        with self.assertRaisesRegex(ValueError, expected):
                            train(args)
                    execute.assert_not_called()

            valid = base / "model_2700.pt"
            valid.write_bytes(b"native-checkpoint-fixture")
            for extra in (("--from-run", "official-run"), ("--load-run", "native-run"),
                          ("--checkpoint", str(valid))):
                with self.subTest(conflict=extra[0]):
                    case_root = base / f"conflict-{extra[0][2:]}"
                    args, task, lab = self._import_args(case_root, valid, "go2", *extra)
                    with patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}, clear=False), \
                         patch("issacsimz_cli.cli.resolve_task_root", return_value=task), \
                         patch("issacsimz_cli.cli.resolve_isaaclab_launcher", return_value=lab / "isaaclab.sh"), \
                         patch("issacsimz_cli.cli.run_command") as execute:
                        with self.assertRaisesRegex(ValueError, "cannot be combined"):
                            train(args)
                    execute.assert_not_called()

    def test_official_import_rejects_destination_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw)
            source = base / "model_2700.pt"
            source.write_bytes(b"native-checkpoint-fixture")
            source_sha = sha256_file(source)

            args, task, lab = self._import_args(base / "symlink", source)
            native_root = task / PROFILES["go2"].native_run_root
            native_root.mkdir(parents=True)
            destination = native_root / f"issacsimz-import-{source_sha[:16]}"
            link_target = base / "link-target"
            link_target.mkdir()
            try:
                destination.symlink_to(link_target, target_is_directory=True)
            except OSError as exc:
                self.skipTest(f"directory symlinks unavailable: {exc}")
            with patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}, clear=False), \
                 patch("issacsimz_cli.cli.resolve_task_root", return_value=task), \
                 patch("issacsimz_cli.cli.resolve_isaaclab_launcher", return_value=lab / "isaaclab.sh"), \
                 patch("issacsimz_cli.cli.run_command") as execute:
                with self.assertRaisesRegex(ValueError, "not a regular directory"):
                    train(args)
            execute.assert_not_called()

    def test_official_import_sha_collision_does_not_overwrite_existing_checkpoint(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw)
            source = base / "model_2700.pt"
            source.write_bytes(b"native-checkpoint-fixture")
            source_sha = sha256_file(source)
            case_root = base / "collision"
            args, task, lab = self._import_args(case_root, source)
            native_root = task / PROFILES["go2"].native_run_root
            collision = native_root / f"issacsimz-import-{source_sha[:16]}"
            collision.mkdir(parents=True)
            existing = collision / source.name
            existing.write_bytes(b"different-checkpoint")
            with patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}, clear=False), \
                 patch("issacsimz_cli.cli.resolve_task_root", return_value=task), \
                 patch("issacsimz_cli.cli.resolve_isaaclab_launcher", return_value=lab / "isaaclab.sh"), \
                 patch("issacsimz_cli.cli.run_command") as execute, \
                 patch("issacsimz_cli.cli.ProfileLock"):
                with self.assertRaisesRegex(ValueError, "differs from imported source"):
                    train(args)
            execute.assert_not_called()
            self.assertEqual(existing.read_bytes(), b"different-checkpoint")

    def test_personal_import_resume_stages_native_checkpoint_with_unknown_lineage(self) -> None:
        for robot in ("h1", "go2"):
            with self.subTest(robot=robot), tempfile.TemporaryDirectory() as raw:
                base = Path(raw)
                source = base / "incoming" / "model_4950.pt"
                source.parent.mkdir()
                source_bytes = b"personal-native-checkpoint-fixture"
                source.write_bytes(source_bytes)
                source_sha = sha256_file(source)
                args, task, lab = self._import_args(base, source, robot)
                with patch.dict(os.environ, {"ISSACSIMZ_MODE": "personal"}, clear=False), \
                     patch("issacsimz_cli.cli.resolve_task_root", return_value=task), \
                     patch("issacsimz_cli.cli.resolve_isaaclab_launcher", return_value=lab / "isaaclab.sh"), \
                     patch("issacsimz_cli.cli.run_command", return_value=0) as execute, \
                     patch("issacsimz_cli.cli.ProfileLock"):
                    self.assertEqual(train(args), 0)

                forwarded = execute.call_args.args[0]
                expected_load_run = f"issacsimz-import-{source_sha[:16]}"
                staged = task / PROFILES[robot].native_run_root / expected_load_run / source.name
                self.assertEqual(staged.read_bytes(), source_bytes)
                self.assertEqual(source.read_bytes(), source_bytes)
                self.assertEqual(forwarded.command[forwarded.command.index("--load_run") + 1], expected_load_run)
                self.assertEqual(forwarded.command[forwarded.command.index("--checkpoint") + 1], re.escape(source.name))
                self.assertEqual(forwarded.source_checkpoint, str(source.resolve()))
                self.assertEqual(forwarded.source_checkpoint_sha256, source_sha)
                self.assertEqual(forwarded.source_checkpoint_origin, "user_imported_checkpoint")
                self.assertEqual(forwarded.source_run_mode, "unknown")
                self.assertFalse(forwarded.source_provenance_verified)
                self.assertIsNone(forwarded.parent_run_id)
                self.assertFalse(forwarded.resume_lineage["official_resume"])
                self.assertTrue(forwarded.resume_lineage["native_checkpoint_staged"])

    def test_imported_lineage_cannot_be_reused_as_verified_official_lineage(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw)
            source = base / "model_2700.pt"
            source.write_bytes(b"native-checkpoint-fixture")
            evidence = base / "evidence"
            run = self._official_train_run(evidence)
            metadata_path = run / "metadata.json"
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            metadata.update(
                source_checkpoint_origin="user_imported_checkpoint",
                source_run_mode="unknown",
                source_provenance_verified=False,
            )
            metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
            write_manifest(run)
            for command in (
                ["play", "go2", "--name", "blocked-play", "--from-run", run.name,
                 "--log-root", str(evidence)],
                ["train", "go2", "--name", "blocked-resume", "--iters", "5000",
                 "--from-run", run.name, "--checkpoint", str(source), "--log-root", str(evidence)],
            ):
                with self.subTest(command=command[0]), \
                     patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}, clear=False), \
                     patch("issacsimz_cli.cli.resolve_task_root", return_value=base / "task"), \
                     patch("issacsimz_cli.cli.resolve_isaaclab_launcher", return_value=base / "lab/isaaclab.sh"), \
                     patch("issacsimz_cli.cli.run_command") as execute:
                    with self.assertRaisesRegex(ValueError, "lineage is unverified after single-file import"):
                        if command[0] == "play":
                            play(build_parser().parse_args(command))
                        else:
                            train(build_parser().parse_args(command))
                    execute.assert_not_called()

    def test_video_defaults_to_twenty_seconds_and_enables_recording(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            args = self._args(Path(raw))
            with patch("issacsimz_cli.cli.play", return_value=0):
                self.assertEqual(video(args), 0)
            self.assertEqual(args.video_length, 1000)
            self.assertEqual(args.extra, ["--video", "--video_length", "1000", "--enable_cameras"])

    def test_video_length_can_be_explicitly_overridden(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            args = self._args(Path(raw), "--video-length", "250")
            with patch("issacsimz_cli.cli.play", return_value=0):
                self.assertEqual(video(args), 0)
            self.assertIn("250", args.extra)

    def test_video_label_is_metadata_only_and_names_the_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            args = self._args(Path(raw), "--label", "stairs")
            with patch("issacsimz_cli.cli.play", return_value=0):
                self.assertEqual(video(args), 0)
            self.assertEqual(args.video_label, "stairs")
            self.assertEqual(args.name, "train-run-video-stairs")
            self.assertNotIn("stairs", args.extra)

    def test_video_rejects_unknown_label(self) -> None:
        with self.assertRaises(SystemExit):
            build_parser().parse_args(["video", "go2", "--from-run", "run", "--label", "unknown"])

    def test_video_rejects_slope_label_from_another_profile(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            args = self._args(Path(raw), "--label", "slope_up_10deg")
            with self.assertRaisesRegex(ValueError, "does not match profile"):
                video(args)

    def test_video_length_must_be_positive(self) -> None:
        with self.assertRaises(SystemExit):
            build_parser().parse_args(["video", "go2", "--from-run", "run", "--video-length", "0"])

    def test_labeled_play_uses_video_evidence_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw)
            task, lab = base / "training" / "quadruped", base / "IsaacLab"
            task.mkdir(parents=True)
            lab.mkdir()
            (task / "train.py").write_text("# fixture\n", encoding="utf-8")
            (lab / ("isaaclab.bat" if os.name == "nt" else "isaaclab.sh")).write_text(
                "fixture\n", encoding="utf-8"
            )
            checkpoint = base / "model_4997.pt"
            checkpoint.write_bytes(b"checkpoint")
            (task / "exported").mkdir()
            (task / "exported" / "model_best.pt").write_bytes(b"canonical")
            args = build_parser().parse_args([
                "play", "go2", "--name", "suite-stairs", "--checkpoint", str(checkpoint),
                "--video-label", "stairs", "--handoff-run-id", "checkpoint-go2-model_4997-fixture",
                "--task-root", str(task), "--isaaclab-root", str(lab), "--log-root", str(base / "evidence"),
                "--extra", "--video", "--video_length", "1000", "--enable_cameras",
            ])
            with patch("issacsimz_cli.cli.run_command", return_value=0):
                self.assertEqual(play(args), 0)
            self.assertEqual(args.profile_operation, "video")
            self.assertEqual(args.parent_run_id, "checkpoint-go2-model_4997-fixture")
            self.assertTrue(args.fail_on_validation)
            self.assertEqual(args.video_label, "stairs")

    def test_labeled_play_requires_handoff_parent(self) -> None:
        args = build_parser().parse_args([
            "play", "go2", "--name", "missing-parent", "--checkpoint", "model.pt", "--video-label", "stairs",
        ])
        with self.assertRaisesRegex(ValueError, "handoff-run-id"):
            play(args)

    def test_official_play_allows_only_native_video_switches(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw)
            task, lab = base / "task", base / "lab"
            task.mkdir(); lab.mkdir()
            run = self._official_train_run(base / "evidence")
            checkpoint = run / "collected" / "exported" / "model_best.pt"
            (task / "exported").mkdir()
            (task / "exported" / "model_best.pt").write_bytes(b"canonical")
            args = build_parser().parse_args([
                "play", "go2", "--name", "blocked", "--from-run", "official-run",
                "--checkpoint", str(checkpoint), "--log-root", str(base / "evidence"),
                "--extra", "env.scene.terrain.num_rows=1",
            ])
            with patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}, clear=False), \
                 patch("issacsimz_cli.cli.resolve_task_root", return_value=task), \
                 patch("issacsimz_cli.cli.resolve_isaaclab_launcher", return_value=lab / "isaaclab.sh"):
                with self.assertRaisesRegex(ValueError, "arbitrary --extra is disabled"):
                    play(args)

            allowed = build_parser().parse_args([
                "play", "go2", "--name", "allowed", "--from-run", "official-run",
                "--checkpoint", str(checkpoint), "--log-root", str(base / "evidence"),
                "--extra", "--video", "--video_length", "1000", "--enable_cameras",
            ])
            with patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}, clear=False), \
                 patch("issacsimz_cli.cli.resolve_task_root", return_value=task), \
                 patch("issacsimz_cli.cli.resolve_isaaclab_launcher", return_value=lab / "isaaclab.sh"), \
                 patch("issacsimz_cli.cli.run_command", return_value=0):
                self.assertEqual(play(allowed), 0)

    def test_official_play_requires_official_train_lineage(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw)
            checkpoint = base / "model.pt"
            checkpoint.write_bytes(b"checkpoint")
            args = build_parser().parse_args([
                "play", "go2", "--name", "blocked", "--checkpoint", str(checkpoint),
            ])
            with patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}, clear=False), \
                 patch("issacsimz_cli.cli.resolve_task_root", return_value=base / "task"), \
                 patch("issacsimz_cli.cli.resolve_isaaclab_launcher", return_value=base / "lab/isaaclab.sh"):
                with self.assertRaisesRegex(ValueError, "requires --from-run"):
                    play(args)

    def test_official_video_rejects_personal_or_failed_train_evidence(self) -> None:
        for mode, validation, expected in (
            ("personal", "PASS", "mode=official"),
            ("official", "FAIL", "validation=FAIL"),
        ):
            with self.subTest(mode=mode, validation=validation), tempfile.TemporaryDirectory() as raw:
                base = Path(raw)
                self._official_train_run(base / "evidence", mode=mode, validation=validation)
                args = build_parser().parse_args([
                    "video", "go2", "--from-run", "official-run",
                    "--log-root", str(base / "evidence"),
                ])
                with patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}, clear=False):
                    with self.assertRaisesRegex(ValueError, expected):
                        video(args)

    def test_official_video_rejects_tampered_train_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw)
            run = self._official_train_run(base / "evidence")
            metadata = run / "metadata.json"
            metadata.write_text(metadata.read_text(encoding="utf-8") + "\n", encoding="utf-8")
            args = build_parser().parse_args([
                "video", "go2", "--from-run", "official-run",
                "--log-root", str(base / "evidence"),
            ])
            with patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}, clear=False):
                with self.assertRaisesRegex(ValueError, "metadata does not match"):
                    video(args)

    def test_official_play_allows_organizer_keeper_with_explicit_lineage(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw)
            task, lab = base / "task", base / "lab"
            task.mkdir(); lab.mkdir()
            source_run = self._official_train_run(base / "evidence")
            checkpoint = task / "backup_log" / "model_5000.pt"
            checkpoint.parent.mkdir()
            checkpoint.write_bytes(b"keeper-checkpoint")
            self._index_checkpoint(source_run, checkpoint, "organizer_keeper_backup")
            (task / "exported").mkdir()
            (task / "exported" / "model_best.pt").write_bytes(b"canonical")
            args = build_parser().parse_args([
                "play", "go2", "--name", "keeper", "--from-run", "official-run",
                "--checkpoint", str(checkpoint), "--log-root", str(base / "evidence"),
            ])
            with patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}, clear=False), \
                 patch("issacsimz_cli.cli.resolve_task_root", return_value=task), \
                 patch("issacsimz_cli.cli.resolve_isaaclab_launcher", return_value=lab / "isaaclab.sh"), \
                 patch("issacsimz_cli.cli.run_command", return_value=0) as run:
                self.assertEqual(play(args), 0)
            forwarded = run.call_args.args[0]
            self.assertTrue(forwarded.source_provenance_verified)
            self.assertEqual(forwarded.source_checkpoint_origin, "organizer_keeper_backup")
            self.assertEqual(forwarded.source_evidence_run_id, "official-run")
            self.assertEqual(forwarded.source_run_mode, "official")

    def test_official_play_rejects_unrelated_or_tampered_checkpoint(self) -> None:
        for case in ("unrelated", "tampered"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as raw:
                base = Path(raw)
                task, lab = base / "task", base / "lab"
                task.mkdir(); lab.mkdir()
                run = self._official_train_run(base / "evidence")
                evidence_checkpoint = run / "collected" / "exported" / "model_best.pt"
                if case == "unrelated":
                    checkpoint = base / "incoming" / "model_5000.pt"
                    checkpoint.parent.mkdir()
                    checkpoint.write_bytes(b"external")
                    expected = "checkpoint_index"
                else:
                    evidence_checkpoint.write_bytes(b"tampered")
                    checkpoint = evidence_checkpoint
                    expected = "does not match its evidence"
                args = build_parser().parse_args([
                    "play", "go2", "--name", case, "--from-run", "official-run",
                    "--checkpoint", str(checkpoint), "--log-root", str(base / "evidence"),
                ])
                with patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}, clear=False), \
                     patch("issacsimz_cli.cli.resolve_task_root", return_value=task), \
                     patch("issacsimz_cli.cli.resolve_isaaclab_launcher", return_value=lab / "isaaclab.sh"), \
                     patch("issacsimz_cli.cli.run_command") as execute:
                    with self.assertRaisesRegex(ValueError, expected):
                        play(args)
                execute.assert_not_called()

    def test_official_numbered_checkpoint_requires_indexed_sha(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw)
            task, lab = base / "task", base / "lab"
            task.mkdir(); lab.mkdir()
            run = self._official_train_run(base / "evidence")
            native = base / "native-run"
            native.mkdir()
            checkpoint = native / "model_5000.pt"
            checkpoint.write_bytes(b"indexed-checkpoint")
            metadata = json.loads((run / "metadata.json").read_text(encoding="utf-8"))
            metadata["native_run"] = str(native)
            (run / "metadata.json").write_text(json.dumps(metadata), encoding="utf-8")
            self._index_checkpoint(run, checkpoint, "official_native_run")
            (task / "exported").mkdir()
            (task / "exported" / "model_best.pt").write_bytes(b"canonical")

            args = build_parser().parse_args([
                "play", "go2", "--name", "indexed", "--from-run", "official-run",
                "--checkpoint", str(checkpoint), "--log-root", str(base / "evidence"),
            ])
            with patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}, clear=False), \
                 patch("issacsimz_cli.cli.resolve_task_root", return_value=task), \
                 patch("issacsimz_cli.cli.resolve_isaaclab_launcher", return_value=lab / "isaaclab.sh"), \
                 patch("issacsimz_cli.cli.run_command", return_value=0):
                self.assertEqual(play(args), 0)

            checkpoint.write_bytes(b"replaced-checkpoint")
            with patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}, clear=False), \
                 patch("issacsimz_cli.cli.resolve_task_root", return_value=task), \
                 patch("issacsimz_cli.cli.resolve_isaaclab_launcher", return_value=lab / "isaaclab.sh"), \
                 patch("issacsimz_cli.cli.run_command") as execute:
                with self.assertRaisesRegex(ValueError, "does not match"):
                    play(args)
            execute.assert_not_called()

    def test_official_numbered_play_requires_completed_source_run(self) -> None:
        for status in ("completed", "failed", "interrupted", None):
            for origin in ("official_native_run", "organizer_keeper_backup"):
                with self.subTest(status=status, origin=origin), tempfile.TemporaryDirectory() as raw:
                    base = Path(raw)
                    task, lab = base / "task", base / "lab"
                    task.mkdir(); lab.mkdir()
                    run = self._official_train_run(base / "evidence")
                    checkpoint = task / "backup_log" / "model_5000.pt"
                    checkpoint.parent.mkdir()
                    checkpoint.write_bytes(b"indexed-checkpoint")
                    metadata = json.loads((run / "metadata.json").read_text(encoding="utf-8"))
                    metadata.update(status=status, training_status=status)
                    (run / "metadata.json").write_text(json.dumps(metadata), encoding="utf-8")
                    self._index_checkpoint(run, checkpoint, origin)
                    (task / "exported").mkdir()
                    (task / "exported" / "model_best.pt").write_bytes(b"canonical")
                    args = build_parser().parse_args([
                        "play", "go2", "--name", "completion-guard", "--from-run", "official-run", "--checkpoint", str(checkpoint),
                        "--log-root", str(base / "evidence"),
                    ])
                    with patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}, clear=False), \
                         patch("issacsimz_cli.cli.resolve_task_root", return_value=task), \
                         patch("issacsimz_cli.cli.resolve_isaaclab_launcher", return_value=lab / "isaaclab.sh"), \
                         patch("issacsimz_cli.cli.run_command", return_value=0) as execute:
                        if status == "completed":
                            self.assertEqual(play(args), 0)
                            execute.assert_called_once()
                        else:
                            with self.assertRaisesRegex(ValueError, "completed source train run"):
                                play(args)
                            execute.assert_not_called()
                    self.assertEqual(checkpoint.read_bytes(), b"indexed-checkpoint")
                    self.assertEqual((task / "exported" / "model_best.pt").read_bytes(), b"canonical")

    def test_official_resume_requires_and_records_verified_lineage(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw)
            task, lab = base / "task", base / "lab"
            task.mkdir(); lab.mkdir()
            run = self._official_train_run(base / "evidence")
            native = task / "logs" / "rsl_rl" / "quadruped" / "native-run"
            native.mkdir(parents=True)
            checkpoint = native / "model_5000.pt"
            checkpoint.write_bytes(b"resume-checkpoint")
            metadata = json.loads((run / "metadata.json").read_text(encoding="utf-8"))
            metadata["native_run"] = str(native)
            (run / "metadata.json").write_text(json.dumps(metadata), encoding="utf-8")
            self._index_checkpoint(run, checkpoint, "official_native_run")

            common = [
                "train", "go2", "--name", "resume", "--iters", "6000", "--resume",
                "--load-run", native.name, "--checkpoint", str(checkpoint),
                "--log-root", str(base / "evidence"),
            ]
            missing = build_parser().parse_args(common)
            with patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}, clear=False), \
                 patch("issacsimz_cli.cli.resolve_task_root", return_value=task), \
                 patch("issacsimz_cli.cli.resolve_isaaclab_launcher", return_value=lab / "isaaclab.sh"):
                with self.assertRaisesRegex(ValueError, "requires --from-run"):
                    train(missing)

            args = build_parser().parse_args([*common, "--from-run", "official-run"])
            with patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}, clear=False), \
                 patch("issacsimz_cli.cli.resolve_task_root", return_value=task), \
                 patch("issacsimz_cli.cli.resolve_isaaclab_launcher", return_value=lab / "isaaclab.sh"), \
                 patch("issacsimz_cli.cli.run_command", return_value=0) as execute, \
                 patch("issacsimz_cli.cli.ProfileLock"):
                self.assertEqual(train(args), 0)
            forwarded = execute.call_args.args[0]
            self.assertTrue(forwarded.resume_lineage["official_resume"])
            self.assertTrue(forwarded.resume_lineage["source_provenance_verified"])
            self.assertEqual(forwarded.source_checkpoint_origin, "official_native_run")
            self.assertEqual(forwarded.command[forwarded.command.index("--checkpoint") + 1], "model_5000.pt")
            self.assertEqual(forwarded.command[forwarded.command.index("--load_run") + 1], native.name)

    def test_official_resume_restores_verified_keeper_checkpoint_for_native_loader(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw)
            task, lab = base / "task", base / "lab"
            native = task / "logs" / "rsl_rl" / "quadruped" / "native-run"
            native.mkdir(parents=True)
            lab.mkdir()
            run = self._official_train_run(base / "evidence")
            metadata = json.loads((run / "metadata.json").read_text(encoding="utf-8"))
            metadata["native_run"] = str(native)
            (run / "metadata.json").write_text(json.dumps(metadata), encoding="utf-8")
            keeper = task / "backup_log" / native.name / "model_2950.pt"
            keeper.parent.mkdir(parents=True)
            keeper.write_bytes(b"verified-keeper-checkpoint")
            self._index_checkpoint(run, keeper, "organizer_keeper_backup")
            args = build_parser().parse_args([
                "train", "go2", "--name", "resume", "--iters", "5000",
                "--from-run", run.name, "--checkpoint", str(keeper),
                "--log-root", str(base / "evidence"),
            ])
            with patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}, clear=False), \
                 patch("issacsimz_cli.cli.resolve_task_root", return_value=task), \
                 patch("issacsimz_cli.cli.resolve_isaaclab_launcher", return_value=lab / "isaaclab.sh"), \
                 patch("issacsimz_cli.cli.run_command", return_value=0) as execute, \
                 patch("issacsimz_cli.cli.ProfileLock"):
                self.assertEqual(train(args), 0)
            forwarded = execute.call_args.args[0]
            self.assertEqual(forwarded.command[forwarded.command.index("--load_run") + 1], native.name)
            self.assertEqual(forwarded.command[forwarded.command.index("--checkpoint") + 1], keeper.name)
            self.assertEqual(forwarded.source_checkpoint, str(keeper.resolve()))
            self.assertEqual(forwarded.source_checkpoint_origin, "organizer_keeper_backup")
            self.assertTrue(forwarded.resume_lineage["native_checkpoint_staged"])
            self.assertEqual((native / keeper.name).read_bytes(), keeper.read_bytes())

            (native / keeper.name).write_bytes(b"wrong-checkpoint")
            with patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}, clear=False), \
                 patch("issacsimz_cli.cli.resolve_task_root", return_value=task), \
                 patch("issacsimz_cli.cli.resolve_isaaclab_launcher", return_value=lab / "isaaclab.sh"), \
                 patch("issacsimz_cli.cli.run_command") as execute:
                with self.assertRaisesRegex(ValueError, "differs from indexed source"):
                    train(args)
            execute.assert_not_called()

    def test_official_resume_preflight_does_not_restore_or_start_training(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw)
            task, lab = base / "task", base / "lab"
            native = task / "logs" / "rsl_rl" / "quadruped" / "native-run"
            native.mkdir(parents=True)
            lab.mkdir()
            run = self._official_train_run(base / "evidence")
            metadata = json.loads((run / "metadata.json").read_text(encoding="utf-8"))
            metadata["native_run"] = str(native)
            (run / "metadata.json").write_text(json.dumps(metadata), encoding="utf-8")
            keeper = task / "backup_log" / native.name / "model_2950.pt"
            keeper.parent.mkdir(parents=True)
            keeper.write_bytes(b"verified-keeper-checkpoint")
            self._index_checkpoint(run, keeper, "organizer_keeper_backup")
            args = build_parser().parse_args([
                "train", "go2", "--name", "resume", "--iters", "5000",
                "--from-run", run.name, "--checkpoint", str(keeper),
                "--log-root", str(base / "evidence"), "--preflight-only",
            ])
            with patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}, clear=False), \
                 patch("issacsimz_cli.cli.resolve_task_root", return_value=task), \
                 patch("issacsimz_cli.cli.resolve_isaaclab_launcher", return_value=lab / "isaaclab.sh"), \
                 patch("issacsimz_cli.cli.run_command") as execute:
                self.assertEqual(train(args), 0)
            execute.assert_not_called()
            self.assertFalse((native / keeper.name).exists())

            export = run / "collected" / "exported" / "model_best.pt"
            args = build_parser().parse_args([
                "train", "go2", "--name", "resume", "--iters", "5000",
                "--from-run", run.name, "--checkpoint", str(export),
                "--log-root", str(base / "evidence"), "--preflight-only",
            ])
            with patch.dict(os.environ, {"ISSACSIMZ_MODE": "official"}, clear=False), \
                 patch("issacsimz_cli.cli.resolve_task_root", return_value=task), \
                 patch("issacsimz_cli.cli.resolve_isaaclab_launcher", return_value=lab / "isaaclab.sh"), \
                 patch("issacsimz_cli.cli.run_command") as execute:
                with self.assertRaisesRegex(ValueError, "requires a numbered checkpoint"):
                    train(args)
            execute.assert_not_called()
