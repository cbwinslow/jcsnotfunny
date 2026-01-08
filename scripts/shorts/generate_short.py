#!/usr/bin/env python3
"""Shorts generator (dry-run friendly)

Generates trimmed clips from a source video and a provided EDL.
In dry-run mode it creates placeholder files so tests can run without ffmpeg.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import argparse


def generate_clips_from_edl(source_video: str, edl: List[Dict[str, Any]], output_dir: str, dry_run: bool = True) -> List[str]:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    outputs: List[str] = []

    for clip in edl:
        clip_id = clip.get("clip_id") or edl.index(clip) + 1
        start = clip.get("start")
        end = clip.get("end")
        out_name = Path(output_dir) / f"short_{clip_id:03d}.mp4"

        if dry_run:
            # Create a tiny placeholder file to simulate output
            try:
                with open(out_name, "wb") as fh:
                    fh.write(b"SHORTPLACEHOLDER")
            except Exception:
                pass
        else:
            # Real ffmpeg invocation (left as a simple template)
            cmd = [
                "ffmpeg",
                "-y",
                "-ss",
                str(start),
                "-i",
                source_video,
                "-to",
                str(end),
                "-c",
                "copy",
                str(out_name),
            ]
            os.system(" ".join(cmd))

        outputs.append(str(out_name))

    return outputs


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Generate shorts from EDL")
    parser.add_argument("--source", required=True)
    parser.add_argument("--edl", required=True, help="Path to EDL JSON produced by edl_generator")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args(argv)

    with open(args.edl, "r") as fh:
        data = json.load(fh)

    clips = data.get("clips", [])
    outs = generate_clips_from_edl(args.source, clips, args.output_dir, dry_run=args.dry_run)
    print(f"Generated {len(outs)} clips -> {args.output_dir}")


if __name__ == "__main__":
    main()
