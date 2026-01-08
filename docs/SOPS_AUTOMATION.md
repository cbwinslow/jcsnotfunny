# SOP - Automation Workflows (Thumbnails, SEO, Scheduling, Archive)

## Purpose
Provide repeatable automation steps for thumbnails, SEO, scheduling, and file archiving.

## Tooling Config
- `configs/automation_tools.yml` controls which automation services are used.
- `configs/master_settings.yml` points to the automation config file.
  - JSON config is also supported: `configs/automation_tools.json`.

## Thumbnail Automation
- Inputs: title, summary, transcript, keyframes.
- Tool: `scripts/thumbnail_agent.py` generates a thumbnail brief and prompt.
- Output: `exports/thumbnails/thumbnail_brief.json` and optional image.

Checklist:
- [ ] Capture keyframes or mark moments for the thumbnail.
- [ ] Run thumbnail brief generation and review suggested text.
- [ ] Approve final thumbnail before upload.

Example:
```bash
python scripts/automation_runner.py --metadata metadata.json --transcript exports/transcripts/ep01.json --keyframes exports/frames/ep01_01.png
```

## SEO Automation
- Inputs: title, summary, keywords, canonical URL, thumbnail URL.
- Tool: `scripts/seo_tools.py` builds metadata and JSON-LD.
- Output: `exports/seo/<episode>.json`

Checklist:
- [ ] Confirm keywords and summary accuracy.
- [ ] Verify JSON-LD schema includes guest and episode number.
- [ ] Link the thumbnail URL and canonical URL.

## Social Scheduling Automation
- Inputs: metadata, base publish time, platform offsets.
- Tool: `scripts/social_scheduler.py` to build a schedule and call the workflow.
- Output: scheduled post IDs and validation reports.

Checklist:
- [ ] Confirm publish time and timezone.
- [ ] Review scheduled posts in provider UI.
- [ ] Validate post timing within tolerance.

## Archive Upload Automation
- Inputs: final exports, transcripts, project files.
- Tool: `scripts/archive_uploader.py` to build a manifest and upload to R2/B2.
- Output: `exports/archive_manifest.json` and uploaded objects.
  - Budget-friendly storage: Cloudflare R2 (cheap, no egress to Cloudflare), Backblaze B2.

Checklist:
- [ ] Build a manifest with hashes enabled for integrity checks.
- [ ] Upload to the archive bucket.
- [ ] Verify samples download correctly.
