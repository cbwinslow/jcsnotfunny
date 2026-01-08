import json
from pathlib import Path

from scripts.transcribe_agent.agent import run_diarization


def test_run_diarization_with_pyannote_mock(monkeypatch):
    # Prepare fake diarization result similar to fixture two_speaker
    class FakeTurn:
        def __init__(self, start, end):
            self.start = start
            self.end = end

    class FakeDiarization:
        def __init__(self, segments):
            self._segments = segments

        def itertracks(self, yield_label=False):
            # yield (turn, None, speaker_label)
            for i, (s, e) in enumerate(self._segments):
                yield (FakeTurn(s, e), None, f"S{i}")

    class FakePipeline:
        @classmethod
        def from_pretrained(cls, name):
            return cls()

        def __call__(self, audio_path):
            # return segments that match two_speaker.diar.json
            # introduce a small offset to emulate real model behavior
            return FakeDiarization([(0.0, 0.49), (0.5, 0.99)])

    # Insert fake pyannote.audio module into sys.modules so import succeeds
    import sys, types
    fake_mod = types.SimpleNamespace(Pipeline=FakePipeline)
    monkeypatch.setitem(sys.modules, 'pyannote.audio', fake_mod)
    # Also ensure module-level Pipeline reference is set if already imported
    monkeypatch.setattr('scripts.transcribe_agent.agent.Pipeline', FakePipeline, raising=False)

    fixture = Path('tests/fixtures/transcripts/two_speaker.diar.json')
    expected = json.loads(fixture.read_text())

    out = run_diarization('tests/fixtures/transcripts/two_speaker.wav')
    # should return two segments
    assert len(out) == len(expected)

    # compute average absolute boundary error across starts and ends
    total_err = 0.0
    count = 0
    for a, b in zip(out, expected):
        total_err += abs(a['start'] - b['start'])
        total_err += abs(a['end'] - b['end'])
        count += 2
    avg_err = total_err / count
    assert avg_err <= 0.5
