"""Routes that call Claude. Nothing in here builds prompts - that lives in llm.py and prompts.py."""

import anthropic
import llm
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from routers.common import get_fund_or_404

router = APIRouter(tags=["ai"])

# defined once at module level (like IdempotencyKey in common.py), which also satisfies ruff B008
fund_exists = Depends(get_fund_or_404)

# Specific errors are checked first and everything else pulls an Error 502
def provide_error(label:str, e: anthropic.APIError) -> HTTPException:
    if isinstance(e, anthropic.APITimeoutError):
        return HTTPException(status_code=504, detail=f"{label} query has timed out")
    if isinstance(e, anthropic.RateLimitError):
        return HTTPException(status_code=429, detail=f"{label} query has hit rate limit")
    return HTTPException(status_code=502, detail=f"{label} query has failed due to API error {e}")


@router.post("/funds/{fund_id}/summary")
def funds_summary(fund:dict = fund_exists):
    try:
        return llm.summarise_fund(fund)
    except anthropic.APIError as e:
        raise provide_error("Summary", e) from e

   
@router.get("/funds/{fund_id}/summary/estimate")
def fund_summary_estimate(fund:dict = fund_exists):
    try:
        return{
            "fund_id": fund["fund_id"],
            "est_input_token": llm.est_fund_tokens(fund),
            "model": llm.MODEL,
        }
    except anthropic.APIError as e:
        raise provide_error("Token count", e) from e
    

@router.get("/funds/{fund_id}/summary/stream")
def fund_summary_stream(fund:dict = fund_exists):
    return StreamingResponse(
        llm.stream_fund_summary(fund),
        media_type="text/plain",
    )
    
    
@router.post("/funds/{fund_id}/analysis")
def fund_analysis(fund: dict = fund_exists):
    try:
        return llm.analyse_fund(fund)
    except anthropic.APIError as e:
        raise provide_error("Analysis", e) from e