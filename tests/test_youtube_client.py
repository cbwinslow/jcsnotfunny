import pytest

from scripts.providers.youtube_client import YouTubeClient


def test_refresh_access_token_missing_credentials(monkeypatch):
    # ensure env vars are not present
    monkeypatch.delenv('YT_CLIENT_ID', raising=False)
    monkeypatch.delenv('YT_CLIENT_SECRET', raising=False)
    monkeypatch.delenv('YT_REFRESH_TOKEN', raising=False)

    client = YouTubeClient()
    with pytest.raises(RuntimeError):
        client.refresh_access_token()


def test_refresh_access_token_success(monkeypatch):
    client = YouTubeClient(client_id='cid', client_secret='csecret', refresh_token='rtok')

    class DummyResp:
        def raise_for_status(self):
            pass

        def json(self):
            return {'access_token': 'abc', 'expires_in': 3600}

    def fake_post(url, data, timeout):
        assert url == 'https://oauth2.googleapis.com/token'
        assert data['grant_type'] == 'refresh_token'
        return DummyResp()

    monkeypatch.setattr('scripts.providers.youtube_client.requests.post', fake_post)

    out = client.refresh_access_token()
    assert out['access_token'] == 'abc'


def test_upload_short_calls_refresh(monkeypatch, tmp_path):
    client = YouTubeClient(client_id='cid', client_secret='csecret', refresh_token='rtok')
    called = {}

    def fake_refresh():
        called['done'] = True
        return {'access_token': 'abc'}

    monkeypatch.setattr(client, 'refresh_access_token', fake_refresh)

    # create a dummy file so MediaFileUpload won't fail if used
    f = tmp_path / "video.mp4"
    f.write_bytes(b"dummy")

    # stub out googleapiclient build and MediaFileUpload to avoid touching network/files
    class DummyReq:
        def __init__(self, result):
            self._result = result

        def execute(self):
            return self._result

    class DummyVideos:
        def __init__(self, result):
            self._result = result

        def insert(self, part, body, media_body):
            return DummyReq(self._result)

    class DummyYouTube:
        def __init__(self, result):
            self._videos = DummyVideos(result)

        def videos(self):
            return self._videos

    def fake_build(service, version, credentials=None):
        return DummyYouTube({'id': 'ABC'})

    monkeypatch.setattr('googleapiclient.discovery.build', fake_build)
    monkeypatch.setattr('googleapiclient.http.MediaFileUpload', lambda *a, **k: object())

    resp = client.upload_short(str(f), 'title', 'desc')

    assert called.get('done') is True
    assert resp['id'] == 'ABC'
