import tempfile
import os
import json
from scripts.publish import push_episode_to_website


def test_push_episode_to_website(tmp_path):
    meta = {'title': 'Test', 'slug': 'test-001', 'guest': 'Jared'}
    content_dir = str(tmp_path / "episodes")
    target = push_episode_to_website(meta, content_dir)
    assert os.path.exists(target)
    with open(target, 'r') as fh:
        data = json.load(fh)
    assert data['title'] == 'Test'
