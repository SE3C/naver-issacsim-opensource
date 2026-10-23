#!/usr/bin/env python
"""Reproduce native H1 scenario7 episode-weighted audit from an unmodified combined ZIP.
Usage: python reproduce_analysis.py INPUT.zip [OUTPUT_DIRECTORY]
Requires: pandas, numpy. No GPU/evaluator/MP4 creation. Existing output files are overwritten in output directory only.
"""
import sys,zipfile,json,pathlib,io,hashlib
from collections import Counter
import pandas as pd
import numpy as np

def main(inp,out):
    out=pathlib.Path(out);out.mkdir(exist_ok=True,parents=True)
    with zipfile.ZipFile(inp) as z:
        names=z.namelist(); bad=z.testzip(); assert not bad,("ZIP CRC failure",bad)
        manifest=json.loads(z.read('evaluation/evaluation_manifest.json'));diag=json.loads(z.read('evaluation/diagnostics.json'))
        link=json.loads(z.read('evaluation/video_evaluation_link.json'))
        config=json.loads(z.read('evaluation/resolved_configs.json'))
        rows=[json.loads(line) for line in z.read('evaluation/episodes.jsonl').splitlines() if line]
        video_checks={}
        for line in z.read('SHA256SUMS.txt').decode('utf-8-sig').splitlines():
            if not line.strip():continue
            declared,f=line.split('  ',1)
            calculated=hashlib.sha256(z.read(f)).hexdigest()
            video_checks[f]={'manifest_sha256':declared,'computed_sha256':calculated,'match':declared==calculated}
    df=pd.DataFrame(rows)
    assert len(df)>0
    sha=manifest['policy']['sha256'];protocol=manifest['protocol_id']
    df['world_xy_residual_m']=np.hypot(df.world_dx_m,df.world_dy_m)
    df['abs_body_progress_m']=df.forward_progress_m.abs()
    df['cohort_key']=df[['scenario','case','seed','env_id']].astype(str).agg('|'.join,axis=1)
    group=['scenario','case'];numerics=['mean_tracking_error','vx_error','vy_error','yaw_error','xy_rmse','yaw_rmse','forward_progress_m','abs_body_progress_m','world_dx_m','world_dy_m','world_xy_residual_m','lateral_drift_m','stall_fraction','roll_pitch_rms','action_delta_rms','duration_s']
    summary=df.groupby(group,sort=True).agg(episodes=('episode_id','size'),cohorts=('cohort_key','nunique'),survival=('survived','mean'),terminated=('end_reason',lambda x: int((x=='terminated').sum())), base_contact_failure=('base_contact_failure',lambda x:int(x.fillna(False).sum()) if x.notna().any() else None),**{k:(k,'mean') for k in numerics}).reset_index()
    for f in ['forward_progress_m','mean_tracking_error','stall_fraction','world_xy_residual_m','vy_error','yaw_error']:
        q=df.groupby(group)[f].quantile([.05,.50,.95]).unstack();q.columns=[f+'_'+str(int(v*100)).zfill(2) for v in q.columns];summary=summary.merge(q.reset_index(),on=group)
    summary['forward_progress_min']=df.groupby(group)['forward_progress_m'].min().values
    summary['stall_gt_005']=df.groupby(group)['stall_fraction'].apply(lambda x: int((x>.05).sum())).values
    summary.to_csv(out/'case_metrics.csv',index=False,float_format='%.9g')
    sg=df.groupby(group+['seed'],sort=True).agg(episodes=('episode_id','size'),survival=('survived','mean'),**{k:(k,'mean') for k in numerics}).reset_index()
    sg.to_csv(out/'case_seed_metrics.csv',index=False,float_format='%.9g')
    h5=df.query("scenario=='H5'").sort_values('forward_progress_m')
    h3=df.query("scenario=='H3'").sort_values('vy_error',ascending=False)
    h4=df.query("scenario=='H4'").sort_values('yaw_error',ascending=False)
    h1=df.query("scenario=='H1'").sort_values('world_xy_residual_m',ascending=False)
    outliers=pd.concat([h5.head(12).assign(outlier_class='H5 lowest progress'),h5.sort_values('stall_fraction',ascending=False).head(12).assign(outlier_class='H5 highest stall'),h3.head(10).assign(outlier_class='H3 highest vy error'),h4.head(10).assign(outlier_class='H4 highest yaw error'),h1.head(10).assign(outlier_class='H1 highest world residue')],ignore_index=True)
    outliers[['outlier_class','scenario','case','seed','env_id','episode_id','survived','end_reason','duration_s','mean_tracking_error','vx_error','vy_error','yaw_error','forward_progress_m','world_xy_residual_m','stall_fraction','roll_pitch_rms','action_delta_rms']].to_csv(out/'outlier_episodes.csv',index=False,float_format='%.9g')
    cohorts=df.groupby('cohort_key').agg(episode_count=('episode_id','size'),ever_terminated=('end_reason',lambda a:bool((a=='terminated').any())),terminated_count=('end_reason',lambda a:int((a=='terminated').sum())))
    diag_check={k:{'calculated_episodes':int(len(v)),'calculated_survival_rate':float(v.survived.mean()),'calculated_tracking_error':float(v.mean_tracking_error.mean()),'diagnostics_episodes':diag['scenarios'][k]['episodes'],'diagnostics_survival_rate':diag['scenarios'][k]['survival_rate'],'diagnostics_tracking_error':diag['scenarios'][k]['mean_episode_tracking_error']} for k,v in df.groupby('scenario')}
    episode_key=df['episode_id']
    check={
     'policy_sha256':sha,'protocol_id':protocol, 'policy_sha_match_manifest_link':sha==link['source_checkpoint_sha256'], 'policy_sha_all_episode_rows':bool((df.policy_sha256==sha).all()),'protocol_all_episode_rows':bool((df.protocol_id==protocol).all()), 'robot':manifest['robot'],'complete':manifest['complete'],'smoke':manifest['smoke'], 'execution_status':manifest['execution_status'],'raw_episodes':int(len(df)),'unique_episode_ids':int(episode_key.nunique()),'unique_cohorts':int(df.cohort_key.nunique()),'episode_rows_per_cohort_hist':dict(Counter(cohorts.episode_count.astype(str))),'case_counts':{f'{a}/{b}':int(len(g)) for (a,b),g in df.groupby(group)}, 'end_reason_counts':df.end_reason.value_counts(dropna=False).to_dict(), 'survived_counts':df.survived.value_counts(dropna=False).astype(int).to_dict(),'base_contact_missing':int(df.base_contact_failure.isna().sum()),'base_contact_true':int(df.base_contact_failure.fillna(False).sum()), 'cohorts_ever_terminated':int(cohorts.ever_terminated.sum()),'total_cohort_termination_count':int(cohorts.terminated_count.sum()),'duration_s_hist':{str(k):int(v) for k,v in df.duration_s.value_counts().items()},'progress_integrated_diff_max':float((df.forward_progress_m-df.integrated_body_forward_m).abs().max()),'diagnostics_crosscheck':diag_check, 'resolved_agent_keys':list(config['agent'].keys()),'resolved_case_seed_keys':list(config['environment_by_case_seed'].keys()),'overall_episode_weighted_tracking':float(df.mean_tracking_error.mean()),'overall_episode_weighted_survival':float(df.survived.mean()),'overall_case_equal_tracking':float(summary.mean_tracking_error.mean()),'sha256_input_zip':hashlib.sha256(pathlib.Path(inp).read_bytes()).hexdigest(),'video_sha256_checks':video_checks}
    (out/'verification.json').write_text(json.dumps(check,indent=2,ensure_ascii=False),encoding='utf8')
    try:
        import matplotlib.pyplot as plt
        fig,ax=plt.subplots(figsize=(9,4.5));ax.hist(df.query("scenario=='H5'")['forward_progress_m'],bins=28)
        ax.axvline(10,linestyle='--',label='Command-integrated target: 0.5 m/s × 20 s = 10 m')
        ax.axvline(float(df.query("scenario=='H5'")['forward_progress_m'].quantile(.05)),linestyle=':',label='H5 5th percentile')
        ax.set(xlabel='Body-frame forward progress (m)',ylabel='Episode count',title='H5 rough terrain: per-episode progress (n=384)')
        ax.legend(loc='upper right',fontsize=8);fig.tight_layout();fig.savefig(out/'h5_progress_histogram.png',dpi=160);plt.close(fig)
    except ImportError:
        print('Optional: matplotlib not installed; PNG chart omitted')
    print('CHECK',json.dumps({k:v for k,v in check.items() if k not in ('resolved_agent_keys','resolved_case_seed_keys','diagnostics_crosscheck')},indent=2,ensure_ascii=False))
    print('\nCASES\n',summary[['scenario','case','episodes','survival','mean_tracking_error','vx_error','vy_error','yaw_error','forward_progress_m','forward_progress_m_05','forward_progress_min','stall_fraction','stall_gt_005','roll_pitch_rms','world_xy_residual_m','action_delta_rms']].to_string(index=False,float_format=lambda x:f'{x:.5f}'))
    print('\nSEEDS\n',sg[['scenario','case','seed','mean_tracking_error','forward_progress_m','vy_error','yaw_error','stall_fraction']].to_string(index=False,float_format=lambda x:f'{x:.5f}'))
    print('\nWORST H5\n',outliers.query("outlier_class=='H5 lowest progress'")[['seed','env_id','forward_progress_m','stall_fraction','mean_tracking_error']].to_string(index=False))
if __name__=='__main__':
    if len(sys.argv)<2:raise SystemExit(__doc__)
    main(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else '.')
