#!/usr/bin/env python3
"""Simple download video tool (skeleton).
Attempts to use yt-dlp if available; otherwise creates an empty placeholder file.
"""
import logging
import shlex
import subprocess
from pathlib import Path

logger = logging.getLogger("download_video")


def download_video(url: str, output_dir: str) -> dict:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    # derive filename
    safe_name = url.replace("/", "_").replace(":", "_")[:120]
    out_path = Path(output_dir) / f"{safe_name}.mp4"

    # Try to use Python yt-dlp if available
    try:
        import yt_dlp as ytdl

        ydl_opts = {"outtmpl": str(out_path)}
        with ytdl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        logger.info(f"Downloaded video to {out_path} using yt_dlp Python module")
    except Exception:
        # Try external binary
        try:
            subprocess.run(["yt-dlp", "-o", str(out_path), url], check=True)
            logger.info(f"Downloaded video to {out_path} using yt-dlp binary")
        except Exception:
            # fallback: create an empty file as placeholder
            out_path.write_bytes(b"")
            logger.warning("yt-dlp not available or failed; created placeholder file")

    # Return metadata (filesize and path). Try to get duration with ffprobe if available
    filesize = out_path.stat().st_size if out_path.exists() else 0

    # Attempt to read duration using ffprobe if available
    duration = None
    try:
        import json
        import subprocess

        cmd = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            str(out_path),
        ]
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        j = json.loads(out)
        duration = float(j.get("format", {}).get("duration")) if j.get("format") else None
    except Exception:
        duration = None

    return {"video_path": str(out_path), "filesize": filesize, "duration": duration}
