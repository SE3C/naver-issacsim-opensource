#!/usr/bin/env python3
"""Exercise only extracted pure Python functions from original worker via AST.
Never imports/launches Isaac Sim, AppLauncher, gym, torch, task, or any subprocess.
"""
import ast
import json
import os
from pathlib import Path
SOURCE = Path(os.environ.get('NCRC_SOURCE_DIR',str(Path(__file__).resolve().parent.parent/'source'/'ncrc_h1_end_to_end')))
tree=ast.parse((SOURCE/'evaluator'/'h1_eval_worker.py').read_text())
sel=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'_command_at','_tracking_mix'}]
assert len(sel)==2
mod=ast.Module(body=sel, type_ignores=[])
ns={}
exec(compile(mod,'<AST-only _command_at/_tracking_mix>', 'exec'),ns)
cmd=ns['_command_at']
times=[0.0,2.0,5.999,6.0,7.0,10.0,13.0,14.0,17.0,18.0,19.9]
out={'extracted_functions':['worker._command_at','worker._tracking_mix'],
     'H3_command_timeline':[{ 'time_s':t,'command':cmd('H3',t)} for t in times],
     'H4_command_timeline':[{ 'time_s':t,'command':cmd('H4',t)} for t in times],
     'H2_command_timeline':[{ 'time_s':t,'command':cmd('H2',t)} for t in times],
     'tracking_mix':{'H1':ns['_tracking_mix']('H1',0.5,0.9),
                     'H4':ns['_tracking_mix']('H4',0.5,0.9),
                     'H5':ns['_tracking_mix']('H5',0.5,0.9)}}
Path(__file__).with_name('worker_pure_results.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps(out,indent=2))
