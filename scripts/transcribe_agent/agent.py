"""Transcription agent: orchestrate transcribe, diarize, captions, and embeddings.

Design goals:
- Safe imports: heavy libraries imported lazily so unit tests can run without GPUs.
- Produce: VTT, SRT, JSON transcript (with segments), embeddings (optional), and an index file for RAG.
- Provide simple defaults using available stubs (whisper/whisperx) and fallbacks.
"""
from __future__ import annotations
import json
import logging
import os
from pathlib import Path
from typing import Dict, List

# reuse existing helper for VTT timestamp formatting
try:
    from scripts.transcribe import format_time
except Exception:
    def format_time(seconds):
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = seconds % 60
        return f"{h:02d}:{m:02d}:{s:06.3f}".replace('.', ',')

logger = logging.getLogger('transcribe_agent')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(handler)


def ensure_dir(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


def transcribe_media(input_file: str, out_dir: str, backend: str = 'whisper') -> Dict:
    """Transcribe `input_file` and write outputs to `out_dir`.

    Returns a dict with paths to generated artifacts.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    base = out_dir / (Path(input_file).stem)

    vtt_path = str(base.with_suffix('.vtt'))
    json_path = str(base.with_suffix('.json'))

    # Use existing legacy script if whisper is the selected backend
    if backend == 'whisper':
        try:
            from scripts import transcribe as legacy
        except Exception:
            logger.exception('Failed to import legacy transcribe module')
            raise
        legacy.transcribe_with_whisper(input_file, vtt_path)
        # legacy writes JSON sidecar at vtt + .json
        if os.path.exists(vtt_path + '.json'):
            # normalize to our json path
            os.replace(vtt_path + '.json', json_path)
        else:
            # create a minimal JSON
            meta = {'segments': []}
            with open(json_path, 'w') as fh:
                json.dump(meta, fh)

    elif backend == 'whisperx':
        # Use whisper + whisperx alignment to produce word-level timestamps
        try:
            _whisperx_transcribe_and_align(input_file, vtt_path, json_path)
        except Exception:
            logger.exception('whisperx backend failed')
            raise

    else:
        raise NotImplementedError('Only whisper and whisperx backends are implemented in prototype')

    return {'vtt': vtt_path, 'json': json_path}


def _whisperx_transcribe_and_align(input_file: str, vtt_path: str, json_path: str):
    """Transcribe with Whisper and align with WhisperX to produce word-level timestamps.

    Writes a VTT file and a JSON sidecar containing segments and word-level segments.
    """
    try:
        import whisper
        import whisperx
    except Exception as exc:
        logger.error('whisperx not available: %s', exc)
        raise

    logger.info('Loading whisper model for %s', input_file)
    model = whisper.load_model('small')
    result = model.transcribe(input_file)
    segments = result.get('segments', [])
    language = result.get('language')
    text = result.get('text')

    logger.info('Loading whisperx align model')
    align_model, metadata = whisperx.load_align_model(language_code=language, device='cpu')
    aligned = whisperx.align(segments, align_model, metadata, input_file, device='cpu')
    # aligned contains 'word_segments'
    word_segments = aligned.get('word_segments') or []

    # write VTT using segment-level text
    os.makedirs(os.path.dirname(vtt_path) or '.', exist_ok=True)
    with open(vtt_path, 'w') as fh:
        fh.write('WEBVTT\n\n')
        for s in segments:
            start = s['start']
            end = s['end']
            text_seg = s.get('text', '').strip()
            fh.write(f"{format_time(start)} --> {format_time(end)}\n{text_seg}\n\n")

    meta = {
        'language': language,
        'text': text,
        'segments': segments,
        'word_segments': word_segments,
    }
    with open(json_path, 'w') as fh:
        json.dump(meta, fh)
    logger.info('whisperx alignment complete and written to %s', json_path)


def convert_vtt_to_srt(vtt_path: str, srt_path: str):
    """Convert VTT to SRT (simple conversion)."""
    with open(vtt_path, 'r') as fh:
        lines = fh.read().splitlines()
    out = []
    seq = 1
    buf = []
    for line in lines:
        if line.strip() == 'WEBVTT':
            continue
        if '-->' in line:
            if buf:
                out.append('\n'.join(buf))
                buf = []
            buf.append(str(seq))
            seq += 1
            buf.append(line.replace('.', ','))
        elif line.strip() == '':
            if buf:
                out.append('\n'.join(buf))
                buf = []
        else:
            buf.append(line)
    if buf:
        out.append('\n'.join(buf))
    with open(srt_path, 'w') as fh:
        fh.write('\n\n'.join(out))


def run_diarization(audio_file: str) -> List[Dict]:
    """Attempt to run speaker diarization and return list of segments:
    [{'start': float, 'end': float, 'speaker': 'SPEAKER_0', 'confidence': 0.9}, ...]

    Falls back to a single-speaker segment if library isn't available.
    """
    try:
        from pyannote.audio import Pipeline
    except Exception:
        logger.warning('pyannote.audio not available; returning single speaker fallback')
        # fallback single segment entire file
        import soundfile as sf
        try:
            dur = sf.info(audio_file).duration
        except Exception:
            dur = 0.0
        return [{'start': 0.0, 'end': dur, 'speaker': 'SPEAKER_0', 'confidence': 0.0}]

    # Example usage if Pipeline is configured via env variables and auth
    pipeline = Pipeline.from_pretrained('pyannote/speaker-diarization')
    diarization = pipeline(audio_file)
    out = []
    idx = 0
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        out.append({'start': turn.start, 'end': turn.end, 'speaker': speaker, 'confidence': 1.0})
        idx += 1
    return out


def embeddings_for_transcript(text: str, model_name: str = 'all-MiniLM-L6-v2'):
    """Compute embeddings for transcript using sentence-transformers (optional)."""
    try:
        from sentence_transformers import SentenceTransformer
    except Exception:
        logger.warning('sentence-transformers not available; skipping embeddings')
        return None
    model = SentenceTransformer(model_name)
    sent_emb = model.encode(text.split('\n'), show_progress_bar=False)
    return sent_emb


def index_embeddings(embeddings, ids, index_path: str):
    """Save embeddings to a FAISS index if available, otherwise a JSON fallback."""
    try:
        import faiss
    except Exception:
        logger.warning('faiss not available; storing embeddings as JSON')
        out = {'ids': ids, 'embeddings': [e.tolist() for e in embeddings]}
        with open(index_path, 'w') as fh:
            json.dump(out, fh)
        return index_path

    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    import numpy as np
    matrix = np.vstack(embeddings).astype('float32')
    index.add(matrix)
    faiss.write_index(index, index_path)
    return index_path


def build_transcript_package(input_file: str, out_dir: str, do_diarize: bool = True, do_embeddings: bool = True):
    """High-level helper: transcribe, optionally diarize and embed; returns summary dict."""
    out = transcribe_media(input_file, out_dir)
    summary = {'vtt': out['vtt'], 'json': out['json']}

    if do_diarize:
        # extract audio from media if needed
        audio_path = str(Path(out_dir) / (Path(input_file).stem + '.wav'))
        if not Path(audio_path).exists():
            # attempt to extract using ffmpeg
            cmd = f"ffmpeg -y -i {input_file} -vn -acodec pcm_s16le -ar 16000 -ac 1 {audio_path}"
            logger.info('Extracting audio for diarization: %s', cmd)
            os.system(cmd)
        diar = run_diarization(audio_path)
        summary['diarization'] = diar
        with open(Path(out_dir) / (Path(input_file).stem + '.diar.json'), 'w') as fh:
            json.dump(diar, fh)

    if do_embeddings:
        with open(out['json'], 'r') as fh:
            meta = json.load(fh)
        text = meta.get('text') or ''
        emb = embeddings_for_transcript(text)
        if emb is not None:
            ids = [f"{Path(input_file).stem}_{i}" for i in range(len(emb))]
            idx_path = str(Path(out_dir) / (Path(input_file).stem + '.emb.index'))
            index_embeddings(emb, ids, idx_path)
            summary['embeddings'] = idx_path

    return summary
