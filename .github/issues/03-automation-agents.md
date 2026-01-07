# Issue: Automation agents (ingest, transcribe, clip-generator, publish)

**Description**
Design agents and provide sample scripts / configs so production steps can be automated.

**Subtasks**

- [ ] Define agent contracts (input file patterns, output locations, naming format)
- [ ] Add a `transcribe.py` stub that calls whisper/whisperx or an external API
- [ ] Add a `clip_generator.py` that takes timestamps and exports clips via FFmpeg
- [ ] Document how to run agents locally and in CI

**Acceptance criteria**

- All agent stubs exist under `scripts/agents/` with README and sample input/output

**Labels**: type/automation, area/editing
**Estimate**: 2-3 days (PoC)
