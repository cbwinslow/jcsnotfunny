"""Fetcher that retrieves actionable tasks from GitHub Project v2 or Issues.
This is a minimal dev implementation with a local-file fallback for ease of testing.
"""
import os
import json
import logging
from typing import List, Dict

logger = logging.getLogger('github_fetcher')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(ch)


class GitHubFetcher:
    def __init__(self, project_id: str | None = None, token: str | None = None, dev_fallback: str | None = None):
        self.project_id = project_id or os.environ.get('GITHUB_PROJECT_ID')
        self.token = token or os.environ.get('GITHUB_TOKEN')
        self.dev_fallback = dev_fallback or os.environ.get('GITHUB_FETCHER_FALLBACK')

    def fetch_tasks(self) -> List[Dict]:
        # If a fallback JSON file exists, read it and return list of tasks
        if self.dev_fallback and os.path.exists(self.dev_fallback):
            logger.info('Using local fallback tasks file %s', self.dev_fallback)
            with open(self.dev_fallback, 'r') as fh:
                data = json.load(fh)
            return data.get('items', [])
        # For production, we would call GitHub GraphQL API here using token
        # Minimal safe fallback: return empty list
        logger.info('No fallback found and no live fetch configured; returning empty task list')
        return []
