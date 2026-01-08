# Shorts Automation — Summary

Scope: Automate generation of YouTube Shorts from full episodes.

Key components & paths
- Pipeline: `scripts/youtube_shorts_pipeline.py` — orchestrates download → transcribe → analyze → EDL → generate clips
- EDL generator: `scripts/auto_edit/edl_generator.py` — select_candidate_clips(), write_edl()
- Shorts generator: `scripts/shorts/generate_short.py` — generate_clips_from_edl() (dry-run friendly)
- Tests: `tests/test_youtube_shorts_pipeline_integration.py` (dry-run integration)
- CI: runs in `transcribe-integration.yml` and `e2e-smoke.yml` as dry-run steps

Operational notes
- Work in dry-run mode for CI — placeholders used to avoid heavy ffmpeg/ffprobe dependency in CI.
- Add quality filters (min funny score, min duration) before clip generation to improve output quality.

Where to go next (developer tasks)
- Flesh out quality scoring and multiple formats (quotes, reactions)
- Add thumbnail generation & A/B testing hooks
- Add artifact upload & retention to CI

Related docs: `docs/knowledge_base/EDL_AUTOMATION.md`, `docs/toolsets/VIDEO_EDITING.md`
