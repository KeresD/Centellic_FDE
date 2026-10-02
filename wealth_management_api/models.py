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
    currency: str = Field(pattern=r"^[A-Z]{3}$")
    currency_hedging: str = Field(min_length=1)
    holdings_as_of: date
    holdings_coverage_pct: float = Field(ge=0, le=100)
    quarter_return_pct: float
    benchmark_quarter_return_pct: float
    trailing_12m_return_pct: float
    return_basis: str = Field(min_length=1)
    quarter_cost_drag_pp: float = Field(ge=0)
    performance_period_start: date
    performance_period_end: date

    @model_validator(mode="after")
    def consistency(self):
        if (self.esg_score_status == "approved") != (self.esg_score is not None):
            raise ValueError("Approved ESG requires a score; pending review requires a null score")
        if self.performance_period_end < self.performance_period_start:
            raise ValueError("Performance period end must follow its start")
        return self


class Fund(FundCreate):
    fund_id: int


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
    currency: str | None = None
    currency_hedging: str | None = None
    holdings_as_of: date | None = None
    holdings_coverage_pct: float | None = Field(default=None, ge=0, le=100)
    quarter_return_pct: float | None = None
    benchmark_quarter_return_pct: float | None = None
    trailing_12m_return_pct: float | None = None
    return_basis: str | None = None
    quarter_cost_drag_pp: float | None = Field(default=None, ge=0)
    performance_period_start: date | None = None
    performance_period_end: date | None = None


class Allocation(InputModel):
    fund_id: int = Field(gt=0)
    weight: float = Field(gt=0, le=100)


class Allocations(InputModel):
    allocations: list[Allocation] = Field(min_length=1)

    @model_validator(mode="after")
    def check_weights(self):
        if len({a.fund_id for a in self.allocations}) != len(self.allocations):
            raise ValueError("Duplicate funds are not allowed")
        if abs(sum(a.weight for a in self.allocations) - 100) > 1e-8:
            raise ValueError("Allocation weights must sum to 100%")
        return self


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


class PortfolioPatch(InputModel):
    name: str | None = None
    client_name: str | None = None
    mandate_id: int | None = None
    valuation_gbp: float | None = None
    as_of_date: date | None = None
    client_fees: ClientFees | None = None


class MandateCreate(InputModel):
    name: str = Field(min_length=1)
    client_name: str = Field(min_length=1)
    effective_date: date
    review_date: date
    version: str = Field(default="1.0", min_length=1)
    document_id: int = Field(gt=0)
    status: Literal["active", "inactive"] = "active"

    @model_validator(mode="after")
    def dates(self):
        if self.review_date < self.effective_date:
            raise ValueError("Review date must follow effective date")
        return self


class MandatePatch(InputModel):
    name: str | None = None
    client_name: str | None = None
    effective_date: date | None = None
    review_date: date | None = None
    version: str | None = None
    document_id: int | None = None
    status: Literal["active", "inactive"] | None = None


RuleType = Literal["activity_exclusion", "activity_exposure", "company_exposure", "sector_exposure",
                   "sector_exclusion", "minimum_esg_score", "maximum_risk_rating",
                   "maximum_fund_weight", "asset_class_exposure"]


class RuleCreate(InputModel):
    rule_type: RuleType
    target: str = Field(min_length=1)
    operator: Literal["<=", ">=", "="]
    limit: float = Field(ge=0, le=100)
    unit: Literal["percent", "score_0_100", "rating_1_7"]
    scope: Literal["portfolio", "each_fund"]
    source_document_id: int = Field(gt=0)
    source_section: str = Field(min_length=1)
    source_clause_text: str = Field(min_length=1)
    target_issuer_id: int | None = Field(default=None, gt=0)

    @model_validator(mode="after")
    def semantics(self):
        expected = {
            "minimum_esg_score": (">=", "score_0_100", "each_fund"),
            "maximum_risk_rating": ("<=", "rating_1_7", "each_fund"),
            "maximum_fund_weight": ("<=", "percent", "each_fund"),
            "activity_exclusion": ("=", "percent", "portfolio"),
            "sector_exclusion": ("=", "percent", "portfolio"),
        }
        contract = expected.get(self.rule_type)
        if contract and (self.operator, self.unit, self.scope) != contract:
            raise ValueError(f"Invalid operator/unit/scope for {self.rule_type}")
        if not contract and (self.unit != "percent" or self.scope != "portfolio"):
            raise ValueError("Exposure rules use portfolio percentages")
        if not contract and self.operator == "=":
            raise ValueError("Exposure rules require <= or >=")
        if self.rule_type.endswith("exclusion") and self.limit != 0:
            raise ValueError("Exclusions require a zero limit")
        if self.rule_type == "maximum_risk_rating" and not 1 <= self.limit <= 7:
            raise ValueError("Risk limit must be between 1 and 7")
        if self.rule_type == "company_exposure" and self.target_issuer_id is None:
            raise ValueError("Company exposure requires an explicit issuer ID")
        if self.rule_type == "asset_class_exposure" and self.target not in {"equity", "fixed_income", "cash"}:
            raise ValueError("Unknown underlying asset class")
        return self


class AskRequest(InputModel):
    question: str = Field(min_length=1, max_length=2000)


class ScreenInput(InputModel):
    portfolio_id: int = Field(gt=0)
    mandate_id: int | None = Field(default=None, gt=0)


class SearchInput(InputModel):
    query: str = Field(min_length=1, max_length=2000)


class FundAssessment(InputModel):
    strengths: list[str] = Field(max_length=5)
    risks: list[str] = Field(max_length=5)
    fee_observations: list[str] = Field(max_length=5)
    esg_observations: list[str] = Field(max_length=5)
    evidence_gaps: list[str] = Field(max_length=5)