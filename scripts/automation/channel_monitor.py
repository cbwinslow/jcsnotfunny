#!/usr/bin/env python3
"""Simple skeleton to watch a YouTube channel and trigger the shorts pipeline.

This is a scaffold: fill in API keys and concrete implementations.
"""

import os
import time
import argparse
import requests
from typing import Optional, List

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")  # or read from config
POLL_SECONDS = int(os.getenv("CHANNEL_MONITOR_POLL_SECONDS", 300))


def get_latest_videos(channel_id: str, api_key: Optional[str] = None, max_results: int = 5) -> List[str]:
    """Return list of recent video IDs using YouTube Data API v3.

    Raises RuntimeError if API key is not available.
    """
    api_key = api_key or os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise RuntimeError("YOUTUBE_API_KEY is required to query the YouTube Data API")

    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "channelId": channel_id,
        "order": "date",
        "type": "video",
        "maxResults": max_results,
        "key": api_key
    }

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    video_ids: List[str] = []
    for item in data.get("items", []):
        vid = item.get("id", {}).get("videoId")
        if vid:
            video_ids.append(vid)

    return video_ids


def trigger_shorts_pipeline(video_id: str, dry_run: bool = True):
    """Call the shorts pipeline for a given video ID using the pipeline class."""
    try:
        from scripts.youtube_shorts_pipeline import YouTubeShortsPipeline

        pipeline = YouTubeShortsPipeline()
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        output_dir = f"youtube_shorts_{video_id}"
        # Keep dry_run default True to avoid heavy ffmpeg in tests/CI
        pipeline.run_pipeline(youtube_url, output_dir=output_dir, dry_run=dry_run)
    except Exception as e:
        print(f"[DRY-RUN={dry_run}] Failed to trigger pipeline for {video_id}: {e}")


def main(poll_seconds: int = POLL_SECONDS, channel_id: Optional[str] = None, once: bool = False, dry_run: bool = True):
    seen = set()
    cid = channel_id or CHANNEL_ID
    if not cid:
        raise RuntimeError("CHANNEL_ID must be provided via env or --channel-id")

    while True:
        videos = get_latest_videos(cid, api_key=os.getenv("YOUTUBE_API_KEY"))
        for v in videos:
            if v not in seen:
                trigger_shorts_pipeline(v, dry_run=dry_run)
                seen.add(v)
        if once:
            break
        time.sleep(poll_seconds)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Watch a YouTube channel and trigger the Shorts pipeline")
    parser.add_argument("--channel-id", help="YouTube channel ID to watch")
    parser.add_argument("--poll-seconds", type=int, default=POLL_SECONDS)
    parser.add_argument("--once", action="store_true", help="Run one iteration and exit")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Run in dry-run mode (default)")

    args = parser.parse_args()
    main(poll_seconds=args.poll_seconds, channel_id=args.channel_id, once=args.once, dry_run=args.dry_run)
