#!/usr/bin/env python3
"""Check Markdown files for broken internal links.

Usage:
    python scripts/doc_link_checker.py --root . --exclude .git,.venv,node_modules

Outputs non-zero exit code when broken links found (except ones in whitelist file).
"""
from __future__ import annotations

import argparse
import os
import re
from pathlib import Path
from typing import Iterable, List, Tuple

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def find_markdown_files(root: Path, exclude: Iterable[str] = None) -> List[Path]:
    exclude = set(exclude or [])
    md_files = []
    for p in root.rglob("*.md"):
        if any(part in exclude for part in p.parts):
            continue
        md_files.append(p)
    return md_files


def extract_links(md_text: str) -> List[str]:
    return [m.group(1).strip() for m in LINK_RE.finditer(md_text)]


def is_external(link: str) -> bool:
    return link.startswith("http://") or link.startswith("https://") or link.startswith("mailto:")


def check_internal_link(md_file: Path, link: str, root: Path) -> Tuple[bool, str]:
    """Return (ok, reason). Handles file:line anchors and ignores non-file schemes (e.g., mdc:/, url, parsed_args).

    Rules:
    - If the link is an anchor only ("#foo"), it's considered OK.
    - If the link uses a non-file scheme (contains a leading word and colon, like 'mdc:/...'), it's ignored as non-file reference.
    - If the link contains a trailing ':<digits>' (e.g. 'file.js:123'), the path portion before the first ':' is checked for existence.
    - Otherwise, the resolver behaves as before (relative to doc or repo root for absolute paths).
    """
    # strip anchor
    link_path = link.split('#', 1)[0]

    # empty link (just an anchor) — OK
    if link_path == '':
        return True, ''

    # ignore non-file schemes like mdc:/, schema:, url, parsed_args, etc.
    if re.match(r'^[a-zA-Z0-9_-]+:', link_path):
        # treat as non-file scheme (not checkable by file existence)
        return True, 'non-file-scheme'

    # If link contains file:line (e.g., path/to/file.js:123 or file.py:45:2), try to resolve the file part
    m = re.match(r'^(?P<path>.+?):\d+(?:[:]\d+)?$', link_path)
    if m:
        path_only = m.group('path')
        # treat like a normal path relative to md file
        if path_only.startswith('/'):
            target = (root / path_only.lstrip('/')).resolve()
        else:
            target = (md_file.parent / path_only).resolve()
        if target.exists():
            return True, ''
        # fall through to check original (in case colon is part of a filename on exotic systems)

    # absolute or relative path handling
    if link_path.startswith('/'):
        target = (root / link_path.lstrip('/')).resolve()
    else:
        target = (md_file.parent / link_path).resolve()

    if target.exists():
        return True, ''
    else:
        return False, f"target not found: {target}"


def load_whitelist(path: Path) -> List[str]:
    if not path.exists():
        return []
    return [line.strip() for line in path.read_text().splitlines() if line.strip() and not line.strip().startswith('#')]


def find_broken_links(root: Path, exclude: Iterable[str] = None) -> List[Tuple[Path, str, str]]:
    md_files = find_markdown_files(root, exclude)
    broken = []
    for md in md_files:
        try:
            text = md.read_text()
        except Exception as e:
            broken.append((md, '<file-read>', f'read error: {e}'))
            continue
        links = extract_links(text)
        for link in links:
            if is_external(link):
                continue
            ok, reason = check_internal_link(md, link, root)
            if not ok:
                broken.append((md, link, reason))
    return broken


def main():
    parser = argparse.ArgumentParser(description='Check Markdown links for broken internal references')
    parser.add_argument('--root', type=Path, default=Path('.'), help='Repo root to scan')
    parser.add_argument('--exclude', type=str, default='.git,node_modules,website/.next', help='Comma-separated list of path parts to exclude')
    parser.add_argument('--whitelist', type=Path, default=Path('docs/doc_link_whitelist.txt'), help='Path to whitelist file')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    exclude = [p.strip() for p in args.exclude.split(',') if p.strip()]
    root = args.root.resolve()

    broken = find_broken_links(root, exclude)

    whitelist = load_whitelist(args.whitelist)
    filtered = []
    for md, link, reason in broken:
        key = f"{md.relative_to(root)} -> {link}"
        if key in whitelist:
            if args.verbose:
                print(f"Whitelisted broken link: {key} ({reason})")
            continue
        filtered.append((md, link, reason))

    if filtered:
        print('\nBroken internal Markdown links found:')
        for md, link, reason in filtered:
            print(f" - {md.relative_to(root)} -> {link} ({reason})")
        print('\nHint: to whitelist a link, add a line to docs/doc_link_whitelist.txt with the form:')
        print('  path/to/file.md -> relative/path/to/target.md#anchor')
        raise SystemExit(2)

    print('No broken internal Markdown links found (excluding whitelist).')


if __name__ == '__main__':
    main()
