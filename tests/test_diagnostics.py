from scripts.diagnostics import check_stream_endpoints, run_snapshot, _parse_rtmp_url


def test_parse_rtmp_url_defaults():
    host, port, scheme = _parse_rtmp_url("rtmps://example.com/live")
    assert host == "example.com"
    assert port == 443
    assert scheme == "rtmps"


def test_check_stream_endpoints_offline():
    urls = {"youtube": "rtmps://example.com/live"}
    results = check_stream_endpoints(urls, live=False)
    assert results[0].status == "ok"
    assert "offline" in results[0].details


def test_check_stream_endpoints_live():
    def fake_connector(host, port):
        return 120.0

    urls = {"youtube": "rtmps://example.com/live"}
    results = check_stream_endpoints(urls, live=True, connector=fake_connector)
    assert results[0].status == "ok"
    assert results[0].value == 120.0


def test_run_snapshot_offline(monkeypatch):
    monkeypatch.setattr("scripts.diagnostics.load_settings", lambda: None)
    snapshot = run_snapshot(live=False)
    assert "timestamp" in snapshot
    assert "disk" in snapshot
    assert "stream_endpoints" in snapshot


def test_run_checks_basic(monkeypatch):
    # Ensure basic env checks run without error
    from scripts.diagnostics.check_env import run_checks
    report, critical = run_checks()
    assert 'binaries' in report
    assert 'python' in report
    assert 'packages' in report
    assert isinstance(critical, bool)
