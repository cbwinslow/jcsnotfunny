#!/usr/bin/env python3
"""Normalize links that include file:line references in Markdown files.

Replaces occurrences like `(path/to/file.js:123)` with `(path/to/file.js)` inside Markdown link targets.

Usage: python scripts/normalize_file_line_links.py --root . --exclude .git,node_modules
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable

FILE_LINE_RE = re.compile(r"\(([^)]+?\.[a-zA-Z0-9_-]+):\d+(?:[:]\d+)?\)")


def find_markdown_files(root: Path, exclude: Iterable[str] = None):
    exclude = set(exclude or [])
    for p in root.rglob("*.md"):
        if any(part in exclude for part in p.parts):
            continue
        yield p


def normalize_file(path: Path) -> bool:
    text = path.read_text()
    new_text = FILE_LINE_RE.sub(lambda m: f"({m.group(1)})", text)
    if new_text != text:
        path.write_text(new_text)
        return True
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path('.'))
    parser.add_argument("--exclude", type=str, default='.git,node_modules,website/.next')
    args = parser.parse_args()

    exclude = [p.strip() for p in args.exclude.split(',') if p.strip()]
    root = args.root.resolve()

    changed = []
    for md in find_markdown_files(root, exclude):
        if normalize_file(md):
            changed.append(md)

    if changed:
        print("Normalized file:line links in:")
        for p in changed:
            print(f" - {p.relative_to(root)}")
    else:
        print("No file:line links found to normalize.")


if __name__ == '__main__':
    main()
