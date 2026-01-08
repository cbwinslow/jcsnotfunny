---
name: Feature Request
about: Suggest an idea for this project
title: 'Enhance: Integrate advanced features for Transcribe & Captioning Agent (scripts/transcribe.py)'
labels: enhancement, type/automation, area/editing, priority/high
assignees: ''

---

This issue is for integrating advanced features into the `scripts/transcribe.py` script, which is part of the Transcribe & Captioning Agent. This aligns with PRIORITY 1 as defined in `tasks.md`.

**Description:**
The `scripts/transcribe.py` currently provides basic transcription. This task involves enhancing it with advanced capabilities like word-level alignment, speaker diarization, and embedding generation to enable search, clipping, and RAG pipelines.

**Subtasks (from tasks.md):**
- Integrate word-level alignment (whisperx) and speaker diarization (pyannote or equivalent).
- Produce VTT/SRT, JSON transcript, diarization `.diar.json`, and embedding index (FAISS or JSON fallback).

**Acceptance Criteria (from tasks.md):**
- On the provided synthetic test assets, the agent produces `*.vtt`, `*.json`, and `*.diar.json` files and the VTT contains the expected sample lines (assert exact matches in tests).
- Diarization test asserts correct number of speaker segments for 2-speaker synthetic file and that segment boundaries differ from ground-truth by <= 0.5s on average (measured in unit test).
- Embedding index is created and a small nearest-neighbor lookup returns the expected nearest sentence for a given query (testable with FAISS or JSON fallback).
- A CI job `transcribe-integration.yml` runs on a push and passes on the sample dataset.

**Additional Automation Opportunities (from previous analysis):**
- **Implement API Backend:** Complete the API backend in `transcribe.py` to allow for transcription via external services.
- **Automated Quality Checks for Transcripts:** Add a post-transcription step to validate VTT format and potentially check for profanity or sensitive words.
