# This document contains both funds and holdings' CRUD
from typing import Literal

from fastapi import APIRouter, HTTPException, Query, Response, status
from pydantic import BaseModel, Field, model_validator

from wealth_management_api.documents.funds import FUNDS
from wealth_management_api.helpers.funds_helpers import (
    ensure_fund_not_held,
    find_fund_or_404,
    fund_name_exists,
)


router = APIRouter(
    prefix="/funds",
    tags=["Funds"],
)

class FundCreate(BaseModel):
    name: str
    strategy: str

    asset_class: Literal["equity", "fixed_income"]

    ongoing_charges_pct: float = Field(ge=0)
    estimated_transaction_costs_pct: float = Field(ge=0)

    risk_rating: int = Field(ge=1, le=7)

    esg_score: int | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    esg_score_status: Literal[
        "approved",
        "pending_review",
    ]

    benchmark: str
    currency: str
    currency_hedging: str

    holdings_as_of: str

    holdings_coverage_pct: float = Field(
        ge=0,
        le=100,
    )

    quarter_return_pct: float
    benchmark_quarter_return_pct: float
    trailing_12m_return_pct: float

    return_basis: str

    quarter_cost_drag_pp: float = Field(ge=0)

    performance_period_start: str
    performance_period_end: str

    @model_validator(mode="after")
    def validate_esg(self):
        if (
            self.esg_score_status == "approved"
            and self.esg_score is None
        ):
            raise ValueError(
                "esg_score is required when status is approved"
            )

        if (
            self.esg_score_status == "pending_review"
            and self.esg_score is not None
        ):
            raise ValueError(
                "esg_score must be null when status is pending_review"
            )

        return self
    
    
class FundPatch(BaseModel):
    name: str | None = None
    strategy: str | None = None

    asset_class: Literal[
        "equity",
        "fixed_income",
    ] | None = None

    ongoing_charges_pct: float | None = Field(
        default=None,
        ge=0,
    )

    estimated_transaction_costs_pct: float | None = Field(
        default=None,
        ge=0,
    )

    risk_rating: int | None = Field(
        default=None,
        ge=1,
        le=7,
    )

    esg_score: int | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    esg_score_status: Literal[
        "approved",
        "pending_review",
    ] | None = None

    benchmark: str | None = None
    currency: str | None = None
    currency_hedging: str | None = None

    holdings_as_of: str | None = None

    holdings_coverage_pct: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    quarter_return_pct: float | None = None
    benchmark_quarter_return_pct: float | None = None
    trailing_12m_return_pct: float | None = None

    return_basis: str | None = None

    quarter_cost_drag_pp: float | None = Field(
        default=None,
        ge=0,
    )

    performance_period_start: str | None = None
    performance_period_end: str | None = None


@router.get("")
def get_funds(
    asset_class: Literal[
        "equity",
        "fixed_income",
    ] | None = None,

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
        "pending_review",
    ] | None = None,

    max_ongoing_charges_pct: float | None = Query(
        default=None,
        ge=0,
    ),
):
    results = FUNDS

    if asset_class is not None:
        results = [
            fund for fund in results
            if fund["asset_class"] == asset_class
        ]

    if max_risk_rating is not None:
        results = [
            fund for fund in results
            if fund["risk_rating"] <= max_risk_rating
        ]

    if min_esg_score is not None:
        results = [
            fund for fund in results
            if fund["esg_score"] is not None
            and fund["esg_score"] >= min_esg_score
        ]

    if esg_score_status is not None:
        results = [
            fund for fund in results
            if fund["esg_score_status"] == esg_score_status
        ]

    if max_ongoing_charges_pct is not None:
        results = [
            fund for fund in results
            if fund["ongoing_charges_pct"]
            <= max_ongoing_charges_pct
        ]

    return results


@router.get("/{fund_id}")
def get_fund(fund_id: int):
    return find_fund_or_404(fund_id)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
def create_fund(fund: FundCreate):
    if fund_name_exists(fund.name):
        raise HTTPException(
            status_code=409,
            detail="Fund name already exists",
        )

    new_id = max(
        (existing["fund_id"] for existing in FUNDS),
        default=0,
    ) + 1

    new_fund = {
        "fund_id": new_id,
        **fund.model_dump(),
    }

    FUNDS.append(new_fund)

    return new_fund


@router.patch("/{fund_id}")
def update_fund(
    fund_id: int,
    updates: FundPatch,
):
    fund = find_fund_or_404(fund_id)

    update_data = updates.model_dump(
        exclude_unset=True
    )

    if (
        "name" in update_data
        and fund_name_exists(
            update_data["name"],
            exclude_fund_id=fund_id,
        )
    ):
        raise HTTPException(
            status_code=409,
            detail="Fund name already exists",
        )

    fund.update(update_data)

    return fund


@router.delete(
    "/{fund_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_fund(fund_id: int):
    fund = find_fund_or_404(fund_id)

    ensure_fund_not_held(fund_id)

    FUNDS.remove(fund)

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )