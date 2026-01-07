from scripts.transcribe import format_time


def test_format_time_seconds():
    assert format_time(1.234).startswith('00:00:01')
    assert format_time(3661.5).startswith('01:01:01')
