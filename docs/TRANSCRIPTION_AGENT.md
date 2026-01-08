# Transcription & Captioning Agent

This agent transcribes audio/video media, runs speaker diarization, generates captions (VTT/SRT) and prepares embeddings for RAG indexing.

## Overview

- Input: any media file (video/audio), mixed master audio, or per-track audio.

- Output: WebVTT, SRT, JSON transcript, diarization JSON, optional embedding index (FAISS) and an index pointer.

## Usage

- CLI (prototype):

  python scripts/transcribe_agent/cli.py --input episode.mp4 --out transcripts/

## Backends & optional packages

- Whisper: `whisper` (already used by `scripts/transcribe.py`) or `whisperx` for word-level alignment.

- Diarization: `pyannote.audio` (best quality), speaker embedding clustering (resemblyzer) is an alternative.

- Embeddings: `sentence-transformers` (e.g., `all-MiniLM-L6-v2`) + `faiss-cpu` for local vector store.

## Indexing for RAG

- Embeddings produced by `sentence-transformers` can be stored into a FAISS index. Store the index file and a JSON mapping of ids -> metadata (episode, time range).

## Notes

- All heavy dependencies are optional; the agent will fall back to simple single-speaker transcripts if diarization or embedding libraries are not installed.

- Add a scheduled job or post-publish hook to call the agent for every new episode and upload transcripts/embeddings to the archive/storage.
