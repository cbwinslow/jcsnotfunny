"""SEO helper utilities for episodes, clips, and pages."""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Optional


@dataclass
class SEOPackage:
    title: str
    description: str
    keywords: List[str]
    canonical_url: Optional[str]
    og_image_url: Optional[str]
    jsonld: Dict

    def as_dict(self) -> Dict:
        return {
            'title': self.title,
            'description': self.description,
            'keywords': self.keywords,
            'canonical_url': self.canonical_url,
            'og_image_url': self.og_image_url,
            'jsonld': self.jsonld,
        }


def build_jsonld_episode(
    title: str,
    description: str,
    url: str,
    published_at: Optional[str] = None,
    episode_number: Optional[str] = None,
    show_name: str = "Jared's Not Funny",
    host_name: str = "Jared",
    guest_name: Optional[str] = None,
    image_url: Optional[str] = None,
) -> Dict:
    published_at = published_at or datetime.now(timezone.utc).date().isoformat()
    jsonld = {
        '@context': 'https://schema.org',
        '@type': 'PodcastEpisode',
        'name': title,
        'description': description,
        'url': url,
        'partOfSeries': {
            '@type': 'PodcastSeries',
            'name': show_name,
        },
        'datePublished': published_at,
        'author': {'@type': 'Person', 'name': host_name},
    }
    if episode_number:
        jsonld['episodeNumber'] = episode_number
    if guest_name:
        jsonld['actor'] = {'@type': 'Person', 'name': guest_name}
    if image_url:
        jsonld['image'] = image_url
    return jsonld


def build_seo_package(
    title: str,
    summary: str,
    keywords: List[str],
    canonical_url: Optional[str],
    og_image_url: Optional[str],
    published_at: Optional[str] = None,
    episode_number: Optional[str] = None,
    guest_name: Optional[str] = None,
) -> SEOPackage:
    jsonld = build_jsonld_episode(
        title=title,
        description=summary,
        url=canonical_url or '',
        published_at=published_at,
        episode_number=episode_number,
        guest_name=guest_name,
        image_url=og_image_url,
    )
    return SEOPackage(
        title=title,
        description=summary,
        keywords=keywords,
        canonical_url=canonical_url,
        og_image_url=og_image_url,
        jsonld=jsonld,
    )


def write_seo_package(seo: SEOPackage, path: str) -> str:
    from pathlib import Path
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as fh:
        json.dump(seo.as_dict(), fh, indent=2)
    return path
