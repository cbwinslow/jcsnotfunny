# Growth Playbook — Jared's Not Funny

Goal: Scale Shorts production, repurpose episodes across platforms, and build merch + avatar assets to increase discoverability and revenue.

## Quick links
- Canonical links: `docs/links_and_channels.md`

## Objectives & Metrics
- Production volume: target 3–5 Shorts per episode
- Engagement: watch-through rate, saves, comments, CTR on thumbnails
- Conversion: website visits, merch purchases, newsletter signups

## Content ideas
- Funny moments (short clips with caption overlays)
- Quotes / one-liners (text-over-video, animated captions)
- Reaction/Behind-the-scenes (cut-ups + B-roll)
- Audiograms with animated avatar for audio-only clips
- Repurpose high-performing Shorts into TikTok/IG Reels with platform-specific aspect and caption tweaks

## Automation workflows (high level)
1. Channel monitor → new upload detected
2. Auto-download video → transcribe → run funny-moment detection
3. EDL selection → generate candidate clips → score & filter
4. Create Short variants (mobile layouts, thumbnails, titles/descriptions) → dry-run + manual QA → publish
5. Republish top-performing clips to other platforms with tailored captions and hashtags

## Merch (t-shirt) strategy
- Generate design concepts via generative-art + human review
- Test designs via small print-on-demand runs
- Link on the website and in Shorts descriptions

## Avatar & animation ideas
- Static avatar illustrations (Stable Diffusion / Midjourney prompts) for merch & thumbnails
- Talking avatar videos: D-ID / Synthesia / First-Order-Motion (source photo + audio) for short promos
- Audio-driven lip-sync videos (Wav2Lip, DFDNet + face tracking) for episode snippets
- Consider privacy/ethics: get explicit permission for synthetic likeness usage

## Tools & integrations (suggested)
- YouTube API (channel monitoring, upload metadata)
- Stable Diffusion / DreamStudio / Midjourney for art generation
- Runway / Kaiber / D-ID for short videos and lip sync
- FFMPEG for clip generation in production runs
- GitHub Actions for CI tests (dry-run) and artifact uploads

## Testing & CI
- Keep CI dry-run friendly (placeholders for ffmpeg heavy steps)
- Add integration tests that run the full pipeline with mock agents and deterministic fixtures
- Upload EDL + placeholder artifacts to workflow artifacts for review

## Next immediate tasks
- Create a `channel-monitor` script that watches YouTube uploads and triggers the Shorts pipeline (dry-run by default)
- Create T-shirt design generator + review workflow
- Prototype an avatar generator and a short lip-synced promo pipeline
- Add tests and CI steps for the above

## Suggested issues (created automatically):
- `Growth: Channel monitor + auto-trigger pipeline`
- `Growth: Shorts repurposing & cross-platform scheduling`
- `Merch: T-shirt design generator & POD pipeline`
- `Avatar: prototype talking-avatar videos from audio`
- `CI: upload EDL and placeholder artifacts from dry-run tests`

