#!/usr/bin/env python
"""Check only decision-changing values in supplied derived CSVs. No episode/MP4/native .pt access.

Run from the ZIP's top directory: python calculations/targeted_check.py
CSV output is reproducible from unmodified evidence/ files.
"""
from pathlib import Path
import csv

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / 'calculations' / 'targeted_numeric_checks.csv'

def read(rel):
    with (BASE / rel).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

case = read('evidence/sources/parent_comparison/csv/case_summary.csv')
case_idx = {(r['policy'],r['case_id']):r for r in case}
derived = read('evidence/sources/next_hypothesis/derived_case_L_vs_B.csv')
der_idx = {r['case']:r for r in derived}
rough_dir = {r['comparison']:r for r in read('evidence/sources/parent_comparison/csv/rough_paired_direction.csv')}
rough_l = {r['comparison']:r for r in read('evidence/sources/next_hypothesis/derived_H5_L_vs_B.csv')}
items=[]
def add(group, metric, left, right, left_val, right_val, unit, direction, source, detail):
    d=float(left_val)-float(right_val)
    items.append(dict(group=group,metric=metric,left=left,right=right,
                      left_value=f'{float(left_val):.9f}',right_value=f'{float(right_val):.9f}',
                      delta_left_minus_right=f'{d:.9f}',unit=unit,preferred_direction=direction,
                      source=source,qualification=detail))

pc='evidence/sources/parent_comparison/csv/case_summary.csv'
for scenario,field,unit,direction in (
  ('H1/flat','forward_progress_m_mean','m signed body x','abs zero'),
  ('H1/flat','world_net_m_mean','m world net magnitude','lower'),
  ('H3/flat','forward_progress_m_mean','m signed body x','abs zero'),
  ('H3/flat','vy_error_mean','m/s','lower'),
  ('H3/flat','world_net_m_mean','m world net magnitude','lower'),
  ('H4/flat','yaw_error_mean','rad/s','lower'),
  ('H5/rough','forward_progress_m_mean','m','higher'),
  ('H5/rough','forward_progress_m_p05','m','higher'),
  ('H5/rough','forward_progress_m_min','m','higher'),
  ('H5/rough','stall_fraction_max','fraction','lower')):
    b=case_idx[('B',scenario)];c=case_idx[('C',scenario)]
    add('C-B',scenario+' / '+field,'C','B',c[field],b[field],unit,direction,pc,
        'Parent A same; C selected4650 vs B endpoint4699, not controlled reward causality')

lp='evidence/sources/next_hypothesis/derived_case_L_vs_B.csv'
for scenario,field,unit,direction in (
  ('H3/flat','world_net','m','lower'),
  ('H3/flat','vy','m/s','lower'),
  ('H4/flat','yaw','rad/s','lower'),
  ('H5/rough','progress','m','higher')):
    r=der_idx[scenario]
    add('L-B',scenario+' / '+field,'L','B',r[field+'_L'],r[field+'_B'],unit,direction,lp,
        'Supplied cross-derived per-case aggregate; L selected4650 vs B endpoint4699')

assert int(rough_dir['C-B']['progress_increase'])==373
assert int(rough_dir['C-B']['progress_decrease'])==11
assert int(rough_dir['B-A']['progress_decrease'])==384
assert int(rough_l['L-B']['n_positive'])==384
assert int(rough_l['L-B']['n_negative'])==0
assert abs(float(rough_l['L-B']['mean_progress_delta_m']) - 1.6266836864383258)<1e-9
assert abs(float(rough_dir['C-B']['mean_progress_delta']) - 0.850111115)<1e-8
assert float(case_idx[('C','H5/rough')]['forward_progress_m_min'])<float(case_idx[('B','H5/rough')]['forward_progress_m_min'])
assert abs(float(der_idx['H3/flat']['world_net_L']) - 2.397547)<0.002

with OUT.open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(items[0].keys()))
    w.writeheader();w.writerows(items)
print(f'PASS: {len(items)} targeted aggregate comparisons; direction checks: C-B 373/11, B-A 384 decreases, L-B 384 increases')
print('Input = supplied derived CSVs only; no independent raw episode/video/native checkpoint reading')
