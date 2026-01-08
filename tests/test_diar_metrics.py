import json
from pathlib import Path

from scripts.transcribe_agent.compute_diar_metrics import compute


def test_compute_metrics_identical():
    expected = Path('tests/fixtures/transcripts/two_speaker.diar.json')
    actual = expected
    out = compute(str(expected), str(actual))
    assert out['avg_boundary_error_seconds'] == 0
    assert out['coverage'] == 1.0
    assert out['expected_segments'] == out['actual_segments']
