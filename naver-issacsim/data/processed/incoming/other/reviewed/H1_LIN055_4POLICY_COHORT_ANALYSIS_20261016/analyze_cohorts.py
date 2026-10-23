#!/usr/bin/env python3
"""Existing H1 scenario7 CPU-only, reproducible A/B/C/D cohort audit.

Usage: python analyze_cohorts.py --input H1_LIN055_4POLICY_COHORT_INPUT_20261015.zip --out OUTPUT_DIRECTORY
Requires Python 3.10+ standard library only. Does not import Torch/Isaac Sim; never runs evaluation.
This code reads ZIP members only and does not modify original files.
"""
from __future__ import annotations
import argparse
import collections
import csv
import hashlib
import json
import math
import platform
import re
import statistics
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile

POLICIES = ("A_parent2700", "B_unchanged4699", "C_lin055_4650", "D_lin065_4650")
CASES = (("H1", "flat"), ("H2", "flat"), ("H3", "flat"), ("H4", "flat"),
         ("H5", "rough"), ("H6", "slope_up"), ("H6", "slope_down"), ("H7", "push"))
KEY = ("scenario", "case", "seed", "env_id")
COMPARISONS = (("C_lin055_4650", "B_unchanged4699"), ("C_lin055_4650", "D_lin065_4650"),
               ("B_unchanged4699", "A_parent2700"), ("C_lin055_4650", "A_parent2700"),
               ("D_lin065_4650", "A_parent2700"))
# Directions are strictly per-field descriptive. 'neutral' metrics are NOT given good/bad ranks.
DIRECTIONS = {
 "mean_tracking_error": "lower", "vx_error": "lower", "vy_error": "lower", "yaw_error": "lower",
 "xy_rmse": "lower", "yaw_rmse": "lower", "abs_forward_m": "lower", "world_xy_net_m": "lower",
 "lateral_drift_m": "lower", "stall_fraction": "lower", "stall_gt_005": "lower",
 "roll_pitch_rms": "lower", "action_delta_rms": "lower", "survived": "higher",
 "forward_progress_m": "higher", "integrated_body_forward_m": "higher",
}
METRICS = tuple(DIRECTIONS.keys())
UNITS = {
 "mean_tracking_error": "mixed (vx/vy m/s, yaw rad/s; not one physical unit)",
 "vx_error": "m/s (episode reported)", "vy_error": "m/s (episode reported)",
 "yaw_error": "rad/s (episode reported)", "xy_rmse": "m/s (episode reported)",
 "yaw_rmse": "rad/s (episode reported)", "forward_progress_m": "m (integrated body-frame forward)",
 "integrated_body_forward_m": "m", "abs_forward_m": "m", "world_xy_net_m": "m (final net displacement)",
 "lateral_drift_m": "m (integrated |vy tracking error|, NOT world displacement)",
 "stall_fraction": "fraction [0,1]", "stall_gt_005": "0/1 indicator (stall_fraction > 0.05)",
 "roll_pitch_rms": "rad (reported RMS)", "action_delta_rms": "action-value units (reported RMS)",
 "survived": "0/1",
}


def digest(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def jload(z: ZipFile, member: str):
    return json.loads(z.read(member).decode('utf-8-sig'))


def quantile(values, q):
    seq = sorted(values)
    if not seq:
        return math.nan
    pos = (len(seq)-1) * q
    lo = int(math.floor(pos)); hi = int(math.ceil(pos))
    return seq[lo] + (seq[hi] - seq[lo]) * (pos-lo)


def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        wr = csv.DictWriter(f, fields, extrasaction='ignore')
        wr.writeheader()
        wr.writerows(rows)


def vfmt(x, digits=4):
    return f'{x:.{digits}f}'


def key_of(r):
    return tuple(r[k] for k in KEY)


def derived_metrics(e):
    assert e['forward_progress_m'] == e['integrated_body_forward_m'], 'Progress must be identity field'
    out = {k: float(e[k]) for k in ("mean_tracking_error", "vx_error", "vy_error", "yaw_error",
             "xy_rmse", "yaw_rmse", "forward_progress_m", "integrated_body_forward_m",
             "lateral_drift_m", "stall_fraction", "roll_pitch_rms", "action_delta_rms")}
    out['abs_forward_m'] = abs(float(e['forward_progress_m']))
    out['world_xy_net_m'] = math.hypot(float(e['world_dx_m']), float(e['world_dy_m']))
    out['stall_gt_005'] = float(float(e['stall_fraction']) > 0.05)
    out['survived'] = float(bool(e['survived']))
    assert all(math.isfinite(v) for v in out.values()), 'NaN/infinite metrics'
    return out


def aggregate(xs):
    vals = sorted(xs)
    return {'count':len(vals), 'mean':statistics.fmean(vals), 'p05':quantile(vals,.05),
            'p50':quantile(vals,.5), 'p95':quantile(vals,.95), 'min':min(vals), 'max':max(vals)}


def direction_for(metric, scenario):
    # The XY endpoint magnitude is NOT a success criterion for body-frame H3 +/-vy.
    if metric == 'world_xy_net_m' and scenario != 'H1':
        return 'descriptive_only'
    # Signed body progress is not a higher-is-better metric under zero-vx H1/H3.
    if metric in ('forward_progress_m', 'integrated_body_forward_m') and scenario in ('H1','H3'):
        return 'descriptive_only'
    return DIRECTIONS[metric]


def paired_stats(rows, metric, direction):
    vals = [r['candidate'][metric] - r['reference'][metric] for r in rows]
    d = direction
    eps = 1e-12
    if d == 'descriptive_only':
        improved = None; worsened = None
    elif d == 'lower':
        improved = sum(v < -eps for v in vals); worsened = sum(v > eps for v in vals)
    else:
        improved = sum(v > eps for v in vals); worsened = sum(v < -eps for v in vals)
    return {'n_pairs':len(vals), 'mean_delta_candidate_minus_reference':statistics.fmean(vals),
            'median_delta':quantile(vals,.5), 'p05_delta':quantile(vals,.05), 'p95_delta':quantile(vals,.95),
            'improved_n':improved, 'worsened_n':worsened,
            'ties_n':None if improved is None else len(vals)-improved-worsened,
            'worsened_fraction':None if worsened is None else worsened/len(vals)}


def collect_input(z):
    im = jload(z, 'INPUT_MANIFEST.json')  # FIRST substantive read; identity source
    assert im['purpose'] == 'existing evaluation cohort comparison, no GPU run'
    assert tuple(x['label'] for x in im['policies']) == POLICIES
    inputs = {x['label']:x for x in im['policies']}
    # Verify all source ZIP member checksums from the supplied audit list.
    checks = {}
    for line in z.read('SHA256SUMS.txt').decode('utf-8-sig').splitlines():
        if not line.strip(): continue
        sha, member = line.split(maxsplit=1)
        assert member in z.namelist(), ('member absent',member)
        assert member not in checks, 'Duplicate checksum member'
        actual = digest(z.read(member))
        assert actual == sha, ('Input checksum mismatch',member)
        checks[member] = sha
    assert len(checks) == len(z.namelist())-1 and 'SHA256SUMS.txt' not in checks
    manifests={}; resolutions={}; publications={}; episodes={}; metrics={}; integrity=[]; metadata=[]
    for label in POLICIES:
        root=label+'/'; m=jload(z,root+'evaluation/evaluation_manifest.json')
        pub=jload(z,root+'publication_manifest.json')
        res=jload(z,root+'evaluation/resolved_configs.json')
        link=jload(z,root+'evaluation/video_evaluation_link.json')
        expected=inputs[label]['checkpoint_sha256']
        assert m['policy']['sha256']==expected == pub['source_checkpoint_sha256']==link['source_checkpoint_sha256']
        assert pub['training_run_id']==inputs[label]['training_run_id']
        assert m['protocol_id']==inputs[label]['protocol_id'] == link['protocol_id']
        assert m['complete'] is True and m['execution_status']=='COMPLETE' and m['smoke'] is False
        assert m['evaluation_environment']=='PERSONAL' and m['policy']['source_run_id'] is None
        assert m['policy']['preset'] is None
        epbytes=z.read(root+'evaluation/episodes.jsonl')
        rows=[json.loads(line) for line in epbytes.splitlines() if line.strip()]
        assert len(rows)==inputs[label]['evaluation_rows']==3072
        bykey={}
        for e in rows:
            key=key_of(e)
            assert key not in bykey, ('Duplicate cohort key',label,key)
            assert e['policy_sha256']==expected and e['protocol_id']==m['protocol_id']
            assert e['episode_id'] == f'{key[0]}-{key[1]}-s{key[2]}-e{key[3]}-n0', ('noninitial episode',e['episode_id'])
            assert e['steps']==1000 and e['duration_s']==20.0 and e['end_reason']=='timeout'
            assert e['survived'] is True and e['base_contact_failure'] is False
            assert key[2] in (4201,4202,4203) and 0<=key[3]<128
            bykey[key]=e
        expected_keys={(case[0],case[1],s,e) for case in CASES for s in (4201,4202,4203) for e in range(128)}
        assert set(bykey)==expected_keys, ('Missing/unexpected cohort', label)
        assert len({x['episode_id'] for x in rows})==3072
        for sc,case in CASES:
            cases=[x for x in rows if (x['scenario'],x['case'])==(sc,case)]
            assert len(cases)==inputs[label]['scenario_case_counts'][f'{sc}/{case}']==384
        manifests[label]=m; resolutions[label]=res; publications[label]=pub
        episodes[label]=bykey; metrics[label]={key:derived_metrics(e) for key,e in bykey.items()}
        metadata.append({
            'policy':label, 'evaluation_policy_sha256':expected,
            'source_checkpoint_filename':pub.get('source_checkpoint_filename'),
            'training_run_id_publication_only':pub.get('training_run_id'),
            'selection_and_lineage_input_manifest':inputs[label]['selection_and_lineage'],
            'training_lin_input_manifest':inputs[label]['track_lin_vel_xy_exp_training'],
            'training_action_input_manifest':inputs[label]['action_rate_l2_training'],
            'raw_evaluation_source_run_id':m['policy']['source_run_id'],
            'raw_evaluation_preset':m['policy']['preset'],
            'publication_raw_parent_run_id':pub.get('raw_run_parent_run_id'),
            'publication_raw_source_provenance_verified':pub.get('raw_source_provenance_verified'),
            'evaluation_start_utc':m['started_at'], 'evaluation_finish_utc':m['finished_at'],
            'wall_seconds':m['elapsed_wall_s'],
            'protocol_id':m['protocol_id'], 'evaluation_environment':m['evaluation_environment'],
            'rows':len(rows), 'sha256_episodes_member':digest(epbytes),
        })
        for sc, case in CASES:
            for seed in (4201,4202,4203):
                group=[x for x in rows if (x['scenario'],x['case'],x['seed'])==(sc,case,seed)]
                integrity.append({'policy':label,'scenario':sc,'case':case,'seed':seed,
                   'rows':len(group),'distinct_env_ids':len(set(e['env_id'] for e in group)),
                   'distinct_episode_ids':len(set(e['episode_id'] for e in group)),
                   'timeout_rows':sum(x['end_reason']=='timeout' for x in group),
                   'contact_failure_rows':sum(x['base_contact_failure'] for x in group),
                   'non_n0_rows':sum(not x['episode_id'].endswith('-n0') for x in group),
                   'total_steps':sum(x['steps'] for x in group)})
    # Verify parity, equality of all evaluator-facing objects, and record only runtime differences.
    reference=POLICIES[0]
    for p in POLICIES[1:]:
        a=manifests[reference]; b=manifests[p]
        assert a['protocol']==b['protocol'], ('Protocol difference',p)
        assert a['source_fingerprints']==b['source_fingerprints'], ('Evaluator source fingerprint difference',p)
        assert a['task_config']==b['task_config'], ('Task configuration difference',p)
        assert a['suite']==b['suite'], ('Command/suite difference',p)
        assert resolutions[reference]==resolutions[p], ('Resolved config difference',p)
    return im, checks, manifests, resolutions, publications, episodes, metrics, integrity, metadata


def make_stats(metrics):
    summ_case=[]; summ_seed_case=[]; paired_case=[]; paired_seed_case=[]; paired_cohorts=[]; tail=[]
    for label in POLICIES:
        for sc,case in CASES:
            for seed in (None,4201,4202,4203):
                keys=[k for k in metrics[label] if (k[0],k[1])==(sc,case) and (seed is None or k[2]==seed)]
                for metric in METRICS:
                    stats=aggregate([metrics[label][k][metric] for k in keys])
                    entry={'policy':label, 'scenario':sc,'case':case,'seed':seed if seed else 'ALL',
                           'metric':metric,'unit':UNITS[metric],**stats}
                    (summ_case if seed is None else summ_seed_case).append(entry)
                if (sc,case)==('H5','rough'):
                    progs=[metrics[label][k]['forward_progress_m'] for k in keys]
                    stalls=[metrics[label][k]['stall_fraction'] for k in keys]
                    tail.append({'policy':label,'seed':seed if seed is not None else 'ALL','n':len(keys),
                                 'mean_progress_m':statistics.fmean(progs),'p05_progress_m':quantile(progs,.05),
                                 'min_progress_m':min(progs),'p50_progress_m':quantile(progs,.5),
                                 'p95_progress_m':quantile(progs,.95), 'max_progress_m':max(progs),
                                 'mean_stall_fraction':statistics.fmean(stalls), 'max_stall_fraction':max(stalls),
                                 'stall_gt_005_count':sum(v>0.05 for v in stalls)})
    for candidate, ref in COMPARISONS:
        for key in sorted(metrics[candidate]):
            c=metrics[candidate][key]; b=metrics[ref][key]
            entry={'candidate':candidate,'reference':ref, **dict(zip(KEY,key))}
            for mt in ("mean_tracking_error", "vx_error", "vy_error", "yaw_error", "abs_forward_m",
                       "forward_progress_m", "world_xy_net_m", "stall_fraction", "action_delta_rms"):
                entry[mt+'_candidate']=c[mt];entry[mt+'_reference']=b[mt];entry['delta_'+mt]=c[mt]-b[mt]
            paired_cohorts.append(entry)
        for sc, case in CASES:
            for seed in (None,4201,4202,4203):
                keys=[k for k in metrics[candidate] if (k[0],k[1])==(sc,case) and (seed is None or k[2]==seed)]
                for mt in METRICS:
                    paired=[{'candidate':metrics[candidate][key],'reference':metrics[ref][key]} for key in keys]
                    stats=paired_stats(paired,mt,direction_for(mt,sc))
                    o={'candidate':candidate,'reference':ref,'scenario':sc,'case':case,
                       'seed':seed if seed else 'ALL', 'metric':mt,'unit':UNITS[mt],
                       'better_direction':direction_for(mt,sc),
                       'candidate_mean':statistics.fmean(x['candidate'][mt] for x in paired),
                       'reference_mean':statistics.fmean(x['reference'][mt] for x in paired), **stats}
                    (paired_case if seed is None else paired_seed_case).append(o)
    return summ_case, summ_seed_case, paired_case, paired_seed_case, paired_cohorts, tail


def make_parity(manifests,resolutions):
    baseline=manifests[POLICIES[0]]
    checks={
       'evaluation_manifest.protocol':lambda m: m['protocol'],
       'evaluation_manifest.protocol_id':lambda m: m['protocol_id'],
       'evaluation_manifest.source_fingerprints':lambda m: m['source_fingerprints'],
       'evaluation_manifest.protocol.applied_environment_config_fingerprints':lambda m:m['protocol']['applied_environment_config_fingerprints'],
       'evaluation_manifest.protocol.agent_config_fingerprint':lambda m:m['protocol']['agent_config_fingerprint'],
       'evaluation_manifest.task_config':lambda m:m['task_config'],
       'evaluation_manifest.suite':lambda m:m['suite'],
       'evaluation_manifest.policy.actor_mode':lambda m:m['protocol']['actor_mode'],
       'evaluation_manifest.protocol.command_schedule':lambda m:m['protocol']['command_schedule'],
       'evaluation_manifest.protocol.disturbance_schedule':lambda m:m['protocol']['disturbance_schedule'],
       'evaluation_manifest.protocol.seeds':lambda m:m['protocol']['seeds'],
       'evaluation_manifest.protocol.num_envs':lambda m:m['protocol']['num_envs'],
       'evaluation_manifest.protocol.versions':lambda m:m['protocol']['versions'],
       'evaluation_manifest.smoke':lambda m:m['smoke'],
       'evaluation_manifest.complete':lambda m:m['complete'],
       'evaluation_manifest.execution_status':lambda m:m['execution_status'],
    }
    rows=[]
    for name, getter in checks.items():
        v0=getter(baseline)
        for p in POLICIES:
            v=getter(manifests[p]); rows.append({'section':name,'policy':p,'matches_A':v==v0,
                'sha256_of_canonical_json':digest(json.dumps(v,sort_keys=True,ensure_ascii=False).encode())})
    for p in POLICIES:
        v=resolutions[p];v0=resolutions[POLICIES[0]]
        rows.append({'section':'evaluation.resolved_configs.json (FULL structural+byte equality)',
                     'policy':p,'matches_A':v==v0,'sha256_of_canonical_json':digest(json.dumps(v,sort_keys=True).encode())})
    assert all(x['matches_A'] for x in rows)
    return rows


def show(policy, sc, case, metric, values):
    return next(x['mean'] for x in values if x['policy']==policy and x['scenario']==sc and x['case']==case and x['metric']==metric)


def pair(candidate,ref,sc,case,metric,values):
    return next(x for x in values if x['candidate']==candidate and x['reference']==ref and x['scenario']==sc and x['case']==case and x['metric']==metric)


def tailrow(policy, seed, tails):
    return next(r for r in tails if r['policy']==policy and r['seed']==seed)


def report_text(input_path, inputs_sha, checks, manifests, resolutions, pubs, integrity,
                summ_case, summ_seed_case, paired_case, paired_seed_case, tails, metadata):
    A,B,C,D=POLICIES
    short={A:'A 부모2700',B:'B unchanged4699',C:'C lin=.55/4650',D:'D lin=.65/4650'}
    def mean(p, sc,mt,case='flat'):return show(p,sc,case,mt,summ_case)
    def delta(p,q,sc,mt,case='flat'):return pair(p,q,sc,case,mt,paired_case)['mean_delta_candidate_minus_reference']
    def cnt(p,q,sc,mt,case='flat'):
        r=pair(p,q,sc,case,mt,paired_case);return f"개선 {r['improved_n']}/{r['n_pairs']}, 악화 {r['worsened_n']}/{r['n_pairs']} ({r['worsened_fraction']*100:.1f}%)"
    def cell(p,sc,mt,case='flat'):return vfmt(mean(p,sc,mt,case),3)
    def scdelta(p,q,sc,mt,case='flat'):return f'{delta(p,q,sc,mt,case):+.3f}'
    rows=[]
    rows += ['# H1 scenario7 4정책 기존 원자료 코호트 비교',
             '', '> 검토: 2026-10-16(KST) | 기존 PERSONAL Windows camera-off episode 원자료 CPU 재집계 | **새 GPU 평가·렌더·학습 없음**',
             '', '## 결론',
             '', f"**C는 B의 rough H5 평균 진행 손실을 일부 복구했습니다**: {cell(B,'H5','forward_progress_m','rough')}→{cell(C,'H5','forward_progress_m','rough')}m (Δ {scdelta(C,B,'H5','forward_progress_m','rough')}m), {cnt(C,B,'H5','forward_progress_m','rough')}. 그러나 A의 rough 평균 {cell(A,'H5','forward_progress_m','rough')}m와 P05 {vfmt(tailrow(A,'ALL',tails)['p05_progress_m'],3)}m에는 미달하며 H3 vy 오차가 B보다 커집니다. **A의 강점을 온전히 유지하며 B의 약점을 해결했다고 판정할 수 없습니다.**",
             '', f"**C가 D보다 균형상 우월하다고 결론낼 수 없습니다.** C는 H4 yaw 오차가 {cell(D,'H4','yaw_error')}→{cell(C,'H4','yaw_error')}rad/s (낮을수록 양호)로 감소하지만, H3 vy 오차는 {cell(D,'H3','vy_error')}→{cell(C,'H3','vy_error')}m/s로 증가하고 H5 평균/P05/min 진행에서 D가 우세합니다. 서로 다른 축의 trade-off이며 별도 합성점수/승자 선정은 하지 않았습니다.",
             '', '**결정: C는 범용 대표 PROMOTE 보류(HOLD).** B는 H5 지속적 진행 손실이 있는 참고 대조군, A는 H5 진행 기준선, D는 rough·H3 vy 참고 후보로 분리합니다. 아래의 전체 8개 case 결과를 판단에 포함했습니다.',
             '', '## 1. 원본 감사, 계보 및 평가 조건',
             '', f'- 입력 파일명: `{input_path.name}`. 입력 ZIP SHA-256: `{inputs_sha}`. `SHA256SUMS.txt`의 {len(checks)}개 멤버 해시 모두 재계산 일치(자기 자신 제외). ZIP 내부 평가 raw만 재집계했고 checkpoint `.pt` 본체는 제공되지 않아 checkpoint 바이트 SHA를 새로 계산한 것은 아닙니다.',
             '- `INPUT_MANIFEST.json` → 평가 `policy.sha256` → `video_evaluation_link` → `publication_manifest.source_checkpoint_sha256`의 **기재 SHA 4-way 일치**를 확인했습니다. `publication_manifest`의 학습 Run 연결은 **외부 메타데이터를 통한 매핑**이고 평가 원문 `policy.source_run_id=null`, `preset=null`은 원형 보존했습니다. 부모 import provenance도 null/false를 변경하지 않았습니다.',
             '', '| 정책 | 평가 checkpoint SHA-256 | 학습 run (publication 매핑) | 선택·설정 (INPUT 기준) |',
             '|---|---|---|---|']
    for row in metadata:
        p=row['policy']; rows.append(f"| {short[p]} | `{row['evaluation_policy_sha256']}` | `{row['training_run_id_publication_only']}` | {row['selection_and_lineage_input_manifest']}; lin={row['training_lin_input_manifest']}, action={row['training_action_input_manifest']} |")
    rows += ['', '**평가 parity:** 네 `evaluation_manifest.protocol` 전체, `source_fingerprints`, 적용 환경 fingerprint 전 24개(8 case×3 seed), `agent_config_fingerprint`, `task_config`, `suite`, `resolved_configs.json` 961,753바이트의 **동일 SHA**(`'+digest(json.dumps(resolutions[A],sort_keys=True).encode())+'`는 canonical JSON 해시), 원본 JSON 바이트도 네 파일 동일합니다. Protocol ID: `'+manifests[A]['protocol_id']+'`.',
            '- 환경: PERSONAL Windows H1 `Humanoid-v0`, deterministic actor, 카메라 비활성, 평가 GPU RTX 3060 Laptop. 동일 `source_fingerprints` 4개. RSL-RL 5.0.1, Isaac Lab 0.54.3 및 commit이 같은 protocol에 기록되어 있습니다. Isaac Sim 버전 `unavailable`은 미검증.',
            '- Case: H1 flat 정지, H2 flat 0.5→1.0 m/s 전진, H3 flat body-frame vy +0.3→-0.3 m/s, H4 flat vx 0.5m/s 및 yaw +0.5→-0.5rad/s, H5 rough vx0.5m/s, H6 up/down vx1m/s, H7 push vx0.5m/s. 명령 주기 10초, 총 20초. H7 외란은 fixed XY velocity deltas 4/8/12/16초(프로토콜 명시)이며 `command_schedule=per_episode_step_clock_without_rng_v1`.',
            '- Randomization: 평가 `resolved_configs`의 `events.add_base_mass`, `events.base_com`, `events.base_external_force_torque`, `events.physics_material`, `events.push_robot`은 모두 `null`. 단 `events.reset_base`는 reset마다 x/y 각 -0.5..0.5m, yaw -3.14..3.14rad의 균등 초기 자세 범위를 적용하며 `reset_robot_joints`는 position scale [1,1], velocity [0,0]으로 기록됩니다. H5 random rough terrain generator와 seed·difficulty 설정/적용 fingerprint가 같습니다. 하지만 실제 난수 draw/reset 자세·generated tile 자체가 정책 간 동일했다고 증명할 수는 없습니다. 개별 step/terrain realization ID가 원자료에 없습니다.',
            '- 동일하지 않은 manifest 필드 7개(A 대비): `policy.sha256`, 임시 staging `policy.path`, `started_at`, `finished_at`, `elapsed_wall_s`, `gpu_info_before`, `gpu_info_after`. 평가 시작·종료 날짜가 각기 다릅니다. 평가에 사용한 GPU·명령·task source 설정의 차이는 발견되지 않았습니다.',
            '- **중요:** 네 평가 `resolved_configs`에 기록된 reward는 평가 중 로드한 환경 설정을 뜻합니다(예: action weight -0.0005). A/B/C/D 학습 reward를 식별하는 근거로 전용할 수 없으며, 학습 설정 .50/.55/.65 및 action=-.0001은 `INPUT_MANIFEST`/publication의 외부 연결 주장입니다. OFFICIAL train resolved source·PPO 전체를 이 입력으로 재감사한 것은 아닙니다.',
            '', '## 2. 코호트 구조·독립성',
            '', '- 각 3,072 행 = 8 case × 3 evaluator seed × 128 env. 전체 12,288 episode행. 모든 정책·case·seed마다 128개 고유 env ID이며 3,072개의 동일 `(scenario,case,seed,env_id)` 키를 1:1 매칭했습니다. 중복 0, 누락 0.',
            '- `episode_id`는 전부 `-n0`, 1,000 step(20.0초), `end_reason=timeout`, `survived=true`, `base_contact_failure=false`. 후속 reset/restart episode나 조기 종료는 기록되지 않습니다. H1/H3 등 모두 고정 명령 시간창이 동일합니다.',
            '- 동일 key의 **대응 변화량은 유용한 기술통계**지만 동일 terrain realization·관절 trajectory를 의미하지 않습니다. 128개 env는 같은 훈련의 128번 독립 실험이 아니고 evaluator seed 3개도 학습 seed 반복 3개가 아닙니다. 유의성 p값/독립 샘플 3072개인 CI를 계산하지 않았습니다. seed 3개 범위와 paired 방향을 기술합니다.',
            '', '## 3. 핵심 지표 절댓값과 주요 변화량',
            '', '값은 cohort 전체 산술평균(별도 표시된 H5 P05/min은 분포 통계)입니다. Δ는 **앞 정책 − 뒤 정책**; forward progress는 증가가 좋고 오차·절대 누수·stall은 감소가 좋습니다. yaw는 rad/s, 선속도 오차는 m/s, 진행·world XY는 m입니다.',
            '', '| 진단 | A | B | C | D | C−B | C−D | C−A |',
            '|---|---:|---:|---:|---:|---:|---:|---:|']
    main_metrics=[('H1 절대 body forward 누수 (m)','H1','flat','abs_forward_m'),
        ('H1 world XY 순변위 (m)','H1','flat','world_xy_net_m'),
        ('H3 vy 오차 (m/s)','H3','flat','vy_error'),('H3 yaw 오차 (rad/s)','H3','flat','yaw_error'),
        ('H3 절대 body forward 누수 (m)','H3','flat','abs_forward_m'),
        ('H3 world XY 순변위—보조 (m)','H3','flat','world_xy_net_m'),
        ('H4 yaw 오차 (rad/s)','H4','flat','yaw_error'),
        ('H5 rough 진행 평균 (m)','H5','rough','forward_progress_m'),
        ('H5 rough mean tracking (혼합)','H5','rough','mean_tracking_error'),
        ('H5 rough mean stall','H5','rough','stall_fraction'),
        ('H5 rough stall>0.05 비율','H5','rough','stall_gt_005')]
    for name,sc,case,mt in main_metrics:
        rows.append('| '+name+' | '+' | '.join([cell(p,sc,mt,case) for p in POLICIES]+[scdelta(C,B,sc,mt,case),scdelta(C,D,sc,mt,case),scdelta(C,A,sc,mt,case)])+' |')
    rows += ['', 'H5 진행 lower-tail (모든 384 cohort를 포함; **하위 10% 제거 또는 채택 규칙 사용하지 않음**):',
            '', '| 정책 | 평균 (m) | P05 (m) | min (m) | P95 (m) | stall>0.05 |',
            '|---|---:|---:|---:|---:|---:|']
    for p in POLICIES:
        t=tailrow(p,'ALL',tails)
        rows.append(f"| {short[p]} | {t['mean_progress_m']:.3f} | {t['p05_progress_m']:.3f} | {t['min_progress_m']:.3f} | {t['p95_progress_m']:.3f} | {t['stall_gt_005_count']}/384 |")
    rows += ['', '### 우선 비교: C 대 B',
            '', f"- H5 진행 {scdelta(C,B,'H5','forward_progress_m','rough')}m; {cnt(C,B,'H5','forward_progress_m','rough')}. C의 P05 {vfmt(tailrow(C,'ALL',tails)['p05_progress_m'],3)}m vs B {vfmt(tailrow(B,'ALL',tails)['p05_progress_m'],3)}m; 최저값도 C {vfmt(tailrow(C,'ALL',tails)['min_progress_m'],3)}m vs B {vfmt(tailrow(B,'ALL',tails)['min_progress_m'],3)}m. 전체 tail 및 seed별 분리 표 참조.",
            f"- H1 body 누수 절댓값 {scdelta(C,B,'H1','abs_forward_m')}m ({cnt(C,B,'H1','abs_forward_m')}). 단 **world XY 순변위 평균**은 B {cell(B,'H1','world_xy_net_m')}→C {cell(C,'H1','world_xy_net_m')}m로 반드시 같이 기록합니다.",
            f"- H3 body-frame vy 오차 {scdelta(C,B,'H3','vy_error')}m/s ({cnt(C,B,'H3','vy_error')}); yaw 오차 {scdelta(C,B,'H3','yaw_error')}rad/s ({cnt(C,B,'H3','yaw_error')}). H3 world XY 종료 순변위는 응용 진단일 뿐 필수 복귀/성공 문턱이 아닙니다.",
            f"- H4 회전 yaw 오차 {scdelta(C,B,'H4','yaw_error')}rad/s ({cnt(C,B,'H4','yaw_error')}); C는 회전 축에서 B의 이점을 지키는지 별도 확인이 필요합니다.",
            '', '### 두 번째 비교: C 대 D',
            '', f"- H3 vy 오차 {scdelta(C,D,'H3','vy_error')}m/s ({cnt(C,D,'H3','vy_error')}), yaw 오차 {scdelta(C,D,'H3','yaw_error')}rad/s ({cnt(C,D,'H3','yaw_error')}) — 횡속도/회전 누수의 상충.",
            f"- H4 yaw 오차 {scdelta(C,D,'H4','yaw_error')}rad/s ({cnt(C,D,'H4','yaw_error')}). H5 진행 {scdelta(C,D,'H5','forward_progress_m','rough')}m ({cnt(C,D,'H5','forward_progress_m','rough')}); P05 C {vfmt(tailrow(C,'ALL',tails)['p05_progress_m'],3)} vs D {vfmt(tailrow(D,'ALL',tails)['p05_progress_m'],3)}m, min C {vfmt(tailrow(C,'ALL',tails)['min_progress_m'],3)} vs D {vfmt(tailrow(D,'ALL',tails)['min_progress_m'],3)}m.",
            '', '## 4. 8개 case 모두 검토: 추종·전진·자세·action 변화량',
            '', 'Mixed tracking은 평가기의 episode summary 혼합값이며 물리 단위가 하나가 아닙니다. 서로 다른 축의 지표를 합산한 승자 점수는 계산하지 않았습니다.',
            '', '| case | track A/B/C/D (↓) | C−B / C−D track Δ | forward A/B/C/D (m) | C−B / C−D forward Δ (m) |',
            '|---|---|---|---|---|']
    for sc,case in CASES:
        f=lambda m: '/'.join(cell(p,sc,m,case) for p in POLICIES)
        rows.append(f'| {sc}/{case} | {f("mean_tracking_error")} | {scdelta(C,B,sc,"mean_tracking_error",case)} / {scdelta(C,D,sc,"mean_tracking_error",case)} | {f("forward_progress_m")} | {scdelta(C,B,sc,"forward_progress_m",case)} / {scdelta(C,D,sc,"forward_progress_m",case)} |')
    rows += ['', '사전 지정한 나머지 회귀 검사(H2 forward, H6 slope-up/down, H7 push 포함)는 위 **전 case** 결과로 수행했습니다. H1/H3 `forward_progress_m`은 목표가 전진 0이므로 signed mean을 우열로 해석하지 말고 절대 누수와 vx 추종을 사용하십시오. H4에는 동시에 전진 0.5m/s 명령이 들어가므로 yaw만으로 전진 성능을 대신하지 않습니다.',
            '', '### 사전 정의된 case별 대응 악화 방향',
            '', '| 비교 | case | metric | 평균 Δ (candidate−reference) | 악화 / 전체 (%) |',
            '|---|---|---|---:|---|']
    checkpoints=[('H1','flat','abs_forward_m'),('H3','flat','vy_error'),('H3','flat','yaw_error'),
                 ('H4','flat','yaw_error'),('H5','rough','forward_progress_m'),
                 ('H5','rough','mean_tracking_error'),('H5','rough','stall_fraction'),
                 ('H2','flat','forward_progress_m'),('H6','slope_up','forward_progress_m'),
                 ('H6','slope_down','forward_progress_m'),('H7','push','forward_progress_m')]
    for c,r in COMPARISONS:
        for sc,case,mt in checkpoints:
            p=pair(c,r,sc,case,mt,paired_case)
            rows.append(f"| {c[0]}−{r[0]} | {sc}/{case} | `{mt}` | {p['mean_delta_candidate_minus_reference']:+.4f} | {p['worsened_n']}/{p['n_pairs']} ({p['worsened_fraction']*100:.1f}%) |")
    rows += ['', '세 축 회귀에서 보이는 추가 상충: C는 B보다 대부분 case에서 `vx_error`가 낮고 전진 적분은 개선되지만, H3/H4의 `vy_error`/`yaw_error`, 자세 `roll_pitch_rms`와 `action_delta_rms`(행동 변화 크기)는 B보다 증가합니다. 반면 D에 비해서는 C가 대부분 case의 yaw 축에서 유리하지만 lateral `vy_error`가 지속적으로 큽니다. 자세·action RMS는 별도 기록된 proxy이며 영상/물리적 보행 우열과 일대일 대응하지 않습니다.',
             '', '| case | C−B vx / vy / yaw 오차 Δ | C−B roll/pitch RMS Δ | C−B action Δ RMS 변화 |',
             '|---|---|---:|---:|']
    for sc,case in CASES:
        rows.append(f"| {sc}/{case} | {scdelta(C,B,sc,'vx_error',case)} / {scdelta(C,B,sc,'vy_error',case)} / {scdelta(C,B,sc,'yaw_error',case)} | {scdelta(C,B,sc,'roll_pitch_rms',case)} | {scdelta(C,B,sc,'action_delta_rms',case)} |")
    rows += ['', '평가 전체 episode `mean_tracking_error` (사전에 존재한 진단 요약·새 합성 점수 아님): '+', '.join(f'{short[p]} {statistics.fmean(show(p,sc,case,"mean_tracking_error",summ_case) for sc,case in CASES):.6f}' for p in POLICIES)+'. 이 수치만으로 후보를 고르지 않습니다.',
             '', '### 주요 개선/악화의 평가 seed별 확인',
             '', '| 비교 | case / 지표 | seed4201 Δ | seed4202 Δ | seed4203 Δ |',
             '|---|---|---:|---:|---:|']
    for c,r in ((C,B),(C,D)):
        for sc,case,mt in [('H1','flat','abs_forward_m'),('H3','flat','vy_error'),('H3','flat','yaw_error'),('H4','flat','yaw_error'),('H5','rough','forward_progress_m')]:
            arr=[next(x['mean_delta_candidate_minus_reference'] for x in paired_seed_case if x['candidate']==c and x['reference']==r and x['scenario']==sc and x['case']==case and x['metric']==mt and x['seed']==seed) for seed in (4201,4202,4203)]
            rows.append(f"| {c[0]}−{r[0]} | {sc}/{case} `{mt}` | {arr[0]:+.4f} | {arr[1]:+.4f} | {arr[2]:+.4f} |")
    rows += ['', '## 5. seed별 H5 rough 꼬리와 개선의 일관성',
            '', '| 정책 | 평가 seed | 진행 mean / P05 / min (m) | stall>0.05 | 최대 stall |',
            '|---|---:|---|---:|---:|']
    for p in POLICIES:
        for s in (4201,4202,4203):
            t=tailrow(p,s,tails)
            rows.append(f"| {short[p]} | {s} | {t['mean_progress_m']:.3f} / {t['p05_progress_m']:.3f} / {t['min_progress_m']:.3f} | {t['stall_gt_005_count']}/128 | {t['max_stall_fraction']:.4f} |")
    rows += ['', 'H5 seed별 paired 진행 변화량(각 seed에 128 env, 이들이 독립 학습 반복은 아님):',
            '', '| 비교 | seed 4201 (m) | seed 4202 (m) | seed 4203 (m) | seed Δ 최소..최대 (m) |',
            '|---|---:|---:|---:|---|']
    for c,r in COMPARISONS:
        v=[next(x['mean_delta_candidate_minus_reference'] for x in paired_seed_case if x['candidate']==c and x['reference']==r and x['scenario']=='H5' and x['case']=='rough' and x['metric']=='forward_progress_m' and x['seed']==s) for s in (4201,4202,4203)]
        rows.append(f"| {c[0]}−{r[0]} | {v[0]:+.3f} | {v[1]:+.3f} | {v[2]:+.3f} | {min(v):+.3f}..{max(v):+.3f} |")
    rows += ['', '## 6. 부모 A 대비 무엇을 유지했는가',
            '', f"- **H5 rough:** A 평균/P05/min {tailrow(A,'ALL',tails)['mean_progress_m']:.3f}/{tailrow(A,'ALL',tails)['p05_progress_m']:.3f}/{tailrow(A,'ALL',tails)['min_progress_m']:.3f}m; B {tailrow(B,'ALL',tails)['mean_progress_m']:.3f}/{tailrow(B,'ALL',tails)['p05_progress_m']:.3f}/{tailrow(B,'ALL',tails)['min_progress_m']:.3f}m; C {tailrow(C,'ALL',tails)['mean_progress_m']:.3f}/{tailrow(C,'ALL',tails)['p05_progress_m']:.3f}/{tailrow(C,'ALL',tails)['min_progress_m']:.3f}m; D {tailrow(D,'ALL',tails)['mean_progress_m']:.3f}/{tailrow(D,'ALL',tails)['p05_progress_m']:.3f}/{tailrow(D,'ALL',tails)['min_progress_m']:.3f}m. C는 B보다 회복되었지만 A의 강한 험지 진행을 유지하지 못했습니다.",
            f"- **H2/H6/H7 진행:** A→C 각각 H2 {cell(A,'H2','forward_progress_m')}→{cell(C,'H2','forward_progress_m')}m, H6 up {cell(A,'H6','forward_progress_m','slope_up')}→{cell(C,'H6','forward_progress_m','slope_up')}m, down {cell(A,'H6','forward_progress_m','slope_down')}→{cell(C,'H6','forward_progress_m','slope_down')}m, H7 {cell(A,'H7','forward_progress_m','push')}→{cell(C,'H7','forward_progress_m','push')}m. 전진은 유지에 가까운 정도가 있으나 원본 수준과 동일하지는 않습니다.",
            f"- **정지/횡명령:** A H1 절대 누수 {cell(A,'H1','abs_forward_m')}→C {cell(C,'H1','abs_forward_m')}m, H3 절대 누수 {cell(A,'H3','abs_forward_m')}→C {cell(C,'H3','abs_forward_m')}m로 감소. 그러나 H3 vy 오차 A {cell(A,'H3','vy_error')}→C {cell(C,'H3','vy_error')}m/s 증가: 전진 누수의 감소가 횡속도 명령 추종 개선을 의미하지는 않습니다.",
            '- A는 fresh3K 자동 best2700, B는 continuation endpoint4699, C/D는 keeper/selected4650이며 평가 날짜도 다릅니다. 동일 부모라는 external lineage 주장만으로 학습 길이·PPO 전체·checkpoint selector를 통제한 단일 reward 인과 실험이라고 단정할 수 없습니다.',
            '', '## 7. 지표·불확실성·미확인 근거',
            '', '- `forward_progress_m`와 `integrated_body_forward_m`는 **모든 행에서 정확히 동일 값**입니다. body-frame forward velocity의 signed 시간적분(단위 m)이고 world pathlength 또는 rough tile 실제 통과 거리가 아닙니다. H1/H3는 `abs_forward_m`를 비의도 전진 누수 보조 지표로 사용했습니다.',
            '- `world_xy_net_m=hypot(world_dx_m, world_dy_m)`은 **최종 세계좌표 순변위**이며 누적 path length가 아닙니다. 특히 H3 body-frame ±vy 명령은 world XY 원점 복귀 의무가 없습니다. `lateral_drift_m`는 evaluator 맥락상 vy 오차 크기의 시간적분으로, 실제 물리적 world-side displacement가 아닙니다.',
            '- `vx_error`/`vy_error`는 episode summary 속도축 오차(m/s), `yaw_error`는 yaw 각속도 오차(rad/s), `xy_rmse`/`yaw_rmse`는 해당 summary RMS. 세 축 통합 `mean_tracking_error`는 물리적으로 단일 단위가 없으며 공식 Tracking Score와 같지 않습니다. 이 입력에는 evaluator의 계산 함수 전체 소스가 없어 절댓값/평균의 exact 코드식·step별 가중과 제외 방식은 파일명/필드만으로 독립 증명할 수 없습니다.',
            '- `stall_fraction`은 명령 속도>0.2m/s 구간 중 관측 진행 속도<0.1m/s의 비율이라는 suite 임계값(코드 구현은 미동봉)을 사용한 evaluator summary입니다. H1 stall=0은 정지 유지 증거가 아닙니다. `stall>0.05`는 관찰 보고용 보조 빈도이며 채택/trim 기준이 아닙니다.',
            '- H5 P05는 **모든 n=384**를 포함한 선형보간 경험적 5백분위수(정렬 후 (n−1)×0.05 위치)입니다. 3개의 평가 seed에 의한 편차와 case별 차이를 보고하되 CI/p-value는 제공하지 않습니다(평가 seed 3개, 학습 seed 반복 부재). 각 seed는 128 env 관측값을 포함해 군집되어 있습니다.',
            '- 원자료는 case별 episode endpoint aggregate만 담고 있어 **H3 전반/후반 ±vy별 추종, 10초 전환 직후 과도응답, H4 ±yaw 구간별 추종, push 후 몇 초 내 회복, H5 rough 지형의 실제 patch 통과/슬립/계단·상자 성공, 발생시각/접촉 시계열**은 미확인입니다. 영상 파일도 이번 입력에는 없으므로 보행 동작을 직접 관찰하지 않았습니다.',
            '- 본 결과는 PERSONAL camera-off diagnostic이며 **공식 채점·공식 성공률·공식 점수 예측 또는 새로운 합성 점수**가 아닙니다. 원본 source_run_id/provenance를 임의 보완하지 않았습니다.',
            '', '## 8. 다음 행동 한 가지',
            '', '**새 평가·렌더·학습 없이 이 비교를 기록하고 C의 범용 후보 승격을 보류(HOLD)한다.** H5 하위꼬리/진행과 H3 vy·H4 yaw의 축별 trade-off를 기존 checkpoint/보고서의 판단 근거로 보존하고, 선택 기준을 사후 변경하지 않습니다.',
            '', '## 재현 산출물',
            '', '`csv/policy_case_metrics.csv`(모든 8 case × 4정책 × 지표), `csv/policy_seed_case_metrics.csv`(seed별), `csv/paired_case_metrics.csv`(5개 사전 정의 비교 × 8 case × 지표), `csv/paired_seed_case_metrics.csv`, `csv/paired_cohorts_key_metrics.csv`(키별 후보/reference 값과 Δ), `csv/h5_tail_by_seed.csv`, `csv/manifest_parity.csv`, `csv/policy_provenance.csv`, `csv/cohort_integrity.csv`, `PROVENANCE_AND_RUN.md`, `analyze_cohorts.py`. 후자는 동일 입력 ZIP을 직접 읽고 모든 표와 이 보고서를 다시 생성합니다.',
            '']
    return '\n'.join(rows)


def run(input_path, out):
    assert input_path.is_file()
    out.mkdir(parents=True,exist_ok=True)
    input_sha=digest(input_path.read_bytes())
    with ZipFile(input_path) as z:
        assert z.testzip() is None
        im,checks,manifests,resolutions,pubs,episodes,metrics,integrity,metadata=collect_input(z)
        summ_case,summ_seed_case,paired_case,paired_seed_case,paired_cohorts,tails=make_stats(metrics)
        parity=make_parity(manifests,resolutions)
        text=report_text(input_path,input_sha,checks,manifests,resolutions,pubs,integrity,
                         summ_case,summ_seed_case,paired_case,paired_seed_case,tails,metadata)
    folder=out/'csv'
    write_csv(folder/'policy_provenance.csv',metadata,list(metadata[0]))
    write_csv(folder/'manifest_parity.csv',parity,list(parity[0]))
    write_csv(folder/'cohort_integrity.csv',integrity,list(integrity[0]))
    write_csv(folder/'policy_case_metrics.csv',summ_case,list(summ_case[0]))
    write_csv(folder/'policy_seed_case_metrics.csv',summ_seed_case,list(summ_seed_case[0]))
    write_csv(folder/'paired_case_metrics.csv',paired_case,list(paired_case[0]))
    write_csv(folder/'paired_seed_case_metrics.csv',paired_seed_case,list(paired_seed_case[0]))
    write_csv(folder/'paired_cohorts_key_metrics.csv',paired_cohorts,list(paired_cohorts[0]))
    write_csv(folder/'h5_tail_by_seed.csv',tails,list(tails[0]))
    (out/'H1_FOUR_POLICY_COHORT_REPORT.md').write_text(text,encoding='utf-8')
    details=f'''# Provenance and reproduction

- Input: `{input_path.name}`
- Input ZIP SHA-256: `{input_sha}`
- ZIP archive member CRC tested with Python ZipFile.testzip() == None.
- `SHA256SUMS.txt`: {len(checks)} of {len(checks)} listed member checksums validated; `SHA256SUMS.txt` itself is not listed.
- Original inputs were opened read-only via ZipFile; no extraction, modification or posting.
- Evaluation raw checkpoint identifiers are assertions across `INPUT_MANIFEST.json`, evaluation manifest, evaluation link, and external publication metadata. **No `.pt` bytes included**, so checkpoint SHA is not a newly computed checksum.
- Raw evaluation `source_run_id=null`, `preset=null`, and publication imported-parent provenance remain unmodified and distinct from publication metadata mapping.
- Evaluator protocol parity is checked using full dict equality, full resolved config equality, source and applied environment fingerprints, not merely the protocol ID.
- Case keys required: scenario/case/seed/env_id; strict one `-n0` episode per case/seed/env and no restarts, all 20 seconds timeout. Missing, duplicate, reset or early-ended data fails the script rather than being silently omitted.
- Policy comparison order fixed before computing outputs: C−B, C−D, B−A, C−A, D−A. Every scenario/case included; no outcome-driven filtering.
- The sign of world XY net displacement is descriptive-only outside H1; H3 does NOT require world-origin return. Signed forward progress is descriptive-only for H1/H3 (zero forward command); absolute forward leakage is the meaningful comparison there. For descriptive-only metrics, improved/worsened/ties columns are deliberately blank, although delta values are preserved.
- P05 uses linear interpolation on sorted raw values at 0.05×(n−1); outliers are never trimmed. Sign counts use zero tolerance 1e-12 only.
- CSV files use UTF-8 BOM for Excel compatibility; decimal numbers remain full numeric precision.
- Runtime creating this package: Python `{platform.python_version()}`, system `{platform.system()}`. The analysis itself is Python standard-library only.

## Re-run (CPU only)

Place `analyze_cohorts.py` next to the input archive or point `--input` to the original ZIP. From a directory in which write access is available:

```bash
python analyze_cohorts.py \\
  --input /path/to/H1_LIN055_4POLICY_COHORT_INPUT_20261015.zip \\
  --out /path/to/recreated_results
```

No Isaac Sim, Torch, GPU, evaluator or video is invoked; reading source data and generating CSV/MD is the only action. Output directory is newly created or overwritten for same-name generated artifacts; source ZIP is never written. `INPUT_MANIFEST` was read first. Do not change provenance fields inside source JSON.

## Known limitations

This archive contains episode summaries and manifests, not evaluator implementation code, per-step trajectories, video, training resolved reward/PPO archives, actual terrain realization snapshots, or `.pt` checkpoint bytes. The publication linkage and training values come from supplied manifest metadata. Same evaluator fingerprint and cohort index do not certify matched physical trajectory. Three evaluator seeds are not independent training runs; no inferential confidence interval or significance test should be inferred from per-env paired fractions. No new official score is computed.
'''
    (out/'PROVENANCE_AND_RUN.md').write_text(details,encoding='utf-8')
    return { 'input_sha':input_sha,'policy_rows':[sum(k[:2]==(sc,case) for k in episodes[POLICIES[0]]) for sc,case in CASES],
             'parity_count':len(parity),'integrity_count':len(integrity),'paired_count':len(paired_cohorts),
             'h5_tails':{x['policy']:x for x in tails if x['seed']=='ALL'},
             'cb_h5_delta':pair(POLICIES[2],POLICIES[1],'H5','rough','forward_progress_m',paired_case)}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args()
    results=run(args.input,args.out)
    print(json.dumps(results,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
