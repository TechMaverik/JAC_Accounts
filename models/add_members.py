from pydantic import BaseModel
from typing import Optional


class AddMembers(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    gender: Optional[str] = None
    dob: Optional[str] = None
    voting_power: Optional[str] = None
    married: Optional[str] = None
    contact_no: Optional[str] = None
    whatsapp_no: Optional[str] = None
    dom: Optional[str] = None
    spouse_name: Optional[str] = None
    nos_children: Optional[str] = None
    subscription: Optional[str] = None
