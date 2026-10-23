"""CPU-only descriptive comparison of five preserved evaluation inputs."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import statistics
import zipfile

parser = argparse.ArgumentParser()
parser.add_argument('--four-policy-input', type=Path, required=True)
parser.add_argument('--angxy-evaluation', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
expected = {
    'A_parent2700': 'e54d3389e20ea913968ef8d3edbea5004368ff225fa6b94f73fcd91cf93ca7ae',
    'B_unchanged4699': '722b35a127f7ae4209d94a9111ac5ee02071ba7f3b985dc9cdc0760bbe48f646',
    'C_lin055_4650': 'e8a358a50832f6653b1e558788a5a676ab9a849d3ec6c64e3ed2430e9ff41814',
    'D_lin065_4650': 'ce7ad58657f3dd744e7cf2b7531f3d7d455773dfc6fb135f39d8a55aa49dea70',
    'E_angxy008_4650': 'c272b13b5d3702c8a84c1470b597526efe2214d0ee38f34f65918c5f912a335f',
}
manifests, configs, rows = {}, {}, {}
input_records = []
for source, labels in [(args.four_policy_input, list(expected)[:4]), (args.angxy_evaluation, list(expected)[4:])]:
    input_records.append({'filename': source.name, 'sha256': hashlib.file_digest(source.open('rb'), 'sha256').hexdigest()})
    with zipfile.ZipFile(source) as archive:
        for label in labels:
            prefix = '' if label.startswith('E_') else label + '/'
            manifests[label] = json.loads(archive.read(prefix + 'evaluation/evaluation_manifest.json'))
            configs[label] = json.loads(archive.read(prefix + 'evaluation/resolved_configs.json'))
            data = [json.loads(line) for line in archive.read(prefix + 'evaluation/episodes.jsonl').splitlines() if line.strip()]
            keys = [(r['scenario'], r['case'], r['seed'], r['env_id']) for r in data]
            assert len(data) == len(set(keys)) == 3072, label
            assert all(r['policy_sha256'] == expected[label] for r in data), label
            assert all(r['end_reason'] == 'timeout' and r['duration_s'] == 20 and r['steps'] == 1000 and not r['base_contact_failure'] for r in data), label
            assert manifests[label]['complete'] and not manifests[label]['smoke'], label
            assert manifests[label]['policy']['sha256'] == expected[label], label
            rows[label] = dict(zip(keys, data))
reference = 'A_parent2700'
assert all(set(data) == set(rows[reference]) for data in rows.values())
assert all(m['protocol'] == manifests[reference]['protocol'] for m in manifests.values())
assert all(c == configs[reference] for c in configs.values())
assert all(r['protocol_id'] == manifests[reference]['protocol_id'] for data in rows.values() for r in data.values())

def percentile(values, q):
    ordered = sorted(values)
    position = (len(ordered) - 1) * q
    low = math.floor(position)
    high = math.ceil(position)
    return ordered[low] + (ordered[high] - ordered[low]) * (position - low)

def write_csv(filename, data):
    with (args.output / filename).open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(data[0]))
        writer.writeheader()
        writer.writerows(data)

metrics = ['vx_error', 'vy_error', 'yaw_error', 'forward_progress_m', 'stall_fraction', 'roll_pitch_rms', 'action_delta_rms']
cases = sorted({(r['scenario'], r['case']) for r in rows[reference].values()})
summaries = []
for label, data in rows.items():
    for scenario, case in cases:
        for seed in ['all', 4201, 4202, 4203]:
            selected = [r for r in data.values() if r['scenario'] == scenario and r['case'] == case and (seed == 'all' or r['seed'] == seed)]
            result = {'policy': label, 'scenario': scenario, 'case': case, 'seed': seed, 'n': len(selected)}
            result.update({metric + '_mean': statistics.fmean(r[metric] for r in selected) for metric in metrics})
            progress = [r['forward_progress_m'] for r in selected]
            result.update({'progress_p05_m': percentile(progress, .05), 'progress_min_m': min(progress), 'absolute_body_forward_mean_m': statistics.fmean(abs(r['forward_progress_m']) for r in selected), 'world_xy_mean_m': statistics.fmean(math.hypot(r['world_dx_m'], r['world_dy_m']) for r in selected)})
            summaries.append(result)
deltas = []
candidate = rows['E_angxy008_4650']
for label in list(expected)[:4]:
    for scenario, case in cases:
        keys = [k for k in candidate if k[:2] == (scenario, case)]
        for metric in metrics:
            values = [candidate[k][metric] - rows[label][k][metric] for k in keys]
            deltas.append({'candidate': 'E_angxy008_4650', 'reference': label, 'scenario': scenario, 'case': case, 'metric': metric, 'n': len(values), 'candidate_minus_reference_mean': statistics.fmean(values), 'positive_keys': sum(v > 0 for v in values), 'negative_keys': sum(v < 0 for v in values), 'equal_keys': sum(v == 0 for v in values)})
args.output.mkdir(parents=True, exist_ok=True)
write_csv('case_seed_summary.csv', summaries)
write_csv('angxy_minus_reference.csv', deltas)
verification = {'inputs': input_records, 'checkpoint_sha256': expected, 'rows_per_policy': 3072, 'policies': 5, 'total_rows': 15360, 'matching_unique_keys': True, 'identical_evaluation_protocol': True, 'identical_resolved_evaluation_configs': True, 'protocol_id': manifests[reference]['protocol_id'], 'mode': 'CPU saved-data only; no render/evaluator/training', 'limits': ['Matching keys/configs do not prove identical realized terrain/trajectories.', 'Three evaluation seeds are not three independent training seeds.', 'A automatic-best2700, B endpoint4699, C/D/E selected keeper4650 differ in selection role.', 'No official score, reward causality, p-values or aggregate mixed-unit score.']}
(args.output / 'verification.json').write_text(json.dumps(verification, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
for summary in summaries:
    if summary['seed'] == 'all' and summary['scenario'] in ['H1', 'H3', 'H4', 'H5', 'H6']:
        print(json.dumps(summary))
