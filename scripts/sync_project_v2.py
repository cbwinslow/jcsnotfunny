#!/usr/bin/env python3
"""Sync Project V2 items into `.github/issues/` markdown files.

This script queries GitHub Projects V2 via GraphQL and ensures items with
attached Issues or DraftIssues are present in the repository under
`.github/issues/`. It is intentionally conservative (it only adds/updates files
for items that map to Issue/DraftIssue content). It can be run from CI and
will commit changes when run inside a workflow.

Usage:
  python scripts/sync_project_v2.py --project-number 20

Requirements: set env var `GITHUB_TOKEN` with a token that can read the project
and write repo contents (in CI, GITHUB_TOKEN is provided by Actions).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, Any

import requests

GITHUB_API = "https://api.github.com/graphql"

ISSUES_DIR = Path('.github/issues')
ISSUES_DIR.mkdir(parents=True, exist_ok=True)


def slugify(title: str) -> str:
    s = title.lower()
    s = re.sub(r"[^a-z0-9]+", '-', s)
    s = re.sub(r"^-+|-+$", '', s)
    return s[:80]


def write_issue_file(number: int | None, title: str, body: str) -> Path:
    if number:
        filename = f"{str(number).zfill(3)}-{slugify(title)}.md"
    else:
        filename = f"draft-{hashlib.sha1(title.encode()).hexdigest()[:8]}-{slugify(title)}.md"

    path = ISSUES_DIR / filename

    content = f"# {title}\n\n" + body.strip() + "\n"

    if path.exists():
        existing = path.read_text(encoding='utf-8')
        if existing.strip() == content.strip():
            print(f"No change for {filename}")
            return path

    path.write_text(content, encoding='utf-8')
    print(f"Wrote: {path}")
    return path


def run_graphql_query(token: str, query: str, variables: Dict[str, Any]):
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json',
    }
    resp = requests.post(GITHUB_API, json={'query': query, 'variables': variables}, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    if 'errors' in data:
        raise SystemExit(f"GraphQL errors: {data['errors']}")
    return data['data']


PROJECT_ITEMS_QUERY = """
query($owner: String!, $name: String!, $number: Int!, $after: String) {
  repository(owner: $owner, name: $name) {
    projectV2(number: $number) {
      id
      title
      items(first: 50, after: $after) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          content {
            __typename
            ... on Issue { number title body url }
            ... on DraftIssue { title body }
          }
        }
      }
    }
  }
}
"""


def sync_project_items(token: str, owner: str, repo: str, project_number: int) -> int:
    variables = {'owner': owner, 'name': repo, 'number': project_number, 'after': None}

    created = 0
    while True:
        data = run_graphql_query(token, PROJECT_ITEMS_QUERY, variables)
        project = data['repository']['projectV2']
        if not project:
            print(f"No projectV2 found for {owner}/{repo} #{project_number}")
            return created

        items = project['items']
        for node in items['nodes']:
            content = node.get('content')
            if not content:
                continue

            typename = content.get('__typename')
            if typename == 'Issue':
                number = content.get('number')
                title = content.get('title') or f'Issue #{number}'
                body = content.get('body') or ''
                write_issue_file(number, title, body)
                created += 1
            elif typename == 'DraftIssue':
                title = content.get('title') or 'Draft'
                body = content.get('body') or ''
                write_issue_file(None, title, body)
                created += 1
            else:
                print(f"Skipping content type: {typename}")

        page_info = items['pageInfo']
        if page_info['hasNextPage']:
            variables['after'] = page_info['endCursor']
            continue
        break

    return created


def parse_repo(repo_full: str):
    if '/' not in repo_full:
        raise SystemExit('GITHUB_REPOSITORY must be in owner/name format')
    owner, repo = repo_full.split('/', 1)
    return owner, repo


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--project-number', '-p', type=int, default=20, help='Project V2 number (e.g., 20)')
    parser.add_argument('--repo', default=os.environ.get('GITHUB_REPOSITORY'), help='Repository owner/name')
    args = parser.parse_args()

    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        print('GITHUB_TOKEN is required')
        sys.exit(1)

    owner, repo = parse_repo(args.repo)

    created = sync_project_items(token, owner, repo, args.project_number)
    print(f"Processed {created} items from project #{args.project_number}")


if __name__ == '__main__':
    main()
