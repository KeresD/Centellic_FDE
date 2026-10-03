"""Every route that calls Claude or Voyage. Provider failures are mapped to status codes in
one place: timeout 504, rate limit 429, any other upstream failure 502 (brief §1)."""

from collections.abc import Callable, Iterator
from typing import Any

import anthropic
import config
import knowledge_store
import llm
import voyageai.error as voyage_error
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from models import AskRequest, SearchInput
from prompts import REFUSAL

from routers.common import get_fund_or_404

router = APIRouter(tags=["ai"])

# defined once at module level (like IdempotencyKey in common.py), which also satisfies ruff B008
FundFromPath = Depends(get_fund_or_404)


# ---------- provider errors ----------

def _call(label: str, fn: Callable[..., Any], *args: Any) -> Any:
    """Run one provider call and turn its failures into the status codes the brief asks for."""
    try:
        return fn(*args)
    except (anthropic.APITimeoutError, voyage_error.Timeout):
        raise HTTPException(status_code=504, detail=f"{label}: provider timed out") from None
    except (anthropic.RateLimitError, voyage_error.RateLimitError):
        raise HTTPException(status_code=429, detail=f"{label}: provider rate limit reached") from None
    except (anthropic.APIError, voyage_error.VoyageError) as e:
        raise HTTPException(status_code=502,
                            detail=f"{label}: provider error ({type(e).__name__})") from None


def _search(question: str) -> list[dict]:
    try:
        return _call("Search", knowledge_store.search, question)
    except RuntimeError as e:
        # index not built: 409 so the UI can tell this apart from a provider failure
        raise HTTPException(status_code=409, detail=str(e)) from None


# ---------- fund summary and analysis ----------

@router.post("/funds/{fund_id}/summary")
def fund_summary(fund: dict = FundFromPath):
    return _call("Summary", llm.summarise_fund, fund)


@router.get("/funds/{fund_id}/summary/stream")
def fund_summary_stream(fund: dict = FundFromPath):
    chunks = llm.stream_fund_summary(fund)
    # take the first chunk now: that opens the Claude request, so a failure still becomes
    # a 504/429/502 instead of a 200 that stops halfway through
    first = _call("Summary stream", next, chunks, "")

    def body() -> Iterator[str]:
        yield first
        yield from chunks

    return StreamingResponse(body(), media_type="text/plain")


@router.get("/funds/{fund_id}/summary/estimate")
def fund_summary_estimate(fund: dict = FundFromPath):
    return {"fund_id": fund["fund_id"], "model": llm.MODEL,
            "est_input_tokens": _call("Token estimate", llm.est_fund_tokens, fund)}


@router.post("/funds/{fund_id}/analysis")
def fund_analysis(fund: dict = FundFromPath):
    try:
        return _call("Analysis", llm.analyse_fund, fund)
    except ValueError:
        # Claude replied, but not in the FundAssessment shape
        raise HTTPException(status_code=502,
                            detail="Analysis: provider returned an invalid assessment") from None


# ---------- knowledge: index, search, grounded answers ----------

@router.post("/knowledge/index")
def build_index():
    return _call("Index", knowledge_store.build_index)


@router.post("/knowledge/search")
def search(body: SearchInput):
    """Retrieval only, no Claude: every result with its score."""
    return {"results": _search(body.query)}


@router.post("/ask")
def ask(body: AskRequest):
    results = _search(body.question)
    relevant = [r for r in results if r["score"] >= config.RELEVANCE_FLOOR]
    if not relevant:
        # refuse WITHOUT calling Claude (brief §3): nothing to ground on, no tokens spent
        return {"answer": REFUSAL, "refused": True, "sources": [],
                "best_score": max((r["score"] for r in results), default=None)}
    answer = _call("Answer", llm.answer_from_context, body.question,
                   knowledge_store.format_context(relevant))
    return {**answer,
            "refused": REFUSAL in answer["answer"],   # Claude may still refuse if context falls short
            "sources": [{"id": r["id"], "title": r["title"], "score": r["score"]} for r in relevant]}