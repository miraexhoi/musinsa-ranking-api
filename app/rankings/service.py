from playwright.async_api import Error as PlaywrightError

from app.rankings.crawler import fetch_ranking_html
from app.rankings.parser import parse_ranking_items
from app.rankings.schemas import RankingResponse


async def get_rankings_response(
    gender: str,
    age_band: str,
    include_soldout: bool,
) -> RankingResponse:
    """랭킹 HTML 수집, 파싱, 품절 필터링 후 API 응답을 만든다."""
    html = await fetch_ranking_html(
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


__all__ = ["PlaywrightError", "get_rankings_response"]
