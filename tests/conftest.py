# Test session fixtures and environment fixes
# Ensure google.* packages are importable early so tests that monkeypatch
# 'googleapiclient.discovery.build' do not fail when deriving import paths.
import importlib

for _mod in ("google.auth", "googleapiclient.discovery", "googleapiclient.http"):
    try:
        importlib.import_module(_mod)
    except Exception:
        # Best-effort pre-import to reduce ImportError during monkeypatch.resolve
        pass
