# Website integration & media test harness

Summary

Use the existing website and linked YouTube channel as authoritative sources to test and validate our agents: transcription, auto-edit, and publish pipeline. Respect the site's robots content-signal (`ai-train=no`) and prefer YouTube API for media ingestion.

Acceptance criteria

- A GitHub Action or worker job polls the YouTube channel for new uploads and triggers `transcribe-integration.yml` (dry-run) for each new item.
- A crawler (respecting robots.txt) can discover episode pages and extract canonical URLs for indexing; saved results are added to `tests/fixtures/website_discovery/` for agent tests.
- Add docs: `docs/WEBSITE_ANALYSIS.md` and a snapshot file stored under `docs/` (done).

Subtasks

- Implement `scripts/integrations/youtube_watcher.py` (uses YouTube API) and add `tests/test_youtube_watcher.py` with a mocked API.
- Implement a site crawler `scripts/integrations/site_crawler.py` that respects robots.txt and extracts links; add a test fixture and unit tests.
- Add a workflow or worker rule that triggers on new YouTube items and runs `transcribe-integration.yml`.

Labels: type/automation, area/website, priority/high

Estimate: 2–4 days
