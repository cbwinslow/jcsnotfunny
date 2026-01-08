# Transcription & Captioning Agent (Priority: 1)

Summary

Build a robust transcription/captioning agent that produces accurate WebVTT/SRT, speaker diarization, JSON transcripts, and embeddings for RAG indexing for every media item (audio/video/streams). This enables search, clipping, and RAG pipelines.

Acceptance criteria (measurable)

- For the provided synthetic test assets, the agent produces `*.vtt`, `*.json`, and `*.diar.json` files and the VTT contains the expected sample lines (assert exact matches in tests).

- Diarization test asserts correct number of speaker segments for 2-speaker synthetic file and segment boundaries differ from ground-truth by <= 0.5s on average.

- Embedding index is created and a nearest-neighbor lookup returns the expected nearest sentence for a given query (FAISS or JSON fallback).

- CI job `transcribe-integration.yml` runs on push and passes on the sample dataset.

Subtasks / microgoals

- Add synthetic single-speaker and multi-speaker WAVs with ground-truth captions.

- Integrate whisperx alignment and pyannote diarization (with documented auth/config).

- Produce VTT/SRT, JSON transcript, diarization `.diar.json`, and embedding index.

- Add tests: diarization accuracy, VTT content, embedding NN lookup.

- Add CI workflow to run integration test and upload artifacts.

Labels: type/automation, area/editing, priority/high

Estimate: 2–5 days (prototype + tests)

Notes: See `docs/TRANSCRIPTION_AGENT.md` and `scripts/transcribe_agent/` for existing prototype code.
