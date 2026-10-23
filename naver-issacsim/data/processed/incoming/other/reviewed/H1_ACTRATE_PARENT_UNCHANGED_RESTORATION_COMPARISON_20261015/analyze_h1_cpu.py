#!/usr/bin/env python3
"""Reproduce H1 A/B/C camera-off scenario7 comparison from the original outer ZIP.
CPU only. Requires numpy, pandas, matplotlib; never modifies original input.
Usage: python analyze_h1_cpu.py --input <outer.zip> --output <derived_dir>
"""
import argparse, csv, hashlib, io, json, zipfile
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

KEY=['scenario','case','seed','env_id']
METRICS=['mean_tracking_error','vx_error','vy_error','yaw_error','xy_rmse','yaw_rmse','forward_progress_m','stall_fraction','roll_pitch_rms','action_delta_rms','world_net_m','lateral_drift_m']
CHKS={
 'A':'e54d3389e20ea913968ef8d3edbea5004368ff225fa6b94f73fcd91cf93ca7ae',
 'B':'722b35a127f7ae4209d94a9111ac5ee02071ba7f3b985dc9cdc0760bbe48f646',
 'C':'a8249db467a60015036bf229b0026b215a61e17859f1d302efe283af225b84ea',
}
ZIPCHKS={
 'A':'6270d299def2a3bcb8cc10253027898621dd65a00ad30baafde0cbcde03076e3',
 'B':'3b331610cdc776c253bf8c4a1a13a3201c9ee4aed417d1af94ef4735f57a543e',
 'C':'f3c5bd802479ab50b347984a122615a895343ccf418f9e66b4d846f83399f84c',
}
TARGET={'H1/flat':0.0,'H2/flat':15.0,'H3/flat':0.0,'H4/flat':10.0,'H5/rough':10.0,'H6/slope_up':20.0,'H6/slope_down':20.0,'H7/push':10.0}

def summarize(g,p,case):
 n=len(g); row={'policy':p,'case_id':case,'n_episodes':n,'n_seeds':g.seed.nunique(),
 'n_timeout':int((g.end_reason=='timeout').sum()),'n_contact_failure':int(g.base_contact_failure.sum()),
 'survival_fraction':g.survived.mean()}
 for m in METRICS:
  a=g[m].to_numpy(dtype=float)
  row.update({f'{m}_{stat}':val for stat,val in [('mean',a.mean()),('p05',np.quantile(a,.05)),('median',np.median(a)),('p95',np.quantile(a,.95)),('min',a.min()),('max',a.max())]})
 if case in TARGET and TARGET[case]>0:
  target=TARGET[case]; shortage=target-g.forward_progress_m
  row.update(command_integral_m=target,mean_shortfall_m=float(shortage.mean()),
   mean_positive_shortfall_m=float(shortage.clip(lower=0).mean()),
   p95_shortfall_m=float(shortage.quantile(.95)),
   n_below_command_integral=int((g.forward_progress_m<target).sum()),
   fraction_below_command_integral=float((g.forward_progress_m<target).mean()))
 else:
  row.update(command_integral_m=TARGET.get(case,np.nan),mean_shortfall_m=np.nan,
  mean_positive_shortfall_m=np.nan,p95_shortfall_m=np.nan,n_below_command_integral=np.nan,fraction_below_command_integral=np.nan)
 row.update(n_stall_gt_005=int((g.stall_fraction>0.05).sum()),
            n_stall_gt_01=int((g.stall_fraction>0.1).sum()))
 return row

def main():
 a=argparse.ArgumentParser();a.add_argument('--input',required=True,type=Path);a.add_argument('--output',required=True,type=Path)
 x=a.parse_args(); out=x.output; (out/'csv').mkdir(parents=True,exist_ok=True);(out/'figures').mkdir(exist_ok=True)
 src=x.input; D={}; M={};diag={};ident=[];checks=[]
 with zipfile.ZipFile(src) as outer:
  assert outer.testzip() is None,'outer ZIP CRC failure'
  for oi in outer.infolist():
   if not oi.filename.endswith('.zip'):continue
   s='A' if oi.filename.startswith('model_2700_') else 'B' if 'unchanged-cont2k_model_4699' in oi.filename else 'C' if 'return2700-2k_model_4650' in oi.filename else None
   if s is None:continue
   buf=outer.read(oi);zipsha=hashlib.sha256(buf).hexdigest()
   with zipfile.ZipFile(io.BytesIO(buf)) as z:
    assert z.testzip() is None,(s,'CRC')
    expected={l.split()[1]:l.split()[0] for l in z.read('SHA256SUMS.txt').decode('utf-8-sig').strip().splitlines()}
    vchecks={name:hashlib.sha256(z.read(name)).hexdigest()==digest for name,digest in expected.items()}
    if not all(vchecks.values()):raise ValueError(('video SHA mismatch',s,vchecks))
    M[s]=json.loads(z.read('evaluation/evaluation_manifest.json'))
    diag[s]=json.loads(z.read('evaluation/diagnostics.json'))
    D[s]=pd.read_json(io.BytesIO(z.read('evaluation/episodes.jsonl')),lines=True)
    df=D[s]
    df['world_net_m']=np.hypot(df.world_dx_m,df.world_dy_m)
    df['case_id']=df.scenario+'/'+df.case
    assert df[KEY].drop_duplicates().shape[0]==3072,(s,'key duplicates')
    assert len(df)==3072 and (df.steps==1000).all() and (df.duration_s==20).all()
    assert (df.episode_id.str.endswith('-n0')).all(),(s,'reset episodes should be preserved, not silently dropped')
    assert (df.forward_progress_m==df.integrated_body_forward_m).all(),(s,'forward alias')
    assert df.policy_sha256.eq(M[s]['policy']['sha256']).all()
    assert df.protocol_id.eq(M[s]['protocol_id']).all()
    assert M[s]['policy']['sha256']==CHKS[s]
    assert zipsha==ZIPCHKS[s],(s,'outer supplied nested digest differs')
    ident.append({'policy':s,'nested_zip':oi.filename,'zip_sha256_observed':zipsha,'zip_sha256_matched':True,
     'checkpoint_sha256_manifest':M[s]['policy']['sha256'],'policy_source_run_id':M[s]['policy']['source_run_id'],
     'protocol_id':M[s]['protocol_id'],'source_fingerprints_json':json.dumps(M[s]['source_fingerprints'],sort_keys=True),
     'resolved_configs_sha256':hashlib.sha256(z.read('evaluation/resolved_configs.json')).hexdigest(),
     'crc_ok':True,'video_sha_pass':sum(vchecks.values()),'video_n':len(vchecks),
     'episode_rows':len(df),'cohort_keys':len(df[KEY].drop_duplicates())})
 for s in 'ABC':assert s in D,'missing '+s
 parity={}
 for a1,b1 in [('A','B'),('B','C'),('A','C')]:
  for k in ['protocol','source_fingerprints','suite','task_config']:
   parity[f'{a1}_{b1}_{k}_identical']=M[a1][k]==M[b1][k]
  parity[f'{a1}_{b1}_resolved_sha_identical']=(ident['ABC'.index(a1)]['resolved_configs_sha256']==ident['ABC'.index(b1)]['resolved_configs_sha256'])
  parity[f'{a1}_{b1}_keyset_identical']=set(map(tuple,D[a1][KEY].to_numpy()))==set(map(tuple,D[b1][KEY].to_numpy()))
 assert all(parity.values()),parity
 pd.DataFrame(ident).to_csv(out/'csv/identity_audit.csv',index=False)
 (out/'csv/evaluation_parity.json').write_text(json.dumps(parity,ensure_ascii=False,indent=2),encoding='utf-8')
 cases=[];scenario=[];seed=[];recon=[]
 for s,d in D.items():
  cases += [summarize(g,s,k) for k,g in d.groupby('case_id',sort=True)]
  scenario +=[summarize(g,s,k) for k,g in d.groupby('scenario',sort=True)]
  seed += [(summarize(g,s,k) | {'seed':int(se)}) for (k,se),g in d.groupby(['case_id','seed'],sort=True)]
  for k,v in diag[s]['scenarios'].items():
   g=d[d.scenario==k]
   recon.append({'policy':s,'scenario':k,'n_raw':len(g),'n_diagnostics':v['episodes'],
    'mean_raw':g.mean_tracking_error.mean(),'mean_diagnostics':v['mean_episode_tracking_error'],
    'mean_absolute_difference':abs(g.mean_tracking_error.mean()-v['mean_episode_tracking_error']),
    'n_fail_raw':(~g.survived).sum(),'n_fail_diagnostics':v['failed_episodes'],
    'survival_raw':g.survived.mean(),'survival_diagnostics':v['survival_rate']})
 caseDF=pd.DataFrame(cases);caseDF.to_csv(out/'csv/case_summary.csv',index=False,float_format='%.9g')
 pd.DataFrame(scenario).to_csv(out/'csv/scenario_summary.csv',index=False,float_format='%.9g')
 pd.DataFrame(seed).to_csv(out/'csv/case_seed_summary.csv',index=False,float_format='%.9g')
 reconDF=pd.DataFrame(recon);reconDF.to_csv(out/'csv/diagnostics_reconciliation.csv',index=False,float_format='%.12g')
 assert reconDF.mean_absolute_difference.max()<1e-10
 allDF=[]
 for s,d in D.items():
  allDF.append({'policy':s,'episode_weighted_tracking':d.mean_tracking_error.mean(),
    'case_equal_tracking':d.groupby('case_id').mean_tracking_error.mean().mean(),
    'scenario_equal_tracking':d.groupby('scenario').mean_tracking_error.mean().mean(),
    'all_survival_rate':d.survived.mean(),'overall_action_delta_rms_ep_mean':d.action_delta_rms.mean(),
    'overall_roll_pitch_rms_ep_mean':d.roll_pitch_rms.mean(),
    'all_mean_vx_error':d.vx_error.mean(),'all_mean_vy_error':d.vy_error.mean(),
    'all_mean_yaw_error':d.yaw_error.mean()})
 pd.DataFrame(allDF).to_csv(out/'csv/overall_summary.csv',index=False,float_format='%.9g')
 pairs=[];rougheps=[]
 for left,right in [('C','B'),('B','A'),('C','A')]:
  xdf=D[left].set_index(KEY).sort_index();ydf=D[right].set_index(KEY).sort_index()
  assert xdf.index.equals(ydf.index)
  difference=xdf[METRICS]-ydf[METRICS]
  for k,g in difference.groupby(xdf.case_id):
   row={'comparison':f'{left}-{right}','case_id':k,'matched_episode_keys':len(g)}
   for m in METRICS:
    a=g[m]
    row.update({f'delta_{m}_mean':a.mean(),f'delta_{m}_p05':a.quantile(.05),f'delta_{m}_p95':a.quantile(.95),
      f'count_{m}_positive':int((a>0).sum()),f'count_{m}_negative':int((a<0).sum())})
   pairs.append(row)
  h=difference.xs('H5',level='scenario'); rawleft=xdf.xs('H5',level='scenario');rawright=ydf.xs('H5',level='scenario')
  for (case,se,e),v in h.iterrows():
   l=rawleft.loc[(case,se,e)];r=rawright.loc[(case,se,e)]
   rougheps.append({'comparison':f'{left}-{right}','scenario':'H5','case':case,'seed':se,'env_id':e,
    'left_progress_m':l.forward_progress_m,'right_progress_m':r.forward_progress_m,
    'delta_progress_m':v.forward_progress_m,
    'left_tracking':l.mean_tracking_error,'right_tracking':r.mean_tracking_error,'delta_tracking':v.mean_tracking_error,
    'left_stall':l.stall_fraction,'right_stall':r.stall_fraction,'delta_stall':v.stall_fraction,
    'left_action':l.action_delta_rms,'right_action':r.action_delta_rms,'delta_action':v.action_delta_rms,
    'left_roll_pitch':l.roll_pitch_rms,'right_roll_pitch':r.roll_pitch_rms})
 pd.DataFrame(pairs).to_csv(out/'csv/matched_case_deltas.csv',index=False,float_format='%.9g')
 pd.DataFrame(rougheps).to_csv(out/'csv/rough_matched_episodes.csv',index=False,float_format='%.9g')
 h5=[]
 for s,d in D.items():
  h=d[d.scenario=='H5']
  h5.append({'policy':s,'n':len(h),'progress_mean':h.forward_progress_m.mean(),
    'progress_p05':h.forward_progress_m.quantile(.05),'progress_median':h.forward_progress_m.median(),
    'progress_min':h.forward_progress_m.min(),'progress_p95':h.forward_progress_m.quantile(.95),
    'tracking_mean':h.mean_tracking_error.mean(),'tracking_p95':h.mean_tracking_error.quantile(.95),
    'tracking_max':h.mean_tracking_error.max(),'vx_error_mean':h.vx_error.mean(),
    'vy_error_mean':h.vy_error.mean(),'yaw_error_mean':h.yaw_error.mean(),
    'stall_mean':h.stall_fraction.mean(),'stall_p95':h.stall_fraction.quantile(.95),
    'stall_max':h.stall_fraction.max(),'stall_gt_005':int((h.stall_fraction>.05).sum()),
    'roll_pitch_mean':h.roll_pitch_rms.mean(),'action_mean':h.action_delta_rms.mean(),
    'command_integral_m':10.0,'n_shortfall_m_positive':int((h.forward_progress_m<10.0).sum()),
    'shortfall_mean_m':(10-h.forward_progress_m).mean(),'shortfall_p95_m':(10-h.forward_progress_m).quantile(.95),
    'shortfall_max_m':(10-h.forward_progress_m).max(),
    'sub_8m':int((h.forward_progress_m<8).sum()),'sub_9m':int((h.forward_progress_m<9).sum())})
 pd.DataFrame(h5).to_csv(out/'csv/rough_key_distribution.csv',index=False,float_format='%.9g')
 # Observe matched cohort directions, not independent training-seed replication.
 count=[]
 for pair in ['C-B','B-A','C-A']:
  g=pd.DataFrame(rougheps);g=g[g.comparison==pair]
  count.append({'comparison':pair,'n_matched_h5':len(g),'progress_increase':int((g.delta_progress_m>0).sum()),
    'progress_decrease':int((g.delta_progress_m<0).sum()),
    'mean_progress_delta':g.delta_progress_m.mean(),'min_progress_delta':g.delta_progress_m.min(),
    'tracking_lower':int((g.delta_tracking<0).sum()),'tracking_higher':int((g.delta_tracking>0).sum()),
    'stall_lower':int((g.delta_stall<0).sum()),'stall_higher':int((g.delta_stall>0).sum())})
 pd.DataFrame(count).to_csv(out/'csv/rough_paired_direction.csv',index=False,float_format='%.9g')
 # figure 1: empirical CDF and 10-m reference
 fig,ax=plt.subplots(figsize=(8.2,4.7),layout='constrained')
 for s in 'ABC':
  vals=np.sort(D[s].loc[D[s].scenario=='H5','forward_progress_m']);ax.plot(vals,np.arange(1,len(vals)+1)/len(vals),label=s,linewidth=2)
 ax.axvline(10,linestyle='--',linewidth=1.5,color='0.35',label='10 m command integral')
 ax.set(xlabel='H5 body-forward progress (m)',ylabel='Empirical cumulative fraction',title='Rough terrain: full 384-episode progress distribution');ax.grid(alpha=.2);ax.legend()
 fig.savefig(out/'figures/rough_progress_ecdf.png',dpi=170);plt.close(fig)
 # figure 2: mean/P05/worst per policy
 f,ax=plt.subplots(figsize=(8.2,4.7),layout='constrained')
 xx=np.arange(3)
 vals=pd.DataFrame(h5).set_index('policy').loc[list('ABC')]
 ax.plot(xx,vals.progress_mean,marker='o',label='Mean',linewidth=2)
 ax.plot(xx,vals.progress_p05,marker='s',label='P05',linewidth=2)
 ax.plot(xx,vals.progress_min,marker='^',label='Worst episode',linewidth=2)
 ax.axhline(10,linestyle='--',color='0.35',label='10m command integral')
 ax.set(xticks=xx,xticklabels=list('ABC'),ylabel='Body-forward progress (m)',title='Rough terrain: average recovery vs worst-tail decline')
 ax.grid(alpha=.25);ax.legend();f.savefig(out/'figures/rough_mean_p05_worst.png',dpi=170);plt.close(f)
 # figure 3: tracking components per case
 cc=caseDF.pivot(index='case_id',columns='policy',values='mean_tracking_error_mean').reindex(list(TARGET))
 f,ax=plt.subplots(figsize=(11.5,5.1),layout='constrained')
 xx=np.arange(len(cc));width=.25
 for i,s in enumerate('ABC'):ax.bar(xx+(i-1)*width,cc[s].values,width,label=s)
 ax.set(xticks=xx,xticklabels=cc.index, ylabel='Mean mixed vx/vy/yaw tracking error (no single unit)',title='scenario7: equal 384 episodes per case');ax.grid(alpha=.2,axis='y');ax.legend();f.savefig(out/'figures/scenario_tracking.png',dpi=165);plt.close(f)
 # figure 4: seed consistency, explicit not separate training seeds
 f,ax=plt.subplots(figsize=(8.5,4.8),layout='constrained');seeds=sorted(D['A'].seed.unique())
 for s in 'ABC':
  m=D[s].query("scenario=='H5'").groupby('seed').forward_progress_m.mean();ax.plot(seeds,[m[k] for k in seeds],marker='o',label=s,linewidth=2)
 ax.axhline(10,color='0.35',linestyle='--',label='10m command integral');ax.set(xticks=seeds,xlabel='Evaluator seed (each has 128 envs)',ylabel='H5 mean progress (m)',title='Across evaluator seeds; single training seed per policy');ax.grid(alpha=.2);ax.legend();f.savefig(out/'figures/rough_seed_consistency.png',dpi=165);plt.close(f)
 print('Verified all 3 ZIP CRC+video SHA; episodes',sum(len(q) for q in D.values()),'diagnostics max diff',reconDF.mean_absolute_difference.max())
 print(pd.DataFrame(h5).round(5).to_string(index=False))
 print('OVERALL',pd.DataFrame(allDF).round(6).to_string(index=False))
 print('H5 matched',pd.DataFrame(count).round(6).to_string(index=False))

if __name__=='__main__':main()
