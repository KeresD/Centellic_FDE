# System prompts, tasks and build_fund_prompt

"""Fund performance facts, worked out in code before Claude sees anything.
Plain Python: nothing here knows about FastAPI or Claude."""

from datetime import date
from typing import Any

import config
from data_doc.funds import FUND_QUARTERLY_RETURNS
from data_doc.holding_details import HOLDING_DETAILS
from data_doc.holdings import HOLDINGS
from data_doc.issuers import ISSUERS

from helpers_and_compliance.helpers import find_one, today


def fund_performance_facts(fund: dict) -> dict[str, Any]:
    fund_holding_ids = {h["holding_id"] for h in HOLDINGS if h["fund_id"] == fund["fund_id"]}

    contributions = []
    for detail in HOLDING_DETAILS:
        if detail["holding_id"] in fund_holding_ids:
            # resolve the name by issuer ID, not the source alias (doc 12 §3.3)
            issuer = find_one(ISSUERS, "issuer_id", detail["issuer_id"])
            contributions.append({
                "company": issuer["name"] if issuer else detail["source_company_name"],
                "contribution_pp": round(detail["gross_contribution_pp"], 3),
            })
    contributions.sort(key=lambda c: c["contribution_pp"], reverse=True)

    fund_return = fund.get("quarter_return_pct")
    benchmark_return = fund.get("benchmark_quarter_return_pct")
    relative = (round(fund_return - benchmark_return, 2)
                if fund_return is not None and benchmark_return is not None else None)

    as_of = fund.get("holdings_as_of")
    stale = (as_of is None
             or (today() - date.fromisoformat(as_of)).days > config.HOLDINGS_STALE_DAYS)

    history = sorted((r for r in FUND_QUARTERLY_RETURNS if r["fund_id"] == fund["fund_id"]),
                     key=lambda r: r["period_start"])

    return {
        "period": f"{fund.get('performance_period_start')} to {fund.get('performance_period_end')}",
        "fund_return_pct": fund_return,
        "benchmark_return_pct": benchmark_return,
        "relative_return_pp": relative,
        "trailing_12m_return_pct": fund.get("trailing_12m_return_pct"),
        "cost_drag_pp": fund.get("quarter_cost_drag_pp"),
        "contributions": contributions,
        "contributions_total_pp": round(sum(c["contribution_pp"] for c in contributions), 3),
        "holdings_as_of": as_of,
        "holdings_stale": stale,
        "quarterly_history": [
            {"period_end": r["period_end"],
             "fund_pct": round(r["fund_return_pct"], 2),
             "benchmark_pct": round(r["benchmark_return_pct"], 2)}
            for r in history
        ],
    }