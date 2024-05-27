from pydantic import BaseModel
from typing import Optional


class LedgerHead(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    company: Optional[str] = None


class Receipt(BaseModel):
    id: str
    name: str
    date: str
    item: Optional[list]
