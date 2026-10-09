# how we call the model...nothing in here knows about FastAPI

import os

# from anthropic import APIStatusErrror, APITimeoutError, RateLimitErrror
import anthropic
from anthropic.types import ParsedTextBlock, TextBlock
from pydantic import BaseModel, Field

MODEL = "claude-haiku-4-5-20251001"

# SDK default are max_retries=2 and 600-second read timeout
# both = overridden here deliverately...decisions thather than accident

client = anthropic.Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"],
    timeout=30.0,
    max_retries=3,
)

# Rules = in System
# Data = in User

SYSTEM_PROMPT = (
    "You are a legal market analyst writing for an institute audience. "
    "Use British English. Use only the figures given to you."
    "Never invent numbers, rankings or facts that are not in the data provided."
)

def build_prompt(firm: dict) -> str:
    return(
        f"Summarise this law firm in two short paragraphs. \n\n"
        f"Name: {firm['name']}\n"
        f"Jurisdiction: {firm['jurisdiction']}\n"
        f"Revenue: {firm['revenue_usd_m']}\n"
        f"Lawyers: {firm['lawyers']}\n"
        f"Equity_partners: {firm['equity_partners']}\n"
    )

#The call
def summarise_firm(firm: dict) -> dict:
    # one LLM call - returns text + what it costs -> input and output
    # to see if the call is cut off or unfinished call stop_reason()
    # every call will have input,output tokens and stop_reason
    response = client.messages.create(
        model=MODEL,
        max_tokens=400,
        system=GROUNDED_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_prompt(firm)}],
    )
    block = response.content[0]
    assert isinstance(block, TextBlock)
    return {
        "id": firm["id"],
        "name": firm["name"],
        "summary": block.text,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "stop_reason": response.stop_reason,
    }

'''>>> from data import FIRMS
>>> import llm
>>> result = llm.summarise_firm(FIRMS[0])
>>> print(result)
{'id': 1, 'name': 'Harding & Voss', 
'summary': '# Harding & Voss\n\nHarding & Voss is a UK-based law firm with a 
substantial presence in the domestic', 
'input_tokens': 97, 'output_tokens': 30, 'stop_reason': 'max_tokens'}'''

# messages.count_tokens() tells you how big a request is wihtout sending the request
# much cheaper end point

# est = estimate
def est_input_tokens(firm: dict) -> int:
    '''Count tokens before sending. Costs nothing, tells you what call costs'''
    counted = client.messages.count_tokens(
        model=MODEL,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_prompt(firm)}],
    )
    return counted.input_tokens

def stream_firm_summary(firm: dict):
    '''Yields text chunks as they arrive, rather than waiting for whole response'''
    with client.messages.stream(
        model=MODEL,
        max_tokens=400,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_prompt(firm)}],
    ) as stream:
        yield from stream.text_stream

# how to verify a function - define class and use pydantic tests - ruff, pytest, mypy

class FirmAnalysis(BaseModel):
    """This is the shape we require back. It is not a suggestion to the model. It is a contract"""
    tier: str = Field(description="One of: magic circle, national, boutique") # tier = type of firm
    # strengths
    strengths: list[str] = Field(max_length=3)
    # risks
    risks: list[str] = Field(max_length=3)
    # headcount_efficiency
    headcount_efficiency: str = Field(description="high, medium, low")
    
    
def analyse_firm(firm: dict) -> dict:
    """Structured output. Response = validated against FirmAnalysis or it fails."""
    response = client.messages.parse(
        model=MODEL,
        max_tokens=600,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_prompt(firm)}],
        output_format=FirmAnalysis,
    )
    block = response.content[0]
    assert isinstance(block, ParsedTextBlock)
    analysis = block.parsed_output
    assert analysis is not None
    
    return {
        # id
        "id": firm["id"],
        # name
        "name": firm["name"],
        # analysis
        "analysis": analysis,
        # input tokens
        "input_tokens": response.usage.input_tokens,
        # output tokens
        "output_tokens": response.usage.output_tokens,
        # stop reason
        "stop_reason": response.stop_reason,
    }

# add the generation step
# retrieval finds documents...RAG's third letter is generate - turn those docs into answers

GROUNDED_SYSTEM_PROMPT = (
    "You are a legal market analyst. Answer using ONLY the context provided."
    "Cite the document id in square brackets after each claim, like [doc-001]."
    "If the context does not contain the answer, say exactly:"
    "'The provided documents do not answer that question.'"
    "Never use knowledge from outside the context. Use British English. No em dash characters."
)

# notice where the context goes
# rules in the system
# data in user

def answer_from_context(question: str, context: str, system: str = GROUNDED_SYSTEM_PROMPT) -> dict:
    '''Answer strictly from retrieved context - the G in RAG'''
    response = client.messages.create(
        model=MODEL,
        max_tokens=500,
        system=system,
        messages=[{
            "role": "user",
            "content": f"Context: \n\n{context}\n\nQuestion: {question}",
        }]
    )
    block = response.content[0]
    assert isinstance(block, TextBlock)
    return {
        "answer": block.text,
        # input and output tokens
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "stop_reason": response.stop_reason,
    }