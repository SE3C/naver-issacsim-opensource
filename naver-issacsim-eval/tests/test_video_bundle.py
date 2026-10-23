import json
from pathlib import Path
import re
import tempfile
from types import ModuleType
import unittest
import zipfile

from test_eval import _fixture
from eval_core import protocol_hash


script = (Path(__file__).resolve().parents[1] / 'go2_6terrain_video.ps1').read_text(encoding='utf-8-sig')
helper = ModuleType('video_evaluation_bundle_test')
exec(re.search(r"\$EvaluationSource = @'\r?\n(.*?)\r?\n'@", script, re.S).group(1), helper.__dict__)


class VideoBundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'source.pt'
        self.source.write_bytes(b'synthetic checkpoint, no inference')
        self.source_hash = helper.digest(self.source)
        self.video_zip = self.root / 'videos.zip'
        runs = []
        with zipfile.ZipFile(self.video_zip, 'w') as archive:
            for terrain in helper.TERRAINS:
                name = terrain + '.mp4'
                content = ('synthetic video ' + terrain).encode('ascii')
                archive.writestr(name, content)
                runs.append({'file': name, 'sha256': helper.hashlib.sha256(content).hexdigest()})
            for name in ('SHA256SUMS.txt', 'source_checkpoint.txt', 'environment.txt', 'README.txt'):
                archive.writestr(name, b'synthetic metadata')
        self.video = {'zip_path': str(self.video_zip), 'zip_sha256': helper.digest(self.video_zip), 'runs': runs}
        self.directory = self.root / 'evaluation'
        self.directory.mkdir()
        _, manifest, rows = _fixture(policy_sha=self.source_hash)
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
        second = self.package()
        self.assertNotEqual(second['path'], result['path'])
        self.assertTrue(Path(result['path']).is_file())

    def test_smoke_and_incomplete_evaluation_cannot_be_packaged_as_full(self):
        for field, value in (('smoke', True), ('complete', False), ('native_exit_code', 1)):
            with self.subTest(field=field):
                old = self.evaluation[field]
                self.evaluation[field] = value
                with self.assertRaisesRegex(ValueError, 'successful full'):
                    self.package()
                self.evaluation[field] = old
        self.assertEqual(list(self.root.glob('*6terrain_evaluation*')), [])

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
