"""Mandate compliance engine. Plain Python: nothing here knows about FastAPI or Claude.

Implements the Responsible Investment and Exclusions Policy (document 12):
  3.2  look-through exposure = portfolio fund weight x fund holding weight / 100
  3.3  company exposure aggregated by issuer ID, never by name
  2.3  activity exposure from recorded tags only
  3.5  cash has no company, sector or activity exposure and is not fixed income
  3.6  limits are inclusive
  5    missing evidence is neither a pass nor a breach
"""

from datetime import date

import config
from data_doc.funds import FUNDS
from data_doc.holding_details import HOLDING_DETAILS
from data_doc.holdings import HOLDINGS
from data_doc.issuers import ISSUERS
from data_doc.mandates_and_rules import MANDATE_RULES, MANDATES
from data_doc.portfolio_and_funds import PORTFOLIO_FUNDS
from data_doc.securities import SECURITIES

from helpers_and_compliance.helpers import find_one, today

PASS, BREACH, INSUFFICIENT = "pass", "breach", "insufficient_evidence"

FIXED_INCOME_TYPES = {"corporate_bond", "government_bond"}
PORTFOLIO_LEVEL = {"activity_exclusion", "activity_exposure", "company_exposure",
                   "sector_exposure", "sector_exclusion", "asset_class_exposure"}
FUND_LEVEL = {"minimum_esg_score", "maximum_risk_rating", "maximum_fund_weight"}


def _within_limit(value: float, operator: str, limit: float) -> bool:
    value = round(value, 6)   # avoid 25.000000001 style float noise
    if operator == "<=":
        return value <= limit
    if operator == ">=":
        return value >= limit
    if operator == "=":
        return value == limit
    raise ValueError(f"Unknown operator {operator}")


def _overall(statuses: list[str]) -> str:
    if BREACH in statuses:
        return BREACH
    if INSUFFICIENT in statuses:
        return INSUFFICIENT
    return PASS


def look_through(allocations: list[dict]) -> tuple[list[dict], list[str]]:
    """Expand fund allocations into underlying positions at portfolio level.
    Returns (positions, problems). A problem is anything we cannot classify."""
    positions: list[dict] = []
    problems: list[str] = []
    for alloc in allocations:
        fund_holdings = [h for h in HOLDINGS if h["fund_id"] == alloc["fund_id"]]
        if not fund_holdings:
            problems.append(f"Fund {alloc['fund_id']} has no recorded holdings")
        for holding in fund_holdings:
            detail = find_one(HOLDING_DETAILS, "holding_id", holding["holding_id"])
            issuer = find_one(ISSUERS, "issuer_id", detail["issuer_id"]) if detail else None
            security = find_one(SECURITIES, "security_id", detail["security_id"]) if detail else None
            if issuer is None or security is None:
                problems.append(f"Holding {holding['holding_id']} ({holding['company_name']}) "
                                "cannot be classified")
                continue
            positions.append({
                "fund_id": alloc["fund_id"],
                "issuer_id": issuer["issuer_id"],
                "sector": issuer["sector"],
                "activity_tags": issuer["activity_tags"],
                "instrument_type": security["instrument_type"],
                "weight_pct": alloc["weight"] * holding["weight"] / 100,
            })
    return positions, problems


def _portfolio_exposure(rule: dict, positions: list[dict]) -> float:
    rule_type, target = rule["rule_type"], rule["target"]
    if rule_type in ("activity_exclusion", "activity_exposure"):
        matches = [p for p in positions if target in p["activity_tags"]]
    elif rule_type == "company_exposure":
        matches = [p for p in positions if p["issuer_id"] == rule["target_issuer_id"]]
    elif rule_type in ("sector_exposure", "sector_exclusion"):
        matches = [p for p in positions if p["sector"] == target]
    elif target == "fixed_income":          # asset_class_exposure
        matches = [p for p in positions if p["instrument_type"] in FIXED_INCOME_TYPES]
    else:                                   # asset_class_exposure: "equity" or "cash"
        matches = [p for p in positions if p["instrument_type"] == target]
    return round(sum(p["weight_pct"] for p in matches), 4)


def _fund_value(rule: dict, fund: dict, weight: float) -> float | None:
    if rule["rule_type"] == "maximum_fund_weight":
        return weight
    if rule["rule_type"] == "maximum_risk_rating":
        return fund["risk_rating"]
    # minimum_esg_score: only an approved score counts (doc 12 §4.2)
    return fund["esg_score"] if fund["esg_score_status"] == "approved" else None


def evaluate_rule(rule: dict, allocations: list[dict], positions: list[dict],
                  problems: list[str]) -> dict:
    result = {
        "rule_id": rule["rule_id"],
        "rule_type": rule["rule_type"],
        "target": rule["target"],
        "operator": rule["operator"],
        "limit": rule["limit"],
        "unit": rule["unit"],
        "source": f"document {rule['source_document_id']}, section {rule['source_section']}",
    }

    if rule["rule_type"] in PORTFOLIO_LEVEL:
        if problems:
            return {**result, "value": None, "status": INSUFFICIENT, "reason": "; ".join(problems)}
        value = _portfolio_exposure(rule, positions)
        status = PASS if _within_limit(value, rule["operator"], rule["limit"]) else BREACH
        return {**result, "value": value, "status": status}

    if rule["rule_type"] in FUND_LEVEL:
        per_fund = []
        for alloc in allocations:
            fund = find_one(FUNDS, "fund_id", alloc["fund_id"])
            fund_value = _fund_value(rule, fund, alloc["weight"]) if fund else None
            if fund_value is None:
                status = INSUFFICIENT
            else:
                status = PASS if _within_limit(fund_value, rule["operator"], rule["limit"]) else BREACH
            per_fund.append({"fund_id": alloc["fund_id"],
                             "fund_name": fund["name"] if fund else None,
                             "value": fund_value, "status": status})
        # assessed fund by fund, never averaged (doc 13 §2.3)
        return {**result, "status": _overall([f["status"] for f in per_fund]), "per_fund": per_fund}

    return {**result, "value": None, "status": INSUFFICIENT,
            "reason": f"Rule type {rule['rule_type']} is not supported by the engine"}


def _data_warnings(mandate: dict, allocations: list[dict]) -> list[str]:
    warnings: list[str] = []
    as_at = today()
    for alloc in allocations:
        fund = find_one(FUNDS, "fund_id", alloc["fund_id"])
        if fund is None:
            continue
        as_of = fund.get("holdings_as_of")
        if as_of is None:
            warnings.append(f"{fund['name']} has no recorded holdings date")
        elif (as_at - date.fromisoformat(as_of)).days > config.HOLDINGS_STALE_DAYS:
            warnings.append(f"{fund['name']} holdings are as of {as_of}, "
                            f"older than {config.HOLDINGS_STALE_DAYS} days")
    if date.fromisoformat(mandate["review_date"]) < as_at:
        warnings.append(f"Mandate review was due on {mandate['review_date']}")
    return warnings


def check_allocations(mandate: dict, allocations: list[dict]) -> dict:
    positions, problems = look_through(allocations)
    rules = [r for r in MANDATE_RULES if r["mandate_id"] == mandate["mandate_id"]]
    results = [evaluate_rule(r, allocations, positions, problems) for r in rules]
    statuses = [r["status"] for r in results]
    return {
        "mandate_id": mandate["mandate_id"],
        "mandate_name": mandate["name"],
        "overall_status": _overall(statuses),
        "breaches": statuses.count(BREACH),
        "insufficient_evidence": statuses.count(INSUFFICIENT),
        "rules": results,
        "data_warnings": _data_warnings(mandate, allocations),
        "note": ("Mandate compliance is not a suitability assessment. Breaches and "
                 "insufficient evidence are referred to the portfolio manager."),
    }


def _current_allocations(portfolio_id: int) -> list[dict]:
    return [{"fund_id": pf["fund_id"], "weight": pf["weight"]}
            for pf in PORTFOLIO_FUNDS if pf["portfolio_id"] == portfolio_id]


def _mandate_for(portfolio: dict) -> dict:
    mandate = find_one(MANDATES, "mandate_id", portfolio["mandate_id"])
    if mandate is None:
        raise ValueError(f"Portfolio {portfolio['portfolio_id']} points at an unknown mandate")
    return mandate


def check_portfolio(portfolio: dict) -> dict:
    """Does this portfolio, as held today, meet every rule in its mandate?"""
    return {
        "portfolio_id": portfolio["portfolio_id"],
        "client_name": portfolio["client_name"],
        **check_allocations(_mandate_for(portfolio), _current_allocations(portfolio["portfolio_id"])),
    }


def check_proposed_fund(portfolio: dict, fund_id: int, weight_pct: float) -> dict:
    """Would adding this fund at this weight keep the portfolio within its mandate?
    Assumption: the purchase is funded pro rata from existing holdings."""
    scale = (100 - weight_pct) / 100
    proposed = [{"fund_id": a["fund_id"], "weight": a["weight"] * scale}
                for a in _current_allocations(portfolio["portfolio_id"])]
    existing = find_one(proposed, "fund_id", fund_id)
    if existing is not None:
        existing["weight"] += weight_pct
    else:
        proposed.append({"fund_id": fund_id, "weight": weight_pct})

    return {
        "portfolio_id": portfolio["portfolio_id"],
        "client_name": portfolio["client_name"],
        "proposed_allocations": [{**a, "weight": round(a["weight"], 2)} for a in proposed],
        "assumption": "New fund funded pro rata from existing holdings",
        **check_allocations(_mandate_for(portfolio), proposed),
    }