from urllib.parse import parse_qs, urlparse

from app.rankings.crawler import MUSINSA_RANKING_URL, build_ranking_url


def test_build_ranking_url_contains_base_url():
    url = build_ranking_url(
        gender="A",
        age_band="AGE_BAND_ALL",
        include_soldout=True,
    )

    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

    assert base_url == MUSINSA_RANKING_URL


def test_build_ranking_url_maps_query_params():
    url = build_ranking_url(
        gender="F",
        age_band="AGE_BAND_20",
        include_soldout=False,
    )

    query_params = parse_qs(urlparse(url).query)

    assert query_params["gf"] == ["F"]
    assert query_params["ageBand"] == ["AGE_BAND_20"]
    assert query_params["soldOut"] == ["false"]
    assert query_params["storeCode"] == ["sneaker"]
    assert query_params["sectionId"] == ["256"]
    assert query_params["categoryCode"] == ["103000"]
