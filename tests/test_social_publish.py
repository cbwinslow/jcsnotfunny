import pytest
from scripts.social_publish import render_post


def test_render_post_ok():
    md = {'title': 'Ep1', 'guest': 'Jared', 'ep_link': 'https://youtu.be/VID'}
    txt = render_post('x', md)
    assert 'Ep1' in txt and 'Jared' in txt


def test_render_post_missing_key():
    md = {'title': 'Ep1', 'ep_link': 'https://youtu.be/VID'}
    with pytest.raises(KeyError):
        render_post('x', md)
