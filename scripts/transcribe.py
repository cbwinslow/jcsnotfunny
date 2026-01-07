"""Transcription agent (stub)

Usage:
  python scripts/transcribe.py --input audio.wav --output transcript.vtt

This is a minimal example that uses OpenAI Whisper if installed, or falls back
to calling a configurable transcription API. It writes a WebVTT file and a
simple JSON summary with word-level timestamps if available.

Environment:
- Optionally set TRANSCRIBE_BACKEND to 'whisper' or 'api'.
- For 'api', configure TRANSCRIBE_API_KEY and TRANSCRIBE_API_URL.
"""
import argparse
import json
import os
import logging

logger = logging.getLogger('transcribe')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(handler)


def transcribe_with_whisper(input_file, output_vtt):
    try:
        import whisper
    except Exception:
        logger.error("Whisper not available; install 'whisper' or set TRANSCRIBE_BACKEND=api")
        raise RuntimeError("Whisper not available; install 'whisper' or set TRANSCRIBE_BACKEND=api")
    logger.info('Loading whisper model')
    model = whisper.load_model("small")
    result = model.transcribe(input_file)
    # Save VTT
    segments = result.get("segments", [])
    os.makedirs(os.path.dirname(output_vtt) or '.', exist_ok=True)
    with open(output_vtt, "w") as fh:
        fh.write("WEBVTT\n\n")
        for s in segments:
            start = s['start']
            end = s['end']
            text = s['text'].strip()
            fh.write(f"{format_time(start)} --> {format_time(end)}\n{text}\n\n")
    # Save summary JSON
    meta = {
        'language': result.get('language'),
        'text': result.get('text'),
        'segments': segments,
    }
    with open(output_vtt + '.json', 'w') as fh:
        json.dump(meta, fh, indent=2)
    logger.info('Transcription complete')


def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    # Use standard VTT formatting HH:MM:SS.mmm
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace('.', ',')




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    backend = os.environ.get('TRANSCRIBE_BACKEND', 'whisper')
    if backend == 'whisper':
        transcribe_with_whisper(args.input, args.output)
    else:
        # Example fallback: call external API
        url = os.environ.get('TRANSCRIBE_API_URL')
        key = os.environ.get('TRANSCRIBE_API_KEY')
        if not url or not key:
            raise RuntimeError('TRANSCRIBE_API_URL and TRANSCRIBE_API_KEY must be set to use API backend')
        # This is intentionally a stub; implement your API calls here
        raise RuntimeError('API backend not implemented in stub')

if __name__ == '__main__':
    main()
