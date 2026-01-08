from scripts.social_scheduler import build_schedule


def test_build_schedule_offsets():
    schedule = build_schedule(
        platforms=["x", "instagram"],
        base_time="2024-01-02T18:00:00+00:00",
        offsets_minutes={"instagram": 15},
    )
    assert schedule[0].platform == "x"
    assert schedule[1].platform == "instagram"
    assert schedule[1].scheduled_for != schedule[0].scheduled_for
