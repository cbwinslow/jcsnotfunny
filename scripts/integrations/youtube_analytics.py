"""YouTube Analytics helpers and report generator.

This module provides simple helpers to fetch YouTube Analytics reports and
produce basic summaries (views by video, watchTime, traffic sources, subscribers).

Design notes:
- Supports dependency injection for the HTTP fetcher to ease testing.
- By default uses requests to call the YouTube Analytics `reports` endpoint.
- Requires OAuth access token for analytics; a service that only has API key may
  have limited capabilities.
"""
from __future__ import annotations

import csv
import datetime
import json
import logging
import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

import requests

logger = logging.getLogger("youtube_analytics")
logging.basicConfig(level=logging.INFO)

YT_ANALYTICS_REPORTS = "https://youtubeanalytics.googleapis.com/v2/reports"


@dataclass
class ReportRow:
    metric_values: Dict[str, Any]
    dimensions: Dict[str, Any]


class YouTubeAnalyticsError(RuntimeError):
    pass


def _default_fetcher(url: str, params: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:
    resp = requests.get(url, params=params, headers=headers, timeout=15)
    if resp.status_code != 200:
        logger.error("YouTube Analytics error: %s %s", resp.status_code, resp.text)
        raise YouTubeAnalyticsError(f"Analytics API returned {resp.status_code}")
    return resp.json()


def fetch_report(
    start_date: str,
    end_date: str,
    metrics: str,
    dimensions: Optional[str] = None,
    channel_id: Optional[str] = None,
    access_token: Optional[str] = None,
    fetcher=_default_fetcher,
) -> Dict[str, Any]:
    """Fetch a report from YouTube Analytics API.

    start_date / end_date: ISO yyyy-mm-dd
    metrics: comma-separated metrics per API (e.g., views,estimatedMinutesWatched)
    dimensions: optional comma-separated dimensions
    channel_id: required (use channel==CHANNEL_ID in ids)

    Returns parsed JSON response or raises YouTubeAnalyticsError.
    """
    if not channel_id:
        raise YouTubeAnalyticsError("channel_id is required")

    ids = f"channel=={channel_id}"
    params: Dict[str, Any] = {
        "ids": ids,
        "startDate": start_date,
        "endDate": end_date,
        "metrics": metrics,
    }
    if dimensions:
        params["dimensions"] = dimensions

    headers = {}
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    data = fetcher(YT_ANALYTICS_REPORTS, params=params, headers=headers)
    return data


def parse_simple_rows(data: Dict[str, Any]) -> List[ReportRow]:
    """Parse a simple analytics report into rows (dimensions vs metric values).

    The typical Analytics v2 `reports` response contains `columnHeaders` and `rows`.
    """
    headers = data.get("columnHeaders", [])
    labels = [h.get("name") for h in headers]
    rows = data.get("rows", [])

    parsed: List[ReportRow] = []
    for r in rows:
        # align values: dimensions first then metrics
        dim_count = sum(1 for h in headers if h.get("columnType") == "DIMENSION")
        dims = {}
        metrics = {}
        for i, val in enumerate(r):
            key = labels[i] if i < len(labels) else f"col_{i}"
            if i < dim_count:
                dims[key] = val
            else:
                metrics[key] = val
        parsed.append(ReportRow(metric_values=metrics, dimensions=dims))
    return parsed


def views_by_video(
    start_date: str,
    end_date: str,
    channel_id: str,
    access_token: Optional[str] = None,
    fetcher=_default_fetcher,
) -> List[Dict[str, Any]]:
    data = fetch_report(start_date, end_date, metrics="views", dimensions="video", channel_id=channel_id, access_token=access_token, fetcher=fetcher)
    rows = parse_simple_rows(data)
    out = []
    for r in rows:
        vid = r.dimensions.get("video") or r.dimensions.get("videoId") or None
        views = int(r.metric_values.get("views", 0))
        out.append({"video_id": vid, "views": views, **r.dimensions})
    return sorted(out, key=lambda x: x["views"], reverse=True)


def watchtime_by_video(
    start_date: str,
    end_date: str,
    channel_id: str,
    access_token: Optional[str] = None,
    fetcher=_default_fetcher,
) -> List[Dict[str, Any]]:
    data = fetch_report(start_date, end_date, metrics="estimatedMinutesWatched", dimensions="video", channel_id=channel_id, access_token=access_token, fetcher=fetcher)
    rows = parse_simple_rows(data)
    out = []
    for r in rows:
        vid = r.dimensions.get("video")
        watch = float(r.metric_values.get("estimatedMinutesWatched", 0))
        out.append({"video_id": vid, "watch_minutes": watch, **r.dimensions})
    return sorted(out, key=lambda x: x["watch_minutes"], reverse=True)


def traffic_sources(
    start_date: str,
    end_date: str,
    channel_id: str,
    access_token: Optional[str] = None,
    fetcher=_default_fetcher,
) -> List[Dict[str, Any]]:
    data = fetch_report(start_date, end_date, metrics="views", dimensions="insightTrafficSourceType", channel_id=channel_id, access_token=access_token, fetcher=fetcher)
    rows = parse_simple_rows(data)
    out = []
    for r in rows:
        source = r.dimensions.get("insightTrafficSourceType")
        views = int(r.metric_values.get("views", 0))
        out.append({"source": source, "views": views})
    return sorted(out, key=lambda x: x["views"], reverse=True)


def write_csv_report(rows: Iterable[Dict[str, Any]], path: str) -> None:
    rows = list(rows)
    if not rows:
        logger.info("No rows to write to CSV: %s", path)
        return
    with open(path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    logger.info("Wrote CSV report: %s", path)


def cli_generate_report():
    import argparse

    p = argparse.ArgumentParser(description="Generate YouTube analytics reports (views/watchtime/traffic)")
    p.add_argument("--channel-id", required=True)
    p.add_argument("--start-date", required=True, help="YYYY-MM-DD")
    p.add_argument("--end-date", required=True, help="YYYY-MM-DD")
    p.add_argument("--report", choices=["views","watchtime","traffic"], default="views")
    p.add_argument("--out", help="CSV output path", default=None)
    p.add_argument("--access-token", help="OAuth access token (or set env YT_ACCESS_TOKEN)")

    args = p.parse_args()
    token = args.access_token or os.environ.get("YT_ACCESS_TOKEN")

    if args.report == "views":
        rows = views_by_video(args.start_date, args.end_date, args.channel_id, access_token=token)
    elif args.report == "watchtime":
        rows = watchtime_by_video(args.start_date, args.end_date, args.channel_id, access_token=token)
    else:
        rows = traffic_sources(args.start_date, args.end_date, args.channel_id, access_token=token)

    if args.out:
        write_csv_report(rows, args.out)
    else:
        print(json.dumps(rows, indent=2, default=str))


if __name__ == "__main__":
    cli_generate_report()
