from scripts.thumbnail_agent import extract_keywords, generate_thumbnail_brief


def test_extract_keywords_basic():
    text = "Jared talks comedy, comedy tours, and podcast production."
    keywords = extract_keywords(text, limit=3)
    assert "comedy" in keywords


def test_generate_thumbnail_brief_payload(tmp_path):
    transcript = tmp_path / "transcript.txt"
    transcript.write_text("This is a test transcript about touring and comedy.")
    out_path = tmp_path / "brief.json"
    payload = generate_thumbnail_brief(
        title="Episode Title",
        summary="A bold summary.",
        transcript_path=str(transcript),
        out_path=str(out_path),
    )
    assert "prompt" in payload
    assert out_path.exists()
