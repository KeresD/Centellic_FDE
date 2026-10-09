"""Portfolio records: CRUD with TWO filters, Allocations = inside each portfolio"""

from data_doc.data import FUNDS, MANDATES, PORTFOLIOS
from fastapi import APIRouter
from helpers_and_compliance.helpers import next_id
from models import Allocation, PortfolioCreate, PortfolioPatch

from routers.common import (
    IdempotencyKey,
    get_portfolio_or_404,
    must_exist,
    patch_record,
    remember,
    replay,
)

router = APIRouter(prefix="/portfolios", tags=["portfolios"])


def _check_ids(mandate_id: int | None, allocations: list[Allocation] | None) -> None:
    if mandate_id is not None:
        must_exist(MANDATES, "mandate_id", mandate_id, "mandate")
    for a in allocations or []:
        must_exist(FUNDS, "fund_id", a.fund_id, "fund")


@router.get("")
def list_portfolios(mandate_id: int | None = None, holds_fund: int | None = None):
    results = PORTFOLIOS
    if mandate_id is not None:
        results = [p for p in results if p["mandate_id"] == mandate_id]
    if holds_fund is not None:
        results = [p for p in results if any(a["fund_id"] == holds_fund for a in p["allocations"])]
    return results


@router.get("/{portfolio_id}")
def get_portfolio(portfolio_id: int):
    return get_portfolio_or_404(portfolio_id)


@router.post("", status_code=201)
def create_portfolio(new: PortfolioCreate, idempotency_key: str = IdempotencyKey):
    earlier = replay("portfolios", idempotency_key, new)
    if earlier is not None:
        return earlier
    _check_ids(new.mandate_id, new.allocations)
    portfolio = {"portfolio_id": next_id(PORTFOLIOS, "portfolio_id"), **new.model_dump(mode="json")}
    PORTFOLIOS.append(portfolio)
    remember("portfolios", idempotency_key, new, portfolio)
    return portfolio


@router.patch("/{portfolio_id}")
def update_portfolio(portfolio_id: int, changes: PortfolioPatch):
    portfolio = get_portfolio_or_404(portfolio_id)
    _check_ids(changes.mandate_id, changes.allocations)
    return patch_record(portfolio, changes, PortfolioCreate)


@router.delete("/{portfolio_id}", status_code=204)
def delete_portfolio(portfolio_id: int):
    PORTFOLIOS.remove(get_portfolio_or_404(portfolio_id))