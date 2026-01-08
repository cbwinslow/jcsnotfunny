import pytest
from agents.tasks.github_executor import GitHubProposer

class DummyResponse:
    def __init__(self, status_code=201, json_data=None):
        self.status_code = status_code
        self._json = json_data or {}
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception('http error')
    def json(self):
        return self._json

def test_post_comment(monkeypatch):
    called = {}
    def fake_post(url, json=None, headers=None, timeout=None):
        called['url'] = url
        called['json'] = json
        return DummyResponse(201, {'id': 123})
    monkeypatch.setattr('agents.tasks.github_executor.requests.post', fake_post)

    p = GitHubProposer(owner='cbwinslow', repo='jcsnotfunny', token='fake')
    res = p.post_comment(21, 'hello')
    assert called['url'].endswith('/issues/21/comments')
    assert called['json']['body'] == 'hello'
    assert res['id'] == 123
