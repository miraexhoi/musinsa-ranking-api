from fastapi import FastAPI

from app.exceptions import register_exception_handlers
from app.rankings.router import router as rankings_router

app = FastAPI(title="Musinsa Ranking API")
register_exception_handlers(app)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Musinsa Ranking API"}


@app.get("/health")
def read_health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(rankings_router)
