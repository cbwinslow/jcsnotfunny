"""Social scheduling helpers for building schedules and validations."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Dict, Iterable, List, Optional

from scripts.social_workflows import SocialWorkflow, normalize_platform


@dataclass
class ScheduleItem:
    platform: str
    scheduled_for: str
    status: str = 'planned'

    def as_dict(self) -> Dict:
        return {
            'platform': self.platform,
            'scheduled_for': self.scheduled_for,
            'status': self.status,
        }


def _coerce_datetime(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed


def build_schedule(
    platforms: Iterable[str],
    base_time: str,
    offsets_minutes: Optional[Dict[str, int]] = None,
) -> List[ScheduleItem]:
    offsets_minutes = offsets_minutes or {}
    base_dt = _coerce_datetime(base_time)
    items: List[ScheduleItem] = []
    for platform in platforms:
        key = normalize_platform(platform)
        offset = offsets_minutes.get(key, 0)
        scheduled = base_dt + timedelta(minutes=offset)
        items.append(
            ScheduleItem(platform=key, scheduled_for=scheduled.astimezone(timezone.utc).isoformat())
        )
    return items


def schedule_posts(
    workflow: SocialWorkflow,
    metadata: Dict,
    schedule: List[ScheduleItem],
) -> Dict[str, Dict]:
    results: Dict[str, Dict] = {}
    for item in schedule:
        out = workflow.publish([item.platform], metadata, scheduled_for=item.scheduled_for)
        results[item.platform] = out.get(item.platform, {})
    return results


def validate_schedule(
    workflow: SocialWorkflow,
    metadata: Dict,
    schedule: List[ScheduleItem],
    tolerance_seconds: int = 300,
) -> Dict[str, Dict]:
    reports: Dict[str, Dict] = {}
    for item in schedule:
        report = workflow.validate_post(
            platform=item.platform,
            expected_text=None,
            scheduled_for=item.scheduled_for,
            tolerance_seconds=tolerance_seconds,
        )
        reports[item.platform] = report.as_dict()
    return reports
