"""Validated API inputs shared by routers and tools."""
from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

AssetClass = Literal["equity", "fixed_income"]


class InputModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, allow_inf_nan=False)


class FundCreate(InputModel):
    name: str = Field(min_length=1)
    strategy: str = Field(min_length=1)
    asset_class: AssetClass
    ongoing_charges_pct: float = Field(ge=0)
    estimated_transaction_costs_pct: float = Field(ge=0)
    risk_rating: int = Field(ge=1, le=7)
    esg_score: int | None = Field(default=None, ge=0, le=100)
    esg_score_status: Literal["approved", "pending_review"]
    benchmark: str = Field(min_length=1)
    currency_hedging: str = Field(min_length=1)
    period: str = Field(min_length=1)
    quarter_return_pct: float
    benchmark_quarter_return_pct: float
    trailing_12m_return_pct: float
    quarter_cost_drag_pp: float = Field(ge=0)
    holdings_as_of: date

    @model_validator(mode="after")
    def esg_consistency(self):
        if(self.esg_score_status == "approved") != (self.esg_score is not None):
            raise ValueError("Approved ESG requires a score; pending review requires a null score.")
        return self


class FundPatch(InputModel):
    name: str | None = None
    strategy: str | None = None
    asset_class: AssetClass | None = None
    ongoing_charges_pct: float | None = Field(default=None, ge=0)
    estimated_transaction_costs_pct: float | None = Field(default=None, ge=0)
    risk_rating: int | None = Field(default=None, ge=1, le=7)
    esg_score: int | None = Field(default=None, ge=0, le=100)
    esg_score_status: Literal["approved", "pending_review"] | None = None
    benchmark: str | None = None
    currency_hedging: str | None = None
    period: str | None = None
    quarter_return_pct: float | None = None
    benchmark_quarter_return_pct: float | None = None
    trailing_12m_return_pct: float | None = None
    quarter_cost_drag_pp: float | None = Field(default=None, ge=0)
    holdings_as_of: date | None = None


class Allocation(InputModel):
    fund_id: int = Field(gt=0)
    weight: float = Field(gt=0, le=100)

class ClientFees(InputModel):
    adviser_fee_pct_pa: float = Field(default=0, ge=0, le=100)
    platform_fee_pct_pa: float = Field(default=0, ge=0, le=100)

class PortfolioCreate(InputModel):
    name: str = Field(min_length=1)
    client_name: str = Field(min_length=1)
    mandate_id: int = Field(gt=0)
    valuation_gbp: float = Field(gt=0)
    as_of_date: date
    client_fees: ClientFees = Field(default_factory=ClientFees)
    # required, so an empty portfolio can never "pass" every mandate rule
    allocations: list[Allocation] = Field(min_length=1)
    
    @model_validator(mode="after")
    def check_weight(self):
        if len({a.fund_id for a in self.allocations}) != len(self.allocations):
            raise ValueError("Duplicate funds are not allowed.")
        if abs(sum(a.weight for a in self.allocations) - 100) > 1e-8:
            raise ValueError("Allocations weights must sum to 100%.")
        return self


class PortfolioPatch(InputModel):
    name: str | None = None
    client_name: str | None = None
    mandate_id: int | None = None
    valuation_gbp: float | None = None
    as_of_date: date | None = None
    client_fees: ClientFees | None = None
    # replaces whole list, then rechecked
    allocations: list[Allocation] | None = None 


class AskRequest(InputModel):
    question: str = Field(min_length=1, max_length=2000)


class ScreenInput(InputModel):
    client_name: str = Field(min_length=1)
    fund_name: str | None = Field(default=None, min_length=1)
    weight_pct: float | None = Field(default=None, gt=0, lt=100)

    @model_validator(mode="after")
    def fund_and_weight_together(self):
        if (self.fund_name is None) != (self.weight_pct is None):
            raise ValueError("fund_name and weight_pct must be given together")
        return self


class SearchInput(InputModel):
    query: str = Field(min_length=1, max_length=2000)


class FundAssessment(InputModel):
    strengths: list[str] = Field(max_length=5)
    risks: list[str] = Field(max_length=5)
    fee_observations: list[str] = Field(max_length=5)
    esg_observations: list[str] = Field(max_length=5)
    evidence_gaps: list[str] = Field(max_length=5)