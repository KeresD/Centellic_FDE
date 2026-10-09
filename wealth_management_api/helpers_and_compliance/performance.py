"""Fund performance facts, worked out in code before Claude sees anything.
Plain Python: nothing here knows about FastAPI or Claude."""

from datetime import date
from typing import Any

import config

from helpers_and_compliance.helpers import today


def fund_performance_facts(fund: dict) -> dict[str, Any]:
    contributions = sorted(
        ({"company": h["company"], "contribution_pp": h["contribution_pp"]} for h in fund["holdings"]),
        key=lambda c: c["contribution_pp"], reverse=True,
    )

    fund_return = fund.get("quarter_return_pct")
    benchmark_return = fund.get("benchmark_quarter_return_pct")
    
    # for missing returns --> stays as none never as zero
    relative_return = None
    if fund_return is not None and benchmark_return is not None:
        relative_return = round(fund_return - benchmark_return, 2)


    as_of = fund["holdings_as_of"]
    stale = (today() - date.fromisoformat(as_of)).days > config.HOLDINGS_STALE_DAYS


    return {
        "period": fund["period"],
        "fund_return_pct": fund_return,
        "benchmark_return_pct": benchmark_return,
        "relative_return_pp": relative_return,
        "trailing_12m_return_pct": fund["trailing_12m_return_pct"],
        "cost_drag_pp": fund["quarter_cost_drag_pp"],
        "contributions": contributions,
        "contributions_total_pp": round(sum(c["contribution_pp"] for c in contributions), 3),
        "holdings_as_of": as_of,
        "holdings_stale": stale,
    }