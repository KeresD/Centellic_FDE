"""Extract a monetary amount from a line of text, using a model.

LEARNER STARTER. SYNTHETIC PLACEHOLDER DATA ONLY.

This module currently does the naive thing. It runs. It is also untestable and
unsafe, in ways the three gates from Day 1 will only partly catch.
"""
import re
from decimal import Decimal

from pydantic import BaseModel, field_validator

from model_client import ModelClient


#ModelRefused Class
class ModelRefused(Exception):
    """Raised when the model's reply contains no JSON to extract."""

# ModelContractViolation: raised when the model's reply doesn't match the expected shape.
class ModelContractViolation(Exception):
     """Raised when the reply is JSON but doesn't match the expected shape."""
     
class ModelReply(BaseModel):
    amount:Decimal
    
    @field_validator("amount", mode="before")
    @classmethod
    def reject_float(cls, value: object) -> object:
        if isinstance(value, float):
            raise ValueError("amount must arrive as a string, not a float")
        return value        

def extract_amount(line: str, client: ModelClient) -> Decimal:
    reply = client.complete(f"What is the amount on this line? {line}")
    _JSON_OBJECT = re.compile(r"\{.*\}", re.DOTALL)
    
    match = _JSON_OBJECT.search(reply)
    if match is None:
        raise ModelRefused(reply.strip()[:200])
    return ModelReply.model_validate_json(match.group(0)).amount