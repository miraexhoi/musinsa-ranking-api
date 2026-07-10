from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.rankings.errors import RankingFetchError
from app.rankings.schemas import RankingItem, RankingResponse

client = TestClient(app)


def test_get_health_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_rankings_returns_ranking_response():
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
        "app.rankings.router.get_rankings_response",
        new=AsyncMock(return_value=ranking_response),
    ) as mocked_get_rankings_response:
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
    mocked_get_rankings_response.assert_awaited_once_with(
        gender="A",
        age_band="AGE_BAND_ALL",
        include_soldout=True,
    )


def test_list_rankings_returns_error_response_when_fetch_fails():
    with patch(
        "app.rankings.router.get_rankings_response",
        new=AsyncMock(
            side_effect=RankingFetchError(
                code="RANKING_PAGE_FETCH_FAILED",
                message="Failed to fetch Musinsa ranking page",
                status_code=502,
                debug_detail="Playwright timeout",
            )
        ),
    ):
        response = client.get("/rankings")

    assert response.status_code == 502
    assert response.json() == {
        "status": "error",
        "message": "Failed to fetch Musinsa ranking page",
    }


def test_list_rankings_returns_fail_response_when_query_param_is_invalid():
    response = client.get(
        "/rankings",
        params={"include_soldout": "not-a-bool"},
    )

    assert response.status_code == 422
    assert response.json()["status"] == "fail"
    assert "detail" in response.json()["data"]


def test_list_rankings_returns_fail_response_when_gender_is_invalid():
    response = client.get(
        "/rankings",
        params={"gender": "UNKNOWN"},
    )

    assert response.status_code == 422
    assert response.json()["status"] == "fail"
    assert "detail" in response.json()["data"]
