#!/usr/bin/env python3
"""Simple transcription skeleton.
This script is intended to be a lightweight helper to call WhisperX or a mock implementation.
"""
import json
from pathlib import Path


def run_transcription(audio_path: str, output_vtt: str) -> dict:
    # For now, simulate by creating a minimal VTT file and metadata
    vtt = Path(output_vtt)
    vtt.parent.mkdir(parents=True, exist_ok=True)
    vtt.write_text("WEBVTT\n\n00:00.000 --> 00:05.000\nHello world\n")

    metadata = {
        "vtt_path": str(vtt),
        "raw_transcript_path": str(vtt.with_suffix('.txt')),
        "language": "en",
        "duration_seconds": 5,
        "diarization": []
    }
    Path(metadata['raw_transcript_path']).write_text("Hello world\n")
    # If whisperx is available, use it to produce higher-quality alignment and VTT
    try:
        import whisperx  # type: ignore

        try:
            model = whisperx.load_model("small", device="cpu")
            result = model.transcribe(str(Path(audio_path)), batch_size=16)
            # alignment
            align_model = whisperx.load_align_model(result["language"], device="cpu")
            result_aligned = whisperx.align(result["segments"], model, str(Path(audio_path)), align_model, device="cpu")

            # write VTT
            vtt = Path(output_vtt)
            with open(vtt, "w") as f:
                f.write("WEBVTT\n\n")
                for seg in result_aligned:
                    start = seg["start"]
                    end = seg["end"]
                    text = seg["text"].strip().replace("\n", " ")
                    f.write(f"{format_timestamp(start)} --> {format_timestamp(end)}\n{text}\n\n")

            metadata["engine"] = "whisperx"
            metadata["vtt_path"] = str(vtt)
        except Exception:
            # if whisperx fails during runtime, fallback gracefully
            metadata["engine"] = "placeholder"
    except Exception:
        metadata["engine"] = "placeholder"

    return metadata


# small helper for timestamp formatting

def format_timestamp(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"
