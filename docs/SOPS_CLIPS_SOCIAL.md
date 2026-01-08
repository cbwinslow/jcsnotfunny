# SOP - Clips, Social Posts, and Scheduling

## Purpose
Define clip creation, social asset prep, and scheduling/validation procedures.

## Inputs
- Final episode master, timestamps, and social templates.

## Outputs
- Exported clips, captions, thumbnails, and scheduled social posts.

## Checklist - Clip Selection
- [ ] Identify 5-10 clip candidates with timestamps.
- [ ] Prioritize moments with hooks in the first 3 seconds.
- [ ] Confirm no spoilers or sensitive content.
- [ ] Document clip title, platform, and CTA.

## Checklist - Clip Editing
- [ ] Create 15-90 second clips for each platform.
- [ ] Add burned-in captions and verify readability.
- [ ] Export vertical versions (1080x1920) and square versions (1080x1080) as needed.
- [ ] Add platform-specific safe area padding.
- [ ] Verify audio loudness consistency.

## Checklist - Social Copy
- [ ] Generate copy from `templates/social_post_templates.md`.
- [ ] Confirm hashtags and tags for each platform.
- [ ] Validate metadata placeholders (title, guest, links).
  - Optional: generate thumbnail brief via `scripts/thumbnail_agent.py`.

## Checklist - SEO Hooks
- [ ] Generate SEO metadata for episode and clips.
- [ ] Confirm keywords match the episode topic and guest.

## Checklist - Scheduling
- [ ] Use `scripts/social_workflows.py` or `scripts/mcp_publish.py` to schedule.
- [ ] Log scheduled time, platform, and post IDs.
- [ ] Confirm scheduled post status in provider UI (if available).

## Checklist - Validation
- [ ] Fetch recent posts and verify the scheduled post exists.
- [ ] Check publish timing vs scheduled time (tolerance <= 5 minutes).
- [ ] Confirm links resolve and point to correct destination.
- [ ] Capture any failures with error logs or screenshots.

## Placeholders
- [PLACEHOLDER: clip quota per episode]
- [PLACEHOLDER: default scheduling cadence]
