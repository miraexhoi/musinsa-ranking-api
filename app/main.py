from fastapi import FastAPI, HTTPException
from playwright.sync_api import Error as PlaywrightError

from app.crawler import fetch_ranking_html
from app.parser import parse_ranking_items
from app.schemas import RankingResponse

app = FastAPI(title="Musinsa Ranking API")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Musinsa Ranking API"}


@app.get("/health")
def read_health() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/rankings", response_model=RankingResponse)
def read_rankings(
    gender: str = "A",
    age_band: str = "AGE_BAND_ALL",
    include_soldout: bool = True,
) -> RankingResponse:
    try:
        html = fetch_ranking_html(
            gender=gender,
            age_band=age_band,
            include_soldout=include_soldout,
        )
    except PlaywrightError as error:
        raise HTTPException(
            status_code=502,
            detail="Failed to fetch Musinsa ranking page",
        ) from error

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