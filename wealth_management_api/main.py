from fastapi import FastAPI
from routers import ai, funds, mandates, portfolios

app = FastAPI(title="Wealth Management API")

app.include_router(funds.router)
app.include_router(portfolios.router)
app.include_router(mandates.router)
app.include_router(ai.router)


@app.get("/health")
def health():
    return {"status": "ok"}