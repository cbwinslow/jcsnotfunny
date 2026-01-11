# Transcription & Captioning Milestone (Milestone #5)

Overview

This milestone consolidates the work needed to make transcription and captioning reliable and testable across the repo. It contains small, reviewable tasks so multiple agents (human or automated) can take ownership.

Milestone owner: @cbwinslow
Due: 2026-01-31

Primary issue: https://github.com/cbwinslow/jcsnotfunny/issues/21

Subtasks (linked issues)
- #24 Add synthetic test assets (single and 2-speaker WAVs + expected VTT/diarization outputs)
- #28 Add transcribe CI workflow (`.github/workflows/transcribe-integration.yml`)
- #25 Integrate whisperx alignment (word-level timestamps, opt-in)
- #26 Integrate pyannote diarization
- #27 Embedding creation & NN lookup test (FAISS or JSON fallback)

How to help

- Pick an open sub-issue (see project board 'Project v2 — Production') and leave a comment that you're taking it.
- Use `scripts/triage/sync_milestone.py --milestone 5 <issue_number...>` to ensure your issues are attached to the milestone and commented.
- Follow the acceptance criteria listed on each sub-issue; add unit tests and a small PR when ready.

CI & testing

The integration workflow `transcribe-integration.yml` is a daily smoke (and manually dispatchable) runner that exercises the transcribe pipeline against fixtures.

Notes

- Keep model-specific or heavyweight dependencies optional and gated behind environment variables (e.g., `TRANSCRIBE_BACKEND=whisper|api`).
- Focus on reproducible, small fixtures and deterministic tests to make CI stable and fast.
