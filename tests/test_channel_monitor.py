import json
from types import SimpleNamespace

import pytest

from scripts.automation.channel_monitor import get_latest_videos, trigger_shorts_pipeline


def test_get_latest_videos_parses_ids(monkeypatch):
    fake_response = {"items": [{"id": {"videoId": "abc123"}}, {"id": {"videoId": "def456"}}]}

    class FakeResp:
        def __init__(self, j):
            self._j = j

        def raise_for_status(self):
            return None

        def json(self):
            return self._j

    def fake_get(url, params=None, timeout=None):
        assert params is not None
        assert params.get("channelId") == "UC123"
        return FakeResp(fake_response)

    monkeypatch.setattr("requests.get", fake_get)

    ids = get_latest_videos("UC123", api_key="dummy", max_results=2)
    assert ids == ["abc123", "def456"]


def test_trigger_shorts_pipeline_calls_pipeline(monkeypatch, tmp_path):
    # Replace the real pipeline with a fake that records calls
    class FakePipeline:
        last_instance = None

        def __init__(self):
            FakePipeline.last_instance = self
            self.called = False

        def run_pipeline(self, youtube_url, output_dir: str = "out", dry_run: bool = True, **kwargs):
            self.called = True
            self.youtube_url = youtube_url
            self.output_dir = output_dir
            self.dry_run = dry_run
            return {"status": "ok"}

    monkeypatch.setattr("scripts.youtube_shorts_pipeline.YouTubeShortsPipeline", FakePipeline)

    trigger_shorts_pipeline("abc123", dry_run=True)

    assert FakePipeline.last_instance is not None
    assert FakePipeline.last_instance.called is True
    assert "abc123" in FakePipeline.last_instance.youtube_url
    assert FakePipeline.last_instance.dry_run is True
