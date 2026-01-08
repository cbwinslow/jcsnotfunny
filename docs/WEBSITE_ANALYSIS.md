# Website analysis: Jared's Not Funny (https://www.jaredsnotfunny.com/)

Date: 2026-01-08 UTC

Summary

- Host: Google Sites (site shows "Page updatedGoogle Sites"). Site uses Cloudflare-managed settings (robots content-signal header present).
- Primary platforms linked: YouTube channel (main source of podcast episodes), Linktree (shows/tickets), TikTok, other socials.
- Robots.txt includes a content-signal header: `search=yes, ai-train=no`. It explicitly disallows GPTBot and several other crawlers.
- No `sitemap.xml` detected at the root (404).

Immediate implications / policy

- The `ai-train=no` signal indicates training/AI input usage is explicitly disallowed. Respect these signals: do not use the website content for training models or bulk AI ingestion for model updates.
- `search=yes` and `Allow: /` indicates regular crawling for search/indexing (short excerpts and links) is permitted.

Fast opportunities (quick wins)

1. Add machine-readable syndication feeds (RSS/Atom) or ensure YouTube channel RSS is surfaced on the site for automated polling of new episodes.
2. Add a simple sitemap.xml so crawlers and search engines discover site structure (automatically generated or static in site files).
3. Expose structured metadata (JSON-LD) on episode pages: episode title, description, published date, duration, tags, and canonical URL.
4. Provide published transcripts (WebVTT/SRT) alongside episode pages or links to their transcript artifacts; this improves accessibility and enables search.
5. Add OpenGraph and Twitter Card meta tags for rich link previews on social platforms.

Medium-term improvements

1. Integrate the site with our pipeline: when a new YouTube episode is published, trigger our post-publish automation to fetch, transcribe, generate clips, and add clips/summary to the episode page.
2. Create an episodes index page with structured JSON (search endpoint) for site search and API consumption by our agents.
3. Add visual/audio accessibility checks and a badge on episode pages indicating transcript availability and audio LUFS check.

Agent test & integration ideas

- Use YouTube API (preferred) to enumerate new uploads on the channel (avoid scraping the site). For each new upload:
  - Download video (yt-dlp) to a test storage bucket and run `scripts/transcribe_agent`.
  - Validate VTT/SRT generation and diarization quality (use our synthetic metric thresholds as acceptance for smoke runs).
  - Generate clips (auto-edit) and publish short clips to a test channel or stash as artifacts for manual review.
- Use the site's Linktree and social links as a discovery source for short-form content (TikTok) and integrate scheduled sampling for clips.

SEO & Accessibility checklist

- Add canonical URLs and JSON-LD for episodes.
- Ensure images have alt text and meaningful captions.
- Provide transcripts for each episode and include structured data (Transcript schema) if possible.
- Serve a sitemap.xml and robots.txt (already present) and include `ai-train` content-signal explicitly as required.
- Monitor Core Web Vitals and compress/optimize images (WebP) for faster loads.

Security & Privacy

- Check that contact forms or mailing list capture sensitive data safely (HTTPS enforced already via Cloudflare).
- Ensure any embedded third-party scripts are trusted and do not leak PII.

Next steps I can take (pick any)

- Create automated integration that polls YouTube channel and runs the `transcribe-integration` workflow when new episodes appear (using GitHub Actions or our worker).
- Add a script to crawl the site respecting robots.txt and extract episode pages and links (for indexing/searching) and add that crawl to `tests/fixtures/` for agent testing.
- Prepare a sitemap.md or patch for the website (if we have editing access) to add RSS and JSON-LD.

Permission note

We must obey the site's robots content signals: crawling for search is allowed, but AI training and bulk ingestion for model training is disallowed. Use the YouTube channel as the preferred source for media files and transcripts (YouTube TOS and API must be followed).
