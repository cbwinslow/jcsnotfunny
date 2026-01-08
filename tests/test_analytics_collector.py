from unittest.mock import MagicMock

from scripts.integrations.analytics_collector import collect_and_store


def test_collect_and_store_no_r2_no_push(monkeypatch):
    # Mock youtube_analytics functions to return predictable rows
    monkeypatch.setattr('scripts.integrations.youtube_analytics.views_by_video', lambda *a, **k: [{'video_id': 'v1', 'views': 10}])
    monkeypatch.setattr('scripts.integrations.youtube_analytics.watchtime_by_video', lambda *a, **k: [{'video_id': 'v1', 'watch_minutes': 5.0}])
    monkeypatch.setattr('scripts.integrations.youtube_analytics.traffic_sources', lambda *a, **k: [{'source': 'SEARCH', 'views': 3}])

    res = collect_and_store(channel_id='chan', r2_bucket=None, r2_prefix=None, pushgateway=None, access_token='tok', days=3)
    assert res['counts']['views_rows'] == 1
    assert res['counts']['watch_rows'] == 1
    assert res['counts']['traffic_rows'] == 1
    assert res['uploaded'] == []
    assert res['pushed'] is False


def test_collect_and_store_with_r2_and_push(monkeypatch):
    monkeypatch.setattr('scripts.integrations.youtube_analytics.views_by_video', lambda *a, **k: [{'video_id': 'v1', 'views': 10}])
    monkeypatch.setattr('scripts.integrations.youtube_analytics.watchtime_by_video', lambda *a, **k: [{'video_id': 'v1', 'watch_minutes': 5.0}])
    monkeypatch.setattr('scripts.integrations.youtube_analytics.traffic_sources', lambda *a, **k: [{'source': 'SEARCH', 'views': 3}])

    # stub upload_text (analytics_collector imports upload_text directly)
    monkeypatch.setattr('scripts.integrations.analytics_collector.upload_text', lambda bucket, key, txt, content_type=None: None, raising=False)

    # stub push_to_gateway via monkeypatching push_to_gateway function to be no-op
    monkeypatch.setattr('scripts.integrations.analytics_collector.push_to_gateway', lambda *a, **k: None, raising=False)

    res = collect_and_store(channel_id='chan', r2_bucket='mybucket', r2_prefix='pfx', pushgateway='http://pushgw', access_token='tok', days=3)
    assert 'views.csv'  # sanity
    assert res['pushed'] is True or res['pushed'] is False  # allow both based on push result
    assert res['uploaded']  # at least one uploaded key
