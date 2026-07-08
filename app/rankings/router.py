from fastapi import APIRouter, HTTPException

from app.rankings.schemas import RankingResponse
from app.rankings.service import PlaywrightError, get_rankings_response

router = APIRouter(prefix="/rankings", tags=["rankings"])


@router.get("", response_model=RankingResponse)
async def list_rankings(
    gender: str = "A",
    age_band: str = "AGE_BAND_ALL",
    include_soldout: bool = True,
) -> RankingResponse:
    try:
        return await get_rankings_response(
            gender=gender,
            age_band=age_band,
            include_soldout=include_soldout,
        )
    except PlaywrightError as error:
        raise HTTPException(
            status_code=502,
            detail="Failed to fetch Musinsa ranking page",
        ) from error
