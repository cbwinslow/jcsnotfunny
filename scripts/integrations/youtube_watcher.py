"""YouTube watcher utility.

Polls a YouTube channel for recent uploads (using API key by default), tracks seen
video IDs in a small state file, and invokes a callback for newly discovered videos.

Design goals:
- Lightweight and testable (requests-based, easy to mock)
- Supports dry-run mode (doesn't persist state)
- Minimal dependencies
"""
from __future__ import annotations

import json
import logging
import os
import time
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional

import requests

logger = logging.getLogger("youtube_watcher")
logging.basicConfig(level=logging.INFO)

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"


class YouTubeWatcher:
    def __init__(
        self,
        api_key: Optional[str] = None,
        channel_id: Optional[str] = None,
        state_file: str | Path = ".youtube_watcher_state.json",
    ) -> None:
        self.api_key = api_key or os.environ.get("YT_API_KEY") or os.environ.get("YOUTUBE_API_KEY")
        self.channel_id = channel_id or os.environ.get("YT_CHANNEL_ID") or os.environ.get("YOUTUBE_CHANNEL_ID")
        self.state_file = Path(state_file)
        self._seen: set[str] = set()
        self._load_state()

    def _load_state(self) -> None:
        if self.state_file.exists():
            try:
                data = json.loads(self.state_file.read_text())
                self._seen = set(data.get("seen", []))
            except Exception:
                logger.warning("Failed to read state file; starting fresh")
                self._seen = set()
        else:
            self._seen = set()

    def _save_state(self) -> None:
        try:
            self.state_file.write_text(json.dumps({"seen": list(self._seen)}))
        except Exception:
            logger.exception("Failed to write watcher state file")

    def get_latest_videos(self, max_results: int = 5) -> List[Dict]:
        """Return the latest uploads from the channel as a list of items with keys:
        'video_id', 'title', 'published_at'.
        Raises RuntimeError on API failure.
        """
        if not self.api_key:
            raise RuntimeError("No YouTube API key configured (YT_API_KEY)")
        if not self.channel_id:
            raise RuntimeError("No channel id configured (YT_CHANNEL_ID)")

        params = {
            "part": "snippet",
            "channelId": self.channel_id,
            "order": "date",
            "maxResults": int(max_results),
            "type": "video",
            "key": self.api_key,
        }

        resp = requests.get(YOUTUBE_SEARCH_URL, params=params, timeout=10)
        if resp.status_code != 200:
            logger.error("YouTube API error: %s %s", resp.status_code, resp.text)
            raise RuntimeError(f"YouTube API returned status {resp.status_code}")

        data = resp.json()
        items = []
        for it in data.get("items", []):
            snippet = it.get("snippet", {})
            vid = it.get("id", {}).get("videoId")
            if not vid:
                continue
            items.append({
                "video_id": vid,
                "title": snippet.get("title"),
                "published_at": snippet.get("publishedAt"),
            })

        return items

    def run_once(
        self,
        callback: Optional[Callable[[Dict], None]] = None,
        dry_run: bool = True,
        max_results: int = 5,
    ) -> List[Dict]:
        """Check for new videos and call the callback for each new one.

        Returns the list of newly discovered items.
        """
        callback = callback or (lambda item: logger.info("New video: %s", item))

        latest = self.get_latest_videos(max_results=max_results)
        new = [it for it in latest if it["video_id"] not in self._seen]

        for it in new:
            try:
                callback(it)
            except Exception:
                logger.exception("Watcher callback failed for %s", it)

        if not dry_run and new:
            for it in new:
                self._seen.add(it["video_id"])
            self._save_state()

        return new


def _cli_main():
    import argparse

    p = argparse.ArgumentParser(description="YouTube channel watcher (polling)")
    p.add_argument("--api-key", help="YouTube API key")
    p.add_argument("--channel-id", help="YouTube Channel ID")
    p.add_argument("--state-file", default=".youtube_watcher_state.json")
    p.add_argument("--interval", type=int, default=0, help="Run in a loop every N seconds (0 = run once)")
    p.add_argument("--dry-run", action="store_true", default=False, help="Do not persist state; just print new items")
    p.add_argument("--max-results", type=int, default=5)
    args = p.parse_args()

    watcher = YouTubeWatcher(api_key=args.api_key, channel_id=args.channel_id, state_file=args.state_file)

    def cb(item: Dict) -> None:
        print("New video detected:")
        print(json.dumps(item, indent=2))
        # Example: shell out to `gh workflow run transcribe-integration.yml -f video_id=<id>`

    if args.interval <= 0:
        watcher.run_once(callback=cb, dry_run=args.dry_run, max_results=args.max_results)
        return

    try:
        while True:
            watcher.run_once(callback=cb, dry_run=args.dry_run, max_results=args.max_results)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        logger.info("Watcher stopped by user")


if __name__ == "__main__":
    _cli_main()
