from unittest.mock import AsyncMock, patch

import pytest

from app.rankings.schemas import RankingItem
from app.rankings.service import get_rankings_response


@pytest.mark.anyio
async def test_get_rankings_response_returns_parsed_items():
    items = [
        RankingItem(
            rank=1,
            name="테스트 상품",
            product_url="https://www.musinsa.com/products/1",
            brand="테스트 브랜드",
            price=10000,
            image_url="https://image.msscdn.net/sample.jpg",
            is_soldout=False,
        )
    ]

    with (
        patch(
            "app.rankings.service.fetch_ranking_html",
            new=AsyncMock(return_value="<html></html>"),
        ),
        patch("app.rankings.service.parse_ranking_items", return_value=items),
    ):
        response = await get_rankings_response(
            gender="A",
            age_band="AGE_BAND_ALL",
            include_soldout=True,
        )

    assert response.gender == "A"
    assert response.age_band == "AGE_BAND_ALL"
    assert response.include_soldout is True
    assert response.count == 1
    assert response.items == items


@pytest.mark.anyio
async def test_get_rankings_response_excludes_soldout_items():
    items = [
        RankingItem(
            rank=1,
            name="판매중 상품",
            product_url="https://www.musinsa.com/products/1",
            is_soldout=False,
        ),
        RankingItem(
            rank=2,
            name="품절 상품",
            product_url="https://www.musinsa.com/products/2",
            is_soldout=True,
        ),
    ]

    with (
        patch(
            "app.rankings.service.fetch_ranking_html",
            new=AsyncMock(return_value="<html></html>"),
        ),
        patch("app.rankings.service.parse_ranking_items", return_value=items),
    ):
        response = await get_rankings_response(
            gender="A",
            age_band="AGE_BAND_ALL",
            include_soldout=False,
        )

    assert response.include_soldout is False
    assert response.count == 1
    assert len(response.items) == 1
    assert response.items[0].name == "판매중 상품"
    assert response.items[0].is_soldout is False
