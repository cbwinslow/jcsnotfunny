"""MCP / API Social Publish Wrapper

This module provides a wrapper that can publish social posts either by
- calling an MCP-style agent server (managed agent endpoint) or
- calling a local/provider API function (X, Instagram, YouTube short, etc.).

Configuration via env vars or `configs/social_providers.yml` (example included).

Usage examples:
    python scripts/mcp_publish.py --mode mcp --endpoint https://mcp.example/agent/publish --platforms "x,instagram" --metadata metadata.json

Or local API mode:
    python scripts/mcp_publish.py --mode api --platforms "x,yt_short" --metadata metadata.json

The script returns JSON containing publish/schedule results.
"""
import argparse
import json
import os
import logging
import requests
from scripts.social_publish import render_post, schedule_post

logger = logging.getLogger('mcp_publish')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(ch)


def publish_via_mcp(endpoint, api_key, platforms, metadata, scheduled_for=None):
    payload = {'platforms': platforms, 'metadata': metadata}
    if scheduled_for:
        payload['scheduled_for'] = scheduled_for
    headers = {'Content-Type': 'application/json'}
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'
    logger.info('Calling MCP endpoint %s for platforms %s', endpoint, platforms)
    resp = requests.post(endpoint, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()


def publish_via_api(platforms, metadata, scheduled_for=None):
    results = {}
    for p in platforms:
        text = render_post(p, metadata)
        # For now, we schedule immediately (stub); integrate provider APIs here.
        r = schedule_post(p, metadata, when=scheduled_for)
        results[p] = {'rendered': text, 'scheduled': r}
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=('mcp','api'), default='api')
    parser.add_argument('--endpoint', help='MCP endpoint URL')
    parser.add_argument('--platforms', required=True)
    parser.add_argument('--metadata', required=True, help='JSON file with metadata keys expected by templates')
    parser.add_argument('--api-key', help='Optional API key for MCP')
    parser.add_argument('--schedule-at', help='ISO-8601 timestamp for scheduling')
    args = parser.parse_args()

    platforms = [p.strip() for p in args.platforms.split(',') if p.strip()]
    with open(args.metadata, 'r') as fh:
        metadata = json.load(fh)

    if args.mode == 'mcp':
        if not args.endpoint:
            raise SystemExit('MCP endpoint is required for mode=mcp')
        out = publish_via_mcp(
            args.endpoint,
            args.api_key or os.environ.get('MCP_API_KEY'),
            platforms,
            metadata,
            scheduled_for=args.schedule_at,
        )
    else:
        out = publish_via_api(platforms, metadata, scheduled_for=args.schedule_at)

    print(json.dumps(out, indent=2))

if __name__ == '__main__':
    main()
