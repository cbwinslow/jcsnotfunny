from pathlib import Path

from scripts.tools.thumbnail_renderer import render_thumbnail


def test_render_thumbnail_creates_file(tmp_path):
    out = render_thumbnail("video.mp4#t=10", "Funny moment", str(tmp_path / "thumb.png"))
    p = Path(out['thumbnail_path'])
    assert p.exists()
    assert p.read_text().startswith("Thumbnail for")
