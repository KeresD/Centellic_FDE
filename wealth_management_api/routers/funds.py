# This document contains both funds and holdings' CRUD
from typing import Any, Literal
from fastapi import APIRouter, HTTPException, Query

from wealth_management_api.documents.funds import FUNDS

''' routers/funds.py
- GET /funds  - filter --> ?asset_class, max_risk_rating, min_esg_score, esg_score_status, max_ongoing_charges_pct
- GET /funds/{fund_id}
- GET /funds/{id}/performance --> maybe to see how the fund performing in x amount of time
- POST /funds
- PATCH /funds/{fund_id}
- DELETE /funds/{fund_id}

Validations:
- fund_id not found --> error 404
- bad formatting --> return 422
- deleting a fund still held in portfolio --> returns 409

- asset_class must be equity or fixed_income.
- risk_rating must be an integer from 1 to 7.
- esg_score_status must be approved or pending_review.
- If the status is approved, esg_score is required and must be 0–100.
- If the status is pending_review, esg_score must be null.
- Charges must be ≥ 0.
- holdings_coverage_pct must be 0–100.
- performance_period_start must be on or before performance_period_end.
- name must be unique (case-insensitive).

'''

router = APIRouter(
    prefix="/funds",
    tags=["Funds"],
)


def find_fund_or_404(fund_id: int) -> dict[str, Any]:
    for fund in FUNDS:
        if fund["fund_id"] == fund_id:
            return fund

    raise HTTPException(
        status_code=404,
        detail=f"Fund {fund_id} not found",
    )


@router.get("")
def get_funds(
    asset_class: Literal["equity", "fixed_income"] | None = None,

    max_risk_rating: int | None = Query(
        default=None,
        ge=1,
        le=7,
    ),

    min_esg_score: int | None = Query(
        default=None,
        ge=0,
        le=100,
    ),

    esg_score_status: Literal[
        "approved",
        "pending_review"
    ] | None = None,

    max_ongoing_charges_pct: float | None = Query(
        default=None,
        ge=0,
    ),
):
    results = FUNDS

    if asset_class is not None:
        results = [
            fund
            for fund in results
            if fund["asset_class"] == asset_class
        ]

    if max_risk_rating is not None:
        results = [
            fund
            for fund in results
            if fund["risk_rating"] <= max_risk_rating
        ]

    if min_esg_score is not None:
        results = [
            fund
            for fund in results
            if fund["esg_score"] is not None
            and fund["esg_score"] >= min_esg_score
        ]

    if esg_score_status is not None:
        results = [
            fund
            for fund in results
            if fund["esg_score_status"] == esg_score_status
        ]

    if max_ongoing_charges_pct is not None:
        results = [
            fund
            for fund in results
            if fund["ongoing_charges_pct"]
            <= max_ongoing_charges_pct
        ]

    return results


@router.get("/{fund_id}")
def get_fund(fund_id: int):
    return find_fund_or_404(fund_id)