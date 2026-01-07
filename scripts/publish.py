"""Publishing helper stub

Functions:
- upload_to_youtube(video_path, title, description, tags)
- push_episode_to_website(metadata, content_dir)

This is a stub demonstrating expected inputs and how secrets are used.
Implementations should use the official APIs and secure credentials.
"""
import os
import json
import logging

logger = logging.getLogger('publish')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(ch)


def upload_to_youtube(video_path, title, description, tags=None):
    """Placeholder: upload a video to YouTube using OAuth credentials stored in env vars.

    Environment variables expected (examples):
    - YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN

    Returns a dict with 'url' and 'id' when successful.
    """
    logger.info('Simulating upload of %s to YouTube with title: %s', video_path, title)
    # Return example response
    return {'id': 'VIDEO_ID_123', 'url': f'https://youtu.be/VIDEO_ID_123'}


def push_episode_to_website(metadata, content_dir):
    """Placeholder: commit episode data to the website content folder and trigger a deploy.

    metadata: dict with fields: title, date, guest, youtube_url, transcript_path, tags
    content_dir: path under `website/content/episodes/`
    """
    os.makedirs(content_dir, exist_ok=True)
    target = os.path.join(content_dir, f"{metadata['slug']}.json")
    with open(target, 'w') as fh:
        json.dump(metadata, fh, indent=2)
    logger.info('Wrote episode metadata to %s', target)
    # Optionally trigger a site deploy via Cloudflare Pages or commit & push
    return target


if __name__ == '__main__':
    # simple smoke test
    meta = dict(title='Test ep', date='2026-01-07', guest='Jared Christianson', slug='ep-000-test')
    push_episode_to_website(meta, 'website/content/episodes')
