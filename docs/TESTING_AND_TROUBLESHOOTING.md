# Testing & Troubleshooting Guide

This document describes the testing strategy, how to run tests locally, CI workflows, and troubleshooting steps to diagnose common failures.

## Test categories

- Unit tests: small, fast, no external services — run with `pytest tests/<module>.py`
- Integration tests: rely on small sample fixtures (e.g., `tests/fixtures/transcripts`) and validate data flow between components
- E2E smoke tests: run the publish → transcribe → auto-edit smoke pipeline on a small synthetic asset and upload artifacts for review
- Diagnostics & health checks: lightweight scripts to validate the runtime environment (binaries, python packages)

## How to run locally

- Install dev dependencies:
  pip install -r requirements.txt
  pip install pytest

- Run unit tests quickly:
  pytest tests/test_transcribe_agent.py -q

- Run the full transcription integration test:
  pytest tests/test_transcription_fixtures.py tests/test_whisperx_alignment.py tests/test_diarization_accuracy.py tests/test_diar_metrics.py -q

- Run environment diagnostics:
  python scripts/diagnostics/check_env.py

## CI Workflows

- `transcribe-integration.yml` runs on push and workflow_dispatch and validates transcription fixtures and metrics and uploads artifacts.
- `e2e-smoke.yml` (planned) will run nightly and on-demand to validate the full pipeline (publish → transcribe → auto-edit) and upload artifacts.

## Troubleshooting steps (common failures)

1. Failing tests complaining about missing binaries (`ffmpeg`/`ffprobe`):

   - Run `which ffmpeg` and `ffmpeg -version` to confirm installation.
   - Install via apt/brew or use the provided Docker images.

2. Missing Python packages or import errors:

   - Ensure you're using the project's Python (virtualenv) and install `pip install -r requirements.txt`.
   - For heavy deps (pyannote, whisperx) these are optional — CI uses mocks for unit tests. Use dedicated runners with GPUs for full integration.

3. Diarization timing mismatches:

   - Run `python scripts/transcribe_agent/compute_diar_metrics.py --expected expected.diar.json --actual actual.diar.json --output metrics.json` to compute average boundary error and coverage.

4. CI test failures due to timeouts or flaky tests:
   - Re-run the workflow with `workflow_dispatch` and check artifacts in the job to narrow down the failing step.
   - Add increased timeouts or retries in tests that depend on external services.

## Debugging and Signal Collection

- The integration workflows upload `outputs/` as artifacts — download and inspect VTT, JSON, diar.json, and metrics.json.
- For non-obvious failures, collect logs by rerunning the failing job and enabling step `ACTIONS_STEP_DEBUG` secrets in GitHub Actions for more verbose logs.

## Adding more tests

- Prefer small, deterministic synthetic fixtures stored under `tests/fixtures/`.
- Mock heavy or external dependencies in unit tests (we use `sys.modules` injection for `whisper` and `pyannote.audio` in tests).

## Contact & Next Steps

If tests consistently fail on CI but pass locally, open an issue and attach the job url and artifacts; use template `bug` with label `CI` and include the artifact links.
