"""Fund records: CRUD with TWO filters and holdings = in each fund."""

from data_doc.data import FUNDS, PORTFOLIOS
from fastapi import APIRouter, HTTPException, Query
from helpers_and_compliance.helpers import next_id
from models import AssetClass, FundCreate, FundPatch

from routers.common import (
    IdempotencyKey,
    ensure_unique_fund_name,
    get_fund_or_404,
    patch_record,
    remember,
    replay,
)

router = APIRouter(prefix="/funds", tags=["funds"])


@router.get("")
def list_funds(asset_class: AssetClass | None = None,
               max_risk_rating: int | None = Query(default=None, ge=1, le=7)):
    results = FUNDS
    if asset_class is not None:
        results = [f for f in results if f["asset_class"] == asset_class]
    if max_risk_rating is not None:
        results = [f for f in results if f["risk_rating"] <= max_risk_rating]
    return results


@router.get("/{fund_id}")
def get_fund(fund_id: int):
    return get_fund_or_404(fund_id)


@router.post("", status_code=201)
def create_fund(new: FundCreate, idempotency_key: str = IdempotencyKey):
    # replay first: a retried create must return the original, not a 409 for its own name
    earlier = replay("funds", idempotency_key, new)
    if earlier is not None:
        return earlier
    ensure_unique_fund_name(new.name)
    fund = {"fund_id": next_id(FUNDS, "fund_id"), **new.model_dump(mode="json"), "holdings": []}
    FUNDS.append(fund)
    remember("funds", idempotency_key, new, fund)
    return fund


@router.patch("/{fund_id}")
def update_fund(fund_id: int, changes: FundPatch):
    fund = get_fund_or_404(fund_id)
    if changes.name is not None:
        ensure_unique_fund_name(changes.name, exclude_fund_id=fund_id)
    return patch_record(fund, changes, FundCreate)


@router.delete("/{fund_id}", status_code=204)
def delete_fund(fund_id: int):
    fund = get_fund_or_404(fund_id)
    if any (a["fund_id"] == fund_id for p in PORTFOLIOS for a in p["allocations"]):
        raise HTTPException(status_code=409, detail="Fund is still held in a client portfolio.")
    # since holdings live inside, they get deleted too
    FUNDS.remove(fund)