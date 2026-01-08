#!/usr/bin/env python3
"""Simple skeleton to watch a YouTube channel and trigger the shorts pipeline.

This is a scaffold: fill in API keys and concrete implementations.
"""

import os
import time
from typing import Optional

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")  # or read from config
POLL_SECONDS = int(os.getenv("CHANNEL_MONITOR_POLL_SECONDS", 300))


def get_latest_videos(channel_id: str, api_key: Optional[str] = None):
    """Return list of recent video IDs. Implement using YouTube Data API v3."""
    # TODO: implement API calls
    return []


def trigger_shorts_pipeline(video_id: str, dry_run: bool = True):
    """Call the shorts pipeline for a given video ID. Use subprocess or direct import."""
    # TODO: call scripts.youtube_shorts_pipeline.run_pipeline(video_id, dry_run=dry_run)
    print(f"[DRY-RUN={dry_run}] Triggering pipeline for {video_id}")


def main():
    seen = set()
    while True:
        videos = get_latest_videos(CHANNEL_ID, YOUTUBE_API_KEY)
        for v in videos:
            if v not in seen:
                trigger_shorts_pipeline(v, dry_run=True)
                seen.add(v)
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
