from fastapi import FastAPI

app = FastAPI(title="Musinsa Ranking API")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Musinsa Ranking API"}


@app.get("/health")
def read_health() -> dict[str, str]:
    return {"status": "ok"}
