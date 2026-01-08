import os
from datetime import datetime, timedelta, timezone

import pytest

from scripts.social_workflows import (
    InMemoryPostStore,
    MockProviderClient,
    SocialWorkflow,
    build_endpoint,
    check_release_timing,
    load_dotenv,
    normalize_platform,
    validate_post_delivery,
)


def test_load_dotenv_respects_override(tmp_path, monkeypatch):
    env_path = tmp_path / ".env"
    env_path.write_text("SOCIAL_TEST_KEY=from_file\n")
    monkeypatch.setenv("SOCIAL_TEST_KEY", "from_env")
    loaded = load_dotenv(str(env_path), override=False)
    assert loaded == {}
    loaded = load_dotenv(str(env_path), override=True)
    assert os.environ["SOCIAL_TEST_KEY"] == "from_file"
    assert loaded["SOCIAL_TEST_KEY"] == "from_file"


def test_normalize_platform_aliases():
    assert normalize_platform("Twitter") == "x"
    assert normalize_platform("YT") == "youtube"


def test_build_endpoint_requires_params():
    endpoint = build_endpoint("x", "post")
    assert endpoint.endswith("/tweets")
    with pytest.raises(KeyError):
        build_endpoint("instagram", "post")


def test_mock_provider_publish_and_schedule():
    store = InMemoryPostStore()
    client = MockProviderClient(store=store)
    post = client.post_text("x", "Hello world")
    scheduled = client.schedule_text("x", "Later post", "2024-01-02T00:00:00+00:00")
    assert post.status == "published"
    assert scheduled.status == "scheduled"
    client.mark_published(scheduled.id, "2024-01-02T00:00:05+00:00")
    recent = client.fetch_recent_posts("x", limit=5)
    ids = {item.id for item in recent}
    assert post.id in ids
    assert scheduled.id in ids


def test_social_workflow_publish_schedules():
    client = MockProviderClient()
    workflow = SocialWorkflow(provider_client=client, load_env=False)
    metadata = {
        "title": "Ep 1",
        "guest": "Jared",
        "ep_link": "https://example.com/ep1",
        "date": "2024-01-01",
    }
    results = workflow.publish(["x"], metadata, scheduled_for="2024-01-02T00:00:00+00:00")
    assert "x" in results
    assert "scheduled" in results["x"]
    assert results["x"]["scheduled"]["status"] == "scheduled"
    assert "rendered" in results["x"]


def test_validate_post_delivery_on_time():
    client = MockProviderClient()
    post = client.post_text("x", "Hello world")
    report = validate_post_delivery(
        platform="x",
        posts=[post],
        expected_text="hello world",
        scheduled_for=post.published_at,
        tolerance_seconds=60,
    )
    assert report.found is True
    assert report.matched_text is True
    assert report.timing_status == "on_time"


def test_validate_post_delivery_missing():
    report = validate_post_delivery(
        platform="x",
        posts=[],
        expected_text="missing post",
    )
    assert report.found is False
    assert "post_not_found" in report.errors


def test_check_release_timing_early_late():
    scheduled = datetime(2024, 1, 1, tzinfo=timezone.utc)
    late_published = scheduled + timedelta(seconds=400)
    delta, status = check_release_timing(scheduled, late_published, tolerance_seconds=300)
    assert status == "late"
    assert delta == 400
    early_published = scheduled - timedelta(seconds=400)
    delta, status = check_release_timing(scheduled, early_published, tolerance_seconds=300)
    assert status == "early"
    assert delta == -400
