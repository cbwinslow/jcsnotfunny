import importlib
from pathlib import Path

import pytest

from scripts.tools.run_transcription import run_transcription


@pytest.mark.skipif(importlib.util.find_spec("whisperx") is None, reason="whisperx not installed")
def test_whisperx_available_sets_engine(tmp_path):
    vtt_path = tmp_path / "out.vtt"
    metadata = run_transcription("dummy.wav", str(vtt_path))
    assert metadata.get("engine") == "whisperx"