#!/usr/bin/env python3
"""Isolated CPU-only probes for the unmodified ZIP app.py functions/API.
No Isaac Lab, no GPU, no app.main(), no external server, no original DB writes.
"""
import importlib.util
import os
import json
import tempfile
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
import sys

SOURCE = Path(os.environ.get('NCRC_SOURCE_DIR', str(Path(__file__).resolve().parent.parent / 'source' / 'ncrc_h1_end_to_end')))
spec = importlib.util.spec_from_file_location('ncrc_original_app_for_review', SOURCE / 'app.py')
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)
import optuna
optuna.logging.set_verbosity(optuna.logging.WARNING)

out = {'optuna_version': optuna.__version__, 'python_version': sys.version.split()[0]}
with tempfile.TemporaryDirectory(prefix='ncrc_cpu_only_review_') as tmp:
    app.DB_PATH = Path(tmp) / 'probe.db'
    app.HISTORY_PATH = Path(tmp) / 'history.jsonl'
    # Trial identity and reinitialized sampler: repeated first suggestion, distinct trial IDs.
    repeated=[]
    for i in range(3):
        st=app.get_study('seed_repeat')
        tr=st.ask()
        repeated.append({'trial':tr.number,'params':app.suggest_params(tr)})
    out['reinitialized_sampler']={
        'trials': repeated,
        'all_exactly_equal': all(t['params']==repeated[0]['params'] for t in repeated),
        'all_trial_numbers_distinct':len({t['trial'] for t in repeated})==len(repeated),
    }
    # Artificial eight COMPLETE outcomes with identical candidate vector:
    # demonstrates startup count is not a count of distinct reward configurations.
    startup_params=[]
    for i in range(8):
        s=app.get_study('startup_eight')
        t=s.ask(); pp=app.suggest_params(t);startup_params.append(pp)
        s.tell(t.number, 0.1+0.01*i)  # Synthetic objective values, NOT experimental data.
    s=app.get_study('startup_eight')
    ninth=s.ask();ninth_params=app.suggest_params(ninth)
    out['eight_completed_startup_synthetic']={'complete_count':8,
        'unique_first_eight_param_vectors':len({tuple(p.items()) for p in startup_params}),
        'ninth_trial':ninth.number, 'ninth_params':ninth_params,
        'note':'Outcomes are fabricated CPU fixtures; not H1 evidence.'}
    # Compare with same sampler instance (not reset).
    st = app.get_study('kept_sampler_instance')
    continuous=[]
    for i in range(3):
        tr=st.ask();continuous.append(app.suggest_params(tr))
    out['single_sampler_instance']={'all_exactly_equal':len({tuple(d.items()) for d in continuous})==1,
                                    'first_reward':continuous[0], 'second_reward':continuous[1]}
    # An empty-param trial can still be told: no evidence of training/evaluation.
    st=app.get_study('empty_params')
    tr=st.ask()
    st.tell(tr.number, 0.7)
    out['empty_param_tell']={'trial':tr.number,'params':st.trials[-1].params,
                              'state':st.trials[-1].state.name,'value':st.trials[-1].value}
    # Same stage name for two distinct user-visible stage strings.
    out['stage_collision']={'names':[app.study_name('alpha a'),app.study_name('alphaa')],
                            'collides':app.study_name('alpha a')==app.study_name('alphaa')}
    # Real localhost-only HTTP API, without starting app.main(): tests score/objective mismatch and duplicate tell.
    httpd=ThreadingHTTPServer(('127.0.0.1',0),app.Handler)
    thread=threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    base=f'http://127.0.0.1:{httpd.server_address[1]}'
    def post(path,payload):
        req=urllib.request.Request(base+path, json.dumps(payload).encode('utf8'),
                                   headers={'Content-Type':'application/json'},method='POST')
        try:
            with urllib.request.urlopen(req,timeout=5) as r:
                return r.status,json.load(r)
        except urllib.error.HTTPError as e:
            return e.code,json.load(e)
    try:
        astatus,asked=post('/api/ask',{'stage':'blind_tell'})
        body={'stage':'blind_tell','trial':asked['trial'],'score_70':10.0,
              'objective':1.0,'calibration':{'policy_sha256':'MISMATCH_OR_NONE','evidence':'fake'}}
        tstatus,told=post('/api/tell-and-ask',body)
        duplicate_status,duplicate=post('/api/tell-and-ask',body)
        out['api_blind_tell']={'ask_http':astatus,'tell_http':tstatus,'duplicate_http':duplicate_status,
            'sent_score_70':body['score_70'],'sent_objective':body['objective'],
            'score_div_70':body['score_70']/70,
            'stored_trial_value':app.get_study('blind_tell').trials[0].value,
            'stored_params':app.get_study('blind_tell').trials[0].params,
            'response_objective':told.get('objective'),
            'next_trial':told.get('next_trial'),
            'duplicate_error':duplicate.get('error')}
    finally:
        httpd.shutdown(); httpd.server_close();thread.join(5)
    # Simulate failure at process boundary after DB commit but before JSONL append.
    st=app.get_study('partial_failure')
    t=st.ask();app.suggest_params(t)
    st.tell(t.number,.5) # process fails BEFORE append_history in app.py sequence
    out['post_db_pre_history_crash_window']={
        'stored_state':app.get_study('partial_failure').trials[0].state.name,
        'tell_history_count':sum('"stage":"partial_failure"' in x and '"event":"tell"' in x
                                 for x in app.HISTORY_PATH.read_text().splitlines()),
        'note':'synthetic fault injection at the exact boundary; not an observed production crash'}
    # Fake small result aggregate: pure Python, no worker.
    spec2=importlib.util.spec_from_file_location('ncrc_original_aggregator_for_review',
                                                SOURCE/'evaluator'/'h1_evaluator.py')
    aggmod=importlib.util.module_from_spec(spec2);spec2.loader.exec_module(aggmod)
    rows={f'H{i}':{'score':0.5,'fall_rate':0.2,'xy_rmse':0.4,'yaw_rmse':0.9} for i in range(1,8)}
    out['synthetic_aggregate'] = aggmod.aggregate(rows)
    out['search_space']={'dimensions':len(app.SEARCH_SPACE),'action_rate_l2':app.SEARCH_SPACE['action_rate_l2'],
            'contains_minus_0_0001':app.SEARCH_SPACE['action_rate_l2'][0]<= -0.0001 <= app.SEARCH_SPACE['action_rate_l2'][1]}
Path(__file__).with_name('optuna_cpu_results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2))
