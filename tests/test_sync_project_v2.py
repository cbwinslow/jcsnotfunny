import json
import pytest

from scripts import sync_project_v2 as sp


class DummyResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


def test_run_graphql_query(monkeypatch, tmp_path):
    sample_payload = {
        'data': {
            'repository': {
                'projectV2': {
                    'items': {
                        'pageInfo': {'hasNextPage': False, 'endCursor': None},
                        'nodes': [
                            {
                                'content': {
                                    '__typename': 'Issue',
                                    'number': 123,
                                    'title': 'Test Issue',
                                    'body': 'Issue body'
                                }
                            },
                            {
                                'content': {
                                    '__typename': 'DraftIssue',
                                    'title': 'Draft Title',
                                    'body': 'Draft body'
                                }
                            }
                        ]
                    }
                }
            }
        }
    }

    def fake_post(url, json, headers):
        return DummyResponse(sample_payload)

    monkeypatch.setattr('scripts.sync_project_v2.requests.post', fake_post)

    token = 'fake'
    created = sp.sync_project_items(token, 'owner', 'repo', 20)

    assert created == 2
    # Check that files were created in .github/issues
    assert (sp.ISSUES_DIR).exists()
    files = list(sp.ISSUES_DIR.glob('*.md'))
    assert len(files) >= 2
