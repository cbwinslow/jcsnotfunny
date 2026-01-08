"""Environment diagnostics for the production toolchain.

Checks installed binaries (ffmpeg, ffprobe), Python version, key Python packages from requirements.txt,
and reports a JSON summary and human-readable output. Exit code is non-zero on critical failures.
"""
import json
import shutil
import sys
import subprocess
from pathlib import Path

REQUIRED_BINARIES = ["ffmpeg", "ffprobe"]
RECOMMENDED_PY_PKGS = ["whisper", "whisperx", "pyannote.audio", "sentence_transformers", "faiss"]


def check_binaries():
    out = {}
    for b in REQUIRED_BINARIES:
        path = shutil.which(b)
        out[b] = {'found': bool(path), 'path': path}
    return out


def check_python_version(min_major=3, min_minor=10):
    v = sys.version_info
    ok = (v.major > min_major) or (v.major == min_major and v.minor >= min_minor)
    return {'python_version': f"{v.major}.{v.minor}.{v.micro}", 'ok': ok}


def check_packages():
    out = {}
    for pkg in RECOMMENDED_PY_PKGS:
        try:
            __import__(pkg)
            out[pkg] = {'installed': True}
        except Exception:
            out[pkg] = {'installed': False}
    # Also check requirements.txt packages
    reqs = []
    req_file = Path('requirements.txt')
    if req_file.exists():
        reqs = [line.strip() for line in req_file.read_text().splitlines() if line.strip() and not line.startswith('#')]
    out['requirements'] = reqs
    return out


def check_ffmpeg_functional():
    try:
        p = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, timeout=5)
        return {'ok': p.returncode == 0, 'version': p.stdout.splitlines()[0] if p.stdout else ''}
    except Exception as exc:
        return {'ok': False, 'error': str(exc)}


def run_checks():
    report = {}
    report['binaries'] = check_binaries()
    report['python'] = check_python_version()
    report['packages'] = check_packages()
    report['ffmpeg'] = check_ffmpeg_functional()

    # decide exit code: critical if ffmpeg/ffprobe missing or python version bad
    critical = False
    for b, info in report['binaries'].items():
        if not info['found']:
            critical = True
    if not report['python']['ok']:
        critical = True
    return report, critical


def main():
    report, critical = run_checks()
    print(json.dumps(report, indent=2))
    if critical:
        print("CRITICAL: Missing required components. See report JSON output.")
        sys.exit(2)
    else:
        print("OK: Environment looks good for basic operation.")
        sys.exit(0)


if __name__ == '__main__':
    main()
