#!/usr/bin/env python3
"""Recompute single-policy H1 scenario7 metrics from the original 18-item ZIP.
Usage: python recompute_metrics.py input.zip out_directory
Requires Python 3 with pandas and numpy. No GPU/video renderer. Input remains untouched.
"""
from pathlib import Path
import sys, json, zipfile, hashlib
import numpy as np
import pandas as pd

METRICS = ['mean_tracking_error','vx_error','vy_error','yaw_error','xy_rmse','yaw_rmse','forward_progress_m','lateral_drift_m','stall_fraction','roll_pitch_rms','action_delta_rms','world_norm_m']

def main(input_zip, target):
    target=Path(target); target.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(input_zip) as z:
        assert z.testzip() is None, 'ZIP CRC failure'
        m=json.loads(z.read('evaluation/evaluation_manifest.json'))
        d=json.loads(z.read('evaluation/diagnostics.json'))
        episodes=pd.DataFrame(json.loads(line) for line in z.read('evaluation/episodes.jsonl').decode().splitlines() if line.strip())
        links=json.loads(z.read('evaluation/video_evaluation_link.json'))
        src=z.read('source_checkpoint.txt').decode()
    sha=m['policy']['sha256']; proto=m['protocol_id']
    assert m['complete'] and m['execution_status']=='COMPLETE' and m['smoke'] is False
    assert links['source_checkpoint_sha256']==sha and links['protocol_id']==proto and sha in src
    assert len(episodes)==3072 and not episodes.episode_id.duplicated().any()
    assert (episodes.policy_sha256==sha).all() and (episodes.protocol_id==proto).all()
    assert not episodes[METRICS[:-1]].isna().any().any()
    assert np.allclose(episodes.forward_progress_m,episodes.integrated_body_forward_m)
    episodes['world_norm_m']=np.hypot(episodes.world_dx_m,episodes.world_dy_m)
    key=['scenario','case','seed','env_id']
    assert (episodes.groupby(key).size()==1).all(), 'More than one episode per cohort: use explicit cohort window logic'
    assert len(episodes.drop_duplicates(key))==3072
    assert (episodes.steps==1000).all() and (episodes.duration_s==20).all()
    assert (episodes.end_reason=='timeout').all() and episodes.survived.all() and (~episodes.base_contact_failure).all()
    bycase=episodes.groupby(['scenario','case'],sort=True)
    rows=[]
    for (s,c),f in bycase:
        r={'scenario':s,'case':c,'episodes':len(f),'cohorts':f[key].drop_duplicates().shape[0], 'terminated_cohorts':int(f.groupby(key).apply(lambda x:(x.end_reason=='terminated').any(),include_groups=False).sum()),'survival_fraction_episode':float(f.survived.mean())}
        for metric in METRICS:
            r[metric+'_mean']=float(f[metric].mean())
            r[metric+'_p05']=float(f[metric].quantile(.05))
            r[metric+'_p50']=float(f[metric].median())
            r[metric+'_p95']=float(f[metric].quantile(.95))
            r[metric+'_min']=float(f[metric].min())
            r[metric+'_max']=float(f[metric].max())
        r['stall_gt_0p05_count']=int((f.stall_fraction>.05).sum())
        rows.append(r)
    pd.DataFrame(rows).to_csv(target/'case_summary.csv',index=False,float_format='%.10g')
    rows=[]
    for (s,c,seed),f in episodes.groupby(['scenario','case','seed'],sort=True):
        r={'scenario':s,'case':c,'seed':int(seed),'episodes':len(f),'survival_fraction_episode':float(f.survived.mean())}
        for metric in METRICS:r[metric+'_mean']=float(f[metric].mean())
        r['progress_p05_m']=float(f.forward_progress_m.quantile(.05))
        rows.append(r)
    pd.DataFrame(rows).to_csv(target/'seed_case_summary.csv',index=False,float_format='%.10g')
    anomalies=pd.concat([episodes[(episodes.scenario=='H5') & (episodes.stall_fraction>.05)],episodes[(episodes.scenario=='H3') & (episodes.world_norm_m>1.2)]],ignore_index=True)
    anomalies[key+['episode_id','mean_tracking_error','forward_progress_m','world_dx_m','world_dy_m','world_norm_m','stall_fraction','roll_pitch_rms','action_delta_rms','end_reason']].to_csv(target/'outlier_cohorts.csv',index=False,float_format='%.10g')
    diagnostics_diffs={}
    for s,summary in d['scenarios'].items():
        f=episodes[episodes.scenario==s]
        diagnostics_diffs[s]={'count_match':int(len(f))==summary['episodes'],'tracking_abs_delta':abs(float(f.mean_tracking_error.mean())-summary['mean_episode_tracking_error']),'survival_abs_delta':abs(float(f.survived.mean())-summary['survival_rate'])}
        assert diagnostics_diffs[s]['count_match'] and diagnostics_diffs[s]['tracking_abs_delta']<1e-10 and diagnostics_diffs[s]['survival_abs_delta']<1e-10
    q={'source_zip_name':Path(input_zip).name,'source_zip_sha256':hashlib.sha256(Path(input_zip).read_bytes()).hexdigest(), 'policy_sha256_from_metadata_only':sha, 'protocol_id':proto,'record_count':len(episodes),'distinct_cohorts':len(episodes.drop_duplicates(key)),'case_count':len(rows)//3,'terminated_episodes':int((episodes.end_reason=='terminated').sum()),'episode_tracking_mean':float(episodes.mean_tracking_error.mean()),'scenario_equal_weight_tracking_mean':float(episodes.groupby('scenario').mean_tracking_error.mean().mean()),'case_equal_weight_tracking_mean':float(episodes.groupby(['scenario','case']).mean_tracking_error.mean().mean()), 'diagnostics_reconciliation':diagnostics_diffs,'source_checkpoint_original_bytes_present_in_bundle':False}
    (target/'recompute_validation.json').write_text(json.dumps(q,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(q,ensure_ascii=False,indent=2))
if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: python recompute_metrics.py <original.zip> <out_dir>')
    main(sys.argv[1],sys.argv[2])
