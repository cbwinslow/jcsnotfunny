"""Thumbnail agent helpers for generating a thumbnail brief and prompt."""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

STOPWORDS = {
    'the', 'and', 'a', 'an', 'of', 'to', 'in', 'for', 'on', 'with', 'is', 'are',
    'it', 'this', 'that', 'at', 'as', 'by', 'from', 'be', 'or', 'we', 'you',
    'your', 'our', 'they', 'their', 'i', 'me', 'my', 'us', 'was', 'were',
}


@dataclass
class ThumbnailBrief:
    title: str
    hook: str
    keywords: List[str]
    summary: str
    suggested_text: List[str]
    keyframe_paths: List[str]
    style_notes: List[str]

    def as_dict(self) -> Dict:
        return {
            'title': self.title,
            'hook': self.hook,
            'keywords': self.keywords,
            'summary': self.summary,
            'suggested_text': self.suggested_text,
            'keyframe_paths': self.keyframe_paths,
            'style_notes': self.style_notes,
        }


def _load_text(path: Path) -> str:
    if not path.exists():
        return ''
    if path.suffix == '.json':
        with path.open('r') as fh:
            data = json.load(fh)
        return data.get('text', '') if isinstance(data, dict) else ''
    return path.read_text()


def extract_keywords(text: str, limit: int = 8) -> List[str]:
    words = re.findall(r"[A-Za-z0-9']+", text.lower())
    counts: Dict[str, int] = {}
    for word in words:
        if word in STOPWORDS or len(word) <= 2:
            continue
        counts[word] = counts.get(word, 0) + 1
    ranked = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return [word for word, _count in ranked[:limit]]


def build_thumbnail_brief(
    title: str,
    summary: str,
    transcript: str,
    keyframe_paths: Optional[List[str]] = None,
) -> ThumbnailBrief:
    keyframe_paths = keyframe_paths or []
    keywords = extract_keywords(' '.join([title, summary, transcript]), limit=8)
    hook = summary.split('. ', 1)[0] if summary else title
    suggested_text = [title, hook]
    style_notes = [
        'Use bold, high-contrast text',
        'Emphasize guest face or expressive moment',
        'Keep text under 4-6 words',
    ]
    return ThumbnailBrief(
        title=title,
        hook=hook,
        keywords=keywords,
        summary=summary,
        suggested_text=suggested_text,
        keyframe_paths=keyframe_paths,
        style_notes=style_notes,
    )


def build_thumbnail_prompt(brief: ThumbnailBrief) -> str:
    keywords = ', '.join(brief.keywords)
    text_overlay = ' / '.join(brief.suggested_text[:2])
    keyframes = ', '.join(brief.keyframe_paths) if brief.keyframe_paths else 'no keyframes provided'
    return (
        "Create a YouTube thumbnail. "
        f"Title: {brief.title}. "
        f"Hook: {brief.hook}. "
        f"Keywords: {keywords}. "
        f"Text overlay suggestion: {text_overlay}. "
        f"Keyframes: {keyframes}. "
        "Use bold typography, high contrast, and a clean composition."
    )


def generate_thumbnail_brief(
    title: str,
    summary: str = '',
    transcript_path: Optional[str] = None,
    keyframe_paths: Optional[List[str]] = None,
    out_path: Optional[str] = None,
) -> Dict:
    transcript = ''
    if transcript_path:
        transcript = _load_text(Path(transcript_path))
    brief = build_thumbnail_brief(
        title=title,
        summary=summary,
        transcript=transcript,
        keyframe_paths=keyframe_paths or [],
    )
    payload = brief.as_dict()
    payload['prompt'] = build_thumbnail_prompt(brief)
    if out_path:
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, 'w') as fh:
            json.dump(payload, fh, indent=2)
    return payload


def generate_thumbnail_image(*_args, **_kwargs):
    """Placeholder for AI image generation; integrate with your provider."""
    raise NotImplementedError('Integrate an image generation provider here')
