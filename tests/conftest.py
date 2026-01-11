# Test session fixtures and environment fixes
# Ensure the repository root is on sys.path so tests can import local modules like `scripts`.
import os
import sys

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Ensure google.* packages are importable early so tests that monkeypatch
# 'googleapiclient.discovery.build' do not fail when deriving import paths.
import importlib

for _mod in ("google.auth", "googleapiclient.discovery", "googleapiclient.http"):
    try:
        importlib.import_module(_mod)
    except Exception:
        # Best-effort pre-import to reduce ImportError during monkeypatch.resolve
        pass
