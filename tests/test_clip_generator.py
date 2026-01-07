import tempfile
import os
from scripts.clip_generator import parse_vtt, parse_time

VTT_SAMPLE = """WEBVTT

00:00:01.000 --> 00:00:05.000
Hello world

00:00:06.500 --> 00:00:12.000
Another segment
"""

def test_parse_time():
    assert abs(parse_time('00:00:01,000') - 1.0) < 0.001
    assert abs(parse_time('00:01:00.000') - 60.0) < 0.001


def test_parse_vtt(tmp_path):
    p = tmp_path / "sample.vtt"
    p.write_text(VTT_SAMPLE)
    segments = parse_vtt(str(p))
    assert len(segments) == 2
    assert segments[0]['text'] == 'Hello world'
    assert abs(segments[0]['start'] - 1.0) < 0.001
    assert abs(segments[1]['end'] - 12.0) < 0.001
