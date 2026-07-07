from pydantic import BaseModel

class RankingItem(BaseModel):
    rank: int
    brand: str
    name: str
    price: int
    product_url: str
    image_url: str | None = None
    is_soldout: bool = False

class RankingResponse(BaseModel):
   gender: str
   age_band: str
   include_soldout: bool
   count: int
   items: list[RankingItem]