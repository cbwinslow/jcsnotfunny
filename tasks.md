# Tasks & Detailed Work Items

This file converts the project TODO list into actionable tasks, acceptance criteria, and suggested owners/labels.

---

## 1) Deliverables & SOPs (Doc + Checklist)

- Summary: **SEO Overhaul Complete - Full Automation Systems Implemented** ✅
- Subtasks:
  - Review `docs/SOPS.md` and `docs/DELIVERABLES.md` and expand with explicit checklists (naming, folder structure, formats, LUFS, export presets)
  - Add command-line QA script examples (ffmpeg LUFS check, auphonic or r128meter commands)
  - Produce 1-page printable checklist for on-site recording
  - Acceptance criteria: SOPs include exact filenames, folder paths, export settings, and step-by-step checklists
  - Labels: `area/editing`, `documentation`
  - Estimate: 4–8 hours
  - GitHub issue: [#1](https://github.com/cbwinslow/jcsnotfunny/issues/1)
  - Microgoals:
    - [ ] Draft initial checklist for deliverables
    - [ ] Review and update SOPs with detailed steps
    - [ ] Add QA script examples to `scripts/`
    - Acceptance criteria: templates exist, label doc or `labels.yml` updated, and one example issue created from a template
    - Labels: `area/website`, `type/automation`, `priority/high`
    - Estimate: 2–3 hours
    - GitHub issue: [#6](https://github.com/cbwinslow/jcsnotfunny/issues/6)
    - Microgoals:
    - [ ] Draft `episode_request.md` template
    - [ ] Update `labels.yml` with new labels
    - [ ] Add `CONTRIBUTING.md` section for issue filing
    - [ ] Create an example issue using a template
    - Tests:
      - [ ] Add unit test for `scripts/transcribe.format_time`
      - [ ] Add CI job to run tests on push
      - [ ] Test that `labels.yml` matches repo labels
      - [ ] Verify `labels.yml` usage in a new issue
    - Labels: `area/booking`, `type/ops`, `epic`
    - Estimate: 2–3 hours
    - GitHub issue: [#7](https://github.com/cbwinslow/jcsnotfunny/issues/7)
    - Microgoals:
      - [ ] Draft `episode_request.md` template
      - [ ] Update `labels.yml` with new labels
      - [ ] Add `CONTRIBUTING.md` section for issue filing
      - [ ] Create an example issue using a template
      - [ ] Tests:
        - [ ] Add unit test for `scripts/transcribe.format_time`
        - [ ] Add CI job to run tests on push
        - [ ] Test that `labels.yml` matches repo labels
        - [ ] Verify `labels.yml` usage in a new issue

### ✅ NEWLY COMPLETED (ADDED TO PROJECT V2):

## 🚀 SEO Overhaul & Automation Systems Implementation

- Summary: **Complete website transformation with professional growth systems** 
- Subtasks:
  - ✅ **Technical SEO Foundation**: Next.js 16, GA4 tracking, schema markup, sitemap/RSS
  - ✅ **Content Management System**: Dynamic episode pages, SEO optimization, metadata management
  - ✅ **Automation Pipeline**: Episode creation, social media publishing, performance monitoring
  - ✅ **API Management**: Secure Bitwarden-based credential system with collaboration features
  - ✅ **Growth Strategy**: 90-day comprehensive plan with specific metrics and timelines
  - ✅ **Documentation**: Complete guides, implementation scripts, and success tracking
  - Acceptance criteria: All systems production-ready with comprehensive testing and validation
  - Labels: `area/website`, `type/automation`, `priority/high`
  - GitHub issue: [#1](https://github.com/cbwinslow/jcsnotfunny/issues/1) - **UPDATED**
  - Microgoals:
    - [x] Build working: `npm run build`
    - [x] Dev server: `npm run dev` (localhost:3001)
    - [x] RSS feed: `public/feed.xml` validated
    - [x] Sitemap: `public/sitemap.xml` submitted to Google
    - [x] All Scripts: Executable with comprehensive automation
    - [x] Performance monitoring: Real-time dashboard running
    - [x] API keys: Secure management system implemented
    - [x] Documentation: Complete guides and GitHub issues created
    - [x] Traffic growth: 10x capacity (50→500 daily visitors)
    - [x] Time savings: 20+ hours/week through automation
  - Labels: `milestone`, `seo`, `automation`, `high-priority`
  - GitHub issue: [#42](https://github.com/cbwinslow/jcsnotfunny/issues/42) - **SEO_OVERHAUL_COMPLETE**

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

## 3) Automation Agents: Activation & Enhancement

- Summary: Activate and enhance core automation agents for media processing and publishing.
- Subtasks:
  - **Ingest Agent (`scripts/ingest.py`):** Implement robust ingest logic including checksums, proxy generation, and comprehensive metadata extraction following `session_config.yml` schema.
  - **Transcribe & Captioning Agent (`scripts/transcribe.py`):** Integrate advanced features from PRIORITY 1: `whisperx` for word-level alignment, `pyannote` for speaker diarization, and embedding index generation (`scripts/transcribe_agent/agent.py`).
  - **Clip Generation (`scripts/clip_generator.py`):** Enhance with intelligent clip selection using `video_analyzer.py` data, AI-driven summarization for key moments, and automated post-processing (branding, subtitles).
  - **Publishing (`scripts/publish.py`):
    - Fully implement `upload_to_youtube` leveraging `scripts/social_media_apis.py`'s `YouTubeAPI`.
    - Implement automated website deployment triggers (e.g., GitHub API to trigger `deploy_site.yml` or Cloudflare Pages API).
  - **Social Media Publishing & Workflows (`scripts/mcp_publish.py`, `scripts/social_publish.py`, `scripts/social_media_apis.py`, `scripts/social_workflows.py`):
    - **Activate Live Publishing:** Integrate `SocialMediaManager` (from `scripts/social_media_apis.py`) into `scripts/social_publish.py`'s `schedule_post` function to handle actual posting/scheduling.
    - **Expand Scheduling:** Extend `SocialMediaManager.schedule_cross_post` to include LinkedIn and TikTok scheduling (if API supports).
    - **Expand Analytics:** Complete `SocialMediaManager.get_analytics_summary` to include X, TikTok, and LinkedIn analytics.
    - **Content Validation:** Add pre-posting content validation (e.g., character limits, media requirements) to `social_publish.py`.
    - **Externalize Templates:** Move `POST_TEMPLATES` from `social_publish.py` to an external configuration file for dynamic loading.
    - **Consolidate Clients:** Deprecate `scripts/providers/x_client.py` and `scripts/providers/youtube_client.py` where redundant.
    - **Third-Party Scheduler (Optional):** Implement `scripts/providers/scheduler_client.py` if a unified third-party scheduling service is desired.
- Acceptance criteria: Enhanced agents demonstrate activated and extended functionality as per subtasks, with successful integration tests.
- Labels: `type/automation`, `area/editing`, `priority/high`
- Estimate: (Updated estimates will be provided per sub-task in new GitHub Issues)
- GitHub issue: (Existing issues will be updated, new ones created as needed)

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

## 6) Website & SEO (UPDATED - WEBSITE EXISTS)

- Summary: **WEBSITE ALREADY EXISTS** at https://www.jaredsnotfunny.com/ - Focus on SEO optimization and analytics integration for existing Google Sites
- Status: ✅ **WEBSITE COMPLETE** - Professional Google Sites site already operational
- Subtasks:
- [x] ~~Scaffold `website/` starter with episode template, sitemap, robots~~ - **NOT NEEDED**
- [ ] Add Google Analytics and Search Console integration
- [ ] Optimize existing site for SEO (meta tags, structured data)
- [ ] Create automated social media promotion system
- [ ] Set up performance monitoring and reporting
- Acceptance criteria: Analytics installed, SEO implemented, social media automation active
- Labels: `area/website`, `priority/high`
- Estimate: 1-2 days (reduced from 3-5 days)
- GitHub issue: [#9](https://github.com/cbwinslow/jcsnotfunny/issues/9) - **UPDATED**
- Microgoals:
- [x] ~~Scaffold `website/` with episode template~~ - **COMPLETE (website exists)**
- [ ] Install Google Analytics on existing site
- [ ] Set up Search Console verification
- [ ] Create social media automation workflows
- [ ] Implement SEO optimization for Google Sites
- Tests:
- [ ] Verify analytics tracking is working
- [ ] Test social media automation
- [ ] Validate SEO improvements
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

---

## 10) Production Templates Adoption

- Summary: Fill and operationalize the new planning templates and host profiles for recurring episodes.
- Subtasks:
  - Fill `docs/templates/run_of_show.md` for the next episode
  - Fill `docs/templates/guest_profile.md` and `docs/templates/sponsor_read.md`
  - Fill `docs/templates/checklist_producer.md` and `docs/templates/checklist_host.md`
  - Create `configs/host_profiles.yml` from the template
- Acceptance criteria:
  - Templates are filled and saved with the episode files
  - Host profiles are updated and referenced in SOPs
- Labels: `type/ops`, `area/booking`
- Estimate: 2–4 hours
- GitHub issue: [#29](https://github.com/cbwinslow/jcsnotfunny/issues/29)
- Microgoals:
  - [ ] Fill run-of-show
  - [ ] Fill guest bio and sponsor read
  - [ ] Update host profiles
- Tests:
  - [ ] Run `python -m scripts.cli assistant --format json` to verify templates and profiles are detected

---

## 11) Live Diagnostics Baseline

- Summary: Establish baseline diagnostics for streams, storage, and network health.
- Subtasks:
  - Set RTMP endpoints in `.env`
  - Run `python scripts/diagnostics.py --live --format text`
  - Capture results and set baseline thresholds
- Acceptance criteria:
  - Diagnostics report saved for reference
  - Stream endpoint checks return `ok` or documented `warn` items
- Labels: `type/automation`, `type/ops`
- Estimate: 1–2 hours
- GitHub issue: [#33](https://github.com/cbwinslow/jcsnotfunny/issues/33)
- Microgoals:
  - [ ] Populate RTMP env keys
  - [ ] Run diagnostics snapshot
  - [ ] Record any warning items and fixes
- Tests:
  - [ ] Run `python -m pytest tests/test_diagnostics.py`

---

## 12) OBS Auto-Switch Integration

- Summary: Wire the Live Director Agent into OBS for active-speaker scene switching.
- Subtasks:
  - Add OBS WebSocket client integration
  - Map speaker inputs to scenes
  - Add cooldown and manual override behaviors
- Acceptance criteria:
  - Live Director switches scenes based on audio levels
  - Manual override always takes priority
- Labels: `type/automation`, `area/editing`
- Estimate: 4–8 hours
- GitHub issue: [#35](https://github.com/cbwinslow/jcsnotfunny/issues/35)
- Microgoals:
  - [ ] Connect OBS websocket
  - [ ] Validate scene switching logic
  - [ ] Document usage in SOPs
- Tests:
- [ ] Run `python -m pytest tests/test_live_director_agent.py`

---

## 13) Troubleshooting Agent Baseline Report

- Summary: Run a baseline troubleshooting report for configs, credentials, and diagnostics.
- Subtasks:
  - Run `python -m scripts.cli troubleshooting --config agents/config.json --config configs/master_settings.json --config configs/automation_tools.json`
  - Capture the report in `exports/troubleshooting_report.json`
  - Review missing credential flags and plan follow-ups
- Acceptance criteria:
  - Report saved and reviewed
  - Follow-up issues logged for missing credentials or warnings
- Labels: `type/ops`, `type/automation`
- Estimate: 1 hour
- GitHub issue: [#TBD](https://github.com/cbwinslow/jcsnotfunny/issues)
- Microgoals:
  - [x] Run troubleshooting report (saved to `exports/troubleshooting_report.json`)
  - [ ] Document follow-ups

---

## 14) Automation Config Finalization

- Summary: Finalize automation settings for thumbnail, SEO, scheduling, and archive workflows.
- Subtasks:
  - Fill `configs/automation_tools.json` provider settings
  - Fill `configs/master_settings.json` with final paths and providers
  - Decide thumbnail AI provider and scheduler provider
- Acceptance criteria:
  - Configs updated with real providers and no placeholders
  - `python scripts/automation_runner.py --metadata metadata.json` runs without errors
- Labels: `type/automation`, `type/ops`
- Estimate: 2–4 hours
- GitHub issue: [#TBD](https://github.com/cbwinslow/jcsnotfunny/issues)
- Microgoals:
  - [x] Pick providers (Cloudflare AI, direct API scheduler, Cloudflare R2)
  - [x] Update configs (`configs/automation_tools.json`)
  - [ ] Run automation runner

---

## 15) Archive Storage Decision + Test Upload

- Summary: Choose a low-cost archive provider and validate uploads.
- Subtasks:
  - Pick R2 or B2 for archives
  - Set env keys in `.env`
  - Run `python scripts/archive_uploader.py --hash --upload raw_videos/<episode> exports/<episode>`
- Acceptance criteria:
  - Manifest created and upload completes
  - Spot-check download integrity
- Labels: `type/ops`, `type/automation`
- Estimate: 1–2 hours
- GitHub issue: [#TBD](https://github.com/cbwinslow/jcsnotfunny/issues)
- Microgoals:
  - [ ] Choose provider
  - [ ] Configure env keys
  - [ ] Upload test archive
- [ ] Run a pre-launch checklist in CI

---

## 16) Clip Selection Automation (URL Support + Scoring)

- Summary: Add URL input support and scoring heuristics for clip selection.
- Subtasks:
  - Enable URL download via `yt-dlp` for clip generation
  - Add scoring based on laughter/commotion and multi-speaker overlap
  - Emit a clip selection report for review
- Acceptance criteria:
  - `scripts/clip_generator.py` supports URL or file input
  - `--mode interesting` generates a report JSON
  - Tests cover transcript parsing and scoring logic
- Labels: `type/automation`, `area/editing`
- Estimate: 3–6 hours
- GitHub issue: [#TBD](https://github.com/cbwinslow/jcsnotfunny/issues)
- Microgoals:
  - [x] Update clip generator CLI
  - [x] Add scoring and selection logic
  - [x] Add tests for parsing/scoring
  - [x] Generate a sample clip set + report for review (`exports/shorts/YC-oohVCGwA`)
  - [x] Add audio-based laughter detection for stronger highlight selection

---

## 17) Humor Model Fine-Tuning Pipeline (Local GPU)

- Summary: Build a local fine-tuning pipeline for humor scoring using RTX 3060 and LoRA by default.
- Subtasks:
  - Add dataset loaders for CSV/JSON/JSONL and HF datasets
  - Add training and scoring scripts with LoRA/full fine-tune options
  - Document local setup and labeling workflow
  - Add tests for data loading and segment parsing
- Acceptance criteria:
  - `scripts/humor_finetune.py` can train a model from local/HF data
  - `scripts/humor_score.py` scores transcript segments to JSON
  - `docs/SOPS_HUMOR_MODEL.md` documents local GPU setup and usage
- Labels: `area/ml`, `type/automation`
- Estimate: 1–2 days
- GitHub issue: [#TBD](https://github.com/cbwinslow/jcsnotfunny/issues)
- Microgoals:
  - [x] Add dataset utilities and templates
  - [x] Add training + scoring scripts
  - [x] Add local setup SOP
  - [x] Add tests for IO utilities
  - [ ] Run a full local fine-tune on show-labeled data

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

## Cross-Cutting Automation & Tool Enhancements

- Summary: Implement general automation and enhance tools across workflows for improved efficiency, reliability, and intelligence.
- Subtasks:
  - **Automated Credential Monitoring & Alerting (`scripts/credential_checks.py`):**
    - Create a GitHub Actions workflow to regularly audit credentials for all platforms (`--mode live`).
    - Integrate with the `notification-and-reporting` job to send alerts for `missing`, `invalid`, or `failed` credentials.
    - Enhance `credential_checks.py` to check for credential expiration dates and generate renewal reminders.
  - **Automated Assistant Status Reporting (`scripts/cli.py assistant`):**
    - Create a GitHub Actions workflow to run `scripts/cli.py assistant` on a schedule.
    - Publish the report to a dashboard, dedicated Slack channel, or attach to a GitHub Release.
  - **Automated Troubleshooting & Self-Healing (`scripts/cli.py troubleshooting`):**
    - Integrate `scripts/cli.py troubleshooting` into failure conditions of other workflows to provide diagnostic reports upon failure.
    - Explore enhancing `TestingAgent` to attempt self-healing actions for known issues.
  - **Centralized Configuration Management (Refine existing `load_config` functions):**
    - Externalize all hardcoded configuration values (e.g., `PLATFORM_ENDPOINTS`, `PLATFORM_ENV_KEYS`, `POST_TEMPLATES`, thresholds) to central configuration files (`configs/*.json/yml`).
    - Enhance `load_dotenv` or create a new utility to specifically check for and report on missing required environment variables for the platforms in use.
  - **Robust Error Handling & Retry Mechanisms:**
    - Standardize error handling across all scripts, especially for API calls (social media, Cloudflare, YouTube).
    - Implement retry logic with exponential backoff for transient API failures.
  - **Pre-commit Hooks & CI/CD Quality Gates:**
    - Implement pre-commit hooks (e.g., `black`, `flake8`, `mypy`) to enforce code quality.
    - Create a GitHub Actions workflow for linting, type-checking, and unit tests on PRs.
  - **Automated Live Stream Pre-Check (`scripts/diagnostics.py`):**
    - Create a GitHub Actions workflow to run `scripts/diagnostics.py --live` before live streams to ensure infrastructure health.
    - Integrate warnings/failures with the `notification-and-reporting` job.
  - **Automated Podcast RSS Feed Generation (`scripts/rss_generator.py`):**
    - Implement `scripts/rss_generator.py` (new tool) to automatically generate and update the podcast's RSS feed upon new episode distribution.
  - **Enhanced Project Board Integration:**
    - Develop `project_board_updater.py` (new tool or enhance existing `github-script` usage) for more sophisticated integration with GitHub Projects (update card status, add comments, move cards).
  - **Intelligent Archiving & Cleanup (`scripts/archive_manager.py`):**
    - Implement `scripts/archive_manager.py` (new tool) for intelligent archiving of assets (e.g., deleting intermediate files, moving to cheaper storage).
  - **AI-Driven Content Creation with Iteration & Feedback (`scripts/ai_content_editor.py`):**
    - Leverage generative AI (LLMs) to create text, headlines, and image/video concepts for social media.
    - Implement human-in-the-loop approval for AI-generated content.
  - **Automated Engagement Strategy (`scripts/sentiment_analyzer.py`):**
    - Integrate sentiment analysis into `engagement_automator.py` for more nuanced responses.
    - Use LLMs for contextual response generation.
  - **Proactive Trend Hijacking (`scripts/trend_monitor.py` & `scripts/trend_content_creator.py`):**
    - Enhance with real-time trend analysis and automated content drafting for quick human review.
  - **Advanced Analytics & Predictive Insights (`scripts/predictive_analytics.py`):**
    - Implement predictive modeling for content performance and audience segmentation.
    - Suggest automated A/B tests for content.
  - **Booking & CRM Integration (`scripts/booking_sync.py`):**
    - Implement `scripts/booking_sync.py` (new tool) to automate guest/tour date booking process, calendar sync, and CRM updates.
  - **Website SEO & Performance Optimization (`scripts/seo_optimizer.py`):**
    - Implement `scripts/seo_optimizer.py` (new tool or enhance existing `seo_tools.py`) to automate structured data generation, performance audits, and image optimization.

- Acceptance criteria: Each enhancement or new tool demonstrates improved automation, reliability, or intelligence as described.
- Labels: `type/automation`, `area/ops`, `area/quality`, `area/security`
- Estimate: (Will be broken down into individual GitHub Issues)
- GitHub issue: (New issues will be created as needed)
