# Publish pipeline: Wire transcription, auto-edit and publish hooks

Summary

Wire the end-to-end publish pipeline so that when an episode is published the following steps occur (configurable): upload master files to storage, run transcription & diarization, run auto-edit to generate clips, and publish assets to platforms (YouTube/Twitch/X). Provide retries, monitoring, and artifact retention.

Acceptance criteria (measurable)

- A publish workflow `./.github/workflows/publish-pipeline.yml` exists and can be run via `workflow_dispatch` to perform (upload artifact -> transcribe -> auto-edit -> upload to publish endpoints) in a dry-run mode.
- Artifacts for each stage (transcripts, edl, rendered clips) are uploaded to Actions artifacts or configured storage.
- Workflow includes retry/backoff for transient errors and logs statuses to workflow output or a monitoring endpoint.

Subtasks / microgoals

- Add `publish-pipeline.yml` with stage jobs and a `dry_run` flag.
- Add a CLI helper `scripts/publish/pipeline.py` that orchestrates steps and can be invoked locally or in Actions.
- Add unit tests and an integration smoke test that runs on sample assets and uploads artifacts.

Labels: type/automation, area/website, priority/high

Estimate: 3–6 days
