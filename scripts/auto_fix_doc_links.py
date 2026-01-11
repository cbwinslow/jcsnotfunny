#!/usr/bin/env python3
"""Auto-fix broken internal Markdown links conservatively.

Conservative rules:
- Normalize file:line links (use existing script) before attempting fixes.
- For missing Markdown targets inside the repo: create a small stub `docs/*.md` with a TODO note.
- For missing code files under `agents/`, `mcp-servers/`: create a minimal stub file (module-level docstring and minimal class/function).
- Never generate content beyond a tiny placeholder. Always open a PR for review (no auto-merge unless explicitly enabled).

Usage:
  python scripts/auto_fix_doc_links.py --root . --dry-run
  python scripts/auto_fix_doc_links.py --root . --dry-run --report report.json
  python scripts/auto_fix_doc_links.py --root . --no-dry-run --create-pr --branch-name auto/fix-doc-links

The script uses existing `scripts/doc_link_checker.py` functions where possible to detect broken links.
"""
from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

# Import helpers from the doc checker
sys.path.insert(0, str(Path(__file__).resolve().parent))
from doc_link_checker import find_broken_links, load_whitelist  # type: ignore


@dataclass
class FixAction:
    source: str
    link: str
    action: str
    target: str


def run_normalize(root: Path, exclude: List[str]) -> None:
    # call the normalize script to rewrite file:line links to file
    script = Path(__file__).with_name("normalize_file_line_links.py")
    if script.exists():
        subprocess.run([sys.executable, str(script), "--root", str(root), "--exclude", ",".join(exclude)], check=True)


def is_markdown_link(link: str) -> bool:
    return link.lower().endswith(".md")


def is_code_link(link: str) -> bool:
    for ext in (".py", ".js", ".ts", ".tsx", ".sh"):
        if link.lower().split('#', 1)[0].endswith(ext):
            return True
    return False


def create_md_stub(target_path: Path, source: Path) -> None:
    if target_path.exists():
        return
    target_path.parent.mkdir(parents=True, exist_ok=True)
    title = target_path.stem.replace('-', ' ').replace('_', ' ').title()
    content = f"# {title}\n\nAuto-generated placeholder created on {datetime.utcnow().isoformat()}Z to satisfy a link from `{source}`.\n\nTODO: expand this document with real content.\n"
    target_path.write_text(content)


def create_code_stub(target_path: Path, source: Path) -> None:
    if target_path.exists():
        return
    target_path.parent.mkdir(parents=True, exist_ok=True)
    if target_path.suffix == '.py':
        content = f"\"\"\"Auto-generated stub created on {datetime.utcnow().isoformat()}Z to satisfy a doc link from {source}\n\nPlease replace with a real implementation.\n\"\"\"\n\nclass Placeholder:\n    \"\"\"Placeholder class\"\"\"\n    def __init__(self):\n        pass\n"
        target_path.write_text(content)
    else:
        # simple generic stub for other languages
        target_path.write_text(f"// Auto-generated placeholder created to satisfy a doc link from {source}\n")


def git_commit_and_branch(root: Path, branch_name: str, commit_message: str, dry_run: bool) -> None:
    if dry_run:
        print("[dry-run] would create branch, commit files")
        return

    subprocess.run(["git", "checkout", "-b", branch_name], cwd=root, check=True)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    subprocess.run(["git", "commit", "-m", commit_message], cwd=root, check=True)
    subprocess.run(["git", "push", "--set-upstream", "origin", branch_name], cwd=root, check=True)


def create_pr(branch_name: str, title: str, body: str, dry_run: bool) -> str:
    if dry_run:
        print(f"[dry-run] would create PR {title}")
        return ""
    # create PR via gh
    cmd = [
        "gh",
        "pr",
        "create",
        "--title",
        title,
        "--body",
        body,
        "--head",
        branch_name,
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        # try to extract PR url
        out = res.stdout.strip()
        return out.splitlines()[-1]
    else:
        print("Failed to create PR:", res.stderr)
        return ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path('.'), help="Repo root")
    parser.add_argument("--exclude", type=str, default='.git,node_modules,website/.next')
    parser.add_argument("--whitelist", type=Path, default=Path('docs/doc_link_whitelist.txt'))
    parser.add_argument("--dry-run", dest='dry_run', action='store_true', default=True)
    parser.add_argument("--no-dry-run", dest='dry_run', action='store_false')
    parser.add_argument("--branch-name", type=str, default='auto/fix-doc-links')
    parser.add_argument("--commit-message", type=str, default='chore(docs): auto-fix missing doc links (stub)')
    parser.add_argument("--create-pr", action='store_true', default=False)
    parser.add_argument("--auto-merge", action='store_true', default=False, help='Attempt to auto-merge PR if checks pass (use with care)')
    parser.add_argument("--report", type=Path, default=Path('docs/doc_link_fix_report.json'))
    args = parser.parse_args()

    root = args.root.resolve()
    exclude = [p.strip() for p in args.exclude.split(',') if p.strip()]

    # Step 0: normalize file:line links
    run_normalize(root, exclude)

    # Step 1: find broken links
    broken = find_broken_links(root, exclude)
    whitelist = load_whitelist(args.whitelist)

    actions: List[FixAction] = []
    unresolved: List[Tuple[str, str, str]] = []

    for md, link, reason in broken:
        key = f"{md.relative_to(root)} -> {link}"
        if key in whitelist:
            continue

        # consider fixing candidates
        link_path = link.split('#', 1)[0]
        if link_path == '':
            # anchor only; skip
            continue

        # skip non-file schemes and bare tokens
        if link_path.split(':', 1)[0].isalpha() and ':' in link_path:
            unresolved.append((str(md.relative_to(root)), link, reason))
            continue
        if ("/" not in link_path) and ("." not in link_path):
            unresolved.append((str(md.relative_to(root)), link, reason))
            continue

        # determine absolute candidate path
        if link_path.startswith('/'):
            target = (root / link_path.lstrip('/')).resolve()
        else:
            target = (md.parent / link_path).resolve()

        if target.exists():
            # transient reason; skip
            continue

        if is_markdown_link(link_path):
            # create doc stub
            create_md_stub(target, md)
            actions.append(FixAction(str(md.relative_to(root)), link, 'create_md_stub', str(target.relative_to(root))))
        elif is_code_link(link_path):
            # likely a code file; only auto-create under trusted directories
            if 'agents' in str(target) or 'mcp-servers' in str(target) or 'scripts' in str(target):
                create_code_stub(target, md)
                actions.append(FixAction(str(md.relative_to(root)), link, 'create_code_stub', str(target.relative_to(root))))
            else:
                unresolved.append((str(md.relative_to(root)), link, reason))
        else:
            # unknown — leave for triage
            unresolved.append((str(md.relative_to(root)), link, reason))

    report = {
        'root': str(root),
        'dry_run': args.dry_run,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'actions': [asdict(a) for a in actions],
        'unresolved': unresolved,
    }

    # Ensure report path is anchored under the repo root when a relative path is provided.
    if not args.report.is_absolute():
        args.report = root / args.report

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2))

    if not actions:
        print('No auto-fix actions taken.')
    else:
        print(f"Planned {len(actions)} actions:")
        for a in actions:
            print(f" - {a.action}: {a.target} (from {a.source} -> {a.link})")

    # If not dry-run, commit and create PR
    if actions and not args.dry_run:
        git_commit_and_branch(root, args.branch_name, args.commit_message, dry_run=False)
        if args.create_pr:
            pr_url = create_pr(args.branch_name, "chore(docs): auto-fix doc links", json.dumps(report, indent=2), dry_run=False)
            print('PR created:', pr_url)
            if args.auto_merge and pr_url:
                print('[auto-merge] Auto-merge requested but not implemented in script; configure your CI to auto-merge safely.')

    # Exit code: 0 unless there are unresolved issues and we are not dry-run? We'll return 0 but include report for manual triage.
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
