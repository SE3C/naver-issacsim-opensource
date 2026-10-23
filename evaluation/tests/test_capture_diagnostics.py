import ast
import csv
import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest import mock


class Frame:
    shape = (2, 2, 3)
    dtype = 'uint8'
    size = 12

    def __init__(self, value):
        self.value = value

    def max(self):
        return self.value

    def min(self):
        return self.value


class Recorder:
    def __init__(self):
        self.recorded_frames = []
        self.step_id = -1
        self.next_frame = None
        self.encode_error = False
        self.encode_calls = 0

    def _capture_frame(self):
        if self.next_frame is not None:
            self.recorded_frames.append(self.next_frame)

    def stop_recording(self):
        self.encode_calls += 1
        if self.encode_error:
            raise RuntimeError('synthetic encoder error')
        self.recorded_frames.clear()
        return 'encoded'


class CaptureDiagnosticsTests(unittest.TestCase):
    def recorders(self):
        repo = Path(__file__).resolve().parents[1]
        for robot in ('h1', 'go2'):
            with self.subTest(robot=robot), tempfile.TemporaryDirectory() as directory:
                work = Path(directory)
                text = (repo / (robot + '_6terrain_video.ps1')).read_text(encoding='utf-8-sig')
                source = re.search(r"\$RunnerSource = @'\r?\n(.*?)\r?\n'@", text, re.S).group(1)
                node = next(node for node in ast.parse(source).body
                            if isinstance(node, ast.ClassDef) and node.name == 'CountedRecordVideo')
                namespace = {'OriginalRecordVideo': Recorder, 'WORK': work, 'Path': Path,
                             'csv': csv, 'json': json, 'TRACE_HEADER': ['step']}
                exec(compile(ast.Module(body=[node], type_ignores=[]), '<video runner>', 'exec'), namespace)
                with mock.patch.object(Path, 'cwd', return_value=work / 'run-01_stairs'):
                    recorder = namespace['CountedRecordVideo']()
                try:
                    yield recorder, text
                finally:
                    recorder.trace.close()

    def capture(self, recorder, values):
        for index, value in enumerate(values):
            recorder.step_id = index
            recorder.next_frame = Frame(value) if value is not None else None
            recorder._capture_frame()

    def test_alternating_black_is_recorded_without_changing_frames_or_result(self):
        for recorder, text in self.recorders():
            self.capture(recorder, [0, 255, 0, 255])
            frames = list(recorder.recorded_frames)
            self.assertEqual([row['max'] for row in recorder.capture_probes], [0, 255, 0, 255])
            self.assertEqual(recorder.recorded_frames, frames)
            with mock.patch('builtins.print') as output:
                self.assertEqual(recorder.stop_recording(), 'encoded')
            report = json.loads(recorder.capture_diagnostics_path.read_text())
            self.assertEqual(report['capture_black_indices'], [0, 2])
            self.assertEqual(report['pre_encode_black_indices'], [0, 2])
            self.assertEqual(report['changed_probe_indices'], [])
            self.assertEqual(recorder.recorded_frames, [])
            self.assertEqual(recorder.encode_calls, 1)
            self.assertIn('WARNING', output.call_args.args[0])
            self.assertIn("$_.Name.EndsWith('.capture_diagnostics.json')", text)

    def test_buffer_change_and_no_append_are_distinguished(self):
        for recorder, _ in self.recorders():
            self.capture(recorder, [12, None, 9])
            recorder.recorded_frames[0].value = 0
            recorder.stop_recording()
            report = json.loads(recorder.capture_diagnostics_path.read_text())
            self.assertEqual(report['capture_black_indices'], [])
            self.assertEqual(report['pre_encode_black_indices'], [0])
            self.assertEqual(report['changed_probe_indices'], [0])
            self.assertEqual(report['capture_no_append_steps'], [1])

    def test_sidecar_survives_encoder_failure(self):
        for recorder, _ in self.recorders():
            self.capture(recorder, [0, 255])
            recorder.encode_error = True
            with self.assertRaisesRegex(RuntimeError, 'synthetic encoder error'):
                recorder.stop_recording()
            report = json.loads(recorder.capture_diagnostics_path.read_text())
            self.assertEqual(report['stage'], 'before_encoding')
            self.assertEqual(report['capture_black_indices'], [0])
            self.assertEqual(len(recorder.recorded_frames), 2)

    def test_initial_black_is_info_and_dark_nonzero_is_not_black(self):
        for recorder, _ in self.recorders():
            self.capture(recorder, [0, 1, 2])
            with mock.patch('builtins.print') as output:
                recorder.stop_recording()
            self.assertIn('INFO', output.call_args.args[0])
            report = json.loads(recorder.capture_diagnostics_path.read_text())
            self.assertEqual(report['pre_encode_black_indices'], [0])

    def test_diagnostic_write_failure_does_not_block_encoding(self):
        for recorder, _ in self.recorders():
            self.capture(recorder, [255])
            recorder.capture_diagnostics_path = recorder.capture_diagnostics_path / 'missing.json'
            with mock.patch('builtins.print') as output:
                self.assertEqual(recorder.stop_recording(), 'encoded')
            self.assertEqual(recorder.encode_calls, 1)
            self.assertIn('pre-encode probe', output.call_args.args[0])

    def test_no_frame_is_preserved_without_encoding(self):
        for recorder, _ in self.recorders():
            self.capture(recorder, [None])
            report = json.loads(recorder.capture_diagnostics_path.read_text())
            self.assertEqual(report['stage'], 'capture_no_append')
            self.assertEqual(report['capture_no_append_steps'], [0])
            self.assertEqual(recorder.encode_calls, 0)

    def test_fractional_and_signed_pixels_are_not_mistaken_for_black(self):
        for recorder, _ in self.recorders():
            self.capture(recorder, [0.5, 0])
            recorder.recorded_frames[1].min = lambda: -1
            recorder.stop_recording()
            report = json.loads(recorder.capture_diagnostics_path.read_text())
            self.assertEqual(report['capture_black_indices'], [1])
            self.assertEqual(report['pre_encode_black_indices'], [])
            self.assertEqual(report['changed_probe_indices'], [1])


if __name__ == '__main__':
    unittest.main()
