"""Everything Claude is told. Rules live in the system prompts; data lives in the user
message built by build_fund_prompt. Each rule traces to a policy document."""

from typing import Any

from helpers_and_compliance.performance import fund_performance_facts

# System prompts

ADVISER_SYSTEM_PROMPT = (
    "You write fund updates that a financial adviser will review and pass to a client. "
    "Use plain British English a non-specialist can follow, and explain terms such as "
    "benchmark or percentage point the first time you use them. "
    "Use only the figures provided. Never invent figures. "
    # doc 6 evidence policy; doc 13 - 4.2
    "Explain performance only through the holding contributions and cost drag provided. "
    "Do not suggest economic, market or currency causes, because none are in the evidence. "
    "Holding contributions are absolute, so do not present them as the reason the fund "
    "beat or trailed its benchmark. "
    # doc 12 - 4.2
    "If the ESG score is pending review, say it has not yet been approved and never estimate it. "
    "If the holdings data is marked stale, say the figures may be out of date. "
    # doc 13 - 4.1, 5, 4.3
    "Returns are after fund costs but before adviser and platform fees. "
    "Do not recommend buying, selling or holding. "
    "End with: Past performance is not a reliable indicator of future results. "
    "No em dash characters."
)

ANALYSIS_SYSTEM_PROMPT = (
    "You are a fund analyst supporting a portfolio manager at a wealth manager. "
    "Use only the figures provided. Never invent numbers, holdings or causes. "
    "Do not suggest economic, market or currency causes, because none are in the evidence. "
    "Put anything the data cannot support in evidence_gaps, for example an ESG score pending "
    "review, stale holdings, or losses within a quarter, which "
    "quarterly figures cannot show. "
    "Do not assess suitability for any client and do not make recommendations. "
    "Use British English. No em dash characters."
)

REFUSAL = "The provided documents do not answer that question."

GROUNDED_SYSTEM_PROMPT = (
    "You are an assistant for portfolio managers and advisers at Wrenford Asset Management. "
    "Answer using ONLY the context provided. "
    "Cite the document id in square brackets after each claim, like [doc-007]. "
    f"If the context does not contain the answer, reply exactly: '{REFUSAL}' "
    "Never use knowledge from outside the context. "
    "Mandate compliance is not suitability: never say an investment is suitable for a client "
    "and never make a personal recommendation. "
    "If documents have different dates, say which date each figure comes from. "
    "Use British English. No em dash characters."
)

# Tasks

SUMMARY_TASK = "Write a two paragraph client update on this fund's performance and risk last quarter."
ANALYSIS_TASK = "Assess this fund for a portfolio manager."


# User message

def _show(value: Any, suffix: str = "") -> str:
    return "not available" if value is None else f"{value}{suffix}"


def build_fund_prompt(fund: dict, task: str) -> str:
    facts = fund_performance_facts(fund)
    esg = (f"{fund['esg_score']}/100, approved" if fund["esg_score_status"] == "approved"
           else "pending review, no approved score")
    freshness = "STALE" if facts["holdings_stale"] else "current"

    lines = [
        task, "",
        f"Fund: {fund['name']}",
        f"Strategy: {fund['strategy']}",
        f"Asset class: {fund['asset_class']}",
        f"Risk rating (1 lowest, 7 highest): {fund['risk_rating']}",
        f"ESG score: {esg}",
        f"Ongoing charges: {fund['ongoing_charges_pct']}% a year",
        f"Estimated transaction costs: {fund['estimated_transaction_costs_pct']}% a year",
        f"Currency hedging: {fund['currency_hedging']}",
        f"Holdings as of: {_show(facts['holdings_as_of'])} ({freshness})",
        "",
        f"Period: {facts['period']}",
        f"Fund return after fund costs: {_show(facts['fund_return_pct'], '%')}",
        f"Benchmark ({fund['benchmark']}) return: {_show(facts['benchmark_return_pct'], '%')}",
        f"Difference from benchmark: {_show(facts['relative_return_pp'], ' percentage points')}",
        f"Fund cost drag this quarter: {_show(facts['cost_drag_pp'], ' percentage points')}",
        f"Trailing 12 month return: {_show(facts['trailing_12m_return_pct'], '%')}",
        "",
        "Holding contributions before fund costs (percentage points):",
        *[f"- {c['company']}: {c['contribution_pp']:+.3f}" for c in facts["contributions"]],
        f"Total of contributions: {facts['contributions_total_pp']:+.3f}",
    ]
    return "\n".join(lines)