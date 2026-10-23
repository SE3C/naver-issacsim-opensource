#!/usr/bin/env python3
"""NCRC PC-only Optuna Ask / manual Record / gated Tell service (v2).

SQLite (Optuna RDB) is authoritative for trial state; JSONL is best-effort audit.
No evaluator, training, reward editing, or remote service is executed here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sqlite3
import sys
import threading
import traceback
import webbrowser
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import optuna
from optuna.samplers import TPESampler
from optuna.trial import TrialState

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / 'index.html'
DB_PATH = ROOT / 'ncrc_optuna.db'
HISTORY_PATH = ROOT / 'optuna_history.jsonl'
CONFIG_PATH = ROOT / 'study_config.json'
SEED = 20260922
STARTUP_TRIALS = 8
LOCK = threading.RLock()  # Single-process/single-user: serialize ask/tell/record.
STUDIES = {}  # study name -> (Study, config hash); one sampler per process lifetime.
STAGE_RE = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,63}\Z')
SHA_RE = re.compile(r'[0-9a-fA-F]{64}\Z')
EVIDENCE_FIELDS = (
    'training_run_id', 'checkpoint_sha256', 'evaluation_id', 'protocol_id',
    'evaluator_id', 'parent_checkpoint_sha256', 'training_iterations',
    'training_seed', 'checkpoint_selector', 'resolved_reward_id',
    'evaluation_archive_sha256', 'notes',
)


def now():
    return datetime.now(timezone.utc).isoformat()


def stage_name(s):
    if not isinstance(s, str) or not STAGE_RE.fullmatch(s):
        raise ValueError('stage must be 1..64 ASCII letters/digits/._- and start alphanumeric; no silent normalization')
    return s


def study_name(s):
    return 'ncrc_h1__' + stage_name(s)


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def finite_number(x, field):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x):
        raise ValueError(f'{field} must be a finite JSON number (not missing/NaN/string)')
    return float(x)


def positive_int(x, field, allow_zero=False):
    if isinstance(x, bool) or not isinstance(x, int) or x < (0 if allow_zero else 1):
        raise ValueError(f'{field} must be a positive integer')
    return x


def load_config():
    data = json.loads(CONFIG_PATH.read_text(encoding='utf-8'))
    if data.get('schema_version') != 2:
        raise ValueError('study_config.json schema_version must equal 2')
    space = data.get('search_space')
    if not isinstance(space, dict) or not space:
        raise ValueError('search_space must explicitly list at least one parameter')
    for key, bounds in space.items():
        if not isinstance(key, str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*', key):
            raise ValueError(f'invalid parameter name: {key!r}')
        if not isinstance(bounds, list) or len(bounds) != 2:
            raise ValueError(f'search_space[{key}] must be [min,max]')
        lo, hi = (finite_number(bounds[0], f'{key} min'), finite_number(bounds[1], f'{key} max'))
        if lo > hi:
            raise ValueError(f'search_space[{key}] must have min <= max (equal values are an explicit fixed parameter)')
    context = data.get('reward_context')
    if not isinstance(context, dict) or not isinstance(context.get('baseline_config_id'), str) or not context['baseline_config_id'].strip():
        raise ValueError('reward_context.baseline_config_id is required (may explicitly say unverified)')
    obj = data.get('objective')
    if obj is not None:
        if not isinstance(obj, dict) or not all(isinstance(obj.get(k), str) and obj[k].strip() for k in ('name', 'unit', 'source', 'direction')):
            raise ValueError('objective requires name, unit, source, direction')
        if obj['direction'] not in ('maximize', 'minimize'):
            raise ValueError('objective.direction must be maximize or minimize')
        lo = finite_number(obj.get('min'), 'objective.min')
        hi = finite_number(obj.get('max'), 'objective.max')
        if lo >= hi:
            raise ValueError('objective.min must be less than objective.max')
    comp = data.get('comparison')
    if comp is not None:
        if not isinstance(comp, dict):
            raise ValueError('comparison must be object or null')
        for key in ('protocol_id', 'evaluator_id', 'training_mode', 'checkpoint_selector'):
            if not isinstance(comp.get(key), str) or not comp[key].strip():
                raise ValueError(f'comparison.{key} must be a nonempty string')
        if comp['training_mode'] not in ('fresh', 'resume'):
            raise ValueError('comparison.training_mode must be fresh or resume')
        positive_int(comp.get('training_iterations'), 'comparison.training_iterations')
        positive_int(comp.get('training_seed'), 'comparison.training_seed', allow_zero=True)
        if comp['training_mode'] == 'resume':
            if not valid_sha(comp.get('parent_checkpoint_sha256')):
                raise ValueError('resume comparison requires actual parent_checkpoint_sha256')
        elif comp.get('parent_checkpoint_sha256') not in (None, ''):
            raise ValueError('fresh comparison must have no parent checkpoint')
    return data


def valid_sha(s):
    return isinstance(s, str) and SHA_RE.fullmatch(s) is not None


def frozen_contract(cfg):
    # Lock even an unapproved objective/comparison, so editing config requires NEW stage.
    return {k: cfg.get(k) for k in ('schema_version', 'reward_context', 'search_space', 'objective', 'comparison')}


def storage_url():
    return 'sqlite:///' + DB_PATH.resolve().as_posix()


def init_records():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH, timeout=30) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS pc_trial_records (
            study_name TEXT NOT NULL, trial_number INTEGER NOT NULL,
            detail_json TEXT NOT NULL, updated_at TEXT NOT NULL,
            PRIMARY KEY (study_name, trial_number))''')


def record_read(name, number):
    with sqlite3.connect(DB_PATH, timeout=30) as conn:
        row = conn.execute('SELECT detail_json FROM pc_trial_records WHERE study_name=? AND trial_number=?', (name, number)).fetchone()
    return json.loads(row[0]) if row else {'evidence': {}, 'decision': None, 'diagnostic': ''}


def record_write(name, number, item):
    init_records()
    with sqlite3.connect(DB_PATH, timeout=30) as conn:
        conn.execute('INSERT INTO pc_trial_records VALUES(?,?,?,?) ON CONFLICT(study_name,trial_number) DO UPDATE SET detail_json=excluded.detail_json, updated_at=excluded.updated_at',
                     (name, number, json.dumps(item, allow_nan=False, ensure_ascii=False, sort_keys=True), now()))


def audit(event):
    try:
        HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
        with HISTORY_PATH.open('a', encoding='utf-8') as f:
            f.write(json.dumps({'time': now(), **event}, ensure_ascii=False, allow_nan=False) + '\n')
        return None
    except OSError as exc:
        # The Optuna RDB state already changed. Never report it as undone.
        return f'optional history unavailable: {exc}'


def _load_study(name):
    try:
        return optuna.load_study(study_name=name, storage=storage_url())
    except KeyError:
        return None


def _sample_seed(name, count):
    # Deterministic distinct startup seed after a RESTART; NOT RNG checkpointing.
    digest = hashlib.sha256(f'{SEED}:{name}:{count}'.encode('utf-8')).digest()
    return int.from_bytes(digest[:4], 'big')


def get_study(stage, *, create=False, config=None):
    name = study_name(stage)
    if name in STUDIES:
        return STUDIES[name][0]
    if not create:
        return _load_study(name)
    cfg = config if config is not None else load_config()
    old = _load_study(name)
    n = len(old.trials) if old is not None else 0
    sampler = TPESampler(seed=_sample_seed(name, n), n_startup_trials=STARTUP_TRIALS, multivariate=True)
    direction = cfg['objective']['direction'] if cfg.get('objective') else 'maximize'
    study = optuna.create_study(study_name=name, storage=storage_url(), direction=direction,
                                sampler=sampler, load_if_exists=True)
    STUDIES[name] = (study, canonical_hash(frozen_contract(cfg)))
    return study


def require_contract(study, cfg, *, initialize=False):
    current = frozen_contract(cfg)
    digest = canonical_hash(current)
    saved = study.user_attrs.get('pc_v2_contract')
    if saved is None:
        if study.get_trials(deepcopy=False):
            raise ValueError('existing study without v2 contract; use a new stage (legacy trials are preserved)')
        if initialize:
            study.set_user_attr('pc_v2_contract', current)
            study.set_user_attr('pc_v2_contract_hash', digest)
        else:
            raise ValueError('study has no frozen contract')
    elif saved != current:
        raise ValueError('study frozen contract differs from study_config.json; restore config or use a NEW stage')
    if cfg.get('objective') and study.direction.name.lower() != cfg['objective']['direction']:
        raise ValueError('study direction differs from objective direction')
    return digest


def find_trial(study, number):
    positive_int(number, 'trial', allow_zero=True)
    trials = {t.number: t for t in study.get_trials(deepcopy=False)}
    if number not in trials:
        raise ValueError(f'trial {number} does not exist')
    return trials[number]


def trial_dict(study, t):
    entry = record_read(study.study_name, t.number)
    return {'number': t.number, 'state': t.state.name, 'value': t.value,
            'params': dict(t.params), 'created_at': t.datetime_start.isoformat() if t.datetime_start else None,
            'record': entry, 'contract_hash': t.user_attrs.get('contract_hash')}


def summary(stage):
    with LOCK:
        cfg = load_config()
        stage = stage_name(stage)
        study = get_study(stage)
        if study is None:
            return {'exists': False, 'stage': stage, 'trials': [], 'config': cfg, 'tell_ready': False}
        trials = study.get_trials(deepcopy=False)
        locked = study.user_attrs.get('pc_v2_contract')
        return {'exists': True, 'stage': stage, 'study_name': study.study_name,
                'contract': locked, 'config_matches': locked == frozen_contract(cfg),
                'tell_ready': bool(locked == frozen_contract(cfg) and cfg.get('objective') and cfg.get('comparison')),
                'trials': [trial_dict(study, t) for t in trials],
                'counts': {s: sum(t.state.name == s for t in trials) for s in ('RUNNING', 'COMPLETE', 'FAIL', 'PRUNED')}}


def ask(stage):
    with LOCK:
        cfg = load_config()
        stage = stage_name(stage)
        init_records()
        study = get_study(stage, create=True, config=cfg)
        digest = require_contract(study, cfg, initialize=True)
        trial = study.ask()
        trial.set_user_attr('contract_hash', digest)
        params = {k: trial.suggest_float(k, *bounds) for k, bounds in cfg['search_space'].items()}
        warning = audit({'event': 'ask', 'stage': stage, 'trial': trial.number, 'params': params})
        return {'stage': stage, 'trial': trial.number, 'params': params, 'contract_hash': digest,
                'tell_ready': bool(cfg.get('objective') and cfg.get('comparison')), 'warning': warning}


def _evidence_from_body(evidence):
    if not isinstance(evidence, dict) or set(evidence) - set(EVIDENCE_FIELDS):
        raise ValueError('evidence must be an object with documented keys only')
    result = {}
    for key in EVIDENCE_FIELDS:
        val = evidence.get(key)
        if val in (None, ''):
            result[key] = None
            continue
        if key in ('training_iterations', 'training_seed'):
            result[key] = positive_int(val, key, allow_zero=key == 'training_seed')
        elif not isinstance(val, str) or not val.strip() or len(val) > 4096:
            raise ValueError(f'evidence.{key} must be a nonempty string')
        elif key.endswith('sha256'):
            if not valid_sha(val):
                raise ValueError(f'evidence.{key} must be full 64-digit SHA-256 hex')
            result[key] = val.lower()
        else:
            result[key] = val.strip()
    return result


def record(stage, number, evidence, decision, diagnostic):
    with LOCK:
        cfg = load_config()
        study = get_study(stage)
        if study is None:
            raise ValueError('study not found')
        require_contract(study, cfg)
        t = find_trial(study, number)
        if t.state != TrialState.RUNNING:
            raise ValueError(f'trial is {t.state.name}; record is immutable after finish')
        if decision not in (None, 'UNDECIDED', 'HOLD', 'REJECT', 'PROMOTE'):
            raise ValueError('decision must be UNDECIDED/HOLD/REJECT/PROMOTE or null')
        if not isinstance(diagnostic, str) or len(diagnostic) > 10000:
            raise ValueError('diagnostic must be text (max 10000 chars)')
        item = {'evidence': _evidence_from_body(evidence), 'decision': decision,
                'diagnostic': diagnostic, 'recorded_at': now(),
                'provenance': 'user-entered; not independently verified by this application'}
        record_write(study.study_name, number, item)
        return {'trial': number, 'state': t.state.name, 'record': item,
                'warning': audit({'event': 'record', 'stage': stage, 'trial': number, 'decision': decision})}


def validate_tell_evidence(study, cfg, number, item):
    comp = cfg.get('comparison')
    obj = cfg.get('objective')
    if not obj or not comp:
        raise ValueError('Tell BLOCKED: approved objective and comparison are not set in the frozen stage config')
    if item.get('decision') in ('HOLD', 'REJECT'):
        raise ValueError('Tell BLOCKED: HOLD/REJECT diagnostics cannot become an arbitrary numeric observation')
    ev = item.get('evidence') or {}
    required = ('training_run_id', 'checkpoint_sha256', 'evaluation_id', 'protocol_id',
                'evaluator_id', 'training_iterations', 'training_seed', 'checkpoint_selector', 'resolved_reward_id')
    missing = [k for k in required if ev.get(k) is None]
    if missing:
        raise ValueError('Tell BLOCKED: missing manual evidence: ' + ', '.join(missing))
    if not valid_sha(ev['checkpoint_sha256']):
        raise ValueError('invalid checkpoint SHA')
    for key in ('protocol_id', 'evaluator_id', 'training_iterations', 'training_seed', 'checkpoint_selector'):
        if ev[key] != comp[key]:
            raise ValueError(f'Tell BLOCKED: evidence {key} mismatches frozen comparison')
    # A baseline ID identifies the frozen reference, not the newly trained candidate's final config.
    # The actual resolved_reward_id is retained separately and not guessed from baseline or path.
    if comp['training_mode'] == 'resume':
        if not ev.get('parent_checkpoint_sha256') or ev['parent_checkpoint_sha256'].lower() != comp['parent_checkpoint_sha256'].lower():
            raise ValueError('Tell BLOCKED: parent checkpoint SHA mismatch/unknown')
    elif ev.get('parent_checkpoint_sha256'):
        raise ValueError('Tell BLOCKED: unexpected parent checkpoint in fresh study')
    for other in study.get_trials(deepcopy=False):
        if other.number != number and other.state == TrialState.COMPLETE:
            prev = record_read(study.study_name, other.number)['evidence'].get('evaluation_id')
            if ev['evaluation_id'] == prev:
                raise ValueError('Tell BLOCKED: evaluation_id was already used by another COMPLETE trial')


def tell(stage, number, value):
    with LOCK:
        cfg = load_config()
        study = get_study(stage)
        if study is None:
            raise ValueError('study not found')
        digest = require_contract(study, cfg)
        t = find_trial(study, number)
        if t.state != TrialState.RUNNING:
            raise ValueError(f'trial {number} already {t.state.name}; duplicate Tell rejected')
        if t.user_attrs.get('contract_hash') != digest:
            raise ValueError('trial contract identity mismatch')
        item = record_read(study.study_name, number)
        validate_tell_evidence(study, cfg, number, item)
        obj = cfg['objective']
        score = finite_number(value, 'objective_value')
        if not obj['min'] <= score <= obj['max']:
            raise ValueError(f'objective_value outside configured [{obj["min"]}, {obj["max"]}]')
        study.tell(number, score)
        warning = audit({'event': 'tell', 'stage': stage, 'trial': number,
                         'objective_value': score, 'objective_name': obj['name']})
        return {'trial': number, 'state': 'COMPLETE', 'objective_value': score, 'warning': warning,
                'note': 'SQLite Optuna state is authoritative, including if history append fails'}


def abandon(stage, number, reason):
    with LOCK:
        if not isinstance(reason, str) or not reason.strip() or len(reason) > 1000:
            raise ValueError('failure/abandon reason (max 1000 chars) required')
        study = get_study(stage)
        if study is None:
            raise ValueError('study not found')
        t = find_trial(study, number)
        if t.state != TrialState.RUNNING:
            raise ValueError(f'trial {number} already {t.state.name}')
        item = record_read(study.study_name, number)
        item['abandon_reason'] = reason.strip()
        record_write(study.study_name, number, item)
        study.tell(number, state=TrialState.FAIL)
        warning = audit({'event': 'fail', 'stage': stage, 'trial': number, 'reason': reason})
        return {'trial': number, 'state': 'FAIL', 'warning': warning}


class Handler(BaseHTTPRequestHandler):
    server_version = 'NCRCOptunaPC/2.0'

    def log_message(self, fmt, *args):
        print(f'[{self.log_date_time_string()}] {fmt % args}', flush=True)

    def response(self, data, code=200):
        body = json.dumps(data, allow_nan=False, ensure_ascii=False, indent=2).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        try:
            if parsed.path in ('/', '/index.html'):
                body = INDEX.read_bytes()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(body)))
                self.send_header('Cache-Control', 'no-store')
                self.end_headers()
                self.wfile.write(body)
            elif parsed.path == '/api/health':
                self.response({'ok': True, 'version': '2.0.0', 'optuna_version': optuna.__version__,
                               'host': '127.0.0.1', 'db': str(DB_PATH), 'evaluator_enabled': False})
            elif parsed.path == '/api/config':
                self.response(load_config())
            elif parsed.path == '/api/study':
                stage = parse_qs(parsed.query).get('stage', ['legacy_h1_review'])[0]
                self.response(summary(stage))
            else:
                self.response({'error': 'endpoint not found; self evaluator disabled'}, 404)
        except (ValueError, KeyError, sqlite3.Error) as exc:
            self.response({'error': str(exc)}, 400)
        except Exception as exc:
            traceback.print_exc()
            self.response({'error': str(exc)}, 500)

    def do_POST(self):
        path = urlparse(self.path).path
        if path in ('/api/evaluate/start', '/api/tell-and-ask'):
            return self.response({'error': 'disabled: no self-evaluator or combined Tell+Ask in v2'}, 403)
        if self.headers.get('Content-Type', '').split(';')[0].strip().lower() != 'application/json':
            return self.response({'error': 'application/json required'}, 415)
        origin = self.headers.get('Origin')
        if origin and origin not in (f'http://127.0.0.1:{self.server.server_port}', f'http://localhost:{self.server.server_port}'):
            return self.response({'error': 'cross-origin requests are disabled'}, 403)
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if length < 1 or length > 200000:
                raise ValueError('JSON body required (<=200000 bytes)')
            body = json.loads(self.rfile.read(length).decode('utf-8'), parse_constant=lambda _: (_ for _ in ()).throw(ValueError('NaN/Infinity not allowed')))
            if not isinstance(body, dict):
                raise ValueError('JSON body must be object')
            stage = stage_name(body.get('stage'))
            if path == '/api/ask':
                result = ask(stage)
            elif path == '/api/record':
                result = record(stage, body.get('trial'), body.get('evidence', {}), body.get('decision'), body.get('diagnostic', ''))
            elif path == '/api/tell':
                if set(body) & {'score_70', 'objective', 'calibration'}:
                    raise ValueError('legacy score_70/objective/calibration fields forbidden; send one objective_value')
                result = tell(stage, body.get('trial'), body.get('objective_value'))
            elif path == '/api/abandon':
                result = abandon(stage, body.get('trial'), body.get('reason'))
            else:
                return self.response({'error': 'endpoint not found'}, 404)
            self.response(result)
        except (ValueError, KeyError, TypeError, sqlite3.Error) as exc:
            self.response({'error': str(exc)}, 400)
        except Exception as exc:
            traceback.print_exc()
            self.response({'error': str(exc)}, 500)


def main():
    global DB_PATH, HISTORY_PATH, CONFIG_PATH
    ap = argparse.ArgumentParser(description='PC-local Optuna manual Ask/Tell, evaluator disabled')
    ap.add_argument('--host', default='127.0.0.1', choices=['127.0.0.1'], help='loopback only')
    ap.add_argument('--port', type=int, default=8765)
    ap.add_argument('--db', type=Path, default=DB_PATH)
    ap.add_argument('--history', type=Path, default=HISTORY_PATH)
    ap.add_argument('--config', type=Path, default=CONFIG_PATH)
    ap.add_argument('--open', action='store_true')
    args = ap.parse_args()
    DB_PATH, HISTORY_PATH, CONFIG_PATH = args.db, args.history, args.config
    load_config()
    init_records()
    http = ThreadingHTTPServer((args.host, args.port), Handler)
    url = f'http://127.0.0.1:{http.server_port}/'
    print(f'NCRC Optuna PC v2 | Optuna {optuna.__version__} | {url} | DB {DB_PATH} | evaluator OFF', flush=True)
    if args.open:
        webbrowser.open(url)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        http.server_close()


if __name__ == '__main__':
    main()
