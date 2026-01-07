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

---

## Notes / Next steps

- After you review this `tasks.md`, I can create Project v2 board items and convert these task drafts into real GitHub issues via the GitHub UI/API. If you'd like, I can also add issue drafts under `.github/issues/` so they're ready for creating issues.
