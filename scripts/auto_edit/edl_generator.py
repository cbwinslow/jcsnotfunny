#!/usr/bin/env python3
"""EDL Generator (Auto-Edit PoC)

Selects candidate short clips from transcript segments and outputs a simple
EDL (Edit Decision List) JSON that other tools can consume to generate clips.

Design goals:
- Deterministic and testable logic based on `funny_score` (or heuristics)
- Respects min/max clip duration and avoids overlapping clips
- Simple CLI for offline use (accepts JSON input of segments)
"""
from __future__ import annotations

import json
from typing import List, Dict, Any, Optional
import argparse
import os


def _get_time_keys(seg: Dict[str, Any]) -> (float, float):
    """Normalize segment dict to (start, end). Accepts different key names."""
    if "start" in seg and "end" in seg:
        return float(seg["start"]), float(seg["end"])
    if "start_time" in seg and "end_time" in seg:
        return float(seg["start_time"]), float(seg["end_time"])
    # fallback: use 0/10
    return float(seg.get("start", 0.0)), float(seg.get("end", seg.get("start", 0) + 10.0))


def select_candidate_clips(
    segments: List[Dict[str, Any]],
    min_duration: float = 5.0,
    max_duration: float = 30.0,
    max_clips: int = 5,
    min_funny_score: float = 0.5,
) -> List[Dict[str, Any]]:
    """Select a ranked list of candidate clips from transcript segments.

    Arguments:
        segments: list of transcript segments (each must include text and optional funny_score)
        min_duration: minimum clip length
        max_duration: maximum clip length
        max_clips: maximum number of clips to return
        min_funny_score: minimum funny score to consider a segment

    Returns:
        List of clip dicts: {clip_id, start, end, duration, text, funny_score}
    """

    cleaned = []
    for seg in segments:
        start, end = _get_time_keys(seg)
        duration = max(0.0, end - start)
        score = float(seg.get("funny_score", 0.0))
        text = seg.get("text") or seg.get("transcript_text") or ""

        # If there's no score but the text contains laughter markers, bump score
        if score == 0.0 and any(k in text.lower() for k in ("lol", "lmao", "haha", "ha ", "hehe")):
            score = 0.6

        cleaned.append({"start": start, "end": end, "duration": duration, "text": text, "funny_score": score})

    # Filter by score and basic duration
    candidates = [c for c in cleaned if c["funny_score"] >= min_funny_score]

    # Expand or shrink segments to meet min/max duration
    for c in candidates:
        if c["duration"] < min_duration:
            c["end"] = c["start"] + min_duration
            c["duration"] = c["end"] - c["start"]
        if c["duration"] > max_duration:
            c["end"] = c["start"] + max_duration
            c["duration"] = c["end"] - c["start"]

    # Sort by funny_score desc, then by duration (shorter preferred)
    candidates.sort(key=lambda x: (-x["funny_score"], x["duration"]))

    # Enforce non-overlap: pick top candidates while skipping overlaps
    selected: List[Dict[str, Any]] = []

    def overlaps(a_start: float, a_end: float, b_start: float, b_end: float) -> bool:
        return not (a_end <= b_start or b_end <= a_start)

    for candidate in candidates:
        s, e = candidate["start"], candidate["end"]
        conflict = False
        for sel in selected:
            if overlaps(s, e, sel["start"], sel["end"]):
                conflict = True
                break
        if not conflict:
            selected.append(candidate)
        if len(selected) >= max_clips:
            break

    # Assign clip IDs and return
    for idx, clip in enumerate(selected, start=1):
        clip["clip_id"] = idx

    return selected


def write_edl(clips: List[Dict[str, Any]], output_path: str) -> None:
    """Write a simple EDL JSON file containing the selected clips."""
    data = {"clips": clips, "count": len(clips)}
    with open(output_path, "w") as fh:
        json.dump(data, fh, indent=2)


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="EDL generator (Auto-Edit PoC)")
    parser.add_argument("--input-json", required=True, help="Input JSON with segments (list) or transcript")
    parser.add_argument("--output-edl", required=True, help="Output EDL JSON path")
    parser.add_argument("--min-duration", type=float, default=5.0)
    parser.add_argument("--max-duration", type=float, default=30.0)
    parser.add_argument("--max-clips", type=int, default=5)
    parser.add_argument("--min-funny-score", type=float, default=0.5)

    args = parser.parse_args(argv)

    if not os.path.exists(args.input_json):
        raise FileNotFoundError(args.input_json)

    with open(args.input_json, "r") as fh:
        segments = json.load(fh)

    if isinstance(segments, dict) and "segments" in segments:
        segments = segments["segments"]

    clips = select_candidate_clips(
        segments,
        min_duration=args.min_duration,
        max_duration=args.max_duration,
        max_clips=args.max_clips,
        min_funny_score=args.min_funny_score,
    )

    write_edl(clips, args.output_edl)
    print(f"Wrote {len(clips)} clips to {args.output_edl}")


if __name__ == "__main__":
    main()
