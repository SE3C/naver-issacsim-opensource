#!/usr/bin/env python
"""Cross-reference two *previously calculated CPU CSV bundles*, without episodes/MP4/GPU.

Usage: python derive_existing_cpu.py --input /path/H1_HYPOTHESIS_DISCOVERY_20261015.zip --output /path/out
Stdlib only. Does not execute code bundled in the input archive. Does not create training/evaluation runs.
"""
import argparse, csv, io, json, statistics, zipfile
from pathlib import Path

OLD='comparison_outputs\\H1_4policy_LINTRACK065_analysis_bundle_20261014.zip'
NEW='comparison_outputs\\H1_ACTRATE_PARENT_UNCHANGED_RESTORATION_COMPARISON_20261015.zip'

def load_csv(z, member):
    return list(csv.DictReader(io.StringIO(z.read(member).decode('utf-8-sig'))))

def percentile(v, q):
    a=sorted(v); p=(len(a)-1)*q; lo=int(p); hi=min(lo+1,len(a)-1)
    return a[lo]+(a[hi]-a[lo])*(p-lo)

def summary(values):
    return {'mean':statistics.fmean(values),'p05':percentile(values,0.05),'min':min(values),
            'max':max(values), 'p95':percentile(values,0.95)}

def write_csv(p, records, cols=None):
    if cols is None: cols=list(records[0])
    with open(p,'w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(records)

def process(input_zip, out):
    out.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(input_zip) as master:
        with zipfile.ZipFile(io.BytesIO(master.read(OLD))) as old, zipfile.ZipFile(io.BytesIO(master.read(NEW))) as new:
            former=load_csv(old,'analysis/rough_cohorts.csv')
            latest=load_csv(new,'csv/rough_matched_episodes.csv')
            oldcases=load_csv(old,'analysis/scenario_summary.csv')
            newcases=load_csv(new,'csv/case_summary.csv')
    # Name-only matches are NOT sufficient: preserve case, seed, env_id and A value equality check.
    byold={(x['policy'],int(x['seed']),int(x['env_id'])):x for x in former
           if x['scenario']=='H5' and x['case']=='rough'}
    bynew={(x['comparison'],int(x['seed']),int(x['env_id'])):x for x in latest
           if x['scenario']=='H5' and x['case']=='rough'}
    expected={(s,e) for s in (4201,4202,4203) for e in range(128)}
    for pol in ('2700','4650'):
        assert {(s,e) for (p,s,e) in byold if p==pol} == expected,pol
    assert {(s,e) for (p,s,e) in bynew if p=='B-A'}==expected
    rec=[]; mismatch=[]
    for seed,env in sorted(expected):
        a_old=byold['2700',seed,env]
        l=byold['4650',seed,env]
        ba=bynew['B-A',seed,env]
        a_new=float(ba['right_progress_m'])
        assert abs(float(a_old['forward_progress_m'])-a_new)<1e-6, (seed,env,'A mismatch')
        assert abs(float(a_old['tracking'])-float(ba['right_tracking']))<1e-6
        L=float(l['forward_progress_m']);B=float(ba['left_progress_m']);A=a_new
        rec.append({'seed':seed,'env_id':env,'A':A,'B':B,'L':L,
                    'L_tracking':float(l['tracking']),'B_tracking':float(ba['left_tracking']),
                    'L_stall':float(l['stall_fraction']),'B_stall':float(ba['left_stall']),
                    'L_vx':float(l['vx_error']),'L_vy':float(l['vy_error']),
                    'L_yaw':float(l['yaw_error'])})
    assert len(rec)==384
    joined=[]
    for name,left,right in [('L-B','L','B'),('L-A','L','A')]:
        vals=[r[left]-r[right] for r in rec]
        ss=summary(vals)
        joined.append({'comparison':name,'n_corresponding_keys':len(vals),
                       'mean_progress_delta_m':ss['mean'],
                       'p05_of_paired_deltas_m':ss['p05'],
                       'min_paired_delta_m':ss['min'],
                       'n_positive':sum(v>1e-9 for v in vals),
                       'n_negative':sum(v<-1e-9 for v in vals),
                       'mean_left_m':statistics.fmean(r[left] for r in rec),
                       'mean_right_m':statistics.fmean(r[right] for r in rec),
                       'marginal_p05_left_m':percentile([r[left] for r in rec],.05),
                       'marginal_p05_right_m':percentile([r[right] for r in rec],.05)})
    for met in ('tracking','stall'):
        vs=[r['L_'+met]-r['B_'+met] for r in rec]
        s=summary(vs)
        joined.append({'comparison':'L-B/'+met, 'n_corresponding_keys':len(vs),
                       'mean_progress_delta_m':s['mean'], 'p05_of_paired_deltas_m':s['p05'],
                       'min_paired_delta_m':s['min'],
                       'n_positive':sum(v>1e-9 for v in vs),
                       'n_negative':sum(v<-1e-9 for v in vs),
                       'mean_left_m':statistics.fmean(r['L_'+met] for r in rec),
                       'mean_right_m':statistics.fmean(r['B_'+met] for r in rec),
                       'marginal_p05_left_m':percentile([r['L_'+met] for r in rec],.05),
                       'marginal_p05_right_m':percentile([r['B_'+met] for r in rec],.05)})
    write_csv(out/'derived_H5_L_vs_B.csv',joined)
    omap={x['case']:x for x in oldcases if x['policy']=='4650'}
    nmap={x['case_id']:x for x in newcases if x['policy']=='B'}
    maps=[('H1_flat','H1/flat'),('H2_flat','H2/flat'),('H3_flat','H3/flat'),('H4_flat','H4/flat'),('H5_rough','H5/rough'),('H6_slope_up','H6/slope_up'),('H6_slope_down','H6/slope_down'),('H7_push','H7/push')]
    case=[]
    for o,n in maps:
        a,b=omap[o],nmap[n]
        d={'case':n,'n_old_L':int(a['n']), 'n_new_B':int(b['n_episodes'])}
        for col,ocol,ncol in [('tracking','mean_tracking_error_mean','mean_tracking_error_mean'),('vx','vx_error_mean','vx_error_mean'),('vy','vy_error_mean','vy_error_mean'),('yaw','yaw_error_mean','yaw_error_mean'),('progress','forward_progress_m_mean','forward_progress_m_mean'),('world_net','world_xy_m_mean','world_net_m_mean'),('posture','roll_pitch_rms_mean','roll_pitch_rms_mean'),('action_delta','action_delta_rms_mean','action_delta_rms_mean')]:
            v=float(a[ocol]);w=float(b[ncol]); d[col+'_L']=v;d[col+'_B']=w;d['delta_'+col+'_L_minus_B']=v-w
        case.append(d)
    write_csv(out/'derived_case_L_vs_B.csv',case)
    # Compact, independently regenerated scatter plot using cross-bundle case summaries.
    # x=absolute signed H1 body-forward leakage, y=mean H5 body-forward progress;
    # H4 yaw and H3 world residual are explicit annotations, not mixed into one score.
    o={x['case']:x for x in oldcases if x['policy']=='4650'}
    n={pol:{x['case_id']:x for x in newcases if x['policy']==pol} for pol in ('A','B','C')}
    pts=[]
    for pol,label in [('A','부모2700'),('B','무변경4699'),('C','복원4650')]:
        x=n[pol]
        pts.append({'id':pol,'name':label,
            'drift':abs(float(x['H1/flat']['forward_progress_m_mean'])),
            'rough':float(x['H5/rough']['forward_progress_m_mean']),
            'yaw':float(x['H4/flat']['yaw_error_mean']),
            'h3':float(x['H3/flat']['world_net_m_mean'])})
    pts.append({'id':'L','name':'lin=.65 4650',
        'drift':abs(float(o['H1_flat']['forward_progress_m_mean'])),
        'rough':float(o['H5_rough']['forward_progress_m_mean']),
        'yaw':float(o['H4_flat']['yaw_error_mean']),
        'h3':float(o['H3_flat']['world_xy_m_mean'])})
    import html
    x0,y0=105,380;w,h=595,310
    xfun=lambda v:x0+v/2.15*w
    yfun=lambda v:y0-(v-7.5)/2.9*h
    colors={'A':'#125979','B':'#a35b13','C':'#73439a','L':'#0e766b'}
    lines=['<svg xmlns="http://www.w3.org/2000/svg" width="890" height="525" viewBox="0 0 890 525">',
           '<rect width="890" height="525" fill="#ffffff"/>',
           '<text x="65" y="34" font-size="22" font-weight="700" font-family="sans-serif">H1 정지 body 누수와 H5 rough 진행의 상쇄</text>',
           '<text x="65" y="58" font-size="12" fill="#444" font-family="sans-serif">기존 CPU 요약값 / 서로 다른 체크포인트와 학습 경로 / yaw·횡복귀는 별도 비용</text>']
    for v in (8,8.5,9,9.5,10):
        yy=yfun(v)
        lines += [f'<line x1="{x0}" y1="{yy:.1f}" x2="{x0+w}" y2="{yy:.1f}" stroke="#dee3e8"/>',
                  f'<text x="{x0-10}" y="{yy+4:.1f}" text-anchor="end" font-size="12" font-family="sans-serif">{v:.1f}</text>']
    for v in (0,.5,1,1.5,2):
        xx=xfun(v)
        lines += [f'<line x1="{xx:.1f}" y1="{y0}" x2="{xx:.1f}" y2="{y0-h}" stroke="#eef1f4"/>',
                  f'<text x="{xx:.1f}" y="{y0+20}" text-anchor="middle" font-size="12" font-family="sans-serif">{v:.1f}</text>']
    lines += [f'<line x1="{x0}" y1="{y0-h}" x2="{x0}" y2="{y0}" stroke="#444"/>',
              f'<line x1="{x0}" y1="{y0}" x2="{x0+w}" y2="{y0}" stroke="#444"/>',
              f'<text x="{x0+w/2}" y="{y0+49}" text-anchor="middle" font-size="14" font-family="sans-serif">H1 |비명령 body x 적분| (m) ↓</text>',
              f'<text x="22" y="{y0-h/2}" transform="rotate(-90 22 {y0-h/2})" text-anchor="middle" font-size="14" font-family="sans-serif">H5 body 진행 평균 (m) ↑</text>']
    # Place concise side legend to avoid plot-label collisions.
    for idx,p in enumerate(pts):
        xx,yy=xfun(p['drift']),yfun(p['rough'])
        lines += [f'<circle cx="{xx:.1f}" cy="{yy:.1f}" r="8" fill="{colors[p["id"]]}" stroke="white" stroke-width="2"/>',
                  f'<text x="{xx+13:.1f}" y="{yy-8:.1f}" font-family="sans-serif" font-size="13" font-weight="bold" fill="{colors[p["id"]]}">{p["id"]}</text>']
        ty=107+idx*63
        lines += [f'<circle cx="720" cy="{ty-5}" r="6" fill="{colors[p["id"]]}"/>',
                  f'<text x="735" y="{ty}" font-size="13" font-weight="700" font-family="sans-serif">{html.escape(p["id"]+" "+p["name"])}</text>',
                  f'<text x="735" y="{ty+17}" font-size="12" font-family="sans-serif">H4 yaw {p["yaw"]:.3f}</text>',
                  f'<text x="735" y="{ty+34}" font-size="12" font-family="sans-serif">H3 world {p["h3"]:.3f}m</text>']
    lines += ['<text x="65" y="483" font-family="sans-serif" font-size="12" fill="#555">H1 body 누수는 부호를 제거하여 표시. world 복귀·vy 추종과 같지 않음.</text>',
              '<text x="65" y="503" font-family="sans-serif" font-size="12" fill="#555">L=lin=.65 resume, B=unchanged resume. 평가 seed 3개는 학습 seed 반복 아님.</text>', '</svg>']
    (out/'tradeoff_scatter.svg').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    # Important: H5 indices match the old and new A by rounded values; this is NOT same terrain/trajectory proof.
    info={'source_old':OLD+'!analysis/rough_cohorts.csv',
          'source_new':NEW+'!csv/rough_matched_episodes.csv',
          'original_A_progress_value_crosscheck':'384/384 abs difference <1e-6 m',
          'original_A_tracking_value_crosscheck':'384/384 abs difference <1e-6',
          'cohort_keys':'384/384 H5 case + evaluator_seed + env_id',
          'calculation':'existing CPU-derived CSV cross-table join; no episodes.jsonl, MP4, native checkpoint read',
          'warning':'same evaluation keys != guaranteed identical physics; evaluator seeds != independent training seeds; selected L4650 vs endpoint B4699',
          'old_L_checkpoint':'ce7ad58657f3dd744e7cf2b7531f3d7d455773dfc6fb135f39d8a55aa49dea70',
          'new_B_checkpoint':'722b35a127f7ae4209d94a9111ac5ee02071ba7f3b985dc9cdc0760bbe48f646'}
    (out/'method_and_checks.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('H5 cross:',json.dumps(joined,indent=2,ensure_ascii=False))
    print('H1,H3,H4,H5 case comparison:',*[{'case':x['case'],'d_yaw':x['delta_yaw_L_minus_B'],'d_world_net':x['delta_world_net_L_minus_B'],'d_progress':x['delta_progress_L_minus_B']} for x in case if x['case'] in ['H1/flat','H3/flat','H4/flat','H5/rough']],sep='\n')
    return rec,joined,case

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();process(args.input,args.output)
