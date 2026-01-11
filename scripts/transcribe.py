# Backwards-compatible shim for older imports/tests.
from scripts.transcription.transcribe import format_time  # noqa: F401

__all__ = ["format_time"]
