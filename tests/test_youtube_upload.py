import pytest

from scripts.providers.youtube_client import YouTubeClient


class DummyRequest:
    def __init__(self, result):
        self._result = result

    def execute(self):
        return self._result


class DummyVideos:
    def __init__(self, result):
        self._result = result

    def insert(self, part, body, media_body):
        assert part == 'snippet,status'
        assert 'snippet' in body
        return DummyRequest(self._result)


class DummyYouTube:
    def __init__(self, result):
        self._videos = DummyVideos(result)

    def videos(self):
        return self._videos


def test_upload_short_uses_google_api_and_returns_url(monkeypatch, tmp_path):
    client = YouTubeClient(client_id='cid', client_secret='csecret', refresh_token='rtok')
    # ensure refresh is called
    called = {}

    def fake_refresh():
        called['done'] = True
        return {'access_token': 'abc'}

    monkeypatch.setattr(client, 'refresh_access_token', fake_refresh)

    # create a dummy file
    f = tmp_path / "video.mp4"
    f.write_bytes(b"dummy")

    # fake build to return our DummyYouTube
    def fake_build(service, version, credentials=None):
        assert service == 'youtube'
        return DummyYouTube({'id': 'XYZ'})

    # patch the googleapiclient.discovery.build function that upload_short imports
    monkeypatch.setattr('googleapiclient.discovery.build', fake_build)

    class DummyMedia:
        pass

    monkeypatch.setattr('googleapiclient.http.MediaFileUpload', lambda p, chunksize, resumable, mimetype: DummyMedia())

    out = client.upload_short(str(f), 't', 'd', tags=['a'])
    assert called.get('done') is True
    assert out['id'] == 'XYZ'
    assert out['url'] == 'https://youtu.be/XYZ'


def test_upload_short_falls_back_when_google_not_installed(monkeypatch, tmp_path):
    client = YouTubeClient(client_id='cid', client_secret='csecret', refresh_token='rtok')

    def fake_refresh():
        return {'access_token': 'abc'}

    monkeypatch.setattr(client, 'refresh_access_token', fake_refresh)

    f = tmp_path / "video.mp4"
    f.write_bytes(b"dummy")

    # Make import fail by ensuring the attribute lookup raises
    monkeypatch.setitem(__import__('sys').modules, 'googleapiclient.discovery', None)

    out = client.upload_short(str(f), 't', 'd')
    assert out['id'].startswith('YT_SHORT_')
    assert out['url'].startswith('https://youtu.be/')
