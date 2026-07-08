from pydantic import BaseModel


class RankingItem(BaseModel):
    rank: int
    name: str
    product_url: str
    brand: str | None = None
    price: int | None = None
    image_url: str | None = None
    is_soldout: bool = False


class RankingResponse(BaseModel):
    gender: str
    age_band: str
    include_soldout: bool
    count: int
    items: list[RankingItem]