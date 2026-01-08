# End-to-end integration smoke test for publish -> transcribe -> auto-edit

Summary

Add an end-to-end smoke test that runs the publish pipeline on a small synthetic episode (sample master file) and validates outputs from transcription and auto-edit stages. The smoke test should run in CI on `workflow_dispatch` and on a cron schedule nightly for monitoring.

Acceptance criteria (measurable)

- A CI workflow `./.github/workflows/e2e-smoke.yml` runs the publish pipeline on a sample asset and asserts that transcripts, diarization JSON, EDL, and a rendered sample clip are produced and uploaded as artifacts.

- The workflow includes a failure threshold and posts results to a configured Slack / webhook on failures (optional).

Subtasks / microgoals

- Add `tests/fixtures/synthetic_episode/` sample master asset and expected output checks.
- Implement `tests/test_e2e_smoke.py` that runs the pipeline in dry-run and asserts artifacts presence.
- Add `e2e-smoke.yml` workflow with `workflow_dispatch` and `schedule` triggers.

Labels: CI, type/automation, priority/high

Estimate: 2–4 days
