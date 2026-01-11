#!/usr/bin/env python3
"""Check staged files for media (images, videos, pdfs) and exit non-zero if found.

Use as a pre-commit hook: `python scripts/check_no_media_in_commit.py` or add it to .pre-commit-config.yaml
"""
import re
import subprocess
import sys

PATTERN = re.compile(r"(^downloads/|^exports/|\.(png|jpg|jpeg|gif|mp4|webm|mov|pdf)$)", re.I)

def staged_files():
    res = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"], capture_output=True, text=True)
    if res.returncode != 0:
        print("Failed to list staged files", file=sys.stderr)
        sys.exit(2)
    return [l.strip() for l in res.stdout.splitlines() if l.strip()]


def main():
    files = staged_files()
    offending = [f for f in files if PATTERN.search(f)]
    if offending:
        print("Refusing to commit: the following staged files appear to be media or large artifacts:")
        for f in offending:
            print("  - ", f)
        print("\nPlease remove them from the commit, store them externally, and re-run the commit.")
        sys.exit(1)
    print("No media artifacts staged.")

if __name__ == '__main__':
    main()
