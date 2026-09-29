
from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, Field

from data import FIRMS

# router prefixes instead of @app
router = APIRouter(prefix="/firms", tags=["firm"])

_seen_keys: dict[str, dict] = {}

class NewFirm(BaseModel):
    # name, jurisdiction, revenue_usd_m, lawyers, equity_partners
    # lawyers, ep being set to greater than 0 because logically firms cannot have 0 lawyers,
    # and doesn't make any sense to have 0 ep - also avoids division error
    name: str = Field(min_length=1)
    jurisdiction: str = Field(min_length=2, max_length=5)
    revenue_usd_m: float = Field(gt=0)
    lawyers: int = Field(gt=0)
    equity_partners: int = Field(gt=0)
    
def get_firm_or_404(firm_id: int) -> dict:
    for firm in FIRMS:
        if firm["id"] == firm_id:
            return firm
    raise HTTPException(status_code=404, detail=f"No firm with id {firm_id} exists")

# decorator that registers function below it as the handler for GET request to the /health path
@router.get("/health")
# handler function. Take no params and returns python dict, which fastapi automatically serialises to JSON
# so get/health requet returns
def health():
    return{"status": "ok"} #json

@router.get("/{firm_id}")
def get_firm(firm: dict = Depends(get_firm_or_404)):
    return firm


@router.get("")
def list_firms(jurisdiction: str | None = None, min_lawyers: int | None = None):
    results = FIRMS
    errors = []
    
    '''if jurisdiction is not None:
        results = [firm for firm in results if firm["jurisdiction"] == jurisdiction]'''
    
    if jurisdiction is not None:
        known_jurisdictions = {firm["jurisdiction"] for firm in FIRMS}
        if jurisdiction not in known_jurisdictions:
            errors.append(f"No jurisdiction named '{jurisdiction}' found")
           
    '''if min_lawyers is not None:
    results = [firm for firm in results if firm["lawyers"] >= min_lawyers]'''
                
    if min_lawyers is not None and min_lawyers < 0:
        errors.append(" min_lawyers cannot have negative values")

    if errors:
        raise HTTPException(status_code=422, detail=errors)
    
    if jurisdiction is not None:
        results = [firm for firm in results if firm["jurisdiction"] == jurisdiction]
    
    if min_lawyers is not None:
        results = [firm for firm in results if firm["lawyers"] >= min_lawyers]
    
    return results

@router.get("/{firm_id}/benchmarks")
def get_benchmarks(firm: dict = Depends(get_firm_or_404)):
    revenue = firm["revenue_usd_m"]
    return {
            # id
            "id": firm["id"],
            # name
            "name": firm["name"],
            # rev per lawyer rev * 1,000,000 because revenue is in usd but also usd_m = millions
            # 1_000_000 = for readability - doesn't affect python to jst write 1000000
            "revenue_per_lawyer_usd": 
                round(revenue * 1_000_000 / firm["lawyers"]),
            # profit per ep (equity partner) — 0.35 assumed margin, no cost data in FIRMS
            "profit_per_equity_partner": 
                round(revenue * 1_000_000 * 0.35 / firm["equity_partners"]),
        }
    
'''@router.post("", status_code=201)
def add_firm(new: NewFirm):
    new_id = max(firm["id"] for firm in FIRMS) + 1
    firm = {
        "id": new_id,
        "name": new.name,
        "jurisdiction": new.jurisdiction,
        "revenue_usd_m": new.revenue_usd_m,
        "lawyers": new.lawyers,
        "equity_partners": new.equity_partners
    }
    FIRMS.append(firm)
    return firm'''

# post
# /firms
@router.post("", status_code=201)
def add_firm(new: NewFirm, idempotency_key: str | None = Header(default=None)):
    if idempotency_key is not None and idempotency_key in _seen_keys:
        return _seen_keys[idempotency_key]
    new_id = max(firm["id"] for firm in FIRMS) + 1
    firm = {
        "id": new_id,
        "name": new.name,
        "jurisdiction": new.jurisdiction,
        "revenue_usd_m": new.revenue_usd_m,
        "lawyers": new.lawyers,
        "equity_partners": new.equity_partners
    }
    FIRMS.append(firm)
    if idempotency_key is not None:
        _seen_keys[idempotency_key] = firm
    return firm

@router.put("/{firm_id}")
def update_firm(updated: NewFirm, firm: dict = Depends(get_firm_or_404)):
    """CHALLENGE 1 - replace a firm's data.
    Requirements:
      - Body is validated the same way as POST /firms (how did we do this before?).
      - Update `firm`'s fields *in place* so the change persists for later
        requests (the same idea as add_firm appending to FIRMS - mutate
        the existing dict, don't just return a new one).
      - Return the updated firm.
      - Status code 200 (the default - no status_code= needed).
    """
    firm["name"] = updated.name
    firm["jurisdiction"] = updated.jurisdiction
    firm["revenue_usd_m"] = updated.revenue_usd_m
    firm["lawyers"] = updated.lawyers
    firm["equity_partners"] = updated.equity_partners
    return firm

# could also write above like this:
'''@app.put("/firms/{firm_id}")
def update_firm(updated: NewFirm, firm: dict = Depends(get_firm_or_404)):
    firm.update(updated.model_dump())
    return firm'''

@router.delete("/{firm_id}", status_code=204)
def delete_firm(firm: dict = Depends(get_firm_or_404)):
    """CHALLENGE 2 - remove a firm.
    Requirements:
      - `firm` is already looked up and guaranteed to exist.
      - Remove it from the FIRMS list.
      - Return nothing (a 204 response must have an empty body - a bare
        `return` is enough; FastAPI handles the rest because of
        status_code=204 above).
    """
    FIRMS.remove(firm)
