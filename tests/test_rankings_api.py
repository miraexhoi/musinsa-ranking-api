from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.rankings.schemas import RankingItem, RankingResponse

client = TestClient(app)


def test_read_health_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_rankings_returns_ranking_response():
    ranking_response = RankingResponse(
        gender="A",
        age_band="AGE_BAND_ALL",
        include_soldout=True,
        count=1,
        items=[
            RankingItem(
                rank=1,
                name="테스트 상품",
                product_url="https://www.musinsa.com/products/1",
                brand="테스트 브랜드",
                price=10000,
                image_url="https://image.msscdn.net/sample.jpg",
                is_soldout=False,
            )
        ],
    )

    with patch(
        "app.rankings.router.get_ranking_response",
        new=AsyncMock(return_value=ranking_response),
    ) as mocked_get_ranking_response:
        response = client.get(
            "/rankings",
            params={
                "gender": "A",
                "age_band": "AGE_BAND_ALL",
                "include_soldout": "true",
            },
        )

    assert response.status_code == 200
    assert response.json()["count"] == 1
    assert response.json()["items"][0]["name"] == "테스트 상품"
    mocked_get_ranking_response.assert_awaited_once_with(
        gender="A",
        age_band="AGE_BAND_ALL",
        include_soldout=True,
    )
