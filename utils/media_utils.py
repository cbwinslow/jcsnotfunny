"""Media utility helpers

Functions for checksums, ffprobe metadata, and preliminary loudness checks.
"""
import hashlib
import subprocess
import json
import os


def checksum(path, algo='sha256'):
    h = hashlib.new(algo)
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def ffprobe_metadata(path):
    cmd = ['ffprobe','-v','quiet','-print_format','json','-show_format','-show_streams', path]
    out = subprocess.run(cmd, capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError('ffprobe failed')
    return json.loads(out.stdout)


def measure_loudness(path, sample_limit=None):
    """Return a mocked loudness measurement or call ffmpeg ebur128 for real checks.

    For now, this will attempt ffmpeg and parse integrated loudness if present.
    """
    cmd = ['ffmpeg','-hide_banner','-nostats','-i', path, '-filter_complex', 'ebur128=framelog=verbose', '-f', 'null', '-']
    out = subprocess.run(cmd, capture_output=True, text=True)
    stderr = out.stderr or ''
    # look for 'Integrated loudness: -14.0 LUFS' sample
    for line in stderr.splitlines():
        if 'Integrated loudness' in line:
            parts = line.split(':')
            try:
                val = float(parts[-1].strip().split()[0])
                return {'integrated_loudness': val}
            except Exception:
                pass
    return {'integrated_loudness': None}
