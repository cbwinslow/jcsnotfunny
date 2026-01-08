# YouTube Analytics & Reporting

This document explains how to generate YouTube Analytics reports for channel performance.

Requirements

- An OAuth token with `https://www.googleapis.com/auth/yt-analytics.readonly` or a token that has read access to the channel analytics.
- The channel ID you want to query (e.g., `UC...`).

Quick start

Run a views report for a date range and print JSON:

```bash
python scripts/integrations/youtube_analytics.py --channel-id <CHANNEL_ID> --start-date 2026-01-01 --end-date 2026-01-08 --report views
```

Write a CSV report:

```bash
python scripts/integrations/youtube_analytics.py --channel-id <CHANNEL_ID> --start-date 2026-01-01 --end-date 2026-01-08 --report views --out /tmp/views.csv
```

Notes

- The Analytics API often requires OAuth (not an API key). Use `scripts/integrations/get_youtube_token.py` to obtain a token if the channel owner runs the flow and stores the value in Bitwarden or a GitHub Secret.
- The functions in `youtube_analytics.py` have a `fetcher` parameter so you can substitute a mock fetcher in tests or in environments where direct API calls are replaced with cached data.
- Example metrics: `views`, `estimatedMinutesWatched`, `averageViewDuration`, `subscribersGained`, `subscribersLost`.

Next steps

- Add more pre-built reports (daily trends, top countries, revenue reports if monetized).
- Add a periodic job to collect metrics and store them in a time-series DB (Prometheus/Grafana) or a CSV/Parquet bucket for long-term analysis.
