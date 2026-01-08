"""Social workflow utilities for API/MCP publishing, scheduling, and validation.

These helpers are intentionally lightweight so they can run offline in tests.
Integrate real provider SDKs by swapping the provider client implementation.
"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional, Tuple

from scripts.mcp_publish import publish_via_mcp
from scripts.social_publish import render_post

logger = logging.getLogger('social_workflows')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(ch)

PLATFORM_ALIASES = {
    'twitter': 'x',
    'x/twitter': 'x',
    'ig': 'instagram',
    'yt': 'youtube',
    'li': 'linkedin',
    'fb': 'facebook',
}

PLATFORM_ENDPOINTS: Dict[str, Dict[str, str]] = {
    'x': {
        'base_url': 'https://api.twitter.com/2',
        'post': '/tweets',
        'recent': '/users/{user_id}/tweets',
        'status': '/tweets/{id}',
    },
    'instagram': {
        'base_url': 'https://graph.facebook.com/v18.0',
        'post': '/{business_id}/media',
        'publish': '/{business_id}/media_publish',
        'recent': '/{business_id}/media',
    },
    'tiktok': {
        'base_url': 'https://open.tiktokapis.com/v2',
        'post': '/post/publish/video/init/',
        'recent': '/post/publish/video/list/',
        'status': '/post/publish/status/',
    },
    'youtube': {
        'base_url': 'https://www.googleapis.com/youtube/v3',
        'post': '/videos',
        'recent': '/search',
        'status': '/videos',
    },
    'yt_short': {
        'base_url': 'https://www.googleapis.com/youtube/v3',
        'post': '/videos',
        'recent': '/search',
        'status': '/videos',
    },
    'linkedin': {
        'base_url': 'https://api.linkedin.com/v2',
        'post': '/ugcPosts',
        'recent': '/ugcPosts',
    },
    'facebook': {
        'base_url': 'https://graph.facebook.com/v18.0',
        'post': '/{page_id}/feed',
        'recent': '/{page_id}/posts',
    },
}

PLATFORM_ENV_KEYS: Dict[str, List[str]] = {
    'x': [
        'X_API_KEY',
        'X_API_SECRET',
        'X_ACCESS_TOKEN',
        'X_ACCESS_SECRET',
        'X_BEARER_TOKEN',
    ],
    'instagram': ['INSTAGRAM_ACCESS_TOKEN', 'INSTAGRAM_BUSINESS_ID'],
    'tiktok': ['TIKTOK_CLIENT_KEY', 'TIKTOK_CLIENT_SECRET', 'TIKTOK_ACCESS_TOKEN'],
    'youtube': [
        'YT_API_KEY',
        'YT_CLIENT_ID',
        'YT_CLIENT_SECRET',
        'YT_REFRESH_TOKEN',
        'YT_CHANNEL_ID',
    ],
    'yt_short': [
        'YT_API_KEY',
        'YT_CLIENT_ID',
        'YT_CLIENT_SECRET',
        'YT_REFRESH_TOKEN',
        'YT_CHANNEL_ID',
    ],
    'linkedin': ['LINKEDIN_CLIENT_ID', 'LINKEDIN_CLIENT_SECRET', 'LINKEDIN_ACCESS_TOKEN'],
    'facebook': ['FACEBOOK_PAGE_ID', 'FACEBOOK_PAGE_ACCESS_TOKEN'],
}


def load_dotenv(path: str = '.env', override: bool = False) -> Dict[str, str]:
    """Load a simple .env file without external dependencies."""
    if not os.path.exists(path):
        return {}
    loaded: Dict[str, str] = {}
    with open(path, 'r') as fh:
        for raw_line in fh:
            line = raw_line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if not key:
                continue
            if key in os.environ and not override:
                continue
            os.environ[key] = value
            loaded[key] = value
    return loaded


def normalize_platform(platform: str) -> str:
    return PLATFORM_ALIASES.get(platform.strip().lower(), platform.strip().lower())


def list_supported_platforms() -> List[str]:
    return sorted(PLATFORM_ENDPOINTS.keys())


def build_endpoint(platform: str, operation: str, **params: Any) -> str:
    platform_key = normalize_platform(platform)
    if platform_key not in PLATFORM_ENDPOINTS:
        raise KeyError(f'Unknown platform: {platform}')
    base_url = PLATFORM_ENDPOINTS[platform_key]['base_url']
    if operation not in PLATFORM_ENDPOINTS[platform_key]:
        raise KeyError(f'Unknown operation for {platform_key}: {operation}')
    path = PLATFORM_ENDPOINTS[platform_key][operation]
    try:
        path = path.format(**params)
    except KeyError as exc:
        raise KeyError(f'Missing endpoint params for {platform_key}:{operation}') from exc
    return f'{base_url}{path}'


def required_env_vars(platform: str) -> List[str]:
    return PLATFORM_ENV_KEYS.get(normalize_platform(platform), [])


def missing_env_vars(platform: str) -> List[str]:
    return [key for key in required_env_vars(platform) if not os.environ.get(key)]


def _normalize_text(text: str) -> str:
    return ' '.join(text.lower().split())


def _coerce_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value
    if isinstance(value, str):
        clean_value = value.replace('Z', '+00:00') if value.endswith('Z') else value
        parsed = datetime.fromisoformat(clean_value)
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=timezone.utc)
        return parsed
    raise TypeError('Expected datetime or ISO 8601 string')


def _isoformat(value: Any) -> str:
    return _coerce_datetime(value).astimezone(timezone.utc).isoformat()


def check_release_timing(
    scheduled_for: Any,
    published_at: Any,
    tolerance_seconds: int = 300,
) -> Tuple[int, str]:
    scheduled_dt = _coerce_datetime(scheduled_for)
    published_dt = _coerce_datetime(published_at)
    delta_seconds = int((published_dt - scheduled_dt).total_seconds())
    if abs(delta_seconds) <= tolerance_seconds:
        return delta_seconds, 'on_time'
    if delta_seconds > 0:
        return delta_seconds, 'late'
    return delta_seconds, 'early'


@dataclass
class PostRecord:
    id: str
    platform: str
    text: str
    created_at: str
    status: str
    published_at: Optional[str] = None
    scheduled_for: Optional[str] = None
    url: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'platform': self.platform,
            'text': self.text,
            'created_at': self.created_at,
            'status': self.status,
            'published_at': self.published_at,
            'scheduled_for': self.scheduled_for,
            'url': self.url,
            'metadata': self.metadata,
        }


@dataclass
class ValidationReport:
    platform: str
    expected_text: Optional[str]
    post_id: Optional[str]
    found: bool
    matched_text: bool
    scheduled_for: Optional[str]
    published_at: Optional[str]
    release_delta_seconds: Optional[int]
    timing_status: Optional[str]
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def as_dict(self) -> Dict[str, Any]:
        return {
            'platform': self.platform,
            'expected_text': self.expected_text,
            'post_id': self.post_id,
            'found': self.found,
            'matched_text': self.matched_text,
            'scheduled_for': self.scheduled_for,
            'published_at': self.published_at,
            'release_delta_seconds': self.release_delta_seconds,
            'timing_status': self.timing_status,
            'errors': self.errors,
            'warnings': self.warnings,
        }


class InMemoryPostStore:
    def __init__(self) -> None:
        self._posts: List[PostRecord] = []
        self._counter = 0

    def next_id(self, platform: str) -> str:
        self._counter += 1
        return f'{platform}_post_{self._counter}'

    def add(self, post: PostRecord) -> None:
        self._posts.append(post)

    def update(self, post_id: str, **updates: Any) -> PostRecord:
        for post in self._posts:
            if post.id == post_id:
                for key, value in updates.items():
                    setattr(post, key, value)
                return post
        raise KeyError(f'Post not found: {post_id}')

    def list_recent(self, platform: str, limit: int = 5) -> List[PostRecord]:
        filtered = [post for post in self._posts if post.platform == platform]
        filtered.sort(key=lambda item: item.created_at, reverse=True)
        return filtered[:limit]


class MockProviderClient:
    """Offline provider client for tests and local validation."""
    def __init__(self, store: Optional[InMemoryPostStore] = None) -> None:
        self.store = store or InMemoryPostStore()

    def post_text(self, platform: str, text: str, url: Optional[str] = None) -> PostRecord:
        now = _isoformat(datetime.now(timezone.utc))
        post = PostRecord(
            id=self.store.next_id(platform),
            platform=platform,
            text=text,
            created_at=now,
            status='published',
            published_at=now,
            url=url,
        )
        self.store.add(post)
        return post

    def schedule_text(self, platform: str, text: str, when: Any) -> PostRecord:
        now = _isoformat(datetime.now(timezone.utc))
        post = PostRecord(
            id=self.store.next_id(platform),
            platform=platform,
            text=text,
            created_at=now,
            status='scheduled',
            scheduled_for=_isoformat(when),
        )
        self.store.add(post)
        return post

    def mark_published(self, post_id: str, published_at: Any) -> PostRecord:
        return self.store.update(
            post_id,
            status='published',
            published_at=_isoformat(published_at),
        )

    def fetch_recent_posts(self, platform: str, limit: int = 5) -> List[PostRecord]:
        return self.store.list_recent(platform, limit=limit)


def find_matching_post(
    posts: Iterable[PostRecord],
    expected_text: Optional[str] = None,
    post_id: Optional[str] = None,
) -> Optional[PostRecord]:
    if post_id:
        for post in posts:
            if post.id == post_id:
                return post
        return None
    if expected_text:
        target = _normalize_text(expected_text)
        for post in posts:
            if target and target in _normalize_text(post.text):
                return post
    return None


def validate_post_delivery(
    platform: str,
    posts: Iterable[PostRecord],
    expected_text: Optional[str] = None,
    post_id: Optional[str] = None,
    scheduled_for: Optional[Any] = None,
    tolerance_seconds: int = 300,
) -> ValidationReport:
    errors: List[str] = []
    warnings: List[str] = []
    if not expected_text and not post_id:
        errors.append('missing_expected_text_or_post_id')
    match = find_matching_post(posts, expected_text=expected_text, post_id=post_id)
    if not match:
        errors.append('post_not_found')
        return ValidationReport(
            platform=platform,
            expected_text=expected_text,
            post_id=post_id,
            found=False,
            matched_text=False,
            scheduled_for=_isoformat(scheduled_for) if scheduled_for else None,
            published_at=None,
            release_delta_seconds=None,
            timing_status=None,
            errors=errors,
            warnings=warnings,
        )
    matched_text = False
    if expected_text:
        matched_text = _normalize_text(expected_text) in _normalize_text(match.text)
        if not matched_text:
            warnings.append('expected_text_not_found_in_post')
    release_delta_seconds = None
    timing_status = None
    if scheduled_for:
        if match.published_at:
            release_delta_seconds, timing_status = check_release_timing(
                scheduled_for,
                match.published_at,
                tolerance_seconds=tolerance_seconds,
            )
        else:
            warnings.append('scheduled_post_not_published')
    return ValidationReport(
        platform=platform,
        expected_text=expected_text,
        post_id=match.id,
        found=True,
        matched_text=matched_text or (expected_text is None),
        scheduled_for=_isoformat(scheduled_for) if scheduled_for else match.scheduled_for,
        published_at=match.published_at,
        release_delta_seconds=release_delta_seconds,
        timing_status=timing_status,
        errors=errors,
        warnings=warnings,
    )


class SocialWorkflow:
    """Unified workflow for API or MCP publishing + validation."""
    def __init__(
        self,
        mode: str = 'api',
        provider_client: Optional[MockProviderClient] = None,
        mcp_endpoint: Optional[str] = None,
        mcp_api_key: Optional[str] = None,
        env_path: str = '.env',
        load_env: bool = True,
    ) -> None:
        if load_env:
            load_dotenv(env_path, override=False)
        self.mode = mode
        self.provider_client = provider_client or MockProviderClient()
        self.mcp_endpoint = mcp_endpoint or os.environ.get('MCP_ENDPOINT')
        self.mcp_api_key = mcp_api_key or os.environ.get('MCP_API_KEY')

    def publish(
        self,
        platforms: Iterable[str],
        metadata: Dict[str, Any],
        scheduled_for: Optional[Any] = None,
    ) -> Dict[str, Dict[str, Any]]:
        normalized = [normalize_platform(p) for p in platforms]
        if self.mode == 'mcp':
            if not self.mcp_endpoint:
                raise ValueError('MCP endpoint is required for mode=mcp')
            return publish_via_mcp(
                self.mcp_endpoint,
                self.mcp_api_key,
                normalized,
                metadata,
                scheduled_for=_isoformat(scheduled_for) if scheduled_for else None,
            )
        results: Dict[str, Dict[str, Any]] = {}
        for platform in normalized:
            text = render_post(platform, metadata)
            if scheduled_for:
                post = self.provider_client.schedule_text(platform, text, scheduled_for)
                results[platform] = {'rendered': text, 'scheduled': post.as_dict()}
            else:
                post = self.provider_client.post_text(platform, text)
                results[platform] = {'rendered': text, 'published': post.as_dict()}
        return results

    def fetch_recent_posts(self, platform: str, limit: int = 5) -> List[PostRecord]:
        return self.provider_client.fetch_recent_posts(normalize_platform(platform), limit=limit)

    def validate_post(
        self,
        platform: str,
        expected_text: Optional[str] = None,
        post_id: Optional[str] = None,
        scheduled_for: Optional[Any] = None,
        tolerance_seconds: int = 300,
    ) -> ValidationReport:
        posts = self.fetch_recent_posts(platform, limit=10)
        return validate_post_delivery(
            platform=normalize_platform(platform),
            posts=posts,
            expected_text=expected_text,
            post_id=post_id,
            scheduled_for=scheduled_for,
            tolerance_seconds=tolerance_seconds,
        )
