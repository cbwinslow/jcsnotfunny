# Post-publish automation: Trigger transcription & auto-edit on published episodes

Summary

When an episode is published (website deploy or release), automatically trigger the post-processing pipeline that: records/archives the master file, runs `scripts/transcribe_agent` (transcription + diarization + embeddings), and optionally triggers `scripts/auto_edit` to generate clips and a cleaned render.

Acceptance criteria (measurable)

- A GitHub Action or webhook exists that triggers on the publish event (release or website deploy) and enqueues a job to run transcription on the published episode asset.

- The job runs against a sample published artifact in CI and produces `vtt`, `json`, `diar.json`, and an `emb.index` artifact that are uploaded to Actions artifacts or storage.

- A follow-up job is optionally dispatched to `auto_edit` that produces an EDL JSON; an artifact is uploaded for review.

Subtasks / microgoals

- Add `./.github/workflows/post-publish.yml` (or `dispatch-post-publish.yml`) with `workflow_dispatch` and `repository_dispatch` triggers.
- Add tests that simulate a release and verify artifacts are produced and uploaded to Actions artifacts.
- Add documentation for required secrets and storage (S3 / R2 / Backblaze).

Labels: type/automation, area/website, priority/high

Estimate: 1–3 days
