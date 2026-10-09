from data import PEOPLE
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from .firms import get_firm_or_404

# router prefixes instead of @app
router = APIRouter(prefix="/people", tags=["people"])

class NewPerson(BaseModel):
    name: str = Field(min_length=1)
    role: str = Field(min_length=1)
    firm_id: int
    
def get_person_or_404(person_id: int) -> dict:
    for person in PEOPLE:
        if person["id"] == person_id:
            return person
    raise HTTPException(status_code=404, detail=f"No person with id {person_id} exists")
    
@router.get("/health")
def health():
    return{"status": "ok"}

@router.get("/{person_id}")
def get_firm(person: dict = Depends(get_person_or_404)):
    return person

@router.get("")
def list_people(firm_id: int | None=None):
    if firm_id is None:
        return PEOPLE
    return [p for p in PEOPLE if p["firm_id"] == firm_id]

# EOD Wednesday
'''
- Gone through all of CRUD - put, post, get, delete
- Refactored too
'''

#get person
@router.get("/{person_id}")
def get_person(person: dict = Depends(get_person_or_404)):
    return person

#add person
@router.post("", status_code=201)
def add_person(new: NewPerson):
    get_firm_or_404(new.firm_id)  # raises 404 if the firm doesn't exist
    new_id = max(person["id"] for person in PEOPLE) + 1
    person = {
        "id": new_id,
        "name": new.name,
        "role": new.role,
        "firm_id": new.firm_id,
    }
    PEOPLE.append(person)
    return person