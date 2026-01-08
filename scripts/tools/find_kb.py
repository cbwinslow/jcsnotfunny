#!/usr/bin/env python3
"""Small helper to query the knowledge_index.json for relevant doc paths.

Usage: python scripts/tools/find_kb.py <keyword>
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INDEX_PATH = ROOT / "docs" / "knowledge_base" / "knowledge_index.json"


def load_index():
    with open(INDEX_PATH, "r") as fh:
        return json.load(fh)


def find(keyword: str):
    keyword = keyword.lower()
    idx = load_index()
    matches = []
    for key, meta in idx.items():
        if keyword in key or keyword in meta.get("intent", ""):
            matches.append((key, meta["path"]))
    return matches


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: find_kb.py <keyword>")
        sys.exit(2)
    for k, p in find(sys.argv[1]):
        print(f"{k}: {p}")
