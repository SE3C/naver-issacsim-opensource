#!/usr/bin/env python
"""Recompute H1 evaluation diagnostics from an untouched combined ZIP.
Usage: python recompute_metrics.py INPUT.zip OUTPUT_DIRECTORY
Requires pandas, numpy. Does not run Isaac Sim, load policy, or modify input.
"""
import argparse, hashlib, io, json, pathlib, zipfile
import numpy as np
import pandas as pd

METRICS = ["mean_tracking_error", "vx_error", "vy_error", "yaw_error", "xy_rmse", "yaw_rmse", "forward_progress_m", "stall_fraction", "roll_pitch_rms", "action_delta_rms", "lateral_drift_m"]
KEYS = ["scenario", "case", "seed", "env_id"]

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('source_zip',type=pathlib.Path)
    ap.add_argument('output_dir',type=pathlib.Path)
    args=ap.parse_args()
    args.output_dir.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(args.source_zip) as z:
        bad=z.testzip()
        manifest=json.loads(z.read('evaluation/evaluation_manifest.json'))
        diag=json.loads(z.read('evaluation/diagnostics.json'))
        link=json.loads(z.read('evaluation/video_evaluation_link.json'))
        source=z.read('source_checkpoint.txt').decode('utf-8-sig')
        ep=pd.DataFrame([json.loads(line) for line in io.TextIOWrapper(z.open('evaluation/episodes.jsonl'),encoding='utf-8') if line.strip()])
        sha_manifest=dict(line.split('  ',1) for line in z.read('SHA256SUMS.txt').decode().splitlines() if line.strip())
        sha_checks={name:hashlib.sha256(z.read(name)).hexdigest()==hash_id for hash_id,name in sha_manifest.items()}
        entries=z.namelist()
    ep['world_xy_net_m']=np.hypot(ep['world_dx_m'],ep['world_dy_m'])
    assert len(ep)==ep.episode_id.nunique() and ep.episode_id.notna().all(),"missing/duplicate episode ID"
    assert ep[KEYS].drop_duplicates().shape[0]==len(ep), "multi-episode cohort; change fixed-window calculation"
    assert np.allclose(ep.forward_progress_m,ep.integrated_body_forward_m), "progress alias differs"
    assert set(ep.policy_sha256)=={manifest['policy']['sha256']}
    assert set(ep.protocol_id)=={manifest['protocol_id']}
    assert source.split('source_checkpoint_sha256=')[1].splitlines()[0]==manifest['policy']['sha256']==link['source_checkpoint_sha256']
    groups=[]
    for (sc,case),g in ep.groupby(['scenario','case'],sort=False):
        row={'scenario':sc,'case':case,'episodes':len(g),'distinct_cohorts':len(g[KEYS].drop_duplicates()),'seed_count':g.seed.nunique(), 'terminated_episodes':int((g.end_reason=='terminated').sum()),'cohorts_with_termination':int(g.groupby(KEYS,dropna=False)['end_reason'].apply(lambda x:(x=='terminated').any()).sum()), 'survival_rate':g.survived.mean(), 'world_xy_net_m_mean':g.world_xy_net_m.mean()}
        for col in METRICS:
            row[col+'_mean']=g[col].mean()
            row[col+'_p05']=g[col].quantile(.05)
            row[col+'_p95']=g[col].quantile(.95)
            row[col+'_min']=g[col].min()
            row[col+'_max']=g[col].max()
        row['stall_gt_005_count']=int((g.stall_fraction>0.05).sum())
        groups.append(row)
    case=pd.DataFrame(groups)
    case.to_csv(args.output_dir/'case_metrics.csv',index=False,float_format='%.9f')
    seed_case=ep.groupby(['scenario','case','seed'],sort=False).agg(episodes=('episode_id','size'),survival_rate=('survived','mean'),**{k+'_mean':(k,'mean') for k in METRICS},world_xy_net_m_mean=('world_xy_net_m','mean')).reset_index()
    seed_case.to_csv(args.output_dir/'seed_case_metrics.csv',index=False,float_format='%.9f')
    rough=ep.query("scenario == 'H5' and case == 'rough'").copy().sort_values('forward_progress_m').head(20)
    rough[KEYS+['episode_id','forward_progress_m','stall_fraction','mean_tracking_error','vx_error','yaw_error']].to_csv(args.output_dir/'H5_worst20_cohorts.csv',index=False,float_format='%.9f')
    deviations={sc:float(abs(g.mean_tracking_error.mean()-diag['scenarios'][sc]['mean_episode_tracking_error'])) for sc,g in ep.groupby('scenario')}
    metadata={'archive_entries':len(entries),'zip_crc_bad_member':bad,'video_sha256_checks':sha_checks,'all_video_sha256_pass':all(sha_checks.values()),'checkpoint_sha':manifest['policy']['sha256'],'protocol_id':manifest['protocol_id'],'complete':manifest['complete'],'smoke':manifest['smoke'],'rows':len(ep),'distinct_episode_ids':ep.episode_id.nunique(),'distinct_cohorts':len(ep[KEYS].drop_duplicates()),'end_reasons':ep.end_reason.value_counts().to_dict(),'survived_total':int(ep.survived.sum()),'base_contact_failure_true':int((ep.base_contact_failure==True).sum()),'diagnostics_absolute_difference_by_scenario':deviations,'all_diagnostics_match_tol_1e-12':all(x<1e-12 for x in deviations.values()),'mixed_tracking_episode_weighted_mean':ep.mean_tracking_error.mean(),'scenario_equal_weight_mean':float(ep.groupby('scenario').mean_tracking_error.mean().mean()),'case_equal_weight_mean':float(ep.groupby(['scenario','case']).mean_tracking_error.mean().mean())}
    (args.output_dir/'validation.json').write_text(json.dumps(metadata,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(metadata,indent=2,ensure_ascii=False))

if __name__=='__main__':main()
