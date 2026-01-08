from scripts.seo_tools import build_jsonld_episode, build_seo_package


def test_build_jsonld_episode():
    jsonld = build_jsonld_episode(
        title="Ep 1",
        description="Summary",
        url="https://example.com/ep1",
        episode_number="1",
        guest_name="Guest",
    )
    assert jsonld["@type"] == "PodcastEpisode"
    assert jsonld["episodeNumber"] == "1"
    assert jsonld["actor"]["name"] == "Guest"


def test_build_seo_package():
    seo = build_seo_package(
        title="Ep 2",
        summary="Summary",
        keywords=["podcast"],
        canonical_url="https://example.com/ep2",
        og_image_url="https://example.com/ep2.png",
    )
    payload = seo.as_dict()
    assert payload["title"] == "Ep 2"
    assert payload["jsonld"]["url"] == "https://example.com/ep2"
