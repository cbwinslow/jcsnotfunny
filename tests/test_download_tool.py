from pathlib import Path

from scripts.tools.download_video import download_video


def test_download_video_creates_file(tmp_path):
    out = download_video("https://example.com/video123", str(tmp_path))
    p = Path(out['video_path'])
    assert p.exists()
    assert 'duration' in out
    # duration may be None if ffprobe not installed
    assert out['duration'] is None or isinstance(out['duration'], (int, float))
    # cleanup
    p.unlink()
