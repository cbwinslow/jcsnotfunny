import json
import os
import pathlib
import subprocess
import tempfile
from pathlib import Path


def test_auto_fix_creates_md_and_code_stubs(tmp_path: pathlib.Path) -> None:
    # Set up a small repo
    repo = tmp_path
    (repo / 'docs').mkdir()
    (repo / 'agents').mkdir()
    # create a markdown file referencing a missing doc and missing agent module
    md = repo / 'README.md'
    md.write_text('[missing-doc](docs/newpage.md)\n[missing-agent](agents/new_agent.py)')

    # run auto-fix in dry-run mode: should produce a report but not create files
    res = subprocess.run(["python3", "scripts/auto_fix_doc_links.py", "--root", str(repo), "--dry-run"], capture_output=True, text=True)
    assert res.returncode == 0
    report_path = repo / 'docs' / 'doc_link_fix_report.json'
    assert report_path.exists()
    report = json.loads(report_path.read_text())
    assert isinstance(report['actions'], list)

    # run in no-dry-run mode to actually create stubs
    res = subprocess.run(["python3", "scripts/auto_fix_doc_links.py", "--root", str(repo), "--no-dry-run"], capture_output=True, text=True)
    assert res.returncode == 0
    # files should have been created
    assert (repo / 'docs' / 'newpage.md').exists()
    assert (repo / 'agents' / 'new_agent.py').exists()


def test_auto_fix_skips_external_tokens(tmp_path: pathlib.Path) -> None:
    repo = tmp_path
    md = repo / 'README.md'
    md.write_text('[token](parsed_args)\n')

    res = subprocess.run(["python3", "scripts/auto_fix_doc_links.py", "--root", str(repo), "--dry-run"], capture_output=True, text=True)
    assert res.returncode == 0
    report = json.loads((repo / 'docs' / 'doc_link_fix_report.json').read_text())
    # parsed_args is a bare token and should be ignored by the checker; no unresolved items expected
    assert report['unresolved'] == []
