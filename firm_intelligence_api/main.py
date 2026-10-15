import insights
from fastapi import FastAPI

from routers import agent, ask, firms, knowledge, people, reports  # type: ignore

app = FastAPI(title="Firm Intelligence API")
app.include_router(firms.router)
app.include_router(people.router)
app.include_router(reports.router)
app.include_router(knowledge.router)
app.include_router(insights.router)
app.include_router(ask.router)
app.include_router(agent.router)

@app.get("/health")
def health():
    return {"status": "ok"}