# Thumbnail Agent

## Overview
Generates a thumbnail brief and AI prompt using episode metadata, transcript, and keyframes.

## Inputs
- Title, summary, transcript text
- Keyframes (optional)
- Brand colors and typography

## Outputs
- Thumbnail brief JSON
- Suggested text overlay and style notes

## Usage
```bash
python - <<'PY'
from scripts.thumbnail_agent import generate_thumbnail_brief
payload = generate_thumbnail_brief(
    title="Episode Title",
    summary="One-sentence hook",
    transcript_path="exports/transcripts/ep01.json",
    keyframe_paths=["exports/frames/ep01_01.png"],
    out_path="exports/thumbnails/thumbnail_brief.json",
)
print(payload["prompt"])
PY
```

## Notes
- Replace `generate_thumbnail_image` with your chosen AI provider.
- Keep overlay text short (4-6 words).
