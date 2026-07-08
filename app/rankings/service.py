from playwright.sync_api import Error as PlaywrightError

from app.rankings.crawler import fetch_ranking_html
from app.rankings.parser import parse_ranking_items
from app.rankings.schemas import RankingResponse


def get_ranking_response(
    gender: str,
    age_band: str,
    include_soldout: bool,
) -> RankingResponse:
    html = fetch_ranking_html(
        gender=gender,
        age_band=age_band,
        include_soldout=include_soldout,
    )
    items = parse_ranking_items(html)

    if not include_soldout:
        items = [item for item in items if not item.is_soldout]

    return RankingResponse(
        gender=gender,
        age_band=age_band,
        include_soldout=include_soldout,
        count=len(items),
        items=items,
    )


__all__ = ["PlaywrightError", "get_ranking_response"]
