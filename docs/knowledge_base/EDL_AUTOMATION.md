# EDL (Edit Decision List) — Auto-Edit PoC

Purpose: deterministic selection of short clip candidates from transcript segments.

Key functions
- `select_candidate_clips(segments, min_duration, max_duration, max_clips, min_funny_score)` — returns ranked, non-overlapping clips
  - Logic: normalize segments, bump score for laughter markers, enforce duration bounds, sort by score then duration, pick non-overlapping top candidates
- `write_edl(clips, output_path)` — writes JSON edl

Inputs expected
- Segments with time keys (`start`/`end` or `start_time`/`end_time`), `text`, optional `funny_score`

Best practices
- Use `min_funny_score` conservatively; tune with real data
- Respect non-overlap to avoid duplicate content
- Store EDL artifacts (e.g., `edl.json`) alongside clips for traceability

Tests & Integration
- Unit tests: `tests/test_auto_edit.py`
- Integration: wired into `scripts/youtube_shorts_pipeline.py` and tested by `tests/test_youtube_shorts_pipeline_integration.py`

Notes
- PoC uses deterministic heuristics to keep tests reproducible; ML scoring can replace heuristics later.
