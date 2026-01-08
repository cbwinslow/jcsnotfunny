# Live Streaming & Multi-Platform Archival Agent (Priority: 3)

Summary

Implement a live-controller capable of programmatically switching scenes (OBS WebSocket integration), pushing to a relay (Nginx-RTMP or SRS), and recording/archiving streams and triggering post-processing pipelines (transcription & auto-edit).

Acceptance criteria (measurable)

- `scripts/live_controller/demo.py` runs against a mocked OBS WebSocket and logs scene change requests in the expected order (unit test with WebSocket mock).

- A simulated streaming run against a local RTMP relay produces a recorded file and triggers `scripts/transcribe_agent` (mocked CI smoke test asserting the trigger was invoked).

- Recorded file metadata includes ad-read timestamps and chapters JSON.

Subtasks / microgoals

- Add docker-compose example for Nginx-RTMP for local test relay.

- Implement an OBS WebSocket demo controller and unit tests with mocks.

- Implement archiver trigger and a smoke test that asserts downstream pipeline invocation.

- Document multi-stream configuration and secrets required for endpoints.

Labels: type/automation, area/website, priority/medium

Estimate: 3–6 days (PoC + tests)
