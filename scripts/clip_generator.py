"""Clip generation agent (stub)

Takes a multimedia file + transcript (WebVTT or JSON) and generates short
clips based on timestamps, keywords, or silence detection.

Usage:
  python scripts/clip_generator.py --input episode.mp4 --transcript episode.vtt --outdir clips/

This stub uses ffmpeg (must be installed and available on PATH).
"""
import argparse
import os
import re
import subprocess
import logging

logger = logging.getLogger('clip_generator')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(ch)


def parse_vtt(vtt_path):
    """Parse a VTT file and return list of segments with start,end,text."""
    segments = []
    with open(vtt_path, 'r') as fh:
        content = fh.read()
    blocks = re.split(r"\n\n+", content.strip())
    for b in blocks:
        if '-->' in b:
            lines = b.splitlines()
            times = lines[0]
            text = ' '.join(lines[1:]).strip()
            start, arrow, end = times.partition('-->')
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


def create_clip(input_video, start, duration, outpath):
    """Create a clip using ffmpeg. Tries stream copy; falls back to re-encode on failure."""
    os.makedirs(os.path.dirname(outpath) or '.', exist_ok=True)
    cmd = ['ffmpeg', '-y', '-ss', str(start), '-i', input_video, '-t', str(duration), '-c', 'copy', outpath]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        logger.warning('stream copy failed, trying re-encode for %s', outpath)
        cmd = ['ffmpeg', '-y', '-ss', str(start), '-i', input_video, '-t', str(duration), '-c:v', 'libx264', '-c:a', 'aac', outpath]
        subprocess.run(cmd, check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--transcript', required=True)
    parser.add_argument('--outdir', required=True)
    parser.add_argument('--min_duration', type=float, default=8.0)
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    segments = parse_vtt(args.transcript)
    # Create a clip for each segment longer than min_duration, or extend small segments
    i = 1
    for s in segments:
        duration = s['end'] - s['start']
        if duration < args.min_duration:
            # extend to min_duration when possible
            duration = args.min_duration
        outpath = os.path.join(args.outdir, f"clip-{i:03d}.mp4")
        print(f"Exporting {outpath}: start={s['start']} dur={duration}")
        create_clip(args.input, s['start'], duration, outpath)
        i += 1

if __name__ == '__main__':
    main()
