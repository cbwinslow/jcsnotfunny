"""Collect analytics, write CSV reports, upload to R2 and push Prometheus metrics.

Features:
- Uses youtube_analytics helpers to collect views/watchtime/traffic
- Writes CSV files and uploads to Cloudflare R2 (if configured)
- Optionally pushes summary metrics to Prometheus Pushgateway
- Designed to be used as a cron job, scheduled workflow, or a small service
"""
from __future__ import annotations

import datetime
import logging
import os
from typing import Optional

# prometheus_client is optional for local tests; import lazily when needed. We'll try to import in the push block and handle absence gracefully.

from scripts.integrations import youtube_analytics
from scripts.integrations.r2_uploader import upload_text, R2UploadError

logger = logging.getLogger("analytics_collector")
logging.basicConfig(level=logging.INFO)


def _today_range(days: int = 7) -> tuple[str, str]:
    end = datetime.date.today()
    start = end - datetime.timedelta(days=days)
    return start.isoformat(), end.isoformat()


def collect_and_store(
    channel_id: str,
    r2_bucket: Optional[str] = None,
    r2_prefix: Optional[str] = None,
    pushgateway: Optional[str] = None,
    access_token: Optional[str] = None,
    days: int = 7,
) -> dict:
    start_date, end_date = _today_range(days)

    logger.info("Collecting reports for %s to %s", start_date, end_date)

    # Views report
    views = youtube_analytics.views_by_video(start_date, end_date, channel_id=channel_id, access_token=access_token)
    watch = youtube_analytics.watchtime_by_video(start_date, end_date, channel_id=channel_id, access_token=access_token)
    traffic = youtube_analytics.traffic_sources(start_date, end_date, channel_id=channel_id, access_token=access_token)

    # Prepare CSV payloads
    import io
    import csv

    def rows_to_csv_bytes(rows, fieldnames):
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)
        return buf.getvalue()

    reports = {}

    if views:
        csv_txt = rows_to_csv_bytes(views, fieldnames=list(views[0].keys()))
        reports['views.csv'] = csv_txt

    if watch:
        csv_txt = rows_to_csv_bytes(watch, fieldnames=list(watch[0].keys()))
        reports['watchtime.csv'] = csv_txt

    if traffic:
        csv_txt = rows_to_csv_bytes(traffic, fieldnames=list(traffic[0].keys()))
        reports['traffic.csv'] = csv_txt

    # Upload to R2 (if configured)
    uploaded = []
    if r2_bucket:
        for name, txt in reports.items():
            key = f"{r2_prefix.rstrip('/')}/" + name if r2_prefix else name
            try:
                upload_text(r2_bucket, key, txt, content_type='text/csv')
                uploaded.append(key)
            except R2UploadError as e:
                logger.error("Failed to upload %s: %s", name, e)

    # Push summary metrics to Pushgateway if configured
    pushed = False
    if pushgateway:
        try:
            from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
        except Exception:
            logger.warning("prometheus_client not installed; skipping push to Pushgateway")
            pushed = False
        else:
            registry = CollectorRegistry()
            g_views = Gauge('yt_total_views', 'Total views in the period', registry=registry)
            g_watch = Gauge('yt_total_watch_minutes', 'Total watch minutes in the period', registry=registry)

            total_views = sum(r.get('views', 0) for r in views) if views else 0
            total_watch = sum(r.get('watch_minutes', 0) for r in watch) if watch else 0

            g_views.set(total_views)
            g_watch.set(total_watch)

            try:
                # call module-level wrapper so tests can monkeypatch it
                push_to_gateway(pushgateway, job=f"youtube_{channel_id}", registry=registry)
                pushed = True
            except Exception as e:
                logger.exception("Failed to push metrics to Pushgateway: %s", e)
                pushed = False

    # Return summary
    return {
        'start_date': start_date,
        'end_date': end_date,
        'uploaded': uploaded,
        'pushed': pushed,
        'counts': {'views_rows': len(views), 'watch_rows': len(watch), 'traffic_rows': len(traffic)}
    }


def push_to_gateway(pushgateway_url: str, job: str, registry) -> None:
    """Wrapper around prometheus_client.push_to_gateway so it can be mocked in tests."""
    try:
        from prometheus_client import push_to_gateway as _push
    except Exception:
        raise RuntimeError("prometheus_client is required to push metrics to Pushgateway")
    return _push(pushgateway_url, job=job, registry=registry)


def cli_run():
    import argparse

    p = argparse.ArgumentParser(description='Collect YouTube analytics and store/push metrics')
    p.add_argument('--channel-id', required=True)
    p.add_argument('--r2-bucket', help='Cloudflare R2 bucket name (optional)')
    p.add_argument('--r2-prefix', help='Prefix path within bucket', default='youtube_reports')
    p.add_argument('--pushgateway', help='Prometheus Pushgateway URL (optional)')
    p.add_argument('--access-token', help='YouTube access token (optional, env YT_ACCESS_TOKEN)')
    p.add_argument('--days', type=int, default=7)

    args = p.parse_args()
    token = args.access_token or os.environ.get('YT_ACCESS_TOKEN')

    res = collect_and_store(
        args.channel_id,
        r2_bucket=args.r2_bucket,
        r2_prefix=args.r2_prefix,
        pushgateway=args.pushgateway,
        access_token=token,
        days=args.days,
    )
    print(res)


if __name__ == '__main__':
    cli_run()
