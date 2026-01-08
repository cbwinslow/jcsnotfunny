import os
from pathlib import Path
import shutil
import pytest

from run_swarm_on_github_issues import GitHubIssueLoader


def test_load_issues(tmp_path, monkeypatch):
    issues_dir = tmp_path / "issues"
    issues_dir.mkdir()

    # Create a sample issue file
    content = "# Sample Issue\n\nThis is a test issue.\n\nLabels: area/editing,priority/high"
    (issues_dir / "001-sample-issue.md").write_text(content, encoding='utf-8')

    loader = GitHubIssueLoader(issues_dir=str(issues_dir))
    issues = loader.load_all_issues()

    assert len(issues) == 1
    issue = issues[0]
    assert issue['title'] == 'Sample Issue'
    assert 'content_distribution' in issue['labels'] or isinstance(issue['labels'], list)


def test_priority_and_complexity(tmp_path):
    issues_dir = tmp_path / "issues"
    issues_dir.mkdir()

    long_content = "# Complex Issue\n\n" + ("integration " * 500)
    (issues_dir / "002-complex.md").write_text(long_content, encoding='utf-8')

    loader = GitHubIssueLoader(issues_dir=str(issues_dir))
    issues = loader.load_all_issues()

    assert issues[0]['estimated_complexity'] in ('medium', 'high')
