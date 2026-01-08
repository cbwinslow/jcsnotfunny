# SEO Agent

## Overview
Generates SEO metadata and JSON-LD for episode pages and clips.

## Inputs
- Title, summary, keywords
- Canonical URL and thumbnail URL
- Guest name and episode number

## Outputs
- SEO JSON package (`exports/seo/<episode>.json`)

## Usage
```bash
python - <<'PY'
from scripts.seo_tools import build_seo_package, write_seo_package
seo = build_seo_package(
    title="Episode Title",
    summary="Short description",
    keywords=["podcast", "comedy", "guest"],
    canonical_url="https://jaredsnotfunny.com/episodes/ep01",
    og_image_url="https://cdn.example.com/thumbs/ep01.png",
    episode_number="1",
    guest_name="Guest Name",
)
write_seo_package(seo, "exports/seo/ep01.json")
PY
```
