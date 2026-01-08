import shutil
from pathlib import Path
import json

from tests.fixtures.transcripts.generate_fixtures import generate_all
from scripts.transcribe_agent.agent import transcribe_media, build_transcript_package


def test_generate_fixtures(tmp_path):
    # Generate fixtures into test tmp directory and ensure files created
    fixtures_dir = tmp_path / 'fixtures'
    fixtures_dir.mkdir()
    # Execute generator to ensure fixtures exist
    generate_all()
    base = Path('tests/fixtures/transcripts')
    assert (base / 'single_speaker.wav').exists()
    assert (base / 'single_speaker.vtt').exists()
    assert (base / 'two_speaker.wav').exists()
    assert (base / 'two_speaker.vtt').exists()


def test_transcribe_media_with_fixture(monkeypatch, tmp_path):
    # Ensure transcribe_media writes expected VTT and JSON by monkeypatching legacy transcribe
    generated = Path('tests/fixtures/transcripts')
    single_wav = generated / 'single_speaker.wav'
    out_dir = tmp_path / 'out'
    out_dir.mkdir()

    def fake_transcribe(input_file, vtt_path):
        # copy the expected vtt to the output
        shutil.copy(str(generated / 'single_speaker.vtt'), vtt_path)
        with open(vtt_path + '.json', 'w') as fh:
            json.dump({'text': 'hello world'}, fh)

    monkeypatch.setattr('scripts.transcribe.transcribe_with_whisper', fake_transcribe)
    res = transcribe_media(str(single_wav), str(out_dir))
    assert Path(res['vtt']).exists()
    text = (Path(res['vtt']).read_text())
    assert 'hello world' in text
    assert Path(res['json']).exists()


def test_build_transcript_package_integration(monkeypatch, tmp_path):
    # Run high-level package builder with monkeypatched transcribe to ensure diarization file produced
    generated = Path('tests/fixtures/transcripts')
    two_wav = generated / 'two_speaker.wav'

    def fake_transcribe(input_file, vtt_path):
        shutil.copy(str(generated / 'two_speaker.vtt'), vtt_path)
        with open(vtt_path + '.json', 'w') as fh:
            json.dump({'text': 'first speaker\nsecond speaker'}, fh)

    monkeypatch.setattr('scripts.transcribe.transcribe_with_whisper', fake_transcribe)
    # stub diarization to return segments like the fixture
    monkeypatch.setattr('scripts.transcribe_agent.agent.run_diarization', lambda x: json.loads((generated / 'two_speaker.diar.json').read_text()))

    out = build_transcript_package(str(two_wav), str(tmp_path / 'out'))
    assert 'vtt' in out and Path(out['vtt']).exists()
    assert 'json' in out and Path(out['json']).exists()
    assert 'diarization' in out
    assert len(out['diarization']) == 2
