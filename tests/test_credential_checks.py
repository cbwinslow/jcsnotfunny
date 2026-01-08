import os

from scripts.credential_checks import audit_credentials


class DummyResponse:
    def __init__(self, status_code=200, payload=None):
        self.status_code = status_code
        self._payload = payload or {}

    def json(self):
        return self._payload


class DummySession:
    def __init__(self, responses):
        self.responses = responses
        self.calls = []

    def get(self, url, **kwargs):
        self.calls.append((url, kwargs))
        return self.responses.get(url, DummyResponse(status_code=404, payload={}))


def test_audit_credentials_offline_missing(monkeypatch):
    monkeypatch.delenv('X_API_KEY', raising=False)
    monkeypatch.delenv('X_API_SECRET', raising=False)
    results = audit_credentials(mode='offline')
    x_result = next(result for result in results if result.category == 'social' and result.name == 'x')
    assert x_result.status == 'missing'
    assert 'X_API_KEY' in x_result.missing


def test_audit_credentials_streaming_ok(monkeypatch):
    monkeypatch.setenv('YOUTUBE_RTMP_URL', 'rtmps://example.com/live')
    monkeypatch.setenv('YOUTUBE_STREAM_KEY', 'abc123')
    results = audit_credentials(mode='offline')
    yt_result = next(result for result in results if result.category == 'streaming' and result.name == 'youtube_live')
    assert yt_result.status == 'ok'


def test_audit_credentials_live_cloudflare(monkeypatch):
    monkeypatch.setenv('CF_IMAGES_API_TOKEN', 'token')
    monkeypatch.setenv('CF_STREAM_API_TOKEN', 'token')
    monkeypatch.setenv('CF_WORKERS_API_TOKEN', 'token')
    monkeypatch.setenv('CF_AI_API_TOKEN', 'token')
    session = DummySession(
        responses={
            'https://api.cloudflare.com/client/v4/user/tokens/verify': DummyResponse(
                status_code=200, payload={'success': True}
            )
        }
    )
    results = audit_credentials(mode='live', session=session)
    cf_result = next(result for result in results if result.category == 'cloudflare' and result.name == 'images_token')
    assert cf_result.status == 'ok'
    assert cf_result.checked is True
