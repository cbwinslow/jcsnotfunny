from scripts.automation_runner import run_automation


def test_run_automation_basic(tmp_path):
    tools_config = {
        "thumbnail_agent": {"enabled": True, "output": {"out_dir": str(tmp_path / "thumbs")}},
        "seo_assistant": {"enabled": True, "output_dir": str(tmp_path / "seo"), "keywords_limit": 5},
        "social_scheduler": {"enabled": True, "default_offsets_minutes": {"x": 0}},
        "archive_uploader": {"enabled": False},
    }
    metadata = {
        "title": "Ep 1",
        "slug": "ep1",
        "summary": "Summary text",
        "platforms": ["x"],
    }
    report_path = tmp_path / "report.json"
    results = run_automation(
        metadata=metadata,
        base_time="2024-01-02T00:00:00+00:00",
        schedule_offsets={"x": 0},
        tools_config=tools_config,
        report_path=str(report_path),
    )
    assert "thumbnail" in results
    assert "seo" in results
    assert "schedule" in results
    assert report_path.exists()
