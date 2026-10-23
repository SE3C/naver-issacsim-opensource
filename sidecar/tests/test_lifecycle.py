from __future__ import annotations

import json
import os
import select
import signal
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import unittest
from contextlib import ExitStack
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from issacsimz_cli.cli import main
from issacsimz_cli.artifacts import sha256_file
from issacsimz_cli.core import archive_run, verify_archive
from issacsimz_cli.profiles import PROFILES
from issacsimz_cli.safety import ProfileLock


@unittest.skipIf(os.name == "nt", "Linux/WSL lifecycle fixture")
class LifecycleTests(unittest.TestCase):
    def _workspace(self, base: Path) -> tuple[Path, Path]:
        task = base / "training" / "humanoid"
        lab = base / "IsaacLab"
        package = task / "h1_task"
        package.mkdir(parents=True)
        lab.mkdir()
        shutil.copy2(Path(__file__).parent / "fixtures" / "fake_train.py", task / "train.py")
        shutil.copy2(Path(__file__).parent / "fixtures" / "fake_play.py", task / "play.py")
        for name in ("humanoid_rewards.py", "pyproject.toml"):
            (task / name).write_text(f"# {name}\n", encoding="utf-8")
        for name in ("_finalize.py", "env_cfg.py", "agent_cfg.py", "__init__.py"):
            (package / name).write_text(f"# {name}\n", encoding="utf-8")
        (task / "logs" / "rsl_rl" / "humanoid").mkdir(parents=True)
        launcher = lab / "isaaclab.sh"
        launcher.write_text(
            "#!/usr/bin/env bash\n"
            "script=$2\n"
            "shift 2\n"
            f"exec {sys.executable} $script $@\n",
            encoding="utf-8",
        )
        launcher.chmod(0o755)
        return task, lab

    def _run(self, base: Path, scenario: str, *, credentials: bool = True,
             mode: str = "personal") -> tuple[int, Path, Path]:
        task, lab = self._workspace(base)
        exported = task / "exported"
        exported.mkdir(exist_ok=True)
        (exported / "submit_config.txt").write_text("token=SUPER_SECRET_DO_NOT_RECORD", encoding="utf-8")
        if scenario == "stale_exports":
            (exported / "model_best.pt").write_bytes(b"stale")
            (exported / "env.yaml").write_text("stale: true", encoding="utf-8")
        logs, locks = base / "evidence", base / "locks"
        environment = {"PATH": os.environ.get("PATH", ""), "ISSACSIMZ_FIXTURE_SCENARIO": scenario,
                       "ISSACSIMZ_MODE": mode,
                       "ISSACSIMZ_DOWNLOAD_ROOT": str(base / "download")}
        if credentials:
            environment.update({"SUBMIT_HOST": "https://secret.invalid", "SUBMIT_TOKEN": "SUPER_SECRET_DO_NOT_RECORD"})
        with ExitStack() as stack:
            stack.enter_context(patch.dict(os.environ, environment, clear=True))
            if mode == "official":
                stack.enter_context(patch.dict(PROFILES, {"h1": replace(PROFILES["h1"], default_root=task.resolve())}))
                stack.enter_context(patch("issacsimz_cli.profiles.OFFICIAL_ISAACLAB_ROOT", lab.resolve()))
            poll_seconds = "10" if scenario == "cleanup_race" else "0.01"
            code = main([
                "train", "h1", "--iters", "1", "--name", scenario,
                "--task-root", str(task), "--isaaclab-root", str(lab),
                "--log-root", str(logs), "--lock-root", str(locks),
                "--poll-seconds", poll_seconds, "--gpu-interval", "0.05",
            ])
        evidence = next((logs / "runs").iterdir())
        return code, evidence, logs

    def _spawn_interrupt_run(self, base: Path, scenario: str) -> tuple[subprocess.Popen[str], str, Path]:
        task, lab = self._workspace(base)
        logs, locks = base / "evidence", base / "locks"
        environment = os.environ.copy()
        for name in ("NO_AUTO_SUBMIT", "SUBMIT_DEBUG", "SUBMIT_HOST", "SUBMIT_TOKEN"):
            environment.pop(name, None)
        environment["ISSACSIMZ_FIXTURE_SCENARIO"] = scenario
        environment["ISSACSIMZ_DOWNLOAD_ROOT"] = str(base / "download")
        environment["ISSACSIMZ_MODE"] = "personal"
        repository = Path(__file__).resolve().parents[1]
        environment["PYTHONPATH"] = str(repository)
        command = [
            sys.executable, "-m", "issacsimz_cli", "train", "h1",
            "--iters", "1", "--name", scenario,
            "--task-root", str(task), "--isaaclab-root", str(lab),
            "--log-root", str(logs), "--lock-root", str(locks),
            "--poll-seconds", "0.01", "--gpu-interval", "0.05",
        ]
        process = subprocess.Popen(
            command, cwd=repository, env=environment,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
        )
        assert process.stdout is not None
        output = ""
        deadline = time.monotonic() + 10
        while "[fixture] training" not in output:
            if time.monotonic() >= deadline:
                process.kill()
                self.fail(f"fixture did not start; output={output!r}")
            ready, _, _ = select.select([process.stdout], [], [], 0.2)
            if ready:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    self.fail(f"fixture exited before signal; output={output!r}")
                output += line
        return process, output, logs

    def test_success_lifecycle_and_secret_exclusion(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            code, evidence, logs = self._run(base, "cleanup_race")
            self.assertEqual(code, 0)
            metadata = json.loads((evidence / "metadata.json").read_text(encoding="utf-8"))
            self.assertEqual(metadata["official_finalize_status"], "completed")
            self.assertEqual(metadata["official_backup_status"], "success")
            self.assertEqual(metadata["evidence_validation"], "PASS")
            self.assertIn("agent.save_interval=50", metadata["command"])
            self.assertGreaterEqual(metadata["checkpoint_count"], 1)
            self.assertTrue(metadata["gpu_monitor_enabled"])
            self.assertTrue(metadata["checkpoint_mirror_enabled"])
            self.assertTrue((evidence / "system" / "nvidia_smi_during.csv").is_file())
            self.assertTrue((evidence / "watcher.log").is_file())
            self.assertFalse(any((evidence / "native_run").rglob("model_*.pt")))
            self.assertFalse((evidence / "collected" / "exported" / "submit_config.txt").exists())
            archive = next((logs / "exports").glob("*.tar.gz"))
            self.assertTrue(verify_archive(archive, require_sidecar=True)["ok"])
            handoff = base / "download" / evidence.name
            self.assertEqual(sha256_file(handoff / archive.name), sha256_file(archive))
            self.assertTrue((handoff / "model_best.pt").is_file())
            self.assertTrue((handoff / "env.yaml").is_file())
            self.assertEqual((handoff.parent / "LATEST.txt").read_text(encoding="utf-8"), f"{evidence.name}\n")
            with tarfile.open(archive, "r:gz") as bundle:
                for member in bundle.getmembers():
                    if member.isfile():
                        stream = bundle.extractfile(member)
                        self.assertNotIn(b"SUPER_SECRET_DO_NOT_RECORD", stream.read() if stream else b"")

    def test_official_train_uses_one_shot_native_collection_without_monitors(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            code, evidence, logs = self._run(base, "success", mode="official")
            self.assertEqual(code, 0)
            metadata = json.loads((evidence / "metadata.json").read_text(encoding="utf-8"))
            self.assertEqual(metadata["mode"], "official")
            self.assertFalse(metadata["gpu_monitor_enabled"])
            self.assertFalse(metadata["checkpoint_mirror_enabled"])
            self.assertEqual(metadata["checkpoint_count"], 2)
            self.assertIn("agent.save_interval=50", metadata["command"])
            self.assertEqual(metadata["organizer_keeper"]["exit_code"], 0)
            self.assertEqual(metadata["organizer_checkpoint_count"], 2)
            self.assertEqual(
                {path.name for path in (evidence / "organizer_checkpoints").glob("model_*.pt")},
                {"model_100.pt", "model_200.pt"},
            )
            self.assertTrue(metadata["native_run_detected"])
            self.assertTrue(any((evidence / "native_run").rglob("events.out.tfevents*")))
            checkpoint_index = json.loads((evidence / "checkpoint_index.json").read_text(encoding="utf-8"))
            self.assertEqual(checkpoint_index["mode"], "official")
            self.assertEqual(
                {item["filename"] for item in checkpoint_index["checkpoints"]},
                {"model_100.pt", "model_200.pt"},
            )
            self.assertEqual(
                {item["origin"] for item in checkpoint_index["checkpoints"]},
                {"official_native_run", "organizer_keeper_backup"},
            )
            self.assertTrue(all(len(item["sha256"]) == 64
                                for item in checkpoint_index["checkpoints"]))
            self.assertEqual(metadata["checkpoint_index_count"], 4)
            self.assertFalse((evidence / "checkpoints").exists())
            self.assertFalse((evidence / "watcher.log").exists())
            self.assertFalse((evidence / "system" / "nvidia_smi_during.csv").exists())
            self.assertTrue((evidence / "system" / "nvidia_smi_before.txt").is_file())
            self.assertTrue((evidence / "system" / "nvidia_smi_after.txt").is_file())
            validation = json.loads((evidence / "validation.json").read_text(encoding="utf-8"))
            self.assertEqual(validation["overall"], "PASS")
            self.assertNotIn("checkpoints", {item["name"] for item in validation["checks"]})
            archive = next((logs / "exports").glob("*.tar.gz"))
            self.assertTrue(verify_archive(archive, require_sidecar=True)["ok"])
            with tarfile.open(archive, "r:gz") as bundle:
                self.assertTrue(any(member.name.endswith("organizer_checkpoints/model_200.pt")
                                    for member in bundle.getmembers()))
            download_bundle = base / "download" / f"{evidence.name}-download.tar.gz"
            self.assertTrue(download_bundle.is_file())
            with tarfile.open(download_bundle, "r:gz") as bundle:
                self.assertTrue(any(member.name.endswith(archive.name)
                                    for member in bundle.getmembers()))

    def test_failed_official_train_still_archives_preserved_checkpoint(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            code, evidence, logs = self._run(base, "exit1", mode="official")
            self.assertEqual(code, 1)
            self.assertEqual((evidence / "organizer_checkpoints" / "model_100.pt").read_bytes(), b"checkpoint-100")
            archive = next((logs / "exports").glob("*_FAILED.tar.gz"))
            self.assertTrue(verify_archive(archive, require_sidecar=True)["ok"])
            with tarfile.open(archive, "r:gz") as bundle:
                self.assertTrue(any(member.name.endswith("organizer_checkpoints/model_100.pt")
                                    for member in bundle.getmembers()))
            self.assertTrue((base / "download" / f"{evidence.name}-download.tar.gz").is_file())

    def test_failed_backup_and_missing_artifacts_fail_validation(self) -> None:
        for scenario in ("backup_failed", "missing_artifacts"):
            with self.subTest(scenario=scenario), tempfile.TemporaryDirectory() as temporary:
                code, evidence, _ = self._run(Path(temporary), scenario)
                self.assertEqual(code, 0)
                metadata = json.loads((evidence / "metadata.json").read_text(encoding="utf-8"))
                expected = "failed" if scenario == "backup_failed" else "skipped_missing_artifacts"
                self.assertEqual(metadata["official_backup_status"], expected)
                self.assertEqual(metadata["evidence_validation"], "FAIL")

    def test_missing_backup_config_is_explicit_and_not_expected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            code, evidence, _ = self._run(Path(temporary), "no_config", credentials=False)
            self.assertEqual(code, 0)
            metadata = json.loads((evidence / "metadata.json").read_text(encoding="utf-8"))
            self.assertEqual(metadata["official_backup_status"], "skipped_no_config")
            self.assertFalse(metadata["official_backup_expected"])
            self.assertEqual(metadata["official_backup_environment"], {
                "submit_config_present": False,
                "submit_host_present": False,
                "submit_token_present": False,
                "submit_credentials_present": False,
            })

    def test_finalize_incomplete_and_failed_archive_suffix(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            code, evidence, logs = self._run(Path(temporary), "finalize_incomplete")
            self.assertEqual(code, 1)
            metadata = json.loads((evidence / "metadata.json").read_text(encoding="utf-8"))
            self.assertEqual(metadata["official_finalize_status"], "incomplete")
            self.assertTrue(any((logs / "exports").glob("*_FAILED.tar.gz")))

    def test_stale_export_and_source_change_fail_validation(self) -> None:
        for scenario in ("stale_exports", "source_change"):
            with self.subTest(scenario=scenario), tempfile.TemporaryDirectory() as temporary:
                base = Path(temporary)
                code, evidence, _ = self._run(base, scenario)
                self.assertEqual(code, 0)
                metadata = json.loads((evidence / "metadata.json").read_text(encoding="utf-8"))
                self.assertEqual(metadata["evidence_validation"], "FAIL")

    def test_live_and_stale_profile_locks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with ProfileLock("go2", lock_root=root):
                with self.assertRaises(ValueError):
                    ProfileLock("go2", lock_root=root).acquire()
            stale = root / "h1.lock"
            stale.write_text('{"pid": 99999999}', encoding="utf-8")
            with self.assertRaises(ValueError):
                ProfileLock("h1", lock_root=root).acquire()
            with ProfileLock("h1", lock_root=root, force_unlock=True):
                self.assertTrue(stale.exists())
            self.assertFalse(stale.exists())

    def test_archive_overwrite_requires_force(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            code, evidence, logs = self._run(Path(temporary), "success")
            self.assertEqual(code, 0)
            with self.assertRaises(FileExistsError):
                archive_run(logs, evidence.name)
            archive_run(logs, evidence.name, force=True)

    def test_ctrl_c_waits_for_finalize_without_automatic_timeout(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            process, output, logs = self._spawn_interrupt_run(Path(temporary), "wait_for_interrupt")
            process.send_signal(signal.SIGINT)
            tail, _ = process.communicate(timeout=15)
            output += tail
            evidence = next((logs / "runs").iterdir())
            metadata = json.loads((evidence / "metadata.json").read_text(encoding="utf-8"))
            self.assertEqual(metadata["status"], "interrupted")
            self.assertFalse(metadata["forced_stop"])
            self.assertEqual(metadata["official_finalize_status"], "completed")
            self.assertEqual(metadata["official_backup_status"], "skipped_no_config")
            self.assertIn("waiting for train.py finalize/official backup", output)
            self.assertTrue(any((logs / "exports").glob("*_INTERRUPTED.tar.gz")))

    def test_second_ctrl_c_force_stop_is_recorded(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            process, output, logs = self._spawn_interrupt_run(Path(temporary), "wait_for_force")
            process.send_signal(signal.SIGINT)
            time.sleep(0.3)
            process.send_signal(signal.SIGINT)
            tail, _ = process.communicate(timeout=20)
            output += tail
            evidence = next((logs / "runs").iterdir())
            metadata = json.loads((evidence / "metadata.json").read_text(encoding="utf-8"))
            self.assertEqual(metadata["status"], "interrupted")
            self.assertTrue(metadata["forced_stop"])
            self.assertEqual(metadata["official_finalize_status"], "incomplete")
            self.assertIn("second Ctrl+C: force stopping process group", output)
            self.assertTrue(any((logs / "exports").glob("*_INTERRUPTED.tar.gz")))

    def _video(self, base: Path, scenario: str = "success", extra: list[str] | None = None,
               mode: str = "personal") -> tuple[int, Path, Path, Path]:
        _, train_evidence, logs = self._run(base, "success", mode=mode)
        task, lab = base / "training" / "humanoid", base / "IsaacLab"
        if scenario == "stale":
            exported = task / "exported"
            (exported / "policy.pt").write_bytes(b"policy-stale")
            (exported / "play_video.mp4").write_bytes(b"video-stale")
        environment = {
            "PATH": os.environ.get("PATH", ""), "ISSACSIMZ_PLAY_SCENARIO": scenario,
            "ISSACSIMZ_DOWNLOAD_ROOT": str(base / "download"), "ISSACSIMZ_MODE": mode,
        }
        with ExitStack() as stack:
            stack.enter_context(patch.dict(os.environ, environment, clear=True))
            if mode == "official":
                stack.enter_context(patch.dict(
                    PROFILES, {"h1": replace(PROFILES["h1"], default_root=task.resolve())}
                ))
                stack.enter_context(patch("issacsimz_cli.profiles.OFFICIAL_ISAACLAB_ROOT", lab.resolve()))
            command = [
                "video", "h1", "--from-run", train_evidence.name,
                "--task-root", str(task), "--isaaclab-root", str(lab),
                "--log-root", str(logs), "--poll-seconds", "0.01", "--gpu-interval", "0.05",
            ]
            if extra:
                command += extra
            code = main(command)
        video_evidence = next(path for path in (logs / "runs").iterdir() if path != train_evidence)
        return code, train_evidence, video_evidence, logs

    def test_video_uses_train_model_best_with_manifest_and_archive(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            code, train_evidence, evidence, logs = self._video(base, extra=["--extra", 'env.viewer.eye="[1.0,2.0,3.0]"'])
            self.assertEqual(code, 0)
            checkpoint = train_evidence / "collected" / "exported" / "model_best.pt"
            official_checkpoint = base / "training" / "humanoid" / "exported" / "model_best.pt"
            metadata = json.loads((evidence / "metadata.json").read_text(encoding="utf-8"))
            self.assertEqual(metadata["operation"], "video")
            self.assertEqual(metadata["parent_run_id"], train_evidence.name)
            self.assertEqual(metadata["source_checkpoint"], str(checkpoint))
            self.assertEqual(metadata["source_checkpoint_sha256"], sha256_file(checkpoint))
            manifest = json.loads((evidence / "video_manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["parent_run_id"], train_evidence.name)
            self.assertEqual(manifest["source_checkpoint_sha256"], sha256_file(checkpoint))
            self.assertEqual(manifest["play_video_sha256"], sha256_file(evidence / "collected" / "exported" / "play_video.mp4"))
            self.assertNotIn("policy_pt_sha256", manifest)
            self.assertEqual(official_checkpoint.read_bytes(), checkpoint.read_bytes())
            self.assertFalse((checkpoint.parent / "exported").exists())
            self.assertIn("--video", metadata["command"])
            self.assertIn("--video_length", metadata["command"])
            self.assertIn("1000", metadata["command"])
            self.assertIn("--enable_cameras", metadata["command"])
            self.assertIn('env.viewer.eye="[1.0,2.0,3.0]"', metadata["command"])
            validation = json.loads((evidence / "validation.json").read_text(encoding="utf-8"))
            states = {item["name"]: item["status"] for item in validation["checks"]}
            self.assertEqual(validation["overall"], "PASS")
            self.assertEqual(states["exported_play_video.mp4"], "PASS")
            self.assertFalse({"native_run", "tensorboard", "checkpoints", "official_backup"} & set(states))
            archive = next((logs / "exports").glob(f"{evidence.name}.tar.gz"))
            with tarfile.open(archive, "r:gz") as bundle:
                names = bundle.getnames()
            self.assertIn(f"{evidence.name}/video_manifest.json", names)
            self.assertIn(f"{evidence.name}/collected/exported/play_video.mp4", names)
            handoff = base / "download" / train_evidence.name
            self.assertTrue((handoff / "play_video.mp4").is_file())
            self.assertEqual((handoff.parent / "LATEST.txt").read_text(encoding="utf-8"), f"{train_evidence.name}\n")

    def test_official_video_records_verified_train_and_policy_lineage(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            code, train_evidence, evidence, _ = self._video(base, mode="official")
            self.assertEqual(code, 0)
            metadata = json.loads((evidence / "metadata.json").read_text(encoding="utf-8"))
            self.assertTrue(metadata["source_provenance_verified"])
            self.assertEqual(metadata["source_evidence_run_id"], train_evidence.name)
            self.assertEqual(metadata["source_run_mode"], "official")
            self.assertEqual(metadata["source_checkpoint_origin"], "train_evidence_export")
            policy = json.loads((evidence / "policy_manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(policy["source_evidence_run_id"], train_evidence.name)
            self.assertEqual(policy["source_run_mode"], "official")
            self.assertTrue(policy["source_provenance_verified"])
            self.assertIsNotNone(policy["policy_pt_sha256"])
            video_manifest = json.loads((evidence / "video_manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(video_manifest["source_evidence_run_id"], train_evidence.name)
            validation = json.loads((evidence / "validation.json").read_text(encoding="utf-8"))
            states = {item["name"]: item["status"] for item in validation["checks"]}
            self.assertEqual(states["official_checkpoint_provenance"], "PASS")

    def test_labeled_video_records_label_and_preserves_legacy_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            legacy_code, train_evidence, _, logs = self._video(base)
            self.assertEqual(legacy_code, 0)
            handoff = base / "download" / train_evidence.name
            legacy = (handoff / "play_video.mp4").read_bytes()
            with patch.dict(os.environ, {"PATH": os.environ.get("PATH", ""), "ISSACSIMZ_PLAY_SCENARIO": "success",
                                        "ISSACSIMZ_DOWNLOAD_ROOT": str(base / "download"),
                                        "ISSACSIMZ_MODE": "personal"}, clear=True):
                code = main([
                    "video", "h1", "--from-run", train_evidence.name, "--label", "stairs",
                    "--task-root", str(base / "training" / "humanoid"),
                    "--isaaclab-root", str(base / "IsaacLab"), "--log-root", str(logs),
                    "--poll-seconds", "0.01", "--gpu-interval", "0.05",
                ])
            self.assertEqual(code, 0)
            evidence = next(
                path for path in (logs / "runs").iterdir()
                if path != train_evidence and path.name.endswith("video-stairs")
            )
            metadata = json.loads((evidence / "metadata.json").read_text(encoding="utf-8"))
            manifest = json.loads((evidence / "video_manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(metadata["video_label"], "stairs")
            self.assertEqual(manifest["video_label"], "stairs")
            self.assertEqual((handoff / "play_video.mp4").read_bytes(), legacy)
            self.assertTrue((handoff / "videos" / "stairs.mp4").is_file())

    def test_video_rejects_wrong_robot_non_train_and_missing_checkpoint(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            _, train_evidence, logs = self._run(base, "success")
            self.assertEqual(main(["video", "go2", "--from-run", train_evidence.name, "--log-root", str(logs)]), 2)
            invalid = logs / "runs" / "not-train"; invalid.mkdir()
            (invalid / "metadata.json").write_text('{"operation":"play","profile":"h1"}', encoding="utf-8")
            self.assertEqual(main(["video", "h1", "--from-run", invalid.name, "--log-root", str(logs)]), 2)
            (train_evidence / "collected" / "exported" / "model_best.pt").unlink()
            self.assertEqual(main(["video", "h1", "--from-run", train_evidence.name, "--log-root", str(logs)]), 2)

    def test_video_stale_outputs_fail_freshness_validation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            code, _, evidence, _ = self._video(base, "stale")
            self.assertEqual(code, 3)
            validation = json.loads((evidence / "validation.json").read_text(encoding="utf-8"))
            states = {item["name"]: item["status"] for item in validation["checks"]}
            self.assertEqual(states["exported_play_video.mp4"], "FAIL")


if __name__ == "__main__":
    unittest.main()
