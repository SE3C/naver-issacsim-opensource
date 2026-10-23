param([string]$Path, [string]$ExpectedSHA256,
      [ValidateSet('maneuver_push')][string]$Scenario = 'maneuver_push',
      [string]$VideoResult,
      [ValidateRange(1,4096)][int]$EvaluationNumEnvs = 128,
      [string]$EvaluationSeeds = '4201,4202,4203', [string]$CompareWith)
$ErrorActionPreference = 'Stop'
$Work = $null
$Success = $false
$Mutex = New-Object System.Threading.Mutex($false, 'Local\Go2SixTerrainVideoSuite')
try { $Locked = $Mutex.WaitOne(0) } catch [System.Threading.AbandonedMutexException] { $Locked = $true }
if (-not $Locked) {
    Write-Host '[FAIL] Another Go2 video suite is already running.' -ForegroundColor Red
    $Mutex.Dispose()
    exit 1
}
try {
    Write-Host 'Go2 Windows Native - 6 Terrain Video Suite' -ForegroundColor Cyan
    if ([string]::IsNullOrWhiteSpace($Path)) { $Path = Read-Host 'Checkpoint .pt path' }
    $Checkpoint = [IO.Path]::GetFullPath($Path.Trim().Trim('"').Trim("'"))
    if (-not (Test-Path -LiteralPath $Checkpoint -PathType Leaf)) { throw 'Checkpoint does not exist.' }
    if ([IO.Path]::GetExtension($Checkpoint) -ine '.pt') { throw 'Checkpoint must be a .pt file.' }
    if ($VideoResult -and -not (Test-Path -LiteralPath $VideoResult -PathType Leaf)) { throw 'Saved video result JSON does not exist.' }
    if ($CompareWith -and (-not (Test-Path -LiteralPath $CompareWith -PathType Container))) { throw 'CompareWith requires a saved evaluation directory.' }
    $ScenarioText = @'
{
  "maneuver_push": {
    "label": "Forward, sideways, turns / timed side pushes",
    "phases": [
      {"start_step": 0, "end_step": 300, "velocity": [1.0, 0.0, 0.0]},
      {"start_step": 300, "end_step": 500, "velocity": [0.5, 0.3, 0.0]},
      {"start_step": 500, "end_step": 700, "velocity": [0.5, -0.3, 0.0]},
      {"start_step": 700, "end_step": 850, "velocity": [0.5, 0.0, 0.5]},
      {"start_step": 850, "end_step": 1000, "velocity": [0.5, 0.0, -0.5]}
    ],
    "pushes": [
      {"step": 200, "velocity_delta_world": [0.0, 0.5, 0.0]},
      {"step": 400, "velocity_delta_world": [0.0, -0.5, 0.0]},
      {"step": 600, "velocity_delta_world": [0.0, 0.5, 0.0]},
      {"step": 800, "velocity_delta_world": [0.0, -0.5, 0.0]}
    ]
  },
  "reverse": {
    "label": "Forward first, then reverse, sideways, turns / no pushes",
    "phases": [
      {"start_step": 0, "end_step": 300, "velocity": [1.0, 0.0, 0.0]},
      {"start_step": 300, "end_step": 500, "velocity": [-0.5, 0.0, 0.0]},
      {"start_step": 500, "end_step": 700, "velocity": [0.5, 0.3, 0.0]},
      {"start_step": 700, "end_step": 850, "velocity": [0.5, 0.0, 0.5]},
      {"start_step": 850, "end_step": 1000, "velocity": [0.5, 0.0, -0.5]}
    ],
    "pushes": []
  }
}

'@
    Write-Host '[FIXED SUITE] 6 terrains, one schedule, 20 seconds per video.' -ForegroundColor Cyan
    Write-Host ('[SCENARIO] ' + $Scenario)
    Write-Host 'Forward first, then sideways and turns. Side pushes at 4,8,12,16 seconds.'
    Write-Host ('[NEXT] Sequential camera-off Go2 scenario7 evaluation: ' + $EvaluationNumEnvs + ' environments; seeds=' + $EvaluationSeeds)
    foreach ($Required in @('C:\isaacsim\python.bat', 'C:\NCRC\IsaacLab\scripts\reinforcement_learning\rsl_rl\play.py', 'C:\NCRC\naver-issacsim-nvidia\training\quadruped\go2_task\__init__.py')) {
        if (-not (Test-Path -LiteralPath $Required)) { throw ('Missing required file: ' + $Required) }
    }
    if (Get-Process kit -ErrorAction SilentlyContinue) { throw 'Kit is already running. Close it before starting this suite.' }
    $BundleRoot = Join-Path $PSScriptRoot 'go2-video-evaluator'
    $Bundle = Get-Content -LiteralPath (Join-Path $BundleRoot 'bundle_manifest.json') -Raw -Encoding UTF8 | ConvertFrom-Json
    foreach ($Name in @('isaac_runner.py','eval_core.py','compare_cli.py')) {
        $File = Join-Path $BundleRoot $Name
        if ((Get-FileHash -LiteralPath $File -Algorithm SHA256).Hash.ToLowerInvariant() -ne $Bundle.file_sha256.$Name) { throw ('Evaluator bundle SHA256 mismatch: ' + $Name) }
    }
    $WorkBase = 'C:\NCRC\go2-video-suite-work'
    $Work = Join-Path $WorkBase ('suite-' + [guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $Work | Out-Null
    $env:OMNI_CONFIG_PATH = 'C:\ov-config'
    $env:ISAACLAB_PATH = 'C:\NCRC\IsaacLab'
    $env:WARP_CACHE_PATH = 'C:\ov\warp-cache'
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONUNBUFFERED = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    $env:HYDRA_FULL_ERROR = '1'
    Remove-Item Env:\NCRC_PLAY_PUSH -ErrorAction SilentlyContinue
    New-Item -ItemType Directory -Force -Path $env:WARP_CACHE_PATH | Out-Null
    $Config = @{ checkpoint=$Checkpoint; expected_sha256=$ExpectedSHA256; scenario=$Scenario;
                 video_result=$VideoResult;
                 evaluation_num_envs=$EvaluationNumEnvs; evaluation_seeds=$EvaluationSeeds; compare_with=$CompareWith }
    $Config | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $Work 'config.json') -Encoding UTF8
    [IO.File]::WriteAllText((Join-Path $Work 'scenarios.json'), $ScenarioText, [Text.Encoding]::ASCII)
    $RunnerSource = @'
import csv
import hashlib
import json
import math
from pathlib import Path
import runpy
import sys

WORK = Path(__file__).resolve().parent
SCENARIO = json.loads((WORK / 'scenario.json').read_text(encoding='utf-8'))
TASK = 'C:/NCRC/naver-issacsim-nvidia/training/quadruped'
PLAY = 'C:/NCRC/IsaacLab/scripts/reinforcement_learning/rsl_rl/play.py'
sys.path.insert(0, TASK)
sys.path.insert(0, str(Path(PLAY).parent))
import go2_task
import gymnasium as gym
import moviepy.video.io.ImageSequenceClip as clip_module


def command_for_step(step):
    for phase in SCENARIO['phases']:
        if step < phase['end_step']:
            return phase['velocity']
    return SCENARIO['phases'][-1]['velocity']


def trace_row(step, command, delta):
    return [str(step), f'{step * 0.02:.2f}'] + [f'{v:.6f}' for v in command + delta]


TRACE_HEADER = ['step', 'sim_seconds', 'target_vx_body_mps', 'target_vy_body_mps',
                'target_yaw_rate_radps', 'push_dvx_world_mps', 'push_dvy_world_mps', 'push_dvz_world_mps']
PUSHES = {push['step']: push['velocity_delta_world'] for push in SCENARIO['pushes']}
OriginalMake = gym.make


def make_scheduled_env(*args, **kwargs):
    # These imports require AppLauncher; gym.make is called after the official play launcher.
    from isaaclab.envs.mdp.commands.velocity_command import UniformVelocityCommand

    class ScheduledVelocityCommand(UniformVelocityCommand):
        def _resample_command(self, env_ids):
            self._update_command()

        def _update_command(self):
            self.vel_command_b[:] = self.vel_command_b.new_tensor(command_for_step(self._env.common_step_counter))

    cfg = kwargs['cfg']
    cfg.commands.base_velocity.class_type = ScheduledVelocityCommand
    cfg.commands.base_velocity.heading_command = False
    cfg.commands.base_velocity.ranges.heading = None
    cfg.commands.base_velocity.rel_heading_envs = 0.0
    cfg.commands.base_velocity.rel_standing_envs = 0.0
    cfg.scene.terrain.terrain_generator.seed = 42
    cfg.scene.terrain.max_init_terrain_level = 0
    cfg.curriculum.terrain_levels = None
    cfg.events.reset_base.params['pose_range'] = {'x': (0.0, 0.0), 'y': (0.0, 0.0), 'yaw': (0.0, 0.0)}
    cfg.events.add_base_mass.params['mass_distribution_params'] = (0.0, 0.0)
    cfg.observations.policy.enable_corruption = False
    cfg.events.push_robot = None
    environment = OriginalMake(*args, **kwargs)
    if abs(environment.unwrapped.step_dt - 0.02) > 1e-9:
        raise RuntimeError('Scenario requires 0.02-second control steps')
    print('[SCENARIO] ' + SCENARIO['name'] + ' / ' + SCENARIO['sha256'], flush=True)
    for phase in SCENARIO['phases']:
        print(f"[PHASE] {phase['start_step'] * 0.02:g}-{phase['end_step'] * 0.02:g}s: vx,vy,yaw={phase['velocity']}", flush=True)
    return environment


gym.make = make_scheduled_env
OriginalClip = clip_module.ImageSequenceClip


class ExactDurationClip(OriginalClip):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.fps is not None:
            self.duration = len(self.sequence) / float(self.fps)
            self.end = self.start + self.duration


clip_module.ImageSequenceClip = ExactDurationClip
OriginalRecordVideo = gym.wrappers.RecordVideo


class CountedRecordVideo(OriginalRecordVideo):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.control_steps = 0
        self.push_steps = []
        self.trace_path = WORK / (Path.cwd().name.removeprefix('run-') + '.commands.csv')
        self.trace = self.trace_path.open('x', encoding='ascii', newline='')
        self.trace_writer = csv.writer(self.trace, lineterminator='\n')
        self.trace_writer.writerow(TRACE_HEADER)
        self.capture_probes = []
        self.capture_no_append_steps = []
        self.capture_diagnostics_path = WORK / (self.trace_path.stem.removesuffix('.commands') + '.capture_diagnostics.json')

    @staticmethod
    def _frame_probe(frame):
        maximum = float(frame.max()) if frame.size else None
        return {'shape': list(frame.shape), 'dtype': str(frame.dtype),
                'max': maximum, 'all_zero': bool(maximum == 0 and frame.min() == 0)}

    def _capture_frame(self):
        before = len(self.recorded_frames)
        super()._capture_frame()
        try:
            if len(self.recorded_frames) == before:
                self.capture_no_append_steps.append(self.step_id)
                if not self.recorded_frames:
                    self.capture_diagnostics_path.write_text(json.dumps({
                        'schema_version': 1, 'stage': 'capture_no_append',
                        'capture_no_append_steps': self.capture_no_append_steps}), encoding='utf-8')
            for index in range(before, len(self.recorded_frames)):
                self.capture_probes.append({'index': index, 'step_id': self.step_id,
                                            **self._frame_probe(self.recorded_frames[index])})
        except Exception as exc:
            print(f'[CAPTURE DIAGNOSTIC WARNING] capture probe: {exc}', flush=True)

    def stop_recording(self):
        if self.recorded_frames:
            try:
                pre_encode = [dict(index=index, **self._frame_probe(frame))
                              for index, frame in enumerate(self.recorded_frames)]
                captured = {row['index']: row for row in self.capture_probes}
                capture_black = [row['index'] for row in self.capture_probes if row['all_zero']]
                pre_encode_black = [row['index'] for row in pre_encode if row['all_zero']]
                changed = [row['index'] for row in pre_encode if row['index'] in captured
                           and any(row[key] != captured[row['index']][key] for key in ('shape', 'dtype', 'max', 'all_zero'))]
                report = {'schema_version': 1, 'stage': 'before_encoding',
                          'black_definition': 'all pixel values exactly zero; empty frame has max=null',
                          'capture': self.capture_probes, 'pre_encode': pre_encode,
                          'capture_black_indices': capture_black,
                          'pre_encode_black_indices': pre_encode_black,
                          'capture_no_append_steps': self.capture_no_append_steps,
                          'changed_probe_indices': changed,
                          'note': 'No extra render, frame copy, pixel repair, or encoder-output audit. Equal probes do not prove equal bytes.'}
                self.capture_diagnostics_path.write_text(json.dumps(report), encoding='utf-8')
                warning = changed or self.capture_no_append_steps or any(index > 0 for index in capture_black + pre_encode_black)
                print(f"[CAPTURE DIAGNOSTIC {'WARNING' if warning else 'INFO'}] "
                      f'capture_black={len(capture_black)} pre_encode_black={len(pre_encode_black)} '
                      f'changed_probes={len(changed)} no_append={len(self.capture_no_append_steps)}; {self.capture_diagnostics_path}', flush=True)
            except Exception as exc:
                print(f'[CAPTURE DIAGNOSTIC WARNING] pre-encode probe: {exc}', flush=True)
        return super().stop_recording()

    def step(self, action):
        step = self.control_steps
        base = self.env.unwrapped
        if base.common_step_counter != step:
            raise RuntimeError('Scenario step counter mismatch')
        actual = base.command_manager.get_command('base_velocity')[0].detach().cpu().tolist()
        expected = command_for_step(step)
        if any(not math.isfinite(a) or abs(a - b) > 1e-6 for a, b in zip(actual, expected)):
            raise RuntimeError(f'Unexpected command at step {step}: {actual}, expected {expected}')
        delta = PUSHES.get(step, [0.0, 0.0, 0.0])
        if step in PUSHES:
            import torch
            from isaaclab.envs import mdp
            asset = base.scene['robot']
            before = asset.data.root_vel_w.clone()
            mdp.push_by_setting_velocity(
                base, torch.arange(base.num_envs, device=base.device),
                velocity_range={axis: (value, value) for axis, value in zip(('x', 'y', 'z'), delta)},
            )
            measured = (asset.data.root_vel_w - before)[0].detach().cpu().tolist()
            if any(not math.isfinite(a) or abs(a - b) > 1e-5 for a, b in zip(measured, delta + [0.0, 0.0, 0.0])):
                raise RuntimeError(f'Push was not applied at step {step}: delta={measured}')
            self.push_steps.append(step)
            print(f'[PUSH] {step * 0.02:g}s: world velocity delta={delta} m/s', flush=True)
        result = super().step(action)
        self.trace_writer.writerow(trace_row(step, actual, delta))
        self.control_steps += 1
        if self.control_steps % 100 == 0:
            self.trace.flush()
            print(f'[CONTROL STEP] {self.control_steps}/1000', flush=True)
        return result

    def close(self):
        captured_frames = len(self.recorded_frames)
        try:
            super().close()
        finally:
            self.trace.close()
        trace_hash = hashlib.sha256(self.trace_path.read_bytes()).hexdigest()
        Path('control_steps.json').write_text(json.dumps({
            'control_steps': self.control_steps, 'captured_frames': captured_frames,
            'scenario_sha256': SCENARIO['sha256'], 'command_trace_sha256': trace_hash,
            'push_steps': self.push_steps,
        }))
        if self.control_steps != 1000 or captured_frames != 1000 or self.push_steps != sorted(PUSHES):
            raise RuntimeError('Incomplete video, command trace, or push schedule')


gym.wrappers.RecordVideo = CountedRecordVideo
sys.argv = [PLAY] + sys.argv[1:]
runpy.run_path(PLAY, run_name='__main__')

'@
    [IO.File]::WriteAllText((Join-Path $Work 'runner.py'), $RunnerSource, [Text.Encoding]::ASCII)
    $EvaluationSource = @'
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import sys
import time
import uuid
import zipfile
from datetime import datetime


TERRAINS = ('01_stairs', '02_inverted_stairs', '03_boxes', '04_random_rough',
            '05_slope_up_20deg', '06_slope_down_20deg')


def digest(path):
    result = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(chunk)
    return result.hexdigest()


def verify_video_result(result_path, source, source_hash, scenario_hash):
    result = json.loads(Path(result_path).read_text(encoding='utf-8-sig'))
    if not result.get('video_success', result.get('success', False)):
        raise ValueError('Saved video suite was not successful')
    if result['source_checkpoint_sha256'] != source_hash or Path(result['source_checkpoint']).resolve() != source.resolve():
        raise ValueError('Saved videos belong to a different checkpoint')
    runs = result['runs']
    if [row['terrain'] for row in runs] != list(TERRAINS):
        raise ValueError('Saved video suite must contain the exact six terrains')
    for row in runs:
        if not row['verified'] or row['exit_code'] != 0 or row['control_steps'] != 1000 or row['frames'] != 1000:
            raise ValueError('Saved video suite has incomplete or failed videos')
        if row['scenario_sha256'] != scenario_hash:
            raise ValueError('Saved video schedule differs from the fixed schedule')
    archive_path = Path(result['zip_path'])
    if not archive_path.is_file() or archive_path.stat().st_size <= 0 or digest(archive_path) != result['zip_sha256']:
        raise ValueError('Saved video ZIP is missing or its SHA256 changed')
    expected = {name + '.mp4' for name in TERRAINS} | {
        'SHA256SUMS.txt', 'source_checkpoint.txt', 'environment.txt', 'README.txt'}
    with zipfile.ZipFile(archive_path) as archive:
        if len(archive.infolist()) != 10 or set(archive.namelist()) != expected or archive.testzip() is not None:
            raise ValueError('Saved video ZIP entries or CRC are invalid')
        provenance = dict(line.split('=', 1) for line in archive.read('source_checkpoint.txt').decode('utf-8-sig').splitlines() if '=' in line)
        if provenance.get('source_checkpoint_sha256') != source_hash or Path(provenance.get('source_checkpoint', '')).resolve() != source.resolve():
            raise ValueError('Saved video ZIP checkpoint provenance mismatch')
        for row in runs:
            if archive.getinfo(row['file']).file_size != row['size'] or row['size'] <= 0:
                raise ValueError('Saved MP4 size differs from its receipt')
            with archive.open(row['file']) as stream:
                hashed = hashlib.sha256()
                for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                    hashed.update(chunk)
            if hashed.hexdigest() != row['sha256']:
                raise ValueError('Saved MP4 SHA256 mismatch')
    return {key: result[key] for key in ('runs', 'environment', 'zip_path', 'zip_size', 'zip_sha256')}


def validate_evaluation(directory, source_hash, num_envs, seeds, started):
    from eval_core import load_jsonl, load_suite, validate_dataset

    directory = Path(directory)
    for name in ('episodes.jsonl', 'evaluation_manifest.json', 'resolved_configs.json'):
        path = directory / name
        if not path.is_file() or path.stat().st_size <= 0 or path.stat().st_mtime < started - 2:
            raise ValueError('Missing, empty or stale evaluation file: ' + name)
    manifest = json.loads((directory / 'evaluation_manifest.json').read_text(encoding='utf-8-sig'))
    if manifest.get('execution_status') != 'COMPLETE' or manifest.get('smoke') is not False or manifest.get('complete') is not True:
        raise ValueError('Evaluator did not finish the requested full evaluation: ' + str(manifest.get('error', manifest.get('execution_status'))))
    if manifest['robot'] != 'go2' or manifest['policy']['sha256'] != source_hash or manifest['policy']['kind'] != 'rsl_rl_checkpoint':
        raise ValueError('Evaluation checkpoint/robot/format mismatch')
    expected_suite = load_suite('go2', 'scenario7')
    expected_seeds = seeds
    protocol = manifest['protocol']
    if manifest['suite'] != expected_suite or protocol['num_envs'] != num_envs or protocol['seeds'] != expected_seeds:
        raise ValueError('Evaluation suite, environment count or seeds differ from the requested protocol')
    if protocol['camera_enabled'] is not False or protocol['render_mode'] is not None or protocol['actor_mode'] != 'deterministic_inference':
        raise ValueError('Evaluation must be camera-off deterministic inference')
    rows = load_jsonl(directory / 'episodes.jsonl')
    validate_dataset(rows, manifest)
    return manifest, rows


def evaluate_checkpoint(work, source, checkpoint, source_hash, video_result, config, run_child):
    from eval_core import write_json

    work, source, checkpoint = Path(work), Path(source), Path(checkpoint)
    num_envs = config.get('evaluation_num_envs', 128)
    seeds = [int(value) for value in config.get('evaluation_seeds', '4201,4202,4203').split(',')]
    if num_envs < 1 or not seeds or any(seed < 0 for seed in seeds) or len(set(seeds)) != len(seeds):
        raise ValueError('Invalid evaluator environment count or seed list')
    output = work / 'evaluation'
    arguments = [sys.executable, '-u', str(work / 'evaluator/isaac_runner.py'),
                 '--mode', 'personal', '--robot', 'go2', '--suite', 'scenario7',
                 '--task-root', 'C:/NCRC/naver-issacsim-nvidia/training/quadruped',
                 '--isaaclab-root', 'C:/NCRC/IsaacLab', '--checkpoint', str(checkpoint),
                 '--num-envs', str(num_envs), '--seeds', ','.join(map(str, seeds)),
                 '--device', 'cuda:0', '--output', str(output)]
    print('[VIDEO COMPLETE] ZIP preserved: ' + video_result['zip_path'], flush=True)
    print('[EVALUATION START] camera-off scenario7; full 9 cases / 20 seconds each', flush=True)
    started = time.time()
    code = run_child(arguments, work, work / 'evaluation.log')
    if code != 0:
        raise RuntimeError('Evaluator native child exit=' + str(code) + '; videos preserved; see evaluation.log')
    manifest, rows = validate_evaluation(output, source_hash, num_envs, seeds, started)
    if digest(source) != source_hash or digest(checkpoint) != source_hash:
        raise ValueError('Source or staged checkpoint SHA256 changed during evaluation')
    write_json(output / 'video_evaluation_link.json', {
        'source_checkpoint': str(source), 'source_checkpoint_sha256': source_hash,
        'staged_checkpoint_used': str(checkpoint), 'video_zip': video_result['zip_path'],
        'video_zip_sha256': video_result['zip_sha256'],
        'upstream_implementation_commit': '9c774a322f2f7d4944444de57f01308987bcb3da',
        'handoff_commit': '28895d75edf3095607e392a07207a62e768478c7',
        'collector_sha256': digest(work / 'evaluator/isaac_runner.py'),
        'scorer_sha256': digest(work / 'evaluator/eval_core.py'),
        'protocol_id': manifest['protocol_id'], 'smoke': False,
    })
    diagnostics = {}
    for scenario in manifest['suite']['scenarios']:
        selected = [row for row in rows if row['scenario'] == scenario['id']]
        diagnostics[scenario['id']] = {
            'name': scenario['name'], 'episodes': len(selected),
            'failed_episodes': sum(not row['survived'] for row in selected),
            'survival_rate': sum(row['survived'] for row in selected) / len(selected),
            'mean_episode_tracking_error': sum(row['mean_tracking_error'] for row in selected) / len(selected),
        }
    write_json(output / 'diagnostics.json', {'raw_diagnostics_only': True, 'official_score': False, 'scenarios': diagnostics})
    (output / 'README.txt').write_text(
        'PERSONAL camera-off evaluation, separate from the six videos.\n'
        'Not an official score or reproduction of unpublished official conditions.\n'
        'Full datasets can be compared with another completed dataset using compare_cli.py.\n'
        'Use one common calibration for both policies; B-provisional calibration changes with B.\n', encoding='ascii')
    shutil.copy2(work / 'evaluation.log', output / 'evaluation.log')
    hashes = {path.name: digest(path) for path in output.iterdir() if path.is_file()}
    prefix = source.stem + '_go2_evaluation_'
    destination = source.parent / (prefix + datetime.now().strftime('%Y%m%d-%H%M%S') + '_' + uuid.uuid4().hex[:8])
    partial = destination.with_name(destination.name + '.partial')
    shutil.copytree(output, partial)
    if {path.name: digest(path) for path in partial.iterdir() if path.is_file()} != hashes:
        raise ValueError('Published evaluation copy SHA256 mismatch; partial folder preserved: ' + str(partial))
    os.rename(partial, destination)
    summary = {
        'success': True, 'native_exit_code': code, 'path': str(destination),
        'protocol_id': manifest['protocol_id'], 'complete': manifest['complete'],
        'smoke': False, 'episodes': len(rows), 'num_envs': num_envs,
        'seeds': seeds, 'file_sha256': hashes,
    }
    print('[EVALUATION PASS] ' + str(destination), flush=True)
    return summary


def package_video_evaluation(source, source_hash, video_result, evaluation):
    source = Path(source)
    if (not evaluation.get('success') or evaluation.get('native_exit_code') != 0
            or evaluation.get('smoke') is not False or evaluation.get('complete') is not True):
        raise ValueError('Combined ZIP requires a successful full evaluation; smoke is not full')
    if digest(source) != source_hash:
        raise ValueError('Source checkpoint changed before combined packaging')
    directory = Path(evaluation['path'])
    expected_evaluation = {'episodes.jsonl', 'evaluation_manifest.json', 'resolved_configs.json',
                           'video_evaluation_link.json', 'diagnostics.json', 'evaluation.log', 'README.txt'}
    if set(evaluation['file_sha256']) != expected_evaluation:
        raise ValueError('Combined ZIP requires the exact seven evaluation files')
    for name, expected_hash in evaluation['file_sha256'].items():
        path = directory / name
        if not path.is_file() or path.stat().st_size <= 0 or digest(path) != expected_hash:
            raise ValueError('Evaluation file missing or changed: ' + name)
    manifest, _ = validate_evaluation(directory, source_hash, evaluation['num_envs'],
                                      evaluation['seeds'], 0)
    if manifest['protocol_id'] != evaluation['protocol_id']:
        raise ValueError('Evaluation receipt protocol mismatch')
    link = json.loads((directory / 'video_evaluation_link.json').read_text(encoding='utf-8-sig'))
    if (link['source_checkpoint_sha256'] != source_hash
            or link['video_zip_sha256'] != video_result['zip_sha256']
            or link['protocol_id'] != evaluation['protocol_id'] or link['smoke'] is not False):
        raise ValueError('Video/evaluation link mismatch')
    video_zip = Path(video_result['zip_path'])
    if digest(video_zip) != video_result['zip_sha256']:
        raise ValueError('Video ZIP changed before combined packaging')
    video_names = {name + '.mp4' for name in TERRAINS} | {
        'SHA256SUMS.txt', 'source_checkpoint.txt', 'environment.txt', 'README.txt'}
    expected_hashes = {}
    with zipfile.ZipFile(video_zip) as archive:
        if len(archive.infolist()) != 10 or set(archive.namelist()) != video_names or archive.testzip() is not None:
            raise ValueError('Invalid source video ZIP')
        for name in video_names:
            with archive.open(name) as stream:
                hashed = hashlib.sha256()
                for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                    hashed.update(chunk)
            expected_hashes[name] = hashed.hexdigest()
    for row in video_result['runs']:
        if expected_hashes[row['file']] != row['sha256']:
            raise ValueError('Video hash differs from receipt')
    name = source.stem + '_go2_6terrain_evaluation_' + datetime.now().strftime('%Y%m%d-%H%M%S') + '_' + uuid.uuid4().hex[:8] + '.zip'
    destination = source.parent / name
    partial = destination.with_name(destination.name + '.partial')
    with video_zip.open('rb') as src, partial.open('xb') as dest:
        shutil.copyfileobj(src, dest)
    readme = ('Six qualitative terrain videos and the same checkpoint full camera-off evaluation.\n'
              'Evaluation files and raw diagnostic summary are in evaluation/.\n'
              'Not an official score. No A/B comparison report or calibration is included.\n'
              'Original video ZIP and evaluation directory are preserved.\n'
              'source_checkpoint_sha256=' + source_hash + '\n'
              'video_zip_sha256=' + video_result['zip_sha256'] + '\n'
              'protocol_id=' + evaluation['protocol_id'] + '\n').encode('ascii')
    with zipfile.ZipFile(partial, 'a', compression=zipfile.ZIP_DEFLATED) as archive:
        for file_name in sorted(expected_evaluation):
            archive.write(directory / file_name, 'evaluation/' + file_name)
            expected_hashes['evaluation/' + file_name] = evaluation['file_sha256'][file_name]
        archive.writestr('BUNDLE_README.txt', readme)
        expected_hashes['BUNDLE_README.txt'] = hashlib.sha256(readme).hexdigest()
    with zipfile.ZipFile(partial) as archive:
        if (len(archive.infolist()) != 18 or set(archive.namelist()) != set(expected_hashes)
                or archive.testzip() is not None):
            raise ValueError('Combined ZIP entries or CRC verification failed: ' + str(partial))
        for file_name, expected_hash in expected_hashes.items():
            if archive.getinfo(file_name).file_size <= 0:
                raise ValueError('Combined ZIP contains an empty file: ' + file_name)
            with archive.open(file_name) as stream:
                hashed = hashlib.sha256()
                for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                    hashed.update(chunk)
            if hashed.hexdigest() != expected_hash:
                raise ValueError('Combined ZIP SHA256 mismatch: ' + file_name)
    if digest(source) != source_hash:
        raise ValueError('Source checkpoint changed during combined packaging')
    archive_hash = digest(partial)
    os.rename(partial, destination)
    print('[COMBINED ZIP] ' + str(destination), flush=True)
    print('[COMBINED ZIP SHA256] ' + archive_hash, flush=True)
    return {'path': str(destination), 'sha256': archive_hash,
            'size': destination.stat().st_size, 'entries': 18}


def compare_saved(candidate, reference, work, run_child):
    output = Path(candidate).parent / ('comparison-go2-' + datetime.now().strftime('%Y%m%d-%H%M%S') + '-' + uuid.uuid4().hex[:8])
    code = run_child([sys.executable, '-u', str(Path(work) / 'evaluator/compare_cli.py'),
                      '--robot', 'go2', '--a', str(candidate), '--b', str(reference),
                      '--output', str(output)], Path(work), Path(work) / 'comparison.log')
    if code != 0:
        raise RuntimeError('Saved-data CPU comparison failed; evaluation and videos preserved; see comparison.log')
    for name in ('calibration.json', 'comparison.json', 'comparison.html'):
        if not (output / name).is_file() or (output / name).stat().st_size <= 0:
            raise ValueError('Missing comparison output: ' + name)
    return str(output)

'@
    [IO.File]::WriteAllText((Join-Path $Work 'video_evaluation.py'), $EvaluationSource, [Text.Encoding]::ASCII)
    $EvaluatorWork = Join-Path $Work 'evaluator'
    New-Item -ItemType Directory -Path $EvaluatorWork | Out-Null
    foreach ($Name in @('isaac_runner.py','eval_core.py','compare_cli.py','bundle_manifest.json')) {
        Copy-Item -LiteralPath (Join-Path $BundleRoot $Name) -Destination $EvaluatorWork
    }
    $DriverSource = @'
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time
import traceback
import zipfile
from datetime import datetime
from importlib.metadata import version

WORK = Path(__file__).resolve().parent
CONFIG = json.loads((WORK / 'config.json').read_text(encoding='utf-8-sig'))
SOURCE = Path(CONFIG['checkpoint'])
LAB = Path('C:/NCRC/IsaacLab')
TASK_REPO = Path('C:/NCRC/naver-issacsim-nvidia')
TASK = TASK_REPO / 'training/quadruped'
PLAY = LAB / 'scripts/reinforcement_learning/rsl_rl/play.py'
TEMPLATES = json.loads((WORK / 'scenarios.json').read_text(encoding='utf-8'))
SCENARIO_NAME = CONFIG['scenario']
SCENARIO = dict(TEMPLATES[SCENARIO_NAME], name=SCENARIO_NAME, version=1, control_dt=0.02,
                terrain_seed=42, reset_pose_xy_yaw=[0.0, 0.0, 0.0],
                observation_noise=False, added_base_mass=0.0)
SCENARIO_HASH = hashlib.sha256(json.dumps(SCENARIO, sort_keys=True, separators=(',', ':')).encode('ascii')).hexdigest()
SCENARIO['sha256'] = SCENARIO_HASH
PROFILES = [
    ('01_stairs', 'pyramid_stairs'),
    ('02_inverted_stairs', 'pyramid_stairs_inv'),
    ('03_boxes', 'boxes'),
    ('04_random_rough', 'random_rough'),
    ('05_slope_up_20deg', 'hf_pyramid_slope'),
    ('06_slope_down_20deg', 'hf_pyramid_slope_inv'),
]
PREFIX = 'env.scene.terrain.terrain_generator'
RESULT = {'success': False, 'work': str(WORK), 'runs': []}
CHILD = None
SOURCE_HASH = None
SUCCESS = False


def sha256(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def git_head(repo):
    return subprocess.check_output(
        ['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True
    ).strip()


def run_child(arguments, directory, log_path):
    global CHILD
    print('[COMMAND] ' + subprocess.list2cmdline(arguments), flush=True)
    with open(log_path, 'w', encoding='utf-8') as logfile:
        logfile.write('[COMMAND] ' + subprocess.list2cmdline(arguments) + '\n')
        CHILD = subprocess.Popen(
            arguments, cwd=directory, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace',
            bufsize=1,
        )
        (WORK / 'active_child.json').write_text(
            json.dumps({'pid': CHILD.pid, 'command': arguments}), encoding='utf-8'
        )
        try:
            for line in CHILD.stdout:
                print(line, end='', flush=True)
                logfile.write(line)
                logfile.flush()
            code = CHILD.wait()
        finally:
            if CHILD.poll() is None:
                CHILD.terminate()
                try:
                    CHILD.wait(timeout=15)
                except subprocess.TimeoutExpired:
                    CHILD.kill()
                    CHILD.wait()
            CHILD.stdout.close()
            CHILD = None
            (WORK / 'active_child.json').unlink(missing_ok=True)
        print('[CHILD EXIT] ' + str(code), flush=True)
        logfile.write('[CHILD EXIT] ' + str(code) + '\n')
        return code


def main():
    global SOURCE_HASH
    import torch
    import tensordict
    import rsl_rl
    import imageio_ffmpeg

    environment = {
        'created_at': datetime.now().astimezone().isoformat(),
        'isaac_sim_version': Path('C:/isaacsim/VERSION').read_text().strip(),
        'isaaclab_git_head': git_head(LAB),
        'task_repo_git_head': git_head(TASK_REPO),
        'isaaclab_git_tracked_dirty': bool(subprocess.check_output(['git', '-C', str(LAB), 'status', '--porcelain', '--untracked-files=no']).strip()),
        'task_repo_git_tracked_dirty': bool(subprocess.check_output(['git', '-C', str(TASK_REPO), 'status', '--porcelain', '--untracked-files=no']).strip()),
        'suite_driver_sha256': sha256(__file__),
        'launcher_sha256': sha256('C:/NCRC/go2_6terrain_video.ps1'),
        'python': platform.python_version(),
        'torch': torch.__version__,
        'tensordict': version('tensordict'),
        'rsl_rl_lib': version('rsl-rl-lib'),
        'cuda_available': torch.cuda.is_available(),
        'torch_cuda': torch.version.cuda,
        'gpu': torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'NONE',
        'seed': 42, 'video_length': 1000, 'horizontal_scale': 0.05,
        'fixed_slope_value': 0.363970234, 'num_rows': 1, 'num_cols': 1,
        'task': 'Quadruped-v0', 'num_envs': 1,
        'headless': True, 'video': True, 'enable_cameras': True,
        'scenario_name': SCENARIO_NAME, 'scenario_sha256': SCENARIO_HASH,
        'scenario_version': 1, 'control_dt': 0.02, 'terrain_seed': 42,
        'reset_pose_xy_yaw': [0.0, 0.0, 0.0], 'observation_noise': False,
        'added_base_mass': 0.0, 'heading_command': False,
        'command_phases': SCENARIO['phases'], 'scheduled_pushes': SCENARIO['pushes'],
        'push_method': 'IsaacLab mdp.push_by_setting_velocity; additive world velocity impulse; not official G6 settings',
        'OMNI_CONFIG_PATH': os.environ['OMNI_CONFIG_PATH'],
        'ISAACLAB_PATH': os.environ['ISAACLAB_PATH'],
        'WARP_CACHE_PATH': os.environ['WARP_CACHE_PATH'],
    }
    RESULT['environment'] = environment
    for key, value in environment.items():
        print('[ENV] ' + key + '=' + str(value), flush=True)
    for key, expected in {
        'python': '3.11.13', 'torch': '2.7.0+cu128', 'tensordict': '0.9.0',
        'rsl_rl_lib': '5.0.1',
        'isaaclab_git_head': '3e73d6dd79080fd7632488c061052a6edd52e230',
    }.items():
        if environment[key] != expected:
            raise RuntimeError(f'Unexpected {key}: {environment[key]} (expected {expected})')
    if not environment['cuda_available']:
        raise RuntimeError('CUDA unavailable')
    print('[PREFLIGHT PASS] Python stack imports and CUDA', flush=True)

    SOURCE_HASH = sha256(SOURCE)
    RESULT['source_checkpoint'] = str(SOURCE)
    RESULT['source_checkpoint_sha256'] = SOURCE_HASH
    expected_hash = CONFIG.get('expected_sha256', '')
    if expected_hash and SOURCE_HASH != expected_hash.lower():
        raise RuntimeError('Source checkpoint SHA256 does not match expected hash')
    print('[SOURCE SHA256] ' + SOURCE_HASH, flush=True)
    staged_source = WORK / 'checkpoint.pt'
    shutil.copy2(SOURCE, staged_source)
    if sha256(staged_source) != SOURCE_HASH:
        raise RuntimeError('Checkpoint staging SHA256 mismatch')
    print('[STAGING PASS] ' + str(staged_source), flush=True)

    sys.path.insert(0, str(WORK / 'evaluator'))
    from video_evaluation import compare_saved, evaluate_checkpoint, verify_video_result, package_video_evaluation
    if CONFIG.get('video_result'):
        RESULT.update(verify_video_result(Path(CONFIG['video_result']), SOURCE, SOURCE_HASH, SCENARIO_HASH))
        RESULT['reused_video_result'] = CONFIG['video_result']
        RESULT['video_success'] = True
        print('[SAVED VIDEO PASS] Exact six videos and ZIP SHA256 verified', flush=True)
    else:
        create_video_suite(staged_source, environment, imageio_ffmpeg)
    RESULT['success'] = False
    (WORK / 'progress.json').write_text(json.dumps(RESULT, indent=2), encoding='utf-8')
    RESULT['evaluation'] = evaluate_checkpoint(WORK, SOURCE, staged_source, SOURCE_HASH, RESULT, CONFIG, run_child)
    RESULT['combined_archive'] = package_video_evaluation(SOURCE, SOURCE_HASH, RESULT, RESULT['evaluation'])
    if CONFIG.get('compare_with'):
        RESULT['comparison_path'] = compare_saved(RESULT['evaluation']['path'], CONFIG['compare_with'], WORK, run_child)
    RESULT['success'] = True


def create_video_suite(staged_source, environment, imageio_ffmpeg):

    (WORK / 'scenario.json').write_text(json.dumps(SCENARIO, indent=2), encoding='utf-8')
    runner = WORK / 'runner.py'
    if not runner.is_file():
        raise RuntimeError('Missing scenario runner')

    suite = WORK / 'suite'
    suite.mkdir()
    for index, (label, key) in enumerate(PROFILES, 1):
        run_directory = WORK / ('run-' + label)
        run_directory.mkdir()
        checkpoint = run_directory / 'model.pt'
        shutil.copy2(staged_source, checkpoint)
        if sha256(checkpoint) != SOURCE_HASH:
            raise RuntimeError(label + ': checkpoint staging SHA256 mismatch')
        overrides = [PREFIX + '.num_rows=1', PREFIX + '.num_cols=1',
                     PREFIX + '.horizontal_scale=0.05']
        for _, terrain in PROFILES:
            overrides.append(PREFIX + '.sub_terrains.' + terrain +
                             '.proportion=' + ('1.0' if terrain == key else '0.0'))
        if key in ('hf_pyramid_slope', 'hf_pyramid_slope_inv'):
            overrides.append(PREFIX + '.sub_terrains.' + key +
                             '.slope_range=[0.363970234,0.363970234]')
        args = [sys.executable, '-u', str(runner), '--task', 'Quadruped-v0',
                '--num_envs', '1', '--headless', '--video', '--video_length', '1000',
                '--enable_cameras', '--seed', '42', '--checkpoint', str(checkpoint)] + overrides
        print(f'\n========== [{index}/6] {label} ==========', flush=True)
        started = time.time()
        record = {'terrain': label, 'key': key, 'command': args, 'started_epoch': started}
        RESULT['runs'].append(record)
        code = run_child(args, run_directory, WORK / (label + '.log'))
        record['exit_code'] = code
        if code != 0:
            raise RuntimeError(f'{label}: native child exit code {code}; see {label}.log')
        receipt = run_directory / 'control_steps.json'
        if not receipt.is_file():
            raise RuntimeError(label + ': missing control step count')
        counts = json.loads(receipt.read_text())
        if counts['control_steps'] != 1000 or counts['captured_frames'] != 1000:
            raise RuntimeError(label + ': incomplete control step or captured frame count')
        trace_path = WORK / (label + '.commands.csv')
        if counts['scenario_sha256'] != SCENARIO_HASH or counts['command_trace_sha256'] != sha256(trace_path):
            raise RuntimeError(label + ': scenario or command trace SHA256 mismatch')
        expected_pushes = {push['step']: push['velocity_delta_world'] for push in SCENARIO['pushes']}
        if counts['push_steps'] != sorted(expected_pushes):
            raise RuntimeError(label + ': push schedule mismatch')
        with trace_path.open(encoding='ascii', newline='') as handle:
            rows = list(csv.DictReader(handle))
        if len(rows) != 1000:
            raise RuntimeError(label + ': command trace must contain 1000 steps')
        for step, row in enumerate(rows):
            phase = next(phase for phase in SCENARIO['phases'] if phase['start_step'] <= step < phase['end_step'])
            expected = phase['velocity'] + expected_pushes.get(step, [0.0, 0.0, 0.0])
            actual = [float(row[name]) for name in ('target_vx_body_mps', 'target_vy_body_mps', 'target_yaw_rate_radps',
                                                    'push_dvx_world_mps', 'push_dvy_world_mps', 'push_dvz_world_mps')]
            if int(row['step']) != step or abs(float(row['sim_seconds']) - step * 0.02) > 1e-6 or any(not math.isfinite(a) or abs(a - b) > 1e-6 for a, b in zip(actual, expected)):
                raise RuntimeError(f'{label}: command/push trace mismatch at step {step}')
        if index > 1 and counts['command_trace_sha256'] != RESULT['runs'][0]['command_trace_sha256']:
            raise RuntimeError(label + ': command trace differs from first terrain')
        videos = list((run_directory / 'videos/play').glob('*.mp4'))
        if len(videos) != 1:
            raise RuntimeError(f'{label}: expected one new MP4, found {len(videos)}')
        video = videos[0]
        stat = video.stat()
        if stat.st_size <= 0 or stat.st_mtime < started - 2 or stat.st_ctime < started - 2:
            raise RuntimeError(label + ': empty or stale MP4')
        frames, seconds = imageio_ffmpeg.count_frames_and_secs(str(video))
        if frames != 1000 or seconds <= 0:
            raise RuntimeError(f'{label}: invalid video frames={frames}, seconds={seconds}')
        destination = suite / (label + '.mp4')
        shutil.copy2(video, destination)
        video_hash = sha256(destination)
        if video_hash != sha256(video):
            raise RuntimeError(label + ': copied video SHA256 mismatch')
        record.update(file=destination.name, sha256=video_hash, size=stat.st_size,
                      frames=frames, control_steps=counts['control_steps'],
                      captured_frames=counts['captured_frames'], duration_seconds=seconds, verified=True,
                      scenario_sha256=SCENARIO_HASH, command_trace_sha256=counts['command_trace_sha256'],
                      push_steps=counts['push_steps'])
        print(f"[SCENARIO PASS] {SCENARIO_NAME}: 1000 commands verified; pushes={counts['push_steps']}; trace SHA256={counts['command_trace_sha256']}", flush=True)
        print(f'[PASS] {destination.name}: exit=0, {frames} frames, {seconds}s, {stat.st_size} bytes', flush=True)
        (WORK / 'progress.json').write_text(json.dumps(RESULT, indent=2), encoding='utf-8')

    (suite / 'SHA256SUMS.txt').write_text(''.join(
        row['sha256'] + '  ' + row['file'] + '\n' for row in RESULT['runs']), encoding='ascii')
    (suite / 'source_checkpoint.txt').write_text(
        'source_checkpoint=' + str(SOURCE) + '\nsource_checkpoint_sha256=' + SOURCE_HASH + '\n',
        encoding='utf-8-sig')
    environment['completed_at'] = datetime.now().astimezone().isoformat()
    environment['command_trace_sha256'] = RESULT['runs'][0]['command_trace_sha256']
    (suite / 'environment.txt').write_text(
        '\n'.join(str(k) + '=' + str(v) for k, v in environment.items()) + '\n' +
        '\n'.join(row['terrain'] + '_frames=' + str(row['frames']) for row in RESULT['runs']) + '\n',
        encoding='utf-8-sig')
    (suite / 'README.txt').write_text(
        'Go2 Windows Native 6-Terrain Video Suite\n\n'
        'These videos are qualitative behavior evidence, not fixed evaluator results or official scores.\n'
        'Each run uses Quadruped-v0, num_envs=1, seed=42, headless, video, enable_cameras.\n'
        '1000 control steps and 1000 decoded frames per video.\n'
        'Scenario: ' + SCENARIO_NAME + '; SHA256=' + SCENARIO_HASH + '\n'
        'Compare checkpoints only with the same scenario hash, command trace hash, environment and terrain settings.\n'
        'All templates begin with forward walking. Schedules use global video steps, not episode timers.\n'
        'Commands are body-frame vx/vy (m/s) and yaw rate (rad/s); heading feedback is disabled.\n'
        'Push variants add world-Y velocity impulses of +/-0.5 m/s at 4,8,12,16 simulated seconds.\n'
        'These pushes are local qualitative tests, not a reproduction of unpublished official G6 conditions.\n'
        'Initial/reset x,y,yaw=0; observation noise off; added base mass=0; terrain seed=42.\n'
        'Terrain generator: num_rows=1, num_cols=1, horizontal_scale=0.05.\n'
        'Selected terrain proportion=1.0; all five other proportions=0.0.\n'
        'Slope runs: slope_range=[0.363970234,0.363970234] (20 degrees).\n\n' +
        '\n'.join(label + '.mp4 -> ' + key for label, key in PROFILES) + '\n', encoding='utf-8-sig')

    archive_path = Path('C:/NCRC/go2-video-suite-logs') / WORK.name / 'video_source.zip'
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    staged_archive = WORK / 'verified_suite.zip'
    with zipfile.ZipFile(staged_archive, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for file in sorted(suite.iterdir()):
            archive.write(file, arcname=file.name)
    expected_names = {label + '.mp4' for label, _ in PROFILES} | {
        'SHA256SUMS.txt', 'source_checkpoint.txt', 'environment.txt', 'README.txt'}
    with zipfile.ZipFile(staged_archive) as archive:
        if len(archive.infolist()) != 10 or set(archive.namelist()) != expected_names:
            raise RuntimeError('ZIP names/count verification failed')
        if archive.testzip() is not None:
            raise RuntimeError('ZIP CRC verification failed')
        for row in RESULT['runs']:
            with archive.open(row['file']) as handle:
                digest = hashlib.sha256()
                for chunk in iter(lambda: handle.read(1024 * 1024), b''):
                    digest.update(chunk)
            if digest.hexdigest() != row['sha256']:
                raise RuntimeError('ZIP MP4 SHA256 verification failed: ' + row['file'])
    if staged_archive.stat().st_size <= 0:
        raise RuntimeError('ZIP size is zero')
    if sha256(SOURCE) != SOURCE_HASH:
        raise RuntimeError('Original checkpoint SHA256 changed')
    partial_archive = archive_path.with_name(archive_path.name + '.partial-' + WORK.name)
    RESULT['partial_archive'] = str(partial_archive)
    with open(staged_archive, 'rb') as src, open(partial_archive, 'xb') as dest:
        shutil.copyfileobj(src, dest)
        dest.flush()
        os.fsync(dest.fileno())
    if sha256(partial_archive) != sha256(staged_archive):
        raise RuntimeError('Final ZIP copy SHA256 mismatch')
    # Windows rename fails if destination exists, preserving existing archives.
    os.rename(partial_archive, archive_path)
    RESULT.pop('partial_archive', None)
    with zipfile.ZipFile(archive_path) as archive:
        if len(archive.infolist()) != 10 or set(archive.namelist()) != expected_names or archive.testzip() is not None:
            raise RuntimeError('Published ZIP verification failed')
    RESULT.update(video_success=True, zip_path=str(archive_path), zip_size=archive_path.stat().st_size,
                  zip_sha256=sha256(archive_path), source_checkpoint_unchanged=True)
    print('[INTERNAL VIDEO ZIP] ' + str(archive_path), flush=True)
    print('[ZIP SHA256] ' + RESULT['zip_sha256'], flush=True)
    print('[VERIFY] Original checkpoint unchanged: ' + SOURCE_HASH, flush=True)


try:
    main()
    SUCCESS = True
except BaseException as exc:
    RESULT['error'] = str(exc) or type(exc).__name__
    traceback.print_exc()
    print('[FAIL] Diagnostics preserved at: ' + str(WORK), flush=True)
finally:
    if SOURCE_HASH is not None:
        try:
            RESULT['source_checkpoint_unchanged'] = sha256(SOURCE) == SOURCE_HASH
            if not RESULT['source_checkpoint_unchanged']:
                SUCCESS = False
                RESULT.update(success=False, error='Original checkpoint SHA256 changed')
        except OSError as exc:
            SUCCESS = False
            RESULT.update(success=False, error='Final source integrity check failed: ' + str(exc))
    (WORK / 'result.json').write_text(json.dumps(RESULT, ensure_ascii=True, indent=2), encoding='utf-8')
sys.exit(0 if SUCCESS else 1)

'@
    $Driver = Join-Path $Work 'suite_driver.py'
    [IO.File]::WriteAllText($Driver, $DriverSource, [Text.Encoding]::ASCII)
    Write-Host ('[WORK] ' + $Work)
    Write-Host 'Live Isaac / Kit output and per-terrain log files are enabled.'
    Push-Location $Work
    try {
        & 'C:\isaacsim\python.bat' '-u' $Driver
        $Code = $LASTEXITCODE
    } finally { Pop-Location }
    $Receipt = Join-Path $Work 'result.json'
    if ($Code -ne 0) { throw ('Video suite failed: launcher exit=' + $Code) }
    if (-not (Test-Path -LiteralPath $Receipt)) { throw 'Missing suite completion receipt.' }
    $Result = Get-Content -LiteralPath $Receipt -Raw -Encoding UTF8 | ConvertFrom-Json
    if (-not $Result.success) { throw ('Video suite failed: ' + $Result.error) }
    $Success = $true
    $LogDir = Join-Path 'C:\NCRC\go2-video-suite-logs' ([IO.Path]::GetFileName($Work))
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
    Get-ChildItem -LiteralPath $Work -File | Where-Object { $_.Extension -in @('.log','.csv') -or $_.Name.EndsWith('.capture_diagnostics.json') -or $_.Name -in @('result.json','scenario.json') } | Copy-Item -Destination $LogDir
    Write-Host '[COMPLETE] 6/6 videos and separate full Go2 evaluation verified.' -ForegroundColor Green
    if ($Result.combined_archive) {
        Write-Host ('ZIP (videos + evaluation): ' + $Result.combined_archive.path)
        Write-Host ('ZIP SHA256: ' + $Result.combined_archive.sha256)
    } else {
        Write-Host ('ZIP: ' + $Result.zip_path)
        Write-Host ('ZIP SHA256: ' + $Result.zip_sha256)
    }
    Write-Host ('Evaluation data: ' + $Result.evaluation.path)
    if ($Result.comparison_path) { Write-Host ('CPU comparison: ' + $Result.comparison_path) }
    Write-Host ('Diagnostics: ' + $LogDir)
} catch {
    $Success = $false
    Write-Host ('[FAIL] ' + $_.Exception.Message) -ForegroundColor Red
    if ($Work) { Write-Host ('Diagnostics preserved: ' + $Work) }
} finally {
    if ($Success -and $Work) {
        $ResolvedBase = [IO.Path]::GetFullPath('C:\NCRC\go2-video-suite-work\')
        $ResolvedWork = [IO.Path]::GetFullPath($Work)
        if ($ResolvedWork.StartsWith($ResolvedBase, [StringComparison]::OrdinalIgnoreCase) -and [IO.Path]::GetFileName($ResolvedWork) -match '^suite-[0-9a-f]{32}$') {
            try { Remove-Item -LiteralPath $ResolvedWork -Recurse -Force } catch { Write-Host ('[CLEANUP] Work retained: ' + $Work) }
        }
    }
    $Mutex.ReleaseMutex()
    $Mutex.Dispose()
}
if ($Success) { exit 0 } else { exit 1 }
