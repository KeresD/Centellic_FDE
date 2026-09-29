"""HTTP layer for the tool-use agent - all FastAPI concerns live here, not in agent.py"""

from anthropic import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    RateLimitError
    )

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

import agent

router = APIRouter(prefix="/agent", tags=["agent"])

class AskRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    question: str = Field(
        min_length=1,
        max_length=2000,
        description="The question for the agent to research and answer",
    )

@router.post("/ask")
def ask(body: AskRequest) -> dict:
    try:
        return agent.ask_with_tools(body.question)
    except APITimeoutError:
        raise HTTPException(status_code=504, detail="LLM request timed out")
    except RateLimitError:
        raise HTTPException(status_code=429, detail="LLM rate limit exceeded")
    except (APIConnectionError, APIStatusError) as e:
        raise HTTPException(status_code=502, detail=f"LLM provider unavailable: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")