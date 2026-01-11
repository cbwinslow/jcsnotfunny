# Test session fixtures and environment fixes
# Ensure google.* packages are importable early so tests that monkeypatch
# 'googleapiclient.discovery.build' do not fail when deriving import paths.
try:
    import google.auth  # noqa: F401
except Exception:
    # If google.auth is not available, allow tests to continue; tests that
    # require it will fail later - in CI we expect the dependency to be installed.
    pass

try:
    import googleapiclient.discovery  # noqa: F401
except Exception:
    # Allow remaining tests to run; monkeypatch resolution may still try to
    # import and can surface errors, but pre-importing helps in many cases.
    pass
