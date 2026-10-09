"""The agent's tools: the schemas Claude sees, the functions behind them, and one dispatcher.
Nothing in here knows about FastAPI. Nothing in here raises to the agent loop."""

import json

import config
import knowledge_store
import voyageai.error as voyage_error
from data_doc.data import FUNDS, PORTFOLIOS
from helpers_and_compliance.helpers_and_compliance import (
    check_portfolio,
    check_proposed_fund,
)
from models import ScreenInput, SearchInput
from pydantic import ValidationError

# The Schema Claude sees

SEARCH_TOOL = {
    "name": "search_documents",
    "description": (
        "Search Wrenford's documents: fund factsheets, manager commentary, client investment "
        "mandates, the ESG and exclusions policy and the suitability rules. Use it for what a "
        "policy or mandate says, or why a fund performed as it did."
    ),
    "input_schema": {
        "type": "object",
        "properties": {"query": {"type": "string", "description": "What to search for"}},
        "required": ["query"],
    },
}

SCREEN_TOOL = {
    "name": "screen_portfolio",
    "description": (
        "Check a client's portfolio against every rule in its mandate, using look-through to the "
        "funds' underlying holdings. Give only client_name to check the portfolio as held today. "
        "Also give fund_name and weight_pct to check a proposed purchase, assumed to be funded "
        "pro rata from existing holdings. Returns pass, breach or insufficient_evidence per rule."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "client_name": {"type": "string", "description": "Client name, or a distinctive part of it"},
            "fund_name": {"type": "string", "description": "Fund to add, or a distinctive part of its name"},
            "weight_pct": {"type": "number", "description": "Proposed weight of that fund, 0 to 100"},
        },
        "required": ["client_name"],
    },
}

TOOLS = [SEARCH_TOOL, SCREEN_TOOL]

# The functions behind them

def _find_by_name(records: list[dict], key: str, name: str, label: str) -> dict:
    """Case-insensitive partial match that must find exactly one record.
    The error lists the valid names, so Claude can correct itself and try again."""
    wanted = name.strip().lower()
    matches = [r for r in records if wanted in r[key].lower()]
    if len(matches) != 1:
        problem = "No" if not matches else "More than one"
        known = "; ".join(r[key] for r in records)
        raise LookupError(f"{problem} {label} matches '{name}'. Known {label}s: {known}")
    return matches[0]

def search_documents(tool_input: dict) -> str:
    args = SearchInput.model_validate(tool_input)
    # same relevance floor as /ask, so the agent cannot ground an answer on a weak match
    results = [r for r in knowledge_store.search(args.query) if r["score"] >= config.RELEVANCE_FLOOR]
    if not results:
        return "No document cleared the relevance floor for that query."
    return knowledge_store.format_context(results)

def screen_portfolio(tool_input: dict) -> str:
    args = ScreenInput.model_validate(tool_input)
    portfolio = _find_by_name(PORTFOLIOS, "client_name", args.client_name, "client")
    if args.fund_name is None or args.weight_pct is None:
        result = check_portfolio(portfolio)
    else:
        fund = _find_by_name(FUNDS, "name", args.fund_name, "fund")
        result = check_proposed_fund(portfolio, fund["fund_id"], args.weight_pct)
    return json.dumps(result)

HANDLERS = {"search_documents": search_documents, "screen_portfolio": screen_portfolio}

# dispatcher

def run_tool(name: str, tool_input: dict) -> tuple[str, bool]:
    """Run one tool call and return (result_text, is_error). Never raises: unknown tools,
    bad arguments and failures all go back to Claude as errors it can read (brief section 4)."""
    handler = HANDLERS.get(name)
    if handler is None:
        return f"Unknown tool: {name}. Available: {', '.join(HANDLERS)}", True
    try:
        return handler(tool_input), False
    except ValidationError as e:
        problems = "; ".join(f"{'.'.join(str(p) for p in err['loc']) or 'input'}: {err['msg']}"
                             for err in e.errors())
        return f"Invalid arguments for {name}: {problems}", True
    except (LookupError, RuntimeError, ValueError, voyage_error.VoyageError) as e:
        # expected failures: unknown client or fund, index not built, bad value, Voyage down
        return f"{name} failed: {e}", True