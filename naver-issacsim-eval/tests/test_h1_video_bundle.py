import ast
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile
from types import ModuleType, SimpleNamespace
import unittest
from unittest import mock
import zipfile

from test_eval import _fixture
from eval_core import protocol_hash


script_path = Path(__file__).resolve().parents[1] / 'h1_6terrain_video.ps1'
script = script_path.read_text(encoding='utf-8-sig')
helper = ModuleType('h1_video_evaluation_bundle_test')
match = re.search(r"\$EvaluationSource = @'\r?\n(.*?)\r?\n'@", script, re.S)
if match is None:
    raise RuntimeError('h1_6terrain_video.ps1 has no embedded EvaluationSource')
exec(match.group(1), helper.__dict__)


class H1VideoBundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'source.pt'
        self.source.write_bytes(b'synthetic H1 checkpoint, no inference')
        self.source_hash = helper.digest(self.source)
        self.video_zip = self.root / 'videos.zip'
        runs = []
        with zipfile.ZipFile(self.video_zip, 'w') as archive:
            for terrain in helper.TERRAINS:
                name = terrain + '.mp4'
                content = ('synthetic H1 video ' + terrain).encode('ascii')
                archive.writestr(name, content)
                runs.append({'file': name, 'sha256': helper.hashlib.sha256(content).hexdigest()})
            for name in ('SHA256SUMS.txt', 'source_checkpoint.txt', 'environment.txt', 'README.txt'):
                archive.writestr(name, b'synthetic metadata')
        self.video = {'zip_path': str(self.video_zip), 'zip_sha256': helper.digest(self.video_zip), 'runs': runs}
        self.directory = self.root / 'evaluation'
        self.directory.mkdir()
        _, manifest, rows = _fixture(robot='h1', policy_sha=self.source_hash)
        manifest.update(execution_status='COMPLETE', smoke=False)
        manifest['policy']['kind'] = 'rsl_rl_checkpoint'
        manifest['protocol'].update(camera_enabled=False, render_mode=None, actor_mode='deterministic_inference')
        manifest['protocol_id'] = protocol_hash(manifest['protocol'])
        for row in rows:
            row['protocol_id'] = manifest['protocol_id']
        (self.directory / 'evaluation_manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
        (self.directory / 'episodes.jsonl').write_text(''.join(json.dumps(row) + '\n' for row in rows), encoding='utf-8')
        (self.directory / 'video_evaluation_link.json').write_text(json.dumps({
            'source_checkpoint_sha256': self.source_hash, 'video_zip_sha256': self.video['zip_sha256'],
            'protocol_id': manifest['protocol_id'], 'smoke': False}), encoding='utf-8')
        for name in ('resolved_configs.json', 'diagnostics.json', 'evaluation.log', 'README.txt'):
            (self.directory / name).write_text('{}', encoding='utf-8')
        self.evaluation = {'success': True, 'native_exit_code': 0, 'smoke': False, 'complete': True,
                           'path': str(self.directory), 'num_envs': 2, 'seeds': [42],
                           'protocol_id': manifest['protocol_id'],
                           'file_sha256': {path.name: helper.digest(path) for path in self.directory.iterdir()}}

    def package(self):
        return helper.package_video_evaluation(self.source, self.source_hash, self.video, self.evaluation)

    def test_h1_launcher_contract(self):
        self.assertIn('Humanoid-v0', script)
        self.assertIn('training/humanoid', script)
        self.assertIn('h1_task', script)
        self.assertIn('slope_up_10deg', script)
        self.assertIn('slope_down_10deg', script)
        self.assertIn('0.176326981', script)
        self.assertIn("load_suite('h1', 'scenario7')", script)
        self.assertIn('full 8 cases / 20 seconds each', script)
        self.assertNotIn('Quadruped-v0', script)
        self.assertNotIn('training/quadruped', script)

    def test_windows_entry_points_are_full_only(self):
        repo = script_path.parent
        for robot in ('h1', 'go2'):
            text = (repo / (robot + '_6terrain_video.ps1')).read_text(encoding='utf-8-sig')
            self.assertNotIn('EvaluationSmoke', text)
            self.assertNotIn('evaluation_smoke', text)
            self.assertNotIn("arguments.append('--smoke')", text)
            self.assertNotIn("'smoke': smoke", text)
            self.assertFalse((repo / (robot + '_eval_smoke.bat')).exists())
            self.assertFalse((repo / (robot + '_eval_smoke.ps1')).exists())
        installer = (repo / 'install_windows.ps1').read_text(encoding='utf-8-sig')
        self.assertNotIn('eval_smoke', installer)
        self.assertIn("SourceName = 'h1_6terrain_video.bat'", installer)
        self.assertIn('h1-video-evaluator', installer)

    def test_video_runner_accepts_disabled_mass_event(self):
        source = re.search(r"\$RunnerSource = @'\r?\n(.*?)\r?\n'@", script, re.S).group(1)
        function = next(node for node in ast.parse(source).body
                        if isinstance(node, ast.FunctionDef) and node.name == 'make_scheduled_env')
        module = ModuleType('isaaclab.envs.mdp.commands.velocity_command')
        module.UniformVelocityCommand = object
        environment = SimpleNamespace(unwrapped=SimpleNamespace(step_dt=0.02))
        namespace = {'OriginalMake': mock.Mock(return_value=environment),
                     'SCENARIO': {'name': 'test', 'sha256': 'test', 'phases': []}}
        exec(compile(ast.Module(body=[function], type_ignores=[]), '<H1 runner>', 'exec'), namespace)
        for event in (None, SimpleNamespace(params={'mass_distribution_params': (-1.0, 1.0)})):
            with self.subTest(event_enabled=event is not None):
                cfg = SimpleNamespace(
                    commands=SimpleNamespace(base_velocity=SimpleNamespace(ranges=SimpleNamespace())),
                    scene=SimpleNamespace(terrain=SimpleNamespace(terrain_generator=SimpleNamespace())),
                    curriculum=SimpleNamespace(),
                    events=SimpleNamespace(reset_base=SimpleNamespace(params={}), add_base_mass=event),
                    observations=SimpleNamespace(policy=SimpleNamespace()))
                with mock.patch.dict('sys.modules', {module.__name__: module}), mock.patch('builtins.print'):
                    self.assertIs(namespace['make_scheduled_env']('Humanoid-v0', cfg=cfg), environment)
                self.assertIs(cfg.events.add_base_mass, event)
                if event is not None:
                    self.assertEqual(event.params['mass_distribution_params'], (0.0, 0.0))

    def test_full_validator_checks_all_h1_cases(self):
        manifest, rows = helper.validate_evaluation(self.directory, self.source_hash, 2, [42], 0)
        self.assertTrue(manifest['complete'])
        self.assertEqual(len({(row['scenario'], row['case']) for row in rows}), 8)

    def test_video_zip_stays_internal_for_both_robots(self):
        for robot in ('h1', 'go2'):
            text = (script_path.parent / (robot + '_6terrain_video.ps1')).read_text(encoding='utf-8-sig')
            driver = re.search(r"\$DriverSource = @'\r?\n(.*?)\r?\n'@", text, re.S).group(1)
            function = next(node for node in ast.parse(driver).body
                            if isinstance(node, ast.FunctionDef) and node.name == 'create_video_suite')
            assignment = next(node for node in function.body
                              if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)
                              and node.targets[0].id == 'archive_path')
            namespace = {'Path': Path, 'WORK': self.root / 'suite-test', 'SOURCE': self.source}
            exec(compile(ast.Module(body=[assignment], type_ignores=[]), '<video ZIP path>', 'exec'), namespace)
            self.assertEqual(namespace['archive_path'],
                             Path('C:/NCRC/' + robot + '-video-suite-logs/suite-test/video_source.zip'))
            self.assertNotEqual(namespace['archive_path'].parent, self.source.parent)

    def test_evaluation_finalization_returns_full_summary(self):
        work = self.root / 'work'
        (work / 'evaluator').mkdir(parents=True)
        for name in ('isaac_runner.py', 'eval_core.py'):
            (work / 'evaluator' / name).write_text('synthetic source')

        def completed_child(arguments, cwd, log):
            self.assertNotIn('--smoke', arguments)
            shutil.copytree(self.directory, work / 'evaluation')
            shutil.copy2(self.directory / 'evaluation.log', log)
            return 0

        result = helper.evaluate_checkpoint(work, self.source, self.source, self.source_hash,
                                            self.video, {'evaluation_num_envs': 2,
                                                         'evaluation_seeds': '42'}, completed_child)
        self.assertTrue(result['success'])
        self.assertTrue(result['complete'])
        self.assertIs(result['smoke'], False)
        self.assertEqual(result['native_exit_code'], 0)
        self.assertEqual(len(result['file_sha256']), 7)
        self.assertTrue((work / 'evaluation' / 'episodes.jsonl').exists())

    def test_full_validator_refuses_smoke_data(self):
        path = self.directory / 'evaluation_manifest.json'
        manifest = json.loads(path.read_text())
        manifest.update(smoke=True, complete=False)
        path.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, 'full evaluation'):
            helper.validate_evaluation(self.directory, self.source_hash, 2, [42], 0)

    def test_evaluation_only_preserves_full_data_without_video_receipt(self):
        work = self.root / 'work'
        (work / 'evaluator').mkdir(parents=True)
        for name in ('isaac_runner.py', 'eval_core.py'):
            (work / 'evaluator' / name).write_text('synthetic source')

        def completed_child(arguments, cwd, log):
            self.assertNotIn('--enable_cameras', arguments)
            self.assertNotIn('--smoke', arguments)
            shutil.copytree(self.directory, work / 'evaluation')
            shutil.copy2(self.directory / 'evaluation.log', log)
            return 0

        result = helper.evaluate_checkpoint(work, self.source, self.source, self.source_hash,
                                            None, {'evaluation_num_envs': 2,
                                                   'evaluation_seeds': '42'}, completed_child)
        self.assertTrue(result['complete'])
        self.assertEqual(len(result['file_sha256']), 7)
        link = json.loads((Path(result['path']) / 'video_evaluation_link.json').read_text())
        self.assertIsNone(link['video_zip'])
        self.assertIsNone(link['video_zip_sha256'])
        self.assertEqual(link['source_checkpoint_sha256'], self.source_hash)
        self.assertEqual(list(self.root.glob('*.zip')), [self.video_zip])
        with self.assertRaisesRegex(RuntimeError, 'native child exit=7'):
            helper.evaluate_checkpoint(work, self.source, self.source, self.source_hash,
                                       None, {'evaluation_num_envs': 2, 'evaluation_seeds': '42'},
                                       lambda *args: 7)

    def test_evaluation_only_driver_never_calls_video_paths(self):
        driver = re.search(r"\$DriverSource = @'\r?\n(.*?)\r?\n'@", script, re.S).group(1)
        main = next(node for node in ast.parse(driver).body
                    if isinstance(node, ast.FunctionDef) and node.name == 'main')
        evaluation = ModuleType('video_evaluation')
        evaluation.evaluate_checkpoint = mock.Mock(return_value={'path': 'saved-evaluation'})
        for name in ('compare_saved', 'verify_video_result', 'package_video_evaluation'):
            setattr(evaluation, name, mock.Mock(side_effect=AssertionError('Unexpected video/comparison path')))
        torch = SimpleNamespace(__version__='2.7.0+cu128', version=SimpleNamespace(cuda='12.8'),
                                cuda=SimpleNamespace(is_available=lambda: True, get_device_name=lambda _: 'fixture'))
        work = self.root / 'work'
        work.mkdir()
        namespace = dict(helper.__dict__, WORK=work, SOURCE=self.source, RESULT={},
                         CONFIG={'evaluation_only': True, 'evaluation_num_envs': 128,
                                 'evaluation_seeds': '4201,4202,4203'},
                         LAB=self.root, TASK_REPO=self.root, __file__=str(self.source),
                         SCENARIO_NAME='maneuver_push', SCENARIO_HASH='unused',
                         SCENARIO={'phases': [], 'pushes': []},
                         sha256=mock.Mock(return_value=self.source_hash),
                         git_head=lambda _: '3e73d6dd79080fd7632488c061052a6edd52e230',
                         version=lambda name: {'tensordict': '0.9.0', 'rsl-rl-lib': '5.0.1'}[name],
                         subprocess=SimpleNamespace(check_output=lambda _: b''),
                         platform=SimpleNamespace(python_version=lambda: '3.11.13'),
                         run_child=mock.Mock(), create_video_suite=mock.Mock(side_effect=AssertionError('Rendered video')))
        exec(compile(ast.Module(body=[main], type_ignores=[]), '<H1 driver>', 'exec'), namespace)
        with mock.patch.dict(sys.modules, {'torch': torch, 'tensordict': ModuleType('tensordict'),
                                         'rsl_rl': ModuleType('rsl_rl'), 'video_evaluation': evaluation,
                                         'imageio_ffmpeg': None}), \
             mock.patch.dict('os.environ', {'OMNI_CONFIG_PATH': 'fixture', 'ISAACLAB_PATH': 'fixture',
                                          'WARP_CACHE_PATH': 'fixture'}), \
             mock.patch.object(Path, 'read_text', return_value='fixture'), \
             mock.patch.object(sys, 'path', list(sys.path)):
            namespace['main']()
        self.assertTrue(namespace['RESULT']['success'])
        self.assertFalse(namespace['RESULT']['environment']['enable_cameras'])
        self.assertIsNone(evaluation.evaluate_checkpoint.call_args.args[4])
        self.assertFalse(namespace['create_video_suite'].called)
        self.assertFalse(evaluation.package_video_evaluation.called)

    def test_combined_archive_has_six_videos_full_data_and_preserves_originals(self):
        result = self.package()
        with zipfile.ZipFile(result['path']) as archive:
            self.assertEqual(len(archive.infolist()), 18)
            self.assertEqual(sum(name.endswith('.mp4') for name in archive.namelist()), 6)
            self.assertIn('evaluation/diagnostics.json', archive.namelist())
            self.assertIsNone(archive.testzip())
        self.assertEqual(helper.digest(result['path']), result['sha256'])
        self.assertEqual(helper.digest(self.video_zip), self.video['zip_sha256'])
        self.assertEqual(helper.digest(self.source), self.source_hash)
        self.assertEqual(len(list(self.directory.iterdir())), 7)

    def test_smoke_and_incomplete_evaluation_cannot_be_packaged_as_full(self):
        for field, value in (('smoke', True), ('complete', False), ('native_exit_code', 1)):
            with self.subTest(field=field):
                old = self.evaluation[field]
                self.evaluation[field] = value
                with self.assertRaisesRegex(ValueError, 'successful full'):
                    self.package()
                self.evaluation[field] = old

    def test_changed_evaluation_or_video_is_rejected(self):
        diagnostics = self.directory / 'diagnostics.json'
        diagnostics.write_text('changed')
        with self.assertRaisesRegex(ValueError, 'missing or changed'):
            self.package()
        diagnostics.write_text('{}')
        self.video_zip.write_bytes(b'corrupted archive')
        with self.assertRaisesRegex(ValueError, 'Video ZIP changed'):
            self.package()

    def test_wrong_checkpoint_link_is_rejected(self):
        link = self.directory / 'video_evaluation_link.json'
        data = json.loads(link.read_text())
        data['source_checkpoint_sha256'] = '0' * 64
        link.write_text(json.dumps(data))
        self.evaluation['file_sha256'][link.name] = helper.digest(link)
        with self.assertRaisesRegex(ValueError, 'link mismatch'):
            self.package()


if __name__ == '__main__':
    unittest.main()
