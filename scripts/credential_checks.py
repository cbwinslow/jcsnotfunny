"""Credential auditing helpers for social, streaming, and Cloudflare."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Tuple

import requests

from scripts.social_workflows import load_dotenv, required_env_vars

SOCIAL_PLATFORMS = ['x', 'instagram', 'tiktok', 'youtube', 'linkedin', 'facebook', 'yt_short']

STREAMING_TARGETS: Dict[str, Tuple[str, str]] = {
    'youtube_live': ('YOUTUBE_RTMP_URL', 'YOUTUBE_STREAM_KEY'),
    'twitch_live': ('TWITCH_RTMP_URL', 'TWITCH_STREAM_KEY'),
    'x_live': ('X_RTMP_URL', 'X_STREAM_KEY'),
    'facebook_live': ('FACEBOOK_RTMP_URL', 'FACEBOOK_STREAM_KEY'),
    'instagram_live': ('INSTAGRAM_RTMP_URL', 'INSTAGRAM_STREAM_KEY'),
    'tiktok_live': ('TIKTOK_RTMP_URL', 'TIKTOK_STREAM_KEY'),
    'kick_live': ('KICK_RTMP_URL', 'KICK_STREAM_KEY'),
    'linkedin_live': ('LINKEDIN_RTMP_URL', 'LINKEDIN_STREAM_KEY'),
}

OBS_KEYS = ['OBS_PROFILE', 'OBS_SCENE_COLLECTION', 'OBS_WEBSOCKET_HOST', 'OBS_WEBSOCKET_PORT']

CLOUDFLARE_TOKEN_KEYS = [
    'CF_IMAGES_API_TOKEN',
    'CF_STREAM_API_TOKEN',
    'CF_WORKERS_API_TOKEN',
    'CF_AI_API_TOKEN',
]

CLOUDFLARE_R2_KEYS = [
    'CF_R2_ACCESS_KEY_ID',
    'CF_R2_SECRET_ACCESS_KEY',
    'CF_R2_BUCKET',
    'CF_R2_ENDPOINT',
]


@dataclass
class CredentialCheckResult:
    category: str
    name: str
    status: str
    details: str = ''
    missing: List[str] = field(default_factory=list)
    checked: bool = False

    def as_dict(self) -> Dict:
        return {
            'category': self.category,
            'name': self.name,
            'status': self.status,
            'details': self.details,
            'missing': self.missing,
            'checked': self.checked,
        }


def _format_missing(missing: Iterable[str]) -> str:
    return ', '.join(sorted(set(missing)))


def _is_rtmp_url(value: str) -> bool:
    return value.startswith('rtmp://') or value.startswith('rtmps://')


def _check_env_group(category: str, name: str, keys: List[str]) -> CredentialCheckResult:
    missing = [key for key in keys if not os.environ.get(key)]
    if missing:
        return CredentialCheckResult(
            category=category,
            name=name,
            status='missing',
            details=f'missing env: {_format_missing(missing)}',
            missing=missing,
            checked=False,
        )
    return CredentialCheckResult(category=category, name=name, status='ok', checked=False)


def _check_stream_target(name: str, rtmp_key: str, stream_key: str) -> CredentialCheckResult:
    missing = [key for key in (rtmp_key, stream_key) if not os.environ.get(key)]
    if missing:
        return CredentialCheckResult(
            category='streaming',
            name=name,
            status='missing',
            details=f'missing env: {_format_missing(missing)}',
            missing=missing,
            checked=False,
        )
    rtmp_url = os.environ.get(rtmp_key, '')
    if not _is_rtmp_url(rtmp_url):
        return CredentialCheckResult(
            category='streaming',
            name=name,
            status='invalid',
            details='rtmp url must start with rtmp:// or rtmps://',
            checked=False,
        )
    return CredentialCheckResult(category='streaming', name=name, status='ok', checked=False)


def _cloudflare_verify_token(token: str, session: requests.Session) -> Tuple[bool, str]:
    url = 'https://api.cloudflare.com/client/v4/user/tokens/verify'
    headers = {'Authorization': f'Bearer {token}'}
    resp = session.get(url, headers=headers, timeout=10)
    if resp.status_code != 200:
        return False, f'http_{resp.status_code}'
    data = resp.json()
    return bool(data.get('success')), 'ok' if data.get('success') else 'invalid'


def _check_cloudflare_tokens(mode: str, session: requests.Session) -> List[CredentialCheckResult]:
    results: List[CredentialCheckResult] = []
    for key in CLOUDFLARE_TOKEN_KEYS:
        token = os.environ.get(key)
        name = key.lower().replace('cf_', '').replace('_api_token', '_token')
        if not token:
            results.append(
                CredentialCheckResult(
                    category='cloudflare',
                    name=name,
                    status='missing',
                    details=f'missing env: {key}',
                    missing=[key],
                    checked=False,
                )
            )
            continue
        if mode != 'live':
            results.append(
                CredentialCheckResult(
                    category='cloudflare',
                    name=name,
                    status='ok',
                    details='token present (live check skipped)',
                    checked=False,
                )
            )
            continue
        ok, detail = _cloudflare_verify_token(token, session)
        results.append(
            CredentialCheckResult(
                category='cloudflare',
                name=name,
                status='ok' if ok else 'failed',
                details=detail,
                checked=True,
            )
        )
    return results


def _live_check_youtube(session: requests.Session) -> CredentialCheckResult:
    api_key = os.environ.get('YT_API_KEY')
    channel_id = os.environ.get('YT_CHANNEL_ID')
    if not api_key or not channel_id:
        return CredentialCheckResult(
            category='social',
            name='youtube',
            status='missing',
            details='missing env: YT_API_KEY or YT_CHANNEL_ID',
            missing=[k for k in ['YT_API_KEY', 'YT_CHANNEL_ID'] if not os.environ.get(k)],
            checked=False,
        )
    url = 'https://www.googleapis.com/youtube/v3/channels'
    params = {'part': 'id', 'id': channel_id, 'key': api_key}
    resp = session.get(url, params=params, timeout=10)
    if resp.status_code != 200:
        return CredentialCheckResult(
            category='social',
            name='youtube',
            status='failed',
            details=f'http_{resp.status_code}',
            checked=True,
        )
    items = resp.json().get('items', [])
    return CredentialCheckResult(
        category='social',
        name='youtube',
        status='ok' if items else 'failed',
        details='ok' if items else 'channel not found',
        checked=True,
    )


def _live_check_instagram(session: requests.Session) -> CredentialCheckResult:
    token = os.environ.get('INSTAGRAM_ACCESS_TOKEN')
    business_id = os.environ.get('INSTAGRAM_BUSINESS_ID')
    if not token or not business_id:
        missing = [k for k in ['INSTAGRAM_ACCESS_TOKEN', 'INSTAGRAM_BUSINESS_ID'] if not os.environ.get(k)]
        return CredentialCheckResult(
            category='social',
            name='instagram',
            status='missing',
            details=f'missing env: {_format_missing(missing)}',
            missing=missing,
            checked=False,
        )
    url = f'https://graph.facebook.com/v18.0/{business_id}'
    params = {'fields': 'id', 'access_token': token}
    resp = session.get(url, params=params, timeout=10)
    if resp.status_code != 200:
        return CredentialCheckResult(
            category='social',
            name='instagram',
            status='failed',
            details=f'http_{resp.status_code}',
            checked=True,
        )
    data = resp.json()
    return CredentialCheckResult(
        category='social',
        name='instagram',
        status='ok' if data.get('id') else 'failed',
        details='ok' if data.get('id') else 'no business id returned',
        checked=True,
    )


def _live_check_facebook(session: requests.Session) -> CredentialCheckResult:
    token = os.environ.get('FACEBOOK_PAGE_ACCESS_TOKEN')
    page_id = os.environ.get('FACEBOOK_PAGE_ID')
    if not token or not page_id:
        missing = [k for k in ['FACEBOOK_PAGE_ACCESS_TOKEN', 'FACEBOOK_PAGE_ID'] if not os.environ.get(k)]
        return CredentialCheckResult(
            category='social',
            name='facebook',
            status='missing',
            details=f'missing env: {_format_missing(missing)}',
            missing=missing,
            checked=False,
        )
    url = f'https://graph.facebook.com/v18.0/{page_id}'
    params = {'fields': 'id', 'access_token': token}
    resp = session.get(url, params=params, timeout=10)
    if resp.status_code != 200:
        return CredentialCheckResult(
            category='social',
            name='facebook',
            status='failed',
            details=f'http_{resp.status_code}',
            checked=True,
        )
    data = resp.json()
    return CredentialCheckResult(
        category='social',
        name='facebook',
        status='ok' if data.get('id') else 'failed',
        details='ok' if data.get('id') else 'no page id returned',
        checked=True,
    )


def _live_check_linkedin(session: requests.Session) -> CredentialCheckResult:
    token = os.environ.get('LINKEDIN_ACCESS_TOKEN')
    if not token:
        return CredentialCheckResult(
            category='social',
            name='linkedin',
            status='missing',
            details='missing env: LINKEDIN_ACCESS_TOKEN',
            missing=['LINKEDIN_ACCESS_TOKEN'],
            checked=False,
        )
    url = 'https://api.linkedin.com/v2/me'
    headers = {'Authorization': f'Bearer {token}'}
    resp = session.get(url, headers=headers, timeout=10)
    if resp.status_code != 200:
        return CredentialCheckResult(
            category='social',
            name='linkedin',
            status='failed',
            details=f'http_{resp.status_code}',
            checked=True,
        )
    return CredentialCheckResult(
        category='social',
        name='linkedin',
        status='ok',
        details='ok',
        checked=True,
    )


def audit_credentials(
    mode: str = 'offline',
    env_path: str = '.env',
    session: Optional[requests.Session] = None,
) -> List[CredentialCheckResult]:
    load_dotenv(env_path, override=False)
    session = session or requests.Session()
    results: List[CredentialCheckResult] = []

    for platform in SOCIAL_PLATFORMS:
        results.append(_check_env_group('social', platform, required_env_vars(platform)))

    for name, (rtmp_key, stream_key) in STREAMING_TARGETS.items():
        results.append(_check_stream_target(name, rtmp_key, stream_key))

    results.append(_check_env_group('streaming', 'obs_websocket', OBS_KEYS))
    results.append(_check_env_group('streaming', 'restream', ['RESTREAM_API_KEY']))

    results.extend(_check_cloudflare_tokens(mode, session))
    results.append(_check_env_group('cloudflare', 'r2', CLOUDFLARE_R2_KEYS))

    if mode == 'live':
        live_checks = [
            _live_check_youtube,
            _live_check_instagram,
            _live_check_facebook,
            _live_check_linkedin,
        ]
        for check in live_checks:
            results.append(check(session))

    return results


def summarize_results(results: Iterable[CredentialCheckResult]) -> Dict[str, int]:
    summary: Dict[str, int] = {}
    for result in results:
        summary[result.status] = summary.get(result.status, 0) + 1
    return summary


def format_report(results: Iterable[CredentialCheckResult]) -> str:
    lines = []
    for result in results:
        detail = f" - {result.details}" if result.details else ''
        lines.append(f"[{result.category}] {result.name}: {result.status}{detail}")
    return '\n'.join(lines)


def results_to_json(results: Iterable[CredentialCheckResult]) -> str:
    return json.dumps([result.as_dict() for result in results], indent=2)
