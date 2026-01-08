import json
import tempfile
from scripts.auto_edit.edl_generator import select_candidate_clips, write_edl


def test_select_candidate_clips_basic():
    segments = [
        {"start": 0, "end": 5, "text": "This is funny LOL", "funny_score": 0.8},
        {"start": 10, "end": 12, "text": "small laugh haha", "funny_score": 0.6},
        {"start": 20, "end": 40, "text": "too long but maybe", "funny_score": 0.9},
        {"start": 30, "end": 33, "text": "overlap laugh lmao", "funny_score": 0.7},
    ]

    clips = select_candidate_clips(segments, min_duration=4, max_duration=15, max_clips=3, min_funny_score=0.5)

    # Should return up to 3 clips
    assert len(clips) <= 3

    # Each clip must be within constraints
    for c in clips:
        assert c["duration"] >= 4
        assert c["duration"] <= 15
        assert c["funny_score"] >= 0.5

    # Clips should be non-overlapping
    for i in range(len(clips)):
        for j in range(i + 1, len(clips)):
            assert not (clips[i]["end"] > clips[j]["start"] and clips[j]["end"] > clips[i]["start"])


def test_write_edl_and_cli(tmp_path):
    segments = [
        {"start": 0, "end": 6, "text": "Funny mock", "funny_score": 0.7}
    ]
    clips = select_candidate_clips(segments, min_duration=4, max_duration=10)

    out = tmp_path / "out.edl.json"
    write_edl(clips, str(out))

    loaded = json.loads(out.read_text())
    assert "clips" in loaded
    assert loaded["count"] == len(clips)
