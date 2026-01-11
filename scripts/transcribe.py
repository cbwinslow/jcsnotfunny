# Backwards-compatible shim for older imports/tests.
from scripts.transcription.transcribe import format_time, transcribe_with_whisper  # noqa: F401

__all__ = ["format_time", "transcribe_with_whisper"]
