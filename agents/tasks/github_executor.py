"""Helper to propose changes to GitHub: post comments or create draft PRs in propose-only mode."""
import os
import logging
from typing import Dict, Any

import requests

logger = logging.getLogger('github_executor')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(ch)


class GitHubProposer:
    def __init__(self, owner: str = None, repo: str = None, token: str = None):
        self.owner = owner or os.environ.get('GITHUB_REPO_OWNER')
        self.repo = repo or os.environ.get('GITHUB_REPO')
        self.token = token or os.environ.get('GITHUB_TOKEN')
        self.api_base = f'https://api.github.com/repos/{self.owner}/{self.repo}' if self.owner and self.repo else None

    def post_comment(self, issue_number: int, body: str) -> Dict[str, Any]:
        if not self.api_base:
            raise RuntimeError('GitHubProposer not configured with owner/repo')
        url = f'{self.api_base}/issues/{issue_number}/comments'
        headers = {'Authorization': f'token {self.token}', 'Accept': 'application/vnd.github+json'}
        resp = requests.post(url, json={'body': body}, headers=headers, timeout=10)
        resp.raise_for_status()
        logger.info('Posted comment to issue #%s', issue_number)
        return resp.json()

    def create_draft_pr(self, head: str, base: str, title: str, body: str) -> Dict[str, Any]:
        if not self.api_base:
            raise RuntimeError('GitHubProposer not configured with owner/repo')
        url = f'{self.api_base}/pulls'
        headers = {'Authorization': f'token {self.token}', 'Accept': 'application/vnd.github+json'}
        payload = {'title': title, 'head': head, 'base': base, 'body': body, 'draft': True}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        resp.raise_for_status()
        logger.info('Created draft PR: %s', title)
        return resp.json()
