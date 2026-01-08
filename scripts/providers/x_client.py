"""X (Twitter) client stub

Implements a minimal client interface to post text updates. Uses
environment variables for credentials and provides a consistent interface
that can be used by `mcp_publish.py`.

Real implementation notes:
- Use Twitter/X API v2 or v1.1 endpoints depending on features
- For OAuth2: use OAuth 2.0 Bearer or OAuth 1.0a for user-context posting
- Handle rate-limits and 429 retries
"""
import os
import logging
from requests_oauthlib import OAuth1Session

logger = logging.getLogger('x_client')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(ch)

class XClient:
    def __init__(self, api_key=None, api_secret=None, access_token=None, access_secret=None):
        self.api_key = api_key or os.environ.get('X_API_KEY')
        self.api_secret = api_secret or os.environ.get('X_API_SECRET')
        self.access_token = access_token or os.environ.get('X_ACCESS_TOKEN')
        self.access_secret = access_secret or os.environ.get('X_ACCESS_SECRET')

    def post_text(self, text):
        """Post text to X using OAuth1 session to v1.1 statuses/update

        Returns dict {id, url} on success and raises on error.
        """
        if not all([self.api_key, self.api_secret, self.access_token, self.access_secret]):
            raise RuntimeError('Missing X API credentials')
        session = OAuth1Session(self.api_key,
                                client_secret=self.api_secret,
                                resource_owner_key=self.access_token,
                                resource_owner_secret=self.access_secret)
        url = 'https://api.twitter.com/1.1/statuses/update.json'
        resp = session.post(url, data={'status': text})
        if resp.status_code != 200:
            logger.error('X post failed: %s %s', resp.status_code, resp.text[:200])
            resp.raise_for_status()
        j = resp.json()
        post_id = j.get('id_str') or str(j.get('id'))
        screen_name = j.get('user', {}).get('screen_name', 'unknown')
        return {'id': post_id, 'url': f'https://x.com/{screen_name}/status/{post_id}'}
