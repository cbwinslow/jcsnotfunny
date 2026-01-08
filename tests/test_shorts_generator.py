import tempfile
from pathlib import Path
from scripts.shorts.generate_short import generate_clips_from_edl


def test_generate_clips_dry_run(tmp_path):
    src = tmp_path / "source.mp4"
    src.write_bytes(b"FAKEVIDEO")

    edl = [{"clip_id": 1, "start": 0, "end": 5, "text": "funny", "funny_score": 0.8}]
    out_dir = tmp_path / "outs"

    outputs = generate_clips_from_edl(str(src), edl, str(out_dir), dry_run=True)

    assert len(outputs) == 1
    assert Path(outputs[0]).exists()
    assert Path(outputs[0]).stat().st_size > 0
