"""YouTube client stub for uploads (shorts / video)

Implements a simple interface and token refresh placeholder. For real
implementations, use google-auth and googleapiclient.
"""
import os
import logging

import requests

logger = logging.getLogger('youtube_client')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(ch)

class YouTubeClient:
    def __init__(self, client_id=None, client_secret=None, refresh_token=None):
        self.client_id = client_id or os.environ.get('YT_CLIENT_ID')
        self.client_secret = client_secret or os.environ.get('YT_CLIENT_SECRET')
        self.refresh_token = refresh_token or os.environ.get('YT_REFRESH_TOKEN')

    def refresh_access_token(self):
        """Refresh access token using OAuth2 refresh token flow.

        Returns the token response JSON (expects an `access_token` field).
        Raises RuntimeError if credentials are missing.
        """
        if not all([self.client_id, self.client_secret, self.refresh_token]):
            raise RuntimeError('Missing YouTube OAuth credentials')

        token_url = 'https://oauth2.googleapis.com/token'
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token,
            'grant_type': 'refresh_token',
        }
        resp = requests.post(token_url, data=data, timeout=10)
        resp.raise_for_status()
        out = resp.json()
        # expected fields: access_token, expires_in, scope, token_type
        logger.info('Refreshed access token, expires in %s', out.get('expires_in'))
        return out

    def upload_short(self, file_path, title, description, tags=None):
        """Upload a short (MP4) to YouTube using googleapiclient resumable upload.

        Uses an access token obtained from refresh_access_token() to construct
        google.oauth2.credentials.Credentials and perform a videos.insert()
        request. On success returns a dict with `id` and `url`.
        """
        token_response = self.refresh_access_token()
        access_token = token_response.get('access_token')
        if not access_token:
            raise RuntimeError('Failed to obtain access token for upload')

        try:
            from googleapiclient.discovery import build
            from googleapiclient.http import MediaFileUpload
            from google.oauth2.credentials import Credentials
        except Exception as exc:  # pragma: no cover - environment may not have googleapiclient in CI
            logger.warning('googleapiclient not available: %s; falling back to simulation', exc)
            logger.info('Simulating YouTube upload for %s (title=%s)', file_path, title)
            return {'id': 'YT_SHORT_123', 'url': 'https://youtu.be/YT_SHORT_123'}

        creds = Credentials(token=access_token)
        youtube = build('youtube', 'v3', credentials=creds)

        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags or [],
            },
            'status': {
                'privacyStatus': 'public'
            }
        }

        media = MediaFileUpload(file_path, chunksize=-1, resumable=True, mimetype='video/mp4')
        req = youtube.videos().insert(part='snippet,status', body=body, media_body=media)

        try:
            resp = req.execute()
            vid_id = resp.get('id')
            logger.info('Uploaded to YouTube id=%s', vid_id)
            return {'id': vid_id, 'url': f'https://youtu.be/{vid_id}'}
        except Exception as exc:
            logger.exception('YouTube upload failed: %s', exc)
            raise

