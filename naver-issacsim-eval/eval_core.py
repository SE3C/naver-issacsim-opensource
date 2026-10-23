"""Versioned internal scores and cohort comparisons; standard library only."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
import random
import statistics as stats
from collections import defaultdict
from pathlib import Path

VERSION = "se3c-internal-eval-v1"


def protocol_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     allow_nan=False).encode()).hexdigest()


def file_sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2,
                                    sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


def load_suite(robot, name="scenario7"):
    if robot not in ("h1", "go2") or name not in ("scenario7", "terrain6"):
        raise ValueError("robot must be h1/go2, suite scenario7/terrain6")
    slope = math.tan(math.radians(10 if robot == "h1" else 20))

    def case(cid, terrain, commands=None, **extra):
        return {"id": cid, "terrain": terrain, "commands": commands or [[1.0, 0.0, 0.0]],
                "difficulty": 0.5, **extra}

    up = case("slope_up", "hf_pyramid_slope", slope=slope)
    down = case("slope_down", "hf_pyramid_slope_inv", slope=slope)
    if name == "terrain6":
        cases = [case("stairs", "pyramid_stairs"), case("inverted_stairs", "pyramid_stairs_inv"),
                 case("boxes", "boxes"), case("random_rough", "random_rough"), up, down]
        scenarios = [{"id": f"T{i+1}", "name": c["id"], "weight": 1 / 6,
                      "cases": [{**c, "difficulty": 1.0}]} for i, c in enumerate(cases)]
    elif robot == "h1":
        specs = [("balance", .15, [case("flat", "flat", [[0., 0., 0.]])]),
                 ("forward_tracking", .20, [case("flat", "flat", [[.5, 0., 0.], [1., 0., 0.]])]),
                 ("lateral_tracking", .10, [case("flat", "flat", [[0., .3, 0.], [0., -.3, 0.]])]),
                 ("rotation_tracking", .10, [case("flat", "flat", [[.5, 0., .5], [.5, 0., -.5]])]),
                 ("rough_terrain", .15, [case("rough", "random_rough", [[.5, 0., 0.]])]),
                 ("slope", .15, [up, down]),
                 ("push_recovery", .15, [case("push", "flat", [[.5, 0., 0.]], push_delta=.5)])]
        scenarios = [{"id": f"H{i+1}", "name": n, "weight": w, "cases": c}
                     for i, (n, w, c) in enumerate(specs)]
    else:
        specs = [("forward_tracking", .15, [case("flat", "flat", [[1., 0., 0.], [1.5, 0., 0.]])]),
                 ("omnidirectional_tracking", .15, [case("mixed", "flat", [[.6, .3, .5], [.6, -.3, -.5]])]),
                 ("rough_terrain", .20, [case("rough", "random_rough")]),
                 ("slope", .15, [up, down]),
                 ("stairs", .15, [case("stairs_up", "pyramid_stairs", step_height=.125),
                                  case("stairs_down", "pyramid_stairs_inv", step_height=.125)]),
                 ("push_recovery", .10, [case("push", "flat", push_delta=.5)]),
                 ("domain_randomization", .10, [case("randomized", "random_rough", randomization={
                     "friction_range": [0.6, 1.2], "added_mass_range": [-1.0, 1.0]})])]
        scenarios = [{"id": f"G{i+1}", "name": n, "weight": w, "cases": c}
                     for i, (n, w, c) in enumerate(specs)]
    return {"version": "internal-suite-v1", "robot": robot, "name": name,
            "duration_s": 20., "command_period_s": 10.,
            "episode_mode": "time_window" if name == "scenario7" else "first_episode",
            "stall_speed_m_s": .1, "stall_command_m_s": .2,
            "scenarios": scenarios}


def number(value, label, low=None, high=None):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{label} must be a finite number")
    if low is not None and value < low or high is not None and value > high:
        raise ValueError(f"{label} outside allowed range")
    return float(value)


def integer(value, label, low=0):
    if isinstance(value, bool) or not isinstance(value, int) or value < low:
        raise ValueError(f"{label} must be integer >= {low}")
    return value


def load_jsonl(path):
    rows = []
    with open(path, encoding="utf-8-sig") as stream:
        for line_no, line in enumerate(stream, 1):
            if line.strip():
                try:
                    row = json.loads(line)
                except ValueError as exc:
                    raise ValueError(f"{path}:{line_no}: {exc}") from exc
                if not isinstance(row, dict):
                    raise ValueError(f"{path}:{line_no}: episode must be an object")
                rows.append(row)
    return rows


DIAGNOSTICS = ("vx_error", "vy_error", "yaw_error", "xy_rmse", "yaw_rmse",
               "forward_progress_m", "lateral_drift_m", "stall_fraction",
               "roll_pitch_rms", "action_delta_rms", "integrated_body_forward_m",
               "world_dx_m", "world_dy_m")


def validate_dataset(rows, manifest):
    if not isinstance(manifest, dict) or manifest.get("schema") != "se3c-evaluation-v1":
        raise ValueError("unsupported evaluation manifest")
    if manifest.get("complete") is not True:
        raise ValueError("evaluation is incomplete; preserve raw data, do not score")
    suite, protocol = manifest["suite"], manifest["protocol"]
    if suite.get("version") != "internal-suite-v1":
        raise ValueError("unsupported suite version")
    if suite != protocol.get("suite") or suite["robot"] != manifest["robot"]:
        raise ValueError("suite/robot mismatch")
    if protocol_hash(protocol) != manifest["protocol_id"]:
        raise ValueError("protocol hash mismatch")
    if suite["name"] not in ("scenario7", "terrain6"):
        raise ValueError("unsupported suite")
    expected_specs = load_suite(manifest["robot"], suite["name"])["scenarios"]
    if [(s["id"], s["name"], s["weight"], [c["id"] for c in s["cases"]]) for s in suite["scenarios"]] != [
            (s["id"], s["name"], s["weight"], [c["id"] for c in s["cases"]]) for s in expected_specs]:
        raise ValueError("scenario identities/weights/cases differ from supported suite")
    if suite["episode_mode"] != ("time_window" if suite["name"] == "scenario7" else "first_episode"):
        raise ValueError("invalid episode mode")
    duration = number(suite["duration_s"], "duration_s", .001)
    num_envs = integer(protocol["num_envs"], "num_envs", 1)
    seeds = protocol["seeds"]
    if not seeds or len(set(seeds)) != len(seeds):
        raise ValueError("seed list empty or duplicate")
    for seed in seeds:
        integer(seed, "seed")
    policy_sha = manifest["policy"]["sha256"]
    if not isinstance(policy_sha, str) or len(policy_sha) != 64 or any(c not in "0123456789abcdef" for c in policy_sha):
        raise ValueError("policy SHA must be lowercase SHA256")
    expected = {(s["id"], c["id"], seed, env) for s in suite["scenarios"]
                for c in s["cases"] for seed in seeds for env in range(num_envs)}
    cohorts, ids = defaultdict(list), set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("episode must be object")
        key = (row["scenario"], row["case"], integer(row["seed"], "seed"), integer(row["env_id"], "env_id"))
        if key not in expected:
            raise ValueError(f"unexpected cohort {key}")
        eid = row["episode_id"]
        if not isinstance(eid, str) or not eid or (row["scenario"], row["case"], eid) in ids:
            raise ValueError("missing/duplicate episode identity")
        ids.add((row["scenario"], row["case"], eid))
        if row["protocol_id"] != manifest["protocol_id"] or row["policy_sha256"] != policy_sha:
            raise ValueError("episode protocol/policy identity mismatch")
        integer(row["steps"], "steps", 1)
        number(row["duration_s"], "episode duration", .000001, duration + .1)
        number(row["mean_tracking_error"], "mean_tracking_error", 0.)
        if not isinstance(row["survived"], bool):
            raise ValueError("survived must be boolean")
        if row["end_reason"] not in ("terminated", "timeout", "evaluation_end"):
            raise ValueError("invalid end_reason")
        if row["survived"] != (row["end_reason"] != "terminated"):
            raise ValueError("termination must take priority over timeout")
        if "base_contact_failure" in row:
            if not isinstance(row["base_contact_failure"], bool):
                raise ValueError("base_contact_failure must be boolean")
            if row["base_contact_failure"] and row["survived"]:
                raise ValueError("base contact failure cannot be survival")
        for field in DIAGNOSTICS:
            if field in row and row[field] is not None:
                lower = None if field in ("forward_progress_m", "lateral_drift_m",
                                         "integrated_body_forward_m", "world_dx_m", "world_dy_m") else 0.
                number(row[field], field, lower, 1. if field == "stall_fraction" else None)
        cohorts[key].append(row)
    if set(cohorts) != expected:
        raise ValueError(f"missing cohorts: {len(expected - set(cohorts))}")
    for key, eps in cohorts.items():
        total_duration = sum(r["duration_s"] for r in eps)
        if suite["episode_mode"] == "first_episode":
            if len(eps) != 1:
                raise ValueError("first_episode suite needs exactly one episode per cohort")
            if eps[0]["survived"] and abs(total_duration - duration) > .1:
                raise ValueError("surviving first episode has incomplete horizon")
        elif abs(total_duration - duration) > .1:
            raise ValueError(f"incomplete time-window cohort: {key}")
    return dict(cohorts)


def validate_calibration(calibration, suite):
    if calibration.get("schema") != "se3c-calibration-v1" or not calibration.get("id"):
        raise ValueError("unsupported calibration")
    if calibration.get("robot") != suite["robot"] or calibration.get("suite_hash") != protocol_hash(suite):
        raise ValueError("calibration suite mismatch")
    ids = {s["id"] for s in suite["scenarios"]}
    if set(calibration["e50_by_scenario"]) != ids:
        raise ValueError("calibration must cover exactly the scenario set")
    for value in calibration["e50_by_scenario"].values():
        number(value, "e50", .000000001)


def _diagnostics(rows):
    result = {}
    for name in DIAGNOSTICS:
        values = [r[name] for r in rows if r.get(name) is not None]
        result[name] = stats.mean(values) if values else None
        result[name + "_coverage"] = len(values) / len(rows)
    contacts = [float(r["base_contact_failure"]) for r in rows if "base_contact_failure" in r]
    result["base_contact_failure_rate"] = stats.mean(contacts) if contacts else None
    result["base_contact_coverage"] = len(contacts) / len(rows)
    return result


def _aggregate(rows, suite, calibration):
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["scenario"]].append(row)
    scenarios, total = {}, 0.
    for spec in suite["scenarios"]:
        eps = grouped[spec["id"]]
        errors = [r["mean_tracking_error"] for r in eps]
        survival = sum(r["survived"] for r in eps) / len(eps)
        error = stats.mean(errors)
        tracking = math.exp(-math.log(2) * error / calibration["e50_by_scenario"][spec["id"]])
        value = survival * tracking
        weighted = value * spec["weight"]
        total += weighted
        scenarios[spec["id"]] = {"name": spec["name"], "weight": spec["weight"],
            "episodes": len(eps), "survival_rate": survival, "mean_tracking_error": error,
            "internal_tracking_score": tracking, "scenario_score": value,
            "weighted_score": weighted, "tracking_error_p95": quantile(errors, .95),
            "diagnostics": _diagnostics(eps)}
    return 100 * total, scenarios


def quantile(values, q):
    values = sorted(values)
    pos = (len(values) - 1) * q
    lo, hi = math.floor(pos), math.ceil(pos)
    return values[lo] + (values[hi] - values[lo]) * (pos - lo)


def _total_score(rows, suite, calibration):
    sums = {s["id"]: [0, 0, 0.] for s in suite["scenarios"]}
    for row in rows:
        item = sums[row["scenario"]]
        item[0] += 1
        item[1] += row["survived"]
        item[2] += row["mean_tracking_error"]
    return 100 * sum(s["weight"] * sums[s["id"]][1] / sums[s["id"]][0] *
        math.exp(-math.log(2) * sums[s["id"]][2] / sums[s["id"]][0] /
                 calibration["e50_by_scenario"][s["id"]]) for s in suite["scenarios"])


def score_policy(rows, manifest, calibration):
    validate_dataset(rows, manifest)
    validate_calibration(calibration, manifest["suite"])
    if calibration.get("reference_protocol_id") not in (None, manifest["protocol_id"]):
        raise ValueError("reference calibration belongs to another execution protocol")
    score, scenarios = _aggregate(rows, manifest["suite"], calibration)
    seed_scores = {}
    for seed in manifest["protocol"]["seeds"]:
        seed_scores[str(seed)] = _aggregate([r for r in rows if r["seed"] == seed], manifest["suite"], calibration)[0]
    warnings = ["Internal score only; calibration is not the official tracking function."]
    if calibration.get("status") != "frozen":
        warnings.append("Calibration is provisional; freeze it before candidate ranking.")
    if len(seed_scores) < 3:
        warnings.append("Fewer than 3 seeds: uncertainty is conditional on the sampled seeds.")
    stalled = [sid for sid, result in scenarios.items() if
               result["diagnostics"].get("stall_fraction") is not None and
               result["diagnostics"]["stall_fraction"] >= .5]
    if stalled:
        warnings.append("Survival with substantial commanded-motion stall: " + ", ".join(stalled))
    missing_motion = [sid for sid, result in scenarios.items() if
                      result["diagnostics"]["stall_fraction_coverage"] < 1 or
                      result["diagnostics"]["forward_progress_m_coverage"] < 1]
    if missing_motion:
        warnings.append("Incomplete motion diagnostics; traversal conclusions unavailable: " + ", ".join(missing_motion))
    cases = {}
    for spec in manifest["suite"]["scenarios"]:
        for case in spec["cases"]:
            eps = [r for r in rows if r["scenario"] == spec["id"] and r["case"] == case["id"]]
            cases[spec["id"] + "/" + case["id"]] = {"episodes": len(eps),
                "survival_rate": stats.mean(float(r["survived"]) for r in eps),
                "mean_tracking_error": stats.mean(r["mean_tracking_error"] for r in eps),
                "diagnostics": _diagnostics(eps)}
    return {"schema": VERSION, "robot": manifest["robot"], "suite": manifest["suite"]["name"],
            "protocol_id": manifest["protocol_id"], "policy": manifest["policy"],
            "calibration": calibration, "calibration_hash": protocol_hash(calibration),
            "score_scale": "0-100 internal only", "internal_policy_score": score,
            "scenarios": scenarios, "cases": cases, "per_seed_scores": seed_scores,
            "worst_seed_score": min(seed_scores.values()),
            "worst_scenario": min(scenarios, key=lambda s: scenarios[s]["scenario_score"]),
            "warnings": warnings}


def compare_policies(rows_a, manifest_a, rows_b, manifest_b, calibration, bootstrap=1000, seed=7):
    ca, cb = validate_dataset(rows_a, manifest_a), validate_dataset(rows_b, manifest_b)
    if manifest_a["protocol_id"] != manifest_b["protocol_id"] or set(ca) != set(cb):
        raise ValueError("comparison requires identical evaluation protocols and cohorts")
    integer(bootstrap, "bootstrap", 100)
    integer(seed, "bootstrap seed")
    a, b = score_policy(rows_a, manifest_a, calibration), score_policy(rows_b, manifest_b, calibration)
    rng, deltas = random.Random(seed), []
    suite = manifest_a["suite"]
    seeds = manifest_a["protocol"]["seeds"]
    envs = range(manifest_a["protocol"]["num_envs"])
    for _ in range(bootstrap):
        ra, rb = [], []
        for sampled_seed in rng.choices(seeds, k=len(seeds)):
            for spec in suite["scenarios"]:
                for case in spec["cases"]:
                    for env in rng.choices(envs, k=len(envs)):
                        key = (spec["id"], case["id"], sampled_seed, env)
                        ra.extend(ca[key]); rb.extend(cb[key])
        deltas.append(_total_score(ra, suite, calibration) - _total_score(rb, suite, calibration))
    delta = a["internal_policy_score"] - b["internal_policy_score"]
    interval = [quantile(deltas, .025), quantile(deltas, .975)]
    conclusion = "A_HIGHER" if interval[0] > 0 else "B_HIGHER" if interval[1] < 0 else "TIE" if delta == 0 and interval == [0., 0.] else "INCONCLUSIVE"
    scenarios = {}
    for sid in a["scenarios"]:
        x, y = a["scenarios"][sid], b["scenarios"][sid]
        scenarios[sid] = {"weighted_score_delta": 100 * (x["weighted_score"] - y["weighted_score"]),
                          "survival_delta": x["survival_rate"] - y["survival_rate"],
                          "tracking_error_delta": x["mean_tracking_error"] - y["mean_tracking_error"],
                          "diagnostics_A": x["diagnostics"], "diagnostics_B": y["diagnostics"]}
    return {"schema": "se3c-internal-compare-v1", "robot": manifest_a["robot"],
            "score_A": a["internal_policy_score"], "score_B": b["internal_policy_score"],
            "policy_A": manifest_a["policy"], "policy_B": manifest_b["policy"],
            "delta_A_minus_B": delta, "ci95_delta": interval, "conclusion": conclusion,
            "conclusion_scope": "sampled evaluation cohorts only",
            "ranking_ready": len(seeds) >= 3 and calibration.get("status") == "frozen",
            "protocol_id": a["protocol_id"], "calibration_hash": a["calibration_hash"],
            "bootstrap": {"replicates": bootstrap, "seed": seed,
                          "unit": "paired seed/case/environment cohort blocks, episodes preserved"},
            "scenarios": scenarios, "warnings": a["warnings"] + [
                "Same seeds pair evaluation cohorts, not identical post-reset trajectories.",
                "Higher internal score is not automatic adoption; inspect worst scenario, stall, and falls."]}


def calibrate(rows, manifest, calibration_id):
    validate_dataset(rows, manifest)
    values = {}
    for spec in manifest["suite"]["scenarios"]:
        median = stats.median(r["mean_tracking_error"] for r in rows if r["scenario"] == spec["id"])
        if median <= 0:
            raise ValueError("zero-error reference cannot determine a positive e50")
        values[spec["id"]] = median
    return {"schema": "se3c-calibration-v1", "id": calibration_id, "robot": manifest["robot"],
            "suite_hash": protocol_hash(manifest["suite"]), "e50_by_scenario": values,
            "status": "provisional", "method": "reference episode-error median per scenario",
            "reference_policy_sha256": manifest["policy"]["sha256"],
            "reference_protocol_id": manifest["protocol_id"],
            "reference_rows_sha256": protocol_hash(rows)}


def report_html(result):
    encoded = html.escape(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    title = "내부 정책 비교" if "score_A" in result else "내부 정책 평가"
    if "score_A" in result:
        headline = f"A {result['score_A']:.2f} · B {result['score_B']:.2f} · Δ {result['delta_A_minus_B']:+.2f} · 95% CI {result['ci95_delta']}"
        inputs = "<p>A (후보): " + html.escape(str(result["policy_A"].get("path", ""))) + "<br>B (기준): " + html.escape(str(result["policy_B"].get("path", ""))) + "</p>"
    else:
        headline = f"{result['internal_policy_score']:.2f} / 100 · worst scenario {result['worst_scenario']}"
        inputs = ""
    warnings = "".join(f"<li>{html.escape(w)}</li>" for w in result["warnings"])
    if "score_A" in result:
        columns = "<th>시나리오</th><th>가중 점수 Δ</th><th>생존율 Δ</th><th>추종 오차 Δ</th>"
        body = "".join(f"<tr><td>{html.escape(sid)}</td><td>{r['weighted_score_delta']:+.3f}</td><td>{r['survival_delta']:+.3f}</td><td>{r['tracking_error_delta']:+.3f}</td></tr>" for sid, r in result["scenarios"].items())
    else:
        columns = "<th>시나리오</th><th>episode</th><th>생존율</th><th>추종 오차</th><th>내부 점수</th><th>stall</th><th>세계 X 변위(m)</th>"
        body = ""
        for sid, r in result["scenarios"].items():
            stall = r["diagnostics"]["stall_fraction"]
            stall_text = "미기록" if stall is None else f"{stall:.3f}"
            displacement = r["diagnostics"]["world_dx_m"]
            displacement_text = "미기록" if displacement is None else f"{displacement:.3f}"
            body += f"<tr><td>{html.escape(sid + ' ' + r['name'])}</td><td>{r['episodes']}</td><td>{r['survival_rate']:.3f}</td><td>{r['mean_tracking_error']:.3f}</td><td>{100*r['scenario_score']:.2f}</td><td>{stall_text}</td><td>{displacement_text}</td></tr>"
    return f'<!doctype html><html lang="ko"><meta charset="utf-8"><title>{title}</title><style>body{{font:16px system-ui;margin:40px;max-width:1200px}}pre{{white-space:pre-wrap;background:#f5f5f5;padding:20px}}li{{margin:8px}}table{{border-collapse:collapse;width:100%}}th,td{{padding:10px;border-bottom:1px solid #ccc;text-align:left}}</style><h1>{title}</h1><h2>{html.escape(headline)}</h2>{inputs}<p>공식 채점·제출 점수가 아닌 PERSONAL 사후 평가입니다.</p><ul>{warnings}</ul><table><thead><tr>{columns}</tr></thead><tbody>{body}</tbody></table><details><summary>전체 수치·프로토콜·진단 보기</summary><pre>{encoded}</pre></details></html>'


def demo(output, robot, suite_name):
    root = Path(output); root.mkdir(parents=True, exist_ok=False)
    suite = load_suite(robot, suite_name)
    protocol = {"suite": suite, "num_envs": 4, "seeds": [42, 43, 44],
                "collector_version": "synthetic-test-only"}
    for label, error, sha in [("a", .4, "a" * 64), ("b", .6, "b" * 64)]:
        path = root / label; path.mkdir()
        manifest = {"schema": "se3c-evaluation-v1", "robot": robot, "suite": suite,
                    "protocol": protocol, "protocol_id": protocol_hash(protocol),
                    "policy": {"sha256": sha, "path": "SYNTHETIC-NO-POLICY"}, "complete": True,
                    "synthetic": True}
        rows = [{"scenario": s["id"], "case": c["id"], "seed": seed, "env_id": env,
                 "episode_id": f"{seed}-{env}-0", "steps": 1000, "duration_s": 20.,
                 "end_reason": "evaluation_end", "survived": True,
                 "mean_tracking_error": error + env * .01, "policy_sha256": sha,
                 "protocol_id": manifest["protocol_id"], "stall_fraction": 0.,
                 "base_contact_failure": False} for s in suite["scenarios"] for c in s["cases"]
                for seed in protocol["seeds"] for env in range(4)]
        write_json(path / "evaluation_manifest.json", manifest)
        (path / "episodes.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    write_json(root / "calibration.json", {"schema": "se3c-calibration-v1", "id": "demo-unvalidated",
        "robot": robot, "suite_hash": protocol_hash(suite), "status": "provisional",
        "method": "synthetic smoke value, not measured", "e50_by_scenario": {s["id"]: 1. for s in suite["scenarios"]}})


def main(argv=None):
    parser = argparse.ArgumentParser(description="PERSONAL posthoc internal evaluator; no simulation in this scorer")
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("score", "calibrate"):
        p = commands.add_parser(name); p.add_argument("--evaluation", required=True)
        p.add_argument("--out", required=True)
        if name == "score": p.add_argument("--calibration", required=True)
        else: p.add_argument("--id", required=True)
    p = commands.add_parser("compare"); p.add_argument("--a", required=True); p.add_argument("--b", required=True)
    p.add_argument("--calibration", required=True); p.add_argument("--out", required=True)
    p.add_argument("--bootstrap", type=int, default=1000); p.add_argument("--seed", type=int, default=7)
    p = commands.add_parser("demo"); p.add_argument("--out", required=True)
    p.add_argument("--robot", choices=("h1", "go2"), default="go2")
    p.add_argument("--suite", choices=("scenario7", "terrain6"), default="scenario7")
    p = commands.add_parser("suite"); p.add_argument("--robot", choices=("h1", "go2"), required=True)
    p.add_argument("--suite", choices=("scenario7", "terrain6"), default="scenario7")
    args = parser.parse_args(argv)
    try:
        if args.command == "demo": demo(args.out, args.robot, args.suite); return 0
        if args.command == "suite": print(json.dumps(load_suite(args.robot, args.suite), indent=2)); return 0
        output = Path(args.out)
        if output.suffix.lower() != ".json" or output.exists():
            raise ValueError("--out must be a new .json file; existing artifacts are never overwritten")
        if args.command != "calibrate" and output.with_suffix(".html").exists():
            raise ValueError("HTML output already exists; choose a new --out")

        def read(directory):
            path = Path(directory)
            return load_jsonl(path / "episodes.jsonl"), json.loads((path / "evaluation_manifest.json").read_text(encoding="utf-8-sig"))

        if args.command == "calibrate": result = calibrate(*read(args.evaluation), args.id)
        else:
            calibration = json.loads(Path(args.calibration).read_text(encoding="utf-8-sig"))
            if args.command == "score": result = score_policy(*read(args.evaluation), calibration)
            else:
                ra, ma = read(args.a); rb, mb = read(args.b)
                result = compare_policies(ra, ma, rb, mb, calibration, args.bootstrap, args.seed)
        write_json(args.out, result)
        if args.command != "calibrate": Path(args.out).with_suffix(".html").write_text(report_html(result), encoding="utf-8")
        print(json.dumps({k: result[k] for k in ("internal_policy_score", "delta_A_minus_B", "ci95_delta", "conclusion", "id") if k in result}, ensure_ascii=False))
        return 0
    except (ValueError, KeyError, OSError, TypeError) as exc:
        parser.exit(2, f"ERROR: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
