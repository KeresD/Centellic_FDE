"""Every Claude call lives here, and nothing else. No FastAPI, no prompt wording, no maths:
those live in routers/ai.py, prompts.py and helpers_and_compliance/performance.py."""

import os
from collections.abc import Iterator

import anthropic
import config
from anthropic.types import Message, MessageParam, TextBlock
from helpers_and_compliance.performance import fund_performance_facts
from models import FundAssessment
from prompts import (
    ADVISER_SYSTEM_PROMPT,
    ANALYSIS_SYSTEM_PROMPT,
    ANALYSIS_TASK,
    GROUNDED_SYSTEM_PROMPT,
    SUMMARY_TASK,
    build_fund_prompt,
)

MODEL = config.MODEL

# SDK defaults are a 600-second timeout and 2 retries; both overridden deliberately
client = anthropic.Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"],
    timeout=30.0,
    max_retries=3,
)


# ---------- small helpers ----------

def _messages(fund: dict, task: str, include_history: bool = False) -> list[MessageParam]:
    return [{"role": "user", "content": build_fund_prompt(fund, task, include_history)}]


def _text(response: Message) -> str:
    block = response.content[0]
    assert isinstance(block, TextBlock)
    return block.text


def _usage(response: Message) -> dict:
    """Every generated answer reports what it cost (brief §2)."""
    return {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "stop_reason": response.stop_reason,
    }


# ---------- the calls ----------

def summarise_fund(fund: dict) -> dict:
    """Plain-language client update, for an adviser to review."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=500,
        system=ADVISER_SYSTEM_PROMPT,
        messages=_messages(fund, SUMMARY_TASK),
    )
    return {"fund_id": fund["fund_id"], "name": fund["name"],
            "summary": _text(response), **_usage(response)}


def stream_fund_summary(fund: dict) -> Iterator[str]:
    """Same summary, yielded in chunks as Claude writes it."""
    with client.messages.stream(
        model=MODEL,
        max_tokens=500,
        system=ADVISER_SYSTEM_PROMPT,
        messages=_messages(fund, SUMMARY_TASK),
    ) as stream:
        yield from stream.text_stream


def est_fund_tokens(fund: dict) -> int:
    """Count the summary's input tokens without generating anything."""
    counted = client.messages.count_tokens(
        model=MODEL,
        system=ADVISER_SYSTEM_PROMPT,
        messages=_messages(fund, SUMMARY_TASK),
    )
    return counted.input_tokens


def analyse_fund(fund: dict) -> dict:
    """Structured assessment, validated against FundAssessment or it fails."""
    response = client.messages.parse(
        model=MODEL,
        max_tokens=800,
        system=ANALYSIS_SYSTEM_PROMPT,
        messages=_messages(fund, ANALYSIS_TASK, include_history=True),
        output_format=FundAssessment,
    )
    assessment = response.parsed_output
    if assessment is None:
        raise ValueError("Claude did not return a valid FundAssessment")
    facts = fund_performance_facts(fund)
    return {
        "fund_id": fund["fund_id"],
        "name": fund["name"],
        "assessment": assessment.model_dump(),
        # numbers come from code, not from the model
        "relative_return_pp": facts["relative_return_pp"],
        "holdings_stale": facts["holdings_stale"],
        **_usage(response),
    }


def answer_from_context(question: str, context: str) -> dict:
    """The G in RAG: answer strictly from retrieved documents."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=600,
        system=GROUNDED_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f"Context:\n\n{context}\n\nQuestion: {question}"}],
    )
    return {"answer": _text(response), **_usage(response)}