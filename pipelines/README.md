# Content Pipeline Design

## Goal ✅
Automate detection of new podcast episodes, extract high-quality short clips (YouTube Shorts/TikTok), run QA, and publish to staging/production channels with observability and retries.

## Scope
- Trigger pipeline on new episode (YouTube webhook or scheduled poll)
- Run funny-moment detection and quality scoring
- Generate clips and thumbnails optimized for mobile
- Publish to staging environment for QA, then to production
- Provide metrics, alerts, and logs

---

## Key Components 🔧
- Trigger: YouTube webhook (recommended) or scheduled poll (cron)
- Orchestration: `production_launcher.py` (or agent runner) executed in GitHub Actions / self-hosted runner
- Processing: agent(s) for detection, trimming, quality scoring, thumbnail generation
- Storage: `generated_clips/` (artifacts) + optional cloud storage (S3/GCS)
- Publishing: Jobs to upload to platform APIs with templated metadata
- Observability: Logging, metrics telemetry, Slack/GitHub notifications

---

## Triggers & Workflow
- Webhook (preferred): YouTube → middle service (secure endpoint) → dispatch a `repository_dispatch` event to GitHub repo
- Polling (fallback): Scheduled GitHub Actions workflow runs every N minutes/hours, checks channel via YouTube Data API for new uploads

Sequence:
1. Trigger (webhook or scheduler) identifies new episode
2. Create a draft GitHub Issue (or project item) to track work
3. Kick `content_pipeline` workflow (GitHub Actions) to run `production_launcher.py` with env vars
4. Agents process video and produce artifacts in `generated_clips/` and/or cloud storage
5. Run QA step (automated checks + optional manual QA via PR or GitHub Issue assignment)
6. If QA passes, run publishing job to staging (and optionally production)
7. Create a release note/issue comment with links and metrics

---

## File & API Contracts
- Input: video URL or file path + episode metadata (title, publish date, id)
- Output: clips (mp4), thumbnails (.png/jpg), metadata JSON

Artifacts naming convention:
`generated_clips/{episode_id}/{clip_type}/{episode_id}-{clip_index}-{format}.mp4`

---

## Secrets & Credentials 🔑
- `YOUTUBE_API_KEY` (read), `YOUTUBE_OAUTH` (publish) — GitHub Secrets
- `TIKTOK_KEY`, `INSTAGRAM_TOKEN` — GH Secrets or Vault
- `CLOUD_STORAGE_CREDENTIALS` — encrypted secret or service principal

Permissions: restrict publishing keys to staging channels for initial rollout

---

## Monitoring & Alerts 📈
- Emit metrics: clip_count, clip_quality_score, upload_success, upload_latency
- Send notifications for failures: Slack + GitHub Status Check
- Store logs/artifacts for debugging

---

## E2E Tests & Local Dev
- Provide sample video fixture(s) in `tests/fixtures/sample_videos/`
- E2E test job: runs full pipeline using sample videos and mocked API creds
- Mock production uploads in CI and assert artifacts generated

---

## Acceptance Criteria ✅
- Pipeline detects new episode and runs end-to-end on a sample post
- Artifacts are generated and stored in `generated_clips/`
- QA checks pass for automated criteria (audio levels, subtitles detection, adequate resolution)
- Publishing to a staging channel succeeds with retry on transient errors

---

## Rollout Plan
1. Implement pipeline in staging with polling + scheduled actions
2. Add webhook receiver/service and enable repository_dispatch for fast runs
3. Run limited production publishing to a test channel for 2 weeks
4. Gradually increase volume and add platform scheduling

---

## Next steps (short-term)
- Create `docs/pipelines.md` and add a sample `content_pipeline` GitHub Actions workflow
- Add E2E tests and sample videos
- Implement webhook handler or pick a hosted service (Cloud Run, AWS Lambda)

---

## Owners
- Automation owner: @cbwinslow
- Publishing owner: (assign)
- Monitoring owner: (assign)

---

For details on the sample workflow, see `.github/workflows/content_pipeline.yml`.