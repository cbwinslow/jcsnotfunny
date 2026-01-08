import wave
from array import array
from scripts.clip_generator import (
    parse_vtt,
    parse_time,
    parse_transcript,
    detect_laughter_segments,
    score_segment,
    select_interesting_segments,
)

VTT_SAMPLE = """WEBVTT

00:00:01.000 --> 00:00:05.000
Hello world

00:00:06.500 --> 00:00:12.000
Another segment
"""

SRT_SAMPLE = """1
00:00:01,000 --> 00:00:05,000
Hello world

2
00:00:06,500 --> 00:00:12,000
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


def test_parse_srt(tmp_path):
    p = tmp_path / "sample.srt"
    p.write_text(SRT_SAMPLE)
    segments = parse_vtt(str(p))
    assert len(segments) == 2
    assert segments[1]['text'] == 'Another segment'


def test_parse_transcript_json(tmp_path):
    p = tmp_path / "sample.json"
    p.write_text('{"segments": [{"start": 0.0, "end": 1.0, "text": "hi"}]}')
    segments = parse_transcript(str(p))
    assert len(segments) == 1
    assert segments[0]['text'] == 'hi'


def test_score_segment_laughter():
    seg = {'start': 0.0, 'end': 20.0, 'text': 'That was hilarious, haha!'}
    score, reasons = score_segment(seg, diarization=[])
    assert score > 0
    assert 'laughter' in reasons


def test_score_segment_audio_laughter():
    seg = {'start': 1.0, 'end': 2.0, 'text': 'plain text'}
    laughter_segments = [{'start': 0.5, 'end': 1.5, 'confidence': 0.8}]
    score, reasons = score_segment(seg, diarization=[], laughter_segments=laughter_segments)
    assert score > 0
    assert 'laughter_audio' in reasons


def test_select_interesting_segments():
    segments = [
        {'start': 0.0, 'end': 10.0, 'text': 'hello'},
        {'start': 10.0, 'end': 30.0, 'text': 'big laugh haha'},
    ]
    selected = select_interesting_segments(segments, diarization=[], laughter_segments=[], max_clips=1)
    assert len(selected) == 1
    assert 'laugh' in selected[0]['text']


def test_detect_laughter_segments(tmp_path):
    test_audio = tmp_path / "laugh.wav"
    samples = array('h')
    rate = 16000
    for duration, amplitude in [(1.0, 0), (1.0, 12000), (1.0, 0), (0.8, 10000)]:
        count = int(rate * duration)
        for i in range(count):
            value = amplitude if i % 2 == 0 else -amplitude
            samples.append(value)
    with wave.open(str(test_audio), 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        wf.writeframes(samples.tobytes())

    segments = detect_laughter_segments(str(test_audio), window_sec=0.25, min_duration=0.5)
    assert len(segments) >= 1
    assert any(seg['start'] <= 1.1 <= seg['end'] for seg in segments)
