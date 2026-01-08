"""Clip generation agent.

Takes a multimedia file (path or URL) + transcript (WebVTT/SRT/JSON) and
generates short clips based on transcript segments and simple scoring.

Usage:
  python scripts/clip_generator.py --input episode.mp4 --transcript episode.vtt --outdir clips/
  python scripts/clip_generator.py --input https://youtu.be/ID --transcript episode.vtt --outdir clips/ --mode interesting

Requires ffmpeg. URL inputs require yt-dlp for downloads.
"""
import argparse
import json
import os
import re
import subprocess
import logging
import math
import wave
from array import array
from pathlib import Path
from urllib.parse import urlparse

logger = logging.getLogger('clip_generator')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(ch)


LAUGHTER_TOKENS = ('laugh', 'laughter', 'haha', 'ha ha', '[laugh', '(laugh', 'lol')
COMMOTION_TOKENS = ('applause', 'crowd', 'cheer', 'cheering', 'gasps', 'gasp')
EMPHASIS_TOKENS = ('!', '?')
EXCITE_WORDS = ('wild', 'crazy', 'insane', 'hilarious', 'funny', 'best', 'worst')


def parse_vtt(vtt_path):
    """Parse a VTT/SRT file and return list of segments with start,end,text."""
    segments = []
    with open(vtt_path, 'r') as fh:
        content = fh.read()
    blocks = re.split(r"\n\n+", content.strip())
    for b in blocks:
        if '-->' not in b:
            continue
        lines = [line.strip() for line in b.splitlines() if line.strip()]
        time_idx = next((i for i, line in enumerate(lines) if '-->' in line), None)
        if time_idx is None:
            continue
        times = lines[time_idx]
        text = ' '.join(lines[time_idx + 1:]).strip()
        start, _arrow, end = times.partition('-->')
        segments.append({'start': parse_time(start.strip()), 'end': parse_time(end.strip()), 'text': text})
    return segments


def parse_time(t):
    """Convert 'HH:MM:SS,mmm' or 'H:MM:SS.mmm' to seconds (float)."""
    t = t.replace(',', '.')
    parts = t.split(':')
    if len(parts) == 3:
        s = float(parts[-1]) + int(parts[-2]) * 60 + int(parts[-3]) * 3600
    elif len(parts) == 2:
        s = float(parts[-1]) + int(parts[-2]) * 60
    else:
        s = float(parts[0])
    return s


def parse_transcript(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == '.json':
        with open(path, 'r') as fh:
            data = json.load(fh)
        segments = data.get('segments', []) if isinstance(data, dict) else []
        out = []
        for seg in segments:
            if not all(k in seg for k in ('start', 'end', 'text')):
                continue
            out.append({'start': float(seg['start']), 'end': float(seg['end']), 'text': seg['text']})
        return out
    return parse_vtt(path)


def is_url(value):
    try:
        parsed = urlparse(value)
        return parsed.scheme in ('http', 'https')
    except Exception:
        return False


def download_video(url, outdir, fmt):
    os.makedirs(outdir, exist_ok=True)
    output_template = os.path.join(outdir, '%(title).200s_%(id)s.%(ext)s')
    cmd = [
        'yt-dlp',
        '--no-progress',
        '-f',
        fmt,
        '-o',
        output_template,
        '--print',
        'filename',
        url,
    ]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    paths = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    if not paths:
        raise RuntimeError('yt-dlp did not return a filename')
    return paths[-1]


def resolve_input(input_value, download_dir, fmt):
    if is_url(input_value):
        return download_video(input_value, download_dir, fmt)
    return input_value


def load_diarization(path):
    if not path:
        return []
    with open(path, 'r') as fh:
        data = json.load(fh)
    if isinstance(data, dict):
        return data.get('segments', [])
    if isinstance(data, list):
        return data
    return []


def _count_token_hits(text, tokens):
    return sum(1 for token in tokens if token in text)

def _segment_bounds(segment):
    start = segment.get('start', segment.get('start_time'))
    end = segment.get('end', segment.get('end_time'))
    return start, end


def _overlaps(start_a, end_a, start_b, end_b):
    return start_a < end_b and start_b < end_a


def score_segment(segment, diarization=None, laughter_segments=None):
    diarization = diarization or []
    laughter_segments = laughter_segments or []
    text = (segment.get('text') or '').lower()
    duration = max(0.0, segment['end'] - segment['start'])
    score = 0.0
    reasons = []

    if 15 <= duration <= 60:
        score += 2.0
        reasons.append('ideal_length')
    elif 8 <= duration < 15:
        score += 1.0
        reasons.append('short_length')

    laughter_hits = _count_token_hits(text, LAUGHTER_TOKENS)
    if laughter_hits:
        score += 2.5 + (0.5 * min(laughter_hits, 3))
        reasons.append('laughter')

    commotion_hits = _count_token_hits(text, COMMOTION_TOKENS)
    if commotion_hits:
        score += 1.5
        reasons.append('crowd_reaction')

    emphasis_hits = sum(text.count(token) for token in EMPHASIS_TOKENS)
    if emphasis_hits:
        score += min(emphasis_hits, 3) * 0.5
        reasons.append('emphasis')

    if any(word in text for word in EXCITE_WORDS):
        score += 0.8
        reasons.append('excited_wording')

    speaker_set = set()
    for seg in diarization:
        if seg.get('end', 0) < segment['start'] or seg.get('start', 0) > segment['end']:
            continue
        speaker = seg.get('speaker')
        if speaker:
            speaker_set.add(speaker)
    if len(speaker_set) >= 2:
        score += 1.2
        reasons.append('multi_speaker')

    audio_laughter_score = 0.0
    for laugh in laughter_segments:
        laugh_start, laugh_end = _segment_bounds(laugh)
        if laugh_start is None or laugh_end is None:
            continue
        if _overlaps(segment['start'], segment['end'], laugh_start, laugh_end):
            confidence = min(max(float(laugh.get('confidence', 0.6)), 0.0), 1.0)
            audio_laughter_score = max(audio_laughter_score, 1.2 + (confidence * 1.8))
    if audio_laughter_score:
        score += audio_laughter_score
        reasons.append('laughter_audio')

    return score, reasons


def select_interesting_segments(segments, diarization=None, laughter_segments=None, max_clips=10, min_score=1.0):
    scored = []
    for seg in segments:
        score, reasons = score_segment(seg, diarization=diarization, laughter_segments=laughter_segments)
        scored.append({**seg, 'score': score, 'reasons': reasons})
    scored.sort(key=lambda item: item['score'], reverse=True)
    selected = [seg for seg in scored if seg['score'] >= min_score]
    return selected[:max_clips] if max_clips else selected


def ensure_wav_audio(audio_path, outdir):
    if audio_path.lower().endswith('.wav'):
        return audio_path
    os.makedirs(outdir, exist_ok=True)
    output_path = os.path.join(outdir, f"{Path(audio_path).stem}_laughter.wav")
    cmd = [
        'ffmpeg',
        '-y',
        '-i',
        audio_path,
        '-ac',
        '1',
        '-ar',
        '16000',
        '-acodec',
        'pcm_s16le',
        output_path,
    ]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    return output_path


def detect_laughter_segments(audio_path, window_sec=0.25, min_duration=0.6, max_gap=0.2):
    """Detect laughter-ish bursts using audio energy spikes."""
    def rms_from_frames(frames, sample_width):
        if not frames:
            return 0.0
        if sample_width == 1:
            samples = array('B')
            samples.frombytes(frames)
            values = [s - 128 for s in samples]
        elif sample_width == 2:
            samples = array('h')
            samples.frombytes(frames)
            values = samples
        elif sample_width == 4:
            samples = array('i')
            samples.frombytes(frames)
            values = samples
        else:
            raise ValueError(f"Unsupported sample width: {sample_width}")
        if not values:
            return 0.0
        sum_sq = 0.0
        for value in values:
            sum_sq += float(value) * float(value)
        return math.sqrt(sum_sq / len(values))

    with wave.open(audio_path, 'rb') as wf:
        sample_rate = wf.getframerate()
        sample_width = wf.getsampwidth()
        frames_per_window = max(1, int(sample_rate * window_sec))
        rms_values = []
        time_windows = []
        idx = 0
        while True:
            frames = wf.readframes(frames_per_window)
            if not frames:
                break
            rms = rms_from_frames(frames, sample_width)
            start = idx * window_sec
            end = start + window_sec
            rms_values.append(rms)
            time_windows.append((start, end))
            idx += 1

    if not rms_values:
        return []
    max_rms = max(rms_values)
    if max_rms < 1:
        return []
    sorted_rms = sorted(rms_values)
    median = sorted_rms[len(sorted_rms) // 2]
    if max_rms / max(median, 1) < 1.1:
        return []
    threshold = max_rms * 0.6

    segments = []
    current = None
    rms_accum = 0.0
    rms_count = 0
    for (start, end), rms in zip(time_windows, rms_values):
        if rms >= threshold:
            if current is None:
                current = {'start': start, 'end': end}
                rms_accum = rms
                rms_count = 1
            elif start - current['end'] <= max_gap:
                current['end'] = end
                rms_accum += rms
                rms_count += 1
            else:
                if current['end'] - current['start'] >= min_duration:
                    avg_rms = rms_accum / max(rms_count, 1)
                    segments.append({
                        'start': current['start'],
                        'end': current['end'],
                        'confidence': min(1.0, avg_rms / max_rms),
                    })
                current = {'start': start, 'end': end}
                rms_accum = rms
                rms_count = 1
        else:
            if current and (start - current['end'] > max_gap):
                if current['end'] - current['start'] >= min_duration:
                    avg_rms = rms_accum / max(rms_count, 1)
                    segments.append({
                        'start': current['start'],
                        'end': current['end'],
                        'confidence': min(1.0, avg_rms / max_rms),
                    })
                current = None
                rms_accum = 0.0
                rms_count = 0
    if current and current['end'] - current['start'] >= min_duration:
        avg_rms = rms_accum / max(rms_count, 1)
        segments.append({
            'start': current['start'],
            'end': current['end'],
            'confidence': min(1.0, avg_rms / max_rms),
        })
    return segments


def apply_padding(segment, pad_before, pad_after):
    start = max(0.0, segment['start'] - pad_before)
    end = segment['end'] + pad_after
    return start, end


def clamp_duration(start, end, min_duration, max_duration=None):
    duration = end - start
    if duration < min_duration:
        end = start + min_duration
    if max_duration and end - start > max_duration:
        end = start + max_duration
    return start, end, end - start


def create_clip(input_video, start, duration, outpath):
    """Create a clip using ffmpeg with a compatible codec baseline."""
    os.makedirs(os.path.dirname(outpath) or '.', exist_ok=True)
    cmd = [
        'ffmpeg',
        '-y',
        '-ss',
        str(start),
        '-i',
        input_video,
        '-t',
        str(duration),
        '-c:v',
        'libx264',
        '-preset',
        'fast',
        '-crf',
        '20',
        '-r',
        '30',
        '-pix_fmt',
        'yuv420p',
        '-c:a',
        'aac',
        '-b:a',
        '192k',
        '-movflags',
        '+faststart',
        outpath,
    ]
    subprocess.run(cmd, check=True)


def generate_clips(
    input_video,
    transcript,
    outdir,
    min_duration=8.0,
    max_duration=None,
    mode='all',
    max_clips=10,
    pad_before=0.0,
    pad_after=0.0,
    diarization_path=None,
    laughter_segments=None,
    report_path=None,
):
    os.makedirs(outdir, exist_ok=True)
    segments = parse_transcript(transcript)
    diarization = load_diarization(diarization_path)
    laughter_segments = laughter_segments or []
    if mode == 'interesting':
        segments = select_interesting_segments(
            segments,
            diarization=diarization,
            laughter_segments=laughter_segments,
            max_clips=max_clips,
        )

    report = {'clips': [], 'mode': mode, 'laughter_segments': laughter_segments}
    i = 1
    for s in segments:
        start, end = apply_padding(s, pad_before, pad_after)
        start, end, duration = clamp_duration(start, end, min_duration, max_duration)
        outpath = os.path.join(outdir, f"clip-{i:03d}.mp4")
        print(f"Exporting {outpath}: start={start} dur={duration}")
        create_clip(input_video, start, duration, outpath)
        report['clips'].append(
            {
                'path': outpath,
                'start': start,
                'end': end,
                'duration': duration,
                'text': s.get('text', ''),
                'score': s.get('score'),
                'reasons': s.get('reasons', []),
            }
        )
        i += 1

    if report_path:
        os.makedirs(os.path.dirname(report_path) or '.', exist_ok=True)
        with open(report_path, 'w') as fh:
            json.dump(report, fh, indent=2)
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--transcript', required=True)
    parser.add_argument('--outdir', required=True)
    parser.add_argument('--min_duration', type=float, default=8.0)
    parser.add_argument('--max_duration', type=float, default=None)
    parser.add_argument('--mode', choices=('all', 'interesting'), default='all')
    parser.add_argument('--max_clips', type=int, default=10)
    parser.add_argument('--pad_before', type=float, default=0.0)
    parser.add_argument('--pad_after', type=float, default=0.0)
    parser.add_argument('--diarization', default=None)
    parser.add_argument('--laughter_detection', action='store_true')
    parser.add_argument('--laughter_audio', default=None)
    parser.add_argument('--report', default=None)
    parser.add_argument('--download_dir', default='downloads')
    parser.add_argument('--format', default='bestvideo[height<=2160]+bestaudio/best')
    args = parser.parse_args()
    input_video = resolve_input(args.input, args.download_dir, args.format)
    laughter_segments = []
    if args.laughter_detection or args.laughter_audio:
        try:
            audio_source = args.laughter_audio or input_video
            wav_path = ensure_wav_audio(audio_source, args.outdir)
            laughter_segments = detect_laughter_segments(wav_path)
        except Exception as exc:
            logger.warning('laughter detection failed: %s', exc)
    generate_clips(
        input_video,
        args.transcript,
        args.outdir,
        min_duration=args.min_duration,
        max_duration=args.max_duration,
        mode=args.mode,
        max_clips=args.max_clips,
        pad_before=args.pad_before,
        pad_after=args.pad_after,
        diarization_path=args.diarization,
        laughter_segments=laughter_segments,
        report_path=args.report,
    )

if __name__ == '__main__':
    main()
