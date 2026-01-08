from validators.transcript_validator import validate_vtt

VTT = """WEBVTT

00:00:01.000 --> 00:00:05.000
Hello world
"""

def test_validate_vtt(tmp_path):
    p = tmp_path / 's.vtt'
    p.write_text(VTT)
    ok, errs = validate_vtt(str(p))
    assert ok
    assert errs == []
