import json

from scripts.humor_score import load_segments


VTT_SAMPLE = """WEBVTT\n\n00:00:01.000 --> 00:00:03.000\nHello world\n"""


def test_load_segments_vtt(tmp_path):
    path = tmp_path / "sample.vtt"
    path.write_text(VTT_SAMPLE)
    segments = load_segments(str(path))
    assert len(segments) == 1
    assert segments[0]["text"] == "Hello world"


def test_load_segments_json(tmp_path):
    path = tmp_path / "sample.json"
    payload = {"segments": [{"start": 0.0, "end": 1.0, "text": "hi"}]}
    path.write_text(json.dumps(payload))
    segments = load_segments(str(path))
    assert len(segments) == 1
    assert segments[0]["text"] == "hi"


def test_load_segments_jsonl(tmp_path):
    path = tmp_path / "sample.jsonl"
    path.write_text('{"text": "line", "start": 1, "end": 2}\n')
    segments = load_segments(str(path))
    assert len(segments) == 1
    assert segments[0]["text"] == "line"
