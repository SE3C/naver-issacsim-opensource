"""CPU-only regression tests; temp SQLite DB, synthetic/manual fixture, no GPU."""
import contextlib
import copy
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.request
import urllib.error

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def http(port, path, data=None, *, raw=None, content_type='application/json'):
    payload = None if data is None and raw is None else (json.dumps(data, allow_nan=False).encode() if raw is None else raw)
    req = urllib.request.Request(f'http://127.0.0.1:{port}{path}', data=payload)
    if payload is not None:
        req.add_header('Content-Type', content_type)
    try:
        with urllib.request.urlopen(req, timeout=10) as res:
            return res.status, json.load(res)
    except urllib.error.HTTPError as err:
        return err.code, json.load(err)


class Service:
    def __init__(self, tmp):
        self.tmp = Path(tmp)
        self.config = self.tmp/'config.json'
        shutil.copy(ROOT/'study_config.json', self.config)
        self.db = self.tmp/'cpu.db'
        self.history = self.tmp/'cpu.jsonl'
        self.proc = None
        self.port = None

    def run(self):
        cmd = [PYTHON, '-u', str(ROOT/'app.py'), '--port', '0', '--db', str(self.db), '--history', str(self.history), '--config', str(self.config)]
        self.proc = subprocess.Popen(cmd, cwd=str(ROOT), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        line = self.proc.stdout.readline()
        matched = re.search(r'http://127\.0\.0\.1:(\d+)/', line)
        if not matched:
            raise AssertionError(f'not started, rc={self.proc.poll()}: {line}')
        self.port = int(matched.group(1))
        return self

    def stop(self):
        if self.proc is not None:
            self.proc.terminate()
            try:self.proc.wait(timeout=6)
            except subprocess.TimeoutExpired:self.proc.kill();self.proc.wait(timeout=6)
            self.proc.stdout.close()
            self.proc = None

    def reload(self):
        self.stop()
        return self.run()

    def call(self, path, data=None, **kw):
        return http(self.port, path, data, **kw)

    def config_edit(self, *, objective=None, comparison=None, space=None):
        cfg = json.loads(self.config.read_text())
        if objective is not None:cfg['objective'] = objective
        if comparison is not None:cfg['comparison'] = comparison
        if space is not None:cfg['search_space'] = space
        self.config.write_text(json.dumps(cfg), encoding='utf-8')
        return cfg


OBJECTIVE = {'name':'MANUALLY_APPROVED_SYNTHETIC_FIXTURE_ONLY', 'unit':'fixture_units',
             'source':'synthetic test only, not official', 'direction':'maximize', 'min':0, 'max':1}
COMPARISON = {'protocol_id':'fixture-protocol', 'evaluator_id':'fixture-evaluator',
              'training_mode':'fresh', 'training_iterations':2000, 'training_seed':42,
              'checkpoint_selector':'final_numbered'}
SHA1='a'*64
SHA2='b'*64

def evidence(eval_id='eval-a', checkpoint=SHA1, **extra):
    obj = {'training_run_id':'fake-run-only-for-cpu-test', 'checkpoint_sha256':checkpoint,
           'evaluation_id':eval_id, 'protocol_id':'fixture-protocol', 'evaluator_id':'fixture-evaluator',
           'training_iterations':2000, 'training_seed':42, 'checkpoint_selector':'final_numbered',
           'resolved_reward_id':'synthetic-config-id'}
    obj.update(extra)
    return obj


class CpuHTTPTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.s = Service(self.temp.name).run()
        self.addCleanup(self.s.stop)
        self.stage = 'synthetic_stage'

    def call(self, path, obj=None, **kw):
        return self.s.call(path, obj, **kw)

    def ask(self):
        rc,res = self.call('/api/ask', {'stage':self.stage})
        self.assertEqual(rc,200,res)
        return res

    def setup_ready(self):
        self.s.stop()
        self.s.config_edit(objective=OBJECTIVE,comparison=COMPARISON)
        self.s.run()

    def test_initial_candidates_not_identical_and_reproducible(self):
        first=[self.ask()['params'] for _ in range(3)]
        self.assertEqual(len({json.dumps(x,sort_keys=True) for x in first}),3)
        self.assertEqual(self.call('/api/study?stage='+self.stage)[1]['counts']['RUNNING'],3)
        # A separate fresh SQLite starts with same first candidate (documented RNG policy).
        with tempfile.TemporaryDirectory() as other:
            fresh=Service(other).run()
            try:
                rc,p=fresh.call('/api/ask',{'stage':self.stage})
                self.assertEqual(rc,200)
                self.assertEqual(p['params'],first[0])
            finally:fresh.stop()

    def test_actual_process_restart_next_ask_and_db_restore(self):
        a=self.ask();b=self.ask()
        self.s.reload()
        rc,st=self.call('/api/study?stage='+self.stage)
        self.assertEqual(rc,200)
        self.assertEqual([t['number'] for t in st['trials']],[0,1])
        self.assertTrue(all(t['state']=='RUNNING' for t in st['trials']))
        c=self.ask()
        self.assertEqual(c['trial'],2)
        self.assertNotIn(c['params'], [a['params'],b['params']])

    def test_no_tell_without_config_even_after_record(self):
        a=self.ask()
        rc,r=self.call('/api/record',{'stage':self.stage,'trial':a['trial'],'evidence':evidence(),'decision':'UNDECIDED','diagnostic':'synthetic evidence'})
        self.assertEqual(rc,200,r)
        for val in (0,0.6,1):
            rc,res=self.call('/api/tell',{'stage':self.stage,'trial':a['trial'],'objective_value':val})
            self.assertEqual(rc,400,res)
            self.assertIn('BLOCKED',res['error'])
        self.assertEqual(self.call('/api/study?stage='+self.stage)[1]['trials'][0]['state'],'RUNNING')

    def test_manual_record_hold_reject_and_abandon(self):
        a=self.ask()
        for decision in ('HOLD','REJECT'):
            rc,r=self.call('/api/record', {'stage':self.stage,'trial':a['trial'], 'decision':decision,
                                            'diagnostic':'No scalar objective', 'evidence':{}})
            self.assertEqual(rc,200,r)
            self.assertEqual(r['record']['evidence']['checkpoint_sha256'],None)
            self.assertEqual(r['record']['decision'],decision)
        rc,r=self.call('/api/abandon', {'stage':self.stage,'trial':a['trial'], 'reason':'synthetic failed run'})
        self.assertEqual(rc,200,r)
        self.assertEqual(r['state'],'FAIL')
        self.s.reload()
        self.assertEqual(self.call('/api/study?stage='+self.stage)[1]['trials'][0]['state'],'FAIL')
        self.assertEqual(self.call('/api/abandon', {'stage':self.stage,'trial':0,'reason':'again'})[0],400)

    def test_stage_collision_prevention(self):
        self.assertEqual(self.call('/api/ask', {'stage':'alpha a'})[0],400)
        self.assertEqual(self.call('/api/ask', {'stage':'alphaa'})[0],200)
        self.assertEqual(self.call('/api/ask', {'stage':'alpha-a'})[0],200)
        self.assertEqual(self.call('/api/ask', {'stage':'A'*65})[0],400)
        self.assertEqual(self.call('/api/ask', {'stage':'한글'})[0],400)

    def test_safety_boundary_and_local_bind_only(self):
        self.assertEqual(self.call('/api/evaluate/start',{'stage':self.stage})[0],403)
        self.assertEqual(self.call('/api/tell-and-ask',{'stage':self.stage})[0],403)
        self.assertEqual(self.call('/api/evaluator')[0],404)
        cmd=[PYTHON,str(ROOT/'app.py'),'--host','0.0.0.0','--config',str(self.s.config)]
        r=subprocess.run(cmd,capture_output=True,text=True,timeout=10)
        self.assertNotEqual(r.returncode,0)
        self.assertIn('invalid choice',r.stderr)
        rc,r=self.call('/api/ask',{'stage':self.stage},content_type='text/plain')
        self.assertEqual(rc,415)

    def test_config_mutation_frozen_existing_stage(self):
        self.ask()
        self.s.stop()
        new_space={'action_rate_l2':[-0.0002,0.0]}
        self.s.config_edit(space=new_space)
        self.s.run()
        rc,status=self.call('/api/study?stage='+self.stage)
        self.assertFalse(status['config_matches'])
        self.assertEqual(self.call('/api/ask',{'stage':self.stage})[0],400)
        rc,r=self.call('/api/ask',{'stage':'different_stage'})
        self.assertEqual(rc,200,r)
        self.assertTrue(-0.0002<=r['params']['action_rate_l2']<=0)
        # Actual -0.0001 is expressible by explicitly configured new search bounds.
        self.assertTrue(new_space['action_rate_l2'][0] <= -0.0001 <= new_space['action_rate_l2'][1])

    def test_ready_tell_duplicate_invalid_and_recovery(self):
        self.setup_ready()
        a=self.ask();n=a['trial']
        # No score from UI is inferred or reused; legacy contradictory pair prohibited.
        self.assertEqual(self.call('/api/tell',{'stage':self.stage,'trial':n,'score_70':50,'objective':0.1})[0],400)
        self.assertEqual(self.call('/api/tell',{'stage':self.stage,'trial':n})[0],400)
        self.assertEqual(self.call('/api/tell',{'stage':self.stage,'trial':n,'objective_value':None})[0],400)
        for raw in (b'{"stage":"synthetic_stage","trial":0,"objective_value":NaN}',
                    b'{"stage":"synthetic_stage","trial":0,"objective_value":Infinity}'):
            self.assertEqual(self.call('/api/tell',raw=raw)[0],400)
        self.assertEqual(self.call('/api/tell',{'stage':self.stage,'trial':n,'objective_value':'0.5'})[0],400)
        self.assertEqual(self.call('/api/tell',{'stage':self.stage,'trial':n,'objective_value':-0.1})[0],400)
        self.assertEqual(self.call('/api/tell',{'stage':self.stage,'trial':n,'objective_value':1.1})[0],400)
        self.assertEqual(self.call('/api/tell',{'stage':self.stage,'trial':n,'objective_value':0})[0],400) # missing evidence
        self.assertEqual(self.call('/api/record',{'stage':self.stage,'trial':n,'evidence':evidence(protocol_id='wrong'),'decision':'UNDECIDED','diagnostic':''})[0],200)
        self.assertEqual(self.call('/api/tell',{'stage':self.stage,'trial':n,'objective_value':0.5})[0],400)
        self.assertEqual(self.call('/api/record',{'stage':self.stage,'trial':n,'evidence':evidence(),'decision':'HOLD','diagnostic':'hold'})[0],200)
        self.assertEqual(self.call('/api/tell',{'stage':self.stage,'trial':n,'objective_value':0.5})[0],400)
        self.assertEqual(self.call('/api/record',{'stage':self.stage,'trial':n,'evidence':evidence(),'decision':'UNDECIDED','diagnostic':'fixture'})[0],200)
        rc,r=self.call('/api/tell',{'stage':self.stage,'trial':n,'objective_value':0.5})
        self.assertEqual(rc,200,r)
        self.assertEqual(r['state'],'COMPLETE')
        self.assertEqual(self.call('/api/tell',{'stage':self.stage,'trial':n,'objective_value':0.6})[0],400)
        self.s.reload()
        t=self.call('/api/study?stage='+self.stage)[1]['trials'][0]
        self.assertEqual((t['state'],t['value'] ),('COMPLETE',0.5))
        self.assertEqual(t['record']['evidence']['checkpoint_sha256'],SHA1)
        self.assertEqual(self.call('/api/record',{'stage':self.stage,'trial':n,'evidence':evidence(),'diagnostic':'edit'})[0],400)
        # A new trial cannot use the same evaluation identity.
        a2=self.ask()
        self.call('/api/record',{'stage':self.stage,'trial':a2['trial'],'evidence':evidence(eval_id='eval-a',checkpoint=SHA2),'decision':'UNDECIDED','diagnostic':''})
        rc,r=self.call('/api/tell',{'stage':self.stage,'trial':a2['trial'],'objective_value':0.8})
        self.assertEqual(rc,400)
        self.assertIn('evaluation_id',r['error'])


    def test_explicit_fixed_action_value_new_stage(self):
        self.s.stop()
        self.s.config_edit(space={'action_rate_l2':[-0.0001,-0.0001]})
        self.s.run()
        first=self.s.call('/api/ask',{'stage':'fixed_action_fixture'})[1]
        second=self.s.call('/api/ask',{'stage':'fixed_action_fixture'})[1]
        self.assertEqual(first['params'],{'action_rate_l2':-0.0001})
        self.assertEqual(second['params'],{'action_rate_l2':-0.0001})
        # Deliberately fixed identical candidates are not a sampler-seed regression.

    def test_tell_missing_or_bad_sha_and_comparison_seed(self):
        self.setup_ready()
        n=self.ask()['trial']
        bad=evidence(checkpoint_sha256='unverified')
        rc,_=self.call('/api/record',{'stage':self.stage,'trial':n,'evidence':bad,'decision':'UNDECIDED','diagnostic':''})
        self.assertEqual(rc,400)
        no_sha=evidence(checkpoint_sha256=None)
        self.assertEqual(self.call('/api/record',{'stage':self.stage,'trial':n,'evidence':no_sha,'decision':'UNDECIDED','diagnostic':''})[0],200)
        rc,r=self.call('/api/tell',{'stage':self.stage,'trial':n,'objective_value':0.4})
        self.assertEqual(rc,400)
        self.assertIn('checkpoint_sha256',r['error'])
        wrong_seed=evidence(training_seed=99)
        self.assertEqual(self.call('/api/record',{'stage':self.stage,'trial':n,'evidence':wrong_seed,'decision':'UNDECIDED','diagnostic':''})[0],200)
        rc,r=self.call('/api/tell',{'stage':self.stage,'trial':n,'objective_value':0.4})
        self.assertEqual(rc,400)
        self.assertIn('training_seed',r['error'])

    def test_history_write_failure_does_not_hide_complete(self):
        self.setup_ready()
        a=self.ask()
        self.call('/api/record',{'stage':self.stage,'trial':a['trial'],'evidence':evidence(),'decision':'UNDECIDED','diagnostic':''})
        self.s.stop()
        self.s.history.unlink(missing_ok=True)
        self.s.history.mkdir()  # append will raise IsADirectoryError, DB tell must remain complete
        self.s.run()
        rc,r=self.call('/api/tell',{'stage':self.stage,'trial':a['trial'],'objective_value':0.3})
        self.assertEqual(rc,200,r)
        self.assertIn('history unavailable',r['warning'])
        self.s.reload()
        t=self.call('/api/study?stage='+self.stage)[1]['trials'][0]
        self.assertEqual(t['state'],'COMPLETE')
        self.assertEqual(t['value'],0.3)

    def test_fail_resume_comparison_parent_check(self):
        self.s.stop()
        comp=dict(COMPARISON, training_mode='resume',parent_checkpoint_sha256=SHA2)
        self.s.config_edit(objective=OBJECTIVE,comparison=comp)
        self.s.run()
        a=self.ask()
        self.call('/api/record',{'stage':self.stage,'trial':a['trial'],'evidence':evidence(),'decision':'UNDECIDED','diagnostic':''})
        self.assertEqual(self.call('/api/tell',{'stage':self.stage,'trial':a['trial'],'objective_value':.4})[0],400)
        self.call('/api/record',{'stage':self.stage,'trial':a['trial'],'evidence':evidence(parent_checkpoint_sha256=SHA2),'decision':'UNDECIDED','diagnostic':''})
        self.assertEqual(self.call('/api/tell',{'stage':self.stage,'trial':a['trial'],'objective_value':.4})[0],200)


if __name__=='__main__':
    unittest.main(verbosity=2)
