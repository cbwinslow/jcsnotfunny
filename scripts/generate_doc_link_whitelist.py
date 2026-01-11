#!/usr/bin/env python3
"""Generate/update docs/doc_link_whitelist.txt from a run of scripts/doc_link_checker.py

This script appends any currently-detected broken link lines (normalized) to the whitelist file
so tests can enforce *no new* broken links while we iteratively fix the baseline.
"""
import os
import re
import subprocess

ROOT = os.getcwd()
EXCLUDE = ".git,venv,.venv,node_modules,website/.next"
WHITELIST = os.path.join(ROOT, "docs", "doc_link_whitelist.txt")

res = subprocess.run(["python3", "scripts/doc_link_checker.py", "--root", ROOT, "--exclude", EXCLUDE, "--verbose"], capture_output=True, text=True)
out = res.stdout + "\n" + res.stderr

# match lines like: - FILE -> TARGET (target not found: ...)
pattern = re.compile(r"^-\s*(?P<link>.+?->.+?)(?:\s*\(target not found: .+\))?\s*$")
found = []
for ln in out.splitlines():
    m = pattern.match(ln.strip())
    if m:
        found.append(m.group('link').strip())

if not found:
    print("No broken links found (or none parsed).")
    raise SystemExit(0)

# Read existing whitelist
existing = set()
if os.path.exists(WHITELIST):
    with open(WHITELIST, "r") as f:
        for ln in f:
            ln = ln.strip()
            if not ln or ln.startswith('#'):
                continue
            existing.add(ln)

new = [ln for ln in found if ln not in existing]
if not new:
    print("Whitelist already contains current broken links.")
    raise SystemExit(0)

with open(WHITELIST, "a") as f:
    for ln in new:
        f.write(ln + "\n")

print(f"Appended {len(new)} new links to {WHITELIST}.")
