import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

from scripts.integrations.youtube_watcher import YouTubeWatcher


SAMPLE_RESPONSE = {
    "items": [
        {
            "id": {"videoId": "vid_1"},
            "snippet": {"title": "Episode 1", "publishedAt": "2026-01-01T00:00:00Z"}
        },
        {
            "id": {"videoId": "vid_2"},
            "snippet": {"title": "Episode 2", "publishedAt": "2026-01-02T00:00:00Z"}
        }
    ]
}


def test_get_latest_videos_success(monkeypatch):
    def fake_get(url, params=None, timeout=None):
        m = MagicMock()
        m.status_code = 200
        m.json.return_value = SAMPLE_RESPONSE
        return m

    monkeypatch.setattr('requests.get', fake_get)

    w = YouTubeWatcher(api_key="key", channel_id="chan")
    items = w.get_latest_videos()
    assert len(items) == 2
    assert items[0]["video_id"] == "vid_1"


def test_run_once_detects_new_and_persists(tmp_path, monkeypatch):
    def fake_get(url, params=None, timeout=None):
        m = MagicMock()
        m.status_code = 200
        m.json.return_value = SAMPLE_RESPONSE
        return m

    monkeypatch.setattr('requests.get', fake_get)

    state_file = tmp_path / "state.json"
    w = YouTubeWatcher(api_key="k", channel_id="c", state_file=state_file)

    called = []

    def cb(item):
        called.append(item['video_id'])

    new = w.run_once(callback=cb, dry_run=False)
    assert set(called) == {"vid_1", "vid_2"}
    assert len(new) == 2

    # second run should find no new videos
    called.clear()
    new = w.run_once(callback=cb, dry_run=False)
    assert called == []
    assert new == []


def test_api_error_raises(monkeypatch):
    def bad_get(url, params=None, timeout=None):
        m = MagicMock()
        m.status_code = 403
        m.text = "error"
        return m

    monkeypatch.setattr('requests.get', bad_get)

    w = YouTubeWatcher(api_key="k", channel_id="c")
    try:
        w.get_latest_videos()
        assert False, "expected RuntimeError"
    except RuntimeError:
        pass
