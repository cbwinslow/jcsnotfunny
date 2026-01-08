"""Social publish helper (stub)

Generates post text from templates and offers helper methods to post to
X, Instagram, TikTok, LinkedIn, Facebook, or scheduling services (Buffer, Hootsuite).

Environment variables:
- X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN (for Twitter/X)
- IG_USERNAME and IG_PASSWORD (or use the Facebook Graph API tokens)
- SCHEDULER_API_KEY for scheduling providers
"""
import os
import logging
from datetime import datetime, timezone

logger = logging.getLogger('social_publish')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(ch)

POST_TEMPLATES = {
    'x': "{title} — New episode: {ep_link} | Guest: {guest} #JaredsNotFunny",
    'instagram': "{title}\n\nGuest: {guest}\n\nListen/link in bio: {ep_link}\n\n#podcast #comedy",
    'yt_short': "Clip: {title} — {guest} | Watch full ep: {ep_link}",
    'youtube': "{title}\nGuest: {guest}\nWatch: {ep_link}",
    'tiktok': "Clip from {title} — {guest} | {ep_link}",
    'linkedin': "{title} — New episode with {guest}. Watch: {ep_link}",
    'facebook': "{title} — New episode with {guest}. Watch: {ep_link}",
}


def render_post(platform, metadata):
    template = POST_TEMPLATES.get(platform)
    if not template:
        raise ValueError('Unknown platform')
    # Verify placeholders exist in metadata
    try:
        text = template.format(**metadata)
    except KeyError as e:
        missing = e.args[0]
        logger.error('Missing metadata key for template: %s', missing)
        raise
    return text


def schedule_post(platform, metadata, when=None):
    text = render_post(platform, metadata)
    when = when or datetime.now(timezone.utc).isoformat()
    logger.info('Scheduling on %s at %s', platform, when)
    logger.debug('\n%s\n', text)
    # Implement API calls to scheduling provider or direct publish
    return {'scheduled_at': when, 'platform': platform}


if __name__ == '__main__':
    md = {'title': 'Ep 0 — Pilot', 'ep_link': 'https://youtu.be/VIDID', 'guest': 'Jared Christianson'}
    print(render_post('x', md))
    schedule_post('x', md)
