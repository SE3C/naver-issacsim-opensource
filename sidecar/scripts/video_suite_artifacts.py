#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tarfile
from datetime import datetime, timezone
from pathlib import Path


PROFILES = {
    "go2": (
        ("stairs", "pyramid_stairs"),
        ("inverted_stairs", "pyramid_stairs_inv"),
        ("boxes", "boxes"),
        ("random_rough", "random_rough"),
        ("slope_up_20deg", "hf_pyramid_slope"),
        ("slope_down_20deg", "hf_pyramid_slope_inv"),
    ),
    "h1": (
        ("stairs", "pyramid_stairs"),
        ("inverted_stairs", "pyramid_stairs_inv"),
        ("boxes", "boxes"),
        ("random_rough", "random_rough"),
        ("slope_up_10deg", "hf_pyramid_slope"),
        ("slope_down_10deg", "hf_pyramid_slope_inv"),
    ),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid JSON: {path}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def find_video_evidence(evidence_root: Path, *, run_id: str, robot: str, label: str,
                        checkpoint_sha: str, started: datetime) -> tuple[str, dict, Path]:
    candidates: list[tuple[datetime, str, dict, Path]] = []
    for metadata_path in (evidence_root / "runs").glob("*/metadata.json"):
        try:
            metadata = read_json(metadata_path)
            start = parse_time(str(metadata.get("start_utc", "")))
        except (ValueError, TypeError):
            continue
        if start < started:
            continue
        if (
            metadata.get("operation") != "video"
            or metadata.get("profile") != robot
            or metadata.get("video_label") != label
            or metadata.get("parent_run_id") != run_id
            or metadata.get("source_checkpoint_sha256") != checkpoint_sha
        ):
            continue
        validation_path = metadata_path.parent / "validation.json"
        try:
            validation = read_json(validation_path)
        except ValueError:
            continue
        if validation.get("overall") != "PASS":
            continue
        mp4 = metadata_path.parent / "collected" / "exported" / "play_video.mp4"
        if not mp4.is_file() or mp4.stat().st_size <= 0:
            continue
        candidates.append((start, metadata_path.parent.name, metadata, mp4))
    if not candidates:
        raise ValueError(f"no PASS video evidence for {label} with checkpoint {checkpoint_sha}")
    _, evidence_id, metadata, mp4 = max(candidates, key=lambda item: item[0])
    return evidence_id, metadata, mp4


def finalize(args: argparse.Namespace) -> None:
    handoff = Path(args.handoff).resolve()
    evidence_root = Path(args.evidence_root).resolve()
    checkpoint = Path(args.checkpoint).resolve()
    started = parse_time(args.started_utc)
    if args.robot not in PROFILES:
        raise ValueError(f"unsupported robot: {args.robot}")
    if not checkpoint.is_file() or sha256(checkpoint) != args.checkpoint_sha:
        raise ValueError("checkpoint changed after video suite started")

    entries = []
    for label, terrain in PROFILES[args.robot]:
        video = handoff / "videos" / f"{label}.mp4"
        if not video.is_file() or video.stat().st_size <= 0:
            raise ValueError(f"missing suite video: {video}")
        evidence_id, metadata, evidence_video = find_video_evidence(
            evidence_root,
            run_id=args.run_id,
            robot=args.robot,
            label=label,
            checkpoint_sha=args.checkpoint_sha,
            started=started,
        )
        video_sha = sha256(video)
        if sha256(evidence_video) != video_sha:
            raise ValueError(f"handoff/evidence MP4 mismatch: {label}")
        entries.append({
            "label": label,
            "terrain": terrain,
            "mp4": f"videos/{label}.mp4",
            "mp4_sha256": video_sha,
            "video_evidence_id": evidence_id,
            "source_checkpoint_sha256": metadata["source_checkpoint_sha256"],
        })

    manifest = {
        "schema_version": 1,
        "suite_run_id": args.run_id,
        "robot": args.robot,
        "checkpoint_filename": checkpoint.name,
        "checkpoint_sha256": args.checkpoint_sha,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "terrains": entries,
    }
    manifest_path = handoff / "video_suite_manifest.json"
    temporary = manifest_path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(manifest_path)

    checksum = handoff / "SHA256SUMS"
    lines = [f"{entry['mp4_sha256']}  {entry['mp4']}" for entry in entries]
    lines.append(f"{sha256(manifest_path)}  video_suite_manifest.json")
    checksum.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_checksums(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        digest, separator, name = line.partition("  ")
        if not separator or len(digest) != 64 or name in result:
            raise ValueError(f"invalid checksum line: {line}")
        result[name] = digest
    return result


def verify(args: argparse.Namespace) -> None:
    suite = Path(args.suite_dir).resolve()
    archive = Path(args.archive).resolve()
    sidecar = Path(args.archive_sidecar).resolve()
    manifest_path = suite / "video_suite_manifest.json"
    checksum_path = suite / "SHA256SUMS"
    manifest = read_json(manifest_path)
    robot = manifest.get("robot")
    expected = PROFILES.get(robot)
    if expected is None:
        raise ValueError(f"unsupported manifest robot: {robot}")
    checkpoint_sha = manifest.get("checkpoint_sha256")
    if not isinstance(checkpoint_sha, str) or len(checkpoint_sha) != 64:
        raise ValueError("invalid manifest checkpoint SHA-256")
    entries = manifest.get("terrains")
    if not isinstance(entries, list) or len(entries) != 6:
        raise ValueError("suite manifest must contain exactly six terrains")
    expected_labels = [label for label, _ in expected]
    if [entry.get("label") for entry in entries] != expected_labels:
        raise ValueError("suite terrain labels do not match the robot profile")
    evidence_ids: set[str] = set()
    required: dict[str, str] = {}
    for entry in entries:
        if entry.get("source_checkpoint_sha256") != checkpoint_sha:
            raise ValueError("video checkpoint SHA does not match suite checkpoint SHA")
        evidence_id = entry.get("video_evidence_id")
        if not isinstance(evidence_id, str) or not evidence_id or evidence_id in evidence_ids:
            raise ValueError("video evidence IDs must be present and unique")
        evidence_ids.add(evidence_id)
        relative = entry.get("mp4")
        if relative != f"videos/{entry['label']}.mp4":
            raise ValueError("unexpected MP4 filename in suite manifest")
        video = suite / relative
        if not video.is_file() or video.stat().st_size <= 0:
            raise ValueError(f"missing suite video: {video}")
        actual = sha256(video)
        if entry.get("mp4_sha256") != actual:
            raise ValueError(f"MP4 SHA mismatch: {relative}")
        required[relative] = actual
    required["video_suite_manifest.json"] = sha256(manifest_path)
    checksums = parse_checksums(checksum_path)
    if checksums != required:
        raise ValueError("SHA256SUMS does not exactly match the six MP4 files and manifest")

    if not archive.is_file() or not sidecar.is_file():
        raise ValueError("suite archive and sidecar are required")
    sidecar_parts = sidecar.read_text(encoding="utf-8").strip().split()
    if len(sidecar_parts) != 2 or sidecar_parts[0] != sha256(archive) or sidecar_parts[1] != archive.name:
        raise ValueError("suite archive SHA-256 sidecar mismatch")
    top = suite.name
    with tarfile.open(archive, "r:gz") as bundle:
        members = {member.name: member for member in bundle.getmembers() if member.isfile()}
        for relative, digest in {**required, "SHA256SUMS": sha256(checksum_path)}.items():
            name = f"{top}/{relative}"
            member = members.get(name)
            if member is None:
                raise ValueError(f"suite archive missing: {name}")
            stream = bundle.extractfile(member)
            if stream is None or hashlib.sha256(stream.read()).hexdigest() != digest:
                raise ValueError(f"suite archive content mismatch: {name}")


def list_assets(args: argparse.Namespace) -> None:
    suite = Path(args.suite_dir).resolve()
    manifest = read_json(suite / "video_suite_manifest.json")
    expected = PROFILES.get(manifest.get("robot"))
    if expected is None:
        raise ValueError("unsupported manifest robot")
    for label, _ in expected:
        print(f"videos/{label}.mp4")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="action", required=True)
    finish = sub.add_parser("finalize")
    finish.add_argument("--robot", required=True, choices=PROFILES)
    finish.add_argument("--run-id", required=True)
    finish.add_argument("--checkpoint", required=True)
    finish.add_argument("--checkpoint-sha", required=True)
    finish.add_argument("--handoff", required=True)
    finish.add_argument("--evidence-root", required=True)
    finish.add_argument("--started-utc", required=True)
    check = sub.add_parser("verify")
    check.add_argument("--suite-dir", required=True)
    check.add_argument("--archive", required=True)
    check.add_argument("--archive-sidecar", required=True)
    assets = sub.add_parser("list-assets")
    assets.add_argument("--suite-dir", required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.action == "finalize":
            finalize(args)
        elif args.action == "verify":
            verify(args)
        else:
            list_assets(args)
    except (OSError, ValueError, tarfile.TarError) as exc:
        print(f"[issacsimz] ERROR: {exc}", file=sys.stderr)
        return 1
    if args.action != "list-assets":
        print(f"[issacsimz] video_suite_{args.action}=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
