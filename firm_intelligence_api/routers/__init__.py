from fastapi import APIRouter, FastAPI

from .firms import router as firms_router
from .people import router as people_router
from .reports import router as reports_router

app = FastAPI()
app.include_router(firms_router)
app.include_router(people_router)
app.include_router(reports_router)

# router prefixes instead of @app
router = APIRouter(prefix="/people", tags=["people"])

#curl http://127.0.0.1:8000/insert_def - to check status

#decorator that registers function below it as the handler for GET request to the /health path
router.get("/health")
# handler function. Take no params and returns python dict, which fastapi automatically serialises to JSON
# so get/health requet returns
def health():
    return{"status": "ok"} #json