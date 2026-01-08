import json
from pathlib import Path

from scripts.transcribe_agent.agent import transcribe_media, convert_vtt_to_srt, build_transcript_package


def test_transcribe_media_fallback(monkeypatch, tmp_path):
    # Ensure whisper backend path uses legacy transcribe function; we will monkeypatch it
    in_f = tmp_path / "audio.wav"
    in_f.write_bytes(b"dummy")

    out_dir = tmp_path / "out"

    class Dummy:
        def __init__(self):
            pass

    # monkeypatch the legacy module function to create a vtt and json
    def fake_transcribe(input_file, vtt_path):
        with open(vtt_path, 'w') as fh:
            fh.write('WEBVTT\n\n00:00:00.000 --> 00:00:01.000\nhello\n')
        with open(vtt_path + '.json', 'w') as fh:
            json.dump({'text': 'hello'}, fh)

    monkeypatch.setattr('scripts.transcribe.transcribe_with_whisper', fake_transcribe)

    out = transcribe_media(str(in_f), str(out_dir))
    assert Path(out['vtt']).exists()
    assert Path(out['json']).exists()


def test_convert_vtt_to_srt(tmp_path):
    vtt = tmp_path / 'foo.vtt'
    vtt.write_text('WEBVTT\n\n00:00:00.000 --> 00:00:01.000\nhello\n')
    srt = tmp_path / 'foo.srt'
    convert_vtt_to_srt(str(vtt), str(srt))
    assert srt.exists()


def test_build_transcript_package(monkeypatch, tmp_path):
    in_f = tmp_path / "audio.wav"
    in_f.write_bytes(b"dummy")

    # stub transcribe_media
    def fake_transcribe(input_file, out_dir):
        o = tmp_path / 'out'
        o.mkdir()
        vtt = o / (Path(input_file).stem + '.vtt')
        vtt.write_text('WEBVTT\n\n00:00:00.000 --> 00:00:01.000\nhello\n')
        with open(str(vtt) + '.json', 'w') as fh:
            json.dump({'text': 'hello'}, fh)
        return {'vtt': str(vtt), 'json': str(vtt) + '.json'}

    monkeypatch.setattr('scripts.transcribe_agent.agent.transcribe_media', fake_transcribe)

    # stub diarization to avoid heavy deps
    monkeypatch.setattr('scripts.transcribe_agent.agent.run_diarization', lambda x: [{'start': 0, 'end': 1, 'speaker': 'S0', 'confidence': 0.5}])
    res = build_transcript_package(str(in_f), str(tmp_path / 'out'))
    assert 'diarization' in res
    assert 'vtt' in res
