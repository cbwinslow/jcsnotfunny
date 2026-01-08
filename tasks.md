# Tasks & Detailed Work Items

This file converts the project TODO list into actionable tasks, acceptance criteria, and suggested owners/labels.

---

## 1) Deliverables & SOPs (Doc + Checklist)

- Summary: Finalize and formalize the deliverable specs and SOPs for ingest → edit → mix → clips → publish
- Subtasks:
  - Review `docs/SOPS.md` and `docs/DELIVERABLES.md` and expand with explicit checklists (naming, folder structure, formats, LUFS, export presets)
  - Add command-line QA script examples (ffmpeg LUFS check, auphonic or r128meter commands)
  - Produce 1-page printable checklist for on-site recording
- Acceptance criteria:
  - SOPs include exact filenames, folder paths, export settings, and step-by-step checklists
  - Examples and one test script are added to `scripts/` and referenced in the SOP
- Labels: `area/editing`, `documentation`
- Estimate: 4–8 hours
- GitHub issue: [#1](https://github.com/cbwinslow/jcsnotfunny/issues/1)
- Microgoals:
  - [ ] Draft initial checklist for deliverables
  - [ ] Review and update SOPs with detailed steps
  - [ ] Add QA script examples to `scripts/`
  - [ ] Finalize and print on-site recording checklist
- Tests:
  - [ ] Add unit test for `scripts/transcribe.format_time`
  - [ ] Add unit test for LUFS/export validation script
  - [ ] Add CI job to run tests on push

---

## 2) Issue templates & labels

- Summary: Create issue templates for Feature, Bug, Episode Request, Task; maintain label taxonomy with clear usage guide
- Subtasks:
- Add `episode_request.md` template (guest name, date, availability, brief)
- Update `labels.yml` with new labels (area/booking, priority/low, type/ops, epic)
- Add a short `CONTRIBUTING.md` section describing label usage and how to file issues
- Acceptance criteria: templates exist, label doc or `labels.yml` updated, and one example issue created from a template
- Labels: `area/website`, `type/automation`, `priority/high`
- Estimate: 2–3 hours
- GitHub issue: [#6](https://github.com/cbwinslow/jcsnotfunny/issues/6)
- Microgoals:
- [ ] Draft `episode_request.md` template
- [ ] Update `labels.yml` with new labels
- [ ] Add `CONTRIBUTING.md` section for issue filing
- [ ] Create an example issue using the template
- Tests:
- [ ] Unit test to validate issue templates parsing
- [ ] Test that `labels.yml` matches repo labels

---

## 3) Automation agents (ingest, transcribe, clip-generator, publish)

- Summary: Design lightweight agents and example workflows that can be run locally or in CI
- Subtasks:
- Define each agent: inputs, outputs, success criteria
- Create simple proof-of-concept scripts: ingest (done), transcribe (Whisper/assembly.ai passthrough), clip-generator (ffmpeg + timestamps), publish (youtube-upload stub)
- Add `examples/agents/README.md` documenting usage
- Acceptance criteria: proof-of-concept scripts exist with README and example run
- Labels: `type/automation`, `area/editing`
- Estimate: 2–3 days (PoC)
- GitHub issue: [#7](https://github.com/cbwinslow/jcsnotfunny/issues/7)
- Microgoals:
- [ ] Define inputs/outputs for each agent
- [ ] Create proof-of-concept scripts for ingest, transcribe, clip-generator, and publish
- [ ] Document usage in `examples/agents/README.md`
- Tests:
- [ ] Add unit tests for `parse_vtt` and `parse_time` (done)
- [ ] Add integration test for a small clip generation run (CI artifact)
- GitHub issue: [#12](https://github.com/cbwinslow/jcsnotfunny/issues/12)
- GitHub issue: [#13](https://github.com/cbwinslow/jcsnotfunny/issues/13)
- Follow-ups:
- [ ] Implement X client (issue: [#14](https://github.com/cbwinslow/jcsnotfunny/issues/14))
- [ ] Implement YouTube client (issue: [#15](https://github.com/cbwinslow/jcsnotfunny/issues/15))
- [ ] Implement Scheduler integration (issue: [#16](https://github.com/cbwinslow/jcsnotfunny/issues/16))
- GitHub issue: [#7](https://github.com/cbwinslow/jcsnotfunny/issues/7)

---

## 4) CI / Deploy

- Summary: Build a GitHub Actions layout for site build, deploy, and optional clip-generation runner
- Subtasks:
- Add `deploy_site.yml` (added) and test with a simple `website/` build
- Add an `artifact` job for generated clips/assets for integration testing
- Add secrets docs & required permissions
- Acceptance criteria: site build passes and artifacts are uploaded to actions artifacts or cloud storage
- Labels: `CI`, `type/automation`
- Estimate: 1–2 days
- GitHub issue: [#8](https://github.com/cbwinslow/jcsnotfunny/issues/8)
- Microgoals:
- [ ] Add and test `deploy_site.yml`
- [ ] Add `artifact` job for clips/assets
- [ ] Document secrets and permissions
- Tests:
- [ ] Add CI workflow to build website and upload example artifact
- [ ] Smoke test GitHub Actions with a sample commit

---

## 5) Cloudflare & CDN setup

- Summary: Document and configure Cloudflare Pages + DNS + caching and asset strategies
- Subtasks:
- Add Cloudflare Pages deploy action (done) and `CLOUDFLARE_SETUP.md` docs (done)
- Add recommended cache rules for `assets/`, STS headers, and signed access notes
- Acceptance criteria: docs complete and secrets referenced. Optional: test Pages deploy to staging domain
- Labels: `area/website`
- Estimate: 2–4 hours
- GitHub issue: [#2](https://github.com/cbwinslow/jcsnotfunny/issues/2)
- Microgoals:
- [ ] Review and update `CLOUDFLARE_SETUP.md`
- [ ] Add cache rules and security headers
- [ ] Test Cloudflare Pages deploy
- Tests:
- [ ] Add an automated test to validate sitemap & robots
- [ ] Validate Pages deploy in staging

---

## 6) Website & SEO

- Summary: Build skeleton site (Next.js/Astro) and SEO checklists with templates for episode pages
- Subtasks:
- Scaffold `website/` starter with episode template, sitemap, robots
- Add JSON-LD schemas and meta templates
- Add sample episode page using demo data
- Acceptance criteria: local site build runs and renders sample episode, SEO checklist is in repo
- Labels: `area/website`, `priority/high`
- Estimate: 3–5 days
- GitHub issue: [#9](https://github.com/cbwinslow/jcsnotfunny/issues/9)
- Microgoals:
- [ ] Scaffold `website/` with episode template
- [ ] Add JSON-LD schemas and meta templates
- [ ] Create sample episode page with demo data
- [ ] Test local site build
- Tests:
- [ ] Add unit tests for metadata serialization
- [ ] Add end-to-end smoke test that builds the site locally

---

## 7) Booking / Workflow CRM

- Summary: Define a simple booking flow for guests, gigs, advertisers with contact forms and calendar integration
- Subtasks:
- Draft booking form + TOS and contract template
- Add suggested integrations (Calendly/Google Calendar/Notion) and automation flows
- Acceptance criteria: form + workflow documentation exists; sample calendar integration documented
- Labels: `area/booking`
- Estimate: 1–2 days
- GitHub issue: [#3](https://github.com/cbwinslow/jcsnotfunny/issues/3)
- Microgoals:
- [ ] Draft booking form and TOS
- [ ] Add integrations and automation flows
- [ ] Document sample calendar integration
- Tests:
- [ ] Add an integration test plan for Calendar/Zapier flow

---

## 8) Quality checklist & KPIs

- Summary: Create QA checklist and KPI dashboards (analytics plan)
- Subtasks:
- QA checklist (Audio LUFS, peaks, noise, color balance, captions ok)
- KPI plan: weekly views, top clips, CTR, mailing list signups
- Add sample dashboard wireframe or query list for analytics provider
- Acceptance criteria: QA checklist in `docs/` and a KPI plan with data sources
- Labels: `needs/review`, `area/website`
- Estimate: 4–6 hours
- GitHub issue: [#10](https://github.com/cbwinslow/jcsnotfunny/issues/10)
- Microgoals:
- [ ] Draft QA checklist for audio and video
- [ ] Define KPI plan and data sources
- [ ] Add sample dashboard wireframe
- Tests:
- [ ] Add automated LUFS check script and unit tests
- [ ] Add sample analytics query tests

---

## 9) Launch plan

- Summary: Define milestones to get MVP live: site + first 5 episodes + marketing plan
- Subtasks:
- Create milestone checklist for MVP (content readiness, site, analytics, promotion schedule)
- Add social promo templates and comms calendar
- Acceptance criteria: MVP checklist complete and responsible owners assigned
- Labels: `priority/high`
- Estimate: 1–2 days
- GitHub issue: [#4](https://github.com/cbwinslow/jcsnotfunny/issues/4)
- Microgoals:
- [ ] Draft MVP milestone checklist
- [ ] Create social promo templates
- [ ] Add comms calendar
- Tests:
- [ ] Verify first-5-episodes content exists and pages are linked
- [ ] Run a pre-launch checklist in CI

---

## 10) Growth & Ads

- Summary: Define ad inventory, pricing templates, sponsor docs, and delivery expectations
- Subtasks:
- Create sponsor one-pager + ad insertion SLA and spec sheet
- Add billing/invoicing template and tracking sheet
- Acceptance criteria: sponsor materials and a process for booking+tracking ads exist
- Labels: `area/booking`, `documentation`
- Estimate: 1–2 days
- GitHub issue: [#11](https://github.com/cbwinslow/jcsnotfunny/issues/11)
- Microgoals:
- [ ] Draft sponsor one-pager and SLA
- [ ] Add billing/invoicing template
- [ ] Document ad booking and tracking process
- Tests:
- [ ] Add a Financial tracking CSV test and sample invoice generation script

---

## 11) Transcription & Captioning Agent (PRIORITY 1)

- Summary: Build a robust transcription/captioning agent that produces accurate WebVTT/SRT, speaker diarization, JSON transcripts, and embeddings for RAG indexing for every media item (audio/video/streams). This is the highest priority to enable search, clipping, and RAG pipelines.
- Subtasks:
  - Implement `scripts/transcribe_agent` (CLI, agent orchestration) — prototype exists
  - Integrate word-level alignment (whisperx) and speaker diarization (pyannote or equivalent)
  - Produce VTT/SRT, JSON transcript, diarization `.diar.json`, and embedding index (FAISS or JSON fallback)
  - Add synthetic test assets (1v1.wav, 2speaker.wav) with ground-truth captions for automated tests
  - Add CI job to run transcribe on sample assets and validate outputs
- Acceptance criteria (measurable):
  - On the provided synthetic test assets, the agent produces `*.vtt`, `*.json`, and `*.diar.json` files and the VTT contains the expected sample lines (assert exact matches in tests)
  - Diarization test asserts correct number of speaker segments for 2-speaker synthetic file and that segment boundaries differ from ground-truth by <= 0.5s on average (measured in unit test)
  - Embedding index is created and a small nearest-neighbor lookup returns the expected nearest sentence for a given query (testable with FAISS or JSON fallback)
  - A CI job `transcribe-integration.yml` runs on a push and passes on the sample dataset
- Labels: `type/automation`, `area/editing`, `priority/high`
- Estimate: 2–5 days (prototype + tests)
- Microgoals:
  - [ ] Add synthetic single-speaker and multi-speaker test WAVs and ground-truth captions
  - [ ] Integrate whisperx alignment and wire into `scripts/transcribe_agent`
  - [ ] Add pyannote or fallback diarization and unit tests for diarization accuracy
  - [ ] Add embedding creation and a test for NN lookup
  - [ ] Add CI workflow to run integration test on sample assets
- Tests:
  - [ ] `tests/test_transcribe_agent.py` (unit): validate VTT/SRT creation and JSON sidecars
  - [ ] `tests/test_diarization_accuracy.py` (integration): run diarization on 2-speaker synthetic audio and assert speaker counts and timing accuracy
  - [ ] `tests/test_embeddings_index.py` (unit): ensure embeddings are produced and NN lookup returns expected id
  - [ ] Add CI job `transcribe-integration.yml` (runs only on `push` and `workflow_dispatch`) to validate outputs

---

## 12) Auto-Edit / Multi-Cam Edit Agent (PRIORITY 2)

- Summary: Build an automated multi-camera editor that takes camera feeds + audio + transcripts/CC and produces an EDL and a rendered video that focuses on the active speaker, with rules for reaction shots, wide shots, and scene-interest switching.
- Subtasks:
  - Create `scripts/auto_edit/` skeleton with modules: `ingest.py`, `sync.py`, `audio.py` (VAD/diarization hooks), `vision.py` (face detection & tracking), `mapper.py` (lip-sync mapping), `edl.py` (shot selection rules), and `renderer.py` (ffmpeg-based render)
  - Implement synthetic test videos for 1v1 and 3-way scenarios with ground-truth shot list
  - Implement face tracking (MediaPipe) and lip-motion correlation; include fallback when per-camera audio exists
  - Implement EDL generator with configurable min_shot_length, guard_time, hysteresis, and reaction-shot rules
  - Add CLI `scripts/auto_edit/cli.py` and session `session_config.yml` template
- Acceptance criteria (measurable):
  - For the provided synthetic 1v1 test, the EDL JSON generated matches ground-truth shot list within a tolerance of +/- 0.5s per cut (tested in CI)
  - EDL covers >= 95% of the speaker-active intervals (speech time) for the test set
  - Unit tests assert min_shot_length enforcement and that rapid speaker switches are smoothed according to guard_time/hysteresis rules
  - Render step produces an MP4 (or a verified simulated render) artifact and a CI job uploads it as an artifact for manual review
- Labels: `type/automation`, `area/editing`, `priority/high`
- Estimate: 4–8 days (PoC + tests)
- Microgoals:
  - [ ] Skeleton `scripts/auto_edit/` with CLI and config templates
  - [ ] Implement VAD & diarization hooks (re-use `scripts/transcribe_agent`) and tests
  - [ ] Implement face detection & tracker and unit tests on synthetic frames
  - [ ] Implement mapping and EDL generator with unit tests
  - [ ] Implement renderer proof-of-concept with ffmpeg and CI artifact upload
- Tests:
  - [ ] `tests/test_edl_generator.py` (unit): validate shot rules and constraints
  - [ ] `tests/test_face_tracker.py` (unit): run tracker over synthetic frames and assert stable track IDs
  - [ ] `tests/test_auto_edit_integration.py` (integration): run full pipeline on synthetic 1v1 and assert EDL and rendered artifact presence

---

## 13) Live Streaming & Multi-Platform Archival Agent (PRIORITY 3)

- Summary: Implement a live-controller capable of programmatically switching scenes (OBS WebSocket integration), pushing to a relay (Nginx-RTMP/SRS or Restream), and ensuring recordings are archived and post-processed (triggering transcription & auto-edit pipelines post-stream).
- Subtasks:
  - Implement `scripts/live_controller` with an OBS WebSocket client example and a control API that accepts a decision stream (JSON with timestamps/actions)
  - Build a local RTMP relay docker-compose example (Nginx-RTMP) for CI/testing and a publish module to send to multiple endpoints
  - Implement archiving hooks: ensure local or cloud recording is saved as a master file and post-processing job is triggered on completion
  - Provide an ad-read & chapters logging helper (emit timestamps to metadata JSON for downstream baking)
- Acceptance criteria (measurable):
  - A test demo script `scripts/live_controller/demo.py` when run against a mocked OBS WebSocket returns success and logs scene change requests in the expected order (unit test mocks WebSocket and asserts call sequence)
  - A simulated streaming run against the local RTMP relay produces a recorded file and triggers `scripts/transcribe_agent` on the recorded file (this can be a mocked CI smoke test checking that the trigger is invoked)
  - Recorded file metadata includes ad-read timestamps and chapters JSON
- Labels: `type/automation`, `area/website`, `priority/medium`
- Estimate: 3–6 days (PoC + tests)
- Microgoals:
  - [ ] Add docker-compose example for Nginx-RTMP as a test relay
  - [ ] Implement OBS WebSocket demo controller and unit tests with mocks
  - [ ] Implement archiver trigger and a smoke test that asserts downstream pipeline trigger
  - [ ] Document multi-stream configuration and secrets needed for endpoints
- Tests:
  - [ ] `tests/test_live_controller_mock.py` (unit): mock WebSocket and assert scene change calls
  - [ ] `tests/test_stream_archival_trigger.py` (integration): mock recording completion and assert transcribe agent invoked

---

## Cross-cutting: Media Ingest & Metadata (ALL AGENTS)

- Summary: Ensure all agents accept and normalize common media types (camera MP4/ProRes, audio WAV, per-camera audio, VTT/SRT, JSON metadata, clips) and produce consistent artifact naming & metadata JSON for traceability.
- Microgoals:
  - [ ] Define `session_config.yml` schema for camera roles, audio mapping, timecode offsets, and priorities
  - [ ] Implement `scripts/ingest.normalize()` that outputs canonical media objects and checksums
  - [ ] Add tests: ensure ingestion of each supported media type produces expected metadata fields
- Acceptance criteria (measurable):
  - Ingest normalization unit tests pass and return canonical metadata for all supported inputs
  - All generated artifacts (EDL, transcripts, renders) include a `metadata.json` that references original checksums

---

## Notes / Next steps

- After you review this `tasks.md`, I can create prioritized Project v2 board items and convert these task drafts into GitHub issues under `.github/issues/` so they're ready to be created. Priorities are: 1) Transcription & Captioning Agent, 2) Auto-Edit Agent, 3) Live Streaming & Archival Agent.
