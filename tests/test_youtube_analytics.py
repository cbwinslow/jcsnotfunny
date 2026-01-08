from unittest.mock import MagicMock

import pytest

from scripts.integrations.youtube_analytics import (
    fetch_report,
    parse_simple_rows,
    views_by_video,
    watchtime_by_video,
    traffic_sources,
    YouTubeAnalyticsError,
)


SAMPLE_REPORT = {
    'columnHeaders': [
        {'name': 'video', 'columnType': 'DIMENSION'},
        {'name': 'views', 'columnType': 'METRIC'}
    ],
    'rows': [
        ['vid_1', '100'],
        ['vid_2', '50']
    ]
}


def fake_fetcher(url, params=None, headers=None):
    return SAMPLE_REPORT


def test_parse_rows():
    rows = parse_simple_rows(SAMPLE_REPORT)
    assert len(rows) == 2
    assert rows[0].dimensions['video'] == 'vid_1'
    assert rows[0].metric_values['views'] == '100'


def test_views_by_video():
    res = views_by_video('2026-01-01', '2026-01-05', channel_id='chan', access_token='tok', fetcher=fake_fetcher)
    assert res[0]['video_id'] == 'vid_1'
    assert res[0]['views'] == 100


def test_watchtime_by_video():
    rep = {
        'columnHeaders': [
            {'name': 'video', 'columnType': 'DIMENSION'},
            {'name': 'estimatedMinutesWatched', 'columnType': 'METRIC'}
        ],
        'rows': [['vid_1', '123.4']]
    }

    def f(url, params=None, headers=None):
        return rep

    res = watchtime_by_video('2026-01-01', '2026-01-05', channel_id='chan', access_token='tok', fetcher=f)
    assert res[0]['video_id'] == 'vid_1'
    assert abs(res[0]['watch_minutes'] - 123.4) < 0.001


def test_traffic_sources():
    rep = {
        'columnHeaders': [
            {'name': 'insightTrafficSourceType', 'columnType': 'DIMENSION'},
            {'name': 'views', 'columnType': 'METRIC'}
        ],
        'rows': [['RELATED_VIDEO', '200'], ['SEARCH', '150']]
    }

    def f(url, params=None, headers=None):
        return rep

    res = traffic_sources('2026-01-01', '2026-01-05', channel_id='chan', access_token='tok', fetcher=f)
    assert res[0]['source'] == 'RELATED_VIDEO'
    assert res[0]['views'] == 200


def test_fetch_report_requires_channel():
    with pytest.raises(YouTubeAnalyticsError):
        fetch_report('2026-01-01', '2026-01-02', metrics='views', channel_id=None, access_token='tok')
