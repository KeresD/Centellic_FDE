"""Portfolio records: CRUD, allocations, and the PM's compliance checks."""

from data_doc.funds import FUNDS
from data_doc.mandates_and_rules import MANDATES
from data_doc.portfolio_and_funds import (
    PORTFOLIO_FUNDS,
    PORTFOLIO_QUARTERLY_RETURNS,
    PORTFOLIOS,
)
from fastapi import APIRouter, HTTPException, Query
from helpers_and_compliance.helpers import find_one, next_id, remove_where, today
from helpers_and_compliance.helpers_and_compliance import (
    check_portfolio,
    check_proposed_fund,
)
from models import Allocations, PortfolioCreate, PortfolioPatch

from routers.common import (
    IdempotencyKey,
    get_fund_or_404,
    get_portfolio_or_404,
    must_exist,
    patch_record,
    remember,
    replay,
)

router = APIRouter(prefix="/portfolios", tags=["portfolios"])


def _with_allocations(portfolio: dict) -> dict:
    allocations = [{"fund_id": pf["fund_id"], "weight": pf["weight"]}
                   for pf in PORTFOLIO_FUNDS if pf["portfolio_id"] == portfolio["portfolio_id"]]
    return {**portfolio, "allocations": allocations}


def _require_allocations(portfolio: dict) -> None:
    # an empty portfolio would otherwise "pass" every rule, which is wrong, not compliant
    if find_one(PORTFOLIO_FUNDS, "portfolio_id", portfolio["portfolio_id"]) is None:
        raise HTTPException(status_code=409, detail="Portfolio has no allocations yet. "
                            f"PUT /portfolios/{portfolio['portfolio_id']}/allocations first")


@router.get("")
def list_portfolios(mandate_id: int | None = None, holds_fund: int | None = None):
    results = PORTFOLIOS
    if mandate_id is not None:
        results = [p for p in results if p["mandate_id"] == mandate_id]
    if holds_fund is not None:
        holders = {pf["portfolio_id"] for pf in PORTFOLIO_FUNDS if pf["fund_id"] == holds_fund}
        results = [p for p in results if p["portfolio_id"] in holders]
    return results


@router.get("/{portfolio_id}")
def get_portfolio(portfolio_id: int):
    return _with_allocations(get_portfolio_or_404(portfolio_id))


@router.post("", status_code=201)
def create_portfolio(new: PortfolioCreate, idempotency_key: str = IdempotencyKey):
    earlier = replay("portfolios", idempotency_key, new)
    if earlier is not None:
        return earlier
    must_exist(MANDATES, "mandate_id", new.mandate_id, "mandate")
    portfolio = {"portfolio_id": next_id(PORTFOLIOS, "portfolio_id"),
                 **new.model_dump(mode="json"),
                 "client_profile": None}    # recorded by an adviser, never by the API
    PORTFOLIOS.append(portfolio)
    response = _with_allocations(portfolio)
    remember("portfolios", idempotency_key, new, response)
    return response


@router.patch("/{portfolio_id}")
def update_portfolio(portfolio_id: int, changes: PortfolioPatch):
    portfolio = get_portfolio_or_404(portfolio_id)
    if changes.mandate_id is not None:
        must_exist(MANDATES, "mandate_id", changes.mandate_id, "mandate")
    return _with_allocations(patch_record(portfolio, changes, PortfolioCreate))


@router.put("/{portfolio_id}/allocations")
def replace_allocations(portfolio_id: int, body: Allocations):
    """Allocations only make sense as a complete set summing to 100, so this replaces all of them."""
    portfolio = get_portfolio_or_404(portfolio_id)
    for a in body.allocations:
        must_exist(FUNDS, "fund_id", a.fund_id, "fund")
    remove_where(PORTFOLIO_FUNDS, "portfolio_id", portfolio_id)
    first_id, as_at = next_id(PORTFOLIO_FUNDS, "portfolio_fund_id"), today().isoformat()
    for offset, a in enumerate(body.allocations):
        PORTFOLIO_FUNDS.append({"portfolio_fund_id": first_id + offset, "portfolio_id": portfolio_id,
                                "fund_id": a.fund_id, "weight": a.weight, "as_of_date": as_at})
    return _with_allocations(portfolio)


@router.delete("/{portfolio_id}", status_code=204)
def delete_portfolio(portfolio_id: int):
    PORTFOLIOS.remove(get_portfolio_or_404(portfolio_id))
    for table in (PORTFOLIO_FUNDS, PORTFOLIO_QUARTERLY_RETURNS):
        remove_where(table, "portfolio_id", portfolio_id)


@router.get("/{portfolio_id}/compliance")
def portfolio_compliance(portfolio_id: int):
    """PM: does this portfolio, as held today, meet its mandate?"""
    portfolio = get_portfolio_or_404(portfolio_id)
    _require_allocations(portfolio)
    return check_portfolio(portfolio)


@router.get("/{portfolio_id}/compliance/what-if")
def proposed_holding_compliance(portfolio_id: int, fund_id: int,
                                weight_pct: float = Query(gt=0, lt=100)):
    """PM: would adding this fund at this weight fit? Read-only: nothing is changed."""
    portfolio = get_portfolio_or_404(portfolio_id)
    get_fund_or_404(fund_id)
    _require_allocations(portfolio)
    return check_proposed_fund(portfolio, fund_id, weight_pct)