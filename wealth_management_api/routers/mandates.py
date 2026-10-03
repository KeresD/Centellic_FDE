"""Mandate records and their rules. Rules have no PATCH: a changed clause is a delete plus a create."""

from data_doc.documents import DOCUMENTS
from data_doc.issuers import ISSUERS
from data_doc.mandates_and_rules import MANDATE_RULES, MANDATES
from data_doc.portfolio_and_funds import PORTFOLIOS
from fastapi import APIRouter, HTTPException
from helpers_and_compliance.helpers import find_one, next_id, remove_where
from models import MandateCreate, MandatePatch, RuleCreate

from routers.common import (
    IdempotencyKey,
    get_mandate_or_404,
    must_exist,
    patch_record,
    remember,
    replay,
)

router = APIRouter(prefix="/mandates", tags=["mandates"])


@router.get("")
def list_mandates(status: str | None = None):
    return [m for m in MANDATES if status is None or m["status"] == status]


@router.get("/{mandate_id}")
def get_mandate(mandate_id: int):
    return get_mandate_or_404(mandate_id)


@router.post("", status_code=201)
def create_mandate(new: MandateCreate, idempotency_key: str = IdempotencyKey):
    earlier = replay("mandates", idempotency_key, new)
    if earlier is not None:
        return earlier
    must_exist(DOCUMENTS, "document_id", new.document_id, "document")
    mandate = {"mandate_id": next_id(MANDATES, "mandate_id"), **new.model_dump(mode="json")}
    MANDATES.append(mandate)
    remember("mandates", idempotency_key, new, mandate)
    return mandate


@router.patch("/{mandate_id}")
def update_mandate(mandate_id: int, changes: MandatePatch):
    mandate = get_mandate_or_404(mandate_id)
    if changes.document_id is not None:
        must_exist(DOCUMENTS, "document_id", changes.document_id, "document")
    return patch_record(mandate, changes, MandateCreate)


@router.delete("/{mandate_id}", status_code=204)
def delete_mandate(mandate_id: int):
    mandate = get_mandate_or_404(mandate_id)
    if find_one(PORTFOLIOS, "mandate_id", mandate_id) is not None:
        raise HTTPException(status_code=409,
                            detail="Mandate is still used by a portfolio. Set status to inactive instead")
    MANDATES.remove(mandate)
    remove_where(MANDATE_RULES, "mandate_id", mandate_id)


@router.get("/{mandate_id}/rules")
def get_mandate_rules(mandate_id: int, rule_type: str | None = None):
    get_mandate_or_404(mandate_id)
    return [r for r in MANDATE_RULES
            if r["mandate_id"] == mandate_id and (rule_type is None or r["rule_type"] == rule_type)]


@router.post("/{mandate_id}/rules", status_code=201)
def create_rule(mandate_id: int, new: RuleCreate, idempotency_key: str = IdempotencyKey):
    get_mandate_or_404(mandate_id)
    scope = f"rules:{mandate_id}"
    earlier = replay(scope, idempotency_key, new)
    if earlier is not None:
        return earlier
    must_exist(DOCUMENTS, "document_id", new.source_document_id, "document")
    if new.target_issuer_id is not None:
        must_exist(ISSUERS, "issuer_id", new.target_issuer_id, "issuer")
    rule = {"rule_id": next_id(MANDATE_RULES, "rule_id"), "mandate_id": mandate_id,
            **new.model_dump(mode="json")}
    MANDATE_RULES.append(rule)
    remember(scope, idempotency_key, new, rule)
    return rule


@router.delete("/{mandate_id}/rules/{rule_id}", status_code=204)
def delete_rule(mandate_id: int, rule_id: int):
    get_mandate_or_404(mandate_id)
    rule = find_one(MANDATE_RULES, "rule_id", rule_id)
    if rule is None or rule["mandate_id"] != mandate_id:
        raise HTTPException(status_code=404, detail=f"No rule {rule_id} on mandate {mandate_id}")
    MANDATE_RULES.remove(rule)