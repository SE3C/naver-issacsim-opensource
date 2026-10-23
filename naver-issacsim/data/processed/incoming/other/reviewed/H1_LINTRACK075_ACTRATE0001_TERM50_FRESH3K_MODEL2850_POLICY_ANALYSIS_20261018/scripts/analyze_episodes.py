#!/usr/bin/env python
"""Recompute H1 PERSONAL camera-off scenario7 episode statistics from episodes.jsonl.
Usage: python analyze_episodes.py PATH/TO/evaluation/episodes.jsonl --out PATH/TO/OUTPUT
No GPU, training, external network, or modification of input files.
"""
import argparse,json,pathlib
import numpy as np, pandas as pd
ap=argparse.ArgumentParser();ap.add_argument('episodes');ap.add_argument('--out',default='.');a=ap.parse_args()
out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
data=[json.loads(line) for line in open(a.episodes,encoding='utf8') if line.strip()]
df=pd.DataFrame(data)
df['case_key']=df['scenario']+'/'+df['case']
df['world_xy_distance_m']=np.hypot(df['world_dx_m'],df['world_dy_m'])
assert len(df)==3072, len(df)
assert df['episode_id'].is_unique
assert (df['forward_progress_m'] == df['integrated_body_forward_m']).all()
assert df.groupby(['scenario','case','seed','env_id']).size().max()==1
metrics=['mean_tracking_error','vx_error','vy_error','yaw_error','xy_rmse','yaw_rmse','forward_progress_m','world_dx_m','world_dy_m','world_xy_distance_m','lateral_drift_m','stall_fraction','roll_pitch_rms','action_delta_rms']
rows=[]
for (scenario,case),g in df.groupby(['scenario','case'],sort=True):
 rec={'scenario':scenario,'case':case,'episodes':len(g),'cohorts':g.groupby(['scenario','case','seed','env_id']).ngroups,'survival':g['survived'].mean(),'terminations':int((g['end_reason']=='terminated').sum()),'base_contact_failures':int((g['base_contact_failure']==True).sum()),'stalls_gt_005':int((g.stall_fraction>0.05).sum()),'stalls_gt_01':int((g.stall_fraction>0.1).sum())}
 for m in metrics:
  col=g[m].dropna().astype(float)
  for suffix,fn in [('mean',np.mean),('p05',lambda v:np.quantile(v,.05)),('p50',np.median),('p95',lambda v:np.quantile(v,.95)),('min',np.min),('max',np.max)]:
   rec[m+'_'+suffix]=float(fn(col)) if len(col) else None
 rows.append(rec)
case_df=pd.DataFrame(rows);case_df.to_csv(out/'case_metrics.csv',index=False,float_format='%.9f')
seed=df.groupby(['scenario','case','seed'],as_index=False).agg(episodes=('episode_id','count'),survival=('survived','mean'),tracking=('mean_tracking_error','mean'),vx_error=('vx_error','mean'),vy_error=('vy_error','mean'),yaw_error=('yaw_error','mean'),progress_m=('forward_progress_m','mean'),progress_p05=('forward_progress_m',lambda x:x.quantile(.05)),progress_min=('forward_progress_m','min'),stall=('stall_fraction','mean'),stall_max=('stall_fraction','max'),world_xy_m=('world_xy_distance_m','mean'),roll_pitch=('roll_pitch_rms','mean'),action_delta=('action_delta_rms','mean'))
seed.to_csv(out/'seed_case_metrics.csv',index=False,float_format='%.9f')
# Boundary cases and tails: keep concrete identifiers for audit.
ext=[]
for (scenario,case),g in df.groupby(['scenario','case'],sort=True):
 for m,good in [('forward_progress_m','lower'),('mean_tracking_error','higher'),('stall_fraction','higher'),('yaw_error','higher'),('vy_error','higher'),('roll_pitch_rms','higher')]:
  r=(g.nsmallest(3,m) if good=='lower' else g.nlargest(3,m))
  for rank,(_,x) in enumerate(r.iterrows(),1):
   ext.append({'scenario':scenario,'case':case,'metric':m,'kind':good,'rank':rank,'seed':int(x.seed),'env_id':int(x.env_id),'episode_id':x.episode_id,'value':float(x[m]),'survived':x.survived,'duration_s':float(x.duration_s),'end_reason':x.end_reason})
pd.DataFrame(ext).to_csv(out/'tail_episodes.csv',index=False,float_format='%.9f')
summary={'rows':len(df),'unique_episode_ids':int(df.episode_id.nunique()),'cohorts':int(df.groupby(['scenario','case','seed','env_id']).ngroups),'unique_seeds':sorted(df.seed.unique().tolist()),'counts_by_case':df.groupby('case_key').size().to_dict(),'end_reason':df.end_reason.value_counts().to_dict(),'policy_shas':df.policy_sha256.unique().tolist(),'protocols':df.protocol_id.unique().tolist(),'overall_episode_weighted':{m:float(df[m].mean()) for m in metrics},'case_equal_tracking':float(case_df['mean_tracking_error_mean'].mean()),'case_equal_survival':float(case_df['survival'].mean()),'cohort_ever_terminated_count':int(df.groupby(['scenario','case','seed','env_id'])['end_reason'].apply(lambda a:(a=='terminated').any()).sum()),'tracked_diagnostics':{},'case_rows':case_df[['scenario','case','episodes','mean_tracking_error_mean','forward_progress_m_mean','forward_progress_m_p05','forward_progress_m_min','stall_fraction_mean','stall_fraction_max']].to_dict('records')}
(out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print('OVERALL episode tracking:',summary['overall_episode_weighted']['mean_tracking_error'],'same case weighted',summary['case_equal_tracking']);print('CASE SUMMARY')
sel=['scenario','case','episodes','mean_tracking_error_mean','vx_error_mean','vy_error_mean','yaw_error_mean','forward_progress_m_mean','forward_progress_m_p05','forward_progress_m_min','world_xy_distance_m_mean','stall_fraction_mean','stall_fraction_max','stalls_gt_005','roll_pitch_rms_mean','action_delta_rms_mean']
print(case_df[sel].to_string(index=False,float_format=lambda x: f'{x:8.4f}'))
print('\nSEED rough + lateral+ balance + yaw:');print(seed[seed.scenario.isin(['H1','H3','H4','H5'])].to_string(index=False,float_format=lambda x: f'{x:8.4f}'))
print('\nH5 worst low progress');print(df[df.scenario.eq('H5')].nsmallest(8,'forward_progress_m')[['seed','env_id','forward_progress_m','mean_tracking_error','stall_fraction','roll_pitch_rms','world_dx_m','world_dy_m']].to_string(index=False))
print('\nH5 worst stalls');print(df[df.scenario.eq('H5')].nlargest(8,'stall_fraction')[['seed','env_id','forward_progress_m','mean_tracking_error','stall_fraction']].to_string(index=False))
print('\nH3 worst drift');print(df[df.scenario.eq('H3')].nlargest(8,'world_xy_distance_m')[['seed','env_id','forward_progress_m','world_dx_m','world_dy_m','world_xy_distance_m','vy_error']].to_string(index=False))
