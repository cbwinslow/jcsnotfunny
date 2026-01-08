# Social Scheduler Agent

## Overview
Builds a platform schedule and triggers the social workflow with time offsets.

## Inputs
- Metadata JSON (title, guest, links)
- Base publish time
- Platform offsets (minutes)

## Outputs
- Scheduled post records and validation reports

## Usage
```bash
python - <<'PY'
from scripts.social_scheduler import build_schedule, schedule_posts
from scripts.social_workflows import SocialWorkflow

schedule = build_schedule(
    platforms=["x", "instagram", "youtube"],
    base_time="2024-01-02T18:00:00-05:00",
    offsets_minutes={"instagram": 15},
)
workflow = SocialWorkflow()
out = schedule_posts(workflow, {"title": "Ep1", "guest": "Jared", "ep_link": "https://example.com"}, schedule)
print(out)
PY
```
