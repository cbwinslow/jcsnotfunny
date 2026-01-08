# Transcription & Diarization — Summary

Scope: transcribe audio/video → produce WebVTT and JSON sidecars; optionally run speaker diarization and generate embeddings.

Key locations
- `scripts/transcribe.py` — CLI wrapper (whisper, api backends)
- `scripts/transcribe_agent/agent.py` — high-level orchestration, diarization hooks, package builder
- Tests: `tests/test_transcription_fixtures.py`, `tests/test_transcribe_agent.py`
- CI: `transcribe-integration.yml` runs transcription tests and metrics

Operational notes
- Default backend: `whisper` (local) — can fall back to `TRANSCRIBE_BACKEND=api` for external services
- Use fixtures in `tests/fixtures/transcripts/` for deterministic CI

Next steps
- Add alignment verification and embedding tests for RAG pipelines
- Add VAD/diarization integration tests with sample assets


Related docs: `docs/TRANSCRIPTION_AGENT.md`, `docs/TESTING_AND_TROUBLESHOOTING.md`
