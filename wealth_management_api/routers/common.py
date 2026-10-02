"""Shared by every router: lookups, idempotency and the PATCH helper.
Lives in routers/ (not helpers) because it raises HTTPException."""

from data_doc.funds import FUNDS
from data_doc.mandates_and_rules import MANDATES
from data_doc.portfolio_and_funds import PORTFOLIOS
from fastapi import Header, HTTPException
from helpers_and_compliance.helpers import find_one
from pydantic import BaseModel, ValidationError

# ---------- lookups ----------

def get_or_404(records: list[dict], key: str, value: int, label: str) -> dict:
    record = find_one(records, key, value)
    if record is None:
        raise HTTPException(status_code=404, detail=f"No {label} with id {value}")
    return record


def get_fund_or_404(fund_id: int) -> dict:
    return get_or_404(FUNDS, "fund_id", fund_id, "fund")


def get_portfolio_or_404(portfolio_id: int) -> dict:
    return get_or_404(PORTFOLIOS, "portfolio_id", portfolio_id, "portfolio")


def get_mandate_or_404(mandate_id: int) -> dict:
    return get_or_404(MANDATES, "mandate_id", mandate_id, "mandate")


def must_exist(records: list[dict], key: str, value: int, label: str) -> None:
    """For ids inside a request body: a missing one makes the request invalid (422), not 404."""
    if find_one(records, key, value) is None:
        raise HTTPException(status_code=422, detail=f"No {label} with id {value}")


def ensure_unique_fund_name(name: str, exclude_fund_id: int | None = None) -> None:
    """Fund names must be unique: the agent finds funds by name, so duplicates are ambiguous."""
    wanted = name.strip().lower()
    for fund in FUNDS:
        if fund["name"].strip().lower() == wanted and fund["fund_id"] != exclude_fund_id:
            raise HTTPException(status_code=409, detail=f"A fund named '{name}' already exists")


# ---------- idempotency for POST ----------

IdempotencyKey = Header(alias="Idempotency-Key", min_length=1)

_idempotency: dict[str, dict] = {}   # "scope:key" -> {"request": ..., "response": ...}


def replay(scope: str, key: str, body: BaseModel) -> dict | None:
    """Return the earlier response if this key was seen before, otherwise None."""
    seen = _idempotency.get(f"{scope}:{key}")
    if seen is None:
        return None
    if seen["request"] != body.model_dump(mode="json"):
        raise HTTPException(status_code=422,
                            detail="Idempotency-Key was already used with a different request")
    return seen["response"]


def remember(scope: str, key: str, body: BaseModel, response: dict) -> None:
    # store a copy, so a later PATCH doesn't change what a retry returns
    _idempotency[f"{scope}:{key}"] = {"request": body.model_dump(mode="json"),
                                      "response": dict(response)}


# ---------- PATCH ----------

def patch_record(record: dict, changes: BaseModel, full_model: type[BaseModel]) -> dict:
    """Apply a partial update, then re-validate the WHOLE record against the full model,
    so cross-field rules (e.g. approved ESG needs a score) still hold after the change."""
    current = {k: record[k] for k in full_model.model_fields if k in record}
    merged = {**current}
    for key, value in changes.model_dump(exclude_unset=True).items():
        # nested objects (client_fees) are merged too, so unsent sub-fields keep their values
        if isinstance(value, dict) and isinstance(current.get(key), dict):
            merged[key] = {**current[key], **value}
        else:
            merged[key] = value
    try:
        valid = full_model(**merged)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors(include_url=False, include_context=False))
    record.update(valid.model_dump(mode="json"))   # mode="json": dates stored as "2026-09-30"
    return record