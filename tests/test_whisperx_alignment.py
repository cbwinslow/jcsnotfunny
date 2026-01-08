import json
from pathlib import Path

from scripts.transcribe_agent.agent import transcribe_media


def test_whisperx_path_creates_word_segments(monkeypatch, tmp_path):
    # prepare fake whisper + whisperx behavior
    class FakeModel:
        def transcribe(self, input_file):
            return {
                'segments': [{'start': 0.0, 'end': 1.0, 'text': 'hello world'}],
                'language': 'en',
                'text': 'hello world'
            }

    class FakeAlignModel:
        pass

    def fake_load_model(name):
        return FakeModel()

    def fake_load_align_model(language_code=None, device=None):
        return (FakeAlignModel(), {'meta': True})

    def fake_align(segments, align_model, metadata, input_file, device=None):
        return {'word_segments': [
            {'start': 0.0, 'end': 0.5, 'word': 'hello'},
            {'start': 0.5, 'end': 1.0, 'word': 'world'},
        ]}

    import sys
    fake_whisper = type('m', (), {'load_model': lambda name: FakeModel()})
    fake_whisperx = type('m', (), {'load_align_model': fake_load_align_model, 'align': fake_align})
    sys.modules['whisper'] = fake_whisper
    sys.modules['whisperx'] = fake_whisperx
    # also ensure agent module picks them up if it imported previously
    try:
        import importlib
        importlib.reload(__import__('scripts.transcribe_agent.agent', fromlist=['*']))
    except Exception:
        pass

    in_wav = Path('tests/fixtures/transcripts/single_speaker.wav')
    out_dir = tmp_path / 'out'
    out_dir.mkdir()

    res = transcribe_media(str(in_wav), str(out_dir), backend='whisperx')
    j = json.loads(Path(res['json']).read_text())
    assert 'word_segments' in j
    assert len(j['word_segments']) == 2
    assert Path(res['vtt']).exists()
    vtt_text = Path(res['vtt']).read_text()
    assert 'hello world' in vtt_text
