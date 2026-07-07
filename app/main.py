from fastapi import FastAPI

app = FastAPI(title="Musinsa Ranking API")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Musinsa Ranking API"}


@app.get("/health")
def read_health() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/rankings")
def read_rankings(
    gender: str = "A",
    age_band: str = "AGE_BAND_ALL",
    include_soldout: bool = True,
) -> dict[str, str | bool]:
    return {
        "gender": gender,
        "age_band": age_band,
        "include_soldout": include_soldout,
        "message": "Ranking endpoint is ready",
    }
