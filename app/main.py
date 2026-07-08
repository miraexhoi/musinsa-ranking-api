from fastapi import FastAPI

from app.exceptions import register_exception_handlers
from app.rankings.router import router as rankings_router

app = FastAPI(
    title="Musinsa Ranking API",
    description="무신사 스니커즈 랭킹 상품 목록을 조회하는 API입니다.",
)
register_exception_handlers(app)


@app.get("/")
def get_root() -> dict[str, str]:
    """API 기본 응답을 반환한다."""
    return {"message": "Musinsa Ranking API"}


@app.get("/health")
def get_health() -> dict[str, str]:
    """서버 상태 확인 응답을 반환한다."""
    return {"status": "ok"}


app.include_router(rankings_router)
