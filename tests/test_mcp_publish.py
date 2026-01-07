import json
import tempfile
from scripts.mcp_publish import publish_via_api, publish_via_mcp


def test_publish_via_api_ok():
    md = {'title': 'Ep X', 'guest': 'Jared', 'ep_link': 'https://youtu.be/VID'}
    res = publish_via_api(['x'], md)
    assert 'x' in res and 'rendered' in res['x']


class DummyResponse:
    def __init__(self, json_data):
        self._json = json_data
        self.status_code = 200
    def json(self):
        return self._json
    def raise_for_status(self):
        return None


def test_publish_via_mcp(monkeypatch):
    def fake_post(url, json=None, headers=None, timeout=None):
        return DummyResponse({'ok': True, 'sent': json})
    monkeypatch.setattr('requests.post', fake_post)
    md = {'title': 'Ep X', 'guest': 'Jared', 'ep_link': 'https://youtu.be/VID'}
    out = publish_via_mcp('https://mcp.example/publish', 'APIKEY', ['x','instagram'], md)
    assert out.get('ok') is True
    assert 'sent' in out
