from fastapi import FastAPI

from app.schemas import RankingItem, RankingResponse

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
    items = [
        RankingItem(
            rank=1,
            brand="Sample Brand",
            name="Sample Sneaker",
            price=129000,
            product_url="https://www.musinsa.com/sample-product",
            image_url=None,
            is_soldout=False,
        )
    ]

    return RankingResponse(
        gender=gender,
        age_band=age_band,
        include_soldout=include_soldout,
        count=len(items),
        items=items,
    )