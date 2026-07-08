from fastapi import APIRouter, HTTPException

from app.rankings.schemas import RankingResponse
from app.rankings.service import PlaywrightError, get_rankings_response

router = APIRouter(prefix="/rankings", tags=["rankings"])


@router.get(
    "",
    response_model=RankingResponse,
    summary="무신사 스니커즈 랭킹 목록 조회",
)
async def list_rankings(
    gender: str = "A",
    age_band: str = "AGE_BAND_ALL",
    include_soldout: bool = True,
) -> RankingResponse:
    """성별, 연령대, 품절 포함 여부에 맞는 랭킹 목록을 반환한다."""
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
